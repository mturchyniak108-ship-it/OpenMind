# MAF Segment Locality Runtime Telemetry Integration Validation V1.1 Protocol

## Status

**PREREGISTERED — SUCCESSOR HARNESS CORRECTION ONLY**

Validation V1.1 is a successor to spent Validation V1.

It does **not** change the scientific question, integration implementation,
runtime implementation, telemetry data model, persistence authority, or
V01–V42 acceptance matrix.

The only permitted change from V1 is validation-harness correctness.

## Historical predecessor

Validation V1 exact-once execution is permanently spent and MUST NOT be
rerun or replaced.

Frozen V1 identities:

- V1 protocol SHA256: `5cd24df624e8dea9571a1ac8d7e2ac7f8de998e8176c3772590f271687cc5fbb`
- V1 runner SHA256: `1566bf938b071b1c8f3c42a7bb1093586ede66c26f95abd8332b83a8384870c3`
- V1 raw result SHA256: `f45517765d35e84493a5f414353b0fb887d6aae68cbea38f021276ddc6a5d521`
- V1 verdict SHA256: `8812bf265ba1cf821c0048c28c3bc2840e2ee029069273344aceeb0324e6d842`
- V1 disposition: `INVALID / HARNESS FAILURE`
- V1 checks executed: `0 / 42`

V1 failed before the scientific matrix because its synthetic fixture used
raw 64-character SHA256 strings where the frozen telemetry data model
requires namespaced canonical primary keys.

This protocol is rooted at repository commit:

`a34facae69a437e7741b1c703d2a3c70c2178956`

## Frozen implementation authorities

The successor validation MUST test these exact frozen bytes:

- Phase 6C runtime SHA256: `4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9`
- Phase 6D telemetry data-model SHA256: `5432f2d74a610f2d0f9181e9af146013bb198a4e837af634993909358fff8ad0`
- Runtime telemetry integration SHA256: `0c805296ca1eca8926dbd8ce28badc6b87b56bd482280624548e1ea7d53ae7bb`

No modification to those implementations is authorized by this protocol.

## Canonical V1.1 synthetic fixture grammar

The V1.1 harness MUST construct synthetic identities as follows.

### model_pk

Exactly:

`"mafmodel:v1:" + <64 lowercase hexadecimal SHA256>`

The suffix MUST be exactly 64 lowercase hexadecimal characters.

### generation_pk

Exactly:

`"mafgen:v1:" + <64 lowercase hexadecimal SHA256>`

The suffix MUST be exactly 64 lowercase hexadecimal characters.

### object_pk

Exactly:

`"mafobj:v1:" + <64 lowercase hexadecimal SHA256>`

The suffix MUST be exactly 64 lowercase hexadecimal characters.

Each synthetic object MUST receive a unique object PK.

### SHA256 fields

Each of the following MUST be exactly 64 lowercase hexadecimal characters:

- `generation_manifest_sha256`
- `object_file_sha256`
- `payload_sha256`
- `segment_sha256`

### ResidentPKEntry structural fields

The synthetic `ResidentPKEntry` values MUST additionally satisfy the
frozen Phase 6C runtime structure:

- `segment_id` is a non-empty string.
- `offset` is a plain Python `int` and is nonnegative.
- `length` is a plain Python `int` and is strictly positive.
- `segment_length` is a plain Python `int` and is strictly positive.
- `segment_path` is a non-empty string.
- `offset + length <= segment_length`.

The runtime's `model_pk` and `generation_pk` bindings MUST exactly equal
the corresponding values on every registered entry.

The telemetry adapter's source-generation and manifest binding MUST use
those same canonical fixture identities.

## Canonical deterministic construction

The runner MUST derive canonical PK suffixes deterministically from fixed
validation-only byte strings using SHA256.

The recommended construction is:

- model suffix from `b"validation-model-v1.1"`
- generation suffix from `b"validation-generation-v1.1"`
- object suffixes from UTF-8 strings `validation-object-v1.1-<index>`
- manifest SHA from `b"validation-manifest-v1.1"`

The namespaced prefix MUST be added only after computing each SHA256
suffix.

