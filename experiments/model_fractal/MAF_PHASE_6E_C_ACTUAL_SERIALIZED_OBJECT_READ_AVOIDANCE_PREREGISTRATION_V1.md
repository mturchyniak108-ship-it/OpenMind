# MAF Phase 6E-C Actual Serialized Object Read Avoidance Preregistration V1

**STATUS: PROSPECTIVE PREREGISTRATION — NO PHASE 6E-C RUNNER EXISTS — NO PHASE 6E-C SCIENCE EXECUTED**

## 1. Purpose

This document preregisters the first Phase 6E-C experiment.

Phase 6E-C follows the frozen Phase 6E-A selective-working-set sufficiency PASS and the frozen Phase 6E-B-S1 bounded-expansion recovery PASS.

The experiment asks whether the already accepted non-oracle query-to-PK mechanism can produce a bounded MAF working set whose **application-level serialized-object payload reads are actually restricted to that working set**, rather than merely claiming avoidance from a selected-PK list.

This experiment is prospective. It does not reinterpret Phase 6E-A or Phase 6E-B-S1, does not rerun either phase, and does not treat prior selected-PK state as proof of physical read avoidance.

## 2. Frozen predecessor checkpoint

Required branch:

`labs/multidimensional-maf`

Required preregistration parent checkpoint:

`9350b4ad4f24fff30a2926155bd5c466665d751f`

That checkpoint contains the frozen Phase 6E-B-S1 narrow verdict.

Phase 6E-A runner commit:

`7cf66034e3cf66356584cd3f02b1d2c556e31a64`

Phase 6E-A runner SHA256:

`72c0eca00013e0b70c4a95c4043f0a11b0b6b3d885166a898014f74b928961d6`

The 64-hex SHA above is the historically verified Git-frozen identity. The previously carried 63-character value is invalid and MUST NOT be used as an authority.

## 3. Frozen predecessor scientific results

### Phase 6E-A result

SHA256:

`f86433603e68fc9f1e5c65f7d3ecbd8d9ce9313d252c605dd6e2cada18a91c86`

Phase 6E-A established, within its frozen boundary, that all 32 evaluable non-fallback queries had sufficient required generation-bound MAF object payload state at selector candidate budget 4.

It did not establish actual object or tensor avoidance.

### Phase 6E-A verdict

Path:

`experiments/model_fractal/MAF_PHASE_6E_A_SELECTIVE_WORKING_SET_SUFFICIENCY_V1_VERDICT.md`

SHA256:

`a6c9ce2f2207beb252b2c02b47e27878b27e72736dad4275ab9905d40812e334`

### Phase 6E-B-S1 result

Path:

`experiments/model_fractal/maf_phase_6e_b_s1_bounded_expansion_recovery_v1.json`

SHA256:

`194857dd4df6baabbee3138f1e6cb3d75988ddd092a4fd877892ab4528cf81a4`

Frozen expansion trace SHA256:

`5fab94f632b8e653b2debe3f5e98f9a19b9688bd9bacb4a578c75537c1b0ca53`

Qualified Phase 6E-B-S1 counts:

- frozen query population: 40;
- specific-intent queries: 24;
- multi-target-intent queries: 8;
- fallback controls: 8;
- initially sufficient non-fallback queries at candidate budget 1: 24;
- initial-insufficiency challenges: 8;
- recovered challenges: 8;
- not recovered: 0;
- qualified verdict: `PASS`.

Phase 6E-B-S1 established bounded recovery of required object payload state under the fixed 1→2→3→4 selector schedule.

It explicitly did not establish actual object or tensor avoidance.

### Phase 6E-B-S1 verdict

Path:

`experiments/model_fractal/MAF_PHASE_6E_B_S1_BOUNDED_EXPANSION_RECOVERY_V1_VERDICT.md`

SHA256:

`6ba5427a18d4bbbb2435456250874372016438367d8c591913432c084c627abf`

## 4. Original Phase 6E-B incident remains historical and spent

Frozen incident:

`experiments/model_fractal/MAF_PHASE_6E_B_EXECUTION_FAILURE_INCIDENT_AND_CORRECTIVE_SUCCESSOR_DESIGN_V1.md`

SHA256:

`1ecf171bee1e6470d5ac48c1482a2166eca05c895313eeb4acbc8e90b64a64ad`

The original Phase 6E-B runner remains spent and MUST NOT be imported, called, or executed.

The original Phase 6E-B result path MUST remain absent permanently.

