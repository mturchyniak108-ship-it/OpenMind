# Phase 6C MAF Object Runtime Residency Scientific Verdict

Status: CLOSED — PASS
Phase: 6C
Scope: MAF object runtime/residency correctness
Scientific engine verdict: PASS
Performance verdict: NONE
Benchmark executed: NO
Backend selected: NONE

## 1. Closure

Phase 6C is scientifically closed on frozen V1.3 evidence.

The exact-once V1.3 validation executed all 32 prospectively preregistered
checks.

Result:

- validation valid: true
- all pass: true
- check count: 32
- failed checks: []
- fatal error: none
- source fixture unchanged: true
- benchmark executed: false
- backend selected: none

V29-V32 executed and passed.

The Phase 6C engine verdict is therefore PASS for the preregistered
runtime/residency correctness surface.

## 2. Frozen repository closure point

Closure parent:

`263079f5f2091dec905e12964b2e0ba02f2fcebc`

Branch:

`labs/multidimensional-maf`

The closure parent freezes the complete isolated V1.3 runtime evidence.

## 3. Frozen design and engine

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

## 4. Frozen V1.3 scientific lineage

Validation protocol:

`experiments/model_fractal/MAF_OBJECT_RUNTIME_RESIDENCY_VALIDATION_V1_3_PROTOCOL.md`

SHA256:

`e12c5dc67d2e147d2c0305c0782cc76ce90a390e7bd276ba0030b3e461fabf17`

Frozen protocol commit:

`63f268439dedbfa53f8ba866722fdf7f1d9eb2aa`

Validation runner:

`experiments/model_fractal/maf_object_runtime_residency_validation_v1_3.py`

SHA256:

`9d74a78ec5aad3eb937090f5c0aebccd49fca3a83d1eb99665bd7c246a66a1f6`

Frozen runner commit:

`6cae169102675fce82b2917d25ea10e4108e1937`

Raw scientific result:

`experiments/model_fractal/maf_object_runtime_residency_validation_v1_3.json`

SHA256:

`1b7fcbe8ca8674928a11b58be950adaaa6a85e1f991636d21a557d160d0c719f`

Frozen result commit:

`88777eb148c36da19299afdc1a6e2c1594678808`

Frozen isolated-runtime commit:

`263079f5f2091dec905e12964b2e0ba02f2fcebc`

Isolated-runtime tree SHA256:

`fa196304f93da590f728f55cb09ba57c260fb821900c9a73c0ff4a01ba1c8ac0`

## 5. Frozen source authority

Source authority root:

`results/runtime/maf_object_runtime_residency_validation_v1_2_fixture`

`active_generation.json`

- size: 380
- SHA256:
  `8608a480178c030cf70de39df845e724cc8f1a8afa99f74c66ef1c46f1befbd6`

`candidate_a.manifest.json`

- size: 1846
- SHA256:
  `ba5ba793a0bcdda217b5e3b91061a35151617bcf7cb97ae6202f14c080369c96`

`segment_00000000.mafseg`

- size: 4096
- SHA256:
  `f965b526538d757ca2d6114af6517c57cbcb3650b71d8cfb92046a04ef2f566b`

The source authority remained immutable across the valid V1.3 scientific run.

## 6. Frozen V1.3 isolated runtime evidence

Runtime root:

`results/runtime/maf_object_runtime_residency_validation_v1_3`

Runtime tree SHA256:

`fa196304f93da590f728f55cb09ba57c260fb821900c9a73c0ff4a01ba1c8ac0`

Files:

`active_generation.json`

- size: 380
- SHA256:
  `8608a480178c030cf70de39df845e724cc8f1a8afa99f74c66ef1c46f1befbd6`

`candidate_a.manifest.json`

- size: 1846
- SHA256:
  `ba5ba793a0bcdda217b5e3b91061a35151617bcf7cb97ae6202f14c080369c96`

`corrupt_segment.mafseg`

