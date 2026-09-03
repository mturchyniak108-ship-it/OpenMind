"""
OpenMind Production Holdout V5

Leak-free masked-layer prediction.

For each interior layer:
    - hide the target layer
    - calculate component normalization using all NON-TARGET layers
    - predict target from:
        1. left neighbor
        2. right neighbor
        3. midpoint interpolation
        4. non-target component mean

The target is never used to calculate normalization parameters.

This is a structural predictive test, not an unseen-prompt test.
"""

from pathlib import Path
import json
import math
import statistics

ROOT = Path(__file__).resolve().parents[2]

SOURCE = ROOT / "experiments/model_fractal/q8_parameter_field_v4_1.json"
OUT = ROOT / "results/production_holdout_v5.json"

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


def value(layer, component):
    stats = layer[component]["stats"]

    if "rms" not in stats:
        raise RuntimeError(
            f"Missing RMS: {component}"
        )

    x = float(stats["rms"])

    if not math.isfinite(x):
        raise RuntimeError(
            f"Non-finite RMS: {component}"
        )

    return x


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


data = json.loads(SOURCE.read_text())

raw_layers = data["layers"]
layer_ids = sorted(int(x) for x in raw_layers)

raw = []

for layer_id in layer_ids:
    row = [
        value(raw_layers[str(layer_id)], component)
        for component in COMPONENTS
    ]

    if len(row) != len(COMPONENTS):
        raise RuntimeError(
            f"Layer {layer_id}: expected "
            f"{len(COMPONENTS)} values"
        )

    raw.append(row)


def normalize_without_target(target_index):
    """
    Calculate mean/std for each component while excluding
    the target layer entirely.
    """

    train_rows = [
        row
        for i, row in enumerate(raw)
        if i != target_index
    ]

    means = []

    stds = []

    for component_index in range(len(COMPONENTS)):

        column = [
            row[component_index]
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

    return normalized, means, stds


results = []

for target_index in range(1, len(raw) - 1):

    target_layer = layer_ids[target_index]

    normalized, means, stds = normalize_without_target(
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
        for _ in COMPONENTS
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
            "baseline": cosine(
                target,
                baseline,
            ),
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


summary = {
    "layers_tested": len(results),

    "cosine_left": avg("cosine", "left"),
    "cosine_right": avg("cosine", "right"),
    "cosine_interpolation": avg(
        "cosine",
        "interpolation",
    ),
    "cosine_baseline": avg(
        "cosine",
        "baseline",
    ),

    "nrmse_left": avg("nrmse", "left"),
    "nrmse_right": avg("nrmse", "right"),
    "nrmse_interpolation": avg(
        "nrmse",
        "interpolation",
    ),
    "nrmse_baseline": avg(
        "nrmse",
        "baseline",
    ),
}


report = {
    "protocol": "production_holdout_v5",

    "status": "LEAK_FREE_STRUCTURAL_HOLDOUT",

    "warning": (
        "This tests layer-level structural prediction. "
        "It is not an unseen-prompt generalization test."
    ),

    "representation": {
        "layers": len(layer_ids),
        "components": len(COMPONENTS),
        "values_per_layer": len(COMPONENTS),
        "feature": "tensor RMS",
        "normalization": (
            "per-target component z-score "
            "excluding target layer"
        ),
    },

    "summary": summary,

    "components": COMPONENTS,

    "results": results,
}


OUT.write_text(
    json.dumps(
        report,
        indent=2,
    )
)


print("=" * 78)
print(" OPENMIND PRODUCTION HOLDOUT V5")
print("=" * 78)
print()
print("STATUS: LEAK-FREE STRUCTURAL HOLDOUT")
print()

print("REPRESENTATION")
print("-" * 78)
print(f"layers              : {len(layer_ids)}")
print(f"components          : {len(COMPONENTS)}")
print(f"values/layer        : {len(COMPONENTS)}")
print("feature              : tensor RMS")
print("normalization       : target-excluded component z-score")
print()

print("SUMMARY")
print("-" * 78)

for key, value_ in summary.items():

    if isinstance(value_, float):
        print(
            f"{key:<35} "
            f"{value_:.9f}"
        )
    else:
        print(
            f"{key:<35} "
            f"{value_}"
        )

print()

print("PER-LAYER")
print("-" * 78)

print(
    f"{'layer':>5} "
    f"{'left':>9} "
    f"{'right':>9} "
    f"{'interp':>9} "
    f"{'base':>9} "
    f"{'NRMSE':>9}"
)

for r in results:

    baseline_cos = r["cosine"]["baseline"]

    baseline_text = (
        f"{baseline_cos:9.4f}"
        if baseline_cos is not None
        else f"{'N/A':>9}"
    )

    print(
        f"{r['layer']:5d} "
        f"{r['cosine']['left']:9.4f} "
        f"{r['cosine']['right']:9.4f} "
        f"{r['cosine']['interpolation']:9.4f} "
        f"{baseline_text} "
        f"{r['nrmse']['interpolation']:9.4f}"
    )

print()
print(f"Saved: {OUT}")
