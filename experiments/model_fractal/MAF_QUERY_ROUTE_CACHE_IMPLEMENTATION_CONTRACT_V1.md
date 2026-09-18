# MAF Query Route Cache Implementation Contract V1

**Status:** IMPLEMENTATION CONTRACT CANDIDATE — NOT YET FROZEN

**Phase:** OpenMind Phase 6D-Q4 — Query Route Cache

This document defines the proposed production implementation boundary for the already frozen Q4 validation protocol. It does not authorize Q4 scientific execution.

## 1. Frozen authority bindings

- Q4 protocol SHA256: `af587bfe685deb86ac4574b3d41d1a80b5df2cec84bce757eac8c7e307d82ad9`
- Q1 capsule data model SHA256: `f897b97011714f3c84b7350c6bb53e800232be8a5d34e5148a3e50a81952976e`
- Q2 query-to-PK selector SHA256: `e21c05e352fe921b791e8c936425727a98911ce7566989672a96bfd2b9613fa2`
- Resident PK directory SHA256: `4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6`
- Phase 6C runtime SHA256: `4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9`
- Q1 relationship-validation evidence V1 SHA256: `c8f3f27a8a4069083896b8e1c365d5edded4195bfa468bd62ee4e9c8e023f253`
- Q1 relationship-validation evidence V1.1 SHA256: `f367226f8ad130830dac3ac83dec6620487affa3f54b7f3540d390b68711d5c7`
- Q3 corrected validation runner SHA256: `26b4bef94fa5f063f7340190879d37b124bba305da60ac0abc12e83433159f99`
- Q4 protocol freeze commit: `cd32d6af4b4dd09808c872b629e72007b144a538`

## 2. Production module

The proposed production module path is:

`experiments/model_fractal/maf_query_route_cache_v1.py`

The production module must remain metadata-only.

It must not import:

- `maf_object_runtime_residency_v1`;
- either Q1 validation runner;
- the Q3 validation runner;
- inference or generation code.

The production module may use Python standard-library modules required for immutable data models, canonical JSON, SHA256, filesystem persistence, and type definitions.

The production module may import Q1 `MAFQueryCapsuleV1` and the resident PK directory data types required for explicit object-PK validation.

Q2 remains the frozen semantic authority for query selection and signatures. A cache hit must not rerun or reinterpret Q2 selection.

## 3. Existing Q1 cache class disposition

`MAFQueryRouteCacheEntryV1` in the frozen Q1 data model is not the Q4 persistent record.

Its frozen field set is:

- `schema`
- `exact_query_sha256`
- `query_signature`
- `source_generation_pk`
- `initial_pk_route`
- `additional_pks`
- `touched_pks`
- `selected_unused_pks`
- `route_config_sha256`
- `validation_metadata_sha256`

This differs materially from the frozen Q4 protocol record.

Q4 must not modify, rename, reinterpret, subclass as a compatibility shortcut, or silently repurpose `MAFQueryRouteCacheEntryV1`.

## 4. New Q4 persistent record

The production class shall be named:

`MAFQueryRouteCacheRecordV1`

Its schema shall be exactly:

`openmind.maf_query_route_cache.v1`

Its persistent fields, in protocol order, shall be exactly:

- `schema`
- `cache_pk`
- `query_signature`
- `source_generation_pk`
- `source_manifest_sha256`
- `selection_config_sha256`
- `expansion_policy`
- `max_object_budget`
- `max_expansion_rounds`
- `initial_object_pks`
- `selected_relationship_pks`
- `route_order`
- `route_payload_sha256`

No additional persistent field is permitted in V1.

The record must be immutable after construction.

## 5. Canonical serialization

Canonical bytes shall follow the existing Q1/Q2/Q3 convention:

- JSON object serialization;
- keys sorted lexicographically;
- separators `,` and `:` with no insignificant whitespace;
- UTF-8;
- non-ASCII characters preserved rather than escaped when supported by the existing convention;
- non-finite numeric values rejected;
- exactly one trailing newline for persisted canonical record bytes.

The Q4 production module shall implement its own small canonicalization helper following the frozen convention. It must not import helper functions from a validation runner.

`MAFQueryRouteCacheRecordV1.canonical_bytes()` must be deterministic.

`from_json_bytes()` must reject malformed data and must support canonical-readback validation.

## 6. Cache identity

The cache identity fields shall be exactly:

- `query_signature`
- `source_generation_pk`
- `source_manifest_sha256`
- `selection_config_sha256`
- `expansion_policy`
- `max_object_budget`
- `max_expansion_rounds`

The implementation shall expose a deterministic identity mapping containing only those fields and in that semantic order.

`cache_pk` shall be:

`mafroutecache:v1:` + SHA256(canonical JSON bytes of the identity mapping without the persisted trailing newline).

A supplied or deserialized `cache_pk` that does not equal the deterministic value must be rejected.

## 7. Route payload integrity

The route payload fields shall be exactly:

- `initial_object_pks`
- `selected_relationship_pks`
- `route_order`

`route_payload_sha256` shall be SHA256 of canonical JSON bytes containing exactly those route payload fields.

Route order is semantic. Reordering `route_order` changes the payload digest.

A supplied or deserialized `route_payload_sha256` that does not equal the deterministic payload digest must be rejected.

## 8. Q1 capsule integration

The production module may provide:

`build_route_cache_record_v1(capsule: MAFQueryCapsuleV1) -> MAFQueryRouteCacheRecordV1`

This factory may copy only fields already present in the frozen Q1 capsule that are required by the Q4 protocol.

The factory must compute `cache_pk` and `route_payload_sha256`; callers must not provide authoritative digest values.

