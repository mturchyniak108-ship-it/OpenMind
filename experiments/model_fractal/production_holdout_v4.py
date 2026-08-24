"""
OpenMind Production Holdout V4

Leave-one-layer-out structural prediction.

For every interior layer n:
    target = representation[n]

Predict target using:
    A) left neighbor only
    B) right neighbor only
    C) bidirectional interpolation

Normalization is performed independently per component across layers
to prevent large-scale components from dominating the metric.

No target-layer statistics are used to construct the prediction.
"""

from pathlib import Path
import json
import math
import statistics

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "experiments" / "model_fractal"
OUT = ROOT / "results" / "production_holdout_v4.json"

SOURCE = ART / "q8_parameter_field_v4_1.json"

COMPONENTS = [
    "attn_k.bias",
    "attn_k.weight",
    "attn_norm.weight",
    "attn_output.weight",
    "attn_q.bias",
    "attn_q.weight",
    "attn_v.bias",
    "attn_v.weight",
    "ffn_down.weight",
    "ffn_gate.weight",
    "ffn_norm.weight",
    "ffn_up.weight",
]


def finite(x):
    return isinstance(x, (int, float)) and math.isfinite(float(x))


def component_value(layer, component):
    """
    Extract the scalar representation used by the structural pipeline.

    The source contains per-tensor statistics. We use RMS as the
    component-level scalar because it exists consistently for both
    F32 and Q8 tensors.
    """
    obj = layer[component]

    stats = obj.get("stats", {})

    if "rms" not in stats:
        raise RuntimeError(
            f"Missing rms for component {component}"
        )

    value = float(stats["rms"])

    if not math.isfinite(value):
        raise RuntimeError(
            f"Non-finite value for component {component}"
        )

    return value


data = json.loads(SOURCE.read_text())

layers_raw = data["layers"]

layer_ids = sorted(int(x) for x in layers_raw)

matrix = []

for layer_id in layer_ids:
    layer = layers_raw[str(layer_id)]

    row = [
        component_value(layer, component)
        for component in COMPONENTS
    ]

    if len(row) != len(COMPONENTS):
        raise RuntimeError(
            f"Layer {layer_id}: expected {len(COMPONENTS)} values"
        )

    matrix.append(row)


# ----------------------------------------------------------------------
# Component-wise normalization
# ----------------------------------------------------------------------

columns = list(zip(*matrix))

means = [
    statistics.mean(col)
    for col in columns
]

stds = []

for col, mean in zip(columns, means):
    variance = statistics.mean(
        (x - mean) ** 2
        for x in col
    )
    std = math.sqrt(variance)

    if std == 0:
        std = 1.0

    stds.append(std)


normalized = []

for row in matrix:
    normalized.append([
        (x - mean) / std
        for x, mean, std in zip(row, means, stds)
    ])


def cosine(a, b):
    aa = math.sqrt(sum(x * x for x in a))
    bb = math.sqrt(sum(x * x for x in b))

    if aa == 0 or bb == 0:
        return None

    return sum(x * y for x, y in zip(a, b)) / (aa * bb)


def nrmse(target, prediction):
    mse = statistics.mean(
        (a - b) ** 2
        for a, b in zip(target, prediction)
    )

    rmse = math.sqrt(mse)

    scale = math.sqrt(
        statistics.mean(x * x for x in target)
    )

    if scale == 0:
        return None

    return rmse / scale


results = []

# Interior layers only because both neighbors are required.
for i in range(1, len(normalized) - 1):

    target = normalized[i]
    left = normalized[i - 1]
    right = normalized[i + 1]

    # Predict target entirely from left.
    pred_left = left[:]

    # Predict target entirely from right.
    pred_right = right[:]

    # Equal-weight structural interpolation.
    pred_interp = [
        (a + b) / 2.0
        for a, b in zip(left, right)
    ]

    results.append({
        "layer": layer_ids[i],

        "left_cosine": cosine(target, pred_left),
        "right_cosine": cosine(target, pred_right),
        "interp_cosine": cosine(target, pred_interp),

        "left_nrmse": nrmse(target, pred_left),
        "right_nrmse": nrmse(target, pred_right),
        "interp_nrmse": nrmse(target, pred_interp),
    })


def mean(key):
    values = [
        r[key]
        for r in results
        if r[key] is not None
    ]
    return statistics.mean(values)


report = {
    "protocol": "production_holdout_v4",
    "status": "STRUCTURAL_LEAVE_ONE_LAYER_OUT",

    "representation": {
        "layers": len(layer_ids),
        "components": len(COMPONENTS),
        "values_per_layer": len(COMPONENTS),
        "normalization": "component-wise z-score across layers",
    },

    "summary": {
        "layers_tested": len(results),

        "mean_cosine_left": mean("left_cosine"),
        "mean_cosine_right": mean("right_cosine"),
        "mean_cosine_interpolation": mean("interp_cosine"),

        "mean_nrmse_left": mean("left_nrmse"),
        "mean_nrmse_right": mean("right_nrmse"),
        "mean_nrmse_interpolation": mean("interp_nrmse"),
    },

    "components": COMPONENTS,
    "results": results,
}

OUT.write_text(json.dumps(report, indent=2))

print("=" * 78)
print(" OPENMIND PRODUCTION HOLDOUT V4")
print("=" * 78)
print()
print("STATUS: STRUCTURAL LEAVE-ONE-LAYER-OUT")
print()
print("REPRESENTATION")
print("-" * 78)
print(f"layers              : {len(layer_ids)}")
print(f"components          : {len(COMPONENTS)}")
print(f"values/layer        : {len(COMPONENTS)}")
print("normalization       : component-wise z-score")
print()
print("SUMMARY")
print("-" * 78)

s = report["summary"]

for k, v in s.items():
    if isinstance(v, float):
        print(f"{k:<35} {v:.9f}")
    else:
        print(f"{k:<35} {v}")

print()
print("PER-LAYER")
print("-" * 78)
print(
    f"{'layer':>5} "
    f"{'left':>10} "
    f"{'right':>10} "
    f"{'interp':>10} "
    f"{'NRMSE':>10}"
)

for r in results:
    print(
        f"{r['layer']:5d} "
        f"{r['left_cosine']:10.6f} "
        f"{r['right_cosine']:10.6f} "
        f"{r['interp_cosine']:10.6f} "
        f"{r['interp_nrmse']:10.6f}"
    )

print()
print(f"Saved: {OUT}")
