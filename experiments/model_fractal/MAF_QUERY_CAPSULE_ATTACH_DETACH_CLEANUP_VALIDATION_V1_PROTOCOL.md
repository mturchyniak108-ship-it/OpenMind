# MAF Query Capsule Attach / Detach / Cleanup Validation V1 Protocol

Status: PREREGISTRATION — SCIENCE NOT EXECUTED

Phase: **6D-Q3 — Attach / Detach / Cleanup**

## 1. Purpose

This protocol prospectively validates query-scoped MAF lifecycle semantics.

The scientific question is:

> Given an accepted immutable Query Capsule and generation-bound PK selection, can OpenMind attach only the capsule-selected objects to the frozen Phase 6C runtime, maintain explicit ownership, reject invalid source bindings, and deterministically return to a clean state after both success and injected failure without modifying canonical MAFDB authority?

This is a lifecycle, ownership, source-binding, and failure-atomicity experiment only.

## 2. Canonical phase naming

The canonical roadmap name for this experiment is:

**Phase 6D-Q3 — Attach / Detach / Cleanup**

The earlier architecture research-question label `Q7 — Cleanup correctness` is descriptive only and does not supersede the roadmap phase identifier.

Selective sufficiency remains Phase 6E-A and is not part of this experiment.

## 3. Frozen architecture authority

- `MAF_QUERY_SCOPED_WORKING_SET_ARCHITECTURE.md`
- SHA256 `7df826096e506d13502e442fb11f7e1f18fb2c5a342f4214b91a3c3df043559c`

## 4. Frozen Q1 Query Capsule authorities

- protocol SHA256 `5255a58c8c6340c251e24ae8543760fcd66a8deb8be1a8356ad5b78ad898edda`
- implementation SHA256 `f897b97011714f3c84b7350c6bb53e800232be8a5d34e5148a3e50a81952976e`
- Validation V1.1 protocol SHA256 `63b40e4ec91410ebea43b85b032a57ed42ba181942390c41fd603a7e5c5cfd3d`
- authoritative result SHA256 `24d1605d1ad95f1b7e7bee190fd0cc978d7b2597d095ac06f68c350208ef1774`
- authoritative verdict SHA256 `c396346adfc3d7aed08373a52d02e88ce14b2195269c9d090c2572828db77615`

Q3 must use the frozen immutable `MAFQueryCapsuleV1` representation.

## 5. Frozen Phase 6C runtime authorities

- runtime protocol SHA256 `81987d00ef4cb51556dcebf08bff9c9fa8979f033df05304d347b759e545eb13`
- runtime implementation SHA256 `4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9`
- Validation V1.3 protocol SHA256 `e12c5dc67d2e147d2c0305c0782cc76ce90a390e7bd276ba0030b3e461fabf17`
- authoritative runtime result SHA256 `1b7fcbe8ca8674928a11b58be950adaaa6a85e1f991636d21a557d160d0c719f`
- Phase 6C verdict SHA256 `800fd8e6e58d2af7ea46133e2e6a26d3b380fa4abd371f055324f722ad92784f`
- activation implementation SHA256 `9435ae8dd32656c7350887689d453f3cb8460887068bfaf06e6f68b5b5b927a1`
- resident PK directory SHA256 `4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6`

Q3 must compose these authorities rather than redesigning Phase 6C residency semantics.

## 6. Frozen Q2 selector authorities

- selection protocol SHA256 `b42a0643976c2393871e3b826ba5573b4de981b49603de63230d69cf57be0811`
- selector implementation SHA256 `e21c05e352fe921b791e8c936425727a98911ce7566989672a96bfd2b9613fa2`
- catalog SHA256 `c51ef0fabeb10e7c8a091a093aa1934620a69b2026b5a87cb02477b9dd7ca900`
- query fixture SHA256 `32f4636bd5e8ceee0dca8342335279a6f8e6acafe866a5469f2c23aa2655202a`
- selection configuration SHA256 `0caeaeaafdd870e6b02ccc8b4450576883d4ef5234ba689c472e3b14d9dbe120`

The Q3 runner may call the frozen `select_query_to_pks_v1` selector implementation.

The spent Q2 V1.4 validation runner must never be invoked.

Q3 consumes selector output as an accepted upstream component. Q3 does not re-test Q2 selection accuracy.

## 7. Frozen authoritative Q2 closure

