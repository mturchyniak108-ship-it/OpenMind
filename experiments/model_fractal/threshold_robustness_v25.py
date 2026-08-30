import json
import math
from pathlib import Path

INPUT = Path(
    "experiments/model_fractal/spatial_null_v24.json"
)

GEOMETRY = Path(
    "experiments/model_fractal/normalized_geometry_v10.json"
)

OUTPUT = Path(
    "experiments/model_fractal/threshold_robustness_v25.json"
)

PERIOD = 8
EPS = 1e-12

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

base_threshold = float(
    d["bond_threshold"]
)

multipliers = [
    0.80,
    0.85,
    0.90,
    0.95,
    1.00,
    1.05,
    1.10,
    1.15,
    1.20,
]


def sub(a, b):
    return tuple(
        x - y for x, y in zip(a, b)
    )


def dot(a, b):
    return sum(
        x * y for x, y in zip(a, b)
    )


def norm(v):
    return math.sqrt(dot(v, v))


def distance(a, b):
    return norm(sub(a, b))


def cosine(a, b):
    na = norm(a)
    nb = norm(b)

    if na <= EPS or nb <= EPS:
        return 0.0

    return dot(a, b) / (na * nb)


def build_graph(threshold):
    neighbors = [
        []
        for _ in range(N)
    ]

    edges = []

    for i in range(N):
        for j in range(i + 1, N):
            dist = distance(
                points[i],
                points[j],
            )

            if dist <= threshold:
                neighbors[i].append(j)
                neighbors[j].append(i)

                edges.append(
                    (i, j, dist)
                )

    return edges, neighbors


def analyze(threshold):
    edges, neighbors = build_graph(
        threshold
    )

    degrees = [
        len(x)
        for x in neighbors
    ]

    mean_degree = (
        sum(degrees) / N
        if N
        else 0.0
    )

    degree_std = math.sqrt(
        sum(
            (x - mean_degree) ** 2
            for x in degrees
        ) / N
    ) if N else 0.0

    degree_cv = (
        degree_std / mean_degree
        if mean_degree > EPS
        else 0.0
    )

    edge_lengths = [
        e[2]
        for e in edges
    ]

    mean_edge = (
        sum(edge_lengths)
        / len(edge_lengths)
        if edge_lengths
        else 0.0
    )

    edge_std = math.sqrt(
        sum(
            (x - mean_edge) ** 2
            for x in edge_lengths
        )
        / len(edge_lengths)
    ) if edge_lengths else 0.0

    edge_cv = (
        edge_std / mean_edge
        if mean_edge > EPS
        else 0.0
    )

    neighbor_sets = [
        set(x)
        for x in neighbors
    ]

    # --------------------------------------------------------------
    # Clustering
    # --------------------------------------------------------------

    local_clustering = []

    for i in range(N):
        ns = neighbors[i]
        k = len(ns)

        if k < 2:
            local_clustering.append(0.0)
            continue

        links = 0

        for a in range(k):
            for b in range(a + 1, k):
                if (
                    ns[b]
                    in neighbor_sets[ns[a]]
                ):
                    links += 1

        possible = k * (k - 1) / 2

        local_clustering.append(
            links / possible
        )

    clustering = (
        sum(local_clustering)
        / N
        if N
        else 0.0
    )

    # --------------------------------------------------------------
    # Period-8 topology
    # --------------------------------------------------------------

    motif_scores = []

    for i in range(
        N - PERIOD
    ):
        j = i + PERIOD

        degree_similarity = (
            min(
                degrees[i],
                degrees[j],
            )
            / max(
                degrees[i],
                degrees[j],
            )
            if max(
                degrees[i],
                degrees[j],
            ) > 0
            else 0.0
        )

        union = (
            neighbor_sets[i]
            | neighbor_sets[j]
        )

        intersection = (
            neighbor_sets[i]
            & neighbor_sets[j]
        )

        jaccard = (
            len(intersection)
            / len(union)
            if union
            else 0.0
        )

        motif_scores.append(
            0.5 * degree_similarity
            + 0.5 * jaccard
        )

    period8_topology = (
        sum(motif_scores)
        / len(motif_scores)
        if motif_scores
        else 0.0
    )

    # --------------------------------------------------------------
    # Period-8 translation
    # --------------------------------------------------------------

    translation_scores = []

    for i in range(
        N - PERIOD - 1
    ):
        j = i + PERIOD

        v1 = sub(
            points[i + 1],
            points[i],
        )

        v2 = sub(
            points[j + 1],
            points[j],
        )

        translation_scores.append(
            max(
                0.0,
                cosine(v1, v2),
            )
        )

    period8_translation = (
        sum(translation_scores)
        / len(translation_scores)
        if translation_scores
        else 0.0
    )

    # --------------------------------------------------------------
    # Simple-cubic fingerprint
    # --------------------------------------------------------------

    angles = []

    for center in range(N):
        ns = neighbors[center]

        for a in range(len(ns)):
            for b in range(a + 1, len(ns)):
                va = sub(
                    points[ns[a]],
                    points[center],
                )

                vb = sub(
                    points[ns[b]],
                    points[center],
                )

                na = norm(va)
                nb = norm(vb)

                if (
                    na <= EPS
                    or nb <= EPS
                ):
                    continue

                c = max(
                    -1.0,
                    min(
                        1.0,
                        dot(va, vb)
                        / (na * nb),
                    ),
                )

                angles.append(
                    math.degrees(
                        math.acos(c)
                    )
                )

    mean_angle = (
        sum(angles) / len(angles)
        if angles
        else 0.0
    )

    coordination_score = max(
        0.0,
        1.0
        - abs(
            mean_degree - 6.0
        ) / 6.0,
    )

    angle_score = max(
        0.0,
        1.0
        - abs(
            mean_angle - 90.0
        ) / 180.0,
    )

    bond_score = max(
        0.0,
        1.0 - edge_cv,
    )

    simple_cubic_score = (
        0.45 * coordination_score
        + 0.40 * angle_score
        + 0.15 * bond_score
    )

    return {
        "threshold": threshold,
        "multiplier": (
            threshold / base_threshold
        ),
        "bond_count": len(edges),
        "mean_degree": mean_degree,
        "degree_cv": degree_cv,
        "mean_edge": mean_edge,
        "edge_cv": edge_cv,
        "clustering": clustering,
        "mean_angle": mean_angle,
        "period8_topology": (
            period8_topology
        ),
        "period8_translation": (
            period8_translation
        ),
        "simple_cubic_score": (
            simple_cubic_score
        ),
    }


