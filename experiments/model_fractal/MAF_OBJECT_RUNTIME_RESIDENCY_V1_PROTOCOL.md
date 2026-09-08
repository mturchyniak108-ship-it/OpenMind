# OpenMind MAF Object Runtime and Residency V1 Protocol

Status: **PREREGISTERED DESIGN / UNIMPLEMENTED / BACKEND-NEUTRAL**

Phase:

**6C — MAF Object Runtime and Residency**

Schema:

`openmind.maf_object_runtime_residency.v1`

## 1. Purpose

This protocol prospectively freezes the observable correctness contract for
the first Phase 6C MAF Object Runtime and Residency implementation.

It is written before any Phase 6C runtime engine exists.

It does not implement the runtime.

It does not select a production storage backend.

It does not select mmap, persistent file-descriptor caching, an eviction
algorithm, a database engine, a GPU cache, or a multithread scaling strategy.

The protocol defines:

- residency states;
- legal state transitions;
- logical/runtime identity separation;
- runtime resource ownership;
- verified-byte integrity;
- pin/unpin behavior;
- explicit demotion and eviction mechanics;
- dense-view materialization semantics;
- concurrency and thread-safety semantics;
- resource accounting;
- deterministic failure atomicity;
- validation obligations before performance claims.

## 2. Frozen research authority

Phase 6C entry HEAD:

`aabab5f7bddea26a2e26615811947a82cff69d65`

Roadmap:

`ROADMAP.md`

Roadmap SHA256:

`b00bc6ce3fab484936cef9d7676906a32b1f0eb0e3070bc76cd02c32f3da50d6`

Phase 6C entry checkpoint:

`experiments/model_fractal/MAF_PHASE_6C_ENTRY_CHECKPOINT.md`

Entry checkpoint SHA256:

`5f2972d44ddc470aec3826ddda2ebade2fb92b28cbb562a99ab87daa15f21871`

Frozen Phase 6B completion:

`experiments/model_fractal/MAF_SEGMENT_READER_V1_COMPLETION.md`

Phase 6B completion SHA256:

`2539b9ad7c623b6415434f73786bf33fc5571a5ec79bd319f7dd8d6bdfe09e94`

Resident PK Directory V1:

`experiments/model_fractal/maf_resident_pk_directory_v1.py`

SHA256:

`4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6`

Segment Reader V1:

`experiments/model_fractal/maf_segment_reader_v1.py`

SHA256:

`3499cb8e528fe8e9315e3e5656d6aa888c95ca175310b6371e722de409827369`

Dense Compute View Boundary V1:

`experiments/model_fractal/MAF_DENSE_COMPUTE_VIEW_BOUNDARY_V1_PROTOCOL.md`

SHA256:

`e67dc84bd86d0e46cc26823b3e000ae1daf29618e1d9fdffc4f11ede4fec55d3`

CPU Thermal Characterization V1.2 protocol:

`experiments/model_fractal/CPU_THERMAL_CHARACTERIZATION_V1_2_PROTOCOL.md`

SHA256:

`b98e4c4d7309948b0fbf71f4a961e038a7e55470f03153e85ec724ffd32f3cbb`

These predecessor bytes are immutable inputs.

Phase 6C must consume them without silently changing their semantics.

## 3. Frozen predecessor interface

The runtime consumes immutable `ResidentPKEntry` evidence.

The frozen `ResidentPKEntry` fields are:

- `model_pk: str`;
- `generation_pk: str`;
- `generation_manifest_sha256: str`;
- `object_pk: str`;
- `segment_id: str`;
- `offset: int`;
- `length: int`;
- `object_file_sha256: str`;
- `payload_sha256: str`;
- `segment_length: int`;
- `segment_sha256: str`;
- `segment_path: str`.

The frozen verified-read boundary is:

`read_serialized_object(entry: ResidentPKEntry, expected_generation_pk: str) -> bytes`

Segment Reader V1:

- validates the entry;
- requires the expected generation;
- opens the segment read-only;
- obtains metadata from the opened descriptor;
- requires a regular segment;
- requires exact segment length;
- performs one positional object-range read;
- rejects short reads;
- hashes the returned object range;
- rejects object-file SHA256 mismatch;
- returns bytes only after successful verification;
- closes the descriptor.

The Phase 6C V1 runtime must not weaken this verified-byte boundary.

