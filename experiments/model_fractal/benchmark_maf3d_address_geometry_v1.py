#!/usr/bin/env python3

import argparse
import gc
import hashlib
import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = ROOT / "experiments/data/manifests/maf3d_address_geometry_v1_protocol.json"
CLARIFICATION = ROOT / "experiments/data/manifests/maf3d_address_geometry_v1_preexecution_clarification.json"
RESULT_DIR = ROOT / "results/maf3d_address_geometry_v1"
RESULT_FILE = RESULT_DIR / "maf3d_address_geometry_v1_result.json"

ROUTE_BITS = 21
DEPTH_BITS = 5
NODE_BITS = 21

ROUTE_MASK = (1 << ROUTE_BITS) - 1
DEPTH_MASK = (1 << DEPTH_BITS) - 1
NODE_MASK = (1 << NODE_BITS) - 1

# 7-bit -> 21-bit expansion with two zero bits between source bits.
SPREAD7 = tuple(
    sum(
        ((value >> bit) & 1) << (3 * bit)
        for bit in range(7)
    )
    for value in range(128)
)


def coordinate(index):
    """Deterministic unique route/depth/node coordinate for index < 2^20."""
    if not 0 <= index < 1_000_000:
        raise ValueError("benchmark index outside preregistered range")

    route = index >> 15
    depth = (index >> 10) & DEPTH_MASK
    node = index & 1023

    return route, depth, node


def packed_key(route, depth, node):
    if route & ~ROUTE_MASK:
        raise ValueError("route overflow")
    if depth & ~DEPTH_MASK:
        raise ValueError("depth overflow")
    if node & ~NODE_MASK:
        raise ValueError("node overflow")

    return (
        route
        | (depth << ROUTE_BITS)
        | (node << (ROUTE_BITS + DEPTH_BITS))
    )


def spread21(value):
    if value < 0 or value > ROUTE_MASK:
        raise ValueError("Morton coordinate overflow")

    return (
        SPREAD7[value & 127]
        | (SPREAD7[(value >> 7) & 127] << 21)
        | (SPREAD7[(value >> 14) & 127] << 42)
    )


def morton3d_key(route, depth, node):
    return (
        spread21(route)
        | (spread21(depth) << 1)
        | (spread21(node) << 2)
    )


def selftest():
    with PROTOCOL.open(encoding="utf-8") as f:
        protocol = json.load(f)

    if protocol["coordinate_contract"]["morton_key_bits"] != 63:
        raise RuntimeError("protocol Morton width mismatch")

    samples = (0, 1, 31, 32, 1023, 1024, 32767, 32768, 999999)

    coords = [coordinate(i) for i in samples]

    if len(set(coords)) != len(coords):
        raise RuntimeError("coordinate collision")

    tuple_keys = set(coords)
    packed = {packed_key(*c) for c in coords}
    morton = {morton3d_key(*c) for c in coords}

    if len(tuple_keys) != len(samples):
        raise RuntimeError("tuple key collision")
    if len(packed) != len(samples):
        raise RuntimeError("packed key collision")
    if len(morton) != len(samples):
        raise RuntimeError("Morton key collision")

    return coords



SIZES = (1000, 10000, 100000, 1000000)
QUERY_COUNT = 4096
QUERY_START = 104729
QUERY_STRIDE = 7919
REPEATS = 20
WARMUPS = 2

CANDIDATES = (
    "tuple_maf",
    "packed_integer",
    "morton3d",
    "nested_dict_control",
)


def query_indices(size):
    if size not in SIZES:
        raise ValueError("unexpected benchmark size")

    return tuple(
        (QUERY_START + QUERY_STRIDE * j) % size
        for j in range(QUERY_COUNT)
    )


def encode_key(kind, route, depth, node):
    if kind == "tuple_maf":
        return (route, depth, node)

    if kind == "packed_integer":
        return packed_key(route, depth, node)

    if kind == "morton3d":
        return morton3d_key(route, depth, node)

    if kind == "nested_dict_control":
        return (route, depth, node)

    raise ValueError(f"unknown candidate {kind}")


def build_table(kind, size):
    if size <= 0 or size > 1_000_000:
        raise ValueError("invalid table size")

    if kind == "nested_dict_control":
        table = {}

        for index in range(size):
            route, depth, node = coordinate(index)

            level1 = table.setdefault(route, {})
            level2 = level1.setdefault(depth, {})
            level2[node] = index

        return table

    table = {}

    for index in range(size):
        route, depth, node = coordinate(index)

        table[
            encode_key(
                kind,
                route,
                depth,
                node,
            )
        ] = index

    return table


