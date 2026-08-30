#!/usr/bin/env python3

"""MAF Activation V1.1.

Adds the current-physical-validity eligibility boundary preregistered by
the frozen Activation V1.1 corrective protocol.

Generation identity and physical reconstruction are delegated to the
frozen Generation Engine V1.

The actual active-authority transition is delegated to the frozen
Activation V1 implementation after physical eligibility succeeds.

This module does not implement rollback, retirement, runtime residency,
inference, or a production catalog storage engine.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import maf_activation_v1 as activation_v1
import maf_generation_engine_v1 as generation


MAFActivationError = activation_v1.MAFActivationError
ActivationResult = activation_v1.ActivationResult

ACTIVE_SCHEMA = activation_v1.ACTIVE_SCHEMA
ACTIVE_VERSION = activation_v1.ACTIVE_VERSION
ACTIVE_FIELDS = activation_v1.ACTIVE_FIELDS


def canonical_json_bytes(
    value: Any,
) -> bytes:
    """Use the frozen canonical authority serialization."""
    return activation_v1.canonical_json_bytes(
        value
    )


def _validate_model_pk(
    value: Any,
) -> str:
    if (
        not isinstance(value, str)
        or generation.MODEL_PK_RE.fullmatch(
            value
        )
        is None
    ):
        raise MAFActivationError(
            "invalid model_pk"
        )

    return value


def _validate_generation_pk(
    value: Any,
) -> str:
    if (
        not isinstance(value, str)
        or generation.GENERATION_PK_RE.fullmatch(
            value
        )
        is None
    ):
        raise MAFActivationError(
            "invalid generation_pk"
        )

    return value


def _load_candidate_manifest(
    candidate_manifest_path: Path,
) -> tuple[
    dict[str, Any],
    bytes,
]:
    """Reopen exact canonical candidate bytes and verify identity."""
    path = Path(
        candidate_manifest_path
    )

    if not path.is_file():
        raise MAFActivationError(
            "candidate manifest missing"
        )

    raw = path.read_bytes()

    try:
        manifest = json.loads(
            raw.decode("utf-8")
        )
    except Exception as exc:
        raise MAFActivationError(
            "invalid candidate manifest JSON"
        ) from exc

    try:
        generation.verify_manifest(
            manifest
        )
    except generation.MAFGenerationEngineError as exc:
        raise MAFActivationError(
            str(exc)
        ) from exc

    if (
        generation.canonical_json_bytes(
            manifest
        )
        != raw
    ):
        raise MAFActivationError(
            "candidate manifest is not canonical JSON"
        )

    return manifest, raw


def _segment_path_mapping(
    *,
    descriptor: dict[str, Any],
    segment_paths: Any,
) -> dict[str, Path]:
    """Require one and only one physical path for every descriptor segment."""
    if not isinstance(
        segment_paths,
        dict,
    ):
        raise MAFActivationError(
            "segment_paths mapping required"
        )

    descriptor_ids = [
        row["segment_id"]
        for row in descriptor["segments"]
    ]

    expected = set(
        descriptor_ids
    )
    supplied = set(
        segment_paths
    )

    missing = expected.difference(
        supplied
    )

    if missing:
        raise MAFActivationError(
            "missing descriptor segment mapping"
        )

    extra = supplied.difference(
        expected
    )

    if extra:
        raise MAFActivationError(
            "extra descriptor segment mapping"
        )

    mapped: dict[str, Path] = {}

    for segment_id in descriptor_ids:
        value = segment_paths[
            segment_id
        ]

        try:
            path = Path(
                value
            )
        except Exception as exc:
            raise MAFActivationError(
                "invalid segment path mapping"
            ) from exc

        mapped[
            segment_id
        ] = path

    return mapped


def _validate_current_candidate(
    *,
    model_pk: str,
    generation_pk: str,
    candidate_manifest_path: Path,
    segment_paths: Any,
) -> dict[str, Any]:
    """Physically reconstruct and exactly reproduce one candidate."""
    model_pk = _validate_model_pk(
        model_pk
    )

    generation_pk = (
        _validate_generation_pk(
            generation_pk
        )
    )

    manifest, _ = (
        _load_candidate_manifest(
            candidate_manifest_path
        )
    )

    candidate_descriptor = manifest[
        "descriptor"
    ]

    if (
        candidate_descriptor[
            "model_pk"
        ]
        != model_pk
    ):
        raise MAFActivationError(
            "requested model_pk mismatch"
        )

    if (
        manifest[
            "generation_pk"
        ]
        != generation_pk
    ):
        raise MAFActivationError(
            "requested generation_pk mismatch"
        )

    mapped_paths = (
        _segment_path_mapping(
            descriptor=(
                candidate_descriptor
            ),
            segment_paths=segment_paths,
        )
    )

    segment_inputs = [
        {
            "segment_path":
                str(
                    mapped_paths[
                        row["segment_id"]
                    ]
                ),
            "segment_length":
                row[
                    "segment_length"
                ],
            "segment_sha256":
                row[
                    "segment_sha256"
                ],
        }
        for row
        in candidate_descriptor[
            "segments"
        ]
    ]

    object_inputs = [
        {
            "model_pk":
                model_pk,
            "object_pk":
                row[
                    "object_pk"
                ],
            "segment_path":
                str(
                    mapped_paths[
                        row["segment_id"]
                    ]
                ),
            "offset":
                row[
                    "offset"
                ],
            "length":
                row[
                    "length"
                ],
            "object_file_sha256":
                row[
                    "object_file_sha256"
                ],
            "payload_sha256":
                row[
                    "payload_sha256"
                ],
        }
        for row
        in candidate_descriptor[
            "objects"
        ]
    ]

    try:
        (
            reconstructed_descriptor,
            reconstructed_descriptor_sha256,
            reconstructed_generation_pk,
        ) = generation.build_descriptor(
            model_pk=model_pk,
            segments=segment_inputs,
            objects=object_inputs,
        )
    except generation.MAFGenerationEngineError as exc:
        raise MAFActivationError(
            str(exc)
        ) from exc

    if (
        reconstructed_descriptor
        != candidate_descriptor
    ):
        raise MAFActivationError(
            "reconstructed descriptor mismatch"
        )

    candidate_descriptor_bytes = (
        generation.canonical_json_bytes(
            candidate_descriptor
        )
    )

    reconstructed_descriptor_bytes = (
        generation.canonical_json_bytes(
            reconstructed_descriptor
        )
    )

    if (
        reconstructed_descriptor_bytes
        != candidate_descriptor_bytes
    ):
        raise MAFActivationError(
            "reconstructed descriptor bytes mismatch"
        )

    expected_descriptor_sha256 = (
        hashlib.sha256(
            candidate_descriptor_bytes
        ).hexdigest()
    )

    if (
        reconstructed_descriptor_sha256
        != expected_descriptor_sha256
    ):
        raise MAFActivationError(
            "reconstructed descriptor SHA256 mismatch"
        )

    if (
        reconstructed_generation_pk
        != manifest[
            "generation_pk"
        ]
    ):
        raise MAFActivationError(
            "reconstructed generation_pk mismatch"
        )

    if (
        reconstructed_generation_pk
        != generation_pk
    ):
        raise MAFActivationError(
            "requested reconstructed generation_pk mismatch"
        )

    return manifest


def build_active_record(
    *,
    model_pk: str,
    generation_pk: str,
    candidate_manifest_path: Path,
    segment_paths: Any,
) -> dict[str, Any]:
    """Build authority bytes only after current physical validity passes."""
    _validate_current_candidate(
        model_pk=model_pk,
        generation_pk=generation_pk,
        candidate_manifest_path=(
            candidate_manifest_path
        ),
        segment_paths=segment_paths,
    )

    return activation_v1.build_active_record(
        model_pk=model_pk,
        generation_pk=generation_pk,
        candidate_manifest_path=(
            candidate_manifest_path
        ),
    )


def verify_active_record(
    record: Any,
) -> dict[str, Any]:
    """Reuse the frozen five-field active-record verifier."""
    return activation_v1.verify_active_record(
        record
    )


def reopen_active_generation(
    active_record_path: Path,
) -> dict[str, Any]:
    """Reuse the frozen independent authority-record reopen."""
    return activation_v1.reopen_active_generation(
        active_record_path
    )


def activate_generation(
    *,
    model_pk: str,
    generation_pk: str,
    candidate_manifest_path: Path,
    active_record_path: Path,
    segment_paths: Any,
) -> ActivationResult:
    """Revalidate current physical evidence, then delegate authority switch."""
    _validate_current_candidate(
        model_pk=model_pk,
        generation_pk=generation_pk,
        candidate_manifest_path=(
            candidate_manifest_path
        ),
        segment_paths=segment_paths,
    )

    return activation_v1.activate_generation(
        model_pk=model_pk,
        generation_pk=generation_pk,
        candidate_manifest_path=(
            candidate_manifest_path
        ),
        active_record_path=(
            active_record_path
        ),
    )
