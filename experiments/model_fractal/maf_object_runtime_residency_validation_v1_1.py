#!/usr/bin/env python3
"""Exact-once Phase 6C MAF Object Runtime and Residency V1.1 validation."""

from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path
import shutil
import threading
from typing import Any, Callable

import maf_object_runtime_residency_v1 as runtime_mod

from maf_object_runtime_residency_v1 import (
    MAFObjectRuntime,
    MAFObjectRuntimeClosedError,
    MAFObjectRuntimeDenseBudgetExceededError,
    MAFObjectRuntimeDenseMaterializationError,
    MAFObjectRuntimeIllegalTransitionError,
    MAFObjectRuntimePinTokenError,
    MAFObjectRuntimePinnedDemotionError,
    MAFObjectRuntimeResidencyUnavailableError,
    MAFObjectRuntimeSerializedBudgetExceededError,
    MAFObjectRuntimeStaleGenerationError,
    MAFObjectRuntimeVerifiedReadError,
    ResidencyState,
)
from maf_resident_pk_directory_v1 import (
    ResidentPKEntry,
    build_snapshot,
)
from maf_segment_reader_v1 import (
    MAFSegmentReaderShortReadError,
)


SCHEMA = "openmind.maf_object_runtime_residency_validation.v1.1"

DESIGN_PROTOCOL_PATH = Path(
    "experiments/model_fractal/"
    "MAF_OBJECT_RUNTIME_RESIDENCY_V1_PROTOCOL.md"
)
DESIGN_PROTOCOL_SHA256 = (
    "81987d00ef4cb51556dcebf08bff9c9fa8979f033df05304d347b759e545eb13"
)

ENGINE_PATH = Path(
    "experiments/model_fractal/"
    "maf_object_runtime_residency_v1.py"
)
ENGINE_SHA256 = (
    "4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9"
)

VALID_PROTOCOL_PATH = Path(
    "experiments/model_fractal/"
    "MAF_OBJECT_RUNTIME_RESIDENCY_VALIDATION_V1_1_PROTOCOL.md"
)
VALID_PROTOCOL_SHA256 = (
    "e93ea0f418fc25a01573aad6d23b8d3f999be73b932828596b47ed6548128681"
)

RESIDENT_PATH = Path(
    "experiments/model_fractal/"
    "maf_resident_pk_directory_v1.py"
)
RESIDENT_SHA256 = (
    "4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6"
)

READER_PATH = Path(
    "experiments/model_fractal/"
    "maf_segment_reader_v1.py"
)
READER_SHA256 = (
    "3499cb8e528fe8e9315e3e5656d6aa888c95ca175310b6371e722de409827369"
)

RESULT_PATH = Path(
    "experiments/model_fractal/"
    "maf_object_runtime_residency_validation_v1_1.json"
)

SOURCE_RUNTIME = Path(
    "results/runtime/"
    "maf_resident_pk_directory_benchmark_v1_1"
)

VALIDATION_RUNTIME = Path(
    "results/runtime/"
    "maf_object_runtime_residency_validation_v1_1"
)

SOURCE_FILE_EXPECTATIONS = {
    "active_generation.json": {
        "size": 380,
        "sha256": (
            "031d1a50a3cf53f158057a02bb6c68001edfb07bf48bf893afc9bc8f095458e9"
        ),
    },
    "candidate_a.manifest.json": {
        "size": 1202,
        "sha256": (
            "941301aa362d3f949389e5364b1be4d7f26b96f0d45efa81346c82fce3260f93"
        ),
    },
    "segment_00000000.mafseg": {
        "size": 4096,
        "sha256": (
            "f965b526538d757ca2d6114af6517c57cbcb3650b71d8cfb92046a04ef2f566b"
        ),
    },
}

PROMOTION_RACE_REPETITIONS = 16
PIN_THREAD_COUNT = 8
JOIN_TIMEOUT_SECONDS = 10.0

CHECK_NAMES = (
    "V01_runtime_binding",
    "V02_initial_cold_disk",
    "V03_legal_upward_primitive_transitions",
    "V04_legal_downward_primitive_transitions",
    "V05_illegal_skipped_transitions",
    "V06_same_state_idempotence",
    "V07_verified_hot_maf_promotion",
    "V08_corruption_hash_failure_nonpublication",
    "V09_short_read_nonpublication",
    "V10_stale_generation_rejection",
    "V11_serialized_byte_accounting",
    "V12_dense_byte_accounting",
    "V13_zero_budget_rejection",
    "V14_over_budget_failure_atomicity",
    "V15_multiple_pin_floor_composition",
    "V16_pinned_demotion_rejected",
    "V17_unknown_pin_rejection",
    "V18_consumed_pin_rejection",
    "V19_unpin_no_automatic_demotion",
    "V20_dense_materialization_success",
    "V21_dense_materialization_failure_atomicity",
    "V22_dense_view_lifetime_invalidation",
    "V23_runtime_close_cleanup",
    "V24_close_idempotence",
    "V25_operation_rejection_after_close",
    "V26_source_file_immutability",
    "V27_no_unverified_byte_escape",
    "V28_snapshot_accounting_consistency",
    "V29_concurrent_same_object_promotion",
    "V30_concurrent_pin_unpin_accounting",
    "V31_concurrent_observation_no_provisional_state",
    "V32_promotion_race_no_duplicate_ownership",
)


class ValidationHarnessError(RuntimeError):
    pass


