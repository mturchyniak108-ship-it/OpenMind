#!/usr/bin/env python3
"""Exact-once functional validation for MAF Segment Reader V1."""

from __future__ import annotations

import ast
import dataclasses
import hashlib
import json
import os
import shutil
import sys
from dataclasses import FrozenInstanceError
from pathlib import Path
from typing import Any

import maf_segment_reader_v1 as reader
from maf_resident_pk_directory_v1 import ResidentPKEntry


SCHEMA = "openmind.maf_segment_reader_validation.v1"
VERSION = "maf_segment_reader_validation_v1"

PROTOCOL = Path(
    "experiments/model_fractal/"
    "MAF_SEGMENT_READER_VALIDATION_V1_PROTOCOL.md"
)

ENGINE = Path(
    "experiments/model_fractal/maf_segment_reader_v1.py"
)

SOURCE_RUNTIME = Path(
    "results/runtime/"
    "maf_resident_pk_directory_benchmark_v1_1"
)

SOURCE_MANIFEST = (
    SOURCE_RUNTIME / "candidate_a.manifest.json"
)

RESULT = Path(
    "experiments/model_fractal/"
    "maf_segment_reader_validation_v1.json"
)

RUNTIME = Path(
    "results/runtime/"
    "maf_segment_reader_validation_v1"
)

FD_REPEAT = 100

EXPECTED_PROTOCOL_SHA256 = "c896e6b68be67352e4b09ed8f6486cdea2e20435fa03c7c44fd4871051e202be"
EXPECTED_ENGINE_SHA256 = "3499cb8e528fe8e9315e3e5656d6aa888c95ca175310b6371e722de409827369"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write_json_exclusive(path: Path, data: dict[str, Any]) -> None:
    encoded = json.dumps(
        data,
        indent=2,
        sort_keys=True,
    ) + "\n"

    with path.open(
        "x",
        encoding="utf-8",
        newline="\n",
    ) as f:
        f.write(encoded)


def fd_count() -> int | None:
    root = Path("/proc/self/fd")

    if not root.is_dir():
        return None

    try:
        return len(list(root.iterdir()))
    except OSError:
        return None


def expect_exception(
    expected_type: type[BaseException],
    operation,
) -> tuple[bool, str]:
    try:
        operation()
    except Exception as exc:
        return (
            isinstance(exc, expected_type),
            type(exc).__name__,
        )

    return False, "NO_EXCEPTION"


def resolve_entries() -> tuple[list[ResidentPKEntry], dict[str, bytes], str]:
    manifest_raw = SOURCE_MANIFEST.read_bytes()
    manifest_sha = sha256_bytes(manifest_raw)
    manifest = json.loads(
        manifest_raw.decode("utf-8")
    )

    descriptor = manifest["descriptor"]
    generation_pk = manifest["generation_pk"]

    model_pk = descriptor["model_pk"]

    segments = {
        item["segment_id"]: item
        for item in descriptor["segments"]
    }

    segment_paths: dict[str, Path] = {}
    segment_bytes: dict[str, bytes] = {}

    for segment_id, segment in segments.items():
        expected_length = segment["segment_length"]
        expected_sha = segment["segment_sha256"]

        matches = []

        for path in sorted(
            SOURCE_RUNTIME.rglob("*.mafseg")
        ):
            if path.stat().st_size != expected_length:
                continue

            raw = path.read_bytes()

            if sha256_bytes(raw) == expected_sha:
                matches.append((path, raw))

        if matches:
            segment_paths[segment_id] = matches[0][0]
            segment_bytes[segment_id] = matches[0][1]

    entries = []

    for obj in descriptor["objects"]:
        segment_id = obj["segment_id"]

        if segment_id not in segment_paths:
            continue

        segment = segments[segment_id]

        entries.append(
            ResidentPKEntry(
                model_pk=model_pk,
                generation_pk=generation_pk,
                generation_manifest_sha256=manifest_sha,
                object_pk=obj["object_pk"],
                segment_id=segment_id,
                offset=obj["offset"],
                length=obj["length"],
                object_file_sha256=obj[
                    "object_file_sha256"
                ],
                payload_sha256=obj[
                    "payload_sha256"
                ],
                segment_length=segment[
                    "segment_length"
                ],
                segment_sha256=segment[
                    "segment_sha256"
                ],
                segment_path=str(
                    segment_paths[segment_id]
                ),
            )
        )

    return entries, segment_bytes, manifest_sha


