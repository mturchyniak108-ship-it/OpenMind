#!/usr/bin/env python3

import csv
import hashlib
import importlib.util
import json
import math
import struct
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]

EXTERNAL_ENGINE = ROOT / "experiments/model_fractal/qwen2048_external_prompt_replication_v1.py"
EXTERNAL_PROTOCOL = ROOT / "experiments/data/manifests/qwen2048_external_prompt_replication_v1_protocol.json"
CORPUS_MANIFEST = ROOT / "experiments/data/manifests/qwen2048_external_prompt_replication_v1_canonical_v1.json"

BRIDGE_PROTOCOL = ROOT / "experiments/data/manifests/forest_recurrence_bridge_v1_protocol.json"
BRIDGE_CLARIFICATION = ROOT / "experiments/data/manifests/forest_recurrence_bridge_v1_preexecution_clarification.json"
BRIDGE_ANALYSIS = ROOT / "experiments/data/manifests/forest_recurrence_bridge_v1_analysis_contract.json"

FOREST_PATH = ROOT / "results/forest_qwen25_3b_v1/forest_qwen25_3b_v1.bin"

DIM = 2048
GROUP_SIZE = 64
GROUP_COUNT = 32
BUDGETS = (4, 8, 16, 24, 32)
PRIMARY_BUDGETS = (4, 8, 16, 24)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_forest(path):
    raw = Path(path).read_bytes()

    expected = 24 + DIM * 4 + GROUP_COUNT * 4
    if len(raw) != expected:
        raise RuntimeError("Forest byte size mismatch")

    magic, version, dim, group_size, groups = struct.unpack(
        "<8sIIII", raw[:24]
    )

    if (magic, version, dim, group_size, groups) != (
        b"OMFRST01", 1, DIM, GROUP_SIZE, GROUP_COUNT
    ):
        raise RuntimeError("Forest header mismatch")

    offset = 24
    dimension_map = np.frombuffer(
        raw, dtype="<u4", count=DIM, offset=offset
    ).astype(np.int64)

    offset += DIM * 4
    ranking = np.frombuffer(
        raw, dtype="<u4", count=GROUP_COUNT, offset=offset
    ).astype(np.int64)

    if sorted(dimension_map.tolist()) != list(range(DIM)):
        raise RuntimeError("Forest dimension map is not a permutation")

    if sorted(ranking.tolist()) != list(range(GROUP_COUNT)):
        raise RuntimeError("Forest ranking is not a permutation")

    return dimension_map, ranking


def lround_away_from_zero(x):
    x = np.asarray(x, dtype=np.float32)
    return np.copysign(
        np.floor(np.abs(x) + np.float32(0.5)),
        x,
    )


def reconstruct_budget(
    source,
    budget,
    dimension_map,
    ranking,
):
    source = np.asarray(source, dtype=np.float32)

    if source.ndim != 2 or source.shape[1] != DIM:
        raise RuntimeError("codec source shape mismatch")

    if budget not in BUDGETS:
        raise RuntimeError("invalid Forest budget")

    reconstructed = np.zeros_like(source)

    for rank in range(budget):
        block = int(ranking[rank])

        dims = dimension_map[
            block * GROUP_SIZE:
            (block + 1) * GROUP_SIZE
        ]

        values = source[:, dims]
        peak = np.max(np.abs(values), axis=1).astype(np.float32)

        scale = (
            peak / np.float32(127.0)
        ).astype(np.float32)

        active = scale != 0.0

        if not np.any(active):
            continue

        q = np.zeros_like(values, dtype=np.float32)

        q[active] = lround_away_from_zero(
            values[active] / scale[active, None]
        )

        q = np.clip(
            q,
            np.float32(-127.0),
            np.float32(127.0),
        ).astype(np.int8)

        reconstructed[:, dims] = (
            q.astype(np.float32)
            * scale[:, None]
        )

    return reconstructed


def mean_reconstruction_cosine(
    source,
    reconstructed,
):
    source = np.asarray(source, dtype=np.float32)
    reconstructed = np.asarray(reconstructed, dtype=np.float32)

    dot = np.sum(
        source * reconstructed,
        axis=1,
        dtype=np.float64,
    )

    left = np.sqrt(
        np.sum(
            source * source,
            axis=1,
            dtype=np.float64,
        )
    )

    right = np.sqrt(
        np.sum(
            reconstructed * reconstructed,
            axis=1,
            dtype=np.float64,
        )
    )

    if np.any(left == 0.0) or np.any(right == 0.0):
        raise RuntimeError("zero vector in cosine")

    return float(np.mean(dot / (left * right)))


