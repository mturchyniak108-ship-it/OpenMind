# MAF Segment Locality Telemetry Snapshot Persistence V1.1 Protocol

Status: PROSPECTIVE PREREGISTRATION

Phase: 6D — Segment Locality and Path-Aware Repacking

Scope: platform-compatible immutable telemetry snapshot persistence

Scientific status: NOT YET IMPLEMENTED / NOT YET VALIDATED

Performance status: NONE

Runtime integration: NOT AUTHORIZED

Phase 6E: NOT ENTERED

## Purpose

This protocol prospectively defines Persistence V1.1, a narrow
platform-compatible successor to the frozen Persistence V1 lineage.

Persistence V1 used same-directory hard-link publication. The frozen
Android/Termux environment does not expose Python `os.link` or
`posix.link`, and direct libc hard-link creation was denied on the
tested Termux-private temporary filesystem.

A subsequent isolated capability discovery established that the same
Android runtime exposes libc `renameat2`, and that
`renameat2(..., RENAME_NOREPLACE)` successfully performed
same-directory atomic no-replace publication while preserving an
ordinary regular file and returning `EEXIST` on collision.

Those discovery observations motivate this successor but do not
constitute the future V1.1 scientific validation result.

V1.1 preserves the V1 persistent file format and strict reader model.
The deliberate semantic change is limited to successful publication:

    exclusive sibling .partial
    -> complete canonical write
    -> file fsync
    -> renameat2(..., RENAME_NOREPLACE)
    -> parent-directory fsync
    -> ordinary immutable final file

A successful rename consumes the `.partial` pathname. Therefore V1.1
does not perform the V1 post-publication partial unlink step.

## Frozen predecessor state

- Persistence V1 protocol SHA256: `0e08a8a18a45a16eddc05927b8191d73ca9fc7453cb97fc1140e5e243e03db51`
- Persistence V1 implementation SHA256: `4a7c8ba1e1d7e9e4004a16d54464f17fd07ba75cc84ddea25403697d53d0581c`
- Persistence Validation V1 protocol SHA256: `7c79cf2eb97e98c14fb0acbd947ca30a8e46746eba1bd2b0127375ac01b8b9a5`
- Persistence Validation V1 runner SHA256: `27939c9524fa351af9b1b99910902c951abb1a36d00dbabc07171624515541c7`
- Persistence Validation V1 execution: NONE
- Persistence Validation V1 result: ABSENT
- Persistence Validation V1 exact-once slot: UNSPENT
- Locality data model SHA256: `5432f2d74a610f2d0f9181e9af146013bb198a4e837af634993909358fff8ad0`
- Accepted locality data-model result SHA256: `9aa2e467dc451b2d2122802e1e8b8fabf616db756a36b53a3600cca793923b4d`
- Formal locality data-model verdict SHA256: `7754c9d5dada8dc214a21236827c64cafea880e4b0c679cd84c9c4833fd3e9db`
- Closed Phase 6C engine SHA256: `4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9`

The V1 lineage is immutable historical evidence. Nothing in V1.1
authorizes editing or executing the frozen V1 validation runner.

## File format

The snapshot file schema remains `openmind.maf_segment_locality.telemetry_snapshot_file.v1`.

The exact top-level envelope remains:

1. `schema`
2. `snapshot_sha256`
3. `snapshot`

Canonical serialization remains inherited from the accepted locality
data model and Persistence V1 protocol.

## Publication backend

V1.1 shall use the process C library through Python standard-library
`ctypes`.

The required primitive is:

    renameat2(
        parent_fd,
        partial_basename,
        parent_fd,
        final_basename,
        RENAME_NOREPLACE,
    )

`RENAME_NOREPLACE` is preregistered as integer `1`.

The source and destination use the same already-open parent-directory
file descriptor and sibling relative basenames.

No hard-link, symlink, ordinary rename, overwrite-capable replace,
shell command, subprocess, or alternate backend is authorized.

