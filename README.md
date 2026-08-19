# OpenMind

OpenMind is a local-first AI inference platform designed around native
llama.cpp execution and hardware-accelerated inference.

## Current Status

Native llama.cpp inference is operational on the Samsung Galaxy S26 Ultra
using the Adreno 840 GPU through the Vulkan backend and Mesa Turnip driver.

### Verified Baseline

- Device: Samsung Galaxy S26 Ultra
- GPU: Adreno 840
- Vulkan driver: Mesa Turnip
- Model: Qwen 2.5 3B Q4_K_M
- Context: 512
- GPU layers: 99
- Prompt speed: 21.95 tok/s
- Generation speed: 17.34 tok/s
- Native Vulkan inference: PASS

See:

`benchmarks/baseline-qwen25-3b-vulkan.txt`

## Architecture

OpenMind is being developed as a native inference/control platform rather
than simply a wrapper around an existing AI application.

Current components:

- `native/` — native C++ inference integration
- `benchmarks/` — reproducible performance baselines
- `preflight/` — system and resource discovery
- `vulkan/` — Vulkan/GPU capability probing
- `models/` — local model location (ignored by Git)
- `llama.cpp/` — llama.cpp inference engine

## Current Milestone

**Milestone 0 — Native inference foundation**

1. Device/resource discovery
2. Vulkan capability verification
3. llama.cpp Vulkan build
4. Native C++ inference
5. Baseline performance measurement
6. Reproducible project structure
7. Native persistent session API
8. Multi-session sequence isolation and RAII lifecycle
9. CMake/CTest integration testing

## Native Inference API

The native inference layer currently provides:

- `InferenceEngine` for model and runtime ownership
- Stateless `InferenceEngine::generate()` requests
- Persistent `Session` handles for conversational KV-cache state
- Independent llama sequence IDs for multiple concurrent sessions
- Configurable maximum session capacity
- Configuration validation for required runtime limits
- Session reset and RAII sequence-slot release
- Inference timing and token-throughput metrics
- Vulkan-backed llama.cpp execution

The native integration test verifies model loading, stateless requests,
session persistence, session isolation, reset behavior, session capacity,
sequence-slot reuse, and destructor-based lifecycle cleanup.

CTest is configured through `OPENMIND_TEST_MODEL` and has been verified
against the Qwen 2.5 3B Q4_K_M GGUF model on the S26 Ultra Vulkan runtime.

## License

To be defined before public release.
