# OpenMind MAF Generation Engine V1 Protocol

Status: Frozen Phase 6B research protocol.

Engine schema:

    openmind.maf_generation_engine.v1

Engine version:

    maf_generation_engine_v1


## 1. Purpose

Generation Engine V1 constructs one deterministic candidate physical
generation from already validated immutable MAF segment evidence.

Its responsibilities are limited to:

1. validate candidate segment evidence;
2. normalize immutable segment records;
3. normalize authoritative object placement records;
4. construct the canonical generation descriptor;
5. derive generation_pk;
6. construct the outer generation manifest;
7. persist the candidate manifest atomically;
8. reopen and independently verify the persisted manifest.

It does not activate the generation.


## 2. Governing protocols

Generation Engine V1 is subordinate to:

- MAF Identity V1;
- MAF Segment Builder V1;
- MAF Catalog Generation V1;
- MAF Generation Descriptor V1.

The engine must not redefine any frozen logical identity.


## 3. Initial validation input

The first validation is intentionally narrow.

It uses the already frozen Segment Builder V1 three-object result:

    experiments/model_fractal/
    maf_segment_builder_validation_v1.json

Expected segment SHA256:

    c9f9ef93b96c60569d130fb1c27aa3357aa35e82f0b2b2c3aec497342df3e7b6

Expected segment length:

    17137795

Expected object count:

    3


## 4. Source GGUF boundary

Generation Engine V1 must not require or open the source GGUF.

Its inputs are validated MAF physical evidence.

The first validation must prove that no source GGUF access is required.


## 5. Candidate evidence

V1 accepts candidate evidence describing:

- model_pk;
- completed immutable segment path;
- segment SHA256;
- segment length;
- object placements;
- object_file_sha256;
- payload_sha256.

Candidate evidence is not automatically authoritative.


## 6. Segment validation

Before descriptor construction, the engine must validate the referenced
completed segment.

At minimum:

- file exists;
- file is a regular completed artifact;
- length matches declared segment length;
- independent SHA256 matches declared segment SHA256.

Failure must occur before candidate manifest activation or replacement.


## 7. Segment Builder evidence

The engine may consume validated fields from Segment Builder V1 output.

It must not blindly trust those fields.

The immutable segment itself must be independently checked where this
protocol requires an independent check.


## 8. Segment normalization

Generation Engine V1 normalizes segment inputs according to MAF
Generation Descriptor V1.

Canonical segment ordering is independent of caller order.

V1 segment records contain:

    segment_id
    segment_length
    segment_sha256


## 9. Duplicate segment content

Duplicate candidate entries representing identical:

    segment_sha256
    segment_length

must collapse to one canonical immutable segment record.

Conflicting records must fail closed.


## 10. Segment ID assignment

segment_id assignment occurs only after canonical segment ordering.

V1 uses:

    segment:00000000
    segment:00000001
    ...

Changing caller input order must not change segment_id assignment.


## 11. Object placement normalization

Generation Engine V1 constructs exactly one placement record per
object_pk.

Each record contains:

    object_pk
    segment_id
    offset
    length
    object_file_sha256
    payload_sha256

Canonical object order is ascending lexicographic object_pk.


## 12. Object PK preservation

object_pk values are inherited from frozen identity evidence.

Generation Engine V1 must not:

- regenerate object_pk;
- derive object_pk from segment placement;
- derive object_pk from offset;
- derive object_pk from path;
- substitute tensor name for object_pk.


## 13. Model PK preservation

model_pk is inherited exactly.

Generation Engine V1 must not regenerate model_pk.


## 14. Mixed-model rejection

All candidate objects must belong to one declared model_pk.

Mixed-model candidate evidence fails closed.


## 15. Duplicate object rejection

Two candidate placement records with the same object_pk are invalid.

V1 permits exactly one authoritative placement per object_pk within a
generation.


## 16. Placement bounds

For each placement:

    offset >= 0
    length > 0

and:

    offset + length <= segment_length

