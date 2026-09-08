# MAF Query Capsule Data Model Validation V1 Protocol

## 1. Status

**PREREGISTERED SCIENTIFIC VALIDATION — PHASE 6D-Q1**

This protocol prospectively validates the frozen Query Capsule Data Model V1.

It does not validate query-to-PK selection, inference sufficiency, bounded
expansion, tensor/object avoidance, route-cache persistence, quality,
performance, or MAF-native computation.

## 2. Frozen authorities

Data-model protocol:

`MAF_QUERY_CAPSULE_DATA_MODEL_V1_PROTOCOL.md`

SHA256:

`5255a58c8c6340c251e24ae8543760fcd66a8deb8be1a8356ad5b78ad898edda`

Frozen implementation:

`maf_query_capsule_data_model_v1.py`

SHA256:

`f897b97011714f3c84b7350c6bb53e800232be8a5d34e5148a3e50a81952976e`

Phase 6E entry checkpoint SHA256:

`7fc64010695365b73058ca450c2c161e4f3aa3758347796c8bcca826f9bc886b`

The validator MUST reject execution if any frozen authority differs.

## 3. Validation target

Runner:

`experiments/model_fractal/maf_query_capsule_data_model_validation_v1.py`

Authoritative result:

`experiments/model_fractal/maf_query_capsule_data_model_validation_v1.json`

Reservation artifact:

`experiments/model_fractal/maf_query_capsule_data_model_validation_v1.json.partial`

Verdict:

`experiments/model_fractal/MAF_QUERY_CAPSULE_DATA_MODEL_VALIDATION_V1_VERDICT.md`

Result schema:

`openmind.maf_query_capsule_data_model_validation.v1`

Expected check count:

`36`

## 4. Scientific question

The validation asks:

> Does the exact frozen Data Model V1 implementation satisfy its
> preregistered deterministic, immutable, generation-bound Query Capsule and
> Query Route Cache representation contract?

No inference claim is permitted.

## 5. Fixture boundary

Validation uses deterministic synthetic identifiers and payload-free metadata.

The fixture MUST NOT:

- access a real GGUF or model;
- execute inference;
- select PKs from an answer oracle;
- persist route-cache entries;
- attach capsules to the runtime;
- open MAF segment payloads;
- invoke Phase 6D-Q2;
- invoke Phase 6E;
- benchmark performance;
- access the network;
- launch subprocesses.

Phase 6D-Q1 fixtures use:

`validation_metadata_sha256 = None`

No quality evidence is created.

## 6. Fixture qualification

The future runner MUST expose:

`--qualify-fixture`

Fixture qualification is non-spending.

It must occur before exact-once reservation.

It must prove that the deterministic synthetic fixture can construct at least:

- one valid Query Capsule;
- one valid Query Route Cache entry;
- canonical generation and object PKs;
- valid lowercase SHA256 bindings.

Fixture qualification MUST NOT execute V01-V36 or create the final/partial
result.

## 7. Guard-false behavior

The future runner MUST expose:

`--guard-false`

This mode must be inert and non-spending.

It MUST NOT:

- import or execute the scientific matrix where avoidable;
- reserve the result slot;
- write the result;
- execute V01-V36.

## 8. Exact-once arming

Scientific execution requires BOTH:

CLI:

`--arm-exact-once`

and environment:

`OPENMIND_ARM_QUERY_CAPSULE_DATA_MODEL_VALIDATION_V1=YES`

Either arm alone is insufficient.

Unarmed execution MUST NOT spend the result slot.

## 9. Exact-once reservation

Immediately before scientific execution the runner must reject if either:

- `experiments/model_fractal/maf_query_capsule_data_model_validation_v1.json` exists; or
- `experiments/model_fractal/maf_query_capsule_data_model_validation_v1.json.partial` exists.

After frozen-authority verification and fixture qualification, the runner
must reserve:

`experiments/model_fractal/maf_query_capsule_data_model_validation_v1.json.partial`

using exclusive creation equivalent to:

`O_WRONLY | O_CREAT | O_EXCL`

Once reservation succeeds, Validation V1 is permanently spent.

No automatic retry is permitted after reservation.

An auditor error after reservation is itself authoritative evidence and must
be published rather than retried.

## 10. Publication

The result must be canonical UTF-8 JSON followed by one newline.

The reserved file must be flushed and fsynced before publication.

Publication must use no-replace semantics from the reserved partial artifact
to the final result.

Existing final authority must never be overwritten.

## 11. Exact validation matrix

The authoritative scientific matrix is exactly V01 through V36, in order.

### V01 — schema_constants

Exact capsule and route-cache schema identifiers match the frozen protocol.

### V02 — field_inventory

Capsule and Route Cache dataclass field inventories exactly match the frozen
V1 inventories.

### V03 — generation_pk_grammar

Valid canonical generation PKs are accepted and malformed generation PKs are
rejected.

### V04 — object_pk_grammar

Valid canonical object PKs are accepted and malformed object PKs are rejected.

### V05 — query_pk_grammar

Canonical `mafquery:v1:` grammar is enforced.

### V06 — query_pk_exact_derivation

Independent canonical-JSON/SHA256 derivation exactly equals
`derive_query_pk(...)`.

### V07 — query_pk_generation_binding

Changing only source generation changes Query PK identity.

### V08 — query_pk_manifest_binding

Changing only source manifest changes Query PK identity.

### V09 — query_pk_configuration_binding

