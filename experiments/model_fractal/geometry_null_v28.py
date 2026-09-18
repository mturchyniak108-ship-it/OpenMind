import json
import math
import random
from pathlib import Path

INPUT = Path(
    "experiments/model_fractal/q8_parameter_field_v4_1.json"
)

OUTPUT = Path(
    "experiments/model_fractal/geometry_null_v28.json"
)

SEED = 2801
NULL_RUNS = 2000
EPS = 1e-12


def norm(v):
    return math.sqrt(sum(x * x for x in v))


def distance(a, b):
    return math.sqrt(
        sum((x - y) ** 2 for x, y in zip(a, b))
    )


def cosine(a, b):
    na = norm(a)
    nb = norm(b)

    if na <= EPS or nb <= EPS:
        return 0.0

    return sum(
        x * y for x, y in zip(a, b)
    ) / (na * nb)


def mean(values):
    return (
        sum(values) / len(values)
        if values else 0.0
    )


def layer_vector(layer):
    # Use the same 12-component RMS representation
    # used by transition_field_v5.py.
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

    result = []

    for component in components:
        item = layer.get(component)

        if item is None:
            continue

        stats = item.get("stats", {})
        value = stats.get("rms")

        if value is None:
            raise ValueError(
                f"Missing RMS for {component}"
            )

        result.append(float(value))

    return result


def transition_distances(order, vectors):
    return [
        distance(
            vectors[order[i]],
            vectors[order[i + 1]],
        )
        for i in range(len(order) - 1)
    ]


def transition_cosines(order, vectors):
    return [
        cosine(
            vectors[order[i]],
            vectors[order[i + 1]],
        )
        for i in range(len(order) - 1)
    ]


def lag_distances(order, vectors, lag):
    return [
        distance(
            vectors[order[i]],
            vectors[order[i + lag]],
        )
        for i in range(len(order) - lag)
    ]


def recurrence_minima(order, vectors):
    values = []

    for i in range(len(order)):
        for j in range(i + 2, len(order)):
            values.append(
                distance(
                    vectors[order[i]],
                    vectors[order[j]],
                )
            )

    return values


def turning_angles(order, vectors):
    angles = []

    for i in range(1, len(order) - 1):
        a = vectors[order[i - 1]]
        b = vectors[order[i]]
        c = vectors[order[i + 1]]

        u = [
            x - y
            for x, y in zip(a, b)
        ]

        v = [
            x - y
            for x, y in zip(c, b)
        ]

        nu = norm(u)
        nv = norm(v)

        if nu <= EPS or nv <= EPS:
            continue

        value = sum(
            x * y for x, y in zip(u, v)
        ) / (nu * nv)

        value = max(-1.0, min(1.0, value))

        angles.append(math.acos(value))

    return angles


def summarize(values):
    if not values:
        return {
            "count": 0,
            "mean": 0.0,
            "min": 0.0,
            "max": 0.0,
        }

    return {
        "count": len(values),
        "mean": mean(values),
        "min": min(values),
        "max": max(values),
    }


def measure(order, vectors):
    transitions = transition_distances(
        order,
        vectors,
    )

    cosines = transition_cosines(
        order,
        vectors,
    )

    lags = {}

    for lag in range(1, len(order)):
        values = lag_distances(
            order,
            vectors,
            lag,
        )

        lags[str(lag)] = mean(values)

    recurrence = recurrence_minima(
        order,
        vectors,
    )

    angles = turning_angles(
        order,
        vectors,
    )

    return {
        "mean_transition_distance":
            mean(transitions),

        "transition_distance":
            summarize(transitions),

        "mean_cosine_similarity":
            mean(cosines),

        "minimum_cosine_similarity":
            min(cosines),

        "maximum_cosine_similarity":
            max(cosines),

        "lag_distance":
            lags,

        "nonlocal_recurrence":
            summarize(recurrence),

        "turning_angle":
            summarize(angles),
    }


def percentile(values, p):
    if not values:
        return 0.0

    values = sorted(values)

    index = (
        (len(values) - 1) * p
    )

    lo = int(math.floor(index))
    hi = int(math.ceil(index))

    if lo == hi:
        return values[lo]

    fraction = index - lo

    return (
        values[lo] * (1 - fraction)
        + values[hi] * fraction
    )


data = json.loads(
    INPUT.read_text()
)

layers = data["layers"]

layer_ids = sorted(
    int(x)
    for x in layers
)

vectors = {
    layer_id:
        layer_vector(layers[str(layer_id)])
    for layer_id in layer_ids
}

