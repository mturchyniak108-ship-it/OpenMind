# OpenMind Roadmap

<!-- OPENMIND:PUBLIC-MAF-STATUS-AUTHORITY:START -->
> **Current MAF status authority:** see [`docs/research/MAF_CURRENT_STATUS.md`](docs/research/MAF_CURRENT_STATUS.md). Older phase-status passages below are retained as historical provenance and may describe earlier checkpoints.
<!-- OPENMIND:PUBLIC-MAF-STATUS-AUTHORITY:END -->


## Mission

OpenMind investigates whether useful AI computation can be performed through a local, native, representation-driven architecture that can reduce dependence on conventional token-by-token inference while preserving correctness and provenance.

The project treats the Canonical Model GGUF as the canonical model/reference artifact and evaluates MAF, fractal MAF, vector maps, fuzzy logic, machine learning, heatwave/heightmap relationships, and native optimized execution as derived computational systems.

## Core Architecture

Canonical Model GGUF -> Truth/Relationship/Provenance/Landscape Maps -> MAF Object Compiler -> MAF Model Catalog -> MAF Segment Store -> MAF Object Runtime + Adaptive Residency -> Fractal/Selective MAF -> Routing/Transition Intelligence -> Validation -> Native C++ -> ARM64/NEON -> Vulkan Optimization

## Phase 1 — Native Local Inference [COMPLETE]

- Native llama.cpp integration
- GGUF loading
- Android ARM64 execution
- Vulkan GPU acceleration
- Native C++ inference
- Persistent sessions
- CMake/CTest validation

## Phase 2 — Representation Discovery [ACTIVE]

- Capture activations
- Analyze layer recurrence
- Analyze transition vectors
- Cross-prompt consistency
- Identify stable representation structures
- Validate numerical reconstruction
- Establish reproducible representation baselines

## Phase 3 — Canonical Model GGUF [ACTIVE]

- Establish canonical GGUF artifact
- Record model hash and metadata
- Inventory tensors and layers
- Preserve quantization information
- Build deterministic extraction tooling
- Establish GGUF-to-representation correspondence

## Phase 4 — Four-Map Representation [NEXT]

- Truth Map — canonical semantic structure
- Relationship Map — semantic and computational relationships
- Provenance Map — evidence lineage and source ancestry
- Landscape Map — activation density, recurrence, convergence, heightmap/heatwave features
- Stable identifiers between all maps
- Vector links between canonical and derived structures

## Phase 5 — GGUF to MAF [RESEARCH]

- Convert a copy of the Canonical Model GGUF into MAF
- Preserve source correspondence
- Measure reconstruction fidelity
- Measure storage size
- Measure RAM
- Measure working memory
- Measure lookup latency
- Measure token requirements
- Compare against original GGUF

## Phase 6 — Fractal MAF [RESEARCH]

- Recursive MAF cells
- Multi-dimensional fractal relationships
- Fractal links to all three primary maps
- Sparse activation representation
- Recursive aggregation
- Test token reduction
- Test memory reduction
- Test computational reduction


## Phase 6A — MAF Object Compilation [ACTIVE RESEARCH]

Goal: make MAF the persistent model-object representation rather than merely
an index around conventional tensors.

Development order:

1. Prove exact `tensor -> MAF object -> tensor/view` round-trip fidelity.
2. Assign stable model, object, and fragment primary keys.
3. Classify objects from metadata before reading payload bytes whenever possible.
4. Generate a compile recipe before payload conversion.
5. Stream source payloads once, performing hashing, exact transformation,
   fragment construction, and placement statistics in the same pass.
6. Avoid whole-tensor temporary allocations where block streaming is sufficient.
7. Preserve dense tensors as optional compute/materialization views until
   MAF-native computation is independently validated.

Initial MAF Compiler stages:

`Scanner -> Classifier -> Planner -> Encoder -> Segment Builder`

Classification is split into:

- static semantic class: weight, embedding, norm, state, route, residual, etc.
- structural class: direct, fragmentable, fractal, sparse, reversible-transform.
- runtime class: cold, warm, hot-MAF, hot-dense, prefetch candidate.