Phase 6E-C MUST NOT reconstruct or reuse any unpersisted state from the spent original Phase 6E-B execution.

## 5. Phase 6E roadmap position

Frozen Phase 6E entry checkpoint:

`experiments/model_fractal/MAF_PHASE_6E_ENTRY_CHECKPOINT.md`

SHA256:

`1807437ea97e46a6cc687adbbe8c384dabae45a562f1d2aef6bd37e43b4bbe35`

The frozen roadmap progression is:

1. Phase 6E-A — selective working-set sufficiency;
2. Phase 6E-B — bounded expansion and recovery;
3. Phase 6E-C — actual tensor/object avoidance;
4. Phase 6E-D — output parity and quality;
5. Phase 6F — performance measurement after correctness.

Phase 6E-C therefore precedes Phase 6E-D and Phase 6F.

## 6. Scientific question

For the frozen 40-query population and frozen 12-object validation generation, can the accepted non-oracle query-to-PK mechanism drive an execution path in which:

1. the complete query-derived working-set route is frozen before hidden reference interpretation;
2. application-level serialized MAF object reads occur only for the query-derived working set;
3. every required generation-bound object payload for evaluable non-fallback queries is actually read and verified;
4. every catalog object outside that query's touched working set receives no scientific-window serialized-object read;
5. the touched serialized-object set is strictly smaller than the full frozen 12-object catalog for every evaluable non-fallback query?

## 7. Narrow claim boundary

A PASS may establish only:

> Within the frozen 40-query population, frozen 12-object catalog, frozen validation generation, frozen selector, and preregistered read-observation boundary, the query-derived MAF working-set path caused actual application-level serialized-object range reads only for the recorded touched objects, while every required generation-bound payload was present and verified for each evaluable non-fallback query, and at least one catalog object was demonstrably unread for every such query.

The preferred narrower terminology is:

`generation-bound serialized MAF object/tensor-payload read avoidance`

This is **not** a claim about storage-device sectors, kernel page-cache misses, physical NAND reads, or hardware bus transactions.

The experiment observes application-level file/range reads issued by the frozen MAF path.

## 8. What Phase 6E-C V1 does not establish

This experiment MUST NOT claim:

- arbitrary-prompt generalization;
- correctness outside the frozen 40-query population;
- avoidance outside the frozen 12-object validation catalog;
- avoidance across the full 339-tensor source model;
- source-GGUF tensor avoidance during conventional inference;
- dense-runtime replacement;
- direct computation on persistent MAF bytes;
- MAF-native inference;
- answer generation;
- logit parity;
- top-k parity;
- token agreement;
- output-quality equivalence;
- latency improvement;
- throughput improvement;
- memory improvement;
- energy improvement;
- storage-I/O performance improvement;
- speedup of any kind;
- relationship-based expansion;
- Query Route Cache benefit;
- route optimality.

Output and quality fidelity remain Phase 6E-D.

Performance remains Phase 6F.

MAF-native compute remains `disabled_unvalidated`.

## 9. Frozen source model and generation

Source GGUF:

`/data/data/com.termux/files/home/qwen2.5-coder-q8_0.gguf`

Source GGUF SHA256:

`507de59046601282ba768a9789900e6ccf60ed93ddf346730b7c68eb0715bc47`

Source model PK:

`mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258`

Source generation PK:

`mafgen:v1:45a80a2aa271ce04853003185b6a1227cb309bd1e3e2dc538eea849fac9f5db0`

Generation construction authority SHA256:

`a5e953ae2ab2dd11a9f6dc564ae5ee57cb064d6eea0a8a5517191b4a6efc1a6d`

Generation manifest:

`results/runtime/maf_query_to_pk_selection_validation_v1_generation/validation_generation.manifest.json`

Generation manifest SHA256:

`28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3`

Frozen serialized object count:

`12`

Frozen serialized object bytes:

`312326668`

The 12-object validation generation is the only catalog denominator authorized for Phase 6E-C V1.

## 10. Frozen non-oracle query authorities

Query fixture:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_queries.json`

SHA256:

`32f4636bd5e8ceee0dca8342335279a6f8e6acafe866a5469f2c23aa2655202a`

Catalog:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_catalog.json`

SHA256:

`c51ef0fabeb10e7c8a091a093aa1934620a69b2026b5a87cb02477b9dd7ca900`

Frozen query classes:

- 24 `specific_intent`;
- 8 `multi_target_intent`;
- 8 `fallback_control`.

Accepted selector protocol SHA256:

