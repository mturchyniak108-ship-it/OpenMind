# native/src/inference_test.cpp

## Purpose

Provides the native OpenMind inference integration and regression test suite.

## Architectural Role

This test validates the public OpenMind inference API against a real llama.cpp model rather than testing only isolated helper functions.

## Responsibilities

- Verify native model loading.
- Verify stateless inference.
- Verify persistent sessions.
- Verify session persistence.
- Verify session isolation.
- Verify session reset.
- Verify session capacity limits.
- Verify sequence-slot reuse.
- Verify RAII cleanup.
- Verify concurrent session requests.
- Verify session reuse after concurrent requests.

## Concurrency Regression Test

The test creates multiple sessions and submits requests from separate C++ threads.

The expected invariant is:

multiple logical sessions -> independent sequence state -> serialized shared native runtime access -> valid results

The test specifically guards against corruption caused by concurrent access to the shared llama context, sampler, or KV-cache.

## Model Configuration

CTest supplies the model path through the OpenMind test configuration.

The test should be run against a real GGUF model when validating native runtime behavior.

## Running

From the repository root:

ctest --test-dir native/build --output-on-failure

## Failure Interpretation

Failures should be classified before modifying implementation code.

Model loading failure may indicate an invalid model path or incompatible GGUF.

Inference failure may indicate llama.cpp, backend, memory, or OpenMind integration problems.

Session isolation failure indicates a serious KV-cache or sequence-management regression.

Concurrency failure indicates a possible shared-runtime synchronization regression.

## Agent Guidance

When changing `native/src/inference.cpp`, inspect and extend this test when behavior changes.

Do not remove a regression test simply because it exposes a synchronization or lifecycle problem.

The test is part of the native architecture contract.

## Required Validation

After native inference changes:

git diff --check
cmake --build native/build -j2
ctest --test-dir native/build --output-on-failure
