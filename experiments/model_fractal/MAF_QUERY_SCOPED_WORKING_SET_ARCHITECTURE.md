# MAF Query-Scoped Working Set Architecture

Status: PROPOSED RESEARCH ARCHITECTURE

Phase: 6D-Q

Scientific validation status: NOT VALIDATED

Runtime integration status: NOT AUTHORIZED

Phase 6E status: NOT ENTERED

## Purpose

This document records a proposed architectural bridge between the Phase 6D
persistent/locality work and Phase 6E selective MAF execution.

The core proposal is to compile each user input into a query-scoped MAF working
set derived from canonical MAF object PKs rather than treating every inference
as an unconditional request for the complete model representation.

The proposal does not claim that useful PK subsets can already be selected, that
a subset can already answer an arbitrary prompt, or that this architecture is
faster than a conventional LLM runtime. Those are future experimental claims.

## Architecture summary

The proposed system separates three authorities.

### 1. Canonical MAFDB

MAFDB remains the immutable source of model truth.

Its responsibility is to resolve stable logical PK identity to persistent MAF
objects and their physical storage locations.

Canonical MAFDB data is not deleted when a query finishes.

A query route never becomes canonical model truth.

### 2. Query-Scoped MAF Capsule

A Query-Scoped MAF Capsule is a derived, temporary execution description for
one input.

It may contain:

- query PK;
- deterministic query signature;
- source generation PK;
- source manifest SHA256;
- initial selected object PKs;
- selected relationship or transition PKs where applicable;
- deterministic route order;
- expansion policy;
- maximum object budget;
- maximum expansion rounds;
- selection/configuration SHA256.

The capsule should preferentially reference immutable MAFDB objects rather than
duplicate model payloads.

An early proof-of-concept may physically materialize a temporary subset if that
is required to prove feasibility, but duplicated query materialization is not
the preferred final architecture.

### 3. Reusable MAF Query Route Cache

The Query Route Cache is persistent derived metadata describing successful
routes through canonical MAF objects.

A route cache entry may contain:

- exact query hash;
- query feature/signature representation;
- source generation PK;
- initial PK route;
- additional PKs requested during bounded expansion;
- PKs actually touched;
- PKs selected but unused;
- route/configuration SHA256;
- validation or quality metadata where scientifically authorized.

The route cache stores how the engine reached useful model state.

It should not be treated as a cache of canonical truth and should not silently
replace model inference with a previously generated answer.

## Proposed inference flow

User input

    -> deterministic query signature
    -> exact prior-route lookup
    -> similar-route candidate lookup if authorized
    -> PK candidate selector
    -> Query-Scoped MAF Capsule
    -> attach capsule to MAF execution engine
    -> selectively resolve/materialize required PKs
    -> determine whether the current working set is sufficient
    -> bounded PK-neighbor/relationship expansion when required
    -> produce answer
    -> record actual PK usage
    -> release all engine ownership
    -> detach query capsule
    -> retire ephemeral materialization
    -> preserve compact reusable query-route metadata

## Initial selection is not required to be perfect

The architecture should not require a query compiler to identify the entire
correct working set before execution begins.

The initial selection may instead be a bounded seed set.

If execution proves that the seed is insufficient, the engine may request
additional PKs through a preregistered expansion mechanism.

This creates a selective-access loop:

    initial PK set
    -> execute
    -> sufficient?
       -> yes: answer
       -> no: request bounded adjacent/related PKs
              -> execute again

A failed initial selection must therefore be recoverable rather than silently
producing a degraded answer.

## Cleanup semantics

Cleanup applies only to query-scoped derived state.

The proposed order is:

1. finish answer generation;
2. freeze query execution evidence needed for interpretation;
3. release dense/materialized views;
4. release MAF object ownership;
5. close query-owned descriptors/maps;
6. detach the Query-Scoped MAF Capsule;
7. delete or unlink ephemeral query materialization;
8. preserve only the reusable query-route record when policy allows it.

Canonical MAFDB objects and active generation authority must not be deleted by
query cleanup.

No path may be unlinked while the execution engine still owns it.

## Query-route reuse

Future inputs should first test whether a previously validated route can provide
a useful starting point.

Reuse may have several levels:

- exact query-hash route reuse;
- normalized-query route reuse;
- similar-query route candidate reuse;
- no useful prior route, requiring fresh PK selection.

Similarity must not imply identity.

A reused route remains a candidate working set and may require expansion.

Route reuse should be generation-bound. A route created against one source
generation must not silently become authoritative for another generation.

## Proposed telemetry

Query-scoped execution should eventually expose derived telemetry including:

- number of initial PKs selected;
- number of PKs actually touched;
- selected-but-unused PK count;
- number of expansion rounds;
- number of additional PKs fetched;
- serialized MAF bytes read;
- dense bytes materialized;
- cache hits and misses;
- route-cache exact hit;
- route-cache similarity hit;
- route-cache miss;
- answer-equivalence or quality evidence where separately preregistered.

These measurements can feed Phase 6D locality work without changing canonical
model truth.

## Scientific questions

The architecture creates several independent hypotheses.

### Q1 — Query-route representation

Can a query-scoped PK route be represented deterministically and bound to an
immutable source generation?

### Q2 — PK selection feasibility

Can an input select a bounded PK candidate set without using oracle knowledge
from the expected answer?

### Q3 — Selective sufficiency

Can the selected MAF working set produce an acceptably equivalent result to the
authorized full-reference execution?

### Q4 — Bounded expansion

When the initial PK set is insufficient, can deterministic expansion recover the
required model state?

### Q5 — Avoidance

Can the system prove that MAF objects outside the successful route were not read
or materialized?

Avoidance requires actual access evidence. Merely ignoring an object after it
was loaded does not count.

### Q6 — Route reuse

Do similar future inputs benefit from previously successful PK routes without
silently reducing answer quality?

### Q7 — Cleanup correctness

Can ephemeral query state be retired without altering canonical MAFDB state,
active generation authority, or reusable route evidence?

## Proposed roadmap placement

### Phase 6D-Q1 — Query Capsule Data Model

Freeze deterministic Query Capsule and Query Route Cache schemas.

No inference claim.

### Phase 6D-Q2 — Query-to-PK Selection Prototype

Test whether query-derived signals can select bounded PK candidates without
answer leakage.

No selective-inference claim yet.

### Phase 6D-Q3 — Attach / Detach / Cleanup

Prove query-scoped working-set lifecycle, ownership, failure atomicity, and
ephemeral cleanup.

No performance claim.

### Phase 6D-Q4 — Query Route Cache

Test exact and similar-query route reuse with strict source-generation binding.

No claim that semantic route reuse improves generation quality until measured.

### Phase 6E-A — Selective Sufficiency

Compare query-scoped execution with an authorized full-reference execution.

### Phase 6E-B — Bounded Expansion

Prove deterministic recovery when the initial working set is incomplete.

### Phase 6E-C — Tensor / Object Avoidance

Prove that unnecessary model objects are genuinely avoided.

### Phase 6E-D — Output Parity and Quality

Measure the effect of selective execution on output behavior under a separately
frozen evaluation protocol.

### Phase 6F — Performance and Scaling

Only after correctness and selective-access claims are established should the
project measure latency, throughput, memory, I/O, multithread scaling, and
device-specific performance.

## Relationship to Phase 6D locality

Query routes can become a strong source of path telemetry.

Repeated successful PK sequences may reveal physical colocations that should be
tested by the Phase 6D locality/repacking experiments.

This does not authorize a locality planner to optimize against answer/test
oracle information.

Training telemetry, route-cache construction, and locality evaluation must
retain prospective train/evaluation separation.

## Persistence note

The current frozen telemetry snapshot Persistence V1 remains a separate
scientific lineage.

Its Android Python hard-link incompatibility and frozen unexecuted Validation V1
are not resolved by this architecture document.

Any persistence mechanism used by Query Capsules or Query Route Cache artifacts
must receive its own platform-compatible correctness protocol before becoming
authoritative.

## Nonclaims

This architecture document does not establish:

- prompt-to-PK selection correctness;
- selective model sufficiency;
- answer parity;
- reduced tensor reads;
- reduced model loading;
- reduced memory;
- improved latency;
- improved throughput;
- MAF-native inference;
- replacement of llama.cpp or another LLM runtime;
- generalization of route reuse to unseen prompts;
- production-ready MAFDB behavior.

It records the proposed architecture and experimental sequence only.
