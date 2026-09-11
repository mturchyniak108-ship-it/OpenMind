# MAF Command Reference

## Purpose

This manual describes the currently verified command-line and development surfaces in OpenMind.

Commands are grouped by status so users do not accidentally treat research scripts as supported interfaces.

## Command Status Classes

### Canonical Command

A user-facing command backed by canonical MAF implementation.

### Development Tool

A command used to build, test, benchmark, inspect, or operate MAF during development.

### Diagnostic Tool

A command that inspects the local environment or hardware without defining canonical project behavior.

### Experimental / Lab Command

A research command under `experiments/`.

Lab commands may be incomplete, superseded, computationally expensive, or tied to specific research artifacts. Their existence does not make them supported production interfaces.

## General Rule

Run commands from the repository root unless a section explicitly says otherwise.

```bash
cd ~/OpenMind
```

Human contributors apply source-code changes and decide what enters the repository. AI collaborators may inspect output, propose commands, analyze failures, and suggest changes for human review.

## Canonical Truth CLI

**Status:** Canonical Command

Module:

`openmind.cli.truth`

Purpose:

Resolve a canonical path through the current demonstration Truth Graph while reporting relationship weights, evidence status, canonical score, provenance coverage, and provenance gaps.

### Syntax

```bash
python -m openmind.cli.truth <start_node> <end_node>
```

The command requires exactly two node identifiers.

If the start or end node is unknown, or no canonical path can be resolved, it returns:

```text
NO CANONICAL PATH
```

### Data Source

The current CLI loads its canonical demonstration data from:

`demo/truth_graph/`

This includes the graph, evidence registry, and evidence bindings used by the implemented truth-trace pipeline.

### Human-Readable Output

Successful output includes:

- start node;
- end node;
- resolved path;
- relationship type and weight for every edge;
- evidence identifier and evidence status;
- canonical path score;
- registered, unbound, and missing evidence counts;
- provenance coverage;
- explicit provenance gaps.

### Programmatic JSON Interface

The same module currently exposes the Python function:

`report_json(start, end)`

It returns an exit/status code and deterministic JSON report for programmatic use.

This is currently a Python API surface rather than a separate command-line flag.

## Python Validation Commands

**Status:** Development Tool

### Compile Python Sources

```bash
python -m compileall -q .
```

Purpose: detect Python syntax/compilation failures across the repository.

### Check Git Whitespace

```bash
git diff --check
```

Purpose: detect whitespace errors in modified tracked content.

### Run Python Tests

```bash
pytest -q
```

Purpose: execute the Python test suite.

Use focused tests before the full suite when diagnosing a specific component.

Example:

```bash
pytest -q tests/test_truth_graph.py
```

A passing test establishes only the behavior covered by that test.

## Native Build Commands

**Status:** Development Tool

The current native project is defined by:

`native/CMakeLists.txt`

### Build Existing Native Configuration

```bash
cmake --build native/build -j2
```

The current native CMake project defines these targets:

- `openmind_inference` — static native inference library;
- `openmind_inference_test` — integration test executable;
- `openmind_inference_benchmark` — inference benchmark executable;
- `openmind_activation_probe` — activation capture and representation-analysis executable.

The currently observed build tree contains:

```text
native/build/openmind_activation_probe
native/build/openmind_inference_benchmark
native/build/openmind_inference_test
```

## Native Integration Tests

**Status:** Development Tool

CTest is enabled by the native CMake project.

The native inference test is registered when `OPENMIND_TEST_MODEL` is configured.

### Run Registered Native Tests

```bash
ctest --test-dir native/build --output-on-failure
```

The recorded Termux build currently configures `OPENMIND_TEST_MODEL` to a local Qwen 2.5 3B Q4_K_M GGUF path.

Model paths are environment-specific.

## Activation Probe

**Status:** Development / Research Tool

Build only the activation probe with:

```bash
cmake --build native/build --target openmind_activation_probe -j2
```

A currently documented invocation is:

```bash
native/build/openmind_activation_probe ~/qwen2.5-coder-q8_0.gguf "The purpose of this experiment is to measure representation recurrence across transformer layers."
```

The activation probe captures internal model representations and therefore belongs to the representation-research workflow even though the executable itself is built by the native project.

For reproducible captures, record the model identity and hash, prompt, build/revision state, output artifact, dimensions, and relevant environment information.

See `docs/experiments/ACTIVATION_CAPTURE.md`.

## Native Inference Benchmark

**Status:** Development / Benchmark Tool

Executable:

`native/build/openmind_inference_benchmark`

Use this executable only with a workload and model configuration whose command contract has been verified for the current source revision.

Benchmark results should record model identity, hardware, runtime revision, workload, configuration, repetitions, and relevant resource conditions.

Do not compare unlike workloads without documenting the differences.

## Native Inference Integration Test Executable

**Status:** Development Tool

Executable:

`native/build/openmind_inference_test`

Normally prefer the registered CTest invocation when validating the configured build:

```bash
ctest --test-dir native/build --output-on-failure
```

## Preflight Tools

**Status:** Diagnostic Tool

The `preflight/` directory currently contains:

```text
preflight.sh
resource_profile.sh
report.txt
resource_profile.txt
```

The `.sh` files are executable diagnostic scripts. The `.txt` files are captured output artifacts and should not be mistaken for current machine state.

### System Preflight

```bash
bash preflight/preflight.sh
```

Purpose: inspect the development environment and required system capabilities.

### Resource Profile

```bash
bash preflight/resource_profile.sh
```

Purpose: inspect hardware, software, memory, storage, and other resource characteristics relevant to MAF development.

Environment reports are snapshots. Rerun diagnostics when current state matters.

## Vulkan Probe

**Status:** Diagnostic Tool

Script:

`vulkan/probe.sh`

Run with:

```bash
bash vulkan/probe.sh
```

The probe currently reports or attempts to inspect:

- Android device identity;
- SoC information;
- architecture;
- Android GPU properties;
- system GPU libraries;
- `vulkaninfo` availability and summary;
- `vkmark` availability;
- Termux Vulkan libraries;
- Vulkan ICD files;
- `/dev/dri` visibility;
- relevant Vulkan, Mesa, GPU, EGL, ICD, and Termux environment variables;
- OpenCL availability through `clinfo`.

The Vulkan probe is diagnostic. Its output does not itself prove that a particular MAF model workload will execute correctly.

## Git Inspection Commands

**Status:** Development Tool

Useful read-only repository checks include:

```bash
git status --short
git diff --stat
git diff --check
git log -5 --oneline --decorate
```

Before committing, humans should inspect the exact staged content:

```bash
git diff --cached --name-status
git diff --cached --check
git diff --cached --stat
```

## Experimental Model-Fractal Commands

**Status:** Experimental / Lab Command

The directory `experiments/model_fractal/` contains a large research surface.

These scripts are not a stable CLI API.

Current research families include:

### Representation Recurrence

- `all_token_recurrence.py`;
- `recurrence_controlled_baseline_v1.py`;
- `recurrence_controls_v1.py`;
- `recurrence_controls_v2.py`;
- `recurrence_structure_analysis.py`;
- `recurrence_token_topology_v1.py`;
- `recurrence_token_topology_v2.py`;
- `recurrence_topology_v1.py`;
- `recurrence_topology_v2.py`;
- `recurrence_topology_v3.py`;
- `recurrence_topology_v4_fast.py`;
- `transition_recurrence.py`.

### Cross-Prompt Research

- `cross_prompt_baseline_v1.py`;
- `cross_prompt_recurrence_v1.py`;
- `maf_cross_prompt_holdout_v1.py`.

### Lodgepole Research

- `maf_lodgepole_v1.py`;
- `maf_lodgepole_v2.py`;
- `maf_lodgepole_v3.py`;
- `lodgepole_fractal_storage_v1.py`;
- `benchmark_lodgepole_scaling_v1.py` through later versions;
- `benchmark_lodgepole_vs_flat_v1.py` and later versions.

### MAF Engineering

- indexed-access benchmarks;
- workload benchmarks;
- reconstruction benchmarks;
- neighborhood experiments;
- streaming experiments;
- MAF representation and index builders;
- MAF validation tools.

### Validation Utilities

- `validate_gguf_tensors_v1.py`;
- `validate_maf_index_v1.py`;
- `validate_topology_v3_v4.py`.

## Running Lab Scripts

Do not run an unfamiliar lab script solely because it exists.

First inspect:

1. its input paths;
2. model requirements;
3. expected runtime;
4. memory requirements;
5. output paths;
6. whether it overwrites an artifact;
7. experiment status;
8. provenance requirements;
9. whether another process is already consuming substantial CPU or GPU resources.

The general invocation form is usually:

```bash
python experiments/model_fractal/<script>.py
```

but the source file and associated experiment documentation are authoritative for each research command.

## Long-Running Experiments

For a known process ID, inspect status with:

```bash
ps -o pid,etime,time,%cpu,%mem,cmd -p <PID>
```

Important fields:

- `ELAPSED` — wall-clock time since process start;
- `TIME` — accumulated CPU time;
- `%CPU` — current CPU utilization;
- `%MEM` — memory percentage;
- `CMD` — process command.

When standard output is redirected to a file, output may remain empty while Python is still running because file output can be buffered.

An empty output file alone therefore does not prove a process is stalled.

## Status and Evidence Rules

Commands under `experiments/` remain research commands unless explicitly promoted.

Successful execution means the command ran successfully. It does not automatically establish that the experiment hypothesis is true.

Research interpretation should follow:

- `docs/labs/README.md`;
- `docs/experiments/EXPERIMENT_WORKFLOW.md`;
- `docs/experiments/VALIDATION.md`;
- `docs/ai/EXPERIMENT_PROMOTION.md`;
- `docs/data/REPRODUCIBILITY.md`.

## Related Manuals

- `docs/getting-started/README.md` — project introduction;
- `docs/getting-started/INSTALLATION.md` — installation and build environment;
- `docs/getting-started/GLOSSARY.md` — MAF terminology;
- `docs/development/BEST_PRACTICES.md` — engineering workflow;
- `docs/operations/OPERATIONS.md` — operational guidance.
