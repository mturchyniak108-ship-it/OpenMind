# MAF Segment Locality Runtime Telemetry Integration V1 Protocol

Status: PREREGISTERED / IMPLEMENTATION NOT STARTED / VALIDATION NOT AUTHORIZED

Phase: 6D — Segment Locality and Path-Aware Repacking

Artifact class: prospective implementation protocol

Scientific result: NONE

Performance verdict: NONE

Benchmark authorized: NO

Real-model telemetry collection authorized: NO

Repack planner authorized: NO

Repack realization authorized: NO

Phase 6D-Q authorized: NO

## 1. Purpose

This protocol prospectively defines the first integration boundary between the
frozen Phase 6C MAF Object Runtime and Residency implementation and the frozen
Phase 6D telemetry data model.

The purpose is to observe real runtime operations and translate them
deterministically into the already validated Phase 6D `TelemetryEvent` /
`TelemetryAccumulator` contract without modifying Phase 6C runtime semantics or
canonical MAF authority.

This protocol freezes integration semantics before implementation.

Freezing this protocol is not a scientific result.

## 2. Frozen parent authority

Repository parent commit:

`b3929a2c712228374b8daf30bff99b47775dadd7`

Branch:

`labs/multidimensional-maf`

Current ROADMAP SHA256 at preregistration:

`50ecfa32aa64e5b0b8b0a1e8f0fbc9802de537284ca36aa9f1594bcc6ea4c94c`

Phase 6D remains ACTIVE RESEARCH.

## 3. Frozen Phase 6C authority

Frozen runtime implementation:

`experiments/model_fractal/maf_object_runtime_residency_v1.py`

SHA256:

`4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9`

Frozen runtime protocol SHA256:

`81987d00ef4cb51556dcebf08bff9c9fa8979f033df05304d347b759e545eb13`

Frozen Phase 6C formal verdict SHA256:

`800fd8e6e58d2af7ea46133e2e6a26d3b380fa4abd371f055324f722ad92784f`

Phase 6C is CLOSED / PASS and MUST NOT be reopened or edited by this work.

## 4. Frozen Phase 6D telemetry authority

Frozen locality data-model implementation SHA256:

`5432f2d74a610f2d0f9181e9af146013bb198a4e837af634993909358fff8ad0`

Frozen locality data-model protocol SHA256:

`712caa2e7dfc948f607a4c8d68064fc838eb1f58701fc5206c52aaf8e6492bc4`

Frozen locality data-model Validation V1 raw-result SHA256:

`9aa2e467dc451b2d2122802e1e8b8fabf616db756a36b53a3600cca793923b4d`

Frozen locality data-model formal-verdict SHA256:

`7754c9d5dada8dc214a21236827c64cafea880e4b0c679cd84c9c4833fd3e9db`

The existing ten telemetry event kinds and accumulator semantics are
authoritative and MUST NOT be modified by Integration V1.

## 5. Frozen persistence authority

Frozen Telemetry Snapshot Persistence V1.1 implementation SHA256:

`cb1e2e3dc11006c75e38e33c941b39959aa4d99f971de9e08250d8b995fe09b0`

Frozen Persistence V1.1 protocol SHA256:

`511c995fd86998da33e47691db98794ddcda9e51ec3fd71794a2324ef2a53bba`

Accepted Persistence Validation V1.3 raw-result SHA256:

`042a0474e3ec9926d69cee1bda088427c23b121088a424c5c94b68f2510b2bff`

Accepted Persistence Validation V1.3 formal-verdict SHA256:

`a623507248a32c8384b5c00b509d1fe45c176eee4719527fbfb7b0e60db89322`

Persistence correctness is accepted.

Integration V1 does not perform persistence writes.

## 6. Frozen Phase 6D parent protocol

`MAF_SEGMENT_LOCALITY_REPACKING_V1_PROTOCOL.md` SHA256:

`a4c1a1d4fe22f7e714efa331cec9cf4dbd3a9e178f2b28b3ddb9034387e210ae`

