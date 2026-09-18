import json
import math
from pathlib import Path

INPUT = Path(
    "experiments/model_fractal/normalized_geometry_v10.json"
)

OUTPUT = Path(
    "experiments/model_fractal/unit_cell_v12.json"
)

EPS = 1e-12

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
print(" OPENMIND / FRACTAL UNIT CELL V12")
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


def scale(a, s):
    return tuple(
        x * s for x in a
    )


def dot(a, b):
    return sum(
        x * y for x, y in zip(a, b)
    )


def norm(a):
    return math.sqrt(dot(a, a))


def cosine(a, b):
    na = norm(a)
    nb = norm(b)

    if na <= EPS or nb <= EPS:
        return 0.0

    return dot(a, b) / (na * nb)


def distance(a, b):
    return norm(sub(a, b))


def mean(values):
    return (
        sum(values) / len(values)
        if values else 0.0
    )


def rms(values):
    if not values:
        return 0.0

    return math.sqrt(
        sum(x * x for x in values) / len(values)
    )


# ----------------------------------------------------------------------
# Evaluate candidate periods
# ----------------------------------------------------------------------

candidate_periods = [4, 5, 6, 7, 8, 10, 11, 13]

results = []

for period in candidate_periods:

    if period >= N:
        continue

    # --------------------------------------------------------------
    # Compare displacement vectors separated by one cell.
    # --------------------------------------------------------------

    translations = []

    for i in range(N - period - 1):
        a = sub(
            points[i + period],
            points[i]
        )

        b = sub(
            points[i + 1 + period],
            points[i + 1]
        )

        translations.append(
            {
                "cosine": cosine(a, b),
                "scale_ratio": (
                    min(norm(a), norm(b))
                    / max(norm(a), norm(b))
                    if max(norm(a), norm(b)) > EPS
                    else 0.0
                ),
            }
        )

    translation_similarity = [
        x["cosine"] * x["scale_ratio"]
        for x in translations
    ]

    # --------------------------------------------------------------
    # Compare complete cells.
    #
    # For each pair of adjacent cells, align them by their first
    # point and measure residual geometric error.
    # --------------------------------------------------------------

    cell_errors = []
    cell_cosines = []
    cell_scale_ratios = []

    cell_count = N // period

    for cell_index in range(cell_count - 1):

        start_a = cell_index * period
        start_b = (cell_index + 1) * period

        # Each cell uses period + 1 trajectory points.
        # Require the complete second cell to remain inside [0, N-1].
        if start_b + period + 1 > N:
            break

        origin_a = points[start_a]
        origin_b = points[start_b]

        vectors_a = [
            sub(points[start_a + j], origin_a)
            for j in range(period + 1)
        ]

        vectors_b = [
            sub(points[start_b + j], origin_b)
            for j in range(period + 1)
        ]

        lengths_a = [
            norm(v) for v in vectors_a[1:]
        ]

        lengths_b = [
            norm(v) for v in vectors_b[1:]
        ]

        scales = []

        for la, lb in zip(lengths_a, lengths_b):
            if la > EPS and lb > EPS:
                scales.append(lb / la)

        cell_scale = mean(scales) if scales else 1.0

        residuals = []

        for va, vb in zip(vectors_a, vectors_b):
            predicted = scale(
                va,
                cell_scale
            )

            residuals.append(
                norm(
                    sub(vb, predicted)
                )
            )

        denominator = max(
            rms([
                norm(v)
                for v in vectors_b
            ]),
            EPS
        )

        normalized_error = (
            rms(residuals) / denominator
        )

        cell_errors.append(normalized_error)

        directional = []

        for va, vb in zip(
            vectors_a[1:],
            vectors_b[1:]
        ):
            directional.append(
                cosine(va, vb)
            )

        cell_cosines.append(
            mean(directional)
        )

        cell_scale_ratios.append(
            cell_scale
        )

    # --------------------------------------------------------------
    # Synthetic reconstruction.
    #
    # Use the first cell as the canonical unit cell and translate it
    # through the observed cell origins.
    # --------------------------------------------------------------

    reconstruction_errors = []

    if cell_count >= 2:

        canonical_origin = points[0]

        canonical = [
            sub(
                points[j],
                canonical_origin
            )
            for j in range(period + 1)
        ]

        for cell_index in range(1, cell_count):

            target_start = cell_index * period

            # A complete cell requires period + 1 points.
            # The final required index is target_start + period.
            if target_start + period >= N:
                break

            target_origin = points[target_start]

            # Determine best scalar scale from the target cell.
            numerator = 0.0
            denominator = 0.0

            for j in range(1, period + 1):

                ca = canonical[j]
                tb = sub(
                    points[target_start + j],
                    target_origin
                )

                numerator += dot(ca, tb)
                denominator += dot(ca, ca)

            cell_scale = (
                numerator / denominator
                if denominator > EPS
                else 1.0
            )

            predicted = [
                add(
                    target_origin,
                    scale(v, cell_scale)
                )
                for v in canonical
            ]

            actual = [
                points[target_start + j]
                for j in range(period + 1)
            ]

            errors = [
                distance(a, p)
                for a, p in zip(actual, predicted)
            ]

            reconstruction_errors.append(
                rms(errors)
            )

    reconstruction_error = mean(
        reconstruction_errors
    )

    results.append(
        {
            "period": period,
            "cell_count": cell_count,

            "translation_similarity_mean":
                mean(translation_similarity),

            "translation_similarity_rms":
                rms(translation_similarity),

            "cell_error_mean":
                mean(cell_errors),

            "cell_error_rms":
                rms(cell_errors),

            "cell_cosine_mean":
                mean(cell_cosines),

            "cell_scale_mean":
                mean(cell_scale_ratios),

            "cell_scale_rms":
                rms(cell_scale_ratios),

            "reconstruction_error":
                reconstruction_error,
        }
    )


# ----------------------------------------------------------------------
# Rank by reconstruction quality
# ----------------------------------------------------------------------

ranked = sorted(
    results,
    key=lambda x: (
        x["reconstruction_error"],
        -x["cell_cosine_mean"],
    )
)


print()
print("=== UNIT CELL CANDIDATES ===")

for r in ranked:
    print(
        f"period={r['period']:2d} "
        f"reconstruction={r['reconstruction_error']:.8f} "
        f"cell_cos={r['cell_cosine_mean']:.8f} "
        f"translation={r['translation_similarity_mean']:.8f}"
    )


best = ranked[0]

print()
print("=== BEST UNIT CELL ===")
print(
    f"period       = {best['period']}"
)
print(
    f"reconstruction = "
    f"{best['reconstruction_error']:.8f}"
)
print(
    f"cell cosine   = "
    f"{best['cell_cosine_mean']:.8f}"
)
print(
    f"translation   = "
    f"{best['translation_similarity_mean']:.8f}"
)


# ----------------------------------------------------------------------
# Extract canonical unit cell
# ----------------------------------------------------------------------

period = best["period"]

canonical_cell = [
    {
        "index": i,
        "x": points[i][0],
        "y": points[i][1],
        "z": points[i][2],
    }
    for i in range(period + 1)
]


result = {
    "schema":
        "openmind.fractal_unit_cell.v12",

    "source":
        str(INPUT),

    "layer_count":
        N,

    "candidate_periods":
        candidate_periods,

    "results":
        results,

    "best_period":
        period,

    "best_metrics":
        best,

    "canonical_unit_cell":
        canonical_cell,
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
print("FRACTAL UNIT CELL ANALYSIS COMPLETE")
