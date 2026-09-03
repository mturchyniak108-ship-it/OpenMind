# MAF Query-to-PK Selection Validation V1 Protocol

## Status

**PREREGISTERED PROSPECTIVE SCIENTIFIC VALIDATION**

Phase:

**6D-Q2 — Query-to-PK Selection Prototype**

Validation:

**V1**

Scientific execution is not authorized by creation of this document.

---

## 1. Scientific question

Can the exact frozen Phase 6D-Q2 V1 selector use only query-derived signals
and immutable static object metadata to select bounded MAF object-PK
candidates under the preregistered non-oracle contract?

This validation tests metadata-intent routing only.

It does not test selective inference sufficiency.

---

## 2. Frozen upstream authorities

Q2 selection protocol SHA256:

`b42a0643976c2393871e3b826ba5573b4de981b49603de63230d69cf57be0811`

Q2 selector implementation SHA256:

`e21c05e352fe921b791e8c936425727a98911ce7566989672a96bfd2b9613fa2`

Q1 scientific acceptance verdict SHA256:

`c396346adfc3d7aed08373a52d02e88ce14b2195269c9d090c2572828db77615`

The validation runner must reject any authority mismatch before scientific
result reservation.

---

## 3. Validation authorities to be frozen later

The following files do not exist at protocol freeze time.

They must be separately constructed, independently audited, and frozen before
the authoritative scientific run.

Candidate catalog:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_catalog.json`

Prospective query fixture:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_queries.json`

Validation runner:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1.py`

Authoritative result:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1.json`

Formal verdict:

`experiments/model_fractal/MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_VERDICT.md`

---

## 4. Validation catalog

The validation catalog must satisfy the exact frozen Q2 catalog schema:

`openmind.maf_query_pk_catalog.v1`

It must be canonical JSON with no trailing newline.

Its SHA256 becomes a frozen validation authority.

The catalog must bind one exact:

- source generation PK;
- source manifest SHA256.

The catalog must contain only the Q2-authorized static metadata surface:

- object PK;
- tensor name;
- tensor type;
- dimensions;
- element count.

It must not contain answer, execution, route-cache, locality, cache,
residency, offset, segment-path, or benchmark-label information.

---

## 5. Catalog construction boundary

Catalog construction is non-scientific preparation.

It may inspect frozen immutable MAF model/object authorities needed to
construct the protocol-defined catalog.

It must not:

- execute the Q2 selector;
- execute inference;
- consult expected answers;
- inspect reference execution traces;
- use touched-object telemetry;
- use route-cache information;
- perform bounded expansion.

The frozen catalog must precede construction of the prospective evaluation
query fixture.

---

## 6. Prospective query fixture schema

Schema identifier:

`openmind.maf_query_to_pk_selection_validation_queries.v1`

Exact top-level fields:

1. `schema`
2. `source_generation_pk`
3. `source_manifest_sha256`
4. `catalog_sha256`
5. `selection_config`
6. `random_baseline_seed`
7. `queries`

No additional fields are permitted.

---

## 7. Selection configuration

`selection_config` must satisfy the frozen Q2 configuration schema:

`openmind.maf_query_to_pk_selection_config.v1`

The validation configuration must be frozen before runner construction.

`max_candidates` must remain within the Q2 protocol range:

`1 <= max_candidates <= 32`

The configuration must use exactly:

- `nfkc_casefold_v1`
- `metadata_intent_alias_v1`
- `tensor_name_descriptor_v1`
- `metadata_subset_rank_v1`
- `sha256_rendezvous_v1`

---

## 8. Random baseline

The query fixture must contain exactly:

`OPENMIND_6D_Q2_V1_RANDOM_BASELINE`

as `random_baseline_seed`.

The baseline formula is exactly the Q2 protocol formula:

`sha256(seed + "\0" + query_signature + "\0" + object_pk)`

Baseline ranking is ascending digest then ascending object PK.

The baseline receives the same candidate budget as the tested selector.

It must not receive expected targets.

---

## 9. Query entry schema

Each query fixture entry contains exactly:

1. `query_id`
2. `query_text`
3. `query_class`

No expected object PK may be stored in the query entry.

No answer text may be stored in the query entry.

---

## 10. Query IDs

`query_id` must be a unique non-empty ASCII identifier.

Authoritative fixture order is ascending lexical `query_id`.

Duplicate IDs are forbidden.

---

