import json
import math
from pathlib import Path

PATH = Path("experiments/model_fractal/gguf_structure_v1.json")

data = json.loads(PATH.read_text())

layers = data["layer_vectors"]
layer_ids = data["layer_ids"]

def normalized_distance(a, b):
    total = 0.0

    for x, y in zip(a, b):
        scale = max(abs(x), abs(y), 1.0)
        d = (x - y) / scale
        total += d * d

    return math.sqrt(total / len(a))

print("=" * 72)
print(" OPENMIND / STRUCTURAL DIVERGENCE V1")
print("=" * 72)

print()
print("Layers:", len(layer_ids))
print("Feature dimensions:", len(layers[str(layer_ids[0])]))
print()

scores = []

for a, b in zip(layer_ids, layer_ids[1:]):

    va = layers[str(a)]
    vb = layers[str(b)]

    score = normalized_distance(va, vb)

    scores.append((a, b, score))

    print(
        f"L{a:02d} -> L{b:02d} | "
        f"structural={score:.6f}"
    )

print()
print("=" * 72)
print(" STRUCTURAL TRANSITION RANKING")
print("=" * 72)

for a, b, score in sorted(
    scores,
    key=lambda x: x[2],
    reverse=True
):
    print(
        f"L{a:02d} -> L{b:02d} | "
        f"{score:.6f}"
    )

values = [x[2] for x in scores]

print()
print("=" * 72)
print(" SUMMARY")
print("=" * 72)

print(f"Minimum structural: {min(values):.6f}")
print(f"Maximum structural: {max(values):.6f}")
print(f"Mean structural:    {sum(values)/len(values):.6f}")

maximum = max(scores, key=lambda x: x[2])
minimum = min(scores, key=lambda x: x[2])

print(
    f"Maximum transition: "
    f"L{maximum[0]:02d} -> L{maximum[1]:02d}"
)

print(
    f"Minimum transition: "
    f"L{minimum[0]:02d} -> L{minimum[1]:02d}"
)

print()
print("STRUCTURAL DIVERGENCE COMPLETE")
