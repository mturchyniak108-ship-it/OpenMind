# OpenMind Phase 6E-A Selective Working-Set Sufficiency Protocol V1

## Status

This protocol prospectively defines authoritative Phase 6E-A selective working-set sufficiency evaluation.

Freezing this protocol authorizes later implementation, static qualification, and separately gated execution of Phase 6E-A only. It does not itself establish sufficiency and it does not authorize bounded expansion, inference, tensor or object avoidance claims, output fidelity claims, answer-quality claims, performance claims, MAF-native compute, or replacement of conventional LLM execution.

## Scientific question

Phase 6E-A asks:

> Given the accepted non-oracle Q2 query-derived PK selector and a Query-Scoped MAF working set bound to one immutable source generation, is the initial selected working set sufficient to reproduce every object payload identity required by the independently frozen full-reference state for each supported query?

Phase 6E-A tests initial working-set sufficiency only.

## Frozen authority chain

- Phase 6E entry checkpoint:
  - `experiments/model_fractal/MAF_PHASE_6E_ENTRY_CHECKPOINT.md`
  - SHA256 `1807437ea97e46a6cc687adbbe8c384dabae45a562f1d2aef6bd37e43b4bbe35`
- Query-scoped architecture:
  - `experiments/model_fractal/MAF_QUERY_SCOPED_WORKING_SET_ARCHITECTURE.md`
  - SHA256 `7df826096e506d13502e442fb11f7e1f18fb2c5a342f4214b91a3c3df043559c`
- Phase 6E-A reference-state preregistration:
  - `experiments/model_fractal/MAF_PHASE_6E_A_REFERENCE_STATE_FIXTURE_PREREGISTRATION_V1.md`
  - SHA256 `8824025988ccda4adcaa21a989b9dc9dc2a567a0ea82666de5d58e94f77f3411`
- Reference-state construction protocol:
  - `experiments/model_fractal/MAF_PHASE_6E_A_REFERENCE_STATE_FIXTURE_CONSTRUCTION_PROTOCOL_V1.md`
  - SHA256 `4573406d6f91f870e7a370292303fdc881a046016f2643d1dd80dc19d9d17011`
- Qualified frozen reference fixture:
  - `experiments/model_fractal/maf_phase_6e_a_reference_state_fixture_v1.json`
  - SHA256 `870b656e0c3181ec8f7be1537bdeafde10fffd1b947f5372d21cdee4c00a83a0`
  - freeze commit `0a984b5bbfab1a6cf8c66f26cdfbc5a47382f647`
- Q2 selection protocol:
  - `experiments/model_fractal/MAF_QUERY_TO_PK_SELECTION_V1_PROTOCOL.md`
  - SHA256 `b42a0643976c2393871e3b826ba5573b4de981b49603de63230d69cf57be0811`
- Accepted Q2 selector:
  - `experiments/model_fractal/maf_query_to_pk_selection_v1.py`
  - SHA256 `e21c05e352fe921b791e8c936425727a98911ce7566989672a96bfd2b9613fa2`
- Q2 selection configuration SHA256:
  - `0caeaeaafdd870e6b02ccc8b4450576883d4ef5234ba689c472e3b14d9dbe120`
- Frozen query fixture:
  - `experiments/model_fractal/maf_query_to_pk_selection_validation_v1_queries.json`
  - SHA256 `32f4636bd5e8ceee0dca8342335279a6f8e6acafe866a5469f2c23aa2655202a`
- Frozen 12-object catalog:
  - `experiments/model_fractal/maf_query_to_pk_selection_validation_v1_catalog.json`
  - SHA256 `c51ef0fabeb10e7c8a091a093aa1934620a69b2026b5a87cb02477b9dd7ca900`
- Generation-construction authority:
  - `experiments/model_fractal/maf_query_to_pk_selection_validation_v1_generation_construction_authority.json`
  - SHA256 `a5e953ae2ab2dd11a9f6dc564ae5ee57cb064d6eea0a8a5517191b4a6efc1a6d`
- GGUF tensor inventory:
  - `experiments/model_fractal/gguf_tensor_inventory_v1.json`
  - SHA256 `7acf6d5dc672182aee0244b1bb85a47466f33dbdcdf10bde863e24f3659240ee`
- Accepted Q3 lifecycle verdict:
  - `experiments/model_fractal/MAF_QUERY_CAPSULE_ATTACH_DETACH_CLEANUP_VALIDATION_V1_1_VERDICT.md`
  - SHA256 `57233349f5d79f7dd00ac1a436cd3b109153d551b416ccdd32e85ef9e3ff0d0a`
