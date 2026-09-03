# OpenMind MAF Identity v1 Protocol

Status: experimental protocol.

Schema family:

`openmind.maf_identity.v1`

## 1. Purpose

MAF Identity v1 defines stable logical primary keys for:

- model
- MAF object
- future MAF fragment

The protocol separates permanent logical identity from:

- payload integrity
- physical storage location
- segment generation
- cache residency
- device placement

Core rule:

    identity describes what an object is,
    never where the object currently lives

A logical primary key must therefore remain unchanged when an
object is repacked, relocated, mapped, cached, or promoted to a
different physical storage tier.

## 2. Identity versus integrity

Logical primary keys and SHA256 payload hashes serve different
purposes.

Logical primary key:

- answers which logical model/object/fragment this is
- remains stable across physical relocation
- may remain stable across regenerated physical containers
- must not encode file offsets or storage paths

Integrity hash:

- verifies exact bytes
- may change if the canonical representation changes
- must not be treated as the permanent logical primary key

Therefore:

    payload_sha256 != object_pk

and:

    object_file_sha256 != object_pk

unless a future protocol explicitly proves that content-addressed
identity is the intended semantic identity.

MAF Identity v1 does not make that assumption.

## 3. Canonical descriptor encoding

All deterministic identifiers derive from a canonical identity
descriptor.

Descriptor encoding:

- UTF-8
- canonical JSON
- sorted keys
- compact separators
- no insignificant whitespace

Canonicalization rules must be identical across implementations.

The identifier digest is:

    SHA256(canonical_descriptor_bytes)

The printable primary key is:

    <namespace>:<64 lowercase hexadecimal SHA256 characters>

The namespace is part of the identifier string but is not included
inside the SHA256 digest unless explicitly represented in the
descriptor itself.

## 4. Model primary key

Namespace:

    mafmodel:v1

Descriptor schema:

    openmind.maf_model_identity.v1

Required fields:

- schema
- architecture
- model_family
- model_variant
- tensor_count

Optional identity-defining fields may include:

- parameterization variant
- quantization family
- vocabulary identity
- canonical model lineage

Physical source filename must not define model identity.

Physical GGUF byte offsets must not define model identity.

Source-file SHA256 may be recorded as provenance/integrity, but is
not automatically the logical model PK.

Initial Qwen research may use a deterministic descriptor derived
from already frozen canonical metadata, provided the descriptor is
preregistered before PK generation.

## 5. Object primary key

Namespace:

    mafobj:v1

Descriptor schema:

    openmind.maf_object_identity.v1

Required fields:

- schema
- model_pk
- tensor_name
- tensor_type
- dims
- encoding

For MAF Object v1:

    encoding = gguf_payload_exact

The object PK must not include:

- source file offset
- source data offset
- MAF object filename
- MAF object byte offset
- segment filename
- segment offset
- cache tier
- device residency
- physical generation
- object file SHA256

Payload SHA256 is stored independently for integrity.

The same logical tensor represented by the same identity descriptor
must resolve to the same object PK even after physical repacking.

## 6. Fragment primary key

Namespace:

    maffrag:v1

Descriptor schema:

    openmind.maf_fragment_identity.v1

Fragment identity is specified now but operational generation is
deferred until fragmentation is formally introduced.

Required fields when fragments become active:

- schema
- object_pk
- fragment_scheme
- logical_fragment_index
- logical_range

The fragment PK must identify the logical fragment, not its segment
or byte location.

Physical fragmentation strategies may change without changing the
fragment PK only when the logical fragment boundaries and semantics
remain identical.

If logical boundaries change, new fragment PKs are required.

## 7. Route and transition identity

Route and transition identifiers are downstream of model/object
identity.

They must reference stable logical PKs rather than:

- filenames
- offsets
- memory addresses
- cache handles

Route identity is not defined by this v1 protocol.

## 8. Physical placement

The following are explicitly non-identity attributes:

- segment generation
- segment path
- segment offset
- segment length
- mmap address
- cache tier
- RAM pointer
- Vulkan buffer
- device identifier
- prefetch state

They belong to catalog/runtime placement records.

A repack operation may alter all physical placement fields while
leaving model_pk, object_pk and eligible fragment_pk unchanged.

## 9. Generations

Physical storage generations must have their own generation
identity.

A generation identifier does not replace logical model/object
identity.

Conceptually:

    model_pk
      └── object_pk
            └── fragment_pk

may resolve through:

    generation_pk
      └── segment
            └── offset / length

Generation activation and rollback therefore do not alter logical
identity.

## 10. Determinism requirements

Given identical canonical identity inputs, independent
implementations must produce identical PKs.

Required validation:

1. canonical descriptor equality
2. descriptor byte equality
3. digest equality
4. printable PK equality
5. repeated-run equality
6. independence from physical offset/path changes

Any implementation that derives an object PK from a mutable
physical location fails this protocol.

## 11. Collision handling

SHA256 collision risk is treated as negligible for experimental v1,
but identifier parsing and catalog insertion must still detect
duplicate PKs with conflicting descriptors.

If:

    same PK
    + different canonical descriptor

is ever observed, processing must halt.

No silent overwrite is permitted.

## 12. Provenance

Identity descriptors may be accompanied by provenance fields such
as:

- source model SHA256
- GGUF inventory SHA256
- compiler version
- protocol version
- creation generation

Provenance must not silently become identity.

Any field that participates in the identity digest must be explicitly
declared by the applicable descriptor schema.

## 13. Initial validation gate

Before all-model MAF compilation, OpenMind must prove that the five
already validated pilot tensors receive deterministic object PKs.

The validation must demonstrate:

- one deterministic model PK
- five deterministic object PKs
- repeated generation equality
- unique PKs across the five objects
- object PK stability after changing synthetic physical placement
  metadata
- payload SHA retained separately from object PK

No fragment PKs need to be generated during this initial gate.

## 14. Promotion gate

MAF Identity v1 may be used by full-model compilation only after the
initial five-object identity validation passes.

After that gate, the 339-tensor compiler may produce:

- one model record
- 339 object records
- stable PK mappings
- persistent MAF objects or segments

without binding logical identity to physical storage layout.
