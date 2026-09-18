import json
import math
import struct
from pathlib import Path
from collections import defaultdict


# ============================================================
# CONFIG
# ============================================================

PATH = Path.home() / "qwen2.5-coder-q8_0.gguf"
OUT = Path(
    "experiments/model_fractal/"
    "q8_parameter_field_v4.json"
)

SAMPLE_BYTES = 65536
Q8_BLOCK = 34


# ============================================================
# GGUF TYPES
# ============================================================

TYPE_NAMES = {
    0: "F32",
    1: "F16",
    8: "Q8_0",
}


# ============================================================
# GGUF PRIMITIVES
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

    return data.decode(
        "utf-8",
        errors="replace",
    )


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
# GGUF DIRECTORY
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
                f"TYPE_{tensor_type}",
            ),
            "offset": offset,
        })

    directory_end = f.tell()


data_start = align(
    directory_end,
    alignment,
)


# ============================================================
# EXACT TENSOR SPANS
# ============================================================

ordered = sorted(
    tensors,
    key=lambda x: x["offset"],
)

file_size = PATH.stat().st_size
payload_size = file_size - data_start

for i, tensor in enumerate(ordered):

    start = tensor["offset"]

    if i + 1 < len(ordered):
        end = ordered[i + 1]["offset"]
    else:
        end = payload_size

    tensor["file_start"] = (
        data_start + start
    )

    tensor["span"] = (
        end - start
    )


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

    variance = sum(
        (x - mean) ** 2
        for x in values
    ) / n

    std = math.sqrt(
        max(variance, 0.0)
    )

    rms = math.sqrt(
        sum(x * x for x in values) / n
    )

    abs_mean = (
        sum(abs(x) for x in values) / n
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
# ============================================================

def decode_q8_sample(data):

    usable = (
        len(data) // Q8_BLOCK
    ) * Q8_BLOCK

    values = []
    scales = []

    for pos in range(
        0,
        usable,
        Q8_BLOCK,
    ):

        block = data[
            pos:pos + Q8_BLOCK
        ]

        scale = struct.unpack(
            "<e",
            block[:2],
        )[0]

        if not math.isfinite(scale):
            continue

        q = struct.unpack(
            "<32b",
            block[2:],
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
        data[:usable],
    )

    return [
        x
        for x in raw
        if math.isfinite(x)
    ]


# ============================================================
# DETERMINISTIC SAMPLING
# ============================================================

def sample_tensor(f, tensor):

    start = tensor["file_start"]
    span = tensor["span"]
    typ = tensor["type_name"]

    if typ == "Q8_0":

        total_blocks = (
            span // Q8_BLOCK
        )

        if total_blocks == 0:
            return [], []

        target_blocks = max(
            1,
            SAMPLE_BYTES // Q8_BLOCK,
        )

        target_blocks = min(
            target_blocks,
            total_blocks,
        )

        samples = []

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

            block = f.read(
                Q8_BLOCK
            )

            if len(block) == Q8_BLOCK:
                samples.append(block)

        return decode_q8_sample(
            b"".join(samples)
        )

    if typ == "F32":

        if span <= SAMPLE_BYTES:

            f.seek(start)

            return (
                decode_f32(
                    f.read(span)
                ),
                [],
            )

        chunk = 4096

        count = max(
            1,
            SAMPLE_BYTES // chunk,
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

            samples.append(
                f.read(chunk)
            )

        return (
            decode_f32(
                b"".join(samples)
            ),
            [],
        )

    raise ValueError(
        f"Unsupported tensor type: {typ}"
    )


# ============================================================
# TENSOR FINGERPRINT
# ============================================================

def fingerprint(f, tensor):

    values, scales = sample_tensor(
        f,
        tensor,
    )

    value_stats = summarize(values)
    scale_stats = summarize(scales)

    return {
        "name": tensor["name"],
        "type": tensor["type_name"],
        "dims": tensor["dims"],
        "span": tensor["span"],
        "sample_bytes": SAMPLE_BYTES,
        "value": value_stats,
        "scale": scale_stats,
    }


# ============================================================
# BUILD LAYER FIELD
# ============================================================

layers = defaultdict(dict)
global_tensors = []

with PATH.open("rb") as f:

    for tensor in tensors:

        name = tensor["name"]

        result = fingerprint(
            f,
            tensor,
        )

        if name.startswith("blk."):

            parts = name.split(".")

            layer = int(parts[1])
            component = ".".join(parts[2:])

            layers[layer][component] = result

        else:

            global_tensors.append(result)


# ============================================================
# COMPONENT SCHEMA
# ============================================================

layer_ids = sorted(layers)

components = sorted({
    component
    for layer in layers.values()
    for component in layer
})


# ============================================================
# COMPONENT DISTANCE
# ============================================================

FEATURES = [
    "mean",
    "std",
    "rms",
    "abs_mean",
]


def component_distance(a, b):

    total = 0.0

    for key in FEATURES:

        x = a["value"][key]
        y = b["value"][key]

        scale = max(
            abs(x),
            abs(y),
            1e-12,
        )

        d = (
            x - y
        ) / scale

        total += d * d

    return math.sqrt(
        total / len(FEATURES)
    )


def scale_distance(a, b):

    total = 0.0
    count = 0

    for key in (
        "mean",
        "std",
        "rms",
    ):

        x = a["scale"][key]
        y = b["scale"][key]

        scale = max(
            abs(x),
            abs(y),
            1e-12,
        )

        d = (
            x - y
        ) / scale

        total += d * d
        count += 1

    return math.sqrt(
        total / count
    )


# ============================================================
# TRANSITION FIELD
# ============================================================

transitions = []

for a, b in zip(
    layer_ids,
    layer_ids[1:],
):

    component_scores = {}

    for component in components:

        if (
            component not in layers[a]
            or component not in layers[b]
        ):
            continue

        x = layers[a][component]
        y = layers[b][component]

        component_scores[component] = {
            "value": component_distance(
                x,
                y,
            ),
            "scale": scale_distance(
                x,
                y,
            ),
        }

    if component_scores:

        mean_value = (
            sum(
                x["value"]
                for x in component_scores.values()
            )
            / len(component_scores)
        )

        mean_scale = (
            sum(
                x["scale"]
                for x in component_scores.values()
            )
            / len(component_scores)
        )

    else:

        mean_value = 0.0
        mean_scale = 0.0

    transitions.append({
        "from": a,
        "to": b,
        "value_divergence": mean_value,
        "scale_divergence": mean_scale,
        "components": component_scores,
    })


# ============================================================
# PERSIST
# ============================================================

result = {
    "format": (
        "OpenMind Q8 Parameter "
        "Field Fingerprint V4"
    ),
    "source": str(PATH),
    "gguf": {
        "version": version,
        "tensor_count": tensor_count,
        "metadata_count": metadata_count,
        "alignment": alignment,
        "data_start": data_start,
        "file_size": file_size,
    },
    "sampling": {
        "method": "deterministic_block_aligned",
        "sample_bytes": SAMPLE_BYTES,
        "q8_block_bytes": Q8_BLOCK,
    },
    "layer_count": len(layer_ids),
    "layer_ids": layer_ids,
    "components": components,
    "global_tensors": global_tensors,
    "layers": {
        str(layer): layers[layer]
        for layer in layer_ids
    },
    "transitions": transitions,
}


OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

OUT.write_text(
    json.dumps(
        result,
        indent=2,
        sort_keys=True,
    )
)


# ============================================================
# REPORT
# ============================================================

print("=" * 72)
print(
    " OPENMIND / Q8 PARAMETER FIELD "
    "FINGERPRINT V4"
)
print("=" * 72)

print()
print("Source:", PATH)
print("GGUF version:", version)
print("Tensor count:", tensor_count)
print("Layer count:", len(layer_ids))
print("Components:", len(components))
print(
    "Sampling:",
    SAMPLE_BYTES,
    "bytes/tensor",
)

print()
print("=== COMPONENT FIELD SCHEMA ===")

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
print("=" * 72)
print(" PARAMETER-FIELD TRANSITIONS")
print("=" * 72)

for transition in transitions:

    print(
        f"L{transition['from']:02d} -> "
        f"L{transition['to']:02d} | "
        f"value="
        f"{transition['value_divergence']:.6f} | "
        f"scale="
        f"{transition['scale_divergence']:.6f}"
    )

print()
print("=" * 72)
print(" TOP COMPONENT TRANSITIONS")
print("=" * 72)

ranked = []

for transition in transitions:

    for component, score in (
        transition["components"].items()
    ):

        ranked.append((
            score["value"],
            transition["from"],
            transition["to"],
            component,
            score["scale"],
        ))

for value, a, b, component, scale in sorted(
    ranked,
    reverse=True,
)[:20]:

    print(
        f"L{a:02d} -> L{b:02d} | "
        f"{component:<25} "
        f"value={value:.6f} "
        f"scale={scale:.6f}"
    )

print()
print("Output:", OUT)
print()
print("Q8 PARAMETER FIELD FINGERPRINT COMPLETE")
