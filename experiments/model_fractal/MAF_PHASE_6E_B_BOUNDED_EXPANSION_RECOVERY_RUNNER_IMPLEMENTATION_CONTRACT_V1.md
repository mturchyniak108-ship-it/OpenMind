# OpenMind Phase 6E-B Bounded Expansion Recovery Runner Implementation Contract V1

## Status

**PROSPECTIVE IMPLEMENTATION CONTRACT — RUNNER NOT YET CREATED OR EXECUTED**

This document defines the dedicated Phase 6E-B runner implementation boundary authorized by the frozen Phase 6E-B preregistration.

Freezing this contract authorizes only creation and static qualification of the dedicated runner source under this exact contract. It does not authorize Phase 6E-B scientific execution.

## Scientific contract inherited unchanged

The runner MUST implement the frozen Phase 6E-B preregistration without changing its scientific question, population, selector, catalog, generation, round schedule, challenge definition, payload-recovery rule, denominator, thresholds, or claim boundary.

The frozen scientific question remains:

For the frozen Phase 6E query population, can deterministic non-oracle bounded expansion recover every required generation-bound MAF object payload when the initial working set is deliberately constrained to a one-object selector budget?

The scientific boundary remains object-state payload identity only.

## Frozen preregistration authority

Path:

`experiments/model_fractal/MAF_PHASE_6E_B_BOUNDED_EXPANSION_RECOVERY_PREREGISTRATION_V1.md`

SHA256:

`85b44a1e78193f020c54b12f9b0698b8c20cc3a69365647b9520132d4b01dacd`

Freeze commit:

`2df93f6b461e546391df2ee519b8559146b936b8`

The runner MUST bind this exact preregistration identity.

## Frozen upstream authorities

Phase 6E-A final verdict:

`experiments/model_fractal/MAF_PHASE_6E_A_SELECTIVE_WORKING_SET_SUFFICIENCY_V1_VERDICT.md`

SHA256:

`a6c9ce2f2207beb252b2c02b47e27878b27e72736dad4275ab9905d40812e334`

Phase 6E-A result:

`experiments/model_fractal/maf_phase_6e_a_selective_working_set_sufficiency_v1.json`

SHA256:

`f86433603e68fc9f1e5c65f7d3ecbd8d9ce9313d252c605dd6e2cada18a91c86`

Phase 6E-A hidden reference fixture:

`experiments/model_fractal/maf_phase_6e_a_reference_state_fixture_v1.json`

SHA256:

`870b656e0c3181ec8f7be1537bdeafde10fffd1b947f5372d21cdee4c00a83a0`

Phase 6E entry checkpoint:

`experiments/model_fractal/MAF_PHASE_6E_ENTRY_CHECKPOINT.md`

SHA256:

`1807437ea97e46a6cc687adbbe8c384dabae45a562f1d2aef6bd37e43b4bbe35`

Query-scoped working-set architecture:

`experiments/model_fractal/MAF_QUERY_SCOPED_WORKING_SET_ARCHITECTURE.md`

SHA256:

`7df826096e506d13502e442fb11f7e1f18fb2c5a342f4214b91a3c3df043559c`

Query Capsule protocol:

`experiments/model_fractal/MAF_QUERY_CAPSULE_DATA_MODEL_V1_PROTOCOL.md`

SHA256:

`5255a58c8c6340c251e24ae8543760fcd66a8deb8be1a8356ad5b78ad898edda`

Query Capsule implementation:

`experiments/model_fractal/maf_query_capsule_data_model_v1.py`

SHA256:

`f897b97011714f3c84b7350c6bb53e800232be8a5d34e5148a3e50a81952976e`

Accepted Q2 selector protocol:

`experiments/model_fractal/MAF_QUERY_TO_PK_SELECTION_V1_PROTOCOL.md`

SHA256:

`b42a0643976c2393871e3b826ba5573b4de981b49603de63230d69cf57be0811`

Accepted Q2 selector implementation:

`experiments/model_fractal/maf_query_to_pk_selection_v1.py`

SHA256:

`e21c05e352fe921b791e8c936425727a98911ce7566989672a96bfd2b9613fa2`

Frozen query fixture:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_queries.json`

SHA256:

`32f4636bd5e8ceee0dca8342335279a6f8e6acafe866a5469f2c23aa2655202a`

Frozen catalog:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_catalog.json`

