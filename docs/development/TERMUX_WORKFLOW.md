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

- frozen runner commit: `09b2d6fd887155f9fda8fff6405b31ac556ed42b`
- frozen runner SHA256: `e2e32f85b1dc7015802ec51a6f214188becc5d35f45c76f4b320617ccd6cd873`
- authoritative run: not executed
- V01-V48: not executed
- exact-once result slot: `UNSPENT`
