import json
import math
import struct
from pathlib import Path
from collections import Counter, defaultdict

PATH = Path.home() / "qwen2.5-coder-q8_0.gguf"
OUT = Path("experiments/model_fractal/gguf_structure_v1.json")

TYPE_NAMES = {
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

    raise ValueError(
        f"Unsupported GGUF metadata type: {typ}"
    )


def align(offset, alignment):
    return (
        (offset + alignment - 1)
        // alignment
    ) * alignment


# ============================================================
# READ GGUF DIRECTORY
# ============================================================

with PATH.open("rb") as f:

    if f.read(4) != b"GGUF":
        raise SystemExit("Not a GGUF file")

    version = u32(f)
    tensor_count = u64(f)
    metadata_count = u64(f)

    alignment = 32

    for _ in range(metadata_count):

        key = read_string(f)
        typ = u32(f)

        if key == "general.alignment" and typ == 4:
            alignment = u32(f)
        else:
            skip_value(f, typ)

    tensors = []

    for _ in range(tensor_count):

        name = read_string(f)
        n_dims = u32(f)

        dims = tuple(
            u64(f)
            for _ in range(n_dims)
        )

        tensor_type = u32(f)
        offset = u64(f)

        tensors.append({
            "name": name,
            "dims": list(dims),
            "type": tensor_type,
            "type_name": TYPE_NAMES.get(
                tensor_type,
                f"TYPE_{tensor_type}"
            ),
            "offset": offset,
        })

    directory_end = f.tell()

data_start = align(
    directory_end,
    alignment
)

# ============================================================
# DERIVE EXACT TENSOR SPANS
# ============================================================

ordered = sorted(
    tensors,
    key=lambda x: x["offset"]
)

file_size = PATH.stat().st_size
payload_size = file_size - data_start

for i, tensor in enumerate(ordered):

    start = tensor["offset"]

    if i + 1 < len(ordered):
        end = ordered[i + 1]["offset"]
    else:
        end = payload_size

    tensor["file_start"] = data_start + start
    tensor["span"] = end - start

# ============================================================
# STRUCTURAL MODEL
# ============================================================

layers = defaultdict(dict)
global_tensors = []

for tensor in tensors:

    name = tensor["name"]

    if name.startswith("blk."):

        parts = name.split(".")

        layer = int(parts[1])
        component = ".".join(parts[2:])

        layers[layer][component] = {
            "name": name,
            "type": tensor["type_name"],
            "dims": tensor["dims"],
            "span": tensor["span"],
        }

    else:

        global_tensors.append({
            "name": name,
            "type": tensor["type_name"],
            "dims": tensor["dims"],
            "span": tensor["span"],
        })

# ============================================================
# NUMERIC LAYER ORDER
# ============================================================

layer_ids = sorted(layers)

components = sorted({
    component
    for layer in layers.values()
    for component in layer
})

# ============================================================
# STRUCTURAL FEATURE VECTOR
# ============================================================

layer_vectors = {}

for layer_id in layer_ids:

    layer = layers[layer_id]

    vector = []

    for component in components:

        tensor = layer.get(component)

        if tensor is None:

            vector.extend([
                0.0,  # presence
                0.0,  # type
                0.0,  # rank
                0.0,  # parameter count
                0.0,  # byte span
            ])

            continue

        type_code = {
            "F32": 1.0,
            "F16": 2.0,
            "Q8_0": 8.0,
        }.get(
            tensor["type"],
            float(tensor["type"]
                  if isinstance(tensor["type"], int)
                  else 0.0)
        )

        parameter_count = math.prod(
            tensor["dims"]
        )

        vector.extend([
            1.0,
            type_code,
            float(len(tensor["dims"])),
            float(parameter_count),
            float(tensor["span"]),
        ])

    layer_vectors[str(layer_id)] = vector

# ============================================================
# SUMMARY
# ============================================================

type_counts = Counter(
    tensor["type_name"]
    for tensor in tensors
)

layer_component_counts = {
    str(layer): len(layers[layer])
    for layer in layer_ids
}

structure = {
    "format": "OpenMind GGUF Structural Fingerprint V1",
    "source": str(PATH),
    "gguf": {
        "version": version,
        "tensor_count": tensor_count,
        "metadata_count": metadata_count,
        "alignment": alignment,
        "directory_end": directory_end,
        "tensor_data_start": data_start,
        "file_size": file_size,
    },
    "tensor_type_counts": dict(
        sorted(type_counts.items())
    ),
    "layer_count": len(layer_ids),
    "layer_ids": layer_ids,
    "components": components,
    "layer_component_counts": layer_component_counts,
    "global_tensors": global_tensors,
    "layers": {
        str(layer): layers[layer]
        for layer in layer_ids
    },
    "layer_vectors": layer_vectors,
}

OUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

OUT.write_text(
    json.dumps(
        structure,
        indent=2,
        sort_keys=True
    )
)

# ============================================================
# REPORT
# ============================================================

print("=" * 72)
print(" OPENMIND / GGUF STRUCTURAL FINGERPRINT V1")
print("=" * 72)

print()
print("Source:", PATH)
print("GGUF version:", version)
print("Tensor count:", tensor_count)
print("Layer count:", len(layer_ids))
print("Data start:", data_start)
print()

print("=== TYPE COUNTS ===")

for name, count in sorted(type_counts.items()):
    print(f"{name:<12} {count}")

print()
print("=== LAYER STRUCTURE ===")

for layer in layer_ids:
    print(
        f"L{layer:02d}: "
        f"{len(layers[layer])} components"
    )

print()
print("=== COMPONENT SCHEMA ===")

for component in components:
    types = sorted({
        layers[layer][component]["type"]
        for layer in layer_ids
        if component in layers[layer]
    })

    print(
        f"{component:<25} "
        f"{','.join(types)}"
    )

print()
print("=== GLOBAL TENSORS ===")

for tensor in global_tensors:
    print(
        f"{tensor['name']:<30} "
        f"{tensor['type']:<8} "
        f"dims={tuple(tensor['dims'])}"
    )

print()
print("=== LAYER ORDER CHECK ===")

print(
    "first:",
    layer_ids[0]
)

print(
    "last:",
    layer_ids[-1]
)

print(
    "contiguous:",
    layer_ids == list(range(len(layer_ids)))
)

print()
print("=== OUTPUT ===")
print(OUT)

print()
print("STRUCTURAL FINGERPRINT COMPLETE")
