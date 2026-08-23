import json
import math
import random
from pathlib import Path

RAW = Path(
    "experiments/model_fractal/crystal_raw_lattice_v15.json"
)

MOTIF = Path(
    "experiments/model_fractal/motif_graph_v19.json"
)

OUTPUT = Path(
    "experiments/model_fractal/material_compatibility_v20.json"
)

EPS = 1e-12
GRAPHENE_ANGLE = math.radians(120.0)
GRAPHENE_COORDINATION = 3
PERIOD = 8

raw = json.loads(RAW.read_text())
motif = json.loads(MOTIF.read_text())

print("=" * 72)
print(" OPENMIND / MATERIAL COMPATIBILITY V20")
print("=" * 72)

# V15 contains the raw lattice diagnostics, but V19 contains the
# authoritative normalized trajectory through its source reference.
source = Path(
    "experiments/model_fractal/normalized_geometry_v10.json"
)

geometry = json.loads(source.read_text())

points = [
    (
        float(p["x"]),
        float(p["y"]),
        float(p["z"]),
    )
    for p in geometry["layer_coordinates"]
]

N = len(points)

print()
print(f"Layers: {N}")
print(f"Candidate motif period: {PERIOD}")


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

    return max(
        -1.0,
        min(
            1.0,
            dot(a, b) / (na * nb),
        ),
    )


def angle(a, b):
    return math.acos(cosine(a, b))


# ----------------------------------------------------------------------
# Pairwise geometry
# ----------------------------------------------------------------------

pairs = []

for i in range(N):
    for j in range(i + 1, N):
        d = distance(points[i], points[j])

        if d > EPS:
            pairs.append((i, j, d))


distances = sorted(
    x[2]
    for x in pairs
)

# Use the same lower-neighborhood philosophy as V19.
threshold_index = max(
    0,
    int(len(distances) * 0.20) - 1,
)

bond_threshold = distances[threshold_index]


bonds = [
    (i, j, d)
    for i, j, d in pairs
    if d <= bond_threshold + EPS
]


print()
print("=== OPENMIND BOND NETWORK ===")
print(
    f"bond threshold = "
    f"{bond_threshold:.8f}"
)
print(
    f"bond count     = "
    f"{len(bonds)}"
)


# ----------------------------------------------------------------------
# Coordination
# ----------------------------------------------------------------------

neighbors = {
    i: []
    for i in range(N)
}

for i, j, d in bonds:
    neighbors[i].append((j, d))
    neighbors[j].append((i, d))


coordination = [
    len(neighbors[i])
    for i in range(N)
]

mean_coordination = (
    sum(coordination) / N
    if N
    else 0.0
)


coordination_error = abs(
    mean_coordination
    - GRAPHENE_COORDINATION
) / GRAPHENE_COORDINATION


# ----------------------------------------------------------------------
# Bond lengths
# ----------------------------------------------------------------------

bond_lengths = [
    d
    for _, _, d in bonds
]

mean_bond = (
    sum(bond_lengths) / len(bond_lengths)
    if bond_lengths
    else 0.0
)

bond_rms = (
    math.sqrt(
        sum(
            (d - mean_bond) ** 2
            for d in bond_lengths
        )
        / len(bond_lengths)
    )
    if bond_lengths
    else 0.0
)

bond_cv = (
    bond_rms / mean_bond
    if mean_bond > EPS
    else 0.0
)


# ----------------------------------------------------------------------
# Bond-angle distribution
# ----------------------------------------------------------------------

angles = []

for center in range(N):

    ns = neighbors[center]

    for a in range(len(ns)):
        for b in range(a + 1, len(ns)):

            pa = points[ns[a][0]]
            pb = points[ns[b][0]]
            pc = points[center]

            va = sub(pa, pc)
            vb = sub(pb, pc)

            angles.append(
                angle(va, vb)
            )


angle_error_values = [
    abs(a - GRAPHENE_ANGLE)
    for a in angles
]

mean_angle_error = (
    sum(angle_error_values)
    / len(angle_error_values)
    if angle_error_values
    else math.pi
)

