# OpenMind Phase 6E-D Entry — Complete-Model Persistent Generation Partial-State Recovery Protocol V1

## 1. Purpose

This protocol defines a separate fail-closed recovery boundary for the preserved complete-model partial state produced by the spent Phase 6E-D materialization attempt.

It does not rerun, reinterpret, or retroactively convert the failed authoritative materialization attempt into a pass.

The original authoritative verdict remains:

`COMPLETE-MODEL PERSISTENT GENERATION NOT QUALIFIED`

Recovery may establish a new independently qualified recovered persistent generation only through the gates frozen below.

## 2. Frozen recovery checkpoint

- Branch: `labs/multidimensional-maf`
- Recovery-protocol parent HEAD: `f386695eb0769a5367c42ed00d02a2f12181acbd`
- Original materialization runner: `experiments/model_fractal/maf_phase_6e_d_entry_complete_model_persistent_maf_payload_generation_v1.py`
- Original materialization runner SHA256: `e0c9d56adc35b4e34603ba8d031cb6569246c0d8d6775bc0d86ac074225e63a4`
- Original materialization runner Git blob: `e2c407e72ec45cfc32e8ef2b70f81b7f49ed3758`
- Original construction protocol SHA256: `f599a652ae88bcf7ae193bdc26e42fdde89b6bef21a98012a061e55bb48919bb`
- Frozen inventory SHA256: `7acf6d5dc672182aee0244b1bb85a47466f33dbdcdf10bde863e24f3659240ee`
- Frozen full-model identity SHA256: `ef954f38e16ccbc73211c503d7d9c9b8462028d6222fb32fb9b15eb59615d25d`
- Frozen compile-recipe validation SHA256: `ceed863754a119fc59b6fdeb80b9a6d1766bfa47e33992315536669f58331ccd`
- Frozen full representation SHA256: `0e70bc32fb76945d7c684b3d73d5598f587fd17c6bda77b32db3e601af3f8dbe`
- Frozen object API SHA256: `eed6cbd96995412a632883f3c534f9023e7711ea8eb437afe35a48312502f63b`
- Frozen segment builder SHA256: `f063c87989f9a646497743034e85d3f4674a7b45cf88df754b669d6621cc28f0`
- Frozen generation engine SHA256: `8868c58e98084226dd957391e1a2f4d1122e886607640ae0be59279f025f1a51`
- Frozen segment reader SHA256: `3499cb8e528fe8e9315e3e5656d6aa888c95ca175310b6371e722de409827369`
- Frozen resident PK directory SHA256: `4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6`

No recovery implementation may silently substitute a different frozen authority.

## 3. Original one-shot state is immutable

- Original spent sentinel: `/data/data/com.termux/files/home/.openmind_authoritative_slots/phase_6e_d_complete_model_persistent_generation_f386695eb0769a5367c42ed00d02a2f12181acbd.spent`
- Original spent sentinel SHA256: `abd8b27a648048d59a8cd9ab9e5fd2fb65ecaf3067d202ff31124da3f5519bfb`
- Original runner execution count authorized: exactly one
- Original runner execution count already consumed: one
- Original materialization runner rerun: forbidden
- Original spent sentinel deletion or replacement: forbidden

Recovery must use a separately defined recovery execution slot. A recovery slot must never reuse, remove, rename, overwrite, or reinterpret the original spent sentinel.

## 4. Preserved partial-state authority

The only partial state authorized for this recovery protocol is the exact preserved namespace:

`results/runtime/maf_full_model_persistent_generation_v1.building/`

Frozen stat and metadata observations at protocol construction:

- Final runtime exists: `NO`
- Building runtime is a regular non-symlink directory: `YES`
- Serialized object regular-file count: `339`
- Serialized object partial-file count: `0`
- Serialized object symlink count: `0`
- Serialized object aggregate stat bytes: `1888934699`
- Preserved segment: `segment_00000000.mafseg`
- Preserved segment stat bytes: `1888934699`
- Preserved segment manifest: `segment_00000000.manifest.json`
- Preserved segment manifest SHA256: `3ceff3ac93710ad0c789509a47a50d032c3834f3349d30c46140a9367376e982`
- Segment manifest schema: `openmind.maf_segment_manifest.v1`
- Segment manifest model PK: `mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258`
- Segment manifest recorded segment SHA256: `a930f1a1baae97279a3cbc50c1d126f3a70ef92d87f188f76747b2d7877109b9`
- Segment placement count: `339`
- Unique segment placement PK count: `339`
- Existing generation manifest: `NO`
- Existing recovery qualification result: `NO`

The aggregate object and segment byte equality is an observed stat property only. It does not replace cryptographic recovery qualification.

## 5. Proven original integration defect

The failed runner passed `object_records` as the generation-engine `objects` argument.

Those pre-segment records lacked all three placement fields required by the frozen generation engine:

- `length`
- `offset`
- `segment_path`

The frozen generation engine requires object placement records containing at least:

- `model_pk`
- `object_pk`
- `segment_path`
- `offset`
- `length`
- `object_file_sha256`
- `payload_sha256`

