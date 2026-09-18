import json
import math
import random
from pathlib import Path
from collections import Counter

INPUT = Path(
    "experiments/model_fractal/topology_lattice_v22.json"
)

GEOMETRY = Path(
    "experiments/model_fractal/normalized_geometry_v10.json"
)

OUTPUT = Path(
    "experiments/model_fractal/spatial_null_v24.json"
)

PERIOD = 8
TRIALS = 2000
SEED = 2401
EPS = 1e-12

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
print(" OPENMIND / SPATIAL NULL MODEL V24")
print("=" * 72)
print()
print(f"Layers: {N}")
print(f"Period: {PERIOD}")
print(f"Null trials: {TRIALS}")
print(f"Random seed: {SEED}")


def add(a, b):
    return tuple(
        x + y for x, y in zip(a, b)
    )


def sub(a, b):
    return tuple(
        x - y for x, y in zip(a, b)
    )


def scale(v, s):
    return tuple(
        x * s for x in v
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


def centroid(ps):
    return tuple(
        sum(p[k] for p in ps) / len(ps)
        for k in range(3)
    )


CENTER = centroid(points)

radii = [
    distance(p, CENTER)
    for p in points
]


def random_unit_vector():
    # Uniform direction on S^2.
    z = random.uniform(-1.0, 1.0)
    phi = random.uniform(
        0.0,
        2.0 * math.pi,
    )

    s = math.sqrt(
        max(0.0, 1.0 - z * z)
    )

    return (
        s * math.cos(phi),
        s * math.sin(phi),
        z,
    )


def radial_randomization():
    return [
        add(
            CENTER,
            scale(
                random_unit_vector(),
                r,
            ),
        )
        for r in radii
    ]


def build_graph(ps, threshold):
    edges = []

    neighbors = [
        []
        for _ in range(len(ps))
    ]

    for i in range(len(ps)):
        for j in range(i + 1, len(ps)):
            dist = distance(
                ps[i],
                ps[j],
            )

            if dist <= threshold:
                edges.append(
                    (i, j, dist)
                )

                neighbors[i].append(j)
                neighbors[j].append(i)

    return edges, neighbors


def graph_metrics(ps, threshold):
    edges, neighbors = build_graph(
        ps,
        threshold,
    )

    degrees = [
        len(ns)
        for ns in neighbors
    ]

    mean_degree = (
        sum(degrees) / len(degrees)
        if degrees
        else 0.0
    )

    degree_std = (
        math.sqrt(
            sum(
                (x - mean_degree) ** 2
                for x in degrees
            ) / len(degrees)
        )
        if degrees
        else 0.0
    )

    degree_cv = (
        degree_std / mean_degree
        if mean_degree > EPS
        else 0.0
    )

    lengths = [
        e[2]
        for e in edges
    ]

    mean_edge = (
        sum(lengths) / len(lengths)
        if lengths
        else 0.0
    )

    edge_std = (
        math.sqrt(
            sum(
                (x - mean_edge) ** 2
                for x in lengths
            ) / len(lengths)
        )
        if lengths
        else 0.0
    )

    edge_cv = (
        edge_std / mean_edge
        if mean_edge > EPS
        else 0.0
    )

    # --------------------------------------------------------------
    # Triangle count
    # --------------------------------------------------------------

    triangles = 0

    neighbor_sets = [
        set(ns)
        for ns in neighbors
    ]

    for i in range(len(ps)):
        ns = sorted(neighbor_sets[i])

        for a in range(len(ns)):
            for b in range(a + 1, len(ns)):
                if ns[b] in neighbor_sets[ns[a]]:
                    triangles += 1

    # --------------------------------------------------------------
    # Clustering
    # --------------------------------------------------------------

    local_clustering = []

    for i in range(len(ps)):
        ns = neighbors[i]
        k = len(ns)

        if k < 2:
            local_clustering.append(0.0)
            continue

        links = 0

        for a in range(k):
            for b in range(a + 1, k):
                if ns[b] in neighbor_sets[ns[a]]:
                    links += 1

        possible = k * (k - 1) / 2

        local_clustering.append(
            links / possible
        )

    clustering = (
        sum(local_clustering)
        / len(local_clustering)
        if local_clustering
        else 0.0
    )

    # --------------------------------------------------------------
    # Quadrilateral count
    # --------------------------------------------------------------

    squares = set()

    for a in range(len(ps)):
        for b in neighbors[a]:
            if b <= a:
                continue

            common = (
                neighbor_sets[a]
                & neighbor_sets[b]
            )

            common = sorted(common)

            for x in range(len(common)):
                for y in range(x + 1, len(common)):
                    c = common[x]
                    d4 = common[y]

                    if (
                        d4 in neighbor_sets[c]
                        and a in neighbor_sets[d4]
                    ):
                        squares.add(
                            tuple(
                                sorted(
                                    (
                                        a,
                                        b,
                                        c,
                                        d4,
                                    )
                                )
                            )
                        )

    # --------------------------------------------------------------
    # Period-8 topology
    # --------------------------------------------------------------

    motif_scores = []

    # Both trajectory steps must remain inside [0, len(ps)-1].
    # The shifted segment accesses j + 1, so exclude the final
    # incomplete period window.
    for i in range(
        len(ps) - PERIOD - 1
    ):
        j = i + PERIOD

        da = degrees[i]
        db = degrees[j]

        degree_similarity = (
            min(da, db) / max(da, db)
            if max(da, db) > 0
            else 0.0
        )

        na = neighbor_sets[i]
        nb = neighbor_sets[j]

        union = na | nb
        inter = na & nb

        jaccard = (
            len(inter) / len(union)
            if union
            else 0.0
        )

        motif_scores.append(
            0.5 * degree_similarity
            + 0.5 * jaccard
        )

    period_topology = (
        sum(motif_scores)
        / len(motif_scores)
        if motif_scores
        else 0.0
    )

    # --------------------------------------------------------------
    # Period-8 translation similarity
    # --------------------------------------------------------------

    translation_scores = []

    # The translated step also accesses j + 1.
    # Exclude the final incomplete period window.
    for i in range(
        len(ps) - PERIOD - 1
    ):
        j = i + PERIOD

        v1 = sub(
            ps[i + 1],
            ps[i],
        )

        v2 = sub(
            ps[j + 1],
            ps[j],
        )

        c = cosine(v1, v2)

        translation_scores.append(
            max(0.0, c)
        )

    translation = (
        sum(translation_scores)
        / len(translation_scores)
        if translation_scores
        else 0.0
    )

    # --------------------------------------------------------------
    # Simple-cubic fingerprint
    #
    # This deliberately uses the same broad idea as V21:
    # coordination near 6 and angles near 90 degrees.
    # --------------------------------------------------------------

    angle_values = []

    for center in range(len(ps)):
        ns = neighbors[center]

        for a in range(len(ns)):
            for b in range(a + 1, len(ns)):
                va = sub(
                    ps[ns[a]],
                    ps[center],
                )

                vb = sub(
                    ps[ns[b]],
                    ps[center],
                )

                na = norm(va)
                nb = norm(vb)

                if na <= EPS or nb <= EPS:
                    continue

                c = max(
                    -1.0,
                    min(
                        1.0,
                        dot(va, vb)
                        / (na * nb),
                    ),
                )

                angle_values.append(
                    math.degrees(
                        math.acos(c)
                    )
                )

    mean_angle = (
        sum(angle_values)
        / len(angle_values)
        if angle_values
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

    simple_cubic = (
        0.45 * coordination_score
        + 0.40 * angle_score
        + 0.15 * bond_score
    )

    return {
        "edge_count": len(edges),
        "mean_degree": mean_degree,
        "degree_cv": degree_cv,
        "mean_edge": mean_edge,
        "edge_cv": edge_cv,
        "triangle_count": triangles,
        "quadrilateral_count": len(squares),
        "clustering": clustering,
        "period8_topology": period_topology,
        "period8_translation": translation,
        "simple_cubic_score": simple_cubic,
        "mean_angle": mean_angle,
    }


# ----------------------------------------------------------------------
# Observed geometry
# ----------------------------------------------------------------------

bond_threshold = float(
    d.get(
        "bond_threshold",
        2.08934562,
    )
)

observed = graph_metrics(
    points,
    bond_threshold,
)

print()
print("=== OBSERVED SPATIAL GEOMETRY ===")
print(
    f"bond count             = "
    f"{observed['edge_count']}"
)
print(
    f"mean degree            = "
    f"{observed['mean_degree']:.8f}"
)
print(
    f"degree CV              = "
    f"{observed['degree_cv']:.8f}"
)
print(
    f"mean edge              = "
    f"{observed['mean_edge']:.8f}"
)
print(
    f"edge CV                = "
    f"{observed['edge_cv']:.8f}"
)
print(
    f"clustering             = "
    f"{observed['clustering']:.8f}"
)
print(
    f"triangles              = "
    f"{observed['triangle_count']}"
)
print(
    f"quadrilaterals         = "
    f"{observed['quadrilateral_count']}"
)
print(
    f"period-8 topology      = "
    f"{observed['period8_topology']:.8f}"
)
print(
    f"period-8 translation   = "
    f"{observed['period8_translation']:.8f}"
)
print(
    f"simple-cubic score     = "
    f"{observed['simple_cubic_score']:.8f}"
)


# ----------------------------------------------------------------------
# Spatial null
# ----------------------------------------------------------------------

null_metrics = {
    key: []
    for key in observed
}

for trial in range(TRIALS):

    randomized = radial_randomization()

    metrics = graph_metrics(
        randomized,
        bond_threshold,
    )

    for key, value in metrics.items():
        null_metrics[key].append(value)


def summarize(values, observed_value):
    mean_value = (
        sum(values) / len(values)
        if values
        else 0.0
    )

    variance = (
        sum(
            (x - mean_value) ** 2
            for x in values
        ) / len(values)
        if values
        else 0.0
    )

    std_value = math.sqrt(
        variance
    )

    if std_value > EPS:
        z = (
            observed_value
            - mean_value
        ) / std_value
    else:
        z = 0.0

    # Two-sided empirical permutation probability.
    extreme = sum(
        abs(x - mean_value)
        >= abs(observed_value - mean_value)
        for x in values
    )

    p = (
        (extreme + 1)
        / (len(values) + 1)
    )

    return {
        "observed": observed_value,
        "null_mean": mean_value,
        "null_std": std_value,
        "z_score": z,
        "empirical_p_two_sided": p,
    }


statistics = {
    key: summarize(
        null_metrics[key],
        observed[key],
    )
    for key in observed
}


print()
print("=== RADIAL-PRESERVING SPATIAL NULL ===")

for key in (
    "period8_topology",
    "period8_translation",
    "simple_cubic_score",
    "clustering",
    "edge_cv",
):
    s = statistics[key]

    print(
        f"{key:24s} "
        f"obs={s['observed']:.8f} "
        f"null={s['null_mean']:.8f} "
        f"z={s['z_score']:.5f} "
        f"p={s['empirical_p_two_sided']:.5f}"
    )


# ----------------------------------------------------------------------
# Conservative interpretation
# ----------------------------------------------------------------------

periodic_p = min(
    statistics["period8_topology"][
        "empirical_p_two_sided"
    ],
    statistics["period8_translation"][
        "empirical_p_two_sided"
    ],
)

lattice_p = (
    statistics["simple_cubic_score"][
        "empirical_p_two_sided"
    ]
)

if (
    periodic_p < 0.01
    and lattice_p < 0.01
):
    classification = (
        "SPATIALLY_SIGNIFICANT_LATTICE_LIKE_STRUCTURE"
    )
elif periodic_p < 0.05:
    classification = (
        "SPATIAL_PERIODICITY_SIGNAL_REQUIRES_CONFIRMATION"
    )
elif lattice_p < 0.05:
    classification = (
        "SPATIAL_LATTICE_FINGERPRINT_REQUIRES_CONFIRMATION"
    )
else:
    classification = (
        "NO_SPATIALLY_SIGNIFICANT_LATTICE_STRUCTURE"
    )


print()
print("=== CLASSIFICATION ===")
print(classification)


output = {
    "schema":
        "openmind.spatial_null.v24",
    "source":
        str(INPUT),
    "geometry_source":
        str(GEOMETRY),
    "layer_count":
        N,
    "period":
        PERIOD,
    "trials":
        TRIALS,
    "seed":
        SEED,
    "bond_threshold":
        bond_threshold,
    "center":
        CENTER,
    "radii":
        radii,
    "observed":
        observed,
    "null_statistics":
        statistics,
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
    "SPATIAL NULL MODEL COMPLETE"
)
