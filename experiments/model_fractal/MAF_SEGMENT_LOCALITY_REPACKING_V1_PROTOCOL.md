# MAF Segment Locality and Path-Aware Repacking V1 Protocol

Status: PROSPECTIVE PREREGISTRATION
Phase: 6D
Roadmap title: Segment Locality and Path-Aware Repacking
Artifact class: parent research / architecture protocol
Scientific result: NONE
Performance verdict: NONE
Experiment execution authorized: NO

## 1. Purpose

This protocol prospectively defines the first Phase 6D research boundary for
OpenMind MAF segment locality and path-aware repacking.

Phase 6C is closed and immutable.

Phase 6D must not redefine Phase 6C runtime/residency correctness and must not
prematurely enter Phase 6E selective-access, tensor-avoidance, or selective-
materialization claims.

The Phase 6D goal is the existing authoritative roadmap goal:

> Goal: make physical storage follow measured model pathways.

The central research question is whether measured runtime transition structure
can be converted into a validated physical-layout proposal while preserving
logical MAF identity and generation recoverability.

## 2. Frozen parent

Branch:

`labs/multidimensional-maf`

Parent:

`7a15f9dd5cdd16c41383ea6ec9469f93925e9613`

The parent is the frozen Phase 6C scientific closure commit.

## 3. Authoritative roadmap boundary

Roadmap:

`ROADMAP.md`

Roadmap SHA256:

`b00bc6ce3fab484936cef9d7676906a32b1f0eb0e3070bc76cd02c32f3da50d6`

Frozen Phase 6D section SHA256:

`374d63c18ed246f3c5fd876e34940ee560e7b91d69695a04b675f31883ad6bb1`

Canonical heading:

`## Phase 6D — Segment Locality and Path-Aware Repacking [RESEARCH]`

Canonical goal:

`Goal: make physical storage follow measured model pathways.`

The roadmap section is authoritative.

This protocol may make its requirements more precise but may not broaden the
phase into Phase 6E.

## 4. Frozen Phase 6C dependency

Phase 6C verdict:

`experiments/model_fractal/MAF_OBJECT_RUNTIME_RESIDENCY_PHASE_6C_VERDICT.md`

SHA256:

`800fd8e6e58d2af7ea46133e2e6a26d3b380fa4abd371f055324f722ad92784f`

Phase 6C established the preregistered runtime/residency correctness surface,
including V29-V32 concurrency correctness.

Phase 6C does not provide a performance verdict.

Phase 6C must not be reopened by Phase 6D work.

## 5. Related frozen architecture boundaries

Segment Builder V1 protocol:

`experiments/model_fractal/MAF_SEGMENT_BUILDER_V1_PROTOCOL.md`

SHA256:

`3f55e727c2688852aeffdfefc23993e33a3b703e2a6a7e4c8ba3302b5601a6e1`

The Segment Builder boundary already establishes that path-aware repacking
belongs to Phase 6D and that repacking creates a new physical segment artifact.

Dense Compute View Boundary V1 protocol:

`experiments/model_fractal/MAF_DENSE_COMPUTE_VIEW_BOUNDARY_V1_PROTOCOL.md`

SHA256:

`e67dc84bd86d0e46cc26823b3e000ae1daf29618e1d9fdffc4f11ede4fec55d3`

That boundary assigns locality/repacking to Phase 6D and selective access /
tensor avoidance / selective dense materialization to Phase 6E.

Object Runtime and Residency V1 protocol:

`experiments/model_fractal/MAF_OBJECT_RUNTIME_RESIDENCY_V1_PROTOCOL.md`

SHA256:

`81987d00ef4cb51556dcebf08bff9c9fa8979f033df05304d347b759e545eb13`

Phase 6D may consume runtime telemetry from the Phase 6C runtime contract but
must not alter the meaning of logical object identity.

## 6. Phase 6D V1 scope

V1 covers five ordered research layers:

1. deterministic runtime telemetry semantics;
2. deterministic aggregation and frozen telemetry snapshots;
3. explicit physical-locality metrics;
4. deterministic path-aware repack proposals;
5. generation-safe realization and validation boundaries.

Performance benchmarking is a subsequent gate.

Phase 6D V1 must prove semantics and provenance before any storage-performance
claim is accepted.

## 7. Telemetry remains derived state

Runtime telemetry is derived evidence.

It is not canonical model truth.

Telemetry must not alter:

- model PK;
- generation PK;
- logical object PK;
- object payload identity;
- object semantic identity.

Loss of telemetry must not corrupt or invalidate the authoritative MAF
generation.

