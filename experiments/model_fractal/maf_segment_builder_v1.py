#!/usr/bin/env python3

"""OpenMind MAF Segment Builder v1."""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from maf_object_v1 import (
    DEFAULT_CHUNK_BYTES,
    ObjectView,
    inspect_object,
)


SCHEMA = "openmind.maf_segment_builder.v1"
BUILDER_VERSION = "maf_segment_builder_v1"

MANIFEST_SCHEMA = "openmind.maf_segment_manifest.v1"
PLACEMENT_POLICY = "sequential_exact_object_pack"

MODEL_PK_RE = re.compile(
    r"^mafmodel:v1:[0-9a-f]{64}$"
)

OBJECT_PK_RE = re.compile(
    r"^mafobj:v1:[0-9a-f]{64}$"
)

SHA256_RE = re.compile(
    r"^[0-9a-f]{64}$"
)


class MAFSegmentBuilderError(RuntimeError):
    pass


@dataclass(frozen=True)
class ValidatedInput:
    model_pk: str
    object_pk: str
    object_path: Path
    object_length: int
    object_view: ObjectView
    expected_object_file_sha256: str | None
    expected_payload_sha256: str | None


@dataclass(frozen=True)
class SegmentBuildResult:
    schema: str
    builder_version: str
    model_pk: str
    segment_path: Path
    manifest_path: Path
    segment_length: int
    segment_sha256: str
    manifest: dict


def _canonical_json_bytes(value: dict) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _require_nonempty_text(
    value: Any,
    label: str,
) -> str:
    if (
        not isinstance(value, str)
        or not value
    ):
        raise MAFSegmentBuilderError(
            f"{label} must be non-empty text"
        )

    return value


def _validate_model_pk(value: Any) -> str:
    value = _require_nonempty_text(
        value,
        "model_pk",
    )

    if MODEL_PK_RE.fullmatch(value) is None:
        raise MAFSegmentBuilderError(
            "invalid model_pk"
        )

    return value


def _validate_object_pk(
    value: Any,
    label: str = "object_pk",
) -> str:
    value = _require_nonempty_text(
        value,
        label,
    )

    if OBJECT_PK_RE.fullmatch(value) is None:
        raise MAFSegmentBuilderError(
            f"invalid {label}"
        )

    return value


def _validate_optional_sha256(
    value: Any,
    label: str,
) -> str | None:
    if value is None:
        return None

    value = _require_nonempty_text(
        value,
        label,
    )

    if SHA256_RE.fullmatch(value) is None:
        raise MAFSegmentBuilderError(
            f"invalid {label}"
        )

    return value


def _validate_chunk_bytes(
    chunk_bytes: Any,
) -> int:
    if (
        not isinstance(chunk_bytes, int)
        or isinstance(chunk_bytes, bool)
        or chunk_bytes <= 0
    ):
        raise MAFSegmentBuilderError(
            "chunk_bytes must be a positive integer"
        )

    return chunk_bytes


def _normalized_path(path: Path) -> Path:
    return Path(path).expanduser().resolve(
        strict=False
    )


def _validate_input_record(
    record: Any,
    *,
    expected_model_pk: str,
    chunk_bytes: int,
) -> ValidatedInput:
    if not isinstance(record, dict):
        raise MAFSegmentBuilderError(
            "object record must be a dict"
        )

    required = {
        "model_pk",
        "object_pk",
        "object_path",
    }

    missing = required.difference(record)

    if missing:
        raise MAFSegmentBuilderError(
            "missing object record fields: "
            + ", ".join(sorted(missing))
        )

    record_model_pk = _validate_model_pk(
        record["model_pk"]
    )

    if record_model_pk != expected_model_pk:
        raise MAFSegmentBuilderError(
            "mixed-model segment request"
        )

    object_pk = _validate_object_pk(
        record["object_pk"]
    )

    object_path_text = _require_nonempty_text(
        record["object_path"],
        "object_path",
    )

    object_path = Path(
        object_path_text
    )

    if not object_path.exists():
        raise MAFSegmentBuilderError(
            f"object does not exist: {object_path}"
        )

    if not object_path.is_file():
        raise MAFSegmentBuilderError(
            f"object is not a regular file: {object_path}"
        )

    object_length = object_path.stat().st_size

    if object_length <= 0:
        raise MAFSegmentBuilderError(
            f"object is empty: {object_path}"
        )

    expected_object_file_sha256 = (
        _validate_optional_sha256(
            record.get(
                "object_file_sha256"
            ),
            "object_file_sha256",
        )
    )

    expected_payload_sha256 = (
        _validate_optional_sha256(
            record.get(
                "payload_sha256"
            ),
            "payload_sha256",
        )
    )

    try:
        view = inspect_object(
            object_path,
            chunk_bytes=chunk_bytes,
        )
    except Exception as exc:
        raise MAFSegmentBuilderError(
            f"invalid MAF Object V1: {object_path}"
        ) from exc

    if (
        expected_payload_sha256 is not None
        and view.payload_sha256
        != expected_payload_sha256
    ):
        raise MAFSegmentBuilderError(
            "expected payload SHA256 mismatch"
        )

    return ValidatedInput(
        model_pk=record_model_pk,
        object_pk=object_pk,
        object_path=object_path,
        object_length=object_length,
        object_view=view,
        expected_object_file_sha256=(
            expected_object_file_sha256
        ),
        expected_payload_sha256=(
            expected_payload_sha256
        ),
    )


