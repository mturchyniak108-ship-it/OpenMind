# MAF Phase 6E-B-S1 Bounded Expansion Recovery Preregistration V1

**STATUS: PROSPECTIVE PREREGISTRATION — NO S1 RUNNER EXISTS — NO S1 SCIENCE EXECUTED**

## 1. Purpose

This document preregisters Phase 6E-B-S1, a prospective corrective successor to the spent Phase 6E-B execution.

Phase 6E-B-S1 exists only because the first frozen Phase 6E-B runner terminated on an implementation integrity error before any recovery classification or payload inspection occurred.

The successor does not reinterpret, repair, resume, or rerun the original execution. It is a new prospective experiment with new immutable runner and result identities.

## 2. Frozen predecessor and incident authorities

Scientific branch:

`labs/multidimensional-maf`

Current predecessor checkpoint before this preregistration candidate:

`4691293d3dbecbb55880a8bfaf10e59b61fef1d6`

Frozen original Phase 6E-B preregistration:

`experiments/model_fractal/MAF_PHASE_6E_B_BOUNDED_EXPANSION_RECOVERY_PREREGISTRATION_V1.md`

Original Phase 6E-B preregistration SHA256:

`85b44a1e78193f020c54b12f9b0698b8c20cc3a69365647b9520132d4b01dacd`

Frozen original Phase 6E-B runner implementation contract:

`experiments/model_fractal/MAF_PHASE_6E_B_BOUNDED_EXPANSION_RECOVERY_RUNNER_IMPLEMENTATION_CONTRACT_V1.md`

Original runner implementation contract SHA256:

`747261cce78f770401155e4823bc3558bc6e41770f107d35a965e014e5cc6fb5`

Frozen original Phase 6E-B runner commit:

`79a225e9124705704e87070ace79958a29fdd4dc`

Frozen original Phase 6E-B runner:

`experiments/model_fractal/maf_phase_6e_b_bounded_expansion_recovery_v1.py`

Original runner SHA256:

`c7e1efc2a5fddb85c49962f993be34709405979a5e9e60183a6975c7d18ee891`

Frozen failure incident:

`experiments/model_fractal/MAF_PHASE_6E_B_EXECUTION_FAILURE_INCIDENT_AND_CORRECTIVE_SUCCESSOR_DESIGN_V1.md`

Failure incident SHA256:

`1ecf171bee1e6470d5ac48c1482a2166eca05c895313eeb4acbc8e90b64a64ad`

Original Phase 6E-B result path:

`experiments/model_fractal/maf_phase_6e_b_bounded_expansion_recovery_v1.json`

Original result state:

`ABSENT PERMANENTLY`

The original execution slot is spent and MUST NOT be reused.

The original frozen Phase 6E-B runner MUST NOT be executed again.

## 3. Incident fact available to the successor

The only implementation fact learned from the spent execution that may inform Phase 6E-B-S1 is:

The frozen reference fixture is compact canonical JSON followed by exactly one terminal LF byte, while the frozen Phase 6E-B runner validated it using compact canonical JSON without that terminal LF.

Observed exact convention:

`reference_raw == compact_canonical_json_bytes(reference_value) + b"\n"`

The failure occurred after complete non-oracle four-round trace construction and reference JSON deserialization, but before:

- required-object classification;
- initial sufficiency classification;
- recovery classification;
- MAF payload inspection;
- result construction;
- scientific verdict publication.

No required-object PKs, reference payload identities, recovery outcomes, challenge denominator, recovered count, not-recovered count, or Phase 6E-B scientific verdict were observed.

The unpersisted trace SHA from the spent execution is not available to this successor and MUST NOT be reconstructed or inferred from hidden state.

## 4. Corrective scope

Phase 6E-B-S1 permits exactly one implementation correction:

A reference-fixture-specific canonical-byte rule equivalent to:

`canonical_reference_fixture_bytes(value) = canonical_bytes(value) + b"\n"`

The successor reference loader must verify:

`canonical_reference_fixture_bytes(reference_fixture) == reference_raw`

The global `canonical_bytes` convention MUST remain:

- UTF-8;
- `sort_keys=True`;
- `ensure_ascii=False`;
- separators `(",", ":")`;
- no terminal LF.

This no-LF global canonicalizer remains authoritative for:

- frozen query fixture canonical checks;
- frozen catalog canonical checks;
- S1 trace snapshot canonicalization;
- S1 trace SHA256 computation;
- S1 result serialization.

