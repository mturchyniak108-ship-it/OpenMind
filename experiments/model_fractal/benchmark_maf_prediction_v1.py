import csv
import math
import statistics
from pathlib import Path

INPUT = Path("activation_vectors.csv")

def load_vectors(path):
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))

    vectors = {}
    for row in rows:
        layer = int(row["layer"])
        values = []
        i = 0
        while f"v{i}" in row:
            values.append(float(row[f"v{i}"]))
            i += 1
        vectors[layer] = values

    return vectors

def cosine(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(x*x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)

def mse(a, b):
    return statistics.fmean(
        (x-y)*(x-y) for x, y in zip(a, b)
    )

def norm_rmse(a, b):
    err = math.sqrt(mse(a, b))
    scale = math.sqrt(
        statistics.fmean(x*x for x in b)
    )
    return err / scale if scale else 0.0

vectors = load_vectors(INPUT)
layers = sorted(vectors)

print("=" * 72)
print(" OPENMIND / MAF PREDICTIVE RECURRENCE BENCHMARK V1")
print("=" * 72)
print(f"layers:     {len(layers)}")
print(f"dimension:  {len(vectors[layers[0]])}")
print()

results = []

for gap in range(2, len(layers)):
    for source in layers:
        target = source + gap

        if target not in vectors:
            continue

        a = vectors[source]
        b = vectors[target]

        c = cosine(a, b)
        e = mse(a, b)
        r = norm_rmse(a, b)

        results.append(
            (gap, source, target, c, e, r)
        )

print("gap | source | target | cosine | mse | norm_rmse")
print("-" * 72)

for gap, source, target, c, e, r in sorted(
    results,
    key=lambda x: (-x[3], x[0], x[1])
)[:30]:
    print(
        f"{gap:3d} | "
        f"L{source:02d} | "
        f"L{target:02d} | "
        f"{c:0.9f} | "
        f"{e:0.6f} | "
        f"{r:0.6f}"
    )

print()
print("=" * 72)
print(" GAP SUMMARY")
print("=" * 72)
print("gap | count | mean_cosine | mean_norm_rmse")
print("-" * 56)

for gap in range(2, len(layers)):
    group = [r for r in results if r[0] == gap]
    if not group:
        continue

    print(
        f"{gap:3d} | "
        f"{len(group):5d} | "
        f"{statistics.fmean(r[3] for r in group):0.9f} | "
        f"{statistics.fmean(r[5] for r in group):0.6f}"
    )

print()
print("=" * 72)
print(" BEST RECURRENCE CANDIDATES")
print("=" * 72)

for gap, source, target, c, e, r in sorted(
    [x for x in results if x[0] >= 4],
    key=lambda x: -x[3]
)[:20]:
    print(
        f"L{source:02d} -> L{target:02d} "
        f"gap={gap} "
        f"cosine={c:.9f} "
        f"norm_rmse={r:.6f}"
    )

print()
print("BENCHMARK COMPLETE")
