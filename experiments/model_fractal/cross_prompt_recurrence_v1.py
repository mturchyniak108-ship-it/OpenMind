import csv
import math
import statistics
from pathlib import Path

FILES = [
    Path("activation_vectors_A.csv"),
    Path("activation_vectors_B.csv"),
    Path("activation_vectors_C.csv"),
    Path("activation_vectors_D.csv"),
]

MIN_GAP = 2
TOP = 30


def load(path):
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
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))

    if na == 0 or nb == 0:
        return 0.0

    return dot / (na * nb)


datasets = {}

for path in FILES:
    datasets[path.stem] = load(path)

names = list(datasets)
layers = sorted(datasets[names[0]])

print("=" * 72)
print(" OPENMIND / CROSS-PROMPT RECURRENCE VALIDATION V1")
print("=" * 72)

print(f"prompts:    {', '.join(names)}")
print(f"layers:     {len(layers)}")
print(f"dimension:  {len(datasets[names[0]][layers[0]])}")
print()

results = []

for gap in range(MIN_GAP, len(layers)):

    for source in layers:
        target = source + gap

        if target not in layers:
            continue

        scores = []

        for name in names:
            scores.append(
                cosine(
                    datasets[name][source],
                    datasets[name][target],
                )
            )

        results.append({
            "gap": gap,
            "source": source,
            "target": target,
            "mean": statistics.fmean(scores),
            "std": statistics.pstdev(scores),
            "minimum": min(scores),
            "maximum": max(scores),
            "scores": scores,
        })


print("=" * 72)
print(" MOST STABLE CROSS-PROMPT RECURRENCES")
print("=" * 72)

print(
    "source -> target | gap | mean | std | min | max | A B C D"
)
print("-" * 72)

stable = sorted(
    results,
    key=lambda x: (-x["mean"], x["std"])
)

for r in stable[:TOP]:
    scores = " ".join(
        f"{x:.4f}" for x in r["scores"]
    )

    print(
        f"L{r['source']:02d} -> L{r['target']:02d} | "
        f"{r['gap']:3d} | "
        f"{r['mean']:.6f} | "
        f"{r['std']:.6f} | "
        f"{r['minimum']:.6f} | "
        f"{r['maximum']:.6f} | "
        f"{scores}"
    )


print()
print("=" * 72)
print(" GAP STABILITY SUMMARY")
print("=" * 72)

print("gap | count | mean | mean_std | worst | best")
print("-" * 60)

for gap in range(MIN_GAP, len(layers)):

    group = [
        r for r in results
        if r["gap"] == gap
    ]

    if not group:
        continue

    print(
        f"{gap:3d} | "
        f"{len(group):5d} | "
        f"{statistics.fmean(r['mean'] for r in group):.6f} | "
        f"{statistics.fmean(r['std'] for r in group):.6f} | "
        f"{min(r['mean'] for r in group):.6f} | "
        f"{max(r['mean'] for r in group):.6f}"
    )


print()
print("=" * 72)
print(" PROMPT-INVARIANT CANDIDATES")
print("=" * 72)

# Require:
#   mean cosine >= .90
#   cross-prompt std <= .02
#   every prompt >= .85

candidates = [
    r for r in results
    if (
        r["mean"] >= 0.90
        and r["std"] <= 0.02
        and r["minimum"] >= 0.85
    )
]

candidates.sort(
    key=lambda x: (-x["mean"], x["std"])
)

for r in candidates[:TOP]:
    print(
        f"L{r['source']:02d} -> L{r['target']:02d} "
        f"gap={r['gap']} "
        f"mean={r['mean']:.6f} "
        f"std={r['std']:.6f} "
        f"min={r['minimum']:.6f}"
    )

print()
print(f"Prompt-invariant candidates: {len(candidates)}")
print()
print("CROSS-PROMPT VALIDATION COMPLETE")
