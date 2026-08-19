#include "openmind/inference.h"

#include "ggml-backend.h"
#include "llama.h"

#include <chrono>
#include <cstring>
#include <memory>
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
};

InferenceEngine::InferenceEngine(const InferenceConfig& config)
    : impl_(std::make_unique<Impl>(config)) {}

InferenceEngine::~InferenceEngine() = default;

bool InferenceEngine::load() {
    if (!impl_ || impl_->config.model_path.empty()) {
        return false;
    }

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
     * Keep the batch large enough for the configured context.
     * The actual prompt batch is still limited by the prompt size.
     */
    ctx_params.n_batch =
        impl_->config.context_size;

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

    const llama_pos prompt_end =
        next_pos +
        static_cast<llama_pos>(tokens.size());

    if (prompt_end >
        static_cast<llama_pos>(impl_->config.context_size)) {
        throw std::runtime_error(
            "OpenMind session context capacity exceeded; "
            "reset the session or increase context_size");
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
            static_cast<llama_pos>(
                impl_->config.context_size)) {
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
    return impl_ && impl_->loaded;
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

    impl_->sampler =
        llama_sampler_clone(engine.impl_->sampler);

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
    if (engine_) {
        engine_->release_session_seq_id(seq_id_);
    }

    impl_.reset();
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
