# OpenMind CPU Thermal Characterization V1.2 Completion

Status: COMPLETE / RAW RESULT FROZEN / DO NOT RERUN

## Frozen Evidence

- Protocol SHA256: `b98e4c4d7309948b0fbf71f4a961e038a7e55470f03153e85ec724ffd32f3cbb`
- Runner SHA256: `19218eaf8fe98a6bcbf6f465f9f0d5320d8fb42f6b3937bbfcc5b4a29a78c2f2`
- Result SHA256: `b2e587547ed2b7388f141210fb3de5873de7a9d61b1ca3273ec4e4a964eaa8b2`
- Raw result freeze commit: `ae6b260`
- Exact-once execution parent: `569225c`
- Schema: `openmind.cpu_thermal_characterization.v1_2`
- `characterization_valid`: `true`
- Fatal execution error: none
- Affinity-restoration error: none

V1 and V1.1 were superseded before execution.

**CPU Thermal Characterization V1.2 must never be rerun.**

## Result Coverage

- CPU profiles: 8/8
- Profile order: `0,6,1,7,2,3,4,5`
- Total staircase stages recorded: 44
- Confirmed CPUs: 2
- Not-confirmed CPUs: 6
- Governing thermal zones: 20
- Excluded trip/threshold zones: 2
- Excluded types: `cpu-hw-trip-0;cpu-hw-trip-1`
- Affinity-transition records: 11
- Transition kinds: `bridge`=3, `bridge_to_target`=3, `direct`=4, `initial_pin`=1
- Bridge cooldown records: 3

## Per-CPU Outcome

| CPU | Cluster | Baseline C | Optimal ceiling C | Hard ceiling C | Stages | Preliminary ms | Confirmation | Confirmed ms | Recorded duty |
|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|
| 0 | 0 | 41.1 | 46.1 | 49.1 | 6 | 250 | CONFIRMED | 250 | 1.0 |
| 6 | 1 | 42.6 | 47.6 | 50.6 | 3 | - | NOT_CONFIRMED | - | - |
| 1 | 0 | 42.6 | 47.6 | 50.6 | 6 | 500 | NOT_CONFIRMED | - | - |
| 7 | 1 | 41.1 | 46.1 | 49.1 | 2 | - | NOT_CONFIRMED | - | - |
| 2 | 0 | 46.5 | 51.5 | 54.5 | 7 | 8000 | NOT_CONFIRMED | - | - |
| 3 | 0 | 40.3 | 45.3 | 48.3 | 6 | 250 | CONFIRMED | 250 | 1.0 |
| 4 | 0 | 41.5 | 46.5 | 49.5 | 7 | 500 | NOT_CONFIRMED | - | - |
| 5 | 0 | 43.8 | 48.8 | 51.8 | 7 | 4000 | NOT_CONFIRMED | - | - |

## Confirmed Normal Workload Lane

Only CPU0 and CPU3 reproduced a thermally eligible preliminary window during the independent confirmation cycle.

- CPU0 confirmed active window: **250 ms**
- CPU3 confirmed active window: **250 ms**
- CPU0 observed 250 ms workload throughput: **1803.1 operations/s ≈ 1803.1 MiB/s**
- CPU3 observed 250 ms workload throughput: **1824.0 operations/s ≈ 1824.0 MiB/s**

The MiB/s equivalence applies only to this characterization because each operation processes exactly one 1 MiB buffer.

The recorded duty value of 1.0 for CPU0/CPU3 describes the observed confirmation cycle only. It is not evidence of universal indefinite 100% duty safety.

## Unconfirmed Cool-Start Windows

Longer preliminary windows on CPU1, CPU2, CPU4 and CPU5 did not survive independent confirmation.

They are preserved as cool-start/sprint evidence and must not be treated as validated sustained operating windows.

- CPU1 preliminary: 500 ms; not confirmed
- CPU2 preliminary: 8000 ms; confirmation hard-stopped
- CPU4 preliminary: 500 ms; not confirmed
- CPU5 preliminary: 4000 ms; confirmation hard-stopped

## Cluster 1 — Prospective Micro-Fragment Lane

CPU6 and CPU7 showed high short-burst throughput but did not produce a thermally eligible sustained stage under the frozen characterization criterion.

- CPU6 100 ms observed throughput: **2476.4 operations/s ≈ 2476.4 MiB/s**; thermally ineligible.
- CPU7 100 ms observed throughput: **2486.0 operations/s ≈ 2486.0 MiB/s**; thermally ineligible.

Therefore cluster 1 is **not validated for a fixed sustained time window**.

For Segment Reader Benchmark V1.1, CPU6/CPU7 may instead be tested as a prospective **micro-fragment / small-object lane**:

1. Dispatch one bounded fragment or small serialized object.
2. Record latency, operations/s, returned bytes/s and returned MiB/s.
3. Observe thermal state immediately around the dispatch.
4. Do not run a sustained cluster-1 batch merely because the object is small.
5. Alternate CPU6 and CPU7 where the benchmark design permits.
6. Report CPU6 and CPU7 separately from cluster 0.
7. Treat this as a hypothesis being validated, not a previously validated safe routing rule.

## Segment Reader Benchmark V1.1 Scheduling Policy

### Normal lane

- Primary CPUs: **CPU0 and CPU3**
- Cluster: **0**
- Active workload batch ceiling: **250 ms**
- Preserve <=100 ms thermal observation granularity.
- Preserve cross-cluster bridge/cooldown governance.

### Micro-fragment candidate lane

- Candidate CPUs: **CPU6 and CPU7**
- Cluster: **1**
- Work unit: one bounded small fragment/object per dispatch.
- No preregistered sustained time window is claimed.
- Thermal eligibility and performance must be established by Segment Reader Benchmark V1.1 itself.

The benchmark must determine whether object/fragment size creates a crossover where cluster 1's higher short-burst throughput is useful without unacceptable thermal escalation.

## Required Benchmark Reporting

Segment Reader Benchmark V1.1 must report, at minimum:

- raw latency samples
- operations/s
- returned bytes/s
- returned MiB/s
- whole-segment processed bytes/s and MiB/s for whole-segment modes
- per-CPU metrics
- per-cluster metrics
- pooled metrics
- object/fragment size
- CPU placement
- thermal observations
- frequency observations
- hard-stop/cooldown events

Cluster-1 measurements must never be silently pooled with cluster 0.

## Evidence Limitation

The successful V1.2 JSON does not contain an explicit top-level `affinity_restored` field.

No affinity-restoration exception was recorded, but absence of that exception is not equivalent to an explicit success-path restoration record.

This is a reporting limitation of the frozen first result. It does not authorize rerunning V1.2.

## Interpretation

**Validated:** CPU0 and CPU3 provide reproducible 250 ms thermally eligible workload windows under the frozen characterization.

**Observed but not sustained-validated:** CPU6 and CPU7 provide higher short-burst workload throughput while rapidly exceeding the thermal eligibility envelope.

**Prospective:** use real MAF fragment/object size as a routing dimension and test whether CPU6/CPU7 are advantageous for sufficiently small individual reads.

No production CPU-routing claim is made.
No Phase 6C concurrency claim is made.
No multithreaded-performance claim is made.

## Next Step

Preregister Segment Reader Benchmark V1.1 using this two-lane CPU policy, then perform static and live preflight before its single exact-once execution.

Segment Reader Benchmark V1 remains frozen and unexecuted.
Phase 6C remains not started.
No upstream push is authorized by this completion record.
