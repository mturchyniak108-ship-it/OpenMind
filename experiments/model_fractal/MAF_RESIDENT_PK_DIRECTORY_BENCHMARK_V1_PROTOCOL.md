# MAF Resident PK Directory Performance Benchmark V1 Protocol

## Status

PREREGISTERED. This protocol must be frozen before benchmark execution.

## Purpose

Measure Resident PK Directory V1 performance without changing its frozen functional contract.

The benchmark evaluates four separate properties:

1. direct resident `object_pk` lookup latency distribution;
2. scaling of direct lookup as resident entry count increases;
3. direct lookup versus an explicit linear-scan baseline;
4. actual current-generation snapshot build and same-generation refresh cost;
5. resident snapshot memory scaling.

## Evidence boundary

The benchmark must bind to the already-frozen Resident PK Directory engine and functionally accepted validation result.

It must not rerun the frozen functional validation runner.

It must not modify frozen functional evidence.

It must not access a source GGUF.

It must not perform inference, tensor math, Segment Reader work, MAF-native compute, generation deletion, or storage-engine selection.

## Benchmark environment

The benchmark is a device-local Python microbenchmark.

Its results apply to the measured device and software environment. They are not a universal production latency guarantee.

## Lookup scaling sizes

The exact preregistered resident entry counts are:

- 100
- 1,000
- 10,000
- 100,000

## Lookup repetitions

The exact timed repetition counts are:

- 100 entries: 2,000 repetitions
- 1,000 entries: 1,000 repetitions
- 10,000 entries: 250 repetitions
- 100,000 entries: 50 repetitions

Each size uses a deterministic terminal key so the linear baseline traverses the complete resident mapping.

## Direct lookup measurement

Direct lookup must call the frozen `ResidentPKSnapshot.lookup` method.

Each timed sample records one lookup using `time.perf_counter_ns`.

Median and p95 latency are recorded for every size.

The measured direct lookup section must not include JSON parsing, manifest scanning, filesystem discovery, physical validation, or snapshot construction.

## Linear baseline

The baseline must apply the same model, generation, and PK-class checks and then explicitly iterate resident entries until the requested key is found.

Median and p95 latency are recorded for every size.

## Actual build and refresh measurement

The benchmark creates an isolated benchmark runtime from retained validated Activation evidence.

The setup activates retained candidate A inside that isolated benchmark runtime.

Setup time is not counted as Resident PK Directory build time.

The benchmark then measures:

- 10 calls to `build_snapshot` after two warmups;
- 10 same-generation `ResidentPKDirectory.refresh` calls after two warmups.

Median and p95 latency are recorded.

Build and refresh must use the frozen current physical-validation semantics.

## Memory scaling

For every preregistered lookup size, construct the same synthetic immutable resident snapshot under `tracemalloc`.

Record current allocated delta, peak allocated delta, and peak bytes per entry.

Memory measurements are descriptive evidence and have no V1 pass threshold.

## Preregistered scaling acceptance criteria

Functional benchmark execution passes only if all of these are true:

1. every timed direct lookup returns the exact requested canonical entry;
2. all four lookup sizes complete their preregistered repetition counts;
3. direct median latency max/min ratio across 1,000, 10,000, and 100,000 entries is at most 4.0;
4. direct p95 latency max/min ratio across 1,000, 10,000, and 100,000 entries is at most 6.0;
5. linear median latency at 100,000 entries divided by linear median latency at 1,000 entries is at least 20.0;
6. direct median lookup at 100,000 entries is lower than linear median lookup at 100,000 entries;
7. all 10 measured actual snapshot builds succeed;
8. all 10 measured same-generation refreshes succeed;
9. all four memory measurements complete with positive peak allocation.

These thresholds test scaling behavior. They do not create an absolute production latency guarantee.

## Result publication

The benchmark runner writes one raw JSON result exclusively.

The runner must refuse execution when either its result or benchmark runtime already exists.

A failed or negative benchmark must be preserved and must not be automatically rerun.

## Completion boundary

Phase 6B.9 remains incomplete until the frozen benchmark is executed exactly once, its raw result is frozen, and that result is interpreted separately.

Benchmark success does not implement Segment Reader V1 and does not begin Phase 6C.