def budget_cosines(
    source,
    dimension_map,
    ranking,
):
    source = np.asarray(source, dtype=np.float32)

    if source.ndim != 2 or source.shape[1] != DIM:
        raise RuntimeError("score source shape mismatch")

    source_sq = np.sum(
        source * source,
        axis=1,
        dtype=np.float64,
    )

    if np.any(source_sq == 0.0):
        raise RuntimeError("zero source delta")

    dot = np.zeros(source.shape[0], dtype=np.float64)
    recon_sq = np.zeros(source.shape[0], dtype=np.float64)

    wanted = set(BUDGETS)
    result = {}

    for rank in range(1, GROUP_COUNT + 1):
        block = int(ranking[rank - 1])

        dims = dimension_map[
            block * GROUP_SIZE:
            (block + 1) * GROUP_SIZE
        ]

        values = source[:, dims]

        peak = np.max(
            np.abs(values),
            axis=1,
        ).astype(np.float32)

        scale = (
            peak / np.float32(127.0)
        ).astype(np.float32)

        q = np.zeros_like(values, dtype=np.float32)
        active = scale != 0.0

        if np.any(active):
            q[active] = lround_away_from_zero(
                values[active] / scale[active, None]
            )

        q = np.clip(
            q,
            np.float32(-127.0),
            np.float32(127.0),
        ).astype(np.int8)

        reconstructed = (
            q.astype(np.float32)
            * scale[:, None]
        )

        dot += np.sum(
            values * reconstructed,
            axis=1,
            dtype=np.float64,
        )

        recon_sq += np.sum(
            reconstructed * reconstructed,
            axis=1,
            dtype=np.float64,
        )

        if rank in wanted:
            if np.any(recon_sq == 0.0):
                raise RuntimeError(
                    f"zero reconstruction at budget {rank}"
                )

            cosine = dot / np.sqrt(
                source_sq * recon_sq
            )

            result[rank] = float(
                np.mean(cosine)
            )

    if tuple(sorted(result)) != BUDGETS:
        raise RuntimeError("missing budget score")

    return result


def pair_prompt_scores(
    tensor,
    pairs,
    dimension_map,
    ranking,
):
    table = np.empty(
        (len(pairs), len(BUDGETS)),
        dtype=np.float64,
    )

    for pair_index, (a, b) in enumerate(pairs):
        delta = (
            tensor[:, b, :]
            - tensor[:, a, :]
        ).astype(np.float32)

        scores = budget_cosines(
            delta,
            dimension_map,
            ranking,
        )

        for budget_index, budget in enumerate(BUDGETS):
            table[pair_index, budget_index] = scores[budget]

    return table


def deterministic_gap_baseline(
    values,
    pools,
    gap_counts,
):
    total = 0.0

    for gap, count in sorted(gap_counts.items()):
        pool = pools.get(gap)

        if not pool:
            raise RuntimeError(
                f"missing gap pool {gap}"
            )

        total += (
            count
            * float(np.mean(values[pool]))
        )

    return total / 50.0


def selected_mean(
    values,
    selected,
):
    return float(
        np.mean(
            values[
                np.asarray(
                    selected,
                    dtype=np.int64,
                )
            ]
        )
    )


def primary_pair_values(
    pair_budget_table,
):
    if pair_budget_table.ndim != 2:
        raise RuntimeError("pair table rank mismatch")

    if pair_budget_table.shape[1] != len(BUDGETS):
        raise RuntimeError("pair table budget mismatch")

    return np.mean(
        pair_budget_table[:, :len(PRIMARY_BUDGETS)],
        axis=1,
    )


def exact_gap_randomization(
    pair_primary,
    pools,
    gap_counts,
    draw_function,
    draws,
    seed,
    observed_enrichment,
):
    rng = np.random.default_rng(seed)

    null = np.empty(
        draws,
        dtype=np.float64,
    )

    baseline = deterministic_gap_baseline(
        pair_primary,
        pools,
        gap_counts,
    )

    for i in range(draws):
        indices = draw_function(
            rng,
            pools,
            gap_counts,
        )

        score = selected_mean(
            pair_primary,
            indices,
        )

        null[i] = score - baseline

    exceedances = int(
        np.count_nonzero(
            null >= observed_enrichment
        )
    )

    p = (
        1.0 + exceedances
    ) / (
        draws + 1.0
    )

    return {
        "draws": int(draws),
        "seed": int(seed),
        "exceedances": exceedances,
        "empirical_p": float(p),
        "null_mean": float(np.mean(null)),
        "null_sd": float(np.std(null)),
    }