## 4. Authority model

Persistent MAF bytes remain authoritative.

Runtime state is derived, process-local state.

Runtime state is never authoritative model identity.

The minimum runtime object identity is:

`(model_pk, generation_pk, object_pk)`

The runtime must not reinterpret:

- `segment_path`;
- `segment_id`;
- `offset`;
- `length`;
- `object_file_sha256`;
- `segment_length`;
- `segment_sha256`

as permanent logical identity.

Physical placement may change in later immutable generations without changing
the logical meaning of an object.

## 5. Runtime generation binding

One V1 runtime instance is bound to exactly:

- one `model_pk`; and
- one active `generation_pk`.

A runtime operation involving an entry whose:

- `model_pk` differs from the runtime model; or
- `generation_pk` differs from the runtime generation

must fail before changing residency state.

No stale entry may be promoted into runtime residency.

Refreshing or replacing the active generation belongs to an explicit runtime
replacement/refresh operation and must not mutate the identity of already
published objects in place.

## 6. Public residency states

The V1 public residency states are:

1. `COLD_DISK`
2. `MAPPED`
3. `HOT_MAF`
4. `HOT_DENSE`

`VULKAN_MAF` remains a roadmap-level future state and is outside this V1
implementation contract.

No Vulkan residency claim is authorized by V1.

## 7. COLD_DISK

`COLD_DISK` means:

- the object exists through frozen persistent/catalog authority;
- no runtime attachment is required;
- no verified serialized-object byte buffer is resident;
- no dense compute view is resident;
- no object-specific runtime resource is required.

`COLD_DISK` does not mean the object is absent.

It means the persistent representation is authoritative and the runtime has
not promoted that object.

## 8. MAPPED

`MAPPED` is a backend-neutral runtime attachment state.

The word `MAPPED` in this protocol does **not** select OS `mmap`.

`MAPPED` means:

- the runtime has accepted one generation-bound `ResidentPKEntry`;
- the persistent segment/range is known and addressable by the runtime;
- no unverified serialized bytes are exposed as `HOT_MAF`;
- no dense compute view exists;
- runtime attachment accounting exists.

A conforming V1 implementation may represent this attachment without a
long-lived OS file descriptor and without an OS memory mapping.

Any later implementation that uses mmap or persistent descriptors must earn
that choice through separately frozen design/benchmark evidence.

## 9. HOT_MAF

`HOT_MAF` means:

- the object is at least `MAPPED`;
- the exact serialized object-file bytes are resident in process memory;
- those bytes have passed the frozen Segment Reader V1 verification boundary;
- the resident bytes hash to `ResidentPKEntry.object_file_sha256`;
- the runtime owns the resident byte buffer;
- callers cannot mutate the authoritative resident bytes in place.

A byte buffer obtained without successful integrity verification must never
enter `HOT_MAF`.

For V1, promotion into `HOT_MAF` MUST use the frozen
`read_serialized_object()` boundary.

Replacing that read path requires a separate prospective successor protocol
or independently validated equivalent integrity mechanism.

## 10. HOT_DENSE

`HOT_DENSE` means:

- the object is at least `HOT_MAF`;
- a derived dense compute view exists;
- the persistent MAF representation remains authoritative;
- the dense view is optional;
- the dense view is non-authoritative;
- destruction of the dense view does not alter logical identity;
- construction of the dense view does not alter persistent bytes;
- `HOT_MAF` verified bytes remain logically available as the parent authority
  while the dense view exists.

V1 does not authorize a dense view to overwrite persistent MAF bytes.

## 11. Primitive legal transitions

The primitive upward transitions are:

`COLD_DISK -> MAPPED`

`MAPPED -> HOT_MAF`

`HOT_MAF -> HOT_DENSE`

The primitive downward transitions are:

`HOT_DENSE -> HOT_MAF`

`HOT_MAF -> MAPPED`

`MAPPED -> COLD_DISK`

No primitive transition may skip a state.

A convenience operation may request a higher target state, but it must be
observably equivalent to performing the required primitive transitions in
order.

A failed intermediate transition leaves the object at the last completely
committed state.

## 12. Illegal transitions

Examples of illegal primitive transitions include:

- `COLD_DISK -> HOT_MAF`;
- `COLD_DISK -> HOT_DENSE`;
- `MAPPED -> HOT_DENSE`;
- `HOT_DENSE -> MAPPED`;
- `HOT_DENSE -> COLD_DISK`;
- transition to `VULKAN_MAF`;
- transition to an unknown state.

An illegal primitive transition must fail deterministically and must not
change:

- object state;
- pin state;
- resident-byte accounting;
- dense-byte accounting;
- runtime identity.

## 13. Idempotent target requests

Requesting the object's already-committed residency state is an idempotent
no-op.

It must not:

- duplicate resources;
- duplicate resident bytes;
- increment pin counts;
- rerun dense materialization;
- alter accounting except an optional operation counter.

This rule does not convert illegal skipped primitive transitions into legal
primitive transitions.

## 14. Transition atomicity

Every transition has:

1. a previously committed state;
2. zero or more provisional resources;
3. one successful commit point.

Before the commit point, failure must preserve the previous committed state.

After the commit point, accounting and externally observable state must agree.

Partially initialized resources must never be published as a committed
residency state.

## 15. HOT_MAF integrity invariant

For every committed `HOT_MAF` or `HOT_DENSE` object:

`sha256(resident_serialized_bytes) == ResidentPKEntry.object_file_sha256`

must hold.

Promotion failure due to:

- stale generation;
- invalid entry;
- segment I/O;
- nonregular segment;
- segment-length mismatch;
- short read;
- object hash mismatch

must leave the object no higher than its previously committed residency
state.

No unverified-byte escape is permitted.

## 16. Re-entry integrity

After an object is demoted below `HOT_MAF`, a later promotion back to
`HOT_MAF` must verify the serialized object again.

A previous successful verification must not silently authorize unrelated
future bytes after:

- demotion;
- detachment;
- generation replacement;
- process restart.

V1 therefore treats verified resident bytes as a runtime capability whose
validity ends when those bytes are discarded.

## 17. Runtime resource ownership

Every runtime-created resource has exactly one runtime owner.

Ownership must be explicit for:

- attachment records;
- resident serialized-byte buffers;
- dense views;
- pin leases;
- any later backend resource.

A resource must not be released twice.

A resource must not remain reachable after its owning committed residency
state has been destroyed, except for immutable externally owned input
evidence.

Long-lived file descriptor ownership is within Phase 6C research scope but
is **not selected by this V1 protocol**.

## 18. Pin model

V1 pinning uses explicit pin leases.

Each active pin lease is bound to:

- one runtime object identity;
- one minimum required residency state.

Permitted minimum pin states are:

- `MAPPED`;
- `HOT_MAF`;
- `HOT_DENSE`.

A pin request for `COLD_DISK` is unnecessary and invalid.

Each successful pin returns a unique opaque pin token.

The runtime maintains an exact active pin set.

## 19. Effective pin floor

For an object with active pins, its effective pin floor is the highest
minimum residency state requested by any active pin.

Ordering is:

`MAPPED < HOT_MAF < HOT_DENSE`

The runtime must not demote an object below its effective pin floor.

Example:

- one `MAPPED` pin;
- one `HOT_MAF` pin

produces effective floor `HOT_MAF`.

Removing the `HOT_MAF` pin lowers the floor to `MAPPED`.

## 20. Unpin behavior

Unpinning requires an active opaque pin token.

An unknown token must fail deterministically.

A previously consumed token must fail deterministically.

Unpin changes only pin ownership/accounting.

Unpin does not automatically demote an object.

Demotion remains an explicit operation or a later separately specified
eviction policy action.

## 21. Eviction and demotion V1 boundary

V1 freezes eviction **mechanics**, not an automatic eviction algorithm.

The V1 runtime must support explicit safe demotion.

V1 does not select:

- LRU;
- TinyLFU;
- CLOCK;
- FIFO;
- LFU;
- random eviction;
- another automatic policy.

Automatic policy comparison belongs to later prospective benchmark/design
work.

Explicit demotion must obey:

- pin floors;
- state-transition legality;
- ownership cleanup;
- accounting invariants.

## 22. Budget model

V1 must support explicit nonnegative runtime budgets for at least:

- verified serialized resident bytes;
- dense resident bytes.

A budget of zero is valid.

Before a promotion commits, the runtime must calculate the resulting
accounted usage.

If committing the transition would exceed the relevant budget, promotion
must fail with no committed state change.

