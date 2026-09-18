# Native Inference File Documentation

## Purpose

The native directory contains the OpenMind-owned C++ inference layer built on top of llama.cpp.

This layer owns model/runtime configuration, inference requests, persistent sessions, session sequence allocation, KV-cache lifecycle, concurrency protection, and native regression testing.

## native/CMakeLists.txt

### Purpose

Defines the native OpenMind CMake build, inference library, test executable, benchmark executable, llama.cpp include/library integration, and threading dependency.

### Use

Configure and build from the native build directory using CMake. The exact model/runtime configuration is supplied through the existing project configuration and test environment.

### Important Invariant

The native inference target must link the threading implementation required by std::mutex and related concurrency primitives.

## native/include/openmind/inference.h

### Purpose

Defines the public C++ interface for OpenMind native inference.

### Primary Responsibilities

- InferenceEngine configuration and lifecycle
- Stateless generation
- Persistent Session creation and lifecycle
- Session request and reset operations
- Session capacity management
- Inference result and metric structures

### Architectural Role

This header is the boundary between OpenMind application code and the native llama.cpp inference implementation.

Public API changes should be treated as architectural changes and accompanied by tests and documentation updates.

## native/src/inference.cpp

### Purpose

Implements the OpenMind native inference engine and persistent session runtime.

### Primary Responsibilities

- Load and initialize llama.cpp models and contexts
- Configure inference runtime
- Tokenize prompts
- Execute llama.cpp decoding
- Generate responses
- Track inference metrics
- Maintain persistent session KV-cache state
- Allocate and release llama sequence IDs
- Reset session state
- Protect shared native runtime state

### Concurrency Model

The underlying llama context and runtime are shared. OpenMind therefore serializes complete native inference transactions with the engine inference mutex.

Independent sessions use independent llama sequence IDs, but sequence isolation does not imply that the underlying context is safe for simultaneous mutation.

### Important Invariants

- Stateless generate requests clear prior memory state.
- Persistent sessions preserve their own sequence state.
- Session sequence IDs must not overlap active sessions.
- Session destruction must release its sequence state safely.
- Shared llama runtime state must not be concurrently mutated.
- Prompt sizes must respect configured context and batch capacity.

### Safe Modification Rule

Changes involving llama context access, memory, sequence IDs, samplers, loading, or session lifecycle require regression testing for both sequential and concurrent behavior.

## native/src/inference_test.cpp

### Purpose

Native integration and regression test executable.

### Verified Areas

- Model loading
- Stateless generation
- Persistent session behavior
- Session isolation
- Session reset
- Session capacity
- Sequence-slot reuse
- RAII cleanup
- Concurrent session requests
- Post-concurrency session reuse

### Usage

Run through CTest after building the native targets.

## native/openmind_llama_smoke.cpp

### Purpose

Small native smoke-test/probe used to verify direct llama.cpp integration and basic model execution independently of the higher-level inference API.

### Architectural Role

Useful for isolating llama.cpp/runtime problems from OpenMind inference-layer problems.

## Native Testing Rule

After changing native inference behavior:

1. Rebuild the native targets.
2. Run the native CTest suite.
3. Run git diff --check.
4. Inspect failures before changing additional code.

The native implementation is considered verified only when the relevant regression tests pass.
