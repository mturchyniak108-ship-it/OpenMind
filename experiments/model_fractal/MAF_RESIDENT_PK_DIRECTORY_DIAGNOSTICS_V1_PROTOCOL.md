# MAF Resident PK Directory Diagnostics V1 Protocol

## Status

PREREGISTERED. Freeze before any diagnostic execution.

## Purpose

This suite searches for correctness and degradation defects that can remain invisible after syntax checks, functional validation, and short microbenchmarks.

It is specifically intended to detect logic errors, failure-path corruption, retained-object growth, memory/resource leaks, file-descriptor leaks, unexpected filesystem activity, runtime-file accumulation, and sustained performance degradation.

## Frozen evidence inputs

Resident PK Directory engine SHA256: 4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6

Functional validation result SHA256: 24540c16eac53e9a179781c7007d61d98b34f7bc74e1f3dfc462b5786dd186b1

Accepted Benchmark V1.1 result SHA256: 57562c9fbcac012c6706903ff07c23a15b5bf59bb0599a9f6dd04ceecbec95b1

Retained Benchmark V1.1 candidate SHA256: 941301aa362d3f949389e5364b1be4d7f26b96f0d45efa81346c82fce3260f93

Retained Benchmark V1.1 active-record SHA256: 031d1a50a3cf53f158057a02bb6c68001edfb07bf48bf893afc9bc8f095458e9

The Benchmark V1.1 runtime is read-only source evidence.

Diagnostics must copy required evidence into a new isolated diagnostic runtime.

Neither benchmark runtime may be modified or cleaned.

## Exact-once rule

The diagnostic runner may execute only when both its result and runtime are absent.

The runner creates the diagnostic runtime once.

It publishes one raw result exactly once.

A negative or fatal diagnostic run is evidence and must not be automatically retried.

## Logic diagnostics

1. Build a fresh snapshot from isolated exact copies of the accepted active generation.
2. Require a non-empty exact resident directory.
3. Require repeated direct lookup to return the exact resident entry.
4. Require the resident MappingProxyType surface to reject mutation.
5. Require frozen resident entries to reject field mutation.
6. Rebuild the snapshot 200 times and require identical logical/physical projection digests.
7. Refresh successfully and require the manager current snapshot to equal the returned replacement.
8. Perform 200 intentionally invalid refreshes and require every failure to preserve the prior current snapshot by object identity.
9. Require the final logical/physical projection digest to equal the initial digest.

## Hot-path I/O diagnostic

Install a process-local Python audit hook after setup.

During a dedicated 50,000-lookup block, require zero new filesystem open events.

The diagnostic applies only to the ResidentPKSnapshot.lookup hot path.

## Memory and object-retention diagnostics

After warmup and garbage collection, use tracemalloc to measure retained current allocation rather than transient peak allocation.

Direct lookup retained growth after 100,000 lookups must be <= 262,144 bytes.

Successful refresh retained growth after 500 refreshes must be <= 1,048,576 bytes.

After garbage collection, live ResidentPKSnapshot object count may grow by at most 2 objects relative to the warmed baseline.

These limits are leak/regression sentinels, not production memory guarantees.

## Process-resource diagnostics

On Android/Termux, read /proc/self/status for VmRSS and /proc/self/fd for descriptor count.

Across the sustained diagnostic workload:

- RSS growth must be <= 16 MiB;
- open file-descriptor growth must be <= 2;
- diagnostic runtime file count must not grow after setup;
- diagnostic runtime byte count must not grow after setup.

## Sustained degradation diagnostics

Lookup degradation:

- 2 warmup batches;
- 20 measured batches;
- 5,000 lookups per batch;
- compare median ns/op of first 5 measured batches with last 5;
- final/initial ratio must be <= 2.0.

Refresh degradation:

- 2 warmup batches;
- 20 measured batches;
- 25 refreshes per batch;
- compare median ns/op of first 5 measured batches with last 5;
- final/initial ratio must be <= 2.5.

No absolute latency target is introduced by this suite.

## Failure behavior

A diagnostic check may fail without making the diagnostic runner itself invalid.

All check outcomes and raw measurements must be written to the raw result.

Unexpected exceptions must be converted into a fatal raw diagnostic result where possible.

No automatic retry is permitted.

## Nonclaims

Passing diagnostics does not prove absence of all memory leaks or all logic defects.

Passing diagnostics does not establish universal production latency or memory guarantees.

This suite does not implement Segment Reader V1.

It does not select a storage engine.

It performs no inference or tensor math.

It does not require or access the source GGUF.

It does not begin Phase 6C.