## 8. Required telemetry surface

The authoritative roadmap requires collection of:

- object access count;
- reuse interval;
- transition frequency;
- materialization count;
- bytes read;
- cache hit/miss;
- promotion/demotion;
- prefetch usefulness.

V1 implementations may add versioned diagnostic fields, but the eight roadmap
signals above are mandatory.

No mandatory signal may be silently inferred from another signal.

## 9. Telemetry event ordering

A telemetry stream must possess an explicit monotonically increasing logical
event sequence number.

The logical sequence number is the authoritative ordering field for V1
aggregation.

Wall-clock timestamps may be recorded diagnostically but must not be required
for deterministic aggregation.

Equal logical inputs must produce equal aggregates.

## 10. Access count

For each logical object PK:

`access_count[object_pk]`

is the number of preregistered runtime access events attributed to that object.

The exact event classes counted as an access must be frozen by the future
telemetry implementation protocol before execution.

No post-hoc event-class changes are permitted within a frozen measurement
version.

## 11. Reuse interval

For V1, reuse interval is defined in logical event distance rather than elapsed
wall time.

For consecutive qualifying accesses to the same object at event indices
`i_prev` and `i_now`:

`reuse_interval = i_now - i_prev`

A future device-performance protocol may separately measure time-domain reuse.

Logical-event reuse and elapsed-time reuse must not be conflated.

## 12. Transition frequency

For consecutive qualifying logical object accesses:

`transition_count[(source_pk, target_pk)] += 1`

Directed transitions are authoritative raw aggregates.

A planner may derive a symmetric relationship weight only if it declares the
mapping explicitly.

A canonical symmetric candidate is:

`w(a,b) = transition_count[(a,b)] + transition_count[(b,a)]`

The raw directed counts must remain available for audit.

## 13. Materialization count

Materialization count records actual qualifying object materialization events.

It must not be substituted with access count, promotion count, or cache miss
count.

## 14. Bytes read

Bytes read records the bytes attributable to the explicitly defined read event
surface.

Logical requested bytes and physical storage bytes may differ and therefore
must be named separately if both are collected.

The implementation protocol must state which one each counter represents.

## 15. Cache hit and miss

Cache outcomes must be explicit telemetry events or explicit aggregate
increments.

A hit/miss classification must be tied to a named cache boundary.

No generic "cache hit" claim is valid without identifying which cache is being
measured.

## 16. Promotion and demotion

Promotion/demotion telemetry records actual runtime state transitions under the
frozen runtime state machine.

Phase 6D telemetry must not redefine the Phase 6C state transition contract.

## 17. Prefetch usefulness

If prefetch is not implemented, the telemetry field remains unsupported or
zero according to the future implementation protocol.

V1 must not simulate prefetch usefulness and report it as observed runtime
evidence.

If prefetch is later implemented, usefulness must distinguish at minimum:

- prefetched and subsequently consumed;
- prefetched and not consumed before invalidation/eviction/end of trace.

## 18. RAM-first aggregation

The roadmap requires runtime telemetry collection in RAM followed by periodic
persistence of aggregated statistics.

V1 therefore requires:

- raw runtime operation is not blocked on a persistence write for every
  telemetry event;
- aggregation state is explicitly versioned;
- snapshot creation is a defined operation;
- persisted snapshots are derived artifacts;
- snapshot failure must not corrupt canonical MAF model data.

The exact persistence cadence is not fixed by this parent protocol.

## 19. Frozen telemetry snapshot

Any telemetry dataset used to produce a scientific repacking result must first
be frozen as an immutable snapshot.

The snapshot must bind at minimum:

- schema/version;
- model PK;
- source generation PK;
- source manifest identity;
- telemetry aggregation semantics/version;
- complete aggregate values;
- event-count boundary or trace boundary;
- content SHA256.

A repack experiment must never consume an unfrozen mutable telemetry dataset
while claiming a reproducible result.

## 20. Training/evaluation separation

A future claim that a repacking policy generalizes beyond the telemetry used to
construct it requires prospective held-out evaluation.

The planner-training trace and the evaluation trace must be separated before
evaluating the claimed improvement.

This V1 parent protocol does not choose a split ratio or corpus.

Those must be preregistered after a telemetry corpus exists but before the
corresponding experiment is executed.

## 21. Logical identity invariant

The roadmap rule is absolute:

`logical PKs never change because of repacking`

Therefore a repack proposal must preserve every logical object PK exactly.

Repacking may change only physical representation metadata that is permitted
to vary by the existing MAF generation architecture.

