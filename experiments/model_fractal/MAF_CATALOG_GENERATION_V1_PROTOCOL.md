# OpenMind MAF Catalog Generation V1 Protocol

Status: Frozen Phase 6B research protocol.

Schema:

    openmind.maf_catalog_generation.v1


## 1. Purpose

This protocol defines the first authoritative storage boundary for
Phase 6B — MAF Model Catalog and Segment Store.

It separates permanent logical identity from temporary physical
placement.

Its primary relation is:

    logical PK
        ->
    active generation
        ->
    immutable segment / offset / length

This protocol defines authority and lifecycle semantics.

It does not select a storage engine or hot-path index implementation.


## 2. Governing protocols

This protocol is subordinate to:

- MAF Identity V1;
- MAF Object V1;
- MAF Segment Builder V1;
- MAF Dense Compute View Boundary V1.

It must not redefine logical model, object, or fragment identity.


## 3. Identity separation

Logical identities remain independent of physical placement.

At minimum:

    model_pk
    object_pk
    fragment_pk

must not depend on:

- generation_pk;
- segment identifier;
- segment path;
- segment offset;
- segment length;
- cache tier;
- mapping address;
- device residency.

A repack may change every physical field while preserving logical PKs.


## 4. Generation identity

Physical storage generations require their own identity:

    generation_pk

Generation identity does not replace model_pk or object_pk.

A generation represents one immutable candidate mapping from logical
objects to physical storage records.


## 5. Generation PK namespace

The V1 printable generation namespace is:

    mafgen:v1:<64 lowercase hexadecimal SHA256 characters>

This protocol freezes the namespace and canonical derivation boundary.

The exact canonical descriptor used to derive the digest must be
defined by the Phase 6B generation engine protocol before any engine
is implemented or validated.


## 6. Generation descriptor principle

generation_pk must be deterministic from canonical immutable generation
content.

It must not depend on mutable runtime state such as:

- current/active status;
- wall-clock activation time;
- RAM address;
- mmap address;
- cache state;
- device residency;
- process ID;
- temporary filesystem path.

Independent implementations given identical canonical generation
content must produce identical generation_pk values.


## 7. Candidate generation

A newly constructed generation begins as a candidate.

A candidate generation is not authoritative merely because:

- segment files exist;
- Segment Builder validation passed;
- a placement manifest exists;
- a generation manifest was serialized.

Authority begins only through explicit catalog activation.


## 8. Segment adoption

A catalog generation may adopt only completed immutable segment
artifacts.

Adoption must validate the segment and placement metadata required by
the generation engine protocol.

Catalog adoption must not modify adopted segment bytes.


## 9. Segment identity boundary

Segment paths are physical locations, not logical model/object
identity.

V1 does not require a globally permanent logical segment PK.

A generation manifest must nevertheless identify each adopted segment
unambiguously within that generation and retain sufficient integrity
metadata to detect substitution or corruption.


## 10. Authoritative object placement

For each adopted object, the generation must provide an authoritative
physical placement record containing at minimum:

    object_pk
    segment reference
    offset
    length
    object integrity hash
    payload integrity hash

The direct resolution relation is:

    object_pk
        ->
    segment reference, offset, length

Integrity hashes remain independent from object_pk identity.


## 11. Placement semantics

For a placement:

    offset >= 0
    length > 0

and:

    offset + length

must remain inside the referenced immutable segment.

The selected byte range must correspond exactly to the adopted MAF
object bytes established by prior validation.


## 12. Logical PK authority

The catalog must be keyed by logical PK rather than mutable physical
location.

object_pk is therefore the authoritative object lookup identity.

Tensor name may be retained as metadata or a secondary lookup aid but
must not replace object_pk as the authoritative catalog key.


## 13. Duplicate object PK

Within one generation, one object_pk must resolve to one authoritative
placement.

A candidate containing conflicting placements for the same object_pk
must fail closed.

V1 does not authorize ambiguous multi-placement resolution.


## 14. Model membership

Every object adopted into a model generation must belong to the
intended model_pk according to frozen logical identity evidence.

