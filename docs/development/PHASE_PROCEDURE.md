# MAF Standard Experimental Phase Procedure

## Purpose

Every MAF research phase follows the same evidence-driven lifecycle.
No experimental result becomes a production capability merely because it appears promising.

## Standard Lifecycle

1. Define the hypothesis.
2. Identify the Canonical Model Artifact and source artifacts.
3. Record provenance and hashes.
4. Establish a baseline.
5. Build the smallest experimental component.
6. Capture raw evidence without overwriting source data.
7. Measure accuracy, token usage, latency, RAM, storage, CPU, GPU, and energy/resource behavior where available.
8. Test against independent prompts and holdout data.
9. Preserve contradictory, rejected, pruned, and terminated paths when they contain useful information.
10. Compare against the baseline.
11. If the result is promising, componentize the complete phase.
12. Implement the validated component in native C++.
13. Compile and benchmark the C++ implementation.
14. Optimize the execution pathway for the target device.
15. Re-run the original experiment against the optimized implementation.
16. Record regression and improvement measurements.
17. Update README, ROADMAP, TODO, AI instructions, and provenance documentation.
18. Commit the reproducible implementation and documentation.

## Canonical Data Hierarchy

Canonical Model Artifact -> authoritative model reference.
Truth Map -> canonical semantic structure.
Provenance Map -> evidence lineage.
Relationship/Vector Map -> derived computational representation.
Heatwave/Heightmap structures -> derived relationship features.
Fuzzy/ML layer -> learned heuristic signals.
MAF -> experimental computational representation.
Fractal MAF -> experimental recursive/compositional representation.
Tokens -> one possible interface to the system, not necessarily the internal computational primitive.

## Evidence Rule

Derived representations may recommend, rank, compress, predict, or traverse.
They may not silently redefine canonical truth.

## Failure Rule

False, rejected, contradictory, pruned, or terminated paths should remain available as negative evidence when retention provides future training, calibration, provenance, or debugging value.

Termination must be explicit rather than silently deleting a candidate.

## Componentization Rule

When a phase is experimentally validated, freeze its interface and convert the complete phase into a small native component.

Each component should have:
- a stable C++ interface
- deterministic inputs and outputs
- unit/regression tests
- benchmark coverage
- provenance metadata
- failure handling
- resource measurements
- device-specific optimization hooks

## Device Optimization

The primary mobile target is the Samsung Galaxy S26 Ultra.
Optimization should consider ARM64, NEON, Vulkan, memory bandwidth, cache locality, allocation behavior, and thermal/resource constraints.

Optimization must preserve numerical and behavioral correctness.

## Required Validation

Before promotion:

- baseline comparison
- holdout validation
- regression tests
- reproducibility check
- memory measurement
- token measurement where applicable
- latency measurement
- accuracy/correctness measurement
- provenance audit
- git diff --check
- native rebuild
- CTest

## Promotion Rule

Experimental -> validated -> componentized -> native C++ -> optimized -> integrated.

No phase may skip directly from experimental observation to production architecture.
