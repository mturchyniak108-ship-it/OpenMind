# benchmarks/

## Purpose

Contains reproducible performance records for OpenMind native inference.

Benchmark files are evidence, not implementation code.

## Architectural Role

Benchmarks establish measurable behavior for the native inference stack and provide regression baselines when the runtime, model, backend, or session architecture changes.

## Current Benchmark Categories

- Vulkan baseline inference
- Native inference performance
- Sequential request and memory reset behavior
- Persistent session inference
- Qwen model runtime characteristics

## Important Variables

Interpret benchmark results using the complete execution context:

- Device
- CPU
- GPU
- Vulkan driver
- llama.cpp build
- Model
- Quantization
- Context size
- GPU layers
- Prompt length
- Generation length
- Memory availability

## Agent Rules

Do not compare two benchmark numbers as equivalent unless their relevant runtime conditions are comparable.

Do not modify benchmark records to make performance appear better.

Create a new benchmark record when a change establishes a new meaningful baseline.

## Relationship To The Roadmap

Benchmarking eventually extends beyond inference speed.

Future measurements should include:

- Truth-node lookup latency
- Vector search latency
- Graph traversal latency
- Start-to-end path discovery
- Cycle reduction
- Compiled heuristic mapping latency
- Index size
- Memory consumption
- Cross-language retrieval accuracy
- Provenance preservation

## Knowledge Architecture

The benchmark system will eventually compare:

Conventional Vector Search
vs
OpenMind Truth-Graph Retrieval
vs
OpenMind Compiled Truth-Path Retrieval

The objective is to measure whether semantic truth paths and compiled heuristic mappings provide measurable improvements over conventional document-oriented retrieval.
