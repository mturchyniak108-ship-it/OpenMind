import json
import math
import random
from pathlib import Path

INPUT = Path(
    "experiments/model_fractal/q8_parameter_field_v4_1.json"
)

OUTPUT = Path(
    "experiments/model_fractal/geometry_scaling_model_audit_v33.json"
)

NULL_RUNS = 10000
SEED = 28033
EPS = 1e-15

random.seed(SEED)

data = json.loads(INPUT.read_text())

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

layers_data = data["layers"]

layer_ids = sorted(
    layers_data,
    key=lambda x: int(x),
)

layers = len(layer_ids)

vectors = []

for layer_id in layer_ids:
    layer = layers_data[str(layer_id)]
    vector = []

    for component in components:
        item = layer.get(component)

        if item is None:
            raise ValueError(
                f"Missing component {component} "
                f"in layer {layer_id}"
            )

        value = item.get("stats", {}).get("rms")

        if value is None:
            raise ValueError(
                f"Missing RMS for {component} "
                f"in layer {layer_id}"
            )

        vector.append(float(value))

    vectors.append(vector)


def distance(a, b):
    return math.sqrt(
        sum(
            (x - y) ** 2
            for x, y in zip(a, b)
        )
    )


def mean(values):
    return sum(values) / len(values)


def fit_linear(xs, ys):
    mx = mean(xs)
    my = mean(ys)

    denom = sum(
        (x - mx) ** 2
        for x in xs
    )

    if denom <= EPS:
        return [my, 0.0]

    slope = sum(
        (x - mx) * (y - my)
        for x, y in zip(xs, ys)
    ) / denom

    intercept = my - slope * mx

    return [intercept, slope]


def solve3(matrix, vector):
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

        a[i], a[pivot] = a[pivot], a[i]

        pivot_value = a[i][i]

        for j in range(i, n + 1):
            a[i][j] /= pivot_value

        for r in range(n):

            if r == i:
                continue

            factor = a[r][i]

            for j in range(i, n + 1):
                a[r][j] -= factor * a[i][j]

    return [a[i][n] for i in range(n)]


def fit_quadratic(xs, ys):
    s0 = len(xs)
    s1 = sum(xs)
    s2 = sum(x * x for x in xs)
    s3 = sum(x * x * x for x in xs)
    s4 = sum(x * x * x * x for x in xs)

    t0 = sum(ys)
    t1 = sum(
        x * y
        for x, y in zip(xs, ys)
    )
    t2 = sum(
        x * x * y
        for x, y in zip(xs, ys)
    )

    matrix = [
        [s0, s1, s2],
        [s1, s2, s3],
        [s2, s3, s4],
    ]

    return solve3(
        matrix,
        [t0, t1, t2],
    )


def predictions(model, params, xs):
    if model == "linear":
        a, b = params
        return [
            a + b * x
            for x in xs
        ]

    if model == "quadratic":
        a, b, c = params
        return [
            a + b * x + c * x * x
            for x in xs
        ]

    if model == "power":
        a, alpha = params
        return [
            math.exp(a) * (x ** alpha)
            for x in xs
        ]

    raise ValueError(model)


def fit_model(model, xs, ys):

    if model == "linear":

        params = fit_linear(
            xs,
            ys,
        )

        fitted = predictions(
            model,
            params,
            xs,
        )

        parameter_count = 2

    elif model == "quadratic":

        params = fit_quadratic(
            xs,
            ys,
        )

        fitted = predictions(
            model,
            params,
            xs,
        )

        parameter_count = 3

    elif model == "power":

        log_x = [
            math.log(x)
            for x in xs
        ]

        log_y = [
            math.log(y)
            for y in ys
        ]

        log_params = fit_linear(
            log_x,
            log_y,
        )

        params = log_params

        fitted = predictions(
            model,
            params,
            xs,
        )

        parameter_count = 2

    else:
        raise ValueError(model)

    residuals = [
        y - f
        for y, f in zip(ys, fitted)
    ]

    sse = sum(
        r * r
        for r in residuals
    )

    mse = sse / len(xs)

    rmse = math.sqrt(mse)

    y_mean = mean(ys)

    sst = sum(
        (y - y_mean) ** 2
        for y in ys
    )

    r2 = (
        1.0 - sse / sst
        if sst > EPS
        else 0.0
    )

    n = len(xs)

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
        "parameters": params,
        "sse": sse,
        "rmse": rmse,
        "r2": r2,
        "aic": aic,
        "bic": bic,
        "residuals": residuals,
    }


def lag_curve(order):
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
        for lag in range(1, len(order))
    ]


MODELS = [
    "linear",
    "quadratic",
    "power",
]

WINDOWS = {
    "1_8": (1, 8),
    "1_12": (1, 12),
    "2_16": (2, 16),
    "4_20": (4, 20),
    "1_20": (1, 20),
    "1_23": (1, 23),
    "1_27": (1, 27),
}


