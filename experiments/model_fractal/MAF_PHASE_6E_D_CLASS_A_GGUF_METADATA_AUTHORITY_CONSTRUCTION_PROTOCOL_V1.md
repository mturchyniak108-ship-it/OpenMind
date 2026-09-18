# OpenMind / Gold Standard V2
## Phase 6E-D — Class-A GGUF Metadata Authority Construction Protocol V1

Status: CONSTRUCTION PROTOCOL ONLY. This document does not authorize model loading, inference, prompt execution, output parity, answer quality, performance claims, or MAF-native compute.

### 1. Frozen authorities

OpenMind branch:
`labs/multidimensional-maf`

Construction parent HEAD:
`5c8b5ae385900f46d74bb6aade75c3066581188f`

Qualified recovered generation:
`mafgen:v1:74e506919d3418e2c540413cdcce72c35605195ef8efa36cdad4c56ad2a167d2`

Tracked recovery qualification SHA256:
`94207083df68717f5ed32a0aa20b6a60df798f39a0307a99ec46cbef146eb9d6`

Source GGUF:
`/data/data/com.termux/files/home/qwen2.5-coder-q8_0.gguf`

Frozen source-GGUF SHA256 provenance:
`507de59046601282ba768a9789900e6ccf60ed93ddf346730b7c68eb0715bc47`

Source file stat size:
`1894532160`

Frozen tensor inventory:
`experiments/model_fractal/gguf_tensor_inventory_v1.json`
SHA256:
`7acf6d5dc672182aee0244b1bb85a47466f33dbdcdf10bde863e24f3659240ee`

Current external llama.cpp authority:
`4cf5cab65d5257be31e7623eb552b1861e969c75`

Qualified callback:
`llama_model_init_from_user(...)`

Current callback implementation SHA256:
`b71398c15876926f7ea34fc013caf36926aef139960de937900f9b1edfdf46e7`

Historical equivalence to any earlier llama.cpp checkout is NOT claimed.

### 2. Purpose

Construct a durable, typed model-level GGUF metadata authority sufficient to reconstruct an in-memory `gguf_context` for the Class-A MAF-backed tensor-provider path.

The authority must contain:
- exact GGUF version;
- exact ordered key/value metadata set and GGUF types;
- exact array element types and values;
- exact string values and string arrays, including tokenizer metadata;
- lossless floating-point representation sufficient for exact reconstruction;
- exact 339 tensor declarations: name, GGML type, dimensions, and ordering;
- computed tensor-data boundary;
- bindings to the frozen inventory, recovered generation, source provenance, and current llama.cpp authority.

### 3. Source-access boundary

A future separately frozen extractor may open the source GGUF for METADATA-ONLY access.

It may read only:
1. GGUF header;
2. key/value metadata records;
3. tensor-info records;
4. alignment bytes needed only to determine the first tensor-data byte.

It MUST NOT:
- read any tensor payload byte;
- read/hash the complete GGUF;
- seek into tensor payloads;
- compute or verify payload SHA256 values from the source;
- invoke model loading;
- invoke `llama_model_load_from_file`;
- invoke `llama_model_init_from_user`;
- execute inference.

The frozen full-file source SHA256 above is inherited provenance only and MUST NOT be recomputed by this construction.

The extractor must calculate the first tensor-data offset from parsed GGUF structure and prove that every source read ends strictly before that boundary.

### 4. Metadata representation

Output authority path:
`experiments/model_fractal/maf_phase_6e_d_class_a_gguf_metadata_authority_v1.json`

Schema:
`openmind.maf_phase_6e_d_class_a_gguf_metadata_authority.v1`

Canonical JSON:
UTF-8, `ensure_ascii=false`, `sort_keys=true`, separators `(",", ":")`, trailing newline forbidden.

Every metadata entry must preserve:
- ordinal;
- key;
- GGUF value type;
- scalar/array classification;
- array element type where applicable;
- exact logical value.

For F32/F64 values, exact IEEE-754 source bits must also be preserved as hexadecimal so reconstruction does not depend on decimal round-trip behavior.

Unknown or unsupported GGUF types fail closed.

### 5. Tensor declaration binding

Exactly 339 tensor declarations are required.

For every ordinal, the extracted declaration must agree with the frozen tensor inventory on:
- tensor name;
- tensor type;
- dimensions;
- element count.

No tensor payload byte may be consumed for this comparison.

The authority must bind the recovered generation PK but must not read serialized MAF object or segment payloads during construction.

### 6. Reconstruction target

The resulting authority is intended for a later provider implementation to reconstruct an in-memory context using the current llama.cpp APIs, including:
- `gguf_init_empty`;
- typed `gguf_set_val_*`;
- `gguf_set_arr_data`;
- `gguf_set_arr_str`;
- `gguf_add_tensor`;
- `gguf_set_tensor_type`;
- `llama_model_init_from_user`.

This protocol does not itself authorize those calls during construction.

### 7. Fail-closed gates

MAD01. Branch and frozen parent HEAD exact.
MAD02. Tracked worktree clean and index empty.
MAD03. Original unrelated untracked baseline preserved.
MAD04. Frozen qualification, inventory, and protocol authorities exact.
MAD05. llama.cpp checkout exact `4cf5cab65d5257be31e7623eb552b1861e969c75` and clean.
MAD06. Source path regular, non-symlink, exact frozen stat size before source open.
MAD07. Separate metadata-construction one-shot namespace eligible before source access.
MAD08. One-shot sentinel durably reserved before first source byte is read.
MAD09. GGUF header/version/counts parse successfully.
MAD10. All metadata key/value records decode with exact type fidelity.
MAD11. Exactly 339 tensor-info records and 339/339 inventory agreement.
MAD12. First tensor-data boundary computed and every source read proven strictly before it.
MAD13. Canonical authority validates and reopens byte-identically.
MAD14. No source payload, MAF payload, model load, inference, network, or subprocess execution.
MAD15. Final syntax/logic/self-check passes before publication authorization.

Any failed gate yields:
`CLASS-A GGUF METADATA AUTHORITY NOT QUALIFIED`

Narrow success verdict:
`CLASS-A GGUF METADATA AUTHORITY QUALIFIED`

### 8. Construction sequencing

1. Freeze this protocol.
2. Construct the standalone metadata-only extractor.
3. Perform static MAD01-MAD15 qualification of that extractor.
4. Freeze the extractor in a separate commit.
5. Run a final read-only preflight.
6. Execute the metadata extraction through a separate one-shot wrapper.
7. Qualify and freeze the resulting metadata authority.
8. Only then construct the Class-A MAF-backed tensor provider.

### 9. Scientific boundary

Successful completion establishes only that OpenMind has a frozen metadata authority capable of supporting later reconstruction of the current llama.cpp `gguf_context` metadata surface.

It does NOT establish:
- successful model loading;
- tensor callback correctness;
- inference correctness;
- output parity;
- answer quality;
- selective compute;
- performance improvement;
- MAF-native compute.

Phase 6E-D science remains NOT AUTHORIZED until separately preregistered and gated.
