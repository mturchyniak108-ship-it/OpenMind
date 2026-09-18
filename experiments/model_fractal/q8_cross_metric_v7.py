import json
import math
from pathlib import Path

V5_PATH = Path(
    "experiments/model_fractal/q8_component_coherence_v5.json"
)

V6_PATH = Path(
    "experiments/model_fractal/q8_phase_detection_v6.json"
)

OUT = Path(
    "experiments/model_fractal/q8_cross_metric_v7.json"
)


# ============================================================
# LOAD
# ============================================================

v5 = json.loads(V5_PATH.read_text())
v6 = json.loads(V6_PATH.read_text())


# ============================================================
# INDEX V5 TRANSITIONS
# ============================================================

v5_transitions = {
    (x["from"], x["to"]): x
    for x in v5["transitions"]
}


# ============================================================
# INDEX V6 TRANSITIONS
# ============================================================

v6_transitions = {
    (x["from"], x["to"]): x
    for x in v6["transition_scores"]
}


# ============================================================
# INDEX V6 PHASE SCORES
# ============================================================

phase_scores = {
    x["layer"]: x
    for x in v6["phase_scores"]
}


phase_candidates = {
    x["layer"]: x
    for x in v6["phase_candidates"]
}


# ============================================================
# CORRELATION
# ============================================================

def pearson(xs, ys):

    n = len(xs)

    if n < 2:
        return 0.0

    mx = sum(xs) / n
    my = sum(ys) / n

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
# CROSS-METRIC TRANSITIONS
# ============================================================

cross_transitions = []

coherences = []
means = []
maxima = []
phase_left = []
phase_right = []
phase_delta = []

for key in sorted(v5_transitions):

    if key not in v6_transitions:
        continue

    a, b = key

    t5 = v5_transitions[key]
    t6 = v6_transitions[key]

    coherence = float(t5["coherence"])
    mean_value = float(t5["mean"])
    maximum = float(t5["maximum"])

    left_phase = phase_scores.get(a)
    right_phase = phase_scores.get(b)

    if left_phase is None or right_phase is None:
        continue

    left_local = float(left_phase["local"])
    right_local = float(right_phase["local"])

    delta = right_local - left_local

    record = {
        "from": a,
        "to": b,
        "coherence": coherence,
        "mean_field": mean_value,
        "maximum_field": maximum,
        "strong_count": int(t5["strong_count"]),
        "left_phase": left_local,
        "right_phase": right_local,
        "phase_delta": delta,
        "phase_magnitude": abs(delta),
    }

    cross_transitions.append(record)

    coherences.append(coherence)
    means.append(mean_value)
    maxima.append(maximum)
    phase_left.append(left_local)
    phase_right.append(right_local)
    phase_delta.append(delta)


# ============================================================
# CROSS-METRIC CORRELATIONS
# ============================================================

correlation = {
    "coherence_vs_mean_field":
        pearson(coherences, means),

    "coherence_vs_maximum_field":
        pearson(coherences, maxima),

    "coherence_vs_phase_delta":
        pearson(coherences, phase_delta),

    "mean_field_vs_phase_delta":
        pearson(means, phase_delta),

    "maximum_field_vs_phase_delta":
        pearson(maxima, phase_delta),
}


# ============================================================
# PHASE / COHERENCE AGREEMENT
# ============================================================

candidate_layers = sorted(phase_candidates)

candidate_transition_pairs = []

for layer in candidate_layers:

    left = layer - 1
    right = layer

    if (left, right) in v5_transitions:

        t = v5_transitions[(left, right)]

        candidate_transition_pairs.append({
            "boundary_layer": layer,
            "from": left,
            "to": right,
            "phase_local": phase_candidates[layer]["local"],
            "coherence": t["coherence"],
            "mean_field": t["mean"],
            "maximum_field": t["maximum"],
            "strong_count": t["strong_count"],
        })


