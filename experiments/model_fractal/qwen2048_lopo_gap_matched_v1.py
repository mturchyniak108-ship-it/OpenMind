#!/usr/bin/env python3

import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path

import numpy as np


DEFAULT_PROTOCOL = (
    "experiments/data/manifests/"
    "qwen2048_lopo_gap_matched_v1_protocol.json"
)

EXPECTED_LAYERS = 36
EXPECTED_PAIRS = 630
TOP_K = 50


def sha256(path):
    path = Path(path)

    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()


def load_json(path):
    with Path(path).open() as f:
        return json.load(f)


def load_module(path, name):
    path = Path(path)

    spec = (
        importlib.util
        .spec_from_file_location(
            name,
            path,
        )
    )

    if (
        spec is None
        or spec.loader is None
    ):
        raise RuntimeError(
            f"unable to import {path}"
        )

    module = (
        importlib.util
        .module_from_spec(
            spec
        )
    )

    spec.loader.exec_module(
        module
    )

    return module


def canonical_pairs():
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

    if len(pairs) != EXPECTED_PAIRS:
        raise RuntimeError(
            "canonical pair count mismatch"
        )

    return pairs


def pair_selection_hash(
    pairs,
    selected_indices,
):
    text = ",".join(
        f"{pairs[i][0]}-{pairs[i][1]}"
        for i in selected_indices
    )

    return hashlib.sha256(
        text.encode()
    ).hexdigest()


def build_gap_pools(pairs):
    pools = {}

    for i, (a, b) in enumerate(
        pairs
    ):
        gap = b - a

        pools.setdefault(
            gap,
            [],
        ).append(i)

    return pools


def normalize_gap_counts(
    raw_counts,
):
    counts = {
        int(gap):
            int(count)
        for gap, count
        in raw_counts.items()
    }

    if sum(
        counts.values()
    ) != TOP_K:
        raise RuntimeError(
            "gap counts do not total 50"
        )

    if any(
        count < 0
        for count in counts.values()
    ):
        raise RuntimeError(
            "negative gap count"
        )

    return counts


def gap_counts_for_selection(
    pairs,
    selected_indices,
):
    counts = {}

    for i in selected_indices:

        a, b = pairs[i]

        gap = b - a

        counts[gap] = (
            counts.get(
                gap,
                0,
            )
            + 1
        )

    return counts


def draw_gap_matched_indices(
    pools,
    gap_counts,
    rng,
):
    selected = []

    for gap in sorted(
        gap_counts
    ):

        count = gap_counts[
            gap
        ]

        pool = pools.get(
            gap
        )

        if pool is None:
            raise RuntimeError(
                f"missing gap pool {gap}"
            )

        if count > len(pool):
            raise RuntimeError(
                f"gap {gap}: "
                "requested count exceeds pool"
            )

        chosen = rng.choice(
            np.asarray(
                pool,
                dtype=np.int64,
            ),
            size=count,
            replace=False,
        )

        selected.extend(
            int(x)
            for x in chosen
        )

    if len(selected) != TOP_K:
        raise RuntimeError(
            "matched draw is not size 50"
        )

    if len(
        set(selected)
    ) != TOP_K:
        raise RuntimeError(
            "duplicate pair in matched draw"
        )

    return selected


def deterministic_gap_baseline(
    heldout_values,
    pools,
    gap_counts,
):
    total = 0.0

    for gap, count in (
        gap_counts.items()
    ):

        indices = pools[
            gap
        ]

        mean_for_gap = float(
            np.mean(
                heldout_values[
                    indices
                ]
            )
        )

        total += (
            count
            * mean_for_gap
        )

    return (
        total
        / TOP_K
    )


def matched_mean(
    heldout_values,
    indices,
):
    return float(
        np.mean(
            heldout_values[
                indices
            ]
        )
    )


def holm_adjust(p_values):
    p_values = [
        float(p)
        for p in p_values
    ]

    m = len(
        p_values
    )

    order = sorted(
        range(m),
        key=lambda i:
            (
                p_values[i],
                i,
            ),
    )

    adjusted = [
        0.0
        for _ in p_values
    ]

    running = 0.0

    for rank, index in enumerate(
        order
    ):

        factor = (
            m - rank
        )

        value = min(
            1.0,
            factor
            * p_values[index],
        )

        running = max(
            running,
            value,
        )

        adjusted[index] = (
            running
        )

    return adjusted