The factory must not alter the capsule, rerun selection, attach runtime objects, or materialize tensors.

## 9. Object-PK validation

The resident PK directory remains the production object-resolution authority.

Before reuse, every object PK referenced by `initial_object_pks` and `route_order` must resolve under the expected model and `source_generation_pk` using a caller-supplied `ResidentPKSnapshot` or equivalent frozen resident-directory lookup surface.

The record itself does not persist `model_pk`, resident-directory objects, paths, mmap state, file descriptors, or lookup handles.

Unknown, stale-generation, cross-model, or otherwise unresolved object PKs must fail closed.

Object validation must not cause runtime attachment.

## 10. Relationship-PK validation

Neither the frozen Q2 selector nor the resident PK directory exposes a production relationship-PK lookup API.

The two frozen Q1 validation files are evidence of relationship validation semantics only. Production Q4 must not import them.

Production reuse validation shall therefore accept an explicit caller-supplied immutable relationship authority set:

`relationship_authority_pks: AbstractSet[str]`

Every value in `selected_relationship_pks` must be an exact member of that set.

An unknown relationship PK must fail closed.

The Q4 module must not derive new relationship PKs, reinterpret relationships, or treat the validation runners as runtime authorities.

The supplied relationship authority set is ephemeral validation context and is never persisted inside the route-cache record.

## 11. Exact-context reuse API

The production module shall provide a pure validation surface equivalent to:

`validate_route_cache_for_reuse_v1(*, record, expected_query_signature, expected_source_generation_pk, expected_source_manifest_sha256, expected_selection_config_sha256, expected_expansion_policy, expected_max_object_budget, expected_max_expansion_rounds, model_pk, resident_snapshot, relationship_authority_pks) -> None`

Validation must fail closed unless:

- schema is exact;
- `cache_pk` is deterministic and exact;
- every expected identity field matches exactly;
- `route_payload_sha256` is exact;
- route structure is valid;
- every referenced object PK resolves under the expected generation;
- every selected relationship PK is present in the supplied relationship authority set.

This API validates metadata only.

It must not attach, pin, map, materialize, transition runtime state, or allocate dense model state.

## 12. Validated route return surface

After successful validation, a separate pure helper may expose the validated route metadata:

`validated_route_payload_v1(record) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]`

The returned values correspond exactly to:

1. `initial_object_pks`;
2. `selected_relationship_pks`;
3. `route_order`.

This helper does not construct runtime ownership and does not prove working-set sufficiency.

## 13. Persistence API

The production module shall provide:

`write_route_cache_record_v1(path: Path, record: MAFQueryRouteCacheRecordV1) -> None`

`read_route_cache_record_v1(path: Path) -> MAFQueryRouteCacheRecordV1`

V1 persistence shall use the audited Q3 durability pattern as an implementation pattern, not as an imported dependency:

1. canonicalize record bytes;
2. if the final path already exists, read it and accept only byte-identical canonical content as idempotent success;
3. otherwise create a sibling partial file with exclusive creation;
4. write the complete canonical bytes;
5. flush and `fsync` the partial file;
6. atomically publish without overwriting an existing final record;
7. `fsync` the containing directory after publication.

A pre-existing final record with different bytes must fail closed.

A malformed or noncanonical persisted record must fail closed on read.

V1 exposes no cache deletion API and no eviction policy.

## 14. Cleanup and runtime separation

Q3 cleanup remains authoritative.

A persistent Q4 record must never own:

- a runtime object;
- a pin or lease;
- mapped or serialized model payload state;
- a dense or materialized tensor view;
- Query Capsule attachment;
- file descriptors or mmap handles associated with model payloads.

The production Q4 module must not import the Phase 6C runtime.

Q4 validation integration may separately observe the runtime to prove Q3 cleanup compatibility, but that integration belongs in the future validation harness and not in production Q4 source.

## 15. Error model

The production module shall define a Q4-specific exception hierarchy rooted at:

`MAFQueryRouteCacheError`

At minimum, distinct fail-closed errors shall cover:

- invalid record/schema or structural data;
- identity mismatch or cache miss;
- route-payload integrity failure;
- unresolved object PK;
- unresolved relationship PK;
- persistence or canonical-readback failure.

Exception types must not encode inference, quality, or sufficiency semantics.

## 16. Forbidden production dependencies

The Q4 production module must not import or call:

- `maf_object_runtime_residency_v1`;
- `maf_query_capsule_data_model_validation_v1`;
- `maf_query_capsule_data_model_validation_v1_1`;
- `maf_query_capsule_attach_detach_cleanup_validation_v1`;
- `maf_query_capsule_attach_detach_cleanup_validation_v1_1`;
- any Q4 validation runner;
- inference or generation engines.

## 17. Q4 scientific boundary

Implementation acceptance is not scientific acceptance.

Freezing and testing the production module does not establish:

- selective working-set sufficiency;
- Phase 6E;
- inference or generation capability;
- answer or model quality;
- performance benefit;
- cache hit-rate benefit;
- parity, avoidance, or replacement of conventional inference;
- MAF-native model computation.

No Q4 scientific result may exist until the separate validation runner is prereviewed and frozen under the already frozen 44-check protocol.

## 18. Candidate disposition

This contract is a candidate only.

Before production source is written:

1. this exact contract must receive independent static review against the frozen Q4 protocol;
2. any protocol mismatch must be resolved in the contract, never by altering the frozen Q4 protocol;
3. the accepted contract must be frozen as an exact-path Git commit.

At candidate creation:

- Q3: CLOSED;
- Q4 protocol: FROZEN;
- Q4 production implementation: NOT STARTED;
- Q4 scientific validation: NOT ENTERED;
- Phase 6E: NOT ENTERED.
