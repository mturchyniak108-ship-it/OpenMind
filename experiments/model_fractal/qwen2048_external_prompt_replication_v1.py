#!/usr/bin/env python3

import argparse
import csv
import hashlib
import importlib.util
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np


PROTOCOL_PATH = (
    "experiments/data/manifests/"
    "qwen2048_external_prompt_replication_v1_protocol.json"
)

CORPUS_MANIFEST_PATH = (
    "experiments/data/manifests/"
    "qwen2048_external_prompt_replication_v1_canonical_v1.json"
)

LOPO_ENGINE_PATH = (
    "experiments/model_fractal/"
    "qwen2048_lopo_recurrence_v1.py"
)

GAP_ENGINE_PATH = (
    "experiments/model_fractal/"
    "qwen2048_lopo_gap_matched_v1.py"
)


EXPECTED_PROTOCOL_SHA = (
    "8a3a492c05220b23a8b4324640563b043"
    "9238faef43fb7c97b4de2bba7489ec0"
)

EXPECTED_CORPUS_MANIFEST_SHA = (
    "e955ab3eef83addf977294fcbecae34c9"
    "412c49bf695196bc92694e13b643431"
)

EXPECTED_CANONICAL_SHA = (
    "d51422d9c89da5a469e328297362faa23"
    "887e03a9c7dd56e19e00260c7a5835d"
)

EXPECTED_LOPO_SHA = (
    "0b30157669e3be64e16c120c6b2da1e7"
    "ad9ebd4c24d3e52f59d071ff2b2608e7"
)

EXPECTED_GAP_SHA = (
    "74b0c20bef7ff6dcc8ca15fe7250cc9f"
    "453192e182c6f05d58e08b09264d11d1"
)

EXPECTED_SELECTION_SHA = (
    "945c826494a62c20ba52a8f4ae1b0133"
    "a3d8686f0a7fc23dc336666863992e7a"
)


PROMPT_IDS = [
    "R01",
    "R02",
    "R03",
    "R04",
    "R05",
    "R06",
    "R07",
    "R08",
]

LAYERS = 36
DIMENSIONS = 2048
TOP_K = 50
PAIR_COUNT = 630


def sha256(path):
    path = Path(path)

    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(
            lambda: f.read(
                1024 * 1024
            ),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()


def load_json(path):
    with Path(path).open() as f:
        return json.load(f)


def load_module(path, name):
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
            f"cannot import {path}"
        )

    module = (
        importlib.util
        .module_from_spec(spec)
    )

    spec.loader.exec_module(
        module
    )

    return module


def canonical_pairs():
    pairs = [
        (a, b)
        for a in range(LAYERS)
        for b in range(
            a + 1,
            LAYERS,
        )
    ]

    if len(pairs) != PAIR_COUNT:
        raise RuntimeError(
            "canonical pair count mismatch"
        )

    return pairs


def verify_base_contract(
    protocol_path,
    include_corpus=False,
    corpus_manifest_path=None,
):
    if (
        sha256(protocol_path)
        != EXPECTED_PROTOCOL_SHA
    ):
        raise RuntimeError(
            "protocol SHA mismatch"
        )

    if (
        sha256(LOPO_ENGINE_PATH)
        != EXPECTED_LOPO_SHA
    ):
        raise RuntimeError(
            "LOPO engine SHA mismatch"
        )

    if (
        sha256(GAP_ENGINE_PATH)
        != EXPECTED_GAP_SHA
    ):
        raise RuntimeError(
            "gap engine SHA mismatch"
        )

    protocol = load_json(
        protocol_path
    )

    if (
        protocol["status"]
        != "PREREGISTERED"
    ):
        raise RuntimeError(
            "protocol status mismatch"
        )

    if (
        protocol[
            "reference_topology"
        ][
            "may_be_retrained_on_replication_prompts"
        ]
        is not False
    ):
        raise RuntimeError(
            "topology retraining contract changed"
        )

    if (
        protocol[
            "reference_topology"
        ][
            "selection_sha256"
        ]
        != EXPECTED_SELECTION_SHA
    ):
        raise RuntimeError(
            "selection SHA mismatch"
        )

    corpus_manifest = None

    if include_corpus:

        if corpus_manifest_path is None:
            raise RuntimeError(
                "missing corpus manifest"
            )

        if (
            sha256(
                corpus_manifest_path
            )
            != EXPECTED_CORPUS_MANIFEST_SHA
        ):
            raise RuntimeError(
                "corpus manifest SHA mismatch"
            )

        corpus_manifest = load_json(
            corpus_manifest_path
        )

        if (
            corpus_manifest["status"]
            != "CANONICAL_FROZEN"
        ):
            raise RuntimeError(
                "corpus status mismatch"
            )

        corpus = corpus_manifest[
            "canonical_corpus"
        ]

        if (
            corpus["sha256"]
            != EXPECTED_CANONICAL_SHA
        ):
            raise RuntimeError(
                "canonical SHA contract mismatch"
            )

        if (
            sha256(
                corpus["path"]
            )
            != EXPECTED_CANONICAL_SHA
        ):
            raise RuntimeError(
                "canonical file SHA mismatch"
            )

    return (
        protocol,
        corpus_manifest,
    )