def fit_windows(order):

    curve = lag_curve(order)

    output = {}

    for name, (lo, hi) in WINDOWS.items():

        points = [
            (x, y)
            for x, y in curve
            if lo <= x <= hi
        ]

        xs = [x for x, _ in points]
        ys = [y for _, y in points]

        output[name] = {}

        for model in MODELS:
            output[name][model] = fit_model(
                model,
                xs,
                ys,
            )

    return output


real_order = list(range(layers))

real_fits = fit_windows(real_order)


# ------------------------------------------------------------
# Null model comparison
#
# For each permutation we record:
#   power-vs-linear AIC difference
#   power-vs-quadratic AIC difference
#
# Positive value means power law has LOWER AIC and therefore
# better fit.
# ------------------------------------------------------------

null_statistics = {
    window: {
        "power_minus_linear_aic": [],
        "power_minus_quadratic_aic": [],
        "power_minus_linear_bic": [],
        "power_minus_quadratic_bic": [],
    }
    for window in WINDOWS
}


for run in range(NULL_RUNS):

    order = list(range(layers))
    random.shuffle(order)

    fits = fit_windows(order)

    for window in WINDOWS:

        power = fits[window]["power"]
        linear = fits[window]["linear"]
        quadratic = fits[window]["quadratic"]

        null_statistics[window][
            "power_minus_linear_aic"
        ].append(
            linear["aic"] - power["aic"]
        )

        null_statistics[window][
            "power_minus_quadratic_aic"
        ].append(
            quadratic["aic"] - power["aic"]
        )

        null_statistics[window][
            "power_minus_linear_bic"
        ].append(
            linear["bic"] - power["bic"]
        )

        null_statistics[window][
            "power_minus_quadratic_bic"
        ].append(
            quadratic["bic"] - power["bic"]
        )


def summarize_null(values, real_value):

    m = mean(values)

    sd = math.sqrt(
        sum(
            (x - m) ** 2
            for x in values
        ) / len(values)
    )

    p = (
        sum(
            x >= real_value
            for x in values
        ) + 1
    ) / (len(values) + 1)

    z = (
        (real_value - m)
        / max(sd, EPS)
    )

    return {
        "null_mean": m,
        "null_sd": sd,
        "real": real_value,
        "z": z,
        "empirical_p": p,
    }


statistics = {}

for window in WINDOWS:

    statistics[window] = {}

    for metric, values in (
        null_statistics[window].items()
    ):

        if metric == "power_minus_linear_aic":
            real_value = (
                real_fits[window]["linear"]["aic"]
                - real_fits[window]["power"]["aic"]
            )

        elif metric == "power_minus_quadratic_aic":
            real_value = (
                real_fits[window]["quadratic"]["aic"]
                - real_fits[window]["power"]["aic"]
            )

        elif metric == "power_minus_linear_bic":
            real_value = (
                real_fits[window]["linear"]["bic"]
                - real_fits[window]["power"]["bic"]
            )

        else:
            real_value = (
                real_fits[window]["quadratic"]["bic"]
                - real_fits[window]["power"]["bic"]
            )

        statistics[window][metric] = summarize_null(
            values,
            real_value,
        )


result = {
    "schema":
        "openmind.geometry_scaling_model_audit.v33",

    "source":
        str(INPUT),

    "layer_count":
        layers,

    "null_runs":
        NULL_RUNS,

    "seed":
        SEED,

    "models":
        MODELS,

    "windows":
        {
            name: {
                "min_lag": lo,
                "max_lag": hi,
            }
            for name, (lo, hi)
            in WINDOWS.items()
        },

    "real_fits":
        real_fits,

    "statistics":
        statistics,
}


OUTPUT.write_text(
    json.dumps(
        result,
        indent=2,
    )
)


print("=" * 72)
print(" OPENMIND / GEOMETRY SCALING MODEL AUDIT V33")
print("=" * 72)
print()
print("Layers:", layers)
print("Dimensions:", len(components))
print("Permutation runs:", NULL_RUNS)
print()

for window in WINDOWS:

    print("WINDOW:", window)

    for model in MODELS:

        fit = real_fits[window][model]

        print(
            f"  {model:10s}"
            f" R2={fit['r2']:.6f}"
            f" RMSE={fit['rmse']:.6f}"
            f" AIC={fit['aic']:.6f}"
            f" BIC={fit['bic']:.6f}"
        )

    print()

print("POWER-LAW PARAMETERS")

for window in WINDOWS:

    params = (
        real_fits[window]["power"]["parameters"]
    )

    log_a, alpha = params

    print(
        f"  {window:8s}"
        f" alpha={alpha:.6f}"
        f" A={math.exp(log_a):.6f}"
    )

print()
print("MODEL COMPARISON")
print()

for window in WINDOWS:

    print("WINDOW:", window)

    for metric in [
        "power_minus_linear_aic",
        "power_minus_quadratic_aic",
        "power_minus_linear_bic",
        "power_minus_quadratic_bic",
    ]:

        s = statistics[window][metric]

        print(
            f"  {metric}:"
            f" real={s['real']:.6f}"
            f" null_mean={s['null_mean']:.6f}"
            f" z={s['z']:.6f}"
            f" p={s['empirical_p']:.6f}"
        )

    print()

print("OUTPUT:", OUTPUT)
print("=" * 72)
