import json
import math
import random
from pathlib import Path

INPUT = Path(
    "experiments/model_fractal/q8_parameter_field_v4_1.json"
)

OUTPUT = Path(
    "experiments/model_fractal/geometry_order_null_v30.json"
)

NULL_RUNS = 10000
SEED = 28029
EPS = 1e-15

random.seed(SEED)

data = json.loads(INPUT.read_text())

# ------------------------------------------------------------
# Recover the ACTUAL ordered layer vectors directly from the
# source RMS parameter field.
#
# IMPORTANT:
# Do not reconstruct these vectors from transition deltas.
# Delta reconstruction produces R_i - R_0, which preserves
# Euclidean distances but changes cosine geometry.
# ------------------------------------------------------------

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

        stats = item.get("stats", {})
        value = stats.get("rms")

        if value is None:
            raise ValueError(
                f"Missing RMS for {component} "
                f"in layer {layer_id}"
            )

        vector.append(float(value))

    vectors.append(vector)

if len(vectors) != layers:
    raise ValueError(
        f"Expected {layers} vectors, got {len(vectors)}"
    )

if any(len(v) != dimension for v in vectors):
    raise ValueError("Inconsistent vector dimension")


def distance(a, b):
    return math.sqrt(
        sum(
            (x - y) ** 2
            for x, y in zip(a, b)
        )
    )


def cosine(a, b):
    dot = sum(
        x * y
        for x, y in zip(a, b)
    )

    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))

    if na <= EPS or nb <= EPS:
        return 0.0

    return dot / (na * nb)


def evaluate(order):
    distances = []
    cosines = []

    for i in range(len(order) - 1):
        a = vectors[order[i]]
        b = vectors[order[i + 1]]

        distances.append(distance(a, b))
        cosines.append(cosine(a, b))

    return {
        "mean_distance":
            sum(distances) / len(distances),

        "mean_cosine":
            sum(cosines) / len(cosines),

        "median_distance":
            sorted(distances)[len(distances) // 2],

        "min_cosine":
            min(cosines),

        "max_distance":
            max(distances),
    }


# ------------------------------------------------------------
# REAL ORDER
# ------------------------------------------------------------

real_order = list(range(layers))
real = evaluate(real_order)

# ------------------------------------------------------------
# PERMUTATION NULL
# ------------------------------------------------------------

null_distance = []
null_cosine = []
null_median_distance = []
null_min_cosine = []

for _ in range(NULL_RUNS):

    order = list(range(layers))
    random.shuffle(order)

    result = evaluate(order)

    null_distance.append(result["mean_distance"])
    null_cosine.append(result["mean_cosine"])
    null_median_distance.append(
        result["median_distance"]
    )
    null_min_cosine.append(
        result["min_cosine"]
    )


def mean(values):
    return sum(values) / len(values)


def std(values):
    m = mean(values)

    return math.sqrt(
        sum(
            (x - m) ** 2
            for x in values
        ) / len(values)
    )


def percentile_low(real_value, null_values):
    count = sum(
        x <= real_value
        for x in null_values
    )

    return count / len(null_values)


def percentile_high(real_value, null_values):
    count = sum(
        x >= real_value
        for x in null_values
    )

    return count / len(null_values)


def zscore(real_value, null_values):
    return (
        real_value - mean(null_values)
    ) / max(std(null_values), EPS)


distance_p = percentile_low(
    real["mean_distance"],
    null_distance,
)

cosine_p = percentile_high(
    real["mean_cosine"],
    null_cosine,
)

distance_effect = (
    mean(null_distance)
    - real["mean_distance"]
) / max(std(null_distance), EPS)

cosine_effect = (
    real["mean_cosine"]
    - mean(null_cosine)
) / max(std(null_cosine), EPS)


result = {
    "schema":
        "openmind.geometry_order_null.v30",

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

    "real": real,

    "null": {
        "mean_distance":
            mean(null_distance),
        "std_distance":
            std(null_distance),

        "mean_cosine":
            mean(null_cosine),
        "std_cosine":
            std(null_cosine),

        "mean_median_distance":
            mean(null_median_distance),
        "std_median_distance":
            std(null_median_distance),

        "mean_min_cosine":
            mean(null_min_cosine),
        "std_min_cosine":
            std(null_min_cosine),
    },

    "statistics": {
        "distance_lower_tail_fraction":
            distance_p,

        "distance_empirical_p":
            (sum(
                x <= real["mean_distance"]
                for x in null_distance
            ) + 1) / (NULL_RUNS + 1),

        "cosine_upper_tail_fraction":
            cosine_p,

        "cosine_empirical_p":
            (sum(
                x >= real["mean_cosine"]
                for x in null_cosine
            ) + 1) / (NULL_RUNS + 1),

        "distance_z":
            zscore(
                real["mean_distance"],
                null_distance,
            ),

        "cosine_z":
            zscore(
                real["mean_cosine"],
                null_cosine,
            ),

        "distance_effect_size":
            distance_effect,

        "cosine_effect_size":
            cosine_effect,
    },
}

OUTPUT.write_text(
    json.dumps(
        result,
        indent=2,
    )
)

print("=" * 72)
print(" OPENMIND / GEOMETRY ORDER NULL V30")
print("=" * 72)
print()
print("Layers:", layers)
print("Dimensions:", dimension)
print("Permutation runs:", NULL_RUNS)
print()
print("REAL")
print(
    "  mean distance:",
    real["mean_distance"],
)
print(
    "  mean cosine:",
    real["mean_cosine"],
)
print()
print("NULL")
print(
    "  mean distance:",
    mean(null_distance),
)
print(
    "  distance SD:",
    std(null_distance),
)
print(
    "  mean cosine:",
    mean(null_cosine),
)
print(
    "  cosine SD:",
    std(null_cosine),
)
print()
print("SIGNIFICANCE")
print(
    "  distance empirical p:",
    result["statistics"]["distance_empirical_p"],
)
print(
    "  cosine empirical p:",
    result["statistics"]["cosine_empirical_p"],
)
print(
    "  distance z:",
    result["statistics"]["distance_z"],
)
print(
    "  cosine z:",
    result["statistics"]["cosine_z"],
)
print(
    "  distance effect:",
    result["statistics"]["distance_effect_size"],
)
print(
    "  cosine effect:",
    result["statistics"]["cosine_effect_size"],
)
print()
print("OUTPUT:", OUTPUT)
print("=" * 72)