## 22. Physical mapping mutability

The roadmap explicitly permits:

`physical segment/offset mappings may change`

A Phase 6D repack proposal may therefore alter:

- physical segment membership;
- physical segment identifier where generated according to frozen segment
  rules;
- byte offset;
- physical object ordering;
- physical segment packing.

It must not silently alter logical identity or payload content.

## 23. Payload preservation

For every logical object included in a lossless V1 repack:

- logical object PK must be unchanged;
- object payload length must be unchanged;
- object payload SHA256 must be unchanged;
- exact object bytes must reconstruct identically.

A locality improvement obtained by changing object payload bytes is invalid.

## 24. Repacking is generational

The authoritative roadmap requires:

`repacking is generational, validated, and atomically activated`

Therefore V1 must never modify an active generation's segment bytes in place.

A realized repack must produce a new candidate generation.

The old generation remains authoritative until candidate validation and atomic
activation succeed.

## 25. Recoverability

The roadmap requires:

`old generations remain recoverable until the new generation validates`

A candidate repack failure must leave the previous generation recoverable.

Validation failure must not destroy, overwrite, or make the previous
generation unreachable.

## 26. Flash-wear boundary

The roadmap requires avoiding frequent rewrites that create flash wear or
cache churn.

V1 therefore treats rewrite volume and activation frequency as explicit costs.

No algorithm may be called superior based solely on locality if it requires
unbounded or pathological rewrite frequency.

The threshold at which rewrite cost outweighs locality benefit is not assumed
by this parent protocol and must be device-benchmarked prospectively.

## 27. Transition locality precedence

The roadmap states:

`transition locality is more important than global popularity alone`

Therefore any scientific Phase 6D locality comparison must include a
popularity-only control if it claims benefit from transition structure.

A transition-aware planner must not be compared only against a deliberately
weak or random layout.

## 28. Original-layout control

The original physical layout is a mandatory control for any repacking-benefit
claim.

A candidate layout that fails to improve the preregistered locality objective
against the original layout cannot establish a Phase 6D locality-improvement
claim.

## 29. Popularity-only control

A global-popularity-only layout is a mandatory control for any claim that
transition-aware topology provides value beyond simple hot-object ordering.

The exact popularity ordering and tie-break rule must be preregistered before
the corresponding benchmark.

## 30. Random/permutation control

A randomized/permutation layout control is strongly required for scientific
locality comparisons.

Any random seed and permutation count must be frozen before execution.

This parent protocol intentionally does not select them before the evaluation
corpus and benchmark design exist.

## 31. Physical locality metrics

Phase 6D must measure locality explicitly.

No wall-clock performance claim may be substituted for an undefined notion of
"better locality."

At minimum, a future locality experiment must preregister one primary locality
metric and may preregister secondary metrics.

Candidate metrics include the metrics defined below.

## 32. Weighted transition rank distance

Given a deterministic physical object order and directed transition counts:

`rank_distance(a,b) = abs(rank(a) - rank(b))`

and:

`weighted_transition_rank_distance =
    sum(c(a,b) * rank_distance(a,b)) / sum(c(a,b))`

over the preregistered qualifying transitions.

Lower is more local.

This metric is independent of object byte size and is therefore useful as a
topological ordering metric.

## 33. Weighted transition byte gap

For objects mapped into an ordered physical byte space, define each object's
closed-open interval:

`[offset, offset + length)`

For two non-overlapping intervals in the same physical segment, byte gap is the
number of bytes between the intervals.

Adjacent intervals have byte gap zero.

A future benchmark may compute transition-count-weighted byte gap.

Cross-segment transitions must not be assigned an arbitrary byte distance;
they must be reported separately or handled by a prospectively defined metric.

## 34. Cross-segment transition fraction

For qualifying directed transitions:

`cross_segment_fraction =
    cross_segment_transition_count /
    total_transition_count`

with transition counts weighted by observed frequency.

Lower is more co-located.

## 35. Co-segment transition fraction

The complementary directly interpretable metric is:

`co_segment_fraction =
    same_segment_transition_count /
    total_transition_count`

Higher is more co-located.

A benchmark need not report both if one is fully derivable from the other.

## 36. Metric selection must precede results

The primary metric, secondary metrics, tie-breaks, thresholds, exclusions, and
aggregation rules for a scientific Phase 6D benchmark must be frozen before
that benchmark executes.

Metrics may not be selected after viewing candidate-layout results.

## 37. Deterministic repack planner contract

A V1 repack planner must be deterministic.

For identical:

- source generation identity;
- object metadata;
- frozen telemetry snapshot;
- planner version;
- planner configuration;

