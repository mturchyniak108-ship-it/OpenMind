import hashlib
import json
import random
import statistics
import time
from pathlib import Path

SOURCE = Path.home() / "qwen2.5-coder-q8_0.gguf"

INVENTORY = Path(
    "experiments/model_fractal/gguf_tensor_inventory_v1.json"
)

MAF = Path(
    "experiments/model_fractal/maf_representation_v1.json"
)

INDEX = Path(
    "experiments/model_fractal/maf_index_v1.json"
)

OUT = Path(
    "experiments/model_fractal/maf_workload_benchmark_v2.json"
)

SEED = 20260825
REPEATS = 5
REQUESTS = 1000

READ_SIZES = (64, 256, 1024, 4096)


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def linear_lookup(tensors, name):
    for tensor in tensors:
        if tensor["name"] == name:
            return tensor
    raise KeyError(name)


def nested_maf_lookup(maf, name):
    for tensor in maf["global_tensors"]:
        if tensor["name"] == name:
            return tensor

    for layer in maf["layers"].values():
        for tensor in layer:
            if tensor["name"] == name:
                return tensor

    raise KeyError(name)


def indexed_lookup(index, name):
    return index[name]


def read_bounded(f, tensor, size):
    start = int(tensor["file_start"])
    span = int(tensor["span_bytes"])
    n = min(size, span)

    f.seek(start)
    return f.read(n)


def timed(fn):
    start = time.perf_counter_ns()
    result = fn()
    end = time.perf_counter_ns()
    return result, end - start


def percentile(values, p):
    ordered = sorted(values)
    if not ordered:
        return 0

    k = (len(ordered) - 1) * p
    lo = int(k)
    hi = min(lo + 1, len(ordered) - 1)

    if lo == hi:
        return ordered[lo]

    return ordered[lo] + (ordered[hi] - ordered[lo]) * (k - lo)


def summary(values):
    return {
        "count": len(values),
        "mean_ns": statistics.mean(values),
        "median_ns": statistics.median(values),
        "p95_ns": percentile(values, 0.95),
        "p99_ns": percentile(values, 0.99),
        "min_ns": min(values),
        "max_ns": max(values),
        "requests_per_second":
            1_000_000_000 / statistics.mean(values),
    }