def verify_frozen_inputs(
    protocol,
):
    if (
        protocol.get("status")
        != "PREREGISTERED"
    ):
        raise RuntimeError(
            "protocol not preregistered"
        )

    frozen = protocol[
        "frozen_inputs"
    ]

    verified = {}

    for name, item in (
        frozen.items()
    ):

        path = Path(
            item["path"]
        )

        expected = item[
            "sha256"
        ]

        if not path.exists():
            raise RuntimeError(
                f"missing frozen input: "
                f"{path}"
            )

        actual = sha256(
            path
        )

        if actual != expected:
            raise RuntimeError(
                f"frozen hash mismatch: "
                f"{name}"
            )

        verified[
            name
        ] = actual

    return verified


def load_frozen_context(
    protocol_path,
):
    protocol_path = Path(
        protocol_path
    )

    protocol = load_json(
        protocol_path
    )

    verified = (
        verify_frozen_inputs(
            protocol
        )
    )

    canonical_item = (
        protocol[
            "frozen_inputs"
        ][
            "canonical"
        ]
    )

    engine_item = (
        protocol[
            "frozen_inputs"
        ][
            "engine"
        ]
    )

    audit_item = (
        protocol[
            "frozen_inputs"
        ][
            "engine_audit"
        ]
    )

    canonical = load_json(
        canonical_item["path"]
    )

    frozen_audit = load_json(
        audit_item["path"]
    )

    lopo_engine = load_module(
        engine_item["path"],
        "openmind_lopo_frozen",
    )

    corpus_path = Path(
        canonical[
            "corpus"
        ][
            "path"
        ]
    )

    (
        loaded_canonical,
        corpus_sha,
        tensors,
        token_lists,
    ) = lopo_engine.load_corpus(
        corpus_path,
        canonical_item["path"],
    )

    if (
        corpus_sha
        != canonical[
            "corpus"
        ][
            "sha256"
        ]
    ):
        raise RuntimeError(
            "corpus SHA mismatch"
        )

    return (
        protocol,
        canonical,
        frozen_audit,
        lopo_engine,
        tensors,
        token_lists,
        verified,
    )


def compute_prompt_deltas(
    prompts,
    tensors,
    lopo_engine,
    pairs,
):
    result = {}

    for prompt in prompts:

        matrix = (
            lopo_engine
            .observed_delta_matrix(
                tensors[prompt]
            )
        )

        result[
            prompt
        ] = np.asarray(
            [
                matrix[a, b]
                for a, b in pairs
            ],
            dtype=np.float64,
        )

    return result


def reconstruct_selections(
    protocol,
    canonical,
    frozen_audit,
    prompt_delta,
    pairs,
):
    prompts = canonical[
        "prompt_ids"
    ]

    expected_hashes = (
        protocol[
            "selection"
        ][
            "selection_hashes"
        ]
    )

    expected_profiles = (
        protocol[
            "selection"
        ][
            "gap_profiles"
        ]
    )

    frozen_hashes = (
        frozen_audit[
            "selection_hashes"
        ]
    )

    selections = {}

    for heldout in prompts:

        training = [
            prompt
            for prompt in prompts
            if prompt != heldout
        ]

        if len(training) != 7:
            raise RuntimeError(
                "training prompt count "
                "is not seven"
            )

        train_score = np.mean(
            np.stack(
                [
                    prompt_delta[
                        prompt
                    ]
                    for prompt
                    in training
                ],
                axis=0,
            ),
            axis=0,
        )

        selected = sorted(
            range(
                len(pairs)
            ),
            key=lambda i:
                (
                    -float(
                        train_score[i]
                    ),
                    i,
                ),
        )[:TOP_K]

        digest = (
            pair_selection_hash(
                pairs,
                selected,
            )
        )

        if (
            digest
            != expected_hashes[
                heldout
            ]
        ):
            raise RuntimeError(
                f"protocol selection "
                f"hash mismatch: "
                f"{heldout}"
            )

        if (
            digest
            != frozen_hashes[
                heldout
            ]
        ):
            raise RuntimeError(
                f"audit selection "
                f"hash mismatch: "
                f"{heldout}"
            )

        actual_counts = (
            gap_counts_for_selection(
                pairs,
                selected,
            )
        )

        expected_counts = (
            normalize_gap_counts(
                expected_profiles[
                    heldout
                ][
                    "gap_counts"
                ]
            )
        )

        if (
            actual_counts
            != expected_counts
        ):
            raise RuntimeError(
                f"gap profile mismatch: "
                f"{heldout}"
            )

        selections[
            heldout
        ] = {
            "training_prompts":
                training,

            "selected_indices":
                selected,

            "selection_hash":
                digest,

            "gap_counts":
                actual_counts,
        }

    return selections


