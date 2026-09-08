# MAF Query Route Cache Validation V1.3 Runner-Only Harness Recovery Preregistration

## 1. Status and scope

This document preregisters a fresh Q4 V1.3 exact-once validation recovery after the permanently spent Q4 V1.2 run failed because of a frozen runner/harness call-arity defect.

This recovery is runner-only. It does not authorize any production-module change, protocol change, scientific-check change, frozen-case change, acceptance-boundary change, or Phase 6E entry.

Q4 V1, V1.1, and V1.2 are permanently spent and MUST NOT be rerun.

Q4 V1.3 science is NOT ENTERED by this preregistration.

## 2. Frozen V1.2 failure evidence

The authoritative V1.2 evidence is frozen as follows:

- V1.2 runner:
  - path: `experiments/model_fractal/maf_query_route_cache_validation_v1_2.py`
  - SHA256: `6287c836bee9b1b69c224e8d5a3b812966287a9d8c17f86d7f6e805854036ac3`
- V1.2 result:
  - path: `experiments/model_fractal/maf_query_route_cache_validation_v1_2.json`
  - SHA256: `b85ad6e128b35512faa4aed25113b887392b29ce8ab4f9d88d6a2b2009cfa1fb`
  - bytes: `1653`
- V1.2 slot:
  - path: `experiments/model_fractal/maf_query_route_cache_validation_v1_2.slot`
  - SHA256: `eb84a7c280c0c39671ca2f7cb2271ff928663eafa82293f4642413f841ace0af`
  - bytes: `1311`
  - durable states: `RESERVATION_PREPARED`, `RESERVED_DURABLE`, `PUBLISHED_DURABLE`
- V1.2 provenance commit:
  - commit: `b8f1e26d20fd52a38540e4ee32a7681671118b48`
  - message: `research: preserve failed Q4 V1.2 exact-once provenance`

The V1.2 result records:

- status: `FAIL`
- all_pass: `false`
- recorded Q4 checks: `0`
- recorded case results: `0`
- failure stage: `post_reservation`
- failure type: `TypeError`
- failure message: `_expect_q4_rejection() missing 1 required positional argument: 'action'`

Therefore V1.2 establishes neither a Q4 scientific PASS nor a Q4 scientific rejection.

## 3. Proven frozen harness defect

The frozen helper signature in V1.1 and V1.2 is:

`_expect_q4_rejection(expected_error, action)`

The frozen V1.2 runner contains exactly one malformed call to that helper, at source line 683 inside `_run_science`:

`_expect_q4_rejection(lambda: validate_route_cache_for_reuse_v1(... expected_source_generation_pk=mismatch_generation ...))`

That call supplies only the action lambda and omits the required `expected_error` argument.

The same malformed call shape is present in the frozen V1.1 runner.

The malformed call tests a source-generation-PK mismatch. The correct rejection class for that identity mismatch is `MAFQueryRouteCacheIdentityError`, as already used by the adjacent frozen identity-mismatch checks.

## 4. Sole authorized scientific-harness correction

A future V1.3 runner MAY correct only the proven malformed call described above by changing it to the semantically equivalent two-argument form:

`_expect_q4_rejection(MAFQueryRouteCacheIdentityError, lambda: validate_route_cache_for_reuse_v1(... expected_source_generation_pk=mismatch_generation ...))`

The lambda body, all keyword arguments, resident snapshot, relationship authority, model PK, and tested generation mismatch MUST remain unchanged.

No other `_expect_q4_rejection` call may be changed.

The helper signature MUST remain unchanged.

No production implementation behavior may be changed.

This correction is classified as a frozen runner/harness repair, not a scientific-design change.

## 5. Fresh V1.3 namespace

The future V1.3 recovery MUST use only the fresh namespace:

- runner: `experiments/model_fractal/maf_query_route_cache_validation_v1_3.py`
- result: `experiments/model_fractal/maf_query_route_cache_validation_v1_3.json`
- slot: `experiments/model_fractal/maf_query_route_cache_validation_v1_3.slot`
- transient partial: `experiments/model_fractal/maf_query_route_cache_validation_v1_3.json.partial`

Before any V1.3 exact-once execution, the result, slot, and partial paths MUST all be absent.

The V1.3 runner MUST be frozen before any V1.3 result, slot, or partial is created.

## 6. Frozen authorities that remain unchanged

The following frozen authorities remain unchanged:

- Q4 validation protocol:
  - path: `experiments/model_fractal/MAF_QUERY_ROUTE_CACHE_VALIDATION_V1_PROTOCOL.md`
  - SHA256: `af587bfe685deb86ac4574b3d41d1a80b5df2cec84bce757eac8c7e307d82ad9`
- Q4 production implementation contract:
  - path: `experiments/model_fractal/MAF_QUERY_ROUTE_CACHE_IMPLEMENTATION_CONTRACT_V1.md`
  - SHA256: `9f253138399383d703fabd6dc6945af2e94c4af29d5b0f2995c0775984e1cf11`
