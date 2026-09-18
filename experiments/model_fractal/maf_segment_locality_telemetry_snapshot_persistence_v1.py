"""Phase 6D telemetry snapshot persistence V1.

Standalone deterministic persistence for the already-validated
TelemetrySnapshot data model.

This module does not collect runtime telemetry, integrate with Phase 6C,
plan repacks, realize generations, benchmark storage, or implement Phase 6E.
"""

from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any, Mapping
import hashlib
import json
import os
import re
import stat

from experiments.model_fractal import (
    maf_segment_locality_data_model_v1 as _model,
)


PERSISTENCE_PROTOCOL_SHA256 = (
    "0e08a8a18a45a16eddc05927b8191d73ca9fc7453cb97fc1140e5e243e03db51"
)

DATA_MODEL_SHA256 = (
    "5432f2d74a610f2d0f9181e9af146013bb198a4e837af634993909358fff8ad0"
)

DATA_MODEL_VALIDATION_RESULT_SHA256 = (
    "9aa2e467dc451b2d2122802e1e8b8fabf616db756a36b53a3600cca793923b4d"
)

DATA_MODEL_VALIDATION_VERDICT_SHA256 = (
    "7754c9d5dada8dc214a21236827c64cafea880e4b0c679cd84c9c4833fd3e9db"
)

PHASE6C_ENGINE_SHA256 = (
    "4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9"
)

SNAPSHOT_FILE_SCHEMA = (
    "openmind.maf_segment_locality.telemetry_snapshot_file.v1"
)

ENVELOPE_KEYS = frozenset(
    {
        "schema",
        "snapshot_sha256",
        "snapshot",
    }
)


class TelemetrySnapshotPersistenceError(
    Exception
):
    """Base class for telemetry snapshot persistence failures."""


class TelemetrySnapshotPersistenceValidationError(
    TelemetrySnapshotPersistenceError
):
    """Persistence input or envelope validation failed."""


class TelemetrySnapshotPersistenceReadError(
    TelemetrySnapshotPersistenceError
):
    """Validated telemetry snapshot read failed."""


class TelemetrySnapshotPersistenceWriteError(
    TelemetrySnapshotPersistenceError
):
    """Immutable telemetry snapshot publication failed."""


@dataclass(
    frozen=True,
    slots=True,
)
class TelemetrySnapshotWriteResult:
    final_path: str
    snapshot_sha256: str
    file_sha256: str
    byte_length: int


@dataclass(
    frozen=True,
    slots=True,
)
class TelemetrySnapshotReadResult:
    snapshot: _model.TelemetrySnapshot
    snapshot_sha256: str
    file_sha256: str
    byte_length: int


def _require_plain_nonnegative_int(
    value: Any,
    *,
    field_name: str,
) -> int:
    if (
        isinstance(
            value,
            bool,
        )
        or not isinstance(
            value,
            int,
        )
        or value < 0
    ):
        raise TelemetrySnapshotPersistenceValidationError(
            field_name
            + " must be a plain non-negative integer"
        )

    return value


def _require_lower_sha256(
    value: Any,
    *,
    field_name: str,
) -> str:
    if (
        not isinstance(
            value,
            str,
        )
        or re.fullmatch(
            r"[0-9a-f]{64}",
            value,
        )
        is None
    ):
        raise TelemetrySnapshotPersistenceValidationError(
            field_name
            + " must be exactly 64 lowercase hexadecimal characters"
        )

    return value


def _require_exact_mapping(
    value: Any,
    expected_keys: set[str] | frozenset[str],
    *,
    context: str,
) -> Mapping[str, Any]:
    if not isinstance(
        value,
        dict,
    ):
        raise TelemetrySnapshotPersistenceValidationError(
            context
            + " must be a JSON object"
        )

    actual = set(
        value.keys()
    )

    if actual != set(
        expected_keys
    ):
        missing = sorted(
            set(expected_keys)
            - actual
        )

        extra = sorted(
            actual
            - set(expected_keys)
        )

        raise TelemetrySnapshotPersistenceValidationError(
            context
            + " key-set mismatch"
            + "; missing="
            + repr(missing)
            + "; extra="
            + repr(extra)
        )

    if not all(
        isinstance(
            key,
            str,
        )
        for key in value
    ):
        raise TelemetrySnapshotPersistenceValidationError(
            context
            + " keys must all be strings"
        )

    return value


