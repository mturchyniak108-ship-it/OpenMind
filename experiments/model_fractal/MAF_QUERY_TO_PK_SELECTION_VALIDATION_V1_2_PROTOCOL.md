# MAF Query-to-PK Selection Validation V1.2 Protocol

## Status

**PREREGISTERED PROSPECTIVE SCIENTIFIC VALIDATION**

Phase:

**6D-Q2 — Query-to-PK Selection Prototype**

Validation:

**V1.2 — durable exact-once journal handshake successor**

Scientific execution is not authorized by creation of this document.

V1 remains frozen and unexecuted.

V1.1 remains frozen as negative design evidence and must not be implemented or executed.

---

## 1. Reason for V1.2

Independent static audit of V1.1 identified two critical specification gaps and
one design ambiguity before any V1.1 runner existed:

1. the exact slot-record schema identifier was not frozen;
2. failure while writing the initial slot record was not explicitly classified;
3. the initial record was named `RESERVED_DURABLE` before its durability
   barrier had completed.

V1.2 corrects all three findings before runner construction.

No scientific hypothesis, selector behavior, catalog, query fixture, target
oracle, baseline formula, metric definition, candidate budget, threshold, or
boundary exclusion is changed from frozen V1.

---

## 2. Historical authorities and dispositions

Frozen V1 validation protocol SHA256:

`9bea52de94d8784f6862eee9108afdd1f52f9ff4d4f95eb03fb78d5477e00c11`

Frozen V1 runner SHA256:

`e2e32f85b1dc7015802ec51a6f214188becc5d35f45c76f4b320617ccd6cd873`

Frozen V1.1 protocol SHA256:

`5d94ef0e3330bb63964b0ec2f929fbc9b41290f3f307684bfaece6a1f6e1a8ed`

V1 disposition:

**RETIRED-UNEXECUTED / RESULT SLOT UNSPENT / DO NOT ARM**

V1.1 disposition:

**SUPERSEDED-PRE-RUNNER / NEGATIVE DESIGN EVIDENCE / SLOT UNSPENT / DO NOT IMPLEMENT**

Neither historical protocol may be edited.

---

## 3. Unchanged scientific question

Can the exact frozen Phase 6D-Q2 V1 selector use only query-derived signals
and immutable static object metadata to select bounded MAF object-PK
candidates under the preregistered non-oracle contract?

This tests metadata-intent routing only.

It does not test selective inference sufficiency.

---

## 4. Frozen scientific authorities

Selection protocol SHA256:

`b42a0643976c2393871e3b826ba5573b4de981b49603de63230d69cf57be0811`

Selector implementation SHA256:

`e21c05e352fe921b791e8c936425727a98911ce7566989672a96bfd2b9613fa2`

Q1 acceptance verdict SHA256:

`c396346adfc3d7aed08373a52d02e88ce14b2195269c9d090c2572828db77615`

Catalog SHA256:

`c51ef0fabeb10e7c8a091a093aa1934620a69b2026b5a87cb02477b9dd7ca900`

Prospective query fixture SHA256:

`32f4636bd5e8ceee0dca8342335279a6f8e6acafe866a5469f2c23aa2655202a`

Source generation manifest SHA256:

`28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3`

Source generation PK:

`mafgen:v1:45a80a2aa271ce04853003185b6a1227cb309bd1e3e2dc538eea849fac9f5db0`

Selection configuration SHA256:

`0caeaeaafdd870e6b02ccc8b4450576883d4ef5234ba689c472e3b14d9dbe120`

Random baseline seed:

`OPENMIND_6D_Q2_V1_RANDOM_BASELINE`

These scientific authorities are unchanged from V1.

---

## 5. V1.2 namespace

Protocol:

`experiments/model_fractal/MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_2_PROTOCOL.md`

Future runner:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_2.py`

Future runner SHA authority:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_2.py.sha256`

Future authoritative result:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_2.json`

Future result partial:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_2.json.partial`