- V1.4 protocol SHA256 `a814bca93a6b014ee53aad234b8396c841d0efc2a9363598e8a2192f23745699`
- V1.4 runner SHA256 `7bda960c125786fdf3cfca65c4b7b5851ca8bd91257282facfee2fec1ae7a030`
- V1.4 slot SHA256 `0545bba0abcf73e5235d639b0d4390a1e3c01011b1ff0cc9d0372eaf5eb8716a`
- V1.4 result SHA256 `b2ad49d7a9a3e1ef565e07e595efc4a4e00b283f422723553c6437ef3a42def6`
- V1.4 verdict SHA256 `c17198e0013fd9c0a8c59b8f09c05d4f22693dc7d56afdc0f761f55a008c2663`

Q2 V1.4 is permanently spent and must not be rerun, repaired, regenerated, or replaced.

## 8. Frozen physical source generation

- model PK `mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258`
- generation PK `mafgen:v1:45a80a2aa271ce04853003185b6a1227cb309bd1e3e2dc538eea849fac9f5db0`
- generation manifest SHA256 `28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3`
- segment SHA256 `aa6ccf99df2b65c19634bbeceb91cfe8db2aeced429e55f8fa6318f1d28ff67d`
- segment length `312326668` bytes
- catalog object count `12`

The tracked and physical generation manifests must remain byte-identical.

The physical generation must be consumed read-only.

Q3 is forbidden from rebuilding the generation, objects, or segment.

## 9. Q3 isolated fixture authority

Q3 fixture root:

`results/runtime/maf_query_capsule_attach_detach_cleanup_validation_v1_fixture`

Q3 active record:

`results/runtime/maf_query_capsule_attach_detach_cleanup_validation_v1_fixture/active_generation.json`

Frozen fixture authority record:

`experiments/model_fractal/maf_query_capsule_attach_detach_cleanup_validation_v1_fixture_authority.json`

Fixture qualification is explicitly non-scientific.

Fixture qualification must:

1. verify every frozen authority above;
2. verify tracked and physical generation manifest byte identity;
3. verify the exact physical segment hash and byte length;
4. create only the Q3-isolated active record using frozen `maf_activation_v1_1.activate_generation`;
5. pass the frozen Q2 physical manifest as `candidate_manifest_path`;
6. map the manifest segment to the existing frozen physical segment without copying or rewriting it;
7. reopen and independently verify the five-field active record;
8. build a resident PK directory snapshot from the new Q3 active authority;
9. prove that exactly the 12 frozen catalog object PKs resolve;
10. prove the snapshot generation PK and manifest SHA match the frozen Q2 source generation;
11. write canonical fixture authority JSON only after all qualification checks pass.

Fixture qualification failure produces no Q3 scientific PASS or FAIL.

The scientific runner must never create or repair the fixture.

The runner must require a previously frozen fixture authority and active record.

## 10. Prospective Q3 query cases

Exactly four pre-existing frozen Q2 query records are authorized:

- `q001` — specific intent — `layer 0 attention query` — expected structural cardinality 1
- `q025` — multi-target intent — `layer 0 normalization` — expected structural cardinality 2
- `q026` — multi-target intent — `layer 0 attention` — expected structural cardinality 4
- `q033` — fallback control — `weather tomorrow` — expected selected cardinality 4

No other Q2 query may be substituted after protocol freeze.

Q3 does not assert the scientific correctness of these selections. That claim belongs to closed Q2.

## 11. Query Capsule construction

For each authorized query, the frozen selector output supplies:

- `query_signature`;
- `source_generation_pk`;
- `source_manifest_sha256`;
- `selection_config_sha256`;
- ordered `selected_object_pks`.

The Q3 Query Capsule must use:

- `initial_object_pks = selected_object_pks`;
- `selected_relationship_pks = ()`;
- `route_order = selected_object_pks` in exact selector order;
- `expansion_policy = "disabled"`;
- `max_object_budget = 4`;
- `max_expansion_rounds = 0`;
- deterministic Q1 `derive_query_pk`.

No relationship expansion is authorized.

## 12. Runtime construction

Each independent query lifecycle receives a fresh Phase 6C `MAFObjectRuntime` bound to the exact frozen model PK and generation PK.

Only directory entries named by the Query Capsule route may be registered into that runtime.

Runtime serialized-byte budget for Q3 V1 is `33554432` bytes.

Runtime dense-byte budget for Q3 V1 is `4096` bytes.

Dense-state testing uses a synthetic lifecycle-only materializer.

The synthetic materializer returns `(sha256(serialized).digest(), 32)`.

This synthetic view exists only to exercise ownership and cleanup of `HOT_DENSE` state. It is not a tensor decoder, model computation, inference backend, or answer-generation path.

## 13. Ownership definition

