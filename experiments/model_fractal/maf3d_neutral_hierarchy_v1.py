#!/usr/bin/env python3

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]

PROTOCOL = (
    ROOT
    / "experiments/data/manifests/"
      "maf3d_neutral_hierarchy_v1_protocol.json"
)

EXPECTED_PROTOCOL_SHA256 = (
    "404a6fbc34f0a1efa3f0147815a2dd6"
    "bca045919c6045722a9f5595f1de39441"
)

DIMENSION = 2048
MAX_DEPTH = 5
DEPTHS = tuple(range(MAX_DEPTH + 1))


def sha256_file(path):
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()


def region(depth, node_id):
    if depth not in DEPTHS:
        raise ValueError("invalid depth")

    node_count = 1 << depth

    if not 0 <= node_id < node_count:
        raise ValueError("invalid node_id")

    width = DIMENSION // node_count
    start = node_id * width
    stop = start + width

    return start, stop


def address(route_id, depth, node_id):
    if not isinstance(route_id, int):
        raise TypeError("route_id must be int")

    region(depth, node_id)

    return route_id, depth, node_id


def build_hierarchy(route_id, vector):
    x = np.asarray(vector)

    if x.dtype != np.float32:
        raise TypeError("input must be float32")

    if x.shape != (DIMENSION,):
        raise ValueError("input shape must be (2048,)")

    if not np.all(np.isfinite(x)):
        raise ValueError("input must be finite")

    hierarchy = {}

    for depth in DEPTHS:
        node_count = 1 << depth

        for node_id in range(node_count):
            start, stop = region(
                depth,
                node_id,
            )

            key = address(
                route_id,
                depth,
                node_id,
            )

            if key in hierarchy:
                raise RuntimeError(
                    "duplicate MAF address"
                )

            if depth == MAX_DEPTH:
                payload = x[start:stop].copy()
            else:
                payload = np.float32(
                    np.mean(
                        x[start:stop],
                        dtype=np.float32,
                    )
                )

            hierarchy[key] = payload

    return hierarchy


def reconstruct(route_id, hierarchy, depth):
    if depth not in DEPTHS:
        raise ValueError("invalid depth")

    out = np.empty(
        DIMENSION,
        dtype=np.float32,
    )

    node_count = 1 << depth

    for node_id in range(node_count):
        start, stop = region(
            depth,
            node_id,
        )

        key = address(
            route_id,
            depth,
            node_id,
        )

        payload = hierarchy[key]

        if depth == MAX_DEPTH:
            leaf = np.asarray(payload)

            if leaf.dtype != np.float32:
                raise RuntimeError(
                    "leaf dtype mismatch"
                )

            if leaf.shape != (stop - start,):
                raise RuntimeError(
                    "leaf shape mismatch"
                )

            out[start:stop] = leaf
        else:
            value = np.float32(payload)

            if not np.isfinite(value):
                raise RuntimeError(
                    "non-finite node mean"
                )

            out[start:stop] = value

    return out


def synthetic_vector():
    index = np.arange(
        DIMENSION,
        dtype=np.float32,
    )

    x = (
        np.sin(index * np.float32(0.013))
        + np.cos(index * np.float32(0.007))
        + index * np.float32(0.0001)
    ).astype(
        np.float32,
        copy=False,
    )

    if x.shape != (DIMENSION,):
        raise RuntimeError(
            "synthetic shape mismatch"
        )

    if not np.all(np.isfinite(x)):
        raise RuntimeError(
            "synthetic vector non-finite"
        )

    return x


def structural_selftest():
    protocol_sha = sha256_file(PROTOCOL)

    if protocol_sha != EXPECTED_PROTOCOL_SHA256:
        raise RuntimeError(
            "protocol SHA mismatch"
        )

    route_id = 17
    x = synthetic_vector()

    hierarchy = build_hierarchy(
        route_id,
        x,
    )

    expected_nodes = sum(
        1 << depth
        for depth in DEPTHS
    )

    if expected_nodes != 63:
        raise RuntimeError(
            "expected-node calculation mismatch"
        )

    if len(hierarchy) != expected_nodes:
        raise RuntimeError(
            "hierarchy node count mismatch"
        )

    if len(set(hierarchy)) != expected_nodes:
        raise RuntimeError(
            "address uniqueness failure"
        )

    coverage = {}

    for depth in DEPTHS:
        spans = []

        for node_id in range(1 << depth):
            spans.append(
                region(
                    depth,
                    node_id,
                )
            )

        cursor = 0

        for start, stop in spans:
            if start != cursor:
                raise RuntimeError(
                    f"coverage gap/overlap depth={depth}"
                )

            if stop <= start:
                raise RuntimeError(
                    "non-positive region width"
                )

            cursor = stop

        if cursor != DIMENSION:
            raise RuntimeError(
                f"incomplete coverage depth={depth}"
            )

        coverage[str(depth)] = cursor

    for depth in range(MAX_DEPTH):
        for node_id in range(1 << depth):
            parent = region(
                depth,
                node_id,
            )

            left = region(
                depth + 1,
                2 * node_id,
            )

            right = region(
                depth + 1,
                2 * node_id + 1,
            )

            if left[0] != parent[0]:
                raise RuntimeError(
                    "left child start mismatch"
                )

            if left[1] != right[0]:
                raise RuntimeError(
                    "child boundary mismatch"
                )

            if right[1] != parent[1]:
                raise RuntimeError(
                    "right child stop mismatch"
                )

    reconstruction = {}

    for depth in DEPTHS:
        y = reconstruct(
            route_id,
            hierarchy,
            depth,
        )

        if y.shape != (DIMENSION,):
            raise RuntimeError(
                "reconstruction shape mismatch"
            )

        if y.dtype != np.float32:
            raise RuntimeError(
                "reconstruction dtype mismatch"
            )

        if not np.all(np.isfinite(y)):
            raise RuntimeError(
                "non-finite reconstruction"
            )

        reconstruction[str(depth)] = {
            "shape": list(y.shape),
            "finite": True,
        }

        if depth == MAX_DEPTH:
            if not np.array_equal(x, y):
                raise RuntimeError(
                    "depth-5 exact reconstruction failure"
                )

            reconstruction[str(depth)][
                "bitwise_exact"
            ] = True

    return {
        "status": "PASS",
        "protocol_sha256": protocol_sha,
        "dimension": DIMENSION,
        "depths": list(DEPTHS),
        "total_nodes": expected_nodes,
        "unique_addresses": len(hierarchy),
        "coverage": coverage,
        "parent_child_union": True,
        "depth5_bitwise_exact": True,
        "all_outputs_finite": True,
        "activation_corpus_accessed": False,
    }


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--selftest",
        action="store_true",
        required=True,
    )

    args = parser.parse_args()

    if args.selftest:
        print(
            json.dumps(
                structural_selftest(),
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
