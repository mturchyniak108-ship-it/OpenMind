#!/usr/bin/env python3

import csv
import math
import statistics

import numpy as np


PATH = "activation_vectors_all_tokens.csv"

EXCLUDED_TOKENS = {0}

BRANCHING = 4
MAX_DEPTH = 6
BLOCK_SIZE = 64

ACCESS_FRACTIONS = (
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


def path_from_root(node):
    out = []

    cur = node

    while cur is not None:
        out.append(cur)
        cur = cur["parent"]

    return list(reversed(out))


def node_residual(node):
    return (
        node["centroid"]
        - node["parent"]["centroid"]
    )


def item_residual(leaf, item):
    return (
        item["vector"]
        - leaf["centroid"]
    )


# ============================================================
# ENCODING
# ============================================================

def fp16_encode(vector):
    q = np.asarray(
        vector,
        dtype=np.float16,
    )

    return (
        q.astype(np.float64),
        q.nbytes,
    )


def block_int8_encode(vector):
    vector = np.asarray(
        vector,
        dtype=np.float64,
    )

    decoded = np.empty_like(vector)

    blocks = []

    total_bytes = 0

    for start in range(
        0,
        len(vector),
        BLOCK_SIZE,
    ):
        part = vector[
            start:start + BLOCK_SIZE
        ]

        peak = float(
            np.max(np.abs(part))
        )

        if peak == 0.0:
            scale = 1.0

            q = np.zeros(
                part.shape,
                dtype=np.int8,
            )
        else:
            scale = peak / 127.0

            q = np.clip(
                np.rint(part / scale),
                -127,
                127,
            ).astype(np.int8)

        decoded_part = (
            q.astype(np.float64)
            * scale
        )

        decoded[
            start:start + len(part)
        ] = decoded_part

        blocks.append({
            "start": start,
            "length": len(part),
            "decoded": decoded_part,
            "bytes": int(q.nbytes + 4),
        })

        total_bytes += (
            q.nbytes + 4
        )

    return (
        decoded,
        int(total_bytes),
        blocks,
    )


# ============================================================
# LOAD DATA
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

root = build(data)

nodes = list(
    walk(root)
)

non_root_nodes = [
    node
    for node in nodes
    if node["parent"] is not None
]

leaves = [
    node
    for node in nodes
    if not node["children"]
]


# ============================================================
# SHARED V2B NUMERICAL ENCODING
# ============================================================

root_decoded = (
    root["centroid"]
    .astype(np.float32)
    .astype(np.float64)
)

ROOT_BYTES = dim * 4

encoded_nodes = {}

NODE_BYTES = 0

for node in non_root_nodes:
    decoded, nbytes = fp16_encode(
        node_residual(node)
    )

    encoded_nodes[
        id(node)
    ] = decoded

    NODE_BYTES += nbytes


encoded_items = {}

ITEM_BYTES = 0

for leaf in leaves:
    for item in leaf["items"]:
        decoded, nbytes, blocks = (
            block_int8_encode(
                item_residual(
                    leaf,
                    item,
                )
            )
        )

        encoded_items[
            id(item)
        ] = {
            "decoded": decoded,
            "bytes": nbytes,
            "blocks": blocks,
            "leaf": leaf,
        }

        ITEM_BYTES += nbytes


FLAT_FP32_BYTES = (
    len(data)
    * dim
    * 4
)


# ============================================================
# METADATA CONTRACTS
#
# FAIR V2:
#
# Pine block and Orange wedge both get per-block addressing.
# Therefore topology metadata differs only in packaging labels,
# not in block addressability capability.
# ============================================================

PINE_CONE_HEADER_BYTES = 4
PINE_NEEDLE_HEADER_BYTES = 4
PINE_BLOCK_ENTRY_BYTES = 8
PINE_SEED_BYTES = 8

ORANGE_FRUIT_HEADER_BYTES = 4
ORANGE_WEDGE_ENTRY_BYTES = 8
ORANGE_SEED_BYTES = 8


BLOCKS_PER_VECTOR = int(
    math.ceil(
        dim / BLOCK_SIZE
    )
)


PINE_METADATA = (
    len(leaves)
    * PINE_CONE_HEADER_BYTES
    + len(data)
    * PINE_NEEDLE_HEADER_BYTES
    + len(data)
    * BLOCKS_PER_VECTOR
    * PINE_BLOCK_ENTRY_BYTES
    + len(data)
    * PINE_SEED_BYTES
)


ORANGE_METADATA = (
    len(data)
    * ORANGE_FRUIT_HEADER_BYTES
    + len(data)
    * BLOCKS_PER_VECTOR
    * ORANGE_WEDGE_ENTRY_BYTES
    + len(data)
    * ORANGE_SEED_BYTES
)


PAYLOAD_BYTES = (
    ROOT_BYTES
    + NODE_BYTES
    + ITEM_BYTES
)


PINE_TOTAL = (
    PAYLOAD_BYTES
    + PINE_METADATA
)


ORANGE_TOTAL = (
    PAYLOAD_BYTES
    + ORANGE_METADATA
)


# ============================================================
# ACCESS COST
#
# Modes:
#
# PINE_FULL
#   full branch path + complete needle
#
# PINE_BLOCK
#   full branch path + requested needle blocks
#
# ORANGE_WEDGE
#   full branch path + requested wedges
#
# ORANGE_CACHED_WEDGE
#   requested wedges only; common branch representation
#   assumed resident/cached.
#
# Also include PINE_CACHED_BLOCK as fairness control.
# ============================================================

modes = (
    "PINE_FULL",
    "PINE_BLOCK",
    "PINE_CACHED_BLOCK",
    "ORANGE_WEDGE",
    "ORANGE_CACHED_WEDGE",
)

access = {
    mode: {
        fraction: []
        for fraction in ACCESS_FRACTIONS
    }
    for mode in modes
}


def shared_path_bytes(leaf):
    path = path_from_root(
        leaf
    )

    total = ROOT_BYTES

    for node in path[1:]:
        total += dim * 2

    return total


for leaf in leaves:
    shared = shared_path_bytes(
        leaf
    )

    for item in leaf["items"]:
        entry = encoded_items[
            id(item)
        ]

        blocks = entry[
            "blocks"
        ]

        for fraction in ACCESS_FRACTIONS:
            requested_dimensions = max(
                1,
                int(
                    math.ceil(
                        dim * fraction
                    )
                ),
            )

            requested_blocks = min(
                len(blocks),
                int(
                    math.ceil(
                        requested_dimensions
                        / BLOCK_SIZE
                    )
                ),
            )

            partial_payload = sum(
                block["bytes"]
                for block
                in blocks[:requested_blocks]
            )

            full_payload = entry[
                "bytes"
            ]

            pine_full_metadata = (
                PINE_CONE_HEADER_BYTES
                + PINE_NEEDLE_HEADER_BYTES
                + PINE_SEED_BYTES
                + BLOCKS_PER_VECTOR
                * PINE_BLOCK_ENTRY_BYTES
            )

            pine_partial_metadata = (
                PINE_CONE_HEADER_BYTES
                + PINE_NEEDLE_HEADER_BYTES
                + PINE_SEED_BYTES
                + requested_blocks
                * PINE_BLOCK_ENTRY_BYTES
            )

            orange_partial_metadata = (
                ORANGE_FRUIT_HEADER_BYTES
                + ORANGE_SEED_BYTES
                + requested_blocks
                * ORANGE_WEDGE_ENTRY_BYTES
            )

            access[
                "PINE_FULL"
            ][fraction].append(
                shared
                + full_payload
                + pine_full_metadata
            )

            access[
                "PINE_BLOCK"
            ][fraction].append(
                shared
                + partial_payload
                + pine_partial_metadata
            )

            access[
                "PINE_CACHED_BLOCK"
            ][fraction].append(
                partial_payload
                + pine_partial_metadata
            )

            access[
                "ORANGE_WEDGE"
            ][fraction].append(
                shared
                + partial_payload
                + orange_partial_metadata
            )

            access[
                "ORANGE_CACHED_WEDGE"
            ][fraction].append(
                partial_payload
                + orange_partial_metadata
            )


# ============================================================
# FIDELITY
# ============================================================

partial_cosines = {
    fraction: []
    for fraction in ACCESS_FRACTIONS
}

partial_errors = {
    fraction: []
    for fraction in ACCESS_FRACTIONS
}


for leaf in leaves:
    path = path_from_root(
        leaf
    )

    shared_reconstructed = (
        root_decoded.copy()
    )

    for node in path[1:]:
        shared_reconstructed += (
            encoded_nodes[id(node)]
        )

    for item in leaf["items"]:
        entry = encoded_items[
            id(item)
        ]

        for fraction in ACCESS_FRACTIONS:
            requested_dimensions = min(
                dim,
                max(
                    1,
                    int(
                        math.ceil(
                            dim * fraction
                        )
                    ),
                ),
            )

            requested_blocks = int(
                math.ceil(
                    requested_dimensions
                    / BLOCK_SIZE
                )
            )

            reconstructed = (
                shared_reconstructed[
                    :requested_dimensions
                ].copy()
            )

            for block in entry[
                "blocks"
            ][:requested_blocks]:
                start = block[
                    "start"
                ]

                if start >= requested_dimensions:
                    break

                end = min(
                    requested_dimensions,
                    start + block["length"],
                )

                reconstructed[
                    start:end
                ] += block[
                    "decoded"
                ][
                    :end - start
                ]

            original = item[
                "vector"
            ][
                :requested_dimensions
            ]

            partial_cosines[
                fraction
            ].append(
                cosine(
                    original,
                    reconstructed,
                )
            )

            partial_errors[
                fraction
            ].append(
                relative_l2(
                    original,
                    reconstructed,
                )
            )


# ============================================================
# OUTPUT
# ============================================================

print("=" * 120)

print(
    " OPENMIND / FOREST TOPOLOGY V2 — "
    "FAIR BLOCK ADDRESSABILITY"
)

print("=" * 120)

print()

print("DATASET")
print("-" * 120)

print(f"vectors                    : {len(data)}")
print(f"dimensions                 : {dim}")
print(f"tree nodes                 : {len(nodes)}")
print(f"terminal leaves            : {len(leaves)}")
print(f"block/wedge size           : {BLOCK_SIZE}")
print(f"blocks per vector          : {BLOCKS_PER_VECTOR}")


print()
print("PAYLOAD")
print("-" * 120)

print(f"flat FP32 bytes            : {FLAT_FP32_BYTES}")
print(f"shared encoded payload     : {PAYLOAD_BYTES}")

print(
    f"payload saving             : "
    f"{1.0 - PAYLOAD_BYTES / FLAT_FP32_BYTES:.9f}"
)


print()
print("FAIR TOPOLOGY METADATA")
print("-" * 120)

print(f"Lodgepole metadata         : {PINE_METADATA}")
print(f"Lodgepole total            : {PINE_TOTAL}")

print(f"Orange metadata            : {ORANGE_METADATA}")
print(f"Orange total               : {ORANGE_TOTAL}")

print(
    f"Orange minus Lodgepole     : "
    f"{ORANGE_TOTAL - PINE_TOTAL}"
)


print()
print("UNCACHED ACCESS")
print("-" * 120)

print(
    "request    PINE_FULL    PINE_BLOCK   "
    "ORANGE_WEDGE  orange/pineblock"
)

for fraction in ACCESS_FRACTIONS:
    pine_full = statistics.mean(
        access["PINE_FULL"][fraction]
    )

    pine_block = statistics.mean(
        access["PINE_BLOCK"][fraction]
    )

    orange = statistics.mean(
        access["ORANGE_WEDGE"][fraction]
    )

    print(
        f"{fraction:7.2f} "
        f"{pine_full:12.3f} "
        f"{pine_block:12.3f} "
        f"{orange:13.3f} "
        f"{orange / pine_block:16.9f}"
    )


print()
print("CACHED SHARED-PATH ACCESS")
print("-" * 120)

print(
    "request    PINE_CACHED   ORANGE_CACHED   "
    "orange/pine   difference"
)

for fraction in ACCESS_FRACTIONS:
    pine = statistics.mean(
        access[
            "PINE_CACHED_BLOCK"
        ][fraction]
    )

    orange = statistics.mean(
        access[
            "ORANGE_CACHED_WEDGE"
        ][fraction]
    )

    print(
        f"{fraction:7.2f} "
        f"{pine:13.3f} "
        f"{orange:15.3f} "
        f"{orange / pine:12.9f} "
        f"{orange - pine:11.3f}"
    )


print()
print("PARTIAL RECONSTRUCTION FIDELITY")
print("-" * 120)

print(
    "request   mean_cosine   min_cosine    "
    "mean_rel_l2   max_rel_l2"
)

for fraction in ACCESS_FRACTIONS:
    print(
        f"{fraction:7.2f} "
        f"{statistics.mean(partial_cosines[fraction]):13.9f} "
        f"{min(partial_cosines[fraction]):13.9f} "
        f"{statistics.mean(partial_errors[fraction]):13.9f} "
        f"{max(partial_errors[fraction]):13.9f}"
    )


print()
print("FAIRNESS RESULT")
print("-" * 120)

ratios = []

for fraction in ACCESS_FRACTIONS:
    pine = statistics.mean(
        access[
            "PINE_BLOCK"
        ][fraction]
    )

    orange = statistics.mean(
        access[
            "ORANGE_WEDGE"
        ][fraction]
    )

    ratios.append(
        orange / pine
    )

mean_ratio = statistics.mean(
    ratios
)

print(
    f"mean Orange/Pine fair ratio : "
    f"{mean_ratio:.12f}"
)

if abs(
    mean_ratio - 1.0
) <= 0.01:
    print(
        "result                      : "
        "STRUCTURAL ACCESS PARITY"
    )
else:
    print(
        "result                      : "
        "TOPOLOGY ACCESS DIFFERENCE"
    )


print()
print("INTERPRETATION")
print("-" * 120)

print(
    "PINE_BLOCK and ORANGE_WEDGE receive equivalent "
    "64-component terminal addressability."
)

print(
    "If their access costs converge, Forest V1's Orange "
    "advantage came primarily from access granularity."
)

print(
    "Orange should only become a distinct architecture if "
    "future wedges provide useful organization that ordinary "
    "Pine blocks cannot reproduce."
)

print(
    "Possible next test: non-contiguous or learned wedges "
    "derived from representation structure."
)
