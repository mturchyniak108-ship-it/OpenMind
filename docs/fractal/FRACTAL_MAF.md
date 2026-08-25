# Fractal MAF Architecture

## Objective

Investigate whether the Memory/Activation Field (MAF) can represent useful model behavior through recursively structured, multi-dimensional activation relationships while reducing token, memory, and compute requirements.

## Three-map architecture

The primary maps are:

1. Truth Canon
2. Relationship Map
3. Landscape Map

The Truth Canon defines canonical knowledge and provenance.
The Relationship Map defines connections between nodes.
The Landscape Map represents dynamic structural properties including activation density, heatwave relationships, heightmaps, confidence, recurrence, and learned routing signals.

Fractal structures may reference all three maps.

## Fractal MAF

A fractal MAF treats activation structures as recursively composable cells.

A cell may represent an activation, node, relationship, local MAF, higher-level MAF, or recursively aggregated region.

The structure is not restricted to two dimensions. Dimensions may represent semantic position, activation magnitude, confidence, provenance, temporal state, layer depth, relationship strength, recurrence, locality, and scale.

## Sparse activation

The working hypothesis is that MAF can become a sparse model substrate rather than merely a post-processing representation.

```text
input
  -> anchor selection
  -> relationship traversal
  -> fractal expansion
  -> local activation
  -> fuzzy/ML routing
  -> pruning
  -> retained state
  -> decoder
```

## Pruning

Pruning must preserve termination information. A rejected path may become useful future training information and should not be silently destroyed.

## Validation

Compare against the baseline LLM for correctness, token usage, memory usage, latency, throughput, model size, energy where measurable, reasoning consistency, retrieval accuracy, and repeated-prompt consistency.

## Native implementation

Python is permitted for exploration. Validated components should progressively move into C++ and receive ARM64, NEON, and Vulkan optimization where beneficial.