class ExpectedDenseFailure(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        while True:
            chunk = f.read(8 * 1024 * 1024)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()


def file_identity(path: Path) -> dict[str, Any]:
    return {
        "size": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def runtime_inventory(path: Path) -> dict[str, dict[str, Any]]:
    result = {}

    if not path.is_dir():
        return result

    for item in sorted(path.rglob("*")):
        if item.is_file():
            result[str(item.relative_to(path))] = file_identity(item)

    return result


def frozen_identities() -> dict[str, str]:
    return {
        "design_protocol_sha256": sha256_file(DESIGN_PROTOCOL_PATH),
        "engine_sha256": sha256_file(ENGINE_PATH),
        "validation_protocol_sha256": sha256_file(VALID_PROTOCOL_PATH),
        "resident_pk_directory_sha256": sha256_file(RESIDENT_PATH),
        "segment_reader_sha256": sha256_file(READER_PATH),
    }


def assert_frozen_exact(observed: dict[str, str]) -> None:
    expected = {
        "design_protocol_sha256": DESIGN_PROTOCOL_SHA256,
        "engine_sha256": ENGINE_SHA256,
        "validation_protocol_sha256": VALID_PROTOCOL_SHA256,
        "resident_pk_directory_sha256": RESIDENT_SHA256,
        "segment_reader_sha256": READER_SHA256,
    }

    if observed != expected:
        raise ValidationHarnessError(
            "frozen validation target identity mismatch"
        )


def source_identities() -> dict[str, dict[str, Any]]:
    result = {}

    for name in SOURCE_FILE_EXPECTATIONS:
        path = SOURCE_RUNTIME / name

        if not path.is_file():
            raise ValidationHarnessError(
                f"source fixture missing: {name}"
            )

        result[name] = file_identity(path)

    return result


def assert_source_exact(observed: dict[str, dict[str, Any]]) -> None:
    if observed != SOURCE_FILE_EXPECTATIONS:
        raise ValidationHarnessError(
            "source fixture identity mismatch"
        )


def collect_segment_ids(value: Any) -> set[str]:
    result = set()

    if isinstance(value, dict):
        for key, child in value.items():
            if key == "segment_id" and isinstance(child, str) and child:
                result.add(child)

            result.update(
                collect_segment_ids(child)
            )

    elif isinstance(value, list):
        for child in value:
            result.update(
                collect_segment_ids(child)
            )

    return result


def prepare_runtime() -> dict[str, Path]:
    if RESULT_PATH.exists():
        raise ValidationHarnessError(
            "validation result already exists"
        )

    if VALIDATION_RUNTIME.exists():
        raise ValidationHarnessError(
            "validation runtime already exists"
        )

    VALIDATION_RUNTIME.mkdir(
        parents=True,
        exist_ok=False,
    )

    copied = {}

    for name in SOURCE_FILE_EXPECTATIONS:
        src = SOURCE_RUNTIME / name
        dst = VALIDATION_RUNTIME / name

        shutil.copyfile(src, dst)
        copied[name] = dst

    copied_ids = {
        name: file_identity(path)
        for name, path in copied.items()
    }

    if copied_ids != SOURCE_FILE_EXPECTATIONS:
        raise ValidationHarnessError(
            "isolated fixture identity mismatch"
        )

    return copied


def build_fixture_entries(
    copied: dict[str, Path],
) -> tuple[str, str, tuple[ResidentPKEntry, ...]]:
    active = json.loads(
        copied["active_generation.json"].read_text(
            encoding="utf-8"
        )
    )

    manifest = json.loads(
        copied["candidate_a.manifest.json"].read_text(
            encoding="utf-8"
        )
    )

    segment_ids = sorted(
        collect_segment_ids(manifest)
    )

    if len(segment_ids) != 1:
        raise ValidationHarnessError(
            "fixture must expose exactly one segment_id"
        )

    segment_path = copied[
        "segment_00000000.mafseg"
    ]

    snapshot = build_snapshot(
        model_pk=active["model_pk"],
        active_record_path=copied[
            "active_generation.json"
        ],
        active_candidate_manifest_path=copied[
            "candidate_a.manifest.json"
        ],
        active_segment_paths={
            segment_ids[0]: segment_path,
        },
    )

    entries = tuple(
        sorted(
            (
                replace(
                    entry,
                    segment_path=str(segment_path),
                )
                for entry in snapshot.entries.values()
                if entry.length > 0
            ),
            key=lambda entry: (
                entry.length,
                entry.object_pk,
            ),
        )
    )

    if len(entries) < 4:
        raise ValidationHarnessError(
            "fixture requires at least four positive-length entries"
        )

    return (
        snapshot.model_pk,
        snapshot.generation_pk,
        entries,
    )


def normal_dense_materializer(
    entry: ResidentPKEntry,
    serialized: bytes,
) -> tuple[Any, int]:
    digest = hashlib.sha256(serialized).hexdigest()

    view = (
        "dense-validation-view",
        entry.model_pk,
        entry.generation_pk,
        entry.object_pk,
        digest,
        len(serialized),
    )

    return (
        view,
        len(serialized) + 17,
    )


def failing_dense_materializer(
    entry: ResidentPKEntry,
    serialized: bytes,
) -> tuple[Any, int]:
    del entry
    del serialized

    raise ExpectedDenseFailure(
        "deterministic dense validation failure"
    )


def dense_charge(entry: ResidentPKEntry) -> int:
    return entry.length + 17


def serialized_budget(entries: tuple[ResidentPKEntry, ...]) -> int:
    return (
        sum(entry.length for entry in entries) * 8
        + 4096
    )


def dense_budget(entries: tuple[ResidentPKEntry, ...]) -> int:
    return (
        sum(dense_charge(entry) for entry in entries) * 8
        + 4096
    )


def new_runtime(
    model_pk: str,
    generation_pk: str,
    entries: tuple[ResidentPKEntry, ...],
    *,
    serialized_limit: int | None = None,
    dense_limit: int | None = None,
    materializer: Callable[
        [ResidentPKEntry, bytes],
        tuple[Any, int],
    ] | None = normal_dense_materializer,
) -> MAFObjectRuntime:
    return MAFObjectRuntime(
        model_pk=model_pk,
        generation_pk=generation_pk,
        serialized_byte_budget=(
            serialized_budget(entries)
            if serialized_limit is None
            else serialized_limit
        ),
        dense_byte_budget=(
            dense_budget(entries)
            if dense_limit is None
            else dense_limit
        ),
        dense_materializer=materializer,
    )


def expect_error(
    exc_type: type[BaseException],
    func: Callable[[], Any],
) -> BaseException:
    try:
        func()

    except exc_type as exc:
        return exc

    except Exception as exc:
        raise AssertionError(
            f"expected {exc_type.__name__}; "
            f"observed {type(exc).__name__}"
        ) from exc

    raise AssertionError(
        f"expected {exc_type.__name__}"
    )


def object_snapshot(
    runtime: MAFObjectRuntime,
    object_pk: str,
) -> Any:
    matches = [
        item
        for item in runtime.snapshot().objects
        if item.object_pk == object_pk
    ]

    if len(matches) != 1:
        raise AssertionError(
            "expected one object snapshot"
        )

    return matches[0]


def atomic_view(
    runtime: MAFObjectRuntime,
    object_pk: str,
) -> tuple[Any, ...]:
    snap = runtime.snapshot()
    obj = object_snapshot(runtime, object_pk)

    return (
        snap.model_pk,
        snap.generation_pk,
        obj.state,
        obj.pin_count,
        obj.effective_pin_floor,
        snap.active_pin_leases,
        snap.serialized_resident_bytes,
        snap.dense_resident_bytes,
        obj.serialized_resident_bytes,
        obj.dense_resident_bytes,
    )


def assert_accounting_snapshot(snap: Any) -> None:
    if (
        snap.cold_disk_count
        + snap.mapped_count
        + snap.hot_maf_count
        + snap.hot_dense_count
        != snap.object_count
    ):
        raise AssertionError(
            "state counts do not sum to object_count"
        )

    if (
        sum(
            item.serialized_resident_bytes
            for item in snap.objects
        )
        != snap.serialized_resident_bytes
    ):
        raise AssertionError(
            "serialized accounting mismatch"
        )

    if (
        sum(
            item.dense_resident_bytes
            for item in snap.objects
        )
        != snap.dense_resident_bytes
    ):
        raise AssertionError(
            "dense accounting mismatch"
        )

    if (
        sum(
            item.pin_count
            for item in snap.objects
        )
        != snap.active_pin_leases
    ):
        raise AssertionError(
            "pin accounting mismatch"
        )

    for name, value in snap.counters:
        if (
            type(name) is not str
            or type(value) is not int
            or value < 0
        ):
            raise AssertionError(
                "counter invariant violated"
            )


def corrupt_entry_copy(
    entry: ResidentPKEntry,
    clean_segment: Path,
) -> tuple[ResidentPKEntry, Path]:
    corrupt = (
        VALIDATION_RUNTIME
        / "corrupt_segment.mafseg"
    )

    if corrupt.exists():
        raise ValidationHarnessError(
            "corruption fixture already exists"
        )

    shutil.copyfile(
        clean_segment,
        corrupt,
    )

    original_size = corrupt.stat().st_size

    data = bytearray(
        corrupt.read_bytes()
    )

    if not (
        0 <= entry.offset < len(data)
    ):
        raise ValidationHarnessError(
            "corruption offset outside segment"
        )

    data[entry.offset] ^= 0x01

    corrupt.write_bytes(bytes(data))

    if corrupt.stat().st_size != original_size:
        raise ValidationHarnessError(
            "corruption changed segment length"
        )

    if sha256_file(corrupt) == sha256_file(clean_segment):
        raise ValidationHarnessError(
            "corruption did not alter segment"
        )

    return (
        replace(
            entry,
            segment_path=str(corrupt),
        ),
        corrupt,
    )


class Context:
    def __init__(
        self,
        *,
        model_pk: str,
        generation_pk: str,
        entries: tuple[ResidentPKEntry, ...],
        clean_segment: Path,
        source_before: dict[str, dict[str, Any]],
    ) -> None:
        self.model_pk = model_pk
        self.generation_pk = generation_pk
        self.entries = entries
        self.clean_segment = clean_segment
        self.source_before = source_before
        self.evidence = {}


def v01(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
    )

    assert runtime.register_entry(
        entry
    ).state is ResidencyState.COLD_DISK

    count_before = runtime.snapshot().object_count

    expect_error(
        MAFObjectRuntimeStaleGenerationError,
        lambda: runtime.register_entry(
            replace(
                ctx.entries[1],
                model_pk=ctx.model_pk + "_other",
            )
        ),
    )

    expect_error(
        MAFObjectRuntimeStaleGenerationError,
        lambda: runtime.register_entry(
            replace(
                ctx.entries[2],
                generation_pk=ctx.generation_pk + "_other",
            )
        ),
    )

    assert runtime.snapshot().object_count == count_before

    runtime.close()

    return {"mismatch_rejections": 2}


def v02(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
    )

    snap = runtime.register_entry(entry)

    assert snap.state is ResidencyState.COLD_DISK
    assert snap.serialized_resident_bytes == 0
    assert snap.dense_resident_bytes == 0
    assert snap.pin_count == 0

    runtime.close()

    return {"state": snap.state.value}


def v03(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
    )

    runtime.register_entry(entry)

    observed = []

    for target in (
        ResidencyState.MAPPED,
        ResidencyState.HOT_MAF,
        ResidencyState.HOT_DENSE,
    ):
        assert runtime.transition(
            entry.object_pk,
            target,
        ).state is target

        observed.append(target.value)

    runtime.close()

    return {"states": observed}


def v04(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
    )

    runtime.register_entry(entry)

    runtime.ensure_state(
        entry.object_pk,
        ResidencyState.HOT_DENSE,
    )

    observed = []

    for target in (
        ResidencyState.HOT_MAF,
        ResidencyState.MAPPED,
        ResidencyState.COLD_DISK,
    ):
        assert runtime.transition(
            entry.object_pk,
            target,
        ).state is target

        observed.append(target.value)

    snap = runtime.snapshot()

    assert snap.serialized_resident_bytes == 0
    assert snap.dense_resident_bytes == 0

    runtime.close()

    return {"states": observed}


def v05(ctx: Context) -> dict[str, Any]:
    cases = (
        (
            ResidencyState.COLD_DISK,
            ResidencyState.HOT_MAF,
        ),
        (
            ResidencyState.COLD_DISK,
            ResidencyState.HOT_DENSE,
        ),
        (
            ResidencyState.MAPPED,
            ResidencyState.HOT_DENSE,
        ),
        (
            ResidencyState.HOT_DENSE,
            ResidencyState.MAPPED,
        ),
        (
            ResidencyState.HOT_DENSE,
            ResidencyState.COLD_DISK,
        ),
    )

    for index, (start, target) in enumerate(cases):
        entry = ctx.entries[
            index % len(ctx.entries)
        ]

        runtime = new_runtime(
            ctx.model_pk,
            ctx.generation_pk,
            ctx.entries,
        )

        runtime.register_entry(entry)

        runtime.ensure_state(
            entry.object_pk,
            start,
        )

        before = atomic_view(
            runtime,
            entry.object_pk,
        )

        expect_error(
            MAFObjectRuntimeIllegalTransitionError,
            lambda: runtime.transition(
                entry.object_pk,
                target,
            ),
        )

        after = atomic_view(
            runtime,
            entry.object_pk,
        )

        assert before == after

        runtime.close()

    return {"rejected": len(cases)}


def v06(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
    )

    runtime.register_entry(entry)

    runtime.ensure_state(
        entry.object_pk,
        ResidencyState.HOT_MAF,
    )

    before = atomic_view(
        runtime,
        entry.object_pk,
    )

    runtime.transition(
        entry.object_pk,
        ResidencyState.HOT_MAF,
    )

    after = atomic_view(
        runtime,
        entry.object_pk,
    )

    assert before == after

    runtime.close()

    return {"state": "HOT_MAF"}


def v07(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
    )

    runtime.register_entry(entry)

    runtime.transition(
        entry.object_pk,
        ResidencyState.MAPPED,
    )

    runtime.transition(
        entry.object_pk,
        ResidencyState.HOT_MAF,
    )

    serialized = runtime.serialized_bytes(
        entry.object_pk
    )

    observed_sha = hashlib.sha256(
        serialized
    ).hexdigest()

    assert len(serialized) == entry.length
    assert observed_sha == entry.object_file_sha256

    runtime.close()

    return {
        "length": len(serialized),
        "sha256": observed_sha,
    }


def v08(ctx: Context) -> dict[str, Any]:
    corrupt_entry, corrupt_path = (
        corrupt_entry_copy(
            ctx.entries[0],
            ctx.clean_segment,
        )
    )

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        (corrupt_entry,),
    )

    runtime.register_entry(corrupt_entry)

    runtime.transition(
        corrupt_entry.object_pk,
        ResidencyState.MAPPED,
    )

    before = atomic_view(
        runtime,
        corrupt_entry.object_pk,
    )

    expect_error(
        MAFObjectRuntimeVerifiedReadError,
        lambda: runtime.transition(
            corrupt_entry.object_pk,
            ResidencyState.HOT_MAF,
        ),
    )

    after = atomic_view(
        runtime,
        corrupt_entry.object_pk,
    )

    assert before == after

    expect_error(
        MAFObjectRuntimeResidencyUnavailableError,
        lambda: runtime.serialized_bytes(
            corrupt_entry.object_pk
        ),
    )

    runtime.close()

    ctx.evidence[
        "corruption_failure_nonpublication"
    ] = True

    return {
        "corrupt_sha256": sha256_file(corrupt_path),
    }


def v09(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
    )

    runtime.register_entry(entry)

    runtime.transition(
        entry.object_pk,
        ResidencyState.MAPPED,
    )

    original = runtime_mod.read_serialized_object

    def injected_short_read(
        entry_arg: ResidentPKEntry,
        generation_arg: str,
    ) -> bytes:
        del entry_arg
        del generation_arg

        raise MAFSegmentReaderShortReadError(
            "validation injected short read"
        )

    before = atomic_view(
        runtime,
        entry.object_pk,
    )

    try:
        runtime_mod.read_serialized_object = injected_short_read

        expect_error(
            MAFObjectRuntimeVerifiedReadError,
            lambda: runtime.transition(
                entry.object_pk,
                ResidencyState.HOT_MAF,
            ),
        )

    finally:
        runtime_mod.read_serialized_object = original

    assert runtime_mod.read_serialized_object is original

    after = atomic_view(
        runtime,
        entry.object_pk,
    )

    assert before == after

    expect_error(
        MAFObjectRuntimeResidencyUnavailableError,
        lambda: runtime.serialized_bytes(
            entry.object_pk
        ),
    )

    runtime.close()

    ctx.evidence[
        "short_read_failure_nonpublication"
    ] = True

    return {"callable_restored": True}


def v10(ctx: Context) -> dict[str, Any]:
    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
    )

    expect_error(
        MAFObjectRuntimeStaleGenerationError,
        lambda: runtime.register_entry(
            replace(
                ctx.entries[0],
                generation_pk=ctx.generation_pk + "_stale",
            )
        ),
    )

    assert runtime.snapshot().object_count == 0

    runtime.close()

    return {"rejected": True}


