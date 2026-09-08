# MAF Phase 6E-D — Class-A MAF-Backed Tensor Provider Contract V1

Status: FROZEN CONSTRUCTION CONTRACT — NO EXECUTION OR SCIENCE AUTHORITY

## 1. Purpose

This contract defines the only admissible Class-A bridge from the frozen persistent MAF generation into the current llama.cpp user-supplied tensor initialization path.

It does not authorize provider execution, model loading, inference, output-parity science, performance claims, or MAF-native compute claims.

## 2. Frozen authority bindings

- OpenMind parent HEAD: `5163abd99ed2664c1c39c69a91726f79ec10802a`
- llama.cpp HEAD: `4cf5cab65d5257be31e7623eb552b1861e969c75`
- Class-A GGUF metadata authority SHA256: `bdfe20b15732519c8fcbe253ff8598b829666a0227ce04420e2cb1888d626966`
- GGUF tensor inventory SHA256: `7acf6d5dc672182aee0244b1bb85a47466f33dbdcdf10bde863e24f3659240ee`
- Complete-model recovered-generation qualification SHA256: `94207083df68717f5ed32a0aa20b6a60df798f39a0307a99ec46cbef146eb9d6`
- Metadata-authority construction protocol SHA256: `5d3063745be9b036769d73726830a11d9458f4a447daf09ac22c6c045c2e6af4`
- Qualified persistent generation PK: `mafgen:v1:74e506919d3418e2c540413cdcce72c35605195ef8efa36cdad4c56ad2a167d2`
- Metadata records: `26`
- Tensor declarations: `339`

### llama.cpp source authority

- `include/llama.h`
  - Git blob: `a14498925f1443a8bf9330b470b922e9886a2d96`
  - SHA256: `db39eaf53de25f88d0803f5a1eb77206ee86d4e3c968dd54a83690cb021b8cda`
- `src/llama.cpp`
  - Git blob: `d6e0bbfefa729329fe6b83e46e603a85dab0f2e3`
  - SHA256: `8fa22037f00c14f04492d76658b1b2075b479477039c18d6bc76c52bfc9031db`
- `src/llama-model.cpp`
  - Git blob: `4cc1c0a1c2c0632dfc3d46b891baa69562013699`
  - SHA256: `6a6cb4491cd23c6599d1415f440a4e1a4a6e06bb60f18a63cf98aa207a86aff6`
- `src/llama-model-loader.cpp`
  - Git blob: `71bc9f7ef0aaa883f046537c0a28803bdb39754d`
  - SHA256: `73f87966e648493b5b9687aced2253903a7bb03bf3a7bdd5596bac3578330e7a`
- `tests/test-llama-archs.cpp`
  - Git blob: `0e29d221ba17e68e9a6aacabb5f77c5ab3020b64`
  - SHA256: `922582214b70c8081efaa7be215c187fc33e130d64326e9c88cf571dd6b83497`

## 3. Class-A bridge definition

The treatment bridge SHALL use `llama_model_init_from_user(...)` with an in-memory `gguf_context` reconstructed from the frozen Class-A metadata authority.

The treatment SHALL NOT reconstruct, serialize, copy, or expose a conventional complete GGUF file to the ordinary file loader.

The treatment tensor bytes SHALL originate from the qualified persistent MAF generation identified above.

Ordinary llama.cpp / GGML compute after successful weight provisioning is allowed. This contract does not establish MAF-native compute.

## 4. In-memory GGUF metadata contract

Before model initialization, the bridge SHALL reconstruct the complete typed model-level GGUF metadata authority in memory, including:

1. GGUF version and ordered key/value metadata.
2. Exact scalar GGUF types.
3. Exact array element types and values.
4. Exact string and string-array values.
5. Exact IEEE-754 floating-point values represented by the frozen bit patterns.
6. All 339 tensor declarations with exact tensor name, GGML type, dimensions, and declaration order.

Tensor type and shape SHALL therefore be fixed before the provider callback is invoked.

## 5. Allocation and callback semantics

For this frozen llama.cpp authority:

1. `llama_model_init_from_user(...)` forces `LLAMA_LOAD_MODE_NONE` and disables extra buffer types.
2. The provider configuration SHALL require `params.no_alloc = false`.
3. With `no_alloc = false`, llama.cpp allocates real backend tensor buffers using `ggml_backend_alloc_ctx_tensors_from_buft(...)` before loading tensor data.
4. After allocation, `llama_model_base::load_tensors(...)` calls `llama_model_loader::load_all_data(...)`.
5. For the user-metadata path, `files.empty()` is true and `load_all_data(...)` invokes the supplied tensor callback for tensors in the allocated model contexts.
6. `no_alloc = true` is forbidden for the Class-A treatment because llama.cpp would create dummy zero-sized buffers and return before tensor-data loading.