SHA256:

`c51ef0fabeb10e7c8a091a093aa1934620a69b2026b5a87cb02477b9dd7ca900`

Frozen generation-construction authority:

`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_generation_construction_authority.json`

SHA256:

`a5e953ae2ab2dd11a9f6dc564ae5ee57cb064d6eea0a8a5517191b4a6efc1a6d`

Frozen MAF object implementation:

`experiments/model_fractal/maf_object_v1.py`

SHA256:

`eed6cbd96995412a632883f3c534f9023e7711ea8eb437afe35a48312502f63b`

## Frozen model and generation binding

Source model PK:

`mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258`

Source generation PK:

`mafgen:v1:45a80a2aa271ce04853003185b6a1227cb309bd1e3e2dc538eea849fac9f5db0`

Source generation manifest SHA256:

`28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3`

Source GGUF SHA256:

`507de59046601282ba768a9789900e6ccf60ed93ddf346730b7c68eb0715bc47`

The GGUF is provenance only and MUST NOT be the scientific payload source.

## Dedicated runner namespace

Runner path:

`experiments/model_fractal/maf_phase_6e_b_bounded_expansion_recovery_v1.py`

Result path:

`experiments/model_fractal/maf_phase_6e_b_bounded_expansion_recovery_v1.json`

No predecessor runner may be imported, called, or executed.

The spent Q2 V1.4 validation runner MUST NOT be imported, called, or executed.

The Phase 6E-A runner MUST NOT be imported, called, or executed.

## Deterministic schemas

Expansion trace snapshot schema:

`openmind.maf_phase_6e_b_expansion_trace_snapshot.v1`

Final result schema:

`openmind.maf_phase_6e_b_bounded_expansion_recovery.v1`

Canonical JSON bytes for both structures MUST be:

`json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8") + b"\n"`

The SHA256 stored for the expansion trace snapshot MUST be the SHA256 of these canonical snapshot bytes including the final newline.

## Frozen round schedule

Exactly four selector states are authorized for every one of the 40 queries.

Round 0:

- candidate budget `1`
- selection configuration SHA256 `2dd2925a3d9f63197deff6dc98f951c5177dc63dc08818b6492228dbac7d5576`

Round 1:

- candidate budget `2`
- selection configuration SHA256 `57f751a3a019bccd58c5c32b4f5ecaf78283f49cc146896d61492ce31dfdd1c6`

Round 2:

- candidate budget `3`
- selection configuration SHA256 `67dd6e5589cb16374e949b3ed633c3364f0ccb1d8c2b0a9ca1c6eaa2d2ceed56`

Round 3:

- candidate budget `4`
- selection configuration SHA256 `0caeaeaafdd870e6b02ccc8b4450576883d4ef5234ba689c472e3b14d9dbe120`

No fifth selector state, larger candidate budget, retry, rescue, manual PK insertion, relationship expansion, or route-cache expansion is permitted.

## Selector configuration construction

For each round the runner MUST call the frozen:

`default_selection_config_v1(max_candidates=<round budget>)`

The resulting configuration SHA256 MUST equal the frozen round-specific SHA256 before any selector call using that configuration is accepted.

The runner MUST NOT construct a semantically different configuration with the same candidate budget.

## Population

The runner MUST load exactly the frozen 40-query fixture:

- 24 `specific_intent`
- 8 `multi_target_intent`
- 8 `fallback_control`

All 40 queries MUST participate in every selector round.

The required query ID order is the frozen fixture order and MUST remain unchanged through:

- selector execution;
- capsule construction;
- trace snapshot;
- final result.

Only non-fallback queries may enter the scientific recovery denominator.

## Selector execution rule

For every query at every round, the runner MUST invoke only:

`select_query_to_pks_v1`

with:

- exact frozen query text;
- exact frozen catalog;
- exact round-specific frozen selector configuration;
- exact frozen source generation PK;
- exact frozen source manifest SHA256.

The runner MUST preserve the selector returned `selected_object_pks` order.

It MUST reject:

- duplicate selected PKs;
- a selected count above the round candidate budget;
- a selected PK absent from the frozen catalog;
- a selector result with a mismatched configuration SHA256;
- a selector result with a mismatched source generation;
- a selector result with a mismatched source manifest.