def _dataclass_field_names(
    cls: type,
) -> frozenset[str]:
    return frozenset(
        item.name
        for item in fields(
            cls
        )
    )


def _construct_dataclass(
    cls: type,
    value: Any,
    *,
    context: str,
) -> Any:
    mapping = _require_exact_mapping(
        value,
        _dataclass_field_names(
            cls
        ),
        context=context,
    )

    try:
        return cls(
            **dict(
                mapping
            )
        )

    except Exception as exc:
        raise TelemetrySnapshotPersistenceValidationError(
            context
            + " failed frozen data-model validation: "
            + type(exc).__name__
            + ": "
            + str(exc)
        ) from exc


def _construct_dataclass_tuple(
    cls: type,
    value: Any,
    *,
    context: str,
) -> tuple[Any, ...]:
    if not isinstance(
        value,
        list,
    ):
        raise TelemetrySnapshotPersistenceValidationError(
            context
            + " must be a JSON array"
        )

    return tuple(
        _construct_dataclass(
            cls,
            item,
            context=(
                context
                + "["
                + str(index)
                + "]"
            ),
        )
        for index, item
        in enumerate(
            value
        )
    )


def reconstruct_snapshot_payload(
    payload: Any,
) -> _model.TelemetrySnapshot:
    mapping = _require_exact_mapping(
        payload,
        _dataclass_field_names(
            _model.TelemetrySnapshot
        ),
        context="snapshot",
    )

    kwargs = dict(
        mapping
    )

    kwargs[
        "object_aggregates"
    ] = _construct_dataclass_tuple(
        _model.ObjectTelemetryAggregate,
        mapping[
            "object_aggregates"
        ],
        context="snapshot.object_aggregates",
    )

    kwargs[
        "transition_aggregates"
    ] = _construct_dataclass_tuple(
        _model.TransitionTelemetryAggregate,
        mapping[
            "transition_aggregates"
        ],
        context="snapshot.transition_aggregates",
    )

    kwargs[
        "cache_aggregates"
    ] = _construct_dataclass_tuple(
        _model.CacheTelemetryAggregate,
        mapping[
            "cache_aggregates"
        ],
        context="snapshot.cache_aggregates",
    )

    kwargs[
        "residency_transition_aggregates"
    ] = _construct_dataclass_tuple(
        _model.ResidencyTransitionAggregate,
        mapping[
            "residency_transition_aggregates"
        ],
        context=(
            "snapshot."
            "residency_transition_aggregates"
        ),
    )

    kwargs[
        "prefetch_aggregates"
    ] = _construct_dataclass_tuple(
        _model.PrefetchTelemetryAggregate,
        mapping[
            "prefetch_aggregates"
        ],
        context="snapshot.prefetch_aggregates",
    )

    try:
        snapshot = _model.TelemetrySnapshot(
            **kwargs
        )

    except Exception as exc:
        raise TelemetrySnapshotPersistenceValidationError(
            "snapshot failed frozen data-model validation: "
            + type(exc).__name__
            + ": "
            + str(exc)
        ) from exc

    regenerated = _model.snapshot_payload(
        snapshot
    )

    if regenerated != payload:
        raise TelemetrySnapshotPersistenceValidationError(
            "reconstructed snapshot payload differs from stored payload"
        )

    return snapshot


def snapshot_file_payload(
    snapshot: _model.TelemetrySnapshot,
) -> dict[str, Any]:
    if not isinstance(
        snapshot,
        _model.TelemetrySnapshot,
    ):
        raise TelemetrySnapshotPersistenceValidationError(
            "snapshot must be a frozen TelemetrySnapshot"
        )

    try:
        payload = _model.snapshot_payload(
            snapshot
        )

        snapshot_sha = _model.snapshot_sha256(
            snapshot
        )

    except Exception as exc:
        raise TelemetrySnapshotPersistenceValidationError(
            "snapshot could not be serialized by frozen data model: "
            + type(exc).__name__
            + ": "
            + str(exc)
        ) from exc

    _require_lower_sha256(
        snapshot_sha,
        field_name="snapshot_sha256",
    )

    return {
        "schema":
            SNAPSHOT_FILE_SCHEMA,

        "snapshot_sha256":
            snapshot_sha,

        "snapshot":
            payload,
    }


