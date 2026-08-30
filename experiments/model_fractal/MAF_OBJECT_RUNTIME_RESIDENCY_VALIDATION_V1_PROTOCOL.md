# OpenMind MAF Object Runtime and Residency Validation V1 Protocol

Status: **PREREGISTERED / UNEXECUTED / EXACT-ONCE**

Schema:

`openmind.maf_object_runtime_residency_validation.v1`

## 1. Purpose

This protocol prospectively freezes the first correctness validation for:

**Phase 6C — MAF Object Runtime and Residency V1**

The validation target is already frozen.

No validation runner exists when this protocol is constructed.

No validation result exists.

No validation runtime exists.

No Phase 6C performance claim is made by this protocol.

## 2. Frozen validation target

Design protocol:

`experiments/model_fractal/MAF_OBJECT_RUNTIME_RESIDENCY_V1_PROTOCOL.md`

SHA256:

`81987d00ef4cb51556dcebf08bff9c9fa8979f033df05304d347b759e545eb13`

Runtime engine:

`experiments/model_fractal/maf_object_runtime_residency_v1.py`

SHA256:

`4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9`

Resident PK Directory V1:

`experiments/model_fractal/maf_resident_pk_directory_v1.py`

SHA256:

`4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6`

Segment Reader V1:

`experiments/model_fractal/maf_segment_reader_v1.py`

SHA256:

`3499cb8e528fe8e9315e3e5656d6aa888c95ca175310b6371e722de409827369`

Phase 6C entry checkpoint:

`experiments/model_fractal/MAF_PHASE_6C_ENTRY_CHECKPOINT.md`

SHA256:

`5f2972d44ddc470aec3826ddda2ebade2fb92b28cbb562a99ab87daa15f21871`

Validation construction parent:

`ecd6a51dd2bd3ab2e137abc996caa66af711e8b9`

All of these identities must remain unchanged through validation execution.

## 3. Validation result path

The one authorized V1 result path is:

`experiments/model_fractal/maf_object_runtime_residency_validation_v1.json`

Before exact-once execution, that path must not exist.

After execution, the raw result must be frozen before interpretation.

## 4. Validation runtime path

The isolated validation runtime is:

`results/runtime/maf_object_runtime_residency_validation_v1`

Before exact-once execution, that directory must not exist.

The validation runner may create it exactly once during the authorized
validation execution.

No cleanup is performed after execution, whether validation passes or fails.

## 5. Frozen source fixture

Read-only source fixture directory:

`results/runtime/maf_resident_pk_directory_benchmark_v1_1`

Required source files:

### active_generation.json

Size:

`380`

SHA256:

`031d1a50a3cf53f158057a02bb6c68001edfb07bf48bf893afc9bc8f095458e9`

### candidate_a.manifest.json

Size:

`1202`

SHA256:

`941301aa362d3f949389e5364b1be4d7f26b96f0d45efa81346c82fce3260f93`

### segment_00000000.mafseg

Size:

`4096`

SHA256:

`f965b526538d757ca2d6114af6517c57cbcb3650b71d8cfb92046a04ef2f566b`

The source fixture is immutable.

The validation runner must copy required source files into the isolated
validation runtime before mutation/corruption tests.

## 6. Fixture construction

The runner must derive a valid `ResidentPKEntry` from frozen Phase 6B
authority.

Permitted predecessor operations include:

- `build_snapshot(...)`;
- `ResidentPKSnapshot.lookup(...)`.

The selected validation entry must have:

- matching runtime `model_pk`;
- matching runtime `generation_pk`;
- positive serialized-object length;
- a range fully inside the copied segment;
- exact frozen hashes inherited from accepted authority.

The entry's `segment_path` may be rebound to the isolated copied segment while
all other semantic identity/range fields remain unchanged.

The isolated clean copied segment must initially hash to:

`f965b526538d757ca2d6114af6517c57cbcb3650b71d8cfb92046a04ef2f566b`

## 7. Runtime construction

Every independent test must construct a fresh runtime unless the test
explicitly validates sequential behavior.

The runtime must be constructed with:

- exact fixture `model_pk`;
- exact fixture `generation_pk`;
- explicitly chosen serialized-byte budget;
- explicitly chosen dense-byte budget;
- deterministic materializer where needed.

Tests must not depend on hidden automatic eviction.

## 8. Deterministic dense materializer

The normal validation materializer receives:

- the immutable `ResidentPKEntry`;
- verified serialized bytes.

It must deterministically return:

- a derived immutable validation view;
- an exact nonnegative byte charge.

The normal dense view must contain enough deterministic evidence to verify it
was derived from the expected entry and verified bytes.

The materializer must not modify the input entry or serialized bytes.

A separate deterministic failing materializer must raise a known validation
exception before returning a view.

