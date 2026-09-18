# MAF Generation Engine V1.1 Corrective Validation Protocol

Status: Preregistered Phase 6B.5 corrective-validation protocol.

## 1. Purpose

This protocol defines a narrow corrective validation of the already
frozen MAF Generation Engine V1.

It does not replace, rewrite, delete, or retroactively alter the frozen
V1 validation record.

The V1 result remains historical evidence exactly as recorded.

## 2. Frozen V1 artifacts

The engine under validation remains:

    experiments/model_fractal/
    maf_generation_engine_v1.py

The frozen V1 validation runner remains:

    experiments/model_fractal/
    maf_generation_engine_validation_v1.py

The frozen V1 raw result remains:

    experiments/model_fractal/
    maf_generation_engine_validation_v1.json

None of these files may be modified by the V1.1 corrective-validation
sequence.

## 3. Frozen V1 result

The V1 raw result records:

    all_pass = false

The V1 result also records successful behavioral evidence including:

- positive generation construction;
- preregistered negative controls;
- deterministic generation_pk;
- caller-order independence;
- filesystem-path independence;
- physical-placement sensitivity;
- model_pk preservation;
- object_pk preservation;
- exact segment integrity verification;
- exact object-range integrity verification;
- manifest persistence and reopen verification;
- source-segment immutability;
- no generation activation;
- no selected catalog engine;
- no engine mmap use;
- MAF-native compute remaining disabled.

The aggregate V1 failure includes:

    static_policy_checks.runner_no_source_gguf_path = false

## 4. Corrective hypothesis

V1.1 tests whether the failed runner static-policy result was caused by
the validation mechanism conflating policy language about a prohibited
source-GGUF dependency with executable logic that actually requires or
accesses a source GGUF.

V1.1 must test that distinction without weakening the original engine
contract.

## 5. Corrective scope

V1.1 may change validation-runner logic only.

Generation Engine V1 itself must remain unchanged.

V1.1 must not remove a previously passing positive requirement.

V1.1 must not remove a previously passing negative control.

V1.1 must not alter logical identities merely to obtain a passing
aggregate result.

## 6. Source-GGUF independence contract

Generation Engine validation must operate from already validated,
immutable MAF physical evidence.

Execution must not require the source GGUF.

The V1.1 runner must not obtain validation truth by:

- opening the source GGUF;
- reading the source GGUF;
- hashing the source GGUF;
- statting the source GGUF;
- resolving a source-GGUF path for validation input;
- deriving expected object evidence directly from the source GGUF.

The raw V1.1 result must record:

    source_gguf_required = false

## 7. Corrected runner static-policy test

V1.1 must explicitly determine whether the runner contains an
operational source-GGUF dependency.

The static test must distinguish between:

1. descriptive or policy text that names or prohibits source-GGUF
   access; and

2. executable behavior that identifies, resolves, opens, reads,
   hashes, stats, or otherwise depends upon a source GGUF.

Policy language alone must not cause the static check to fail.

Executable source-GGUF dependency must cause the check to fail.

## 8. Required inherited positive validation

V1.1 must repeat the V1 positive validation and establish at minimum:

- canonical manifest bytes;
- descriptor SHA256 reproduces generation_pk identity;
- generation_pk reproduces on reopen;
- exact model_pk preservation;
- exact object_pk preservation;
- exact object count;
- exact object placement offsets;
- exact object lengths;
- exact object_file_sha256 values;
- exact payload_sha256 values;
- exact segment count;
- exact segment length;
- exact segment SHA256;
- persisted manifest equals validated in-memory representation;
- repeated construction is deterministic;
- caller object-order permutation is identity-neutral.

## 9. Required inherited negative controls

V1.1 must retain fail-closed controls for at least:

- duplicate object_pk;
- mixed-model request;
- missing segment;
- altered segment SHA256;
- out-of-bounds object placement;
- zero-length placement;
- incorrect object_file_sha256;
- malformed object_pk;
- malformed SHA256;
- pre-existing final manifest;
- pre-existing partial manifest;
- generation_pk mismatch on reopen.

Every negative control must fail closed.

## 10. Structural controls

V1.1 must repeat:

- multi-segment order independence;
- filesystem-path independence;
- physical-placement sensitivity;
- object_pk stability across placement changes;
- source-segment unchanged verification.

## 11. Engine policy controls

V1.1 must continue to establish:

    engine_no_activation_api = true
    engine_no_mmap = true
    engine_no_sqlite = true
    maf_native_not_enabled = true

A corrective validation may not weaken these controls.

## 12. Aggregate pass rule

V1.1 may record:

    all_pass = true

only if all required checks pass.

This includes:

- inherited positive validation;
- inherited negative controls;
- structural controls;
- source-segment immutability;
- source_gguf_required = false;
- corrected runner source-GGUF policy check;
- engine static-policy controls.

No failed individual requirement may be hidden by the aggregate result.

## 13. Historical interpretation rule

A future successful V1.1 result must not be interpreted as changing the
historical V1 result.

Both statements may simultaneously be true:

    V1 validation:
        all_pass = false

    V1.1 corrective validation:
        all_pass = true

They represent distinct frozen validation artifacts.

## 14. Expected V1.1 runner

The preregistered corrective validation runner is:

    experiments/model_fractal/
    maf_generation_engine_validation_v1_1.py

The runner must be frozen before execution.

## 15. Expected V1.1 raw result

The corrective raw result is:

    experiments/model_fractal/
    maf_generation_engine_validation_v1_1.json

The V1.1 result must never overwrite the V1 result.

## 16. Freeze order

The required order is:

    frozen Generation Engine V1
        ->
    frozen V1 validation runner
        ->
    frozen V1 raw result
        ->
    frozen V1.1 corrective-validation protocol
        ->
    implement V1.1 runner
        ->
    freeze V1.1 runner
        ->
    execute frozen V1.1 runner
        ->
    freeze V1.1 raw result
        ->
    interpret result

Implementation and execution must remain separate stages.

## 17. Activation boundary

Generation activation is outside V1.1.

Rollback is outside V1.1.

V1.1 must not add:

- active-generation switching;
- rollback behavior;
- production catalog authority;
- resident-directory behavior.

Those require independently preregistered later Phase 6B gates.

## 18. Storage-engine boundary

V1.1 does not select:

- SQLite;
- MAFDB;
- a compiled binary index;
- mmap;
- another persistent catalog engine.

Correctness must be frozen before storage-engine promotion.

## 19. Compute boundary

V1.1 does not establish:

- selective inference;
- dense-materialization avoidance;
- MAF-native computation;
- Vulkan execution;
- model replacement.

These remain later research questions.

## 20. Acceptance criterion

Phase 6B.5 corrective validation may advance to interpretation only
after:

1. this protocol is frozen;
2. the V1.1 runner is independently implemented;
3. the V1.1 runner is frozen before execution;
4. the frozen runner is executed;
5. the raw V1.1 result is frozen before interpretation.

This protocol alone does not complete Phase 6B.5.
