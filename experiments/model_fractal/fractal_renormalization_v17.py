import json
import math
from pathlib import Path

INPUT = Path(
    "experiments/model_fractal/normalized_geometry_v10.json"
)

OUTPUT = Path(
    "experiments/model_fractal/fractal_renormalization_v17.json"
)

EPS = 1e-12

d = json.loads(INPUT.read_text())

layer_coordinates = d["layer_coordinates"]

points = [
    (
        float(p["x"]),
        float(p["y"]),
        float(p["z"]),
    )
    for p in layer_coordinates
]

N = len(points)


print("=" * 72)
print(" OPENMIND / FRACTAL RENORMALIZATION V17")
print("=" * 72)

print()
print(f"Layers: {N}")


# ----------------------------------------------------------------------
# Vector helpers
# ----------------------------------------------------------------------

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
    return math.sqrt(dot(v, v))


def distance(a, b):
    return norm(sub(a, b))


def cosine(a, b):
    na = norm(a)
    nb = norm(b)

    if na <= EPS or nb <= EPS:
        return 0.0

    return dot(a, b) / (na * nb)


def centroid(values):
    if not values:
        return (0.0, 0.0, 0.0)

    return tuple(
        sum(p[k] for p in values) / len(values)
        for k in range(3)
    )


# ----------------------------------------------------------------------
# Coarse graining
#
# Scale 1 = original trajectory.
# Scale 2 = averages of 2 consecutive points.
# Scale 4 = averages of 4 consecutive points.
# Scale 8 = averages of 8 consecutive points.
#
# Only complete blocks are retained.
# ----------------------------------------------------------------------

def coarse_grain(values, block_size):

    result = []

    count = len(values) // block_size

    for i in range(count):

        block = values[
            i * block_size:
            (i + 1) * block_size
        ]

        result.append(
            centroid(block)
        )

    return result


# ----------------------------------------------------------------------
# Normalize trajectory
#
# Translation is removed.
# Overall scale is removed.
# ----------------------------------------------------------------------

def normalize_trajectory(values):

    if not values:
        return []

    c = centroid(values)

    centered = [
        sub(p, c)
        for p in values
    ]

    rms = math.sqrt(
        sum(
            dot(p, p)
            for p in centered
        )
        / len(centered)
    )

    if rms <= EPS:
        return centered

    return [
        scale(p, 1.0 / rms)
        for p in centered
    ]


# ----------------------------------------------------------------------
# Step geometry
# ----------------------------------------------------------------------

def step_vectors(values):

    return [
        sub(values[i + 1], values[i])
        for i in range(len(values) - 1)
    ]


def step_lengths(values):

    return [
        norm(v)
        for v in step_vectors(values)
    ]


def normalized_lengths(values):

    lengths = step_lengths(values)

    if not lengths:
        return []

    mean = sum(lengths) / len(lengths)

    if mean <= EPS:
        return [0.0 for _ in lengths]

    return [
        x / mean
        for x in lengths
    ]


# ----------------------------------------------------------------------
# Curvature signature
# ----------------------------------------------------------------------

def curvature_signature(values):

    steps = step_vectors(values)

    result = []

    for i in range(1, len(steps)):

        result.append(
            cosine(
                steps[i - 1],
                steps[i],
            )
        )

    return result


# ----------------------------------------------------------------------
# Signature comparison
# ----------------------------------------------------------------------

def sequence_similarity(a, b):

    n = min(len(a), len(b))

    if n == 0:
        return 0.0

    aa = a[:n]
    bb = b[:n]

    mean_a = sum(aa) / n
    mean_b = sum(bb) / n

    va = [
        x - mean_a
        for x in aa
    ]

    vb = [
        x - mean_b
        for x in bb
    ]

    numerator = sum(
        x * y
        for x, y in zip(va, vb)
    )

    denominator = math.sqrt(
        sum(x * x for x in va)
        *
        sum(y * y for y in vb)
    )

    if denominator <= EPS:
        return 0.0

    return numerator / denominator


# ----------------------------------------------------------------------
# Period-8 recurrence
# ----------------------------------------------------------------------

def recurrence_score(values, period=8):

    if len(values) <= period:
        return 0.0

    steps = step_vectors(values)

    if len(steps) <= period:
        return 0.0

    similarities = []

    for i in range(
        len(steps) - period
    ):

        a = steps[i]
        b = steps[i + period]

        na = norm(a)
        nb = norm(b)

        if na <= EPS or nb <= EPS:
            continue

        direction = cosine(a, b)

        scale_ratio = (
            min(na, nb)
            / max(na, nb)
        )

        similarities.append(
            direction * scale_ratio
        )

    if not similarities:
        return 0.0

    return math.sqrt(
        sum(
            x * x
            for x in similarities
        )
        / len(similarities)
    )


# ----------------------------------------------------------------------
# Build representations
# ----------------------------------------------------------------------

scales = [1, 2, 4, 8]

representations = {}

for s in scales:

    coarse = coarse_grain(
        points,
        s
    )

    normalized = normalize_trajectory(
        coarse
    )

    representations[s] = normalized


# ----------------------------------------------------------------------
# Per-scale diagnostics
# ----------------------------------------------------------------------

diagnostics = []

print()
print("=== SCALE REPRESENTATIONS ===")

