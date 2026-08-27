# OpenMind Labs

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

These remain experimental research history unless separately promoted through the OpenMind validation process.

## Promotion Rule

Experimental work may be promoted toward the professional OpenMind surface only when it has:

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