A query-owned object is a Capsule-selected object for which the Q3 harness has acquired exactly one live Phase 6C pin lease.

The required pin floor is `MAPPED`.

The Q3 harness must maintain an explicit object-PK to pin-lease ownership table.

No object outside the exact Capsule route may acquire a Q3 ownership lease.

A second ownership acquisition for an already query-owned object is rejected by the Q3 harness.

## 14. Successful lifecycle order

For each object in exact `route_order`:

1. resolve its frozen resident-directory entry;
2. register that entry in the fresh runtime;
3. transition `COLD_DISK -> MAPPED`;
4. acquire exactly one `MAPPED` pin lease;
5. record query ownership.

For `q001`, the success-path lifecycle additionally transitions the selected object through `HOT_MAF` and the synthetic `HOT_DENSE` view before cleanup.

The other three success cases remain at `MAPPED` while owned.

## 15. Deterministic cleanup order

Cleanup runs in reverse `route_order`.

For every query-owned object:

1. if `HOT_DENSE`, demote to `HOT_MAF`;
2. if `HOT_MAF`, demote to `MAPPED`;
3. consume the exact live pin lease once;
4. transition `MAPPED -> COLD_DISK`;
5. remove the object from the Q3 ownership table.

After object cleanup, runtime snapshot accounting must show:

- `active_pin_leases == 0`;
- `serialized_resident_bytes == 0`;
- `dense_resident_bytes == 0`;
- every registered query object at `COLD_DISK`.

The runtime is then closed.

A second close must be harmless and post-close mutation/resource operations must be rejected according to the frozen Phase 6C contract.

## 16. Failure injection cases

Exactly these controlled lifecycle failures are preregistered:

- F01 before first attach;
- F02 after first `MAPPED` attach but before first pin;
- F03 after first pin acquisition;
- F04 after `q001` reaches `HOT_MAF`;
- F05 after `q001` reaches synthetic `HOT_DENSE`;
- F06 after two `q026` route objects have acquired ownership.

Injected failure uses a dedicated Q3 test exception and must always enter the same deterministic cleanup path.

Every failure case must finish with zero ownership, zero active leases, zero serialized resident bytes, zero dense resident bytes, and every registered object at `COLD_DISK` before runtime close.

## 17. Negative source and object tests

Q3 must separately test:

- a canonical but unknown object PK rejected before attach;
- a Capsule with a different canonical generation PK rejected before attach;
- a Capsule with a different valid manifest SHA rejected before attach;
- a second ownership request for an already-owned object rejected;
- attempted demotion below the active `MAPPED` pin floor rejected.

No negative test may modify frozen Q1, Q2, generation, catalog, or physical segment evidence.

## 18. Canonical-state preservation

The following bytes must hash identically before and after Q3 science:

- frozen Q1 protocol, implementation, result, and verdict;
- frozen Q2 protocol, runner, slot, result, and verdict;
- Q2 catalog and query fixture;
- Q2 tracked generation manifest;
- Q2 physical generation manifest;
- Q2 physical segment;
- Q3 frozen active-generation record;
- Q3 fixture authority record.

Canonical MAFDB objects and active source-generation authority must not be deleted or rewritten by lifecycle cleanup.

## 19. Frozen scientific acceptance checks

The final validation runner must emit these checks in this exact order:

V01_protocol_authority_binding
V02_q1_capsule_implementation_binding
V03_q1_acceptance_verdict_binding
V04_phase6c_runtime_implementation_binding
V05_phase6c_acceptance_verdict_binding
V06_activation_implementation_binding
V07_resident_directory_binding
V08_selector_authority_binding
V09_catalog_and_query_fixture_binding
V10_q2_authoritative_closure_binding
V11_physical_generation_hash_binding
V12_fixture_authority_binding
V13_fixture_active_record_source_binding
V14_fixture_directory_exact_12_pk_resolution
V15_exact_preregistered_query_case_set
V16_selector_output_source_binding
V17_capsule_deterministic_construction
V18_expansion_disabled_and_budget_exact
V19_only_capsule_selected_objects_registered
V20_unknown_object_rejected_pre_attach
V21_stale_generation_and_manifest_rejected_pre_attach
V22_q001_success_lifecycle
V23_q025_success_lifecycle
V24_q026_success_lifecycle
V25_q033_success_lifecycle
V26_attach_transitions_observed
V27_exact_one_ownership_lease_per_object
V28_duplicate_ownership_rejected
V29_pinned_demotion_rejected
V30_reverse_route_cleanup_order
V31_success_cleanup_active_leases_zero
V32_success_cleanup_serialized_bytes_zero
V33_success_cleanup_dense_bytes_zero
V34_success_cleanup_all_objects_cold
V35_active_record_unchanged
V36_generation_manifest_unchanged
V37_physical_segment_unchanged
V38_q1_q2_frozen_evidence_unchanged
V39_failure_before_first_attach_cleanup
V40_failure_after_partial_attach_cleanup
V41_failure_after_pin_cleanup
V42_failure_after_hot_maf_cleanup
V43_failure_after_hot_dense_cleanup
V44_failure_mid_multi_object_cleanup
V45_repeated_lifecycle_clean_baseline
V46_close_terminal_semantics
V47_route_cache_expansion_inference_and_sufficiency_excluded
V48_phase_boundary_and_no_performance_claim

