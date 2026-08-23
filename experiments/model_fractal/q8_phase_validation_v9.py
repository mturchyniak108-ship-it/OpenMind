import json
import math
import random
from pathlib import Path

V4_PATH = Path(
    "experiments/model_fractal/q8_parameter_field_v4.json"
)

V6_PATH = Path(
    "experiments/model_fractal/q8_phase_detection_v6.json"
)

V8_PATH = Path(
    "experiments/model_fractal/q8_phase_component_v8.json"
)

OUT = Path(
    "experiments/model_fractal/q8_phase_validation_v9.json"
)

SEED = 20260823
PERMUTATIONS = 5000
BOOTSTRAPS = 3000


# ============================================================
# LOAD
# ============================================================

v4 = json.loads(V4_PATH.read_text())
v6 = json.loads(V6_PATH.read_text())
v8 = json.loads(V8_PATH.read_text())

random.seed(SEED)


# ============================================================
# PHASE DATA
# ============================================================

phase_scores = {
    x["layer"]: float(x["local"])
    for x in v6["phase_scores"]
}

candidate_layers = {
    x["layer"]
    for x in v6["phase_candidates"]
}


# ============================================================
# TRANSITION DATA
# ============================================================

transitions = sorted(
    v4["transitions"],
    key=lambda x: (x["from"], x["to"])
)

components = list(v4["components"])


# ============================================================
# PEARSON
# ============================================================

def pearson(xs, ys):

    if len(xs) < 2:
        return 0.0

    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)

    numerator = sum(
        (x - mx) * (y - my)
        for x, y in zip(xs, ys)
    )

    dx = math.sqrt(
        sum((x - mx) ** 2 for x in xs)
    )

    dy = math.sqrt(
        sum((y - my) ** 2 for y in ys)
    )

    if dx == 0.0 or dy == 0.0:
        return 0.0

    return numerator / (dx * dy)


# ============================================================
# BUILD OBSERVATIONS
# ============================================================

observations = []

for transition in transitions:

    a = transition["from"]
    b = transition["to"]

    if a not in phase_scores or b not in phase_scores:
        continue

    phase = (
        phase_scores[a]
        + phase_scores[b]
    ) / 2.0

    candidate = (
        a in candidate_layers
        or b in candidate_layers
    )

    observations.append({
        "from": a,
        "to": b,
        "phase": phase,
        "candidate": candidate,
        "components": {
            c: float(
                transition["components"][c]["value"]
            )
            for c in components
        },
    })


# ============================================================
# COMPONENT STATISTICS
# ============================================================

def component_stats(component):

    values = [
        x["components"][component]
        for x in observations
    ]

    phases = [
        x["phase"]
        for x in observations
    ]

    candidate_values = [
        x["components"][component]
        for x in observations
        if x["candidate"]
    ]

    outside_values = [
        x["components"][component]
        for x in observations
        if not x["candidate"]
    ]

    candidate_mean = (
        sum(candidate_values)
        / len(candidate_values)
    )

    outside_mean = (
        sum(outside_values)
        / len(outside_values)
    )

    return {
        "phase_correlation":
            pearson(values, phases),

        "candidate_mean":
            candidate_mean,

        "outside_mean":
            outside_mean,

        "candidate_difference":
            candidate_mean - outside_mean,

        "sample_count":
            len(values),

        "candidate_count":
            len(candidate_values),

        "outside_count":
            len(outside_values),
    }


observed = {
    c: component_stats(c)
    for c in components
}


# ============================================================
# PERMUTATION TEST
#
# Keep the observed phase values fixed but randomly permute
# component values across transitions.
# ============================================================

null_correlations = {
    c: []
    for c in components
}

null_differences = {
    c: []
    for c in components
}


for _ in range(PERMUTATIONS):

    indices = list(range(len(observations)))
    random.shuffle(indices)

    for component in components:

        values = [
            observations[i]["components"][component]
            for i in indices
        ]

        phases = [
            x["phase"]
            for x in observations
        ]

        corr = pearson(
            values,
            phases
        )

        null_correlations[component].append(
            corr
        )

        candidate_values = [
            observations[i]["components"][component]
            for i in range(len(observations))
            if observations[i]["candidate"]
        ]

        outside_values = [
            observations[i]["components"][component]
            for i in range(len(observations))
            if not observations[i]["candidate"]
        ]

        difference = (
            sum(candidate_values)
            / len(candidate_values)
            -
            sum(outside_values)
            / len(outside_values)
        )

        null_differences[component].append(
            difference
        )


