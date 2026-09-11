# MAF Research Documentation

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

Current authority:
- `CURRENT_WORK.md`
- `MAF_CURRENT_STATUS.md`

Proposed work, frozen mechanisms, executed results and promoted research are distinct states.
