# MAF Segment Locality Runtime Telemetry Integration V1.1 Protocol

Status: PREREGISTERED / IMPLEMENTATION NOT STARTED / VALIDATION NOT AUTHORIZED

Phase: 6D — Segment Locality and Path-Aware Repacking

## 1. Purpose

Integration V1.1 is a narrowly scoped successor to frozen Runtime Telemetry
Integration V1.

Its sole substantive correction is enforcement of the source generation
manifest binding discovered by authoritative Validation V1.1 check V06.

Integration V1 MUST remain frozen and unchanged.

## 2. Frozen predecessor authorities

Integration V1 protocol SHA256:

`078ab7c95bd98b94cc24a5af19bd876d69fec860a77e781aa12b6ec57262434c`

Integration V1 implementation SHA256:

`0c805296ca1eca8926dbd8ce28badc6b87b56bd482280624548e1ea7d53ae7bb`

Frozen Phase 6C runtime SHA256:

`4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9`

Frozen Phase 6D telemetry data-model SHA256:

`5432f2d74a610f2d0f9181e9af146013bb198a4e837af634993909358fff8ad0`

Historical Validation V1.1 protocol SHA256:

`105d448397a03f2ced7e66871f46e85f83f3e8fef673fda369d8f41601b6779e`

Historical Validation V1.1 runner SHA256:

`7b39e22238659a9750d873176039844a92ffe786c6e6775fcaf9d8ab1e6226b6`

Historical authoritative Validation V1.1 result SHA256:

`302dff27ac6ea744a87027248973a2631d8e93d58e674fd8b42612ea317ba3b7`

Historical Validation V1.1 verdict SHA256:

`efeefebc7f79ba110a64de31fc90bd5533ad42b59f8f8ab58d686307e49b31d8`

The historical Validation V1.1 slot is spent and MUST NEVER be rerun.

## 3. Scientific motivation

Validation V1.1 executed all 42 preregistered checks with no auditor error.

The authoritative raw failures were V06, V31, and V36.

Post-result classification established:

- V06 is a substantive integration binding failure;
- V31 is a validation-assertion false negative;
- V36 is a validation-order false negative.

Scientific rejection of Integration V1 is justified by V06 alone.

## 4. V06 defect

The frozen Phase 6C runtime binds model PK and generation PK.

Integration V1 additionally accepts a constructor argument:

`source_manifest_sha256`

and passes that binding into the frozen `TelemetryAccumulator`.

A registered `ResidentPKEntry` independently carries:

`generation_manifest_sha256`

Integration V1 does not compare those two manifest identities before
delegating registration to the Phase 6C runtime.

Therefore an otherwise valid entry can be registered against an adapter bound
to a different source manifest.

That behavior violates the exact source-generation identity required for
scientific telemetry.

## 5. Successor namespace

The successor implementation path is:

`experiments/model_fractal/maf_segment_locality_runtime_telemetry_integration_v1_1.py`

The successor module version is:

`v1.1`

The predecessor implementation file MUST NOT be modified.

## 6. Allowed implementation delta

Integration V1.1 MUST begin from the exact frozen Integration V1 bytes and may
change only what is required for successor provenance and manifest binding.

Authorized semantic changes are:

1. identify the implementation as Integration V1.1;
2. bind the eventual frozen V1.1 protocol SHA256;
3. preserve the validated constructor `source_manifest_sha256` as an adapter
   private binding after successful constructor validation;
4. reject an otherwise valid registration whose
   `entry.generation_manifest_sha256` differs from that adapter binding;
5. perform that rejection before runtime registration and before telemetry
   registration bookkeeping.

No other Integration V1 behavior is intentionally changed.

## 7. Constructor binding

The existing constructor argument remains:

`source_manifest_sha256`

The frozen `TelemetryAccumulator` remains the validation authority for that
constructor value.

Only after construction of the accumulator succeeds, the adapter MUST retain
the exact validated manifest identity for registration-time comparison.

The intended private binding name is:

`_source_manifest_sha256`

The V1.1 implementation MUST NOT weaken or bypass the existing data-model
validation of this SHA256 value.

## 8. Registration manifest guard

For an otherwise structurally valid, not-yet-registered entry whose model PK
and generation PK are compatible with the attached runtime, successful
adapter-mediated registration requires:

`entry.generation_manifest_sha256 == self._source_manifest_sha256`

If that equality is false, registration MUST fail.

The manifest guard MUST occur before:

`self._runtime.register_entry(entry)`

and before any registration telemetry bookkeeping commits.

## 9. Manifest-mismatch error contract

An otherwise valid manifest-mismatched registration MUST raise:

`MAFSegmentLocalityRuntimeTelemetryIntegrationError`

The successor implementation MUST use the exact message:

`entry generation manifest differs from adapter source manifest binding`

The mismatch is an expected input/binding rejection.

It MUST NOT mark the telemetry trace faulted.

## 10. Manifest-mismatch no-commit invariant

After a manifest-mismatched registration attempt:

- the Phase 6C runtime MUST contain no newly registered object from that
  attempt;
- `_registered_lengths` MUST be unchanged;
- `_registration_order` MUST be unchanged;
- `_next_sequence` MUST be unchanged;
- no telemetry event MUST be emitted;
- telemetry aggregate state MUST be unchanged;
- telemetry fault state MUST be unchanged;
- the adapter MUST remain usable for a subsequent valid registration.

