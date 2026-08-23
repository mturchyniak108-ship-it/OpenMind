import json
import math
from pathlib import Path
from collections import Counter

INPUT = Path(
    "experiments/model_fractal/normalized_geometry_v10.json"
)

OUTPUT = Path(
    "experiments/model_fractal/motif_graph_v19.json"
)

EPS = 1e-12
PERIOD = 8

d = json.loads(INPUT.read_text())
layers = d["layer_coordinates"]

points = [
    (
        float(p["x"]),
        float(p["y"]),
        float(p["z"]),
    )
    for p in layers
]

N = len(points)

print("=" * 72)
print(" OPENMIND / MOTIF GRAPH V19")
print("=" * 72)
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

    return dot(a, b) / (na * nb)


# ----------------------------------------------------------------------
# Pairwise distances
# ----------------------------------------------------------------------

distances = []

for i in range(N):
    for j in range(i + 1, N):
        distances.append(
            {
                "i": i,
                "j": j,
                "distance": distance(points[i], points[j]),
            }
        )


positive = [
    x["distance"]
    for x in distances
    if x["distance"] > EPS
]

positive_sorted = sorted(positive)

# Use the lower-distance structure as the local-neighborhood scale.
# The 20th percentile is deliberately conservative so the graph does
# not become fully connected.
cut_index = max(0, int(len(positive_sorted) * 0.20) - 1)
bond_threshold = positive_sorted[cut_index]

print()
print("=== BOND SCALE ===")
print(f"threshold = {bond_threshold:.8f}")


# ----------------------------------------------------------------------
# Build local bond graph
# ----------------------------------------------------------------------

edges = []

for item in distances:
    if item["distance"] <= bond_threshold + EPS:
        edges.append(item)


degree = Counter()

for edge in edges:
    degree[edge["i"]] += 1
    degree[edge["j"]] += 1


print()
print("=== COORDINATION ===")

for i in range(N):
    print(
        f"L{i:02d} coordination={degree[i]}"
    )


degree_values = [
    degree[i]
    for i in range(N)
]

degree_mean = (
    sum(degree_values) / N
    if N
    else 0.0
)

degree_uniformity = (
    1.0
    - (
        max(degree_values) - min(degree_values)
    ) / max(degree_values)
    if max(degree_values) > 0
    else 0.0
)


# ----------------------------------------------------------------------
# Local motif signatures
#
# A motif signature is intentionally simple:
# sorted normalized bond lengths + coordination.
# ----------------------------------------------------------------------

def local_signature(index):
    local = [
        e["distance"]
        for e in distances
        if (
            (
                e["i"] == index
                or e["j"] == index
            )
            and e["distance"] <= bond_threshold + EPS
        )
    ]

    if not local:
        return {
            "coordination": 0,
            "normalized_lengths": [],
        }

    scale = sum(local) / len(local)

    normalized = sorted(
        round(x / scale, 8)
        for x in local
    )

    return {
        "coordination": len(local),
        "normalized_lengths": normalized,
    }


signatures = [
    local_signature(i)
    for i in range(N)
]


# ----------------------------------------------------------------------
# Motif recurrence at period 8
# ----------------------------------------------------------------------

def signature_similarity(a, b):
    if (
        a["coordination"] == 0
        or b["coordination"] == 0
    ):
        return 0.0

    coordination_score = (
        min(
            a["coordination"],
            b["coordination"],
        )
        / max(
            a["coordination"],
            b["coordination"],
        )
    )

    la = a["normalized_lengths"]
    lb = b["normalized_lengths"]

    m = min(len(la), len(lb))

    if m == 0:
        length_score = 0.0
    else:
        errors = [
            abs(la[i] - lb[i])
            for i in range(m)
        ]

        length_score = max(
            0.0,
            1.0 - sum(errors) / m
        )

    return (
        coordination_score
        * length_score
    )


motif_recurrences = []

for i in range(N - PERIOD):
    j = i + PERIOD

    similarity = signature_similarity(
        signatures[i],
        signatures[j],
    )

    motif_recurrences.append(
        {
            "from_layer": i,
            "to_layer": j,
            "similarity": similarity,
            "coordination_a":
                signatures[i]["coordination"],
            "coordination_b":
                signatures[j]["coordination"],
        }
    )


ranked_motifs = sorted(
    motif_recurrences,
    key=lambda x: x["similarity"],
    reverse=True,
)


