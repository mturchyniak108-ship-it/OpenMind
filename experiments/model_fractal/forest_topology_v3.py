#!/usr/bin/env python3

import csv
import math
import random
import statistics

import numpy as np


PATH = "activation_vectors_all_tokens.csv"

EXCLUDED_TOKENS = {0}

BRANCHING = 4
MAX_DEPTH = 6

GROUP_SIZE = 64
RANDOM_SEED = 1337

ACCESS_FRACTIONS = (
    0.125,
    0.25,
    0.50,
    0.75,
    1.00,
)


# ============================================================
# MATH
# ============================================================

def cosine(a, b):
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)

    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)

    if na == 0.0 or nb == 0.0:
        return 0.0

    return float(
        np.dot(a, b) / (na * nb)
    )


def relative_l2(a, b):
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)

    denom = np.linalg.norm(a)

    if denom == 0.0:
        return 0.0

    return float(
        np.linalg.norm(a - b) / denom
    )


# ============================================================
# TREE
# ============================================================

def centroid(items):
    return np.stack(
        [item["vector"] for item in items],
        axis=0,
    ).mean(
        axis=0,
        dtype=np.float64,
    )


def split(items):
    if len(items) <= 1:
        return [items]

    matrix = np.stack(
        [item["vector"] for item in items],
        axis=0,
    )

    variances = matrix.var(
        axis=0,
        dtype=np.float64,
    )

    axis = int(
        np.argmax(variances)
    )

    ordered = sorted(
        items,
        key=lambda item: item["vector"][axis],
    )

    groups = []

    for k in range(BRANCHING):
        lo = len(ordered) * k // BRANCHING
        hi = len(ordered) * (k + 1) // BRANCHING

        if lo < hi:
            groups.append(
                ordered[lo:hi]
            )

    return groups


def build(items, depth=0, parent=None):
    node = {
        "depth": depth,
        "centroid": centroid(items),
        "parent": parent,
        "children": [],
        "items": items,
    }

    if (
        depth >= MAX_DEPTH
        or len(items) <= BRANCHING
    ):
        return node

    for group in split(items):
        node["children"].append(
            build(
                group,
                depth + 1,
                node,
            )
        )

    return node


def walk(node):
    yield node

    for child in node["children"]:
        yield from walk(child)


# ============================================================
# LOAD
# ============================================================

data = []