class ShortReadOS:
    def __init__(self, base):
        self._base = base

    def __getattr__(self, name):
        return getattr(self._base, name)

    def pread(self, fd, length, offset):
        return b""


class TrackingOS:
    def __init__(self, base):
        self._base = base
        self.open_flags = []

    def __getattr__(self, name):
        return getattr(self._base, name)

    def open(self, path, flags, *args):
        self.open_flags.append(flags)
        return self._base.open(
            path,
            flags,
            *args,
        )


def run_static_checks() -> dict[str, bool]:
    text = ENGINE.read_text(
        encoding="utf-8"
    )

    tree = ast.parse(
        text,
        filename=str(ENGINE),
    )

    functions = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }

    function = functions[
        "read_serialized_object"
    ]

    source = (
        ast.get_source_segment(
            text,
            function,
        )
        or ""
    )

    generation_pos = source.find(
        "expected_generation_pk != entry.generation_pk"
    )

    range_pos = source.find(
        "length > segment_length - offset"
    )

    open_pos = source.find(
        "os.open("
    )

    same_fd = all(
        token in source
        for token in (
            "os.fstat(fd)",
            "os.pread(",
            "os.close(fd)",
        )
    )

    no_json_manifest_gguf = (
        "json" not in source.lower()
        and "manifest" not in source.lower()
        and ".gguf" not in source.lower()
    )

    no_write = all(
        token not in source
        for token in (
            "O_WRONLY",
            "O_RDWR",
            "O_CREAT",
            "O_TRUNC",
            "O_APPEND",
            ".write(",
            "write_bytes(",
        )
    )

    no_residency = all(
        token not in source.lower()
        for token in (
            "cache",
            "mmap",
            "resident_files",
            "fd_pool",
        )
    )

    return {
        "static_generation_before_open":
            0 <= generation_pos < open_pos,

        "static_range_before_open":
            0 <= range_pos < open_pos,

        "static_same_fd_fstat_pread":
            same_fd,

        "static_object_hash_only":
            "entry.object_file_sha256"
            in source,

        "static_no_payload_hash":
            "entry.payload_sha256"
            not in source,

        "static_no_whole_segment_hash":
            "entry.segment_sha256"
            not in source,

        "static_no_json_manifest_gguf":
            no_json_manifest_gguf,

        "static_no_write_api":
            no_write,

        "static_no_residency":
            no_residency,
    }


