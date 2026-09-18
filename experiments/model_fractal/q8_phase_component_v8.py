import json
import math
from pathlib import Path

V4_PATH = Path(
    "experiments/model_fractal/q8_parameter_field_v4.json"
)

V5_PATH = Path(
    "experiments/model_fractal/q8_component_coherence_v5.json"
)

V6_PATH = Path(
    "experiments/model_fractal/q8_phase_detection_v6.json"
)

OUT = Path(
    "experiments/model_fractal/q8_phase_component_v8.json"
)


# ============================================================
# LOAD
# ============================================================

v4 = json.loads(V4_PATH.read_text())
v5 = json.loads(V5_PATH.read_text())
v6 = json.loads(V6_PATH.read_text())


# ============================================================
# PHASE DATA
# ============================================================

phase_scores = {
    x["layer"]: x
    for x in v6["phase_scores"]
}

candidate_layers = {
    x["layer"]
    for x in v6["phase_candidates"]
}


# ============================================================
# COMPONENT TRANSITIONS FROM V4
# ============================================================

transitions = {
    (x["from"], x["to"]): x
    for x in v4["transitions"]
}


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
# COMPONENT ANALYSIS
# ============================================================

component_results = []


for component in components:

    values = []
    phase_values = []
    phase_deltas = []

    candidate_values = []
    noncandidate_values = []

    candidate_deltas = []
    noncandidate_deltas = []

    for (a, b), transition in transitions.items():

        entry = transition["components"].get(component)

        if entry is None:
            continue

        value = float(entry["value"])

        left = phase_scores.get(a)
        right = phase_scores.get(b)

        if left is None or right is None:
            continue

        left_phase = float(left["local"])
        right_phase = float(right["local"])

        delta = right_phase - left_phase

        values.append(value)
        phase_values.append(
            (left_phase + right_phase) / 2.0
        )
        phase_deltas.append(delta)

        # A transition belongs to the candidate region
        # when either side touches a phase candidate.
        is_candidate = (
            a in candidate_layers
            or b in candidate_layers
        )

        if is_candidate:
            candidate_values.append(value)
            candidate_deltas.append(delta)
        else:
            noncandidate_values.append(value)
            noncandidate_deltas.append(delta)

    candidate_mean = (
        sum(candidate_values)
        / len(candidate_values)
        if candidate_values else 0.0
    )

    noncandidate_mean = (
        sum(noncandidate_values)
        / len(noncandidate_values)
        if noncandidate_values else 0.0
    )

    candidate_delta_mean = (
        sum(candidate_deltas)
        / len(candidate_deltas)
        if candidate_deltas else 0.0
    )

    noncandidate_delta_mean = (
        sum(noncandidate_deltas)
        / len(noncandidate_deltas)
        if noncandidate_deltas else 0.0
    )

    results = {
        "component": component,

        "transition_count": len(values),

        "phase_correlation":
            pearson(values, phase_values),

        "phase_delta_correlation":
            pearson(values, phase_deltas),

        "candidate_mean":
            candidate_mean,

        "noncandidate_mean":
            noncandidate_mean,

        "candidate_mean_difference":
            candidate_mean - noncandidate_mean,

        "candidate_delta_mean":
            candidate_delta_mean,

        "noncandidate_delta_mean":
            noncandidate_delta_mean,

        "candidate_delta_difference":
            candidate_delta_mean
            - noncandidate_delta_mean,
    }

    component_results.append(results)


# ============================================================
# RANKINGS
# ============================================================

by_phase_correlation = sorted(
    component_results,
    key=lambda x: abs(x["phase_correlation"]),
    reverse=True,
)

by_phase_delta = sorted(
    component_results,
    key=lambda x: abs(x["phase_delta_correlation"]),
    reverse=True,
)

by_candidate_difference = sorted(
    component_results,
    key=lambda x: abs(
        x["candidate_mean_difference"]
    ),
    reverse=True,
)


# ============================================================
# OUTPUT
# ============================================================

result = {
    "format":
        "OpenMind Q8 Phase Component Analysis V8",

    "sources": {
        "v4": str(V4_PATH),
        "v5": str(V5_PATH),
        "v6": str(V6_PATH),
    },

    "phase_candidates":
        sorted(candidate_layers),

    "components":
        components,

    "component_results":
        component_results,

    "rankings": {
        "phase_correlation":
            [
                x["component"]
                for x in by_phase_correlation
            ],

        "phase_delta_correlation":
            [
                x["component"]
                for x in by_phase_delta
            ],

        "candidate_difference":
            [
                x["component"]
                for x in by_candidate_difference
            ],
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
print(" OPENMIND / Q8 PHASE COMPONENT ANALYSIS V8")
print("=" * 72)

print()
print(
    "Phase candidates:",
    sorted(candidate_layers)
)

print()
print("=" * 72)
print(" COMPONENT / PHASE CORRELATION")
print("=" * 72)

for x in by_phase_correlation:

    print(
        f"{x['component']:<25} "
        f"phase={x['phase_correlation']:+.6f} | "
        f"delta={x['phase_delta_correlation']:+.6f}"
    )

print()
print("=" * 72)
print(" CANDIDATE VS NON-CANDIDATE")
print("=" * 72)

for x in by_candidate_difference:

    print(
        f"{x['component']:<25} "
        f"candidate={x['candidate_mean']:.6f} | "
        f"outside={x['noncandidate_mean']:.6f} | "
        f"delta={x['candidate_mean_difference']:+.6f}"
    )

print()
print("=" * 72)
print(" STRONGEST PHASE-ASSOCIATED COMPONENTS")
print("=" * 72)

for x in by_phase_correlation[:6]:

    print(
        f"{x['component']:<25} "
        f"r={x['phase_correlation']:+.6f}"
    )

print()
print("Output:", OUT)

print()
print("Q8 PHASE COMPONENT ANALYSIS V8 COMPLETE")
