import json
import math
import random
from pathlib import Path


# ------------------------------------------------------------------
# OPENMIND / V42 GEOMETRY ROBUSTNESS TEST
# ------------------------------------------------------------------
#
# V41 found a strong late-lag slope transition using:
#
#   12-dimensional component RMS vectors
#   Euclidean distance
#   lag range 1..27
#   candidate breakpoints 19..23
#
# V42 asks:
#
#   Does the transition survive:
#
#       1. alternative distance geometries
#       2. removal of endpoint-favorable breakpoints
#       3. quadratic baseline adjustment
#       4. maximum-over-breakpoint permutation correction
#
# IMPORTANT:
#
# All geometries operate on the SAME 12-dimensional RMS vectors.
# This isolates distance geometry from representation changes.
#
# Candidate breakpoints are 12..21.
#
# With max lag = 27, breakpoint 21 leaves six post-breakpoint
# observations (22..27), avoiding the strongest endpoint leverage
# present at V41 breakpoint 23.
#
# ------------------------------------------------------------------


NULL_RUNS = 2500
SEED = 34038

LAG_MIN = 1
LAG_MAX = 27

TRANSITION_MIN = 12
TRANSITION_MAX = 21

INPUT = Path(
    "experiments/model_fractal/"
    "q8_parameter_field_v4_1.json"
)

OUTPUT = Path(
    "experiments/model_fractal/"
    "geometry_scaling_transition_test_v42.json"
)

EPS = 1e-15


COMPONENTS = [
    "attn_norm.weight",
    "ffn_down.weight",
    "ffn_gate.weight",
    "ffn_up.weight",
    "ffn_norm.weight",
    "attn_k.bias",
    "attn_k.weight",
    "attn_output.weight",
    "attn_q.bias",
    "attn_q.weight",
    "attn_v.bias",
    "attn_v.weight",
]


# ------------------------------------------------------------------
# DATA
# ------------------------------------------------------------------

data = json.loads(INPUT.read_text())
layers_data = data["layers"]

layer_ids = sorted(
    layers_data,
    key=lambda x: int(x),
)

vectors = []

for layer_id in layer_ids:
    layer = layers_data[str(layer_id)]

    vector = []

    for component in COMPONENTS:
        value = layer[component]["stats"]["rms"]
        vector.append(float(value))

    vectors.append(vector)


# ------------------------------------------------------------------
# BASIC HELPERS
# ------------------------------------------------------------------

def mean(values):
    return sum(values) / len(values)


def euclidean(a, b):
    return math.sqrt(
        sum(
            (x - y) ** 2
            for x, y in zip(a, b)
        )
    )


def relative_distance(a, b):
    total = 0.0

    for x, y in zip(a, b):
        denominator = max(
            abs(x),
            abs(y),
            EPS,
        )

        delta = (
            (x - y)
            / denominator
        )

        total += delta * delta

    return math.sqrt(total)


def cosine_distance(a, b):
    dot = sum(
        x * y
        for x, y in zip(a, b)
    )

    norm_a = math.sqrt(
        sum(x * x for x in a)
    )

    norm_b = math.sqrt(
        sum(y * y for y in b)
    )

    if (
        norm_a <= EPS
        or norm_b <= EPS
    ):
        return 0.0

    cosine = (
        dot
        / (norm_a * norm_b)
    )

    cosine = max(
        -1.0,
        min(1.0, cosine),
    )

    return 1.0 - cosine


# ------------------------------------------------------------------
# STANDARDIZED GEOMETRY
# ------------------------------------------------------------------

dimension_count = len(vectors[0])

feature_means = []
feature_stds = []

for j in range(dimension_count):

    values = [
        vector[j]
        for vector in vectors
    ]

    m = mean(values)

    variance = mean([
        (x - m) ** 2
        for x in values
    ])

    feature_means.append(m)
    feature_stds.append(
        math.sqrt(variance)
    )


standardized_vectors = []

