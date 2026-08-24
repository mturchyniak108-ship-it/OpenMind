"""
OpenMind Production Holdout V3

Leave-one-layer-out predictive test.

For each interior layer L:
    prediction(L) = mean(L-1, L+1)

The target layer is never used to construct its prediction.

Metrics:
    cosine similarity
    normalized RMSE

Baselines:
    nearest-left layer
    nearest-right layer
    neighbor interpolation

This tests whether the canonical parameter field has
predictable local structure.

It is NOT an unseen-prompt generalization test.
"""

from pathlib import Path
import json
import math

ROOT = Path(__file__).resolve().parents[2]

PARAMETER_FILE = (
    ROOT / "experiments/model_fractal/q8_parameter_field_v4_1.json"
)

OUT = ROOT / "results/production_holdout_v3.json"


def finite(x):
    return isinstance(x, (int, float)) and math.isfinite(float(x))


def cosine(a, b):
    aa = math.sqrt(sum(x * x for x in a))
    bb = math.sqrt(sum(x * x for x in b))

    if aa == 0.0 or bb == 0.0:
        return None

    return sum(x * y for x, y in zip(a, b)) / (aa * bb)


def rmse(a, b):
    return math.sqrt(
        sum((x - y) ** 2 for x, y in zip(a, b))
        / len(a)
    )


def normalized_rmse(pred, actual):
    denom = math.sqrt(
        sum(x * x for x in actual) / len(actual)
    )

    if denom == 0.0:
        return None

    return rmse(pred, actual) / denom


data = json.loads(PARAMETER_FILE.read_text())

components = data["components"]
layers = data["layers"]

vectors = {}

for layer_id in sorted(layers, key=lambda x: int(x)):
    layer = layers[layer_id]
    vector = []

    for component in components:
        value = layer[component]["stats"]["rms"]

        if not finite(value):
            raise RuntimeError(
                f"Invalid RMS at layer {layer_id}, "
                f"component {component}"
            )

        vector.append(float(value))

    vectors[int(layer_id)] = vector


layer_ids = sorted(vectors)

results = {}

for i in range(1, len(layer_ids) - 1):

    layer = layer_ids[i]

    left_id = layer_ids[i - 1]
    right_id = layer_ids[i + 1]

    actual = vectors[layer]
    left = vectors[left_id]
    right = vectors[right_id]

    # Neighbor interpolation.
    prediction = [
        (a + b) / 2.0
        for a, b in zip(left, right)
    ]

    results[str(layer)] = {
        "left_layer": left_id,
        "right_layer": right_id,

        "cosine_left": cosine(actual, left),
        "cosine_right": cosine(actual, right),
        "cosine_prediction": cosine(actual, prediction),

        "nrmse_left": normalized_rmse(left, actual),
        "nrmse_right": normalized_rmse(right, actual),
        "nrmse_prediction": normalized_rmse(
            prediction,
            actual,
        ),
    }


def mean_metric(name):
    values = [
        r[name]
        for r in results.values()
        if r[name] is not None
    ]

    return sum(values) / len(values) if values else None


summary = {
    "layers_tested": len(results),

    "mean_cosine_left": mean_metric(
        "cosine_left"
    ),

    "mean_cosine_right": mean_metric(
        "cosine_right"
    ),

    "mean_cosine_prediction": mean_metric(
        "cosine_prediction"
    ),

    "mean_nrmse_left": mean_metric(
        "nrmse_left"
    ),

    "mean_nrmse_right": mean_metric(
        "nrmse_right"
    ),

    "mean_nrmse_prediction": mean_metric(
        "nrmse_prediction"
    ),
}


report = {
    "protocol": "production_holdout_v3",
    "status": "PREDICTIVE_BASELINE",
    "warning": (
        "This is a layer-level structural prediction test. "
        "It is not an unseen-prompt generalization test."
    ),

    "representation": {
        "source": str(PARAMETER_FILE),
        "method": "stats.rms",
        "component_count": len(components),
        "layer_count": len(vectors),
        "dimension": len(components),
    },

    "method": {
        "prediction": "mean(previous_layer, next_layer)",
        "target_excluded": True,
        "fitting": False,
        "threshold_discovery": False,
    },

    "results": results,
    "summary": summary,
}


OUT.write_text(json.dumps(report, indent=2))

print("=" * 78)
print(" OPENMIND PRODUCTION HOLDOUT V3")
print("=" * 78)
print()

print("STATUS: PREDICTIVE BASELINE")
print()

print("REPRESENTATION")
print("-" * 78)
print(f"layers              : {len(vectors)}")
print(f"components          : {len(components)}")
print(f"target layers       : {len(results)}")
print()

print("SUMMARY")
print("-" * 78)

for k, v in summary.items():
    if isinstance(v, float):
        print(f"{k:<30} {v:.9f}")
    else:
        print(f"{k:<30} {v}")

print()

print("PER-LAYER RESULTS")
print("-" * 78)
print(
    f"{'layer':>5} "
    f"{'left':>10} "
    f"{'right':>10} "
    f"{'interp':>10} "
    f"{'NRMSE':>10}"
)

for layer, r in results.items():
    print(
        f"{layer:>5} "
        f"{r['cosine_left']:>10.6f} "
        f"{r['cosine_right']:>10.6f} "
        f"{r['cosine_prediction']:>10.6f} "
        f"{r['nrmse_prediction']:>10.6f}"
    )

print()
print(f"Saved: {OUT}")
