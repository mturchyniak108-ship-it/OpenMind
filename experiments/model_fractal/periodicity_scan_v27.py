import json
import math
import random
from pathlib import Path

INPUT = Path(
    "experiments/model_fractal/normalized_geometry_v10.json"
)

OUTPUT = Path(
    "experiments/model_fractal/periodicity_scan_v27.json"
)

SEED = 2701
TRIALS = 2000
MIN_PERIOD = 2
MAX_PERIOD = 13
EPS = 1e-12

random.seed(SEED)

d = json.loads(INPUT.read_text())

raw_points = d["layer_coordinates"]

points = [
    (
        float(p["x"]),
        float(p["y"]),
        float(p["z"]),
    )
    for p in raw_points
]

N = len(points)


def sub(a, b):
    return tuple(
        x - y
        for x, y in zip(a, b)
    )


def dot(a, b):
    return sum(
        x * y
        for x, y in zip(a, b)
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


def percentile(values, q):
    if not values:
        return 0.0

    values = sorted(values)

    pos = q * (len(values) - 1)

    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))

    if lo == hi:
        return values[lo]

    return (
        values[lo]
        + (values[hi] - values[lo])
        * (pos - lo)
    )


# ----------------------------------------------------------------------
# Spatial scale
#
# Use the same broad neighborhood definition used by V24/V25.
# ----------------------------------------------------------------------

pair_distances = [
    distance(points[i], points[j])
    for i in range(N)
    for j in range(i + 1, N)
]

bond_threshold = percentile(
    pair_distances,
    0.20,
)


def build_graph(ps):
    neighbors = [
        set()
        for _ in range(len(ps))
    ]

    for i in range(len(ps)):
        for j in range(i + 1, len(ps)):
            if distance(ps[i], ps[j]) <= bond_threshold:
                neighbors[i].add(j)
                neighbors[j].add(i)

    return neighbors


def local_signature(ps, neighbors, i):
    center = ps[i]

    distances = sorted(
        distance(center, ps[j])
        for j in neighbors[i]
    )

    if not distances:
        return (
            0.0,
            0.0,
            0.0,
        )

    degree = float(len(distances))

    mean_distance = mean(distances)

    distance_cv = (
        math.sqrt(
            mean(
                (x - mean_distance) ** 2
                for x in distances
            )
        ) / mean_distance
        if mean_distance > EPS
        else 0.0
    )

    return (
        degree,
        mean_distance,
        distance_cv,
    )


def signature_similarity(a, b):
    # Degree similarity.
    degree_sim = (
        min(a[0], b[0])
        / max(a[0], b[0])
        if max(a[0], b[0]) > EPS
        else 1.0
    )

    # Local radial similarity.
    radial_sim = (
        min(a[1], b[1])
        / max(a[1], b[1])
        if max(a[1], b[1]) > EPS
        else 1.0
    )

    # Shape/uniformity similarity.
    uniform_sim = max(
        0.0,
        1.0 - abs(a[2] - b[2]),
    )

    return (
        degree_sim
        + radial_sim
        + uniform_sim
    ) / 3.0


def period_metric(ps, period):
    neighbors = build_graph(ps)

    signatures = [
        local_signature(
            ps,
            neighbors,
            i,
        )
        for i in range(len(ps))
    ]

    scores = []

    # Compare only complete period windows.
    for i in range(
        len(ps) - period
    ):
        j = i + period

        scores.append(
            signature_similarity(
                signatures[i],
                signatures[j],
            )
        )

    return mean(scores)


# ----------------------------------------------------------------------
# Observed period scan
# ----------------------------------------------------------------------

observed = {}

for period in range(
    MIN_PERIOD,
    MAX_PERIOD + 1,
):
    observed[period] = period_metric(
        points,
        period,
    )


# ----------------------------------------------------------------------
# Spatial null
#
# Preserve radial distances from the origin while randomizing directions.
# ----------------------------------------------------------------------

radii = [
    norm(p)
    for p in points
]


def random_radial_points():
    result = []

    for r in radii:
        # Uniform random direction on S^2.
        z = random.uniform(
            -1.0,
            1.0,
        )

        theta = random.uniform(
            0.0,
            2.0 * math.pi,
        )

        xy = math.sqrt(
            max(
                0.0,
                1.0 - z * z,
            )
        )

        result.append(
            (
                r * xy * math.cos(theta),
                r * xy * math.sin(theta),
                r * z,
            )
        )

    return result


null_values = {
    period: []
    for period in range(
        MIN_PERIOD,
        MAX_PERIOD + 1,
    )
}


