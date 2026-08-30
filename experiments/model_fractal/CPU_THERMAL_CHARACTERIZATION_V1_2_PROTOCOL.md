# OpenMind CPU Thermal Characterization V1.2 Protocol

Status: PREREGISTERED / NOT EXECUTED

## V1.2 Supersession

V1.1 was frozen but never executed.

Its final execution-safety preflight proved that live sensor selection,
thermal governance, cross-cluster bridge cooldowns, affinity
restoration structure and exact-once publication were valid.

That same preflight found one remaining exact-once evidence defect:

    a mid-run exception could occur after useful characterization
    evidence had already been accumulated, but fatal_result() retained
    only the exception type and message.

Because automatic retry is forbidden, discarding already accumulated
evidence would make the permanent failure result incomplete.

V1.2 therefore supersedes V1.1 before any CPU characterization load.

V1.2 must preserve, when available at the time of failure:

- every fully completed CPU profile;
- fully completed staircase stages for the currently active CPU;
- a completed confirmation result if it has already returned;
- completed affinity transitions;
- completed bridge-cooldown evidence;
- frozen topology and thermal-zone selection context;
- original affinity;
- whether original affinity was successfully restored;
- the original execution exception;
- a distinct affinity-restoration exception if restoration itself also
  fails.

An affinity-restoration failure must never overwrite or hide the
original workload exception.

V1.2 does not fabricate evidence for an operation that had not yet
returned a complete record when the exception occurred.

V1 and V1.1 remain preserved unchanged and permanently unexecuted.

## Supersession

V1 was frozen but never executed.

Its final execution preflight correctly blocked execution because the
original keyword-based thermal selector included:

    cpu-hw-trip-0
    cpu-hw-trip-1

Read-only sensor diagnostics established that these are trip-threshold
style zones rather than governing live-temperature sensors.

Observed evidence before this V1.1 preregistration:

    cpu-hw-trip-0:
        reported temperature = 105000 mC
        two-second delta = 0 mC
        exposed trip point = 105000 mC

    selected non-trip zones:
        count = 20
        all 20 changed over the same passive observation interval
        observed maximum = 40700 mC

V1.1 therefore supersedes V1 before any characterization workload.

V1 remains preserved unchanged and permanently unexecuted.

## Purpose

Characterize the usable single-CPU operating window of every exposed
logical CPU on the current Android device.

Thermal tolerance is the primary optimization criterion.

Peak instantaneous speed does NOT determine the selected operating
window.

The result will be used to choose workload batch length, CPU rotation,
cooldown and affinity policy for later OpenMind benchmarks.

## Known Topology

Discovery before preregistration established:

    logical CPUs = 8

    cluster 0:
        cpu0,cpu1,cpu2,cpu3,cpu4,cpu5

    cluster 1:
        cpu6,cpu7

The runner must rediscover and verify this topology before loading a CPU.

The device does not expose physical X/Y die coordinates.

"Farthest" therefore means:

    opposite exposed topology cluster

No literal physical-distance claim is permitted.

## Workload

Use a deterministic single-thread CPU-bound SHA-256 workload.

Buffer size:

    1 MiB

The buffer is allocated before timed work.

Each operation hashes the complete fixed buffer.

This workload is a thermal characterization workload.

It is NOT claimed to represent every possible OpenMind workload or the
absolute maximum capability of the CPU.

## CPU Pinning

Use:

    os.sched_getaffinity
    os.sched_setaffinity

Only one logical CPU is eligible during an active test stage.

The original process affinity must always be restored in `finally`.

No CPU hotplugging is permitted.

No cpufreq, governor, thermal, scheduler or sysfs control may be
modified.

Sysfs is read-only evidence.

## Cross-Cluster Movement

After a logical CPU test, movement to another single-CPU affinity must
cross topology clusters.

If the next CPU requiring characterization belongs to the same cluster
as the just-tested CPU, first move to an idle bridge CPU in the
opposite cluster and cool there.

The following move from the bridge CPU to the next test CPU therefore
also crosses clusters.

Bridge CPUs perform no characterization workload while acting as a
cooldown destination.

This prevents intentional repeated localized loading on one topology
group.

## Thermal Sensor Selection

Read:

    /sys/class/thermal/thermal_zone*

Accept only plausible readings:

    0 C <= temperature <= 120 C

First classify trip/threshold-style zones.

Exclude from the governing live-temperature set any thermal-zone type
whose lowercase name contains:

    trip
    threshold
    thresh

Excluded zones are NOT discarded.

Their identities remain preserved in the raw result as diagnostic
evidence, but their temperature values cannot govern baseline,
cooldown, optimal-envelope or hard-stop decisions.

From the remaining live candidates, prefer thermal-zone types
containing:

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

If no preferred live candidate exists, fall back to every remaining
plausible non-trip live candidate and record the fallback.

Execution is invalid if no plausible non-trip live candidate remains.

The maximum selected NON-TRIP live-temperature reading is the governing
temperature.

This rule exists specifically to prevent static hardware trip thresholds
from masquerading as current silicon temperature.

## Initial Thermal Preconditions

Record an initial global thermal baseline.

Execution is forbidden if the baseline is at or above:

    75 C

Between CPU tests, cool until the governing temperature is at or below:

    min(
        initial_global_baseline + 3 C,
        70 C
    )

Maximum cooldown wait:

    120 seconds