## Success semantics

Successful publication requires:

1. a previously absent final pathname;
2. an exclusively created sibling partial file;
3. complete canonical bytes written to that partial;
4. successful file fsync;
5. successful `renameat2(..., RENAME_NOREPLACE)` returning zero;
6. the partial pathname consumed by the rename;
7. the final pathname naming the same completed regular-file object;
8. successful parent-directory fsync;
9. a validated write result returned only after the preceding steps.

## Collision and failure semantics

If the final pathname appears after partial creation but before
publication, RENAME_NOREPLACE must fail rather than replace it.

That collision must preserve both:

- the competing final authority unchanged; and
- the completed partial file as failure residue.

No hidden failure cleanup is authorized.

## Validation methodology note

The frozen V1 validation runner was never executed. Its P38 race
fixture was later found during no-write preflight not to prove that
its stop point occurred after partial-file fsync.

V1.1 prospectively removes that ambiguity from its future validation
method. No-replace safety shall be established by:

1. static proof of the exact writer order:
   complete write -> file fsync -> exact RENAME_NOREPLACE backend;
2. deterministic dynamic execution of that exact backend against a
   fully fsynced source and an already-existing competing final;
3. proof of `EEXIST`/failure, source preservation, and final
   preservation.

The validation shall not infer post-fsync synchronization merely from
the visibility of the partial pathname.

## Requirements

### S01_frozen_predecessor_binding

V1.1 shall bind the exact frozen Persistence V1 protocol, Persistence V1 implementation, frozen unexecuted Validation V1 protocol and runner, accepted locality data model evidence, and closed Phase 6C engine identities before any successor behavior is evaluated.

### S02_platform_successor_identity

V1.1 is a prospective platform-compatible successor to Persistence V1. It shall not edit, reinterpret, or silently replace the frozen V1 bytes.

### S03_file_schema_unchanged

The persistent snapshot file schema remains exactly `openmind.maf_segment_locality.telemetry_snapshot_file.v1`.

### S04_envelope_key_set_unchanged

The serialized envelope shall continue to contain exactly the keys `schema`, `snapshot_sha256`, and `snapshot`.

### S05_snapshot_payload_unchanged

The `snapshot` member shall remain exactly the JSON-compatible mapping returned by the frozen data model `snapshot_payload`.

### S06_snapshot_sha_unchanged

The envelope `snapshot_sha256` shall remain exactly the frozen data model `snapshot_sha256(snapshot)` value.

### S07_canonical_file_bytes

Complete file bytes shall remain the frozen canonical JSON encoding: sorted keys, compact separators, UTF-8, ensure_ascii false.

### S08_no_trailing_newline

Canonical snapshot files shall contain no trailing newline or other padding outside the canonical JSON byte sequence.

### S09_file_sha256

File SHA256 shall remain SHA256 over the complete canonical envelope bytes and shall remain distinct from the snapshot payload SHA256.

### S10_strict_reader_semantics_unchanged

V1.1 shall retain the strict V1 reader contract: exact UTF-8, valid JSON, canonical re-encoding equality, exact schema and key sets, strict nested reconstruction, payload equality, and snapshot SHA equality.

### S11_symlink_read_rejection

The reader shall reject a symlink presented as snapshot authority.

### S12_nonregular_read_rejection

The reader shall require a regular file and reject directories and other nonregular file types.

### S13_no_reader_repair_or_fallback

The reader shall not repair malformed bytes, select alternate files, follow a `.partial` file as authority, or silently fall back to a different representation.

### S14_parent_directory_required

The writer shall require the final file's parent directory to exist before publication begins and shall not create missing parents.

### S15_existing_final_preflight_refusal

If the final pathname already exists before partial creation, the writer shall refuse publication without modifying that final file.

### S16_existing_partial_preflight_refusal

If the exact sibling partial pathname already exists, the writer shall refuse publication without truncating or modifying that residue.

