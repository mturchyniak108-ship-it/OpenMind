import json
import random
import math
from pathlib import Path


NULL_RUNS = 2500
SEED = 34038
MIN_SEGMENT_SIZES = [4, 6, 8, 10]

INPUT = Path(
    "experiments/model_fractal/q8_parameter_field_v4_1.json"
)

OUTPUT = Path(
    "experiments/model_fractal/geometry_scaling_model_audit_v39.json"
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


def lag_curve():
    result = []

    for lag in range(1, len(vectors)):
        value = mean([
            distance(
                vectors[i],
                vectors[i + lag],
            )
            for i in range(
                len(vectors) - lag
            )
        ])

        result.append((lag, value))

    return result


curve = lag_curve()


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


def polynomial_fit(xs, ys, degree):
    powers = [
        [x ** p for p in range(degree + 1)]
        for x in xs
    ]

    matrix = []

    vector = []

    for i in range(degree + 1):
        matrix.append([
            sum(
                row[i] * row[j]
                for row in powers
            )
            for j in range(degree + 1)
        ])

        vector.append(
            sum(
                row[i] * y
                for row, y in zip(
                    powers,
                    ys,
                )
            )
        )

    params = solve_linear_system(
        matrix,
        vector,
    )

    predictions = [
        sum(
            params[p] * (x ** p)
            for p in range(degree + 1)
        )
        for x in xs
    ]

    return params, predictions


def power_fit(xs, ys):
    def evaluate(alpha):
        powers = [
            x ** alpha
            for x in xs
        ]

        denom = sum(
            p * p
            for p in powers
        )

        if denom <= EPS:
            return float("inf"), 0.0

        A = sum(
            y * p
            for y, p in zip(
                ys,
                powers,
            )
        ) / denom

        sse = sum(
            (y - A * p) ** 2
            for y, p in zip(
                ys,
                powers,
            )
        )

        return sse, A

    lo = -5.0
    hi = 30.0

    phi = (
        1.0 + math.sqrt(5.0)
    ) / 2.0

    inv_phi = 1.0 / phi

    c = hi - (
        hi - lo
    ) * inv_phi

    d = lo + (
        hi - lo
    ) * inv_phi

    fc, _ = evaluate(c)
    fd, _ = evaluate(d)

    for _ in range(240):
        if fc < fd:
            hi = d
            d = c
            fd = fc

            c = hi - (
                hi - lo
            ) * inv_phi

            fc, _ = evaluate(c)

        else:
            lo = c
            c = d
            fc = fd

            d = lo + (
                hi - lo
            ) * inv_phi

            fd, _ = evaluate(d)

    alpha = (
        lo + hi
    ) / 2.0

    sse, A = evaluate(alpha)

    predictions = [
        A * (x ** alpha)
        for x in xs
    ]

    return [
        math.log(A),
        alpha,
    ], predictions


def exponential_fit(xs, ys):
    """
    y = A * exp(beta*x)

    Fit in log-space, then evaluate SSE
    in the original distance space.
    """

    log_y = [
        math.log(y)
        for y in ys
    ]

    params = polynomial_fit(
        xs,
        log_y,
        1,
    )[0]

    log_A, beta = params

    A = math.exp(log_A)

    predictions = [
        A * math.exp(
            beta * x
        )
        for x in xs
    ]

    return [
        log_A,
        beta,
    ], predictions


def fit_global_models():
    xs = [
        x
        for x, _ in curve
        if WINDOW[0] <= x <= WINDOW[1]
    ]

    ys = [
        y
        for x, y in curve
        if WINDOW[0] <= x <= WINDOW[1]
    ]

    results = {}

    params, pred = polynomial_fit(
        xs,
        ys,
        1,
    )

    results["linear"] = {
        "parameters": params,
        **regression_metrics(
            ys,
            pred,
            2,
        ),
    }

    params, pred = polynomial_fit(
        xs,
        ys,
        2,
    )

    results["quadratic"] = {
        "parameters": params,
        **regression_metrics(
            ys,
            pred,
            3,
        ),
    }

    params, pred = power_fit(
        xs,
        ys,
    )

    results["power"] = {
        "parameters": params,
        "A": math.exp(params[0]),
        **regression_metrics(
            ys,
            pred,
            2,
        ),
    }

    params, pred = exponential_fit(
        xs,
        ys,
    )

    results["exponential"] = {
        "parameters": params,
        "A": math.exp(params[0]),
        **regression_metrics(
            ys,
            pred,
            2,
        ),
    }

    return results


def fit_piecewise(
    breakpoint,
    model,
    min_segment_size=4,
):
    """
    Piecewise models use separate fits on:

        [1, breakpoint]
        [breakpoint+1, 27]

    The two segments are intentionally
    independent in V37.

    Parameter counts:

        linear      4
        quadratic   6
        power       4
        exponential 4
    """

    left = [
        (x, y)
        for x, y in curve
        if x <= breakpoint
    ]

    right = [
        (x, y)
        for x, y in curve
        if x > breakpoint
    ]

    if (
        len(left) < min_segment_size
        or len(right) < min_segment_size
    ):
        return None

    xs1 = [x for x, _ in left]
    ys1 = [y for _, y in left]

    xs2 = [x for x, _ in right]
    ys2 = [y for _, y in right]

    if model == "linear":
        p1, pred1 = polynomial_fit(
            xs1,
            ys1,
            1,
        )

        p2, pred2 = polynomial_fit(
            xs2,
            ys2,
            1,
        )

        parameter_count = 4

    elif model == "quadratic":
        p1, pred1 = polynomial_fit(
            xs1,
            ys1,
            2,
        )

        p2, pred2 = polynomial_fit(
            xs2,
            ys2,
            2,
        )

        parameter_count = 6

    elif model == "power":
        p1, pred1 = power_fit(
            xs1,
            ys1,
        )

        p2, pred2 = power_fit(
            xs2,
            ys2,
        )

        parameter_count = 4

    elif model == "exponential":
        p1, pred1 = exponential_fit(
            xs1,
            ys1,
        )

        p2, pred2 = exponential_fit(
            xs2,
            ys2,
        )

        parameter_count = 4

    else:
        raise ValueError(model)

    ys = ys1 + ys2
    predictions = pred1 + pred2

    metrics = regression_metrics(
        ys,
        predictions,
        parameter_count,
    )

    return {
        "breakpoint": breakpoint,
        "left_parameters": p1,
        "right_parameters": p2,
        **metrics,
    }


def evaluate_order(
    order,
    min_segment_size=4,
):
    """
    Evaluate one layer ordering using exactly the V37 model-selection
    procedure.

    The lag curve is rebuilt from the supplied ordering, then:
      1. all global models are fit;
      2. every legal breakpoint 8..23 is searched;
      3. the best piecewise fit for each model is selected;
      4. the best global model by BIC is selected.
    """

    global curve

    curve = [
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
        for lag in range(1, len(order))
    ]

    global_models = fit_global_models()

    piecewise_models = {}

    for model in [
        "linear",
        "quadratic",
        "power",
        "exponential",
    ]:

        piecewise_models[model] = {}

        for breakpoint in range(8, 24):
            fit = fit_piecewise(
                breakpoint,
                model,
                min_segment_size=min_segment_size,
            )

            if fit is not None:
                piecewise_models[model][
                    str(breakpoint)
                ] = fit

    best_piecewise = {}

    for model, fits in piecewise_models.items():
        best_piecewise[model] = min(
            fits.values(),
            key=lambda x: x["bic"],
        )

    best_global = min(
        global_models.items(),
        key=lambda kv: kv[1]["bic"],
    )

    best_piecewise_global = min(
        best_piecewise.items(),
        key=lambda kv: kv[1]["bic"],
    )

    delta_bic = (
        best_global[1]["bic"]
        - best_piecewise_global[1]["bic"]
    )

    return {
        "global_models": global_models,
        "piecewise_models": piecewise_models,
        "best_global": best_global,
        "best_piecewise": best_piecewise,
        "best_piecewise_global": best_piecewise_global,
        "delta_bic": delta_bic,
    }


# ------------------------------------------------------------------
# V39 ROBUSTNESS AUDIT
#
# The SAME permutation sequence is evaluated at every minimum
# segment size. This makes the robustness comparison paired rather
# than introducing different random null samples.
# ------------------------------------------------------------------

def summarize(values, real_value):
    ordered = sorted(values)
    n = len(ordered)

    m = mean(ordered)

    variance = (
        sum(
            (x - m) ** 2
            for x in ordered
        )
        / n
    )

    sd = math.sqrt(variance)

    def percentile(q):
        if n == 1:
            return ordered[0]

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

    exceedances = sum(
        x >= real_value
        for x in ordered
    )

    empirical_p = (
        exceedances + 1
    ) / (
        n + 1
    )

    return {
        "n": n,
        "mean": m,
        "sd": sd,
        "min": ordered[0],
        "p01": percentile(0.01),
        "p05": percentile(0.05),
        "p50": percentile(0.50),
        "p95": percentile(0.95),
        "p99": percentile(0.99),
        "max": ordered[-1],
        "real": real_value,
        "exceedances": exceedances,
        "empirical_p": empirical_p,
    }


# ------------------------------------------------------------------
# REAL DATA
# ------------------------------------------------------------------

real_order = list(range(len(vectors)))

real_by_segment_size = {}

for min_segment_size in MIN_SEGMENT_SIZES:

    real = evaluate_order(
        real_order,
        min_segment_size=min_segment_size,
    )

    real_best_global_model = (
        real["best_global"][0]
    )

    real_best_global = (
        real["best_global"][1]
    )

    real_best_piecewise_model = (
        real["best_piecewise_global"][0]
    )

    real_best_piecewise = (
        real["best_piecewise_global"][1]
    )

    real_by_segment_size[
        str(min_segment_size)
    ] = {
        "best_global": {
            "model":
                real_best_global_model,
            **real_best_global,
        },

        "best_piecewise": {
            "model":
                real_best_piecewise_model,
            **real_best_piecewise,
        },

        "delta_bic":
            real["delta_bic"],
    }


# ------------------------------------------------------------------
# PERMUTATION NULL
# ------------------------------------------------------------------

rng = random.Random(SEED)

null_by_segment_size = {}

for min_segment_size in MIN_SEGMENT_SIZES:

    null_delta_bic = []

    null_breakpoints = {
        str(breakpoint): 0
        for breakpoint in range(8, 24)
    }

    null_global_models = {
        model: 0
        for model in [
            "linear",
            "quadratic",
            "power",
            "exponential",
        ]
    }

    null_piecewise_models = {
        model: 0
        for model in [
            "linear",
            "quadratic",
            "power",
            "exponential",
        ]
    }

    null_joint_selection = {}

    null_legal_breakpoints = []

    for breakpoint in range(8, 24):

        left_size = breakpoint
        right_size = len(vectors) - 1 - breakpoint

        if (
            left_size >= min_segment_size
            and right_size >= min_segment_size
        ):
            null_legal_breakpoints.append(
                breakpoint
            )

    # --------------------------------------------------------------
    # IMPORTANT:
    # Each segment-size audit receives its own deterministic stream
    # derived from the master seed. This makes runs reproducible while
    # keeping each robustness condition statistically independent.
    # --------------------------------------------------------------

    condition_rng = random.Random(
        SEED + min_segment_size
    )

    real_delta_bic = (
        real_by_segment_size[
            str(min_segment_size)
        ]["delta_bic"]
    )

    for run in range(NULL_RUNS):

        order = list(range(len(vectors)))

        condition_rng.shuffle(order)

        result_run = evaluate_order(
            order,
            min_segment_size=min_segment_size,
        )

        delta = result_run["delta_bic"]

        null_delta_bic.append(delta)

        global_model = (
            result_run["best_global"][0]
        )

        piecewise_model, piecewise_fit = (
            result_run[
                "best_piecewise_global"
            ]
        )

        breakpoint = str(
            piecewise_fit["breakpoint"]
        )

        null_global_models[
            global_model
        ] += 1

        null_piecewise_models[
            piecewise_model
        ] += 1

        null_breakpoints[
            breakpoint
        ] += 1

        joint_key = (
            f"{piecewise_model}:{breakpoint}"
        )

        null_joint_selection[
            joint_key
        ] = (
            null_joint_selection.get(
                joint_key,
                0,
            )
            + 1
        )

    null_by_segment_size[
        str(min_segment_size)
    ] = {
        "delta_bic":
            summarize(
                null_delta_bic,
                real_delta_bic,
            ),

        "global_model_counts":
            null_global_models,

        "piecewise_model_counts":
            null_piecewise_models,

        "breakpoint_counts":
            null_breakpoints,

        "joint_piecewise_selection_counts":
            null_joint_selection,

        "legal_breakpoints":
            null_legal_breakpoints,
    }


# ------------------------------------------------------------------
# ROBUSTNESS SUMMARY
# ------------------------------------------------------------------

robustness = {}

for min_segment_size in MIN_SEGMENT_SIZES:

    key = str(min_segment_size)

    real = real_by_segment_size[key]

    null = null_by_segment_size[key]

    robustness[key] = {
        "best_global_model":
            real["best_global"]["model"],

        "best_global_bic":
            real["best_global"]["bic"],

        "best_piecewise_model":
            real["best_piecewise"]["model"],

        "best_piecewise_breakpoint":
            real["best_piecewise"]["breakpoint"],

        "best_piecewise_bic":
            real["best_piecewise"]["bic"],

        "delta_bic":
            real["delta_bic"],

        "empirical_p":
            null["delta_bic"]["empirical_p"],

        "null_p95":
            null["delta_bic"]["p95"],

        "null_p99":
            null["delta_bic"]["p99"],

        "breakpoint_23_null_frequency":
            (
                null["breakpoint_counts"]["23"]
                / NULL_RUNS
            ),

        "breakpoint_23_legal":
            23 in null["legal_breakpoints"],
    }


result = {
    "schema":
        "openmind.geometry_scaling_model_audit.v39",

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

    "models":
        [
            "linear",
            "quadratic",
            "power",
            "exponential",
        ],

    "breakpoint_search":
        {
            "requested_min": 8,
            "requested_max": 23,
            "rule":
                "left x<=breakpoint; right x>breakpoint",
            "minimum_segment_sizes":
                MIN_SEGMENT_SIZES,
        },

    "null_runs_per_condition":
        NULL_RUNS,

    "seed":
        SEED,

    "selection_statistic":
        "best_global_bic_minus_best_piecewise_bic",

    "real_by_min_segment_size":
        real_by_segment_size,

    "null_by_min_segment_size":
        null_by_segment_size,

    "robustness":
        robustness,
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

print("=" * 100)
print(" OPENMIND / V39 BREAKPOINT ROBUSTNESS AUDIT")
print("=" * 100)
print()

print("CONFIGURATION")
print()

print(
    f"  permutation runs / condition="
    f"{NULL_RUNS}"
)

print(
    f"  minimum segment sizes="
    f"{MIN_SEGMENT_SIZES}"
)

print(
    f"  seed={SEED}"
)

print()

print("REAL DATA ROBUSTNESS")
print()

print(
    "  minseg  global       piecewise"
    "          bp     delta_BIC       p"
)

print(
    "  ------  -----------  "
    "-----------  -----  ------------  --------"
)

for min_segment_size in MIN_SEGMENT_SIZES:

    key = str(min_segment_size)

    r = robustness[key]

    print(
        f"  {min_segment_size:6d}"
        f"  {r['best_global_model']:11s}"
        f"  {r['best_piecewise_model']:11s}"
        f"  {r['best_piecewise_breakpoint']:5d}"
        f"  {r['delta_bic']:12.6f}"
        f"  {r['empirical_p']:.6f}"
    )

print()

print("NULL PERCENTILES")
print()

print(
    "  minseg       p95        p99        max"
)

for min_segment_size in MIN_SEGMENT_SIZES:

    key = str(min_segment_size)

    summary = (
        null_by_segment_size[key]
        ["delta_bic"]
    )

    print(
        f"  {min_segment_size:6d}"
        f"  {summary['p95']:10.6f}"
        f"  {summary['p99']:10.6f}"
        f"  {summary['max']:10.6f}"
    )

print()

print("BREAKPOINT 23 NULL FREQUENCY")
print()

for min_segment_size in MIN_SEGMENT_SIZES:

    key = str(min_segment_size)

    r = robustness[key]

    print(
        f"  minseg={min_segment_size:2d}"
        f"  legal={str(r['breakpoint_23_legal']):5s}"
        f"  frequency="
        f"{r['breakpoint_23_null_frequency']:.4%}"
    )

print()

print("OUTPUT:", OUTPUT)
print("=" * 100)