def _validate_inputs(
    *,
    model_pk: str,
    objects: Any,
    chunk_bytes: int,
) -> list[ValidatedInput]:
    if not isinstance(objects, list):
        raise MAFSegmentBuilderError(
            "objects must be a list"
        )

    if not objects:
        raise MAFSegmentBuilderError(
            "objects must not be empty"
        )

    validated = []
    seen_object_pks = set()

    for ordinal, record in enumerate(objects):
        item = _validate_input_record(
            record,
            expected_model_pk=model_pk,
            chunk_bytes=chunk_bytes,
        )

        if item.object_pk in seen_object_pks:
            raise MAFSegmentBuilderError(
                "duplicate object_pk at ordinal "
                f"{ordinal}: {item.object_pk}"
            )

        seen_object_pks.add(
            item.object_pk
        )

        validated.append(item)

    return validated


def _validate_output_paths(
    *,
    validated: list[ValidatedInput],
    segment_path: Path,
    manifest_path: Path,
) -> tuple[Path, Path, Path, Path]:
    segment_path = Path(segment_path)
    manifest_path = Path(manifest_path)

    segment_partial = segment_path.with_name(
        segment_path.name + ".partial"
    )

    manifest_partial = manifest_path.with_name(
        manifest_path.name + ".partial"
    )

    outputs = (
        segment_path,
        manifest_path,
        segment_partial,
        manifest_partial,
    )

    normalized_outputs = [
        _normalized_path(path)
        for path in outputs
    ]

    if len(set(normalized_outputs)) != len(
        normalized_outputs
    ):
        raise MAFSegmentBuilderError(
            "segment/manifest output paths collide"
        )

    source_paths = {
        _normalized_path(item.object_path)
        for item in validated
    }

    for path in normalized_outputs:
        if path in source_paths:
            raise MAFSegmentBuilderError(
                "output path collides with input object"
            )

    if segment_path.exists():
        raise MAFSegmentBuilderError(
            f"final segment already exists: {segment_path}"
        )

    if manifest_path.exists():
        raise MAFSegmentBuilderError(
            f"final manifest already exists: {manifest_path}"
        )

    if segment_partial.exists():
        raise MAFSegmentBuilderError(
            "partial segment already exists: "
            f"{segment_partial}"
        )

    if manifest_partial.exists():
        raise MAFSegmentBuilderError(
            "partial manifest already exists: "
            f"{manifest_partial}"
        )

    return (
        segment_path,
        manifest_path,
        segment_partial,
        manifest_partial,
    )


def _stream_copy_object(
    *,
    source_path: Path,
    target,
    object_length: int,
    chunk_bytes: int,
    segment_digest,
) -> str:
    object_digest = hashlib.sha256()
    copied = 0

    with source_path.open("rb") as source:
        remaining = object_length

        while remaining:
            want = min(
                remaining,
                chunk_bytes,
            )

            chunk = source.read(want)

            if len(chunk) != want:
                raise MAFSegmentBuilderError(
                    "truncated object while packing: "
                    f"{source_path}"
                )

            target.write(chunk)

            object_digest.update(chunk)
            segment_digest.update(chunk)

            copied += len(chunk)
            remaining -= len(chunk)

        if source.read(1):
            raise MAFSegmentBuilderError(
                "object grew while packing: "
                f"{source_path}"
            )

    if copied != object_length:
        raise MAFSegmentBuilderError(
            "object byte-count mismatch while packing"
        )

    return object_digest.hexdigest()


def _independent_validate_segment(
    *,
    segment_path: Path,
    expected_segment_length: int,
    expected_segment_sha256: str,
    placements: list[dict],
    chunk_bytes: int,
) -> None:
    segment_digest = hashlib.sha256()
    observed_total = 0

    with segment_path.open("rb") as stream:
        for expected_ordinal, placement in enumerate(
            placements
        ):
            if placement["ordinal"] != expected_ordinal:
                raise MAFSegmentBuilderError(
                    "manifest ordinal mismatch"
                )

            if placement["offset"] != observed_total:
                raise MAFSegmentBuilderError(
                    "non-contiguous segment placement"
                )

            remaining = placement["length"]
            object_digest = hashlib.sha256()

            while remaining:
                want = min(
                    remaining,
                    chunk_bytes,
                )

                chunk = stream.read(want)

                if len(chunk) != want:
                    raise MAFSegmentBuilderError(
                        "truncated segment during reopen"
                    )

                object_digest.update(chunk)
                segment_digest.update(chunk)

                observed_total += len(chunk)
                remaining -= len(chunk)

            if (
                object_digest.hexdigest()
                != placement[
                    "object_file_sha256"
                ]
            ):
                raise MAFSegmentBuilderError(
                    "segment object-range SHA256 mismatch"
                )

        if stream.read(1):
            raise MAFSegmentBuilderError(
                "unexpected trailing segment bytes"
            )

    if observed_total != expected_segment_length:
        raise MAFSegmentBuilderError(
            "segment length mismatch during reopen"
        )

    if (
        segment_digest.hexdigest()
        != expected_segment_sha256
    ):
        raise MAFSegmentBuilderError(
            "segment SHA256 mismatch during reopen"
        )


