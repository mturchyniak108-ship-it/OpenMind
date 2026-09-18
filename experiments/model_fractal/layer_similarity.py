import math
import re
import struct
from pathlib import Path
from collections import defaultdict

PATH = Path.home() / "qwen2.5-coder-q8_0.gguf"

Q8_BLOCK = 34
SAMPLE_BYTES = 65536


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
# ORGANIZE LAYERS
# ------------------------------------------------------------

layers = defaultdict(list)

for tensor in tensors:

    match = re.match(
        r"blk\.(\d+)\.(.+)",
        tensor["name"]
    )

    if not match:
        continue

    layer = int(match.group(1))
    component = match.group(2)

    tensor["component"] = component

    layers[layer].append(tensor)


# ------------------------------------------------------------
# Q8 STATISTICS
# ------------------------------------------------------------

def q8_statistics(f, tensor):

    start = tensor["file_start"]
    span = tensor["span"]

    total_blocks = span // Q8_BLOCK

    if total_blocks == 0:
        return None

    target_blocks = max(
        1,
        min(
            total_blocks,
            SAMPLE_BYTES // Q8_BLOCK
        )
    )

    values = []
    scales = []

    for i in range(target_blocks):

        block_index = (
            i * total_blocks
            // target_blocks
        )

        pos = (
            start
            + block_index * Q8_BLOCK
        )

        f.seek(pos)

        block = f.read(Q8_BLOCK)

        if len(block) != Q8_BLOCK:
            continue

        scale = struct.unpack(
            "<e",
            block[:2]
        )[0]

        if not math.isfinite(scale):
            continue

        q = struct.unpack(
            "<32b",
            block[2:]
        )

        for x in q:

            value = scale * x

            if math.isfinite(value):
                values.append(value)

        scales.append(scale)

    if not values:
        return None

    n = len(values)

    mean = sum(values) / n

    variance = sum(
        (x - mean) ** 2
        for x in values
    ) / n

    rms = math.sqrt(
        sum(x * x for x in values)
        / n
    )

    abs_mean = (
        sum(abs(x) for x in values)
        / n
    )

    scale_mean = (
        sum(scales)
        / len(scales)
    )

    scale_rms = math.sqrt(
        sum(x * x for x in scales)
        / len(scales)
    )

    return {
        "mean": mean,
        "variance": variance,
        "rms": rms,
        "abs_mean": abs_mean,
        "scale_mean": scale_mean,
        "scale_rms": scale_rms,
    }


# ------------------------------------------------------------
# BUILD LAYER SIGNATURE
# ------------------------------------------------------------

print("=" * 72)
print(" OPENMIND / FULL LAYER STRUCTURAL SIMILARITY")
print("=" * 72)

print()
print(f"File:       {PATH}")
print(f"GGUF:       v{version}")
print(f"Tensors:    {tensor_count}")
print(f"Layers:     {len(layers)}")
print("Mode:       deterministic Q8_0 structural signatures")
print()

layer_stats = {}

with PATH.open("rb") as f:

    for layer in sorted(layers):

        print(
            f"Building signature L{layer:02d}..."
        )

        component_stats = {}

        for tensor in layers[layer]:

            if tensor["type"] != 8:
                continue

            result = q8_statistics(
                f,
                tensor
            )

            if result is not None:
                component_stats[
                    tensor["component"]
                ] = result

        layer_stats[layer] = component_stats


# ------------------------------------------------------------
# NORMALIZED FEATURE VECTOR
# ------------------------------------------------------------

COMPONENTS = sorted(
    set(
        component
        for layer in layer_stats.values()
        for component in layer
    )
)

FIELDS = [
    "mean",
    "variance",
    "rms",
    "abs_mean",
    "scale_mean",
    "scale_rms",
]


def feature_vector(layer):

    vector = []

    for component in COMPONENTS:

        stats = layer_stats[layer].get(
            component
        )

        if stats is None:
            vector.extend(
                [0.0] * len(FIELDS)
            )
            continue

        vector.extend(
            stats[field]
            for field in FIELDS
        )

    return vector


vectors = {
    layer: feature_vector(layer)
    for layer in layer_stats
}


# ------------------------------------------------------------
# NORMALIZE FEATURES ACROSS DEPTH
# ------------------------------------------------------------

dimension_count = len(
    next(iter(vectors.values()))
)

means = []

stds = []

for index in range(dimension_count):

    values = [
        vector[index]
        for vector in vectors.values()
    ]

    mean = sum(values) / len(values)

    variance = sum(
        (x - mean) ** 2
        for x in values
    ) / len(values)

    std = math.sqrt(variance)

    means.append(mean)
    stds.append(std)


