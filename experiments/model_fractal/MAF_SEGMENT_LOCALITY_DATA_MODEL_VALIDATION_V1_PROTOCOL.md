# MAF Segment Locality Data Model Validation V1 Protocol

Status: PROSPECTIVE PREREGISTRATION
Phase: 6D
Validation target: MAF Segment Locality Data Model V1
Scientific execution authorized by protocol freeze: NO
Benchmark execution: FORBIDDEN
Performance verdict: NONE

## 1. Purpose

This protocol prospectively defines the scientific validation of the frozen
Phase 6D locality data-model implementation.

No validation result exists at protocol freeze time.

The validation runner must be implemented and frozen separately before any
scientific invocation is permitted.

## 2. Frozen parent commit

Branch:

`labs/multidimensional-maf`

Parent commit:

`e0c7fce8b10429fe8a85f88bf839f3b8737f6afa`

## 3. Frozen implementation target

Implementation:

`experiments/model_fractal/maf_segment_locality_data_model_v1.py`

Implementation SHA256:

`5432f2d74a610f2d0f9181e9af146013bb198a4e837af634993909358fff8ad0`

The implementation is immutable for Validation V1.

Validation V1 may inspect and import those exact bytes but may not modify them.

## 4. Frozen data-model protocol

Protocol:

`experiments/model_fractal/MAF_SEGMENT_LOCALITY_DATA_MODEL_V1_PROTOCOL.md`

SHA256:

`712caa2e7dfc948f607a4c8d68064fc838eb1f58701fc5206c52aaf8e6492bc4`

The implementation and validation must remain within this frozen semantic
boundary.

## 5. Parent Phase 6D protocol

Protocol:

`experiments/model_fractal/MAF_SEGMENT_LOCALITY_REPACKING_V1_PROTOCOL.md`

SHA256:

`a4c1a1d4fe22f7e714efa331cec9cf4dbd3a9e178f2b28b3ddb9034387e210ae`

## 6. Frozen Phase 6C runtime

Runtime:

`experiments/model_fractal/maf_object_runtime_residency_v1.py`

SHA256:

`4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9`

Phase 6C remains closed and immutable.

Validation V1 must not edit, rewrite, monkey-patch, or replace this file.

## 7. Validation runner path

The future validation runner path is exactly:

`experiments/model_fractal/maf_segment_locality_data_model_validation_v1.py`

The runner does not exist at this protocol freeze.

## 8. Raw result path

The exact raw result path is:

`experiments/model_fractal/maf_segment_locality_data_model_validation_v1.json`

The result does not exist at this protocol freeze.

## 9. Result schema

The exact result schema must be:

`openmind.maf_segment_locality_data_model_validation.v1`

## 10. Exact-once rule

The first scientific invocation of the frozen Validation V1 runner permanently
spends the V1 validation slot whether it:

- passes;
- fails;
- raises a validation-harness exception;
- crashes;
- is interrupted after invocation begins.

A spent V1 runner must never be edited and rerun as V1.

Any correction requires a prospectively preregistered successor version.

## 11. Raw-result freeze rule

After scientific execution, the raw result artifact must be frozen in Git
before interpretation.

Failure residue must not be silently deleted or repaired.

## 12. No benchmark

Validation V1 is correctness validation only.

It must not report:

- latency;
- throughput;
- speedup;
- cache performance;
- storage performance;
- memory-performance superiority;
- device-performance superiority.

`benchmark_executed` must be false.

Performance verdict remains NONE.

## 13. No runtime integration

Validation V1 must not integrate telemetry with the Phase 6C runtime.

It validates the standalone Phase 6D data-model module only.

Runtime observer/adapter work remains a later separately preregistered gate.

## 14. No repack realization

Validation V1 must not:

- build segments;
- build generations;
- activate generations;
- repack persistent model data;
- alter an active generation.

Repack realization remains unauthorized.

## 15. Synthetic scientific fixtures

Validation V1 may construct deterministic in-memory synthetic PKs and aggregate
fixtures.

Synthetic PKs must use valid frozen PK syntax and deterministic fixed
hexadecimal suffixes.

No source GGUF, model download, network access, or large external fixture is
required.

## 16. Metric fixture requirements

The runner must preregister its exact synthetic placement and transition
fixtures in source before execution.

The runner may not choose a fixture after observing a computed metric result.

Independent expected numerators and denominators must be literal or derived by
a separately coded reference calculation that does not call the metric under
test.

