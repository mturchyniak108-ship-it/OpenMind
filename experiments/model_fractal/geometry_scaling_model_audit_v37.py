import json
import math
from pathlib import Path

INPUT = Path(
    "experiments/model_fractal/q8_parameter_field_v4_1.json"
)

OUTPUT = Path(
    "experiments/model_fractal/geometry_scaling_model_audit_v37.json"
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

    if len(left) < 4 or len(right) < 4:
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


result = {
    "schema":
        "openmind.geometry_scaling_model_audit.v37",

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

    "global_models":
        global_models,

    "piecewise_models":
        piecewise_models,

    "best_global_model":
        {
            "model": best_global[0],
            **best_global[1],
        },

    "best_piecewise_models":
        best_piecewise,
}


OUTPUT.write_text(
    json.dumps(
        result,
        indent=2,
    )
)


print("=" * 100)
print(" OPENMIND / V37 BREAKPOINT MODEL AUDIT")
print("=" * 100)
print()

print("GLOBAL MODELS")
print()

for model, fit in global_models.items():

    params = fit["parameters"]

    if model == "power":
        detail = (
            f" A={fit['A']:.9g}"
            f" alpha={params[1]:.9f}"
        )

    elif model == "exponential":
        detail = (
            f" A={fit['A']:.9g}"
            f" beta={params[1]:.9f}"
        )

    else:
        detail = ""

    print(
        f"{model:12s}"
        f" R2={fit['r2']:.9f}"
        f" RMSE={fit['rmse']:.9f}"
        f" SSE={fit['sse']:.9f}"
        f" AIC={fit['aic']:.6f}"
        f" BIC={fit['bic']:.6f}"
        f"{detail}"
    )

print()
print("BEST PIECEWISE MODELS BY BIC")
print()

for model, fit in best_piecewise.items():

    print(
        f"{model:12s}"
        f" breakpoint={fit['breakpoint']:2d}"
        f" R2={fit['r2']:.9f}"
        f" RMSE={fit['rmse']:.9f}"
        f" SSE={fit['sse']:.9f}"
        f" AIC={fit['aic']:.6f}"
        f" BIC={fit['bic']:.6f}"
    )

print()
print("ALL PIECEWISE POWER BREAKPOINTS")
print()

for breakpoint, fit in (
    piecewise_models["power"].items()
):

    print(
        f"breakpoint={int(breakpoint):2d}"
        f" R2={fit['r2']:.9f}"
        f" SSE={fit['sse']:.9f}"
        f" AIC={fit['aic']:.6f}"
        f" BIC={fit['bic']:.6f}"
        f" "
        f"alpha_left={fit['left_parameters'][1]:.6f}"
        f" "
        f"alpha_right={fit['right_parameters'][1]:.6f}"
    )

print()
print("BEST GLOBAL BY BIC:")
print(
    best_global[0],
    f"BIC={best_global[1]['bic']:.6f}",
)

print()
print("OUTPUT:", OUTPUT)
print("=" * 100)
