# MAF Segment Locality Data Model V1 Protocol

Status: PROSPECTIVE PREREGISTRATION
Phase: 6D
Parent research phase: Segment Locality and Path-Aware Repacking
Artifact class: data-model / aggregation-semantics protocol
Implementation status: NOT IMPLEMENTED
Scientific result: NONE
Performance verdict: NONE
Runtime instrumentation authorized: NO
Generation realization authorized: NO
Experiment execution authorized: NO

## 1. Purpose

This protocol prospectively freezes the first standalone Phase 6D data-model
boundary.

It defines deterministic representation semantics for:

1. runtime telemetry events;
2. RAM telemetry aggregation;
3. immutable telemetry snapshots;
4. exact locality metric values;
5. deterministic repack-placement plans.

It does not instrument the frozen Phase 6C runtime.

It does not build or activate a repacked generation.

It does not execute a scientific experiment or benchmark.

## 2. Frozen parent

Branch:

`labs/multidimensional-maf`

Parent commit:

`ae1299158ec1981746e8f40af2ac9e5e00e3d85b`

Parent Phase 6D protocol:

`experiments/model_fractal/MAF_SEGMENT_LOCALITY_REPACKING_V1_PROTOCOL.md`

SHA256:

`a4c1a1d4fe22f7e714efa331cec9cf4dbd3a9e178f2b28b3ddb9034387e210ae`

Frozen Phase 6C runtime:

`experiments/model_fractal/maf_object_runtime_residency_v1.py`

SHA256:

`4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9`

The Phase 6C runtime remains immutable historical evidence.

## 3. Existing implementation boundary

Read-only discovery and semantic audit established that no existing Python
module implements this Phase 6D telemetry/repack data model.

The earlier lexical candidates were:

- `experiments/model_fractal/maf_compile_recipe_v1.py`
- `experiments/model_fractal/maf_compile_recipe_validation_v1.py`
- `experiments/model_fractal/maf_encoder_v1.py`

Their frozen SHA256 identities are:

- `388110497205591135bd191016987391fb2c9664513f9133bc7a4abd5df5ff51`
- `751d0d5cce0036f1f701067b7106b164099799aea0fe53ea52b80c3ed90bce5b`
- `0232fc49c2ef568291453b48b62bf6a37fa64f123051224b4228a214454995c0`

They do not implement:

- runtime telemetry aggregation;
- telemetry snapshots;
- transition-aware physical placement;
- Phase 6D repack-plan semantics;
- Phase 6D generational repack realization.

The new implementation therefore does not compete with an existing Phase 6D
implementation.

## 4. Authorized future implementation artifact

The only implementation artifact directly authorized after this protocol is
frozen is:

`experiments/model_fractal/maf_segment_locality_data_model_v1.py`

The module must be standalone.

It may use the Python standard library.

It must not modify the frozen Phase 6C runtime.

It must perform no filesystem write, activation, generation mutation, benchmark,
or scientific execution at import time.

## 5. Derived-state rule

Canonical model, generation, manifest, segment, and object data remain
authoritative.

Telemetry, telemetry aggregates, snapshots, metric values, and repack plans are
derived evidence.

No Phase 6D data-model operation may silently alter:

- model PK;
- generation PK;
- logical object PK;
- object payload bytes;
- object payload SHA256.

## 6. Canonical JSON

V1 canonical JSON bytes are produced by Python json.dumps with:

- sort_keys=True;
- separators equal to comma and colon with no added spaces;
- ensure_ascii=False;

followed by UTF-8 encoding.

No trailing newline forms part of canonical identity.

Canonical snapshot and plan SHA256 values are hashes of those canonical bytes.

## 7. Integer semantics

Scientific counters and ordinals require plain Python integers.

Boolean values are invalid where an integer is required.

Counters and ordinals must be non-negative unless a field is explicitly
documented otherwise.

Canonical scientific identity must not depend on floating-point arithmetic.

Ratios are represented exactly as integer numerator and denominator pairs.

## 8. Required identifier semantics

Required text identifiers are non-empty strings.

SHA256 fields contain exactly 64 lowercase hexadecimal characters.

PK fields must obey their already frozen entity-class syntax.

## 9. Event ordering

Every telemetry event contains an authoritative logical sequence number named:

`sequence`

The sequence must be:

- a plain non-negative integer;
- unique within one accumulator trace;
- strictly increasing as events are committed.

Wall-clock time is not part of V1 scientific ordering.

## 10. TelemetryEventKind

The future implementation must define exactly these ten V1 event kinds:

1. `ACCESS`
2. `MATERIALIZATION`
3. `BYTES_READ`
4. `CACHE_HIT`
5. `CACHE_MISS`
6. `PROMOTION`
7. `DEMOTION`
8. `PREFETCH_ISSUED`
9. `PREFETCH_CONSUMED`
10. `PREFETCH_UNUSED`

No free-form event kind is authoritative in V1.

## 11. TelemetryEvent

The future implementation must define an immutable slotted value object named:

`TelemetryEvent`

Required fields:

- `sequence`
- `kind`
- `object_pk`
- `byte_count`
- `cache_name`
- `from_state`
- `to_state`
- `prefetch_id`

Fields not applicable to a given kind use null.

Legal field combinations must be validated before an event is committed.

## 12. ACCESS semantics

ACCESS requires:

- sequence;
- object PK.

Each accepted ACCESS increments that object's access count exactly once.

## 13. Directed access transitions

Directed transitions are derived from consecutive accepted ACCESS events in
global logical event order.

If one ACCESS targets A and the next ACCESS targets B:

`transition_count[(A, B)] += 1`

Non-ACCESS events between those ACCESS events do not break the access
transition sequence.

Self-transitions are valid.

## 14. Reuse interval

For consecutive ACCESS events to the same object at logical sequences
`previous_sequence` and `current_sequence`:

`reuse_interval = current_sequence - previous_sequence`

The first access to an object yields no reuse interval.

## 15. MATERIALIZATION semantics

MATERIALIZATION requires:

- sequence;
- object PK.

It increments materialization count exactly once.

Materialization count is independent from access, cache miss, promotion, and
bytes-read counts.

## 16. BYTES_READ semantics

BYTES_READ requires:

- sequence;
- object PK;
- non-negative byte count.

The accumulator adds exactly the supplied byte count.

V1 calls this runtime-attributed read bytes.

It does not claim that this counter equals kernel or physical-device traffic.

## 17. Cache event semantics

CACHE_HIT and CACHE_MISS require:

- sequence;
- object PK;
- non-empty cache name.

Cache aggregates are keyed by:

- cache name;
- object PK.

An unnamed generic cache statistic is invalid.

## 18. Residency event semantics

PROMOTION and DEMOTION require:

- sequence;
- object PK;
- from state;
- to state.

V1 state names are:

- `COLD_DISK`
- `MAPPED`
- `HOT_MAF`
- `HOT_DENSE`

Phase 6D records committed runtime observations and does not redefine the
Phase 6C state machine.

## 19. Prefetch event semantics

PREFETCH_ISSUED, PREFETCH_CONSUMED, and PREFETCH_UNUSED require a non-empty
prefetch ID.

A consumed or unused event must refer to an already issued ID.

An issued prefetch may receive at most one terminal resolution.

Support in this data model does not claim that runtime prefetch currently
exists.

## 20. ObjectTelemetryAggregate

The future module must define an immutable slotted:

`ObjectTelemetryAggregate`

Required fields:

- `object_pk`
- `access_count`
- `reuse_interval_count`
- `reuse_interval_sum`
- `reuse_interval_min`
- `reuse_interval_max`
- `materialization_count`
- `bytes_read`

For no observed reuse:

- count = 0;
- sum = 0;
- min = null;
- max = null.

## 21. TransitionTelemetryAggregate

The future module must define an immutable slotted:

`TransitionTelemetryAggregate`

Fields:

- `source_object_pk`
- `target_object_pk`
- `count`

Canonical order:

1. source object PK;
2. target object PK.

## 22. CacheTelemetryAggregate

The future module must define an immutable slotted:

`CacheTelemetryAggregate`

Fields:

- `cache_name`
- `object_pk`
- `hit_count`
- `miss_count`

Canonical order:

1. cache name;
2. object PK.

## 23. ResidencyTransitionAggregate

The future module must define an immutable slotted:

`ResidencyTransitionAggregate`