Runtime usage changes must not change logical object identity.

Natural lossless gains such as exact deduplication, reversible transforms,
shared fragments, or exact residual representation may be measured during
compilation, but compression must not reduce representation fidelity.

## Phase 6B — MAF Model Catalog and Segment Store [RESEARCH]

Goal: separate permanent logical identity from temporary physical placement.

The catalog must provide stable primary-key identity for:

- model
- MAF object
- fragment
- route/transition
- physical segment generation

Physical records may change segment, offset, cache tier, or device residency
without changing their logical primary key.

Initial storage model:

- compact resident object/fragment directory
- immutable MAF segment files
- direct `(PK -> segment, offset, length)` resolution
- integrity hashes independent of PK identity
- generation manifests with atomic activation/rollback
- no JSON parsing on the inference hot path

Candidate storage engines remain experimental until benchmarked:

1. compiled binary/RAM index + external MAF segments
2. SQLite control plane + external MAF segments
3. purpose-built MAFDB object engine
4. other permissively licensed embedded engines only when they provide a
   measurable advantage

Do not fork or replace a mature database engine merely for architectural novelty.
A custom MAFDB must earn promotion through measured MAF-specific advantage.

<!-- OPENMIND_PHASE_6B_STATUS_START -->

### Current Phase 6B / Phase 6C Research Status

Research authority for this status:

    local branch: labs/multidimensional-maf
    Phase 6B exit HEAD: 4c1b973
    Phase 6B completion SHA256: 2539b9ad7c623b6415434f73786bf33fc5571a5ec79bd319f7dd8d6bdfe09e94
    Phase 6C entry checkpoint: experiments/model_fractal/MAF_PHASE_6C_ENTRY_CHECKPOINT.md

The active MAF research history remains local-only unless a later
explicit upstream synchronization is performed.

Phase 6B progression:

- **6B.1 Authority / identity rules — COMPLETE**
- **6B.2 Segment Builder — COMPLETE + VALIDATED**
- **6B.3 Generation descriptor / manifest — COMPLETE**
- **6B.4 Generation Engine V1 — COMPLETE**
- **6B.5 Generation Engine validation — COMPLETE**
- **6B.6 Activation protocol — COMPLETE**
- **6B.7 Atomic activation — COMPLETE / VALIDATED**
- **6B.8 Rollback — COMPLETE / VALIDATED**
- **6B.9 Resident PK Directory — COMPLETE / VALIDATED / BENCHMARKED / DIAGNOSTICALLY ACCEPTED**
- **6B.10 Segment Reader V1 — COMPLETE / VALIDATED / BENCHMARKED / DIAGNOSTICALLY ACCEPTED**

**Phase 6B — COMPLETE / CLOSED.**

The unresolved CPU6/CPU7 cluster-1 crossover is optional prospective
follow-up research and does not block Phase 6B exit or Phase 6C entry.

Phase 6C status:

- **Phase 6C — MAF Object Runtime and Residency — RESEARCH CURRENT / ENTRY FROZEN**
- **Phase 6C runtime implementation — NOT YET ACCEPTED**

The Phase 6C entry checkpoint freezes scope before runtime
implementation. Frozen Phase 6B artifacts remain immutable.

<!-- OPENMIND_PHASE_6B_STATUS_END -->

## Phase 6C — MAF Object Runtime and Residency [RESEARCH]

Status: **STARTED / RESEARCH CURRENT / ENTRY FROZEN / NO RUNTIME IMPLEMENTATION ACCEPTED YET**

Entry checkpoint: `experiments/model_fractal/MAF_PHASE_6C_ENTRY_CHECKPOINT.md`

Goal: keep only the useful model working set resident.

Starting Phase 6C scope includes:

- runtime residency state machines;
- long-lived descriptor ownership where justified;
- mmap / mapped-segment residency where justified;
- eviction and reuse policy;
- on-demand dense materialization;
- runtime concurrency and thread-safety contracts.

The database/catalog knows every MAF object; it does not require every object
to be loaded.

Target residency states:

`COLD_DISK -> MAPPED -> HOT_MAF -> HOT_DENSE`

Later:

`HOT_MAF/HOT_DENSE -> VULKAN_MAF`

Required runtime capabilities:

- map/attach and detach/unmap MAF segments
- object pin/unpin
- fragment-level retrieval
- dense materialization on demand
- reuse-aware promotion/demotion
- byte-budgeted caches rather than object-count caches
- bounded allocation arenas/slabs
- minimize copies between disk, mapped payload, decoded cache, and compute view
- preserve canonical immutable bytes on disk so eviction does not require
  reserialization

Compare cache policies including simple LRU controls and frequency/reuse-aware
admission/eviction such as TinyLFU/CLOCK-style designs.

## Phase 6D — Segment Locality and Path-Aware Repacking [RESEARCH]

Goal: make physical storage follow measured model pathways.

Initial segment-size and fragment-size choices are hypotheses and must be
device-benchmarked rather than assumed.

Collect runtime telemetry in RAM, then periodically persist aggregated statistics:

- object access count
- reuse interval
- transition frequency
- materialization count
- bytes read
- cache hit/miss
- promotion/demotion
- prefetch usefulness

Frequently traversed object sequences may be physically colocated in a new
immutable segment generation.

Rules:

- logical PKs never change because of repacking
- physical segment/offset mappings may change
- repacking is generational, validated, and atomically activated
- avoid frequent rewrites that create flash wear or cache churn
- transition locality is more important than global popularity alone
- old generations remain recoverable until the new generation validates

<!-- OPENMIND:MAF-QUERY-SCOPED-WORKING-SETS-ROADMAP:START -->
## Phase 6D-Q — Query-Scoped MAF Working Sets and Reusable PK Route Cache

Status: PROPOSED — NOT VALIDATED

Phase 6D-Q introduces a proposed bridge from persistent/locality-aware MAF
storage to selective MAF execution.

The proposed architecture separates:

- canonical immutable MAFDB model authority;
- a temporary Query-Scoped MAF Capsule containing or referencing the PK working
  set for one input;
- a persistent derived Query Route Cache that remembers successful PK routes for
  exact or similar future queries.

Proposed execution flow:

    input
    -> query signature
    -> prior route lookup
    -> bounded PK selection
    -> query-scoped MAF working set
    -> selective execution
    -> bounded expansion when insufficient
    -> answer
    -> release/detach
    -> retire ephemeral materialization
    -> retain compact route metadata

The initial PK set is not required to be perfect. The intended architecture
allows deterministic bounded expansion when the current working set is
insufficient.

The scientific gates are:

- 6D-Q1: freeze Query Capsule and Query Route Cache schemas;
- 6D-Q2: test non-oracle query-to-PK selection feasibility;
- 6D-Q3: prove attach/detach ownership and cleanup semantics;
- 6D-Q4: test exact/similar query-route reuse with generation binding;
- 6E-A: test selective working-set sufficiency;
- 6E-B: test bounded expansion/recovery;
- 6E-C: prove actual tensor/object avoidance;
- 6E-D: evaluate output parity/quality;
- 6F: measure performance only after correctness.

No current result proves that a prompt can yet select a sufficient PK subset or
that this architecture improves inference performance.

Architecture:
`experiments/model_fractal/MAF_QUERY_SCOPED_WORKING_SET_ARCHITECTURE.md`
<!-- OPENMIND:MAF-QUERY-SCOPED-WORKING-SETS-ROADMAP:END -->

## Phase 6E — Selective MAF Access and Tensor Avoidance [CRITICAL RESEARCH]

Goal: determine whether OpenMind can avoid touching or materializing complete
dense tensors while preserving inference fidelity.

Required progression:

1. exact whole-object reconstruction
2. partial/fractal reconstruction
3. selective fragment retrieval
4. shadow hidden-state comparison against untouched model oracle
5. logit/top-k/token agreement
6. selective dense materialization
7. direct MAF-native computation only after fidelity gates pass

A smaller payload or lower RAM footprint is not sufficient evidence by itself.

The core hypothesis is falsifiable:

> A MAF object may become the persistent numerical state, while a dense tensor
> is only an optional materialized compute view.

If selective access does not preserve correctness, retain full materialization
and record the negative result rather than rescuing the hypothesis post hoc.

## Phase 6F — Proven MAF Runtime Optimization [FUTURE]

Optimization order must compound proven gains:

1. representation correctness
2. compiler efficiency
3. indexed disk retrieval
4. RAM residency/cache behavior
5. selective access
6. native C++ implementation
7. mmap/pread, batching, arenas, prefetch, and copy reduction
8. ARM64/NEON optimization
9. Vulkan optimization

Vulkan work begins only after the MAF object/runtime architecture demonstrates
a measurable advantage or a clearly identified GPU-addressable bottleneck.

Potential Vulkan endpoint:

`disk MAF -> mapped fragment -> RAM MAF cache -> Vulkan MAF cache -> GPU MAF kernel`

Do not use GPU acceleration to justify an otherwise inferior representation
or storage architecture.

## Phase 7 — Fuzzy Logic Routing [RESEARCH]

- Weighted relationship membership
- Contradiction penalties
- Provenance weighting
- Path-cost weighting
- Candidate ranking
- Deterministic fallback

## Phase 8 — Machine Learning Routing [RESEARCH]

- Learn routing weights
- Train from validated outcomes
- Use rejected paths as negative evidence
- Preserve terminated paths
- Calibrate confidence
- Test overfitting
- Test holdout generalization

## Phase 9 — Heatwave and Heightmap Features [RESEARCH]

- Activation density
- Relationship density
- Recurrence
- Convergence
- Height/depth relationships
- Dynamic landscape features
- Feed validated features into ML routing

## Phase 10 — Integrated MAF Brain [RESEARCH]

- MAF cells as heuristic neuron-like firing units
- Node-to-node activation
- Fractal-cell activation
- Relationship propagation
- Sparse routing
- Candidate convergence
- Explicit termination states
- Negative/failure memory

## Phase 11 — Comparative Inference [RESEARCH]

Compare:

- Original GGUF/LLM
- MAF
- Fractal MAF
- MAF + fuzzy routing
- MAF + ML routing
- Integrated fractal MAF
- Native optimized implementation

Measure correctness, tokens, RAM, storage, latency, throughput, CPU, GPU, thermal behavior, and energy where available.

## Phase 12 — Native Componentization [CONTINUOUS]

Every validated phase becomes a small native C++ component.

Experimental Python -> validated algorithm -> C++ component -> tests -> benchmark -> ARM64 optimization -> NEON/Vulkan optimization -> integration

## Phase 13 — Production Candidate [FUTURE]

- Stable native API
- Validated MAF/fractal representation
- Model/representation packaging
- Device-specific execution paths
- Failure handling
- Security review
- Reproducible release process

## Non-Negotiable Research Rules

The Canonical Model GGUF remains the authoritative model artifact.
Derived representations never silently redefine truth.
Provenance survives every transformation.
Rejected, contradictory, pruned, and terminated paths may be retained as negative evidence.
Experimental success requires reproducible benchmark improvement.
No alternative inference system is considered a replacement for an LLM until correctness and generalization are demonstrated.

## Standard Procedure

Define -> Baseline -> Experiment -> Measure -> Holdout -> Validate -> Componentize -> C++ -> Optimize -> Rebenchmark -> Document -> Commit

## Phase 5A — Canonical Model GGUF → MAF Performance Gate [CRITICAL]



Before expanding MAF into a general inference architecture, determine whether

conversion of a copy of the Canonical Model GGUF produces a measurable advantage.



The original Canonical Model GGUF remains immutable and is always the model reference.



### Required comparison



```text

Canonical Model GGUF

       |

       +----> conventional LLM baseline

       |

       +----> MAF representation

```



### Required metrics



- persistent model/representation size

- peak RAM

- working memory

- lookup latency

- initialization time

- prompt tokens

- generated tokens

- total tokens

- throughput

- CPU utilization

- GPU utilization

- thermal behavior where measurable

- energy/resource consumption where measurable

- correctness

