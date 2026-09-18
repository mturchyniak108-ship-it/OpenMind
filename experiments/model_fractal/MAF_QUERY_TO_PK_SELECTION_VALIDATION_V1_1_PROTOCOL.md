# MAF Query-to-PK Selection Validation V1.1 Protocol

## Status

**PREREGISTERED PROSPECTIVE SCIENTIFIC VALIDATION**

Phase:

**6D-Q2 — Query-to-PK Selection Prototype**

Validation:

**V1.1 — durable exact-once successor**

Scientific execution is not authorized by creation of this document.

V1 remains frozen, unexecuted, and historically preserved.

V1 must not be executed after V1.1 protocol freeze.

---

## 1. Reason for successor

V1 correctly used exclusive result reservation and no-replace publication,
but its `.partial` pathname was also the exact-once reservation authority.

V1 did not require the newly-created reservation pathname and its parent
directory entry to become durable before scientific evaluation began.

V1.1 strengthens only the execution, durability, provenance, and recovery
contract.

No scientific hypothesis, selector behavior, catalog, query fixture,
evaluation oracle, baseline formula, metric definition, or acceptance
threshold is changed.

V1.1 is therefore a durability-hardened successor, not a scientific redesign.

---

## 2. V1 retirement boundary

Frozen V1 protocol SHA256:

`9bea52de94d8784f6862eee9108afdd1f52f9ff4d4f95eb03fb78d5477e00c11`

Frozen V1 runner SHA256:

`e2e32f85b1dc7015802ec51a6f214188becc5d35f45c76f4b320617ccd6cd873`

V1 result namespace:

`maf_query_to_pk_selection_validation_v1.json`

V1 partial namespace:

`maf_query_to_pk_selection_validation_v1.json.partial`

Both must remain absent.

V1 is classified:

**RETIRED-UNEXECUTED / SCIENTIFIC SLOT UNSPENT / DO NOT ARM**

V1 source files remain immutable historical authorities.

---

## 3. Scientific question

The V1.1 scientific question is exactly the V1 scientific question:

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

## 5. V1.1 files

Protocol:

`experiments/model_fractal/MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_1_PROTOCOL.md`

Future runner:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_1.py`

Future runner SHA authority:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_1.py.sha256`

Future authoritative result:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_1.json`

Future result partial:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_1.json.partial`