The query signature MUST be identical across all four rounds for the same query.

A violation is an integrity failure, not a scientific recovery failure.

## Monotonic expansion invariant

For rounds 1 through 3:

`set(previous_selected_object_pks) <= set(current_selected_object_pks)`

MUST hold.

`additional_pks` MUST be the current selected PKs absent from the previous selected set, preserving their order in the current selector result.

The cumulative route order begins as the round-zero selector order.

At each later round, only `additional_pks` are appended to the cumulative route order.

The cumulative route order MUST:

- contain no duplicates;
- contain exactly the current selected PK set;
- preserve the admission order created by the four frozen selector states.

A non-monotonic selector result is an infrastructure/integrity failure and MUST stop the operation without publishing a scientific result.

## Query Capsule construction

After all 40 round-zero selector calls and before any round-one call, the runner MUST construct exactly 40 generation-bound `MAFQueryCapsuleV1` objects.

Each capsule MUST use:

- query signature from the round-zero selector result;
- query PK derived by the frozen capsule implementation;
- source generation PK equal to the frozen Phase 6E generation;
- source manifest SHA256 equal to the frozen manifest;
- `initial_object_pks` equal to the round-zero selected PK sequence;
- `selected_relationship_pks = ()`;
- `route_order` equal to the round-zero selected PK sequence;
- `expansion_policy = "bounded_v1"`;
- `max_object_budget = 4`;
- `max_expansion_rounds = 3`;
- `selection_config_sha256` equal to the round-zero configuration SHA256.

The runner MUST use the frozen capsule implementation for deterministic query-PK validation and canonical serialization.

The canonical capsule SHA256 stored in the trace MUST be the SHA256 of the capsule canonical JSON bytes produced by the frozen capsule implementation.

No Query Route Cache object may be read, created, updated, or persisted.

## Mandatory anti-leakage ordering

The runner may hash the hidden Phase 6E-A reference fixture before trace construction to verify file identity.

It MUST NOT parse, deserialize, iterate, inspect, or otherwise expose any reference fixture query target or required object record to program state before the complete trace snapshot is frozen.

The mandatory high-level execution order is:

1. repository preflight;
2. static frozen-authority identity verification;
3. hash the hidden reference fixture without parsing it;
4. load the frozen query fixture and catalog;
5. load the frozen selector and capsule implementations;
6. load generation-construction authority needed for source binding, but not hidden reference targets;
7. execute all 40 round-zero selector calls;
8. construct all 40 round-zero Query Capsules;
9. execute all 40 round-one selector calls;
10. execute all 40 round-two selector calls;
11. execute all 40 round-three selector calls;
12. build and freeze one canonical complete expansion trace snapshot;
13. compute and retain its canonical SHA256;
14. only then parse the hidden Phase 6E-A reference fixture;
15. load generation placement state required for payload evaluation;
16. classify initial sufficiency;
17. inspect generation-bound MAF object payloads;
18. determine earliest recovery rounds;
19. aggregate the scientific verdict;
20. build one deterministic result;
21. publish the result once with exclusive creation;
22. independently reread and qualify the written result and repository state.

No code path may load the reference fixture before step 14.

## Expansion trace snapshot contract

The trace snapshot MUST contain exactly these top-level semantic fields:

- `schema`;
- `source_generation_pk`;
- `source_manifest_sha256`;
- `query_fixture_sha256`;
- `catalog_sha256`;
- `selector_sha256`;
- `capsule_implementation_sha256`;
- `expansion_policy`;
- `max_object_budget`;
- `max_expansion_rounds`;
- `round_config_sha256`;
- `queries`.

`round_config_sha256` MUST deterministically encode rounds `0`, `1`, `2`, and `3` with their exact frozen configuration identities.

The snapshot MUST contain exactly 40 query trace records.

Each query trace record MUST contain:

- `query_id`;
- `query_signature`;
- `query_pk`;
- `round_zero_capsule_sha256`;
- `rounds`.

Each `rounds` sequence MUST contain exactly four records in order 0, 1, 2, 3.

Each round record MUST contain:

- `round_index`;
- `candidate_budget`;
- `selection_config_sha256`;
- `selected_object_pks`;
- `selected_count`;
- `additional_pks`;
- `cumulative_route_order`.

