# OpenMind AI Agent Documentation

## Purpose

This directory contains machine-readable documentation for AI agents, repository scrapers, coding agents, and maintainers.

The documentation explains what each OpenMind-owned file does, how components connect, what inputs and outputs they use, and which architectural invariants must be preserved.

## Agent Rules

Before modifying OpenMind:

1. Read README.md.
2. Read ROADMAP.md.
3. Read docs/ai/README.md.
4. Read documentation for files being modified.
5. Inspect related tests.
6. Preserve architectural invariants.
7. Run git diff --check.
8. Rebuild affected targets.
9. Run CTest.
10. Update documentation when behavior changes.

## Repository Ownership

### OpenMind-owned

- native/
- benchmarks/
- preflight/
- vulkan/
- docs/
- ROADMAP.md
- README.md
- Repository build and configuration files

### External Dependency

- llama.cpp/

Do not rewrite or duplicate upstream llama.cpp documentation into the OpenMind AI documentation layer unless OpenMind directly depends on a specific upstream API or behavior.

## Documentation Structure

docs/ai/
├── README.md
├── architecture.md
├── invariants.md
├── data-model.md
├── retrieval.md
├── agents.md
├── files/
│   ├── README.md
│   ├── native/
│   ├── benchmarks/
│   ├── preflight/
│   └── vulkan/
└── generated/
    └── file-index.md

## File Documentation

Each OpenMind-owned source file should eventually have an AI-readable documentation entry describing its purpose, interfaces, dependencies, inputs, outputs, tests, usage, and architectural constraints.

## AI Agent Workflow

AI agents working on OpenMind should follow this sequence:

1. Identify the requested subsystem.
2. Read the relevant roadmap milestone.
3. Read the subsystem architecture documentation.
4. Read the AI documentation for affected files.
5. Inspect the current implementation before proposing changes.
6. Inspect existing tests and benchmarks.
7. Make the smallest change that satisfies the requirement.
8. Preserve public interfaces unless the roadmap explicitly requires an interface change.
9. Add or update regression tests.
10. Run formatting and validation checks.
11. Update affected AI documentation.
12. Report files changed, tests run, and remaining risks.

## File Documentation Contract

Every documented source file should describe:

- Purpose
- Architectural role
- Dependencies
- Public interfaces
- Important internal structures
- Inputs
- Outputs
- State changes
- Error behavior
- Thread-safety requirements
- Persistence requirements
- Related tests
- Related benchmarks
- Related roadmap milestones
- Safe modification boundaries

## Scraper Guidance

Repository scrapers should treat README.md, ROADMAP.md, and docs/ai/ as the primary architectural index.

Source code remains authoritative for implementation behavior.

Tests remain authoritative for verified behavior.

Benchmarks remain authoritative for measured performance.

ROADMAP.md describes intended future architecture and must not be interpreted as implemented functionality unless the corresponding source and tests confirm it.

## Truth-Graph Architecture

The planned knowledge architecture represents known truths independently from natural language.

TruthNode represents a language-independent semantic truth.
TruthEdge represents a relationship between truths.
TruthPath represents a candidate route between semantic start and end nodes.
PathWeight represents the confidence and cost of a candidate route.

Natural-language expressions should reference semantic truths rather than creating separate truths for every language.
