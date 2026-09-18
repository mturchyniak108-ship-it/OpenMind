import json
import random
import statistics
import time
from pathlib import Path

INDEX = Path("experiments/model_fractal/maf_index_v1.json")

SEED = 20260825
REPEATS = 200

SIZES = [
    339,
    1_000,
    10_000,
    100_000,
    1_000_000,
]


def timed(fn):
    start = time.perf_counter_ns()
    result = fn()
    end = time.perf_counter_ns()
    return result, end - start


def percentile(values, p):
    values = sorted(values)
    if not values:
        return 0

    k = (len(values) - 1) * p
    f = int(k)
    c = min(f + 1, len(values) - 1)

    if f == c:
        return values[f]

    return values[f] + (values[c] - values[f]) * (k - f)


def summary(values):
    return {
        "count": len(values),
        "mean_ns": statistics.mean(values),
        "median_ns": statistics.median(values),
        "p95_ns": percentile(values, 0.95),
        "p99_ns": percentile(values, 0.99),
        "min_ns": min(values),
        "max_ns": max(values),
    }


def linear_lookup(items, name):
    for item in items:
        if item["name"] == name:
            return item

    raise KeyError(name)


def nested_lookup(groups, name):
    for group in groups:
        for item in group:
            if item["name"] == name:
                return item

    raise KeyError(name)


def make_structures(base_items, size):
    items = []

    for i in range(size):
        base = base_items[i % len(base_items)]

        items.append({
            "name": f"{base['name']}__scale_{i}",
            "file_start": base["file_start"],
            "span_bytes": base["span_bytes"],
        })

    linear = items

    nested = []
    chunk_size = 12

    for i in range(0, size, chunk_size):
        nested.append(items[i:i + chunk_size])

    indexed = {
        item["name"]: item
        for item in items
    }

    return linear, nested, indexed


def main():
    if not INDEX.exists():
        raise SystemExit(f"Missing index: {INDEX}")

    data = json.loads(
        INDEX.read_text(encoding="utf-8")
    )

    base_items = [
        {
            "name": name,
            "file_start": tensor["file_start"],
            "span_bytes": tensor["span_bytes"],
        }
        for name, tensor in data["index"].items()
    ]

    rng = random.Random(SEED)

    print("=" * 72)
    print(" OPENMIND / MAF INDEX SCALE BENCHMARK V2")
    print("=" * 72)

    results = []

    for size in SIZES:
        linear, nested, indexed = make_structures(
            base_items,
            size,
        )

        names = list(indexed.keys())

        selected = rng.sample(
            names,
            min(32, len(names)),
        )

        linear_ns = []
        nested_ns = []
        indexed_ns = []

        # Warm-up
        for name in selected:
            linear_lookup(linear, name)
            nested_lookup(nested, name)
            indexed[name]

        for _ in range(REPEATS):
            for name in selected:

                _, ns = timed(
                    lambda: linear_lookup(
                        linear,
                        name,
                    )
                )
                linear_ns.append(ns)

                _, ns = timed(
                    lambda: nested_lookup(
                        nested,
                        name,
                    )
                )
                nested_ns.append(ns)

                _, ns = timed(
                    lambda: indexed[name]
                )
                indexed_ns.append(ns)

        row = {
            "size": size,
            "linear": summary(linear_ns),
            "nested": summary(nested_ns),
            "indexed": summary(indexed_ns),
        }

        results.append(row)

        print()
        print(f"N = {size:,}")
        print(
            f"linear   median={row['linear']['median_ns']:.1f} ns "
            f"p95={row['linear']['p95_ns']:.1f} ns"
        )
        print(
            f"nested   median={row['nested']['median_ns']:.1f} ns "
            f"p95={row['nested']['p95_ns']:.1f} ns"
        )
        print(
            f"indexed  median={row['indexed']['median_ns']:.1f} ns "
            f"p95={row['indexed']['p95_ns']:.1f} ns"
        )

    out = Path(
        "experiments/model_fractal/"
        "maf_index_scale_benchmark_v2.json"
    )

    output = {
        "format":
            "openmind.maf_index_scale_benchmark.v2",
        "seed": SEED,
        "repeats": REPEATS,
        "sizes": SIZES,
        "results": results,
    }

    out.write_text(
        json.dumps(
            output,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print()
    print(f"output: {out}")
    print()
    print("MAF INDEX SCALE BENCHMARK COMPLETE")


if __name__ == "__main__":
    main()
