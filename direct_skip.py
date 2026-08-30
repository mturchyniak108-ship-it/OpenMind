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

train = datasets[:-1]
test = datasets[-1]

layers = sorted(test)

source = layers[0]

print("============================================================")
print(" OPENMIND / DIRECT LAYER SKIP TEST")
print("============================================================")
print("training prompts:", len(train))
print("source layer:    L%02d" % source)
print()
print("target   cosine       error")
print("-----------------------------")


for target in layers[1:]:

    X = np.stack([
        d[source]
        for d in train
    ])

    Y = np.stack([
        d[target]
        for d in train
    ])

    X1 = np.column_stack([
        X,
        np.ones(len(X))
    ])

    W, *_ = np.linalg.lstsq(
        X1,
        Y,
        rcond=1e-6
    )

    pred = np.append(test[source], 1.0) @ W
    actual = test[target]

    cosine = np.dot(pred, actual) / (
        np.linalg.norm(pred) *
        np.linalg.norm(actual)
    )

    error = (
        np.linalg.norm(pred - actual) /
        np.linalg.norm(actual)
    )

    print(
        f"L{target:02d}     "
        f"{cosine:.9f}   "
        f"{error:.9f}"
    )