with open(PATH, newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        token = int(
            row["token_index"]
        )

        if token in EXCLUDED_TOKENS:
            continue

        dim = int(
            row["embedding_dimension"]
        )

        data.append({
            "layer": int(row["layer"]),
            "token": token,
            "vector": np.asarray(
                [
                    float(row[f"v{i}"])
                    for i in range(dim)
                ],
                dtype=np.float64,
            ),
        })


if not data:
    raise RuntimeError(
        "dataset empty after exclusions"
    )


dim = len(
    data[0]["vector"]
)

if dim % GROUP_SIZE != 0:
    raise RuntimeError(
        "V3 requires dimension divisible by group size"
    )


GROUP_COUNT = (
    dim // GROUP_SIZE
)


root = build(data)

nodes = list(
    walk(root)
)

leaves = [
    node
    for node in nodes
    if not node["children"]
]


# ============================================================
# TERMINAL RESIDUAL MATRIX
#
# V3 deliberately isolates terminal organization.
# Shared tree reconstruction remains exact.
# ============================================================

residual_records = []

for leaf in leaves:
    for item in leaf["items"]:
        residual_records.append({
            "leaf": leaf,
            "item": item,
            "residual": (
                item["vector"]
                - leaf["centroid"]
            ),
        })


R = np.stack(
    [
        record["residual"]
        for record
        in residual_records
    ],
    axis=0,
)


# ============================================================
# PINE GROUPS
#
# Ordinary contiguous groups.
# ============================================================

pine_groups = []

for start in range(
    0,
    dim,
    GROUP_SIZE,
):
    pine_groups.append(
        np.arange(
            start,
            start + GROUP_SIZE,
            dtype=np.int32,
        )
    )


# ============================================================
# RANDOM CONTROL
#
# Non-contiguous but structure-free.
# ============================================================

rng = random.Random(
    RANDOM_SEED
)

random_dims = list(
    range(dim)
)

rng.shuffle(
    random_dims
)

random_groups = []

for start in range(
    0,
    dim,
    GROUP_SIZE,
):
    random_groups.append(
        np.asarray(
            random_dims[
                start:start + GROUP_SIZE
            ],
            dtype=np.int32,
        )
    )


# ============================================================
# ORANGE CORRELATION WEDGES
#
# 1. Standardize terminal-residual dimensions.
# 2. Compute dimension correlation.
# 3. Pick highest-variance unused dimension as seed.
# 4. Fill wedge with unused dimensions most strongly
#    correlated in absolute value with that seed.
#
# This is intentionally simple/deterministic.
# It is not claimed to be an optimal clustering algorithm.
# ============================================================

column_variance = R.var(
    axis=0,
    dtype=np.float64,
)

centered = (
    R - R.mean(
        axis=0,
        dtype=np.float64,
    )
)

std = centered.std(
    axis=0,
    dtype=np.float64,
)

safe_std = np.where(
    std > 1e-12,
    std,
    1.0,
)

Z = (
    centered
    / safe_std
).astype(
    np.float32
)

denom = max(
    1,
    len(R) - 1,
)

corr = (
    Z.T @ Z
) / float(denom)

corr = np.abs(
    corr
)

unused = set(
    range(dim)
)

orange_groups = []

while unused:
    seed = max(
        unused,
        key=lambda i: (
            column_variance[i],
            -i,
        ),
    )

    candidates = np.fromiter(
        unused,
        dtype=np.int32,
    )

    strengths = corr[
        seed,
        candidates,
    ]

    order = np.argsort(
        -strengths,
        kind="stable",
    )

    chosen = []

    for pos in order:
        d = int(
            candidates[pos]
        )

        if d in unused:
            chosen.append(d)

        if len(chosen) >= GROUP_SIZE:
            break

    if seed not in chosen:
        chosen[-1] = seed

    chosen = sorted(
        set(chosen),
        key=lambda d: (
            -float(
                corr[seed, d]
            ),
            d,
        ),
    )

    if len(chosen) < GROUP_SIZE:
        remaining = sorted(
            unused - set(chosen)
        )

        chosen.extend(
            remaining[
                :GROUP_SIZE
                - len(chosen)
            ]
        )

    chosen = chosen[
        :GROUP_SIZE
    ]

    for d in chosen:
        unused.remove(d)

    orange_groups.append(
        np.asarray(
            chosen,
            dtype=np.int32,
        )
    )


if len(orange_groups) != GROUP_COUNT:
    raise RuntimeError(
        "unexpected Orange group count"
    )


# ============================================================
# GROUP STRUCTURE METRICS
# ============================================================

def mean_within_abs_corr(groups):
    values = []

    for group in groups:
        sub = corr[
            np.ix_(
                group,
                group,
            )
        ]

        mask = ~np.eye(
            len(group),
            dtype=bool,
        )

        values.extend(
            sub[mask].tolist()
        )

    return statistics.mean(
        values
    )


pine_corr = mean_within_abs_corr(
    pine_groups
)

random_corr = mean_within_abs_corr(
    random_groups
)

orange_corr = mean_within_abs_corr(
    orange_groups
)


# ============================================================
# ORACLE INFORMATION-CONCENTRATION TEST
#
# For every item:
#
# - calculate residual energy in each group
# - choose the highest-energy K groups
# - reconstruct ONLY those residual dimensions
# - leave remaining residual dimensions at leaf centroid
#
# Equal K for Pine, Orange, Random.
#
# This is an oracle upper-bound experiment, NOT yet a
# production retrieval policy.
# ============================================================

schemes = {
    "PINE_CONTIGUOUS": pine_groups,
    "RANDOM_CONTROL": random_groups,
    "ORANGE_CORRELATED": orange_groups,
}


metrics = {
    name: {
        fraction: {
            "cosine": [],
            "rel_l2": [],
            "energy": [],
        }
        for fraction
        in ACCESS_FRACTIONS
    }
    for name
    in schemes
}


for record in residual_records:
    leaf = record["leaf"]
    item = record["item"]
    residual = record["residual"]

    original = item[
        "vector"
    ]

    base = leaf[
        "centroid"
    ]

    total_energy = float(
        np.dot(
            residual,
            residual,
        )
    )

    for name, groups in schemes.items():
        group_energy = []

        for index, group in enumerate(
            groups
        ):
            part = residual[
                group
            ]

            energy = float(
                np.dot(
                    part,
                    part,
                )
            )

            group_energy.append(
                (
                    energy,
                    index,
                )
            )

        group_energy.sort(
            key=lambda x: (
                -x[0],
                x[1],
            )
        )

        for fraction in ACCESS_FRACTIONS:
            keep_count = max(
                1,
                min(
                    GROUP_COUNT,
                    int(
                        math.ceil(
                            GROUP_COUNT
                            * fraction
                        )
                    ),
                ),
            )

            selected = [
                index
                for _energy, index
                in group_energy[
                    :keep_count
                ]
            ]

            reconstructed = (
                base.copy()
            )

            retained_energy = 0.0

            for index in selected:
                group = groups[
                    index
                ]

                reconstructed[
                    group
                ] += residual[
                    group
                ]

                retained_energy += (
                    group_energy[
                        next(
                            i
                            for i, pair
                            in enumerate(
                                group_energy
                            )
                            if pair[1]
                            == index
                        )
                    ][0]
                )

            metrics[
                name
            ][fraction][
                "cosine"
            ].append(
                cosine(
                    original,
                    reconstructed,
                )
            )

            metrics[
                name
            ][fraction][
                "rel_l2"
            ].append(
                relative_l2(
                    original,
                    reconstructed,
                )
            )

            if total_energy > 0.0:
                retained = (
                    retained_energy
                    / total_energy
                )
            else:
                retained = 1.0

            metrics[
                name
            ][fraction][
                "energy"
            ].append(
                retained
            )


# ============================================================
# CORRELATION MAPPING STORAGE
#
# Pine contiguous mapping is implicit.
#
# Orange and random need one uint16 dimension ID for each
# dimension if represented as an explicit global permutation.
# This map is global, not repeated for every vector.
# ============================================================

PINE_MAPPING_BYTES = 0

ORANGE_MAPPING_BYTES = (
    dim * 2
)

RANDOM_MAPPING_BYTES = (
    dim * 2
)


# ============================================================
# OUTPUT
# ============================================================

print("=" * 124)

print(
    " OPENMIND / FOREST TOPOLOGY V3 — "
    "NON-CONTIGUOUS ORANGE WEDGES"
)

print("=" * 124)

print()

print("DATASET")
print("-" * 124)

print(
    f"vectors                     : "
    f"{len(data)}"
)

print(
    f"dimensions                  : "
    f"{dim}"
)

print(
    f"terminal residuals          : "
    f"{len(residual_records)}"
)

print(
    f"terminal leaves             : "
    f"{len(leaves)}"
)

print(
    f"group size                  : "
    f"{GROUP_SIZE}"
)

print(
    f"groups                      : "
    f"{GROUP_COUNT}"
)


print()
print("GROUPING CONTRACT")
print("-" * 124)

print(
    "PINE_CONTIGUOUS   : ordinary contiguous "
    "64-dimension terminal groups"
)

print(
    "RANDOM_CONTROL    : deterministic shuffled "
    "non-contiguous groups"
)

print(
    "ORANGE_CORRELATED : non-contiguous groups seeded "
    "by terminal-residual dimension correlation"
)


print()
print("WITHIN-GROUP ABSOLUTE CORRELATION")
print("-" * 124)

print(
    f"PINE_CONTIGUOUS             : "
    f"{pine_corr:.9f}"
)

print(
    f"RANDOM_CONTROL              : "
    f"{random_corr:.9f}"
)

print(
    f"ORANGE_CORRELATED           : "
    f"{orange_corr:.9f}"
)

print(
    f"Orange/Pine correlation     : "
    f"{orange_corr / pine_corr:.9f}"
)

print(
    f"Orange/Random correlation   : "
    f"{orange_corr / random_corr:.9f}"
)


print()
print("GLOBAL GROUP-MAP STORAGE")
print("-" * 124)

print(
    f"Pine mapping bytes          : "
    f"{PINE_MAPPING_BYTES}"
)

print(
    f"Random mapping bytes        : "
    f"{RANDOM_MAPPING_BYTES}"
)

print(
    f"Orange mapping bytes        : "
    f"{ORANGE_MAPPING_BYTES}"
)

print(
    "Orange mapping assumption  : uint16 dimension ID "
    "stored once globally"
)


print()
print("ORACLE INFORMATION CONCENTRATION")
print("-" * 124)

print(
    "scheme               request groups "
    "mean_energy  mean_cosine  min_cosine "
    "mean_rel_l2  max_rel_l2"
)

for name in schemes:
    for fraction in ACCESS_FRACTIONS:
        row = metrics[
            name
        ][fraction]

        keep = max(
            1,
            min(
                GROUP_COUNT,
                int(
                    math.ceil(
                        GROUP_COUNT
                        * fraction
                    )
                ),
            ),
        )

        print(
            f"{name:<20} "
            f"{fraction:7.3f} "
            f"{keep:6d} "
            f"{statistics.mean(row['energy']):11.9f} "
            f"{statistics.mean(row['cosine']):12.9f} "
            f"{min(row['cosine']):11.9f} "
            f"{statistics.mean(row['rel_l2']):11.9f} "
            f"{max(row['rel_l2']):11.9f}"
        )


print()
print("ORANGE VS PINE")
print("-" * 124)

print(
    "request  orange_energy/pine  "
    "orange_cos-pine   "
    "orange_rel_l2/pine"
)

orange_wins = 0

for fraction in ACCESS_FRACTIONS:
    pine = metrics[
        "PINE_CONTIGUOUS"
    ][fraction]

    orange = metrics[
        "ORANGE_CORRELATED"
    ][fraction]

    pine_energy = statistics.mean(
        pine["energy"]
    )

    orange_energy = statistics.mean(
        orange["energy"]
    )

    pine_cos = statistics.mean(
        pine["cosine"]
    )

    orange_cos = statistics.mean(
        orange["cosine"]
    )

    pine_err = statistics.mean(
        pine["rel_l2"]
    )

    orange_err = statistics.mean(
        orange["rel_l2"]
    )

    energy_ratio = (
        orange_energy
        / pine_energy
        if pine_energy
        else 1.0
    )

    error_ratio = (
        orange_err
        / pine_err
        if pine_err
        else 1.0
    )

    print(
        f"{fraction:7.3f} "
        f"{energy_ratio:18.9f} "
        f"{orange_cos - pine_cos:+17.9f} "
        f"{error_ratio:18.9f}"
    )

    if (
        fraction < 1.0
        and orange_energy
        > pine_energy
        and orange_err
        < pine_err
    ):
        orange_wins += 1


print()
print("RANDOM CONTROL CHECK")
print("-" * 124)

print(
    "request  orange_energy/random "
    "orange_rel_l2/random"
)

for fraction in ACCESS_FRACTIONS:
    random_row = metrics[
        "RANDOM_CONTROL"
    ][fraction]

    orange_row = metrics[
        "ORANGE_CORRELATED"
    ][fraction]

    re = statistics.mean(
        random_row["energy"]
    )

    oe = statistics.mean(
        orange_row["energy"]
    )

    rr = statistics.mean(
        random_row["rel_l2"]
    )

    ore = statistics.mean(
        orange_row["rel_l2"]
    )

    print(
        f"{fraction:7.3f} "
        f"{oe / re:20.9f} "
        f"{ore / rr:20.9f}"
    )


print()
print("FOREST V3 DECISION")
print("-" * 124)

print(
    f"partial-access Orange wins : "
    f"{orange_wins}/"
    f"{len(ACCESS_FRACTIONS) - 1}"
)

if orange_wins >= 3:
    print(
        "result                     : "
        "CORRELATED WEDGES PROMISING"
    )
elif orange_wins > 0:
    print(
        "result                     : "
        "MIXED / REQUIRES FOLLOW-UP"
    )
else:
    print(
        "result                     : "
        "NO CORRELATED-WEDGE ADVANTAGE"
    )


print()
print("INTERPRETATION BOUNDARY")
print("-" * 124)

print(
    "Forest V3 isolates terminal grouping geometry "
    "using exact residual values."
)

print(
    "It deliberately does NOT benchmark quantization "
    "or production serialization."
)

print(
    "Group selection is oracle top-energy selection "
    "per item, so this measures information-concentration "
    "potential rather than a deployable query router."
)

print(
    "The random control distinguishes correlation-derived "
    "structure from arbitrary non-contiguous grouping."
)

print(
    "If Orange wins this gate, the next experiment should "
    "quantize correlated wedges and replace oracle selection "
    "with a measurable routing rule."
)
