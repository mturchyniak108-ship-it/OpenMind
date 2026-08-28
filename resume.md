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

## Current Exact Next Task

Phase 6B.7 remains the current incomplete gate.

Next action:

    Preregister and freeze the Activation V1 validation runner against
    the frozen implementation.

The validation runner must cover all protocol-required positive and
negative controls, including the real os.replace failure boundary.

Do not execute activation validation before the runner is frozen.

Do not begin rollback, resident-directory work, storage-engine
selection, or Phase 6C.
