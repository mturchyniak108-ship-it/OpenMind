# MAF Segment Locality Runtime Telemetry Integration Validation V1.2 Protocol

Status: PREREGISTERED / RUNNER NOT IMPLEMENTED / SCIENTIFIC EXECUTION NOT AUTHORIZED

Phase: 6D — Segment Locality and Path-Aware Repacking

## 1. Purpose

Validation V1.2 is the fresh exact-once successor validation for frozen
Runtime Telemetry Integration V1.1.

It tests whether the successor implementation corrects the substantive V06
manifest-binding defect while preserving the scientifically valid Integration
V1 behavior.

Historical Validation V1 and Validation V1.1 MUST NOT be rerun.

## 2. Frozen authorities

Integration V1.1 protocol SHA256:

`98f86d72ce2119e76349360d801c39b8184bbad2ec6f968fda4047fd132944ec`

Integration V1.1 implementation SHA256:

`850c4bae5f6c361c34f504b5af76b9ac6530980d777f8bd1a9003f3b9bb55ae6`

Phase 6C runtime SHA256:

`4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9`

Phase 6D telemetry data model SHA256:

`5432f2d74a610f2d0f9181e9af146013bb198a4e837af634993909358fff8ad0`

Telemetry persistence implementation SHA256:

`cb1e2e3dc11006c75e38e33c941b39959aa4d99f971de9e08250d8b995fe09b0`

Resident PK directory SHA256:

`4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6`

Segment reader SHA256:

`3499cb8e528fe8e9315e3e5656d6aa888c95ca175310b6371e722de409827369`

Historical Validation V1.1 protocol SHA256:

`105d448397a03f2ced7e66871f46e85f83f3e8fef673fda369d8f41601b6779e`

Historical Validation V1.1 runner SHA256:

`7b39e22238659a9750d873176039844a92ffe786c6e6775fcaf9d8ab1e6226b6`

Historical authoritative Validation V1.1 result SHA256:

`302dff27ac6ea744a87027248973a2631d8e93d58e674fd8b42612ea317ba3b7`

Historical Validation V1.1 verdict SHA256:

`efeefebc7f79ba110a64de31fc90bd5533ad42b59f8f8ab58d686307e49b31d8`

## 3. Historical interpretation

Historical Validation V1.1 executed all 42 checks and was scientifically
rejected.

Its immutable raw failures remain:

`[V06, V31, V36]`

The frozen verdict classifies:

- V06 as the substantive Integration V1 manifest-binding defect;
- V31 as a validation-assertion false negative;
- V36 as a validation-order false negative.

Validation V1.2 MUST preserve that history and MUST NOT rewrite the old result.

## 4. Successor validation namespace

Protocol:

`experiments/model_fractal/MAF_SEGMENT_LOCALITY_RUNTIME_TELEMETRY_INTEGRATION_VALIDATION_V1_2_PROTOCOL.md`

Runner:

`experiments/model_fractal/maf_segment_locality_runtime_telemetry_integration_validation_v1_2.py`

Final result:

`experiments/model_fractal/maf_segment_locality_runtime_telemetry_integration_validation_v1_2.json`

Exclusive reservation path:

`experiments/model_fractal/maf_segment_locality_runtime_telemetry_integration_validation_v1_2.json.partial`

Verdict:

`experiments/model_fractal/MAF_SEGMENT_LOCALITY_RUNTIME_TELEMETRY_INTEGRATION_VALIDATION_V1_2_VERDICT.md`

Result schema:

`openmind.maf_segment_locality_runtime_telemetry_integration_validation.v1_2`

Expected scientific check count:

`42`

## 5. Exact-once arm

Scientific execution requires BOTH:

CLI flag:

`--arm-exact-once`

Environment variable:

`OPENMIND_ARM_RUNTIME_TELEMETRY_INTEGRATION_VALIDATION_V1_2=YES`

Either mechanism alone is insufficient.

An unarmed invocation MUST be inert and MUST NOT reserve the exact-once slot.

No automatic retry is permitted.

## 6. Mandatory non-spending fixture qualification

The runner MUST provide:

`--qualify-fixture`

Qualification occurs only after all frozen authority checks pass and before
any exact-once reservation.

Qualification MUST construct canonical synthetic V1.2 identities and a
synthetic segment sufficient to create four valid ResidentPKEntry objects.

Canonical identity grammar MUST be:

- model PK: `mafmodel:v1:` plus 64 lowercase hex;
- generation PK: `mafgen:v1:` plus 64 lowercase hex;
- object PK: `mafobj:v1:` plus 64 lowercase hex.

