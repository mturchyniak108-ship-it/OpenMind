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

SCALE_BYTES = 4
DIMENSION_ID_BYTES = 2
ROUTER_SCORE_BYTES = 4


def load_vectors():
    rows = []

    with PATH.open(newline="") as f:
        reader = csv.DictReader(f)

        for r in reader:
            token = int(r["token_index"])

            if token in EXCLUDED_TOKENS:
                continue

            dim = int(r["embedding_dimension"])

            rows.append({
                "token": token,
                "layer": int(r["layer"]),
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
            "token": row["token"],
            "layer": row["layer"],
            "residual": row["vec"] - centroid,
        }
        for row in rows
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
        values = group_energies(
            row["residual"],
            groups,
        )

        accum[row["layer"]].append(values)
        global_values.append(values)

    layer_rankings = {}
    layer_scores = {}

    for layer, values in accum.items():
        mean_energy = np.stack(
            values,
            axis=0,
        ).mean(axis=0)

        layer_scores[layer] = mean_energy

        layer_rankings[layer] = np.argsort(
            -mean_energy,
            kind="stable",
        )

    global_mean = np.stack(
        global_values,
        axis=0,
    ).mean(axis=0)

    global_ranking = np.argsort(
        -global_mean,
        kind="stable",
    )

    return (
        layer_rankings,
        global_ranking,
        layer_scores,
        global_mean,
    )


def quantize_block(values):
    values = np.asarray(
        values,
        dtype=np.float64,
    )

    if values.size == 0:
        return (
            np.asarray([], dtype=np.float64),
            SCALE_BYTES,
        )

    peak = float(
        np.max(
            np.abs(values)
        )
    )

    if peak == 0.0:
        reconstructed = np.zeros_like(values)

    else:
        scale = peak / 127.0

        q = np.clip(
            np.rint(values / scale),
            -127,
            127,
        ).astype(np.int8)

        reconstructed = (
            q.astype(np.float64) * scale
        )

    encoded_bytes = (
        int(values.size)
        + SCALE_BYTES
    )

    return reconstructed, encoded_bytes


def select_indices(ranking, group_count, fraction):
    k = max(
        1,
        math.ceil(
            group_count * fraction
        ),
    )

    return [
        int(x)
        for x in ranking[:k]
    ]


def oracle_indices(vec, groups, fraction):
    energies = group_energies(
        vec,
        groups,
    )

    ranking = np.argsort(
        -energies,
        kind="stable",
    )

    return select_indices(
        ranking,
        len(groups),
        fraction,
    )


def reconstruct_selected(
    vec,
    groups,
    selected,
):
    reconstructed = np.zeros_like(
        vec,
        dtype=np.float64,
    )

    encoded_bytes = 0

    for index in selected:
        group = groups[index]

        restored, block_bytes = (
            quantize_block(
                vec[group]
            )
        )

        reconstructed[group] = restored
        encoded_bytes += block_bytes

    return reconstructed, encoded_bytes


def energy_fraction(
    original,
    reconstructed,
):
    denom = float(
        np.dot(
            original,
            original,
        )
    )

    if denom == 0.0:
        return 1.0

    return float(
        np.dot(
            reconstructed,
            reconstructed,
        )
    ) / denom


def cosine(a, b):
    na = float(
        np.linalg.norm(a)
    )

    nb = float(
        np.linalg.norm(b)
    )

    if na == 0.0 or nb == 0.0:
        return 0.0

    return float(
        np.dot(a, b)
        / (na * nb)
    )


def relative_l2(a, b):
    denom = float(
        np.linalg.norm(a)
    )

    if denom == 0.0:
        return 0.0

    return float(
        np.linalg.norm(a - b)
        / denom
    )


def token_folds(tokens):
    values = sorted(tokens)

    rng = random.Random(SEED)
    rng.shuffle(values)

    folds = [
        []
        for _ in range(FOLDS)
    ]

    for i, token in enumerate(values):
        folds[i % FOLDS].append(token)

    return folds


def mean(values):
    return statistics.mean(values)


rows = load_vectors()

if not rows:
    raise RuntimeError("no vectors loaded")

dim = len(rows[0]["vec"])

tokens = sorted({
    row["token"]
    for row in rows
})

layers = sorted({
    row["layer"]
    for row in rows
})

folds = token_folds(tokens)

pine_groups = contiguous_groups(dim)

flat_fp32_bytes = (
    len(rows) * dim * 4
)

group_count = len(pine_groups)

summary = {
    fraction: {
        "pine_energy": [],
        "orange_energy": [],
        "oracle_energy": [],
        "pine_cos": [],
        "orange_cos": [],
        "oracle_cos": [],
        "pine_l2": [],
        "orange_l2": [],
        "oracle_l2": [],
        "pine_bytes": [],
        "orange_bytes": [],
        "oracle_bytes": [],
    }
    for fraction in REQUEST_FRACTIONS
}

fold_wins = {
    fraction: 0
    for fraction in REQUEST_FRACTIONS
}

orange_map_bytes = (
    dim * DIMENSION_ID_BYTES
)

router_metadata_bytes = (
    len(layers)
    * group_count
    * ROUTER_SCORE_BYTES
)

print("=" * 132)
print(
    " OPENMIND / FOREST TOPOLOGY V6 "
    "— QUANTIZED NON-ORACLE ORANGE"
)
print("=" * 132)

print()
print("EXPERIMENT CONTRACT")
print("-" * 132)

print(
    "Pine and Orange both use BLOCK_INT8_64 "
    "quantization for selected terminal groups."
)

print(
    "Orange groups and layer-conditioned routing "
    "statistics are learned from training tokens only."
)

print(
    "Held-out residual values are never inspected "
    "before non-oracle routing."
)

print(
    "Orange Oracle is retained only as an upper-bound "
    "selection control."
)

print()
print("GLOBAL ACCOUNTING")
print("-" * 132)

print(f"vectors                    : {len(rows)}")
print(f"tokens                     : {len(tokens)}")
print(f"dimensions                 : {dim}")
print(f"layers                     : {len(layers)}")
print(f"group size                 : {GROUP_SIZE}")
print(f"groups                     : {group_count}")
print(f"flat FP32 bytes            : {flat_fp32_bytes}")
print(f"Orange group map bytes     : {orange_map_bytes}")
print(f"Orange router bytes        : {router_metadata_bytes}")
print(
    f"Orange fixed metadata      : "
    f"{orange_map_bytes + router_metadata_bytes}"
)

print()
print("FOLD RESULTS")
print("-" * 132)

for fold_index, test_tokens in enumerate(
    folds,
    start=1,
):
    test_set = set(test_tokens)

    train_raw = [
        row
        for row in rows
        if row["token"] not in test_set
    ]

    test_raw = [
        row
        for row in rows
        if row["token"] in test_set
    ]

    train_matrix_raw = np.stack(
        [
            row["vec"]
            for row in train_raw
        ],
        axis=0,
    )

    train_centroid = (
        train_matrix_raw.mean(
            axis=0
        )
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
            row["residual"]
            for row in train
        ],
        axis=0,
    )

    orange_groups = correlated_groups(
        train_matrix
    )

    (
        orange_layer,
        orange_global,
        _,
        _,
    ) = learn_layer_router(
        train,
        orange_groups,
    )

    (
        pine_layer,
        pine_global,
        _,
        _,
    ) = learn_layer_router(
        train,
        pine_groups,
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
        "  request "
        "pine_energy orange_energy oracle_energy "
        "orange/pine router/oracle "
        "pine_cos orange_cos "
        "orange_l2 pine_l2"
    )

    fold_values = {
        fraction: {
            key: []
            for key in (
                "pine_energy",
                "orange_energy",
                "oracle_energy",
                "pine_cos",
                "orange_cos",
                "oracle_cos",
                "pine_l2",
                "orange_l2",
                "oracle_l2",
                "pine_bytes",
                "orange_bytes",
                "oracle_bytes",
            )
        }
        for fraction in REQUEST_FRACTIONS
    }

    for row in test:
        vec = row["residual"]
        layer = row["layer"]

        pine_rank = pine_layer.get(
            layer,
            pine_global,
        )

        orange_rank = orange_layer.get(
            layer,
            orange_global,
        )

        for fraction in REQUEST_FRACTIONS:
            pine_selected = select_indices(
                pine_rank,
                len(pine_groups),
                fraction,
            )

            orange_selected = select_indices(
                orange_rank,
                len(orange_groups),
                fraction,
            )

            oracle_selected = oracle_indices(
                vec,
                orange_groups,
                fraction,
            )

            pine_recon, pine_bytes = (
                reconstruct_selected(
                    vec,
                    pine_groups,
                    pine_selected,
                )
            )

            orange_recon, orange_bytes = (
                reconstruct_selected(
                    vec,
                    orange_groups,
                    orange_selected,
                )
            )

            oracle_recon, oracle_bytes = (
                reconstruct_selected(
                    vec,
                    orange_groups,
                    oracle_selected,
                )
            )

            values = fold_values[fraction]

            values["pine_energy"].append(
                energy_fraction(
                    vec,
                    pine_recon,
                )
            )

            values["orange_energy"].append(
                energy_fraction(
                    vec,
                    orange_recon,
                )
            )

            values["oracle_energy"].append(
                energy_fraction(
                    vec,
                    oracle_recon,
                )
            )

            values["pine_cos"].append(
                cosine(
                    vec,
                    pine_recon,
                )
            )

            values["orange_cos"].append(
                cosine(
                    vec,
                    orange_recon,
                )
            )

            values["oracle_cos"].append(
                cosine(
                    vec,
                    oracle_recon,
                )
            )

            values["pine_l2"].append(
                relative_l2(
                    vec,
                    pine_recon,
                )
            )

            values["orange_l2"].append(
                relative_l2(
                    vec,
                    orange_recon,
                )
            )

            values["oracle_l2"].append(
                relative_l2(
                    vec,
                    oracle_recon,
                )
            )

            values["pine_bytes"].append(
                pine_bytes
            )

            values["orange_bytes"].append(
                orange_bytes
            )

            values["oracle_bytes"].append(
                oracle_bytes
            )

    for fraction in REQUEST_FRACTIONS:
        values = fold_values[fraction]

        pine_energy = mean(
            values["pine_energy"]
        )

        orange_energy = mean(
            values["orange_energy"]
        )

        oracle_energy = mean(
            values["oracle_energy"]
        )

        orange_pine = (
            orange_energy / pine_energy
        )

        router_oracle = (
            orange_energy / oracle_energy
        )

        pine_cos = mean(
            values["pine_cos"]
        )

        orange_cos = mean(
            values["orange_cos"]
        )

        pine_l2 = mean(
            values["pine_l2"]
        )

        orange_l2 = mean(
            values["orange_l2"]
        )

        if (
            orange_energy > pine_energy
            and
            orange_cos >= pine_cos
            and
            orange_l2 <= pine_l2
        ):
            fold_wins[fraction] += 1

        for key in summary[fraction]:
            summary[fraction][key].append(
                mean(values[key])
            )

        print(
            f"  {fraction:7.3f} "
            f"{pine_energy:11.9f} "
            f"{orange_energy:13.9f} "
            f"{oracle_energy:13.9f} "
            f"{orange_pine:11.9f} "
            f"{router_oracle:13.9f} "
            f"{pine_cos:10.8f} "
            f"{orange_cos:10.8f} "
            f"{orange_l2:10.8f} "
            f"{pine_l2:10.8f}"
        )


