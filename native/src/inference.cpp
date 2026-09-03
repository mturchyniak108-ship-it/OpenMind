#include "openmind/inference.h"

#include "ggml-backend.h"
#include "llama.h"

#include <chrono>
#include <cstdint>
#include <cstring>
#include <memory>
#include <mutex>
#include <stdexcept>
#include <utility>
#include <vector>

namespace openmind {

namespace {

using Clock = std::chrono::steady_clock;

double elapsed_ms(Clock::time_point start, Clock::time_point end) {
    return std::chrono::duration<double, std::milli>(end - start).count();
}

} // namespace

struct InferenceEngine::Impl {
    explicit Impl(const InferenceConfig& config)
        : config(config) {}

    ~Impl() {
        if (sampler) {
            llama_sampler_free(sampler);
        }

        if (ctx) {
            llama_free(ctx);
        }

        if (model) {
            llama_model_free(model);
        }

        if (backend_initialized) {
            llama_backend_free();
        }
    }

    InferenceConfig config;

    llama_model* model = nullptr;
    llama_context* ctx = nullptr;
    llama_sampler* sampler = nullptr;

    const llama_vocab* vocab = nullptr;

    bool backend_initialized = false;
    bool loaded = false;
    double model_load_ms = 0.0;

    /*
     * The llama context, model, and engine sampler are shared
     * across OpenMind sessions. Serialize access to the native
     * inference runtime until explicit concurrent execution
     * semantics are established.
     */
    mutable std::mutex inference_mutex;
};

InferenceEngine::InferenceEngine(const InferenceConfig& config)
    : impl_(std::make_unique<Impl>(config)) {}

InferenceEngine::~InferenceEngine() = default;

bool InferenceEngine::load() {
    if (!impl_ ||
        impl_->config.model_path.empty() ||
        impl_->config.context_size == 0 ||
        impl_->config.max_tokens == 0 ||
        impl_->config.max_sessions == 0 ||
        impl_->config.gpu_layers >
            static_cast<uint32_t>(INT32_MAX)) {
        return false;
    }

    /*
     * Model/context initialization mutates the same native runtime
     * state used by inference and session lifecycle operations.
     * Serialize initialization with those operations.
     */
    std::lock_guard<std::mutex> lock(
        impl_->inference_mutex);

    if (impl_->loaded) {
        return true;
    }

    ggml_backend_load_all();
    llama_backend_init();
    impl_->backend_initialized = true;

    const auto load_start = Clock::now();

    llama_model_params model_params =
        llama_model_default_params();

    model_params.n_gpu_layers =
        static_cast<int32_t>(impl_->config.gpu_layers);

    impl_->model =
        llama_model_load_from_file(
            impl_->config.model_path.c_str(),
            model_params);

    if (!impl_->model) {
        if (impl_->backend_initialized) {
            llama_backend_free();
            impl_->backend_initialized = false;
        }
        return false;
    }

    impl_->vocab =
        llama_model_get_vocab(impl_->model);

    llama_context_params ctx_params =
        llama_context_default_params();

    ctx_params.n_ctx =
        impl_->config.context_size;

    /*
     * Support independent llama sequence state for multiple
     * OpenMind Session instances.
     */
    ctx_params.n_seq_max =
        impl_->config.max_sessions;

    /*
     * Use llama.cpp unified KV storage when requested.
     * This allows each OpenMind session to address the
     * full configured context instead of partitioning
     * it across max_sessions.
     */
    ctx_params.kv_unified =
        impl_->config.kv_unified;

    /*
     * Keep the batch large enough for the configured context.
     * The actual prompt batch is still limited by the prompt size.
     */
    ctx_params.n_batch =
        std::max<uint32_t>(impl_->config.context_size, 32u);

    impl_->ctx =
        llama_init_from_model(
            impl_->model,
            ctx_params);

    if (!impl_->ctx) {
        llama_model_free(impl_->model);
        impl_->model = nullptr;
        impl_->vocab = nullptr;

        if (impl_->backend_initialized) {
            llama_backend_free();
            impl_->backend_initialized = false;
        }

        return false;
    }

    llama_sampler_chain_params sampler_params =
        llama_sampler_chain_default_params();

    impl_->sampler =
        llama_sampler_chain_init(sampler_params);

    if (!impl_->sampler) {
        llama_free(impl_->ctx);
        impl_->ctx = nullptr;

        llama_model_free(impl_->model);
        impl_->model = nullptr;
        impl_->vocab = nullptr;

        if (impl_->backend_initialized) {
            llama_backend_free();
            impl_->backend_initialized = false;
        }

        return false;
    }

    llama_sampler_chain_add(
        impl_->sampler,
        llama_sampler_init_greedy());

    const auto load_end = Clock::now();

    impl_->model_load_ms =
        elapsed_ms(load_start, load_end);

    impl_->loaded = true;

    return true;
}

InferenceResult InferenceEngine::generate(
    const std::string& prompt) {

    if (!loaded()) {
        throw std::runtime_error(
            "OpenMind inference engine is not loaded");
    }

    if (prompt.empty()) {
        throw std::invalid_argument(
            "OpenMind inference prompt is empty");
    }

    /*
     * The llama context and engine sampler are shared runtime
     * state. Serialize the complete inference transaction so
     * another request cannot interleave token sampling,
     * decoding, or KV-cache mutation.
     */
    std::lock_guard<std::mutex> lock(
        impl_->inference_mutex);

    /*
     * Each generate() call is an independent inference request.
     * Clear the previous KV-cache/memory state before evaluating
     * the new prompt. Explicit conversational state can be added
     * later as a separate session API.
     */
    llama_memory_clear(
        llama_get_memory(impl_->ctx),
        true);

    InferenceResult result;

    const auto total_start = Clock::now();

    /*
     * Determine prompt token count.
     */
    int n_prompt =
        -llama_tokenize(
            impl_->vocab,
            prompt.c_str(),
            prompt.size(),
            nullptr,
            0,
            true,
            true);

    if (n_prompt <= 0) {
        throw std::runtime_error(
            "Failed to determine prompt token count");
    }

    std::vector<llama_token> tokens(
        static_cast<size_t>(n_prompt));

    const int tokenized =
        llama_tokenize(
            impl_->vocab,
            prompt.c_str(),
            prompt.size(),
            tokens.data(),
            tokens.size(),
            true,
            true);

    if (tokenized < 0) {
        throw std::runtime_error(
            "Prompt tokenization failed");
    }

    result.metrics.prompt_tokens =
        static_cast<uint32_t>(n_prompt);

    /*
     * Evaluate prompt.
     */
    const auto prompt_start = Clock::now();

    llama_batch batch =
        llama_batch_get_one(
            tokens.data(),
            tokens.size());

    if (llama_decode(impl_->ctx, batch) != 0) {
        throw std::runtime_error(
            "llama_decode(prompt) failed");
    }

    const auto prompt_end = Clock::now();

    result.metrics.prompt_eval_ms =
        elapsed_ms(prompt_start, prompt_end);

    if (result.metrics.prompt_eval_ms > 0.0) {
        result.metrics.prompt_tokens_per_second =
            (static_cast<double>(n_prompt) /
             result.metrics.prompt_eval_ms) *
            1000.0;
    }

    /*
     * Generate response.
     */
    const auto generation_start = Clock::now();

    std::string output;
    uint32_t generated = 0;

    for (uint32_t i = 0;
         i < impl_->config.max_tokens;
         ++i) {

        const llama_token token =
            llama_sampler_sample(
                impl_->sampler,
                impl_->ctx,
                -1);

        if (llama_vocab_is_eog(
                impl_->vocab,
                token)) {
            break;
        }

        char piece[256];

        const int n =
            llama_token_to_piece(
                impl_->vocab,
                token,
                piece,
                sizeof(piece),
                0,
                true);

        if (n < 0) {
            throw std::runtime_error(
                "Token-to-piece conversion failed");
        }

        output.append(piece, static_cast<size_t>(n));
        ++generated;

        llama_token next_token = token;

        batch =
            llama_batch_get_one(&next_token, 1);

        if (llama_decode(
                impl_->ctx,
                batch) != 0) {

            throw std::runtime_error(
                "llama_decode(generation) failed");
        }
    }

    const auto generation_end = Clock::now();
    const auto total_end = Clock::now();

    result.text = std::move(output);

    result.metrics.generated_tokens = generated;

    result.metrics.generation_ms =
        elapsed_ms(
            generation_start,
            generation_end);

    result.metrics.total_ms =
        elapsed_ms(
            total_start,
            total_end);

    result.metrics.model_load_ms =
        impl_->model_load_ms;

    if (result.metrics.generation_ms > 0.0) {
        result.metrics.generation_tokens_per_second =
            (static_cast<double>(generated) /
             result.metrics.generation_ms) *
            1000.0;
    }

    (void)total_start;
    (void)total_end;

    return result;
}

std::vector<InferenceResult>
InferenceEngine::generate_batch(
    const std::vector<std::string>& prompts) {

    if (!loaded()) {
        throw std::runtime_error(
            "OpenMind inference engine is not loaded");
    }

    if (prompts.empty()) {
        throw std::invalid_argument(
            "OpenMind inference batch is empty");
    }

    /*
     * The llama context is shared runtime state. Serialize the batch
     * transaction exactly as the existing stateless/session paths do.
     *
     * This is intentionally the first scheduler-compatible
     * implementation: one caller owns the context, while multiple
     * requests share llama_decode() calls.
     */
    std::lock_guard<std::mutex> lock(
        impl_->inference_mutex);

    llama_memory_t memory =
        llama_get_memory(impl_->ctx);

    /*
     * Batch requests are independent/stateless.
     */
    llama_memory_clear(
        memory,
        true);

    const auto total_start = Clock::now();

    struct BatchRequest {
        std::vector<llama_token> tokens;
        llama_sampler* sampler = nullptr;
        std::string output;
        uint32_t generated = 0;
        bool finished = false;

        /*
         * Index of the most recently produced logits for this request.
         * Initially this points at the final token of the prompt batch.
         * After each generation decode it points into that generation
         * batch and is used for the next sampler step.
         */
        int32_t last_logits_index = -1;
    };

    std::vector<BatchRequest> requests;
    requests.reserve(prompts.size());

    /*
     * Tokenize every request and create an independent sampler.
     */
    for (const auto& prompt : prompts) {
        if (prompt.empty()) {
            throw std::invalid_argument(
                "OpenMind inference batch contains an empty prompt");
        }

        BatchRequest request;

        const int n_prompt =
            -llama_tokenize(
                impl_->vocab,
                prompt.c_str(),
                prompt.size(),
                nullptr,
                0,
                true,
                true);

        if (n_prompt <= 0) {
            throw std::runtime_error(
                "Failed to determine batch prompt token count");
        }

        request.tokens.resize(
            static_cast<size_t>(n_prompt));

        const int tokenized =
            llama_tokenize(
                impl_->vocab,
                prompt.c_str(),
                prompt.size(),
                request.tokens.data(),
                request.tokens.size(),
                true,
                true);

        if (tokenized < 0) {
            throw std::runtime_error(
                "Batch prompt tokenization failed");
        }

        request.sampler =
            llama_sampler_clone(impl_->sampler);

        if (!request.sampler) {
            for (auto& existing : requests) {
                if (existing.sampler) {
                    llama_sampler_free(existing.sampler);
                }
            }

            throw std::runtime_error(
                "OpenMind batch sampler clone failed");
        }

        requests.push_back(std::move(request));
    }

    /*
     * Make sure the complete prompt batch fits in n_batch.
     */
    size_t total_prompt_tokens = 0;

    for (const auto& request : requests) {
        total_prompt_tokens += request.tokens.size();
    }

    const uint32_t batch_capacity =
        llama_n_batch(impl_->ctx);

    if (total_prompt_tokens >
        static_cast<size_t>(batch_capacity)) {

        for (auto& request : requests) {
            if (request.sampler) {
                llama_sampler_free(request.sampler);
            }
        }

        throw std::runtime_error(
            "OpenMind inference batch exceeds n_batch capacity");
    }

    const auto prompt_start = Clock::now();

    /*
     * One llama_batch contains every prompt.
     *
     * Each request gets its own sequence ID. Since this is a
     * stateless batch, sequence IDs are temporary and are cleared
     * with the memory after the transaction.
     */
    llama_batch batch =
        llama_batch_init(
            static_cast<int32_t>(total_prompt_tokens),
            0,
            static_cast<int32_t>(requests.size()));

    size_t batch_index = 0;
    int32_t prompt_logits_index = 0;

    for (size_t request_index = 0;
         request_index < requests.size();
         ++request_index) {

        const auto& tokens =
            requests[request_index].tokens;

        for (size_t token_index = 0;
             token_index < tokens.size();
             ++token_index) {

            batch.token[batch_index] =
                tokens[token_index];

            batch.pos[batch_index] =
                static_cast<llama_pos>(token_index);

            batch.n_seq_id[batch_index] = 1;

            batch.seq_id[batch_index][0] =
                static_cast<llama_seq_id>(request_index);

            batch.logits[batch_index] =
                (token_index + 1 == tokens.size())
                    ? 1
                    : 0;

            if (token_index + 1 == tokens.size()) {
                requests[request_index].last_logits_index =
                    static_cast<int32_t>(batch_index);

            }

            ++batch_index;
        }
    }

    batch.n_tokens =
        static_cast<int32_t>(batch_index);

    if (llama_decode(
            impl_->ctx,
            batch) != 0) {

        llama_batch_free(batch);

        for (auto& request : requests) {
            if (request.sampler) {
                llama_sampler_free(request.sampler);
            }
        }

        throw std::runtime_error(
            "llama_decode(batch prompt) failed");
    }

    llama_batch_free(batch);

    const auto prompt_end = Clock::now();

    /*
     * Autoregressive generation.
     *
     * Every active request contributes one token to the next
     * llama_batch. This is the critical micro-batching behavior:
     * one GPU decode operation services multiple requests.
     */
    const auto generation_start = Clock::now();

    for (uint32_t step = 0;
         step < impl_->config.max_tokens;
         ++step) {

        size_t active_count = 0;

        for (const auto& request : requests) {
            if (!request.finished) {
                ++active_count;
            }
        }

        if (active_count == 0) {
            break;
        }

        llama_batch generation_batch =
            llama_batch_init(
                static_cast<int32_t>(active_count),
                0,
                static_cast<int32_t>(requests.size()));

        size_t output_index = 0;

        for (size_t request_index = 0;
             request_index < requests.size();
             ++request_index) {

            auto& request =
                requests[request_index];

            if (request.finished) {
                continue;
            }

            if (request.last_logits_index < 0) {
                llama_batch_free(generation_batch);

                for (auto& cleanup : requests) {
                    if (cleanup.sampler) {
                        llama_sampler_free(cleanup.sampler);
                        cleanup.sampler = nullptr;
                    }
                }

                throw std::runtime_error(
                    "Batch request has no valid logits index");
            }

            const llama_token token =
                llama_sampler_sample(
                    request.sampler,
                    impl_->ctx,
                    request.last_logits_index);

            if (llama_vocab_is_eog(
                    impl_->vocab,
                    token)) {

                request.finished = true;
                continue;
            }

            char piece[256];

            const int n =
                llama_token_to_piece(
                    impl_->vocab,
                    token,
                    piece,
                    sizeof(piece),
                    0,
                    true);

            if (n < 0) {
                llama_batch_free(generation_batch);

                for (auto& cleanup : requests) {
                    if (cleanup.sampler) {
                        llama_sampler_free(cleanup.sampler);
                    }
                }

                throw std::runtime_error(
                    "Batch token-to-piece conversion failed");
            }

            request.output.append(
                piece,
                static_cast<size_t>(n));

            ++request.generated;

            generation_batch.token[output_index] =
                token;

            generation_batch.pos[output_index] =
                static_cast<llama_pos>(
                    request.tokens.size() +
                    request.generated -
                    1);

            generation_batch.n_seq_id[output_index] = 1;

            generation_batch.seq_id[output_index][0] =
                static_cast<llama_seq_id>(request_index);

            generation_batch.logits[output_index] = 1;

            request.last_logits_index =
                static_cast<int32_t>(output_index);

            ++output_index;
        }

        if (output_index == 0) {
            llama_batch_free(generation_batch);
            break;
        }

        generation_batch.n_tokens =
            static_cast<int32_t>(output_index);

        if (llama_decode(
                impl_->ctx,
                generation_batch) != 0) {

            llama_batch_free(generation_batch);

            for (auto& request : requests) {
                if (request.sampler) {
                    llama_sampler_free(request.sampler);
                }
            }

            throw std::runtime_error(
                "llama_decode(batch generation) failed");
        }

        llama_batch_free(generation_batch);
    }

    const auto generation_end = Clock::now();
    const auto total_end = Clock::now();

    std::vector<InferenceResult> results;
    results.reserve(requests.size());

    const double prompt_ms =
        elapsed_ms(
            prompt_start,
            prompt_end);

    const double generation_ms =
        elapsed_ms(
            generation_start,
            generation_end);

    const double total_ms =
        elapsed_ms(
            total_start,
            total_end);

    for (auto& request : requests) {
        InferenceResult result;

        result.text =
            std::move(request.output);

        result.metrics.model_load_ms =
            impl_->model_load_ms;

        result.metrics.prompt_tokens =
            static_cast<uint32_t>(
                request.tokens.size());

        result.metrics.generated_tokens =
            request.generated;

        result.metrics.prompt_eval_ms =
            prompt_ms;

        result.metrics.generation_ms =
            generation_ms;

        result.metrics.total_ms =
            total_ms;

        if (prompt_ms > 0.0) {
            result.metrics.prompt_tokens_per_second =
                (static_cast<double>(
                    request.tokens.size()) /
                 prompt_ms) *
                1000.0;
        }

        if (generation_ms > 0.0) {
            result.metrics.generation_tokens_per_second =
                (static_cast<double>(
                    request.generated) /
                 generation_ms) *
                1000.0;
        }

        results.push_back(
            std::move(result));

        if (request.sampler) {
            llama_sampler_free(
                request.sampler);

            request.sampler = nullptr;
        }
    }

    return results;
}

InferenceResult InferenceEngine::generate_session(
    const std::string& prompt,
    int32_t seq_id,
    llama_sampler* sampler) {

    if (!loaded()) {
        throw std::runtime_error(
            "OpenMind inference engine is not loaded");
    }

    if (prompt.empty()) {
        throw std::invalid_argument(
            "OpenMind inference prompt is empty");
    }

    if (seq_id < 0) {
        throw std::invalid_argument(
            "OpenMind session sequence ID is invalid");
    }

    /*
     * Sessions have independent sequence IDs, but they still
     * share the underlying llama context and native runtime.
     * Serialize the complete session transaction.
     */
    std::lock_guard<std::mutex> lock(
        impl_->inference_mutex);

    InferenceResult result;

    const auto total_start = Clock::now();

    int n_prompt =
        -llama_tokenize(
            impl_->vocab,
            prompt.c_str(),
            prompt.size(),
            nullptr,
            0,
            true,
            true);

    if (n_prompt <= 0) {
        throw std::runtime_error(
            "Failed to determine prompt token count");
    }

    std::vector<llama_token> tokens(
        static_cast<size_t>(n_prompt));

    const int tokenized =
        llama_tokenize(
            impl_->vocab,
            prompt.c_str(),
            prompt.size(),
            tokens.data(),
            tokens.size(),
            true,
            true);

    if (tokenized < 0) {
        throw std::runtime_error(
            "Prompt tokenization failed");
    }

    result.metrics.prompt_tokens =
        static_cast<uint32_t>(n_prompt);

    llama_memory_t memory =
        llama_get_memory(impl_->ctx);

    llama_pos next_pos =
        llama_memory_seq_pos_max(
            memory,
            seq_id);

    if (next_pos < 0) {
        next_pos = 0;
    } else {
        ++next_pos;
    }

    const uint32_t session_ctx =
        session_context_size();

    if (session_ctx == 0) {
        throw std::runtime_error(
            "OpenMind session context capacity is zero");
    }

    const llama_pos prompt_end =
        next_pos +
        static_cast<llama_pos>(tokens.size());

    if (prompt_end >
        static_cast<llama_pos>(session_ctx)) {
        throw std::runtime_error(
            "OpenMind session context capacity exceeded; "
            "reset the session or increase context_size "
            "or reduce max_sessions");
    }

    /*
     * llama_decode() requires the complete submitted batch to fit
     * within the context's logical n_batch capacity.  llama.cpp
     * asserts this internally, so reject the request here instead
     * of allowing an oversized prompt to abort the process.
     */
    const uint32_t batch_capacity =
        llama_n_batch(impl_->ctx);

    if (tokens.size() >
        static_cast<size_t>(batch_capacity)) {
        throw std::runtime_error(
            "OpenMind session context capacity exceeded; "
            "reduce the prompt size or increase context_size");
    }

    const auto prompt_start = Clock::now();

    llama_batch batch =
        llama_batch_init(
            static_cast<int32_t>(tokens.size()),
            0,
            1);

    for (size_t i = 0; i < tokens.size(); ++i) {
        batch.token[i] = tokens[i];
        batch.pos[i] =
            next_pos +
            static_cast<llama_pos>(i);
        batch.n_seq_id[i] = 1;
        batch.seq_id[i][0] = seq_id;
        batch.logits[i] =
            (i + 1 == tokens.size()) ? 1 : 0;
    }

    batch.n_tokens =
        static_cast<int32_t>(tokens.size());

    if (llama_decode(
            impl_->ctx,
            batch) != 0) {
        llama_batch_free(batch);
        throw std::runtime_error(
            "llama_decode(session prompt) failed");
    }

    llama_batch_free(batch);

    const auto prompt_end_time = Clock::now();

    result.metrics.prompt_eval_ms =
        elapsed_ms(
            prompt_start,
            prompt_end_time);

    if (result.metrics.prompt_eval_ms > 0.0) {
        result.metrics.prompt_tokens_per_second =
            (static_cast<double>(n_prompt) /
             result.metrics.prompt_eval_ms) *
            1000.0;
    }

    const auto generation_start = Clock::now();

    std::string output;
    uint32_t generated = 0;

    llama_pos generation_pos = prompt_end;

    for (uint32_t i = 0;
         i < impl_->config.max_tokens;
         ++i) {

        const llama_token token =
            llama_sampler_sample(
                sampler,
                impl_->ctx,
                -1);

        if (llama_vocab_is_eog(
                impl_->vocab,
                token)) {
            break;
        }

        char piece[256];

        const int n =
            llama_token_to_piece(
                impl_->vocab,
                token,
                piece,
                sizeof(piece),
                0,
                true);

        if (n < 0) {
            throw std::runtime_error(
                "Token-to-piece conversion failed");
        }

        output.append(
            piece,
            static_cast<size_t>(n));

        ++generated;

        if (generation_pos >=
            static_cast<llama_pos>(session_ctx)) {
            break;
        }

        llama_batch next_batch =
            llama_batch_init(1, 0, 1);

        next_batch.n_tokens = 1;
        next_batch.token[0] = token;
        next_batch.pos[0] = generation_pos;
        next_batch.n_seq_id[0] = 1;
        next_batch.seq_id[0][0] = seq_id;
        next_batch.logits[0] = 1;

        if (llama_decode(
                impl_->ctx,
                next_batch) != 0) {
            llama_batch_free(next_batch);
            throw std::runtime_error(
                "llama_decode(session generation) failed");
        }

        llama_batch_free(next_batch);

        ++generation_pos;
    }

    const auto generation_end = Clock::now();
    const auto total_end = Clock::now();

    result.text = std::move(output);
    result.metrics.generated_tokens = generated;

    result.metrics.generation_ms =
        elapsed_ms(
            generation_start,
            generation_end);

    result.metrics.total_ms =
        elapsed_ms(
            total_start,
            total_end);

    result.metrics.model_load_ms =
        impl_->model_load_ms;

    if (result.metrics.generation_ms > 0.0) {
        result.metrics.generation_tokens_per_second =
            (static_cast<double>(generated) /
             result.metrics.generation_ms) *
            1000.0;
    }

    return result;
}

bool InferenceEngine::loaded() const noexcept {
    if (!impl_) {
        return false;
    }

    std::lock_guard<std::mutex> lock(
        impl_->inference_mutex);

    return impl_->loaded;
}

uint32_t InferenceEngine::session_context_size() const noexcept {
    if (!impl_ || !impl_->ctx) {
        return 0;
    }

    return llama_n_ctx_seq(impl_->ctx);
}

int32_t InferenceEngine::allocate_session_seq_id() {
    if (!impl_) {
        throw std::runtime_error(
            "OpenMind inference engine implementation unavailable");
    }

    if (impl_->config.max_sessions == 0) {
        throw std::runtime_error(
            "OpenMind maximum session count is zero");
    }

    std::lock_guard<std::mutex> lock(
        impl_->inference_mutex);

    if (!free_session_seq_ids_.empty()) {
        const int32_t seq_id = free_session_seq_ids_.back();
        free_session_seq_ids_.pop_back();
        return seq_id;
    }

    if (next_session_seq_id_ < 0 ||
        static_cast<uint32_t>(next_session_seq_id_) >=
            impl_->config.max_sessions) {
        throw std::overflow_error(
            "OpenMind session sequence capacity exhausted");
    }

    return next_session_seq_id_++;
}

void InferenceEngine::release_session_seq_id(
    int32_t seq_id) noexcept {

    if (seq_id < 0) {
        return;
    }

    if (!impl_ ||
        static_cast<uint32_t>(seq_id) >=
            impl_->config.max_sessions) {
        return;
    }

    std::lock_guard<std::mutex> lock(
        impl_->inference_mutex);

    llama_memory_seq_rm(
        llama_get_memory(impl_->ctx),
        seq_id,
        0,
        -1);

    free_session_seq_ids_.push_back(seq_id);
}

} // namespace openmind

