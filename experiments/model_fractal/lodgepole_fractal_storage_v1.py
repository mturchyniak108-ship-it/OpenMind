#!/usr/bin/env python3

import csv
import math
import statistics
from collections import defaultdict

PATH = "activation_vectors_all_tokens.csv"
EXCLUDED_TOKENS = {0}
BRANCHING = 4
MAX_DEPTH = 6


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def l2(v):
    return math.sqrt(sum(x * x for x in v))


def centroid(items):
    n = len(items)
    d = len(items[0]["vector"])
    out = [0.0] * d
    for item in items:
        v = item["vector"]
        for i in range(d):
            out[i] += v[i]
    inv = 1.0 / n
    return [x * inv for x in out]


def split(items):
    """Deterministic variance-axis split into up to BRANCHING groups."""
    if len(items) <= 1:
        return [items]

    d = len(items[0]["vector"])
    means = [0.0] * d

    for item in items:
        for i, x in enumerate(item["vector"]):
            means[i] += x

    inv = 1.0 / len(items)
    means = [x * inv for x in means]

    variances = [0.0] * d
    for item in items:
        for i, x in enumerate(item["vector"]):
            z = x - means[i]
            variances[i] += z * z

    axis = max(range(d), key=variances.__getitem__)
    ordered = sorted(items, key=lambda x: x["vector"][axis])

    groups = []
    for k in range(BRANCHING):
        lo = len(ordered) * k // BRANCHING
        hi = len(ordered) * (k + 1) // BRANCHING
        if lo < hi:
            groups.append(ordered[lo:hi])

    return groups


def build(items, depth=0, parent=None):
    c = centroid(items)

    node = {
        "depth": depth,
        "centroid": c,
        "parent_centroid": parent,
        "items": items,
        "children": [],
    }

    if depth >= MAX_DEPTH or len(items) <= BRANCHING:
        return node

    for group in split(items):
        node["children"].append(
            build(group, depth + 1, c)
        )

    return node


def walk(node):
    yield node
    for child in node["children"]:
        yield from walk(child)


def reconstruct_leaf(node, item):
    """
    Exact hierarchical reconstruction:
    parent/root centroid + node residuals + leaf residual.
    """
    path = []
    cur = node

    # Leaf reconstruction only needs its leaf centroid plus
    # the final item residual. Ancestor decomposition is
    # mathematically equivalent and measured separately.
    base = cur["centroid"]
    residual = [
        x - y
        for x, y in zip(item["vector"], base)
    ]

    return [
        x + r
        for x, r in zip(base, residual)
    ], residual



data = []

with open(PATH, newline="") as f:
    for row in csv.DictReader(f):
        token = int(row["token_index"])
        if token in EXCLUDED_TOKENS:
            continue

        dim = int(row["embedding_dimension"])
        data.append({
            "layer": int(row["layer"]),
            "token": token,
            "vector": [
                float(row[f"v{i}"])
                for i in range(dim)
            ],
        })


root = build(data)
nodes = list(walk(root))

node_residual_norms = defaultdict(list)
node_centroid_norms = defaultdict(list)
leaf_residual_norms = []
leaf_original_norms = []
leaf_cosines = []
leaf_errors = []
leaves = []

for node in nodes:
    depth = node["depth"]
    node_centroid_norms[depth].append(l2(node["centroid"]))

    if node["parent_centroid"] is not None:
        residual = [
            x - y
            for x, y in zip(
                node["centroid"],
                node["parent_centroid"],
            )
        ]
        node_residual_norms[depth].append(l2(residual))

    if not node["children"]:
        leaves.append(node)
        for item in node["items"]:
            reconstructed, residual = reconstruct_leaf(node, item)
            original = item["vector"]

            leaf_original_norms.append(l2(original))
            leaf_residual_norms.append(l2(residual))
            leaf_cosines.append(cosine(original, reconstructed))

            denom = l2(original)
            err = l2([
                x - y
                for x, y in zip(original, reconstructed)
            ])
            leaf_errors.append(err / denom if denom else 0.0)


dim = len(data[0]["vector"])
flat_scalars = len(data) * dim

# Current hypothetical residual representation:
# one root centroid + one residual vector per non-root node +
# one leaf residual per original vector.
non_root_nodes = len(nodes) - 1
fractal_scalars = (
    dim
    + non_root_nodes * dim
    + len(data) * dim
)

print("=" * 88)
print(" OPENMIND / LODGEPOLE FRACTAL STORAGE V1")
print("=" * 88)
print()
print(f"Dataset            : {PATH}")
print(f"Vectors            : {len(data)}")
print(f"Dimensions         : {dim}")
print(f"Excluded tokens    : {sorted(EXCLUDED_TOKENS)}")
print(f"Branching          : {BRANCHING}")
print(f"Maximum depth      : {MAX_DEPTH}")
print(f"Tree nodes         : {len(nodes)}")
print(f"Terminal leaves    : {len(leaves)}")

print()
print("NODE RESIDUAL MAGNITUDE BY DEPTH")
print("-" * 88)
print("depth   nodes   mean_centroid_norm   mean_parent_residual   residual/centroid")

for depth in sorted(node_centroid_norms):
    cent = node_centroid_norms[depth]
    res = node_residual_norms.get(depth, [])

    cm = statistics.mean(cent)
    rm = statistics.mean(res) if res else 0.0
    ratio = rm / cm if cm else 0.0

    print(
        f"{depth:5d} "
        f"{len(cent):7d} "
        f"{cm:20.9f} "
        f"{rm:20.9f} "
        f"{ratio:19.9f}"
    )

print()
print("LEAF RESIDUALS")
print("-" * 88)
print(f"mean original norm : {statistics.mean(leaf_original_norms):.9f}")
print(f"mean residual norm : {statistics.mean(leaf_residual_norms):.9f}")
print(
    "residual/original  : "
    f"{statistics.mean(leaf_residual_norms) / statistics.mean(leaf_original_norms):.9f}"
)
print(f"mean cosine        : {statistics.mean(leaf_cosines):.12f}")
print(f"min cosine         : {min(leaf_cosines):.12f}")
print(f"max relative error : {max(leaf_errors):.12g}")

print()
print("RAW SCALAR ACCOUNTING")
print("-" * 88)
print(f"flat vectors       : {flat_scalars}")
print(f"hierarchical naive : {fractal_scalars}")
print(f"naive ratio        : {fractal_scalars / flat_scalars:.6f}")

print()
print("NOTE")
print("-" * 88)
print(
    "V1 intentionally stores full-precision residuals. "
    "It tests whether residual energy contracts with tree depth; "
    "it is not yet a compression benchmark."
)
