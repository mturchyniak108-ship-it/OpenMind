#!/usr/bin/env python3

"""Resident PK Directory V1.

Derived, process-local lookup state for the currently active immutable MAF
generation.

This module is intentionally not an authority writer. It validates frozen
active/generation evidence, constructs a complete immutable snapshot, and
publishes that snapshot only after successful construction.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

import maf_activation_v1_1 as activation


OBJECT_PK_KIND = "object_pk"


class MAFResidentPKDirectoryError(RuntimeError):
    """Base error for Resident PK Directory V1."""


class MAFResidentPKDirectoryAuthorityError(
    MAFResidentPKDirectoryError
):
    """Current active authority is missing or invalid."""


class MAFResidentPKDirectoryActiveGenerationMismatch(
    MAFResidentPKDirectoryError
):
    """Candidate evidence is not bound to current active authority."""


class MAFResidentPKDirectoryPhysicalEvidenceError(
    MAFResidentPKDirectoryError
):
    """Current physical generation evidence is invalid."""


class MAFResidentPKDirectoryDuplicatePKError(
    MAFResidentPKDirectoryError
):
    """A logical resident key occurs more than once."""


class MAFResidentPKDirectoryUnsupportedPKError(
    MAFResidentPKDirectoryError
):
    """Requested PK class is not supported by V1."""


class MAFResidentPKDirectoryNotFoundError(
    MAFResidentPKDirectoryError
):
    """Requested logical PK is absent from the resident snapshot."""


class MAFResidentPKDirectoryStaleSnapshotError(
    MAFResidentPKDirectoryError
):
    """Resident snapshot is not the caller's expected generation."""


class MAFResidentPKDirectoryCrossModelError(
    MAFResidentPKDirectoryError
):
    """Requested model differs from the resident snapshot model."""


class MAFResidentPKDirectoryUnavailableError(
    MAFResidentPKDirectoryError
):
    """No complete resident snapshot has been published."""


@dataclass(
    frozen=True,
    slots=True,
)
class ResidentPKEntry:
    """One immutable direct-access mapping derived from active descriptor."""

    model_pk: str
    generation_pk: str
    generation_manifest_sha256: str
    object_pk: str

    segment_id: str
    offset: int
    length: int

    object_file_sha256: str
    payload_sha256: str

    segment_length: int
    segment_sha256: str

    segment_path: str


@dataclass(
    frozen=True,
    slots=True,
)
class ResidentPKSnapshot:
    """Immutable lookup snapshot for exactly one active model generation."""

    model_pk: str
    generation_pk: str
    generation_manifest_sha256: str
    active_record_sha256: str

    entries: Mapping[
        tuple[
            str,
            str,
            str,
        ],
        ResidentPKEntry,
    ]

    @property
    def entry_count(
        self,
    ) -> int:
        return len(
            self.entries
        )

    def lookup(
        self,
        *,
        model_pk: str,
        pk_kind: str,
        logical_pk: str,
        expected_generation_pk: str,
    ) -> ResidentPKEntry:
        """Perform one direct generation-bound resident lookup."""
        if model_pk != self.model_pk:
            raise MAFResidentPKDirectoryCrossModelError(
                "resident snapshot model mismatch"
            )

        if (
            expected_generation_pk
            != self.generation_pk
        ):
            raise MAFResidentPKDirectoryStaleSnapshotError(
                "resident snapshot generation mismatch"
            )

        if pk_kind != OBJECT_PK_KIND:
            raise MAFResidentPKDirectoryUnsupportedPKError(
                "unsupported resident PK class"
            )

        if (
            not isinstance(
                logical_pk,
                str,
            )
            or not logical_pk
        ):
            raise MAFResidentPKDirectoryNotFoundError(
                "logical PK not found"
            )

        key = (
            model_pk,
            OBJECT_PK_KIND,
            logical_pk,
        )

        try:
            return self.entries[
                key
            ]
        except KeyError as exc:
            raise MAFResidentPKDirectoryNotFoundError(
                "logical PK not found"
            ) from exc


