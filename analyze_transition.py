import csv
import glob
import numpy as np

FILES = sorted(glob.glob("activation_dataset/prompt_*.csv"))

data = []

for path in FILES:
    with open(path) as f:
        rows = list(csv.DictReader(f))

    by_layer = {}

    for r in rows:
        layer = int(r["layer"])

        x = np.array(
            [float(r[f"v{i}"]) for i in range(1536)],
            dtype=np.float64,
        )

        by_layer[layer] = x

    data.append(by_layer)

print("prompts:", len(data))
print()

pairs = []

for d in data:
    layers = sorted(d)

    for a, b in zip(layers, layers[1:]):
        xa = d[a]
        xb = d[b]

        cosine = np.dot(xa, xb) / (
            np.linalg.norm(xa) *
            np.linalg.norm(xb)
        )

        pairs.append((a, b, xa, xb, cosine))

print("transition       samples   mean cosine    std")
print("------------------------------------------------")

for a, b in sorted(set((x[0], x[1]) for x in pairs)):
    vals = [
        x[4]
        for x in pairs
        if x[0] == a and x[1] == b
    ]

    print(
        f"L{a:02d}->L{b:02d}       "
        f"{len(vals):3d}       "
        f"{np.mean(vals):.9f}   "
        f"{np.std(vals):.9f}"
    )
