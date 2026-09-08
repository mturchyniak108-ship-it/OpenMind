# OpenMind Q2 V1.4 — What the Result Means

## Result

**Authoritative result: PASS — 74/74.**

Q2 V1.4 is closed. Its exact-once namespace is permanently spent and the experiment must not be rerun.

## What Q2 tested

Q2 tested whether the frozen non-oracle selector could take a prospective query and select the intended persistent MAF object primary keys (PKs) under preregistered rules and budgets.

Evaluation surface:

- evaluation queries: **40**
- specific-intent queries: **24**
- fallback/control queries: **8**
- unique expected object PKs: **12**

Measured results:

- supported-intent target hit rate: **1.0**
- supported-intent precision: **1.0**
- specific-intent top-1 accuracy: **1.0**
- deterministic random-baseline top-1 accuracy: **0.041666666666666664**
- selector minus baseline difference: **0.9583333333333334**
- structural, budget, and oracle-input violations: **0**

## What this means

Within the frozen Q2 evaluation, OpenMind demonstrated that a query can be mapped to the intended MAF object PKs without supplying the expected PK answer to the selector.

This validates the routing and selection step needed before OpenMind can construct query-scoped MAF working sets.

The result moves query-to-object routing from architecture-only status to validated research for the exact frozen Q2 scope.

## What this does not establish

Q2 does not establish:

- inference or answer generation;
- working-set sufficiency;
- selective tensor or object avoidance;
- output parity with the full model;
- answer quality;
- MAF-native compute;
- latency, memory, energy, or throughput superiority;
- replacement of llama.cpp or a conventional LLM pipeline.

These require separate prospective experiments.

## What comes next

The roadmap-defined next gate is **6D-Q3 — attach/detach ownership and cleanup semantics**.

Q3 tests lifecycle correctness for query-scoped objects: ownership, attachment lifetime, deterministic detach and cleanup, generation binding, and cleanup after failure.

After Q3, the existing roadmap proceeds to **6D-Q4**, testing exact or similar query-route reuse with generation binding.

Only after the Phase 6D-Q prerequisites are closed should the separately gated Phase 6E experiments begin.

Phase 6E remains **not entered**.

## Frozen evidence

- result SHA256: `b2ad49d7a9a3e1ef565e07e595efc4a4e00b283f422723553c6437ef3a42def6`
- verdict SHA256: `c17198e0013fd9c0a8c59b8f09c05d4f22693dc7d56afdc0f761f55a008c2663`
- evidence freeze commit: `10da372a8317dc629674fb2b52a7560f55ee416f`
- synchronized status commit: `49ec4ed23f9e96be0eb07dbfbfab6ad61b28567b`

This page explains the frozen evidence; it does not replace it.
