# benchmarks/native-inference-qwen25-3b-vulkan.txt

## Purpose

Records native OpenMind inference performance using Qwen 2.5 3B with Vulkan acceleration.

## Remember

Native inference performance evidence.

## Measures

- Prompt processing speed.
- Generation speed.
- Model/runtime configuration.
- Vulkan execution behavior.

## Architecture

Qwen 2.5 3B -> llama.cpp -> Vulkan -> OpenMind native C++ -> measured inference performance.

## Usage

Use this record when comparing native inference changes, backend changes, model configuration changes, or performance regressions.

## Agent Rule

Do not compare benchmark numbers without checking device, model, quantization, context, GPU layers, backend, and build conditions.

## Future

The same measurement discipline will eventually be applied to Truth Graph traversal, vector retrieval, weighted path discovery, and compiled heuristic mappings.
