# benchmarks/baseline-qwen25-3b-vulkan.txt

## Purpose

Records the verified baseline performance of OpenMind native local inference using Qwen 2.5 3B with the Vulkan backend.

## Architectural Role

This file establishes a reference point for measuring future native inference changes.

It should be treated as a historical performance record rather than generated application state.

## Baseline Environment

The current documented baseline uses:

- Samsung Galaxy S26 Ultra
- Adreno 840 GPU
- Mesa Turnip Vulkan driver
- Qwen 2.5 3B Q4_K_M GGUF
- Context size 512
- Vulkan GPU acceleration

## Recorded Metrics

The repository README identifies the baseline as approximately:

- Prompt processing: 21.95 tokens/second
- Generation: 17.34 tokens/second

The benchmark record itself is authoritative for the exact captured run details.

## Agent Usage

Use this benchmark when evaluating changes to:

- llama.cpp configuration
- Vulkan configuration
- native inference integration
- model loading
- context configuration
- GPU layer configuration

## Comparison Rules

Only compare results when the model, quantization, device, backend, context, and relevant runtime conditions are sufficiently equivalent.

A faster result obtained under materially different conditions is not automatically a regression improvement.

## Relationship To Future Work

This baseline measures inference execution only.

Future OpenMind benchmarks will extend the same reproducibility principle to semantic retrieval, Truth Graph traversal, vector indexing, path ranking, and compiled heuristic mappings.

## Agent Guidance

Never overwrite an established baseline simply because a newer run produces different numbers.

Create a new benchmark record when the architecture or test conditions change significantly.
