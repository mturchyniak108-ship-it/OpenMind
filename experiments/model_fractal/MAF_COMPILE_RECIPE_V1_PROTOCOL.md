# MAF Compile Recipe V1 Protocol

Status: research protocol

Schema:

`openmind.maf_compile_recipe.v1`

## 1. Purpose

The MAF compile recipe is the deterministic output of the
Planner stage in:

`Scanner -> Classifier -> Planner -> Encoder -> Segment Builder`

A recipe describes what the Encoder is permitted and required
to do before any source payload conversion begins.

The Planner consumes logical object identity and metadata
classification records.

The Planner must not inspect source tensor payload bytes.

The recipe is therefore a pre-payload execution contract,
not an observation of payload-derived properties.

## 2. Phase 6A scope

V1 exists to establish the conservative exact-fidelity
baseline required by Phase 6A step 4:

> Generate a compile recipe before payload conversion.

The V1 planner must produce a complete deterministic recipe
for every valid classified object even when no structural,
compression, fragmentation, residency, or locality decision
can yet be justified.

Unknown or unresolved decisions must remain explicit.

They must not be replaced by guesses.

## 3. Input boundary

The Planner may consume:

- stable model PK;
- stable object PK;
- tensor name;
- tensor type;
- dimensions;
- element count;
- layer index;
- component;
- parameter kind;
- semantic class;
- structural class;
- runtime class;
- classifier schema/version.

The Planner may also consume immutable policy constants
defined by this protocol.

The Planner must not determine a V1 recipe from:

- source payload bytes;
- payload SHA256;
- payload values;
- quantization block contents;
- observed activation values;
- physical segment;
- physical offset;
- cache tier;
- device placement;
- runtime hotness;
- observed reuse;
- future access traces.

## 4. Identity boundary

A compile recipe is not logical object identity.

Changing:

- planner version;
- physical placement;
- chunk size;
- segment generation;
- cache policy;
- temporary runtime residency;

must not silently change the existing model or object PK.

The object PK remains governed by
`MAF_IDENTITY_V1_PROTOCOL.md`.

A future representation that changes the logical encoding
participating in object identity must be introduced under an
explicit identity-compatible protocol change.

V1 does not redefine object identity.

## 5. Required output record

Each recipe must contain:

- `schema`
- `planner_version`
- `model_pk`
- `object_pk`
- `name`
- `tensor_type`
- `dims`
- `elements`
- `semantic_class`
- `structural_class`
- `runtime_class`
- `source_encoding`
- `target_representation`
- `fidelity_requirement`
- `payload_access`
- `payload_passes`
- `hash_policy`
- `transform_policy`
- `compression_policy`
- `deduplication_policy`
- `fragmentation_policy`
- `dense_materialization_policy`
- `segment_placement_policy`
- `runtime_residency_policy`
- `maf_native_compute_policy`
- `unresolved`
- `planning_basis`

## 6. Schema and planner version

V1 schema:

`openmind.maf_compile_recipe.v1`

V1 planner version:

`maf_planner_v1`

The planner version identifies the decision rules that
produced the recipe.

## 7. Source encoding

For the current exact GGUF baseline:

`source_encoding = gguf_payload_exact`

This term intentionally reuses the frozen baseline encoding
already defined by the MAF object and identity protocols.

V1 does not reinterpret F32 or Q8_0 numerical payloads.

Tensor type remains separately recorded.

## 8. Target representation

V1 baseline:

`target_representation = persistent_maf_object_exact`

This means:

- persist the source numerical payload exactly;
- wrap it in the MAF object representation;
- do not apply lossy conversion;
- do not require a permanently materialized conventional
  dense tensor.

This field describes compilation intent.

It does not claim MAF-native execution.

## 9. Fidelity requirement

V1:

`fidelity_requirement = exact`

Exact means the compiled representation must support the
same literal payload bytes or an independently validated
exact reconstruction defined by a later protocol.

