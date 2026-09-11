# Installing and Building MAF

## Scope

This document describes the current MAF development environment, dependencies, build requirements, and validation workflow.

MAF is under active development. This is a developer build guide rather than a finalized end-user installer.

Requirements and observed development versions are deliberately kept separate.

## Project Requirements

Requirements declared by the repository are authoritative for the package contract.

Current declared requirements are:

| Component | Requirement | Purpose |
| --- | --- | --- |
| Python | >= 3.10 | Python implementation and research tooling |
| setuptools | >= 61.0 | Python build backend requirement |
| wheel | required by build system | Python package building |
| pytest | >= 7.0, optional `test` extra | Python testing |
| CMake | >= 3.22 | Native build configuration |
| C++ compiler | C++17 support | Native inference implementation |
| Threads | required | Native threading support |
| llama.cpp | compatible source/build | GGUF inference backend |

The core Python project currently declares no mandatory runtime package dependencies.

## Verified Termux Development Environment

The following versions describe a development environment on which MAF is currently being developed and tested.

They are reproducibility information, not minimum version requirements unless explicitly stated above.

| Component | Verified version |
| --- | --- |
| MAF | 0.1.0 |
| Python | 3.13.13 |
| pip | 26.1.2 |
| Git | 2.54.0 |
| CMake | 4.3.4 |
| Ninja | 1.13.2 |
| Clang | 21.1.8 |
| Clang++ | 21.1.8 |
| LLVM | 21.1.8 |
| pytest | 9.1.1 |
| NumPy | 2.4.4 |
| Vulkan tools | 1.4.354 |
| Mesa Freedreno Vulkan ICD | 26.0.6-1 |

The Termux package versions observed for several components are:

```text
python                     3.13.13-1
git                        2.54.0
cmake                      4.3.4
ninja                      1.13.2
clang                      21.1.8-2
libllvm                    21.1.8-2
vulkan-loader              0.0.3
vulkan-tools               1.4.354
mesa-vulkan-icd-freedreno  26.0.6-1
```

## Python Package State

The current Termux environment reports:

```text
pytest       9.1.1
numpy        2.4.4
setuptools   NOT INSTALLED
wheel        NOT INSTALLED
scipy        NOT INSTALLED
```

This distinction is important.

`setuptools>=61.0` and `wheel` are declared as Python build-system requirements. Their absence from the current interactive environment does not remove them from the package build contract; a compatible PEP 517 build frontend may install build requirements in an isolated build environment.

NumPy is installed in the current development environment but is not presently declared as a mandatory MAF runtime dependency.

SciPy is not installed in this recorded Termux environment and is not a declared core dependency.

Do not add packages to MAF requirements solely because they happen to be installed on a development device.

## Repository Layout Relevant to Building

The primary implementation layers are:

- `openmind/` — Python implementation;
- `native/` — native C++ integration;
- `llama.cpp/` — external inference dependency;
- `tests/` — Python tests;
- `preflight/` — environment inspection;
- `vulkan/` — Vulkan probing and diagnostics.

Run development commands from the repository root unless documentation states otherwise.

```bash
cd ~/OpenMind
```

## Python Validation

Basic Python validation commonly includes:

```bash
python -m compileall -q .
git diff --check
pytest -q
```

Run focused tests first when changing a specific component.

## Native Build Requirements

The native project is defined by `native/CMakeLists.txt`.

The current build contract requires:

- CMake 3.22 or newer;
- C++17;
- thread support;
- a compatible llama.cpp source tree;
- required llama.cpp and GGML shared libraries.

The current native configuration expects llama.cpp at:

`llama.cpp/`

and its Vulkan-enabled libraries at:

`llama.cpp/build-vulkan/bin/`

## Required llama.cpp Libraries

The current native targets link against:

- `libllama.so`;
- `libggml.so`;
- `libggml-base.so`;
- `libggml-cpu.so`;
- `libggml-vulkan.so`.

All five libraries were present in the recorded Termux development environment.

## Recorded llama.cpp Revision

The recorded development checkout uses:

```text
commit: dc72703fc69698b1ea68ece8d2dd8a96e6a4e1fe
describe: b10502-15-gdc72703fc-dirty
branch: master
```

The exact commit provides reproducibility information.

The `dirty` suffix means the recorded llama.cpp working tree contained local modifications. Results that depend on those modifications should preserve the relevant diff or otherwise identify the changed source before being treated as fully reproducible.

This revision is a verified development reference, not a declaration that MAF supports only this llama.cpp commit.

## Current Native Configuration

The recorded `native/build/CMakeCache.txt` contains:

```text
CMAKE_BUILD_TYPE=Release
CMAKE_CXX_COMPILER=/data/data/com.termux/files/usr/bin/clang++
OPENMIND_TEST_MODEL=/data/data/com.termux/files/home/models/qwen2.5-3b-q4_k_m.gguf
```

Absolute paths are environment-specific and should not be copied blindly to another device.

## Native Targets

The current CMake project defines:

- `openmind_inference` — static inference library;
- `openmind_inference_test` — native integration test;
- `openmind_inference_benchmark` — inference benchmark;
- `openmind_activation_probe` — activation capture and analysis tool.

The public native API is defined in:

`native/include/openmind/inference.h`

## Building an Existing Native Configuration

For an already configured `native/build` tree:

```bash
cmake --build native/build -j2
```

To build only the activation probe:

```bash
cmake --build native/build --target openmind_activation_probe -j2
```

## Native Tests

CTest is enabled by the native CMake project.

`openmind_inference_test` is registered with CTest when `OPENMIND_TEST_MODEL` points to a GGUF model.

For an already configured build:

```bash
ctest --test-dir native/build --output-on-failure
```

Model identity and cryptographic hash should be recorded with reproducible inference or research results.

## Vulkan

The recorded Termux environment uses the Mesa Freedreno Vulkan ICD and Vulkan tooling listed above.

Vulkan compatibility depends on the device, GPU, driver, operating environment, llama.cpp revision, and build configuration.

Use `preflight/` and `vulkan/` diagnostics when validating a new environment.

## Models

GGUF model files are external artifacts and are not automatically part of the MAF software distribution.

Models retain their applicable upstream licenses.

For reproducible work, record at minimum:

- filename;
- cryptographic hash;
- model architecture;
- quantization;
- context size;
- relevant inference configuration;
- llama.cpp revision.

## Troubleshooting Order

When a build or test fails:

1. preserve the exact error output;
2. verify required tool versions;
3. verify the llama.cpp build;
4. verify required shared libraries;
5. verify model path and compatibility;
6. reproduce the narrowest failing operation;
7. inspect logs or debugger evidence before changing code;
8. rerun relevant regression tests after a human applies a change.

AI collaborators may analyze failures and propose modifications. Human contributors apply source-code changes and decide what enters the repository.

## Distribution Status

MAF does not yet provide a finalized one-command installer or stable end-user binary distribution.

This document therefore describes the current development environment and build contract.

## Related Documentation

- `docs/getting-started/README.md` — project introduction
- `docs/getting-started/GLOSSARY.md` — terminology
- `docs/development/BEST_PRACTICES.md` — development practices
- `docs/development/TESTING.md` — testing guidance
- `docs/architecture/AUTHORITY_AND_TERMINOLOGY.md` — authority terminology
- `docs/operations/OPERATIONS.md` — operational guidance
- `THIRD_PARTY_LICENSES.md` — third-party licensing
