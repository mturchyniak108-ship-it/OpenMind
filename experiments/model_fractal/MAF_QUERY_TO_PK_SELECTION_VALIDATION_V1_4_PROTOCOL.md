# MAF Query-to-PK Selection Validation V1.4 Protocol

## Status

**PREREGISTERED PROSPECTIVE SCIENTIFIC VALIDATION**

Phase:

**6D-Q2 — Query-to-PK Selection Prototype**

Validation:

**V1.4 — unconditional namespace-guard successor**

Scientific execution is not authorized by creation of this document.

V1 remains retired and unexecuted.
V1.1, V1.2, and V1.3 remain superseded before runner construction.
No prior scientific slot is spent.

---

## 1. Reason for successor

V1.3 independent protocol audit passed most durability requirements but failed
four required explicit contracts:

1. final-result existence did not independently and unconditionally reject execution;
2. the no-retry rule after successful slot creation was not stated broadly enough;
3. the PREPARED to RESERVED_DURABLE to science order was not stated literally enough;
4. the authoritative result did not explicitly require `validation_runner_sha256`.

V1.4 corrects only those execution-harness and provenance clauses.

The scientific question, selector, catalog, query fixture, oracle, random baseline,
candidate budget, metrics, thresholds, and boundary exclusions remain unchanged.

---

## 2. Frozen predecessor authority

Frozen V1.3 protocol:

`experiments/model_fractal/MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_3_PROTOCOL.md`

Frozen V1.3 protocol SHA256:

`32c69903393661cc25338ff461b9aa40796d7274e332f97743b53703326bd6cb`

V1.3 disposition:

**SUPERSEDED-PRE-RUNNER / SLOT UNSPENT**

V1.3 must not receive a runner or scientific execution after V1.4 freeze.

V1.4 normatively inherits every V1.3 scientific clause not explicitly
superseded by this protocol. If wording conflicts, V1.4 controls.

---

## 3. Frozen V1 scientific runner authority

Frozen V1 runner SHA256:

`e2e32f85b1dc7015802ec51a6f214188becc5d35f45c76f4b320617ccd6cd873`

The frozen V1 runner remains historical evidence only.

V1 must not be armed or executed.

---

## 4. V1.4 namespace

Protocol:

`experiments/model_fractal/MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_4_PROTOCOL.md`

Future runner:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_4.py`

Future runner SHA authority:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_4.py.sha256`

Permanent slot journal:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_4.slot`

Result partial:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_4.json.partial`