## 17. Snapshot reproducibility

Snapshot reproducibility must compare independently created valid accumulator
states representing the same semantic event history.

The runner must not establish reproducibility merely by hashing the same Python
object twice.

## 18. Plan reproducibility

Plan reproducibility must compare independently constructed valid RepackPlan
objects representing identical semantics.

The runner must not establish reproducibility merely by hashing the same plan
object twice.

## 19. Failure atomicity

V26 must compare snapshot identity before and after a rejected event.

The rejected event must be rejected before scientific state commitment.

## 20. Import-time side-effect test

V50 must perform module import in an isolated child Python process.

The observation directory must be empty before import.

After successful import, the runner must verify that the directory inventory is
unchanged.

The child import may create ordinary interpreter state in memory.

It must not create a file in the observation directory.

## 21. Phase 6C immutability check

V49 must hash the frozen Phase 6C runtime immediately before and immediately
after the validation test body.

Both identities must equal:

`4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9`

## 22. Mandatory result fields

The raw validation result must contain at minimum:

- `schema`;
- `validation_valid`;
- `all_pass`;
- `checks`;
- `failed_checks`;
- `fatal_error`;
- `benchmark_executed`;
- `performance_verdict`;
- `implementation_path`;
- `implementation_sha256`;
- `protocol_path`;
- `protocol_sha256`;
- `phase6c_engine_sha256`;
- `check_count`.

## 23. Valid successful result

A successful accepted V1 result requires:

- `validation_valid = true`;
- `all_pass = true`;
- `check_count = 50`;
- checks exactly V01 through V50;
- every check passes;
- `failed_checks = []`;
- `fatal_error = null`;
- `benchmark_executed = false`;
- `performance_verdict = null`;
- exact implementation SHA binding;
- exact validation protocol SHA binding;
- exact Phase 6C SHA binding.

## 24. Harness failure

If the runner cannot validly execute the frozen test matrix, it must return a
raw result with:

- `validation_valid = false`;
- `all_pass = false`;
- a non-null fatal error description.

A harness failure is not an implementation correctness verdict.

The exact-once slot is still spent after invocation.

## 25. Scientific validation matrix

### V01_module_binding

Bind the imported validation target to the exact frozen module SHA256 and the exact frozen data-model protocol SHA256. Any mismatch invalidates the entire validation before semantic checks begin.

### V02_canonical_json_determinism

Equivalent JSON-compatible values must produce byte-identical canonical JSON independent of input mapping insertion order. Canonical bytes must contain no trailing newline.

### V03_plain_integer_validation

Reject boolean, negative, and otherwise invalid values wherever the frozen protocol requires a plain non-negative integer.

### V04_exact_event_kind_surface

TelemetryEventKind must expose exactly ACCESS, MATERIALIZATION, BYTES_READ, CACHE_HIT, CACHE_MISS, PROMOTION, DEMOTION, PREFETCH_ISSUED, PREFETCH_CONSUMED, and PREFETCH_UNUSED.

### V05_event_field_combinations

Accept valid event-field combinations and reject forbidden non-null fields for each event kind.

### V06_strict_sequence_enforcement

After one committed event, reject an event with a lower sequence number without changing committed accumulator state.

### V07_duplicate_sequence_rejection

Reject reuse of the last committed sequence number without changing committed accumulator state.

### V08_access_counting

Accepted ACCESS events increment exactly the addressed object's access count and the global access-event count.

### V09_self_transition_counting

Two consecutive ACCESS events for the same object create exactly one directed self-transition.

### V10_directed_transition_counting

Consecutive ACCESS A then ACCESS B increments A->B exactly once and does not silently increment B->A.

### V11_non_access_preserves_access_adjacency

Non-ACCESS events between ACCESS A and ACCESS B must not break the derived A->B access transition.

### V12_first_access_reuse_behavior

The first ACCESS to an object produces no reuse interval and leaves reuse count zero, sum zero, and min/max null.

### V13_reuse_interval_count

Each ACCESS after the first ACCESS to the same object increments reuse interval count exactly once.

### V14_reuse_interval_sum

Reuse interval sum equals the exact sum of logical sequence differences between consecutive ACCESS events to the same object.

### V15_reuse_interval_min

Reuse interval minimum equals the smallest observed logical sequence difference for that object.

### V16_reuse_interval_max

Reuse interval maximum equals the largest observed logical sequence difference for that object.