## 9. Runtime state ordering

Validation uses the exact public order:

`COLD_DISK < MAPPED < HOT_MAF < HOT_DENSE`

Primitive legal transitions are exactly:

`COLD_DISK -> MAPPED`

`MAPPED -> HOT_MAF`

`HOT_MAF -> HOT_DENSE`

`HOT_DENSE -> HOT_MAF`

`HOT_MAF -> MAPPED`

`MAPPED -> COLD_DISK`

`VULKAN_MAF` is outside V1.

## 10. General pass rule

A check passes only when all assertions for that check pass.

Unexpected exceptions fail the check.

Expected exceptions must match the intended semantic error category.

A validation check must not be marked PASS merely because an exception
occurred.

## 11. Failure atomicity rule

For every expected-failure test, validation must compare state/accounting
before and after the failure.

Unless the protocol explicitly states otherwise, expected failure must
preserve:

- committed residency state;
- serialized-byte accounting;
- dense-byte accounting;
- active pin ownership;
- runtime model/generation identity.

## 12. Required validation checks

The runner must publish exactly the following 32 named checks.

### V01 — runtime_binding

Register an entry whose `model_pk` and `generation_pk` match the runtime.

Registration must succeed.

Separate mismatched-model and mismatched-generation entries must fail before
residency promotion.

### V02 — initial_cold_disk

A newly registered valid object must report exactly:

`COLD_DISK`

It must have:

- zero serialized resident bytes;
- zero dense resident bytes;
- zero pins.

### V03 — legal_upward_primitive_transitions

Starting at `COLD_DISK`, perform exactly:

`COLD_DISK -> MAPPED -> HOT_MAF -> HOT_DENSE`

Each transition must commit the exact requested state.

### V04 — legal_downward_primitive_transitions

Starting at `HOT_DENSE`, perform exactly:

`HOT_DENSE -> HOT_MAF -> MAPPED -> COLD_DISK`

Each transition must commit the exact requested state and release the
corresponding derived resources/accounting.

### V05 — illegal_skipped_transitions

At minimum reject:

- `COLD_DISK -> HOT_MAF`;
- `COLD_DISK -> HOT_DENSE`;
- `MAPPED -> HOT_DENSE`;
- `HOT_DENSE -> MAPPED`;
- `HOT_DENSE -> COLD_DISK`.

Each rejection must preserve the previous committed state.

### V06 — same_state_idempotence

Request the already committed state.

The operation must be a no-op with no duplicated resource/accounting and no
implicit pin change.

### V07 — verified_hot_maf_promotion

Promotion `MAPPED -> HOT_MAF` must succeed through the frozen Segment Reader
boundary.

Returned `serialized_bytes(object_pk)` must equal the exact verified object
range and hash to `object_file_sha256`.

### V08 — corruption_hash_failure_nonpublication

Create a corrupted isolated segment by flipping exactly one bit inside the
selected object range without changing file length.

Use an entry pointing at that corrupted copy while retaining the original
expected object hash.

Promotion to `HOT_MAF` must fail through the verified-read/integrity error
category.

No serialized bytes may become externally available.

State must remain `MAPPED`.

### V09 — short_read_nonpublication

Temporarily replace only the engine module's bound
`read_serialized_object` callable with a deterministic validation double that
raises the frozen Segment Reader short-read error category.

The original callable identity must be restored immediately after the test.

Promotion must fail through the runtime verified-read error category.

State must remain `MAPPED`.

No serialized bytes may escape.

This test validates runtime non-publication/failure atomicity; frozen Segment
Reader short-read correctness is already independently accepted Phase 6B
evidence.

### V10 — stale_generation_rejection

A valid-structure entry with a nonmatching generation must be rejected before
registration/promotion changes runtime state.

### V11 — serialized_byte_accounting

After one successful `HOT_MAF` promotion:

`serialized_resident_bytes == len(serialized_bytes)`

After `HOT_MAF -> MAPPED`:

`serialized_resident_bytes == 0`

No double charge is permitted.

### V12 — dense_byte_accounting

After `HOT_MAF -> HOT_DENSE`:

`dense_resident_bytes == exact materializer charge`

After `HOT_DENSE -> HOT_MAF`:

`dense_resident_bytes == 0`

### V13 — zero_budget_rejection

With serialized budget zero, `MAPPED -> HOT_MAF` must fail without publishing
resident bytes.

With dense budget zero and a positive-charge materializer,
`HOT_MAF -> HOT_DENSE` must fail without publishing a dense view.

### V14 — over_budget_failure_atomicity

Use positive budgets smaller than the required exact charges.

The rejected promotion must preserve the previous committed state and exact
accounting.

### V15 — multiple_pin_floor_composition

Acquire at least:

- one `MAPPED` pin;
- one `HOT_MAF` pin.

Effective pin floor must become `HOT_MAF`.

After consuming the `HOT_MAF` pin, effective floor must become `MAPPED`.

### V16 — pinned_demotion_rejected

With effective floor `HOT_MAF`, demotion below `HOT_MAF` must fail.

With effective floor `MAPPED`, demotion below `MAPPED` must fail.

The failure must not consume the pin.

### V17 — unknown_pin_rejection

Unpinning a token that was never issued must fail with the pin-token error
category.

### V18 — consumed_pin_rejection

Successfully consume one valid pin token.

A second unpin of the same token must fail.

### V19 — unpin_no_automatic_demotion

Unpin a resident object.

Residency state before and immediately after unpin must be identical.

### V20 — dense_materialization_success

Using the deterministic successful materializer, promote:

`HOT_MAF -> HOT_DENSE`

The returned dense view must match deterministic expected content and exact
byte charge.

Persistent/source bytes must remain unchanged.

### V21 — dense_materialization_failure_atomicity

Using the deterministic failing materializer:

`HOT_MAF -> HOT_DENSE`

must fail.

State must remain `HOT_MAF`.

Verified serialized bytes must remain available.

Dense accounting must remain zero.

### V22 — dense_view_lifetime_invalidation

After successful `HOT_DENSE`, obtain the dense view.

Demote to `HOT_MAF`.

A new `dense_view(object_pk)` request must fail as unavailable.

### V23 — runtime_close_cleanup

Create a runtime containing resident serialized bytes, a dense view, and
active pins.

`close()` must:

- clear active pins;
- remove dense ownership;
- remove serialized resident ownership;
- reduce resident byte accounting to zero;
- return registered object states to `COLD_DISK`;
- preserve source files unchanged.

### V24 — close_idempotence

Call `close()` twice.

The second call must succeed as an idempotent no-op.

Accounting must remain zero.

### V25 — operation_rejection_after_close

After close, attempts to:

- register;
- transition;
- pin;
- expose serialized resident bytes;
- expose dense view

must fail through the closed/unavailable lifecycle boundary as applicable.

Snapshot inspection remains permitted if the implementation exposes it after
close.

### V26 — source_file_immutability

Hash all frozen source fixture files before validation.

Hash them again after all checks.

Every source file must remain byte-identical.

### V27 — no_unverified_byte_escape

Combine evidence from:

- corruption failure;
- short-read failure;
- zero/over-budget failure.

No failure path may expose bytes as `HOT_MAF`.

### V28 — snapshot_accounting_consistency

For a mixed runtime containing objects in multiple states, verify the
snapshot's:

- object count;
- per-state counts;
- active pin count;
- serialized resident bytes;
- dense resident bytes.

The sum of per-state counts must equal total object count.

All counters must be nonnegative integers.

### V29 — concurrent_same_object_promotion

Use a synchronized thread start with at least two threads requesting the same
object's promotion to `HOT_MAF`.

Temporarily wrap the engine module's bound `read_serialized_object` callable
with a thread-safe counting wrapper that delegates to the original frozen
reader.

Restore the original callable immediately afterward.

Required outcome:

- no worker exception;
- final state exactly `HOT_MAF`;
- serialized accounting charged once;
- reader call count exactly one;
- no duplicate ownership.

### V30 — concurrent_pin_unpin_accounting

From a stable resident state, concurrently acquire multiple valid pin leases.

All issued tokens must be unique.

Snapshot pin count must equal the exact number of active leases.

Then concurrently unpin each issued token exactly once.

Final active pin count must be zero.

No accounting corruption is permitted.

### V31 — concurrent_observation_no_provisional_state

Coordinate one mutating transition and concurrent snapshot/state
observations.

Every observed public residency state must be one of the valid fully
committed states.

No observer may see:

- a state/accounting combination impossible under the protocol;
- provisional dense accounting before `HOT_DENSE`;
- provisional serialized accounting before `HOT_MAF`.

### V32 — promotion_race_no_duplicate_ownership

Repeat same-object concurrent promotion sufficiently to validate the
coarse-lock ownership invariant across fresh runtime instances.

For every repetition:

- final state is `HOT_MAF`;
- one verified buffer charge exists;
- reader invocation count is exactly one per fresh object promotion;
- demotion returns serialized accounting to zero.

The repetition count must be frozen in the validation runner before
execution and printed in the raw result.

## 13. Counter validation

The validation runner must additionally inspect runtime counters while
performing the named checks.

Counter values must never be negative.

Where a named test deterministically implies a successful or failed action,
the corresponding counter must move in the expected direction.

Counter observations support the named checks; they are not extra named
checks beyond V01-V32.

## 14. Threading discipline

