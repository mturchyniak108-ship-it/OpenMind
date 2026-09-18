import math
import re
import struct
from pathlib import Path
from collections import defaultdict

PATH = Path.home() / "qwen2.5-coder-q8_0.gguf"

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

EPS = 1e-12


# ------------------------------------------------------------
# GGUF
# ------------------------------------------------------------

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
        f"Unsupported metadata type: {typ}"
    )


def align(offset, alignment):
    return (
        (offset + alignment - 1)
        // alignment
    ) * alignment


# ------------------------------------------------------------
# READ DIRECTORY
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
# LAYER DIRECTORY
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
# Q8 SIGNATURE
# ------------------------------------------------------------

def summarize_q8(data):

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

        for x in q:

            value = scale * x

            if math.isfinite(value):
                values.append(value)

        scales.append(scale)

    if not values:
        return None

    n = len(values)

    mean = (
        sum(values) / n
    )

    rms = math.sqrt(
        sum(x * x for x in values) / n
    )

    abs_mean = (
        sum(abs(x) for x in values)
        / n
    )

    variance = (
        sum(
            (x - mean) ** 2
            for x in values
        )
        / n
    )

    scale_mean = (
        sum(scales)
        / len(scales)
        if scales
        else 0.0
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
# TENSOR SAMPLING
# ------------------------------------------------------------

def tensor_signature(
    f,
    tensor,
    fraction
):

    if tensor["type"] != 8:
        return None

    total_blocks = (
        tensor["span"] // BLOCK
    )

    if total_blocks == 0:
        return None

    count = min(
        SAMPLE_BLOCKS,
        total_blocks
    )

    max_start = (
        total_blocks - count
    )

    start_block = int(
        max_start * fraction
    )

    data = bytearray()

    for i in range(count):

        block_index = (
            start_block
            + i * count
            // count
        )

        block_index = min(
            block_index,
            total_blocks - 1
        )

        pos = (
            tensor["file_start"]
            + block_index * BLOCK
        )

        f.seek(pos)

        chunk = f.read(BLOCK)

        if len(chunk) == BLOCK:
            data.extend(chunk)

    return summarize_q8(
        bytes(data)
    )


# ------------------------------------------------------------
# ROBUST NORMALIZATION
# ------------------------------------------------------------

def normalize_component(sig):

    if sig is None:
        return None

    # Transform each statistic into a scale-free quantity.
    #
    # RMS and abs_mean are normalized by RMS.
    # Variance is normalized by RMS^2.
    # Scale statistics are normalized by scale RMS.

    mean = sig[0]
    rms = sig[1]
    abs_mean = sig[2]
    variance = sig[3]
    scale_mean = sig[4]
    scale_rms = sig[5]

    value_scale = max(
        abs(rms),
        abs(abs_mean),
        EPS
    )

    variance_scale = max(
        rms * rms,
        EPS
    )

    scale_scale = max(
        abs(scale_rms),
        EPS
    )

    return [
        mean / value_scale,
        rms / value_scale,
        abs_mean / value_scale,
        variance / variance_scale,
        scale_mean / scale_scale,
        scale_rms / scale_scale,
    ]


# ------------------------------------------------------------
# LAYER SIGNATURE
# ------------------------------------------------------------

def layer_signature(
    f,
    layer,
    fraction
):

    result = {}

    for component in sorted(
        layers[layer]
    ):

        tensor = layers[layer][component]

        sig = tensor_signature(
            f,
            tensor,
            fraction
        )

        sig = normalize_component(
            sig
        )

        if sig is not None:
            result[component] = sig

    return result


# ------------------------------------------------------------
# DISTANCE
# ------------------------------------------------------------

def compare_layers(a, b):

    common = sorted(
        set(a)
        & set(b)
    )

    if not common:
        return float("inf"), 0.0

    va = []
    vb = []

    for component in common:

        va.extend(a[component])
        vb.extend(b[component])

    n = len(va)

    distance = math.sqrt(
        sum(
            (va[i] - vb[i]) ** 2
            for i in range(n)
        )
        / n
    )

    dot = sum(
        va[i] * vb[i]
        for i in range(n)
    )

    norm_a = math.sqrt(
        sum(x * x for x in va)
    )

    norm_b = math.sqrt(
        sum(x * x for x in vb)
    )

    if norm_a < EPS or norm_b < EPS:
        cosine = 0.0
    else:
        cosine = (
            dot
            / (norm_a * norm_b)
        )

    return distance, cosine


# ------------------------------------------------------------
# RUN
# ------------------------------------------------------------

print("=" * 72)
print(" OPENMIND / RECURRENCE STABILITY V2")
print("=" * 72)

print()
print(f"File:       {PATH}")
print(f"Layers:     {len(layers)}")
print(f"Candidates: {len(CANDIDATES)}")
print("Method:     normalized Q8_0 multi-offset signatures")
print()

offsets = [
    0.00,
    0.20,
    0.40,
    0.60,
    0.80,
]

signatures = {}

with PATH.open("rb") as f:

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


# ------------------------------------------------------------
# RECURRENCE TEST
# ------------------------------------------------------------

print()
print("=" * 72)
print(" NORMALIZED RECURRENCE STABILITY")
print("=" * 72)

results = {}

for a, b in CANDIDATES:

    distances = []
    cosines = []

    for fraction in offsets:

        d, c = compare_layers(
            signatures[
                (fraction, a)
            ],
            signatures[
                (fraction, b)
            ]
        )

        distances.append(d)
        cosines.append(c)

    mean_d = (
        sum(distances)
        / len(distances)
    )

    mean_c = (
        sum(cosines)
        / len(cosines)
    )

    variance = (
        sum(
            (x - mean_d) ** 2
            for x in distances
        )
        / len(distances)
    )

    std_d = math.sqrt(
        variance
    )

    results[(a, b)] = (
        mean_d,
        std_d,
        mean_c,
        distances,
        cosines,
    )

    print(
        f"L{a:02d} <-> L{b:02d} | "
        f"distance={mean_d:.6f} | "
        f"std={std_d:.6f} | "
        f"cosine={mean_c:.6f}"
    )


# ------------------------------------------------------------
# RANKING
# ------------------------------------------------------------

print()
print("=" * 72)
print(" RECURRENCE RANKING")
print("=" * 72)

for (a, b), (
    mean_d,
    std_d,
    mean_c,
    distances,
    cosines,
) in sorted(
    results.items(),
    key=lambda x: x[1][0]
):

    print(
        f"L{a:02d} <-> L{b:02d} | "
        f"d={mean_d:.6f} | "
        f"std={std_d:.6f} | "
        f"cos={mean_c:.6f}"
    )


# ------------------------------------------------------------
# OFFSET DETAIL
# ------------------------------------------------------------

print()
print("=" * 72)
print(" OFFSET-BY-OFFSET DETAIL")
print("=" * 72)

for (a, b), (
    mean_d,
    std_d,
    mean_c,
    distances,
    cosines,
) in results.items():

    print()
    print(
        f"L{a:02d} <-> L{b:02d}"
    )

    for i, fraction in enumerate(offsets):

        print(
            f"  {fraction:.2f} | "
            f"d={distances[i]:.6f} | "
            f"cos={cosines[i]:.6f}"
        )


print()
print("=" * 72)
print(" INTERPRETATION")
print("=" * 72)

print(
    "Low distance + low std + high cosine:"
)

print(
    "    strongest evidence for stable recurrence."
)

print(
    "Low distance + high std:"
)

print(
    "    likely sampling-sensitive."
)

print(
    "High distance + high cosine:"
)

print(
    "    related magnitude/shape but not strongly"
)

print(
    "    equivalent under this signature."
)

print()
print(
    "Normalized recurrence stability V2 complete."
)
