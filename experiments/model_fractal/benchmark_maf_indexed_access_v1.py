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
    "experiments/model_fractal/maf_indexed_access_benchmark_v1.json"
)

SEED = 20260824
SAMPLES = 32
REPEATS = 5


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def load_json(path):
    return json.loads(
        path.read_text(encoding="utf-8")
    )


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


def read_tensor(f, tensor):
    f.seek(int(tensor["file_start"]))
    return f.read(int(tensor["span_bytes"]))


def timed(fn):
    start = time.perf_counter_ns()
    result = fn()
    end = time.perf_counter_ns()
    return result, end - start


def summary(values):
    return {
        "count": len(values),
        "mean_ns": statistics.mean(values),
        "median_ns": statistics.median(values),
        "min_ns": min(values),
        "max_ns": max(values),
    }


def main():
    for path in (
        SOURCE,
        INVENTORY,
        MAF,
        INDEX,
    ):
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

    if inventory["source"]["sha256"] != indexed["source"]["sha256"]:
        raise SystemExit(
            "SOURCE HASH MISMATCH BETWEEN INVENTORY AND INDEX"
        )

    names = [
        tensor["name"]
        for tensor in tensors
    ]

    rng = random.Random(SEED)

    selected_names = rng.sample(
        names,
        min(SAMPLES, len(names)),
    )

    linear_ns = []
    nested_ns = []
    indexed_ns = []

    linear_read_ns = []
    nested_read_ns = []
    indexed_read_ns = []

    verified = []

    with SOURCE.open("rb") as f:

        for name in selected_names:

            linear = linear_lookup(
                tensors,
                name,
            )

            nested = nested_maf_lookup(
                maf,
                name,
            )

            direct = indexed_lookup(
                index,
                name,
            )

            # ----------------------------------------------------
            # Address equivalence
            # ----------------------------------------------------

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

            # ----------------------------------------------------
            # Lookup benchmark
            # ----------------------------------------------------

            for _ in range(REPEATS):

                _, ns = timed(
                    lambda: linear_lookup(
                        tensors,
                        name,
                    )
                )
                linear_ns.append(ns)

                _, ns = timed(
                    lambda: nested_maf_lookup(
                        maf,
                        name,
                    )
                )
                nested_ns.append(ns)

                _, ns = timed(
                    lambda: indexed_lookup(
                        index,
                        name,
                    )
                )
                indexed_ns.append(ns)

                # ------------------------------------------------
                # Payload access benchmark
                # ------------------------------------------------

                payload, ns = timed(
                    lambda: read_tensor(
                        f,
                        linear,
                    )
                )
                linear_read_ns.append(ns)

                nested_payload, ns = timed(
                    lambda: read_tensor(
                        f,
                        nested,
                    )
                )
                nested_read_ns.append(ns)

                indexed_payload, ns = timed(
                    lambda: read_tensor(
                        f,
                        direct,
                    )
                )
                indexed_read_ns.append(ns)

                h_linear = sha256(payload)
                h_nested = sha256(nested_payload)
                h_indexed = sha256(indexed_payload)

                if not (
                    h_linear
                    == h_nested
                    == h_indexed
                    == linear["payload_sha256"]
                ):
                    raise SystemExit(
                        f"PAYLOAD HASH MISMATCH: {name}"
                    )

            verified.append({
                "name": name,
                "type": linear["type"],
                "dims": linear["dims"],
                "file_start": linear["file_start"],
                "span_bytes": linear["span_bytes"],
                "payload_sha256":
                    linear["payload_sha256"],
            })

    output = {
        "format":
            "openmind.maf_indexed_access_benchmark.v1",

        "source": {
            "path": str(SOURCE),
            "sha256":
                inventory["source"]["sha256"],
            "bytes":
                SOURCE.stat().st_size,
        },

        "benchmark": {
            "seed": SEED,
            "samples": len(selected_names),
            "repeats": REPEATS,
            "total_accesses":
                len(selected_names) * REPEATS,
        },

        "lookup": {
            "linear_inventory":
                summary(linear_ns),
            "nested_maf":
                summary(nested_ns),
            "indexed_maf":
                summary(indexed_ns),
        },

        "payload_read": {
            "linear_inventory":
                summary(linear_read_ns),
            "nested_maf":
                summary(nested_read_ns),
            "indexed_maf":
                summary(indexed_read_ns),
        },

        "verified_payloads": verified,
    }

    OUT.write_text(
        json.dumps(
            output,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print(" OPENMIND / O(1) MAF INDEX ACCESS BENCHMARK V1")
    print("=" * 72)
    print(f"source:       {SOURCE}")
    print(
        f"source sha256: {inventory['source']['sha256']}"
    )
    print(f"samples:      {len(selected_names)}")
    print(f"repeats:      {REPEATS}")
    print()

    print("=== LOOKUP ===")

    print(
        "linear mean ns:",
        output["lookup"]["linear_inventory"]["mean_ns"],
    )

    print(
        "nested MAF mean ns:",
        output["lookup"]["nested_maf"]["mean_ns"],
    )

    print(
        "indexed MAF mean ns:",
        output["lookup"]["indexed_maf"]["mean_ns"],
    )

    print()

    print("=== PAYLOAD READ ===")

    print(
        "linear mean ns:",
        output["payload_read"]["linear_inventory"]["mean_ns"],
    )

    print(
        "nested MAF mean ns:",
        output["payload_read"]["nested_maf"]["mean_ns"],
    )

    print(
        "indexed MAF mean ns:",
        output["payload_read"]["indexed_maf"]["mean_ns"],
    )

    print()

    print(
        "verified payloads:",
        len(verified),
    )

    print(
        f"output: {OUT}"
    )

    print()
    print("O(1) MAF INDEX BENCHMARK COMPLETE")


if __name__ == "__main__":
    main()