results = [
    analyze(
        base_threshold * multiplier
    )
    for multiplier in multipliers
]


print("=" * 72)
print(" OPENMIND / THRESHOLD ROBUSTNESS V25")
print("=" * 72)
print()
print(f"Layers: {N}")
print(
    f"Base threshold: "
    f"{base_threshold:.8f}"
)

print()
print("=== THRESHOLD SWEEP ===")

for r in results:
    print(
        f"x{r['multiplier']:.2f} "
        f"bonds={r['bond_count']:3d} "
        f"degree={r['mean_degree']:.4f} "
        f"cluster={r['clustering']:.4f} "
        f"period8={r['period8_topology']:.4f} "
        f"translation={r['period8_translation']:.4f} "
        f"SC={r['simple_cubic_score']:.4f}"
    )


# --------------------------------------------------------------
# Stability analysis
# --------------------------------------------------------------

period_values = [
    r["period8_topology"]
    for r in results
]

sc_values = [
    r["simple_cubic_score"]
    for r in results
]

cluster_values = [
    r["clustering"]
    for r in results
]


def mean(values):
    return (
        sum(values) / len(values)
        if values
        else 0.0
    )


def std(values):
    m = mean(values)

    return math.sqrt(
        sum(
            (x - m) ** 2
            for x in values
        )
        / len(values)
    ) if values else 0.0


period_mean = mean(period_values)
period_std = std(period_values)

sc_mean = mean(sc_values)
sc_std = std(sc_values)

cluster_mean = mean(cluster_values)
cluster_std = std(cluster_values)


# A signal is considered threshold-stable when it does
# not collapse across the central 0.90x–1.10x region.
central = [
    r
    for r in results
    if 0.90
    <= r["multiplier"]
    <= 1.10
]

central_period = [
    r["period8_topology"]
    for r in central
]

central_sc = [
    r["simple_cubic_score"]
    for r in central
]


central_period_min = min(
    central_period
)

central_sc_min = min(
    central_sc
)

period_stable = (
    central_period_min
    >= 0.25
)

sc_stable = (
    central_sc_min
    >= 0.75
)


if (
    period_stable
    and sc_stable
):
    classification = (
        "THRESHOLD_ROBUST_LATTICE_LIKE_STRUCTURE"
    )
elif period_stable:
    classification = (
        "THRESHOLD_ROBUST_PERIODIC_TOPOLOGY"
    )
elif sc_stable:
    classification = (
        "THRESHOLD_ROBUST_GEOMETRIC_LATTICE_FINGERPRINT"
    )
else:
    classification = (
        "THRESHOLD_SENSITIVE_STRUCTURE"
    )


print()
print("=== STABILITY ===")
print(
    f"period-8 mean = "
    f"{period_mean:.8f}"
)
print(
    f"period-8 std  = "
    f"{period_std:.8f}"
)
print(
    f"simple-cubic mean = "
    f"{sc_mean:.8f}"
)
print(
    f"simple-cubic std  = "
    f"{sc_std:.8f}"
)
print(
    f"central period-8 minimum = "
    f"{central_period_min:.8f}"
)
print(
    f"central simple-cubic minimum = "
    f"{central_sc_min:.8f}"
)

print()
print("=== CLASSIFICATION ===")
print(classification)


output = {
    "schema":
        "openmind.threshold_robustness.v25",
    "source":
        str(INPUT),
    "geometry_source":
        str(GEOMETRY),
    "layer_count":
        N,
    "period":
        PERIOD,
    "base_threshold":
        base_threshold,
    "multipliers":
        multipliers,
    "results":
        results,
    "stability": {
        "period8_mean":
            period_mean,
        "period8_std":
            period_std,
        "simple_cubic_mean":
            sc_mean,
        "simple_cubic_std":
            sc_std,
        "clustering_mean":
            cluster_mean,
        "clustering_std":
            cluster_std,
        "central_period8_min":
            central_period_min,
        "central_simple_cubic_min":
            central_sc_min,
        "period_stable":
            period_stable,
        "simple_cubic_stable":
            sc_stable,
    },
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
print(
    f"Output: {OUTPUT}"
)
print()
print(
    "THRESHOLD ROBUSTNESS ANALYSIS COMPLETE"
)
