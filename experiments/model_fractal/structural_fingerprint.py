import struct
import re
from pathlib import Path
from collections import defaultdict

PATH = Path.home() / "qwen2.5-coder-q8_0.gguf"

GGML_TYPE_NAMES = {
    0: "F32",
    1: "F16",
    2: "Q4_0",
    3: "Q4_1",
    6: "Q5_0",
    7: "Q5_1",
    8: "Q8_0",
    9: "Q8_1",
    10: "Q2_K",
    11: "Q3_K_S",
    12: "Q3_K_M",
    13: "Q3_K_L",
    14: "Q4_K_S",
    15: "Q4_K_M",
    16: "Q5_K_S",
    17: "Q5_K_M",
    18: "Q6_K",
    19: "IQ2_XXS",
    20: "IQ2_XS",
    21: "IQ3_XXS",
    22: "IQ1_S",
    23: "IQ4_NL",
    24: "IQ3_S",
    25: "IQ2_S",
    26: "IQ4_XS",
    27: "IQ1_M",
    28: "BF16",
    29: "Q4_0_4_4",
    30: "Q4_0_4_8",
    31: "Q4_0_8_8",
    32: "TQ1_0",
    33: "TQ2_0",
    34: "TQ2_1",
    35: "IQ4_NL_4_4",
    36: "IQ4_NL_4_8",
    37: "IQ4_NL_8_8",
}

def u32(f):
    return struct.unpack("<I", f.read(4))[0]

def u64(f):
    return struct.unpack("<Q", f.read(8))[0]

def read_string(f):
    n = u64(f)
    data = f.read(n)
    if len(data) != n:
        raise EOFError("Unexpected EOF")
    return data.decode("utf-8", errors="replace")

def skip_value(f, typ):
    sizes = {
        0: 1,
        1: 1,
        2: 2,
        3: 2,
        4: 4,
        5: 4,
        6: 4,
        7: 1,
        10: 8,
        11: 8,
        12: 8,
    }

    if typ in sizes:
        f.seek(sizes[typ], 1)
        return

    if typ == 8:
        n = u64(f)
        f.seek(n, 1)
        return

    if typ == 9:
        elem_type = u32(f)
        count = u64(f)
        for _ in range(count):
            skip_value(f, elem_type)
        return

    raise ValueError(f"Unsupported GGUF metadata type: {typ}")

def align(offset, alignment):
    return (offset + alignment - 1) // alignment * alignment


# ------------------------------------------------------------
# READ GGUF DIRECTORY
# ------------------------------------------------------------

with PATH.open("rb") as f:

    magic = f.read(4)
    if magic != b"GGUF":
        raise SystemExit("Not a GGUF file")

    version = u32(f)
    tensor_count = u64(f)
    metadata_count = u64(f)

    alignment = 32

    for _ in range(metadata_count):
        key = read_string(f)
        typ = u32(f)

        if key == "general.alignment":
            if typ == 4:
                alignment = u32(f)
            else:
                skip_value(f, typ)
        else:
            skip_value(f, typ)

    tensors = []

    for _ in range(tensor_count):

        name = read_string(f)
        n_dims = u32(f)

        dims = tuple(u64(f) for _ in range(n_dims))

        tensor_type = u32(f)
        offset = u64(f)

        tensors.append({
            "name": name,
            "dims": dims,
            "type": tensor_type,
            "type_name": GGML_TYPE_NAMES.get(
                tensor_type,
                f"TYPE_{tensor_type}"
            ),
            "offset": offset,
        })

    tensor_info_end = f.tell()
    tensor_data_start = align(tensor_info_end, alignment)


# ------------------------------------------------------------
# DERIVE TENSOR SPANS
# ------------------------------------------------------------

for i, tensor in enumerate(tensors):

    start = tensor["offset"]

    if i + 1 < len(tensors):
        end = tensors[i + 1]["offset"]
    else:
        end = PATH.stat().st_size - tensor_data_start

    tensor["relative_start"] = start
    tensor["relative_end"] = end
    tensor["span"] = end - start


# ------------------------------------------------------------
# MODEL FINGERPRINT
# ------------------------------------------------------------

print("=" * 72)
print(" OPENMIND / MODEL STRUCTURAL FINGERPRINT")
print("=" * 72)

print()
print(f"File:             {PATH}")
print(f"File size:        {PATH.stat().st_size:,} bytes")
print(f"GGUF version:     {version}")
print(f"Tensor count:     {tensor_count}")
print(f"Metadata count:   {metadata_count}")
print(f"Alignment:        {alignment}")
print(f"Tensor data:      {tensor_data_start:,}")

