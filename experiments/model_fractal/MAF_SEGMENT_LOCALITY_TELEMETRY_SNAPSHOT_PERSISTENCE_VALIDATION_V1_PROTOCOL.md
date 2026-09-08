# MAF Segment Locality Telemetry Snapshot Persistence Validation V1 Protocol

Status: PROSPECTIVE PREREGISTRATION
Phase: 6D
Validation target: telemetry snapshot persistence V1
Scientific execution authorized by protocol freeze: NO
Exact-once slot: UNSPENT
Benchmark execution: FORBIDDEN
Performance verdict: NONE
Runtime integration: NOT AUTHORIZED
Phase 6E: NOT ENTERED

## 1. Purpose

This protocol prospectively defines scientific correctness validation for the
frozen Phase 6D telemetry snapshot persistence implementation.

The persistence implementation exists and is already frozen.

No Validation V1 runner exists at this protocol freeze.

No Validation V1 result exists at this protocol freeze.

Freezing this artifact authorizes implementation of the validation runner only.

It does not authorize scientific execution.

## 2. Frozen parent commit

Branch:

`labs/multidimensional-maf`

Parent commit:

`b960b89e19912860cf35d177eb2b6aa9e6c958c4`

## 3. Frozen persistence protocol

Path:

`experiments/model_fractal/MAF_SEGMENT_LOCALITY_TELEMETRY_SNAPSHOT_PERSISTENCE_V1_PROTOCOL.md`

SHA256:

`0e08a8a18a45a16eddc05927b8191d73ca9fc7453cb97fc1140e5e243e03db51`

The exact preregistered requirement set is P01 through P48.

## 4. Frozen persistence implementation

Path:

`experiments/model_fractal/maf_segment_locality_telemetry_snapshot_persistence_v1.py`

SHA256:

`4a7c8ba1e1d7e9e4004a16d54464f17fd07ba75cc84ddea25403697d53d0581c`

The implementation is immutable for Persistence Validation V1.

The runner may import and execute these exact bytes after its binding gate
passes.

The runner must never modify these bytes.

## 5. Frozen validated locality data model

Path:

`experiments/model_fractal/maf_segment_locality_data_model_v1.py`

SHA256:

`5432f2d74a610f2d0f9181e9af146013bb198a4e837af634993909358fff8ad0`

This module remains authoritative for TelemetrySnapshot scientific semantics.

## 6. Accepted upstream validation evidence

Accepted data-model raw result:

`experiments/model_fractal/maf_segment_locality_data_model_validation_v1.json`

SHA256:

`9aa2e467dc451b2d2122802e1e8b8fabf616db756a36b53a3600cca793923b4d`

Formal data-model verdict:

`experiments/model_fractal/MAF_SEGMENT_LOCALITY_DATA_MODEL_VALIDATION_V1_VERDICT.md`

SHA256:

`7754c9d5dada8dc214a21236827c64cafea880e4b0c679cd84c9c4833fd3e9db`

## 7. Frozen Phase 6C runtime

Path:

`experiments/model_fractal/maf_object_runtime_residency_v1.py`

SHA256:

`4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9`

Phase 6C remains closed and immutable.

Validation uses this path only for provenance and before/after SHA256 checks.

The persistence target must not import or integrate the Phase 6C runtime.

## 8. Persistent file schema

The exact persistence schema under test is:

`openmind.maf_segment_locality.telemetry_snapshot_file.v1`

## 9. Future validation runner

The future runner path is exactly:

`experiments/model_fractal/maf_segment_locality_telemetry_snapshot_persistence_validation_v1.py`

It does not exist when this protocol is frozen.

## 10. Raw validation result

The raw result path is exactly:

`experiments/model_fractal/maf_segment_locality_telemetry_snapshot_persistence_validation_v1.json`

It does not exist when this protocol is frozen.

## 11. Raw validation result schema

The exact result schema must be:

`openmind.maf_segment_locality.telemetry_snapshot_persistence_validation.v1`

## 12. Exact check set

Validation V1 contains exactly 48 ordered checks.

The check identifiers are exactly the preregistered persistence requirement
identifiers P01 through P48.

No check may be silently skipped, renamed, added after execution, or removed.

