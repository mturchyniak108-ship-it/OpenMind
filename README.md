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

## License

To be defined before public release.
