# MAF Phase 6E-D — Class-A Positive Model-Load Validation Protocol V1

## 1. Purpose

This protocol defines the first controlled positive execution of the frozen Phase 6E-D Class-A MAF-backed tensor provider.

Its sole positive objective is to prove that one real llama.cpp model object can be constructed from an in-memory GGUF context reconstructed from the frozen metadata authority while tensor payloads are supplied from the qualified persistent MAF generation through the frozen Class-A provider.

A successful run SHALL terminate after the provider acceptance gate passes and the returned model handle is freed exactly once.

The exact permitted PASS claim is:

`CLASS-A MAF-BACKED POSITIVE MODEL-LOAD VALIDATION PASS`

This means MAF-backed provisioning succeeded. It does not establish MAF-native compute.

Context creation, tokenization, prompt evaluation, logits access, inference, output comparison, parity science, performance measurement, and Phase 6F work remain prohibited.

## 2. Frozen authority bindings

Execution SHALL fail closed unless all frozen execution authorities are exact.

The following hash is protocol-construction provenance only. It is not a future execution-HEAD invariant.

Protocol-construction parent:

`0063da0ea461be844912db0e47273929d587a600`

The future execution HEAD SHALL equal the frozen positive-runner commit produced after this protocol is independently qualified and frozen.

Any other execution HEAD SHALL fail closed.

Negative-path protocol SHA256:

`f89a4e3303c8e04e9fd3fc9b6378b13f3efec6b9706f814bc665b7458f104123`

Negative-path runner SHA256:

`f21d9b7ea0319d96d530127e3c9ed97040ec340214af8db36f4b81f817d77697`

Negative-path result SHA256:

`ec23ed47ca813792ff3fedf9e7b08e16140d265a5a88c4908082dde250f399d5`

Negative-path result Git blob:

`fec4588467ef475b1b4a18936174d0d604a22cee`

Provider SHA256:

`e436bbf14e34dfb1c46a6d947b66788fcf85fe3a0c9f8312ff3963ab6155e3ec`

Provider Git blob:

`14fa6be4a2cf69b8125e6540e0a808bd2758f792`

Provider contract SHA256:

`2782678c5153761e028f29f35d7275b019590af5a35391ea967c71c027c2ebb2`

Metadata authority SHA256:

`bdfe20b15732519c8fcbe253ff8598b829666a0227ce04420e2cb1888d626966`

Tensor-object-segment join SHA256:

`34aa1e85e3ee8090d4419dd5032f223eb2d0aecfc2009ad2a7625249b8bea709`

Persistent-generation qualification SHA256:

`94207083df68717f5ed32a0aa20b6a60df798f39a0307a99ec46cbef146eb9d6`

Model PK:

`mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258`

Generation PK:

`mafgen:v1:74e506919d3418e2c540413cdcce72c35605195ef8efa36cdad4c56ad2a167d2`

Qualified segment:

`results/runtime/maf_full_model_persistent_generation_v1/segment_00000000.mafseg`

Segment byte length:

`1888934699`

Segment SHA256:

`a930f1a1baae97279a3cbc50c1d126f3a70ef92d87f188f76747b2d7877109b9`

Pinned llama.cpp HEAD:

`4cf5cab65d5257be31e7623eb552b1861e969c75`

Qualified shared library:

`/data/data/com.termux/files/home/llama.cpp/build-vulkan/bin/libllama.so.0.0.10318`

Shared-library SHA256:

`a4857a95e357944826146700003eb7747e17245de7b76433f7549db4cb913ac9`

The future runner SHALL also verify the exact shared-library byte count recorded in the frozen negative-path result before loading it.

## 3. Positive execution authorization

A future frozen runner MAY:

1. import the frozen provider;
2. load exactly the qualified shared library;
3. reconstruct all 26 frozen GGUF metadata records in memory;
4. reconstruct all 339 tensor declarations in memory;
5. construct the qualified resident PK directory;
6. permit valid serialized-object reads from only the qualified persistent MAF segment through the frozen reader;
7. invoke `ClassAMAFBackedTensorProvider.initialize_model` exactly once;
8. permit the provider to call the real `llama_model_init_from_user` exactly once;
9. require the provider acceptance gate to pass;
10. accept exactly one non-null model handle;
11. free that accepted model exactly once with `llama_model_free`; and
12. publish one canonical validation result.

