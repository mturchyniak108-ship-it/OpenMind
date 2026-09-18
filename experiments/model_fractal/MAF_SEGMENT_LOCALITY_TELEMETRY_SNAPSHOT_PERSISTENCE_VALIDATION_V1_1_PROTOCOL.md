# MAF Segment Locality Telemetry Snapshot Persistence Validation V1.1 Protocol

Status: PROSPECTIVE PREREGISTRATION

Phase: 6D — Segment Locality and Path-Aware Repacking

Target: frozen Android-compatible Telemetry Snapshot Persistence V1.1

Scientific execution status: NOT YET EXECUTED

Exact-once slot: UNSPENT

Benchmark status: FORBIDDEN

Performance verdict: NONE

Runtime integration: NOT AUTHORIZED

6D-Q: ROADMAP ONLY / NOT ACTIVE

Phase 6E: NOT ENTERED

## Purpose

This protocol prospectively defines the first scientific validation of
the frozen Telemetry Snapshot Persistence V1.1 implementation.

Persistence V1.1 is the platform-compatible successor to frozen
Persistence V1. Its deliberate implementation change is the publication
primitive only: Android-compatible ctypes/libc renameat2 with
RENAME_NOREPLACE replaces the V1 hard-link publication sequence.

The file schema, canonical envelope, reader, reconstruction logic,
source data model, source-authority semantics, and successful result
contracts remain inherited from the frozen V1 lineage.

The validation must independently establish both inherited persistence
correctness and the new publication behavior.

## Frozen identities

- Persistence V1.1 protocol SHA256: `511c995fd86998da33e47691db98794ddcda9e51ec3fd71794a2324ef2a53bba`
- Persistence V1.1 implementation SHA256: `cb1e2e3dc11006c75e38e33c941b39959aa4d99f971de9e08250d8b995fe09b0`
- Persistence V1 protocol SHA256: `0e08a8a18a45a16eddc05927b8191d73ca9fc7453cb97fc1140e5e243e03db51`
- Persistence V1 implementation SHA256: `4a7c8ba1e1d7e9e4004a16d54464f17fd07ba75cc84ddea25403697d53d0581c`
- Persistence Validation V1 protocol SHA256: `7c79cf2eb97e98c14fb0acbd947ca30a8e46746eba1bd2b0127375ac01b8b9a5`
- Persistence Validation V1 runner SHA256: `27939c9524fa351af9b1b99910902c951abb1a36d00dbabc07171624515541c7`
- Persistence Validation V1 result: ABSENT
- Persistence Validation V1 exact-once slot: UNSPENT
- Locality data model SHA256: `5432f2d74a610f2d0f9181e9af146013bb198a4e837af634993909358fff8ad0`
- Accepted data-model result SHA256: `9aa2e467dc451b2d2122802e1e8b8fabf616db756a36b53a3600cca793923b4d`
- Formal data-model verdict SHA256: `7754c9d5dada8dc214a21236827c64cafea880e4b0c679cd84c9c4833fd3e9db`
- Closed Phase 6C engine SHA256: `4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9`

Any mismatch in these frozen identities before target import makes the
Validation V1.1 harness invalid.

## Validation result contract

The raw result schema shall be exactly `openmind.maf_segment_locality.telemetry_snapshot_persistence_validation.v1_1`.

The raw result shall contain at minimum:

- schema;
- validation_valid;
- all_pass;
- check_count;
- checks;
- failed_checks;
- fatal_error;
- benchmark_executed;
- performance_verdict;
- target_protocol_sha256;
- target_implementation_sha256;
- platform;

check_count shall be exactly 57.

benchmark_executed shall be false.

performance_verdict shall be null.

A fatal harness/binding error must not be converted into a scientific
target pass.

## Fixture requirements

The runner shall construct snapshots using the already-frozen locality
data model rather than inventing a parallel snapshot representation.

At minimum it shall exercise:

- one valid empty TelemetrySnapshot;
- one deterministic representative nonempty snapshot containing object,
  transition, named-cache, residency-transition, and prefetch aggregates;
- strict malformed/corrupt file cases;
- successful actual Android write/read publication;
- preflight final and partial refusal;
- deterministic exact-backend collision behavior;
- failure residue preservation.

All temporary storage shall be isolated from repository authority.

Temporary validation artifacts may be removed only by the validation
harness after all scientifically relevant failure residue has first been
measured and recorded. The frozen target itself must perform no hidden
cleanup where the protocol requires residue preservation.

## Corrected no-replace methodology

Validation V1.1 shall not reproduce the frozen V1 P38 synchronization
defect.

No scientific claim shall infer that the target had passed its file-fsync
boundary merely because the .partial pathname was visible.

Instead the no-replace claim is decomposed into two independently
observable facts:

1. static analysis of the exact frozen target proves the writer order
   _write_all -> file fsync -> file close ->
   _publish_snapshot_noreplace;
2. deterministic dynamic execution of the exact frozen
   _publish_snapshot_noreplace helper uses an already-complete and
   already-fsynced partial while an existing final sentinel is present.

The second fact must return publication failure while preserving both
the fully fsynced source residue and existing final authority.

This is not a timing benchmark and does not claim a synchronized race.

## Validation checks

### V01_frozen_predecessor_binding

Before importing either persistence implementation or the locality data model, independently SHA256-hash every frozen predecessor named by this protocol. Require exact identities for Persistence V1.1 protocol and implementation, Persistence V1 protocol and implementation, frozen unexecuted V1 validation protocol and runner, accepted locality data-model implementation/result/verdict, and the closed Phase 6C engine. A binding mismatch makes the harness invalid.

### V02_platform_successor_identity

Prove that the target under test is exactly Persistence V1.1, that its PERSISTENCE_PROTOCOL_SHA256 names the frozen V1.1 protocol, that its frozen predecessor constants name the exact V1 lineage, and that no V1 validation result exists. V1 remains historical and unexecuted.

### V03_file_schema_unchanged

Require SNAPSHOT_FILE_SCHEMA to equal exactly `openmind.maf_segment_locality.telemetry_snapshot_file.v1`.

### V04_envelope_key_set_unchanged

For a valid snapshot, require snapshot_file_payload to return exactly the top-level keys schema, snapshot_sha256, and snapshot, with no unknown or missing top-level field.

### V05_snapshot_payload_unchanged

Require the envelope snapshot member to equal exactly the frozen locality data-model snapshot_payload(snapshot) mapping.

### V06_snapshot_sha_unchanged

Require envelope snapshot_sha256 to equal exactly the frozen locality data-model snapshot_sha256(snapshot) value.

### V07_canonical_file_bytes

Require snapshot_file_bytes(snapshot) to equal exactly the frozen canonical JSON byte encoding of snapshot_file_payload(snapshot): sorted keys, compact separators, UTF-8, and ensure_ascii false.

### V08_no_trailing_newline

Require canonical file bytes to end with the canonical JSON content itself, with no trailing newline or padding byte.

### V09_file_sha256

Require snapshot_file_sha256(snapshot) and successful write/read results to bind SHA256 of the complete canonical envelope bytes. Confirm this file SHA is independently computed from the snapshot payload SHA.

### V10_strict_reader_semantics_unchanged

Exercise the inherited strict reader with valid empty and nonempty round trips and corruption cases. The corruption matrix shall cover invalid UTF-8, invalid JSON, duplicate JSON keys, noncanonical JSON, unknown/missing envelope fields, wrong schema, invalid SHA syntax, snapshot SHA mismatch, payload mutation, malformed nested payloads, unknown nested fields, invalid plain-integer semantics including bool rejection, invalid PKs, and invalid aggregate invariants. No corrupt case may be accepted.

### V11_symlink_read_rejection

If symlinks are supported by the platform, create a validation-only symlink to a valid snapshot and require read_snapshot_file to reject the symlink authority. If the platform cannot create a symlink, the harness is invalid rather than passing the check by omission.

### V12_nonregular_read_rejection

Require read_snapshot_file to reject a directory or other available nonregular path presented as snapshot authority.

### V13_no_reader_repair_or_fallback

Prove statically and dynamically that malformed final authority is rejected rather than repaired, and that a sibling .partial file is never selected as read authority when the final is missing or invalid.

### V14_parent_directory_required

Invoke the frozen V1.1 writer with a final path under a missing parent and require explicit write failure without creating the parent.

### V15_existing_final_preflight_refusal

Create a final sentinel before invoking write_snapshot_file. Require preflight refusal and prove the final bytes and identity remain unchanged and no partial is created.

### V16_existing_partial_preflight_refusal

Create the exact sibling partial sentinel before invoking write_snapshot_file. Require refusal and prove the residue bytes and identity remain unchanged and no final is published.

### V17_exact_partial_path

Require partial_path_for(final) to return exactly the same-directory pathname formed by appending .partial to the final filename.

### V18_partial_exclusive_creation

Prove statically that the writer uses O_CREAT and O_EXCL for partial creation and dynamically confirm that an existing partial cannot be truncated or overwritten.

### V19_complete_partial_write

Prove statically that the canonical byte sequence is passed through the inherited robust _write_all loop before publication. In failure tests where a completed partial is intentionally retained, independently hash the residue and require exact canonical bytes.

### V20_partial_file_fsync_before_publication

Using AST/source-order evidence from the exact frozen implementation, prove the writer sequence is _write_all -> os.fsync(partial fd) -> os.close(partial fd) -> _publish_snapshot_noreplace. Dynamic success shall additionally prove the actual Android path completes this flow.

