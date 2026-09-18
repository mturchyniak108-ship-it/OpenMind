# OpenMind / MAF Phase 6E-D Entry — MAF-to-Inference Integration Construction Protocol V1

## Status

**PROSPECTIVE CONSTRUCTION PROTOCOL — NO PHASE 6E-D SCIENCE AUTHORIZED**

This protocol defines the engineering and evidence boundary that must be satisfied before OpenMind may preregister or execute Phase 6E-D output-parity / quality science.

It does not itself authorize inference, model loading, prompt execution, token generation, logit evaluation, output-parity claims, quality claims, performance claims, MAF-native-compute claims, or replacement of conventional llama.cpp model execution.

---

## 1. Frozen entry state

Phase 6E-C is closed and frozen.

Frozen Phase 6E-C verdict commit:

`5f6b71f3546c9d4870d5e2834cfac46f451efd75`

Frozen Phase 6E-C result:

- path: `experiments/model_fractal/maf_phase_6e_c_actual_serialized_object_read_avoidance_v1.json`
- SHA256: `99f1b72ab0da23142cd544f408e5c3cc1d6f5ab716e74eb434ec37cc53769f23`

Frozen Phase 6E-C verdict:

- path: `experiments/model_fractal/MAF_PHASE_6E_C_ACTUAL_SERIALIZED_OBJECT_READ_AVOIDANCE_V1_VERDICT.md`
- SHA256: `7e284db7c320824037dd4e860a88416a78184695e65092383e7b10464e35de16`

Phase 6E-C established generation-bound application-level serialized MAF object/tensor-payload read avoidance for the frozen validation population.

Phase 6E-C did not establish inference, output parity, answer quality, physical-device I/O avoidance, MAF-native compute, or performance.

---

## 2. Phase 6E-D roadmap boundary

The frozen roadmap states:

- Phase 6E-C: prove actual tensor/object avoidance;
- Phase 6E-D: evaluate output parity/quality;
- Phase 6F: measure performance only after correctness.

The Phase 6E entry checkpoint assigns the following to the separately preregistered Phase 6E-D fidelity boundary:

- output parity;
- logits;
- top-k behavior;
- token agreement;
- generation-quality effects.

Direct MAF-native compute remains:

`disabled_unvalidated`

Therefore Phase 6E-D science requires a real executable treatment arm before its comparison protocol can be frozen.

---

## 3. Binding-audit findings motivating this protocol

The read-only Phase 6E-D entry audits established the following.

### 3.1 Conventional control arm exists

The native inference engine exposes:

- `InferenceConfig.model_path`;
- `InferenceEngine::load()`;
- `InferenceEngine::generate(prompt)`;
- a llama.cpp model loaded through `llama_model_load_from_file(...)`.

This is a valid conventional full-GGUF control surface.

### 3.2 Deterministic text generation exists

The native inference engine configures:

`llama_sampler_init_greedy()`

and samples through:

`llama_sampler_sample(...)`

This provides a deterministic greedy text-generation surface suitable for later comparison once a valid treatment arm exists.

### 3.3 Current public observability is incomplete for strong parity science

`InferenceResult` currently exposes:

- generated text;
- inference metrics.

It does not expose:

- generated token IDs;
- logits;
- top-k distributions.

Therefore exact text parity can potentially be observed today, but token/logit/top-k parity requires a separately frozen observation surface before such claims are authorized.

### 3.4 No executable MAF inference treatment arm is currently proved

The repository-wide binding audit found:

- zero native source files with a proved MAF-aware compute path;
- zero same-function paths joining the strong MAF serialized-object read APIs to native inference execution;
- no proved MAF-to-llama.cpp tensor provider;
- no proved selective tensor injection mechanism;
- no proved MAF-backed model loader.

Several files contain both generic MAF terms and process/FFI machinery, but those co-occurrences do not establish an executable MAF inference arm.

### 3.5 Dense reconstruction candidates are not sufficient

Some existing validation files contain MAF-related terms and GGUF/write operations.

Those are only construction candidates.

A path that simply recreates or copies the complete conventional GGUF and then invokes the ordinary llama.cpp loader does not establish selective MAF compute and must not be presented as the authoritative Phase 6E-D treatment.

---

## 4. Construction question

The engineering question governed by this protocol is:

> Can OpenMind construct and statically qualify an inference integration in which the treatment execution consumes numerical model state derived from the frozen MAF generation through an explicitly identified MAF-backed path, rather than silently falling back to the same conventional full-GGUF model-loading path used by the control?

This is a construction and binding question only.

It is not yet the Phase 6E-D scientific parity question.

---

## 5. Required bridge property

A qualifying bridge must make the provenance of treatment numerical state explicit and auditable.

At minimum, the bridge must identify:

1. the frozen MAF generation;
2. the query-derived treatment PK route or another separately frozen treatment-selection authority;
3. the exact serialized MAF objects used;
4. the exact payload SHA256 values used as numerical state;
5. the compute-facing tensor or model-state destination receiving those bytes;
6. the inference entry point consuming that destination;
7. the control path from the conventional GGUF;
8. the mechanism preventing silent control-path substitution during treatment execution.

