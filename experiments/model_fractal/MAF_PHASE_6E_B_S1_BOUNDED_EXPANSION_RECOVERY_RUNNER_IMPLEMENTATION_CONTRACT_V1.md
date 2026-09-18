# MAF Phase 6E-B-S1 Bounded Expansion Recovery Runner Implementation Contract V1

**STATUS: PROSPECTIVE RUNNER IMPLEMENTATION CONTRACT — NO S1 RUNNER EXISTS — NO S1 SCIENCE EXECUTED**

## 1. Purpose

This contract defines the exact implementation requirements for the dedicated Phase 6E-B-S1 bounded-expansion recovery runner.

It is subordinate to the frozen Phase 6E-B-S1 prospective preregistration and must not broaden, reinterpret, or modify the scientific question.

The runner implementation is authorized only after this contract is frozen.

## 2. Frozen S1 preregistration authority

Frozen preregistration:

`experiments/model_fractal/MAF_PHASE_6E_B_S1_BOUNDED_EXPANSION_RECOVERY_PREREGISTRATION_V1.md`

SHA256:

`823853c71e378d2a559c95d80177990bea59e546965ce579cae9e589aa3991bf`

Freeze commit:

`1c15d26e0fe036c68dc9234cc5401eba84ee6770`

The S1 runner MUST bind this exact preregistration SHA256 in source constants and in any produced S1 result.

## 3. Frozen predecessor incident authority

Frozen incident:

`experiments/model_fractal/MAF_PHASE_6E_B_EXECUTION_FAILURE_INCIDENT_AND_CORRECTIVE_SUCCESSOR_DESIGN_V1.md`

SHA256:

`1ecf171bee1e6470d5ac48c1482a2166eca05c895313eeb4acbc8e90b64a64ad`

The incident records that the original Phase 6E-B execution slot is spent.

The original Phase 6E-B runner MUST NOT be imported, called, or executed by S1.

The original Phase 6E-B result path MUST remain absent permanently.

## 4. Frozen predecessor runner identity

Original spent runner:

`experiments/model_fractal/maf_phase_6e_b_bounded_expansion_recovery_v1.py`

SHA256:

`c7e1efc2a5fddb85c49962f993be34709405979a5e9e60183a6975c7d18ee891`

Git blob:

`bec368adebaab497b9321a860135c1411f7194f1`

This runner is historical evidence only.

It MUST NOT be executed again.

It MUST NOT be imported by S1.

It MAY be read during static construction only to prove which implementation defect is being corrected, but no scientific output from that spent execution may be reconstructed or consumed.

## 5. S1 runner and result identities

Reserved S1 runner path:

`experiments/model_fractal/maf_phase_6e_b_s1_bounded_expansion_recovery_v1.py`

Reserved S1 result path:

`experiments/model_fractal/maf_phase_6e_b_s1_bounded_expansion_recovery_v1.json`

S1 result schema:

`openmind.maf_phase_6e_b_s1_bounded_expansion_recovery.v1`

S1 trace schema:

`openmind.maf_phase_6e_b_s1_expansion_trace_snapshot.v1`

Before runner construction:

- S1 runner path must be absent;
- S1 result path must be absent;
- original Phase 6E-B result path must remain absent;
- tracked worktree must be clean;
- index must be empty;
- canonical untracked baseline must match the frozen repository checkpoint.

## 6. Frozen scientific authorities

The runner MUST bind and verify all of the following exact files before scientific execution.

### Phase 6E-A result

Path:

`experiments/model_fractal/maf_phase_6e_a_selective_working_set_sufficiency_v1.json`

SHA256:

`f86433603e68fc9f1e5c65f7d3ecbd8d9ce9313d252c605dd6e2cada18a91c86`

### Phase 6E-A verdict

Path:

`experiments/model_fractal/MAF_PHASE_6E_A_SELECTIVE_WORKING_SET_SUFFICIENCY_V1_VERDICT.md`

SHA256:

`a6c9ce2f2207beb252b2c02b47e27878b27e72736dad4275ab9905d40812e334`

### Phase 6E entry checkpoint

Path:

`experiments/model_fractal/MAF_PHASE_6E_ENTRY_CHECKPOINT.md`

SHA256:

`1807437ea97e46a6cc687adbbe8c384dabae45a562f1d2aef6bd37e43b4bbe35`

### Query-scoped architecture

Path:

`experiments/model_fractal/MAF_QUERY_SCOPED_WORKING_SET_ARCHITECTURE.md`

SHA256:

`7df826096e506d13502e442fb11f7e1f18fb2c5a342f4214b91a3c3df043559c`

### Query Capsule protocol

Path:

`experiments/model_fractal/MAF_QUERY_CAPSULE_DATA_MODEL_V1_PROTOCOL.md`

SHA256:

`5255a58c8c6340c251e24ae8543760fcd66a8deb8be1a8356ad5b78ad898edda`

### Query Capsule implementation

Path:

`experiments/model_fractal/maf_query_capsule_data_model_v1.py`

SHA256:

`f897b97011714f3c84b7350c6bb53e800232be8a5d34e5148a3e50a81952976e`

### Selector protocol

Path:

`experiments/model_fractal/MAF_QUERY_TO_PK_SELECTION_V1_PROTOCOL.md`

SHA256:

`b42a0643976c2393871e3b826ba5573b4de981b49603de63230d69cf57be0811`

### Selector implementation

Path:

`experiments/model_fractal/maf_query_to_pk_selection_v1.py`

SHA256:

`e21c05e352fe921b791e8c936425727a98911ce7566989672a96bfd2b9613fa2`

### Query fixture

Path:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_queries.json`

SHA256:

`32f4636bd5e8ceee0dca8342335279a6f8e6acafe866a5469f2c23aa2655202a`

### Catalog

Path:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_catalog.json`

SHA256:

`c51ef0fabeb10e7c8a091a093aa1934620a69b2026b5a87cb02477b9dd7ca900`

### Generation construction authority

Path:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_generation_construction_authority.json`

SHA256:

`a5e953ae2ab2dd11a9f6dc564ae5ee57cb064d6eea0a8a5517191b4a6efc1a6d`

### Generation manifest

Path:

`results/runtime/maf_query_to_pk_selection_validation_v1_generation/validation_generation.manifest.json`

SHA256:

`28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3`

### Frozen reference fixture

Path:

`experiments/model_fractal/maf_phase_6e_a_reference_state_fixture_v1.json`

SHA256:

`870b656e0c3181ec8f7be1537bdeafde10fffd1b947f5372d21cdee4c00a83a0`

### MAF object implementation

Path:

`experiments/model_fractal/maf_object_v1.py`

SHA256:

`eed6cbd96995412a632883f3c534f9023e7711ea8eb437afe35a48312502f63b`

## 7. Frozen model and generation identity

Source model PK:

`mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258`

Source generation PK:

`mafgen:v1:45a80a2aa271ce04853003185b6a1227cb309bd1e3e2dc538eea849fac9f5db0`

Source manifest SHA256:

`28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3`

Source GGUF:

`/data/data/com.termux/files/home/qwen2.5-coder-q8_0.gguf`

Source GGUF SHA256:

`507de59046601282ba768a9789900e6ccf60ed93ddf346730b7c68eb0715bc47`

## 8. Only permitted corrective delta

The global canonical JSON function MUST remain unchanged from the failed 6E-B runner:

```python
def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
```

No terminal LF may be added to the global `canonical_bytes`.

The S1 runner MUST add a reference-fixture-specific helper equivalent to:

```python
def canonical_reference_fixture_bytes(value):
    return canonical_bytes(value) + b"\n"