It SHALL NOT authorize a source GGUF read, conventional complete GGUF construction, conventional GGUF loader, second model initialization attempt, llama context creation, tokenization, evaluation, logits access, inference, generation, parity science, performance work, network access, or Git mutation.

## 4. One-shot execution rule

Positive execution is one-shot.

Before the first operation capable of reaching real `llama_model_init_from_user`, the runner SHALL atomically reserve a dedicated sentinel under:

`~/.openmind_authoritative_slots/`

The sentinel identity SHALL bind this positive validation and the frozen positive runner SHA256.

Reservation SHALL use exclusive fail-closed creation.

An existing sentinel SHALL prohibit execution.

Once successfully reserved, the slot is permanently spent regardless of PASS, FAIL, exception, native failure, termination, result-publication failure, or reporting failure.

The run SHALL never be blindly repeated.

If a deterministic result is produced, that result is authoritative for the spent execution.

## 5. Source GGUF prohibition

The source model:

`~/qwen2.5-coder-q8_0.gguf`

is prohibited.

The runner SHALL install its protected-I/O guard before provider import.

The guard SHALL fail closed on the canonical source GGUF path and, when identity can be determined metadata-only, aliases of the same inode.

No conventional complete GGUF may be created or used.

`llama_model_load_from_file` is prohibited.

`gguf_init_from_file` is prohibited.

`gguf_init_from_buffer` SHALL NOT be used to load a conventional complete model image.

A PASS result requires source GGUF opens: exactly 0.

## 6. Qualified persistent MAF read boundary

This protocol authorizes valid persistent MAF reads for the first time in this validation sequence.

Only this segment is authorized:

`results/runtime/maf_full_model_persistent_generation_v1/segment_00000000.mafseg`

Only the frozen serialized-object reader may open/read that segment for tensor provisioning.

The runner SHALL enforce a guarded-reader window around each legitimate serialized-object read.

The requested resident entry SHALL bind:

- the exact model PK;
- the exact generation PK;
- PK kind `object_pk`;
- an exact frozen join record;
- the exact qualified segment;
- exact serialized-object offset and length;
- valid segment bounds.

Any `.mafseg` access outside the guarded-reader window SHALL fail closed.

Any other segment path or inode SHALL fail closed.

Telemetry SHALL distinguish authorized persistent MAF reads from unauthorized segment accesses.

The protocol does not require callback count or serialized-object read count to equal 339.

## 7. Object and payload integrity

Every authorized serialized object SHALL pass the frozen reader and provider integrity checks.

No frozen integrity check may be bypassed.

The positive path SHALL preserve verification of generation identity, object PK, serialized header, metadata bounds, payload bounds, tensor identity, GGML type, dimensions, element count, byte count, payload SHA256, object placement, and segment bounds.

The runner SHALL NOT independently synthesize payload bytes.

Zero-fill, substitution, truncation, padding, silent recovery, or fallback is prohibited.

Any integrity violation is FAIL.

## 8. GGUF metadata reconstruction

The frozen authority contains exactly 26 metadata records.

The in-memory GGUF context SHALL be created using:

`gguf_init_empty`

All records SHALL be applied exactly once in frozen ordinal order.

The frozen root type distribution is:

- `GGUF_TYPE_UINT32 = 4`: 11
- `GGUF_TYPE_FLOAT32 = 6`: 2
- `GGUF_TYPE_BOOL = 7`: 1
- `GGUF_TYPE_STRING = 8`: 9
- `GGUF_TYPE_ARRAY = 9`: 3

The pinned complete numeric mapping is:

- `GGUF_TYPE_UINT8 = 0`
- `GGUF_TYPE_INT8 = 1`
- `GGUF_TYPE_UINT16 = 2`
- `GGUF_TYPE_INT16 = 3`
- `GGUF_TYPE_UINT32 = 4`
- `GGUF_TYPE_INT32 = 5`
- `GGUF_TYPE_FLOAT32 = 6`
- `GGUF_TYPE_BOOL = 7`
- `GGUF_TYPE_STRING = 8`
- `GGUF_TYPE_ARRAY = 9`
- `GGUF_TYPE_UINT64 = 10`
- `GGUF_TYPE_INT64 = 11`
- `GGUF_TYPE_FLOAT64 = 12`

