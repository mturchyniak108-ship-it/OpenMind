import json
import math
import random
from pathlib import Path
from statistics import mean, median

V4 = Path("experiments/model_fractal/q8_parameter_field_v4.json")
V6 = Path("experiments/model_fractal/q8_phase_detection_v6.json")
V10 = Path("experiments/model_fractal/q8_phase_region_validation_v10.json")
OUT = Path("experiments/model_fractal/q8_phase_stability_v11.json")

SEED = 20260823
rng = random.Random(SEED)

v4 = json.loads(V4.read_text())
v6 = json.loads(V6.read_text())
v10 = json.loads(V10.read_text())

transitions = v4["transitions"]

candidate_layers = set(v10["regions"]["candidate_layers"])

candidate = [
    t for t in transitions
    if t["to"] in candidate_layers
]

outside = [
    t for t in transitions
    if t["to"] not in candidate_layers
]

components = v4["components"]


def component_value(t, component):
    return t["components"][component]["value"]


def group_mean(items, component):
    return mean(
        component_value(t, component)
        for t in items
    )


def delta(candidate_items, outside_items, component):
    return (
        group_mean(candidate_items, component)
        - group_mean(outside_items, component)
    )


def permutation_p(candidate_items, outside_items, component, trials=5000):
    observed = abs(
        delta(candidate_items, outside_items, component)
    )

    values = [
        component_value(t, component)
        for t in candidate_items + outside_items
    ]

    n_candidate = len(candidate_items)

    extreme = 0

    for _ in range(trials):
        shuffled = values[:]
        rng.shuffle(shuffled)

        a = shuffled[:n_candidate]
        b = shuffled[n_candidate:]

        d = abs(mean(a) - mean(b))

        if d >= observed:
            extreme += 1

    return (extreme + 1) / (trials + 1)


print("=" * 72)
print(" OPENMIND / Q8 PHASE STABILITY V11")
print("=" * 72)

print()
print("Candidate transitions:", len(candidate))
print("Outside transitions:", len(outside))
print("Components:", len(components))

print()
print("=" * 72)
print(" BASELINE SIGNALS")
print("=" * 72)

baseline = {}

for component in components:

    d = delta(candidate, outside, component)
    p = permutation_p(
        candidate,
        outside,
        component
    )

    baseline[component] = {
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
print(" LEAVE-ONE-CANDIDATE-OUT")
print("=" * 72)

loo_results = []

for removed in candidate:

    reduced = [
        t for t in candidate
        if t is not removed
    ]

    print()
    print(
        f"REMOVE L{removed['from']:02d} -> "
        f"L{removed['to']:02d}"
    )

    for component in components:

        d = delta(
            reduced,
            outside,
            component
        )

        loo_results.append({
            "removed_from": removed["from"],
            "removed_to": removed["to"],
            "component": component,
            "delta": d,
        })

        if component in (
            "attn_v.bias",
            "ffn_up.weight",
        ):
            print(
                f"  {component:<23} "
                f"delta={d:+.6f}"
            )

print()
print("=" * 72)
print(" TARGET SIGNAL STABILITY")
print("=" * 72)

targets = [
    "attn_v.bias",
    "ffn_up.weight",
]

stability = {}

for component in targets:

    baseline_delta = baseline[component]["delta"]

    values = [
        x["delta"]
        for x in loo_results
        if x["component"] == component
    ]

    same_sign = sum(
        1
        for x in values
        if (
            x < 0
            and baseline_delta < 0
        ) or (
            x > 0
            and baseline_delta > 0
        )
    )

    max_abs_change = max(
        abs(x - baseline_delta)
        for x in values
    )

    stability[component] = {
        "baseline_delta": baseline_delta,
        "leave_one_out": values,
        "same_sign_count": same_sign,
        "total": len(values),
        "sign_stability": (
            same_sign / len(values)
            if values else 0.0
        ),
        "max_absolute_change": max_abs_change,
    }

    print(
        f"{component:<25} "
        f"sign_stability="
        f"{same_sign}/{len(values)} "
        f"({same_sign/len(values):.3f})"
    )

    print(
        f"{'':25} "
        f"max_delta_change="
        f"{max_abs_change:.6f}"
    )

print()
print("=" * 72)
print(" REGION STRUCTURE")
print("=" * 72)

candidate_pairs = [
    [t["from"], t["to"]]
    for t in candidate
]

print("Candidate transitions:", candidate_pairs)

print()
print("=" * 72)
print(" INTERPRETATION FLAGS")
print("=" * 72)

for component in targets:

    s = stability[component]

    if s["sign_stability"] == 1.0:
        status = "STABLE"
    elif s["sign_stability"] >= 0.8:
        status = "MOSTLY_STABLE"
    else:
        status = "FRAGILE"

    print(
        f"{component:<25} {status}"
    )

result = {
    "format": "OpenMind Q8 Phase Stability V11",
    "seed": SEED,
    "candidate_layers": sorted(candidate_layers),
    "candidate_transition_count": len(candidate),
    "outside_transition_count": len(outside),
    "components": components,
    "baseline": baseline,
    "leave_one_out": loo_results,
    "target_stability": stability,
    "candidate_transitions": candidate_pairs,
}

OUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

OUT.write_text(
    json.dumps(
        result,
        indent=2,
        sort_keys=True
    )
)

print()
print("Output:", OUT)
print()
print("Q8 PHASE STABILITY V11 COMPLETE")
