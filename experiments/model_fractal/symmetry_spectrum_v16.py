import json
import math
import random
from pathlib import Path

INPUT = Path(
    "experiments/model_fractal/normalized_geometry_v10.json"
)

OUTPUT = Path(
    "experiments/model_fractal/symmetry_spectrum_v16.json"
)

EPS = 1e-12
SEED = 108
NULL_TRIALS = 250


d = json.loads(INPUT.read_text())

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
print(" OPENMIND / SYMMETRY SPECTRUM V16")
print("=" * 72)
print()
print(f"Layers: {N}")


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


def add(a, b):
    return tuple(
        x + y for x, y in zip(a, b)
    )


def scale(v, s):
    return tuple(
        x * s for x in v
    )


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
            dot(a, b) / (na * nb)
        )
    )


# ----------------------------------------------------------------------
# Center trajectory
# ----------------------------------------------------------------------

centroid = scale(
    (
        sum(p[0] for p in points),
        sum(p[1] for p in points),
        sum(p[2] for p in points),
    ),
    1.0 / N,
)

centered = [
    sub(p, centroid)
    for p in points
]


# ----------------------------------------------------------------------
# Step geometry
# ----------------------------------------------------------------------

steps = [
    sub(
        centered[i + 1],
        centered[i]
    )
    for i in range(N - 1)
]

step_lengths = [
    norm(v)
    for v in steps
]


# ----------------------------------------------------------------------
# Rotation-free local motif similarity
#
# Compare adjacent step-length windows. This deliberately ignores
# orientation and tests whether the same local geometric "shape"
# reappears elsewhere.
# ----------------------------------------------------------------------

motifs = []

for period in range(2, 14):

    similarities = []

    for i in range(len(step_lengths) - period):

        a = step_lengths[i:i + period]
        b = step_lengths[i + 1:i + period + 1]

        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(x * x for x in b))

        if na <= EPS or nb <= EPS:
            continue

        similarities.append(
            sum(
                x * y
                for x, y in zip(a, b)
            ) / (na * nb)
        )

    if similarities:

        motifs.append(
            {
                "period": period,
                "mean": sum(similarities) / len(similarities),
                "max": max(similarities),
                "rms": math.sqrt(
                    sum(x * x for x in similarities)
                    / len(similarities)
                ),
            }
        )


# ----------------------------------------------------------------------
# Reversal symmetry
# ----------------------------------------------------------------------

forward = step_lengths
reverse = list(reversed(step_lengths))

reverse_cos = cosine(
    forward,
    reverse
)


# ----------------------------------------------------------------------
# Scale recurrence
#
# Compare step-length windows after optimal scalar normalization.
# ----------------------------------------------------------------------

scale_recurrence = []

for period in range(2, 14):

    values = []

    for i in range(len(step_lengths) - period):

        a = step_lengths[i:i + period]
        b = step_lengths[i + period:i + 2 * period]

        if len(b) != period:
            continue

        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(x * x for x in b))

        if na <= EPS or nb <= EPS:
            continue

        values.append(
            cosine(a, b)
        )

    if values:
        scale_recurrence.append(
            {
                "period": period,
                "mean": sum(values) / len(values),
                "max": max(values),
                "rms": math.sqrt(
                    sum(x * x for x in values)
                    / len(values)
                ),
            }
        )


# ----------------------------------------------------------------------
# Raw translation recurrence
# ----------------------------------------------------------------------

translations = []

for period in range(1, 14):

    sims = []

    for i in range(N - period - 1):

        a = sub(
            centered[i + period],
            centered[i]
        )

        b = sub(
            centered[i + period + 1],
            centered[i + 1]
        )

        sims.append(
            cosine(a, b)
        )

    if sims:

        translations.append(
            {
                "period": period,
                "mean": sum(sims) / len(sims),
                "max": max(sims),
                "rms": math.sqrt(
                    sum(x * x for x in sims)
                    / len(sims)
                ),
            }
        )


# ----------------------------------------------------------------------
# Reflection / inversion symmetry
#
# Test x -> -x after centering. Because the trajectory is centered,
# this is a direct inversion test.
# ----------------------------------------------------------------------

inversion_errors = [
    distance(
        centered[i],
        scale(centered[N - 1 - i], -1.0)
    )
    for i in range(N)
]