## 6. Provider callback contract

For every callback invocation, the provider SHALL fail closed unless all of the following are true before payload transfer:

1. `tensor` is non-null.
2. `tensor->name` resolves to an exact frozen metadata-authority tensor declaration.
3. The resolved logical tensor maps to the qualified persistent MAF generation and its strong locator.
4. `tensor->type` exactly matches the frozen declaration.
5. Every tensor dimension exactly matches the frozen declaration.
6. `ggml_nelements(tensor)` equals the frozen element count.
7. `ggml_nbytes(tensor)` equals the exact qualified MAF tensor payload byte span expected for that logical tensor.
8. The requested MAF payload range is wholly contained within the qualified object/segment locator.

No type coercion, reshaping, truncation, zero-fill substitution, fallback tensor, source-GGUF fallback, or conventional-GGUF fallback is permitted.

## 7. MAF payload resolution

The provider SHALL resolve payloads only through the already-qualified MAF object/generation authority.

The implementation SHALL use the frozen generation/object/segment semantics rather than inventing a second ad-hoc address scheme.

A callback may read only the MAF bytes required for the callback tensor. It SHALL NOT read the source GGUF.

Any missing object, missing segment, locator mismatch, length mismatch, identity mismatch, generation mismatch, or I/O failure SHALL make model initialization fail closed.

## 8. Transfer and ownership semantics

The provider SHALL transfer the complete tensor byte span into the already-allocated llama.cpp backend tensor using:

`ggml_backend_tensor_set(tensor, provider_bytes, 0, ggml_nbytes(tensor))`

The frozen llama.cpp test authority demonstrates this interface using a temporary local vector followed by `ggml_backend_tensor_set(...)`; the temporary vector is destroyed after the callback returns.

Therefore this contract treats `ggml_backend_tensor_set(...)` as the copy/upload boundary. Provider-owned temporary staging memory does not need to remain alive after the call completes successfully.

The provider SHALL NOT assign a borrowed MAF pointer directly to `tensor->data` and SHALL NOT require llama.cpp to retain provider-owned payload storage.

## 9. Callback multiplicity

The contract SHALL NOT assume that callback invocation count equals 339.

The authoritative requirement is identity-based: every callback tensor must resolve successfully to an allowed frozen logical tensor and receive exactly the correct bytes. llama.cpp may internally duplicate or reuse logical weights according to its frozen implementation.

Provider qualification SHALL record callback count, unique callback names, duplicate-name counts, and resolution results before any scientific use.

## 10. Failure semantics

The provider implementation SHALL maintain explicit failure state and SHALL prevent successful model initialization after any callback contract violation.

A future implementation qualification must prove the exact failure-propagation mechanism for this void callback API before execution authority is granted.

Silent continuation after a provider failure is forbidden.

## 11. Integrity and measurement separation

The frozen generation and its strong authority bindings SHALL be verified before treatment execution.

If per-tensor cryptographic revalidation is performed during provider execution, the implementation and later science protocol SHALL state whether that work is inside or outside the timed region.

Correctness qualification must precede any attempt to optimize integrity-check cost.

## 12. Prohibited treatment collapse

The following do NOT qualify as Class-A treatment:

- rebuilding a complete GGUF and calling the ordinary GGUF file loader;
- copying the source GGUF into another path;
- reading tensor payloads from the source GGUF;
- silently falling back to conventional loader I/O;
- loading the same conventional GGUF for both control and treatment;
- claiming selective MAF compute when only weight provisioning is MAF-backed.

## 13. Claim boundary

A successfully qualified implementation may establish only:

`Class-A MAF-backed model weight provisioning into ordinary llama.cpp/GGML compute.`

It does not by itself establish:

- MAF-native compute;
- output parity;
- generation quality parity;
- performance advantage;
- reduced total runtime I/O;
- reduced memory use;
- Phase 6E-D scientific success.

## 14. Required future gates

Before Phase 6E-D science, the following remain mandatory:

1. Provider implementation construction.
2. Static implementation qualification.
3. Exact implementation freeze.
4. Metadata-context reconstruction qualification.
5. MAF tensor-resolution qualification.
6. Allocation/callback/transfer instrumentation qualification.
7. Fail-closed negative-path qualification.
8. Final execution preflight.
9. Only then: controlled Class-A model-load and inference validation.
10. Only after correctness: Phase 6E-D output parity/quality science.

## 15. Frozen disposition

- Class-A metadata authority gate: CLOSED.
- Class-A provider contract gate: DEFINED BY THIS ARTIFACT.
- Provider implementation: NOT YET AUTHORIZED FOR EXECUTION.
- Phase 6E-D science: NOT AUTHORIZED.
- Phase 6F performance work: NOT AUTHORIZED.
