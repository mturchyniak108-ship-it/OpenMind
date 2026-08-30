import hashlib
import json
from pathlib import Path

SOURCE = Path.home() / "qwen2.5-coder-q8_0.gguf"
STRUCTURE = Path("experiments/model_fractal/gguf_structure_v1.json")
VALIDATION = Path("experiments/model_fractal/gguf_tensor_validation_v1.json")
OUT = Path("experiments/model_fractal/gguf_tensor_inventory_v1.json")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def main():
    for p in (SOURCE, STRUCTURE, VALIDATION):
        if not p.exists():
            raise SystemExit(f"Missing required artifact: {p}")

    structure = json.loads(
        STRUCTURE.read_text(encoding="utf-8")
    )

    validation = json.loads(
        VALIDATION.read_text(encoding="utf-8")
    )

    raw_size = SOURCE.stat().st_size

    actual_source_hash = sha256_bytes(
        SOURCE.read_bytes()
    )

    validation_source = validation["source"]

    if actual_source_hash != validation_source["sha256"]:
        raise SystemExit(
            "SOURCE HASH DOES NOT MATCH VALIDATION\n"
            f"actual:     {actual_source_hash}\n"
            f"validation: {validation_source['sha256']}"
        )

    structure_source = structure["source"]

    if structure_source != str(SOURCE):
        raise SystemExit(
            "STRUCTURE SOURCE PATH DOES NOT MATCH SOURCE"
        )

    gguf = structure["gguf"]

    data_start = int(gguf["tensor_data_start"])
    tensor_count = int(gguf["tensor_count"])
    file_size = int(gguf["file_size"])

    if file_size != raw_size:
        raise SystemExit(
            f"FILE SIZE MISMATCH: structure={file_size} "
            f"actual={raw_size}"
        )

    results = validation["results"]

    if len(results) != tensor_count:
        raise SystemExit(
            f"TENSOR COUNT MISMATCH: validation={len(results)} "
            f"structure={tensor_count}"
        )

    extracted = []

    with SOURCE.open("rb") as f:
        for r in results:
            name = r["name"]
            typ = r["type"]
            dims = list(r["dims"])

            file_start = int(r["file_start"])
            span = int(r["span_bytes"])

            if file_start < data_start:
                raise ValueError(
                    f"{name}: tensor starts before tensor data region"
                )

            if file_start + span > raw_size:
                raise ValueError(
                    f"{name}: tensor exceeds source file"
                )

            f.seek(file_start)
            payload = f.read(span)

            if len(payload) != span:
                raise ValueError(
                    f"{name}: truncated payload"
                )

            payload_hash = sha256_bytes(payload)

            if payload_hash != r["payload_sha256"]:
                raise SystemExit(
                    f"PAYLOAD HASH MISMATCH: {name}\n"
                    f"validation: {r['payload_sha256']}\n"
                    f"actual:     {payload_hash}"
                )

            extracted.append({
                "index": int(r["index"]),
                "name": name,
                "type": typ,
                "dims": dims,
                "elements": int(r["elements"]),
                "offset": file_start - data_start,
                "file_start": file_start,
                "span_bytes": span,
                "payload_sha256": payload_hash,
                "decoded_elements": int(
                    r["decoded_elements"]
                ),
                "validation": r["validation"],
            })

    extracted.sort(
        key=lambda x: (
            x["file_start"],
            x["name"],
        )
    )

    for i, tensor in enumerate(extracted):
        if tensor["file_start"] + tensor["span_bytes"] > raw_size:
            raise SystemExit(
                f"OUT OF BOUNDS: {tensor['name']}"
            )

        if tensor["decoded_elements"] != tensor["elements"]:
            raise SystemExit(
                f"ELEMENT COUNT MISMATCH: {tensor['name']}"
            )

        if i > 0:
            previous = extracted[i - 1]

            previous_end = (
                previous["file_start"]
                + previous["span_bytes"]
            )

            if tensor["file_start"] < previous_end:
                raise SystemExit(
                    f"OVERLAPPING TENSORS: "
                    f"{previous['name']} -> {tensor['name']}"
                )

    canonical = json.dumps(
        extracted,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    manifest_hash = sha256_bytes(canonical)

    f32_count = sum(
        t["type"] == "F32"
        for t in extracted
    )

    q8_count = sum(
        t["type"] == "Q8_0"
        for t in extracted
    )

    output = {
        "format": "openmind.gguf_tensor_inventory.v1",
        "source": {
            "path": str(SOURCE),
            "sha256": actual_source_hash,
            "bytes": raw_size,
        },
        "gguf": {
            "version": int(gguf["version"]),
            "tensor_count": tensor_count,
            "tensor_data_start": data_start,
            "file_size": file_size,
            "alignment": int(gguf["alignment"]),
            "directory_end": int(gguf["directory_end"]),
        },
        "tensor_type_counts": {
            "F32": f32_count,
            "Q8_0": q8_count,
        },
        "manifest_sha256": manifest_hash,
        "tensors": extracted,
    }

    OUT.write_text(
        json.dumps(
            output,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print(" OPENMIND / DETERMINISTIC GGUF TENSOR MANIFEST V1")
    print("=" * 72)
    print(f"source bytes:       {raw_size:,}")
    print(f"source sha256:      {actual_source_hash}")
    print(f"GGUF version:       {gguf['version']}")
    print(f"data start:         {data_start}")
    print(f"tensor count:       {tensor_count}")
    print(f"F32 tensors:        {f32_count}")
    print(f"Q8_0 tensors:       {q8_count}")
    print(f"manifest sha256:    {manifest_hash}")
    print(f"output:             {OUT}")
    print()
    print("PAYLOAD HASHES VERIFIED")
    print("DETERMINISTIC EXTRACTION COMPLETE")


if __name__ == "__main__":
    main()
