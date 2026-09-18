# MAF Resident PK Directory V1 Protocol

Status: Preregistered Phase 6B.9 research protocol.

## 1. Purpose

Resident PK Directory V1 defines a derived in-memory lookup surface from
stable logical MAF identity to the currently active immutable physical
generation evidence.

Its purpose is to make logical-PK lookup independent of linear manifest
scanning and independent of physical placement changes.

## 2. Phase dependency

Phase 6B.7 Atomic Activation is complete.

Phase 6B.8 Rollback is complete.

The frozen authority chain remains:

    logical model PK
        ->
    active generation authority
        ->
    immutable generation descriptor
        ->
    immutable segment / offset / length evidence

Resident PK Directory V1 must not replace or redefine this authority chain.

## 3. Derived cache, not authority

The resident directory is derived state.

It is not authoritative truth.

The canonical active-generation record remains the authority selecting the
current generation.

The canonical generation descriptor remains the authority defining immutable
logical-to-segment mapping.

A resident entry must never override contradictory active or descriptor
evidence.

## 4. No new logical identity

The directory must not invent, renumber, alias, or rewrite logical PKs.

Physical relocation, directory rebuild, process restart, activation, or
rollback must not change logical PK identity.

## 5. Authority source

A directory snapshot must be built from one exact active-generation state.

Minimum build inputs are:

    model_pk
    active_record_path
    active_candidate_manifest_path
    active_segment_paths

active_segment_paths is runtime execution metadata:

    segment_id -> physical path

It is not logical identity.

## 6. Current active authority validation

Before building or refreshing a snapshot, the active record must be strictly
reopened using the frozen active-authority validation semantics.

The active record must remain the exact frozen five-field schema:

    schema
    active_generation_version
    model_pk
    generation_pk
    generation_manifest_sha256

Malformed, noncanonical, missing, or cross-model active authority fails
closed.

## 7. Manifest binding

The supplied active candidate manifest must:

- be canonical;
- structurally validate under the frozen Generation Engine;
- match the requested model_pk;
- match the active generation_pk;
- hash exactly to active generation_manifest_sha256.

A manifest that is valid but not the currently authoritative manifest must
not populate the resident directory.

## 8. Current physical validation

The active generation's current physical evidence must validate before its
directory snapshot may become resident.

Validation must preserve the frozen Activation V1.1 rules:

- exact segment-ID mapping;
- regular-file requirement;
- exact segment length;
- exact segment SHA256;
- valid object bounds;
- exact object byte-range SHA256;
- exact reconstructed descriptor;
- exact reconstructed generation identity.

Historical validity alone is insufficient.

## 9. Snapshot model

One resident snapshot represents exactly one:

    model_pk
    generation_pk
    generation_manifest_sha256

A snapshot must not combine entries from multiple generations.

A snapshot must not combine entries from multiple models.

## 10. Snapshot identity metadata

Each snapshot must retain at minimum:

    model_pk
    generation_pk
    generation_manifest_sha256

It may retain a derived active-record byte hash or equivalent freshness
fingerprint as runtime metadata.

Such a fingerprint is not logical PK identity.

## 11. Required V1 key class

Resident PK Directory V1 must support canonical object_pk lookup when
object_pk is explicitly present in the active immutable generation
descriptor.

The minimum directory key is logically:

    (model_pk, "object_pk", object_pk)

model_pk must participate in lookup scope even when an implementation uses a
per-model directory object.

## 12. Additional key classes

Additional PK classes may be indexed only when they exist explicitly in the
canonical active descriptor evidence.

For example, fragment_pk may be indexed only if a canonical fragment identity
is present in the frozen descriptor schema being consumed.

The directory must not synthesize fragment, route, transition, or other PK
classes from offsets, ordering, names, or physical paths.

Unsupported PK classes fail explicitly.

## 13. Directory value contract

For object_pk, the minimum resident value must resolve the immutable active
mapping needed for direct access:

    model_pk
    generation_pk
    generation_manifest_sha256
    object_pk
    segment_id
    offset
    length
    object_file_sha256

The exact field names used by implementation may follow the frozen descriptor
schema, but the semantic evidence above must be preserved.

## 14. Runtime physical-path metadata

A resident entry may also retain the currently resolved physical segment path
needed for direct byte access.

Physical path is runtime metadata.

Physical path must not participate in:

- object_pk;
- generation_pk;
- generation_manifest_sha256;
- canonical logical directory identity.

## 15. Path independence

Relocating byte-identical valid segment evidence and rebuilding the directory
must preserve:

- model_pk;
- object_pk;
- generation_pk;
- generation_manifest_sha256;
- segment_id;
- offset;
- length;
- object_file_sha256.

Only runtime physical-path metadata may change.

## 16. Duplicate logical PK rejection

Within one active snapshot, the same composite logical key must resolve to
exactly one canonical immutable mapping.

Conflicting duplicate logical PK entries fail snapshot construction.

