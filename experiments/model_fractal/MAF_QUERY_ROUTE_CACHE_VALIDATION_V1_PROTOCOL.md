# MAF Query Route Cache Validation V1 Protocol

**Status:** PREREGISTRATION CANDIDATE — NOT YET FROZEN

**Phase:** OpenMind Phase 6D-Q4 — Query Route Cache

Creating or reviewing this candidate does not constitute Q4 scientific entry. No Q4 implementation, persistent cache write, validation execution, or scientific claim is authorized until this protocol is independently reviewed and frozen.

## 1. Primary authority and prior phase boundary

- Primary architecture: `experiments/model_fractal/MAF_QUERY_SCOPED_WORKING_SET_ARCHITECTURE.md`
- Primary architecture SHA256: `7df826096e506d13502e442fb11f7e1f18fb2c5a342f4214b91a3c3df043559c`
- Q3 closure commit: `e498aef49fcc6843b1d46da304fb018be2d82f89`
- Q3 V1.1 verdict SHA256: `57233349f5d79f7dd00ac1a436cd3b109153d551b416ccdd32e85ef9e3ff0d0a`
- Q3 V1.1 result SHA256: `2db54aca02c913ff9c54728aeb63bca6f280296a8564ef6a388be2e994290690`
- Q3 V1.1 permanent slot SHA256: `d20826af7c080b8660233ae9790fc761cbcd81d4bb45e9e033177f981455fa95`

Q3 is closed. V1 and V1.1 are permanently non-rerunnable. Q4 must not alter any Q3 evidence.

## 2. Scientific question

Can OpenMind persist only query-route derived metadata, reuse it deterministically for an exactly matching query and source-generation context, reject or invalidate stale or corrupted route metadata, and preserve that metadata across Query Capsule cleanup without retaining runtime ownership, serialized payload state, dense materialization, or other ephemeral query state?

This question concerns route-metadata identity, persistence, integrity, exact-context reuse, invalidation, and interaction with the already validated Q3 cleanup lifecycle.

## 3. Q4 object: Query Route Cache record

The Q4 cache is derived metadata. It is not canonical model state and is not a replacement for the immutable MAF generation.

The initial V1 cache record schema shall be:

`openmind.maf_query_route_cache.v1`

A cache record shall contain only the minimum information required to identify and validate a previously derived route:

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

No tensor bytes, dense vectors, mapped buffers, serialized MAF payload bytes, open file descriptors, mmap objects, runtime object references, pin handles, leases, Query Capsule object references, or engine-owned path handles may be part of the persistent cache record.

## 4. Cache identity

The cache lookup identity shall be computed before route reuse from canonical query/context identity fields:

`query_signature`
`source_generation_pk`
`source_manifest_sha256`
`selection_config_sha256`
`expansion_policy`
`max_object_budget`
`max_expansion_rounds`

`cache_pk` shall be deterministic:

`mafroutecache:v1:` + SHA256(canonical JSON of the ordered identity object).

The route payload itself is not part of the lookup key. Route content integrity is independently bound by `route_payload_sha256`.

Two records with identical lookup identity must produce the same `cache_pk`. Any change to a lookup-identity field must produce a different lookup identity and must not reuse the previous record.

## 5. Route payload integrity

`route_payload_sha256` shall bind canonical JSON containing exactly:

- `initial_object_pks`
- `selected_relationship_pks`
- `route_order`

Route order is semantic and must remain exact. Reordering an otherwise identical set is a payload change.

Before reuse, every referenced object PK and relationship PK must resolve under the currently bound frozen authorities. A record containing an unknown, missing, malformed, duplicated where prohibited, or authority-inconsistent PK must fail closed.

## 6. Generation and source binding

Cache reuse is generation-bound.

A route derived for one `source_generation_pk` must never be reused for another generation.

A route must also match the exact `source_manifest_sha256`. An identical query signature does not authorize reuse across a generation or manifest change.

Selection configuration and route-policy identity are also part of the cache identity. A configuration, budget, round limit, or expansion-policy mismatch is a cache miss, not permission to reinterpret the existing record.

