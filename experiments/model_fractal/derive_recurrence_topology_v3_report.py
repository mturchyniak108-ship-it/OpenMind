#!/usr/bin/env python3

import contextlib
import hashlib
import importlib.util
import io
import json
import math
import re
import statistics
import sys
import time
from collections import defaultdict
from pathlib import Path


(
    source_path,
    original_path,
    frozen_manifest_path,
    frozen_result_path,
    checkpoint_path,
    report_path,
    report_manifest_path,
) = map(
    Path,
    sys.argv[1:],
)


def sha256(path):
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()


# ------------------------------------------------------------
# VERIFY FROZEN EVIDENCE
# ------------------------------------------------------------

with frozen_manifest_path.open() as f:
    frozen_manifest = json.load(f)

if (
    frozen_manifest.get("status")
    != "VALIDATED_PASS"
):
    raise SystemExit(
        "frozen manifest is not VALIDATED_PASS"
    )

required = [
    source_path,
    original_path,
    frozen_result_path,
    checkpoint_path,
]

for path in required:

    if not path.exists():
        raise SystemExit(
            f"missing frozen artifact: {path}"
        )

    expected = (
        frozen_manifest
        .get("sha256", {})
        .get(str(path))
    )

    if expected is None:
        raise SystemExit(
            f"manifest has no hash for {path}"
        )

    actual = sha256(path)

    if actual != expected:
        raise SystemExit(
            f"frozen hash mismatch: {path}"
        )


# ------------------------------------------------------------
# LOAD FROZEN CHECKPOINT
# ------------------------------------------------------------

with checkpoint_path.open() as f:
    checkpoint = json.load(f)

completed = checkpoint[
    "completed_permutations"
]

raw_nulls = checkpoint[
    "null_deltas"
]

if completed != 1000:
    raise SystemExit(
        "checkpoint is not 1000 permutations"
    )

if len(raw_nulls) != 378:
    raise SystemExit(
        "checkpoint does not contain 378 pairs"
    )

null_lengths = {
    len(values)
    for values
    in raw_nulls.values()
}

if null_lengths != {1000}:
    raise SystemExit(
        "checkpoint null distributions incomplete"
    )


# ------------------------------------------------------------
# LOAD VALIDATED V3-FIXED IMPLEMENTATION
# ------------------------------------------------------------

spec = importlib.util.spec_from_file_location(
    "openmind_v3_fixed",
    source_path,
)

if spec is None or spec.loader is None:
    raise SystemExit(
        "unable to load V3-fixed source"
    )

mod = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    mod
)


data, layers, tokens = mod.load_data(
    mod.DEFAULT_PATH
)

if len(layers) != 28:
    raise SystemExit(
        "layer count mismatch"
    )

if len(tokens) != 13:
    raise SystemExit(
        "token count mismatch"
    )

if len(data) != 364:
    raise SystemExit(
        "vector count mismatch"
    )

dimension = len(
    next(iter(data.values()))
)

if dimension != 1536:
    raise SystemExit(
        "dimension mismatch"
    )


layer_pairs = [
    (a, b)
    for i, a in enumerate(layers)
    for b in layers[i + 1:]
]

if len(layer_pairs) != 378:
    raise SystemExit(
        "derived layer-pair count mismatch"
    )


# ------------------------------------------------------------
# REBUILD ONLY COSINE CACHE
#
# NO PERMUTATIONS ARE RUN HERE.
# ------------------------------------------------------------

cache_started = time.monotonic()

with contextlib.redirect_stdout(
    io.StringIO()
):
    cache = mod.build_cosine_cache(
        data,
        layers,
        tokens,
    )

cache_seconds = (
    time.monotonic()
    - cache_started
)


# ------------------------------------------------------------
# OBSERVED IDENTITY STATISTIC
# ------------------------------------------------------------

identity = list(
    range(len(tokens))
)

observed = {}

for pair in layer_pairs:

    observed[pair] = (
        mod.pair_stat_cached(
            cache[pair],
            identity,
            len(tokens),
        )
    )


# ------------------------------------------------------------
# RECONSTRUCT FROZEN EMPIRICAL STATISTICS
# ------------------------------------------------------------

records = []

