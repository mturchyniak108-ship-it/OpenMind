# OpenMind — Session Resume

This file is the short authoritative handoff for continuing OpenMind
research in a new ChatGPT session.

Update it at meaningful research checkpoints.

## Repository

Repository:

    ~/OpenMind

Current branch:

    labs/multidimensional-maf

Phase 6B research anchor HEAD:

    7b4ed07

Commit:

    research: freeze initial MAF generation engine v1 validation result

Last verified GitHub state from the current research session:

    origin/main: aa17ed9
    origin/labs/multidimensional-maf: ABSENT

Therefore the current multidimensional-MAF research history is local-only.

Do not push upstream merely to synchronize history. Push only when
explicitly intended.

## Current Roadmap Position

Current major phase:

    Phase 6B — MAF Model Catalog and Segment Store [RESEARCH]

Work through incomplete lean gates one at a time.

Do not advance into Phase 6C while an earlier Phase 6B correctness gate
remains incomplete unless a deliberate research exception is documented.

## Phase 6B Current State

    6B.1 Authority / identity rules
        COMPLETE

    6B.2 Segment Builder
        COMPLETE + VALIDATED

    6B.3 Generation descriptor / manifest
        COMPLETE

    6B.4 Generation Engine V1
        COMPLETE

    6B.5 Generation Engine validation
        COMPLETE

    6B.6 Activation protocol
        COMPLETE

    6B.7 Atomic activation
        CURRENT INCOMPLETE GATE

    6B.8 Rollback
        NOT STARTED

    6B.9 Resident PK directory
        NOT STARTED

    6B.10 Segment Reader validation
        NOT STARTED

## Frozen V1 Validation State

Frozen raw result:

    experiments/model_fractal/
    maf_generation_engine_validation_v1.json

The frozen result records:

    all_pass = false

The behavioral Generation Engine evidence passed, including:

- positive construction validation;
- all preregistered negative controls;
- deterministic generation_pk;
- object-order independence;
- filesystem-path independence;
- placement sensitivity;
- model_pk preservation;
- object_pk preservation;
- segment SHA256 preservation;
- object-range SHA256 verification;
- manifest persistence/reopen verification;
- source-segment immutability;
- no generation activation;
- no SQLite engine selection;
- no mmap engine dependency;
- MAF-native computation remaining disabled.

The aggregate V1 failure came from:

    static_policy_checks.runner_no_source_gguf_path = false

The frozen V1 result is historical evidence and must not be rewritten.

## Current Corrective Direction

The next gate is an additive V1.1 corrective validation.

Expected sequence:

    frozen Generation Engine V1
        ->
    frozen V1 validation runner
        ->
    frozen V1 failed raw result
        ->
    V1.1 corrective-validation protocol
        ->
    freeze V1.1 runner
        ->
    execute V1.1
        ->
    freeze V1.1 raw result
        ->
    interpret
        ->
    decide whether 6B.5 is complete

Expected V1.1 files:

    experiments/model_fractal/
    MAF_GENERATION_ENGINE_V1_1_PROTOCOL.md

    experiments/model_fractal/
    maf_generation_engine_validation_v1_1.py

    experiments/model_fractal/
    maf_generation_engine_validation_v1_1.json

## Frozen-History Rule

Do not modify these V1 artifacts as part of V1.1:

    experiments/model_fractal/
    maf_generation_engine_v1.py

    experiments/model_fractal/
    maf_generation_engine_validation_v1.py

    experiments/model_fractal/
    maf_generation_engine_validation_v1.json

A successful V1.1 result does not convert the historical V1 failure into
a historical success.

Both records remain valid:

    V1 validation:
        all_pass = false

and, if demonstrated later:

    V1.1 corrective validation:
        all_pass = true

## Scope Boundary

Do not implement the following while 6B.5 remains open:

- generation activation;
- rollback;
- resident-directory optimization;
- storage-engine selection;
- SQLite catalog authority;
- MAFDB promotion;
- hot-path mmap;
- Phase 6C residency;
- selective inference;
- MAF-native computation;
- Vulkan MAF execution.

Those require later independently controlled gates.

## Working-Tree Safety

This repository contains many unrelated untracked historical experiment
and result files.

Do not use broad mutation commands such as:

    git add .
    git add -A
    git clean
    git clean -fd

Do not delete unusual untracked files merely because their names appear
accidental without first auditing them.

Use explicit paths for:

    git status
    git diff
    git add
    git commit

## Research Workflow

For each meaningful gate:

1. inspect read-only;
2. establish the first incomplete requirement;
3. preregister the protocol where appropriate;
4. freeze implementation before experimental execution;
5. execute the frozen implementation;
6. freeze raw results before interpretation;
7. interpret without rewriting history;
8. update documentation;
9. commit only targeted artifacts;
10. create/update this handoff;
11. reassess before advancing.

## Termux / ChatGPT Workflow

Prefer single-click paste command blocks.

Diagnostic blocks should end with:

    🟡⏱️ ===== PASTE BACK TO CHAT FROM HERE ===== ⏱️🟡

Do not use `exit` or `logout` in supplied Termux blocks.

## Immediate Resume Instruction

When a new ChatGPT session receives this file:

1. read this file first;
2. confirm branch and HEAD;
3. reconcile any difference read-only;
4. inspect only Phase 6B.5 artifacts;
5. continue the V1.1 corrective-validation sequence;
6. do not begin Phase 6B.6 until 6B.5 has a frozen interpreted result.

## V1.1 Protocol Freeze Checkpoint

The Phase 6B.5 corrective-validation protocol is now included in the
current targeted freeze:

    experiments/model_fractal/
    MAF_GENERATION_ENGINE_V1_1_PROTOCOL.md

The protocol preserves the frozen V1 history and defines the corrected
source-GGUF independence test.

## Phase 6B.5 Completion Checkpoint

Phase 6B.5 — Generation Engine validation is COMPLETE.

Historical V1 result:

    experiments/model_fractal/
    maf_generation_engine_validation_v1.json

    all_pass = false

The V1 failure remains preserved exactly as historical evidence.

Corrective V1.1 protocol:

    experiments/model_fractal/
    MAF_GENERATION_ENGINE_V1_1_PROTOCOL.md

Frozen V1.1 runner:

    experiments/model_fractal/
    maf_generation_engine_validation_v1_1.py

    commit:
        33ebd95

    sha256:
        f9dc577d25f75b2cb57dde633fbdd2bc
        4ab0d9213d285aa31901843115fa9ec3

