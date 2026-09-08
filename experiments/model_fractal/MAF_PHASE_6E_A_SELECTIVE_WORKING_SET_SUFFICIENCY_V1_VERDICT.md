# OpenMind Phase 6E-A Selective Working-Set Sufficiency V1 Verdict

## Status

**VERDICT: PASS**

Phase 6E-A establishes that, for the frozen 40-query validation population and the frozen accepted Q2 selector configuration, the initial non-oracle Q2-selected MAF working set was sufficient to reproduce every required frozen reference object payload for all 32 evaluable non-fallback queries, with no expansion.

The 8 fallback-control queries were reported separately as `CONTROL` and did not contribute to the sufficiency numerator or denominator.

This verdict is limited to the frozen object-state payload-identity comparison contract defined by the Phase 6E-A protocol.

## Frozen evidence chain

- Phase 6E-A reference-state fixture freeze commit: `0a984b5bbfab1a6cf8c66f26cdfbc5a47382f647`
- Phase 6E-A sufficiency protocol freeze commit: `383243f54f991c09a100b8af5cbd98361f43efb5`
- Phase 6E-A frozen science runner commit: `7cf66034e3cf66356584cd3f02b1d2c556e31a64`
- Phase 6E-A qualified result freeze commit: `729047e47fdf1093bac4b60a1da21122d2b456dc`

### Frozen Phase 6E-A protocol

Path:

`experiments/model_fractal/MAF_PHASE_6E_A_SELECTIVE_WORKING_SET_SUFFICIENCY_PROTOCOL_V1.md`

SHA256:

`0ecf4936969f890b3d9f9c398541246642ac46f2edf975c32c121e8f4189ee1d`

### Frozen reference fixture

Path:

`experiments/model_fractal/maf_phase_6e_a_reference_state_fixture_v1.json`

SHA256:

`870b656e0c3181ec8f7be1537bdeafde10fffd1b947f5372d21cdee4c00a83a0`

### Frozen Phase 6E-A runner

Path:

`experiments/model_fractal/maf_phase_6e_a_selective_working_set_sufficiency_v1.py`

SHA256:

`72c0eca00013e0b70c4a95c4043f0a11b0b6b3d885166a898014f74b928961d6`

### Frozen qualified Phase 6E-A result

Path:

`experiments/model_fractal/maf_phase_6e_a_selective_working_set_sufficiency_v1.json`

Bytes:

`66018`

SHA256:

`f86433603e68fc9f1e5c65f7d3ecbd8d9ce9313d252c605dd6e2cada18a91c86`

Selection snapshot SHA256:

`06382d7b4fa181f07024b4cb786634db1d8d7bc56d17ae53face4898e545a3c3`

## Frozen source and selector bindings

Source model PK:

`mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258`

Source generation PK:

`mafgen:v1:45a80a2aa271ce04853003185b6a1227cb309bd1e3e2dc538eea849fac9f5db0`

Source generation manifest SHA256:

`28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3`

Source GGUF SHA256:

`507de59046601282ba768a9789900e6ccf60ed93ddf346730b7c68eb0715bc47`

Accepted Q2 selector SHA256:

`e21c05e352fe921b791e8c936425727a98911ce7566989672a96bfd2b9613fa2`

Frozen Q2 selection configuration SHA256:

`0caeaeaafdd870e6b02ccc8b4450576883d4ef5234ba689c472e3b14d9dbe120`

Frozen Q2 maximum candidate budget:

`4`

Frozen query fixture SHA256:

`32f4636bd5e8ceee0dca8342335279a6f8e6acafe866a5469f2c23aa2655202a`

Frozen catalog SHA256:

`c51ef0fabeb10e7c8a091a093aa1934620a69b2026b5a87cb02477b9dd7ca900`

Frozen generation-construction authority SHA256:

`a5e953ae2ab2dd11a9f6dc564ae5ee57cb064d6eea0a8a5517191b4a6efc1a6d`

## Prospective execution contract

The authoritative execution followed the frozen Phase 6E-A ordering:

1. Verify frozen identities and repository state.
2. Load the accepted Q2 selector inputs.
3. Execute all 40 Q2 selections without reading the reference target sets.
4. Freeze the canonical 40-query selection snapshot.
5. Only after the snapshot is frozen, load the independently frozen Phase 6E-A reference fixture.
6. Evaluate the immutable initial selected sets against the required object PKs.
7. Reopen generation-bound MAF objects and observe actual payload SHA256 identities.
8. Compare observed payload identities to the frozen reference fixture.
9. Preserve fallback controls separately.
10. Aggregate the result under the exact 32-of-32 Phase 6E-A rule.

No selected object PK was added after the selection snapshot. Maximum expansion rounds were zero.

## Authoritative result

Frozen population:

- 40 total queries
- 24 `specific_intent`
- 8 `multi_target_intent`
- 8 `fallback_control`
- 32 evaluable non-fallback queries

Observed result:

- Evaluable PASS: `32`
- Evaluable FAIL: `0`
- Fallback CONTROL: `8`
- Phase 6E-A verdict: `PASS`

The exact prospective acceptance threshold was 32 of 32 evaluable queries. That threshold was met.

## Object-payload result

The frozen reference state contained 12 unique required MAF object PKs.

Independent post-run qualification reopened all 12 generation-bound MAF object files and verified:

- the frozen generation manifest identity;
- the object placement set;
- each serialized MAF object file SHA256 against its generation placement;
- each object tensor identity and metadata against the frozen reference object record;
- each actual observed MAF payload SHA256 against the generation manifest payload identity;
- each actual observed MAF payload SHA256 against the independently frozen reference fixture payload identity.

All 12 unique required object payload identities passed independent qualification.

For every evaluable query:

- `missing_required_pks` was empty;
- `payload_mismatch_pks` was empty;
- the number of payload-evidence records equaled the required-object count;
- every required payload-evidence record had `payload_match = true`;
- no expansion occurred.

## Independent post-run qualification

The independent qualifier did not rerun the frozen Phase 6E-A science runner and did not rerun the Q2 selector.

It independently recomputed and verified:

- exact 66,018-byte result identity;
- canonical result JSON;
- frozen authority bindings;
- canonical selection-snapshot SHA256;
- all 12 generation-bound serialized-object identities;
- all 12 actual MAF payload SHA256 identities;
- all 40 query set relations;
- all per-query verdicts;
- the exact 32-of-32 aggregate rule;
- the separate 8 fallback-control verdicts;
- repository preservation.

Independent qualification verdict:

`PASS`

Recomputed Phase 6E-A scientific verdict:

`PASS`

## Execution-wrapper display note

The outer execution wrapper printed `Result absent before execution : FAIL` after the authoritative run because that display expression checked the result path after the frozen runner had already created the result artifact.

The same wrapper recorded `Execution precondition : PASS`, launched the frozen runner exactly once, and preserved the result. The later independent result qualification verified the exact result and repository state without rerunning the science.

This display-timing artifact does not alter the Phase 6E-A scientific result.

## Claim authorized by Phase 6E-A

For the frozen Phase 6E-A validation population, frozen source generation, accepted Q2 selector, and frozen selection configuration, the initial query-selected MAF working set was sufficient to reproduce every required frozen reference object payload identity for all 32 evaluable queries without expansion.

This is an object-state sufficiency result.

## Claims not authorized by Phase 6E-A

This verdict does **not** establish any of the following:

- that unselected model objects or tensors were not physically read;
- model-access avoidance;
- bytes-read reduction;
- memory reduction;
- materialization reduction;
- inference correctness;
- logit parity;
- token parity;
- answer parity;
- output quality;
- latency improvement;
- throughput improvement;
- energy improvement;
- MAF-native model computation;
- dense-runtime replacement.

Those claims remain reserved for later phases.

## Phase boundary

Phase 6E-A is complete at the frozen object-state sufficiency boundary.

The next research phase is Phase 6E-B, which may test bounded deterministic expansion or recovery behavior under its own prospective frozen contract.

Actual access or materialization avoidance remains Phase 6E-C.

Output, logit, token, or answer fidelity remains Phase 6E-D.

Performance remains Phase 6F.

Direct MAF-native computation remains disabled and unvalidated until separately authorized and validated.

## Final verdict

**PHASE 6E-A: PASS**

The frozen initial Q2-selected working sets reproduced all required frozen MAF object payload identities for all 32 evaluable queries with zero expansion, while 8 fallback controls remained separately classified as `CONTROL`.

No broader inference, avoidance, fidelity, performance, or MAF-native-compute claim is made by this verdict.
