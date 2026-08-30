#!/usr/bin/env python3

import hashlib
import json
import math
import struct
from pathlib import Path


SOURCE = Path.home() / "qwen2.5-coder-q8_0.gguf"

INVENTORY = Path(
    "experiments/model_fractal/gguf_tensor_inventory_v1.json"
)

PILOT = Path(
    "experiments/model_fractal/maf_pilot_manifest_v1.json"
)

PHASE6F = Path(
    "experiments/model_fractal/maf_q8_0_ffn_roundtrip_v1.json"
)

RESULT = Path(
    "experiments/model_fractal/"
    "maf_q8_0_embedding_stream_roundtrip_v1.json"
)

TARGET = "token_embd.weight"

EXPECTED = {
    "inventory":
        "7acf6d5dc672182aee0244b1bb85a47466f33dbdcdf10bde863e24f3659240ee",
    "pilot":
        "690ec47152646907eed1ca873ff9cf86352777e79b116a6c2d63186e33f859d0",
    "phase6f":
        "25e0b3cee788dbb09d2b5484844f2701e375e1c994d0d8c0a3b5a8f78f305cf2",
}

QK = 32
BLOCK_BYTES = 34
BATCH_BLOCKS = 16384


def sha256_file(path):
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()


def product(values):
    n = 1

    for value in values:
        n *= int(value)

    return n


