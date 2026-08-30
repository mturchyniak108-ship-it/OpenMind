#!/usr/bin/env python3

"""Persistent OpenMind MAF Object v1 container."""

from __future__ import annotations

import hashlib
import json
import os
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Iterator


SCHEMA = "openmind.maf_object.v1"
ENCODING = "gguf_payload_exact"

MAGIC = b"OMMAFOBJ"
VERSION = 1
FLAGS = 0

HEADER_STRUCT = struct.Struct("<8sIIQQ32s32s")
HEADER_SIZE = HEADER_STRUCT.size

DEFAULT_CHUNK_BYTES = 4 * 1024 * 1024


class MAFObjectError(RuntimeError):
    pass


@dataclass(frozen=True)
class ObjectView:
    path: Path
    tensor_name: str
    tensor_type: str
    dims: tuple[int, ...]
    element_count: int
    payload_offset: int
    payload_length: int
    payload_sha256: str
    metadata_sha256: str


def canonical_json_bytes(value: dict) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_sha256_text(value: str) -> None:
    if len(value) != 64:
        raise MAFObjectError(
            "SHA256 must contain 64 hex characters"
        )

    try:
        raw = bytes.fromhex(value)
    except ValueError as exc:
        raise MAFObjectError(
            "SHA256 is not hexadecimal"
        ) from exc

    if len(raw) != 32:
        raise MAFObjectError(
            "SHA256 decoded length is not 32 bytes"
        )


def checked_element_count(
    dims: list[int] | tuple[int, ...],
) -> int:
    if not dims:
        raise MAFObjectError(
            "tensor dimensions must not be empty"
        )

    total = 1

    for dim in dims:
        if isinstance(dim, bool) or not isinstance(dim, int):
            raise MAFObjectError(
                f"invalid tensor dimension: {dim!r}"
            )

        if dim <= 0:
            raise MAFObjectError(
                f"tensor dimension must be positive: {dim}"
            )

        total *= dim

        if total > 0x7FFFFFFFFFFFFFFF:
            raise MAFObjectError(
                "tensor element count exceeds int64"
            )

    return total


def iter_exact(
    stream: BinaryIO,
    length: int,
    chunk_bytes: int = DEFAULT_CHUNK_BYTES,
) -> Iterator[bytes]:
    if length < 0:
        raise MAFObjectError(
            "negative stream length"
        )

    if chunk_bytes <= 0:
        raise MAFObjectError(
            "chunk size must be positive"
        )

    remaining = length

    while remaining:
        want = min(remaining, chunk_bytes)
        chunk = stream.read(want)

        if len(chunk) != want:
            raise MAFObjectError(
                "truncated stream: "
                f"wanted {want}, received {len(chunk)}"
            )

        yield chunk
        remaining -= len(chunk)


def build_metadata(
    *,
    tensor_name: str,
    tensor_type: str,
    dims: list[int] | tuple[int, ...],
    payload_length: int,
    payload_sha256: str,
    provenance: dict | None = None,
) -> dict:
    if not tensor_name:
        raise MAFObjectError(
            "tensor name must not be empty"
        )

    if not tensor_type:
        raise MAFObjectError(
            "tensor type must not be empty"
        )

    if payload_length < 0:
        raise MAFObjectError(
            "negative payload length"
        )

    validate_sha256_text(payload_sha256)

    normalized_dims = list(dims)
    element_count = checked_element_count(
        normalized_dims
    )

    metadata = {
        "dims": normalized_dims,
        "element_count": element_count,
        "encoding": ENCODING,
        "payload_length": payload_length,
        "payload_sha256": payload_sha256,
        "schema": SCHEMA,
        "tensor_name": tensor_name,
        "tensor_type": tensor_type,
    }

    if provenance is not None:
        metadata["provenance"] = provenance

    return metadata


def pack_header(
    *,
    metadata_length: int,
    payload_length: int,
    metadata_sha256: str,
    payload_sha256: str,
) -> bytes:
    if not 0 <= metadata_length <= 0xFFFFFFFF:
        raise MAFObjectError(
            "metadata length exceeds uint32"
        )

    if not 0 <= payload_length <= 0xFFFFFFFFFFFFFFFF:
        raise MAFObjectError(
            "payload length exceeds uint64"
        )

    validate_sha256_text(metadata_sha256)
    validate_sha256_text(payload_sha256)

    return HEADER_STRUCT.pack(
        MAGIC,
        VERSION,
        metadata_length,
        payload_length,
        FLAGS,
        bytes.fromhex(metadata_sha256),
        bytes.fromhex(payload_sha256),
    )