dimension = len(
    vectors[layer_ids[0]]
)

real_order = layer_ids[:]

real = measure(
    real_order,
    vectors,
)

rng = random.Random(SEED)

null_values = {
    "mean_transition_distance": [],
    "mean_cosine_similarity": [],
    "lag_1": [],
    "lag_2": [],
    "lag_4": [],
    "lag_8": [],
    "lag_13": [],
    "minimum_nonlocal_distance": [],
    "mean_turning_angle": [],
}

for _ in range(NULL_RUNS):

    order = layer_ids[:]

    rng.shuffle(order)

    result = measure(
        order,
        vectors,
    )

    null_values[
        "mean_transition_distance"
    ].append(
        result["mean_transition_distance"]
    )

    null_values[
        "mean_cosine_similarity"
    ].append(
        result["mean_cosine_similarity"]
    )

    for lag in (1, 2, 4, 8, 13):
        null_values[
            f"lag_{lag}"
        ].append(
            result["lag_distance"][str(lag)]
        )

    null_values[
        "minimum_nonlocal_distance"
    ].append(
        result[
            "nonlocal_recurrence"
        ]["min"]
    )

    null_values[
        "mean_turning_angle"
    ].append(
        result[
            "turning_angle"
        ]["mean"]
    )


null_summary = {}

for key, values in null_values.items():
    null_summary[key] = {
        "mean": mean(values),
        "p01": percentile(values, 0.01),
        "p05": percentile(values, 0.05),
        "p50": percentile(values, 0.50),
        "p95": percentile(values, 0.95),
        "p99": percentile(values, 0.99),
    }


def percentile_rank(value, values):
    if not values:
        return 0.0

    return (
        sum(x <= value for x in values)
        / len(values)
    )


comparison = {
    "transition_distance_percentile":
        percentile_rank(
            real["mean_transition_distance"],
            null_values[
                "mean_transition_distance"
            ],
        ),

    "cosine_percentile":
        percentile_rank(
            real["mean_cosine_similarity"],
            null_values[
                "mean_cosine_similarity"
            ],
        ),

    "lag_1_percentile":
        percentile_rank(
            real["lag_distance"]["1"],
            null_values["lag_1"],
        ),

    "lag_2_percentile":
        percentile_rank(
            real["lag_distance"]["2"],
            null_values["lag_2"],
        ),

    "lag_4_percentile":
        percentile_rank(
            real["lag_distance"]["4"],
            null_values["lag_4"],
        ),

    "lag_8_percentile":
        percentile_rank(
            real["lag_distance"]["8"],
            null_values["lag_8"],
        ),

    "lag_13_percentile":
        percentile_rank(
            real["lag_distance"]["13"],
            null_values["lag_13"],
        ),

    "turning_angle_percentile":
        percentile_rank(
            real["turning_angle"]["mean"],
            null_values[
                "mean_turning_angle"
            ],
        ),
}


result = {
    "schema":
        "openmind.geometry_null.v28",

    "source":
        str(INPUT),

    "layer_count":
        len(layer_ids),

    "component_dimension":
        dimension,

    "seed":
        SEED,

    "null_runs":
        NULL_RUNS,

    "real_order":
        real_order,

    "real":
        real,

    "null":
        null_summary,

    "comparison":
        comparison,
}

OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

OUTPUT.write_text(
    json.dumps(
        result,
        indent=2,
    )
)

print("=" * 72)
print(" OPENMIND / GEOMETRY NULL V28")
print("=" * 72)
print()
print("Layers:", len(layer_ids))
print("Dimensions:", dimension)
print("Null runs:", NULL_RUNS)
print()
print(
    "REAL mean transition distance:",
    real["mean_transition_distance"],
)
print(
    "NULL mean:",
    null_summary[
        "mean_transition_distance"
    ]["mean"],
)
print(
    "REAL percentile:",
    comparison[
        "transition_distance_percentile"
    ],
)
print()
print(
    "REAL mean cosine:",
    real["mean_cosine_similarity"],
)
print(
    "NULL mean:",
    null_summary[
        "mean_cosine_similarity"
    ]["mean"],
)
print(
    "REAL percentile:",
    comparison[
        "cosine_percentile"
    ],
)
print()
print("LAG DISTANCES")
for lag in (1, 2, 4, 8, 13):
    print(
        f"  lag {lag:02d}: "
        f"{real['lag_distance'][str(lag)]:.8f}"
    )
print()
print("OUTPUT:", OUTPUT)
print("=" * 72)
