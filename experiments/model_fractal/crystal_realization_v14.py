import json
import math
from pathlib import Path

INPUT = Path(
    "experiments/model_fractal/normalized_geometry_v10.json"
)

LATTICE_INPUT = Path(
    "experiments/model_fractal/crystal_lattice_v13.json"
)

OUTPUT = Path(
    "experiments/model_fractal/crystal_realization_v14.json"
)

EPS = 1e-12
PERIOD = 8
GRID = 3

d = json.loads(INPUT.read_text())
lattice = json.loads(LATTICE_INPUT.read_text())

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


print("=" * 72)
print(" OPENMIND / CRYSTAL REALIZATION V14")
print("=" * 72)

print()
print(f"Source layers: {N}")
print(f"Candidate period: {PERIOD}")
print(f"Replication grid: {GRID} x {GRID} x {GRID}")


# ----------------------------------------------------------------------
# Extract canonical period-8 cell.
#
# Eight transitions require nine trajectory points.
# ----------------------------------------------------------------------

canonical_origin = points[0]

canonical = [
    sub(points[i], canonical_origin)
    for i in range(PERIOD + 1)
]


# ----------------------------------------------------------------------
# Translation vectors.
#
# The dominant structural recurrence is period 8. Use the observed
# displacement of one complete cell as the primary translation vector.
# ----------------------------------------------------------------------

translation = sub(
    points[PERIOD],
    points[0]
)

translation_length = norm(translation)

print()
print("=== PRIMARY TRANSLATION ===")
print(
    "T = "
    f"({translation[0]:.8f}, "
    f"{translation[1]:.8f}, "
    f"{translation[2]:.8f})"
)
print(f"|T| = {translation_length:.8f}")


# ----------------------------------------------------------------------
# Construct three non-collinear lattice vectors.
#
# A single observed translation cannot define a 3D crystal. We therefore
# derive candidate vectors from recurring geometric scales.
#
# T1 = period 8
# T2 = period 6
# T3 = period 11
# ----------------------------------------------------------------------

def displacement(period):
    if period >= N:
        return (0.0, 0.0, 0.0)

    return sub(
        points[period],
        points[0]
    )


T1 = displacement(8)
T2 = displacement(6)
T3 = displacement(11)


# Remove the projection of vectors 2 and 3 onto earlier vectors.
# This gives a Gram-Schmidt orthogonalized basis while preserving
# the observed lattice directions.

e1_len = norm(T1)

if e1_len > EPS:
    e1 = scale(T1, 1.0 / e1_len)
else:
    e1 = (1.0, 0.0, 0.0)


T2_perp = sub(
    T2,
    scale(e1, dot(T2, e1))
)

if norm(T2_perp) > EPS:
    e2 = scale(
        T2_perp,
        1.0 / norm(T2_perp)
    )
else:
    e2 = (0.0, 1.0, 0.0)


T3_perp = sub(
    T3,
    scale(e1, dot(T3, e1))
)

T3_perp = sub(
    T3_perp,
    scale(e2, dot(T3_perp, e2))
)

if norm(T3_perp) > EPS:
    e3 = scale(
        T3_perp,
        1.0 / norm(T3_perp)
    )
else:
    e3 = (0.0, 0.0, 1.0)


# Preserve observed magnitudes.

basis = [
    T1,
    T2_perp,
    T3_perp,
]


print()
print("=== LATTICE BASIS ===")

for i, v in enumerate(basis, 1):
    print(
        f"A{i} = "
        f"({v[0]:.8f}, "
        f"{v[1]:.8f}, "
        f"{v[2]:.8f}) "
        f"|A{i}|={norm(v):.8f}"
    )


# ----------------------------------------------------------------------
# Basis angles.
# ----------------------------------------------------------------------

basis_angles = []

for i in range(3):
    for j in range(i + 1, 3):
        c = cosine(basis[i], basis[j])
        c = max(-1.0, min(1.0, c))

        angle = math.degrees(
            math.acos(c)
        )

        basis_angles.append(
            {
                "a": i + 1,
                "b": j + 1,
                "cosine": c,
                "angle_degrees": angle,
            }
        )


print()
print("=== BASIS ANGLES ===")

for x in basis_angles:
    print(
        f"A{x['a']}-A{x['b']} "
        f"angle={x['angle_degrees']:.6f}° "
        f"cos={x['cosine']:.6f}"
    )


# ----------------------------------------------------------------------
# Construct 3D replicated crystal.
# ----------------------------------------------------------------------

atoms = []

for ix in range(-GRID, GRID + 1):
    for iy in range(-GRID, GRID + 1):
        for iz in range(-GRID, GRID + 1):

            origin = (
                ix * basis[0][0]
                + iy * basis[1][0]
                + iz * basis[2][0],

                ix * basis[0][1]
                + iy * basis[1][1]
                + iz * basis[2][1],

                ix * basis[0][2]
                + iy * basis[1][2]
                + iz * basis[2][2],
            )

            for j, p in enumerate(canonical):

                atoms.append(
                    {
                        "cell": [ix, iy, iz],
                        "local_index": j,
                        "x": origin[0] + p[0],
                        "y": origin[1] + p[1],
                        "z": origin[2] + p[2],
                    }
                )