The central V1.1 correction invariant is:

**wrong manifest -> reject before runtime registration -> no telemetry
bookkeeping -> no partial state change**

## 11. Existing runtime authority

The Phase 6C runtime remains authoritative for:

- entry structural validation;
- model-PK binding;
- generation-PK binding;
- duplicate object rejection;
- runtime closed-state behavior;
- residency behavior;
- pin behavior;
- byte-budget behavior;
- runtime snapshots.

Integration V1.1 MUST NOT broaden its correction into a replacement runtime
validation system.

The new manifest-binding behavior is defined for the V06 scientific case:
an otherwise valid entry with correct runtime model/generation identity and a
manifest identity different from the adapter binding.

No intentional change to unrelated invalid-entry error precedence is
authorized.

## 12. Successful registration behavior

When the entry manifest matches the adapter binding, V1.1 MUST preserve
Integration V1 registration behavior:

1. delegate registration to the exact frozen Phase 6C runtime;
2. commit adapter registration bookkeeping only after runtime registration
   succeeds;
3. record the exact object PK;
4. record the exact serialized length;
5. emit no telemetry event for registration;
6. return the exact runtime registration result.

## 13. Existing telemetry semantics

Except for rejection of a wrong-manifest registration, V1.1 MUST preserve the
scientifically specified Integration V1 semantics for:

- sequence numbering;
- ACCESS events;
- CACHE events;
- RESIDENCY events;
- BYTES_READ events;
- MATERIALIZATION events;
- PROMOTION events;
- DEMOTION events;
- pin/unpin behavior;
- close behavior;
- telemetry-fault handling;
- deterministic snapshots;
- cache names;
- registered-byte authority;
- persistence compatibility.

## 14. Composition boundary

Integration V1.1 remains a composition adapter around the exact frozen Phase
6C `MAFObjectRuntime`.

It MUST NOT:

- subclass the runtime;
- monkey patch the runtime;
- inject callbacks into frozen runtime code;
- modify the frozen runtime;
- modify the frozen telemetry data model;
- modify Integration V1 in place.

## 15. Historical result preservation

The authoritative Validation V1.1 result remains exactly:

`failed_checks = [V06, V31, V36]`

That raw historical result MUST NOT be rewritten.

Integration V1.1 is a successor implementation, not a reinterpretation or
replacement of the tested Integration V1 bytes.

## 16. Successor validation prerequisites

No exact-once successor scientific validation may be preregistered until the
implementation has first been statically audited against this protocol.

A successor validation must use a new validation namespace and a new
exact-once slot.

It MUST NOT reuse or rerun Validation V1.1.

## 17. Mandatory successor negative manifest test

The successor validation MUST include an otherwise valid entry whose:

- model PK matches the runtime;
- generation PK matches the runtime;
- entry generation-manifest SHA256 differs from the adapter
  `source_manifest_sha256`.

The test MUST verify:

- exact `MAFSegmentLocalityRuntimeTelemetryIntegrationError`;
- exact preregistered error message;
- runtime object count unchanged;
- no registered object committed;
- registration-order inventory unchanged;
- registered-length inventory unchanged;
- sequence unchanged;
- telemetry snapshot unchanged;
- telemetry trace not faulted;
- a subsequent valid registration still succeeds.

## 18. V31 successor correction

Historical V31 was a validation false negative.

The successor validation failure-parity helper MUST consider the following
pair to be parity:

- control succeeds;
- integrated succeeds.

It must also consider the following pair to be parity:

- control and integrated raise the same exception type and message.

It MUST fail only when control and integrated behavior differs.

## 19. V36 successor correction

Historical V36 was a validation-order false negative.

The frozen Phase 6C runtime intentionally returns runtime snapshot objects in
canonical lexical object-PK order.

The successor validation MUST either:

- compare object PKs in the runtime's canonical sorted order; or
- compare logical object identity as a set when ordering is not itself the
  criterion.

It MUST NOT require fixture insertion order from `RuntimeSnapshot.objects`.

## 20. Preservation matrix

The successor validation SHOULD preserve every scientifically valid V01-V42
criterion from Validation V1.1 unless a separately preregistered successor
validation protocol explicitly documents a necessary correction.

V31 and V36 must use the corrected assertions specified above.

The V06 successor criterion must require manifest mismatch rejection and the
full no-commit invariant.

## 21. Scope exclusions

Integration V1.1 implementation and its implementation audit MUST NOT:

- access a real model;
- run inference;
- execute Phase 6E;
- benchmark runtime performance;
- access the network;
- launch subprocess-based scientific workloads.

## 22. Phase gate

Phase 6D remains NOT ACCEPTED while this successor is unvalidated.

Phase 6E remains blocked.

A V1.1 implementation freeze does not itself constitute scientific
acceptance.

Phase 6D may advance only after a new preregistered successor validation
accepts the corrected implementation.

## 23. Implementation authorization

Freezing this protocol authorizes creation of a candidate Integration V1.1
implementation conforming exactly to this protocol.

It does NOT authorize scientific validation.

The implementation must be built, statically audited, and frozen before a
successor validation protocol is preregistered.
