"""
OpenMind Production Holdout V6

Richer structural representation.

Each layer is represented by tensor statistics rather than
tensor RMS alone.

Protocol:
- leave one layer out
- target-excluded component normalization
- no fitting on target
- compare left, right, interpolation, and zero baseline

This remains a structural layer holdout, not an unseen-prompt test.
"""

from pathlib import Path
import json
import math
import statistics

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "experiments" / "model_fractal"
OUT = ROOT / "results" / "production_holdout_v6.json"

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

BASE_STATS = [
    "mean",
    "rms",
    "std",
    "min",
    "max",
    "abs_mean",
]

Q8_STATS = [
    "mean",
    "rms",
    "std",
    "min",
    "max",
    "abs_mean",
]


def finite(x):
    return isinstance(x, (int, float)) and math.isfinite(float(x))


def get_stats(tensor):
    """
    Extract the six ordinary tensor statistics.

    For Q8 tensors, append the six scale statistics.
    """
    stats = tensor.get("stats", {})

    values = []

    for key in BASE_STATS:
        value = stats.get(key)

        if not finite(value):
            raise RuntimeError(
                f"Missing/non-finite stats field: {key}"
            )

        values.append(float(value))

    q8 = tensor.get("q8")

    if isinstance(q8, dict):
        scale = q8.get("scale_stats")

        if isinstance(scale, dict):
            for key in Q8_STATS:
                value = scale.get(key)

                if not finite(value):
                    raise RuntimeError(
                        f"Missing/non-finite Q8 scale stat: {key}"
                    )

                values.append(float(value))

    return values


data = json.loads(SOURCE.read_text())

raw_layers = data["layers"]

layer_ids = sorted(
    int(x)
    for x in raw_layers.keys()
)

raw = []

feature_names = []

# Establish feature schema from layer 0.
for component in COMPONENTS:
    tensor = raw_layers[str(layer_ids[0])][component]

    stats = tensor.get("stats", {})
    q8 = tensor.get("q8")

    for key in BASE_STATS:
        feature_names.append(
            f"{component}__{key}"
        )

    if isinstance(q8, dict) and isinstance(
        q8.get("scale_stats"), dict
    ):
        for key in Q8_STATS:
            feature_names.append(
                f"{component}__q8_scale_{key}"
            )


for layer_id in layer_ids:
    row = []

    layer = raw_layers[str(layer_id)]

    for component in COMPONENTS:
        if component not in layer:
            raise RuntimeError(
                f"Layer {layer_id} missing component "
                f"{component}"
            )

        values = get_stats(layer[component])

        row.extend(values)

    if len(row) != len(feature_names):
        raise RuntimeError(
            f"Layer {layer_id}: got {len(row)} features, "
            f"expected {len(feature_names)}"
        )

    raw.append(row)


def normalize_without_target(target_index):
    """
    Component-wise feature z-score.

    Target layer is excluded entirely from mean/std estimation.
    """
    train_rows = [
        row
        for i, row in enumerate(raw)
        if i != target_index
    ]

    dimensions = len(raw[0])

    means = []
    stds = []

    for j in range(dimensions):
        column = [
            row[j]
            for row in train_rows
        ]

        mean = statistics.mean(column)

        variance = statistics.mean(
            (x - mean) ** 2
            for x in column
        )

        std = math.sqrt(variance)

        if std == 0:
            std = 1.0

        means.append(mean)
        stds.append(std)

    normalized = []

    for row in raw:
        normalized.append([
            (x - mean) / std
            for x, mean, std
            in zip(row, means, stds)
        ])

    return normalized


def cosine(a, b):
    aa = math.sqrt(sum(x * x for x in a))
    bb = math.sqrt(sum(x * x for x in b))

    if aa == 0 or bb == 0:
        return None

    return sum(
        x * y
        for x, y in zip(a, b)
    ) / (aa * bb)


def nrmse(target, prediction):
    mse = statistics.mean(
        (a - b) ** 2
        for a, b in zip(target, prediction)
    )

    rmse = math.sqrt(mse)

    mean_square = statistics.mean(
        x * x
        for x in target
    )

    denominator = math.sqrt(mean_square)

    if denominator == 0:
        return None

    return rmse / denominator


