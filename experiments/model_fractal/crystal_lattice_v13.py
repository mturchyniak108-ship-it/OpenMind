import json
import math
from pathlib import Path

INPUT = Path(
    "experiments/model_fractal/normalized_geometry_v10.json"
)

V11 = Path(
    "experiments/model_fractal/structural_lattice_v11.json"
)

OUTPUT = Path(
    "experiments/model_fractal/crystal_lattice_v13.json"
)

EPS = 1e-12

d = json.loads(INPUT.read_text())
v11 = json.loads(V11.read_text())

points = [
    (
        float(p["x"]),
        float(p["y"]),
        float(p["z"]),
    )
    for p in d["layer_coordinates"]
]

N = len(points)

print("=" * 72)
print(" OPENMIND / CRYSTAL LATTICE V13")
print("=" * 72)
print()
print(f"Layers: {N}")


def sub(a, b):
    return tuple(
        x - y for x, y in zip(a, b)
    )


def add(a, b):
    return tuple(
        x + y for x, y in zip(a, b)
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


# ----------------------------------------------------------------------
# Candidate periods
# ----------------------------------------------------------------------

periods = [4, 6, 8, 11]

# Keep only periods that actually fit twice in the trajectory.
periods = [
    p for p in periods
    if 2 * p < N
]


# ----------------------------------------------------------------------
# Extract unit cells
# ----------------------------------------------------------------------

def cell_vectors(period):
    cells = []

    start = 0

    while start + period < N:
        origin = points[start]

        cell = [
            sub(
                points[start + j],
                origin
            )
            for j in range(period + 1)
        ]

        cells.append(cell)

        start += period

    return cells


# ----------------------------------------------------------------------
# Cell comparison
# ----------------------------------------------------------------------

def best_scale(a, b):
    numerator = sum(
        dot(x, y)
        for x, y in zip(a, b)
    )

    denominator = sum(
        dot(x, x)
        for x in a
    )

    if denominator <= EPS:
        return 1.0

    return numerator / denominator


def cell_error(a, b):
    s = best_scale(a, b)

    errors = []

    for va, vb in zip(a, b):
        predicted = scale(va, s)
        errors.append(
            norm(sub(vb, predicted))
        )

    if not errors:
        return 0.0

    return math.sqrt(
        sum(x * x for x in errors)
        / len(errors)
    )


def cell_similarity(a, b):
    vectors = []

    for va, vb in zip(a[1:], b[1:]):
        if norm(va) > EPS and norm(vb) > EPS:
            vectors.append(
                cosine(va, vb)
            )

    if not vectors:
        return 0.0

    return sum(vectors) / len(vectors)


# ----------------------------------------------------------------------
# Build lattice candidates
# ----------------------------------------------------------------------

candidates = []

for period in periods:

    cells = cell_vectors(period)

    if len(cells) < 2:
        continue

    errors = []
    similarities = []
    translations = []

    for i in range(len(cells) - 1):

        a = cells[i]
        b = cells[i + 1]

        errors.append(
            cell_error(a, b)
        )

        similarities.append(
            cell_similarity(a, b)
        )

        origin_a = points[i * period]
        origin_b = points[(i + 1) * period]

        translation = sub(
            origin_b,
            origin_a
        )

        translations.append(
            translation
        )

    mean_error = (
        sum(errors) / len(errors)
        if errors else 0.0
    )

    mean_similarity = (
        sum(similarities) / len(similarities)
        if similarities else 0.0
    )

    translation_lengths = [
        norm(v)
        for v in translations
    ]

    mean_translation = (
        sum(translation_lengths)
        / len(translation_lengths)
        if translation_lengths
        else 0.0
    )

    translation_std = 0.0

    if len(translation_lengths) > 1:
        mean_t = mean_translation
        translation_std = math.sqrt(
            sum(
                (x - mean_t) ** 2
                for x in translation_lengths
            )
            / len(translation_lengths)
        )

    uniformity = (
        1.0
        / (
            1.0
            + translation_std
            / max(mean_translation, EPS)
        )
    )

    # A conservative composite score.
    structural_score = (
        0.40 * max(0.0, mean_similarity)
        + 0.30 * uniformity
        + 0.30
        * (
            1.0
            / (1.0 + mean_error)
        )
    )

    candidates.append(
        {
            "period": period,
            "cell_count": len(cells),
            "mean_reconstruction_error": mean_error,
            "mean_cell_similarity": mean_similarity,
            "mean_translation_length": mean_translation,
            "translation_std": translation_std,
            "translation_uniformity": uniformity,
            "structural_score": structural_score,
        }
    )


candidates.sort(
    key=lambda x: x["structural_score"],
    reverse=True,
)


print()
print("=== CRYSTAL CANDIDATES ===")

for c in candidates:
    print(
        f"period={c['period']:2d} "
        f"score={c['structural_score']:.8f} "
        f"error={c['mean_reconstruction_error']:.8f} "
        f"similarity={c['mean_cell_similarity']:.8f} "
        f"uniformity={c['translation_uniformity']:.8f}"
    )


# ----------------------------------------------------------------------
# Build translation basis for the strongest candidate
# ----------------------------------------------------------------------

best = candidates[0] if candidates else None

basis = []

if best:

    period = best["period"]

    for i in range(
        min(3, N // period - 1)
    ):

        a = points[i * period]
        b = points[(i + 1) * period]

        v = sub(b, a)

        if norm(v) > EPS:
            basis.append(
                {
                    "x": v[0],
                    "y": v[1],
                    "z": v[2],
                    "length": norm(v),
                }
            )


# ----------------------------------------------------------------------
# Crystal replication test
#
# Replicate the canonical cell along each observed translation vector.
# Measure nearest-neighbor consistency between copies.
# ----------------------------------------------------------------------

replication_tests = []

if best and basis:

    period = best["period"]

    canonical = [
        points[j]
        for j in range(period + 1)
    ]

    origin = canonical[0]

    canonical = [
        sub(p, origin)
        for p in canonical
    ]

    for axis_index, b in enumerate(basis):

        for copies in (2, 3, 5, 8):

            generated = []

            for k in range(copies):

                offset = scale(
                    (
                        b["x"],
                        b["y"],
                        b["z"],
                    ),
                    k,
                )

                for p in canonical:

                    generated.append(
                        add(p, offset)
                    )

            nearest = []

            for i, p in enumerate(generated):

                best_distance = None

                for j, q in enumerate(generated):

                    if i == j:
                        continue

                    dist = distance(p, q)

                    if dist <= EPS:
                        continue

                    if (
                        best_distance is None
                        or dist < best_distance
                    ):
                        best_distance = dist

                if best_distance is not None:
                    nearest.append(best_distance)

            if nearest:

                mean_nn = (
                    sum(nearest)
                    / len(nearest)
                )

                nn_std = math.sqrt(
                    sum(
                        (x - mean_nn) ** 2
                        for x in nearest
                    )
                    / len(nearest)
                )

                nn_uniformity = (
                    1.0
                    / (
                        1.0
                        + nn_std
                        / max(mean_nn, EPS)
                    )
                )

            else:
                mean_nn = 0.0
                nn_std = 0.0
                nn_uniformity = 0.0

            replication_tests.append(
                {
                    "axis": axis_index,
                    "copies": copies,
                    "point_count": len(generated),
                    "mean_nearest_neighbor":
                        mean_nn,
                    "nearest_neighbor_std":
                        nn_std,
                    "nearest_neighbor_uniformity":
                        nn_uniformity,
                }
            )


# ----------------------------------------------------------------------
# Result
# ----------------------------------------------------------------------

result = {
    "schema": "openmind.crystal_lattice.v13",

    "source": str(INPUT),

    "structural_lattice_source": str(V11),

    "layer_count": N,

    "candidate_periods": periods,

    "candidates": candidates,

    "best_candidate": best,

    "translation_basis": basis,

    "replication_tests": replication_tests,

    "interpretation": {
        "status":
            "crystalline_candidate"
            if best
            and best["structural_score"] >= 0.65
            else "periodic_fractal_candidate",

        "warning":
            "A high structural score indicates geometric "
            "lattice-like recurrence, not physical crystallinity."
    },
}


OUTPUT.write_text(
    json.dumps(
        result,
        indent=2
    )
)

print()
print("Output:", OUTPUT)
print()
print("CRYSTAL LATTICE ANALYSIS COMPLETE")
