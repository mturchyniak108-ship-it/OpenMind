# MAF Resident PK Directory Diagnostics V1.3 Correction Protocol

## Status

PREREGISTERED. Freeze before any execution.

## Preserved lineage

Diagnostics V1.2 protocol SHA256: fbaaeb38346d5173637f31579e72e880a807dfea31d7d92434fc9af040cf23a8

Diagnostics V1.2 runner SHA256: 9cfca287a6edff317a27ed650f8984057175f1028a6f596a8073892bc5a5fde6

Diagnostics V1.2 was never executed.

Its result and runtime remain absent.

V1.2 execution is forbidden.

## Complete-coverage preflight result

The V1.2 preflight reported zero static failures and a fully supported bound lookup contract.

Three requested post-validation surfaces remained uncovered:

1. sustained build-path degradation;
2. sustained physical hash/file-validation degradation within that build path;
3. explicit stale-generation/state rejection stress.

These are diagnostic coverage gaps, not production-engine defects.

## V1.3 build degradation diagnostic

V1.3 adds:

- 2 build warmup batches;
- 20 measured build batches;
- 25 complete build_snapshot operations per batch;
- median ns/op comparison of the first 5 measured batches against the last 5;
- final/initial build degradation ratio <= 2.5.

Each measured operation executes the real build_from_prepared path.

That path executes Resident PK Directory build_snapshot and current-candidate physical validation.

Therefore the build drift measurement includes repeated manifest/file opening, physical segment validation, and hash-validation cost performed by the frozen engine.

The same measured build ratio is recorded as the end-to-end hash/file-validation degradation sentinel.

This is a sustained-degradation sentinel, not an absolute latency guarantee.

## V1.3 stale-state diagnostic

V1.3 constructs a same-format generation PK that differs from the snapshot generation PK.

It prepares a lookup using that deliberately stale expected generation.

It performs 200 stale-generation lookup attempts.

Every attempt must fail.

The rejection exception type must remain stable.

The resident snapshot projection must remain unchanged.

The stale-state block also measures:

- retained tracemalloc growth <= 262,144 bytes;
- live snapshot growth <= 2;
- RSS growth <= 16 MiB;
- file-descriptor growth <= 2;
- runtime file count unchanged;
- runtime byte count unchanged.

## Preserved V1.2 methodology

All existing V1.2 workloads, limits, thresholds, failure tests, build leak checks, failed-refresh leak checks, lookup leak checks, refresh leak checks, write-intent audit, lookup degradation checks, and refresh degradation checks remain unchanged.

No prior threshold is relaxed.

## Execution rule

V1.3 must receive a separate final frozen-state preflight before execution.

If accepted, V1.3 may execute exactly once.

No automatic retry is permitted.

## Nonclaims

No production engine code is changed.

No benchmark or functional validation is rerun.

No Segment Reader is implemented.

Phase 6C is not started.
