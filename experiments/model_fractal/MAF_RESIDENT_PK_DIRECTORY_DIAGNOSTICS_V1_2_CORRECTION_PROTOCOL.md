# MAF Resident PK Directory Diagnostics V1.2 Correction Protocol

## Status

PREREGISTERED CORRECTION. Freeze before execution.

## Preserved lineage

Diagnostics V1.1 correction protocol SHA256: 9f01c39fe8777c6f93eae550d16596af625d3cb86d07993e500c0479648b35ab

Diagnostics V1.1 runner SHA256: 12e70402b018488940c710e4b24a76966d150c91ac113fb89d23656e01e812c2

Diagnostics V1.1 was never executed.

Its result and runtime remain absent.

Diagnostics V1.1 execution is forbidden.

## Preflight clarification

The V1.1 final preflight reported `self` as an unsupported required lookup argument by inspecting the unbound class method.

That is a preflight-helper false positive.

The diagnostic runner calls `inspect.signature(snapshot.lookup)` on a bound method, where `self` is already bound.

No runner correction is authorized for this false positive.

## Confirmed V1.1 coverage defect

Repeated snapshot rebuilds and repeated intentionally failed refreshes execute before the existing tracemalloc, RSS, file-descriptor, and runtime-growth baselines.

Therefore V1.1 can detect logical instability in those paths but cannot detect retained-memory or persistent-resource growth caused specifically by those paths.

This is a diagnostic coverage defect, not a Resident PK Directory engine defect.

## Authorized V1.2 additions

V1.2 adds isolated measurements around the existing 200-build stress block:

- retained tracemalloc growth <= 1,048,576 bytes;
- live ResidentPKSnapshot growth <= 2 objects after garbage collection;
- RSS growth <= 16 MiB;
- file-descriptor growth <= 2;
- diagnostic runtime file count unchanged;
- diagnostic runtime byte count unchanged.

V1.2 adds the same isolated measurements around the existing 200 intentionally failed refreshes:

- retained tracemalloc growth <= 1,048,576 bytes;
- live ResidentPKSnapshot growth <= 2 objects after garbage collection;
- RSS growth <= 16 MiB;
- file-descriptor growth <= 2;
- diagnostic runtime file count unchanged;
- diagnostic runtime byte count unchanged.

V1.2 also installs a post-setup Python audit hook and requires zero write-intent filesystem open events during diagnostic operations.

Read-only opens used for generation validation remain allowed.

## Preserved methodology

Existing V1.1 workloads and thresholds remain unchanged.

The prepared lookup binding correction remains unchanged.

Rebuild count remains 200.

Failed-refresh count remains 200.

Hot lookup count remains 50,000.

Leak lookup count remains 100,000.

Successful-refresh leak count remains 500.

Lookup and refresh degradation workloads and thresholds remain unchanged.

Failure-path object-identity preservation remains unchanged.

No existing threshold is relaxed.

## Execution

V1.2 must receive a separate frozen-state preflight before execution.

V1.2 is exact-once if eventually executed.

No automatic retry is permitted.

## Nonclaims

No Resident PK Directory production code is changed.

No accepted functional or benchmark evidence is changed.

No Segment Reader is implemented.

No Phase 6C work begins.
