# MAF Segment Locality Telemetry Snapshot Persistence V1 Protocol

Status: PROSPECTIVE PREREGISTRATION
Phase: 6D
Subsystem: telemetry snapshot persistence
Scientific result: NONE
Performance verdict: NONE
Runtime integration: NOT AUTHORIZED
Repack realization: NOT AUTHORIZED
Phase 6E: NOT ENTERED

## 1. Purpose

Phase 6D requires runtime telemetry to be aggregated in RAM and periodically
persisted as a frozen, deterministic, independently verifiable snapshot.

The RAM aggregation and snapshot data model has already passed its
prospectively preregistered V01-V50 validation.

This protocol defines the first persistent representation of that validated
TelemetrySnapshot.

This protocol does not authorize collection of telemetry from the Phase 6C
runtime.

It does not authorize a repack planner.

It does not authorize generation realization.

It does not authorize benchmarking.

## 2. Frozen parent commit

Branch:

`labs/multidimensional-maf`

Parent commit:

`8826175a9dd67774ca20e94f8efc2632570e0efd`

## 3. Parent Phase 6D protocol

Path:

`experiments/model_fractal/MAF_SEGMENT_LOCALITY_REPACKING_V1_PROTOCOL.md`

SHA256:

`a4c1a1d4fe22f7e714efa331cec9cf4dbd3a9e178f2b28b3ddb9034387e210ae`

## 4. Validated locality data-model protocol

Path:

`experiments/model_fractal/MAF_SEGMENT_LOCALITY_DATA_MODEL_V1_PROTOCOL.md`

SHA256:

`712caa2e7dfc948f607a4c8d68064fc838eb1f58701fc5206c52aaf8e6492bc4`

## 5. Validated locality data-model implementation

Path:

`experiments/model_fractal/maf_segment_locality_data_model_v1.py`

SHA256:

`5432f2d74a610f2d0f9181e9af146013bb198a4e837af634993909358fff8ad0`

The persistence implementation must use this frozen data model as the
authoritative definition of TelemetrySnapshot, snapshot_payload, and
snapshot_sha256.

It must not fork or redefine those scientific semantics.

## 6. Accepted data-model validation evidence

Validation protocol:

`experiments/model_fractal/MAF_SEGMENT_LOCALITY_DATA_MODEL_VALIDATION_V1_PROTOCOL.md`

SHA256:

`954e71a523694b2913c35d328efdc59f7c95413c1746e7c50c087045da4291d8`

Accepted result:

`experiments/model_fractal/maf_segment_locality_data_model_validation_v1.json`

SHA256:

`9aa2e467dc451b2d2122802e1e8b8fabf616db756a36b53a3600cca793923b4d`

Formal verdict:

`experiments/model_fractal/MAF_SEGMENT_LOCALITY_DATA_MODEL_VALIDATION_V1_VERDICT.md`

SHA256:

`7754c9d5dada8dc214a21236827c64cafea880e4b0c679cd84c9c4833fd3e9db`

The accepted result established validation_valid=true, all_pass=true,
check_count=50, benchmark_executed=false, and performance_verdict=null.

Validation V1 is spent and must never be rerun.

## 7. Frozen Phase 6C provenance

Path:

`experiments/model_fractal/maf_object_runtime_residency_v1.py`

SHA256:

`4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9`

Phase 6C is closed and immutable.

The persistence implementation must not import or execute the Phase 6C
runtime.

This binding is provenance only.

## 8. Future implementation path

The authorized future implementation path is exactly:

`experiments/model_fractal/maf_segment_locality_telemetry_snapshot_persistence_v1.py`

The implementation does not exist when this protocol is frozen.

## 9. Future validation artifacts

Validation protocol:

`experiments/model_fractal/MAF_SEGMENT_LOCALITY_TELEMETRY_SNAPSHOT_PERSISTENCE_VALIDATION_V1_PROTOCOL.md`

Validation runner:

`experiments/model_fractal/maf_segment_locality_telemetry_snapshot_persistence_validation_v1.py`

Raw validation result:

`experiments/model_fractal/maf_segment_locality_telemetry_snapshot_persistence_validation_v1.json`

None may exist at this protocol freeze.

## 10. Persistent envelope schema

The exact V1 persistent schema is:

`openmind.maf_segment_locality.telemetry_snapshot_file.v1`

A persistent telemetry snapshot file contains exactly three top-level members:

1. `schema`
2. `snapshot_sha256`
3. `snapshot`

No fourth member is permitted.

No required member may be omitted.

## 11. Snapshot member

`snapshot` is exactly the JSON-compatible mapping produced by:

`snapshot_payload(snapshot)`

from the frozen locality data-model implementation.

The persistence layer must not add storage-only fields inside the snapshot
payload.

The persistence layer must not rename data-model fields.

The persistence layer must not reorder scientific tuple semantics.

## 12. Snapshot identity

`snapshot_sha256` is exactly:

`snapshot_sha256(snapshot)`

from the frozen data model.

The SHA is computed from the canonical snapshot payload, not from the
persistent envelope.

The snapshot SHA therefore remains stable independent of the storage wrapper.

## 13. Persistent file identity

The complete envelope is encoded with the same canonical JSON rules used by
the frozen data model:

- json.dumps;
- sort_keys=True;
- separators=(",", ":");
- ensure_ascii=False;
- UTF-8 encoding;
- no trailing newline;
- no extra bytes.

The SHA256 of those complete bytes is the persistent file identity.

Snapshot SHA256 and persistent-file SHA256 are distinct identities and must
never be conflated.

## 14. Canonical read rule

A reader must parse the file and then independently re-encode the parsed
envelope canonically.

The re-encoded bytes must equal the original file bytes exactly.

This rejects whitespace variants, alternate key ordering, trailing newlines,
and other noncanonical representations even if ordinary JSON parsing would
accept them.

## 15. Strict reconstruction

The reader must reconstruct the frozen TelemetrySnapshot and nested frozen
aggregate value objects.

Reconstruction must use the exact field surface and validators of the frozen
data model.

Unknown fields are rejected.

Missing fields are rejected.

Invalid plain-integer semantics are rejected.

Malformed PKs are rejected.

Invalid aggregate invariants are rejected.

## 16. Reconstruction identity check

After reconstruction:

1. `snapshot_payload(reconstructed_snapshot)` must equal the stored `snapshot`
   mapping exactly.
2. `snapshot_sha256(reconstructed_snapshot)` must equal stored
   `snapshot_sha256`.

A mismatch is corruption or noncanonical state and must be rejected.

## 17. Reader filesystem authority

The final path must exist as a regular filesystem file.

Symbolic links are not accepted as snapshot authority.

Directories and non-regular objects are rejected.

The reader performs no repair.

The reader performs no fallback to `.partial`.

## 18. Writer preconditions

Before creating bytes on disk:

- the TelemetrySnapshot must already be valid;
- the full canonical envelope bytes must already be derived in memory;
- the final parent directory must already exist;
- the final path must not exist;
- the exact sibling partial path must not exist.

The persistence layer does not create parent directories.

## 19. Exact partial path

For final path:

`<name>`

the only V1 publication residue path is:

`<name>.partial`

in the same directory.

Same-directory placement is mandatory because V1 atomic publication assumes
one filesystem.

## 20. Partial exclusive creation

The `.partial` file must be created with exclusive-create semantics.

A pre-existing `.partial` path is an error.

It must not be truncated.

It must not be silently replaced.

## 21. Complete partial write

The complete canonical byte sequence must be written.

Short writes must be handled until complete or treated as failure.

The partial file must be fsynced before publication.

Closing an un-fsynced partial file is not sufficient for successful
publication.

## 22. Atomic no-replace publication

After the partial file is fully written and fsynced, publication uses an
atomic same-directory hard-link operation:

`.partial -> final`

The final path must still be absent.

Hard-link creation provides V1 no-replace publication semantics: if the final
path appeared concurrently, publication fails rather than overwriting it.

`os.replace` is not the V1 final-publication primitive because it permits
replacement of an existing final path.

## 23. Directory durability