The V1 baseline uses literal exact payload preservation.

Lossy conversion is prohibited.

## 10. Payload access policy

Recipes are generated before payload access.

Therefore:

`payload_access = deferred_to_encoder`

The Planner must not read source payload bytes.

## 11. Payload pass policy

V1:

`payload_passes = 1`

This is the target execution contract for the Encoder:

when compilation occurs, the source payload should be
streamed once where practical while performing required
hashing and output construction.

This field does not itself perform the pass.

A later Encoder validation must independently prove whether
the one-pass contract was achieved.

## 12. Hash policy

V1:

`hash_policy = sha256_stream_required`

The Encoder must calculate or verify the exact payload hash
while streaming the source payload.

The Planner does not calculate the payload hash.

A pre-existing inventory hash may be used as an expected
integrity value, but payload-derived evidence must not
influence the recipe decision itself.

## 13. Transform policy

V1:

`transform_policy = none`

No numerical transformation is authorized by the baseline
recipe.

This includes no:

- residual transform;
- reversible transform;
- fractal transform;
- sparse transform;
- numerical re-encoding.

Future exact transforms require separate validation.

## 14. Compression policy

V1:

`compression_policy = none`

The baseline planner does not authorize compression.

Future compression must preserve exact representation
fidelity and must be independently validated.

## 15. Deduplication policy

V1:

`deduplication_policy = unresolved`

Metadata classification alone cannot prove payload equality.

The Planner must not infer deduplication eligibility from:

- equal dimensions;
- equal tensor type;
- similar names;
- equal semantic class.

Payload-derived exact deduplication may be measured later
during compilation, but it is not a pre-payload V1 decision.

## 16. Fragmentation policy

V1:

`fragmentation_policy = none`

The existing fragment identity primitive does not define an
operational production fragmentation scheme.

Therefore the baseline Planner must not invent fragment
ranges or fragment sizes.

Future fragmentation requires:

- an explicit fragment scheme;
- defined logical range units;
- exact reconstruction validation;
- independent selective-access validation.

## 17. Structural class handling

The metadata classifier currently emits:

`structural_class = unknown`

for the frozen Qwen validation inventory.

V1 must preserve that fact.

The Planner must not upgrade `unknown` to:

- direct;
- fragmentable;
- fractal;
- sparse;
- reversible-transform;

without evidence defined by a future structural protocol.

## 18. Runtime class handling

The metadata classifier currently emits:

`runtime_class = unknown`

for the frozen Qwen validation inventory.

V1 must preserve that fact.

Runtime classification depends on observed execution and
residency behavior and is not a pre-payload logical fact.

The Planner must not invent:

- cold;
- warm;
- hot-MAF;
- hot-dense;
- prefetch candidate.

## 19. Dense materialization policy

V1:

`dense_materialization_policy = optional_compute_view`

The persistent MAF object is the storage representation.

A conventional dense tensor may be materialized later when
required by an existing compute backend.

This policy does not require eager dense materialization.

It also does not claim that dense materialization can yet
be eliminated.

## 20. Segment placement policy

V1:

`segment_placement_policy = unresolved`

Physical segment placement belongs to the later
Segment Builder / catalog / locality layers.

The Planner must not assign:

- segment filename;
- generation;
- byte offset;
- cache tier;
- device.

Physical placement must remain independent from logical
object identity.

## 21. Runtime residency policy

V1:

`runtime_residency_policy = unresolved`

Residency decisions belong to the later runtime/residency
phase and depend on observed usage.

The pre-payload Planner must not determine runtime residency.

## 22. MAF-native compute policy

V1:

`maf_native_compute_policy = disabled_unvalidated`

The baseline recipe does not authorize direct MAF-native
numerical computation.

Existing dense compute paths remain permitted through
optional materialized views.

MAF-native computation may only be enabled after independent
fidelity validation.

## 23. Unresolved decisions

Every recipe must contain an `unresolved` list.

