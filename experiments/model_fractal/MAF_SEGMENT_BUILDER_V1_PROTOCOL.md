# MAF Segment Builder V1 Protocol

Status: experimental frozen protocol candidate

Schema:

    openmind.maf_segment_builder.v1

Builder version:

    maf_segment_builder_v1


## 1. Purpose

Segment Builder V1 defines the physical-storage boundary immediately
downstream of Encoder V1.

The compiler pipeline is:

    Scanner -> Classifier -> Planner -> Encoder -> Segment Builder

Encoder V1 produces independently valid persistent MAF Object V1 files.

Segment Builder V1 consumes those completed objects and constructs an
immutable physical segment plus a placement manifest.

Its purpose is physical packing.

It does not redefine logical identity, numerical representation,
runtime residency, inference behavior, or catalog activation.


## 2. Governing contracts

Segment Builder V1 is subordinate to:

- MAF Identity V1;
- MAF Compile Recipe V1;
- MAF Encoder V1;
- MAF Object V1;
- the Phase 6A / Phase 6B roadmap boundary.

Where these contracts distinguish logical identity from physical
placement, Segment Builder V1 must preserve that distinction.


## 3. Logical identity is immutable

Segment Builder V1 must never create, regenerate, reinterpret, or alter:

- model_pk;
- object_pk;
- fragment_pk.

The builder consumes existing logical identifiers.

Physical packing must not affect those identifiers.


## 4. Physical placement is non-identity state

Segment Builder V1 may assign:

- segment-relative object offset;
- segment-relative object length;
- physical segment path supplied by the caller;
- physical ordering within the candidate segment.

These are physical placement attributes.

They must not participate in logical object identity.


## 5. V1 placement policy

The V1 placement policy is:

    sequential_exact_object_pack

Objects are placed in exactly the order supplied by the caller.

No implicit sorting by:

- object_pk;
- tensor name;
- tensor type;
- size;
- semantic class;
- structural class;
- access frequency;
- source GGUF offset;
- hash

is permitted.

This makes physical ordering explicit and independently testable.


## 6. V1 segment representation

A V1 segment is the exact bytewise concatenation of completed
standalone MAF Object V1 files.

Conceptually:

    segment =
        object_0_bytes
        || object_1_bytes
        || ...
        || object_n_bytes

There is no V1 segment-internal transformation of object bytes.

There is no V1 segment header inserted between objects.

Physical lookup metadata is carried separately by the placement
manifest.


## 7. Exact object preservation

Every object inserted into a segment must preserve its complete
standalone MAF Object V1 byte sequence exactly.

Segment Builder V1 must not:

- rewrite an object header;
- rewrite object metadata;
- rewrite object payload bytes;
- normalize JSON;
- alter padding internal to an object;
- requantize;
- dequantize;
- transpose;
- reorder tensor payload bytes;
- compress;
- encrypt;
- deduplicate;
- fragment.

For every placed object:

    SHA256(segment[offset : offset + length])
        ==
    SHA256(original standalone MAF object)


## 8. Required input record

Each requested placement must provide at minimum:

- model_pk;
- object_pk;
- object_path.

The object path is execution information only.

It must not become part of logical identity.


## 9. Input object requirements

Before placement, every input object must:

- exist;
- be a regular file;
- be non-empty;
- independently validate as MAF Object V1;
- contain a valid complete object;
- have no trailing bytes beyond its defined MAF Object V1 extent;
- agree with any supplied expected integrity metadata.

Malformed objects must fail closed.


## 10. Model consistency

All objects in one V1 segment-build request must belong to the same
model_pk supplied by the caller.

Segment Builder V1 does not infer model identity from physical paths.

Mixed-model segment construction is prohibited in V1.


## 11. Object PK preservation

The object_pk supplied to Segment Builder V1 must be treated as an
existing logical identifier.

The builder must not derive a replacement object_pk from:

- object bytes;
- object SHA256;
- segment offset;
- segment path;
- source path;
- physical order.

Placement records preserve the supplied object_pk verbatim.


## 12. Duplicate logical objects

A V1 build request must not contain the same object_pk more than once.

Duplicate object_pk entries fail closed.

This rule prevents ambiguous physical resolution.

It is not a deduplication feature.


## 13. Fragmentation

Operational fragmentation remains disabled.

V1:

    fragmentation_policy = none

Segment Builder V1 must not create:

- fragment PKs;
- fragment boundaries;
- fragment placement records;
- shared fragments;
- sub-object physical records.

Fragment support requires a separately frozen protocol.


## 14. Deduplication

Deduplication remains unresolved.

V1 performs no payload or object deduplication.

Two distinct logical objects with identical bytes remain two distinct
placements when both are supplied.

No content-address substitution is permitted.


## 15. Structural optimization

