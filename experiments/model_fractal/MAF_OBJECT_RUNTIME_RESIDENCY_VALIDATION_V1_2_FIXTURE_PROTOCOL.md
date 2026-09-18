# MAF Object Runtime Residency Validation V1.2
## Dedicated Four-Object Authority Fixture Construction Protocol

Status: PROSPECTIVE PREREGISTRATION
Phase: 6C
Artifact class: fixture-construction protocol
Construction status: NOT YET EXECUTED
Scientific validation status: NOT YET PREREGISTERED
Engine verdict: NONE

## 1. Purpose

This protocol preregisters one dedicated persistent four-object MAF authority
fixture for future runtime-residency validation V1.2.

It corrects only the fixture-cardinality defect proven after the permanently
spent V1.1 validation attempt.

V01-V32 scientific semantics remain unchanged.
The runtime-residency engine remains unchanged.
This protocol does not authorize fixture execution or V1.2 validation.

## 2. Frozen parent

Branch:

`labs/multidimensional-maf`

Parent:

`3edf6c19469d857e98a0f5c752efa31b310d96d6`

## 3. Historical constraint

V1.1 stopped before V01 because its frozen fixture exposed only two
positive-length Resident PK authority entries while the unchanged matrix
requires a maximum simultaneous cardinality of four.

Proven requirements:

- V01: at least 3 distinct entries;
- V25: at least 2 entries;
- V28: exactly 4 usable distinct entries;
- unchanged matrix fixture minimum: 4 positive-length entries.

V1 and V1.1 must never be rerun.

The correction is a new fixture.
The four-entry requirement must not merely be lowered.

## 4. Frozen dependencies

Generation Engine V1:

`experiments/model_fractal/maf_generation_engine_v1.py`

SHA256:

`8868c58e98084226dd957391e1a2f4d1122e886607640ae0be59279f025f1a51`

Activation V1.1 wrapper:

`experiments/model_fractal/maf_activation_v1_1.py`

SHA256:

`9435ae8dd32656c7350887689d453f3cb8460887068bfaf06e6f68b5b5b927a1`

Base Activation V1:

`experiments/model_fractal/maf_activation_v1.py`

SHA256:

`76d79f90d9bc30118a6dfe0297beacd9b323aed9f56876881f653a2c01c1f210`

Runtime-residency engine:

`experiments/model_fractal/maf_object_runtime_residency_v1.py`

SHA256:

`4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9`

Resident PK Directory V1:

`experiments/model_fractal/maf_resident_pk_directory_v1.py`

SHA256:

`4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6`

Segment Reader V1:

`experiments/model_fractal/maf_segment_reader_v1.py`

SHA256:

`3499cb8e528fe8e9315e3e5656d6aa888c95ca175310b6371e722de409827369`

V1.1 raw result SHA256:

`18204da5e5c50af29a1a5f67a26288a6aec48bf35c2d09b5415c82f0113ad778`

## 5. Future builder and fixture paths

Builder:

`experiments/model_fractal/maf_object_runtime_residency_validation_v1_2_fixture.py`

Construction result:

`experiments/model_fractal/maf_object_runtime_residency_validation_v1_2_fixture.json`

Runtime fixture root:

`results/runtime/maf_object_runtime_residency_validation_v1_2_fixture`

Successful fixture files:

- `segment_00000000.mafseg`
- `candidate_a.manifest.json`
- `active_generation.json`

The dedicated fixture root and construction-result path must both be absent
before the one authorized builder invocation.

## 6. Exact-once fixture-construction rule

The builder must be implemented, statically audited, and frozen in Git before
execution.

Immediately before execution, protocol SHA256, builder SHA256, frozen
dependency SHAs, repository state, and output-path absence must be checked.

The first invocation spends the fixture-construction slot whether it succeeds
or fails.

After invocation:

- never edit and rerun that frozen builder version;
- retain all produced residue as evidence;
- freeze the raw construction result before interpretation;
- use a prospectively preregistered successor version for any correction.

No cleanup may disguise a failed construction attempt.

