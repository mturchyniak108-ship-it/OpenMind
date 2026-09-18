import json
import math
from pathlib import Path

INPUT = Path(
    "experiments/model_fractal/q8_parameter_field_v4_1.json"
)

OUTPUT = Path(
    "experiments/model_fractal/transition_field_v5.json"
)

EPS = 1e-12

d = json.loads(INPUT.read_text())

layers = d["layers"]

layer_ids = sorted(
    map(int, layers.keys())
)

components = d["components"]


def rms(component):
    stats = component.get("stats", {})

    value = stats.get("rms")

    if value is None:
        value = stats.get("RMS")

    if value is None:
        raise ValueError(
            f"Missing RMS statistic in component metadata: {component}"
        )

    return float(value)


def vector(layer_id):
    layer = layers[str(layer_id)]

    return [
        rms(layer[c])
        for c in components
        if c in layer
    ]


def cosine(a, b):

    dot = sum(
        x * y
        for x, y in zip(a, b)
    )

    na = math.sqrt(
        sum(x * x for x in a)
    )

    nb = math.sqrt(
        sum(y * y for y in b)
    )

    if na <= EPS or nb <= EPS:
        return 0.0

    return dot / (na * nb)


transitions = []

for a, b in zip(
    layer_ids,
    layer_ids[1:],
):

    va = vector(a)
    vb = vector(b)

    deltas = [
        y - x
        for x, y in zip(va, vb)
    ]

    relative = [
        (y - x) / max(abs(x), EPS)
        for x, y in zip(va, vb)
    ]

    energy = math.sqrt(
        sum(
            delta * delta
            for delta in deltas
        )
        / len(deltas)
    )

    relative_energy = math.sqrt(
        sum(
            value * value
            for value in relative
        )
        / len(relative)
    )

    transitions.append(
        {
            "from_layer": a,
            "to_layer": b,

            "delta": deltas,

            "relative_delta": relative,

            "transition_energy": energy,

            "relative_transition_energy":
                relative_energy,

            "cosine_similarity":
                cosine(va, vb),

            "mean_delta":
                sum(deltas) / len(deltas),

            "max_abs_delta":
                max(
                    abs(x)
                    for x in deltas
                ),

            "min_delta":
                min(deltas),

            "max_delta":
                max(deltas),
        }
    )


# ------------------------------------------------------------
# Rank transitions
# ------------------------------------------------------------

ranked_energy = sorted(
    transitions,
    key=lambda x:
        x["transition_energy"],
    reverse=True,
)

ranked_relative = sorted(
    transitions,
    key=lambda x:
        x["relative_transition_energy"],
    reverse=True,
)

ranked_similarity = sorted(
    transitions,
    key=lambda x:
        x["cosine_similarity"],
)


result = {
    "schema": "openmind.transition_field.v5",

    "source": str(INPUT),

    "layer_count": len(layer_ids),

    "component_count": len(components),

    "components": components,

    "transitions": transitions,

    "rankings": {
        "highest_transition_energy": [
            {
                "from_layer":
                    x["from_layer"],
                "to_layer":
                    x["to_layer"],
                "value":
                    x["transition_energy"],
            }
            for x in ranked_energy
        ],

        "highest_relative_transition_energy": [
            {
                "from_layer":
                    x["from_layer"],
                "to_layer":
                    x["to_layer"],
                "value":
                    x["relative_transition_energy"],
            }
            for x in ranked_relative
        ],

        "lowest_cosine_similarity": [
            {
                "from_layer":
                    x["from_layer"],
                "to_layer":
                    x["to_layer"],
                "value":
                    x["cosine_similarity"],
            }
            for x in ranked_similarity
        ],
    },
}


OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

OUTPUT.write_text(
    json.dumps(
        result,
        indent=2,
    )
)

print("=" * 72)
print(" OPENMIND / TRANSITION FIELD V5")
print("=" * 72)

print()
print("Layers:", len(layer_ids))
print("Components:", len(components))
print("Transitions:", len(transitions))

print()
print("=== HIGHEST TRANSITION ENERGY ===")

for x in ranked_energy[:10]:

    print(
        f"L{x['from_layer']:02d} -> "
        f"L{x['to_layer']:02d}  "
        f"energy="
        f"{x['transition_energy']:.8f}  "
        f"cos="
        f"{x['cosine_similarity']:.8f}"
    )

print()
print("=== HIGHEST RELATIVE TRANSITION ===")

for x in ranked_relative[:10]:

    print(
        f"L{x['from_layer']:02d} -> "
        f"L{x['to_layer']:02d}  "
        f"relative="
        f"{x['relative_transition_energy']:.8f}"
    )

print()
print("=== LOWEST COMPONENT COSINE ===")

for x in ranked_similarity[:10]:

    print(
        f"L{x['from_layer']:02d} -> "
        f"L{x['to_layer']:02d}  "
        f"cos="
        f"{x['cosine_similarity']:.8f}"
    )

print()
print("Output:", OUTPUT)
print()
print("TRANSITION FIELD COMPLETE")
