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
    "q8_parameter_field_v4_1.json"
)

# Number of Q8 blocks sampled per tensor.
SAMPLE_BLOCKS = 128

Q8_BLOCK_VALUES = 32
Q8_BLOCK_BYTES = 34

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


def i32(f):
    return struct.unpack("<i", f.read(4))[0]


def f32(f):
    return struct.unpack("<f", f.read(4))[0]


def f16(f):
    return struct.unpack("<e", f.read(2))[0]


def read_string(f):
    n = u64(f)
    data = f.read(n)

    if len(data) != n:
        raise EOFError("Unexpected EOF while reading string")

    return data.decode("utf-8", errors="replace")


# ============================================================
# GGUF VALUE SKIPPING
# ============================================================

FIXED_SIZES = {
    0: 4,   # UINT32
    1: 1,   # UINT8
    2: 2,   # INT8? / INT16-family depending GGUF type
    3: 2,
    4: 4,
    5: 4,
    6: 4,
    7: 1,   # BOOL
    10: 8,
    11: 8,
    12: 8,
}


def skip_value(f, typ):
    if typ in FIXED_SIZES:
        f.seek(FIXED_SIZES[typ], 1)
        return

    if typ == 8:
        # STRING
        n = u64(f)
        f.seek(n, 1)
        return

    if typ == 9:
        # ARRAY
        subtype = u32(f)
        count = u64(f)

        for _ in range(count):
            skip_value(f, subtype)

        return

    raise ValueError(f"Unsupported GGUF metadata type: {typ}")


# ============================================================
# READ GGUF STRUCTURE
# ============================================================

def read_header():
    with PATH.open("rb") as f:

        if f.read(4) != b"GGUF":
            raise ValueError("Not a GGUF file")

        version = u32(f)
        tensor_count = u64(f)
        metadata_count = u64(f)

        metadata = {}

        for _ in range(metadata_count):
            key = read_string(f)
            typ = u32(f)

            # We only need a small subset of metadata values.
            if typ == 8:
                metadata[key] = read_string(f)

            elif typ == 4:
                metadata[key] = u32(f)

            elif typ == 0:
                metadata[key] = f32(f)

            elif typ == 7:
                metadata[key] = bool(f.read(1)[0])

            elif typ == 9:
                subtype = u32(f)
                count = u64(f)

                # Don't materialize huge tokenizer arrays.
                metadata[key] = {
                    "array": True,
                    "count": count,
                    "type": subtype,
                }

                for _ in range(count):
                    skip_value(f, subtype)

            else:
                skip_value(f, typ)

        tensor_info_start = f.tell()

        tensors = []

        for _ in range(tensor_count):

            name = read_string(f)

            n_dims = u32(f)

            dims = [
                u64(f)
                for _ in range(n_dims)
            ]

            tensor_type = u32(f)
            offset = u64(f)

            tensors.append({
                "name": name,
                "dims": dims,
                "type": tensor_type,
                "type_name": TYPE_NAMES.get(
                    tensor_type,
                    f"TYPE_{tensor_type}",
                ),
                "offset": offset,
            })

        # GGUF tensor data is aligned.
        alignment = 32

        data_start = (
            (f.tell() + alignment - 1)
            // alignment
        ) * alignment

    return {
        "version": version,
        "tensor_count": tensor_count,
        "metadata_count": metadata_count,
        "metadata": metadata,
        "tensor_info_start": tensor_info_start,
        "data_start": data_start,
        "tensors": tensors,
    }


# ============================================================
# NUMERICAL HELPERS
# ============================================================

def summarize(values):
    if not values:
        return {
            "count": 0,
            "mean": None,
            "rms": None,
            "std": None,
            "min": None,
            "max": None,
            "abs_mean": None,
        }

    n = len(values)

    mean = sum(values) / n

    mean_sq = (
        sum(x * x for x in values)
        / n
    )

    variance = max(
        0.0,
        mean_sq - mean * mean,
    )

    return {
        "count": n,
        "mean": mean,
        "rms": math.sqrt(mean_sq),
        "std": math.sqrt(variance),
        "min": min(values),
        "max": max(values),
        "abs_mean": (
            sum(abs(x) for x in values)
            / n
        ),
    }


