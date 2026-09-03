import json
import math
import random
from pathlib import Path


# ================================================================
# OPENMIND / V44 COMPONENT LOCALIZATION TEST
# ================================================================
#
# V42 established that the strongest transition is consistently
# located at BP=21 across four distance geometries.
#
# V44 asks:
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

# V44 breakpoint-search range.
# BP=21 remains the fixed reference breakpoint.
SEARCH_BREAKPOINT_MIN = 12
SEARCH_BREAKPOINT_MAX = 21

LAG_MIN = 1
LAG_MAX = 27

INPUT = Path(
    "experiments/model_fractal/"
    "q8_parameter_field_v4_1.json"
)

OUTPUT = Path(
    "experiments/model_fractal/"
    "geometry_scaling_component_localization_test_v44.json"
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
    # V42 cosine operates on the complete 12-D vector. V44 uses
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


def fit_hinge(curve, breakpoint=None):

    xs = [x for x, _ in curve]
    ys = [y for _, y in curve]

    if breakpoint is None:
        breakpoint = BREAKPOINT

    k = float(breakpoint)

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


def fit_quadratic_hinge(curve, breakpoint=None):

    xs = [x for x, _ in curve]
    ys = [y for _, y in curve]

    if breakpoint is None:
        breakpoint = BREAKPOINT

    k = float(breakpoint)

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
    breakpoint=None,
):

    curve = build_curve(
        values,
        distance_function,
        order,
    )

    linear = fit_linear(curve)
    hinge = fit_hinge(
        curve,
        breakpoint,
    )

    quadratic = fit_quadratic(curve)
    quadratic_hinge = (
        fit_quadratic_hinge(
            curve,
            breakpoint,
        )
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
# BREAKPOINT SEARCH
# ================================================================

def breakpoint_candidates():
    return list(
        range(
            SEARCH_BREAKPOINT_MIN,
            SEARCH_BREAKPOINT_MAX + 1,
        )
    )


def breakpoint_search(
    values,
    distance_function,
    order,
):
    curve = build_curve(
        values,
        distance_function,
        order,
    )

    candidates = breakpoint_candidates()

    rows = []

    for breakpoint in candidates:
        linear = fit_linear(curve)

        hinge = fit_hinge(
            curve,
            breakpoint,
        )

        quadratic = fit_quadratic(curve)

        quadratic_hinge = (
            fit_quadratic_hinge(
                curve,
                breakpoint,
            )
        )

        primary_delta = (
            linear["bic"]
            - hinge["bic"]
        )

        quadratic_delta = (
            quadratic["bic"]
            - quadratic_hinge["bic"]
        )

        rows.append({
            "breakpoint": breakpoint,
            "primary_delta_bic":
                primary_delta,
            "quadratic_delta_bic":
                quadratic_delta,
            "slope_change":
                hinge["slope_change"],
            "slope_before":
                hinge["slope_before"],
            "slope_after":
                hinge["slope_after"],
        })

    best_primary = max(
        rows,
        key=lambda x:
            x["primary_delta_bic"],
    )

    best_quadratic = max(
        rows,
        key=lambda x:
            x["quadratic_delta_bic"],
    )

    fixed = observed_test(
        values,
        distance_function,
        order,
        BREAKPOINT,
    )

    return {
        "fixed":
            fixed,

        "candidates":
            rows,

        "best_primary":
            best_primary,

        "best_quadratic":
            best_quadratic,
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

    null_fixed_primary = []
    null_fixed_quadratic = []

    null_max_primary = []
    null_max_quadratic = []

    base_order = list(
        range(len(values))
    )

    for _ in range(NULL_RUNS):

        order = base_order[:]

        rng.shuffle(order)

        searched = breakpoint_search(
            values,
            distance_function,
            order,
        )

        fixed = searched["fixed"]

        null_fixed_primary.append(
            fixed["linear_delta_bic"]
        )

        null_fixed_quadratic.append(
            fixed["quadratic_delta_bic"]
        )

        null_max_primary.append(
            searched["best_primary"][
                "primary_delta_bic"
            ]
        )

        null_max_quadratic.append(
            searched["best_quadratic"][
                "quadratic_delta_bic"
            ]
        )

    real_fixed_primary = (
        observed["fixed"][
            "linear_delta_bic"
        ]
    )

    real_fixed_quadratic = (
        observed["fixed"][
            "quadratic_delta_bic"
        ]
    )

    real_max_primary = (
        observed["best_primary"][
            "primary_delta_bic"
        ]
    )

    real_max_quadratic = (
        observed["best_quadratic"][
            "quadratic_delta_bic"
        ]
    )

    fixed_primary_exceedances = sum(
        x >= real_fixed_primary
        for x in null_fixed_primary
    )

    fixed_quadratic_exceedances = sum(
        x >= real_fixed_quadratic
        for x in null_fixed_quadratic
    )

    max_primary_exceedances = sum(
        x >= real_max_primary
        for x in null_max_primary
    )

    max_quadratic_exceedances = sum(
        x >= real_max_quadratic
        for x in null_max_quadratic
    )

    return {
        "fixed": {
            "primary": {
                "n": NULL_RUNS,
                "mean":
                    mean(null_fixed_primary),
                "sd":
                    math.sqrt(
                        mean([
                            (
                                x
                                - mean(
                                    null_fixed_primary
                                )
                            ) ** 2
                            for x in null_fixed_primary
                        ])
                    ),
                "p95":
                    percentile(
                        null_fixed_primary,
                        0.95,
                    ),
                "p99":
                    percentile(
                        null_fixed_primary,
                        0.99,
                    ),
                "max":
                    max(null_fixed_primary),
                "exceedances":
                    fixed_primary_exceedances,
                "empirical_p":
                    (
                        fixed_primary_exceedances
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
                    mean(null_fixed_quadratic),
                "sd":
                    math.sqrt(
                        mean([
                            (
                                x
                                - mean(
                                    null_fixed_quadratic
                                )
                            ) ** 2
                            for x in null_fixed_quadratic
                        ])
                    ),
                "p95":
                    percentile(
                        null_fixed_quadratic,
                        0.95,
                    ),
                "p99":
                    percentile(
                        null_fixed_quadratic,
                        0.99,
                    ),
                "max":
                    max(null_fixed_quadratic),
                "exceedances":
                    fixed_quadratic_exceedances,
                "empirical_p":
                    (
                        fixed_quadratic_exceedances
                        + 1
                    )
                    / (
                        NULL_RUNS
                        + 1
                    ),
            },
        },

        "max_statistic": {
            "primary": {
                "n": NULL_RUNS,
                "mean":
                    mean(null_max_primary),
                "sd":
                    math.sqrt(
                        mean([
                            (
                                x
                                - mean(
                                    null_max_primary
                                )
                            ) ** 2
                            for x in null_max_primary
                        ])
                    ),
                "p95":
                    percentile(
                        null_max_primary,
                        0.95,
                    ),
                "p99":
                    percentile(
                        null_max_primary,
                        0.99,
                    ),
                "max":
                    max(null_max_primary),
                "exceedances":
                    max_primary_exceedances,
                "empirical_p":
                    (
                        max_primary_exceedances
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
                    mean(null_max_quadratic),
                "sd":
                    math.sqrt(
                        mean([
                            (
                                x
                                - mean(
                                    null_max_quadratic
                                )
                            ) ** 2
                            for x in null_max_quadratic
                        ])
                    ),
                "p95":
                    percentile(
                        null_max_quadratic,
                        0.95,
                    ),
                "p99":
                    percentile(
                        null_max_quadratic,
                        0.99,
                    ),
                "max":
                    max(null_max_quadratic),
                "exceedances":
                    max_quadratic_exceedances,
                "empirical_p":
                    (
                        max_quadratic_exceedances
                        + 1
                    )
                    / (
                        NULL_RUNS
                        + 1
                    ),
            },
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
print(" OPENMIND / V44 COMPONENT LOCALIZATION")
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

        observed = breakpoint_search(
            values,
            distance_function,
            order,
        )

        null = permutation_test(
            values,
            distance_function,
            observed,
        )

        fixed = observed["fixed"]

        results[geometry][
            component
        ] = {
            "component":
                component,

            **group_of(component),

            "breakpoint":
                BREAKPOINT,

            "search_breakpoint_min":
                SEARCH_BREAKPOINT_MIN,

            "search_breakpoint_max":
                SEARCH_BREAKPOINT_MAX,

            "primary_delta_bic":
                fixed[
                    "linear_delta_bic"
                ],

            "quadratic_delta_bic":
                fixed[
                    "quadratic_delta_bic"
                ],

            "slope_before":
                fixed[
                    "slope_before"
                ],

            "slope_after":
                fixed[
                    "slope_after"
                ],

            "slope_change":
                fixed[
                    "slope_change"
                ],

            "primary_null":
                null["fixed"]["primary"],

            "quadratic_null":
                null["fixed"]["quadratic"],

            "best_primary":
                observed[
                    "best_primary"
                ],

            "best_quadratic":
                observed[
                    "best_quadratic"
                ],

            "max_statistic_null":
                null[
                    "max_statistic"
                ],
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
            x["best_primary"][
                "primary_delta_bic"
            ],
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

            "fixed_breakpoint":
                x["breakpoint"],

            "fixed_primary_delta_bic":
                x["primary_delta_bic"],

            "fixed_primary_p":
                x["primary_null"][
                    "empirical_p"
                ],

            "best_primary_breakpoint":
                x["best_primary"][
                    "breakpoint"
                ],

            "best_primary_delta_bic":
                x["best_primary"][
                    "primary_delta_bic"
                ],

            "max_primary_p":
                x["max_statistic_null"][
                    "primary"
                ]["empirical_p"],

            "fixed_quadratic_delta_bic":
                x["quadratic_delta_bic"],

            "fixed_quadratic_p":
                x["quadratic_null"][
                    "empirical_p"
                ],

            "best_quadratic_breakpoint":
                x["best_quadratic"][
                    "breakpoint"
                ],

            "best_quadratic_delta_bic":
                x["best_quadratic"][
                    "quadratic_delta_bic"
                ],

            "max_quadratic_p":
                x["max_statistic_null"][
                    "quadratic"
                ]["empirical_p"],

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
        "openmind.geometry_scaling_component_localization_test.v44",

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
print(" V44 COMPLETE")
print("=" * 80)
print()
print(
    f"Output: {OUTPUT}"
)
