# MAF Current Work

<!-- MAF_CURRENT_WORK_AUTHORITY_V2_BEGIN -->
> **Current authority — post-Phase-6:** Whole Phase 6 is formally closed. **MAF — Model Address Fabric** is the active successor identity for model-object representation/addressing work. Documentation publication and live-site deployment are complete. The older Phase 6D/Q2/Q4 status sections below are preserved historical status snapshots; they are not the current phase state. This status note does not authorize a Phase-6 rerun, MAFDB implementation, package/native/schema rename, repository/remote rename, external integration, successor runtime work or model execution.
<!-- MAF_CURRENT_WORK_AUTHORITY_V2_END -->

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

## Scientific authority
- branch: `labs/multidimensional-maf`
- V1.4 protocol SHA256: `a814bca93a6b014ee53aad234b8396c841d0efc2a9363598e8a2192f23745699`
- frozen V1.4 runner commit: `d9056941f2db77f521222f38b125927ae16bbf3e`
- V1.4 runner SHA256: `7bda960c125786fdf3cfca65c4b7b5851ca8bd91257282facfee2fec1ae7a030`

## Phase state
- 6B: closed
- 6C: closed
- 6D: active
- 6D-Q2: authoritative V1.4 query-to-PK selection validation PASS — 74/74
- 6E: not entered

## Q2 V1.4
The durable exact-once V1.4 protocol and validation runner are frozen.

Static closure established:
- V01-V74 exact count/order: PASS
- journal schemas: PASS
- unconditional slot/partial/result namespace guard: PASS
- `RESERVATION_PREPARED -> RESERVED_DURABLE -> SCIENCE` ordering: PASS
- permanent namespace spend after successful slot creation: PASS
- absolute post-slot no-retry semantics: PASS
- no-replace result publication and durability barriers: PASS
- non-finite canonical JSON forbidden with `allow_nan=False`
- unchanged V1 scientific metric surface: 17/17 fields
- result binds exact `validation_runner_sha256`

The initial post-freeze audit reported `runner_sha_pre_slot`. Exact source
inspection closed that finding as an audit matcher false-negative:
`_full_prequalification()` calls `_qualify_authorities()`, which verifies the
runner SHA authority/self-hash path, and full prequalification completes before
the first V1.4 slot creation.

Authoritative execution order begins:
`NAMESPACE_GUARD -> PREQUAL -> SLOT_CREATE -> PREPARED_WRITE -> SLOT_FSYNC -> DIR_FSYNC -> RESERVED_DURABLE_APPEND -> SLOT_FSYNC -> DIR_FSYNC -> PARTIAL_CREATE -> SCIENCE`.

The V1.4 runner reuses the frozen V1 scientific evaluation and preserves its
scientific metric schema. The V1.4 harness changes execution durability,
exact-once handling, provenance and the V01-V74 validation surface; it does not
claim new science before execution.

## Scientific boundary
- authoritative run: PASS — 74/74
- authoritative result SHA256: `b2ad49d7a9a3e1ef565e07e595efc4a4e00b283f422723553c6437ef3a42def6`
- authoritative verdict SHA256: `c17198e0013fd9c0a8c59b8f09c05d4f22693dc7d56afdc0f761f55a008c2663`
- authoritative freeze commit: `10da372a8317dc629674fb2b52a7560f55ee416f`
- V01-V74: ALL PASS
- result: PRESENT — authoritative frozen result
- partial: ABSENT
- exact-once slot: SPENT
- retry: FORBIDDEN

Q2 does not establish inference, answer generation, selective-working-set
sufficiency, tensor/object avoidance, output parity, answer quality,
MAF-native compute, performance improvement, or LLM replacement.

## Authority order
1. exact source/Git commit
2. frozen protocols and runner SHA authorities
3. tests/static audits
4. immutable validated results
5. manifests/provenance
6. current-status docs
7. README/roadmap

Termux click-paste operations are atomic and no-heredoc; see
`docs/development/TERMUX_WORKFLOW.md`.

## Next scientific gate
**6D-Q3 — attach/detach ownership and cleanup semantics.**

Q3 requires a new preregistration and authority boundary. It must validate query-scoped object ownership, attachment lifetime, deterministic detach and cleanup, generation binding, and failure cleanup without modifying or rerunning Q2 V1.4 evidence.

The roadmap then proceeds to 6D-Q4 route reuse with generation binding. Phase 6E remains not entered.

Human-readable Q2 explanation: `Q2_V1_4_SUMMARY.md`.

<!-- MAF_CURRENT_WORK_POST_PHASE6_V1 -->
## Post-Phase-6 current state

Whole Phase 6 is formally closed.

Current authorized successor work is documentation,
terminology, lineage and compatibility design for
**MAF — Model Address Fabric**.

The completed Phase-6 scientific evidence remains frozen.

Current documentation work does not authorize:

- Phase-6 reruns;
- mutation of frozen evidence;
- schema migration;
- package/native rename;
- repository/remote rename;
- MAFDB implementation;
- native/NEON/Vulkan successor implementation;
- GPT-OSS model work.

See `PHASE_6_SUMMARY.md` for the bounded closure summary.
