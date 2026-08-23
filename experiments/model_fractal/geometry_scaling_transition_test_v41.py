import json
import math
import random
from pathlib import Path


# ------------------------------------------------------------------
# OPENMIND / V41 CONTINUOUS TRANSITION TEST
# ------------------------------------------------------------------
#
# Purpose:
#
#   V40 established a broad late-lag breakpoint ridge around 19..23.
#
#   V41 asks a different question:
#
#       Does the lag-distance curve exhibit a statistically
#       detectable CHANGE IN SLOPE across that region?
#
#   The primary model is a continuous hinge:
#
#       y = a + b*x + c*max(0, x-k)
#
#   where:
#
#       b = pre-transition slope
#       c = slope change
#       k = fixed candidate transition
#
#   Null:
#
#       c = 0
#
#   The primary test statistic is improvement in BIC over the
#   corresponding global linear model.
#
#   We additionally compute the maximum statistic across k=19..23
#   and evaluate that maximum under the same paired permutation null.
#
# ------------------------------------------------------------------


NULL_RUNS = 2500
SEED = 34038

TRANSITION_MIN = 19
TRANSITION_MAX = 23

INPUT = Path(
    "experiments/model_fractal/q8_parameter_field_v4_1.json"
)

OUTPUT = Path(
    "experiments/model_fractal/"
    "geometry_scaling_transition_test_v41.json"
)

EPS = 1e-15


