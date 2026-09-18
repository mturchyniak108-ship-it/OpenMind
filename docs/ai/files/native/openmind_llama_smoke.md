# native/openmind_llama_smoke.cpp

## Purpose

Provides a minimal native smoke test for the llama.cpp integration used by OpenMind.

## Architectural Role

This test sits below the OpenMind inference API.

It helps determine whether the underlying llama.cpp model loading and inference runtime work independently of higher-level OpenMind session and knowledge features.

## Responsibilities

- Initialize llama.cpp.
- Load a configured GGUF model.
- Tokenize a prompt.
- Execute native model evaluation.
- Verify that native inference can produce output.
- Exercise the low-level runtime independently of OpenMind session logic.

## Why It Exists

When native inference fails, agents need to distinguish an upstream runtime problem from an OpenMind integration problem.

The smoke test provides that boundary.

## Diagnostic Interpretation

If the smoke test fails, investigate llama.cpp, model compatibility, backend configuration, Vulkan, or runtime initialization.

If the smoke test passes but OpenMind inference fails, investigate the OpenMind native integration.

## Relationship To llama.cpp

OpenMind does not replace llama.cpp.

The smoke test verifies the specific llama.cpp integration that OpenMind depends upon.

Upstream llama.cpp behavior should be treated as an external dependency.

## Relationship To Vulkan

The smoke test can help establish whether the configured llama.cpp build can execute using the available hardware backend.

Backend diagnostics should be performed with `vulkan/probe.sh` before drawing conclusions from failures.

## Agent Guidance

Do not add OpenMind-specific semantic retrieval, Truth Graph, or heuristic mapping logic to this smoke test.

Keep it focused on validating the low-level inference dependency.

Changes to the smoke test should remain small and directly related to runtime validation.
