#include "llama.h"
#include "ggml-backend.h"

#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>

using Clock = std::chrono::steady_clock;

static double elapsed_ms(Clock::time_point start, Clock::time_point end) {
    return std::chrono::duration<double, std::milli>(end - start).count();
}

int main(int argc, char ** argv) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s MODEL.gguf \"prompt\"\n", argv[0]);
        return 1;
    }

    const char * model_path = argv[1];
    const char * prompt = argv[2];

    printf("OpenMind native llama.cpp benchmark\n");
    printf("Model: %s\n", model_path);
    printf("Prompt: %s\n\n", prompt);

    const auto total_start = Clock::now();

    ggml_backend_load_all();
    llama_backend_init();

    llama_model_params model_params =
        llama_model_default_params();

    model_params.n_gpu_layers = 99;

    const auto load_start = Clock::now();

    llama_model * model =
        llama_model_load_from_file(model_path, model_params);

    const auto load_end = Clock::now();

    if (!model) {
        fprintf(stderr, "ERROR: failed to load model\n");
        llama_backend_free();
        return 2;
    }

    const llama_vocab * vocab =
        llama_model_get_vocab(model);

    int n_prompt =
        -llama_tokenize(
            vocab,
            prompt,
            std::strlen(prompt),
            nullptr,
            0,
            true,
            true
        );

    if (n_prompt <= 0) {
        fprintf(stderr, "ERROR: failed to determine token count\n");
        llama_model_free(model);
        llama_backend_free();
        return 3;
    }

    std::vector<llama_token> tokens(n_prompt);

    if (llama_tokenize(
            vocab,
            prompt,
            std::strlen(prompt),
            tokens.data(),
            tokens.size(),
            true,
            true) < 0) {

        fprintf(stderr, "ERROR: tokenization failed\n");
        llama_model_free(model);
        llama_backend_free();
        return 4;
    }

    printf("Prompt tokens: %d\n", n_prompt);

    llama_context_params ctx_params =
        llama_context_default_params();

    ctx_params.n_ctx = 512;
    ctx_params.n_batch = n_prompt;

    llama_context * ctx =
        llama_init_from_model(model, ctx_params);

    if (!ctx) {
        fprintf(stderr, "ERROR: failed to create context\n");
        llama_model_free(model);
        llama_backend_free();
        return 5;
    }

    llama_sampler_chain_params sampler_params =
        llama_sampler_chain_default_params();

    llama_sampler * sampler =
        llama_sampler_chain_init(sampler_params);

    llama_sampler_chain_add(
        sampler,
        llama_sampler_init_greedy()
    );

    const auto prompt_start = Clock::now();

    llama_batch batch =
        llama_batch_get_one(tokens.data(), tokens.size());

    if (llama_decode(ctx, batch) != 0) {
        fprintf(stderr, "ERROR: llama_decode(prompt) failed\n");

        llama_sampler_free(sampler);
        llama_free(ctx);
        llama_model_free(model);
        llama_backend_free();

        return 6;
    }

    const auto prompt_end = Clock::now();

    printf("\nResponse:\n");

    constexpr int max_tokens = 32;

    int generated_tokens = 0;
    const auto generation_start = Clock::now();

    for (int i = 0; i < max_tokens; ++i) {
        llama_token token =
            llama_sampler_sample(sampler, ctx, -1);

        if (llama_vocab_is_eog(vocab, token)) {
            break;
        }

        char piece[256];

        int n =
            llama_token_to_piece(
                vocab,
                token,
                piece,
                sizeof(piece),
                0,
                true
            );

        if (n < 0) {
            fprintf(stderr, "\nERROR: token-to-piece failed\n");
            break;
        }

        fwrite(piece, 1, n, stdout);
        fflush(stdout);

        ++generated_tokens;

        batch = llama_batch_get_one(&token, 1);

        if (llama_decode(ctx, batch) != 0) {
            fprintf(stderr, "\nERROR: llama_decode(generation) failed\n");
            break;
        }
    }

    const auto generation_end = Clock::now();
    const auto total_end = Clock::now();

    const double load_ms =
        elapsed_ms(load_start, load_end);

    const double prompt_ms =
        elapsed_ms(prompt_start, prompt_end);

    const double generation_ms =
        elapsed_ms(generation_start, generation_end);

    const double total_ms =
        elapsed_ms(total_start, total_end);

    const double prompt_tps =
        prompt_ms > 0.0
            ? (static_cast<double>(n_prompt) / prompt_ms) * 1000.0
            : 0.0;

    const double generation_tps =
        generation_ms > 0.0
            ? (static_cast<double>(generated_tokens) / generation_ms) * 1000.0
            : 0.0;

    printf("\n\n=== OpenMind Benchmark ===\n");
    printf("Model load:       %.2f ms\n", load_ms);
    printf("Prompt tokens:    %d\n", n_prompt);
    printf("Prompt eval:      %.2f ms\n", prompt_ms);
    printf("Prompt speed:     %.2f tok/s\n", prompt_tps);
    printf("Generated tokens: %d\n", generated_tokens);
    printf("Generation:       %.2f ms\n", generation_ms);
    printf("Generation speed: %.2f tok/s\n", generation_tps);
    printf("Total runtime:    %.2f ms\n", total_ms);

    printf("\nNative inference benchmark complete.\n");

    llama_sampler_free(sampler);
    llama_free(ctx);
    llama_model_free(model);
    llama_backend_free();

    return 0;
}
