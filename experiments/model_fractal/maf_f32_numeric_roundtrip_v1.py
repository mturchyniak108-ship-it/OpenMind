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

ROUNDTRIP_6C = Path(
    "experiments/model_fractal/maf_f32_roundtrip_v1.json"
)

RESULT = Path(
    "experiments/model_fractal/maf_f32_numeric_roundtrip_v1.json"
)

EXPECTED = {
    "inventory":
        "7acf6d5dc672182aee0244b1bb85a47466f33dbdcdf10bde863e24f3659240ee",
    "pilot":
        "690ec47152646907eed1ca873ff9cf86352777e79b116a6c2d63186e33f859d0",
    "phase6c":
        "37c78d701a62cbc23ea1bf19596dd94257d8c9b96e08a5eb37c00b3147d92a7d",
}

TARGETS = (
    "output_norm.weight",
    "blk.0.attn_norm.weight",
)


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


def main():
    required = (
        SOURCE,
        INVENTORY,
        PILOT,
        ROUNDTRIP_6C,
    )

    for p in required:
        if not p.exists():
            raise SystemExit(
                f"HOLD: missing artifact: {p}"
            )

    checks = {
        "inventory": sha256_file(INVENTORY),
        "pilot": sha256_file(PILOT),
        "phase6c": sha256_file(ROUNDTRIP_6C),
    }

    for key, actual in checks.items():
        expected = EXPECTED[key]

        if actual != expected:
            raise SystemExit(
                f"HOLD: {key} drift\n"
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

    pilot_tensors = {
        t["name"]: t
        for t in pilot["pilot"]
    }

    results = []

    with SOURCE.open("rb") as f:
        for name in TARGETS:
            t = tensors[name]
            p = pilot_tensors[name]

            if t["type"] != "F32":
                raise SystemExit(
                    f"HOLD: not F32: {name}"
                )

            span = int(t["span_bytes"])
            elements = int(t["elements"])

            if span != elements * 4:
                raise SystemExit(
                    f"HOLD: F32 size mismatch: {name}"
                )

            f.seek(int(t["file_start"]))
            raw = f.read(span)

            if len(raw) != span:
                raise SystemExit(
                    f"HOLD: short read: {name}"
                )

            raw_hash = sha256_bytes(raw)

            if raw_hash != p["payload_sha256"]:
                raise SystemExit(
                    f"HOLD: payload drift: {name}"
                )

            # Actual numerical decoding to Python floats.
            values = struct.unpack(
                f"<{elements}f",
                raw,
            )

            finite_count = sum(
                math.isfinite(v)
                for v in values
            )

            if finite_count != elements:
                raise SystemExit(
                    f"HOLD: non-finite F32 value: {name}"
                )

            # Independent numerical re-encoding.
            rebuilt = struct.pack(
                f"<{elements}f",
                *values,
            )

            rebuilt_hash = sha256_bytes(
                rebuilt
            )

            byte_equal = rebuilt == raw
            hash_equal = rebuilt_hash == raw_hash

            passed = (
                byte_equal
                and hash_equal
                and finite_count == elements
            )

            results.append({
                "name": name,
                "elements": elements,
                "span_bytes": span,
                "finite_count": finite_count,
                "minimum": min(values),
                "maximum": max(values),
                "mean": (
                    sum(values) / elements
                ),
                "source_sha256": raw_hash,
                "reencoded_sha256": rebuilt_hash,
                "byte_equal": byte_equal,
                "pass": passed,
            })

    if not all(r["pass"] for r in results):
        raise SystemExit(
            "HOLD: numeric round-trip failure"
        )

    out = {
        "schema":
            "openmind.maf_f32_numeric_roundtrip.v1",
        "decode":
            "IEEE-754 little-endian F32 -> Python float",
        "encode":
            "Python float -> IEEE-754 little-endian F32",
        "target_count":
            len(results),
        "element_count":
            sum(r["elements"] for r in results),
        "payload_bytes":
            sum(r["span_bytes"] for r in results),
        "results":
            results,
        "all_pass":
            True,
    }

    RESULT.write_text(
        json.dumps(
            out,
            indent=2,
        ) + "\n"
    )

    print("=" * 72)
    print(
        " OPENMIND / PHASE 6D — "
        "F32 NUMERIC ROUND TRIP"
    )
    print("=" * 72)

    for r in results:
        print(r["name"])
        print(
            f"  elements : {r['elements']:,}"
        )
        print(
            f"  finite   : {r['finite_count']:,}"
        )
        print(
            f"  min      : {r['minimum']:.9g}"
        )
        print(
            f"  max      : {r['maximum']:.9g}"
        )
        print(
            f"  mean     : {r['mean']:.9g}"
        )
        print(
            f"  byte eq  : {r['byte_equal']}"
        )
        print(
            f"  PASS     : {r['pass']}"
        )
        print()

    print(
        "total elements :", 
        f"{out['element_count']:,}"
    )
    print(
        "payload bytes  :",
        f"{out['payload_bytes']:,}"
    )
    print(
        "all pass       :",
        out["all_pass"],
    )
    print("PHASE 6D PASS")


if __name__ == "__main__":
    main()