Fields:

- `object_pk`
- `from_state`
- `to_state`
- `count`

Canonical order:

1. object PK;
2. from state;
3. to state.

## 24. PrefetchTelemetryAggregate

The future module must define an immutable slotted:

`PrefetchTelemetryAggregate`

Fields:

- `object_pk`
- `issued_count`
- `consumed_count`
- `unused_count`

Invariant:

`consumed_count + unused_count <= issued_count`

## 25. TelemetryAccumulator

The one authorized mutable V1 helper is:

`TelemetryAccumulator`

It is RAM-only derived state.

It must be initialized with authority binding sufficient to produce the frozen
snapshot fields:

- model PK;
- source generation PK;
- source manifest SHA256.

It must:

- accept events in strict sequence order;
- reject duplicate or decreasing sequences;
- update aggregates deterministically;
- retain sufficient state for reuse and transition accounting;
- provide no canonical-model mutation operation.

## 26. Accumulator failure atomicity

An invalid event must not partially mutate the accumulator.

Validation occurs before event commitment.

If event application fails, the next snapshot must equal the snapshot that
would have existed immediately before that failed event.

## 27. TelemetrySnapshot

The future module must define an immutable slotted:

`TelemetrySnapshot`

Required fields:

- `schema`
- `aggregation_version`
- `model_pk`
- `source_generation_pk`
- `source_manifest_sha256`
- `first_sequence`
- `last_sequence`
- `event_count`
- `access_event_count`
- `object_aggregates`
- `transition_aggregates`
- `cache_aggregates`
- `residency_transition_aggregates`
- `prefetch_aggregates`

## 28. Snapshot identity constants

Exact snapshot schema:

`openmind.maf_segment_locality.telemetry_snapshot.v1`

Exact aggregation version:

`maf_segment_locality_aggregation_v1`

## 29. Empty snapshot

For an accumulator containing zero committed events:

- event count = 0;
- access event count = 0;
- first sequence = null;
- last sequence = null;
- all aggregate collections are empty.

## 30. Non-empty sequence bounds

For a non-empty snapshot:

- first sequence equals the first committed event sequence;
- last sequence equals the last committed event sequence;
- first sequence is less than or equal to last sequence.

Event count counts all accepted telemetry events.

Access event count counts ACCESS events only.

## 31. Snapshot ordering

Snapshot aggregate collections must have deterministic order independent of
dictionary insertion order.

Object aggregates:

lexical object PK.

Transition aggregates:

lexical source PK then target PK.

Cache aggregates:

lexical cache name then object PK.

Residency aggregates:

lexical object PK then from state then to state.

Prefetch aggregates:

lexical object PK.

## 32. Snapshot payload

The module must expose:

`snapshot_payload(snapshot)`

It returns only JSON-compatible canonical data.

Scientific identity must not depend on:

- Python object address;
- repr output;
- hash randomization;
- wall-clock time;
- unordered-container iteration.

## 33. Snapshot SHA256

The module must expose:

`snapshot_sha256(snapshot)`

Its value is SHA256 of canonical JSON bytes from `snapshot_payload(snapshot)`.

The snapshot SHA is not included inside the payload being hashed.

## 34. LocalityMetricId

V1 defines exactly three locality metric identifiers:

1. `WEIGHTED_TRANSITION_RANK_DISTANCE`
2. `CROSS_SEGMENT_FRACTION`
3. `CO_SEGMENT_FRACTION`

Weighted byte-gap measurement is deferred because final byte offsets belong to
the later realization boundary.

## 35. ExactRatio

The future module must define an immutable slotted:

`ExactRatio`

Fields:

- `numerator`
- `denominator`

Both are non-negative plain integers.

A denominator of zero is undefined and must be rejected when a metric value is
requested.

## 36. LocalityMetricValue

The future module must define an immutable slotted:

`LocalityMetricValue`

Fields:

- `metric_id`
- `numerator`
- `denominator`

The canonical metric representation remains exact and contains no floating
point.

## 37. Weighted transition rank distance

For transition counts `c(a,b)` and planned object ranks:

numerator equals the sum of:

`c(a,b) * abs(rank(a) - rank(b))`

denominator equals the sum of qualifying transition counts.

Lower is more local.

