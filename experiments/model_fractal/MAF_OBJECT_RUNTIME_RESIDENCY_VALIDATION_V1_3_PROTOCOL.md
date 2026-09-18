# MAF Object Runtime Residency Validation V1.3 Protocol

Status: PROSPECTIVE PREREGISTRATION
Phase: 6C
Artifact class: scientific validation protocol
Validation status: NOT YET EXECUTED
Engine verdict: NONE

## 1. Purpose

This protocol preregisters Phase 6C MAF Object Runtime Residency Validation
V1.3.

V1.3 is a prospective successor to frozen V1.2.

V1.2 did not execute V01-V32. It stopped during source-fixture identity
verification before isolated validation-runtime creation.

The V1.2 root cause is proven exactly:

- `candidate_a.manifest.json` SHA256 was correct;
- frozen authority size is `1846` bytes;
- frozen V1.2 runner expected the stale V1.1 size
  `1202` bytes;
- the harness therefore raised
  `ValidationHarnessError: source fixture identity mismatch`;
- V1.2 recorded zero scientific checks;
- V1.2 produced no engine verdict;
- V29-V32 did not execute.

V1.3 corrects only that stale fixture-size binding plus the minimum
version/provenance/output-path changes required for a successor validation.

The scientific V01-V32 matrix remains unchanged.

## 2. Frozen repository parent

Branch:

`labs/multidimensional-maf`

Parent:

`cc69f470000d01568d7ec363b315edc4d467b66c`

This parent is the commit that freezes the raw V1.2 result.

## 3. Frozen V1.2 failure evidence

V1.2 protocol:

`experiments/model_fractal/MAF_OBJECT_RUNTIME_RESIDENCY_VALIDATION_V1_2_PROTOCOL.md`

SHA256:

`74b74a31c889ab3c1c39a35de11714b9e76e87acb5bb3bfa969c120b427a14f2`

V1.2 runner:

`experiments/model_fractal/maf_object_runtime_residency_validation_v1_2.py`

SHA256:

`9a077e0963b137bbcc36bda67321de441c20de575bc54f85dcc06b3ce49b016a`

V1.2 raw result:

`experiments/model_fractal/maf_object_runtime_residency_validation_v1_2.json`

SHA256:

`4190ae354583d3e9594a94b6ff64f31ea0869a8e0ded228b116e71bbb59b546c`

Frozen V1.2 result facts:

- schema:
  `openmind.maf_object_runtime_residency_validation.v1.2`
- `validation_valid = false`
- `all_pass = false`
- scientific check count = `0`
- failed-check list = `[]`
- fatal type = `ValidationHarnessError`
- fatal message = `source fixture identity mismatch`
- isolated V1.2 validation runtime = absent
- engine verdict = none.

The V1.2 exact-once slot is permanently spent.

V1.2 must never be edited or rerun.

## 4. Earlier spent validation versions

V1 exact-once slot: SPENT — RERUN FORBIDDEN.

V1.1 exact-once slot: SPENT — RERUN FORBIDDEN.

V1.2 exact-once slot: SPENT — RERUN FORBIDDEN.

Historical harness failures must remain immutable evidence.

## 5. Frozen engine under test

Design protocol:

`experiments/model_fractal/MAF_OBJECT_RUNTIME_RESIDENCY_V1_PROTOCOL.md`

SHA256:

`81987d00ef4cb51556dcebf08bff9c9fa8979f033df05304d347b759e545eb13`

Runtime engine:

`experiments/model_fractal/maf_object_runtime_residency_v1.py`

SHA256:

`4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9`

Resident PK Directory:

`experiments/model_fractal/maf_resident_pk_directory_v1.py`

SHA256:

`4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6`

Segment Reader:

`experiments/model_fractal/maf_segment_reader_v1.py`

SHA256:

`3499cb8e528fe8e9315e3e5656d6aa888c95ca175310b6371e722de409827369`

V1.3 does not authorize any engine, resident-directory, or segment-reader
modification.

## 6. Frozen four-object fixture lineage

Fixture-construction protocol:

`experiments/model_fractal/MAF_OBJECT_RUNTIME_RESIDENCY_VALIDATION_V1_2_FIXTURE_PROTOCOL.md`

SHA256:

`da86e2c86967c64865010bea45846237baa6a9b877f560bdb9201e52d1723a31`

Fixture builder:

`experiments/model_fractal/maf_object_runtime_residency_validation_v1_2_fixture.py`