V1 performs no hidden automatic eviction to satisfy a failed promotion.

This keeps policy experiments separable from runtime correctness.

## 23. Serialized resident-byte accounting

Only committed runtime-owned verified serialized buffers count toward
serialized resident bytes.

The accounting unit is exact bytes.

For one object in `HOT_MAF` or `HOT_DENSE`, its serialized resident-byte
charge must equal the actual owned verified buffer length.

No object may be charged twice for the same owned buffer.

Demotion from `HOT_MAF` to `MAPPED` releases that charge exactly once.

## 24. Dense resident-byte accounting

A committed dense view must expose or supply an exact byte charge.

Dense resident bytes are derived-view accounting and remain separate from
serialized resident bytes.

Promotion `HOT_MAF -> HOT_DENSE` adds the dense charge exactly once.

Demotion `HOT_DENSE -> HOT_MAF` removes the dense charge exactly once.

Dense accounting must never modify persistent-byte authority.

## 25. Attachment accounting

V1 must account for committed `MAPPED`-or-higher objects.

At minimum, the runtime must expose:

- total object count;
- `COLD_DISK` count;
- `MAPPED` count;
- `HOT_MAF` count;
- `HOT_DENSE` count;
- total active pin leases;
- serialized resident bytes;
- dense resident bytes.

If later backends introduce descriptors or mappings, those resources require
their own explicit counters before acceptance.

## 26. Required counters

V1 must expose monotonically nonnegative counters for at least:

- successful attach transitions;
- successful verified-byte promotions;
- successful dense materializations;
- successful dense demotions;
- successful serialized-byte demotions;
- successful detach transitions;
- successful pin acquisitions;
- successful unpins;
- failed transitions;
- verification failures;
- budget rejections.

Counters are diagnostic evidence, not logical identity.

Counter overflow or negative accounting is invalid.

## 27. Dense materializer contract

Dense materialization is performed through an explicit materializer boundary.

The materializer receives:

- immutable `ResidentPKEntry` evidence;
- verified serialized object bytes.

It may return a derived dense view plus its exact accounted byte size.

The materializer must not:

- mutate the `ResidentPKEntry`;
- mutate verified serialized bytes;
- mutate persistent segment bytes;
- change runtime model/generation identity.

A materialization error leaves the object in `HOT_MAF`.

## 28. Dense view lifetime

A dense view is owned by the runtime after successful commit.

It remains valid only while the object remains `HOT_DENSE`.

Demotion to `HOT_MAF` destroys runtime ownership of that dense view.

A stale reference must not be returned as a current runtime dense view after
demotion.

V1 validation must check this observable lifetime boundary.

## 29. Read exposure

The runtime must not expose mutable internal accounting or state containers.

Serialized resident bytes returned to callers must preserve immutable-byte
semantics.

Dense-view mutability, if required by a future compute adapter, must be
specified independently from persistent authority.

Mutation of a dense view must never mutate persistent MAF bytes or the
verified serialized parent buffer.

## 30. Concurrency contract

V1 correctness is thread-safe at the public runtime API boundary.

For one runtime object:

- at most one mutating state transition may commit at a time;
- public mutations are linearizable;
- state observations see either the complete state before a transition or the
  complete state after it;
- observers must not see provisional state;
- pin accounting must be race-safe;
- byte accounting must be race-safe;
- duplicate promotion races must not duplicate ownership or accounting.

The protocol does not require lock-free behavior.

The protocol does not claim multithread scaling.

## 31. Cross-object concurrency

Operations on different objects may be serialized by the first
implementation.

A coarse-grained implementation is acceptable for V1 correctness.

Performance promotion requires later measurements.

No benchmark may infer concurrency scaling merely because V1 is thread-safe.

## 32. Callback/re-entrancy boundary

A V1 materializer or other externally supplied callback must not recursively
invoke mutation on the same runtime instance unless a future protocol
explicitly authorizes re-entrancy.

Re-entrant mutation is outside the V1 contract.

The implementation must fail safely or document internal prevention rather
than allowing partially recursive state mutation.

## 33. Runtime snapshot/read consistency

A runtime inspection/snapshot API must return a self-consistent view of:

- bound model;
- bound generation;
- per-state object counts;
- active pin count;
- serialized resident bytes;
- dense resident bytes;
- diagnostic counters.

