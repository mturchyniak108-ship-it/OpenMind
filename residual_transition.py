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

train = datasets[:-1]
test = datasets[-1]

layers = sorted(test)

models = {}

for a, b in zip(layers, layers[1:]):

    X = np.stack([d[a] for d in train])
    Y = np.stack([d[b] - d[a] for d in train])

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


current = test[layers[0]]

print("============================================================")
print(" OPENMIND / RECURSIVE RESIDUAL TRANSITION TEST")
print("============================================================")
print("training prompts:", len(train))
print("test prompt:     ", len(datasets))
print()
print("start: REAL L%02d" % layers[0])
print()

print("transition   residual_cos   residual_err")
print("------------------------------------------")


for a, b in zip(layers, layers[1:]):

    W = models[(a, b)]

    current1 = np.append(current, 1.0)

    delta = current1 @ W

    predicted = current + delta

    actual = test[b]

    cosine = np.dot(predicted, actual) / (
        np.linalg.norm(predicted) *
        np.linalg.norm(actual)
    )

    error = (
        np.linalg.norm(predicted - actual) /
        np.linalg.norm(actual)
    )

    print(
        f"L{a:02d}->L{b:02d}   "
        f"{cosine:.9f}      "
        f"{error:.9f}"
    )

    current = predicted


actual = test[layers[-1]]

final_cos = np.dot(current, actual) / (
    np.linalg.norm(current) *
    np.linalg.norm(actual)
)

final_error = (
    np.linalg.norm(current - actual) /
    np.linalg.norm(actual)
)

print()
print("Final recursive result:")
print(f"L{layers[-1]:02d} cosine = {final_cos:.9f}")
print(f"L{layers[-1]:02d} error  = {final_error:.9f}")