def load_frozen_modules():
    lopo = load_module(
        LOPO_ENGINE_PATH,
        "openmind_frozen_lopo_v1",
    )

    gap = load_module(
        GAP_ENGINE_PATH,
        "openmind_frozen_gap_v1",
    )

    return lopo, gap


def build_gap_pools(pairs):
    pools = {}

    for index, (
        a,
        b,
    ) in enumerate(pairs):

        gap = b - a

        pools.setdefault(
            gap,
            [],
        ).append(
            index
        )

    return pools


def protocol_gap_counts(
    protocol,
):
    counts = {
        int(gap): int(count)
        for gap, count in (
            protocol[
                "reference_topology"
            ][
                "gap_counts"
            ].items()
        )
    }

    if sum(
        counts.values()
    ) != TOP_K:
        raise RuntimeError(
            "gap counts do not total 50"
        )

    return counts


def reference_selection(
    protocol,
    pairs,
    gap_module,
):
    pair_index = {
        pair: i
        for i, pair
        in enumerate(pairs)
    }

    rows = sorted(
        protocol[
            "reference_topology"
        ][
            "pairs"
        ],
        key=lambda row: row["rank"],
    )

    if len(rows) != TOP_K:
        raise RuntimeError(
            "reference topology size mismatch"
        )

    selected = []

    for expected_rank, row in enumerate(
        rows,
        start=1,
    ):
        if (
            row["rank"]
            != expected_rank
        ):
            raise RuntimeError(
                "reference rank mismatch"
            )

        pair = (
            int(row["layer_a"]),
            int(row["layer_b"]),
        )

        if pair not in pair_index:
            raise RuntimeError(
                f"invalid reference pair {pair}"
            )

        if (
            int(row["gap"])
            != pair[1] - pair[0]
        ):
            raise RuntimeError(
                "reference gap mismatch"
            )

        selected.append(
            pair_index[pair]
        )

    if len(
        set(selected)
    ) != TOP_K:
        raise RuntimeError(
            "duplicate reference pair"
        )

    actual_gaps = Counter(
        pairs[i][1]
        - pairs[i][0]
        for i in selected
    )

    expected_gaps = (
        protocol_gap_counts(
            protocol
        )
    )

    if dict(
        sorted(
            actual_gaps.items()
        )
    ) != dict(
        sorted(
            expected_gaps.items()
        )
    ):
        raise RuntimeError(
            "reference gap profile mismatch"
        )

    frozen_pairs = (
        gap_module
        .canonical_pairs()
    )

    if list(
        frozen_pairs
    ) != pairs:
        raise RuntimeError(
            "predecessor canonical pair order mismatch"
        )

    selection_sha = (
        gap_module
        .pair_selection_hash(
            pairs,
            selected,
        )
    )

    if (
        selection_sha
        != EXPECTED_SELECTION_SHA
    ):
        raise RuntimeError(
            "reference selection hash mismatch"
        )

    return (
        selected,
        expected_gaps,
    )


def deterministic_gap_baseline(
    delta,
    pools,
    gap_counts,
):
    total = 0.0

    for gap, count in sorted(
        gap_counts.items()
    ):
        pool = pools.get(
            gap
        )

        if not pool:
            raise RuntimeError(
                f"missing gap pool {gap}"
            )

        mean_for_gap = float(
            np.mean(
                delta[pool]
            )
        )

        total += (
            count
            * mean_for_gap
        )

    return total / TOP_K