Permanent exact-once slot journal:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_1.slot`

Future formal verdict:

`experiments/model_fractal/MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_1_VERDICT.md`

---

## 6. Runner freeze authority

The V1.1 runner does not exist at protocol freeze.

After runner construction and independent static audit:

1. runner bytes are frozen;
2. SHA256 of the exact runner bytes is computed;
3. the `.py.sha256` authority file is created with exactly:
   - 64 lowercase hexadecimal characters;
   - one terminal newline;
   - no additional content;
4. neither file may subsequently change.

Before any reservation, the runner must:

- hash its own `__file__`;
- read the frozen SHA authority;
- require exact equality;
- record that SHA in the authoritative result.

A launcher must independently verify the same runner SHA before supplying
the scientific arm controls.

---

## 7. Scientific-equivalence requirement

V1.1 must not alter V1 scientific behavior.

Before reservation, a static semantic audit must prove equivalence for the
V1 scientific/evaluation surface, including:

- independent query normalization;
- independent query-intent parsing;
- tensor descriptor parsing;
- independent expected-target calculation;
- query-signature construction;
- deterministic random baseline;
- scientific selector invocation;
- metric accumulation;
- query-class semantics;
- threshold constants;
- boundary exclusions.

Harness-only changes are permitted.

No new query may be added.

No query may be removed or edited.

No expected target may be changed.

No candidate budget may be changed.

---

## 8. Permanent slot journal

The V1.1 exact-once reservation authority is not the result partial.

It is the permanent slot journal:

`maf_query_to_pk_selection_validation_v1_1.slot`

The slot journal is append-only for the lifetime of V1.1.

The authoritative runner must never:

- delete it;
- truncate it;
- rename it;
- replace it;
- reuse it;
- recreate it.

Presence of the slot journal means:

**V1.1 MAY NOT BE RUN AGAIN**

regardless of the presence or absence of result or partial files.

---

## 9. Slot creation primitive

The slot journal must be created using exclusive creation semantics equivalent
to:

`O_WRONLY | O_CREAT | O_EXCL | O_APPEND`

with mode:

`0600`

The journal must be created relative to an already-open parent directory
descriptor where supported by the execution environment.

No shell command or subprocess may create the slot.

---

## 10. Initial reservation record

The first journal record must be canonical UTF-8 JSON and contain only frozen
execution identity information.

Its state is exactly:

`RESERVED_DURABLE`

It must bind at least:

- slot schema;
- V1.1 protocol SHA256;
- prior V1 protocol SHA256;
- prior V1 runner SHA256;
- V1.1 runner SHA256;
- selection protocol SHA256;
- selector SHA256;
- catalog SHA256;
- query fixture SHA256;
- source generation manifest SHA256;
- source generation PK;
- final result basename;
- partial result basename.

The record has exactly one terminal newline.

No timestamp is required or authoritative.

---

## 11. Durable reservation barrier

After exclusive journal creation:

1. write the complete initial reservation record;
2. fsync the slot-journal file descriptor;
3. fsync the already-open parent directory descriptor;
4. only after both fsync operations succeed may reservation be classified
   `RESERVED_DURABLE`;
5. only after `RESERVED_DURABLE` may scientific evaluation begin.

This ordering is mandatory:

`PREQUAL -> SLOT_CREATE -> SLOT_WRITE -> SLOT_FSYNC -> DIR_FSYNC -> SCIENCE`

Science before the completed durability barrier is forbidden.

---

## 12. Reservation durability failure

If exclusive slot creation succeeds but either reservation fsync fails:

- science must not begin;
- automatic retry is forbidden;
- V1.1 is conservatively treated as spent/contaminated;
- the event is classified as:
  `RESERVATION_DURABILITY_UNCONFIRMED`;
- the existing slot file, if present, must be preserved;
- a successor protocol/version is required for another scientific attempt.

The runner must never infer that absence after a storage/power failure makes
such an attempted namespace safe to reuse.

---

## 13. Partial result creation

Only after durable slot reservation may the result partial be created.

Partial creation uses exclusive creation.

The partial is a data-publication staging file.

It is not the exact-once authority.

Failure to create or use the partial after durable slot reservation does not
restore the scientific slot.

---

## 14. Scientific execution

The exact scientific selector evaluation occurs only after:

- frozen authorities pass;
- V1 science-equivalence audit passes;
- runner SHA authority passes;
- fixture qualification passes;
- backend qualification passes;
- guard qualification passes;
- durable slot reservation passes;
- partial result staging is available.

No automatic scientific retry exists.

---

## 15. Result write durability

After result construction:

1. canonical result bytes are written completely to the partial;
2. short writes must continue only while positive progress is made;
3. zero or negative write progress is a hard failure;
4. the partial file descriptor is fsynced;
5. the partial descriptor may then be closed.

---

## 16. Publication primitive

Final publication must use only:

`renameat2(..., RENAME_NOREPLACE)`

with:

`RENAME_NOREPLACE = 1`

Source and destination are same-directory siblings.

The same already-open parent directory descriptor is used for both sides.

Forbidden publication fallbacks remain:

- `os.rename`;
- `os.replace`;
- `os.link`;
- libc `link`;
- libc `linkat`;
- shell commands;
- subprocesses.

---

## 17. Post-rename durability barrier

Publication ordering is exactly:

`PARTIAL_FSYNC -> RENAME_NOREPLACE -> PARENT_DIR_FSYNC`

A successful `renameat2` call does not by itself establish durable publication.

Only a successful parent-directory fsync after the rename establishes:

`RESULT_NAME_DURABLE`

---

## 18. Post-rename fsync failure

If rename succeeds but the post-rename parent-directory fsync fails:

- automatic retry is forbidden;
- the slot remains permanently spent;
- no synthetic scientific result may be generated;
- the runner must classify:
  `POST_RENAME_DURABILITY_UNCONFIRMED`;
- it must report whether final and partial pathnames are currently visible;
- it must report any readable final/partial sizes and SHA256 values;
- it must preserve all surviving evidence;
- it must re-raise the original failure.

A visible final file is not silently declared durable.

An absent final file does not make the namespace reusable.

---

## 19. Durable publication journal record

Only after successful post-rename parent-directory fsync may a second
append-only slot-journal record be written.

Its state is exactly:

`PUBLISHED_DURABLE`

It must contain at least:

- result SHA256;
- result byte count;
- final result basename.

The second record is appended to the already durable slot journal.

After append:

- fsync the slot-journal descriptor.

No rewrite of the initial reservation record is permitted.

---

## 20. Journal append failure after durable result publication

If the result rename and parent-directory fsync have both succeeded but
appending/fsyncing the `PUBLISHED_DURABLE` record fails:

- the final result may already be durably published;
- the slot remains spent;
- automatic retry is forbidden;
- classify:
  `PUBLICATION_DURABLE_JOURNAL_COMMIT_FAILED`;
- preserve final result and slot journal;
- re-raise.

A recovery audit may inspect the files.

A recovery audit must not execute science.

---

## 21. Power-loss recovery invariant

Once `RESERVED_DURABLE` has been established, exact-once safety does not
depend on the partial or final pathname.

The permanent slot journal remains the spending authority.

Therefore these recovery states are all non-runnable:

- slot + partial;
- slot + final;
- slot only;
- slot + partial + final;
- slot with complete publication record;
- slot with incomplete/torn trailing publication record.

No state containing the durable slot authority permits automatic rerun.

---

## 22. Torn journal handling

The first reservation record must be completely written and fsynced before
science.

A malformed or torn trailing second journal record is therefore a
post-reservation condition.

It must be classified as publication/recovery uncertainty.

It must never cause the initial durable reservation record to be ignored.

---

## 23. Pre-reservation failures

Failures before successful slot creation remain non-spending.

Examples include:

- frozen SHA mismatch;
- V1 historical authority mismatch;
- runner self-SHA mismatch;
- science-equivalence mismatch;
- malformed catalog;
- malformed query fixture;
- backend qualification failure;
- guard failure;
- readiness failure.

These must leave V1.1 slot, result, and partial absent.

---

## 24. Dual-arm execution

V1.1 authoritative science requires a new V1.1-specific environment arm and
a new V1.1-specific CLI arm.

V1 arm values must not authorize V1.1.

The future runner freezes their exact names and values.

Environment-only must refuse without slot creation.

CLI-only must refuse without slot creation.

Guard-false must refuse without slot creation.

---

## 25. Scientific metrics

The V1.1 metric keys are exactly unchanged from V1:

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

## 26. Acceptance thresholds

Thresholds are exactly unchanged from V1:

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

No threshold may be weakened.

---

## 27. Result schema

Schema identifier:

`openmind.maf_query_to_pk_selection_validation.v1_1`

Exact top-level fields are:

1. `schema`
2. `exact_once`
3. `validation_protocol_sha256`
4. `prior_v1_protocol_sha256`
5. `prior_v1_runner_sha256`
6. `selection_protocol_sha256`
7. `implementation_sha256`
8. `q1_verdict_sha256`
9. `catalog_sha256`
10. `query_fixture_sha256`
11. `source_generation_pk`
12. `source_manifest_sha256`
13. `selection_config_sha256`
14. `validation_runner_sha256`
15. `random_baseline_seed`
16. `expected_check_count`
17. `check_count`
18. `checks`
19. `failed_checks`
20. `auditor_error`
21. `all_pass`
22. `metrics`
23. `acceptance_thresholds`
24. `boundary_exclusions`
25. `publication_backend`

No additional top-level fields are permitted.

---

## 28. Result canonicalization

Canonical JSON rules remain:

- UTF-8;
- `sort_keys=True`;
- `separators=(",", ":")`;
- `ensure_ascii=False`;
- exactly one terminal newline.

Non-finite floating-point values are forbidden.

The runner must serialize with behavior equivalent to:

`allow_nan=False`

---

## 29. Exact V1.1 check matrix

Expected check count:

`62`

Exact ordered IDs:

`V01_prior_v1_protocol_binding`
`V02_prior_v1_runner_binding`
`V03_q2_protocol_binding`
`V04_selector_implementation_binding`
`V05_q1_acceptance_verdict_binding`
`V06_catalog_schema`
`V07_catalog_canonical_json`
`V08_catalog_generation_manifest_binding`
`V09_catalog_unique_sorted_object_pks`
`V10_catalog_static_metadata_surface_only`
`V11_selection_config_exact`
`V12_query_fixture_schema`
`V13_query_fixture_canonical_json`
`V14_evaluation_query_minimum`
`V15_specific_query_minimum`
`V16_distinct_specific_target_minimum`
`V17_fallback_control_minimum`
`V18_query_id_uniqueness_and_order`
`V19_query_class_semantics`
`V20_selector_api_non_oracle`
`V21_no_route_cache_input`
`V22_no_bounded_expansion`
`V23_no_inference_network_or_subprocess`
`V24_independent_target_predicate`
`V25_target_predicate_does_not_call_selector`
`V26_random_baseline_exact_seed_and_formula`
`V27_random_baseline_no_oracle_input`
`V28_v1_science_semantic_equivalence`
`V29_runner_self_sha_authority`
`V30_renameat2_backend_required`
`V31_rename_noreplace_exact_value`
`V32_no_link_publication`
`V33_no_replace_or_rename_fallback`
`V34_dual_arm_required`
`V35_guard_false_non_spending`
`V36_fixture_qualification_before_slot`
`V37_backend_qualification_before_slot`
`V38_slot_journal_name_and_schema`
`V39_slot_o_excl_append_reservation`
`V40_slot_initial_record_complete`
`V41_slot_file_fsync_before_science`
`V42_slot_parent_fsync_before_science`
`V43_science_after_durable_slot_only`
`V44_partial_o_excl_after_durable_slot`
`V45_partial_file_fsync_before_publication`
`V46_no_replace_result_publication`
`V47_parent_directory_fsync_after_rename`
`V48_published_record_after_directory_fsync`
`V49_slot_journal_fsync_after_published_record`
`V50_slot_journal_never_deleted_or_replaced`
`V51_failure_classifier_distinguishes_rename_state`
`V52_post_rename_durability_failure_no_retry`
`V53_reservation_durability_failure_retires_namespace`
`V54_exact_once_no_retry_contract`
`V55_result_schema_and_canonical_json`
`V56_result_authority_bindings`
`V57_supported_intent_target_hit_threshold`
`V58_supported_intent_precision_threshold`
`V59_specific_top1_threshold`
`V60_random_baseline_advantage_threshold`
`V61_budget_duplicate_and_binding_thresholds`
`V62_boundary_exclusions`

No check may be removed, renamed, reordered, or added after runner freeze.

---

## 30. Failure-state model

The runner must distinguish at least:

`PRE_RESERVATION_FAILURE`

`RESERVATION_DURABILITY_UNCONFIRMED`

`RESERVED_DURABLE_PRE_SCIENCE_FAILURE`

`SCIENTIFIC_EVALUATION_FAILURE`

`RESULT_CONSTRUCTION_FAILURE`

`PARTIAL_WRITE_OR_FSYNC_FAILURE`

`RENAME_NOREPLACE_FAILURE`

`POST_RENAME_DURABILITY_UNCONFIRMED`

`PUBLICATION_DURABLE_JOURNAL_COMMIT_FAILED`

`PUBLISHED_DURABLE`

Every state after slot creation forbids automatic scientific retry.

---

## 31. Boundary exclusions

V1.1 preserves the exact V1 exclusions:

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

## 32. Negative-result policy

Scientific failure remains evidence.

No failed V1.1 result may be rescued by:

- editing the selector;
- changing catalog bytes;
- changing query bytes;
- changing expected-target logic;
- changing thresholds;
- increasing the candidate budget;
- retrying V1.1;
- deleting its slot journal.

A successor protocol is required.

---

## 33. Construction order

After this protocol is frozen:

1. independently audit this protocol;
2. freeze its SHA256;
3. construct V1.1 runner only;
4. statically compare V1.1 science logic with frozen V1 science logic;
5. audit all durability and failure-state paths;
6. freeze runner bytes;
7. create and freeze runner SHA authority file;
8. perform non-spending static/readiness checks;
9. update current-facing documentation;
10. publish all frozen authorities to remote;
11. independently verify local/remote hashes;
12. only then consider one V1.1 authoritative execution.

---

## 34. Current authorization

At protocol freeze:

**V1 SCIENCE: FORBIDDEN / RETIRED-UNEXECUTED**

**V1 RESULT SLOT: UNSPENT**

**V1.1 SCIENCE: NOT AUTHORIZED**

**V1.1 SLOT: MUST NOT EXIST**

**V1.1 RUNNER: MUST NOT EXIST**

The next authorized activity is:

**STATIC AUDIT AND FREEZE OF THIS V1.1 PROTOCOL, THEN RUNNER CONSTRUCTION**