## 11. Query classes

The exact permitted query classes are:

- `specific_intent`
- `multi_target_intent`
- `fallback_control`

A specific-intent query must have exactly one independently determined
metadata target.

A multi-target-intent query must have two or more independently determined
metadata targets.

A fallback-control query must have zero metadata-eligible targets.

---

## 12. Prospective fixture minimums

Before the scientific result namespace is reserved, fixture qualification
must prove:

- total evaluation queries >= 32;
- specific-intent queries >= 16;
- distinct expected object PKs across specific-intent queries >= 8;
- fallback-control queries >= 4.

If the frozen catalog cannot support these minimums, validation must stop
before exact-once reservation.

The minimums may not be weakened afterward.

---

## 13. Independent expected-target oracle

The validation harness may compute expected metadata target sets.

Those expected sets are evaluation-only oracle information.

They must be computed by an implementation independent of the selector's
candidate-ranking function.

The target oracle may use:

- query text;
- frozen query grammar;
- frozen alias table;
- frozen tensor-name descriptor grammar;
- frozen catalog.

The target oracle must not call:

- `select_query_to_pks_v1`;
- selector candidate-ranking helpers;
- selector fallback-ranking helpers.

---

## 14. Selector input firewall

For every scientific evaluation query, the selector receives exactly:

- query text;
- frozen catalog;
- frozen selector configuration;
- frozen source generation PK;
- frozen source manifest SHA256.

It must not receive:

- expected target PKs;
- expected answers;
- answer tokens;
- logits;
- hidden states;
- reference execution data;
- touched-object telemetry;
- route-cache state;
- pass/fail labels.

---

## 15. Specific-intent target definition

A specific-intent target is established only when the independent target
predicate identifies exactly one metadata-eligible catalog object.

If independent qualification identifies zero or multiple targets for a query
marked `specific_intent`, fixture qualification must fail before scientific
reservation.

---

## 16. Multi-target definition

A query marked `multi_target_intent` must independently resolve to at least
two metadata-eligible catalog objects.

Zero or one target is a fixture qualification failure.

---

## 17. Fallback-control definition

A query marked `fallback_control` must independently resolve to zero
metadata-eligible objects.

The selector must report:

`fallback_used = true`

for every qualified fallback-control query.

Fallback-control queries are excluded from supported-intent precision and
target-hit calculations.

---

## 18. Supported-intent set

The supported-intent evaluation set is the union of:

- specific-intent queries;
- multi-target-intent queries.

Fallback controls are excluded.

---

## 19. Supported-intent target-hit rate

For each supported-intent query:

`hit = selected_set intersects expected_target_set`

Target-hit rate is:

`sum(hit) / supported_intent_query_count`

Acceptance requires:

`1.0`

---

## 20. Supported-intent precision

Across supported-intent queries:

`precision = total_selected_expected / total_selected`

where each selected PK is expected only if it belongs to that query's
independently computed expected target set.

Acceptance requires:

`1.0`

No unrelated budget filling is therefore permitted.

---

## 21. Specific-intent top-1 accuracy

For every specific-intent query, the first selected object PK must be
compared with its one independent expected object PK.

Accuracy is:

`correct_top1 / specific_intent_query_count`

Acceptance requires:

`>= 0.95`

---

## 22. Random-baseline top-1 accuracy

The deterministic random baseline selects the first candidate from its
protocol-defined ranking.

It uses no expected-target information.

Its specific-intent top-1 accuracy must be reported.

---

## 23. Selector-minus-baseline difference

Compute:

`selector_specific_top1 - random_baseline_specific_top1`

Acceptance requires:

`>= 0.50`

---

## 24. Candidate-count metrics

The result must report:

- mean selected-candidate count;
- maximum selected-candidate count.

Every selection must satisfy the frozen candidate budget.

---

## 25. Structural violation metrics

The result must report counts for:

- candidate-budget violations;
- duplicate selected PKs;
- generation-binding violations;
- manifest-binding violations;
- oracle-input violations.

Acceptance requires all five counts to equal zero.

---

## 26. Required scientific metrics

The authoritative result must report exactly these metric keys:

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

No post-hoc metric substitution is permitted.

---

## 27. Acceptance thresholds

The frozen scientific thresholds are exactly:

- evaluation query count >= 32;
- specific-intent query count >= 16;
- unique specific-intent expected object PKs >= 8;
- supported-intent target-hit rate = 1.0;
- supported-intent precision = 1.0;
- specific-intent top-1 accuracy >= 0.95;
- selector-minus-baseline top-1 difference >= 0.50;
- budget violation count = 0;
- duplicate selection count = 0;
- generation-binding violation count = 0;
- manifest-binding violation count = 0;
- oracle-input violation count = 0.

Every required structural validation check must also pass.

---

## 28. Negative-result policy

Failure of any frozen threshold is a scientific negative result.

The validation must not be rescued by:

- modifying the selector;
- modifying catalog contents after scientific execution;
- changing query text;
- replacing failed queries;
- weakening thresholds;
- increasing the candidate budget above the frozen configuration;
- adding route-cache data;
- using reference execution;
- adding bounded expansion.

A successor protocol is required for any redesign.

---

## 29. Exact scientific check matrix

The validation check IDs are exactly:

`V01` through `V48`.

Expected check count:

`48`

The runner must emit exactly one ordered record for each ID.

No additional scientific check IDs may be introduced after runner freeze.

---

## 30. V01-V08 — frozen authority and catalog checks

- `V01_q2_protocol_binding`
- `V02_selector_implementation_binding`
- `V03_q1_acceptance_verdict_binding`
- `V04_catalog_schema`
- `V05_catalog_canonical_json`
- `V06_catalog_generation_manifest_binding`
- `V07_catalog_unique_sorted_object_pks`
- `V08_catalog_static_metadata_surface_only`

---

## 31. V09-V17 — query fixture qualification

- `V09_selection_config_exact`
- `V10_query_fixture_schema`
- `V11_query_fixture_canonical_json`
- `V12_evaluation_query_minimum`
- `V13_specific_query_minimum`
- `V14_distinct_specific_target_minimum`
- `V15_fallback_control_minimum`
- `V16_query_id_uniqueness_and_order`
- `V17_query_class_semantics`

---

## 32. V18-V25 — non-oracle and independent evaluation

- `V18_selector_api_non_oracle`
- `V19_no_route_cache_input`
- `V20_no_bounded_expansion`
- `V21_no_inference_network_or_subprocess`
- `V22_independent_target_predicate`
- `V23_target_predicate_does_not_call_selector`
- `V24_random_baseline_exact_seed_and_formula`
- `V25_random_baseline_no_oracle_input`

---

## 33. V26-V37 — exact-once publication harness

- `V26_renameat2_backend_required`
- `V27_rename_noreplace_exact_value`
- `V28_no_os_link_publication`
- `V29_no_link_or_linkat_fallback`
- `V30_no_replace_or_plain_rename_fallback`
- `V31_dual_arm_required`
- `V32_guard_false_non_spending`
- `V33_fixture_qualification_before_reservation`
- `V34_backend_qualification_before_reservation`
- `V35_o_excl_partial_reservation`
- `V36_matrix_after_reservation`
- `V37_no_replace_result_publication`

---

## 34. V38-V48 — result, metrics, and scientific disposition

- `V38_partial_file_fsync_before_publication`
- `V39_parent_directory_fsync_after_publication`
- `V40_result_schema_and_canonical_json`
- `V41_result_authority_bindings`
- `V42_supported_intent_target_hit_threshold`
- `V43_supported_intent_precision_threshold`
- `V44_specific_top1_threshold`
- `V45_random_baseline_advantage_threshold`
- `V46_budget_duplicate_and_binding_thresholds`
- `V47_boundary_exclusions`
- `V48_exact_once_no_retry_contract`

---

## 35. Result schema

Authoritative result schema identifier:

`openmind.maf_query_to_pk_selection_validation.v1`

Exact top-level result fields:

1. `schema`
2. `exact_once`
3. `validation_protocol_sha256`
4. `selection_protocol_sha256`
5. `implementation_sha256`
6. `q1_verdict_sha256`
7. `catalog_sha256`
8. `query_fixture_sha256`
9. `source_generation_pk`
10. `source_manifest_sha256`
11. `selection_config_sha256`
12. `random_baseline_seed`
13. `expected_check_count`
14. `check_count`
15. `checks`
16. `failed_checks`
17. `auditor_error`
18. `all_pass`
19. `metrics`
20. `acceptance_thresholds`
21. `boundary_exclusions`
22. `publication_backend`

No additional top-level fields are permitted.

---

## 36. Result canonicalization

