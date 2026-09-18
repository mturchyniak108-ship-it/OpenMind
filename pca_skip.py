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
print(" OPENMIND / PCA LATENT SKIP TEST")
print("============================================================")
print("prompts:", len(datasets))
print("source: L%02d" % source)
print()

for K in [16, 32, 64, 128]:

    print("------------------------------------------------------------")
    print("LATENT DIMENSIONS:", K)
    print("------------------------------------------------------------")

    scores = {target: [] for target in layers[1:]}

    for test_i in range(len(datasets)):

        train = [
            d for i, d in enumerate(datasets)
            if i != test_i
        ]

        test = datasets[test_i]

        X = np.stack([d[source] for d in train])

        # Center the training source states.
        mean = X.mean(axis=0)

        Xc = X - mean

        # PCA through SVD.
        U, S, Vt = np.linalg.svd(
            Xc,
            full_matrices=False
        )

        components = Vt[:K]

        Z = Xc @ components.T

        # Add bias.
        Z1 = np.column_stack([
            Z,
            np.ones(len(Z))
        ])

        test_z = (
            test[source] - mean
        ) @ components.T

        test_z1 = np.append(
            test_z,
            1.0
        )

        for target in layers[1:]:

            Y = np.stack([
                d[target]
                for d in train
            ])

            W, *_ = np.linalg.lstsq(
                Z1,
                Y,
                rcond=1e-6
            )

            pred = test_z1 @ W

            actual = test[target]

            cosine = np.dot(pred, actual) / (
                np.linalg.norm(pred) *
                np.linalg.norm(actual)
            )

            scores[target].append(cosine)

    for target in layers[1:]:

        vals = np.array(scores[target])

        print(
            f"L{target:02d}  "
            f"mean={vals.mean():.6f}  "
            f"std={vals.std():.6f}  "
            f"min={vals.min():.6f}"
        )

print()
print("Complete.")
