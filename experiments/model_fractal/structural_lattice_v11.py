import json
import math
from pathlib import Path

INPUT = Path(
    "experiments/model_fractal/normalized_geometry_v10.json"
)

OUTPUT = Path(
    "experiments/model_fractal/structural_lattice_v11.json"
)

EPS = 1e-12

d = json.loads(INPUT.read_text())

# V10 schema:
# layer_coordinates = 28 layer points, L00 ... L27
trajectory = d["layer_coordinates"]

points = [
    (
        float(p["x"]),
        float(p["y"]),
        float(p["z"]),
    )
    for p in trajectory
]

print("=" * 72)
print(" OPENMIND / STRUCTURAL LATTICE V11")
print("=" * 72)

print()
print(f"Layers: {len(points)}")


def sub(a, b):
    return tuple(
        x - y
        for x, y in zip(a, b)
    )


def dot(a, b):
    return sum(
        x * y
        for x, y in zip(a, b)
    )


def norm(v):
    return math.sqrt(dot(v, v))


def cosine(a, b):
    na = norm(a)
    nb = norm(b)

    if na <= EPS or nb <= EPS:
        return 0.0

    return dot(a, b) / (na * nb)


# ----------------------------------------------------------------------
# Step vectors
# ----------------------------------------------------------------------

steps = [
    sub(points[i + 1], points[i])
    for i in range(len(points) - 1)
]

step_lengths = [
    norm(v)
    for v in steps
]


# ----------------------------------------------------------------------
# Turning geometry
# ----------------------------------------------------------------------

turns = []

for i in range(1, len(steps)):

    c = cosine(
        steps[i - 1],
        steps[i]
    )

    c = max(-1.0, min(1.0, c))

    angle = math.acos(c)

    turns.append(
        {
            "layer": i,
            "cosine": c,
            "angle": angle,
            "angle_degrees": math.degrees(angle),
        }
    )


ranked_turns = sorted(
    turns,
    key=lambda x: x["angle"],
    reverse=True,
)


print()
print("=== SHARPEST TURNS ===")

for t in ranked_turns[:10]:

    print(
        f"L{t['layer']-1:02d}->L{t['layer']:02d}->"
        f"L{t['layer']+1:02d} "
        f"angle={t['angle_degrees']:.6f}° "
        f"cos={t['cosine']:.6f}"
    )


# ----------------------------------------------------------------------
# Step-direction recurrence
# ----------------------------------------------------------------------

recurrences = []

for period in range(1, 14):

    local = []

    for i in range(
        len(steps) - period
    ):

        a = steps[i]
        b = steps[i + period]

        direction = abs(
            cosine(a, b)
        )

        scale_ratio = (
            min(norm(a), norm(b))
            / max(norm(a), norm(b))
            if max(norm(a), norm(b)) > EPS
            else 0.0
        )

        local.append(
            direction * scale_ratio
        )

    if local:

        rms = math.sqrt(
            sum(x * x for x in local)
            / len(local)
        )

        mean = sum(local) / len(local)

        recurrences.append(
            {
                "period": period,
                "count": len(local),
                "mean_similarity": mean,
                "rms_similarity": rms,
                "max_similarity": max(local),
            }
        )


ranked_recurrences = sorted(
    recurrences,
    key=lambda x: x["rms_similarity"],
    reverse=True,
)


print()
print("=== STEP RECURRENCE ===")

for r in ranked_recurrences[:10]:

    print(
        f"period={r['period']:2d} "
        f"rms={r['rms_similarity']:.8f} "
        f"mean={r['mean_similarity']:.8f} "
        f"max={r['max_similarity']:.8f}"
    )


# ----------------------------------------------------------------------
# Translation recurrence
#
# Compare displacement vectors separated by a candidate period.
# ----------------------------------------------------------------------

translation_recurrence = []

for period in range(1, 14):

    local = []

    for i in range(
        len(points) - period
    ):

        if i + period >= len(points):
            break

        a = sub(
            points[i + period],
            points[i],
        )

        j = i + 1

        if j + period >= len(points):
            break

        b = sub(
            points[j + period],
            points[j],
        )

        na = norm(a)
        nb = norm(b)

        if na <= EPS or nb <= EPS:
            continue

        direction = abs(
            cosine(a, b)
        )

        scale_ratio = (
            min(na, nb) / max(na, nb)
        )

        local.append(
            direction * scale_ratio
        )

    if local:

        translation_recurrence.append(
            {
                "period": period,
                "count": len(local),
                "mean_similarity":
                    sum(local) / len(local),
                "rms_similarity":
                    math.sqrt(
                        sum(x * x for x in local)
                        / len(local)
                    ),
                "max_similarity":
                    max(local),
            }
        )


translation_recurrence.sort(
    key=lambda x:
        x["rms_similarity"],
    reverse=True,
)


print()
print("=== TRANSLATION RECURRENCE ===")

for r in translation_recurrence[:10]:

    print(
        f"period={r['period']:2d} "
        f"rms={r['rms_similarity']:.8f} "
        f"mean={r['mean_similarity']:.8f} "
        f"max={r['max_similarity']:.8f}"
    )


