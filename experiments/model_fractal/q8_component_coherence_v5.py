import json
import math
from pathlib import Path


# ============================================================
# CONFIG
# ============================================================

PATH = Path(
    "experiments/model_fractal/"
    "q8_parameter_field_v4.json"
)

OUT = Path(
    "experiments/model_fractal/"
    "q8_component_coherence_v5.json"
)

THRESHOLD = 0.75


# ============================================================
# LOAD
# ============================================================

data = json.loads(
    PATH.read_text()
)

transitions = data["transitions"]
components = data["components"]


# ============================================================
# STATISTICS
# ============================================================

def mean(values):

    if not values:
        return 0.0

    return sum(values) / len(values)


def median(values):

    if not values:
        return 0.0

    values = sorted(values)
    n = len(values)

    middle = n // 2

    if n % 2:
        return values[middle]

    return (
        values[middle - 1]
        + values[middle]
    ) / 2.0


def stddev(values):

    if not values:
        return 0.0

    m = mean(values)

    return math.sqrt(
        sum(
            (x - m) ** 2
            for x in values
        ) / len(values)
    )


# ============================================================
# COHERENCE ANALYSIS
# ============================================================

results = []

for transition in transitions:

    a = transition["from"]
    b = transition["to"]

    component_map = (
        transition["components"]
    )

    values = []

    component_values = {}

    for component in components:

        entry = component_map.get(
            component
        )

        if entry is None:
            continue

        value = float(
            entry["value"]
        )

        values.append(value)

        component_values[component] = {
            "value": value,
            "scale": float(
                entry["scale"]
            ),
            "strong": (
                value >= THRESHOLD
            ),
        }

    if not values:
        continue

    strong_components = [
        component
        for component, entry
        in component_values.items()
        if entry["strong"]
    ]

    coherence = (
        len(strong_components)
        / len(values)
    )

    results.append({
        "from": a,
        "to": b,
        "component_count": len(values),
        "mean": mean(values),
        "median": median(values),
        "std": stddev(values),
        "minimum": min(values),
        "maximum": max(values),
        "threshold": THRESHOLD,
        "strong_count": len(
            strong_components
        ),
        "coherence": coherence,
        "strong_components": (
            strong_components
        ),
        "components": component_values,
    })


# ============================================================
# RANKINGS
# ============================================================

by_coherence = sorted(
    results,
    key=lambda x: (
        x["coherence"],
        x["mean"],
    ),
    reverse=True,
)

by_mean = sorted(
    results,
    key=lambda x: x["mean"],
    reverse=True,
)

by_max = sorted(
    results,
    key=lambda x: x["maximum"],
    reverse=True,
)


# ============================================================
# COMPONENT PARTICIPATION
# ============================================================

participation = {}

for component in components:

    strong_transitions = []

    for result in results:

        entry = result[
            "components"
        ].get(component)

        if entry and entry["strong"]:

            strong_transitions.append({
                "from": result["from"],
                "to": result["to"],
                "value": entry["value"],
                "scale": entry["scale"],
            })

    participation[component] = {
        "strong_transition_count": len(
            strong_transitions
        ),
        "fraction": (
            len(strong_transitions)
            / len(results)
            if results
            else 0.0
        ),
        "transitions": strong_transitions,
    }


# ============================================================
# GLOBAL SUMMARY
# ============================================================

coherence_values = [
    x["coherence"]
    for x in results
]

mean_values = [
    x["mean"]
    for x in results
]


# ============================================================
# OUTPUT
# ============================================================

output = {
    "format": (
        "OpenMind Q8 Component "
        "Coherence V5"
    ),
    "source": str(PATH),
    "threshold": THRESHOLD,
    "component_count": len(components),
    "transition_count": len(results),
    "components": components,
    "transitions": results,
    "rankings": {
        "coherence": [
            {
                "from": x["from"],
                "to": x["to"],
                "coherence": x["coherence"],
                "mean": x["mean"],
                "strong_count": x[
                    "strong_count"
                ],
            }
            for x in by_coherence
        ],
        "mean": [
            {
                "from": x["from"],
                "to": x["to"],
                "mean": x["mean"],
                "coherence": x["coherence"],
            }
            for x in by_mean
        ],
        "maximum": [
            {
                "from": x["from"],
                "to": x["to"],
                "maximum": x["maximum"],
                "coherence": x["coherence"],
            }
            for x in by_max
        ],
    },
    "component_participation": participation,
    "summary": {
        "minimum_coherence": (
            min(coherence_values)
            if coherence_values
            else 0.0
        ),
        "maximum_coherence": (
            max(coherence_values)
            if coherence_values
            else 0.0
        ),
        "mean_coherence": (
            mean(coherence_values)
            if coherence_values
            else 0.0
        ),
        "mean_transition_value": (
            mean(mean_values)
            if mean_values
            else 0.0
        ),
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
    " OPENMIND / Q8 COMPONENT "
    "COHERENCE V5"
)
print("=" * 72)

print()
print("Source:", PATH)
print("Components:", len(components))
print("Transitions:", len(results))
print("Threshold:", THRESHOLD)

print()
print("=" * 72)
print(" TRANSITION COHERENCE")
print("=" * 72)

for result in by_coherence:

    print(
        f"L{result['from']:02d} -> "
        f"L{result['to']:02d} | "
        f"coherence="
        f"{result['coherence']:.3f} | "
        f"strong="
        f"{result['strong_count']:02d}/"
        f"{result['component_count']:02d} | "
        f"mean="
        f"{result['mean']:.6f} | "
        f"median="
        f"{result['median']:.6f} | "
        f"std="
        f"{result['std']:.6f} | "
        f"max="
        f"{result['maximum']:.6f}"
    )

print()
print("=" * 72)
print(" TOP COHERENT TRANSITIONS")
print("=" * 72)

for result in by_coherence[:10]:

    print()
    print(
        f"L{result['from']:02d} -> "
        f"L{result['to']:02d}"
    )

    print(
        f"coherence: "
        f"{result['coherence']:.3f}"
    )

    print(
        "strong components:"
    )

    for component in (
        result["strong_components"]
    ):
        entry = result[
            "components"
        ][component]

        print(
            f"  {component:<25} "
            f"value={entry['value']:.6f} "
            f"scale={entry['scale']:.6f}"
        )


print()
print("=" * 72)
print(" COMPONENT PARTICIPATION")
print("=" * 72)

for component, info in sorted(
    participation.items(),
    key=lambda item: (
        item[1][
            "strong_transition_count"
        ],
        item[0],
    ),
    reverse=True,
):

    print(
        f"{component:<25} "
        f"{info['strong_transition_count']:02d}/"
        f"{len(results):02d} "
        f"({info['fraction']:.3f})"
    )


print()
print("=" * 72)
print(" SUMMARY")
print("=" * 72)

summary = output["summary"]

print(
    f"Minimum coherence: "
    f"{summary['minimum_coherence']:.6f}"
)

print(
    f"Maximum coherence: "
    f"{summary['maximum_coherence']:.6f}"
)

print(
    f"Mean coherence:    "
    f"{summary['mean_coherence']:.6f}"
)

print(
    f"Mean field value:  "
    f"{summary['mean_transition_value']:.6f}"
)

print()
print("Output:", OUT)
print()
print(
    "Q8 COMPONENT COHERENCE V5 COMPLETE"
)
