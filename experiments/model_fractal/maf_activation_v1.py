#!/usr/bin/env python3

"""MAF Activation V1.

Provides the minimum model-scoped authority transition defined by the
frozen MAF Activation V1 protocol.

Candidate generation validation is delegated to the frozen Generation
Engine V1 manifest verifier.

This module changes only the explicit active-generation authority record.
It does not modify generation manifests, descriptors, segments, objects,
logical identities, runtime residency, or compute state.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import maf_generation_engine_v1 as generation


ACTIVE_SCHEMA = "openmind.maf_active_generation.v1"
ACTIVE_VERSION = "maf_active_generation_v1"

ACTIVE_FIELDS = {
    "schema",
    "active_generation_version",
    "model_pk",
    "generation_pk",
    "generation_manifest_sha256",
}


class MAFActivationError(ValueError):
    """Activation V1 fail-closed error."""


@dataclass(frozen=True)
class ActivationResult:
    active_record_path: Path
    record: dict[str, Any]
    changed: bool


def canonical_json_bytes(
    value: Any,
) -> bytes:
    """Return canonical bytes using the frozen generation convention."""
    return generation.canonical_json_bytes(
        value
    )


def _require_text(
    value: Any,
    label: str,
) -> str:
    if (
        not isinstance(value, str)
        or not value
    ):
        raise MAFActivationError(
            f"{label} must be non-empty text"
        )

    return value


def _validate_model_pk(
    value: Any,
) -> str:
    value = _require_text(
        value,
        "model_pk",
    )

    if (
        generation.MODEL_PK_RE.fullmatch(
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
    value = _require_text(
        value,
        "generation_pk",
    )

    if (
        generation.GENERATION_PK_RE.fullmatch(
            value
        )
        is None
    ):
        raise MAFActivationError(
            "invalid generation_pk"
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

    if (
        generation.SHA256_RE.fullmatch(
            value
        )
        is None
    ):
        raise MAFActivationError(
            f"invalid {label}"
        )

    return value


def _load_candidate_manifest(
    candidate_manifest_path: Path,
) -> tuple[
    dict[str, Any],
    bytes,
]:
    """Read exact candidate bytes and verify with Generation Engine V1."""
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
        canonical_json_bytes(
            manifest
        )
        != raw
    ):
        raise MAFActivationError(
            "candidate manifest is not canonical JSON"
        )

    return manifest, raw


def build_active_record(
    *,
    model_pk: str,
    generation_pk: str,
    candidate_manifest_path: Path,
) -> dict[str, Any]:
    """Build one canonical authority record without mutating authority."""
    model_pk = _validate_model_pk(
        model_pk
    )
    generation_pk = (
        _validate_generation_pk(
            generation_pk
        )
    )

    manifest, raw = (
        _load_candidate_manifest(
            candidate_manifest_path
        )
    )

    actual_generation_pk = (
        generation.verify_manifest(
            manifest
        )
    )

    descriptor = manifest[
        "descriptor"
    ]

    actual_model_pk = descriptor[
        "model_pk"
    ]

    if actual_model_pk != model_pk:
        raise MAFActivationError(
            "requested model_pk mismatch"
        )

    if (
        manifest["generation_pk"]
        != generation_pk
    ):
        raise MAFActivationError(
            "requested generation_pk mismatch"
        )

    if actual_generation_pk != generation_pk:
        raise MAFActivationError(
            "verified generation_pk mismatch"
        )

    record = {
        "schema": ACTIVE_SCHEMA,
        "active_generation_version":
            ACTIVE_VERSION,
        "model_pk": model_pk,
        "generation_pk": generation_pk,
        "generation_manifest_sha256":
            hashlib.sha256(
                raw
            ).hexdigest(),
    }

    verify_active_record(
        record
    )

    return record


def verify_active_record(
    record: Any,
) -> dict[str, Any]:
    """Strictly verify one active-generation authority record."""
    if not isinstance(
        record,
        dict,
    ):
        raise MAFActivationError(
            "active record must be an object"
        )

    if set(record) != ACTIVE_FIELDS:
        raise MAFActivationError(
            "invalid active record field set"
        )

    if record["schema"] != ACTIVE_SCHEMA:
        raise MAFActivationError(
            "invalid active record schema"
        )

    if (
        record[
            "active_generation_version"
        ]
        != ACTIVE_VERSION
    ):
        raise MAFActivationError(
            "invalid active record version"
        )

    _validate_model_pk(
        record["model_pk"]
    )

    _validate_generation_pk(
        record["generation_pk"]
    )

    _validate_sha256(
        record[
            "generation_manifest_sha256"
        ],
        "generation_manifest_sha256",
    )

    return record


def _read_active_record(
    active_record_path: Path,
) -> tuple[
    dict[str, Any],
    bytes,
]:
    path = Path(
        active_record_path
    )

    if not path.is_file():
        raise MAFActivationError(
            "active record missing"
        )

    raw = path.read_bytes()

    try:
        record = json.loads(
            raw.decode("utf-8")
        )
    except Exception as exc:
        raise MAFActivationError(
            "invalid active record JSON"
        ) from exc

    verify_active_record(
        record
    )

    if canonical_json_bytes(
        record
    ) != raw:
        raise MAFActivationError(
            "active record is not canonical JSON"
        )

    return record, raw


def reopen_active_generation(
    active_record_path: Path,
) -> dict[str, Any]:
    """Independently reopen and verify completed active authority."""
    record, _ = _read_active_record(
        active_record_path
    )

    return record


def activate_generation(
    *,
    model_pk: str,
    generation_pk: str,
    candidate_manifest_path: Path,
    active_record_path: Path,
) -> ActivationResult:
    """Atomically switch one model-scoped active-generation reference."""
    candidate_manifest_path = Path(
        candidate_manifest_path
    )

    active_record_path = Path(
        active_record_path
    )

    if (
        candidate_manifest_path.resolve()
        == active_record_path.resolve()
    ):
        raise MAFActivationError(
            "candidate and active paths must differ"
        )

    target = build_active_record(
        model_pk=model_pk,
        generation_pk=generation_pk,
        candidate_manifest_path=(
            candidate_manifest_path
        ),
    )

    target_bytes = (
        canonical_json_bytes(
            target
        )
    )

    partial_path = (
        active_record_path.with_name(
            active_record_path.name
            + ".partial"
        )
    )

    if partial_path.exists():
        raise MAFActivationError(
            "partial active record already exists"
        )

    if active_record_path.exists():
        (
            current,
            current_bytes,
        ) = _read_active_record(
            active_record_path
        )

        if (
            current["model_pk"]
            != target["model_pk"]
        ):
            raise MAFActivationError(
                "existing active record model mismatch"
            )

        if current == target:
            if current_bytes != target_bytes:
                raise MAFActivationError(
                    "idempotent active bytes mismatch"
                )

            return ActivationResult(
                active_record_path=(
                    active_record_path
                ),
                record=current,
                changed=False,
            )

    active_record_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    created_partial = False

    try:
        with partial_path.open(
            "xb"
        ) as handle:
            created_partial = True

            handle.write(
                target_bytes
            )

            handle.flush()
            os.fsync(
                handle.fileno()
            )

        (
            partial_record,
            partial_bytes,
        ) = _read_active_record(
            partial_path
        )

        if partial_record != target:
            raise MAFActivationError(
                "partial active record mismatch"
            )

        if partial_bytes != target_bytes:
            raise MAFActivationError(
                "partial active bytes mismatch"
            )

        os.replace(
            partial_path,
            active_record_path,
        )

        created_partial = False

    except Exception:
        if (
            created_partial
            and partial_path.exists()
        ):
            partial_path.unlink()

        raise

    return ActivationResult(
        active_record_path=(
            active_record_path
        ),
        record=target,
        changed=True,
    )
