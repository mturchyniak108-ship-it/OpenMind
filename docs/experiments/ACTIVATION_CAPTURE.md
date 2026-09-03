# All-Token Activation Capture

## Purpose

OpenMind's native activation probe can export the input representation for every prompt token at every repeating transformer layer exposed by the instrumented `llama.cpp` runtime.

This dataset is used by downstream representation-recurrence and MAF experiments.

## Canonical V1 Capture

The canonical capture uses:

- Model: `qwen2.5-coder-q8_0.gguf`
- Model SHA-256: `507de59046601282ba768a9789900e6ccf60ed93ddf346730b7c68eb0715bc47`
- Prompt: `The purpose of this experiment is to measure representation recurrence across transformer layers.`
- GPU layers requested: 99
- Context: 512
- Batch: 512
- Captured transformer layers: 28 (`0..27`)
- Prompt tokens: 14 (`0..13`)
- Embedding dimension: 1536

The CSV schema is:

`layer,token_index,embedding_dimension,v0,...,v1535`

The canonical dataset contains:

- 392 activation records
- 602,112 floating-point activation values
- zero missing layer/token pairs
- zero duplicate/schema errors
- SHA-256: `863d6770a5fd824c5a4deb1b7653b42402d1352d37151c36e55388848c8f1432`

The large CSV is intentionally excluded from Git. Its immutable metadata is tracked in:

`experiments/data/manifests/activation_vectors_all_tokens_v1.json`

## Deterministic Reproduction

A pre-manifest capture created on August 25, 2026 was preserved before the canonical reproduction run.

The canonical reproduction on August 26, 2026 used the explicitly identified model and prompt.

Both files produced the same SHA-256:

`863d6770a5fd824c5a4deb1b7653b42402d1352d37151c36e55388848c8f1432`

A byte comparison also passed.

This demonstrates byte-for-byte reproducibility of this activation export under the tested runtime configuration.

## Reproduction

Build:

`cmake --build native/build --target openmind_activation_probe -j2`

Capture:

`native/build/openmind_activation_probe ~/qwen2.5-coder-q8_0.gguf "The purpose of this experiment is to measure representation recurrence across transformer layers."`

Verify:

`sha256sum activation_vectors_all_tokens.csv`

Expected V1 SHA-256:

`863d6770a5fd824c5a4deb1b7653b42402d1352d37151c36e55388848c8f1432`

## Compatibility

The all-token export is additive.

`activation_vectors.csv` remains the existing final-token compatibility export. Downstream consumers depending on the original format do not need to change.

## Reliability

The all-token writer validates stream state after flushing and closing. A write or close failure causes the probe to return an error rather than silently treating a partial dataset as valid.

## Research Boundary

The activation capture is measurement infrastructure.

Observed recurrence or other downstream structure must be established independently using controls, null models, holdouts, statistical tests, and reproducible analysis. The existence of a deterministic capture does not by itself establish any claim about model architecture or representation recurrence.
