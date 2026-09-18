# OpenMind — ML Fuzzy Logic Weighted Graph

## Status

**EXPERIMENTAL / RESEARCH ONLY — IMPLEMENTED PROTOTYPE**

The current prototype provides:

- deterministic weighted node vectors
- fuzzy relationship membership
- experimental predictive path scoring
- canonical-path reuse
- bounded experimental scores
- explicit isolation from canonical Truth Graph state

The implementation is not authoritative and must not modify canonical
truth, provenance, or canonical path scores.

This subsystem must not become authoritative over the OpenMind Truth Graph.

## Purpose

Investigate whether fuzzy logic combined with machine-learned weighted vectors can improve:

- semantic candidate retrieval
- relationship ranking
- path selection
- contradiction handling
- evidence weighting
- provenance-aware reasoning
- multilingual retrieval
- reduction of unnecessary graph traversal

## Canonical Architecture

Truth Graph
  |
  +-- TruthNode
  +-- TruthEdge
  +-- Relationship Tags
  +-- Provenance
  +-- Truth Confidence
  +-- Contradiction State
        |
        v
Weighted Vector Layer
        |
        v
Fuzzy Membership Layer
        |
        v
ML Weighting / Calibration
        |
        v
Ranked Candidate Paths
        |
        v
Truth Graph Validation
        |
        v
Answer / Hypothesis

The ML/fuzzy layer produces candidates and hypotheses.
It does not create truth merely because a score is high.

## Current Prototype

The implemented prototype derives experimental signals from canonical graph
state.

`FuzzyVectorGraph` currently derives:

- node vectors from TruthNode confidence and outgoing relationships
- relationship membership from edge weight and endpoint confidence
- bounded predictive relationship weights

`PredictivePathScorer` currently evaluates canonical graph paths using:

- mean relationship weight
- mean fuzzy relationship membership
- path cost penalty
- deterministic tie-breaking

These calculations are experimental signals only.

## Fuzzy Model

Candidate membership may combine:

- semantic similarity
- relationship strength
- evidence strength
- provenance strength
- truth confidence
- contradiction penalty
- path cost
- historical predictive performance

All scores must remain inspectable.

## Weighted Vectors

Every vector must retain a deterministic mapping to its canonical object.

Required metadata:

- TruthNode identifier
- TruthEdge identifier where applicable
- embedding model/version
- vector dimensions
- normalization method
- generation timestamp
- graph version
- provenance reference

## ML Weighting

ML may learn weighting coefficients from benchmark outcomes.

Learned weights must be:

- versioned
- reproducible
- auditable
- benchmarked
- separable from canonical truth
- replaceable without modifying TruthNode identity

Predictive performance must not automatically become truth confidence.

## Scientific Method

Each experiment must define:

1. Hypothesis
2. Baseline
3. Variables
4. Dataset
5. Metrics
6. Experimental procedure
7. Results
8. Reproduction procedure
9. Conclusion
10. Limitations

No feature graduates from experimental status without measurable and reproducible evidence.

## Current Research Gaps

The prototype does **not** yet establish:

- learned ML weighting
- model training or calibration
- contradiction-aware scoring
- provenance-aware predictive weighting
- vector persistence
- embedding-model integration
- multilingual evaluation
- benchmark evidence demonstrating retrieval improvement

These remain research tasks rather than implemented capabilities.

## Required Comparisons

Compare:

- graph traversal
- vector retrieval
- fuzzy graph without ML
- ML-weighted fuzzy graph
- OpenMind Truth Graph + weighted fuzzy graph
- future multimodal/fractal-assisted retrieval

## Safety / Integrity Rule

A high fuzzy score, vector similarity, ML prediction, fractal convergence, waveform feature, or visual pattern is a candidate signal.

It is never proof by itself.

Canonical truth remains:

Truth Graph + Provenance + Validation
