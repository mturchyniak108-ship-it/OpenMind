import json
import random
from pathlib import Path
from statistics import mean

V4 = Path("experiments/model_fractal/q8_parameter_field_v4.json")
OUT = Path("experiments/model_fractal/q8_phase_blind_discovery_v13.json")

SEED = 20260823
PERMUTATIONS = 5000

TARGETS = {
    "attn_v.bias",
    "ffn_up.weight",
}

WINDOW_SIZES = [3, 4, 5, 6]

rng = random.Random(SEED)

v4 = json.loads(V4.read_text())

transitions = v4["transitions"]
components = v4["components"]

DISCOVERY_COMPONENTS = [
    c for c in components
    if c not in TARGETS
]


def field(t):
    return float(t["value_divergence"])


def scale(t):
    return float(t["scale_divergence"])


def component_value(t, component):
    return float(
        t["components"][component]["value"]
    )


def window_mean(items, fn):
    return mean(fn(t) for t in items)


def component_delta(window, outside, component):
    return (
        window_mean(
            window,
            lambda t: component_value(t, component),
        )
        -
        window_mean(
            outside,
            lambda t: component_value(t, component),
        )
    )


def permutation_p(window, outside, component):
    observed = abs(
        component_delta(
            window,
            outside,
            component,
        )
    )

    values = [
        component_value(t, component)
        for t in window + outside
    ]

    n = len(window)
    extreme = 0

    for _ in range(PERMUTATIONS):
        shuffled = values[:]
        rng.shuffle(shuffled)

        a = shuffled[:n]
        b = shuffled[n:]

        d = abs(mean(a) - mean(b))

        if d >= observed:
            extreme += 1

    return (
        extreme + 1
    ) / (
        PERMUTATIONS + 1
    )


def discovery_score(window, outside):
    field_delta = (
        window_mean(window, field)
        -
        window_mean(outside, field)
    )

    scale_delta = (
        window_mean(window, scale)
        -
        window_mean(outside, scale)
    )

    component_deltas = {}

    for component in DISCOVERY_COMPONENTS:
        component_deltas[component] = (
            component_delta(
                window,
                outside,
                component,
            )
        )

    component_signal = mean(
        abs(x)
        for x in component_deltas.values()
    )

    # Equal-weight structural evidence.
    score = (
        abs(field_delta)
        + abs(scale_delta)
        + component_signal
    )

    return {
        "score": score,
        "field_delta": field_delta,
        "scale_delta": scale_delta,
        "component_signal": component_signal,
        "component_deltas": component_deltas,
    }


print("=" * 72)
print(" OPENMIND / Q8 TARGET-BLIND PHASE DISCOVERY V13")
print("=" * 72)

print()
print("Transitions:", len(transitions))
print("Components:", len(components))
print("Discovery components:", len(DISCOVERY_COMPONENTS))
print("Excluded targets:", sorted(TARGETS))
print("Window sizes:", WINDOW_SIZES)
print("Permutations:", PERMUTATIONS)
print("Seed:", SEED)

windows = []

for size in WINDOW_SIZES:

    for start in range(
        0,
        len(transitions) - size + 1,
    ):

        window = transitions[
            start:start + size
        ]

        outside = (
            transitions[:start]
            +
            transitions[start + size:]
        )

        if not outside:
            continue

        first = window[0]["from"]
        last = window[-1]["to"]

        result = discovery_score(
            window,
            outside,
        )

        windows.append({
            "start_index": start,
            "size": size,
            "from": first,
            "to": last,
            **result,
        })


windows.sort(
    key=lambda x: x["score"],
    reverse=True,
)

print()
print("=" * 72)
print(" TARGET-BLIND DISCOVERY RANKING")
print("=" * 72)

for rank, w in enumerate(
    windows[:20],
    start=1,
):

    print(
        f"{rank:02d}. "
        f"L{w['from']:02d}-L{w['to']:02d} "
        f"size={w['size']} "
        f"score={w['score']:.6f} "
        f"field={w['field_delta']:+.6f} "
        f"scale={w['scale_delta']:+.6f} "
        f"blind_components={w['component_signal']:.6f}"
    )


print()
print("=" * 72)
print(" WINDOW-SIZE WINNERS")
print("=" * 72)

size_winners = {}

for size in WINDOW_SIZES:

    candidates = [
        w for w in windows
        if w["size"] == size
    ]

    winner = max(
        candidates,
        key=lambda x: x["score"],
    )

    size_winners[str(size)] = winner

    print(
        f"size={size} | "
        f"L{winner['from']:02d}-L{winner['to']:02d} | "
        f"score={winner['score']:.6f}"
    )


# Global target-blind winner.
winner = windows[0]

