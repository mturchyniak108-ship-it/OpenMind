# MAF Encoder V1 Protocol

Status: experimental protocol pending implementation validation.

Schema:

`openmind.maf_encoder.v1`

Encoder version:

`maf_encoder_v1`

## 1. Purpose

MAF Encoder V1 defines the execution boundary between the
pre-payload Planner and the persistent MAF Object V1 compiler.

The compiler pipeline is:

`Scanner -> Classifier -> Planner -> Encoder -> Segment Builder`

The Planner emits deterministic compile intent.

The Encoder is the first stage permitted to access source tensor
payload bytes.

MAF Encoder V1 executes only the exact conservative recipe frozen
for Phase 6A.

It does not make new planning decisions.

## 2. V1 execution model

The V1 execution path is:

frozen compile recipe
+
validated physical tensor record
+
source model path
+
output object path

→ validate logical/physical agreement

→ enforce frozen recipe policy

→ stream source tensor payload once

→ calculate/verify SHA256 during that stream

→ write exact persistent MAF Object V1

→ independently reopen the new MAF object

→ atomically activate the completed object

The source GGUF tensor payload must not require a second payload
pass during encoding.

Independent validation of the newly written MAF object is not a
second source payload pass.

## 3. Frozen dependencies

Encoder V1 is downstream of:

- MAF Identity V1;
- MAF Metadata Classification V1;
- MAF Compile Recipe V1;
- MAF Object V1.

V1 must reuse the existing exact MAF Object V1 persistence
primitive unless a separately frozen protocol authorizes a new
object format.

The existing object compiler is:

`maf_object_v1.compile_object()`

Encoder V1 must not duplicate the exact object persistence format
without an explicit protocol revision.

## 4. Recipe inputs

Encoder V1 requires one valid compile recipe with schema:

`openmind.maf_compile_recipe.v1`

The recipe supplies logical compile intent including:

- model PK;
- object PK;
- tensor name;
- tensor type;
- dims;
- elements;
- source encoding;
- target representation;
- fidelity requirement;
- payload access policy;
- payload pass count;
- hash policy;
- transform policy;
- compression policy;
- deduplication policy;
- fragmentation policy;
- dense materialization policy;
- segment placement policy;
- runtime residency policy;
- MAF-native compute policy;
- unresolved decisions.

The Encoder must preserve the supplied model PK and object PK as
logical context.

It must not regenerate them.

## 5. Physical tensor input

Encoder V1 may consume a frozen physical tensor record containing:

- tensor name;
- tensor type;
- dims;
- element count;
- source file start;
- source tensor span in bytes;
- expected payload SHA256.

For the frozen GGUF inventory these correspond to:

- `name`
- `type`
- `dims`
- `elements`
- `file_start`
- `span_bytes`
- `payload_sha256`

The Encoder may also receive the source model path separately.

Physical source placement is execution information.

It is not logical object identity.

## 6. Required pre-payload agreement

Before opening the source model payload, Encoder V1 must verify
that recipe and physical tensor record agree on:

- tensor name;
- tensor type;
- dims;
- element count.

A mismatch must fail before payload streaming begins.

The Encoder must also validate:

- source file start is a non-negative integer;
- source tensor span is a non-negative integer;
- expected payload SHA256 is valid lowercase SHA256 text;
- output path is suitable for MAF Object V1 compilation.

## 7. Required V1 recipe policy

Encoder V1 accepts only the frozen conservative policy:

`source_encoding = gguf_payload_exact`

`target_representation = persistent_maf_object_exact`

`fidelity_requirement = exact`

`payload_access = deferred_to_encoder`

`payload_passes = 1`

`hash_policy = sha256_stream_required`

`transform_policy = none`

`compression_policy = none`

`deduplication_policy = unresolved`

`fragmentation_policy = none`

`dense_materialization_policy = optional_compute_view`

`segment_placement_policy = unresolved`

`runtime_residency_policy = unresolved`

`maf_native_compute_policy = disabled_unvalidated`

The unresolved list must remain exactly:

- deduplication;
- structural optimization;
- segment placement;
- runtime residency;
- MAF-native compute.

Unsupported or altered policies must be rejected.

The Encoder must not silently reinterpret them.

## 8. Source payload access

Encoder V1 is permitted to open the source model only after all
pre-payload validation succeeds.

For one tensor encode operation, the source tensor payload must be
traversed once.

The Encoder must not perform:

- a preliminary payload digest pass;
- a separate transform pass;
- a separate compression pass;
- a separate fragment discovery pass;
- a second source comparison pass during encoding.

The exact source payload SHA256 must be calculated or verified
while the payload is streamed to the persistent object.

## 9. Bounded streaming

Whole-tensor temporary payload allocations are prohibited.

The Encoder must use bounded chunked I/O.

MAF Object V1 currently defines:

`DEFAULT_CHUNK_BYTES = 4 * 1024 * 1024`

Encoder V1 may expose a bounded chunk-size parameter.

Changing chunk size must not change logical identity, recipe
meaning, object payload bytes, or payload digest.

Chunk size is an execution parameter only.

## 10. Exact fidelity

V1 performs no numerical transformation.

The source tensor payload bytes must be copied exactly.

The expected relationship is:

source GGUF tensor byte span
=
stored MAF Object V1 payload byte span

The stored payload digest must equal the frozen expected payload
SHA256.

Any digest mismatch must fail compilation.

## 11. Object persistence

Encoder V1 must preserve the MAF Object V1 persistence guarantees:

- sibling `.partial` creation;
- exclusive creation of the partial object;
- bounded payload streaming;
- payload SHA256 while streaming;
- exact copied-byte count;
- target flush;
- target `fsync`;
- independent reopen and validation of the new object;
- atomic `os.replace` activation;
- partial cleanup on failure.

