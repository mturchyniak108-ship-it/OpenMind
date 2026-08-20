# preflight/

## Purpose

Contains OpenMind host and resource discovery tools used before native inference builds and benchmarks.

Preflight establishes the actual capabilities of the execution environment instead of relying on assumptions.

## Files

### preflight.sh

Performs general environment validation and reports required commands, packages, system information, and available resources.

Use this before beginning a new OpenMind build or when diagnosing environment-dependent failures.

### resource_profile.sh

Collects a more detailed resource profile of the current environment.

Use it when determining appropriate model size, context limits, build configuration, concurrency limits, or workload placement.

### report.txt

Captured output from a preflight run.

Treat this as historical environment evidence rather than live system state.

### resource_profile.txt

Captured detailed resource information from a resource-profile run.

Use it to understand the environment that existed when the report was generated.

## Agent Usage

Before changing resource-sensitive OpenMind components:

1. Inspect the current device and resource profile.
2. Verify required commands and packages.
3. Confirm available memory.
4. Confirm compiler and build tooling.
5. Confirm SQLite availability when the knowledge/index layer requires it.
6. Confirm GPU/Vulkan capabilities separately with the Vulkan probe.

## Architectural Role

Preflight is discovery infrastructure.

It should not make architectural decisions automatically.

Its purpose is to provide facts that higher-level components can use when selecting configurations.

The intended dependency direction is:

```text
Preflight
   |
   v
Resource / capability profile
   |
   +----> Native inference configuration
   |
   +----> Model selection
   |
   +----> Workload placement
   |
   +----> Knowledge/index sizing
```

## Knowledge-System Relevance

The future Truth Graph and specialized vector index must respect the physical constraints reported by preflight.

Examples include:

- Available RAM limits graph/index size.
- Storage capacity limits persistent knowledge databases.
- CPU capability affects graph compilation workloads.
- GPU capability affects embedding and inference workloads.
- Available concurrency affects background compilation.

## Vivobook Role

The Vivobook is intended to become the heavier knowledge-processing and compilation environment.

Preflight information on the Vivobook should therefore guide:

- Large-scale embedding generation
- Truth-graph construction
- Graph analysis
- Path compilation
- Specialized index construction
- Regression benchmarks

## Agent Rule

Do not treat captured report files as current hardware state without verifying the live environment.

When a decision depends on current resources, rerun the appropriate preflight script.
