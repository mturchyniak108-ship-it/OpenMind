# MAF Activation V1 Protocol

Status: Preregistered Phase 6B.6 research protocol.

## 1. Purpose

This protocol defines the authority semantics required to move one
validated immutable MAF generation from candidate state to active state.

It defines the contract consumed by Phase 6B.7 atomic-activation
implementation and validation.

This protocol does not itself implement activation.

## 2. Existing authority chain

The frozen catalog-generation authority model is:

    logical PK
        ->
    active generation
        ->
    immutable segment / offset / length

A generation manifest is candidate physical evidence.

A generation does not become authoritative merely because:

- its segment files exist;
- Segment Builder validation passed;
- its generation manifest exists;
- its generation_pk is valid;
- Generation Engine validation passed.

Authority begins only through explicit activation.

## 3. Frozen prerequisite evidence

Activation V1 consumes the contracts established by:

    MAF_CATALOG_GENERATION_V1_PROTOCOL.md
    MAF_GENERATION_DESCRIPTOR_V1_PROTOCOL.md
    MAF_GENERATION_ENGINE_V1_PROTOCOL.md
    MAF_GENERATION_ENGINE_V1_1_PROTOCOL.md

Generation Engine V1 remains unchanged.

The frozen V1.1 validation established a valid candidate generation
without activating it.

## 4. Authority domain

Activation authority is model-scoped.

For one:

    model_pk

there may be at most one authoritative active generation at a time.

Different models may independently have different active generations.

Activation must not silently cross model boundaries.

## 5. Candidate identity

The activation target is identified by:

    model_pk
    generation_pk

The target generation_pk must be reproduced from the immutable canonical
generation descriptor contained in the candidate generation manifest.

Activation must not invent, rewrite, alias, or substitute generation_pk.

## 6. Logical identity preservation

Activation changes authority only.

It must not alter:

- model_pk;
- object_pk;
- fragment identity;
- route/transition identity;
- generation_pk;
- segment_sha256;
- object_file_sha256;
- payload_sha256.

Logical identity remains separate from mutable active-state authority.

## 7. Generation identity independence

The following must not enter generation_pk:

- active/inactive state;
- activation timestamp;
- active-record path;
- process ID;
- RAM address;
- mmap address;
- device residency;
- cache state;
- storage-engine choice.

Activating a generation therefore does not create a new generation.

## 8. Active-generation authority record

Activation V1 defines one minimal canonical authority record.

Schema:

    openmind.maf_active_generation.v1

Version:

    maf_active_generation_v1

Required fields:

    schema
    active_generation_version
    model_pk
    generation_pk
    generation_manifest_sha256

No additional field is authoritative in V1.

## 9. Active record is mutable authority state

The active-generation record is not a new logical PK object.

Its purpose is to identify which immutable generation currently has
authority for one model.

Its content may change only through a valid authority transition.

The generations it references remain immutable.

## 10. Manifest integrity binding

The active record must bind the target generation to the exact validated
candidate manifest bytes through:

    generation_manifest_sha256

This integrity hash is not part of generation_pk.

It exists to prevent the authority record from silently referring to
different manifest bytes under the same external location.

## 11. Path independence

The active authority record must not contain the candidate manifest
filesystem path.

A candidate manifest may be relocated without changing:

- model_pk;
- generation_pk;
- generation_manifest_sha256;
- canonical active-record bytes.

The physical path supplied to an activation call is execution metadata,
not authority identity.

## 12. Source-GGUF independence

Activation must not require the source GGUF.

Activation must not:

- open the source GGUF;
- read the source GGUF;
- hash the source GGUF;
- stat the source GGUF;
- derive authority from a source-GGUF path.

The activation authority transition consumes validated MAF generation
evidence only.

## 13. Activation request

The Phase 6B.7 reference implementation must accept an explicit target
containing at minimum:

    model_pk
    generation_pk
    candidate_manifest_path
    active_record_path

The caller-provided model_pk and generation_pk are expectations.

They must be checked against the independently reopened candidate
manifest.

## 14. Candidate-manifest precondition

Before an authority transition, activation must independently reopen and
verify the candidate generation manifest.

At minimum it must establish:

- candidate manifest exists as a regular file;
- manifest JSON is valid;
- manifest schema is correct;
- manifest version is correct;
- descriptor schema is correct;
- descriptor content is valid;
- generation_pk reproduces from the descriptor;
- reproduced generation_pk equals the manifest generation_pk;
- manifest model_pk equals the requested model_pk;
- manifest generation_pk equals the requested generation_pk;
- canonical persisted bytes match canonical reconstructed bytes.

