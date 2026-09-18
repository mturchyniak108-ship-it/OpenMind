# MAF Rollback V1 Protocol

Status: Preregistered Phase 6B.8 research protocol.

## 1. Purpose

Rollback V1 defines how authority may move from the currently active MAF
generation to retained immutable generation evidence.

Rollback changes authority only.

Rollback does not mutate generation identity or generation bytes.

## 2. Phase dependency

Phase 6B.7 Atomic Activation is complete.

Rollback V1 preserves the frozen authority model:

    logical model PK
        ->
    physically validated generation
        ->
    canonical five-field active-generation authority record

## 3. Authority schema

Rollback must not introduce a second authoritative schema.

The active record remains exactly the frozen Activation V1 fields:

    schema
    active_generation_version
    model_pk
    generation_pk
    generation_manifest_sha256

Rollback-specific paths, timestamps, flags, receipts, or physical locations
must not enter authoritative identity.

## 4. Operational rollback

Rollback V1 is:

    active generation A
        ->
    retained target generation B
        ->
    validate B's current physical evidence
        ->
    atomically replace active authority
        ->
    B becomes authoritative

Generation A remains retained and immutable.

## 5. Historical-provenance boundary

Phase 6B.7 did not create an authoritative append-only activation-history
journal.

Therefore Rollback V1 must not claim that arbitrary retained generation
evidence proves that the generation was historically authoritative.

Rollback V1 establishes operational reactivation of retained immutable
generation evidence.

A future historical-authority journal may strengthen that claim separately.

## 6. Minimum request

Rollback V1 requires:

    model_pk
    target_generation_pk
    target_candidate_manifest_path
    active_record_path
    target_segment_paths

target_segment_paths is execution metadata:

    segment_id -> physical path

It is not logical identity.

## 7. Current authority prerequisite

The current active record must be strictly reopened and validated before
rollback.

It must be:

- present as a regular file;
- canonical JSON;
- exact frozen five-field schema;
- valid model_pk;
- valid generation_pk;
- valid generation_manifest_sha256.

Malformed or corrupt current authority must fail closed.

Rollback must not overwrite corrupt authority merely because the target is
valid.

## 8. Model scope

The current active record model_pk must equal the requested model_pk.

The target generation descriptor model_pk must equal the requested model_pk.

Cross-model rollback must fail closed.

## 9. Target identity

target_generation_pk must match both:

- the target manifest generation_pk;
- the generation_pk reconstructed from the immutable target descriptor.

Rollback must not alias, renumber, or rewrite target identity.

## 10. Target manifest

The target manifest must satisfy the frozen Activation V1.1 candidate
requirements:

- regular file;
- valid JSON;
- correct schema/version;
- canonical bytes;
- Generation Engine structural verification;
- exact model consistency;
- exact generation identity.

## 11. Current physical validation

Rollback must validate target B's current physical evidence immediately
before authority transition.

Historical validity alone is insufficient.

## 12. Exact segment mapping

Required:

    set(target_segment_paths)
        ==
    set(target descriptor segment IDs)

Missing mapping fails.

Extra mapping fails.

Mapping iteration order must not affect identity.

## 13. Physical segment integrity

Before authority mutation, every target segment must satisfy:

- mapped path exists;
- mapped path is a regular file;
- physical length equals descriptor segment_length;
- physical SHA256 equals descriptor segment_sha256.

## 14. Object integrity

Every target object range must be within its segment and must reproduce the
descriptor object_file_sha256.

## 15. Payload boundary

Rollback inherits the frozen Generation Engine boundary:

payload_sha256 is not independently derived from raw segment bytes by the
Generation Engine.

Rollback must not claim otherwise.

## 16. Descriptor reconstruction

Rollback must reuse frozen Generation Engine reconstruction.

The reconstructed descriptor must equal the target descriptor exactly.

Canonical reconstructed descriptor bytes must equal canonical target
descriptor bytes.

Reconstructed descriptor SHA256 must match independently calculated target
descriptor SHA256.

## 17. Generation identity reconstruction

The reconstructed generation_pk must equal:

- target manifest generation_pk;
- requested target_generation_pk.

Any mismatch fails closed.

## 18. Manifest-byte binding

The new active record generation_manifest_sha256 must bind the exact
canonical target manifest bytes used for rollback.

Physical path relocation must not change this logical binding.

## 19. Path independence

Relocating byte-identical target manifest or segment evidence must not
change:

- model_pk;
- object_pk;
- generation_pk;
- generation_manifest_sha256;
- canonical active authority bytes.

## 20. Atomic transition

All target validation must complete before authority mutation.

Before commit:

    A remains authoritative

After successful commit:

    B is authoritative

There is one authority transition boundary.

## 21. Authority writer reuse

