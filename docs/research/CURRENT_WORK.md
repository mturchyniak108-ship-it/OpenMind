# OpenMind Current Work

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
Q2 V1.4 is closed and must not be rerun. Any next Phase 6D-Q experiment must
have a separate preregistration and authority boundary before execution.
Phase 6E remains not entered.