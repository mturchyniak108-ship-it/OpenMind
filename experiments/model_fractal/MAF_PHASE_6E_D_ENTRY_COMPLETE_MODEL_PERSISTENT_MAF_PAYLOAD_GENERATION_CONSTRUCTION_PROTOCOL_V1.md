# OpenMind Phase 6E-D Entry — Complete-Model Persistent MAF Payload Generation Construction Protocol V1

Status: CONSTRUCTION PROTOCOL ONLY — COMPLETE-MODEL MATERIALIZATION IS NOT AUTHORIZED BY THIS DOCUMENT

Author: Mitchell Turchyniak

## 1. Purpose

This protocol defines the prospective construction boundary for materializing the already-qualified complete 339-object MAF model namespace into persistent serialized MAF generation storage.

It does not authorize inference, output-parity science, performance measurement, selector science, MAF-native compute claims, or modification of llama.cpp.

The construction goal is narrow: preserve the existing 339 logical object identities and materialize exact numerical payload backing under those identities using the already validated MAF serialization, segment, generation, and reader machinery.

## 2. Frozen repository checkpoint

- Branch: `labs/multidimensional-maf`
- Parent HEAD: `ced756f32d019a1649796cce587766ec408c8b9b`
- Phase 6E-D integration construction protocol SHA256: `93383a2b4def3ea3913d1272099c8c5b06be7e6c8671d41de18f37b14725a09d`

## 3. Frozen complete-model authorities

- Source GGUF tensor inventory: `experiments/model_fractal/gguf_tensor_inventory_v1.json`
- Inventory SHA256: `7acf6d5dc672182aee0244b1bb85a47466f33dbdcdf10bde863e24f3659240ee`
- Frozen source tensor count: `339`
- Full MAF representation: `experiments/model_fractal/maf_representation_v1.json`
- Representation SHA256: `0e70bc32fb76945d7c684b3d73d5598f587fd17c6bda77b32db3e601af3f8dbe`
- Full-model identity validation: `experiments/model_fractal/maf_full_model_identity_validation_v1.json`
- Full-model identity SHA256: `ef954f38e16ccbc73211c503d7d9c9b8462028d6222fb32fb9b15eb59615d25d`
- Qualified logical object count: `339`
- Qualified unique object PK count: `339`
- Compile recipe validation: `experiments/model_fractal/maf_compile_recipe_validation_v1.json`
- Compile recipe validation SHA256: `ceed863754a119fc59b6fdeb80b9a6d1766bfa47e33992315536669f58331ccd`
- Identity-to-recipe PK mapping agreement: exact `339/339`
- Frozen source GGUF SHA256 authority: `507de59046601282ba768a9789900e6ccf60ed93ddf346730b7c68eb0715bc47`

The qualified 339-PK namespace is immutable for this construction. No new logical object PK may be minted as a replacement for an existing qualified PK.

## 4. Existing persistent-generation control

- Existing runtime validation generation manifest: `results/runtime/maf_query_to_pk_selection_validation_v1_generation/validation_generation.manifest.json`
- Manifest SHA256: `28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3`
- Existing persistent coverage: `12/339` qualified model PKs
- Existing strong locator coverage: `12/339`
- Complete 339-object persistent generation currently present: `NO`

The 12-object generation is a validated construction and reader control only. It must not be reinterpreted as complete-model persistence.

## 5. Frozen construction machinery

- MAF object API: `experiments/model_fractal/maf_object_v1.py`
- MAF object API SHA256: `eed6cbd96995412a632883f3c534f9023e7711ea8eb437afe35a48312502f63b`
- Compile recipe engine: `experiments/model_fractal/maf_compile_recipe_v1.py`
- Compile recipe engine SHA256: `388110497205591135bd191016987391fb2c9664513f9133bc7a4abd5df5ff51`
- Segment builder: `experiments/model_fractal/maf_segment_builder_v1.py`
- Segment builder SHA256: `f063c87989f9a646497743034e85d3f4674a7b45cf88df754b669d6621cc28f0`
- Segment builder validation SHA256: `732291986d1b1ee3feeeadec1af34b5222d887f8b01acecc492de3cb0f0f242f`
- Generation engine: `experiments/model_fractal/maf_generation_engine_v1.py`
- Generation engine SHA256: `8868c58e98084226dd957391e1a2f4d1122e886607640ae0be59279f025f1a51`
- Generation engine validation SHA256: `a37ee07ab548b1dea398bb42de42cd893df437b06b91a8a767464a4559e52727`
- Segment reader: `experiments/model_fractal/maf_segment_reader_v1.py`
- Segment reader SHA256: `3499cb8e528fe8e9315e3e5656d6aa888c95ca175310b6371e722de409827369`
- Resident PK directory: `experiments/model_fractal/maf_resident_pk_directory_v1.py`
- Resident PK directory SHA256: `4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6`