print()
print("CROSS-FOLD QUANTIZED SUMMARY")
print("-" * 132)

print(
    "request "
    "pine_energy orange_energy oracle_energy "
    "orange/pine router/oracle "
    "pine_cos orange_cos "
    "pine_l2 orange_l2 "
    "bytes/item fold_wins"
)

all_pass = True

for fraction in REQUEST_FRACTIONS:
    values = summary[fraction]

    pine_energy = mean(
        values["pine_energy"]
    )

    orange_energy = mean(
        values["orange_energy"]
    )

    oracle_energy = mean(
        values["oracle_energy"]
    )

    orange_pine = (
        orange_energy / pine_energy
    )

    router_oracle = (
        orange_energy / oracle_energy
    )

    pine_cos = mean(
        values["pine_cos"]
    )

    orange_cos = mean(
        values["orange_cos"]
    )

    pine_l2 = mean(
        values["pine_l2"]
    )

    orange_l2 = mean(
        values["orange_l2"]
    )

    pine_bytes = mean(
        values["pine_bytes"]
    )

    orange_bytes = mean(
        values["orange_bytes"]
    )

    wins = fold_wins[fraction]

    passed = (
        orange_pine > 1.0
        and
        orange_cos >= pine_cos
        and
        orange_l2 <= pine_l2
        and
        wins >= 3
    )

    if not passed:
        all_pass = False

    if abs(
        orange_bytes - pine_bytes
    ) > 1e-9:
        all_pass = False

    print(
        f"{fraction:7.3f} "
        f"{pine_energy:11.9f} "
        f"{orange_energy:13.9f} "
        f"{oracle_energy:13.9f} "
        f"{orange_pine:11.9f} "
        f"{router_oracle:13.9f} "
        f"{pine_cos:10.8f} "
        f"{orange_cos:10.8f} "
        f"{pine_l2:10.8f} "
        f"{orange_l2:10.8f} "
        f"{orange_bytes:10.3f} "
        f"{wins:4d}/4"
    )


