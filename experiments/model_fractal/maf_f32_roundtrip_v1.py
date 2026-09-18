#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path


SOURCE = Path.home() / "qwen2.5-coder-q8_0.gguf"

INVENTORY = Path(
    "experiments/model_fractal/"
    "gguf_tensor_inventory_v1.json"
)

PILOT = Path(
    "experiments/model_fractal/"
    "maf_pilot_manifest_v1.json"
)

RESULT = Path(
    "experiments/model_fractal/"
    "maf_f32_roundtrip_v1.json"
)

EXPECTED_INVENTORY_FILE_SHA256 = (
    "7acf6d5dc672182aee0244b1bb85a47466f33dbdcdf10bde863e24f3659240ee"
)

EXPECTED_PILOT_FILE_SHA256 = (
    "690ec47152646907eed1ca873ff9cf86352777e79b116a6c2d63186e33f859d0"
)

TARGETS = (
    "output_norm.weight",
    "blk.0.attn_norm.weight",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()


def main():
    for path in (
        SOURCE,
        INVENTORY,
        PILOT,
    ):
        if not path.exists():
            raise SystemExit(
                f"HOLD: missing required artifact: {path}"
            )

    inventory_file_hash = sha256_file(INVENTORY)
    pilot_file_hash = sha256_file(PILOT)

    if inventory_file_hash != EXPECTED_INVENTORY_FILE_SHA256:
        raise SystemExit(
            "HOLD: inventory artifact drift\n"
            f"expected: {EXPECTED_INVENTORY_FILE_SHA256}\n"
            f"actual:   {inventory_file_hash}"
        )

    if pilot_file_hash != EXPECTED_PILOT_FILE_SHA256:
        raise SystemExit(
            "HOLD: pilot manifest artifact drift\n"
            f"expected: {EXPECTED_PILOT_FILE_SHA256}\n"
            f"actual:   {pilot_file_hash}"
        )

    inventory = json.loads(
        INVENTORY.read_text(
            encoding="utf-8"
        )
    )

    pilot = json.loads(
        PILOT.read_text(
            encoding="utf-8"
        )
    )

    tensors = {
        t["name"]: t
        for t in inventory["tensors"]
    }

    pilot_items = {
        t["name"]: t
        for t in pilot["pilot"]
    }

    source_expected_hash = (
        inventory["source"]["sha256"]
    )

    source_actual_hash = sha256_file(SOURCE)

    if source_actual_hash != source_expected_hash:
        raise SystemExit(
            "HOLD: GGUF source drift\n"
            f"expected: {source_expected_hash}\n"
            f"actual:   {source_actual_hash}"
        )

    results = []

    with SOURCE.open("rb") as source:
        for name in TARGETS:
            if name not in tensors:
                raise SystemExit(
                    f"HOLD: inventory missing {name}"
                )

            if name not in pilot_items:
                raise SystemExit(
                    f"HOLD: pilot missing {name}"
                )

            tensor = tensors[name]
            pilot_tensor = pilot_items[name]

            if tensor["type"] != "F32":
                raise SystemExit(
                    f"HOLD: {name} is not F32"
                )

            if pilot_tensor["type"] != "F32":
                raise SystemExit(
                    f"HOLD: pilot {name} is not F32"
                )

            if tensor["dims"] != pilot_tensor["dims"]:
                raise SystemExit(
                    f"HOLD: dims drift for {name}"
                )

            if int(tensor["span_bytes"]) != int(
                pilot_tensor["span_bytes"]
            ):
                raise SystemExit(
                    f"HOLD: span drift for {name}"
                )

            if (
                tensor["payload_sha256"]
                != pilot_tensor["payload_sha256"]
            ):
                raise SystemExit(
                    f"HOLD: manifest hash drift for {name}"
                )

            file_start = int(
                tensor["file_start"]
            )

            span_bytes = int(
                tensor["span_bytes"]
            )

            source.seek(file_start)

            raw_payload = source.read(
                span_bytes
            )

            if len(raw_payload) != span_bytes:
                raise SystemExit(
                    f"HOLD: truncated source payload: {name}"
                )

            source_slice_hash = sha256_bytes(
                raw_payload
            )

            if (
                source_slice_hash
                != tensor["payload_sha256"]
            ):
                raise SystemExit(
                    f"HOLD: source slice mismatch: {name}"
                )

            # -------------------------------------------------
            # MAF OBJECT V1
            #
            # This phase intentionally performs NO numerical
            # reinterpretation or transformation.
            #
            # The payload is treated as an opaque exact byte
            # object with deterministic addressing metadata.
            # -------------------------------------------------

            maf_object = {
                "schema":
                    "openmind.maf.raw_tensor_object.v1",
                "name":
                    name,
                "type":
                    tensor["type"],
                "dims":
                    tensor["dims"],
                "elements":
                    int(tensor["elements"]),
                "source_offset":
                    int(tensor["offset"]),
                "source_file_start":
                    file_start,
                "span_bytes":
                    span_bytes,
                "payload_sha256":
                    source_slice_hash,
                "payload":
                    raw_payload,
            }

            # Reconstruction is intentionally just retrieval
            # from the exact object payload in Phase 6C.

            reconstructed = maf_object[
                "payload"
            ]

            reconstructed_hash = sha256_bytes(
                reconstructed
            )

            byte_equal = (
                reconstructed == raw_payload
            )

            hash_equal = (
                reconstructed_hash
                == source_slice_hash
                == tensor["payload_sha256"]
                == pilot_tensor["payload_sha256"]
            )

            passed = (
                byte_equal
                and hash_equal
                and len(reconstructed)
                == span_bytes
            )

            results.append({
                "name":
                    name,
                "type":
                    tensor["type"],
                "dims":
                    tensor["dims"],
                "span_bytes":
                    span_bytes,
                "file_start":
                    file_start,
                "offset":
                    int(tensor["offset"]),
                "manifest_sha256":
                    pilot_tensor[
                        "payload_sha256"
                    ],
                "source_slice_sha256":
                    source_slice_hash,
                "reconstructed_sha256":
                    reconstructed_hash,
                "byte_equal":
                    byte_equal,
                "hash_equal":
                    hash_equal,
                "pass":
                    passed,
            })

    if len(results) != 2:
        raise SystemExit(
            "HOLD: expected exactly 2 F32 results"
        )

    if not all(
        r["pass"]
        for r in results
    ):
        raise SystemExit(
            "HOLD: one or more F32 round trips failed"
        )

    output = {
        "schema":
            "openmind.maf_f32_roundtrip.v1",
        "source":
            str(SOURCE),
        "source_sha256":
            source_actual_hash,
        "inventory_file_sha256":
            inventory_file_hash,
        "pilot_manifest_file_sha256":
            pilot_file_hash,
        "target_count":
            len(results),
        "total_payload_bytes":
            sum(
                r["span_bytes"]
                for r in results
            ),
        "transformation":
            "opaque byte-preserving object",
        "numeric_decode":
            False,
        "results":
            results,
        "all_pass":
            all(
                r["pass"]
                for r in results
            ),
    }

    RESULT.write_text(
        json.dumps(
            output,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print(
        " OPENMIND / PHASE 6C — "
        "F32 EXACT RAW-SPAN ROUND TRIP"
    )
    print("=" * 72)

    print(
        f"source sha256 : {source_actual_hash}"
    )

    print(
        f"targets       : {len(results)}"
    )

    print(
        "payload bytes : "
        f"{sum(r['span_bytes'] for r in results):,}"
    )

    print()

    for r in results:
        print(r["name"])
        print(
            f"  span       : "
            f"{r['span_bytes']:,}"
        )
        print(
            f"  manifest   : "
            f"{r['manifest_sha256']}"
        )
        print(
            f"  source     : "
            f"{r['source_slice_sha256']}"
        )
        print(
            f"  reconstructed: "
            f"{r['reconstructed_sha256']}"
        )
        print(
            f"  byte equal : "
            f"{r['byte_equal']}"
        )
        print(
            f"  PASS       : "
            f"{r['pass']}"
        )
        print()

    print(
        "numeric decode       : NO"
    )
    print(
        "payload transformed  : NO"
    )
    print(
        "exact reconstruction : YES"
    )
    print(
        f"result                : {RESULT}"
    )
    print(
        "PHASE 6C PASS"
    )


if __name__ == "__main__":
    main()
