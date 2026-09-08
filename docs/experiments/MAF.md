# MAF Research

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

MAF research analyzes model structure at representation and parameter levels.

Current analysis areas include GGUF inspection, dequantization, layer profiling, tensor localization, fingerprints, divergence, component analysis, and validation.

MAF outputs remain research artifacts until independently validated.

Production candidates must be tested against baseline outputs, holdout prompts, numerical stability, runtime performance, and memory usage.

## Current Phase 6B Architecture

Phase 6B moves MAF engineering from isolated object experiments toward a generation-bound model-object storage and lookup architecture.

### Stable logical identity

`model_pk`, `generation_pk`, and canonical `object_pk` values are logical identity. They are not derived from filesystem paths or mutable placement.

### Immutable generation evidence

A generation descriptor records canonical segment and object mappings. Physical validation checks segment identity, length, SHA256, object bounds, object byte-range SHA256, reconstructed descriptor bytes, and reconstructed generation identity.

### Atomic Activation

Atomic Activation validates a candidate generation before atomically publishing the canonical active-generation record. Phase 6B.7 is complete and validated.

### Rollback

Rollback revalidates a retained generation and changes current authority back to it. Rollback does not delete newer generations or invent historical provenance. Phase 6B.8 is complete and validated.

### Resident PK Directory V1

Resident PK Directory V1 builds an immutable process-local snapshot from current active authority and current physical generation evidence.

The minimum V1 key is `(model_pk, "object_pk", object_pk)`.

Each object entry preserves generation identity, manifest identity, segment ID, offset, length, object hash, segment integrity metadata, and the current runtime segment path.

The runtime path is metadata, not logical identity.

Successful resident lookup performs direct mapping access without JSON parsing, manifest scanning, filesystem discovery, or linear descriptor scanning.

The frozen implementation targets average O(1) resident lookup, but no Phase 6B.9 performance claim is accepted until benchmark evidence is frozen.

### Current validation boundary

The Resident PK Directory V1 protocol, engine, and validation runner are frozen. The validation runner has not yet executed. No raw Phase 6B.9 validation result or runtime exists yet.

### Explicit nonclaims

Resident PK Directory V1 does not implement Segment Reader behavior, perform inference, perform tensor math, enable MAF-native compute, select a production storage engine, require a source GGUF for resident lookup, or begin Phase 6C.