Frozen V1.1 raw result:

    experiments/model_fractal/
    maf_generation_engine_validation_v1_1.json

    commit:
        9dbb325

    sha256:
        a37ee07ab548b1dea398bb42de42cd89
        3df437b06b91a8a767464a4559e52727

V1.1 records:

    all_pass = true
    source_gguf_required = false
    generation_activated = false
    catalog_engine_selected = false
    maf_native_compute_enabled = false

Validated evidence:

- 16/16 positive checks pass;
- 12/12 negative controls pass;
- generation_pk is unchanged from V1;
- path independence passes;
- multi-segment order independence passes;
- placement sensitivity passes;
- source-segment immutability passes;
- engine static-policy controls pass;
- corrected runner source-GGUF policy check passes.

The complete V1/V1.1 JSON comparison produced only five differences:

- schema version;
- aggregate all_pass;
- corrected runner static-policy value;
- V1/V1.1 runtime path in positive manifest_path;
- V1/V1.1 runtime path in missing-segment error_text.

No behavioral validation evidence was weakened.

The V1.1 runtime directory remains untracked research/runtime evidence and
has not been cleaned as part of this interpretation checkpoint.

## Phase 6B.6 Activation Protocol Checkpoint

Phase 6B.6 — Activation Protocol is COMPLETE.

Frozen protocol:

    experiments/model_fractal/
    MAF_ACTIVATION_V1_PROTOCOL.md

The protocol defines one model-scoped active-generation authority record:

    schema
    active_generation_version
    model_pk
    generation_pk
    generation_manifest_sha256

The authority record:

- references one validated immutable generation;
- contains no candidate manifest filesystem path;
- does not change logical PK identity;
- does not change generation_pk;
- does not modify generation/segment/object bytes;
- does not require the source GGUF;
- remains independent of catalog storage-engine choice.

The protocol defines required old-or-new atomic authority semantics.

It does not implement those semantics.

Rollback remains explicitly outside scope.

## Phase 6B.7 Activation Engine Freeze Checkpoint

The minimum Activation V1 reference engine is now included in the
current targeted freeze:

    experiments/model_fractal/
    maf_activation_v1.py

The implementation reuses the frozen Generation Engine V1 manifest
verification contract rather than duplicating generation identity logic.

Public authority surface:

    build_active_record(...)
    verify_active_record(...)
    reopen_active_generation(...)
    activate_generation(...)

Only:

    activate_generation(...)

mutates active-generation authority.

The implementation uses canonical active-record bytes and a sibling
partial file followed by fsync and os.replace.

The os.replace operation is the authority linearization point.

The later validation runner can inject a pre-commit replacement failure
by replacing os.replace during the controlled negative test. No
test-specific mutation API is included in the activation engine.

No activation call has been executed at this checkpoint.

No activation validation runner or raw result exists at this checkpoint.

Rollback remains outside scope.

## Phase 6B.7 V1.1 Corrective Protocol Checkpoint

The frozen Activation V1 implementation remains preserved unchanged:

    experiments/model_fractal/
    maf_activation_v1.py

    commit:
        ca44146

    sha256:
        76d79f90d9bc30118a6dfe0297beacd9
        b323aed9f56876881f653a2c01c1f210

No activation call or Activation V1 validation execution occurred before
the corrective requirement was discovered.

Read-only audits 6B.7c1-c3 established:

- Generation Engine verify_manifest accepts canonical generation
  structure/identity without reopening physical segment bytes;
- a synthetic in-memory manifest can therefore pass verify_manifest
  without physical segment/object evidence;
- the generation manifest contains no historical validation receipt;
- physical segment paths intentionally do not enter generation identity;
- the frozen Generation Engine build_descriptor path revalidates current
  physical segment length/SHA and object byte ranges;
- current frozen physical evidence reconstructs the exact frozen candidate
  descriptor;
- reconstructed canonical descriptor bytes are exact;
- reconstructed generation_pk is exact.

The additive correction is preregistered as:

    experiments/model_fractal/
    MAF_ACTIVATION_V1_1_PROTOCOL.md

V1.1 defines activation eligibility as current physical reconstruction of
the exact immutable candidate generation.

Physical segment paths remain execution metadata only.

The active-record schema remains unchanged.

Historical Activation V1 remains untouched.

## Phase 6B.7 Activation V1.1 Engine Freeze Checkpoint

The additive Activation V1.1 implementation is now included in the
current targeted freeze:

    experiments/model_fractal/
    maf_activation_v1_1.py

Frozen prerequisite:

    experiments/model_fractal/
    MAF_ACTIVATION_V1_1_PROTOCOL.md

    commit:
        26d0a70

    sha256:
        94aebe64ab466f9ae94db91ce8a82f2c
        56f87376cd962f687d133712a491bcfb

Activation V1.1 adds only the corrective candidate-eligibility boundary.

Before any authority switch it:

- reopens and verifies canonical candidate manifest identity;
- requires an exact segment_id -> physical path execution mapping;
- reconstructs the descriptor through frozen Generation Engine
  build_descriptor;
- rechecks current segment length and SHA256;
- rechecks object byte-range SHA256;
- requires exact reconstructed descriptor equality;
- requires exact canonical descriptor-byte equality;
- requires exact descriptor SHA256;
- requires exact reconstructed generation_pk equality.

Physical paths remain execution metadata and do not enter generation or
active-record identity.

The five-field active authority record remains exactly the Activation V1
record.

The authority mutation itself remains delegated to frozen Activation V1,
so the existing partial/fsync/os.replace transition is not duplicated.

Every V1.1 activate_generation call performs physical eligibility checking
before delegating to Activation V1. Same-generation reactivation therefore
cannot bypass current physical reconstruction.

No activation call has been executed.

No V1.1 validation runner, raw result, or runtime exists.

Rollback remains outside scope.

## Phase 6B.7 Activation V1.1 Validation Runner Freeze Checkpoint

The frozen additive Activation V1.1 implementation remains:

    experiments/model_fractal/
    maf_activation_v1_1.py

    commit:
        bd52026

    sha256:
        9435ae8dd32656c7350887689d453f3c
        b8460887068bfaf06e6f68b5b5b927a1

The preregistered Activation V1.1 validation runner is now included in
the targeted freeze:

    experiments/model_fractal/
    maf_activation_validation_v1_1.py

Runner SHA256:

    b6457a3f9e9cdf971b6d92f4531c4484790146b1fcc4f4f10f20280f60c9f664

The runner is self-contained around controlled physical segment fixtures.

It preregisters:

- exact current-physical reconstruction of known-good candidates;
- first activation;
- exact five-field active authority;
- canonical active bytes;
- exact manifest SHA256 binding;
- independent authority reopen;
- manifest-path and segment-path independence;
- same-generation idempotence with no authority rewrite;
- same-generation physical revalidation before idempotent success;
- replacement generation A -> B;
- logical model/object PK preservation;
- multi-segment mapping-order independence;
- wrong segment-to-content association rejection;
- canonical synthetic-manifest rejection without physical evidence;
- missing/malformed/corrupt candidate controls;
- exact segment mapping controls;
- missing/non-regular/length/SHA physical segment controls;
- object byte-range SHA256 mismatch rejection;
- malformed and cross-model existing authority rejection;
- pre-existing partial authority rejection;
- controlled failure at the real frozen Activation V1 os.replace boundary;
- byte-for-byte preservation of prior authority on failed replacement;
- frozen engine/protocol identity controls;
- no source GGUF operational dependency;
- no rollback, retirement, SQLite, mmap, inference, or MAF-native compute.

The runner also fails closed if its result, result partial, or runtime
already exists. Existing validation evidence will not be silently cleaned
or reused.

No runner execution has occurred at this checkpoint.

No Activation V1.1 raw validation result exists.

No Activation V1.1 validation runtime exists.

## Phase 6B.7 Validation V1.1.1 Corrective Protocol Checkpoint

The frozen Activation V1.1 validation result remains historical evidence:

    experiments/model_fractal/
    maf_activation_validation_v1_1.json

    commit:
        53bb864

    sha256:
        aff5b47e3ff6cbd611b2b29fa1ce826d
        fce1ece6fdc7356fb94ba9fefe41b548

Historical status remains:

    all_pass = false

Exactly one negative control recorded pass=false:

    multi_segment_wrong_content_association

Frozen evidence:

    raised        = true
    failed_closed = true
    error_type    = MAFActivationError
    error_text    = segment length mismatch

The frozen runner AST proves that this control required:

    expected_text = "segment SHA256 mismatch"

The frozen controlled fixture uses unequal 2048-byte and 3072-byte
segments.

Swapping their segment_id -> physical path association therefore correctly
violates segment length before SHA256 comparison.

Classification:

    Activation V1.1 engine defect:
        NOT INDICATED

    Validation-runner expectation defect:
        CONFIRMED

The validation-only correction is preregistered as:

    experiments/model_fractal/
    MAF_ACTIVATION_VALIDATION_V1_1_1_PROTOCOL.md

Historical Activation V1.1 engine, runner, raw result, and runtime remain
untouched.

## Phase 6B.7 Validation V1.1.1 Runner Freeze Checkpoint

The validation-only corrective protocol is frozen:

    experiments/model_fractal/
    MAF_ACTIVATION_VALIDATION_V1_1_1_PROTOCOL.md

    commit:
        0348d11

    sha256:
        98f4d3dcdbc079f00f097b70a28cab28
        41f32abd19b02e79b54a36fbcdf7a9fc

The corrected preregistered runner is:

    experiments/model_fractal/
    maf_activation_validation_v1_1_1.py

Runner SHA256:

    7d6d5c106cd8b438938a1d6d33bb55e9c107795f8da05207c210bd94ebdb42d2

The V1.1.1 runner is a narrow derivative of the frozen V1.1 runner.

Substantive validation-control inventory is preserved.

The confirmed correction is limited to the multi-segment wrong-content
association expectation and distinct V1.1.1 validation evidence identity.

The corrected control requires:

    error_type = MAFActivationError

and accepts only:

    segment length mismatch
    segment SHA256 mismatch

for the frozen unequal-length wrong-content substitution.

Historical V1.1 evidence remains unchanged:

    maf_activation_validation_v1_1.py
    maf_activation_validation_v1_1.json
    results/runtime/maf_activation_validation_v1_1

Historical V1.1 remains all_pass=false.

No V1.1 rerun occurred.

No V1.1.1 validation execution has occurred.

No V1.1.1 raw result or runtime exists.

## Phase 6B.7 Atomic Activation Completion Checkpoint

Phase 6B.7 is now complete.

Status:

    Phase 6B.7 — Atomic activation — COMPLETE

The final accepted validation evidence is:

    experiments/model_fractal/
    maf_activation_validation_v1_1_1.json

Frozen result commit:

    0d62257

Result SHA256:

    586f4a4958aab67972dc06845171ee79
    bfe937dfcd731f1f5b3fc594df841ac8

Frozen corrected validation runner:

    experiments/model_fractal/
    maf_activation_validation_v1_1_1.py

Runner SHA256:

    7d6d5c106cd8b438938a1d6d33bb55e
    9c107795f8da05207c210bd94ebdb42d2

Frozen validation correction protocol:

    experiments/model_fractal/
    MAF_ACTIVATION_VALIDATION_V1_1_1_PROTOCOL.md

Protocol SHA256:

    98f4d3dcdbc079f00f097b70a28cab28
    41f32abd19b02e79b54a36fbcdf7a9fc

Final V1.1.1 validation recorded:

    all_pass = true

Validated properties include:

- canonical candidate identity validation;
- current physical segment reconstruction before authority change;
- exact segment mapping requirements;
- physical segment length validation;
- physical segment SHA256 validation;
- object byte-range SHA256 validation;
- exact descriptor reconstruction;
- exact reconstructed generation_pk;
- canonical five-field active authority records;
- first activation;
- replacement activation;
- independent active-record reopen;
- idempotent same-generation activation;
- mandatory physical revalidation before idempotent success;
- path independence;
- multi-segment mapping order independence;
- wrong-content association rejection;
- synthetic canonical but physically unsupported manifest rejection;
- malformed and cross-model authority rejection;
- pre-existing partial rejection;
- injected pre-os.replace failure preservation;
- prior-authority byte preservation on failed replacement;
- partial cleanup after injected precommit failure.

The final suite contains 25 negative controls and all pass.

The corrected wrong-content control records:

    error_type    = MAFActivationError
    error_text    = segment length mismatch
    raised        = true
    failed_closed = true
    pass          = true

Historical Validation V1.1 remains preserved unchanged:

    experiments/model_fractal/
    maf_activation_validation_v1_1.json

Historical V1.1 result SHA256:

    aff5b47e3ff6cbd611b2b29fa1ce826d
    fce1ece6fdc7356fb94ba9fefe41b548

Historical V1.1 remains:

    all_pass = false