Existing completed output objects must not be silently
overwritten.

## 12. Independent reopen

After source streaming is complete, the new `.partial` MAF object
may be independently reopened and fully validated.

This validation may reread the MAF object payload.

It must not require reopening or rereading the source GGUF tensor
payload.

Therefore:

one source payload pass

does not mean

one total read of every byte in every persistence artifact.

The contract applies specifically to the source tensor payload
during encoding.

## 13. Provenance

Encoder V1 may attach provenance supported by MAF Object V1.

Provenance must not redefine logical identity.

At minimum, Encoder validation should be able to associate an
encode operation with:

- model PK;
- object PK;
- recipe schema;
- planner version;
- Encoder schema;
- Encoder version.

However, MAF Encoder V1 must not require changes to the frozen MAF
Object V1 metadata schema merely to persist these fields.

If provenance is persisted, it must use the existing optional
MAF Object V1 provenance field.

## 14. Identity boundary

Encoder V1 must not generate:

- model PKs;
- object PKs;
- fragment PKs.

It consumes existing model/object identity.

Physical source fields such as:

- file path;
- file start;
- tensor offset;
- span bytes;
- output path;
- chunk size;

must not change logical PKs.

## 15. Fragmentation

V1 requires:

`fragmentation_policy = none`

The Encoder must not create operational fragments.

It must not generate fragment PKs.

Fragment identity remains a separately validated logical
primitive without an operational fragmentation scheme.

## 16. Transformation and compression

V1 requires:

`transform_policy = none`

and:

`compression_policy = none`

The Encoder must not:

- requantize;
- dequantize;
- transpose;
- reorder numerical elements;
- repack quantization blocks;
- compress payload bytes;
- rewrite payload representation.

The exact source byte representation is the persistent V1
representation.

## 17. Deduplication

V1 requires:

`deduplication_policy = unresolved`

Encoder V1 does not perform payload deduplication.

Equal payload hashes do not authorize shared logical identity or
shared persistent storage.

## 18. Dense materialization

The recipe declares:

`dense_materialization_policy = optional_compute_view`

Encoder V1 does not materialize dense compute tensors.

Dense materialization belongs to later runtime/compute layers.

## 19. Segment placement

The recipe declares:

`segment_placement_policy = unresolved`

Encoder V1 produces or activates an individual MAF Object V1 at
the caller-provided output path.

This is not a Segment Builder placement decision.

Encoder V1 must not assign:

- immutable segment generation;
- catalog segment ID;
- segment-relative object offset;
- locality generation;
- route placement.

Those belong downstream.

## 20. Runtime residency

The recipe declares:

`runtime_residency_policy = unresolved`

Encoder V1 must not assign:

- COLD_DISK;
- MAPPED;
- HOT_MAF;
- HOT_DENSE;
- VULKAN_MAF;
- cache priority;
- pin state;
- device placement.

Residency belongs to Phase 6C.

## 21. MAF-native compute

The recipe declares:

`maf_native_compute_policy = disabled_unvalidated`

Encoder V1 does not perform inference or numerical kernels.

Successful encoding does not establish MAF-native compute
correctness.

## 22. Failure behavior

Encoder V1 must fail closed on:

- malformed recipe;
- unsupported recipe schema;
- unsupported Encoder policy;
- recipe/physical metadata disagreement;
- invalid physical source span;
- invalid expected payload digest;
- source span outside file bounds;
- short source read;
- copied byte-count mismatch;
- source payload digest mismatch;
- object reopen validation failure;
- pre-existing final output;
- pre-existing partial output.

A failed encode must not leave an activated final object.

Partial cleanup behavior must remain consistent with MAF Object
V1.

## 23. Required validation

Before Encoder V1 is considered validated, a preregistered
validation must prove at minimum:

- recipe policy is enforced;
- existing model PK is preserved;
- existing object PK is preserved;
- identity is not regenerated;
- recipe/physical mismatches fail before payload streaming;
- source payload is streamed once;
- hash is updated during the source stream;
- bounded chunks are used;
- no whole-tensor temporary payload allocation is used;
- no transform occurs;
- no compression occurs;
- no deduplication occurs;
- no operational fragments are created;
- no fragment PK is generated;
- no Segment Builder placement is assigned;
- no runtime residency is assigned;
- no MAF-native compute is enabled;
- exact payload digest matches;
- persistent object independently reopens;
- failure does not activate a final object;
- completed object remains usable without the source model.

## 24. Initial validation scope

The first Encoder validation should use a representative subset
of the frozen Qwen2.5-Coder inventory, bounded in size, rather
than re-encode all 339 tensors immediately.

The subset should include both frozen tensor types:

- F32;
- Q8_0.

It should include materially different tensor sizes where
practical.

The validation must use existing frozen recipes and existing
frozen object identity.

The exact target subset must be preregistered before execution.

## 25. Relationship to previous fidelity evidence

MAF Object V1 has already demonstrated exact persistent-object
fidelity on the frozen pilot subset.

Encoder V1 validation does not invalidate or replace that
evidence.

Its new claim is narrower:

a frozen pre-payload compile recipe can be enforced through an
explicit Encoder boundary while preserving the already-proven
single-source-pass exact persistence behavior.

## 26. Non-claims

Encoder V1 does not establish:

- compression;
- deduplication;
- operational fragmentation;
- selective tensor access;
- sparse execution;
- partial reconstruction;
- segment locality;
- runtime cache policy;
- reduced RAM usage for inference;
- reduced inference payload traffic;
- direct MAF-native inference;
- numerical acceleration;
- Vulkan execution;
- model replacement.

Those remain later research phases.
