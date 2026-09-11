# MAF — Model Address Fabric AI Collaboration Instructions

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

<!-- OPENMIND:Q2-V1-4-AUTHORITY:START -->
## Current Q2 Exact-Once Research Boundary

For Phase 6D-Q2, the authoritative frozen validation authority is V1.4:

- scientific result: `PASS — 74/74`;
- authoritative V01-V74: `ALL PASS`;
- exact-once slot: `PERMANENTLY SPENT`;
- retry: `FORBIDDEN`;
- result SHA256: `b2ad49d7a9a3e1ef565e07e595efc4a4e00b283f422723553c6437ef3a42def6`;
- verdict SHA256: `c17198e0013fd9c0a8c59b8f09c05d4f22693dc7d56afdc0f761f55a008c2663`;
- freeze commit: `10da372a8317dc629674fb2b52a7560f55ee416f`.

The earlier post-run shell-auditor failure label is superseded: it resulted
from an incorrect assumption about the result `checks` representation and was
not produced by the V1.4 runner. The forensic audit confirmed the exact
74-check order and the permanent slot journal hash chain.

AI collaborators must preserve the frozen authority. Do not import, execute,
repair, regenerate, or rerun V1.4. The Q2 PASS is limited to query-to-PK
selection validation and does not establish inference, answer generation,
selective working-set sufficiency, tensor/object avoidance, output parity,
answer quality, performance superiority, MAF-native compute, or conventional
LLM replacement.

Any next Phase 6D-Q experiment requires a new preregistered gate. Phase 6E
remains not entered.
Successor gate: **6D-Q3 — attach/detach ownership and cleanup semantics** under a new preregistered authority.

AI collaborators must not reuse, regenerate, repair, or rerun Q2 V1.4. Human-readable closure: `docs/research/Q2_V1_4_SUMMARY.md`.
<!-- OPENMIND:Q2-V1-4-AUTHORITY:END -->

## Human Authority Rule

MAF source code is modified by human contributors.

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