Structural optimization remains unresolved.

V1 does not perform:

- fractal packing;
- sparse packing;
- residual encoding;
- shared-block extraction;
- reversible transforms;
- semantic coalescing.

Those require independent validation.


## 16. Alignment

V1 adds no inter-object alignment padding.

Therefore:

    first_offset = 0

and:

    next_offset =
        previous_offset + previous_length

Any future alignment policy must be independently specified and
validated.

Alignment must remain physical placement state.


## 17. Placement manifest

Each successful build produces a placement manifest.

Schema:

    openmind.maf_segment_manifest.v1

The manifest must contain at minimum:

- schema;
- builder_version;
- placement_policy;
- model_pk;
- object_count;
- segment_length;
- segment_sha256;
- objects.

Each object placement record must contain:

- ordinal;
- object_pk;
- offset;
- length;
- object_file_sha256;
- payload_sha256.

The manifest may contain additional integrity or provenance fields that
do not alter logical identity.


## 18. Manifest ordering

Manifest object records must appear in the exact physical order used
for segment construction.

For each record:

    ordinal == physical placement index

Offsets must be strictly monotonic for non-empty objects.


## 19. Placement arithmetic

For object zero:

    offset = 0

For every later object:

    offset_i =
        offset_(i-1) + length_(i-1)

The final condition must be:

    segment_length =
        final_offset + final_length

No overlap is permitted.

No gaps are permitted in V1.


## 20. Integrity hashes

Integrity hashes are separate from logical identity.

Segment Builder V1 must calculate:

- SHA256 of each complete standalone object byte sequence while copying;
- SHA256 of the completed segment byte sequence;
- the payload SHA256 already established by MAF Object V1 validation.

Object-file SHA256 and segment SHA256 must never replace object_pk.


## 21. Payload integrity

The payload SHA256 recorded for each object must agree with the
validated MAF Object V1 payload digest.

Segment Builder V1 does not redefine payload integrity.

The segment operation must not change payload bytes.


## 22. Streaming requirement

Object copying must use bounded streaming.

Whole-object temporary allocations are prohibited when bounded
streaming is sufficient.

V1 must not require loading an entire object or segment into a Python
bytes object before writing.


## 23. Source-model isolation

Segment Builder V1 operates only on completed MAF Object V1 files.

It must not reopen or require:

- the source GGUF;
- source tensor payload ranges;
- source tensor offsets;
- the original model file.

The Encoder boundary has already completed source-model conversion.


## 24. Independent object validation

Before physical packing, each source object must be independently
validated through the existing MAF Object V1 inspection contract or
an equivalently strict implementation.

This validation may reread the completed MAF object.

It must not reread the source GGUF.


## 25. Candidate segment lifecycle

A build must use a sibling partial path.

Conceptually:

    target.segment.partial
        ->
    validated immutable candidate segment
        ->
    target.segment

The final segment must not become visible as completed until the build
has succeeded.


## 26. Atomic activation at file level

Segment Builder V1 may atomically replace its own completed partial
file with the requested final segment path.

This is file-level completion only.

It is not catalog-generation activation.


## 27. Existing final targets

V1 must not silently overwrite an existing completed segment.

If the requested final segment path already exists, fail closed unless
a future protocol explicitly defines replacement semantics.


## 28. Partial targets

A preexisting partial target is an error in V1.

The builder must not silently adopt or append to an unknown partial
segment.


## 29. Failure cleanup

On build failure:

- no completed final segment may be activated;
- builder-created partial segment state must be removed where safe;
- the failure must not alter input MAF objects;
- no catalog activation may occur.

Input objects are immutable sources to the builder.


## 30. Segment immutability

After successful completion, a V1 segment is immutable.

Repacking requires creation of a new physical segment artifact.

Existing segment bytes must not be modified in place.


## 31. Generation identity

MAF Identity V1 requires physical storage generations to have their
own generation identity.

Segment Builder V1 does not define generation_pk derivation.

It must not synthesize a generation_pk.

Generation identity and generation manifests belong to the Phase 6B
catalog/storage protocol.


## 32. Catalog activation

Segment Builder V1 does not:

- create the authoritative model catalog;
- mutate the authoritative PK directory;
- activate a storage generation;
- retire a storage generation;
- perform rollback;
- decide which generation is current.

It produces physical artifacts that a later catalog layer may adopt.


## 33. Segment identifier

V1 does not define a permanent logical segment identifier.

A segment path is a physical artifact location.

Any future segment ID or generation PK must remain distinct from
model_pk, object_pk, and fragment_pk.


## 34. Runtime residency

Runtime residency remains unresolved.

Segment Builder V1 must not assign:

- COLD_DISK;
- MAPPED;
- HOT_MAF;
- HOT_DENSE;
- VULKAN_MAF;
- cache priority;
- pin state;
- prefetch state;
- device residency.