`b42a0643976c2393871e3b826ba5573b4de981b49603de63230d69cf57be0811`

Accepted selector implementation:

`experiments/model_fractal/maf_query_to_pk_selection_v1.py`

SHA256:

`e21c05e352fe921b791e8c936425727a98911ce7566989672a96bfd2b9613fa2`

The spent Q2 V1.4 runner:

`maf_query_to_pk_selection_validation_v1_4.py`

MUST NOT be imported, called, or executed.

## 11. Frozen capsule authority

Capsule protocol SHA256:

`5255a58c8c6340c251e24ae8543760fcd66a8deb8be1a8356ad5b78ad898edda`

Capsule implementation:

`experiments/model_fractal/maf_query_capsule_data_model_v1.py`

SHA256:

`f897b97011714f3c84b7350c6bb53e800232be8a5d34e5148a3e50a81952976e`

The frozen capsule model already defines:

`touched_pks`

and requires deterministic selected-minus-touched accounting.

For Phase 6E-C, `touched_pks` MUST be populated from independently observed successful serialized-object reads.

It MUST NOT be populated merely by copying `selected_object_pks`.

## 12. Frozen physical serialized-object read boundary

Segment reader:

`experiments/model_fractal/maf_segment_reader_v1.py`

SHA256:

`3499cb8e528fe8e9315e3e5656d6aa888c95ca175310b6371e722de409827369`

The scientific serialized-object read primitive is:

`read_serialized_object`

A Phase 6E-C scientific **object touch** is one successful invocation of the frozen generation-bound serialized-object reader for one catalog object PK during that query's scientific read-observation window.

The event MUST bind at minimum:

- query ID;
- object PK;
- source generation PK;
- segment identity;
- segment path identity;
- object offset;
- serialized object length;
- returned serialized-byte length;
- returned serialized-object SHA256;
- read ordinal.

A failed read MUST be recorded separately and MUST NOT be silently converted into a successful touch.

## 13. Application-level read definition

For this experiment:

`TOUCHED`

means the runner issued the authorized serialized-object range read and obtained the exact generation-bound serialized bytes for that PK.

`UNTOUCHED`

means no authorized or unauthorized scientific-window serialized-object payload/range read event was issued for that catalog PK.

This definition is intentionally application-level.

Operating-system caching may satisfy a read without a physical storage-device transaction. Therefore Phase 6E-C V1 does not use the words "disk read avoided" or "physical NAND read avoided" as scientific claims.

## 14. Metadata-read separation

The following are metadata or authority reads and MUST NOT count as object-payload touches:

- Git identity checks;
- SHA256 qualification performed before the scientific observation window;
- query fixture reads;
- catalog reads;
- generation authority reads;
- generation manifest reads;
- reference fixture bytes read after the access trace is frozen;
- result-file writes or rereads;
- source-code reads;
- commit/object database reads.

The Phase 6E-C result MUST distinguish:

- `preflight_authority_reads`;
- `scientific_serialized_object_reads`;
- `post_trace_reference_reads`;
- `result_publication_io`.

Only `scientific_serialized_object_reads` contribute to the avoidance claim.

## 15. Source GGUF boundary

The source GGUF may be verified before the scientific observation window.

After the Phase 6E-C scientific observation window begins, the runner MUST NOT open, seek, read, mmap, materialize, or otherwise consume source GGUF tensor bytes.

Any source-GGUF payload access during the scientific observation window is an infrastructure/integrity failure.

This experiment does not claim that a later conventional inference runtime can operate without the source GGUF. That remains outside Phase 6E-C V1.

## 16. Object-file and segment boundary

The scientific read path MUST use the frozen generation-bound segment placement and the frozen segment reader.

The runner MUST NOT establish avoidance by directly opening each serialized object file for payload inspection during the scientific observation window.

The returned bytes from the authorized segment-range read are the payload-evidence source for that touch.

Any second scientific-window filesystem payload read of the same object for verification is prohibited.

Verification MUST operate on the already returned serialized bytes in memory.

## 17. In-memory verification requirement

For every touched object, the runner must verify from the bytes already returned by the authorized serialized-object read:

1. serialized byte length equals the generation placement length;
2. serialized-object SHA256 equals the frozen generation manifest object-file SHA256;
3. serialized header/metadata are structurally valid under the frozen MAF object format;
4. payload span lies exactly inside the returned serialized object;
5. observed payload SHA256 computed from that in-memory payload span equals the generation descriptor payload SHA256;
6. after the reference barrier opens, observed payload SHA256 equals the frozen reference payload SHA256 for required objects.

