# MAF Coined Terms Registry

This registry tracks terminology introduced or specialized
by the MAF research and engineering lineage.

It does not replace the normative definitions in
`docs/architecture/AUTHORITY_AND_TERMINOLOGY.md`.

## Status classes

**Canonical**

The preferred term for current MAF documentation.

**Provisional**

A working term that may change after validation or design
review.

**Historical**

A term preserved because it appears in earlier research,
evidence, schemas, paths, or Git history.

**Compatibility Identifier**

A historical identifier that remains valid because software,
data, schemas, or integrations may depend on it.

## Registry

| Term | Expanded form / meaning | Status | Notes |
| --- | --- | --- | --- |
| MAF | Model Address Fabric | Canonical | Post-Phase-6 project identity for the model-object representation and addressing architecture. |
| Model Address Fabric | Persistent model-object representation and addressing architecture | Canonical | Focuses on stable identities, deterministic addressing, provenance and reconstruction. |
| MAF object | Addressable model object governed by MAF identity/provenance rules | Canonical | Exact serialized forms remain version-specific. |
| MAF segment | Persistent storage segment used by MAF research/runtime structures | Canonical | Historical segment formats remain governed by their frozen protocols. |
| PK | Existing MAF identifier/address concept | Canonical existing term | Its historical semantics are not redefined by this registry. |
| resident PK directory | Runtime directory used to resolve resident PK locations | Historical + current architectural term | Existing Phase-6 implementation and evidence retain original identity. |
| OpenMind | Original repository/research lineage name | Historical | Preserved in Git history and historical artifacts. |
| `openmind.*` | Existing schema namespace | Compatibility Identifier | Must not be mass-renamed. Versioned migration requires a separate compatibility contract. |
| Gold Standard | Fail-closed engineering/research workflow used by this project | Canonical workflow term | Separates discovery, mutation, execution, evidence freeze and publication. |

## Registration rule

A new coined term should record:

1. the term;
2. its definition;
3. its status;
4. where it was introduced;
5. any aliases or superseded terminology;
6. compatibility implications;
7. the authority document that governs it.

## Historical preservation

Registering a preferred MAF term does not authorize changing
historical artifacts that used an earlier term.
