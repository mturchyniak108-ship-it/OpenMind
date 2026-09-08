# MAF Query Capsule Data Model Validation V1.1 Protocol

## 1. Status

**PREREGISTERED SCIENTIFIC VALIDATION — PHASE 6D-Q1**

Validation namespace: **V1.1**

This is the prospective successor to rejected Validation V1.

Validation V1 MUST NOT be rerun.

## 2. Reason for successor namespace

Validation V1 reserved its exact-once slot and executed V01-V36.

Its frozen partial evidence recorded:

- 36/36 checks passed;
- failed checks: none;
- auditor error: none;
- all_pass: true.

V1 nevertheless failed its preregistered final publication step because the
Android/Termux Python runtime did not expose Python `os.link`.

V1 was formally rejected as:

**V01-V36 MATRIX PASS / HARNESS PUBLICATION CONTRACT FAIL**

V1.1 corrects the publication harness prospectively.

V1.1 does not promote, rename, reconstruct, or reuse the V1 partial as its
authoritative result.

## 3. Frozen predecessor authorities

Data-model protocol SHA256:

`5255a58c8c6340c251e24ae8543760fcd66a8deb8be1a8356ad5b78ad898edda`

Frozen Data Model V1 implementation SHA256:

`f897b97011714f3c84b7350c6bb53e800232be8a5d34e5148a3e50a81952976e`

Validation V1 protocol SHA256:

`6e77946c0e25a72052f4b4e6f9762b46fe1e141d9e5b03eecde1184d53ff78f9`

Validation V1 runner SHA256:

`c8f3f27a8a4069083896b8e1c365d5edded4195bfa468bd62ee4e9c8e023f253`

Frozen V1 spent-partial evidence SHA256:

`c6959fcbfde559243cee7686d1b4f970c4130139e01f1318a5eaa7b08e2e9451`

Formal V1 rejection verdict SHA256:

`d78a2695d943d481badb5359d666133190a130d05e5acb8d69d9082be7cbf410`

The V1 final result pathname MUST remain absent.

## 4. V1.1 target namespace

Protocol:

`experiments/model_fractal/MAF_QUERY_CAPSULE_DATA_MODEL_VALIDATION_V1_1_PROTOCOL.md`

Runner:

`experiments/model_fractal/maf_query_capsule_data_model_validation_v1_1.py`

Authoritative result:

`experiments/model_fractal/maf_query_capsule_data_model_validation_v1_1.json`

Reservation artifact:

`experiments/model_fractal/maf_query_capsule_data_model_validation_v1_1.json.partial`

Verdict:

`experiments/model_fractal/MAF_QUERY_CAPSULE_DATA_MODEL_VALIDATION_V1_1_VERDICT.md`

Result schema:

`openmind.maf_query_capsule_data_model_validation.v1_1`

Expected scientific check count:

`36`

## 5. Scientific question

V1.1 independently asks:

> Does the exact frozen Query Capsule Data Model V1 implementation satisfy
> the preregistered deterministic, immutable, generation-bound Query Capsule
> and Query Route Cache representation contract?

V1 evidence does not substitute for V1.1 execution.

## 6. Scientific matrix

The scientific matrix remains exactly V01-V36, in the same order and with
the same substantive meanings frozen by Validation V1:

V01 schema_constants

V02 field_inventory

V03 generation_pk_grammar

V04 object_pk_grammar

V05 query_pk_grammar

V06 query_pk_exact_derivation

V07 query_pk_generation_binding

V08 query_pk_manifest_binding

V09 query_pk_configuration_binding

V10 capsule_canonical_json

V11 capsule_round_trip

V12 ordered_sequence_preservation

V13 duplicate_initial_object_rejection

V14 duplicate_relationship_rejection

V15 route_order_permutation

V16 object_budget

V17 disabled_expansion_policy

V18 bounded_expansion_policy

V19 capsule_generation_mismatch

V20 capsule_manifest_mismatch

V21 sha256_validation

V22 capsule_unknown_field_rejection

V23 route_exact_cache_key

V24 duplicate_route_pk_rejection

V25 initial_additional_disjointness

V26 touched_subset

V27 selected_unused_derivation

V28 route_generation_mismatch

V29 validation_metadata_boundary

V30 route_unknown_field_rejection

