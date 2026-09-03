import hashlib
import json
import math
import struct
from pathlib import Path

SOURCE = Path.home() / "qwen2.5-coder-q8_0.gguf"
INVENTORY = Path("experiments/model_fractal/gguf_structure_v1.json")
OUT = Path("experiments/model_fractal/gguf_tensor_validation_v1.json")

Q8_BLOCK_BYTES = 34
Q8_VALUES_PER_BLOCK = 32


def tensor_element_count(dims):
    n = 1
    for d in dims:
        n *= int(d)
    return n


def sha256_file(path, chunk_size=8 * 1024 * 1024):
    h = hashlib.sha256()

    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()


def sha256_region(f, start, size, chunk_size=8 * 1024 * 1024):
    h = hashlib.sha256()

    f.seek(start)
    remaining = size

    while remaining:
        chunk = f.read(min(chunk_size, remaining))

        if not chunk:
            raise EOFError(
                f"Unexpected EOF while hashing region "
                f"{start}:{start + size}"
            )

        h.update(chunk)
        remaining -= len(chunk)

    return h.hexdigest()


def validate_f32(f, start, span, expected):
    expected_bytes = expected * 4

    if span != expected_bytes:
        raise ValueError(
            f"F32 span mismatch: {span} != {expected_bytes}"
        )

    # Read only a small sample. Full tensor materialization is unnecessary.
    sample_bytes = min(span, 4096)

    f.seek(start)
    sample = f.read(sample_bytes)

    if len(sample) != sample_bytes:
        raise EOFError("Unexpected EOF in F32 tensor")

    if len(sample) % 4:
        raise ValueError("F32 sample is not 4-byte aligned")

    finite = 0
    nonfinite = 0
    max_abs = 0.0

    for (x,) in struct.iter_unpack("<f", sample):
        if math.isfinite(x):
            finite += 1
            max_abs = max(max_abs, abs(x))
        else:
            nonfinite += 1

    return {
        "structural_valid": True,
        "sample_elements": finite + nonfinite,
        "sample_finite": finite,
        "sample_nonfinite": nonfinite,
        "sample_max_abs": max_abs,
        "quantization_error": None,
    }


def validate_q8_0(f, start, span, expected):
    if expected % Q8_VALUES_PER_BLOCK:
        raise ValueError(
            f"Q8_0 element count not divisible by "
            f"{Q8_VALUES_PER_BLOCK}: {expected}"
        )

    expected_bytes = (
        expected // Q8_VALUES_PER_BLOCK
    ) * Q8_BLOCK_BYTES

    if span != expected_bytes:
        raise ValueError(
            f"Q8_0 span mismatch: {span} != {expected_bytes}"
        )

    # Validate every block's scale and layout, but never materialize
    # the complete tensor.
    f.seek(start)

    blocks = expected // Q8_VALUES_PER_BLOCK
    nonfinite_scales = 0
    zero_scales = 0
    max_abs_scale = 0.0

    for _ in range(blocks):
        block = f.read(Q8_BLOCK_BYTES)

        if len(block) != Q8_BLOCK_BYTES:
            raise EOFError("Unexpected EOF in Q8_0 tensor")

        scale = struct.unpack_from("<e", block, 0)[0]

        if not math.isfinite(scale):
            nonfinite_scales += 1

        if scale == 0.0:
            zero_scales += 1

        max_abs_scale = max(max_abs_scale, abs(scale))

        # Confirm the 32 signed int8 values can be decoded.
        struct.unpack_from("<32b", block, 2)

    return {
        "structural_valid": True,
        "blocks": blocks,
        "values_per_block": Q8_VALUES_PER_BLOCK,
        "nonfinite_scales": nonfinite_scales,
        "zero_scales": zero_scales,
        "max_abs_scale": max_abs_scale,
        "quantization_error": None,
    }


