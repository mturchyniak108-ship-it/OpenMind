# OpenMind AI Agent Documentation

<!-- OPENMIND_MAF_Q4_STATUS_BEGIN -->
## MAF Phase 6D-Q4 status — CLOSED

Phase 6D-Q4 Query Route Cache validation is formally closed on frozen evidence.

- Scientific result: **PASS — 44/44 Q4 checks**.
- Frozen cases: `q001`, `q025`, `q026`, `q033`.
- Frozen runner: `bafed2c9ef6d2cf35d8d5212bbb17497f68a67fff9a67d855ac96243af3ac686`.
- Frozen result: `1be2608271e899d320b4255fccba2e64c1616281110ebb375f803a7f740c43e0` / 9184 bytes.
- Frozen exact-once slot: `af63aa8d3b769ad984b898d805ff45361eb5e079658d47a088514d3ba4145a2d` / 1311 bytes.
- Runner implementation contract: `daa291fcb06c0456e028807308e35ef86486e5176b4fe88d254915718d6943e4`.
- Evidence commit: `b386abde55b1b8f156292eb7500fb739ea8be918`.
- Exact-once history: V1, V1.1, V1.2, and V1.3 are permanently spent and MUST NOT be rerun.
- Durable V1.3 state: `RESERVATION_PREPARED -> RESERVED_DURABLE -> PUBLISHED_DURABLE`; no partial residue.
- Claim scope remains limited to safe generation-bound route-metadata persistence, reuse, and invalidation.
- Not established by Q4: inference execution, answer generation, working-set sufficiency, performance superiority or metrics, output parity, route-expansion optimality, MAF-native compute, or LLM replacement.
- Phase 6E: **READY FOR ENTRY REVIEW — NOT ENTERED**.
- Canonical closure record: `experiments/model_fractal/MAF_QUERY_ROUTE_CACHE_VALIDATION_V1_3_VERDICT.md`.

<!-- OPENMIND_MAF_Q4_STATUS_END -->

<!-- OPENMIND:CURRENT-WORK-LINK:START -->
Current scientific work: [`../research/CURRENT_WORK.md`](../research/CURRENT_WORK.md).
<!-- OPENMIND:CURRENT-WORK-LINK:END -->

<!-- OPENMIND:Q2-V1-4-AGENT-STATUS:START -->
## Current Phase 6D-Q2 Agent Guardrail

The authoritative query-to-PK validation authority is V1.4:

- scientific result: `PASS — 74/74`;
- V01-V74: `ALL PASS`;
- exact-once namespace: `PERMANENTLY SPENT`;
- retry: `FORBIDDEN`;
- result SHA256: `b2ad49d7a9a3e1ef565e07e595efc4a4e00b283f422723553c6437ef3a42def6`;
- verdict SHA256: `c17198e0013fd9c0a8c59b8f09c05d4f22693dc7d56afdc0f761f55a008c2663`;
- freeze commit: `10da372a8317dc629674fb2b52a7560f55ee416f`.

AI collaborators must not:

- import or execute the V1.4 exact-once runner for inspection or documentation;
- create, delete, truncate, repair, replace, or regenerate the V1.4 slot/result;
- rerun V1.4 for any reason;
- extend the Q2 PASS beyond query-to-PK selection validation;
- claim inference, answer generation, selective working-set sufficiency,
  tensor/object avoidance, output parity, answer quality, performance
  superiority, MAF-native compute, or conventional-LLM replacement from Q2.

Q2 V1.4 is closed. Any next Phase 6D-Q experiment requires a separately
preregistered scientific gate. Phase 6E remains not entered.
Next authorized research target: **6D-Q3 — attach/detach ownership and cleanup semantics** under a separate preregistration.

Do not interpret Q2 PASS as selective-working-set sufficiency or Phase 6E entry. Human-readable summary: `../research/Q2_V1_4_SUMMARY.md`.
<!-- OPENMIND:Q2-V1-4-AGENT-STATUS:END -->

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

## Phase 6B MAF Agent Rules

AI collaborators working on Phase 6B must preserve these boundaries:

- treat the canonical active-generation record as current-generation authority;
- treat the immutable generation descriptor as logical-to-physical mapping authority;
- treat Resident PK Directory state as derived and rebuildable;
- never synthesize logical PK identity from path, position, filename, or ordering;
- require current physical validation before resident snapshot publication;
- reject stale generation expectations rather than silently serving old state;
- preserve the prior valid resident snapshot when replacement construction fails;
- keep successful resident lookup free of JSON parsing, manifest scanning, filesystem discovery, and linear descriptor scans;
- preserve source-GGUF independence for resident directory construction and lookup;
- do not claim measured average O(1) performance until benchmark evidence exists;
- do not infer Segment Reader, MAF-native compute, inference replacement, storage-engine selection, or Phase 6C completion from Phase 6B.9 implementation alone;
- do not rerun exact-once validation runners after frozen raw evidence exists.

<!-- OPENMIND:MAF-QUERY-SCOPED-WORKING-SETS-DOCS-AI-README-MD:START -->
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

Architecture document: `../../experiments/model_fractal/MAF_QUERY_SCOPED_WORKING_SET_ARCHITECTURE.md`
<!-- OPENMIND:MAF-QUERY-SCOPED-WORKING-SETS-DOCS-AI-README-MD:END -->
