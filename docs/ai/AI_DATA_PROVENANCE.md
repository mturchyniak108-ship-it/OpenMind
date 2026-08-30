# OpenMind AI Data Provenance Policy

## Purpose

OpenMind must distinguish authoritative information from copied, scraped, derived, mirrored, cloned, synthetic, and unknown information.

The Canonical Truth Graph is the canonical knowledge layer. AI-generated or duplicated material must never silently become independent evidence.

## Source classes

- `CANONICAL` — OpenMind canonical truth.
- `PRIMARY` — original or authoritative external source.
- `DERIVATIVE` — legitimately transformed source with traceable ancestry.
- `MIRROR` — copy with identifiable origin.
- `SCRAPE` — extracted material with identifiable origin.
- `CLONE` — replicated or copied material.
- `SYNTHETIC` — AI-generated material.
- `UNKNOWN` — provenance cannot currently be established.

## Independence rule

Multiple copies of the same source do not constitute multiple independent confirmations.

The provenance graph must preserve source lineage. A clone or scrape inherits the evidentiary lineage of its source.

## AI-generated information

AI output may be used as a hypothesis, candidate relationship, heuristic, classification, training signal, or proposed canonicalization.

AI output must not automatically become canonical truth.

Where available, retain model identity, model version, generation timestamp, prompt hash, source hashes, parent provenance, synthetic status, and confidence.

## Required provenance fields

```text
source_uri
source_type
source_hash
retrieval_timestamp
parent_source
derivation_chain
content_hash
model_generated
confidence
```

## Truth protection

Canonical Truth Graph state is immutable by default.

New information creates an evidence or relationship proposal. Promotion to canonical truth requires an explicit validation path.

## Failure preservation

Rejected, contradictory, pruned, and terminated paths remain represented as provenance-bearing information where useful.