For the V1 baseline, it must contain:

- `deduplication`
- `structural_optimization`
- `segment_placement`
- `runtime_residency`
- `maf_native_compute`

Fragmentation is not unresolved in V1.

It is explicitly disabled:

`fragmentation_policy = none`

because no production fragment scheme has yet been defined.

Compression and transformation are likewise explicitly
disabled rather than unresolved.

## 24. Planning basis

Each recipe must include:

`planning_basis`

The planning basis records the logical facts and policy
version used to choose the recipe.

At minimum it must identify:

- classifier schema;
- planner schema;
- planner version;
- model PK;
- object PK;
- tensor metadata;
- semantic class;
- structural class;
- runtime class.

It must not contain payload-derived values as decision
inputs.

## 25. Determinism

Given the same:

- model PK;
- object PK;
- classifier record;
- V1 planner policy;

the Planner must emit the same canonical recipe.

Input ordering must not change an individual object's
recipe.

Physical metadata changes must not change the recipe.

Payload hash changes must not change the pre-payload
planning decision.

## 26. Frozen Qwen validation target

The first planner validation target is the same frozen
Qwen2.5-Coder inventory used for metadata classification.

Expected input count:

`339`

Expected recipe count:

`339`

All recipes should use:

- `source_encoding = gguf_payload_exact`
- `target_representation = persistent_maf_object_exact`
- `fidelity_requirement = exact`
- `payload_access = deferred_to_encoder`
- `payload_passes = 1`
- `hash_policy = sha256_stream_required`
- `transform_policy = none`
- `compression_policy = none`
- `deduplication_policy = unresolved`
- `fragmentation_policy = none`
- `dense_materialization_policy = optional_compute_view`
- `segment_placement_policy = unresolved`
- `runtime_residency_policy = unresolved`
- `maf_native_compute_policy = disabled_unvalidated`

All frozen classifier structural classes should remain:

`unknown`

All frozen classifier runtime classes should remain:

`unknown`

## 27. Required validation properties

A V1 planner validation must prove:

- 339 valid inputs produce 339 recipes;
- every input object receives exactly one recipe;
- object PKs are preserved unchanged;
- repeated planning is deterministic;
- input ordering does not alter per-object recipes;
- physical metadata does not alter recipes;
- payload hashes do not alter planning decisions;
- no source GGUF payload is opened by the Planner;
- no payload bytes are read by the Planner;
- no fragment PKs are generated;
- no physical segment placement is assigned;
- no runtime residency is assigned;
- no structural optimization is invented;
- no MAF-native compute is enabled;
- malformed planner inputs are rejected where applicable.

## 28. Planner / Encoder boundary

The Planner emits intent.

The Encoder executes that intent.

The Planner may say:

- preserve exact source payload;
- hash during streaming;
- make one payload pass;
- write persistent MAF object form.

The Planner must not:

- open source payload;
- compute payload digest;
- copy payload bytes;
- create segments;
- choose offsets;
- activate runtime residency.

Those actions belong downstream.

## 29. Relationship to existing MAF object v1

`maf_object_v1.py` currently provides an exact persistent
object compiler.

Its existing behavior is compatible with the conservative
V1 recipe baseline:

- exact GGUF payload preservation;
- SHA256 verification;
- streaming copy;
- persistent object output.

The compile-recipe protocol does not modify or replace that
engine.

A later Encoder integration may consume V1 recipes and call
or refactor equivalent exact-object construction behavior.

## 30. Non-claims

Passing V1 planning validation does not establish:

- compression;
- exact deduplication;
- payload sharing;
- operational fragmentation;
- selective fragment access;
- structural fractal suitability;
- sparse suitability;
- reversible transforms;
- cache policy;
- prefetch suitability;
- segment locality;
- reduced RAM usage;
- reduced payload traffic;
- direct MAF-native inference;
- improved inference speed.

It establishes only that a deterministic, auditable,
pre-payload compile contract exists before conversion.
