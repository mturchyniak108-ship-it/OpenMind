import math
import re
import struct
from pathlib import Path
from collections import defaultdict

PATH = Path.home() / "qwen2.5-coder-q8_0.gguf"

TYPE_NAMES = {
    0: "F32",
    8: "Q8_0",
}


# ============================================================
# BASIC GGUF READERS
# ============================================================

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
            "dims": dims,
            "type": tensor_type,
            "type_name": TYPE_NAMES.get(
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


# ============================================================
# FIND TRANSFORMER LAYERS
# ============================================================

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


# ============================================================
# STATISTICS
# ============================================================

def summarize(values):

    values = [
        float(x)
        for x in values
        if math.isfinite(x)
    ]

    if not values:
        return {
            "mean": 0.0,
            "std": 0.0,
            "rms": 0.0,
            "abs_mean": 0.0,
            "minimum": 0.0,
            "maximum": 0.0,
            "count": 0,
        }

    n = len(values)

    mean = sum(values) / n

    variance = (
        sum(
            (x - mean) ** 2
            for x in values
        )
        / n
    )

    std = math.sqrt(
        max(variance, 0.0)
    )

    rms = math.sqrt(
        sum(
            x * x
            for x in values
        )
        / n
    )

    abs_mean = (
        sum(abs(x) for x in values)
        / n
    )

    return {
        "mean": mean,
        "std": std,
        "rms": rms,
        "abs_mean": abs_mean,
        "minimum": min(values),
        "maximum": max(values),
        "count": n,
    }


# ============================================================
# Q8_0 DECODER
#
# Q8_0:
#   2 bytes FP16 scale
#   32 signed int8 values
#   34 bytes/block
# ============================================================

def decode_q8_sample(data):

    BLOCK = 34

    usable = (
        len(data) // BLOCK
    ) * BLOCK

    values = []
    scales = []

    for pos in range(
        0,
        usable,
        BLOCK
    ):

        block = data[
            pos:pos + BLOCK
        ]

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

        scales.append(scale)

        for x in q:

            value = scale * x

            if math.isfinite(value):
                values.append(value)

    return values, scales


# ============================================================
# F32 DECODER
# ============================================================

def decode_f32(data):

    usable = (
        len(data) // 4
    ) * 4

    if usable == 0:
        return []

    count = usable // 4

    raw = struct.unpack(
        f"<{count}f",
        data[:usable]
    )

    return [
        x
        for x in raw
        if math.isfinite(x)
    ]


# ============================================================
# DETERMINISTIC BLOCK-ALIGNED SAMPLING
# ============================================================

def sample_tensor(
    f,
    tensor,
    sample_bytes=65536
):

    start = tensor["file_start"]
    span = tensor["span"]
    typ = tensor["type_name"]

    if typ == "Q8_0":

        BLOCK = 34

        total_blocks = span // BLOCK

        if total_blocks == 0:
            return [], []

        target_blocks = max(
            1,
            sample_bytes // BLOCK
        )

        target_blocks = min(
            target_blocks,
            total_blocks
        )

        samples = []

        for i in range(target_blocks):

            block_index = (
                i * total_blocks
                // target_blocks
            )

            pos = (
                start
                + block_index * BLOCK
            )

            f.seek(pos)

            block = f.read(BLOCK)

            if len(block) == BLOCK:
                samples.append(block)

        data = b"".join(samples)

        return decode_q8_sample(data)

    if typ == "F32":

        if span <= sample_bytes:

            f.seek(start)

            data = f.read(span)

        else:

            chunk = 4096

            count = max(
                1,
                sample_bytes // chunk
            )

            samples = []

            for i in range(count):

                pos = (
                    start
                    + i * span
                    // count
                )

                pos -= pos % 4

                f.seek(pos)

                chunk_data = f.read(chunk)

                samples.append(
                    chunk_data
                )

            data = b"".join(samples)

        return decode_f32(data), []

    raise ValueError(
        f"Unsupported tensor type: {typ}"
    )


# ============================================================
# TENSOR FINGERPRINT
# ============================================================

def tensor_statistics(
    f,
    tensor
):

    values, scales = sample_tensor(
        f,
        tensor
    )

    result = summarize(values)

    scale_stats = summarize(scales)

    result["scale_mean"] = (
        scale_stats["mean"]
    )

    result["scale_std"] = (
        scale_stats["std"]
    )

    result["scale_rms"] = (
        scale_stats["rms"]
    )

    return result


# ============================================================
# NORMALIZED DISTANCE
# ============================================================

FEATURES = [
    "mean",
    "std",
    "rms",
    "abs_mean",
    "scale_mean",
    "scale_std",
    "scale_rms",
]


def raw_distance(a, b):

    return math.sqrt(
        sum(
            (
                a[key]
                - b[key]
            ) ** 2
            for key in FEATURES
        )
    )


def relative_distance(a, b):

    total = 0.0

    for key in FEATURES:

        denominator = max(
            abs(a[key]),
            abs(b[key]),
            1e-12
        )

        delta = (
            a[key] - b[key]
        ) / denominator

        total += delta * delta

    return math.sqrt(total)


def cosine_distance(a, b):

    va = [
        a[key]
        for key in FEATURES
    ]

    vb = [
        b[key]
        for key in FEATURES
    ]

    dot = sum(
        x * y
        for x, y in zip(va, vb)
    )

    na = math.sqrt(
        sum(x * x for x in va)
    )

    nb = math.sqrt(
        sum(y * y for y in vb)
    )

    if na == 0.0 or nb == 0.0:
        return 0.0

    cosine = dot / (na * nb)

    cosine = max(
        -1.0,
        min(1.0, cosine)
    )

    return 1.0 - cosine


# ============================================================
# RUN
# ============================================================

print("=" * 72)
print(" OPENMIND / Q8_0-AWARE PARAMETER DIVERGENCE V3")
print("=" * 72)

print()
print(f"File:       {PATH}")
print(f"GGUF:       v{version}")
print(f"Tensors:    {tensor_count}")
print(f"Layers:     {len(layers)}")
print("Mode:       decoded + normalized deterministic sampling")
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

            stats[layer][component] = (
                tensor_statistics(
                    f,
                    layers[layer][component]
                )
            )


# ============================================================
# LAYER TRANSITIONS
# ============================================================

print()
print("=" * 72)
print(" NORMALIZED LAYER DIVERGENCE")
print("=" * 72)

layers_sorted = sorted(stats)

transitions = {}

for a, b in zip(
    layers_sorted,
    layers_sorted[1:]
):

    raw_values = []
    relative_values = []
    cosine_values = []

    common = set(
        stats[a]
    ) & set(
        stats[b]
    )

    for component in common:

        sa = stats[a][component]
        sb = stats[b][component]

        raw_values.append(
            raw_distance(sa, sb)
        )

        relative_values.append(
            relative_distance(sa, sb)
        )

        cosine_values.append(
            cosine_distance(sa, sb)
        )

    transitions[(a, b)] = {
        "raw": sum(raw_values) / len(raw_values),
        "relative": (
            sum(relative_values)
            / len(relative_values)
        ),
        "cosine": (
            sum(cosine_values)
            / len(cosine_values)
        ),
    }

    print(
        f"L{a:02d} -> L{b:02d} | "
        f"relative={transitions[(a,b)]['relative']:.6f} | "
        f"cosine={transitions[(a,b)]['cosine']:.6f}"
    )


# ============================================================
# COMPONENT DIVERGENCE
# ============================================================

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

    relative = []
    cosine = []

    for a, b in zip(
        layers_sorted,
        layers_sorted[1:]
    ):

        if (
            component not in stats[a]
            or component not in stats[b]
        ):
            continue

        relative.append(
            relative_distance(
                stats[a][component],
                stats[b][component]
            )
        )

        cosine.append(
            cosine_distance(
                stats[a][component],
                stats[b][component]
            )
        )

    if relative:

        r = (
            sum(relative)
            / len(relative)
        )

        c = (
            sum(cosine)
            / len(cosine)
        )

        component_scores[component] = (
            r,
            c
        )

        print(
            f"{component:30s} | "
            f"relative={r:.6f} | "
            f"cosine={c:.6f}"
        )


# ============================================================
# TRANSITION RANKING
# ============================================================

print()
print("=" * 72)
print(" TRANSITION RANKING")
print("=" * 72)

ranked = sorted(
    transitions.items(),
    key=lambda x: x[1]["relative"],
    reverse=True
)

for (a, b), score in ranked:

    print(
        f"L{a:02d} -> L{b:02d} | "
        f"relative={score['relative']:.6f} | "
        f"cosine={score['cosine']:.6f}"
    )


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 72)
print(" SUMMARY")
print("=" * 72)

relative_values = [
    x["relative"]
    for x in transitions.values()
]

cosine_values = [
    x["cosine"]
    for x in transitions.values()
]

if relative_values:

    max_relative = max(
        relative_values
    )

    min_relative = min(
        relative_values
    )

    mean_relative = (
        sum(relative_values)
        / len(relative_values)
    )

    max_pair = max(
        transitions,
        key=lambda p:
            transitions[p]["relative"]
    )

    min_pair = min(
        transitions,
        key=lambda p:
            transitions[p]["relative"]
    )

    print(
        f"Minimum relative: "
        f"{min_relative:.6f}"
    )

    print(
        f"Maximum relative: "
        f"{max_relative:.6f}"
    )

    print(
        f"Mean relative:    "
        f"{mean_relative:.6f}"
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
    "Q8_0-aware parameter divergence V3 complete."
)

print(
    "Tensor payloads were streamed and deterministically sampled."
)