Qualification MUST instantiate the exact frozen Integration V1.1
implementation and exact frozen runtime, register all four matching entries,
verify registration identity/order/length preservation, and close cleanly.

Qualification MUST NOT:

- reserve the result slot;
- create final or partial result files;
- execute V01-V42;
- emit a scientific PASS/FAIL verdict;
- access a real model;
- run inference;
- execute Phase 6E;
- access the network;
- launch subprocesses.

Qualification failure leaves the V1.2 exact-once slot UNSPENT.

## 7. Exact-once execution order

The armed path MUST execute in this order:

1. verify dual-arm mechanisms;
2. verify V1.2 result, partial and verdict namespace is empty;
3. revalidate every frozen authority SHA256;
4. execute canonical fixture qualification;
5. on qualification failure stop with the slot UNSPENT;
6. exclusively reserve the partial result path using create-and-fail-if-exists semantics;
7. execute V01-V42 exactly once;
8. construct the authoritative PASS, FAIL or post-reservation auditor-failure result;
9. durably flush result bytes;
10. publish final result with no-replace semantics;
11. never execute the scientific matrix again.

Once step 6 succeeds, the V1.2 slot is SPENT regardless of later success or
failure.

## 8. Post-reservation failure rule

Any harness/auditor exception after exclusive reservation MUST itself be
frozen as an authoritative V1.2 result with:

- `all_pass = false`;
- `check_count = 0` unless completed checks are authoritatively represented;
- `auditor_error.type`;
- `auditor_error.message`;
- frozen runner and protocol identities.

A post-reservation exception MUST NOT trigger an automatic retry.

## 9. Result publication

The partial result reservation MUST be exclusive.

The final result MUST be published with no-replace semantics.

The runner MUST fsync result bytes before publication and MUST refuse to
overwrite an existing final result.

Historical result files MUST never be modified.

## 10. Scientific matrix

### V01 — Predecessor identity

Revalidate exact Integration V1.1 protocol and implementation identities.

### V02 — Runtime identity

Revalidate exact frozen Phase 6C runtime bytes.

### V03 — Data-model identity

Revalidate exact frozen Phase 6D telemetry data-model bytes.

### V04 — Persistence identity

Revalidate exact frozen telemetry persistence implementation bytes.

### V05 — Clean attachment

Adapter attaches only to a pristine, open, empty, unpinned and unresident runtime with zero counters.

### V06 — Exact binding and manifest rejection

Verify exact model/generation/manifest telemetry binding; wrong manifest must raise the exact preregistered IntegrationError before runtime or telemetry registration, preserve the complete no-commit invariant, not fault telemetry, and permit a subsequent valid registration. Wrong model and wrong generation remain rejected.

### V07 — First sequence

First committed telemetry primitive has sequence 1.

### V08 — Sequence continuity

Every subsequent committed primitive increments sequence by exactly one.

### V09 — Serialized success

Successful serialized access emits ACCESS then the exact serialized-cache HIT semantics.

### V10 — Serialized unavailable

Unavailable serialized access emits the exact ACCESS/MISS semantics without fabricated residency success.

### V11 — Dense success

Successful dense access emits ACCESS then the exact dense-cache HIT semantics.

### V12 — Dense unavailable

Unavailable dense access emits the exact ACCESS/MISS semantics.

### V13 — Unknown object

Unknown-object failure emits no ACCESS or CACHE event.

### V14 — Closed runtime

Closed-runtime behavior remains runtime-identical and emits no fabricated ACCESS or CACHE event.

### V15 — Cold to mapped

COLD_DISK to MAPPED promotion emits the exact committed residency primitive.

### V16 — Mapped to HOT_MAF

Mapped to HOT_MAF emits exact BYTES_READ followed by PROMOTION.

### V17 — Byte authority

Committed BYTES_READ byte_count equals the frozen registered ResidentPKEntry.length.

### V18 — HOT_MAF to HOT_DENSE

Dense promotion emits exact MATERIALIZATION followed by PROMOTION.

### V19 — Downward demotion

Downward state transitions emit explicit adjacent DEMOTION primitives without collapsing intermediate states.

### V20 — No synthetic skips

No skipped or invented state-transition primitive is emitted.

### V21 — ensure_state preservation

ensure_state return value and runtime behavior are preserved exactly.

### V22 — Pin preservation

pin returns the exact runtime PinLease behavior and token semantics.

### V23 — Partial failure

A partially committed runtime operation records only primitives that actually committed before failure.

### V24 — No-commit failure

A runtime operation that commits no residency/read/materialization state emits none of those primitives.

### V25 — Registration inventory