# ============================================================
# EMPIRICAL P-VALUE
# ============================================================

def permutation_pvalue(
    observed_value,
    null_values
):

    extreme = sum(
        abs(x) >= abs(observed_value)
        for x in null_values
    )

    return (
        extreme + 1
    ) / (
        len(null_values) + 1
    )


# ============================================================
# BOOTSTRAP CONFIDENCE INTERVAL
# ============================================================

def bootstrap_correlation(component):

    values = [
        x["components"][component]
        for x in observations
    ]

    phases = [
        x["phase"]
        for x in observations
    ]

    n = len(values)
    results = []

    for _ in range(BOOTSTRAPS):

        indices = [
            random.randrange(n)
            for _ in range(n)
        ]

        bx = [
            values[i]
            for i in indices
        ]

        by = [
            phases[i]
            for i in indices
        ]

        results.append(
            pearson(bx, by)
        )

    results.sort()

    low = results[
        int(0.025 * len(results))
    ]

    high = results[
        int(0.975 * len(results))
    ]

    return low, high


# ============================================================
# FINAL COMPONENT RESULTS
# ============================================================

results = {}

for component in components:

    low, high = bootstrap_correlation(
        component
    )

    results[component] = {
        **observed[component],

        "phase_correlation_p":
            permutation_pvalue(
                observed[component][
                    "phase_correlation"
                ],
                null_correlations[component],
            ),

        "candidate_difference_p":
            permutation_pvalue(
                observed[component][
                    "candidate_difference"
                ],
                null_differences[component],
            ),

        "bootstrap_phase_low":
            low,

        "bootstrap_phase_high":
            high,
    }


# ============================================================
# RANKINGS
# ============================================================

correlation_ranking = sorted(
    components,
    key=lambda c:
        abs(
            results[c]["phase_correlation"]
        ),
    reverse=True,
)

difference_ranking = sorted(
    components,
    key=lambda c:
        abs(
            results[c]["candidate_difference"]
        ),
    reverse=True,
)


# ============================================================
# OUTPUT
# ============================================================

result = {
    "format":
        "OpenMind Q8 Phase Validation V9",

    "seed": SEED,

    "permutations":
        PERMUTATIONS,

    "bootstraps":
        BOOTSTRAPS,

    "phase_candidates":
        sorted(candidate_layers),

    "observation_count":
        len(observations),

    "components":
        components,

    "results":
        results,

    "rankings": {
        "phase_correlation":
            correlation_ranking,

        "candidate_difference":
            difference_ranking,
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


# ============================================================
# REPORT
# ============================================================

print("=" * 72)
print(" OPENMIND / Q8 PHASE VALIDATION V9")
print("=" * 72)

print()
print("Observations:", len(observations))
print("Components:", len(components))
print("Permutations:", PERMUTATIONS)
print("Bootstraps:", BOOTSTRAPS)
print("Seed:", SEED)

print()
print("=" * 72)
print(" COMPONENT VALIDATION")
print("=" * 72)

for component in correlation_ranking:

    x = results[component]

    print(
        f"{component:<25} "
        f"r={x['phase_correlation']:+.6f} | "
        f"p={x['phase_correlation_p']:.4f} | "
        f"CI=["
        f"{x['bootstrap_phase_low']:+.4f},"
        f"{x['bootstrap_phase_high']:+.4f}"
        f"] | "
        f"candidate_delta="
        f"{x['candidate_difference']:+.6f}"
    )

print()
print("=" * 72)
print(" CANDIDATE DIFFERENCE VALIDATION")
print("=" * 72)

for component in difference_ranking:

    x = results[component]

    print(
        f"{component:<25} "
        f"delta={x['candidate_difference']:+.6f} | "
        f"p={x['candidate_difference_p']:.4f}"
    )

print()
print("=" * 72)
print(" STRONGEST VALIDATED SIGNALS")
print("=" * 72)

for component in correlation_ranking[:6]:

    x = results[component]

    print(
        f"{component:<25} "
        f"r={x['phase_correlation']:+.6f} | "
        f"p={x['phase_correlation_p']:.4f}"
    )

print()
print("Output:", OUT)

print()
print("Q8 PHASE VALIDATION V9 COMPLETE")