No verification step may reread object payload bytes from disk.

## 18. MAF object format authority

MAF object implementation:

`experiments/model_fractal/maf_object_v1.py`

SHA256:

`eed6cbd96995412a632883f3c534f9023e7711ea8eb437afe35a48312502f63b`

The later runner implementation contract must statically identify the exact frozen parsing functions or constants used to parse an already-read serialized object in memory.

If the frozen module exposes no safe in-memory parser, the implementation contract must define a minimal independent parser from the frozen format without opening the object file.

The scientific runner MUST NOT call `inspect_object` during its scientific read-observation window because `inspect_object` opens and reads the object path independently.

## 19. Existing telemetry authorities

Phase 6E-C may reuse existing telemetry data structures only if their frozen identity and semantics are statically qualified before runner creation.

Relevant discovered authorities include:

`experiments/model_fractal/maf_segment_locality_data_model_v1.py`

SHA256:

`5432f2d74a610f2d0f9181e9af146013bb198a4e837af634993909358fff8ad0`

This model contains event kinds including:

- `MATERIALIZATION`;
- `BYTES_READ`.

Relevant runtime telemetry integration:

`experiments/model_fractal/maf_segment_locality_runtime_telemetry_integration_v1_1.py`

SHA256:

`850c4bae5f6c361c34f504b5af76b9ac6530980d777f8bd1a9003f3b9bb55ae6`

Telemetry reuse is optional.

If reused, telemetry MUST be observational only and MUST NOT change selector output, route ordering, read ordering, payload bytes, or scientific classification.

A dedicated immutable Phase 6E-C access ledger remains mandatory even if telemetry is also emitted.

## 20. Existing runtime materialization authority

Relevant runtime residency implementation discovered during read-only design review:

`experiments/model_fractal/maf_object_runtime_residency_v1.py`

SHA256:

`4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9`

That runtime contains dense-materialization support.

Phase 6E-C V1 does **not** require dense materialization to establish its narrow serialized-object read-avoidance claim.

Dense tensor materialization MUST remain disabled unless a later separately frozen Phase 6E-C sub-protocol explicitly authorizes it.

Therefore this V1 result may not be described as end-to-end dense tensor materialization avoidance.

## 21. Route Cache and relationship expansion

Query Route Cache is disabled for Phase 6E-C V1.

Relationship-based expansion is disabled.

`selected_relationship_pks` MUST remain empty.

No Query Route Cache implementation may influence:

- query selection;
- round expansion;
- touched object sets;
- access ordering;
- avoidance classification.

## 22. Frozen selector schedule

Phase 6E-C uses the same deterministic selector budget schedule already preregistered and executed prospectively by Phase 6E-B-S1:

- round 0 candidate budget: 1;
- round 1 candidate budget: 2;
- round 2 candidate budget: 3;
- round 3 candidate budget: 4.

Frozen selection-config SHA256 values, in order:

1. `2dd2925a3d9f63197deff6dc98f951c5177dc63dc08818b6492228dbac7d5576`
2. `57f751a3a019bccd58c5c32b4f5ecaf78283f49cc146896d61492ce31dfdd1c6`
3. `67dd6e5589cb16374e949b3ed633c3364f0ccb1d8c2b0a9ca1c6eaa2d2ceed56`
4. `0caeaeaafdd870e6b02ccc8b4450576883d4ef5234ba689c472e3b14d9dbe120`

No budget may be adapted after target observation.

## 23. Fresh non-oracle route construction

The authoritative Phase 6E-C runner MUST construct its own fresh deterministic query-to-PK route using the frozen selector and frozen non-oracle inputs.

It MUST NOT copy per-query selected PKs from:

- Phase 6E-A result;
- Phase 6E-B-S1 result;
- hidden reference state;
- any expected-target fixture;
- any manually authored route.

Prior results may be used only as frozen predecessor provenance and later independent comparison evidence.

## 24. Pre-reference route barrier

The runner MUST complete, canonicalize, and hash the full 40-query selector/expansion route trace before parsing hidden required-object state.

The route trace must contain only expansion-causal non-oracle evidence.

Before the reference barrier opens, the route trace MUST NOT contain:

- required object PKs;
- expected payload SHA256 values;
- reference payload SHA256 values;
- recovery verdicts;
- sufficiency verdicts derived from hidden reference;
- Phase 6E-A selected PKs;
- Phase 6E-B-S1 selected PKs.

