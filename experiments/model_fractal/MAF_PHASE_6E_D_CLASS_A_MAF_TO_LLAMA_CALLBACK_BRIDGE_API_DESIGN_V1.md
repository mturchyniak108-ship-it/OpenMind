# OpenMind / MAF Phase 6E-D Class A Callback Bridge API Design V1

## Status

FROZEN DESIGN ONLY.

This document does not authorize bridge construction,
metadata extraction, source-GGUF access, native build,
model loading, inference, runtime mutation, or Phase 6F.

## Frozen parent

Branch: labs/multidimensional-maf
Parent HEAD: a30db11a753fd03d3eb94936b002c57ef2c9c164
ROADMAP SHA256: edf8b65061623d2564fe4c83826370293b6094d7b5f0fd89ab5bb9814b0de271

Recovered-generation qualification result:
experiments/model_fractal/maf_phase_6e_d_partial_state_recovery_qualification_v1.json
SHA256: 94207083df68717f5ed32a0aa20b6a60df798f39a0307a99ec46cbef146eb9d6
Git blob: 88b93ddd8febb74d6fcf74a77641581a526b9d0b

Class-A metadata construction protocol:
experiments/model_fractal/MAF_PHASE_6E_D_CLASS_A_GGUF_METADATA_AUTHORITY_CONSTRUCTION_PROTOCOL_V1.md
SHA256: 5d3063745be9b036769d73726830a11d9458f4a447daf09ac22c6c045c2e6af4
Git blob: b1b586e9d26b9c2dbcb8d7201466f9ad07aebda1

llama.cpp checkpoint:
dc72703fc69698b1ea68ece8d2dd8a96e6a4e1fe

llama public header SHA256:
1fbcba4003cfc089fa9681973acb3d9e24e465f32c3506ceb0ec7fa29952bdae

Model PK:
mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258

Generation PK:
mafgen:v1:74e506919d3418e2c540413cdcce72c35605195ef8efa36cdad4c56ad2a167d2

## Selected bridge

CLASS A - DIRECT MAF-BACKED NATIVE TENSOR PROVIDER

Treatment data flow:

qualified GGUF metadata authority
  -> reconstructed in-memory gguf_context
  -> llama_model_init_from_user
  -> callback tensor name
  -> frozen tensor-name/object-PK mapping
  -> generation-bound MAF locator
  -> verified serialized MAF object
  -> verified exact MAF tensor payload
  -> ggml_backend_tensor_set
  -> unchanged llama.cpp compute
  -> unchanged decode / greedy sampler

A reconstructed complete GGUF is not the
authoritative treatment path.

No llama.cpp source modification is required.

## Metadata authority boundary

The metadata construction protocol is already frozen.

It authorizes no extraction by itself.

The future metadata authority artifact is:
experiments/model_fractal/maf_phase_6e_d_class_a_gguf_metadata_authority_v1.json

Required schema:
openmind.maf_phase_6e_d_class_a_gguf_metadata_authority.v1

Current state:
METADATA AUTHORITY ARTIFACT NOT YET QUALIFIED

A future separately authorized extractor may perform
metadata-only source-GGUF access.

It must not read, seek into, hash, or otherwise consume
source tensor payload bytes.

The metadata authority must be qualified before
Class-A model initialization is authorized.

## Tensor population

V1 population mode:
GGML_BACKEND_TENSOR_SET COPY

Population API:
ggml_backend_tensor_set

Destination byte count:
ggml_nbytes(tensor)

Pointer aliasing is prohibited.
Zero-copy MAF aliasing is prohibited.
Dequantization is prohibited.
Requantization is prohibited.
Type conversion is prohibited.
Shape repair is prohibited.
Numerical substitution is prohibited.

## 339-row tensor mapping prerequisite

A deterministic frozen 339-row tensor-name/object-PK
mapping is required before bridge execution.

Each entry must bind:
- tensor name
- object PK
- model PK
- generation PK
- segment ID
- segment path
- serialized offset
- serialized length
- object SHA256
- payload SHA256
- payload length
- expected ggml type
- expected dimensions

Unknown, duplicate, missing, stale-generation,
or cross-model mappings fail closed.

## Verified MAF read contract

Before one callback tensor is populated, prove:

1. exact model and generation identity
2. exact tensor-name/object-PK mapping
3. valid generation-bound locator
4. valid segment target and range
5. serialized-object SHA256 match
6. valid MAF object magic and version
7. metadata SHA256 match
8. exact tensor name
9. exact tensor type
10. exact dimensions
11. exact payload SHA256
12. exact payload length
13. ggml_nbytes(tensor) equals payload length

Any mismatch fails the treatment load.

## No-fallback invariant

For every treatment tensor:

bytes_sourced_from_maf = true
conventional_gguf_payload_read = false

Conventional GGUF tensor-payload fallback is prohibited.
Zero substitution is prohibited.
Random substitution is prohibited.
Reference-output-guided substitution is prohibited.

## Provenance ledger

Every callback request must record:
- request ordinal
- tensor name
- tensor type
- tensor dimensions
- tensor nbytes
- model PK
- generation PK
- object PK
- locator
- object SHA256
- payload SHA256
- metadata verification
- payload verification
- callback tensor-contract verification
- population API = ggml_backend_tensor_set
- bytes sourced from MAF = true
- conventional GGUF payload read = false
- status
- failure code

## Control / treatment separation

CONTROL:
llama_model_load_from_file
  -> conventional complete GGUF
  -> existing llama.cpp inference path

TREATMENT:
qualified metadata authority
  -> llama_model_init_from_user
  -> verified MAF callback provider
  -> existing llama.cpp inference path

The scientific distinction is the source
and construction of numerical model state.

## Observation surface

Initial V1 observation level:
LEVEL 1 - EXACT DETERMINISTIC GENERATED UTF-8 TEXT

Token-ID, logit, top-k, and probability claims
remain separately gated.

## Native component reservation

Planned only:
native/include/openmind/maf_callback_bridge.h
native/src/maf_callback_bridge.cpp

These files are not constructed by this design freeze.

## Explicit nonclaims

This design does not establish:
- qualified metadata authority artifact
- 339-row mapping artifact
- native bridge implementation
- native build
- successful MAF-backed model initialization
- inference
- output parity
- token parity
- logit parity
- fidelity
- lower RAM
- lower physical I/O
- latency advantage
- throughput advantage
- MAF-native compute
- Vulkan MAF execution
- GPT-OSS execution
- Phase 6F entry

## Sequencing

Required order from this freeze:

1. construct and qualify the already-protocolled
   Class-A GGUF metadata authority
2. freeze and construct the 339-row tensor map
3. freeze native Class-A bridge construction protocol
4. construct and statically qualify native bridge
5. separately authorize build
6. separately qualify bridge execution
7. only then preregister Phase 6E-D fidelity science

## Final invariant

Authoritative treatment architecture:

qualified metadata context
  +
persistent MAF numerical state
  -> verified MAF payload
  -> ggml_backend_tensor_set copy
  -> unchanged llama.cpp compute

Phase 6F remains blocked until
Phase 6E-D correctness and fidelity close.
