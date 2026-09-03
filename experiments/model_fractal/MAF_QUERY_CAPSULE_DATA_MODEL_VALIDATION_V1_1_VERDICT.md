# MAF Query Capsule Data Model Validation V1.1 Verdict

## Status

**SCIENTIFIC ACCEPTANCE — PASS**

Phase:

**6D-Q1 — Query Capsule Data Model V1**

Phase disposition:

**ACCEPTED / CLOSED**

Validation namespace:

**V1.1**

## Frozen authorities

### Data-model protocol

`experiments/model_fractal/MAF_QUERY_CAPSULE_DATA_MODEL_V1_PROTOCOL.md`

SHA256:

`5255a58c8c6340c251e24ae8543760fcd66a8deb8be1a8356ad5b78ad898edda`

### Frozen implementation

`experiments/model_fractal/maf_query_capsule_data_model_v1.py`

SHA256:

`f897b97011714f3c84b7350c6bb53e800232be8a5d34e5148a3e50a81952976e`

### Rejected predecessor V1 verdict

`experiments/model_fractal/MAF_QUERY_CAPSULE_DATA_MODEL_VALIDATION_V1_VERDICT.md`

SHA256:

`d78a2695d943d481badb5359d666133190a130d05e5acb8d69d9082be7cbf410`

### V1.1 validation protocol

`experiments/model_fractal/MAF_QUERY_CAPSULE_DATA_MODEL_VALIDATION_V1_1_PROTOCOL.md`

SHA256:

`63b40e4ec91410ebea43b85b032a57ed42ba181942390c41fd603a7e5c5cfd3d`

Protocol freeze commit:

`1edaee183013e5d39002ec182553758fb8bd3b47`

### V1.1 validation runner

`experiments/model_fractal/maf_query_capsule_data_model_validation_v1_1.py`

SHA256:

`f367226f8ad130830dac3ac83dec6620487affa3f54b7f3540d390b68711d5c7`

Runner freeze commit:

`d22ef4ab13b8c3ea573344bd40ac26e90664f584`

### Authoritative V1.1 result

`experiments/model_fractal/maf_query_capsule_data_model_validation_v1_1.json`

SHA256:

`24d1605d1ad95f1b7e7bee190fd0cc978d7b2597d095ac06f68c350208ef1774`

Result freeze commit:

`25c179ff2804e2893d02146e21f76d0b8a68f7d1`

## Pre-scientific qualification

Before the V1.1 exact-once scientific run, the frozen runner passed all
required non-spending gates.

These included:

- source-level runner audit;
- exact V01-V36 matrix equivalence to frozen V1;
- guard-false behavior;
- synthetic fixture qualification;
- dual-arm refusal for environment-only arming;
- dual-arm refusal for CLI-only arming;
- real Android/Termux publication-backend qualification;
- successful libc renameat2 availability and ABI binding;
- successful RENAME_NOREPLACE publication;
- successful parent-directory fsync;
- inode preservation;
- deterministic collision rejection;
- preservation of incumbent final bytes on collision;
- preservation of unpublished partial bytes on collision;
- final exact-once source and namespace readiness.

All non-spending gates preserved the V1.1 result namespace.

## Authoritative execution

The V1.1 scientific execution was performed once under the preregistered
dual-arm mechanism.

The exact-once result slot was reserved.

The complete scientific matrix executed exactly once.

The authoritative result reports:

- expected check count: **36**
- executed check count: **36**
- ordered IDs: **V01-V36**
- failed checks: **NONE**
- auditor error: **NONE**
- all_pass: **true**

Therefore:

**V01-V36: PASS 36/36**

## Publication

The authoritative result was published successfully using:

`libc.renameat2(RENAME_NOREPLACE)`

The preregistered no-clobber publication contract succeeded.

The final result exists at the frozen V1.1 result pathname.

The V1.1 partial pathname is absent after successful publication.

The frozen authoritative result is canonical JSON and SHA-stable.

## Scientific boundary

The authoritative result records that the validation did not execute:

- inference;
- a real model;
- route-cache persistence;
- Phase 6D-Q2;
- Phase 6E;
- performance benchmarking;
- network access;
- subprocess launch.

Accordingly, this verdict establishes only the Phase 6D-Q1 data-model
contract that was preregistered.

It does not establish query-to-PK selection correctness, selective inference
sufficiency, bounded expansion, object/tensor avoidance, output parity,
performance improvement, or MAF-native computation.

## V1 predecessor disposition

Validation V1 remains permanently rejected as a completed validation because
its publication harness failed after exact-once reservation.

Its frozen 36/36 partial evidence remains preserved.

Validation V1 MUST NOT be rerun.

Its missing final result MUST NOT be reconstructed or promoted post hoc.

## V1.1 exact-once disposition

Validation V1.1 completed successfully and its result slot is permanently
spent.

Validation V1.1 MUST NOT be rerun.

The V1.1 runner and authoritative result are frozen authorities.

## Formal scientific verdict

**PHASE 6D-Q1: SCIENTIFIC ACCEPTANCE — PASS**

The frozen Query Capsule Data Model V1 implementation satisfies the
preregistered V01-V36 representation/data-model validation contract.

**PHASE 6D-Q1 IS ACCEPTED AND CLOSED.**

## Phase progression

With Phase 6D-Q1 closed:

**PHASE 6D-Q2 IS UNBLOCKED.**

The next research gate is:

**6D-Q2 — NON-ORACLE QUERY-TO-PK SELECTION FEASIBILITY**

6D-Q2 may construct and validate bounded non-oracle query-to-PK selection.

6D-Q2 does not yet establish selective inference sufficiency.

Phase 6E-A remains blocked until Phase 6D-Q1, 6D-Q2, 6D-Q3, and 6D-Q4
are all closed.

Bounded expansion remains Phase 6E-B.

Actual object/tensor avoidance remains Phase 6E-C.

Output parity and quality remain Phase 6E-D.

MAF-native computation remains disabled and unvalidated.

Performance evaluation remains Phase 6F.

## Next gate

**PREREGISTER PHASE 6D-Q2 NON-ORACLE QUERY-TO-PK SELECTION PROTOCOL**
