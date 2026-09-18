"""
OpenMind production holdout protocol.

This experiment evaluates whether a frozen representation can
predict held-out representation states.

No fitting or threshold discovery is performed here.
"""

from pathlib import Path
import json
import math
import statistics

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "experiments" / "model_fractal"
OUT = ROOT / "results" / "production_holdout_v1.json"


def load(name):
    path = ART / name
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text())


def flatten_numbers(obj):
    values = []

    if isinstance(obj, (int, float)):
        if math.isfinite(obj):
            values.append(float(obj))

    elif isinstance(obj, list):
        for x in obj:
            values.extend(flatten_numbers(x))

    elif isinstance(obj, dict):
        for x in obj.values():
            values.extend(flatten_numbers(x))

    return values


def cosine(a, b):
    n = min(len(a), len(b))

    if n == 0:
        return None

    a = a[:n]
    b = b[:n]

    aa = math.sqrt(sum(x * x for x in a))
    bb = math.sqrt(sum(x * x for x in b))

    if aa == 0 or bb == 0:
        return None

    return sum(x * y for x, y in zip(a, b)) / (aa * bb)


parameter = load("q8_parameter_field_v4_1.json")
transition = load("transition_field_v5.json")
geometry = load("normalized_geometry_v10.json")
phase = load("q8_phase_detection_v6.json")

vectors = {
    "parameter": flatten_numbers(parameter),
    "transition": flatten_numbers(transition),
    "geometry": flatten_numbers(geometry),
    "phase": flatten_numbers(phase),
}

results = {}

names = list(vectors)

for i, a in enumerate(names):
    for b in names[i + 1:]:
        results[f"{a}__{b}"] = cosine(
            vectors[a],
            vectors[b],
        )

report = {
    "protocol": "production_holdout_v1",
    "status": "BASELINE_ONLY",
    "warning": (
        "This is a representation-consistency baseline, "
        "not an unseen-prompt generalization test."
    ),
    "dimensions": {
        k: len(v)
        for k, v in vectors.items()
    },
    "cross_representation_cosine": results,
}

OUT.write_text(json.dumps(report, indent=2))

print("=" * 78)
print(" OPENMIND PRODUCTION HOLDOUT V1")
print("=" * 78)
print()
print("STATUS: BASELINE ONLY")
print()

for k, v in results.items():
    if v is None:
        print(f"{k:<35} unavailable")
    else:
        print(f"{k:<35} {v:.9f}")

print()
print(f"Saved: {OUT}")