Thermal polling interval:

    2 seconds

Failure to cool is permanent negative evidence and does not authorize a
rerun.

## Thermal Tolerance — Primary Selection Rule

For each CPU, after pre-test cooldown, record a CPU-specific baseline.

### Optimal envelope

A workload stage is thermally eligible only when its peak governing
temperature is at or below BOTH:

    CPU baseline + 5 C

and:

    75 C

Therefore:

    optimal_limit =
        min(
            cpu_baseline + 5 C,
            75 C
        )

### Hard stop

Stop active characterization on that CPU when temperature reaches or
exceeds:

    hard_limit =
        min(
            cpu_baseline + 8 C,
            80 C
        )

A hard stop preserves every sample already collected.

No hotter stage may be attempted for that CPU.

## Staircase

Candidate active-work durations:

    100 ms
    250 ms
    500 ms
    1 second
    2 seconds
    4 seconds
    8 seconds

Stages execute in ascending order.

Between stages:

    0.5 second passive rest

No sample is discarded because it is slow or hot.

The active workload is divided into epochs no longer than:

    100 ms

Thermal state is read between epochs, never inside an individual hash
operation.

This permits early thermal stopping without forcing an entire long
stage to complete.

## Latency and Throughput

For every active epoch preserve:

- active elapsed nanoseconds;
- operations completed;
- bytes processed;
- nanoseconds per operation;
- operations per second;
- bytes per second;
- MiB per second;
- governing temperature after the epoch;
- CPU;
- topology cluster;
- stage;
- frequency snapshot.

For distributions report:

- minimum;
- maximum;
- mean;
- median;
- nearest-rank p95.

Latency and throughput are peer metrics.

## Thermal Metrics

For every stage derive:

- baseline temperature;
- peak temperature;
- ending temperature;
- temperature rise;
- active work time;
- wall time;
- thermal rise per active second;
- operations;
- bytes processed;
- operations/second;
- MiB/second;
- MiB processed per degree Celsius of rise when rise is positive.

## Primary Optimal-Usage Selection

For each CPU:

1. consider only fully completed stages;
2. reject every stage exceeding the optimal thermal envelope;
3. select the LONGEST remaining stage.

Therefore thermal tolerance decides the operating window.

Throughput does not permit selection of a thermally ineligible stage.

If no stage is eligible, that CPU has no validated operating window
under this protocol.

## Confirmation Cycle

After selecting the preliminary operating window:

1. cool back to the global resume threshold;
2. rerun that selected duration exactly once;
3. apply the same CPU-specific +5 C / 75 C optimal envelope;
4. apply the +8 C / 80 C hard stop;
5. preserve all confirmation evidence;
6. cool back to the global resume threshold and measure recovery time.

No confirmation retry is permitted.

If confirmation violates the thermal envelope, the CPU is classified:

    NOT_CONFIRMED

The protocol does not silently select a faster/hotter alternative.

## Sustainable Duty Cycle

For a confirmed CPU derive:

    active_seconds =
        confirmed active workload duration

    recovery_seconds =
        time from confirmation completion until global resume
        temperature is restored

    duty_cycle =
        active_seconds
        /
        (active_seconds + recovery_seconds)

This is a characterization of the tested conditions only.

## Frequency Evidence

Read, where available:

- scaling_cur_freq;
- scaling_min_freq;
- scaling_max_freq;
- cpuinfo_min_freq;
- cpuinfo_max_freq;
- scaling_governor.

Record frequency evidence before and after every stage and confirmation.

Frequency behavior is secondary evidence.

Thermal tolerance remains the deciding factor for optimal usage.

## CPU Summary

For every logical CPU report:

- cluster;
- baseline temperature;
- optimal thermal limit;
- hard thermal limit;
- longest thermally eligible stage;
- confirmation status;
- confirmed active-work window;
- recovery time;
- sustainable duty cycle;
- latency statistics;
- operations/second statistics;
- bytes/second statistics;
- MiB/second statistics;
- thermal rise rate;
- thermal efficiency;
- observed frequencies;
- hard-stop status.

## Cross-CPU Summary

Rankings may be reported for:

- confirmed active window;
- sustainable duty cycle;
- median operations/second;
- median MiB/second;
- MiB per degree rise.

However no ranking can override thermal eligibility.

## Exact-Once Rule

Result must be absent before execution.

The frozen V1.2 runner may execute exactly once.

No automatic retry is permitted.

The first result or fatal error is permanent historical evidence.

## Result

Result path:

    experiments/model_fractal/cpu_thermal_characterization_v1_2.json

Schema:

    openmind.cpu_thermal_characterization.v1_2

Publication must use exclusive create.

## Claim Boundary

This characterization does NOT establish:

- literal physical die spacing;
- prevention or measurement of semiconductor wear;
- universal CPU safety limits;
- permanent device thermal properties;
- multithreaded scaling;
- GPU behavior;
- production performance;
- Segment Reader performance.

It establishes a conservative thermal scheduling profile for this
device under this exact synthetic workload and observed conditions.

## Downstream Use

After V1.2 interpretation, the confirmed per-CPU operating windows
and cooldown behavior are inputs to:

    Segment Reader Benchmark V1.1

Later multithreading remains:

    Phase 6C:
        concurrency/thread-safety contract

    Phase 6D:
        topology/locality-aware architecture

    Phase 6F:
        multithreaded performance implementation and scaling
