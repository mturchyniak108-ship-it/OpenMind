#!/usr/bin/env python3

import argparse
import csv
import hashlib
import json
import math
import statistics
import time
from collections import defaultdict
from pathlib import Path

import numpy as np


DEFAULT_CORPUS = (
    "results/forest_v9a_2048_corpus/"
    "qwen25_3b_multi_prompt_2048.csv"
)

DEFAULT_CANONICAL = (
    "experiments/data/manifests/"
    "qwen25_3b_multi_prompt_2048_canonical_v1.json"
)

EXPECTED_DIM = 2048
EXPECTED_LAYERS = 36
EXPECTED_PROMPTS = 8
EXCLUDED_TOKEN = 0


def sha256(path):
    h = hashlib.sha256()

    with Path(path).open("rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()


def average_ranks(values):
    values = np.asarray(
        values,
        dtype=np.float64,
    )

    order = np.argsort(
        values,
        kind="mergesort",
    )

    ranks = np.empty(
        len(values),
        dtype=np.float64,
    )

    i = 0

    while i < len(values):

        j = i + 1

        while (
            j < len(values)
            and values[order[j]]
            == values[order[i]]
        ):
            j += 1

        rank = (
            i + j - 1
        ) / 2.0

        ranks[
            order[i:j]
        ] = rank

        i = j

    return ranks


def spearman(a, b):
    ra = average_ranks(a)
    rb = average_ranks(b)

    sa = float(
        np.std(
            ra,
            ddof=0,
        )
    )

    sb = float(
        np.std(
            rb,
            ddof=0,
        )
    )

    if sa == 0 or sb == 0:
        return 0.0

    return float(
        np.corrcoef(
            ra,
            rb,
        )[0, 1]
    )


def load_corpus(
    corpus_path,
    canonical_path,
):
    corpus_path = Path(
        corpus_path
    )

    canonical_path = Path(
        canonical_path
    )

    with canonical_path.open() as f:
        canonical = json.load(f)

    expected_sha = canonical[
        "corpus"
    ][
        "sha256"
    ]

    actual_sha = sha256(
        corpus_path
    )

    if actual_sha != expected_sha:
        raise RuntimeError(
            "corpus SHA mismatch"
        )

    prompt_ids = canonical[
        "prompt_ids"
    ]

    raw = {
        prompt: defaultdict(dict)
        for prompt in prompt_ids
    }

    with corpus_path.open(
        newline="",
        encoding="utf-8",
    ) as f:

        reader = csv.reader(f)

        header = next(reader)

        p_idx = header.index(
            "prompt_id"
        )

        l_idx = header.index(
            "layer"
        )

        t_idx = header.index(
            "token_index"
        )

        d_idx = header.index(
            "embedding_dimension"
        )

        vector_names = [
            f"v{i}"
            for i in range(
                EXPECTED_DIM
            )
        ]

        v_start = header.index(
            "v0"
        )

        if (
            header[
                v_start:
                v_start + EXPECTED_DIM
            ]
            != vector_names
        ):
            raise RuntimeError(
                "vector columns not contiguous"
            )

        rows = 0

        for row in reader:

            rows += 1

            prompt = row[p_idx]

            layer = int(
                row[l_idx]
            )

            token = int(
                row[t_idx]
            )

            dim = int(
                row[d_idx]
            )

            if dim != EXPECTED_DIM:
                raise RuntimeError(
                    "dimension mismatch"
                )

            if token == EXCLUDED_TOKEN:
                continue

            vector = np.asarray(
                row[
                    v_start:
                    v_start + EXPECTED_DIM
                ],
                dtype=np.float64,
            )

            raw[
                prompt
            ][
                token
            ][
                layer
            ] = vector

    if rows != 4068:
        raise RuntimeError(
            f"row count mismatch: {rows}"
        )

    tensors = {}
    token_lists = {}

    for prompt in prompt_ids:

        tokens = sorted(
            raw[prompt]
        )

        expected_tokens = [
            x
            for x
            in canonical[
                "per_prompt"
            ][
                prompt
            ][
                "token_indices"
            ]
            if x != EXCLUDED_TOKEN
        ]

        if tokens != expected_tokens:
            raise RuntimeError(
                f"token mismatch: {prompt}"
            )

        x = np.empty(
            (
                len(tokens),
                EXPECTED_LAYERS,
                EXPECTED_DIM,
            ),
            dtype=np.float64,
        )

        for ti, token in enumerate(
            tokens
        ):

            layers = raw[
                prompt
            ][
                token
            ]

            if sorted(layers) != list(
                range(
                    EXPECTED_LAYERS
                )
            ):
                raise RuntimeError(
                    f"incomplete trajectory: "
                    f"{prompt}/{token}"
                )

            for layer in range(
                EXPECTED_LAYERS
            ):
                x[
                    ti,
                    layer,
                    :,
                ] = layers[layer]

        norms = np.linalg.norm(
            x,
            axis=2,
            keepdims=True,
        )

        if np.any(norms == 0):
            raise RuntimeError(
                f"zero vector: {prompt}"
            )

        x /= norms

        tensors[prompt] = x
        token_lists[prompt] = tokens

    return (
        canonical,
        actual_sha,
        tensors,
        token_lists,
    )


def observed_delta_matrix(x):
    n = x.shape[0]

    flat = (
        x.transpose(
            1,
            0,
            2,
        )
        .reshape(
            EXPECTED_LAYERS,
            n * EXPECTED_DIM,
        )
    )

    same_sum = (
        flat
        @ flat.T
    )

    layer_sums = np.sum(
        x,
        axis=0,
    )

    total = (
        layer_sums
        @ layer_sums.T
    )

    same_mean = (
        same_sum / n
    )

    cross_mean = (
        total - same_sum
    ) / (
        n * (n - 1)
    )

    return (
        same_mean
        - cross_mean
    )


def selected_null(
    x,
    pairs,
    permutations,
    seed,
):
    n = x.shape[0]

    matrices = np.empty(
        (
            len(pairs),
            n,
            n,
        ),
        dtype=np.float64,
    )

    for i, (a, b) in enumerate(
        pairs
    ):
        matrices[i] = (
            x[:, a, :]
            @ x[:, b, :].T
        )

    totals = np.sum(
        matrices,
        axis=(1, 2),
    )

    rows = np.arange(n)

    identity_same = np.sum(
        matrices[
            :,
            rows,
            rows,
        ],
        axis=1,
    )

    identity_delta = (
        identity_same / n
        - (
            totals
            - identity_same
        ) / (
            n * (n - 1)
        )
    )

    observed = float(
        np.mean(
            identity_delta
        )
    )

    rng = np.random.default_rng(
        seed
    )

    null = np.empty(
        permutations,
        dtype=np.float64,
    )

    for i in range(
        permutations
    ):
        perm = rng.permutation(
            n
        )

        same_sum = np.sum(
            matrices[
                :,
                rows,
                perm,
            ],
            axis=1,
        )

        delta = (
            same_sum / n
            - (
                totals
                - same_sum
            ) / (
                n * (n - 1)
            )
        )

        null[i] = float(
            np.mean(
                delta
            )
        )

    return observed, null


def matrix_identity_selftest():
    rng = np.random.default_rng(
        99173
    )

    for n in (
        3,
        7,
        13,
    ):
        c = rng.normal(
            size=(n, n)
        )

        total = float(
            np.sum(c)
        )

        for _ in range(20):

            perm = rng.permutation(
                n
            )

            same_sum = sum(
                c[i, perm[i]]
                for i in range(n)
            )

            explicit_cross = []

            for ta in range(n):
                for tb in range(n):

                    if ta == tb:
                        continue

                    explicit_cross.append(
                        c[
                            ta,
                            perm[tb],
                        ]
                    )

            explicit = (
                same_sum / n
                - statistics.mean(
                    explicit_cross
                )
            )

            algebraic = (
                same_sum / n
                - (
                    total
                    - same_sum
                ) / (
                    n * (n - 1)
                )
            )

            if abs(
                explicit
                - algebraic
            ) > 1e-12:
                raise RuntimeError(
                    "permutation algebra "
                    "self-test failed"
                )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--corpus",
        default=DEFAULT_CORPUS,
    )

    parser.add_argument(
        "--canonical",
        default=DEFAULT_CANONICAL,
    )

    parser.add_argument(
        "--permutations",
        type=int,
        default=1000,
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=1337,
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=50,
    )

    parser.add_argument(
        "--json-out",
    )

    args = parser.parse_args()

    if args.permutations < 1:
        raise SystemExit(
            "permutations must be >= 1"
        )

    if args.top_k < 1:
        raise SystemExit(
            "top-k must be >= 1"
        )

    started = time.monotonic()

    matrix_identity_selftest()

    load_started = time.monotonic()

    (
        canonical,
        corpus_sha,
        tensors,
        token_lists,
    ) = load_corpus(
        args.corpus,
        args.canonical,
    )

    load_seconds = (
        time.monotonic()
        - load_started
    )

    prompts = canonical[
        "prompt_ids"
    ]

    pairs = [
        (a, b)
        for a in range(
            EXPECTED_LAYERS
        )
        for b in range(
            a + 1,
            EXPECTED_LAYERS
        )
    ]

    if len(pairs) != 630:
        raise RuntimeError(
            "layer-pair count mismatch"
        )

    if args.top_k > len(pairs):
        raise RuntimeError(
            "top-k exceeds layer pairs"
        )

    pair_index = {
        pair: i
        for i, pair
        in enumerate(pairs)
    }

    prompt_delta = {}

    for prompt in prompts:

        matrix = observed_delta_matrix(
            tensors[prompt]
        )

        prompt_delta[prompt] = np.asarray(
            [
                matrix[a, b]
                for a, b in pairs
            ],
            dtype=np.float64,
        )

    results = []

    print(
        "=" * 88
    )

    print(
        " OPENMIND / QWEN-2048 LOPO RECURRENCE V1"
    )

    print(
        "=" * 88
    )

    print(
        f"Corpus SHA           : {corpus_sha}"
    )

    print(
        f"Prompts              : {len(prompts)}"
    )

    print(
        f"Layers               : {EXPECTED_LAYERS}"
    )

    print(
        f"Layer pairs          : {len(pairs)}"
    )

    print(
        f"Excluded token       : T00"
    )

    print(
        f"Top K                : {args.top_k}"
    )

    print(
        f"Permutations         : {args.permutations}"
    )

    print(
        f"Seed                 : {args.seed}"
    )

    print(
        f"Corpus load seconds  : {load_seconds:.3f}"
    )

    print()

    for split_index, heldout in enumerate(
        prompts
    ):

        training = [
            prompt
            for prompt in prompts
            if prompt != heldout
        ]

        train_stack = np.stack(
            [
                prompt_delta[prompt]
                for prompt in training
            ],
            axis=0,
        )

        train_score = np.mean(
            train_stack,
            axis=0,
        )

        # Deterministic tie break:
        # descending score, then ascending
        # canonical pair index.
        selected_indices = sorted(
            range(
                len(pairs)
            ),
            key=lambda i: (
                -float(
                    train_score[i]
                ),
                i,
            ),
        )[
            :args.top_k
        ]

        selected_pairs = [
            pairs[i]
            for i in selected_indices
        ]

        held = prompt_delta[
            heldout
        ]

        selected_direct = float(
            np.mean(
                held[
                    selected_indices
                ]
            )
        )

        observed, null = selected_null(
            tensors[heldout],
            selected_pairs,
            args.permutations,
            args.seed + split_index,
        )

        if abs(
            selected_direct
            - observed
        ) > 1e-12:
            raise RuntimeError(
                "heldout direct/cache "
                "equivalence failure"
            )

        exceed = int(
            np.sum(
                null >= observed
            )
        )

        p = (
            exceed + 1
        ) / (
            args.permutations + 1
        )

        null_mean = float(
            np.mean(null)
        )

        if args.permutations > 1:
            null_sd = float(
                np.std(
                    null,
                    ddof=1,
                )
            )
        else:
            null_sd = 0.0

        if null_sd == 0:
            z = 0.0
        else:
            z = (
                observed
                - null_mean
            ) / null_sd

        rho = spearman(
            train_score,
            held,
        )

        all_mean = float(
            np.mean(
                held
            )
        )

        enrichment = (
            observed
            - all_mean
        )

        positive_fraction = float(
            np.mean(
                held[
                    selected_indices
                ] > 0
            )
        )

        split_pass = (
            observed > 0
            and p <= 0.01
        )

        top10 = [
            {
                "pair":
                    f"L{a:02d}<->L{b:02d}",

                "gap":
                    b - a,

                "training_delta":
                    float(
                        train_score[
                            pair_index[
                                (a, b)
                            ]
                        ]
                    ),

                "heldout_delta":
                    float(
                        held[
                            pair_index[
                                (a, b)
                            ]
                        ]
                    ),
            }
            for a, b in selected_pairs[:10]
        ]

        result = {
            "split":
                f"LOPO_{heldout}",

            "heldout_prompt":
                heldout,

            "training_prompts":
                training,

            "training_trajectories":
                sum(
                    len(
                        token_lists[prompt]
                    )
                    for prompt in training
                ),

            "heldout_trajectories":
                len(
                    token_lists[
                        heldout
                    ]
                ),

            "split_seed":
                args.seed
                + split_index,

            "selected_mean_delta":
                observed,

            "heldout_all_pair_mean_delta":
                all_mean,

            "selected_enrichment":
                enrichment,

            "null_mean":
                null_mean,

            "null_sd":
                null_sd,

            "z":
                z,

            "exceedances":
                exceed,

            "empirical_p":
                p,

            "spearman_training_vs_heldout":
                rho,

            "selected_positive_fraction":
                positive_fraction,

            "primary_split_pass":
                split_pass,

            "top10_selected":
                top10,
        }

        results.append(
            result
        )

        print(
            f"{result['split']:8s} "
            f"train={result['training_trajectories']:3d} "
            f"test={result['heldout_trajectories']:2d} "
            f"delta={observed:+.6f} "
            f"null={null_mean:+.6f} "
            f"z={z:+.3f} "
            f"p={p:.6f} "
            f"rho={rho:+.3f} "
            f"enrich={enrichment:+.6f} "
            f"positive={positive_fraction:.3f}"
        )

    total_seconds = (
        time.monotonic()
        - started
    )

    split_passes = sum(
        x[
            "primary_split_pass"
        ]
        for x in results
    )

    print()

    print(
        f"engineering split passes : "
        f"{split_passes}/8"
    )

    print(
        f"total runtime seconds     : "
        f"{total_seconds:.3f}"
    )

    print(
        "scientific final          : "
        + (
            "YES"
            if args.permutations == 1000
            else "NO"
        )
    )

    payload = {
        "schema":
            "openmind.qwen2048_lopo_recurrence."
            "result.v1",

        "corpus_sha256":
            corpus_sha,

        "permutations":
            args.permutations,

        "seed":
            args.seed,

        "top_k":
            args.top_k,

        "layer_pairs":
            len(pairs),

        "excluded_token":
            EXCLUDED_TOKEN,

        "corpus_load_seconds":
            load_seconds,

        "total_runtime_seconds":
            total_seconds,

        "splits":
            results,

        "split_passes":
            split_passes,

        "scientific_final":
            args.permutations
            == 1000,

        "final_gate":
            (
                "PASS"
                if (
                    args.permutations == 1000
                    and split_passes == 8
                )
                else (
                    "HOLD"
                    if args.permutations == 1000
                    else "NOT_APPLICABLE_SMOKE"
                )
            ),
    }

    if args.json_out:

        path = Path(
            args.json_out
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                payload,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )


if __name__ == "__main__":
    main()