Mixed-model candidate generations must fail closed unless a future
protocol explicitly defines multi-model catalog semantics.


## 15. Fragment boundary

Phase 6B requires future fragment resolution support.

V1 freezes the authority rule:

    fragment_pk

must remain logical identity independent of generation and placement.

This protocol does not yet require fragment records to be present when
no validated fragment representation exists.


## 16. Route/transition boundary

Route or transition identity remains outside the initial object
placement implementation unless independently defined by its own
logical identity protocol.

Physical catalog work must not invent route identity from storage
placement.


## 17. Generation manifest

Each candidate generation requires an immutable canonical generation
manifest.

The manifest is the persistent control-plane description of that
generation.

It must contain enough information to independently reconstruct and
validate the generation's logical-to-physical mapping.


## 18. Minimum generation manifest content

The future V1 engine manifest must contain at minimum:

- schema;
- generation version;
- generation_pk;
- model_pk;
- segment records;
- object placement records;
- object count;
- generation integrity information.

Exact field encoding and canonical serialization belong to the frozen
engine protocol that follows this authority protocol.


## 19. Canonical serialization

Generation identity must be based on a canonical representation.

Pretty-print formatting, dictionary insertion order, filesystem
enumeration order, and other incidental serialization behavior must
not change generation identity.


## 20. Generation immutability

After generation_pk has been derived, the generation content it names
is immutable.

Changing:

- segment membership;
- object placement;
- offset;
- length;
- integrity hash;
- model membership

requires creation of a new generation and therefore a new
generation_pk where canonical content differs.


## 21. No in-place repacking

Repacking must not mutate an active generation in place.

The required lifecycle is:

    active generation A
        ->
    build candidate generation B
        ->
    independently validate B
        ->
    atomically activate B

Generation A remains an independent immutable generation.


## 22. Catalog authority

The authoritative live catalog must identify which validated
generation is current for a model.

A Segment Builder manifest alone is not the live catalog.

A generation manifest alone is not active merely because it exists.


## 23. Atomic activation

Generation activation must be an atomic authority transition.

Readers must observe either:

    old active generation

or:

    new active generation

and must not observe a partially activated mixture of both.


## 24. Activation precondition

Only a completely validated candidate generation may be activated.

Activation must fail closed if any required generation or adopted
segment validation has failed.


## 25. Rollback

Rollback is an authority switch to a previously retained validated
generation.

Rollback must not:

- alter logical PKs;
- rewrite immutable segments;
- mutate historical generation manifests;
- reconstruct the previous generation from mutable runtime state.

The previous validated generation must remain independently
addressable while rollback is permitted.


## 26. Failed activation

A failed activation must leave the previously active generation
authoritative.

Failure must not produce a mixed generation state.


## 27. Generation retirement

Retirement is distinct from activation.

A generation may cease to be active while remaining retained for
rollback, audit, or provenance.

Physical deletion policy is not defined by this protocol.


## 28. Persistent control plane

The catalog authority must survive process restart.

The exact persistence mechanism remains experimental.

Candidate implementations include:

- compiled binary control records;
- SQLite control plane;
- purpose-built MAFDB;
- another measured embedded engine.

No implementation is selected by this protocol.


## 29. Resident directory boundary

Phase 6B requires a compact resident object/fragment directory.

This protocol defines its authority source but not its representation.

A resident directory is a derived runtime acceleration structure built
from the active validated generation.


## 30. Hot-path boundary

The inference hot path must not require JSON parsing.

JSON may be used as research evidence or offline control-plane
serialization where independently validated.

The final resident lookup representation must be benchmarked
separately.


## 31. Old experimental index boundary

Earlier name-keyed MAF index experiments are not authoritative catalog
records.

Their useful result is limited to demonstrating that direct indexed
lookup can outperform linear traversal.

They do not define:

- logical PK authority;
- generation identity;
- segment adoption;
- activation;
- rollback;
- persistent catalog authority.

Their lookup strategy may be reused only after adaptation to this
protocol.


## 32. Direct lookup target

