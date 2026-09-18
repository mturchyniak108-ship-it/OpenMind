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

print("============================================================")
print(" OPENMIND / RECURSIVE TRANSITION TEST")
print("============================================================")
print("training prompts:", len(train))
print("test prompt:     ", len(datasets))
print()

# Fit one transition matrix for each adjacent layer.
models = {}

for a, b in zip(layers, layers[1:]):
    X = np.stack([d[a] for d in train])
    Y = np.stack([d[b] for d in train])

    X1 = np.column_stack([
        X,
        np.ones(len(X))
    ])

    W, *_ = np.linalg.lstsq(
        X1,
        Y,
        rcond=1e-6,
    )

    models[(a, b)] = W

# Start from REAL L21.
current = test[layers[0]]

print("start: REAL L%02d" % layers[0])
print()
print("transition   recursive_cos   recursive_err   direct_cos")
print("----------------------------------------------------------")

for a, b in zip(layers, layers[1:]):
    W = models[(a, b)]

    current1 = np.append(current, 1.0)
    predicted = current1 @ W

    actual = test[b]

    recursive_cos = np.dot(predicted, actual) / (
        np.linalg.norm(predicted) *
        np.linalg.norm(actual)
    )

    recursive_err = (
        np.linalg.norm(predicted - actual) /
        np.linalg.norm(actual)
    )

    direct_cos = np.dot(test[a], actual) / (
        np.linalg.norm(test[a]) *
        np.linalg.norm(actual)
    )

    print(
        f"L{a:02d}->L{b:02d}   "
        f"{recursive_cos:.9f}      "
        f"{recursive_err:.9f}     "
        f"{direct_cos:.9f}"
    )

    # CRITICAL:
    # feed prediction into the next transition.
    current = predicted

print()
print("Final recursive comparison:")
actual_final = test[layers[-1]]

final_cos = np.dot(current, actual_final) / (
    np.linalg.norm(current) *
    np.linalg.norm(actual_final)
)

final_err = (
    np.linalg.norm(current - actual_final) /
    np.linalg.norm(actual_final)
)

print(f"L{layers[-1]:02d} cosine = {final_cos:.9f}")
print(f"L{layers[-1]:02d} error  = {final_err:.9f}")
