#!/usr/bin/env python3

import argparse
import csv
import json
import math
import random
import statistics
import time
from collections import defaultdict
from pathlib import Path

DEFAULT_PATH = "activation_vectors_all_tokens.csv"

SEED = 1337
EXCLUDED_TOKENS = {0}


def cosine(a, b):
    dot = 0.0
    na = 0.0
    nb = 0.0

    for x, y in zip(a, b):
        dot += x * y
        na += x * x
        nb += y * y

    if na == 0.0 or nb == 0.0:
        return 0.0

    return dot / math.sqrt(na * nb)


def load_data(path):
    data = {}

    with open(path, newline="") as f:
        reader = csv.DictReader(f)

        value_columns = [
            x
            for x in reader.fieldnames
            if x.startswith("v")
        ]

        for r in reader:
            layer = int(r["layer"])
            token = int(r["token_index"])

            if token in EXCLUDED_TOKENS:
                continue

            data[(layer, token)] = [
                float(r[k])
                for k in value_columns
            ]

    layers = sorted({
        layer
        for layer, _ in data
    })

    tokens = sorted({
        token
        for _, token in data
    })

    return data, layers, tokens


def build_cosine_cache(
    data,
    layers,
    tokens,
):
    """
    Cache:

        cache[(a, b)][ta][tb]

    for each unique layer pair.

    V3-original recomputed these 1536-dimensional cosines
    repeatedly during every permutation. V3-fixed computes each
    required cosine once.
    """

    cache = {}

    layer_pairs = [
        (a, b)
        for i, a in enumerate(layers)
        for b in layers[i + 1:]
    ]

    total = len(layer_pairs)

    for index, (a, b) in enumerate(
        layer_pairs,
        1,
    ):
        matrix = []

        for ta in tokens:
            row = []

            va = data[(a, ta)]

            for tb in tokens:
                row.append(
                    cosine(
                        va,
                        data[(b, tb)],
                    )
                )

            matrix.append(row)

        cache[(a, b)] = matrix

        if (
            index == 1 or
            index % 25 == 0 or
            index == total
        ):
            print(
                "CACHE "
                f"{index}/{total}",
                flush=True,
            )

    return cache


def pair_stat_cached(
    matrix,
    label_indices,
    token_count,
):
    same = []
    cross = []

    for ta in range(token_count):
        same.append(
            matrix[ta][label_indices[ta]]
        )

    for ta in range(token_count):
        row = matrix[ta]

        for tb in range(token_count):
            if ta == tb:
                continue

            cross.append(
                row[label_indices[tb]]
            )

    same_mean = statistics.mean(
        same
    )

    cross_mean = statistics.mean(
        cross
    )

    return (
        same_mean,
        cross_mean,
        same_mean - cross_mean,
    )

