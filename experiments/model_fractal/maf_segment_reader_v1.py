"""MAF Segment Reader V1.

Reads one generation-bound serialized object-file range from an already
validated ResidentPKEntry.

This module does not perform catalog discovery, activation discovery,
manifest parsing, payload decoding, descriptor residency, or Phase 6C
runtime management.
"""

from __future__ import annotations

import hashlib
import os
import stat

from maf_resident_pk_directory_v1 import ResidentPKEntry


class MAFSegmentReaderError(RuntimeError):
    """Base error for Segment Reader V1."""


class MAFSegmentReaderInvalidEntryError(MAFSegmentReaderError):
    """The supplied resident entry or reader argument is invalid."""


class MAFSegmentReaderStaleGenerationError(MAFSegmentReaderError):
    """The caller expected a generation different from the resident entry."""


class MAFSegmentReaderInvalidRangeError(MAFSegmentReaderError):
    """The resident entry describes an invalid physical range."""


class MAFSegmentReaderSegmentIOError(MAFSegmentReaderError):
    """The segment could not be opened, inspected, read, or closed."""


class MAFSegmentReaderNonRegularSegmentError(MAFSegmentReaderError):
    """The opened segment target is not a regular file."""


class MAFSegmentReaderSegmentLengthMismatchError(MAFSegmentReaderError):
    """The opened segment length differs from the resident entry."""


class MAFSegmentReaderShortReadError(MAFSegmentReaderError):
    """The positional read returned fewer bytes than requested."""


class MAFSegmentReaderObjectHashMismatchError(MAFSegmentReaderError):
    """The serialized object range does not match object_file_sha256."""


def _require_plain_int(name: str, value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise MAFSegmentReaderInvalidEntryError(
            f"{name} must be an integer"
        )

    return value


def read_serialized_object(
    entry: ResidentPKEntry,
    expected_generation_pk: str,
) -> bytes:
    """Read and verify one serialized object-file range.

    The returned bytes are the physical serialized object bytes addressed by
    ``entry.offset`` and ``entry.length``. Their SHA256 must equal
    ``entry.object_file_sha256``.

    This operation intentionally does not decode or verify payload_sha256.
    """

    if not isinstance(entry, ResidentPKEntry):
        raise MAFSegmentReaderInvalidEntryError(
            "entry must be ResidentPKEntry"
        )

    if not isinstance(expected_generation_pk, str):
        raise MAFSegmentReaderInvalidEntryError(
            "expected_generation_pk must be str"
        )

    if expected_generation_pk != entry.generation_pk:
        raise MAFSegmentReaderStaleGenerationError(
            "resident entry generation does not match expected generation"
        )

    offset = _require_plain_int("offset", entry.offset)
    length = _require_plain_int("length", entry.length)
    segment_length = _require_plain_int(
        "segment_length",
        entry.segment_length,
    )

    if offset < 0 or length < 0 or segment_length < 0:
        raise MAFSegmentReaderInvalidRangeError(
            "negative segment range"
        )

    if offset > segment_length:
        raise MAFSegmentReaderInvalidRangeError(
            "offset exceeds segment length"
        )

    if length > segment_length - offset:
        raise MAFSegmentReaderInvalidRangeError(
            "object range exceeds segment length"
        )

    if not isinstance(entry.segment_path, str) or not entry.segment_path:
        raise MAFSegmentReaderInvalidEntryError(
            "segment_path must be a non-empty string"
        )

    if (
        not isinstance(entry.object_file_sha256, str)
        or not entry.object_file_sha256
    ):
        raise MAFSegmentReaderInvalidEntryError(
            "object_file_sha256 must be a non-empty string"
        )

    flags = os.O_RDONLY

    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC

    try:
        fd = os.open(entry.segment_path, flags)
    except OSError as exc:
        raise MAFSegmentReaderSegmentIOError(
            "segment open failed"
        ) from exc

    try:
        try:
            metadata = os.fstat(fd)
        except OSError as exc:
            raise MAFSegmentReaderSegmentIOError(
                "segment fstat failed"
            ) from exc

        if not stat.S_ISREG(metadata.st_mode):
            raise MAFSegmentReaderNonRegularSegmentError(
                "segment target is not a regular file"
            )

        if metadata.st_size != segment_length:
            raise MAFSegmentReaderSegmentLengthMismatchError(
                "segment length does not match resident entry"
            )

        try:
            serialized_object = os.pread(
                fd,
                length,
                offset,
            )
        except OSError as exc:
            raise MAFSegmentReaderSegmentIOError(
                "segment positional read failed"
            ) from exc

        if len(serialized_object) != length:
            raise MAFSegmentReaderShortReadError(
                "segment positional read returned unexpected length"
            )

        observed_sha256 = hashlib.sha256(
            serialized_object
        ).hexdigest()

        if observed_sha256 != entry.object_file_sha256:
            raise MAFSegmentReaderObjectHashMismatchError(
                "serialized object SHA256 does not match resident entry"
            )

        return serialized_object

    finally:
        try:
            os.close(fd)
        except OSError as exc:
            raise MAFSegmentReaderSegmentIOError(
                "segment descriptor close failed"
            ) from exc


__all__ = [
    "MAFSegmentReaderError",
    "MAFSegmentReaderInvalidEntryError",
    "MAFSegmentReaderStaleGenerationError",
    "MAFSegmentReaderInvalidRangeError",
    "MAFSegmentReaderSegmentIOError",
    "MAFSegmentReaderNonRegularSegmentError",
    "MAFSegmentReaderSegmentLengthMismatchError",
    "MAFSegmentReaderShortReadError",
    "MAFSegmentReaderObjectHashMismatchError",
    "read_serialized_object",
]
