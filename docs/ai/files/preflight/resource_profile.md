# preflight/resource_profile.sh

## Purpose

Profiles the available system resources so OpenMind workloads can be matched to the actual device capabilities.

## Responsibilities

- Inspect available memory.
- Inspect CPU information.
- Inspect storage information.
- Inspect installed development tooling.
- Record relevant resource limits.
- Produce a reproducible resource profile.

## Output

The generated report is:

preflight/resource_profile.txt

## Usage

cd ~/OpenMind
bash preflight/resource_profile.sh

## Architectural Importance

Resource profiling determines which work should execute on the Samsung Galaxy S26 Ultra and which work should be delegated to the Vivobook.

### Samsung Galaxy S26 Ultra

Preferred for interactive local inference, session management, query handling, and lightweight runtime operations.

### Vivobook

Preferred for heavier preprocessing, embedding generation, Truth Graph construction, graph analysis, path discovery, index construction, and compiled heuristic mapping.

## Knowledge-System Relevance

Resource measurements will eventually influence:

- Vector index size.
- Embedding batch size.
- Graph construction batch size.
- Path-search limits.
- Mapping compilation workload.
- Cache sizes.
- Memory residency decisions.

## Agent Guidance

Do not assume that a workload is suitable for a device based only on CPU model or advertised memory.

Use the actual resource profile before selecting model sizes, batch sizes, indexing strategies, or compilation workloads.

The profile is diagnostic data and should not be treated as a permanent hardware specification.