Out-of-bounds placement fails closed.


## 17. Exact byte-range integrity

The engine must independently read each declared segment range and
verify:

    SHA256(range bytes) == object_file_sha256

A mismatch fails closed.


## 18. Payload hash handling

payload_sha256 is preserved as independently established integrity
metadata.

Generation Engine V1 does not decode numerical payloads merely to
rederive payload_sha256.


## 19. Canonical descriptor construction

The engine constructs exactly the descriptor defined by:

    openmind.maf_generation_descriptor.v1

No extra runtime or lifecycle fields may enter the descriptor.


## 20. Generation PK derivation

The engine computes:

    canonical_descriptor_bytes =
        canonical JSON encoding of descriptor

    generation_digest =
        SHA256(canonical_descriptor_bytes)

    generation_pk =
        "mafgen:v1:" + generation_digest.hexdigest()

No alternative derivation is permitted in V1.


## 21. Deterministic generation identity

Identical normalized immutable generation content must yield identical:

- descriptor object;
- canonical descriptor bytes;
- descriptor SHA256;
- generation_pk.

Repeated independent construction must be equal.


## 22. Path independence

Filesystem segment path must not enter descriptor identity.

Moving or aliasing the same validated immutable segment bytes to a
different path must leave generation_pk unchanged.


## 23. Input ordering independence

Permuting candidate segment input order or object placement input order
must not change generation_pk.


## 24. Placement sensitivity

Changing a valid object placement must change the generation descriptor
and therefore generation_pk.

The corresponding logical object_pk must remain unchanged.


## 25. Candidate manifest

Generation Engine V1 emits:

    openmind.maf_generation_manifest.v1

with:

    schema
    manifest_version
    generation_pk
    descriptor


## 26. Manifest generation PK verification

Immediately before persistence and again after reopen:

    manifest.generation_pk

must equal the digest-derived PK from manifest.descriptor.

Mismatch fails closed.


## 27. Manifest serialization

The persisted V1 candidate manifest must use deterministic canonical
JSON serialization.

Persistence formatting must be independently reproducible.


## 28. Candidate path

The caller supplies the candidate manifest output path.

That path is physical metadata and must not enter generation identity.


## 29. Atomic candidate persistence

Candidate manifest construction uses a temporary sibling partial file
followed by atomic replacement only after complete write and local
validation.

A partially written manifest must not appear as completed output.


## 30. Existing final target

V1 must not silently overwrite an existing completed candidate manifest.

If the requested final path exists, fail closed.


## 31. Existing partial target

If the requested engine-owned partial path already exists, V1 fails
closed.

It must not silently reuse ambiguous prior partial state.


## 32. Failure cleanup

On engine-created write failure, an engine-created partial should be
removed where safe.

Existing external evidence and immutable segments must not be altered.


## 33. Reopen validation

After persistence, Generation Engine V1 must reopen the candidate
manifest from disk and independently verify at least:

- manifest schema;
- manifest version;
- canonical descriptor shape;
- generation_pk derivation;
- model_pk;
- segment records;
- object records;
- deterministic canonical serialization.


## 34. Segment mutation protection

The engine must not modify adopted segment bytes.

The segment SHA before and after generation construction must remain
identical.


## 35. Candidate state only

A successful engine run produces a validated candidate generation
manifest.

It does not make that generation active.


## 36. Activation boundary

Generation Engine V1 must not:

- change current generation;
- create an active-generation pointer;
- retire an old generation;
- perform rollback;
- delete an old generation.

Those operations require an independently frozen activation protocol.


## 37. Catalog persistence boundary

Generation Engine V1 persists a candidate generation manifest only.

It does not establish the durable live catalog control plane.


## 38. Resident directory boundary

Generation Engine V1 does not build the production resident
object/fragment directory.

That representation follows independent generation correctness
validation.


## 39. Segment Reader boundary

Generation Engine V1 may read exact ranges for integrity validation.

It does not implement the production inference-hot-path Segment Reader.


## 40. JSON hot-path boundary

