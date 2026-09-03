import json
import math
from pathlib import Path
from collections import Counter

INPUT = Path(
    "experiments/model_fractal/canonical_lattice_v21.json"
)

GEOMETRY = Path(
    "experiments/model_fractal/normalized_geometry_v10.json"
)

OUTPUT = Path(
    "experiments/model_fractal/topology_lattice_v22.json"
)

EPS = 1e-12
PERIOD = 8

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
print(" OPENMIND / TOPOLOGY LATTICE ANALYSIS V22")
print("=" * 72)

print()
print(f"Layers: {N}")


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


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


def mean(values):
    return (
        sum(values) / len(values)
        if values
        else 0.0
    )


def rms(values):
    return (
        math.sqrt(
            sum(x * x for x in values)
            / len(values)
        )
        if values
        else 0.0
    )


# ----------------------------------------------------------------------
# Reconstruct V21 bond graph.
# ----------------------------------------------------------------------

threshold = float(
    d["bond_threshold"]
)

edges = []

for i in range(N):
    for j in range(i + 1, N):

        dist = distance(
            points[i],
            points[j],
        )

        if dist <= threshold:
            edges.append((i, j, dist))


neighbors = [
    set()
    for _ in range(N)
]

for i, j, dist in edges:
    neighbors[i].add(j)
    neighbors[j].add(i)


degrees = [
    len(n)
    for n in neighbors
]


# ----------------------------------------------------------------------
# Graph statistics
# ----------------------------------------------------------------------

degree_histogram = dict(
    sorted(
        Counter(degrees).items()
    )
)

degree_mean = mean(degrees)

degree_std = math.sqrt(
    mean(
        [
            (x - degree_mean) ** 2
            for x in degrees
        ]
    )
)

degree_cv = (
    degree_std / degree_mean
    if degree_mean > EPS
    else 0.0
)


# ----------------------------------------------------------------------
# Edge-length distribution
# ----------------------------------------------------------------------

edge_lengths = [
    e[2]
    for e in edges
]

edge_mean = mean(edge_lengths)

edge_std = math.sqrt(
    mean(
        [
            (x - edge_mean) ** 2
            for x in edge_lengths
        ]
    )
)

edge_cv = (
    edge_std / edge_mean
    if edge_mean > EPS
    else 0.0
)


# ----------------------------------------------------------------------
# Local neighborhood similarity
#
# Compare degree signatures of vertices separated by PERIOD.
# ----------------------------------------------------------------------

period_pairs = []

for i in range(N - PERIOD):

    j = i + PERIOD

    a = sorted(
        degrees[k]
        for k in neighbors[i]
    )

    b = sorted(
        degrees[k]
        for k in neighbors[j]
    )

    m = max(len(a), len(b))

    if m == 0:
        similarity = 1.0
    else:
        a = a + [0] * (m - len(a))
        b = b + [0] * (m - len(b))

        error = mean(
            [
                abs(x - y)
                for x, y in zip(a, b)
            ]
        )

        similarity = max(
            0.0,
            1.0 - error / 8.0,
        )

    period_pairs.append(similarity)


period8_topology = mean(
    period_pairs
)


# ----------------------------------------------------------------------
# Triangle count
# ----------------------------------------------------------------------

triangles = set()

for i in range(N):

    ns = neighbors[i]

    for j in ns:

        if j <= i:
            continue

        common = (
            ns.intersection(
                neighbors[j]
            )
        )

        for k in common:

            if k > j:
                triangles.add(
                    tuple(
                        sorted(
                            (i, j, k)
                        )
                    )
                )


# ----------------------------------------------------------------------
# Four-cycles
# ----------------------------------------------------------------------

squares = set()

for a in range(N):

    for b in neighbors[a]:

        if b <= a:
            continue

        common = (
            neighbors[a]
            .intersection(
                neighbors[b]
            )
        )

        for c in common:

            if c <= b:
                continue

            for d4 in (
                neighbors[c]
                .intersection(
                    neighbors[b]
                )
            ):

                if d4 <= c:
                    continue

                if d4 == a:
                    continue

                if a in neighbors[d4]:

                    squares.add(
                        tuple(
                            sorted(
                                (a, b, c, d4)
                            )
                        )
                    )