### S17_exact_partial_path

The partial pathname shall remain exactly `<final filename>.partial` in the same directory as the final pathname.

### S18_partial_exclusive_creation

The writer shall create the partial file using exclusive creation semantics and shall never overwrite or truncate pre-existing residue.

### S19_complete_partial_write

The complete canonical envelope byte sequence shall be written to the partial file using a robust write loop before publication.

### S20_partial_file_fsync_before_publication

The partial file descriptor shall be successfully fsynced after the complete write and before the rename-no-replace publication syscall.

### S21_ctypes_standard_library_backend

The Android-compatible publication backend shall use Python standard library `ctypes`; no external Python package is required.

### S22_libc_load_use_errno

The backend shall load the process C library using `ctypes.CDLL(None, use_errno=True)` so syscall failure errno can be read deterministically.

### S23_renameat2_symbol_required

The backend shall require the libc `renameat2` symbol. Backend unavailability is an explicit failure and shall not trigger an alternate publication mechanism.

### S24_exact_renameat2_abi_binding

The backend shall bind `renameat2` with two directory-fd integers, two C pathname pointers, one unsigned flags value, and integer return type before use.

### S25_rename_noreplace_exact_value

`RENAME_NOREPLACE` shall be bound to the exact Linux value `1`.

### S26_parent_directory_fd

Publication shall use an already-open file descriptor for the common parent directory.

### S27_same_directory_relative_names

The `renameat2` call shall use the same parent directory fd for both source and destination and shall pass only the sibling partial and final basenames as relative names.

### S28_exact_renameat2_publication

Publication shall consist of exactly `renameat2(parent_fd, partial_name, parent_fd, final_name, RENAME_NOREPLACE)` for the authoritative transition.

### S29_publication_success_return

Successful publication requires `renameat2` to return zero.

### S30_success_consumes_partial_name

On successful rename-no-replace publication, the partial pathname shall cease to exist because the same inode is renamed to the final pathname.

### S31_success_final_regular_file

The successfully published authority shall be an ordinary regular file, not a symlink or indirection object.

### S32_success_inode_identity_preserved

The rename publication shall preserve the completed partial file's underlying file identity across the pathname transition.

### S33_atomic_no_replace_collision

If another actor creates the final pathname before publication, `renameat2(..., RENAME_NOREPLACE)` shall fail rather than overwrite the competing final authority.

### S34_collision_final_preserved

A no-replace collision shall leave the existing final file unchanged.

### S35_collision_partial_preserved

A no-replace collision shall leave the completed partial file present and unchanged as explicit failure residue.

### S36_parent_directory_fsync_after_success

After successful rename-no-replace publication, the writer shall fsync the parent directory before reporting durable publication success.

### S37_failure_residue_preservation

Failures after partial creation shall not perform hidden cleanup. Existing partial residue shall be preserved whenever the failed operation leaves it present.

### S38_no_success_partial_unlink

Unlike V1 hard-link publication, V1.1 shall not unlink a partial pathname after successful publication because the successful rename already consumed that pathname.

### S39_no_os_link

V1.1 shall not call `os.link`.

### S40_no_posix_link

V1.1 shall not call `posix.link`.

### S41_no_symlink_publication

V1.1 shall not publish snapshot authority through a symbolic link.

### S42_no_replace_or_plain_rename_fallback

V1.1 shall not fall back to `os.replace`, plain `os.rename`, or an equivalent overwrite-capable publication primitive.

### S43_no_shell_or_subprocess_publication

V1.1 shall not invoke shell `ln`, `mv`, or another subprocess to publish snapshot authority.

### S44_no_libc_hardlink_fallback

V1.1 shall not fall back to libc `link` or `linkat` when `renameat2` is unavailable or fails.

### S45_backend_unavailable_explicit_failure

Absence of the required libc symbol or an unsupported backend shall produce an explicit persistence write/backend error before authority is published.

