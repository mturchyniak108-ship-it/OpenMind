import numpy as np

from .gguf_reader import load_model
from .q8_decode import decode_tensor

Q8_0 = 8
F32 = 0


def fingerprint_values(values):
    values = np.asarray(values, dtype=np.float32)

    abs_values = np.abs(values)

    return {
        "mean": float(np.mean(values)),
        "std": float(np.std(values)),
        "min": float(np.min(values)),
        "max": float(np.max(values)),
        "abs_mean": float(np.mean(abs_values)),
        "rms": float(np.sqrt(np.mean(values * values))),
        "zero_fraction": float(np.mean(values == 0.0)),
    }


def fingerprint_tensor(tensor):
    tensor_type = int(tensor.tensor_type)

    shape = tuple(int(x) for x in tensor.shape)

    if tensor_type == Q8_0:
        values = decode_tensor(tensor)

    elif tensor_type == F32:
        values = np.asarray(
            tensor.data,
            dtype=np.float32,
        ).reshape(shape)

    else:
        raise ValueError(
            f"Unsupported tensor type: {tensor_type}"
        )

    result = {
        "name": tensor.name,
        "shape": shape,
        "type": tensor_type,
        "elements": int(np.prod(shape)),
        "raw_bytes": int(tensor.data.nbytes),
    }

    result.update(fingerprint_values(values))

    return result


def model_fingerprint(path):
    reader = load_model(path)

    results = []

    for tensor in reader.tensors:
        results.append(
            fingerprint_tensor(tensor)
        )

    return results


def print_fingerprint(path):
    results = model_fingerprint(path)

    print("=" * 100)
    print(" MAF / MODEL NUMERICAL FINGERPRINT")
    print("=" * 100)

    print("Model:", path)
    print("Tensors:", len(results))
    print()

    for i, r in enumerate(results):
        print(
            f"{i:03d} "
            f"{r['name']:40s} "
            f"shape={str(r['shape']):22s} "
            f"type={r['type']:2d} "
            f"mean={r['mean']:+.6e} "
            f"std={r['std']:.6e} "
            f"rms={r['rms']:.6e}"
        )

    print()
    print("=" * 100)
    print(" FINGERPRINT COMPLETE")
    print("=" * 100)


if __name__ == "__main__":
    from pathlib import Path

    print_fingerprint(
        Path.home() / "qwen2.5-coder-q8_0.gguf"
    )
