# MAF Research

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
