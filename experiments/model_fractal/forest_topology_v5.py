#!/usr/bin/env python3

import csv
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path

import numpy as np


PATH = Path("activation_vectors_all_tokens.csv")

SEED = 1337
FOLDS = 4
GROUP_SIZE = 64
EXCLUDED_TOKENS = {0}

REQUEST_FRACTIONS = (
    0.125,
    0.250,
    0.500,
    0.750,
)


def load_vectors():
    rows = []

    with PATH.open(newline="") as f:
        reader = csv.DictReader(f)

        for r in reader:
            token = int(r["token_index"])

            if token in EXCLUDED_TOKENS:
                continue

            layer = int(r["layer"])
            dim = int(r["embedding_dimension"])

            rows.append({
                "token": token,
                "layer": layer,
                "vec": np.asarray(
                    [
                        float(r[f"v{i}"])
                        for i in range(dim)
                    ],
                    dtype=np.float64,
                ),
            })

    return rows


def residualize(rows, centroid):
    return [
        {
            "token": r["token"],
            "layer": r["layer"],
            "residual": r["vec"] - centroid,
        }
        for r in rows
    ]


def contiguous_groups(dim):
    return [
        np.arange(
            start,
            min(start + GROUP_SIZE, dim),
            dtype=np.int32,
        )
        for start in range(0, dim, GROUP_SIZE)
    ]


def random_groups(dim, seed):
    ids = list(range(dim))

    rng = random.Random(seed)
    rng.shuffle(ids)

    return [
        np.asarray(
            ids[start:start + GROUP_SIZE],
            dtype=np.int32,
        )
        for start in range(0, dim, GROUP_SIZE)
    ]


def correlated_groups(train_matrix):
    corr = np.corrcoef(
        train_matrix,
        rowvar=False,
    )

    corr = np.nan_to_num(
        corr,
        nan=0.0,
        posinf=0.0,
        neginf=0.0,
    )

    corr = np.abs(corr)
    np.fill_diagonal(corr, 0.0)

    dim = train_matrix.shape[1]

    unused = set(range(dim))
    mean_corr = corr.mean(axis=1)
    groups = []

    while unused:
        seed = max(
            unused,
            key=lambda i: (
                mean_corr[i],
                -i,
            ),
        )

        candidates = sorted(
            (
                i
                for i in unused
                if i != seed
            ),
            key=lambda i: (
                -corr[seed, i],
                i,
            ),
        )

        members = [seed]
        members.extend(
            candidates[:GROUP_SIZE - 1]
        )

        for i in members:
            unused.remove(i)

        groups.append(
            np.asarray(
                members,
                dtype=np.int32,
            )
        )

    return groups


def group_energies(vec, groups):
    return np.asarray(
        [
            float(
                np.dot(
                    vec[group],
                    vec[group],
                )
            )
            for group in groups
        ],
        dtype=np.float64,
    )


def learn_layer_router(train_rows, groups):
    accum = defaultdict(list)

    global_values = []

    for row in train_rows:
        energies = group_energies(
            row["residual"],
            groups,
        )

        accum[row["layer"]].append(
            energies
        )

        global_values.append(
            energies
        )

    layer_rankings = {}

    for layer, values in accum.items():
        mean_energy = np.stack(
            values,
            axis=0,
        ).mean(axis=0)

        ranking = np.argsort(
            -mean_energy,
            kind="stable",
        )

        layer_rankings[layer] = ranking

    global_mean = np.stack(
        global_values,
        axis=0,
    ).mean(axis=0)

    global_ranking = np.argsort(
        -global_mean,
        kind="stable",
    )

    return layer_rankings, global_ranking


def select_from_ranking(
    vec,
    groups,
    ranking,
    fraction,
):
    k = max(
        1,
        math.ceil(
            len(groups) * fraction
        ),
    )

    selected = ranking[:k]

    total = float(
        np.dot(vec, vec)
    )

    captured = 0.0

    for index in selected:
        part = vec[
            groups[int(index)]
        ]

        captured += float(
            np.dot(part, part)
        )

    if total == 0.0:
        return 1.0

    return captured / total


