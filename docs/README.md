# OpenMind Documentation

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
Current scientific work: [`research/CURRENT_WORK.md`](research/CURRENT_WORK.md).
<!-- OPENMIND:CURRENT-WORK-LINK:END -->

<!-- OPENMIND:CURRENT-AUTHORITY:START -->
Current scientific authority: `research/CURRENT_WORK.md` and `research/MAF_CURRENT_STATUS.md`.
<!-- OPENMIND:CURRENT-AUTHORITY:END -->

OpenMind is a local-first AI systems project combining native inference, evidence-backed knowledge structures, reproducible model research, and experimental representation engineering.

These documents are written for people first while remaining structured enough for AI collaborators to navigate reliably.

## Start Here

- [Getting Started](getting-started/README.md)
- [Installation and Build](getting-started/INSTALLATION.md)
- [Command Reference](getting-started/COMMAND_REFERENCE.md)
- [Glossary](getting-started/GLOSSARY.md)

If you are new to OpenMind:

1. Read the project `README.md` for the high-level project status.
2. Read [Architecture](architecture/ARCHITECTURE.md) for the system model.
3. Read [Development](development/DEVELOPMENT.md) before changing code.
4. Read [Best Practices](development/BEST_PRACTICES.md) for the shared human/AI engineering workflow.
5. Read [OpenMind Labs](labs/README.md) before interpreting experimental work.

## Who These Documents Are For

### Users

Users need installation, operation, configuration, troubleshooting, and stable feature documentation.

Human-oriented getting-started and manual pages are being expanded as OpenMind interfaces stabilize.

### Developers

Developers should begin with:

- [Development](development/DEVELOPMENT.md)
- [Contributing](development/CONTRIBUTING.md)
- [Testing](development/TESTING.md)
- [Documentation Standards](development/DOCUMENTATION.md)
- [Best Practices](development/BEST_PRACTICES.md)

### Researchers

Research work must distinguish observation from interpretation and validated evidence from active laboratory work.

Begin with:

- [Experiment Workflow](experiments/EXPERIMENT_WORKFLOW.md)
- [Validation and Holdouts](experiments/VALIDATION.md)
- [Representation Analysis](experiments/REPRESENTATION_ANALYSIS.md)
- [MAF Research](experiments/MAF.md)
- [Data and Provenance](data/DATA_AND_PROVENANCE.md)
- [Reproducibility](data/REPRODUCIBILITY.md)
- [OpenMind Labs](labs/README.md)

### AI Collaborators

AI agents work alongside human contributors. They may inspect, analyze, explain, review, debug, test, benchmark, and propose changes.

Only a human contributor may apply modifications to OpenMind source code or decide that a proposed change enters the repository.

AI-specific navigation and repository rules are under [AI Documentation](ai/README.md).

## Documentation Map

### Architecture

- [System Architecture](architecture/ARCHITECTURE.md)
- [Authority and Terminology](architecture/AUTHORITY_AND_TERMINOLOGY.md)
- [Inference Pipeline](architecture/INFERENCE_PIPELINE.md)
- [Representation Pipeline](architecture/REPRESENTATION_PIPELINE.md)

### Experiments and Research

- [All-Token Activation Capture](experiments/ACTIVATION_CAPTURE.md)
- [Experiment Workflow](experiments/EXPERIMENT_WORKFLOW.md)
- [MAF Research](experiments/MAF.md)
- [Representation Analysis](experiments/REPRESENTATION_ANALYSIS.md)
- [Validation](experiments/VALIDATION.md)
- [Labs](labs/README.md)

### Data and Evidence

- [Data and Provenance](data/DATA_AND_PROVENANCE.md)
- [Reproducibility](data/REPRODUCIBILITY.md)

### Development

- [Development](development/DEVELOPMENT.md)
- [Contributing](development/CONTRIBUTING.md)
- [Testing](development/TESTING.md)
- [Documentation](development/DOCUMENTATION.md)
- [Best Practices](development/BEST_PRACTICES.md)

### Operations and Security

- [Operations](operations/OPERATIONS.md)
- [Security](security/SECURITY.md)

### AI Collaboration

- [AI Agent Documentation](ai/README.md)
- [AI Engineering](ai/AI_ENGINEERING.md)
- [AI Debugging](ai/AI_DEBUGGING.md)
- [AI Testing](ai/AI_TESTING.md)
- [Experimental Promotion Policy](ai/EXPERIMENT_PROMOTION.md)

## Evidence and Status Language

OpenMind uses four important status classes:

- `canonical` — implemented behavior supported by source and appropriate tests.
- `validated_research` — reproducible measured evidence that has completed its research validation requirements.
- `lab_candidate` — active experimental work that has not completed promotion.
- `historical` — superseded research retained for provenance or methodology.

An experimental script, benchmark result, roadmap item, or AI interpretation is not automatically a project capability.

## Documentation Principle

Important OpenMind concepts should eventually provide three levels of explanation:

1. a one-sentence description;
2. a practical human-readable example;
3. a precise technical description.

Commands should be reproducible, claims should identify their evidence level, and limitations should be stated explicitly.

## Phase 6B MAF Engineering

- [MAF Research](experiments/MAF.md)
- [Phase 6B MAF Walkthrough](getting-started/MAF_PHASE6B_WALKTHROUGH.md)
- [Authority and Terminology](architecture/AUTHORITY_AND_TERMINOLOGY.md)
- [Development Best Practices](development/BEST_PRACTICES.md)

These documents distinguish frozen implementation, validated behavior, benchmark targets, and future work.

<!-- OPENMIND:Q2-HUMAN-SUMMARY:START -->
## Q2 V1.4 Result

Q2 V1.4 query-to-PK selection validation is complete: **PASS — 74/74**.

For a plain-language explanation of what was proven, what remains unproven, and why the next gate is 6D-Q3, see [`research/Q2_V1_4_SUMMARY.md`](research/Q2_V1_4_SUMMARY.md).

Phase 6E remains not entered.
<!-- OPENMIND:Q2-HUMAN-SUMMARY:END -->
