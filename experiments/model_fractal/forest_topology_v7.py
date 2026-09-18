#!/usr/bin/env python3

import csv
import math
import os
import random
import statistics
import struct
import time
from collections import defaultdict
from pathlib import Path

import numpy as np


SOURCE = Path("activation_vectors_all_tokens.csv")

OUT_DIR = Path("results/forest_topology_v7")
PINE_BIN = OUT_DIR / "pine_v7.bin"
ORANGE_BIN = OUT_DIR / "orange_v7.bin"

SEED = 1337
GROUP_SIZE = 64
EXCLUDED_TOKENS = {0}

REQUEST_FRACTIONS = (
    0.125,
    0.250,
    0.500,
    0.750,
    1.000,
)

REPEATS = 40

MAGIC_PINE = b"OMPNV7\0\0"
MAGIC_ORANGE = b"OMORV7\0\0"

VERSION = 1

HEADER = struct.Struct("<8sIIIIQQQQ")
INDEX_ENTRY = struct.Struct("<iiQ")
BLOCK_SCALE = struct.Struct("<f")

SCALE_BYTES = 4


def load_vectors():
    rows = []

    with SOURCE.open(newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            token = int(row["token_index"])

            if token in EXCLUDED_TOKENS:
                continue

            dim = int(row["embedding_dimension"])

            rows.append({
                "layer": int(row["layer"]),
                "token": token,
                "vec": np.asarray(
                    [
                        float(row[f"v{i}"])
                        for i in range(dim)
                    ],
                    dtype=np.float64,
                ),
            })

    return rows


def contiguous_groups(dim):
    return [
        np.arange(
            start,
            min(start + GROUP_SIZE, dim),
            dtype=np.int32,
        )
        for start in range(0, dim, GROUP_SIZE)
    ]


def correlated_groups(matrix):
    corr = np.corrcoef(
        matrix,
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

    dim = matrix.shape[1]
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


def quantize_block(values):
    values = np.asarray(
        values,
        dtype=np.float64,
    )

    peak = float(
        np.max(
            np.abs(values)
        )
    )

    if peak == 0.0:
        scale = 0.0
        q = np.zeros(
            values.size,
            dtype=np.int8,
        )
    else:
        scale = peak / 127.0

        q = np.clip(
            np.rint(values / scale),
            -127,
            127,
        ).astype(np.int8)

    return scale, q


def decode_block(blob):
    scale = BLOCK_SCALE.unpack_from(
        blob,
        0,
    )[0]

    q = np.frombuffer(
        blob,
        dtype=np.int8,
        offset=SCALE_BYTES,
    ).astype(np.float64)

    return q * scale


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

    for row in rows:
        by_layer[row["layer"]].append(
            group_energies(
                row["residual"],
                groups,
            )
        )

    rankings = {}

    for layer, values in by_layer.items():
        mean_energy = np.stack(
            values,
            axis=0,
        ).mean(axis=0)

        rankings[layer] = np.argsort(
            -mean_energy,
            kind="stable",
        ).astype(np.int32)

    return rankings


def prepare_rows(raw):
    matrix = np.stack(
        [
            row["vec"]
            for row in raw
        ],
        axis=0,
    )

    centroid = matrix.mean(
        axis=0
    )

    rows = []

    for row in raw:
        rows.append({
            "layer": row["layer"],
            "token": row["token"],
            "residual": row["vec"] - centroid,
        })

    return rows, centroid


def write_file(
    path,
    magic,
    rows,
    groups,
    router,
    explicit_map,
):
    dim = len(rows[0]["residual"])
    group_count = len(groups)

    block_bytes = (
        GROUP_SIZE + SCALE_BYTES
    )

    index_bytes = (
        len(rows)
        * INDEX_ENTRY.size
    )

    map_bytes = (
        dim * 2
        if explicit_map
        else 0
    )

    layers = sorted(router)

    router_bytes = (
        len(layers)
        * group_count
        * 2
    )

    header_bytes = HEADER.size

    index_offset = header_bytes
    map_offset = index_offset + index_bytes
    router_offset = map_offset + map_bytes
    payload_offset = router_offset + router_bytes

    item_bytes = (
        group_count
        * block_bytes
    )

    with path.open("wb") as f:
        f.write(
            HEADER.pack(
                magic,
                VERSION,
                len(rows),
                dim,
                group_count,
                index_offset,
                map_offset,
                router_offset,
                payload_offset,
            )
        )

        for item_index, row in enumerate(rows):
            offset = (
                payload_offset
                + item_index * item_bytes
            )

            f.write(
                INDEX_ENTRY.pack(
                    row["layer"],
                    row["token"],
                    offset,
                )
            )

        if explicit_map:
            for group in groups:
                for dimension in group:
                    f.write(
                        struct.pack(
                            "<H",
                            int(dimension),
                        )
                    )

        for layer in layers:
            ranking = router[layer]

            for group_index in ranking:
                f.write(
                    struct.pack(
                        "<H",
                        int(group_index),
                    )
                )

        for row in rows:
            vec = row["residual"]

            for group in groups:
                values = vec[group]

                scale, q = quantize_block(
                    values
                )

                f.write(
                    BLOCK_SCALE.pack(scale)
                )

                f.write(
                    q.tobytes()
                )

    return {
        "block_bytes": block_bytes,
        "item_bytes": item_bytes,
        "index_bytes": index_bytes,
        "map_bytes": map_bytes,
        "router_bytes": router_bytes,
        "payload_offset": payload_offset,
    }


def read_header(fd):
    blob = os.pread(
        fd,
        HEADER.size,
        0,
    )

    return HEADER.unpack(blob)


def read_index(fd, count, offset):
    items = []

    for i in range(count):
        blob = os.pread(
            fd,
            INDEX_ENTRY.size,
            offset + i * INDEX_ENTRY.size,
        )

        layer, token, payload = (
            INDEX_ENTRY.unpack(blob)
        )

        items.append({
            "layer": layer,
            "token": token,
            "payload": payload,
        })

    return items


def read_router(
    fd,
    offset,
    layers,
    group_count,
):
    router = {}

    cursor = offset

    for layer in layers:
        values = []

        for _ in range(group_count):
            blob = os.pread(
                fd,
                2,
                cursor,
            )

            cursor += 2

            values.append(
                struct.unpack(
                    "<H",
                    blob,
                )[0]
            )

        router[layer] = values

    return router


def read_group_map(
    fd,
    offset,
    dim,
):
    values = np.empty(
        dim,
        dtype=np.int32,
    )

    cursor = offset

    for i in range(dim):
        blob = os.pread(
            fd,
            2,
            cursor,
        )

        cursor += 2

        values[i] = struct.unpack(
            "<H",
            blob,
        )[0]

    return [
        values[
            start:start + GROUP_SIZE
        ].copy()
        for start in range(
            0,
            dim,
            GROUP_SIZE,
        )
    ]


def timed_read(
    fd,
    entry,
    ranking,
    groups,
    fraction,
    block_bytes,
):
    group_count = len(groups)

    k = max(
        1,
        math.ceil(
            group_count * fraction
        ),
    )

    selected = [
        int(x)
        for x in ranking[:k]
    ]

    reconstructed = np.zeros(
        sum(len(g) for g in groups),
        dtype=np.float64,
    )

    touched = 0

    start = time.perf_counter_ns()

    for group_index in selected:
        offset = (
            entry["payload"]
            + group_index * block_bytes
        )

        blob = os.pread(
            fd,
            block_bytes,
            offset,
        )

        touched += len(blob)

        values = decode_block(blob)

        reconstructed[
            groups[group_index]
        ] = values

    elapsed = (
        time.perf_counter_ns()
        - start
    )

    return (
        elapsed,
        touched,
        reconstructed,
    )


raw = load_vectors()

if not raw:
    raise RuntimeError(
        "no vectors loaded"
    )

rows, centroid = prepare_rows(raw)

dim = len(rows[0]["residual"])

pine_groups = contiguous_groups(dim)

matrix = np.stack(
    [
        row["residual"]
        for row in rows
    ],
    axis=0,
)

orange_groups = correlated_groups(
    matrix
)

pine_router = learn_router(
    rows,
    pine_groups,
)

orange_router = learn_router(
    rows,
    orange_groups,
)

OUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

pine_meta = write_file(
    PINE_BIN,
    MAGIC_PINE,
    rows,
    pine_groups,
    pine_router,
    explicit_map=False,
)

orange_meta = write_file(
    ORANGE_BIN,
    MAGIC_ORANGE,
    rows,
    orange_groups,
    orange_router,
    explicit_map=True,
)

pine_size = PINE_BIN.stat().st_size
orange_size = ORANGE_BIN.stat().st_size

pine_fd = os.open(
    PINE_BIN,
    os.O_RDONLY,
)

orange_fd = os.open(
    ORANGE_BIN,
    os.O_RDONLY,
)

try:
    (
        pine_magic,
        pine_version,
        pine_count,
        pine_dim,
        pine_group_count,
        pine_index_offset,
        pine_map_offset,
        pine_router_offset,
        pine_payload_offset,
    ) = read_header(pine_fd)

    (
        orange_magic,
        orange_version,
        orange_count,
        orange_dim,
        orange_group_count,
        orange_index_offset,
        orange_map_offset,
        orange_router_offset,
        orange_payload_offset,
    ) = read_header(orange_fd)

    pine_index = read_index(
        pine_fd,
        pine_count,
        pine_index_offset,
    )

    orange_index = read_index(
        orange_fd,
        orange_count,
        orange_index_offset,
    )

    layers = sorted({
        row["layer"]
        for row in rows
    })

    pine_router_disk = read_router(
        pine_fd,
        pine_router_offset,
        layers,
        pine_group_count,
    )

    orange_router_disk = read_router(
        orange_fd,
        orange_router_offset,
        layers,
        orange_group_count,
    )

    orange_groups_disk = read_group_map(
        orange_fd,
        orange_map_offset,
        orange_dim,
    )

    rng = random.Random(SEED)

    order = list(
        range(len(rows))
    )

    rng.shuffle(order)

    print("=" * 132)
    print(
        " OPENMIND / FOREST TOPOLOGY V7 "
        "— SERIALIZED INDEXED PARTIAL READS"
    )
    print("=" * 132)

    print()
    print("SERIALIZED FORMAT")
    print("-" * 132)

    print(f"vectors                    : {len(rows)}")
    print(f"dimensions                 : {dim}")
    print(f"groups                     : {len(pine_groups)}")
    print(f"group size                 : {GROUP_SIZE}")
    print(f"block bytes                : {pine_meta['block_bytes']}")
    print(f"index entry bytes          : {INDEX_ENTRY.size}")
    print(f"header bytes               : {HEADER.size}")

    print()
    print("ACTUAL FILE STORAGE")
    print("-" * 132)

    print(f"Pine file bytes            : {pine_size}")
    print(f"Orange file bytes          : {orange_size}")
    print(
        f"Orange minus Pine          : "
        f"{orange_size - pine_size}"
    )
    print(
        f"Orange/Pine file ratio     : "
        f"{orange_size / pine_size:.9f}"
    )

    print(
        f"Pine index bytes           : "
        f"{pine_meta['index_bytes']}"
    )
    print(
        f"Orange index bytes         : "
        f"{orange_meta['index_bytes']}"
    )
    print(
        f"Orange map bytes           : "
        f"{orange_meta['map_bytes']}"
    )
    print(
        f"Pine router bytes          : "
        f"{pine_meta['router_bytes']}"
    )
    print(
        f"Orange router bytes        : "
        f"{orange_meta['router_bytes']}"
    )

    print()
    print("WARM INDEXED PARTIAL READ BENCHMARK")
    print("-" * 132)

    print(
        "request  "
        "pine_mean_ns orange_mean_ns "
        "orange/pine "
        "pine_bytes orange_bytes "
        "pine_p50_ns orange_p50_ns"
    )

    benchmark_rows = []

    for fraction in REQUEST_FRACTIONS:
        pine_times = []
        orange_times = []

        pine_touched = []
        orange_touched = []

        for _ in range(REPEATS):
            for item_index in order:
                pine_entry = (
                    pine_index[item_index]
                )

                orange_entry = (
                    orange_index[item_index]
                )

                layer = pine_entry["layer"]

                elapsed, touched, _ = (
                    timed_read(
                        pine_fd,
                        pine_entry,
                        pine_router_disk[layer],
                        pine_groups,
                        fraction,
                        pine_meta["block_bytes"],
                    )
                )

                pine_times.append(elapsed)
                pine_touched.append(touched)

                elapsed, touched, _ = (
                    timed_read(
                        orange_fd,
                        orange_entry,
                        orange_router_disk[layer],
                        orange_groups_disk,
                        fraction,
                        orange_meta["block_bytes"],
                    )
                )

                orange_times.append(elapsed)
                orange_touched.append(touched)

        pine_mean = statistics.mean(
            pine_times
        )

        orange_mean = statistics.mean(
            orange_times
        )

        pine_p50 = statistics.median(
            pine_times
        )

        orange_p50 = statistics.median(
            orange_times
        )

        pine_bytes = statistics.mean(
            pine_touched
        )

        orange_bytes = statistics.mean(
            orange_touched
        )

        ratio = (
            orange_mean / pine_mean
        )

        benchmark_rows.append({
            "fraction": fraction,
            "pine_mean": pine_mean,
            "orange_mean": orange_mean,
            "ratio": ratio,
            "pine_bytes": pine_bytes,
            "orange_bytes": orange_bytes,
        })

        print(
            f"{fraction:7.3f} "
            f"{pine_mean:12.1f} "
            f"{orange_mean:14.1f} "
            f"{ratio:11.6f} "
            f"{pine_bytes:10.1f} "
            f"{orange_bytes:12.1f} "
            f"{pine_p50:11.1f} "
            f"{orange_p50:13.1f}"
        )

    print()
    print("SERIALIZATION VALIDATION")
    print("-" * 132)

    print(
        "Pine magic                 : "
        + (
            "PASS"
            if pine_magic == MAGIC_PINE
            else "FAIL"
        )
    )

    print(
        "Orange magic               : "
        + (
            "PASS"
            if orange_magic == MAGIC_ORANGE
            else "FAIL"
        )
    )

    print(
        "Pine item count            : "
        + (
            "PASS"
            if pine_count == len(rows)
            else "FAIL"
        )
    )

    print(
        "Orange item count          : "
        + (
            "PASS"
            if orange_count == len(rows)
            else "FAIL"
        )
    )

    print(
        "Orange map roundtrip       : "
        + (
            "PASS"
            if all(
                np.array_equal(a, b)
                for a, b in zip(
                    orange_groups,
                    orange_groups_disk,
                )
            )
            else "FAIL"
        )
    )

    same_bytes = all(
        abs(
            row["pine_bytes"]
            - row["orange_bytes"]
        ) < 1e-9
        for row in benchmark_rows
    )

    print(
        "equal requested bytes      : "
        + (
            "PASS"
            if same_bytes
            else "FAIL"
        )
    )

    print()
    print("FOREST V7 DECISION")
    print("-" * 132)

    print(
        "result                     : "
        "REAL SERIALIZATION AND INDEXED READS EXECUTED"
    )

    print()
    print("INTERPRETATION BOUNDARY")
    print("-" * 132)

    print(
        "V7 writes real binary Pine and Orange artifacts "
        "and uses os.pread() for indexed terminal reads."
    )

    print(
        "Pine and Orange request the same quantized block "
        "bytes at each access fraction."
    )

    print(
        "The benchmark is warm/page-cache influenced and "
        "does not claim controlled cold-storage latency."
    )

    print(
        "The Orange geometry/router in V7 are trained on "
        "the full experimental residual set because V7 "
        "isolates serialization and access-engine cost."
    )

    print(
        "Held-out generalization remains established by "
        "Forest V4-V6, not by this storage benchmark."
    )

finally:
    os.close(pine_fd)
    os.close(orange_fd)
