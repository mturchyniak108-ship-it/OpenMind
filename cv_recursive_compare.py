import glob
import csv
import numpy as np

FILES = sorted(glob.glob("activation_dataset/prompt_*.csv"))
D = 1536

def load(path):
    with open(path) as f:
        rows = list(csv.DictReader(f))

    out = {}

    for r in rows:
        layer = int(r["layer"])
        out[layer] = np.array(
            [float(r[f"v{i}"]) for i in range(D)],
            dtype=np.float64,
        )

    return out


datasets = [load(p) for p in FILES]
layers = sorted(datasets[0])

source = layers[0]
final = layers[-1]

results = {
    "direct": [],
    "recursive": [],
    "residual": [],
}

for test_i in range(len(datasets)):

    train = [
        d for i, d in enumerate(datasets)
        if i != test_i
    ]

    test = datasets[test_i]

    # ---------------------------------------------------------
    # DIRECT L21 -> L27
    # ---------------------------------------------------------

    X = np.stack([d[source] for d in train])
    Y = np.stack([d[final] for d in train])

    X1 = np.column_stack([
        X,
        np.ones(len(X)),
    ])

    W, *_ = np.linalg.lstsq(
        X1,
        Y,
        rcond=1e-6,
    )

    pred = np.append(
        test[source],
        1.0,
    ) @ W

    actual = test[final]

    direct_cos = np.dot(pred, actual) / (
        np.linalg.norm(pred) *
        np.linalg.norm(actual)
    )

    # ---------------------------------------------------------
    # RECURSIVE
    # ---------------------------------------------------------

    models = {}

    for a, b in zip(layers, layers[1:]):

        X = np.stack([d[a] for d in train])
        Y = np.stack([d[b] for d in train])

        X1 = np.column_stack([
            X,
            np.ones(len(X)),
        ])

        W, *_ = np.linalg.lstsq(
            X1,
            Y,
            rcond=1e-6,
        )

        models[(a, b)] = W

    current = test[source]

    for a, b in zip(layers, layers[1:]):

        W = models[(a, b)]

        current = np.append(
            current,
            1.0,
        ) @ W

    recursive_cos = np.dot(
        current,
        actual,
    ) / (
        np.linalg.norm(current) *
        np.linalg.norm(actual)
    )

    # ---------------------------------------------------------
    # RESIDUAL RECURSIVE
    # ---------------------------------------------------------

    residual_models = {}

    for a, b in zip(layers, layers[1:]):

        X = np.stack([d[a] for d in train])

        Y = np.stack([
            d[b] - d[a]
            for d in train
        ])

        X1 = np.column_stack([
            X,
            np.ones(len(X)),
        ])

        W, *_ = np.linalg.lstsq(
            X1,
            Y,
            rcond=1e-6,
        )

        residual_models[(a, b)] = W

    current = test[source]

    for a, b in zip(layers, layers[1:]):

        W = residual_models[(a, b)]

        delta = np.append(
            current,
            1.0,
        ) @ W

        current = current + delta

    residual_cos = np.dot(
        current,
        actual,
    ) / (
        np.linalg.norm(current) *
        np.linalg.norm(actual)
    )

    results["direct"].append(direct_cos)
    results["recursive"].append(recursive_cos)
    results["residual"].append(residual_cos)


print("============================================================")
print(" OPENMIND / 20-FOLD TRANSITION ARCHITECTURE COMPARISON")
print("============================================================")
print()
print("Architecture        mean       std       min       max")
print("--------------------------------------------------------")

for name in [
    "direct",
    "recursive",
    "residual",
]:

    x = np.array(results[name])

    print(
        f"{name:18s} "
        f"{x.mean():.6f}   "
        f"{x.std():.6f}   "
        f"{x.min():.6f}   "
        f"{x.max():.6f}"
    )

print()
print("Complete.")