Self-transitions contribute zero to the numerator but remain in the
denominator.

## 38. Cross-segment fraction

Numerator:

sum of qualifying transition counts whose source and target are assigned to
different target segment ordinals.

Denominator:

sum of all qualifying transition counts.

Lower is more co-located.

## 39. Co-segment fraction

Numerator:

sum of qualifying transition counts whose source and target share a target
segment ordinal.

Denominator:

sum of all qualifying transition counts.

For a non-zero denominator:

`cross_numerator + co_numerator = denominator`

## 40. RepackPlacement

The future module must define an immutable slotted:

`RepackPlacement`

Fields:

- `object_pk`
- `target_segment_ordinal`
- `target_object_ordinal`

Ordinals are zero-based non-negative integers.

The placement is a planning decision, not a final segment PK or byte offset.

## 41. Placement invariants

Within one complete V1 plan:

- every object PK appears exactly once;
- each segment/object ordinal pair is unique;
- target segment ordinals form a contiguous zero-based range;
- object ordinals inside each target segment form a contiguous zero-based
  range.

## 42. Complete source-object-set boundary

V1 supports only complete source-generation placement plans.

A plan must represent exactly the source logical object set supplied for
validation.

Partial/selective object planning is not authorized because it would begin to
cross into Phase 6E selective-access research.

## 43. PlannerConfigEntry

The future module must define an immutable slotted:

`PlannerConfigEntry`

Fields:

- `key`
- `canonical_value_json`

Keys are non-empty and unique.

Entries are ordered lexically by key.

`canonical_value_json` contains one canonical JSON value encoded as text.

## 44. RepackPlan

The future module must define an immutable slotted:

`RepackPlan`

Fields:

- `schema`
- `planner_version`
- `model_pk`
- `source_generation_pk`
- `source_manifest_sha256`
- `telemetry_snapshot_sha256`
- `objective_metric_id`
- `planner_config`
- `placements`

## 45. Plan identity constants

Exact plan schema:

`openmind.maf_segment_locality.repack_plan.v1`

Planner version is mandatory and non-empty but this protocol does not select a
scientific planning algorithm.

That algorithm requires later prospective preregistration.

## 46. Repack-plan ordering

Planner config is canonically ordered by key.

Placements are canonically ordered by:

1. target segment ordinal;
2. target object ordinal;
3. object PK.

## 47. Repack-plan payload

The module must expose:

`repack_plan_payload(plan)`

It returns JSON-compatible canonical data containing every field that affects
scientific plan identity.

## 48. Repack-plan SHA256

The module must expose:

`repack_plan_sha256(plan)`

Its value is SHA256 of canonical JSON bytes from `repack_plan_payload(plan)`.

The plan SHA itself is not inside the payload being hashed.

## 49. Snapshot binding

Every plan binds exactly one frozen telemetry snapshot SHA256.

A scientifically valid plan may not claim to originate from mutable,
unidentified telemetry.

## 50. Source-generation binding

Every plan binds:

- model PK;
- source generation PK;
- source manifest SHA256.

A plan must not silently migrate to another generation.

## 51. No payload mutation

RepackPlan contains placement decisions only.

It contains no mechanism for:

- replacing object payload bytes;
- changing object PK;
- changing object payload SHA;
- changing logical object semantics.

## 52. No filesystem or activation semantics

The V1 data-model module contains no operation that:

- writes a segment;
- persists a generation;
- activates a generation;
- modifies active authority;
- deletes an old generation.

Those belong to future Phase 6D realization/integration work.

## 53. No Phase 6C runtime mutation

The implementation must not edit, monkey-patch, or mutate:

`experiments/model_fractal/maf_object_runtime_residency_v1.py`

A future observer/adapter or runtime successor requires separate prospective
preregistration.

## 54. Threading boundary

Value objects are immutable.

V1 does not establish concurrent accumulator correctness or multithread
performance.

Any shared-thread integration requires separate prospective validation.

Phase 6F performance claims remain forbidden.

## 55. Mandatory future validation matrix

Before integration or scientific use, a separate validation protocol must test
at minimum:

1. canonical JSON byte determinism;
2. plain-integer validation;
3. exact ten-event-kind surface;
4. event-kind validation;
5. event-field combination validation;
6. strict increasing sequence enforcement;
7. duplicate sequence rejection;
8. ACCESS counting;
9. self-transition counting;
10. directed transition counting;
11. non-ACCESS events preserving ACCESS adjacency;
12. first-access reuse behavior;
13. reuse count;
14. reuse sum;
15. reuse minimum;
16. reuse maximum;
17. materialization-count independence;
18. bytes-read accounting;
19. named cache hit accounting;
20. named cache miss accounting;
21. residency transition aggregation;
22. prefetch issue accounting;
23. prefetch consumed accounting;
24. prefetch unused accounting;
25. duplicate prefetch terminal-resolution rejection;
26. invalid-event failure atomicity;
27. empty-snapshot semantics;
28. non-empty sequence bounds;
29. deterministic snapshot tuple ordering;
30. snapshot payload reproducibility;
31. snapshot SHA reproducibility;
32. zero-denominator metric rejection;
33. weighted transition-rank exactness;
34. cross-segment metric exactness;
35. co-segment metric exactness;
36. cross/co complement invariant;
37. placement uniqueness;
38. contiguous segment ordinals;
39. contiguous per-segment object ordinals;
40. exact source object-set preservation;
41. deterministic planner-config ordering;
42. duplicate planner-config-key rejection;
43. source-generation binding;
44. telemetry-snapshot binding;
45. deterministic plan ordering;
46. plan payload reproducibility;
47. plan SHA reproducibility;
48. no object payload mutation surface;
49. no Phase 6C source mutation;
50. import-time side-effect absence.

## 56. Validation ordering

The data-model implementation must be frozen before scientific validation is
preregistered.

Required order:

1. freeze this protocol;
2. implement the module;
3. static-audit the implementation;
4. freeze the implementation;
5. preregister validation;
6. freeze validation runner;
7. final no-write preflight;
8. exactly one validation invocation;
9. freeze raw result before interpretation.

## 57. Reserved future validation artifacts

Validation protocol:

`experiments/model_fractal/MAF_SEGMENT_LOCALITY_DATA_MODEL_VALIDATION_V1_PROTOCOL.md`

Validation runner:

`experiments/model_fractal/maf_segment_locality_data_model_validation_v1.py`

Raw validation result:

`experiments/model_fractal/maf_segment_locality_data_model_validation_v1.json`

They are reserved by this protocol but are not created by this protocol
freeze.

## 58. Performance boundary

This data model establishes no performance result.

It does not establish:

- faster inference;
- fewer physical reads;
- lower latency;
- higher throughput;
- better cache behavior;
- lower RAM use;
- lower energy;
- better thermal behavior;
- lower flash wear.

Performance verdict remains NONE.

## 59. Phase 6E boundary

This data model must not implement or claim:

- selective fragment retrieval;
- selective tensor avoidance;
- selective dense materialization;
- hidden-state equivalence;
- logit equivalence;
- top-k agreement;
- token agreement.

Each V1 repack plan represents a complete source logical object set.

## 60. Explicit nonclaims

Freezing this protocol proves no Phase 6D scientific result.

It does not prove:

- telemetry correctness;
- snapshot correctness;
- locality improvement;
- planner correctness;
- repack correctness;
- generation correctness;
- runtime integration correctness;
- performance improvement;
- Phase 6E selective access;
- MAF-native inference;
- replacement of a conventional LLM runtime.

## 61. Authorization boundary

PHASE 6C EDIT: FORBIDDEN.

PHASE 6C REOPEN: FORBIDDEN.

PHASE 6D DATA MODEL IMPLEMENTATION: AUTHORIZED AFTER THIS PROTOCOL FREEZE.

PHASE 6D DATA MODEL VALIDATION: NOT YET AUTHORIZED.

PHASE 6D RUNTIME INTEGRATION: NOT AUTHORIZED.

PHASE 6D REPACK REALIZATION: NOT AUTHORIZED.

PHASE 6D LOCALITY EXPERIMENT: NOT AUTHORIZED.

PHASE 6D DEVICE BENCHMARK: NOT AUTHORIZED.

PHASE 6E: NOT ENTERED.

PERFORMANCE VERDICT: NONE.

PUSH: NOT AUTHORIZED BY THIS PROTOCOL.
