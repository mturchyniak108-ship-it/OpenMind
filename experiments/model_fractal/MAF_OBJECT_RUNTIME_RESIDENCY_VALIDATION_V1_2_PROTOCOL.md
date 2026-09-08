# MAF Object Runtime Residency Validation V1.2 Protocol

Status: PROSPECTIVE PREREGISTRATION
Phase: 6C
Artifact class: scientific validation protocol
Validation status: NOT YET EXECUTED
Engine verdict: NONE

## 1. Purpose

This protocol preregisters the first scientifically valid successor attempt
to validate the frozen MAF Object Runtime Residency V1 engine after V1 and
V1.1 each spent their exact-once validation slots.

V1.2 changes the authority fixture and versioned provenance only.

The scientific V01-V32 matrix remains unchanged from frozen V1.1.

No runtime-engine implementation change is authorized by this protocol.

## 2. Frozen repository parent

Branch:

`labs/multidimensional-maf`

Parent:

`a4c205baff2b6536b01c1a7f082c786d47d56b48`

## 3. Historical lineage

Frozen V1.1 validation protocol:

`experiments/model_fractal/MAF_OBJECT_RUNTIME_RESIDENCY_VALIDATION_V1_1_PROTOCOL.md`

SHA256:

`e93ea0f418fc25a01573aad6d23b8d3f999be73b932828596b47ed6548128681`

Frozen V1.1 validation runner:

`experiments/model_fractal/maf_object_runtime_residency_validation_v1_1.py`

SHA256:

`87fc8a01cde4f90afd4b45cb799c2a9c52573db410e365ac620f30092803c029`

V1 and V1.1 validation exact-once slots are permanently spent and must never
be rerun.

V1.1 stopped before V01 because its source authority fixture exposed only two
positive-length entries while the unchanged matrix requires four.

That defect was corrected outside the scientific validation runner by
prospectively constructing and freezing a dedicated four-object authority
fixture.

## 4. Frozen engine under test

Design protocol:

`experiments/model_fractal/MAF_OBJECT_RUNTIME_RESIDENCY_V1_PROTOCOL.md`

SHA256:

`81987d00ef4cb51556dcebf08bff9c9fa8979f033df05304d347b759e545eb13`

Runtime engine:

`experiments/model_fractal/maf_object_runtime_residency_v1.py`

SHA256:

`4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9`

The engine under test must remain byte-identical throughout V1.2.

V1.2 tests the existing frozen implementation; it does not authorize an
engine modification.

## 5. Frozen fixture-construction lineage

Fixture-construction protocol:

`experiments/model_fractal/MAF_OBJECT_RUNTIME_RESIDENCY_VALIDATION_V1_2_FIXTURE_PROTOCOL.md`

SHA256:

`da86e2c86967c64865010bea45846237baa6a9b877f560bdb9201e52d1723a31`

Fixture builder:

`experiments/model_fractal/maf_object_runtime_residency_validation_v1_2_fixture.py`

SHA256:

`6e183519582b5704d34aca8910d26619c5664571df78ff44734e41f7edec258b`

Frozen construction result:

`experiments/model_fractal/maf_object_runtime_residency_validation_v1_2_fixture.json`

SHA256:

`acb9d90f3ac29357529f283a6a51fa13d7f48d7c599bb52be50d77e108a2e4e5`

The fixture construction slot has been spent permanently.

Fixture reconstruction or rerun is forbidden.

## 6. Frozen source authority fixture

Source fixture root:

`results/runtime/maf_object_runtime_residency_validation_v1_2_fixture`

The source fixture contains exactly three files and no subdirectories.

### Active authority

Path:

`results/runtime/maf_object_runtime_residency_validation_v1_2_fixture/active_generation.json`

SHA256:

`8608a480178c030cf70de39df845e724cc8f1a8afa99f74c66ef1c46f1befbd6`

### Candidate manifest

Path:

`results/runtime/maf_object_runtime_residency_validation_v1_2_fixture/candidate_a.manifest.json`

SHA256:

`ba5ba793a0bcdda217b5e3b91061a35151617bcf7cb97ae6202f14c080369c96`

### Persistent segment

Path:

`results/runtime/maf_object_runtime_residency_validation_v1_2_fixture/segment_00000000.mafseg`

SHA256:

`f965b526538d757ca2d6114af6517c57cbcb3650b71d8cfb92046a04ef2f566b`

Model PK:

`mafmodel:v1:b3d13be495d56e4fa7bafe145bf4efdc3b5dc13596446252d45f8adadd340a1b`

Generation PK:

`mafgen:v1:7eb91f963f0bde05ec74e9031d9fb72e74992d947bcc8dbdca486d36478db51f`

