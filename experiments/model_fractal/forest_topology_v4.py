#!/usr/bin/env python3

import csv
import math
import random
import statistics
from pathlib import Path

import numpy as np


PATH = Path("activation_vectors_all_tokens.csv")

SEED = 1337
FOLDS = 4
GROUP_SIZE = 64
EXCLUDED_TOKENS = {0}

REQUEST_FRACTIONS = (
    0.125,
    0.250,
    0.500,
    0.750,
)


def cosine(a, b):
    dot = float(np.dot(a, b))
    na = float(np.linalg.norm(a))
    nb = float(np.linalg.norm(b))

    if na == 0.0 or nb == 0.0:
        return 0.0

    return dot / (na * nb)


def relative_l2(a, b):
    denom = float(np.linalg.norm(a))

    if denom == 0.0:
        return 0.0

    return float(np.linalg.norm(a - b)) / denom


def load_vectors():
    rows = []

    with PATH.open(newline="") as f:
        reader = csv.DictReader(f)

        for r in reader:
            token = int(r["token_index"])

            if token in EXCLUDED_TOKENS:
                continue

            layer = int(r["layer"])
            dim = int(r["embedding_dimension"])

            vec = np.asarray(
                [
                    float(r[f"v{i}"])
                    for i in range(dim)
                ],
                dtype=np.float64,
            )

            rows.append(
                {
                    "token": token,
                    "layer": layer,
                    "vec": vec,
                }
            )

    return rows


def build_residuals(rows):
    """
    V4 isolates grouping generalization.

    Remove a global centroid so correlation grouping operates on
    representation displacement rather than absolute vector offset.
    """

    matrix = np.stack(
        [r["vec"] for r in rows],
        axis=0,
    )

    centroid = matrix.mean(axis=0)

    out = []

    for r in rows:
        out.append(
            {
                "token": r["token"],
                "layer": r["layer"],
                "residual": r["vec"] - centroid,
            }
        )

    return out


def contiguous_groups(dim):
    return [
        np.arange(
            start,
            min(start + GROUP_SIZE, dim),
            dtype=np.int32,
        )
        for start in range(0, dim, GROUP_SIZE)
    ]


def random_groups(dim, seed):
    ids = list(range(dim))

    rng = random.Random(seed)
    rng.shuffle(ids)

    return [
        np.asarray(
            ids[start:start + GROUP_SIZE],
            dtype=np.int32,
        )
        for start in range(0, dim, GROUP_SIZE)
    ]


def correlated_groups(train_matrix):
    """
    Greedy non-overlapping grouping.

    Each group starts from an unused dimension with the highest
    remaining mean absolute correlation and then takes the unused
    dimensions most correlated with that seed.
    """

    corr = np.corrcoef(
        train_matrix,
        rowvar=False,
    )

    corr = np.nan_to_num(
        corr,
        nan=0.0,
        posinf=0.0,
        neginf=0.0,
    )

    abs_corr = np.abs(corr)
    np.fill_diagonal(abs_corr, 0.0)

    dim = train_matrix.shape[1]

    unused = set(range(dim))
    groups = []

    mean_corr = abs_corr.mean(axis=1)

    while unused:
        seed = max(
            unused,
            key=lambda i: (
                mean_corr[i],
                -i,
            ),
        )

        candidates = sorted(
            (
                i
                for i in unused
                if i != seed
            ),
            key=lambda i: (
                -abs_corr[seed, i],
                i,
            ),
        )

        members = [seed]

        members.extend(
            candidates[:GROUP_SIZE - 1]
        )

        for i in members:
            unused.remove(i)

        groups.append(
            np.asarray(
                members,
                dtype=np.int32,
            )
        )

    return groups


def mean_within_abs_corr(matrix, groups):
    corr = np.corrcoef(
        matrix,
        rowvar=False,
    )

    corr = np.nan_to_num(
        corr,
        nan=0.0,
        posinf=0.0,
        neginf=0.0,
    )

    vals = []

    for group in groups:
        if len(group) < 2:
            continue

        sub = np.abs(
            corr[np.ix_(group, group)]
        )

        tri = sub[
            np.triu_indices(
                len(group),
                k=1,
            )
        ]

        vals.extend(tri.tolist())

    if not vals:
        return 0.0

    return statistics.mean(vals)


def oracle_partial(vec, groups, fraction):
    energies = []

    total_energy = float(
        np.dot(vec, vec)
    )

    for index, group in enumerate(groups):
        part = vec[group]

        energy = float(
            np.dot(part, part)
        )

        energies.append(
            (energy, index)
        )

    energies.sort(
        key=lambda x: (
            -x[0],
            x[1],
        )
    )

    k = max(
        1,
        math.ceil(
            len(groups) * fraction
        ),
    )

    selected = energies[:k]

    reconstructed = np.zeros_like(vec)

    selected_energy = 0.0

    for energy, index in selected:
        group = groups[index]

        reconstructed[group] = vec[group]

        selected_energy += energy

    if total_energy == 0.0:
        energy_fraction = 1.0
    else:
        energy_fraction = (
            selected_energy /
            total_energy
        )

    return {
        "energy": energy_fraction,
        "cosine": cosine(
            vec,
            reconstructed,
        ),
        "rel_l2": relative_l2(
            vec,
            reconstructed,
        ),
    }


