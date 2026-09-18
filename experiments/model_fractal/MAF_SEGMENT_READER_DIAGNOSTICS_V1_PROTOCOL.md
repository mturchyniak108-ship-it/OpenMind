# MAF Segment Reader Diagnostics V1 Protocol

Status: PREREGISTERED / UNEXECUTED / EXACT-ONCE

## 1. Purpose

This protocol defines the mandatory post-validation diagnostics required by
MAF Segment Reader V1 before Phase 6C may begin.

The frozen Segment Reader V1 protocol requires diagnostics to examine:

1. repeated successful-read degradation;
2. repeated failure-path degradation;
3. file-descriptor leaks;
4. retained Python-object growth;
5. RSS growth where measurable;
6. unexpected filesystem writes;
7. runtime-file accumulation;
8. unverified-byte escape;
9. short-read handling;
10. same-file-descriptor metadata/read behavior;
11. mutation/corruption failure behavior.

Diagnostics V1 exists only to satisfy that frozen Phase-6B.10 boundary.

It does not modify Segment Reader V1.

It does not rerun functional validation.

It does not rerun any Segment Reader benchmark.

It does not begin Phase 6C.

## 2. Frozen identities

Segment Reader V1 protocol:

`192402f1e4f2d41540d225cce7629757152b9996a9adffaafeab6674e13f0f5d`

Segment Reader V1 implementation:

`3499cb8e528fe8e9315e3e5656d6aa888c95ca175310b6371e722de409827369`

Segment Reader Validation V1 protocol:

`c896e6b68be67352e4b09ed8f6486cdea2e20435fa03c7c44fd4871051e202be`

Segment Reader Validation V1 runner:

`1f5cfdba3d3bd681eb78b07d98b9ee49497a3608bc51408c7e503b0dbc80bf88`

Segment Reader Validation V1 frozen result:

`1ceef1ed2b814da3951811ea97e9f4475b3fa79557b341e7c8e089ec8a409328`

Segment Reader Benchmark V1.2 completion record:

`5d5e3c10d39b39e5527e778753828ecca4aead4f60d3b92a59db4eb892644907`

The frozen validation result must remain `all_pass=true`.

## 3. Preserved source evidence

Read-only source runtime:

`results/runtime/maf_resident_pk_directory_benchmark_v1_1`

Frozen active-generation record SHA256:

`031d1a50a3cf53f158057a02bb6c68001edfb07bf48bf893afc9bc8f095458e9`

Frozen candidate manifest SHA256:

`941301aa362d3f949389e5364b1be4d7f26b96f0d45efa81346c82fce3260f93`

Frozen source segment:

`results/runtime/maf_resident_pk_directory_benchmark_v1_1/segment_00000000.mafseg`

Frozen source segment SHA256:

`f965b526538d757ca2d6114af6517c57cbcb3650b71d8cfb92046a04ef2f566b`

Frozen source segment bytes:

`4096`

The source runtime is immutable evidence.

Diagnostics must not modify, clean, rename, delete, truncate or replace any
source-runtime file.

## 4. Isolated diagnostic runtime

Diagnostics V1 uses only:

`results/runtime/maf_segment_reader_diagnostics_v1`

The diagnostic runtime and result must both be absent before the single
permitted execution.

Setup must create exact copies of the accepted active record, candidate
manifest and source segment.

A corruption fixture may be created only inside the isolated diagnostic
runtime before diagnostic measurement begins.

No diagnostic failure may authorize cleanup of the runtime.

## 5. Frozen validation helper boundary

Diagnostics V1 may import the frozen Validation V1 runner only as a helper
module.

The only Validation V1 callable authorized for use is:

`resolve_entries()`

Diagnostics V1 must not invoke Validation V1 `main()`, `run_validation()`,
or result publication.

Returned source entries must be rebound to byte-identical segment copies in
the isolated diagnostic runtime before reader diagnostics begin.

## 6. Reader boundary

The only production reader operation under diagnostic execution is:

`maf_segment_reader_v1.read_serialized_object()`