# ----------------------------------------------------------------------
# Local clustering coefficient
# ----------------------------------------------------------------------

clustering = []

for i in range(N):

    ns = list(neighbors[i])

    k = len(ns)

    if k < 2:
        clustering.append(0.0)
        continue

    possible = k * (k - 1) / 2

    actual = 0

    for a in range(k):

        for b in range(a + 1, k):

            if ns[b] in neighbors[ns[a]]:
                actual += 1

    clustering.append(
        actual / possible
    )


mean_clustering = mean(
    clustering
)


# ----------------------------------------------------------------------
# Translation geometry
#
# Compare displacement vectors separated by period 8.
# ----------------------------------------------------------------------

translation_cosines = []

translation_scale = []

# Both shifted segments must remain inside the trajectory.
for i in range(N - PERIOD - 1):

    a = sub(
        points[i + PERIOD],
        points[i],
    )

    b = sub(
        points[i + PERIOD + 1],
        points[i + 1],
    )

    na = norm(a)
    nb = norm(b)

    if na > EPS and nb > EPS:

        translation_cosines.append(
            cosine(a, b)
        )

        translation_scale.append(
            min(na, nb)
            / max(na, nb)
        )


translation_score = (
    mean(translation_cosines)
    * mean(translation_scale)
    if translation_cosines
    else 0.0
)


# ----------------------------------------------------------------------
# Local environment fingerprint
#
# Each node is represented by its sorted neighboring degree sequence.
# Repeated environments indicate structural motifs.
# ----------------------------------------------------------------------

environment_counter = Counter()

for i in range(N):

    signature = tuple(
        sorted(
            degrees[j]
            for j in neighbors[i]
        )
    )

    environment_counter[signature] += 1


repeated_environments = [
    {
        "signature": list(signature),
        "count": count,
    }
    for signature, count
    in environment_counter.items()
    if count > 1
]

repeated_environment_fraction = (
    sum(
        x["count"]
        for x in repeated_environments
    )
    / N
    if N
    else 0.0
)


# ----------------------------------------------------------------------
# Canonical topology expectations
#
# These are graph-level signatures, deliberately separate from V21's
# mean-angle scoring.
# ----------------------------------------------------------------------

canonical = {

    "simple_cubic": {
        "degree": 6,
        "triangles": 0,
        "squares": 1,
    },

    "bcc": {
        "degree": 8,
        "triangles": 0,
        "squares": 0,
    },

    "diamond": {
        "degree": 4,
        "triangles": 0,
        "squares": 0,
    },

    "graphene": {
        "degree": 3,
        "triangles": 0,
        "squares": 0,
    },

}


# ----------------------------------------------------------------------
# Topology fingerprints
# ----------------------------------------------------------------------

fingerprints = []

triangle_density = (
    len(triangles) / N
    if N
    else 0.0
)

square_density = (
    len(squares) / N
    if N
    else 0.0
)


for name, target in canonical.items():

    degree_score = max(
        0.0,
        1.0
        - abs(
            degree_mean
            - target["degree"]
        ) / 8.0,
    )

    # The actual graph has many finite-size cycles, so compare cycle
    # presence gently rather than demanding zero.
    if target["triangles"] == 0:
        triangle_score = (
            1.0
            if triangle_density == 0
            else max(
                0.0,
                1.0
                - triangle_density / 4.0,
            )
        )
    else:
        triangle_score = 1.0

    if target["squares"] == 0:
        square_score = (
            1.0
            if square_density == 0
            else max(
                0.0,
                1.0
                - square_density / 4.0,
            )
        )
    else:
        # Simple cubic networks contain many 4-cycles.
        square_score = min(
            1.0,
            square_density,
        )

    score = (
        0.50 * degree_score
        + 0.25 * triangle_score
        + 0.25 * square_score
    )

    fingerprints.append(
        {
            "lattice": name,
            "score": score,
            "degree_score": degree_score,
            "triangle_score": triangle_score,
            "square_score": square_score,
        }
    )