Integration V1 inherits the parent requirements that telemetry is derived
evidence, never canonical model truth, and must not alter logical object
identity.

## 7. Required implementation namespace

The only authorized initial implementation path is:

`experiments/model_fractal/maf_segment_locality_runtime_telemetry_integration_v1.py`

The implementation MUST be a new module.

It MUST NOT edit:

- the frozen Phase 6C runtime;
- the frozen Phase 6D data model;
- telemetry persistence;
- generation authority;
- Segment Reader;
- Resident PK Directory.

## 8. Integration architecture

V1 MUST use composition.

The integration object wraps one existing frozen `MAFObjectRuntime` instance.

It MUST NOT:

- monkey-patch the runtime;
- mutate runtime module globals;
- replace runtime methods;
- inject callbacks into the runtime;
- subclass the runtime to override frozen behavior;
- alter runtime state-machine rules;
- alter runtime exception classes;
- alter runtime return values.

The intended public class name is:

`MAFSegmentLocalityRuntimeTelemetryAdapter`

## 9. Clean-attachment precondition

For scientifically valid V1 telemetry, the adapter MUST attach before runtime
use begins.

At adapter construction the wrapped runtime MUST be:

- open;
- bound to one model PK;
- bound to one generation PK;
- object count zero;
- active pin count zero;
- resident serialized bytes zero;
- resident dense bytes zero;
- all frozen runtime counters zero.

An already-used runtime is outside V1 scientific scope.

This requirement ensures the adapter observes every object registration and
every covered runtime operation from trace start.

## 10. Source manifest binding

The Phase 6C runtime binds model PK and generation PK but does not itself expose
canonical source-manifest SHA as a constructor argument.

Integration V1 therefore requires an explicit:

`source_manifest_sha256`

binding at adapter construction.

The adapter MUST instantiate the frozen `TelemetryAccumulator` with exactly:

- runtime model PK;
- runtime generation PK;
- the provided source-manifest SHA256.

No manifest identity may be inferred after telemetry collection.

## 11. Exact V1 telemetry event vocabulary

The event vocabulary remains exactly the frozen ten-kind data-model vocabulary:

1. `ACCESS`
2. `MATERIALIZATION`
3. `BYTES_READ`
4. `CACHE_HIT`
5. `CACHE_MISS`
6. `PROMOTION`
7. `DEMOTION`
8. `PREFETCH_ISSUED`
9. `PREFETCH_CONSUMED`
10. `PREFETCH_UNUSED`

Integration V1 MUST NOT add an eleventh event kind.

## 12. Logical event sequence

The first emitted V1 telemetry event has sequence:

`1`

Every subsequently committed telemetry event increments the sequence by exactly
one.

Sequence numbers are observer-local logical ordering.

Wall-clock time MUST NOT determine ordering.

No sequence number may be reused within a valid trace.

## 13. V1 ACCESS definition

V1 `ACCESS` means model-object demand through exactly these frozen runtime
resource APIs:

- `serialized_bytes(object_pk)`
- `dense_view(object_pk)`

The following are NOT V1 `ACCESS` events:

- `register_entry`;
- `state`;
- `transition`;
- `ensure_state`;
- `pin`;
- `unpin`;
- `snapshot`;
- `close`.

For a known object while the runtime is open:

- a successful resource request emits one `ACCESS`;
- a request ending in
  `MAFObjectRuntimeResidencyUnavailableError` also emits one `ACCESS`.

Unknown-object requests, closed-runtime requests, invalid arguments, and other
runtime errors do not emit `ACCESS`.

This freezes access counting as demand, not merely successful data return.

## 14. Named cache boundaries

V1 defines exactly two named derived residency-cache boundaries:

`runtime.serialized_residency`

and

`runtime.dense_residency`

These names are frozen.

They describe Phase 6C runtime residency only.

They MUST NOT be described as:

- CPU hardware cache;
- filesystem page cache;
- operating-system cache;
- GPU cache;
- model KV cache.

## 15. Serialized-residency cache semantics

For a valid known-object call to:

`serialized_bytes(object_pk)`

emit, in order:

1. `ACCESS`;
2. one cache outcome.

If the call returns frozen verified serialized bytes:

`CACHE_HIT(cache_name="runtime.serialized_residency")`

If the call raises
`MAFObjectRuntimeResidencyUnavailableError`:

`CACHE_MISS(cache_name="runtime.serialized_residency")`

No other failure class produces a cache outcome.

## 16. Dense-residency cache semantics

For a valid known-object call to:

`dense_view(object_pk)`

emit, in order:

1. `ACCESS`;
2. one cache outcome.

If the call returns a dense view:

`CACHE_HIT(cache_name="runtime.dense_residency")`

If the call raises
`MAFObjectRuntimeResidencyUnavailableError`:

`CACHE_MISS(cache_name="runtime.dense_residency")`

No other failure class produces a cache outcome.

## 17. V1 BYTES_READ definition

V1 `BYTES_READ` measures serialized object bytes successfully read through the
frozen Segment Reader and committed into runtime HOT_MAF residency.

It does not count ordinary reads from already resident RAM.

For every committed primitive transition:

`MAPPED -> HOT_MAF`

Integration V1 emits exactly one:

`BYTES_READ`

whose `byte_count` equals the frozen registered `ResidentPKEntry.length`.

A failed verified read or failed promotion that does not commit HOT_MAF emits no
V1 `BYTES_READ`.

Therefore V1 does not claim complete physical-I/O accounting for failed reads.

## 18. V1 MATERIALIZATION definition

For every committed primitive transition:

`HOT_MAF -> HOT_DENSE`

Integration V1 emits exactly one:

`MATERIALIZATION`

for that object.

A dense-materializer attempt that fails before HOT_DENSE commit emits no
`MATERIALIZATION`.

## 19. Promotion semantics

Every committed primitive upward Phase 6C state transition emits exactly one
`PROMOTION` with exact frozen state names.

The upward primitive transitions are:

- `COLD_DISK -> MAPPED`
- `MAPPED -> HOT_MAF`
- `HOT_MAF -> HOT_DENSE`

No skipped-state promotion event is permitted.

## 20. Demotion semantics

Every committed primitive downward Phase 6C state transition emits exactly one
`DEMOTION`.

The downward primitive transitions are:

- `HOT_DENSE -> HOT_MAF`
- `HOT_MAF -> MAPPED`
- `MAPPED -> COLD_DISK`

No skipped-state demotion event is permitted.

## 21. Per-primitive event ordering

For a committed:

`COLD_DISK -> MAPPED`

emit:

1. `PROMOTION`

For a committed:

`MAPPED -> HOT_MAF`

emit:

1. `BYTES_READ`
2. `PROMOTION`

For a committed:

`HOT_MAF -> HOT_DENSE`

emit:

1. `MATERIALIZATION`
2. `PROMOTION`

For each committed downward primitive transition emit:

1. `DEMOTION`

This ordering is frozen before implementation.

## 22. Multi-step runtime operations

`ensure_state` and `pin` may cause multiple primitive transitions.

Integration V1 MUST represent the exact committed primitive path in frozen
Phase 6C state-machine order.

A call that moves:

`COLD_DISK -> HOT_DENSE`

therefore produces the event groups for:

1. `COLD_DISK -> MAPPED`;
2. `MAPPED -> HOT_MAF`;
3. `HOT_MAF -> HOT_DENSE`.

The adapter MUST NOT collapse this into one synthetic promotion.

## 23. Partial failure semantics

A Phase 6C multi-step operation may commit one or more primitive transitions
before a later primitive fails.

Integration V1 MUST compare authoritative runtime state before and after the
delegated call and emit telemetry only for primitive transitions proven to have
committed.

If the runtime commits:

`COLD_DISK -> MAPPED -> HOT_MAF`

and the attempted `HOT_MAF -> HOT_DENSE` materialization then fails, telemetry
records the first two committed primitives and MUST NOT record the failed third
primitive.

