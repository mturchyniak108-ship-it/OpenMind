#!/usr/bin/env python3

import csv
import hashlib
import json
import struct
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np


DATASET = Path("activation_vectors_all_tokens.csv")

DIM = 1536
GROUP_SIZE = 64
GROUP_COUNT = DIM // GROUP_SIZE
EXCLUDED_TOKENS = {0}

MAGIC = b"OMFRZV1\0"
VERSION = 1

HEADER = struct.Struct("<8s7I32s")

# Header fields:
#
# magic
# version
# dimensions
# group_size
# group_count
# layer_count
# training_rows
# training_tokens
# dataset_sha256_raw[32]


def sha256_file(path):
    h = hashlib.sha256()

    with Path(path).open("rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
            h.update(chunk)

    return h.digest()


def load_rows():
    rows = []

    with DATASET.open(newline="") as f:
        reader = csv.DictReader(f)

        for r in reader:
            token = int(r["token_index"])

            if token in EXCLUDED_TOKENS:
                continue

            dim = int(r["embedding_dimension"])

            if dim != DIM:
                raise RuntimeError(
                    f"unexpected dimension {dim}, expected {DIM}"
                )

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

    if not rows:
        raise RuntimeError("no training rows loaded")

    return rows


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

    unused = set(range(DIM))

    mean_corr = corr.mean(
        axis=1
    )

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
            candidates[
                :GROUP_SIZE - 1
            ]
        )

        for i in members:
            unused.remove(i)

        groups.append(
            np.asarray(
                members,
                dtype=np.uint32,
            )
        )

    if len(groups) != GROUP_COUNT:
        raise RuntimeError(
            "unexpected Orange group count"
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


def learn_router(rows, groups):
    by_layer = defaultdict(list)
    global_values = []

    for row in rows:
        values = group_energies(
            row["residual"],
            groups,
        )

        by_layer[
            row["layer"]
        ].append(values)

        global_values.append(values)

    layers = sorted(
        by_layer
    )

    rankings = []

    for layer in layers:
        mean_energy = np.stack(
            by_layer[layer],
            axis=0,
        ).mean(axis=0)

        ranking = np.argsort(
            -mean_energy,
            kind="stable",
        ).astype(np.uint32)

        rankings.append(
            ranking
        )

    global_mean = np.stack(
        global_values,
        axis=0,
    ).mean(axis=0)

    global_ranking = np.argsort(
        -global_mean,
        kind="stable",
    ).astype(np.uint32)

    return (
        layers,
        rankings,
        global_ranking,
    )


def validate_permutation(
    values,
    expected,
    name,
):
    values = [
        int(x)
        for x in values
    ]

    if sorted(values) != list(
        range(expected)
    ):
        raise RuntimeError(
            f"{name} is not a permutation"
        )


def main():
    if len(sys.argv) != 3:
        raise SystemExit(
            "usage: export_forest_frozen_v1.py "
            "ARTIFACT MANIFEST"
        )

    artifact_path = Path(
        sys.argv[1]
    )

    manifest_path = Path(
        sys.argv[2]
    )

    artifact_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    rows = load_rows()

    tokens = sorted({
        row["token"]
        for row in rows
    })

    raw_matrix = np.stack(
        [
            row["vec"]
            for row in rows
        ],
        axis=0,
    )

    centroid64 = raw_matrix.mean(
        axis=0
    )

    residual_rows = [
        {
            "token": row["token"],
            "layer": row["layer"],
            "residual":
                row["vec"] -
                centroid64,
        }
        for row in rows
    ]

    residual_matrix = np.stack(
        [
            row["residual"]
            for row in residual_rows
        ],
        axis=0,
    )

    groups = correlated_groups(
        residual_matrix
    )

    dimension_map = np.concatenate(
        groups
    ).astype(np.uint32)

    validate_permutation(
        dimension_map,
        DIM,
        "dimension map",
    )

    (
        layers,
        rankings,
        global_ranking,
    ) = learn_router(
        residual_rows,
        groups,
    )

    if len(layers) != 28:
        raise RuntimeError(
            f"expected 28 layers, got {len(layers)}"
        )

    for i, ranking in enumerate(
        rankings
    ):
        validate_permutation(
            ranking,
            GROUP_COUNT,
            f"layer ranking {i}",
        )

    validate_permutation(
        global_ranking,
        GROUP_COUNT,
        "global ranking",
    )

    centroid = centroid64.astype(
        "<f4"
    )

    dimension_map = dimension_map.astype(
        "<u4"
    )

    layer_ids = np.asarray(
        layers,
        dtype="<u4",
    )

    rankings_array = np.stack(
        rankings,
        axis=0,
    ).astype("<u4")

    global_ranking = (
        global_ranking
        .astype("<u4")
    )

    dataset_hash_raw = sha256_file(
        DATASET
    )

    header = HEADER.pack(
        MAGIC,
        VERSION,
        DIM,
        GROUP_SIZE,
        GROUP_COUNT,
        len(layers),
        len(rows),
        len(tokens),
        dataset_hash_raw,
    )

    with artifact_path.open(
        "wb"
    ) as f:
        f.write(header)

        f.write(
            centroid.tobytes(
                order="C"
            )
        )

        f.write(
            dimension_map.tobytes(
                order="C"
            )
        )

        f.write(
            layer_ids.tobytes(
                order="C"
            )
        )

        f.write(
            rankings_array.tobytes(
                order="C"
            )
        )

        f.write(
            global_ranking.tobytes(
                order="C"
            )
        )

    artifact_sha = hashlib.sha256(
        artifact_path.read_bytes()
    ).hexdigest()

    dataset_sha = (
        dataset_hash_raw.hex()
    )

    expected_bytes = (
        HEADER.size
        + DIM * 4
        + DIM * 4
        + len(layers) * 4
        + len(layers)
        * GROUP_COUNT
        * 4
        + GROUP_COUNT * 4
    )

    actual_bytes = (
        artifact_path.stat().st_size
    )

    if actual_bytes != expected_bytes:
        raise RuntimeError(
            "artifact size mismatch: "
            f"{actual_bytes} != "
            f"{expected_bytes}"
        )

    manifest = {
        "schema":
            "openmind.forest_frozen.v1",

        "status":
            "frozen_training_artifact",

        "artifact": {
            "path":
                str(artifact_path),

            "sha256":
                artifact_sha,

            "bytes":
                actual_bytes,

            "header_bytes":
                HEADER.size,
        },

        "training": {
            "dataset":
                str(DATASET),

            "dataset_sha256":
                dataset_sha,

            "rows":
                len(rows),

            "tokens":
                tokens,

            "token_count":
                len(tokens),

            "excluded_tokens":
                sorted(
                    EXCLUDED_TOKENS
                ),
        },

        "geometry": {
            "dimensions":
                DIM,

            "group_size":
                GROUP_SIZE,

            "group_count":
                GROUP_COUNT,

            "layers":
                layers,

            "layer_count":
                len(layers),
        },

        "encoding": {
            "endianness":
                "little",

            "centroid":
                "float32[1536]",

            "dimension_map":
                "uint32[1536]",

            "layer_ids":
                "uint32[28]",

            "layer_rankings":
                "uint32[28][24]",

            "global_ranking":
                "uint32[24]",
        },

        "scientific_contract": {
            "live_activation_used_for_training":
                False,

            "live_routing_feedback":
                False,

            "intended_next_use":
                "Forest V9 shadow activation integration",
        },
    }

    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    print(
        "=" * 72
    )

    print(
        " OPENMIND / FOREST FROZEN V1"
    )

    print(
        "=" * 72
    )

    print()

    print(
        f"training rows        : {len(rows)}"
    )

    print(
        f"training tokens      : {len(tokens)}"
    )

    print(
        f"layers               : {len(layers)}"
    )

    print(
        f"dimensions           : {DIM}"
    )

    print(
        f"group size           : {GROUP_SIZE}"
    )

    print(
        f"group count          : {GROUP_COUNT}"
    )

    print(
        f"header bytes         : {HEADER.size}"
    )

    print(
        f"artifact bytes       : {actual_bytes}"
    )

    print(
        f"dataset sha256       : {dataset_sha}"
    )

    print(
        f"artifact sha256      : {artifact_sha}"
    )

    print()

    print(
        "dimension map       : VALID PERMUTATION"
    )

    print(
        "layer rankings      : VALID PERMUTATIONS"
    )

    print(
        "global ranking      : VALID PERMUTATION"
    )

    print()

    print(
        "result              : FOREST FROZEN V1 CREATED"
    )


if __name__ == "__main__":
    main()