def draw_gap_matched_indices(
    rng,
    pools,
    gap_counts,
):
    selected = []

    for gap, count in sorted(
        gap_counts.items()
    ):
        pool = np.asarray(
            pools[gap],
            dtype=np.int64,
        )

        if count > len(pool):
            raise RuntimeError(
                f"gap {gap} pool too small"
            )

        draw = rng.choice(
            pool,
            size=count,
            replace=False,
        )

        selected.extend(
            int(x)
            for x in draw
        )

    if len(selected) != TOP_K:
        raise RuntimeError(
            "matched draw size mismatch"
        )

    if len(
        set(selected)
    ) != TOP_K:
        raise RuntimeError(
            "matched draw duplicate"
        )

    return selected


def direct_pair_delta(
    x,
    a,
    b,
):
    left = x[:, a, :]
    right = x[:, b, :]

    similarity = (
        left
        @ right.T
    )

    n = similarity.shape[0]

    if n < 2:
        raise RuntimeError(
            "need at least two tokens"
        )

    diagonal = float(
        np.trace(
            similarity
        )
    )

    same = (
        diagonal
        / n
    )

    cross = (
        (
            float(
                np.sum(
                    similarity
                )
            )
            - diagonal
        )
        /
        (
            n
            * (n - 1)
        )
    )

    return same - cross


def normalize_tensor(x):
    norms = np.linalg.norm(
        x,
        axis=2,
        keepdims=True,
    )

    if np.any(
        norms == 0
    ):
        raise RuntimeError(
            "zero activation vector"
        )

    return x / norms


def synthetic_selftest(
    protocol_path,
):
    protocol, _ = (
        verify_base_contract(
            protocol_path,
            include_corpus=False,
        )
    )

    lopo, gap = (
        load_frozen_modules()
    )

    pairs = canonical_pairs()

    (
        selected,
        gap_counts,
    ) = reference_selection(
        protocol,
        pairs,
        gap,
    )

    pools = build_gap_pools(
        pairs
    )

    rng = np.random.default_rng(
        99173
    )

    x = rng.normal(
        size=(
            7,
            LAYERS,
            DIMENSIONS,
        )
    )

    x = normalize_tensor(
        x
    )

    matrix = (
        lopo
        .observed_delta_matrix(
            x
        )
    )

    test_indices = [
        0,
        1,
        2,
        7,
        15,
        31,
        63,
        95,
        127,
        191,
        255,
        319,
        383,
        447,
        511,
        575,
        629,
    ]

    max_delta_diff = 0.0

    for index in test_indices:

        a, b = pairs[index]

        direct = (
            direct_pair_delta(
                x,
                a,
                b,
            )
        )

        frozen = float(
            matrix[a, b]
        )

        max_delta_diff = max(
            max_delta_diff,
            abs(
                direct
                - frozen
            ),
        )

    if max_delta_diff > 1e-12:
        raise RuntimeError(
            "delta algebra selftest failed"
        )

    draw_rng = (
        np.random.default_rng(
            99174
        )
    )

    exact_gap_draws = 256

    for _ in range(
        exact_gap_draws
    ):
        draw = (
            draw_gap_matched_indices(
                draw_rng,
                pools,
                gap_counts,
            )
        )

        actual = Counter(
            pairs[i][1]
            - pairs[i][0]
            for i in draw
        )

        if dict(
            sorted(
                actual.items()
            )
        ) != dict(
            sorted(
                gap_counts.items()
            )
        ):
            raise RuntimeError(
                "exact-gap draw selftest failed"
            )

    synthetic_delta = rng.normal(
        size=len(pairs)
    )

    baseline = (
        deterministic_gap_baseline(
            synthetic_delta,
            pools,
            gap_counts,
        )
    )

    expanded = []

    for gap_id, count in sorted(
        gap_counts.items()
    ):
        gap_mean = float(
            np.mean(
                synthetic_delta[
                    pools[gap_id]
                ]
            )
        )

        expanded.extend(
            [gap_mean] * count
        )

    direct_baseline = float(
        np.mean(
            expanded
        )
    )

    baseline_diff = abs(
        baseline
        - direct_baseline
    )

    if baseline_diff > 1e-15:
        raise RuntimeError(
            "baseline identity selftest failed"
        )

    p_values = [
        0.01,
        0.04,
        0.03,
    ]

    holm = (
        gap
        .holm_adjust(
            p_values
        )
    )

    expected_holm = [
        0.03,
        0.06,
        0.06,
    ]

    holm_diff = max(
        abs(
            float(a)
            - float(b)
        )
        for a, b in zip(
            holm,
            expected_holm,
        )
    )

    if holm_diff > 1e-15:
        raise RuntimeError(
            "Holm selftest failed"
        )

    selected_gap_counts = Counter(
        pairs[i][1]
        - pairs[i][0]
        for i in selected
    )

    payload = {
        "schema":
            "openmind.qwen2048_external_prompt_replication."
            "engine_selftest.v1",

        "status":
            "SELFTEST_PASS",

        "mode":
            "SYNTHETIC_ONLY",

        "real_replication_corpus_loaded":
            False,

        "replication_endpoint_calculated":
            False,

        "protocol_sha256":
            sha256(
                protocol_path
            ),

        "lopo_engine_sha256":
            sha256(
                LOPO_ENGINE_PATH
            ),

        "gap_engine_sha256":
            sha256(
                GAP_ENGINE_PATH
            ),

        "pair_count":
            len(pairs),

        "selected_pair_count":
            len(selected),

        "selection_sha256":
            EXPECTED_SELECTION_SHA,

        "gap_counts": {
            str(k): int(v)
            for k, v in sorted(
                selected_gap_counts.items()
            )
        },

        "delta_algebra": {
            "comparisons":
                len(
                    test_indices
                ),

            "max_abs_diff":
                max_delta_diff,

            "status":
                "PASS",
        },

        "exact_gap_randomization": {
            "draws_checked":
                exact_gap_draws,

            "status":
                "PASS",
        },

        "deterministic_gap_baseline": {
            "max_abs_diff":
                baseline_diff,

            "status":
                "PASS",
        },

        "holm_bonferroni": {
            "max_abs_diff":
                holm_diff,

            "status":
                "PASS",
        },

        "scientific_boundary": [
            "Synthetic vectors only.",
            "Frozen predecessor engines were imported by exact SHA256 contract.",
            "The canonical replication corpus was not loaded.",
            "No R01-R08 recurrence statistic was calculated.",
            "No prospective primary endpoint was calculated.",
        ],
    }

    return payload


