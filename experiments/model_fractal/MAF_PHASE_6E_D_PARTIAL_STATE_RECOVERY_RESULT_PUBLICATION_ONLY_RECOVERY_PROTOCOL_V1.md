# MAF Phase 6E-D Publication-Only Recovery Protocol V1

## 1. Purpose and authority

This protocol governs only publication of the already-created Phase 6E-D recovery qualification result.

The scientific recovery itself is not rerun.

The previously authorized recovery reached RCV01 through RCV15, including pre-promotion readback 339/339, one atomic runtime promotion, post-promotion readback 339/339, repository-state preservation, and all prohibited-activity gates.

The previous recovery execution failed only because Android/Termux Python did not expose `os.link` during final result publication.

Formal Phase 6E-D status remains blocked until this publication-only protocol is separately implemented and qualified.

Failure verdict:

`PUBLICATION-ONLY RECOVERY NOT QUALIFIED`

Success verdict:

`PUBLICATION-ONLY RECOVERY QUALIFIED`

## 2. Repository authority

- Branch: `labs/multidimensional-maf`
- Protocol parent HEAD: `a6300eb374db041a5f2bf2ebf6d345421d2515b3`
- Original untracked count: `440`
- Original untracked path-set SHA256: `8e4c81040c64f62df83b690dd7956de825bb4cb5a86dafa26ed3a65e90b0f219`

## 3. Prior frozen recovery authority

- Recovery protocol: `experiments/model_fractal/MAF_PHASE_6E_D_ENTRY_COMPLETE_MODEL_PERSISTENT_GENERATION_PARTIAL_STATE_RECOVERY_PROTOCOL_V1.md`
- Recovery protocol SHA256: `a6526b2ae971300f34937313b7ad52d877050355bcb5bbb28fe34d90871eed95`
- Corrected recovery runner: `experiments/model_fractal/maf_phase_6e_d_entry_complete_model_persistent_generation_partial_state_recovery_v1.py`
- Recovery runner HEAD: `a6300eb374db041a5f2bf2ebf6d345421d2515b3`
- Recovery runner SHA256: `419ab9d24dddaf44c5ae527f91d2a26b87764c0ca8b79c77f6e1a6a7efe9deb1`
- Recovery runner Git blob: `01d7ce02df75c2b8441422438af1691ef8f81814`
- Spent recovery sentinel: `/data/data/com.termux/files/home/.openmind_authoritative_slots/phase_6e_d_partial_state_recovery_a6300eb374db041a5f2bf2ebf6d345421d2515b3.spent`
- Spent recovery sentinel SHA256: `69f7458e011e18d78270f791c51e872d99a6becce64057582fa616cd435d1cd5`

The recovery sentinel is permanently spent.

The recovery runner must never be executed again.

## 4. Existing promoted state

- Building runtime: `/data/data/com.termux/files/home/OpenMind/results/runtime/maf_full_model_persistent_generation_v1.building`
- Required state: ABSENT
- Final runtime: `/data/data/com.termux/files/home/OpenMind/results/runtime/maf_full_model_persistent_generation_v1`
- Required state: PRESENT regular non-symlink directory
- Recovered model PK: `mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258`
- Recovered generation PK: `mafgen:v1:74e506919d3418e2c540413cdcce72c35605195ef8efa36cdad4c56ad2a167d2`
- Segment-manifest SHA256: `3ceff3ac93710ad0c789509a47a50d032c3834f3349d30c46140a9367376e982`
- Segment SHA256: `a930f1a1baae97279a3cbc50c1d126f3a70ef92d87f188f76747b2d7877109b9`

No object payload or segment-body access is authorized by this protocol.

## 5. Frozen source publication artifact

Source:

`/data/data/com.termux/files/home/OpenMind/results/runtime/maf_full_model_persistent_generation_v1/recovery_qualification_v1.json.partial`

Required frozen authority:

