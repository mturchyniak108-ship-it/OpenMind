# native/src/inference.cpp

## Purpose

Implements the OpenMind native inference runtime.

This is the primary C++ integration layer between OpenMind and the upstream llama.cpp inference engine.

## Responsibilities

- Own the llama model and context.
- Initialize the configured llama backend.
- Load GGUF models.
- Execute stateless inference.
- Execute persistent session inference.
- Manage llama sequence IDs.
- Manage session lifecycle.
- Maintain session KV-cache state.
- Protect shared native inference state from concurrent access.

## Main Components

### InferenceEngine

Owns the native inference runtime.

Primary operations:

- load()
- generate(prompt)
- generate_session(prompt, seq_id, sampler)
- loaded()
- session_context_size()
- allocate_session_seq_id()
- release_session_seq_id()

### Session

Represents persistent conversational inference.

A Session owns an independent llama sequence ID and sampler while sharing the parent engine context.

Persistent sessions allow KV-cache state to remain available between requests.

## Stateless Generation

InferenceEngine::generate() represents an independent request.

The request clears previous llama memory before processing the new prompt.

This prevents conversational state from leaking between independent requests.

## Persistent Session Generation

generate_session() uses a caller-provided llama sequence ID.

Example session layout:

- Session A -> sequence 0
- Session B -> sequence 1
- Session C -> sequence 2
- Session D -> sequence 3

The llama context remains shared while sequence IDs isolate session KV-cache state.

## Concurrency Model

The native runtime currently serializes access to shared llama state with inference_mutex.

The mutex protects model initialization, inference, session operations, sequence allocation, sequence release, sampler cloning, reset operations, and session destruction.

This provides correctness and prevents concurrent requests from corrupting shared llama context state.

It does not yet provide parallel token generation.

## Session Lifecycle

Session construction allocates a sequence ID and clones the engine sampler.

Session reset removes the session sequence KV-cache state.

Session destruction removes the sequence state and returns the sequence ID to the engine free pool.

RAII is used so native resources are reclaimed when a Session leaves scope.

## Sequence Isolation

Each active Session must have a unique sequence ID.

Sequence state must never be shared accidentally between independent sessions.

Released sequence IDs may be reused after the associated session has been destroyed.

## Context Safety

Prompt token counts are checked before llama_decode() is called.

Requests exceeding the configured context or batch capacity are rejected instead of allowing llama.cpp assertions to terminate the process.

## Testing

The implementation is exercised by native/src/inference_test.cpp.

Important tested behaviors include:

- Model loading
- Stateless inference
- Persistent session inference
- Session persistence
- Session isolation
- Session reset
- Session capacity limits
- Sequence ID reuse
- RAII cleanup
- Concurrent session requests
- Post-concurrency session reuse

The native test suite is executed through CTest.

Recommended validation:

cmake --build native/build -j2

ctest --test-dir native/build --output-on-failure

## Agent Usage

AI agents modifying this file should inspect inference.h and inference_test.cpp before making changes.

Changes to session behavior must include regression tests.

Changes involving shared llama context state must preserve the inference mutex unless a stronger concurrency architecture replaces it.

Do not assume llama context operations are independently safe merely because Sessions use different sequence IDs.

## Architectural Boundary

This file is responsible for native inference execution and session state.

Knowledge retrieval, TruthNode storage, vector indexing, heuristic path compilation, and language-independent knowledge mapping belong to higher OpenMind architecture layers and should not be embedded directly into the inference engine.

## Related Files

- native/include/openmind/inference.h — public inference API
- native/src/inference_test.cpp — native regression tests
- native/CMakeLists.txt — native build configuration
- benchmarks/ — inference performance evidence
- ROADMAP.md — future Truth Graph, vector index, heuristic mapping, and Vivobook compiler architecture
