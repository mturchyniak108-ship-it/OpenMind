# OpenMind Phase 6E-A Reference-State Fixture Preregistration V1

## Status

**PROSPECTIVE PREREGISTRATION — NOT YET FROZEN**

Freezing this document authorizes only deterministic reference-fixture construction and qualification. It does not authorize Phase 6E-A scientific execution, selector-sufficiency evaluation, inference, bounded expansion, tensor/object avoidance claims, output-fidelity claims, performance claims, or MAF-native compute.

## Scientific question

Phase 6E-A asks whether the initial non-oracle Q2-selected MAF working set is sufficient to reproduce the independently frozen full-reference state required by the comparison contract.

The reference state MUST be fixed independently of selector output and before any Phase 6E-A sufficiency result is observed.

Q2 selection and 6E-A sufficiency remain distinct:

- Q2 accepted a candidate set when it intersected an independently expected target set.
- Phase 6E-A will require the initial selected set to reproduce **every** required object payload for the supported query under a separately frozen comparison protocol.

## Frozen authority bindings

Phase 6E checkpoint:
`experiments/model_fractal/MAF_PHASE_6E_ENTRY_CHECKPOINT.md`
SHA256 `1807437ea97e46a6cc687adbbe8c384dabae45a562f1d2aef6bd37e43b4bbe35`

Query-scoped architecture:
`experiments/model_fractal/MAF_QUERY_SCOPED_WORKING_SET_ARCHITECTURE.md`
SHA256 `7df826096e506d13502e442fb11f7e1f18fb2c5a342f4214b91a3c3df043559c`

Q2 selection protocol:
`experiments/model_fractal/MAF_QUERY_TO_PK_SELECTION_V1_PROTOCOL.md`
SHA256 `b42a0643976c2393871e3b826ba5573b4de981b49603de63230d69cf57be0811`

Q2 selector:
`experiments/model_fractal/maf_query_to_pk_selection_v1.py`
SHA256 `e21c05e352fe921b791e8c936425727a98911ce7566989672a96bfd2b9613fa2`

Q2 selection configuration SHA256:
`0caeaeaafdd870e6b02ccc8b4450576883d4ef5234ba689c472e3b14d9dbe120`

Frozen query fixture:
`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_queries.json`
SHA256 `32f4636bd5e8ceee0dca8342335279a6f8e6acafe866a5469f2c23aa2655202a`

Frozen 12-object catalog:
`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_catalog.json`
SHA256 `c51ef0fabeb10e7c8a091a093aa1934620a69b2026b5a87cb02477b9dd7ca900`

Original independent expected-target protocol:
`experiments/model_fractal/MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_PROTOCOL.md`
SHA256 `9bea52de94d8784f6862eee9108afdd1f52f9ff4d4f95eb03fb78d5477e00c11`

Original selector-independent expected-target implementation:
`experiments/model_fractal/maf_query_to_pk_selection_validation_v1.py`
SHA256 `e2e32f85b1dc7015802ec51a6f214188becc5d35f45c76f4b320617ccd6cd873`

Q2 V1.4 validation protocol:
`experiments/model_fractal/MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_4_PROTOCOL.md`
SHA256 `a814bca93a6b014ee53aad234b8396c841d0efc2a9363598e8a2192f23745699`

Q2 V1.4 result:
`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_4.json`
SHA256 `b2ad49d7a9a3e1ef565e07e595efc4a4e00b283f422723553c6437ef3a42def6`

Q2 V1.4 verdict:
`experiments/model_fractal/MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_4_VERDICT.md`
SHA256 `c17198e0013fd9c0a8c59b8f09c05d4f22693dc7d56afdc0f761f55a008c2663`

Generation-construction authority:
`experiments/model_fractal/maf_query_to_pk_selection_validation_v1_generation_construction_authority.json`
SHA256 `a5e953ae2ab2dd11a9f6dc564ae5ee57cb064d6eea0a8a5517191b4a6efc1a6d`

Frozen GGUF tensor inventory:
`experiments/model_fractal/gguf_tensor_inventory_v1.json`
SHA256 `7acf6d5dc672182aee0244b1bb85a47466f33dbdcdf10bde863e24f3659240ee`