def unpack_header(raw: bytes) -> dict:
    if len(raw) != HEADER_SIZE:
        raise MAFObjectError(
            f"invalid header length: {len(raw)}"
        )

    (
        magic,
        version,
        metadata_length,
        payload_length,
        flags,
        metadata_digest,
        payload_digest,
    ) = HEADER_STRUCT.unpack(raw)

    if magic != MAGIC:
        raise MAFObjectError(
            f"invalid magic: {magic!r}"
        )

    if version != VERSION:
        raise MAFObjectError(
            f"unsupported version: {version}"
        )

    if flags != FLAGS:
        raise MAFObjectError(
            f"unsupported flags: {flags}"
        )

    return {
        "metadata_length": metadata_length,
        "payload_length": payload_length,
        "metadata_sha256": metadata_digest.hex(),
        "payload_sha256": payload_digest.hex(),
    }


def validate_metadata(
    metadata: dict,
    header: dict,
) -> None:
    required = {
        "dims",
        "element_count",
        "encoding",
        "payload_length",
        "payload_sha256",
        "schema",
        "tensor_name",
        "tensor_type",
    }

    missing = required.difference(metadata)

    if missing:
        raise MAFObjectError(
            "missing metadata fields: "
            + ", ".join(sorted(missing))
        )

    if metadata["schema"] != SCHEMA:
        raise MAFObjectError(
            "unexpected metadata schema"
        )

    if metadata["encoding"] != ENCODING:
        raise MAFObjectError(
            "unexpected payload encoding"
        )

    if not isinstance(metadata["dims"], list):
        raise MAFObjectError(
            "metadata dims must be a list"
        )

    expected_elements = checked_element_count(
        metadata["dims"]
    )

    if metadata["element_count"] != expected_elements:
        raise MAFObjectError(
            "element-count mismatch"
        )

    if (
        metadata["payload_length"]
        != header["payload_length"]
    ):
        raise MAFObjectError(
            "payload-length metadata/header mismatch"
        )

    if (
        metadata["payload_sha256"]
        != header["payload_sha256"]
    ):
        raise MAFObjectError(
            "payload-hash metadata/header mismatch"
        )


def inspect_object(
    path: Path,
    *,
    chunk_bytes: int = DEFAULT_CHUNK_BYTES,
) -> ObjectView:
    path = Path(path)

    with path.open("rb") as stream:
        header = unpack_header(
            stream.read(HEADER_SIZE)
        )

        metadata_raw = stream.read(
            header["metadata_length"]
        )

        if len(metadata_raw) != header["metadata_length"]:
            raise MAFObjectError(
                "truncated metadata"
            )

        metadata_sha256 = sha256_bytes(
            metadata_raw
        )

        if (
            metadata_sha256
            != header["metadata_sha256"]
        ):
            raise MAFObjectError(
                "metadata SHA256 mismatch"
            )

        try:
            metadata = json.loads(
                metadata_raw.decode("utf-8")
            )
        except (
            UnicodeDecodeError,
            json.JSONDecodeError,
        ) as exc:
            raise MAFObjectError(
                "invalid metadata JSON"
            ) from exc

        if canonical_json_bytes(metadata) != metadata_raw:
            raise MAFObjectError(
                "metadata is not canonical JSON"
            )

        validate_metadata(
            metadata,
            header,
        )

        payload_offset = stream.tell()
        digest = hashlib.sha256()
        payload_count = 0

        for chunk in iter_exact(
            stream,
            header["payload_length"],
            chunk_bytes,
        ):
            digest.update(chunk)
            payload_count += len(chunk)

        if payload_count != header["payload_length"]:
            raise MAFObjectError(
                "payload byte-count mismatch"
            )

        payload_sha256 = digest.hexdigest()

        if payload_sha256 != header["payload_sha256"]:
            raise MAFObjectError(
                "payload SHA256 mismatch"
            )

        if stream.read(1):
            raise MAFObjectError(
                "unexpected trailing bytes"
            )

    return ObjectView(
        path=path,
        tensor_name=metadata["tensor_name"],
        tensor_type=metadata["tensor_type"],
        dims=tuple(metadata["dims"]),
        element_count=metadata["element_count"],
        payload_offset=payload_offset,
        payload_length=header["payload_length"],
        payload_sha256=payload_sha256,
        metadata_sha256=metadata_sha256,
    )


