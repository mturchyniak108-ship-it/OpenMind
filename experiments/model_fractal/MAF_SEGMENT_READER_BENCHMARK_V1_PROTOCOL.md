# OpenMind MAF Segment Reader Benchmark V1 Protocol

Status: PREREGISTERED / NOT EXECUTED

## Purpose

Characterize the latency, throughput, and cost structure of the frozen Segment Reader V1 implementation after successful functional validation.

This benchmark is observational.

No latency, ratio, speedup, or performance acceptance threshold is preregistered.

Performance values must be reported as measured and must not be used to retroactively redefine success.

## Frozen Subject

The benchmark subject is:

    experiments/model_fractal/maf_segment_reader_v1.py

The reader contract remains:

    read_serialized_object(entry, expected_generation_pk)

The benchmark must not modify the reader.

## Preserved Source

Use only the already-preserved Phase 6B.9 benchmark fixture:

    results/runtime/maf_resident_pk_directory_benchmark_v1_1/candidate_a.manifest.json

and the immutable `.mafseg` files already present beneath:

    results/runtime/maf_resident_pk_directory_benchmark_v1_1

No source segment may be rewritten, copied over, truncated, or cleaned.

## Fixture Selection

Resolve valid ResidentPKEntry objects before timing.

Select up to the first three resolvable objects, requiring:

- at least two objects;
- at least two distinct offsets;
- exact segment length and segment SHA256;
- exact object range SHA256 equal to object_file_sha256;
- physical object-file hash distinct from payload_sha256.

Fixture discovery, manifest parsing, segment discovery, and expected-byte construction are outside timed regions.

## Benchmark Modes

For every selected object measure three modes.

### 1. reader_v1

Call the frozen:

    read_serialized_object(entry, expected_generation_pk)

This includes the actual V1 behavior:

- entry/range checks;
- open;
- fstat;
- bounded pread;
- object_file_sha256 verification;
- close.

### 2. direct_nohash_reference

Use an equivalent read-only open/fstat/pread/close path but omit object SHA256 verification and reader-level entry validation.

This is a reference baseline only.

It is NOT an alternative implementation and does not provide the integrity guarantees of Segment Reader V1.

### 3. whole_segment_hash_reference

Open the segment read-only, read the entire segment, verify the full segment SHA256, then return the requested object range.

This is deliberately outside the V1 hot-path contract.

It exists only to quantify the cost of a whole-segment integrity strategy that Segment Reader V1 intentionally avoids.

## Open Flags

All benchmark/reference segment opens must use:

    O_RDONLY

plus:

    O_CLOEXEC

when available.

No write-capable file-open flag is permitted.

## Timing

Clock:

    time.perf_counter_ns

Per selected object:

    warmup calls per mode = 100
    measured calls per mode = 1000

Warmup samples are discarded.

Measured mode order rotates deterministically each iteration to reduce fixed ordering bias:

    reader_v1
    direct_nohash_reference
    whole_segment_hash_reference

then rotate left by iteration modulo three.

The timer surrounds only the mode call.

Returned-byte verification occurs immediately after stopping the timer.

## Raw Evidence

Preserve every measured nanosecond sample in the raw JSON result.

For each object and mode derive latency statistics:

- count;
- minimum;
- maximum;
- mean;
- median;
- nearest-rank p95.

Throughput is mandatory alongside latency.

For every latency sample derive:

    operations_per_second = 1_000_000_000 / latency_ns

For every mode also derive returned-object throughput:

    bytes_per_second = object_length * 1_000_000_000 / latency_ns

    mib_per_second = bytes_per_second / (1024 * 1024)

For `whole_segment_hash_reference` additionally derive physical
segment-processing throughput using `segment_length` as the processed
byte count:

    segment_bytes_per_second =
        segment_length * 1_000_000_000 / latency_ns

    segment_mib_per_second =
        segment_bytes_per_second / (1024 * 1024)

For every throughput distribution report:

- count;
- minimum;
- maximum;
- mean;
- median;
- nearest-rank p95.

Aggregate throughput must be derived sample-by-sample using the actual
object length associated with each sample. Whole-segment aggregate
processing throughput must likewise use the actual segment length
associated with each sample.

Raw timing samples remain authoritative. Throughput is derived
deterministically from those preserved samples.

Also derive aggregate latency and throughput statistics per mode across
all selected objects.

Ratios are descriptive only.

Latency ratios:

- reader median latency / direct-nohash median latency;
- whole-segment-hash median latency / reader median latency.

Throughput ratios:

- reader median operations/s / direct-nohash median operations/s;
- whole-segment-hash median operations/s / reader median operations/s;
- equivalent returned MiB/s median ratios.

No latency or throughput ratio is a PASS/FAIL threshold.

## Integrity Requirements

The benchmark itself is valid only if:

- protocol identity is exact;
- reader identity is exact;
- resident-directory dependency identity is exact;
- functional validation result identity is exact;
- at least two valid objects with distinct offsets are selected;
- every warmup and measured return equals the independently reconstructed expected object bytes;
- source evidence is unchanged before versus after benchmark;
- `/proc/self/fd` count is balanced when supported;
- all reference opens are read-only;
- no timed region performs manifest discovery or JSON parsing.

Integrity failure invalidates benchmark interpretation but does not authorize a rerun.

## Exact-Once Rule

Before execution:

- benchmark result must be absent.

The frozen runner may execute exactly once.

No automatic retry is permitted.

If execution fails, the first failure is evidence and the runner must not be rerun.

## Result

Publish exactly once to:

    experiments/model_fractal/maf_segment_reader_benchmark_v1.json

using exclusive create mode.

Schema:

    openmind.maf_segment_reader_benchmark.v1

The result must contain:

- frozen identities;
- source identity/fingerprint;
- benchmark configuration;
- selected fixture metadata;
- raw samples;
- derived latency statistics;
- derived operations/s, bytes/s, and MiB/s throughput statistics;
- whole-segment processing throughput where applicable;
- descriptive latency and throughput ratios;
- integrity checks;
- fatal_error;
- benchmark_valid.

## Claim Boundary

This benchmark may characterize only the tested device, files, object sizes, offsets, Python runtime, and frozen Segment Reader V1 implementation.

It does NOT establish:

- universal O(1) production performance;
- production storage-engine selection;
- raw payload decoding;
- payload_sha256 reconstruction;
- FD caching or mmap residency;
- Phase 6C runtime residency;
- selective tensor avoidance;
- MAF-native inference performance;
- replacement of a standard LLM runtime.
