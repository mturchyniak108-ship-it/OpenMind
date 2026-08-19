#include "openmind/inference.h"

#include <cstdlib>
#include <iostream>
#include <string>

int main(int argc, char ** argv) {
    if (argc < 2) {
        std::cerr
            << "Usage: " << argv[0]
            << " <model.gguf> [prompt]\n";
        return 2;
    }

    openmind::InferenceConfig config;
    config.model_path = argv[1];
    config.context_size = 512;
    config.gpu_layers = 99;
    config.max_tokens = 128;

    if (argc >= 3) {
        // Prompt supplied as one argument.
        // Shell quoting can be used for spaces.
    }

    const std::string prompt =
        argc >= 3
            ? argv[2]
            : "Explain in one short sentence what OpenMind is.";

    std::cout << "=== OPENMIND NATIVE INFERENCE TEST ===\n";
    std::cout << "Model: " << config.model_path << "\n";
    std::cout << "Context: " << config.context_size << "\n";
    std::cout << "GPU layers: " << config.gpu_layers << "\n";
    std::cout << "Max tokens: " << config.max_tokens << "\n";
    std::cout << "\nLoading model...\n";

    openmind::InferenceEngine engine(config);

    if (!engine.load()) {
        std::cerr << "ERROR: failed to load model\n";
        return 1;
    }

    std::cout << "Model loaded successfully.\n";
    std::cout << "\nPrompt: " << prompt << "\n";
    std::cout << "\nGenerating...\n\n";

    try {
        const auto result = engine.generate(prompt);

        std::cout << "=== RESPONSE ===\n";
        std::cout << result.text << "\n";

        std::cout << "\n=== METRICS ===\n";
        std::cout
            << "Prompt tokens: "
            << result.metrics.prompt_tokens
            << "\n";

        std::cout
            << "Generated tokens: "
            << result.metrics.generated_tokens
            << "\n";

        std::cout
            << "Model load: "
            << result.metrics.model_load_ms
            << " ms\n";

        std::cout
            << "Prompt eval: "
            << result.metrics.prompt_eval_ms
            << " ms\n";

        std::cout
            << "Prompt speed: "
            << result.metrics.prompt_tokens_per_second
            << " tok/s\n";

        std::cout
            << "Generation: "
            << result.metrics.generation_ms
            << " ms\n";

        std::cout
            << "Total: "
            << result.metrics.total_ms
            << " ms\n";

        std::cout
            << "Generation speed: "
            << result.metrics.generation_tokens_per_second
            << " tok/s\n";

    } catch (const std::exception & e) {
        std::cerr
            << "ERROR during inference: "
            << e.what() << "\n";
        return 1;
    }

    return 0;
}
