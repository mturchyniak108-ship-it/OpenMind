# Phase 6B MAF Architecture Walkthrough

## Purpose

This walkthrough explains the current Phase 6B model-object architecture without executing the still-unrun Resident PK Directory validation runner.

## 1. Start with stable logical identity

A MAF object is identified logically by canonical PKs. Physical paths are not identity.

At minimum, Resident PK Directory V1 resolves:

```text
(model_pk, "object_pk", object_pk)
```

## 2. Build an immutable generation

A generation descriptor records immutable segment records and object mappings. Object mappings contain canonical segment ID, offset, length, and integrity hashes.

The resulting `generation_pk` is bound to canonical descriptor content.

## 3. Validate current physical evidence

Before a generation can become active or resident, current segment files and object byte ranges are validated against the immutable descriptor.

Validation includes segment mapping, regular-file status, exact segment length, segment SHA256, object bounds, object byte-range SHA256, descriptor reconstruction, and generation reconstruction.

## 4. Atomic Activation selects authority

Atomic Activation validates the complete candidate before publishing the canonical five-field active-generation record.

The active record selects the current generation. It does not rewrite generation identity.

Phase 6B.7 Atomic Activation is complete and validated.

## 5. Rollback changes authority without deleting generations

Rollback validates a retained target generation and atomically selects it as active.

Rollback does not delete the generation being left, mutate generation bytes, or invent historical provenance.

Phase 6B.8 Rollback is complete and validated.

## 6. Build the Resident PK Directory

Resident PK Directory V1 reopens current active authority, verifies manifest binding, reuses the frozen physical-validation semantics, builds all resident entries, and publishes one immutable snapshot only after construction succeeds.

A resident entry preserves logical and integrity evidence while also retaining the current physical segment path as runtime metadata.

## 7. Perform direct logical lookup

A successful lookup is model-scoped and requires the expected generation.

The lookup checks model identity, generation freshness, supported PK class, and then directly indexes the immutable resident map.

No JSON parse, manifest scan, filesystem discovery, or linear descriptor scan belongs on this successful lookup path.

## 8. Activation and rollback make old snapshots stale

After activation A -> B, snapshot A is stale.

After rollback B -> A, snapshot B is stale.

The newly current generation must be rebuilt or refreshed from current physical evidence before current-generation lookup is served.

## 9. Failed refresh does not corrupt serving state

A replacement snapshot is constructed before publication. If construction fails, the previously published valid snapshot remains unchanged.

## 10. Physical relocation does not change identity

Moving byte-identical valid segment evidence may change runtime path metadata. It must not change `model_pk`, `generation_pk`, `object_pk`, segment ID, offset, length, or canonical integrity hashes.

## 11. What has been validated

- Generation construction and reconstruction foundations;
- Atomic Activation;
- Rollback.

## 12. What is frozen but not yet validated

- Resident PK Directory V1 engine;
- Resident PK Directory Validation V1 runner.

The Resident PK Directory validation runner has not yet executed. Its raw result and runtime remain absent.

## 13. What remains a target rather than a result

Average O(1) resident lookup is an implementation target. It is not yet an accepted Phase 6B.9 benchmark result.

## 14. What Phase 6B.9 does not claim

- no Segment Reader implementation;
- no source-GGUF dependency for resident lookup;
- no production storage-engine selection;
- no MAF-native tensor computation;
- no replacement for `llama.cpp`;
- no Phase 6C runtime or residency completion.

## 15. Current next gate

After this documentation checkpoint is frozen, the next research gate is the first and exact-once execution of the already-frozen Resident PK Directory Validation V1 runner.
