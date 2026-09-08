# Getting Started with OpenMind

<!-- OPENMIND:CURRENT-WORK-LINK:START -->
Current scientific work: [`../research/CURRENT_WORK.md`](../research/CURRENT_WORK.md).
<!-- OPENMIND:CURRENT-WORK-LINK:END -->

## What OpenMind Is

OpenMind is a local-first AI systems project.

It combines several related areas:

- native local language-model inference;
- evidence and provenance tracking;
- truth and relationship graphs;
- reproducible model-analysis research;
- representation experiments;
- experimental MAF and Lodgepole structures.

You do not need to understand every research area to use or contribute to the project.

## Project Status

OpenMind contains both implemented capabilities and active research.

These are intentionally kept separate.

- `canonical` means implemented behavior supported by source code and appropriate tests.
- `validated_research` means measured research evidence that has completed its stated validation requirements.
- `lab_candidate` means active experimental work.
- `historical` means superseded work retained for provenance or methodology.

Do not assume that an experiment or roadmap item is already a production feature.

## Recommended Reading Order

For a first visit:

1. Read the repository `README.md`.
2. Read `docs/README.md` for the documentation map.
3. Read `docs/getting-started/GLOSSARY.md` when unfamiliar terminology appears.
4. Read `docs/architecture/ARCHITECTURE.md` for the system structure.
5. Developers should read `docs/development/BEST_PRACTICES.md`.
6. Researchers should read `docs/labs/README.md` and the experiment workflow.

## Human and AI Collaboration

OpenMind is developed by human contributors.

AI systems may work alongside people as engineering collaborators by analyzing code, proposing changes, helping debug failures, designing tests, reviewing results, and assisting with documentation.

Only human contributors apply source-code changes and decide what enters the repository.

## Repository Orientation

Important top-level areas include:

- `openmind/` — Python implementation and canonical project logic;
- `native/` — native C++ inference integration;
- `tests/` — Python test suite;
- `benchmarks/` — preserved performance evidence;
- `experiments/` — experimental and research work;
- `results/` — research and validation outputs;
- `docs/` — human and AI documentation;
- `preflight/` — environment and resource inspection;
- `vulkan/` — Vulkan-related probing;
- `llama.cpp/` — external inference dependency.

The presence of a file under `experiments/` does not make that behavior canonical.

## Basic Development Checks

Python changes commonly begin with:

```bash
python -m compileall -q .
git diff --check
pytest -q
```

Run narrower tests first when working on a specific component.

Native C++ changes should use the appropriate CMake build and CTest targets.

See `docs/development/TESTING.md` and `docs/development/BEST_PRACTICES.md` before making substantive changes.

## Research Work

Research should begin with a question, not a desired conclusion.

A strong OpenMind experiment records:

- the question;
- immutable inputs;
- model and artifact hashes where relevant;
- configuration;
- reproduction command;
- baseline or control;
- result artifact;
- limitations;
- interpretation boundary.

Discovery data and validation data should remain distinct where the experiment requires a holdout.

## Licenses

OpenMind software source code is licensed under Apache License 2.0.

Original OpenMind research data and results are licensed under CC BY 4.0 only where explicitly marked.

Third-party software, models, and datasets retain their own applicable licenses.

See `LICENSE`, `RESEARCH_DATA_LICENSE.md`, and `THIRD_PARTY_LICENSES.md`.

## Where to Go Next

- Architecture: `docs/architecture/`
- Development: `docs/development/`
- Experiments: `docs/experiments/`
- Active research: `docs/labs/README.md`
- Provenance: `docs/data/`
- AI collaboration: `AGENTS.md` and `docs/ai/`