## 25. Read-plan freeze barrier

After the full non-oracle route trace is frozen, the runner MUST derive a deterministic per-query read plan from that trace alone.

The read plan MUST be canonicalized and SHA256-bound before any hidden reference parse.

For evaluable and fallback queries alike, the planned touch order must be deterministic.

No hidden target may add, remove, reorder, or substitute planned object reads.

## 26. Scientific observation window

The scientific serialized-object observation window begins only after:

1. repository/authority qualification is complete;
2. source GGUF preflight qualification is complete;
3. frozen query/catalog/generation authorities are loaded;
4. the complete 40-query route trace is frozen;
5. the complete 40-query read plan is frozen.

During this window:

- source GGUF payload access is prohibited;
- direct object-file payload reads are prohibited;
- `inspect_object` is prohibited;
- only the frozen segment reader path may obtain serialized object payload bytes;
- every successful or failed serialized-object read attempt must be ledgered;
- the ledger is append-only in memory until the complete scientific access trace is frozen.

## 27. Per-query touch discipline

For each query:

1. start with an empty observed `touched_pks`;
2. traverse the preregistered read plan in deterministic order;
3. issue exactly one authorized serialized-object read for each planned PK;
4. append a successful touch only after exact generation-bound serialized bytes are returned;
5. do not reread an already touched PK;
6. do not read a PK absent from the frozen per-query plan;
7. compute verification evidence only from the returned bytes.

Any duplicate payload read, unplanned object read, or direct object payload file read is an infrastructure/integrity failure.

## 28. Fallback controls

The eight frozen fallback queries remain controls and are excluded from the scientific PASS denominator because they have no frozen required object PKs.

Their route and actual reads are still recorded.

Fallback controls MUST NOT be relabeled as recovered, sufficient, avoided, or failed scientific targets.

Their evidence may be used only to characterize deterministic control-path access behavior.

## 29. Evaluable scientific population

The scientific PASS denominator is the 32 frozen non-fallback queries:

- 24 specific-intent queries;
- 8 multi-target-intent queries.

This denominator is frozen independently of the Phase 6E-C observed access outcome.

## 30. Full-catalog avoidance denominator

For each evaluable query, the full catalog denominator is the complete frozen 12-object validation catalog.

Let:

`catalog_pks`

be the ordered set of all 12 frozen catalog object PKs.

Let:

`touched_pks`

be the ordered unique PKs with successful scientific-window serialized-object read events.

Define:

`untouched_pks = catalog_pks - touched_pks`

using deterministic catalog order.

An object counts as avoided only when it appears in `untouched_pks` and has no scientific-window serialized-object read event.

## 31. Serialized-byte avoidance accounting

Let:

`catalog_serialized_bytes`

be the sum of frozen serialized lengths for all 12 catalog objects:

`312326668`

For each evaluable query, define:

`touched_serialized_bytes`

as the sum of frozen serialized lengths for unique successfully touched PKs.

Define:

`avoided_serialized_bytes = catalog_serialized_bytes - touched_serialized_bytes`

and:

`avoided_object_count = 12 - len(touched_pks)`

Byte accounting is descriptive correctness evidence only.

It is not a performance metric.

No time measurement belongs in Phase 6E-C.

## 32. Required-object correctness evaluation

Only after:

1. the complete route trace is frozen;
2. the complete read plan is frozen;
3. all scientific serialized-object reads are complete;
4. the complete immutable access ledger is canonicalized and SHA256-bound;

may the runner parse the hidden frozen reference fixture.

Reference fixture:

`experiments/model_fractal/maf_phase_6e_a_reference_state_fixture_v1.json`

SHA256:

`870b656e0c3181ec8f7be1537bdeafde10fffd1b947f5372d21cdee4c00a83a0`

The reference fixture's known serialization convention remains compact canonical JSON followed by exactly one terminal LF.

Reference interpretation may classify the already frozen access trace but may not change it.

## 33. Per-query scientific classification

For each non-fallback query, derive:

### `READ_COMPLETE_AND_AVOIDED`

only if all are true:

1. every required object PK appears in the observed `touched_pks`;
2. every required touched object has exact generation-bound serialized-object SHA256;
3. every required touched object has exact in-memory observed payload SHA256 matching both generation descriptor and reference;
4. no payload mismatch exists;
5. no unplanned serialized-object read occurred;
6. no duplicate serialized-object payload read occurred;
7. no source-GGUF payload access occurred during the scientific window;
8. `len(touched_pks) < 12`;
9. `avoided_object_count > 0`;
10. `avoided_serialized_bytes > 0`.