def v11(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
    )

    runtime.register_entry(entry)

    runtime.ensure_state(
        entry.object_pk,
        ResidencyState.HOT_MAF,
    )

    serialized = runtime.serialized_bytes(
        entry.object_pk
    )

    assert (
        runtime.snapshot().serialized_resident_bytes
        == len(serialized)
        == entry.length
    )

    runtime.transition(
        entry.object_pk,
        ResidencyState.MAPPED,
    )

    assert (
        runtime.snapshot().serialized_resident_bytes
        == 0
    )

    runtime.close()

    return {"charge": entry.length}


def v12(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
    )

    runtime.register_entry(entry)

    runtime.ensure_state(
        entry.object_pk,
        ResidencyState.HOT_DENSE,
    )

    assert (
        runtime.snapshot().dense_resident_bytes
        == dense_charge(entry)
    )

    runtime.transition(
        entry.object_pk,
        ResidencyState.HOT_MAF,
    )

    assert runtime.snapshot().dense_resident_bytes == 0

    runtime.close()

    return {"charge": dense_charge(entry)}


def v13(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]

    zero_serialized = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
        serialized_limit=0,
    )

    zero_serialized.register_entry(entry)

    zero_serialized.transition(
        entry.object_pk,
        ResidencyState.MAPPED,
    )

    expect_error(
        MAFObjectRuntimeSerializedBudgetExceededError,
        lambda: zero_serialized.transition(
            entry.object_pk,
            ResidencyState.HOT_MAF,
        ),
    )

    assert (
        zero_serialized.state(entry.object_pk)
        is ResidencyState.MAPPED
    )
    assert (
        zero_serialized.snapshot().serialized_resident_bytes
        == 0
    )

    zero_serialized.close()

    zero_dense = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
        dense_limit=0,
    )

    zero_dense.register_entry(entry)

    zero_dense.ensure_state(
        entry.object_pk,
        ResidencyState.HOT_MAF,
    )

    expect_error(
        MAFObjectRuntimeDenseBudgetExceededError,
        lambda: zero_dense.transition(
            entry.object_pk,
            ResidencyState.HOT_DENSE,
        ),
    )

    assert (
        zero_dense.state(entry.object_pk)
        is ResidencyState.HOT_MAF
    )
    assert zero_dense.snapshot().dense_resident_bytes == 0

    zero_dense.close()

    ctx.evidence[
        "budget_failure_nonpublication"
    ] = True

    return {
        "serialized_zero_rejected": True,
        "dense_zero_rejected": True,
    }


