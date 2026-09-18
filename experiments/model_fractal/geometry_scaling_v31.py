import json
import math
import random
from pathlib import Path

INPUT = Path(
    "experiments/model_fractal/q8_parameter_field_v4_1.json"
)

OUTPUT = Path(
    "experiments/model_fractal/geometry_scaling_v31.json"
)

NULL_RUNS = 10000
SEED = 28031
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
dimension = len(components)

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


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))

    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))

    if na <= EPS or nb <= EPS:
        return 0.0

    return dot / (na * nb)


def lag_measure(order, lag):
    distances = []
    cosines = []

    for i in range(len(order) - lag):
        a = vectors[order[i]]
        b = vectors[order[i + lag]]

        distances.append(distance(a, b))
        cosines.append(cosine(a, b))

    return {
        "mean_distance": sum(distances) / len(distances),
        "mean_cosine": sum(cosines) / len(cosines),
    }


lags = list(range(1, layers))

real = {
    str(lag): lag_measure(
        list(range(layers)),
        lag,
    )
    for lag in lags
}


def mean(values):
    return sum(values) / len(values)


def std(values):
    m = mean(values)

    return math.sqrt(
        sum((x - m) ** 2 for x in values)
        / len(values)
    )


def slope_loglog(values):
    points = [
        (math.log(k), math.log(v))
        for k, v in values
        if k > 0 and v > 0
    ]

    if len(points) < 2:
        return 0.0

    xs = [p[0] for p in points]
    ys = [p[1] for p in points]

    mx = mean(xs)
    my = mean(ys)

    numerator = sum(
        (x - mx) * (y - my)
        for x, y in zip(xs, ys)
    )

    denominator = sum(
        (x - mx) ** 2
        for x in xs
    )

    if denominator <= EPS:
        return 0.0

    return numerator / denominator


real_distance_curve = [
    (lag, real[str(lag)]["mean_distance"])
    for lag in lags
]

real_cosine_curve = [
    (lag, real[str(lag)]["mean_cosine"])
    for lag in lags
]

real_distance_exponent = slope_loglog(
    real_distance_curve
)


null_distance_curves = []
null_cosine_curves = []
null_distance_exponents = []

for _ in range(NULL_RUNS):
    order = list(range(layers))
    random.shuffle(order)

    distance_curve = []
    cosine_curve = []

    for lag in lags:
        measurement = lag_measure(
            order,
            lag,
        )

        distance_curve.append(
            measurement["mean_distance"]
        )

        cosine_curve.append(
            measurement["mean_cosine"]
        )

    null_distance_curves.append(distance_curve)
    null_cosine_curves.append(cosine_curve)

    null_distance_exponents.append(
        slope_loglog(
            list(zip(lags, distance_curve))
        )
    )


null_exponent_mean = mean(
    null_distance_exponents
)

null_exponent_std = std(
    null_distance_exponents
)

exponent_z = (
    real_distance_exponent
    - null_exponent_mean
) / max(
    null_exponent_std,
    EPS,
)

exponent_p = (
    sum(
        x >= real_distance_exponent
        for x in null_distance_exponents
    ) + 1
) / (NULL_RUNS + 1)


# ------------------------------------------------------------
# Pointwise null statistics
# ------------------------------------------------------------

lag_statistics = {}

for index, lag in enumerate(lags):

    distance_values = [
        curve[index]
        for curve in null_distance_curves
    ]

    cosine_values = [
        curve[index]
        for curve in null_cosine_curves
    ]

    real_distance = real[str(lag)]["mean_distance"]
    real_cosine = real[str(lag)]["mean_cosine"]

    distance_p = (
        sum(
            x <= real_distance
            for x in distance_values
        ) + 1
    ) / (NULL_RUNS + 1)

    cosine_p = (
        sum(
            x >= real_cosine
            for x in cosine_values
        ) + 1
    ) / (NULL_RUNS + 1)

    lag_statistics[str(lag)] = {
        "real_distance": real_distance,
        "null_distance_mean": mean(
            distance_values
        ),
        "null_distance_sd": std(
            distance_values
        ),
        "distance_empirical_p": distance_p,

        "real_cosine": real_cosine,
        "null_cosine_mean": mean(
            cosine_values
        ),
        "null_cosine_sd": std(
            cosine_values
        ),
        "cosine_empirical_p": cosine_p,
    }


result = {
    "schema":
        "openmind.geometry_scaling.v31",

    "source":
        str(INPUT),

    "layer_count":
        layers,

    "component_dimension":
        dimension,

    "null_runs":
        NULL_RUNS,

    "seed":
        SEED,

    "lags":
        lags,

    "real":
        real,

    "real_distance_scaling_exponent":
        real_distance_exponent,

    "null_distance_scaling_exponent": {
        "mean": null_exponent_mean,
        "std": null_exponent_std,
    },

    "scaling_statistics": {
        "exponent_z":
            exponent_z,
        "exponent_empirical_p":
            exponent_p,
    },

    "lag_statistics":
        lag_statistics,
}


OUTPUT.write_text(
    json.dumps(
        result,
        indent=2,
    )
)

print("=" * 72)
print(" OPENMIND / GEOMETRY SCALING V31")
print("=" * 72)
print()
print("Layers:", layers)
print("Dimensions:", dimension)
print("Permutation runs:", NULL_RUNS)
print()
print("REAL DISTANCE SCALING EXPONENT:")
print(" ", real_distance_exponent)
print()
print("NULL EXPONENT:")
print("  mean:", null_exponent_mean)
print("  SD:", null_exponent_std)
print()
print("SCALING SIGNIFICANCE")
print("  z:", exponent_z)
print("  empirical p:", exponent_p)
print()
print("LAG CURVE")
for lag in lags:
    r = real[str(lag)]
    print(
        f"  lag {lag:02d}: "
        f"distance={r['mean_distance']:.8f} "
        f"cosine={r['mean_cosine']:.8f}"
    )
print()
print("OUTPUT:", OUTPUT)
print("=" * 72)
