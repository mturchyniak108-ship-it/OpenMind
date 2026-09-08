#!/usr/bin/env python3
"""Phase 6D Runtime Telemetry Integration V1.

Composition-only adapter between the frozen Phase 6C MAFObjectRuntime and the
frozen Phase 6D TelemetryAccumulator.

This module is implementation only. It does not authorize scientific telemetry
collection, persistence, repacking, benchmarking, Phase 6D-Q, or Phase 6E.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, TypeVar

import maf_object_runtime_residency_v1 as _runtime
import maf_segment_locality_data_model_v1 as _model


INTEGRATION_VERSION = "v1.1"

INTEGRATION_PROTOCOL_SHA256 = "98f86d72ce2119e76349360d801c39b8184bbad2ec6f968fda4047fd132944ec"

FROZEN_RUNTIME_SHA256 = (
    "4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9"
)

FROZEN_DATA_MODEL_SHA256 = (
    "5432f2d74a610f2d0f9181e9af146013bb198a4e837af634993909358fff8ad0"
)

SERIALIZED_RESIDENCY_CACHE = (
    "runtime.serialized_residency"
)

DENSE_RESIDENCY_CACHE = (
    "runtime.dense_residency"
)


class MAFSegmentLocalityRuntimeTelemetryIntegrationError(
    RuntimeError
):
    """Base Integration V1 error."""


class MAFSegmentLocalityRuntimeTelemetryAttachmentError(
    MAFSegmentLocalityRuntimeTelemetryIntegrationError
):
    """The wrapped runtime is not a clean V1 attachment target."""


class MAFSegmentLocalityRuntimeTelemetryFaultedError(
    MAFSegmentLocalityRuntimeTelemetryIntegrationError
):
    """Scientific telemetry export is forbidden for a faulted trace."""


@dataclass(
    frozen=True,
    slots=True,
)
class TelemetryFaultDiagnostics:
    faulted: bool
    fault_count: int
    first_exception_type: str | None
    first_exception_message: str | None


_T = TypeVar("_T")


_STATE_ORDER = (
    _runtime.ResidencyState.COLD_DISK,
    _runtime.ResidencyState.MAPPED,
    _runtime.ResidencyState.HOT_MAF,
    _runtime.ResidencyState.HOT_DENSE,
)

_STATE_RANK = {
    state: index
    for index, state in enumerate(_STATE_ORDER)
}


class MAFSegmentLocalityRuntimeTelemetryAdapter:
    """Composition adapter for one pristine frozen Phase 6C runtime."""

    __slots__ = (
        "_runtime",
        "_accumulator",
        "_source_manifest_sha256",
        "_next_sequence",
        "_registered_lengths",
        "_registration_order",
        "_faulted",
        "_fault_count",
        "_first_fault_type",
        "_first_fault_message",
    )

    def __init__(
        self,
        runtime: _runtime.MAFObjectRuntime,
        *,
        source_manifest_sha256: str,
    ) -> None:
        if type(runtime) is not _runtime.MAFObjectRuntime:
            raise TypeError(
                "runtime must be an exact MAFObjectRuntime instance"
            )

        snapshot = runtime.snapshot()

        counters_zero = all(
            value == 0
            for _, value in snapshot.counters
        )

        if (
            snapshot.closed
            or snapshot.object_count != 0
            or snapshot.cold_disk_count != 0
            or snapshot.mapped_count != 0
            or snapshot.hot_maf_count != 0
            or snapshot.hot_dense_count != 0
            or snapshot.active_pin_leases != 0
            or snapshot.serialized_resident_bytes != 0
            or snapshot.dense_resident_bytes != 0
            or not counters_zero
        ):
            raise (
                MAFSegmentLocalityRuntimeTelemetryAttachmentError(
                    "runtime must be pristine, open, empty, unpinned, "
                    "unresident, and have all counters equal to zero"
                )
            )

        self._runtime = runtime

        self._accumulator = _model.TelemetryAccumulator(
            model_pk=snapshot.model_pk,
            source_generation_pk=snapshot.generation_pk,
            source_manifest_sha256=source_manifest_sha256,
        )

        self._source_manifest_sha256 = (
            source_manifest_sha256
        )

        self._next_sequence = 1

        self._registered_lengths: dict[
            str,
            int,
        ] = {}

        self._registration_order: list[str] = []

        self._faulted = False
        self._fault_count = 0
        self._first_fault_type = None
        self._first_fault_message = None

    # --------------------------------------------------------
    # TELEMETRY FAULT ISOLATION
    # --------------------------------------------------------

    def _mark_telemetry_fault(
        self,
        exc: Exception,
    ) -> None:
        self._fault_count += 1

        if not self._faulted:
            self._faulted = True
            self._first_fault_type = (
                f"{type(exc).__module__}."
                f"{type(exc).__qualname__}"
            )
            self._first_fault_message = str(exc)

    def _telemetry_step(
        self,
        fn: Callable[[], None],
    ) -> None:
        if self._faulted:
            return

        try:
            fn()
        except Exception as exc:
            self._mark_telemetry_fault(
                exc
            )

    def _emit(
        self,
        kind: _model.TelemetryEventKind,
        object_pk: str,
        *,
        byte_count: int | None = None,
        cache_name: str | None = None,
        from_state: str | None = None,
        to_state: str | None = None,
        prefetch_id: str | None = None,
    ) -> None:
        if self._faulted:
            return

        sequence = self._next_sequence

        try:
            event = _model.TelemetryEvent(
                sequence=sequence,
                kind=kind,
                object_pk=object_pk,
                byte_count=byte_count,
                cache_name=cache_name,
                from_state=from_state,
                to_state=to_state,
                prefetch_id=prefetch_id,
            )

            self._accumulator.add_event(
                event
            )

        except Exception as exc:
            self._mark_telemetry_fault(
                exc
            )
            return

        self._next_sequence += 1

    # --------------------------------------------------------
    # OBSERVATION HELPERS
    # --------------------------------------------------------

    def _capture_runtime_snapshot(
        self,
    ) -> Any | None:
        if self._faulted:
            return None

        try:
            return self._runtime.snapshot()
        except Exception as exc:
            self._mark_telemetry_fault(
                exc
            )
            return None

    @staticmethod
    def _state_map(
        snapshot: Any,
    ) -> dict[str, _runtime.ResidencyState]:
        return {
            item.object_pk: item.state
            for item in snapshot.objects
        }

    def _registered_object_sets_match(
        self,
        snapshot: Any,
    ) -> bool:
        runtime_pks = {
            item.object_pk
            for item in snapshot.objects
        }

        adapter_pks = set(
            self._registered_lengths
        )

        return runtime_pks == adapter_pks

    def _primitive_path(
        self,
        before: _runtime.ResidencyState,
        after: _runtime.ResidencyState,
    ) -> tuple[
        tuple[
            _runtime.ResidencyState,
            _runtime.ResidencyState,
        ],
        ...,
    ]:
        start = _STATE_RANK[before]
        end = _STATE_RANK[after]

        if start == end:
            return ()

        step = 1 if end > start else -1

        pairs = []

        current = start

        while current != end:
            nxt = current + step

            pairs.append(
                (
                    _STATE_ORDER[current],
                    _STATE_ORDER[nxt],
                )
            )

            current = nxt

        return tuple(pairs)

    def _emit_primitive(
        self,
        object_pk: str,
        before: _runtime.ResidencyState,
        after: _runtime.ResidencyState,
    ) -> None:
        before_name = before.value
        after_name = after.value

        if (
            before is _runtime.ResidencyState.COLD_DISK
            and after is _runtime.ResidencyState.MAPPED
        ):
            self._emit(
                _model.TelemetryEventKind.PROMOTION,
                object_pk,
                from_state=before_name,
                to_state=after_name,
            )
            return

        if (
            before is _runtime.ResidencyState.MAPPED
            and after is _runtime.ResidencyState.HOT_MAF
        ):
            try:
                byte_count = self._registered_lengths[
                    object_pk
                ]
            except KeyError as exc:
                self._mark_telemetry_fault(
                    MAFSegmentLocalityRuntimeTelemetryIntegrationError(
                        "committed HOT_MAF promotion references an "
                        "object not registered through the adapter"
                    )
                )
                return

            self._emit(
                _model.TelemetryEventKind.BYTES_READ,
                object_pk,
                byte_count=byte_count,
            )

            self._emit(
                _model.TelemetryEventKind.PROMOTION,
                object_pk,
                from_state=before_name,
                to_state=after_name,
            )
            return

        if (
            before is _runtime.ResidencyState.HOT_MAF
            and after is _runtime.ResidencyState.HOT_DENSE
        ):
            self._emit(
                _model.TelemetryEventKind.MATERIALIZATION,
                object_pk,
            )

            self._emit(
                _model.TelemetryEventKind.PROMOTION,
                object_pk,
                from_state=before_name,
                to_state=after_name,
            )
            return

        if _STATE_RANK[after] < _STATE_RANK[before]:
            self._emit(
                _model.TelemetryEventKind.DEMOTION,
                object_pk,
                from_state=before_name,
                to_state=after_name,
            )
            return

        self._mark_telemetry_fault(
            MAFSegmentLocalityRuntimeTelemetryIntegrationError(
                "observed non-primitive or unsupported runtime transition"
            )
        )

    def _observe_state_delta(
        self,
        before_snapshot: Any | None,
        after_snapshot: Any | None,
        object_order: tuple[str, ...],
    ) -> None:
        if (
            self._faulted
            or before_snapshot is None
            or after_snapshot is None
        ):
            return

        if not self._registered_object_sets_match(
            before_snapshot
        ):
            self._mark_telemetry_fault(
                MAFSegmentLocalityRuntimeTelemetryIntegrationError(
                    "runtime object inventory differs from adapter "
                    "registration inventory before delegated operation"
                )
            )
            return

        if not self._registered_object_sets_match(
            after_snapshot
        ):
            self._mark_telemetry_fault(
                MAFSegmentLocalityRuntimeTelemetryIntegrationError(
                    "runtime object inventory differs from adapter "
                    "registration inventory after delegated operation"
                )
            )
            return

        before_states = self._state_map(
            before_snapshot
        )

        after_states = self._state_map(
            after_snapshot
        )

        for object_pk in object_order:
            if self._faulted:
                return

            if (
                object_pk not in before_states
                or object_pk not in after_states
            ):
                self._mark_telemetry_fault(
                    MAFSegmentLocalityRuntimeTelemetryIntegrationError(
                        "observed object missing from runtime snapshot"
                    )
                )
                return

            path = self._primitive_path(
                before_states[object_pk],
                after_states[object_pk],
            )

            for state_before, state_after in path:
                self._emit_primitive(
                    object_pk,
                    state_before,
                    state_after,
                )

                if self._faulted:
                    return

    def _delegate_observed(
        self,
        fn: Callable[[], _T],
        *,
        object_order: tuple[str, ...],
    ) -> _T:
        before = self._capture_runtime_snapshot()

        try:
            result = fn()
        except Exception:
            after = self._capture_runtime_snapshot()

            self._observe_state_delta(
                before,
                after,
                object_order,
            )

            # Preserve the original delegated runtime exception.
            raise

        after = self._capture_runtime_snapshot()

        self._observe_state_delta(
            before,
            after,
            object_order,
        )

        # Telemetry failure is deliberately not raised here.
        return result

    def _resource_access_eligible(
        self,
        object_pk: Any,
        before_snapshot: Any | None,
    ) -> bool:
        if (
            before_snapshot is None
            or self._faulted
            or before_snapshot.closed
            or type(object_pk) is not str
        ):
            return False

        return (
            object_pk
            in self._registered_lengths
        )

    def _emit_access_and_cache(
        self,
        *,
        object_pk: str,
        cache_name: str,
        hit: bool,
    ) -> None:
        self._emit(
            _model.TelemetryEventKind.ACCESS,
            object_pk,
        )

        self._emit(
            (
                _model.TelemetryEventKind.CACHE_HIT
                if hit
                else _model.TelemetryEventKind.CACHE_MISS
            ),
            object_pk,
            cache_name=cache_name,
        )

    # --------------------------------------------------------
    # FROZEN RUNTIME PUBLIC SURFACE
    # --------------------------------------------------------

    def register_entry(
        self,
        entry: Any,
    ) -> Any:
        if (
            entry.generation_manifest_sha256
            != self._source_manifest_sha256
        ):
            raise (
                MAFSegmentLocalityRuntimeTelemetryIntegrationError(
                    "entry generation manifest differs from "
                    "adapter source manifest binding"
                )
            )

        result = self._runtime.register_entry(
            entry
        )

        def commit_registration() -> None:
            object_pk = entry.object_pk
            length = entry.length

            if object_pk in self._registered_lengths:
                raise (
                    MAFSegmentLocalityRuntimeTelemetryIntegrationError(
                        "adapter registration inventory contains duplicate object"
                    )
                )

            self._registered_lengths[
                object_pk
            ] = length

            self._registration_order.append(
                object_pk
            )

        self._telemetry_step(
            commit_registration
        )

        return result

    def state(
        self,
        object_pk: str,
    ) -> _runtime.ResidencyState:
        return self._runtime.state(
            object_pk
        )

    def transition(
        self,
        object_pk: str,
        target: _runtime.ResidencyState | str,
    ) -> Any:
        return self._delegate_observed(
            lambda: self._runtime.transition(
                object_pk,
                target,
            ),
            object_order=(object_pk,),
        )

    def ensure_state(
        self,
        object_pk: str,
        target: _runtime.ResidencyState | str,
    ) -> Any:
        return self._delegate_observed(
            lambda: self._runtime.ensure_state(
                object_pk,
                target,
            ),
            object_order=(object_pk,),
        )

    def pin(
        self,
        object_pk: str,
        minimum_state: _runtime.ResidencyState | str,
    ) -> Any:
        return self._delegate_observed(
            lambda: self._runtime.pin(
                object_pk,
                minimum_state,
            ),
            object_order=(object_pk,),
        )

    def unpin(
        self,
        token: int,
    ) -> None:
        return self._runtime.unpin(
            token
        )

    def serialized_bytes(
        self,
        object_pk: str,
    ) -> bytes:
        before = self._capture_runtime_snapshot()

        eligible = self._resource_access_eligible(
            object_pk,
            before,
        )

        try:
            result = self._runtime.serialized_bytes(
                object_pk
            )

        except (
            _runtime.MAFObjectRuntimeResidencyUnavailableError
        ):
            if eligible:
                self._emit_access_and_cache(
                    object_pk=object_pk,
                    cache_name=SERIALIZED_RESIDENCY_CACHE,
                    hit=False,
                )

            raise

        if eligible:
            self._emit_access_and_cache(
                object_pk=object_pk,
                cache_name=SERIALIZED_RESIDENCY_CACHE,
                hit=True,
            )

        return result

    def dense_view(
        self,
        object_pk: str,
    ) -> Any:
        before = self._capture_runtime_snapshot()

        eligible = self._resource_access_eligible(
            object_pk,
            before,
        )

        try:
            result = self._runtime.dense_view(
                object_pk
            )

        except (
            _runtime.MAFObjectRuntimeResidencyUnavailableError
        ):
            if eligible:
                self._emit_access_and_cache(
                    object_pk=object_pk,
                    cache_name=DENSE_RESIDENCY_CACHE,
                    hit=False,
                )

            raise

        if eligible:
            self._emit_access_and_cache(
                object_pk=object_pk,
                cache_name=DENSE_RESIDENCY_CACHE,
                hit=True,
            )

        return result

    def snapshot(
        self,
    ) -> Any:
        return self._runtime.snapshot()

    def close(
        self,
    ) -> None:
        order = tuple(
            self._registration_order
        )

        return self._delegate_observed(
            self._runtime.close,
            object_order=order,
        )

    # --------------------------------------------------------
    # DERIVED TELEMETRY SURFACE
    # --------------------------------------------------------

    def telemetry_snapshot(
        self,
    ) -> _model.TelemetrySnapshot:
        if self._faulted:
            raise (
                MAFSegmentLocalityRuntimeTelemetryFaultedError(
                    "telemetry trace is faulted; scientific snapshot "
                    "export is forbidden"
                )
            )

        return self._accumulator.snapshot()

    def telemetry_fault_diagnostics(
        self,
    ) -> TelemetryFaultDiagnostics:
        return TelemetryFaultDiagnostics(
            faulted=self._faulted,
            fault_count=self._fault_count,
            first_exception_type=self._first_fault_type,
            first_exception_message=(
                self._first_fault_message
            ),
        )


__all__ = [
    "INTEGRATION_VERSION",
    "INTEGRATION_PROTOCOL_SHA256",
    "FROZEN_RUNTIME_SHA256",
    "FROZEN_DATA_MODEL_SHA256",
    "SERIALIZED_RESIDENCY_CACHE",
    "DENSE_RESIDENCY_CACHE",
    "MAFSegmentLocalityRuntimeTelemetryIntegrationError",
    "MAFSegmentLocalityRuntimeTelemetryAttachmentError",
    "MAFSegmentLocalityRuntimeTelemetryFaultedError",
    "TelemetryFaultDiagnostics",
    "MAFSegmentLocalityRuntimeTelemetryAdapter",
]