That failure remains valid historical evidence of the
overconstrained validation-runner expectation.

No historical runner was reexecuted.

Historical and corrected runtime evidence remain preserved separately:

    results/runtime/
    maf_activation_validation_v1_1

    results/runtime/
    maf_activation_validation_v1_1_1

Activation V1 remains frozen unchanged.

Activation V1.1 remains frozen unchanged.

Generation Engine V1 remains frozen unchanged.

No source GGUF is required by activation validation.

No rollback implementation exists.

No catalog/storage engine has been selected.

No inference was performed.

MAF-native compute was not enabled.

Phase 6B.7 therefore establishes the validated authority transition:

    logical PK
        ->
    validated current physical generation
        ->
    atomic active-generation authority record

within the explicitly frozen V1/V1.1 research scope.

## Phase 6B.8 Rollback V1 Protocol Checkpoint

Phase 6B.7 Atomic Activation remains COMPLETE.

Phase 6B.8 Rollback is now the current incomplete gate.

The Rollback V1 protocol is frozen as:

    experiments/model_fractal/
    MAF_ROLLBACK_V1_PROTOCOL.md

Rollback preserves the frozen five-field active authority record.

Rollback is defined as current physical validation and operational
reactivation of retained immutable generation evidence followed by the
existing atomic authority transition.

The currently active authority must strictly validate before rollback.

The retained target must physically reconstruct exactly before authority
mutation.

Any precommit failure must preserve current authority bytes exactly.

A same-generation rollback request must physically revalidate before
idempotent changed=false success.

The generation being left remains retained and immutable.

Phase 6B.7 did not create an authoritative append-only activation-history
journal. Rollback V1 therefore does not invent proof that arbitrary retained
generation evidence was historically authoritative.

No source GGUF is required.

No generation deletion is part of rollback.

No storage engine is selected.

No inference or MAF-native compute is enabled.

No rollback implementation or validation exists yet.

## Phase 6B.8 Rollback V1 Engine Freeze Checkpoint

The Rollback V1 protocol remains frozen:

    experiments/model_fractal/
    MAF_ROLLBACK_V1_PROTOCOL.md

Protocol commit:

    9f4a438

Protocol SHA256:

    0d71f4eb28ea35658d9c24a55d085e54
    b6cc6a5c92cda9dc2a17dfe57df07a42

The minimum Rollback V1 implementation is:

    experiments/model_fractal/
    maf_rollback_v1.py

Rollback engine SHA256:

    73b02c26f840d59499dd7be86985db6a3a14720769de1d040f2cad9c78703b79

The rollback engine intentionally owns no authority persistence mechanism.

Its operation is:

    strictly reopen current active authority
        ->
    enforce active model_pk equality
        ->
    delegate retained target physical validation
        ->
    delegate atomic authority transition

Target validation and same-generation physical revalidation remain owned by
frozen Activation V1.1.

Atomic active-record persistence remains owned by frozen Activation V1.

Rollback V1 remains operational reactivation of retained immutable
generation evidence. It does not create historical-authority provenance.

No source GGUF dependency exists.

No generation deletion or retirement is implemented.

No storage engine is selected.

No inference, residency, or MAF-native compute is implemented.

No rollback validation runner, result, or runtime exists yet.

Phase 6B.8 remains INCOMPLETE / CURRENT.

## Phase 6B.8 Rollback V1 Validation Runner Freeze Checkpoint

Rollback V1 protocol remains frozen:

    experiments/model_fractal/
    MAF_ROLLBACK_V1_PROTOCOL.md

Protocol SHA256:

    0d71f4eb28ea35658d9c24a55d085e54
    b6cc6a5c92cda9dc2a17dfe57df07a42

Rollback V1 implementation remains frozen:

    experiments/model_fractal/
    maf_rollback_v1.py

Rollback engine commit:

    fea6e01

Rollback engine SHA256:

    73b02c26f840d59499dd7be86985db6a
    3a14720769de1d040f2cad9c78703b79

The preregistered Rollback V1 validation runner is:

    experiments/model_fractal/
    maf_rollback_validation_v1.py

Runner SHA256:

    42fdb589b743197be672c47d3b70e40706c1ceea01d23f8862f489cfd5270b7d

The runner has not been executed.

No rollback result exists.

No rollback runtime exists.

The validation runner uses frozen Activation V1.1.1 evidence as read-only
retained generation evidence and copies byte-identical candidate evidence into
its own isolated runtime when executed.

The runner preregisters:

- A -> B operational rollback;
- B -> A operational reactivation;
- same-generation physical revalidation;
- changed=false idempotence;
- exact five-field authority;
- generation manifest hash binding;
- independent authority reopen;
- physical-path independence;
- strict current-authority validation;
- active model-scope enforcement;
- malformed/cross-model current-authority rejection;
- malformed target request and manifest rejection;
- missing/extra segment mappings;
- missing/nonregular target segments;
- segment length and SHA256 rejection;
- inherited frozen object-range integrity evidence;
- inherited frozen multi-segment wrong-content evidence;
- inherited physically unsupported-manifest evidence;
- invalid same-generation physical evidence rejection;
- injected failure before authority replacement;
- exact prior-authority byte preservation;
- precommit partial cleanup;
- retained generation immutability;
- no historical-authority provenance claim;
- no generation deletion;
- source-GGUF independence;
- storage neutrality;
- no inference;
- no MAF-native compute;
- no Phase 6B.9 implementation.

Phase 6B.8 remains INCOMPLETE / CURRENT.

## Phase 6B.8 Rollback Completion Checkpoint

Phase 6B.8 is now complete.

Status:

    Phase 6B.8 — Rollback — COMPLETE

Frozen Rollback V1 protocol:

    experiments/model_fractal/
    MAF_ROLLBACK_V1_PROTOCOL.md

Protocol commit:

    9f4a438

Protocol SHA256:

    0d71f4eb28ea35658d9c24a55d085e54
    b6cc6a5c92cda9dc2a17dfe57df07a42

Frozen Rollback V1 engine:

    experiments/model_fractal/
    maf_rollback_v1.py

Engine commit:

    fea6e01

Engine SHA256:

    73b02c26f840d59499dd7be86985db6a
    3a14720769de1d040f2cad9c78703b79

Frozen Rollback V1 validation runner:

    experiments/model_fractal/
    maf_rollback_validation_v1.py

Runner commit:

    e019732

Runner SHA256:

    42fdb589b743197be672c47d3b70e407
    06c1ceea01d23f8862f489cfd5270b7d

