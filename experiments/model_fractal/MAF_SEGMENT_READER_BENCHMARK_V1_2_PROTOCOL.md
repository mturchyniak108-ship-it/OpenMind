# OpenMind MAF Segment Reader Benchmark V1.2 Protocol

Status: PREREGISTERED SUCCESSOR / UNEXECUTED / EXACT-ONCE

## Purpose

MAF Segment Reader Benchmark V1.2 is the minimal corrective successor to the
executed MAF Segment Reader Benchmark V1.1.

V1.1 was invoked exactly once and produced a permanent pre-measurement failure
record. It recorded zero raw samples, zero normal-lane batches and zero
micro-lane dispatches. V1.1 must never be rerun or modified.

V1.2 exists only to correct the confirmed construction defect that prevented
V1.1 from reaching measurement.

## Frozen V1.1 Evidence

- V1.1 protocol:
  `experiments/model_fractal/MAF_SEGMENT_READER_BENCHMARK_V1_1_PROTOCOL.md`
- V1.1 protocol SHA256:
  `8a6af3a65c78c0ed9f47244ebd40613c5e84f13fc2e4e2d1543089e5481e3770`
- V1.1 runner:
  `experiments/model_fractal/benchmark_maf_segment_reader_v1_1.py`
- V1.1 runner SHA256:
  `d1e17670aad32dbb57deb29e588aad656735ff60582202f4436b5db2b89bda69`
- V1.1 exact-once result:
  `experiments/model_fractal/maf_segment_reader_benchmark_v1_1.json`
- V1.1 result SHA256:
  `a4f31246e5412110487abac7b0304c16fd9528b48b22e882be6c6c5b48feb2e3`
- V1.1 result schema:
  `openmind.maf_segment_reader_benchmark.v1_1`
- V1.1 benchmark_valid:
  `false`
- V1.1 fatal error:
  `NameError: name 'runtime_state' is not defined`
- V1.1 raw samples:
  `0`
- V1.1 normal batches:
  `0`
- V1.1 micro dispatches:
  `0`

The V1.1 result is failure evidence only. It contains no latency, throughput,
thermal-performance or crossover evidence.

## Normative Base

Except for the explicitly enumerated V1.2 deltas below, every experimental,
measurement, scheduling, thermal, CPU-placement, fixture, reporting,
failure-evidence and interpretation requirement in frozen MAF Segment Reader
Benchmark V1.1 protocol SHA256 `8a6af3a65c78c0ed9f47244ebd40613c5e84f13fc2e4e2d1543089e5481e3770` is incorporated into V1.2
without change.

This includes, without modification:

- Phase 6B scope and Phase 6C exclusion.
- Frozen Segment Reader V1 measurement core.
- Normal lane CPUs CPU0 and CPU3 on cluster 0.
- Normal lane modes:
  `reader_v1`, `direct_nohash_reference`,
  `whole_segment_hash_reference`.
- Normal active-work batch ceiling of 250 ms.
- 100 ms individual-operation thermal observation-gap limit.
- Prospective micro lane CPUs CPU6 and CPU7 on cluster 1.
- Exactly one bounded serialized-object operation per micro dispatch.
- Micro modes:
  `reader_v1`, `direct_nohash_reference`.
- Deterministic CPU6/CPU7 alternation where possible.
- Relative small-object fixture selection:
  sort by serialized object length then stable fixture identifier;
  select `ceil(N/2)`, cap at 8, minimum one when non-empty.
- CPU Thermal Characterization V1.2 sensor-selection policy.
- Initial execution temperature below 75 C.
- Per-CPU eligibility ceiling:
  `min(baseline + 5 C, 75 C)`.
- Per-CPU hard stop:
  `min(baseline + 8 C, 80 C)`.
- Global resume threshold:
  `min(initial benchmark baseline + 3 C, 70 C)`.