the planner must emit byte-for-byte identical canonical plan output.

## 38. Repack plan artifact

Before physical segment generation, the planner should emit an immutable
repack plan.

At minimum, the plan must bind:

- schema/version;
- planner version;
- source model PK;
- source generation PK;
- telemetry snapshot identity;
- ordered logical object PKs or explicit physical placement decisions;
- planner configuration;
- objective/metric identifiers;
- plan SHA256.

The plan is derived state and does not itself become canonical model truth.

## 39. Planner tie-breaking

All planner ties must have deterministic tie-break rules.

Logical object PK lexical ordering is an acceptable final deterministic
tie-break unless a different rule is preregistered.

Iteration order of an unordered Python container must never determine a
scientific repack plan.

## 40. No oracle leakage

A planner may use only the telemetry and metadata authorized by its prospective
protocol.

Held-out evaluation transitions must not influence a planner that is being
evaluated for held-out locality improvement.

Phase 6E inference outputs, hidden-state oracle information, or future-token
knowledge must not leak into a Phase 6D planner unless a separate protocol
explicitly studies such information.

## 41. Realization boundary

A validated plan may be realized only through the existing immutable MAF
segment/generation architecture.

No in-place active-segment rewrite is authorized.

Physical realization must preserve the exact logical objects required by the
plan.

## 42. Candidate-generation validation

Before activation, a candidate repacked generation must receive independent
prospective validation.

At minimum that validation must establish:

- candidate manifest integrity;
- candidate segment integrity;
- exact logical object set preservation;
- exact logical PK preservation;
- exact payload-byte reconstruction;
- exact payload-hash preservation;
- valid physical mappings;
- source/old-generation recoverability;
- activation preconditions.

## 43. Atomic activation

Only a validated candidate generation may become active.

Activation must use the already established atomic/generational model rather
than overwriting active authority in place.

Activation failure must not create ambiguous authority.

## 44. Rollback / recovery

A repack workflow must preserve a defined recovery path to the prior valid
generation.

Repacking is invalid if candidate failure destroys the last known-good
generation.

## 45. Segment-size hypothesis

The authoritative roadmap explicitly states that initial segment-size choices
are hypotheses.

This parent protocol freezes no "optimal" segment size.

Any claim about segment size must be supported by a separate prospective device
benchmark.

## 46. Fragment-size hypothesis

The same rule applies to fragment size.

Phase 6D V1 does not assume that smaller or larger fragments improve locality,
I/O, inference, or storage efficiency.

## 47. Device benchmark boundary

Correct repacking semantics do not establish device performance benefit.

After correctness validation, a separate prospective benchmark must measure
the relevant device costs and benefits.

Possible device measurements include:

- bytes physically read;
- read-call count;
- segment crossings;
- cache hit/miss;
- wall-clock latency;
- throughput;
- CPU time;
- memory pressure;
- energy/thermal behavior where measurable;
- rewrite volume;
- repack construction cost.

The actual benchmark surface must be preregistered separately.

## 48. No performance threshold in this parent protocol

This parent protocol intentionally freezes no percentage-improvement threshold.

A performance threshold chosen before representative telemetry and benchmark
design exist would be arbitrary.

Thresholds, equivalence margins, and statistical tests must be frozen in the
specific future benchmark protocol before execution.

## 49. Phase 6E boundary

Phase 6E begins at:

`## Phase 6E — Selective MAF Access and Tensor Avoidance [CRITICAL RESEARCH]`

Its goal is to determine whether OpenMind can avoid touching or materializing
complete dense tensors while preserving inference fidelity.

Phase 6D must not claim:

- selective tensor avoidance;
- selective fragment retrieval fidelity;
- hidden-state equivalence;
- logit equivalence;
- top-k agreement;
- token agreement;
- MAF-native inference equivalence.

Those belong to Phase 6E or later.

## 50. Phase 6F boundary

Multithreaded performance optimization and scaling remain Phase 6F.

Phase 6D may require thread-safe telemetry correctness, but must not convert
that requirement into a Phase 6F performance claim.

## 51. Scientific controls

Any future claim that path-aware repacking improves locality must compare a
prospectively frozen candidate against appropriate controls.

At minimum:

- original physical layout;
- global-popularity-only layout.

A randomized/permutation control should also be used unless a future protocol
provides a documented reason it is inappropriate.

## 52. Failure atomicity

A failure during telemetry persistence, planning, candidate generation,
validation, or activation must not mutate logical object identity or corrupt
the previous valid generation.