def v14(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
        serialized_limit=max(
            0,
            entry.length - 1,
        ),
    )

    runtime.register_entry(entry)

    runtime.transition(
        entry.object_pk,
        ResidencyState.MAPPED,
    )

    before = atomic_view(
        runtime,
        entry.object_pk,
    )

    expect_error(
        MAFObjectRuntimeSerializedBudgetExceededError,
        lambda: runtime.transition(
            entry.object_pk,
            ResidencyState.HOT_MAF,
        ),
    )

    after = atomic_view(
        runtime,
        entry.object_pk,
    )

    # Counters may legitimately record the rejection.
    # Committed state/accounting/pins/identity must remain unchanged.
    assert before == after

    runtime.close()

    runtime2 = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
        dense_limit=max(
            0,
            dense_charge(entry) - 1,
        ),
    )

    runtime2.register_entry(entry)

    runtime2.ensure_state(
        entry.object_pk,
        ResidencyState.HOT_MAF,
    )

    before2 = atomic_view(
        runtime2,
        entry.object_pk,
    )

    expect_error(
        MAFObjectRuntimeDenseBudgetExceededError,
        lambda: runtime2.transition(
            entry.object_pk,
            ResidencyState.HOT_DENSE,
        ),
    )

    after2 = atomic_view(
        runtime2,
        entry.object_pk,
    )

    assert before2 == after2

    runtime2.close()

    return {"failure_atomic": True}


