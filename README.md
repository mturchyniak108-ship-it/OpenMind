# OpenMind

<!-- OPENMIND:CURRENT-SCIENTIFIC-STATUS:START -->
## Current Scientific Status

- Phase 6B/6C: closed
- Phase 6D: active
- Phase 6D-Q2: authoritative V1.4 query-to-PK selection validation PASS — 74/74
- Phase 6E: not entered
- V1.4 protocol SHA256: `a814bca93a6b014ee53aad234b8396c841d0efc2a9363598e8a2192f23745699`
- frozen V1.4 runner commit: `d9056941f2db77f521222f38b125927ae16bbf3e`
- V1.4 runner SHA256: `7bda960c125786fdf3cfca65c4b7b5851ca8bd91257282facfee2fec1ae7a030`
- static closure audit: `0 critical findings`
- post-freeze self-SHA finding: `CLOSED — audit matcher false-negative`
- authoritative Q2 run: `PASS — 74/74`
- V01-V74: `ALL PASS`
- exact-once result slot: `SPENT`
- authoritative result SHA256: `b2ad49d7a9a3e1ef565e07e595efc4a4e00b283f422723553c6437ef3a42def6`
- authoritative verdict SHA256: `c17198e0013fd9c0a8c59b8f09c05d4f22693dc7d56afdc0f761f55a008c2663`
- authoritative freeze commit: `10da372a8317dc629674fb2b52a7560f55ee416f`

Runner freeze and static-audit completion are not a scientific PASS or FAIL.
Q2 V1.4 is closed and must not be rerun. Any next Phase 6D-Q experiment requires a separate preregistered gate; Phase 6E remains not entered.
Current authority: `docs/research/CURRENT_WORK.md`.
<!-- OPENMIND:CURRENT-SCIENTIFIC-STATUS:END -->

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

#### Current MAF engineering state

OpenMind's current MAF engineering status is determined from frozen completion,
validation, benchmark, diagnostic, and scientific-verdict artifacts rather than
from roadmap intent alone.

Current accepted state:

- **Phase 6B — MAF Persistent Object Pipeline — COMPLETE / CLOSED.**
- Atomic Activation is complete and validated.
- Rollback is complete and validated.
- Resident PK Directory is complete, validated, benchmarked, and diagnostically accepted.
- Segment Reader V1 is complete, validated, benchmarked, and diagnostically accepted.
- **Phase 6C — MAF Object Runtime and Residency — CLOSED / PASS** for its
  preregistered runtime/residency correctness surface.
- The Phase 6C performance verdict is **NONE** and no Phase 6C benchmark was
  executed as part of that scientific closure.
- **Phase 6D — Segment Locality and Path-Aware Repacking — ACTIVE RESEARCH.**
- The Phase 6D locality data-model implementation and Validation V1 result are
  accepted and frozen with a PASS result.
- Telemetry snapshot persistence Validation V1.3 is **PASS / accepted / frozen**
  for its preregistered V01-V57 correctness surface.
- No telemetry persistence benchmark was executed and its performance verdict is
  **NONE**.
- Runtime telemetry integration and real-model telemetry collection remain
  separately gated Phase 6D research.
- Phase 6D-Q query-scoped MAF working sets remain **PROPOSED — NOT VALIDATED**.

The Resident PK Directory remains derived process-local state rather than
canonical authority. Authority remains bound to the active-generation record
and immutable generation artifacts.

MAF engineering results do not currently establish MAF-native inference, a
replacement for `llama.cpp` or another language-model runtime, or a general
performance advantage over conventional inference.

All performance and correctness claims remain bounded to the exact workloads,
artifacts, devices, versions, controls, and validation scopes that produced
their accepted evidence.

<!-- OPENMIND:MAF-QUERY-SCOPED-WORKING-SETS-README-MD:START -->
## Proposed query-scoped MAF execution architecture

OpenMind now tracks a proposed **Phase 6D-Q** research direction in which an
input is compiled into a bounded PK working set over canonical MAFDB objects.

The proposed design separates canonical MAFDB authority from a temporary
Query-Scoped MAF Capsule and a persistent derived Query Route Cache. A query may
start from an initial PK set, expand deterministically when required, answer,
release its temporary working state, and retain only compact reusable route
metadata for future exact or similar queries.

This is a roadmap architecture, **not a validated inference capability**.
Selective sufficiency, object/tensor avoidance, output parity, route reuse, and
performance all require separate prospective experiments.

Architecture document: `./experiments/model_fractal/MAF_QUERY_SCOPED_WORKING_SET_ARCHITECTURE.md`
<!-- OPENMIND:MAF-QUERY-SCOPED-WORKING-SETS-README-MD:END -->