Changing only selection configuration changes Query PK identity.

### V10 — capsule_canonical_json

Capsule canonical bytes exactly match independently generated canonical JSON.

### V11 — capsule_round_trip

Capsule canonical bytes round-trip to an equal immutable value.

### V12 — ordered_sequence_preservation

Initial object, relationship, and route-order sequences retain authoritative
order.

### V13 — duplicate_initial_object_rejection

Duplicate initial object PKs are rejected.

### V14 — duplicate_relationship_rejection

Duplicate selected relationship/transition PK strings are rejected.

### V15 — route_order_permutation

Route order must be an exact permutation of initial object PKs.

### V16 — object_budget

Initial selected object count cannot exceed `max_object_budget`.

### V17 — disabled_expansion_policy

`disabled` requires exactly zero expansion rounds.

### V18 — bounded_expansion_policy

`bounded_v1` requires a positive expansion-round bound.

This check validates representation only, not an expansion algorithm.

### V19 — capsule_generation_mismatch

A capsule rejects a different source generation.

### V20 — capsule_manifest_mismatch

A capsule rejects a different source manifest.

### V21 — sha256_validation

Malformed, uppercase, prefixed, truncated, and non-hex SHA256 strings are
rejected wherever the V1 contract requires canonical SHA256.

### V22 — capsule_unknown_field_rejection

Unknown Query Capsule V1 fields are rejected.

### V23 — route_exact_cache_key

The exact route-cache key equals:

`(source_generation_pk, exact_query_sha256, route_config_sha256)`

### V24 — duplicate_route_pk_rejection

Duplicate object PKs inside authoritative route sequences are rejected.

### V25 — initial_additional_disjointness

An object PK cannot occur in both initial and additional route sets.

### V26 — touched_subset

Every touched PK must belong to the selected initial-plus-additional PK set.

### V27 — selected_unused_derivation

`selected_unused_pks` exactly equals selected-minus-touched while preserving
selected order.

### V28 — route_generation_mismatch

A Route Cache entry rejects lookup under a different source generation.

### V29 — validation_metadata_boundary

Phase 6D-Q1 fixtures retain:

`validation_metadata_sha256 = None`

and create no quality/inference evidence.

### V30 — route_unknown_field_rejection

Unknown Query Route Cache Entry V1 fields are rejected.

### V31 — immutable_value_objects

Capsule and Route Cache authoritative fields cannot be mutated in place.

### V32 — mutable_input_alias_isolation

Mutation of caller-owned input lists after construction cannot mutate the
authoritative objects.

### V33 — construction_failure_atomicity

Failed construction leaves previously valid authoritative objects
byte-identical.

### V34 — canonical_authority_untouched

Validation does not mutate canonical MAFDB authority, source generation
authority, or unrelated repository artifacts.

### V35 — canonical_serialization_field_set

Canonical serialization contains exactly the frozen schema field set,
with tuple values represented as arrays in authoritative order and no unknown
fields.

### V36 — scientific_boundary_exclusions

The result must record all of the following as false:

- `benchmark_executed`
- `inference_executed`
- `real_model_accessed`
- `route_cache_persistence_executed`
- `phase_6d_q2_executed`
- `phase_6e_executed`
- `network_accessed`
- `subprocess_launched`

## 12. Result schema

The authoritative JSON must contain at minimum:

- `schema`
- `exact_once`
- `runner_sha256`
- `validation_protocol_sha256`
- `data_model_protocol_sha256`
- `implementation_sha256`
- `expected_check_count`
- `check_count`
- `all_pass`
- `failed_checks`
- `checks`
- `auditor_error`
- all V36 boundary-exclusion booleans.

`checks` must contain exactly 36 ordered records corresponding to V01-V36.

Each record must contain:

- `id`
- `name`
- `passed`
- `details`

The IDs must be exactly:

`V01, V02, ... V36`

with no duplicates or omissions.

## 13. Scientific classification

Acceptance requires simultaneously:

- exact frozen authorities;
- exact-once execution;
- `check_count == 36`;
- all V01-V36 present exactly once and in order;
- `all_pass == true`;
- `failed_checks == []`;
- `auditor_error == null`;
- every V36 exclusion flag false.

Any failed check is a scientific validation failure.

A post-reservation auditor error is authoritative and MUST NOT be retried.

## 14. No benchmark claim

Validation V1 contains no performance benchmark.

No latency, throughput, memory, I/O, scaling, or superiority claim follows
from acceptance.

## 15. No inference claim

Validation V1 performs no language-model inference.

Successful acceptance proves the data-model representation contract only.

It does not establish useful PK selection or selective model sufficiency.

## 16. Phase progression

Phase 6D-Q2 remains blocked until:

1. this protocol is frozen;
2. the exact validator implementation is frozen;
3. fixture qualification passes;
4. exact-once readiness passes;
5. the authoritative result is frozen;
6. a scientific acceptance verdict is frozen.

Phase 6E-A remains blocked until Phase 6D-Q1 through Phase 6D-Q4 close.

## 17. Runner construction authorization

Freezing this validation protocol authorizes construction and non-scientific
audit of:

`experiments/model_fractal/maf_query_capsule_data_model_validation_v1.py`

It does NOT authorize the scientific exact-once execution.

## 18. Frozen next gate

After this protocol freezes:

**BUILD VALIDATION V1 RUNNER**

The runner must be statically audited and frozen before any scientific arm
is authorized.