The trace snapshot MUST NOT contain:

- query class;
- required object PKs;
- covered required PKs;
- missing required PKs;
- expected payload SHA256;
- reference payload SHA256;
- payload-match state;
- Phase 6E-A selected PKs;
- any verdict or recovery classification.

The snapshot is expansion-causal evidence only.

## Snapshot immutability

Once canonical snapshot bytes and their SHA256 are computed:

- the in-memory snapshot MUST NOT be changed;
- no selected PK sequence may be changed;
- no additional PK sequence may be changed;
- no cumulative route order may be changed;
- no capsule SHA may be changed;
- no round may be added, removed, or rerun.

Post-snapshot evaluation MUST consume the frozen trace, never repair it.

## Hidden reference loading

Only after snapshot freeze may the runner parse the exact hidden reference fixture.

The runner MUST verify:

- exact fixture schema;
- exact frozen source model PK;
- exact frozen source generation PK;
- exact frozen source manifest SHA256;
- exact frozen source GGUF SHA256;
- exact frozen query fixture SHA256;
- exact frozen catalog SHA256;
- exactly 40 reference query records;
- exactly 12 reference object records;
- exact query ID order and class counts;
- no duplicate reference query IDs;
- no duplicate reference object PKs.

Reference integrity failure is infrastructure failure.

## Controlled challenge classification

For each non-fallback query:

`initial_selected = round 0 selected_object_pks`

`required = frozen reference required_object_pks`

`initial_missing = required - initial_selected`

If `initial_missing` is empty, classification is:

`INITIAL_SUFFICIENT`

That query MUST be excluded from both the recovery numerator and denominator.

If `initial_missing` is non-empty, classification is:

`INITIAL_INSUFFICIENT`

That query MUST enter the recovery denominator.

Fallback controls MUST have an empty required set and classification:

`CONTROL`

Fallback controls MUST never enter the recovery numerator or denominator.

The challenge classification is computed after trace freeze only.

## Generation-bound object resolution

Payload evaluation MUST use the frozen generation-construction authority and frozen runtime generation manifest.

For any required PK present in an evaluated round:

1. resolve the exact target and placement for that PK;
2. require exact frozen source-generation binding;
3. require the serialized object file to exist;
4. compute the serialized object file SHA256;
5. require it to equal the generation descriptor `object_file_sha256`;
6. require the serialized object byte length to equal the descriptor placement length;
7. call only the frozen `maf_object_v1.inspect_object` implementation;
8. require the inspected object PK/tensor metadata to match the frozen reference object record where represented by the object format;
9. obtain the actual observed payload SHA256 from payload bytes;
10. require it to equal the generation descriptor payload SHA256;
11. require it to equal the hidden reference fixture payload SHA256.

Metadata equality alone MUST NOT count as payload recovery.

The source GGUF MUST NOT be opened as the scientific payload source.

## Payload observation cache

The runner MAY cache independently observed generation-bound object evidence by object PK after the reference has been loaded.

The cache MUST contain only evidence obtained from the frozen generation-bound MAF object files.

The cache MUST NOT alter selection, expansion, classification, or stopping.

It exists only to avoid repeatedly hashing the same immutable object payload during post-snapshot evaluation.

## Per-round post-snapshot evaluation

For each query and each round, post-snapshot evaluation MUST compute:

- selected object PKs from the frozen trace;
- covered required PKs;
- missing required PKs;
- payload mismatch PKs;
- payload evidence for every covered required PK.

For a covered required PK, payload evidence MUST include:

- `object_pk`;
- `serialized_object_sha256`;
- `generation_payload_sha256`;
- `reference_payload_sha256`;
- `observed_payload_sha256`;
- `payload_match`.

`payload_match` is true only when the observed payload identity matches both generation and reference authorities.

## Earliest recovery round

For each `INITIAL_INSUFFICIENT` query, evaluate frozen rounds 1, 2, and 3 in order.

The earliest recovery round is the first round where:

- missing required PKs are empty;
- payload mismatch PKs are empty;
- payload evidence exists for every required PK;
- every payload evidence record has `payload_match = true`.

If none qualifies:

`earliest_recovery_round = null`

Earliest recovery is descriptive post-snapshot evidence only.

The runner MUST still have executed all four selector states before this value is computed.