No stale cache record may be silently rebound to a new generation, manifest, selector configuration, or route policy.

## 7. Persistence and reuse

A valid route-cache record may survive the end of a Query Capsule because it is persistent derived metadata rather than live query state.

Persistence does not imply runtime residency.

On an exact identity match, a cache record may supply its validated route metadata for reconstruction of a new Query Capsule route.

Reuse must revalidate:

- cache schema;
- deterministic `cache_pk`;
- exact identity fields;
- `route_payload_sha256`;
- object-PK and relationship-PK resolution;
- route ordering and structural validity.

A cache hit must not itself attach, pin, map, materialize, or create dense state. Those runtime transitions remain governed by their separate lifecycle.

## 8. Invalidation

Invalidation means that a cache record is not eligible for reuse.

The V1 validation must demonstrate fail-closed invalidation for at least:

- changed `query_signature`;
- changed `source_generation_pk`;
- changed `source_manifest_sha256`;
- changed `selection_config_sha256`;
- changed `expansion_policy`, object budget, or expansion-round limit;
- corrupted `route_payload_sha256`;
- altered route order;
- unknown or invalid object PK;
- unknown or invalid relationship PK;
- malformed cache schema.

Invalidating or discarding derived route metadata must never delete, rewrite, mutate, or re-identify the canonical MAF generation.

Physical stale-cache deletion policy and cache eviction policy are not part of the Q4 V1 scientific question. Logical rejection is sufficient for the validation.

## 9. Interaction with Q3 cleanup

Q3 cleanup semantics remain authoritative.

After a query using a valid cached route completes, cleanup must still release:

- dense/materialized views;
- runtime MAF ownership;
- ownership leases and pins;
- query-scoped descriptors and maps;
- Query Capsule attachment;
- ephemeral materialization.

After cleanup, the validated derived route-cache record may remain persistent.

The existence of a persistent route record must not keep an object above `COLD_DISK`, retain serialized bytes, retain dense bytes, retain a lease, retain a pin, or prevent runtime close semantics.

Repeated reuse and cleanup must return the runtime to the same clean baseline established by Q3.

## 10. Frozen initial validation cases

Q4 V1 shall initially reuse the four already exercised Q3 query cases:

- `q001`
- `q025`
- `q026`
- `q033`

The purpose is not to measure generalization or sufficiency. These cases provide controlled route/cache lifecycle coverage against already frozen Q2/Q3 authorities.

No query-case expansion is permitted after the validation protocol is frozen.

## 11. Required validation categories

The future validation runner must cover:

1. authority/source binding;
2. deterministic identity construction;
3. canonical persistence/readback;
4. valid exact-context cache reuse;
5. stale-context rejection;
6. payload corruption rejection;
7. PK/relationship structural validation;
8. metadata-only persistence;
9. Q3 cleanup compatibility;
10. repeated reuse/cleanup baseline restoration;
11. immutable canonical-generation preservation;
12. phase and claim-boundary enforcement.

## 12. Frozen scientific acceptance checks

The validation check identifiers and order are preregistered as follows:

- Q4-V01_primary_architecture_binding
- Q4-V02_q3_closure_verdict_binding
- Q4-V03_q3_result_binding
- Q4-V04_q3_permanent_slot_binding
- Q4-V05_q3_closed_and_nonrerunnable_boundary
- Q4-V06_frozen_q2_selector_authority_binding
- Q4-V07_source_generation_and_manifest_binding
- Q4-V08_exact_preregistered_query_case_set
- Q4-V09_cache_schema_exact
- Q4-V10_cache_pk_deterministic
- Q4-V11_canonical_cache_serialization_deterministic
- Q4-V12_query_signature_identity_binding
- Q4-V13_source_generation_pk_identity_binding
- Q4-V14_source_manifest_sha256_identity_binding
- Q4-V15_selection_config_identity_binding
- Q4-V16_route_policy_and_budget_identity_binding
- Q4-V17_initial_object_pks_payload_exact
- Q4-V18_selected_relationship_pks_payload_exact
- Q4-V19_route_order_payload_exact
- Q4-V20_route_payload_sha256_integrity
- Q4-V21_persistent_record_metadata_only
- Q4-V22_no_dense_payload_persistence
- Q4-V23_no_serialized_maf_payload_persistence
- Q4-V24_no_runtime_handles_or_ownership_persistence
- Q4-V25_first_persistence_readback_exact
- Q4-V26_repeated_persistence_idempotent
- Q4-V27_exact_context_cache_reuse_accepted
- Q4-V28_query_signature_mismatch_rejected
- Q4-V29_generation_pk_mismatch_rejected
- Q4-V30_manifest_sha_mismatch_rejected
- Q4-V31_selection_config_mismatch_rejected
- Q4-V32_route_policy_or_budget_mismatch_rejected
- Q4-V33_route_payload_digest_corruption_rejected
- Q4-V34_route_order_tamper_rejected
- Q4-V35_unknown_object_pk_rejected
- Q4-V36_unknown_relationship_pk_rejected
- Q4-V37_malformed_cache_schema_rejected
- Q4-V38_q3_cleanup_preserves_allowed_route_metadata
- Q4-V39_q3_cleanup_releases_all_runtime_state
- Q4-V40_invalid_cache_never_mutates_canonical_generation
- Q4-V41_repeated_cache_reuse_returns_clean_baseline
- Q4-V42_cache_hit_does_not_imply_runtime_attachment
- Q4-V43_route_expansion_inference_sufficiency_and_performance_excluded
- Q4-V44_phase_boundary_and_no_replacement_claim

All 44 checks must pass. There is no partial scientific PASS.

After this protocol is frozen, scientific check identifiers, order, query-case set, cache identity fields, route-payload fields, invalidation cases, and claim boundary may not be changed by the validation runner.

## 13. Validation execution discipline

Q4 implementation and Q4 validation are separate steps.

No Q4 science may execute during protocol drafting, protocol review, implementation drafting, static implementation review, or runner drafting.

Before the scientific arm:

- the protocol must be frozen;
- the cache implementation must be independently reviewed and frozen;
- the validation runner must be independently reviewed and self-hash frozen;
- the Q4 result namespace must be empty;
- all frozen Q2/Q3/source authorities must match exactly;
- the repository must satisfy the preregistered clean-state gates.

The scientific validation shall use a single exact-once result namespace. Once its durable slot is created, that namespace is permanently spent whether the run passes, fails, or aborts. No scientific retry is permitted in the same namespace.

## 14. Claim boundary

A successful Q4 result may establish only that generation-bound query-route derived metadata can be deterministically persisted, validated, safely reused under exact identity, rejected when stale or corrupted, and preserved across Q3 cleanup without retaining prohibited runtime state.

Q4 does not establish:

- route expansion quality or usefulness;
- selective working-set sufficiency;
- Phase 6E;
- inference or generation capability;
- answer correctness or answer quality;
- model quality;
- performance, latency, throughput, memory, storage, or efficiency improvement;
- cache hit-rate benefit;
- parity with a conventional inference pipeline;
- avoidance of conventional inference;
- replacement of an LLM runtime;
- MAF-native model computation.

A cache hit means only that a previously derived route record passed the frozen Q4 identity and integrity gates. It is not evidence that the cached working set is sufficient to answer a query.

## 15. Q4 / Phase 6E hard boundary

Q4 asks whether route metadata can be safely reused.

Phase 6E, if separately preregistered later, may ask whether a selected working set is sufficient for a downstream model task.

Those questions must remain separate.

No Q4 cache result may be interpreted as evidence of selective working-set sufficiency.

At protocol-candidate creation time:

- Q3: CLOSED
- Q4: NOT YET SCIENTIFICALLY ENTERED
- Phase 6E: NOT ENTERED

## 16. Candidate disposition

This document becomes authoritative only after independent review confirms conformance with the frozen query-scoped architecture and after an exact-path freeze commit.

Until then it is a preregistration candidate only.