def snapshot_file_bytes(
    snapshot: _model.TelemetrySnapshot,
) -> bytes:
    envelope = snapshot_file_payload(
        snapshot
    )

    try:
        return _model.canonical_json_bytes(
            envelope
        )

    except Exception as exc:
        raise TelemetrySnapshotPersistenceValidationError(
            "persistent envelope canonicalization failed: "
            + type(exc).__name__
            + ": "
            + str(exc)
        ) from exc


def snapshot_file_sha256(
    snapshot: _model.TelemetrySnapshot,
) -> str:
    return hashlib.sha256(
        snapshot_file_bytes(
            snapshot
        )
    ).hexdigest()


def partial_path_for(
    final_path: str | os.PathLike[str],
) -> Path:
    path = Path(
        final_path
    )

    if path.name == "":
        raise TelemetrySnapshotPersistenceValidationError(
            "final path must name a file"
        )

    return path.with_name(
        path.name
        + ".partial"
    )


def _object_pairs_no_duplicates(
    pairs: list[tuple[str, Any]],
) -> dict[str, Any]:
    result: dict[str, Any] = {}

    for key, value in pairs:
        if key in result:
            raise TelemetrySnapshotPersistenceValidationError(
                "duplicate JSON object key: "
                + repr(
                    key
                )
            )

        result[
            key
        ] = value

    return result


def _parse_canonical_envelope(
    raw: bytes,
) -> tuple[
    Mapping[str, Any],
    _model.TelemetrySnapshot,
    str,
]:
    try:
        text = raw.decode(
            "utf-8",
            errors="strict",
        )

    except UnicodeDecodeError as exc:
        raise TelemetrySnapshotPersistenceReadError(
            "snapshot file is not strict UTF-8"
        ) from exc

    try:
        parsed = json.loads(
            text,
            object_pairs_hook=(
                _object_pairs_no_duplicates
            ),
        )

    except TelemetrySnapshotPersistenceValidationError as exc:
        raise TelemetrySnapshotPersistenceReadError(
            str(exc)
        ) from exc

    except Exception as exc:
        raise TelemetrySnapshotPersistenceReadError(
            "snapshot file contains invalid JSON: "
            + type(exc).__name__
            + ": "
            + str(exc)
        ) from exc

    try:
        canonical = _model.canonical_json_bytes(
            parsed
        )

    except Exception as exc:
        raise TelemetrySnapshotPersistenceReadError(
            "parsed envelope cannot be canonically encoded: "
            + type(exc).__name__
            + ": "
            + str(exc)
        ) from exc

    if canonical != raw:
        raise TelemetrySnapshotPersistenceReadError(
            "snapshot file bytes are not canonical"
        )

    try:
        envelope = _require_exact_mapping(
            parsed,
            ENVELOPE_KEYS,
            context="envelope",
        )

        if (
            envelope[
                "schema"
            ]
            != SNAPSHOT_FILE_SCHEMA
        ):
            raise TelemetrySnapshotPersistenceValidationError(
                "unsupported telemetry snapshot persistence schema"
            )

        stored_snapshot_sha = _require_lower_sha256(
            envelope[
                "snapshot_sha256"
            ],
            field_name="snapshot_sha256",
        )

        snapshot = reconstruct_snapshot_payload(
            envelope[
                "snapshot"
            ]
        )

        reconstructed_payload = _model.snapshot_payload(
            snapshot
        )

        if (
            reconstructed_payload
            != envelope[
                "snapshot"
            ]
        ):
            raise TelemetrySnapshotPersistenceValidationError(
                "snapshot payload reconstruction mismatch"
            )

        computed_snapshot_sha = _model.snapshot_sha256(
            snapshot
        )

        if (
            computed_snapshot_sha
            != stored_snapshot_sha
        ):
            raise TelemetrySnapshotPersistenceValidationError(
                "snapshot SHA256 mismatch"
            )

    except TelemetrySnapshotPersistenceValidationError as exc:
        raise TelemetrySnapshotPersistenceReadError(
            str(exc)
        ) from exc

    except Exception as exc:
        raise TelemetrySnapshotPersistenceReadError(
            "snapshot reconstruction failed: "
            + type(exc).__name__
            + ": "
            + str(exc)
        ) from exc

    return (
        envelope,
        snapshot,
        stored_snapshot_sha,
    )


