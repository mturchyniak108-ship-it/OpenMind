# MAF Query Capsule Attach / Detach / Cleanup Validation V1.1 Correction Protocol

Status: preregistration only  
Phase: 6D-Q3 — Attach / Detach / Cleanup  
Scientific execution: not authorized by this protocol freeze alone

## 1. Purpose

This protocol preregisters the Q3 V1.1 correction namespace after the frozen Q3 V1 exact-once namespace was permanently spent by a harness-level Python class-identity failure before scientific result publication.

V1.1 is not a retry of V1.

V1 remains immutable failed provenance.

V1.1 may correct only the proven module-loading identity defect described below. It must preserve the original Q3 scientific question, lifecycle semantics, query cases, acceptance checks, source evidence, failure injections, exact-once durability model, and claim boundary.

## 2. Failed V1 immutable provenance

Frozen V1 runner:

`experiments/model_fractal/maf_query_capsule_attach_detach_cleanup_validation_v1.py`

Frozen V1 runner SHA256:

`b3a0812f5abe7549ce2282efce78b33628d7cbc42689ba236c43ec1b767d4638`

Frozen V1 runner commit:

`b67191666230ff053bed9f61353a83e3d983a2cd`

Spent V1 slot:

`experiments/model_fractal/maf_query_capsule_attach_detach_cleanup_validation_v1.slot`

Spent V1 slot SHA256:

`17cc5ac3ecd2caf6822dd6fb36b8c0273dda5bbde6791b598a51b933bb079a33`

Required V1 slot states, in exact order:

1. `RESERVATION_PREPARED`
2. `RESERVED_DURABLE`

Preserved V1 partial:

`experiments/model_fractal/maf_query_capsule_attach_detach_cleanup_validation_v1.json.partial`

Preserved V1 partial bytes:

`0`

Preserved V1 partial SHA256:

`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

V1 final result:

must remain absent.

V1 automatic retry:

forbidden.

V1 manual scientific retry:

forbidden.

No V1 slot, partial, runner, runner SHA authority, or prospective result path may be deleted, rewritten, renamed, repaired, replaced, truncated, or reused by V1.1.

## 3. Proven V1 failure localization

The V1 exact-once run reached:

`NAMESPACE_GUARD -> PREQUAL -> SLOT_CREATE -> PREPARED_DURABLE -> RESERVED_DURABLE -> PARTIAL_CREATE -> SCIENCE`

The failure occurred during `SCIENCE`, before any bytes were written to the V1 partial and before V1 result publication.

Observed failure type:

`MAFObjectRuntimeInvalidEntryError`

Observed failure message:

`entry must be ResidentPKEntry`

The frozen canonical Q3 source evidence, fixture evidence, Q2 evidence, active record, catalog, query fixture, generation manifests, and physical segment remained unchanged.

## 4. Proven root cause

The V1 harness dynamically loaded the resident-directory implementation and the runtime implementation under separate dynamic module identities.

The runtime implementation imports `ResidentPKEntry` from canonical module name:

`maf_resident_pk_directory_v1`

The V1 harness separately loaded the resident-directory source under another module identity.

Therefore the resident-directory entry returned to the runtime was structurally equivalent to `ResidentPKEntry` but was not an instance of the exact `ResidentPKEntry` class object used by the runtime.

The class-identity forensic probe confirmed:

- the dynamically loaded resident class and runtime resident class were different class objects;
- an instance created from the dynamically loaded resident class failed `isinstance(..., runtime.ResidentPKEntry)`;
- this mismatch explains the observed V1 `MAFObjectRuntimeInvalidEntryError`.

This is a harness module-identity defect. It is not scientific evidence against Q3 lifecycle semantics.

## 5. Authorized V1.1 correction

V1.1 may change only dependency-loading mechanics required to guarantee one coherent Python module identity for the resident-directory class used by both the resident snapshot builder and the runtime.

The required invariant is:

`resident_module.ResidentPKEntry is runtime_module.ResidentPKEntry`

before V1.1 namespace reservation and before V1.1 science.

The correction must use canonical module identity for the resident-directory dependency.

The implementation may establish the frozen `experiments/model_fractal` directory as an import search path and load the resident-directory and runtime implementations under their canonical module names, or use another deterministic mechanism that proves the same exact class-object identity.

The V1.1 readiness/prequalification path must fail closed unless all of the following are true:

- frozen resident-directory source SHA is exact;
- frozen runtime source SHA is exact;
- resident and runtime modules originate from the frozen expected paths;
- `resident_module.ResidentPKEntry is runtime_module.ResidentPKEntry`;
- the resident snapshot still resolves the exact frozen 12 object PKs;
- all original Q3 source and fixture bindings remain exact;
- failed V1 provenance remains exact and unmodified;
- the V1.1 namespace is empty.

No scientific logic may be changed to make checks pass.

## 6. Scientific semantics unchanged

V1.1 must preserve the frozen Q3 V1 scientific semantics exactly.

The preregistered query cases remain exactly:

- `q001` — `specific_intent` — `layer 0 attention query` — selected cardinality 1 — fallback false;
- `q025` — `multi_target_intent` — `layer 0 normalization` — selected cardinality 2 — fallback false;
- `q026` — `multi_target_intent` — `layer 0 attention` — selected cardinality 4 — fallback false;
- `q033` — `fallback_control` — `weather tomorrow` — selected cardinality 4 — fallback true.

Query Capsule requirements remain:

- `initial_object_pks = selected_object_pks`;
- `selected_relationship_pks = ()`;
- `route_order = selected_object_pks` in exact selector order;
- `expansion_policy = "disabled"`;
- `max_object_budget = 4`;
- `max_expansion_rounds = 0`;
- deterministic Q1 `derive_query_pk`.

Runtime requirements remain:

- fresh Phase 6C runtime per independent lifecycle;
- exact frozen model PK and generation PK;
- register only objects in the exact Capsule route;
- serialized-byte budget `33554432`;
- dense-byte budget `4096`;
- lifecycle-only dense materializer `(sha256(serialized).digest(), 32)`.

Ownership requirements remain:

- exactly one live `MAPPED` pin lease per query-owned object;
- explicit object-PK to lease table;
- duplicate ownership rejected;
- no object outside the Capsule route may acquire ownership.

Successful lifecycle and deterministic reverse-route cleanup remain unchanged.

Failure injections remain exactly:

- F01 before first attach;
- F02 after first `MAPPED` attach but before first pin;
- F03 after first pin acquisition;
- F04 after `q001` reaches `HOT_MAF`;
- F05 after `q001` reaches synthetic `HOT_DENSE`;
- F06 after two `q026` route objects have acquired ownership.

Negative tests remain exactly:

- canonical but unknown object PK rejected before attach;
- stale canonical generation rejected before attach;
- valid-looking manifest SHA mismatch rejected before attach;
- duplicate ownership rejected;
- pinned demotion below `MAPPED` rejected.

## 7. Acceptance checks unchanged

V1.1 must emit the same 48 scientific acceptance checks in the same exact order:

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

All V01-V48 are required.

There is no partial scientific PASS.

V1.1 must additionally record non-scientific correction provenance and prequalification evidence proving the class-identity invariant and failed-V1 bindings. These provenance fields do not replace, renumber, weaken, or add scientific acceptance checks.

## 8. Canonical-state preservation

V1.1 must hash-bind and preserve the same frozen Q1, Q2, source-generation, catalog, query-fixture, active-record, fixture-authority, physical-manifest, and physical-segment evidence required by V1.

V1.1 must additionally preserve and hash-bind:

- failed V1 runner;
- failed V1 runner SHA authority;
- failed V1 spent slot;
- failed V1 empty partial.

V1 result absence must be verified before V1.1 readiness and before V1.1 reservation.

## 9. V1.1 exact-once namespace

Prospective V1.1 runner:

`experiments/model_fractal/maf_query_capsule_attach_detach_cleanup_validation_v1_1.py`

Runner SHA authority:

`experiments/model_fractal/maf_query_capsule_attach_detach_cleanup_validation_v1_1.py.sha256`

Permanent slot journal:

`experiments/model_fractal/maf_query_capsule_attach_detach_cleanup_validation_v1_1.slot`

Exclusive partial result:

`experiments/model_fractal/maf_query_capsule_attach_detach_cleanup_validation_v1_1.json.partial`

Final result:

`experiments/model_fractal/maf_query_capsule_attach_detach_cleanup_validation_v1_1.json`

Prospective verdict:

`experiments/model_fractal/MAF_QUERY_CAPSULE_ATTACH_DETACH_CLEANUP_VALIDATION_V1_1_VERDICT.md`

Result schema:

`openmind.maf_query_capsule_attach_detach_cleanup_validation.v1_1`

V1.1 namespace guard must refuse execution if any V1.1 slot, partial, or final result path already exists.

The V1.1 runner must verify its own frozen `.py.sha256` authority before reservation.

Successful V1.1 slot creation permanently spends the V1.1 namespace.

Any failure after successful V1.1 slot creation permanently spends the V1.1 namespace.

No automatic retry is permitted.

No manual scientific retry in the same V1.1 namespace is permitted.

## 10. V1.1 durability order

The exact V1.1 order is:

`NAMESPACE_GUARD -> PREQUAL -> SLOT_CREATE -> PREPARED_DURABLE -> RESERVED_DURABLE -> PARTIAL_CREATE -> SCIENCE -> PARTIAL_FSYNC -> RENAME_NOREPLACE -> RESULT_DIR_FSYNC -> PUBLISHED_DURABLE`

Required durability properties remain:

- slot creation uses exclusive creation and append semantics;
- prepared record is durably fsynced before reserved append;
- parent directory is fsynced at required barriers;
- partial creation is exclusive;
- science begins only after durable reservation;
- partial bytes are fsynced before publication;
- publication uses `renameat2` with `RENAME_NOREPLACE = 1`;
- there is no publication fallback;
- result parent directory is fsynced after rename;
- published journal record is appended only after the result name is durable;
- slot journal is never removed, replaced, truncated, renamed, or reused;
- canonical JSON uses `allow_nan=False`.

## 11. V1.1 readiness

A non-spending V1.1 readiness mode is authorized only after the V1.1 runner and its SHA authority have been independently reviewed and frozen.

Readiness must:

- run the namespace guard;
- verify all frozen authorities;
- verify failed V1 provenance;
- verify the V1 result remains absent;
- prove coherent resident/runtime `ResidentPKEntry` class identity;
- verify the exact frozen fixture and 12-PK resident snapshot;
- verify the publication backend;
- perform no Q3 scientific lifecycle;
- call no Q2 validation runner;
- create no V1.1 slot, partial, or result.

## 12. Claim boundary

A successful V1.1 run may support only:

- Q3 attach/detach lifecycle correctness under the frozen cases;
- Q3 ownership-lease correctness;
- Q3 source/generation binding;
- deterministic cleanup accounting;
- preregistered failure cleanup atomicity;
- terminal close semantics.

It must not claim:

- route-cache validity or Q4 completion;
- bounded expansion;
- inference;
- answer generation;
- working-set sufficiency;
- tensor/object avoidance;
- output parity;
- answer quality;
- MAF-native compute;
- performance superiority;
- LLM replacement;
- Phase 6E entry.

## 13. Freeze rule

This correction protocol must be frozen before implementation of the V1.1 runner.

After this protocol is frozen:

1. implement only the V1.1 runner and its self-hash authority;
2. perform compile/static/semantic review only;
3. freeze the exact V1.1 runner and SHA authority;
4. run non-spending V1.1 readiness;
5. only after readiness acceptance may one exact-once V1.1 scientific arm be considered.

No V1.1 science is authorized during protocol creation, runner implementation, static review, or runner freeze.
