# MAF Query-to-PK Selection Validation V1.3 Protocol

## Status

**PREREGISTERED PROSPECTIVE SCIENTIFIC VALIDATION**

Phase:

**6D-Q2 — Query-to-PK Selection Prototype**

Validation:

**V1.3 — unconditional namespace/rerun guard successor**

Scientific execution is not authorized by this document.

V1 remains retired-unexecuted.
V1.1 remains superseded-pre-runner.
V1.2 remains superseded-pre-runner.

No V1, V1.1, or V1.2 scientific runner may be armed.

---

## 1. Reason for V1.3

The independent V1.2 audit found three specification gaps in its
pre-execution/recovery wording:

1. existing-slot refusal was not stated as an unconditional namespace guard;
2. prepared, empty, malformed, or torn slot refusal was not stated
   unconditionally enough;
3. existing result/partial refusal was not stated as an unconditional
   pre-execution guard.

The root-cause audit also showed that initial slot-write failure and
post-slot no-retry wording must be explicit at the authoritative guard.

V1.3 corrects only exact-once namespace, durability, and recovery semantics.

It does not change the scientific question, selector, catalog, query fixture,
expected-target oracle, random baseline, candidate budget, metrics, thresholds,
or scientific interpretation.

---

## 2. Frozen predecessor authorities

V1 protocol SHA256:

`9bea52de94d8784f6862eee9108afdd1f52f9ff4d4f95eb03fb78d5477e00c11`

V1 frozen runner SHA256:

`e2e32f85b1dc7015802ec51a6f214188becc5d35f45c76f4b320617ccd6cd873`

V1.1 protocol SHA256:

`5d94ef0e3330bb63964b0ec2f929fbc9b41290f3f307684bfaece6a1f6e1a8ed`

V1.2 protocol SHA256:

`44339b53054a31a6ff1dbcdacd122e95a7b23ad2cea97264e4e67c382a43fd86`

V1 disposition:

**RETIRED-UNEXECUTED / SLOT UNSPENT / DO NOT ARM**

V1.1 disposition:

**SUPERSEDED-PRE-RUNNER / SLOT UNSPENT**

V1.2 disposition:

**SUPERSEDED-PRE-RUNNER / SLOT UNSPENT**

---

## 3. Frozen scientific authorities

Selection protocol SHA256:

`b42a0643976c2393871e3b826ba5573b4de981b49603de63230d69cf57be0811`

Selector implementation SHA256:

`e21c05e352fe921b791e8c936425727a98911ce7566989672a96bfd2b9613fa2`

Q1 acceptance verdict SHA256:

`c396346adfc3d7aed08373a52d02e88ce14b2195269c9d090c2572828db77615`

Catalog SHA256:

`c51ef0fabeb10e7c8a091a093aa1934620a69b2026b5a87cb02477b9dd7ca900`

Query fixture SHA256:

`32f4636bd5e8ceee0dca8342335279a6f8e6acafe866a5469f2c23aa2655202a`

Source generation manifest SHA256:

`28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3`

Source generation PK:

`mafgen:v1:45a80a2aa271ce04853003185b6a1227cb309bd1e3e2dc538eea849fac9f5db0`

Selection configuration SHA256:

`0caeaeaafdd870e6b02ccc8b4450576883d4ef5234ba689c472e3b14d9dbe120`

Random baseline seed:

`OPENMIND_6D_Q2_V1_RANDOM_BASELINE`

All scientific authorities are unchanged.

---

## 4. V1.3 namespaces

Protocol:

`experiments/model_fractal/MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_3_PROTOCOL.md`

Future runner:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_3.py`

Future runner SHA authority:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_3.py.sha256`

Future permanent slot:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_3.slot`

Future partial result:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_3.json.partial`