for vector in vectors:

    standardized = []

    for j, value in enumerate(vector):

        std = feature_stds[j]

        if std > EPS:
            standardized.append(
                (
                    value
                    - feature_means[j]
                )
                / std
            )
        else:
            standardized.append(0.0)

    standardized_vectors.append(
        standardized
    )


def standardized_euclidean(a, b):
    return euclidean(a, b)


# ------------------------------------------------------------------
# GEOMETRY REGISTRY
# ------------------------------------------------------------------

GEOMETRIES = {
    "euclidean_rms": (
        euclidean,
        vectors,
    ),

    "relative_rms": (
        relative_distance,
        vectors,
    ),

    "cosine_rms": (
        cosine_distance,
        vectors,
    ),

    "standardized_euclidean_rms": (
        standardized_euclidean,
        standardized_vectors,
    ),
}


# ------------------------------------------------------------------
# LAG CURVE
# ------------------------------------------------------------------

def build_curve(
    order,
    distance_function,
    geometry_vectors,
):
    curve = []

    for lag in range(
        LAG_MIN,
        LAG_MAX + 1,
    ):

        values = []

        for i in range(
            len(order) - lag
        ):

            values.append(
                distance_function(
                    geometry_vectors[
                        order[i]
                    ],
                    geometry_vectors[
                        order[i + lag]
                    ],
                )
            )

        curve.append(
            (
                lag,
                mean(values),
            )
        )

    return curve


# ------------------------------------------------------------------
# LINEAR ALGEBRA
# ------------------------------------------------------------------

def solve_linear_system(matrix, vector):

    a = [
        [float(x) for x in row]
        + [float(b)]
        for row, b in zip(
            matrix,
            vector,
        )
    ]

    n = len(a)

    for i in range(n):

        pivot = max(
            range(i, n),
            key=lambda r:
                abs(a[r][i]),
        )

        if abs(a[pivot][i]) <= EPS:
            raise ValueError(
                "Singular matrix"
            )

        a[i], a[pivot] = (
            a[pivot],
            a[i],
        )

        p = a[i][i]

        for j in range(
            i,
            n + 1,
        ):
            a[i][j] /= p

        for r in range(n):

            if r == i:
                continue

            factor = a[r][i]

            for j in range(
                i,
                n + 1,
            ):
                a[r][j] -= (
                    factor
                    * a[i][j]
                )

    return [
        a[i][n]
        for i in range(n)
    ]


def least_squares(
    xs,
    ys,
    basis,
):

    design = [
        basis(x)
        for x in xs
    ]

    p = len(design[0])

    matrix = []
    vector = []

    for i in range(p):

        matrix.append([
            sum(
                row[i] * row[j]
                for row in design
            )
            for j in range(p)
        ])

        vector.append(
            sum(
                row[i] * y
                for row, y in zip(
                    design,
                    ys,
                )
            )
        )

    parameters = solve_linear_system(
        matrix,
        vector,
    )

    predictions = [
        sum(
            a * b
            for a, b in zip(
                parameters,
                row,
            )
        )
        for row in design
    ]

    return parameters, predictions


# ------------------------------------------------------------------
# REGRESSION METRICS
# ------------------------------------------------------------------

def regression_metrics(
    ys,
    predictions,
    parameter_count,
):

    n = len(ys)

    residuals = [
        y - p
        for y, p in zip(
            ys,
            predictions,
        )
    ]

    sse = sum(
        r * r
        for r in residuals
    )

    rmse = math.sqrt(
        sse / n
    )

    ymean = mean(ys)

    sst = sum(
        (y - ymean) ** 2
        for y in ys
    )

    r2 = (
        1.0 - sse / sst
        if sst > EPS
        else 0.0
    )

    aic = (
        n * math.log(
            max(sse / n, EPS)
        )
        + 2 * parameter_count
    )

    bic = (
        n * math.log(
            max(sse / n, EPS)
        )
        + parameter_count
        * math.log(n)
    )

    return {
        "sse": sse,
        "rmse": rmse,
        "r2": r2,
        "aic": aic,
        "bic": bic,
    }


