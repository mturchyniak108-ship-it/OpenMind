# MAF Phase 6C Entry Checkpoint

Status: **STARTED / RESEARCH ENTRY FROZEN / NO RUNTIME IMPLEMENTATION YET**

## Purpose

This checkpoint records the formal transition from the completed Phase 6B
persistent-object pipeline into:

**Phase 6C — MAF Object Runtime and Residency**

This is a research-entry and governance artifact.

It does not implement runtime behavior.

## Entry authority

Branch:

`labs/multidimensional-maf`

Phase 6C entry parent HEAD:

`4c1b9732250f85ee5df30a6f9b488886a9568158`

Frozen Phase 6B exit record:

`experiments/model_fractal/MAF_SEGMENT_READER_V1_COMPLETION.md`

Phase 6B exit record SHA256:

`2539b9ad7c623b6415434f73786bf33fc5571a5ec79bd319f7dd8d6bdfe09e94`

Pre-alignment ROADMAP SHA256:

`26646b2ec8ba9a5fef0626fc161972c138f83df641fe1ebbd2ab80dd3a61666e`

The frozen Phase 6B completion record states that:

- Phase 6B.10 is closed;
- Phase 6B is complete and closed;
- no additional Phase 6B experiment is required;
- Phase 6C may begin after that completion checkpoint is frozen.

Those conditions are satisfied at this entry.

## Phase 6C starting state

Phase 6C is formally entered by the Git commit that freezes this checkpoint
and the aligned roadmap together.

At entry:

- Phase 6B remains immutable historical evidence;
- Phase 6C research is current;
- no Phase 6C runtime implementation has yet been accepted;
- no Phase 6C benchmark has yet been accepted;
- no Phase 6C production storage policy has been selected;
- no Phase 6C concurrency implementation has yet been accepted.

## Frozen predecessor boundary

Phase 6C must consume the accepted Phase 6B interfaces rather than silently
rewrite their semantics.

The following Phase 6B responsibilities remain frozen:

- stable logical/object identity;
- generation descriptor and manifest semantics;
- generation construction;
- active-generation authority;
- atomic activation;
- rollback;
- Resident PK Directory V1;
- Segment Reader V1;
- accepted functional validation;
- accepted benchmark evidence;
- accepted post-validation diagnostics.

Any correction to a frozen predecessor requires a new prospective version,
not an in-place Phase 6C modification.

## Phase 6C goal

Keep only the useful model working set resident while preserving the stable
logical identity and exact-byte integrity established by Phase 6B.

The catalog may know every object without requiring every object to remain
materialized or resident.

## Authorized research scope

Phase 6C may investigate and prospectively specify:

1. runtime residency state machines;
2. ownership and lifetime of long-lived file descriptors where justified;
3. mmap or mapped-segment residency where justified by evidence;
4. eviction, reuse, and re-entry policy;
5. on-demand dense materialization;
6. runtime concurrency and thread-safety contracts;
7. resource accounting required to make residency decisions auditable;
8. interaction between frozen ResidentPKEntry identity and runtime-resident
   physical state.

These are research permissions, not implementation conclusions.

## Initial design constraints

The Phase 6C runtime must preserve the separation between:

- logical identity;
- active-generation authority;
- physical serialized range;
- runtime residency state;
- dense/materialized compute view.

Runtime residency must not become authoritative model identity.

Eviction must not alter persistent object identity.

Re-entry must not silently bypass the verification guarantees established by
the frozen Segment Reader boundary unless a separately preregistered,
equivalent integrity mechanism is demonstrated.

## No premature backend selection

This entry checkpoint does not select:

- mmap;
- pread-only residency;
- persistent FD caching;
- SQLite;
- LMDB;
- RocksDB;
- a custom MAFDB;
- a GPU-resident object cache;
- any other production storage/runtime backend.

Such choices require prospective design and measured evidence.

## Concurrency boundary

Concurrency and thread safety are explicitly part of Phase 6C design scope.

No thread-safety claim is inherited automatically from the process-local
Phase 6B experiments.

Before shared concurrent runtime state is accepted, Phase 6C must define
ownership, mutation, lifetime, failure, and synchronization semantics
prospectively.

## Dense materialization boundary

The previously frozen dense-compute-view boundary assigns actual on-demand
dense materialization to Phase 6C.

Phase 6C may therefore design the runtime transition from verified serialized
object bytes to an authorized dense compute view.

This entry checkpoint itself performs no materialization.

## Performance boundary

Phase 6C must not infer runtime performance from the Phase 6B Segment Reader
benchmark alone.

Resident-runtime claims require their own prospective benchmarks.

The unresolved CPU6/CPU7 cluster-1 crossover remains optional follow-up
research and does not block Phase 6C.

## First implementation gate

No Phase 6C runtime code should be accepted merely because this entry
checkpoint exists.

The first implementation gate is a prospective Phase 6C runtime/residency
design protocol that freezes at least:

- runtime state semantics;
- ownership/lifetime semantics;
- transition invariants;
- integrity boundaries;
- error behavior;
- concurrency/thread-safety boundary;
- resource accounting;
- validation plan.

Implementation follows that design freeze, not the reverse.

## Nonclaims

This checkpoint does not establish:

- mmap superiority;
- FD-cache superiority;
- a production eviction policy;
- a production storage engine;
- concurrency correctness;
- multithread scaling;
- GPU residency;
- selective tensor execution;
- MAF-native inference;
- replacement of a conventional LLM runtime.

## Phase boundary

**Phase 6B remains COMPLETE / CLOSED.**

**Phase 6C becomes STARTED / RESEARCH CURRENT when this checkpoint and the
aligned roadmap are frozen together in Git.**

At that moment Phase 6C has started as a research phase, but Phase 6C runtime
implementation remains not yet started.