## Per-query result contract

Every final query record MUST contain at least:

- `query_id`;
- `query_class`;
- `query_text_sha256`;
- `query_signature`;
- `query_pk`;
- `source_generation_pk`;
- `round_zero_capsule_sha256`;
- `rounds`;
- `round_zero_selected_object_pks`;
- `round_zero_missing_required_pks`;
- `required_object_pks`;
- `initial_classification`;
- `earliest_recovery_round`;
- `final_selected_object_pks`;
- `final_covered_required_pks`;
- `final_missing_required_pks`;
- `payload_mismatch_pks`;
- `payload_evidence`;
- `additional_pks_by_round`;
- `final_cumulative_route_order`;
- `verdict`.

For independent qualification, the runner SHOULD also include:

`round_evaluations`

with one post-snapshot evaluation record for each round 0 through 3.

`round_evaluations` is not part of the trace snapshot and therefore may contain hidden-reference comparison fields.

## Per-query verdict rule

Fallback query:

`verdict = "CONTROL"`

Initially sufficient non-fallback query:

`verdict = "INITIAL_SUFFICIENT"`

Initially insufficient query with a qualifying earliest recovery round:

`verdict = "RECOVERED"`

Initially insufficient query with no qualifying round 1 through 3:

`verdict = "NOT_RECOVERED"`

No other scientific query verdict is permitted.

## Aggregate counters

The result MUST deterministically compute:

- `challenge_count`;
- `initial_sufficient_count`;
- `recovered_count`;
- `not_recovered_count`;
- `fallback_control_count`.

The following invariant MUST hold:

`challenge_count + initial_sufficient_count == 32`

and:

`fallback_control_count == 8`

and:

`recovered_count + not_recovered_count == challenge_count`

## Phase verdict rule

If:

`challenge_count == 0`

then:

`phase_verdict = "NOT_TESTABLE"`

If:

`challenge_count > 0`

and:

`not_recovered_count > 0`

then:

`phase_verdict = "FAIL"`

If and only if:

- `challenge_count > 0`;
- `recovered_count == challenge_count`;
- `not_recovered_count == 0`;
- `fallback_control_count == 8`;
- all integrity invariants hold;

then:

`phase_verdict = "PASS"`

A scientifically valid `FAIL` or `NOT_TESTABLE` is not an infrastructure error.

A valid scientific result MUST be preserved unchanged regardless of PASS, FAIL, or NOT_TESTABLE.

## Run-level result contract

The final result MUST contain at least:

- `schema`;
- `preregistration_sha256`;
- `phase_6e_a_verdict_sha256`;
- `phase_6e_a_result_sha256`;
- `reference_fixture_sha256`;
- `phase_6e_entry_checkpoint_sha256`;
- `query_scoped_architecture_sha256`;
- `capsule_protocol_sha256`;
- `capsule_implementation_sha256`;
- `selector_protocol_sha256`;
- `selector_implementation_sha256`;
- `query_fixture_sha256`;
- `catalog_sha256`;
- `generation_authority_sha256`;
- `maf_object_implementation_sha256`;
- `source_model_pk`;
- `source_generation_pk`;
- `source_manifest_sha256`;
- `source_gguf_sha256`;
- `expansion_policy`;
- `max_object_budget`;
- `max_expansion_rounds`;
- `round_config_sha256`;
- `expansion_trace_snapshot`;
- `expansion_trace_snapshot_sha256`;
- `class_counts`;
- `challenge_count`;
- `initial_sufficient_count`;
- `recovered_count`;
- `not_recovered_count`;
- `fallback_control_count`;
- `queries`;
- `phase_verdict`;
- `scientific_boundary`.

The final result MAY embed the complete frozen trace snapshot because doing so strengthens independent auditability.

## Scientific-boundary flags

The final result MUST contain a `scientific_boundary` mapping in which all of the following are false:

- `route_cache_assisted_expansion`;
- `relationship_expansion`;
- `adaptive_rescue`;
- `inference`;
- `avoidance_claim`;
- `fidelity_claim`;
- `performance_claim`;
- `maf_native_compute`.

The result MUST NOT contain a positive claim for any later phase.

## Dedicated runner function surface

The runner MUST provide clear dedicated functions whose responsibilities are statically auditable.

