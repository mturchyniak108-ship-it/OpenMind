import json
import random
from pathlib import Path
from statistics import mean

V4 = Path("experiments/model_fractal/q8_parameter_field_v4.json")
V13 = Path("experiments/model_fractal/q8_phase_blind_discovery_v13.json")
OUT = Path("experiments/model_fractal/q8_structural_matched_targets_v14.json")

SEED = 20260823
PERMUTATIONS = 5000

TARGETS = [
    "attn_v.bias",
    "ffn_up.weight",
]

WINDOW_SIZE = 4
TARGET_REGION = (8, 12)

rng = random.Random(SEED)

v4 = json.loads(V4.read_text())
v13 = json.loads(V13.read_text())

transitions = v4["transitions"]
components = v4["components"]


def mean_value(items, component):
    return mean(
        t["components"][component]["value"]
        for t in items
    )


def mean_field(items):
    return mean(
        t["value_divergence"]
        for t in items
    )


def mean_scale(items):
    return mean(
        t["scale_divergence"]
        for t in items
    )


def window(start, size=WINDOW_SIZE):
    return transitions[start:start + size]


def outside(start, size=WINDOW_SIZE):
    return (
        transitions[:start]
        +
        transitions[start + size:]
    )


def target_delta(items, outside_items, component):
    return (
        mean_value(items, component)
        -
        mean_value(outside_items, component)
    )


def structural_vector(items):
    return (
        mean_field(items),
        mean_scale(items),
    )


def distance(a, b):
    return (
        abs(a[0] - b[0])
        +
        abs(a[1] - b[1])
    )


print("=" * 72)
print(" OPENMIND / Q8 STRUCTURAL-MATCHED TARGET TEST V14")
print("=" * 72)

print()
print("Target region: L08-L12")
print("Window size:", WINDOW_SIZE)
print("Targets:", TARGETS)
print("Permutations:", PERMUTATIONS)
print("Seed:", SEED)


# ------------------------------------------------------------
# Build all windows of the target size.
# ------------------------------------------------------------

windows = []

for start in range(
    0,
    len(transitions) - WINDOW_SIZE + 1,
):

    items = window(start)
    outside_items = outside(start)

    first = items[0]["from"]
    last = items[-1]["to"]

    field = mean_field(items)
    scale = mean_scale(items)

    windows.append({
        "start": start,
        "from": first,
        "to": last,
        "field": field,
        "scale": scale,
        "vector": (field, scale),
    })


target = next(
    w for w in windows
    if (
        w["from"] == TARGET_REGION[0]
        and
        w["to"] == TARGET_REGION[1]
    )
)

print()
print("=" * 72)
print(" TARGET WINDOW")
print("=" * 72)

print(
    f"L{target['from']:02d}-L{target['to']:02d}"
)

print(
    f"field={target['field']:+.6f} "
    f"scale={target['scale']:+.6f}"
)


# ------------------------------------------------------------
# Structurally match every other window.
# ------------------------------------------------------------

for w in windows:
    w["structural_distance"] = distance(
        target["vector"],
        w["vector"],
    )

matched = [
    w for w in windows
    if w is not target
]

matched.sort(
    key=lambda w: w["structural_distance"]
)


print()
print("=" * 72)
print(" CLOSEST STRUCTURAL MATCHES")
print("=" * 72)

for rank, w in enumerate(
    matched[:12],
    start=1,
):

    print(
        f"{rank:02d}. "
        f"L{w['from']:02d}-L{w['to']:02d} "
        f"distance={w['structural_distance']:.6f} "
        f"field={w['field']:+.6f} "
        f"scale={w['scale']:+.6f}"
    )


# ------------------------------------------------------------
# Calculate target effects for every window.
# ------------------------------------------------------------

for w in windows:

    items = window(w["start"])
    outside_items = outside(w["start"])

    w["targets"] = {}

    for component in TARGETS:

        w["targets"][component] = target_delta(
            items,
            outside_items,
            component,
        )


print()
print("=" * 72)
print(" TARGET EFFECTS")
print("=" * 72)

for w in sorted(
    windows,
    key=lambda x: x["start"],
):

    print(
        f"L{w['from']:02d}-L{w['to']:02d} | "
        f"v_bias={w['targets']['attn_v.bias']:+.6f} | "
        f"ffn_up={w['targets']['ffn_up.weight']:+.6f}"
    )


# ------------------------------------------------------------
# Structural-matched contrast.
# ------------------------------------------------------------

MATCH_COUNT = min(8, len(matched))

