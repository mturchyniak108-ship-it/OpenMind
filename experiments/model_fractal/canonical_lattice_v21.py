import json
import math
from pathlib import Path
from collections import Counter
from statistics import mean

INPUT = Path(
    "experiments/model_fractal/material_compatibility_v20.json"
)

OUTPUT = Path(
    "experiments/model_fractal/canonical_lattice_v21.json"
)

EPS = 1e-12

d = json.loads(INPUT.read_text())

# V20 retains the source geometry indirectly. Load the V10 geometry
# because it is the canonical normalized trajectory representation.
geometry_path = Path(
    "experiments/model_fractal/normalized_geometry_v10.json"
)

g = json.loads(geometry_path.read_text())

raw_points = g["layer_coordinates"]

points = [
    (
        float(p["x"]),
        float(p["y"]),
        float(p["z"]),
    )
    for p in raw_points
]

N = len(points)

print("=" * 72)
print(" OPENMIND / CANONICAL LATTICE FINGERPRINT V21")
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


def angle(a, b):
    c = max(-1.0, min(1.0, cosine(a, b)))
    return math.degrees(math.acos(c))


# ----------------------------------------------------------------------
# Build the same bond graph used by V20.
#
# Use V20's threshold so V21 is directly comparable with the material
# compatibility experiment.
# ----------------------------------------------------------------------

bond_threshold = float(
    d.get("bond_threshold", 0.0)
)

if bond_threshold <= EPS:
    # Conservative fallback derived from the trajectory.
    pair_distances = [
        distance(points[i], points[j])
        for i in range(N)
        for j in range(i + 1, N)
    ]

    pair_distances.sort()

    # Use the lower geometric neighborhood rather than the largest
    # distances in the trajectory.
    cutoff_index = max(
        0,
        min(
            len(pair_distances) - 1,
            int(len(pair_distances) * 0.18),
        ),
    )

    bond_threshold = pair_distances[cutoff_index]


edges = []

for i in range(N):
    for j in range(i + 1, N):
        dist = distance(points[i], points[j])

        if dist <= bond_threshold:
            edges.append(
                {
                    "i": i,
                    "j": j,
                    "distance": dist,
                }
            )


neighbors = [[] for _ in range(N)]

for e in edges:
    neighbors[e["i"]].append(e["j"])
    neighbors[e["j"]].append(e["i"])


coordination = [
    len(x)
    for x in neighbors
]


# ----------------------------------------------------------------------
# Bond statistics
# ----------------------------------------------------------------------

bond_lengths = [
    e["distance"]
    for e in edges
]

mean_bond = (
    sum(bond_lengths) / len(bond_lengths)
    if bond_lengths
    else 0.0
)

bond_rms = (
    math.sqrt(
        sum(x * x for x in bond_lengths)
        / len(bond_lengths)
    )
    if bond_lengths
    else 0.0
)

bond_std = (
    math.sqrt(
        sum((x - mean_bond) ** 2 for x in bond_lengths)
        / len(bond_lengths)
    )
    if bond_lengths
    else 0.0
)

bond_cv = (
    bond_std / mean_bond
    if mean_bond > EPS
    else 0.0
)


# ----------------------------------------------------------------------
# Local bond angles
# ----------------------------------------------------------------------

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

            if norm(va) > EPS and norm(vb) > EPS:
                angles.append(angle(va, vb))


mean_angle = (
    sum(angles) / len(angles)
    if angles
    else 0.0
)


# ----------------------------------------------------------------------
# Coordination histogram
# ----------------------------------------------------------------------

coord_histogram = dict(
    sorted(
        Counter(coordination).items()
    )
)


# ----------------------------------------------------------------------
# Canonical structural signatures
#
# These are idealized fingerprints, not claims that the structure is
# one of these materials.
# ----------------------------------------------------------------------

canonical = {
    "simple_cubic": {
        "coordination": 6.0,
        "angle": 90.0,
    },
    "bcc": {
        "coordination": 8.0,
        "angle": 70.5288,
    },
    "fcc": {
        "coordination": 12.0,
        "angle": 60.0,
    },
    "diamond": {
        "coordination": 4.0,
        "angle": 109.4712,
    },
    "graphene": {
        "coordination": 3.0,
        "angle": 120.0,
    },
    "hexagonal_close_packed": {
        "coordination": 12.0,
        "angle": 60.0,
    },
}


# ----------------------------------------------------------------------
# Fingerprint scoring
#
# Coordination and angle are normalized independently.
# ----------------------------------------------------------------------

fingerprints = []

