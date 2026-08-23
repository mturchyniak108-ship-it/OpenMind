import json
import math
from pathlib import Path

INPUT = Path(
    "experiments/model_fractal/transition_field_v5.json"
)

OUTPUT = Path(
    "experiments/model_fractal/transition_geometry_v6.json"
)

EPS = 1e-12

d = json.loads(INPUT.read_text())
transitions = d["transitions"]

print("=" * 72)
print(" OPENMIND / TRANSITION GEOMETRY V6")
print("=" * 72)

print()
print(f"Transitions: {len(transitions)}")


# ----------------------------------------------------------------------
# Extract transition measurements
# ----------------------------------------------------------------------

energy = [
    float(t["transition_energy"])
    for t in transitions
]

cosine = [
    float(t["cosine_similarity"])
    for t in transitions
]

relative = [
    float(t["relative_transition_energy"])
    for t in transitions
]



# ----------------------------------------------------------------------
# First and second differences
# ----------------------------------------------------------------------

first_energy = []

for i in range(1, len(energy)):
    first_energy.append(
        energy[i] - energy[i - 1]
    )


second_energy = []

for i in range(1, len(first_energy)):
    second_energy.append(
        first_energy[i] - first_energy[i - 1]
    )


# ----------------------------------------------------------------------
# Normalized local neighborhoods
# ----------------------------------------------------------------------

def normalize(values):
    if not values:
        return []

    scale = max(abs(x) for x in values)

    if scale <= EPS:
        return [0.0 for _ in values]

    return [
        x / scale
        for x in values
    ]


def neighborhood(values, center, radius=2):
    lo = max(0, center - radius)
    hi = min(len(values), center + radius + 1)

    return values[lo:hi]


# ----------------------------------------------------------------------
# Peak detection
# ----------------------------------------------------------------------

peaks = []

for i in range(1, len(energy) - 1):

    if (
        energy[i] >= energy[i - 1]
        and energy[i] >= energy[i + 1]
    ):
        peaks.append(i)


peaks.sort(
    key=lambda i: energy[i],
    reverse=True
)


# ----------------------------------------------------------------------
# Self-similarity between peak neighborhoods
# ----------------------------------------------------------------------

def profile_similarity(a, b):
    n = min(len(a), len(b))

    if n == 0:
        return 0.0

    a = a[:n]
    b = b[:n]

    dot = sum(x * y for x, y in zip(a, b))

    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))

    if na <= EPS or nb <= EPS:
        return 0.0

    return dot / (na * nb)


peak_profiles = {}

for rank, index in enumerate(peaks):

    profile = normalize(
        neighborhood(
            energy,
            index,
            radius=2,
        )
    )

    peak_profiles[str(index)] = {
        "rank": rank + 1,
        "transition_index": index,
        "from_layer": transitions[index]["from_layer"],
        "to_layer": transitions[index]["to_layer"],
        "energy": energy[index],
        "cosine": cosine[index],
        "relative_energy": relative[index],
        "profile": profile,
    }


similarities = []

for i in range(len(peaks)):

    for j in range(i + 1, len(peaks)):

        a = peaks[i]
        b = peaks[j]

        similarity = profile_similarity(
            peak_profiles[str(a)]["profile"],
            peak_profiles[str(b)]["profile"],
        )

        similarities.append(
            {
                "peak_a": a,
                "peak_b": b,
                "layer_a": [
                    transitions[a]["from_layer"],
                    transitions[a]["to_layer"],
                ],
                "layer_b": [
                    transitions[b]["from_layer"],
                    transitions[b]["to_layer"],
                ],
                "similarity": similarity,
            }
        )


similarities.sort(
    key=lambda x: x["similarity"],
    reverse=True
)


# ----------------------------------------------------------------------
# Transition records
# ----------------------------------------------------------------------

geometry = []

for i, t in enumerate(transitions):

    geometry.append(
        {
            "index": i,
            "from_layer": t["from_layer"],
            "to_layer": t["to_layer"],
            "energy": energy[i],
            "cosine": cosine[i],
            "relative_energy": relative[i],
            "first_energy_delta": (
                first_energy[i - 1]
                if i >= 1
                else None
            ),
            "second_energy_delta": (
                second_energy[i - 2]
                if i >= 2
                else None
            ),
        }
    )


# ----------------------------------------------------------------------
# Output
# ----------------------------------------------------------------------

output = {
    "schema": "openmind.transition_geometry.v6",
    "source": str(INPUT),
    "transition_count": len(transitions),

    "transitions": geometry,

    "peaks": [
        peak_profiles[str(i)]
        for i in peaks
    ],

    "peak_similarity": similarities,

    "summary": {
        "highest_energy_transition": (
            max(
                geometry,
                key=lambda x: x["energy"]
            )
            if geometry
            else None
        ),

        "lowest_cosine_transition": (
            min(
                geometry,
                key=lambda x: x["cosine"]
            )
            if geometry
            else None
        ),

        "highest_relative_transition": (
            max(
                geometry,
                key=lambda x: x["relative_energy"]
            )
            if geometry
            else None
        ),
    },
}

OUTPUT.write_text(
    json.dumps(
        output,
        indent=2,
    )
)

print()
print("=== ENERGY PEAKS ===")

for p in peaks[:10]:

    t = transitions[p]

    print(
        f"L{t['from_layer']:02d} -> "
        f"L{t['to_layer']:02d} "
        f"energy={energy[p]:.8f} "
        f"cos={cosine[p]:.8f}"
    )


print()
print("=== MOST SELF-SIMILAR PEAK PAIRS ===")

for item in similarities[:10]:

    a = item["layer_a"]
    b = item["layer_b"]

    print(
        f"L{a[0]:02d}->L{a[1]:02d} "
        f"vs "
        f"L{b[0]:02d}->L{b[1]:02d} "
        f"similarity={item['similarity']:.8f}"
    )


print()
print(f"Output: {OUTPUT}")
print()
print("TRANSITION GEOMETRY COMPLETE")
