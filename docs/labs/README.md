# MAF Labs

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

<!-- OPENMIND:CURRENT-WORK-LINK:START -->
Current scientific work: [`../research/CURRENT_WORK.md`](../research/CURRENT_WORK.md).
<!-- OPENMIND:CURRENT-WORK-LINK:END -->

This directory documents active and historical experimental work.

Experiments under `experiments/model_fractal/` are not automatically production capabilities.
Promotion requires reproducible evidence, controls, validation, documented limitations, and an explicit promotion decision.

## Current Research Tracks

### 1. Representation Recurrence

Current focus: determine whether token-conditioned internal representations recur across non-adjacent transformer layers beyond appropriate controls.

Primary current candidates:

- `all_token_recurrence.py` — original all-token baseline
- `all_token_recurrence_no_t00.py` — controlled baseline excluding structural T00 case
- `recurrence_controls_v1.py` — recurrence control experiments
- `recurrence_structure_analysis.py` — structural recurrence analysis
- `recurrence_token_topology_v1.py` — token-level topology analysis
- `recurrence_topology_v3.py` — current permutation-topology candidate; seed 1337, 1000 permutations, T00 excluded
- `cross_prompt_recurrence_v1.py` — independent prompt recurrence analysis

Historical methodological iterations currently retained for provenance:

- `all_token_recurrence_no_t00_original.py`
- `recurrence_topology_v1.py`
- `recurrence_topology_v2.py`

### 2. MAF Engineering

MAF experiments investigate whether measured representation structure can be stored, indexed, reconstructed, streamed, or accessed more efficiently.

Current subtracks include:

- indexed access
- workload benchmarking
- reconstruction
- streaming
- native neighborhood access
- Lodgepole organization and scaling
- cross-prompt holdout testing

MAF engineering results must not be treated as evidence that representation recurrence exists; they depend on independently validated measurements.

### 3. Earlier Model-Fractal Research

The directory also contains earlier geometry, lattice, waveform, phase, parameter-field, and fractal experiments.

These remain experimental research history unless separately promoted through the MAF validation process.

## Promotion Rule

Experimental work may be promoted toward the current MAF surface only when it has:

1. a defined hypothesis or engineering question;
2. immutable input provenance;
3. a reproducible execution command;
4. appropriate controls or baseline;
5. deterministic or statistically characterized output;
6. result artifact hashes;
7. documented limitations;
8. tests or benchmark evidence where applicable;
9. no unsupported architectural or scientific claim;
10. an explicit promotion commit.

## Current Canonical Measurement Artifact

All-token activation capture V1 is documented at:

`docs/experiments/ACTIVATION_CAPTURE.md`

Its tracked manifest is:

`experiments/data/manifests/activation_vectors_all_tokens_v1.json`

#### Current MAF engineering checkpoint

The active MAF engineering line has progressed through the persistent object
pipeline and runtime/residency correctness gates into Phase 6D locality
research.

Accepted state:

- Phase 6B is **COMPLETE / CLOSED**.
- Atomic Activation is complete and validated.
- Rollback is complete and validated.
- Resident PK Directory is complete, validated, benchmarked, and diagnostically accepted.
- Segment Reader V1 is complete, validated, benchmarked, and diagnostically accepted.
- Phase 6C MAF Object Runtime and Residency is **CLOSED / PASS** for its
  preregistered correctness surface.
- Phase 6C has **no performance verdict** and executed **no benchmark**.
- Phase 6D is **ACTIVE RESEARCH**.
- Phase 6D locality data-model Validation V1 is **PASS / accepted / frozen**.
- Telemetry snapshot persistence Validation V1.3 is **PASS / accepted / frozen**
  for its preregistered V01-V57 correctness surface.
- No telemetry persistence benchmark was executed; its performance verdict is
  **NONE**.
- Runtime telemetry integration and real-model telemetry collection remain
  separately gated Phase 6D research.
- Phase 6D-Q remains **PROPOSED / NOT VALIDATED**.

The resident directory and runtime layers remain derived state and do not
replace immutable generation authority.

No current accepted evidence establishes MAF-native inference, general
selective tensor avoidance, a replacement for `llama.cpp`, or an overall
inference-performance advantage.