This integration defect is the recovery basis. Recovery must not reconstruct or reread source payloads merely to repair a metadata-shape failure occurring after segment construction.

## 6. Recovery scope

Recovery is limited to validating and completing generation metadata from the preserved serialized objects, segment, and segment manifest.

Recovery explicitly forbids:

- opening, hashing, or reading the source GGUF
- calling `compile_object` or any equivalent source-payload materializer
- recreating any of the 339 serialized object files
- rewriting any preserved serialized object file
- rebuilding or rewriting the preserved segment
- deleting or replacing the preserved segment manifest
- rerunning the original materialization runner
- replacing any of the 339 qualified logical PKs
- inference, prompts, token generation, logits, output-parity measurement, or performance science
- network access
- Git history rewriting

Recovery is allowed to read the preserved serialized objects and segment only after a separately frozen recovery runner and recovery execution preflight authorize that access.

## 7. Placement-record reconstruction contract

Recovery generation placement records must be derived only from the frozen segment manifest and frozen recovery runtime path.

For each of the 339 segment-manifest object rows, the recovery runner must construct exactly one generation-engine placement record with:

- `model_pk` equal to the frozen segment-manifest model PK
- `object_pk` copied exactly from the segment manifest
- `segment_path` equal to the preserved recovery segment path at execution time
- `offset` copied exactly from the segment manifest
- `length` copied exactly from the segment manifest
- `object_file_sha256` copied exactly from the segment manifest
- `payload_sha256` copied exactly from the segment manifest

No placement field may be recovered from filename order, filesystem order, guessed offsets, source GGUF metadata, or pre-segment `object_records`.

Success requires exactly 339 placement records, exactly 339 unique qualified object PKs, and zero unexpected PKs.

## 8. Preserved object-store qualification

Before generation completion, every preserved serialized object file must be independently qualified against frozen authorities.

For all 339 objects require:

- regular non-symlink file
- no sibling `.partial` object
- exact serialized-object SHA256 equals the segment-manifest `object_file_sha256` for the same qualified PK
- frozen object-format structural validation passes
- decoded tensor name equals frozen full-model identity authority
- decoded tensor type equals frozen full-model identity authority
- decoded dimensions equal frozen full-model identity authority
- decoded payload length equals frozen inventory authority
- decoded payload SHA256 equals both the segment-manifest authority and frozen inventory authority
- decoded logical identity remains the already-qualified object PK

Object qualification must be bounded and streaming. At most one large object payload may be actively validated at a time.

## 9. Preserved segment qualification

The preserved segment must be independently qualified before generation metadata is accepted.

Require:

- regular non-symlink segment file
- stat length equals `1888934699`
- full streamed segment SHA256 equals `a930f1a1baae97279a3cbc50c1d126f3a70ef92d87f188f76747b2d7877109b9`
- segment manifest SHA256 remains `3ceff3ac93710ad0c789509a47a50d032c3834f3349d30c46140a9367376e982`
- segment-manifest object count remains 339
- every object placement lies entirely inside the segment
- every placed byte range hashes to its recorded `object_file_sha256`
- every placement PK belongs to the frozen 339-PK namespace
- zero overlapping or out-of-range placements unless explicitly permitted by the frozen segment format, which this recovery does not assume

The frozen generation engine may perform streamed segment and object-range hashing as part of this qualification.

## 10. Generation construction contract

Only after Sections 8 and 9 pass may the recovery runner invoke the frozen generation engine.

The recovery runner must call the frozen generation engine with:

- the frozen model PK
- exactly one preserved segment record
- exactly 339 reconstructed placement records
- a create-once generation-manifest path inside the preserved building runtime
- the frozen bounded chunk size selected by the recovery runner

The generation engine must reopen and verify the persisted candidate manifest under its frozen implementation.

Generation success requires:

- one deterministic generation PK
- exactly 339 generation object records
- exactly 339 unique qualified object PKs
- zero unexpected object PKs
- exactly one segment authority
- 339 of 339 strong locator coverage
- generation metadata that remains path-independent and relocation-safe

## 11. Segment-reader and object-format recovery readback

Generation creation alone is not recovery qualification.

Every one of the 339 generation locators must be read back through the frozen MAF segment reader.

For every readback require:

- requested PK equals the locator PK
- returned serialized byte count equals locator length
- serialized-object SHA256 equals locator `object_file_sha256`
- frozen object-format structural decode succeeds
- decoded tensor name equals frozen tensor name
- decoded tensor type equals frozen tensor type
- decoded dimensions equal frozen dimensions
- decoded payload length equals frozen payload length
- decoded payload SHA256 equals frozen payload SHA256
- locator resolves only to the single preserved recovery segment

Readback qualification must be bounded one object at a time.

## 12. Promotion contract

The building runtime must not be promoted merely because a generation manifest was written.

Before promotion require all pre-promotion recovery gates to pass and require the final runtime path to remain absent.

Promotion is one atomic directory rename:

`results/runtime/maf_full_model_persistent_generation_v1.building/`

to:

`results/runtime/maf_full_model_persistent_generation_v1/`

No copy-and-delete promotion is authorized.