start = winner["start_index"]
size = winner["size"]

selected = transitions[
    start:start + size
]

outside = (
    transitions[:start]
    +
    transitions[start + size:]
)

print()
print("=" * 72)
print(" SELECTED TARGET-BLIND REGION")
print("=" * 72)

print(
    f"L{winner['from']:02d}-L{winner['to']:02d}"
)

print(
    "Transitions:",
    [
        [t["from"], t["to"]]
        for t in selected
    ],
)

print(
    f"Discovery score: "
    f"{winner['score']:.6f}"
)

print(
    f"Field delta: "
    f"{winner['field_delta']:+.6f}"
)

print(
    f"Scale delta: "
    f"{winner['scale_delta']:+.6f}"
)


print()
print("=" * 72)
print(" POST-HOC TARGET VALIDATION")
print("=" * 72)

target_validation = {}

for component in sorted(TARGETS):

    d = component_delta(
        selected,
        outside,
        component,
    )

    p = permutation_p(
        selected,
        outside,
        component,
    )

    target_validation[component] = {
        "delta": d,
        "p": p,
    }

    print(
        f"{component:<25} "
        f"delta={d:+.6f} | "
        f"p={p:.4f}"
    )


print()
print("=" * 72)
print(" TARGET DIRECTION")
print("=" * 72)

both_negative = all(
    target_validation[c]["delta"] < 0
    for c in TARGETS
)

both_positive = all(
    target_validation[c]["delta"] > 0
    for c in TARGETS
)

if both_negative:
    direction = "BOTH_NEGATIVE"

elif both_positive:
    direction = "BOTH_POSITIVE"

else:
    direction = "MIXED"

print("Target direction:", direction)


print()
print("=" * 72)
print(" NEIGHBORHOOD COMPETITION")
print("=" * 72)

same_size = [
    w for w in windows
    if w["size"] == size
]

same_size.sort(
    key=lambda x: x["from"]
)

neighborhood = []

for w in same_size:

    neighborhood.append({
        "from": w["from"],
        "to": w["to"],
        "score": w["score"],
        "field_delta": w["field_delta"],
        "scale_delta": w["scale_delta"],
        "component_signal":
            w["component_signal"],
        "selected":
            (
                w["from"] == winner["from"]
                and
                w["to"] == winner["to"]
            ),
    })

    marker = "*" if neighborhood[-1]["selected"] else " "

    print(
        f"{marker} "
        f"L{w['from']:02d}-L{w['to']:02d} "
        f"score={w['score']:.6f}"
    )


rank_of_selected = (
    next(
        i + 1
        for i, w in enumerate(
            sorted(
                same_size,
                key=lambda x: x["score"],
                reverse=True,
            )
        )
        if (
            w["from"] == winner["from"]
            and
            w["to"] == winner["to"]
        )
    )
)


print()
print("=" * 72)
print(" V12 CORE REGION CHECK")
print("=" * 72)

v12_core = (
    winner["from"] <= 8
    and winner["to"] >= 12
)

print(
    "Target-blind region overlaps "
    "V12 core L08-L12:",
    v12_core,
)

print(
    "Selected window:",
    f"L{winner['from']:02d}-L{winner['to']:02d}",
)

print(
    "Same-size neighborhood rank:",
    f"{rank_of_selected}/{len(same_size)}",
)


result = {
    "format":
        "OpenMind Q8 Target-Blind Phase Discovery V13",

    "configuration": {
        "seed": SEED,
        "permutations": PERMUTATIONS,
        "window_sizes": WINDOW_SIZES,
    },

    "excluded_targets":
        sorted(TARGETS),

    "discovery_components":
        DISCOVERY_COMPONENTS,

    "window_count":
        len(windows),

    "ranked_windows":
        windows,

    "window_size_winners":
        size_winners,

    "selected_region": {
        "from": winner["from"],
        "to": winner["to"],
        "size": size,
        "start_index": start,
        "score": winner["score"],
        "field_delta": winner["field_delta"],
        "scale_delta": winner["scale_delta"],
        "component_signal":
            winner["component_signal"],
        "transitions": [
            [t["from"], t["to"]]
            for t in selected
        ],
    },

    "target_validation":
        target_validation,

    "target_direction":
        direction,

    "neighborhood": {
        "window_size": size,
        "rank": rank_of_selected,
        "count": len(same_size),
        "windows": neighborhood,
    },

    "v12_core_overlap":
        v12_core,
}

OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

OUT.write_text(
    json.dumps(
        result,
        indent=2,
        sort_keys=True,
    )
)

print()
print("Output:", OUT)
print()
print("Q8 TARGET-BLIND PHASE DISCOVERY V13 COMPLETE")