# ------------------------------------------------------------------
# MODELS
# ------------------------------------------------------------------

def fit_linear(curve):

    xs = [x for x, _ in curve]
    ys = [y for _, y in curve]

    parameters, predictions = (
        least_squares(
            xs,
            ys,
            lambda x: [
                1.0,
                float(x),
            ],
        )
    )

    return {
        "model": "linear",
        "parameters": parameters,
        **regression_metrics(
            ys,
            predictions,
            2,
        ),
    }


def fit_hinge(
    curve,
    breakpoint,
):

    xs = [x for x, _ in curve]
    ys = [y for _, y in curve]

    k = float(breakpoint)

    parameters, predictions = (
        least_squares(
            xs,
            ys,
            lambda x: [
                1.0,
                float(x),
                max(
                    0.0,
                    float(x) - k,
                ),
            ],
        )
    )

    a, slope_before, slope_change = (
        parameters
    )

    return {
        "model":
            "continuous_hinge",

        "breakpoint":
            breakpoint,

        "parameters":
            parameters,

        "intercept":
            a,

        "slope_before":
            slope_before,

        "slope_after":
            slope_before
            + slope_change,

        "slope_change":
            slope_change,

        **regression_metrics(
            ys,
            predictions,
            3,
        ),
    }


def fit_quadratic(curve):

    xs = [x for x, _ in curve]
    ys = [y for _, y in curve]

    parameters, predictions = (
        least_squares(
            xs,
            ys,
            lambda x: [
                1.0,
                float(x),
                float(x) ** 2,
            ],
        )
    )

    return {
        "model": "quadratic",
        "parameters": parameters,
        **regression_metrics(
            ys,
            predictions,
            3,
        ),
    }


def fit_quadratic_hinge(
    curve,
    breakpoint,
):

    xs = [x for x, _ in curve]
    ys = [y for _, y in curve]

    k = float(breakpoint)

    parameters, predictions = (
        least_squares(
            xs,
            ys,
            lambda x: [
                1.0,
                float(x),
                float(x) ** 2,
                max(
                    0.0,
                    float(x) - k,
                ),
            ],
        )
    )

    return {
        "model":
            "quadratic_hinge",

        "breakpoint":
            breakpoint,

        "parameters":
            parameters,

        **regression_metrics(
            ys,
            predictions,
            4,
        ),
    }


def transition_result(
    curve,
    breakpoint,
):

    linear = fit_linear(curve)

    hinge = fit_hinge(
        curve,
        breakpoint,
    )

    quadratic = fit_quadratic(
        curve
    )

    quadratic_hinge = (
        fit_quadratic_hinge(
            curve,
            breakpoint,
        )
    )

    linear_delta_bic = (
        linear["bic"]
        - hinge["bic"]
    )

    quadratic_delta_bic = (
        quadratic["bic"]
        - quadratic_hinge["bic"]
    )

    return {
        "breakpoint":
            breakpoint,

        "linear":
            linear,

        "hinge":
            hinge,

        "quadratic":
            quadratic,

        "quadratic_hinge":
            quadratic_hinge,

        "linear_delta_bic":
            linear_delta_bic,

        "quadratic_delta_bic":
            quadratic_delta_bic,

        "primary_delta_bic":
            linear_delta_bic,

        "slope_change":
            hinge["slope_change"],

        "slope_before":
            hinge["slope_before"],

        "slope_after":
            hinge["slope_after"],
    }


# ------------------------------------------------------------------
# PERCENTILES / NULL SUMMARY
# ------------------------------------------------------------------

def percentile(values, q):

    ordered = sorted(values)
    n = len(ordered)

    position = q * (n - 1)

    lower = int(
        math.floor(position)
    )

    upper = int(
        math.ceil(position)
    )

    if lower == upper:
        return ordered[lower]

    fraction = position - lower

    return (
        ordered[lower]
        + fraction
        * (
            ordered[upper]
            - ordered[lower]
        )
    )