- regular non-symlink
- bytes: `2350`
- SHA256: `94207083df68717f5ed32a0aa20b6a60df798f39a0307a99ec46cbef146eb9d6`
- valid JSON object
- schema: `openmind.maf_phase_6e_d_partial_state_recovery.v1`
- verdict: `RECOVERED COMPLETE-MODEL PERSISTENT GENERATION QUALIFIED`
- object count: 339
- object-store qualification count: 339
- unique object PK count: 339
- strong locator count: 339
- payload authority match count: 339
- pre-promotion readback: 339
- post-promotion readback: 339
- all 15 encoded recovery gates: PASS
- no source GGUF access: true
- no object rematerialization: true
- no segment rematerialization: true
- no network access: true
- no inference/output-parity science: true

These exact bytes are the sole publication source.

The JSON must not be reconstructed, regenerated, normalized, reformatted, copied, or reserialized.

## 6. Frozen final target

Destination:

`/data/data/com.termux/files/home/OpenMind/results/runtime/maf_full_model_persistent_generation_v1/recovery_qualification_v1.json`

Before publication it must be absent under `lstat` semantics.

Any filesystem entry at the destination is a hard failure.

Overwrite is prohibited.

## 7. Exact publication primitive

The only permitted publication syscall is:

`renameat2(AT_FDCWD, source, AT_FDCWD, destination, RENAME_NOREPLACE)`

Frozen constants:

- `AT_FDCWD = -100`
- `RENAME_NOREPLACE = 1`

The source and destination must be in the same parent directory.

The publication runner must bind libc `renameat2` through `ctypes` with the exact five-argument ABI.

The runner must invoke `renameat2` exactly once.

`RENAME_NOREPLACE` is mandatory.

Fallback to `os.rename` is prohibited.

Fallback to `os.replace` is prohibited.

Copy publication is prohibited.

Hard-link publication is not required.

Automatic retry is prohibited.

Automatic rollback is prohibited.

## 8. Separate one-shot publication slot

A future publication runner must be frozen in Git before execution.

A separately qualified external launcher must create this publication-only sentinel before the runner may invoke `renameat2`:

`~/.openmind_authoritative_slots/phase_6e_d_publication_only_recovery_<FROZEN_PUBLICATION_RUNNER_HEAD>.spent`

Required sentinel creation:

- `O_WRONLY`
- `O_CREAT`
- `O_EXCL`
- mode `0600`
- canonical JSON
- exactly one terminal newline
- complete write loop
- sentinel file `fsync`
- parent-directory `fsync`
- exact byte readback

The publication sentinel remains permanently spent whether publication succeeds or fails.

## 9. Pre-publication gates

PUB01. Branch equals `labs/multidimensional-maf`.

PUB02. HEAD equals the future frozen publication-runner HEAD.

PUB03. Tracked worktree is clean and index is empty.

PUB04. Original untracked baseline remains exactly `440` paths with SHA256 `8e4c81040c64f62df83b690dd7956de825bb4cb5a86dafa26ed3a65e90b0f219`.

PUB05. This frozen protocol matches its future frozen SHA256 and Git blob.

PUB06. Recovery protocol remains SHA256 `a6526b2ae971300f34937313b7ad52d877050355bcb5bbb28fe34d90871eed95`.

PUB07. Corrected recovery runner remains SHA256 `419ab9d24dddaf44c5ae527f91d2a26b87764c0ca8b79c77f6e1a6a7efe9deb1` and Git blob `01d7ce02df75c2b8441422438af1691ef8f81814`.

PUB08. Recovery sentinel remains regular, non-symlink, and SHA256 `69f7458e011e18d78270f791c51e872d99a6becce64057582fa616cd435d1cd5`.

PUB09. New publication execution sentinel exists and exactly matches its frozen authority.

PUB10. Building runtime remains absent.

PUB11. Final runtime remains a regular non-symlink directory.

