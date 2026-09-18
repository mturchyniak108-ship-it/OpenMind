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

# Hold out the final prompt.
train = datasets[:-1]
test = datasets[-1]

layers = sorted(test)

print("training prompts:", len(train))
print("test prompts:    ", 1)
print()

for a, b in zip(layers, layers[1:]):

    X = np.stack([
        d[a]
        for d in train
        if a in d and b in d
    ])

    Y = np.stack([
        d[b]
        for d in train
        if a in d and b in d
    ])

    # Add bias dimension.
    X1 = np.column_stack([
        X,
        np.ones(len(X))
    ])

    # Least-squares transition.
    W, *_ = np.linalg.lstsq(
        X1,
        Y,
        rcond=1e-6,
    )

    xt = test[a]
    yt = test[b]

    xt1 = np.append(xt, 1.0)

    pred = xt1 @ W

    cosine = np.dot(pred, yt) / (
        np.linalg.norm(pred) *
        np.linalg.norm(yt)
    )

    relative_error = (
        np.linalg.norm(pred - yt) /
        np.linalg.norm(yt)
    )

    baseline_cosine = np.dot(xt, yt) / (
        np.linalg.norm(xt) *
        np.linalg.norm(yt)
    )

    identity_error = (
        np.linalg.norm(xt - yt) /
        np.linalg.norm(yt)
    )

    print(
        f"L{a:02d}->L{b:02d} "
        f"identity_cos={baseline_cosine:.6f} "
        f"pred_cos={cosine:.6f} "
        f"pred_err={relative_error:.6f} "
        f"id_err={identity_error:.6f}"
    )
