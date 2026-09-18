# MAF Query Route Cache Validation Runner Implementation Contract V1

Status: CANDIDATE — NOT FROZEN  
Phase: 6D-Q4 — Query Route Cache  
Scientific execution: NOT ENTERED  
Phase 6E: NOT ENTERED

## 1. Purpose

This contract preregisters the implementation and execution boundary for the Phase 6D-Q4 validation runner before runner source exists.

The runner exists only to execute the already-frozen Phase 6D-Q4 validation protocol against the already-frozen Q4 production module. It MUST NOT redefine the Q4 scientific question, change the 44 frozen checks, extend the claim boundary, or enter Phase 6E.

## 2. Frozen authorities

The runner MUST bind to these exact authorities:

- Q4 validation protocol:
  - path: `experiments/model_fractal/MAF_QUERY_ROUTE_CACHE_VALIDATION_V1_PROTOCOL.md`
  - SHA256: `af587bfe685deb86ac4574b3d41d1a80b5df2cec84bce757eac8c7e307d82ad9`
- Q4 production implementation contract:
  - path: `experiments/model_fractal/MAF_QUERY_ROUTE_CACHE_IMPLEMENTATION_CONTRACT_V1.md`
  - SHA256: `9f253138399383d703fabd6dc6945af2e94c4af29d5b0f2995c0775984e1cf11`
- Q4 production module:
  - path: `experiments/model_fractal/maf_query_route_cache_v1.py`
  - SHA256: `b44eeca010514a0950240fac59469870ccd79150faceebecca105feb3fa02a80`
- Q4 V1.2 persistence portability recovery authority:
  - path: `experiments/model_fractal/MAF_QUERY_ROUTE_CACHE_PERSISTENCE_PORTABILITY_RECOVERY_V1.md`
  - SHA256: `b08d45caefd68316b7ced523c401052addec81d7932539a576a4266fe7a5a106`
  - scope: fresh Q4 V1.2 recovery only.
  - supersession: only the Q4 production-module SHA binding above is updated to the corrected frozen production module.
  - the Q4 validation protocol and Q4 production implementation contract remain unchanged.
  - all Q4-V01 through Q4-V44 checks, frozen cases `q001`, `q025`, `q026`, and `q033`, scientific meanings, claim boundaries, and exact-once semantics remain unchanged.
  - Q4 V1 and Q4 V1.1 remain permanently spent and MUST NOT be rerun.
  - the recovery runner, when later materialized, MUST use the fresh V1.2 namespace frozen by this recovery authority; this contract supersession does not create or execute that runner.
  - Q4 V1.2 science is NOT ENTERED by this contract supersession.
  - Phase 6E remains NOT ENTERED.
- Q4 V1.3 runner-only harness recovery authority:
  - path: `experiments/model_fractal/MAF_QUERY_ROUTE_CACHE_VALIDATION_V1_3_RECOVERY_PREREGISTRATION.md`
  - SHA256: `3537f1a45bb2452c1aa08ecbd27cdb009f39d809c4d0872f6290622c1c955be8`
  - scope: fresh Q4 V1.3 runner-only harness recovery only.
  - frozen V1.2 failure evidence remains bound by runner SHA `6287c836bee9b1b69c224e8d5a3b812966287a9d8c17f86d7f6e805854036ac3`, result SHA `b85ad6e128b35512faa4aed25113b887392b29ce8ab4f9d88d6a2b2009cfa1fb`, and slot SHA `eb84a7c280c0c39671ca2f7cb2271ff928663eafa82293f4642413f841ace0af`.
  - Q4 V1, Q4 V1.1, and Q4 V1.2 are permanently spent and MUST NOT be rerun.
  - the Q4 validation protocol, Q4 production implementation contract, corrected Q4 production module, canonical 44-check matrix, frozen cases `q001`, `q025`, `q026`, and `q033`, scientific meanings, claim boundaries, and exact-once semantics remain unchanged.
  - the future V1.3 runner MUST be derived mechanically from the frozen V1.2 runner.
  - authorized runner delta is limited to the fresh V1.3 current-run namespace strings, the runner-contract SHA rebinding required by this supersession, and the single proven line-683 harness repair.
  - the sole harness repair is `_expect_q4_rejection(MAFQueryRouteCacheIdentityError, lambda: validate_route_cache_for_reuse_v1(... expected_source_generation_pk=mismatch_generation ...))`, preserving the existing action lambda unchanged.
  - the `_expect_q4_rejection(expected_error, action)` helper signature MUST remain unchanged, and no other `_expect_q4_rejection` call may be changed.
  - no production-module, protocol, implementation-contract, Q2, Q3, check-set, frozen-case, result-schema, reservation, publication, or scientific acceptance behavior may be changed by this recovery.
  - fresh V1.3 runner namespace: `experiments/model_fractal/maf_query_route_cache_validation_v1_3.py`
  - fresh V1.3 result namespace: `experiments/model_fractal/maf_query_route_cache_validation_v1_3.json`
  - fresh V1.3 slot namespace: `experiments/model_fractal/maf_query_route_cache_validation_v1_3.slot`
  - fresh V1.3 transient partial namespace: `experiments/model_fractal/maf_query_route_cache_validation_v1_3.json.partial`
  - before any V1.3 exact-once execution, the result, slot, and transient partial paths MUST all be absent and the V1.3 runner MUST already be frozen.
  - once V1.3 reaches durable `RESERVED_DURABLE`, V1.3 is permanently spent and MUST NOT be rerun regardless of scientific or harness outcome.
  - no retry branch is authorized.
  - this contract supersession does not create, import, or execute the V1.3 runner and does not create any V1.3 result, slot, or partial artifact.
  - Q4 V1.3 science is NOT ENTERED by this contract supersession.
  - Phase 6E remains NOT ENTERED.
