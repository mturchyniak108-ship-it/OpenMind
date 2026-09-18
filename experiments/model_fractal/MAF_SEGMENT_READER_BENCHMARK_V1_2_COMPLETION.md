# MAF Segment Reader Benchmark V1.2 Completion

Status: COMPLETE / SUCCESS RESULT FROZEN / DO NOT RERUN

## Frozen identities

- Preregistration commit:
  `cb97a5fb76a5f98c7b1cd34dd7496eac4707ba62`
- Result-freeze commit:
  `a524d71d46090a42a7ac6b69582ca79ca699e65f`
- Protocol SHA256:
  `c49c75fee93b28805f03280a775f703c2395826124c43993f97ff3358367c5db`
- Runner SHA256:
  `29f8312e874a76005832855f187376faae63cd4534e1f606866d519cf26a751f`
- Result SHA256:
  `44b15ba5a02492f9a7c79cda3120c0cb4b6b398201eacb5f5249f38a281e5a54`
- Result bytes:
  `323334664`
- Schema:
  `openmind.maf_segment_reader_benchmark.v1_2`
- `benchmark_valid`:
  `true`

V1.2 executed exactly once and must never be rerun or modified.

## Execution integrity

The result contains:

- 14,000 measured samples;
- 12,000 normal cluster-0 samples;
- 2,000 prospective micro cluster-1 samples;
- 0 normal-lane hard stops;
- 0 observation-gap violations;
- 378 micro-lane hard-stop observations.

All ten frozen result integrity checks passed, including affinity restoration,
file-descriptor balance, source immutability, topology identity and dependency
identity.

## Thermally stratified normal-lane evidence

Normal samples:

- thermally eligible: 7,049 / 12,000;
- thermally ineligible: 4,951 / 12,000.

Thermally eligible results:

| Mode | n | Median | p95 | Mean |
| --- | ---: | ---: | ---: | ---: |
| direct_nohash_reference | 2327 | 8.125 us | 9.531 us | 8.390 us |
| reader_v1 | 2358 | 10.834 us | 12.552 us | 11.260 us |
| whole_segment_hash_reference | 2364 | 12.083 us | 13.750 us | 12.650 us |

At the eligible median:

- `reader_v1` is approximately 33.34% higher latency than unchecked direct
  access;
- `reader_v1` is approximately 10.34% lower latency than whole-segment hashing;
- absolute reader overhead versus direct access is approximately 2.709 us;
- reader advantage versus whole-segment hashing is approximately 1.249 us.

The same ordering remained present in the thermally ineligible population:

`direct_nohash_reference < reader_v1 < whole_segment_hash_reference`.

This supports the conclusion that the normal-lane ordering is not an artifact
of thermal stratification.

## CPU placement

Eligible sample retention:

- CPU0: 4,766 / 6,000 = 79.43%;
- CPU3: 2,283 / 6,000 = 38.05%.

Eligible reader medians:

- CPU0: 10.938 us;
- CPU3: 10.729 us.

CPU3 is approximately 1.91% faster for the eligible reader observations, but
CPU0 retained thermal eligibility far more reliably.

Therefore:

- CPU0 is the preferred sustained Phase-6B normal-lane placement on this
  device;
- CPU3 is a valid, slightly faster eligible secondary placement.

This is device-specific evidence and not a universal scheduling rule.

## Cluster-1 micro lane

The cluster-1 micro experiment did not establish a thermally controlled
crossover.

Thermal eligibility:

- CPU6: 1 eligible / 1,000 measured samples;
- CPU7: 0 eligible / 1,000 measured samples;
- combined: 1 / 2,000 = 0.05%.

Hard-stop observations:

- CPU6: 57;
- CPU7: 321;
- combined: 378.

Observed 512-byte cluster-1 versus cluster-0 median latency ratios were:

- reader_v1: 1.5264x;
- direct_nohash_reference: 1.4359x.

These measurements describe the observed thermally uncontrolled cluster-1
conditions only.

V1.2 therefore does NOT establish that cluster 1 is intrinsically slower and
does NOT establish a valid size-dependent cluster crossover.

The crossover question remains unresolved.

## Engineering interpretation

MAF Segment Reader V1 demonstrates bounded structured object access at roughly
10.8 us median latency under thermally eligible normal-lane conditions on the
tested Android device and fixtures.

The reader is measurably slower than an unchecked direct reference but faster
than the whole-segment hash reference.

This is useful evidence that structured MAF access can remain within a small
microsecond-scale overhead of direct access while avoiding the latency of
whole-segment verification.

## Scope boundary

This result does not establish:

- production storage-engine readiness;
- multithread or concurrency scaling;
- universal thermal safety;
- universal CPU-placement policy;
- a valid cluster-1 crossover;
- selective tensor avoidance;
- MAF-native LLM replacement;
- generalization beyond the tested device, fixtures and runtime.

Phase 6C is not declared started by this record.

## Next research gate

Perform a read-only Phase-6B exit and roadmap alignment audit.

Determine whether:

1. the current reader/storage evidence satisfies Phase-6B exit criteria;
2. the unresolved cluster-1 crossover is optional or blocking;
3. Phase 6C concurrency work may begin;
4. any remaining Phase-6B experiment should be preregistered first.

## Classification

`MAF_SEGMENT_READER_BENCHMARK_V1_2_COMPLETE_SUCCESS`