After successful link publication, the parent directory is fsynced.

Only after that directory fsync may the final path be considered durably
published.

## 24. Successful partial retirement

After durable final publication:

1. unlink `.partial`;
2. fsync the parent directory again.

Successful completion requires the final file present and `.partial` absent.

## 25. Failure residue

If failure occurs after `.partial` creation, the persistence implementation
must not perform hidden failure cleanup.

Existing failure residue remains available for audit.

If the final link was successfully published but later cleanup/durability work
fails, the final file and any remaining partial residue are preserved.

The caller receives a failure rather than a false success.

## 26. No overwrite

V1 is immutable-file publication.

There is no update operation.

There is no overwrite operation.

There is no append-to-existing-snapshot operation.

There is no in-place repair operation.

A new scientific snapshot requires a new final path.

## 27. Writer result

Successful write returns a frozen/slotted result containing at minimum:

- final path;
- snapshot_sha256;
- file_sha256;
- byte_length.

The path is operational metadata and does not participate in snapshot
scientific identity.

## 28. Reader result

Successful read returns a frozen/slotted validated result containing at
minimum:

- reconstructed TelemetrySnapshot;
- snapshot_sha256;
- file_sha256;
- byte_length.

No unverified snapshot may escape the reader.

## 29. Determinism

Two independently constructed semantically equivalent TelemetrySnapshot
instances must generate:

- equal snapshot payload;
- equal snapshot SHA256;
- equal persistence envelope;
- byte-identical persistent files;
- equal persistent-file SHA256.

## 30. RAM-first boundary

This persistence layer consumes a completed TelemetrySnapshot.

It does not own the mutable TelemetryAccumulator.

It does not persist every event.

It does not define runtime flush cadence.

It does not decide when a snapshot should be taken.

Those are later integration concerns.

## 31. No Phase 6C integration

The module must not:

- import the Phase 6C runtime;
- create a Phase 6C runtime;
- monkey-patch the Phase 6C runtime;
- attach observers to it;
- intercept promotions or demotions;
- alter residency state;
- alter pinning;
- change budgets.

Runtime integration requires a separate prospective protocol.

## 32. No planner

The persistence module does not choose object placement.

It does not compute a repack plan.

It does not optimize locality.

It does not rank alternative physical layouts.

It only persists validated telemetry evidence for later scientific use.

## 33. No generation realization

The persistence module must not:

- build a MAF segment;
- write a candidate model generation;
- alter an active-generation file;
- activate a generation;
- roll back a generation.

## 34. No Phase 6E semantics

This module does not implement:

- partial tensor reconstruction;
- fragment retrieval;
- selective materialization;
- tensor avoidance;
- shadow hidden-state comparison;
- logit agreement;
- token agreement.

Phase 6E has not been entered.

## 35. No performance verdict

This protocol contains no storage benchmark.

It contains no latency experiment.

It contains no throughput experiment.

It contains no flash-wear experiment.

It contains no filesystem-comparison experiment.

Performance verdict is NONE.

## 36. No network

Implementation and validation must require no network access.

No package download is authorized.

No model download is authorized.

## 37. Standard-library implementation boundary

The persistence implementation must use only Python standard-library
dependencies plus the already-frozen Phase 6D locality data-model module.

A new third-party persistence dependency is not authorized by this protocol.

## 38. Error model

The implementation must expose persistence-specific validation/read/write
errors without weakening the frozen data-model errors.

At minimum, failures must be distinguishable as:

- persistence validation error;
- persistence read error;
- persistence write/publication error.

Exact class names are frozen by implementation before validation.

## 39. Future validation discipline

Persistence Validation V1 must be prospectively preregistered after the
implementation itself has been implemented, statically audited, and frozen.

The future runner must then be frozen separately.

A final no-write preflight is required.

The first scientific runner invocation permanently spends that validation
version.

No spent validation runner may be edited or rerun under the same version.

## 40. Failure residue discipline

Scientific validation failure artifacts are frozen before interpretation.

No failed scientific validation is silently cleaned and rerun.

A harness correction requires a new prospectively preregistered validation
version.

