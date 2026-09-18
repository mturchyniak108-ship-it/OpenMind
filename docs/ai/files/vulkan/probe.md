
## Modification Rules

- Preserve diagnostic transparency.
- Do not hard-code a GPU unless device-specific behavior is intentional.
- Keep probing separate from inference execution.
- Document new backend checks.
- Re-run native smoke tests after meaningful backend changes.
- Re-run benchmarks when backend configuration changes.

## Failure Interpretation

If the probe fails, investigate the Vulkan environment before changing OpenMind inference code.

If the probe succeeds but the smoke test fails, investigate llama.cpp configuration, model compatibility, or runtime initialization.

If the smoke test succeeds but OpenMind inference fails, investigate the OpenMind native integration.

If inference succeeds but performance changes, compare the benchmark environment and configuration before changing algorithms.

## Future Role

The Vulkan probe remains an environment diagnostic even after the Truth Graph, specialized vector index, and compiled heuristic mapping system are implemented.

Knowledge representation must remain independent of the hardware backend.