Frozen Rollback V1 raw validation result:

    experiments/model_fractal/
    maf_rollback_validation_v1.json

Result commit:

    6a898c3

Result SHA256:

    36698287b411b30d1616bc24455435022
    a0e13a9e9b35b16e68cdf32300c4a82

The frozen validation runner executed exactly once.

The raw result was frozen before semantic interpretation.

Final accepted result:

    all_pass = true

Validation establishes:

- valid operational rollback A -> B;
- later B -> A operational reactivation;
- strict validation of current authority before rollback;
- model-scoped rollback authority;
- exact retained-target generation identity;
- current physical target reconstruction before authority transition;
- exact target segment mapping;
- target segment length and SHA256 validation;
- target object byte-range SHA256 integrity;
- canonical five-field active authority records;
- exact generation_manifest_sha256 binding;
- independent active-authority reopen;
- target path independence;
- same-generation physical revalidation;
- same-generation changed=false idempotence;
- current-authority byte preservation on precommit failure;
- partial cleanup after injected precommit failure;
- retained generation immutability;
- source Activation V1.1.1 runtime preservation;
- rollback candidate-copy preservation;
- source-GGUF independence;
- storage/catalog neutrality;
- no generation deletion;
- no inference;
- no MAF-native compute;
- no resident PK directory implementation.

The final rollback suite contains 25 negative controls and all pass.

Twenty-two controls are executed directly by the Rollback V1 validation runner.

Three controls intentionally inherit already-frozen Activation V1.1.1 evidence:

- object_byte_range_sha256_mismatch;
- multi_segment_wrong_content_association;
- synthetic_canonical_without_physical_evidence.

The inherited wrong-content evidence is:

    mode                 = inherited_frozen_activation_v1_1_1
    pass                 = true
    source_error_type    = MAFActivationError
    source_error_text    = segment length mismatch
    source_failed_closed = true

The inherited-control projection contract was verified read-only against the
exact frozen Activation V1.1.1 result.

The earlier Phase 6B.8e and 6B.8e1 interpretation failures were
interpretation-audit expectation defects. They did not indicate a Rollback
V1 engine defect or Rollback V1 validation-runner defect.

No rollback validation rerun occurred.

No frozen rollback or activation result was rewritten.

Rollback runtime evidence remains preserved:

    results/runtime/
    maf_rollback_validation_v1

Activation runtime evidence remains preserved:

    results/runtime/
    maf_activation_validation_v1_1_1

Historical Activation V1.1 runtime evidence remains preserved:

    results/runtime/
    maf_activation_validation_v1_1

Rollback V1 remains operational reactivation of retained immutable generation
evidence.

It does not create or infer authoritative historical activation provenance.

Phase 6B.8 therefore establishes:

    current valid authority A
        +
    retained immutable target B
        +
    current physical validation of B
        ->
    atomic authority transition
        ->
    B authoritative
        +
    A retained unchanged

within the frozen Phase 6B.7 / 6B.8 research scope.

## Phase 6B.9 Resident PK Directory V1 Protocol Checkpoint

Phase 6B.8 Rollback remains COMPLETE.

Phase 6B.9 Resident PK Directory is the current incomplete gate.

The Resident PK Directory V1 protocol is frozen as:

    experiments/model_fractal/
    MAF_RESIDENT_PK_DIRECTORY_V1_PROTOCOL.md

The resident directory is derived in-memory state, not authority.

Authority remains:

    canonical active-generation record
        ->
    canonical immutable active generation descriptor

The minimum V1 resident key class is canonical object_pk.

Logical lookup scope is model-bound.

The minimum semantic lookup key is:

    (model_pk, "object_pk", object_pk)

The resident mapping preserves the active immutable descriptor evidence needed
for direct access:

    generation_pk
    generation_manifest_sha256
    segment_id
    offset
    length
    object_file_sha256

Physical segment path may be retained as runtime metadata but is not logical
identity.

Directory snapshots are generation-bound and immutable after publication.

Activation and rollback make the prior generation snapshot stale.

Current physical evidence must be validated before a replacement snapshot is
published.

A failed replacement build must preserve the prior valid snapshot unchanged.

A resident successful lookup must not require JSON parsing, manifest scanning,
filesystem discovery, or linear scanning over all descriptor objects.

Average O(1) keyed lookup is the implementation target, not yet a benchmarked
performance claim.

No source GGUF dependency is allowed.

No storage engine is selected.

No generation deletion is implemented.

No Segment Reader is implemented.

No inference or MAF-native compute is enabled.

No Phase 6C implementation has begun.

No Resident PK Directory implementation or validation exists yet.

## Phase 6B.9 Resident PK Directory V1 Engine Checkpoint

Phase 6B.8 Rollback remains COMPLETE.

Phase 6B.9 Resident PK Directory remains INCOMPLETE / CURRENT.

Frozen protocol:

    experiments/model_fractal/
    MAF_RESIDENT_PK_DIRECTORY_V1_PROTOCOL.md

Protocol SHA256:

    5d053b52963a10285f21a600aa0bb257
    b0ad645f12a9a36417cfa6f77a017939

Resident PK Directory V1 implementation is now frozen as:

    experiments/model_fractal/
    maf_resident_pk_directory_v1.py

Engine SHA256:

    4dadac5a1ffe448437718432edeee14a
    219a20da5a54956d2884d0b0b1d426b6

The implementation remains derived process-local state rather than authority.

Current authority remains the frozen five-field active-generation record.

Current immutable logical mapping remains the frozen active generation descriptor.

Snapshot construction:

- strictly reopens current active authority;
- rejects cross-model authority;
- binds candidate manifest bytes to generation_manifest_sha256;
- reuses frozen Activation V1.1 physical candidate validation;
- reuses frozen Activation V1.1 segment-path mapping;
- validates the complete snapshot before publication;
- verifies active authority did not change during build;
- verifies candidate manifest did not change during build.

Resident PK Directory V1 minimum key class is:

    object_pk

The logical resident key remains:

    (model_pk, "object_pk", object_pk)

Each resident object entry preserves:

    model_pk
    generation_pk
    generation_manifest_sha256
    object_pk
    segment_id
    offset
    length
    object_file_sha256
    payload_sha256
    segment_length
    segment_sha256

Physical segment path is retained only as runtime metadata.

Resident entries and snapshots are frozen dataclasses.

The published entry mapping uses immutable MappingProxyType state.

A successful resident lookup:

- is model scoped;
- requires expected_generation_pk;
- rejects stale generation expectation;
- rejects unsupported PK classes;
- rejects missing logical PK explicitly;
- uses direct resident mapping access;
- performs no JSON parsing;
- performs no filesystem read;
- performs no manifest scan;
- performs no linear descriptor scan.

ResidentPKDirectory.refresh() builds a complete replacement snapshot before
one publication assignment.

Therefore a failed replacement build preserves the prior published snapshot.

No active-authority writer was added.

No rollback writer was added.

No source GGUF dependency was added.

No generation deletion was added.

No storage engine was selected.

No Segment Reader was implemented.

No inference or MAF-native compute was implemented.

No directory validation runner, result, or runtime exists yet.

No benchmark has been executed.

## Phase 6B.9 Resident PK Directory Validation V1 Runner Checkpoint

Phase 6B.8 Rollback remains COMPLETE.

Phase 6B.9 Resident PK Directory remains INCOMPLETE / CURRENT.

Frozen Resident PK Directory V1 protocol:

    experiments/model_fractal/
    MAF_RESIDENT_PK_DIRECTORY_V1_PROTOCOL.md

Protocol SHA256:

    5d053b52963a10285f21a600aa0bb257
    b0ad645f12a9a36417cfa6f77a017939

Frozen Resident PK Directory V1 engine:

    experiments/model_fractal/
    maf_resident_pk_directory_v1.py

Engine SHA256:

    4dadac5a1ffe448437718432edeee14a2
    19a20da5a54956d2884d0b0b1d426b6

Resident PK Directory Validation V1 runner is now frozen as:

    experiments/model_fractal/
    maf_resident_pk_directory_validation_v1.py

Runner SHA256:

    8dcf90a3a076cc84ff290b3d44435340
    44b735d5d2cd3767014a34dc12473257

The validation runner has not been executed.

The validation result remains absent.

The validation runtime remains absent.

The runner preregisters exactly 22 unique negative controls.

The exact preregistered control inventory is preserved.

Control call-site ordering is not validation semantics.

The earlier corrected-freeze attempt imposed an arbitrary AST traversal/source
ordering on those controls and therefore stopped safely before staging or
commit.

That failure is classified as:

    STATIC_AUDIT_CONTROL_ORDER_DEFECT

It does not indicate a validation-runner defect.

No validation-runner rewrite was required.

The earlier source-GGUF freeze failure is also preserved as:

    STATIC_AUDIT_FALSE_POSITIVE

The runner's ".gguf" literal is only a sentinel that verifies the frozen
Resident PK Directory engine source contains no source-GGUF dependency.

The runner contains no GGUF, llama, or ggml import or executable call and no
source-model GGUF path.

Its exact-once guard refuses execution when either the raw result or validation
runtime already exists.

No benchmark has been executed.


## Phase 6B.9 Documentation Checkpoint

Phase 6B documentation has been synchronized before first Resident PK Directory validation execution.

Updated surfaces include:

- root README;
- Phase 6B roadmap status;
- documentation index;
- architecture and authority documentation;
- MAF research documentation;
- development best practices;
- glossary;
- Labs guidance;
- AI collaborator guidance;
- Phase 6B walkthrough / tutorial.

The documentation now distinguishes validated behavior, frozen implementation awaiting validation, benchmark targets, and future work.

Atomic Activation and Rollback are documented as complete and validated.

Resident PK Directory V1 protocol, engine, and validation runner remain frozen.

The Resident PK Directory validation runner has still not been executed.

No Resident PK Directory validation result or runtime exists yet.

Average O(1) resident lookup remains a target until benchmark evidence is frozen.

No Segment Reader implementation, production storage-engine selection, MAF-native compute, inference replacement, or Phase 6C implementation is claimed.


## Phase 6B.9 Resident PK Directory Validation Raw-Result Checkpoint

The already-frozen Resident PK Directory Validation V1 runner has now been executed exactly once.

Runner SHA256:

    8dcf90a3a076cc84ff290b3d4443534044b735d5d2cd3767014a34dc12473257

Raw validation result:

    experiments/model_fractal/maf_resident_pk_directory_validation_v1.json

Raw result SHA256:

    24540c16eac53e9a179781c7007d61d98b34f7bc74e1f3dfc462b5786dd186b1

Runner return code: 0

Raw all_pass field: True

Raw negative controls passed: 22 / 22

Raw benchmark_performed field: False

These values are recorded as raw evidence only.

The result has not yet been semantically interpreted or accepted.

The validation runner must not be rerun.

The validation runtime is preserved and must not be cleaned.

No benchmark was performed in this raw-freeze gate.

No Segment Reader implementation was added.

No production storage engine was selected.

Phase 6C has not started.


## Phase 6B.9 Functional Interpretation and Benchmark Preregistration Checkpoint

Resident PK Directory V1 functional validation is semantically ACCEPTED.

Frozen functional validation result SHA256:

    24540c16eac53e9a179781c7007d61d98b34f7bc74e1f3dfc462b5786dd186b1

Functional interpretation established:

- all top-level contract bindings passed;
- all 37 positive boolean checks passed;
- all 11 static policy checks passed;
- all 22 preregistered negative controls passed;
- activation refresh behavior passed;
- rollback refresh behavior passed;
- stale snapshot rejection passed;
- failed refresh prior-snapshot preservation passed;
- physical relocation semantics passed;
- source Activation runtime remained unchanged.

The functional validation runner must not be rerun.

Phase 6B.9 remains incomplete because dedicated performance evidence is still required.

Resident PK Directory Performance Benchmark V1 protocol is frozen as:

    experiments/model_fractal/MAF_RESIDENT_PK_DIRECTORY_BENCHMARK_V1_PROTOCOL.md

Benchmark protocol SHA256:

    496a19e5f2f2a9cebbb74aaf204b96e28916c0aa0276fb85dfb8401e55e2266f

Benchmark runner is frozen as:

    experiments/model_fractal/benchmark_maf_resident_pk_directory_v1.py

Benchmark runner SHA256:

    536d5a360bf7d450eb6a882581cd3c202cc81d66323d7b9e871bd15353f1c27d

The benchmark has not been executed.

Its raw result and runtime remain absent.

The benchmark preregisters direct lookup latency distributions, scaling, linear comparison, actual build and refresh cost, and memory scaling.

Average O(1) resident lookup remains a target until the benchmark result is frozen and interpreted.

No production latency guarantee is preregistered.


## Phase 6B.9 Benchmark V1 Failure and V1.1 Correction Checkpoint

Resident PK Directory Benchmark V1 was executed exactly once and failed before performance measurement or raw-result publication.