def load_replication_tensors(
    corpus_manifest,
):
    corpus = corpus_manifest[
        "canonical_corpus"
    ]

    path = Path(
        corpus["path"]
    )

    source_map = {
        row["prompt_id"]:
            row
        for row in (
            corpus_manifest[
                "sources"
            ]
        )
    }

    if list(
        source_map
    ) != PROMPT_IDS:
        raise RuntimeError(
            "replication prompt order mismatch"
        )

    arrays = {}
    seen = {}

    for prompt_id in PROMPT_IDS:
        n_tokens = int(
            source_map[
                prompt_id
            ][
                "tokens"
            ]
        )

        arrays[prompt_id] = (
            np.empty(
                (
                    n_tokens,
                    LAYERS,
                    DIMENSIONS,
                ),
                dtype=np.float64,
            )
        )

        seen[prompt_id] = (
            np.zeros(
                (
                    n_tokens,
                    LAYERS,
                ),
                dtype=bool,
            )
        )

    expected_header = [
        "prompt_id",
        "layer",
        "token_index",
        "embedding_dimension",
    ] + [
        f"v{i}"
        for i in range(
            DIMENSIONS
        )
    ]

    with path.open(
        newline="",
        encoding="utf-8",
    ) as f:

        reader = csv.reader(
            f
        )

        try:
            header = next(
                reader
            )
        except StopIteration:
            raise RuntimeError(
                "empty canonical corpus"
            )

        if (
            header
            != expected_header
        ):
            raise RuntimeError(
                "canonical schema mismatch"
            )

        for row in reader:

            if len(row) != len(
                expected_header
            ):
                raise RuntimeError(
                    "canonical row width mismatch"
                )

            prompt_id = row[0]
            layer = int(
                row[1]
            )
            token = int(
                row[2]
            )
            dimension = int(
                row[3]
            )

            if prompt_id not in arrays:
                raise RuntimeError(
                    "unexpected prompt id"
                )

            if dimension != DIMENSIONS:
                raise RuntimeError(
                    "dimension mismatch"
                )

            if not (
                0 <= layer < LAYERS
            ):
                raise RuntimeError(
                    "layer mismatch"
                )

            if not (
                0 <= token
                < arrays[
                    prompt_id
                ].shape[0]
            ):
                raise RuntimeError(
                    "token mismatch"
                )

            if seen[
                prompt_id
            ][
                token,
                layer,
            ]:
                raise RuntimeError(
                    "duplicate corpus row"
                )

            vector = np.asarray(
                row[4:],
                dtype=np.float64,
            )

            if vector.shape != (
                DIMENSIONS,
            ):
                raise RuntimeError(
                    "vector width mismatch"
                )

            if not np.all(
                np.isfinite(
                    vector
                )
            ):
                raise RuntimeError(
                    "non-finite activation"
                )

            arrays[
                prompt_id
            ][
                token,
                layer,
                :,
            ] = vector

            seen[
                prompt_id
            ][
                token,
                layer,
            ] = True

    result = {}

    for prompt_id in PROMPT_IDS:

        if not np.all(
            seen[
                prompt_id
            ]
        ):
            raise RuntimeError(
                f"{prompt_id} incomplete corpus"
            )

        x = arrays[
            prompt_id
        ][
            1:,
            :,
            :,
        ]

        if x.shape[0] < 2:
            raise RuntimeError(
                f"{prompt_id} too few active tokens"
            )

        result[
            prompt_id
        ] = normalize_tensor(
            x
        )

    return result


