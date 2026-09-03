import math
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
        * alignment
    )


# ------------------------------------------------------------
# GGUF DIRECTORY
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
# STREAMING BYTE STATISTICS
# ------------------------------------------------------------

def tensor_statistics(
    f,
    tensor,
    sample_limit=65536
):

    f.seek(tensor["file_start"])

    remaining = tensor["span"]

    # Deterministic sampling.
    # We inspect evenly distributed chunks instead
    # of loading the tensor.

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
                    i
                    * remaining
                    // count
                )
            )

            f.seek(pos)

            samples.append(
                f.read(chunk)
            )

        data = b"".join(samples)

    if not data:
        return {
            "mean": 0.0,
            "rms": 0.0,
            "abs_mean": 0.0,
            "variance": 0.0,
            "minimum": 0,
            "maximum": 0,
        }

    values = list(data)

    n = len(values)

    mean = (
        sum(values)
        / n
    )

    abs_mean = (
        sum(abs(x - 127.5) for x in values)
        / n
    )

    rms = math.sqrt(
        sum(
            (x - 127.5) ** 2
            for x in values
        )
        / n
    )

    variance = (
        sum(
            (x - mean) ** 2
            for x in values
        )
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
# COLLECT STATISTICS
# ------------------------------------------------------------

print("=" * 72)
print(" OPENMIND / QUANTITATIVE PARAMETER DIVERGENCE")
print("=" * 72)

print()
print(f"File:       {PATH}")
print(f"Layers:     {len(layers)}")
print("Mode:       deterministic streamed sampling")
print()

stats = defaultdict(dict)

with PATH.open("rb") as f:

    for layer in sorted(layers):

        print(
            f"Sampling layer {layer:02d}..."
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
# DISTANCE
# ------------------------------------------------------------

def distance(a, b):

    return math.sqrt(
        (a["mean"] - b["mean"]) ** 2
        + (a["rms"] - b["rms"]) ** 2
        + (a["abs_mean"] - b["abs_mean"]) ** 2
        + (a["variance"] - b["variance"]) ** 2
    )


print()
print("=" * 72)
print(" LAYER PARAMETER DIVERGENCE")
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

        d = distance(
            stats[a][component],
            stats[b][component]
        )

        distances.append(d)

    total = sum(distances)

    mean_distance = (
        total / len(distances)
        if distances
        else 0
    )

    layer_distances[(a, b)] = (
        mean_distance
    )

    print(
        f"L{a:02d} -> L{b:02d} | "
        f"mean_distance={mean_distance:.6f}"
    )


# ------------------------------------------------------------
# COMPONENT DIVERGENCE
# ------------------------------------------------------------

print()
print("=" * 72)
print(" COMPONENT DIVERGENCE")
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

        mean_value = (
            sum(values)
            / len(values)
        )

        component_scores[component] = (
            mean_value
        )

        print(
            f"{component:30s} | "
            f"mean_distance={mean_value:.6f}"
        )


# ------------------------------------------------------------
# MOST DIVERGENT TRANSITIONS
# ------------------------------------------------------------

print()
print("=" * 72)
print(" TRANSITION RANKING")
print("=" * 72)

ranked = sorted(
    layer_distances.items(),
    key=lambda x: x[1],
    reverse=True
)

for (a, b), value in ranked:

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

if layer_distances:

    values = list(
        layer_distances.values()
    )

    print(
        f"Minimum transition: "
        f"{min(values):.6f}"
    )

    print(
        f"Maximum transition: "
        f"{max(values):.6f}"
    )

    print(
        f"Mean transition:    "
        f"{sum(values)/len(values):.6f}"
    )

    max_pair = max(
        layer_distances,
        key=layer_distances.get
    )

    min_pair = min(
        layer_distances,
        key=layer_distances.get
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
    "Quantitative parameter divergence complete."
)
print(
    "No complete tensor payloads were loaded."
)
