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
