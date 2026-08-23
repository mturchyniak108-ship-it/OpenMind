import json
import math
import random
from pathlib import Path
from statistics import mean, stdev

V4 = Path("experiments/model_fractal/q8_parameter_field_v4.json")
V6 = Path("experiments/model_fractal/q8_phase_detection_v6.json")
V8 = Path("experiments/model_fractal/q8_phase_component_v8.json")
OUT = Path("experiments/model_fractal/q8_phase_region_validation_v10.json")

SEED = 20260823
PERMUTATIONS = 5000
BOOTSTRAPS = 3000

v4 = json.loads(V4.read_text())
v6 = json.loads(V6.read_text())
v8 = json.loads(V8.read_text())

transitions = v4["transitions"]
phase_scores = v6["phase_scores"]
phase_candidates = {
    x["layer"]
    for x in v6["phase_candidates"]
}

components = v4["components"]

# ------------------------------------------------------------
# PHASE SCORE MAP
# ------------------------------------------------------------

phase_map = {
    x["layer"]: x["local"]
    for x in phase_scores
}

# ------------------------------------------------------------
# TRANSITION RECORDS
# ------------------------------------------------------------

records = []

for t in transitions:
    a = t["from"]
    b = t["to"]

    # A transition is associated with the phase state of its
    # destination/interior layer.
    phase_layer = b

    if phase_layer not in phase_map:
        continue

    records.append({
        "from": a,
        "to": b,
        "phase_layer": phase_layer,
        "phase": phase_map[phase_layer],
        "is_candidate": phase_layer in phase_candidates,

        # Actual V4 field names.
        "mean_field": t["value_divergence"],
        "scale_field": t["scale_divergence"],

        "components": {
            c: {
                "value": t["components"][c]["value"],
                "scale": t["components"][c]["scale"],
            }
            for c in components
        },
    })

# ------------------------------------------------------------
# BASIC STATISTICS
# ------------------------------------------------------------

candidate_records = [
    r for r in records
    if r["is_candidate"]
]

outside_records = [
    r for r in records
    if not r["is_candidate"]
]

def avg(rows, key):
    if not rows:
        return 0.0
    return sum(r[key] for r in rows) / len(rows)

candidate_mean = avg(candidate_records, "mean_field")
outside_mean = avg(outside_records, "mean_field")

candidate_scale = avg(candidate_records, "scale_field")
outside_scale = avg(outside_records, "scale_field")

# ------------------------------------------------------------
# COMPONENT REGION DIFFERENCES
# ------------------------------------------------------------

component_stats = {}

for component in components:

    candidate_values = [
        r["components"][component]["value"]
        for r in candidate_records
    ]

    outside_values = [
        r["components"][component]["value"]
        for r in outside_records
    ]

    if not candidate_values or not outside_values:
        continue

    cmean = mean(candidate_values)
    omean = mean(outside_values)

    component_stats[component] = {
        "candidate_mean": cmean,
        "outside_mean": omean,
        "delta": cmean - omean,
        "candidate_n": len(candidate_values),
        "outside_n": len(outside_values),
    }

# ------------------------------------------------------------
# PERMUTATION TEST
# ------------------------------------------------------------

rng = random.Random(SEED)

def permutation_pvalue(candidate_values, outside_values):

    observed = (
        mean(candidate_values)
        - mean(outside_values)
    )

    combined = candidate_values + outside_values
    n_candidate = len(candidate_values)

    extreme = 0

    for _ in range(PERMUTATIONS):

        shuffled = combined[:]
        rng.shuffle(shuffled)

        a = shuffled[:n_candidate]
        b = shuffled[n_candidate:]

        diff = mean(a) - mean(b)

        if abs(diff) >= abs(observed):
            extreme += 1

    return (extreme + 1) / (PERMUTATIONS + 1)

# ------------------------------------------------------------
# BOOTSTRAP CONFIDENCE INTERVAL
# ------------------------------------------------------------

def bootstrap_ci(candidate_values, outside_values):

    observed = (
        mean(candidate_values)
        - mean(outside_values)
    )

    diffs = []

    for _ in range(BOOTSTRAPS):

        a = [
            candidate_values[
                rng.randrange(len(candidate_values))
            ]
            for _ in candidate_values
        ]

        b = [
            outside_values[
                rng.randrange(len(outside_values))
            ]
            for _ in outside_values
        ]

        diffs.append(mean(a) - mean(b))

    diffs.sort()

    low = diffs[
        max(0, int(0.025 * len(diffs)))
    ]

    high = diffs[
        min(len(diffs) - 1, int(0.975 * len(diffs)))
    ]

    return low, high, observed

# ------------------------------------------------------------
# VALIDATE COMPONENT REGION DIFFERENCES
# ------------------------------------------------------------