# ----------------------------------------------------------------------
# Candidate lattice basis
# ----------------------------------------------------------------------

candidate_periods = [
    r["period"]
    for r in ranked_recurrences[:5]
]


basis_candidates = []

for period in candidate_periods:

    if period >= len(points):
        continue

    basis = sub(
        points[period],
        points[0],
    )

    basis_length = norm(basis)

    basis_candidates.append(
        {
            "period": period,
            "basis_vector": {
                "x": basis[0],
                "y": basis[1],
                "z": basis[2],
            },
            "basis_length": basis_length,
        }
    )


# ----------------------------------------------------------------------
# Pairwise layer distances
# ----------------------------------------------------------------------

distance_scales = []

for separation in range(1, 14):

    values = []

    for i in range(
        len(points) - separation
    ):

        values.append(
            norm(
                sub(
                    points[i + separation],
                    points[i],
                )
            )
        )

    if values:

        mean = sum(values) / len(values)

        variance = (
            sum(
                (x - mean) ** 2
                for x in values
            )
            / len(values)
        )

        distance_scales.append(
            {
                "separation": separation,
                "count": len(values),
                "mean_distance": mean,
                "std_distance": math.sqrt(
                    variance
                ),
                "min_distance": min(values),
                "max_distance": max(values),
            }
        )


# ----------------------------------------------------------------------
# Closure
# ----------------------------------------------------------------------

closure_distance = float(
    d["closure_distance"]
)

path_length = float(
    d["path_length"]
)

closure_ratio = (
    closure_distance / path_length
    if path_length > EPS
    else 0.0
)


# ----------------------------------------------------------------------
# Structural diagnostics
# ----------------------------------------------------------------------

if step_lengths:

    mean_step = (
        sum(step_lengths)
        / len(step_lengths)
    )

    variance_step = (
        sum(
            (x - mean_step) ** 2
            for x in step_lengths
        )
        / len(step_lengths)
    )

    step_cv = (
        math.sqrt(variance_step)
        / max(mean_step, EPS)
    )

else:

    mean_step = 0.0
    step_cv = 0.0


best_recurrence = (
    ranked_recurrences[0]
    if ranked_recurrences
    else None
)

best_period = (
    best_recurrence["period"]
    if best_recurrence
    else None
)

best_recurrence_score = (
    best_recurrence["rms_similarity"]
    if best_recurrence
    else 0.0
)

uniformity_score = (
    1.0 / (1.0 + step_cv)
)

closure_score = (
    1.0
    if closure_ratio <= 1e-10
    else 1.0 / (1.0 + closure_ratio)
)

structural_score = (
    0.45 * best_recurrence_score
    + 0.30 * uniformity_score
    + 0.25 * closure_score
)


# ----------------------------------------------------------------------
# Output
# ----------------------------------------------------------------------

result = {

    "schema":
        "openmind.structural_lattice.v11",

    "source":
        str(INPUT),

    "layer_count":
        len(points),

    "transition_count":
        len(steps),

    "geometry": {

        "path_length":
            path_length,

        "closure_distance":
            closure_distance,

        "closure_ratio":
            closure_ratio,

        "mean_step_length":
            mean_step,

        "step_length_coefficient_variation":
            step_cv,
    },

    "turning_geometry":
        turns,

    "ranked_turns":
        ranked_turns,

    "step_recurrence":
        ranked_recurrences,

    "translation_recurrence":
        translation_recurrence,

    "candidate_lattice_basis":
        basis_candidates,

    "distance_scales":
        distance_scales,

    "structural_diagnostics": {

        "best_period":
            best_period,

        "best_recurrence_score":
            best_recurrence_score,

        "uniformity_score":
            uniformity_score,

        "closure_score":
            closure_score,

        "structural_score":
            structural_score,
    },

    "layer_coordinates":
        trajectory,

    "interpretation": {

        "status":
            "candidate_lattice_geometry",

        "physical_crystal_claim":
            False,

        "note":
            "The structure represents recurrence and geometric "
            "organization in a neural-network parameter trajectory. "
            "It does not by itself establish a physical crystalline "
            "material structure.",
    },
}


OUTPUT.write_text(
    json.dumps(
        result,
        indent=2,
    )
)


print()
print("=== LATTICE DIAGNOSTICS ===")

print(
    f"best period       = "
    f"{best_period}"
)

print(
    f"recurrence score  = "
    f"{best_recurrence_score:.8f}"
)

print(
    f"uniformity score  = "
    f"{uniformity_score:.8f}"
)

print(
    f"closure score     = "
    f"{closure_score:.8f}"
)

print(
    f"structural score  = "
    f"{structural_score:.8f}"
)

print()
print("=== CANDIDATE LATTICE BASIS ===")

for b in basis_candidates:

    v = b["basis_vector"]

    print(
        f"period={b['period']:2d} "
        f"basis=("
        f"{v['x']:.6f}, "
        f"{v['y']:.6f}, "
        f"{v['z']:.6f}) "
        f"length={b['basis_length']:.8f}"
    )


print()
print(f"Output: {OUTPUT}")
print()
print("STRUCTURAL LATTICE ANALYSIS COMPLETE")