JSON is permitted for this candidate control-plane research artifact.

No inference hot path may depend on parsing this JSON manifest.

A resident compiled representation remains later Phase 6B work.


## 41. Storage engine neutrality

Generation Engine V1 does not select:

- SQLite;
- compiled binary catalog;
- MAFDB;
- another embedded engine.

The candidate manifest exists to freeze correctness before engine
comparison.


## 42. Runtime residency boundary

The engine does not assign:

- COLD_DISK;
- MAPPED;
- HOT_MAF;
- HOT_DENSE;
- VULKAN_MAF.

Residency remains Phase 6C.


## 43. Dense-view boundary

Generation construction must not materialize dense compute tensors.

Persistent authority remains MAF bytes.


## 44. MAF-native compute boundary

Generation Engine V1 does not enable MAF-native compute.

The governing state remains:

    disabled_unvalidated


## 45. Bounded I/O

Segment integrity and object range verification must use bounded reads.

The engine must not intentionally allocate the entire segment as one
Python bytes object merely to calculate hashes.


## 46. Initial validation positive case

The preregistered validation must use the frozen three-object Segment
Builder candidate and demonstrate:

- expected model_pk preserved;
- expected segment SHA preserved;
- expected segment length preserved;
- exactly three object placements;
- exact object_pk preservation;
- exact offsets;
- exact lengths;
- exact object_file_sha256;
- exact payload_sha256;
- deterministic descriptor;
- deterministic generation_pk;
- successful canonical manifest reopen.


## 47. Required negative controls

Initial validation must preregister at least:

- duplicate object_pk;
- mixed model;
- missing segment;
- altered segment SHA;
- out-of-bounds offset;
- zero length;
- incorrect object_file_sha256;
- malformed object_pk;
- malformed SHA256 field;
- preexisting final manifest;
- preexisting partial manifest;
- generation_pk mismatch on reopen.


## 48. Determinism controls

Initial validation must also demonstrate:

- repeated construction equality;
- object input permutation equality;
- path independence;
- segment-input ordering independence where more than one segment is
  tested or synthetically exercised.


## 49. Placement sensitivity control

A preregistered synthetic valid placement change must produce:

    generation_pk_changed = true

while:

    object_pk_changed = false

This test must not mutate frozen source evidence.


## 50. Raw-result boundary

Engine implementation must be frozen before the validation runner.

The validation runner must be frozen before execution.

Raw validation output must be frozen before interpretation.


## 51. Expected implementation file

The initial engine implementation is expected at:

    experiments/model_fractal/maf_generation_engine_v1.py

The filename is frozen for the initial research sequence.


## 52. Expected validation file

The initial preregistered validation runner is expected at:

    experiments/model_fractal/maf_generation_engine_validation_v1.py


## 53. Expected raw result

The initial frozen raw result is expected at:

    experiments/model_fractal/
    maf_generation_engine_validation_v1.json


## 54. Nonclaims

Generation Engine V1 does not establish:

- active catalog generation;
- atomic generation activation;
- rollback;
- production catalog persistence;
- resident directory performance;
- direct inference-hot-path lookup;
- SQLite suitability;
- MAFDB suitability;
- binary-index superiority;
- RAM reduction;
- latency reduction;
- selective inference;
- dense materialization;
- MAF-native computation;
- Vulkan execution;
- model replacement.


## 55. V1 invariant summary

    inputs are validated immutable MAF physical evidence

    source GGUF is not required

    model_pk and object_pk are preserved

    physical placement defines generation content but not logical PKs

    generation_pk is deterministic from the frozen canonical descriptor

    caller ordering does not define generation identity

    filesystem path does not define generation identity

    adopted segment bytes are immutable

    object ranges are independently hash-verified

    manifest persistence is atomic and fail-closed

    reopened manifest must independently reproduce generation_pk

    successful output is candidate only

    no generation activation occurs

    no storage engine is selected

    no runtime residency is assigned

    MAF-native compute remains disabled_unvalidated
