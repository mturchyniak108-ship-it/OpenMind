import json
import math
from pathlib import Path

INPUT = Path(
    "experiments/model_fractal/transition_field_v5.json"
)

OUTPUT = Path(
    "experiments/model_fractal/transition_recurrence_v7.json"
)

EPS = 1e-12

d = json.loads(INPUT.read_text())
transitions = d["transitions"]

components = d["components"]
n = len(transitions)


def normalize(v):
    norm = math.sqrt(sum(x * x for x in v))

    if norm <= EPS:
        return [0.0] * len(v)

    return [x / norm for x in v]


vectors = [
    normalize(
        [float(x) for x in t["delta"]]
    )
    for t in transitions
]


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))

    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))

    if na <= EPS or nb <= EPS:
        return 0.0

    return dot / (na * nb)


similarity_matrix = []

for i in range(n):
    row = []

    for j in range(n):
        row.append(
            cosine(vectors[i], vectors[j])
        )

    similarity_matrix.append(row)


pairs = []

for i in range(n):
    for j in range(i + 1, n):

        similarity = similarity_matrix[i][j]

        pairs.append(
            {
                "transition_a": {
                    "from_layer":
                        transitions[i]["from_layer"],
                    "to_layer":
                        transitions[i]["to_layer"],
                },

                "transition_b": {
                    "from_layer":
                        transitions[j]["from_layer"],
                    "to_layer":
                        transitions[j]["to_layer"],
                },

                "layer_separation":
                    abs(
                        transitions[i]["from_layer"]
                        -
                        transitions[j]["from_layer"]
                    ),

                "similarity": similarity,
            }
        )


pairs.sort(
    key=lambda x: x["similarity"],
    reverse=True,
)


# ------------------------------------------------------------
# Recurrence by layer separation
# ------------------------------------------------------------

separation_groups = {}

for pair in pairs:

    separation = pair["layer_separation"]

    separation_groups.setdefault(
        str(separation),
        []
    ).append(
        pair["similarity"]
    )


separation_summary = []

for separation, values in sorted(
    separation_groups.items(),
    key=lambda x: int(x[0])
):

    separation_summary.append(
        {
            "layer_separation": int(separation),

            "count": len(values),

            "mean_similarity":
                sum(values) / len(values),

            "max_similarity":
                max(values),

            "min_similarity":
                min(values),
        }
    )


# ------------------------------------------------------------
# Best recurrence partner for each transition
# ------------------------------------------------------------

nearest = []

for i in range(n):

    candidates = [
        p for p in pairs
        if (
            p["transition_a"]["from_layer"]
            == transitions[i]["from_layer"]
            or
            p["transition_b"]["from_layer"]
            == transitions[i]["from_layer"]
        )
    ]

    if candidates:

        nearest.append(
            max(
                candidates,
                key=lambda x: x["similarity"]
            )
        )


result = {
    "schema":
        "openmind.transition_recurrence.v7",

    "source":
        str(INPUT),

    "transition_count":
        n,

    "components":
        components,

    "similarity_matrix":
        similarity_matrix,

    "ranked_pairs":
        pairs,

    "separation_summary":
        separation_summary,

    "nearest_recurrence":
        nearest,
}


OUTPUT.write_text(
    json.dumps(
        result,
        indent=2
    )
)


print("=" * 72)
print(" OPENMIND / TRANSITION RECURRENCE V7")
print("=" * 72)

print()
print(f"Transitions: {n}")

print()
print("=== STRONGEST RECURRENCES ===")

for pair in pairs[:15]:

    a = pair["transition_a"]
    b = pair["transition_b"]

    print(
        f"L{a['from_layer']:02d}->L{a['to_layer']:02d} "
        f"vs "
        f"L{b['from_layer']:02d}->L{b['to_layer']:02d} "
        f"similarity={pair['similarity']:.8f} "
        f"separation={pair['layer_separation']}"
    )


print()
print("=== RECURRENCE BY LAYER SEPARATION ===")

for item in separation_summary:

    print(
        f"ΔL={item['layer_separation']:2d} "
        f"count={item['count']:2d} "
        f"mean={item['mean_similarity']:.8f} "
        f"max={item['max_similarity']:.8f}"
    )


print()
print(
    f"Output: {OUTPUT}"
)

print()
print("TRANSITION RECURRENCE COMPLETE")
