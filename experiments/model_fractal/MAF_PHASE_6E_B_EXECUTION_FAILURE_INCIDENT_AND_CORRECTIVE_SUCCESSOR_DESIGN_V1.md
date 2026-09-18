# MAF Phase 6E-B Execution Failure Incident and Corrective Successor Design V1

**STATUS: PROSPECTIVE CORRECTIVE DESIGN — ORIGINAL PHASE 6E-B EXECUTION SLOT SPENT**

## 1. Purpose

This document freezes the observed Phase 6E-B infrastructure failure and defines the only permitted corrective successor direction.

It does not reinterpret the failed execution as scientific evidence. It does not authorize a rerun of the frozen Phase 6E-B runner. It does not authorize reuse of the original Phase 6E-B result slot.

## 2. Frozen incident checkpoint

Repository branch:

`labs/multidimensional-maf`

Frozen runner commit:

`79a225e9124705704e87070ace79958a29fdd4dc`

Frozen runner:

`experiments/model_fractal/maf_phase_6e_b_bounded_expansion_recovery_v1.py`

Runner SHA256:

`c7e1efc2a5fddb85c49962f993be34709405979a5e9e60183a6975c7d18ee891`

Runner Git blob:

`bec368adebaab497b9321a860135c1411f7194f1`

Frozen reference fixture:

`experiments/model_fractal/maf_phase_6e_a_reference_state_fixture_v1.json`

Reference fixture SHA256:

`870b656e0c3181ec8f7be1537bdeafde10fffd1b947f5372d21cdee4c00a83a0`

Original Phase 6E-B result path:

`experiments/model_fractal/maf_phase_6e_b_bounded_expansion_recovery_v1.json`

Observed result state:

`ABSENT`

Original untracked baseline after the failed execution remained exactly 440 paths with canonical NUL-delimited SHA256:

`f206c0eed32daef9ed0cfaae195aa56a343a85437ebd3135aeafdb4c1ffacddd`

## 3. Observed authoritative execution

The frozen Phase 6E-B runner was launched exactly once.

Observed runner return code:

`2`

Observed infrastructure error:

`PHASE 6E-B INFRASTRUCTURE/INTEGRITY FAILURE: reference fixture is not canonical JSON`

No retry occurred.

No Phase 6E-B result artifact was created.

No Phase 6E-B scientific verdict was produced.

The correct scientific status of the original execution is:

`UNAVAILABLE`

It is not `PASS`.

It is not `FAIL`.

It is not `NOT_TESTABLE`.

## 4. Exact execution position

The observed control flow proves that execution reached the reference fixture canonical-byte check only after the complete expansion trace had already been constructed.

Therefore the following work completed before the infrastructure failure:

- all 40 round-zero selector calls;
- all 40 round-zero Query Capsules;
- all 40 round-one selector calls;
- all 40 round-two selector calls;
- all 40 round-three selector calls;
- 160 total selector calls;
- all four fixed candidate budgets `1, 2, 3, 4`;
- complete 40-query expansion trace construction;
- complete trace canonical-byte construction;
- complete trace SHA256 computation;
- frozen reference fixture SHA256 verification;
- reference fixture JSON deserialization.

The complete trace SHA256 was computed only in process memory and was not persisted.

The following scientific operations were not reached:

- required-object classification;
- `INITIAL_SUFFICIENT` classification;
- `INITIAL_INSUFFICIENT` classification;
- earliest recovery determination;
- generation-bound MAF payload inspection;
- payload-match classification;
- `RECOVERED` classification;
- `NOT_RECOVERED` classification;
- Phase 6E-B scientific verdict construction;
- result publication.

## 5. Root cause

The frozen reference fixture is valid and unchanged.

Reference raw bytes:

`14283`

Reference raw SHA256:

`870b656e0c3181ec8f7be1537bdeafde10fffd1b947f5372d21cdee4c00a83a0`

Reference JSON deserialization:

`PASS`

The reference fixture exact file convention is compact sorted UTF-8 JSON followed by one terminal LF byte.

The compact JSON without the terminal LF is 14282 bytes with SHA256:

`1d5fde04effa7c494507918f023bc575e7705f4c2d87e7cda516fcbcb3754aff`

The exact frozen reference bytes equal:

`compact_json_bytes + b"\n"`

The frozen Phase 6E-A runner canonicalizer returned compact canonical JSON plus terminal LF.

The frozen Phase 6E-B runner canonicalizer returned compact canonical JSON without terminal LF.

The Phase 6E-B reference loader incorrectly required:

`canonical_bytes(fixture) == raw`

That predicate was incompatible with the exact frozen reference fixture byte convention.

The root cause is therefore:

`PHASE 6E-B RUNNER REFERENCE-FIXTURE SERIALIZATION-CONVENTION MISMATCH`

This is an implementation integrity failure. It is not evidence against or in favor of the scientific hypothesis.

## 6. Important constraint discovered by the incident

The corrective successor MUST NOT globally change the existing Phase 6E-B `canonical_bytes` convention.

The frozen query fixture and catalog passed their canonical-byte checks during the spent execution using compact canonical JSON without terminal LF.

The trace SHA256 computation and prospective result serialization also use that same no-LF `canonical_bytes` function.

Changing the global canonicalizer to append LF would therefore change more than the failing reference validation and could break already qualified non-oracle input checks or alter trace and result serialization semantics.

The corrective change must be reference-fixture specific.