def summarize_null(
    values,
    real_value,
):

    ordered = sorted(values)

    exceedances = sum(
        x >= real_value
        for x in ordered
    )

    n = len(ordered)

    empirical_p = (
        exceedances + 1
    ) / (
        n + 1
    )

    m = mean(ordered)

    variance = mean([
        (x - m) ** 2
        for x in ordered
    ])

    return {
        "n": n,
        "real": real_value,
        "mean": m,
        "sd": math.sqrt(
            variance
        ),
        "p95": percentile(
            ordered,
            0.95,
        ),
        "p99": percentile(
            ordered,
            0.99,
        ),
        "max": ordered[-1],
        "exceedances":
            exceedances,
        "empirical_p":
            empirical_p,
    }


# ------------------------------------------------------------------
# RUN ONE GEOMETRY
# ------------------------------------------------------------------

def run_geometry(
    name,
    distance_function,
    geometry_vectors,
):

    real_order = list(
        range(len(geometry_vectors))
    )

    real_curve = build_curve(
        real_order,
        distance_function,
        geometry_vectors,
    )

    real_tests = {}

    for breakpoint in range(
        TRANSITION_MIN,
        TRANSITION_MAX + 1,
    ):

        real_tests[str(breakpoint)] = (
            transition_result(
                real_curve,
                breakpoint,
            )
        )

    real_max = max(
        real_tests.values(),
        key=lambda x:
            x["primary_delta_bic"],
    )

    real_max_quadratic = max(
        real_tests.values(),
        key=lambda x:
            x["quadratic_delta_bic"],
    )

    rng = random.Random(
        SEED
    )

    null_primary = {
        str(breakpoint): []
        for breakpoint in range(
            TRANSITION_MIN,
            TRANSITION_MAX + 1,
        )
    }

    null_quadratic = {
        str(breakpoint): []
        for breakpoint in range(
            TRANSITION_MIN,
            TRANSITION_MAX + 1,
        )
    }

    null_max_primary = []
    null_max_quadratic = []

    for _ in range(NULL_RUNS):

        order = list(
            range(len(geometry_vectors))
        )

        rng.shuffle(order)

        curve = build_curve(
            order,
            distance_function,
            geometry_vectors,
        )

        run_primary = []
        run_quadratic = []

        for breakpoint in range(
            TRANSITION_MIN,
            TRANSITION_MAX + 1,
        ):

            test = transition_result(
                curve,
                breakpoint,
            )

            primary = (
                test["primary_delta_bic"]
            )

            quadratic = (
                test["quadratic_delta_bic"]
            )

            null_primary[
                str(breakpoint)
            ].append(primary)

            null_quadratic[
                str(breakpoint)
            ].append(quadratic)

            run_primary.append(
                primary
            )

            run_quadratic.append(
                quadratic
            )

        null_max_primary.append(
            max(run_primary)
        )

        null_max_quadratic.append(
            max(run_quadratic)
        )

    fixed_summary = {}

    for breakpoint in range(
        TRANSITION_MIN,
        TRANSITION_MAX + 1,
    ):

        key = str(breakpoint)

        fixed_summary[key] = {
            "primary_linear_hinge":
                summarize_null(
                    null_primary[key],
                    real_tests[key][
                        "primary_delta_bic"
                    ],
                ),

            "quadratic_hinge":
                summarize_null(
                    null_quadratic[key],
                    real_tests[key][
                        "quadratic_delta_bic"
                    ],
                ),
        }

    max_primary_summary = (
        summarize_null(
            null_max_primary,
            real_max[
                "primary_delta_bic"
            ],
        )
    )

    max_quadratic_summary = (
        summarize_null(
            null_max_quadratic,
            real_max_quadratic[
                "quadratic_delta_bic"
            ],
        )
    )

    return {
        "geometry": name,

        "real_tests":
            real_tests,

        "fixed_breakpoint_null":
            fixed_summary,

        "maximum_over_region": {
            "primary": {
                "breakpoint":
                    real_max[
                        "breakpoint"
                    ],

                "real_delta_bic":
                    real_max[
                        "primary_delta_bic"
                    ],

                "slope_before":
                    real_max[
                        "slope_before"
                    ],

                "slope_after":
                    real_max[
                        "slope_after"
                    ],

                "slope_change":
                    real_max[
                        "slope_change"
                    ],

                "null":
                    max_primary_summary,
            },

            "quadratic_adjusted": {
                "breakpoint":
                    real_max_quadratic[
                        "breakpoint"
                    ],

                "real_delta_bic":
                    real_max_quadratic[
                        "quadratic_delta_bic"
                    ],

                "null":
                    max_quadratic_summary,
            },
        },
    }