- canonical Q4 44-check matrix:
  - SHA256: `8dc81ec92bace5678a983332cdb6aa342ba7341273a18ee51346f96e1a6414da`
- Q2 selector:
  - path: `experiments/model_fractal/maf_query_to_pk_selection_v1.py`
  - SHA256: `e21c05e352fe921b791e8c936425727a98911ce7566989672a96bfd2b9613fa2`
- Q2 V1.4 validation runner, evidence/design authority only:
  - path: `experiments/model_fractal/maf_query_to_pk_selection_validation_v1_4.py`
  - SHA256: `7bda960c125786fdf3cfca65c4b7b5851ca8bd91257282facfee2fec1ae7a030`
  - the earlier value containing `...3cfba65...` is rejected as a transcription error and MUST NOT be used.
- frozen query fixture:
  - path: `experiments/model_fractal/maf_query_to_pk_selection_validation_v1_queries.json`
  - SHA256: `32f4636bd5e8ceee0dca8342335279a6f8e6acafe866a5469f2c23aa2655202a`
- frozen catalog:
  - path: `experiments/model_fractal/maf_query_to_pk_selection_validation_v1_catalog.json`
  - SHA256: `c51ef0fabeb10e7c8a091a093aa1934620a69b2026b5a87cb02477b9dd7ca900`
- Q3 V1.1 validation runner, durability/design authority only:
  - path: `experiments/model_fractal/maf_query_capsule_attach_detach_cleanup_validation_v1_1.py`
  - SHA256: `26b4bef94fa5f063f7340190879d37b124bba305da60ac0abc12e83433159f99`
- resident PK directory:
  - path: `experiments/model_fractal/maf_resident_pk_directory_v1.py`
  - SHA256: `4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6`

Any mismatch is a pre-execution failure. A mismatch MUST prevent result-slot reservation and MUST prevent Q4 scientific execution.

## 3. Frozen cases

The validation runner MUST execute exactly these four frozen query cases:

1. `q001`
2. `q025`
3. `q026`
4. `q033`

The query content MUST come from the frozen query fixture. The runner MUST NOT substitute, regenerate, reinterpret, or silently normalize a different query set.

The four cases are evidence samples for Q4 route-cache behavior only. They are not a downstream task-quality benchmark.

## 4. Frozen check set

The runner MUST implement exactly these 44 protocol checks, in this order:

`Q4-V01`, `Q4-V02`, `Q4-V03`, `Q4-V04`, `Q4-V05`, `Q4-V06`, `Q4-V07`, `Q4-V08`, `Q4-V09`, `Q4-V10`, `Q4-V11`, `Q4-V12`, `Q4-V13`, `Q4-V14`, `Q4-V15`, `Q4-V16`, `Q4-V17`, `Q4-V18`, `Q4-V19`, `Q4-V20`, `Q4-V21`, `Q4-V22`, `Q4-V23`, `Q4-V24`, `Q4-V25`, `Q4-V26`, `Q4-V27`, `Q4-V28`, `Q4-V29`, `Q4-V30`, `Q4-V31`, `Q4-V32`, `Q4-V33`, `Q4-V34`, `Q4-V35`, `Q4-V36`, `Q4-V37`, `Q4-V38`, `Q4-V39`, `Q4-V40`, `Q4-V41`, `Q4-V42`, `Q4-V43`, `Q4-V44`.