def v15(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
    )

    runtime.register_entry(entry)

    mapped = runtime.pin(
        entry.object_pk,
        ResidencyState.MAPPED,
    )

    hot = runtime.pin(
        entry.object_pk,
        ResidencyState.HOT_MAF,
    )

    snap = object_snapshot(
        runtime,
        entry.object_pk,
    )

    assert snap.pin_count == 2
    assert snap.effective_pin_floor is ResidencyState.HOT_MAF

    runtime.unpin(hot.token)

    snap = object_snapshot(
        runtime,
        entry.object_pk,
    )

    assert snap.pin_count == 1
    assert snap.effective_pin_floor is ResidencyState.MAPPED

    runtime.unpin(mapped.token)
    runtime.close()

    return {"composition": True}


def v16(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
    )

    runtime.register_entry(entry)

    hot = runtime.pin(
        entry.object_pk,
        ResidencyState.HOT_MAF,
    )

    expect_error(
        MAFObjectRuntimePinnedDemotionError,
        lambda: runtime.transition(
            entry.object_pk,
            ResidencyState.MAPPED,
        ),
    )

    assert object_snapshot(
        runtime,
        entry.object_pk,
    ).pin_count == 1

    runtime.unpin(hot.token)

    mapped = runtime.pin(
        entry.object_pk,
        ResidencyState.MAPPED,
    )

    runtime.ensure_state(
        entry.object_pk,
        ResidencyState.MAPPED,
    )

    expect_error(
        MAFObjectRuntimePinnedDemotionError,
        lambda: runtime.transition(
            entry.object_pk,
            ResidencyState.COLD_DISK,
        ),
    )

    assert object_snapshot(
        runtime,
        entry.object_pk,
    ).pin_count == 1

    runtime.unpin(mapped.token)
    runtime.close()

    return {"blocked": 2}


def v17(ctx: Context) -> dict[str, Any]:
    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
    )

    expect_error(
        MAFObjectRuntimePinTokenError,
        lambda: runtime.unpin(999999999),
    )

    runtime.close()

    return {"rejected": True}


def v18(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
    )

    runtime.register_entry(entry)

    lease = runtime.pin(
        entry.object_pk,
        ResidencyState.MAPPED,
    )

    runtime.unpin(lease.token)

    expect_error(
        MAFObjectRuntimePinTokenError,
        lambda: runtime.unpin(lease.token),
    )

    runtime.close()

    return {"token": lease.token}


def v19(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
    )

    runtime.register_entry(entry)

    lease = runtime.pin(
        entry.object_pk,
        ResidencyState.HOT_MAF,
    )

    before = runtime.state(
        entry.object_pk
    )

    runtime.unpin(lease.token)

    after = runtime.state(
        entry.object_pk
    )

    assert before is after

    runtime.close()

    return {"state": before.value}


def v20(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]
    clean_before = sha256_file(ctx.clean_segment)

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
    )

    runtime.register_entry(entry)

    runtime.ensure_state(
        entry.object_pk,
        ResidencyState.HOT_DENSE,
    )

    serialized = runtime.serialized_bytes(
        entry.object_pk
    )

    expected_view = (
        "dense-validation-view",
        entry.model_pk,
        entry.generation_pk,
        entry.object_pk,
        hashlib.sha256(serialized).hexdigest(),
        len(serialized),
    )

    assert runtime.dense_view(entry.object_pk) == expected_view

    assert (
        runtime.snapshot().dense_resident_bytes
        == dense_charge(entry)
    )

    runtime.close()

    assert sha256_file(ctx.clean_segment) == clean_before

    return {
        "dense_charge": dense_charge(entry),
    }


def v21(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
        materializer=failing_dense_materializer,
    )

    runtime.register_entry(entry)

    runtime.ensure_state(
        entry.object_pk,
        ResidencyState.HOT_MAF,
    )

    before = atomic_view(
        runtime,
        entry.object_pk,
    )

    serialized = runtime.serialized_bytes(
        entry.object_pk
    )

    expect_error(
        MAFObjectRuntimeDenseMaterializationError,
        lambda: runtime.transition(
            entry.object_pk,
            ResidencyState.HOT_DENSE,
        ),
    )

    after = atomic_view(
        runtime,
        entry.object_pk,
    )

    assert before == after
    assert (
        runtime.serialized_bytes(entry.object_pk)
        == serialized
    )

    runtime.close()

    return {"failure_atomic": True}