### `READ_COMPLETE_NO_AVOIDANCE`

if all required payloads are correctly touched but the observed touched set equals the full 12-object catalog.

### `READ_INCOMPLETE`

if one or more required PKs were not successfully touched.

### `READ_PAYLOAD_MISMATCH`

if required payload bytes fail the frozen identity checks.

Any instrumentation-integrity violation is not a scientific negative and must instead terminate as an infrastructure/integrity failure before result publication.

## 34. Phase PASS condition

Phase 6E-C V1 is `PASS` if and only if:

1. evaluable query count is exactly 32;
2. all 32 evaluable queries classify `READ_COMPLETE_AND_AVOIDED`;
3. zero evaluable queries classify `READ_COMPLETE_NO_AVOIDANCE`;
4. zero classify `READ_INCOMPLETE`;
5. zero classify `READ_PAYLOAD_MISMATCH`;
6. every touched PK has exactly one successful authorized scientific-window serialized-object read;
7. every untouched PK has zero scientific-window serialized-object read events;
8. no source-GGUF payload read occurs during the observation window;
9. no direct object-file payload read occurs during the observation window;
10. the complete route trace, read plan, and access ledger all satisfy their frozen canonical SHA256 invariants.

## 35. Phase FAIL condition

Phase 6E-C V1 is a scientific `FAIL` if a valid authoritative run completes without instrumentation-integrity failure and one or more evaluable queries classify:

- `READ_COMPLETE_NO_AVOIDANCE`;
- `READ_INCOMPLETE`;
- `READ_PAYLOAD_MISMATCH`.

A valid negative result MUST be preserved and frozen.

The selector, schedule, denominator, read plan rules, or acceptance criteria MUST NOT be changed after observing a valid scientific FAIL in order to rescue the hypothesis.

## 36. NOT_TESTABLE condition

The experiment is `NOT_TESTABLE` only if the frozen evaluable denominator unexpectedly resolves to zero after exact authority validation.

Given the frozen query-class authority, the preregistered expectation is 32 evaluable non-fallback queries.

If an authority inconsistency prevents that population from being established, the runner must distinguish an infrastructure/integrity failure from a valid `NOT_TESTABLE` result.

## 37. Infrastructure/integrity failures

Examples include:

- wrong branch;
- wrong frozen runner commit binding;
- dirty tracked worktree;
- non-empty index;
- unexpected untracked-state change before science;
- frozen authority SHA mismatch;
- source GGUF identity mismatch during preflight;
- generation manifest inconsistency;
- query/catalog canonicalization mismatch;
- route non-determinism;
- route non-monotonicity;
- read-plan mutation after freeze;
- reference parse before route/read/access barriers permit it;
- unplanned serialized-object payload read;
- duplicate serialized-object payload read;
- direct object-file payload read during the scientific window;
- `inspect_object` during the scientific window;
- source-GGUF payload read during the scientific window;
- telemetry changing scientific behavior;
- ledger mutation after freeze;
- result-path collision;
- partial result publication.

Infrastructure/integrity failure is not scientific PASS or FAIL.

## 38. Access-ledger schema requirements

The implementation contract must define a canonical immutable access ledger containing, at minimum:

- schema;
- phase;
- source generation PK;
- route trace SHA256;
- read-plan SHA256;
- ordered query records;
- for every query:
  - query ID;
  - query class;
  - ordered planned PKs;
  - ordered successful touch events;
  - ordered failed read events;
  - ordered touched PKs;
  - deterministic untouched PKs;
  - touched serialized bytes;
  - avoided serialized bytes;
  - avoided object count;
- global scientific-window prohibited-access counters;
- source-GGUF scientific-window read count;
- direct-object-file scientific-window payload-read count;
- duplicate-read count;
- unplanned-read count.

The ledger must be complete and SHA256-bound before hidden reference interpretation.

## 39. Result schema

Planned result schema:

`openmind.maf_phase_6e_c_actual_serialized_object_read_avoidance.v1`

Planned result path:

`experiments/model_fractal/maf_phase_6e_c_actual_serialized_object_read_avoidance_v1.json`

The result path must be absent before the one authoritative execution.

Result publication must be immutable and fail closed, preferably using exclusive creation equivalent to `O_EXCL`.

## 40. Minimum result bindings

The result must bind at minimum:

