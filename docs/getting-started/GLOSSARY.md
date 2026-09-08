# OpenMind Glossary

This glossary gives a plain-language meaning first, followed by the more technical OpenMind usage where useful.

## Canonical

**Plain language:** A part of OpenMind that the project currently treats as implemented behavior.

**Technical meaning:** Source-backed behavior supported by appropriate tests and repository evidence.

Canonical does not mean perfect or permanently frozen.

## Validated Research

**Plain language:** An experimental result that has passed its stated evidence and validation requirements.

**Technical meaning:** Reproducible research with immutable inputs, controls or baselines, characterized outputs, hashes, limitations, and explicit promotion.

Validated research is still not automatically a production feature.

## Lab Candidate

**Plain language:** Work currently being investigated.

It may be promising, incomplete, wrong, or later superseded.

## Historical

**Plain language:** Older work kept so the research path is not lost.

Historical experiments may remain useful for provenance, comparison, or methodology even when newer versions replace them.

## Provenance

**Plain language:** The record of where information or an artifact came from.

**Technical meaning:** Source identity, version, command, environment, hashes, relationships, and other evidence needed to trace an artifact.

## Evidence

Information used to support or verify a project claim.

OpenMind distinguishes measured evidence from interpretation.

## Truth Graph

**Plain language:** A structured network for representing things OpenMind knows and how those things relate.

**Technical meaning:** Canonical nodes and weighted relationships with provenance-aware traversal and evidence bindings.

## Truth Path

A route through related entries in the Truth Graph.

A path can represent how one piece of information connects to another and can carry relationship and provenance information.

## Representation

**Plain language:** The internal numerical form a model uses while processing information.

In current OpenMind research, representations often refer to hidden-state vectors captured at transformer layers.

## Activation

A numerical value or vector produced inside a neural network during computation.

OpenMind activation experiments capture selected internal model representations for analysis.

## Embedding Dimension

The number of numerical components in a representation vector.

For example, a 1536-dimensional activation contains 1536 scalar values.

## Recurrence

**Plain language:** Similar internal structure appearing again at another point in model processing.

In OpenMind research, recurrence is measured rather than assumed. High similarity alone does not prove identical information or identical computation.

## Cosine Similarity

A measurement of how closely two vectors point in the same direction.

Values near 1 indicate similar direction, but interpretation depends on the experiment and its controls.

## Holdout

Data intentionally kept out of discovery or fitting so a candidate can be tested on information it did not use during development.

## Baseline

A reference measurement used for comparison.

A baseline may represent current behavior, exhaustive search, a control population, or another appropriate reference.

## Control

An alternative condition designed to test whether an observed result could arise for a simpler or unrelated reason.

Examples include shuffled labels, cross-token comparisons, and randomized mappings.

## MAF

**Plain language:** OpenMind research into compact, indexed, or structured representations of model-derived information.

MAF work includes retrieval, indexing, reconstruction, streaming, scaling, and related representation experiments.

MAF engineering results do not by themselves prove that a scientific recurrence hypothesis is correct.

## Lodgepole

**Plain language:** An experimental tree organization inspired by a lodgepole pine: shared structure forms the trunk and branches while increasingly specific information appears toward terminal needles.

**Technical meaning:** Current experiments use deterministic hierarchical partitioning, centroids, routing, and residual representations to investigate retrieval and storage behavior.

## Root

The top node of a tree structure.

In Lodgepole experiments, the root represents the broadest shared group.

## Branch

An intermediate subdivision of the tree containing more specific related information.

## Leaf / Needle

A terminal part of a Lodgepole tree.

Current experiments use terminal nodes to hold the most localized groups of representations.

The term `needle` is a project metaphor and should not be confused with a standard machine-learning term.

## Centroid

The arithmetic center of a group of vectors.

It provides a representative vector for a tree node or cluster.

## Residual

**Plain language:** The difference left after subtracting a shared representation.

For example, a child centroid minus its parent centroid is a parent-child residual.

Residual magnitude is currently being investigated as a possible basis for hierarchical storage.

## Reconstruction

Building an approximation or exact version of an original representation from stored components.

Any lossy reconstruction must be evaluated for numerical error and, where relevant, behavioral fidelity.

## Fractal

OpenMind uses this term for experimental repeated or hierarchical structure.

It should not be interpreted as proof that transformer representations are mathematical fractals unless an experiment specifically establishes that property.

## Deterministic

Given the same defined inputs and environment, an operation produces the same result.

Where execution is not deterministic, OpenMind should record sources of variation.

## Manifest

A structured metadata file describing an artifact or experiment, including configuration, hashes, provenance, status, and validation information.

## Promotion

The explicit process of moving work from a lower evidence status toward validated research or canonical project behavior.

Promotion is never implied merely by the existence of a successful-looking result.

## MAF Generation

An immutable canonical descriptor plus its generation identity and physical segment evidence. A generation is not defined by its current filesystem location.

## Active Generation

The generation selected by the canonical active-generation authority record for a model.

## Stable Logical PK

A canonical logical identifier such as `model_pk`, `generation_pk`, or `object_pk` whose identity is independent of mutable physical placement.

## Resident PK Directory

A derived process-local immutable lookup snapshot built from current active-generation authority and validated physical evidence. It is not authoritative truth.

Resident PK Directory V1 supports model-scoped canonical `object_pk` lookup as its minimum key class.

## Stale Snapshot

A resident snapshot whose generation binding no longer matches the generation expected by the current runtime after activation, rollback, or another authority transition.

## Path Independence

The property that byte-identical valid physical evidence may move to another runtime path without changing logical PK identity or immutable descriptor mappings.

<!-- MAF_GLOSSARY_POST_PHASE6_V1 -->
## MAF — Model Address Fabric

**Status:** Canonical current term.

MAF means **Model Address Fabric**.

It is the persistent model-object representation and
addressing architecture focused on stable identities,
deterministic addressing, tensor ↔ object relationships,
payload provenance, reconstruction, scalable lookup and
selection, and fail-closed validation.

The acronym existed in earlier OpenMind research. This
post-Phase-6 definition establishes the expanded
current-facing name without rewriting historical
evidence.

## Terminology status

**Canonical** — preferred current term.

**Provisional** — working term that may change after
design or validation.

**Historical** — preserved term from earlier research or
evidence.

**Compatibility Identifier** — historical identifier that
remains valid because software, schemas or data may
depend on it.

See `../terminology/COINED_TERMS.md`.
