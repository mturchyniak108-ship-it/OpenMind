# MAF Query Route Cache Validation V1.1 Recovery Preregistration

Status: preregistration candidate. Q4 V1.1 science is NOT ENTERED.

## 1. Purpose

This document preregisters one recovery revision for Phase 6D-Q4 after the permanently spent Q4 V1 namespace failed because of a validation-runner harness defect before Q4-V01 completed.

This document does not reopen, alter, erase, or rerun Q4 V1.

## 2. Immutable V1 provenance

- Q4 V1 frozen runner SHA256: `0dfea009ea8984770858c326c955a26f07d8496e9e6c8cb333fdaa9c17d9ba87`
- Q4 V1 failed result SHA256: `e5c1cf91d0929f9ee2d5c492ecfa082887bd94db16448b9f34c59af689165e63`
- Q4 V1 permanent slot SHA256: `ba262ccb0b07c92160ed6c40c3d1c9510e4582fadc0661b206f947cb17c522f6`
- Q4 validation protocol SHA256: `af587bfe685deb86ac4574b3d41d1a80b5df2cec84bce757eac8c7e307d82ad9`
- Q4 runner implementation contract SHA256: `1d57f67e5944c6a04e50c3f18c458872b56cf45937ba04b72d529b0b78aec20c`
- Q4 production module SHA256: `a168528b47b2575fb18dc68d36a1c31ab6390534a779d5c769299a3dc891d507`

V1 is permanently spent and MUST NOT be rerun.

## 3. Proven V1 harness defect

The frozen V1 runner called `catalog.catalog_sha256()` even though frozen Q2 defines `MAFQueryPKCatalogV1.catalog_sha256` as an `@property` returning `str`.

The frozen V1 runner also contains `config.selection_config_sha256()` even though frozen Q2 defines `MAFQueryToPKSelectionConfigV1.selection_config_sha256` as an `@property` returning `str`.

The first defect at V1 runner line 483 raised `TypeError: str object is not callable` before Q4-V01 completed.

V1 completed 0 of 44 checks and 0 of 4 frozen query cases. Therefore V1 establishes no Q4 scientific PASS or FAIL verdict.

## 4. Scientific design remains frozen

V1.1 MUST preserve all 44 Q4-V01 through Q4-V44 check identifiers and their order.

V1.1 MUST preserve frozen cases `q001`, `q025`, `q026`, and `q033`.

Q2 selector semantics, resident object-PK authority, ephemeral relationship authority, route-cache identity and payload semantics, typed Q4-V28 through Q4-V37 rejection classes, the corrected Q4-V34 route-order tamper, metadata-only persistence, Q3-style cleanup, exact-once durability, and the Q4 claim boundary remain unchanged.

No scientific hypothesis, case, check, threshold, route policy, payload field, authority, or claim may change in V1.1.

## 5. Fresh Q4 V1.1 exact-once namespace

- runner: `experiments/model_fractal/maf_query_route_cache_validation_v1_1.py`
- result: `experiments/model_fractal/maf_query_route_cache_validation_v1_1.json`
- slot: `experiments/model_fractal/maf_query_route_cache_validation_v1_1.slot`
- partial result: `experiments/model_fractal/maf_query_route_cache_validation_v1_1.json.partial`

The V1.1 result, slot, and partial paths MUST be absent before V1.1 execution.

V1.1 MUST NOT overwrite, mutate, rename, delete, or reuse the V1 result or V1 slot.

## 6. Exact permitted V1 to V1.1 runner delta

The V1.1 runner MUST be derived from the exact frozen V1 runner.

Only these four source-delta categories are permitted:

1. Replace `catalog.catalog_sha256()` with `catalog.catalog_sha256`.
2. Replace `config.selection_config_sha256()` with `config.selection_config_sha256`.
3. Change the logger namespace from `openmind.maf_query_route_cache_validation_v1` to `openmind.maf_query_route_cache_validation_v1_1`.
4. Change only the `RESULT_PATH`, `SLOT_PATH`, and `PARTIAL_PATH` filenames from the V1 execution namespace to the V1.1 execution namespace.

No other source delta is permitted.

`RUNNER_PATH = Path(__file__).resolve()` remains the self-binding mechanism so V1.1 records the exact V1.1 runner SHA256.

The result schema and slot-record schemas remain unchanged because the scientific result and durability data formats are unchanged.

## 7. Review and freeze before arm

Before any V1.1 slot reservation, this recovery preregistration MUST be independently reviewed and frozen.

The untracked V1.1 runner candidate MUST then pass an exact source-delta audit against frozen V1, compile without import or execution, and pass independent semantic review of all authorities, 44 checks, four cases, typed negative tests, Q4-V34, relationship-authority closure, and exact-once ordering.

The accepted V1.1 runner MUST be frozen in an exact-path commit and the unused V1.1 result, slot, and partial namespace MUST be reverified before V1.1 may be armed.

## 8. Exact-once rule

Once durable V1.1 slot reservation succeeds, V1.1 is permanently spent whether the run passes, fails, or aborts.

V1.1 MUST NOT be silently retried.

## 9. Phase boundary

V1.1 exists only to recover from the proven V1 runner harness defect while preserving the original frozen Q4 science.

Phase 6E is NOT entered by this preregistration, runner construction, review, freeze, or V1.1 execution.
