import numpy as np

from .gguf_reader import load_model

Q8_0 = 8
F32 = 0
BLOCK = 32
BLOCK_BYTES = 34


def validate(path):
    reader = load_model(path)

    print("=" * 60)
    print(" MAF / FULL Q8_0 INTEGRITY VALIDATION")
    print("=" * 60)

    q8_count = 0
    f32_count = 0
    failures = []
    total_q8_bytes = 0
    total_q8_elements = 0

    for i, t in enumerate(reader.tensors):
        shape = tuple(int(x) for x in t.shape)
        typ = int(t.tensor_type)
        raw_bytes = int(t.data.nbytes)

        if typ == F32:
            f32_count += 1
            continue

        if typ != Q8_0:
            failures.append(
                f"{i:03d} {t.name}: unexpected type {typ}"
            )
            continue

        q8_count += 1

        # GGUF stores the logical tensor shape in reversed order
        # relative to the raw block layout exposed by GGUFReader.
        block_axis = shape[0]

        if block_axis % BLOCK != 0:
            failures.append(
                f"{i:03d} {t.name}: "
                f"dimension {block_axis} not divisible by {BLOCK}"
            )
            continue

        blocks = block_axis // BLOCK
        expected = blocks * BLOCK_BYTES * int(np.prod(shape[1:]))

        if raw_bytes != expected:
            failures.append(
                f"{i:03d} {t.name}: "
                f"raw={raw_bytes:,} expected={expected:,}"
            )
            continue

        total_q8_bytes += raw_bytes
        total_q8_elements += int(np.prod(shape))

    print()
    print("Tensor count       :", len(reader.tensors))
    print("Q8_0 tensors       :", q8_count)
    print("F32 tensors        :", f32_count)
    print("Q8_0 storage       :", f"{total_q8_bytes:,} bytes")
    print("Q8_0 logical elems :", f"{total_q8_elements:,}")
    print()

    if failures:
        print("FAILURES:")
        for failure in failures:
            print("  ", failure)

        print()
        print("=" * 60)
        print(" Q8_0 INTEGRITY FAILED")
        print("=" * 60)
        raise SystemExit(1)

    print("=" * 60)
    print(" Q8_0 INTEGRITY PASSED")
    print("=" * 60)


if __name__ == "__main__":
    from pathlib import Path

    validate(
        Path.home() / "qwen2.5-coder-q8_0.gguf"
    )