### V17_materialization_independence

MATERIALIZATION increments only materialization accounting and must not implicitly increment access, bytes-read, cache, or residency counters.

### V18_bytes_read_accounting

BYTES_READ adds exactly the supplied non-negative byte count to the addressed object's runtime-attributed bytes-read aggregate.

### V19_named_cache_hit_accounting

CACHE_HIT increments only the exact cache-name/object-PK hit aggregate.

### V20_named_cache_miss_accounting

CACHE_MISS increments only the exact cache-name/object-PK miss aggregate.

### V21_residency_transition_aggregation

PROMOTION and DEMOTION observations aggregate by exact object PK, from state, and to state without redefining Phase 6C transition legality.

### V22_prefetch_issue_accounting

PREFETCH_ISSUED increments issued accounting exactly once and records the prefetch ID as unresolved.

### V23_prefetch_consumed_accounting

PREFETCH_CONSUMED resolves a matching previously issued ID exactly once and increments consumed accounting.

### V24_prefetch_unused_accounting

PREFETCH_UNUSED resolves a matching previously issued ID exactly once and increments unused accounting.

### V25_duplicate_prefetch_terminal_rejection

A prefetch ID already resolved as consumed or unused must reject a second terminal resolution without changing committed state.

### V26_invalid_event_failure_atomicity

For a representative invalid event, snapshot identity immediately after failure must equal snapshot identity immediately before failure.

### V27_empty_snapshot_semantics

A new accumulator produces event_count=0, access_event_count=0, null sequence bounds, and all aggregate tuples empty.

### V28_nonempty_sequence_bounds

A non-empty snapshot exposes the exact first and last committed logical sequence numbers and the exact accepted event count.

### V29_deterministic_snapshot_ordering

Snapshot object, transition, cache, residency, and prefetch aggregate collections must appear in the exact canonical lexical ordering defined by the protocol.

### V30_snapshot_payload_reproducibility

Equivalent frozen snapshot state created through different valid insertion patterns must produce equal snapshot_payload output.

### V31_snapshot_sha_reproducibility

Equivalent frozen snapshots must produce the same snapshot_sha256, and the result must equal an independently computed SHA256 over canonical snapshot payload bytes.

### V32_zero_denominator_metric_rejection

Each locality metric requiring transition weight must reject a zero total transition denominator rather than return zero, NaN, or infinity.

### V33_weighted_rank_distance_exactness

For a preregistered synthetic transition/placement fixture, weighted transition rank distance numerator and denominator must equal independently calculated exact integers.

### V34_cross_segment_fraction_exactness

For the same frozen fixture, cross-segment numerator and denominator must equal independently calculated exact integers.

### V35_co_segment_fraction_exactness

For the same frozen fixture, co-segment numerator and denominator must equal independently calculated exact integers.

### V36_cross_co_complement

For non-zero transition weight, cross-segment numerator plus co-segment numerator must equal their common denominator.

### V37_placement_uniqueness

Reject duplicate object PKs and reject duplicate (target_segment_ordinal,target_object_ordinal) coordinates.

### V38_contiguous_segment_ordinals

Reject a placement plan whose target segment ordinals do not form the contiguous zero-based range required by V1.

### V39_contiguous_object_ordinals

Reject a placement plan whose object ordinals inside any target segment do not form a contiguous zero-based range.

### V40_exact_source_object_set_preservation

validate_complete_source_object_set must accept an exact complete set and reject missing, extra, or duplicate source object identities.

### V41_deterministic_planner_config_ordering

RepackPlan accepts planner configuration only in the protocol's canonical lexical key ordering and preserves that deterministic ordering in payload.

### V42_duplicate_planner_config_key_rejection

Reject duplicate planner configuration keys.

### V43_source_generation_binding

Plan payload must preserve exactly the supplied model PK, source generation PK, and source manifest SHA256.

### V44_telemetry_snapshot_binding

Plan payload must preserve exactly the supplied telemetry snapshot SHA256.

### V45_deterministic_plan_ordering

RepackPlan must reject non-canonical placement ordering and preserve canonical segment/object ordering in its payload.

### V46_plan_payload_reproducibility

Equivalent valid plans must produce byte-for-byte equivalent canonical repack_plan_payload structures.

### V47_plan_sha_reproducibility

Equivalent valid plans must produce the same repack_plan_sha256 and equal an independently computed SHA256 over canonical plan payload bytes.