def lookup_key(table, kind, key):
    if kind == "nested_dict_control":
        route, depth, node = key
        return table[route][depth][node]

    return table[key]


def correctness_selftest():
    coords = selftest()

    for kind in CANDIDATES:
        table = build_table(kind, 1000)

        for index in (
            0,
            1,
            31,
            32,
            511,
            999,
        ):
            coord = coordinate(index)
            key = encode_key(kind, *coord)

            if lookup_key(table, kind, key) != index:
                raise RuntimeError(
                    f"{kind} lookup mismatch at {index}"
                )

    q = query_indices(1000)

    if len(q) != QUERY_COUNT:
        raise RuntimeError("query-count mismatch")

    return coords



def timed_lookup_only(
    table,
    kind,
    keys,
    expected_checksum,
):
    timings = []

    for repeat in range(WARMUPS + REPEATS):
        checksum = 0

        start = time.perf_counter_ns()

        for key in keys:
            checksum += lookup_key(
                table,
                kind,
                key,
            )

        elapsed = (
            time.perf_counter_ns()
            - start
        )

        if checksum != expected_checksum:
            raise RuntimeError(
                f"{kind} lookup-only checksum mismatch"
            )

        if repeat >= WARMUPS:
            timings.append(
                elapsed / QUERY_COUNT
            )

    if len(timings) != REPEATS:
        raise RuntimeError(
            "lookup-only repeat count mismatch"
        )

    return float(
        statistics.median(timings)
    )


def timed_address_plus_lookup(
    table,
    kind,
    indices,
    expected_checksum,
):
    timings = []

    for repeat in range(WARMUPS + REPEATS):
        checksum = 0

        start = time.perf_counter_ns()

        for index in indices:
            route, depth, node = coordinate(index)

            key = encode_key(
                kind,
                route,
                depth,
                node,
            )

            checksum += lookup_key(
                table,
                kind,
                key,
            )

        elapsed = (
            time.perf_counter_ns()
            - start
        )

        if checksum != expected_checksum:
            raise RuntimeError(
                f"{kind} address+lookup checksum mismatch"
            )

        if repeat >= WARMUPS:
            timings.append(
                elapsed / QUERY_COUNT
            )

    if len(timings) != REPEATS:
        raise RuntimeError(
            "address+lookup repeat count mismatch"
        )

    return float(
        statistics.median(timings)
    )


def benchmark_candidate_size(
    kind,
    size,
):
    indices = query_indices(size)

    expected_checksum = sum(indices)

    build_start = time.perf_counter_ns()

    table = build_table(
        kind,
        size,
    )

    build_ns = (
        time.perf_counter_ns()
        - build_start
    )

    keys = tuple(
        encode_key(
            kind,
            *coordinate(index),
        )
        for index in indices
    )

    lookup_only_ns = timed_lookup_only(
        table,
        kind,
        keys,
        expected_checksum,
    )

    address_plus_lookup_ns = (
        timed_address_plus_lookup(
            table,
            kind,
            indices,
            expected_checksum,
        )
    )

    memory_bytes_per_entry = (
        estimate_shallow_bytes_per_entry(
            table,
            kind,
            size,
        )
    )

    result = {
        "size": int(size),
        "candidate": kind,
        "build_ns": int(build_ns),
        "median_lookup_only_ns":
            float(lookup_only_ns),
        "median_address_plus_lookup_ns":
            float(address_plus_lookup_ns),
        "estimated_shallow_bytes_per_entry":
            float(memory_bytes_per_entry),
        "lookup_correctness": True,
    }

    del keys
    del table
    gc.collect()

    return result



HIERARCHY_QUERIES = 4096
HIERARCHY_DEPTHS = (4, 3, 2, 1, 0)


def hierarchy_chain(query_id):
    if not 0 <= query_id < HIERARCHY_QUERIES:
        raise ValueError("hierarchy query outside range")

    route = query_id
    node = query_id

    chain = []

    for depth in HIERARCHY_DEPTHS:
        chain.append(
            (
                route,
                depth,
                node,
            )
        )

        node >>= 1

    if len(chain) != 5:
        raise RuntimeError(
            "hierarchy chain length mismatch"
        )

    return tuple(chain)


def build_hierarchy_table(kind):
    expected_entries = (
        HIERARCHY_QUERIES
        * len(HIERARCHY_DEPTHS)
    )

    if kind == "nested_dict_control":
        table = {}
    else:
        table = {}

    entry_count = 0

    for query_id in range(HIERARCHY_QUERIES):
        chain = hierarchy_chain(query_id)

        for step, coord in enumerate(chain):
            sentinel = (
                query_id * 5
                + step
            )

            if kind == "nested_dict_control":
                route, depth, node = coord

                level1 = table.setdefault(
                    route,
                    {},
                )

                level2 = level1.setdefault(
                    depth,
                    {},
                )

                level2[node] = sentinel
            else:
                table[
                    encode_key(
                        kind,
                        *coord,
                    )
                ] = sentinel

            entry_count += 1

    if entry_count != expected_entries:
        raise RuntimeError(
            "hierarchy entry count mismatch"
        )

    return table, entry_count