SHA256:

`6e183519582b5704d34aca8910d26619c5664571df78ff44734e41f7edec258b`

Fixture construction result:

`experiments/model_fractal/maf_object_runtime_residency_validation_v1_2_fixture.json`

SHA256:

`acb9d90f3ac29357529f283a6a51fa13d7f48d7c599bb52be50d77e108a2e4e5`

Fixture-construction exact-once slot: SPENT PERMANENTLY.

Fixture reconstruction or rerun: FORBIDDEN.

## 7. Frozen authority fixture

Authority root:

`results/runtime/maf_object_runtime_residency_validation_v1_2_fixture`

### active_generation.json

Size:

`380`

SHA256:

`8608a480178c030cf70de39df845e724cc8f1a8afa99f74c66ef1c46f1befbd6`

### candidate_a.manifest.json

Correct frozen size:

`1846`

SHA256:

`ba5ba793a0bcdda217b5e3b91061a35151617bcf7cb97ae6202f14c080369c96`

The stale V1.2 runner value was:

`1202`

That stale value is forbidden in the V1.3
`SOURCE_FILE_EXPECTATIONS["candidate_a.manifest.json"]["size"]` field.

### segment_00000000.mafseg

Size:

`4096`

SHA256:

`f965b526538d757ca2d6114af6517c57cbcb3650b71d8cfb92046a04ef2f566b`

Model PK:

`mafmodel:v1:b3d13be495d56e4fa7bafe145bf4efdc3b5dc13596446252d45f8adadd340a1b`

Generation PK:

`mafgen:v1:7eb91f963f0bde05ec74e9031d9fb72e74992d947bcc8dbdca486d36478db51f`

The authority fixture remains byte-for-byte unchanged from V1.2.

V1.3 corrects the harness binding to the fixture; it does not alter the
fixture.

## 8. V1.3 output paths

Future V1.3 runner:

`experiments/model_fractal/maf_object_runtime_residency_validation_v1_3.py`

Raw result:

`experiments/model_fractal/maf_object_runtime_residency_validation_v1_3.json`

Isolated validation runtime:

`results/runtime/maf_object_runtime_residency_validation_v1_3`

Before the V1.3 exact-once invocation, both the result and isolated-runtime
paths must be absent.

## 9. Authorized V1.2 -> V1.3 runner delta

The V1.3 runner must be mechanically derived from the exact frozen V1.2
runner.

Only these transformations are authorized:

1. current validation version/human-readable lineage from V1.2 to V1.3;
2. result schema from
   `openmind.maf_object_runtime_residency_validation.v1.2`
   to
   `openmind.maf_object_runtime_residency_validation.v1.3`;
3. validation protocol path from the frozen V1.2 protocol to this V1.3
   protocol;
4. validation protocol SHA256 to this protocol's eventual frozen SHA256;
5. result path from the V1.2 result path to the V1.3 result path;
6. isolated validation-runtime path from the V1.2 runtime path to the V1.3
   runtime path;
7. exactly one fixture-identity data correction:
   `SOURCE_FILE_EXPECTATIONS["candidate_a.manifest.json"]["size"]`
   from `1202` to `1846`;
8. exact-once/rerun wording where needed to refer correctly to V1.3.

The following must remain unchanged:

- source fixture root;
- all three source SHA256 identities;
- active-generation size `380`;
- segment size `4096`;
- runtime-engine identity;
- V01-V32 test logic;
- assertion logic;
- pass/fail aggregation;
- failure-atomicity semantics;
- fixture-copy logic;
- four-positive-entry guard;
- source-immutability logic;
- concurrency worker structure;
- thread cardinality;
- barriers;
- start/join behavior;
- timeouts;
- operation ordering.

No other V1.2 -> V1.3 transformation is authorized.

## 10. Required successor-delta proof

Before V1.3 may be frozen, a static audit must prove:

- V1.2 runner SHA256 is exact;
- only the authorized successor fields changed;
- the manifest expected size is exactly `1846`;
- stale size `1202` is absent from the V1.3 manifest-size
  expectation;
- all three expected fixture sizes equal actual frozen file sizes;
- all three expected fixture hashes equal actual frozen hashes;
- V01-V32 names and order are unchanged;
- function order is unchanged;
- concurrency constructor/start/join structure is unchanged;
- reverse-normalizing the authorized successor changes reproduces the frozen
  V1.2 AST.

The V1.3 runner must not be imported or executed during that audit.