- Accepted Q4 route-cache verdict:
  - `experiments/model_fractal/MAF_QUERY_ROUTE_CACHE_VALIDATION_V1_3_VERDICT.md`
  - SHA256 `cfff3cee4062cfe6df440c3c69aa7abb65e612b0e521a626fc163821339992c6`

Q2 V1.4 is spent validation evidence. The spent runner `experiments/model_fractal/maf_query_to_pk_selection_validation_v1_4.py` MUST NOT be imported, called, or executed by Phase 6E-A.

## Immutable source identity

- source model PK: `mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258`
- source generation PK: `mafgen:v1:45a80a2aa271ce04853003185b6a1227cb309bd1e3e2dc538eea849fac9f5db0`
- source manifest SHA256: `28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3`
- source GGUF SHA256: `507de59046601282ba768a9789900e6ccf60ed93ddf346730b7c68eb0715bc47`

Every authoritative Phase 6E-A query evaluation MUST remain bound to this immutable generation.

## Frozen population

The authoritative population is exactly the 40 frozen queries `q001` through `q040` in frozen order:

- 24 `specific_intent` queries;
- 8 `multi_target_intent` queries;
- 8 `fallback_control` queries.

The 32 specific and multi-target records are the evaluable sufficiency population.

The 8 fallback controls MUST be executed and reported separately. Their empty `required_object_pks` set MUST NOT count as automatic success and MUST NOT enter the Phase 6E-A sufficiency numerator or denominator.

## Reference-state contract

For each query, the frozen reference fixture is the sole authoritative source of:

- `query_id`;
- `query_class`;
- `query_text_sha256`;
- `required_object_pks`;
- required object PK identity;
- required object tensor metadata;
- required object payload SHA256.

For every non-fallback query, the full reference state is exactly the complete set of object payload identities named by `required_object_pks`.

The reference state MUST NOT be repaired, expanded, reduced, or reinterpreted after Phase 6E-A selection or results are observed.

## Selection isolation and anti-leakage rule

Authoritative initial PK selection MUST derive only from the accepted frozen Q2 selector under the frozen Q2 configuration.

The selector may consume only inputs authorized by the frozen Q2 contract, including the frozen query text and frozen selector catalog/configuration inputs.

The selector MUST NOT consume:

- the Phase 6E-A reference fixture;
- `required_object_pks`;
- expected-target records;
- expected answers;
- reference logits;
- reference hidden states;
- full-reference PK use discovered during evaluation;
- Phase 6E-A labels or verdicts;
- any post-hoc information chosen because it would make the query pass.

All 40 authoritative Q2 selections MUST be completed before the reference fixture is loaded for Phase 6E-A evaluation.

Immediately after selection, the runner MUST freeze a canonical selection snapshot containing every query ID and its initial `selected_object_pks`, and MUST compute and report the selection-snapshot SHA256.

After that snapshot is frozen, no `selected_object_pks` record may be modified, retried, augmented, reordered semantically, or replaced during Phase 6E-A.

## Route-cache rule

Authoritative Phase 6E-A MUST use fresh Q2 query-derived selection. Query Route Cache reuse MUST NOT replace or augment the initial Q2-selected set.

Q4 remains prerequisite architectural evidence, but cached candidate-route reuse is outside this Phase 6E-A sufficiency decision.

## Query-Scoped working-set rule

For each query, the initial Query-Scoped MAF working set is exactly the frozen Q2 `selected_object_pks` set for that query, bound to the immutable source generation.

Any Query-Scoped MAF Capsule representation used by the implementation MUST preserve the exact initial selected PK set and source-generation binding.

Expansion policy MUST be disabled for authoritative Phase 6E-A.

Maximum expansion rounds MUST be zero.

No object PK may be added after the initial selection snapshot.

## No-expansion rule

Phase 6E-A evaluates only the initial working set.

If the initial set is insufficient, the query records a negative Phase 6E-A result.

No retry, neighboring-PK expansion, relationship expansion, fallback expansion, heuristic rescue, manual repair, or post-hoc target addition is permitted.

Deterministic bounded expansion belongs to Phase 6E-B.

## Object-state reproduction rule

For each non-fallback query:

1. read its frozen `required_object_pks` only after the selection snapshot is frozen;
2. compute `covered_required_pks` as required PKs present in the initial selected set;
3. compute `missing_required_pks` as required PKs absent from the initial selected set;
4. for every covered required PK, resolve or materialize the canonical MAF object bound to the frozen source generation;
5. compute or independently verify the SHA256 of the actual resolved object payload bytes;
6. compare that observed payload SHA256 with the frozen reference fixture `payload_sha256` for the same object PK;
7. record any payload identity failure in `payload_mismatch_pks`.