## 41. Mandatory future validation requirements

### P01_frozen_provenance_binding

Bind the persistence implementation to the exact frozen Phase 6D parent protocol, validated locality data-model protocol, validated data-model implementation, accepted data-model result, formal data-model verdict, and frozen Phase 6C runtime identities.

### P02_import_time_side_effect_absence

Importing the persistence implementation must not create, modify, rename, link, or delete filesystem objects.

### P03_exact_file_schema

The persistence envelope schema must be exactly `openmind.maf_segment_locality.telemetry_snapshot_file.v1`.

### P04_exact_envelope_key_set

The persisted top-level envelope must contain exactly `schema`, `snapshot_sha256`, and `snapshot` with no additional or missing keys.

### P05_snapshot_member_exact_payload

The `snapshot` member must equal the JSON-compatible mapping returned by the frozen data model's `snapshot_payload(snapshot)` without semantic additions, omissions, or normalization.

### P06_snapshot_sha_exact

The envelope `snapshot_sha256` must equal the frozen data model's `snapshot_sha256(snapshot)` for the exact contained snapshot.

### P07_canonical_file_bytes

Persistent file bytes must be the frozen canonical JSON encoding of the entire envelope: sorted keys, compact separators, UTF-8, ensure_ascii=False.

### P08_no_trailing_newline

Canonical persistent file bytes must contain no trailing newline or other bytes outside the canonical JSON document.

### P09_deterministic_file_sha

The file SHA256 must be computed over the exact canonical persistent file bytes and be reproducible for equivalent snapshots.

### P10_empty_snapshot_round_trip

A valid empty TelemetrySnapshot must persist and reconstruct exactly.

### P11_nonempty_snapshot_round_trip

A valid non-empty TelemetrySnapshot containing representative object, transition, cache, residency, and prefetch aggregates must persist and reconstruct exactly.

### P12_source_identity_preservation

model_pk, source_generation_pk, and source_manifest_sha256 contained in the snapshot must survive persistence and read-back exactly.

### P13_sequence_identity_preservation

first_sequence, last_sequence, event_count, and access_event_count must survive persistence and read-back exactly.

### P14_aggregate_order_preservation

The deterministic aggregate tuple ordering accepted by the frozen data model must survive persistence and read-back exactly.

### P15_strict_utf8_decode

Read-back must reject persistent bytes that are not strict UTF-8.

### P16_invalid_json_rejection

Read-back must reject malformed JSON.

### P17_noncanonical_json_rejection

Read-back must reject semantically valid JSON whose bytes are not the exact canonical encoding required by this protocol.

### P18_unknown_envelope_key_rejection

Read-back must reject an otherwise valid envelope containing an unknown top-level key.

### P19_missing_envelope_key_rejection

Read-back must reject an envelope missing any required top-level key.

### P20_wrong_schema_rejection

Read-back must reject a persistence schema other than the exact V1 schema.

### P21_snapshot_sha_syntax_rejection

Read-back must reject snapshot_sha256 values that are not exactly 64 lowercase hexadecimal characters.

### P22_snapshot_sha_mismatch_rejection

Read-back must reject an envelope whose declared snapshot SHA256 does not match the reconstructed snapshot.

### P23_payload_mutation_detection

Mutating any identity-relevant snapshot payload field without updating all bound identity must be detected and rejected.

### P24_malformed_nested_payload_rejection

Read-back must reject malformed object, transition, cache, residency, or prefetch aggregate payload structures.

### P25_unknown_nested_field_rejection

Read-back must reject unknown fields inside snapshot and aggregate payload objects rather than silently ignoring them.

### P26_invalid_integer_semantics_rejection

Read-back must preserve the frozen data model rule that booleans are not integers and invalid negative integer fields are rejected.

### P27_invalid_pk_rejection

Read-back must reject malformed model, generation, or object PKs by delegating to or exactly preserving the frozen data-model validators.

### P28_invalid_aggregate_invariant_rejection

Read-back must reject aggregate states that violate frozen data-model invariants, including prefetch consumed+unused exceeding issued.

### P29_missing_file_rejection