## 13. Exact-once rule

The first scientific invocation of the frozen Persistence Validation V1 runner
permanently spends the V1 slot regardless of whether the invocation:

- passes;
- returns a validation failure;
- encounters a harness defect;
- raises;
- crashes;
- is externally interrupted after invocation begins.

A spent V1 runner must never be edited and rerun as V1.

Any correction requires a prospectively preregistered successor validation
version.

## 14. Raw-result freeze rule

Whatever raw result or scientific failure residue is produced by the exact-once
invocation must be frozen before scientific interpretation.

No failed result may be deleted and replaced by a rerun.

## 15. Isolated filesystem root

All dynamic persistence tests must operate beneath one validation-specific
temporary root created by the runner.

The root must not be inside:

- the repository's tracked source tree;
- the existing historical results tree;
- any Phase 6C authority directory.

The runner may create synthetic test files only beneath this isolated root,
except for read-only SHA inspection of the frozen repository inputs.

## 16. Deterministic scientific fixtures

All semantic fixture values must be fixed in runner source before execution.

Synthetic identities must use deterministic valid model, generation, and object
PK strings.

No fixture may be chosen or modified after observing a test result.

The representative non-empty snapshot must include at least:

- two objects;
- at least one directed cross-object access transition;
- cache hit/miss evidence;
- one residency transition;
- one issued-and-consumed prefetch;
- one issued-and-unused prefetch;
- non-null first/last logical sequence values;
- non-zero event_count and access_event_count.

## 17. Empty snapshot fixture

The empty snapshot fixture must be created through the frozen validated data
model and must have:

- event_count = 0;
- access_event_count = 0;
- first_sequence = null;
- last_sequence = null;
- empty aggregate tuples.

## 18. Independent expectations

Where a validation target exposes a SHA, byte length, canonical byte sequence,
or payload mapping, the expected value must be calculated independently by the
runner rather than accepted from the target result object alone.

This requirement applies to:

- snapshot payload identity;
- snapshot SHA256;
- persistent envelope;
- persistent bytes;
- persistent file SHA256;
- byte length.

## 19. Corruption fixtures

Corruption cases must be produced as independent candidate files.

The accepted source snapshot and the frozen implementation must not be modified.

Each negative case must have its own isolated path so failure residue from one
case cannot alter another.

## 20. Canonical JSON corruption discipline

Cases testing malformed or semantically altered envelopes must distinguish:

- invalid UTF-8;
- invalid JSON;
- valid but noncanonical JSON;
- canonical JSON with invalid schema/content.

A failure in one category cannot substitute for testing another category.

## 21. Existing-final sentinel

P33 and the second-publication portion of P42 must use deterministic sentinel or
already-published final bytes and verify SHA256 identity before and after the
rejected write.

## 22. Existing-partial sentinel

P34 and P35 must use deterministic partial sentinel bytes and verify SHA256
identity before and after the rejected write.

## 23. Race fixture

P38 must create the final-path race after the candidate partial file exists and
before final hard-link publication.

The validation runner may use a validation-only child process or controlled
filesystem interposition to synchronize that race.

The frozen persistence implementation itself must not be monkey-patched,
rewritten, or replaced.

A race case that does not prove the competing final path existed before the
target publication attempt is invalid.

## 24. Failure-residue observation

For P41, failure residue must be observed and hashed before the runner removes
anything from the isolated temporary validation root.

Temporary validation-root cleanup after all evidence has been recorded does not
count as hidden scientific failure cleanup.

Repository failure artifacts remain subject to the usual freeze-before-
interpretation rule.

## 25. Symlink capability

P31 must actually exercise a symbolic link if the host filesystem supports
creating one.

If the environment does not support symlink creation, Validation V1 must be
marked invalid by the harness rather than treating P31 as passed without a test.

## 26. Durability claim boundary

Calls to fsync and their ordering are correctness properties under test.

Validation V1 does not claim proof against physical storage-device failure or
power loss.

No hardware durability superiority claim is authorized.

## 27. Hard-link claim boundary

Validation must establish use and observed no-replace behavior of the frozen V1
hard-link publication strategy.

It does not establish that every possible filesystem provides identical
hard-link durability semantics.