Concurrency tests must use Python threads against the frozen coarse-RLock V1
implementation.

A deterministic barrier or equivalent synchronized start must be used.

All worker exceptions must be captured and converted into validation
evidence.

No exception may disappear inside a worker thread.

Each concurrency test must have a bounded join timeout.

A thread still alive after the timeout fails the check.

## 15. Validation monkeypatch discipline

Monkeypatching is permitted only for the following two narrowly scoped
validation purposes:

1. V09 deterministic short-read error injection;
2. V29/V32 reader-call counting while delegating to the real frozen reader.

Only the engine module's already-bound `read_serialized_object` name may be
temporarily replaced.

The frozen Segment Reader source file must never be modified.

Every temporary replacement must be restored in a `finally` block.

The runner must verify restored callable identity after each patched test.

## 16. Corruption discipline

The clean isolated copied segment must never be modified in place.

Corruption tests must create a separate corruption copy inside the validation
runtime.

The corruption copy must:

- preserve exact total segment length;
- differ from the clean segment;
- change at least one byte inside the selected object range.

The frozen source runtime must never be modified.

## 17. Materializer callback discipline

The successful materializer must be deterministic.

The failing materializer must fail deterministically.

The concurrency validation does not require concurrent execution inside the
materializer because the V1 coarse runtime lock serializes public mutation.

No multithread scaling claim may be inferred.

## 18. Required result schema

The JSON result must use:

`schema = "openmind.maf_object_runtime_residency_validation.v1"`

It must include at least:

- `validation_valid`;
- `all_pass`;
- `fatal_error`;
- `phase_6c_validation`;
- frozen identity hashes;
- source fixture hashes;
- isolated runtime inventory;
- fixture identity summary;
- exact V01-V32 check map;
- failed check names;
- selected concurrency repetition counts;
- reader-count observations;
- accounting observations;
- source-runtime before/after hashes;
- validation-runtime inventory.

## 19. Scientific result semantics

`validation_valid = true` means the runner completed according to this
protocol and produced interpretable evidence.

`all_pass = true` means all V01-V32 checks passed.

The following is a valid negative scientific result:

`validation_valid = true`

`all_pass = false`

Such a result must be frozen and interpreted; it must not be rerun merely to
obtain a passing outcome.

A harness failure may produce:

`validation_valid = false`

with a non-null `fatal_error`.

That result is still immutable historical evidence once the exact-once slot
has been spent.

## 20. Exact-once rule

Validation V1 is exact-once.

Execution is forbidden until:

1. this protocol is committed;
2. the validation runner is constructed;
3. the validation runner is statically audited;
4. the validation runner is committed;
5. a final live preflight confirms exact identities;
6. result path is absent;
7. validation runtime path is absent;
8. staging is empty.

Once the runner is invoked, the V1 exact-once slot is permanently spent.

No V1 rerun is permitted.

If a defect is discovered after execution, correction requires a successor
validation version.

## 21. No cleanup after execution

The runner must not delete the validation runtime after success or failure.

The isolated runtime is retained as execution evidence.

The raw JSON result is retained as execution evidence.

## 22. No benchmark during validation

The validation runner must not:

- benchmark latency;
- compare mmap;
- compare persistent descriptors;
- compare eviction policies;
- claim cache advantage;
- claim concurrency scaling.

Correctness validation precedes performance work.

## 23. Backend neutrality

Validation V1 must not select or require:

- mmap;
- persistent descriptor caching;
- SQLite;
- LMDB;
- RocksDB;
- MAFDB;
- Vulkan residency;
- automatic eviction.

`MAPPED` remains the frozen backend-neutral attachment state.

## 24. Phase 6C acceptance boundary

Passing Validation V1 would establish only that the frozen runtime engine
satisfies the preregistered functional correctness checks under this fixture
and execution environment.

Passing Validation V1 would not by itself establish:

- resource-leak freedom under sustained workloads;
- performance advantage;
- cache-policy advantage;
- mmap advantage;
- production readiness;
- multithread scaling;
- Vulkan residency;
- MAF-native inference;
- conventional LLM runtime replacement.

Those require later diagnostics and/or benchmarks.

## 25. Post-validation order

If exact-once Validation V1 produces an interpretable result:

1. freeze the raw result before interpretation;
2. interpret V01-V32;
3. if accepted, construct prospective runtime diagnostics;
4. perform diagnostics before declaring the Phase 6C V1 runtime complete;
5. only then proceed to performance/backend experiments as separately
   preregistered work.

## 26. Immutability

This validation protocol becomes immutable when committed.

The frozen design protocol and runtime engine remain immutable validation
targets.

No source result may be edited to conform to expectations.

No failed check may be removed retrospectively.

No acceptance threshold may be added after execution.