Synthetic segment and payload hashes MUST be calculated from the actual
synthetic bytes used by the fixture.

No real GGUF or production model material may be used.

## Mandatory non-spending fixture qualification

V1.1 MUST add a dedicated fixture-qualification execution mode.

This mode is part of harness qualification and is **not** a scientific
validation execution.

Before the V1.1 exact-once result slot may be reserved, the runner MUST
successfully prove that the synthetic fixture can cross the frozen runtime
entry-validation boundary.

At minimum the qualification MUST:

1. construct the canonical namespaced `model_pk`;
2. construct the canonical namespaced `generation_pk`;
3. construct at least four unique canonical namespaced `object_pk` values;
4. construct all required lowercase SHA256 fields;
5. create the synthetic segment in a temporary directory;
6. create the exact `ResidentPKEntry` objects intended for V01–V42;
7. instantiate a frozen Phase 6C runtime with matching model/generation;
8. register every intended entry successfully;
9. confirm registered object identity/order/length values are preserved;
10. close the qualification runtime cleanly.

The qualification MUST NOT:

- reserve the V1.1 result slot;
- create the V1.1 result or partial result;
- execute V01–V42;
- emit a scientific PASS/FAIL;
- access a real model;
- perform inference;
- execute Phase 6E;
- use the network;
- launch a subprocess;
- mutate any frozen implementation.

A failed qualification MUST leave the V1.1 exact-once slot **UNSPENT**.

The final armed execution MUST perform the same qualification before slot
reservation. Only after qualification succeeds may result reservation
occur.

## Exact-once ordering invariant

For the armed V1.1 path the order MUST be:

1. verify both explicit arm mechanisms;
2. verify result and partial-result namespace is empty;
3. verify frozen authority SHA256 identities;
4. perform canonical fixture qualification;
5. if qualification fails, stop with slot UNSPENT;
6. reserve the V1.1 partial-result slot using exclusive creation;
7. execute V01–V42 exactly once;
8. freeze either scientific PASS/FAIL or post-reservation auditor failure;
9. publish final result with no-replace semantics.

The reservation MUST therefore occur **after fixture qualification and
before scientific execution**.

## Scientific matrix

The V1.1 scientific matrix is inherited unchanged from Validation V1.

The following checks are the complete V1.1 scientific acceptance matrix:

1. V01 — predecessor identity
2. V02 — runtime bytes unchanged
3. V03 — data-model bytes unchanged
4. V04 — persistence bytes unchanged
5. V05 — clean empty attachment
6. V06 — exact binding
7. V07 — sequence first=1
8. V08 — sequence increments by exactly one
9. V09 — serialized success emits ACCESS then CACHE_HIT
10. V10 — serialized unavailable emits ACCESS then CACHE_MISS
11. V11 — dense success emits ACCESS then CACHE_HIT
12. V12 — dense unavailable emits ACCESS then CACHE_MISS
13. V13 — unknown object emits no access/cache event
14. V14 — closed runtime emits no access/cache event
15. V15 — COLD_DISK to MAPPED emits PROMOTION
16. V16 — MAPPED to HOT_MAF emits BYTES_READ then PROMOTION
17. V17 — BYTES_READ equals exact ResidentPKEntry.length
18. V18 — HOT_MAF to HOT_DENSE emits MATERIALIZATION then PROMOTION
19. V19 — every committed downward residency primitive emits exactly the corresponding DEMOTION event
20. V20 — no skipped synthetic events
21. V21 — ensure_state preserves exact runtime semantics
22. V22 — pin preserves exact runtime semantics
23. V23 — partial failure records committed primitives only
24. V24 — no-commit failure emits no residency/read/materialization primitives
25. V25 — registration order/length exact and registration emits no telemetry event
26. V26 — close produces deterministic demotions
27. V27 — cache names exactly match frozen integration constants
28. V28 — state/snapshot/unpin emit no access event
29. V29 — prefetch remains unsupported with zero aggregate representation
30. V30 — successful runtime results are preserved across the shared API surface
31. V31 — runtime failure type and message are preserved
32. V32 — telemetry failure cannot replace a successful runtime result
33. V33 — telemetry fault remains sticky and permanently blocks scientific telemetry export
34. V34 — canonical trace is deterministic
35. V35 — telemetry/control runtimes produce equal Phase 6C RuntimeSnapshot state
36. V36 — logical identities remain unchanged
37. V37 — segment/model authority remains unchanged
38. V38 — integration performs no unauthorized filesystem writes
39. V39 — integration performs no network or subprocess activity
40. V40 — integration performs no automatic persistence
41. V41 — integration uses composition only; no monkey patch or callback injection
42. V42 — all frozen predecessor SHA identities are revalidated