class ResidentPKDirectory:
    """Own one replaceable immutable resident snapshot."""

    __slots__ = (
        "_snapshot",
    )

    def __init__(
        self,
    ) -> None:
        self._snapshot: (
            ResidentPKSnapshot
            | None
        ) = None

    @property
    def snapshot(
        self,
    ) -> ResidentPKSnapshot:
        value = self._snapshot

        if value is None:
            raise MAFResidentPKDirectoryUnavailableError(
                "resident snapshot unavailable"
            )

        return value

    def refresh(
        self,
        *,
        model_pk: str,
        active_record_path: Path,
        active_candidate_manifest_path: Path,
        active_segment_paths: Any,
    ) -> ResidentPKSnapshot:
        """Build completely, then replace the published resident snapshot."""
        replacement = build_snapshot(
            model_pk=model_pk,
            active_record_path=(
                active_record_path
            ),
            active_candidate_manifest_path=(
                active_candidate_manifest_path
            ),
            active_segment_paths=(
                active_segment_paths
            ),
        )

        self._snapshot = replacement

        return replacement

    def lookup(
        self,
        *,
        model_pk: str,
        pk_kind: str,
        logical_pk: str,
        expected_generation_pk: str,
    ) -> ResidentPKEntry:
        """Delegate one direct lookup to the published immutable snapshot."""
        return self.snapshot.lookup(
            model_pk=model_pk,
            pk_kind=pk_kind,
            logical_pk=logical_pk,
            expected_generation_pk=(
                expected_generation_pk
            ),
        )


def _read_bytes(
    path: Path,
    *,
    label: str,
) -> bytes:
    try:
        return path.read_bytes()
    except OSError as exc:
        raise MAFResidentPKDirectoryAuthorityError(
            label
            + " cannot be read"
        ) from exc


def _sha256_bytes(
    value: bytes,
) -> str:
    return hashlib.sha256(
        value
    ).hexdigest()


def _reopen_active_authority(
    *,
    active_record_path: Path,
) -> tuple[
    dict[str, Any],
    bytes,
    str,
]:
    before = _read_bytes(
        active_record_path,
        label="active authority",
    )

    try:
        record = (
            activation.reopen_active_generation(
                active_record_path
            )
        )
    except activation.MAFActivationError as exc:
        raise MAFResidentPKDirectoryAuthorityError(
            str(
                exc
            )
        ) from exc

    after = _read_bytes(
        active_record_path,
        label="active authority",
    )

    if after != before:
        raise MAFResidentPKDirectoryAuthorityError(
            "active authority changed during reopen"
        )

    return (
        record,
        before,
        _sha256_bytes(
            before
        ),
    )


def _validate_candidate_binding(
    *,
    active_record: dict[str, Any],
    candidate_manifest_path: Path,
) -> bytes:
    candidate_bytes = _read_bytes(
        candidate_manifest_path,
        label="active candidate manifest",
    )

    candidate_sha256 = (
        _sha256_bytes(
            candidate_bytes
        )
    )

    if (
        candidate_sha256
        != active_record[
            "generation_manifest_sha256"
        ]
    ):
        raise (
            MAFResidentPKDirectoryActiveGenerationMismatch(
                "active candidate manifest SHA256 mismatch"
            )
        )

    return candidate_bytes