The original runtime exception remains authoritative.

## 24. No-commit failures

A failed operation that leaves runtime state unchanged emits no:

- `BYTES_READ`;
- `MATERIALIZATION`;
- `PROMOTION`;
- `DEMOTION`.

Resource-demand ACCESS/cache semantics remain governed separately by Sections
13 through 16.

## 25. Registration tracking

A successful adapter-mediated `register_entry(entry)` records the exact
registered:

- object PK;
- serialized length;
- registration order.

It emits no telemetry event.

The registered length is the authority used for committed HOT_MAF
`BYTES_READ`.

A failed registration records nothing.

Direct registration through the wrapped runtime during a scientific trace
invalidates the trace.

## 26. Close semantics

`close()` remains the frozen Phase 6C close operation.

Integration V1 MUST delegate to runtime close and MUST NOT alter its behavior.

For telemetry purposes, committed close demotions are represented as the
equivalent frozen primitive downward transitions.

When multiple registered objects are closed, event groups are emitted in exact
adapter registration order.

Close does not emit ACCESS.

## 27. Calls that emit no telemetry

Successful calls to these APIs emit no V1 telemetry unless they cause committed
residency transitions under another section:

- `register_entry`;
- `state`;
- `snapshot`;
- `unpin`.

`transition`, `ensure_state`, and `pin` emit only their committed residency /
read / materialization events.

## 28. Prefetch boundary

The frozen Phase 6C runtime has no prefetch API.

Integration V1 therefore emits:

- zero `PREFETCH_ISSUED`;
- zero `PREFETCH_CONSUMED`;
- zero `PREFETCH_UNUSED`.

A valid V1 snapshot has an empty prefetch aggregate surface unless a separately
prospectively preregistered runtime successor introduces real prefetch behavior.

V1 MUST NOT simulate prefetch events.

## 29. Runtime-outcome authority

The wrapped Phase 6C runtime executes before telemetry interpretation of its
outcome.

The adapter MUST preserve the runtime outcome.

For successful runtime calls, the adapter returns the exact delegated result
without semantic transformation.

For failed runtime calls, the adapter re-raises the original runtime exception
type and preserves its message.

Telemetry MUST NOT convert:

- runtime success into runtime failure;
- runtime failure into runtime success;
- one runtime failure class into another runtime failure class.

Exact Python traceback frame identity is not a V1 claim.

## 30. Telemetry-fault isolation

Telemetry is derived evidence and is subordinate to canonical runtime
authority.

If telemetry construction or `TelemetryAccumulator.add_event()` fails after a
runtime operation:

1. the runtime outcome remains authoritative;
2. the telemetry exception MUST NOT replace the runtime outcome;
3. the adapter enters a persistent faulted telemetry state;
4. scientific telemetry snapshot export becomes forbidden;
5. subsequent runtime delegation may continue;
6. no faulted trace may be used for repacking science.

The first telemetry fault type/message and a fault count may be retained as
derived diagnostics.

## 31. Snapshot API

The adapter preserves the frozen runtime:

`snapshot()`

meaning as a pass-through Phase 6C `RuntimeSnapshot`.

Integration V1 additionally exposes:

`telemetry_snapshot()`

which returns the frozen Phase 6D `TelemetrySnapshot` only when the integration
trace is valid and not faulted.

`telemetry_snapshot()` performs no filesystem write.

## 32. Persistence boundary

Integration V1 does not call the telemetry persistence implementation
automatically.

RAM aggregation and persistence remain separate operations.

A future real-model collection protocol may:

1. obtain a valid `telemetry_snapshot()`;
2. then explicitly pass it to the already validated persistence layer.

No runtime API call may synchronously persist a snapshot as part of each event.

## 33. Scientific trace integrity

During a scientific V1 integration trace, every covered Phase 6C runtime call
MUST pass through the adapter.

Direct calls to the wrapped runtime invalidate the trace because the adapter
cannot prove complete observation.

The implementation may provide diagnostics sufficient to detect only
adapter-visible violations; it MUST NOT claim impossible detection of arbitrary
external direct references.