inversion_rms = math.sqrt(
    sum(x * x for x in inversion_errors)
    / N
)

trajectory_scale = math.sqrt(
    sum(norm(p) ** 2 for p in centered)
    / N
)

inversion_score = (
    max(
        0.0,
        1.0 - inversion_rms / max(trajectory_scale, EPS)
    )
)


# ----------------------------------------------------------------------
# Null model
#
# Preserve the exact step-length distribution but randomize directions.
# This asks whether observed directional recurrence exceeds what the
# same magnitude statistics would produce by chance.
# ----------------------------------------------------------------------

rng = random.Random(SEED)

observed_period8 = next(
    (
        x["rms"]
        for x in translations
        if x["period"] == 8
    ),
    0.0,
)

null_scores = []

for _ in range(NULL_TRIALS):

    random_steps = []

    for length in step_lengths:

        z = [
            rng.gauss(0.0, 1.0)
            for _ in range(3)
        ]

        nz = math.sqrt(
            sum(x * x for x in z)
        )

        if nz <= EPS:
            z = [1.0, 0.0, 0.0]
            nz = 1.0

        random_steps.append(
            scale(z, length / nz)
        )

    sims = []

    for i in range(len(random_steps) - 8):

        a = random_steps[i]
        b = random_steps[i + 1]

        sims.append(
            cosine(a, b)
        )

    if sims:

        null_scores.append(
            math.sqrt(
                sum(x * x for x in sims)
                / len(sims)
            )
        )


null_mean = (
    sum(null_scores) / len(null_scores)
    if null_scores
    else 0.0
)

null_std = math.sqrt(
    sum(
        (x - null_mean) ** 2
        for x in null_scores
    ) / len(null_scores)
) if null_scores else 0.0

z_score = (
    (observed_period8 - null_mean)
    / max(null_std, EPS)
)


# ----------------------------------------------------------------------
# Rankings
# ----------------------------------------------------------------------

motifs_ranked = sorted(
    motifs,
    key=lambda x: x["rms"],
    reverse=True,
)

scale_ranked = sorted(
    scale_recurrence,
    key=lambda x: x["rms"],
    reverse=True,
)

translation_ranked = sorted(
    translations,
    key=lambda x: x["rms"],
    reverse=True,
)


print()
print("=== LOCAL MOTIF RECURRENCE ===")

for x in motifs_ranked[:10]:
    print(
        f"period={x['period']:2d} "
        f"rms={x['rms']:.8f} "
        f"mean={x['mean']:.8f} "
        f"max={x['max']:.8f}"
    )


print()
print("=== SCALE RECURRENCE ===")

for x in scale_ranked[:10]:
    print(
        f"period={x['period']:2d} "
        f"rms={x['rms']:.8f} "
        f"mean={x['mean']:.8f}"
    )


print()
print("=== TRANSLATION SYMMETRY ===")

for x in translation_ranked[:10]:
    print(
        f"period={x['period']:2d} "
        f"rms={x['rms']:.8f} "
        f"mean={x['mean']:.8f}"
    )


print()
print("=== GLOBAL SYMMETRY ===")
print(
    f"reversal cosine = {reverse_cos:.8f}"
)
print(
    f"inversion score  = {inversion_score:.8f}"
)


print()
print("=== NULL MODEL / PERIOD-8 ===")
print(
    f"observed RMS = {observed_period8:.8f}"
)
print(
    f"null mean    = {null_mean:.8f}"
)
print(
    f"null std     = {null_std:.8f}"
)
print(
    f"z-score      = {z_score:.8f}"
)


result = {
    "schema": "openmind.symmetry_spectrum.v16",
    "source": str(INPUT),
    "layer_count": N,
    "motif_recurrence": motifs,
    "scale_recurrence": scale_recurrence,
    "translation_symmetry": translations,
    "reversal_cosine": reverse_cos,
    "inversion_score": inversion_score,
    "null_model": {
        "seed": SEED,
        "trials": NULL_TRIALS,
        "observed_period8_rms": observed_period8,
        "null_mean": null_mean,
        "null_std": null_std,
        "z_score": z_score,
    },
}

OUTPUT.write_text(
    json.dumps(
        result,
        indent=2
    )
)

print()
print(f"Output: {OUTPUT}")
print()
print("SYMMETRY SPECTRUM COMPLETE")