def build_snapshot(
    *,
    model_pk: str,
    active_record_path: Path,
    active_candidate_manifest_path: Path,
    active_segment_paths: Any,
) -> ResidentPKSnapshot:
    """Build one complete immutable snapshot from current active evidence."""
    active_record_path = Path(
        active_record_path
    )

    active_candidate_manifest_path = Path(
        active_candidate_manifest_path
    )

    (
        active_record,
        active_record_bytes,
        active_record_sha256,
    ) = _reopen_active_authority(
        active_record_path=(
            active_record_path
        ),
    )

    if (
        active_record[
            "model_pk"
        ]
        != model_pk
    ):
        raise MAFResidentPKDirectoryCrossModelError(
            "active authority model mismatch"
        )

    candidate_bytes = (
        _validate_candidate_binding(
            active_record=active_record,
            candidate_manifest_path=(
                active_candidate_manifest_path
            ),
        )
    )

    try:
        manifest = (
            activation._validate_current_candidate(
                model_pk=model_pk,
                generation_pk=(
                    active_record[
                        "generation_pk"
                    ]
                ),
                candidate_manifest_path=(
                    active_candidate_manifest_path
                ),
                segment_paths=(
                    active_segment_paths
                ),
            )
        )
    except activation.MAFActivationError as exc:
        raise MAFResidentPKDirectoryPhysicalEvidenceError(
            str(
                exc
            )
        ) from exc

    if (
        manifest[
            "generation_pk"
        ]
        != active_record[
            "generation_pk"
        ]
    ):
        raise (
            MAFResidentPKDirectoryActiveGenerationMismatch(
                "validated generation differs from active authority"
            )
        )

    descriptor = manifest[
        "descriptor"
    ]

    if (
        descriptor[
            "model_pk"
        ]
        != model_pk
    ):
        raise MAFResidentPKDirectoryCrossModelError(
            "validated descriptor model mismatch"
        )

    try:
        mapped_paths = (
            activation._segment_path_mapping(
                descriptor=descriptor,
                segment_paths=(
                    active_segment_paths
                ),
            )
        )
    except activation.MAFActivationError as exc:
        raise MAFResidentPKDirectoryPhysicalEvidenceError(
            str(
                exc
            )
        ) from exc

    segment_records: dict[
        str,
        dict[str, Any],
    ] = {}

    for row in descriptor[
        "segments"
    ]:
        segment_id = row[
            "segment_id"
        ]

        if (
            segment_id
            in segment_records
        ):
            raise MAFResidentPKDirectoryPhysicalEvidenceError(
                "duplicate segment_id in validated descriptor"
            )

        segment_records[
            segment_id
        ] = row

    mutable_entries: dict[
        tuple[
            str,
            str,
            str,
        ],
        ResidentPKEntry,
    ] = {}

    for row in descriptor[
        "objects"
    ]:
        object_pk = row[
            "object_pk"
        ]

        key = (
            model_pk,
            OBJECT_PK_KIND,
            object_pk,
        )

        if key in mutable_entries:
            raise MAFResidentPKDirectoryDuplicatePKError(
                "duplicate object_pk in active descriptor"
            )

        segment_id = row[
            "segment_id"
        ]

        try:
            segment_record = (
                segment_records[
                    segment_id
                ]
            )
            segment_path = (
                mapped_paths[
                    segment_id
                ]
            )
        except KeyError as exc:
            raise MAFResidentPKDirectoryPhysicalEvidenceError(
                "validated object references missing segment"
            ) from exc

        mutable_entries[
            key
        ] = ResidentPKEntry(
            model_pk=model_pk,
            generation_pk=(
                active_record[
                    "generation_pk"
                ]
            ),
            generation_manifest_sha256=(
                active_record[
                    "generation_manifest_sha256"
                ]
            ),
            object_pk=object_pk,
            segment_id=segment_id,
            offset=row[
                "offset"
            ],
            length=row[
                "length"
            ],
            object_file_sha256=row[
                "object_file_sha256"
            ],
            payload_sha256=row[
                "payload_sha256"
            ],
            segment_length=(
                segment_record[
                    "segment_length"
                ]
            ),
            segment_sha256=(
                segment_record[
                    "segment_sha256"
                ]
            ),
            segment_path=str(
                segment_path
            ),
        )

    candidate_after = _read_bytes(
        active_candidate_manifest_path,
        label="active candidate manifest",
    )

    if (
        candidate_after
        != candidate_bytes
    ):
        raise (
            MAFResidentPKDirectoryActiveGenerationMismatch(
                "active candidate manifest changed during snapshot build"
            )
        )

    active_after = _read_bytes(
        active_record_path,
        label="active authority",
    )

    if (
        active_after
        != active_record_bytes
    ):
        raise MAFResidentPKDirectoryAuthorityError(
            "active authority changed during snapshot build"
        )

    immutable_entries = MappingProxyType(
        mutable_entries
    )

    return ResidentPKSnapshot(
        model_pk=model_pk,
        generation_pk=(
            active_record[
                "generation_pk"
            ]
        ),
        generation_manifest_sha256=(
            active_record[
                "generation_manifest_sha256"
            ]
        ),
        active_record_sha256=(
            active_record_sha256
        ),
        entries=immutable_entries,
    )