The manifest contains exactly four genuine positive-length object authority
entries.

Their frozen V1.1-compatible sort order by `(length, object_pk)` is:

`A, B, C, D`

The source fixture is immutable evidence.

V1.2 must copy the source fixture into its isolated validation runtime exactly
as V1.1 did; validation must never mutate the frozen source fixture.

## 7. V1.2 output paths

Future V1.2 runner:

`experiments/model_fractal/maf_object_runtime_residency_validation_v1_2.py`

Raw result:

`experiments/model_fractal/maf_object_runtime_residency_validation_v1_2.json`

Isolated validation runtime:

`results/runtime/maf_object_runtime_residency_validation_v1_2`

Before the exact-once validation invocation, both the raw result path and
isolated validation runtime must be absent.

## 8. Authorized V1.1 -> V1.2 runner transformations

The V1.2 runner must be derived from the exact frozen V1.1 runner.

Only the following successor transformations are authorized:

1. validation version/docstring/console lineage from V1.1 to V1.2;
2. result schema from
   `openmind.maf_object_runtime_residency_validation.v1.1`
   to
   `openmind.maf_object_runtime_residency_validation.v1.2`;
3. validation protocol path from the V1.1 protocol to this V1.2 protocol;
4. validation protocol SHA256 to this protocol's eventual frozen SHA256;
5. result path from the V1.1 result path to the V1.2 result path;
6. source runtime path from the old two-object source fixture to the dedicated
   frozen four-object V1.2 authority fixture;
7. source expected-file identities to the exact active, manifest, and segment
   SHA256 values frozen in Section 6;
8. isolated validation runtime path from the V1.1 runtime directory to the
   V1.2 runtime directory;
9. version-specific human-readable exact-once/rerun wording where needed to
   refer correctly to V1.2.

No other transformation is authorized.

In particular:

- V01-V32 test bodies must not be scientifically changed;
- assertions must not be weakened;
- thresholds must not be changed;
- concurrency structure must not be weakened;
- synchronization/barrier behavior must not be changed;
- thread cardinality must not be changed;
- operation ordering must not be changed;
- pass/fail aggregation semantics must not be changed;
- failure atomicity expectations must not be changed;
- source immutability requirements must not be changed;
- the four-entry fixture guard must remain in force.

A static V1.1-to-V1.2 diff audit must prove the successor delta is confined to
the authorized transformations before the V1.2 runner may be frozen.

## 9. Frozen scientific matrix

Exactly 32 scientific checks are preregistered, in this order:

01. `V01_runtime_binding`
02. `V02_initial_cold_disk`
03. `V03_legal_upward_primitive_transitions`
04. `V04_legal_downward_primitive_transitions`
05. `V05_illegal_skipped_transitions`
06. `V06_same_state_idempotence`
07. `V07_verified_hot_maf_promotion`
08. `V08_corruption_hash_failure_nonpublication`
09. `V09_short_read_nonpublication`
10. `V10_stale_generation_rejection`
11. `V11_serialized_byte_accounting`
12. `V12_dense_byte_accounting`
13. `V13_zero_budget_rejection`
14. `V14_over_budget_failure_atomicity`
15. `V15_multiple_pin_floor_composition`
16. `V16_pinned_demotion_rejected`
17. `V17_unknown_pin_rejection`
18. `V18_consumed_pin_rejection`
19. `V19_unpin_no_automatic_demotion`
20. `V20_dense_materialization_success`
21. `V21_dense_materialization_failure_atomicity`
22. `V22_dense_view_lifetime_invalidation`
23. `V23_runtime_close_cleanup`
24. `V24_close_idempotence`
25. `V25_operation_rejection_after_close`
26. `V26_source_file_immutability`
27. `V27_no_unverified_byte_escape`
28. `V28_snapshot_accounting_consistency`
29. `V29_concurrent_same_object_promotion`
30. `V30_concurrent_pin_unpin_accounting`
31. `V31_concurrent_observation_no_provisional_state`
32. `V32_promotion_race_no_duplicate_ownership`

No check may be removed, renamed, reordered, bypassed, or replaced.

## 10. Concurrency correctness boundary

V29-V32 are the concurrency-correctness portion of Phase 6C:

- V29 proves concurrent same-object promotion behavior;
- V30 proves concurrent pin/unpin accounting;
- V31 proves observation does not expose provisional state;
- V32 proves promotion races do not produce duplicate ownership.

These are correctness tests, not throughput benchmarks.

Broad multithread throughput, lock-contention, scaling, and performance
optimization remain outside this validation and belong to later performance
work.

## 11. Source-fixture isolation rule

Before V01 begins, the runner must:

1. verify all three frozen source fixture hashes;
2. verify the expected four positive-length authority entries;
3. require the V1.2 validation-runtime path to be absent;
4. create a new isolated validation runtime;
5. copy the three frozen source files into that runtime;
6. verify copied-file identities exactly;
7. construct runtime entries from the copied authority state.

The source fixture must be hashed again after validation.

Any source-fixture mutation is validation failure.

The isolated validation runtime is evidence and must not be cleaned after the
exact-once run.

## 12. Fixture cardinality

The global requirement for at least four positive-length entries remains
unchanged.

The frozen source fixture provides exactly four.

The validation matrix therefore uses the frozen sorted entries as follows:

- V01 has at least A, B, C available;
- V25 has its required second entry B;
- V28 has A, B, C, D available;
- concurrency checks operate against the same frozen four-object authority
  population used by the unchanged V1.1 scientific logic.

No scientific check is modified merely to fit the fixture.

## 13. Exact-once scientific validation rule

The V1.2 runner must be implemented, statically audited, and frozen in Git
before execution.

A separate final no-write preflight must then prove:

- exact branch and frozen parent;
- exact V1.2 protocol SHA256;
- exact V1.2 runner SHA256;
- exact engine SHA256;
- exact source fixture hashes;
- source fixture remains committed and unchanged;
- raw V1.2 result path absent;
- isolated V1.2 validation runtime absent;
- staging empty;
- no executable Git hooks;
- V1 and V1.1 remain untouched.

The first invocation of the frozen V1.2 runner permanently spends the V1.2
scientific validation slot whether the process succeeds, fails, crashes, or
terminates before V01.

After invocation:

- never edit and rerun that frozen runner version;
- never delete failure residue to create a clean retry;
- freeze the raw V1.2 result before interpretation whenever it exists;
- retain the isolated validation runtime as evidence;
- use a prospectively preregistered successor version for any correction.

## 14. Raw result requirements

The V1.2 raw result must retain the V1.1 result structure except for authorized
version/provenance changes.

It must bind at minimum:

- V1.2 schema;
- design protocol SHA256;
- V1.2 validation protocol SHA256;
- engine SHA256;
- source fixture identities;
- source-before and source-after identities;
- isolated fixture identities;
- validation check records;
- failed-check set;
- validation validity;
- all-pass state;
- fatal type/message when applicable.

The raw result is evidence whether the validation passes or fails.

## 15. Interpretation boundary

Only after the raw result has been frozen may the V1.2 scientific outcome be
interpreted.

A fixture-copy failure, harness failure, or provenance failure must not be
misreported as an engine correctness failure.

An engine verdict is permitted only when the result structure and validation
progress justify that conclusion.

## 16. Success criterion

V1.2 scientific validation succeeds only if:

- the validation harness is valid;
- every V01-V32 check executes under its preregistered semantics;
- all 32 checks pass;
- no failed checks remain;
- no fatal error remains;
- source fixture hashes are unchanged;
- the runtime engine SHA256 remains unchanged;
- result provenance binds this exact frozen protocol and runner.

## 17. Failure criterion

Any failed V01-V32 check means V1.2 does not establish full Phase 6C
runtime-residency correctness.

Any harness/provenance failure invalidating scientific interpretation must be
classified separately from an engine failure.

In all cases, once invoked, V1.2 may not be rerun.

## 18. Nonclaims

Even a complete V1.2 pass would establish only the preregistered Phase 6C
runtime-residency correctness properties.

It would not by itself establish:

- MAF-native language-model inference;
- replacement of a conventional LLM inference pipeline;
- selective tensor avoidance during model computation;
- Vulkan acceleration;
- multithread throughput superiority;
- lock-scaling superiority;
- end-to-end generation quality parity;
- end-to-end generation speed parity.

Those require later phases and separate prospective benchmarks.

## 19. Freeze sequence

After this protocol is frozen:

1. derive V1.2 runner from frozen V1.1;
2. perform static V1.1-to-V1.2 successor-delta audit;
3. freeze the V1.2 runner locally;
4. perform final no-write exact-once preflight;
5. invoke V1.2 exactly once;
6. freeze the raw result immediately;
7. preserve the isolated validation runtime;
8. interpret only the frozen evidence.

## 20. Authorization boundary

Freezing this protocol authorizes only implementation, static audit, and local
freeze of the V1.2 runner.

It does not authorize V1.2 execution yet.

V1 RERUN: FORBIDDEN.

V1.1 RERUN: FORBIDDEN.

FIXTURE RERUN: FORBIDDEN.

V1.2 VALIDATION: NOT AUTHORIZED UNTIL RUNNER FREEZE + FINAL PREFLIGHT.

No cleanup of frozen fixture evidence is authorized.

No upstream push is authorized.