### V21_ctypes_standard_library_backend

Prove statically that the publication backend uses Python standard library ctypes and does not require an external Python package.

### V22_libc_load_use_errno

Prove the lazy backend loader contains exactly one ctypes.CDLL(None, use_errno=True) call and that no CDLL loading occurs at module import time.

### V23_renameat2_symbol_required

Prove statically that the backend requires libc.renameat2 and converts an absent symbol into TelemetrySnapshotPersistenceBackendError with no fallback publication primitive.

### V24_exact_renameat2_abi_binding

Prove statically that renameat2 argtypes are exactly int, char pointer, int, char pointer, unsigned int and that restype is int before use.

### V25_rename_noreplace_exact_value

Require RENAME_NOREPLACE to be the plain integer value 1.

### V26_parent_directory_fd

Prove the publication helper opens the parent directory and supplies its already-open descriptor to the renameat2 operation.

### V27_same_directory_relative_names

Prove the exact renameat2 call uses the same parent fd for source and destination and os.fsencode(partial.name)/os.fsencode(final.name), not absolute source or destination paths.

### V28_exact_renameat2_publication

Prove statically that the authoritative publication transition is exactly one five-argument renameat2(parent_fd, partial_name, parent_fd, final_name, RENAME_NOREPLACE) call.

### V29_publication_success_return

On the real Android backend, invoke write_snapshot_file for a valid snapshot and absent final/partial. Require successful publication and a validated TelemetrySnapshotWriteResult.

### V30_success_consumes_partial_name

After successful write_snapshot_file, require the final to exist and the exact sibling .partial pathname not to exist.

### V31_success_final_regular_file

After successful publication, lstat the final and require ordinary regular-file authority, not symlink authority.

### V32_success_inode_identity_preserved

For a validation-only fully fsynced partial passed to the exact frozen _publish_snapshot_noreplace helper, capture its device/inode before publication and require the successful final to retain that same device/inode after the rename.

### V33_atomic_no_replace_collision

Create a fully written and fsynced validation-only partial plus an already-existing final sentinel, then invoke the exact frozen _publish_snapshot_noreplace helper. Require no-replace publication failure caused by EEXIST semantics; do not use a timing race.

### V34_collision_final_preserved

For V33, hash and stat the competing final before and after the exact backend call and require its bytes and file identity to remain unchanged.

### V35_collision_partial_preserved

For V33, hash and stat the fully fsynced partial before and after the exact backend call and require its bytes and file identity to remain unchanged as explicit failure residue.

### V36_parent_directory_fsync_after_success

Prove statically that the exact frozen publication helper calls os.fsync(parent_fd) only after renameat2 returns success and before the helper reports success. Dynamic successful publication must complete on the actual Android filesystem.

### V37_failure_residue_preservation

For publication failure after a completed partial exists, require failure residue to remain and independently hash it before temporary validation-root cleanup. The target must perform no hidden cleanup.

### V38_no_success_partial_unlink

Prove statically that Persistence V1.1 contains no os.unlink call and dynamically confirm successful publication consumes the partial name through rename rather than a second unlink operation.

### V39_no_os_link

Prove the exact frozen V1.1 implementation contains no executable os.link call.

### V40_no_posix_link

Prove the exact frozen V1.1 implementation contains no executable posix.link call.

### V41_no_symlink_publication

Prove the exact frozen V1.1 implementation contains no executable os.symlink publication call and successful authority is a regular file.

### V42_no_replace_or_plain_rename_fallback

Prove the target contains no executable os.replace or os.rename publication fallback.

### V43_no_shell_or_subprocess_publication

Prove the target does not import subprocess and contains no os.system, subprocess, shell ln, or shell mv publication path.

### V44_no_libc_hardlink_fallback

Prove the target does not bind or invoke libc link/linkat as a fallback and contains no hard-link publication path.

### V45_backend_unavailable_explicit_failure

Prove statically that CDLL load failure, absent renameat2 symbol, ABI binding failure, invocation failure, and ENOSYS each lead to the explicit backend error surface where applicable, with no alternate publication mechanism. This check does not fabricate an unavailable platform by monkey-patching the frozen target.

### V46_error_surface_distinction

Require the frozen module to expose distinct persistence validation, read, backend, and write/publication exception classes with the documented inheritance from TelemetrySnapshotPersistenceError.

### V47_write_result_contract

Require successful write_snapshot_file to return the frozen/slotted TelemetrySnapshotWriteResult with final_path, snapshot_sha256, file_sha256, and exact byte_length matching independently computed values.

### V48_read_result_contract

Require successful read_snapshot_file to return the frozen/slotted TelemetrySnapshotReadResult with reconstructed snapshot, snapshot SHA, file SHA, and exact byte length matching independently computed values.