def v22(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
    )

    runtime.register_entry(entry)

    runtime.ensure_state(
        entry.object_pk,
        ResidencyState.HOT_DENSE,
    )

    assert runtime.dense_view(entry.object_pk) is not None

    runtime.transition(
        entry.object_pk,
        ResidencyState.HOT_MAF,
    )

    expect_error(
        MAFObjectRuntimeResidencyUnavailableError,
        lambda: runtime.dense_view(
            entry.object_pk
        ),
    )

    runtime.close()

    return {"invalidated": True}


def v23(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
    )

    runtime.register_entry(entry)

    runtime.ensure_state(
        entry.object_pk,
        ResidencyState.HOT_DENSE,
    )

    runtime.pin(
        entry.object_pk,
        ResidencyState.HOT_DENSE,
    )

    runtime.close()

    snap = runtime.snapshot()

    assert snap.closed is True
    assert snap.active_pin_leases == 0
    assert snap.serialized_resident_bytes == 0
    assert snap.dense_resident_bytes == 0
    assert (
        object_snapshot(runtime, entry.object_pk).state
        is ResidencyState.COLD_DISK
    )

    return {"closed": True}


def v24(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
    )

    runtime.register_entry(entry)

    runtime.ensure_state(
        entry.object_pk,
        ResidencyState.HOT_DENSE,
    )

    runtime.close()
    first = runtime.snapshot()

    runtime.close()
    second = runtime.snapshot()

    assert first == second

    return {"idempotent": True}


def v25(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
    )

    runtime.register_entry(entry)

    runtime.ensure_state(
        entry.object_pk,
        ResidencyState.HOT_DENSE,
    )

    runtime.close()

    expect_error(
        MAFObjectRuntimeClosedError,
        lambda: runtime.register_entry(
            ctx.entries[1]
        ),
    )

    expect_error(
        MAFObjectRuntimeClosedError,
        lambda: runtime.transition(
            entry.object_pk,
            ResidencyState.MAPPED,
        ),
    )

    expect_error(
        MAFObjectRuntimeClosedError,
        lambda: runtime.pin(
            entry.object_pk,
            ResidencyState.MAPPED,
        ),
    )

    expect_error(
        MAFObjectRuntimeClosedError,
        lambda: runtime.serialized_bytes(
            entry.object_pk
        ),
    )

    expect_error(
        MAFObjectRuntimeClosedError,
        lambda: runtime.dense_view(
            entry.object_pk
        ),
    )

    assert runtime.snapshot().closed is True

    return {"rejected": 5}


def v26(ctx: Context) -> dict[str, Any]:
    assert source_identities() == ctx.source_before

    return {"source_unchanged": True}


def v27(ctx: Context) -> dict[str, Any]:
    names = (
        "corruption_failure_nonpublication",
        "short_read_failure_nonpublication",
        "budget_failure_nonpublication",
    )

    for name in names:
        assert ctx.evidence.get(name) is True

    return {
        name: True
        for name in names
    }


def v28(ctx: Context) -> dict[str, Any]:
    entries = ctx.entries[:4]

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        entries,
    )

    for entry in entries:
        runtime.register_entry(entry)

    runtime.ensure_state(
        entries[1].object_pk,
        ResidencyState.MAPPED,
    )

    runtime.ensure_state(
        entries[2].object_pk,
        ResidencyState.HOT_MAF,
    )

    runtime.ensure_state(
        entries[3].object_pk,
        ResidencyState.HOT_DENSE,
    )

    lease = runtime.pin(
        entries[2].object_pk,
        ResidencyState.MAPPED,
    )

    snap = runtime.snapshot()

    assert snap.object_count == 4
    assert snap.cold_disk_count == 1
    assert snap.mapped_count == 1
    assert snap.hot_maf_count == 1
    assert snap.hot_dense_count == 1
    assert snap.active_pin_leases == 1

    assert_accounting_snapshot(snap)

    runtime.unpin(lease.token)
    runtime.close()

    return {
        "counts": [1, 1, 1, 1],
    }


