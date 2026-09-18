# MAF Phase 6E-B-S1 Bounded Expansion Recovery V1 — Verdict

**STATUS: COMPLETE / FROZEN SCIENTIFIC RESULT — PASS**

## 1. Phase identity

Phase:

`6E-B-S1`

Scientific question:

For the frozen 40-query population, can deterministic non-oracle bounded expansion recover every required generation-bound MAF object payload when the initial working set is deliberately constrained to selector candidate budget 1?

Qualified scientific verdict:

`PASS`

## 2. Frozen result authority

Frozen result:

`experiments/model_fractal/maf_phase_6e_b_s1_bounded_expansion_recovery_v1.json`

Result SHA256:

`194857dd4df6baabbee3138f1e6cb3d75988ddd092a4fd877892ab4528cf81a4`

Result Git blob:

`cf0b72947282dc00ad1603050db028c0c599246a`

Result freeze commit:

`408ea53e209752187d22e6fdfb879a38564930cc`

Result parent:

`d3d7815456672a67d5cbd5e289e9a5b2a9ee33a3`

Frozen expansion trace SHA256:

`5fab94f632b8e653b2debe3f5e98f9a19b9688bd9bacb4a578c75537c1b0ca53`

## 3. Prospective S1 authorities

Frozen S1 preregistration:

`experiments/model_fractal/MAF_PHASE_6E_B_S1_BOUNDED_EXPANSION_RECOVERY_PREREGISTRATION_V1.md`

SHA256:

`823853c71e378d2a559c95d80177990bea59e546965ce579cae9e589aa3991bf`

Freeze commit:

`1c15d26e0fe036c68dc9234cc5401eba84ee6770`

Frozen S1 runner implementation contract:

`experiments/model_fractal/MAF_PHASE_6E_B_S1_BOUNDED_EXPANSION_RECOVERY_RUNNER_IMPLEMENTATION_CONTRACT_V1.md`

SHA256:

`3bd876254e4ab549d099ef3b473e0b775c4d8dac43111a3f660937bcc83ca292`

Freeze commit:

`32ffb801937d86ff01ad836ba807357a09d1d705`

Frozen S1 runner:

`experiments/model_fractal/maf_phase_6e_b_s1_bounded_expansion_recovery_v1.py`

SHA256:

`16f70dea1582abf15780eeb177a71ce56121c64830567b7ff76f65125af97270`

Git blob:

`c4baa922ab7708cdfd370a9f04f17958495aec2e`

Freeze commit:

`d3d7815456672a67d5cbd5e289e9a5b2a9ee33a3`

## 4. Corrective-successor provenance

The original Phase 6E-B execution slot was spent by an infrastructure/integrity failure before scientific classification.

Frozen failure incident:

`experiments/model_fractal/MAF_PHASE_6E_B_EXECUTION_FAILURE_INCIDENT_AND_CORRECTIVE_SUCCESSOR_DESIGN_V1.md`

SHA256:

`1ecf171bee1e6470d5ac48c1482a2166eca05c895313eeb4acbc8e90b64a64ad`

Incident freeze commit:

`4691293d3dbecbb55880a8bfaf10e59b61fef1d6`

Original Phase 6E-B runner SHA256:

`c7e1efc2a5fddb85c49962f993be34709405979a5e9e60183a6975c7d18ee891`

Original Phase 6E-B result path:

`experiments/model_fractal/maf_phase_6e_b_bounded_expansion_recovery_v1.json`

Original result state:

`ABSENT PERMANENTLY`

The S1 run was a new prospective corrective successor, not a retry of the original runner.

The only permitted correction was reference-fixture-specific terminal-LF canonical validation.

The global no-LF canonicalization used for queries, catalog, trace, and result remained unchanged.

## 5. Authoritative S1 execution

The frozen S1 runner received exactly one authoritative execution.

Execution HEAD:

`d3d7815456672a67d5cbd5e289e9a5b2a9ee33a3`

Execution return code:

`0`

The external one-shot spent-slot sentinel was created before launch and preserved after execution.

No automatic retry occurred.

No second S1 execution is authorized under the frozen S1 runner identity.

## 6. Frozen population

Total queries:

`40`

Query classes:

- `specific_intent`: 24
- `multi_target_intent`: 8
- `fallback_control`: 8

Non-fallback evaluable population:

`32`

Fallback controls:

`8`

## 7. Fixed bounded-expansion schedule

The preregistered selector candidate budgets were:

- Round 0: `1`
- Round 1: `2`
- Round 2: `3`
- Round 3: `4`

All 40 queries executed all four selector rounds.

No early stopping was permitted.

Round configuration SHA256 values:

- Round 0: `2dd2925a3d9f63197deff6dc98f951c5177dc63dc08818b6492228dbac7d5576`
- Round 1: `57f751a3a019bccd58c5c32b4f5ecaf78283f49cc146896d61492ce31dfdd1c6`
- Round 2: `67dd6e5589cb16374e949b3ed633c3364f0ccb1d8c2b0a9ca1c6eaa2d2ceed56`
- Round 3: `0caeaeaafdd870e6b02ccc8b4450576883d4ef5234ba689c472e3b14d9dbe120`

Expansion policy:

`bounded_v1`

Maximum object budget:

`4`

Maximum expansion rounds after round zero:

`3`

## 8. Anti-oracle execution boundary

The S1 execution completed:

1. all 40 round-zero selector calls;
2. all 40 round-zero Query Capsules;
3. all 40 round-one selector calls;
4. all 40 round-two selector calls;
5. all 40 round-three selector calls;
6. complete 40-query trace construction;
7. canonical trace serialization;
8. trace SHA256 computation;

before the frozen reference fixture was deserialized.

No required-object target, reference payload identity, recovery classification, or phase verdict influenced selection or expansion.