- Two-second cooldown polling and 120-second maximum cooldown.
- Cross-cluster bridge/cooldown governance.
- Immediate cluster-0 relief surrounding cluster-1 micro dispatches.
- Timing only the target measurement-mode call.
- Raw latency in nanoseconds as authoritative evidence.
- All V1.1 throughput definitions.
- All raw-sample reporting fields.
- Per-CPU, per-cluster, per-lane, per-mode, per-fixture and pooled summaries.
- Cluster-1 versus cluster-0 size-specific crossover evidence.
- Exact-once result publication.
- Preservation of partial failure evidence.
- Distinct preservation of benchmark and affinity-restoration exceptions.
- Read-only benchmark source behavior.
- No GGUF, segment or sysfs writes.
- No production storage-engine, scheduler, concurrency or replacement-model
  claims.

## V1.2 Delta 1 — Confirmed Defect Correction

Frozen V1.1 `fixture_json()` contains this erroneous statement:

`runtime_state["current_workload_unit"] = None`

`fixture_json()` has no `runtime_state` parameter, no enclosing lexical binding
for that name and no module-level binding. Python therefore resolves that load
as an unbound global and V1.1 terminated with `NameError` while constructing
post-run/common evidence before any measurement began.

V1.2 removes exactly that erroneous statement from `fixture_json()`.

No replacement statement is added there.

## V1.2 Delta 2 — Nested Dispatch Is Not Modified

The nested `dispatch()` inside `run_micro_lane()` references `runtime_state`
through a valid Python lexical closure over the enclosing
`run_micro_lane(..., runtime_state=...)` parameter.

Closure-aware analysis confirmed that the nested symbol is a free variable
bound by the enclosing function.

V1.2 therefore preserves this dispatch closure unchanged.

## V1.2 Delta 3 — Version Identities

V1.2 uses:

- Protocol:
  `experiments/model_fractal/MAF_SEGMENT_READER_BENCHMARK_V1_2_PROTOCOL.md`
- Runner:
  `experiments/model_fractal/benchmark_maf_segment_reader_v1_2.py`
- Result:
  `experiments/model_fractal/maf_segment_reader_benchmark_v1_2.json`
- Result schema:
  `openmind.maf_segment_reader_benchmark.v1_2`

The V1.2 result path must be absent before any benchmark dependency module or
fixture is loaded.

The V1.1 result remains immutable historical evidence and must remain present
with its frozen SHA256 before V1.2 is eligible to execute.

## V1.2 Delta 4 — Direct Predecessor Identity Binding

The V1.2 runner must verify before dependency loading:

1. this V1.2 protocol identity;
2. frozen V1.1 protocol SHA256;
3. frozen V1.1 runner SHA256;
4. frozen V1.1 exact-once failure-result SHA256;
5. all previously frozen V1.1 dependency identities.

V1.2 must refuse execution if any predecessor identity differs.

## V1.2 Delta 5 — Stronger Static Scope Audit

Before V1.2 is frozen for execution, static audit must use Python lexical
symbol-table semantics rather than a simple per-function load/store scan.

At minimum it must demonstrate:

- zero referenced global names that are absent from the module namespace and
  Python builtins;
- `fixture_json()` has no `runtime_state` reference;
- `run_micro_lane()` has `runtime_state` as a parameter;
- nested `dispatch()` resolves `runtime_state` as a free variable;
- no forbidden V1 calls to `main()`, `run_benchmark()` or `measure_all()`;
- V1.2 syntax compiles without executing the runner.

This stronger audit is a preregistration requirement and not an optional
diagnostic.

## Exact-Once Rule

V1.2 is unexecuted at protocol construction time.

After V1.2 protocol and runner are frozen, live preflight and final execution
authorization must occur before a single invocation.

If V1.2 is invoked, that invocation is permanent historical evidence whether
successful or fatal.

V1.2 must not be retried under the same version.

Any later construction defect requires another explicitly preregistered
successor.

## Interpretation Boundary

A successful V1.2 may establish only the claims already permitted by frozen
V1.1.

The V1.1 failure establishes no MAF performance result.

V1.2 does not retroactively convert V1.1 into a successful benchmark and does
not erase, replace or modify its failure evidence.

Phase 6C remains not started.
No multithreaded-performance claim is made.
No MAF-native LLM replacement claim is made.