Successful registration preserves exact registration order and byte length and emits no telemetry event.

### V26 — Close behavior

close preserves deterministic runtime demotions and corresponding telemetry semantics.

### V27 — Cache names

Serialized and dense cache names equal the frozen canonical names.

### V28 — Non-access operations

state, snapshot and unpin do not create ACCESS events.

### V29 — Prefetch boundary

Unsupported prefetch remains absent/zero and is never synthesized.

### V30 — Successful result preservation

Successful adapter calls return the exact runtime result.

### V31 — Outcome parity

Corrected assertion: control-success/integrated-success is parity; equal exception type plus exact message is parity; any differing outcome is failure.

### V32 — Telemetry failure isolation

Telemetry failure cannot replace or corrupt an already committed successful runtime result.

### V33 — Sticky telemetry fault

Once telemetry faults, scientific telemetry export remains permanently blocked while exact fault diagnostics remain available.

### V34 — Deterministic trace

Equivalent deterministic operations produce the exact canonical telemetry trace.

### V35 — Runtime snapshot parity

Control and integrated paths end with equal Phase 6C RuntimeSnapshot state.

### V36 — Logical identity preservation

Corrected assertion: model_pk and generation_pk must match exactly and RuntimeSnapshot.objects object PKs must equal sorted(entry.object_pk for entry in fixture entries), matching the frozen runtime canonical lexical order rather than fixture insertion order.

### V37 — Authority preservation

Segment, object, model and generation authority are not rewritten or inferred by telemetry integration.

### V38 — Filesystem boundary

Integration execution performs no project filesystem writes.

### V39 — Network/subprocess boundary

Integration execution performs no network access and launches no subprocess.

### V40 — Persistence boundary

Integration performs no automatic telemetry persistence.

### V41 — Composition boundary

No runtime subclassing, monkey patching, callback injection or frozen-authority mutation occurs.

### V42 — Final authority revalidation

Revalidate all frozen predecessor SHA256 authorities after the complete scientific matrix.

## 11. V06 exact successor requirements

The wrong-manifest case MUST use an otherwise valid entry whose model PK and
generation PK match the runtime while its generation_manifest_sha256 differs
from the adapter source_manifest_sha256.

It MUST verify exact exception class:

`MAFSegmentLocalityRuntimeTelemetryIntegrationError`

and exact message:

`entry generation manifest differs from adapter source manifest binding`

Immediately after rejection it MUST verify:

- runtime snapshot unchanged;
- runtime object count unchanged;
- object absent from runtime inventory;
- registered-length inventory unchanged;
- registration-order inventory unchanged;
- next telemetry sequence unchanged;
- telemetry snapshot unchanged;
- fault flag/count/type/message unchanged;
- telemetry fault diagnostics unchanged;
- no telemetry event emitted;
- a subsequent correct registration of that object succeeds.

## 12. V31 corrected parity definition

The V31 outcome comparator MUST represent both successful completion and
exceptions.

Parity is true exactly when either:

1. control succeeds and integrated succeeds; or
2. both raise, with identical concrete exception type and exact message.

Success versus exception, different exception type, or different exception
message is failure.

The historical V31 helper semantics MUST NOT be copied unchanged.

## 13. V36 corrected identity definition

The frozen Phase 6C runtime canonicalizes RuntimeSnapshot.objects in lexical
object-PK order.

V36 MUST therefore compare the observed object-PK sequence against:

`sorted(entry.object_pk for entry in entries)`

It MUST NOT compare RuntimeSnapshot.objects against fixture insertion order.

Model PK and generation PK must still match exactly.

## 14. Scientific isolation

The scientific validation MUST use synthetic fixture data only.

It MUST NOT:

- access a real model;
- run inference;
- execute Phase 6E;
- run a performance benchmark;
- access the network;
- launch subprocesses;
- modify frozen predecessor implementations;
- automatically persist telemetry.

## 15. Runner construction gate

Freezing this protocol authorizes construction of a V1.2 validation runner.

It does NOT authorize exact-once scientific execution.

Before any scientific arm, the runner MUST be:

1. implemented in the V1.2 namespace;
2. statically audited against this protocol;
3. byte-frozen in a runner-only local commit;
4. tested in unarmed guard-false mode;
5. tested in non-spending fixture-qualification mode;
6. subjected to a final exact-once readiness audit.

Only after every pre-spend gate passes may V1.2 be explicitly armed.

## 16. Phase gate

Integration V1.1 remains scientifically unaccepted until Validation V1.2
produces an authoritative PASS.

Phase 6D remains NOT YET ACCEPTED.

Phase 6E remains BLOCKED.