The meaning of each check is exclusively defined by the frozen Q4 protocol and the canonical check-matrix SHA above. This contract does not rename, weaken, merge, split, or reinterpret any check.

A scientific PASS requires all 44 checks to pass. Partial PASS is forbidden.

## 5. Runner namespace

Proposed runner namespace:

- runner source:
  `experiments/model_fractal/maf_query_route_cache_validation_v1.py`
- result:
  `experiments/model_fractal/maf_query_route_cache_validation_v1.json`
- exact-once slot:
  `experiments/model_fractal/maf_query_route_cache_validation_v1.slot`
- transient publication partial:
  `experiments/model_fractal/maf_query_route_cache_validation_v1.json.partial`

The runner source MUST be frozen before any scientific execution.

The result and slot paths MUST NOT exist before the exact-once scientific run. Any pre-existing result, slot, or conflicting partial is fail-closed unless the frozen Q4 protocol explicitly defines a stricter state rule.

The runner MUST NOT overwrite an existing result or slot.

## 6. Imports and dependency boundary

The validation runner MAY import the frozen production surfaces needed to exercise Q4:

- `maf_query_route_cache_v1`
- `maf_query_to_pk_selection_v1`
- Q1 capsule data-model production code as required
- `maf_resident_pk_directory_v1`
- Python standard library

The validation runner MUST NOT import prior validation runners as executable dependencies, including:

- `maf_query_to_pk_selection_validation_v1_4`
- `maf_query_capsule_attach_detach_cleanup_validation_v1_1`
- Q1 validation runners
- runtime validation runners

Those prior runners are evidence/design authorities only.

The Q4 validation runner MUST NOT import the Phase 6C runtime production module as a route-cache dependency and MUST NOT require inference or generation execution.

## 7. Selection authority

Q2 remains the semantic authority for query-to-PK selection.

For each frozen query, the runner MUST obtain the route-selection inputs through the frozen Q2 production selector and frozen catalog/config/source-binding authorities. Q4 MUST NOT redefine selection scoring, parsing, ranking, tie-breaking, query normalization, or semantic interpretation.

The Q4 runner may package the resulting Q2 selection into a Q1 capsule only as required to exercise the frozen Q4 production API.

A cache hit MUST NOT trigger a new semantic-selection rule and MUST NOT be interpreted as proof that the selected working set is sufficient for inference.

## 8. Resident object-PK validation authority

Object-PK reuse validation MUST use a caller-supplied `ResidentPKSnapshot` compatible with the frozen resident directory API.

The runner MUST construct any validation snapshot deterministically from frozen Q2/Q1 evidence and source-generation binding. It MUST NOT hard-code a guessed resident `pk_kind`.

The production module remains responsible for discovering the matching entry's `pk_kind` and then using the public snapshot lookup API.

Unknown, ambiguous, mismatched-generation, or otherwise unresolved object PKs MUST fail closed through the production Q4 error surface.

## 9. Relationship authority

No Q2 or resident production authority defines relationship lookup for Q4.

Therefore the validation runner MUST supply an explicit ephemeral relationship-authority set to the Q4 production reuse validator.

Requirements:

- materialize it only for the validation operation;
- use an immutable/frozen set representation at the call boundary;
- do not persist it into the cache record;
- do not reinterpret it as a general production relationship registry;
- construct valid-case membership deterministically from frozen capsule/route evidence;
- construct unknown-relationship negative cases by deterministic mutation or exclusion;
- demonstrate fail-closed rejection for relationship PKs outside the supplied authority.

The relationship-authority mechanism is validation scaffolding for the production API contract, not evidence of a new relationship semantic layer.

## 10. Cache record construction and metadata-only rule

The runner MUST exercise the frozen `MAFQueryRouteCacheRecordV1` and its public Q4 APIs.

Persisted Q4 cache records are metadata-only. A record MUST NOT contain or retain:

- tensor bytes;
- dense vectors;
- mapped buffers;
- serialized MAF payload bytes;
- open file descriptors;
- mmap objects;
- runtime object references;
- pins;
- leases;
- capsule references;
- engine handles.

The record fields, cache identity, canonical serialization, and route-payload digest MUST remain exactly as frozen by the Q4 protocol and production implementation contract.

## 11. Reuse and invalidation

Exact-context reuse is permitted only when all frozen identity fields match:

- `query_signature`
- `source_generation_pk`
- `source_manifest_sha256`
- `selection_config_sha256`
- `expansion_policy`
- `max_object_budget`
- `max_expansion_rounds`

The runner MUST demonstrate fail-closed invalidation/rejection for the mismatch and corruption cases required by Q4-V28 through Q4-V37, including changed identity, malformed schema, cache identity corruption, payload/order corruption, unknown object PK, and unknown relationship PK as specified by the protocol.

The runner MUST NOT treat a cache miss or invalidated record as an error in the scientific claim. The claim is whether unsafe reuse is prevented.

No deletion or eviction policy is introduced in Q4 V1.

## 12. Cleanup and runtime separation

The runner MUST validate that allowed route metadata can survive Q3-style capsule cleanup while prohibited runtime state does not.

The test sequence MUST preserve the frozen Q3 ownership boundary:

1. create/obtain the Q2 selection and Q1 capsule required by the case;
2. construct and persist the Q4 metadata-only route-cache record in an isolated validation filesystem location;
3. perform the Q3-equivalent capsule detach/cleanup state transition using production-compatible objects or faithful local validation scaffolding without importing the Q3 validation runner;
4. demonstrate that no prohibited dense/materialized/runtime state is retained by the cache record;
5. demonstrate that the persisted route metadata remains readable after capsule cleanup;
6. validate reuse only through the frozen Q4 production API and caller-supplied resident/relationship authorities.

The validation MUST NOT delete, mutate, or replace the canonical MAF generation.

The runner MUST NOT unlink a canonical generation path while an engine owns it.

## 13. Validation cache filesystem scope

Q4 science may exercise the production persistence API only inside a runner-owned isolated temporary validation directory.

Requirements:

- never write cache-test records into the canonical model/generation namespace;
- never modify tracked repository fixtures;
- never modify Q2/Q3 frozen evidence;
- use unique runner-owned temporary paths;
- validate canonical write/read, idempotent identical write behavior, no-overwrite behavior, and corruption handling as required by the protocol;
- after all required evidence has been captured, runner-owned temporary cache files may be cleaned up;
- cleanup of test files MUST NOT be confused with a Q4 cache eviction policy.

The persistent-behavior claim concerns survival across capsule cleanup and safe later reuse validation, not indefinite retention of the runner's temporary files.

## 14. Failure handling

Known failures MUST have typed, explicit handling.

Unexpected failures MUST:

1. be logged with traceback;
2. be converted into a controlled validation failure;
3. fail closed;
4. never be silently swallowed.

Bare `except` handlers are forbidden.

Silent `pass` inside exception handlers is forbidden.

Known benign cleanup `FileNotFoundError` may use an explicit logged cleanup escape when absence means cleanup is already complete.

The validation runner MUST NOT terminate the user's Termux shell. It MUST NOT call `exit`, `quit`, `os._exit`, or equivalent shell/session termination mechanisms. Normal Python process return codes are permitted.

## 15. Canonical result schema

The final scientific result MUST be canonical JSON with:

- sorted object keys;
- compact separators;
- UTF-8;
- `ensure_ascii=False`;
- `allow_nan=False`;
- exactly one trailing newline in the persisted result file.

The top-level result MUST contain at least:

- `schema`
- `status`
- `protocol_sha256`
- `runner_contract_sha256`
- `runner_sha256`
- `production_module_sha256`
- `check_matrix_sha256`
- `q2_selector_sha256`
- `q2_runner_evidence_sha256`
- `q3_runner_evidence_sha256`
- `query_fixture_sha256`
- `catalog_sha256`
- `frozen_cases`
- `checks`
- `case_results`
- `claim_boundary`
- `failure`

Result schema identifier:

`openmind.maf_query_route_cache_validation.v1`

`checks` MUST contain exactly one boolean outcome for every `Q4-V01` through `Q4-V44`.

