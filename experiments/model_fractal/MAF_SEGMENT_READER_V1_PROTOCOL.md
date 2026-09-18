# MAF Segment Reader V1 Protocol

## Status

PREREGISTERED / IMPLEMENTATION NOT STARTED

This protocol defines Phase 6B.10 Segment Reader V1.

It is frozen before implementation, validation, benchmarking, or post-validation diagnostics.

## Purpose

Segment Reader V1 performs one bounded physical operation:

Given an already validated ResidentPKEntry and an expected generation identity, read and verify the exact serialized object-file byte range addressed by that entry.

Segment Reader V1 does not decode the serialized object into its underlying payload.

## Frozen upstream identities

Resident PK Directory V1 engine SHA256:

    4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6

Segment Builder V1 protocol SHA256:

    3f55e727c2688852aeffdfefc23993e33a3b703e2a6a7e4c8ba3302b5601a6e1

Segment Builder V1 engine SHA256:

    f063c87989f9a646497743034e85d3f4674a7b45cf88df754b669d6621cc28f0

Generation Descriptor V1 protocol SHA256:

    068ae007d746ff5c87f213820abf7bdf07b807aebe15976beac07bf16d1c8de2

Generation Engine V1 SHA256:

    8868c58e98084226dd957391e1a2f4d1122e886607640ae0be59279f025f1a51

## Authoritative resident locator

ResidentPKEntry contains:

- model_pk
- generation_pk
- generation_manifest_sha256
- object_pk
- segment_id
- offset
- length
- object_file_sha256
- payload_sha256
- segment_length
- segment_sha256
- segment_path

No segment_pk exists in the frozen contract.

Segment Reader V1 MUST NOT introduce a segment_pk namespace.

## Proven physical-byte semantics

Read-only discovery established the following on preserved Phase 6B evidence:

- segment_id: segment:00000000
- object_pk: mafobj:v1:ea258c628d783a1e140430a6bbde438f97f0be7d85e5f218ee149ad3b1fb2815
- offset: 64
- length: 512
- addressed range is within the preserved immutable segment
- the complete preserved segment matches segment_sha256
- SHA256 of segment_bytes[offset:offset+length] equals object_file_sha256
- SHA256 of that same range does NOT equal payload_sha256
- object_file_sha256 and payload_sha256 are distinct

For the discovery sample:

    object_file_sha256 = f9849113558b125c1cfa52b62e5625d362300ff2d9897ca8bb7143dd4473f611

    payload_sha256     = dfec24a7cf80461e5f8ec518ee4733b2b9edae226b672de2253038e23675bbf6

    physical slice SHA = f9849113558b125c1cfa52b62e5625d362300ff2d9897ca8bb7143dd4473f611

Therefore offset and length address the serialized object-file bytes stored inside the segment.

They do not directly address the raw semantic payload represented by payload_sha256.

## Hash-layer boundary

object_file_sha256 is the integrity checksum for the physical serialized object range addressed by offset and length.

Segment Reader V1 MUST verify the returned physical range against object_file_sha256.

Segment Reader V1 MUST NOT compare the physical range digest to payload_sha256.

payload_sha256 is retained as upstream object/payload provenance for a later decoding or semantic layer.

Segment Reader V1 does not claim to reconstruct or verify that payload layer.

## API contract

The implementation MUST expose a direct serialized-object read operation accepting:

1. a ResidentPKEntry;
2. an expected_generation_pk.

On success it returns immutable bytes of exactly entry.length bytes.

Those returned bytes are the serialized object-file bytes identified by entry.object_file_sha256.

## Generation binding

Before any segment file is opened:

    expected_generation_pk == entry.generation_pk

MUST hold.

A mismatch MUST fail closed before physical storage access.

Segment Reader V1 is not activation authority and MUST NOT reopen the active-generation record.

The Resident PK Directory / activation layer remains responsible for providing a currently valid entry.

## Physical read algorithm

The direct V1 operation MUST:

1. require a valid ResidentPKEntry;
2. validate expected_generation_pk against entry.generation_pk before file access;
3. require offset to be a non-negative integer;
4. require length to be a non-negative integer;
5. require offset + length <= entry.segment_length;
6. open entry.segment_path read-only;
7. use the same opened file descriptor for metadata inspection and data access;
8. require the opened target to be a regular file;
9. require fstat size == entry.segment_length;
10. perform a bounded positional read beginning at entry.offset for entry.length bytes;
11. require exactly entry.length bytes;
12. compute SHA256 over exactly those returned serialized-object bytes;
13. require the digest to equal entry.object_file_sha256;
14. close the descriptor on all success and failure paths;
15. return the verified serialized-object bytes.

