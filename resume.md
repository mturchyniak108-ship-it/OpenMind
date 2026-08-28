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
        CURRENT INCOMPLETE GATE

    6B.6 Activation protocol
        NOT STARTED

    6B.7 Atomic activation
        NOT STARTED

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

## V1.1 Runner Freeze Checkpoint

The V1.1 corrective-validation runner is now included in the current
targeted freeze:

    experiments/model_fractal/
    maf_generation_engine_validation_v1_1.py

The V1 behavioral validation body is preserved.

The corrective delta is limited to:

- V1.1-specific runtime/result/schema naming;
- V1.1 console/failure labeling;
- the corrected AST-based runner source-GGUF static-policy check.

No V1.1 validation has been executed at this checkpoint.

No V1.1 raw result exists at this checkpoint.

Current exact next task:

    Perform a pre-execution frozen-runner audit, then execute the
    frozen V1.1 runner exactly once.

After execution, freeze the raw V1.1 result before interpreting it.
