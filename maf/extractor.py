import sys
from pathlib import Path

from .gguf_reader import load_model


Q8_0 = 8
F32 = 0


def inspect(path):
    reader = load_model(path)

    print("=" * 60)
    print(" MAF MODEL EXTRACTION CENSUS")
    print("=" * 60)

    print("Model:", path)
    print("Tensor count:", len(reader.tensors))
    print()

    total = 0
    q8 = 0
    f32 = 0

    for i, t in enumerate(reader.tensors):
        shape = tuple(int(x) for x in t.shape)
        size = int(t.data.nbytes)

        total += size

        if int(t.tensor_type) == Q8_0:
            q8 += 1
        elif int(t.tensor_type) == F32:
            f32 += 1

        print(
            f"{i:03d} "
            f"{t.name:40s} "
            f"{shape!s:24s} "
            f"type={int(t.tensor_type):2d} "
            f"bytes={size:,}"
        )

    print()
    print("=" * 60)
    print(" SUMMARY")
    print("=" * 60)
    print("Tensor bytes:", f"{total:,}")
    print("Q8_0 tensors:", q8)
    print("F32 tensors:", f32)


if __name__ == "__main__":
    model = (
        Path.home()
        / "qwen2.5-coder-q8_0.gguf"
    )

    inspect(model)
