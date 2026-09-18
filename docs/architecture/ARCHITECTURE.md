# MAF Architecture

## Design Principles

1. Local-first execution.
2. Separate inference from research experiments.
3. Keep hardware acceleration behind stable interfaces.
4. Make experiments reproducible.
5. Preserve provenance.
6. Do not silently promote experiments into production.
7. Keep components small and testable.

## System Flow

```text
                MAF successor + preserved OpenMind layers
                            |
          +-----------------+-----------------+
          |                 |                 |
          v                 v                 v
      Inference          Analysis          Research
          |                 |                 |
          v                 v                 v
      llama.cpp            MAF           Experiments
          |                 |                 |
          v                 v                 v
       Vulkan          Activations       Holdouts
          |                 |                 |
          +-----------------+-----------------+
                            |
                            v
                    Validation / DAG
                            |
                            v
                   Provenance / Results
```

## Architecture Rule

Research produces evidence. Production consumes validated components.

## MAF Phase 6B Architecture

Phase 6B separates logical identity, authority, immutable physical evidence, and derived runtime lookup.

```text
stable logical PK
    -> active-generation authority
    -> immutable generation descriptor
    -> immutable segment / offset / length evidence
    -> derived Resident PK Directory snapshot
```

The Resident PK Directory does not become a new authority layer. It is rebuildable process-local state derived from the current active generation.

Activation changes which immutable generation is authoritative. Rollback changes authority back to another retained generation after validating its current physical evidence.

A resident snapshot is generation-bound. When activation or rollback changes active authority, the previous resident snapshot is stale and must not be served as current.

Phase 6B.10 will address physical Segment Reader validation. Phase 6C will address broader object runtime and residency. Neither responsibility is assigned to Resident PK Directory V1.