def run_threads(
    workers: list[Callable[[], None]],
) -> list[str]:
    barrier = threading.Barrier(
        len(workers)
    )

    errors = []
    errors_lock = threading.Lock()

    def wrapped(
        worker: Callable[[], None],
    ) -> None:
        try:
            barrier.wait(
                timeout=JOIN_TIMEOUT_SECONDS
            )
            worker()

        except Exception as exc:
            with errors_lock:
                errors.append(
                    f"{type(exc).__name__}: {exc}"
                )

    threads = [
        threading.Thread(
            target=wrapped,
            args=(worker,),
        )
        for worker in workers
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join(
            timeout=JOIN_TIMEOUT_SECONDS
        )

    if any(
        thread.is_alive()
        for thread in threads
    ):
        raise AssertionError(
            "worker join timeout"
        )

    return errors


def v29(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
    )

    runtime.register_entry(entry)

    runtime.transition(
        entry.object_pk,
        ResidencyState.MAPPED,
    )

    original = runtime_mod.read_serialized_object
    count = 0
    count_lock = threading.Lock()

    def counting_reader(
        entry_arg: ResidentPKEntry,
        generation_arg: str,
    ) -> bytes:
        nonlocal count

        with count_lock:
            count += 1

        return original(
            entry_arg,
            generation_arg,
        )

    try:
        runtime_mod.read_serialized_object = counting_reader

        errors = run_threads(
            [
                lambda: runtime.transition(
                    entry.object_pk,
                    ResidencyState.HOT_MAF,
                ),
                lambda: runtime.transition(
                    entry.object_pk,
                    ResidencyState.HOT_MAF,
                ),
            ]
        )

    finally:
        runtime_mod.read_serialized_object = original

    assert runtime_mod.read_serialized_object is original
    assert errors == []
    assert count == 1
    assert (
        runtime.state(entry.object_pk)
        is ResidencyState.HOT_MAF
    )
    assert (
        runtime.snapshot().serialized_resident_bytes
        == entry.length
    )

    runtime.close()

    return {
        "reader_calls": count,
        "errors": errors,
    }


def v30(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
    )

    runtime.register_entry(entry)

    runtime.ensure_state(
        entry.object_pk,
        ResidencyState.HOT_MAF,
    )

    leases = []
    lease_lock = threading.Lock()

    def acquire() -> None:
        lease = runtime.pin(
            entry.object_pk,
            ResidencyState.MAPPED,
        )

        with lease_lock:
            leases.append(lease)

    errors = run_threads(
        [
            acquire
            for _ in range(PIN_THREAD_COUNT)
        ]
    )

    assert errors == []

    tokens = [
        lease.token
        for lease in leases
    ]

    assert len(tokens) == PIN_THREAD_COUNT
    assert len(set(tokens)) == PIN_THREAD_COUNT
    assert (
        runtime.snapshot().active_pin_leases
        == PIN_THREAD_COUNT
    )

    errors = run_threads(
        [
            (
                lambda token=token:
                    runtime.unpin(token)
            )
            for token in tokens
        ]
    )

    assert errors == []
    assert runtime.snapshot().active_pin_leases == 0

    assert_accounting_snapshot(
        runtime.snapshot()
    )

    runtime.close()

    return {
        "threads": PIN_THREAD_COUNT,
        "unique_tokens": len(set(tokens)),
    }


def v31(ctx: Context) -> dict[str, Any]:
    entry = ctx.entries[0]

    runtime = new_runtime(
        ctx.model_pk,
        ctx.generation_pk,
        ctx.entries,
    )

    runtime.register_entry(entry)

    runtime.transition(
        entry.object_pk,
        ResidencyState.MAPPED,
    )

    pre = runtime.snapshot()
    assert_accounting_snapshot(pre)

    original = runtime_mod.read_serialized_object

    reader_entered = threading.Event()
    release_reader = threading.Event()

    worker_errors = []
    observed = []

    def blocking_reader(
        entry_arg: ResidentPKEntry,
        generation_arg: str,
    ) -> bytes:
        reader_entered.set()

        if not release_reader.wait(
            timeout=JOIN_TIMEOUT_SECONDS
        ):
            raise RuntimeError(
                "reader release timeout"
            )

        return original(
            entry_arg,
            generation_arg,
        )

    def promote() -> None:
        try:
            runtime.transition(
                entry.object_pk,
                ResidencyState.HOT_MAF,
            )

        except Exception as exc:
            worker_errors.append(
                f"{type(exc).__name__}: {exc}"
            )

    def observe() -> None:
        try:
            observed.append(
                runtime.snapshot()
            )
            observed.append(
                runtime.state(
                    entry.object_pk
                )
            )

        except Exception as exc:
            worker_errors.append(
                f"{type(exc).__name__}: {exc}"
            )

    try:
        runtime_mod.read_serialized_object = blocking_reader

        mutation = threading.Thread(
            target=promote
        )
        mutation.start()

        if not reader_entered.wait(
            timeout=JOIN_TIMEOUT_SECONDS
        ):
            raise AssertionError(
                "mutation did not reach reader"
            )

        observer = threading.Thread(
            target=observe
        )
        observer.start()

        release_reader.set()

        mutation.join(
            timeout=JOIN_TIMEOUT_SECONDS
        )
        observer.join(
            timeout=JOIN_TIMEOUT_SECONDS
        )

        if mutation.is_alive() or observer.is_alive():
            raise AssertionError(
                "observation join timeout"
            )

    finally:
        release_reader.set()
        runtime_mod.read_serialized_object = original

    assert runtime_mod.read_serialized_object is original
    assert worker_errors == []

    # Before transition, public state is fully committed MAPPED.
    assert pre.mapped_count == 1
    assert pre.serialized_resident_bytes == 0

    # Because public API access is protected by the same runtime lock,
    # concurrent observers may see only complete committed states.
    for item in observed:
        if isinstance(item, ResidencyState):
            assert item in (
                ResidencyState.MAPPED,
                ResidencyState.HOT_MAF,
            )

        else:
            assert_accounting_snapshot(item)

            if item.mapped_count == 1:
                assert item.serialized_resident_bytes == 0

            if item.hot_maf_count == 1:
                assert (
                    item.serialized_resident_bytes
                    == entry.length
                )

    assert (
        runtime.state(entry.object_pk)
        is ResidencyState.HOT_MAF
    )

    post = runtime.snapshot()
    assert_accounting_snapshot(post)

    assert post.hot_maf_count == 1
    assert (
        post.serialized_resident_bytes
        == entry.length
    )

    runtime.close()

    return {
        "observations": len(observed),
        "worker_errors": worker_errors,
    }


def v32(ctx: Context) -> dict[str, Any]:
    original = runtime_mod.read_serialized_object
    calls = []

    for repetition in range(
        PROMOTION_RACE_REPETITIONS
    ):
        entry = ctx.entries[
            repetition % len(ctx.entries)
        ]

        runtime = new_runtime(
            ctx.model_pk,
            ctx.generation_pk,
            ctx.entries,
        )

        runtime.register_entry(entry)

        runtime.transition(
            entry.object_pk,
            ResidencyState.MAPPED,
        )

        count = 0
        count_lock = threading.Lock()

        def counting_reader(
            entry_arg: ResidentPKEntry,
            generation_arg: str,
        ) -> bytes:
            nonlocal count

            with count_lock:
                count += 1

            return original(
                entry_arg,
                generation_arg,
            )

        try:
            runtime_mod.read_serialized_object = counting_reader

            errors = run_threads(
                [
                    lambda: runtime.transition(
                        entry.object_pk,
                        ResidencyState.HOT_MAF,
                    ),
                    lambda: runtime.transition(
                        entry.object_pk,
                        ResidencyState.HOT_MAF,
                    ),
                ]
            )

        finally:
            runtime_mod.read_serialized_object = original

        assert errors == []
        assert count == 1
        assert (
            runtime.state(entry.object_pk)
            is ResidencyState.HOT_MAF
        )
        assert (
            runtime.snapshot().serialized_resident_bytes
            == entry.length
        )

        runtime.transition(
            entry.object_pk,
            ResidencyState.MAPPED,
        )

        assert (
            runtime.snapshot().serialized_resident_bytes
            == 0
        )

        calls.append(count)

        runtime.close()

    assert runtime_mod.read_serialized_object is original

    return {
        "repetitions": PROMOTION_RACE_REPETITIONS,
        "reader_calls": calls,
    }


CHECK_FUNCTIONS = {
    "V01_runtime_binding": v01,
    "V02_initial_cold_disk": v02,
    "V03_legal_upward_primitive_transitions": v03,
    "V04_legal_downward_primitive_transitions": v04,
    "V05_illegal_skipped_transitions": v05,
    "V06_same_state_idempotence": v06,
    "V07_verified_hot_maf_promotion": v07,
    "V08_corruption_hash_failure_nonpublication": v08,
    "V09_short_read_nonpublication": v09,
    "V10_stale_generation_rejection": v10,
    "V11_serialized_byte_accounting": v11,
    "V12_dense_byte_accounting": v12,
    "V13_zero_budget_rejection": v13,
    "V14_over_budget_failure_atomicity": v14,
    "V15_multiple_pin_floor_composition": v15,
    "V16_pinned_demotion_rejected": v16,
    "V17_unknown_pin_rejection": v17,
    "V18_consumed_pin_rejection": v18,
    "V19_unpin_no_automatic_demotion": v19,
    "V20_dense_materialization_success": v20,
    "V21_dense_materialization_failure_atomicity": v21,
    "V22_dense_view_lifetime_invalidation": v22,
    "V23_runtime_close_cleanup": v23,
    "V24_close_idempotence": v24,
    "V25_operation_rejection_after_close": v25,
    "V26_source_file_immutability": v26,
    "V27_no_unverified_byte_escape": v27,
    "V28_snapshot_accounting_consistency": v28,
    "V29_concurrent_same_object_promotion": v29,
    "V30_concurrent_pin_unpin_accounting": v30,
    "V31_concurrent_observation_no_provisional_state": v31,
    "V32_promotion_race_no_duplicate_ownership": v32,
}


def run_validation() -> dict[str, Any]:
    if tuple(CHECK_FUNCTIONS) != CHECK_NAMES:
        raise ValidationHarnessError(
            "V01-V32 function map/order mismatch"
        )

    frozen_before = frozen_identities()
    assert_frozen_exact(frozen_before)

    source_before = source_identities()
    assert_source_exact(source_before)

    copied = prepare_runtime()

    model_pk, generation_pk, entries = (
        build_fixture_entries(copied)
    )

    ctx = Context(
        model_pk=model_pk,
        generation_pk=generation_pk,
        entries=entries,
        clean_segment=copied[
            "segment_00000000.mafseg"
        ],
        source_before=source_before,
    )

    check_results = {}
    check_details = {}

    for name in CHECK_NAMES:
        try:
            details = CHECK_FUNCTIONS[name](ctx)

            check_results[name] = True

            check_details[name] = {
                "pass": True,
                "details": details,
            }

        except Exception as exc:
            check_results[name] = False

            check_details[name] = {
                "pass": False,
                "error_type": type(exc).__name__,
                "error": str(exc),
            }

    frozen_after = frozen_identities()
    source_after = source_identities()

    if frozen_after != frozen_before:
        raise ValidationHarnessError(
            "frozen validation target changed"
        )

    if source_after != source_before:
        raise ValidationHarnessError(
            "source fixture changed"
        )

    failed = [
        name
        for name, passed
        in check_results.items()
        if not passed
    ]

    return {
        "schema": SCHEMA,
        "validation_valid": True,
        "all_pass": not failed,
        "fatal_error": None,
        "phase_6c_validation": (
            "object_runtime_residency_v1"
        ),
        "phase_6c_started": True,
        "benchmark_executed": False,
        "backend_selected": None,
        "exact_once": True,
        "frozen_identities_before": frozen_before,
        "frozen_identities_after": frozen_after,
        "frozen_identities_unchanged": True,
        "source_fixture_before": source_before,
        "source_fixture_after": source_after,
        "source_fixture_unchanged": True,
        "fixture": {
            "model_pk": model_pk,
            "generation_pk": generation_pk,
            "entry_count": len(entries),
            "selected_entries": [
                {
                    "object_pk": entry.object_pk,
                    "offset": entry.offset,
                    "length": entry.length,
                    "segment_id": entry.segment_id,
                    "object_file_sha256":
                        entry.object_file_sha256,
                }
                for entry in entries[:4]
            ],
        },
        "concurrency": {
            "promotion_race_repetitions":
                PROMOTION_RACE_REPETITIONS,
            "pin_thread_count":
                PIN_THREAD_COUNT,
            "join_timeout_seconds":
                JOIN_TIMEOUT_SECONDS,
        },
        "checks": check_results,
        "check_details": check_details,
        "failed_checks": failed,
        "runtime_inventory":
            runtime_inventory(
                VALIDATION_RUNTIME
            ),
    }


def fatal_result(exc: BaseException) -> dict[str, Any]:
    try:
        frozen = frozen_identities()
    except Exception:
        frozen = {}

    try:
        source = source_identities()
    except Exception:
        source = {}

    return {
        "schema": SCHEMA,
        "validation_valid": False,
        "all_pass": False,
        "fatal_error": {
            "type": type(exc).__name__,
            "message": str(exc),
        },
        "phase_6c_validation":
            "object_runtime_residency_v1",
        "phase_6c_started": True,
        "benchmark_executed": False,
        "backend_selected": None,
        "exact_once": True,
        "frozen_identities": frozen,
        "source_fixture": source,
        "checks": {},
        "failed_checks": [],
        "runtime_inventory":
            runtime_inventory(
                VALIDATION_RUNTIME
            ),
    }


def publish_result(result: dict[str, Any]) -> None:
    if RESULT_PATH.exists():
        raise ValidationHarnessError(
            "refusing to overwrite existing validation result"
        )

    RESULT_PATH.write_text(
        json.dumps(
            result,
            sort_keys=True,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    if RESULT_PATH.exists():
        raise ValidationHarnessError(
            "validation result already exists; V1.1 rerun forbidden"
        )

    try:
        result = run_validation()

    except BaseException as exc:
        result = fatal_result(exc)

    publish_result(result)

    print(
        "OPENMIND / MAF OBJECT RUNTIME RESIDENCY VALIDATION V1.1"
    )
    print(
        "validation_valid:",
        result["validation_valid"],
    )
    print(
        "all_pass:",
        result["all_pass"],
    )
    print(
        "fatal_error:",
        result["fatal_error"],
    )
    print(
        "checks:",
        len(result.get("checks", {})),
    )
    print(
        "failed_checks:",
        result.get("failed_checks", []),
    )
    print(
        "result:",
        RESULT_PATH,
    )

    return (
        0
        if result["validation_valid"]
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(main())
