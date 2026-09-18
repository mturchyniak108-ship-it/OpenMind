# OpenMind AI Instructions — ML Fuzzy Logic Weighted Graph

## Role

You are working on an experimental reasoning layer for OpenMind.

The canonical knowledge authority is the Truth Graph.

## Absolute Rules

1. Never modify canonical truth because a model predicts something.
2. Never treat vector similarity as proof.
3. Never treat fuzzy membership as proof.
4. Never treat ML confidence as proof.
5. Never treat predictive success as truth confidence without explicit validation.
6. Preserve provenance through every transformation.
7. Preserve contradiction information.
8. Preserve TruthNode identity across languages.
9. Keep learned weights versioned.
10. Keep experimental representations reversible where practical.

## Reasoning Procedure

For a query:

1. Resolve candidate semantic locations.
2. Retrieve candidate TruthNodes.
3. Apply vector similarity.
4. Apply fuzzy relationship membership.
5. Apply learned weighting where available.
6. Construct candidate paths.
7. Penalize contradiction, weak evidence, weak provenance, excessive cost, and unnecessary cycles.
8. Rank candidate paths.
9. Validate the selected candidate against canonical Truth Graph state.
10. Inspect provenance.
11. Produce the answer only after validation.

## Weighting Principle

A useful conceptual score is:

candidate_score =
semantic_similarity
+ relationship_strength
+ evidence_strength
+ provenance_strength
+ predictive_weight
- contradiction_penalty
- path_cost

This is an experimental model, not a canonical truth equation.

The exact weighting must be learned or benchmarked rather than assumed.

## Experimental Fractal Integration

If Milestone 11 fractal representations are available, they may be used as another candidate-ranking signal.

The fractal must not replace:

- TruthNode identity
- TruthEdge identity
- provenance
- contradiction state
- canonical graph validation

## Experimental Waveform Integration

Knowledge Waveforms may provide derived signals for:

- relationship strength
- relationship class
- direction
- contradiction
- path cost
- provenance

Again, these are candidate signals only.

## Scientific Requirement

When proposing a new weighting mechanism, state:

- hypothesis
- expected mechanism
- baseline
- measurable metric
- falsification condition

Prefer a failed reproducible experiment over an unsupported claim.

## Output Discipline

When reporting a conclusion, distinguish:

CANONICAL FACT
EXPERIMENTAL SIGNAL
MODEL PREDICTION
FUZZY INFERENCE
UNRESOLVED HYPOTHESIS

Never merge these categories.
