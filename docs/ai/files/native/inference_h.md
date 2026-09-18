# native/include/openmind/inference.h

## Purpose

Defines the public C++ interface for the OpenMind native inference layer.

This header separates consumers of the inference engine from the implementation in native/src/inference.cpp.

## Responsibilities

- Define inference configuration.
- Define inference results.
- Define the InferenceEngine interface.
- Define persistent Session behavior.
- Define session capacity and sequence management interfaces.
- Expose timing and runtime information needed by callers.

## InferenceEngine

InferenceEngine represents ownership of the native llama.cpp model and runtime.

Conceptually:

InferenceEngine -> model -> llama context -> inference operations

It supports both stateless inference and persistent session-based inference.

## Stateless Inference

Stateless generation is intended for independent requests where previous conversational KV-cache state is not required.

Conceptual operation:

generate(prompt) -> InferenceResult

## Persistent Sessions

Session provides persistent conversational state backed by an independent llama sequence ID.

Conceptual operation:

Session -> sequence ID -> KV-cache state -> repeated requests

## Session Isolation

Multiple sessions must maintain independent sequence state.

The implementation uses sequence IDs to separate session memory within the shared llama context.

## Concurrency

The current native implementation protects shared llama runtime state with a mutex.

This means session identity is independent, but native context operations are serialized until explicit concurrent execution semantics are established.
