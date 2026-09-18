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

PHASE6D = Path(
    "experiments/model_fractal/"
    "maf_f32_numeric_roundtrip_v1.json"
)

RESULT = Path(
    "experiments/model_fractal/"
    "maf_q8_0_numeric_roundtrip_v1.json"
)

TARGET = "blk.0.attn_q.weight"

EXPECTED = {
    "inventory":
        "7acf6d5dc672182aee0244b1bb85a47466f33dbdcdf10bde863e24f3659240ee",
    "pilot":
        "690ec47152646907eed1ca873ff9cf86352777e79b116a6c2d63186e33f859d0",
    "phase6d":
        "9dcc4f074b5efd60a64b8a336563829988203284ec7760eebb393ed568151012",
}

QK8_0 = 32
SCALE_BYTES = 2
QUANT_BYTES = 32
BLOCK_BYTES = SCALE_BYTES + QUANT_BYTES


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


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
    result = 1

    for value in values:
        result *= int(value)

    return result


def main():
    for path in (
        SOURCE,
        INVENTORY,
        PILOT,
        PHASE6D,
    ):
        if not path.exists():
            raise SystemExit(
                f"HOLD: missing artifact: {path}"
            )

    artifact_hashes = {
        "inventory": sha256_file(INVENTORY),
        "pilot": sha256_file(PILOT),
        "phase6d": sha256_file(PHASE6D),
    }

    for name, actual in artifact_hashes.items():
        expected = EXPECTED[name]

        if actual != expected:
            raise SystemExit(
                f"HOLD: {name} artifact drift\n"
                f"expected: {expected}\n"
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

    if TARGET not in tensors:
        raise SystemExit(
            f"HOLD: inventory missing {TARGET}"
        )

    if TARGET not in pilots:
        raise SystemExit(
            f"HOLD: pilot missing {TARGET}"
        )

    tensor = tensors[TARGET]
    pilot_tensor = pilots[TARGET]

    if tensor["type"] != "Q8_0":
        raise SystemExit(
            f"HOLD: target is not Q8_0: {TARGET}"
        )

    dims = [int(x) for x in tensor["dims"]]

    elements = int(tensor["elements"])
    dims_elements = product(dims)

    if elements != dims_elements:
        raise SystemExit(
            "HOLD: dimension/product mismatch\n"
            f"dims product: {dims_elements}\n"
            f"elements:     {elements}"
        )

    if elements % QK8_0 != 0:
        raise SystemExit(
            "HOLD: Q8_0 element count is not "
            "divisible by 32"
        )

    expected_blocks = elements // QK8_0
    span_bytes = int(tensor["span_bytes"])

    expected_span = (
        expected_blocks * BLOCK_BYTES
    )

    if span_bytes != expected_span:
        raise SystemExit(
            "HOLD: Q8_0 span mismatch\n"
            f"blocks:        {expected_blocks}\n"
            f"expected span: {expected_span}\n"
            f"actual span:   {span_bytes}"
        )

    if (
        span_bytes
        != int(pilot_tensor["span_bytes"])
    ):
        raise SystemExit(
            "HOLD: pilot span drift"
        )

    with SOURCE.open("rb") as f:
        f.seek(int(tensor["file_start"]))
        raw = f.read(span_bytes)

    if len(raw) != span_bytes:
        raise SystemExit(
            "HOLD: truncated tensor read"
        )

    source_hash = sha256_bytes(raw)

    if (
        source_hash
        != tensor["payload_sha256"]
        or source_hash
        != pilot_tensor["payload_sha256"]
    ):
        raise SystemExit(
            "HOLD: Q8_0 payload hash mismatch"
        )

    rebuilt = bytearray()

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

    for block_index in range(expected_blocks):
        start = block_index * BLOCK_BYTES
        block = raw[
            start:start + BLOCK_BYTES
        ]

        if len(block) != BLOCK_BYTES:
            raise SystemExit(
                f"HOLD: truncated block {block_index}"
            )

        scale_raw = block[:2]
        quant_raw = block[2:]

        # GGML Q8_0 block:
        #
        #   ggml_half d;
        #   int8_t qs[32];
        #
        # Decode the FP16 scale numerically.
        scale = struct.unpack(
            "<e",
            scale_raw,
        )[0]

        if not math.isfinite(scale):
            raise SystemExit(
                "HOLD: non-finite Q8_0 scale at "
                f"block {block_index}"
            )

        finite_scales += 1

        if scale == 0.0:
            zero_scales += 1

        if scale_min is None or scale < scale_min:
            scale_min = scale

        if scale_max is None or scale > scale_max:
            scale_max = scale

        scale_sum += scale

        # Decode all 32 signed quantized values.
        quants = struct.unpack(
            "<32b",
            quant_raw,
        )

        # Independently rebuild the block from the
        # interpreted FP16 scale and int8 values.
        rebuilt_scale = struct.pack(
            "<e",
            scale,
        )

        rebuilt_quants = struct.pack(
            "<32b",
            *quants,
        )

        rebuilt.extend(
            rebuilt_scale
            + rebuilt_quants
        )

        for q in quants:
            quant_count += 1
            quant_sum += q

            if q < quant_min:
                quant_min = q

            if q > quant_max:
                quant_max = q

            # Numerical Q8_0 dequantization.
            value = scale * q

            if not math.isfinite(value):
                raise SystemExit(
                    "HOLD: non-finite dequantized "
                    f"value at block {block_index}"
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

    if finite_scales != expected_blocks:
        raise SystemExit(
            "HOLD: scale count mismatch"
        )

    if quant_count != elements:
        raise SystemExit(
            "HOLD: quantized element count mismatch"
        )

    rebuilt = bytes(rebuilt)

    if len(rebuilt) != span_bytes:
        raise SystemExit(
            "HOLD: reconstructed size mismatch"
        )

    rebuilt_hash = sha256_bytes(
        rebuilt
    )

    byte_equal = rebuilt == raw

    hash_equal = (
        rebuilt_hash
        == source_hash
        == tensor["payload_sha256"]
        == pilot_tensor["payload_sha256"]
    )

    passed = (
        byte_equal
        and hash_equal
        and finite_scales == expected_blocks
        and quant_count == elements
    )

    if not passed:
        raise SystemExit(
            "HOLD: Q8_0 numeric round-trip failed"
        )

    output = {
        "schema":
            "openmind.maf_q8_0_numeric_roundtrip.v1",
        "target":
            TARGET,
        "dims":
            dims,
        "elements":
            elements,
        "qk":
            QK8_0,
        "block_bytes":
            BLOCK_BYTES,
        "block_count":
            expected_blocks,
        "span_bytes":
            span_bytes,
        "source_sha256":
            source_hash,
        "reencoded_sha256":
            rebuilt_hash,
        "finite_scale_count":
            finite_scales,
        "zero_scale_count":
            zero_scales,
        "scale_min":
            scale_min,
        "scale_max":
            scale_max,
        "scale_mean":
            scale_sum / expected_blocks,
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
        "byte_equal":
            byte_equal,
        "hash_equal":
            hash_equal,
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
        " OPENMIND / PHASE 6E — "
        "Q8_0 NUMERIC ROUND TRIP"
    )
    print("=" * 72)

    print("target       :", TARGET)
    print("dims         :", dims)
    print("elements     :", f"{elements:,}")
    print("blocks       :", f"{expected_blocks:,}")
    print("block bytes  :", BLOCK_BYTES)
    print("span bytes   :", f"{span_bytes:,}")
    print()

    print(
        "finite scales:",
        f"{finite_scales:,}",
    )
    print(
        "zero scales  :",
        f"{zero_scales:,}",
    )
    print(
        "scale range  :",
        scale_min,
        "to",
        scale_max,
    )
    print()

    print(
        "quant range  :",
        quant_min,
        "to",
        quant_max,
    )
    print(
        "dequant range:",
        dequant_min,
        "to",
        dequant_max,
    )
    print()

    print(
        "source hash  :",
        source_hash,
    )
    print(
        "rebuilt hash :",
        rebuilt_hash,
    )
    print(
        "bytes equal  :",
        byte_equal,
    )
    print(
        "hash equal   :",
        hash_equal,
    )
    print(
        "all pass     :",
        passed,
    )

    print()
    print("PHASE 6E PASS")


if __name__ == "__main__":
    main()