## 11. Frozen scientific matrix

Exactly 32 scientific checks remain preregistered, in this order:

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

No check may be removed, renamed, reordered, bypassed, weakened, or replaced.

## 12. Concurrency correctness boundary

V29-V32 remain correctness tests:

- V29 concurrent same-object promotion;
- V30 concurrent pin/unpin accounting;
- V31 concurrent observation with no provisional state exposure;
- V32 promotion race with no duplicate ownership.

V1.2 never reached these checks.

V1.3 makes no concurrency performance claim.

Throughput, contention, scalability, and lock-granularity benchmarking remain
outside this validation.

## 13. Source-fixture identity rule

Before isolated-runtime creation, V1.3 must verify all three frozen authority
files against both size and SHA256:

`active_generation.json`

- size = `380`
- SHA256 = `8608a480178c030cf70de39df845e724cc8f1a8afa99f74c66ef1c46f1befbd6`

`candidate_a.manifest.json`

- size = `1846`
- SHA256 = `ba5ba793a0bcdda217b5e3b91061a35151617bcf7cb97ae6202f14c080369c96`

`segment_00000000.mafseg`

- size = `4096`
- SHA256 = `f965b526538d757ca2d6114af6517c57cbcb3650b71d8cfb92046a04ef2f566b`

The complete observed identity dictionary must equal the complete preregistered
expectation dictionary.

This exact size+SHA verification is part of the harness provenance boundary.

## 14. Fixture cardinality

The frozen authority manifest exposes exactly four positive-length objects.

The preregistered four-entry requirement remains unchanged.

No scientific test may be weakened to fit the fixture.

## 15. Exact-once V1.3 rule

The V1.3 runner must be implemented, statically audited, and frozen in Git
before any execution.

A final no-write preflight must then prove:

- exact branch;
- exact frozen V1.3 protocol SHA256;
- exact frozen V1.3 runner SHA256;
- exact engine/dependency SHA256 values;
- exact source fixture sizes;
- exact source fixture SHA256 values;
- result path absent;
- isolated-runtime path absent;
- staging empty;
- no executable Git hooks;
- V1, V1.1, and V1.2 evidence unchanged.

The first execution of the frozen V1.3 runner permanently spends the V1.3
scientific slot whether it passes, fails, crashes, or terminates before V01.

After execution:

- V1.3 may never be rerun;
- the raw result must be frozen before interpretation whenever produced;
- isolated-runtime residue must be preserved;
- no cleanup may be used to manufacture a retry;
- any correction requires another prospectively preregistered successor.

## 16. Raw-result interpretation

A pre-V01 harness/provenance failure is not an engine failure.

An engine verdict is allowed only if the frozen result provides sufficient
scientific execution evidence.

A full successful Phase 6C V1.3 validation requires:

- valid harness;
- all V01-V32 executed;
- check count = 32;
- all checks pass;
- failed checks = [];
- fatal error = none;
- source fixture unchanged;
- exact frozen provenance retained.

## 17. Nonclaims

Even a complete V1.3 pass would establish only the preregistered Phase 6C
runtime/residency correctness properties.

It would not alone establish:

- MAF-native model inference;
- conventional LLM runtime replacement;
- selective tensor avoidance;
- Vulkan acceleration;
- multithread performance superiority;
- end-to-end generation quality parity;
- end-to-end generation speed parity.

Those require separate prospective work.

## 18. Freeze sequence

After this protocol is frozen:

1. mechanically derive V1.3 from frozen V1.2;
2. correct only the preregistered manifest-size binding plus successor
   provenance/version/output fields;
3. perform static successor-delta audit;
4. freeze V1.3 runner locally;
5. run final no-write exact-once preflight;
6. invoke V1.3 exactly once;
7. freeze raw result immediately;
8. preserve isolated-runtime evidence;
9. interpret only frozen evidence.

## 19. Authorization boundary

Freezing this protocol authorizes only:

- implementation of the V1.3 runner;
- static successor-delta auditing;
- local runner freeze.

It does not authorize V1.3 execution yet.

V1 RERUN: FORBIDDEN.

V1.1 RERUN: FORBIDDEN.

V1.2 RERUN: FORBIDDEN.

FIXTURE RERUN: FORBIDDEN.

V1.3 VALIDATION: NOT AUTHORIZED UNTIL RUNNER FREEZE + FINAL PREFLIGHT.

No cleanup is authorized.

No upstream push is authorized.
