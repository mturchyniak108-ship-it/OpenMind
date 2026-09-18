import json
import math
import random
from pathlib import Path

INPUT = Path(
    "experiments/model_fractal/normalized_geometry_v10.json"
)

V24 = Path(
    "experiments/model_fractal/spatial_null_v24.json"
)

OUTPUT = Path(
    "experiments/model_fractal/lattice_recovery_v25.json"
)

EPS = 1e-12
PERIOD = 8
NULL_TRIALS = 2000
SEED = 2501

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
        x - y
        for x, y in zip(a, b)
    )


def add(a, b):
    return tuple(
        x + y
        for x, y in zip(a, b)
    )


def scale(v, s):
    return tuple(
        x * s
        for x in v
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

    return dot(a, b) / (
        na * nb
    )


def mean(values):
    values = list(values)
    return (
        sum(values) / len(values)
        if values
        else 0.0
    )


def rms(values):
    return (
        math.sqrt(
            sum(
                x * x
                for x in values
            ) / len(values)
        )
        if values
        else 0.0
    )


# ----------------------------------------------------------------------
# Pairwise distance matrix
# ----------------------------------------------------------------------

D = [
    [
        distance(
            points[i],
            points[j],
        )
        for j in range(N)
    ]
    for i in range(N)
]


# ----------------------------------------------------------------------
# Periodic displacement candidates
#
# For every i -> i+8 transition, calculate the displacement vector.
# We then search for repeated displacement directions without imposing
# a cubic basis.
# ----------------------------------------------------------------------

displacements = []

for i in range(N - PERIOD):
    j = i + PERIOD

    v = sub(
        points[j],
        points[i],
    )

    if norm(v) > EPS:
        displacements.append(v)


# ----------------------------------------------------------------------
# Displacement similarity
# ----------------------------------------------------------------------

pair_cosines = []

for i in range(len(displacements)):
    for j in range(i + 1, len(displacements)):
        pair_cosines.append(
            abs(
                cosine(
                    displacements[i],
                    displacements[j],
                )
            )
        )

displacement_coherence = mean(
    pair_cosines
)


# ----------------------------------------------------------------------
# Best translation vector
#
# Use the mean displacement as an independently recovered candidate.
# ----------------------------------------------------------------------

translation = (
    tuple(
        mean(
            [
                v[k]
                for v in displacements
            ]
        )
        for k in range(3)
    )
    if displacements
    else (0.0, 0.0, 0.0)
)

translation_length = norm(
    translation
)


# ----------------------------------------------------------------------
# Translation residual
# ----------------------------------------------------------------------

translation_residuals = [
    distance(
        v,
        translation,
    )
    for v in displacements
]

translation_rms = rms(
    translation_residuals
)

translation_relative_error = (
    translation_rms / translation_length
    if translation_length > EPS
    else float("inf")
)


# ----------------------------------------------------------------------
# Period-8 distance preservation
#
# Compare the distance pattern inside the first cell with each
# subsequent period-shifted cell.
# ----------------------------------------------------------------------

cell_similarity = []

for start in range(
    0,
    N - PERIOD,
    PERIOD,
):

    if start + PERIOD >= N:
        break

    for a in range(PERIOD):
        for b in range(a + 1, PERIOD):

            i1 = start + a
            i2 = start + b

            if (
                i1 >= N
                or i2 >= N
            ):
                continue

            d0 = D[a][b]
            d1 = D[i1][i2]

            if d0 > EPS and d1 > EPS:
                cell_similarity.append(
                    min(d0, d1)
                    / max(d0, d1)
                )


distance_pattern_similarity = mean(
    cell_similarity
)


# ----------------------------------------------------------------------
# Lattice reconstruction error
#
# Reconstruct each period-shifted point from the first point plus the
# recovered translation vector.
# ----------------------------------------------------------------------

reconstruction_errors = []

for i in range(
    N - PERIOD
):

    predicted = add(
        points[i],
        translation,
    )

    actual = points[
        i + PERIOD
    ]

    reconstruction_errors.append(
        distance(
            predicted,
            actual,
        )
    )

reconstruction_rms = rms(
    reconstruction_errors
)


# ----------------------------------------------------------------------
# Radial-preserving null
#
# Preserve each point's radius from the origin but randomize direction.
# This is deliberately independent from V24's graph metric machinery.
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
        scale(
            random_direction(),
            r,
        )
        for r in radii
    ]


def null_translation_metric(ps):

    vectors = []

    for i in range(
        N - PERIOD
    ):
        vectors.append(
            sub(
                ps[i + PERIOD],
                ps[i],
            )
        )

    if not vectors:
        return 0.0

    ref = tuple(
        mean(
            v[k]
            for v in vectors
        )
        for k in range(3)
    )

    errors = [
        distance(
            v,
            ref,
        )
        for v in vectors
    ]

    scale_ref = norm(ref)

    if scale_ref <= EPS:
        return 0.0

    return max(
        0.0,
        1.0
        - (
            rms(errors)
            / scale_ref
        ),
    )