Permanent slot journal:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_2.slot`

Future verdict:

`experiments/model_fractal/MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_2_VERDICT.md`

At protocol freeze, only the protocol may exist.

---

## 6. Runner freeze authority

The V1.2 runner does not exist at protocol freeze.

After runner construction and independent audit:

1. exact runner bytes are frozen;
2. SHA256 of those bytes is computed;
3. the `.py.sha256` authority contains exactly 64 lowercase hexadecimal
   characters plus one terminal newline;
4. the runner hashes its own `__file__` before any slot creation;
5. the runner requires exact equality with the frozen SHA authority;
6. the result records `validation_runner_sha256`.

No runner modification is permitted after runner freeze.

---

## 7. Scientific-equivalence requirement

Before any V1.2 reservation, static audit must prove that the scientific
surface is semantically equivalent to frozen V1 for:

- query normalization;
- query-intent parsing;
- tensor descriptor parsing;
- independent expected-target calculation;
- query-signature construction;
- deterministic random baseline;
- selector invocation;
- query-class semantics;
- metric accumulation;
- thresholds;
- boundary exclusions.

Harness-only changes are permitted.

No query, target, candidate budget, baseline, threshold, or scientific
interpretation may change.

---

## 8. Exact slot-journal path rule

The exact V1.2 slot journal is:

`maf_query_to_pk_selection_validation_v1_2.slot`

The runner must create it only with exclusive creation semantics equivalent to:

`O_WRONLY | O_CREAT | O_EXCL | O_APPEND`

mode:

`0600`

The slot journal is never:

- deleted;
- truncated;
- renamed;
- replaced;
- recreated;
- reused for another protocol.

Any visible V1.2 slot journal forbids automatic V1.2 scientific execution.

---

## 9. Canonical slot-record encoding

Every slot-journal record is one canonical UTF-8 JSON object followed by
exactly one newline.

Canonical JSON uses:

- `sort_keys=True`
- `separators=(",", ":")`
- `ensure_ascii=False`
- `allow_nan=False`

Records are appended only.

No record is rewritten.

---

## 10. Exact PREPARED record schema

Exact schema identifier:

`openmind.maf_query_to_pk_selection_validation.slot.prepared.v1_2`

Exact field set:

1. `schema`
2. `sequence`
3. `state`
4. `validation_protocol_sha256`
5. `prior_v1_protocol_sha256`
6. `prior_v1_runner_sha256`
7. `prior_v1_1_protocol_sha256`
8. `validation_runner_sha256`
9. `selection_protocol_sha256`
10. `implementation_sha256`
11. `catalog_sha256`
12. `query_fixture_sha256`
13. `source_generation_manifest_sha256`
14. `source_generation_pk`
15. `final_result_basename`
16. `partial_result_basename`

Exact values:

- `sequence = 1`
- `state = "RESERVATION_PREPARED"`

The PREPARED record does not claim durability.

---

## 11. PREPARED write failure classification

After exclusive slot creation, the complete PREPARED record must be written
with positive-progress write semantics.

If record serialization fails, `os.write` raises, a short-write loop makes no
positive progress, file fsync fails, or the first parent-directory fsync
fails:

- science must not begin;
- the runner must classify:
  `RESERVATION_PREPARE_OR_DURABILITY_FAILURE`;
- all surviving slot evidence must be preserved;
- automatic retry is forbidden while a slot pathname remains visible;
- no result or partial may be synthesized;
- the original exception is re-raised.

This explicitly includes failure while writing the initial record.

---

## 12. First durability barrier

Mandatory ordering:

`PREQUAL -> SLOT_CREATE -> PREPARED_WRITE -> SLOT_FSYNC -> DIR_FSYNC`

Only after both the slot fsync and parent-directory fsync succeed is the slot
pathname and PREPARED record considered durably established.

Science is still forbidden at this point.

---

## 13. Exact RESERVED_DURABLE record schema

Exact schema identifier:

`openmind.maf_query_to_pk_selection_validation.slot.reserved_durable.v1_2`

Exact field set:

1. `schema`
2. `sequence`
3. `state`
4. `prepared_record_sha256`

Exact values:

- `sequence = 2`
- `state = "RESERVED_DURABLE"`

`prepared_record_sha256` is SHA256 of the exact canonical PREPARED record
bytes including its terminal newline.

---

## 14. Durable reservation handshake

After the first durability barrier:

1. append the complete RESERVED_DURABLE record;
2. fsync the slot-journal descriptor;
3. fsync the parent directory descriptor again;
4. verify the slot pathname still names the opened journal inode;
5. only then classify the reservation as `RESERVED_DURABLE`;
6. only then may scientific evaluation begin.

Exact ordering:

`PREPARED_DIR_FSYNC -> DURABLE_APPEND -> SLOT_FSYNC -> DIR_FSYNC -> SCIENCE`

The journal therefore never claims `RESERVED_DURABLE` before the durability
barrier protecting that claim has completed.

---

## 15. Durable-marker failure

If appending, writing, fsyncing, directory-fsyncing, or verifying the
RESERVED_DURABLE record fails:

- science must not begin;
- classify:
  `RESERVATION_DURABLE_MARKER_FAILURE`;
- preserve all surviving slot evidence;
- automatic retry is forbidden while a slot pathname remains visible;
- no result or partial may be synthesized;
- re-raise the original failure.

---

## 16. Power-loss interpretation before science

V1.2 science cannot begin before the RESERVED_DURABLE handshake completes.

Therefore:

- if a slot survives a crash, automatic rerun is forbidden;
- if no slot survives and an independent recovery audit proves no durable
  marker could have completed, the event is pre-scientific;
- the runner itself performs no automatic recovery or retry;
- ambiguous recovery requires human review and, if necessary, a successor
  protocol.

No disappearance of a partial or final pathname can restore a spent durable
slot.

---

## 17. Partial result staging

Only after `RESERVED_DURABLE` may the result partial be created.

Partial creation uses exclusive creation.

The partial is staging data only.

It is never the exact-once authority.

Failure after durable reservation never restores the slot.

---

## 18. Scientific execution

Scientific evaluation uses exactly the frozen V1 selector, catalog, query
fixture, source bindings, oracle semantics, baseline, metrics, and thresholds.

There is no scientific retry.

There is no network access.

There is no inference.

---

## 19. Result write durability

After result construction:

1. serialize canonical result JSON with `allow_nan=False`;
2. write complete bytes to the partial with positive-progress semantics;
3. fsync the partial file descriptor;
4. close the partial descriptor only after successful fsync.

Zero write progress is a hard failure.

---

## 20. Publication primitive

Final publication uses only:

`libc.renameat2(..., RENAME_NOREPLACE)`

with exact flag value:

`RENAME_NOREPLACE = 1`

The source partial and final result are same-directory siblings addressed
through the same already-open parent directory descriptor.

Forbidden fallbacks:

- `os.rename`
- `os.replace`
- `os.link`
- libc `link`
- libc `linkat`
- shell publication
- subprocess publication

---

## 21. Result-name durability barrier

Exact publication order:

`PARTIAL_FSYNC -> RENAME_NOREPLACE -> PARENT_DIR_FSYNC`

Rename success alone is not durable publication.

Only successful parent-directory fsync establishes:

`RESULT_NAME_DURABLE`

---

## 22. Post-rename durability failure

If rename succeeds but parent-directory fsync fails:

- slot remains spent;
- no retry is permitted;
- classify:
  `POST_RENAME_DURABILITY_UNCONFIRMED`;
- report visible final/partial pathnames;
- report readable sizes and SHA256 values;
- preserve all evidence;
- re-raise the original failure.

A visible final result is not silently declared durable.

---

## 23. Exact PUBLISHED_DURABLE record schema

Exact schema identifier:

`openmind.maf_query_to_pk_selection_validation.slot.published_durable.v1_2`

Exact field set:

1. `schema`
2. `sequence`
3. `state`
4. `reserved_durable_record_sha256`
5. `result_sha256`
6. `result_bytes`
7. `final_result_basename`

Exact values:

- `sequence = 3`
- `state = "PUBLISHED_DURABLE"`

The record may be appended only after `RESULT_NAME_DURABLE`.

---

## 24. Publication journal commit

After durable result-name publication:

1. append PUBLISHED_DURABLE record;
2. fsync the slot-journal descriptor;
3. fsync the parent directory descriptor;
4. preserve the slot journal permanently.

If append/write/fsync fails after result publication:

- classify:
  `PUBLICATION_DURABLE_JOURNAL_COMMIT_FAILED`;
- preserve final result and slot journal;
- forbid retry;
- re-raise.

---

## 25. Journal recovery invariant

The journal states are monotonic:

`RESERVATION_PREPARED -> RESERVED_DURABLE -> PUBLISHED_DURABLE`

A missing later record never invalidates an earlier surviving record.

A malformed or torn trailing record is post-reservation uncertainty.

Any visible slot journal blocks automatic scientific rerun.

The runner never deletes recovery evidence.

---

## 26. Pre-reservation failures

Failures before successful exclusive slot creation are non-spending.

They must leave V1.2 slot, partial, and result absent.

Examples:

- SHA mismatch;
- runner self-SHA mismatch;
- science-equivalence failure;
- malformed catalog;
- malformed fixture;
- backend qualification failure;
- readiness failure;
- guard failure;
- half-arm failure.

---

## 27. Dual-arm execution

V1.2 uses new V1.2-specific arm values.

V1 or V1.1 arm values cannot authorize V1.2.

Environment-only arming is non-spending.

CLI-only arming is non-spending.

Guard-false execution is non-spending.

Exact names and values are frozen by the future runner before runner freeze.

---

## 28. Scientific metrics

The metric keys remain exactly the V1 keys:

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

## 29. Acceptance thresholds

Thresholds remain exactly V1:

- evaluation query count >= 32;
- specific-intent query count >= 16;
- unique specific expected object PKs >= 8;
- supported-intent target-hit rate = 1.0;
- supported-intent precision = 1.0;
- specific-intent top-1 accuracy >= 0.95;
- selector-minus-baseline top-1 difference >= 0.50;
- budget violation count = 0;
- duplicate selection count = 0;
- generation-binding violation count = 0;
- manifest-binding violation count = 0;
- oracle-input violation count = 0.

No threshold may be weakened.

---

## 30. V1.2 result schema

Schema identifier:

`openmind.maf_query_to_pk_selection_validation.v1_2`

Exact top-level fields:

1. `schema`
2. `exact_once`
3. `validation_protocol_sha256`
4. `prior_v1_protocol_sha256`
5. `prior_v1_runner_sha256`
6. `prior_v1_1_protocol_sha256`
7. `selection_protocol_sha256`
8. `implementation_sha256`
9. `q1_verdict_sha256`
10. `catalog_sha256`
11. `query_fixture_sha256`
12. `source_generation_pk`
13. `source_manifest_sha256`
14. `selection_config_sha256`
15. `validation_runner_sha256`
16. `random_baseline_seed`
17. `expected_check_count`
18. `check_count`
19. `checks`
20. `failed_checks`
21. `auditor_error`
22. `all_pass`
23. `metrics`
24. `acceptance_thresholds`
25. `boundary_exclusions`
26. `publication_backend`

No additional top-level fields are permitted.

Canonical JSON uses `allow_nan=False` and exactly one terminal newline.

---

## 31. Exact V1.2 check matrix

Expected check count:

`66`

Exact ordered IDs:

`V01_prior_v1_protocol_binding`
`V02_prior_v1_runner_binding`
`V03_prior_v1_1_protocol_binding`
`V04_q2_protocol_binding`
`V05_selector_implementation_binding`
`V06_q1_acceptance_verdict_binding`
`V07_catalog_schema`
`V08_catalog_canonical_json`
`V09_catalog_generation_manifest_binding`
`V10_catalog_unique_sorted_object_pks`
`V11_catalog_static_metadata_surface_only`
`V12_selection_config_exact`
`V13_query_fixture_schema`
`V14_query_fixture_canonical_json`
`V15_evaluation_query_minimum`
`V16_specific_query_minimum`
`V17_distinct_specific_target_minimum`
`V18_fallback_control_minimum`
`V19_query_id_uniqueness_and_order`
`V20_query_class_semantics`
`V21_selector_api_non_oracle`
`V22_no_route_cache_input`
`V23_no_bounded_expansion`
`V24_no_inference_network_or_subprocess`
`V25_independent_target_predicate`
`V26_target_predicate_does_not_call_selector`
`V27_random_baseline_exact_seed_and_formula`
`V28_random_baseline_no_oracle_input`
`V29_v1_science_semantic_equivalence`
`V30_runner_self_sha_authority`
`V31_renameat2_backend_required`
`V32_no_weaker_publication_fallback`
`V33_dual_arm_required`
`V34_guard_false_non_spending`
`V35_fixture_qualification_before_slot`
`V36_backend_qualification_before_slot`
`V37_slot_path_exact`
`V38_prepared_schema_exact`
`V39_reserved_durable_schema_exact`
`V40_published_durable_schema_exact`
`V41_slot_o_excl_append_creation`
`V42_prepared_record_exact_fields`
`V43_prepared_write_positive_progress`
`V44_prepared_slot_fsync`
`V45_prepared_parent_directory_fsync`
`V46_reserved_durable_append_after_first_barrier`
`V47_reserved_durable_slot_fsync`
`V48_reserved_durable_parent_directory_fsync`
`V49_science_after_reserved_durable_only`
`V50_existing_slot_rejects_execution`
`V51_partial_o_excl_after_durable_slot`
`V52_partial_file_fsync_before_publication`
`V53_rename_noreplace_result_publication`
`V54_parent_directory_fsync_after_rename`
`V55_published_record_after_result_name_durable`
`V56_published_record_slot_fsync`
`V57_slot_journal_never_deleted_truncated_or_replaced`
`V58_pre_durable_failure_is_non_scientific`
`V59_post_durable_failure_no_retry`
`V60_post_rename_durability_failure_classified`
`V61_publication_journal_failure_classified`
`V62_exact_once_no_retry_contract`
`V63_result_schema_canonical_and_finite`
`V64_result_authority_bindings`
`V65_scientific_thresholds_and_structural_zero_counts`
`V66_boundary_exclusions`

No check may be removed, renamed, reordered, or added after runner freeze.

---

## 32. Failure-state model

The future runner must distinguish at least:

`PRE_RESERVATION_FAILURE`

`RESERVATION_PREPARE_OR_DURABILITY_FAILURE`

`RESERVATION_DURABLE_MARKER_FAILURE`

`RESERVED_DURABLE_PRE_SCIENCE_FAILURE`

`SCIENTIFIC_EVALUATION_FAILURE`

`RESULT_CONSTRUCTION_FAILURE`

`PARTIAL_WRITE_OR_FSYNC_FAILURE`

`RENAME_NOREPLACE_FAILURE`

`POST_RENAME_DURABILITY_UNCONFIRMED`

`PUBLICATION_DURABLE_JOURNAL_COMMIT_FAILED`

`PUBLISHED_DURABLE`

Every state after `RESERVED_DURABLE` forbids scientific retry.

Any visible slot journal forbids automatic execution.

---

## 33. Boundary exclusions

V1.2 preserves the V1 exclusions:

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

## 34. Negative-result policy

Scientific failure remains evidence.

No failed V1.2 run may be rescued by changing selector, catalog, queries,
oracle, baseline, candidate budget, metrics, thresholds, or slot state.

No slot journal may be deleted to enable rerun.

A successor protocol is required.

---

## 35. Construction sequence

After protocol freeze:

1. independently audit V1.2 protocol;
2. freeze protocol SHA256;
3. construct V1.2 runner only;
4. prove V1 scientific semantic equivalence;
5. audit every slot-journal and publication failure path;
6. freeze runner bytes;
7. freeze runner SHA authority;
8. perform non-spending guard/readiness/backend checks;
9. update current-facing documentation;
10. publish through the clean GitHub publication branch;
11. verify local and remote authority hashes;
12. only then consider one authoritative V1.2 run.

---

## 36. Current authorization

At protocol freeze:

**V1 SCIENCE: FORBIDDEN / RETIRED-UNEXECUTED**

**V1 RESULT SLOT: UNSPENT**

**V1.1: SUPERSEDED-PRE-RUNNER / DO NOT IMPLEMENT**

**V1.1 SLOT: UNSPENT**

**V1.2 SCIENCE: NOT AUTHORIZED**

**V1.2 RUNNER: MUST NOT EXIST**

**V1.2 SLOT: MUST NOT EXIST**

The next authorized activity is:

**INDEPENDENT STATIC AUDIT OF THIS V1.2 PROTOCOL**
