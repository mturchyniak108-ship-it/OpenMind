# OpenMind Phase 6E-B Bounded Expansion Recovery Preregistration V1

## Status

**PROSPECTIVE PREREGISTRATION — NOT YET FROZEN**

Freezing this document authorizes only later implementation and static qualification of a dedicated Phase 6E-B bounded-expansion recovery runner under this exact contract. It does not authorize scientific execution until that runner is separately frozen and execution is separately gated.

Phase 6E-A evidence is immutable and must not be modified, repaired, regenerated, or rerun.

## Scientific question

For the frozen Phase 6E query population, can a deterministic non-oracle bounded expansion schedule recover every required generation-bound MAF object payload when the initial working set is deliberately constrained to a one-object selector budget?

The test is at the object-state payload-identity boundary.

It does not test inference, output parity, answer quality, actual object avoidance, actual tensor avoidance, I/O reduction, memory reduction, performance, energy, or MAF-native computation.

## Rationale for a controlled incomplete-working-set challenge

Frozen Phase 6E-A produced:

- 32 evaluable non-fallback queries;
- 32 initial-working-set PASS results;
- 0 initial-working-set FAIL results;
- 8 fallback controls.

Therefore the accepted Phase 6E-A population contains no naturally observed initial insufficiency case under the accepted Q2 budget of 4.

Phase 6E-B must not fabricate a recovery claim by relabeling already sufficient Phase 6E-A states.

Instead, this preregistration prospectively creates a deterministic budget-restricted seed challenge. The challenge changes only the initial candidate budget used by a fresh Phase 6E-B selector invocation. It does not remove a PK by consulting the hidden required-object oracle, and it does not use the Phase 6E-A selected PK snapshot as an expansion source.

## Frozen Phase 6E-A predecessor

Frozen Phase 6E-A final verdict commit:

`d9de837c9cb0c54bb299384301a989902abf644b`

Frozen Phase 6E-A verdict:

`experiments/model_fractal/MAF_PHASE_6E_A_SELECTIVE_WORKING_SET_SUFFICIENCY_V1_VERDICT.md`

SHA256:

`a6c9ce2f2207beb252b2c02b47e27878b27e72736dad4275ab9905d40812e334`

Frozen Phase 6E-A result:

`experiments/model_fractal/maf_phase_6e_a_selective_working_set_sufficiency_v1.json`

SHA256:

`f86433603e68fc9f1e5c65f7d3ecbd8d9ce9313d252c605dd6e2cada18a91c86`

Frozen Phase 6E-A reference fixture:

`experiments/model_fractal/maf_phase_6e_a_reference_state_fixture_v1.json`

SHA256:

`870b656e0c3181ec8f7be1537bdeafde10fffd1b947f5372d21cdee4c00a83a0`

The Phase 6E-A reference fixture may be used only as the hidden evaluation authority after the complete Phase 6E-B expansion trace snapshot has been frozen.

## Frozen upstream authorities

Phase 6E entry checkpoint:

`experiments/model_fractal/MAF_PHASE_6E_ENTRY_CHECKPOINT.md`

SHA256:

`1807437ea97e46a6cc687adbbe8c384dabae45a562f1d2aef6bd37e43b4bbe35`

Query-scoped working-set architecture:

`experiments/model_fractal/MAF_QUERY_SCOPED_WORKING_SET_ARCHITECTURE.md`

SHA256:

`7df826096e506d13502e442fb11f7e1f18fb2c5a342f4214b91a3c3df043559c`

Query Capsule data-model protocol:

`experiments/model_fractal/MAF_QUERY_CAPSULE_DATA_MODEL_V1_PROTOCOL.md`

SHA256:

`5255a58c8c6340c251e24ae8543760fcd66a8deb8be1a8356ad5b78ad898edda`

Query Capsule data-model implementation:

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

## Frozen model and generation bindings

Source model PK:

`mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258`

Source generation PK:

`mafgen:v1:45a80a2aa271ce04853003185b6a1227cb309bd1e3e2dc538eea849fac9f5db0`

Source generation manifest SHA256:

`28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3`

Source GGUF SHA256:

`507de59046601282ba768a9789900e6ccf60ed93ddf346730b7c68eb0715bc47`

The source generation and manifest are immutable throughout Phase 6E-B.

## Frozen population

The Phase 6E-B population is exactly the same frozen 40-query fixture used by Phase 6E-A:

- 24 `specific_intent`;
- 8 `multi_target_intent`;
- 8 `fallback_control`.

All 40 queries participate in the non-oracle selector and expansion trace construction.

Only non-fallback queries may enter the recovery denominator.

Fallback controls are always reported separately as `CONTROL`.

## Frozen bounded-expansion policy label

Each Phase 6E-B Query Capsule must use:

`expansion_policy = "bounded_v1"`

The frozen capsule limits are:

`max_object_budget = 4`

`max_expansion_rounds = 3`

`selected_relationship_pks = ()`

No relationship expansion is authorized because no semantic relationship-PK authority is frozen for Phase 6E-B V1.

The round-zero `route_order` must be an exact permutation of the round-zero `initial_object_pks`, preserving the deterministic selector return order.

## Fresh non-oracle selector rule

Phase 6E-B must execute fresh selector calls from the frozen query text and frozen catalog.

It must not use:

- Phase 6E-A selected PKs as an expansion source;
- Phase 6E-A required PKs as an expansion source;
- the reference fixture during selection or expansion;
- Query Route Cache entries;
- expected targets;
- touched-object telemetry;
- inference outputs;
- answer text;
- manual PK additions.

The accepted selector implementation is unchanged.

Only the candidate budget varies according to the frozen round schedule.

## Frozen round schedule

Every query receives exactly four selector states:

### Round 0 — initial seed

`max_candidates = 1`

Selection configuration SHA256:

`2dd2925a3d9f63197deff6dc98f951c5177dc63dc08818b6492228dbac7d5576`

This is the initial Phase 6E-B working set.

### Round 1

`max_candidates = 2`

Selection configuration SHA256:

`57f751a3a019bccd58c5c32b4f5ecaf78283f49cc146896d61492ce31dfdd1c6`

### Round 2

`max_candidates = 3`

Selection configuration SHA256:

`67dd6e5589cb16374e949b3ed633c3364f0ccb1d8c2b0a9ca1c6eaa2d2ceed56`

### Round 3

`max_candidates = 4`

Selection configuration SHA256:

`0caeaeaafdd870e6b02ccc8b4450576883d4ef5234ba689c472e3b14d9dbe120`

Round 3 is the maximum authorized object-candidate budget and equals the accepted Phase 6E-A Q2 candidate budget.

No round above 3 and no candidate budget above 4 is permitted.

## Deterministic expansion rule

For every query and every round:

1. invoke the exact frozen selector implementation with the exact frozen query, catalog, source generation, source manifest, and round-specific configuration;
2. preserve the selector returned `selected_object_pks` order;
3. reject duplicate PKs;
4. require selected count to be less than or equal to the round candidate budget;
5. require every PK to belong to the frozen catalog;
6. require the previous round selected PK set to be a subset of the current round selected PK set;
7. define `additional_pks` as current selected PKs absent from the previous selected set, preserving current selector order;
8. append only those newly admitted PKs to the cumulative route order.

A non-monotonic selector result is an integrity failure. It is not a scientific recovery failure.

No PK may be inserted by any mechanism other than the frozen selector under the next authorized round budget.

## Fixed execution and stopping rule

The expansion schedule is fixed before evaluation.

All 40 queries execute rounds 0, 1, 2, and 3.

The runner must not stop early because a hidden required set appears satisfied.

The runner must not continue beyond round 3 because a hidden required set remains unsatisfied.

This fixed schedule ensures that the hidden reference state cannot influence whether another expansion round occurs.

Earliest recovery round may be computed only after the complete expansion trace snapshot has been frozen and the hidden reference fixture is loaded for evaluation.

## Query Capsule binding

For each query, after round 0 and before any reference evaluation, construct a generation-bound `MAFQueryCapsuleV1` with:

- query PK derived by the frozen capsule implementation;
- query signature from the round-zero selector result;
- frozen source generation PK;
- frozen source manifest SHA256;
- `initial_object_pks` equal to round-zero selected PKs;
- `selected_relationship_pks = ()`;
- `route_order` equal to the round-zero selector return order;
- `expansion_policy = "bounded_v1"`;
- `max_object_budget = 4`;
- `max_expansion_rounds = 3`;
- `selection_config_sha256` equal to the round-zero configuration SHA256.

The capsule must pass its frozen generation and manifest binding invariants.

The capsule binds the seed and the authorized expansion budget. It does not itself define the scientific expansion algorithm.

## Expansion trace anti-leakage rule

The runner may verify the reference-fixture file identity before selection, but it must not parse or deserialize the reference fixture before the expansion trace snapshot is frozen.

The required order is:

1. verify all frozen identities;
2. load the frozen query fixture, catalog, selector, capsule model, and generation authorities;
3. execute all 40 round-zero selector calls;
4. construct all 40 round-zero Query Capsules;
5. execute all 40 round-one selector calls;
6. execute all 40 round-two selector calls;
7. execute all 40 round-three selector calls;
8. freeze one canonical complete expansion trace snapshot for all 40 queries;
9. compute and freeze the expansion trace snapshot SHA256;
10. only then parse the frozen Phase 6E-A reference fixture;
11. classify initial insufficiency and bounded recovery;
12. inspect generation-bound MAF payloads;
13. aggregate the prospective Phase 6E-B result.

