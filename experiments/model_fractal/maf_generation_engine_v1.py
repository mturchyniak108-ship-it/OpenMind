#!/usr/bin/env python3

"""MAF Generation Engine V1.

Constructs and persists one validated candidate MAF generation manifest.

This module does not activate generations, maintain an authoritative
catalog, assign runtime residency, materialize dense tensors, or perform
MAF-native compute.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ENGINE_SCHEMA = "openmind.maf_generation_engine.v1"
ENGINE_VERSION = "maf_generation_engine_v1"

DESCRIPTOR_SCHEMA = "openmind.maf_generation_descriptor.v1"
DESCRIPTOR_VERSION = "maf_generation_descriptor_v1"

MANIFEST_SCHEMA = "openmind.maf_generation_manifest.v1"
MANIFEST_VERSION = "maf_generation_manifest_v1"

GENERATION_PREFIX = "mafgen:v1:"
DEFAULT_CHUNK_BYTES = 1024 * 1024

MODEL_PK_RE = re.compile(
    r"^mafmodel:v1:[0-9a-f]{64}$"
)
OBJECT_PK_RE = re.compile(
    r"^mafobj:v1:[0-9a-f]{64}$"
)
GENERATION_PK_RE = re.compile(
    r"^mafgen:v1:[0-9a-f]{64}$"
)
SHA256_RE = re.compile(
    r"^[0-9a-f]{64}$"
)


class MAFGenerationEngineError(ValueError):
    """Generation Engine V1 fail-closed error."""


@dataclass(frozen=True)
class ValidatedSegment:
    source_path: Path
    segment_length: int
    segment_sha256: str


@dataclass(frozen=True)
class GenerationBuildResult:
    schema: str
    engine_version: str
    generation_pk: str
    manifest_path: Path
    descriptor_sha256: str
    manifest: dict[str, Any]


def canonical_json_bytes(value: Any) -> bytes:
    """Return frozen canonical JSON bytes."""
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _require_dict(
    value: Any,
    label: str,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise MAFGenerationEngineError(
            f"{label} must be a dict"
        )

    return value


def _require_list(
    value: Any,
    label: str,
) -> list[Any]:
    if not isinstance(value, list):
        raise MAFGenerationEngineError(
            f"{label} must be a list"
        )

    return value


def _require_text(
    value: Any,
    label: str,
) -> str:
    if not isinstance(value, str) or not value:
        raise MAFGenerationEngineError(
            f"{label} must be nonempty text"
        )

    return value


def _require_int(
    value: Any,
    label: str,
) -> int:
    if (
        isinstance(value, bool)
        or not isinstance(value, int)
    ):
        raise MAFGenerationEngineError(
            f"{label} must be an integer"
        )

    return value


def _validate_model_pk(value: Any) -> str:
    value = _require_text(
        value,
        "model_pk",
    )

    if MODEL_PK_RE.fullmatch(value) is None:
        raise MAFGenerationEngineError(
            "invalid model_pk"
        )

    return value


def _validate_object_pk(value: Any) -> str:
    value = _require_text(
        value,
        "object_pk",
    )

    if OBJECT_PK_RE.fullmatch(value) is None:
        raise MAFGenerationEngineError(
            "invalid object_pk"
        )

    return value


def _validate_sha256(
    value: Any,
    label: str,
) -> str:
    value = _require_text(
        value,
        label,
    )

    if SHA256_RE.fullmatch(value) is None:
        raise MAFGenerationEngineError(
            f"invalid {label}"
        )

    return value


def _validate_chunk_bytes(value: Any) -> int:
    value = _require_int(
        value,
        "chunk_bytes",
    )

    if value <= 0:
        raise MAFGenerationEngineError(
            "chunk_bytes must be positive"
        )

    return value


def _normalized_path(path: Path) -> str:
    return os.path.abspath(
        os.fspath(path)
    )


def stream_sha256(
    path: Path,
    *,
    chunk_bytes: int = DEFAULT_CHUNK_BYTES,
) -> str:
    """SHA256 a file using bounded reads."""
    chunk_bytes = _validate_chunk_bytes(
        chunk_bytes
    )

    path = Path(path)

    if not path.is_file():
        raise MAFGenerationEngineError(
            f"not a regular file: {path}"
        )

    digest = hashlib.sha256()

    with path.open("rb") as handle:
        while True:
            block = handle.read(chunk_bytes)

            if not block:
                break

            digest.update(block)

    return digest.hexdigest()


def stream_range_sha256(
    path: Path,
    *,
    offset: int,
    length: int,
    chunk_bytes: int = DEFAULT_CHUNK_BYTES,
) -> str:
    """SHA256 one exact bounded byte range."""
    chunk_bytes = _validate_chunk_bytes(
        chunk_bytes
    )
    offset = _require_int(
        offset,
        "offset",
    )
    length = _require_int(
        length,
        "length",
    )

    if offset < 0:
        raise MAFGenerationEngineError(
            "offset must be nonnegative"
        )

    if length <= 0:
        raise MAFGenerationEngineError(
            "length must be positive"
        )

    path = Path(path)

    if not path.is_file():
        raise MAFGenerationEngineError(
            f"not a regular file: {path}"
        )

    file_length = path.stat().st_size

    if offset + length > file_length:
        raise MAFGenerationEngineError(
            "requested range exceeds file bounds"
        )

    digest = hashlib.sha256()
    remaining = length

    with path.open("rb") as handle:
        handle.seek(offset)

        while remaining:
            want = min(
                remaining,
                chunk_bytes,
            )
            block = handle.read(want)

            if len(block) != want:
                raise MAFGenerationEngineError(
                    "short read during range hash"
                )

            digest.update(block)
            remaining -= len(block)

    return digest.hexdigest()


def _validate_segment_record(
    record: Any,
    *,
    chunk_bytes: int,
) -> ValidatedSegment:
    record = _require_dict(
        record,
        "segment record",
    )

    required = {
        "segment_path",
        "segment_length",
        "segment_sha256",
    }

    missing = required.difference(record)

    if missing:
        raise MAFGenerationEngineError(
            "missing segment fields: "
            + ", ".join(sorted(missing))
        )

    path_text = _require_text(
        record["segment_path"],
        "segment_path",
    )
    path = Path(path_text)

    if not path.is_file():
        raise MAFGenerationEngineError(
            f"segment is not a regular file: {path}"
        )

    declared_length = _require_int(
        record["segment_length"],
        "segment_length",
    )

    if declared_length <= 0:
        raise MAFGenerationEngineError(
            "segment_length must be positive"
        )

    actual_length = path.stat().st_size

    if actual_length != declared_length:
        raise MAFGenerationEngineError(
            "segment length mismatch"
        )

    declared_sha = _validate_sha256(
        record["segment_sha256"],
        "segment_sha256",
    )

    actual_sha = stream_sha256(
        path,
        chunk_bytes=chunk_bytes,
    )

    if actual_sha != declared_sha:
        raise MAFGenerationEngineError(
            "segment SHA256 mismatch"
        )

    return ValidatedSegment(
        source_path=path,
        segment_length=actual_length,
        segment_sha256=actual_sha,
    )


def _normalize_segments(
    segments: Any,
    *,
    chunk_bytes: int,
) -> tuple[
    list[dict[str, Any]],
    dict[str, str],
    dict[str, ValidatedSegment],
]:
    segments = _require_list(
        segments,
        "segments",
    )

    if not segments:
        raise MAFGenerationEngineError(
            "segments must not be empty"
        )

    validated = [
        _validate_segment_record(
            record,
            chunk_bytes=chunk_bytes,
        )
        for record in segments
    ]

    by_content: dict[
        tuple[str, int],
        ValidatedSegment,
    ] = {}

    path_to_content: dict[
        str,
        tuple[str, int],
    ] = {}

    for item in validated:
        content_key = (
            item.segment_sha256,
            item.segment_length,
        )
        normalized_path = _normalized_path(
            item.source_path
        )

        previous_key = path_to_content.get(
            normalized_path
        )

        if (
            previous_key is not None
            and previous_key != content_key
        ):
            raise MAFGenerationEngineError(
                "conflicting segment record for path"
            )

        path_to_content[
            normalized_path
        ] = content_key

        by_content.setdefault(
            content_key,
            item,
        )

    ordered_keys = sorted(
        by_content,
        key=lambda key: (
            key[0],
            key[1],
        ),
    )

    descriptor_segments: list[
        dict[str, Any]
    ] = []
    content_to_id: dict[
        tuple[str, int],
        str,
    ] = {}

    for ordinal, content_key in enumerate(
        ordered_keys
    ):
        segment_id = (
            f"segment:{ordinal:08d}"
        )
        segment_sha, segment_length = (
            content_key
        )

        descriptor_segments.append(
            {
                "segment_id": segment_id,
                "segment_length": (
                    segment_length
                ),
                "segment_sha256": segment_sha,
            }
        )

        content_to_id[
            content_key
        ] = segment_id

    path_to_id = {
        path: content_to_id[content_key]
        for path, content_key
        in path_to_content.items()
    }

    id_to_segment = {
        content_to_id[content_key]:
            by_content[content_key]
        for content_key in ordered_keys
    }

    return (
        descriptor_segments,
        path_to_id,
        id_to_segment,
    )


def _normalize_objects(
    *,
    model_pk: str,
    objects: Any,
    path_to_id: dict[str, str],
    id_to_segment: dict[
        str,
        ValidatedSegment,
    ],
    chunk_bytes: int,
) -> list[dict[str, Any]]:
    objects = _require_list(
        objects,
        "objects",
    )

    if not objects:
        raise MAFGenerationEngineError(
            "objects must not be empty"
        )

    rows: list[dict[str, Any]] = []
    seen_object_pks: set[str] = set()

    for record in objects:
        record = _require_dict(
            record,
            "object placement",
        )

        required = {
            "model_pk",
            "object_pk",
            "segment_path",
            "offset",
            "length",
            "object_file_sha256",
            "payload_sha256",
        }

        missing = required.difference(record)

        if missing:
            raise MAFGenerationEngineError(
                "missing object placement fields: "
                + ", ".join(sorted(missing))
            )

        record_model_pk = _validate_model_pk(
            record["model_pk"]
        )

        if record_model_pk != model_pk:
            raise MAFGenerationEngineError(
                "mixed-model generation request"
            )

        object_pk = _validate_object_pk(
            record["object_pk"]
        )

        if object_pk in seen_object_pks:
            raise MAFGenerationEngineError(
                f"duplicate object_pk: {object_pk}"
            )

        seen_object_pks.add(
            object_pk
        )

        segment_path_text = _require_text(
            record["segment_path"],
            "segment_path",
        )
        normalized_segment_path = (
            _normalized_path(
                Path(segment_path_text)
            )
        )

        if (
            normalized_segment_path
            not in path_to_id
        ):
            raise MAFGenerationEngineError(
                "object references unknown segment"
            )

        segment_id = path_to_id[
            normalized_segment_path
        ]
        segment = id_to_segment[
            segment_id
        ]

        offset = _require_int(
            record["offset"],
            "offset",
        )
        length = _require_int(
            record["length"],
            "length",
        )

        if offset < 0:
            raise MAFGenerationEngineError(
                "offset must be nonnegative"
            )

        if length <= 0:
            raise MAFGenerationEngineError(
                "length must be positive"
            )

        if (
            offset + length
            > segment.segment_length
        ):
            raise MAFGenerationEngineError(
                "object placement exceeds "
                "segment bounds"
            )

        object_file_sha256 = (
            _validate_sha256(
                record[
                    "object_file_sha256"
                ],
                "object_file_sha256",
            )
        )

        payload_sha256 = _validate_sha256(
            record["payload_sha256"],
            "payload_sha256",
        )

        actual_object_sha = (
            stream_range_sha256(
                segment.source_path,
                offset=offset,
                length=length,
                chunk_bytes=chunk_bytes,
            )
        )

        if (
            actual_object_sha
            != object_file_sha256
        ):
            raise MAFGenerationEngineError(
                "object byte-range SHA256 "
                "mismatch"
            )

        rows.append(
            {
                "object_pk": object_pk,
                "segment_id": segment_id,
                "offset": offset,
                "length": length,
                "object_file_sha256": (
                    object_file_sha256
                ),
                "payload_sha256": (
                    payload_sha256
                ),
            }
        )

    rows.sort(
        key=lambda row: row["object_pk"]
    )

    return rows


def build_descriptor(
    *,
    model_pk: str,
    segments: Any,
    objects: Any,
    chunk_bytes: int = DEFAULT_CHUNK_BYTES,
) -> tuple[
    dict[str, Any],
    str,
    str,
]:
    """Validate evidence and construct canonical descriptor."""
    chunk_bytes = _validate_chunk_bytes(
        chunk_bytes
    )
    model_pk = _validate_model_pk(
        model_pk
    )

    (
        descriptor_segments,
        path_to_id,
        id_to_segment,
    ) = _normalize_segments(
        segments,
        chunk_bytes=chunk_bytes,
    )

    descriptor_objects = _normalize_objects(
        model_pk=model_pk,
        objects=objects,
        path_to_id=path_to_id,
        id_to_segment=id_to_segment,
        chunk_bytes=chunk_bytes,
    )

    descriptor = {
        "schema": DESCRIPTOR_SCHEMA,
        "descriptor_version": (
            DESCRIPTOR_VERSION
        ),
        "model_pk": model_pk,
        "segments": descriptor_segments,
        "objects": descriptor_objects,
    }

    descriptor_bytes = canonical_json_bytes(
        descriptor
    )
    descriptor_sha256 = hashlib.sha256(
        descriptor_bytes
    ).hexdigest()
    generation_pk = (
        GENERATION_PREFIX
        + descriptor_sha256
    )

    return (
        descriptor,
        descriptor_sha256,
        generation_pk,
    )


def build_manifest(
    *,
    model_pk: str,
    segments: Any,
    objects: Any,
    chunk_bytes: int = DEFAULT_CHUNK_BYTES,
) -> dict[str, Any]:
    """Construct one candidate generation manifest in memory."""
    (
        descriptor,
        _descriptor_sha256,
        generation_pk,
    ) = build_descriptor(
        model_pk=model_pk,
        segments=segments,
        objects=objects,
        chunk_bytes=chunk_bytes,
    )

    return {
        "schema": MANIFEST_SCHEMA,
        "manifest_version": MANIFEST_VERSION,
        "generation_pk": generation_pk,
        "descriptor": descriptor,
    }


def verify_manifest(
    manifest: Any,
) -> str:
    """Recompute and verify one manifest generation_pk."""
    manifest = _require_dict(
        manifest,
        "manifest",
    )

    expected_keys = {
        "schema",
        "manifest_version",
        "generation_pk",
        "descriptor",
    }

    if set(manifest) != expected_keys:
        raise MAFGenerationEngineError(
            "invalid manifest field set"
        )

    if (
        manifest["schema"]
        != MANIFEST_SCHEMA
    ):
        raise MAFGenerationEngineError(
            "invalid manifest schema"
        )

    if (
        manifest["manifest_version"]
        != MANIFEST_VERSION
    ):
        raise MAFGenerationEngineError(
            "invalid manifest version"
        )

    generation_pk = _require_text(
        manifest["generation_pk"],
        "generation_pk",
    )

    if (
        GENERATION_PK_RE.fullmatch(
            generation_pk
        )
        is None
    ):
        raise MAFGenerationEngineError(
            "invalid generation_pk"
        )

    descriptor = _require_dict(
        manifest["descriptor"],
        "descriptor",
    )

    descriptor_keys = {
        "schema",
        "descriptor_version",
        "model_pk",
        "segments",
        "objects",
    }

    if set(descriptor) != descriptor_keys:
        raise MAFGenerationEngineError(
            "invalid descriptor field set"
        )

    if (
        descriptor["schema"]
        != DESCRIPTOR_SCHEMA
    ):
        raise MAFGenerationEngineError(
            "invalid descriptor schema"
        )

    if (
        descriptor["descriptor_version"]
        != DESCRIPTOR_VERSION
    ):
        raise MAFGenerationEngineError(
            "invalid descriptor version"
        )

    _validate_model_pk(
        descriptor["model_pk"]
    )

    descriptor_bytes = canonical_json_bytes(
        descriptor
    )
    expected_generation_pk = (
        GENERATION_PREFIX
        + hashlib.sha256(
            descriptor_bytes
        ).hexdigest()
    )

    if generation_pk != expected_generation_pk:
        raise MAFGenerationEngineError(
            "generation_pk mismatch"
        )

    segments = _require_list(
        descriptor["segments"],
        "descriptor segments",
    )
    objects = _require_list(
        descriptor["objects"],
        "descriptor objects",
    )

    if not segments:
        raise MAFGenerationEngineError(
            "descriptor segments empty"
        )

    if not objects:
        raise MAFGenerationEngineError(
            "descriptor objects empty"
        )

    expected_segment_ids = [
        f"segment:{i:08d}"
        for i in range(len(segments))
    ]

    actual_segment_ids = []

    for row in segments:
        row = _require_dict(
            row,
            "descriptor segment",
        )

        if set(row) != {
            "segment_id",
            "segment_length",
            "segment_sha256",
        }:
            raise MAFGenerationEngineError(
                "invalid descriptor segment "
                "field set"
            )

        segment_id = _require_text(
            row["segment_id"],
            "segment_id",
        )
        segment_length = _require_int(
            row["segment_length"],
            "segment_length",
        )

        if segment_length <= 0:
            raise MAFGenerationEngineError(
                "invalid descriptor "
                "segment_length"
            )

        _validate_sha256(
            row["segment_sha256"],
            "segment_sha256",
        )
        actual_segment_ids.append(
            segment_id
        )

    if (
        actual_segment_ids
        != expected_segment_ids
    ):
        raise MAFGenerationEngineError(
            "noncanonical segment IDs"
        )

    canonical_segment_order = sorted(
        segments,
        key=lambda row: (
            row["segment_sha256"],
            row["segment_length"],
        ),
    )

    if segments != canonical_segment_order:
        raise MAFGenerationEngineError(
            "noncanonical segment order"
        )

    segment_lengths = {
        row["segment_id"]:
            row["segment_length"]
        for row in segments
    }

    object_pks = []

    for row in objects:
        row = _require_dict(
            row,
            "descriptor object",
        )

        if set(row) != {
            "object_pk",
            "segment_id",
            "offset",
            "length",
            "object_file_sha256",
            "payload_sha256",
        }:
            raise MAFGenerationEngineError(
                "invalid descriptor object "
                "field set"
            )

        object_pk = _validate_object_pk(
            row["object_pk"]
        )
        segment_id = _require_text(
            row["segment_id"],
            "segment_id",
        )

        if segment_id not in segment_lengths:
            raise MAFGenerationEngineError(
                "descriptor object references "
                "unknown segment"
            )

        offset = _require_int(
            row["offset"],
            "offset",
        )
        length = _require_int(
            row["length"],
            "length",
        )

        if offset < 0 or length <= 0:
            raise MAFGenerationEngineError(
                "invalid descriptor placement"
            )

        if (
            offset + length
            > segment_lengths[segment_id]
        ):
            raise MAFGenerationEngineError(
                "descriptor placement exceeds "
                "segment bounds"
            )

        _validate_sha256(
            row["object_file_sha256"],
            "object_file_sha256",
        )
        _validate_sha256(
            row["payload_sha256"],
            "payload_sha256",
        )

        object_pks.append(
            object_pk
        )

    if len(object_pks) != len(
        set(object_pks)
    ):
        raise MAFGenerationEngineError(
            "duplicate descriptor object_pk"
        )

    if object_pks != sorted(object_pks):
        raise MAFGenerationEngineError(
            "noncanonical object order"
        )

    return expected_generation_pk


def persist_candidate_manifest(
    *,
    manifest: Any,
    manifest_path: Path,
) -> None:
    """Atomically persist one candidate manifest."""
    verify_manifest(
        manifest
    )

    manifest_path = Path(
        manifest_path
    )
    partial_path = manifest_path.with_name(
        manifest_path.name + ".partial"
    )

    if manifest_path.exists():
        raise MAFGenerationEngineError(
            "final manifest already exists"
        )

    if partial_path.exists():
        raise MAFGenerationEngineError(
            "partial manifest already exists"
        )

    manifest_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    payload = canonical_json_bytes(
        manifest
    )
    created_partial = False

    try:
        with partial_path.open("xb") as handle:
            created_partial = True
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())

        reopened = json.loads(
            partial_path.read_text(
                encoding="utf-8"
            )
        )

        verify_manifest(
            reopened
        )

        if canonical_json_bytes(
            reopened
        ) != payload:
            raise MAFGenerationEngineError(
                "candidate manifest canonical "
                "reopen mismatch"
            )

        os.replace(
            partial_path,
            manifest_path,
        )
        created_partial = False

    except Exception:
        if (
            created_partial
            and partial_path.exists()
        ):
            partial_path.unlink()

        raise


def reopen_candidate_manifest(
    manifest_path: Path,
) -> dict[str, Any]:
    """Reopen and verify one persisted candidate manifest."""
    manifest_path = Path(
        manifest_path
    )

    if not manifest_path.is_file():
        raise MAFGenerationEngineError(
            "candidate manifest missing"
        )

    raw = manifest_path.read_bytes()

    try:
        manifest = json.loads(
            raw.decode("utf-8")
        )
    except Exception as exc:
        raise MAFGenerationEngineError(
            "invalid candidate manifest JSON"
        ) from exc

    verify_manifest(
        manifest
    )

    if canonical_json_bytes(
        manifest
    ) != raw:
        raise MAFGenerationEngineError(
            "candidate manifest is not "
            "canonical JSON"
        )

    return manifest


def build_generation(
    *,
    model_pk: str,
    segments: Any,
    objects: Any,
    manifest_path: Path,
    chunk_bytes: int = DEFAULT_CHUNK_BYTES,
) -> GenerationBuildResult:
    """Build, persist, reopen, and verify a candidate generation."""
    chunk_bytes = _validate_chunk_bytes(
        chunk_bytes
    )

    segment_snapshot = []

    for record in _require_list(
        segments,
        "segments",
    ):
        record = _require_dict(
            record,
            "segment record",
        )

        path = Path(
            _require_text(
                record.get("segment_path"),
                "segment_path",
            )
        )

        if not path.is_file():
            raise MAFGenerationEngineError(
                f"segment is not a regular file: {path}"
            )

        segment_snapshot.append(
            (
                _normalized_path(path),
                path.stat().st_size,
                stream_sha256(
                    path,
                    chunk_bytes=chunk_bytes,
                ),
            )
        )

    manifest = build_manifest(
        model_pk=model_pk,
        segments=segments,
        objects=objects,
        chunk_bytes=chunk_bytes,
    )

    generation_pk = verify_manifest(
        manifest
    )

    persist_candidate_manifest(
        manifest=manifest,
        manifest_path=manifest_path,
    )

    reopened = reopen_candidate_manifest(
        manifest_path
    )

    reopened_generation_pk = (
        verify_manifest(
            reopened
        )
    )

    if (
        reopened_generation_pk
        != generation_pk
    ):
        raise MAFGenerationEngineError(
            "reopened generation_pk mismatch"
        )

    for (
        path_text,
        expected_length,
        expected_sha,
    ) in segment_snapshot:
        path = Path(path_text)

        if not path.is_file():
            raise MAFGenerationEngineError(
                "adopted segment disappeared"
            )

        if (
            path.stat().st_size
            != expected_length
        ):
            raise MAFGenerationEngineError(
                "adopted segment length changed"
            )

        if (
            stream_sha256(
                path,
                chunk_bytes=chunk_bytes,
            )
            != expected_sha
        ):
            raise MAFGenerationEngineError(
                "adopted segment SHA changed"
            )

    descriptor_bytes = canonical_json_bytes(
        reopened["descriptor"]
    )
    descriptor_sha256 = hashlib.sha256(
        descriptor_bytes
    ).hexdigest()

    return GenerationBuildResult(
        schema=ENGINE_SCHEMA,
        engine_version=ENGINE_VERSION,
        generation_pk=generation_pk,
        manifest_path=Path(
            manifest_path
        ),
        descriptor_sha256=descriptor_sha256,
        manifest=reopened,
    )