components = [
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


WINDOW = (1, 27)


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

    for component in components:
        value = layer[component]["stats"]["rms"]
        vector.append(float(value))

    vectors.append(vector)


def mean(values):
    return sum(values) / len(values)


def distance(a, b):
    return math.sqrt(
        sum(
            (x - y) ** 2
            for x, y in zip(a, b)
        )
    )


def build_curve(order):
    return [
        (
            lag,
            mean([
                distance(
                    vectors[order[i]],
                    vectors[order[i + lag]],
                )
                for i in range(
                    len(order) - lag
                )
            ]),
        )
        for lag in range(
            WINDOW[0],
            WINDOW[1] + 1,
        )
    ]


# ------------------------------------------------------------------
# LINEAR ALGEBRA
# ------------------------------------------------------------------

def solve_linear_system(matrix, vector):
    a = [
        [float(x) for x in row] + [float(b)]
        for row, b in zip(matrix, vector)
    ]

    n = len(a)

    for i in range(n):
        pivot = max(
            range(i, n),
            key=lambda r: abs(a[r][i]),
        )

        if abs(a[pivot][i]) <= EPS:
            raise ValueError("Singular matrix")

        a[i], a[pivot] = (
            a[pivot],
            a[i],
        )

        p = a[i][i]

        for j in range(i, n + 1):
            a[i][j] /= p

        for r in range(n):
            if r == i:
                continue

            factor = a[r][i]

            for j in range(i, n + 1):
                a[r][j] -= (
                    factor * a[i][j]
                )

    return [
        a[i][n]
        for i in range(n)
    ]


def least_squares(xs, ys, basis):
    """
    Generic ordinary least squares.

    basis(x) returns the design-vector for x.
    """

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


def regression_metrics(
    ys,
    predictions,
    parameter_count,
):
    n = len(ys)

    residuals = [
        y - p
        for y, p in zip(ys, predictions)
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
        + parameter_count * math.log(n)
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

    parameters, predictions = least_squares(
        xs,
        ys,
        lambda x: [1.0, float(x)],
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


def fit_hinge(curve, breakpoint):
    """
    Continuous piecewise-linear hinge:

        y = a + b*x + c*max(0, x-k)

    c is the slope change.
    """

    xs = [x for x, _ in curve]
    ys = [y for _, y in curve]

    k = float(breakpoint)

    parameters, predictions = least_squares(
        xs,
        ys,
        lambda x: [
            1.0,
            float(x),
            max(0.0, float(x) - k),
        ],
    )

    a, slope_before, slope_change = parameters

    return {
        "model": "continuous_hinge",
        "breakpoint": breakpoint,
        "parameters": parameters,
        "intercept": a,
        "slope_before": slope_before,
        "slope_after": (
            slope_before + slope_change
        ),
        "slope_change": slope_change,
        **regression_metrics(
            ys,
            predictions,
            3,
        ),
    }


def fit_quadratic(curve):
    xs = [x for x, _ in curve]
    ys = [y for _, y in curve]

    parameters, predictions = least_squares(
        xs,
        ys,
        lambda x: [
            1.0,
            float(x),
            float(x) ** 2,
        ],
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


def fit_quadratic_hinge(curve, breakpoint):
    """
    Continuous quadratic + hinge:

        y = a
            + b*x
            + d*x^2
            + c*max(0, x-k)

    c is the local slope discontinuity/change
    relative to the quadratic baseline.
    """

    xs = [x for x, _ in curve]
    ys = [y for _, y in curve]

    k = float(breakpoint)

    parameters, predictions = least_squares(
        xs,
        ys,
        lambda x: [
            1.0,
            float(x),
            float(x) ** 2,
            max(0.0, float(x) - k),
        ],
    )

    return {
        "model": "quadratic_hinge",
        "breakpoint": breakpoint,
        "parameters": parameters,
        **regression_metrics(
            ys,
            predictions,
            4,
        ),
    }


# ------------------------------------------------------------------
# TEST STATISTIC
# ------------------------------------------------------------------

def transition_result(curve, breakpoint):
    linear = fit_linear(curve)
    hinge = fit_hinge(
        curve,
        breakpoint,
    )

    quadratic = fit_quadratic(curve)
    quadratic_hinge = fit_quadratic_hinge(
        curve,
        breakpoint,
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
        "breakpoint": breakpoint,
        "linear": linear,
        "hinge": hinge,
        "quadratic": quadratic,
        "quadratic_hinge": quadratic_hinge,
        "linear_delta_bic": linear_delta_bic,
        "quadratic_delta_bic": quadratic_delta_bic,
        "primary_delta_bic": linear_delta_bic,
        "slope_change": hinge["slope_change"],
        "slope_before": hinge["slope_before"],
        "slope_after": hinge["slope_after"],
    }


# ------------------------------------------------------------------
# REAL DATA
# ------------------------------------------------------------------

real_order = list(range(len(vectors)))
real_curve = build_curve(real_order)

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
    key=lambda x: x["primary_delta_bic"],
)


real_max_primary = real_max[
    "primary_delta_bic"
]


real_max_quadratic = max(
    real_tests.values(),
    key=lambda x: x["quadratic_delta_bic"],
)


# ------------------------------------------------------------------
# PAIRED PERMUTATION NULL
# ------------------------------------------------------------------

rng = random.Random(SEED)

permutations = []

for _ in range(NULL_RUNS):
    order = list(range(len(vectors)))
    rng.shuffle(order)
    permutations.append(order)


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


for order in permutations:
    curve = build_curve(order)

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

        primary = test["primary_delta_bic"]
        quadratic = test["quadratic_delta_bic"]

        null_primary[
            str(breakpoint)
        ].append(primary)

        null_quadratic[
            str(breakpoint)
        ].append(quadratic)

        run_primary.append(primary)
        run_quadratic.append(quadratic)

    null_max_primary.append(
        max(run_primary)
    )

    null_max_quadratic.append(
        max(run_quadratic)
    )


# ------------------------------------------------------------------
# NULL SUMMARY
# ------------------------------------------------------------------

def percentile(values, q):
    ordered = sorted(values)
    n = len(ordered)

    position = q * (n - 1)

    lower = int(math.floor(position))
    upper = int(math.ceil(position))

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


def summarize_null(values, real_value):
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
        "sd": math.sqrt(variance),
        "p95": percentile(
            ordered,
            0.95,
        ),
        "p99": percentile(
            ordered,
            0.99,
        ),
        "max": ordered[-1],
        "exceedances": exceedances,
        "empirical_p": empirical_p,
    }


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


# Maximum-over-region test.

max_primary_summary = summarize_null(
    null_max_primary,
    real_max_primary,
)

max_quadratic_summary = summarize_null(
    null_max_quadratic,
    real_max_quadratic[
        "quadratic_delta_bic"
    ],
)


# ------------------------------------------------------------------
# RESULT
# ------------------------------------------------------------------

result = {
    "schema":
        "openmind.geometry_scaling_transition_test.v41",

    "source":
        str(INPUT),

    "layer_count":
        len(vectors),

    "component_dimension":
        len(components),

    "lag_range":
        {
            "min": WINDOW[0],
            "max": WINDOW[1],
        },

    "transition_region":
        {
            "min": TRANSITION_MIN,
            "max": TRANSITION_MAX,
        },

    "null_runs":
        NULL_RUNS,

    "seed":
        SEED,

    "paired_permutation_null":
        True,

    "primary_test":
        "continuous_linear_hinge",

    "primary_statistic":
        "linear_bic_minus_hinge_bic",

    "real_tests":
        real_tests,

    "fixed_breakpoint_null":
        fixed_summary,

    "maximum_over_region":
        {
            "primary":
                {
                    "breakpoint":
                        real_max[
                            "breakpoint"
                        ],
                    "real_delta_bic":
                        real_max_primary,
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

            "quadratic_adjusted":
                {
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


OUTPUT.write_text(
    json.dumps(
        result,
        indent=2,
    )
)


# ------------------------------------------------------------------
# REPORT
# ------------------------------------------------------------------

print("=" * 110)
print("OPENMIND / V41 CONTINUOUS TRANSITION TEST")
print("=" * 110)

print()
print("CONFIGURATION")
print()
print(f"  permutation runs={NULL_RUNS}")
print(f"  seed={SEED}")
print(
    "  paired permutation null=True"
)
print(
    f"  transition region="
    f"{TRANSITION_MIN}..{TRANSITION_MAX}"
)

print()
print("FIXED TRANSITION TESTS")
print()

print(
    f"{'BP':>3}  "
    f"{'ΔBIC(linear→hinge)':>20}  "
    f"{'p':>9}  "
    f"{'slope_before':>14}  "
    f"{'slope_after':>14}  "
    f"{'Δslope':>14}"
)

print("-" * 110)

for breakpoint in range(
    TRANSITION_MIN,
    TRANSITION_MAX + 1,
):
    key = str(breakpoint)
    test = real_tests[key]
    null = fixed_summary[key][
        "primary_linear_hinge"
    ]

    print(
        f"{breakpoint:3d}  "
        f"{test['primary_delta_bic']:20.6f}  "
        f"{null['empirical_p']:9.6f}  "
        f"{test['slope_before']:14.8f}  "
        f"{test['slope_after']:14.8f}  "
        f"{test['slope_change']:14.8f}"
    )

print()
print("MAXIMUM-OVER-REGION TEST")
print()

print(
    f"  selected BP={real_max['breakpoint']}"
)

print(
    f"  max ΔBIC={real_max_primary:.6f}"
)

print(
    f"  max-region empirical p="
    f"{max_primary_summary['empirical_p']:.6f}"
)

print(
    f"  null p95="
    f"{max_primary_summary['p95']:.6f}"
)

print(
    f"  null p99="
    f"{max_primary_summary['p99']:.6f}"
)

print(
    f"  null max="
    f"{max_primary_summary['max']:.6f}"
)

print()
print("SLOPE EFFECT")
print()

print(
    f"  slope before="
    f"{real_max['slope_before']:.8f}"
)

print(
    f"  slope after="
    f"{real_max['slope_after']:.8f}"
)

print(
    f"  slope change="
    f"{real_max['slope_change']:.8f}"
)

print()
print("QUADRATIC-ADJUSTED TRANSITION")
print()

print(
    f"  strongest BP="
    f"{real_max_quadratic['breakpoint']}"
)

print(
    f"  ΔBIC="
    f"{real_max_quadratic['quadratic_delta_bic']:.6f}"
)

print(
    f"  max-region p="
    f"{max_quadratic_summary['empirical_p']:.6f}"
)

print()
print("INTERPRETATION")

if max_primary_summary["empirical_p"] < 0.05:
    print(
        "  PASS: the maximum continuous slope transition "
        "across BP 19..23 exceeds the paired permutation null."
    )
else:
    print(
        "  WARN: the maximum continuous slope transition "
        "does not exceed the paired permutation null at p<.05."
    )

if max_quadratic_summary["empirical_p"] < 0.05:
    print(
        "  PASS: the transition remains significant after "
        "allowing global quadratic curvature."
    )
else:
    print(
        "  NOTE: quadratic adjustment removes fixed-region "
        "significance; curvature may explain the ridge."
    )

print()
print("OUTPUT:", OUTPUT)
print("=" * 110)
