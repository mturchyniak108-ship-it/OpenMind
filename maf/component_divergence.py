import re
from pathlib import Path

import numpy as np

from .gguf_reader import load_model
from .q8_decode import decode_tensor as decode_q8_tensor
from .divergence import tensor_divergence


Q8_0 = 8
F32 = 0

LAYER_PATTERN = re.compile(r"blk\.(\d+)\.(.+)")


def decode_tensor(tensor):
    tensor_type = int(tensor.tensor_type)

    if tensor_type == F32:
        return np.asarray(
            tensor.data,
            dtype=np.float32,
        ).reshape(
            tuple(int(x) for x in tensor.shape)
        )

    if tensor_type == Q8_0:
        return decode_q8_tensor(tensor)

    raise ValueError(
        f"Unsupported tensor type {tensor_type} "
        f"for {tensor.name}"
    )


def build_layers(reader):
    layers = {}

    for tensor in reader.tensors:
        match = LAYER_PATTERN.match(tensor.name)

        if not match:
            continue

        layer_id = int(match.group(1))
        component = match.group(2)

        layers.setdefault(layer_id, {})[component] = tensor

    return layers


def profile(path):
    reader = load_model(path)
    layers = build_layers(reader)

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

    print("=" * 78)
    print(" MAF / COMPONENT NUMERICAL DIVERGENCE")
    print("=" * 78)
    print("Model:", path)
    print("Layers:", len(decoded))
    print("Components:", len(components))
    print()

    records = []

    for layer_id in range(1, len(decoded)):
        previous = decoded[layer_id - 1]
        current = decoded[layer_id]

        print("-" * 78)
        print(
            f"TRANSITION {layer_id - 1:02d} -> {layer_id:02d}"
        )
        print("-" * 78)

        for component in components:
            result = tensor_divergence(
                previous[component],
                current[component],
            )

            record = {
                "from": layer_id - 1,
                "to": layer_id,
                "component": component,
                **result,
            }

            records.append(record)

            print(
                f"{component:22s} "
                f"L2={result['relative_l2']:.6f} "
                f"COS={result['cosine']:.6f} "
                f"STDΔ={result['std_delta']:.6e} "
                f"ZEROΔ={result['zero_delta']:.6e}"
            )

    print()
    print("=" * 78)
    print(" TOP COMPONENT DIVERGENCES")
    print("=" * 78)

    top_l2 = sorted(
        records,
        key=lambda x: x["relative_l2"],
        reverse=True,
    )[:10]

    top_cos = sorted(
        records,
        key=lambda x: x["cosine"],
    )[:10]

    print()
    print("TOP 10 RELATIVE L2")
    print("-" * 78)

    for rank, record in enumerate(top_l2, 1):
        print(
            f"{rank:02d}. "
            f"{record['from']:02d}->{record['to']:02d} "
            f"{record['component']:22s} "
            f"L2={record['relative_l2']:.6f} "
            f"COS={record['cosine']:.6f}"
        )

    print()
    print("TOP 10 LOWEST COSINE")
    print("-" * 78)

    for rank, record in enumerate(top_cos, 1):
        print(
            f"{rank:02d}. "
            f"{record['from']:02d}->{record['to']:02d} "
            f"{record['component']:22s} "
            f"COS={record['cosine']:.6f} "
            f"L2={record['relative_l2']:.6f}"
        )

    print()
    print("=" * 78)
    print(" COMPONENT CROSS-LAYER AGGREGATION")
    print("=" * 78)

    component_summary = []

    for component in components:
        subset = [
            record
            for record in records
            if record["component"] == component
        ]

        mean_l2 = float(np.mean([
            r["relative_l2"] for r in subset
        ]))

        max_record = max(
            subset,
            key=lambda r: r["relative_l2"],
        )

        mean_cosine = float(np.mean([
            r["cosine"] for r in subset
        ]))

        min_record = min(
            subset,
            key=lambda r: r["cosine"],
        )

        high_l2_count = sum(
            r["relative_l2"] >= 2.0
            for r in subset
        )

        negative_cos_count = sum(
            r["cosine"] < 0.0
            for r in subset
        )

        component_summary.append({
            "component": component,
            "mean_l2": mean_l2,
            "max_l2": max_record["relative_l2"],
            "max_transition": (
                max_record["from"],
                max_record["to"],
            ),
            "mean_cosine": mean_cosine,
            "min_cosine": min_record["cosine"],
            "min_transition": (
                min_record["from"],
                min_record["to"],
            ),
            "high_l2_count": high_l2_count,
            "negative_cos_count": negative_cos_count,
        })

    ranked = sorted(
        component_summary,
        key=lambda x: (
            x["mean_l2"],
            x["max_l2"],
        ),
        reverse=True,
    )

    print()
    print(
        f"{'COMPONENT':22s} "
        f"{'MEAN L2':>10s} "
        f"{'MAX L2':>10s} "
        f"{'MEAN COS':>10s} "
        f"{'MIN COS':>10s} "
        f"{'HOT':>5s} "
        f"{'NEG':>5s}"
    )
    print("-" * 78)

    for record in ranked:
        print(
            f"{record['component']:22s} "
            f"{record['mean_l2']:10.6f} "
            f"{record['max_l2']:10.6f} "
            f"{record['mean_cosine']:10.6f} "
            f"{record['min_cosine']:10.6f} "
            f"{record['high_l2_count']:5d} "
            f"{record['negative_cos_count']:5d}"
        )

    print()
    print("TOP COMPONENT BY MEAN L2")
    print("-" * 78)

    for rank, record in enumerate(ranked[:5], 1):
        frm, to = record["max_transition"]
        print(
            f"{rank:02d}. "
            f"{record['component']:22s} "
            f"MEAN_L2={record['mean_l2']:.6f} "
            f"MAX={record['max_l2']:.6f} "
            f"at {frm:02d}->{to:02d}"
        )

    print()
    print("MOST NEGATIVE COSINE BY COMPONENT")
    print("-" * 78)

    by_cosine = sorted(
        component_summary,
        key=lambda x: x["min_cosine"],
    )

    for rank, record in enumerate(by_cosine[:5], 1):
        frm, to = record["min_transition"]
        print(
            f"{rank:02d}. "
            f"{record['component']:22s} "
            f"MIN_COS={record['min_cosine']:.6f} "
            f"at {frm:02d}->{to:02d}"
        )

    print()
    print("HOTSPOT DEFINITION")
    print("-" * 78)
    print("HOT = transition with relative L2 >= 2.0")
    print("NEG = transition with cosine < 0.0")

    print()
    print("=" * 78)
    print(" MAF / COMPONENT NUMERICAL DIVERGENCE COMPLETE")
    print("=" * 78)


if __name__ == "__main__":
    model = (
        Path.home()
        / "qwen2.5-coder-q8_0.gguf"
    )

    profile(model)