### S46_error_surface_distinction

Validation, read, backend, and write/publication failures shall remain distinguishable error surfaces.

### S47_write_result_contract

Successful writes shall return a frozen/slotted result containing the final path, snapshot SHA256, file SHA256, and exact byte length.

### S48_read_result_contract

Successful reads shall return a frozen/slotted result containing the reconstructed snapshot, snapshot SHA256, file SHA256, and exact byte length.

### S49_serialization_determinism

Equivalent validated TelemetrySnapshot values shall yield identical snapshot payloads, snapshot SHAs, envelopes, file bytes, and file SHAs.

### S50_source_authority_immutability

Persistence V1.1 shall not mutate the source TelemetrySnapshot or canonical MAF model authority while serializing, writing, or reading.

### S51_phase6c_immutability_and_no_integration

The closed Phase 6C runtime engine remains immutable. V1.1 shall not instantiate or integrate Phase 6C runtime behavior.

### S52_no_repack_or_generation_activation

V1.1 shall not implement a repack planner, realize a repacked generation, activate a generation, or alter locality policy.

### S53_no_phase6e_performance_or_network

V1.1 shall not enter Phase 6E, perform inference, execute benchmarks, make latency/throughput claims, or require network access.

### S54_v1_lineage_preserved

Frozen Persistence V1 and frozen Validation V1 remain immutable historical artifacts. Validation V1 remains unexecuted and its exact-once slot remains unspent.

### S55_successor_validation_exact_once

V1.1 shall receive its own prospective validation protocol and frozen runner. The first scientific execution of that future runner shall permanently spend the V1.1 validation slot regardless of pass, fail, crash, or interruption.

### S56_dynamic_android_backend_validation

Future V1.1 validation shall dynamically prove the actual Android runtime/backend behavior in isolated temporary storage, including successful rename-no-replace publication, regular-file authority, byte identity, and parent-directory fsync.

### S57_no_replace_validation_without_timing_race

Future V1.1 validation shall prove collision safety by combining static proof that the writer reaches the exact RENAME_NOREPLACE primitive only after complete write plus file fsync with a deterministic dynamic collision test of that exact backend after a fully fsynced source exists. Validation shall not claim a timing race was synchronized merely because a partial pathname became visible.

## Implementation order

The authorized order after this protocol is frozen is:

1. implement Persistence V1.1 only;
2. statically audit the implementation without importing/executing it;
3. freeze the exact implementation locally;
4. preregister a separate Persistence Validation V1.1 protocol;
5. implement and statically audit that validation runner;
6. freeze that runner before any scientific invocation;
7. perform a final scoped no-write execution preflight;
8. execute Validation V1.1 exactly once;
9. freeze the raw result before interpretation;
10. issue a formal verdict only from frozen evidence.

Protocol freeze does not authorize implementation execution.

## Exact-once discipline

Persistence Validation V1.1 does not yet exist.

Its future exact-once slot is therefore UNSPENT.

Once a frozen V1.1 validation runner receives its first scientific
invocation, that version slot is permanently spent regardless of
success, failure, harness failure, crash, or interruption.

A spent runner shall never be edited or rerun.

## Explicit nonclaims

This protocol does not establish:

- that Persistence V1.1 has been implemented;
- that Persistence V1.1 has passed validation;
- power-loss durability on all filesystems/devices;
- identical `renameat2` support on all Android devices;
- identical storage semantics across filesystems;
- persistence throughput or latency;
- reduced write amplification;
- reduced flash wear;
- improved inference speed;
- MAF-native inference;
- query-scoped MAF execution;
- repack-planner correctness;
- locality improvement;
- Phase 6E selective tensor avoidance;
- replacement of a conventional LLM runtime.

## Lineage boundary

6D-Q remains roadmap-only proposed research and is not activated by
this persistence successor.

Phase 6C remains closed and immutable.

Phase 6E is not entered.
