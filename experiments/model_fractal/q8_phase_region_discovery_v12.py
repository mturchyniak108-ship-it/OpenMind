import json
import math
import random
from pathlib import Path
from statistics import mean

V4 = Path("experiments/model_fractal/q8_parameter_field_v4.json")
OUT = Path("experiments/model_fractal/q8_phase_region_discovery_v12.json")

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

WINDOW_SIZES = [3, 4, 5, 6]


def value(t, component):
    return t["components"][component]["value"]


def scale(t, component):
    return t["components"][component]["scale"]


def mean_field(items):
    return mean(
        t["value_divergence"]
        for t in items
    )


def scale_field(items):
    return mean(
        t["scale_divergence"]
        for t in items
    )


def component_mean(items, component):
    return mean(
        value(t, component)
        for t in items
    )


def component_delta(window, outside, component):
    return (
        component_mean(window, component)
        - component_mean(outside, component)
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
        value(t, component)
        for t in window + outside
    ]

    n_window = len(window)

    extreme = 0

    for _ in range(PERMUTATIONS):

        shuffled = values[:]
        rng.shuffle(shuffled)

        a = shuffled[:n_window]
        b = shuffled[n_window:]

        d = abs(mean(a) - mean(b))

        if d >= observed:
            extreme += 1

    return (
        extreme + 1
    ) / (
        PERMUTATIONS + 1
    )


def rank_desc(rows, key):
    ordered = sorted(
        rows,
        key=lambda x: abs(x[key]),
        reverse=True,
    )

    ranks = {}

    for rank, row in enumerate(
        ordered,
        start=1,
    ):
        ranks[row["window_id"]] = rank

    return ranks


print("=" * 72)
print(" OPENMIND / Q8 PHASE REGION DISCOVERY V12")
print("=" * 72)

print()
print("Transitions:", len(transitions))
print("Components:", len(components))
print("Window sizes:", WINDOW_SIZES)
print("Permutations:", PERMUTATIONS)
print("Seed:", SEED)

results = []

for window_size in WINDOW_SIZES:

    for start in range(
        0,
        len(transitions) - window_size + 1,
    ):

        end = start + window_size

        window = transitions[start:end]

        outside = (
            transitions[:start]
            + transitions[end:]
        )

        if not outside:
            continue

        first_from = window[0]["from"]
        last_to = window[-1]["to"]

        window_id = (
            f"L{first_from:02d}-L{last_to:02d}"
        )

        mf = mean_field(window)
        of = mean_field(outside)

        sf = scale_field(window)
        os = scale_field(outside)

        field_delta = mf - of
        scale_delta = sf - os

        row = {
            "window_id": window_id,
            "window_size": window_size,
            "start_index": start,
            "end_index": end - 1,
            "from": first_from,
            "to": last_to,
            "mean_field": mf,
            "outside_mean_field": of,
            "mean_field_delta": field_delta,
            "scale_field": sf,
            "outside_scale_field": os,
            "scale_field_delta": scale_delta,
            "components": {},
        }

        for component in TARGETS:

            d = component_delta(
                window,
                outside,
                component,
            )

            p = permutation_p(
                window,
                outside,
                component,
            )

            row["components"][component] = {
                "delta": d,
                "p": p,
                "window_mean":
                    component_mean(
                        window,
                        component,
                    ),
                "outside_mean":
                    component_mean(
                        outside,
                        component,
                    ),
            }

        results.append(row)


# ------------------------------------------------------------
# Rank windows independently by the major signals.
# ------------------------------------------------------------

field_rows = results[:]

field_rank = rank_desc(
    field_rows,
    "mean_field_delta",
)

scale_rank = rank_desc(
    field_rows,
    "scale_field_delta",
)

attn_rank = rank_desc(
    [
        {
            "window_id": r["window_id"],
            "score":
                r["components"]["attn_v.bias"]["delta"],
        }
        for r in results
    ],
    "score",
)

ffn_rank = rank_desc(
    [
        {
            "window_id": r["window_id"],
            "score":
                r["components"]["ffn_up.weight"]["delta"],
        }
        for r in results
    ],
    "score",
)


# ------------------------------------------------------------
# Directional ranking:
# We are specifically interested in reductions in the two
# V11 target components.
# ------------------------------------------------------------

