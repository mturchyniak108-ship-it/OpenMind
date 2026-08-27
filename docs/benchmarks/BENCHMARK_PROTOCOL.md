# OpenMind Benchmark Protocol

Every architectural change must be evaluated against the appropriate baseline.

## Quality

- correctness
- semantic correctness
- Canonical Truth Graph consistency
- contradiction rate
- provenance correctness
- repeated-prompt consistency

## Efficiency

- prompt tokens
- generated tokens
- total tokens
- peak RAM
- persistent model size
- working memory
- latency
- throughput

## Device

Measure CPU, NEON, Vulkan, CPU/GPU split, peak memory, thermal behavior, and sustained throughput where applicable.

## Comparison levels

1. Original GGUF/LLM baseline
2. MAF representation
3. Fractal MAF
4. MAF + fuzzy routing
5. MAF + ML routing
6. MAF-primary inference
7. Native optimized C++ implementation

## Scientific rule

An optimization is accepted only when its measured benefit is reproducible. A reduction in one resource is not an overall improvement if correctness regresses unacceptably.
