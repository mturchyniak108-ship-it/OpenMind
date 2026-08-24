import re
import sys
from pathlib import Path
from collections import defaultdict

from .gguf_reader import load_model

Q8_0 = 8
F32 = 0


def profile(path):
    reader = load_model(path)

    layers = defaultdict(dict)
    global_tensors = []

    for t in reader.tensors:
        name = t.name

        match = re.match(r"blk\.(\d+)\.(.+)", name)

        if match:
            layer = int(match.group(1))
            component = match.group(2)
            layers[layer][component] = t
        else:
            global_tensors.append(t)

    print("=" * 70)
    print(" MAF / TRANSFORMER LAYER PROFILE")
    print("=" * 70)

    print("Model:", path)
    print("Tensor count:", len(reader.tensors))
    print("Detected layers:", len(layers))
    print()

    expected = [
        "attn_norm.weight",
        "attn_k.bias",
        "attn_k.weight",
        "attn_output.weight",
        "attn_q.bias",
        "attn_q.weight",
        "attn_v.bias",
        "attn_v.weight",
        "ffn_norm.weight",
        "ffn_down.weight",
        "ffn_gate.weight",
        "ffn_up.weight",
    ]

    for layer_id in sorted(layers):
        items = layers[layer_id]

        missing = [x for x in expected if x not in items]

        q8 = 0
        f32 = 0
        bytes_total = 0

        for t in items.values():
            tensor_type = int(t.tensor_type)
            bytes_total += int(t.data.nbytes)

            if tensor_type == Q8_0:
                q8 += 1
            elif tensor_type == F32:
                f32 += 1

        print(
            f"LAYER {layer_id:02d} | "
            f"tensors={len(items):2d} | "
            f"Q8={q8:2d} | "
            f"F32={f32:2d} | "
            f"bytes={bytes_total:,}"
        )

        if missing:
            print("         MISSING:", ", ".join(missing))

    print()
    print("=" * 70)
    print(" GLOBAL TENSORS")
    print("=" * 70)

    for t in global_tensors:
        print(
            f"{t.name:35s} "
            f"type={int(t.tensor_type):2d} "
            f"shape={tuple(int(x) for x in t.shape)} "
            f"bytes={int(t.data.nbytes):,}"
        )

    print()
    print("=" * 70)
    print(" ARCHITECTURAL CONSISTENCY")
    print("=" * 70)

    expected_layers = list(range(len(layers)))
    actual_layers = sorted(layers)

    print("Expected layer IDs :", expected_layers)
    print("Actual layer IDs   :", actual_layers)
    print("Layer sequence OK  :", expected_layers == actual_layers)

    complete = all(
        all(component in layers[layer] for component in expected)
        for layer in actual_layers
    )

    print("Layer schemas OK   :", complete)


if __name__ == "__main__":
    model = (
        Path.home()
        / "qwen2.5-coder-q8_0.gguf"
    )

    profile(model)
