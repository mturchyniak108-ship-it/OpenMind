# OpenMind AI Collaboration Instructions

<!-- OPENMIND:TERMUX-ATOMIC-PASTE:START -->
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
<!-- OPENMIND:TERMUX-ATOMIC-PASTE:END -->

## Human Authority Rule

OpenMind source code is modified by human contributors.

AI agents are collaborators, not autonomous repository maintainers.

An AI agent may inspect the repository, analyze code, propose implementations, generate suggested patches or commands, review changes, assist with debugging, design tests, analyze benchmarks, and help document work.

The human counterpart must review and apply source-code modifications and decide whether a proposed change enters the repository.

## Collaboration Model

AI work should support human understanding rather than bypass it.

When proposing a change, explain:

1. the problem being addressed;
2. the relevant source or evidence;
3. the proposed modification;
4. expected behavior;
5. required validation;
6. important risks or limitations.

Prefer small, reviewable proposals.

## Verification

Do not treat AI-generated code as correct merely because it is syntactically plausible.

Use repository builds, tests, debuggers, benchmarks, provenance checks, and research controls as appropriate.

## Research Claims

Do not promote `lab_candidate` or `historical` work into implemented or validated capability.

Follow `docs/ai/EXPERIMENT_PROMOTION.md` and the repository evidence hierarchy.

## Canonical Guidance

Human and AI collaborators should use:

- `docs/README.md` for documentation navigation;
- `docs/development/BEST_PRACTICES.md` for shared engineering practice;
- `docs/development/TESTING.md` for testing guidance;
- `docs/data/REPRODUCIBILITY.md` for reproducibility;
- `docs/labs/README.md` for experimental status;
- `docs/ai/EXPERIMENT_PROMOTION.md` for research promotion boundaries.

The `llama.cpp/` directory is an external dependency and has its own upstream `AGENTS.md` and project rules.