EXPECTED = {
    "bridge_protocol":
        "5435ee0ff16d2d9e1db68898bd05667dac25e56c960a73ab8c9e93a1d3873497",
    "clarification":
        "b417589f41036c367203d154a727ad7b6599c9b257d75574fbe7c8a04a6e8fe8",
    "analysis":
        "42ee9cd91450fc3e9e1cb0c6fed7dede9b78182a0b485b8a259764c6aeb7321c",
    "external_protocol":
        "8a3a492c05220b23a8b4324640563b0439238faef43fb7c97b4de2bba7489ec0",
    "corpus_manifest":
        "e955ab3eef83addf977294fcbecae34c9412c49bf695196bc92694e13b643431",
    "corpus":
        "d51422d9c89da5a469e328297362faa23887e03a9c7dd56e19e00260c7a5835d",
    "forest":
        "da2110ec8a8bac2a0e9533192aca2f601e0b5a311d03983f90ae46e41dc4e902",
}


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def verify_hash(path, expected, label):
    actual = sha256_file(path)

    if actual != expected:
        raise RuntimeError(
            f"{label} SHA mismatch: {actual}"
        )

    return actual


def load_contract():
    verify_hash(
        BRIDGE_PROTOCOL,
        EXPECTED["bridge_protocol"],
        "bridge protocol",
    )
    verify_hash(
        BRIDGE_CLARIFICATION,
        EXPECTED["clarification"],
        "bridge clarification",
    )
    verify_hash(
        BRIDGE_ANALYSIS,
        EXPECTED["analysis"],
        "bridge analysis contract",
    )
    verify_hash(
        EXTERNAL_PROTOCOL,
        EXPECTED["external_protocol"],
        "external protocol",
    )
    verify_hash(
        CORPUS_MANIFEST,
        EXPECTED["corpus_manifest"],
        "corpus manifest",
    )
    verify_hash(
        FOREST_PATH,
        EXPECTED["forest"],
        "Forest artifact",
    )

    bridge = load_json(BRIDGE_PROTOCOL)
    corpus_manifest = load_json(CORPUS_MANIFEST)

    corpus_path = ROOT / corpus_manifest[
        "canonical_corpus"
    ]["path"]

    verify_hash(
        corpus_path,
        EXPECTED["corpus"],
        "canonical corpus",
    )

    if bridge["control"]["draws"] != 10000:
        raise RuntimeError("draw count mismatch")

    if bridge["control"]["seed"] != 48311:
        raise RuntimeError("seed mismatch")

    if tuple(
        bridge["forest_access"]["budgets"]
    ) != BUDGETS:
        raise RuntimeError("budget contract mismatch")

    return bridge, corpus_manifest


def load_analysis_inputs():
    bridge, corpus_manifest = load_contract()

    external = load_module(
        EXTERNAL_ENGINE,
        "openmind_external_replication_bridge",
    )

    external_protocol = load_json(
        EXTERNAL_PROTOCOL
    )

    _, gap_module = external.load_frozen_modules()

    pairs = external.canonical_pairs()

    selected, gap_counts = external.reference_selection(
        external_protocol,
        pairs,
        gap_module,
    )

    pools = external.build_gap_pools(
        pairs
    )

    tensors = external.load_replication_tensors(
        corpus_manifest
    )

    dimension_map, ranking = load_forest(
        FOREST_PATH
    )

    return {
        "bridge": bridge,
        "external": external,
        "pairs": pairs,
        "selected": selected,
        "gap_counts": gap_counts,
        "pools": pools,
        "tensors": tensors,
        "dimension_map": dimension_map,
        "ranking": ranking,
    }




