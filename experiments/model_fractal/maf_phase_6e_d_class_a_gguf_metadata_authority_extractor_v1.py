#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import stat
import struct
from pathlib import Path


SCHEMA = 'openmind.maf_phase_6e_d_class_a_gguf_metadata_authority.v1'
EXPECTED_TENSORS = 339
EXPECTED_SOURCE_SIZE = 1894532160
SOURCE_SHA256_PROVENANCE = '507de59046601282ba768a9789900e6ccf60ed93ddf346730b7c68eb0715bc47'
GENERATION_PK = 'mafgen:v1:74e506919d3418e2c540413cdcce72c35605195ef8efa36cdad4c56ad2a167d2'
INVENTORY_SHA256 = '7acf6d5dc672182aee0244b1bb85a47466f33dbdcdf10bde863e24f3659240ee'
PROTOCOL_SHA256 = '5d3063745be9b036769d73726830a11d9458f4a447daf09ac22c6c045c2e6af4'
LLAMA_AUTHORITY = '4cf5cab65d5257be31e7623eb552b1861e969c75'

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path.home() / 'qwen2.5-coder-q8_0.gguf'
INVENTORY = ROOT / 'experiments/model_fractal/gguf_tensor_inventory_v1.json'
OUTPUT = ROOT / 'experiments/model_fractal/maf_phase_6e_d_class_a_gguf_metadata_authority_v1.json'
SLOT_DIR = Path.home() / '.openmind_authoritative_slots'
SLOT_PREFIX = 'phase_6e_d_class_a_gguf_metadata_authority_'

MAGIC = b'GGUF'
MAX_STRING_BYTES = 64 * 1024 * 1024
MAX_ARRAY_ITEMS = 16 * 1024 * 1024
MAX_METADATA = 1_000_000
MAX_DIMS = 4

GGUF_TYPES = {
    0: 'UINT8',
    1: 'INT8',
    2: 'UINT16',
    3: 'INT16',
    4: 'UINT32',
    5: 'INT32',
    6: 'FLOAT32',
    7: 'BOOL',
    8: 'STRING',
    9: 'ARRAY',
    10: 'UINT64',
    11: 'INT64',
    12: 'FLOAT64',
}

GGML_TYPES = {
    0: 'F32',
    1: 'F16',
    2: 'Q4_0',
    3: 'Q4_1',
    6: 'Q5_0',
    7: 'Q5_1',
    8: 'Q8_0',
    9: 'Q8_1',
    10: 'Q2_K',
    11: 'Q3_K',
    12: 'Q4_K',
    13: 'Q5_K',
    14: 'Q6_K',
    15: 'Q8_K',
    16: 'IQ2_XXS',
    17: 'IQ2_XS',
    18: 'IQ3_XXS',
    19: 'IQ1_S',
    20: 'IQ4_NL',
    21: 'IQ3_S',
    22: 'IQ2_S',
    23: 'IQ4_XS',
    24: 'I8',
    25: 'I16',
    26: 'I32',
    27: 'I64',
    28: 'F64',
    29: 'IQ1_M',
    30: 'BF16',
}


class ExtractionError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ExtractionError(message)


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(',', ':'),
        allow_nan=False,
    ).encode('utf-8')