def run_analysis(
    protocol_path,
    corpus_manifest_path,
):
    (
        protocol,
        corpus_manifest,
    ) = verify_base_contract(
        protocol_path,
        include_corpus=True,
        corpus_manifest_path=(
            corpus_manifest_path
        ),
    )

    lopo, gap = (
        load_frozen_modules()
    )

    pairs = canonical_pairs()

    (
        selected,
        gap_counts,
    ) = reference_selection(
        protocol,
        pairs,
        gap,
    )

    pools = build_gap_pools(
        pairs
    )

    tensors = (
        load_replication_tensors(
            corpus_manifest
        )
    )

    prompt_deltas = {}

    for prompt_id in PROMPT_IDS:

        matrix = (
            lopo
            .observed_delta_matrix(
                tensors[
                    prompt_id
                ]
            )
        )

        prompt_deltas[
            prompt_id
        ] = np.asarray(
            [
                float(
                    matrix[a, b]
                )
                for a, b in pairs
            ],
            dtype=np.float64,
        )

    random_draws = int(
        protocol[
            "per_prompt_statistic"
        ][
            "random_draws"
        ]
    )

    base_seed = int(
        protocol[
            "per_prompt_statistic"
        ][
            "base_seed"
        ]
    )

    prompt_results = []

    observed_enrichments = []

    baselines = {}

    for prompt_index, prompt_id in enumerate(
        PROMPT_IDS
    ):

        delta = prompt_deltas[
            prompt_id
        ]

        observed = float(
            np.mean(
                delta[
                    selected
                ]
            )
        )

        baseline = (
            deterministic_gap_baseline(
                delta,
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

        baselines[
            prompt_id
        ] = baseline

        rng = (
            np.random.default_rng(
                base_seed
                + prompt_index
            )
        )

        exceed = 0

        random_sum = 0.0
        random_sq_sum = 0.0

        for _ in range(
            random_draws
        ):

            draw = (
                draw_gap_matched_indices(
                    rng,
                    pools,
                    gap_counts,
                )
            )

            value = float(
                np.mean(
                    delta[
                        draw
                    ]
                )
            )

            random_sum += value
            random_sq_sum += (
                value
                * value
            )

            if value >= observed:
                exceed += 1

        random_mean = (
            random_sum
            / random_draws
        )

        variance = max(
            0.0,
            (
                random_sq_sum
                / random_draws
            )
            - (
                random_mean
                * random_mean
            ),
        )

        random_sd = math.sqrt(
            variance
        )

        p_value = (
            exceed + 1
        ) / (
            random_draws + 1
        )

        prompt_results.append({
            "prompt_id":
                prompt_id,

            "seed":
                base_seed
                + prompt_index,

            "active_tokens":
                int(
                    tensors[
                        prompt_id
                    ].shape[0]
                ),

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

            "draws":
                random_draws,

            "empirical_p":
                p_value,
        })

    adjusted = (
        gap
        .holm_adjust(
            [
                row[
                    "empirical_p"
                ]
                for row in (
                    prompt_results
                )
            ]
        )
    )

    for row, value in zip(
        prompt_results,
        adjusted,
    ):
        row[
            "holm_adjusted_p"
        ] = float(
            value
        )

    observed_global = float(
        np.mean(
            observed_enrichments
        )
    )

    global_draws = int(
        protocol[
            "primary_endpoint"
        ][
            "global_random_draws"
        ]
    )

    global_seed = int(
        protocol[
            "primary_endpoint"
        ][
            "global_seed"
        ]
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

        randomized = []

        for prompt_id in PROMPT_IDS:

            delta = prompt_deltas[
                prompt_id
            ]

            draw = (
                draw_gap_matched_indices(
                    global_rng,
                    pools,
                    gap_counts,
                )
            )

            random_mean = float(
                np.mean(
                    delta[
                        draw
                    ]
                )
            )

            randomized.append(
                random_mean
                - baselines[
                    prompt_id
                ]
            )

        value = float(
            np.mean(
                randomized
            )
        )

        global_sum += value
        global_sq_sum += (
            value
            * value
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

    positive_prompts = sum(
        1
        for row in prompt_results
        if (
            row[
                "gap_adjusted_enrichment"
            ]
            > 0
        )
    )

    strong_prompts = sum(
        1
        for row in prompt_results
        if (
            row[
                "gap_adjusted_enrichment"
            ]
            > 0
            and row[
                "holm_adjusted_p"
            ]
            <= 0.05
        )
    )

    primary_pass = (
        observed_global > 0
        and global_p <= 0.01
    )

    payload = {
        "schema":
            "openmind.qwen2048_external_prompt_replication."
            "result.v1",

        "status":
            (
                "PRIMARY_PASS"
                if primary_pass
                else "PRIMARY_FAIL"
            ),

        "engine_sha256":
            sha256(
                __file__
            ),

        "protocol_sha256":
            sha256(
                protocol_path
            ),

        "corpus_manifest_sha256":
            sha256(
                corpus_manifest_path
            ),

        "canonical_corpus_sha256":
            EXPECTED_CANONICAL_SHA,

        "reference_topology": {
            "selection_sha256":
                EXPECTED_SELECTION_SHA,

            "selected_pair_count":
                TOP_K,

            "gap_counts": {
                str(k): int(v)
                for k, v in sorted(
                    gap_counts.items()
                )
            },

            "retrained":
                False,
        },

        "per_prompt":
            prompt_results,

        "primary_endpoint": {
            "observed_mean_gap_adjusted_enrichment":
                observed_global,

            "global_seed":
                global_seed,

            "draws":
                global_draws,

            "null_mean":
                global_null_mean,

            "null_sd":
                global_null_sd,

            "exceedances":
                global_exceed,

            "empirical_p":
                global_p,

            "pass":
                primary_pass,
        },

        "robustness": {
            "positive_prompts":
                positive_prompts,

            "positive_requirement_met":
                positive_prompts >= 7,

            "strong_prompts":
                strong_prompts,

            "strong_criterion_met":
                strong_prompts == 8,
        },

        "scientific_boundary": [
            "Reference topology was frozen before replication capture.",
            "Reference topology was not retrained on replication prompts.",
            "Token index zero was excluded from analysis.",
            "Exact frozen gap profile was used for matched randomization.",
            "Primary interpretation is determined only by the preregistered global endpoint.",
        ],
    }

    return payload


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--selftest-only",
        action="store_true",
    )

    parser.add_argument(
        "--protocol",
        default=PROTOCOL_PATH,
    )

    parser.add_argument(
        "--corpus-manifest",
        default=CORPUS_MANIFEST_PATH,
    )

    parser.add_argument(
        "--output",
    )

    args = parser.parse_args()

    if args.selftest_only:

        payload = (
            synthetic_selftest(
                args.protocol
            )
        )

        print(
            json.dumps(
                payload,
                indent=2,
                sort_keys=True,
            )
        )

        return

    if not args.output:
        raise SystemExit(
            "--output is required "
            "outside --selftest-only mode"
        )

    payload = run_analysis(
        args.protocol,
        args.corpus_manifest,
    )

    output = Path(
        args.output
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    print(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