PUB12. Source partial remains exactly `2350` bytes and SHA256 `94207083df68717f5ed32a0aa20b6a60df798f39a0307a99ec46cbef146eb9d6` with the frozen semantics in Section 5.

PUB13. Destination remains absent under `lstat`.

PUB14. Source and destination have the same parent directory and libc `renameat2` with `RENAME_NOREPLACE` is available.

No publication syscall may occur unless PUB01 through PUB14 pass.

## 10. Sole authorized mutation

The only authorized runtime mutation is the same-directory atomic no-overwrite rename:

`/data/data/com.termux/files/home/OpenMind/results/runtime/maf_full_model_persistent_generation_v1/recovery_qualification_v1.json.partial`

to:

`/data/data/com.termux/files/home/OpenMind/results/runtime/maf_full_model_persistent_generation_v1/recovery_qualification_v1.json`

using:

`renameat2(AT_FDCWD, source, AT_FDCWD, destination, RENAME_NOREPLACE)`

No other runtime mutation is authorized.

## 11. Post-publication gates

PUB15. `renameat2` returned zero exactly once.

PUB16. Source partial is absent under `lstat`.

PUB17. Final result exists as a regular non-symlink file.

PUB18. Final result size is exactly `2350` bytes.

PUB19. Final result SHA256 is exactly `94207083df68717f5ed32a0aa20b6a60df798f39a0307a99ec46cbef146eb9d6`.

PUB20. Final result bytes exactly equal the source bytes captured before the syscall.

PUB21. Pre-rename source and post-rename final `st_dev`, `st_ino`, and `st_size` are identical.

PUB22. Final JSON semantics exactly match Section 5.

PUB23. Parent directory is opened read-only and successfully `fsync`ed after rename.

PUB24. Final result is reread after directory `fsync` and still exactly matches the frozen bytes and SHA256.

PUB25. Branch, HEAD, tracked worktree, index, and original untracked baseline remain invariant.

PUB26. No recovery rerun, object payload access, segment-body access, source GGUF access, inference, network access, or performance activity occurred.

All PUB01 through PUB26 are mandatory.

There is no partial pass.

## 12. Failure semantics

A failed PUB01-PUB14 gate prohibits the syscall.

A nonzero `renameat2` result fails closed and records `ctypes.get_errno()`.

After the publication sentinel is spent:

- no automatic retry
- no sentinel deletion
- no source recreation
- no final-result deletion
- no rollback

Any anomaly requires read-only diagnosis.

## 13. Success semantics

Only PUB01 through PUB26 all passing permits:

`PUBLICATION-ONLY RECOVERY QUALIFIED`

The exact unchanged recovery qualification bytes will then exist at:

`/data/data/com.termux/files/home/OpenMind/results/runtime/maf_full_model_persistent_generation_v1/recovery_qualification_v1.json`

Those bytes encode:

`RECOVERED COMPLETE-MODEL PERSISTENT GENERATION QUALIFIED`

This protocol does not authorize inference, output-parity science, performance work, Phase 6F, or Git push.

## 14. Explicit prohibitions

Prohibited:

- recovery-runner rerun
- spent recovery-sentinel mutation
- future spent publication-sentinel mutation
- object payload reads
- segment-body reads
- source GGUF access
- object or segment rematerialization
- generation rebuild
- generation-PK modification
- model-PK modification
- JSON reconstruction or rewrite
- copy publication
- overwrite-capable publication
- fallback `os.rename`
- fallback `os.replace`
- network access
- inference
- prompt execution
- token generation
- logits
- parity science
- performance benchmarking
- automatic retry
- automatic rollback

## 15. Next permitted activity

After this protocol is frozen:

1. construct a publication-only runner,
2. statically qualify it,
3. freeze that runner in a separate commit,
4. construct and statically qualify an external one-shot publication launcher,
5. separately authorize one publication attempt.

Until then:

`PHASE 6E-D PUBLICATION-ONLY RECOVERY EXECUTION BLOCKED`
