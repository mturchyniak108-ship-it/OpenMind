# MAF Resident PK Directory V1 — Phase 6B.9 Completion

## Status

**COMPLETE / VALIDATED / BENCHMARKED / DIAGNOSTICALLY ACCEPTED**

Phase 6B.9 is closed by frozen functional, benchmark, and diagnostic evidence.

The Resident PK Directory implementation itself is unchanged by this completion checkpoint.

## Frozen implementation identity

Protocol SHA256: `5d053b52963a10285f21a600aa0bb257b0ad645f12a9a36417cfa6f77a017939`

Engine SHA256: `4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6`

Core invariant:

Stable logical PK + exact active physical generation + validated immutable descriptor mapping -> immutable resident snapshot -> direct generation-bound lookup.

## Functional validation

Runner SHA256: `8dcf90a3a076cc84ff290b3d4443534044b735d5d2cd3767014a34dc12473257`

Result SHA256: `24540c16eac53e9a179781c7007d61d98b34f7bc74e1f3dfc462b5786dd186b1`

- exact-once validation completed successfully;
- 37 / 37 positive checks passed;
- 11 / 11 static checks passed;
- 22 / 22 negative checks passed;
- stale generation and stale snapshot behavior validated;
- failed refresh preserved the prior resident snapshot;
- duplicate and malformed mappings were rejected;
- synthetic/non-authoritative PK cases were rejected.

Functional validation is historical evidence and must not be rerun merely to reproduce this checkpoint.

## Resident-directory benchmark

Correction protocol SHA256: `d35aca6c8c98d891761f6fbfb176e3b7fc385d466d03e07ae3125892015b61ef`

Runner SHA256: `f9b8d1560eab35ce9340e00cfd7cb2b3683765fbf5b085544ee7f21d8f97a28e`

Result SHA256: `57562c9fbcac012c6706903ff07c23a15b5bf59bb0599a9f6dd04ceecbec95b1`

- Benchmark V1 failed once because its runner passed a list where Activation required a segment-path mapping; that failed lineage remains preserved and rerun-forbidden.
- Benchmark V1.1 corrected only that runner defect and executed exactly once successfully.
- direct lookup median scaling ratio: 1.0 over the preregistered tested range;
- direct lookup p95 scaling ratio: approximately 1.3985;
- linear lookup growth ratio: approximately 100.35;
- 100K-entry direct lookup median: 260 ns;
- 100K-entry linear lookup median: 3,742,318 ns;
- observed 100K direct-vs-linear speedup: approximately 14,393.5x;
- 100K peak resident-memory observation: 40,343,704 bytes, approximately 403.44 bytes/entry;
- build median: 242,864 ns;
- refresh median: 237,422 ns.

These results support O(1)-style resident lookup over the tested range and device only. They are not a universal production-performance guarantee.

## Post-validation diagnostics

Diagnostics V1.4 correction protocol SHA256: `dbb86b4ef1c9cb01efeda00893b8710562895bd347145540335bb20303c1d337`

Diagnostics V1.4 runner SHA256: `1d01720bd0bd88bcfcc522af70876e134d12d3b9763fd56cc23975f9f7d5c694`

Diagnostics V1.4 raw-result SHA256: `9f665383917560327b05673206a8b385d9312386077bbb741878d49866ce29b0`

Diagnostics V1, V1.1, V1.2, and V1.3 were never executed and remain forbidden.

Diagnostics V1.4 passed its final frozen-state preflight and then executed exactly once.

Frozen V1.4 result:

- process return code: 0;
- all_pass: true;
- 45 / 45 checks passed;
- failed checks: none;
- fatal error: none;
- post-setup write-intent opens: 0;
- stale-generation rejection: 200 / 200;
- expected stale exception: MAFResidentPKDirectoryStaleSnapshotError;
- observed stale exception set: exactly MAFResidentPKDirectoryStaleSnapshotError;
- build degradation ratio: 0.9976532401988844 <= 2.5;
- repeated hash/file-validation degradation ratio: 0.9976532401988844 <= 2.5;
- lookup degradation ratio: 1.0174011616149072 <= 2.0;
- refresh degradation ratio: 0.9986062600462365 <= 2.5;
- 26 resource-related acceptance checks passed;
- 4 sustained-degradation checks passed;
- 10 stale-state surface checks passed;
- 8 failure-path checks passed.

The diagnostic runtime remains preserved and must not be cleaned as part of this checkpoint.

## Accepted diagnostic surfaces

The frozen evidence covers:

- logic and invariant violations;
- exception-path corruption;
- stale-state mistakes;
- partial-publication behavior;
- repeated build and refresh behavior;
- retained Python-object growth;
- tracemalloc retained-memory growth;
- RSS growth where measurable;
- file-descriptor growth;
- runtime-file accumulation;
- unexpected write-intent filesystem opens;
- repeated build/hash/file-validation degradation;
- lookup degradation;
- refresh degradation;
- failure-path snapshot preservation;
- exact stale-generation rejection semantics.

## Historical execution constraints

- Functional validation V1: historical exact-once evidence; do not rerun.
- Benchmark V1: historical failed exact-once evidence; rerun forbidden.
- Benchmark V1.1: historical successful exact-once evidence; rerun forbidden.
- Diagnostics V1 through V1.3: never executed; execution forbidden.
- Diagnostics V1.4: historical successful exact-once evidence; rerun forbidden.

## Bounded claims / nonclaims

This completion establishes the Resident PK Directory V1 behavior and evidence required for Phase 6B.9.

It does **not** establish:

- a universal production latency guarantee;
- a universal memory-cost guarantee;
- a final storage-engine selection;
- a Segment Reader implementation;
- MAF-native tensor compute;
- tensor-avoidance execution;
- Phase 6C object residency/runtime completion;
- production deployment readiness.

## Next phase

Phase 6B.10 — Segment Reader V1 is the next research gate.

It is not started by this completion checkpoint.
