# OpenMind Roadmap

## Current Direction

OpenMind is an experimental native AI platform investigating whether useful AI computation can be performed with substantially reduced dependence on conventional token-based inference.

The project combines native local LLM inference, Qwen/GGUF analysis, representation and vector analysis, cross-prompt consistency testing, transition-vector analysis, quantitative benchmarking, robust testing, AI-assisted development, and experimental fractal/MAF representations.

## Phase 1 — Native Local Inference [COMPLETE]

- Native llama.cpp integration
- GGUF model loading
- Android/ARM64 execution
- Vulkan GPU acceleration
- Local Qwen inference
- Native smoke testing

## Phase 2 — Representation Analysis [ACTIVE]

- Capture model representations
- Compare independently generated representations
- Measure layer-to-layer recurrence
- Analyze transition vectors
- Quantify cross-prompt consistency
- Establish reproducible statistical baselines
- Identify stable representation structures

## Phase 3 — Representation-Based Computation [ACTIVE]

Investigate whether useful computation can be performed using representations and vectors rather than conventional token-by-token processing.

Goals:

- Representation lookup structures
- Reusable representation states
- Efficient transition mechanisms
- Representation benchmarking
- Comparison against conventional inference
- Measurable accuracy and performance criteria

## Phase 4 — MAF / Fractal Research [EXPERIMENTAL]

MAF is experimental research infrastructure.

The current native `maf_basic` executable:

- Runs natively on Android ARM64
- Loads `pi_10M.txt`
- Stores decimal digits in memory
- Performs O(1) lookup
- Provides benchmark, bombardment, accuracy and torture tests

MAF is currently NOT a Qwen model format or replacement LLM.

The advanced GGUF/fractal path is the important bridge between model data and experimental representation analysis.

Next objectives:

- Validate GGUF ingestion
- Extract useful model representations
- Transform representations into experimental MAF/fractal structures
- Benchmark memory and lookup performance
- Compare representation fidelity against source model data
- Determine whether useful computational information is preserved

## Phase 5 — Low-Token Inference [RESEARCH]

Investigate whether representation reuse and structured transitions can reduce conventional token processing.

Targets:

- Reduced token consumption
- Representation caching
- State reuse
- Vector/transition lookup
- Structured inference pathways
- Quantitative comparison against conventional inference

## Phase 6 — Tokenless / Alternative Inference [LONG-TERM RESEARCH]

Investigate whether useful AI computation can operate without conventional token-by-token generation for selected workloads.

Potential approaches:

- Vector-native computation
- Representation traversal
- Learned transition structures
- Hierarchical state maps
- Anchor/state lookup
- Fractal representations
- Hybrid token/representation inference

Success criteria:

- Accuracy
- Generalization
- Reproducibility
- Latency
- Memory consumption
- Energy/resource efficiency

## Phase 7 — AI Engineering Agent [PLANNED]

Use local Qwen Coder as an engineering and evaluation agent.

Pipeline:

Qwen Coder
→ Repository analysis
→ Proposed change
→ Implementation
→ Automated tests
→ Benchmark
→ Regression analysis
→ AI-assisted review
→ Next experiment

AI-generated changes remain subject to automated testing, benchmarking and validation.

## Phase 8 — Comparative Benchmarking [PLANNED]

Compare OpenMind approaches against conventional LLM inference.

Measure:

- Tokens processed
- Output quality
- Latency
- Memory
- CPU utilization
- GPU utilization
- Energy/resource usage
- Representation stability
- Accuracy
- Reproducibility

The objective is evidence-based comparison rather than assuming alternative inference is superior.

## Phase 9 — Production Candidate [FUTURE]

After experimental validation:

- Stable inference API
- Model/representation packaging
- Reproducible benchmark suite
- Device compatibility
- Failure handling
- Documentation
- Security review
- Release engineering

## Research Principle

Build → Test → Measure → Debug → Reproduce → Improve

Experimental results must remain clearly separated from validated capabilities.


## Licensing and Open-Source Strategy

OpenMind original software is released under Apache License 2.0.

Original research datasets and results may be released under CC BY 4.0
when explicitly marked.

Third-party code, libraries, models and datasets retain their respective
upstream licenses.

OpenMind follows an open-source-first engineering model: established
open-source projects are used as foundations, studied, integrated,
extended and tested while preserving applicable upstream licensing.

Licensing must remain separate from experimental claims. Open-source
availability does not imply that experimental inference methods have been
validated as replacements for conventional LLMs.
