# MAF — Model Address Fabric

**MAF — Model Address Fabric** is a persistent model-object
representation and addressing architecture.

It is intended for systems that need model data to have more
explicit identity, provenance, addressing and reconstruction
relationships than a conventional opaque model file normally
exposes.

This page is the fastest way to decide whether MAF is relevant
to what you are building, researching or evaluating.

---

## In one minute

MAF treats model-related data as **addressable objects** rather
than only as bytes inside one large model file.

The architecture focuses on:

- stable model-object identity;
- deterministic addressing;
- tensor ↔ object relationships;
- persistent payload provenance;
- object and tensor reconstruction;
- catalogs and segment-based storage;
- selective lookup and working-set selection;
- runtime residency and object location;
- compatibility across representation boundaries;
- fail-closed validation when identity or authority cannot be
  proven.

A simplified mental model is:

**model data → identified objects → persistent addresses →
provenance → selective retrieval → reconstruction**

MAF does **not** require pretending that conventional model
formats never existed. Existing model formats can remain source,
compatibility or reconstruction boundaries.

---

## What problem is MAF trying to solve?

Most model runtimes begin with a large serialized model artifact
and load whatever structures the runtime requires from that
artifact.

MAF explores a different question:

> What if model components had stable identities and could be
> addressed, located, selected, validated and reconstructed as
> persistent objects?

That makes several capabilities possible to investigate
explicitly rather than treating them as incidental properties of
a model file.

These include:

- identifying the same logical model object independently of its
  storage location;
- tracing where payload data came from;
- validating that reconstructed data belongs to the expected
  object;
- organizing model data into persistent segments;
- selecting bounded subsets of model objects;
- reasoning about which model objects are resident or absent;
- building deterministic lookup structures around model data;
- testing alternative provisioning and storage architectures.

---

## What MAF can do today

The current repository contains validated research and
engineering work around:

**Persistent object identity**

Model-related objects can be represented with stable identity and
explicit provenance relationships.

**Tensor ↔ object relationships**

The research includes exact tensor/object representation and
reconstruction work rather than treating an object name as merely
descriptive metadata.

**Persistent segment storage**

MAF research includes segment-based storage, catalogs and readers
for locating persistent model objects.

**PK-based lookup and selection**

Existing work includes PK-oriented catalogs, resident
directories, query-scoped selection and related validation.

**Selective model access research**

Phase 6 investigated whether bounded model working sets and
persistent MAF-backed provisioning could be used across increasingly
complete model-access boundaries.

**Inference correctness validation**

A frozen Phase 6E-D result demonstrated numerical logit parity
between the tested MAF-backed model path and its conventional
reference under one pinned model, runtime, prompt and validation
boundary.

**Performance characterization**

Phase 6F measured the current persistent MAF provisioning path
against the conventional reference path.

That baseline is important because the current implementation was
**not faster**: median model-ready time was approximately **3.98×
the control** under that frozen workload.

This means the repository currently contains a validated
architectural/research foundation, **not a claim that MAF already
provides a faster production inference runtime**.

See [Phase 6 Research Summary](research/PHASE_6_SUMMARY.md).

---

## Is MAF a good fit for what I am doing?

| Your goal | Current fit |
| --- | --- |
| Stable identity for model components | **Strong architectural fit** |
| Deterministic model-object addressing | **Strong architectural fit** |
| Payload provenance and reconstruction | **Strong architectural fit** |
| Persistent model-object storage research | **Strong research fit** |
| Selective / bounded model working sets | **Active research foundation exists** |
| Model catalog and object lookup | **Existing validated research foundation** |
| Compatibility-aware model transformation | **Relevant** |
| Research into model storage/provisioning architectures | **Relevant** |
| Drop-in replacement for a normal inference server | **Not the current goal** |
| Guaranteed faster inference today | **No** |
| Production-ready universal model database | **Not yet** |
| Proven native no-copy runtime | **Not yet** |
| Proven performance across arbitrary models/hardware | **No** |
| Conventional model serving with no need for object identity | **Probably unnecessary** |

---

## When you probably want MAF

MAF is worth investigating when your system needs questions like
these to have explicit answers:

- What model object is this?
- Is this the same logical object as the one seen earlier?
- Where is the object's payload stored?
- What source produced this payload?
- What version or authority governs it?
- Which objects are needed for this operation?
- Which required objects are already resident?
- Can this object be reconstructed deterministically?
- Can the reconstruction be validated?
- Can storage placement change without changing logical identity?
- Can model data be selected or provisioned without treating the
  entire source artifact as one indivisible unit?

If those questions matter to your architecture, MAF is likely
relevant.

---

## When MAF may not be necessary

You may not need MAF if your only requirement is:

- load a conventional model;
- run inference;
- keep the model as one normal runtime artifact;
- and you do not need persistent object identity, provenance,
  selective addressing or reconstruction.

MAF adds architectural structure deliberately. That structure is
useful only when the problems it addresses matter to the system.

---

## What MAF is not

MAF is not currently presented as:

- a new neural-network architecture;
- a new foundation model;
- proof that model objects improve model intelligence;
- a universal replacement for GGUF or other model formats;
- a production-ready distributed database;
- a proven no-copy inference system;
- a proven performance optimization;
- a claim that every model should be decomposed in the same way.

Research claims must remain bounded by the protocols and evidence
that established them.

