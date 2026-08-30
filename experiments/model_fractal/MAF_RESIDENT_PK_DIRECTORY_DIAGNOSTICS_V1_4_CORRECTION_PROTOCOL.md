# MAF Resident PK Directory Diagnostics V1.4 Correction Protocol

## Status

PREREGISTERED CORRECTION. Freeze before execution.

## Preserved V1.3 lineage

Diagnostics V1.3 protocol SHA256: e6e3a0d3995550106c9abf8a60c586b01083fb6e971573df26f3552c06292ff6

Diagnostics V1.3 runner SHA256: 972fa763ea233f791add465ca73c3743d8e4d68d092edd7b874288562e8aea35

Diagnostics V1.3 was never executed.

Its result and runtime remain absent.

Diagnostics V1.3 execution is forbidden.

## Confirmed V1.3 diagnostic defect

The final frozen-state preflight resolved the engine-defined stale-generation rejection exception as:

    MAFResidentPKDirectoryStaleSnapshotError

V1.3 requires all stale attempts to fail and requires one stable exception type, but it does not require that stable type to equal the engine-defined stale-snapshot exception.

Therefore a consistently wrong exception could falsely satisfy the stale-state diagnostic.

This is a diagnostic acceptance defect, not a Resident PK Directory engine defect.

## Authorized V1.4 correction

V1.4 preregisters the exact expected stale exception type as MAFResidentPKDirectoryStaleSnapshotError.

The existing 200 stale-generation attempts remain unchanged.

The existing requirement that all 200 attempts reject remains unchanged.

The existing stable-exception-type requirement remains unchanged.

V1.4 additionally requires the observed exception-type set to equal exactly the preregistered engine-defined exception type.

The expected exception type is recorded in the raw result.

## Preserved methodology

All V1.3 build, hash/file-validation, stale-state, lookup, refresh, memory, object-retention, RSS, file-descriptor, runtime-accumulation, write-audit, failure-preservation, and degradation workloads and thresholds remain unchanged.

No existing threshold is relaxed.

No production engine code is changed.

## Execution rule

V1.4 must receive a separate final frozen-state preflight.

If accepted, V1.4 may execute exactly once.

No automatic retry is permitted.

## Nonclaims

No functional validation or benchmark lineage is rerun.

No Segment Reader is implemented.

Phase 6C is not started.
