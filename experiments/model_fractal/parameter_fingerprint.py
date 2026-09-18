import hashlib
import re
import struct
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

        if key == "general.alignment" and typ == 4:
            alignment = u32(f)
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

    tensor_data_start = align(
        tensor_info_end,
        alignment
    )


# ------------------------------------------------------------
# SORT + DERIVE EXACT TENSOR SPANS
# ------------------------------------------------------------

tensors.sort(key=lambda x: x["offset"])

file_size = PATH.stat().st_size
payload_size = file_size - tensor_data_start

for i, tensor in enumerate(tensors):

    start = tensor["offset"]

    if start < 0 or start >= payload_size:
        raise ValueError(
            f"Invalid tensor offset: {start}"
        )

    if i + 1 < len(tensors):
        end = tensors[i + 1]["offset"]
    else:
        end = payload_size

    if end < start:
        raise ValueError(
            f"Invalid tensor span: {tensor['name']}"
        )

    tensor["relative_start"] = start
    tensor["relative_end"] = end
    tensor["span"] = end - start


# ------------------------------------------------------------
# ASSIGN ABSOLUTE FILE OFFSETS
# ------------------------------------------------------------

for tensor in tensors:
    tensor["file_start"] = (
        tensor_data_start +
        tensor["relative_start"]
    )

    tensor["file_end"] = (
        tensor_data_start +
        tensor["relative_end"]
    )


# ------------------------------------------------------------
# CLASSIFY TRANSFORMER TENSORS
# ------------------------------------------------------------

layers = defaultdict(dict)

for tensor in tensors:

    name = tensor["name"]

    match = re.match(
        r"blk\.(\d+)\.(.+)",
        name
    )

    if not match:
        continue

    layer = int(match.group(1))
    component = match.group(2)

    tensor["layer"] = layer
    tensor["component"] = component

    layers[layer][component] = tensor


# ------------------------------------------------------------
# STREAMED HASH
# ------------------------------------------------------------

def sha256_tensor(f, tensor, chunk_size=1024 * 1024):

    f.seek(tensor["file_start"])

    remaining = tensor["span"]

    h = hashlib.sha256()

    while remaining:

        chunk = f.read(
            min(chunk_size, remaining)
        )

        if not chunk:
            raise EOFError(
                f"Unexpected EOF reading "
                f"{tensor['name']}"
            )

        h.update(chunk)

        remaining -= len(chunk)

    return h.hexdigest()


# ------------------------------------------------------------
# PARAMETER FINGERPRINT
# ------------------------------------------------------------

print("=" * 72)
print(" OPENMIND / PARAMETER FINGERPRINT")
print("=" * 72)

print()
print(f"File:          {PATH}")
print(f"File size:     {file_size:,} bytes")
print(f"GGUF version:  {version}")
print(f"Tensors:       {tensor_count}")
print(f"Layers:        {len(layers)}")
print(f"Data start:    {tensor_data_start:,}")
print()

# ------------------------------------------------------------
# HASH EVERY TRANSFORMER TENSOR
# ------------------------------------------------------------

hashes = defaultdict(dict)

with PATH.open("rb") as f:

    for layer in sorted(layers):

        print(f"Hashing layer {layer:02d}...")

        for component in sorted(layers[layer]):

            tensor = layers[layer][component]

            digest = sha256_tensor(
                f,
                tensor
            )

            hashes[layer][component] = digest


# ------------------------------------------------------------
# COMPONENT DIVERGENCE
# ------------------------------------------------------------

print()
print("=" * 72)
print(" PARAMETER DIVERGENCE")
print("=" * 72)

components = sorted(
    set(
        component
        for layer in hashes.values()
        for component in layer
    )
)

for component in components:

    unique = len({
        hashes[layer][component]
        for layer in hashes
        if component in hashes[layer]
    })

    total = len([
        layer
        for layer in hashes
        if component in hashes[layer]
    ])

    identical = unique == 1

    print(
        f"{component:30s} | "
        f"layers={total:2d} | "
        f"unique_hashes={unique:2d} | "
        f"identical={identical}"
    )


# ------------------------------------------------------------
# LAYER PARAMETER FINGERPRINT
# ------------------------------------------------------------

print()
print("=" * 72)
print(" LAYER PARAMETER FINGERPRINTS")
print("=" * 72)

layer_hashes = {}

for layer in sorted(hashes):

    h = hashlib.sha256()

    for component in sorted(hashes[layer]):

        h.update(
            component.encode("utf-8")
        )

        h.update(
            hashes[layer][component].encode("ascii")
        )

    layer_hashes[layer] = h.hexdigest()

    print(
        f"L{layer:02d} | "
        f"{layer_hashes[layer]}"
    )


# ------------------------------------------------------------
# LAYER HASH DIVERGENCE
# ------------------------------------------------------------

print()
print("=" * 72)
print(" LAYER HASH DIVERGENCE")
print("=" * 72)

layers_sorted = sorted(layer_hashes)

for a, b in zip(
    layers_sorted,
    layers_sorted[1:]
):

    identical = (
        layer_hashes[a] ==
        layer_hashes[b]
    )

    print(
        f"L{a:02d} -> L{b:02d} | "
        f"identical={identical}"
    )


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

unique_layer_hashes = len(
    set(layer_hashes.values())
)

print()
print("=" * 72)
print(" SUMMARY")
print("=" * 72)

print(
    f"Structural layers:        {len(layers)}"
)

print(
    f"Unique layer fingerprints:{unique_layer_hashes}"
)

print(
    f"All layers parameter-identical: "
    f"{unique_layer_hashes == 1}"
)

print()
print("Parameter fingerprint complete.")
print("Tensor payloads were streamed, not loaded into RAM.")