### V48_no_payload_mutation_surface

The frozen module must expose no API field/function for replacement payload bytes, changed object PKs, generation activation, segment construction, or generation construction.

### V49_phase6c_source_immutability

The exact Phase 6C runtime file SHA256 must be unchanged before and after the scientific validation invocation.

### V50_import_time_side_effect_absence

Importing the frozen data-model module in an isolated child process must not create or modify files inside a preregistered empty observation directory and must return successfully.

## 26. Required check set

The exact ordered check names are:

01. `V01_module_binding`
02. `V02_canonical_json_determinism`
03. `V03_plain_integer_validation`
04. `V04_exact_event_kind_surface`
05. `V05_event_field_combinations`
06. `V06_strict_sequence_enforcement`
07. `V07_duplicate_sequence_rejection`
08. `V08_access_counting`
09. `V09_self_transition_counting`
10. `V10_directed_transition_counting`
11. `V11_non_access_preserves_access_adjacency`
12. `V12_first_access_reuse_behavior`
13. `V13_reuse_interval_count`
14. `V14_reuse_interval_sum`
15. `V15_reuse_interval_min`
16. `V16_reuse_interval_max`
17. `V17_materialization_independence`
18. `V18_bytes_read_accounting`
19. `V19_named_cache_hit_accounting`
20. `V20_named_cache_miss_accounting`
21. `V21_residency_transition_aggregation`
22. `V22_prefetch_issue_accounting`
23. `V23_prefetch_consumed_accounting`
24. `V24_prefetch_unused_accounting`
25. `V25_duplicate_prefetch_terminal_rejection`
26. `V26_invalid_event_failure_atomicity`
27. `V27_empty_snapshot_semantics`
28. `V28_nonempty_sequence_bounds`
29. `V29_deterministic_snapshot_ordering`
30. `V30_snapshot_payload_reproducibility`
31. `V31_snapshot_sha_reproducibility`
32. `V32_zero_denominator_metric_rejection`
33. `V33_weighted_rank_distance_exactness`
34. `V34_cross_segment_fraction_exactness`
35. `V35_co_segment_fraction_exactness`
36. `V36_cross_co_complement`
37. `V37_placement_uniqueness`
38. `V38_contiguous_segment_ordinals`
39. `V39_contiguous_object_ordinals`
40. `V40_exact_source_object_set_preservation`
41. `V41_deterministic_planner_config_ordering`
42. `V42_duplicate_planner_config_key_rejection`
43. `V43_source_generation_binding`
44. `V44_telemetry_snapshot_binding`
45. `V45_deterministic_plan_ordering`
46. `V46_plan_payload_reproducibility`
47. `V47_plan_sha_reproducibility`
48. `V48_no_payload_mutation_surface`
49. `V49_phase6c_source_immutability`
50. `V50_import_time_side_effect_absence`

## 27. Acceptance boundary

Passing V01-V50 establishes only the standalone Phase 6D locality data-model
properties directly tested by this protocol.

It does not establish:

- runtime instrumentation correctness;
- persistent telemetry correctness;
- transition-locality improvement;
- planner optimization quality;
- generational repack correctness;
- device storage benefit;
- inference benefit;
- Phase 6E selective access;
- MAF-native inference.

## 28. Runner implementation authorization

Freezing this protocol authorizes creation of the Validation V1 runner only.

The runner must then receive:

1. static derivation audit;
2. local Git freeze;
3. final no-write preflight.

Only after those gates pass may one exact-once scientific invocation occur.

## 29. Authorization boundary

VALIDATION PROTOCOL: PREREGISTERED BY THIS ARTIFACT.

VALIDATION RUNNER IMPLEMENTATION: AUTHORIZED AFTER PROTOCOL FREEZE.

VALIDATION EXECUTION: NOT AUTHORIZED BY PROTOCOL FREEZE ALONE.

PHASE 6C EDIT: FORBIDDEN.

PHASE 6C REOPEN: FORBIDDEN.

RUNTIME INTEGRATION: NOT AUTHORIZED.

REPACK REALIZATION: NOT AUTHORIZED.

LOCALITY EXPERIMENT: NOT AUTHORIZED.

DEVICE BENCHMARK: NOT AUTHORIZED.

PHASE 6E: NOT ENTERED.

PERFORMANCE VERDICT: NONE.

PUSH: NOT AUTHORIZED BY THIS PROTOCOL.