Accepted Q3 verdict:
`experiments/model_fractal/MAF_QUERY_CAPSULE_ATTACH_DETACH_CLEANUP_VALIDATION_V1_1_VERDICT.md`
SHA256 `57233349f5d79f7dd00ac1a436cd3b109153d551b416ccdd32e85ef9e3ff0d0a`

Accepted Q4 verdict:
`experiments/model_fractal/MAF_QUERY_ROUTE_CACHE_VALIDATION_V1_3_VERDICT.md`
SHA256 `cfff3cee4062cfe6df440c3c69aa7abb65e612b0e521a626fc163821339992c6`

The Q2 V1.4 namespace is permanently spent. Rerunning Q2 V1.4 is forbidden.

## Frozen source identity

Model PK:
`mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258`

Source generation PK:
`mafgen:v1:45a80a2aa271ce04853003185b6a1227cb309bd1e3e2dc538eea849fac9f5db0`

Source generation manifest SHA256:
`28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3`

Canonical source GGUF:
`/data/data/com.termux/files/home/qwen2.5-coder-q8_0.gguf`

Canonical source GGUF SHA256:
`507de59046601282ba768a9789900e6ccf60ed93ddf346730b7c68eb0715bc47`

The generation authority requires every dedicated MAF object payload SHA256 to equal the frozen GGUF inventory payload SHA256 for the same tensor. That payload digest is the numerical reference identity used by this fixture.

## Independent expected-target authority

The frozen Q2 expected-target oracle is evaluation authority only. Its target derivation is independent of selector execution.

It defines:

- `specific_intent`: exactly one independently required object PK;
- `multi_target_intent`: two or more independently required object PKs;
- `fallback_control`: zero metadata-eligible required object PKs.

Expected targets MUST NOT be supplied to the selector.

The frozen Q2 V1.4 result records `unique_expected_object_pk_count = 12`. This is a qualification cross-check only and is not a Phase 6E-A sufficiency result.

## Reserved fixture

Path:
`experiments/model_fractal/maf_phase_6e_a_reference_state_fixture_v1.json`

Schema:
`openmind.maf_phase_6e_a_reference_state_fixture.v1`

Canonical serialization is UTF-8 JSON with `sort_keys=true`, `ensure_ascii=false`, separators `,` and `:`, and exactly one trailing newline.

## Exact top-level fields

The fixture MUST contain exactly:

1. `schema`
2. `fixture_version`
3. `source_model_pk`
4. `source_generation_pk`
5. `source_manifest_sha256`
6. `source_gguf_sha256`
7. `query_fixture_sha256`
8. `catalog_sha256`
9. `expected_target_protocol_sha256`
10. `expected_target_implementation_sha256`
11. `gguf_tensor_inventory_sha256`
12. `queries`
13. `objects`

No selected-state or scientific-result field is permitted.

## Query reference records

The `queries` array MUST contain exactly 40 records in frozen order `q001` through `q040`.

Each query record MUST contain exactly:

1. `query_id`
2. `query_class`
3. `query_text_sha256`
4. `required_object_pks`

`query_text_sha256 = sha256(query_text.encode("utf-8")).hexdigest()`.

`required_object_pks` MUST derive only from the frozen independent expected-target oracle and MUST be in ascending lexical object-PK order.

Cardinality is frozen:

- `specific_intent`: exactly 1;
- `multi_target_intent`: at least 2;
- `fallback_control`: exactly 0.

Selector output MUST NOT be consulted during reference derivation.

## Object reference records

The `objects` array contains exactly one record for every distinct non-empty required object PK and is sorted lexically by `object_pk`.

Each object record MUST contain exactly:

1. `object_pk`
2. `tensor_name`
3. `tensor_type`
4. `dims`
5. `element_count`
6. `payload_sha256`

The first five fields bind to the frozen catalog/generation authority. `payload_sha256` binds to the frozen GGUF tensor inventory for the same tensor and MUST agree with generation-construction authority.

No tensor values or MAF object bytes are stored in this fixture.