The reader must reject a missing final snapshot path.

### P30_nonregular_file_rejection

The reader must reject directories and other non-regular filesystem objects.

### P31_symlink_rejection

The reader must reject a symbolic-link snapshot path rather than following it as persistence authority.

### P32_parent_directory_required

The writer must require an already-existing parent directory and must not create directory hierarchy implicitly.

### P33_existing_final_refusal

The writer must refuse to overwrite or replace an already-existing final snapshot path.

### P34_existing_partial_refusal

The writer must refuse to start when the exact sibling `.partial` publication path already exists.

### P35_partial_exclusive_creation

The sibling `.partial` file must be created with exclusive creation semantics so concurrent or stale residue cannot be silently replaced.

### P36_complete_partial_write

The writer must write the entire canonical byte sequence, detect short writes, and fsync the partial file before publication.

### P37_atomic_no_replace_publication

V1 publication must use a same-directory atomic no-replace operation. The preregistered mechanism is an atomic hard-link from the fully fsynced sibling `.partial` file to the absent final path.

### P38_final_no_replace_race_safety

If another actor creates the final path before publication, atomic publication must fail rather than overwrite that path.

### P39_parent_directory_fsync

After final publication, the parent directory must be fsynced before the operation can be reported as durably published.

### P40_success_partial_removal

After durable final publication, successful completion must unlink the sibling `.partial` name and fsync the parent directory again.

### P41_failure_residue_preservation

After a write has begun, publication failure must not silently delete diagnostic partial residue. Failure residue is preserved for audit.

### P42_no_read_modify_write

Snapshot persistence is append-by-new-file publication. V1 must expose no API that edits an existing persisted snapshot in place.

### P43_serialization_determinism

Two independently created equivalent snapshots must produce identical envelope payloads, identical file bytes, identical snapshot SHA256, and identical file SHA256.

### P44_validated_read_result

Successful read-back must return a frozen/slotted validated result containing the reconstructed TelemetrySnapshot, snapshot SHA256, file SHA256, and exact file byte length.

### P45_write_result

Successful publication must return a frozen/slotted write result containing snapshot SHA256, file SHA256, exact byte length, and the final path without changing scientific snapshot identity.

### P46_phase6c_immutability

Persistence implementation and validation must leave the frozen Phase 6C runtime SHA256 unchanged.

### P47_no_runtime_integration

The persistence module must not import, monkey-patch, instrument, or invoke the Phase 6C runtime. The Phase 6C SHA is provenance only.

### P48_no_repack_planner_or_performance_claim

The persistence module must not implement repack planning, generation realization, activation, benchmarks, timing claims, Phase 6E selective access, or any performance verdict.

## 42. Required validation requirement set

The exact ordered persistence requirement identifiers are:

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

## 43. Implementation progression

The authorized order is:

1. freeze this protocol;
2. implement the standalone persistence module;
3. static-audit the implementation without importing it;
4. freeze the implementation locally;
5. preregister Persistence Validation V1;
6. implement and statically audit the validation runner;
7. freeze the runner;
8. perform a final no-write preflight;
9. execute Validation V1 exactly once;
10. freeze the raw result before interpretation;
11. record the accepted verdict if valid.

Runtime integration is not part of this progression.

## 44. Phase 6D continuation after persistence validation

Only after persistence correctness is accepted may Phase 6D proceed to
prospective work for a frozen telemetry corpus and later telemetry/runtime
observation integration.

Planner selection remains separate.

Repack realization remains separate.

The locality experiment remains separate.

Device benchmarking remains separate.

## 45. Authorization boundary

PERSISTENCE PROTOCOL: PREREGISTERED BY THIS ARTIFACT.

PERSISTENCE IMPLEMENTATION: AUTHORIZED AFTER THIS PROTOCOL IS FROZEN.

PERSISTENCE VALIDATION PROTOCOL: NOT YET AUTHORIZED FOR EXECUTION.

PERSISTENCE VALIDATION RUNNER: NOT YET AUTHORIZED.

PERSISTENCE VALIDATION EXECUTION: NOT AUTHORIZED.

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
