import json
import math
from pathlib import Path
from collections import Counter

INPUT = Path(
    "experiments/model_fractal/normalized_geometry_v10.json"
)

OUTPUT = Path(
    "experiments/model_fractal/crystal_raw_lattice_v15.json"
)

EPS = 1e-12
PERIOD = 8
GRID = 7

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


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(v, s):
    return tuple(x * s for x in v)


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


def determinant(a, b, c):
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


print("=" * 72)
print(" OPENMIND / RAW CRYSTAL LATTICE V15")
print("=" * 72)
print()
print(f"Layers: {N}")
print(f"Raw recurrence period: {PERIOD}")
print(f"Replication grid: {GRID} x {GRID} x {GRID}")


# ----------------------------------------------------------------------
# Raw translation vectors
#
# No Gram-Schmidt.
# No forced orthogonality.
# These are measured directly from the observed trajectory.
# ----------------------------------------------------------------------

translations = []

for cell in range((N - 1) // PERIOD):
    start = cell * PERIOD
    end = start + PERIOD

    if end >= N:
        break

    translations.append(
        sub(points[end], points[start])
    )


print()
print("=== RAW TRANSLATION VECTORS ===")

for i, v in enumerate(translations):
    print(
        f"T{i + 1} = "
        f"({v[0]:.8f}, {v[1]:.8f}, {v[2]:.8f}) "
        f"|T|={norm(v):.8f}"
    )


# Use the first three independently observed translations.
basis = translations[:3]

A1, A2, A3 = basis

volume = abs(determinant(A1, A2, A3))


print()
print("=== RAW BASIS ANGLES ===")

angles = {
    "A1-A2": angle(A1, A2),
    "A1-A3": angle(A1, A3),
    "A2-A3": angle(A2, A3),
}

for name, value in angles.items():
    print(
        f"{name} angle={value:.8f}°"
    )

# Print cosines separately to keep the calculation explicit.
for name, a, b in (
    ("A1-A2", A1, A2),
    ("A1-A3", A1, A3),
    ("A2-A3", A2, A3),
):
    print(
        f"{name} cosine={cosine(a, b):.8f}"
    )


print()
print("=== RAW UNIT CELL ===")
print(f"volume = {volume:.10f}")


# ----------------------------------------------------------------------
# Build a raw lattice.
#
# Each observed period-8 segment is treated as the unit-cell motif.
# The cell is translated using the raw basis vectors.
# ----------------------------------------------------------------------

cell_points = points[: PERIOD + 1]

lattice = []

for i in range(GRID):
    for j in range(GRID):
        for k in range(GRID):
            origin = add(
                add(
                    scale(A1, i),
                    scale(A2, j),
                ),
                scale(A3, k),
            )

            for p in cell_points[:-1]:
                lattice.append(add(origin, p))


# ----------------------------------------------------------------------
# Nearest-neighbor statistics.
# ----------------------------------------------------------------------

nearest = []

for i, p in enumerate(lattice):
    best = float("inf")

    for j, q in enumerate(lattice):
        if i == j:
            continue

        dist = distance(p, q)

        if dist < best:
            best = dist

    nearest.append(best)


mean_nn = sum(nearest) / len(nearest)

rms_nn = math.sqrt(
    sum(x * x for x in nearest)
    / len(nearest)
)

std_nn = math.sqrt(
    sum((x - mean_nn) ** 2 for x in nearest)
    / len(nearest)
)

uniformity = (
    1.0 - std_nn / mean_nn
    if mean_nn > EPS
    else 0.0
)


print()
print("=== RAW NEAREST-NEIGHBOR GEOMETRY ===")
print(f"mean distance = {mean_nn:.8f}")
print(f"RMS distance  = {rms_nn:.8f}")
print(f"std distance  = {std_nn:.8f}")
print(f"uniformity    = {uniformity:.8f}")


# ----------------------------------------------------------------------
# Pair-distance shells.
#
# Count distances within the central portion of the lattice to reduce
# boundary effects.
# ----------------------------------------------------------------------

center = lattice[
    len(lattice) // 2
]

distances = []

for p in lattice:
    dist = distance(center, p)

    if dist > EPS:
        distances.append(dist)

distances.sort()

shells = []

tolerance = 0.025

for dist in distances:
    if not shells:
        shells.append(
            {
                "distance": dist,
                "count": 1,
            }
        )
        continue

    previous = shells[-1]["distance"]

    if abs(dist - previous) <= tolerance:
        count = shells[-1]["count"]

        shells[-1]["distance"] = (
            previous * count + dist
        ) / (count + 1)

        shells[-1]["count"] = count + 1
    else:
        shells.append(
            {
                "distance": dist,
                "count": 1,
            }
        )


shells = shells[:15]


print()
print("=== RADIAL DISTANCE SHELLS ===")

for shell in shells:
    print(
        f"r={shell['distance']:.8f} "
        f"count={shell['count']}"
    )


# ----------------------------------------------------------------------
# Translation consistency.
#
# Compare observed period translations against the first raw translation.
# ----------------------------------------------------------------------

translation_cosines = []

for v in translations[1:]:
    translation_cosines.append(
        cosine(A1, v)
    )


translation_mean = (
    sum(translation_cosines)
    / len(translation_cosines)
    if translation_cosines
    else 0.0
)


print()
print("=== TRANSLATION CONSISTENCY ===")

for i, c in enumerate(translation_cosines, start=2):
    print(
        f"T1 vs T{i} cosine={c:.8f}"
    )

print(
    f"mean translation cosine={translation_mean:.8f}"
)


# ----------------------------------------------------------------------
# Raw step-length statistics inside the observed unit cell.
# ----------------------------------------------------------------------

steps = [
    sub(
        cell_points[i + 1],
        cell_points[i],
    )
    for i in range(PERIOD)
]

step_lengths = [
    norm(v)
    for v in steps
]

step_mean = sum(step_lengths) / len(step_lengths)

step_std = math.sqrt(
    sum((x - step_mean) ** 2 for x in step_lengths)
    / len(step_lengths)
)

step_uniformity = (
    1.0 - step_std / step_mean
    if step_mean > EPS
    else 0.0
)


print()
print("=== RAW UNIT-CELL STEP GEOMETRY ===")
print(f"mean step = {step_mean:.8f}")
print(f"RMS step  = {math.sqrt(sum(x*x for x in step_lengths)/len(step_lengths)):.8f}")
print(f"uniformity = {step_uniformity:.8f}")


# ----------------------------------------------------------------------
# Final classification.
#
# Deliberately conservative:
# "RAW_PERIODIC_STRUCTURE" does not claim a conventional crystal.
# ----------------------------------------------------------------------

if (
    volume > EPS
    and uniformity > 0.95
    and translation_mean > 0.75
):
    classification = "RAW_3D_PERIODIC_STRUCTURE"
elif volume > EPS and translation_mean > 0.5:
    classification = "WEAK_RAW_3D_PERIODIC_STRUCTURE"
else:
    classification = "NONCRYSTALLINE_RAW_GEOMETRY"


result = {
    "schema": "openmind.crystal_raw_lattice.v15",
    "source": str(INPUT),
    "period": PERIOD,
    "grid": GRID,
    "layer_count": N,

    "raw_basis": {
        "A1": A1,
        "A2": A2,
        "A3": A3,
    },

    "basis_lengths": {
        "A1": norm(A1),
        "A2": norm(A2),
        "A3": norm(A3),
    },

    "basis_angles_degrees": angles,

    "basis_cosines": {
        "A1-A2": cosine(A1, A2),
        "A1-A3": cosine(A1, A3),
        "A2-A3": cosine(A2, A3),
    },

    "cell_volume": volume,

    "translation_consistency": {
        "individual_cosines": translation_cosines,
        "mean_cosine": translation_mean,
    },

    "nearest_neighbor": {
        "mean": mean_nn,
        "rms": rms_nn,
        "std": std_nn,
        "uniformity": uniformity,
    },

    "unit_cell_steps": {
        "lengths": step_lengths,
        "mean": step_mean,
        "std": step_std,
        "uniformity": step_uniformity,
    },

    "radial_shells": shells,

    "lattice": {
        "cells": GRID ** 3,
        "points": len(lattice),
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
print("=== CLASSIFICATION ===")
print(classification)

print()
print(f"Output: {OUTPUT}")
print()
print("RAW CRYSTAL LATTICE ANALYSIS COMPLETE")