mean_angle_degrees = (
    math.degrees(
        sum(angles) / len(angles)
    )
    if angles
    else 0.0
)

angle_error_degrees = math.degrees(
    mean_angle_error
)


# ----------------------------------------------------------------------
# Optimal uniform scaling against a graphene C-C reference.
#
# This deliberately tests scale only. It does NOT rotate, flatten,
# orthogonalize, or otherwise deform the OpenMind structure.
# ----------------------------------------------------------------------

GRAPHENE_CC = 1.42

optimal_scale = (
    GRAPHENE_CC / mean_bond
    if mean_bond > EPS
    else 1.0
)

scaled_mean_bond = (
    mean_bond * optimal_scale
)

scaled_bond_rms = (
    bond_rms * optimal_scale
)


# ----------------------------------------------------------------------
# Period-8 structural compatibility
# ----------------------------------------------------------------------

motif_pairs = []

# Both the source segment (i -> i+1) and the
# period-shifted segment (j -> j+1) must remain
# inside the closed trajectory.
for i in range(N - PERIOD - 1):
    j = i + PERIOD

    d1 = distance(
        points[i],
        points[i + 1],
    )

    d2 = distance(
        points[j],
        points[j + 1],
    )

    if d1 > EPS and d2 > EPS:
        ratio = min(d1, d2) / max(d1, d2)
    else:
        ratio = 0.0

    motif_pairs.append(ratio)


period8_bond_similarity = (
    sum(motif_pairs) / len(motif_pairs)
    if motif_pairs
    else 0.0
)


# ----------------------------------------------------------------------
# Graphene-like local topology
#
# A site is considered graphene-compatible only when its coordination
# is exactly three. This prevents a good geometric score from hiding
# a fundamentally incompatible graph.
# ----------------------------------------------------------------------

graphene_sites = sum(
    1
    for c in coordination
    if c == 3
)

graphene_coordination_fraction = (
    graphene_sites / N
    if N
    else 0.0
)


# ----------------------------------------------------------------------
# Component scores
# ----------------------------------------------------------------------

coordination_score = max(
    0.0,
    1.0 - coordination_error,
)

angle_score = max(
    0.0,
    1.0
    - mean_angle_error / math.pi,
)

bond_uniformity_score = max(
    0.0,
    1.0 - bond_cv,
)

topology_score = (
    graphene_coordination_fraction
)

motif_score = (
    period8_bond_similarity
)


overall_score = (
    0.25 * coordination_score
    + 0.20 * angle_score
    + 0.15 * bond_uniformity_score
    + 0.25 * topology_score
    + 0.15 * motif_score
)


# ----------------------------------------------------------------------
# Null model
#
# Randomly permute point order while retaining the exact same
# coordinates and bond-distance threshold. This asks whether the
# period-8 bond recurrence survives destruction of layer ordering.
# ----------------------------------------------------------------------

random.seed(1729)

observed = period8_bond_similarity

null_values = []

for _ in range(500):

    order = list(range(N))
    random.shuffle(order)

    local = []

    # Both shifted segments must remain inside the
    # randomized trajectory ordering.
    for i in range(N - PERIOD - 1):
        a = order[i]
        b = order[i + PERIOD]

        d1 = distance(
            points[a],
            points[b],
        )

        c = order[i + 1]
        e = order[i + PERIOD + 1]

        d2 = distance(
            points[c],
            points[e],
        )

        if d1 > EPS and d2 > EPS:
            local.append(
                min(d1, d2)
                / max(d1, d2)
            )

    if local:
        null_values.append(
            sum(local) / len(local)
        )


null_mean = (
    sum(null_values) / len(null_values)
    if null_values
    else 0.0
)

null_std = (
    math.sqrt(
        sum(
            (x - null_mean) ** 2
            for x in null_values
        )
        / len(null_values)
    )
    if null_values
    else 0.0
)

null_z = (
    (observed - null_mean) / null_std
    if null_std > EPS
    else 0.0
)