- size: 4096
- SHA256:
  `740e545ccb9939d3d6c12538c3407c3aa3994544d5f9e291bc86a4cd1a20be9c`

`segment_00000000.mafseg`

- size: 4096
- SHA256:
  `f965b526538d757ca2d6114af6517c57cbcb3650b71d8cfb92046a04ef2f566b`

The frozen result runtime inventory and the frozen runtime evidence matched
exactly.

## 7. Scientific matrix

All 32 checks executed and passed:

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

## 8. Concurrency result

The following preregistered multithreaded correctness tests executed and
passed:

- V29 concurrent same-object promotion;
- V30 concurrent pin/unpin accounting;
- V31 concurrent observation with no provisional state exposure;
- V32 promotion race with no duplicate ownership.

This establishes only the tested concurrency-correctness properties.

It does not establish multithread throughput or scalability.

## 9. Historical exact-once lineage

V1:

- exact-once slot spent;
- harness failed before a valid scientific verdict;
- rerun forbidden.

V1.1:

- exact-once slot spent;
- four-positive-object fixture requirement was not met;
- no valid engine verdict;
- rerun forbidden.

V1.2:

- exact-once slot spent;
- frozen result SHA256:
  `4190ae354583d3e9594a94b6ff64f31ea0869a8e0ded228b116e71bbb59b546c`;
- harness stopped before V01 because
  `candidate_a.manifest.json` expected size remained stale at 1202 bytes
  while the frozen authority size was 1846 bytes;
- no V1.2 engine verdict;
- rerun forbidden.

V1.3:

- prospectively preregistered successor;
- corrected only the stale fixture-size binding plus successor provenance;
- exact-once slot spent;
- all V01-V32 passed;
- Phase 6C verdict: PASS;
- rerun forbidden.

## 10. Claims established by Phase 6C

The frozen evidence supports the preregistered correctness properties for the
current MAF object runtime/residency engine, including:

- runtime binding;
- COLD_DISK initial state;
- legal primitive upward transitions;
- legal primitive downward transitions;
- rejection of illegal skipped transitions;
- same-state idempotence;
- verified HOT_MAF promotion;
- corruption failure nonpublication;
- short-read failure nonpublication;
- stale-generation rejection;
- serialized byte accounting;
- dense byte accounting;
- zero-budget rejection;
- over-budget failure atomicity;
- multiple-pin floor composition;
- pinned-demotion rejection;
- unknown-pin rejection;
- consumed-pin rejection;
- unpin without automatic demotion;
- dense materialization success;
- dense materialization failure atomicity;
- dense-view lifetime invalidation;
- runtime close cleanup;
- close idempotence;
- operation rejection after close;
- source-file immutability;
- no unverified byte escape;
- snapshot accounting consistency;
- concurrent same-object promotion correctness;
- concurrent pin/unpin accounting correctness;
- no provisional-state exposure under concurrent observation;
- no duplicate ownership under the tested promotion race.

## 11. Explicit nonclaims

Phase 6C does not establish:

- inference throughput;
- latency superiority;
- multithread scalability;
- lock-contention behavior;
- Vulkan acceleration;
- GPU residency;
- mmap performance;
- file-descriptor cache performance;
- automatic eviction quality;
- selective tensor materialization;
- selective tensor avoidance;
- full MAF-native model inference;
- language-model generation quality;
- conventional LLM-runtime replacement;
- end-to-end speed parity or superiority versus llama.cpp or another runtime.

`benchmark_executed = false`.

`backend_selected = none`.

Those questions require separate prospective phases.

## 12. Next research boundary

Phase 6C is closed.

The next research phase is:

**Phase 6D — MAF topology/locality**

Phase 6D must be prospectively defined before experimental claims are made.

Phase 6C artifacts, results, runtime evidence, source fixture, and all spent
exact-once validation versions remain immutable historical evidence.

No V1, V1.1, V1.2, or V1.3 validation rerun is permitted.

No fixture rerun is permitted.

No cleanup of frozen scientific evidence is permitted.
