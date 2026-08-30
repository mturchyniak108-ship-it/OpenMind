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
            dtype=np.float64
        )

    return out


datasets = [load(p) for p in FILES]
layers = sorted(datasets[0])
source = layers[0]

print("============================================================")
print(" OPENMIND / CROSS-VALIDATED DIRECT SKIP")
print("============================================================")
print("prompts:", len(datasets))
print("source: L%02d" % source)
print()

results = {target: [] for target in layers[1:]}

for test_i in range(len(datasets)):

    train = [
        d for i, d in enumerate(datasets)
        if i != test_i
    ]

    test = datasets[test_i]

    X = np.stack([d[source] for d in train])

    X1 = np.column_stack([
        X,
        np.ones(len(X))
    ])

    for target in layers[1:]:

        Y = np.stack([
            d[target] for d in train
        ])

        W, *_ = np.linalg.lstsq(
            X1,
            Y,
            rcond=1e-6
        )

        pred = np.append(
            test[source],
            1.0
        ) @ W

        actual = test[target]

        cosine = np.dot(pred, actual) / (
            np.linalg.norm(pred) *
            np.linalg.norm(actual)
        )

        error = (
            np.linalg.norm(pred - actual) /
            np.linalg.norm(actual)
        )

        results[target].append(
            (cosine, error)
        )


print("target   mean_cos    std_cos    min_cos    max_cos    mean_err")
print("----------------------------------------------------------------")

for target in layers[1:]:

    vals = np.array(results[target])

    cos = vals[:, 0]
    err = vals[:, 1]

    print(
        f"L{target:02d}     "
        f"{cos.mean():.6f}    "
        f"{cos.std():.6f}    "
        f"{cos.min():.6f}    "
        f"{cos.max():.6f}    "
        f"{err.mean():.6f}"
    )