After promotion, all 339 locators must again be resolvable against the final segment path and must pass frozen segment-reader readback. This post-promotion readback prevents qualification from depending only on the former `.building` path.

A post-promotion failure must not trigger automatic rollback, automatic rerun, or deletion of the recovery execution sentinel.

## 13. Recovery result publication

A recovery qualification result may be published only after successful post-promotion readback.

The result must record at minimum:

- parent recovery protocol SHA256
- recovery runner SHA256 and Git blob
- original failed-run HEAD
- original spent-sentinel path and SHA256
- preserved segment-manifest SHA256
- preserved segment SHA256
- model PK
- recovered generation PK
- object count
- unique object PK count
- strong locator count
- object-store qualification count
- pre-promotion segment-reader readback count
- post-promotion segment-reader readback count
- payload-authority match count
- PG14 repository state
- explicit no-source-GGUF-access assertion backed by recovery-runner design

A successful recovery result is new recovery evidence. It does not alter the verdict of the spent original run.

## 14. Recovery one-shot semantics

Recovery execution requires a new recovery-specific one-shot sentinel derived from the future frozen recovery-runner HEAD.

Before any recovery payload read or partial-state mutation, the execution wrapper must atomically create and fsync that recovery sentinel using `O_CREAT | O_EXCL`.

If any recovery step fails after spending the recovery slot:

- the recovery sentinel remains spent
- the sentinel must not be deleted
- the recovery runner must not automatically rerun
- the partial or promoted state must be diagnosed read-only before any new recovery protocol is considered

The original materialization sentinel remains independent and permanently spent.

## 15. Git and PG14 isolation

Recovery runtime artifacts remain under the already-frozen ignored final and building namespaces.

Before recovery execution require:

- exact frozen branch and HEAD
- tracked worktree clean
- index empty
- exact preexisting untracked baseline
- exact recovery runner SHA256 and Git blob
- exact recovery protocol SHA256
- exact frozen authority SHAs

After recovery execution require:

- tracked worktree clean
- index empty
- the same preexisting untracked baseline
- no unrelated runtime namespace suppression

Git staging and commits are not part of recovery execution.

## 16. Recovery qualification gates

A recovered complete-model persistent generation is qualified only if every gate passes:

- `RCV01` frozen repository, recovery protocol, authorities, original runner identity, and original spent sentinel all match before access or mutation.
- `RCV02` preserved building state has exactly 339 regular serialized objects, zero partial objects, zero object symlinks, one segment, one exact segment manifest, no generation manifest, and no final runtime.
- `RCV03` frozen segment manifest has exactly 339 unique qualified PK placements and zero unexpected PKs.
- `RCV04` recovery performs no source GGUF access and performs no object or segment rematerialization.
- `RCV05` all 339 preserved serialized object files pass exact SHA, structural, tensor metadata, payload length, and payload SHA qualification.
- `RCV06` preserved segment length and full streamed SHA256 match the frozen segment-manifest authority.
- `RCV07` exactly 339 generation-engine placement records are reconstructed only from the frozen segment manifest plus the preserved segment path.
- `RCV08` frozen generation engine creates and reopens one valid generation manifest with exactly 339 qualified PKs and 339 of 339 strong locator coverage.
- `RCV09` recovered generation PK is deterministic, valid, and bound to the frozen model PK and preserved segment authority.
- `RCV10` pre-promotion frozen segment-reader readback succeeds for all 339 objects with full decoded tensor and payload authority validation.
- `RCV11` no preexisting final target, generation manifest, recovery result, preserved object, segment, or segment manifest is overwritten.
- `RCV12` building-to-final promotion occurs by one atomic directory rename only after all pre-promotion gates pass.
- `RCV13` post-promotion frozen segment-reader readback succeeds for all 339 objects from the final runtime path.
- `RCV14` tracked Git state, index, and preexisting untracked baseline remain unchanged by recovery execution.
- `RCV15` no inference, prompt, token generation, logits, output-parity measurement, performance science, network access, or source GGUF access occurs.

Any single failed gate means:

`PARTIAL-STATE RECOVERY NOT QUALIFIED`

No partial pass may be promoted to recovery qualification.

## 17. Success claim boundary

If and only if RCV01 through RCV15 all pass, the narrow recovery claim is:

`RECOVERED COMPLETE-MODEL PERSISTENT GENERATION QUALIFIED`

This means the preserved post-materialization state was independently validated and completed into a qualified persistent 339-object MAF generation without rereading or rematerializing source GGUF payloads.

It does not establish:

- MAF-native compute
- selective inference correctness
- output parity
- output quality
- performance improvement
- physical-I/O superiority
- generalization beyond the frozen model

## 18. Authorization boundary of this protocol

Freezing this protocol authorizes none of the following:

- recovery runner execution
- source GGUF access
- serialized object payload reads
- segment payload reads
- generation manifest creation
- recovery result creation
- building-to-final promotion
- model loading
- inference
- Phase 6E-D output-parity science
- Phase 6F performance work

The next permitted activity after this protocol is frozen is recovery-runner construction followed by static qualification and a separate freeze.