def synthetic_selftest():
    # --------------------------------------------------------
    # Synthetic pair geometry
    # --------------------------------------------------------

    pairs = canonical_pairs()

    pools = build_gap_pools(
        pairs
    )

    gap_counts = {
        1: 19,
        2: 14,
        3: 8,
        4: 6,
        5: 1,
        6: 1,
        7: 1,
    }

    rng = np.random.default_rng(
        20260827
    )

    draws_checked = 0

    for _ in range(250):

        selected = (
            draw_gap_matched_indices(
                pools,
                gap_counts,
                rng,
            )
        )

        actual = (
            gap_counts_for_selection(
                pairs,
                selected,
            )
        )

        if actual != gap_counts:
            raise RuntimeError(
                "synthetic exact-gap "
                "sampling failure"
            )

        draws_checked += 1


    # --------------------------------------------------------
    # Deterministic baseline identity
    # --------------------------------------------------------

    values = rng.normal(
        size=len(pairs)
    )

    baseline = (
        deterministic_gap_baseline(
            values,
            pools,
            gap_counts,
        )
    )

    explicit = []

    for gap, count in (
        gap_counts.items()
    ):

        gap_mean = float(
            np.mean(
                values[
                    pools[gap]
                ]
            )
        )

        explicit.extend(
            [gap_mean] * count
        )

    direct_baseline = float(
        np.mean(
            explicit
        )
    )

    baseline_diff = abs(
        baseline
        - direct_baseline
    )

    if baseline_diff > 1e-15:
        raise RuntimeError(
            "synthetic baseline "
            "identity failure"
        )


    # --------------------------------------------------------
    # Selected-set eligibility
    #
    # Protocol explicitly leaves selected pairs
    # eligible in the random pool.
    # --------------------------------------------------------

    sentinel = set(
        pools[1][:19]
    )

    seen_sentinel = False

    rng2 = np.random.default_rng(
        991
    )

    for _ in range(200):

        selected = (
            draw_gap_matched_indices(
                pools,
                gap_counts,
                rng2,
            )
        )

        if (
            sentinel
            & set(selected)
        ):
            seen_sentinel = True
            break

    if not seen_sentinel:
        raise RuntimeError(
            "selected-eligible pool "
            "self-test failed"
        )


    # --------------------------------------------------------
    # Holm-Bonferroni known-value test
    # --------------------------------------------------------

    raw = [
        0.001,
        0.01,
        0.03,
        0.20,
    ]

    adjusted = holm_adjust(
        raw
    )

    expected = [
        0.004,
        0.03,
        0.06,
        0.20,
    ]

    holm_diff = max(
        abs(a - b)
        for a, b in zip(
            adjusted,
            expected,
        )
    )

    if holm_diff > 1e-15:
        raise RuntimeError(
            "Holm self-test failed"
        )


    # --------------------------------------------------------
    # Randomization mean sanity
    #
    # Gap-matched random-set means should center
    # near deterministic gap baseline.
    # Synthetic only.
    # --------------------------------------------------------

    rng3 = np.random.default_rng(
        7711
    )

    random_means = []

    for _ in range(5000):

        indices = (
            draw_gap_matched_indices(
                pools,
                gap_counts,
                rng3,
            )
        )

        random_means.append(
            matched_mean(
                values,
                indices,
            )
        )

    random_center = float(
        np.mean(
            random_means
        )
    )

    center_error = abs(
        random_center
        - baseline
    )

    # Monte Carlo sanity tolerance only.
    if center_error > 0.03:
        raise RuntimeError(
            "randomization center "
            "self-test failed"
        )

    return {
        "exact_gap_draws_checked":
            draws_checked,

        "baseline_identity_max_diff":
            baseline_diff,

        "holm_max_diff":
            holm_diff,

        "randomization_center_error":
            center_error,

        "selected_pairs_eligible":
            True,
    }


