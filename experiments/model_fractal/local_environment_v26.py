import json
import math
import random
from pathlib import Path
from collections import Counter

INPUT = Path(
    "experiments/model_fractal/normalized_geometry_v10.json"
)

V24 = Path(
    "experiments/model_fractal/spatial_null_v24.json"
)

OUTPUT = Path(
    "experiments/model_fractal/local_environment_v26.json"
)

PERIOD = 8
NULL_TRIALS = 2000
SEED = 2601
EPS = 1e-12

random.seed(SEED)

g = json.loads(INPUT.read_text())
v24 = json.loads(V24.read_text())

points = [
    (
        float(p["x"]),
        float(p["y"]),
        float(p["z"]),
    )
    for p in g["layer_coordinates"]
]

N = len(points)


def sub(a, b):
    return tuple(
        x - y for x, y in zip(a, b)
    )


def dot(a, b):
    return sum(
        x * y for x, y in zip(a, b)
    )


def norm(v):
    return math.sqrt(
        dot(v, v)
    )


def distance(a, b):
    return norm(
        sub(a, b)
    )


def cosine(a, b):
    na = norm(a)
    nb = norm(b)

    if na <= EPS or nb <= EPS:
        return 0.0

    return dot(a, b) / (na * nb)


def mean(values):
    values = list(values)
    return (
        sum(values) / len(values)
        if values
        else 0.0
    )


def rms(values):
    values = list(values)
    return (
        math.sqrt(
            sum(
                x * x for x in values
            ) / len(values)
        )
        if values
        else 0.0
    )


# ----------------------------------------------------------------------
# Bond threshold
# ----------------------------------------------------------------------

pair_distances = sorted(
    distance(points[i], points[j])
    for i in range(N)
    for j in range(i + 1, N)
)

threshold = float(
    v24.get(
        "bond_threshold",
        pair_distances[
            int(0.20 * len(pair_distances))
        ],
    )
)


# ----------------------------------------------------------------------
# Graph
# ----------------------------------------------------------------------

neighbors = [
    []
    for _ in range(N)
]

edges = []

for i in range(N):
    for j in range(i + 1, N):

        d = distance(
            points[i],
            points[j],
        )

        if d <= threshold:

            edges.append(
                {
                    "i": i,
                    "j": j,
                    "distance": d,
                }
            )

            neighbors[i].append(j)
            neighbors[j].append(i)


degrees = [
    len(x)
    for x in neighbors
]


# ----------------------------------------------------------------------
# Local environment fingerprint
#
# The fingerprint deliberately avoids global coordinates.
#
# It contains:
#   - degree
#   - sorted neighbor distances
#   - sorted neighbor-neighbor distances
#   - local angles
# ----------------------------------------------------------------------

def environment(index, ps, ns):

    center = ps[index]

    neighbor_distances = sorted(
        distance(
            center,
            ps[j],
        )
        for j in ns[index]
    )

    angles = []

    for a in range(
        len(ns[index])
    ):
        for b in range(
            a + 1,
            len(ns[index])
        ):

            va = sub(
                ps[ns[index][a]],
                center,
            )

            vb = sub(
                ps[ns[index][b]],
                center,
            )

            c = cosine(
                va,
                vb,
            )

            c = max(
                -1.0,
                min(1.0, c),
            )

            angles.append(
                math.degrees(
                    math.acos(c)
                )
            )

    neighbor_pair_distances = []

    for a in range(
        len(ns[index])
    ):
        for b in range(
            a + 1,
            len(ns[index])
        ):

            neighbor_pair_distances.append(
                distance(
                    ps[ns[index][a]],
                    ps[ns[index][b]],
                )
            )

    return {
        "degree": len(ns[index]),
        "distances": sorted(
            neighbor_distances
        ),
        "angles": sorted(
            angles
        ),
        "neighbor_pairs": sorted(
            neighbor_pair_distances
        ),
    }