def evaluate(matrix, groups, fraction):
    values = [
        oracle_partial(
            vec,
            groups,
            fraction,
        )
        for vec in matrix
    ]

    return {
        "energy": statistics.mean(
            x["energy"]
            for x in values
        ),
        "cosine": statistics.mean(
            x["cosine"]
            for x in values
        ),
        "min_cosine": min(
            x["cosine"]
            for x in values
        ),
        "rel_l2": statistics.mean(
            x["rel_l2"]
            for x in values
        ),
        "max_rel_l2": max(
            x["rel_l2"]
            for x in values
        ),
    }


def token_folds(tokens):
    tokens = sorted(tokens)

    rng = random.Random(SEED)
    rng.shuffle(tokens)

    folds = [
        []
        for _ in range(FOLDS)
    ]

    for i, token in enumerate(tokens):
        folds[i % FOLDS].append(token)

    return folds


def main():
    rows = load_vectors()

    if not rows:
        raise RuntimeError(
            "no vectors loaded"
        )

    dimensions = len(rows[0]["vec"])

    if dimensions % GROUP_SIZE != 0:
        raise RuntimeError(
            "dimensions must divide evenly "
            "by group size"
        )

    residual_rows = build_residuals(rows)

    tokens = sorted(
        {
            r["token"]
            for r in residual_rows
        }
    )

    folds = token_folds(tokens)

    pine_groups = contiguous_groups(
        dimensions
    )

    random_control = random_groups(
        dimensions,
        SEED,
    )

    print("=" * 124)
    print(
        " OPENMIND / FOREST TOPOLOGY V4 "
        "— TOKEN-HELD-OUT ORANGE GENERALIZATION"
    )
    print("=" * 124)

    print()
    print("DATASET")
    print("-" * 124)

    print(
        f"vectors                     : "
        f"{len(residual_rows)}"
    )
    print(
        f"tokens                      : "
        f"{len(tokens)}"
    )
    print(
        f"dimensions                  : "
        f"{dimensions}"
    )
    print(
        f"group size                  : "
        f"{GROUP_SIZE}"
    )
    print(
        f"groups                      : "
        f"{len(pine_groups)}"
    )
    print(
        f"folds                       : "
        f"{FOLDS}"
    )
    print(
        f"excluded tokens             : "
        f"{sorted(EXCLUDED_TOKENS)}"
    )

    print()
    print("GENERALIZATION CONTRACT")
    print("-" * 124)

    print(
        "Train/test partition is by complete token ID."
    )
    print(
        "Orange correlation groups are learned only "
        "from training-token residuals."
    )
    print(
        "The Orange map is frozen before held-out "
        "token evaluation."
    )
    print(
        "Pine and deterministic Random controls are "
        "fixed globally."
    )
    print(
        "Oracle top-energy group selection is retained "
        "to isolate grouping generalization."
    )

    pooled = {
        fraction: {
            "pine_energy": [],
            "random_energy": [],
            "orange_energy": [],
            "pine_l2": [],
            "random_l2": [],
            "orange_l2": [],
        }
        for fraction in REQUEST_FRACTIONS
    }

    fold_wins = {
        fraction: {
            "pine": 0,
            "random": 0,
        }
        for fraction in REQUEST_FRACTIONS
    }

    print()
    print("FOLD RESULTS")
    print("-" * 124)

    for fold_index, test_tokens in enumerate(
        folds,
        start=1,
    ):
        test_set = set(test_tokens)

        train = [
            r["residual"]
            for r in residual_rows
            if r["token"] not in test_set
        ]

        test = [
            r["residual"]
            for r in residual_rows
            if r["token"] in test_set
        ]

        train_matrix = np.stack(
            train,
            axis=0,
        )

        test_matrix = np.stack(
            test,
            axis=0,
        )

        orange_groups = correlated_groups(
            train_matrix
        )

        pine_corr = mean_within_abs_corr(
            test_matrix,
            pine_groups,
        )

        random_corr = mean_within_abs_corr(
            test_matrix,
            random_control,
        )

        orange_corr = mean_within_abs_corr(
            test_matrix,
            orange_groups,
        )

        print()
        print(
            f"FOLD {fold_index}"
        )

        print(
            f"  train vectors             : "
            f"{len(train)}"
        )
        print(
            f"  test vectors              : "
            f"{len(test)}"
        )
        print(
            f"  held-out tokens           : "
            f"{','.join(map(str, sorted(test_tokens)))}"
        )

        print(
            f"  heldout Pine correlation  : "
            f"{pine_corr:.9f}"
        )
        print(
            f"  heldout Random correlation: "
            f"{random_corr:.9f}"
        )
        print(
            f"  heldout Orange correlation: "
            f"{orange_corr:.9f}"
        )

        print(
            "  request  "
            "pine_energy random_energy orange_energy "
            "orange/pine orange/random "
            "orange_l2/pine orange_l2/random"
        )

        for fraction in REQUEST_FRACTIONS:
            pine = evaluate(
                test_matrix,
                pine_groups,
                fraction,
            )

            random_result = evaluate(
                test_matrix,
                random_control,
                fraction,
            )

            orange = evaluate(
                test_matrix,
                orange_groups,
                fraction,
            )

            orange_pine = (
                orange["energy"] /
                pine["energy"]
            )

            orange_random = (
                orange["energy"] /
                random_result["energy"]
            )

            l2_pine = (
                orange["rel_l2"] /
                pine["rel_l2"]
            )

            l2_random = (
                orange["rel_l2"] /
                random_result["rel_l2"]
            )

            if (
                orange["energy"] >
                pine["energy"]
                and
                orange["rel_l2"] <
                pine["rel_l2"]
            ):
                fold_wins[fraction]["pine"] += 1

            if (
                orange["energy"] >
                random_result["energy"]
                and
                orange["rel_l2"] <
                random_result["rel_l2"]
            ):
                fold_wins[fraction]["random"] += 1

            p = pooled[fraction]

            p["pine_energy"].append(
                pine["energy"]
            )
            p["random_energy"].append(
                random_result["energy"]
            )
            p["orange_energy"].append(
                orange["energy"]
            )

            p["pine_l2"].append(
                pine["rel_l2"]
            )
            p["random_l2"].append(
                random_result["rel_l2"]
            )
            p["orange_l2"].append(
                orange["rel_l2"]
            )

            print(
                f"  {fraction:7.3f} "
                f"{pine['energy']:11.9f} "
                f"{random_result['energy']:13.9f} "
                f"{orange['energy']:13.9f} "
                f"{orange_pine:11.9f} "
                f"{orange_random:13.9f} "
                f"{l2_pine:14.9f} "
                f"{l2_random:16.9f}"
            )

    print()
    print("CROSS-FOLD SUMMARY")
    print("-" * 124)

    print(
        "request  orange/pine_energy "
        "orange/random_energy "
        "orange_l2/pine orange_l2/random "
        "pine_wins random_wins"
    )

    all_pass = True

    for fraction in REQUEST_FRACTIONS:
        p = pooled[fraction]

        pine_energy = statistics.mean(
            p["pine_energy"]
        )

        random_energy = statistics.mean(
            p["random_energy"]
        )

        orange_energy = statistics.mean(
            p["orange_energy"]
        )

        pine_l2 = statistics.mean(
            p["pine_l2"]
        )

        random_l2 = statistics.mean(
            p["random_l2"]
        )

        orange_l2 = statistics.mean(
            p["orange_l2"]
        )

        energy_pine_ratio = (
            orange_energy /
            pine_energy
        )

        energy_random_ratio = (
            orange_energy /
            random_energy
        )

        l2_pine_ratio = (
            orange_l2 /
            pine_l2
        )

        l2_random_ratio = (
            orange_l2 /
            random_l2
        )

        pine_wins = (
            fold_wins[fraction]["pine"]
        )

        random_wins = (
            fold_wins[fraction]["random"]
        )

        passed = (
            energy_pine_ratio > 1.0
            and
            energy_random_ratio > 1.0
            and
            l2_pine_ratio < 1.0
            and
            l2_random_ratio < 1.0
            and
            pine_wins >= 3
            and
            random_wins >= 3
        )

        if not passed:
            all_pass = False

        print(
            f"{fraction:7.3f} "
            f"{energy_pine_ratio:18.9f} "
            f"{energy_random_ratio:20.9f} "
            f"{l2_pine_ratio:14.9f} "
            f"{l2_random_ratio:16.9f} "
            f"{pine_wins:9d}/4 "
            f"{random_wins:11d}/4"
        )

    print()
    print("FOREST V4 DECISION")
    print("-" * 124)

    if all_pass:
        decision = (
            "HELD-OUT ORANGE GENERALIZATION PASSES"
        )
    else:
        decision = (
            "HELD-OUT ORANGE GENERALIZATION "
            "NOT ESTABLISHED"
        )

    print(
        f"result                     : "
        f"{decision}"
    )

    print()
    print("INTERPRETATION BOUNDARY")
    print("-" * 124)

    print(
        "V4 holds out complete token IDs so the "
        "Orange correlation map cannot learn from "
        "the evaluated token trajectories."
    )
    print(
        "This experiment isolates grouping "
        "generalization; it does not yet test a "
        "fully retrained/frozen Lodgepole tree."
    )
    print(
        "Oracle top-energy selection remains in use, "
        "so successful V4 results do not establish "
        "deployable routing."
    )
    print(
        "If V4 passes, the next gate should remove "
        "the oracle before quantization."
    )


if __name__ == "__main__":
    main()
