#!/usr/bin/env python3
"""Backend-neutral Phase 6C MAF Object Runtime and Residency V1.

This module implements the frozen observable correctness contract from:

    MAF_OBJECT_RUNTIME_RESIDENCY_V1_PROTOCOL.md

It deliberately does not select mmap, persistent descriptor caching,
automatic eviction, Vulkan residency, or a production storage backend.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import threading
from typing import Any, Callable

from maf_resident_pk_directory_v1 import ResidentPKEntry
from maf_segment_reader_v1 import (
    MAFSegmentReaderError,
    read_serialized_object,
)


class MAFObjectRuntimeError(RuntimeError):
    """Base error for the Phase 6C V1 runtime."""


class MAFObjectRuntimeInvalidEntryError(MAFObjectRuntimeError):
    """A ResidentPKEntry is invalid for this runtime."""


class MAFObjectRuntimeStaleGenerationError(MAFObjectRuntimeError):
    """An entry does not belong to the runtime model/generation."""


class MAFObjectRuntimeUnknownObjectError(MAFObjectRuntimeError):
    """The requested object is not registered in this runtime."""


class MAFObjectRuntimeIllegalTransitionError(MAFObjectRuntimeError):
    """A requested primitive residency transition is illegal."""


class MAFObjectRuntimePinnedDemotionError(MAFObjectRuntimeError):
    """A demotion would cross an active pin floor."""


class MAFObjectRuntimePinTokenError(MAFObjectRuntimeError):
    """A pin token is invalid, unknown, or already consumed."""


class MAFObjectRuntimeInvalidPinError(MAFObjectRuntimeError):
    """A pin request has an invalid minimum residency state."""


class MAFObjectRuntimeSerializedBudgetExceededError(MAFObjectRuntimeError):
    """A HOT_MAF promotion would exceed the serialized-byte budget."""


class MAFObjectRuntimeDenseBudgetExceededError(MAFObjectRuntimeError):
    """A HOT_DENSE promotion would exceed the dense-byte budget."""


class MAFObjectRuntimeVerifiedReadError(MAFObjectRuntimeError):
    """Frozen Segment Reader verification failed."""


class MAFObjectRuntimeDenseMaterializationError(MAFObjectRuntimeError):
    """Dense materialization failed or returned an invalid result."""


class MAFObjectRuntimeClosedError(MAFObjectRuntimeError):
    """The runtime is closed for mutation or resource exposure."""


class MAFObjectRuntimeReentrancyError(MAFObjectRuntimeError):
    """A callback attempted recursive mutation of the same runtime."""


class MAFObjectRuntimeResidencyUnavailableError(MAFObjectRuntimeError):
    """The requested runtime-resident representation is unavailable."""


class ResidencyState(str, Enum):
    COLD_DISK = "COLD_DISK"
    MAPPED = "MAPPED"
    HOT_MAF = "HOT_MAF"
    HOT_DENSE = "HOT_DENSE"


_STATE_RANK = {
    ResidencyState.COLD_DISK: 0,
    ResidencyState.MAPPED: 1,
    ResidencyState.HOT_MAF: 2,
    ResidencyState.HOT_DENSE: 3,
}


DenseMaterializer = Callable[
    [ResidentPKEntry, bytes],
    tuple[Any, int],
]


@dataclass(
    frozen=True,
    slots=True,
)
class PinLease:
    token: int
    object_pk: str
    minimum_state: ResidencyState


@dataclass(
    frozen=True,
    slots=True,
)
class RuntimeObjectSnapshot:
    object_pk: str
    state: ResidencyState
    pin_count: int
    effective_pin_floor: ResidencyState | None
    serialized_resident_bytes: int
    dense_resident_bytes: int


@dataclass(
    frozen=True,
    slots=True,
)
class RuntimeSnapshot:
    model_pk: str
    generation_pk: str
    closed: bool

    object_count: int
    cold_disk_count: int
    mapped_count: int
    hot_maf_count: int
    hot_dense_count: int

    active_pin_leases: int
    serialized_resident_bytes: int
    dense_resident_bytes: int

    counters: tuple[tuple[str, int], ...]
    objects: tuple[RuntimeObjectSnapshot, ...]


@dataclass(
    slots=True,
)
class _RuntimeObjectRecord:
    entry: ResidentPKEntry
    state: ResidencyState = ResidencyState.COLD_DISK

    serialized_bytes: bytes | None = None

    dense_view: Any = None
    dense_byte_charge: int = 0

    pin_tokens: set[int] = field(
        default_factory=set,
    )


_COUNTER_NAMES = (
    "successful_attach_transitions",
    "successful_verified_byte_promotions",
    "successful_dense_materializations",
    "successful_dense_demotions",
    "successful_serialized_byte_demotions",
    "successful_detach_transitions",
    "successful_pin_acquisitions",
    "successful_unpins",
    "failed_transitions",
    "verification_failures",
    "budget_rejections",
)


def _require_plain_nonnegative_int(
    name: str,
    value: object,
) -> int:
    if (
        type(value) is not int
        or value < 0
    ):
        raise ValueError(
            f"{name} must be a plain nonnegative int"
        )

    return value


def _require_nonempty_str(
    name: str,
    value: object,
) -> str:
    if (
        type(value) is not str
        or not value
    ):
        raise MAFObjectRuntimeInvalidEntryError(
            f"{name} must be a nonempty str"
        )

    return value


def _require_sha256(
    name: str,
    value: object,
) -> str:
    value = _require_nonempty_str(
        name,
        value,
    )

    if (
        len(value) != 64
        or any(
            ch not in "0123456789abcdef"
            for ch in value
        )
    ):
        raise MAFObjectRuntimeInvalidEntryError(
            f"{name} must be lowercase SHA256 hex"
        )

    return value


def _coerce_state(
    value: ResidencyState | str,
) -> ResidencyState:
    if isinstance(
        value,
        ResidencyState,
    ):
        return value

    if type(value) is str:
        try:
            return ResidencyState(value)
        except ValueError as exc:
            raise MAFObjectRuntimeIllegalTransitionError(
                "unknown residency state"
            ) from exc

    raise MAFObjectRuntimeIllegalTransitionError(
        "residency state must be ResidencyState or exact state string"
    )


def _validate_entry_structure(
    entry: object,
) -> ResidentPKEntry:
    if not isinstance(
        entry,
        ResidentPKEntry,
    ):
        raise MAFObjectRuntimeInvalidEntryError(
            "entry must be ResidentPKEntry"
        )

    _require_nonempty_str(
        "model_pk",
        entry.model_pk,
    )
    _require_nonempty_str(
        "generation_pk",
        entry.generation_pk,
    )
    _require_sha256(
        "generation_manifest_sha256",
        entry.generation_manifest_sha256,
    )
    _require_nonempty_str(
        "object_pk",
        entry.object_pk,
    )
    _require_nonempty_str(
        "segment_id",
        entry.segment_id,
    )

    if (
        type(entry.offset) is not int
        or entry.offset < 0
    ):
        raise MAFObjectRuntimeInvalidEntryError(
            "offset must be a plain nonnegative int"
        )

    if (
        type(entry.length) is not int
        or entry.length <= 0
    ):
        raise MAFObjectRuntimeInvalidEntryError(
            "length must be a plain positive int"
        )

    _require_sha256(
        "object_file_sha256",
        entry.object_file_sha256,
    )
    _require_sha256(
        "payload_sha256",
        entry.payload_sha256,
    )

    if (
        type(entry.segment_length) is not int
        or entry.segment_length <= 0
    ):
        raise MAFObjectRuntimeInvalidEntryError(
            "segment_length must be a plain positive int"
        )

    _require_sha256(
        "segment_sha256",
        entry.segment_sha256,
    )

    _require_nonempty_str(
        "segment_path",
        entry.segment_path,
    )

    if (
        entry.offset
        + entry.length
        > entry.segment_length
    ):
        raise MAFObjectRuntimeInvalidEntryError(
            "object range exceeds segment_length"
        )

    return entry


class MAFObjectRuntime:
    """One model/generation-bound Phase 6C V1 residency runtime."""

    def __init__(
        self,
        *,
        model_pk: str,
        generation_pk: str,
        serialized_byte_budget: int,
        dense_byte_budget: int,
        dense_materializer: DenseMaterializer | None = None,
    ) -> None:
        if (
            type(model_pk) is not str
            or not model_pk
        ):
            raise ValueError(
                "model_pk must be a nonempty str"
            )

        if (
            type(generation_pk) is not str
            or not generation_pk
        ):
            raise ValueError(
                "generation_pk must be a nonempty str"
            )

        self._model_pk = model_pk
        self._generation_pk = generation_pk

        self._serialized_byte_budget = (
            _require_plain_nonnegative_int(
                "serialized_byte_budget",
                serialized_byte_budget,
            )
        )

        self._dense_byte_budget = (
            _require_plain_nonnegative_int(
                "dense_byte_budget",
                dense_byte_budget,
            )
        )

        if (
            dense_materializer is not None
            and not callable(
                dense_materializer
            )
        ):
            raise TypeError(
                "dense_materializer must be callable or None"
            )

        self._dense_materializer = (
            dense_materializer
        )

        self._lock = threading.RLock()

        self._records: dict[
            str,
            _RuntimeObjectRecord,
        ] = {}

        self._pins: dict[
            int,
            PinLease,
        ] = {}

        self._next_pin_token = 1

        self._serialized_resident_bytes = 0
        self._dense_resident_bytes = 0

        self._counters = {
            name: 0
            for name in _COUNTER_NAMES
        }

        self._callback_depth = 0
        self._closed = False

    def _require_mutation_allowed_locked(
        self,
    ) -> None:
        if self._closed:
            raise MAFObjectRuntimeClosedError(
                "runtime is closed"
            )

        if self._callback_depth:
            raise MAFObjectRuntimeReentrancyError(
                "recursive runtime mutation from callback is forbidden"
            )

    def _require_resource_access_locked(
        self,
    ) -> None:
        if self._closed:
            raise MAFObjectRuntimeClosedError(
                "runtime is closed"
            )

    def _require_record_locked(
        self,
        object_pk: str,
    ) -> _RuntimeObjectRecord:
        if type(object_pk) is not str:
            raise MAFObjectRuntimeUnknownObjectError(
                "object_pk must be str"
            )

        try:
            return self._records[
                object_pk
            ]
        except KeyError as exc:
            raise MAFObjectRuntimeUnknownObjectError(
                "runtime object is not registered"
            ) from exc

    def _effective_pin_floor_locked(
        self,
        record: _RuntimeObjectRecord,
    ) -> ResidencyState | None:
        if not record.pin_tokens:
            return None

        return max(
            (
                self._pins[token].minimum_state
                for token in record.pin_tokens
            ),
            key=lambda state: _STATE_RANK[state],
        )

    def _check_demotion_pin_floor_locked(
        self,
        record: _RuntimeObjectRecord,
        target: ResidencyState,
    ) -> None:
        floor = (
            self._effective_pin_floor_locked(
                record
            )
        )

        if (
            floor is not None
            and _STATE_RANK[target]
            < _STATE_RANK[floor]
        ):
            raise MAFObjectRuntimePinnedDemotionError(
                "demotion would cross active pin floor"
            )

    def _snapshot_object_locked(
        self,
        record: _RuntimeObjectRecord,
    ) -> RuntimeObjectSnapshot:
        return RuntimeObjectSnapshot(
            object_pk=record.entry.object_pk,
            state=record.state,
            pin_count=len(
                record.pin_tokens
            ),
            effective_pin_floor=(
                self._effective_pin_floor_locked(
                    record
                )
            ),
            serialized_resident_bytes=(
                len(record.serialized_bytes)
                if record.serialized_bytes
                is not None
                else 0
            ),
            dense_resident_bytes=(
                record.dense_byte_charge
                if record.state
                is ResidencyState.HOT_DENSE
                else 0
            ),
        )

    def _promote_hot_maf_locked(
        self,
        record: _RuntimeObjectRecord,
    ) -> None:
        try:
            serialized = (
                read_serialized_object(
                    record.entry,
                    self._generation_pk,
                )
            )

        except MAFSegmentReaderError as exc:
            self._counters[
                "verification_failures"
            ] += 1

            raise MAFObjectRuntimeVerifiedReadError(
                "verified Segment Reader promotion failed"
            ) from exc

        if type(serialized) is not bytes:
            self._counters[
                "verification_failures"
            ] += 1

            raise MAFObjectRuntimeVerifiedReadError(
                "Segment Reader did not return immutable bytes"
            )

        if (
            len(serialized)
            != record.entry.length
        ):
            self._counters[
                "verification_failures"
            ] += 1

            raise MAFObjectRuntimeVerifiedReadError(
                "verified byte length differs from ResidentPKEntry"
            )

        resulting = (
            self._serialized_resident_bytes
            + len(serialized)
        )

        if (
            resulting
            > self._serialized_byte_budget
        ):
            self._counters[
                "budget_rejections"
            ] += 1

            raise MAFObjectRuntimeSerializedBudgetExceededError(
                "serialized resident-byte budget exceeded"
            )

        # Commit point.
        record.serialized_bytes = serialized
        record.state = ResidencyState.HOT_MAF

        self._serialized_resident_bytes = (
            resulting
        )

        self._counters[
            "successful_verified_byte_promotions"
        ] += 1

    def _promote_hot_dense_locked(
        self,
        record: _RuntimeObjectRecord,
    ) -> None:
        if (
            self._dense_materializer
            is None
        ):
            raise MAFObjectRuntimeDenseMaterializationError(
                "no dense materializer is configured"
            )

        serialized = (
            record.serialized_bytes
        )

        if serialized is None:
            raise MAFObjectRuntimeDenseMaterializationError(
                "HOT_MAF serialized bytes are unavailable"
            )

        try:
            self._callback_depth += 1

            result = (
                self._dense_materializer(
                    record.entry,
                    serialized,
                )
            )

        except MAFObjectRuntimeReentrancyError:
            raise

        except Exception as exc:
            raise MAFObjectRuntimeDenseMaterializationError(
                "dense materializer raised"
            ) from exc

        finally:
            self._callback_depth -= 1

        if (
            type(result) is not tuple
            or len(result) != 2
        ):
            raise MAFObjectRuntimeDenseMaterializationError(
                "dense materializer must return (view, exact_byte_charge)"
            )

        dense_view, dense_charge = result

        if dense_view is None:
            raise MAFObjectRuntimeDenseMaterializationError(
                "dense materializer returned no view"
            )

        if (
            type(dense_charge) is not int
            or dense_charge < 0
        ):
            raise MAFObjectRuntimeDenseMaterializationError(
                "dense byte charge must be a plain nonnegative int"
            )

        resulting = (
            self._dense_resident_bytes
            + dense_charge
        )

        if (
            resulting
            > self._dense_byte_budget
        ):
            self._counters[
                "budget_rejections"
            ] += 1

            raise MAFObjectRuntimeDenseBudgetExceededError(
                "dense resident-byte budget exceeded"
            )

        # Commit point.
        record.dense_view = dense_view
        record.dense_byte_charge = (
            dense_charge
        )
        record.state = (
            ResidencyState.HOT_DENSE
        )

        self._dense_resident_bytes = (
            resulting
        )

        self._counters[
            "successful_dense_materializations"
        ] += 1

    def _apply_primitive_locked(
        self,
        record: _RuntimeObjectRecord,
        target: ResidencyState,
    ) -> None:
        current = record.state

        if current is target:
            return

        pair = (
            current,
            target,
        )

        if pair == (
            ResidencyState.COLD_DISK,
            ResidencyState.MAPPED,
        ):
            # MAPPED is backend-neutral attachment state.
            record.state = (
                ResidencyState.MAPPED
            )

            self._counters[
                "successful_attach_transitions"
            ] += 1

            return

        if pair == (
            ResidencyState.MAPPED,
            ResidencyState.HOT_MAF,
        ):
            self._promote_hot_maf_locked(
                record
            )
            return

        if pair == (
            ResidencyState.HOT_MAF,
            ResidencyState.HOT_DENSE,
        ):
            self._promote_hot_dense_locked(
                record
            )
            return

        if pair == (
            ResidencyState.HOT_DENSE,
            ResidencyState.HOT_MAF,
        ):
            self._check_demotion_pin_floor_locked(
                record,
                target,
            )

            charge = (
                record.dense_byte_charge
            )

            # Commit point.
            record.dense_view = None
            record.dense_byte_charge = 0
            record.state = (
                ResidencyState.HOT_MAF
            )

            self._dense_resident_bytes -= (
                charge
            )

            self._counters[
                "successful_dense_demotions"
            ] += 1

            return

        if pair == (
            ResidencyState.HOT_MAF,
            ResidencyState.MAPPED,
        ):
            self._check_demotion_pin_floor_locked(
                record,
                target,
            )

            serialized = (
                record.serialized_bytes
            )

            if serialized is None:
                raise MAFObjectRuntimeResidencyUnavailableError(
                    "HOT_MAF record lacks verified serialized bytes"
                )

            charge = len(serialized)

            # Commit point.
            record.serialized_bytes = None
            record.state = (
                ResidencyState.MAPPED
            )

            self._serialized_resident_bytes -= (
                charge
            )

            self._counters[
                "successful_serialized_byte_demotions"
            ] += 1

            return

        if pair == (
            ResidencyState.MAPPED,
            ResidencyState.COLD_DISK,
        ):
            self._check_demotion_pin_floor_locked(
                record,
                target,
            )

            # Commit point.
            record.state = (
                ResidencyState.COLD_DISK
            )

            self._counters[
                "successful_detach_transitions"
            ] += 1

            return

        raise MAFObjectRuntimeIllegalTransitionError(
            f"illegal primitive transition: "
            f"{current.value} -> {target.value}"
        )

    def _ensure_state_locked(
        self,
        record: _RuntimeObjectRecord,
        target: ResidencyState,
    ) -> None:
        while record.state is not target:
            current_rank = (
                _STATE_RANK[
                    record.state
                ]
            )
            target_rank = (
                _STATE_RANK[target]
            )

            if current_rank < target_rank:
                next_state = ResidencyState(
                    (
                        "MAPPED",
                        "HOT_MAF",
                        "HOT_DENSE",
                    )[current_rank]
                )

            else:
                next_state = ResidencyState(
                    (
                        "COLD_DISK",
                        "MAPPED",
                        "HOT_MAF",
                    )[current_rank - 1]
                )

            self._apply_primitive_locked(
                record,
                next_state,
            )

    def register_entry(
        self,
        entry: ResidentPKEntry,
    ) -> RuntimeObjectSnapshot:
        with self._lock:
            self._require_mutation_allowed_locked()

            entry = (
                _validate_entry_structure(
                    entry
                )
            )

            if (
                entry.model_pk
                != self._model_pk
                or entry.generation_pk
                != self._generation_pk
            ):
                raise MAFObjectRuntimeStaleGenerationError(
                    "entry model/generation differs from runtime binding"
                )

            if (
                entry.object_pk
                in self._records
            ):
                raise MAFObjectRuntimeInvalidEntryError(
                    "object_pk is already registered"
                )

            record = _RuntimeObjectRecord(
                entry=entry,
            )

            self._records[
                entry.object_pk
            ] = record

            return (
                self._snapshot_object_locked(
                    record
                )
            )

    def state(
        self,
        object_pk: str,
    ) -> ResidencyState:
        with self._lock:
            return (
                self._require_record_locked(
                    object_pk
                ).state
            )

    def transition(
        self,
        object_pk: str,
        target: ResidencyState | str,
    ) -> RuntimeObjectSnapshot:
        with self._lock:
            try:
                self._require_mutation_allowed_locked()

                record = (
                    self._require_record_locked(
                        object_pk
                    )
                )

                target_state = (
                    _coerce_state(
                        target
                    )
                )

                self._apply_primitive_locked(
                    record,
                    target_state,
                )

                return (
                    self._snapshot_object_locked(
                        record
                    )
                )

            except MAFObjectRuntimeError:
                self._counters[
                    "failed_transitions"
                ] += 1
                raise

    def ensure_state(
        self,
        object_pk: str,
        target: ResidencyState | str,
    ) -> RuntimeObjectSnapshot:
        with self._lock:
            try:
                self._require_mutation_allowed_locked()

                record = (
                    self._require_record_locked(
                        object_pk
                    )
                )

                target_state = (
                    _coerce_state(
                        target
                    )
                )

                self._ensure_state_locked(
                    record,
                    target_state,
                )

                return (
                    self._snapshot_object_locked(
                        record
                    )
                )

            except MAFObjectRuntimeError:
                self._counters[
                    "failed_transitions"
                ] += 1
                raise

    def pin(
        self,
        object_pk: str,
        minimum_state: ResidencyState | str,
    ) -> PinLease:
        with self._lock:
            self._require_mutation_allowed_locked()

            record = (
                self._require_record_locked(
                    object_pk
                )
            )

            floor = _coerce_state(
                minimum_state
            )

            if (
                floor
                is ResidencyState.COLD_DISK
            ):
                raise MAFObjectRuntimeInvalidPinError(
                    "COLD_DISK is not a valid pin floor"
                )

            if (
                _STATE_RANK[record.state]
                < _STATE_RANK[floor]
            ):
                try:
                    self._ensure_state_locked(
                        record,
                        floor,
                    )
                except MAFObjectRuntimeError:
                    self._counters[
                        "failed_transitions"
                    ] += 1
                    raise

            token = (
                self._next_pin_token
            )

            self._next_pin_token += 1

            lease = PinLease(
                token=token,
                object_pk=object_pk,
                minimum_state=floor,
            )

            self._pins[
                token
            ] = lease

            record.pin_tokens.add(
                token
            )

            self._counters[
                "successful_pin_acquisitions"
            ] += 1

            return lease

    def unpin(
        self,
        token: int,
    ) -> None:
        with self._lock:
            self._require_mutation_allowed_locked()

            if type(token) is not int:
                raise MAFObjectRuntimePinTokenError(
                    "pin token must be an opaque runtime int token"
                )

            try:
                lease = self._pins.pop(
                    token
                )
            except KeyError as exc:
                raise MAFObjectRuntimePinTokenError(
                    "pin token is unknown or already consumed"
                ) from exc

            record = (
                self._require_record_locked(
                    lease.object_pk
                )
            )

            record.pin_tokens.remove(
                token
            )

            self._counters[
                "successful_unpins"
            ] += 1

    def serialized_bytes(
        self,
        object_pk: str,
    ) -> bytes:
        with self._lock:
            self._require_resource_access_locked()

            record = (
                self._require_record_locked(
                    object_pk
                )
            )

            if record.state not in (
                ResidencyState.HOT_MAF,
                ResidencyState.HOT_DENSE,
            ):
                raise MAFObjectRuntimeResidencyUnavailableError(
                    "verified serialized bytes are not resident"
                )

            serialized = (
                record.serialized_bytes
            )

            if serialized is None:
                raise MAFObjectRuntimeResidencyUnavailableError(
                    "verified serialized bytes are unavailable"
                )

            return serialized

    def dense_view(
        self,
        object_pk: str,
    ) -> Any:
        with self._lock:
            self._require_resource_access_locked()

            record = (
                self._require_record_locked(
                    object_pk
                )
            )

            if (
                record.state
                is not ResidencyState.HOT_DENSE
                or record.dense_view
                is None
            ):
                raise MAFObjectRuntimeResidencyUnavailableError(
                    "dense view is not resident"
                )

            return record.dense_view

    def snapshot(
        self,
    ) -> RuntimeSnapshot:
        with self._lock:
            objects = tuple(
                self._snapshot_object_locked(
                    self._records[object_pk]
                )
                for object_pk
                in sorted(self._records)
            )

            counts = {
                state: 0
                for state
                in ResidencyState
            }

            for item in objects:
                counts[
                    item.state
                ] += 1

            return RuntimeSnapshot(
                model_pk=self._model_pk,
                generation_pk=self._generation_pk,
                closed=self._closed,
                object_count=len(objects),
                cold_disk_count=counts[
                    ResidencyState.COLD_DISK
                ],
                mapped_count=counts[
                    ResidencyState.MAPPED
                ],
                hot_maf_count=counts[
                    ResidencyState.HOT_MAF
                ],
                hot_dense_count=counts[
                    ResidencyState.HOT_DENSE
                ],
                active_pin_leases=len(
                    self._pins
                ),
                serialized_resident_bytes=(
                    self._serialized_resident_bytes
                ),
                dense_resident_bytes=(
                    self._dense_resident_bytes
                ),
                counters=tuple(
                    sorted(
                        self._counters.items()
                    )
                ),
                objects=objects,
            )

    def close(
        self,
    ) -> None:
        with self._lock:
            if self._closed:
                return

            if self._callback_depth:
                raise MAFObjectRuntimeReentrancyError(
                    "runtime close from callback is forbidden"
                )

            # Close invalidates active pin leases.
            self._pins.clear()

            for record in self._records.values():
                record.pin_tokens.clear()

                if (
                    record.state
                    is ResidencyState.HOT_DENSE
                ):
                    self._dense_resident_bytes -= (
                        record.dense_byte_charge
                    )

                    record.dense_view = None
                    record.dense_byte_charge = 0
                    record.state = (
                        ResidencyState.HOT_MAF
                    )

                    self._counters[
                        "successful_dense_demotions"
                    ] += 1

                if (
                    record.state
                    is ResidencyState.HOT_MAF
                ):
                    serialized = (
                        record.serialized_bytes
                    )

                    if serialized is not None:
                        self._serialized_resident_bytes -= (
                            len(serialized)
                        )

                    record.serialized_bytes = None
                    record.state = (
                        ResidencyState.MAPPED
                    )

                    self._counters[
                        "successful_serialized_byte_demotions"
                    ] += 1

                if (
                    record.state
                    is ResidencyState.MAPPED
                ):
                    record.state = (
                        ResidencyState.COLD_DISK
                    )

                    self._counters[
                        "successful_detach_transitions"
                    ] += 1

            if (
                self._serialized_resident_bytes
                != 0
                or self._dense_resident_bytes
                != 0
            ):
                raise MAFObjectRuntimeError(
                    "runtime close accounting did not return to zero"
                )

            self._closed = True


__all__ = [
    "MAFObjectRuntimeError",
    "MAFObjectRuntimeInvalidEntryError",
    "MAFObjectRuntimeStaleGenerationError",
    "MAFObjectRuntimeUnknownObjectError",
    "MAFObjectRuntimeIllegalTransitionError",
    "MAFObjectRuntimePinnedDemotionError",
    "MAFObjectRuntimePinTokenError",
    "MAFObjectRuntimeInvalidPinError",
    "MAFObjectRuntimeSerializedBudgetExceededError",
    "MAFObjectRuntimeDenseBudgetExceededError",
    "MAFObjectRuntimeVerifiedReadError",
    "MAFObjectRuntimeDenseMaterializationError",
    "MAFObjectRuntimeClosedError",
    "MAFObjectRuntimeReentrancyError",
    "MAFObjectRuntimeResidencyUnavailableError",
    "ResidencyState",
    "PinLease",
    "RuntimeObjectSnapshot",
    "RuntimeSnapshot",
    "MAFObjectRuntime",
]