def run_validation() -> dict[str, Any]:
    checks: dict[str, bool] = {}
    observations: dict[str, Any] = {}

    protocol_sha = sha256_file(PROTOCOL)
    engine_sha = sha256_file(ENGINE)

    checks["protocol_identity"] = (
        protocol_sha
        == EXPECTED_PROTOCOL_SHA256
    )

    checks["engine_identity"] = (
        engine_sha
        == EXPECTED_ENGINE_SHA256
    )

    source_manifest_before = sha256_file(
        SOURCE_MANIFEST
    )

    entries, segment_bytes, manifest_sha = (
        resolve_entries()
    )

    if len(entries) < 2:
        raise RuntimeError(
            "fewer than two resolvable objects"
        )

    selected = entries[:3]

    offsets = {
        entry.offset
        for entry in selected
    }

    checks["positive_multiple_offsets"] = (
        len(selected) >= 2
        and len(offsets) >= 2
    )

    expected_bytes = []

    returned_bytes = []

    for entry in selected:
        raw = segment_bytes[
            entry.segment_id
        ]

        expected = raw[
            entry.offset:
            entry.offset + entry.length
        ]

        expected_bytes.append(expected)

        returned = reader.read_serialized_object(
            entry,
            entry.generation_pk,
        )

        returned_bytes.append(returned)

    checks["positive_exact_bytes"] = all(
        actual == expected
        for actual, expected in zip(
            returned_bytes,
            expected_bytes,
        )
    )

    checks["positive_exact_lengths"] = all(
        len(actual) == entry.length
        for actual, entry in zip(
            returned_bytes,
            selected,
        )
    )

    checks["positive_object_hashes"] = all(
        sha256_bytes(actual)
        == entry.object_file_sha256
        for actual, entry in zip(
            returned_bytes,
            selected,
        )
    )

    checks["positive_not_payload_hash"] = all(
        sha256_bytes(actual)
        != entry.payload_sha256
        for actual, entry in zip(
            returned_bytes,
            selected,
        )
    )

    base = selected[0]

    missing_path = (
        RUNTIME / "missing.mafseg"
    )

    stale_generation = (
        base.generation_pk[:-1]
        + (
            "0"
            if base.generation_pk[-1] != "0"
            else "1"
        )
    )

    stale_missing = dataclasses.replace(
        base,
        segment_path=str(missing_path),
    )

    ok, observed = expect_exception(
        reader.MAFSegmentReaderStaleGenerationError,
        lambda: reader.read_serialized_object(
            stale_missing,
            stale_generation,
        ),
    )

    checks[
        "generation_mismatch_before_io"
    ] = ok

    observations[
        "generation_mismatch_exception"
    ] = observed

    ok, observed = expect_exception(
        reader.MAFSegmentReaderInvalidEntryError,
        lambda: reader.read_serialized_object(
            object(),
            base.generation_pk,
        ),
    )

    checks["invalid_entry_rejected"] = ok
    observations["invalid_entry_exception"] = observed

    ok, observed = expect_exception(
        reader.MAFSegmentReaderInvalidEntryError,
        lambda: reader.read_serialized_object(
            base,
            123,
        ),
    )

    checks[
        "invalid_generation_type_rejected"
    ] = ok

    observations[
        "invalid_generation_type_exception"
    ] = observed

    range_cases = [
        (
            "negative_offset_rejected",
            dataclasses.replace(
                base,
                offset=-1,
            ),
        ),
        (
            "negative_length_rejected",
            dataclasses.replace(
                base,
                length=-1,
            ),
        ),
        (
            "negative_segment_length_rejected",
            dataclasses.replace(
                base,
                segment_length=-1,
            ),
        ),
        (
            "offset_past_segment_rejected",
            dataclasses.replace(
                base,
                offset=base.segment_length + 1,
                length=0,
            ),
        ),
        (
            "upper_bound_rejected",
            dataclasses.replace(
                base,
                length=(
                    base.segment_length
                    - base.offset
                    + 1
                ),
            ),
        ),
    ]

    for name, entry in range_cases:
        ok, observed = expect_exception(
            reader.MAFSegmentReaderInvalidRangeError,
            lambda entry=entry:
                reader.read_serialized_object(
                    entry,
                    entry.generation_pk,
                ),
        )

        checks[name] = ok
        observations[
            name + "_exception"
        ] = observed

    empty_path = dataclasses.replace(
        base,
        segment_path="",
    )

    ok, observed = expect_exception(
        reader.MAFSegmentReaderInvalidEntryError,
        lambda: reader.read_serialized_object(
            empty_path,
            empty_path.generation_pk,
        ),
    )

    checks["empty_segment_path_rejected"] = ok
    observations["empty_segment_path_exception"] = observed

    empty_hash = dataclasses.replace(
        base,
        object_file_sha256="",
    )

    ok, observed = expect_exception(
        reader.MAFSegmentReaderInvalidEntryError,
        lambda: reader.read_serialized_object(
            empty_hash,
            empty_hash.generation_pk,
        ),
    )

    checks["empty_object_hash_rejected"] = ok
    observations["empty_object_hash_exception"] = observed

    missing_entry = dataclasses.replace(
        base,
        segment_path=str(missing_path),
    )

    ok, observed = expect_exception(
        reader.MAFSegmentReaderSegmentIOError,
        lambda: reader.read_serialized_object(
            missing_entry,
            missing_entry.generation_pk,
        ),
    )

    checks["missing_segment_rejected"] = ok
    observations["missing_segment_exception"] = observed

    nonregular_entry = dataclasses.replace(
        base,
        segment_path=str(RUNTIME),
    )

    ok, observed = expect_exception(
        reader.MAFSegmentReaderNonRegularSegmentError,
        lambda: reader.read_serialized_object(
            nonregular_entry,
            nonregular_entry.generation_pk,
        ),
    )

    checks["nonregular_segment_rejected"] = ok
    observations["nonregular_segment_exception"] = observed

    source_segment = Path(
        base.segment_path
    )

    length_bad_path = (
        RUNTIME / "length_bad.mafseg"
    )

    shutil.copyfile(
        source_segment,
        length_bad_path,
    )

    with length_bad_path.open("ab") as f:
        f.write(b"\x00")

    length_bad_entry = dataclasses.replace(
        base,
        segment_path=str(length_bad_path),
    )

    ok, observed = expect_exception(
        reader.MAFSegmentReaderSegmentLengthMismatchError,
        lambda: reader.read_serialized_object(
            length_bad_entry,
            length_bad_entry.generation_pk,
        ),
    )

    checks["segment_length_mismatch_rejected"] = ok
    observations["segment_length_mismatch_exception"] = observed

    original_os = reader.os

    try:
        reader.os = ShortReadOS(original_os)

        ok, observed = expect_exception(
            reader.MAFSegmentReaderShortReadError,
            lambda: reader.read_serialized_object(
                base,
                base.generation_pk,
            ),
        )
    finally:
        reader.os = original_os

    checks["short_read_rejected"] = ok
    observations["short_read_exception"] = observed

    corrupt_path = (
        RUNTIME / "corrupt_object.mafseg"
    )

    corrupt = bytearray(
        source_segment.read_bytes()
    )

    if base.length <= 0:
        raise RuntimeError(
            "positive object length is zero"
        )

    corrupt[
        base.offset
    ] ^= 0x01

    corrupt_path.write_bytes(
        bytes(corrupt)
    )

    corrupt_entry = dataclasses.replace(
        base,
        segment_path=str(corrupt_path),
    )

    ok, observed = expect_exception(
        reader.MAFSegmentReaderObjectHashMismatchError,
        lambda: reader.read_serialized_object(
            corrupt_entry,
            corrupt_entry.generation_pk,
        ),
    )

    checks["corrupted_object_rejected"] = ok
    observations["corrupted_object_exception"] = observed

    wrong_hash_entry = dataclasses.replace(
        base,
        object_file_sha256="0" * 64,
    )

    ok, observed = expect_exception(
        reader.MAFSegmentReaderObjectHashMismatchError,
        lambda: reader.read_serialized_object(
            wrong_hash_entry,
            wrong_hash_entry.generation_pk,
        ),
    )

    checks["wrong_object_hash_rejected"] = ok
    observations["wrong_object_hash_exception"] = observed

    try:
        base.offset = base.offset + 1
    except FrozenInstanceError:
        frozen = True
    else:
        frozen = False

    checks["resident_entry_frozen"] = frozen

    before_entry = dataclasses.astuple(base)

    reader.read_serialized_object(
        base,
        base.generation_pk,
    )

    after_entry = dataclasses.astuple(base)

    checks[
        "entry_unchanged_after_read"
    ] = before_entry == after_entry

    fd_supported = (
        fd_count() is not None
    )

    observations[
        "fd_measurement_supported"
    ] = fd_supported

    def repeated_fd_check(operation):
        before = fd_count()

        if before is None:
            return True, None, None

        for _ in range(FD_REPEAT):
            operation()

        after = fd_count()

        return (
            after == before,
            before,
            after,
        )

    balanced, before, after = repeated_fd_check(
        lambda: reader.read_serialized_object(
            base,
            base.generation_pk,
        )
    )

    checks["fd_success_balanced"] = balanced

    observations["fd_success_before"] = before
    observations["fd_success_after"] = after

    def hash_failure_operation():
        ok, _ = expect_exception(
            reader.MAFSegmentReaderObjectHashMismatchError,
            lambda: reader.read_serialized_object(
                wrong_hash_entry,
                wrong_hash_entry.generation_pk,
            ),
        )

        if not ok:
            raise RuntimeError(
                "unexpected hash-failure exception"
            )

    balanced, before, after = repeated_fd_check(
        hash_failure_operation
    )

    checks[
        "fd_hash_failure_balanced"
    ] = balanced

    observations[
        "fd_hash_failure_before"
    ] = before

    observations[
        "fd_hash_failure_after"
    ] = after

    def nonregular_failure_operation():
        ok, _ = expect_exception(
            reader.MAFSegmentReaderNonRegularSegmentError,
            lambda: reader.read_serialized_object(
                nonregular_entry,
                nonregular_entry.generation_pk,
            ),
        )

        if not ok:
            raise RuntimeError(
                "unexpected nonregular exception"
            )

    balanced, before, after = repeated_fd_check(
        nonregular_failure_operation
    )

    checks[
        "fd_nonregular_failure_balanced"
    ] = balanced

    observations[
        "fd_nonregular_before"
    ] = before

    observations[
        "fd_nonregular_after"
    ] = after

    original_os = reader.os
    tracker = TrackingOS(original_os)

    try:
        reader.os = tracker

        tracked_result = reader.read_serialized_object(
            base,
            base.generation_pk,
        )
    finally:
        reader.os = original_os

    prohibited_flags = 0

    for name in (
        "O_WRONLY",
        "O_RDWR",
        "O_CREAT",
        "O_TRUNC",
        "O_APPEND",
    ):
        prohibited_flags |= getattr(
            original_os,
            name,
            0,
        )

    checks["reader_opened_read_only"] = (
        tracked_result
        == expected_bytes[0]
        and bool(tracker.open_flags)
        and all(
            flags & prohibited_flags == 0
            for flags in tracker.open_flags
        )
    )

    observations[
        "reader_open_flags"
    ] = tracker.open_flags

    checks.update(
        run_static_checks()
    )

    source_manifest_after = sha256_file(
        SOURCE_MANIFEST
    )

    source_segment_after = sha256_file(
        source_segment
    )

    checks[
        "preserved_sources_unchanged"
    ] = (
        source_manifest_before
        == source_manifest_after
        and source_segment_after
        == base.segment_sha256
    )

    observations[
        "source_manifest_sha256"
    ] = source_manifest_after

    observations[
        "source_segment_sha256"
    ] = source_segment_after

    observations[
        "positive_object_count"
    ] = len(selected)

    observations[
        "positive_offsets"
    ] = [
        entry.offset
        for entry in selected
    ]

    observations[
        "fd_repeat"
    ] = FD_REPEAT

    return {
        "schema": SCHEMA,
        "version": VERSION,
        "protocol_sha256": protocol_sha,
        "engine_sha256": engine_sha,
        "checks": checks,
        "observations": observations,
        "fatal_error": None,
        "all_pass": all(
            checks.values()
        ),
    }


