import hashlib
import json
from pathlib import Path

SOURCE = Path.home() / "qwen2.5-coder-q8_0.gguf"
INDEX = Path("experiments/model_fractal/maf_index_v1.json")
STRUCTURE = Path("experiments/model_fractal/gguf_structure_v1.json")
OUT = Path("experiments/model_fractal/maf_index_validation_v1.json")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def main():
    for p in (SOURCE, INDEX, STRUCTURE):
        if not p.exists():
            raise SystemExit(f"Missing required artifact: {p}")

    index = json.loads(
        INDEX.read_text(encoding="utf-8")
    )

    structure = json.loads(
        STRUCTURE.read_text(encoding="utf-8")
    )

    raw_size = SOURCE.stat().st_size
    source_hash = sha256_bytes(SOURCE.read_bytes())

    expected_hash = index["source"]["sha256"]

    print("=" * 72)
    print(" OPENMIND / INDEXED MAF ACCESS VALIDATION V1")
    print("=" * 72)
    print(f"source: {SOURCE}")
    print(f"source bytes: {raw_size:,}")
    print(f"source sha256: {source_hash}")

    if source_hash != expected_hash:
        raise SystemExit(
            "SOURCE HASH MISMATCH\n"
            f"actual:   {source_hash}\n"
            f"expected: {expected_hash}"
        )

    entries = index["index"]

    if len(entries) != 339:
        raise SystemExit(
            f"Expected 339 index entries, got {len(entries)}"
        )

    data_start = int(
        structure["gguf"]["tensor_data_start"]
    )

    if data_start != 5950528:
        raise SystemExit(
            f"Unexpected tensor data start: {data_start}"
        )

    verified = []
    layer_map = {}
    global_tensors = []

    print()
    print("=== VERIFY INDEXED PAYLOADS ===")

    with SOURCE.open("rb") as f:
        for number, (name, tensor) in enumerate(
            entries.items(),
            start=1,
        ):
            file_start = int(tensor["file_start"])
            span = int(tensor["span_bytes"])
            elements = int(tensor["elements"])
            decoded = int(tensor["decoded_elements"])

            if file_start < data_start:
                raise SystemExit(
                    f"BEFORE DATA START: {name}"
                )

            if span <= 0:
                raise SystemExit(
                    f"INVALID SPAN: {name}"
                )

            if file_start + span > raw_size:
                raise SystemExit(
                    f"OUT OF BOUNDS: {name}"
                )

            if decoded != elements:
                raise SystemExit(
                    f"ELEMENT COUNT MISMATCH: {name}"
                )

            f.seek(file_start)
            payload = f.read(span)

            if len(payload) != span:
                raise SystemExit(
                    f"TRUNCATED PAYLOAD: {name}"
                )

            actual_payload_hash = sha256_bytes(payload)

            if actual_payload_hash != tensor["payload_sha256"]:
                raise SystemExit(
                    f"PAYLOAD HASH MISMATCH: {name}\n"
                    f"index:  {tensor['payload_sha256']}\n"
                    f"actual: {actual_payload_hash}"
                )

            node = {
                "name": name,
                "type": tensor["type"],
                "dims": list(tensor["dims"]),
                "elements": elements,
                "file_start": file_start,
                "span_bytes": span,
                "payload_sha256": actual_payload_hash,
            }

            if name.startswith("blk."):
                parts = name.split(".")

                if len(parts) < 3:
                    raise SystemExit(
                        f"INVALID LAYER NAME: {name}"
                    )

                if not parts[1].isdigit():
                    raise SystemExit(
                        f"INVALID LAYER ID: {name}"
                    )

                layer = int(parts[1])
                component = ".".join(parts[2:])

                node["component"] = component

                layer_map.setdefault(layer, []).append(node)

            else:
                global_tensors.append(node)

            verified.append(name)

            if number % 50 == 0 or number == len(entries):
                print(
                    f"verified: {number}/{len(entries)}"
                )

    # ------------------------------------------------------------
    # Complete topology reconstruction
    # ------------------------------------------------------------

    layer_ids = sorted(layer_map)

    if layer_ids != list(range(28)):
        raise SystemExit(
            f"INVALID LAYER IDS: {layer_ids}"
        )

    for layer in layer_ids:
        layer_map[layer].sort(
            key=lambda x: (
                x["file_start"],
                x["name"],
            )
        )

        if len(layer_map[layer]) != 12:
            raise SystemExit(
                f"LAYER {layer} HAS "
                f"{len(layer_map[layer])} TENSORS"
            )

    global_tensors.sort(
        key=lambda x: (
            x["file_start"],
            x["name"],
        )
    )

    # ------------------------------------------------------------
    # Structural fingerprint topology comparison
    # ------------------------------------------------------------

    structure_layers = structure["layers"]

    topology_mismatches = []

    for layer in layer_ids:
        structure_layer = structure_layers[str(layer)]

        if isinstance(structure_layer, dict):
            expected = sorted(
                structure_layer.keys()
            )
        elif isinstance(structure_layer, list):
            expected = sorted(
                x["component"]
                if isinstance(x, dict) and "component" in x
                else x
                for x in structure_layer
            )
        else:
            raise SystemExit(
                f"UNSUPPORTED STRUCTURE LAYER SCHEMA: "
                f"layer={layer}"
            )

        actual = sorted(
            x["component"]
            for x in layer_map[layer]
        )

        if expected != actual:
            topology_mismatches.append({
                "layer": layer,
                "expected": expected,
                "actual": actual,
            })

    if topology_mismatches:
        raise SystemExit(
            "TOPOLOGY MISMATCHES DETECTED:\n"
            + json.dumps(
                topology_mismatches,
                indent=2,
            )
        )

    # ------------------------------------------------------------
    # Global tensor validation
    # ------------------------------------------------------------

    if len(global_tensors) != 3:
        raise SystemExit(
            f"Expected 3 global tensors, got "
            f"{len(global_tensors)}"
        )

    # ------------------------------------------------------------
    # No-overlap validation
    # ------------------------------------------------------------

    all_tensors = (
        global_tensors
        + [
            tensor
            for layer in layer_ids
            for tensor in layer_map[layer]
        ]
    )

    all_tensors.sort(
        key=lambda x: (
            x["file_start"],
            x["name"],
        )
    )

    overlaps = []

    for previous, current in zip(
        all_tensors,
        all_tensors[1:],
    ):
        previous_end = (
            previous["file_start"]
            + previous["span_bytes"]
        )

        if current["file_start"] < previous_end:
            overlaps.append({
                "previous": previous["name"],
                "current": current["name"],
            })

    if overlaps:
        raise SystemExit(
            "TENSOR OVERLAPS DETECTED:\n"
            + json.dumps(
                overlaps,
                indent=2,
            )
        )

    # ------------------------------------------------------------
    # Canonical reconstruction hash
    # ------------------------------------------------------------

    canonical = {
        "source_sha256": source_hash,
        "tensor_count": len(verified),
        "global_tensors": global_tensors,
        "layers": {
            str(layer): layer_map[layer]
            for layer in layer_ids
        },
    }

    canonical_bytes = json.dumps(
        canonical,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    reconstruction_hash = sha256_bytes(
        canonical_bytes
    )

    # ------------------------------------------------------------
    # Output artifact
    # ------------------------------------------------------------

    output = {
        "format":
            "openmind.maf_index_validation.v1",

        "source": {
            "path": str(SOURCE),
            "sha256": source_hash,
            "bytes": raw_size,
        },

        "index": {
            "path": str(INDEX),
            "index_sha256":
                index["representation"]["index_sha256"],
        },

        "validation": {
            "tensor_count": len(verified),
            "payloads_verified": len(verified),
            "layers_reconstructed": len(layer_ids),
            "global_tensors": len(global_tensors),
            "components_per_layer": 12,
            "topology_mismatches":
                len(topology_mismatches),
            "overlaps": len(overlaps),
        },

        "reconstruction_sha256":
            reconstruction_hash,

        "layers": {
            str(layer): {
                "tensor_count":
                    len(layer_map[layer]),
                "components": [
                    x["component"]
                    for x in layer_map[layer]
                ],
            }
            for layer in layer_ids
        },

        "global_tensor_names": [
            x["name"]
            for x in global_tensors
        ],
    }

    OUT.write_text(
        json.dumps(
            output,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print()
    print("=== VALIDATION RESULT ===")
    print(f"index entries:          {len(entries)}")
    print(f"payloads verified:      {len(verified)}")
    print(f"layers reconstructed:   {len(layer_ids)}")
    print(f"global tensors:         {len(global_tensors)}")
    print(f"components/layer:       12")
    print(f"topology mismatches:    {len(topology_mismatches)}")
    print(f"tensor overlaps:        {len(overlaps)}")
    print(f"reconstruction sha256:  {reconstruction_hash}")
    print(f"output:                 {OUT}")
    print()
    print("ALL 339 PAYLOADS VERIFIED")
    print("28-LAYER TOPOLOGY RECONSTRUCTED")
    print("NO TENSOR OVERLAPS")
    print("INDEXED MAF VALIDATION COMPLETE")


if __name__ == "__main__":
    main()