def main():
    for path in (SOURCE, INVENTORY, MAF, INDEX):
        if not path.exists():
            raise SystemExit(
                f"Missing required artifact: {path}"
            )

    inventory = load_json(INVENTORY)
    maf = load_json(MAF)
    indexed = load_json(INDEX)

    tensors = inventory["tensors"]
    index = indexed["index"]

    if len(tensors) != 339:
        raise SystemExit(
            f"Unexpected inventory count: {len(tensors)}"
        )

    if len(index) != 339:
        raise SystemExit(
            f"Unexpected index count: {len(index)}"
        )

    source_hash = sha256_file(SOURCE)

    if source_hash != inventory["source"]["sha256"]:
        raise SystemExit("SOURCE HASH MISMATCH: INVENTORY")

    if source_hash != indexed["source"]["sha256"]:
        raise SystemExit("SOURCE HASH MISMATCH: INDEX")

    names = [tensor["name"] for tensor in tensors]

    rng = random.Random(SEED)

    random_names = [
        rng.choice(names)
        for _ in range(REQUESTS)
    ]

    sequential_names = [
        names[i % len(names)]
        for i in range(REQUESTS)
    ]

    workloads = {
        "random": random_names,
        "sequential": sequential_names,
    }

    results = {}

    with SOURCE.open("rb") as f:

        # --------------------------------------------------------
        # Verify representation equivalence before timing.
        # --------------------------------------------------------

        for name in names:
            linear = linear_lookup(tensors, name)
            nested = nested_maf_lookup(maf, name)
            direct = indexed_lookup(index, name)

            for field in (
                "file_start",
                "span_bytes",
                "elements",
                "decoded_elements",
                "payload_sha256",
            ):
                if linear[field] != nested[field]:
                    raise SystemExit(
                        f"LINEAR/MAF MISMATCH: {name}: {field}"
                    )

                if linear[field] != direct[field]:
                    raise SystemExit(
                        f"LINEAR/INDEX MISMATCH: {name}: {field}"
                    )

        # --------------------------------------------------------
        # Workload benchmark.
        # --------------------------------------------------------

        for workload_name, request_names in workloads.items():

            results[workload_name] = {}

            for read_size in READ_SIZES:

                lookup_results = {
                    "linear": [],
                    "nested": [],
                    "indexed": [],
                }

                address_results = {
                    "linear": [],
                    "nested": [],
                    "indexed": [],
                }

                access_results = {
                    "linear": [],
                    "nested": [],
                    "indexed": [],
                }

                total_results = {
                    "linear": [],
                    "nested": [],
                    "indexed": [],
                }

                checksums = {
                    "linear": 0,
                    "nested": 0,
                    "indexed": 0,
                }

                for _ in range(REPEATS):

                    for name in request_names:

                        # ------------------------------
                        # Lookup only
                        # ------------------------------

                        linear, ns = timed(
                            lambda name=name:
                            linear_lookup(tensors, name)
                        )
                        lookup_results["linear"].append(ns)

                        nested, ns = timed(
                            lambda name=name:
                            nested_maf_lookup(maf, name)
                        )
                        lookup_results["nested"].append(ns)

                        direct, ns = timed(
                            lambda name=name:
                            indexed_lookup(index, name)
                        )
                        lookup_results["indexed"].append(ns)

                        # ------------------------------
                        # Address resolution
                        # ------------------------------

                        _, ns = timed(
                            lambda linear=linear:
                            (
                                int(linear["file_start"]),
                                int(linear["span_bytes"]),
                            )
                        )
                        address_results["linear"].append(ns)

                        _, ns = timed(
                            lambda nested=nested:
                            (
                                int(nested["file_start"]),
                                int(nested["span_bytes"]),
                            )
                        )
                        address_results["nested"].append(ns)

                        _, ns = timed(
                            lambda direct=direct:
                            (
                                int(direct["file_start"]),
                                int(direct["span_bytes"]),
                            )
                        )
                        address_results["indexed"].append(ns)

                        # ------------------------------
                        # Payload read only
                        # ------------------------------

                        payload, ns = timed(
                            lambda linear=linear:
                            read_bounded(
                                f,
                                linear,
                                read_size,
                            )
                        )
                        access_results["linear"].append(ns)
                        checksums["linear"] ^= (
                            sum(payload) & 0xFFFFFFFF
                        )

                        payload, ns = timed(
                            lambda nested=nested:
                            read_bounded(
                                f,
                                nested,
                                read_size,
                            )
                        )
                        access_results["nested"].append(ns)
                        checksums["nested"] ^= (
                            sum(payload) & 0xFFFFFFFF
                        )

                        payload, ns = timed(
                            lambda direct=direct:
                            read_bounded(
                                f,
                                direct,
                                read_size,
                            )
                        )
                        access_results["indexed"].append(ns)
                        checksums["indexed"] ^= (
                            sum(payload) & 0xFFFFFFFF
                        )

                        # ------------------------------
                        # TRUE END-TO-END REQUEST
                        # lookup + address + payload read
                        # ------------------------------

                        def linear_request(name=name):
                            tensor = linear_lookup(tensors, name)
                            return read_bounded(
                                f, tensor, read_size
                            )

                        def nested_request(name=name):
                            tensor = nested_maf_lookup(maf, name)
                            return read_bounded(
                                f, tensor, read_size
                            )

                        def indexed_request(name=name):
                            tensor = indexed_lookup(index, name)
                            return read_bounded(
                                f, tensor, read_size
                            )

                        payload, ns = timed(linear_request)
                        total_results["linear"].append(ns)

                        payload, ns = timed(nested_request)
                        total_results["nested"].append(ns)

                        payload, ns = timed(indexed_request)
                        total_results["indexed"].append(ns)

                # ------------------------------------------------
                # Ensure all paths actually read identical bytes.
                # ------------------------------------------------

                if not (
                    checksums["linear"]
                    == checksums["nested"]
                    == checksums["indexed"]
                ):
                    raise SystemExit(
                        f"READ CHECKSUM MISMATCH: "
                        f"{workload_name}, {read_size}"
                    )

                results[workload_name][str(read_size)] = {
                    "lookup": {
                        key: summary(value)
                        for key, value
                        in lookup_results.items()
                    },
                    "address_resolution": {
                        key: summary(value)
                        for key, value
                        in address_results.items()
                    },
                    "payload_access": {
                        key: summary(value)
                        for key, value
                        in access_results.items()
                    },
                    "end_to_end": {
                        key: summary(value)
                        for key, value
                        in total_results.items()
                    },
                    "checksums": checksums,
                }

    output = {
        "format":
            "openmind.maf_workload_benchmark.v2",

        "source": {
            "path": str(SOURCE),
            "sha256": source_hash,
            "bytes": SOURCE.stat().st_size,
        },

        "benchmark": {
            "seed": SEED,
            "repeats": REPEATS,
            "requests_per_workload": REQUESTS,
            "read_sizes": list(READ_SIZES),
            "tensor_count": len(tensors),
        },

        "results": results,
    }

    OUT.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print(" OPENMIND / MAF WORKLOAD BENCHMARK V2")
    print("=" * 72)

    print(f"source:   {SOURCE}")
    print(f"sha256:   {source_hash}")
    print(f"tensors:  {len(tensors)}")
    print(f"requests: {REQUESTS}")
    print(f"repeats:  {REPEATS}")
    print()

    for workload_name, workload in results.items():

        print(f"=== {workload_name.upper()} ACCESS ===")

        for read_size, data in workload.items():

            print(f"\nread size: {read_size} bytes")

            for method in ("linear", "nested", "indexed"):

                lookup = data["lookup"][method]["median_ns"]
                access = data["payload_access"][method]["median_ns"]

                total = data["end_to_end"][method]["median_ns"]

                print(
                    f"{method:8s} "
                    f"lookup={lookup:10.1f} ns "
                    f"access={access:10.1f} ns "
                    f"total={total:10.1f} ns"
                )

    print()
    print(f"output: {OUT}")
    print()
    print("MAF WORKLOAD BENCHMARK COMPLETE")


if __name__ == "__main__":
    main()
