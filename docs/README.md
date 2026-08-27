# OpenMind Documentation

OpenMind is a local-first AI systems project combining native inference, evidence-backed knowledge structures, reproducible model research, and experimental representation engineering.

These documents are written for people first while remaining structured enough for AI collaborators to navigate reliably.

## Start Here

- [Getting Started](getting-started/README.md)
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
