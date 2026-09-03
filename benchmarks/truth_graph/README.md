# OpenMind Truth Graph Baseline

This directory contains deterministic benchmark results for the canonical
OpenMind Truth Graph.

The canonical Truth Graph is the control condition.

Experimental retrieval systems must be compared against this baseline.

## Control

Truth Graph:

- deterministic node identities
- deterministic edge relationships
- deterministic path enumeration
- deterministic path scoring
- deterministic candidate selection

## Experimental systems

Future comparisons may include:

- vector retrieval
- compiled path retrieval
- fuzzy graph
- ML-weighted fuzzy graph
- Knowledge Waveform
- fractal memory
- multimodal fractal/video retrieval
- RUNE2 experiments

No experimental system may silently replace canonical Truth Graph validation.

## Required measurements

Each benchmark should record:

- start_node
- end_node
- selected path
- path length
- relationship weights
- truth confidence
- path score
- execution latency
- candidate count

Future systems must additionally report:

- retrieval accuracy
- candidate recall
- ranking accuracy
- contradiction handling
- provenance preservation
- memory usage
