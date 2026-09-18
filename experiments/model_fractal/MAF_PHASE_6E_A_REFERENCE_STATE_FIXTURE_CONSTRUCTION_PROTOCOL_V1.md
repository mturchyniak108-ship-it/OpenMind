# OpenMind Phase 6E-A Reference-State Fixture Construction Protocol V1

Status: PROSPECTIVE — NOT FROZEN

## 1. Scope

This protocol defines deterministic construction of the Phase 6E-A reference-state fixture reserved by the frozen preregistration. It is construction authority only and does not authorize Phase 6E-A sufficiency execution.

## 2. Frozen authorities

- Preregistration: `experiments/model_fractal/MAF_PHASE_6E_A_REFERENCE_STATE_FIXTURE_PREREGISTRATION_V1.md`
  - SHA256 `8824025988ccda4adcaa21a989b9dc9dc2a567a0ea82666de5d58e94f77f3411`
  - freeze commit `fd51e7215e9ceb6bdd0ebfe3549ec0cae6725d90`
- Queries: `experiments/model_fractal/maf_query_to_pk_selection_validation_v1_queries.json`
  - SHA256 `32f4636bd5e8ceee0dca8342335279a6f8e6acafe866a5469f2c23aa2655202a`
- Catalog: `experiments/model_fractal/maf_query_to_pk_selection_validation_v1_catalog.json`
  - SHA256 `c51ef0fabeb10e7c8a091a093aa1934620a69b2026b5a87cb02477b9dd7ca900`
- Expected-target protocol: `experiments/model_fractal/MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_PROTOCOL.md`
  - SHA256 `9bea52de94d8784f6862eee9108afdd1f52f9ff4d4f95eb03fb78d5477e00c11`
- Expected-target implementation authority: `experiments/model_fractal/maf_query_to_pk_selection_validation_v1.py`
  - SHA256 `e2e32f85b1dc7015802ec51a6f214188becc5d35f45c76f4b320617ccd6cd873`
- Generation authority: `experiments/model_fractal/maf_query_to_pk_selection_validation_v1_generation_construction_authority.json`
  - SHA256 `a5e953ae2ab2dd11a9f6dc564ae5ee57cb064d6eea0a8a5517191b4a6efc1a6d`
- GGUF inventory: `experiments/model_fractal/gguf_tensor_inventory_v1.json`
  - SHA256 `7acf6d5dc672182aee0244b1bb85a47466f33dbdcdf10bde863e24f3659240ee`

Frozen identities:

- `source_model_pk` = `mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258`
- `source_generation_pk` = `mafgen:v1:45a80a2aa271ce04853003185b6a1227cb309bd1e3e2dc538eea849fac9f5db0`
- `source_manifest_sha256` = `28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3`
- `source_gguf_sha256` = `507de59046601282ba768a9789900e6ccf60ed93ddf346730b7c68eb0715bc47`

## 3. Reserved output

- Path: `experiments/model_fractal/maf_phase_6e_a_reference_state_fixture_v1.json`
- Schema: `openmind.maf_phase_6e_a_reference_state_fixture.v1`
- `fixture_version` = integer `1`

The output path MUST be absent before construction and MUST NOT be overwritten.

## 4. Selector isolation

The constructor MUST NOT import, call, execute, or consume runtime output from the Q2 selector. `selected_object_pks`, selector ranks, scores, fallback state, success state, and selector result data are forbidden inputs.

The spent runner `experiments/model_fractal/maf_query_to_pk_selection_validation_v1_4.py` MUST NOT be imported or executed.

Required target PKs come only from the frozen independent expected-target oracle.

## 5. Frozen oracle transcription

The constructor MAY contain local copies of exactly:

1. `_independent_query_intent`
2. `_independent_tensor_descriptor`
3. `_independent_targets`

Each local function MUST have the same name and be AST-equivalent to the corresponding frozen definition using `ast.dump(node, include_attributes=False)`.

Every non-builtin global value consumed by those functions MUST be explicitly identified and exact-value qualified against the frozen authority.

The constructor MUST reproduce the `_independent_targets` call semantics used inside frozen `_qualify_query_fixture`. Importing the original Q2 runner as a module is forbidden; it may be read only as frozen source bytes for SHA and AST qualification.

## 6. Pre-construction gates

Construction fails closed unless:

1. branch and expected frozen HEAD are exact;
2. tracked worktree is clean and staging is empty;
3. unrelated untracked baseline is exact;
4. every frozen authority path and SHA256 is exact;
5. frozen JSON parses;
6. queries are exactly 40 in order `q001` through `q040`, with classes 24 specific, 8 multi, 8 fallback;
7. catalog and generation authority each bind the same 12 object PKs;
8. GGUF inventory has 339 tensor records and the frozen source GGUF SHA256;
9. oracle functions and global dependencies pass static qualification;
10. target derivation contains no selector call;
11. reserved output path is absent.

No output bytes may be written before all gates pass.

## 7. Query construction

For each frozen query in original order:

1. validate `query_id`, `query_class`, and nonempty `query_text`;
2. compute `query_text_sha256 = sha256(query_text.encode("utf-8")).hexdigest()`;
3. derive targets with the qualified frozen oracle semantics;
4. sort target PKs lexicographically into `required_object_pks`;
5. require cardinality: specific exactly 1, multi at least 2, fallback exactly 0;
6. perform no selector call and no expansion.

Each query record has exactly:

1. `query_id`
2. `query_class`
3. `query_text_sha256`
4. `required_object_pks`

Fallback records remain present with an empty target array and are not automatic Phase 6E-A successes.

## 8. Object construction

Let `required_union` be the union of all `required_object_pks`. Create exactly one object record per PK in that union, ordered lexicographically by `object_pk`.

For each PK require one catalog row, one generation-authority row, and one GGUF inventory tensor. Require exact agreement on object PK, tensor name, tensor type, dims, and element count. Inventory `name`, `type`, `dims`, and `elements` MUST match, and `payload_sha256` MUST be 64 lowercase hexadecimal characters.

Each object record has exactly:

1. `object_pk`
2. `tensor_name`
3. `tensor_type`
4. `dims`
5. `element_count`
6. `payload_sha256`

The 24 specific queries MUST resolve to exactly 12 unique expected PKs. Fixture `objects` MUST equal the full required union.

## 9. Top-level fixture

Exactly 13 fields are permitted:

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

All identity values MUST equal the frozen authorities above.

## 10. Canonical bytes

Canonical bytes are exactly:

`json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8") + b"\n"`

No indentation, BOM, alternate ordering, or extra trailing bytes are permitted.

## 11. Independent reconstruction

Construction A and Reconstruction B MUST independently reload authority bytes and independently build all 40 query records, the required union, object records, top-level object, and canonical bytes.

B MUST NOT reuse A query records, object records, top-level dictionary, or serialized bytes. The paths MAY share only SHA256, canonical serialization, and the already-qualified frozen oracle definitions.

Success requires `bytes_A == bytes_B` and equal SHA256.

## 12. Qualification and write policy

The run MUST report RF01 through RF30 exactly as frozen in the preregistration. RF24 proves selector isolation; RF25 proves no selected state; RF26-RF29 prove no science, inference, MAF-native compute, or network operation; RF30 proves byte-identical reconstruction.

Build bytes in memory first. Only after all pre-write gates and A/B equality pass may the reserved output be created with exclusive-create semantics. Reread and verify exact bytes and SHA256 after writing.

If post-write qualification fails before staging or commit, remove only the exact fixture candidate created by that run and verify restoration of the prior baseline.

No Git staging or commit is part of fixture construction.

## 13. Claim boundary

A successful construction establishes only a deterministic selector-independent reference-state fixture candidate.

It does not establish working-set sufficiency, inference, actual object or tensor avoidance, output parity, logit parity, token agreement, answer quality, performance improvement, MAF-native compute, or replacement of conventional LLM execution.

## 14. Authorization boundary

Freezing this protocol authorizes only creation and qualification of a deterministic constructor under this contract. It does not authorize Phase 6E-A sufficiency execution, selector execution before the qualified fixture is frozen, bounded expansion, Phase 6E-C claims, Phase 6E-D claims, Phase 6F claims, MAF-native compute, or rerunning Q2 V1.4.

After protocol freeze:

1. create and statically qualify the constructor;
2. freeze the constructor;
3. construct and qualify the fixture once under RF01-RF30;
4. freeze the qualified fixture;
5. only then design and freeze the Phase 6E-A sufficiency protocol.

## 15. Next gate

Independent content, authority, oracle-isolation, canonicalization, and authorization review is required before staging this protocol.