def fatal_result(exc: BaseException) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "version": VERSION,
        "protocol_sha256": (
            sha256_file(PROTOCOL)
            if PROTOCOL.exists()
            else None
        ),
        "engine_sha256": (
            sha256_file(ENGINE)
            if ENGINE.exists()
            else None
        ),
        "checks": {},
        "observations": {},
        "fatal_error": {
            "type": type(exc).__name__,
            "message": str(exc),
        },
        "all_pass": False,
    }


def main() -> int:
    if RESULT.exists():
        raise RuntimeError(
            "validation result already exists"
        )

    if RUNTIME.exists():
        raise RuntimeError(
            "validation runtime already exists"
        )

    if sha256_file(PROTOCOL) != EXPECTED_PROTOCOL_SHA256:
        raise RuntimeError(
            "validation protocol identity mismatch"
        )

    if sha256_file(ENGINE) != EXPECTED_ENGINE_SHA256:
        raise RuntimeError(
            "Segment Reader engine identity mismatch"
        )

    RUNTIME.mkdir(
        parents=True,
        exist_ok=False,
    )

    try:
        result = run_validation()
    except Exception as exc:
        result = fatal_result(exc)

    write_json_exclusive(
        RESULT,
        result,
    )

    print(
        "all_pass:",
        result["all_pass"],
    )

    print(
        "fatal_error:",
        result["fatal_error"],
    )

    return (
        0
        if result["all_pass"]
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