# ------------------------------------------------------------------
# EXECUTION
# ------------------------------------------------------------------

print("=" * 72)
print(" OPENMIND / V42 GEOMETRY ROBUSTNESS TEST")
print("=" * 72)

print()
print(
    f"Layers:             {len(vectors)}"
)

print(
    f"Dimensions:         {len(COMPONENTS)}"
)

print(
    f"Lag range:          "
    f"{LAG_MIN}..{LAG_MAX}"
)

print(
    f"Breakpoints:        "
    f"{TRANSITION_MIN}..{TRANSITION_MAX}"
)

print(
    f"Null runs:          {NULL_RUNS}"
)

print(
    f"Seed:               {SEED}"
)

print()

results = {}

for name, (
    distance_function,
    geometry_vectors,
) in GEOMETRIES.items():

    print(
        f"Running geometry: {name}"
    )

    results[name] = run_geometry(
        name,
        distance_function,
        geometry_vectors,
    )


# ------------------------------------------------------------------
# CROSS-GEOMETRY SUMMARY
# ------------------------------------------------------------------

summary = {}

for name, result in results.items():

    primary = result[
        "maximum_over_region"
    ]["primary"]

    quadratic = result[
        "maximum_over_region"
    ]["quadratic_adjusted"]

    summary[name] = {
        "best_breakpoint":
            primary["breakpoint"],

        "primary_delta_bic":
            primary["real_delta_bic"],

        "primary_empirical_p":
            primary["null"][
                "empirical_p"
            ],

        "slope_change":
            primary["slope_change"],

        "quadratic_best_breakpoint":
            quadratic["breakpoint"],

        "quadratic_delta_bic":
            quadratic["real_delta_bic"],

        "quadratic_empirical_p":
            quadratic["null"][
                "empirical_p"
            ],
    }


# ------------------------------------------------------------------
# RESULT
# ------------------------------------------------------------------

result = {
    "schema":
        "openmind.geometry_scaling_transition_test.v42",

    "source":
        str(INPUT),

    "layer_count":
        len(vectors),

    "component_dimension":
        len(COMPONENTS),

    "representation":
        "12_component_layer_RMS_vectors",

    "lag_range": {
        "min": LAG_MIN,
        "max": LAG_MAX,
    },

    "transition_region": {
        "min": TRANSITION_MIN,
        "max": TRANSITION_MAX,
    },

    "minimum_post_breakpoint_lags":
        LAG_MAX - TRANSITION_MAX,

    "null_runs":
        NULL_RUNS,

    "seed":
        SEED,

    "paired_permutation_null":
        True,

    "distance_contract": {
        "euclidean_rms":
            "raw Euclidean distance",

        "relative_rms":
            "feature-wise relative Euclidean distance",

        "cosine_rms":
            "one_minus_cosine_similarity",

        "standardized_euclidean_rms":
            "Euclidean distance after per-component depth z-score",
    },

    "geometries":
        results,

    "cross_geometry_summary":
        summary,
}


OUTPUT.write_text(
    json.dumps(
        result,
        indent=2,
    )
)

print()
print("=" * 72)
print(" V42 COMPLETE")
print("=" * 72)
print()
print(
    f"Output: {OUTPUT}"
)