namespace openmind {

struct Session::Impl {
    llama_sampler* sampler = nullptr;

    ~Impl() {
        if (sampler) {
            llama_sampler_free(sampler);
        }
    }
};

Session::Session(InferenceEngine& engine)
    : engine_(&engine),
      impl_(std::make_unique<Impl>()) {

    if (!engine.loaded()) {
        engine_ = nullptr;
        impl_.reset();
        throw std::runtime_error(
            "OpenMind session requires a loaded inference engine");
    }

    seq_id_ = engine.allocate_session_seq_id();

    {
        std::lock_guard<std::mutex> lock(
            engine.impl_->inference_mutex);

        impl_->sampler =
            llama_sampler_clone(engine.impl_->sampler);
    }

    if (!impl_->sampler) {
        engine.release_session_seq_id(seq_id_);
        seq_id_ = -1;
        engine_ = nullptr;
        impl_.reset();

        throw std::runtime_error(
            "OpenMind session sampler clone failed");
    }
}

Session::~Session() {
    if (engine_ && engine_->impl_) {
        std::lock_guard<std::mutex> lock(
            engine_->impl_->inference_mutex);

        if (seq_id_ >= 0 &&
            static_cast<uint32_t>(seq_id_) <
                engine_->impl_->config.max_sessions) {
            llama_memory_seq_rm(
                llama_get_memory(engine_->impl_->ctx),
                seq_id_,
                0,
                -1);

            engine_->free_session_seq_ids_.push_back(seq_id_);
        }

        /*
         * The session sampler may be in use by request().
         * Keep the engine mutex held until it has been freed.
         */
        impl_.reset();
    } else {
        impl_.reset();
    }

    engine_ = nullptr;
    seq_id_ = -1;
}

InferenceResult Session::request(const std::string& prompt) {
    if (!engine_) {
        throw std::runtime_error(
            "OpenMind session has no inference engine");
    }

    if (!impl_ || !impl_->sampler) {
        throw std::runtime_error(
            "OpenMind session has no sampler");
    }

    return engine_->generate_session(
        prompt,
        seq_id_,
        impl_->sampler);
}

void Session::reset() noexcept {
    if (!engine_ || !engine_->impl_) {
        return;
    }

    std::lock_guard<std::mutex> lock(
        engine_->impl_->inference_mutex);

    llama_memory_seq_rm(
        llama_get_memory(engine_->impl_->ctx),
        seq_id_,
        0,
        -1);

    if (impl_ && impl_->sampler) {
        llama_sampler_reset(impl_->sampler);
    }
}

} // namespace openmind