def oracle_energy(vec, groups, fraction):
    values = sorted(
        group_energies(
            vec,
            groups,
        ),
        reverse=True,
    )

    k = max(
        1,
        math.ceil(
            len(groups) * fraction
        ),
    )

    total = sum(values)

    if total == 0.0:
        return 1.0

    return sum(values[:k]) / total


def token_folds(tokens):
    tokens = sorted(tokens)

    rng = random.Random(SEED)
    rng.shuffle(tokens)

    folds = [
        []
        for _ in range(FOLDS)
    ]

    for i, token in enumerate(tokens):
        folds[i % FOLDS].append(token)

    return folds


def mean(values):
    return statistics.mean(values)


rows = load_vectors()

if not rows:
    raise RuntimeError("no vectors loaded")

dim = len(rows[0]["vec"])

tokens = sorted({
    r["token"]
    for r in rows
})

folds = token_folds(tokens)

pine_groups = contiguous_groups(dim)

random_groups_fixed = random_groups(
    dim,
    SEED,
)

summary = {
    fraction: {
        "pine": [],
        "random": [],
        "orange_router": [],
        "orange_oracle": [],
    }
    for fraction in REQUEST_FRACTIONS
}

fold_wins = {
    fraction: 0
    for fraction in REQUEST_FRACTIONS
}

print("=" * 124)
print(
    " OPENMIND / FOREST TOPOLOGY V5 "
    "— NON-ORACLE LAYER-CONDITIONED ROUTING"
)
print("=" * 124)

print()
print("ROUTING CONTRACT")
print("-" * 124)

print(
    "Orange wedge geometry is learned from "
    "training tokens only."
)
print(
    "The router ranks wedges using mean training "
    "energy conditioned only on layer index."
)
print(
    "Held-out residual values are never inspected "
    "before wedge selection."
)
print(
    "Orange Oracle remains only as an upper-bound "
    "control."
)

print()
print("FOLD RESULTS")
print("-" * 124)

