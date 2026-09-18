import json
import math
import random
from pathlib import Path

INPUT = Path(
    "experiments/model_fractal/q8_parameter_field_v4_1.json"
)

OUTPUT = Path(
    "experiments/model_fractal/geometry_scaling_windows_v32.json"
)

NULL_RUNS = 10000
SEED = 28032
EPS = 1e-15

random.seed(SEED)

data = json.loads(INPUT.read_text())

components = [
    "attn_norm.weight",
    "ffn_down.weight",
    "ffn_gate.weight",
    "ffn_up.weight",
    "ffn_norm.weight",
    "attn_k.bias",
    "attn_k.weight",
    "attn_output.weight",
    "attn_q.bias",
    "attn_q.weight",
    "attn_v.bias",
    "attn_v.weight",
]

layers_data = data["layers"]

layer_ids = sorted(
    layers_data,
    key=lambda x: int(x),
)

layers = len(layer_ids)

vectors = []

for layer_id in layer_ids:
    layer = layers_data[str(layer_id)]
    vector = []

    for component in components:
        item = layer.get(component)

        if item is None:
            raise ValueError(
                f"Missing component {component} "
                f"in layer {layer_id}"
            )

        value = item.get("stats", {}).get("rms")

        if value is None:
            raise ValueError(
                f"Missing RMS for {component} "
                f"in layer {layer_id}"
            )

        vector.append(float(value))

    vectors.append(vector)


def distance(a, b):
    return math.sqrt(
        sum(
            (x - y) ** 2
            for x, y in zip(a, b)
        )
    )


def lag_distances(order, lag):
    return [
        distance(
            vectors[order[i]],
            vectors[order[i + lag]],
        )
        for i in range(len(order) - lag)
    ]


def mean(values):
    return sum(values) / len(values)


def std(values):
    m = mean(values)

    return math.sqrt(
        sum((x - m) ** 2 for x in values)
        / len(values)
    )


def exponent(curve):
    points = [
        (
            math.log(lag),
            math.log(value),
        )
        for lag, value in curve
        if lag > 0 and value > 0
    ]

    if len(points) < 2:
        return 0.0

    xs = [x for x, _ in points]
    ys = [y for _, y in points]

    mx = mean(xs)
    my = mean(ys)

    numerator = sum(
        (x - mx) * (y - my)
        for x, y in points
    )

    denominator = sum(
        (x - mx) ** 2
        for x in xs
    )

    if denominator <= EPS:
        return 0.0

    return numerator / denominator


# ------------------------------------------------------------
# Windows to test
# ------------------------------------------------------------

windows = {
    "short_1_8": (1, 8),
    "short_1_12": (1, 12),
    "mid_2_16": (2, 16),
    "mid_4_20": (4, 20),
    "full_1_27": (1, 27),
    "trimmed_1_20": (1, 20),
    "trimmed_1_23": (1, 23),
}


def curve_for_order(order, lo, hi):
    return [
        (
            lag,
            mean(lag_distances(order, lag)),
        )
        for lag in range(lo, hi + 1)
    ]


real_order = list(range(layers))

real_curves = {
    name: curve_for_order(
        real_order,
        lo,
        hi,
    )
    for name, (lo, hi) in windows.items()
}

real_exponents = {
    name: exponent(curve)
    for name, curve in real_curves.items()
}


# ------------------------------------------------------------
# Null distributions
# ------------------------------------------------------------

null_exponents = {
    name: []
    for name in windows
}

for _ in range(NULL_RUNS):

    order = list(range(layers))
    random.shuffle(order)

    for name, (lo, hi) in windows.items():

        curve = curve_for_order(
            order,
            lo,
            hi,
        )

        null_exponents[name].append(
            exponent(curve)
        )


statistics = {}

for name in windows:

    values = null_exponents[name]
    real_value = real_exponents[name]

    null_mean = mean(values)
    null_sd = std(values)

    z = (
        real_value - null_mean
    ) / max(null_sd, EPS)

    p = (
        sum(
            x >= real_value
            for x in values
        ) + 1
    ) / (NULL_RUNS + 1)

    statistics[name] = {
        "real_exponent":
            real_value,

        "null_mean":
            null_mean,

        "null_sd":
            null_sd,

        "z":
            z,

        "empirical_p":
            p,
    }


result = {
    "schema":
        "openmind.geometry_scaling_windows.v32",

    "source":
        str(INPUT),

    "layer_count":
        layers,

    "null_runs":
        NULL_RUNS,

    "seed":
        SEED,

    "windows":
        {
            name: {
                "min_lag": lo,
                "max_lag": hi,
            }
            for name, (lo, hi) in windows.items()
        },

    "real_curves":
        real_curves,

    "statistics":
        statistics,
}


OUTPUT.write_text(
    json.dumps(
        result,
        indent=2,
    )
)

print("=" * 72)
print(" OPENMIND / GEOMETRY SCALING WINDOWS V32")
print("=" * 72)
print()
print("Layers:", layers)
print("Permutation runs:", NULL_RUNS)
print()
print("WINDOW RESULTS")

for name in windows:

    s = statistics[name]

    print()
    print(name)
    print(
        "  real exponent:",
        s["real_exponent"],
    )
    print(
        "  null mean:",
        s["null_mean"],
    )
    print(
        "  null SD:",
        s["null_sd"],
    )
    print(
        "  z:",
        s["z"],
    )
    print(
        "  empirical p:",
        s["empirical_p"],
    )

print()
print("OUTPUT:", OUTPUT)
print("=" * 72)