Future final result:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_3.json`

Future verdict:

`experiments/model_fractal/MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_3_VERDICT.md`

---

## 5. Unconditional namespace guard

This is an authoritative rule.

Before backend qualification, fixture qualification, slot creation, partial
creation, selector execution, metric computation, or any scientific work,
the runner must inspect the exact V1.3 slot, partial, and final paths.

If the V1.3 slot exists in any form, execution MUST REFUSE.

If the V1.3 partial exists in any form, execution MUST REFUSE.

If the V1.3 final result exists in any form, execution MUST REFUSE.

The three refusal rules are independent.

No file-content interpretation may weaken them.

No record parser may be consulted to decide whether an existing slot permits
execution.

No recovery classifier may convert an existing namespace artifact back into
an executable state.

**ANY EXISTING SLOT, PARTIAL, OR FINAL PATH FORBIDS V1.3 EXECUTION.**

---

## 6. Existing-slot rule

Presence of the exact V1.3 slot pathname always refuses execution.

This includes a slot file that is:

- empty;
- zero bytes;
- PREPARED only;
- RESERVED_DURABLE;
- PUBLISHED_DURABLE;
- malformed;
- non-canonical;
- truncated;
- torn;
- partially written;
- unreadable;
- unexpectedly typed;
- otherwise uninterpretable.

**A PREPARED, EMPTY, MALFORMED, OR TORN SLOT STILL FORBIDS RERUN.**

The slot is a spending marker by pathname presence, not by successful parsing.

---

## 7. Existing result/partial rule

Presence of the exact V1.3 partial pathname always refuses execution.

Presence of the exact V1.3 final-result pathname always refuses execution.

This rule applies even if the slot pathname is absent.

A partial or final result may never be deleted, ignored, renamed away, or
replaced to make V1.3 runnable.

**ANY EXISTING RESULT OR PARTIAL PATH FORBIDS V1.3 EXECUTION.**

---

## 8. Slot creation spends V1.3 immediately

The exact slot is created only after all non-spending prequalification passes.

Slot creation uses exclusive creation equivalent to:

`O_WRONLY | O_CREAT | O_EXCL | O_APPEND`

with mode:

`0600`

The instant exclusive slot creation returns success, the V1.3 namespace is
irreversibly spent for this protocol version.

This is true before any bytes are written.

Therefore:

**AFTER SUCCESSFUL SLOT CREATION, AUTOMATIC OR MANUAL V1.3 SCIENTIFIC RETRY IS FORBIDDEN.**

A successor protocol version is required for any later scientific attempt.

---

## 9. Exact slot schemas

Prepared schema identifier:

`openmind.maf_query_to_pk_selection_validation.slot.reservation_prepared.v1_3`

Reserved-durable schema identifier:

`openmind.maf_query_to_pk_selection_validation.slot.reserved_durable.v1_3`

Published-durable schema identifier:

`openmind.maf_query_to_pk_selection_validation.slot.published_durable.v1_3`

The slot journal contains newline-delimited canonical UTF-8 JSON records.

Every complete record has exactly one terminal newline.

Records are append-only.

---

## 10. RESERVATION_PREPARED record

The first intended record has exact state:

`RESERVATION_PREPARED`

It does not claim durability.

It binds:

- schema;
- sequence = 1;
- state;
- V1.3 protocol SHA256;
- V1.2 protocol SHA256;
- V1.1 protocol SHA256;
- V1 protocol SHA256;
- V1 runner SHA256;
- V1.3 runner SHA256;
- selection protocol SHA256;
- selector implementation SHA256;
- catalog SHA256;
- query fixture SHA256;
- source generation manifest SHA256;
- source generation PK;
- partial basename;
- final basename.

The exact field set and canonical ordering behavior must be frozen in the
future runner and independently audited before runner freeze.

---

## 11. Initial slot-write failure classification

This is an authoritative rule.

If slot creation succeeds and writing the initial PREPARED record fails for
any reason, including an exception, short write, zero write, interrupted
write, encoding failure, or fsync-preparation failure, classify:

`INITIAL_SLOT_WRITE_FAILURE_NAMESPACE_SPENT`

The runner must:

- perform no science;
- preserve every surviving byte of the slot;
- preserve the slot pathname if visible;
- never truncate, recreate, replace, or delete the slot;
- never retry V1.3;
- re-raise the original error after bounded classification.

**INITIAL SLOT WRITE FAILURE AFTER SUCCESSFUL SLOT CREATION ALWAYS SPENDS V1.3.**

---

## 12. First durability barrier

After writing the complete PREPARED record:

1. fsync the slot descriptor;
2. fsync the already-open parent directory descriptor;
3. verify, without mutation, that the exact slot pathname still refers to the
   opened journal inode.

Failure of any step is classified:

`PREPARED_DURABILITY_FAILURE_NAMESPACE_SPENT`

No science may begin.

No V1.3 retry is permitted.

---

## 13. RESERVED_DURABLE handshake

Only after the PREPARED durability barrier passes may the second record be
appended.

Its exact state is:

`RESERVED_DURABLE`

It binds the SHA256 of the exact complete PREPARED record.

After append:

1. fsync the slot descriptor;
2. fsync the parent directory descriptor;
3. verify the slot pathname/inode binding again;
4. only then classify reservation as durable;
5. only then may partial staging and science begin.

Mandatory order:

`PREQUAL -> SLOT_CREATE -> PREPARED_WRITE -> SLOT_FSYNC -> DIR_FSYNC -> RESERVED_APPEND -> SLOT_FSYNC -> DIR_FSYNC -> SCIENCE`

The journal never calls the first record durable.

---

## 14. RESERVED_DURABLE write/barrier failure

If writing, appending, fsyncing, directory-fsyncing, or verifying the
RESERVED_DURABLE record fails, classify:

`RESERVED_DURABLE_MARKER_FAILURE_NAMESPACE_SPENT`

Science must not begin.

V1.3 must never retry.

The slot and all surviving evidence are preserved.

---

## 15. Any post-slot failure forbids retry

This is an authoritative rule.

**ANY FAILURE AFTER SUCCESSFUL V1.3 SLOT CREATION FORBIDS V1.3 RETRY.**

This includes failure:

- during PREPARED writing;
- during PREPARED fsync;
- during parent-directory fsync;
- during RESERVED_DURABLE append;
- during RESERVED_DURABLE fsync;
- during slot/inode verification;
- before science;
- during science;
- during metric/result construction;
- during partial creation/write/fsync;
- during rename-no-replace;
- during post-rename directory fsync;
- during publication-journal append/fsync;
- during failure classification.

No automatic recovery path may execute the selector again.

---

## 16. Crash or power-loss rule

If a visible V1.3 slot survives a crash or power loss, rerun is forbidden
without inspecting its contents.

If a visible V1.3 partial survives, rerun is forbidden.

If a visible V1.3 final result survives, rerun is forbidden.

If a prior process is known to have successfully created the V1.3 slot but a
later storage failure leaves no visible slot, V1.3 is still conservatively
retired and must not be rerun.

Absence after an uncertain storage/power-loss event is not proof that the
namespace was never spent.

A successor protocol is required.

---

## 17. Slot immutability

After creation, the slot journal is never:

- deleted;
- truncated;
- renamed;
- replaced;
- recreated;
- unlinked;
- moved aside;
- reset.

The runner must not contain a cleanup path that removes the slot.

A recovery tool must not remove the slot to permit execution.

---

## 18. Partial staging

Partial result creation occurs only after the complete RESERVED_DURABLE
handshake.

Partial creation uses exclusive creation.

Failure after partial creation cannot restore the namespace.

A surviving partial always forbids rerun.

---

## 19. Scientific equivalence

The V1.3 science/evaluation surface must remain semantically identical to
frozen V1 for:

- query normalization;
- query intent parsing;
- tensor descriptor parsing;
- independent expected-target calculation;
- query signatures;
- selector call inputs;
- random baseline;
- candidate budget;
- metric accumulation;
- query-class semantics;
- thresholds;
- boundary exclusions.

Harness-only durability/recovery changes are permitted.

No query, catalog entry, target, baseline seed, budget, metric, or threshold
may be changed.

---

## 20. Result writing

Canonical result serialization uses:

- UTF-8;
- `sort_keys=True`;
- `separators=(",", ":")`;
- `ensure_ascii=False`;
- behavior equivalent to `allow_nan=False`;
- exactly one terminal newline.

The partial write loop may continue only on positive progress.

Zero or negative write progress is a hard post-slot failure.

The complete partial must be fsynced before publication.

---

## 21. Publication

Only:

`renameat2(..., RENAME_NOREPLACE)`

with:

`RENAME_NOREPLACE = 1`

may publish the final result.

Source and destination are same-directory siblings using the same already-open
parent directory descriptor.

Forbidden fallbacks include:

- plain rename;
- replace;
- hard-link publication;
- linkat publication;
- shell commands;
- subprocess publication.

---

## 22. Post-rename durability

Publication order:

`PARTIAL_FSYNC -> RENAME_NOREPLACE -> PARENT_DIR_FSYNC`

Rename success without parent-directory fsync success is classified:

`POST_RENAME_DURABILITY_UNCONFIRMED`

The namespace remains spent.

No retry is permitted.

A visible final result is preserved.

A surviving partial is preserved.

No synthetic replacement result may be created.

---

## 23. PUBLISHED_DURABLE record

Only after successful post-rename parent-directory fsync may the final journal
record be appended.

Exact state:

`PUBLISHED_DURABLE`

It binds:

- exact published-durable schema;
- sequence = 3;
- state;
- RESERVED_DURABLE record SHA256;
- final result SHA256;
- final result byte count;
- final result basename.

After append, fsync the slot descriptor.

Failure is classified:

`PUBLICATION_JOURNAL_COMMIT_FAILURE_NAMESPACE_SPENT`

The already durable result is preserved and science is never rerun.

---

## 24. Pre-slot failures

Failures strictly before successful exclusive slot creation are non-spending
for V1.3 only when slot, partial, and final paths all remain absent.

Examples:

- frozen authority mismatch;
- runner self-SHA mismatch;
- scientific-equivalence failure;
- malformed catalog;
- malformed query fixture;
- backend qualification failure;
- guard/half-arm failure;
- readiness failure.

If any V1.3 slot, partial, or final path becomes visible, the unconditional
namespace guard dominates and execution is forbidden.

---

## 25. Dual arm

V1.3 uses V1.3-specific environment and CLI arm values.

V1, V1.1, or V1.2 arm values cannot authorize V1.3.

Environment-only, CLI-only, and guard-false execution must stop before slot
creation.

The exact arm names/values are frozen in the future runner before runner
freeze.

---

## 26. Runner SHA authority

The future V1.3 runner must hash its own exact bytes before slot creation and
compare them with a separately frozen `.py.sha256` authority.

The authoritative result must record the exact V1.3 runner SHA256.

Runner self-SHA failure is pre-slot and non-spending only if all V1.3
namespace paths remain absent.

---

## 27. Scientific metrics

The exact 17 scientific metrics remain unchanged:

1. `evaluation_query_count`
2. `specific_intent_query_count`
3. `unique_expected_object_pk_count`
4. `metadata_eligible_query_count`
5. `fallback_query_count`
6. `mean_selected_candidate_count`
7. `maximum_selected_candidate_count`
8. `supported_intent_target_hit_rate`
9. `supported_intent_precision`
10. `specific_intent_top1_accuracy`
11. `random_baseline_top1_accuracy`
12. `selector_minus_baseline_top1_difference`
13. `budget_violation_count`
14. `duplicate_selection_count`
15. `generation_binding_violation_count`
16. `manifest_binding_violation_count`
17. `oracle_input_violation_count`

---

## 28. Acceptance thresholds

Thresholds remain exactly:

- evaluation queries >= 32;
- specific-intent queries >= 16;
- distinct specific expected PKs >= 8;
- supported-intent target-hit rate = 1.0;
- supported-intent precision = 1.0;
- specific-intent top-1 accuracy >= 0.95;
- selector-minus-baseline top-1 difference >= 0.50;
- budget violation count = 0;
- duplicate selection count = 0;
- generation-binding violation count = 0;
- manifest-binding violation count = 0;
- oracle-input violation count = 0.

---

## 29. Exact V1.3 check matrix

Expected check count:

`70`

Exact ordered IDs:

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

No ID may change after runner freeze.

---

## 30. Failure-state model

The future runner must distinguish at least:

`PRE_SLOT_FAILURE`

`INITIAL_SLOT_WRITE_FAILURE_NAMESPACE_SPENT`

`PREPARED_DURABILITY_FAILURE_NAMESPACE_SPENT`

`RESERVED_DURABLE_MARKER_FAILURE_NAMESPACE_SPENT`

`RESERVED_DURABLE_PRE_SCIENCE_FAILURE`

`SCIENTIFIC_EVALUATION_FAILURE`

`RESULT_CONSTRUCTION_FAILURE`

`PARTIAL_WRITE_OR_FSYNC_FAILURE`

`RENAME_NOREPLACE_FAILURE`

`POST_RENAME_DURABILITY_UNCONFIRMED`

`PUBLICATION_JOURNAL_COMMIT_FAILURE_NAMESPACE_SPENT`

`PUBLISHED_DURABLE`

Every state after successful slot creation forbids V1.3 rerun.

---

## 31. Result schema

Schema identifier:

`openmind.maf_query_to_pk_selection_validation.v1_3`

The exact result field set must include all V1 scientific/result authorities
plus:

- V1.1 protocol SHA256;
- V1.2 protocol SHA256;
- V1.3 validation protocol SHA256;
- V1.3 validation runner SHA256;
- publication backend;
- exact-once disposition.

The exact complete top-level field set must be frozen during runner
construction and independently audited before runner freeze.

No scientific metric field may change.

---

## 32. Boundary exclusions

V1.3 does not execute or establish:

- inference;
- real-model answer generation;
- route-cache reuse;
- bounded expansion;
- Query Capsule attach/detach lifecycle;
- selective-working-set sufficiency;
- object/tensor avoidance;
- output parity;
- answer quality;
- MAF-native compute;
- performance improvement;
- network access.

---

## 33. Negative-result and no-rescue policy

Scientific failure is evidence.

No failed V1.3 may be rescued by changing:

- selector;
- catalog;
- queries;
- expected-target oracle;
- baseline;
- candidate budget;
- metrics;
- thresholds;
- slot state.

No slot, partial, or final artifact may be removed to enable rerun.

A successor protocol is required.

---

## 34. Construction authorization

After V1.3 protocol freeze:

1. independently audit V1.3;
2. freeze its exact SHA256;
3. only after audit PASS, construct the V1.3 runner;
4. independently audit scientific equivalence and all durability paths;
5. freeze runner bytes and runner SHA authority;
6. run only non-spending guard/readiness modes;
7. synchronize current-facing documentation;
8. publish frozen authorities;
9. verify local/remote authority;
10. only then consider one authoritative V1.3 execution.

At protocol freeze:

**V1.3 SCIENCE: NOT AUTHORIZED**

**V1.3 RUNNER: MUST NOT EXIST**

**V1.3 SLOT: MUST NOT EXIST**

**V1.3 RESULT/PARTIAL: MUST NOT EXIST**

Next authorized work:

**INDEPENDENT READ-ONLY V1.3 PROTOCOL AUDIT**