## 7. Minimal corrective design

A corrective successor may introduce exactly one reference-file canonicalization rule equivalent to:

`canonical_reference_fixture_bytes(value) = canonical_bytes(value) + b"\n"`

The successor reference loader may then require:

`canonical_reference_fixture_bytes(fixture) == raw`

Equivalent logic that performs the same exact byte comparison is permitted.

The global `canonical_bytes` function must remain compact sorted UTF-8 JSON with no terminal LF.

No selector implementation, query fixture, catalog, round budget, round configuration, Query Capsule semantics, expansion policy, generation binding, payload rule, classification rule, verdict rule, or scientific boundary may be changed as part of this correction.

## 8. Anti-adaptation rule

The corrective successor may use only the observed infrastructure fact that the frozen reference file has one terminal LF after compact canonical JSON.

It MUST NOT use any reference required-object PK, reference payload SHA256, reference query target, scientific classification, recovery outcome, or payload evidence to alter:

- query text;
- selector behavior;
- selector ranking;
- candidate budget;
- round count;
- capsule construction;
- route order;
- expansion policy;
- trace construction;
- classification thresholds;
- payload verification;
- phase verdict logic.

The corrective successor remains non-oracle with respect to the scientific target.

## 9. Original execution remains spent

The frozen runner at SHA256:

`c7e1efc2a5fddb85c49962f993be34709405979a5e9e60183a6975c7d18ee891`

MUST NOT be executed again.

The original Phase 6E-B result path:

`experiments/model_fractal/maf_phase_6e_b_bounded_expansion_recovery_v1.json`

MUST remain absent permanently.

No future artifact may be published at that path.

The unpersisted trace from the spent execution MUST NOT be reconstructed from hidden state or treated as a scientific result.

## 10. Corrective successor identity separation

Any corrective scientific attempt must be a new prospective successor with new immutable identities.

Recommended successor label:

`Phase 6E-B-S1`

Recommended successor preregistration:

`experiments/model_fractal/MAF_PHASE_6E_B_S1_BOUNDED_EXPANSION_RECOVERY_PREREGISTRATION_V1.md`

Recommended successor runner contract:

`experiments/model_fractal/MAF_PHASE_6E_B_S1_BOUNDED_EXPANSION_RECOVERY_RUNNER_IMPLEMENTATION_CONTRACT_V1.md`

Recommended successor runner:

`experiments/model_fractal/maf_phase_6e_b_s1_bounded_expansion_recovery_v1.py`

Recommended successor result:

`experiments/model_fractal/maf_phase_6e_b_s1_bounded_expansion_recovery_v1.json`

The successor must receive a fresh preregistration freeze before successor runner source is created.

## 11. Successor scientific invariants

Unless explicitly narrowed by the successor preregistration to address this incident, Phase 6E-B-S1 must preserve the original Phase 6E-B scientific design:

- same frozen 40-query population;
- same frozen 12-object catalog;
- same accepted selector implementation;
- same generation and manifest binding;
- same candidate budgets `1, 2, 3, 4`;
- same round config SHA256 values;
- same `bounded_v1` expansion policy;
- same maximum object budget `4`;
- same maximum expansion rounds `3`;
- same empty relationship selection;
- same Query Route Cache prohibition;
- same all-rounds-before-reference schedule;
- same complete trace-before-reference anti-leakage boundary;
- same reference fixture identity;
- same generation-bound serialized-object verification;
- same actual MAF object payload inspection;
- same initial sufficiency classifications;
- same recovery definitions;
- same `PASS`, `FAIL`, and `NOT_TESTABLE` phase rules;
- same object-state payload-identity scientific boundary.

## 12. Successor execution discipline

Before Phase 6E-B-S1 science may run:

1. freeze a successor preregistration;
2. freeze a successor runner implementation contract;
3. create and statically qualify a successor runner;
4. freeze the successor runner;
5. perform a separate read-only authoritative execution preflight;
6. verify the successor result path is absent;
7. authorize one successor execution only after all gates pass.

A successor execution must not be described as a retry of the original runner.

It is a new prospective corrective experiment after a documented infrastructure failure.

## 13. Scientific interpretation

The original Phase 6E-B execution establishes no recovery rate.

It establishes no initial-insufficiency denominator.

It establishes no recovered count.

It establishes no not-recovered count.

It establishes no Phase 6E-B PASS, FAIL, or NOT_TESTABLE verdict.

The only admissible conclusion is:

> The first frozen Phase 6E-B execution terminated after complete non-oracle expansion-trace construction and reference JSON deserialization because the runner applied the wrong terminal-LF convention when validating the frozen reference fixture bytes. No payload inspection, recovery classification, or scientific verdict was reached.

## 14. Authorization boundary

This incident document authorizes documentation and prospective successor design only.

It does not authorize:

- rerunning the frozen Phase 6E-B runner;
- creating the original Phase 6E-B result;
- reusing the spent execution slot;
- treating the unpersisted trace as scientific evidence;
- modifying frozen historical artifacts;
- changing the scientific hypothesis after observing target outcomes;
- executing Phase 6E-B-S1 before its own preregistration, runner contract, runner freeze, and execution preflight.

## 15. Next gate

After this incident record is frozen, the next authorized gate is:

`CREATE + QUALIFY PHASE 6E-B-S1 PROSPECTIVE PREREGISTRATION`

No successor runner source is authorized before that preregistration is frozen.
