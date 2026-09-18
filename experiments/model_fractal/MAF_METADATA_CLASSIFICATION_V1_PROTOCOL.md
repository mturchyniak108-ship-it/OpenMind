# MAF Metadata Classification V1 Protocol

## Status

Preregistered research protocol.

This protocol defines metadata-only logical classification for MAF model
objects before source payload bytes are read.

It does not define payload transforms, fragmentation, storage placement,
runtime residency, or inference behavior.

## Goal

Implement Phase 6A metadata-first classification:

`Scanner -> Classifier -> Planner -> Encoder -> Segment Builder`

The classifier operates only on scanner metadata and produces deterministic,
auditable classification records suitable as inputs to later compile planning.

## Core rule

Classification must distinguish:

1. facts directly observed in scanner metadata;
2. semantic roles deterministically derivable from stable tensor names;
3. structural or runtime hypotheses that are not yet supported.

Unknown information must remain explicitly unknown rather than being guessed.

## Input boundary

V1 classification may use only these logical metadata fields:

- `name`
- `type`
- `dims`
- `elements`

The classifier may derive:

- layer index from a valid `blk.<integer>.<component>` name;
- component family from the tensor name;
- parameter kind from a terminal `.weight` or `.bias`;
- rank from the number of dimensions.

The following scanner fields must not determine logical classification:

- `file_start`
- `offset`
- `payload_sha256`
- `span_bytes`
- `validation`
- physical segment
- physical generation
- device placement
- cache residency

These fields may be carried separately for integrity, storage, or runtime use,
but changing them must not change the metadata classification.

## Output schema

Classification records use schema:

`openmind.maf_metadata_classification.v1`

Each record contains:

- `schema`
- `name`
- `layer_index`
- `component`
- `parameter_kind`
- `semantic_class`
- `structural_class`
- `runtime_class`
- `tensor_type`
- `rank`
- `dims`
- `elements`
- `classification_basis`

`classification_basis` records which logical metadata fields justified the
classification.

## Semantic classes

V1 recognizes the following deterministic semantic classes:

- `embedding`
- `output_projection`
- `normalization`
- `attention_query_weight`
- `attention_key_weight`
- `attention_value_weight`
- `attention_output_weight`
- `attention_query_bias`
- `attention_key_bias`
- `attention_value_bias`
- `ffn_gate_weight`
- `ffn_up_weight`
- `ffn_down_weight`
- `unknown`

## Exact semantic mapping rules

The following complete tensor names map directly:

- `token_embd.weight` -> `embedding`
- `output.weight` -> `output_projection`
- `output_norm.weight` -> `normalization`

For names matching:

`blk.<layer>.<component>`

the component mapping is:

- `attn_norm.weight` -> `normalization`
- `ffn_norm.weight` -> `normalization`
- `attn_q.weight` -> `attention_query_weight`
- `attn_k.weight` -> `attention_key_weight`
- `attn_v.weight` -> `attention_value_weight`
- `attn_output.weight` -> `attention_output_weight`
- `attn_q.bias` -> `attention_query_bias`
- `attn_k.bias` -> `attention_key_bias`
- `attn_v.bias` -> `attention_value_bias`
- `ffn_gate.weight` -> `ffn_gate_weight`
- `ffn_up.weight` -> `ffn_up_weight`
- `ffn_down.weight` -> `ffn_down_weight`

Any unmatched name must produce:

`semantic_class = "unknown"`

V1 must not infer an unsupported semantic role from dimensions, tensor type,
offset, payload hash, or similarity to another tensor.

## Layer index

For:

`blk.<non-negative integer>.<component>`

`layer_index` is that integer.

For model-level tensors such as:

- `token_embd.weight`
- `output.weight`
- `output_norm.weight`

`layer_index` is null.

Malformed block names are not silently repaired.

## Component

For a valid block tensor:

`component` is the suffix following `blk.<layer>.`

For recognized model-level tensors:

- `token_embd.weight` -> `token_embd`
- `output.weight` -> `output`
- `output_norm.weight` -> `output_norm`

Unrecognized model-level names retain their complete tensor name as the
component so that information is not discarded.

## Parameter kind

A name ending in `.weight` has:

`parameter_kind = "weight"`

A name ending in `.bias` has:

`parameter_kind = "bias"`

Otherwise:

`parameter_kind = "unknown"`

Parameter kind is orthogonal to semantic class.

## Structural class

The Phase 6A roadmap anticipates structural classes including:

- direct
- fragmentable
- fractal
- sparse
- reversible-transform

Metadata-only evidence currently does not justify assigning any of these
classes to a tensor.

Therefore V1 requires:

`structural_class = "unknown"`

for every classification record.

A later protocol may promote a structural class only after its criteria are
defined and independently validated.

## Runtime class

The Phase 6A roadmap anticipates runtime classes including:

- cold
- warm
- hot-MAF
- hot-dense
- prefetch candidate

Runtime class depends on observed access, reuse, materialization, residency,
or other runtime evidence.

Scanner metadata alone does not provide that evidence.

Therefore V1 requires:

`runtime_class = "unknown"`

for every classification record.

Runtime behavior must never alter logical object identity.

## Determinism

The same logical metadata input must always generate the same classification
record.

Physical placement or integrity metadata changes must not alter classification.

Input ordering must not alter per-object classifications.

## Frozen Qwen validation target

The initial validation target is the frozen Qwen2.5-Coder inventory:

`experiments/model_fractal/gguf_tensor_inventory_v1.json`

Expected inventory properties:

- 339 tensors
- 339 unique names
- 141 F32 tensors
- 198 Q8_0 tensors
- 141 rank-1 tensors
- 198 rank-2 tensors
- 15 observed name families

All 339 frozen tensor names are expected to match a V1 semantic rule.

This expectation is specific to the frozen validation inventory and is not a
claim that arbitrary GGUF models will have zero unknown semantic classes.

## Validation gates

A validation implementation must demonstrate:

- exactly 339 input records;
- exactly 339 output classifications;
- exactly 339 unique names;
- no GGUF payload access;
- deterministic repeated classification;
- input-order independence;
- physical/integrity-field independence;
- all frozen Qwen names semantically classified;
- all structural classes remain `unknown`;
- all runtime classes remain `unknown`;
- malformed or invalid logical metadata is rejected where applicable;
- no object, model, or fragment PK changes are caused by classification.

## Non-claims

Passing V1 does not establish:

- payload fragmentation;
- fragment range semantics;
- fractal suitability;
- sparse representation;
- reversible transformation eligibility;
- runtime hotness;
- cache policy;
- prefetch suitability;
- compile recipes;
- persistent segment placement;
- selective reconstruction;
- MAF-native inference.

Those require separate protocols and evidence.