A snapshot must not contain half-applied accounting from an in-progress
transition.

## 34. Deterministic error categories

The implementation must define distinct public error categories equivalent
to:

- invalid runtime entry;
- stale model/generation;
- unknown runtime object;
- illegal residency transition;
- pinned demotion;
- unknown/consumed pin token;
- serialized-byte budget exceeded;
- dense-byte budget exceeded;
- verified-read/integrity failure;
- dense materialization failure;
- runtime closed/unavailable;
- concurrency/re-entrancy violation where applicable.

Exact Python class names may be frozen in the implementation protocol/engine,
but these semantic categories are mandatory.

## 35. Failure atomicity

For every public mutation, a raised error must leave:

- committed state valid;
- runtime identity unchanged;
- pin accounting valid;
- byte accounting valid;
- resource ownership valid.

No error path may publish unverified bytes.

No error path may silently lower a pin floor.

No error path may convert a stale generation into current authority.

## 36. Runtime close boundary

The V1 runtime must have an explicit close/lifecycle boundary.

Closing must:

- reject new promotion/pin/materialization operations;
- release runtime-owned dense views;
- release runtime-owned serialized buffers;
- release runtime-owned attachment resources;
- invalidate active runtime pin leases;
- preserve persistent files unchanged.

Close must be idempotent.

A closed runtime cannot be reopened in place.

A new runtime instance may be constructed from accepted current authority.

## 37. Source immutability

Phase 6C V1 runtime operations must not modify:

- active-generation evidence;
- candidate manifests;
- segment files;
- frozen validation/benchmark/diagnostic artifacts;
- Resident PK Directory V1;
- Segment Reader V1.

The first runtime implementation is a derived consumer of frozen authority.

## 38. Filesystem-write boundary

No ordinary residency transition requires mutation of source MAF files.

If a future backend requires runtime metadata files, that behavior must be
prospectively specified and independently validated.

V1 does not authorize persistent runtime metadata mutation.

## 39. Backend neutrality

Selected backend:

**NONE**

V1 does not select:

- `mmap`;
- persistent `pread` descriptor caching;
- per-object descriptors;
- per-segment descriptors;
- SQLite;
- LMDB;
- RocksDB;
- custom MAFDB;
- GPU-resident cache.

The state machine must be implementable independently of these choices.

`MAPPED` is therefore a logical attachment/residency state, not proof that
`mmap(2)` was called.

## 40. VULKAN_MAF boundary

`VULKAN_MAF` is outside V1.

No V1 implementation or validation may claim:

- GPU residency;
- GPU-addressable MAF objects;
- Vulkan cache correctness;
- GPU eviction;
- GPU memory-budget correctness.

Those require later prospective work.

## 41. Selective materialization boundary

Phase 6C permits on-demand materialization for a requested object.

Phase 6E remains responsible for broader selective-materialization claims
about avoiding unnecessary tensor/object materialization across inference
workloads.

V1 must not convert object-level on-demand materialization into a Phase 6E
claim.

## 42. Validation must precede benchmark acceptance

The V1 runtime implementation must receive a separate prospective validation
protocol before its first accepted validation execution.

No performance benchmark may establish correctness.

Validation acceptance must precede benchmark interpretation.

## 43. Mandatory V1 validation matrix

The future V1 validation protocol must test at minimum:

1. exact runtime model/generation binding;
2. initial `COLD_DISK` state;
3. legal upward primitive transitions;
4. legal downward primitive transitions;
5. rejection of skipped/illegal primitive transitions;
6. idempotent same-state target request;
7. verified promotion through frozen Segment Reader V1;
8. corruption/hash-failure non-publication;
9. short-read non-publication;
10. stale-generation rejection;
11. exact serialized-byte accounting;
12. exact dense-byte accounting;
13. zero-budget rejection;
14. over-budget failure atomicity;
15. multiple pin-floor composition;
16. demotion blocked below effective pin floor;
17. unknown pin rejection;
18. consumed pin rejection;
19. unpin without automatic demotion;
20. dense materialization success;
21. dense materialization failure atomicity;
22. dense-view lifetime invalidation on demotion;
23. runtime close cleanup;
24. close idempotence;
25. operation rejection after close;
26. source-file immutability;
27. no unverified-byte escape;
28. runtime snapshot/accounting consistency;
29. concurrent same-object promotion safety;
30. concurrent pin/unpin accounting safety;
31. concurrent observation sees no provisional state;
32. no duplicate ownership under promotion races.