for fold_index, test_tokens in enumerate(
    folds,
    start=1,
):
    test_set = set(test_tokens)

    train_raw = [
        r
        for r in rows
        if r["token"] not in test_set
    ]

    test_raw = [
        r
        for r in rows
        if r["token"] in test_set
    ]

    train_matrix_raw = np.stack(
        [
            r["vec"]
            for r in train_raw
        ],
        axis=0,
    )

    train_centroid = train_matrix_raw.mean(
        axis=0
    )

    train = residualize(
        train_raw,
        train_centroid,
    )

    test = residualize(
        test_raw,
        train_centroid,
    )

    train_matrix = np.stack(
        [
            r["residual"]
            for r in train
        ],
        axis=0,
    )

    orange_groups = correlated_groups(
        train_matrix
    )

    orange_layer, orange_global = (
        learn_layer_router(
            train,
            orange_groups,
        )
    )

    pine_layer, pine_global = (
        learn_layer_router(
            train,
            pine_groups,
        )
    )

    random_layer, random_global = (
        learn_layer_router(
            train,
            random_groups_fixed,
        )
    )

    print()
    print(f"FOLD {fold_index}")

    print(
        "  held-out tokens           : "
        + ",".join(
            map(
                str,
                sorted(test_tokens),
            )
        )
    )

    print(
        "  request  "
        "pine_router random_router "
        "orange_router orange_oracle "
        "orange/pine oracle_fraction"
    )

    fold_values = {
        fraction: {
            "pine": [],
            "random": [],
            "orange_router": [],
            "orange_oracle": [],
        }
        for fraction in REQUEST_FRACTIONS
    }

    for row in test:
        layer = row["layer"]
        vec = row["residual"]

        orange_rank = orange_layer.get(
            layer,
            orange_global,
        )

        pine_rank = pine_layer.get(
            layer,
            pine_global,
        )

        random_rank = random_layer.get(
            layer,
            random_global,
        )

        for fraction in REQUEST_FRACTIONS:
            fold_values[fraction]["pine"].append(
                select_from_ranking(
                    vec,
                    pine_groups,
                    pine_rank,
                    fraction,
                )
            )

            fold_values[fraction]["random"].append(
                select_from_ranking(
                    vec,
                    random_groups_fixed,
                    random_rank,
                    fraction,
                )
            )

            fold_values[fraction][
                "orange_router"
            ].append(
                select_from_ranking(
                    vec,
                    orange_groups,
                    orange_rank,
                    fraction,
                )
            )

            fold_values[fraction][
                "orange_oracle"
            ].append(
                oracle_energy(
                    vec,
                    orange_groups,
                    fraction,
                )
            )

    for fraction in REQUEST_FRACTIONS:
        values = fold_values[fraction]

        pine = mean(values["pine"])
        random_result = mean(
            values["random"]
        )

        orange_router = mean(
            values["orange_router"]
        )

        orange_oracle = mean(
            values["orange_oracle"]
        )

        orange_pine = (
            orange_router / pine
        )

        oracle_fraction = (
            orange_router /
            orange_oracle
        )

        if (
            orange_router > pine
            and
            orange_router > random_result
        ):
            fold_wins[fraction] += 1

        summary[fraction]["pine"].append(
            pine
        )

        summary[fraction]["random"].append(
            random_result
        )

        summary[fraction][
            "orange_router"
        ].append(
            orange_router
        )

        summary[fraction][
            "orange_oracle"
        ].append(
            orange_oracle
        )

        print(
            f"  {fraction:7.3f} "
            f"{pine:11.9f} "
            f"{random_result:13.9f} "
            f"{orange_router:13.9f} "
            f"{orange_oracle:13.9f} "
            f"{orange_pine:11.9f} "
            f"{oracle_fraction:14.9f}"
        )


print()
print("CROSS-FOLD SUMMARY")
print("-" * 124)

print(
    "request  pine_energy random_energy "
    "orange_router orange_oracle "
    "orange/pine orange/random "
    "router/oracle fold_wins"
)

all_pass = True

for fraction in REQUEST_FRACTIONS:
    values = summary[fraction]

    pine = mean(
        values["pine"]
    )

    random_result = mean(
        values["random"]
    )

    orange_router = mean(
        values["orange_router"]
    )

    orange_oracle = mean(
        values["orange_oracle"]
    )

    orange_pine = (
        orange_router /
        pine
    )

    orange_random = (
        orange_router /
        random_result
    )

    router_oracle = (
        orange_router /
        orange_oracle
    )

    wins = fold_wins[fraction]

    passed = (
        orange_pine > 1.0
        and
        orange_random > 1.0
        and
        wins >= 3
    )

    if not passed:
        all_pass = False

    print(
        f"{fraction:7.3f} "
        f"{pine:11.9f} "
        f"{random_result:13.9f} "
        f"{orange_router:13.9f} "
        f"{orange_oracle:13.9f} "
        f"{orange_pine:11.9f} "
        f"{orange_random:13.9f} "
        f"{router_oracle:13.9f} "
        f"{wins:4d}/4"
    )


print()
print("FOREST V5 DECISION")
print("-" * 124)

if all_pass:
    print(
        "result                     : "
        "NON-ORACLE ORANGE ROUTING PASSES"
    )
else:
    print(
        "result                     : "
        "NON-ORACLE ORANGE ROUTING "
        "NOT YET ESTABLISHED"
    )

print()
print("INTERPRETATION BOUNDARY")
print("-" * 124)

print(
    "V5 uses only layer identity and statistics "
    "learned from training tokens to select wedges."
)

print(
    "It does not inspect held-out residual energy "
    "before routing."
)

print(
    "The Orange Oracle is retained only to measure "
    "how much routing headroom remains."
)

print(
    "No quantization, serialization, mmap, or "
    "wall-clock access benchmark is included."
)
