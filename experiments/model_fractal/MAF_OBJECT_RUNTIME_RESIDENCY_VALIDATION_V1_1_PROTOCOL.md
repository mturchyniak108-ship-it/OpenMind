# OpenMind MAF Object Runtime and Residency Validation V1.1 Protocol

Status: **PREREGISTERED / UNEXECUTED / EXACT-ONCE / V1 HARNESS SUCCESSOR**

Schema:

`openmind.maf_object_runtime_residency_validation.v1.1`

## 1. Purpose

Validation V1.1 is a prospective successor to the spent Validation V1
exact-once experiment.

V1.1 exists solely because Validation V1 terminated in the validation harness
before V01 began.

V1.1 does not modify the frozen Phase 6C runtime engine.

V1.1 does not reinterpret the V1 failure as an engine failure.

## 2. Frozen Phase 6C target

Design protocol:

`experiments/model_fractal/MAF_OBJECT_RUNTIME_RESIDENCY_V1_PROTOCOL.md`

SHA256:

`81987d00ef4cb51556dcebf08bff9c9fa8979f033df05304d347b759e545eb13`

Runtime engine:

`experiments/model_fractal/maf_object_runtime_residency_v1.py`

SHA256:

`4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9`

The runtime engine under V1.1 is byte-identical to the runtime engine targeted
by Validation V1.

## 3. Frozen Validation V1 history

V1 protocol:

`experiments/model_fractal/MAF_OBJECT_RUNTIME_RESIDENCY_VALIDATION_V1_PROTOCOL.md`

SHA256:

`251f74723ad101b5b6e12e1eefbbad587338495e34cdb59c8155e8333636133d`

V1 runner:

`experiments/model_fractal/maf_object_runtime_residency_validation_v1.py`

SHA256:

`d6160b2bb6537b20a894b11eefad369995f53d4025e4fe044a10e2b24c403e78`

V1 raw result:

`experiments/model_fractal/maf_object_runtime_residency_validation_v1.json`

SHA256:

`b837625058cb65ce49695abc2f8869b4bf89bba657573a13bc12580fd83acdc1`

V1 result semantics:

- `validation_valid = false`;
- `all_pass = false`;
- zero V01-V32 checks executed;
- fatal error type `AttributeError`;
- fatal message `'tuple' object has no attribute 'length'`.

Validation V1 exact-once slot is permanently spent.

Validation V1 must never be rerun.

Validation V1 runner and result must never be edited.

The retained V1 runtime residue must not be deleted or altered.

## 4. Proven V1 harness root cause

Frozen Resident PK Directory:

`experiments/model_fractal/maf_resident_pk_directory_v1.py`

SHA256:

`4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6`

`ResidentPKSnapshot.entries` is declared as:

`Mapping[tuple[str, str, str], ResidentPKEntry]`

Validation V1 incorrectly used the semantic equivalent of:

`for entry in snapshot.entries`

Iterating a Mapping yields keys.

The yielded object was therefore a tuple key, not a `ResidentPKEntry`.

V1 then accessed:

`entry.length`

which caused:

`AttributeError: 'tuple' object has no attribute 'length'`

This occurred before V01.

Therefore Validation V1 produced no correctness verdict on the frozen runtime
engine.

## 5. Single authorized V1.1 harness correction

The only authorized semantic correction from the V1 harness is:

V1:

`for entry in snapshot.entries`

V1.1:

`for entry in snapshot.entries.values()`

The resulting values must be `ResidentPKEntry` objects.

The existing deterministic sort by:

- `entry.length`;
- `entry.object_pk`;

must remain.

The existing positive-length filter:

`entry.length > 0`

must remain.

The existing isolated copied-segment rebinding via immutable dataclass
replacement must remain.

No other V01-V32 validation semantics may be weakened, removed, or changed to
make the runtime pass.

## 6. Frozen predecessor APIs

Resident PK Directory SHA256:

`4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6`

Segment Reader SHA256:

`3499cb8e528fe8e9315e3e5656d6aa888c95ca175310b6371e722de409827369`

V1.1 must use the same frozen predecessor implementations as V1.

No predecessor source modification is authorized.

## 7. Source fixture

V1.1 uses the same immutable source fixture as V1:

`results/runtime/maf_resident_pk_directory_benchmark_v1_1`

Required files and identities:

- `active_generation.json`
  - size: `380`
  - SHA256: `031d1a50a3cf53f158057a02bb6c68001edfb07bf48bf893afc9bc8f095458e9`
- `candidate_a.manifest.json`
  - size: `1202`
  - SHA256: `941301aa362d3f949389e5364b1be4d7f26b96f0d45efa81346c82fce3260f93`
- `segment_00000000.mafseg`
  - size: `4096`
  - SHA256: `f965b526538d757ca2d6114af6517c57cbcb3650b71d8cfb92046a04ef2f566b`

Source fixture mutation is forbidden.

## 8. V1.1 isolated runtime

V1.1 runtime path:

`results/runtime/maf_object_runtime_residency_validation_v1_1`

It must not exist before exact-once execution.

The V1.1 runner may create it exactly once during authorized execution.

It must be retained after execution whether V1.1 passes or fails.

The V1 runtime path is separate historical evidence and must remain untouched.

## 9. V1.1 result

Authorized raw result path:

`experiments/model_fractal/maf_object_runtime_residency_validation_v1_1.json`

It must not exist before exact-once execution.

It must never overwrite the V1 result.

Once produced, the V1.1 result is immutable exact-once evidence.

## 10. Validation matrix

V1.1 retains exactly the same 32 named validation checks as V1:

- `V01_runtime_binding`
- `V02_initial_cold_disk`
- `V03_legal_upward_primitive_transitions`
- `V04_legal_downward_primitive_transitions`
- `V05_illegal_skipped_transitions`
- `V06_same_state_idempotence`
- `V07_verified_hot_maf_promotion`
- `V08_corruption_hash_failure_nonpublication`
- `V09_short_read_nonpublication`
- `V10_stale_generation_rejection`
- `V11_serialized_byte_accounting`
- `V12_dense_byte_accounting`
- `V13_zero_budget_rejection`
- `V14_over_budget_failure_atomicity`
- `V15_multiple_pin_floor_composition`
- `V16_pinned_demotion_rejected`
- `V17_unknown_pin_rejection`
- `V18_consumed_pin_rejection`
- `V19_unpin_no_automatic_demotion`
- `V20_dense_materialization_success`
- `V21_dense_materialization_failure_atomicity`
- `V22_dense_view_lifetime_invalidation`
- `V23_runtime_close_cleanup`
- `V24_close_idempotence`
- `V25_operation_rejection_after_close`
- `V26_source_file_immutability`
- `V27_no_unverified_byte_escape`
- `V28_snapshot_accounting_consistency`
- `V29_concurrent_same_object_promotion`
- `V30_concurrent_pin_unpin_accounting`
- `V31_concurrent_observation_no_provisional_state`
- `V32_promotion_race_no_duplicate_ownership`

No check may be removed.

No check may be renamed.

No acceptance threshold may be weakened.

## 11. Failure atomicity

The V1.1 runner retains the corrected V1 runner rule that expected failed
operations compare committed residency/resource/pin/identity state without
requiring diagnostic counters to remain unchanged.

Counters may legitimately record failed transitions, verification failures, or
budget rejections.

## 12. Verified-read injection

V09 retains the narrow deterministic short-read injection from V1.

Only the engine module's bound `read_serialized_object` callable may be
temporarily replaced.

It must be restored in `finally`.

The frozen Segment Reader source is never modified.

## 13. Concurrency parameters

V1.1 retains the exact V1 concurrency parameters:

`PROMOTION_RACE_REPETITIONS = 16`

`PIN_THREAD_COUNT = 8`

`JOIN_TIMEOUT_SECONDS = 10.0`

No performance or scaling claim may be made from these correctness checks.

## 14. Corruption fixture discipline

V1.1 retains the V1 rule that the clean copied segment is not corrupted in
place.

A separate isolated corruption copy is created inside the V1.1 runtime.

Exactly one bit inside the selected object range is flipped.

Total segment length must remain unchanged.

## 15. Dense materializer discipline

V1.1 retains the same deterministic successful materializer and deterministic
failing materializer semantics as V1.

Dense views remain derived and non-authoritative.

Persistent MAF bytes remain authoritative.

## 16. Result semantics

V1.1 result schema:

`openmind.maf_object_runtime_residency_validation.v1.1`

`validation_valid = true` means the V1.1 harness completed and produced
interpretable V01-V32 evidence.

`all_pass = true` means all V01-V32 checks passed.

The following remains a valid scientific negative result:

`validation_valid = true`

`all_pass = false`

A harness failure remains:

`validation_valid = false`

with a non-null fatal error.

Any produced result must be frozen before interpretation.

## 17. Exact-once rule

Validation V1.1 is exact-once.

Execution is forbidden until:

1. this V1.1 protocol is frozen;
2. the V1.1 runner is constructed;
3. static audit proves the only intended V1 fixture-extraction semantic change;
4. the V1.1 runner is frozen;
5. final live preflight passes;
6. V1.1 result path is absent;
7. V1.1 runtime path is absent;
8. V1 historical artifacts remain exact;
9. staging is empty.

Once the V1.1 runner is invoked, the V1.1 exact-once slot is permanently
spent.

V1.1 must never be rerun.

Any post-execution defect requires another successor version.

## 18. Runner derivation discipline

The V1.1 runner should be derived from the frozen V1 runner.

Static audit must prove:

- V1 runner remains unchanged;
- V1.1 uses `snapshot.entries.values()`;
- V1.1 does not iterate `snapshot.entries` directly as entries;
- V01-V32 names are unchanged;
- concurrency constants are unchanged;
- source fixture identities are unchanged;
- frozen engine/predecessor hashes are unchanged;
- V1.1 schema/result/runtime paths are versioned separately;
- no benchmark code is added;
- no cleanup of V1 or V1.1 evidence is added.

## 19. Backend neutrality

V1.1 selects no runtime backend.

It does not select or require:

- mmap;
- persistent descriptor cache;
- SQLite;
- LMDB;
- RocksDB;
- custom MAFDB;
- automatic eviction;
- Vulkan residency.

## 20. Nonclaims

Even an all-pass V1.1 result would not by itself establish:

- performance advantage;
- leak freedom under sustained operation;
- production readiness;
- automatic cache-policy quality;
- multithread scaling;
- Vulkan residency;
- MAF-native inference;
- standard LLM runtime replacement.

## 21. Post-V1.1 ordering

After exact-once V1.1 execution:

1. freeze the raw V1.1 result;
2. interpret V01-V32;
3. if the result is accepted, construct prospective Phase 6C runtime
   diagnostics;
4. complete diagnostics before Phase 6C V1 completion;
5. benchmark/backend work remains separately preregistered future work.

## 22. Immutability

This V1.1 protocol becomes immutable when committed.

Validation V1 remains immutable historical evidence.

The Phase 6C engine remains immutable.

No failed result may be rewritten.

No check may be retrospectively removed or weakened.
