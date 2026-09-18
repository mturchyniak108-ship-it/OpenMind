# Fractal MAF Architecture

<!-- OPENMIND_MAF_Q4_STATUS_BEGIN -->
## MAF Phase 6D-Q4 status — CLOSED

Phase 6D-Q4 Query Route Cache validation is formally closed on frozen evidence.

- Scientific result: **PASS — 44/44 Q4 checks**.
- Frozen cases: `q001`, `q025`, `q026`, `q033`.
- Frozen runner: `bafed2c9ef6d2cf35d8d5212bbb17497f68a67fff9a67d855ac96243af3ac686`.
- Frozen result: `1be2608271e899d320b4255fccba2e64c1616281110ebb375f803a7f740c43e0` / 9184 bytes.
- Frozen exact-once slot: `af63aa8d3b769ad984b898d805ff45361eb5e079658d47a088514d3ba4145a2d` / 1311 bytes.
- Runner implementation contract: `daa291fcb06c0456e028807308e35ef86486e5176b4fe88d254915718d6943e4`.
- Evidence commit: `b386abde55b1b8f156292eb7500fb739ea8be918`.
- Exact-once history: V1, V1.1, V1.2, and V1.3 are permanently spent and MUST NOT be rerun.
- Durable V1.3 state: `RESERVATION_PREPARED -> RESERVED_DURABLE -> PUBLISHED_DURABLE`; no partial residue.
- Claim scope remains limited to safe generation-bound route-metadata persistence, reuse, and invalidation.
- Not established by Q4: inference execution, answer generation, working-set sufficiency, performance superiority or metrics, output parity, route-expansion optimality, MAF-native compute, or LLM replacement.
- Phase 6E: **READY FOR ENTRY REVIEW — NOT ENTERED**.
- Canonical closure record: `experiments/model_fractal/MAF_QUERY_ROUTE_CACHE_VALIDATION_V1_3_VERDICT.md`.

<!-- OPENMIND_MAF_Q4_STATUS_END -->

## Objective

Investigate whether the Memory/Activation Field (MAF) can represent useful model behavior through recursively structured, multi-dimensional activation relationships while reducing token, memory, and compute requirements.

## Three-map architecture

The primary maps are:

1. Canonical Truth Graph
2. Relationship Map
3. Landscape Map

The Canonical Truth Graph defines canonical knowledge and preserves its evidence and provenance relationships.
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
