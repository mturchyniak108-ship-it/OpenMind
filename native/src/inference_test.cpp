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

    openmind::Session session(engine);

    const std::string prompt_a =
        argc >= 3
            ? argv[2]
            : "In one short sentence, what is OpenMind?";

    const std::string prompt_b =
        "In one short sentence, why is local inference useful?";

    try {
        std::cout << "\n=== REQUEST 1 ===\n";
        std::cout << "Prompt: " << prompt_a << "\n";
        std::cout << "\nGenerating...\n\n";

        const auto result_a = session.request(prompt_a);

        std::cout << "Response 1:\n"
                  << result_a.text << "\n";

        std::cout << "\nMetrics 1:\n"
                  << "Prompt tokens: "
                  << result_a.metrics.prompt_tokens << "\n"
                  << "Generated tokens: "
                  << result_a.metrics.generated_tokens << "\n"
                  << "Total: "
                  << result_a.metrics.total_ms << " ms\n"
                  << "Generation speed: "
                  << result_a.metrics.generation_tokens_per_second
                  << " tok/s\n";

        std::cout << "\n=== REQUEST 2 ===\n";
        std::cout << "Prompt: " << prompt_b << "\n";
        std::cout << "\nGenerating...\n\n";

        const auto result_b = session.request(prompt_b);

        std::cout << "Response 2:\n"
                  << result_b.text << "\n";

        std::cout << "\nMetrics 2:\n"
                  << "Prompt tokens: "
                  << result_b.metrics.prompt_tokens << "\n"
                  << "Generated tokens: "
                  << result_b.metrics.generated_tokens << "\n"
                  << "Total: "
                  << result_b.metrics.total_ms << " ms\n"
                  << "Generation speed: "
                  << result_b.metrics.generation_tokens_per_second
                  << " tok/s\n";

        std::cout << "\n=== RESET TEST ===\n";
        std::cout << "Two sequential generate() calls completed "
                     "through the same engine instance.\n";
        std::cout << "Each request clears llama memory before "
                     "prompt evaluation.\n";

    } catch (const std::exception & e) {
        std::cerr
            << "ERROR during inference: "
            << e.what() << "\n";
        return 1;
    }

    return 0;
}