def _read_regular_file_bytes(
    path: Path,
) -> bytes:
    try:
        st = os.lstat(
            path
        )

    except FileNotFoundError as exc:
        raise TelemetrySnapshotPersistenceReadError(
            "snapshot file does not exist"
        ) from exc

    except OSError as exc:
        raise TelemetrySnapshotPersistenceReadError(
            "snapshot path inspection failed: "
            + str(exc)
        ) from exc

    if stat.S_ISLNK(
        st.st_mode
    ):
        raise TelemetrySnapshotPersistenceReadError(
            "symbolic-link snapshot paths are forbidden"
        )

    if not stat.S_ISREG(
        st.st_mode
    ):
        raise TelemetrySnapshotPersistenceReadError(
            "snapshot path is not a regular file"
        )

    flags = os.O_RDONLY

    if hasattr(
        os,
        "O_NOFOLLOW",
    ):
        flags |= os.O_NOFOLLOW

    try:
        fd = os.open(
            path,
            flags,
        )

    except OSError as exc:
        raise TelemetrySnapshotPersistenceReadError(
            "snapshot file open failed: "
            + str(exc)
        ) from exc

    chunks: list[bytes] = []

    try:
        opened_stat = os.fstat(
            fd
        )

        if not stat.S_ISREG(
            opened_stat.st_mode
        ):
            raise TelemetrySnapshotPersistenceReadError(
                "opened snapshot authority is not a regular file"
            )

        while True:
            chunk = os.read(
                fd,
                1024 * 1024,
            )

            if not chunk:
                break

            chunks.append(
                chunk
            )

    except TelemetrySnapshotPersistenceReadError:
        raise

    except OSError as exc:
        raise TelemetrySnapshotPersistenceReadError(
            "snapshot file read failed: "
            + str(exc)
        ) from exc

    finally:
        os.close(
            fd
        )

    return b"".join(
        chunks
    )


def read_snapshot_file(
    path: str | os.PathLike[str],
) -> TelemetrySnapshotReadResult:
    final_path = Path(
        path
    )

    raw = _read_regular_file_bytes(
        final_path
    )

    (
        _envelope,
        snapshot,
        snapshot_sha,
    ) = _parse_canonical_envelope(
        raw
    )

    file_sha = hashlib.sha256(
        raw
    ).hexdigest()

    return TelemetrySnapshotReadResult(
        snapshot=snapshot,
        snapshot_sha256=snapshot_sha,
        file_sha256=file_sha,
        byte_length=len(
            raw
        ),
    )


def _write_all(
    fd: int,
    data: bytes,
) -> None:
    view = memoryview(
        data
    )

    offset = 0

    while offset < len(
        view
    ):
        written = os.write(
            fd,
            view[
                offset:
            ],
        )

        if written <= 0:
            raise TelemetrySnapshotPersistenceWriteError(
                "short write while publishing partial snapshot"
            )

        offset += written


def _fsync_directory(
    directory: Path,
) -> None:
    flags = os.O_RDONLY

    if hasattr(
        os,
        "O_DIRECTORY",
    ):
        flags |= os.O_DIRECTORY

    try:
        fd = os.open(
            directory,
            flags,
        )

    except OSError as exc:
        raise TelemetrySnapshotPersistenceWriteError(
            "parent directory open for fsync failed: "
            + str(exc)
        ) from exc

    try:
        os.fsync(
            fd
        )

    except OSError as exc:
        raise TelemetrySnapshotPersistenceWriteError(
            "parent directory fsync failed: "
            + str(exc)
        ) from exc

    finally:
        os.close(
            fd
        )