`frozen_cases` MUST contain exactly `q001`, `q025`, `q026`, `q033` in that order.

`failure` MUST be `null` on scientific PASS. On controlled failure it MUST record enough typed information to identify the failed stage without including runtime objects or non-serializable state.

## 16. Exact-once reservation and publication

Q4 V1 scientific execution is exact-once.

Before any scientific check that may write cache-test data or produce scientific evidence, the runner MUST:

1. verify all frozen authority hashes;
2. verify the exact 44-check matrix;
3. verify all four frozen fixture cases;
4. verify that the result namespace is unused;
5. prepare the exact-once reservation;
6. durably reserve the Q4 V1 slot using a no-overwrite mechanism;
7. fsync the slot and containing directory before scientific execution proceeds.

Once durable reservation succeeds, the Q4 V1 slot is spent even if the scientific execution later fails. The runner MUST NOT silently retry a spent V1 slot.

The result MUST be published with no-overwrite atomic semantics and directory durability modeled on the frozen Q3 V1.1 evidence pattern. Existing different content MUST fail closed.

The runner MUST distinguish at least:

- pre-reservation failure: Q4 science not entered;
- durable slot reserved: Q4 science entered and V1 spent;
- result published durably: Q4 V1 execution complete.

No ordinary validation failure may erase the durable slot.

## 17. Runner self-check before science

Before the runner is frozen, static review MUST prove that the source:

- binds every frozen authority hash;
- binds check-matrix SHA `8dc81ec92bace5678a983332cdb6aa342ba7341273a18ee51346f96e1a6414da`;
- contains exactly the 44 Q4 check IDs with no missing or extra IDs;
- contains exactly the four frozen case IDs;
- contains the canonical result schema identifier;
- has explicit exact-once result/slot handling;
- uses no-overwrite durable publication;
- has no bare exception handlers;
- has no silent `pass` exception handlers;
- logs every broad `Exception` handler before fail-closed conversion;
- imports no prior validation runner as an executable dependency;
- does not import or execute inference/generation/runtime as a route-cache dependency;
- contains no Phase 6E sufficiency test;
- does not write the result namespace during static review.

The runner MUST be frozen as an exact-path commit before any exact-once scientific execution.

## 18. Scientific acceptance

Q4 scientific PASS requires:

- the exact frozen runner executes once under the durable slot;
- all four frozen cases are exercised as required by the protocol;
- all 44 Q4 checks are present;
- all 44 Q4 checks pass;
- no unexpected failure escapes uncontrolled;
- the canonical result is durably published;
- the result hashes bind the exact frozen authorities and runner;
- the claim boundary remains Q4-only.

Any failed Q4 check means the scientific verdict is not PASS.

A harness or implementation defect discovered before durable slot reservation may be corrected through a new reviewed/frozen runner revision without spending Q4 V1.

A defect discovered after durable slot reservation does not permit rerunning the same Q4 V1 namespace.

## 19. Claim boundary

A Q4 PASS may support only the claim that, for the preregistered frozen validation cases and checks, generation/source/config-bound derived route metadata can be persisted and safely reused or invalidated across capsule cleanup without requiring prohibited runtime-state persistence.

A Q4 PASS MUST NOT be described as evidence that:

- the selected working set is sufficient for a downstream model task;
- inference output is correct;
- generation quality is preserved;
- cache reuse improves performance;
- cache hits are beneficial;
- semantic selection is optimal;
- Q4 matches an existing LLM pipeline;
- MAF is a replacement inference engine;
- MAF-native compute has been demonstrated.

Those questions are outside Q4. Selective working-set sufficiency remains Phase 6E-A and is NOT entered by this contract or runner.

## 20. Freeze sequence

Required sequence:

1. create this runner implementation-contract candidate;
2. independently static-audit it against the frozen Q4 protocol, production contract, production module, check-matrix SHA, Q2/Q3 authorities, and frozen fixtures;
3. correct the untracked candidate if necessary;
4. freeze the accepted runner implementation contract as an exact one-path commit;
5. create runner source as an untracked candidate;
6. syntax/static-review the runner without reserving the slot or writing the result namespace;
7. freeze the accepted runner source as an exact one-path commit;
8. perform final readiness audit;
9. only then execute the exact-once Q4 V1 scientific run.

Until step 9 begins after durable slot reservation, Q4 scientific status remains NOT ENTERED.