def main():
    if not SOURCE.exists():
        raise SystemExit(f"Missing source: {SOURCE}")

    if not INVENTORY.exists():
        raise SystemExit(f"Missing inventory: {INVENTORY}")

    inventory = json.loads(
        INVENTORY.read_text(encoding="utf-8")
    )

    source_info = inventory.get("source", "")
    if isinstance(source_info, dict):
        expected_hash = source_info.get("sha256")
    else:
        expected_hash = None

    print("=" * 72)
    print(" OPENMIND / GGUF TENSOR VALIDATION V1")
    print("=" * 72)

    print(f"source: {SOURCE}")
    print(f"file bytes: {SOURCE.stat().st_size:,}")

    print()
    print("=== SOURCE HASH ===")

    actual_hash = sha256_file(SOURCE)

    print(f"actual:   {actual_hash}")
    print(f"inventory:{expected_hash}")

    if expected_hash and actual_hash != expected_hash:
        raise SystemExit("SOURCE HASH MISMATCH")

    # Reconstruct the tensor list from the structural inventory.
    tensors = []

    for layer_id, layer in inventory.get("layers", {}).items():
        for component, tensor in layer.items():
            tensors.append({
                "name": tensor["name"],
                "type_name": tensor["type"],
                "dims": tensor["dims"],
                "file_start": tensor["file_start"],
                "span_bytes": tensor["span"],
            })

    for tensor in inventory.get("global_tensors", []):
        tensors.append({
            "name": tensor["name"],
            "type_name": tensor["type"],
            "dims": tensor["dims"],
            "file_start": tensor["file_start"],
            "span_bytes": tensor["span"],
        })

    tensors.sort(key=lambda x: x["file_start"])

    expected_count = inventory.get("gguf", {}).get(
        "tensor_count"
    )

    if expected_count is not None and len(tensors) != expected_count:
        raise SystemExit(
            f"INVENTORY TENSOR COUNT MISMATCH: "
            f"{len(tensors)} != {expected_count}"
        )

    print()
    print("=== INVENTORY ===")
    print(f"tensors: {len(tensors)}")

    results = []

    with SOURCE.open("rb") as f:

        previous_end = None

        for i, tensor in enumerate(tensors):

            name = tensor["name"]
            typ = tensor["type_name"]
            dims = tensor["dims"]
            start = int(tensor["file_start"])
            span = int(tensor["span_bytes"])

            if span < 0:
                raise ValueError(
                    f"{name}: negative span"
                )

            end = start + span

            if previous_end is not None and start < previous_end:
                raise ValueError(
                    f"{name}: tensor payload overlaps previous tensor"
                )

            previous_end = end

            expected = tensor_element_count(dims)

            if start < 0 or end > SOURCE.stat().st_size:
                raise ValueError(
                    f"{name}: payload outside source file"
                )

            if typ == "F32":
                validation = validate_f32(
                    f,
                    start,
                    span,
                    expected,
                )

            elif typ == "Q8_0":
                validation = validate_q8_0(
                    f,
                    start,
                    span,
                    expected,
                )

            else:
                raise ValueError(
                    f"{name}: unsupported tensor type {typ}"
                )

            payload_hash = sha256_region(
                f,
                start,
                span,
            )

            results.append({
                "index": i,
                "name": name,
                "type": typ,
                "dims": dims,
                "elements": expected,
                "file_start": start,
                "span_bytes": span,
                "payload_sha256": payload_hash,
                "decoded_elements": expected,
                "validation": validation,
            })

    type_counts = {}

    for r in results:
        typ = r["type"]
        type_counts[typ] = type_counts.get(typ, 0) + 1

    output = {
        "format": "openmind.gguf_tensor_validation.v1",

        "source": {
            "path": str(SOURCE),
            "sha256": actual_hash,
            "bytes": SOURCE.stat().st_size,
        },

        "inventory": {
            "path": str(INVENTORY),
            "sha256": sha256_file(INVENTORY),
        },

        "tensor_count": len(results),
        "validated_types": sorted(type_counts),
        "type_counts": type_counts,

        "validation_policy": {
            "full_tensor_materialization": False,
            "q8_0_decode": "structural block validation",
            "f32_decode": "sample validation",
            "quantization_error_claimed": False,
        },

        "results": results,
    }

    OUT.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )

    print()
    print("=== VALIDATED TYPES ===")

    for typ, count in sorted(type_counts.items()):
        print(f"{typ:<8} {count}")

    print()
    print(f"output: {OUT}")
    print(f"artifact bytes: {OUT.stat().st_size:,}")
    print()
    print("TENSOR VALIDATION COMPLETE")


if __name__ == "__main__":
    main()