def timed_hierarchy_traversal(
    table,
    kind,
):
    timings = []

    expected_checksum = sum(
        query_id * 25 + 10
        for query_id
        in range(HIERARCHY_QUERIES)
    )

    for repeat in range(
        WARMUPS + REPEATS
    ):
        checksum = 0

        start = time.perf_counter_ns()

        for query_id in range(
            HIERARCHY_QUERIES
        ):
            for coord in hierarchy_chain(
                query_id
            ):
                key = encode_key(
                    kind,
                    *coord,
                )

                checksum += lookup_key(
                    table,
                    kind,
                    key,
                )

        elapsed = (
            time.perf_counter_ns()
            - start
        )

        if checksum != expected_checksum:
            raise RuntimeError(
                f"{kind} hierarchy checksum mismatch"
            )

        if repeat >= WARMUPS:
            timings.append(
                elapsed / HIERARCHY_QUERIES
            )

    if len(timings) != REPEATS:
        raise RuntimeError(
            "hierarchy repeat count mismatch"
        )

    return float(
        statistics.median(timings)
    )


def estimate_shallow_bytes_per_entry(
    table,
    kind,
    entry_count,
):
    if entry_count <= 0:
        raise ValueError(
            "entry_count must be positive"
        )

    total = sys.getsizeof(table)

    if kind == "nested_dict_control":
        leaf_entries = 0

        for route, level1 in table.items():
            total += sys.getsizeof(route)
            total += sys.getsizeof(level1)

            for depth, level2 in level1.items():
                total += sys.getsizeof(depth)
                total += sys.getsizeof(level2)

                for node, value in level2.items():
                    total += sys.getsizeof(node)
                    total += sys.getsizeof(value)
                    leaf_entries += 1

        if leaf_entries != entry_count:
            raise RuntimeError(
                "nested memory entry count mismatch"
            )

    else:
        counted = 0

        for key, value in table.items():
            total += sys.getsizeof(key)
            total += sys.getsizeof(value)
            counted += 1

        if counted != entry_count:
            raise RuntimeError(
                "flat memory entry count mismatch"
            )

    return float(total / entry_count)


def hierarchy_selftest():
    expected_entries = 20480

    for kind in CANDIDATES:
        table, count = build_hierarchy_table(
            kind
        )

        if count != expected_entries:
            raise RuntimeError(
                f"{kind} hierarchy size mismatch"
            )

        for query_id in (
            0,
            1,
            31,
            255,
            4095,
        ):
            chain = hierarchy_chain(
                query_id
            )

            if len(chain) != 5:
                raise RuntimeError(
                    "hierarchy chain mismatch"
                )

            for step, coord in enumerate(
                chain
            ):
                key = encode_key(
                    kind,
                    *coord,
                )

                expected = (
                    query_id * 5
                    + step
                )

                if lookup_key(
                    table,
                    kind,
                    key,
                ) != expected:
                    raise RuntimeError(
                        f"{kind} hierarchy lookup mismatch"
                    )

        estimate = (
            estimate_shallow_bytes_per_entry(
                table,
                kind,
                count,
            )
        )

        if not (
            estimate > 0.0
        ):
            raise RuntimeError(
                f"{kind} invalid memory estimate"
            )

        del table
        gc.collect()

    return expected_entries



def sha256_file(path):
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()


