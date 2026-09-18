import json
import random
from pathlib import Path
from statistics import mean

V4 = Path("experiments/model_fractal/q8_parameter_field_v4.json")
OUT = Path("experiments/model_fractal/q8_target_specificity_v15.json")

SEED = 20260823
PERMUTATIONS = 5000

rng = random.Random(SEED)

v4 = json.loads(V4.read_text())

transitions = v4["transitions"]
components = v4["components"]

TARGETS = [
    "attn_v.bias",
    "ffn_up.weight",
]

# Pre-specified region from V12/V14.
REGION_FROM = 8
REGION_TO = 12

region = [
    t for t in transitions
    if REGION_FROM <= t["from"] and t["to"] <= REGION_TO
]

outside = [
    t for t in transitions
    if t not in region
]


def component_mean(items, component):
    return mean(
        t["components"][component]["value"]
        for t in items
    )


def component_delta(component):
    return (
        component_mean(region, component)
        - component_mean(outside, component)
    )


def permutation_p(component, trials=PERMUTATIONS):
    observed = abs(component_delta(component))

    values = [
        t["components"][component]["value"]
        for t in region + outside
    ]

    n = len(region)
    extreme = 0

    for _ in range(trials):
        shuffled = values[:]
        rng.shuffle(shuffled)

        a = shuffled[:n]
        b = shuffled[n:]

        d = abs(mean(a) - mean(b))

        if d >= observed:
            extreme += 1

    return (extreme + 1) / (trials + 1)


print("=" * 72)
print(" OPENMIND / Q8 TARGET SPECIFICITY V15")
print("=" * 72)

print()
print("Region: L08-L12")
print("Region transitions:", len(region))
print("Outside transitions:", len(outside))
print("Components:", len(components))
print("Targets:", TARGETS)
print("Permutations:", PERMUTATIONS)
print("Seed:", SEED)

print()
print("=" * 72)
print(" ALL-COMPONENT REGIONAL EFFECTS")
print("=" * 72)

effects = []

for component in components:
    d = component_delta(component)
    p = permutation_p(component)

    effects.append({
        "component": component,
        "delta": d,
        "absolute_delta": abs(d),
        "p": p,
        "target": component in TARGETS,
    })

effects.sort(
    key=lambda x: x["absolute_delta"],
    reverse=True,
)

for i, x in enumerate(effects, 1):
    marker = "*" if x["target"] else " "
    print(
        f"{marker}{i:02d}. "
        f"{x['component']:<25} "
        f"delta={x['delta']:+.6f} | "
        f"abs={x['absolute_delta']:.6f} | "
        f"p={x['p']:.4f}"
    )

print()
print("=" * 72)
print(" TARGET RANKING")
print("=" * 72)

for target in TARGETS:
    row = next(
        x for x in effects
        if x["component"] == target
    )

    rank = next(
        i + 1
        for i, x in enumerate(effects)
        if x["component"] == target
    )

    print(
        f"{target:<25} "
        f"absolute-effect-rank={rank}/{len(effects)} | "
        f"delta={row['delta']:+.6f}"
    )

print()
print("=" * 72)
print(" DIRECTIONAL COHERENCE")
print("=" * 72)

negative = [
    x for x in effects
    if x["delta"] < 0
]

positive = [
    x for x in effects
    if x["delta"] > 0
]

target_negative = sum(
    1 for x in effects
    if x["target"] and x["delta"] < 0
)

target_positive = sum(
    1 for x in effects
    if x["target"] and x["delta"] > 0
)

print("Negative components:", len(negative))
print("Positive components:", len(positive))
print(
    "Targets negative:",
    target_negative,
    "/",
    len(TARGETS),
)

print(
    "Targets positive:",
    target_positive,
    "/",
    len(TARGETS),
)

print()
print("=" * 72)
print(" NON-TARGET REGIONAL SHIFT")
print("=" * 72)

non_targets = [
    x for x in effects
    if not x["target"]
]