- result schema;
- phase `6E-C`;
- this preregistration SHA256;
- later frozen runner implementation contract SHA256;
- later frozen runner source SHA256;
- runner commit binding;
- Phase 6E entry checkpoint SHA256;
- Phase 6E-A result SHA256;
- Phase 6E-A verdict SHA256;
- Phase 6E-B-S1 result SHA256;
- Phase 6E-B-S1 verdict SHA256;
- Phase 6E-B-S1 trace SHA256;
- original Phase 6E-B failure incident SHA256;
- query fixture SHA256;
- catalog SHA256;
- selector protocol SHA256;
- selector implementation SHA256;
- capsule protocol SHA256;
- capsule implementation SHA256;
- generation construction authority SHA256;
- generation manifest SHA256;
- MAF object implementation SHA256;
- segment reader SHA256;
- optional frozen telemetry authority SHA256 values if used;
- reference fixture SHA256;
- source GGUF SHA256;
- source model PK;
- source generation PK;
- route trace SHA256;
- read-plan SHA256;
- access-ledger SHA256;
- exact scientific boundary flags;
- exact counts for evaluable, fallback, PASS-class, negative-class and integrity events;
- per-query read evidence;
- phase verdict.

## 41. Result scientific-boundary flags

The result must explicitly expose booleans or equivalent exact states for:

- `object_state_payload_identity_only`;
- `application_level_serialized_reads_observed`;
- `storage_device_physical_io_claimed`;
- `source_gguf_tensor_avoidance_claimed`;
- `full_model_avoidance_claimed`;
- `dense_materialization_avoidance_claimed`;
- `inference_executed`;
- `output_fidelity_claimed`;
- `answer_quality_claimed`;
- `performance_claimed`;
- `maf_native_compute`;
- `route_cache_used`;
- `relationship_expansion_used`;
- `reference_informed_route`;
- `reference_informed_read_plan`;
- `reference_informed_access_trace`.

For a valid Phase 6E-C V1 result, the non-authorized claims above must remain false and MAF-native compute must remain `disabled_unvalidated`.

## 42. Canonical serialization

The later implementation contract must freeze one exact canonical JSON convention for:

- route trace;
- read plan;
- access ledger;
- result.

The reference fixture's historical terminal-LF convention must remain reference-specific and must not silently change global result canonicalization.

No serialization convention may be changed after authoritative execution.

## 43. Single authoritative execution rule

Phase 6E-C V1 receives exactly one authoritative scientific execution slot only after:

1. this preregistration is frozen;
2. a dedicated Phase 6E-C runner implementation contract is created, statically qualified, and frozen;
3. a dedicated Phase 6E-C runner is created;
4. the runner passes syntax and static semantic qualification;
5. the runner is frozen in Git;
6. a separate read-only authoritative execution preflight passes.

The execution wrapper must create an external spent-slot sentinel before invoking the runner.

No automatic retry is authorized.

## 44. Successful-result preservation

If the authoritative runner publishes a result successfully, that result MUST be preserved even if a later reporting helper, qualifier, or post-run check fails.

A successful scientific result MUST NOT be deleted merely to retry execution.

## 45. Negative-result preservation

A valid scientific FAIL or NOT_TESTABLE result must be qualified and frozen.

No post hoc selector modification, budget change, denominator change, read-boundary change, or acceptance-threshold change is permitted after observing the authoritative outcome.

## 46. No prior-result oracle use

Phase 6E-A and Phase 6E-B-S1 results are frozen predecessor evidence and provenance.

They MUST NOT be used as per-query routing inputs in Phase 6E-C.

In particular, the Phase 6E-C runner MUST NOT load from prior result artifacts:

- selected PK lists;
- required PK lists;
- recovery rounds;
- expected payload identities;
- per-query verdicts;

before its own non-oracle route and read-plan barriers are frozen.

If prior result artifacts are parsed at all during the scientific runner, that parse must occur only after the Phase 6E-C access trace is frozen and only for independent provenance/comparison purposes.

The preferred implementation is to hash prior result bytes for authority binding but not parse them during route or access construction.

## 47. No hidden-reference influence

Before the complete access ledger is frozen, the runner MUST NOT use:

- reference required-object PKs;
- reference tensor names;
- reference payload SHA256 values;
- reference sufficiency classifications;
- Phase 6E-A hidden target state;
- Phase 6E-B-S1 scientific target outcomes.

The reference fixture path and SHA may be verified as raw bytes during preflight, but semantic JSON parsing for science is prohibited until after the access-ledger freeze barrier.

## 48. No network and no publication