Failed V1 benchmark runner SHA256:

    536d5a360bf7d450eb6a882581cd3c202cc81d66323d7b9e871bd15353f1c27d

Failed V1 runtime remains preserved at:

    results/runtime/maf_resident_pk_directory_benchmark_v1

V1 must not be rerun.

Root cause is confirmed as a Benchmark V1 input-contract defect.

Activation requires:

    dict[segment_id -> path-like]

V1 incorrectly supplied a list of paths.

The frozen Activation source proves the value flow:

    value = segment_paths[segment_id]
    path = Path(value)
    mapped[segment_id] = path

No Resident PK Directory engine defect is indicated.

No Activation defect is indicated.

No functional-validation defect is indicated.

No performance measurement was reached in V1.

The g6 VALUE_FLOW_NOT_FULLY_PROVEN classification was a static-audit false negative caused by inspecting only top-level function-body assignments; the extracted nested source body itself proves the contract.

Benchmark V1.1 correction protocol:

    experiments/model_fractal/MAF_RESIDENT_PK_DIRECTORY_BENCHMARK_V1_1_CORRECTION_PROTOCOL.md

Correction protocol SHA256:

    d35aca6c8c98d891761f6fbfb176e3b7fc385d466d03e07ae3125892015b61ef

Corrected benchmark runner:

    experiments/model_fractal/benchmark_maf_resident_pk_directory_v1_1.py

Corrected runner SHA256:

    f9b8d1560eab35ce9340e00cfd7cb2b3683765fbf5b085544ee7f21d8f97a28e

The V1.1 correction changes only the segment-path adapter plus distinct V1.1 lineage/result/runtime identities and correction-protocol binding.

Benchmark sizes, repetitions, warmups, measurement logic, memory logic, actual build/refresh measurement, and all acceptance thresholds remain unchanged.

V1.1 has not been executed.

V1.1 result and runtime remain absent.


## Phase 6B.9 Benchmark V1.1 Raw-Result Checkpoint

The frozen corrected Resident PK Directory Benchmark V1.1 has now been executed exactly once.

Benchmark V1 remains failed historical evidence and was not rerun.

Benchmark V1.1 correction protocol SHA256:

    d35aca6c8c98d891761f6fbfb176e3b7fc385d466d03e07ae3125892015b61ef

Benchmark V1.1 runner SHA256:

    f9b8d1560eab35ce9340e00cfd7cb2b3683765fbf5b085544ee7f21d8f97a28e

Raw V1.1 result:

    experiments/model_fractal/benchmark_maf_resident_pk_directory_v1_1.json

Raw V1.1 result SHA256:

    57562c9fbcac012c6706903ff07c23a15b5bf59bb0599a9f6dd04ceecbec95b1

V1.1 return code: 0

Raw all_pass field: True

Raw acceptance.pass field: True

Raw direct median scaling ratio: 1.0

Raw direct p95 scaling ratio: 1.3984674329501916

Raw linear median growth ratio 100000 vs 1000: 100.35176445350208

Raw build median ns: 242864

Raw build p95 ns: 274531

Raw refresh median ns: 237422

Raw refresh p95 ns: 250416

Raw 100000-entry direct median ns: 260

Raw 100000-entry linear median ns: 3742318

These values are frozen raw evidence only.

Semantic benchmark acceptance has not yet been decided.

Benchmark V1.1 must not be rerun.

Both failed V1 runtime and V1.1 runtime must be preserved.

Functional validation must not be rerun.

No cleanup was performed.

No Segment Reader implementation was added.

No production storage engine was selected.

Phase 6C has not started.


## Phase 6B.9 Post-Validation Diagnostic Preregistration

Resident PK Directory functional evidence is semantically accepted.

Resident PK Directory Benchmark V1.1 performance evidence is semantically accepted.

Accepted Benchmark V1.1 result SHA256: 57562c9fbcac012c6706903ff07c23a15b5bf59bb0599a9f6dd04ceecbec95b1

Observed accepted performance evidence includes:

    direct median scaling ratio: 1.0
    direct p95 scaling ratio: 1.3984674329501916
    linear 100K/1K median growth: 100.35176445350208
    100K direct median: 260 ns
    100K linear median: 3742318 ns
    device-local 100K ratio: approximately 14393.53x

The O(1)-style claim remains limited to observed scaling over the tested range.

No production performance guarantee is claimed.

Before Phase 6B.10, a dedicated post-validation diagnostic suite is now frozen.

Diagnostic protocol: experiments/model_fractal/MAF_RESIDENT_PK_DIRECTORY_DIAGNOSTICS_V1_PROTOCOL.md

Diagnostic protocol SHA256: 5101e4a4dd78b869eb91ce226a1a304181bc2c3636d2ff86a056db15caf0560a

Diagnostic runner: experiments/model_fractal/diagnose_maf_resident_pk_directory_v1.py

Diagnostic runner SHA256: 88452ca6d8fa0d70c4a9982630b1170fb5034e12871a501ead90f68676e2c8aa

The suite preregisters logic/invariant, failed-refresh preservation, hot-path filesystem-I/O, tracemalloc retention, live snapshot retention, RSS, file-descriptor, runtime-file accumulation, and sustained lookup/refresh degradation checks.

Diagnostic execution has not occurred.

Diagnostic result and runtime remain absent.

Both benchmark runtimes remain preserved.

Benchmark and functional runners must not be rerun.


## Phase 6B.9 Diagnostics V1.1 Frozen Correction Checkpoint

Diagnostics V1 remains frozen historical preregistration evidence and was never executed.

Diagnostics V1 protocol SHA256: 5101e4a4dd78b869eb91ce226a1a304181bc2c3636d2ff86a056db15caf0560a

Diagnostics V1 runner SHA256: 88452ca6d8fa0d70c4a9982630b1170fb5034e12871a501ead90f68676e2c8aa

Diagnostics V1 execution is forbidden because static preflight identified repeated inspect.signature lookup-measurement contamination.

No Diagnostics V1 result or runtime exists.

The existing Diagnostics V1.1 correction drafts were independently audited before adoption.

Static preflight result:

    STATIC_ACCEPTANCE=PASS
    FAILED_COUNT=0
    CLASSIFICATION=EXISTING_V1_1_DRAFTS_STATICALLY_ACCEPTABLE

Diagnostics V1.1 correction protocol SHA256:

    9f01c39fe8777c6f93eae550d16596af625d3cb86d07993e500c0479648b35ab

