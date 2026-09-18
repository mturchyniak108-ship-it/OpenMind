# MAF Phase 6E-D Class-A Inference / Logit-Parity Validation Protocol V1

## Status

PREREGISTERED PROTOCOL — EXECUTION NOT AUTHORIZED BY THIS DOCUMENT CONSTRUCTION STEP.

This protocol defines the correctness successor to the frozen qualified Class-A positive model-load PASS.

It asks whether a model loaded directly from serialized MAF tensor objects produces tokenization identical to, and numerically equivalent last-token full-vocabulary logits to, the same model loaded conventionally from the original full GGUF under the same pinned llama.cpp runtime.

All pass/fail criteria are prospective and fixed before runner construction or science execution.

## 1. Frozen predecessor authority

- branch: labs/multidimensional-maf
- protocol-construction parent HEAD: a34e8f3e541cd0d4e54ca9c544aa52dd1a64d537
- frozen V4 runner SHA256: a0c419924ba561b5ef51b1903a4c69bc4a7490b2bc55f3eb4973b634c381008d
- frozen V4 PASS result SHA256: e0903000538df22f61d3b2bff5b97b67b798d742e856b08ecab0b4520daa0d08
- frozen V4 result Git blob: 6eb7b87f827d0c7efaca9521e7442ae799fb0f26
- V4 policy status: SPENT / NEVER RERUN
- V4 provider callbacks: 339
- V4 resolved tensors: 339
- V4 transferred tensors: 339
- V4 accepted model handles: 1
- V4 source GGUF opens: 0
- V4 conventional-loader calls: 0
- V4 inference calls: 0

V4 is lineage/evidence authority only and must never be rerun.

## 2. Frozen Class-A treatment authority

- provider SHA256: e436bbf14e34dfb1c46a6d947b66788fcf85fe3a0c9f8312ff3963ab6155e3ec
- provider Git blob: 14fa6be4a2cf69b8125e6540e0a808bd2758f792
- metadata authority SHA256: bdfe20b15732519c8fcbe253ff8598b829666a0227ce04420e2cb1888d626966
- tensor/object/segment join SHA256: 34aa1e85e3ee8090d4419dd5032f223eb2d0aecfc2009ad2a7625249b8bea709
- generation manifest SHA256: a79b012f10904a5e0540076a8443007344ada4e11e3846d817201b43583fedff
- persistent MAF segment: results/runtime/maf_full_model_persistent_generation_v1/segment_00000000.mafseg
- persistent segment bytes: 1888934699
- persistent segment SHA256 authority: a930f1a1baae97279a3cbc50c1d126f3a70ef92d87f188f76747b2d7877109b9
- tensor count: 339

Treatment must not reconstruct a complete GGUF and must not fall back to the source GGUF.

## 3. Frozen native runtime

- llama.cpp HEAD: 4cf5cab65d5257be31e7623eb552b1861e969c75
- llama.h SHA256: db39eaf53de25f88d0803f5a1eb77206ee86d4e3c968dd54a83690cb021b8cda
- libllama path: /data/data/com.termux/files/home/llama.cpp-openmind-phase6ed-optional-v1-build-vulkan/bin/libllama.so.0.0.10318
- libllama bytes: 3613896
- libllama SHA256: a56bdf41b3409ae870c584ecf23e7e65915451ae313d057d92958be0d94af802
- runtime policy: SELF-CONTAINED-RUNPATH

Required primitives:

- llama_context_default_params
- llama_init_from_model
- llama_free
- llama_model_get_vocab
- llama_tokenize
- llama_batch_get_one
- llama_decode
- llama_synchronize
- llama_get_logits_ith
- llama_vocab_n_tokens
- llama_model_load_from_file
- llama_model_free

Exact ABI signatures must be qualified from the pinned header before runner freeze.

## 4. Scientific question

Under identical runtime, model parameters, context parameters, prompt bytes, tokenization flags, and decode procedure, does the Class-A MAF-backed treatment produce exact token parity and numerically equivalent full-vocabulary logits to the original-GGUF conventional control?

This is inference-correctness parity science only.

## 5. Treatment

The future one-shot treatment must:

1. use the frozen Class-A metadata/resident/provider chain;
2. resolve and transfer all 339 tensors from serialized MAF objects;
3. invoke llama_model_init_from_user exactly once;
4. obtain exactly one non-null model handle;
5. perform zero source-GGUF opens;
6. perform zero conventional loader calls;
7. keep the accepted treatment handle alive through the preregistered inference probe;
8. free treatment context and model before control load begins.

## 6. Conventional control

Original GGUF authority:

- path: /data/data/com.termux/files/home/qwen2.5-coder-q8_0.gguf
- bytes authority: 1894532160
- SHA256 authority: 507de59046601282ba768a9789900e6ccf60ed93ddf346730b7c68eb0715bc47

Source GGUF access is prohibited during protocol construction, qualification, freeze, runner construction, and preflight.

Only inside the later separately authorized one-shot science runner:

1. treatment inference and cleanup finish first;
2. source identity is verified against the frozen SHA;
3. llama_model_load_from_file exactly once is invoked;
4. the same pinned libllama and matching model parameters are used;
5. exactly one non-null control model handle is required;
6. control must not use the MAF provider or MAF segment;
7. control context/model resources are freed exactly once.

Treatment and control models must never be simultaneously live.

## 7. Frozen prompt

Exact UTF-8 text:

```text
OpenMind MAF parity probe.
Given integers 17 and 25, compute their sum and explain the result in one sentence.
```

- UTF-8 bytes: 110
- ASCII-only: true
- SHA256: a79091472f58689a015e1e38947f9713fb9542211db99d2c911e41d58b40acfd

The prompt cannot change after runner freeze.

## 8. Tokenization

Each arm independently tokenizes the exact prompt with:

- add_special: false
- parse_special: false
- no chat template
- no runner-added BOS
- no runner-added EOS
- no sampling
- no generated tokens

Hard PASS requirements:

1. both tokenizations succeed;
2. token count is greater than zero;
3. token count is less than 128;
4. token counts are exactly equal;
5. every token ID is exactly equal by position.

A token mismatch is immediate scientific FAIL.

Both token vectors and canonical hashes must be recorded.

## 9. Context parameters

Start from llama_context_default_params and explicitly set:

- n_ctx: 128
- n_batch: 128
- n_ubatch: 128
- n_seq_max: 1
- n_threads: 1
- n_threads_batch: 1

All other fields remain runtime defaults.

Treatment/control context parameter values must be identical.

## 10. Decode procedure

For each arm:

1. obtain vocabulary;
2. tokenize the frozen prompt;
3. create exactly one context;
4. create one full-prompt single-sequence batch;
5. execute exactly one llama_decode call;
6. require decode return code zero;
7. call llama_synchronize;
8. access last-token logits with llama_get_logits_ith index -1;
9. obtain vocabulary length with llama_vocab_n_tokens;
10. copy the complete vector into runner-owned memory;
11. require every logit finite;
12. free the context exactly once.

Expected vocabulary/logit length: 151936.

No retry, second decode, generation loop, sampling, or generated token is permitted.

## 11. Per-arm logit evidence

The per-arm comparison vector is exactly the complete vocabulary-length logit vector corresponding to the final token of the frozen prompt after that arm's single preregistered decode.

The runner MUST compare every vocabulary element from that final prompt-token vector. It MUST NOT substitute logits from an earlier prompt position, an aggregate across positions, a top-k subset, sampled output, or generated-token logits.

The final prompt-token vector MUST be obtained through the pinned native logits API after the arm's decode/synchronization and copied while that arm's context/model are still live, before cleanup.

Machine-audit scope: FULL_VOCABULARY_FINAL_PROMPT_TOKEN.
Machine-audit prohibited substitutes: EARLIER_TOKEN, AGGREGATE, TOP_K, SAMPLED, GENERATED_TOKEN.
Machine-audit lifetime order: DECODE -> SYNCHRONIZE -> COPY_FULL_LOGIT_VECTOR -> CONTEXT_FREE -> MODEL_FREE.

Record:

- vocabulary length;
- float element count;
- canonical little-endian float32 SHA256;
- minimum;
- maximum;
- arithmetic mean;
- L2 norm;
- argmax token ID/value;
- ordered top-10 token IDs/values;
- non-finite count.

No value may be rounded before comparison.

## 12. Numerical parity

For each vocabulary element i:

```text
absolute_error_i = abs(T_i - C_i)
allowed_error_i  = 1e-5 + 1e-5 * abs(C_i)
```

Every element must satisfy:

```text
absolute_error_i <= allowed_error_i
```

Frozen comparison:

- absolute tolerance: 1e-5
- relative tolerance: 1e-5
- NaN equality: false

Also record:

- exact-equality count;
- maximum absolute error;
- mean absolute error;
- RMSE;
- maximum relative error with safe nonzero denominator;
- cosine similarity;
- treatment/control argmax IDs;
- treatment/control ordered top-10 IDs.

Hard PASS requirements:

1. exact token parity;
2. exact vector-length parity;
3. all values finite;
4. every logit satisfies the fixed tolerance;
5. treatment/control argmax token IDs are identical.

