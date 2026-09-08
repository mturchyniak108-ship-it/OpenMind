# OpenMind Phase 6E Entry Checkpoint

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

**PHASE 6E ENTRY BOUNDARY FROZEN**

Phase 6D is scientifically accepted and closed.

Phase 6E is unblocked for prospective design and preregistration work.

No Phase 6E implementation or scientific execution is authorized by this
checkpoint.

## Frozen design authorities

Roadmap:

`ROADMAP.md`

SHA256:

`50ecfa32aa64e5b0b8b0a1e8f0fbc9802de537284ca36aa9f1594bcc6ea4c94c`

Query-scoped working-set architecture:

`MAF_QUERY_SCOPED_WORKING_SET_ARCHITECTURE.md`

SHA256:

`7df826096e506d13502e442fb11f7e1f18fb2c5a342f4214b91a3c3df043559c`

Dense compute-view boundary:

`MAF_DENSE_COMPUTE_VIEW_BOUNDARY_V1_PROTOCOL.md`

SHA256:

`e67dc84bd86d0e46cc26823b3e000ae1daf29618e1d9fdffc4f11ede4fec55d3`

Accepted Phase 6D verdict:

`MAF_SEGMENT_LOCALITY_RUNTIME_TELEMETRY_INTEGRATION_VALIDATION_V1_2_VERDICT.md`

SHA256:

`c147e811a98688c6ed067f3f82305f97e0dda4d996991bab730120eaacafd622`

## Phase 6E scientific objective

The frozen Phase 6E question is whether OpenMind can selectively access,
reconstruct, or materialize a bounded MAF working set rather than complete
dense tensors while preserving the correctness required by the authorized
comparison boundary.

A smaller payload, lower resident byte count, or lower RAM footprint alone
does not establish success.

Correctness evidence comes first.

Performance remains a later Phase 6F question.

## Mandatory progression

The frozen roadmap progression is interpreted prospectively as:

1. Phase 6D-Q1 — Query Capsule and Query Route Cache schemas
2. Phase 6D-Q2 — non-oracle query-to-PK selection feasibility
3. Phase 6D-Q3 — attach, detach, ownership, cleanup, and failure atomicity
4. Phase 6D-Q4 — generation-bound Query Route Cache behavior
5. Phase 6E-A — selective working-set sufficiency
6. Phase 6E-B — bounded expansion and recovery
7. Phase 6E-C — actual tensor/object avoidance
8. Phase 6E-D — output parity and quality
9. Phase 6F — performance measurement after correctness

The four Phase 6D-Q gates are prerequisites for authoritative Phase 6E-A
scientific execution.

The Phase 6E-A protocol may be designed prospectively before those gates
close, but it MUST NOT authorize implementation-dependent scientific
execution until it can bind the exact accepted Phase 6D-Q authorities.

## Phase 6E-A question

The Phase 6E-A scientific question is:

> Given an accepted non-oracle query-derived PK candidate selector and an
> authorized Query-Scoped MAF Capsule bound to one immutable source
> generation, is the selected initial MAF working set sufficient to reproduce
> the authorized full-reference state required by the frozen comparison
> contract?

Phase 6E-A tests **sufficiency**.

It does not prove actual tensor/object avoidance.

It does not measure performance.

It does not authorize MAF-native compute.

## Selection boundary

Authoritative Phase 6E-A PK selection MUST derive from the accepted
Phase 6D-Q2 non-oracle selector.

The selector MUST NOT consume:

- expected answers;
- reference logits;
- reference hidden states;
- test labels unavailable to the real execution path;
- full-reference PK usage discovered from the comparison run;
- post hoc information selected because it makes the test pass.

The full-reference execution is an evaluation oracle only.

It MUST NOT become a selection oracle.

Hand-authored or oracle-complete PK sets may be used for harness
qualification or debugging only and MUST NOT count as authoritative
Phase 6E-A scientific evidence.

## No-expansion rule for Phase 6E-A

Phase 6E-A evaluates the initial selected working set.

Automatic bounded expansion is disabled for the authoritative Phase 6E-A
sufficiency decision.

If the initial working set is insufficient, Phase 6E-A records that negative
result.

The experiment MUST NOT rescue the hypothesis by adding PKs post hoc.

Deterministic bounded expansion belongs to Phase 6E-B.

## Conventional compute boundary

The conventional dense compute backend remains authorized.

Selective MAF access may create the exact dense views required by that
existing backend.

This does not imply that dense tensors remain the persistent model authority.

It also does not establish direct computation on MAF bytes.

## Phase 6E-C separation

Phase 6E-A success does not establish that unnecessary objects or tensors
were actually avoided.

Actual touch/read/materialization avoidance is a separate Phase 6E-C claim
and requires independent instrumentation and validation.

## Phase 6E-D separation

Phase 6E-A does not establish end-to-end language-model quality equivalence.

Output parity, logits, top-k behavior, token agreement, and generation-quality
effects belong to the separately preregistered Phase 6E-D fidelity boundary
unless a narrower comparison is explicitly required by the Phase 6E-A
protocol.

## MAF-native compute boundary

Direct MAF-native compute remains:

`disabled_unvalidated`

Phase 6E does not automatically enable computation directly on persistent
MAF bytes.

Direct MAF-native computation requires its own independent numerical and
inference-fidelity validation after the required fidelity gates pass.

## Negative-result rule

The Phase 6E hypothesis is falsifiable.

If a valid non-oracle selected working set is insufficient under the frozen
Phase 6E-A contract, the result MUST be recorded as a negative result.

The working set, selector, comparison rule, or acceptance threshold MUST NOT
be changed after observing the authoritative result in order to rescue the
hypothesis.

Any materially changed experiment requires a fresh preregistered namespace.

## Current authorization boundary

Authorized now:

- Phase 6D-Q1 prospective protocol design and preregistration;
- subsequent Phase 6D-Q work only after its preceding gate closes;
- prospective Phase 6E protocol design that does not depend on unknown future
  scientific outcomes.

Not authorized now:

- Phase 6E-A authoritative execution;
- bounded-expansion claims;
- tensor/object avoidance claims;
- output-quality claims;
- performance claims;
- MAF-native compute;
- rerunning Validation V1.2.

## Next gate

**BEGIN PHASE 6D-Q1 PREREGISTRATION**

Phase 6D-Q1 must freeze deterministic Query-Scoped MAF Capsule and Query Route
Cache schemas.

It makes no inference, sufficiency, avoidance, quality, or performance claim.