The reader implementation is frozen and must not be modified.

Process-local replacement of the reader module's `os` facade is permitted
only for the preregistered short-read and same-file-descriptor controls.

The original `os` facade must always be restored with `finally`.

## 7. Deterministic fixture

After frozen Validation V1 `resolve_entries()` reconstructs accepted source
entries, Diagnostics V1 selects one positive entry deterministically by:

1. positive serialized-object length;
2. ascending length;
3. ascending object_pk.

The selected entry is rebound only by replacing its runtime `segment_path`
with the exact isolated copy.

Logical identity, generation identity, range, lengths and hashes remain
unchanged.

## 8. Positive-read invariant

Every successful diagnostic read must return exactly the serialized bytes
addressed by the selected frozen entry.

The returned SHA256 must equal `object_file_sha256`.

Any successful return of different bytes is a fatal diagnostic-harness error.

## 9. Repeated successful-read degradation

Success degradation uses:

- 2 warmup batches;
- 20 measured batches;
- 5,000 verified reads per batch.

Each measured operation performs the real frozen reader call and verifies the
returned bytes.

For each batch record nanoseconds per operation.

Compare:

- median ns/op of the first 5 measured batches;
- median ns/op of the final 5 measured batches.

Required:

`final / initial <= 2.0`

No absolute reader-latency threshold is introduced.

## 10. Repeated failure-path degradation

The repeated failure path uses a valid entry whose
`object_file_sha256` is replaced by an intentionally wrong 64-character
lowercase SHA256 value.

The physical read and SHA256 calculation therefore occur before the expected
`MAFSegmentReaderObjectHashMismatchError`.

Failure degradation uses:

- 2 warmup batches;
- 20 measured batches;
- 2,000 expected failures per batch.

Every operation must raise exactly the expected object-hash mismatch error.

Compare median ns/op for the first 5 and final 5 measured batches.

Required:

`final / initial <= 2.5`

No absolute failure latency target is introduced.

## 11. File-descriptor diagnostics

When `/proc/self/fd` is measurable, Diagnostics V1 records descriptor counts:

- around a sustained successful-read block;
- around a sustained expected-failure block;
- around the overall diagnostic workload.

Permitted descriptor-count growth for each comparison:

`<= 2`

If `/proc/self/fd` is unavailable, this fact must be reported explicitly and
the descriptor-growth checks become not-measurable rather than silently
fabricated.

On the intended Android/Termux environment `/proc/self/fd` is expected to be
available.

## 12. Retained Python-object diagnostics

After warmup and garbage collection, Diagnostics V1 uses `tracemalloc`
current traced allocation to measure retained growth rather than transient
peak growth.

Success retention workload:

`100000` verified successful reads.

Allowed retained-current growth:

`<= 1048576 bytes`

Failure retention workload:

`50000` expected object-hash failures.

Allowed retained-current growth:

`<= 1048576 bytes`

After garbage collection, live `MAFSegmentReaderError` instances may grow by
at most 2 relative to the warmed baseline.

Total GC-tracked Python-object count may grow by at most 512 relative to the
warmed baseline.

These are diagnostic resource sentinels, not universal production memory
guarantees.

## 13. RSS diagnostic

Where `/proc/self/status` exposes `VmRSS`, record RSS around the sustained
diagnostic workload.

Allowed positive RSS growth:

`<= 16777216 bytes`

If RSS is not measurable, report `rss_measured=false`.

No universal RAM guarantee is created.

## 14. Unexpected filesystem-write diagnostic

All expected diagnostic setup writes occur before the write-audit interval.

After setup, install a process-local Python audit hook.

During reader diagnostics require zero observed write-capable filesystem
events from the diagnostic workload, including write/create/truncate/append
opens and filesystem mutation events.

The final diagnostic result publication occurs after this check is frozen in
the in-memory result and is not classified as an unexpected reader write.

## 15. Runtime-file accumulation

After all setup fixtures exist, freeze an exact runtime snapshot containing:

- relative file paths;
- file sizes;
- file SHA256 values.