non_target_mean = mean(
    x["delta"]
    for x in non_targets
)

non_target_abs_mean = mean(
    x["absolute_delta"]
    for x in non_targets
)

target_mean = mean(
    x["delta"]
    for x in effects
    if x["target"]
)

target_abs_mean = mean(
    x["absolute_delta"]
    for x in effects
    if x["target"]
)

print(
    f"Target mean delta:       {target_mean:+.6f}"
)

print(
    f"Non-target mean delta:   {non_target_mean:+.6f}"
)

print(
    f"Target abs mean:         {target_abs_mean:.6f}"
)

print(
    f"Non-target abs mean:     {non_target_abs_mean:.6f}"
)

print()
print("=" * 72)
print(" TARGET-vs-NON-TARGET CONTRAST")
print("=" * 72)

observed_contrast = (
    target_abs_mean
    - non_target_abs_mean
)

print(
    f"Observed absolute-effect contrast: "
    f"{observed_contrast:+.6f}"
)

# Permute component labels while preserving the regional
# effect values. This asks whether the two named targets
# are unusually large effects among all components.

abs_values = [
    x["absolute_delta"]
    for x in effects
]

n_targets = len(TARGETS)

extreme = 0

for _ in range(PERMUTATIONS):

    shuffled = abs_values[:]
    rng.shuffle(shuffled)

    pseudo_target = mean(
        shuffled[:n_targets]
    )

    pseudo_other = mean(
        shuffled[n_targets:]
    )

    pseudo_contrast = (
        pseudo_target
        - pseudo_other
    )

    if abs(pseudo_contrast) >= abs(
        observed_contrast
    ):
        extreme += 1

specificity_p = (
    extreme + 1
) / (
    PERMUTATIONS + 1
)

print(
    f"Target-specificity p={specificity_p:.4f}"
)

print()
print("=" * 72)
print(" TARGET DIRECTIONAL TEST")
print("=" * 72)

target_direction_score = (
    sum(
        1
        for x in effects
        if x["target"] and x["delta"] < 0
    )
    / len(TARGETS)
)

non_target_negative_fraction = (
    len(negative)
    / len(non_targets)
)

print(
    f"Target negative fraction: "
    f"{target_direction_score:.3f}"
)

print(
    f"Non-target negative fraction: "
    f"{non_target_negative_fraction:.3f}"
)

print()
print("=" * 72)
print(" INTERPRETATION")
print("=" * 72)

if (
    specificity_p < 0.05
    and target_abs_mean > non_target_abs_mean
):
    interpretation = "TARGET_SPECIFIC_SIGNAL"
elif (
    non_target_abs_mean > 0.05
    and target_abs_mean > non_target_abs_mean
):
    interpretation = "TARGET_ENRICHED_WITH_BROAD_REGIONAL_SHIFT"
elif non_target_abs_mean > 0.05:
    interpretation = "BROAD_REGIONAL_SHIFT"
else:
    interpretation = "WEAK_REGIONAL_EFFECT"

print("Interpretation:", interpretation)

result = {
    "format":
        "OpenMind Q8 Target Specificity V15",

    "configuration": {
        "seed": SEED,
        "permutations": PERMUTATIONS,
        "region_from": REGION_FROM,
        "region_to": REGION_TO,
        "targets": TARGETS,
    },

    "region": [
        [t["from"], t["to"]]
        for t in region
    ],

    "outside_count":
        len(outside),

    "component_effects":
        effects,

    "target_mean_delta":
        target_mean,

    "non_target_mean_delta":
        non_target_mean,

    "target_absolute_mean":
        target_abs_mean,

    "non_target_absolute_mean":
        non_target_abs_mean,

    "absolute_effect_contrast":
        observed_contrast,

    "target_specificity_p":
        specificity_p,

    "target_negative_fraction":
        target_direction_score,

    "non_target_negative_fraction":
        non_target_negative_fraction,

    "interpretation":
        interpretation,
}

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
print("Q8 TARGET SPECIFICITY V15 COMPLETE")
