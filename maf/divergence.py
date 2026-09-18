import math
import re
from pathlib import Path

import numpy as np

from .gguf_reader import load_model
from .q8_decode import decode_tensor as decode_q8_tensor


Q8_0 = 8
F32 = 0


def stats(x):
    x = np.asarray(x, dtype=np.float32)

    mean = float(np.mean(x))
    std = float(np.std(x))
    rms = float(np.sqrt(np.mean(x * x)))
    minimum = float(np.min(x))
    maximum = float(np.max(x))
    zero = float(np.mean(x == 0.0))

    return {
        "mean": mean,
        "std": std,
        "rms": rms,
        "min": minimum,
        "max": maximum,
        "zero": zero,
    }


def decode_tensor(t):
    tensor_type = int(t.tensor_type)

    if tensor_type == F32:
        return np.asarray(t.data, dtype=np.float32).reshape(
            tuple(int(x) for x in t.shape)
        )

    if tensor_type == Q8_0:
        return decode_q8_tensor(t)

    raise ValueError(
        f"Unsupported tensor type {tensor_type} for {t.name}"
    )


def cosine_similarity(a, b):
    a = np.asarray(a, dtype=np.float32).reshape(-1)
    b = np.asarray(b, dtype=np.float32).reshape(-1)

    denom = float(np.linalg.norm(a) * np.linalg.norm(b))

    if denom == 0.0:
        return 1.0 if np.array_equal(a, b) else 0.0

    return float(np.dot(a, b) / denom)


def relative_l2(a, b):
    a = np.asarray(a, dtype=np.float32).reshape(-1)
    b = np.asarray(b, dtype=np.float32).reshape(-1)

    numerator = float(np.linalg.norm(a - b))
    denominator = float(np.linalg.norm(a))

    if denominator == 0.0:
        return 0.0 if numerator == 0.0 else math.inf

    return numerator / denominator


def tensor_divergence(a, b):
    sa = stats(a)
    sb = stats(b)

    return {
        "mean_delta": abs(sb["mean"] - sa["mean"]),
        "std_delta": abs(sb["std"] - sa["std"]),
        "rms_delta": abs(sb["rms"] - sa["rms"]),
        "zero_delta": abs(sb["zero"] - sa["zero"]),
        "relative_l2": relative_l2(a, b),
        "cosine": cosine_similarity(a, b),
    }


def profile(path):
    reader = load_model(path)

    tensors = {
        t.name: t
        for t in reader.tensors
    }

    layer_pattern = re.compile(r"blk\.(\d+)\.(.+)")

    layers = {}

    for name, tensor in tensors.items():
        match = layer_pattern.match(name)

        if not match:
            continue

        layer = int(match.group(1))
        component = match.group(2)

        layers.setdefault(layer, {})[component] = tensor

    print("=" * 70)
    print(" MAF / LAYER NUMERICAL DIVERGENCE")
    print("=" * 70)

    print("Model:", path)
    print("Layers:", len(layers))
    print()

    decoded = {}

    for layer_id in sorted(layers):
        decoded[layer_id] = {}

        for component, tensor in layers[layer_id].items():
            decoded[layer_id][component] = decode_tensor(tensor)

    components = sorted(
        set.intersection(
            *[
                set(decoded[layer].keys())
                for layer in decoded
            ]
        )
    )

    print("Components:", len(components))
    print()

    aggregate = []

    for layer_id in range(1, len(decoded)):
        previous = decoded[layer_id - 1]
        current = decoded[layer_id]

        component_scores = []

        for component in components:
            result = tensor_divergence(
                previous[component],
                current[component],
            )

            component_scores.append(result)

        mean_l2 = float(
            np.mean([
                x["relative_l2"]
                for x in component_scores
            ])
        )

        mean_cosine = float(
            np.mean([
                x["cosine"]
                for x in component_scores
            ])
        )

        mean_std_delta = float(
            np.mean([
                x["std_delta"]
                for x in component_scores
            ])
        )

        mean_zero_delta = float(
            np.mean([
                x["zero_delta"]
                for x in component_scores
            ])
        )

        aggregate.append({
            "layer": layer_id,
            "relative_l2": mean_l2,
            "cosine": mean_cosine,
            "std_delta": mean_std_delta,
            "zero_delta": mean_zero_delta,
        })

        print(
            f"{layer_id - 1:02d} -> {layer_id:02d} | "
            f"L2={mean_l2:.6f} | "
            f"COS={mean_cosine:.6f} | "
            f"STDΔ={mean_std_delta:.6e} | "
            f"ZEROΔ={mean_zero_delta:.6e}"
        )

    print()
    print("=" * 70)
    print(" DIVERGENCE SUMMARY")
    print("=" * 70)

    max_l2 = max(
        aggregate,
        key=lambda x: x["relative_l2"]
    )

    min_cos = min(
        aggregate,
        key=lambda x: x["cosine"]
    )

    print(
        "Maximum relative L2 : "
        f"{max_l2['relative_l2']:.6f} "
        f"at {max_l2['layer'] - 1:02d}->{max_l2['layer']:02d}"
    )

    print(
        "Minimum cosine      : "
        f"{min_cos['cosine']:.6f} "
        f"at {min_cos['layer'] - 1:02d}->{min_cos['layer']:02d}"
    )

    print()
    print("=" * 70)
    print(" MAF / NUMERICAL DIVERGENCE COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    model = (
        Path.home()
        / "qwen2.5-coder-q8_0.gguf"
    )

    profile(model)
