#!/usr/bin/env python3

import csv
import math
import statistics

import numpy as np


PATH = "activation_vectors_all_tokens.csv"

EXCLUDED_TOKENS = {0}

BRANCHING = 4
MAX_DEPTH = 6

# Existing V2B winner.
WEDGE_SIZE = 64

# Synthetic partial-access requests.
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
# SHARED TREE CONSTRUCTION
#
# Both species use exactly the same deterministic structural
# partition for Forest V1. This isolates packaging/addressing
# effects from clustering effects.
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
    encoded = np.asarray(
        vector,
        dtype=np.float16,
    )

    return (
        encoded.astype(np.float64),
        encoded.nbytes,
    )


def block_int8_encode(vector, block=WEDGE_SIZE):
    vector = np.asarray(
        vector,
        dtype=np.float64,
    )

    decoded = np.empty_like(vector)

    encoded_blocks = []

    total_bytes = 0

    for start in range(
        0,
        len(vector),
        block,
    ):
        part = vector[
            start:start + block
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

        encoded_blocks.append({
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
        encoded_blocks,
    )


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


# Stable integer IDs for storage metadata.
node_id = {
    id(node): i
    for i, node in enumerate(nodes)
}

leaf_id = {
    id(leaf): i
    for i, leaf in enumerate(leaves)
}


# ============================================================
# SHARED PAYLOAD
#
# Preserve the V2B winner:
#
# root            FP32
# shared nodes    FP16
# terminal items  BLOCK_INT8_64
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


PAYLOAD_BYTES = (
    ROOT_BYTES
    + NODE_BYTES
    + ITEM_BYTES
)

FLAT_FP32_BYTES = (
    len(data)
    * dim
    * 4
)


# ============================================================
# FULL RECONSTRUCTION QUALITY
# ============================================================

full_cosines = []
full_errors = []

for leaf in leaves:
    path = path_from_root(
        leaf
    )

    for item in leaf["items"]:
        reconstructed = (
            root_decoded.copy()
        )

        for node in path[1:]:
            reconstructed += (
                encoded_nodes[id(node)]
            )

        reconstructed += (
            encoded_items[
                id(item)
            ]["decoded"]
        )

        full_cosines.append(
            cosine(
                item["vector"],
                reconstructed,
            )
        )

        full_errors.append(
            relative_l2(
                item["vector"],
                reconstructed,
            )
        )


# ============================================================
# LODGEPOLE TOPOLOGY
#
# trunk     = root
# branches  = shared hierarchy
# needles   = terminal item residuals
# cones     = one package per terminal leaf
# scales    = directory entry for each contained needle
# seeds     = route metadata for each original item
#
# Metadata format for benchmark:
#
# cone:
#   uint16 leaf id
#   uint16 item count
#
# cone scale / directory per item:
#   uint16 local item index
#   uint32 payload offset
#   uint32 payload length
#
# seed per item:
#   uint16 cone id
#   uint16 local item
#   uint16 layer
#   uint16 token
# ============================================================

PINE_CONE_HEADER_BYTES = 4
PINE_SCALE_ENTRY_BYTES = 10
PINE_SEED_BYTES = 8

pine_cone_bytes = (
    len(leaves)
    * PINE_CONE_HEADER_BYTES
)

pine_scale_bytes = (
    len(data)
    * PINE_SCALE_ENTRY_BYTES
)

pine_seed_bytes = (
    len(data)
    * PINE_SEED_BYTES
)

PINE_METADATA_BYTES = (
    pine_cone_bytes
    + pine_scale_bytes
    + pine_seed_bytes
)

PINE_TOTAL_BYTES = (
    PAYLOAD_BYTES
    + PINE_METADATA_BYTES
)


# ============================================================
# ORANGE TOPOLOGY
#
# trunk      = root
# branches   = shared hierarchy
# leaves     = terminal clusters
# fruit      = original representation
# wedges     = BLOCK_INT8_64 terminal blocks
# seeds      = route to fruit
#
# Metadata:
#
# fruit:
#   uint16 leaf id
#   uint16 wedge count
#
# wedge directory:
#   uint16 wedge index
#   uint32 payload offset
#   uint16 payload length
#
# seed:
#   uint16 leaf id
#   uint16 fruit id
#   uint16 layer
#   uint16 token
# ============================================================

ORANGE_FRUIT_HEADER_BYTES = 4
ORANGE_WEDGE_ENTRY_BYTES = 8
ORANGE_SEED_BYTES = 8

wedges_per_full_vector = int(
    math.ceil(
        dim / WEDGE_SIZE
    )
)

orange_fruit_bytes = (
    len(data)
    * ORANGE_FRUIT_HEADER_BYTES
)

orange_wedge_directory_bytes = (
    len(data)
    * wedges_per_full_vector
    * ORANGE_WEDGE_ENTRY_BYTES
)

orange_seed_bytes = (
    len(data)
    * ORANGE_SEED_BYTES
)

ORANGE_METADATA_BYTES = (
    orange_fruit_bytes
    + orange_wedge_directory_bytes
    + orange_seed_bytes
)

ORANGE_TOTAL_BYTES = (
    PAYLOAD_BYTES
    + ORANGE_METADATA_BYTES
)


# ============================================================
# ACCESS BENCHMARK
#
# Pine hypothesis:
# locating one needle requires materializing its complete
# terminal residual payload.
#
# Orange hypothesis:
# a request may address only a subset of fruit wedges.
#
# Both must still touch the shared reconstruction path.
#
# We count:
#   shared path bytes
#   terminal payload bytes
#   relevant directory metadata
#
# This is a deterministic touched-byte model, not yet a
# wall-clock storage engine benchmark.
# ============================================================

def shared_path_bytes(leaf):
    path = path_from_root(
        leaf
    )

    # root FP32 is counted once.
    total = ROOT_BYTES

    for node in path[1:]:
        # FP16 residual.
        total += dim * 2

    return total


pine_access = {
    fraction: []
    for fraction in ACCESS_FRACTIONS
}

orange_access = {
    fraction: []
    for fraction in ACCESS_FRACTIONS
}


for leaf in leaves:
    shared_bytes = shared_path_bytes(
        leaf
    )

    for local_index, item in enumerate(
        leaf["items"]
    ):
        entry = encoded_items[
            id(item)
        ]

        terminal_bytes = entry[
            "bytes"
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

            requested_wedges = min(
                len(blocks),
                int(
                    math.ceil(
                        requested_dimensions
                        / WEDGE_SIZE
                    )
                ),
            )

            # Lodgepole needle retrieval materializes the
            # complete terminal residual.
            pine_touched = (
                shared_bytes
                + terminal_bytes
                + PINE_CONE_HEADER_BYTES
                + PINE_SCALE_ENTRY_BYTES
                + PINE_SEED_BYTES
            )

            # Orange retrieves only addressed wedges.
            orange_terminal = sum(
                block["bytes"]
                for block
                in blocks[:requested_wedges]
            )

            orange_touched = (
                shared_bytes
                + orange_terminal
                + ORANGE_FRUIT_HEADER_BYTES
                + requested_wedges
                * ORANGE_WEDGE_ENTRY_BYTES
                + ORANGE_SEED_BYTES
            )

            pine_access[
                fraction
            ].append(
                pine_touched
            )

            orange_access[
                fraction
            ].append(
                orange_touched
            )


# ============================================================
# PARTIAL WEDGE FIDELITY
#
# Evaluate quantization only on the requested dimensions.
# This avoids pretending an unreconstructed portion of the
# vector should contribute to the partial-access error.
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
            requested_dimensions = max(
                1,
                min(
                    dim,
                    int(
                        math.ceil(
                            dim * fraction
                        )
                    ),
                ),
            )

            requested_wedges = int(
                math.ceil(
                    requested_dimensions
                    / WEDGE_SIZE
                )
            )

            reconstructed = (
                shared_reconstructed[
                    :requested_dimensions
                ].copy()
            )

            for block in entry[
                "blocks"
            ][:requested_wedges]:
                start = block["start"]

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

print("=" * 112)

print(
    " OPENMIND / FOREST TOPOLOGY V1 — "
    "LODGEPOLE VS ORANGE"
)

print("=" * 112)

print()

print("DATASET")
print("-" * 112)

print(
    f"path                      : {PATH}"
)

print(
    f"vectors                   : {len(data)}"
)

print(
    f"dimensions                : {dim}"
)

print(
    f"tree nodes                : {len(nodes)}"
)

print(
    f"terminal leaves           : {len(leaves)}"
)

print(
    f"branching                 : {BRANCHING}"
)

print(
    f"maximum depth             : {MAX_DEPTH}"
)

print(
    f"wedge size                : {WEDGE_SIZE}"
)

print(
    f"wedges / full vector      : "
    f"{wedges_per_full_vector}"
)


print()
print("BIOLOGICAL / COMPUTATIONAL CONTRACT")
print("-" * 112)

print(
    "LODGEPOLE: trunk=root, branches=shared residuals, "
    "needles=terminal residuals, cones=leaf packages, "
    "scales=directory entries, seeds=item routes"
)

print(
    "ORANGE: trunk=root, branches=shared residuals, "
    "leaves=terminal clusters, fruit=item representation, "
    "wedges=64-component blocks, seeds=item routes"
)


print()
print("SHARED ENCODING")
print("-" * 112)

print(
    f"flat FP32 bytes           : "
    f"{FLAT_FP32_BYTES}"
)

print(
    f"root FP32 bytes           : "
    f"{ROOT_BYTES}"
)

print(
    f"FP16 node bytes           : "
    f"{NODE_BYTES}"
)

print(
    f"BLOCK_INT8_64 item bytes  : "
    f"{ITEM_BYTES}"
)

print(
    f"shared encoded payload    : "
    f"{PAYLOAD_BYTES}"
)

print(
    f"payload ratio vs flat     : "
    f"{PAYLOAD_BYTES / FLAT_FP32_BYTES:.9f}"
)

print(
    f"payload saving            : "
    f"{1.0 - PAYLOAD_BYTES / FLAT_FP32_BYTES:.9f}"
)


print()
print("FULL RECONSTRUCTION FIDELITY")
print("-" * 112)

print(
    f"mean cosine               : "
    f"{statistics.mean(full_cosines):.12f}"
)

print(
    f"minimum cosine            : "
    f"{min(full_cosines):.12f}"
)

print(
    f"mean relative L2          : "
    f"{statistics.mean(full_errors):.12f}"
)

print(
    f"maximum relative L2       : "
    f"{max(full_errors):.12f}"
)


print()
print("TOPOLOGY METADATA")
print("-" * 112)

print(
    f"Lodgepole cone headers    : "
    f"{pine_cone_bytes}"
)

print(
    f"Lodgepole scale directory : "
    f"{pine_scale_bytes}"
)

print(
    f"Lodgepole seeds           : "
    f"{pine_seed_bytes}"
)

print(
    f"Lodgepole metadata total  : "
    f"{PINE_METADATA_BYTES}"
)

print(
    f"Lodgepole total bytes     : "
    f"{PINE_TOTAL_BYTES}"
)

print(
    f"Lodgepole ratio vs flat   : "
    f"{PINE_TOTAL_BYTES / FLAT_FP32_BYTES:.9f}"
)

print()

print(
    f"Orange fruit headers      : "
    f"{orange_fruit_bytes}"
)

print(
    f"Orange wedge directory    : "
    f"{orange_wedge_directory_bytes}"
)

print(
    f"Orange seeds              : "
    f"{orange_seed_bytes}"
)

print(
    f"Orange metadata total     : "
    f"{ORANGE_METADATA_BYTES}"
)

print(
    f"Orange total bytes        : "
    f"{ORANGE_TOTAL_BYTES}"
)

print(
    f"Orange ratio vs flat      : "
    f"{ORANGE_TOTAL_BYTES / FLAT_FP32_BYTES:.9f}"
)


print()
print("PARTIAL ACCESS / TOUCHED BYTES")
print("-" * 112)

print(
    "request    pine_mean     orange_mean   "
    "orange/pine   reduction"
)

for fraction in ACCESS_FRACTIONS:
    pine_mean = statistics.mean(
        pine_access[fraction]
    )

    orange_mean = statistics.mean(
        orange_access[fraction]
    )

    ratio = (
        orange_mean
        / pine_mean
    )

    reduction = (
        1.0 - ratio
    )

    print(
        f"{fraction:7.2f} "
        f"{pine_mean:13.3f} "
        f"{orange_mean:13.3f} "
        f"{ratio:12.6f} "
        f"{reduction:11.6f}"
    )


print()
print("ORANGE WEDGE FIDELITY")
print("-" * 112)

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
print("FULL-ACCESS COMPARISON")
print("-" * 112)

pine_full = statistics.mean(
    pine_access[1.0]
)

orange_full = statistics.mean(
    orange_access[1.0]
)

print(
    f"Lodgepole touched bytes   : "
    f"{pine_full:.3f}"
)

print(
    f"Orange touched bytes      : "
    f"{orange_full:.3f}"
)

print(
    f"Orange/Lodgepole          : "
    f"{orange_full / pine_full:.9f}"
)


print()
print("FOREST V1 QUESTIONS")
print("-" * 112)

print(
    "1. Does cone/seed metadata preserve a coherent "
    "Lodgepole packaging model?"
)

print(
    "2. Does wedge addressability reduce touched bytes "
    "for partial retrieval?"
)

print(
    "3. Does wedge-only reconstruction retain the same "
    "quantization quality on addressed dimensions?"
)

print(
    "4. Is Orange's extra wedge-directory metadata worth "
    "its retrieval reduction?"
)


print()
print("INTERPRETATION BOUNDARY")
print("-" * 112)

print(
    "Forest V1 uses structural 64-component wedges."
)

print(
    "It does NOT claim those wedges are semantic facets."
)

print(
    "Both species share identical tree construction and "
    "encoded numerical payload for a fair first comparison."
)

print(
    "Touched-byte results are deterministic access-model "
    "measurements, not yet wall-clock mmap/storage benchmarks."
)

print(
    "A later Forest benchmark may learn or derive semantic "
    "wedges only if this structural experiment justifies it."
)