## 28. Static plus dynamic checks

Some requirements inherently contain both static and dynamic evidence.

Static AST/source inspection is permitted for:

- exact import boundary;
- partial exclusive-create flags;
- write-loop surface;
- hard-link publication primitive;
- absence of replace/rename publication;
- parent-directory fsync ordering;
- absence of update/overwrite APIs;
- absence of Phase 6C integration;
- absence of repack/benchmark surfaces.

Dynamic behavior must still be exercised wherever the requirement specifies a
runtime filesystem outcome.

## 29. No benchmark

Persistence Validation V1 is correctness validation only.

The runner must not measure or report:

- latency;
- throughput;
- IOPS;
- fsync duration;
- storage speedup;
- write amplification;
- flash wear;
- model inference speed.

The raw result must contain:

`benchmark_executed = false`

and:

`performance_verdict = null`

## 30. No Phase 6C runtime integration

The validation runner must not instantiate or execute Phase 6C runtime behavior.

It may only SHA256 the frozen Phase 6C source file for P01 and P46.

## 31. No repack realization

Validation V1 must not:

- build production MAF segments;
- construct a new model generation;
- activate or roll back a generation;
- execute a repack planner;
- alter active-generation authority.

## 32. No Phase 6E

Validation V1 must not perform selective tensor access, partial inference,
hidden-state shadow comparison, logit comparison, or token comparison.

Phase 6E remains unentered.

## 33. No network

The validation runner must require no network access and no external download.

All fixtures are synthetic and local.

## 34. Validation validity

A scientifically valid successful result requires all of the following:

- result schema exactly `openmind.maf_segment_locality.telemetry_snapshot_persistence_validation.v1`;
- validation_valid = true;
- all_pass = true;
- check_count = 48;
- exact ordered checks P01 through P48;
- every individual check pass = true;
- failed_checks = [];
- fatal_error = null;
- benchmark_executed = false;
- performance_verdict = null;
- exact persistence implementation SHA256 binding;
- exact persistence protocol SHA256 binding;
- exact data-model SHA256 binding;
- exact Phase 6C SHA256 binding.

## 35. Harness failure

If the frozen runner cannot validly execute the complete preregistered matrix,
the raw result must report:

- validation_valid = false;
- all_pass = false;
- non-null fatal_error.

A harness failure is not a persistence correctness verdict.

The exact-once V1 slot is still spent.

## 36. Mandatory result fields

The raw result must contain at minimum:

- `schema`;
- `validation_valid`;
- `all_pass`;
- `checks`;
- `failed_checks`;
- `fatal_error`;
- `benchmark_executed`;
- `performance_verdict`;
- `implementation_path`;
- `implementation_sha256`;
- `protocol_path`;
- `protocol_sha256`;
- `data_model_sha256`;
- `phase6c_engine_sha256`;
- `check_count`.

## 37. Scientific validation matrix

### P01_frozen_provenance_binding

Before importing the persistence target, independently SHA256 the persistence implementation, persistence protocol, validated locality data model, accepted data-model result, formal data-model verdict, and frozen Phase 6C runtime. Every identity must equal its preregistered constant. Any mismatch invalidates the validation harness before functional checks begin.

### P02_import_time_side_effect_absence

Import the frozen persistence implementation in an isolated child Python process whose current working directory is a preregistered empty observation directory. Compare the recursive directory inventory before and after import. The inventory must remain exactly empty.

### P03_exact_file_schema

Assert the exported SNAPSHOT_FILE_SCHEMA value equals exactly `openmind.maf_segment_locality.telemetry_snapshot_file.v1`.

### P04_exact_envelope_key_set

Serialize a valid synthetic snapshot and require the returned envelope mapping to have exactly the keys `schema`, `snapshot_sha256`, and `snapshot`, with no fourth key and no omission.

### P05_snapshot_member_exact_payload

For the representative non-empty fixture, compare the envelope `snapshot` member directly against the frozen data-model `snapshot_payload(snapshot)` result using structural equality.

### P06_snapshot_sha_exact

For the same fixture, compare envelope `snapshot_sha256` directly against the frozen data-model `snapshot_sha256(snapshot)` result.

### P07_canonical_file_bytes