Final result:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_4.json`

Future verdict:

`experiments/model_fractal/MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_4_VERDICT.md`

---

## 5. Unconditional namespace guard

The namespace guard runs before authority qualification, fixture qualification,
backend qualification, selector import, slot creation, partial creation, or
scientific evaluation.

The guard checks the exact V1.4 slot, partial, and final-result pathnames.

If the slot exists in any form, execution must refuse immediately.

If the partial exists in any form, execution must refuse immediately.

If the final result exists in any form, execution must refuse immediately.

Any one of those three conditions is sufficient to reject execution.

Rejection at this guard must not delete, truncate, rename, replace, repair,
rewrite, or otherwise mutate any namespace evidence.

The guard does not attempt to infer whether an existing file is complete,
valid, canonical, durable, malformed, empty, torn, stale, or recoverable.

Presence alone is authoritative for refusal.

Exact invariant:

`SLOT_EXISTS OR PARTIAL_EXISTS OR RESULT_EXISTS -> REFUSE_EXECUTION`

---

## 6. Successful slot creation permanently spends V1.4

Before slot creation all frozen prequalification gates must pass.

Slot creation uses exclusive creation.

The instant the exclusive slot-creation syscall returns success, the V1.4
namespace is permanently spent.

This rule applies even if the new slot is:

- zero bytes;
- missing the PREPARED record;
- partially written;
- short-written;
- malformed;
- torn;
- not yet fsynced;
- not yet directory-fsynced;
- unable to receive the RESERVED_DURABLE record.

No condition after successful slot creation can restore V1.4 to UNSPENT.

Exact invariant:

`SLOT_CREATE_SUCCESS -> V1_4_PERMANENTLY_SPENT`

---

## 7. Absolute no-retry rule after slot creation

After successful slot creation, automatic or manual scientific retry of V1.4
is forbidden under every failure state.

This includes failure during:

- PREPARED record construction;
- PREPARED record write;
- short-write handling;
- slot fsync;
- parent-directory fsync;
- inode verification;
- RESERVED_DURABLE append;
- second slot fsync;
- second parent-directory fsync;
- partial creation;
- scientific evaluation;
- result construction;
- partial writing;
- partial fsync;
- rename-no-replace publication;
- post-rename directory fsync;
- PUBLISHED_DURABLE append;
- journal fsync.

A successor protocol version is required for another scientific attempt.

Exact invariant:

`ANY_FAILURE_AFTER_SLOT_CREATE_SUCCESS -> NO_V1_4_RETRY`

---

## 8. Literal reservation and science order

The authoritative execution order is exactly:

`NAMESPACE_GUARD -> PREQUAL -> SLOT_CREATE -> PREPARED_WRITE -> SLOT_FSYNC -> DIR_FSYNC -> RESERVED_DURABLE_APPEND -> SLOT_FSYNC -> DIR_FSYNC -> PARTIAL_CREATE -> SCIENCE`

`RESERVATION_PREPARED` is evidence of an attempted reservation and never
authorizes science.

`RESERVED_DURABLE` is appended only after the PREPARED record has been
completely written, the slot descriptor fsynced, and the parent directory
fsynced.

After the RESERVED_DURABLE append, the slot descriptor is fsynced again and
the parent directory is fsynced again.

Science is forbidden until the second slot fsync and second parent-directory
fsync both succeed.

Exact invariant:

`RESERVATION_PREPARED -> RESERVED_DURABLE -> SCIENCE`

No path may execute science directly from `RESERVATION_PREPARED`.

---

## 9. Initial write failure classification

Failure while constructing or writing the initial PREPARED record, including
a zero-progress write or unrecoverable short-write condition after successful
slot creation, is classified:

`RESERVATION_PREPARED_WRITE_FAILURE`

The namespace remains permanently spent.

Science must not begin.

Retry is forbidden.

Surviving evidence must be preserved.

---

## 10. Existing PREPARED, torn, or malformed slot

On any later invocation, any visible V1.4 slot blocks execution before
prequalification regardless of contents.

A PREPARED-only slot blocks execution.

A zero-byte slot blocks execution.

A torn slot blocks execution.

A malformed slot blocks execution.

A slot with an incomplete final record blocks execution.

No recovery parser may convert slot presence back to UNSPENT.

---

## 11. Existing partial or final result

On any invocation, the V1.4 partial pathname independently blocks execution.

On any invocation, the V1.4 final-result pathname independently blocks execution.

This remains true even if the permanent slot pathname is unexpectedly absent.

Neither partial nor final presence may trigger cleanup followed by rerun.

---

## 12. Result publication durability

The inherited V1.3 publication primitive remains:

`renameat2(..., RENAME_NOREPLACE)`

Publication ordering remains:

`PARTIAL_FSYNC -> RENAME_NOREPLACE -> PARENT_DIR_FSYNC`

A successful rename without successful parent-directory fsync is classified
as durability-unconfirmed and never permits retry.

The slot remains the permanent spending authority.

---

## 13. Validation runner SHA authority

The future V1.4 runner must have a separately frozen SHA256 authority file.

Before slot creation, the runner must hash its own exact bytes and require
equality with that frozen authority.

The V1.4 authoritative result must contain the exact top-level field:

`validation_runner_sha256`

Its value must equal the frozen SHA256 of the exact runner bytes that executed
the validation.

A result lacking this field is structurally invalid.

A result containing a different value is structurally invalid.

---

## 14. V1.4 result schema amendment

The inherited V1.3 result schema is superseded only to require
`validation_runner_sha256`.

V1.4 result schema identifier:

`openmind.maf_query_to_pk_selection_validation.v1_4`

All inherited scientific result fields remain required.

`validation_runner_sha256` is mandatory.

No post-hoc field substitution is allowed.

Non-finite floating-point values remain forbidden.

Serialization must use behavior equivalent to:

`allow_nan=False`

---

## 15. Exact V1.4 check matrix

V1.4 expected check count:

`74`

The exact ordered check IDs are:

`V01_v1_protocol_binding`
`V02_v1_runner_binding`
`V03_v1_1_protocol_binding`
`V04_v1_2_protocol_binding`
`V05_q2_protocol_binding`
`V06_selector_implementation_binding`
`V07_q1_acceptance_verdict_binding`
`V08_catalog_schema`
`V09_catalog_canonical_json`
`V10_catalog_generation_manifest_binding`
`V11_catalog_unique_sorted_object_pks`
`V12_catalog_static_metadata_surface_only`
`V13_selection_config_exact`
`V14_query_fixture_schema`
`V15_query_fixture_canonical_json`
`V16_evaluation_query_minimum`
`V17_specific_query_minimum`
`V18_distinct_specific_target_minimum`
`V19_fallback_control_minimum`
`V20_query_id_uniqueness_and_order`
`V21_query_class_semantics`
`V22_selector_api_non_oracle`
`V23_no_route_cache_input`
`V24_no_bounded_expansion`
`V25_no_inference_network_or_subprocess`
`V26_independent_target_predicate`
`V27_target_predicate_does_not_call_selector`
`V28_random_baseline_exact_seed_and_formula`
`V29_random_baseline_no_oracle_input`
`V30_v1_science_semantic_equivalence`
`V31_runner_self_sha_authority`
`V32_dual_arm_required`
`V33_guard_false_non_spending`
`V34_backend_qualification_before_slot`
`V35_fixture_qualification_before_slot`
`V36_unconditional_namespace_guard_before_all_work`
`V37_existing_slot_always_refuses`
`V38_empty_prepared_malformed_torn_slot_refuses`
`V39_existing_partial_always_refuses`
`V40_existing_final_always_refuses`
`V41_slot_path_exact`
`V42_prepared_schema_exact`
`V43_reserved_durable_schema_exact`
`V44_published_durable_schema_exact`
`V45_slot_o_excl_append_creation`
`V46_successful_slot_creation_spends_namespace`
`V47_initial_write_failure_spends_namespace`
`V48_prepared_slot_fsync`
`V49_prepared_parent_directory_fsync`
`V50_reserved_append_after_prepared_barrier`
`V51_reserved_slot_fsync`
`V52_reserved_parent_directory_fsync`
`V53_science_after_reserved_durable_only`
`V54_any_post_slot_failure_no_retry`
`V55_slot_journal_never_removed_or_replaced`
`V56_partial_o_excl_after_durable_reservation`
`V57_partial_file_fsync_before_publication`
`V58_renameat2_backend_required`
`V59_rename_noreplace_exact_value`
`V60_no_publication_fallback`
`V61_parent_directory_fsync_after_rename`
`V62_post_rename_failure_no_retry`
`V63_published_record_after_result_name_durable`
`V64_published_record_slot_fsync`
`V65_result_schema_and_canonical_json`
`V66_result_authority_bindings`
`V67_supported_intent_target_hit_threshold`
`V68_supported_intent_precision_threshold`
`V69_top1_baseline_structural_thresholds`
`V70_boundary_exclusions`
`V71_final_result_exists_rejects_execution`
`V72_slot_creation_permanently_spends_namespace`
`V73_prepared_reserved_science_literal_order`
`V74_result_binds_validation_runner_sha256`

The V1.4 runner must emit exactly V01 through V74 in this order.

No check may be removed, renamed, reordered, substituted, or added after
runner freeze.

---

## 16. Required pre-run static proof

Before V1.4 runner freeze, independent static audit must prove:

- V1.3 protocol SHA binding;
- V1 runner SHA binding;
- exact V1.4 namespace paths;
- slot, partial, and final each independently reject execution;
- namespace guard precedes every qualification and scientific action;
- successful slot creation permanently spends V1.4;
- every post-slot failure forbids retry;
- PREPARED cannot authorize science;
- RESERVED_DURABLE requires both durability barriers;
- partial creation occurs only after RESERVED_DURABLE;
- result publication uses no-replace semantics;
- post-rename directory fsync is mandatory;
- the slot journal is never deleted, truncated, renamed, or replaced;
- result schema requires `validation_runner_sha256`;
- non-finite floats are forbidden;
- V01 through V74 are exact and ordered.

---

## 17. Prior version disposition

V1:

**RETIRED-UNEXECUTED / UNSPENT / DO NOT ARM**

V1.1:

**SUPERSEDED-PRE-RUNNER / UNSPENT**

V1.2:

**SUPERSEDED-PRE-RUNNER / UNSPENT**

V1.3:

**SUPERSEDED-PRE-RUNNER / UNSPENT**

None of those versions may be used as a substitute execution after V1.4
protocol freeze.

---

## 18. Scientific nonchanges

V1.4 does not change:

- selector implementation;
- catalog;
- prospective query fixture;
- independent oracle;
- random baseline;
- candidate budget;
- supported-intent definition;
- target-hit metric;
- precision metric;
- specific top-1 metric;
- baseline-advantage metric;
- acceptance thresholds;
- scientific interpretation boundary.

This remains metadata-intent query-to-PK selection validation only.

It does not establish inference sufficiency, answer quality, output parity,
tensor avoidance, RAM reduction, latency reduction, throughput improvement,
or MAF-native compute.

---

## 19. Current authorization

At V1.4 protocol freeze:

**V1.4 RUNNER: MUST NOT EXIST**

**V1.4 SLOT: MUST NOT EXIST**

**V1.4 PARTIAL: MUST NOT EXIST**

**V1.4 RESULT: MUST NOT EXIST**

**V1.4 SCIENCE: NOT AUTHORIZED**

The next authorized operation is:

**INDEPENDENT READ-ONLY V1.4 PROTOCOL AUDIT**

Runner construction is authorized only after that independent audit passes.
