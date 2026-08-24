# OpenMind Architecture

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
                         OpenMind
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