## Reference-state rule

For a supported query, the full reference state is the complete set of canonical object payload identities named by `required_object_pks`.

A future Phase 6E-A protocol may classify the initial selected working set as sufficient only if it reproduces every required object payload in this independently frozen state.

Fallback controls MUST be reported separately. Their empty required set MUST NOT count as automatic Phase 6E-A success.

Post-hoc expansion is forbidden. Bounded expansion belongs to Phase 6E-B.

## Construction order

After this preregistration is frozen:

1. verify every authority path and SHA256;
2. verify the frozen source identities;
3. load the 40-query fixture;
4. load the frozen 12-object catalog;
5. derive required targets only through the frozen independent expected-target authority;
6. prove derivation does not import or call the Q2 selector;
7. resolve every required PK against the frozen catalog;
8. resolve every payload SHA256 against the frozen GGUF inventory;
9. verify model/generation/manifest/catalog/payload bindings;
10. serialize canonical candidate fixture bytes;
11. independently reconstruct the fixture;
12. require byte-identical reconstruction;
13. freeze the qualified fixture before any selector-sufficiency execution.

Selector execution MUST NOT occur before the reference fixture is frozen.

## Mandatory qualification checks

RF01 — preregistration SHA binding.
RF02 — Phase 6E checkpoint binding.
RF03 — query-scoped architecture binding.
RF04 — query fixture SHA binding.
RF05 — catalog SHA binding.
RF06 — source generation and manifest binding.
RF07 — source model PK binding.
RF08 — source GGUF SHA binding.
RF09 — GGUF inventory SHA binding.
RF10 — independent target protocol SHA binding.
RF11 — independent target implementation SHA binding.
RF12 — exactly 40 query records in `q001` through `q040` order.
RF13 — exact class counts: 24 specific, 8 multi-target, 8 fallback.
RF14 — every specific query has exactly one required PK.
RF15 — every multi-target query has at least two required PKs.
RF16 — every fallback query has zero required PKs.
RF17 — exactly 12 unique specific-intent required PKs.
RF18 — every required PK exists exactly once in the frozen catalog.
RF19 — every `required_object_pks` sequence is lexically sorted.
RF20 — every required object has exactly one fixture object record.
RF21 — fixture object records are lexically sorted by `object_pk`.
RF22 — object metadata matches frozen catalog/generation authority.
RF23 — every `payload_sha256` matches frozen GGUF inventory authority.
RF24 — fixture construction does not import, call, or execute the Q2 selector.
RF25 — fixture contains no `selected_object_pks`, selector rank, score, hit, or success.
RF26 — fixture contains no sufficiency, fidelity, avoidance, or performance result.
RF27 — fixture construction executes no inference.
RF28 — fixture construction executes no MAF-native compute.
RF29 — fixture construction performs no network access.
RF30 — two independent constructions are byte-identical.

Failure of any RF check invalidates the candidate fixture.

The fixture MUST NOT be repaired after observing Phase 6E-A selector sufficiency. Material changes require a fresh frozen namespace or construction authority before scientific execution.

## Claim boundary

Freezing this preregistration establishes only that the reference-state fixture design was fixed prospectively.

It does **not** establish fixture construction, selective working-set sufficiency, inference, actual tensor/object avoidance, output/logit/token parity, answer quality, performance improvement, MAF-native compute, or replacement of conventional LLM execution.

## Authorization after freeze

Authorized next:

1. freeze a deterministic reference-fixture construction protocol or implementation;
2. construct and qualify the fixture under RF01–RF30;
3. freeze the qualified fixture;
4. then design and freeze the Phase 6E-A sufficiency protocol.

Still forbidden:

- Phase 6E-A scientific execution;
- selector-sufficiency evaluation;
- post-hoc or bounded expansion;
- Phase 6E-C avoidance claims;
- Phase 6E-D fidelity claims;
- Phase 6F performance claims;
- MAF-native compute;
- rerunning Q2 V1.4.

## Next gate

**FREEZE AND REVIEW THIS PREREGISTRATION BEFORE FIXTURE CONSTRUCTION.**
