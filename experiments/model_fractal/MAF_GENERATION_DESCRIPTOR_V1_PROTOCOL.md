# OpenMind MAF Generation Descriptor V1 Protocol

Status: Frozen Phase 6B research protocol.

Descriptor schema:

    openmind.maf_generation_descriptor.v1

Manifest schema:

    openmind.maf_generation_manifest.v1

Generation namespace:

    mafgen:v1:


## 1. Purpose

This protocol freezes the canonical immutable descriptor whose digest
defines generation_pk.

It also defines the relationship between that descriptor and a
persistent generation manifest.

It does not implement generation construction, activation, rollback,
or catalog persistence.


## 2. Governing rule

generation_pk identifies immutable physical-generation content.

It must remain independent of logical model/object identity derivation
and independent of mutable runtime state.


## 3. Derivation

The V1 generation PK is:

    generation_pk =
        "mafgen:v1:" + sha256(canonical_descriptor_bytes).hexdigest()

generation_pk is not itself part of the descriptor being hashed.

This avoids circular identity construction.


## 4. Canonical descriptor encoding

The descriptor must be encoded as UTF-8 canonical JSON using:

    sort_keys = true
    separators = (",", ":")
    ensure_ascii = false

No trailing newline is part of canonical descriptor bytes.


## 5. Top-level descriptor fields

The V1 descriptor contains exactly:

    schema
    descriptor_version
    model_pk
    segments
    objects

Where:

    schema = "openmind.maf_generation_descriptor.v1"

    descriptor_version = "maf_generation_descriptor_v1"


## 6. Excluded top-level fields

The canonical descriptor must not contain:

- generation_pk;
- active status;
- activation timestamp;
- creation timestamp;
- wall-clock time;
- source GGUF path;
- catalog file path;
- process identifier;
- host identifier;
- cache state;
- runtime residency;
- mmap address;
- RAM pointer;
- device pointer;
- Vulkan handle.

These are not immutable generation identity content.


## 7. Model identity

model_pk is included exactly as established by MAF Identity V1.

Generation construction must not regenerate or reinterpret model_pk.


## 8. Segment records

Each descriptor segment record contains exactly:

    segment_id
    segment_length
    segment_sha256

segment_id is a generation-local stable identifier.

It is not model_pk, object_pk, fragment_pk, or generation_pk.


## 9. Segment ID format

For V1, segment_id is:

    segment:<zero-padded ordinal>

with decimal ordinal width 8.

Examples:

    segment:00000000
    segment:00000001

Segment IDs are assigned only after deterministic segment ordering has
been established.


## 10. Deterministic segment ordering

Canonical segment order is ascending by this tuple:

    (
        segment_sha256,
        segment_length
    )

If two candidate segment records have identical SHA256 and identical
length, V1 treats them as the same immutable segment content.

Duplicate identical segment content must not appear twice in one
canonical descriptor.


## 11. Segment path exclusion

Filesystem path is not generation identity.

Therefore segment paths are excluded from canonical descriptor bytes.

A persistent manifest may contain path-binding information outside the
hashed descriptor only if the later engine protocol explicitly defines
that binding and proves it does not redefine generation identity.


## 12. Segment integrity

segment_sha256 must be lowercase 64-character SHA256 text.

segment_length must be a positive integer.

The digest is an integrity value for immutable segment bytes.


## 13. Object placement records

Each object record contains exactly:

    object_pk
    segment_id
    offset
    length
    object_file_sha256
    payload_sha256


## 14. Authoritative lookup relation

The object records encode:

    object_pk
        ->
    segment_id
        ->
    offset
        ->
    length

This is physical placement authority within the generation.


## 15. Object ordering

Canonical object order is ascending lexicographic object_pk.

Caller order, source tensor order, Segment Builder invocation order,
and filesystem enumeration order must not affect generation identity.


## 16. Object uniqueness

object_pk must be unique in the canonical descriptor.

Two records with the same object_pk are invalid even if their physical
placements happen to be identical.


## 17. Placement validation

For every object record:

    offset >= 0
    length > 0

and:

    offset + length <= referenced segment_length

The referenced segment_id must exist exactly once.


## 18. Object-file integrity

object_file_sha256 is the SHA256 of the complete standalone MAF Object
V1 byte representation represented by that segment range.

It remains independent of object_pk identity.


## 19. Payload integrity

payload_sha256 is the independently validated numerical payload digest
already established by MAF Object V1.

Generation construction must not redefine it.


## 20. Exact range requirement

The segment byte range selected by:

    segment_id
    offset
    length

must correspond exactly to the complete adopted MAF Object V1 bytes.

A generation must fail validation if the range hash differs from
object_file_sha256.


## 21. Placement affects generation identity

Physical placement is generation content.

Therefore changing any of:

- adopted segment content;
- segment membership;
- object segment_id;
- object offset;
- object length;
- object-file integrity hash;
- payload integrity hash

changes canonical descriptor bytes and therefore changes generation_pk.


## 22. Physical path does not affect generation identity

Moving an unchanged immutable segment to another filesystem path must
not change generation_pk.

The same canonical generation content stored at a different path
retains the same generation identity.


## 23. Activation does not affect generation identity

Changing a generation between:

    candidate
    active
    inactive
    rollback target
    retired

must not change generation_pk.

Lifecycle state is catalog authority state, not immutable generation
content.


## 24. Residency does not affect generation identity

Changes to:

- COLD_DISK;
- MAPPED;
- HOT_MAF;
- HOT_DENSE;
- VULKAN_MAF

must not change descriptor bytes or generation_pk.