Compare `snapshot_file_bytes(snapshot)` against an independently computed canonical JSON encoding of `snapshot_file_payload(snapshot)` using the frozen sort-keys, compact-separator, ensure_ascii=False, UTF-8 rules.

### P08_no_trailing_newline

Require canonical persistent bytes to be non-empty and not end in newline, carriage return, whitespace padding, or bytes outside the independently computed canonical JSON document.

### P09_deterministic_file_sha

Compare `snapshot_file_sha256(snapshot)` against an independent hashlib SHA256 over the exact canonical file bytes.

### P10_empty_snapshot_round_trip

Construct a valid empty TelemetrySnapshot through the validated data-model surface, publish it to an isolated temporary directory, read it through the persistence reader, and require exact snapshot payload/SHA identity.

### P11_nonempty_snapshot_round_trip

Construct one deterministic representative snapshot containing object, directed transition, cache, residency-transition, and prefetch aggregates. Publish and read it back and require exact reconstructed payload identity.

### P12_source_identity_preservation

On the non-empty fixture, verify model_pk, source_generation_pk, and source_manifest_sha256 are identical before persistence and after validated read-back.

### P13_sequence_identity_preservation

Verify first_sequence, last_sequence, event_count, and access_event_count survive the non-empty round trip exactly.

### P14_aggregate_order_preservation

Use deliberately lexically nontrivial object/cache/residency identities whose validated snapshot has deterministic aggregate tuple order. Require all reconstructed aggregate tuples to preserve that exact frozen order.

### P15_strict_utf8_decode

Create a standalone corrupt candidate containing invalid UTF-8 bytes and require read_snapshot_file to raise the persistence read-error family.

### P16_invalid_json_rejection

Create a regular file containing malformed UTF-8-valid JSON and require the persistence reader to reject it.

### P17_noncanonical_json_rejection

Take a semantically valid persistence envelope and write an alternate JSON representation containing whitespace or alternate key formatting. Require rejection because original bytes differ from canonical bytes.

### P18_unknown_envelope_key_rejection

Create a canonical envelope with one additional top-level key while preserving the other members. Require strict read rejection.

### P19_missing_envelope_key_rejection

For each required top-level envelope key in turn, construct a canonical envelope omitting that key and require rejection.

### P20_wrong_schema_rejection

Construct a canonical otherwise-valid envelope whose schema differs from the exact V1 file schema and require rejection.

### P21_snapshot_sha_syntax_rejection

Construct canonical envelopes with representative malformed declared snapshot SHAs, including uppercase hexadecimal, short length, long length, and non-hexadecimal characters. All must be rejected.

### P22_snapshot_sha_mismatch_rejection

Construct a canonical envelope containing an otherwise valid snapshot but replace the declared snapshot SHA with a different well-formed lowercase 64-hex value. Require rejection.

### P23_payload_mutation_detection

Starting from a valid envelope, mutate one identity-relevant snapshot payload value while retaining the original declared snapshot SHA and require rejection.

### P24_malformed_nested_payload_rejection

Construct canonical candidates where representative object, transition, cache, residency, and prefetch aggregate members have malformed JSON container/value structures. Each malformed case must be rejected.

### P25_unknown_nested_field_rejection

For the snapshot mapping and each aggregate class represented in the fixture, inject one unknown nested field while preserving canonical JSON. Require strict rejection rather than ignored-field reconstruction.

### P26_invalid_integer_semantics_rejection

Construct canonical snapshot payload variants placing boolean or negative values into representative frozen plain-nonnegative-integer fields and require rejection.

### P27_invalid_pk_rejection

Construct canonical variants containing malformed model PK, generation PK, and object PK values. Require rejection through frozen data-model validation semantics.

### P28_invalid_aggregate_invariant_rejection

Construct a canonical prefetch aggregate where consumed_count plus unused_count exceeds issued_count, plus at least one other frozen aggregate invariant violation if exposed by the data model. Require rejection.

### P29_missing_file_rejection

Call the reader on a preregistered absent final path inside the isolated validation root and require a persistence read error.

### P30_nonregular_file_rejection

Call the reader on a directory at the expected final path and require a persistence read error. No directory contents may be changed.

### P31_symlink_rejection