The authoritative experiment must perform no network access.

It must not push Git branches.

It must not publish artifacts externally.

Local exact-path Git freezing occurs only in later separate gates after independent qualification.

## 49. Repository mutation boundary

Creating this preregistration candidate authorizes only creation of:

`experiments/model_fractal/MAF_PHASE_6E_C_ACTUAL_SERIALIZED_OBJECT_READ_AVOIDANCE_PREREGISTRATION_V1.md`

It does not authorize:

- Git staging;
- commit creation;
- selector execution;
- capsule construction against live scientific inputs;
- serialized object reads for Phase 6E-C science;
- reference semantic parsing for Phase 6E-C;
- result creation;
- telemetry mutation;
- modification of frozen runtime modules;
- Phase 6E-D work;
- Phase 6F work;
- MAF-native computation;
- network access.

## 50. Static qualification requirements before preregistration freeze

Before this preregistration may be frozen, an independent read-only qualifier must verify at minimum:

1. exact branch and parent HEAD;
2. tracked worktree clean except this one untracked candidate;
3. index empty;
4. original 440-file untracked baseline preserved excluding this candidate;
5. candidate exact bytes/SHA;
6. all frozen authority paths and SHA256 values used by this document;
7. Phase 6E-A and Phase 6E-B-S1 scientific closure;
8. the original spent Phase 6E-B separation;
9. exact Phase 6E-C roadmap position;
10. frozen 40-query / 12-object population;
11. exact serialized-object denominator `312326668`;
12. exact segment-reader read boundary;
13. exact `touched_pks` capsule surface;
14. absence of any authorization for scientific execution;
15. claim-boundary exclusions for 6E-D, 6F, full-model avoidance, hardware I/O, inference, and MAF-native compute.

## 51. Required next implementation analysis after freeze

After this preregistration is frozen, the next gate is a **read-only implementation-contract discovery** that must determine:

1. the exact `read_serialized_object` signature and returned value;
2. the exact generation placement fields consumed by that reader;
3. whether the reader performs any authority reads beyond the requested segment range;
4. the exact frozen in-memory object header/metadata parsing surface;
5. how to prohibit direct object-file reads during the scientific window;
6. how to ledger successful and failed read attempts without changing behavior;
7. how to prove no source-GGUF scientific-window payload read occurred;
8. whether existing telemetry can be safely reused or should remain observationally separate;
9. the exact canonical route/read-plan/access-ledger schemas;
10. the exact one-shot runner result publication discipline.

No runner source may be created before that implementation contract is frozen.

## 52. Interpretation if PASS

A valid PASS would support only the following bounded statement:

> For the frozen 32 evaluable queries in the frozen 12-object validation generation, the preregistered non-oracle MAF route caused actual application-level serialized-object reads for only a strict subset of the catalog, every required generation-bound payload was present and verified from the bytes actually read, and no scientific-window serialized-object read event occurred for the recorded untouched catalog objects.

This would advance the Phase 6E correctness chain from:

- selected-state sufficiency;
- bounded recovery;

to:

- observed selective serialized-object read avoidance.

It would still not establish end-to-end inference avoidance or performance advantage.

## 53. Interpretation if FAIL

A valid FAIL would establish that, under this frozen path and observation boundary, one or more evaluable queries either:

- required the full 12-object catalog;
- failed to actually read required state;
- read mismatching payload state;

despite the prior sufficiency/recovery results.

That negative result would be scientifically meaningful and must be preserved.

## 54. Current authorization state

At candidate creation time:

- Phase 6E-A: complete / frozen / PASS;
- original Phase 6E-B execution: spent infrastructure/integrity failure;
- original Phase 6E-B result: absent permanently;
- Phase 6E-B-S1: complete / frozen / PASS;
- Phase 6E-C instrumentation-surface discovery: complete / qualified;
- Phase 6E-C preregistration: candidate only;
- Phase 6E-C implementation contract: absent;
- Phase 6E-C runner: absent;
- Phase 6E-C result: absent;
- Phase 6E-C scientific execution: not authorized;
- Phase 6E-D: not entered;
- Phase 6F: not entered;
- MAF-native compute: disabled / unvalidated.

## 55. Next gate

After this candidate passes independent static qualification, the next authorized mutation is:

`FREEZE PHASE 6E-C PROSPECTIVE PREREGISTRATION`

Only after that freeze may the dedicated Phase 6E-C runner implementation contract be designed and created.

No Phase 6E-C scientific execution is authorized by this preregistration candidate.
