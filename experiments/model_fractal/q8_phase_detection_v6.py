import json
import math
from pathlib import Path


PATH = Path(
    "experiments/model_fractal/q8_parameter_field_v4.json"
)

OUT = Path(
    "experiments/model_fractal/q8_phase_detection_v6.json"
)


# ============================================================
# LOAD
# ============================================================

data = json.loads(PATH.read_text())

layer_ids = data["layer_ids"]
components = data["components"]
transitions = data["transitions"]


# ============================================================
# BUILD TRANSITION MAP
# ============================================================

transition_map = {}

for transition in transitions:

    key = (
        transition["from"],
        transition["to"],
    )

    transition_map[key] = transition


# ============================================================
# COMPONENT VECTORS
# ============================================================

def component_vector(layer_a, layer_b):

    transition = transition_map.get(
        (layer_a, layer_b)
    )

    if transition is None:
        return []

    values = []

    for component in components:

        entry = transition[
            "components"
        ].get(component)

        if entry is None:
            values.append(0.0)
        else:
            values.append(
                float(entry["value"])
            )

    return values


# ============================================================
# VECTOR DISTANCE
# ============================================================

def distance(a, b):

    if not a or not b:
        return 0.0

    total = 0.0

    for x, y in zip(a, b):

        scale = max(
            abs(x),
            abs(y),
            1e-12,
        )

        d = (
            x - y
        ) / scale

        total += d * d

    return math.sqrt(
        total / len(a)
    )


# ============================================================
# LAYER FIELD SIGNATURES
#
# Each layer gets the average of the incoming
# and outgoing parameter-field transition.
# ============================================================

layer_vectors = {}

for layer in layer_ids:

    incoming = None
    outgoing = None

    if layer > layer_ids[0]:

        incoming = component_vector(
            layer - 1,
            layer,
        )

    if layer < layer_ids[-1]:

        outgoing = component_vector(
            layer,
            layer + 1,
        )

    if incoming and outgoing:

        vector = [
            (
                x + y
            ) / 2.0
            for x, y in zip(
                incoming,
                outgoing,
            )
        ]

    elif incoming:

        vector = incoming

    elif outgoing:

        vector = outgoing

    else:

        vector = [
            0.0
            for _ in components
        ]

    layer_vectors[layer] = vector


# ============================================================
# LOCAL PHASE DISTANCE
# ============================================================

phase_scores = []

for layer in layer_ids[1:-1]:

    previous = layer_vectors[
        layer - 1
    ]

    current = layer_vectors[
        layer
    ]

    following = layer_vectors[
        layer + 1
    ]

    left = distance(
        previous,
        current,
    )

    right = distance(
        current,
        following,
    )

    local = (
        left + right
    ) / 2.0

    phase_scores.append({
        "layer": layer,
        "left": left,
        "right": right,
        "local": local,
    })


# ============================================================
# TRANSITION STRENGTH
# ============================================================

transition_scores = []

for transition in transitions:

    a = transition["from"]
    b = transition["to"]

    values = [
        float(
            transition[
                "components"
            ][component]["value"]
        )
        for component in components
        if component in transition[
            "components"
        ]
    ]

    if not values:
        continue

    mean_value = (
        sum(values)
        / len(values)
    )

    strong = [
        component
        for component in components
        if component in transition[
            "components"
        ]
        and transition[
            "components"
        ][component]["value"] >= 0.75
    ]

    transition_scores.append({
        "from": a,
        "to": b,
        "mean": mean_value,
        "maximum": max(values),
        "strong_count": len(strong),
        "coherence": (
            len(strong)
            / len(values)
        ),
    })


# ============================================================
# RANKINGS
# ============================================================

phase_ranked = sorted(
    phase_scores,
    key=lambda x: x["local"],
    reverse=True,
)

transition_ranked = sorted(
    transition_scores,
    key=lambda x: (
        x["coherence"],
        x["mean"],
    ),
    reverse=True,
)


# ============================================================
# PHASE CANDIDATES
# ============================================================

if phase_ranked:

    phase_mean = (
        sum(
            x["local"]
            for x in phase_scores
        )
        / len(phase_scores)
    )

    phase_std = math.sqrt(
        sum(
            (
                x["local"]
                - phase_mean
            ) ** 2
            for x in phase_scores
        )
        / len(phase_scores)
    )

else:

    phase_mean = 0.0
    phase_std = 0.0


phase_threshold = (
    phase_mean
    + phase_std
)


phase_candidates = [
    x
    for x in phase_scores
    if x["local"] >= phase_threshold
]


# ============================================================
# OUTPUT
# ============================================================

output = {
    "format": (
        "OpenMind Q8 Phase "
        "Detection V6"
    ),
    "source": str(PATH),
    "layer_count": len(layer_ids),
    "component_count": len(components),

    "phase_statistics": {
        "mean": phase_mean,
        "std": phase_std,
        "threshold": phase_threshold,
    },

    "phase_scores": phase_scores,

    "phase_candidates": phase_candidates,

    "transition_scores": transition_scores,

    "rankings": {
        "phase": phase_ranked,
        "transition": transition_ranked,
    },
}


OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

OUT.write_text(
    json.dumps(
        output,
        indent=2,
        sort_keys=True,
    )
)


# ============================================================
# REPORT
# ============================================================

print("=" * 72)
print(
    " OPENMIND / Q8 PHASE DETECTION V6"
)
print("=" * 72)

print()
print("Layers:", len(layer_ids))
print("Components:", len(components))

print()
print("=" * 72)
print(" LOCAL PHASE SCORES")
print("=" * 72)

for item in phase_scores:

    print(
        f"L{item['layer']:02d} | "
        f"left={item['left']:.6f} | "
        f"right={item['right']:.6f} | "
        f"local={item['local']:.6f}"
    )


print()
print("=" * 72)
print(" PHASE BOUNDARY RANKING")
print("=" * 72)

for item in phase_ranked:

    print(
        f"L{item['layer']:02d} | "
        f"{item['local']:.6f}"
    )


print()
print("=" * 72)
print(" PHASE CANDIDATES")
print("=" * 72)

print(
    f"Mean:      {phase_mean:.6f}"
)

print(
    f"Std:       {phase_std:.6f}"
)

print(
    f"Threshold: {phase_threshold:.6f}"
)

if phase_candidates:

    for item in phase_candidates:

        print(
            f"L{item['layer']:02d} | "
            f"local={item['local']:.6f}"
        )

else:

    print("None")


print()
print("=" * 72)
print(" STRONGEST TRANSITIONS")
print("=" * 72)

for item in transition_ranked[:10]:

    print(
        f"L{item['from']:02d} -> "
        f"L{item['to']:02d} | "
        f"coherence="
        f"{item['coherence']:.3f} | "
        f"strong="
        f"{item['strong_count']:02d}/"
        f"{len(components):02d} | "
        f"mean="
        f"{item['mean']:.6f} | "
        f"max="
        f"{item['maximum']:.6f}"
    )


print()
print("=" * 72)
print(" SUMMARY")
print("=" * 72)

print(
    "Candidate phase boundaries:",
    len(phase_candidates),
)

if phase_candidates:

    print(
        "Boundary layers:",
        [
            x["layer"]
            for x in phase_candidates
        ],
    )

print()
print("Output:", OUT)

print()
print(
    "Q8 PHASE DETECTION V6 COMPLETE"
)
