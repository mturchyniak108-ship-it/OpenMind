"""
OPENMIND PRODUCTION HOLDOUT V7

Dual-space + directional structural prediction.

No target layer is used to calculate normalization or
directional statistics.

Compared predictors:

1. raw RMS interpolation
2. raw RMS directional prediction
3. normalized RMS interpolation
4. normalized RMS directional prediction
5. normalized rich-stat interpolation
6. normalized rich-stat directional prediction

This remains a layer-level structural holdout.
It is NOT an unseen-prompt generalization test.
"""

from pathlib import Path
import json
import math
import statistics

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "experiments" / "model_fractal"
OUT = ROOT / "results" / "production_holdout_v7.json"

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


def tensor_rms(tensor):
    stats = tensor.get("stats", {})
    value = stats.get("rms")

    if not finite(value):
        raise RuntimeError(
            f"Missing RMS for {tensor.get('name')}"
        )

    return float(value)


def rich_features(tensor):
    stats = tensor.get("stats", {})
    values = []

    for key in BASE_STATS:
        value = stats.get(key)

        if not finite(value):
            raise RuntimeError(
                f"Missing {key} for {tensor.get('name')}"
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
                        f"Missing Q8 scale {key}"
                    )

                values.append(float(value))

    return values


data = json.loads(SOURCE.read_text())
layers = data["layers"]

layer_ids = sorted(int(x) for x in layers)

raw_rms = []
rich = []

feature_names = []

for component in COMPONENTS:
    feature_names.append(
        f"{component}__rms"
    )

for component in COMPONENTS:

    tensor = layers[str(layer_ids[0])][component]

    for key in BASE_STATS:
        feature_names.append(
            f"{component}__{key}"
        )

    if isinstance(tensor.get("q8"), dict):
        scale = tensor["q8"].get("scale_stats")

        if isinstance(scale, dict):
            for key in Q8_STATS:
                feature_names.append(
                    f"{component}__q8_scale_{key}"
                )


for layer_id in layer_ids:

    layer = layers[str(layer_id)]

    rms_row = []
    rich_row = []

    for component in COMPONENTS:

        tensor = layer[component]

        rms_row.append(
            tensor_rms(tensor)
        )

        rich_row.extend(
            rich_features(tensor)
        )

    raw_rms.append(rms_row)
    rich.append(rich_row)