Duplicate keys must never be resolved by first-wins, last-wins, arbitrary
iteration order, or physical path order.

## 17. Cross-model rejection

A lookup for model A must never resolve an entry derived from model B.

A build request whose requested model_pk differs from active authority or
descriptor evidence fails closed.

## 18. Missing PK behavior

A missing logical PK must return an explicit not-found outcome or raise a
defined directory lookup error.

Missing PK must not:

- fall back to another model;
- fall back to another generation;
- scan historical generations;
- choose a nearest key;
- infer a physical location.

## 19. Unsupported PK behavior

A request for an unsupported PK class must fail explicitly.

It must not reinterpret the supplied value as object_pk or another supported
class.

## 20. Generation freshness

Every resident lookup result is generation-bound.

A directory snapshot for generation A must not be treated as valid after
authority changes to generation B.

Generation mismatch is stale-directory state and must fail or force rebuild
before serving B as current.

## 21. Activation-triggered refresh

After successful activation A -> B, the directory for A is stale.

Before serving current-generation lookups for B, a complete B snapshot must
be built from the newly active authority and physically validated B evidence.

No lookup may silently mix A and B.

## 22. Rollback-triggered refresh

After successful rollback B -> A, the directory for B is stale.

Before serving current-generation lookups for A, a complete A snapshot must
be rebuilt or republished from currently valid A evidence.

Rollback does not restore an old resident snapshot merely because the logical
generation identity matches.

Current physical evidence must be revalidated.

## 23. Same-generation refresh

An authority-preserving same-generation activation or rollback does not
permit physical validation to be skipped.

A resident snapshot may be retained only when its current physical evidence
and authority binding remain valid under the implementation's freshness
contract.

## 24. Startup behavior

Resident directory state is rebuildable derived state.

At process startup, the implementation must reconstruct the current snapshot
from current authoritative evidence before serving directory lookups.

No persisted resident cache is required by V1.

## 25. Rebuild behavior

Snapshot construction must complete fully before the new snapshot becomes
visible to lookups.

Before publication:

    old valid snapshot remains visible
    or
    directory remains unavailable

After publication:

    new complete snapshot is visible

A partially constructed snapshot must never be externally visible.

## 26. Publication boundary

Within the V1 single-process scope, publication should use one resident
snapshot replacement boundary.

The implementation must not mutate a published snapshot entry-by-entry while
lookups can observe it.

Immutable snapshot replacement is preferred.

## 27. Failure preservation

Any failure while validating or constructing a replacement snapshot must
leave the previously published valid snapshot unchanged.

If no valid snapshot existed before the failed build, the directory remains
unavailable.

## 28. Stale-entry rejection

A lookup implementation must have a defined way to reject a snapshot whose
generation binding is not the generation expected by the caller/runtime.

V1 must not require reading or parsing the active JSON record on every
successful lookup.

Freshness belongs to snapshot publication and generation binding, not to a
filesystem read on each hot-path lookup.

## 29. Direct lookup correctness

For a successful object_pk lookup, returned mapping evidence must exactly
equal the canonical active descriptor evidence for that object.

The directory must not recompute offset or length from neighboring entries.

The directory must not derive object bounds from physical file size.

## 30. Lookup complexity target

The intended resident lookup is direct keyed access.

The implementation target is average O(1) logical-PK lookup.

This is a design target, not a performance claim.

No production complexity or latency claim is accepted until benchmarked.

## 31. JSON hot-path exclusion

JSON parsing, manifest scanning, and filesystem discovery must not be required
for an already-resident successful logical-PK lookup.

JSON and canonical manifest processing remain allowed during:

- startup;
- snapshot build;
- activation refresh;
- rollback refresh;
- validation.

## 32. Linear-scan exclusion

A resident successful lookup must not perform a linear scan over all active
descriptor objects.

Any linear scan required to construct the snapshot occurs outside the lookup
hot path.

## 33. Physical byte access boundary

Resident PK Directory V1 resolves location evidence.

It does not itself define a new Segment Reader.

It does not claim that resolving:

    segment path + offset + length

has read, mapped, copied, or computed the referenced bytes.

Phase 6B.10 remains responsible for Segment Reader validation.

## 34. Memory ownership

The resident snapshot is process-local derived memory.

Its entries should be immutable after publication.

The protocol does not prescribe Python dict, C++ hash map, perfect hash,
flat map, trie, or another concrete container.

Container choice must remain benchmarkable.

## 35. Storage neutrality

Resident PK Directory V1 does not select:

- SQLite;
- MAFDB;
- mmap;
- LMDB;
- RocksDB;
- a production catalog database;
- a persisted directory format.

Storage-engine selection requires separate evidence.

## 36. No source GGUF dependency

Directory construction and lookup must not require, open, read, hash, or stat
a source GGUF.

The directory operates on active MAF generation evidence only.

## 37. Generation retention boundary

The directory must not delete, retire, rewrite, or garbage-collect any
generation, manifest, segment, or object.