No construction runner may silently substitute different implementations for these authorities. Any required implementation change must be separately specified, qualified, and frozen before complete-model materialization.

## 6. Downstream llama.cpp consumer boundary

- llama.cpp source checkpoint: `dc72703fc69698b1ea68ece8d2dd8a96e6a4e1fe`
- Public header SHA256: `1fbcba4003cfc089fa9681973acb3d9e24e465f32c3506ceb0ec7fa29952bdae`
- Public `llama_model_init_from_user` load-time tensor callback mechanism: statically proved by the preceding Phase 6E-D entry audits.
- Hybrid GGUF reconstruction required by the public API: `NO`.
- llama.cpp modification required by the public callback mechanism: `NO`.

This construction does not invoke the callback. It prepares persistent bytes that a later separately qualified callback bridge may consume.

## 7. Identity preservation contract

For every one of the 339 source tensor names, construction must:

1. Resolve exactly one already-qualified `mafobj:v1:` PK from the frozen full-model identity authority.
2. Resolve the exact same PK from the frozen compile recipe authority.
3. Reject any name-to-PK mismatch.
4. Reject any duplicate logical PK.
5. Reject any unexpected tensor name.
6. Reject any missing tensor name.
7. Re-derive object identity through the frozen object API when serialization requires identity derivation and require exact equality with the qualified PK.
8. Never override a failed derivation by manually forcing the expected PK.

Success requires exact set equality: `339 expected names = 339 constructed names = 339 qualified PKs`.

## 8. Numerical payload contract

The numerical payload for each object must be the exact frozen GGUF tensor payload associated with that tensor descriptor.

For every tensor, construction must fail closed unless all applicable frozen metadata agree:

- tensor name
- GGML/GGUF tensor type
- dimensions
- element count when present
- payload byte count
- payload SHA256
- qualified logical object PK

No numerical conversion, requantization, dequantization, reordering, padding reinterpretation, normalization, or dtype substitution is permitted in V1.

The representation remains `gguf_payload_exact`.

A later materialization runner may read source-GGUF payload spans only when that runner has been separately frozen and explicitly authorized. This protocol itself performs no source-GGUF read.

## 9. Tied-payload control

`output.weight` and `token_embd.weight` have the same qualified payload SHA256:

`1dc7e3115bc86f6a127f634edfee0257433f893df0eb4730928050abb70d588e`

They nevertheless have distinct qualified logical object PKs.

V1 construction must preserve both logical identities. Equal payload bytes must never collapse the two logical object PKs into one PK.

Physical payload deduplication is not authorized by this V1 protocol unless a separately frozen storage contract proves that deduplication preserves independent object identity, object verification, locator semantics, and callback read semantics.

Absent that separate proof, materialize both logical serialized objects independently.

## 10. Persistent generation target

The prospective runtime generation root is:

`results/runtime/maf_full_model_persistent_generation_v1/`

The future construction runner must use create-once semantics.

- Existing final target: fail.
- Existing partial target: fail unless a separately frozen recovery protocol explicitly permits recovery.
- Existing active generation with conflicting identity: fail.
- Overwrite of an existing segment or manifest: forbidden.
- In-place modification of the validated 12-object generation: forbidden.

Construction output must remain outside Git-tracked science/source paths unless a later qualification result or documentation freeze explicitly selects a tracked summary artifact.

## 11. Generation and locator contract

A successful complete generation must expose exactly 339 qualified logical objects through deterministic generation metadata.

For each object PK, the generation authority must provide enough information for the frozen segment reader and resident-PK machinery to locate and recover exactly one serialized object.

At minimum the effective locator semantics must bind:

- qualified object PK
- physical segment identity
- object offset
- serialized object length
- generation identity or generation-manifest authority
- payload SHA256 or an equivalent frozen integrity path that is verified after decode