def build_segment(
    *,
    model_pk: str,
    objects: list[dict],
    segment_path: Path,
    manifest_path: Path,
    chunk_bytes: int = DEFAULT_CHUNK_BYTES,
) -> SegmentBuildResult:
    """
    Build one immutable V1 candidate segment.

    Input MAF objects are independently validated before any output
    is created. Their complete standalone bytes are then copied in
    caller order using bounded streaming.
    """

    model_pk = _validate_model_pk(
        model_pk
    )

    chunk_bytes = _validate_chunk_bytes(
        chunk_bytes
    )

    validated = _validate_inputs(
        model_pk=model_pk,
        objects=objects,
        chunk_bytes=chunk_bytes,
    )

    (
        segment_path,
        manifest_path,
        segment_partial,
        manifest_partial,
    ) = _validate_output_paths(
        validated=validated,
        segment_path=Path(segment_path),
        manifest_path=Path(manifest_path),
    )

    segment_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    manifest_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    segment_digest = hashlib.sha256()
    placements = []
    offset = 0

    segment_activated = False
    manifest_activated = False

    try:
        with segment_partial.open("xb") as target:
            for ordinal, item in enumerate(validated):
                object_sha256 = _stream_copy_object(
                    source_path=item.object_path,
                    target=target,
                    object_length=item.object_length,
                    chunk_bytes=chunk_bytes,
                    segment_digest=segment_digest,
                )

                if (
                    item.expected_object_file_sha256
                    is not None
                    and object_sha256
                    != item.expected_object_file_sha256
                ):
                    raise MAFSegmentBuilderError(
                        "expected object-file SHA256 mismatch"
                    )

                placements.append(
                    {
                        "ordinal": ordinal,
                        "object_pk": item.object_pk,
                        "offset": offset,
                        "length": item.object_length,
                        "object_file_sha256": (
                            object_sha256
                        ),
                        "payload_sha256": (
                            item.object_view.payload_sha256
                        ),
                    }
                )

                offset += item.object_length

            target.flush()
            os.fsync(
                target.fileno()
            )

        segment_length = offset
        segment_sha256 = segment_digest.hexdigest()

        if (
            segment_partial.stat().st_size
            != segment_length
        ):
            raise MAFSegmentBuilderError(
                "partial segment filesystem length mismatch"
            )

        _independent_validate_segment(
            segment_path=segment_partial,
            expected_segment_length=segment_length,
            expected_segment_sha256=segment_sha256,
            placements=placements,
            chunk_bytes=chunk_bytes,
        )

        manifest = {
            "schema": MANIFEST_SCHEMA,
            "builder_version": BUILDER_VERSION,
            "placement_policy": PLACEMENT_POLICY,
            "model_pk": model_pk,
            "object_count": len(placements),
            "segment_length": segment_length,
            "segment_sha256": segment_sha256,
            "objects": placements,
        }

        manifest_raw = _canonical_json_bytes(
            manifest
        )

        with manifest_partial.open("xb") as target:
            target.write(manifest_raw)
            target.flush()
            os.fsync(
                target.fileno()
            )

        reread_manifest = json.loads(
            manifest_partial.read_text(
                encoding="utf-8"
            )
        )

        if (
            _canonical_json_bytes(reread_manifest)
            != manifest_raw
        ):
            raise MAFSegmentBuilderError(
                "manifest independent reopen mismatch"
            )

        os.replace(
            segment_partial,
            segment_path,
        )

        segment_activated = True

        os.replace(
            manifest_partial,
            manifest_path,
        )

        manifest_activated = True

        return SegmentBuildResult(
            schema=SCHEMA,
            builder_version=BUILDER_VERSION,
            model_pk=model_pk,
            segment_path=segment_path,
            manifest_path=manifest_path,
            segment_length=segment_length,
            segment_sha256=segment_sha256,
            manifest=manifest,
        )

    except Exception:
        if manifest_partial.exists():
            manifest_partial.unlink()

        if segment_partial.exists():
            segment_partial.unlink()

        if manifest_activated and manifest_path.exists():
            manifest_path.unlink()

        if segment_activated and segment_path.exists():
            segment_path.unlink()

        raise