## 7. Exact model

`mafmodel:v1:b3d13be495d56e4fa7bafe145bf4efdc3b5dc13596446252d45f8adadd340a1b`

## 8. Exact deterministic segment

Length:

`4096`

For every zero-based byte index `i` with `0 <= i < 4096`:

`byte[i] = ((i * 73) + 19) % 256`

Whole-segment SHA256:

`f965b526538d757ca2d6114af6517c57cbcb3650b71d8cfb92046a04ef2f566b`

The builder must generate these bytes from the formula and verify this exact
hash before generation construction.

It must not obtain the fixture by copying historical fixture bytes.

The segment file must be created new.

Protected byte index `3500` must remain outside every object range.

## 9. Exact four objects

### A

Object PK:

`mafobj:v1:ea258c628d783a1e140430a6bbde438f97f0be7d85e5f218ee149ad3b1fb2815`

Range:

`[64, 576)`

Offset `64`, length `512`.

`object_file_sha256`:

`f9849113558b125c1cfa52b62e5625d362300ff2d9897ca8bb7143dd4473f611`

`payload_sha256`:

`f9849113558b125c1cfa52b62e5625d362300ff2d9897ca8bb7143dd4473f611`

### B

Object PK:

`mafobj:v1:ecec2d8fcca3888752e67802867631919dbfeb2bafbd137b45441a068f346deb`

Range:

`[1024, 1664)`

Offset `1024`, length `640`.

`object_file_sha256`:

`4e492d3bdc486105115cb3c1ffa07b688385f88fe23dc7881acd3f0bd00585e4`

`payload_sha256`:

`4e492d3bdc486105115cb3c1ffa07b688385f88fe23dc7881acd3f0bd00585e4`

### C

Object PK:

`mafobj:v1:cc2c9d0c6eab228cadf17888746a3d432ed6e361c4a59678a5015f80d65c24ba`

PK seed:

`openmind-phase6c-v1.2-object-c`

PK derivation:

`"mafobj:v1:" + SHA256(UTF8(seed))`

Range:

`[1792, 2560)`

Offset `1792`, length `768`.

`object_file_sha256`:

`d1031a4a74d6d775c24a8cc0a29760ed01e97254eaab4c845323dc2ed15eac1f`

`payload_sha256`:

`d1031a4a74d6d775c24a8cc0a29760ed01e97254eaab4c845323dc2ed15eac1f`

### D

Object PK:

`mafobj:v1:b68292655c246c99a9c1796dcaa4f12dbaa1e6fc668d44d9e6890bce38084b93`

PK seed:

`openmind-phase6c-v1.2-object-d`

PK derivation:

`"mafobj:v1:" + SHA256(UTF8(seed))`

Range:

`[2688, 3488)`

Offset `2688`, length `800`.

`object_file_sha256`:

`5b300021bebaa7ccdaed30c058cae6511533fad0101892fda2017bef69931a79`

`payload_sha256`:

`5b300021bebaa7ccdaed30c058cae6511533fad0101892fda2017bef69931a79`

For this dedicated fixture only, each logical payload is defined as the exact
authoritative serialized object range. Therefore:

`payload_sha256 == object_file_sha256`

This is a fixture rule, not a universal MAF invariant.

## 10. Required range invariants

Before generation construction the builder must prove:

- exactly four objects;
- four distinct object PKs;
- all lengths positive;
- all offsets nonnegative;
- all ranges within 4096 bytes;
- all ranges pairwise non-overlapping;
- byte 3500 outside all object ranges;
- exact A-D range hashes match this protocol;
- historical A range/hash preserved;
- historical B range/hash preserved.

## 11. Required V1.1-compatible ordering

Future validation must retain:

`sorted(entries, key=(entry.length, entry.object_pk))`

This fixture must sort exactly:

`A, B, C, D`

Thus:

- V01 uses A, B, C;
- V25 has B as its second entry;
- V28 uses A, B, C, D.

No V01-V32 scientific check is changed to obtain this cardinality.

## 12. Generation construction

The builder must call frozen:

`maf_generation_engine_v1.build_generation`

with:

- exact model PK;
- one 4096-byte segment;
- exact whole-segment SHA256;
- exactly four A-D object inputs;
- manifest path `candidate_a.manifest.json`.

It must not manually fabricate ResidentPKEntry authority.

The frozen Generation Engine remains responsible for canonical descriptor
construction, descriptor hashing, generation-PK derivation, manifest
construction, and candidate verification.

Expected sole generated segment ID:

`segment:00000000`

Any other segment ID is construction failure.

Generation identity remains:

`"mafgen:v1:" + SHA256(canonical_descriptor_bytes)`

## 13. Physical verification and activation

Before authority publication the builder must call frozen:

`maf_activation_v1_1.activate_generation`

using the actual dedicated segment mapping.

The V1.1 wrapper must physically reconstruct and exactly reproduce the
candidate descriptor and generation identity.

It then delegates to frozen `maf_activation_v1`.

Frozen active-record schema:

`openmind.maf_active_generation.v1`

Frozen active-record version:

`maf_active_generation_v1`

The active record binds:

- model PK;
- generation PK;
- SHA256 of exact canonical candidate-manifest bytes.

The base activation implementation canonicalizes the record, writes a
create-new `.partial`, fsyncs and verifies it, then atomically publishes with
`os.replace`.

Atomic replacement is legitimate activation behavior. For this dedicated
fixture, safety is provided by the stronger preregistered precondition that
the complete fixture root is absent before the first authorized construction.

No `.partial` file may remain after successful construction.

## 14. Construction result

The builder must write exactly one create-new raw result:

`experiments/model_fractal/maf_object_runtime_residency_validation_v1_2_fixture.json`

Schema:

`openmind.maf_object_runtime_residency_validation.v1.2.fixture`

It must record at minimum:

- schema and fixture version;
- protocol path and SHA256;
- builder path and SHA256;
- frozen dependency identities;
- fixture root;
- model PK;
- generated generation PK;
- generated manifest SHA256;
- segment SHA256;
- entry count;
- positive-length entry count;
- exact A-D PK/range/hash data;
- check mapping;
- failed-check list;
- `construction_valid`;
- `all_pass`;
- fatal type/message when applicable.

A caught construction failure must still produce a raw result whenever this
can be done safely without overwriting an existing result.

## 15. Successful postconditions

Success requires:

1. exactly the intended three persistent fixture files;
2. 4096-byte segment with exact preregistered SHA256;
3. canonical candidate manifest;
4. valid Generation Engine manifest;
5. exact model PK;
6. exactly one segment;
7. segment ID `segment:00000000`;
8. exactly four objects;
9. exact A-D PKs, ranges, and hashes;
10. four positive-length entries;
11. four distinct object PKs;
12. canonical active record;
13. active model PK equals candidate model PK;
14. active generation PK equals verified candidate generation PK;
15. active manifest SHA equals SHA256 of exact candidate-manifest bytes;
16. frozen sort order yields A, B, C, D;
17. no `.partial` authority file remains;
18. runtime-residency engine SHA remains unchanged;
19. no V1.2 scientific validation has executed.

## 16. Failure classification

Fixture-construction failure is not a runtime-residency engine failure.

No engine verdict may be inferred from fixture construction.

V1.2 validation may not begin after an invalid construction.

## 17. Freeze sequence

After this protocol is committed:

1. implement fixture builder;
2. static-audit builder against this protocol;
3. commit builder locally;
4. perform final no-write exact-once construction preflight;
5. invoke frozen builder exactly once;
6. freeze raw construction result immediately;
7. freeze exact fixture hashes;
8. only then preregister scientific runtime-residency validation V1.2.

## 18. Authorization boundary

Freezing this protocol authorizes only implementation and static audit of the
fixture builder.

It does **not** authorize fixture execution.

It does **not** preregister or authorize V1.2 scientific validation.

V1 RERUN: FORBIDDEN.

V1.1 RERUN: FORBIDDEN.

No upstream push is authorized.