## 44. Resource diagnostics before Phase 6C runtime acceptance

Before the Phase 6C runtime is considered complete, diagnostics must examine
at least:

- retained serialized buffers after demotion;
- retained dense views after demotion;
- pin-token leakage;
- descriptor leakage where descriptors are used;
- mapping leakage where mappings are used;
- RSS growth where measurable;
- GC-tracked runtime-object growth;
- repeated promotion/demotion degradation;
- repeated failure-path degradation;
- unexpected source-file writes;
- runtime close cleanup;
- concurrency stress invariants.

Thresholds belong to a separately frozen diagnostic protocol after the engine
and validation design are known.

## 45. Performance questions remain prospective

After correctness, benchmarks may compare candidate strategies for:

- attach/detach overhead;
- verified promotion latency;
- repeated object access;
- dense materialization latency;
- explicit demotion latency;
- cache/policy behavior;
- resident-byte efficiency;
- descriptor/mapping strategies;
- concurrent access.

No candidate strategy is selected by this protocol.

## 46. Automatic eviction remains a separate policy experiment

LRU, TinyLFU, CLOCK-style, frequency-aware, reuse-aware, and other automatic
admission/eviction strategies remain candidate policies.

The first V1 runtime may expose explicit deterministic demotion and budgets
without choosing an automatic policy.

This separation is intentional.

## 47. Benchmark evidence required for backend promotion

A concrete backend may be promoted only after prospective comparison against
appropriate controls.

Examples include:

- ordinary verified `pread` behavior;
- persistent descriptor strategies;
- mmap-based strategies;
- other local storage approaches.

Measurements must include correctness and resource costs, not latency alone.

## 48. No Phase 6B rewrite

Phase 6C must not modify Phase 6B evidence to make a runtime strategy easier.

In particular, Phase 6C must not silently change:

- ResidentPKEntry semantics;
- Segment Reader verification semantics;
- active-generation authority;
- rollback semantics;
- accepted benchmark results;
- accepted diagnostic results.

A necessary predecessor correction requires a successor version.

## 49. Initial implementation target

After this protocol itself is frozen in Git, the next authorized engineering
step is construction of a minimal V1 runtime engine that implements this
observable contract.

That first engine must remain:

- process-local;
- backend-neutral;
- persistent-source read-only;
- explicit-policy rather than automatic-eviction driven;
- generation-bound;
- integrity preserving.

Implementation must not be benchmark-tuned before validation.

## 50. Initial implementation nonrequirements

The first V1 engine is not required to provide:

- OS mmap;
- long-lived file descriptors;
- automatic eviction;
- asynchronous I/O;
- prefetch;
- Vulkan;
- multithread speedup;
- production database integration;
- MAF-native computation.

These remain later measured decisions.

## 51. Acceptance boundary

This protocol is a design freeze only.

Protocol construction does not mean runtime correctness exists.

Protocol freeze does not mean runtime correctness exists.

Runtime implementation does not mean validation passed.

Validation success does not mean performance advantage exists.

Performance advantage does not mean production readiness exists.

Each claim requires its own frozen evidence.

## 52. Phase status after protocol freeze

After this protocol is committed:

- Phase 6B remains COMPLETE / CLOSED;
- Phase 6C remains STARTED / RESEARCH CURRENT;
- the Phase 6C V1 runtime contract is frozen;
- Phase 6C runtime implementation becomes authorized;
- no backend choice is implied;
- no runtime correctness claim exists until validation.

## 53. Immutability rule

Once this protocol is frozen in Git, implementation must conform to it.

If a material design defect is found before accepted execution, correction
must be explicit and prospectively frozen.

If a protocol-constrained experiment has already executed, its protocol and
result remain immutable historical evidence.

No result may be rewritten to fit this design.

## 54. Research discipline

The purpose of V1 is to establish a falsifiable runtime correctness boundary,
not to prove the full MAF architecture.

A successful V1 means only that OpenMind can manage generation-bound MAF
objects through a defined, integrity-preserving, resource-accounted
residency state machine under the frozen test conditions.

It does not establish replacement of a conventional LLM runtime.
