# MAF Query Route Cache Validation V1.3 — Closure Verdict

## Verdict

**PASS — Phase 6D-Q4 is closed on frozen V1.3 evidence.**

The exact-once V1.3 runner completed once from frozen source commit `47c598ffbb26c2078aba7c8cf3550efaeb160889` and returned RC 0. The durable result contains `status=PASS`, `all_pass=true`, and the complete ordered `Q4-V01` through `Q4-V44` set with every check passed.

## Frozen scientific evidence

- Runner path: `experiments/model_fractal/maf_query_route_cache_validation_v1_3.py`
- Runner SHA256: `bafed2c9ef6d2cf35d8d5212bbb17497f68a67fff9a67d855ac96243af3ac686`
- Runner bytes: 42578
- Runner freeze commit: `47c598ffbb26c2078aba7c8cf3550efaeb160889`
- Result path: `experiments/model_fractal/maf_query_route_cache_validation_v1_3.json`
- Result SHA256: `1be2608271e899d320b4255fccba2e64c1616281110ebb375f803a7f740c43e0`
- Result bytes: 9184
- Slot path: `experiments/model_fractal/maf_query_route_cache_validation_v1_3.slot`
- Slot SHA256: `af63aa8d3b769ad984b898d805ff45361eb5e079658d47a088514d3ba4145a2d`
- Slot bytes: 1311
- Passing-provenance commit: `b386abde55b1b8f156292eb7500fb739ea8be918`
- Runner implementation contract SHA256: `daa291fcb06c0456e028807308e35ef86486e5176b4fe88d254915718d6943e4`
- V1.3 recovery preregistration SHA256: `3537f1a45bb2452c1aa08ecbd27cdb009f39d809c4d0872f6290622c1c955be8`
- Q4 validation protocol SHA256: `af587bfe685deb86ac4574b3d41d1a80b5df2cec84bce757eac8c7e307d82ad9`
- Production module SHA256: `b44eeca010514a0950240fac59469870ccd79150faceebecca105feb3fa02a80`

## Frozen cases

| Case | Query | Class |
| --- | --- | --- |
| `q001` | `layer 0 attention query` | `specific_intent` |
| `q025` | `layer 0 normalization` | `multi_target_intent` |
| `q026` | `layer 0 attention` | `multi_target_intent` |
| `q033` | `weather tomorrow` | `fallback_control` |

All four cases produced valid deterministic route-cache records and accepted exact-context reuse.

## Exact-once provenance

The durable slot contains exactly three ordered records:

1. `RESERVATION_PREPARED`
2. `RESERVED_DURABLE`
3. `PUBLISHED_DURABLE`

The state-specific schemas are authoritative runner schemas. The reserved record binds the prepared-record SHA256, and the published record binds the reserved-record SHA256 plus the exact final result SHA256 and byte count.

No `.partial` residue remains.

V1.3 reached `RESERVED_DURABLE`; therefore V1.3 is permanently spent and MUST NOT be rerun.

Earlier exact-once attempts remain permanently spent:

- V1 — runner/harness defect before scientific checks.
- V1.1 — frozen production-persistence platform-portability defect.
- V1.2 — frozen runner-harness call-arity defect.
- V1.3 — 44/44 scientific PASS.

These earlier failed runs are provenance, not scientific Q4 rejections.

## Reviewer correction

A post-freeze reviewer initially required one identical slot schema across all three records. That assumption was incorrect. The frozen runner authorizes state-specific schemas:

- `openmind.maf_query_route_cache_validation.slot.prepared.v1`
- `openmind.maf_query_route_cache_validation.slot.reserved_durable.v1`
- `openmind.maf_query_route_cache_validation.slot.published_durable.v1`

The corrected review passed with the record-hash chain, state sequence, result binding, and all scientific evidence intact.

## Claim boundary

Q4 establishes only the frozen protocol scope:

`safe_generation_bound_route_metadata_persistence_reuse_invalidation_only`

Q4 does **not** establish or claim:

- inference execution;
- answer generation;
- working-set sufficiency;
- performance metrics or superiority;
- output parity;
- route-expansion optimality;
- MAF-native compute;
- replacement of the underlying LLM.

## Phase boundary

**Phase 6E is READY FOR ENTRY REVIEW but remains NOT ENTERED by this verdict or documentation update.**

Entering Phase 6E requires a separate human-reviewed entry action under the project development procedure.

## Closure authority

This verdict summarizes already frozen scientific evidence. It does not alter the Q4 protocol, preregistrations, implementation contracts, runner, result, slot, or prior exact-once history.