controls = matched[:MATCH_COUNT]

print()
print("=" * 72)
print(" STRUCTURALLY MATCHED CONTROL SET")
print("=" * 72)

for w in controls:

    print(
        f"L{w['from']:02d}-L{w['to']:02d} | "
        f"distance={w['structural_distance']:.6f}"
    )


control_effects = {}

for component in TARGETS:

    target_effect = target["targets"][component]

    control_values = [
        w["targets"][component]
        for w in controls
    ]

    control_mean = mean(control_values)

    contrast = (
        target_effect
        -
        control_mean
    )

    control_effects[component] = {
        "target_effect": target_effect,
        "control_mean": control_mean,
        "contrast": contrast,
        "control_values": control_values,
    }

    print(
        f"{component:<25} "
        f"target={target_effect:+.6f} "
        f"control={control_mean:+.6f} "
        f"contrast={contrast:+.6f}"
    )


# ------------------------------------------------------------
# Matched permutation test.
#
# Null: target window is exchangeable with its structurally
# matched controls.
# ------------------------------------------------------------

print()
print("=" * 72)
print(" MATCHED PERMUTATION TEST")
print("=" * 72)

permutation_results = {}

for component in TARGETS:

    observed = (
        target["targets"][component]
        -
        mean(
            w["targets"][component]
            for w in controls
        )
    )

    values = [
        target["targets"][component]
    ] + [
        w["targets"][component]
        for w in controls
    ]

    n_controls = len(controls)

    extreme = 0

    for _ in range(PERMUTATIONS):

        shuffled = values[:]
        rng.shuffle(shuffled)

        pseudo_target = shuffled[0]
        pseudo_controls = shuffled[1:]

        pseudo_contrast = (
            pseudo_target
            -
            mean(pseudo_controls)
        )

        if abs(pseudo_contrast) >= abs(observed):
            extreme += 1

    p = (
        extreme + 1
    ) / (
        PERMUTATIONS + 1
    )

    permutation_results[component] = {
        "observed_contrast": observed,
        "p": p,
        "control_count": n_controls,
    }

    print(
        f"{component:<25} "
        f"contrast={observed:+.6f} "
        f"p={p:.4f}"
    )


# ------------------------------------------------------------
# Directional result.
# ------------------------------------------------------------

target_negative = all(
    target["targets"][c] < 0
    for c in TARGETS
)

control_negative = all(
    control_effects[c]["control_mean"] < 0
    for c in TARGETS
)

if target_negative and not control_negative:
    interpretation = (
        "TARGET_NEGATIVE_BEYOND_STRUCTURAL_CONTROLS"
    )

elif target_negative and control_negative:
    interpretation = (
        "TARGET_NEGATIVE_BUT_SHARED_BY_CONTROLS"
    )

else:
    interpretation = (
        "NO_UNIQUE_NEGATIVE_TARGET_SIGNATURE"
    )


print()
print("=" * 72)
print(" INTERPRETATION")
print("=" * 72)

print(interpretation)


# ------------------------------------------------------------
# Rank target by target magnitude.
# ------------------------------------------------------------

for component in TARGETS:

    ranked = sorted(
        windows,
        key=lambda w:
            w["targets"][component],
    )

    rank = next(
        i + 1
        for i, w in enumerate(ranked)
        if w["start"] == target["start"]
    )

    print(
        f"{component:<25} "
        f"negative-rank={rank}/{len(ranked)}"
    )


result = {
    "format":
        "OpenMind Q8 Structural-Matched Target Test V14",

    "configuration": {
        "seed": SEED,
        "permutations": PERMUTATIONS,
        "window_size": WINDOW_SIZE,
        "match_count": MATCH_COUNT,
    },

    "target_region": {
        "from": target["from"],
        "to": target["to"],
        "field": target["field"],
        "scale": target["scale"],
    },

    "structural_matches": [
        {
            "from": w["from"],
            "to": w["to"],
            "distance": w["structural_distance"],
            "field": w["field"],
            "scale": w["scale"],
        }
        for w in controls
    ],

    "all_windows": [
        {
            "from": w["from"],
            "to": w["to"],
            "field": w["field"],
            "scale": w["scale"],
            "structural_distance":
                w["structural_distance"],
            "targets": w["targets"],
        }
        for w in windows
    ],

    "control_effects":
        control_effects,

    "permutation_results":
        permutation_results,

    "interpretation":
        interpretation,
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
print("Q8 STRUCTURAL-MATCHED TARGET TEST V14 COMPLETE")