os.pread or an equivalent positional-read primitive is preferred so the operation does not depend on a shared seek cursor.

## Whole-segment validation boundary

The direct hot path MUST NOT recompute segment_sha256 over the entire segment for every object read.

Whole-segment length/hash validation belongs to the already validated physical-generation / resident-snapshot construction boundary.

Segment Reader V1 still checks the opened file size against entry.segment_length.

The immutable-segment invariant remains an upstream storage requirement.

Mutation of the addressed serialized-object range is detected by object_file_sha256 verification.

Mutation elsewhere in a same-size segment is outside the per-object checksum boundary and remains prohibited by the upstream immutable-segment contract.

## No payload decoding in V1

Segment Reader V1 returns the serialized object-file bytes only.

It MUST NOT:

- infer an undocumented payload offset;
- search the serialized object bytes for payload_sha256;
- strip headers by heuristic;
- deserialize or decode the object payload;
- claim payload reconstruction;
- claim payload_sha256 verification.

A later explicitly specified layer may decode the serialized object format if required.

## Required failure classes

The implementation MUST distinguish at least:

- invalid ResidentPKEntry/type;
- expected-generation mismatch;
- invalid physical range;
- segment open/stat failure;
- non-regular segment target;
- segment-length mismatch;
- short positional read;
- object_file_sha256 mismatch.

Every failure MUST raise an exception and MUST return no unverified bytes.

## Hot-path prohibitions

The direct Segment Reader V1 operation MUST NOT:

- parse JSON;
- reopen generation manifests;
- reopen activation records;
- search directories;
- perform linear PK discovery;
- access the source GGUF;
- hash the complete segment;
- read the complete segment when only one object range is requested;
- compare the physical range checksum to payload_sha256;
- write files;
- mutate ResidentPKEntry;
- mutate ResidentPKSnapshot;
- execute activation;
- execute rollback;
- cache unbounded file descriptors;
- implement residency policy.

## Resource ownership

Segment Reader V1 is stateless regarding descriptor residency.

Every direct read owns and closes its file descriptor.

Long-lived FD caching, mmap residency, mapped-segment residency, or eviction policy belong to later runtime/residency work and are outside V1.

## Functional validation requirements

Validation MUST be separately preregistered and frozen before execution.

It MUST include at least:

- exact positive reconstruction of serialized object bytes;
- verification that the positive bytes hash to object_file_sha256;
- explicit proof that the reader does not use payload_sha256 as the physical range checksum;
- multiple object offsets where available;
- expected-generation mismatch rejected before file open;
- negative offset rejection;
- invalid upper-bound rejection;
- missing segment file;
- non-regular segment target;
- segment-length mismatch;
- truncated or short positional read;
- serialized-object range corruption;
- object_file_sha256 mismatch;
- descriptor/entry immutability;
- file-descriptor closure on positive paths;
- file-descriptor closure on every negative path;
- no JSON/manifest access on the direct read path;
- no source-GGUF access;
- no filesystem writes.

## Benchmark requirements

Any Segment Reader benchmark MUST be separately preregistered.

It must distinguish:

- Resident PK lookup cost;
- positional physical-range read cost;
- object_file_sha256 verification cost;
- total lookup plus verified serialized-object read cost.

No universal latency or throughput claim may be derived from one device, one object size, or one segment size.

## Post-validation diagnostics

Before Phase 6C, Segment Reader V1 diagnostics MUST examine:

- repeated successful-read degradation;
- repeated failure-path degradation;
- file-descriptor leaks;
- retained Python-object growth;
- RSS growth where measurable;
- unexpected filesystem writes;
- runtime-file accumulation;
- unverified-byte escape;
- short-read handling;
- same-file-descriptor metadata/read behavior;
- mutation/corruption failure behavior.

## Nonclaims

Segment Reader V1 does not implement:

- raw payload decoding;
- payload_sha256 verification;
- tensor reconstruction;
- decompression;
- segment residency;
- FD caching;
- mmap residency;
- eviction policy;
- MAF-native compute;
- tensor-avoidance execution;
- storage-engine selection;
- Phase 6C.

## Phase boundary

Freezing this protocol starts the Segment Reader V1 specification lineage only.

Implementation requires a separate gate.

No Segment Reader validation or benchmark may execute before its own preregistration and freeze.