At minimum the implementation MUST expose functions equivalent to:

- `need`;
- `git`;
- `sha256_bytes`;
- `sha256_file`;
- `canonical_bytes`;
- `load_frozen_module`;
- `verify_repository_preflight`;
- `verify_static_authorities`;
- `load_selector_inputs`;
- `execute_round_zero_and_capsules`;
- `execute_selector_round`;
- `execute_all_expansion_rounds`;
- `freeze_expansion_trace_snapshot`;
- `load_reference_fixture_after_snapshot`;
- `load_generation_binding_after_snapshot`;
- `inspect_generation_bound_object`;
- `evaluate_after_snapshot`;
- `build_result`;
- `write_result`;
- `verify_post_write`;
- `main`.

Names may differ only if static qualification can unambiguously prove equivalent separation and ordering.

## Main-function ordering gate

Static qualification MUST prove that `main` orders the scientific boundary so that:

`execute_round_zero_and_capsules`

precedes all later selector rounds;

all round execution precedes:

`freeze_expansion_trace_snapshot`;

snapshot freeze precedes:

`load_reference_fixture_after_snapshot`;

reference loading precedes:

`evaluate_after_snapshot`;

evaluation precedes:

`build_result`;

result construction precedes:

`write_result`;

and write precedes:

`verify_post_write`.

No reference-loading call may be reachable from a pre-snapshot selection or trace-construction function.

## Static anti-oracle qualification

Before runner freeze, AST and source qualification MUST establish that:

- no reference fixture JSON parse occurs in selector-input loading;
- no reference fixture JSON parse occurs in round execution;
- no reference fixture JSON parse occurs in capsule construction;
- no Phase 6E-A result query record is used as a selector input;
- no Phase 6E-A selected PK list is used as a selector input;
- no expected-target implementation is imported;
- no Query Route Cache implementation is imported;
- no spent Q2 V1.4 runner is imported;
- no Phase 6E-A runner is imported.

The reference path and SHA may appear in preflight only for byte identity hashing.

## Static prohibited execution surfaces

The runner MUST NOT contain or use:

- network libraries or network calls;
- HTTP clients;
- sockets;
- subprocess commands other than read-only Git inspection required for repository invariants;
- shell mutation;
- `git add`;
- `git commit`;
- `git push`;
- remote Git operations;
- inference APIs;
- llama.cpp invocation;
- GGUF payload reads;
- Query Route Cache access;
- relationship expansion;
- random expansion;
- time-dependent selection;
- environment-dependent candidate ordering;
- `eval`;
- `exec`.

## Repository preflight

Immediately before scientific execution, the frozen runner MUST require:

- branch `labs/multidimensional-maf`;
- exact frozen runner commit HEAD supplied by the execution preflight;
- tracked worktree clean;
- Git index empty;
- canonical untracked baseline exactly equal to the separately frozen execution-preflight baseline;
- result path absent;
- all frozen authority identities exact;
- runner worktree bytes identical to committed runner bytes.

The runner itself MUST NOT stage or commit anything.

## Result publication rule

The result path MUST be created only once using exclusive creation semantics equivalent to:

`os.O_WRONLY | os.O_CREAT | os.O_EXCL`

The result MUST be canonical JSON bytes.

The runner MUST flush and fsync the result before treating publication as complete.

If writing fails after the runner itself created the new path but before a complete result is established, it may remove only that newly created result path as write rollback.

It MUST NOT remove or alter any pre-existing file.

If the result path exists before execution, the runner MUST fail closed before selector execution.

## Post-write qualification

After result publication the runner MUST independently verify:

- exact reread equality with expected canonical result bytes;
- exact result SHA256 from reread bytes;
- tracked worktree remains clean;
- Git index remains empty;
- the result appears exactly once as the new untracked path;
- all pre-existing unrelated untracked paths remain byte-for-byte name-identical in canonical NUL-delimited baseline form.

A post-write verification failure MUST NOT trigger rerunning scientific selection.

The result and repository state must be preserved for diagnosis unless the failure occurred inside the narrowly defined incomplete-write rollback rule.

## Return-code semantics

Infrastructure or integrity failure:

- nonzero return code;
- no scientific PASS, FAIL, or NOT_TESTABLE reinterpretation.

Successfully published valid scientific result:

- zero return code regardless of whether `phase_verdict` is `PASS`, `FAIL`, or `NOT_TESTABLE`.

Scientific FAIL is data, not process failure.

Scientific NOT_TESTABLE is data, not process failure.

## Independent qualification requirement

The runner result is not frozen immediately after execution.

A separate post-run qualifier MUST independently verify, without rerunning selection:

- result identity;
- canonical JSON;
- frozen trace snapshot SHA;
- all 40 immutable four-round traces;
- round budgets and config SHAs;
- monotonic selection;
- additional PK derivation;
- cumulative route order;
- capsule SHA bindings;
- reference anti-leakage structure;
- challenge classification;
- all generation-bound serialized-object identities;
- actual payload SHA identities;
- earliest recovery rounds;
- query verdicts;
- aggregate counters;
- PASS, FAIL, or NOT_TESTABLE consistency;
- scientific-boundary flags;
- repository preservation.

Only after that independent qualification may the result be frozen.

## Negative-result preservation

If one or more challenge queries are `NOT_RECOVERED`, Phase 6E-B is a scientific FAIL under the frozen contract.

The runner, qualifier, and later workflow MUST NOT:

- increase the candidate budget;
- add another expansion round;
- alter the selector;
- add relationship PKs;
- use Route Cache data;
- use hidden reference targets during expansion;
- repair individual queries;
- weaken the acceptance rule;
- discard the result.

Any redesign requires a successor preregistration.

## NOT_TESTABLE preservation

If `challenge_count == 0`, the Phase 6E-B result is `NOT_TESTABLE`.

That outcome MUST be frozen as a valid prospective result if independently qualified.

It MUST NOT be relabeled PASS.

A successor challenge design would require a new prospective preregistration.

## Claim boundary

A Phase 6E-B PASS would establish only deterministic bounded recovery of frozen required MAF object payload state under:

- the frozen 40-query population;
- the frozen catalog;
- the frozen accepted selector;
- the frozen 1-to-4 candidate-budget schedule;
- the frozen source generation;
- the frozen controlled one-object initial challenge;
- the exact payload-identity rule.

It would not establish:

- arbitrary-prompt generalization;
- recovery of every incomplete working set;
- relationship-based expansion;
- route-cache-assisted expansion;
- actual object avoidance;
- actual tensor avoidance;
- reduced bytes read;
- reduced memory;
- reduced materialization;
- inference correctness;
- logit parity;
- token parity;
- answer parity;
- answer quality;
- latency improvement;
- throughput improvement;
- energy improvement;
- MAF-native computation;
- dense-runtime replacement.

Actual avoidance remains Phase 6E-C.

Output and quality fidelity remain Phase 6E-D.

Performance remains Phase 6F.

MAF-native compute remains disabled and unvalidated.

## Prospective implementation sequence

After this contract is frozen:

1. create the dedicated Phase 6E-B runner source;
2. statically qualify exact authority bindings and syntax;
3. statically qualify the four-round selector schedule;
4. statically qualify capsule construction;
5. statically qualify monotonic expansion and cumulative route rules;
6. statically qualify the trace snapshot schema and anti-leakage ordering;
7. statically qualify post-snapshot reference loading;
8. statically qualify generation-bound payload observation;
9. statically qualify challenge and verdict logic;
10. statically qualify O_EXCL result publication and repository preservation;
11. freeze the exact runner source;
12. perform a separate execution preflight;
13. authorize one authoritative execution only after all gates pass.

## Authorization boundary

Freezing this runner implementation contract authorizes only creation and static qualification of the dedicated Phase 6E-B runner source.

It does not authorize:

- selector execution;
- capsule construction against live query inputs;
- bounded expansion execution;
- hidden reference parsing for science;
- MAF payload inspection for Phase 6E-B science;
- result creation;
- Phase 6E-C claims;
- Phase 6E-D claims;
- Phase 6F claims;
- MAF-native compute;
- network publication.

## Final contract statement

The dedicated Phase 6E-B runner must create one fully frozen non-oracle four-round expansion trace before any hidden target is parsed, then evaluate that immutable trace against generation-bound MAF payload identity and classify only genuinely round-zero-incomplete non-fallback queries as recovery challenges.

No Phase 6E-B scientific result is authorized or observed by this implementation contract.