Failure residue must be preserved when required for audit.

A failed exact-once scientific runner may never be silently cleaned and rerun
under the same version.

## 53. Provenance

Every scientific Phase 6D artifact must bind sufficient identities to recover
its lineage.

Depending on artifact type this includes:

- protocol SHA256;
- implementation SHA256;
- source model/generation identity;
- telemetry snapshot SHA256;
- plan SHA256;
- candidate generation identity;
- result SHA256.

## 54. Exact-once scientific execution

This parent protocol is not itself an exact-once runner.

Every future runner that produces a scientific Phase 6D result must have:

1. a prospectively frozen protocol;
2. a frozen runner;
3. a final no-write preflight;
4. exactly one scientific invocation;
5. immediate raw-result freeze before interpretation;
6. preserved execution residue;
7. no rerun of a spent version.

## 55. Phase 6D V1 implementation sequence

The intended implementation progression is:

1. define and freeze telemetry data structures / aggregation semantics;
2. implement RAM telemetry aggregation without changing canonical MAF truth;
3. prospectively validate telemetry correctness;
4. define and freeze telemetry snapshot serialization;
5. validate deterministic snapshot identity;
6. define and implement deterministic locality metrics;
7. define and implement deterministic repack-plan representation;
8. prospectively validate planner determinism and identity preservation;
9. realize plans as new immutable candidate generations;
10. prospectively validate repacked generation correctness and recoverability;
11. freeze a representative telemetry corpus;
12. preregister locality comparison controls and metrics;
13. run exact-once locality experiments;
14. only after correctness and locality evidence, preregister device benchmarks.

## 56. Initial V1 correctness claims allowed

A future validated V1 implementation may establish only claims it directly
tests, such as:

- telemetry aggregation is deterministic;
- required counters follow frozen event semantics;
- telemetry snapshots are reproducible;
- repack planning is deterministic;
- logical object PKs are preserved;
- object payload bytes are preserved;
- physical placement can change without logical identity change;
- candidate generation creation is immutable;
- candidate failure preserves the old generation;
- validated candidate activation is atomic under the frozen activation model.

## 57. Claims requiring separate locality evidence

The following require a separate prospective locality experiment:

- transition-aware ordering improves measured locality;
- transition-aware ordering beats original layout;
- transition-aware ordering beats global popularity;
- transition topology generalizes to held-out runtime traces.

They are not established by implementation correctness alone.

## 58. Claims requiring separate device benchmark evidence

The following require a separate prospective device benchmark:

- fewer bytes read in practice;
- fewer storage operations;
- lower latency;
- greater throughput;
- lower memory pressure;
- better cache behavior;
- lower energy;
- better thermal behavior;
- net benefit after repack construction cost;
- acceptable flash-write cost;
- an optimal segment size;
- an optimal fragment size.

## 59. Explicit nonclaims

Freezing this protocol establishes no experimental result.

It does not prove:

- physical locality has improved;
- inference is faster;
- inference uses less memory;
- inference uses less power;
- path-aware repacking beats popularity;
- path-aware repacking beats original layout;
- any segment size is optimal;
- any fragment size is optimal;
- selective materialization works;
- tensor avoidance works;
- MAF replaces a conventional LLM runtime;
- MAF-native inference is equivalent to the source model.

## 60. Phase 6D exit boundary

Phase 6D must not be considered scientifically closed merely because a planner
or repacker exists.

Before Phase 6D closure, evidence should establish at minimum:

- telemetry correctness;
- deterministic aggregation;
- deterministic plan generation;
- logical PK preservation;
- exact payload preservation;
- generational candidate construction;
- candidate validation;
- old-generation recoverability;
- atomic activation semantics;
- prospective measured locality evidence against required controls;
- prospectively measured device behavior for layout parameters that are claimed
  to matter.

Phase 6E may be developed only without borrowing unproven Phase 6D performance
claims.

## 61. Authorization boundary

Freezing this parent protocol authorizes only prospective Phase 6D
implementation and further preregistration.

It does not authorize a scientific Phase 6D result yet.

It does not authorize changing the Phase 6C evidence chain.

It does not authorize a device benchmark without a dedicated benchmark
protocol.

It does not authorize Phase 6E claims.

PHASE 6C REOPEN: FORBIDDEN.

V1 / V1.1 / V1.2 / V1.3 PHASE 6C RERUNS: FORBIDDEN.

PHASE 6D SCIENTIFIC RESULT: NONE.

PERFORMANCE VERDICT: NONE.

PUSH: NOT AUTHORIZED BY THIS PROTOCOL.
