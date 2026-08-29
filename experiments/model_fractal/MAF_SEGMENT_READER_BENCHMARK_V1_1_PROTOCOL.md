# OpenMind MAF Segment Reader Benchmark V1.1 Protocol

Status: PREREGISTERED / NOT EXECUTED

## Purpose

Benchmark the frozen MAF Segment Reader V1 under CPU-placement and
thermal governance derived from CPU Thermal Characterization V1.2.

V1.1 supersedes Segment Reader Benchmark V1 before execution.

Segment Reader Benchmark V1 remains frozen and unexecuted.

This benchmark remains Phase 6B work.

Phase 6C concurrency is not started.

No multithreaded performance claim is permitted.

## Frozen Dependencies

The benchmark must bind exact frozen identities for:

- Segment Reader Benchmark V1 measurement core;
- CPU Thermal Characterization V1.2 completion record;
- CPU Thermal Characterization V1.2 raw result;
- Segment Reader V1 and its existing dependencies through the frozen
  Benchmark V1 core.

The V1 core is imported only for its already-frozen fixture resolver and
three measurement-mode functions.

Its V1 `main()`, `run_benchmark()`, `measure_all()` and result publication
must never execute.

## Benchmark Modes

Normal lane:

1. `reader_v1`
2. `direct_nohash_reference`
3. `whole_segment_hash_reference`

Micro lane:

1. `reader_v1`
2. `direct_nohash_reference`

`whole_segment_hash_reference` is intentionally excluded from the micro
lane because its work unit is the full segment rather than the bounded
serialized object addressed by the fixture.

## CPU Policy

### Normal lane

Validated CPUs:

    CPU0
    CPU3

Validated cluster:

    cluster 0

Requested measured active-work window per batch:

    <= 250 ms

The batch may exceed 250 ms only by the latency of one indivisible
operation that began before the requested active-work limit was reached.

Any such overshoot must be recorded.

Thermal state is checked after every measured operation.

Any individual operation whose latency exceeds 100 ms creates a thermal
observation-gap violation and terminates that batch.

### Prospective micro lane

Candidate CPUs:

    CPU6
    CPU7

Candidate cluster:

    cluster 1

No sustained time window is claimed for cluster 1.

Exactly one bounded serialized object operation is dispatched per micro
work unit.

Each micro dispatch requires:

1. passive cooldown while pinned to cluster 0;
2. thermal observation;
3. pin to the selected cluster-1 CPU;
4. frequency and thermal observation;
5. exactly one measured operation;
6. immediate post-operation thermal/frequency observation;
7. immediate return to cluster 0;
8. passive cooldown before another cluster-1 dispatch.

CPU6 and CPU7 alternate deterministically where possible.

The micro lane is prospective evidence only.

V1.1 must determine whether real MAF object/fragment size creates a
latency or throughput crossover that makes cluster 1 useful without
acceptable thermal limits being exceeded.

## Micro Fixture Selection

Resolve the exact fixture set using the frozen Benchmark V1 resolver.

Sort fixtures deterministically by:

    object serialized length
    stable fixture identifier

Select the smaller half of the resolved fixture set:

    ceil(N / 2)

Cap the micro set at:

    8 fixtures

At least one fixture is selected when the resolved fixture set is
non-empty.

This is a relative small-object selection rule.

It does not claim a universal byte threshold.

## Thermal Sensor Selection

Read plausible thermal zones from:

    /sys/class/thermal/thermal_zone*

Plausible range:

    0 C <= temperature <= 120 C

Exclude from the governing live-temperature set any zone type containing:

    trip
    threshold
    thresh

Excluded zones remain recorded as diagnostic evidence.

Prefer remaining zone types containing:

    cpu
    soc
    cpuss
    cluster
    apss
    little
    big
    silver
    gold
    prime

If no preferred live sensors exist, use all remaining plausible non-trip
sensors.

Execution is invalid if no plausible non-trip live thermal sensor exists.

The maximum selected live reading governs thermal decisions.

## Thermal Limits

Execution start requires:

    governing temperature < 75 C

For each workload CPU, establish its first post-cooldown live baseline.

Optimal/eligibility limit:

    min(CPU baseline + 5 C, 75 C)

Hard-stop limit:

    min(CPU baseline + 8 C, 80 C)

Global resume limit:

    min(initial benchmark baseline + 3 C, 70 C)

Passive cooldown polling:

    2 seconds