print()
print("=" * 72)
print(" TENSOR TYPES")
print("=" * 72)

type_counts = defaultdict(int)
type_bytes = defaultdict(int)

for t in tensors:
    type_counts[t["type_name"]] += 1
    type_bytes[t["type_name"]] += t["span"]

for name in sorted(type_counts):
    print(
        f"{name:12s} | "
        f"tensors={type_counts[name]:4d} | "
        f"bytes={type_bytes[name]:12,d}"
    )


# ------------------------------------------------------------
# CLASSIFY TENSORS
# ------------------------------------------------------------

layer_data = defaultdict(list)

for t in tensors:

    name = t["name"]

    match = re.match(r"blk\.(\d+)\.(.+)", name)

    if match:
        layer = int(match.group(1))
        component = match.group(2)

        t["layer"] = layer
        t["component"] = component

        layer_data[layer].append(t)

    elif name == "token_embd.weight":
        t["layer"] = -1
        t["component"] = "embedding"

    elif name == "output.weight":
        t["layer"] = 28
        t["component"] = "output"

    elif name == "output_norm.weight":
        t["layer"] = 28
        t["component"] = "output_norm"


# ------------------------------------------------------------
# LAYER FINGERPRINTS
# ------------------------------------------------------------

print()
print("=" * 72)
print(" LAYER FINGERPRINTS")
print("=" * 72)

layer_fingerprints = {}

for layer in sorted(layer_data):

    items = layer_data[layer]

    total_bytes = sum(t["span"] for t in items)

    by_type = defaultdict(int)
    by_component = defaultdict(int)

    for t in items:
        by_type[t["type_name"]] += t["span"]

        component = t["component"]

        if component.startswith("attn_"):
            group = "attention"
        elif component.startswith("ffn_"):
            group = "ffn"
        else:
            group = "norm_bias"

        by_component[group] += t["span"]

    layer_fingerprints[layer] = {
        "total": total_bytes,
        "attention": by_component["attention"],
        "ffn": by_component["ffn"],
        "norm_bias": by_component["norm_bias"],
        "types": dict(by_type),
    }

    print(
        f"L{layer:02d} | "
        f"total={total_bytes:12,d} | "
        f"attention={by_component['attention']:12,d} | "
        f"ffn={by_component['ffn']:12,d} | "
        f"norm/bias={by_component['norm_bias']:10,d}"
    )


# ------------------------------------------------------------
# STRUCTURAL DISTANCE
# ------------------------------------------------------------

print()
print("=" * 72)
print(" LAYER-TO-LAYER STRUCTURAL DISTANCE")
print("=" * 72)

layers = sorted(layer_fingerprints)

for a, b in zip(layers, layers[1:]):

    x = layer_fingerprints[a]
    y = layer_fingerprints[b]

    distance = (
        abs(x["total"] - y["total"])
        + abs(x["attention"] - y["attention"])
        + abs(x["ffn"] - y["ffn"])
        + abs(x["norm_bias"] - y["norm_bias"])
    )

    print(
        f"L{a:02d} -> L{b:02d} | "
        f"distance={distance:,}"
    )


# ------------------------------------------------------------
# COMPONENT SIGNATURE
# ------------------------------------------------------------

print()
print("=" * 72)
print(" CANONICAL COMPONENT SIGNATURE")
print("=" * 72)

for layer in layers[:1]:

    for t in sorted(
        layer_data[layer],
        key=lambda x: x["name"]
    ):
        print(
            f"{t['component']:30s} "
            f"shape={str(t['dims']):22s} "
            f"type={t['type_name']:8s} "
            f"bytes={t['span']:,}"
        )


# ------------------------------------------------------------
# GLOBAL SUMMARY
# ------------------------------------------------------------

print()
print("=" * 72)
print(" GLOBAL SUMMARY")
print("=" * 72)

transformer_bytes = sum(
    fp["total"] for fp in layer_fingerprints.values()
)

print(f"Transformer bytes:     {transformer_bytes:,}")
print(f"Transformer layers:    {len(layer_fingerprints)}")

if layers:
    totals = [layer_fingerprints[x]["total"] for x in layers]

    print(f"Smallest layer:        {min(totals):,}")
    print(f"Largest layer:         {max(totals):,}")
    print(
        f"Mean layer size:       "
        f"{sum(totals) / len(totals):,.2f}"
    )

print()
print("Structural fingerprint complete.")
print("No tensor payloads were loaded.")
