# OpenMind Roadmap

## Mission

OpenMind investigates whether useful AI computation can be performed through a local, native, representation-driven architecture that can reduce dependence on conventional token-by-token inference while preserving correctness and provenance.

The project treats the Canonical Model GGUF as the canonical model/reference artifact and evaluates MAF, fractal MAF, vector maps, fuzzy logic, machine learning, heatwave/heightmap relationships, and native optimized execution as derived computational systems.

## Core Architecture

Canonical Model GGUF -> Truth Map -> Relationship Map + Provenance Map + Landscape Map -> Vector Links -> MAF -> Fuzzy/ML Routing -> Fractal MAF -> Validation -> Native C++ -> ARM64/NEON/Vulkan Optimization

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