def sequence_similarity(a, b):

    if (
        not a
        and not b
    ):
        return 1.0

    if (
        not a
        or not b
    ):
        return 0.0

    n = min(
        len(a),
        len(b),
    )

    values = []

    for i in range(n):

        x = a[i]
        y = b[i]

        scale = max(
            abs(x),
            abs(y),
            EPS,
        )

        values.append(
            max(
                0.0,
                1.0
                - abs(x - y) / scale,
            )
        )

    return mean(values)


def environment_similarity(a, b):

    degree_similarity = (
        1.0
        - (
            abs(
                a["degree"]
                - b["degree"]
            )
            / max(
                a["degree"],
                b["degree"],
                1,
            )
        )
    )

    distance_similarity = (
        sequence_similarity(
            a["distances"],
            b["distances"],
        )
    )

    angle_similarity = (
        sequence_similarity(
            a["angles"],
            b["angles"],
        )
    )

    pair_similarity = (
        sequence_similarity(
            a["neighbor_pairs"],
            b["neighbor_pairs"],
        )
    )

    return (
        0.25 * degree_similarity
        + 0.25 * distance_similarity
        + 0.25 * angle_similarity
        + 0.25 * pair_similarity
    )


# ----------------------------------------------------------------------
# Observed environments
# ----------------------------------------------------------------------

observed_env = [
    environment(
        i,
        points,
        neighbors,
    )
    for i in range(N)
]


# ----------------------------------------------------------------------
# Period-8 local recurrence
# ----------------------------------------------------------------------

pair_scores = []

for i in range(
    N - PERIOD
):

    j = i + PERIOD

    pair_scores.append(
        environment_similarity(
            observed_env[i],
            observed_env[j],
        )
    )

observed_similarity = mean(
    pair_scores
)


# ----------------------------------------------------------------------
# Degree-preserving local comparison
# ----------------------------------------------------------------------

degree_match = []

for i in range(
    N - PERIOD
):

    j = i + PERIOD

    degree_match.append(
        1.0
        if degrees[i] == degrees[j]
        else 0.0
    )

observed_degree_recurrence = mean(
    degree_match
)


# ----------------------------------------------------------------------
# Local bond-length recurrence
# ----------------------------------------------------------------------

bond_similarity = []

for i in range(
    N - PERIOD
):

    j = i + PERIOD

    a = observed_env[i][
        "distances"
    ]

    b = observed_env[j][
        "distances"
    ]

    bond_similarity.append(
        sequence_similarity(
            a,
            b,
        )
    )

observed_bond_recurrence = mean(
    bond_similarity
)


# ----------------------------------------------------------------------
# Local angular recurrence
# ----------------------------------------------------------------------

angle_similarity = []

for i in range(
    N - PERIOD
):

    j = i + PERIOD

    a = observed_env[i][
        "angles"
    ]

    b = observed_env[j][
        "angles"
    ]

    angle_similarity.append(
        sequence_similarity(
            a,
            b,
        )
    )

observed_angle_recurrence = mean(
    angle_similarity
)


# ----------------------------------------------------------------------
# Spatial null
#
# Preserve every point's radius but randomize its direction.
# ----------------------------------------------------------------------

radii = [
    norm(p)
    for p in points
]


def random_direction():

    z = random.uniform(
        -1.0,
        1.0,
    )

    phi = random.uniform(
        0.0,
        2.0 * math.pi,
    )

    s = math.sqrt(
        max(
            0.0,
            1.0 - z * z,
        )
    )

    return (
        s * math.cos(phi),
        s * math.sin(phi),
        z,
    )


def null_points():

    return [
        tuple(
            r * x
            for x in random_direction()
        )
        for r in radii
    ]


def build_neighbors(ps):

    ns = [
        []
        for _ in range(N)
    ]

    for i in range(N):
        for j in range(i + 1, N):

            d = distance(
                ps[i],
                ps[j],
            )

            if d <= threshold:

                ns[i].append(j)
                ns[j].append(i)

    return ns


def null_metric(ps):

    ns = build_neighbors(ps)

    env = [
        environment(
            i,
            ps,
            ns,
        )
        for i in range(N)
    ]

    scores = []

    for i in range(
        N - PERIOD
    ):

        scores.append(
            environment_similarity(
                env[i],
                env[i + PERIOD],
            )
        )

    return mean(scores)


