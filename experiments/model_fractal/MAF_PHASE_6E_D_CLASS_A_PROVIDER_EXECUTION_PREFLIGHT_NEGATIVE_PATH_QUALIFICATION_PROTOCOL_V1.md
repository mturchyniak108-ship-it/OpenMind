# MAF Phase 6E-D — Class-A Provider Execution Preflight and Negative-Path Qualification Protocol V1

## 1. Purpose

This protocol defines the first executable qualification gate for the frozen Phase 6E-D Class-A MAF-backed tensor provider.

This protocol is deliberately narrower than a valid Class-A treatment run.

It authorizes only:

1. provider import qualification;
2. shared-library discovery and symbol-binding preflight;
3. controlled fake-library and fake-tensor negative-path execution;
4. explicit fail-closed user-init boundary qualification;
5. proof that all negative cases avoid the persistent MAF segment and source GGUF.

It does not authorize a valid model load, valid persistent MAF payload transfer, inference, output-parity science, performance measurement, or Phase 6F.

## 2. Frozen authority bindings

OpenMind branch:

`labs/multidimensional-maf`

Protocol parent HEAD:

`a934c263bcdcbe82a9a3940ec43c78ede3f927b5`

Frozen provider:

`experiments/model_fractal/maf_phase_6e_d_class_a_maf_backed_tensor_provider_v1.py`

Provider SHA256:

`e436bbf14e34dfb1c46a6d947b66788fcf85fe3a0c9f8312ff3963ab6155e3ec`

Provider Git blob:

`14fa6be4a2cf69b8125e6540e0a808bd2758f792`

Provider contract SHA256:

`2782678c5153761e028f29f35d7275b019590af5a35391ea967c71c027c2ebb2`

Tensor to object to segment join authority SHA256:

`34aa1e85e3ee8090d4419dd5032f223eb2d0aecfc2009ad2a7625249b8bea709`

Class-A GGUF metadata authority SHA256:

`bdfe20b15732519c8fcbe253ff8598b829666a0227ce04420e2cb1888d626966`

Resident PK directory SHA256:

`4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6`

Segment reader SHA256:

`3499cb8e528fe8e9315e3e5656d6aa888c95ca175310b6371e722de409827369`

MAF object API SHA256:

`eed6cbd96995412a632883f3c534f9023e7711ea8eb437afe35a48312502f63b`

Pinned llama.cpp HEAD:

`4cf5cab65d5257be31e7623eb552b1861e969c75`

Qualified generation PK:

`mafgen:v1:74e506919d3418e2c540413cdcce72c35605195ef8efa36cdad4c56ad2a167d2`

Qualified model PK:

`mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258`

## 3. Protected payload authorities

Persistent segment path:

`results/runtime/maf_full_model_persistent_generation_v1/segment_00000000.mafseg`

Persistent segment length:

`1888934699`

Frozen segment SHA256 provenance:

`a930f1a1baae97279a3cbc50c1d126f3a70ef92d87f188f76747b2d7877109b9`

Inherited source GGUF SHA256 provenance:

`507de59046601282ba768a9789900e6ccf60ed93ddf346730b7c68eb0715bc47`

The segment SHA256 and source GGUF SHA256 SHALL NOT be recomputed by this qualification.

## 4. Authorization boundary for the future qualification runner

The future qualification runner SHALL be allowed to:

- read frozen tracked Python source and JSON authorities;
- import the exact frozen provider and its frozen MAF Python dependencies;
- inspect filesystem metadata for llama.cpp build artifacts;
- hash candidate llama.cpp shared-library artifacts;
- load one selected llama.cpp shared library using `ctypes.CDLL` for symbol-binding preflight only;
- resolve required exported symbols without calling real `llama_model_init_from_user`;
- instantiate `ResidentPKDirectory` without building a real active persistent snapshot;
- construct in-memory fake FFI callables and fake GGML tensor prefixes;
- execute the provider only against fake user-init behavior and an empty resident directory;
- monkeypatch `segment_reader.read_serialized_object` to a fail-if-called counter during negative tests;
- create one deterministic JSON qualification result.

The future qualification runner SHALL NOT:

- open or read the persistent `.mafseg`;
- call the real segment reader on a qualified persistent entry;
- open or read the source GGUF;
- call real `llama_model_init_from_user`;
- return or accept a real model handle;
- call `llama_init_from_model`;
- run inference;
- reconstruct a conventional GGUF;
- stage or commit Git changes;
- make network requests;
- perform Phase 6E-D output-parity science;
- perform Phase 6F performance work.

## 5. Forbidden-path audit guard

Before importing the provider, the qualification runner SHALL install an audit guard that observes file-open events.

The guard SHALL fail closed if any open attempt targets:

1. the exact protected persistent segment path;
2. the source GGUF path under the user home directory;
3. any alternate path resolving to the same protected segment inode if such an inode can be identified using metadata-only operations.

The runner SHALL separately monkeypatch the imported frozen `maf_segment_reader_v1.read_serialized_object` callable with a counter that raises immediately if invoked during any negative test.

Successful qualification requires:

- protected segment open count = `0`;
- source GGUF open count = `0`;
- real serialized-object reader call count = `0`.

## 6. Shared-library execution preflight

The runner SHALL inspect only shared-library artifacts located under the pinned llama.cpp checkout.

Candidate selection SHALL fail closed unless a regular shared-library artifact can be selected deterministically.

The selected artifact identity SHALL record:

- canonical path;
- byte length;
- SHA256;
- pinned llama.cpp HEAD.

Loading the shared library is authorized only for symbol-binding preflight.

The runner SHALL prove availability of the provider-required interface:

- `ggml_get_name`
- `ggml_nelements`
- `ggml_nbytes`
- `ggml_backend_tensor_set`
- `llama_model_default_params`
- `llama_model_init_from_user`
- `llama_model_free`

No real user-init call is authorized by this protocol.

If one shared-library handle does not expose the complete frozen provider interface, qualification SHALL fail. The runner SHALL NOT silently substitute a multi-library ABI that differs from the frozen implementation.

## 7. Provider import preflight

The runner SHALL import the exact provider SHA256 bound by this protocol.

Import qualification SHALL verify:

- provider module schema;
- provider contract SHA binding;
- join authority SHA binding;
- metadata authority SHA binding;
- model PK;
- generation PK;
- `EXPECTED_TENSOR_COUNT = 339`;
- `EXPECTED_MAF_HEADER_SIZE = 96`;
- `resident.OBJECT_PK_KIND = object_pk`.

Provider import alone SHALL NOT construct a real resident snapshot, read a persistent payload, or call llama user-init.

## 8. Fake-library requirements

Negative tests SHALL use a controlled in-memory fake library object.

Its callables SHALL support writable `argtypes` and `restype` attributes because the frozen provider binds them during initialization.

The fake library SHALL expose controlled implementations for:

- `ggml_get_name`;
- `ggml_nelements`;
- `ggml_nbytes`;
- `ggml_backend_tensor_set`;
- `llama_model_default_params`;
- `llama_model_init_from_user`;
- `llama_model_free`.

Every fake callable SHALL maintain an invocation counter.

The fake backend copy callable SHALL fail the qualification if invoked by a negative case that is expected to fail before payload transfer.

## 9. Negative-path matrix

### NP01 — Missing required FFI symbol

Construct the provider with a fake library missing one required symbol.

Expected result:

- `ClassAProviderAuthorityError`;
- provider construction fails closed;
- real user-init calls = `0`;
- backend tensor copies = `0`;
- serialized-object reads = `0`.

### NP02 — Null in-memory GGUF metadata pointer

Construct the provider with a complete fake library and empty `ResidentPKDirectory`.

Call `initialize_model` with a null metadata pointer.

Expected result:

- `ClassAProviderInitializationError`;
- fake default-params calls = `0`;
- fake user-init calls = `0`;
- fake model-free calls = `0`;
- backend tensor copies = `0`;
- serialized-object reads = `0`.

### NP03 — Fake user-init returns null without callbacks

Use a non-null fake metadata pointer.

Fake user-init returns null and invokes no callback.

Expected result:

- `ClassAProviderInitializationError`;
- fake user-init calls = `1`;
- callback count = `0`;
- fake model-free calls = `0`;
- serialized-object reads = `0`.

### NP04 — Non-null model returned with no callbacks

Fake user-init returns a non-null dummy model pointer and invokes no callback.

Expected result:

- `model_acceptance_gate` rejects the result;
- dummy model is freed exactly once;
- no model handle escapes;
- callback count = `0`;
- backend tensor copies = `0`;
- serialized-object reads = `0`.

### NP05 — Null callback tensor

Fake user-init invokes the frozen callback with a null tensor pointer and then returns a non-null dummy model pointer.

Expected result:

- provider failure state becomes true;
- failure type identifies a tensor contract failure;
- dummy model is freed exactly once;
- no exception unwinds through the ctypes callback ABI;
- no model handle escapes;
- backend tensor copies = `0`;
- serialized-object reads = `0`.

### NP06 — Unknown tensor name

Fake `ggml_get_name` returns a tensor name absent from the frozen 339-record authority.

Fake user-init invokes the callback with a non-null dummy tensor pointer and returns a non-null dummy model pointer.

Expected result:

- provider records a tensor-resolution failure;
- dummy model is freed exactly once;
- no model handle escapes;
- backend tensor copies = `0`;
- serialized-object reads = `0`.

### NP07 — Known tensor with wrong GGML type

Create an in-memory `_GGMLTensorPrefix` for one frozen tensor with:

- allocated-buffer field non-null;
- correct frozen dimensions;
- deliberately wrong GGML type.

Fake `ggml_get_name` returns the frozen tensor name.

Expected result:

- tensor type check fails before resident lookup;
- dummy model is freed exactly once;
- backend tensor copies = `0`;
- serialized-object reads = `0`.

### NP08 — Valid tensor metadata with empty resident directory

Create an in-memory `_GGMLTensorPrefix` matching one frozen tensor.

Fake introspection SHALL return:

- exact frozen name;
- exact frozen GGML type;
- exact frozen dimensions;
- exact frozen element count;
- exact frozen payload byte count.

The provider SHALL use an empty `ResidentPKDirectory`.

Expected result:

- logical tensor resolution succeeds;
- resident `object_pk` lookup fails closed;
- real serialized-object reader is never invoked;
- backend tensor copies = `0`;
- dummy model is freed exactly once;
- no model handle escapes.

### NP09 — One-shot initialization guard

After any first `initialize_model` attempt, call `initialize_model` again on the same provider.

Expected result:

- `ClassAProviderInitializationError`;
- second fake user-init call count increment = `0`;
- second callback count increment = `0`;
- second backend-copy increment = `0`;
- serialized-object reads = `0`.

## 10. Negative-path global invariants

Every NP case SHALL prove all applicable invariants.

A failure is not qualified merely because an exception occurred.

The runner SHALL verify:

- exact expected exception class;
- exact user-init invocation count;
- exact callback count;
- exact model-free count;
- exact backend-copy count;
- exact serialized-object-reader count;
- provider failure-state disposition;
- no returned model handle;
- no protected `.mafseg` open;
- no source GGUF open.

Any silent fallback, substitute data, zero-fill behavior, conventional-GGUF path, or accepted model after a provider violation is an immediate qualification failure.

## 11. Real-library boundary

The real selected llama.cpp shared library may be loaded and its symbols bound.

The real `llama_model_init_from_user` symbol SHALL NOT be called in this protocol.

Therefore this protocol does not establish:

- successful model allocation;
- successful callback delivery by real llama.cpp;
- valid MAF payload transfer;
- successful model construction;
- inference correctness;
- output parity.

Those remain future gates.

## 12. Qualification result requirements

The future runner SHALL emit canonical JSON with no trailing newline.

Required root fields include:

- `schema`;
- `protocol_sha256`;
- `provider_sha256`;
- `provider_git_blob`;
- `llama_cpp_head`;
- `shared_library`;
- `protected_io`;
- `negative_tests`;
- `summary`;
- `disposition`.

Each negative-test record SHALL include:

- test ID;
- expected failure class;
- observed failure class;
- user-init calls;
- callback calls;
- model-free calls;
- backend-copy calls;
- serialized-object-reader calls;
- model-handle escaped;
- pass boolean.

The summary SHALL include:

- negative tests expected = `9`;
- negative tests passed;
- segment opens = `0`;
- source GGUF opens = `0`;
- serialized-object-reader calls = `0`;
- real llama user-init calls = `0`;
- real model loads = `0`;
- inference calls = `0`.

## 13. Required disposition

A complete PASS may establish only:

`CLASS-A PROVIDER EXECUTION PREFLIGHT + NEGATIVE-PATH QUALIFICATION PASS`

A PASS SHALL NOT authorize Phase 6E-D science.

After PASS and exact result freeze, the next gate is a separately frozen positive Class-A model-load validation protocol.

That future positive protocol must explicitly authorize the first valid persistent `.mafseg` reads and real `llama_model_init_from_user` invocation.

## 14. Required future sequence

1. Freeze this protocol.
2. Construct the negative-path qualification runner.
3. Static-qualify the runner.
4. Freeze the runner.
5. Execute the runner under this protocol.
6. Qualify and freeze its result.
7. Freeze a positive Class-A model-load validation protocol.
8. Only then authorize the first valid persistent MAF payload read through the provider.
9. Validate real model construction.
10. Validate inference.
11. Only after correctness: Phase 6E-D output parity and quality science.
12. Only after correctness: Phase 6F performance work.

## 15. Frozen claim boundary

This protocol is a qualification protocol for execution safety and failure propagation.

It does not claim MAF-native compute.

It does not claim output parity.

It does not claim lower memory use.

It does not claim higher performance.

It does not authorize a source GGUF read.

It does not authorize a persistent MAF payload read.

It does not authorize a real model load.