A failed precondition must fail closed.

## 15. Validated-candidate requirement

Activation may consume only a candidate produced under the frozen
Generation Engine contract from validated immutable MAF physical
evidence.

Activation does not relax or replace Generation Engine validation.

The activation layer must not fabricate placement evidence that is absent
from the candidate generation.

## 16. Candidate versus active state

Before successful activation:

    candidate != authoritative merely because it exists

After successful activation:

    active_record.generation_pk == target generation_pk

The active record is the explicit authority boundary.

## 17. First activation

If no valid active-generation record exists yet for the model, a valid
candidate may transition authority from:

    no active generation
        ->
    target generation

No partially written active record may become authoritative.

## 18. Replacement activation

If generation A is active and validated generation B is selected:

    generation A
        ->
    generation B

must be one authority transition.

Readers must observe either complete authority for A or complete
authority for B.

They must not observe a record that mixes fields from both.

## 19. Atomicity requirement

Activation V1 requires atomic authority semantics.

The concrete persistence mechanism is implemented in Phase 6B.7.

The protocol requires the observable result:

    old complete active record

or:

    new complete active record

and never:

    partially written active record

This protocol does not select a database engine merely to provide that
property.

## 20. Linearization point

The authority transition has one commit point.

All candidate validation and active-record construction that can fail
must occur before the commit point where practical.

Before that commit point, the previous valid active state remains
authoritative.

After a successful commit point, the new complete active record is
authoritative.

The implementation must not report a pre-commit validation failure after
authority has already been changed.

## 21. Failed activation

A failure before the authority commit point must leave the previously
valid active record byte-for-byte unchanged.

A failed first activation must leave no completed active record.

A failure must never produce mixed-generation authority.

## 22. Existing active-state validation

Before replacing an existing active record, the implementation must
validate the existing record sufficiently to establish its complete
model-scoped authority state.

A malformed or internally inconsistent existing active record must fail
closed.

Activation V1 must not silently overwrite corrupted authority state.

## 23. Same-generation reactivation

If the currently valid active record already identifies exactly the same:

    model_pk
    generation_pk
    generation_manifest_sha256

reactivation is an idempotent success.

The canonical active record must remain byte-for-byte unchanged.

This does not create a new generation or new logical identity.

## 24. Cross-model rejection

If:

    requested model_pk
        !=
    candidate manifest model_pk

activation must fail closed.

If an existing active record at the supplied authority location belongs
to a different model_pk, activation must fail closed.

## 25. Manifest mutation rejection

If the candidate manifest bytes change such that:

    generation_manifest_sha256

changes, the previously computed activation target is not equivalent.

Activation must independently hash the exact manifest bytes it is
authorizing.

## 26. Immutable-generation rule

Activation must not modify:

- candidate generation manifest bytes;
- descriptor bytes;
- adopted segment bytes;
- object bytes;
- placement offsets;
- integrity hashes.

Only active-state authority may change.

## 27. Old generation retention

Replacing the active authority reference does not delete or rewrite the
previous generation.

Generation retirement is separate from activation.

Physical deletion is outside Activation V1.

The previous immutable generation must remain independently addressable
for later rollback research.

## 28. Rollback boundary

Rollback is Phase 6B.8.

Activation V1 must not expose a rollback API.

Activation V1 must not claim rollback correctness.

A future rollback operation may reuse the same authority-transition
semantics, but it requires its own frozen protocol and validation.

## 29. Persistence boundary

The active authority state must survive ordinary process termination and
subsequent process restart.

Phase 6B.7 must demonstrate independent reopen of the completed active
record.

Crash/power-loss guarantees beyond the validated local persistence
mechanism must not be claimed without separate evidence.

## 30. Storage-engine neutrality

Activation V1 does not select:

- SQLite;
- MAFDB;
- mmap;
- a compiled binary catalog;
- another embedded database.

A file-based canonical reference record may be used to validate
correctness without promoting that representation to production catalog
authority architecture.

Storage-engine comparison remains a later measured decision.

## 31. JSON boundary

Canonical JSON may be used for the Phase 6B.7 research authority record
and validation artifact.

This does not authorize JSON parsing on the inference hot path.

Resident and hot-path representations remain later gates.

## 32. Residency boundary

Activation does not:

- load model tensors into RAM;
- assign device residency;
- allocate Vulkan resources;
- construct dense compute views;
- populate the resident PK directory.

Those are later Phase 6B/6C responsibilities.

