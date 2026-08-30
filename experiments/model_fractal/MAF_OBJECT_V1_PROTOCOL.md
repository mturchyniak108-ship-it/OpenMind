# OpenMind MAF Object v1 Protocol

Status: experimental protocol pending fidelity validation.

Schema:

`openmind.maf_object.v1`

## 1. Purpose

MAF Object v1 tests whether a GGUF tensor payload can become a
persistent self-contained OpenMind model object without losing
byte or numerical fidelity.

Required progression:

GGUF tensor payload
→ persistent MAF object
→ independent object reopen
→ exact payload reconstruction

The original GGUF must not be required to reopen or locate the
payload inside a completed MAF object.

## 2. Scope

MAF Object v1 deliberately does not implement:

- compression
- deduplication
- residual encoding
- fragmentation
- selective/fractal retrieval
- stable logical primary keys
- MAFDB
- cache residency
- native MAF computation
- Vulkan representation

These remain downstream of persistent-object fidelity.

## 3. Canonical layout

Each object contains exactly:

1. fixed binary header
2. canonical UTF-8 JSON metadata
3. exact tensor payload bytes

Logical layout:

    fixed header
    canonical metadata
    exact payload

The payload is copied byte-for-byte from the validated GGUF
tensor span.

## 4. Fixed header

Encoding:

little-endian

Python struct:

    <8sIIQQ32s32s

Fields:

1. magic              8 bytes
2. version            uint32
3. metadata length    uint32
4. payload length     uint64
5. flags              uint64
6. metadata SHA256    32 raw bytes
7. payload SHA256     32 raw bytes

Required values:

    magic   = OMMAFOBJ
    version = 1
    flags   = 0

Header size:

    96 bytes

No flag semantics exist in v1.

## 5. Metadata

Metadata is canonical JSON encoded as UTF-8 with:

- sorted keys
- compact separators
- no insignificant whitespace

Required fields:

- schema
- tensor_name
- tensor_type
- dims
- element_count
- payload_length
- payload_sha256
- encoding

Required values:

    schema   = openmind.maf_object.v1
    encoding = gguf_payload_exact

Optional provenance may record:

- source model hash
- source tensor offset
- source file position
- inventory references

Provenance is informational only.

No provenance value may be required to reopen the object's
payload.

## 6. Payload

The payload is the exact validated GGUF tensor byte span.

MAF Object v1 performs no:

- numerical conversion
- quantization change
- compression
- byte transformation

For a passing object:

    source payload bytes
    ==
    stored MAF payload bytes
    ==
    reconstructed payload bytes

F32 and Q8_0 interpretation remain independent validation layers.

## 7. Integrity

A valid object must satisfy all of the following:

- magic matches
- version matches
- flags equal zero
- metadata SHA256 matches
- metadata is canonical JSON
- metadata schema matches
- metadata payload length equals header payload length
- metadata payload SHA256 equals header payload SHA256
- streamed payload byte count matches
- streamed payload SHA256 matches
- no unexpected trailing bytes exist

## 8. Compilation

Compilation must use bounded streaming.

Required sequence:

1. validate tensor metadata
2. generate canonical metadata
3. create sibling `.partial` object
4. write header and metadata
5. stream source payload once
6. hash payload while streaming
7. verify exact byte count
8. verify expected source payload hash
9. flush and fsync
10. independently reopen and validate `.partial`
11. atomically activate final object

A failed compilation must not produce an activated final object.

Whole-tensor temporary allocations are prohibited when streaming
is sufficient.

## 9. Reconstruction

The v1 reconstruction primitive is an exact payload view:

- object file
- payload offset
- payload length
- tensor metadata
- payload digest

Dense numerical materialization is not part of the container
protocol.

## 10. Identity

SHA256 values provide integrity, not permanent logical identity.

Stable identifiers for:

- model
- object
- fragment

will be defined separately after this representation gate passes.

Future physical segment paths or offsets must never become logical
object identity.

## 11. Fidelity gate

MAF Object v1 passes only when a persisted object can be reopened
independently and its payload is proven byte-for-byte equal to the
validated GGUF tensor payload.

Hash equality must be accompanied by literal streamed byte
comparison during the Phase 6A validation experiment.

Negative results remain valid.

No later optimization may weaken this fidelity gate.