Metadata equality alone is not sufficient evidence of payload reproduction.

A required object counts as reproduced only when:

- its exact PK is present in the initial selected set;
- the resolved object is bound to the frozen source generation;
- the observed payload SHA256 exactly equals the frozen reference payload SHA256.

Extra selected PKs are permitted and MUST be reported as `extra_selected_pks`. Extra selection does not cause sufficiency failure, but it does not establish efficiency or avoidance.

## Per-query decision rule

For every `specific_intent` or `multi_target_intent` query:

`PASS` requires all of the following:

- `missing_required_pks` is empty;
- `payload_mismatch_pks` is empty;
- every frozen required PK has one reproduced payload identity;
- no expansion occurred;
- the initial selection snapshot remained unchanged.

Otherwise the query verdict is `FAIL`.

A `fallback_control` query receives the separate verdict `CONTROL`. It is not classified as Phase 6E-A success or failure.

## Phase-level decision rule

There are exactly 32 evaluable non-fallback queries.

The authoritative Phase 6E-A verdict is `PASS` only if all 32 evaluable queries receive per-query `PASS`.

If one or more of the 32 evaluable queries fail, the authoritative Phase 6E-A verdict is `FAIL` and the negative result MUST be preserved.

The 8 fallback controls MUST all be present with `CONTROL` status for the run to be structurally valid, but they do not contribute to the 32-query sufficiency denominator.

No acceptance threshold below 32 of 32 is authorized by this V1 protocol.

## Result record requirements

Each query result MUST contain at least:

- `query_id`;
- `query_class`;
- `query_text_sha256`;
- `source_generation_pk`;
- `selection_config_sha256`;
- `selected_object_pks`;
- `selected_count`;
- `required_object_pks`;
- `required_count`;
- `covered_required_pks`;
- `missing_required_pks`;
- `payload_mismatch_pks`;
- `extra_selected_pks`;
- `expansion_rounds` fixed to `0`;
- per-query `verdict`.

For every reproduced required object, the evidence MUST also preserve:

- `object_pk`;
- frozen reference `payload_sha256`;
- observed payload SHA256;
- exact payload-match boolean.

All PK arrays MUST use deterministic lexicographic ordering in the result artifact.

## Run-level evidence

The authoritative result MUST report:

- frozen protocol SHA256;
- frozen reference fixture SHA256;
- source model PK;
- source generation PK;
- source manifest SHA256;
- source GGUF SHA256;
- Q2 selector SHA256;
- Q2 selection configuration SHA256;
- canonical selection-snapshot SHA256;
- exact query counts by class;
- exactly 32 evaluable queries;
- exactly 8 fallback controls;
- per-query results in q001 through q040 order;
- evaluable PASS count;
- evaluable FAIL count;
- fallback CONTROL count;
- final Phase 6E-A verdict.

## Execution ordering

The authoritative runner MUST use this ordering:

1. verify frozen repository and authority identities;
2. verify the qualified reference fixture exists and has its frozen identity, but do not load its query targets into selection state;
3. load the frozen Q2 selector and authorized Q2 selection inputs;
4. execute fresh Q2 selection for all 40 frozen queries;
5. freeze and hash the complete 40-query selection snapshot;
6. only after Step 5, load the frozen Phase 6E-A reference fixture for evaluation;
7. construct the generation-bound initial working-set representation for each query;
8. reproduce and hash required payloads available from the initial selected set;
9. compare against the frozen reference payload identities;
10. classify the 32 evaluable queries and 8 fallback controls;
11. compute the Phase 6E-A aggregate verdict;
12. write one deterministic result artifact;
13. perform independent post-run qualification before any verdict document is frozen.

Selection and evaluation MUST remain logically separated even if implemented in one process.

## Failure policy

Any failure of frozen identity, selector execution, selection snapshot creation, generation binding, object resolution, payload hashing, deterministic serialization, or repository invariant causes the authoritative run to fail closed.

A missing required object is a scientific insufficiency result when caused by the frozen initial selected set. It MUST NOT trigger expansion or repair.

An infrastructure or integrity failure that prevents valid evaluation MUST be distinguished from scientific insufficiency and MUST NOT be silently counted as a query PASS or FAIL.

After authoritative results are observed, the selector, configuration, fixture, working-set rule, payload comparison rule, query population, or acceptance rule MUST NOT be modified to rescue the result.

## Scientific boundary

Phase 6E-A may establish only whether the initial non-oracle selected object set is sufficient to reproduce the independently frozen required object payload state under this contract.

