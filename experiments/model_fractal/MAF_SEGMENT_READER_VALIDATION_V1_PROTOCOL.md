# MAF Segment Reader V1 Functional Validation Protocol

## Status

PREREGISTERED / NOT EXECUTED

This protocol validates the frozen Segment Reader V1 implementation.

Validation MUST NOT execute before this protocol and its runner are frozen.

## Frozen identities

Segment Reader V1 protocol SHA256:

    192402f1e4f2d41540d225cce7629757152b9996a9adffaafeab6674e13f0f5d

Segment Reader V1 engine SHA256:

    3499cb8e528fe8e9315e3e5656d6aa888c95ca175310b6371e722de409827369

Resident PK Directory V1 engine SHA256:

    4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6

## Validation source

The validation uses preserved Phase 6B runtime evidence under:

    results/runtime/maf_resident_pk_directory_benchmark_v1_1

The source generation manifest is:

    results/runtime/maf_resident_pk_directory_benchmark_v1_1/candidate_a.manifest.json

The preregistration audit found:

- eligible serialized objects: 2
- distinct physical offsets: 2
- distinct segment IDs: 1
- positive sample count: 2

Preserved Phase 6B evidence is read-only input.

The validation MUST NOT modify or clean that evidence.

## Exact-once rule

The validation result path is:

    experiments/model_fractal/maf_segment_reader_validation_v1.json

The validation runtime path is:

    results/runtime/maf_segment_reader_validation_v1

Both MUST be absent before execution.

The runner may execute exactly once.

No automatic retry is permitted.

If execution produces negative evidence, that evidence is preserved and interpreted rather than overwritten by a rerun.

## Positive acceptance

The runner MUST validate at least two distinct descriptor objects with different physical offsets.

For each selected object it MUST:

1. construct a ResidentPKEntry from the preserved descriptor and matched immutable segment;
2. independently obtain the expected serialized-object range from the preserved segment;
3. invoke read_serialized_object(entry, entry.generation_pk);
4. require exact byte equality with the independently sliced serialized-object bytes;
5. require returned length == entry.length;
6. require SHA256(returned bytes) == entry.object_file_sha256;
7. require the returned physical checksum not to be substituted with payload_sha256.

## Generation-before-I/O acceptance

A generation mismatch MUST raise:

    MAFSegmentReaderStaleGenerationError

The test entry MUST reference a deliberately missing segment path.

Receiving the stale-generation exception rather than an I/O exception proves rejection occurred before storage open.

## Input and range rejection

The validation MUST verify exact rejection of:

- non-ResidentPKEntry input;
- non-string expected_generation_pk;
- negative offset;
- negative length;
- negative segment_length;
- offset greater than segment_length;
- offset + length greater than segment_length;
- empty segment_path;
- empty object_file_sha256.

No unverified bytes may be returned.

## Physical-storage failures

The validation MUST verify:

- missing segment path -> MAFSegmentReaderSegmentIOError;
- non-regular target -> MAFSegmentReaderNonRegularSegmentError;
- same-path file-size mismatch -> MAFSegmentReaderSegmentLengthMismatchError;
- forced short positional read -> MAFSegmentReaderShortReadError;
- same-size serialized-object corruption -> MAFSegmentReaderObjectHashMismatchError;
- deliberately wrong object_file_sha256 -> MAFSegmentReaderObjectHashMismatchError.

The short-read test may replace only the reader module's os facade temporarily.

All monkeypatching MUST be restored before the test continues.

## Immutability

ResidentPKEntry MUST remain frozen.

An attempted field mutation MUST raise dataclasses.FrozenInstanceError.

The reader operation MUST NOT mutate the entry.

## Descriptor closure

The validation MUST measure /proc/self/fd where available.

It MUST perform:

- 100 successful verified reads;
- 100 object-hash-mismatch reads;
- 100 non-regular-target reads.

After each repeated workload group, file-descriptor count MUST return to its baseline.

When /proc/self/fd is unavailable, the condition MUST be recorded as unsupported rather than fabricated.

## Read-only open flags

The validation MUST temporarily replace only the reader module's os facade with a tracking proxy.

At least one successful read MUST be observed.

Every reader os.open flag set MUST exclude:

- O_WRONLY;
- O_RDWR;
- O_CREAT;
- O_TRUNC;
- O_APPEND.

The original os facade MUST then be restored.

## Static hot-path prohibitions

The frozen Segment Reader engine MUST be inspected without executing a reader call.

The direct reader function MUST have:

- no JSON parsing;
- no manifest discovery;
- no source-GGUF access;
- no payload_sha256 consumption;
- no segment_sha256 whole-segment verification;
- no filesystem-write flags or write API;
- no directory search;
- no descriptor cache/residency;
- no activation or rollback call.

The function MUST contain:

- generation comparison before os.open;
- physical-range validation before os.open;
- os.open with O_RDONLY;
- os.fstat(fd);
- stat.S_ISREG;
- os.pread(fd, length, offset);
- exact-length check;
- object_file_sha256 verification;
- os.close(fd) in the descriptor-finalization path.

## Runtime fixture policy

Negative-test files are created only under:

    results/runtime/maf_segment_reader_validation_v1

The runner may copy preserved segment bytes into that runtime to create controlled variants.

It MUST NOT mutate preserved source segments.

Runtime evidence MUST remain preserved after execution.

No cleanup is performed by the validation runner.

## Result requirements

The raw JSON result MUST include:

- schema/version;
- frozen protocol and engine SHA256 values;
- source-manifest SHA256;
- positive object count;
- every named boolean acceptance check;
- exact expected/observed exception names for negative cases;
- FD baseline/final counts where measurable;
- read-only open flag evidence;
- fatal_error;
- all_pass.

A fatal internal runner error MUST fail closed and be recorded when result publication remains possible.

## Required named checks

At minimum the result MUST contain:

- positive_exact_bytes
- positive_exact_lengths
- positive_object_hashes
- positive_multiple_offsets
- generation_mismatch_before_io
- invalid_entry_rejected
- invalid_generation_type_rejected
- negative_offset_rejected
- negative_length_rejected
- negative_segment_length_rejected
- offset_past_segment_rejected
- upper_bound_rejected
- empty_segment_path_rejected
- empty_object_hash_rejected
- missing_segment_rejected
- nonregular_segment_rejected
- segment_length_mismatch_rejected
- short_read_rejected
- corrupted_object_rejected
- wrong_object_hash_rejected
- resident_entry_frozen
- entry_unchanged_after_read
- fd_success_balanced
- fd_hash_failure_balanced
- fd_nonregular_failure_balanced
- reader_opened_read_only
- static_generation_before_open
- static_range_before_open
- static_same_fd_fstat_pread
- static_object_hash_only
- static_no_payload_hash
- static_no_whole_segment_hash
- static_no_json_manifest_gguf
- static_no_write_api
- static_no_residency
- preserved_sources_unchanged

## Nonclaims

This functional validation is not a performance benchmark.

It does not validate:

- raw payload decoding;
- payload_sha256 reconstruction;
- tensor reconstruction;
- segment residency;
- FD caching;
- mmap residency;
- Phase 6C.

## Next boundary

After the protocol and runner are frozen, a separate final read-only preflight is required before the single permitted validation execution.