Scientific callers are responsible for exclusive runtime routing during a V1
trace.

## 34. Single-thread V1 boundary

The frozen Phase 6D `TelemetryAccumulator` has not been validated as a shared
concurrent accumulator.

Integration V1 scientific validation and initial scientific telemetry
collection are therefore single-caller-thread only.

This protocol does not weaken Phase 6C runtime concurrency correctness.

It simply does not claim concurrent telemetry-adapter correctness.

A concurrent integration version requires separate prospective validation.

No Phase 6F performance claim is authorized.

## 35. Canonical-authority invariants

Enabling Integration V1 MUST NOT alter:

- model PK;
- generation PK;
- logical object PK;
- source manifest;
- object payload bytes;
- Resident PK Directory entries;
- segment bytes;
- active-generation authority;
- generation manifests;
- runtime state-machine legality;
- pin semantics;
- runtime budgets.

Telemetry remains discardable derived evidence.

## 36. Filesystem and network boundary

Importing or using Integration V1 for RAM telemetry MUST NOT:

- write files;
- create directories;
- delete files;
- invoke subprocesses;
- make network calls;
- activate generations.

Explicit persistence remains outside this integration module.

## 37. Implementation validation requirement

Implementation does not establish a scientific result.

Before scientific runtime telemetry collection, a separate prospective
validation protocol MUST be frozen.

The expected future validation protocol path is:

`experiments/model_fractal/MAF_SEGMENT_LOCALITY_RUNTIME_TELEMETRY_INTEGRATION_VALIDATION_V1_PROTOCOL.md`

The expected future validation runner path is:

`experiments/model_fractal/maf_segment_locality_runtime_telemetry_integration_validation_v1.py`

The expected future raw result path is:

`experiments/model_fractal/maf_segment_locality_runtime_telemetry_integration_validation_v1.json`

## 38. Mandatory future validation matrix

The separate Validation V1 protocol MUST test at minimum:

V01. exact frozen predecessor identity bindings;

V02. Phase 6C runtime bytes unchanged;

V03. Phase 6D data-model bytes unchanged;

V04. persistence bytes unchanged;

V05. clean empty-runtime attachment precondition;

V06. exact model/generation/manifest accumulator binding;

V07. first event sequence equals 1;

V08. sequence increments exactly once per event;

V09. serialized-residency successful access emits ACCESS then HIT;

V10. serialized-residency unavailable access emits ACCESS then MISS;

V11. dense-residency successful access emits ACCESS then HIT;

V12. dense-residency unavailable access emits ACCESS then MISS;

V13. unknown-object resource failure emits no ACCESS/cache event;

V14. closed-runtime resource failure emits no ACCESS/cache event;

V15. committed `COLD_DISK -> MAPPED` promotion mapping;

V16. committed `MAPPED -> HOT_MAF` exact BYTES_READ then PROMOTION mapping;

V17. exact BYTES_READ equals registered entry length;

V18. committed `HOT_MAF -> HOT_DENSE` MATERIALIZATION then PROMOTION mapping;

V19. exact downward DEMOTION mapping for all three primitives;

V20. no skipped-state synthetic residency events;

V21. multi-step `ensure_state` exact event sequence;

V22. pin-induced multi-step exact event sequence;

V23. partial multi-step failure records only committed primitives;

V24. no-commit failure records no residency/read/materialization events;

V25. registration records length/order but emits no event;

V26. close produces exact deterministic primitive demotions;

V27. exact frozen cache names;

V28. state/snapshot/unpin do not create access telemetry;

V29. prefetch event counts remain zero;

V30. underlying successful return semantics are preserved;

V31. underlying failure type/message semantics are preserved;

V32. telemetry failure cannot replace runtime success or runtime failure;

V33. telemetry fault permanently blocks scientific telemetry snapshot export;

V34. equal single-thread logical traces produce byte-equivalent canonical
telemetry snapshot payloads;

