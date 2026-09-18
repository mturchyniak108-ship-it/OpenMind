# MAF Query Capsule Data Model V1 Protocol

## 1. Status

**PREREGISTERED PROTOCOL — PHASE 6D-Q1**

This protocol freezes the first Phase 6D-Q data-model boundary.

It defines deterministic Query-Scoped MAF Capsule and Query Route Cache
entry representations.

It does not establish query-to-PK selection correctness, selective inference,
bounded-expansion recovery, tensor avoidance, output quality, performance,
or MAF-native computation.

## 2. Frozen authorities

Phase 6E entry checkpoint:

`MAF_PHASE_6E_ENTRY_CHECKPOINT.md`

SHA256:

`7fc64010695365b73058ca450c2c161e4f3aa3758347796c8bcca826f9bc886b`

Query-scoped architecture:

`MAF_QUERY_SCOPED_WORKING_SET_ARCHITECTURE.md`

SHA256:

`7df826096e506d13502e442fb11f7e1f18fb2c5a342f4214b91a3c3df043559c`

These authority bytes define the architectural intent from which this
prospective protocol is derived.

## 3. Scientific question

Phase 6D-Q1 asks:

> Can a query-scoped PK route be represented deterministically and bound to
> one immutable source generation without becoming canonical model truth?

Phase 6D-Q1 is a representation/correctness gate.

There is no inference claim.

## 4. Implementation target

The future implementation target is:

`experiments/model_fractal/maf_query_capsule_data_model_v1.py`

The implementation version is:

`v1`

Freezing this protocol authorizes construction of that implementation only.

It does not authorize scientific validation execution.

A separate prospective validation protocol must be frozen before an
authoritative validation run.

## 5. Persistent authority boundary

Canonical MAFDB remains the immutable source of model truth.

A Query Capsule is temporary derived execution state.

A Query Route Cache entry is persistent derived metadata.

Neither may:

- replace canonical model truth;
- alter canonical MAF object bytes;
- alter source generation identity;
- silently migrate across source generations;
- store a previous generated answer as a substitute for inference.

## 6. Canonical logical identifiers

Existing canonical identifiers remain unchanged.

Generation PK:

`mafgen:v1:<64 lowercase hexadecimal characters>`

Object PK:

`mafobj:v1:<64 lowercase hexadecimal characters>`

Phase 6D-Q1 introduces Query PK:

`mafquery:v1:<64 lowercase hexadecimal characters>`

No existing PK grammar is modified.

This protocol does not introduce a new relationship-PK grammar.

Relationship or transition PKs remain opaque logical PK strings supplied by
their existing/future authority.

## 7. SHA256 representation

Every field named `*_sha256` must contain exactly 64 lowercase hexadecimal
characters.

Uppercase hexadecimal, prefixes such as `sha256:`, truncated hashes, and
non-hexadecimal strings are invalid.

## 8. Query signature boundary

`query_signature` is a deterministic non-empty UTF-8 string.

Phase 6D-Q1 deliberately treats its internal feature construction as opaque.

The same input under the same future signature/configuration algorithm must
produce the same signature.

How query-derived features are constructed and whether they are useful for
PK selection belongs to Phase 6D-Q2.

Phase 6D-Q1 MUST NOT encode answer-oracle information into the signature.

## 9. Query PK derivation

Query PK identity is generation- and configuration-bound.

Construct this logical identity object:

```json
{
  "query_signature": "<query_signature>",
  "selection_config_sha256": "<selection_config_sha256>",
  "source_generation_pk": "<source_generation_pk>",
  "source_manifest_sha256": "<source_manifest_sha256>"
}
```

Serialize it using the canonical JSON rules in this protocol.

Compute SHA256 over those canonical bytes.

Then:

`query_pk = "mafquery:v1:" + sha256_hex`

Initial selected PKs are intentionally not part of Query PK identity.

Selection output is derived state associated with the same query/configuration
identity.

## 10. Query Capsule V1 schema

Schema identifier:

`openmind.maf_query_capsule.v1`

The exact logical fields are:

1. `schema: str`
2. `query_pk: str`
3. `query_signature: str`
4. `source_generation_pk: str`
5. `source_manifest_sha256: str`
6. `initial_object_pks: tuple[str, ...]`
7. `selected_relationship_pks: tuple[str, ...]`
8. `route_order: tuple[str, ...]`
9. `expansion_policy: str`
10. `max_object_budget: int`
11. `max_expansion_rounds: int`
12. `selection_config_sha256: str`

Unknown fields are invalid in V1 canonical serialization.

## 11. Query Capsule sequence invariants

`initial_object_pks`:

- contains only canonical `mafobj:v1:` PKs;
- contains no duplicates;
- may be empty;
- must not exceed `max_object_budget`.

`selected_relationship_pks`:

- contains deterministic non-empty logical PK strings;
- contains no duplicates;
- may be empty;
- Phase 6D-Q1 does not define their semantic graph meaning.

`route_order`:

- contains exactly the same object PK set as `initial_object_pks`;
- contains each object PK exactly once;
- is the deterministic initial traversal order;
- therefore is an exact permutation of `initial_object_pks`.

Container order is authoritative.

Implementations MUST NOT silently convert these ordered sequences to sets.

## 12. Capsule budget invariants

`max_object_budget` must be an integer greater than zero.

`max_expansion_rounds` must be an integer greater than or equal to zero.

V1 recognizes exactly these expansion policy labels:

- `disabled`
- `bounded_v1`

When:

`expansion_policy == "disabled"`

then:

`max_expansion_rounds == 0`

When:

`expansion_policy == "bounded_v1"`

then:

`max_expansion_rounds > 0`

Recognition of `bounded_v1` in this data model does not establish that a
correct bounded-expansion algorithm exists.

That scientific claim belongs to Phase 6E-B.

## 13. Capsule generation binding

The capsule is bound simultaneously to:

- `source_generation_pk`;
- `source_manifest_sha256`.

A consumer operating against a different source generation or source manifest
must reject the capsule.

It MUST NOT silently rebind or reinterpret the capsule for the new authority.

## 14. Query Route Cache Entry V1 schema

Schema identifier:

`openmind.maf_query_route_cache_entry.v1`

The exact logical fields are:

1. `schema: str`
2. `exact_query_sha256: str`
3. `query_signature: str`
4. `source_generation_pk: str`
5. `initial_pk_route: tuple[str, ...]`
6. `additional_pks: tuple[str, ...]`
7. `touched_pks: tuple[str, ...]`
8. `selected_unused_pks: tuple[str, ...]`
9. `route_config_sha256: str`
10. `validation_metadata_sha256: str | None`

Unknown fields are invalid in V1 canonical serialization.

## 15. Route Cache entry invariants

`initial_pk_route` contains canonical object PKs with no duplicates.

`additional_pks` contains canonical object PKs with no duplicates.

No object PK may occur in both `initial_pk_route` and `additional_pks`.

Define:

`selected_pks = initial_pk_route + additional_pks`

`touched_pks`:

- contains no duplicates;
- may contain only PKs present in `selected_pks`;
- preserves deterministic actual-touch order.

`selected_unused_pks` must equal the selected PKs that are absent from
`touched_pks`, preserving their order in `selected_pks`.

Phase 6D-Q1 freezes these representation invariants only.

It does not establish that touching, expansion, or execution has occurred.

## 16. Validation metadata boundary

`validation_metadata_sha256` is either:

- `None`; or
- a valid lowercase SHA256 string referencing separately authorized evidence.

Phase 6D-Q1 itself produces no inference/quality evidence.

Therefore Phase 6D-Q1-only fixtures must use:

`validation_metadata_sha256 = None`

Quality metadata may become non-null only when a later prospective protocol
explicitly authorizes that evidence.

## 17. Route Cache deterministic key

The V1 exact-route cache key is the ordered tuple:

```
(
    source_generation_pk,
    exact_query_sha256,
    route_config_sha256,
)
```

This key is derived metadata identity, not canonical model truth.