No other corrective implementation change is authorized by this preregistration.

## 5. Scientific question

For the same frozen 40-query population, can deterministic non-oracle bounded expansion recover every required generation-bound MAF object payload when the initial working set is deliberately constrained to selector candidate budget 1?

This question is unchanged from the original Phase 6E-B preregistration.

## 6. Scientific boundary

Phase 6E-B-S1 is limited to object-state payload identity.

It does not test or claim:

- model inference;
- token generation;
- answer correctness;
- output/logit parity;
- answer quality;
- actual object avoidance;
- actual tensor avoidance;
- I/O performance;
- memory performance;
- latency;
- throughput;
- energy;
- MAF-native compute.

Generation-bound serialized MAF objects and their actual payloads remain required evidence.

## 7. Frozen source authorities

Phase 6E-B-S1 must bind to the same frozen authorities used by Phase 6E-B.

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

### Query-scoped working-set architecture

Path:

`experiments/model_fractal/MAF_QUERY_SCOPED_WORKING_SET_ARCHITECTURE.md`

SHA256:

`7df826096e506d13502e442fb11f7e1f18fb2c5a342f4214b91a3c3df043559c`

### Query Capsule protocol

Path:

`experiments/model_fractal/MAF_QUERY_CAPSULE_DATA_MODEL_V1_PROTOCOL.md`

SHA256:

`5255a58c8c6340c251e24ae8543760fcd66a8deb8be1a8356ad5b78ad898edda`

### Selector protocol

Path:

`experiments/model_fractal/MAF_QUERY_TO_PK_SELECTION_V1_PROTOCOL.md`

SHA256:

`b42a0643976c2393871e3b826ba5573b4de981b49603de63230d69cf57be0811`

### Query fixture

Path:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_queries.json`

SHA256:

`32f4636bd5e8ceee0dca8342335279a6f8e6acafe866a5469f2c23aa2655202a`

Population:

- 40 total queries;
- 24 `specific_intent`;
- 8 `multi_target_intent`;
- 8 `fallback_control`.

### Catalog

Path:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_catalog.json`

SHA256:

`c51ef0fabeb10e7c8a091a093aa1934620a69b2026b5a87cb02477b9dd7ca900`

Catalog object count:

`12`

### Selector implementation

Path:

`experiments/model_fractal/maf_query_to_pk_selection_v1.py`

SHA256:

`e21c05e352fe921b791e8c936425727a98911ce7566989672a96bfd2b9613fa2`

### Query Capsule implementation

Path:

`experiments/model_fractal/maf_query_capsule_data_model_v1.py`

SHA256:

`f897b97011714f3c84b7350c6bb53e800232be8a5d34e5148a3e50a81952976e`

### MAF object implementation

Path:

`experiments/model_fractal/maf_object_v1.py`

SHA256:

`eed6cbd96995412a632883f3c534f9023e7711ea8eb437afe35a48312502f63b`

### Generation construction authority