### V49_serialization_determinism

Serialize equivalent validated snapshots repeatedly and require identical payload mappings, snapshot SHAs, envelope bytes, file SHAs, and successful read-back identity.

### V50_source_authority_immutability

Capture the source TelemetrySnapshot payload and SHA before write/read validation and require them unchanged afterward. Persistence may derive bytes but shall not mutate canonical snapshot authority.

### V51_phase6c_immutability_and_no_integration

Hash the closed Phase 6C engine immediately before target validation and again after all checks. Require exact equality and prove the V1.1 persistence implementation neither imports nor instantiates Phase 6C.

### V52_no_repack_or_generation_activation

AST/source audit the exact frozen target and validation runner for executable repack planning, build_segment, build_generation, activate_generation, or rollback_generation calls. None are authorized.

### V53_no_phase6e_performance_or_network

Require benchmark_executed false and performance_verdict null in the raw result. Prove no timing benchmark, inference, Phase 6E selective access experiment, socket/network operation, or network dependency is executed.

### V54_v1_lineage_preserved

Before and after the scientific run, require exact SHA identities for all frozen V1 artifacts and require the V1 result namespace to remain absent. The frozen V1 validation runner shall never be imported or executed by the V1.1 runner.

### V55_successor_validation_exact_once

The future Validation V1.1 runner shall refuse execution if its final result or result-temp path already exists. Its first scientific invocation permanently spends the V1.1 slot regardless of pass, fail, fatal harness error, crash, or interruption. A spent runner is never edited or rerun.

### V56_dynamic_android_backend_validation

The scientific run must execute the exact frozen V1.1 target against isolated temporary storage on the actual runtime, require sys.platform android, prove the libc renameat2 backend is available, complete a real write/read round trip, and establish successful regular-file rename-no-replace publication on that runtime.

### V57_no_replace_validation_without_timing_race

The collision proof shall combine static exact-order evidence _write_all -> partial fsync -> partial close -> frozen publication helper with deterministic execution of that exact helper against a fully written/fsynced partial and pre-existing final. It shall not claim a synchronized post-fsync race from observing partial pathname visibility and shall not use SIGSTOP/path-existence polling as proof of the durability boundary.

## Runner construction order

After this protocol is frozen, the authorized order is:

1. construct Validation V1.1 runner without importing/executing target;
2. statically audit runner against this exact protocol;
3. freeze the exact runner in a dedicated local commit;
4. perform a final no-write preflight over frozen hashes, platform,
   result absence, check identifiers, API compatibility, and execution
   methodology;
5. only if that preflight passes, invoke the frozen runner exactly once;
6. freeze the raw result before interpretation;
7. issue a formal verdict only from the frozen protocol, target, runner,
   and raw result.

## Binding-before-import rule

The runner shall independently hash all frozen source artifacts before
importing Persistence V1.1 or the locality data model.

No target import, target execution, result write, or scientific check
may occur before the binding gate succeeds.

## Import-time side-effect check

The runner shall test target import in an isolated child process with
an empty working directory before the main scientific target import.

Import shall not create files, open the libc backend, publish a
snapshot, execute renameat2, integrate Phase 6C, or perform network
activity.

## Raw-result freeze

The future runner shall write exactly one authoritative raw result to:

`experiments/model_fractal/maf_segment_locality_telemetry_snapshot_persistence_validation_v1_1.json`

The result writer may use a validation-harness-specific exclusive temp
and atomic result publication mechanism. That mechanism is not itself
the scientific persistence target and shall not be interpreted as
evidence for Persistence V1.1.

The raw result must be frozen before scientific interpretation.

## Exact-once rule

The Validation V1.1 slot is currently UNSPENT.

The first scientific invocation of the future frozen runner permanently
spends this slot regardless of pass, fail, fatal harness error, crash,
or interruption.

A spent V1.1 runner shall never be edited or rerun.

Any correction after a spent invocation requires a prospectively
versioned successor validation protocol and runner.

## Explicit nonclaims

Validation V1.1 does not test or establish:

- persistence latency or throughput;
- flash wear or write amplification;
- power-loss durability across every Android filesystem/device;
- repack planner correctness;
- locality improvement;
- runtime residency performance;
- inference behavior;
- query-scoped MAF execution;
- selective tensor/object avoidance;
- output parity;
- MAF-LLM replacement capability;
- Phase 6E;
- Phase 6F performance.

## Lineage boundary

Phase 6C remains closed and immutable.

Persistence V1 remains frozen, platform-incompatible on this Android
Python environment, and unvalidated.

Frozen Validation V1 remains unexecuted with its slot UNSPENT.

6D-Q remains roadmap-only proposed research.

Phase 6E is not entered.
