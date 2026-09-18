# MAF Resident PK Directory Diagnostics V1.1 Correction Protocol

## Status

PREREGISTERED CORRECTION. Freeze before execution.

## Preserved V1 lineage

Diagnostics V1 was frozen but never executed.

Diagnostics V1 protocol SHA256: 5101e4a4dd78b869eb91ce226a1a304181bc2c3636d2ff86a056db15caf0560a

Diagnostics V1 runner SHA256: 88452ca6d8fa0d70c4a9982630b1170fb5034e12871a501ead90f68676e2c8aa

The V1 result and runtime remain absent.

Diagnostics V1 must not be executed.

## Confirmed defect

The frozen V1 `call_lookup` helper performs `inspect.signature(snapshot.lookup)` every time the helper is invoked.

The same helper is used inside:

- the 50,000-lookup hot-path filesystem-I/O diagnostic;
- the 100,000-lookup retained-memory diagnostic;
- the sustained timed lookup degradation batches.

Therefore V1 would measure repeated Python introspection and its allocations in addition to the ResidentPKSnapshot lookup path.

This is classified as diagnostic measurement contamination.

V1 was caught before execution, so no contaminated diagnostic evidence exists.

## Authorized V1.1 correction

V1.1 resolves the lookup signature and keyword binding once during setup.

It creates one prepared lookup operation bound to the current ResidentPKSnapshot.

Hot-path, leak, warmup, and timed lookup loops invoke only that prepared lookup operation.

The prepared operation calls the already-bound `snapshot.lookup` method with the already-resolved keyword arguments.

No `inspect.signature` call may occur inside any measured, leak, hot-path, or sustained lookup loop.

## Preserved methodology

The following remain unchanged from Diagnostics V1:

- rebuild repetitions;
- failed-refresh repetitions;
- hot lookup repetitions;
- leak lookup repetitions;
- leak refresh repetitions;
- lookup and refresh batch counts;
- lookup and refresh batch sizes;
- all retained-memory limits;
- live snapshot growth limit;
- RSS growth limit;
- file-descriptor growth limit;
- runtime file/byte stability checks;
- lookup degradation threshold;
- refresh degradation threshold;
- projection-stability checks;
- failure-path preservation checks.

No threshold is relaxed.

## Lineage

V1.1 uses distinct runner, result, and runtime identities.

The original V1 protocol and runner remain frozen historical preregistration evidence.

## Execution rule

V1.1 must undergo another static preflight after freeze.

It must not execute unless that preflight explicitly marks it safe to execute.

If eventually executed, V1.1 is exact-once and may not be automatically retried.

## Nonclaims

This correction does not change Resident PK Directory production code.

It does not change accepted functional or benchmark evidence.

It does not implement Segment Reader V1.

It does not begin Phase 6C.