# ----------------------------------------------------------------------
# Classification
# ----------------------------------------------------------------------

if (
    topology_score >= 0.75
    and angle_score >= 0.75
    and null_z >= 3.0
):
    classification = "GRAPHENE_COMPATIBLE"

elif (
    topology_score >= 0.40
    and motif_score >= 0.70
    and null_z >= 2.0
):
    classification = "PARTIAL_TOPOLOGICAL_COMPATIBILITY"

elif (
    motif_score >= 0.70
    and null_z >= 2.0
):
    classification = "RECURRING_NON_GRAPHENE_MOTIF"

else:
    classification = "GRAPHENE_INCOMPATIBLE"


print()
print("=== GRAPHENE COMPARISON ===")
print(
    f"mean coordination = "
    f"{mean_coordination:.8f}"
)
print(
    f"graphene target    = "
    f"{GRAPHENE_COORDINATION:.8f}"
)
print(
    f"coordination error = "
    f"{coordination_error:.8f}"
)
print(
    f"sites with coord=3 = "
    f"{graphene_coordination_fraction:.8f}"
)

print()
print("=== ANGLE COMPATIBILITY ===")
print(
    f"mean angle = "
    f"{mean_angle_degrees:.8f}°"
)
print(
    f"graphene target = 120.00000000°"
)
print(
    f"mean angular error = "
    f"{angle_error_degrees:.8f}°"
)

print()
print("=== BOND GEOMETRY ===")
print(
    f"mean raw bond = "
    f"{mean_bond:.8f}"
)
print(
    f"optimal scale = "
    f"{optimal_scale:.8f}"
)
print(
    f"scaled bond = "
    f"{scaled_mean_bond:.8f}"
)
print(
    f"bond CV = "
    f"{bond_cv:.8f}"
)

print()
print("=== PERIOD-8 COMPATIBILITY ===")
print(
    f"observed = "
    f"{observed:.8f}"
)
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
    f"{null_z:.8f}"
)

print()
print("=== MATERIAL SCORES ===")
print(
    f"coordination = "
    f"{coordination_score:.8f}"
)
print(
    f"angle        = "
    f"{angle_score:.8f}"
)
print(
    f"bond         = "
    f"{bond_uniformity_score:.8f}"
)
print(
    f"topology     = "
    f"{topology_score:.8f}"
)
print(
    f"period-8     = "
    f"{motif_score:.8f}"
)
print(
    f"overall      = "
    f"{overall_score:.8f}"
)

print()
print("=== CLASSIFICATION ===")
print(classification)


result = {
    "schema": "openmind.material_compatibility.v20",
    "source_geometry": str(source),
    "source_raw": str(RAW),
    "source_motif": str(MOTIF),
    "layer_count": N,
    "period": PERIOD,
    "bond_threshold": bond_threshold,
    "bond_count": len(bonds),
    "mean_coordination": mean_coordination,
    "coordination_error": coordination_error,
    "graphene_coordination_fraction":
        graphene_coordination_fraction,
    "mean_bond_length": mean_bond,
    "bond_rms": bond_rms,
    "bond_cv": bond_cv,
    "optimal_graphene_scale":
        optimal_scale,
    "scaled_graphene_bond_length":
        scaled_mean_bond,
    "mean_angle_degrees":
        mean_angle_degrees,
    "mean_angular_error_degrees":
        angle_error_degrees,
    "period8_bond_similarity":
        period8_bond_similarity,
    "null_mean": null_mean,
    "null_std": null_std,
    "null_z": null_z,
    "scores": {
        "coordination": coordination_score,
        "angle": angle_score,
        "bond": bond_uniformity_score,
        "topology": topology_score,
        "period8": motif_score,
        "overall": overall_score,
    },
    "classification": classification,
}

OUTPUT.write_text(
    json.dumps(
        result,
        indent=2,
    )
)

print()
print(f"Output: {OUTPUT}")
print()
print("MATERIAL COMPATIBILITY ANALYSIS COMPLETE")