```

The S1 reference loader MUST use the reference-specific helper for exactly this check:

```python
need(
    canonical_reference_fixture_bytes(fixture) == raw,
    "reference fixture is not canonical JSON with terminal LF",
)
```

The reference-specific terminal-LF correction MUST NOT be used for:

- query fixture canonicalization;
- catalog canonicalization;
- Query Capsule canonicalization;
- trace snapshot canonicalization;
- trace SHA256 computation;
- result serialization.

No other implementation correction is authorized by this contract.

## 9. Query and catalog loading

The runner must read and SHA-verify the frozen query fixture before any selector call.

It must require:

- canonical no-LF JSON bytes;
- exactly 40 queries;
- exactly 24 `specific_intent`;
- exactly 8 `multi_target_intent`;
- exactly 8 `fallback_control`;
- 40 unique query IDs;
- frozen generation PK;
- frozen manifest SHA256.

The runner must read and SHA-verify the frozen catalog before any selector call.

It must require:

- canonical no-LF JSON bytes;
- successful `MAFQueryPKCatalogV1.from_mapping`;
- exact canonical round trip;
- exact catalog SHA256 through the selector API;
- exact source generation and manifest binding;
- exactly 12 unique object PKs.

## 10. Fixed round configurations

The runner MUST use the frozen selector helper:

`default_selection_config_v1(max_candidates=budget)`

for the exact candidate budgets:

`(1, 2, 3, 4)`

The resulting selection-config SHA256 sequence MUST equal:

Round 0:

`2dd2925a3d9f63197deff6dc98f951c5177dc63dc08818b6492228dbac7d5576`

Round 1:

`57f751a3a019bccd58c5c32b4f5ecaf78283f49cc146896d61492ce31dfdd1c6`

Round 2:

`67dd6e5589cb16374e949b3ed633c3364f0ccb1d8c2b0a9ca1c6eaa2d2ceed56`

Round 3:

`0caeaeaafdd870e6b02ccc8b4450576883d4ef5234ba689c472e3b14d9dbe120`

Any mismatch is an infrastructure/integrity failure.

## 11. Selector execution rule

For every round and query, call exactly:

`select_query_to_pks_v1`

with:

- frozen query text;
- frozen typed catalog;
- current frozen round config;
- frozen source generation PK;
- frozen source manifest SHA256.

The result must satisfy:

- result source generation PK equals frozen generation PK;
- result source manifest SHA256 equals frozen manifest SHA256;
- result catalog SHA256 equals frozen catalog SHA256;
- result selection-config SHA256 equals the current round config SHA256;
- selected object count is less than or equal to the current candidate budget;
- no selected PK duplicates;
- every selected PK belongs to the frozen catalog.

## 12. Deterministic monotonic expansion

Round zero:

- `additional_pks` equals the round-zero selection in selector order;
- cumulative route order equals the round-zero selection.

Rounds one through three:

- previous selected set MUST be a subset of current selected set;
- query signature MUST remain unchanged;
- fallback classification MUST remain unchanged;
- `additional_pks` consists only of selected PKs not present in the previous selected set, preserving current selector order;
- cumulative route order appends only `additional_pks`;
- cumulative route order MUST contain no duplicate PKs;
- cumulative route set MUST equal the current selected set.

Selector non-monotonicity is an infrastructure/integrity failure and MUST NOT be interpreted as a scientific `FAIL`.

## 13. Round-zero Query Capsules

The runner must complete all 40 round-zero selector calls before constructing any round-one selection.

It must then construct exactly 40 round-zero `MAFQueryCapsuleV1` instances.

Each capsule must use:

- `schema = QUERY_CAPSULE_SCHEMA`;
- deterministic query PK from `derive_query_pk`;
- round-zero query signature;
- frozen source generation PK;
- frozen source manifest SHA256;
- `initial_object_pks` equal to round-zero selected PKs;
- `selected_relationship_pks = ()`;
- `route_order` equal to round-zero selected PK order;
- `expansion_policy = "bounded_v1"`;
- `max_object_budget = 4`;
- `max_expansion_rounds = 3`;
- round-zero selection-config SHA256.

Each capsule MUST:

- pass frozen source binding;
- canonicalize using the capsule implementation;
- round-trip exactly through `from_json_bytes`;
- produce a canonical capsule SHA256 for trace recording.

## 14. Barriered anti-leakage schedule

The runner MUST implement this exact scientific schedule:

1. verify repository, result-slot, frozen authority, and GGUF identities;
2. import only frozen selector, capsule, and MAF object modules;
3. load query fixture and catalog;
4. load non-reference generation authority and generation manifest bindings;
5. construct and verify all four selection configurations;
6. execute all 40 round-zero selector calls;
7. construct all 40 round-zero capsules;
8. execute all 40 round-one selector calls;
9. execute all 40 round-two selector calls;
10. execute all 40 round-three selector calls;
11. construct one complete 40-query S1 expansion trace;
12. canonicalize that trace with the unchanged no-LF global `canonical_bytes`;
13. compute the trace SHA256;
14. only then read the frozen reference fixture bytes;
15. SHA-verify the reference fixture;
16. deserialize the reference JSON;
17. validate exact reference bytes using the reference-specific terminal-LF canonicalizer;
18. classify initial sufficiency and recovery;
19. inspect generation-bound MAF payloads;
20. build the S1 result;
21. publish the S1 result using exclusive creation;
22. verify the published result and repository state.

No early stopping is permitted.

All 40 queries execute all four rounds regardless of apparent sufficiency.

## 15. Complete trace construction

The trace object MUST use schema:

`openmind.maf_phase_6e_b_s1_expansion_trace_snapshot.v1`

Run-level fields must include:

- schema;
- source generation PK;
- source manifest SHA256;
- query fixture SHA256;
- catalog SHA256;
- selector implementation SHA256;
- capsule implementation SHA256;
- expansion policy;
- max object budget;
- max expansion rounds;
- four round config SHA256 values;
- exactly 40 query trace records.

Each query trace record must include:

- query ID;
- query signature;
- query PK;
- round-zero capsule SHA256;
- exactly four round records.

Each round record must include:

- round index;
- candidate budget;
- selection-config SHA256;
- selected object PKs;
- selected count;
- additional PKs;
- cumulative route order.

The complete trace MUST be canonicalized and SHA256-hashed before the reference fixture is deserialized.

## 16. Trace anti-oracle prohibition

Before the reference fixture is deserialized, no trace state may contain or derive from:

- required object PK;
- required object PK set;
- expected payload SHA256;
- reference payload SHA256;
- reference object metadata;
- reference target;
- initial sufficiency classification;
- recovery round;
- recovery verdict;
- Phase verdict.

The runner must not load, parse, deserialize, import, or otherwise consume reference fixture contents before the complete trace SHA256 is computed.

The frozen reference fixture path and frozen SHA256 may exist as source constants and may be SHA-verified after trace construction.

## 17. Reference fixture loading

The reference loader MUST execute only after complete trace SHA256 computation.

It must:

1. read exact reference bytes;
2. require exact frozen SHA256;
3. deserialize UTF-8 JSON;
4. require `canonical_reference_fixture_bytes(fixture) == raw`;
5. require frozen source model PK;
6. require frozen source generation PK;
7. require frozen source manifest SHA256;
8. require frozen source GGUF SHA256;
9. require exactly 40 reference query records;
10. require query order to equal the frozen query fixture order.

The helper error message should make the terminal-LF convention explicit to prevent future ambiguity.

## 18. Generation binding

After the trace is frozen in process state, the runner may use the already loaded non-reference generation authority and generation manifest bindings.

It must require:

- frozen authority SHA256;
- frozen generation manifest SHA256;
- exact generation PK;
- exact model PK;
- 12 generation descriptor objects;
- 12 unique descriptor object PKs;
- 12 authority targets;
- 12 unique authority object PKs;
- exact dedicated objects directory path.

For every required object used as recovery evidence, the PK must exist in both descriptor and authority mappings.

## 19. Actual MAF payload inspection

For a required PK under evaluation:

1. locate the exact target object filename from frozen authority;
2. require the object file to exist;
3. compute serialized object SHA256;
4. require serialized object SHA256 equals generation descriptor `object_file_sha256`;
5. require descriptor payload SHA256 equals independent frozen reference payload SHA256;
6. call frozen `maf_object_v1.inspect_object`;
7. require tensor name equality;
8. require tensor type equality;
9. require dims equality;
10. require element count equality;
11. require observed payload SHA256 equals descriptor payload SHA256;
12. require observed payload SHA256 equals independent frozen reference payload SHA256.

Payload evidence must include at minimum:

- object PK;
- serialized object SHA256;
- descriptor payload SHA256;
- reference payload SHA256;
- observed payload SHA256;
- descriptor payload match;
- reference payload match;
- final payload match.

Metadata-only evidence is insufficient.

## 20. Initial sufficiency classification

For each non-fallback query:

`initial_missing = required_set - round_zero_selected_set`

If empty:

`INITIAL_SUFFICIENT`

The query is excluded from challenge numerator and denominator.

If nonempty:

`INITIAL_INSUFFICIENT`

The query enters the challenge denominator.

For `fallback_control`:

- required set MUST be empty;
- classification is `CONTROL`;
- query is excluded from challenge numerator and denominator.

## 21. Earliest recovery classification

For every `INITIAL_INSUFFICIENT` query, examine rounds 1, 2, and 3 in ascending order.

The earliest recovery round is the first round where:

- no required PK is missing;
- every required object has full generation-bound payload evidence;
- every required payload matches;
- no payload mismatch exists.

If found:

query verdict:

`RECOVERED`

If not found by round 3:

query verdict:

`NOT_RECOVERED`

`INITIAL_SUFFICIENT` queries retain verdict `INITIAL_SUFFICIENT`.

Fallback controls retain verdict `CONTROL`.

## 22. Phase count invariants

The runner must produce and verify:

- 40 query results;
- query order equal to frozen input order;
- `challenge_count + initial_sufficient_count == 32`;
- `fallback_control_count == 8`;
- `recovered_count + not_recovered_count == challenge_count`.

Any count inconsistency is an infrastructure/integrity failure.

## 23. S1 scientific verdict

If:

`challenge_count == 0`

then:

`phase_verdict = "NOT_TESTABLE"`

This is not positive evidence.

Else if:

`not_recovered_count > 0`

then:

`phase_verdict = "FAIL"`

Else require:

- `recovered_count == challenge_count`;
- `not_recovered_count == 0`;

and set:

`phase_verdict = "PASS"`

Infrastructure or integrity errors must terminate separately and MUST NOT be mapped to scientific `PASS`, `FAIL`, or `NOT_TESTABLE`.

## 24. S1 result fields

The S1 result MUST bind and expose at minimum:

- schema;
- phase `6E-B-S1`;
- S1 preregistration SHA256;
- S1 runner implementation contract SHA256;
- frozen failure incident SHA256;
- original spent Phase 6E-B runner SHA256;
- original spent execution status;
- original result state;
- Phase 6E-A result SHA256;
- Phase 6E-A verdict SHA256;
- reference fixture SHA256;
- Phase 6E entry checkpoint SHA256;
- query-scoped architecture SHA256;
- capsule protocol SHA256;
- capsule implementation SHA256;
- selector protocol SHA256;
- selector implementation SHA256;
- query fixture SHA256;
- catalog SHA256;
- generation authority SHA256;
- MAF object implementation SHA256;
- source model PK;
- source generation PK;
- source manifest SHA256;
- source GGUF SHA256;
- expansion policy;
- max object budget;
- max expansion rounds;
- four round config SHA256 values;
- S1 trace snapshot SHA256;
- class counts;
- query count;
- challenge count;
- initial sufficient count;
- recovered count;
- not recovered count;
- fallback control count;
- exactly 40 query records;
- phase verdict;
- scientific boundary flags.

## 25. Per-query S1 result fields

Every query record MUST include:

- query ID;
- query class;
- query text SHA256;
- query signature;
- query PK;
- source generation PK;
- round-zero capsule SHA256;
- all four immutable round records;
- round-zero selected PKs;
- round-zero missing required PKs;
- required object PKs;
- initial sufficiency classification;
- earliest recovery round;
- final selected PKs;
- final covered required PKs;
- final missing required PKs;
- payload mismatch PKs;
- required-object payload evidence;
- additional PKs by round;
- final cumulative route order;
- verdict.

## 26. Scientific boundary flags

The result must explicitly state at least:

- `object_state_payload_identity_only = True`;
- `selector_fresh_invocations = True`;
- `fixed_round_schedule_completed_before_reference_parse = True`;
- `reference_informed_expansion = False`;
- `reference_specific_terminal_lf_validation = True`;
- `global_canonical_bytes_terminal_lf = False`;
- `route_cache_used = False`;
- `relationship_expansion_used = False`;
- `inference_executed = False`;
- `actual_object_avoidance_claimed = False`;
- `actual_tensor_avoidance_claimed = False`;
- `output_fidelity_claimed = False`;
- `answer_quality_claimed = False`;
- `performance_claimed = False`;
- `maf_native_compute = "disabled_unvalidated"`.

## 27. Result publication

The S1 result MUST be serialized using the unchanged no-LF global `canonical_bytes`.

Publication MUST use exclusive creation equivalent to:

`os.O_WRONLY | os.O_CREAT | os.O_EXCL`

The runner MUST:

- refuse to run if S1 result already exists;
- never overwrite S1 result;
- flush and `fsync` the result;
- reread and compare exact bytes after write;
- verify tracked worktree remains clean;
- verify index remains empty;
- verify S1 result is exactly one additional untracked path beyond the frozen baseline.

If writing itself raises after file creation, a partially created result may be removed only as part of the runner's own write-failure cleanup before any successful result exists.

A successfully written scientific result MUST NOT be deleted because of a later wrapper, reporting, or qualification failure.

## 28. Repository pre-execution gate

The S1 runner MUST fail closed before importing frozen scientific modules unless all are true:

- branch is the frozen scientific branch;
- HEAD equals the future frozen S1 runner commit expected by the execution wrapper;
- tracked worktree is clean;
- index is empty;
- untracked baseline exactly matches the frozen baseline;
- S1 result path is absent;
- original Phase 6E-B result path is absent;
- all frozen authority files exist and match exact SHA256;
- source GGUF exists and matches exact SHA256.

Because the runner cannot know its future commit hash while being constructed, static qualification must verify that the pre-execution function contains a runner-commit binding mechanism or that the execution wrapper supplies the exact HEAD gate before invoking the runner. At minimum, no S1 science may execute unless the frozen S1 runner commit has been independently verified immediately before launch.

## 29. Module import boundary

The runner may dynamically import only:

- `maf_query_to_pk_selection_v1`;
- `maf_query_capsule_data_model_v1`;
- `maf_object_v1`.

It MUST NOT import or call:

- original spent Phase 6E-B runner;
- `maf_query_to_pk_selection_validation_v1_4.py`;
- Query Route Cache implementation;
- network clients;
- HTTP clients;
- socket clients;
- inference engines.

Standard-library imports required for deterministic file, hashing, JSON, Git, and process-state checks are permitted.

## 30. No Route Cache or relationships

Query Route Cache is disabled.

No Route Cache module may be imported or called.

`selected_relationship_pks` MUST remain an empty tuple.

No relationship PK or transition PK may influence:

- selection;
- expansion;
- route order;
- trace state;
- classification;
- payload evidence;
- verdict.

## 31. No original-run reuse

S1 MUST NOT:

- call the original Phase 6E-B runner;
- import the original Phase 6E-B runner;
- create the original Phase 6E-B result path;
- consume any hidden or reconstructed trace from the spent execution;
- use any scientific target outcome from the spent execution.

The original execution contributes only the frozen infrastructure fact documented in the incident: the reference fixture requires one terminal LF for exact canonical-byte validation.

## 32. Static qualification requirements before runner creation

Before any S1 runner bytes may be admitted into the repository, a construction helper must prove at minimum:

- exact branch and parent HEAD;
- exact frozen untracked baseline;
- S1 preregistration exact SHA256;
- this S1 implementation contract exact SHA256;
- incident exact SHA256;
- all frozen authority SHA256 bindings;
- S1 runner path absent;
- S1 result path absent;
- original result path absent;
- Python syntax and AST compile;
- original spent runner not imported or called;
- spent Q2 V1.4 not imported or called;
- no network/Route Cache import surface;
- unchanged no-LF global canonicalizer;
- explicit reference-specific terminal-LF helper;
- reference loader uses only the reference-specific helper;
- query/catalog/trace/result continue using no-LF canonicalization;
- exact candidate budgets 1, 2, 3, 4;
- exact four config SHA256 values;
- all-round barrier schedule;
- all 40 round-zero calls before capsule completion;
- all 40 capsules before round one;
- all round one before round two;
- all round two before round three;
- trace SHA before reference deserialization;
- no reference field in pre-reference functions;
- exact capsule fields;
- monotonicity enforcement;
- full generation-bound payload verification;
- exact classification and phase verdict logic;
- O_EXCL result publication;
- no science execution during construction/static qualification.

## 33. Runner freeze requirements

After S1 runner creation and static qualification:

1. independently reread and hash the runner;
2. independently AST-review the correction and anti-leakage order;
3. stage only the exact S1 runner path;
4. require a sole ADD;
5. require mode `100644`;
6. verify staged blob equals worktree blob;
7. commit the runner;
8. verify exact parent;
9. verify exact commit message;
10. verify exact sole ADD;
11. verify worktree clean;
12. verify index empty;
13. verify frozen untracked baseline restored;
14. verify S1 result remains absent;
15. verify original result remains absent.

The runner MUST NOT be imported or executed during its freeze.

## 34. Authoritative S1 execution preflight

After the S1 runner is frozen, a separate read-only preflight must verify:

- exact S1 runner commit;
- exact runner bytes, SHA256, and Git blob;
- exact S1 preregistration;
- exact S1 runner contract;
- exact frozen incident;
- exact scientific authorities;
- exact source GGUF;
- all 12 serialized generation-bound object files;
- exact four config SHA256 derivations;
- trace-before-reference static order;
- reference-specific LF helper and loader use;
- original result absent;
- S1 result absent;
- repository unchanged after reads.

The preflight MUST NOT:

- import the S1 runner;
- call the selector;
- construct capsules;
- execute expansion;
- deserialize the reference fixture;
- call `inspect_object`;
- create any result.

## 35. Single authoritative S1 execution

Only after the separate preflight passes may an execution wrapper launch the frozen S1 runner exactly once.

The wrapper MUST:

- reverify frozen runner identity immediately before launch;
- verify S1 result absence immediately before launch;
- invoke the runner exactly once;
- never retry automatically;
- preserve any produced scientific result;
- treat infrastructure/integrity failure separately from scientific verdict;
- avoid network access;
- avoid Git mutation.

If the frozen S1 runner terminates before scientific result publication with an infrastructure/integrity failure, the S1 execution slot becomes spent and a future corrective successor would require another new prospective identity.

## 36. Independent result qualification

Any produced S1 result must be independently qualified without rerunning selector or science.

Qualification must verify:

- canonical no-LF JSON serialization;
- exact result schema;
- all frozen authority bindings;
- 40 query records;
- exact class counts;
- exact four round records per query;
- exact candidate budgets and config SHAs;
- reconstructed trace SHA equals result trace SHA;
- challenge arithmetic;
- query verdict counts;
- phase verdict arithmetic;
- payload evidence completeness and exact identities;
- original result remains absent;
- result is the sole additional untracked path beyond frozen baseline.

No scientific result may be rewritten merely because a later qualification fails.

## 37. Result freeze

After independent qualification, the S1 result may be frozen as a sole ADD commit.

The result freeze must not modify the runner, preregistration, incident, original result path, or any authority.

A later narrow verdict document may summarize only the frozen result and its bounded scientific interpretation.

## 38. Implementation non-goals

The S1 runner MUST NOT add:

- inference;
- generation;
- logit comparison;
- answer comparison;
- output fidelity claims;
- object avoidance claims;
- tensor avoidance claims;
- performance benchmarks;
- memory benchmarks;
- I/O benchmarks;
- energy benchmarks;
- Route Cache;
- relationship expansion;
- alternative selector logic;
- alternate ranking;
- adaptive budgets;
- adaptive stopping;
- target-aware selection;
- target-aware expansion.

## 39. Contract interpretation rule

If a future implementation detail is ambiguous, choose the narrowest behavior that preserves:

1. the frozen S1 preregistration;
2. the frozen incident boundary;
3. the exact scientific design of original Phase 6E-B;
4. the one allowed reference-specific terminal-LF correction;
5. the trace-before-reference anti-leakage barrier;
6. deterministic fail-closed behavior.

Ambiguity MUST NOT be resolved by consulting target outcomes.

## 40. Current authorization boundary

At contract-candidate creation time:

- original Phase 6E-B runner: frozen and spent;
- original Phase 6E-B result: absent permanently;
- failure incident: frozen;
- S1 preregistration: frozen;
- S1 runner implementation contract: candidate only;
- S1 runner: absent;
- S1 result: absent;
- S1 selector execution: not authorized;
- S1 expansion execution: not authorized;
- S1 reference deserialization: not authorized;
- S1 payload inspection: not authorized;
- S1 scientific execution: not authorized.

## 41. Next gate

After this implementation contract candidate passes independent static qualification, the next authorized mutation is:

`FREEZE PHASE 6E-B-S1 RUNNER IMPLEMENTATION CONTRACT`

Only after that freeze may S1 runner source bytes be created.
