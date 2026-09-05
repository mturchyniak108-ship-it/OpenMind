# OpenMind Experimental Fractal Memory Roadmap

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

## Milestone 11 — Experimental Fractal Memory

### Phase 1 — Formal Model

- [ ] Define canonical fractal-memory object
- [ ] Define start_node/end_node representation
- [ ] Define deterministic path representation
- [ ] Define relationship-tag encoding
- [ ] Define double-helix representation
- [ ] Define convergence-point representation
- [ ] Define fractal versioning
- [ ] Define reproducibility requirements

### Phase 2 — Scientific Method

- [ ] Define explicit hypotheses
- [ ] Define measurable predictions
- [ ] Define controlled experiments
- [ ] Define baseline datasets
- [ ] Define noisy/random control datasets
- [ ] Define known-answer test set
- [ ] Define unknown-answer test set
- [ ] Define replication protocol
- [ ] Define statistical evaluation
- [ ] Define acceptance/rejection criteria

### Phase 3 — Fractal Encoder

- [ ] Encode TruthNodes
- [ ] Encode TruthEdges
- [ ] Encode relationship tags
- [ ] Encode direction
- [ ] Encode confidence
- [ ] Encode evidence
- [ ] Encode provenance
- [ ] Encode contradiction
- [ ] Encode semantic relevance
- [ ] Encode path cost
- [ ] Produce deterministic fractal state

### Phase 4 — Double Helix

- [ ] Implement knowledge/evidence strand
- [ ] Implement prediction/retrieval strand
- [ ] Connect strands through shared relationships
- [ ] Encode start_node
- [ ] Encode end_node
- [ ] Test deterministic helix generation
- [ ] Test path reconstruction

### Phase 5 — Center Convergence

- [ ] Define candidate answer center
- [ ] Define relationship attraction
- [ ] Define contradiction influence
- [ ] Define path-cost influence
- [ ] Define predictive-weight influence
- [ ] Measure convergence stability
- [ ] Compare center location with known correct TruthNode
- [ ] Measure convergence accuracy

### Phase 6 — Predictive Weighting

- [ ] Record predictions
- [ ] Record actual outcomes
- [ ] Calculate prediction success
- [ ] Update predictive weights
- [ ] Penalize failed predictions
- [ ] Measure calibration
- [ ] Test against random weighting
- [ ] Test against fixed weighting
- [ ] Test replication stability

### Phase 7 — Color

- [ ] Define deterministic color encoding
- [ ] Encode relationship class
- [ ] Encode evidence strength
- [ ] Encode semantic relevance
- [ ] Encode confidence
- [ ] Encode predictive weight
- [ ] Encode contradiction
- [ ] Benchmark color-enhanced retrieval

### Phase 8 — Sound

- [ ] Define deterministic audio encoding
- [ ] Synchronize sound with graph state
- [ ] Encode relationship strength
- [ ] Encode relationship class
- [ ] Encode direction
- [ ] Encode path cost
- [ ] Encode support/contradiction
- [ ] Generate lossless audio representation
- [ ] Benchmark sound-enhanced retrieval

### Phase 9 — Fractal Video

- [ ] Generate deterministic frames
- [ ] Generate real-time updates
- [ ] Synchronize geometry/color/sound
- [ ] Record graph version per frame
- [ ] Preserve reproducibility metadata
- [ ] Test incremental updates
- [ ] Measure rendering latency
- [ ] Measure memory usage

### Phase 10 — Fractal Memory Probe

- [ ] Detect query-pattern similarity
- [ ] Retrieve associated fractal regions
- [ ] Retrieve associated TruthNodes
- [ ] Retrieve historical successful paths
- [ ] Rank candidate patterns
- [ ] Validate candidates against Truth Graph
- [ ] Fall back to normal graph traversal
- [ ] Measure traversal reduction
- [ ] Measure retrieval improvement

### Phase 11 — Benchmark

Compare:

- [ ] Traditional LLM retrieval
- [ ] Traditional vector retrieval
- [ ] Truth Graph
- [ ] Truth Graph + Knowledge Waveform
- [ ] Truth Graph + Fractal Memory
- [ ] Truth Graph + Fractal Memory + Color
- [ ] Truth Graph + Fractal Memory + Sound
- [ ] Truth Graph + Fractal Memory + Color + Sound

Measure:

- [ ] answer accuracy
- [ ] retrieval recall
- [ ] path-selection accuracy
- [ ] convergence accuracy
- [ ] contradiction detection
- [ ] provenance preservation
- [ ] latency
- [ ] RAM
- [ ] storage
- [ ] update latency
- [ ] rendering performance
- [ ] predictive calibration
- [ ] replication stability

### Phase 12 — RUNE2 Evaluation

- [ ] Identify RUNE2 integration boundary
- [ ] Build isolated prototype
- [ ] Benchmark RUNE2 against baseline implementation
- [ ] Measure performance
- [ ] Measure reproducibility
- [ ] Measure memory requirements
- [ ] Measure retrieval contribution
- [ ] Reject RUNE2 if no measurable benefit

### Scientific Gate

The fractal system remains experimental unless:

1. The hypothesis is explicitly defined.
2. Predictions are made before testing.
3. Results are measured against controls.
4. Results are reproducible.
5. Independent/replicated tests support the result.
6. Improvement is statistically meaningful.
7. The improvement survives comparison against existing OpenMind retrieval mechanisms.

Until those conditions are met:

Truth Graph = canonical knowledge.

Fractal = experimental derived representation.

Color = experimental representation.

Sound = experimental representation.

Video = experimental representation.

Predictive weight = retrieval-performance statistic, not truth.

RUNE2 = experimental implementation candidate.
