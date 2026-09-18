import math
import re
import struct
from pathlib import Path
from collections import defaultdict

PATH = Path.home() / "qwen2.5-coder-q8_0.gguf"

GGML_TYPE_NAMES = {
    0: "F32",
    8: "Q8_0",
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
    return ((offset + alignment - 1) // alignment) * alignment


# ------------------------------------------------------------
# READ GGUF DIRECTORY
# ------------------------------------------------------------

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

    tensors.sort(
        key=lambda x: x["offset"]
    )

    payload_size = (
        PATH.stat().st_size
        - tensor_data_start
    )

    for i, tensor in enumerate(tensors):

        start = tensor["offset"]

        if i + 1 < len(tensors):
            end = tensors[i + 1]["offset"]
        else:
            end = payload_size

        tensor["file_start"] = (
            tensor_data_start + start
        )

        tensor["span"] = end - start


# ------------------------------------------------------------
# FIND TRANSFORMER TENSORS
# ------------------------------------------------------------

layers = defaultdict(dict)

for tensor in tensors:

    match = re.match(
        r"blk\.(\d+)\.(.+)",
        tensor["name"]
    )

    if not match:
        continue

    layer = int(match.group(1))
    component = match.group(2)

    tensor["layer"] = layer
    tensor["component"] = component

    layers[layer][component] = tensor


# ------------------------------------------------------------
# STATISTICS
# ------------------------------------------------------------

def summarize(values):

    if not values:
        return {
            "mean": 0.0,
            "rms": 0.0,
            "abs_mean": 0.0,
            "variance": 0.0,
            "minimum": 0.0,
            "maximum": 0.0,
        }

    n = len(values)

    mean = sum(values) / n

    variance = sum(
        (x - mean) ** 2
        for x in values
    ) / n

    rms = math.sqrt(
        sum(x * x for x in values) / n
    )

    abs_mean = (
        sum(abs(x) for x in values)
        / n
    )

    return {
        "mean": mean,
        "rms": rms,
        "abs_mean": abs_mean,
        "variance": variance,
        "minimum": min(values),
        "maximum": max(values),
    }


# ------------------------------------------------------------
# Q8_0 DECODER
#
# Q8_0 block:
#   fp16 scale
#   32 int8 quantized values
#
# 34 bytes / block
# ------------------------------------------------------------

def decode_q8_0(data):

    values = []
    scales = []

    block_size = 34

    usable = (
        len(data) // block_size
    ) * block_size

    for pos in range(
        0,
        usable,
        block_size
    ):

        block = data[
            pos:pos + block_size
        ]

        scale = struct.unpack(
            "<e",
            block[:2]
        )[0]

        q = struct.unpack(
            "<32b",
            block[2:]
        )

        scales.append(scale)

        values.extend(
            scale * x
            for x in q
        )

    return values, scales


# ------------------------------------------------------------
# F32 DECODER
# ------------------------------------------------------------

def decode_f32(data):

    usable = (
        len(data) // 4
    ) * 4

    count = usable // 4

    return list(
        struct.unpack(
            f"<{count}f",
            data[:usable]
        )
    )


# ------------------------------------------------------------
# STREAM TENSOR
# ------------------------------------------------------------

def tensor_statistics(
    f,
    tensor,
    sample_limit=65536
):

    f.seek(tensor["file_start"])

    remaining = tensor["span"]

    if remaining <= sample_limit:

        data = f.read(remaining)

    else:

        chunk = 4096

        count = max(
            1,
            sample_limit // chunk
        )

        samples = []

        for i in range(count):

            pos = (
                tensor["file_start"]
                + (
                    i * remaining
                    // count
                )
            )

            f.seek(pos)

            samples.append(
                f.read(chunk)
            )

        data = b"".join(samples)

    typ = tensor["type_name"]

    if typ == "Q8_0":

        values, scales = decode_q8_0(
            data
        )

        result = summarize(values)

        scale_stats = summarize(
            scales
        )

        result["scale_mean"] = (
            scale_stats["mean"]
        )

        result["scale_rms"] = (
            scale_stats["rms"]
        )

        result["scale_variance"] = (
            scale_stats["variance"]
        )

        return result

    if typ == "F32":

        values = decode_f32(data)

        result = summarize(values)

        result["scale_mean"] = 0.0
        result["scale_rms"] = 0.0
        result["scale_variance"] = 0.0

        return result

    raise ValueError(
        f"Unsupported tensor type: {typ}"
    )


# ------------------------------------------------------------
# DISTANCE
# ------------------------------------------------------------

def distance(a, b):

    return math.sqrt(
        (a["mean"] - b["mean"]) ** 2
        +
        (a["rms"] - b["rms"]) ** 2
        +
        (a["abs_mean"] - b["abs_mean"]) ** 2
        +
        (a["variance"] - b["variance"]) ** 2
        +
        (a["scale_mean"] - b["scale_mean"]) ** 2
        +
        (a["scale_rms"] - b["scale_rms"]) ** 2
    )


# ------------------------------------------------------------
# RUN
# ------------------------------------------------------------

print("=" * 72)
print(" OPENMIND / Q8_0-AWARE PARAMETER DIVERGENCE")
print("=" * 72)

print()
print(f"File:       {PATH}")
print(f"Layers:     {len(layers)}")
print("Mode:       decoded Q8_0 / F32 statistics")
print()

stats = defaultdict(dict)

with PATH.open("rb") as f:

    for layer in sorted(layers):

        print(
            f"Analyzing layer {layer:02d}..."
        )

        for component in sorted(
            layers[layer]
        ):

            tensor = layers[layer][component]

            stats[layer][component] = (
                tensor_statistics(
                    f,
                    tensor
                )
            )


# ------------------------------------------------------------
# LAYER DISTANCE
# ------------------------------------------------------------

print()
print("=" * 72)
print(" DECODED LAYER DIVERGENCE")
print("=" * 72)

layers_sorted = sorted(stats)

layer_distances = {}

for a, b in zip(
    layers_sorted,
    layers_sorted[1:]
):

    distances = []

    for component in stats[a]:

        if component not in stats[b]:
            continue

        distances.append(
            distance(
                stats[a][component],
                stats[b][component]
            )
        )

    mean_distance = (
        sum(distances)
        / len(distances)
        if distances
        else 0.0
    )

    layer_distances[(a, b)] = (
        mean_distance
    )

    print(
        f"L{a:02d} -> L{b:02d} | "
        f"distance={mean_distance:.6f}"
    )


# ------------------------------------------------------------
# COMPONENT RANKING
# ------------------------------------------------------------

print()
print("=" * 72)
print(" DECODED COMPONENT DIVERGENCE")
print("=" * 72)

component_scores = {}

components = sorted(
    set(
        component
        for layer in stats.values()
        for component in layer
    )
)

for component in components:

    values = []

    for a, b in zip(
        layers_sorted,
        layers_sorted[1:]
    ):

        if (
            component in stats[a]
            and component in stats[b]
        ):

            values.append(
                distance(
                    stats[a][component],
                    stats[b][component]
                )
            )

    if values:

        score = (
            sum(values)
            / len(values)
        )

        component_scores[
            component
        ] = score

        print(
            f"{component:30s} | "
            f"{score:.6f}"
        )


# ------------------------------------------------------------
# RANKING
# ------------------------------------------------------------

print()
print("=" * 72)
print(" TRANSITION RANKING")
print("=" * 72)

for (a, b), value in sorted(
    layer_distances.items(),
    key=lambda x: x[1],
    reverse=True
):

    print(
        f"L{a:02d} -> L{b:02d} | "
        f"{value:.6f}"
    )


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

print()
print("=" * 72)
print(" SUMMARY")
print("=" * 72)

values = list(
    layer_distances.values()
)

if values:

    maximum = max(values)
    minimum = min(values)
    mean = sum(values) / len(values)

    max_pair = max(
        layer_distances,
        key=layer_distances.get
    )

    min_pair = min(
        layer_distances,
        key=layer_distances.get
    )

    print(
        f"Minimum transition: "
        f"{minimum:.6f}"
    )

    print(
        f"Maximum transition: "
        f"{maximum:.6f}"
    )

    print(
        f"Mean transition:    "
        f"{mean:.6f}"
    )

    print(
        f"Maximum divergence: "
        f"L{max_pair[0]:02d} -> "
        f"L{max_pair[1]:02d}"
    )

    print(
        f"Minimum divergence: "
        f"L{min_pair[0]:02d} -> "
        f"L{min_pair[1]:02d}"
    )

print()
print(
    "Q8_0-aware parameter divergence complete."
)
print(
    "Tensor payloads were streamed and sampled."
)