Where symbolic links are supported by the validation filesystem, create a symlink final path pointing to a valid snapshot file and require rejection without following it as authority. If symlink creation itself is unsupported, the harness must report the check invalid rather than pass untested.

### P32_parent_directory_required

Attempt publication beneath a parent directory that does not exist. Require write failure and verify that neither the parent hierarchy nor final/partial paths were created.

### P33_existing_final_refusal

Pre-create the final path with deterministic sentinel bytes, attempt publication, require failure, and verify the sentinel final file remains byte-identical.

### P34_existing_partial_refusal

Pre-create the exact sibling `.partial` path with deterministic sentinel bytes, attempt publication, require failure, and verify the partial sentinel is unchanged and no final path appears.

### P35_partial_exclusive_creation

Statically bind the implementation to O_CREAT|O_EXCL partial creation and dynamically verify the pre-existing-partial case cannot truncate or replace the sentinel residue.

### P36_complete_partial_write

For successful publication, independently compute expected canonical bytes and verify the final file equals them byte-for-byte and has the exact expected length. The runner must also statically confirm the frozen write loop and file fsync surface; no monkey-patching of the frozen implementation is allowed.

### P37_atomic_no_replace_publication

Statically verify the frozen writer's final publication primitive is `os.link(partial, final, follow_symlinks=False)` and that neither `os.replace` nor rename is used for final publication. Dynamic successful publication must produce the expected final file.

### P38_final_no_replace_race_safety

Use a validation-only subprocess/interposition fixture that pauses after the partial is durably created but before the hard-link publication, then create the final path from the controlling process. Resume publication; the writer must fail and the competing final sentinel must remain unchanged. The frozen implementation itself may not be edited.

### P39_parent_directory_fsync

Statically verify the frozen successful publication sequence contains the first parent-directory fsync after hard-link publication and before partial unlink. Dynamic validation does not claim hardware durability.

### P40_success_partial_removal

After a successful publication, require final present, `.partial` absent, and statically verify the second parent-directory fsync follows partial unlink.

### P41_failure_residue_preservation

Exercise at least the no-replace publication failure from P38 and require the `.partial` residue to remain present and byte-identical to the expected canonical snapshot bytes. No cleanup by the runner is permitted until the raw case evidence has been observed and recorded.

### P42_no_read_modify_write

Statically verify the frozen public API has no update/overwrite/append/repair function and dynamically confirm attempting a second publication to the same final path fails without modifying the original file.

### P43_serialization_determinism

Construct two independently created semantically equivalent non-empty snapshots. Require equal snapshot payloads, snapshot SHAs, persistence envelopes, file bytes, and file SHAs.

### P44_validated_read_result

On successful read-back, require the returned object to be the frozen/slotted TelemetrySnapshotReadResult and verify reconstructed snapshot, snapshot SHA, file SHA, and byte length against independent expectations.

### P45_write_result

On successful publication, require the returned object to be the frozen/slotted TelemetrySnapshotWriteResult and verify final path, snapshot SHA, file SHA, and byte length against independent expectations.

### P46_phase6c_immutability

Hash the frozen Phase 6C runtime immediately before the validation test body and immediately after all checks. Both must equal the preregistered Phase 6C SHA256.

### P47_no_runtime_integration

Statically parse the frozen persistence module and verify it does not import the Phase 6C runtime and exposes no runtime promotion, demotion, pinning, budget, or telemetry-observer integration surface.

### P48_no_repack_planner_or_performance_claim

Statically verify the frozen persistence module contains no generation builder/activation/repack-planner execution surface and no benchmark/timing API. The raw result must set benchmark_executed=false and performance_verdict=null.

## 38. Exact ordered check names