print()
print("MODELED STORAGE")
print("-" * 132)

full_blocks_per_item = group_count

block_payload_bytes = (
    GROUP_SIZE + SCALE_BYTES
)

full_quantized_item_bytes = (
    full_blocks_per_item
    * block_payload_bytes
)

pine_full_payload = (
    len(rows)
    * full_quantized_item_bytes
)

orange_full_payload = (
    pine_full_payload
)

orange_total_with_metadata = (
    orange_full_payload
    + orange_map_bytes
    + router_metadata_bytes
)

print(
    f"BLOCK_INT8_64 bytes/block : "
    f"{block_payload_bytes}"
)

print(
    f"full blocks/item          : "
    f"{full_blocks_per_item}"
)

print(
    f"Pine full payload bytes   : "
    f"{pine_full_payload}"
)

print(
    f"Orange full payload bytes : "
    f"{orange_full_payload}"
)

print(
    f"Orange map bytes          : "
    f"{orange_map_bytes}"
)

print(
    f"Orange router bytes       : "
    f"{router_metadata_bytes}"
)

print(
    f"Orange modeled total      : "
    f"{orange_total_with_metadata}"
)

print(
    f"Pine ratio vs flat FP32   : "
    f"{pine_full_payload / flat_fp32_bytes:.9f}"
)

print(
    f"Orange ratio vs flat FP32 : "
    f"{orange_total_with_metadata / flat_fp32_bytes:.9f}"
)

print()
print("FOREST V6 DECISION")
print("-" * 132)

if all_pass:
    print(
        "result                     : "
        "QUANTIZED NON-ORACLE ORANGE PASSES"
    )
else:
    print(
        "result                     : "
        "QUANTIZED ORANGE ADVANTAGE "
        "NOT YET ESTABLISHED"
    )

print()
print("INTERPRETATION BOUNDARY")
print("-" * 132)

print(
    "V6 applies the same BLOCK_INT8_64 quantizer "
    "to Pine and Orange selected groups."
)

print(
    "The Orange grouping and router are trained only "
    "on non-held-out token trajectories."
)

print(
    "Orange grouping-map and router-score metadata "
    "are explicitly modeled."
)

print(
    "This remains an in-memory numerical experiment; "
    "serialization, mmap, filesystem, cache behavior, "
    "and wall-clock retrieval are not yet measured."
)