observed_translation_coherence = max(
    0.0,
    displacement_coherence,
)


null_values = []

for _ in range(
    NULL_TRIALS
):
    ps = null_points()

    null_values.append(
        null_translation_metric(
            ps
        )
    )


null_mean = mean(
    null_values
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
    (
        observed_translation_coherence
        - null_mean
    )
    / null_std
    if null_std > EPS
    else 0.0
)

empirical_p = (
    (
        1
        + sum(
            x >= observed_translation_coherence
            for x in null_values
        )
    )
    / (
        len(null_values)
        + 1
    )
)


# ----------------------------------------------------------------------
# Threshold robustness
#
# Test whether the recovered bond topology changes dramatically when
# the distance cutoff is varied around the V24 threshold.
# ----------------------------------------------------------------------

all_pair_distances = [
    D[i][j]
    for i in range(N)
    for j in range(i + 1, N)
]

all_pair_distances.sort()

q_values = []

for q in (
    0.10,
    0.15,
    0.20,
    0.25,
    0.30,
):

    idx = int(
        q * len(all_pair_distances)
    )

    idx = max(
        0,
        min(
            len(all_pair_distances) - 1,
            idx,
        ),
    )

    threshold = (
        all_pair_distances[idx]
    )

    degrees = [
        sum(
            D[i][j] <= threshold
            for j in range(N)
            if j != i
        )
        for i in range(N)
    ]

    q_values.append(
        {
            "quantile": q,
            "threshold": threshold,
            "mean_degree": mean(degrees),
        }
    )


# ----------------------------------------------------------------------
# Classification
# ----------------------------------------------------------------------

if (
    null_z >= 3.0
    and distance_pattern_similarity >= 0.65
    and translation_relative_error < 1.0
):
    classification = (
        "INDEPENDENT_LATTICE_RECOVERY_SUPPORTED"
    )

elif (
    null_z >= 2.0
    and distance_pattern_similarity >= 0.55
):
    classification = (
        "WEAK_INDEPENDENT_LATTICE_RECOVERY"
    )

else:
    classification = (
        "NO_INDEPENDENT_LATTICE_RECOVERY"
    )


print("=" * 72)
print(
    " OPENMIND / LATTICE RECOVERY V25"
)
print("=" * 72)

print()
print(
    f"Layers: {N}"
)

print()
print("=== PERIOD-8 DISPLACEMENTS ===")
print(
    f"count = {len(displacements)}"
)
print(
    "translation = "
    f"({translation[0]:.8f}, "
    f"{translation[1]:.8f}, "
    f"{translation[2]:.8f})"
)
print(
    f"|translation| = "
    f"{translation_length:.8f}"
)

print()
print("=== DISPLACEMENT COHERENCE ===")
print(
    f"coherence = "
    f"{displacement_coherence:.8f}"
)
print(
    f"relative residual = "
    f"{translation_relative_error:.8f}"
)

print()
print("=== PERIOD-8 DISTANCE PATTERN ===")
print(
    f"similarity = "
    f"{distance_pattern_similarity:.8f}"
)

print()
print("=== TRANSLATION RECONSTRUCTION ===")
print(
    f"RMS error = "
    f"{reconstruction_rms:.8f}"
)

print()
print("=== RADIAL-PRESERVING NULL ===")
print(
    f"observed = "
    f"{observed_translation_coherence:.8f}"
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
print(
    f"empirical p = "
    f"{empirical_p:.8f}"
)

print()
print("=== THRESHOLD ROBUSTNESS ===")

for q in q_values:
    print(
        f"q={q['quantile']:.2f} "
        f"threshold={q['threshold']:.8f} "
        f"mean_degree={q['mean_degree']:.8f}"
    )

print()
print("=== CLASSIFICATION ===")
print(classification)

output = {
    "schema":
        "openmind.lattice_recovery.v25",
    "source":
        str(INPUT),
    "v24_source":
        str(V24),
    "layer_count": N,
    "period": PERIOD,
    "null_trials": NULL_TRIALS,
    "random_seed": SEED,
    "period8_displacement_count":
        len(displacements),
    "translation": translation,
    "translation_length":
        translation_length,
    "displacement_coherence":
        displacement_coherence,
    "translation_relative_error":
        translation_relative_error,
    "distance_pattern_similarity":
        distance_pattern_similarity,
    "translation_reconstruction_rms":
        reconstruction_rms,
    "null_mean":
        null_mean,
    "null_std":
        null_std,
    "null_z":
        null_z,
    "empirical_p":
        empirical_p,
    "threshold_robustness":
        q_values,
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
    "LATTICE RECOVERY COMPLETE"
)