V35. telemetry-enabled and telemetry-disabled control executions reach equal
Phase 6C runtime snapshots for the same runtime operation sequence;

V36. model/generation/object logical identities remain unchanged;

V37. source segment/model authority remains unchanged;

V38. no integration-time filesystem writes;

V39. no integration-time network/subprocess behavior;

V40. no automatic persistence;

V41. no runtime monkey-patching or callback injection;

V42. direct frozen predecessor SHA revalidation after test execution.

The validation protocol may add prospectively justified checks before its
freeze, but MUST NOT delete these minimum requirements.

## 39. Validation outcome boundary

Only a separately frozen and executed validation result may establish runtime
telemetry integration correctness.

A complete future PASS may establish only:

- deterministic adapter mapping under the tested single-thread surface;
- noninterference with frozen Phase 6C runtime semantics;
- correct use of the frozen telemetry accumulator;
- reproducible RAM telemetry snapshots for the tested traces.

It does not establish real-model corpus representativeness.

## 40. Real-model telemetry boundary

Real-model telemetry collection remains NOT AUTHORIZED by this protocol alone.

It becomes eligible only after:

1. Integration V1 implementation is frozen;
2. Integration Validation V1 is prospectively frozen;
3. the validation executes under exact-once discipline;
4. its raw result is frozen before interpretation;
5. a formal accepted PASS verdict exists.

A real-model corpus then requires its own prospective collection/freeze
protocol.

## 41. Repack planner boundary

No repack planner is authorized by this protocol.

Planner work remains downstream of a frozen representative telemetry corpus.

No planner policy, objective threshold, training/evaluation split, popularity
control, or locality benchmark may be selected post hoc after inspecting
candidate results.

## 42. Repack realization boundary

No segment rewrite, candidate generation construction, generation activation,
or rollback experiment is authorized here.

Repack realization remains a later Phase 6D gate.

## 43. Performance boundary

No benchmark is authorized.

No claim may be made about:

- latency;
- throughput;
- memory benefit;
- storage benefit;
- energy;
- flash wear;
- Vulkan performance;
- multithread scaling.

Performance verdict remains NONE.

## 44. Phase 6D-Q / Phase 6E boundary

This protocol does not enter Phase 6D-Q or Phase 6E.

It establishes no evidence for:

- query-to-PK selection;
- selective working sets;
- tensor avoidance;
- output parity;
- MAF-native inference;
- replacement of `llama.cpp`.

## 45. Intended progression after this protocol

If this protocol freezes successfully, the permitted progression is:

1. implement Integration V1 only;
2. independently audit implementation against this protocol;
3. freeze implementation;
4. preregister Integration Validation V1;
5. freeze validation runner;
6. perform final no-write exact-once preflight;
7. invoke validation exactly once;
8. freeze raw result before interpretation;
9. create formal verdict only after raw-result authority is frozen;
10. only after accepted PASS, preregister representative real-model telemetry
    collection.

## 46. Exact-once rule

This implementation protocol is not itself an exact-once experiment.

The future scientific validation runner MUST use the repository's exact-once
discipline:

- prospectively frozen protocol;
- frozen runner;
- final no-write preflight;
- exactly one authorized invocation;
- durable raw-result freeze before interpretation;
- failure residue preservation;
- no rerun of a spent validation version.

## 47. Authorization disposition

PROTOCOL FREEZE: AUTHORIZED BY THIS ARTIFACT.

INTEGRATION V1 IMPLEMENTATION: AUTHORIZED ONLY AFTER THIS PROTOCOL IS FROZEN.

INTEGRATION V1 VALIDATION EXECUTION: NOT AUTHORIZED.

REAL-MODEL TELEMETRY COLLECTION: NOT AUTHORIZED.

REPACK PLANNER: NOT AUTHORIZED.

REPACK REALIZATION: NOT AUTHORIZED.

DEVICE BENCHMARK: NOT AUTHORIZED.

PHASE 6D-Q: NOT ENTERED.

PHASE 6E: NOT ENTERED.

PERFORMANCE VERDICT: NONE.
