# native/CMakeLists.txt

## Purpose

Defines the CMake build configuration for the OpenMind native C++ inference layer.

## Responsibilities

- Configure the native OpenMind project.
- Require the supported C++ language standard.
- Locate the llama.cpp dependency.
- Configure OpenMind include paths.
- Build the native inference library.
- Build native inference tests.
- Build native inference benchmarks.
- Configure CTest integration.
- Link required threading support.

## Native Library

The primary library contains the OpenMind inference implementation.

Conceptually:

OpenMind application -> openmind_inference -> llama.cpp

## Threading

The build explicitly locates the platform threading implementation through CMake Threads support.

This corresponds to the native inference mutex used to serialize shared llama runtime operations.

## Testing

CTest is used to execute the native inference integration test.

Typical workflow:

cmake configuration -> native build -> CTest -> benchmark

## Build

From the repository root, an existing configured build can be rebuilt with:

cmake --build native/build -j2

Run tests with:

ctest --test-dir native/build --output-on-failure

## Agent Guidance

Do not bypass CMake by manually compiling individual OpenMind source files unless specifically debugging a build issue.

When changing native dependencies, compiler requirements, threading behavior, or test targets, update this documentation if the build contract changes.

After meaningful native changes, run:

git diff --check
cmake --build native/build -j2
ctest --test-dir native/build --output-on-failure