No unlisted root metadata type is authorized.

## 9. Scalar and array metadata encoding

Type 4 SHALL use `gguf_set_val_u32`.

Type 6 SHALL reconstruct the exact float32 IEEE-754 bit pattern from frozen `ieee754_hex` and use `gguf_set_val_f32`.

Type 7 SHALL use `gguf_set_val_bool`.

Type 8 SHALL use `gguf_set_val_str`.

The three arrays are exactly:

- one `GGUF_TYPE_INT32` array, numeric element type 5;
- two `GGUF_TYPE_STRING` arrays, numeric element type 8.

INT32 arrays SHALL use `gguf_set_arr_data` with exact contiguous signed 32-bit storage.

STRING arrays SHALL use `gguf_set_arr_str` with stable UTF-8 backing strings that remain alive through the call.

Unsupported types, malformed float authority, out-of-range integers, embedded-NUL ambiguity, or cardinality mismatch SHALL fail closed.

## 10. Tensor declaration reconstruction

The frozen authority contains exactly 339 tensor declarations.

A temporary GGML context SHALL be used only for GGUF tensor metadata construction.

The exact pinned `ggml_init_params` fields are:

- `size_t mem_size`;
- `void * mem_buffer`;
- `bool no_alloc`.

The temporary declaration context SHALL use `no_alloc = true`.

This is metadata-only and SHALL NOT alter positive model allocation.

The provider positive model path SHALL require `llama_model_params.no_alloc = false`.

For every frozen tensor, in exact ordinal order, the runner SHALL:

1. validate its exact name;
2. validate its dimension count;
3. validate all dimensions are positive;
4. validate its frozen GGML type;
5. create the metadata-only tensor declaration with the exact pinned `ggml_new_tensor` API;
6. pass the exact dimension vector to `ggml_new_tensor`;
7. assign the exact name using `ggml_set_name`;
8. add the declaration using `gguf_add_tensor`;
9. establish the exact frozen type using `gguf_set_tensor_type` where required; and
10. verify the resulting declaration agrees with the frozen authority.

The source-relative GGUF data offset is provenance only and SHALL never be used to read the source GGUF.

Temporary tensor storage SHALL never be treated as model payload.

## 11. Ownership and cleanup

The runner SHALL explicitly own:

- the temporary GGML declaration context;
- the in-memory GGUF context;
- metadata backing allocations;
- and the accepted real model handle.

The declaration and GGUF contexts SHALL remain live throughout provider initialization.

After a successful provider return:

1. the handle SHALL be non-null and already accepted by the provider gate;
2. no llama context or inference API may be called;
3. the model SHALL be freed exactly once with `llama_model_free`;
4. the GGUF context SHALL be freed exactly once with `gguf_free`;
5. the temporary GGML context SHALL be freed exactly once with `ggml_free`.

Cleanup SHALL avoid double free.

A model rejected by the frozen provider acceptance gate is owned/freed according to the frozen provider contract and SHALL NOT be freed again by the runner.

## 12. Shared-library boundary

Exactly one real shared-library handle is permitted.

Its path, bytes, SHA256, and llama.cpp HEAD SHALL match the frozen qualified authority.

That same handle SHALL provide the provider FFI symbols plus every GGUF/GGML construction and cleanup symbol needed by this protocol.

Silent symbol substitution using a second library handle is prohibited.

Missing symbols SHALL fail before sentinel reservation and before positive model initialization.

## 13. Real Class-A provider execution

The resident directory SHALL be constructed only from the qualified persistent generation.

The provider SHALL remain bound to its frozen contract, metadata authority, tensor-object-segment join, model PK, generation PK, and `object_pk` resident semantics.

The runner SHALL call:

`ClassAMAFBackedTensorProvider.initialize_model`

exactly once with the non-null in-memory GGUF context pointer.

The runner SHALL NOT directly make an independent real `llama_model_init_from_user` call.

The frozen provider owns that boundary.

