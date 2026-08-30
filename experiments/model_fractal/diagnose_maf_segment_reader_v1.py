#!/usr/bin/env python3
"""Exact-once post-validation diagnostics for MAF Segment Reader V1."""

from __future__ import annotations

import dataclasses
import gc
import hashlib
import json
import os
import statistics
import sys
import time
import tracemalloc
from pathlib import Path
from typing import Any, Callable

import maf_segment_reader_v1 as reader
import maf_segment_reader_validation_v1 as validation


SCHEMA = "openmind.maf_segment_reader_diagnostics.v1"
VERSION = "maf_segment_reader_diagnostics_v1"

PROTOCOL = Path(
    "experiments/model_fractal/"
    "MAF_SEGMENT_READER_DIAGNOSTICS_V1_PROTOCOL.md"
)
PROTOCOL_SHA256 = "817fb546c9e7e1b2cc2dfeea872198f5a01f3a5ef8643a8627ec7162f3e9b089"

SEGMENT_PROTOCOL = Path(
    "experiments/model_fractal/"
    "MAF_SEGMENT_READER_V1_PROTOCOL.md"
)
SEGMENT_PROTOCOL_SHA256 = "192402f1e4f2d41540d225cce7629757152b9996a9adffaafeab6674e13f0f5d"

ENGINE = Path(
    "experiments/model_fractal/"
    "maf_segment_reader_v1.py"
)
ENGINE_SHA256 = "3499cb8e528fe8e9315e3e5656d6aa888c95ca175310b6371e722de409827369"

VALIDATION_PROTOCOL = Path(
    "experiments/model_fractal/"
    "MAF_SEGMENT_READER_VALIDATION_V1_PROTOCOL.md"
)
VALIDATION_PROTOCOL_SHA256 = "c896e6b68be67352e4b09ed8f6486cdea2e20435fa03c7c44fd4871051e202be"

VALIDATION_RUNNER = Path(
    "experiments/model_fractal/"
    "maf_segment_reader_validation_v1.py"
)
VALIDATION_RUNNER_SHA256 = "1f5cfdba3d3bd681eb78b07d98b9ee49497a3608bc51408c7e503b0dbc80bf88"

VALIDATION_RESULT = Path(
    "experiments/model_fractal/"
    "maf_segment_reader_validation_v1.json"
)
VALIDATION_RESULT_SHA256 = "1ceef1ed2b814da3951811ea97e9f4475b3fa79557b341e7c8e089ec8a409328"

BENCHMARK_COMPLETION = Path(
    "experiments/model_fractal/"
    "MAF_SEGMENT_READER_BENCHMARK_V1_2_COMPLETION.md"
)
BENCHMARK_COMPLETION_SHA256 = "5d5e3c10d39b39e5527e778753828ecca4aead4f60d3b92a59db4eb892644907"

SOURCE_RUNTIME = Path(
    "results/runtime/"
    "maf_resident_pk_directory_benchmark_v1_1"
)
SOURCE_ACTIVE = SOURCE_RUNTIME / "active_generation.json"
SOURCE_CANDIDATE = SOURCE_RUNTIME / "candidate_a.manifest.json"
SOURCE_SEGMENT = SOURCE_RUNTIME / "segment_00000000.mafseg"

SOURCE_ACTIVE_SHA256 = "031d1a50a3cf53f158057a02bb6c68001edfb07bf48bf893afc9bc8f095458e9"
SOURCE_CANDIDATE_SHA256 = "941301aa362d3f949389e5364b1be4d7f26b96f0d45efa81346c82fce3260f93"
SOURCE_SEGMENT_SHA256 = "f965b526538d757ca2d6114af6517c57cbcb3650b71d8cfb92046a04ef2f566b"
SOURCE_SEGMENT_BYTES = 4096

RESULT = Path(
    "experiments/model_fractal/"
    "maf_segment_reader_diagnostics_v1.json"
)
RUNTIME = Path(
    "results/runtime/"
    "maf_segment_reader_diagnostics_v1"
)

SUCCESS_BATCH_WARMUPS = 2
SUCCESS_BATCHES = 20
SUCCESS_READS_PER_BATCH = 5000

FAILURE_BATCH_WARMUPS = 2
FAILURE_BATCHES = 20
FAILURES_PER_BATCH = 2000