A treatment arm is not proved merely because MAF metadata was consulted before conventional full-GGUF inference.

---

## 6. Acceptable integration classes

The construction phase may investigate one or more of the following classes.

### Class A — Direct MAF-backed native tensor provider

A native loader/provider obtains compute tensors directly from MAF generation objects or their validated payload views and supplies them to the inference runtime.

This is the strongest bridge class.

### Class B — Explicit hybrid model-state construction

A deterministic compute artifact may combine:

- frozen non-MAF state required by the conventional runtime; and
- explicitly identified MAF-derived treatment tensors or payloads.

For any tensor claimed as MAF-derived, the treatment artifact must prove that its compute bytes equal the frozen MAF payload bytes and that those bytes did not originate from an unobserved reread of the control tensor during treatment construction.

A hybrid bridge may qualify engineering plumbing.

It does not by itself establish selective compute, tensor avoidance, or Phase 6E-D fidelity.

### Class C — Materialized MAF-derived complete model artifact

A complete model artifact constructed from MAF-derived state may be used only as a bridge-qualification tool if its provenance is explicit.

If construction requires complete conventional GGUF tensor payloads, the resulting artifact is not an authoritative selective-MAF treatment arm.

It may validate serialization, loader compatibility, and observability plumbing only.

---

## 7. Explicitly disallowed pseudo-bridges

The following must fail bridge qualification if presented as the treatment arm:

- selecting PKs and then ignoring them while loading the unchanged control GGUF;
- reading MAF metadata but sourcing treatment numerical tensors from the conventional GGUF;
- copying the complete control GGUF byte-for-byte and relabeling it as MAF-derived;
- loading the full control model first and later claiming selected MAF objects were the compute source without tensor-level provenance;
- comparing two invocations of the same unchanged full-GGUF engine and calling one of them the MAF arm;
- using cached prior answers instead of model inference;
- using reference outputs, reference logits, expected answers, or hidden quality labels to choose treatment state;
- modifying the treatment after observing the Phase 6E-D comparison result.

---

## 8. Treatment provenance ledger

Before any Phase 6E-D scientific execution can be authorized, the integration must be capable of producing a deterministic treatment provenance ledger.

For every MAF-derived compute object or tensor, the ledger must contain at least:

- `object_pk`;
- source generation PK;
- source generation-manifest SHA256;
- serialized object SHA256;
- payload SHA256;
- tensor name or compute-state identifier;
- tensor type;
- dimensions where applicable;
- byte length;
- bridge destination identifier;
- bridge operation;
- whether the numerical bytes were sourced from MAF;
- whether conventional GGUF payload bytes were read for that same claimed MAF-derived destination.

The ledger schema and canonical serialization must be frozen before any authoritative Phase 6E-D run.

---

## 9. Control/treatment separation

The later Phase 6E-D comparison must have two explicitly different execution paths.

### Control

The frozen conventional native llama.cpp path using the authorized full GGUF.

### Treatment

The separately frozen MAF integration path.

The treatment must not become identical to the control merely because both ultimately call llama.cpp.

The scientific distinction is the source and construction of compute state, not the final name of the decode function.

---

## 10. Observation-surface requirement

Before Phase 6E-D science, the project must freeze which observable is authoritative.

At minimum one of the following must be available.

### Level 1 — Deterministic exact text

Allowed only when:

- greedy sampling is frozen;
- prompt bytes are frozen;
- tokenizer/model generation is frozen;
- context and generation settings are frozen;
- the comparison is explicitly limited to exact generated UTF-8 text.

This level does not authorize logit or top-k claims.

### Level 2 — Generated token-ID sequence

Preferred over text-only comparison because it removes token-to-piece rendering ambiguity.

Requires the native observation API to expose generated token IDs without changing sampler behavior.

### Level 3 — Logit / top-k observation

Strongest local fidelity surface.

Requires a separately frozen instrumentation contract specifying:

- which decode positions are observed;
- exact vocabulary identity;
- float extraction type;
- top-k value;
- tie behavior;
- numerical tolerance;
- canonical serialization.

Instrumentation must be observational only and must not alter the treatment route or sampling decision.

---

## 11. No performance claim

Bridge construction may record engineering timings for debugging only.

No latency, throughput, RAM, I/O, energy, CPU, GPU, Vulkan, or scaling conclusion is authorized.

All performance science remains Phase 6F.

---

## 12. No new Phase 6E-C claim

This construction phase must not reinterpret Phase 6E-C.

In particular, a bridge may read additional state for engineering qualification without changing the already frozen Phase 6E-C scientific result.

Any later claim that the inference treatment itself preserves the Phase 6E-C selective-read boundary requires explicit instrumentation and preregistration.

Phase 6E-C must not be rerun.

---

## 13. Source-GGUF boundary

The conventional GGUF may be inspected during bridge construction only when explicitly required for engineering provenance or control compatibility.

Such construction access is not Phase 6E-D scientific evidence.

