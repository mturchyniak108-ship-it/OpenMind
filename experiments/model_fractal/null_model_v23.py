import json
import math
import random
from pathlib import Path

INPUT = Path(
    "experiments/model_fractal/topology_lattice_v22.json"
)

GEOMETRY = Path(
    "experiments/model_fractal/normalized_geometry_v10.json"
)

OUTPUT = Path(
    "experiments/model_fractal/null_model_v23.json"
)

EPS = 1e-12
PERIOD = 8
TRIALS = 2000
SEED = 2301

random.seed(SEED)

d = json.loads(INPUT.read_text())
g = json.loads(GEOMETRY.read_text())

points = [
    (
        float(p["x"]),
        float(p["y"]),
        float(p["z"]),
    )
    for p in g["layer_coordinates"]
]

N = len(points)

print("=" * 72)
print(" OPENMIND / DEGREE-PRESERVING NULL MODEL V23")
print("=" * 72)
print()
print(f"Layers: {N}")
print(f"Period: {PERIOD}")
print(f"Null trials: {TRIALS}")
print(f"Random seed: {SEED}")


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


def build_edges():
    threshold = float(
        d["bond_threshold"]
    )

    edges = []

    for i in range(N):
        for j in range(i + 1, N):
            if distance(
                points[i],
                points[j],
            ) <= threshold:
                edges.append(
                    (i, j)
                )

    return edges


edges = build_edges()

adjacency = [
    set()
    for _ in range(N)
]

for a, b in edges:
    adjacency[a].add(b)
    adjacency[b].add(a)


degrees = [
    len(x)
    for x in adjacency
]


# ----------------------------------------------------------------------
# Observed period-8 topology
# ----------------------------------------------------------------------

def environment_similarity(
    a,
    b,
    graph,
):
    na = graph[a]
    nb = graph[b]

    if not na or not nb:
        return 0.0

    da = len(na)
    db = len(nb)

    degree_score = (
        min(da, db)
        / max(da, db)
    )

    common = len(
        na.intersection(nb)
    )

    union = len(
        na.union(nb)
    )

    jaccard = (
        common / union
        if union
        else 0.0
    )

    return (
        0.5 * degree_score
        + 0.5 * jaccard
    )


def topology_score(graph):
    values = []

    for i in range(
        N - PERIOD
    ):
        j = i + PERIOD

        values.append(
            environment_similarity(
                i,
                j,
                graph,
            )
        )

    return (
        sum(values) / len(values)
        if values
        else 0.0
    )


def translation_score():
    values = []

    for i in range(
        N - PERIOD - 1
    ):
        a = sub(
            points[i + PERIOD],
            points[i],
        )

        b = sub(
            points[i + PERIOD + 1],
            points[i + 1],
        )

        values.append(
            abs(cosine(a, b))
        )

    return (
        sum(values) / len(values)
        if values
        else 0.0
    )


observed_topology = topology_score(
    adjacency
)

observed_translation = (
    translation_score()
)


# ----------------------------------------------------------------------
# Degree-preserving edge rewiring
# ----------------------------------------------------------------------

def randomized_graph():
    graph = [
        set()
        for _ in range(N)
    ]

    edge_list = list(edges)

    # Double-edge swap preserves every vertex degree.
    swaps = max(
        100,
        len(edge_list) * 20,
    )

    for _ in range(swaps):
        i, j = random.sample(
            range(len(edge_list)),
            2,
        )

        a, b = edge_list[i]
        c, d4 = edge_list[j]

        if len({
            a, b, c, d4
        }) < 4:
            continue

        candidates = [
            ((a, d4), (c, b)),
            ((a, c), (b, d4)),
        ]

        old = {
            tuple(sorted((a, b))),
            tuple(sorted((c, d4))),
        }

        for e1, e2 in candidates:
            x = tuple(
                sorted(e1)
            )
            y = tuple(
                sorted(e2)
            )

            if x == y:
                continue

            if x in old or y in old:
                continue

            if (
                x[0] == x[1]
                or y[0] == y[1]
            ):
                continue

            existing = {
                tuple(sorted(e))
                for e in edge_list
            }

            if x in existing or y in existing:
                continue

            edge_list[i] = x
            edge_list[j] = y
            break

    for a, b in edge_list:
        graph[a].add(b)
        graph[b].add(a)

    return graph


# ----------------------------------------------------------------------
# Null distribution
# ----------------------------------------------------------------------

null_topology = []
null_translation = []

for trial in range(TRIALS):
    graph = randomized_graph()

    null_topology.append(
        topology_score(graph)
    )

    # Translation is a geometric statistic and therefore does not change
    # under graph rewiring. Keep it explicit rather than pretending it is
    # a graph-null statistic.
    null_translation.append(
        observed_translation
    )


def mean(values):
    return (
        sum(values) / len(values)
        if values
        else 0.0
    )


def std(values):
    if not values:
        return 0.0

    m = mean(values)

    return math.sqrt(
        sum(
            (x - m) ** 2
            for x in values
        ) / len(values)
    )


null_mean = mean(
    null_topology
)

null_std = std(
    null_topology
)

z_score = (
    (observed_topology - null_mean)
    / null_std
    if null_std > EPS
    else 0.0
)

exceedances = sum(
    x >= observed_topology
    for x in null_topology
)

empirical_p = (
    (exceedances + 1)
    / (TRIALS + 1)
)


# ----------------------------------------------------------------------
# Degree preservation verification
# ----------------------------------------------------------------------

verification_graph = randomized_graph()

degree_preserved = (
    sorted(
        len(x)
        for x in verification_graph
    )
    == sorted(degrees)
)


# ----------------------------------------------------------------------
# Classification
# ----------------------------------------------------------------------

if z_score >= 3.0 and empirical_p < 0.01:
    classification = (
        "SIGNIFICANT_PERIODIC_TOPOLOGY"
    )
elif z_score >= 2.0 and empirical_p < 0.05:
    classification = (
        "MODERATE_PERIODIC_TOPOLOGY"
    )
else:
    classification = (
        "NO_SIGNIFICANT_TOPOLOGICAL_PERIODICITY"
    )


print()
print("=== OBSERVED STRUCTURE ===")
print(
    f"period-8 topology = "
    f"{observed_topology:.8f}"
)
print(
    f"translation score = "
    f"{observed_translation:.8f}"
)

print()
print("=== DEGREE SEQUENCE ===")
print(
    f"degree sequence preserved = "
    f"{degree_preserved}"
)

print()
print("=== DEGREE-PRESERVING NULL ===")
print(
    f"null mean = "
    f"{null_mean:.8f}"
)
print(
    f"null std  = "
    f"{null_std:.8f}"
)
print(
    f"z-score   = "
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
    "schema": (
        "openmind.degree_preserving_null_model.v23"
    ),
    "source": str(INPUT),
    "geometry_source": str(GEOMETRY),
    "layer_count": N,
    "period": PERIOD,
    "trials": TRIALS,
    "seed": SEED,
    "bond_count": len(edges),
    "bond_threshold": d["bond_threshold"],
    "degree_sequence": degrees,
    "degree_sequence_preserved": degree_preserved,
    "observed_period8_topology": observed_topology,
    "observed_translation_score": observed_translation,
    "null_mean": null_mean,
    "null_std": null_std,
    "z_score": z_score,
    "exceedances": exceedances,
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
    "DEGREE-PRESERVING NULL MODEL COMPLETE"
)