for s in scales:

    values = representations[s]

    lengths = normalized_lengths(values)

    curvature = curvature_signature(values)

    recurrence = recurrence_score(
        values,
        period=8
    )

    path_length = sum(
        step_lengths(values)
    )

    diagnostics.append(
        {
            "scale": s,
            "point_count": len(values),
            "path_length": path_length,
            "recurrence_period_8": recurrence,
            "mean_normalized_step":
                (
                    sum(lengths) / len(lengths)
                    if lengths
                    else 0.0
                ),
            "curvature_mean":
                (
                    sum(curvature) / len(curvature)
                    if curvature
                    else 0.0
                ),
        }
    )

    print(
        f"scale={s:2d} "
        f"points={len(values):2d} "
        f"path={path_length:.8f} "
        f"period8={recurrence:.8f}"
    )


# ----------------------------------------------------------------------
# Cross-scale shape similarity
# ----------------------------------------------------------------------

print()
print("=== CROSS-SCALE SHAPE SIMILARITY ===")

cross_scale = []

for i in range(len(scales)):

    for j in range(i + 1, len(scales)):

        a_scale = scales[i]
        b_scale = scales[j]

        a = representations[a_scale]
        b = representations[b_scale]

        # Compare normalized radial-distance signatures.
        n = min(len(a), len(b))

        if n == 0:
            similarity = 0.0
        else:

            ra = [
                norm(p)
                for p in a[:n]
            ]

            rb = [
                norm(p)
                for p in b[:n]
            ]

            similarity = sequence_similarity(
                ra,
                rb
            )

        result = {
            "scale_a": a_scale,
            "scale_b": b_scale,
            "shape_similarity": similarity,
        }

        cross_scale.append(result)

        print(
            f"{a_scale} -> {b_scale} "
            f"similarity={similarity:.8f}"
        )


# ----------------------------------------------------------------------
# Cross-scale step similarity
# ----------------------------------------------------------------------

print()
print("=== CROSS-SCALE STEP GEOMETRY ===")

step_comparisons = []

for i in range(len(scales)):

    for j in range(i + 1, len(scales)):

        a_scale = scales[i]
        b_scale = scales[j]

        a = normalized_lengths(
            representations[a_scale]
        )

        b = normalized_lengths(
            representations[b_scale]
        )

        similarity = sequence_similarity(
            a,
            b
        )

        step_comparisons.append(
            {
                "scale_a": a_scale,
                "scale_b": b_scale,
                "step_similarity": similarity,
            }
        )

        print(
            f"{a_scale} -> {b_scale} "
            f"similarity={similarity:.8f}"
        )


# ----------------------------------------------------------------------
# Scale ratios
# ----------------------------------------------------------------------

print()
print("=== PATH SCALE RATIOS ===")

path_ratios = []

for i in range(len(diagnostics) - 1):

    a = diagnostics[i]
    b = diagnostics[i + 1]

    if a["path_length"] > EPS:

        ratio = (
            b["path_length"]
            / a["path_length"]
        )

    else:
        ratio = 0.0

    path_ratios.append(
        {
            "scale_a": a["scale"],
            "scale_b": b["scale"],
            "ratio": ratio,
        }
    )

    print(
        f"{a['scale']} -> {b['scale']} "
        f"ratio={ratio:.8f}"
    )


# ----------------------------------------------------------------------
# Self-similarity score
# ----------------------------------------------------------------------

shape_values = [
    x["shape_similarity"]
    for x in cross_scale
]

step_values = [
    x["step_similarity"]
    for x in step_comparisons
]

if shape_values:
    shape_score = (
        sum(shape_values)
        / len(shape_values)
    )
else:
    shape_score = 0.0

if step_values:
    step_score = (
        sum(step_values)
        / len(step_values)
    )
else:
    step_score = 0.0

recurrence_values = [
    x["recurrence_period_8"]
    for x in diagnostics
]

recurrence_score_mean = (
    sum(recurrence_values)
    / len(recurrence_values)
    if recurrence_values
    else 0.0
)

self_similarity_score = (
    0.5 * shape_score
    + 0.3 * step_score
    + 0.2 * recurrence_score_mean
)


# ----------------------------------------------------------------------
# Classification
# ----------------------------------------------------------------------

if self_similarity_score >= 0.75:
    classification = "STRONG_SELF_SIMILARITY"
elif self_similarity_score >= 0.50:
    classification = "MODERATE_SELF_SIMILARITY"
elif self_similarity_score >= 0.25:
    classification = "WEAK_SELF_SIMILARITY"
else:
    classification = "NO_CLEAR_SELF_SIMILARITY"


print()
print("=== RENORMALIZATION SCORE ===")

print(
    f"shape score       = {shape_score:.8f}"
)

print(
    f"step score        = {step_score:.8f}"
)

print(
    f"recurrence score  = "
    f"{recurrence_score_mean:.8f}"
)

print(
    f"self-similarity   = "
    f"{self_similarity_score:.8f}"
)

print()
print("=== CLASSIFICATION ===")
print(classification)


# ----------------------------------------------------------------------
# Output
# ----------------------------------------------------------------------

result = {
    "schema":
        "openmind.fractal_renormalization.v17",

    "source":
        str(INPUT),

    "original_layer_count":
        N,

    "scales":
        scales,

    "scale_diagnostics":
        diagnostics,

    "cross_scale_shape":
        cross_scale,

    "cross_scale_steps":
        step_comparisons,

    "path_scale_ratios":
        path_ratios,

    "shape_score":
        shape_score,

    "step_score":
        step_score,

    "recurrence_score":
        recurrence_score_mean,

    "self_similarity_score":
        self_similarity_score,

    "classification":
        classification,
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
print("FRACTAL RENORMALIZATION COMPLETE")
