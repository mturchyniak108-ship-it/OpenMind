"""
OpenMind production holdout V2.

Builds a canonical 12-component representation for every model layer
from q8_parameter_field_v4_1.json.

Representation:
    layer -> component -> stats.rms

No fitting.
No threshold discovery.
No use of downstream geometry/phase outputs.

This is a structural representation-consistency protocol.
It is NOT an unseen-prompt generalization benchmark.
"""

from pathlib import Path
import json
import math

ROOT = Path(__file__).resolve().parents[2]

ART = ROOT / "experiments" / "model_fractal"

PARAMETER_FILE = ART / "q8_parameter_field_v4_1.json"
OUT = ROOT / "results" / "production_holdout_v2.json"


def finite(x):
    return isinstance(x, (int, float)) and math.isfinite(float(x))


def cosine(a, b):
    if len(a) != len(b):
        raise ValueError(
            f"Vector length mismatch: {len(a)} != {len(b)}"
        )

    aa = math.sqrt(sum(x * x for x in a))
    bb = math.sqrt(sum(x * x for x in b))

    if aa == 0.0 or bb == 0.0:
        return None

    return sum(x * y for x, y in zip(a, b)) / (aa * bb)


data = json.loads(PARAMETER_FILE.read_text())

components = data["components"]
layers = data["layers"]

expected_components = 12

if len(components) != expected_components:
    raise RuntimeError(
        f"Expected {expected_components} components, "
        f"found {len(components)}"
    )


# ----------------------------------------------------------------------
# Canonical layer representation
# ----------------------------------------------------------------------

layer_vectors = {}

for layer_id in sorted(layers, key=lambda x: int(x)):
    layer = layers[layer_id]

    vector = []

    for component in components:

        if component not in layer:
            raise RuntimeError(
                f"Layer {layer_id} missing component {component!r}"
            )

        record = layer[component]

        stats = record.get("stats")

        if not isinstance(stats, dict):
            raise RuntimeError(
                f"Layer {layer_id}, component {component!r} "
                f"has no stats dictionary"
            )

        value = stats.get("rms")

        if not finite(value):
            raise RuntimeError(
                f"Layer {layer_id}, component {component!r} "
                f"has invalid stats.rms={value!r}"
            )

        vector.append(float(value))

    if len(vector) != expected_components:
        raise RuntimeError(
            f"Layer {layer_id} has {len(vector)} values; "
            f"expected {expected_components}"
        )

    layer_vectors[int(layer_id)] = vector


# ----------------------------------------------------------------------
# Adjacent-layer representation consistency
# ----------------------------------------------------------------------

layer_ids = sorted(layer_vectors)

adjacent = {}

for a, b in zip(layer_ids[:-1], layer_ids[1:]):
    adjacent[f"{a}__{b}"] = cosine(
        layer_vectors[a],
        layer_vectors[b],
    )


# ----------------------------------------------------------------------
# Summary statistics
# ----------------------------------------------------------------------

valid = [
    v for v in adjacent.values()
    if v is not None
]

if valid:
    mean_cosine = sum(valid) / len(valid)
    min_cosine = min(valid)
    max_cosine = max(valid)
else:
    mean_cosine = None
    min_cosine = None
    max_cosine = None


report = {
    "protocol": "production_holdout_v2",
    "status": "BASELINE_ONLY",
    "warning": (
        "This is a structural representation-consistency baseline, "
        "not an unseen-prompt generalization test."
    ),

    "source": str(PARAMETER_FILE),

    "representation": {
        "method": "per-layer component stats.rms",
        "components": components,
        "component_count": len(components),
        "layer_count": len(layer_vectors),
        "dimension_per_layer": len(components),
        "total_layer_values": (
            len(layer_vectors) * len(components)
        ),
    },

    "layers": {
        str(k): v
        for k, v in layer_vectors.items()
    },

    "adjacent_layer_cosine": adjacent,

    "summary": {
        "count": len(valid),
        "mean": mean_cosine,
        "min": min_cosine,
        "max": max_cosine,
    },
}


OUT.write_text(json.dumps(report, indent=2))


print("=" * 78)
print(" OPENMIND PRODUCTION HOLDOUT V2")
print("=" * 78)
print()

print("STATUS: BASELINE ONLY")
print()

print("REPRESENTATION")
print("-" * 78)
print(f"layers              : {len(layer_vectors)}")
print(f"components/layer    : {len(components)}")
print(f"total values        : {len(layer_vectors) * len(components)}")
print()

print("COMPONENTS")
print("-" * 78)

for i, component in enumerate(components):
    print(f"{i:02d}  {component}")

print()

print("ADJACENT LAYER COSINE")
print("-" * 78)

for key, value in adjacent.items():
    print(f"{key:<12} {value:.9f}")

print()

print("SUMMARY")
print("-" * 78)
print(f"count               : {len(valid)}")
print(f"mean                : {mean_cosine:.9f}")
print(f"min                 : {min_cosine:.9f}")
print(f"max                 : {max_cosine:.9f}")

print()
print(f"Saved: {OUT}")