def contract_check():
    with PROTOCOL.open(
        encoding="utf-8"
    ) as f:
        protocol = json.load(f)

    with CLARIFICATION.open(
        encoding="utf-8"
    ) as f:
        clarification = json.load(f)

    checks = {
        "sizes":
            tuple(protocol["sizes"]) == SIZES,
        "query_count":
            protocol["benchmark"][
                "query_count_per_size"
            ] == QUERY_COUNT,
        "repeats":
            protocol["benchmark"][
                "repeats"
            ] == REPEATS,
        "warmups":
            clarification["timing"][
                "warmup_batches"
            ] == WARMUPS,
        "clarified_repeats":
            clarification["timing"][
                "measured_repeats"
            ] == REPEATS,
        "clarified_queries":
            clarification["point_queries"][
                "count"
            ] == QUERY_COUNT,
        "hierarchy_steps":
            clarification["hierarchy"][
                "steps"
            ] == 5,
        "morton_width":
            protocol["coordinate_contract"][
                "morton_key_bits"
            ] == 63,
        "candidate_count":
            len(CANDIDATES) == 4,
        "primary_size":
            protocol["primary"][
                "size"
            ] == 1_000_000,
        "primary_metric":
            protocol["primary"][
                "metric"
            ] == (
                "median_address_plus_lookup_ns"
            ),
    }

    failed = [
        name
        for name, passed
        in checks.items()
        if not passed
    ]

    if failed:
        raise RuntimeError(
            "contract mismatch: "
            + ", ".join(failed)
        )

    correctness_selftest()

    hierarchy_entries = (
        hierarchy_selftest()
    )

    if hierarchy_entries != 20480:
        raise RuntimeError(
            "hierarchy bound mismatch"
        )

    return {
        "status": "PASS",
        "checks": checks,
        "hierarchy_entries": hierarchy_entries,
        "benchmark_executed": False,
    }


def benchmark_hierarchy(kind):
    table, count = build_hierarchy_table(
        kind
    )

    median_ns = timed_hierarchy_traversal(
        table,
        kind,
    )

    result = {
        "candidate": kind,
        "logical_entries": count,
        "median_five_step_hierarchy_traversal_ns":
            float(median_ns),
    }

    del table
    gc.collect()

    return result


def run_benchmark():
    contract_check()

    all_results = []
    hierarchy_results = []

    total_steps = (
        len(CANDIDATES)
        * (len(SIZES) + 1)
    )

    step = 0

    for kind in CANDIDATES:
        for size in SIZES:
            step += 1

            print(
                f"[{step:02d}/{total_steps}] "
                f"{kind} size={size:,}",
                flush=True,
            )

            result = (
                benchmark_candidate_size(
                    kind,
                    size,
                )
            )

            all_results.append(result)

        step += 1

        print(
            f"[{step:02d}/{total_steps}] "
            f"{kind} hierarchy",
            flush=True,
        )

        hierarchy_results.append(
            benchmark_hierarchy(kind)
        )

    primary_size = 1_000_000

    primary_rows = [
        row
        for row in all_results
        if row["size"] == primary_size
    ]

    tuple_row = next(
        row
        for row in primary_rows
        if row["candidate"] == "tuple_maf"
    )

    tuple_ns = tuple_row[
        "median_address_plus_lookup_ns"
    ]

    for row in primary_rows:
        candidate_ns = row[
            "median_address_plus_lookup_ns"
        ]

        if candidate_ns <= 0.0:
            raise RuntimeError(
                "non-positive primary timing"
            )

        row["speedup_vs_tuple"] = (
            tuple_ns / candidate_ns
        )

    winner = min(
        primary_rows,
        key=lambda row:
            row[
                "median_address_plus_lookup_ns"
            ],
    )

    result = {
        "schema":
            "openmind.maf3d.address_geometry_result.v1",
        "status": "COMPLETE",
        "protocol_sha256":
            sha256_file(PROTOCOL),
        "clarification_sha256":
            sha256_file(CLARIFICATION),
        "engine_sha256":
            sha256_file(
                Path(__file__).resolve()
            ),
        "sizes": list(SIZES),
        "query_count": QUERY_COUNT,
        "repeats": REPEATS,
        "warmups": WARMUPS,
        "point_results": all_results,
        "hierarchy_results":
            hierarchy_results,
        "primary": {
            "size": primary_size,
            "metric":
                "median_address_plus_lookup_ns",
            "tuple_baseline_ns":
                tuple_ns,
            "winner":
                winner["candidate"],
            "winner_ns":
                winner[
                    "median_address_plus_lookup_ns"
                ],
            "winner_speedup_vs_tuple":
                winner[
                    "speedup_vs_tuple"
                ],
        },
    }

    RESULT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with RESULT_FILE.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            result,
            f,
            indent=2,
            sort_keys=True,
        )
        f.write("\n")

    print(
        f"result: {RESULT_FILE}",
        flush=True,
    )

    return result


def main():
    parser = argparse.ArgumentParser()

    mode = parser.add_mutually_exclusive_group(
        required=True
    )

    mode.add_argument(
        "--contract-check",
        action="store_true",
    )

    mode.add_argument(
        "--run",
        action="store_true",
    )

    args = parser.parse_args()

    if args.contract_check:
        result = contract_check()

        print(
            json.dumps(
                result,
                sort_keys=True,
            )
        )

        return

    if args.run:
        run_benchmark()
        return

    raise RuntimeError(
        "unreachable CLI state"
    )


if __name__ == "__main__":
    main()