- corrected Q4 production module:
  - path: `experiments/model_fractal/maf_query_route_cache_v1.py`
  - SHA256: `b44eeca010514a0950240fac59469870ccd79150faceebecca105feb3fa02a80`
- primary architecture:
  - path: `experiments/model_fractal/MAF_QUERY_SCOPED_WORKING_SET_ARCHITECTURE.md`
  - SHA256: `7df826096e506d13502e442fb11f7e1f18fb2c5a342f4214b91a3c3df043559c`
- Q4 check matrix SHA256: `8dc81ec92bace5678a983332cdb6aa342ba7341273a18ee51346f96e1a6414da`
- source generation PK: `mafgen:v1:45a80a2aa271ce04853003185b6a1227cb309bd1e3e2dc538eea849fac9f5db0`
- source manifest SHA256: `28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3`
- selection config SHA256: `0caeaeaafdd870e6b02ccc8b4450576883d4ef5234ba689c472e3b14d9dbe120`

The existing runner implementation contract is currently frozen at:

- path: `experiments/model_fractal/MAF_QUERY_ROUTE_CACHE_VALIDATION_RUNNER_IMPLEMENTATION_CONTRACT_V1.md`
- SHA256: `78fcba2b05b6c758898ed83f16d46ed40d25466a6d8cb50d3552c1e1629d7a12`

Before materializing the V1.3 runner, that runner implementation contract MUST be minimally superseded and frozen to bind this V1.3 recovery authority and the future fresh V1.3 namespace while preserving all scientific and exact-once semantics.

No direct Q4 protocol change is authorized.

No direct production-module change is authorized.

## 7. Scientific invariants

The Q4 scientific contract remains unchanged.

All checks Q4-V01 through Q4-V44 MUST remain exactly present with the same meanings and acceptance boundary.

The frozen query cases remain exactly:

- `q001` — `layer 0 attention query`
- `q025` — `layer 0 normalization`
- `q026` — `layer 0 attention`
- `q033` — `weather tomorrow`

The V1.3 runner MUST preserve the complete Q2 and Q3 authority bindings and the frozen Q3 provenance semantics.

No Q4 scientific check may be added, removed, renamed, weakened, strengthened, or semantically reordered by this recovery.

No partial scientific PASS is allowed. Q4 requires the complete frozen acceptance boundary.

## 8. Exact-once invariants

V1.3 MUST retain the existing exact-once state machine and fail-closed persistence behavior:

1. preflight all frozen authorities and pristine V1.3 namespace;
2. create and durably fsync `RESERVATION_PREPARED`;
3. append and durably fsync `RESERVED_DURABLE`;
4. run the frozen Q4 science exactly once;
5. publish the final result using the existing no-overwrite publication semantics;
6. append and durably fsync `PUBLISHED_DURABLE`.

Once V1.3 reaches durable `RESERVED_DURABLE`, V1.3 is permanently spent and MUST NOT be rerun regardless of scientific or harness outcome.

No retry branch is authorized.

## 9. Runner derivation rule

The future V1.3 runner MUST be derived mechanically from the frozen V1.2 runner.

Authorized runner changes are limited to:

1. the four current-run namespace strings from `v1_2` to `v1_3`;
2. the single proven line-683 `_expect_q4_rejection` call-arity correction defined in Section 4;
3. only those frozen authority SHA bindings that become necessarily different because a separately reviewed and frozen runner-contract supersession binds this V1.3 recovery.

No direct production-module change is authorized.

No direct Q4 protocol change is authorized.

No other executable runner logic is authorized to change.

The derived candidate MUST compile without import or execution and MUST be independently static-audited before freeze.

Its authorized delta MUST be exactly reversible to the frozen V1.2 runner after reversing the fresh namespace, the single call-arity correction, and any separately frozen authority rebinding.

## 10. Claim boundary

This recovery does not establish:

- Q4 scientific PASS;
- Q4 scientific rejection;
- inference or generation sufficiency;
- performance parity or superiority;
- model replacement;
- LLM-pipeline replacement;
- MAF-native generation;
- Phase 6E entry.

Those claims remain outside this preregistration.

## 11. Required sequence

The required recovery sequence is:

1. freeze this preregistration as a sole-path documentation commit;
2. post-freeze reverify it;
3. minimally supersede and freeze the runner implementation contract for V1.3 recovery authority;
4. post-freeze reverify that contract supersession;
5. derive the V1.3 runner candidate from frozen V1.2 using only the authorized delta;
6. compile and independently static-audit the candidate without import or execution;
7. freeze the V1.3 runner as a sole-path add;
8. post-freeze reverify the runner;
9. perform a final read-only exact-once pre-arm audit;
10. only after all prior gates pass, invoke V1.3 exactly once.

Until step 10, V1.3 science remains NOT ENTERED.

Phase 6E remains NOT ENTERED.