## 25. Canonical reconstruction

Given a valid generation manifest, an independent implementation must
be able to reconstruct the exact canonical descriptor bytes without
consulting mutable runtime state.


## 26. Generation manifest

A persistent V1 generation manifest contains:

    schema
    manifest_version
    generation_pk
    descriptor

Where:

    schema = "openmind.maf_generation_manifest.v1"

    manifest_version = "maf_generation_manifest_v1"

and descriptor is the exact logical descriptor represented by this
protocol.


## 27. Manifest generation PK check

For every manifest:

    manifest.generation_pk

must equal:

    "mafgen:v1:" +
    sha256(canonical_json(manifest.descriptor)).hexdigest()

A mismatch fails closed.


## 28. Manifest canonical form

The manifest itself may also be canonically serialized for persistence
and integrity validation.

However generation_pk derives only from the canonical descriptor, not
from the outer manifest serialization.


## 29. Why the outer manifest is excluded

The outer manifest contains generation_pk.

Including the outer manifest in its own generation identity digest
would create circular derivation.

Therefore descriptor identity and manifest serialization are separate
layers.


## 30. Segment Builder manifest relationship

MAF Segment Builder V1 manifests are candidate build evidence.

Generation construction may consume validated placement information
from them.

It must transform that evidence into this descriptor contract rather
than treating the Segment Builder manifest as automatically
authoritative.


## 31. Multiple segments

The descriptor supports one or more immutable segments.

Object records may resolve across different segment_id values.

The first validation may use one segment without narrowing the general
V1 contract.


## 32. Empty generations

V1 does not permit an empty generation.

At minimum:

    one segment
    one object placement

must exist.


## 33. Mixed-model prohibition

All object placements in one V1 generation must belong to the declared
model_pk.

Mixed-model generation construction fails closed.


## 34. Fragment boundary

Fragment records are not added to this initial descriptor until a
validated persistent fragment representation exists.

Future descriptor revisions may add canonical fragment mappings.

They must preserve separation between logical fragment_pk and physical
placement.


## 35. Route boundary

Route/transition mappings are not part of this initial descriptor.

Future inclusion requires independently frozen logical route identity.


## 36. No name-keyed authority

Tensor names are intentionally absent from the authoritative descriptor.

Names may exist in debugging or secondary metadata but generation
resolution authority is object_pk based.


## 37. No runtime metadata

The descriptor must not encode:

- access count;
- materialization count;
- reuse interval;
- prefetch state;
- cache admission;
- cache eviction;
- telemetry.

Those values may change without changing generation identity.


## 38. No storage-engine metadata

The descriptor must not depend on:

- SQLite row IDs;
- B-tree page numbers;
- Python dictionary order;
- binary-index slot;
- hash-table capacity;
- MAFDB internal record address.

Storage-engine implementation must not redefine generation identity.


## 39. Determinism gate

Given the same validated physical content and placements,
independent implementations must produce identical:

1. normalized segment records;
2. normalized object records;
3. canonical descriptor object;
4. canonical descriptor bytes;
5. descriptor SHA256;
6. printable generation_pk.


## 40. Required negative controls

The future generation engine validation must fail closed for at least:

- duplicate object_pk;
- missing referenced segment_id;
- out-of-bounds placement;
- zero or negative length;
- invalid segment SHA syntax;
- invalid object-file SHA syntax;
- invalid payload SHA syntax;
- mixed model;
- manifest generation_pk mismatch;
- altered offset after generation_pk derivation;
- altered segment hash after generation_pk derivation.


## 41. Path-independence control

Future validation must prove that changing only segment filesystem
paths does not alter:

- canonical descriptor bytes;
- descriptor SHA256;
- generation_pk.


## 42. Ordering-independence control

Future validation must prove that permuting input segment records or
input object placement records does not alter the normalized canonical
descriptor or generation_pk.


## 43. Placement-sensitivity control

Future validation must prove that changing a valid physical placement
changes generation_pk while leaving object_pk unchanged.


## 44. Integrity separation control

Future validation must demonstrate that logical PK fields are not
derived from mutable offsets or paths.

Integrity hashes remain explicit independent fields.


## 45. Activation boundary

This descriptor protocol does not activate generations.

Atomic activation and rollback consume validated generation manifests
through the later catalog-generation engine.


## 46. Resident-directory boundary

The future resident hot-path directory is derived from an active
validated generation manifest.

Its internal ordering or storage representation must not change
generation_pk.


## 47. Source GGUF boundary

Generation descriptor construction should require only validated MAF
physical evidence.

Source GGUF access is not part of this descriptor protocol.


## 48. Nonclaims

This protocol does not establish:

- generation engine implementation;
- generation validation result;
- real generation_pk values;
- catalog persistence;
- active generation state;
- rollback implementation;
- resident directory;
- Segment Reader;
- SQLite suitability;
- binary-index superiority;
- MAFDB suitability;
- inference performance;
- runtime residency;
- selective access;
- MAF-native computation.


## 49. V1 invariant summary

    generation_pk =
        mafgen:v1:SHA256(canonical immutable descriptor)

    descriptor excludes generation_pk itself

    descriptor is independent of mutable lifecycle/runtime state

    model_pk and object_pk are inherited logical identities

    segment content and object placement define physical-generation
    identity

    segment filesystem paths do not define generation identity

    segment input ordering does not define generation identity

    object input ordering does not define generation identity

    object_pk is the authoritative lookup key

    one object_pk has one placement per generation

    activation/rollback do not alter generation_pk

    storage-engine implementation does not alter generation_pk