def compile_object(
    *,
    source_path: Path,
    source_file_start: int,
    tensor_name: str,
    tensor_type: str,
    dims: list[int] | tuple[int, ...],
    payload_length: int,
    expected_payload_sha256: str,
    output_path: Path,
    provenance: dict | None = None,
    chunk_bytes: int = DEFAULT_CHUNK_BYTES,
) -> ObjectView:
    source_path = Path(source_path)
    output_path = Path(output_path)

    if source_file_start < 0:
        raise MAFObjectError(
            "negative source file position"
        )

    if payload_length < 0:
        raise MAFObjectError(
            "negative payload length"
        )

    metadata = build_metadata(
        tensor_name=tensor_name,
        tensor_type=tensor_type,
        dims=dims,
        payload_length=payload_length,
        payload_sha256=expected_payload_sha256,
        provenance=provenance,
    )

    metadata_raw = canonical_json_bytes(
        metadata
    )

    metadata_sha256 = sha256_bytes(
        metadata_raw
    )

    header = pack_header(
        metadata_length=len(metadata_raw),
        payload_length=payload_length,
        metadata_sha256=metadata_sha256,
        payload_sha256=expected_payload_sha256,
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    partial_path = output_path.with_name(
        output_path.name + ".partial"
    )

    if output_path.exists():
        raise MAFObjectError(
            f"final object already exists: {output_path}"
        )

    if partial_path.exists():
        raise MAFObjectError(
            "partial object already exists: "
            f"{partial_path}"
        )

    copied = 0
    payload_digest = hashlib.sha256()

    try:
        with source_path.open("rb") as source, \
                partial_path.open("xb") as target:

            source_size = os.fstat(
                source.fileno()
            ).st_size

            end = (
                source_file_start
                + payload_length
            )

            if end < source_file_start:
                raise MAFObjectError(
                    "source-span arithmetic overflow"
                )

            if end > source_size:
                raise MAFObjectError(
                    "source tensor span exceeds file"
                )

            source.seek(
                source_file_start
            )

            target.write(header)
            target.write(metadata_raw)

            for chunk in iter_exact(
                source,
                payload_length,
                chunk_bytes,
            ):
                target.write(chunk)
                payload_digest.update(chunk)
                copied += len(chunk)

            if copied != payload_length:
                raise MAFObjectError(
                    "compiled byte-count mismatch"
                )

            actual_sha256 = (
                payload_digest.hexdigest()
            )

            if (
                actual_sha256
                != expected_payload_sha256
            ):
                raise MAFObjectError(
                    "source payload SHA256 mismatch"
                )

            target.flush()
            os.fsync(
                target.fileno()
            )

        view = inspect_object(
            partial_path,
            chunk_bytes=chunk_bytes,
        )

        if (
            view.payload_sha256
            != expected_payload_sha256
        ):
            raise MAFObjectError(
                "independent reopen hash mismatch"
            )

        os.replace(
            partial_path,
            output_path,
        )

        return ObjectView(
            path=output_path,
            tensor_name=view.tensor_name,
            tensor_type=view.tensor_type,
            dims=view.dims,
            element_count=view.element_count,
            payload_offset=view.payload_offset,
            payload_length=view.payload_length,
            payload_sha256=view.payload_sha256,
            metadata_sha256=view.metadata_sha256,
        )

    except Exception:
        if partial_path.exists():
            partial_path.unlink()
        raise


def compare_payload_to_source(
    *,
    object_path: Path,
    source_path: Path,
    source_file_start: int,
    chunk_bytes: int = DEFAULT_CHUNK_BYTES,
) -> bool:
    if source_file_start < 0:
        raise MAFObjectError(
            "negative source file position"
        )

    view = inspect_object(
        Path(object_path),
        chunk_bytes=chunk_bytes,
    )

    with Path(source_path).open("rb") as source, \
            Path(object_path).open("rb") as obj:

        source_size = os.fstat(
            source.fileno()
        ).st_size

        end = (
            source_file_start
            + view.payload_length
        )

        if end < source_file_start:
            raise MAFObjectError(
                "comparison arithmetic overflow"
            )

        if end > source_size:
            raise MAFObjectError(
                "comparison span exceeds source file"
            )

        source.seek(
            source_file_start
        )

        obj.seek(
            view.payload_offset
        )

        remaining = view.payload_length

        while remaining:
            want = min(
                remaining,
                chunk_bytes,
            )

            source_chunk = source.read(
                want
            )
            object_chunk = obj.read(
                want
            )

            if len(source_chunk) != want:
                raise MAFObjectError(
                    "truncated comparison source"
                )

            if len(object_chunk) != want:
                raise MAFObjectError(
                    "truncated comparison object"
                )

            if source_chunk != object_chunk:
                return False

            remaining -= want

    return True