# ----------------------------------------------------------------------
# Null distribution
# ----------------------------------------------------------------------

null_values = []

for _ in range(
    NULL_TRIALS
):

    ps = null_points()

    null_values.append(
        null_metric(ps)
    )


null_mean = mean(
    null_values
)

null_std = (
    math.sqrt(
        sum(
            (
                x - null_mean
            ) ** 2
            for x in null_values
        )
        / len(null_values)
    )
    if null_values
    else 0.0
)

z_score = (
    (
        observed_similarity
        - null_mean
    )
    / null_std
    if null_std > EPS
    else 0.0
)

empirical_p = (
    1.0
    + sum(
        x >= observed_similarity
        for x in null_values
    )
) / (
    len(null_values) + 1
)


# ----------------------------------------------------------------------
# Stronger local recurrence classification
# ----------------------------------------------------------------------

if (
    z_score >= 3.0
    and observed_similarity >= 0.65
    and observed_degree_recurrence >= 0.45
):
    classification = (
        "SIGNIFICANT_PERIODIC_LOCAL_ENVIRONMENT"
    )

elif (
    z_score >= 2.0
    and observed_similarity >= 0.55
):
    classification = (
        "WEAK_PERIODIC_LOCAL_ENVIRONMENT"
    )

else:
    classification = (
        "NO_SIGNIFICANT_LOCAL_ENVIRONMENT_RECURRENCE"
    )


# ----------------------------------------------------------------------
# Output
# ----------------------------------------------------------------------

print("=" * 72)
print(
    " OPENMIND / LOCAL ENVIRONMENT RECURRENCE V26"
)
print("=" * 72)

print()
print(
    f"Layers: {N}"
)
print(
    f"Period: {PERIOD}"
)

print()
print("=== GRAPH ===")
print(
    f"bond count = {len(edges)}"
)
print(
    f"mean degree = {mean(degrees):.8f}"
)
print(
    f"bond threshold = {threshold:.8f}"
)

print()
print("=== OBSERVED PERIOD-8 RECURRENCE ===")
print(
    f"environment similarity = "
    f"{observed_similarity:.8f}"
)
print(
    f"degree recurrence = "
    f"{observed_degree_recurrence:.8f}"
)
print(
    f"bond recurrence = "
    f"{observed_bond_recurrence:.8f}"
)
print(
    f"angle recurrence = "
    f"{observed_angle_recurrence:.8f}"
)

print()
print("=== SPATIAL NULL ===")
print(
    f"null mean = "
    f"{null_mean:.8f}"
)
print(
    f"null std = "
    f"{null_std:.8f}"
)
print(
    f"z-score = "
    f"{z_score:.8f}"
)
print(
    f"empirical p = "
    f"{empirical_p:.8f}"
)

print()
print("=== CLASSIFICATION ===")
print(classification)

output = {
    "schema":
        "openmind.local_environment.v26",
    "source":
        str(INPUT),
    "v24_source":
        str(V24),
    "layer_count": N,
    "period": PERIOD,
    "null_trials": NULL_TRIALS,
    "random_seed": SEED,
    "bond_threshold": threshold,
    "bond_count": len(edges),
    "mean_degree": mean(degrees),
    "observed_environment_similarity":
        observed_similarity,
    "observed_degree_recurrence":
        observed_degree_recurrence,
    "observed_bond_recurrence":
        observed_bond_recurrence,
    "observed_angle_recurrence":
        observed_angle_recurrence,
    "null_mean": null_mean,
    "null_std": null_std,
    "z_score": z_score,
    "empirical_p": empirical_p,
    "classification": classification,
}

OUTPUT.write_text(
    json.dumps(
        output,
        indent=2,
        sort_keys=True,
    )
)

print()
print(
    f"Output: {OUTPUT}"
)
print()
print(
    "LOCAL ENVIRONMENT RECURRENCE COMPLETE"
)
