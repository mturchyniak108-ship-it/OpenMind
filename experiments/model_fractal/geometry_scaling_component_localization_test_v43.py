import json
import math
import random
from pathlib import Path


# ================================================================
# OPENMIND / V43 COMPONENT LOCALIZATION TEST
# ================================================================
#
# V42 established that the strongest transition is consistently
# located at BP=21 across four distance geometries.
#
# V43 asks:
#
#   Is the BP=21 transition distributed across the parameter field,
#   or concentrated in a small subset of components?
#
# BP=21 is FIXED.
# No breakpoint search is performed here.
#
# Each component is tested independently using its RMS value across
# depth.
#
# Primary model:
#
#   y = a + b*x + c*max(0, x-21)
#
# Null:
#
#   c = 0
#
# Test statistic:
#
#   linear BIC - hinge BIC
#
# We also fit a quadratic baseline:
#
#   y = a + b*x + d*x^2
#
# and quadratic + hinge:
#
#   y = a + b*x + d*x^2 + c*max(0,x-21)
#
# Null distribution:
#
#   permutation of layer order.
#
# ================================================================


NULL_RUNS = 2500
SEED = 34038

BREAKPOINT = 21

LAG_MIN = 1
LAG_MAX = 27

INPUT = Path(
    "experiments/model_fractal/"
    "q8_parameter_field_v4_1.json"
)