After diagnostic workloads and before result publication, reconstruct the
same snapshot.

Required:

`final runtime snapshot == initial runtime snapshot`

No runtime file or byte accumulation is permitted after setup.

## 16. Unverified-byte escape

Three negative controls are mandatory:

1. wrong expected object-file hash;
2. corrupted object range;
3. forced short positional read.

Each must:

- raise the exact preregistered Segment Reader exception;
- return no bytes;
- expose no unverified serialized object to the caller.

## 17. Short-read handling

Install a process-local `os` facade whose `pread()` delegates to the real
positional read and then returns one fewer byte than was obtained.

The reader must raise:

`MAFSegmentReaderShortReadError`

The original reader `os` facade must be restored in `finally`.

## 18. Same-file-descriptor metadata/read behavior

Install a tracking `os` facade around one successful read.

It must record one ordered sequence:

`open -> fstat -> pread -> close`

The descriptor returned by `open` must be the same descriptor supplied to:

- `fstat`;
- `pread`;
- `close`.

The returned bytes must still equal the accepted serialized object.

The original reader `os` facade must be restored in `finally`.

## 19. Mutation/corruption behavior

Before measurement begins, create a byte-identical isolated segment copy and
a second isolated corruption fixture.

Flip exactly one bit inside the selected serialized-object range while
preserving total segment length.

Reading through an entry rebound to that corruption fixture must raise:

`MAFSegmentReaderObjectHashMismatchError`

No bytes may escape.

The accepted source segment and exact isolated clean copy must remain
unchanged.

## 20. Source immutability

At diagnostic completion, re-hash:

- source active-generation record;
- source candidate manifest;
- source segment.

All three hashes must remain exact.

## 21. Result semantics

Result schema:

`openmind.maf_segment_reader_diagnostics.v1`

The runner publishes exactly one JSON result with exclusive creation.

A completed diagnostic harness may validly publish:

- `diagnostics_valid=true`;
- `all_pass=false`.

A failed check is scientific diagnostic evidence and must not cause an
automatic retry.

A fatal harness error must be preserved distinctly with
`diagnostics_valid=false`.

## 22. Exact-once rule

Diagnostics V1 is exact-once.

After the frozen protocol and runner are committed and final preflight passes,
one diagnostic invocation is permitted.

Once invocation begins, no retry under Diagnostics V1 is permitted regardless
of success, failed checks, fatal error or partial runtime state.

Any later correction requires a new successor protocol/version.

## 23. Failure preservation

The runner must not clean diagnostic runtime evidence after failure.

A fatal result should preserve, when available:

- frozen identity evidence;
- source evidence;
- current runtime snapshot;
- original exception type and message.

The original exception must not be replaced by cleanup behavior.

## 24. Interpretation boundary

A passing result may establish only that the frozen Segment Reader V1
satisfied these bounded diagnostic checks on the tested device, runtime,
fixture and Python process.

It does not establish:

- absence of all resource leaks;
- universal performance stability;
- universal memory behavior;
- crash/power-loss safety;
- concurrent mutation safety;
- multithread scaling;
- production storage-engine readiness;
- Phase 6C runtime correctness;
- MAF-native inference;
- selective tensor avoidance;
- replacement of a standard LLM runtime.

## 25. Phase boundary

Diagnostics V1 is the remaining mandatory Segment Reader V1 diagnostic gate
identified by the Phase-6B exit audit.

Freezing this protocol and runner does not complete Phase 6B.10.

Phase 6B.10 may close only after:

1. protocol and runner are frozen before execution;
2. final read-only preflight passes;
3. Diagnostics V1 executes exactly once;
4. raw result is frozen before interpretation;
5. the result is interpreted;
6. a Phase-6B.10 completion checkpoint confirms the frozen diagnostic
   obligations were satisfied.

The unresolved CPU6/CPU7 cluster-1 crossover is optional, non-blocking
follow-up research and is not part of this diagnostic acceptance boundary.

Phase 6C remains not started until Phase 6B.10 closes.