Phase 6E-A does not establish:

- actual tensor or object avoidance;
- reduced bytes read;
- reduced materialization;
- reduced memory use;
- output parity;
- logit parity;
- top-k parity;
- token agreement;
- answer quality;
- end-to-end inference correctness;
- throughput;
- latency;
- energy efficiency;
- MAF-native compute correctness;
- replacement of llama.cpp or another LLM runtime.

Actual access avoidance belongs to Phase 6E-C.

Output parity and quality belong to Phase 6E-D.

Performance belongs to Phase 6F.

Direct MAF-native computation remains disabled and unvalidated.

## Conventional dense backend

The conventional dense compute backend remains authorized by the Phase 6E checkpoint.

This Phase 6E-A V1 comparison does not require language-model inference. Its frozen comparison boundary is object-state sufficiency and payload identity.

Any later use of dense execution for a narrower authorized comparison MUST remain downstream of the frozen selection snapshot and MUST NOT become a selection oracle.

## Prospective implementation rule

After this protocol is frozen, a dedicated Phase 6E-A runner may be implemented.

The runner MUST be statically qualified before execution and MUST be frozen in a dedicated commit before authoritative Phase 6E-A science runs.

Static qualification MUST prove at minimum:

- exact frozen authority identities;
- accepted Q2 selector identity;
- no import or execution of the spent Q2 V1.4 runner;
- reference fixture cannot influence selection;
- all 40 selections complete before reference evaluation;
- selection snapshot immutability;
- no route-cache substitution;
- no expansion path;
- exact generation binding;
- actual payload SHA256 comparison;
- deterministic result serialization;
- no inference;
- no MAF-native compute;
- no network;
- no Git staging or commit during science execution.

## Prospective validation gates

`SA01` — protocol identity is frozen.
`SA02` — reference fixture identity is exact.
`SA03` — query fixture identity is exact.
`SA04` — catalog identity is exact.
`SA05` — generation authority identity is exact.
`SA06` — GGUF inventory identity is exact.
`SA07` — accepted Q2 selector identity is exact.
`SA08` — Q2 selection configuration identity is exact.
`SA09` — source model PK is exact.
`SA10` — source generation PK is exact.
`SA11` — source manifest SHA256 is exact.
`SA12` — source GGUF SHA256 is exact.
`SA13` — exactly 40 frozen queries are selected in q001 through q040 order.
`SA14` — class counts are exactly 24 specific, 8 multi-target, 8 fallback.
`SA15` — all 40 selections complete before reference-target evaluation.
`SA16` — canonical selection snapshot is frozen and hashed before reference evaluation.
`SA17` — authoritative selection derives from accepted Q2 only.
`SA18` — Query Route Cache does not substitute or augment selection.
`SA19` — expansion rounds equal zero for every query.
`SA20` — no selected PK changes after snapshot freeze.
`SA21` — required PKs derive only from the frozen Phase 6E-A fixture.
`SA22` — all non-fallback required PK arrays are compared exactly.
`SA23` — covered required objects are generation-bound.
`SA24` — observed required-object payload SHA256 values derive from actual resolved payload bytes.
`SA25` — observed payload SHA256 values are compared exactly with frozen reference values.
`SA26` — missing required PKs are recorded without rescue.
`SA27` — payload mismatches are recorded without rescue.
`SA28` — extra selected PKs are reported without being treated as avoidance evidence.
`SA29` — specific and multi-target PASS requires complete required-state reproduction.
`SA30` — fallback controls are reported as CONTROL and excluded from the sufficiency denominator.
`SA31` — exactly 32 evaluable queries determine the Phase 6E-A verdict.
`SA32` — phase PASS requires exactly 32 of 32 evaluable queries PASS.
`SA33` — no inference is executed.
`SA34` — no Phase 6E-C avoidance claim is made.
`SA35` — no Phase 6E-D fidelity or quality claim is made.
`SA36` — no Phase 6F performance claim is made.
`SA37` — no MAF-native compute is executed.
`SA38` — no network access occurs.
`SA39` — science execution performs no Git staging or commit.
`SA40` — deterministic result artifact passes independent post-run qualification.

## Authorization after freeze

Freezing this protocol authorizes only the next controlled steps:

1. implement a dedicated Phase 6E-A runner under this contract;
2. statically qualify that runner;
3. freeze the qualified runner;
4. perform a fresh final execution preflight;
5. only then execute authoritative Phase 6E-A sufficiency science.

No Phase 6E-A scientific result exists until that later frozen runner executes successfully under this protocol.
