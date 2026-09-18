# OpenMind Experimental Fractal Memory

<!-- OPENMIND_MAF_Q4_STATUS_BEGIN -->
## MAF Phase 6D-Q4 status — CLOSED

Phase 6D-Q4 Query Route Cache validation is formally closed on frozen evidence.

- Scientific result: **PASS — 44/44 Q4 checks**.
- Frozen cases: `q001`, `q025`, `q026`, `q033`.
- Frozen runner: `bafed2c9ef6d2cf35d8d5212bbb17497f68a67fff9a67d855ac96243af3ac686`.
- Frozen result: `1be2608271e899d320b4255fccba2e64c1616281110ebb375f803a7f740c43e0` / 9184 bytes.
- Frozen exact-once slot: `af63aa8d3b769ad984b898d805ff45361eb5e079658d47a088514d3ba4145a2d` / 1311 bytes.
- Runner implementation contract: `daa291fcb06c0456e028807308e35ef86486e5176b4fe88d254915718d6943e4`.
- Evidence commit: `b386abde55b1b8f156292eb7500fb739ea8be918`.
- Exact-once history: V1, V1.1, V1.2, and V1.3 are permanently spent and MUST NOT be rerun.
- Durable V1.3 state: `RESERVATION_PREPARED -> RESERVED_DURABLE -> PUBLISHED_DURABLE`; no partial residue.
- Claim scope remains limited to safe generation-bound route-metadata persistence, reuse, and invalidation.
- Not established by Q4: inference execution, answer generation, working-set sufficiency, performance superiority or metrics, output parity, route-expansion optimality, MAF-native compute, or LLM replacement.
- Phase 6E: **READY FOR ENTRY REVIEW — NOT ENTERED**.
- Canonical closure record: `experiments/model_fractal/MAF_QUERY_ROUTE_CACHE_VALIDATION_V1_3_VERDICT.md`.

<!-- OPENMIND_MAF_Q4_STATUS_END -->

## Status

EXPERIMENTAL / NON-CANONICAL

This subsystem investigates whether the complete OpenMind Truth Graph can be represented as a deterministic, evolving fractal structure that can function as an associative or predictive memory.

The fractal representation MUST NOT become the canonical source of truth unless a reproducible scientific hypothesis demonstrates measurable benefit.

## Canonical Authority

Truth Graph = canonical knowledge.

Provenance = required evidence trail.

Fractal memory = derived experimental representation.

Knowledge Waveform = derived experimental representation.

Vector indexes = candidate retrieval mechanisms only.

LLM/RAG retrieval = comparison baseline.

No fractal, video, color, sound, vector, embedding, or predictive score may silently replace canonical structured truth.

## Research Hypothesis

Primary hypothesis:

A deterministic multimodal fractal representation of the Truth Graph may provide useful associative memory by causing relationships relevant to a query to converge toward a central candidate answer.

The candidate point closest to the center represents the strongest current hypothesis, NOT automatically the truth.

The hypothesis is considered supported only when independent experiments demonstrate measurable improvement over appropriate baselines.

## Scientific Method

The subsystem must follow:

1. Observation
2. Hypothesis
3. Prediction
4. Experiment
5. Measurement
6. Statistical evaluation
7. Weight update
8. Replication
9. Conclusion

The system must distinguish:

- observed facts
- hypotheses
- predictions
- tested outcomes
- replicated outcomes
- conclusions

## Start/End Path Model

Every represented path must retain:

- start_node
- end_node
- path_id
- relationship tags
- relationship direction
- relationship weight
- truth confidence
- evidence strength
- provenance strength
- semantic relevance
- contradiction signal
- path cost
- predictive weight

The same Truth Graph state and path metadata must produce the same deterministic representation.

## Fractal Geometry

The fractal is intended to represent relationships between TruthNodes.

Candidate paths may form double-helix structures.

One strand may represent knowledge/evidence.

The second strand may represent prediction/retrieval behavior.

Relationships should converge toward candidate answer points.

The point of greatest validated relational convergence is the current answer hypothesis.

Geometry must be generated from graph data rather than manually selected to produce a desired answer.

## Predictive Weighting