for name, target in canonical.items():

    coordination_error = abs(
        mean(coordination)
        - target["coordination"]
    ) / max(
        target["coordination"],
        1.0,
    )

    angle_error = abs(
        mean_angle
        - target["angle"]
    ) / 180.0

    bond_uniformity = max(
        0.0,
        1.0 - bond_cv,
    )

    coordination_score = max(
        0.0,
        1.0 - coordination_error,
    )

    angle_score = max(
        0.0,
        1.0 - angle_error,
    )

    score = (
        0.45 * coordination_score
        + 0.40 * angle_score
        + 0.15 * bond_uniformity
    )

    fingerprints.append(
        {
            "lattice": name,
            "score": score,
            "coordination_error": coordination_error,
            "angle_error": angle_error,
            "coordination_score": coordination_score,
            "angle_score": angle_score,
            "bond_uniformity": bond_uniformity,
        }
    )


fingerprints.sort(
    key=lambda x: x["score"],
    reverse=True,
)


# ----------------------------------------------------------------------
# Ring statistics
#
# Count triangles and quadrilaterals in the bond graph.
# ----------------------------------------------------------------------

triangles = set()
squares = set()

for i in range(N):

    ns = set(neighbors[i])

    for j in ns:
        if j <= i:
            continue

        common = ns.intersection(neighbors[j])

        for k in common:
            if k > j:
                triangles.add(
                    tuple(sorted((i, j, k)))
                )


# Simple 4-cycle detection.
for a in range(N):
    for b in neighbors[a]:

        if b <= a:
            continue

        common_ab = set(neighbors[a]).intersection(
            neighbors[b]
        )

        for c in common_ab:
            if c <= b:
                continue

            for d4 in set(neighbors[c]).intersection(
                neighbors[b]
            ):
                if d4 <= c or d4 == a:
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
# Nearest-neighbor shell statistics
# ----------------------------------------------------------------------

shell = {}

for i in range(N):

    distances = sorted(
        distance(points[i], points[j])
        for j in range(N)
        if j != i
    )

    if distances:
        nearest = distances[0]

        key = round(nearest, 6)

        shell[key] = shell.get(key, 0) + 1


# ----------------------------------------------------------------------
# Structural classification
# ----------------------------------------------------------------------

best = fingerprints[0]

if best["score"] >= 0.80:
    classification = (
        "STRONG_CANONICAL_LATTICE_MATCH"
    )
elif best["score"] >= 0.65:
    classification = (
        "MODERATE_CANONICAL_LATTICE_MATCH"
    )
elif best["score"] >= 0.50:
    classification = (
        "WEAK_CANONICAL_LATTICE_MATCH"
    )
else:
    classification = (
        "NONSTANDARD_PERIODIC_OR_AMORPHOUS_GEOMETRY"
    )


print()
print("=== BOND NETWORK ===")
print(f"bond threshold = {bond_threshold:.8f}")
print(f"bond count     = {len(edges)}")
print(
    f"mean bond      = {mean_bond:.8f}"
)
print(
    f"bond CV        = {bond_cv:.8f}"
)


print()
print("=== COORDINATION ===")

for k, v in coord_histogram.items():
    print(
        f"coordination={k:2d} "
        f"count={v:2d}"
    )

print(
    f"mean coordination = "
    f"{sum(coordination) / N:.8f}"
)


print()
print("=== ANGULAR GEOMETRY ===")
print(
    f"angle count = {len(angles)}"
)
print(
    f"mean angle  = {mean_angle:.8f}°"
)


print()
print("=== RING STRUCTURE ===")
print(
    f"triangles = {len(triangles)}"
)
print(
    f"quadrilaterals = {len(squares)}"
)


print()
print("=== CANONICAL LATTICE FINGERPRINTS ===")

for f in fingerprints:
    print(
        f"{f['lattice']:24s} "
        f"score={f['score']:.8f} "
        f"coord_err={f['coordination_error']:.6f} "
        f"angle_err={f['angle_error']:.6f}"
    )


print()
print("=== BEST MATCH ===")
print(
    f"lattice = {best['lattice']}"
)
print(
    f"score   = {best['score']:.8f}"
)


print()
print("=== CLASSIFICATION ===")
print(classification)


output = {
    "schema": "openmind.canonical_lattice_fingerprint.v21",
    "source": str(INPUT),
    "geometry_source": str(geometry_path),
    "layer_count": N,
    "bond_threshold": bond_threshold,
    "bond_count": len(edges),
    "mean_bond": mean_bond,
    "bond_rms": bond_rms,
    "bond_std": bond_std,
    "bond_cv": bond_cv,
    "coordination_histogram": {
        str(k): v
        for k, v in coord_histogram.items()
    },
    "mean_coordination": (
        sum(coordination) / N
        if N
        else 0.0
    ),
    "angle_count": len(angles),
    "mean_angle": mean_angle,
    "triangle_count": len(triangles),
    "quadrilateral_count": len(squares),
    "canonical_fingerprints": fingerprints,
    "best_match": best,
    "classification": classification,
    "nearest_neighbor_shells": shell,
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
    "CANONICAL LATTICE FINGERPRINT COMPLETE"
)