for component in component_stats:

    candidate_values = [
        r["components"][component]["value"]
        for r in candidate_records
    ]

    outside_values = [
        r["components"][component]["value"]
        for r in outside_records
    ]

    p = permutation_pvalue(
        candidate_values,
        outside_values
    )

    low, high, observed = bootstrap_ci(
        candidate_values,
        outside_values
    )

    component_stats[component].update({
        "p": p,
        "ci_low": low,
        "ci_high": high,
        "significant_005": p < 0.05,
        "ci_excludes_zero": (
            low > 0.0 or high < 0.0
        ),
    })

# ------------------------------------------------------------
# TRANSITION-LEVEL REGION SUMMARY
# ------------------------------------------------------------

region_transitions = []

for r in records:

    region_transitions.append({
        "from": r["from"],
        "to": r["to"],
        "phase_layer": r["phase_layer"],
        "phase": r["phase"],
        "candidate": r["is_candidate"],
        "mean_field": r["mean_field"],
        "scale_field": r["scale_field"],
    })

# ------------------------------------------------------------
# OUTPUT
# ------------------------------------------------------------

ranked_components = sorted(
    component_stats.items(),
    key=lambda x: abs(x[1]["delta"]),
    reverse=True,
)

result = {
    "format": "OpenMind Q8 Phase Region Validation V10",

    "source": {
        "v4": str(V4),
        "v6": str(V6),
        "v8": str(V8),
    },

    "configuration": {
        "seed": SEED,
        "permutations": PERMUTATIONS,
        "bootstraps": BOOTSTRAPS,
    },

    "regions": {
        "candidate_layers": sorted(phase_candidates),
        "candidate_transition_count": len(candidate_records),
        "outside_transition_count": len(outside_records),
    },

    "field_validation": {
        "candidate_mean": candidate_mean,
        "outside_mean": outside_mean,
        "delta": candidate_mean - outside_mean,
        "candidate_scale": candidate_scale,
        "outside_scale": outside_scale,
        "scale_delta": candidate_scale - outside_scale,
    },

    "component_validation": component_stats,

    "rankings": {
        "component_abs_delta": [
            {
                "component": component,
                **stats,
            }
            for component, stats in ranked_components
        ]
    },

    "transitions": region_transitions,

    "summary": {
        "candidate_layers": sorted(phase_candidates),
        "candidate_transitions": len(candidate_records),
        "outside_transitions": len(outside_records),
        "mean_field_delta":
            candidate_mean - outside_mean,
        "scale_field_delta":
            candidate_scale - outside_scale,
        "validated_components": sum(
            1
            for x in component_stats.values()
            if x["ci_excludes_zero"]
        ),
        "p005_components": sum(
            1
            for x in component_stats.values()
            if x["significant_005"]
        ),
    },
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

# ------------------------------------------------------------
# REPORT
# ------------------------------------------------------------

print("=" * 72)
print(" OPENMIND / Q8 PHASE REGION VALIDATION V10")
print("=" * 72)

print()
print("Candidate layers:", sorted(phase_candidates))
print("Candidate transitions:", len(candidate_records))
print("Outside transitions:", len(outside_records))
print()

print("=" * 72)
print(" FIELD REGION COMPARISON")
print("=" * 72)

print(
    f"Candidate mean field: "
    f"{candidate_mean:.6f}"
)

print(
    f"Outside mean field:   "
    f"{outside_mean:.6f}"
)

print(
    f"Mean-field delta:     "
    f"{candidate_mean - outside_mean:+.6f}"
)

print()

print(
    f"Candidate scale:      "
    f"{candidate_scale:.6f}"
)

print(
    f"Outside scale:        "
    f"{outside_scale:.6f}"
)

print(
    f"Scale delta:          "
    f"{candidate_scale - outside_scale:+.6f}"
)

print()
print("=" * 72)
print(" COMPONENT REGION VALIDATION")
print("=" * 72)

for component, stats in ranked_components:

    print(
        f"{component:<25} "
        f"delta={stats['delta']:+.6f} | "
        f"p={stats['p']:.4f} | "
        f"CI=["
        f"{stats['ci_low']:+.4f},"
        f"{stats['ci_high']:+.4f}"
        f"]"
    )

print()
print("=" * 72)
print(" SUMMARY")
print("=" * 72)

print(
    "CI-supported components:",
    sum(
        1
        for x in component_stats.values()
        if x["ci_excludes_zero"]
    )
)

print(
    "p < 0.05 components:",
    sum(
        1
        for x in component_stats.values()
        if x["significant_005"]
    )
)

print()
print("Output:", OUT)
print()
print("Q8 PHASE REGION VALIDATION V10 COMPLETE")