def zscore(rows, target_index):
    """
    Normalize columns using every layer EXCEPT target.
    """

    train = [
        row
        for i, row in enumerate(rows)
        if i != target_index
    ]

    dimensions = len(rows[0])

    means = []
    stds = []

    for j in range(dimensions):

        column = [
            row[j]
            for row in train
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

    for row in rows:

        normalized.append([
            (x - mean) / std
            for x, mean, std
            in zip(row, means, stds)
        ])

    return normalized


def cosine(a, b):

    aa = math.sqrt(
        sum(x * x for x in a)
    )

    bb = math.sqrt(
        sum(x * x for x in b)
    )

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

    scale = math.sqrt(
        statistics.mean(
            x * x
            for x in target
        )
    )

    if scale == 0:
        return None

    return rmse / scale


def interpolate(a, b):

    return [
        (x + y) / 2.0
        for x, y in zip(a, b)
    ]


def directional(left2, left1, right1, right2):
    """
    Estimate the missing point using local directional
    information on both sides.

    Each side supplies an estimate of where the trajectory
    should continue.

    left estimate:
        left1 + (left1 - left2)

    right estimate:
        right1 + (right1 - right2)

    Their midpoint is the prediction.
    """

    left_estimate = [
        b + (b - a)
        for a, b in zip(left2, left1)
    ]

    right_estimate = [
        b + (b - a)
        for a, b in zip(right1, right2)
    ]

    return [
        (a + b) / 2.0
        for a, b in zip(
            left_estimate,
            right_estimate,
        )
    ]


def evaluate(target, prediction):

    return {
        "cosine": cosine(
            target,
            prediction,
        ),
        "nrmse": nrmse(
            target,
            prediction,
        ),
    }


results = []

# Need two layers on each side for directional prediction.
for i in range(2, len(layer_ids) - 2):

    target_layer = layer_ids[i]

    rms_norm = zscore(
        raw_rms,
        i,
    )

    rich_norm = zscore(
        rich,
        i,
    )

    target_raw = raw_rms[i]
    left_raw = raw_rms[i - 1]
    right_raw = raw_rms[i + 1]

    target_rms = rms_norm[i]
    left_rms = rms_norm[i - 1]
    right_rms = rms_norm[i + 1]

    target_rich = rich_norm[i]
    left_rich = rich_norm[i - 1]
    right_rich = rich_norm[i + 1]

    raw_interp = interpolate(
        left_raw,
        right_raw,
    )

    raw_direction = directional(
        raw_rms[i - 2],
        raw_rms[i - 1],
        raw_rms[i + 1],
        raw_rms[i + 2],
    )

    rms_interp = interpolate(
        left_rms,
        right_rms,
    )

    rms_direction = directional(
        rms_norm[i - 2],
        rms_norm[i - 1],
        rms_norm[i + 1],
        rms_norm[i + 2],
    )

    rich_interp = interpolate(
        left_rich,
        right_rich,
    )

    rich_direction = directional(
        rich_norm[i - 2],
        rich_norm[i - 1],
        rich_norm[i + 1],
        rich_norm[i + 2],
    )

    predictions = {
        "raw_rms_interpolation": evaluate(
            target_raw,
            raw_interp,
        ),

        "raw_rms_directional": evaluate(
            target_raw,
            raw_direction,
        ),

        "normalized_rms_interpolation": evaluate(
            target_rms,
            rms_interp,
        ),

        "normalized_rms_directional": evaluate(
            target_rms,
            rms_direction,
        ),

        "normalized_rich_interpolation": evaluate(
            target_rich,
            rich_interp,
        ),

        "normalized_rich_directional": evaluate(
            target_rich,
            rich_direction,
        ),
    }

    results.append({
        "layer": target_layer,
        "predictions": predictions,
    })


PREDICTORS = list(
    results[0]["predictions"].keys()
)


def average(metric, predictor):

    values = [
        r["predictions"][predictor][metric]
        for r in results
        if r["predictions"][predictor][metric]
        is not None
    ]

    if not values:
        return None

    return statistics.mean(values)


wins = {
    predictor: 0
    for predictor in PREDICTORS
}

for r in results:

    scores = {
        p: r["predictions"][p]["nrmse"]
        for p in PREDICTORS
    }

    winner = min(
        scores,
        key=lambda x: scores[x]
    )

    wins[winner] += 1


summary = {}

for predictor in PREDICTORS:

    summary[predictor] = {
        "mean_cosine": average(
            "cosine",
            predictor,
        ),
        "mean_nrmse": average(
            "nrmse",
            predictor,
        ),
        "layer_wins": wins[predictor],
    }


report = {
    "protocol": "production_holdout_v7",

    "status": "LEAK_FREE_DUAL_SPACE_DIRECTIONAL",

    "warning": (
        "Structural layer prediction only. "
        "No unseen-prompt generalization is tested."
    ),

    "representation": {
        "layers": len(layer_ids),
        "components": len(COMPONENTS),
        "raw_rms_dimensions": len(raw_rms[0]),
        "rich_dimensions": len(rich[0]),
        "normalization": (
            "target-excluded z-score"
        ),
    },

    "summary": summary,

    "results": results,
}


OUT.write_text(
    json.dumps(
        report,
        indent=2,
    )
)


print("=" * 78)
print(" OPENMIND PRODUCTION HOLDOUT V7")
print("=" * 78)
print()
print("STATUS: LEAK-FREE DUAL-SPACE DIRECTIONAL")
print()
print("REPRESENTATIONS")
print("-" * 78)
print(
    f"layers                 : {len(layer_ids)}"
)
print(
    f"raw RMS dimensions     : {len(raw_rms[0])}"
)
print(
    f"rich dimensions        : {len(rich[0])}"
)
print(
    "normalization          : target-excluded z-score"
)

print()
print("SUMMARY")
print("-" * 78)

for predictor in PREDICTORS:

    s = summary[predictor]

    print(
        f"{predictor:<35} "
        f"cos={s['mean_cosine']:.6f} "
        f"NRMSE={s['mean_nrmse']:.6f} "
        f"wins={s['layer_wins']}"
    )

print()
print("PER-LAYER WINNERS")
print("-" * 78)

for r in results:

    scores = {
        p: r["predictions"][p]["nrmse"]
        for p in PREDICTORS
    }

    winner = min(
        scores,
        key=lambda x: scores[x]
    )

    print(
        f"L{r['layer']:02d} "
        f"{winner:<35} "
        f"NRMSE={scores[winner]:.6f}"
    )

print()
print(f"Saved: {OUT}")