fingerprints.sort(
    key=lambda x: x["score"],
    reverse=True,
)


# ----------------------------------------------------------------------
# Combined structural evidence
# ----------------------------------------------------------------------

best = fingerprints[0]

motif_score = (
    0.40 * period8_topology
    + 0.25 * translation_score
    + 0.20 * repeated_environment_fraction
    + 0.15 * max(
        0.0,
        1.0 - degree_cv,
    )
)

combined_score = (
    0.60 * best["score"]
    + 0.40 * motif_score
)


if combined_score >= 0.75:
    classification = (
        "STRONG_PERIODIC_LATTICE_TOPOLOGY"
    )
elif combined_score >= 0.60:
    classification = (
        "MODERATE_PERIODIC_LATTICE_TOPOLOGY"
    )
elif combined_score >= 0.45:
    classification = (
        "WEAK_LATTICE_TOPOLOGY"
    )
else:
    classification = (
        "NONSTANDARD_GRAPH_GEOMETRY"
    )


print()
print("=== GRAPH STATISTICS ===")
print(
    f"bond count          = {len(edges)}"
)
print(
    f"mean degree         = {degree_mean:.8f}"
)
print(
    f"degree CV           = {degree_cv:.8f}"
)
print(
    f"mean edge length    = {edge_mean:.8f}"
)
print(
    f"edge CV             = {edge_cv:.8f}"
)


print()
print("=== DEGREE HISTOGRAM ===")

for degree, count in degree_histogram.items():
    print(
        f"degree={degree:2d} "
        f"count={count:2d}"
    )


print()
print("=== CYCLE STRUCTURE ===")
print(
    f"triangles           = {len(triangles)}"
)
print(
    f"quadrilaterals      = {len(squares)}"
)
print(
    f"mean clustering     = {mean_clustering:.8f}"
)


print()
print("=== PERIOD-8 TOPOLOGY ===")
print(
    f"topology similarity = "
    f"{period8_topology:.8f}"
)
print(
    f"translation score   = "
    f"{translation_score:.8f}"
)


print()
print("=== REPEATED ENVIRONMENTS ===")
print(
    f"unique environments = "
    f"{len(environment_counter)}"
)
print(
    f"repeated fraction   = "
    f"{repeated_environment_fraction:.8f}"
)


print()
print("=== TOPOLOGY FINGERPRINTS ===")

for f in fingerprints:
    print(
        f"{f['lattice']:16s} "
        f"score={f['score']:.8f}"
    )


print()
print("=== COMBINED STRUCTURAL SCORE ===")
print(
    f"canonical topology = "
    f"{best['score']:.8f}"
)
print(
    f"motif structure    = "
    f"{motif_score:.8f}"
)
print(
    f"combined           = "
    f"{combined_score:.8f}"
)


print()
print("=== CLASSIFICATION ===")
print(classification)


output = {
    "schema": "openmind.topology_lattice_analysis.v22",
    "source": str(INPUT),
    "geometry_source": str(GEOMETRY),
    "layer_count": N,
    "bond_threshold": threshold,
    "bond_count": len(edges),
    "degree_histogram": {
        str(k): v
        for k, v in degree_histogram.items()
    },
    "mean_degree": degree_mean,
    "degree_cv": degree_cv,
    "mean_edge_length": edge_mean,
    "edge_cv": edge_cv,
    "triangle_count": len(triangles),
    "quadrilateral_count": len(squares),
    "mean_clustering": mean_clustering,
    "period8_topology_similarity": period8_topology,
    "period8_translation_score": translation_score,
    "unique_environment_count": len(
        environment_counter
    ),
    "repeated_environment_fraction":
        repeated_environment_fraction,
    "canonical_topology_fingerprints":
        fingerprints,
    "best_canonical_match": best,
    "motif_score": motif_score,
    "combined_score": combined_score,
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
    "TOPOLOGY LATTICE ANALYSIS COMPLETE"
)
