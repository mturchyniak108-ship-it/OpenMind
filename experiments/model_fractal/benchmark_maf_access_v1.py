import hashlib
import json
import os
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

OUT = Path(
    "experiments/model_fractal/maf_access_benchmark_v1.json"
)

SEED = 20260824
SAMPLES = 32
REPEATS = 3


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def load_json(path):
    return json.loads(
        path.read_text(encoding="utf-8")
    )


def direct_inventory_lookup(tensors, name):
    for tensor in tensors:
        if tensor["name"] == name:
            return tensor
    raise KeyError(name)


def maf_lookup(maf, name):
    for tensor in maf["global_tensors"]:
        if tensor["name"] == name:
            return tensor

    for layer in maf["layers"].values():
        for tensor in layer:
            if tensor["name"] == name:
                return tensor

    raise KeyError(name)


def read_tensor(f, tensor):
    f.seek(int(tensor["file_start"]))
    return f.read(int(tensor["span_bytes"]))


def timed(fn):
    start = time.perf_counter_ns()
    result = fn()
    end = time.perf_counter_ns()
    return result, end - start


def main():
    if not SOURCE.exists():
        raise SystemExit(
            f"Missing source: {SOURCE}"
        )

    if not INVENTORY.exists():
        raise SystemExit(
            f"Missing inventory: {INVENTORY}"
        )

    if not MAF.exists():
        raise SystemExit(
            f"Missing MAF: {MAF}"
        )

    inventory = load_json(INVENTORY)
    maf = load_json(MAF)

    tensors = inventory["tensors"]

    if len(tensors) != 339:
        raise SystemExit(
            "Unexpected inventory tensor count"
        )

    source_hash = inventory["source"]["sha256"]

    names = [
        t["name"]
        for t in tensors
    ]

    rng = random.Random(SEED)

    selected_names = rng.sample(
        names,
        min(SAMPLES, len(names)),
    )

    direct_lookup_ns = []
    maf_lookup_ns = []

    direct_read_ns = []
    maf_read_ns = []

    verified = []

    with SOURCE.open("rb") as f:
        for name in selected_names:

            direct = direct_inventory_lookup(
                tensors,
                name,
            )

            maf_tensor = maf_lookup(
                maf,
                name,
            )

            if (
                direct["file_start"]
                != maf_tensor["file_start"]
            ):
                raise SystemExit(
                    f"OFFSET MISMATCH: {name}"
                )

            if (
                direct["span_bytes"]
                != maf_tensor["span_bytes"]
            ):
                raise SystemExit(
                    f"SPAN MISMATCH: {name}"
                )

            for _ in range(REPEATS):

                _, ns = timed(
                    lambda: direct_inventory_lookup(
                        tensors,
                        name,
                    )
                )
                direct_lookup_ns.append(ns)

                _, ns = timed(
                    lambda: maf_lookup(
                        maf,
                        name,
                    )
                )
                maf_lookup_ns.append(ns)

                direct_payload, ns = timed(
                    lambda: read_tensor(
                        f,
                        direct,
                    )
                )
                direct_read_ns.append(ns)

                maf_payload, ns = timed(
                    lambda: read_tensor(
                        f,
                        maf_tensor,
                    )
                )
                maf_read_ns.append(ns)

                direct_hash = sha256(
                    direct_payload
                )

                maf_hash = sha256(
                    maf_payload
                )

                if direct_hash != maf_hash:
                    raise SystemExit(
                        f"PAYLOAD MISMATCH: {name}"
                    )

                if direct_hash != direct[
                    "payload_sha256"
                ]:
                    raise SystemExit(
                        f"SOURCE PAYLOAD HASH MISMATCH: {name}"
                    )

            verified.append({
                "name": name,
                "type": direct["type"],
                "dims": direct["dims"],
                "file_start": direct["file_start"],
                "span_bytes": direct["span_bytes"],
                "payload_sha256": direct[
                    "payload_sha256"
                ],
            })

    def summary(values):
        return {
            "count": len(values),
            "mean_ns": statistics.mean(values),
            "median_ns": statistics.median(values),
            "min_ns": min(values),
            "max_ns": max(values),
        }

    output = {
        "format":
            "openmind.maf_access_benchmark.v1",

        "source": {
            "path": str(SOURCE),
            "sha256": source_hash,
            "bytes": SOURCE.stat().st_size,
        },

        "benchmark": {
            "seed": SEED,
            "samples": len(selected_names),
            "repeats": REPEATS,
            "total_accesses":
                len(selected_names) * REPEATS,
        },

        "direct_lookup": summary(
            direct_lookup_ns
        ),

        "maf_lookup": summary(
            maf_lookup_ns
        ),

        "direct_payload_read": summary(
            direct_read_ns
        ),

        "maf_payload_read": summary(
            maf_read_ns
        ),

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
    print(" OPENMIND / MAF ACCESS BENCHMARK V1")
    print("=" * 72)
    print(f"source:        {SOURCE}")
    print(f"source sha256:  {source_hash}")
    print(f"samples:       {len(selected_names)}")
    print(f"repeats:       {REPEATS}")
    print()

    print("=== LOOKUP ===")
    print(
        "direct mean ns:",
        output["direct_lookup"]["mean_ns"],
    )
    print(
        "MAF mean ns:",
        output["maf_lookup"]["mean_ns"],
    )

    print()

    print("=== PAYLOAD READ ===")
    print(
        "direct mean ns:",
        output["direct_payload_read"]["mean_ns"],
    )
    print(
        "MAF mean ns:",
        output["maf_payload_read"]["mean_ns"],
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
    print("MAF ACCESS BENCHMARK COMPLETE")


if __name__ == "__main__":
    main()