---

## Core concepts

### MAF object

An addressable model-related object governed by identity,
provenance and representation rules.

[Read the MAF Object Model](reference/MAF_OBJECT_MODEL.md).

### PK

An established identifier/addressing concept used by existing MAF
catalog, selection and residency work.

Earlier protocols remain authoritative for their exact semantics.

### Segment

A persistent storage grouping that can contain serialized MAF
object data.

Physical segment placement does not automatically define logical
object identity.

### Provenance

Evidence describing where an object or payload came from and what
authority governs its interpretation.

### Reconstruction

Recovering the model-facing representation required from governed
MAF object and payload data.

### Authority

The protocol, schema, identity or frozen evidence that determines
how an artifact is interpreted and validated.

---

## For humans: fastest reading path

If you have only a few minutes:

1. Read this page.
2. Read the [Glossary](getting-started/GLOSSARY.md).
3. Read the [MAF Object Model](reference/MAF_OBJECT_MODEL.md).
4. Read the [Phase 6 Research Summary](research/PHASE_6_SUMMARY.md).

If you are deciding whether to build on MAF:

1. Read [What Is MAF?](concepts/MAF_OVERVIEW.md).
2. Read [Authority and Terminology](architecture/AUTHORITY_AND_TERMINOLOGY.md).
3. Read [Schema Registry](reference/SCHEMA_REGISTRY.md).
4. Read [OpenMind Compatibility](compatibility/OPENMIND_COMPATIBILITY.md).
5. Check [Current Work](research/CURRENT_WORK.md).

If you want to operate the repository:

- [Getting Started](getting-started/README.md)
- [Installation](getting-started/INSTALLATION.md)
- [Command Reference](getting-started/COMMAND_REFERENCE.md)
- [How-To Guides](howto/README.md)

---

## For AI agents

An agent entering this repository should not infer authority from
a filename, a recent implementation or a successful compile alone.

Recommended orientation order:

1. Read this page.
2. Read
   [Authority and Terminology](architecture/AUTHORITY_AND_TERMINOLOGY.md).
3. Read the
   [OpenMind → MAF Lineage](provenance/OPENMIND_TO_MAF_LINEAGE.md).
4. Read
   [OpenMind Compatibility](compatibility/OPENMIND_COMPATIBILITY.md).
5. Read [Current Work](research/CURRENT_WORK.md).
6. Locate the protocol or frozen authority governing the specific
   artifact or operation.
7. Distinguish historical evidence from active defects.
8. Do not broaden mutation, execution or publication authority
   beyond the explicitly authorized operation.

For terminology created by this project, use the
[Coined Terms Registry](terminology/COINED_TERMS.md).

---

## Evidence and maturity

MAF currently spans several levels of maturity.

**Implemented**

Code or data structures exist.

**Validated**

A defined test, protocol or experiment produced qualifying
evidence.

**Architectural**

A design relationship or system boundary has been established but
does not itself prove production performance.

**Research**

A hypothesis or implementation has bounded experimental evidence
and should not be generalized beyond that evidence.

**Prospective**

Planned or proposed work that has not yet been demonstrated.

These categories should not be treated as interchangeable.

---

## Historical lineage

MAF emerged from model-object research developed in the OpenMind
repository.

The transition to **MAF — Model Address Fabric** preserves that
provenance rather than rewriting it.

Historical OpenMind paths, Git history, frozen research artifacts
and compatibility-bearing `openmind.*` schema identifiers remain
part of the evidence chain.

Read
[OpenMind → MAF Lineage](provenance/OPENMIND_TO_MAF_LINEAGE.md)
before changing historical identifiers.

---

## Current project boundary

Whole Phase 6 is formally closed.

The repository now has a frozen MAF documentation foundation and
a validated research baseline.

Current documentation does not imply that future storage,
database, native-runtime, hardware-acceleration or model-support
work has already been completed.

Those capabilities require their own implementation and validation
gates.

---

## Documentation map

**Understand MAF**

- [MAF Overview](concepts/MAF_OVERVIEW.md)
- [Glossary](getting-started/GLOSSARY.md)
- [Coined Terms](terminology/COINED_TERMS.md)

**Understand the architecture**

- [Authority and Terminology](architecture/AUTHORITY_AND_TERMINOLOGY.md)
- [MAF Object Model](reference/MAF_OBJECT_MODEL.md)
- [Schema Registry](reference/SCHEMA_REGISTRY.md)

**Use the repository**

- [Getting Started](getting-started/README.md)
- [Command Reference](getting-started/COMMAND_REFERENCE.md)
- [How-To Guides](howto/README.md)

**Understand the evidence**

- [Phase 6 Research Summary](research/PHASE_6_SUMMARY.md)
- [Current Work](research/CURRENT_WORK.md)

**Understand provenance and compatibility**

- [OpenMind → MAF Lineage](provenance/OPENMIND_TO_MAF_LINEAGE.md)
- [OpenMind Compatibility](compatibility/OPENMIND_COMPATIBILITY.md)

---

## Short answer

MAF is most relevant when you need a model to be treated as a
collection of **persistent, identifiable, addressable and
provenance-aware objects**, rather than only as one opaque
serialized artifact.

If that distinction matters to your system, continue into the
architecture and object-model documentation.

If it does not, a conventional model-loading architecture may be
simpler and more appropriate.