No required-object PK, expected payload SHA256, or reference query target may enter selector, capsule, expansion, round scheduling, or trace construction state.

## Canonical expansion trace snapshot

The trace snapshot must contain, at minimum:

- schema;
- source generation PK;
- source manifest SHA256;
- query fixture SHA256;
- catalog SHA256;
- selector SHA256;
- capsule implementation SHA256;
- expansion policy label;
- max object budget;
- max expansion rounds;
- all four round configuration SHA256 values;
- exactly 40 query trace records.

Each query trace record must contain:

- query ID;
- query signature;
- query PK;
- round-zero capsule canonical SHA256;
- for each round 0 through 3:
  - round index;
  - candidate budget;
  - selection configuration SHA256;
  - selected object PKs in selector order;
  - selected count;
  - additional PKs relative to the previous round;
  - cumulative route order.

The snapshot must contain no required-object PK field and no reference payload field.

## Controlled insufficiency classification

Only after the complete trace snapshot is frozen may the hidden reference fixture be parsed.

For each non-fallback query:

`initial_required_pks = frozen reference required_object_pks`

`initial_selected_pks = round 0 selected_object_pks`

`initial_missing_pks = required_object_pks - initial_selected_pks`

A non-fallback query with an empty `initial_missing_pks` set is classified:

`INITIAL_SUFFICIENT`

It is reported but excluded from the recovery numerator and denominator.

A non-fallback query with a non-empty `initial_missing_pks` set is classified:

`INITIAL_INSUFFICIENT`

It enters the Phase 6E-B recovery denominator.

This classification occurs only during post-trace evaluation and cannot alter the already frozen expansion schedule.

## Generation-bound payload recovery rule

For every initially insufficient query, evaluate each frozen round state against the independently frozen reference state.

For every required PK present in a round state:

1. resolve its exact frozen generation placement;
2. require the serialized MAF object file SHA256 to match the generation descriptor;
3. inspect the actual MAF object payload using the frozen `maf_object_v1.inspect_object` implementation;
4. require the observed payload SHA256 to match the generation descriptor payload SHA256;
5. require the observed payload SHA256 to match the independently frozen reference payload SHA256.

A required object is recovered only when the exact required PK is present and its actual observed payload identity matches both frozen authorities.

Metadata equality alone is insufficient.

## Earliest recovery round

After the trace snapshot is frozen and the reference fixture is loaded, determine the earliest round in `1, 2, 3` for each initially insufficient query at which:

- `missing_required_pks` is empty;
- `payload_mismatch_pks` is empty;
- every required PK has qualifying payload evidence.

If no authorized round satisfies all conditions, `earliest_recovery_round = null`.

The earliest recovery round is descriptive post-run evidence only. It must not alter the fixed execution schedule.

## Per-query verdicts

### Fallback query

A `fallback_control` query must have an empty frozen required set and receives:

`CONTROL`

It is excluded from every recovery numerator and denominator.

### Initially sufficient non-fallback query

A non-fallback query with no round-zero missing required PK receives:

`INITIAL_SUFFICIENT`

It is excluded from the recovery numerator and denominator.

### Initially insufficient query that recovers

An initially insufficient non-fallback query receives:

`RECOVERED`

only if an authorized round 1 through 3 has complete required-PK coverage and exact payload identity for every required object.

### Initially insufficient query that does not recover

An initially insufficient non-fallback query receives:

`NOT_RECOVERED`

if no authorized round 1 through 3 satisfies the full recovery rule.

## Phase-level prospective acceptance rule

Let:

`challenge_count = number of INITIAL_INSUFFICIENT non-fallback queries`

`recovered_count = number of RECOVERED queries`

`not_recovered_count = number of NOT_RECOVERED queries`

`initial_sufficient_count = number of INITIAL_SUFFICIENT non-fallback queries`

The Phase 6E-B scientific verdict is:

### PASS

only if all conditions hold:

- `challenge_count > 0`;
- `recovered_count == challenge_count`;
- `not_recovered_count == 0`;
- all 8 fallback controls are structurally valid `CONTROL`;
- every recovered required object passes generation-bound payload identity verification;
- no budget, monotonicity, authority, snapshot, or anti-leakage invariant fails.

### FAIL

if:

- `challenge_count > 0`; and
- at least one initially insufficient query is `NOT_RECOVERED`.

### NOT_TESTABLE

if:

- `challenge_count == 0`.

`NOT_TESTABLE` is not a positive Phase 6E-B result.

Infrastructure or integrity failures are distinct from PASS, FAIL, and NOT_TESTABLE and must fail closed without scientific reinterpretation.