Success requires one non-null model handle returned only after the frozen provider acceptance gate passes.

## 14. Acceptance and telemetry

The frozen provider acceptance gate is normative.

The runner SHALL NOT assume exactly 339 callbacks.

PASS requires no provider failure state, callback ABI unwind, unknown tensor, type mismatch, dimension mismatch, element mismatch, byte mismatch, resident failure, object-integrity failure, payload-integrity failure, backend-copy failure, or accepted model after callback violation.

The result SHALL record at minimum:

- callback count;
- unique callback tensor names;
- duplicates;
- resolved object PK count;
- serialized-object reader call count;
- authorized persistent bytes read;
- backend tensor-copy count;
- provider failure state;
- provider failure type;
- acceptance-gate outcome.

## 15. Positive protected-I/O invariants

PASS SHALL establish:

- source GGUF opens: exactly 0;
- conventional complete GGUF files created: exactly 0;
- conventional GGUF loader calls: exactly 0;
- real `llama_model_init_from_user` calls: exactly 1;
- accepted real model handles: exactly 1;
- escaped real model handles: exactly 0;
- accepted-handle model frees: exactly 1;
- llama context creations: exactly 0;
- tokenization calls: exactly 0;
- prompt-evaluation calls: exactly 0;
- logits calls: exactly 0;
- inference calls: exactly 0;
- valid persistent MAF serialized-object reads: greater than 0;
- valid persistent MAF bytes read: greater than 0;
- unauthorized persistent segment opens: exactly 0.

## 16. Deterministic result artifact

A future frozen runner SHALL publish exactly one result at:

`experiments/model_fractal/maf_phase_6e_d_class_a_positive_model_load_validation_v1.json`

It SHALL be UTF-8 canonical JSON with sorted keys, compact separators, and no trailing newline.

The root SHALL contain at minimum:

- `schema`;
- `protocol_sha256`;
- `runner_sha256`;
- `provider_sha256`;
- `provider_git_blob`;
- `negative_result_sha256`;
- `metadata_authority_sha256`;
- `join_authority_sha256`;
- `generation_qualification_sha256`;
- `model_pk`;
- `generation_pk`;
- `llama_cpp_head`;
- `shared_library`;
- `metadata_reconstruction`;
- `tensor_declarations`;
- `protected_io`;
- `provider_execution`;
- `cleanup`;
- `summary`;
- `disposition`.

Publication SHALL be atomic and reopened byte-for-byte.

The result path SHALL be absent before execution.

An existing result prohibits a new execution.

## 17. PASS and FAIL disposition

The exact PASS disposition is:

`CLASS-A MAF-BACKED POSITIVE MODEL-LOAD VALIDATION PASS`

PASS requires every protocol invariant simultaneously.

Frozen-authority mismatch, metadata mismatch, tensor mismatch, source GGUF access, conventional GGUF creation, conventional loader use, wrong library identity, missing symbol, resident failure, unauthorized segment access, payload-integrity failure, callback violation, provider failure state, null model, acceptance failure, second user-init attempt, context creation, inference, cleanup failure, escaped handle, or noncanonical publication is FAIL.

A FAIL result remains authoritative for the spent execution.

No conventional GGUF fallback is permitted.

## 18. Claim boundary and future sequence

A PASS permits only this conclusion:

The frozen Class-A provider can construct and cleanly release one real llama.cpp model object using frozen in-memory GGUF metadata and qualified persistent MAF-backed tensor provisioning without reading the source GGUF or constructing a conventional complete GGUF model file.

It does not establish MAF-native compute, inference correctness, token parity, logits parity, output parity, output quality, memory superiority, latency superiority, throughput superiority, Phase 6E-D science completion, or Phase 6F readiness.

After this protocol is independently qualified and frozen:

1. construct the positive validation runner;
2. statically qualify it;
3. freeze it exactly;
4. perform one one-shot positive model-load validation;
5. independently qualify its result;
6. freeze that result;
7. construct a separate inference/parity protocol;
8. validate controlled inference correctness;
9. only then proceed to Phase 6E-D parity/quality science;
10. Phase 6F performance remains after correctness.

No positive execution is authorized merely by constructing this protocol.
