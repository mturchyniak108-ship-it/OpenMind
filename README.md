# OpenMind

OpenMind is a local-first AI systems project focused on native inference, evidence-backed knowledge structures, reproducible model research, and experimental representation-driven computation.

The long-term research question is whether useful AI computation can be performed with less dependence on conventional token-by-token inference while preserving correctness, provenance, and reproducibility.

OpenMind deliberately separates implemented capabilities from active research. Experimental results are not presented as production features until they complete the project's validation and promotion process.

## Current Status

### Implemented Foundations

OpenMind currently includes:

- native local GGUF inference through llama.cpp;
- Vulkan GPU acceleration on supported hardware;
- a native C++ inference API;
- stateless and persistent inference sessions;
- batch generation support;
- session reset and lifecycle management;
- a canonical Truth Graph data model;
- Truth Nodes, Truth Edges, and Truth Paths;
- Truth Graph persistence;
- evidence registries and evidence bindings;
- provenance-aware truth tracing;
- evidence coverage and edge resolution;
- ingestion infrastructure;
- Python regression and integration tests;
- reproducible benchmark and experiment infrastructure.

## Verified Native Inference Baseline

A verified local inference baseline has been recorded on:

- Device: Samsung Galaxy S26 Ultra
- GPU: Adreno 840
- Backend: Vulkan using Mesa Turnip
- Model: Qwen 2.5 3B Q4_K_M
- Context: 512
- GPU layers requested: 99
- Prompt speed: 21.95 tokens/second
- Generation speed: 17.34 tokens/second
- Native Vulkan inference: PASS

See `benchmarks/baseline-qwen25-3b-vulkan.txt`.

Performance results describe the recorded workload and environment. They should not be generalized to unlike models, devices, prompts, or runtime configurations without measurement.

## Active Research

### Representation Discovery

Current research investigates internal model representations, including activation capture, cross-layer recurrence, transition vectors, token-specific topology, cross-prompt consistency, reconstruction, controls, and permutation tests.

This work asks whether stable or reusable representation structure exists. Similarity measurements alone do not establish equivalent information or equivalent computation.

### MAF

MAF research investigates whether model-derived information can be stored, indexed, retrieved, reconstructed, streamed, or routed more efficiently.

Current experimental areas include indexed access, reconstruction, neighborhood search, scaling, workload benchmarks, cross-prompt holdouts, and hierarchical organization.

MAF engineering results do not by themselves establish a replacement for a language model.

### Lodgepole

Lodgepole is an experimental hierarchical MAF structure inspired by a tree: shared structure is represented toward the root and branches while increasingly specific information appears toward terminal leaves or needles.

Current experiments use hierarchical grouping, centroids, routing, and residual representations to investigate search and storage behavior.

Lodgepole storage and routing remain laboratory research.

## Truth Graph and Evidence

The canonical Python architecture provides TruthNode, TruthEdge, TruthPath, TruthGraph, TruthTrace, evidence registries, evidence bindings, edge evidence resolution, coverage, persistence, and provenance-aware tracing.

The Truth Graph is intended to preserve explicit relationships between information while keeping evidence and provenance traceable.

## Native Inference API

The native C++ layer provides an `InferenceEngine` with model/runtime ownership, stateless generation, persistent sessions, configurable session capacity, batch generation, independent session lifecycle, session reset, inference metrics, and llama.cpp-backed execution.

The public native interface is defined in `native/include/openmind/inference.h`.

## Project Status Language

OpenMind uses explicit evidence classes:

- `canonical` — implemented behavior supported by source code and appropriate tests.
- `validated_research` — experimental evidence that has completed its defined reproducibility, control, validation, limitation, and promotion requirements.
- `lab_candidate` — active experimental work that has not completed promotion.
- `historical` — superseded research retained for provenance and methodology.

A script, benchmark, roadmap entry, successful-looking output, or AI interpretation is not automatically an implemented capability.

## Human and AI Collaboration

OpenMind is developed by human contributors working with AI systems as engineering collaborators.

AI collaborators may inspect code, analyze failures, propose changes, design tests, interpret benchmarks, assist with debugging, and help write documentation.

Only human contributors apply source-code modifications and decide what enters the repository.

See `AGENTS.md` and `docs/development/BEST_PRACTICES.md`.

## Repository Guide

- `openmind/` — Python implementation and canonical project logic
- `native/` — native C++ inference integration
- `tests/` — automated Python tests
- `benchmarks/` — preserved performance baselines
- `experiments/` — research and experimental implementations
- `results/` — experiment and validation outputs
- `docs/` — human and AI documentation
- `preflight/` — device and environment inspection
- `vulkan/` — Vulkan capability probing
- `llama.cpp/` — external inference dependency

Experimental files are not automatically canonical simply because they are present in the repository.

## Getting Started

New contributors should begin with:

1. `docs/getting-started/README.md`
2. `docs/getting-started/GLOSSARY.md`
3. `docs/README.md`
4. `docs/architecture/ARCHITECTURE.md`
5. `docs/development/BEST_PRACTICES.md`

Researchers should also read `docs/labs/README.md`, `docs/experiments/EXPERIMENT_WORKFLOW.md`, `docs/experiments/VALIDATION.md`, and `docs/data/REPRODUCIBILITY.md`.

## Development

OpenMind's Python package requires Python 3.10 or newer.

Basic validation commonly includes:

```bash
python -m compileall -q .
git diff --check
pytest -q
```

Run focused tests before broad regression testing whenever practical.

Native C++ changes should use the relevant CMake build and CTest targets.

See `docs/development/` for development, testing, documentation, and contribution guidance.

## Research Principles

OpenMind research follows several non-negotiable rules:

- preserve canonical source artifacts;
- preserve provenance through transformations;
- separate discovery from validation;
- use controls and baselines;
- retain useful negative evidence;
- record failures rather than rewriting them as successes;
- compare like workloads;
- require correctness and generalization before claiming replacement;
- measure performance rather than assuming optimization;
- distinguish observation from interpretation.

The broader research sequence is documented in `ROADMAP.md`.

## Licenses

OpenMind software source code is licensed under the Apache License 2.0.

Original OpenMind research datasets, benchmark results, measurements, and other materials explicitly marked for research-data release use Creative Commons Attribution 4.0 International (CC BY 4.0).

Third-party software, models, datasets, and artifacts retain their applicable upstream licenses.

See `LICENSE`, `RESEARCH_DATA_LICENSE.md`, and `THIRD_PARTY_LICENSES.md`.

#### Phase 6B — current MAF engineering state

Phase 6B is building the catalog, immutable-generation, activation, rollback, and resident-lookup layer required before MAF can be treated as a runtime model-object system.

Current frozen research status:

- Atomic Activation is complete and validated.
- Rollback is complete and validated.
- Resident PK Directory V1 protocol and implementation are frozen.
- Resident PK Directory Validation V1 is preregistered and frozen but has not yet been executed.
- Segment Reader validation has not started.
- Phase 6C runtime and residency work has not started.

The Resident PK Directory is derived process-local state, not authority. Authority remains the active-generation record plus the immutable active generation descriptor.

The minimum V1 resident lookup key is model-scoped canonical `object_pk` identity. Successful lookup is generation-bound and returns immutable segment, offset, length, object-hash, and runtime-path evidence.

The implementation is designed for direct average O(1) resident lookup with no JSON parsing, manifest scan, filesystem discovery, or linear descriptor scan on the successful hot path. This remains an implementation target until benchmark evidence is frozen.

Phase 6B does not yet claim MAF-native inference, a replacement for `llama.cpp`, a production storage engine, or Segment Reader implementation.