All V01-V48 must pass.

There is no partial scientific PASS.

## 20. Exact-once scientific namespace

Prospective validation runner:

`experiments/model_fractal/maf_query_capsule_attach_detach_cleanup_validation_v1.py`

Runner SHA authority:

`experiments/model_fractal/maf_query_capsule_attach_detach_cleanup_validation_v1.py.sha256`

Exact-once slot:

`experiments/model_fractal/maf_query_capsule_attach_detach_cleanup_validation_v1.slot`

Partial result:

`experiments/model_fractal/maf_query_capsule_attach_detach_cleanup_validation_v1.json.partial`

Final result:

`experiments/model_fractal/maf_query_capsule_attach_detach_cleanup_validation_v1.json`

Scientific verdict:

`experiments/model_fractal/MAF_QUERY_CAPSULE_ATTACH_DETACH_CLEANUP_VALIDATION_V1_VERDICT.md`

The final result schema is:

`openmind.maf_query_capsule_attach_detach_cleanup_validation.v1`

The result must use canonical UTF-8 JSON, sorted keys, compact separators, and `allow_nan=False`.

Before slot creation the runner must:

1. enforce unconditional namespace guard;
2. bind this protocol SHA256;
3. bind its own frozen runner SHA256 authority;
4. bind every frozen upstream authority;
5. bind and verify the already-qualified Q3 fixture;
6. verify Q2 V1.4 remains permanently spent and unchanged;
7. verify Route Cache remains disabled;
8. verify no Q3 final or partial result exists.

The scientific runner must not create, modify, or repair the fixture during prequalification.

After successful exclusive slot creation, the Q3 namespace is permanently spent.

Any failure after successful slot creation forbids retry.

Durability order must preserve the Q2 V1.4 exact-once pattern:

`NAMESPACE_GUARD -> PREQUAL -> SLOT_CREATE -> PREPARED_DURABLE -> RESERVED_DURABLE -> PARTIAL_CREATE -> SCIENCE -> PARTIAL_FSYNC -> RENAME_NOREPLACE -> RESULT_DIR_FSYNC -> PUBLISHED_DURABLE`

No publication fallback is authorized.

## 21. Forbidden operations

Q3 V1 explicitly forbids:

- invoking the Q2 V1.4 validation runner;
- rebuilding the Q2 generation;
- rewriting the Q2 segment;
- modifying the Q2 catalog or query fixture;
- Query Route Cache reads or writes;
- bounded relationship expansion;
- reference-answer consumption;
- answer generation;
- inference;
- working-set sufficiency claims;
- selective tensor or object avoidance claims;
- output parity claims;
- answer-quality claims;
- MAF-native compute claims;
- performance-superiority claims;
- conventional-LLM replacement claims.

## 22. Claim boundary

A Q3 PASS would establish only that the preregistered Query Capsule lifecycle can attach and own the selected objects under the frozen source generation and can deterministically clean query-scoped runtime state after success and controlled failure.

A Q3 PASS would not establish that the selected working set is sufficient to perform model inference.

A Q3 PASS would not enter Phase 6E.

Q4 Query Route Cache reuse remains a separate future experiment.

## 23. Required development order

1. Freeze this protocol in Git.
2. Implement and independently audit Q3 fixture qualification.
3. Create the isolated Q3 active authority and fixture authority.
4. Freeze the qualified fixture evidence in Git where applicable.
5. Implement the lifecycle validation runner against this frozen protocol.
6. Freeze runner SHA authority.
7. Perform static semantic audit before science.
8. Human reviews all frozen authorities.
9. Execute the exact-once Q3 science once.
10. Freeze result and verdict.
11. Update human and AI documentation only after authoritative evidence exists.

No Q3 lifecycle science is authorized before steps 1 through 8 are complete.