# ============================================================
# RANK CROSS-METRIC SIGNAL
# ============================================================

for record in cross_transitions:

    coherence = record["coherence"]
    phase_mag = record["phase_magnitude"]

    record["cross_score"] = (
        coherence * phase_mag
    )


cross_ranked = sorted(
    cross_transitions,
    key=lambda x: x["cross_score"],
    reverse=True,
)


# ============================================================
# SUMMARY
# ============================================================

cross_values = [
    x["cross_score"]
    for x in cross_transitions
]

summary = {
    "transition_count": len(cross_transitions),
    "candidate_count": len(candidate_layers),
    "mean_coherence": (
        sum(coherences) / len(coherences)
        if coherences else 0.0
    ),
    "mean_phase_delta": (
        sum(phase_delta) / len(phase_delta)
        if phase_delta else 0.0
    ),
    "mean_phase_magnitude": (
        sum(abs(x) for x in phase_delta)
        / len(phase_delta)
        if phase_delta else 0.0
    ),
    "mean_cross_score": (
        sum(cross_values) / len(cross_values)
        if cross_values else 0.0
    ),
}


# ============================================================
# OUTPUT
# ============================================================

result = {
    "format":
        "OpenMind Q8 Cross Metric Analysis V7",

    "sources": {
        "v5":
            str(V5_PATH),
        "v6":
            str(V6_PATH),
    },

    "metrics": {
        "coherence":
            "V5 transition coherence",

        "mean_field":
            "V5 transition mean",

        "maximum_field":
            "V5 transition maximum",

        "phase_local":
            "V6 local phase score",

        "phase_delta":
            "V6 right-local minus left-local",
    },

    "phase_candidates":
        candidate_layers,

    "candidate_transition_pairs":
        candidate_transition_pairs,

    "cross_transitions":
        cross_transitions,

    "cross_ranking":
        cross_ranked,

    "correlations":
        correlation,

    "summary":
        summary,
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
print(" OPENMIND / Q8 CROSS METRIC ANALYSIS V7")
print("=" * 72)

print()
print("V5 transitions:", len(v5_transitions))
print("V6 transitions:", len(v6_transitions))
print("Cross transitions:", len(cross_transitions))
print("Phase candidates:", len(candidate_layers))

print()
print("=" * 72)
print(" CROSS-METRIC TRANSITIONS")
print("=" * 72)

for x in cross_ranked:

    print(
        f"L{x['from']:02d} -> L{x['to']:02d} | "
        f"coherence={x['coherence']:.3f} | "
        f"phase_delta={x['phase_delta']:+.6f} | "
        f"cross={x['cross_score']:.6f}"
    )

print()
print("=" * 72)
print(" PHASE / COHERENCE CANDIDATES")
print("=" * 72)

for x in candidate_transition_pairs:

    print(
        f"L{x['boundary_layer']:02d} | "
        f"phase={x['phase_local']:.6f} | "
        f"coherence={x['coherence']:.3f} | "
        f"mean={x['mean_field']:.6f} | "
        f"max={x['maximum_field']:.6f}"
    )

print()
print("=" * 72)
print(" CORRELATIONS")
print("=" * 72)

for name, value in correlation.items():

    print(
        f"{name:<38} "
        f"{value:+.6f}"
    )

print()
print("=" * 72)
print(" SUMMARY")
print("=" * 72)

print(
    f"Mean coherence:       "
    f"{summary['mean_coherence']:.6f}"
)

print(
    f"Mean phase delta:      "
    f"{summary['mean_phase_delta']:+.6f}"
)

print(
    f"Mean phase magnitude:  "
    f"{summary['mean_phase_magnitude']:.6f}"
)

print(
    f"Mean cross score:      "
    f"{summary['mean_cross_score']:.6f}"
)

print()
print("Phase candidates:", candidate_layers)

print()
print("Output:", OUT)

print()
print("Q8 CROSS METRIC ANALYSIS V7 COMPLETE")
