# OpenMind Phase 6E-D Class-A User-Init Optional-Tensor Compatibility Protocol V1

## Status

Versioned construction protocol for the next Class-A model-load integration attempt.

This protocol does not authorize model inference, parity science, performance science, source GGUF reads, or rerun of the spent V1 positive model-load experiment.

## Frozen OpenMind authority

- Branch: `labs/multidimensional-maf`
- Parent HEAD: `a8f5b1efc92e89296a082160ca70d4eaf9db9a99`
- Spent V1 runner SHA256: `1038af1611bf94e5e7bc176fef21894ca1cf2b8d5099523562779272239bac08`
- Spent V1 runner Git blob: `2c553765c6613a17016bbb4d49ac235d61ac3db3`
- Frozen V1 failure result SHA256: `db6e187e73aeaa5dbca12fe997ac364943b32e19aac0d76c8013f507b665317b`
- Frozen V1 failure result Git blob: `4fe607f638d7dc6b2ffa39ef14a9b4e7796172d9`
- Frozen Provider V1 SHA256: `e436bbf14e34dfb1c46a6d947b66788fcf85fe3a0c9f8312ff3963ab6155e3ec`
- Frozen Provider V1 Git blob: `14fa6be4a2cf69b8125e6540e0a808bd2758f792`
- Frozen provider contract SHA256: `2782678c5153761e028f29f35d7275b019590af5a35391ea967c71c027c2ebb2`
- Frozen metadata authority SHA256: `bdfe20b15732519c8fcbe253ff8598b829666a0227ce04420e2cb1888d626966`
- Frozen tensor-object-segment join SHA256: `34aa1e85e3ee8090d4419dd5032f223eb2d0aecfc2009ad2a7625249b8bea709`
- Frozen source tensor inventory SHA256: `7acf6d5dc672182aee0244b1bb85a47466f33dbdcdf10bde863e24f3659240ee`

The spent V1 runner, result, and sentinel are immutable historical authorities. They MUST NOT be modified or rerun.

## Pinned llama.cpp base authority

- Base HEAD: `4cf5cab65d5257be31e7623eb552b1861e969c75`
- Loader: `src/llama-model-loader.cpp`
- Loader SHA256: `73f87966e648493b5b9687aced2253903a7bb03bf3a7bdd5596bac3578330e7a`
- Loader Git blob: `71bc9f7ef0aaa883f046537c0a28803bdb39754d`
- Qwen2 source: `src/models/qwen2.cpp`
- Qwen2 SHA256: `0da43ff61f449be3a3da8ca2e7cc0eee119b4b8e07c8accce0041998241824e8`
- Qwen2 Git blob: `e9c2ea80a6bec381f2d432357ab00e6c4494ddf6`
- User-init source: `src/llama.cpp`
- User-init SHA256: `8fa22037f00c14f04492d76658b1b2075b479477039c18d6bc76c52bfc9031db`
- User-init Git blob: `d6e0bbfefa729329fe6b83e46e603a85dab0f2e3`

The base checkout `~/llama.cpp` MUST remain unmodified.

## Frozen V1 observation

The authoritative V1 attempt performed one real user-init path, three qualified MAF reads, three backend tensor copies, zero source GGUF opens, zero unauthorized segment opens, zero llama contexts, and zero inference calls.

It failed closed on:

`callback tensor is absent from frozen authority: output.bias`

This is a valid frozen negative integration result and MUST NOT be reinterpreted as PASS.

## Established root cause

Pinned Qwen2 declares both `output.weight` and `output.bias` with `TENSOR_NOT_REQUIRED`.

The frozen source authority contains `output.weight` and legitimately omits `output.bias`.

In conventional loading, an absent optional tensor is permitted to resolve to `NULL` through `check_tensor_dims`.

In the `files.empty()` user-init branch, metadata presence is checked with `gguf_find_tensor`, but tensor id `-1` does not itself suppress a valid-dimension optional tensor. The branch synthesizes a ggml tensor and later `load_all_data` invokes `set_tensor_data` for every created tensor.

Therefore absent optional `output.bias` is synthesized and callback-visible even though no source tensor exists.

For Qwen2, `output_b` is pointer-conditional and additive. Conventional source semantics for this model require `output_b == nullptr`.

## Normative compatibility rule

V2 MUST PRESERVE CONVENTIONAL OPTIONAL-TENSOR ABSENCE.

When `files.empty()` is true and `gguf_find_tensor(metadata, tensor_name)` returns `-1` while `TENSOR_NOT_REQUIRED` is set, `llama_model_loader::create_tensor` MUST return `nullptr` before buffer selection, synthetic ggml tensor creation, allocation, or callback enumeration.

Required semantic condition:

```cpp
const int64_t tid = gguf_find_tensor(metadata, tn.str().c_str());

if (tid == -1 && (flags & TENSOR_NOT_REQUIRED)) {
    return nullptr;
}
```

Exact formatting is not normative. Observable semantics are normative.

## Preservation requirements

The compatibility change MUST preserve:

1. `TENSOR_SKIP_IF_VIRTUAL` behavior.
2. Required-tensor fail-closed behavior.
3. Tensor type recovery for metadata-present tensors.
4. Metadata-present optional tensors.
5. `TENSOR_DUPLICATED` behavior.
6. `TENSOR_ALLOW_RESHAPE` behavior.
7. Buffer selection for source-present tensors.
8. Backend allocation for source-present tensors.
9. The public `llama_model_init_from_user` ABI.
10. Forced `LLAMA_LOAD_MODE_NONE`.
11. `params.use_extra_bufts = false`.
12. Ordinary llama model construction after source tensors are resolved.

Missing required tensors MUST NOT be silently suppressed.

## MAF authority rule

V2 MUST NOT add, invent, fabricate, synthesize, zero-fill, or otherwise create a MAF payload for `output.bias`.

`output.bias` is absent from source authority. Its absence is authoritative.

Provider V1 SHOULD remain unchanged. It MUST continue to reject any callback tensor that cannot resolve exactly to frozen MAF authority.

## Compatibility source isolation

The pinned base checkout MUST remain untouched.

Any compatibility implementation MUST be created in an isolated worktree or source tree derived exactly from llama.cpp HEAD `4cf5cab65d5257be31e7623eb552b1861e969c75`.

The preferred source diff is one tracked file only: `src/llama-model-loader.cpp`.

A wider source diff requires a new frozen protocol amendment before execution.

## Compatibility build isolation

The V2 library MUST use a dedicated build directory and MUST NOT overwrite or replace the frozen V1 library.

Before model-load use, the compatibility library authority MUST freeze its source ancestry, exact diff, source SHA, build path, library bytes, library SHA256, required exports, and Vulkan availability.

## V2 runner requirements

The V2 runner MUST be a new artifact and MUST have a new runner-SHA-bound one-shot sentinel.

Recommended paths:

- `experiments/model_fractal/maf_phase_6e_d_class_a_positive_model_load_validation_v2.py`
- `experiments/model_fractal/maf_phase_6e_d_class_a_positive_model_load_validation_v2.json`

The V1 execution slot MUST NOT be reused.

## V2 model-load PASS criteria

A PASS requires:

- exactly one real `llama_model_init_from_user` call;
- exactly one accepted non-null model;
- exactly one accepted-model free;
- zero escaped model handles;
- zero source GGUF opens;
- zero conventional complete-GGUF creation;
- zero conventional GGUF loader calls;
- positive authorized serialized MAF reads;
- positive authorized persistent MAF bytes;
- positive backend tensor copies;
- zero unauthorized persistent-segment opens;
- no callback request for `output.bias`;
- no callback for any tensor absent from frozen MAF authority;
- provider acceptance PASS;
- provider failure state false;
- zero contexts, tokenization, eval, logits, and inference;
- canonical atomic result publication;
- permanently spent V2 sentinel.

Callback count MUST NOT be assumed to equal 339. Every actual callback must resolve exactly to frozen source-derived MAF authority.

## Failure semantics

Any failure after V2 sentinel reservation permanently spends that V2 slot.

A failed V2 execution MUST NOT be rerun.

A failure result MUST be independently qualified and frozen before another compatibility version is designed.

## Claim boundary

A successful V2 model-load validation may establish only that native llama model construction can consume the qualified MAF-backed provider while legitimately absent optional source tensors remain absent.

It MUST NOT establish output parity, tokenization parity, logits parity, generation parity, inference quality, MAF-native compute, performance improvement, memory improvement, Phase 6E-D scientific closure, or Phase 6F conclusions.

## Required sequence

1. Independently qualify this protocol.
2. Freeze this protocol in one exact-file commit.
3. Construct an isolated compatibility patch.
4. Independently qualify and freeze the exact patch authority.
5. Build in a dedicated compatibility build directory.
6. Qualify and freeze the compatibility library authority.
7. Construct, qualify, and freeze a new V2 positive runner.
8. Perform a V2 post-freeze one-shot preflight.
9. Execute exactly one V2 model-load attempt.
10. Qualify and freeze its result.
11. Only after model-load PASS, draft a separate inference/parity protocol.

## Final invariant

MAF supplies source-authoritative tensor payloads.

A source tensor that is legitimately absent and optional MUST remain absent.

Compatibility MUST preserve architecture semantics instead of fabricating missing source tensors.