The frozen reference fixture was used only after the complete trace SHA256 was fixed in process state.

## 9. Qualified scientific counts

Initial sufficient non-fallback queries:

`24`

Initial insufficient challenged queries:

`8`

Recovered challenged queries:

`8`

Not recovered challenged queries:

`0`

Fallback CONTROL queries:

`8`

Required arithmetic:

`24 + 8 = 32` non-fallback queries.

`8 + 0 = 8` challenged queries.

All arithmetic independently qualified:

`PASS`

## 10. Recovery result

All eight queries that were insufficient at the deliberately constrained round-zero candidate budget of 1 became fully covered within the preregistered bounded expansion schedule.

For every recovered challenged query, the required generation-bound MAF object evidence satisfied the frozen payload-identity rules.

No challenged query remained `NOT_RECOVERED` after round 3.

Therefore the preregistered Phase 6E-B-S1 PASS condition was satisfied.

## 11. Generation-bound payload evidence

The frozen generation contains:

`12` serialized MAF objects.

Total serialized object bytes:

`312326668`

Independent qualification verified:

- all 12 serialized object files remained present;
- all 12 serialized object SHA256 identities matched the frozen generation descriptor;
- generation descriptor payload SHA256 values matched the independent frozen reference payload SHA256 values;
- per-query published payload evidence was internally consistent with those frozen identities;
- no payload mismatch PK was reported for any recovered required object.

The authoritative S1 runner performed the generation-bound MAF object inspection required by the frozen scientific protocol.

The later independent qualifier did not call `inspect_object`; it verified the frozen serialized object identities and the published payload evidence without rerunning science.

## 12. Independent qualification

The frozen S1 result was independently qualified after execution.

The independent qualifier:

- did not import the S1 runner;
- did not execute the S1 runner;
- did not call the selector;
- did not construct Query Capsules;
- did not execute expansion;
- did not call `inspect_object`;
- did deserialize the frozen reference fixture after the run for qualification only;
- reconstructed all 40 query classifications;
- reconstructed all four rounds per query;
- reconstructed the complete S1 trace;
- recomputed the trace SHA256 exactly;
- recomputed the phase counts and verdict.

Reconstructed trace SHA256:

`5fab94f632b8e653b2debe3f5e98f9a19b9688bd9bacb4a578c75537c1b0ca53`

Independent scientific verdict:

`PASS`

## 13. What Phase 6E-B-S1 establishes

Within the frozen 40-query population and frozen generation, the experiment establishes:

> When the initial selector working set was constrained to at most one object, deterministic non-oracle bounded expansion through candidate budgets 2, 3, and 4 recovered all required generation-bound MAF object payloads for every query that was initially insufficient.

The experiment also establishes that the preregistered bounded-expansion policy produced a non-empty challenge set:

`8` initially insufficient non-fallback queries.

Therefore this was not a `NOT_TESTABLE` result.

## 14. What Phase 6E-B-S1 does not establish

This result does not establish or claim:

- model inference without the underlying model objects;
- token generation;
- answer correctness;
- logit parity;
- output parity;
- output fidelity;
- answer quality;
- model-object avoidance;
- tensor avoidance;
- reduced I/O;
- reduced memory use;
- lower latency;
- higher throughput;
- reduced energy use;
- MAF-native compute;
- generalization beyond the frozen 40-query population;
- generalization beyond the frozen 12-object catalog;
- generalization beyond the frozen generation and model.

Those questions require separate prospective experiments.

## 15. Relation to Phase 6E-A

Phase 6E-A established that with the frozen selector candidate budget of 4, all 32 evaluable non-fallback queries were initially sufficient.

Phase 6E-B-S1 adds a narrower complementary result:

- reducing the initial candidate budget from 4 to 1 created 8 genuine initial insufficiency challenges;
- the fixed deterministic 1→2→3→4 expansion schedule recovered all 8;
- 24 of 32 non-fallback queries remained initially sufficient even at candidate budget 1.

Together these results support the bounded claim that the frozen query-to-PK mechanism can form a small initial working set and deterministically expand it to complete required-object payload coverage for this frozen population.

They do not yet demonstrate MAF-native inference or performance advantage.

## 16. Final verdict

Phase 6E-B-S1:

`PASS`

Qualified counts:

- total queries: `40`
- evaluable non-fallback queries: `32`
- initially sufficient: `24`
- challenged: `8`
- recovered: `8`
- not recovered: `0`
- fallback controls: `8`

Frozen result SHA256:

`194857dd4df6baabbee3138f1e6cb3d75988ddd092a4fd877892ab4528cf81a4`

Frozen trace SHA256:

`5fab94f632b8e653b2debe3f5e98f9a19b9688bd9bacb4a578c75537c1b0ca53`

Interpretation:

**The preregistered bounded expansion mechanism recovered every initially missing required generation-bound MAF object payload in the frozen Phase 6E-B-S1 challenge population.**

## 17. Current authorization boundary

At verdict-candidate creation time:

- original Phase 6E-B execution: spent;
- original Phase 6E-B result: absent permanently;
- Phase 6E-B-S1 preregistration: frozen;
- Phase 6E-B-S1 runner contract: frozen;
- Phase 6E-B-S1 runner: frozen;
- Phase 6E-B-S1 authoritative execution: spent and complete;
- Phase 6E-B-S1 result: frozen;
- Phase 6E-B-S1 scientific verdict: qualified `PASS`;
- Phase 6E-B-S1 verdict document: candidate only;
- additional S1 execution: not authorized;
- result rewrite: not authorized.

## 18. Next gate

After this verdict candidate passes independent static qualification, the next authorized mutation is:

`FREEZE PHASE 6E-B-S1 NARROW VERDICT`

No scientific rerun is required or authorized.
