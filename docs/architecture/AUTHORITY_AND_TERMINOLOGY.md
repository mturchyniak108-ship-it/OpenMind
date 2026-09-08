# OpenMind Authority and Terminology

## Purpose

OpenMind uses more than one kind of authoritative artifact.

This document defines the terms used to distinguish them.

The distinction is important for people, AI collaborators, documentation, experiments, and future tooling.

## Canonical Model Artifact

The **Canonical Model Artifact** is the immutable reference model used for model-derived research.

In current representation and MAF experiments this may be a specific GGUF file identified by its exact artifact name, metadata, and cryptographic hash.

The Canonical Model Artifact is authoritative for questions such as:

- which model was measured;
- which parameters and tensors were used;
- which architecture and dimensions were present;
- what source artifact a derived representation came from;
- whether two experiments used the same model artifact.

It is not the canonical knowledge store of OpenMind.

The preferred generic term is:

`Canonical Model Artifact`

When the artifact is specifically a GGUF file, documentation may say:

`Canonical Model GGUF`

## Canonical Truth Graph

The **Canonical Truth Graph** is OpenMind's authoritative structured knowledge layer.

It contains explicit nodes and relationships and works with evidence, provenance, path resolution, and persistence.

The Canonical Truth Graph is authoritative for questions such as:

- what structured knowledge OpenMind currently represents;
- how two canonical knowledge entries are related;
- what evidence supports a relationship;
- what provenance gaps exist;
- which canonical path is resolved under the implemented graph contract.

The Canonical Truth Graph does not redefine the parameters of the Canonical Model Artifact.

## Derived Representations

Derived representations are structures calculated from a canonical source.

Examples include experimental:

- MAF representations;
- Lodgepole trees;
- fractal representations;
- waveforms;
- fuzzy graphs;
- landscape or heatmap features;
- activation-derived indexes;
- learned routing structures.

Derived representations may improve access, routing, storage, visualization, or computation, but they do not silently become canonical authority.

## Two-Authority Model

OpenMind therefore currently distinguishes two primary forms of authority:

```text
MODEL AUTHORITY
Canonical Model Artifact
        |
        +--> activations
        +--> tensor measurements
        +--> representations
        +--> MAF / Lodgepole research

KNOWLEDGE AUTHORITY
Canonical Truth Graph
        |
        +--> relationships
        +--> evidence bindings
        +--> provenance
        +--> canonical truth paths
```

The two systems may be linked in future architecture, but one must not be described as the other.

## Provenance Rule

Every derived artifact should identify which authority it derives from.

For model-derived research, record the Canonical Model Artifact identity and hash.

For knowledge-derived structures, preserve correspondence to the Canonical Truth Graph and its evidence/provenance state.

If an artifact combines both sources, both lineages should remain traceable.

## Deprecated Ambiguous Term

The unqualified term `Truth Canon` is ambiguous and should not be introduced in new documentation.

Existing historical documents may contain the term and should be interpreted from context until updated.

Prefer:

- `Canonical Model Artifact` or `Canonical Model GGUF` for the reference model;
- `Canonical Truth Graph` for authoritative structured knowledge.

## Research Boundary

Neither a successful experiment nor a derived representation changes canonical authority automatically.

Research promotion follows the validation and promotion rules documented elsewhere in OpenMind.

## MAF Phase 6B Authority Chain

MAF Phase 6B uses a strict authority-versus-derived-state boundary.

Authoritative current-generation selection:

1. the canonical five-field active-generation record;
2. the immutable generation manifest and descriptor identified by that record;
3. the immutable physical segment and object-range evidence validated against the descriptor.

Derived state:

- Resident PK Directory snapshots;
- runtime physical segment paths;
- lookup indexes and cache structures.

Derived state must never redefine `model_pk`, `generation_pk`, `object_pk`, segment identity, object offsets, lengths, or integrity hashes.

Physical relocation may change runtime path metadata while stable logical PK identity and immutable descriptor evidence remain unchanged.

A successful activation or rollback invalidates the prior current-generation resident snapshot. A replacement snapshot must be completely rebuilt and validated before publication.

<!-- MAF_AUTHORITY_POST_PHASE6_V1 -->
## Post-Phase-6 project identity authority

The canonical current-facing expansion of **MAF** is:

**Model Address Fabric**

MAF is the successor project identity for the
model-object representation/addressing direction after
formal closure of Phase 6.

### Lineage rule

OpenMind remains the historical repository/research
lineage identity.

Adoption of the MAF name does not authorize rewriting:

- frozen scientific artifacts;
- historical paths;
- Git history;
- historical commit subjects;
- existing `openmind.*` schema identifiers.

### Compatibility rule

Existing `openmind.*` schemas, Python import paths and
native identifiers remain compatibility-bearing surfaces
until an explicit versioned migration contract is
authorized.

### Authority rule

Current terminology may explain historical evidence but
must not retroactively change the identity under which
that evidence was produced.