print()
print("=== PERIOD-8 MOTIF RECURRENCE ===")

for r in ranked_motifs[:10]:
    print(
        f"L{r['from_layer']:02d}->"
        f"L{r['to_layer']:02d} "
        f"similarity={r['similarity']:.8f} "
        f"coord="
        f"{r['coordination_a']}/"
        f"{r['coordination_b']}"
    )


# ----------------------------------------------------------------------
# Edge recurrence
#
# Does an edge at (i,j) have a corresponding edge at
# (i+8,j+8)?
# ----------------------------------------------------------------------

edge_set = {
    (e["i"], e["j"])
    for e in edges
}

edge_recurrence = []

for i, j in sorted(edge_set):
    ni = i + PERIOD
    nj = j + PERIOD

    if ni < N and nj < N:
        preserved = (
            (ni, nj) in edge_set
        )

        edge_recurrence.append(
            {
                "edge": [i, j],
                "translated_edge": [ni, nj],
                "preserved": preserved,
            }
        )


preserved_edges = sum(
    1
    for x in edge_recurrence
    if x["preserved"]
)

edge_recurrence_score = (
    preserved_edges / len(edge_recurrence)
    if edge_recurrence
    else 0.0
)


# ----------------------------------------------------------------------
# Bond-length recurrence
# ----------------------------------------------------------------------

bond_pairs = []

for i in range(N - PERIOD):
    j = i + PERIOD

    # Compare local bond-length distributions.
    a = signatures[i]["normalized_lengths"]
    b = signatures[j]["normalized_lengths"]

    m = min(len(a), len(b))

    if m:
        error = sum(
            abs(a[k] - b[k])
            for k in range(m)
        ) / m

        similarity = max(
            0.0,
            1.0 - error
        )
    else:
        similarity = 0.0

    bond_pairs.append(
        {
            "from_layer": i,
            "to_layer": j,
            "similarity": similarity,
        }
    )


bond_recurrence_score = (
    sum(x["similarity"] for x in bond_pairs)
    / len(bond_pairs)
    if bond_pairs
    else 0.0
)


# ----------------------------------------------------------------------
# Overall structural motif score
# ----------------------------------------------------------------------

motif_score = (
    0.40 * (
        sum(
            x["similarity"]
            for x in motif_recurrences
        )
        / len(motif_recurrences)
        if motif_recurrences
        else 0.0
    )
    + 0.35 * edge_recurrence_score
    + 0.25 * bond_recurrence_score
)


if motif_score >= 0.80:
    classification = "STRONG_PERIODIC_MOTIF"
elif motif_score >= 0.60:
    classification = "MODERATE_PERIODIC_MOTIF"
elif motif_score >= 0.40:
    classification = "WEAK_PERIODIC_MOTIF"
else:
    classification = "NO_STABLE_PERIODIC_MOTIF"


print()
print("=== MOTIF DIAGNOSTICS ===")
print(
    f"mean coordination = "
    f"{degree_mean:.8f}"
)
print(
    f"coordination uniformity = "
    f"{degree_uniformity:.8f}"
)
print(
    f"edge recurrence = "
    f"{edge_recurrence_score:.8f}"
)
print(
    f"bond recurrence = "
    f"{bond_recurrence_score:.8f}"
)
print(
    f"motif score = "
    f"{motif_score:.8f}"
)

print()
print("=== CLASSIFICATION ===")
print(classification)


# ----------------------------------------------------------------------
# Output
# ----------------------------------------------------------------------

result = {
    "schema": "openmind.motif_graph.v19",
    "source": str(INPUT),
    "layer_count": N,
    "period": PERIOD,
    "bond_threshold": bond_threshold,
    "edge_count": len(edges),
    "degree_mean": degree_mean,
    "degree_uniformity": degree_uniformity,
    "periodic_motif_recurrence":
        motif_recurrences,
    "edge_recurrence":
        edge_recurrence,
    "edge_recurrence_score":
        edge_recurrence_score,
    "bond_recurrence":
        bond_pairs,
    "bond_recurrence_score":
        bond_recurrence_score,
    "motif_score": motif_score,
    "classification": classification,
    "local_signatures": [
        {
            "layer": i,
            "signature": signatures[i],
        }
        for i in range(N)
    ],
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
print("MOTIF GRAPH ANALYSIS COMPLETE")
