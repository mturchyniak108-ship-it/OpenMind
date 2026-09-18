#include "openmind/inference.h"

#include <chrono>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <string>

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <model.gguf>\n";
        return 2;
    }

    openmind::InferenceConfig config;
    config.model_path = argv[1];
    config.context_size = 2048;
    config.gpu_layers = 99;
    config.max_tokens = 128;
    config.max_sessions = 8;
    config.kv_unified = true;

    openmind::InferenceEngine engine(config);

    const auto load_start = std::chrono::steady_clock::now();

    if (!engine.load()) {
        std::cerr << "ERROR: model load failed\n";
        return 1;
    }

    const auto load_end = std::chrono::steady_clock::now();

    const double load_ms =
        std::chrono::duration<double, std::milli>(
            load_end - load_start).count();

    const std::string prompt =
        "Explain what OpenMind is and why native local inference is useful.";

    std::cout << "===== OPENMIND PERFORMANCE BENCHMARK =====\n";
    std::cout << "Model: " << config.model_path << "\n";
    std::cout << "Context: " << config.context_size << "\n";
    std::cout << "Max tokens: " << config.max_tokens << "\n";
    std::cout << "Model load: " << std::fixed << std::setprecision(2)
              << load_ms << " ms\n\n";

    const auto stateless_start = std::chrono::steady_clock::now();
    const auto stateless = engine.generate(prompt);
    const auto stateless_end = std::chrono::steady_clock::now();

    const double stateless_wall_ms =
        std::chrono::duration<double, std::milli>(
            stateless_end - stateless_start).count();

    std::cout << "--- STATELESS generate() ---\n";
    std::cout << "Generated tokens: "
              << stateless.metrics.generated_tokens << "\n";
    std::cout << "Generation speed: "
              << stateless.metrics.generation_tokens_per_second
              << " tok/s\n";
    std::cout << "Wall time: " << stateless_wall_ms << " ms\n\n";

    openmind::Session session(engine);

    const auto session_start = std::chrono::steady_clock::now();
    const auto session_result = session.request(prompt);
    const auto session_end = std::chrono::steady_clock::now();

    const double session_wall_ms =
        std::chrono::duration<double, std::milli>(
            session_end - session_start).count();

    std::cout << "--- SESSION request() ---\n";
    std::cout << "Generated tokens: "
              << session_result.metrics.generated_tokens << "\n";
    std::cout << "Generation speed: "
              << session_result.metrics.generation_tokens_per_second
              << " tok/s\n";
    std::cout << "Wall time: " << session_wall_ms << " ms\n\n";

    session.reset();

    const auto reset_start = std::chrono::steady_clock::now();
    const auto reset_result = session.request(prompt);
    const auto reset_end = std::chrono::steady_clock::now();

    const double reset_wall_ms =
        std::chrono::duration<double, std::milli>(
            reset_end - reset_start).count();

    std::cout << "--- SESSION after reset() ---\n";
    std::cout << "Generated tokens: "
              << reset_result.metrics.generated_tokens << "\n";
    std::cout << "Generation speed: "
              << reset_result.metrics.generation_tokens_per_second
              << " tok/s\n";
    std::cout << "Wall time: " << reset_wall_ms << " ms\n\n";

    std::cout << "===== SUMMARY =====\n";
    std::cout << "Load: " << load_ms << " ms\n";
    std::cout << "Stateless: "
              << stateless.metrics.generation_tokens_per_second
              << " tok/s\n";
    std::cout << "Session: "
              << session_result.metrics.generation_tokens_per_second
              << " tok/s\n";
    std::cout << "Session reset: "
              << reset_result.metrics.generation_tokens_per_second
              << " tok/s\n";
    std::cout << "===== END =====\n";

    return 0;
}