Rollback V1 should reuse the already validated Activation V1/V1.1 authority
transition rather than create another independent authority writer.

Preferred implementation shape:

    validate current authority
        ->
    validate rollback target
        ->
    delegate to frozen Activation V1.1 / Activation V1 authority path

A new independent os.replace authority mechanism is not justified by this
protocol.

## 22. Failure preservation

Every failure before authority replacement must preserve the current active
authority bytes exactly.

If A was active before a failed rollback, A remains active afterward.

## 23. Same-generation rollback

If the target generation is already active, rollback is idempotent only
after current physical target evidence is revalidated.

Record equality must not bypass physical validation.

Valid same-generation request:

    changed = false

and active bytes remain unchanged.

Invalid current physical evidence:

    fail closed

even if authority already names that generation.

## 24. A to B to A

A successful:

    A -> B

may later be followed by:

    B -> A

when A's retained immutable generation evidence is still available and
currently valid.

This is operational reactivation.

It does not invent historical-authority provenance.

## 25. No deletion

Rollback must not delete, retire, rewrite, or garbage-collect:

- generation A;
- generation B;
- manifests;
- segments;
- objects.

Generation retention policy is separate.

## 26. Source-model independence

Rollback must not require, open, read, hash, or stat a source GGUF.

Rollback operates on retained MAF generation evidence only.

## 27. Storage neutrality

Rollback V1 does not select:

- SQLite;
- MAFDB;
- mmap;
- a production catalog database;
- a resident-directory storage engine.

## 28. Compute boundary

Rollback does not:

- perform inference;
- enable MAF-native compute;
- choose GPU residency;
- load tensors;
- implement the Phase 6B.9 resident PK directory.

## 29. Concurrency boundary

Rollback V1 assumes one authority-changing process and immutable generation
evidence during target validation and authority commit.

It does not claim hostile multiwriter safety.

## 30. Crash-consistency boundary

Rollback inherits the already frozen Activation V1 persistence scope.

No stronger power-loss or filesystem-journaling guarantee is claimed.

## 31. Future implementation

The future implementation target is:

    experiments/model_fractal/maf_rollback_v1.py

It must be frozen before rollback validation.

## 32. Future validation

Future runner:

    experiments/model_fractal/maf_rollback_validation_v1.py

Future raw result:

    experiments/model_fractal/maf_rollback_validation_v1.json

Future runtime:

    results/runtime/maf_rollback_validation_v1

The runner must be preregistered and frozen before execution.

It must execute exactly once.

Any completed raw result must be frozen before interpretation.

Failed runtime evidence must not be silently cleaned.

## 33. Required future positive controls

Validation must include:

- valid current A authority;
- valid retained B;
- exact B physical reconstruction;
- rollback A -> B;
- canonical five-field authority;
- exact target generation_pk;
- exact target manifest hash binding;
- independent reopen;
- A retained unchanged;
- B retained unchanged;
- path independence;
- same-generation physical revalidation;
- idempotent changed=false behavior;
- later B -> A operational reactivation.

## 34. Required future negative controls

Validation must include:

- missing current authority;
- malformed current authority;
- noncanonical current authority;
- cross-model current authority;
- malformed requested model_pk;
- malformed target_generation_pk;
- missing target manifest;
- malformed target JSON;
- invalid target schema/version;
- target generation derivation mismatch;
- requested generation mismatch;
- requested model mismatch;
- noncanonical target manifest;
- missing target segment mapping;
- extra target segment mapping;
- missing mapped segment;
- nonregular mapped segment;
- segment length mismatch;
- segment SHA256 mismatch;
- object byte-range mismatch;
- wrong multi-segment physical association;
- invalid physical evidence on same-generation rollback;
- injected failure before authority replacement.

## 35. Static-policy requirements

Validation must prove:

- Activation V1 unchanged;
- Activation V1.1 unchanged;
- Generation Engine V1 unchanged;
- Phase 6B.7 evidence unchanged;
- no second authority schema;
- no invented historical-authority provenance;
- no generation deletion;
- no source GGUF dependency;
- no SQLite;
- no mmap;
- no inference;
- no MAF-native compute;
- no Phase 6B.9 implementation.

## 36. Completion rule

Freezing this protocol does not complete Phase 6B.8.

Phase 6B.8 completes only after:

1. rollback protocol frozen;
2. rollback implementation frozen;
3. rollback validation runner preregistered and frozen;
4. frozen runner executed exactly once;
5. raw result frozen before interpretation;
6. result satisfies this protocol;
7. completion checkpoint is documented.

## 37. Core invariant

    current authority A
        +
    retained immutable target B
        +
    current physical validation of B
        ->
    atomic authority replacement
        ->
    B authoritative
        +
    A still retained

with no logical identity rewrite, no source GGUF dependency, no generation
deletion, and no invented historical-authority provenance.