The result is canonical UTF-8 JSON using:

- `sort_keys=True`
- `separators=(",", ":")`
- `ensure_ascii=False`

The authoritative result has exactly one terminal newline.

---

## 37. Exact-once namespace

Final result:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1.json`

Reserved partial:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1.json.partial`

The partial pathname is the exact-once reservation authority.

Creation must use exclusive creation semantics.

If either final or partial exists before the scientific run, execution must
refuse.

---

## 38. Dual-arm requirement

Scientific execution requires both:

1. the exact V1 arm environment variable defined by the future frozen runner;
2. the exact scientific CLI arm flag defined by the future frozen runner.

Environment-only arming must fail without spending the result slot.

CLI-only arming must fail without spending the result slot.

Guard-false execution must remain non-spending.

---

## 39. Pre-reservation qualification

Before partial result reservation, the runner must prove:

- all frozen SHA authorities;
- catalog qualification;
- query fixture qualification;
- independent target minimums;
- actual publication-backend qualification.

Failure before reservation must leave the scientific result slot unspent.

---

## 40. Publication backend

The result publication primitive is:

`libc.renameat2(..., RENAME_NOREPLACE)`

`RENAME_NOREPLACE` is exactly integer `1`.

The source partial and destination result must be same-directory sibling
names using the same already-open parent directory descriptor.

---

## 41. Publication durability

Before publication:

- complete result bytes must be written;
- the result partial file must be flushed;
- the result partial file descriptor must be fsynced.

After successful rename-no-replace publication:

- the parent directory descriptor must be fsynced.

---

## 42. Forbidden publication primitives

Executable result publication must not use:

- `os.link`;
- libc `link`;
- libc `linkat`;
- `os.replace`;
- plain `os.rename`;
- shell commands;
- subprocess publication.

No weaker fallback is permitted.

If `renameat2(RENAME_NOREPLACE)` is unavailable, validation must fail
explicitly before scientific reservation when detected during required
backend qualification.

---

## 43. Collision behavior

A non-spending backend qualification must prove on the actual filesystem:

- successful rename-no-replace publication;
- byte preservation;
- inode preservation;
- successful directory fsync;
- collision rejection;
- incumbent final preservation;
- unpublished partial preservation on collision.

The scientific result slot must remain unspent during this qualification.

---

## 44. No automatic retry

Once scientific partial reservation succeeds, the V1 slot is permanently
spent.

Automatic retry is forbidden.

A published result must never be rerun.

A post-reservation partial result must be preserved exactly and classified.

---

## 45. Boundary exclusions

The result must explicitly record that Q2 V1 does not execute or establish:

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

## 46. Scientific interpretation

A successful result means only:

**bounded non-oracle metadata-intent query-to-PK candidate selection is
validated under the frozen Q2 V1 benchmark contract.**

It does not establish that those selected PKs form a sufficient model working
set.

---

## 47. Phase progression

If V1 passes and a formal acceptance verdict is frozen:

**Phase 6D-Q2 is accepted and closed.**

Then:

**Phase 6D-Q3 becomes the next gate.**

Phase 6E-A remains blocked until Q1, Q2, Q3, and Q4 are all closed.

---

## 48. Construction authorization

After this validation protocol is frozen, the next authorized work is:

1. discover the authoritative validation-catalog source;
2. construct and independently audit the exact validation catalog;
3. freeze catalog bytes;
4. construct the prospective query fixture from the frozen catalog;
5. independently audit and freeze query-fixture bytes;
6. build the validation runner.

Scientific selector evaluation is still not authorized.

---

## 49. Scientific execution authorization

Scientific execution becomes authorizable only after:

- catalog frozen;
- query fixture frozen;
- validation runner frozen;
- backend qualification passed non-spending;
- fixture qualification passed non-spending;
- guard-false passed;
- both half-arm controls passed;
- final exact-once source/namespace readiness passed.

Only then may one authoritative V01-V48 execution occur.

---

## 50. Final nonclaims

This protocol does not establish:

- arbitrary natural-language semantic routing;
- inference sufficiency;
- answer correctness;
- answer parity;
- actual avoided reads;
- RAM reduction;
- latency reduction;
- throughput improvement;
- MAF-native compute.

---

## 51. Next gate

After protocol freeze:

**DISCOVER AND FREEZE THE Q2 VALIDATION CATALOG AUTHORITY**

No scientific selector execution is authorized.