Predictive weight measures how reliably a fractal pattern has historically led to useful validated outcomes.

It is NOT truth confidence.

Potential signals include:

- retrieval success
- path success
- answer relevance
- confidence calibration
- replication success
- provenance quality
- contradiction rate
- recency
- convergence stability

Weighting formulas must be experimentally evaluated rather than assumed.

False positives and failed predictions must reduce predictive confidence.

## Multimodal Representation

The same underlying graph state may be represented through:

### Geometry

- spatial position
- path distance
- convergence
- helix structure
- node density
- relationship topology

### Color

Potential mappings:

- hue = relationship class
- brightness = evidence strength
- saturation = semantic relevance
- opacity = confidence
- temperature = predictive weight
- support/contradiction = configurable opposing visual dimensions

Mappings must remain versioned and deterministic.

### Sound

Potential mappings:

- amplitude = relationship strength
- frequency = relationship class
- phase = relationship direction
- duration = path cost/significance
- positive signal = supporting evidence
- negative signal = contradiction
- stereo position = competing paths

Sound must remain synchronized with the same underlying graph state.

## Real-Time Fractal Video

Investigate continuously generated fractal video representing changes in the Truth Graph.

A frame should be reproducible from:

- Truth Graph version
- path metadata
- encoder version
- visualization configuration
- timestamp/state identifier

The video is an observation/representation layer, not an authoritative database.

## Fractal Memory Probe

During retrieval, OpenMind may occasionally inspect existing fractal patterns before performing expensive traversal.

The probe asks:

- Does this query resemble an existing pattern?
- Which TruthNodes are associated with the pattern?
- Which relationships surround it?
- What paths historically succeeded?
- What evidence and provenance support those paths?
- What contradictions exist?
- What predictive weight has the pattern earned?

A fractal match produces a candidate semantic location.

It does NOT produce proof of truth.

Candidates must be validated against the Truth Graph.

## Answer Convergence

For a query:

query -> candidate patterns -> candidate paths -> convergence point

The system should investigate whether the strongest validated candidate naturally approaches the geometric center.

The center therefore represents:

CURRENT BEST HYPOTHESIS

not:

ABSOLUTE TRUTH

A conclusion becomes stronger only when independent evidence, provenance, prediction, and replication support it.

## Experimental Controls

Experiments must include:

- high-quality validated knowledge
- mixed-quality knowledge
- contradictory knowledge
- randomized/noise relationships
- known-answer queries
- unknown-answer queries

Increasing data volume alone must not be interpreted as improved reasoning.

## Required Benchmarks

Compare:

1. Traditional LLM retrieval
2. Traditional vector retrieval
3. OpenMind Truth Graph
4. Truth Graph + Knowledge Waveform
5. Truth Graph + Fractal Memory
6. Truth Graph + Fractal Memory + Color
7. Truth Graph + Fractal Memory + Sound
8. Truth Graph + Fractal Memory + Color + Sound

Measure:

- retrieval recall
- answer accuracy
- path-selection accuracy
- convergence accuracy
- contradiction detection
- provenance preservation
- latency
- RAM usage
- storage size
- update latency
- real-time rendering performance
- predictive-weight calibration
- replication stability

## Scientific Acceptance Rule

The feature remains EXPERIMENTAL until results show statistically and reproducibly meaningful improvement.

A visually compelling fractal is not evidence of improved reasoning.

A central point is not evidence of truth.

A high predictive weight is not evidence of truth.

Only validated evidence and provenance can establish truth.

## RUNE2

RUNE2 may be evaluated as a candidate implementation/runtime backend if it provides measurable advantages.

It must not be adopted merely because it produces visually interesting or computationally complex fractals.

Any RUNE2 integration must remain replaceable behind an experimental interface.

## Failure Conditions

The experiment must be considered unsuccessful if:

- fractal convergence does not correlate with correct answers
- random/noisy data produces equal or better structure
- predictive weighting reinforces incorrect patterns
- provenance is lost
- contradictions are hidden
- results cannot be reproduced
- the representation increases cost without measurable benefit

## Core Principle

The fractal is a hypothesis engine and associative-memory experiment.

The Truth Graph remains the authority.
