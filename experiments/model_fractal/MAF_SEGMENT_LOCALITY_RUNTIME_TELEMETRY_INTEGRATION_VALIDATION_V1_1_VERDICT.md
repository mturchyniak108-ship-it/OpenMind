# MAF Segment Locality Runtime Telemetry Integration Validation V1.1 Verdict

## Status

**SCIENTIFIC REJECTION — AUTHORITATIVE**

Validation V1.1 executed its complete preregistered scientific matrix.

- checks executed: `42 / 42`
- raw `all_pass`: `false`
- raw failed checks: `V06`, `V31`, `V36`
- auditor error: `none`
- exact-once slot: **SPENT**
- V1.1 rerun: **PERMANENTLY FORBIDDEN**

The frozen runtime telemetry integration is scientifically rejected because
of the substantive failure in **V06**.

Subsequent read-only classification established that V31 and V36 are
validation-assertion false negatives and do not represent additional
integration defects.

## Frozen identities

Repository parent at raw-result freeze lineage:

`ad75329fc253f6b79140c70a926a59c6ec47129c`

Validation V1.1 protocol SHA256:

`105d448397a03f2ced7e66871f46e85f83f3e8fef673fda369d8f41601b6779e`

Validation V1.1 runner SHA256:

`7b39e22238659a9750d873176039844a92ffe786c6e6775fcaf9d8ab1e6226b6`

Validation V1.1 authoritative raw result SHA256:

`302dff27ac6ea744a87027248973a2631d8e93d58e674fd8b42612ea317ba3b7`

Runtime telemetry integration V1 SHA256:

`0c805296ca1eca8926dbd8ce28badc6b87b56bd482280624548e1ea7d53ae7bb`

Phase 6C object runtime SHA256:

`4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9`

Phase 6D telemetry data model SHA256:

`5432f2d74a610f2d0f9181e9af146013bb198a4e837af634993909358fff8ad0`

Historical spent Validation V1 raw result SHA256:

`f45517765d35e84493a5f414353b0fb887d6aae68cbea38f021276ddc6a5d521`

Historical Validation V1 verdict SHA256:

`8812bf265ba1cf821c0048c28c3bc2840e2ee029069273344aceeb0324e6d842`

## V06 — substantive integration binding failure

**Classification: SUBSTANTIVE INTEGRATION FAILURE**

The adapter correctly inherits the frozen runtime's model/generation
binding enforcement.

A mismatched `model_pk` was rejected with:

`MAFObjectRuntimeStaleGenerationError`

A mismatched `generation_pk` was rejected with:

`MAFObjectRuntimeStaleGenerationError`

However, an entry carrying a mismatched
`generation_manifest_sha256` was accepted.

The frozen integration `register_entry()` delegates registration to the
Phase 6C runtime and records object PK/length telemetry bookkeeping, but
does not compare the entry's `generation_manifest_sha256` against the
adapter's bound `source_manifest_sha256`.

Therefore the adapter does not enforce the complete generation identity
required by the preregistered exact-binding criterion.

This is sufficient by itself to reject Runtime Telemetry Integration V1.

## V31 — validation assertion false negative

**Classification: VALIDATION ASSERTION FALSE NEGATIVE**

V31 was intended to verify preservation of runtime failure type and
message.

For every recorded case, the control runtime and integrated runtime
behaved identically:

- unknown object: identical `MAFObjectRuntimeUnknownObjectError`;
- serialized residency unavailable: identical
  `MAFObjectRuntimeResidencyUnavailableError`;
- dense residency unavailable: identical
  `MAFObjectRuntimeResidencyUnavailableError`;
- closed-runtime `state()` case: both control and integrated calls
  completed without an exception.

The integrated path therefore preserved the control behavior exactly.

The V31 raw failure arose because the validation helper treated the
closed-runtime pair of successful calls as failure-comparison failure,
despite parity being preserved.

V31 is not evidence of an integration defect.

## V36 — validation ordering false negative

**Classification: VALIDATION ORDER FALSE NEGATIVE**

V36 expected runtime-snapshot object PKs in fixture insertion order.

The frozen Phase 6C runtime intentionally constructs `RuntimeSnapshot`
objects in canonical lexical object-PK order using:

`for object_pk in sorted(self._records)`

The V36 observation preserved:

- the exact `model_pk`;
- the exact `generation_pk`;
- the complete set of four `object_pk` values.

Only ordering differed.

The observed object-PK list matched the frozen runtime's canonical sorted
ordering.

No logical identity was lost, added, substituted, or modified.

V36 is therefore not evidence of an integration identity defect.

## Scientific interpretation

The authoritative V1.1 result remains unchanged:

`failed_checks = [V06, V31, V36]`

The historical raw result MUST NOT be rewritten to remove V31 or V36.

Interpretation of that immutable result is:

- **V06:** substantive integration defect;
- **V31:** validation-assertion false negative;
- **V36:** validation-order false negative.

Scientific rejection is justified by V06 alone.

## Integration disposition

`maf_segment_locality_runtime_telemetry_integration_v1.py` is **NOT
ACCEPTED** as the authoritative Phase 6D runtime telemetry integration.

It MUST remain frozen as the implementation tested by Validation V1.1.

It MUST NOT be silently patched in place and represented as the same
validated implementation.

## Correction path

A successor implementation must add explicit manifest binding at the
integration boundary.

At minimum, registration must refuse an entry when:

`entry.generation_manifest_sha256 != adapter.source_manifest_sha256`

The correction must preserve the already-correct model/generation binding
behavior and telemetry semantics.

The frozen V1 integration remains historical evidence and must not be
modified.

## Successor validation requirements

Before preregistering a successor scientific validation:

1. correct the V31 assertion so exact control/integrated parity passes even
   when both operations succeed;
2. correct V36 to compare logical identity according to the frozen
   runtime's canonical snapshot ordering or compare the object-PK set
   where ordering is not part of the identity criterion;
3. preserve an explicit negative manifest-binding test equivalent to V06;
4. require the wrong-manifest case to fail before telemetry registration
   bookkeeping commits;
5. preserve the remaining scientifically valid V01-V42 requirements unless
   a separately preregistered successor protocol explicitly changes them.

A successor must use a new implementation and validation namespace.

Validation V1.1 MUST NEVER be rerun.

## Scope exclusions

Validation V1.1 did not:

- access a real model;
- run inference;
- execute Phase 6E;
- run a benchmark;
- access the network;
- launch a subprocess.

## Phase disposition

Phase 6D runtime telemetry integration is **NOT YET ACCEPTED**.

Phase 6E remains blocked until a corrected successor integration passes a
new preregistered scientific validation.
