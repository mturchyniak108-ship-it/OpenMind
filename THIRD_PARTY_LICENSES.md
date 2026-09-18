# Third-Party Licensing

OpenMind builds on open-source software and may interact with third-party
models, libraries, tools, datasets, and other components.

## Policy

Third-party materials are NOT automatically relicensed under the OpenMind
Apache-2.0 license.

Each dependency or external artifact retains its applicable upstream license.

When redistributing OpenMind with third-party components, retain the
applicable copyright notices and license terms required by those projects.

## Known AI Infrastructure

### llama.cpp

OpenMind uses or experiments with llama.cpp for local LLM inference.

The llama.cpp project and its source files remain subject to their own
upstream licensing terms.

Repository:
https://github.com/ggml-org/llama.cpp

Before redistribution, consult the current upstream LICENSE and notices.

### GGUF Models

GGUF model files are model artifacts and are NOT automatically covered by
the OpenMind software license.

The applicable model license must be checked for each model.

## Research Data

Original OpenMind benchmark datasets and research results may be released
under CC BY 4.0 where explicitly marked.

Third-party datasets remain under their original terms.

## Adding Dependencies

When adding a dependency, record:

1. Project name
2. Version or commit
3. Upstream repository
4. License
5. Whether redistribution is permitted
6. Required attribution/notices
