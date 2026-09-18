# MAF Resident PK Directory Performance Benchmark V1.1 Correction Protocol

## Status

PREREGISTERED CORRECTION. Must be frozen before V1.1 execution.

## Preserved V1 evidence

Benchmark V1 was executed exactly once and returned code 1 before publishing a raw result.

The V1 benchmark runtime is preserved as failed evidence and must not be deleted or reused.

Benchmark V1 must never be rerun.

Performance measurement was not reached by the failed V1 attempt.

## Confirmed root cause

The frozen Activation V1.1 `_segment_path_mapping` contract requires `segment_paths` to be a dict.

Its exact value flow is:

    for segment_id in descriptor_ids:
        value = segment_paths[segment_id]
        path = Path(value)
        mapped[segment_id] = path

Therefore the exact required contract is:

    dict[segment_id -> path-like]

The failed benchmark V1 instead constructed:

    segment_paths = []

and appended copied paths without descriptor segment-id keys.

Activation correctly rejected that input with:

    MAFActivationError: segment_paths mapping required

This is classified as a frozen Benchmark V1 runner input-contract defect.

No Resident PK Directory engine defect is indicated.

No Activation engine defect is indicated.

No functional-validation defect is indicated.

## Static-audit note

The g6 helper labelled the contract unresolved because its local assignment tracker inspected only top-level function-body statements.

Its own extracted nested source body nevertheless proved the exact value flow above.

That helper classification is therefore a static-audit false negative, not a runtime ambiguity.

## Authorized V1.1 correction

V1.1 may change only the following behavioral adapter:

1. initialize `segment_paths` as a dict instead of a list;
2. after copying each segment, store the copied path under the exact descriptor `segment_id` key.

V1.1 must also use distinct schema/version/result/runtime identities and bind this correction protocol.

## Frozen methodology requirement

The original V1 benchmark methodology and acceptance thresholds remain authoritative and unchanged:

- sizes remain 100, 1,000, 10,000, and 100,000;
- repetition counts remain unchanged;
- lookup warmups remain unchanged;
- build and refresh warmups/repetitions remain unchanged;
- direct lookup measurement remains unchanged;
- explicit linear baseline remains unchanged;
- memory measurement remains unchanged;
- scaling acceptance thresholds remain unchanged;
- actual build/refresh measurement remains unchanged.

No performance threshold may be relaxed because V1 failed.

## V1.1 execution rule

After V1.1 is frozen, it may be executed exactly once only when its result and runtime are both absent.

A failed or negative V1.1 result must be preserved without automatic retry.

Raw evidence must be frozen before semantic interpretation.

## Nonclaims

This correction does not implement Segment Reader V1.

It does not select a production storage engine.

It does not enable MAF-native compute or inference.

It does not begin Phase 6C.
