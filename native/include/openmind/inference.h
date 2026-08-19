#pragma once

#include <cstdint>
#include <memory>
#include <string>

namespace openmind {

struct InferenceConfig {
    std::string model_path;
    uint32_t context_size = 512;
    uint32_t gpu_layers = 99;
    uint32_t max_tokens = 32;
};

struct InferenceMetrics {
    double model_load_ms = 0.0;
    double prompt_eval_ms = 0.0;
    double generation_ms = 0.0;
    double total_ms = 0.0;

    double prompt_tokens_per_second = 0.0;
    double generation_tokens_per_second = 0.0;

    uint32_t prompt_tokens = 0;
    uint32_t generated_tokens = 0;
};

struct InferenceResult {
    std::string text;
    InferenceMetrics metrics;
};

class InferenceEngine {
public:
    explicit InferenceEngine(const InferenceConfig& config);
    ~InferenceEngine();

    InferenceEngine(const InferenceEngine&) = delete;
    InferenceEngine& operator=(const InferenceEngine&) = delete;

    bool load();
    InferenceResult generate(const std::string& prompt);

    bool loaded() const noexcept;

private:
    friend class Session;

    InferenceResult generate_session(
        const std::string& prompt,
        int32_t seq_id);

    struct Impl;
    std::unique_ptr<Impl> impl_;
};

class Session {
public:
    explicit Session(InferenceEngine& engine);

    InferenceResult request(const std::string& prompt);

    void reset() noexcept;

private:
    InferenceEngine* engine_;
    int32_t seq_id_ = 0;
};

} // namespace openmind