## 33. Compute boundary

Activation does not establish:

- selective inference;
- MAF-native computation;
- dense-materialization avoidance;
- Vulkan execution;
- replacement of a standard LLM execution pipeline.

It changes catalog authority only.

## 34. Phase 6B.7 implementation target

The expected reference implementation is:

    experiments/model_fractal/
    maf_activation_v1.py

It must be frozen before its validation execution.

## 35. Phase 6B.7 validation runner

The expected preregistered validation runner is:

    experiments/model_fractal/
    maf_activation_validation_v1.py

Expected raw result:

    experiments/model_fractal/
    maf_activation_validation_v1.json

Expected runtime:

    results/runtime/
    maf_activation_validation_v1

The raw result must be frozen before interpretation.

## 36. Positive validation requirements

Phase 6B.7 validation must establish at minimum:

- first activation succeeds;
- completed active record has the exact required field set;
- active record uses canonical deterministic bytes;
- active record model_pk is exact;
- active record generation_pk is exact;
- generation_manifest_sha256 is exact;
- completed active record independently reopens;
- reopened active record validates;
- same-generation activation is idempotent;
- idempotent reactivation does not rewrite canonical bytes;
- replacement activation changes authority from A to B;
- old generation evidence remains unchanged;
- new generation evidence remains unchanged;
- logical PK identity remains unchanged;
- active record contains no candidate filesystem path;
- source GGUF is not required.

## 37. Required negative controls

Phase 6B.7 validation must fail closed for at least:

- missing candidate manifest;
- malformed candidate JSON;
- invalid manifest schema;
- invalid manifest version;
- generation_pk mismatch;
- requested generation_pk mismatch;
- requested model_pk mismatch;
- malformed model_pk;
- malformed generation_pk;
- corrupted candidate manifest;
- malformed existing active record;
- cross-model existing active record;
- pre-existing partial active-record target;
- injected failure before atomic authority replacement.

For a failed replacement activation, the previously active canonical
record must remain byte-for-byte unchanged.

## 38. Replacement fault control

The validation runner must include a controlled failure before the
authority commit point.

That failure must demonstrate:

    previous active bytes before failure
        ==
    previous active bytes after failure

No completed new authority record may be observed from that failed
attempt.

## 39. No mixed-state control

Validation must demonstrate that the completed authority record always
describes one complete generation.

No test may pass if fields from two generations are combined.

## 40. Static policy controls

Phase 6B.7 validation must establish that the activation implementation:

- does not modify Generation Engine V1;
- does not require source GGUF access;
- does not implement rollback;
- does not select SQLite;
- does not select mmap;
- does not enable MAF-native computation;
- does not perform inference;
- does not delete generations.

## 41. Aggregate validation rule

The activation validation result may record:

    all_pass = true

only if all positive, negative, structural, integrity, atomicity, and
scope-boundary controls pass.

No individual failed control may be hidden by the aggregate result.

## 42. Freeze order

The required research order is:

    frozen Phase 6B.5 evidence
        ->
    frozen Activation V1 protocol
        ->
    implement Activation V1
        ->
    preregister/freeze validation runner
        ->
    freeze implementation and runner
        ->
    execute frozen validation
        ->
    freeze raw validation result
        ->
    interpret
        ->
    document Phase 6B.7 result

Implementation must not be executed experimentally before the required
protocol/runner freeze boundary.

## 43. Phase boundary

Freezing this protocol completes Phase 6B.6 only.

It does not complete Phase 6B.7.

After this protocol is frozen, the first incomplete gate becomes:

    Phase 6B.7 — Atomic activation

Rollback remains:

    Phase 6B.8 — NOT STARTED

## 44. Nonclaims

Activation V1 protocol alone does not establish:

- implemented activation;
- validated atomic replacement;
- rollback;
- generation retirement;
- production catalog persistence;
- a selected catalog database;
- multi-writer concurrency safety;
- inference-hot-path lookup;
- resident PK directory performance;
- runtime residency;
- selective inference;
- MAF-native compute;
- Vulkan execution.

Those claims require later independently frozen evidence.

## 45. Frozen invariant summary

The intended invariant is:

    immutable validated candidate generation
        +
    explicit model-scoped authority transition
        =
    one active generation reference

while:

    model_pk remains unchanged
    object_pk remains unchanged
    generation_pk remains unchanged
    generation manifest remains immutable
    segment bytes remain immutable
    active authority contains no physical manifest path
    failed pre-commit activation preserves prior authority
    rollback remains separate
    storage-engine choice remains unselected
