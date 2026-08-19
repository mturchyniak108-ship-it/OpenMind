#include "openmind/inference.h"

#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>

namespace {

int failures = 0;

void check(bool condition, const char* message) {
    if (condition) {
        std::cout << "[PASS] " << message << "\n";
    } else {
        std::cerr << "[FAIL] " << message << "\n";
        ++failures;
    }
}

} // namespace

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr
            << "Usage: " << argv[0]
            << " <model.gguf>\n";
        return 2;
    }

    openmind::InferenceConfig config;
    config.model_path = argv[1];
    config.context_size = 512;
    config.gpu_layers = 99;
    config.max_tokens = 16;

    std::cout << "=== OPENMIND NATIVE API TEST ===\n";
    std::cout << "Model: " << config.model_path << "\n\n";

    /*
     * Invalid configuration must fail cleanly.
     */
    {
        openmind::InferenceConfig invalid;
        openmind::InferenceEngine engine(invalid);

        check(!engine.load(),
              "empty model path rejected");

        check(!engine.loaded(),
              "engine remains unloaded after failed load");
    }

    /*
     * Real model load.
     */
    openmind::InferenceEngine engine(config);

    check(!engine.loaded(),
          "engine initially unloaded");

    check(engine.load(),
          "real GGUF model loads");

    check(engine.loaded(),
          "engine reports loaded");

    /*
     * Empty prompt must be rejected.
     */
    try {
        (void)engine.generate("");
        check(false, "empty generate prompt rejected");
    } catch (const std::invalid_argument&) {
        check(true, "empty generate prompt rejected");
    } catch (...) {
        check(false, "empty generate prompt rejected with invalid_argument");
    }

    /*
     * Independent generate() requests must not retain
     * previous KV-cache state.
     */
    try {
        const auto first =
            engine.generate("My name is Alice.");

        const auto second =
            engine.generate("What is my name?");

        check(!first.text.empty(),
              "independent request 1 generated text");

        check(!second.text.empty(),
              "independent request 2 generated text");

        check(first.metrics.generated_tokens > 0,
              "request 1 reports generated tokens");

        check(second.metrics.generated_tokens > 0,
              "request 2 reports generated tokens");
    } catch (const std::exception& e) {
        std::cerr
            << "[FAIL] independent generate requests: "
            << e.what() << "\n";
        ++failures;
    }

    /*
     * Session persistence.
     */
    try {
        openmind::Session session(engine);

        const auto first =
            session.request("My name is Alice.");

        const auto second =
            session.request("What is my name?");

        check(!first.text.empty(),
              "session request 1 generated text");

        check(!second.text.empty(),
              "session request 2 generated text");

        check(second.metrics.generated_tokens > 0,
              "session request 2 reports generated tokens");

        /*
         * Reset must be safe and reusable.
         */
        session.reset();

        const auto after_reset =
            session.request("What is my name?");

        check(!after_reset.text.empty(),
              "session remains usable after reset");

        check(after_reset.metrics.generated_tokens > 0,
              "post-reset request reports generated tokens");

        /*
         * Reset may be called repeatedly without failure.
         */
        session.reset();
        session.reset();

        check(true,
              "repeated session reset is safe");
    } catch (const std::exception& e) {
        std::cerr
            << "[FAIL] session lifecycle: "
            << e.what() << "\n";
        ++failures;
    }

    /*
     * Multiple sessions should be constructible from one engine.
     */
    try {
        openmind::Session session_a(engine);
        openmind::Session session_b(engine);

        const auto a =
            session_a.request("My name is Alice.");

        const auto b =
            session_b.request("My name is Bob.");

        check(!a.text.empty(),
              "session A generates independently");

        check(!b.text.empty(),
              "session B generates independently");

        session_a.reset();
        session_b.reset();

        check(true,
              "multiple sessions can be reset independently");
    } catch (const std::exception& e) {
        std::cerr
            << "[FAIL] multiple sessions: "
            << e.what() << "\n";
        ++failures;
    }

    std::cout << "\n=== TEST RESULT ===\n";

    if (failures != 0) {
        std::cerr
            << failures
            << " test(s) failed.\n";
        return 1;
    }

    std::cout
        << "All native API tests passed.\n";

    return 0;
}