for _ in range(TRIALS):
    ps = random_radial_points()

    for period in range(
        MIN_PERIOD,
        MAX_PERIOD + 1,
    ):
        null_values[period].append(
            period_metric(
                ps,
                period,
            )
        )


# ----------------------------------------------------------------------
# Statistics
# ----------------------------------------------------------------------

results = []

for period in range(
    MIN_PERIOD,
    MAX_PERIOD + 1,
):
    null = null_values[period]

    mu = mean(null)

    sigma = math.sqrt(
        mean(
            (x - mu) ** 2
            for x in null
        )
    )

    obs = observed[period]

    z = (
        (obs - mu) / sigma
        if sigma > EPS
        else 0.0
    )

    greater_equal = sum(
        x >= obs
        for x in null
    )

    empirical_p = (
        (greater_equal + 1)
        / (TRIALS + 1)
    )

    results.append(
        {
            "period": period,
            "observed": obs,
            "null_mean": mu,
            "null_std": sigma,
            "z_score": z,
            "empirical_p": empirical_p,
        }
    )


results.sort(
    key=lambda x: x["observed"],
    reverse=True,
)

best_observed = results[0]

# Best period by null-normalized significance.
best_z = max(
    results,
    key=lambda x: x["z_score"],
)

# Bonferroni correction for the 12 tested periods.
tested_periods = (
    MAX_PERIOD - MIN_PERIOD + 1
)

bonferroni_alpha = (
    0.05 / tested_periods
)

significant_periods = [
    r
    for r in results
    if r["empirical_p"]
    <= bonferroni_alpha
]


# ----------------------------------------------------------------------
# Print
# ----------------------------------------------------------------------

print("=" * 72)
print(" OPENMIND / PERIODICITY SCAN V27")
print("=" * 72)

print()
print(f"Layers: {N}")
print(
    f"Periods: "
    f"{MIN_PERIOD}-{MAX_PERIOD}"
)
print(f"Null trials: {TRIALS}")
print(f"Random seed: {SEED}")
print(
    f"Bond threshold: "
    f"{bond_threshold:.8f}"
)

print()
print("=== PERIODICITY SCAN ===")

for r in results:
    print(
        f"period={r['period']:2d} "
        f"obs={r['observed']:.8f} "
        f"null={r['null_mean']:.8f} "
        f"z={r['z_score']:.5f} "
        f"p={r['empirical_p']:.5f}"
    )

print()
print("=== BEST OBSERVED PERIOD ===")
print(
    f"period = "
    f"{best_observed['period']}"
)
print(
    f"score  = "
    f"{best_observed['observed']:.8f}"
)

print()
print("=== BEST NULL-NORMALIZED PERIOD ===")
print(
    f"period = "
    f"{best_z['period']}"
)
print(
    f"z-score = "
    f"{best_z['z_score']:.5f}"
)
print(
    f"p = "
    f"{best_z['empirical_p']:.5f}"
)

print()
print("=== MULTIPLE-TEST CORRECTION ===")
print(
    f"tested periods = "
    f"{tested_periods}"
)
print(
    f"Bonferroni alpha = "
    f"{bonferroni_alpha:.6f}"
)
print(
    f"significant periods = "
    f"{len(significant_periods)}"
)

print()
print("=== CLASSIFICATION ===")

if (
    best_z["period"] == 8
    and best_z["empirical_p"]
    <= bonferroni_alpha
):
    classification = (
        "ROBUST_PERIOD_8_SPATIAL_RECURRENCE"
    )
elif (
    best_z["empirical_p"]
    <= bonferroni_alpha
):
    classification = (
        "ROBUST_PERIODIC_SPATIAL_RECURRENCE"
    )
elif best_z["z_score"] >= 3.0:
    classification = (
        "UNCORRECTED_PERIODIC_SIGNAL"
    )
else:
    classification = (
        "NO_ROBUST_PERIODICITY"
    )

print(classification)


output = {
    "schema":
        "openmind.periodicity_scan.v27",
    "source": str(INPUT),
    "layer_count": N,
    "period_range": [
        MIN_PERIOD,
        MAX_PERIOD,
    ],
    "null_trials": TRIALS,
    "random_seed": SEED,
    "bond_threshold": bond_threshold,
    "results": results,
    "best_observed_period":
        best_observed,
    "best_null_normalized_period":
        best_z,
    "bonferroni_alpha":
        bonferroni_alpha,
    "significant_periods":
        significant_periods,
    "classification":
        classification,
}

OUTPUT.write_text(
    json.dumps(
        output,
        indent=2,
        sort_keys=True,
    )
)

print()
print(f"Output: {OUTPUT}")
print()
print(
    "PERIODICITY SCAN COMPLETE"
)