Diagnostics V1.1 runner SHA256:

    12e70402b018488940c710e4b24a76966d150c91ac113fb89d23656e01e812c2

The correction resolves lookup signature and keyword binding once during setup and reuses the prepared bound lookup operation.

No diagnostic workload, threshold, leak limit, resource limit, failure-path test, or degradation threshold was relaxed.

Diagnostics V1.1 has not been executed.

Diagnostics V1.1 result and runtime remain absent.

A final independent frozen-state fatal/logic/resource preflight is required before exact-once execution.


## Phase 6B.9 Diagnostics V1.2 Coverage Correction

Diagnostics V1 and V1.1 remain frozen and were never executed.

The V1.1 final preflight produced two findings.

The reported unsupported `self` lookup parameter was a preflight-helper false positive caused by inspecting the unbound class method. The runner uses the bound snapshot.lookup method, so no runner correction was required for that finding.

A real diagnostic coverage defect was confirmed: rebuild and intentionally failed-refresh stress occurred before memory/resource baselines, preventing path-specific leak/resource detection.

Diagnostics V1.2 adds isolated tracemalloc, live-snapshot, RSS, file-descriptor, runtime-file-count, and runtime-byte measurements around both the existing 200-build and 200-failed-refresh stress blocks.

V1.2 also adds a post-setup write-intent filesystem-open audit.

All existing V1.1 workloads and thresholds remain unchanged.

Diagnostics V1.2 correction protocol SHA256: fbaaeb38346d5173637f31579e72e880a807dfea31d7d92434fc9af040cf23a8

Diagnostics V1.2 runner SHA256: 9cfca287a6edff317a27ed650f8984057175f1028a6f596a8073892bc5a5fde6

Diagnostics V1.2 has not been executed.

Its result and runtime remain absent.

A final frozen-state preflight is required before execution.


## Phase 6B.9 Diagnostics V1.3 Frozen Coverage Checkpoint

Diagnostics V1.3 recovered draft bytes passed an independent exact-content static audit before adoption.

Audit classification:

    EXISTING_V1_3_DRAFTS_STATICALLY_ACCEPTABLE

Audit failed checks:

    0

Bound lookup unsupported required parameters:

    NONE

Tracemalloc lifecycle:

    starts = 4
    stops  = 4

Diagnostics V1.3 correction protocol SHA256:

    e6e3a0d3995550106c9abf8a60c586b01083fb6e971573df26f3552c06292ff6

Diagnostics V1.3 runner SHA256:

    972fa763ea233f791add465ca73c3743d8e4d68d092edd7b874288562e8aea35

V1.3 adds the remaining requested diagnostic coverage:

- sustained real build-path degradation;
- repeated hash/file-validation degradation through that real build path;
- repeated stale-generation rejection with projection and resource preservation checks.

All prior V1.2 diagnostic coverage and limits remain preserved.

Diagnostics V1.3 has not been executed.

Its raw result and runtime remain absent.

One final independent frozen-state preflight is required before any exact-once execution.


## Phase 6B.9 Diagnostics V1.4 Exact Stale-Exception Correction

Diagnostics V1.3 remained unexecuted after final frozen-state preflight.

The preflight resolved the engine-defined stale-generation rejection exception as:

    MAFResidentPKDirectoryStaleSnapshotError

V1.3 required a stable exception type but did not require that type to equal the engine-defined stale-snapshot exception.

Diagnostics V1.4 corrects only that acceptance defect.

All 200 stale-generation attempts must still reject.

The observed exception-type set must now equal exactly:

    {MAFResidentPKDirectoryStaleSnapshotError}

All V1.3 workloads, thresholds, resource checks, build/hash degradation checks, stale-state preservation checks, and exact-once semantics remain unchanged.

Diagnostics V1.4 correction protocol SHA256: dbb86b4ef1c9cb01efeda00893b8710562895bd347145540335bb20303c1d337

Diagnostics V1.4 runner SHA256: 1d01720bd0bd88bcfcc522af70876e134d12d3b9763fd56cc23975f9f7d5c694

Diagnostics V1.4 has not been executed.

Its result and runtime remain absent.

A final frozen-state preflight is required before exact-once execution.


## Phase 6B.9 Resident PK Directory — COMPLETE

Phase 6B.9 has passed semantic acceptance and is now closed.

Completion evidence is frozen in:

    experiments/model_fractal/MAF_RESIDENT_PK_DIRECTORY_V1_COMPLETION.md

Completion record SHA256:

    6fffb5c5f6c616b9930a65a7297eb4f290e953e04785e72591b5033735ff1f01

Frozen Diagnostics V1.4 result:

    9f665383917560327b05673206a8b385d9312386077bbb741878d49866ce29b0

Diagnostics V1.4 executed exactly once with RC 0 and 45 / 45 checks passing.

No diagnostic, benchmark, or functional-validation rerun is authorized.

Preserved runtimes must not be cleaned.


## Phase 6B.10 Segment Reader V1 — Protocol Frozen

Physical-contract discovery resolved the object/payload boundary before implementation.

The generation descriptor offset and length identify serialized object-file bytes inside the immutable segment.

For the preserved discovery sample:

- segment_id: segment:00000000
- object_pk: mafobj:v1:ea258c628d783a1e140430a6bbde438f97f0be7d85e5f218ee149ad3b1fb2815
- offset: 64
- length: 512
- physical range SHA256 equals object_file_sha256
- physical range SHA256 does not equal payload_sha256
- object_file_sha256 and payload_sha256 are distinct

Segment Reader V1 therefore reads and verifies the serialized object range using object_file_sha256.

It does not decode or verify the underlying payload layer.

Frozen Segment Reader V1 protocol:

    experiments/model_fractal/MAF_SEGMENT_READER_V1_PROTOCOL.md

Protocol SHA256:

    192402f1e4f2d41540d225cce7629757152b9996a9adffaafeab6674e13f0f5d

Segment Reader implementation has not started.

Validation has not been preregistered or executed.

## Current Exact Next Task

Phase 6B.10 — Segment Reader V1 preimplementation audit.

Next action:

    Perform a final read-only audit of the frozen Segment Reader V1 protocol, then implement the minimal stateless positional serialized-object reader in a separate gate.

Do not modify completed Phase 6B.9 evidence.

Do not rerun Resident PK Directory validation, benchmark, or diagnostics.

Do not decode payload_sha256 semantics inside Segment Reader V1.

Do not implement FD residency, mmap residency, descriptor caching, tensor reconstruction, or Phase 6C.

Do not push upstream in this gate.