def write_checkpoint(
    path,
    completed,
    rng,
    null_deltas,
):
    payload = {
        "schema":
            "openmind.recurrence.v3_fixed.checkpoint.v1",

        "completed_permutations":
            completed,

        "rng_state":
            repr(rng.getstate()),

        "null_deltas": {
            f"{a},{b}": values
            for (a, b), values
            in null_deltas.items()
        },
    }

    tmp = path.with_suffix(
        path.suffix + ".tmp"
    )

    tmp.write_text(
        json.dumps(
            payload,
            separators=(",", ":"),
        )
        + "\n"
    )

    tmp.replace(path)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--path",
        default=DEFAULT_PATH,
    )

    parser.add_argument(
        "--permutations",
        type=int,
        default=1000,
    )

    parser.add_argument(
        "--progress-every",
        type=int,
        default=10,
    )

    parser.add_argument(
        "--checkpoint-every",
        type=int,
        default=25,
    )

    parser.add_argument(
        "--checkpoint",
        default=(
            "results/runtime/"
            "v3_fixed_checkpoints/"
            "checkpoint.json"
        ),
    )

    parser.add_argument(
        "--runtime-limit",
        type=float,
        default=0.0,
        help=(
            "Maximum experiment seconds. "
            "0 disables the limit."
        ),
    )

    args = parser.parse_args()

    if args.permutations <= 0:
        raise SystemExit(
            "permutations must be > 0"
        )

    started = time.monotonic()

    data, layers, tokens = (
        load_data(args.path)
    )

    print(
        "=" * 76
    )

    print(
        " OPENMIND / RECURRENCE TOPOLOGY V3-FIXED"
    )

    print(
        "=" * 76
    )

    print(
        f"Dataset              : {args.path}"
    )

    print(
        f"Layers               : {len(layers)}"
    )

    print(
        f"Tokens               : {len(tokens)}"
    )

    print(
        f"Vectors              : {len(data)}"
    )

    print(
        "Dimensions           : "
        f"{len(next(iter(data.values())))}"
    )

    print(
        f"Permutations         : {args.permutations}"
    )

    print(
        f"Seed                 : {SEED}"
    )

    print(
        f"Runtime limit        : "
        f"{args.runtime_limit:.1f} sec"
    )

    print()

    token_count = len(tokens)

    identity = list(
        range(token_count)
    )

    layer_pairs = [
        (a, b)
        for i, a in enumerate(layers)
        for b in layers[i + 1:]
    ]

    print(
        f"Layer pairs          : {len(layer_pairs)}"
    )

    print()

    cache_start = time.monotonic()

    cache = build_cosine_cache(
        data,
        layers,
        tokens,
    )

    cache_seconds = (
        time.monotonic() -
        cache_start
    )

    print(
        f"Cosine cache seconds : "
        f"{cache_seconds:.3f}"
    )

    observed = {}

    for pair in layer_pairs:
        observed[pair] = (
            pair_stat_cached(
                cache[pair],
                identity,
                token_count,
            )
        )

    rng = random.Random(SEED)

    null_deltas = defaultdict(list)

    checkpoint = Path(
        args.checkpoint
    )

    checkpoint.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    permutation_start = (
        time.monotonic()
    )

    completed = 0

    for permutation in range(
        1,
        args.permutations + 1,
    ):
        shuffled = identity[:]

        rng.shuffle(shuffled)

        for pair in layer_pairs:
            _, _, delta = (
                pair_stat_cached(
                    cache[pair],
                    shuffled,
                    token_count,
                )
            )

            null_deltas[pair].append(
                delta
            )

        completed = permutation

        if (
            permutation == 1 or
            permutation %
            args.progress_every == 0 or
            permutation ==
            args.permutations
        ):
            elapsed = (
                time.monotonic() -
                permutation_start
            )

            rate = (
                permutation / elapsed
                if elapsed > 0
                else 0.0
            )

            print(
                "PERM "
                f"{permutation}/"
                f"{args.permutations} "
                f"elapsed={elapsed:.2f}s "
                f"rate={rate:.3f}/s",
                flush=True,
            )

        if (
            permutation %
            args.checkpoint_every == 0
        ):
            write_checkpoint(
                checkpoint,
                completed,
                rng,
                null_deltas,
            )

        if (
            args.runtime_limit > 0.0 and
            (
                time.monotonic() -
                started
            ) >= args.runtime_limit
        ):
            write_checkpoint(
                checkpoint,
                completed,
                rng,
                null_deltas,
            )

            print(
                "RUNTIME LIMIT REACHED "
                f"after {completed} permutations",
                flush=True,
            )

            return 3

    write_checkpoint(
        checkpoint,
        completed,
        rng,
        null_deltas,
    )

    records = []

    for (
        pair,
        observed_values,
    ) in observed.items():

        a, b = pair

        same, cross, delta = (
            observed_values
        )

        null = null_deltas[pair]

        null_mean = (
            statistics.mean(null)
        )

        null_sd = (
            statistics.stdev(null)
            if len(null) > 1
            else 0.0
        )

        if null_sd == 0.0:
            z = 0.0
        else:
            z = (
                delta -
                null_mean
            ) / null_sd

        exceed = sum(
            x >= delta
            for x in null
        )

        p = (
            exceed + 1
        ) / (
            completed + 1
        )

        records.append(
            (
                z,
                p,
                delta,
                same,
                cross,
                null_mean,
                b - a,
                a,
                b,
            )
        )

    records.sort(
        reverse=True
    )

    print()
    print(
        "TOP LAYER PAIRS BY EMPIRICAL Z"
    )

    print(
        "-" * 76
    )

    print(
        "rank       z         p      delta "
        "gap pair"
    )

    print(
        "-" * 76
    )

    for rank, row in enumerate(
        records[:50],
        1,
    ):
        (
            z,
            p,
            delta,
            _same,
            _cross,
            _null,
            gap,
            a,
            b,
        ) = row

        print(
            f"{rank:4d} "
            f"{z:+9.3f} "
            f"{p:9.6f} "
            f"{delta:+10.6f} "
            f"{gap:3d} "
            f"L{a:02d}<->L{b:02d}"
        )

    total_seconds = (
        time.monotonic() -
        started
    )

    print()
    print(
        "=" * 76
    )

    print(
        " COMPLETE"
    )

    print(
        "=" * 76
    )

    print(
        f"completed permutations: "
        f"{completed}"
    )

    print(
        f"total runtime seconds : "
        f"{total_seconds:.3f}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
