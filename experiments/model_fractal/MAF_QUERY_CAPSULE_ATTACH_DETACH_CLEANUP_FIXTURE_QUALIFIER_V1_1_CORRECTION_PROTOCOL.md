# Q3 Fixture Qualifier V1.1 Portability Correction Protocol

Status: PREREGISTRATION — CORRECTION NOT IMPLEMENTED OR EXECUTED

Phase: **6D-Q3 — non-scientific fixture qualification recovery**

## 1. Purpose

This protocol prospectively corrects only the publication-portability defect observed in the frozen non-scientific Q3 fixture qualifier V1.

It does not alter the frozen Q3 scientific protocol, V01-V48 acceptance checks, claim boundary, or exact-once scientific namespace.

## 2. Frozen Q3 scientific protocol

- SHA256 `323c0d4e0cbd5327382e3762e4d9529fba48f3748699861d96b31920db5b0363`

## 3. Frozen failed V1 qualifier

- path `experiments/model_fractal/maf_query_capsule_attach_detach_cleanup_validation_v1_fixture.py`
- SHA256 `d62beb00c44deea17420d191a512050460c5c6460202d96f7d9cd5a048c516c6`
- freeze commit `7f7da85c8745eeb52644ab1a0c2d4ed40daaff63`

V1 is immutable failure provenance and must not be modified or executed again.

V1 completed upstream verification, physical-generation verification, active-record publication and reopen, and resident-directory qualification.

It then failed during fixture-authority publication because target Termux Python 3.13.13 does not expose `os.link`.

Observed failing operation: `os.link(AUTHORITY_PARTIAL, AUTHORITY)`.

Observed exception class: `AttributeError`.

This is a non-scientific portability failure and is not a Q3 scientific PASS or FAIL.

## 4. Frozen recovery active record

- path `results/runtime/maf_query_capsule_attach_detach_cleanup_validation_v1_fixture/active_generation.json`
- SHA256 `ffcf8ada4e2959432e18650a9503bb52175b4366f85ca663d206dea94da3f4e0`
- schema `openmind.maf_active_generation.v1`
- model PK `mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258`
- generation PK `mafgen:v1:45a80a2aa271ce04853003185b6a1227cb309bd1e3e2dc538eea849fac9f5db0`
- generation manifest SHA256 `28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3`

V1.1 must require this exact existing active record and SHA.

V1.1 must not recreate, replace, rewrite, delete, or repair the active record.

## 5. V1.1 implementation namespace

`experiments/model_fractal/maf_query_capsule_attach_detach_cleanup_validation_v1_1_fixture.py`

V1.1 must bind this correction protocol after freeze, the frozen Q3 protocol, the failed V1 SHA, the recovery active-record SHA, and all frozen upstream authorities required by Q3.

## 6. Required prequalification

Before any fixture-authority write V1.1 must:

1. verify the frozen Q3 protocol;
2. verify this frozen correction protocol;
3. verify the failed V1 implementation SHA;
4. verify all frozen Q1, Q2, Phase 6C, selector, catalog, query, and source-generation authorities required by Q3;
5. require the preserved active record and exact SHA;
6. reopen and verify its five-field active-record schema;
7. verify exact model, generation, and manifest bindings;
8. verify tracked and physical generation manifests are byte-identical;
9. verify the physical segment SHA and byte length;
10. independently build the resident PK directory using the preserved active record;
11. resolve exactly the 12 frozen catalog object PKs;
12. require both final and partial fixture-authority paths to be absent.

Any prequalification failure must publish nothing.

## 7. Corrected publication primitive

Python `os.link` is forbidden.

V1.1 must use `ctypes.CDLL(None, use_errno=True)` and libc `renameat2`.

- `AT_FDCWD = -100`
- `RENAME_NOREPLACE = 1`

Required publication order:

`PREQUAL -> PARTIAL_CREATE_EXCLUSIVE -> PARTIAL_WRITE -> PARTIAL_FSYNC -> RENAMEAT2_NOREPLACE -> PARENT_DIR_FSYNC -> FINAL_BYTE_VERIFY`

Partial and final paths must be on the same filesystem and in the same directory.

The final authority must never be overwritten.

If `renameat2` reports `EEXIST`, V1.1 must fail closed.

Any other nonzero return must raise an OS error using captured errno.

## 8. Fixture-authority requirements

Final pathname:

`experiments/model_fractal/maf_query_capsule_attach_detach_cleanup_validation_v1_fixture_authority.json`

The authority must be canonical deterministic JSON and bind:

- frozen Q3 protocol SHA;
- frozen V1.1 correction protocol SHA;
- V1.1 qualifier SHA;
- failed V1 qualifier SHA;
- recovery active-record SHA;
- exact model, generation, and manifest identities;
- physical segment SHA and byte length;
- catalog, query fixture, and selection-config authorities;
- all frozen upstream authority hashes;
- exactly 12 resolved object PKs;
- explicit non-scientific boundary flags.

No execution-history-dependent value may affect frozen authority bytes.

## 9. Preservation requirements

V1.1 must leave byte-identical:

- failed V1 qualifier;
- preserved recovery active record;
- frozen Q3 scientific protocol;
- Q2 slot, result, and verdict;
- source generation manifest;
- physical segment;
- catalog;
- query fixture.

## 10. Scientific boundary

V1.1 is non-scientific fixture qualification only.

It must not create or execute the Q3 scientific runner, slot, partial result, or final result.

It must not invoke Q2 V1.4 validation, invoke the selector, use Query Route Cache, perform bounded expansion, perform inference, or generate answers.

Q4 and Phase 6E remain not entered.

## 11. Acceptance contract

V1.1 is accepted only if:

1. all prequalification passes;
2. preserved active-record SHA remains exact;
3. all 12 catalog object PKs resolve;
4. authority publication succeeds with `renameat2(RENAME_NOREPLACE)`;
5. no partial authority remains;
6. final authority bytes are canonical and SHA-stable;
7. failed V1 and all frozen upstream evidence remain unchanged;
8. Q3 scientific namespace remains untouched.

## 12. Required development order

1. Freeze this correction protocol.
2. Implement V1.1 without modifying V1.
3. Static-audit V1.1.
4. Freeze V1.1 implementation.
5. Execute V1.1 once.
6. Independently audit the preserved active record and new fixture authority.
7. Freeze fixture evidence.
8. Only then implement the Q3 V01-V48 scientific runner.