def fsync_directory(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def reserve_sentinel(path: Path) -> None:
    require(path.parent.resolve() == SLOT_DIR.resolve(), 'invalid sentinel namespace')
    require(path.name.startswith(SLOT_PREFIX), 'invalid sentinel prefix')
    require(path.name.endswith('.spent'), 'invalid sentinel suffix')
    require(SLOT_DIR.is_dir(), 'sentinel namespace missing')
    require(not SLOT_DIR.is_symlink(), 'sentinel namespace is symlink')
    payload = canonical_json_bytes({
        'schema': 'openmind.one_shot_reservation.v1',
        'purpose': 'phase_6e_d_class_a_gguf_metadata_authority',
        'generation_pk': GENERATION_PK,
    })
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(path, flags, 0o600)
    try:
        written = os.write(fd, payload)
        require(written == len(payload), 'short sentinel write')
        os.fsync(fd)
    finally:
        os.close(fd)
    fsync_directory(SLOT_DIR)


class Reader:
    def __init__(self, fd: int, size: int):
        self.fd = fd
        self.size = size
        self.pos = 0
        self.max_end = 0

    def read_exact(self, n: int) -> bytes:
        require(isinstance(n, int) and n >= 0, 'invalid read size')
        require(self.pos + n <= self.size, 'read beyond source size')
        parts = []
        left = n
        while left:
            chunk = os.read(self.fd, left)
            require(chunk, 'unexpected source EOF')
            parts.append(chunk)
            self.pos += len(chunk)
            self.max_end = max(self.max_end, self.pos)
            left -= len(chunk)
        return b''.join(parts)


def unpack(reader: Reader, fmt: str):
    size = struct.calcsize(fmt)
    return struct.unpack(fmt, reader.read_exact(size))[0]


def u8(reader: Reader) -> int:
    return unpack(reader, '<B')

def i8(reader: Reader) -> int:
    return unpack(reader, '<b')

def u16(reader: Reader) -> int:
    return unpack(reader, '<H')

def i16(reader: Reader) -> int:
    return unpack(reader, '<h')

def u32(reader: Reader) -> int:
    return unpack(reader, '<I')

def i32(reader: Reader) -> int:
    return unpack(reader, '<i')

def u64(reader: Reader) -> int:
    return unpack(reader, '<Q')

def i64(reader: Reader) -> int:
    return unpack(reader, '<q')


def gguf_string(reader: Reader) -> str:
    n = u64(reader)
    require(n <= MAX_STRING_BYTES, 'GGUF string exceeds limit')
    raw = reader.read_exact(n)
    return raw.decode('utf-8', errors='strict')


def float_value(raw: bytes, fmt: str, width: int):
    value = struct.unpack(fmt, raw)[0]
    bits = int.from_bytes(raw, 'little', signed=False)
    if math.isnan(value):
        logical = 'nan'
    elif math.isinf(value):
        logical = '+inf' if value > 0 else '-inf'
    else:
        logical = value
    return logical, format(bits, '0' + str(width) + 'x')


def scalar_value(reader: Reader, typ: int):
    if typ == 0:
        return u8(reader), None
    if typ == 1:
        return i8(reader), None
    if typ == 2:
        return u16(reader), None
    if typ == 3:
        return i16(reader), None
    if typ == 4:
        return u32(reader), None
    if typ == 5:
        return i32(reader), None
    if typ == 6:
        return float_value(reader.read_exact(4), '<f', 8)
    if typ == 7:
        raw = u8(reader)
        require(raw in (0, 1), 'invalid GGUF bool')
        return bool(raw), None
    if typ == 8:
        return gguf_string(reader), None
    if typ == 10:
        return u64(reader), None
    if typ == 11:
        return i64(reader), None
    if typ == 12:
        return float_value(reader.read_exact(8), '<d', 16)
    raise ExtractionError('unsupported scalar GGUF type: ' + str(typ))


def metadata_value(reader: Reader, typ: int):
    require(typ in GGUF_TYPES, 'unknown GGUF value type')
    if typ != 9:
        value, bits = scalar_value(reader, typ)
        out = {
            'classification': 'scalar',
            'gguf_value_type': typ,
            'gguf_value_type_name': GGUF_TYPES[typ],
            'value': value,
        }
        if bits is not None:
            out['ieee754_hex'] = bits
        return out
    elem = u32(reader)
    require(elem in GGUF_TYPES and elem != 9, 'unsupported GGUF array element type')
    count = u64(reader)
    require(count <= MAX_ARRAY_ITEMS, 'GGUF array exceeds limit')
    values = []
    float_bits = []
    for _ in range(count):
        value, bits = scalar_value(reader, elem)
        values.append(value)
        if bits is not None:
            float_bits.append(bits)
    out = {
        'array_element_type': elem,
        'array_element_type_name': GGUF_TYPES[elem],
        'classification': 'array',
        'gguf_value_type': 9,
        'gguf_value_type_name': 'ARRAY',
        'value': values,
    }
    if float_bits:
        require(len(float_bits) == count, 'incomplete float array bit capture')
        out['ieee754_hex'] = float_bits
    return out


def product(values) -> int:
    total = 1
    for value in values:
        require(isinstance(value, int) and value > 0, 'invalid tensor dimension')
        total *= value
    return total


def align_up(value: int, alignment: int) -> int:
    require(alignment > 0, 'invalid GGUF alignment')
    return ((value + alignment - 1) // alignment) * alignment


def inventory_name(row: dict) -> str:
    for key in ('name', 'tensor_name'):
        value = row.get(key)
        if isinstance(value, str) and value:
            return value
    raise ExtractionError('inventory tensor name missing')


def inventory_dims(row: dict):
    for key in ('dims', 'shape'):
        value = row.get(key)
        if isinstance(value, list) and value:
            return [int(x) for x in value]
    raise ExtractionError('inventory tensor dimensions missing')


def inventory_type_matches(row: dict, type_id: int) -> bool:
    for key in ('ggml_type', 'tensor_type_id', 'type_id'):
        value = row.get(key)
        if isinstance(value, int):
            return value == type_id
        if isinstance(value, str) and value.isdigit():
            return int(value) == type_id
    expected_name = GGML_TYPES.get(type_id)
    for key in ('tensor_type', 'type', 'ggml_type_name'):
        value = row.get(key)
        if isinstance(value, str) and expected_name is not None:
            clean = value.upper().replace('GGML_TYPE_', '')
            return clean == expected_name
    raise ExtractionError('inventory tensor type field unsupported')


def load_inventory():
    raw = INVENTORY.read_bytes()
    require(sha256_bytes(raw) == INVENTORY_SHA256, 'inventory SHA mismatch')
    obj = json.loads(raw.decode('utf-8'))
    rows = obj.get('tensors')
    require(isinstance(rows, list), 'inventory tensor list missing')
    require(len(rows) == EXPECTED_TENSORS, 'inventory tensor count mismatch')
    return rows


def verify_tensor_inventory(extracted: list, inventory: list) -> None:
    require(len(extracted) == EXPECTED_TENSORS, 'extracted tensor count mismatch')
    require(len(inventory) == EXPECTED_TENSORS, 'inventory tensor count mismatch')
    for ordinal, (got, expected) in enumerate(zip(extracted, inventory)):
        require('index' in expected, 'inventory index missing')
        require(int(expected['index']) == ordinal, 'inventory index mismatch')
        require(got['name'] == inventory_name(expected), 'tensor name mismatch')
        dims = inventory_dims(expected)
        require(got['dims'] == dims, 'tensor dimensions mismatch')
        require(got['element_count'] == product(dims), 'tensor element count mismatch')
        require('elements' in expected, 'inventory elements missing')
        require(got['element_count'] == int(expected['elements']), 'inventory elements mismatch')
        require(inventory_type_matches(expected, got['ggml_type']), 'tensor type mismatch')


def source_preflight():
    st = os.lstat(SOURCE)
    require(stat.S_ISREG(st.st_mode), 'source is not regular')
    require(not stat.S_ISLNK(st.st_mode), 'source is symlink')
    require(st.st_size == EXPECTED_SOURCE_SIZE, 'source stat size mismatch')
    return st


def parse_source(pre_stat):
    flags = os.O_RDONLY
    if hasattr(os, 'O_NOFOLLOW'):
        flags |= os.O_NOFOLLOW
    fd = os.open(SOURCE, flags)
    try:
        opened = os.fstat(fd)
        require(stat.S_ISREG(opened.st_mode), 'opened source is not regular')
        require(opened.st_size == EXPECTED_SOURCE_SIZE, 'opened source size mismatch')
        require(opened.st_dev == pre_stat.st_dev, 'source device changed')
        require(opened.st_ino == pre_stat.st_ino, 'source inode changed')
        reader = Reader(fd, opened.st_size)
        require(reader.read_exact(4) == MAGIC, 'invalid GGUF magic')
        version = u32(reader)
        require(version in (2, 3), 'unsupported GGUF version')
        tensor_count = u64(reader)
        metadata_count = u64(reader)
        require(tensor_count == EXPECTED_TENSORS, 'GGUF tensor count mismatch')
        require(metadata_count <= MAX_METADATA, 'GGUF metadata count exceeds limit')
        metadata = []
        alignment = 32
        for ordinal in range(metadata_count):
            key = gguf_string(reader)
            require(key, 'empty GGUF metadata key')
            typ = u32(reader)
            entry = metadata_value(reader, typ)
            entry['key'] = key
            entry['ordinal'] = ordinal
            metadata.append(entry)
            if key == 'general.alignment':
                require(entry['classification'] == 'scalar', 'alignment must be scalar')
                require(entry['gguf_value_type'] == 4, 'alignment must be UINT32')
                alignment = int(entry['value'])
        require(alignment > 0 and alignment <= 1024 * 1024, 'invalid alignment')
        tensors = []
        for ordinal in range(tensor_count):
            name = gguf_string(reader)
            require(name, 'empty tensor name')
            n_dims = u32(reader)
            require(1 <= n_dims <= MAX_DIMS, 'invalid tensor dimension count')
            dims = [u64(reader) for _ in range(n_dims)]
            count = product(dims)
            type_id = u32(reader)
            offset = u64(reader)
            tensors.append({
                'dims': dims,
                'element_count': count,
                'ggml_type': type_id,
                'ggml_type_name': GGML_TYPES.get(type_id, 'TYPE_' + str(type_id)),
                'name': name,
                'ordinal': ordinal,
                'source_relative_data_offset': offset,
            })
        directory_end = reader.pos
        tensor_data_start = align_up(directory_end, alignment)
        require(tensor_data_start <= opened.st_size, 'tensor data boundary beyond source')
        max_source_byte_read = reader.max_end - 1
        require(max_source_byte_read < tensor_data_start, 'source read reached tensor payload boundary')
        return {
            'alignment': alignment,
            'directory_end': directory_end,
            'max_source_byte_read': max_source_byte_read,
            'metadata': metadata,
            'metadata_count': metadata_count,
            'tensor_count': tensor_count,
            'tensor_data_start': tensor_data_start,
            'tensors': tensors,
            'version': version,
        }
    finally:
        os.close(fd)


def build_authority(parsed: dict, inventory: list) -> dict:
    verify_tensor_inventory(parsed['tensors'], inventory)
    return {
        'generation_pk': GENERATION_PK,
        'gguf': {
            'alignment': parsed['alignment'],
            'directory_end': parsed['directory_end'],
            'max_source_byte_read': parsed['max_source_byte_read'],
            'metadata_count': parsed['metadata_count'],
            'tensor_count': parsed['tensor_count'],
            'tensor_data_start': parsed['tensor_data_start'],
            'version': parsed['version'],
        },
        'inventory': {
            'path': str(INVENTORY.relative_to(ROOT)),
            'sha256': INVENTORY_SHA256,
            'tensor_agreement': EXPECTED_TENSORS,
        },
        'llama_cpp_authority': LLAMA_AUTHORITY,
        'metadata': parsed['metadata'],
        'protocol_sha256': PROTOCOL_SHA256,
        'schema': SCHEMA,
        'source': {
            'path': str(SOURCE),
            'sha256_provenance': SOURCE_SHA256_PROVENANCE,
            'stat_size': EXPECTED_SOURCE_SIZE,
        },
        'tensors': parsed['tensors'],
    }


def publish_authority(authority: dict) -> str:
    require(not OUTPUT.exists(), 'authority output already exists')
    building = OUTPUT.with_name(OUTPUT.name + '.building')
    require(not building.exists(), 'authority building path already exists')
    raw = canonical_json_bytes(authority)
    try:
        with building.open('xb') as f:
            f.write(raw)
            f.flush()
            os.fsync(f.fileno())
        reopened = building.read_bytes()
        require(reopened == raw, 'authority byte reopen mismatch')
        require(json.loads(reopened.decode('utf-8')) == authority, 'authority logical reopen mismatch')
        os.replace(building, OUTPUT)
        fsync_directory(OUTPUT.parent)
    finally:
        if building.exists():
            building.unlink()
    require(OUTPUT.read_bytes() == raw, 'published authority byte mismatch')
    return sha256_bytes(raw)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sentinel', required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sentinel = Path(args.sentinel).expanduser()
    require(sentinel.is_absolute(), 'sentinel path must be absolute')
    require(not OUTPUT.exists(), 'authority output already exists')
    inventory = load_inventory()
    pre_stat = source_preflight()
    reserve_sentinel(sentinel)
    parsed = parse_source(pre_stat)
    authority = build_authority(parsed, inventory)
    authority_sha = publish_authority(authority)
    print('CLASS-A GGUF METADATA AUTHORITY QUALIFIED')
    print('AUTHORITY PATH      :', OUTPUT)
    print('AUTHORITY SHA256    :', authority_sha)
    print('METADATA COUNT      :', parsed['metadata_count'])
    print('TENSOR COUNT        :', parsed['tensor_count'])
    print('TENSOR DATA START   :', parsed['tensor_data_start'])
    print('MAX SOURCE BYTE READ:', parsed['max_source_byte_read'])
    print('SOURCE SHA RECOMPUTED: NO')
    print('MODEL LOADED        : NO')
    print('INFERENCE           : NO')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except ExtractionError as exc:
        print('CLASS-A GGUF METADATA AUTHORITY NOT QUALIFIED')
        print('ERROR:', exc)
        raise SystemExit(1)