for a, b in layer_pairs:

    same, cross, delta = (
        observed[(a, b)]
    )

    key = f"{a},{b}"

    if key not in raw_nulls:
        raise SystemExit(
            f"checkpoint missing pair {key}"
        )

    null = raw_nulls[key]

    null_mean = statistics.mean(
        null
    )

    null_sd = statistics.stdev(
        null
    )

    if null_sd == 0:
        z = 0.0
    else:
        z = (
            delta
            - null_mean
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


# ------------------------------------------------------------
# VERIFY TOP-50 AGAINST FROZEN RESULT
# ------------------------------------------------------------

frozen_text = (
    frozen_result_path.read_text()
)

pattern = re.compile(
    r"^\s*(\d+)\s+"
    r"([+-][0-9.]+)\s+"
    r"([0-9.]+)\s+"
    r"([+-][0-9.]+)\s+"
    r"(\d+)\s+"
    r"(L\d+<->L\d+)\s*$",
    re.MULTILINE,
)

frozen_top = []

for match in pattern.finditer(
    frozen_text
):
    frozen_top.append(
        (
            int(match.group(1)),
            match.group(2),
            match.group(3),
            match.group(4),
            int(match.group(5)),
            match.group(6),
        )
    )

if len(frozen_top) < 50:
    raise SystemExit(
        "unable to parse frozen top-50"
    )

frozen_top = frozen_top[:50]

derived_top = []

for rank, row in enumerate(
    records[:50],
    1,
):
    (
        z,
        p,
        delta,
        same,
        cross,
        null,
        gap,
        a,
        b,
    ) = row

    derived_top.append(
        (
            rank,
            f"{z:+.3f}",
            f"{p:.6f}",
            f"{delta:+.6f}",
            gap,
            f"L{a:02d}<->L{b:02d}",
        )
    )

if derived_top != frozen_top:

    for expected, actual in zip(
        frozen_top,
        derived_top,
    ):
        if expected != actual:
            print(
                "first top-50 mismatch:"
            )

            print(
                f"frozen : {expected}"
            )

            print(
                f"derived: {actual}"
            )

            break

    raise SystemExit(
        "top-50 parity failure"
    )


# ------------------------------------------------------------
# GAP SUMMARY
# ------------------------------------------------------------

by_gap = defaultdict(list)

for row in records:

    (
        z,
        p,
        delta,
        same,
        cross,
        null,
        gap,
        a,
        b,
    ) = row

    by_gap[gap].append(
        (
            delta,
            null,
            z,
        )
    )


# ------------------------------------------------------------
# GLOBAL STATISTICS
# ------------------------------------------------------------

zs = [
    row[0]
    for row in records
]

ps = [
    row[1]
    for row in records
]

deltas = [
    row[2]
    for row in records
]

nulls = [
    row[5]
    for row in records
]


# ------------------------------------------------------------
# LOCAL TOKEN CONTROL
#
# Uses the validated cosine cache.
# No permutation work occurs here.
# ------------------------------------------------------------

token_to_index = {
    token: i
    for i, token
    in enumerate(tokens)
}

local_rows = []

for gap in sorted(by_gap):

    same_values = []
    plus1_values = []
    plus2_values = []

    for a in layers:

        b = a + gap

        if b not in layers:
            continue

        pair = (a, b)

        if pair not in cache:
            continue

        matrix = cache[pair]

        for token in tokens:

            i = token_to_index[token]

            same_values.append(
                matrix[i][i]
            )

            for offset, target in (
                (1, plus1_values),
                (2, plus2_values),
            ):

                other = token + offset

                if other in token_to_index:

                    target.append(
                        matrix[
                            i
                        ][
                            token_to_index[
                                other
                            ]
                        ]
                    )

                other = token - offset

                if other in token_to_index:

                    target.append(
                        matrix[
                            i
                        ][
                            token_to_index[
                                other
                            ]
                        ]
                    )

    if (
        plus1_values
        and plus2_values
    ):
        sm = statistics.mean(
            same_values
        )

        p1 = statistics.mean(
            plus1_values
        )

        p2 = statistics.mean(
            plus2_values
        )

        local_rows.append(
            (
                gap,
                sm,
                p1,
                p2,
                sm - p1,
                sm - p2,
            )
        )


# ------------------------------------------------------------
# WRITE FULL REPORT
# ------------------------------------------------------------

lines = []

lines.append(
    "=" * 100
)

lines.append(
    " OPENMIND / RECURRENCE TOPOLOGY V3-FIXED"
)

lines.append(
    " DERIVED FULL REPORT FROM FROZEN 1000-PERMUTATION CHECKPOINT"
)

lines.append(
    "=" * 100
)

lines.append("")

lines.append(
    f"Dataset     : {mod.DEFAULT_PATH}"
)

lines.append(
    f"Layers      : {len(layers)}"
)

lines.append(
    f"Tokens      : {len(tokens)}"
)

lines.append(
    f"Vectors     : {len(data)}"
)

lines.append(
    f"Dimensions  : {dimension}"
)

lines.append(
    f"Excluded    : {sorted(mod.EXCLUDED_TOKENS)}"
)

lines.append(
    f"Seed        : {mod.SEED}"
)

lines.append(
    f"Permutations: {completed}"
)

lines.append(
    "Permutation rerun: NO"
)

lines.append(
    "Frozen checkpoint: VERIFIED"
)

lines.append(
    f"Cosine cache seconds: {cache_seconds:.3f}"
)


# TOP PAIRS

lines.append("")
lines.append(
    "TOP LAYER PAIRS BY EMPIRICAL Z"
)

lines.append(
    "-" * 100
)

lines.append(
    "rank   z        p-value    delta      same       cross      "
    "null      gap   pair"
)

lines.append(
    "-" * 100
)

for rank, row in enumerate(
    records[:50],
    1,
):

    (
        z,
        p,
        delta,
        same,
        cross,
        null,
        gap,
        a,
        b,
    ) = row

    lines.append(
        f"{rank:4d} "
        f"{z:+8.3f} "
        f"{p:9.6f} "
        f"{delta:+10.6f} "
        f"{same:.6f} "
        f"{cross:.6f} "
        f"{null:+.6f} "
        f"{gap:4d} "
        f"L{a:02d}<->L{b:02d}"
    )


# GAP SUMMARY

lines.append("")
lines.append(
    "=" * 100
)

lines.append(
    " GAP SUMMARY"
)

lines.append(
    "=" * 100
)

lines.append("")

lines.append(
    "gap   mean_delta   mean_null   mean_z    "
    "min_delta   max_delta"
)

lines.append(
    "-" * 100
)

for gap in sorted(by_gap):

    values = by_gap[gap]

    gap_deltas = [
        x[0]
        for x in values
    ]

    gap_nulls = [
        x[1]
        for x in values
    ]

    gap_zs = [
        x[2]
        for x in values
    ]

    lines.append(
        f"{gap:3d} "
        f"{statistics.mean(gap_deltas):+11.6f} "
        f"{statistics.mean(gap_nulls):+11.6f} "
        f"{statistics.mean(gap_zs):+9.4f} "
        f"{min(gap_deltas):+11.6f} "
        f"{max(gap_deltas):+11.6f}"
    )


# GLOBAL

lines.append("")
lines.append(
    "=" * 100
)

lines.append(
    " GLOBAL T00-EXCLUDED TOPOLOGY STATISTICS"
)

lines.append(
    "=" * 100
)

lines.append("")

lines.append(
    f"Layer pairs       : {len(records)}"
)

lines.append(
    f"Mean observed Δ   : "
    f"{statistics.mean(deltas):+.6f}"
)

lines.append(
    f"Mean null Δ       : "
    f"{statistics.mean(nulls):+.6f}"
)

lines.append(
    f"Mean empirical z  : "
    f"{statistics.mean(zs):+.6f}"
)

lines.append(
    f"Max empirical z   : "
    f"{max(zs):+.6f}"
)

lines.append(
    f"Pairs z > 2       : "
    f"{sum(z > 2 for z in zs)} / {len(zs)}"
)

lines.append(
    f"Pairs z > 3       : "
    f"{sum(z > 3 for z in zs)} / {len(zs)}"
)

lines.append(
    f"Pairs p < .05     : "
    f"{sum(p < .05 for p in ps)} / {len(ps)}"
)

lines.append(
    f"Pairs p < .01     : "
    f"{sum(p < .01 for p in ps)} / {len(ps)}"
)


# LOCAL CONTROL

lines.append("")
lines.append(
    "=" * 100
)

lines.append(
    " LOCAL TOKEN CONTROL"
)

lines.append(
    "=" * 100
)

lines.append("")

lines.append(
    "For each layer pair, compare the same-token relationship "
    "against token offsets ±1 and ±2."
)

lines.append("")

lines.append(
    "gap   same_mean   ±1_mean   ±2_mean   "
    "same-±1   same-±2"
)

lines.append(
    "-" * 100
)

for (
    gap,
    sm,
    p1,
    p2,
    d1,
    d2,
) in local_rows:

    lines.append(
        f"{gap:3d} "
        f"{sm:+10.6f} "
        f"{p1:+9.6f} "
        f"{p2:+9.6f} "
        f"{d1:+9.6f} "
        f"{d2:+9.6f}"
    )


lines.append("")
lines.append(
    "=" * 100
)

lines.append(
    " DERIVED REPORT COMPLETE"
)

lines.append(
    "=" * 100
)

lines.append(
    "Frozen top-50 parity : PASS"
)

lines.append(
    "Checkpoint integrity : PASS"
)

lines.append(
    "Permutation rerun    : NO"
)

lines.append(
    "Reporting parity     : COMPLETE"
)

report_path.write_text(
    "\n".join(lines)
    + "\n"
)


# ------------------------------------------------------------
# WRITE DERIVED MANIFEST
# ------------------------------------------------------------

payload = {
    "schema":
        "openmind.recurrence_topology_v3_full_report.v1",

    "status":
        "DERIVED_PARITY_PASS",

    "source":
        "frozen V3-fixed 1000-permutation checkpoint",

    "permutations_rerun":
        False,

    "checkpoint": {
        "completed_permutations":
            completed,

        "layer_pairs":
            len(raw_nulls),

        "null_length":
            1000,
    },

    "reporting": {
        "top_50":
            "PASS",

        "gap_summary":
            "COMPLETE",

        "global_statistics":
            "COMPLETE",

        "local_token_control":
            "COMPLETE",
    },

    "parity": {
        "top_50_matches_frozen_result":
            True,

        "top_50_rows_checked":
            50,
    },

    "dataset": {
        "layers":
            len(layers),

        "tokens":
            len(tokens),

        "vectors":
            len(data),

        "dimensions":
            dimension,

        "excluded_tokens":
            sorted(
                mod.EXCLUDED_TOKENS
            ),
    },

    "cache_build_seconds":
        cache_seconds,

    "sha256": {
        "frozen_manifest":
            sha256(
                frozen_manifest_path
            ),

        "frozen_result":
            sha256(
                frozen_result_path
            ),

        "checkpoint":
            sha256(
                checkpoint_path
            ),

        "fixed_source":
            sha256(
                source_path
            ),

        "original_v3":
            sha256(
                original_path
            ),

        "derived_report":
            sha256(
                report_path
            ),
    },
}

report_manifest_path.write_text(
    json.dumps(
        payload,
        indent=2,
        sort_keys=True,
    )
    + "\n"
)


print(
    "frozen evidence       : VERIFIED"
)

print(
    "permutations rerun    : NO"
)

print(
    "top-50 parity         : PASS"
)

print(
    f"gap rows              : "
    f"{len(by_gap)}"
)

print(
    f"local-control rows    : "
    f"{len(local_rows)}"
)

print(
    f"mean observed delta   : "
    f"{statistics.mean(deltas):+.6f}"
)

print(
    f"mean null delta       : "
    f"{statistics.mean(nulls):+.6f}"
)

print(
    f"mean empirical z      : "
    f"{statistics.mean(zs):+.6f}"
)

print(
    f"max empirical z       : "
    f"{max(zs):+.6f}"
)

print(
    f"pairs z > 3           : "
    f"{sum(z > 3 for z in zs)}/{len(zs)}"
)

print(
    f"pairs p < .01         : "
    f"{sum(p < .01 for p in ps)}/{len(ps)}"
)

print(
    "reporting parity      : COMPLETE"
)

print(
    "derived status        : DERIVED_PARITY_PASS"
)
