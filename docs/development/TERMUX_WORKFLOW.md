# OpenMind Termux Workflow

## Termux Atomic Paste Safety

For interactive Termux click-paste work, shell heredocs are prohibited. Do not use `<<EOF`, `<<'PY'`, `cat <<...`, multiline `python <<...`, or equivalent heredoc forms.

Required practice:

- use one atomic no-heredoc command;
- prefer `python -c` or an already tracked script bound to an exact SHA256;
- hard-bind branch, HEAD, and important artifact hashes before mutation;
- stage exact intended paths only; never use `git add .`, `git add -A`, or `git add --all`;
- never use `exit` or `logout` in click-paste packets;
- a failed gate stops only the operation and leaves Termux open;
- keep scientific execution separate from source assembly, documentation, Git commits, and remote publication;
- emit a bounded Gold Standard return packet.

If Termux unexpectedly shows `>`, treat the operation as incomplete and execution state as unproven. Cancel the pending input, verify Git and artifact state, and do not assume any embedded program executed.

## Recovery From an Unexpected `>` Prompt

1. Cancel the incomplete pending input.
2. Return to the normal `~/OpenMind $` prompt.
3. Verify branch and HEAD.
4. Verify tracked and staged state.
5. Recheck important artifact hashes.
6. Recheck result and partial paths.
7. Retry only with an atomic no-heredoc command.

## Current Q2 Boundary

- active authority: Q2 V1.4
- authoritative result: `PASS — 74/74`
- V01-V74: `ALL PASS`
- result SHA256: `b2ad49d7a9a3e1ef565e07e595efc4a4e00b283f422723553c6437ef3a42def6`
- verdict SHA256: `c17198e0013fd9c0a8c59b8f09c05d4f22693dc7d56afdc0f761f55a008c2663`
- exact-once namespace: `PERMANENTLY SPENT`
- scientific retry: `FORBIDDEN`
- next gate: `6D-Q3 — attach/detach ownership and cleanup semantics`
- Phase 6E: `NOT ENTERED`

Termux documentation, Git operations, and publication must never invoke the V1.4 runner or alter its slot, result, or verdict.