01. `P01_frozen_provenance_binding`
02. `P02_import_time_side_effect_absence`
03. `P03_exact_file_schema`
04. `P04_exact_envelope_key_set`
05. `P05_snapshot_member_exact_payload`
06. `P06_snapshot_sha_exact`
07. `P07_canonical_file_bytes`
08. `P08_no_trailing_newline`
09. `P09_deterministic_file_sha`
10. `P10_empty_snapshot_round_trip`
11. `P11_nonempty_snapshot_round_trip`
12. `P12_source_identity_preservation`
13. `P13_sequence_identity_preservation`
14. `P14_aggregate_order_preservation`
15. `P15_strict_utf8_decode`
16. `P16_invalid_json_rejection`
17. `P17_noncanonical_json_rejection`
18. `P18_unknown_envelope_key_rejection`
19. `P19_missing_envelope_key_rejection`
20. `P20_wrong_schema_rejection`
21. `P21_snapshot_sha_syntax_rejection`
22. `P22_snapshot_sha_mismatch_rejection`
23. `P23_payload_mutation_detection`
24. `P24_malformed_nested_payload_rejection`
25. `P25_unknown_nested_field_rejection`
26. `P26_invalid_integer_semantics_rejection`
27. `P27_invalid_pk_rejection`
28. `P28_invalid_aggregate_invariant_rejection`
29. `P29_missing_file_rejection`
30. `P30_nonregular_file_rejection`
31. `P31_symlink_rejection`
32. `P32_parent_directory_required`
33. `P33_existing_final_refusal`
34. `P34_existing_partial_refusal`
35. `P35_partial_exclusive_creation`
36. `P36_complete_partial_write`
37. `P37_atomic_no_replace_publication`
38. `P38_final_no_replace_race_safety`
39. `P39_parent_directory_fsync`
40. `P40_success_partial_removal`
41. `P41_failure_residue_preservation`
42. `P42_no_read_modify_write`
43. `P43_serialization_determinism`
44. `P44_validated_read_result`
45. `P45_write_result`
46. `P46_phase6c_immutability`
47. `P47_no_runtime_integration`
48. `P48_no_repack_planner_or_performance_claim`

## 39. Acceptance boundary

A complete P01-P48 PASS establishes only correctness properties directly tested
for the frozen standalone telemetry snapshot persistence implementation.

It does not establish:

- production runtime telemetry collection;
- snapshot flush cadence correctness;
- long-running telemetry durability;
- repack planner quality;
- transition-locality improvement;
- physical generation realization;
- locality-experiment success;
- performance superiority;
- device wear characteristics;
- Phase 6E selective access;
- MAF-native inference.

## 40. Runner implementation authorization

Freezing this validation protocol authorizes creation of the Persistence
Validation V1 runner only.

The runner must subsequently receive:

1. static audit without execution;
2. local Git freeze;
3. final scoped no-write preflight.

Only after those gates pass may Validation V1 be invoked exactly once.

## 41. Repository residue policy

The previously classified historical untracked repository residue is preserved.

Global zero-untracked cleanliness is not required.

Before scientific execution, the final preflight must prove that:

- the tracked worktree is clean;
- staging is empty;
- the frozen scientific inputs have exact SHAs;
- the exact validation result and temporary result paths are absent;
- no untracked path collides with the Persistence Validation V1 namespace;
- the preserved historical untracked baseline has not unexpectedly changed,
  except for separately audited scientific residue.

## 42. Authorization boundary

PERSISTENCE IMPLEMENTATION: FROZEN / NOT YET SCIENTIFICALLY VALIDATED.

PERSISTENCE VALIDATION PROTOCOL: PREREGISTERED BY THIS ARTIFACT.

PERSISTENCE VALIDATION RUNNER: AUTHORIZED AFTER THIS PROTOCOL FREEZE.

PERSISTENCE VALIDATION EXECUTION: NOT AUTHORIZED BY THIS PROTOCOL FREEZE ALONE.

EXACT-ONCE SLOT: UNSPENT.

PHASE 6C EDIT: FORBIDDEN.

PHASE 6C REOPEN: FORBIDDEN.

RUNTIME INTEGRATION: NOT AUTHORIZED.

TELEMETRY COLLECTION FROM PHASE 6C: NOT AUTHORIZED.

REPACK PLANNER: NOT AUTHORIZED.

REPACK REALIZATION: NOT AUTHORIZED.

LOCALITY EXPERIMENT: NOT AUTHORIZED.

DEVICE BENCHMARK: NOT AUTHORIZED.

PHASE 6E: NOT ENTERED.

PERFORMANCE VERDICT: NONE.

PUSH: NOT AUTHORIZED BY THIS PROTOCOL.