The future authoritative Phase 6E-D protocol must separately define whether control and treatment setup may read the source GGUF and how those reads are excluded from or included in the scientific boundary.

---

## 14. Construction lifecycle

The required lifecycle is:

1. freeze this construction protocol;
2. perform read-only API and tensor-provenance design;
3. create the smallest bridge implementation needed;
4. statically qualify the bridge;
5. freeze the exact bridge source;
6. build the bridge if native compilation is required;
7. qualify the build identity;
8. execute only non-authoritative engineering fixtures needed to prove the bridge is real;
9. freeze a bridge-qualification result;
10. issue a narrow bridge verdict;
11. only then design the Phase 6E-D prospective scientific preregistration.

No Phase 6E-D authoritative inference may occur during steps 1-10.

---

## 15. Bridge qualification acceptance criteria

The bridge qualifies only if all required criteria pass.

### BQ01 — Frozen generation binding

The bridge is bound to an explicit frozen MAF generation and manifest identity.

### BQ02 — Explicit compute provenance

At least one compute-facing numerical state used by the treatment can be traced to frozen MAF payload bytes.

### BQ03 — No silent control substitution

The bridge proves that the claimed MAF-derived state is not silently sourced from the control GGUF during treatment construction or execution.

### BQ04 — Executable treatment path

A concrete callable path exists from the MAF-backed state into an inference-capable runtime.

Static references alone do not pass.

### BQ05 — Control remains distinct

The conventional full-GGUF path remains independently available as the future control.

### BQ06 — Deterministic treatment construction

The same frozen inputs produce the same treatment artifact/state identity.

### BQ07 — Provenance ledger

A deterministic provenance ledger is generated and independently checked.

### BQ08 — Observation surface identified

The future comparison can observe at least deterministic generated text.

If token/logit claims are planned, the required observation instrumentation must already be frozen and qualified.

### BQ09 — No oracle selection

Expected outputs, reference logits, hidden required PKs, quality labels, and post hoc comparison information are not used to choose the treatment state.

### BQ10 — No science claim

Bridge qualification reports engineering readiness only.

It does not report Phase 6E-D parity or quality.

---

## 16. Mandatory negative-result rule

If the bridge cannot produce an executable treatment whose numerical compute provenance is genuinely MAF-derived, record:

`BRIDGE NOT QUALIFIED`

Do not rescue the design by:

- relabeling the conventional full-GGUF arm;
- weakening provenance after seeing failures;
- calling dense control reconstruction selective MAF compute;
- skipping directly to output comparison.

A negative bridge result is scientifically useful because it identifies the exact architecture still missing.

---

## 17. Phase 6E-D preregistration entry condition

Phase 6E-D prospective science becomes eligible for design only after a frozen bridge verdict establishes all of:

- executable treatment path;
- explicit MAF numerical-state provenance;
- distinct full-GGUF control path;
- deterministic construction;
- frozen observation surface;
- no oracle contamination.

Only then may the Phase 6E-D preregistration define the exact comparison metric.

---

## 18. Expected Phase 6E-D metric hierarchy

The later preregistration should prefer the strongest qualified observable in this order:

1. exact generated token-ID agreement;
2. exact deterministic text agreement;
3. logit/top-k agreement under separately frozen numerical tolerances;
4. separately preregistered answer-quality scoring only if exact parity is neither required nor appropriate.

The metric must be selected before authoritative comparison outputs are observed.

---

## 19. Relationship to MAF-native compute

This construction protocol does not enable or validate direct MAF-native compute.

The current status remains:

`disabled_unvalidated`

A direct MAF-native kernel/runtime requires separate numerical and inference-fidelity validation.

A bridge that uses an existing conventional compute engine with MAF-derived numerical state may be sufficient for Phase 6E-D treatment construction without establishing MAF-native compute.

---

## 20. Relationship to Phase 6F

Phase 6F remains blocked until the required correctness/fidelity gates close.

Bridge construction must not optimize for benchmark results before fidelity is established.

No benchmark is authorized by this protocol.

---

## 21. Authorization boundary

Freezing this protocol authorizes only:

- construction design;
- source implementation;
- static qualification;
- build qualification;
- non-authoritative engineering fixtures needed to prove the bridge exists.

It does not authorize:

- authoritative Phase 6E-D inference;
- control/treatment output comparison;
- scientific prompt execution;
- scientific token generation;
- scientific logit extraction;
- output-parity claims;
- answer-quality claims;
- selective-inference claims beyond already frozen evidence;
- physical-I/O claims;
- performance claims;
- Phase 6F entry;
- rerunning any spent Phase 6E-C authoritative slot.

---

## 22. Next gate after protocol freeze

After this protocol is frozen, the next gate is:

**READ-ONLY MAF→COMPUTE PROVENANCE DESIGN AND MINIMAL BRIDGE API SPECIFICATION**

That gate must choose the smallest implementable bridge class and bind its exact inputs, outputs, tensor provenance, native integration surface, and observation surface before source construction begins.

---

Author: Mitchell Turchyniak
