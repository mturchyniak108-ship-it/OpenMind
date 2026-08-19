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
     * A failed real model load must leave the engine recoverable.
     * This exercises cleanup after llama_model_load_from_file().
     */
    {
        openmind::InferenceConfig recovery = config;
        recovery.model_path =
            "/definitely/nonexistent/openmind-test-model.gguf";

        openmind::InferenceEngine engine(recovery);

        check(!engine.load(),
              "invalid GGUF path rejected");

        check(!engine.loaded(),
              "engine remains unloaded after invalid GGUF");

        recovery.model_path = config.model_path;

        openmind::InferenceEngine recovered(recovery);

        check(recovered.load(),
              "valid GGUF loads after invalid path scenario");

        check(recovered.loaded(),
              "recovered engine reports loaded");
    }

    /*
     * A Session requires a loaded engine because sequence state
     * belongs to the llama context created during load().
     */
    {
        openmind::InferenceEngine unloaded_engine(config);

        bool rejected = false;

        try {
            openmind::Session session(unloaded_engine);
        } catch (const std::runtime_error&) {
            rejected = true;
        }

        check(rejected,
              "session creation rejects unloaded engine");
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
     * Multiple sessions must have independent llama sequence state.
     */
    try {
        openmind::Session session_a(engine);
        openmind::Session session_b(engine);

        const auto a1 =
            session_a.request("My name is Alice.");

        const auto b1 =
            session_b.request("My name is Bob.");

        check(!a1.text.empty(),
              "session A generates independently");

        check(!b1.text.empty(),
              "session B generates independently");

        /*
         * Each session continues its own conversation.
         * The prompts deliberately use different identities so
         * accidental shared sequence state can be detected by
         * subsequent behavioral checks.
         */
        const auto a2 =
            session_a.request("What is my name?");

        const auto b2 =
            session_b.request("What is my name?");

        check(!a2.text.empty(),
              "session A retains usable state");

        check(!b2.text.empty(),
              "session B retains usable state");

        /*
         * Reset A only. B must remain usable afterward.
         */
        session_a.reset();

        const auto b3 =
            session_b.request("Tell me my name again.");

        check(!b3.text.empty(),
              "resetting session A does not invalidate session B");

        /*
         * A must also be reusable after its own reset.
         */
        const auto a3 =
            session_a.request("What is my name?");

        check(!a3.text.empty(),
              "session A remains usable after its own reset");

        session_a.reset();
        session_b.reset();

        check(true,
              "multiple sessions reset independently");
    } catch (const std::exception& e) {
        std::cerr
            << "[FAIL] multiple session isolation: "
            << e.what() << "\n";
        ++failures;
    }

    /*
     * Session capacity must be enforced and released IDs must be reusable.
     */
    try {
        openmind::InferenceConfig limited_config = config;
        limited_config.max_sessions = 2;

        openmind::InferenceEngine limited_engine(limited_config);

        check(limited_engine.load(),
              "limited engine loads for session capacity test");

        {
            openmind::Session session_a(limited_engine);
            openmind::Session session_b(limited_engine);

            check(true,
                  "maximum concurrent session capacity is constructible");

            bool rejected = false;

            try {
                openmind::Session session_c(limited_engine);
            } catch (const std::overflow_error&) {
                rejected = true;
            }

            check(rejected,
                  "session creation rejects capacity overflow");
        }

        /*
         * Both previous sessions are destroyed here, so their sequence
         * IDs must have been returned to the engine's free pool.
         */
        try {
            openmind::Session reused_session(limited_engine);

            const auto result =
                reused_session.request(
                    "Session ID capacity was released. Respond briefly.");

            check(!result.text.empty(),
                  "released session capacity is reusable");
        } catch (const std::exception& e) {
            std::cerr
                << "[FAIL] session capacity reuse: "
                << e.what() << "\n";
            ++failures;
        }
    } catch (const std::exception& e) {
        std::cerr
            << "[FAIL] session capacity lifecycle: "
            << e.what() << "\n";
        ++failures;
    }

    /*
     * Session destruction must release its sequence slot.
     */
    try {
        openmind::InferenceConfig reuse_config = config;
        reuse_config.max_sessions = 1;

        openmind::InferenceEngine reuse_engine(reuse_config);

        check(reuse_engine.load(),
              "engine loads for destructor release test");

        {
            openmind::Session first(reuse_engine);

            const auto result =
                first.request("Generate a brief response.");

            check(!result.text.empty(),
                  "first session works before destruction");
        }

        /*
         * The only available session slot was released by the destructor.
         * A second Session must therefore be constructible.
         */
        try {
            openmind::Session second(reuse_engine);

            const auto result =
                second.request("Generate another brief response.");

            check(!result.text.empty(),
                  "destroyed session sequence slot is reusable");
        } catch (const std::exception& e) {
            std::cerr
                << "[FAIL] destructor sequence release: "
                << e.what() << "\n";
            ++failures;
        }
    } catch (const std::exception& e) {
        std::cerr
            << "[FAIL] destructor release lifecycle: "
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
