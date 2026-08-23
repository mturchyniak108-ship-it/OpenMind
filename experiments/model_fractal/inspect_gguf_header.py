import struct
from pathlib import Path

PATH = Path.home() / "qwen2.5-coder-q8_0.gguf"

TYPE_NAMES = {
    0: "UINT8",
    1: "INT8",
    2: "UINT16",
    3: "INT16",
    4: "UINT32",
    5: "INT32",
    6: "FLOAT32",
    7: "BOOL",
    8: "STRING",
    9: "ARRAY",
    10: "UINT64",
    11: "INT64",
    12: "FLOAT64",
}


def u8(f):
    return struct.unpack("<B", f.read(1))[0]


def u32(f):
    return struct.unpack("<I", f.read(4))[0]


def u64(f):
    return struct.unpack("<Q", f.read(8))[0]


def i8(f):
    return struct.unpack("<b", f.read(1))[0]


def i16(f):
    return struct.unpack("<h", f.read(2))[0]


def i32(f):
    return struct.unpack("<i", f.read(4))[0]


def i64(f):
    return struct.unpack("<q", f.read(8))[0]


def f32(f):
    return struct.unpack("<f", f.read(4))[0]


def f64(f):
    return struct.unpack("<d", f.read(8))[0]


def read_string(f):
    n = u64(f)

    if n > 10_000_000:
        raise ValueError(f"Suspicious string length: {n}")

    data = f.read(n)

    if len(data) != n:
        raise EOFError(
            f"Unexpected EOF reading string: "
            f"wanted {n}, got {len(data)}"
        )

    return data.decode("utf-8", errors="replace")


def skip_value(f, typ):
    """
    Consume one GGUF value without materializing large arrays.
    """

    if typ == 0:
        f.seek(1, 1)

    elif typ == 1:
        f.seek(1, 1)

    elif typ == 2:
        f.seek(2, 1)

    elif typ == 3:
        f.seek(2, 1)

    elif typ == 4:
        f.seek(4, 1)

    elif typ == 5:
        f.seek(4, 1)

    elif typ == 6:
        f.seek(4, 1)

    elif typ == 7:
        f.seek(1, 1)

    elif typ == 8:
        n = u64(f)
        if n > 10_000_000:
            raise ValueError(f"Suspicious string length: {n}")
        f.seek(n, 1)

    elif typ == 9:
        elem_type = u32(f)
        count = u64(f)

        # Consume every element, including variable-length strings.
        for _ in range(count):
            skip_value(f, elem_type)

    elif typ == 10:
        f.seek(8, 1)

    elif typ == 11:
        f.seek(8, 1)

    elif typ == 12:
        f.seek(8, 1)

    else:
        raise ValueError(f"Unsupported GGUF type: {typ}")


def read_value_preview(f, typ):
    """
    Read scalar values.
    For arrays, consume the entire array but only report
    its dimensions/type rather than materializing it.
    """

    if typ == 0:
        return u8(f)

    if typ == 1:
        return i8(f)

    if typ == 2:
        return struct.unpack("<H", f.read(2))[0]

    if typ == 3:
        return i16(f)

    if typ == 4:
        return u32(f)

    if typ == 5:
        return i32(f)

    if typ == 6:
        return f32(f)

    if typ == 7:
        return bool(u8(f))

    if typ == 8:
        return read_string(f)

    if typ == 10:
        return u64(f)

    if typ == 11:
        return i64(f)

    if typ == 12:
        return f64(f)

    if typ == 9:
        elem_type = u32(f)
        count = u64(f)

        # Consume the array safely.
        for _ in range(count):
            skip_value(f, elem_type)

        return (
            f"<ARRAY count={count} "
            f"type={TYPE_NAMES.get(elem_type, elem_type)}>"
        )

    raise ValueError(f"Unsupported GGUF type: {typ}")


def align32(offset):
    return (offset + 31) & ~31


with PATH.open("rb") as f:

    magic = f.read(4)

    if magic != b"GGUF":
        raise SystemExit(f"Not a GGUF file: {magic!r}")

    version = u32(f)
    tensor_count = u64(f)
    metadata_count = u64(f)

    print("=" * 60)
    print(" LIGHTWEIGHT GGUF INVENTORY")
    print("=" * 60)

    print(f"File:             {PATH}")
    print(f"File size:        {PATH.stat().st_size:,} bytes")
    print(f"GGUF version:     {version}")
    print(f"Tensor count:     {tensor_count}")
    print(f"Metadata count:   {metadata_count}")

    print()
    print("=" * 60)
    print(" METADATA")
    print("=" * 60)

    alignment = 32

    for i in range(metadata_count):

        key = read_string(f)
        typ = u32(f)

        value = read_value_preview(f, typ)

        if isinstance(value, str) and len(value) > 300:
            value = value[:300] + "..."

        if key == "general.alignment":
            try:
                alignment = int(value)
            except Exception:
                pass

        print(
            f"{i:3d} | "
            f"{key:45s} | "
            f"{TYPE_NAMES.get(typ, typ):10s} | "
            f"{value}"
        )

    print()
    print("=" * 60)
    print(" TENSOR INVENTORY")
    print("=" * 60)

    tensor_records = []

    for i in range(tensor_count):

        name = read_string(f)

        n_dims = u32(f)

        dims = []
        for _ in range(n_dims):
            dims.append(u64(f))

        tensor_type = u32(f)
        offset = u64(f)

        tensor_records.append(
            (name, dims, tensor_type, offset)
        )

        print(
            f"{i:3d} | "
            f"{name:65s} | "
            f"shape={tuple(dims)!s:25s} | "
            f"type={tensor_type:2d} | "
            f"offset={offset:,}"
        )

    tensor_data_start = align32(f.tell())

    print()
    print("=" * 60)
    print(" TENSOR DATA")
    print("=" * 60)

    print(f"Alignment:        {alignment}")
    print(f"Tensor info end:  {f.tell():,}")
    print(f"Tensor data start:{tensor_data_start:,}")
    print(
        f"Remaining bytes: "
        f"{PATH.stat().st_size - tensor_data_start:,}"
    )

    print()
    print("GGUF structure parsed successfully.")
    print("No tensor payloads were loaded into memory.")