Maximum cooldown wait:

    120 seconds

No hot/throttled observation may be deleted.

## CPU Movement

The device topology preregistered for this experiment is:

    cluster 0 = CPU0,CPU1,CPU2,CPU3,CPU4,CPU5
    cluster 1 = CPU6,CPU7

Literal die-distance coordinates are unavailable.

"Cross-cluster" means movement to the opposite exposed CPU cluster.

Normal CPU0/CPU3 same-cluster transitions must use an opposite-cluster
bridge CPU before the next cluster-0 target.

Micro dispatches must use cluster 0 for relief before and after cluster-1
work.

All affinity transitions must be recorded.

Original process affinity must be restored.

## Timing

Only the target mode call is timed.

Thermal reads, cpufreq reads, affinity changes, cooldown polling and
summary work occur outside the operation timer.

Raw operation latency in nanoseconds is authoritative.

## Raw Sample Fields

Every successful measured operation records at minimum:

- lane;
- CPU;
- cluster;
- fixture identifier;
- object PK when available;
- object serialized length;
- segment length;
- mode;
- latency ns;
- returned bytes;
- processed bytes;
- thermal snapshot before;
- thermal snapshot after;
- governing temperature before;
- governing temperature after;
- CPU frequency before;
- CPU frequency after;
- thermal eligibility;
- hard-stop state;
- observation-gap violation.

## Throughput

Throughput is deterministically derived from each raw latency sample.

Per sample:

    operations/s = 1e9 / latency_ns

    returned bytes/s =
        returned_bytes * 1e9 / latency_ns

    returned MiB/s =
        returned bytes/s / 1048576

    processed bytes/s =
        processed_bytes * 1e9 / latency_ns

    processed MiB/s =
        processed bytes/s / 1048576

For `reader_v1` and `direct_nohash_reference`, processed bytes are the
bounded serialized-object bytes.

For `whole_segment_hash_reference`, processed bytes are the entire
segment length.

Actual returned bytes are measured from the operation's return object
where a byte/string-like return exists; otherwise zero is recorded.

## Required Reporting

The permanent result must contain:

- all raw samples;
- normal batch records;
- micro-dispatch records;
- thermal and cpufreq observations;
- affinity transitions;
- cooldown records;
- per-CPU statistics;
- per-cluster statistics;
- per-lane statistics;
- per-mode statistics;
- per-fixture/object-size statistics;
- pooled statistics;
- cluster-1 versus cluster-0 size-specific crossover evidence.

Statistics must include latency and throughput.

Cluster-1 results must never be silently pooled with cluster 0.

Raw samples remain authoritative over all summaries.

## Failure Evidence

The benchmark is exact-once.

No automatic retry is permitted.

A first fatal execution result is permanent historical evidence.

If failure occurs after useful evidence has been collected, the fatal
result must preserve, when available:

- completed raw samples;
- completed batch/dispatch records;
- affinity transitions;
- cooldown evidence;
- topology;
- governing and excluded thermal zones;
- CPU baselines and limits;
- current workload unit;
- original affinity;
- affinity-restoration status;
- original execution exception;
- distinct affinity-restoration exception.

An affinity-restoration failure must never overwrite the original
benchmark exception.

## File and Storage Rules

Benchmark operations are read-only except for final exclusive JSON result
publication.

No source GGUF write is allowed.

No segment write is allowed.

No sysfs write is allowed.

No cleanup or deletion is allowed.

No mmap/fd-cache production claim is made.

## Exact-Once Publication

Result path:

    experiments/model_fractal/maf_segment_reader_benchmark_v1_1.json

Schema:

    openmind.maf_segment_reader_benchmark.v1_1

The result must be created with exclusive-create semantics.

If the result already exists, execution must stop before benchmark load.

## Interpretation Boundary

This benchmark may establish device-specific, fixture-specific evidence
for:

- Segment Reader latency;
- Segment Reader throughput;
- reference-mode overhead;
- CPU0/CPU3 normal-lane behavior;
- CPU6/CPU7 small-object behavior;
- object-size crossover;
- thermal behavior under the preregistered policy.

It does not establish:

- universal CPU safety;
- production storage-engine selection;
- production scheduler correctness;
- Phase 6C concurrency;
- multithreaded scaling;
- MAF-native LLM replacement;
- selective tensor avoidance;
- generalization beyond the tested device, files and runtime.
