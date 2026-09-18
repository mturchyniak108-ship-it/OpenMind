# OpenMind MAF Dense Compute View Boundary V1 Protocol

Status: Frozen Phase 6A research boundary.

Schema:

    openmind.maf_dense_compute_view_boundary.v1


## 1. Purpose

This protocol closes Phase 6A Step 7:

> Preserve dense tensors as optional compute/materialization views until
> MAF-native computation is independently validated.

It defines an architectural boundary only.

It does not implement dense materialization.


## 2. Governing principle

The persistent MAF representation remains the stored model-object
representation produced by the Phase 6A compiler.

A conventional dense tensor is not the persistent authority of a
compiled MAF object.

A dense tensor may later exist as a derived compute or compatibility
view.


## 3. Persistent authority

For Phase 6A:

    persistent authority = completed MAF object bytes

The authoritative persistent numerical payload remains the exact
validated MAF Object V1 payload.

Creation or destruction of a dense compute view must not alter:

- model_pk;
- object_pk;
- fragment_pk;
- persistent MAF object bytes;
- persistent payload SHA256;
- physical segment bytes.


## 4. Dense view status

A dense compute view is:

- derived;
- optional;
- non-authoritative;
- non-identity-bearing;
- disposable;
- reproducible from validated persistent state under a future
  independently specified materialization contract.

The existence of a dense view does not create a new logical MAF
object.


## 5. No eager materialization requirement

Phase 6A does not require a dense tensor to be created:

- during scanning;
- during classification;
- during planning;
- during encoding;
- during segment construction;
- when a persistent MAF object is reopened.

Persistent MAF validity must not depend on a dense view being resident.


## 6. No dense-view identity

A dense materialization must not derive or replace:

- model_pk;
- object_pk;
- fragment_pk;
- route identity;
- physical generation identity.

Any later cache key or materialization handle is runtime state and
must remain separate from logical identity.


## 7. Numerical fidelity boundary

This protocol does not define numerical decoding.

In particular it does not define:

- F32 compute-buffer construction;
- Q8_0 dequantization;
- quantization conversion;
- dtype promotion;
- layout conversion;
- tensor transpose;
- device-specific packing;
- kernel-specific representation.

Those require independently frozen implementation and fidelity
protocols.


## 8. Exact persistent bytes remain canonical

Materialization must never require rewriting the persistent MAF object
in place.

The immutable stored representation remains recoverable after any
derived compute view is released.

Eviction of a dense view must not require reserialization of canonical
MAF bytes.


## 9. Runtime residency boundary

This protocol does not assign runtime residency.

It does not create or transition:

- COLD_DISK;
- MAPPED;
- HOT_MAF;
- HOT_DENSE;
- VULKAN_MAF.

Residency state machines belong to Phase 6C.


## 10. On-demand materialization boundary

Actual on-demand dense materialization belongs to the MAF Object
Runtime and Residency work in Phase 6C.

Phase 6A only preserves architectural permission for such a derived
view.


## 11. Selective materialization boundary

This protocol does not establish that a complete dense tensor can be
avoided.

It does not define:

- partial tensor reconstruction;
- fragment-level reconstruction;
- selective dense materialization;
- tensor avoidance;
- sparse compute views.

Those are Phase 6E research questions.


## 12. MAF-native compute boundary

MAF-native compute remains:

    disabled_unvalidated

A valid persistent MAF object or segment does not establish that
inference can operate directly on MAF bytes.

Direct MAF-native compute may only be enabled after independent
numerical and inference-fidelity validation.


## 13. Existing dense compute compatibility

Existing conventional dense compute paths remain permitted.

Such compatibility does not make dense tensors the persistent model
representation.

The intended relationship is:

    persistent MAF
        ->
    optional derived dense compute view
        ->
    existing compute path

until a MAF-native compute path independently passes fidelity gates.


## 14. Source-model isolation

A future dense materializer should operate from validated persistent
MAF state where possible.

Phase 6A does not require reopening the source GGUF merely to create
or preserve the dense-view boundary.

This protocol itself performs no source-model access.


## 15. Segment independence

Segment placement does not change dense-view semantics.

Whether a MAF object is standalone or stored as an exact byte range
inside a segment:

- logical identity remains unchanged;
- dense-view status remains derived;
- physical segment offset is not compute identity.


## 16. Cache semantics

Dense-view caching is not defined here.

This protocol does not define:

- cache admission;
- cache eviction;
- cache size;
- byte budgets;
- pinning;
- reuse policy;
- prefetch;
- materialization counters.

Those belong to Phase 6C and Phase 6D.


## 17. Device semantics

This protocol does not define CPU, ARM64, NEON, Vulkan, GPU, or other
device materialization.

Device-specific compute representations are later runtime and
optimization concerns.


## 18. No performance claim

Closing Phase 6A Step 7 establishes no claim of:

- lower RAM;
- lower storage;
- lower payload traffic;
- lower latency;
- higher throughput;
- reduced tensor access;
- selective execution;
- acceleration.

Those require measurement.


## 19. No compression claim

The dense-view boundary does not authorize:

- lossy conversion;
- requantization;
- compression;
- deduplication;
- sparse approximation;
- residual approximation.

Persistent fidelity remains governed by the existing frozen MAF
protocols.


## 20. Failure semantics

A future dense materialization failure must not invalidate or mutate
the persistent MAF object.

Failure to create a derived compute view is a runtime/compute failure,
not permission to rewrite canonical persistent bytes.


## 21. Phase 6A completion condition

For Step 7, Phase 6A requires only that the boundary be frozen such
that:

- persistent MAF remains authoritative;
- dense compute tensors remain optional derived views;
- dense views do not alter logical identity;
- no eager dense materialization is required;
- runtime materialization remains deferred to Phase 6C;
- selective materialization remains deferred to Phase 6E;
- MAF-native compute remains disabled pending independent validation.

No dense-view engine is required to satisfy this Phase 6A boundary.


## 22. Required later validation

Before production dense materialization is promoted, later work must
independently validate at minimum:

- exact object-to-compute-view interpretation;
- dtype and shape correctness;
- quantization/dequantization semantics where applicable;
- numerical agreement with an untouched oracle;
- lifecycle and failure cleanup;
- bounded allocation behavior;
- cache/residency interaction;
- source-GGUF independence where claimed.

Selective materialization requires additional Phase 6E validation.


## 23. Nonclaims

This protocol does not prove:

- dense reconstruction implementation;
- Q8_0 decoding correctness;
- inference correctness;
- model replacement;
- selective reconstruction;
- fragment retrieval;
- tensor avoidance;
- MAF-native kernels;
- runtime residency;
- cache behavior;
- mmap behavior;
- Vulkan execution;
- performance improvement.


## 24. Phase relationship

Phase 6A:

    persistent representation and compiler boundary

Phase 6B:

    catalog and physical object resolution

Phase 6C:

    runtime residency and on-demand dense materialization

Phase 6D:

    locality and repacking

Phase 6E:

    selective access, tensor avoidance, and selective dense
    materialization

Only after those fidelity boundaries pass may direct MAF-native
computation be evaluated for promotion.