The exact manifest field names are governed by the frozen generation machinery. This protocol does not invent an incompatible manifest schema.

Success requires `339/339` qualified PK locator coverage and zero unexpected PKs.

## 12. Serialized-object readback qualification

Materialization is not qualified merely because files were written.

Before the generation can be used by a llama callback bridge, every one of the 339 objects must be read back through the frozen MAF segment-reader path and validated.

For every read-back object, require:

- requested PK equals returned PK
- returned tensor name equals frozen tensor name
- returned type equals frozen type
- returned dimensions equal frozen dimensions
- returned payload length equals frozen payload length
- returned payload SHA256 equals frozen payload SHA256
- serialized object is structurally valid under the frozen object format
- no locator resolves outside the frozen complete-model generation

Any single failure means `COMPLETE-MODEL PERSISTENT GENERATION NOT QUALIFIED`.

## 13. Resource and streaming constraints

Construction must be streaming and bounded.

- Do not retain all 339 numerical payloads in memory simultaneously.
- Process at most a bounded object or bounded batch of objects at one time.
- Perform a disk-space preflight before the first payload byte is written.
- Include space for final serialized objects, generation metadata, temporary construction state, and a safety margin.
- Fail before materialization if available storage is below the frozen runner threshold.
- Do not use network access as part of construction or qualification.

Performance is not an acceptance criterion. Correctness and provenance dominate.

## 14. Determinism contract

The future runner must freeze deterministic ordering before materialization.

Object ordering must derive solely from frozen authorities such as canonical tensor ordering and the frozen compile recipe. Filesystem enumeration order must not determine object order.

The runner must report deterministic hashes for final manifests and segments. A later qualification must distinguish deterministic construction evidence from performance measurements.

## 15. Provenance ledger

The construction result must preserve a machine-readable per-object provenance ledger containing or deterministically resolving:

- tensor name
- qualified object PK
- source descriptor authority
- tensor type
- dimensions
- payload byte count
- payload SHA256
- serialized object length
- serialized object SHA256 when the frozen format or qualification path exposes it
- physical segment identity
- object offset
- generation identity
- whether numerical bytes came from the frozen source payload

No row may claim MAF numerical provenance unless the serialized object actually contains or resolves the verified payload bytes for that exact qualified object.

## 16. Construction qualification gates

The future complete-model materialization is qualified only if all gates pass:

- `PG01` frozen repository and authority hashes pass before mutation.
- `PG02` exact 339 tensor names recovered.
- `PG03` exact 339 qualified PKs recovered.
- `PG04` full identity and compile-recipe PK maps agree 339/339.
- `PG05` all 339 payload SHA256 authorities are present.
- `PG06` every source payload read matches its frozen SHA256 before serialization.
- `PG07` every serialized object preserves the qualified logical PK.
- `PG08` tied-payload control preserves distinct logical PKs.
- `PG09` generation contains exactly 339 qualified PKs and zero unexpected PKs.
- `PG10` strong/effective locator coverage is 339/339.
- `PG11` every object is successfully read back through the frozen reader.
- `PG12` every read-back payload SHA256 matches the frozen authority.
- `PG13` no final or partial output was overwritten.
- `PG14` source Git repository remains clean except for separately authorized tracked qualification artifacts.
- `PG15` no inference, prompt, token generation, logits, or output-parity measurement occurs.

The mandatory negative verdict is:

`COMPLETE-MODEL PERSISTENT GENERATION NOT QUALIFIED`

No partial pass may be promoted to complete-model qualification.

## 17. Authorization boundary

This protocol authorizes only the definition of the construction contract.

It does not authorize:

- source-GGUF payload access
- construction runner execution
- creation of the 339-object persistent generation
- rewriting the existing 12-object generation
- new PK derivation replacing qualified PKs
- callback invocation
- model loading
- inference
- Phase 6E-D output-parity science
- Phase 6F performance work
- network access
- upstream push

`maf_native_compute` remains `disabled_unvalidated`.

## 18. Required next gate

After this protocol is qualified and frozen, the next gate is:

`DEFINE + FREEZE COMPLETE-MODEL PERSISTENT MAF PAYLOAD GENERATION RUNNER`

That runner must be reviewed statically against this protocol before any source-GGUF payload span is read or any complete-model generation is materialized.

Phase 6E-D science remains unauthorized until complete-model persistence and the subsequent public callback bridge are independently qualified and frozen.