- reconstruction fidelity

- repeated-prompt consistency

- holdout accuracy



### Promotion gate



MAF proceeds toward primary inference only if its measured benefits are

reproducible and correctness/generalization remain acceptable.



A reduction in storage, memory, or tokens alone is insufficient if correctness

or generalization materially degrades.



### Negative evidence



The experiment must preserve:



- rejected mappings

- contradictory mappings

- pruned mappings

- failed reconstructions

- terminated paths

- unsuccessful compression candidates



These artifacts may later become training, calibration, routing, or pruning

signals.



### Experimental sequence



```text

GGUF

  -> deterministic extraction

  -> MAF conversion

  -> reconstruction/lookup

  -> baseline comparison

  -> holdout validation

  -> resource benchmark

  -> replication

  -> promotion decision

```



Do not introduce fractalization, fuzzy routing, or ML routing into the primary

comparison until the standalone MAF result has been characterized.

## Forest Morphology Research Program

Status: experimental / Labs only.

The Forest program tests whether biological structural analogies
correspond to measurable representation, storage, routing, or graph
topologies.

Naming is earned experimentally:

> Nature suggests the hypothesis; benchmarks decide the architecture.

Plant names are not canonical implementation claims until controlled
experiments demonstrate a distinct computational advantage.

### Established experimental line

#### Lodgepole

Current role:

- hierarchical shared representation
- trunk/root centroid
- branch/shared residual hierarchy
- terminal packaging and coarse addressability

Status:

- RETAIN
- not deprecated by Orange
- candidate substrate for hybrid Forest architectures

Validated evidence includes:

- Lodgepole Fractal Storage V1
- quantized/storage follow-up experiments
- fair block-addressability controls

#### Orange

Current role:

- correlation-derived non-contiguous terminal wedges
- selective partial representation access
- terminal specialization above or within hierarchical structure

Validated sequence:

- Forest V1:
  Lodgepole vs Orange structural comparison
- Forest V2:
  equivalent block addressability established structural access parity
- Forest V3:
  correlated non-contiguous Orange wedges showed information
  concentration advantage
- Forest V4:
  Orange grouping generalized across complete held-out token IDs
- Forest V5:
  non-oracle layer-conditioned Orange routing passed on held-out tokens

Current Orange result:

- Orange beats Pine/Lodgepole and Random controls at all tested
  partial-access fractions in every held-out fold
- non-oracle router retains most of Oracle performance
- Orange has earned status as a specialized terminal topology
- production storage and retrieval advantage remain unproven

### Active next gate

#### Forest V6 — Quantized Non-Oracle Orange

Priority: ACTIVE.

Question:

Does Orange's held-out non-oracle routing advantage survive realistic
quantized wedge storage?

Primary candidate:

- BLOCK_INT8_64

Controls:

- contiguous Lodgepole/Pine BLOCK_INT8_64
- correlated Orange BLOCK_INT8_64 with non-oracle router
- correlated Orange BLOCK_INT8_64 with Oracle selector

Required measurements:

- encoded payload bytes
- routing metadata bytes
- grouping-map bytes
- total modeled bytes
- compression ratio versus flat FP32
- selected energy fraction
- Orange/Pine selected-energy ratio
- router/Oracle retention
- mean cosine fidelity
- minimum cosine fidelity
- mean relative L2 error
- maximum relative L2 error
- fold-level consistency

Interpretation boundary:

V6 may validate compressed representation quality and routing behavior.
It does not by itself establish mmap, filesystem, latency, or complete
inference-pipeline performance.

### Reserved morphology hypotheses

These experiments are PARKED until the active Orange sequence reaches
its next decision point.

They must not delay Forest V6.

#### Lady Fern / Local Fern Candidate

Candidate computational property:

- repeated hierarchical/self-similar organization
- frond -> pinna -> pinnule -> vein structure
- possible mapping to repeated layer transformations or recurrence

Candidate experiment:

Forest Fern V1 — Cross-Scale Recurrence.

Question:

Can a transformation or displacement model learned at one representation
scale predict structurally similar transformations at another scale
better than independent baselines?