Tolerance may never be widened after observation.

## 13. Frozen experiment order

1. verify frozen authorities;
2. reserve a distinct SHA-derived successor sentinel;
3. load treatment from MAF;
4. qualify 339/339 provisioning;
5. tokenize treatment;
6. create treatment context;
7. decode treatment exactly once;
8. synchronize/copy treatment logits;
9. free treatment context;
10. free treatment model;
11. verify no treatment handle escape;
12. verify control source identity;
13. load control via llama_model_load_from_file exactly once;
14. tokenize control;
15. require exact token parity;
16. create control context;
17. decode control exactly once;
18. synchronize/copy control logits;
19. free control context;
20. free control model;
21. compare preregistered logit evidence;
22. publish one result artifact;
23. never rerun that successor version after launch.

## 14. Failure semantics

Scientific FAIL includes any:

- authority mismatch;
- pre-existing successor sentinel/result;
- treatment source-GGUF access;
- treatment conventional-loader call;
- callback/resolution/transfer count other than 339;
- null treatment/control model;
- provider failure;
- prompt mismatch;
- tokenization/token parity failure;
- context creation failure;
- decode nonzero return;
- null logit pointer;
- vocabulary/vector length mismatch;
- non-finite logit;
- tolerance violation;
- argmax mismatch;
- control GGUF identity mismatch;
- control loader count other than one;
- control MAF/provider access;
- resource leak/escaped handle;
- result publication failure after one-shot launch.

Any unexpected exception, ABI/API failure, telemetry inconsistency, unclassified integrity violation, or inability to prove a required PASS condition is Scientific FAIL. The runner MUST fail closed; missing, ambiguous, or unproven required evidence may never be converted to PASS.

Any launched runner version is spent. Correction requires a distinct version, new SHA, and new sentinel.

## 15. Required telemetry

Treatment:
- user-init calls;
- accepted models;
- callbacks/resolutions/transfers;
- serialized MAF reads/bytes;
- source-GGUF opens;
- conventional-loader calls;
- context/tokenize/decode/synchronize/logits calls;
- context/model frees;
- escaped handles.

Control:
- source identity reads/bytes;
- conventional-loader calls;
- accepted models;
- MAF/provider calls;
- MAF segment reads;
- context/tokenize/decode/synchronize/logits calls;
- context/model frees;
- escaped handles.

Comparison:
- prompt bytes/SHA;
- token vectors/hashes;
- vocabulary size;
- canonical logit hashes;
- exact-equality count;
- max/mean absolute error;
- RMSE;
- max relative error;
- cosine similarity;
- argmax IDs;
- top-10 IDs;
- all-close outcome;
- final parity outcome.

## 16. Cleanup

PASS requires final:

- zero live treatment contexts/models;
- zero live control contexts/models;
- zero escaped native handles;
- temporary metadata resources released exactly once where applicable.

Cleanup evidence is part of the PASS gate.

## 17. Permitted dispositions

```text
CLASS-A MAF-BACKED INFERENCE LOGIT-PARITY VALIDATION PASS
CLASS-A MAF-BACKED INFERENCE LOGIT-PARITY VALIDATION FAIL
```

Process return code alone is never scientific evidence.

## 18. Bounded supported claim after PASS

A qualified and frozen PASS supports only:

Under the pinned llama.cpp runtime and preregistered prompt/decode procedure, the complete 339-tensor model loaded directly from serialized MAF objects produced tokenization identical to, and full-vocabulary last-token logits numerically equivalent to, the same model loaded conventionally from its original full GGUF.

It does not establish:

- open-ended generation quality;
- semantic answer quality;
- multi-token autoregressive parity;
- long-context parity;
- sampling parity;
- throughput/latency/memory advantage;
- selective working-set inference;
- MAF-native compute;
- architecture independence;
- equivalence for other models/prompts/runtimes/devices/quantizations.

## 19. Performance isolation

No timing from this experiment may support performance claims.

Performance remains Phase 6F after correctness closure.

## 20. Successor governance

The future science runner must:

- be a distinct new file/version;
- have a frozen SHA;
- use a fresh SHA-derived one-shot sentinel;
- use a new result path;
- undergo independent static qualification;
- undergo exact one-file freeze;
- undergo read-only execution preflight;
- execute exactly once after explicit authorization;
- never retry after launch.

No inference science is authorized merely by constructing or freezing this protocol.

## 21. Planned protocol freeze subject

```text
research: preregister Phase 6E-D Class-A inference logit parity validation
```

Git staging, commit, and push are outside this construction authorization.