# ============================================================
# Q8_0 SAMPLER
# ============================================================

def sample_q8_0(f, tensor, data_start):

    dims = tensor["dims"]

    elements = 1

    for d in dims:
        elements *= d

    total_blocks = (
        elements // Q8_BLOCK_VALUES
    )

    blocks = min(
        SAMPLE_BLOCKS,
        total_blocks,
    )

    if blocks == 0:
        return {
            "values": [],
            "scales": [],
            "total_blocks": total_blocks,
            "sampled_blocks": 0,
        }

    absolute_start = (
        data_start + tensor["offset"]
    )

    values = []
    scales = []

    # Evenly distribute sampled blocks
    # across the tensor rather than taking
    # only the beginning.
    positions = [
        min(
            total_blocks - 1,
            int(
                i * total_blocks / blocks
            ),
        )
        for i in range(blocks)
    ]

    for block_index in positions:

        absolute = (
            absolute_start
            + block_index * Q8_BLOCK_BYTES
        )

        f.seek(absolute)

        raw_scale = f.read(2)

        if len(raw_scale) != 2:
            raise EOFError(
                f"Unable to read Q8 scale "
                f"at {absolute}"
            )

        scale = struct.unpack(
            "<e",
            raw_scale,
        )[0]

        raw_q = f.read(32)

        if len(raw_q) != 32:
            raise EOFError(
                f"Unable to read Q8 block "
                f"at {absolute}"
            )

        q = struct.unpack(
            "<32b",
            raw_q,
        )

        scales.append(scale)

        for x in q:
            values.append(
                float(scale) * float(x)
            )

    return {
        "values": values,
        "scales": scales,
        "total_blocks": total_blocks,
        "sampled_blocks": blocks,
    }


# ============================================================
# F32 SAMPLER
# ============================================================

def sample_f32(f, tensor, data_start):

    dims = tensor["dims"]

    elements = 1

    for d in dims:
        elements *= d

    absolute_start = (
        data_start + tensor["offset"]
    )

    # Small F32 tensors are cheap.
    if elements <= SAMPLE_BLOCKS * 32:
        count = elements
        positions = range(count)

    else:
        count = min(
            SAMPLE_BLOCKS * 32,
            elements,
        )

        positions = [
            min(
                elements - 1,
                int(
                    i * elements / count
                ),
            )
            for i in range(count)
        ]

    values = []

    for index in positions:

        f.seek(
            absolute_start
            + index * 4
        )

        raw = f.read(4)

        if len(raw) != 4:
            raise EOFError(
                f"Unable to read F32 "
                f"at tensor offset "
                f"{tensor['offset']}"
            )

        values.append(
            struct.unpack(
                "<f",
                raw,
            )[0]
        )

    return {
        "values": values,
        "scales": [],
        "total_blocks": None,
        "sampled_blocks": None,
    }


# ============================================================
# TENSOR FINGERPRINT
# ============================================================

def fingerprint(f, tensor, data_start):

    typ = tensor["type_name"]

    if typ == "Q8_0":
        sampled = sample_q8_0(
            f,
            tensor,
            data_start,
        )

    elif typ == "F32":
        sampled = sample_f32(
            f,
            tensor,
            data_start,
        )

    else:
        return {
            "name": tensor["name"],
            "type": typ,
            "dims": tensor["dims"],
            "unsupported": True,
        }

    stats = summarize(
        sampled["values"]
    )

    result = {
        "name": tensor["name"],
        "type": typ,
        "dims": tensor["dims"],
        "offset": tensor["offset"],
        "stats": stats,
    }

    if typ == "Q8_0":
        scale_stats = summarize(
            sampled["scales"]
        )

        result["q8"] = {
            "total_blocks":
                sampled["total_blocks"],
            "sampled_blocks":
                sampled["sampled_blocks"],
            "scale_stats":
                scale_stats,
        }

    return result


