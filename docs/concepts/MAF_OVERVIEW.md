# What Is MAF — Model Address Fabric?

MAF — Model Address Fabric is a persistent model-object
representation and addressing architecture.

Its purpose is to make portions of a model representable as
stable, addressable objects whose identity, location,
provenance and reconstruction relationships can be reasoned
about explicitly.

## Core concerns

MAF research focuses on:

- stable object identity;
- deterministic addressing;
- tensor ↔ object relationships;
- persistent payload provenance;
- reconstruction;
- catalog and segment organization;
- selective lookup;
- runtime residency;
- query-scoped selection;
- fail-closed validation.

## What MAF is not

MAF is not a claim that a new model architecture has replaced
conventional inference.

MAF is also not, by itself:

- a neural-network architecture;
- a model format superiority claim;
- a no-copy runtime claim;
- a native-performance claim;
- a database implementation;
- a replacement for every existing model file format.

## Current evidence boundary

Phase 6 established a bounded model-object and provisioning
research baseline, including a frozen Class-A inference
parity result and a frozen Phase-6F provisioning
characterization.

Those results remain scoped to their preregistered models,
runtime, workload and correctness boundaries.

See:

- `docs/research/PHASE_6_SUMMARY.md`
- `docs/provenance/OPENMIND_TO_MAF_LINEAGE.md`