results = []

# Interior layers only.
for target_index in range(1, len(raw) - 1):

    target_layer = layer_ids[target_index]

    normalized = normalize_without_target(
        target_index
    )

    target = normalized[target_index]
    left = normalized[target_index - 1]
    right = normalized[target_index + 1]

    interpolation = [
        (a + b) / 2.0
        for a, b in zip(left, right)
    ]

    baseline = [
        0.0
        for _ in target
    ]

    result = {
        "layer": target_layer,

        "cosine": {
            "left": cosine(target, left),
            "right": cosine(target, right),
            "interpolation": cosine(
                target,
                interpolation,
            ),
            "baseline": None,
        },

        "nrmse": {
            "left": nrmse(target, left),
            "right": nrmse(target, right),
            "interpolation": nrmse(
                target,
                interpolation,
            ),
            "baseline": nrmse(
                target,
                baseline,
            ),
        },
    }

    results.append(result)


def avg(section, key):
    values = [
        r[section][key]
        for r in results
        if r[section][key] is not None
    ]

    if not values:
        return None

    return statistics.mean(values)


wins = 0
losses = 0
ties = 0

for r in results:
    score = r["nrmse"]["interpolation"]
    baseline = r["nrmse"]["baseline"]

    if score < baseline:
        wins += 1
    elif score > baseline:
        losses += 1
    else:
        ties += 1


report = {
    "protocol": "production_holdout_v6",

    "status": "LEAK_FREE_RICH_STRUCTURAL_HOLDOUT",

    "warning": (
        "This tests layer-level structural prediction. "
        "It is not an unseen-prompt generalization test."
    ),

    "representation": {
        "layers": len(layer_ids),
        "components": len(COMPONENTS),
        "features_per_layer": len(feature_names),
        "feature_schema": feature_names,
        "normalization": (
            "target-excluded component-wise z-score"
        ),
    },

    "summary": {
        "layers_tested": len(results),

        "cosine_left": avg(
            "cosine",
            "left",
        ),

        "cosine_right": avg(
            "cosine",
            "right",
        ),

        "cosine_interpolation": avg(
            "cosine",
            "interpolation",
        ),

        "nrmse_left": avg(
            "nrmse",
            "left",
        ),

        "nrmse_right": avg(
            "nrmse",
            "right",
        ),

        "nrmse_interpolation": avg(
            "nrmse",
            "interpolation",
        ),

        "nrmse_baseline": avg(
            "nrmse",
            "baseline",
        ),

        "wins": wins,
        "losses": losses,
        "ties": ties,
    },

    "results": results,
}


OUT.write_text(
    json.dumps(
        report,
        indent=2,
    )
)


print("=" * 78)
print(" OPENMIND PRODUCTION HOLDOUT V6")
print("=" * 78)
print()
print("STATUS: LEAK-FREE RICH STRUCTURAL HOLDOUT")
print()
print("REPRESENTATION")
print("-" * 78)
print(f"layers              : {len(layer_ids)}")
print(f"components          : {len(COMPONENTS)}")
print(f"features/layer      : {len(feature_names)}")
print("feature source      : tensor + Q8 scale statistics")
print("normalization       : target-excluded component z-score")
print()
print("SUMMARY")
print("-" * 78)

summary = report["summary"]

for key, value in summary.items():
    if value is None:
        text = "None"
    elif isinstance(value, float):
        text = f"{value:.9f}"
    else:
        text = str(value)

    print(f"{key:<30} {text}")

print()
print("PER-LAYER")
print("-" * 78)

print(
    f"{'layer':>5} "
    f"{'left':>9} "
    f"{'right':>9} "
    f"{'interp':>9} "
    f"{'NRMSE':>9} "
    f"{'win':>5}"
)

for r in results:

    score = r["nrmse"]["interpolation"]
    base = r["nrmse"]["baseline"]

    win = "YES" if score < base else "NO"

    print(
        f"{r['layer']:5d} "
        f"{r['cosine']['left']:9.4f} "
        f"{r['cosine']['right']:9.4f} "
        f"{r['cosine']['interpolation']:9.4f} "
        f"{score:9.4f} "
        f"{win:>5}"
    )

print()
print(f"Saved: {OUT}")
