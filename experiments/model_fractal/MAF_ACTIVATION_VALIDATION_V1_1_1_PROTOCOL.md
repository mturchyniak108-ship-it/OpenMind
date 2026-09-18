# MAF Activation Validation V1.1.1 Corrective Protocol

Status: Preregistered Phase 6B.7 validation-only correction.

## 1. Purpose

Validation V1.1.1 corrects one confirmed false-negative expectation in the
frozen Activation V1.1 validation runner.

It does not modify Activation V1.1 behavior.

It does not rewrite historical V1.1 evidence.

## 2. Frozen historical chain

Frozen Activation V1.1 engine:

    experiments/model_fractal/
    maf_activation_v1_1.py

SHA256:

    9435ae8dd32656c7350887689d453f3c
    b8460887068bfaf06e6f68b5b5b927a1

Frozen Activation V1.1 runner:

    experiments/model_fractal/
    maf_activation_validation_v1_1.py

SHA256:

    b6457a3f9e9cdf971b6d92f4531c4484
    790146b1fcc4f4f10f20280f60c9f664

Frozen Activation V1.1 raw result:

    experiments/model_fractal/
    maf_activation_validation_v1_1.json

SHA256:

    aff5b47e3ff6cbd611b2b29fa1ce826d
    fce1ece6fdc7356fb94ba9fefe41b548

Historical V1.1 remains:

    all_pass = false

## 3. Exact historical failing control

Exactly one V1.1 negative control recorded pass=false:

    multi_segment_wrong_content_association

Its frozen record is:

    raised        = true
    failed_closed = true
    error_type    = MAFActivationError
    error_text    = segment length mismatch
    pass          = false

The activation target was rejected.

No authority acceptance occurred.

## 4. Confirmed historical runner expectation

The frozen runner's AST establishes that this control supplied:

    expected_text = "segment SHA256 mismatch"

The shared expect_failure helper counts a control as passing only when the
raised error contains the supplied expected_text.

The V1.1 false negative therefore resulted from the runner's exact
rejection-text expectation.

## 5. Controlled fixture

The frozen multi-segment fixture uses unequal segment sizes:

    2048 bytes
    3072 bytes

The negative control swaps the segment_id -> physical path associations.

The wrong physical content therefore violates the immutable declared
segment length before SHA256 comparison needs to occur.

Frozen Generation Engine correctly raises:

    segment length mismatch

at that earlier integrity boundary.

## 6. Frozen Activation V1.1 requirement

The frozen Activation V1.1 corrective protocol requires:

    Mapping a segment_id to the wrong physical content must fail closed.

It also requires segment association to be determined by immutable
descriptor integrity rather than caller order.

It does not require segment SHA256 validation to occur before segment
length validation.

## 7. Classification

The evidence establishes:

    Activation V1.1 engine defect:
        NOT INDICATED

    Validation V1.1 runner expectation defect:
        CONFIRMED

No activation-engine correction is authorized by this protocol.

## 8. Correction scope

Validation V1.1.1 may change only:

- validation schema/version identifiers required for a distinct run;
- validation result/runtime paths required for historical isolation;
- the expectation semantics of
  multi_segment_wrong_content_association;
- narrowly necessary validation helper logic for that corrected
  expectation.

All substantive Activation V1.1 behavior remains frozen.

## 9. Corrected wrong-content control

The corrected:

    multi_segment_wrong_content_association

control must prove:

1. a genuinely wrong segment_id -> physical path association is supplied;
2. Activation V1.1 raises MAFActivationError;
3. the activation/build operation does not accept the target;
4. existing authority is preserved when applicable;
5. any controlled partial state is preserved or absent according to the
   existing negative-control contract;
6. the rejection is an expected immutable segment-integrity rejection.

For the frozen unequal-length fixture, the accepted error family is
exactly:

    segment length mismatch
    segment SHA256 mismatch

Either establishes rejection of the wrong current physical content.

## 10. No generic-exception weakening

The corrected control must not pass merely because any arbitrary exception
was raised.

The exception must remain:

    MAFActivationError

and its error text must match one of the preregistered physical-integrity
messages:

    segment length mismatch
    segment SHA256 mismatch

A programming error or unrelated exception is not success.

## 11. Validation-suite preservation

V1.1.1 must preserve the substantive V1.1 validation suite, including:

- positive activation;
- exact active-record fields;
- manifest-hash binding;
- physical descriptor reconstruction;
- exact descriptor equality;
- generation_pk reconstruction;
- synthetic canonical-manifest rejection;
- missing and extra segment mapping rejection;
- missing physical segment rejection;
- non-regular segment rejection;
- segment-length rejection;
- segment-SHA rejection;
- object-byte-range rejection;
- same-generation physical revalidation;
- malformed existing-active rejection;
- cross-model rejection;
- pre-existing partial rejection;
- multi-segment order independence;
- wrong-content association rejection;
- injected pre-os.replace failure preservation;
- replacement atomicity;
- source-GGUF independence;
- no rollback;
- no SQLite;
- no mmap;
- no generation deletion;
- no inference;
- no MAF-native compute.

## 12. Historical runner preservation

The frozen V1.1 runner:

    experiments/model_fractal/
    maf_activation_validation_v1_1.py

must remain byte-for-byte unchanged.

Its SHA256 remains:

    b6457a3f9e9cdf971b6d92f4531c4484
    790146b1fcc4f4f10f20280f60c9f664

It must not be reexecuted.

## 13. Historical result preservation

The frozen V1.1 result:

    experiments/model_fractal/
    maf_activation_validation_v1_1.json

must remain byte-for-byte unchanged.

Its SHA256 remains:

    aff5b47e3ff6cbd611b2b29fa1ce826d
    fce1ece6fdc7356fb94ba9fefe41b548

Its:

    all_pass = false

remains historical truth.

A future V1.1.1 result must not retroactively rewrite V1.1.

## 14. Historical runtime preservation

The existing V1.1 runtime:

    results/runtime/
    maf_activation_validation_v1_1

must remain untouched.

It must not be cleaned, reused, replaced, or adopted as V1.1.1 runtime.

## 15. Corrected runner target

The only corrected runner target is:

    experiments/model_fractal/
    maf_activation_validation_v1_1_1.py

It must be preregistered, statically audited, and frozen before execution.

## 16. Corrected result target

The only corrected result target is:

    experiments/model_fractal/
    maf_activation_validation_v1_1_1.json

It must not exist before V1.1.1 execution.

Its raw bytes must be frozen before interpretation.

## 17. Corrected runtime target

The only corrected runtime target is:

    results/runtime/
    maf_activation_validation_v1_1_1

It must not exist before V1.1.1 execution.

It must remain separate from V1.1 evidence.

## 18. Runner-delta requirement

Before V1.1.1 execution, static audit must demonstrate that the corrected
runner is a narrow derivative of frozen V1.1.

The audit must establish at minimum:

- historical V1.1 runner hash unchanged;
- Activation V1.1 engine hash unchanged;
- Activation V1 engine hash unchanged;
- Generation Engine V1 hash unchanged;
- historical V1.1 result hash unchanged;
- historical V1.1 runtime preserved;
- substantive test inventory preserved;
- corrected schema/version/result/runtime identifiers are distinct;
- wrong-content expectation accepts only the preregistered integrity error
  family;
- no other behavioral expectation is intentionally relaxed.

## 19. Execution rule

V1.1.1 must not execute until:

1. this protocol is frozen;
2. the corrected runner is created;
3. the corrected runner is statically audited;
4. the corrected runner is frozen in Git;
5. all implementation and historical-evidence hashes are rechecked;
6. corrected result and runtime targets are confirmed absent.

The frozen V1.1.1 runner then executes exactly once.

## 20. No retry rule

If V1.1.1 executes and fails:

- do not rerun it;
- preserve the raw result if produced;
- preserve the runtime;
- freeze raw result evidence before interpretation;
- diagnose through a new additive correction if necessary.

## 21. Aggregate success

V1.1.1 may record:

    all_pass = true

only when every preregistered positive, negative, integrity, atomicity,
static-policy, and scope-boundary control passes.

The corrected multi-segment control must not be special-cased out of the
aggregate.

## 22. Phase boundary

Freezing this protocol does not complete Phase 6B.7.

Phase 6B.7 remains:

    Atomic activation — INCOMPLETE / CURRENT

The next single gate after this protocol freeze is:

    create, statically audit, and freeze
    maf_activation_validation_v1_1_1.py

without executing it.

## 23. Rollback boundary

Rollback remains:

    Phase 6B.8 — NOT STARTED

No rollback implementation or validation is authorized here.

## 24. Corrective invariant

The historical engine behavior:

    wrong physical association
        ->
    immutable segment-integrity failure
        ->
    MAFActivationError
        ->
    fail closed
        ->
    no authority acceptance

was correct.

The historical runner expectation:

    only "segment SHA256 mismatch" counts

was too narrow for an unequal-length wrong-content substitution.

V1.1.1 corrects only that validation expectation while preserving the
engine and every historical artifact.