def run_bridge_analysis():
    ctx = load_analysis_inputs()

    bridge = ctx["bridge"]
    external = ctx["external"]
    pairs = ctx["pairs"]
    selected = ctx["selected"]
    gap_counts = ctx["gap_counts"]
    pools = ctx["pools"]
    tensors = ctx["tensors"]
    dimension_map = ctx["dimension_map"]
    ranking = ctx["ranking"]

    prompt_tables = {}

    for prompt_id, tensor in tensors.items():
        prompt_tables[prompt_id] = pair_prompt_scores(
            tensor,
            pairs,
            dimension_map,
            ranking,
        )

    prompt_ids = list(prompt_tables)

    stacked = np.stack(
        [prompt_tables[p] for p in prompt_ids],
        axis=0,
    )

    global_table = np.mean(
        stacked,
        axis=0,
    )

    budget_results = {}

    for budget_index, budget in enumerate(BUDGETS):
        values = global_table[:, budget_index]

        selected_score = selected_mean(
            values,
            selected,
        )

        baseline = deterministic_gap_baseline(
            values,
            pools,
            gap_counts,
        )

        budget_results[str(budget)] = {
            "selected_score": float(selected_score),
            "gap_baseline": float(baseline),
            "enrichment": float(
                selected_score - baseline
            ),
        }

    pair_primary = primary_pair_values(
        global_table
    )

    primary_selected = selected_mean(
        pair_primary,
        selected,
    )

    primary_baseline = deterministic_gap_baseline(
        pair_primary,
        pools,
        gap_counts,
    )

    observed_enrichment = (
        primary_selected
        - primary_baseline
    )

    randomization = exact_gap_randomization(
        pair_primary,
        pools,
        gap_counts,
        external.draw_gap_matched_indices,
        int(bridge["control"]["draws"]),
        int(bridge["control"]["seed"]),
        observed_enrichment,
    )

    prompt_primary = {}

    for prompt_id in prompt_ids:
        values = primary_pair_values(
            prompt_tables[prompt_id]
        )

        selected_score = selected_mean(
            values,
            selected,
        )

        baseline = deterministic_gap_baseline(
            values,
            pools,
            gap_counts,
        )

        prompt_primary[prompt_id] = {
            "selected_score": float(selected_score),
            "gap_baseline": float(baseline),
            "enrichment": float(
                selected_score - baseline
            ),
        }

    positive_prompts = sum(
        row["enrichment"] > 0.0
        for row in prompt_primary.values()
    )

    partial_positive = all(
        budget_results[str(b)]["enrichment"] > 0.0
        for b in PRIMARY_BUDGETS
    )

    primary_pass = (
        observed_enrichment > 0.0
        and randomization["empirical_p"] <= 0.01
    )

    robustness_pass = (
        partial_positive
        and positive_prompts >= 7
    )

    return {
        "schema":
            "openmind.forest.recurrence_bridge.result.v1",
        "status":
            "PRIMARY_PASS"
            if primary_pass
            else "PRIMARY_FAIL",

        "pair_count": len(pairs),
        "selected_pair_count": len(selected),
        "prompt_count": len(prompt_ids),

        "budgets": budget_results,

        "primary": {
            "budgets": list(PRIMARY_BUDGETS),
            "selected_score": float(primary_selected),
            "gap_baseline": float(primary_baseline),
            "enrichment": float(observed_enrichment),
            "pass": bool(primary_pass),
        },

        "randomization": randomization,

        "prompt_primary": prompt_primary,

        "robustness": {
            "all_partial_budgets_positive":
                bool(partial_positive),
            "positive_prompts":
                int(positive_prompts),
            "required_positive_prompts": 7,
            "pass": bool(robustness_pass),
        },

        "full_access_sanity": {
            "budget": 32,
            "selected_score":
                budget_results["32"]["selected_score"],
            "gap_baseline":
                budget_results["32"]["gap_baseline"],
            "enrichment":
                budget_results["32"]["enrichment"],
        },

        "boundaries": [
            "offline shadow analysis only",
            "no model execution",
            "no layer skipping",
            "no inference mutation",
            "no Forest retraining",
        ],
    }


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="OpenMind Forest recurrence bridge V1"
    )

    mode = parser.add_mutually_exclusive_group(
        required=True
    )

    mode.add_argument(
        "--contract-check",
        action="store_true",
        help="Verify frozen inputs without computing bridge statistics.",
    )

    mode.add_argument(
        "--run",
        action="store_true",
        help="Execute the preregistered bridge analysis.",
    )

    parser.add_argument(
        "--output",
        default=str(
            ROOT
            / "results/forest_recurrence_bridge_v1"
            / "forest_recurrence_bridge_v1_result.json"
        ),
    )

    args = parser.parse_args()

    if args.contract_check:
        bridge, corpus_manifest = load_contract()
        dimension_map, ranking = load_forest(
            FOREST_PATH
        )

        print("contract       : PASS")
        print(
            "draws          :",
            bridge["control"]["draws"],
        )
        print(
            "seed           :",
            bridge["control"]["seed"],
        )
        print(
            "corpus prompts :",
            len(corpus_manifest["sources"]),
        )
        print(
            "Forest groups  :",
            len(ranking),
        )
        print(
            "Forest dims    :",
            len(dimension_map),
        )
        return

    result = run_bridge_analysis()

    output = Path(args.output)
    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output.open(
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

    print("result path :", output)
    print("status      :", result["status"])
    print(
        "enrichment  :",
        f'{result["primary"]["enrichment"]:.12f}',
    )
    print(
        "empirical p :",
        f'{result["randomization"]["empirical_p"]:.12f}',
    )
    print(
        "robustness  :",
        "PASS"
        if result["robustness"]["pass"]
        else "FAIL",
    )


if __name__ == "__main__":
    main()