# ============================================================
# LAYER CLASSIFICATION
# ============================================================

def classify_tensor(name):

    parts = name.split(".")

    if (
        len(parts) >= 3
        and parts[0] == "blk"
    ):
        layer = int(parts[1])

        component = ".".join(
            parts[2:]
        )

        return layer, component

    return None, None


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 72)
    print(" OPENMIND / Q8 PARAMETER FIELD V4.1")
    print("=" * 72)

    info = read_header()

    tensors = info["tensors"]

    layers = defaultdict(dict)
    globals_ = []

    with PATH.open("rb") as f:

        for tensor in tensors:

            result = fingerprint(
                f,
                tensor,
                info["data_start"],
            )

            layer, component = (
                classify_tensor(
                    tensor["name"]
                )
            )

            if layer is None:
                globals_.append(result)

            else:
                layers[layer][component] = result

    layer_ids = sorted(layers)

    components = sorted({
        component
        for layer in layers.values()
        for component in layer
    })

    output = {
        "schema": "openmind.q8_parameter_field.v4.1",

        "source": str(PATH),

        "gguf": {
            "version":
                info["version"],
            "tensor_count":
                info["tensor_count"],
            "metadata_count":
                info["metadata_count"],
            "data_start":
                info["data_start"],
        },

        "model": {
            "architecture":
                info["metadata"].get(
                    "general.architecture"
                ),
            "name":
                info["metadata"].get(
                    "general.name"
                ),
            "size_label":
                info["metadata"].get(
                    "general.size_label"
                ),
            "block_count":
                info["metadata"].get(
                    "qwen2.block_count"
                ),
            "embedding_length":
                info["metadata"].get(
                    "qwen2.embedding_length"
                ),
            "feed_forward_length":
                info["metadata"].get(
                    "qwen2.feed_forward_length"
                ),
        },

        "sampling": {
            "q8_blocks_per_tensor":
                SAMPLE_BLOCKS,
            "q8_block_values":
                Q8_BLOCK_VALUES,
            "q8_block_bytes":
                Q8_BLOCK_BYTES,
        },

        "layer_count":
            len(layer_ids),

        "layer_ids":
            layer_ids,

        "components":
            components,

        "global_tensors":
            globals_,

        "layers": {
            str(layer): layers[layer]
            for layer in layer_ids
        },
    }

    OUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUT.write_text(
        json.dumps(
            output,
            indent=2,
        )
    )

    print()
    print("=== MODEL ===")
    print(
        "Name:",
        output["model"]["name"],
    )
    print(
        "Layers:",
        output["layer_count"],
    )
    print(
        "Components/layer:",
        len(components),
    )

    print()
    print("=== NUMERICAL FIELD ===")

    for layer in layer_ids:

        rms_values = [
            layers[layer][component]
            ["stats"]["rms"]
            for component in components
            if component in layers[layer]
        ]

        layer_rms = (
            sum(rms_values)
            / len(rms_values)
            if rms_values
            else 0.0
        )

        print(
            f"L{layer:02d}: "
            f"components={len(layers[layer]):2d} "
            f"mean_component_rms="
            f"{layer_rms:.8f}"
        )

    print()
    print("=== GLOBAL TENSORS ===")

    for tensor in globals_:
        print(
            f"{tensor['name']:30s} "
            f"{tensor['type']:5s} "
            f"RMS="
            f"{tensor['stats']['rms']:.8f}"
        )

    print()
    print("Output:", OUT)
    print()
    print(
        "NUMERICAL PARAMETER FIELD COMPLETE"
    )


if __name__ == "__main__":
    main()