Path:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_generation_construction_authority.json`

SHA256:

`a5e953ae2ab2dd11a9f6dc564ae5ee57cb064d6eea0a8a5517191b4a6efc1a6d`

### Frozen generation manifest

Path:

`results/runtime/maf_query_to_pk_selection_validation_v1_generation/validation_generation.manifest.json`

SHA256:

`28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3`

### Frozen reference fixture

Path:

`experiments/model_fractal/maf_phase_6e_a_reference_state_fixture_v1.json`

SHA256:

`870b656e0c3181ec8f7be1537bdeafde10fffd1b947f5372d21cdee4c00a83a0`

The reference fixture contents remain prohibited from selector, capsule, expansion, scheduling, and trace state.

## 8. Frozen model and generation identity

Source model PK:

`mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258`

Source generation PK:

`mafgen:v1:45a80a2aa271ce04853003185b6a1227cb309bd1e3e2dc538eea849fac9f5db0`

Source generation manifest SHA256:

`28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3`

Source GGUF:

`/data/data/com.termux/files/home/qwen2.5-coder-q8_0.gguf`

Source GGUF SHA256:

`507de59046601282ba768a9789900e6ccf60ed93ddf346730b7c68eb0715bc47`

## 9. Fixed expansion schedule

Expansion policy:

`bounded_v1`

Maximum object budget:

`4`

Maximum expansion rounds after round zero:

`3`

All 40 queries MUST execute all four selector rounds.

No early stopping is permitted.

Round schedule:

### Round 0

`max_candidates = 1`

Selection-config SHA256:

`2dd2925a3d9f63197deff6dc98f951c5177dc63dc08818b6492228dbac7d5576`

### Round 1

`max_candidates = 2`

Selection-config SHA256:

`57f751a3a019bccd58c5c32b4f5ecaf78283f49cc146896d61492ce31dfdd1c6`

### Round 2

`max_candidates = 3`

Selection-config SHA256:

`67dd6e5589cb16374e949b3ed633c3364f0ccb1d8c2b0a9ca1c6eaa2d2ceed56`

### Round 3

`max_candidates = 4`

Selection-config SHA256:

`0caeaeaafdd870e6b02ccc8b4450576883d4ef5234ba689c472e3b14d9dbe120`

No round greater than 3 is permitted.

No candidate budget greater than 4 is permitted.

## 10. Deterministic expansion rule

For every query and every round:

1. call the exact frozen selector;
2. use the exact frozen query text;
3. use the exact frozen catalog;
4. use the exact frozen source generation PK;
5. use the exact frozen source manifest SHA256;
6. use the preregistered round configuration;
7. preserve `selected_object_pks` order exactly as returned;
8. reject duplicate selected PKs;
9. require selected count to be less than or equal to the round candidate budget;
10. require every selected PK to exist in the frozen catalog;
11. for rounds 1 through 3, require the previous round selected set to be a subset of the current selected set;
12. define `additional_pks` as current selected PKs absent from the previous selected set, preserving current selector order;
13. append only those newly admitted PKs to cumulative route order.

Any selector non-monotonicity is an infrastructure/integrity failure.

It is not a scientific `FAIL`.

## 11. Round-zero Query Capsule rule

After all 40 round-zero selector calls complete and before any round-one selector call begins, construct exactly one generation-bound `MAFQueryCapsuleV1` per query.

Each capsule must contain:

- deterministic query PK derived by the frozen capsule implementation;
- round-zero query signature;
- frozen source generation PK;
- frozen source manifest SHA256;
- `initial_object_pks` equal to round-zero selected object PKs;
- `selected_relationship_pks = ()`;
- `route_order` equal exactly to round-zero selector order;
- `expansion_policy = "bounded_v1"`;
- `max_object_budget = 4`;
- `max_expansion_rounds = 3`;
- `selection_config_sha256` equal to the round-zero selection-config SHA256.

Each capsule must pass its frozen source-binding and canonical round-trip invariants.

## 12. Global anti-leakage execution order

The S1 runner MUST implement the following barriered order:

1. verify frozen identities and repository/result-slot preconditions;
2. import only frozen selector, capsule, and MAF object modules;
3. load the frozen query fixture and catalog;
4. load non-reference generation authority and generation manifest bindings;
5. derive and verify the four selection configurations;
6. execute all 40 round-zero selector calls;
7. construct all 40 round-zero Query Capsules;
8. execute all 40 round-one selector calls;
9. execute all 40 round-two selector calls;
10. execute all 40 round-three selector calls;
11. construct one complete 40-query expansion trace snapshot;
12. canonicalize the complete trace using the unchanged no-LF global `canonical_bytes`;
13. compute and freeze the complete trace SHA256 in process state;
14. only after steps 1 through 13 complete, read and SHA-verify the frozen reference fixture;
15. deserialize the frozen reference fixture;
16. validate the reference fixture using the S1 reference-specific terminal-LF canonical-byte rule;
17. classify initial sufficiency and recovery;
18. inspect required generation-bound MAF object payloads;
19. aggregate the S1 scientific result;
20. publish the S1 result exactly once using an exclusive result path.

No reference-derived field may influence steps 1 through 13.

## 13. S1 trace snapshot

S1 trace schema:

`openmind.maf_phase_6e_b_s1_expansion_trace_snapshot.v1`

The trace must include at minimum:

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
- all four selection-config SHA256 values;
- exactly 40 query trace records.

Each query trace record must include:

- query ID;
- query signature;
- query PK;
- round-zero capsule canonical SHA256;
- exactly four round records.

Each round record must include:

- round index;
- candidate budget;
- selection-config SHA256;
- selected object PKs in selector order;
- selected count;
- additional PKs;
- cumulative route order.

The trace MUST NOT contain:

- required object PKs;
- expected payload SHA256;
- reference payload SHA256;
- reference target fields;
- scientific classification;
- recovery verdict.

## 14. Reference use after trace freeze

Only after the complete S1 trace SHA256 is frozen in process state may the runner deserialize the frozen reference fixture.

For every query:

- query text SHA256 must equal the frozen reference query text SHA256;
- required object PK ordering must be exactly the frozen reference ordering;
- fallback controls must have an empty required-object set.

No reference data may retroactively alter any selector, capsule, expansion, route, or trace record.

## 15. Initial sufficiency classification

For every non-fallback query:

`initial_missing = required_object_pks - round_zero_selected_object_pks`

If `initial_missing` is empty:

classification:

`INITIAL_SUFFICIENT`

The query is excluded from the recovery numerator and denominator.

If `initial_missing` is nonempty:

classification:

`INITIAL_INSUFFICIENT`

The query enters the Phase 6E-B-S1 challenge denominator.

Fallback controls are classified:

`CONTROL`

and are excluded from the recovery numerator and denominator.

## 16. Generation-bound payload verification

For every required object used to establish recovery:

1. the PK must exist in the frozen generation descriptor;
2. the PK must exist in the frozen generation construction authority;
3. the dedicated serialized MAF object file must exist;
4. the serialized object SHA256 must equal the generation descriptor `object_file_sha256`;
5. generation descriptor payload SHA256 must equal the independent frozen reference payload SHA256;
6. call the frozen `maf_object_v1.inspect_object`;
7. observed tensor name must equal the frozen reference tensor name;
8. observed tensor type must equal the frozen reference tensor type;
9. observed dims must equal the frozen reference dims;
10. observed element count must equal the frozen reference element count;
11. observed payload SHA256 must equal the generation descriptor payload SHA256;
12. observed payload SHA256 must equal the independent frozen reference payload SHA256.

Metadata-only agreement is insufficient.

Actual generation-bound MAF payload identity is required.

## 17. Earliest recovery rule

For every `INITIAL_INSUFFICIENT` query, evaluate rounds 1, 2, and 3 in ascending order.

The earliest recovery round is the first round for which:

- no required object PK is missing;
- every required object passes the full generation-bound payload verification rule;
- no payload mismatch exists.

If such a round exists:

query verdict:

`RECOVERED`

If no such round exists through round 3:

query verdict:

`NOT_RECOVERED`

## 18. Phase-level counts

The S1 result must report:

- total query count;
- class counts;
- challenge count;
- initial sufficient count;
- recovered count;
- not recovered count;
- fallback CONTROL count.

Required invariants:

`challenge_count + initial_sufficient_count == 32`

`recovered_count + not_recovered_count == challenge_count`

`fallback_control_count == 8`

## 19. Phase verdict rule

Phase verdict:

`NOT_TESTABLE`

iff:

`challenge_count == 0`

This is not a positive result.

Phase verdict:

`FAIL`

iff:

- `challenge_count > 0`; and
- one or more challenged queries are `NOT_RECOVERED`.

Phase verdict:

`PASS`

iff all are true:

- `challenge_count > 0`;
- `recovered_count == challenge_count`;
- `not_recovered_count == 0`;
- all 8 fallback controls are structurally valid;
- every recovered required object passes full generation-bound payload verification;
- no authority, monotonicity, capsule, anti-leakage, trace, publication, or repository invariant fails.

Infrastructure or integrity failures remain distinct from scientific `PASS`, `FAIL`, and `NOT_TESTABLE`.

## 20. S1 result identity

Reserved S1 result path:

`experiments/model_fractal/maf_phase_6e_b_s1_bounded_expansion_recovery_v1.json`

S1 result schema:

`openmind.maf_phase_6e_b_s1_bounded_expansion_recovery.v1`

The original spent Phase 6E-B result path MUST remain absent permanently.

The S1 result must include at minimum:

- result schema;
- phase label `6E-B-S1`;
- this preregistration SHA256;
- frozen failure incident SHA256;
- original Phase 6E-B runner SHA256;
- original Phase 6E-B spent execution status;
- original Phase 6E-B result state;
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
- all four selection-config SHA256 values;
- S1 expansion trace snapshot SHA256;
- class counts;
- challenge count;
- initial sufficient count;
- recovered count;
- not recovered count;
- fallback CONTROL count;
- exactly 40 per-query records;
- final S1 phase verdict;
- explicit scientific-boundary flags.

## 21. Required per-query result fields

Each S1 per-query record must include:

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
- per-required-object payload evidence;
- additional PKs by round;
- final cumulative route order;
- query verdict.

## 22. Route Cache and relationship prohibition

Query Route Cache is disabled.

No Route Cache module may be imported or called.

`selected_relationship_pks` remains empty.

No relationship PK or transition PK may affect selection, expansion, trace state, or recovery classification.

## 23. Spent Q2 validation prohibition

The spent validation implementation:

`maf_query_to_pk_selection_validation_v1_4.py`

must not be imported, called, or executed by Phase 6E-B-S1.

Its path or historical SHA may be documented only if required for provenance.

## 24. Result publication discipline

The S1 result path must be absent before the one authoritative S1 execution.

The S1 runner must publish using exclusive creation semantics equivalent to:

`os.O_WRONLY | os.O_CREAT | os.O_EXCL`

The runner must not overwrite an existing S1 result.

The runner must not delete a successfully written scientific result because a later wrapper or qualification step fails.

A produced `PASS`, `FAIL`, or `NOT_TESTABLE` result is evidence and must be preserved for independent qualification.

## 25. Single-execution rule

Phase 6E-B-S1 receives exactly one authoritative scientific execution slot after:

1. this preregistration is frozen;
2. a dedicated S1 runner implementation contract is frozen;
3. a dedicated S1 runner is created and statically qualified;
4. that S1 runner is frozen;
5. a separate read-only S1 authoritative execution preflight passes.

No S1 runner execution is authorized before all five gates complete.

If the authoritative S1 execution terminates with an infrastructure/integrity failure before result publication, that S1 execution slot becomes spent and MUST NOT be retried under the same frozen S1 runner identity.

## 26. Implementation-order commitment

The required implementation order is:

1. freeze this S1 preregistration;
2. create the dedicated S1 runner implementation contract;
3. statically qualify the contract;
4. freeze the S1 runner implementation contract;
5. create the dedicated S1 runner;
6. statically qualify exact bindings, reference-specific LF correction, schedule, capsule semantics, anti-leakage order, trace semantics, payload checks, verdict logic, O_EXCL publication, and no-network boundary;
7. freeze the S1 runner as a sole ADD commit;
8. perform a separate read-only authoritative execution preflight;
9. authorize one authoritative S1 execution only after every gate passes;
10. independently qualify any produced S1 result and reconstructed trace;
11. freeze the S1 result;
12. freeze a narrow S1 verdict document.

## 27. No adaptation after target observation

No scientific target outcome from the original spent Phase 6E-B execution was observed.

The successor therefore remains prospective with respect to:

- challenge denominator;
- initial sufficiency count;
- recovered count;
- not recovered count;
- earliest recovery rounds;
- required-object payload evidence;
- final scientific verdict.

After this preregistration is frozen, none of those rules may be changed in response to S1 results.

## 28. Success criteria for runner construction

A future S1 runner may be created only if its static qualification proves all of the following before execution:

- exact frozen authority bindings;
- exact S1 preregistration SHA256 binding;
- exact frozen failure incident SHA256 binding;
- original spent runner is never called;
- original result path remains prohibited;
- global no-LF `canonical_bytes` is unchanged;
- reference-specific terminal-LF canonical validation is explicit;
- all 40 round-zero selections precede all capsule construction completion;
- all 40 capsules precede round one;
- all round-one selections precede round two;
- all round-two selections precede round three;
- complete trace SHA is computed before reference deserialization;
- no required-object or reference payload data enters trace state;
- exact 1-to-4 candidate-budget schedule;
- exact four frozen selection-config SHA256 values;
- exact Query Capsule fields;
- monotonic selection enforcement;
- generation-bound actual payload inspection;
- exact recovery and phase verdict rules;
- exclusive result creation;
- no network operations;
- no Route Cache operations;
- no spent Q2 V1.4 execution path.

## 29. Current authorization boundary

At the time this preregistration candidate is created:

- original Phase 6E-B execution slot: spent;
- original Phase 6E-B result: absent permanently;
- failure incident: frozen;
- Phase 6E-B-S1 preregistration: candidate only;
- Phase 6E-B-S1 runner implementation contract: absent;
- Phase 6E-B-S1 runner: absent;
- Phase 6E-B-S1 result: absent;
- S1 selector execution: not authorized;
- S1 expansion execution: not authorized;
- S1 reference deserialization: not authorized;
- S1 payload inspection: not authorized;
- S1 scientific execution: not authorized.

## 30. Next gate

After this preregistration candidate passes independent static qualification, the next authorized mutation is:

`FREEZE PHASE 6E-B-S1 PROSPECTIVE PREREGISTRATION`

Only after that freeze may the dedicated S1 runner implementation contract be created.