SUCCESS_DEGRADATION_LIMIT = 2.0
FAILURE_DEGRADATION_LIMIT = 2.5

SUCCESS_FD_REPEATS = 5000
FAILURE_FD_REPEATS = 5000
FD_GROWTH_LIMIT = 2

SUCCESS_RETAIN_REPEATS = 100000
FAILURE_RETAIN_REPEATS = 50000
SUCCESS_RETAINED_LIMIT_BYTES = 1048576
FAILURE_RETAINED_LIMIT_BYTES = 1048576

LIVE_ERROR_GROWTH_LIMIT = 2
GC_OBJECT_GROWTH_LIMIT = 512

RSS_GROWTH_LIMIT_BYTES = 16 * 1024 * 1024


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        while True:
            chunk = f.read(
                8 * 1024 * 1024
            )

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write_json_exclusive(
    path: Path,
    value: dict[str, Any],
) -> None:
    raw = (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")

    with path.open("xb") as f:
        f.write(raw)


def copy_exclusive(
    source: Path,
    destination: Path,
) -> None:
    raw = source.read_bytes()

    with destination.open("xb") as f:
        f.write(raw)


def fd_count() -> int | None:
    root = Path("/proc/self/fd")

    if not root.is_dir():
        return None

    try:
        return len(list(root.iterdir()))
    except OSError:
        return None


def rss_bytes() -> int | None:
    path = Path("/proc/self/status")

    if not path.is_file():
        return None

    try:
        lines = path.read_text(
            encoding="utf-8"
        ).splitlines()
    except OSError:
        return None

    for line in lines:
        if not line.startswith("VmRSS:"):
            continue

        fields = line.split()

        if len(fields) < 2:
            return None

        try:
            kib = int(fields[1])
        except ValueError:
            return None

        return kib * 1024

    return None


def runtime_snapshot(
    root: Path,
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}

    if not root.is_dir():
        return result

    for path in sorted(
        root.rglob("*")
    ):
        if not path.is_file():
            continue

        relative = str(
            path.relative_to(root)
        )

        result[relative] = {
            "bytes":
                path.stat().st_size,
            "sha256":
                sha256_file(path),
        }

    return result


def positive_growth(
    before: int | None,
    after: int | None,
) -> int | None:
    if before is None or after is None:
        return None

    return max(
        0,
        after - before,
    )


def first_last_ratio(
    values: list[float],
) -> tuple[float, float, float]:
    if len(values) < 10:
        raise RuntimeError(
            "insufficient degradation batches"
        )

    initial = statistics.median(
        values[:5]
    )

    final = statistics.median(
        values[-5:]
    )

    if initial <= 0:
        raise RuntimeError(
            "invalid initial degradation median"
        )

    return (
        initial,
        final,
        final / initial,
    )


def measured_batch(
    operation: Callable[[], None],
    repeats: int,
) -> float:
    start = time.perf_counter_ns()

    for _ in range(repeats):
        operation()

    elapsed = (
        time.perf_counter_ns()
        - start
    )

    return elapsed / repeats


def run_batches(
    operation: Callable[[], None],
    warmups: int,
    batches: int,
    repeats: int,
) -> list[float]:
    for _ in range(warmups):
        measured_batch(
            operation,
            repeats,
        )

    return [
        measured_batch(
            operation,
            repeats,
        )
        for _ in range(batches)
    ]


def measure_retained_growth(
    operation: Callable[[], None],
    repeats: int,
) -> dict[str, int]:
    gc.collect()

    tracemalloc.start()

    try:
        gc.collect()

        before = tracemalloc.get_traced_memory()[0]

        for _ in range(repeats):
            operation()

        gc.collect()

        after = tracemalloc.get_traced_memory()[0]

    finally:
        tracemalloc.stop()

    return {
        "before_bytes":
            before,
        "after_bytes":
            after,
        "positive_growth_bytes":
            max(
                0,
                after - before,
            ),
    }


def live_reader_errors() -> int:
    gc.collect()

    return sum(
        1
        for obj in gc.get_objects()
        if isinstance(
            obj,
            reader.MAFSegmentReaderError,
        )
    )


def gc_object_count() -> int:
    gc.collect()
    return len(gc.get_objects())


def expect_failure(
    expected_type: type[BaseException],
    operation: Callable[[], bytes],
) -> dict[str, Any]:
    try:
        returned = operation()

    except Exception as exc:
        return {
            "raised": True,
            "expected_exception":
                isinstance(
                    exc,
                    expected_type,
                ),
            "exception_type":
                type(exc).__name__,
            "exception_message":
                str(exc),
            "returned":
                False,
            "returned_bytes":
                0,
        }

    return {
        "raised": False,
        "expected_exception": False,
        "exception_type": None,
        "exception_message": None,
        "returned": True,
        "returned_bytes":
            len(returned)
            if isinstance(
                returned,
                (bytes, bytearray),
            )
            else 0,
    }


class ShortReadOS:
    def __init__(self, base):
        self._base = base

    def __getattr__(self, name):
        return getattr(
            self._base,
            name,
        )

    def pread(
        self,
        fd,
        length,
        offset,
    ):
        raw = self._base.pread(
            fd,
            length,
            offset,
        )

        if not raw:
            return raw

        return raw[:-1]


class TrackingOS:
    def __init__(self, base):
        self._base = base
        self.events: list[tuple[str, int]] = []

    def __getattr__(self, name):
        return getattr(
            self._base,
            name,
        )

    def open(self, path, flags):
        fd = self._base.open(
            path,
            flags,
        )

        self.events.append(
            ("open", fd)
        )

        return fd

    def fstat(self, fd):
        self.events.append(
            ("fstat", fd)
        )

        return self._base.fstat(fd)

    def pread(
        self,
        fd,
        length,
        offset,
    ):
        self.events.append(
            ("pread", fd)
        )

        return self._base.pread(
            fd,
            length,
            offset,
        )

    def close(self, fd):
        self.events.append(
            ("close", fd)
        )

        return self._base.close(fd)


def install_write_audit():
    state = {
        "write_events": [],
        "mutation_events": [],
    }

    write_flag_mask = (
        getattr(os, "O_WRONLY", 0)
        | getattr(os, "O_RDWR", 0)
        | getattr(os, "O_CREAT", 0)
        | getattr(os, "O_TRUNC", 0)
        | getattr(os, "O_APPEND", 0)
    )

    mutation_events = {
        "os.remove",
        "os.rename",
        "os.replace",
        "os.rmdir",
        "os.mkdir",
        "os.truncate",
        "os.unlink",
    }

    def hook(event, args):
        if event == "open":
            path = (
                args[0]
                if len(args) >= 1
                else None
            )

            mode = (
                args[1]
                if len(args) >= 2
                else None
            )

            flags = (
                args[2]
                if len(args) >= 3
                else None
            )

            write_capable = False

            if isinstance(mode, str):
                write_capable = any(
                    token in mode
                    for token in (
                        "w",
                        "a",
                        "x",
                        "+",
                    )
                )

            if isinstance(flags, int):
                write_capable = (
                    write_capable
                    or bool(
                        flags
                        & write_flag_mask
                    )
                )

            if write_capable:
                state[
                    "write_events"
                ].append(
                    {
                        "event": event,
                        "path": repr(path),
                        "mode": repr(mode),
                        "flags": flags,
                    }
                )

        elif event in mutation_events:
            state[
                "mutation_events"
            ].append(
                {
                    "event": event,
                    "args":
                        repr(args),
                }
            )

    sys.addaudithook(hook)

    return state


def verify_frozen_identities() -> dict[str, Any]:
    expected = {
        "protocol":
            (
                PROTOCOL,
                PROTOCOL_SHA256,
            ),
        "segment_protocol":
            (
                SEGMENT_PROTOCOL,
                SEGMENT_PROTOCOL_SHA256,
            ),
        "engine":
            (
                ENGINE,
                ENGINE_SHA256,
            ),
        "validation_protocol":
            (
                VALIDATION_PROTOCOL,
                VALIDATION_PROTOCOL_SHA256,
            ),
        "validation_runner":
            (
                VALIDATION_RUNNER,
                VALIDATION_RUNNER_SHA256,
            ),
        "validation_result":
            (
                VALIDATION_RESULT,
                VALIDATION_RESULT_SHA256,
            ),
        "benchmark_completion":
            (
                BENCHMARK_COMPLETION,
                BENCHMARK_COMPLETION_SHA256,
            ),
        "source_active":
            (
                SOURCE_ACTIVE,
                SOURCE_ACTIVE_SHA256,
            ),
        "source_candidate":
            (
                SOURCE_CANDIDATE,
                SOURCE_CANDIDATE_SHA256,
            ),
        "source_segment":
            (
                SOURCE_SEGMENT,
                SOURCE_SEGMENT_SHA256,
            ),
    }

    observed = {}

    for name, (
        path,
        expected_sha,
    ) in expected.items():
        if not path.is_file():
            raise RuntimeError(
                f"missing frozen input: {name}"
            )

        actual = sha256_file(path)

        if actual != expected_sha:
            raise RuntimeError(
                f"frozen identity mismatch: {name}"
            )

        observed[name] = {
            "path": str(path),
            "sha256": actual,
        }

    if (
        SOURCE_SEGMENT.stat().st_size
        != SOURCE_SEGMENT_BYTES
    ):
        raise RuntimeError(
            "source segment size mismatch"
        )

    validation_result = json.loads(
        VALIDATION_RESULT.read_text(
            encoding="utf-8"
        )
    )

    if (
        validation_result.get("all_pass")
        is not True
    ):
        raise RuntimeError(
            "frozen validation result is not accepted"
        )

    return observed


def prepare_runtime():
    if RESULT.exists():
        raise RuntimeError(
            "refusing rerun: diagnostics result already exists"
        )

    if RUNTIME.exists():
        raise RuntimeError(
            "refusing rerun: diagnostics runtime already exists"
        )

    RUNTIME.mkdir()

    copy_exclusive(
        SOURCE_ACTIVE,
        RUNTIME / SOURCE_ACTIVE.name,
    )

    copy_exclusive(
        SOURCE_CANDIDATE,
        RUNTIME / SOURCE_CANDIDATE.name,
    )

    copy_exclusive(
        SOURCE_SEGMENT,
        RUNTIME / SOURCE_SEGMENT.name,
    )

    entries, _, manifest_sha = (
        validation.resolve_entries()
    )

    if manifest_sha != SOURCE_CANDIDATE_SHA256:
        raise RuntimeError(
            "validation helper manifest identity mismatch"
        )

    positive = [
        entry
        for entry in entries
        if (
            isinstance(entry.length, int)
            and not isinstance(
                entry.length,
                bool,
            )
            and entry.length > 0
        )
    ]

    if not positive:
        raise RuntimeError(
            "no positive Segment Reader diagnostic fixture"
        )

    source_entry = min(
        positive,
        key=lambda item: (
            item.length,
            item.object_pk,
        ),
    )

    isolated_segment = (
        RUNTIME
        / Path(
            source_entry.segment_path
        ).name
    )

    base = dataclasses.replace(
        source_entry,
        segment_path=str(
            isolated_segment
        ),
    )

    raw_segment = (
        isolated_segment.read_bytes()
    )

    expected = raw_segment[
        base.offset:
        base.offset + base.length
    ]

    if len(expected) != base.length:
        raise RuntimeError(
            "diagnostic fixture range length mismatch"
        )

    if (
        sha256_bytes(expected)
        != base.object_file_sha256
    ):
        raise RuntimeError(
            "diagnostic fixture object hash mismatch"
        )

    corrupt = bytearray(
        raw_segment
    )

    corrupt[
        base.offset
    ] ^= 0x01

    corrupt_path = (
        RUNTIME
        / "corrupt_segment.mafseg"
    )

    with corrupt_path.open("xb") as f:
        f.write(
            bytes(corrupt)
        )

    corrupt_entry = (
        dataclasses.replace(
            base,
            segment_path=str(
                corrupt_path
            ),
        )
    )

    wrong_hash = (
        "0" * 64
    )

    if (
        wrong_hash
        == base.object_file_sha256
    ):
        wrong_hash = (
            "f" * 64
        )

    wrong_hash_entry = (
        dataclasses.replace(
            base,
            object_file_sha256=
                wrong_hash,
        )
    )

    return {
        "base": base,
        "expected": expected,
        "corrupt_entry":
            corrupt_entry,
        "wrong_hash_entry":
            wrong_hash_entry,
        "initial_runtime_snapshot":
            runtime_snapshot(
                RUNTIME
            ),
    }


def run_diagnostics(
    identity_evidence: dict[str, Any],
) -> dict[str, Any]:
    prepared = prepare_runtime()

    base = prepared["base"]
    expected = prepared["expected"]
    corrupt_entry = (
        prepared[
            "corrupt_entry"
        ]
    )
    wrong_hash_entry = (
        prepared[
            "wrong_hash_entry"
        ]
    )

    initial_runtime_snapshot = (
        prepared[
            "initial_runtime_snapshot"
        ]
    )

    audit_state = install_write_audit()

    checks: dict[str, bool] = {}
    metrics: dict[str, Any] = {}

    def success_operation():
        returned = (
            reader.read_serialized_object(
                base,
                base.generation_pk,
            )
        )

        if returned != expected:
            raise RuntimeError(
                "successful diagnostic read returned unexpected bytes"
            )

    def failure_operation():
        try:
            reader.read_serialized_object(
                wrong_hash_entry,
                wrong_hash_entry.generation_pk,
            )
        except (
            reader.MAFSegmentReaderObjectHashMismatchError
        ):
            return

        raise RuntimeError(
            "expected object-hash failure did not occur"
        )

    # --------------------------------------------------------
    # Positive correctness.
    # --------------------------------------------------------

    positive = (
        reader.read_serialized_object(
            base,
            base.generation_pk,
        )
    )

    checks[
        "positive_exact_bytes"
    ] = (
        positive == expected
        and
        sha256_bytes(positive)
        == base.object_file_sha256
    )

    # --------------------------------------------------------
    # Same-descriptor dynamic control.
    # --------------------------------------------------------

    original_os = reader.os
    tracker = TrackingOS(
        original_os
    )

    try:
        reader.os = tracker

        tracked_return = (
            reader.read_serialized_object(
                base,
                base.generation_pk,
            )
        )

    finally:
        reader.os = original_os

    tracked_names = [
        name
        for name, _
        in tracker.events
    ]

    tracked_fds = [
        fd
        for _, fd
        in tracker.events
    ]

    checks[
        "same_fd_metadata_read_behavior"
    ] = (
        tracked_return == expected
        and
        tracked_names
        == [
            "open",
            "fstat",
            "pread",
            "close",
        ]
        and
        len(set(tracked_fds))
        == 1
    )

    metrics[
        "same_fd_events"
    ] = [
        {
            "operation": name,
            "fd": fd,
        }
        for name, fd
        in tracker.events
    ]

    # --------------------------------------------------------
    # Short-read control.
    # --------------------------------------------------------

    original_os = reader.os

    try:
        reader.os = ShortReadOS(
            original_os
        )

        short_read = expect_failure(
            reader.MAFSegmentReaderShortReadError,
            lambda:
                reader.read_serialized_object(
                    base,
                    base.generation_pk,
                ),
        )

    finally:
        reader.os = original_os

    checks[
        "short_read_handling"
    ] = (
        short_read[
            "raised"
        ]
        and short_read[
            "expected_exception"
        ]
        and not short_read[
            "returned"
        ]
    )

    # --------------------------------------------------------
    # Wrong-hash + corruption controls.
    # --------------------------------------------------------

    wrong_hash_control = (
        expect_failure(
            reader.MAFSegmentReaderObjectHashMismatchError,
            lambda:
                reader.read_serialized_object(
                    wrong_hash_entry,
                    wrong_hash_entry.generation_pk,
                ),
        )
    )

    corruption_control = (
        expect_failure(
            reader.MAFSegmentReaderObjectHashMismatchError,
            lambda:
                reader.read_serialized_object(
                    corrupt_entry,
                    corrupt_entry.generation_pk,
                ),
        )
    )

    checks[
        "mutation_corruption_failure_behavior"
    ] = (
        corruption_control[
            "raised"
        ]
        and corruption_control[
            "expected_exception"
        ]
        and not corruption_control[
            "returned"
        ]
    )

    checks[
        "unverified_byte_escape_blocked"
    ] = all(
        control[
            "raised"
        ]
        and control[
            "expected_exception"
        ]
        and not control[
            "returned"
        ]
        for control in (
            wrong_hash_control,
            corruption_control,
            short_read,
        )
    )

    metrics[
        "negative_controls"
    ] = {
        "wrong_hash":
            wrong_hash_control,
        "corruption":
            corruption_control,
        "short_read":
            short_read,
    }

    # --------------------------------------------------------
    # Warm baseline for resource measurements.
    # --------------------------------------------------------

    for _ in range(100):
        success_operation()

    for _ in range(100):
        failure_operation()

    gc.collect()

    rss_before = rss_bytes()
    fd_overall_before = fd_count()
    live_errors_before = (
        live_reader_errors()
    )
    gc_objects_before = (
        gc_object_count()
    )

    # --------------------------------------------------------
    # Success degradation.
    # --------------------------------------------------------

    success_batches = run_batches(
        success_operation,
        SUCCESS_BATCH_WARMUPS,
        SUCCESS_BATCHES,
        SUCCESS_READS_PER_BATCH,
    )

    (
        success_initial,
        success_final,
        success_ratio,
    ) = first_last_ratio(
        success_batches
    )

    checks[
        "repeated_success_degradation"
    ] = (
        success_ratio
        <= SUCCESS_DEGRADATION_LIMIT
    )

    metrics[
        "success_degradation"
    ] = {
        "batch_ns_per_operation":
            success_batches,
        "initial_median_ns":
            success_initial,
        "final_median_ns":
            success_final,
        "final_over_initial_ratio":
            success_ratio,
        "limit":
            SUCCESS_DEGRADATION_LIMIT,
    }

    # --------------------------------------------------------
    # Failure degradation.
    # --------------------------------------------------------

    failure_batches = run_batches(
        failure_operation,
        FAILURE_BATCH_WARMUPS,
        FAILURE_BATCHES,
        FAILURES_PER_BATCH,
    )

    (
        failure_initial,
        failure_final,
        failure_ratio,
    ) = first_last_ratio(
        failure_batches
    )

    checks[
        "repeated_failure_degradation"
    ] = (
        failure_ratio
        <= FAILURE_DEGRADATION_LIMIT
    )

    metrics[
        "failure_degradation"
    ] = {
        "batch_ns_per_operation":
            failure_batches,
        "initial_median_ns":
            failure_initial,
        "final_median_ns":
            failure_final,
        "final_over_initial_ratio":
            failure_ratio,
        "limit":
            FAILURE_DEGRADATION_LIMIT,
    }

    # --------------------------------------------------------
    # Dedicated descriptor-leak sentinels.
    # --------------------------------------------------------

    success_fd_before = fd_count()

    for _ in range(
        SUCCESS_FD_REPEATS
    ):
        success_operation()

    success_fd_after = fd_count()

    success_fd_growth = (
        positive_growth(
            success_fd_before,
            success_fd_after,
        )
    )

    failure_fd_before = fd_count()

    for _ in range(
        FAILURE_FD_REPEATS
    ):
        failure_operation()

    failure_fd_after = fd_count()

    failure_fd_growth = (
        positive_growth(
            failure_fd_before,
            failure_fd_after,
        )
    )

    checks[
        "success_fd_leak"
    ] = (
        success_fd_growth is None
        or success_fd_growth
        <= FD_GROWTH_LIMIT
    )

    checks[
        "failure_fd_leak"
    ] = (
        failure_fd_growth is None
        or failure_fd_growth
        <= FD_GROWTH_LIMIT
    )

    # --------------------------------------------------------
    # Retained Python allocation growth.
    # --------------------------------------------------------

    success_retained = (
        measure_retained_growth(
            success_operation,
            SUCCESS_RETAIN_REPEATS,
        )
    )

    failure_retained = (
        measure_retained_growth(
            failure_operation,
            FAILURE_RETAIN_REPEATS,
        )
    )

    checks[
        "success_retained_python_growth"
    ] = (
        success_retained[
            "positive_growth_bytes"
        ]
        <= SUCCESS_RETAINED_LIMIT_BYTES
    )

    checks[
        "failure_retained_python_growth"
    ] = (
        failure_retained[
            "positive_growth_bytes"
        ]
        <= FAILURE_RETAINED_LIMIT_BYTES
    )

    # --------------------------------------------------------
    # Final resource state.
    # --------------------------------------------------------

    gc.collect()

    live_errors_after = (
        live_reader_errors()
    )

    gc_objects_after = (
        gc_object_count()
    )

    rss_after = rss_bytes()
    fd_overall_after = fd_count()

    live_error_growth = max(
        0,
        live_errors_after
        - live_errors_before,
    )

    gc_growth = max(
        0,
        gc_objects_after
        - gc_objects_before,
    )

    overall_fd_growth = (
        positive_growth(
            fd_overall_before,
            fd_overall_after,
        )
    )

    rss_growth = (
        positive_growth(
            rss_before,
            rss_after,
        )
    )

    checks[
        "live_reader_error_object_growth"
    ] = (
        live_error_growth
        <= LIVE_ERROR_GROWTH_LIMIT
    )

    checks[
        "gc_tracked_object_growth"
    ] = (
        gc_growth
        <= GC_OBJECT_GROWTH_LIMIT
    )

    checks[
        "overall_fd_leak"
    ] = (
        overall_fd_growth is None
        or overall_fd_growth
        <= FD_GROWTH_LIMIT
    )

    checks[
        "rss_growth_where_measurable"
    ] = (
        rss_growth is None
        or rss_growth
        <= RSS_GROWTH_LIMIT_BYTES
    )

    # --------------------------------------------------------
    # Runtime/source immutability and write audit.
    # --------------------------------------------------------

    final_runtime_snapshot = (
        runtime_snapshot(
            RUNTIME
        )
    )

    checks[
        "runtime_file_accumulation"
    ] = (
        final_runtime_snapshot
        == initial_runtime_snapshot
    )

    write_events = list(
        audit_state[
            "write_events"
        ]
    )

    mutation_events = list(
        audit_state[
            "mutation_events"
        ]
    )

    checks[
        "unexpected_filesystem_writes"
    ] = (
        not write_events
        and not mutation_events
    )

    source_final = {
        "active_generation":
            sha256_file(
                SOURCE_ACTIVE
            ),
        "candidate_manifest":
            sha256_file(
                SOURCE_CANDIDATE
            ),
        "segment":
            sha256_file(
                SOURCE_SEGMENT
            ),
    }

    checks[
        "source_runtime_unchanged"
    ] = (
        source_final[
            "active_generation"
        ]
        == SOURCE_ACTIVE_SHA256
        and
        source_final[
            "candidate_manifest"
        ]
        == SOURCE_CANDIDATE_SHA256
        and
        source_final[
            "segment"
        ]
        == SOURCE_SEGMENT_SHA256
    )

    # Frozen identities are rechecked after diagnostic work.
    identity_final = (
        verify_frozen_identities()
    )

    checks[
        "frozen_identities_unchanged"
    ] = (
        identity_final
        == identity_evidence
    )

    metrics[
        "resources"
    ] = {
        "fd_measured":
            (
                fd_overall_before
                is not None
                and fd_overall_after
                is not None
            ),
        "success_fd_before":
            success_fd_before,
        "success_fd_after":
            success_fd_after,
        "success_fd_growth":
            success_fd_growth,
        "failure_fd_before":
            failure_fd_before,
        "failure_fd_after":
            failure_fd_after,
        "failure_fd_growth":
            failure_fd_growth,
        "overall_fd_before":
            fd_overall_before,
        "overall_fd_after":
            fd_overall_after,
        "overall_fd_growth":
            overall_fd_growth,
        "fd_growth_limit":
            FD_GROWTH_LIMIT,

        "success_retained":
            success_retained,
        "failure_retained":
            failure_retained,
        "success_retained_limit_bytes":
            SUCCESS_RETAINED_LIMIT_BYTES,
        "failure_retained_limit_bytes":
            FAILURE_RETAINED_LIMIT_BYTES,

        "live_reader_errors_before":
            live_errors_before,
        "live_reader_errors_after":
            live_errors_after,
        "live_reader_error_growth":
            live_error_growth,
        "live_reader_error_growth_limit":
            LIVE_ERROR_GROWTH_LIMIT,

        "gc_objects_before":
            gc_objects_before,
        "gc_objects_after":
            gc_objects_after,
        "gc_object_growth":
            gc_growth,
        "gc_object_growth_limit":
            GC_OBJECT_GROWTH_LIMIT,

        "rss_measured":
            (
                rss_before is not None
                and rss_after is not None
            ),
        "rss_before_bytes":
            rss_before,
        "rss_after_bytes":
            rss_after,
        "rss_positive_growth_bytes":
            rss_growth,
        "rss_growth_limit_bytes":
            RSS_GROWTH_LIMIT_BYTES,
    }

    metrics[
        "filesystem"
    ] = {
        "initial_runtime_snapshot":
            initial_runtime_snapshot,
        "final_runtime_snapshot":
            final_runtime_snapshot,
        "write_events":
            write_events,
        "mutation_events":
            mutation_events,
        "source_final_sha256":
            source_final,
    }

    all_pass = all(
        checks.values()
    )

    return {
        "schema":
            SCHEMA,
        "version":
            VERSION,
        "diagnostics_valid":
            True,
        "all_pass":
            all_pass,
        "fatal_error":
            None,
        "phase_6c_started":
            False,

        "identities":
            identity_evidence,

        "fixture": {
            "object_pk":
                base.object_pk,
            "generation_pk":
                base.generation_pk,
            "segment_id":
                base.segment_id,
            "offset":
                base.offset,
            "length":
                base.length,
            "object_file_sha256":
                base.object_file_sha256,
            "segment_length":
                base.segment_length,
            "segment_sha256":
                base.segment_sha256,
            "diagnostic_segment_path":
                base.segment_path,
        },

        "constants": {
            "success_batch_warmups":
                SUCCESS_BATCH_WARMUPS,
            "success_batches":
                SUCCESS_BATCHES,
            "success_reads_per_batch":
                SUCCESS_READS_PER_BATCH,

            "failure_batch_warmups":
                FAILURE_BATCH_WARMUPS,
            "failure_batches":
                FAILURE_BATCHES,
            "failures_per_batch":
                FAILURES_PER_BATCH,

            "success_degradation_limit":
                SUCCESS_DEGRADATION_LIMIT,
            "failure_degradation_limit":
                FAILURE_DEGRADATION_LIMIT,

            "success_retain_repeats":
                SUCCESS_RETAIN_REPEATS,
            "failure_retain_repeats":
                FAILURE_RETAIN_REPEATS,
        },

        "checks":
            checks,

        "metrics":
            metrics,
    }


def fatal_result(
    identity_evidence: dict[str, Any] | None,
    exc: BaseException,
) -> dict[str, Any]:
    current_runtime = {}

    try:
        current_runtime = (
            runtime_snapshot(
                RUNTIME
            )
        )
    except Exception:
        current_runtime = {
            "snapshot_error":
                True
        }

    return {
        "schema":
            SCHEMA,
        "version":
            VERSION,
        "diagnostics_valid":
            False,
        "all_pass":
            False,
        "phase_6c_started":
            False,
        "identities":
            identity_evidence,
        "checks":
            {},
        "metrics": {
            "current_runtime_snapshot":
                current_runtime,
        },
        "fatal_error": {
            "type":
                type(exc).__name__,
            "message":
                str(exc),
        },
    }


def main() -> int:
    if RESULT.exists():
        raise RuntimeError(
            "refusing rerun: diagnostics result already exists"
        )

    if RUNTIME.exists():
        raise RuntimeError(
            "refusing rerun: diagnostics runtime already exists"
        )

    identity_evidence = None

    try:
        identity_evidence = (
            verify_frozen_identities()
        )

        result = run_diagnostics(
            identity_evidence
        )

    except Exception as exc:
        result = fatal_result(
            identity_evidence,
            exc,
        )

    write_json_exclusive(
        RESULT,
        result,
    )

    print("=" * 72)
    print(
        " OPENMIND / "
        "MAF SEGMENT READER DIAGNOSTICS V1"
    )
    print("=" * 72)

    print(
        "diagnostics_valid:",
        result[
            "diagnostics_valid"
        ],
    )

    print(
        "all_pass:",
        result[
            "all_pass"
        ],
    )

    print(
        "fatal_error:",
        result[
            "fatal_error"
        ],
    )

    checks = result.get(
        "checks",
        {},
    )

    failed = [
        name
        for name, value
        in checks.items()
        if value is not True
    ]

    print(
        "checks:",
        len(checks),
    )
    print(
        "failed_checks:",
        failed,
    )
    print(
        "result:",
        RESULT,
    )

    return (
        0
        if (
            result[
                "diagnostics_valid"
            ]
            and result[
                "all_pass"
            ]
        )
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