Generation retention remains separate from lookup.

## 38. Historical-provenance boundary

Directory membership proves current derived lookup state only.

It does not prove historical activation authority.

It must not create or infer an append-only activation-history journal.

## 39. Compute boundary

Resident PK Directory V1 does not:

- perform inference;
- execute tensor math;
- enable MAF-native compute;
- choose GPU residency;
- load model tensors into a compute backend;
- replace llama.cpp;
- implement Segment Reader V1.

## 40. Concurrency boundary

V1 targets one authority-coordinated process.

A future implementation may use a lock or equivalent publication guard.

The protocol does not claim hostile multiwriter or distributed coherence.

## 41. Crash-consistency boundary

The resident directory is rebuildable derived memory.

V1 makes no persistence guarantee for resident snapshot state across process
or device failure.

After restart, authoritative active and generation evidence must be used to
rebuild.

## 42. Error model

The future implementation must define explicit directory errors for at least:

- invalid authority;
- active-generation mismatch;
- invalid physical evidence;
- duplicate logical PK;
- unsupported PK class;
- missing PK;
- stale snapshot;
- cross-model request.

These may share a common resident-directory exception base.

## 43. Future implementation

The future implementation target is:

    experiments/model_fractal/
    maf_resident_pk_directory_v1.py

It must be created, statically audited, and frozen before validation.

## 44. Future validation

Future validation runner:

    experiments/model_fractal/
    maf_resident_pk_directory_validation_v1.py

Future raw result:

    experiments/model_fractal/
    maf_resident_pk_directory_validation_v1.json

Future runtime:

    results/runtime/
    maf_resident_pk_directory_validation_v1

The validation runner must be preregistered and frozen before execution.

## 45. Required future positive controls

Validation must include at minimum:

- build from exact active generation A;
- every canonical object_pk in A indexed exactly once;
- exact object mapping equality with descriptor evidence;
- direct successful object_pk lookup;
- model-scoped lookup;
- generation-bound snapshot metadata;
- path relocation with logical identity unchanged;
- rebuilt relocated snapshot returns new runtime path only;
- activation A -> B makes A snapshot stale;
- complete B refresh before B lookup is accepted;
- rollback B -> A makes B snapshot stale;
- A rebuilt from current physical evidence;
- same-generation refresh preserves logical mappings;
- published snapshot remains immutable;
- failed replacement build preserves prior snapshot;
- successful lookup performs no JSON parse;
- successful lookup performs no manifest linear scan;
- source GGUF not required.

## 46. Required future negative controls

Validation must include at minimum:

- missing active authority;
- malformed active authority;
- noncanonical active authority;
- cross-model active authority;
- manifest hash mismatch;
- active generation mismatch;
- malformed active candidate manifest;
- missing segment mapping;
- extra segment mapping;
- missing physical segment;
- nonregular physical segment;
- segment length mismatch;
- segment SHA256 mismatch;
- object byte-range SHA256 mismatch;
- duplicate object_pk conflict;
- missing object_pk lookup;
- unsupported PK class;
- cross-model lookup;
- stale snapshot after activation;
- stale snapshot after rollback;
- failed refresh preserving prior snapshot;
- attempted synthetic PK creation rejected.

## 47. Benchmark requirements

Before any production performance claim, benchmarking must measure at least:

- lookup latency;
- lookup latency distribution;
- directory build time;
- rebuild time;
- resident memory usage;
- scaling with entry count;
- comparison against linear descriptor lookup.

Benchmark sizes should span enough entries to expose scaling behavior.

Existing historical MAF indexed-lookup measurements may guide expectations
but do not validate this implementation.

## 48. Static-policy requirements

Validation must prove:

- Rollback V1 unchanged;
- Activation V1 unchanged;
- Activation V1.1 unchanged;
- Generation Engine V1 unchanged;
- frozen Phase 6B.7 evidence unchanged;
- frozen Phase 6B.8 evidence unchanged;
- directory remains derived rather than authoritative;
- no second active-authority schema;
- no logical PK synthesis;
- no generation deletion;
- no source GGUF dependency;
- no storage-engine selection;
- no inference;
- no MAF-native compute;
- no Segment Reader implementation;
- no Phase 6C implementation.

## 49. Completion rule

Freezing this protocol does not complete Phase 6B.9.

Phase 6B.9 completes only after its frozen protocol, implementation, validation
runner, exactly-once validation evidence, frozen interpretation, performance
evidence required by the accepted scope, and completion checkpoint satisfy the
preregistered contracts.

## 50. Core invariant

    stable logical PK
        +
    exact current active generation
        +
    exact immutable descriptor mapping
        +
    current physical validation
        ->
    immutable resident snapshot
        ->
    direct generation-bound lookup

with no logical identity rewrite, no JSON or manifest scan on the resident
lookup hot path, no source GGUF dependency, no storage-engine selection, and
no inference or MAF-native compute claim.