Those belong to Phase 6C.


## 35. Locality optimization

V1 does not infer or optimize locality.

Caller order is preserved exactly.

The builder does not use:

- transition frequency;
- route frequency;
- reuse counts;
- runtime heat;
- cache behavior;
- tensor adjacency heuristics

to reorder objects.

Path-aware repacking belongs to Phase 6D.


## 36. Dense materialization

Segment Builder V1 does not materialize dense compute tensors.

The persistent representation remains MAF.

Dense materialization remains an optional later compute/runtime view.


## 37. MAF-native compute

V1 does not perform numerical inference or MAF-native kernels.

Successful segment construction establishes no claim about direct
computation from segment bytes.


## 38. Segment Reader boundary

Segment Builder V1 only defines construction and physical placement.

It does not define a production inference-hot-path Segment Reader.

Direct bounded `(segment, offset, length)` object access belongs to the
Phase 6B storage/catalog implementation and its independent validation.


## 39. Manifest authority

The V1 placement manifest is build output and validation evidence.

It is not automatically the authoritative live catalog.

A later catalog layer must explicitly adopt a candidate segment and its
placements.


## 40. Determinism

Given:

- identical validated input object bytes;
- identical object_pk values;
- identical model_pk;
- identical caller ordering;
- identical V1 placement policy;

independent implementations must produce identical segment bytes,
placement offsets, lengths, object-file hashes, and segment SHA256.

Filesystem path spelling is not part of this deterministic byte result.


## 41. Validation requirements

Before Segment Builder V1 is considered validated, a preregistered
validation must prove at minimum:

- existing model_pk is preserved;
- existing object_pk values are preserved;
- no identity is regenerated;
- duplicate object_pk fails closed;
- malformed input object fails closed;
- mixed-model input fails closed;
- completed MAF objects are independently validated;
- source GGUF is not required;
- caller order is preserved;
- first offset is zero;
- placements are contiguous;
- placements do not overlap;
- no V1 alignment gaps are inserted;
- each placed byte range exactly matches its standalone object;
- each object-file SHA256 matches;
- each payload SHA256 matches;
- completed segment SHA256 matches an independent rehash;
- segment length arithmetic is exact;
- bounded streaming is used;
- no whole-object temporary allocation is required;
- no transform occurs;
- no compression occurs;
- no deduplication occurs;
- no fragments are generated;
- no generation_pk is generated;
- no catalog generation is activated;
- no runtime residency is assigned;
- no locality optimization occurs;
- failure does not activate a completed final segment;
- successful segment remains usable without source GGUF access.


## 42. Initial validation scope

Initial validation should use already-created validated MAF Object V1
artifacts rather than re-encoding source tensors.

The exact input objects, order, expected model_pk, expected object_pk
values, expected object-file hashes, and expected total byte count must
be preregistered before execution.

A small multi-object subset is sufficient for the first validation if
it includes materially different object sizes.


## 43. Relationship to Encoder V1

Encoder V1 ends when an individual MAF Object V1 has been successfully
created and independently reopened.

Segment Builder V1 begins from those completed object artifacts.

The boundary is therefore:

    source GGUF
        ->
    Encoder
        ->
    standalone immutable MAF Object V1
        ->
    Segment Builder
        ->
    immutable candidate segment + placement manifest

Segment Builder does not reopen the source-model conversion boundary.


## 44. Relationship to Phase 6B

Segment Builder V1 supplies the minimum physical artifact required by
Phase 6B.

Phase 6B still must define and validate:

- authoritative model catalog;
- compact resident object/fragment directory;
- direct PK -> segment/offset/length resolution;
- generation identity;
- generation manifests;
- atomic generation activation;
- rollback;
- catalog persistence;
- inference-hot-path lookup representation.

Those are not established by this protocol.


## 45. Non-claims

Segment Builder V1 does not establish:

- compression;
- storage reduction;
- deduplication;
- operational fragmentation;
- selective tensor access;
- partial reconstruction;
- sparse execution;
- segment locality improvement;
- cache efficiency;
- reduced RAM usage;
- reduced inference payload traffic;
- generation activation;
- catalog performance;
- mmap performance;
- direct MAF-native inference;
- numerical acceleration;
- Vulkan execution;
- model replacement.


## 46. V1 invariant summary

Segment Builder V1 is valid only if all of the following remain true:

    logical identity is unchanged

    standalone MAF object bytes are unchanged

    physical placement is explicit and non-identity

    object order equals caller order

    offsets are contiguous and deterministic

    object and segment integrity are independently verifiable

    source GGUF access is unnecessary

    construction is bounded-streaming

    final segment completion is fail-closed

    catalog generation activation is not performed

    runtime residency is not assigned