Possible measurements:

- recurrence similarity across scale
- transform reuse
- residual after shared transform
- storage required for reused versus independent transforms
- held-out layer/token generalization

Field-study note:

Prefer a fern species that can be directly observed locally before
formalizing the biological contract.

#### Daisy

Candidate computational property:

- one apparent object composed of many functional florets
- central disk units plus surrounding ray units
- multiple specialized components presented through one interface

Candidate experiment:

Forest Daisy V1 — Composite Representation.

Question:

Can one logical representation be decomposed into multiple small
specialized components around shared support while improving selective
retrieval or reconstruction?

Potential controls:

- monolithic representation
- equal contiguous partition
- random component partition
- learned specialized components

Possible measurements:

- specialization
- redundancy
- selective reconstruction
- component independence
- storage overhead
- routing cost

#### Dandelion

Candidate computational property:

- dense source structure producing many independently distributable
  compact units
- one-to-many packaging and dissemination

Candidate experiment:

Forest Dandelion V1 — Distributed Representation Units.

Question:

Can a representation be encoded into compact independently useful
fragments that preserve useful partial information and combine cleanly
when multiple fragments are recovered?

Possible uses:

- portable MAF fragments
- distributed retrieval
- constrained-device representation transfer
- resumable/sharded representation transport

Measurements:

- independent-fragment utility
- reconstruction versus fragment count
- redundancy
- payload overhead
- loss tolerance
- deterministic recombination

#### Ivy

Candidate computational property:

- traversal and attachment over an already existing support structure
- incremental growth
- opportunistic branching
- path reuse without replacing the host graph

Candidate experiment:

Forest Ivy V1 — Adaptive Graph Overlay.

Question:

Can a learned traversal layer attach to an existing Truth Graph and
improve route selection without becoming a second source of canonical
truth?

Required boundary:

- canonical Truth Graph remains authoritative
- Ivy may rank, traverse, annotate, or cache
- Ivy must not silently mutate canonical truth

Potential measurements:

- route length
- candidate expansion
- retrieval recall
- cache reuse
- overlay size
- stale-route behavior
- provenance preservation

### Morphology experiment order

Current priority order:

1. Forest V6 — quantized non-oracle Orange
2. Forest V7 — production-like Orange indexing / serialization
3. Forest V8 — wall-clock selective retrieval benchmark
4. Evaluate whether Orange should become a production terminal topology
5. Fern recurrence experiment
6. Daisy composite-representation experiment
7. Dandelion distributed-fragment experiment
8. Ivy graph-overlay experiment

This ordering may change if an earlier result falsifies the underlying
hypothesis.

### Current architecture hypothesis

The present evidence favors a hybrid rather than replacement model:

    Forest
      |
      +-- Lodgepole
      |     hierarchy / shared paths / coarse structure
      |
      +-- Orange
            correlated non-contiguous terminal organization

Other morphologies remain candidate specialized structures until their
own controlled experiments earn implementation status.

### Phase 6B Exit / Phase 6C Entry Checkpoint

The frozen completion artifacts supersede the older Phase 6B.9
checkpoint state previously recorded here.

- Phase 6B.7 Atomic Activation is complete and validated.
- Phase 6B.8 Rollback is complete and validated.
- Phase 6B.9 Resident PK Directory is complete, validated, benchmarked, and diagnostically accepted.
- Phase 6B.10 Segment Reader V1 is complete, validated, benchmarked, and diagnostically accepted.
- Phase 6B is complete and closed.
- Phase 6B closure is frozen by `experiments/model_fractal/MAF_SEGMENT_READER_V1_COMPLETION.md`.
- Phase 6C entry is frozen by `experiments/model_fractal/MAF_PHASE_6C_ENTRY_CHECKPOINT.md`.
- Phase 6C is the current research phase.
- No Phase 6C runtime implementation has yet been accepted.

Resident PK Directory V1 is derived immutable process-local state for exactly one model and one active generation.

The minimum logical lookup key is `(model_pk, "object_pk", object_pk)`.

Average O(1) lookup is a design and implementation target until measured by accepted benchmark evidence.