def run_control(
    protocol_path,
    output_path=None,
):
    (
        protocol,
        canonical,
        frozen_audit,
        lopo_engine,
        tensors,
        token_lists,
        verified,
    ) = load_frozen_context(
        protocol_path
    )

    pairs = canonical_pairs()

    pools = build_gap_pools(
        pairs
    )

    prompts = canonical[
        "prompt_ids"
    ]

    prompt_delta = (
        compute_prompt_deltas(
            prompts,
            tensors,
            lopo_engine,
            pairs,
        )
    )

    selections = (
        reconstruct_selections(
            protocol,
            canonical,
            frozen_audit,
            prompt_delta,
            pairs,
        )
    )

    split_draws = int(
        protocol[
            "gap_matched_baseline"
        ][
            "random_sets_per_split"
        ]
    )

    split_seed_base = int(
        protocol[
            "gap_matched_baseline"
        ][
            "base_seed"
        ]
    )

    global_draws = 10000

    global_seed = int(
        protocol[
            "primary_endpoint"
        ][
            "global_base_seed"
        ]
    )

    split_results = []

    observed_enrichments = []

    for split_index, heldout in enumerate(
        prompts
    ):

        held = prompt_delta[
            heldout
        ]

        selected = selections[
            heldout
        ][
            "selected_indices"
        ]

        gap_counts = selections[
            heldout
        ][
            "gap_counts"
        ]

        observed = matched_mean(
            held,
            selected,
        )

        baseline = (
            deterministic_gap_baseline(
                held,
                pools,
                gap_counts,
            )
        )

        enrichment = (
            observed
            - baseline
        )

        observed_enrichments.append(
            enrichment
        )

        rng = np.random.default_rng(
            split_seed_base
            + split_index
        )

        exceed = 0

        random_sum = 0.0

        random_sq_sum = 0.0

        for _ in range(
            split_draws
        ):

            indices = (
                draw_gap_matched_indices(
                    pools,
                    gap_counts,
                    rng,
                )
            )

            value = matched_mean(
                held,
                indices,
            )

            random_sum += value

            random_sq_sum += (
                value * value
            )

            if value >= observed:
                exceed += 1

        random_mean = (
            random_sum
            / split_draws
        )

        variance = max(
            0.0,
            (
                random_sq_sum
                / split_draws
            )
            - (
                random_mean
                * random_mean
            ),
        )

        random_sd = math.sqrt(
            variance
        )

        p = (
            exceed + 1
        ) / (
            split_draws + 1
        )

        split_results.append({
            "split":
                f"LOPO_{heldout}",

            "heldout_prompt":
                heldout,

            "selection_hash":
                selections[
                    heldout
                ][
                    "selection_hash"
                ],

            "gap_counts": {
                str(k): v
                for k, v
                in sorted(
                    gap_counts.items()
                )
            },

            "observed_selected_mean":
                observed,

            "deterministic_gap_baseline":
                baseline,

            "gap_adjusted_enrichment":
                enrichment,

            "matched_random_mean":
                random_mean,

            "matched_random_sd":
                random_sd,

            "exceedances":
                exceed,

            "empirical_p":
                p,
        })


    raw_p = [
        x["empirical_p"]
        for x in split_results
    ]

    adjusted_p = holm_adjust(
        raw_p
    )

    for result, adjusted in zip(
        split_results,
        adjusted_p,
    ):
        result[
            "holm_adjusted_p"
        ] = adjusted


    observed_global = float(
        np.mean(
            observed_enrichments
        )
    )

    global_rng = (
        np.random.default_rng(
            global_seed
        )
    )

    global_exceed = 0
    global_sum = 0.0
    global_sq_sum = 0.0

    for _ in range(
        global_draws
    ):

        randomized_enrichment = []

        for heldout in prompts:

            held = prompt_delta[
                heldout
            ]

            gap_counts = (
                selections[
                    heldout
                ][
                    "gap_counts"
                ]
            )

            baseline = (
                deterministic_gap_baseline(
                    held,
                    pools,
                    gap_counts,
                )
            )

            indices = (
                draw_gap_matched_indices(
                    pools,
                    gap_counts,
                    global_rng,
                )
            )

            random_mean = (
                matched_mean(
                    held,
                    indices,
                )
            )

            randomized_enrichment.append(
                random_mean
                - baseline
            )

        value = float(
            np.mean(
                randomized_enrichment
            )
        )

        global_sum += value

        global_sq_sum += (
            value * value
        )

        if value >= observed_global:
            global_exceed += 1

    global_null_mean = (
        global_sum
        / global_draws
    )

    global_variance = max(
        0.0,
        (
            global_sq_sum
            / global_draws
        )
        - (
            global_null_mean
            * global_null_mean
        ),
    )

    global_null_sd = math.sqrt(
        global_variance
    )

    global_p = (
        global_exceed + 1
    ) / (
        global_draws + 1
    )

    positive_splits = sum(
        x[
            "gap_adjusted_enrichment"
        ] > 0
        for x in split_results
    )

    strong_splits = sum(
        (
            x[
                "gap_adjusted_enrichment"
            ] > 0
            and x[
                "holm_adjusted_p"
            ] <= 0.05
        )
        for x in split_results
    )

    primary_pass = (
        observed_global > 0
        and global_p <= 0.01
    )

    payload = {
        "schema":
            "openmind.qwen2048_lopo_gap_matched."
            "result.v1",

        "protocol_sha256":
            sha256(
                protocol_path
            ),

        "split_draws":
            split_draws,

        "global_draws":
            global_draws,

        "split_seed_base":
            split_seed_base,

        "global_seed":
            global_seed,

        "splits":
            split_results,

        "positive_splits":
            positive_splits,

        "strong_all_prompt_count":
            strong_splits,

        "global": {
            "observed_mean_gap_adjusted_enrichment":
                observed_global,

            "null_mean":
                global_null_mean,

            "null_sd":
                global_null_sd,

            "exceedances":
                global_exceed,

            "empirical_p":
                global_p,

            "primary_pass":
                primary_pass,
        },

        "primary_gate":
            (
                "PASS"
                if primary_pass
                else "HOLD"
            ),
    }

    if output_path is not None:

        output_path = Path(
            output_path
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_text(
            json.dumps(
                payload,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )

    return payload


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--protocol",
        default=DEFAULT_PROTOCOL,
    )

    parser.add_argument(
        "--json-out",
    )

    parser.add_argument(
        "--self-test",
        action="store_true",
    )

    args = parser.parse_args()

    if args.self_test:

        result = synthetic_selftest()

        print(
            "synthetic self-test    : PASS"
        )

        for key, value in (
            result.items()
        ):
            print(
                f"{key:23s}: {value}"
            )

        return

    result = run_control(
        args.protocol,
        args.json_out,
    )

    print(
        "=" * 88
    )

    print(
        " OPENMIND / QWEN-2048 "
        "LOPO GAP-MATCHED CONTROL V1"
    )

    print(
        "=" * 88
    )

    print(
        f"split draws           : "
        f"{result['split_draws']}"
    )

    print(
        f"global draws          : "
        f"{result['global_draws']}"
    )

    print()

    for split in result[
        "splits"
    ]:

        print(
            f"{split['split']:8s} "
            f"obs="
            f"{split['observed_selected_mean']:+.6f} "
            f"gap="
            f"{split['deterministic_gap_baseline']:+.6f} "
            f"enrich="
            f"{split['gap_adjusted_enrichment']:+.6f} "
            f"p="
            f"{split['empirical_p']:.6f} "
            f"holm="
            f"{split['holm_adjusted_p']:.6f}"
        )

    print()

    print(
        f"positive splits       : "
        f"{result['positive_splits']}/8"
    )

    print(
        f"global enrichment     : "
        f"{result['global']['observed_mean_gap_adjusted_enrichment']:+.6f}"
    )

    print(
        f"global null mean      : "
        f"{result['global']['null_mean']:+.6f}"
    )

    print(
        f"global p              : "
        f"{result['global']['empirical_p']:.6f}"
    )

    print(
        f"primary gate          : "
        f"{result['primary_gate']}"
    )


if __name__ == "__main__":
    main()