## Required per-query result fields

Each final result query record must include at least:

- query ID;
- query class;
- query text SHA256;
- query signature;
- query PK;
- source generation PK;
- round-zero capsule SHA256;
- four immutable round records;
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
- verdict.

## Required run-level result fields

The deterministic result must include at least:

- result schema;
- this preregistration SHA256;
- frozen Phase 6E-A verdict SHA256;
- frozen Phase 6E-A result SHA256;
- frozen reference fixture SHA256;
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
- expansion trace snapshot SHA256;
- class counts;
- challenge count;
- initial sufficient count;
- recovered count;
- not recovered count;
- fallback control count;
- all 40 query records;
- final Phase 6E-B verdict;
- explicit scientific-boundary flags.

## Route Cache boundary

Phase 6E-B V1 does not read, reuse, mutate, or persist Query Route Cache state.

The architecture permits future successful routes to become derived reusable metadata, but route-cache reuse would add a second causal source for expansion and is excluded from this first bounded-expansion recovery experiment.

Any later route-cache-assisted expansion requires its own prospective contract.

## Relationship-expansion boundary

Phase 6E-B V1 does not use relationship or transition PKs.

`selected_relationship_pks` must be empty for every Query Capsule.

A later relationship-based expansion experiment requires an independently frozen semantic relationship authority and a successor protocol.

## No Phase 6E-A reuse as oracle

The frozen Phase 6E-A selection snapshot and selected object lists may be bound for provenance but must not be used to choose any Phase 6E-B round-zero or additional PK.

The frozen Phase 6E-A result may establish predecessor status and motivate the controlled challenge, but its per-query selected PKs and required PKs are forbidden expansion inputs.

## No adaptive rescue

The runner must not:

- increase `max_object_budget` above 4;
- increase `max_expansion_rounds` above 3;
- execute a fifth selector budget;
- add a neighboring PK manually;
- add a relationship PK;
- consult the reference fixture before the trace snapshot;
- rerank using expected targets;
- use output or inference feedback;
- repair a negative query after evaluation;
- alter the challenge after observing results.

Any redesign requires a successor preregistration.

## Execution-source boundary

The source GGUF is a frozen provenance authority, not the scientific payload execution source for this object-state experiment.

Generation-bound serialized MAF objects and their actual payload bytes remain the object-state authority.

No LLM inference is required or authorized for Phase 6E-B V1.

## Scientific nonclaims

A Phase 6E-B PASS would establish only deterministic bounded recovery of frozen required MAF object payload state under this exact budget-restricted challenge, selector, catalog, generation, and population.

It would not establish:

- that the same recovery behavior generalizes to arbitrary prompts;
- that every incomplete MAF working set is recoverable;
- that relationship expansion is correct;
- that route-cache-assisted expansion is correct;
- that unselected objects are avoided;
- that unselected tensors are avoided;
- reduced bytes read;
- reduced memory use;
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

Actual object and tensor avoidance remains Phase 6E-C.

Output, logit, token, answer parity, and quality remain Phase 6E-D.

Performance remains Phase 6F.

MAF-native compute remains disabled and unvalidated.

## Prospective implementation order after freeze

After this preregistration is frozen:

1. implement a dedicated Phase 6E-B runner;
2. statically qualify its exact authority bindings, round schedule, capsule construction, anti-leakage order, trace snapshot contract, payload-resolution path, verdict logic, and no-network boundary;
3. freeze the statically qualified runner;
4. perform a separate execution preflight;
5. authorize one authoritative execution only after all preflight gates pass;
6. preserve the result regardless of PASS, FAIL, or NOT_TESTABLE;
7. independently qualify the frozen trace, payload evidence, recovery classifications, and aggregate verdict;
8. freeze the qualified result;
9. freeze a narrow Phase 6E-B verdict document.

## Authorization boundary after preregistration freeze

Freezing this preregistration does not itself authorize science execution.

It authorizes only implementation and static qualification of a dedicated Phase 6E-B runner under this exact contract.

Still prohibited until separately gated:

- authoritative Phase 6E-B execution;
- reference-informed expansion;
- route-cache-assisted expansion;
- relationship expansion;
- Phase 6E-C avoidance claims;
- Phase 6E-D fidelity claims;
- Phase 6F performance claims;
- MAF-native compute;
- network publication.

## Final preregistered hypothesis

Under the frozen 40-query population and frozen generation, reducing the initial selector candidate budget to one will produce at least one non-fallback incomplete working-set challenge, and deterministic non-oracle expansion through the frozen selector budgets 2, 3, and 4 will recover every required generation-bound MAF object payload for every such challenge query within at most three expansion rounds.

This hypothesis is prospective.

No Phase 6E-B scientific result has been observed.