def write_snapshot_file(
    snapshot: _model.TelemetrySnapshot,
    final_path: str | os.PathLike[str],
) -> TelemetrySnapshotWriteResult:
    path = Path(
        final_path
    )

    if path.name == "":
        raise TelemetrySnapshotPersistenceWriteError(
            "final path must name a file"
        )

    parent = path.parent

    if not parent.exists():
        raise TelemetrySnapshotPersistenceWriteError(
            "parent directory does not exist"
        )

    if not parent.is_dir():
        raise TelemetrySnapshotPersistenceWriteError(
            "parent path is not a directory"
        )

    partial = partial_path_for(
        path
    )

    if os.path.lexists(
        path
    ):
        raise TelemetrySnapshotPersistenceWriteError(
            "final snapshot path already exists"
        )

    if os.path.lexists(
        partial
    ):
        raise TelemetrySnapshotPersistenceWriteError(
            "partial snapshot path already exists"
        )

    try:
        envelope = snapshot_file_payload(
            snapshot
        )

        data = _model.canonical_json_bytes(
            envelope
        )

        snapshot_sha = envelope[
            "snapshot_sha256"
        ]

        file_sha = hashlib.sha256(
            data
        ).hexdigest()

    except TelemetrySnapshotPersistenceError:
        raise

    except Exception as exc:
        raise TelemetrySnapshotPersistenceWriteError(
            "snapshot serialization failed before publication: "
            + type(exc).__name__
            + ": "
            + str(exc)
        ) from exc

    try:
        fd = os.open(
            partial,
            (
                os.O_WRONLY
                | os.O_CREAT
                | os.O_EXCL
            ),
            0o600,
        )

    except OSError as exc:
        raise TelemetrySnapshotPersistenceWriteError(
            "exclusive partial creation failed: "
            + str(exc)
        ) from exc

    write_error: Exception | None = None

    try:
        _write_all(
            fd,
            data,
        )

        os.fsync(
            fd
        )

    except Exception as exc:
        write_error = exc

    try:
        os.close(
            fd
        )

    except OSError as exc:
        if write_error is None:
            write_error = exc

    if write_error is not None:
        if isinstance(
            write_error,
            TelemetrySnapshotPersistenceWriteError,
        ):
            raise write_error

        raise TelemetrySnapshotPersistenceWriteError(
            "partial write/fsync/close failed; residue preserved: "
            + type(write_error).__name__
            + ": "
            + str(write_error)
        ) from write_error

    try:
        os.link(
            partial,
            path,
            follow_symlinks=False,
        )

    except FileExistsError as exc:
        raise TelemetrySnapshotPersistenceWriteError(
            "final snapshot path appeared before atomic publication; "
            "partial residue preserved"
        ) from exc

    except OSError as exc:
        raise TelemetrySnapshotPersistenceWriteError(
            "atomic no-replace hard-link publication failed; "
            "partial residue preserved: "
            + str(exc)
        ) from exc

    _fsync_directory(
        parent
    )

    try:
        os.unlink(
            partial
        )

    except OSError as exc:
        raise TelemetrySnapshotPersistenceWriteError(
            "final snapshot was published but partial retirement failed; "
            "residue preserved: "
            + str(exc)
        ) from exc

    _fsync_directory(
        parent
    )

    return TelemetrySnapshotWriteResult(
        final_path=str(
            path
        ),
        snapshot_sha256=snapshot_sha,
        file_sha256=file_sha,
        byte_length=len(
            data
        ),
    )


__all__ = (
    "PERSISTENCE_PROTOCOL_SHA256",
    "DATA_MODEL_SHA256",
    "DATA_MODEL_VALIDATION_RESULT_SHA256",
    "DATA_MODEL_VALIDATION_VERDICT_SHA256",
    "PHASE6C_ENGINE_SHA256",
    "SNAPSHOT_FILE_SCHEMA",
    "TelemetrySnapshotPersistenceError",
    "TelemetrySnapshotPersistenceValidationError",
    "TelemetrySnapshotPersistenceReadError",
    "TelemetrySnapshotPersistenceWriteError",
    "TelemetrySnapshotWriteResult",
    "TelemetrySnapshotReadResult",
    "snapshot_file_payload",
    "snapshot_file_bytes",
    "snapshot_file_sha256",
    "reconstruct_snapshot_payload",
    "partial_path_for",
    "read_snapshot_file",
    "write_snapshot_file",
)