V31 immutable_value_objects

V32 mutable_input_alias_isolation

V33 construction_failure_atomicity

V34 canonical_authority_untouched

V35 canonical_serialization_field_set

V36 scientific_boundary_exclusions

No check may be added, removed, reordered, or redefined after protocol freeze.

## 7. Synthetic fixture boundary

V1.1 uses deterministic synthetic identifiers and payload-free metadata.

It MUST NOT:

- access a GGUF/model payload;
- execute inference;
- perform query-to-PK selection research;
- attach a Query Capsule to the runtime;
- persist Query Route Cache authority;
- execute Phase 6D-Q2;
- execute Phase 6E;
- benchmark performance;
- access the network;
- launch subprocesses.

## 8. Publication standard

V1.1 MUST NOT use Python `os.link`.

V1.1 authoritative publication MUST use:

`libc.renameat2(..., RENAME_NOREPLACE)`

through Python standard-library `ctypes`.

No alternate publication primitive is authorized.

## 9. Exact renameat2 ABI

The runner must load the process C library using:

`ctypes.CDLL(None, use_errno=True)`

The runner must require the `renameat2` symbol.

Its ABI must be bound as:

- argument 1: `ctypes.c_int`
- argument 2: `ctypes.c_char_p`
- argument 3: `ctypes.c_int`
- argument 4: `ctypes.c_char_p`
- argument 5: `ctypes.c_uint`
- return type: `ctypes.c_int`

`RENAME_NOREPLACE` is exactly integer `1`.

Backend absence, ABI binding failure, invocation failure, or kernel
unsupported behavior is an explicit failure.

There is no fallback.

## 10. Same-parent relative publication

The partial and final result MUST be siblings in the same directory.

The publication helper must open that parent directory and use the same
already-open parent-directory fd for both source and destination.

The rename call must use only:

- `os.fsencode(partial.name)`
- `os.fsencode(final.name)`

not absolute source/destination strings.

The authoritative transition is exactly:

`renameat2(parent_fd, partial_name, parent_fd, final_name, RENAME_NOREPLACE)`

## 11. Partial creation

Before scientific execution the runner must reject if either the V1.1 final
or V1.1 partial pathname exists.

After all non-spending gates pass, exact-once reservation must create the
partial using exclusive creation equivalent to:

`O_WRONLY | O_CREAT | O_EXCL`

Once that reservation succeeds, V1.1 is permanently spent.

No automatic retry is permitted after reservation.

## 12. Write and durability order

After reservation:

1. execute V01-V36;
2. construct authoritative canonical result bytes;
3. write all bytes to the reserved partial;
4. flush the partial;
5. fsync the partial file;
6. open the parent directory;
7. execute exact `renameat2(..., RENAME_NOREPLACE)`;
8. require return code zero;
9. require the partial pathname to be absent;
10. require the final pathname to be a regular file;
11. fsync the parent directory;
12. report publication success.

The final result must never become visible as partially written content.

## 13. Collision semantics

If the final pathname exists before publication,
`RENAME_NOREPLACE` must fail rather than replace it.

On collision:

- the pre-existing final bytes must remain unchanged;
- the V1.1 partial must remain preserved;
- no weaker publication fallback may execute;
- the V1.1 slot remains spent if reservation already occurred.

## 14. Prohibited fallbacks

V1.1 publication must contain no executable fallback using:

- Python `os.link`;
- libc `link`;
- libc `linkat`;
- Python `os.replace`;
- Python plain `os.rename`;
- shell `mv`;
- subprocess publication;
- copy-to-final;
- symlink publication.

If the required backend cannot complete, publication fails explicitly.

## 15. Non-spending guard mode

The future runner must expose:

`--guard-false`

This mode must return without fixture construction, backend probing,
reservation, V01-V36 execution, or result creation.

## 16. Non-spending fixture qualification

The future runner must expose:

`--qualify-fixture`

This mode validates deterministic synthetic Capsule and Route Cache fixture
construction without executing V01-V36 or reserving the result slot.

## 17. Non-spending publication-backend qualification

The future runner must expose:

`--qualify-publication-backend`

This qualification must occur before exact-once scientific arming is
authorized.

It must use an isolated temporary directory on the actual execution
filesystem.

It must dynamically prove:

1. process libc loads;
2. `renameat2` exists;
3. exact ABI binding succeeds;
4. a complete temporary partial can be written and fsynced;
5. `RENAME_NOREPLACE` successfully publishes it;
6. successful publication consumes the temporary partial name;
7. final bytes exactly equal source bytes;
8. source/final inode identity is preserved across rename;
9. parent-directory fsync succeeds;
10. a deterministic collision refuses overwrite;
11. collision preserves existing final bytes;
12. collision preserves the unpublished partial;
13. qualification leaves no persistent repository artifact.

This qualification is non-scientific and non-spending.

It MUST NOT execute V01-V36.

## 18. Dual-arm scientific execution

Scientific V1.1 execution requires BOTH:

CLI:

`--arm-exact-once`

and environment:

`OPENMIND_ARM_QUERY_CAPSULE_DATA_MODEL_VALIDATION_V1_1=YES`

Either arm alone must refuse scientific execution and must not reserve the
result slot.

## 19. Pre-reservation ordering

The future runner must perform, in order:

1. guard-mode resolution;
2. qualification-mode resolution;
3. dual-arm verification;
4. clean V1.1 result namespace check;
5. frozen-authority verification;
6. deterministic fixture qualification;
7. publication-backend qualification;
8. exact-once O_EXCL reservation;
9. V01-V36 execution.

V01-V36 MUST NOT execute before reservation.

## 20. Post-reservation auditor errors

If an auditor error occurs after reservation, it is authoritative evidence.

The runner must construct and attempt to publish an authoritative failure
result containing that auditor error.

The V1.1 namespace must not be retried.

## 21. Result contract

The canonical V1.1 result must contain at minimum:

- schema
- exact_once
- runner_sha256
- validation_protocol_sha256
- data_model_protocol_sha256
- implementation_sha256
- predecessor_v1_verdict_sha256
- publication_backend
- expected_check_count
- check_count
- all_pass
- failed_checks
- checks
- auditor_error
- scientific boundary-exclusion booleans.

`publication_backend` must equal:

`libc.renameat2(RENAME_NOREPLACE)`

The ordered `checks` array must contain exactly V01-V36.

## 22. Canonical result bytes

The result must be UTF-8 canonical JSON using:

- `sort_keys=True`
- `separators=(",", ":")`
- `ensure_ascii=False`

followed by exactly one newline.

## 23. Acceptance requirements

A V1.1 scientific acceptance requires all of the following:

- exact frozen authority bindings;
- successful prior fixture qualification;
- successful prior real-filesystem publication-backend qualification;
- exact-once reservation;
- check_count == 36;
- exact ordered V01-V36 inventory;
- failed_checks == [];
- auditor_error == null;
- all scientific boundary exclusions false;
- all_pass == true;
- successful `renameat2(RENAME_NOREPLACE)` publication;
- V1.1 partial absent after successful publication;
- V1.1 final result present;
- final result canonical and SHA-stable;
- parent-directory fsync completed.

A 36/36 partial that fails publication is not a V1.1 acceptance.

## 24. Scientific nonclaims

V1.1 makes no claim regarding:

- query-to-PK selection correctness;
- selective inference sufficiency;
- bounded expansion;
- tensor/object avoidance;
- output quality;
- performance;
- MAF-native compute.

## 25. Phase progression

Phase 6D-Q1 remains blocked until V1.1 receives:

1. frozen protocol;
2. frozen runner;
3. successful non-spending fixture qualification;
4. successful real-filesystem publication-backend qualification;
5. exact-once readiness PASS;
6. one authoritative V1.1 scientific execution;
7. frozen authoritative final result;
8. frozen scientific acceptance verdict.

Phase 6D-Q2 remains blocked until Phase 6D-Q1 closes.

Phase 6E-A remains blocked pending closure of 6D-Q1 through 6D-Q4.

## 26. Runner construction authorization

Freezing this protocol authorizes construction and non-scientific auditing of
the V1.1 runner.

It does NOT authorize:

- publication-backend qualification;
- fixture qualification;
- exact-once scientific execution.

Those remain separate future gates.

## 27. Next gate

After this protocol freezes:

**BUILD VALIDATION V1.1 RUNNER CANDIDATE**

Scientific execution remains unauthorized.