Similar-query indexing is outside Phase 6D-Q1 and belongs to later
generation-bound route-cache research.

## 18. Route generation binding

A route cache entry is valid only for its exact `source_generation_pk`.

A cache lookup against a different active generation must be rejected as a
generation mismatch.

A route created against one generation MUST NOT silently become authoritative
for another generation.

## 19. Canonical JSON serialization

Canonical serialization is UTF-8 JSON using:

- `sort_keys=True`;
- `separators=(",", ":")`;
- `ensure_ascii=False`;
- no insignificant whitespace;
- no trailing newline in the canonical byte sequence.

Tuple fields serialize as JSON arrays in their authoritative order.

`None` serializes as JSON `null`.

The exact schema field set must be serialized.

Unknown keys are forbidden.

Equivalent valid objects must produce byte-identical canonical serialization.

## 20. Immutability

The future V1 implementation must expose immutable value objects.

After construction, callers must not be able to mutate authoritative fields
in place.

Caller-owned mutable inputs must not remain aliased into authoritative model
state.

## 21. Failure atomicity

Invalid construction must fail before a valid authoritative object is
published to the caller.

Validation failure must not partially mutate:

- canonical MAFDB authority;
- source generation authority;
- caller-owned input sequences;
- another previously valid Query Capsule;
- another previously valid Route Cache entry.

## 22. Cleanup and persistence boundary

Phase 6D-Q1 defines data representations only.

It does not attach a capsule to the runtime.

It does not own descriptors, maps, dense views, or MAF object residency.

It does not implement Query Route Cache persistence.

Any authoritative persistence mechanism requires its own prospective
platform-compatible correctness protocol.

Attach/detach, ownership, cleanup, and failure-atomic runtime behavior belong
to Phase 6D-Q3.

## 23. Explicit nonclaims

Successful Phase 6D-Q1 validation will not establish:

- useful query-to-PK selection;
- non-oracle selector quality;
- selective inference;
- working-set sufficiency;
- bounded-expansion recovery;
- actual object avoidance;
- actual tensor avoidance;
- answer parity;
- generation quality;
- performance improvement;
- memory improvement;
- I/O improvement;
- MAF-native compute.

## 24. Future validation requirements

A separate frozen validation protocol must prospectively test at minimum:

1. exact schema constants;
2. exact field inventory;
3. valid generation PK grammar;
4. valid object PK grammar;
5. valid Query PK grammar;
6. exact Query PK deterministic derivation;
7. canonical JSON byte determinism;
8. canonical round trip;
9. ordered sequence preservation;
10. duplicate initial-object rejection;
11. duplicate relationship-PK rejection;
12. exact route-order permutation enforcement;
13. maximum-object-budget enforcement;
14. expansion-policy invariants;
15. generation/manifest binding;
16. malformed SHA256 rejection;
17. unknown-field rejection;
18. route-cache exact key determinism;
19. duplicate route PK rejection;
20. initial/additional disjointness;
21. touched-PK subset enforcement;
22. exact selected-unused derivation;
23. generation-mismatch rejection;
24. validation-metadata boundary;
25. immutable authoritative objects;
26. mutable-input alias isolation;
27. construction failure atomicity;
28. canonical authority remains untouched;
29. no inference execution;
30. no route-cache persistence;
31. no network access;
32. no subprocess launch.

The validation protocol may add stricter checks before its own freeze.

It must not weaken these minimum requirements.

## 25. Phase progression

Freezing this protocol authorizes:

- construction of `maf_query_capsule_data_model_v1.py`;
- non-scientific static review of that candidate.

It does not authorize an authoritative validation run.

Phase 6D-Q2 remains blocked until Phase 6D-Q1 implementation receives
prospective validation and a frozen acceptance verdict.

Phase 6E-A remains blocked until Phase 6D-Q1 through Phase 6D-Q4 close.

## 26. Frozen next gate

After this protocol is frozen:

**BUILD PHASE 6D-Q1 DATA MODEL V1 IMPLEMENTATION**

No scientific execution is authorized by that build step.