There MUST be exactly 42 scientific checks.

No additional scientific PASS criterion may be silently added.

Harness qualification is a prerequisite to spending the slot but is not a
43rd scientific check.

## V19 clarification retained

V19 MUST evaluate explicit adjacent committed downward primitives:

- `HOT_DENSE -> HOT_MAF`
- `HOT_MAF -> MAPPED`
- `MAPPED -> COLD_DISK`

Each committed primitive MUST correspond to exactly one DEMOTION event.

No synthetic multi-hop transition may be substituted for these three
primitive observations.

## V33 clarification retained

After telemetry becomes faulted:

- a subsequent runtime operation that succeeds MUST still return its
  successful runtime result;
- the telemetry fault MUST remain set;
- scientific telemetry export MUST remain blocked with the frozen
  telemetry-fault exception.

A later successful runtime operation MUST NOT silently clear the fault.

## Exact-once result namespace

Reserved V1.1 paths:

- runner:
  `experiments/model_fractal/maf_segment_locality_runtime_telemetry_integration_validation_v1_1.py`
- result:
  `experiments/model_fractal/maf_segment_locality_runtime_telemetry_integration_validation_v1_1.json`
- partial result:
  `experiments/model_fractal/maf_segment_locality_runtime_telemetry_integration_validation_v1_1.json.partial`
- verdict:
  `experiments/model_fractal/MAF_SEGMENT_LOCALITY_RUNTIME_TELEMETRY_INTEGRATION_VALIDATION_V1_1_VERDICT.md`

Protocol freeze does not spend the V1.1 result slot.

Runner implementation does not spend the V1.1 result slot.

Static inspection does not spend the V1.1 result slot.

Guard-false execution does not spend the V1.1 result slot.

Fixture-qualification execution does not spend the V1.1 result slot.

Only an explicitly dual-armed V1.1 scientific execution may reserve the
V1.1 result slot.

Once reservation succeeds, V1.1 MUST NOT be rerun in place.

If a post-reservation harness/auditor failure occurs, that failure is the
authoritative V1.1 result and any correction requires another successor
validation protocol/version.

## Arming requirement

Scientific execution MUST require both:

- command-line flag `--arm-exact-once`;
- environment variable
  `OPENMIND_ARM_RUNTIME_TELEMETRY_INTEGRATION_VALIDATION_V1_1=YES`.

Either mechanism alone MUST be insufficient.

## Publication requirements

Partial-result reservation MUST use exclusive creation semantics.

Final publication MUST use no-replace semantics.

An existing V1.1 result or partial result MUST cause refusal rather than
overwrite or retry.

## Prohibited scope

Validation V1.1 MUST NOT:

- rerun or replace Validation V1;
- modify the frozen runtime;
- modify the frozen telemetry data model;
- modify the frozen integration;
- use a real GGUF;
- run inference;
- execute Phase 6E;
- run performance benchmarks;
- access the network;
- use automatic persistence;
- monkey patch frozen implementations;
- silently change V01–V42.

## Acceptance

Validation V1.1 is scientifically accepted only if:

- canonical fixture qualification succeeds before reservation;
- the exact frozen authorities revalidate;
- all 42 scientific checks execute;
- V01 through V42 all PASS;
- no auditor error occurs;
- the result is published exactly once.

A qualification failure before reservation is **not** a scientific result
and MUST leave the slot unspent.

A failure after reservation is authoritative and spends the V1.1 slot.