OUTPUT = Path(
    "experiments/model_fractal/"
    "geometry_scaling_component_localization_test_v43.json"
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


# ================================================================
# DATA
# ================================================================

data = json.loads(INPUT.read_text())

layers_data = data["layers"]

layer_ids = sorted(
    layers_data,
    key=lambda x: int(x),
)

component_series = {
    component: []
    for component in COMPONENTS
}

for layer_id in layer_ids:

    layer = layers_data[str(layer_id)]

    for component in COMPONENTS:

        value = layer[component]["stats"]["rms"]

        component_series[component].append(
            float(value)
        )


# ================================================================
# BASIC HELPERS
# ================================================================

def mean(values):
    return sum(values) / len(values)


def percentile(values, q):

    ordered = sorted(values)

    n = len(ordered)

    position = q * (n - 1)

    lo = int(math.floor(position))
    hi = int(math.ceil(position))

    if lo == hi:
        return ordered[lo]

    fraction = position - lo

    return (
        ordered[lo]
        + fraction
        * (
            ordered[hi]
            - ordered[lo]
        )
    )


# ================================================================
# DISTANCE GEOMETRIES
# ================================================================

def euclidean(a, b):

    return abs(a - b)


def relative(a, b):

    denominator = max(
        abs(a),
        abs(b),
        EPS,
    )

    return abs(a - b) / denominator


def cosine_scalar(a, b):

    # For scalar positive RMS values, cosine similarity is 1
    # whenever both values are nonzero. Therefore scalar cosine
    # cannot localize magnitude transitions and is deliberately
    # represented as unavailable rather than producing a false
    # result.
    #
    # V42 cosine operates on the complete 12-D vector. V43 uses
    # scalar components, so cosine is not a meaningful component
    # level distance.
    return None


# ================================================================
# STANDARDIZATION
# ================================================================

standardized_series = {}

for component, values in component_series.items():

    m = mean(values)

    variance = mean([
        (x - m) ** 2
        for x in values
    ])

    std = math.sqrt(variance)

    if std <= EPS:
        standardized_series[component] = [
            0.0
            for _ in values
        ]

    else:
        standardized_series[component] = [
            (x - m) / std
            for x in values
        ]


# ================================================================
# LAG CURVE
# ================================================================

def build_curve(
    values,
    distance_function,
    order,
):

    curve = []

    for lag in range(
        LAG_MIN,
        LAG_MAX + 1,
    ):

        distances = []

        for i in range(
            len(order) - lag
        ):

            a = values[
                order[i]
            ]

            b = values[
                order[i + lag]
            ]

            d = distance_function(
                a,
                b,
            )

            distances.append(d)

        curve.append(
            (
                lag,
                mean(distances),
            )
        )

    return curve


# ================================================================
# LINEAR ALGEBRA
# ================================================================

def solve_linear_system(
    matrix,
    vector,
):

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


# ================================================================
# METRICS
# ================================================================

def metrics(
    ys,
    predictions,
    parameter_count,
):

    n = len(ys)

    sse = sum(
        (y - p) ** 2
        for y, p in zip(
            ys,
            predictions,
        )
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
        "bic": bic,
    }


# ================================================================
# MODELS
# ================================================================

def fit_linear(curve):

    xs = [x for x, _ in curve]
    ys = [y for _, y in curve]

    params, predictions = least_squares(
        xs,
        ys,
        lambda x: [
            1.0,
            float(x),
        ],
    )

    return {
        "parameters": params,
        **metrics(
            ys,
            predictions,
            2,
        ),
    }


def fit_hinge(curve):

    xs = [x for x, _ in curve]
    ys = [y for _, y in curve]

    k = float(BREAKPOINT)

    params, predictions = least_squares(
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

    a, slope_before, slope_change = params

    return {
        "parameters": params,
        "intercept": a,
        "slope_before":
            slope_before,
        "slope_after":
            slope_before
            + slope_change,
        "slope_change":
            slope_change,
        **metrics(
            ys,
            predictions,
            3,
        ),
    }


def fit_quadratic(curve):

    xs = [x for x, _ in curve]
    ys = [y for _, y in curve]

    params, predictions = least_squares(
        xs,
        ys,
        lambda x: [
            1.0,
            float(x),
            float(x) ** 2,
        ],
    )

    return {
        "parameters": params,
        **metrics(
            ys,
            predictions,
            3,
        ),
    }


def fit_quadratic_hinge(curve):

    xs = [x for x, _ in curve]
    ys = [y for _, y in curve]

    k = float(BREAKPOINT)

    params, predictions = least_squares(
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

    return {
        "parameters": params,
        **metrics(
            ys,
            predictions,
            4,
        ),
    }


# ================================================================
# ONE OBSERVED TEST
# ================================================================

def observed_test(
    values,
    distance_function,
    order,
):

    curve = build_curve(
        values,
        distance_function,
        order,
    )

    linear = fit_linear(curve)
    hinge = fit_hinge(curve)

    quadratic = fit_quadratic(curve)
    quadratic_hinge = (
        fit_quadratic_hinge(curve)
    )

    return {
        "linear_delta_bic":
            linear["bic"]
            - hinge["bic"],

        "quadratic_delta_bic":
            quadratic["bic"]
            - quadratic_hinge["bic"],

        "slope_before":
            hinge["slope_before"],

        "slope_after":
            hinge["slope_after"],

        "slope_change":
            hinge["slope_change"],

        "curve":
            curve,
    }


# ================================================================
# PERMUTATION TEST
# ================================================================

def permutation_test(
    values,
    distance_function,
    observed,
):

    rng = random.Random(
        SEED
    )

    null_primary = []
    null_quadratic = []

    base_order = list(
        range(len(values))
    )

    for _ in range(NULL_RUNS):

        order = base_order[:]

        rng.shuffle(order)

        test = observed_test(
            values,
            distance_function,
            order,
        )

        null_primary.append(
            test["linear_delta_bic"]
        )

        null_quadratic.append(
            test["quadratic_delta_bic"]
        )

    real_primary = observed[
        "linear_delta_bic"
    ]

    real_quadratic = observed[
        "quadratic_delta_bic"
    ]

    primary_exceedances = sum(
        x >= real_primary
        for x in null_primary
    )

    quadratic_exceedances = sum(
        x >= real_quadratic
        for x in null_quadratic
    )

    return {
        "primary": {
            "n": NULL_RUNS,
            "mean":
                mean(null_primary),
            "sd":
                math.sqrt(
                    mean([
                        (
                            x
                            - mean(null_primary)
                        ) ** 2
                        for x in null_primary
                    ])
                ),
            "p95":
                percentile(
                    null_primary,
                    0.95,
                ),
            "p99":
                percentile(
                    null_primary,
                    0.99,
                ),
            "max":
                max(null_primary),
            "exceedances":
                primary_exceedances,
            "empirical_p":
                (
                    primary_exceedances
                    + 1
                )
                / (
                    NULL_RUNS
                    + 1
                ),
        },

        "quadratic": {
            "n": NULL_RUNS,
            "mean":
                mean(null_quadratic),
            "sd":
                math.sqrt(
                    mean([
                        (
                            x
                            - mean(
                                null_quadratic
                            )
                        ) ** 2
                        for x in null_quadratic
                    ])
                ),
            "p95":
                percentile(
                    null_quadratic,
                    0.95,
                ),
            "p99":
                percentile(
                    null_quadratic,
                    0.99,
                ),
            "max":
                max(null_quadratic),
            "exceedances":
                quadratic_exceedances,
            "empirical_p":
                (
                    quadratic_exceedances
                    + 1
                )
                / (
                    NULL_RUNS
                    + 1
                ),
        },
    }


# ================================================================
# GEOMETRIES
# ================================================================

GEOMETRIES = {
    "euclidean_rms":
        (
            euclidean,
            component_series,
        ),

    "relative_rms":
        (
            relative,
            component_series,
        ),

    "standardized_euclidean_rms":
        (
            euclidean,
            standardized_series,
        ),
}


# ================================================================
# COMPONENT CLASSIFICATION
# ================================================================

ATTENTION_COMPONENTS = [
    c for c in COMPONENTS
    if c.startswith("attn_")
]

FFN_COMPONENTS = [
    c for c in COMPONENTS
    if c.startswith("ffn_")
]

WEIGHT_COMPONENTS = [
    c for c in COMPONENTS
    if c.endswith(".weight")
]

BIAS_COMPONENTS = [
    c for c in COMPONENTS
    if c.endswith(".bias")
]


def group_of(component):

    if component in ATTENTION_COMPONENTS:
        family = "attention"
    elif component in FFN_COMPONENTS:
        family = "ffn"
    else:
        family = "other"

    if component in BIAS_COMPONENTS:
        parameter_type = "bias"
    else:
        parameter_type = "weight"

    return {
        "family": family,
        "parameter_type":
            parameter_type,
    }


# ================================================================
# RUN
# ================================================================

print("=" * 80)
print(" OPENMIND / V43 COMPONENT LOCALIZATION")
print("=" * 80)
print()

print(
    f"Layers:       {len(layer_ids)}"
)

print(
    f"Components:   {len(COMPONENTS)}"
)

print(
    f"Breakpoint:   {BREAKPOINT}"
)

print(
    f"Lag range:    {LAG_MIN}..{LAG_MAX}"
)

print(
    f"Null runs:    {NULL_RUNS}"
)

print(
    f"Seed:         {SEED}"
)

print()

results = {}


for geometry, (
    distance_function,
    series_map,
) in GEOMETRIES.items():

    print(
        f"Running geometry: {geometry}"
    )

    results[geometry] = {}

    for component in COMPONENTS:

        print(
            f"  {component}"
        )

        values = series_map[
            component
        ]

        order = list(
            range(len(values))
        )

        observed = observed_test(
            values,
            distance_function,
            order,
        )

        null = permutation_test(
            values,
            distance_function,
            observed,
        )

        results[geometry][
            component
        ] = {
            "component":
                component,

            **group_of(component),

            "breakpoint":
                BREAKPOINT,

            "primary_delta_bic":
                observed[
                    "linear_delta_bic"
                ],

            "quadratic_delta_bic":
                observed[
                    "quadratic_delta_bic"
                ],

            "slope_before":
                observed[
                    "slope_before"
                ],

            "slope_after":
                observed[
                    "slope_after"
                ],

            "slope_change":
                observed[
                    "slope_change"
                ],

            "primary_null":
                null["primary"],

            "quadratic_null":
                null["quadratic"],
        }


# ================================================================
# CROSS-GEOMETRY COMPONENT SUMMARY
# ================================================================

component_summary = {}

for component in COMPONENTS:

    geometry_results = {}

    for geometry in results:

        geometry_results[
            geometry
        ] = {
            "primary_delta_bic":
                results[
                    geometry
                ][component][
                    "primary_delta_bic"
                ],

            "primary_p":
                results[
                    geometry
                ][component][
                    "primary_null"
                ]["empirical_p"],

            "quadratic_delta_bic":
                results[
                    geometry
                ][component][
                    "quadratic_delta_bic"
                ],

            "quadratic_p":
                results[
                    geometry
                ][component][
                    "quadratic_null"
                ]["empirical_p"],

            "slope_change":
                results[
                    geometry
                ][component][
                    "slope_change"
                ],
        }

    component_summary[
        component
    ] = geometry_results


# ================================================================
# REFERENCE-STYLE RANKING
# ================================================================

ranking = {}

for geometry in GEOMETRIES:

    ordered = sorted(
        results[geometry].values(),
        key=lambda x:
            x["primary_delta_bic"],
        reverse=True,
    )

    ranking[geometry] = [
        {
            "component":
                x["component"],
            "family":
                x["family"],
            "parameter_type":
                x["parameter_type"],
            "primary_delta_bic":
                x["primary_delta_bic"],
            "primary_p":
                x["primary_null"][
                    "empirical_p"
                ],
            "quadratic_delta_bic":
                x["quadratic_delta_bic"],
            "quadratic_p":
                x["quadratic_null"][
                    "empirical_p"
                ],
            "slope_change":
                x["slope_change"],
        }
        for x in ordered
    ]


# ================================================================
# FAMILY AGGREGATION
# ================================================================

families = {
    "attention": ATTENTION_COMPONENTS,
    "ffn": FFN_COMPONENTS,
    "weights": WEIGHT_COMPONENTS,
    "biases": BIAS_COMPONENTS,
}

family_summary = {}

for geometry in GEOMETRIES:

    family_summary[
        geometry
    ] = {}

    for family_name, members in families.items():

        member_results = [
            results[
                geometry
            ][component]
            for component in members
        ]

        family_summary[
            geometry
        ][family_name] = {
            "component_count":
                len(member_results),

            "mean_primary_delta_bic":
                mean([
                    x[
                        "primary_delta_bic"
                    ]
                    for x in member_results
                ]),

            "median_primary_delta_bic":
                percentile(
                    [
                        x[
                            "primary_delta_bic"
                        ]
                        for x in member_results
                    ],
                    0.50,
                ),

            "mean_primary_p":
                mean([
                    x[
                        "primary_null"
                    ]["empirical_p"]
                    for x in member_results
                ]),

            "mean_quadratic_delta_bic":
                mean([
                    x[
                        "quadratic_delta_bic"
                    ]
                    for x in member_results
                ]),

            "significant_primary_p_lt_0_05":
                sum(
                    x[
                        "primary_null"
                    ]["empirical_p"]
                    < 0.05
                    for x in member_results
                ),

            "significant_quadratic_p_lt_0_05":
                sum(
                    x[
                        "quadratic_null"
                    ]["empirical_p"]
                    < 0.05
                    for x in member_results
                ),
        }


# ================================================================
# RESULT
# ================================================================

result = {
    "schema":
        "openmind.geometry_scaling_component_localization_test.v43",

    "source":
        str(INPUT),

    "layer_count":
        len(layer_ids),

    "component_dimension":
        len(COMPONENTS),

    "breakpoint":
        BREAKPOINT,

    "lag_range": {
        "min": LAG_MIN,
        "max": LAG_MAX,
    },

    "null_runs":
        NULL_RUNS,

    "seed":
        SEED,

    "paired_permutation_null":
        True,

    "cosine_component_level":
        "not applicable: scalar RMS cosine distance is degenerate",

    "geometries":
        results,

    "component_summary":
        component_summary,

    "ranking":
        ranking,

    "family_summary":
        family_summary,
}


OUTPUT.write_text(
    json.dumps(
        result,
        indent=2,
    )
)

print()
print("=" * 80)
print(" V43 COMPLETE")
print("=" * 80)
print()
print(
    f"Output: {OUTPUT}"
)