for row in results:

    wid = row["window_id"]

    row["rankings"] = {
        "field_abs":
            field_rank[wid],
        "scale_abs":
            scale_rank[wid],
        "attn_v_bias_abs":
            attn_rank[wid],
        "ffn_up_weight_abs":
            ffn_rank[wid],
    }

    row["joint_rank"] = (
        field_rank[wid]
        + scale_rank[wid]
        + attn_rank[wid]
        + ffn_rank[wid]
    )

    av = row["components"]["attn_v.bias"]["delta"]
    fu = row["components"]["ffn_up.weight"]["delta"]

    row["target_direction_score"] = (
        max(-av, 0.0)
        + max(-fu, 0.0)
    )

    row["target_both_negative"] = (
        av < 0
        and fu < 0
    )


# ------------------------------------------------------------
# Discovery rankings
# ------------------------------------------------------------

joint = sorted(
    results,
    key=lambda x: x["joint_rank"],
)

target = sorted(
    results,
    key=lambda x: (
        x["target_both_negative"],
        x["target_direction_score"],
    ),
    reverse=True,
)

strong = sorted(
    results,
    key=lambda x: (
        x["target_both_negative"],
        x["joint_rank"] * -1,
    ),
    reverse=True,
)


print()
print("=" * 72)
print(" TOP WINDOWS BY JOINT STRUCTURAL RANK")
print("=" * 72)

for row in joint[:15]:

    av = row["components"]["attn_v.bias"]
    fu = row["components"]["ffn_up.weight"]

    print(
        f"{row['window_id']:<11} "
        f"size={row['window_size']} "
        f"joint={row['joint_rank']:>4} | "
        f"field={row['mean_field_delta']:+.6f} | "
        f"scale={row['scale_field_delta']:+.6f} | "
        f"v_bias={av['delta']:+.6f} "
        f"(p={av['p']:.4f}) | "
        f"ffn_up={fu['delta']:+.6f} "
        f"(p={fu['p']:.4f})"
    )


print()
print("=" * 72)
print(" TOP WINDOWS BY TARGET DIRECTION")
print("=" * 72)

for row in target[:15]:

    av = row["components"]["attn_v.bias"]
    fu = row["components"]["ffn_up.weight"]

    print(
        f"{row['window_id']:<11} "
        f"size={row['window_size']} "
        f"both_negative={row['target_both_negative']} | "
        f"v_bias={av['delta']:+.6f} "
        f"(p={av['p']:.4f}) | "
        f"ffn_up={fu['delta']:+.6f} "
        f"(p={fu['p']:.4f})"
    )


print()
print("=" * 72)
print(" WINDOW-SIZE WINNERS")
print("=" * 72)

size_winners = {}

for size in WINDOW_SIZES:

    subset = [
        r for r in results
        if r["window_size"] == size
    ]

    winner = min(
        subset,
        key=lambda x: x["joint_rank"],
    )

    size_winners[str(size)] = {
        "window": winner["window_id"],
        "joint_rank": winner["joint_rank"],
        "mean_field_delta":
            winner["mean_field_delta"],
        "scale_field_delta":
            winner["scale_field_delta"],
        "attn_v_bias_delta":
            winner["components"]["attn_v.bias"]["delta"],
        "ffn_up_weight_delta":
            winner["components"]["ffn_up.weight"]["delta"],
    }

    print(
        f"size={size} | "
        f"{winner['window_id']} | "
        f"joint={winner['joint_rank']}"
    )


# ------------------------------------------------------------
# Specifically locate the V11 region.
# ------------------------------------------------------------

v11_windows = [
    r for r in results
    if r["from"] == 6
    and r["to"] == 12
]

print()
print("=" * 72)
print(" V11 REGION CHECK")
print("=" * 72)

if v11_windows:

    for row in v11_windows:

        av = row["components"]["attn_v.bias"]
        fu = row["components"]["ffn_up.weight"]

        print(
            f"{row['window_id']} | "
            f"size={row['window_size']} | "
            f"joint_rank={row['joint_rank']} | "
            f"v_bias={av['delta']:+.6f} "
            f"p={av['p']:.4f} | "
            f"ffn_up={fu['delta']:+.6f} "
            f"p={fu['p']:.4f}"
        )

else:

    print(
        "No exact L06-L12 window exists "
        "for the scanned window sizes."
    )


result = {
    "format":
        "OpenMind Q8 Phase Region Discovery V12",

    "configuration": {
        "seed": SEED,
        "permutations": PERMUTATIONS,
        "window_sizes": WINDOW_SIZES,
    },

    "transition_count":
        len(transitions),

    "components":
        components,

    "targets":
        TARGETS,

    "results":
        results,

    "window_size_winners":
        size_winners,

    "top_joint":
        [
            r["window_id"]
            for r in joint[:15]
        ],

    "top_target_direction":
        [
            r["window_id"]
            for r in target[:15]
        ],
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
print("Q8 PHASE REGION DISCOVERY V12 COMPLETE")
