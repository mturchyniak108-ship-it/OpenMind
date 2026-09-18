# vulkan/

## Purpose

Contains OpenMind Vulkan capability-probing infrastructure.

The Vulkan layer determines whether the target environment can provide the GPU acceleration required by the native llama.cpp runtime.

## Files

### probe.sh

Runs Vulkan capability discovery for the current environment.

Use it before diagnosing GPU inference failures or establishing a new hardware baseline.

## Architectural Role

Vulkan is a hardware capability layer, not the inference engine itself.

The intended relationship is:

```text
OpenMind
   |
   v
Native inference
   |
   v
llama.cpp
   |
   v
Vulkan backend
   |
   v
GPU / Vulkan driver
```

## Current Target

The current mobile inference target is the Samsung Galaxy S26 Ultra using the Adreno 840 GPU with the Vulkan backend and Mesa Turnip driver.

The repository benchmark files contain the validated performance measurements.

## Agent Usage

Run the Vulkan probe when:

- Adding or changing GPU execution code.
- Porting OpenMind to another device.
- Changing llama.cpp Vulkan configuration.
- Investigating GPU initialization failures.
- Establishing a new performance baseline.

Do not infer GPU capability solely from the device name.

Use the actual probe results.

## Relationship to Preflight

Preflight establishes general system capabilities.

The Vulkan probe establishes GPU-specific capabilities.

These should be treated as complementary discovery layers.

```text
preflight/
   |
   +--> CPU
   +--> RAM
   +--> storage
   +--> tools
   +--> packages

vulkan/
   |
   +--> Vulkan API
   +--> GPU
   +--> driver
   +--> device capabilities
```

## Knowledge-System Relevance

Future embedding, vector-index, and Truth Graph workloads may be split between devices according to hardware capability.

The Vivobook can perform heavier graph/index compilation while the S26 Ultra remains optimized for interactive local inference.

Vulkan capability should therefore be considered when deciding which workloads remain on-device.

## Agent Rule

Do not modify upstream llama.cpp Vulkan implementation from the OpenMind Vulkan probe directory.

OpenMind-specific Vulkan detection belongs here; upstream Vulkan execution belongs to llama.cpp.
