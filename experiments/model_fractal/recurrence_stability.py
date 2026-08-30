import math
import re
import struct
from pathlib import Path
from collections import defaultdict

PATH = Path.home() / "qwen2.5-coder-q8_0.gguf"

# Candidate pairs discovered by layer_similarity.py
CANDIDATES = [
    (10, 19),
    (7, 11),
    (18, 22),
    (8, 14),
    (6, 14),
    (7, 22),
    (7, 12),
    (7, 18),
    (12, 18),
    (5, 15),
]

BLOCK = 34
SAMPLE_BLOCKS = 512


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

    raise ValueError(f"Unsupported metadata type {typ}")


def align(offset, alignment):
    return ((offset + alignment - 1) // alignment) * alignment


# ------------------------------------------------------------
# GGUF DIRECTORY
# ------------------------------------------------------------

with PATH.open("rb") as f:

    if f.read(4) != b"GGUF":
        raise SystemExit("Not GGUF")

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

tensors.sort(key=lambda x: x["offset"])

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
# FIND LAYER TENSORS
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

    layers[layer][component] = tensor


# ------------------------------------------------------------
# Q8 BLOCK SIGNATURE
# ------------------------------------------------------------

def block_signature(data):

    usable = (
        len(data) // BLOCK
    ) * BLOCK

    if usable == 0:
        return [0.0] * 6

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

        for x in q:
            v = scale * x

            if math.isfinite(v):
                values.append(v)

        scales.append(scale)

    if not values:
        return [0.0] * 6

    n = len(values)

    mean = sum(values) / n

    rms = math.sqrt(
        sum(x * x for x in values) / n
    )

    abs_mean = (
        sum(abs(x) for x in values)
        / n
    )

    variance = (
        sum((x - mean) ** 2 for x in values)
        / n
    )

    scale_mean = (
        sum(scales) / len(scales)
        if scales else 0.0
    )

    scale_rms = math.sqrt(
        sum(x * x for x in scales)
        / len(scales)
    ) if scales else 0.0

    return [
        mean,
        rms,
        abs_mean,
        variance,
        scale_mean,
        scale_rms,
    ]


# ------------------------------------------------------------
# MULTI-OFFSET SIGNATURE
# ------------------------------------------------------------

def tensor_signature(f, tensor, offset_fraction):

    if tensor["type"] != 8:
        return None

    total_blocks = (
        tensor["span"] // BLOCK
    )

    if total_blocks < SAMPLE_BLOCKS:
        count = total_blocks
    else:
        count = SAMPLE_BLOCKS

    if count == 0:
        return None

    base = int(
        total_blocks
        * offset_fraction
    )

    base = min(
        max(base, 0),
        max(0, total_blocks - count)
    )

    data = bytearray()

    for i in range(count):

        block_index = (
            base
            + i * total_blocks
            // count
        )

        pos = (
            tensor["file_start"]
            + block_index * BLOCK
        )

        f.seek(pos)

        data.extend(
            f.read(BLOCK)
        )

    return block_signature(bytes(data))


# ------------------------------------------------------------
# LAYER SIGNATURE
# ------------------------------------------------------------

def layer_signature(f, layer, fraction):

    features = []

    for component in sorted(
        layers[layer]
    ):

        tensor = layers[layer][component]

        sig = tensor_signature(
            f,
            tensor,
            fraction
        )

        if sig is not None:
            features.extend(sig)

    return features


def distance(a, b):

    if not a or not b:
        return float("inf")

    n = min(len(a), len(b))

    return math.sqrt(
        sum(
            (a[i] - b[i]) ** 2
            for i in range(n)
        )
    )


# ------------------------------------------------------------
# RUN
# ------------------------------------------------------------

print("=" * 72)
print(" OPENMIND / RECURRENCE STABILITY ANALYSIS")
print("=" * 72)

print()
print(f"File:       {PATH}")
print(f"Layers:     {len(layers)}")
print(f"Candidates: {len(CANDIDATES)}")
print("Method:     multi-offset Q8_0 sampling")
print()

offsets = [
    0.00,
    0.20,
    0.40,
    0.60,
    0.80,
]

results = defaultdict(list)

with PATH.open("rb") as f:

    signatures = {}

    for fraction in offsets:

        print(
            f"Sampling offset "
            f"{fraction:.2f}..."
        )

        for layer in sorted(layers):

            signatures[
                (fraction, layer)
            ] = layer_signature(
                f,
                layer,
                fraction
            )

    print()
    print("=" * 72)
    print(" RECURRENCE STABILITY")
    print("=" * 72)

    for a, b in CANDIDATES:

        distances = []

        for fraction in offsets:

            da = signatures[
                (fraction, a)
            ]

            db = signatures[
                (fraction, b)
            ]

            distances.append(
                distance(da, db)
            )

        mean = (
            sum(distances)
            / len(distances)
        )

        variance = (
            sum(
                (x - mean) ** 2
                for x in distances
            )
            / len(distances)
        )

        std = math.sqrt(variance)

        results[(a, b)] = (
            mean,
            std,
            distances,
        )

        print(
            f"L{a:02d} <-> L{b:02d} | "
            f"mean={mean:.6f} | "
            f"std={std:.6f} | "
            f"range={min(distances):.6f}"
            f"..{max(distances):.6f}"
        )


print()
print("=" * 72)
print(" STABILITY RANKING")
print("=" * 72)

for (a, b), (
    mean,
    std,
    distances,
) in sorted(
    results.items(),
    key=lambda x: x[1][0]
):

    stability = (
        mean / (std + 1e-12)
    )

    print(
        f"L{a:02d} <-> L{b:02d} | "
        f"mean={mean:.6f} | "
        f"std={std:.6f} | "
        f"stability={stability:.3f}"
    )


print()
print("=" * 72)
print(" INTERPRETATION")
print("=" * 72)

print(
    "Low mean + low std = stable structural recurrence."
)

print(
    "Low mean + high std = possible sampling artifact."
)

print(
    "High mean + low std = consistently dissimilar."
)

print()
print(
    "Recurrence stability analysis complete."
)