normalized = {}

for layer, vector in vectors.items():

    normalized[layer] = [
        (
            vector[i] - means[i]
        )
        / stds[i]
        if stds[i] > 1e-12
        else 0.0
        for i in range(dimension_count)
    ]


# ------------------------------------------------------------
# DISTANCES
# ------------------------------------------------------------

def euclidean(a, b):

    return math.sqrt(
        sum(
            (x - y) ** 2
            for x, y in zip(a, b)
        )
    )


def cosine(a, b):

    dot = sum(
        x * y
        for x, y in zip(a, b)
    )

    na = math.sqrt(
        sum(x * x for x in a)
    )

    nb = math.sqrt(
        sum(y * y for y in b)
    )

    if na == 0 or nb == 0:
        return 0.0

    return dot / (na * nb)


# ------------------------------------------------------------
# FULL PAIRWISE MATRIX
# ------------------------------------------------------------

layers_sorted = sorted(
    normalized
)

distance_matrix = {}

for a in layers_sorted:

    distance_matrix[a] = {}

    for b in layers_sorted:

        distance_matrix[a][b] = (
            euclidean(
                normalized[a],
                normalized[b]
            )
        )


# ------------------------------------------------------------
# NEAREST NON-ADJACENT LAYERS
# ------------------------------------------------------------

print()
print("=" * 72)
print(" NEAREST NON-ADJACENT LAYERS")
print("=" * 72)

pairs = []

for i, a in enumerate(layers_sorted):

    for b in layers_sorted[i + 1:]:

        if abs(a - b) <= 1:
            continue

        pairs.append(
            (
                distance_matrix[a][b],
                a,
                b,
            )
        )

for distance, a, b in sorted(pairs)[:20]:

    print(
        f"L{a:02d} <-> L{b:02d} | "
        f"distance={distance:.6f} | "
        f"depth_gap={abs(a-b)}"
    )


# ------------------------------------------------------------
# MOST DISTANT PAIRS
# ------------------------------------------------------------

print()
print("=" * 72)
print(" MOST DISTANT LAYER PAIRS")
print("=" * 72)

for distance, a, b in sorted(
    pairs,
    reverse=True
)[:20]:

    print(
        f"L{a:02d} <-> L{b:02d} | "
        f"distance={distance:.6f} | "
        f"depth_gap={abs(a-b)}"
    )


# ------------------------------------------------------------
# LAYER NEIGHBOR MAP
# ------------------------------------------------------------

print()
print("=" * 72)
print(" STRUCTURAL NEIGHBORS")
print("=" * 72)

for layer in layers_sorted:

    candidates = []

    for other in layers_sorted:

        if other == layer:
            continue

        candidates.append(
            (
                distance_matrix[layer][other],
                other,
            )
        )

    nearest = sorted(candidates)[:3]

    text = ", ".join(
        f"L{x:02d}:{d:.3f}"
        for d, x in nearest
    )

    print(
        f"L{layer:02d} -> {text}"
    )


# ------------------------------------------------------------
# RECURRENCE DETECTION
# ------------------------------------------------------------

print()
print("=" * 72)
print(" NON-LOCAL RECURRENCE CANDIDATES")
print("=" * 72)

nonlocal_pairs = [
    item
    for item in pairs
    if item[2] - item[1] >= 4
]

for distance, a, b in sorted(
    nonlocal_pairs
)[:20]:

    print(
        f"L{a:02d} <-> L{b:02d} | "
        f"distance={distance:.6f} | "
        f"gap={b-a}"
    )


# ------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------

print()
print("=" * 72)
print(" SUMMARY")
print("=" * 72)

print(
    f"Feature dimensions: "
    f"{dimension_count}"
)

print(
    f"Layer count: "
    f"{len(layers_sorted)}"
)

print(
    f"Pairwise comparisons: "
    f"{len(layers_sorted) * (len(layers_sorted)-1) // 2}"
)

if pairs:

    nearest = min(
        pairs,
        key=lambda x: x[0]
    )

    farthest = max(
        pairs,
        key=lambda x: x[0]
    )

    print(
        f"Nearest non-adjacent: "
        f"L{nearest[1]:02d} <-> "
        f"L{nearest[2]:02d} "
        f"({nearest[0]:.6f})"
    )

    print(
        f"Farthest pair: "
        f"L{farthest[1]:02d} <-> "
        f"L{farthest[2]:02d} "
        f"({farthest[0]:.6f})"
    )

print()
print(
    "Full structural similarity analysis complete."
)
print(
    "No complete tensor payloads were loaded."
)