# ----------------------------------------------------------------------
# Nearest-neighbor statistics.
# ----------------------------------------------------------------------

positions = [
    (
        a["x"],
        a["y"],
        a["z"],
    )
    for a in atoms
]

nearest = []

for i, p in enumerate(positions):

    best = float("inf")

    for j, q in enumerate(positions):

        if i == j:
            continue

        dist = distance(p, q)

        if dist > EPS and dist < best:
            best = dist

    if math.isfinite(best):
        nearest.append(best)


nearest_mean = (
    sum(nearest) / len(nearest)
    if nearest else 0.0
)

nearest_rms = (
    math.sqrt(
        sum(
            x * x
            for x in nearest
        )
        / len(nearest)
    )
    if nearest else 0.0
)

nearest_uniformity = (
    nearest_mean / nearest_rms
    if nearest_rms > EPS
    else 0.0
)


# ----------------------------------------------------------------------
# Unit-cell volume.
#
# |A . (B x C)|
# ----------------------------------------------------------------------

cross23 = (
    basis[1][1] * basis[2][2]
    - basis[1][2] * basis[2][1],

    basis[1][2] * basis[2][0]
    - basis[1][0] * basis[2][2],

    basis[1][0] * basis[2][1]
    - basis[1][1] * basis[2][0],
)

cell_volume = abs(
    dot(
        basis[0],
        cross23
    )
)


# ----------------------------------------------------------------------
# Local canonical-cell bond lengths.
# ----------------------------------------------------------------------

cell_steps = [
    distance(
        canonical[i],
        canonical[i + 1]
    )
    for i in range(PERIOD)
]

cell_step_mean = (
    sum(cell_steps) / len(cell_steps)
)

cell_step_rms = math.sqrt(
    sum(
        x * x
        for x in cell_steps
    )
    / len(cell_steps)
)

cell_step_uniformity = (
    cell_step_mean / cell_step_rms
    if cell_step_rms > EPS
    else 0.0
)


# ----------------------------------------------------------------------
# Print diagnostics.
# ----------------------------------------------------------------------

print()
print("=== 3D CRYSTAL REALIZATION ===")
print(f"Cells per axis = {2 * GRID + 1}")
print(f"Cells          = {(2 * GRID + 1) ** 3}")
print(f"Points/cell    = {len(canonical)}")
print(f"Total points   = {len(atoms)}")
print(f"Cell volume    = {cell_volume:.8f}")

print()
print("=== NEAREST-NEIGHBOR GEOMETRY ===")
print(f"mean distance       = {nearest_mean:.8f}")
print(f"RMS distance        = {nearest_rms:.8f}")
print(f"uniformity          = {nearest_uniformity:.8f}")

print()
print("=== UNIT CELL GEOMETRY ===")
print(f"step mean           = {cell_step_mean:.8f}")
print(f"step RMS            = {cell_step_rms:.8f}")
print(f"step uniformity     = {cell_step_uniformity:.8f}")


# ----------------------------------------------------------------------
# Classification.
#
# This is deliberately diagnostic rather than claiming a physical
# crystal. The generated object is a mathematical lattice realization.
# ----------------------------------------------------------------------

if (
    cell_volume > EPS
    and nearest_uniformity > 0.90
):
    classification = "3D_PERIODIC_LATTICE"
elif cell_volume > EPS:
    classification = "3D_OBLIQUE_FRACTAL_LATTICE"
else:
    classification = "DEGENERATE_LATTICE"


print()
print("=== CLASSIFICATION ===")
print(classification)


result = {
    "schema": "openmind.crystal_realization.v14",

    "source": str(INPUT),

    "lattice_source": str(LATTICE_INPUT),

    "candidate_period": PERIOD,

    "grid": GRID,

    "canonical_cell": [
        {
            "local_index": i,
            "x": p[0],
            "y": p[1],
            "z": p[2],
        }
        for i, p in enumerate(canonical)
    ],

    "basis": [
        {
            "vector": list(v),
            "length": norm(v),
        }
        for v in basis
    ],

    "basis_angles": basis_angles,

    "cell_volume": cell_volume,

    "cell_step_lengths": cell_steps,

    "cell_step_mean": cell_step_mean,

    "cell_step_rms": cell_step_rms,

    "cell_step_uniformity": cell_step_uniformity,

    "replication": {
        "grid": GRID,
        "cells": (2 * GRID + 1) ** 3,
        "points_per_cell": len(canonical),
        "total_points": len(atoms),
    },

    "nearest_neighbor": {
        "mean": nearest_mean,
        "rms": nearest_rms,
        "uniformity": nearest_uniformity,
        "count": len(nearest),
    },

    "classification": classification,

    "atoms": atoms,
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
print("CRYSTAL REALIZATION COMPLETE")