The eventual resident lookup target is conceptually:

    object_pk
        ->
    generation-local segment handle
        ->
    offset
        ->
    length

Lookup implementation may differ as long as it preserves this
authority relation and passes independent validation.


## 33. Reader boundary

This protocol does not implement the production Segment Reader.

A later reader may perform bounded access using the resolved:

    segment, offset, length

but it must consume catalog-authoritative placement rather than invent
placement independently.


## 34. Runtime residency boundary

Catalog placement does not imply runtime residency.

This protocol does not assign:

- COLD_DISK;
- MAPPED;
- HOT_MAF;
- HOT_DENSE;
- VULKAN_MAF.

Residency belongs to Phase 6C.


## 35. Dense materialization boundary

Catalog activation does not materialize dense compute views.

Dense materialization remains governed by the frozen dense-view
boundary and later Phase 6C/6E protocols.


## 36. MAF-native compute boundary

Catalog validity does not establish direct MAF-native compute.

MAF-native compute remains:

    disabled_unvalidated


## 37. Source GGUF independence

Once adopted segments and generation metadata have been independently
validated, normal catalog lookup must not require the source GGUF merely
to resolve physical placement.

Any stronger claim about complete source-model independence requires
separate validation.


## 38. Integrity failure

If an adopted segment or placement fails required integrity validation,
the candidate generation must fail closed.

An invalid candidate must not become authoritative.


## 39. Missing object

Lookup of an object_pk absent from the active generation must fail
explicitly.

V1 must not silently substitute:

- another object;
- name-based nearest match;
- another generation;
- source GGUF location.


## 40. Unknown generation

A generation_pk that is absent or not validated must not become active
through implicit discovery.


## 41. Storage-engine neutrality

This protocol deliberately does not choose between:

1. compiled binary/RAM index plus external segments;
2. SQLite control plane plus external segments;
3. purpose-built MAFDB;
4. another measured embedded engine.

Architecture promotion requires benchmark evidence.


## 42. No custom database presumption

A purpose-built MAFDB must earn promotion through measurable
MAF-specific advantage.

Novelty alone is insufficient justification.


## 43. Initial V1 validation scope

The first generation-engine validation should use the already frozen
three-object Segment Builder V1 evidence.

It should demonstrate at minimum:

- deterministic generation_pk;
- exact model_pk preservation;
- exact object_pk preservation;
- exact adopted segment hash;
- exact placement offsets and lengths;
- one authoritative placement per object_pk;
- failed duplicate/conflicting placement control;
- failed mixed-model control;
- failed corrupted segment or manifest control;
- candidate state distinct from active state;
- atomic activation;
- rollback to prior validated generation;
- no logical PK changes across activation/rollback;
- no source GGUF requirement for catalog lookup where claimed.


## 44. Engine ordering

Phase 6B development order begins:

    authority protocol
        ->
    generation descriptor / manifest protocol
        ->
    catalog-generation engine
        ->
    preregistered validation
        ->
    resident directory / hot-path representation
        ->
    Segment Reader validation

Storage-engine comparisons occur only after correctness is frozen.


## 45. Nonclaims

This protocol does not establish:

- a catalog engine;
- generation_pk implementation;
- activated generation;
- rollback implementation;
- SQLite suitability;
- MAFDB suitability;
- binary-index superiority;
- production persistence;
- hot-path performance;
- Segment Reader performance;
- mmap performance;
- lower RAM;
- lower latency;
- inference correctness;
- selective access;
- dense materialization;
- MAF-native inference;
- Vulkan execution.


## 46. V1 invariant summary

    logical PK identity is permanent across physical repacking

    generation_pk identifies immutable physical-generation content

    physical placement is authoritative only through an active
    validated generation

    object_pk -> segment / offset / length is the catalog resolution
    relation

    integrity hashes remain separate from logical identity

    Segment Builder output is candidate physical evidence, not live
    catalog authority

    generation activation is atomic

    rollback switches authority; it does not rewrite immutable state

    resident indexes are derived acceleration structures

    JSON is not required on the inference hot path

    runtime residency remains separate

    MAF-native compute remains disabled_unvalidated