def main():
    for path in (
        SOURCE,
        INVENTORY,
        PILOT,
        PHASE6F,
    ):
        if not path.exists():
            raise SystemExit(
                f"HOLD: missing artifact: {path}"
            )

    checks = {
        "inventory": sha256_file(INVENTORY),
        "pilot": sha256_file(PILOT),
        "phase6f": sha256_file(PHASE6F),
    }

    for key, actual in checks.items():
        if actual != EXPECTED[key]:
            raise SystemExit(
                f"HOLD: {key} artifact drift\n"
                f"expected: {EXPECTED[key]}\n"
                f"actual:   {actual}"
            )

    inventory = json.loads(
        INVENTORY.read_text()
    )

    pilot = json.loads(
        PILOT.read_text()
    )

    tensors = {
        t["name"]: t
        for t in inventory["tensors"]
    }

    pilots = {
        t["name"]: t
        for t in pilot["pilot"]
    }

    t = tensors[TARGET]
    p = pilots[TARGET]

    if t["type"] != "Q8_0":
        raise SystemExit(
            "HOLD: embedding is not Q8_0"
        )

    dims = [int(x) for x in t["dims"]]
    elements = int(t["elements"])
    span = int(t["span_bytes"])

    if product(dims) != elements:
        raise SystemExit(
            "HOLD: dimension/product mismatch"
        )

    if elements % QK:
        raise SystemExit(
            "HOLD: element count not divisible by 32"
        )

    blocks = elements // QK
    expected_span = blocks * BLOCK_BYTES

    if span != expected_span:
        raise SystemExit(
            "HOLD: Q8_0 span mismatch\n"
            f"expected: {expected_span}\n"
            f"actual:   {span}"
        )

    if span != int(p["span_bytes"]):
        raise SystemExit(
            "HOLD: pilot span mismatch"
        )

    source_hash = hashlib.sha256()
    rebuilt_hash = hashlib.sha256()

    finite_scales = 0
    zero_scales = 0

    scale_min = None
    scale_max = None
    scale_sum = 0.0

    quant_min = 127
    quant_max = -128
    quant_sum = 0

    dequant_min = None
    dequant_max = None
    dequant_sum = 0.0

    quant_count = 0
    processed_blocks = 0

    with SOURCE.open("rb") as f:
        f.seek(int(t["file_start"]))

        while processed_blocks < blocks:
            want_blocks = min(
                BATCH_BLOCKS,
                blocks - processed_blocks,
            )

            chunk = f.read(
                want_blocks * BLOCK_BYTES
            )

            expected_bytes = (
                want_blocks * BLOCK_BYTES
            )

            if len(chunk) != expected_bytes:
                raise SystemExit(
                    "HOLD: truncated source chunk"
                )

            source_hash.update(chunk)

            for offset in range(
                0,
                len(chunk),
                BLOCK_BYTES,
            ):
                block = chunk[
                    offset:offset + BLOCK_BYTES
                ]

                scale_raw = block[:2]
                quant_raw = block[2:]

                scale = struct.unpack(
                    "<e",
                    scale_raw,
                )[0]

                if not math.isfinite(scale):
                    raise SystemExit(
                        "HOLD: non-finite scale"
                    )

                quants = struct.unpack(
                    "<32b",
                    quant_raw,
                )

                rebuilt = (
                    struct.pack("<e", scale)
                    + struct.pack("<32b", *quants)
                )

                rebuilt_hash.update(rebuilt)

                finite_scales += 1

                if scale == 0.0:
                    zero_scales += 1

                if (
                    scale_min is None
                    or scale < scale_min
                ):
                    scale_min = scale

                if (
                    scale_max is None
                    or scale > scale_max
                ):
                    scale_max = scale

                scale_sum += scale

                for q in quants:
                    quant_count += 1
                    quant_sum += q

                    if q < quant_min:
                        quant_min = q

                    if q > quant_max:
                        quant_max = q

                    value = scale * q

                    if not math.isfinite(value):
                        raise SystemExit(
                            "HOLD: non-finite dequant value"
                        )

                    if (
                        dequant_min is None
                        or value < dequant_min
                    ):
                        dequant_min = value

                    if (
                        dequant_max is None
                        or value > dequant_max
                    ):
                        dequant_max = value

                    dequant_sum += value

            processed_blocks += want_blocks

    source_digest = source_hash.hexdigest()
    rebuilt_digest = rebuilt_hash.hexdigest()

    if processed_blocks != blocks:
        raise SystemExit(
            "HOLD: block count mismatch"
        )

    if quant_count != elements:
        raise SystemExit(
            "HOLD: element count mismatch"
        )

    byte_hash_equal = (
        source_digest
        == rebuilt_digest
        == t["payload_sha256"]
        == p["payload_sha256"]
    )

    passed = (
        byte_hash_equal
        and finite_scales == blocks
        and quant_count == elements
    )

    if not passed:
        raise SystemExit(
            "HOLD: embedding round-trip failed"
        )

    output = {
        "schema":
            "openmind.maf_q8_0_embedding_stream_roundtrip.v1",
        "target":
            TARGET,
        "dims":
            dims,
        "elements":
            elements,
        "block_count":
            blocks,
        "block_bytes":
            BLOCK_BYTES,
        "span_bytes":
            span,
        "streaming":
            True,
        "batch_blocks":
            BATCH_BLOCKS,
        "finite_scale_count":
            finite_scales,
        "zero_scale_count":
            zero_scales,
        "scale_min":
            scale_min,
        "scale_max":
            scale_max,
        "scale_mean":
            scale_sum / blocks,
        "quant_min":
            quant_min,
        "quant_max":
            quant_max,
        "quant_mean":
            quant_sum / quant_count,
        "dequant_min":
            dequant_min,
        "dequant_max":
            dequant_max,
        "dequant_mean":
            dequant_sum / quant_count,
        "source_sha256":
            source_digest,
        "reencoded_sha256":
            rebuilt_digest,
        "hash_equal":
            byte_hash_equal,
        "all_pass":
            passed,
    }

    RESULT.write_text(
        json.dumps(
            output,
            indent=2,
        ) + "\n"
    )

    print("=" * 72)
    print(
        " OPENMIND / PHASE 6G — "
        "STREAMING Q8_0 EMBEDDING ROUND TRIP"
    )
    print("=" * 72)
    print("target       :", TARGET)
    print("dims         :", dims)
    print("elements     :", f"{elements:,}")
    print("blocks       :", f"{blocks:,}")
    print("span bytes   :", f"{span:,}")
    print("streaming    : YES")
    print("finite scales:", f"{finite_scales:,}")
    print("zero scales  :", f"{zero_scales:,}")
    print("quant range  :", quant_min, "to", quant_max)
    print(
        "dequant range:",
        dequant_min,
        "to",
        dequant_max,
    )
    print()
    print("source hash  :", source_digest)
    print("rebuilt hash :", rebuilt_digest)
    print("hash equal   :", byte_hash_equal)
    print("all pass     :", passed)
    print()
    print("PHASE 6G PASS")


if __name__ == "__main__":
    main()
