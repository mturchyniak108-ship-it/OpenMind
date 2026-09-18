# MAF Development Best Practices

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

## Purpose

MAF is developed by human contributors with AI systems acting as engineering collaborators.

The quality standard does not depend on whether an idea originated with a person or an AI. Changes are accepted based on human review, reproducibility, tests, debugging evidence, benchmarks, and research controls where applicable.

## Human Authority

Only human contributors modify MAF source code and decide what enters the repository.

AI collaborators may:

- inspect source and repository state;
- explain code and architecture;
- identify defects and risks;
- propose code or patches for human review;
- propose terminal commands;
- analyze compiler, test, debugger, benchmark, and profiler output;
- design tests and experiments;
- review human-applied changes;
- assist with documentation;
- interpret results while respecting evidence boundaries.

AI collaborators must not be treated as autonomous repository maintainers.

## Shared Engineering Workflow

```text
Understand the problem
        |
        v
Inspect relevant source and evidence
        |
        v
Human + AI discuss candidate solution
        |
        v
Human reviews and applies the change
        |
        v
Build / syntax validation
        |
        v
Focused tests
        |
        v
Debug failures if present
        |
        v
Regression tests
        |
        v
Benchmark / research validation when required
        |
        v
Human reviews evidence
        |
        v
Human commits or rejects the change
```

## Change Discipline

Prefer the smallest change that can answer the engineering question.

Keep unrelated changes in separate commits. Avoid rewriting working code merely to make it stylistically different.

Before preserving a change, identify:

- why the change exists;
- what behavior should change;
- what behavior must not change;
- how success will be measured;
- how failure will be detected.

## Testing

Use the narrowest useful test first, followed by broader regression testing.

Common validation includes:

```bash
python -m compileall -q .
git diff --check
pytest -q
```

Native C++ changes should also use the relevant CMake build and CTest targets.

A passing test demonstrates only what that test covers.

## Debugging

Debug from evidence rather than guesses.

Recommended sequence:

1. reproduce the failure;
2. preserve the exact error or unexpected output;
3. reduce the failing case where practical;
4. inspect traceback, logs, assertions, or debugger state;
5. form a testable hypothesis;
6. have the human apply the smallest candidate fix;
7. rerun the focused reproducer;
8. run regression tests;
9. preserve useful failure evidence when it contributes to project knowledge.

For performance defects, use measurements or profiling rather than intuition alone.

## Research Changes

Research code must preserve the distinction between measurement and claim.

Record immutable inputs, relevant hashes, configuration, controls, seeds, outputs, limitations, and reproduction commands.

Discovery data should not silently become holdout data.

Failed experiments are useful evidence and should not be rewritten as successes.

## Benchmarking

Compare like workloads.

Record the model, input, hardware, software version, parameters, timing method, repetitions, and resource conditions that materially affect the result.

Do not describe an optimization as superior solely because it is faster. Correctness, fidelity, memory use, and relevant workload behavior must also be considered.

## Documentation

Write documentation so a human who did not create the feature can understand it.

Prefer:

- plain language before specialized terminology;
- examples before implementation detail;
- explicit status and limitations;
- reproducible commands;
- links to canonical evidence rather than duplicated claims.

Define project-specific terms consistently.

## Commit Discipline

Before committing, inspect the diff and repository status.

```bash
git diff --check
git status --short
git diff --stat
```

A commit should represent one understandable logical change whenever practical.

## Exact-Once Research Closure and Successor Gates

When exact-once research produces authoritative evidence:

1. Treat the namespace as permanently spent.
2. Never rerun, repair, regenerate, or replace its scientific evidence.
3. Freeze protocol, runner, slot, result, verdict, hashes, and claim boundary.
4. Synchronize human docs, AI guardrails, roadmap, and operator workflow.
5. State explicitly what the experiment proves and does not prove.
6. Give every successor experiment a new preregistration and authority boundary.
7. Keep scientific execution separate from documentation, Git work, and publication.
8. Preserve negative evidence and audit corrections as provenance.
9. Use publication-safe branches when large scientific artifacts block ordinary remote publication.
10. Verify the live remote evidence after publication.

For Q2 V1.4, query-to-PK selection passed within its frozen scope. The next gate is 6D-Q3 attach/detach ownership and cleanup semantics. Phase 6E remains not entered.

## MAF Phase 6B Best Practices

When changing Phase 6B MAF infrastructure:

1. Preserve logical identity. Never synthesize or rewrite canonical PKs from paths, ordering, offsets, or filenames.
2. Keep authority separate from caches. The active-generation record and immutable descriptor remain authority; resident indexes are derived.
3. Validate before publication. Build and validate a complete replacement snapshot before making it visible.
4. Preserve the prior valid snapshot on failed refresh. Never publish partial resident state.
5. Treat activation and rollback as freshness boundaries. A snapshot for the previous active generation becomes stale.
6. Revalidate physical evidence after rollback or same-generation refresh. Historical validity is not enough.
7. Keep physical paths out of logical identity. Relocation may change runtime paths without changing PKs or descriptor evidence.
8. Keep successful resident lookup free of JSON parsing, manifest scanning, filesystem discovery, and linear descriptor scans.
9. Do not add source-GGUF dependency to resident directory construction or lookup.
10. Do not select SQLite, mmap, MAFDB, LMDB, RocksDB, or another production storage engine without separate measured evidence.
11. Preserve failed and negative evidence. A failed validation is research evidence, not disposable noise.
12. Distinguish implementation targets from validated performance. Average O(1) resident lookup is not a benchmark claim until measured.
13. Do not merge Segment Reader, inference, tensor computation, or Phase 6C responsibilities into Resident PK Directory V1.
14. Freeze validation protocols and runners before first execution and preserve exact-once evidence boundaries.
