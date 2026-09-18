import gc
import hashlib
import inspect
import json
import os
import shutil
import statistics
import sys
import time
import tracemalloc
from dataclasses import FrozenInstanceError
from pathlib import Path

import maf_resident_pk_directory_v1 as resident

SCHEMA = "openmind.maf_resident_pk_directory_diagnostics.v1_3"
VERSION = "maf_resident_pk_directory_diagnostics_v1_3"

PROTOCOL = Path("experiments/model_fractal/MAF_RESIDENT_PK_DIRECTORY_DIAGNOSTICS_V1_PROTOCOL.md")
PROTOCOL_SHA256 = "5101e4a4dd78b869eb91ce226a1a304181bc2c3636d2ff86a056db15caf0560a"

CORRECTION_PROTOCOL = Path("experiments/model_fractal/MAF_RESIDENT_PK_DIRECTORY_DIAGNOSTICS_V1_1_CORRECTION_PROTOCOL.md")
CORRECTION_PROTOCOL_SHA256 = "9f01c39fe8777c6f93eae550d16596af625d3cb86d07993e500c0479648b35ab"

V1_2_CORRECTION_PROTOCOL = Path("experiments/model_fractal/MAF_RESIDENT_PK_DIRECTORY_DIAGNOSTICS_V1_2_CORRECTION_PROTOCOL.md")
V1_2_CORRECTION_PROTOCOL_SHA256 = "fbaaeb38346d5173637f31579e72e880a807dfea31d7d92434fc9af040cf23a8"

V1_3_CORRECTION_PROTOCOL = Path("experiments/model_fractal/MAF_RESIDENT_PK_DIRECTORY_DIAGNOSTICS_V1_3_CORRECTION_PROTOCOL.md")
V1_3_CORRECTION_PROTOCOL_SHA256 = "e6e3a0d3995550106c9abf8a60c586b01083fb6e971573df26f3552c06292ff6"

ENGINE = Path("experiments/model_fractal/maf_resident_pk_directory_v1.py")
ENGINE_SHA256 = "4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6"

FUNCTIONAL_RESULT = Path("experiments/model_fractal/maf_resident_pk_directory_validation_v1.json")
FUNCTIONAL_RESULT_SHA256 = "24540c16eac53e9a179781c7007d61d98b34f7bc74e1f3dfc462b5786dd186b1"

BENCHMARK_RESULT = Path("experiments/model_fractal/benchmark_maf_resident_pk_directory_v1_1.json")
BENCHMARK_RESULT_SHA256 = "57562c9fbcac012c6706903ff07c23a15b5bf59bb0599a9f6dd04ceecbec95b1"

SOURCE_RUNTIME = Path("results/runtime/maf_resident_pk_directory_benchmark_v1_1")
SOURCE_CANDIDATE = SOURCE_RUNTIME / "candidate_a.manifest.json"
SOURCE_ACTIVE = SOURCE_RUNTIME / "active_generation.json"
SOURCE_CANDIDATE_SHA256 = "941301aa362d3f949389e5364b1be4d7f26b96f0d45efa81346c82fce3260f93"
SOURCE_ACTIVE_SHA256 = "031d1a50a3cf53f158057a02bb6c68001edfb07bf48bf893afc9bc8f095458e9"

RESULT = Path("experiments/model_fractal/maf_resident_pk_directory_diagnostics_v1_3.json")
RUNTIME = Path("results/runtime/maf_resident_pk_directory_diagnostics_v1_3")

REBUILD_REPEATS = 200
FAILED_REFRESH_REPEATS = 200
HOT_LOOKUP_REPEATS = 50000
LEAK_LOOKUP_REPEATS = 100000
LEAK_REFRESH_REPEATS = 500

LOOKUP_BATCH_WARMUPS = 2
LOOKUP_BATCHES = 20
LOOKUPS_PER_BATCH = 5000

REFRESH_BATCH_WARMUPS = 2
REFRESH_BATCHES = 20
REFRESHES_PER_BATCH = 25

LOOKUP_RETAINED_LIMIT_BYTES = 262144
REFRESH_RETAINED_LIMIT_BYTES = 1048576
BUILD_RETAINED_LIMIT_BYTES = 1048576
FAILED_REFRESH_RETAINED_LIMIT_BYTES = 1048576
BUILD_LIVE_SNAPSHOT_GROWTH_LIMIT = 2
FAILED_REFRESH_LIVE_SNAPSHOT_GROWTH_LIMIT = 2
BUILD_RSS_GROWTH_LIMIT_BYTES = 16 * 1024 * 1024
FAILED_REFRESH_RSS_GROWTH_LIMIT_BYTES = 16 * 1024 * 1024
BUILD_FD_GROWTH_LIMIT = 2
FAILED_REFRESH_FD_GROWTH_LIMIT = 2
LIVE_SNAPSHOT_GROWTH_LIMIT = 2
RSS_GROWTH_LIMIT_BYTES = 16 * 1024 * 1024
FD_GROWTH_LIMIT = 2
LOOKUP_DEGRADATION_LIMIT = 2.0
REFRESH_DEGRADATION_LIMIT = 2.5
BUILD_BATCH_WARMUPS = 2
BUILD_BATCHES = 20
BUILDS_PER_BATCH = 25
BUILD_DEGRADATION_LIMIT = 2.5
STALE_STATE_REPEATS = 200
STALE_RETAINED_LIMIT_BYTES = 262144
STALE_LIVE_SNAPSHOT_GROWTH_LIMIT = 2
STALE_RSS_GROWTH_LIMIT_BYTES = 16 * 1024 * 1024
STALE_FD_GROWTH_LIMIT = 2


def file_sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            block = f.read(1024 * 1024)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def read_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json_exclusive(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")


def runtime_stats(root):
    files = [p for p in root.rglob("*") if p.is_file()]
    return {
        "file_count": len(files),
        "byte_count": sum(p.stat().st_size for p in files),
    }


def rss_bytes():
    with Path("/proc/self/status").open("r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("VmRSS:"):
                return int(line.split()[1]) * 1024
    raise RuntimeError("VmRSS unavailable")


def fd_count():
    return len(list(Path("/proc/self/fd").iterdir()))


def live_snapshot_count():
    return sum(
        1
        for obj in gc.get_objects()
        if isinstance(obj, resident.ResidentPKSnapshot)
    )


def projection_digest(snapshot):
    rows = []
    for key, entry in snapshot.entries.items():
        rows.append((
            key,
            entry.model_pk,
            entry.generation_pk,
            entry.generation_manifest_sha256,
            entry.object_pk,
            entry.segment_id,
            entry.offset,
            entry.length,
            entry.object_file_sha256,
            entry.payload_sha256,
            entry.segment_length,
            entry.segment_sha256,
            str(entry.segment_path),
        ))
    raw = repr(sorted(rows)).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def prepare_lookup(snapshot, key, expected_generation_pk=None):
    values = {
        "model_pk": snapshot.model_pk,
        "pk_kind": key[1],
        "pk_class": key[1],
        "logical_pk": key[2],
        "object_pk": key[2],
        "expected_generation_pk": (
            snapshot.generation_pk
            if expected_generation_pk is None
            else expected_generation_pk
        ),
    }
    sig = inspect.signature(snapshot.lookup)
    kwargs = {}
    for name, param in sig.parameters.items():
        if name in values:
            kwargs[name] = values[name]
            continue
        if param.default is inspect.Parameter.empty:
            raise RuntimeError("unsupported required lookup parameter: " + name)
    bound_lookup = snapshot.lookup

    def operation():
        return bound_lookup(**kwargs)

    return operation


def manager_snapshot(manager):
    found = []
    for name in dir(manager):
        try:
            value = getattr(manager, name)
        except Exception:
            continue
        if isinstance(value, resident.ResidentPKSnapshot):
            found.append(value)
    unique = []
    for value in found:
        if all(value is not prior for prior in unique):
            unique.append(value)
    if len(unique) != 1:
        raise RuntimeError("unable to identify exactly one manager snapshot")
    return unique[0]


def locate_source_segment(length, expected_sha):
    matches = []
    for path in SOURCE_RUNTIME.rglob("*"):
        if not path.is_file():
            continue
        if path in (SOURCE_CANDIDATE, SOURCE_ACTIVE):
            continue
        if path.stat().st_size != length:
            continue
        if file_sha256(path) == expected_sha:
            matches.append(path)
    if len(matches) != 1:
        raise RuntimeError(
            "expected exactly one retained physical segment match; found " +
            str(len(matches))
        )
    return matches[0]


def prepare_runtime():
    if RUNTIME.exists():
        raise RuntimeError("diagnostic runtime already exists")

    if file_sha256(SOURCE_CANDIDATE) != SOURCE_CANDIDATE_SHA256:
        raise RuntimeError("source candidate SHA mismatch")

    if file_sha256(SOURCE_ACTIVE) != SOURCE_ACTIVE_SHA256:
        raise RuntimeError("source active-record SHA mismatch")

    manifest = read_json(SOURCE_CANDIDATE)
    descriptor = manifest["descriptor"]

    RUNTIME.mkdir(parents=True, exist_ok=False)
    candidate = RUNTIME / "candidate_a.manifest.json"
    active = RUNTIME / "active_generation.json"
    segment_dir = RUNTIME / "segments"
    segment_dir.mkdir(parents=False, exist_ok=False)

    shutil.copyfile(SOURCE_CANDIDATE, candidate)
    shutil.copyfile(SOURCE_ACTIVE, active)

    segment_paths = {}

    for index, row in enumerate(descriptor["segments"]):
        segment_id = row["segment_id"]
        length = int(row["segment_length"])
        expected_sha = row["segment_sha256"]
        source = locate_source_segment(length, expected_sha)
        target = segment_dir / ("segment_%04d.mafseg" % index)
        shutil.copyfile(source, target)
        if target.stat().st_size != length:
            raise RuntimeError("copied segment length mismatch")
        if file_sha256(target) != expected_sha:
            raise RuntimeError("copied segment SHA mismatch")
        segment_paths[segment_id] = target

    return {
        "manifest": manifest,
        "candidate": candidate,
        "active": active,
        "segment_paths": segment_paths,
    }


def build_from_prepared(prepared):
    descriptor = prepared["manifest"]["descriptor"]
    return resident.build_snapshot(
        model_pk=descriptor["model_pk"],
        active_record_path=prepared["active"],
        active_candidate_manifest_path=prepared["candidate"],
        active_segment_paths=prepared["segment_paths"],
    )


def refresh_from_prepared(manager, prepared, segment_paths=None):
    descriptor = prepared["manifest"]["descriptor"]
    if segment_paths is None:
        segment_paths = prepared["segment_paths"]
    return manager.refresh(
        model_pk=descriptor["model_pk"],
        active_record_path=prepared["active"],
        active_candidate_manifest_path=prepared["candidate"],
        active_segment_paths=segment_paths,
    )


def batch_ns_per_op(operation, iterations):
    start = time.perf_counter_ns()
    for _ in range(iterations):
        operation()
    elapsed = time.perf_counter_ns() - start
    return elapsed / iterations


def degradation_ratio(values):
    first = statistics.median(values[:5])
    last = statistics.median(values[-5:])
    if first <= 0:
        raise RuntimeError("invalid degradation baseline")
    return last / first


def run_diagnostics():
    prepared = prepare_runtime()
    snapshot = build_from_prepared(prepared)

    if not snapshot.entries:
        raise RuntimeError("resident snapshot unexpectedly empty")

    keys = sorted(snapshot.entries)
    target_key = keys[-1]
    expected_entry = snapshot.entries[target_key]
    lookup_operation = prepare_lookup(snapshot, target_key)
    initial_digest = projection_digest(snapshot)

    stale_generation_pk = (
        snapshot.generation_pk[:-1]
        + ("0" if snapshot.generation_pk[-1] != "0" else "1")
    )
    stale_lookup_operation = prepare_lookup(
        snapshot,
        target_key,
        expected_generation_pk=stale_generation_pk,
    )

    lookup_signature = str(inspect.signature(snapshot.lookup))

    checks = {}

    write_open_counter = {"count": 0}

    def write_audit_hook(event, args):
        if event != "open":
            return
        mode = args[1] if len(args) > 1 else None
        flags = args[2] if len(args) > 2 else 0
        mode_writes = (
            isinstance(mode, str)
            and any(ch in mode for ch in ("w", "a", "x", "+"))
        )
        flag_mask = (
            os.O_WRONLY
            | os.O_RDWR
            | os.O_CREAT
            | os.O_TRUNC
            | os.O_APPEND
        )
        flag_writes = isinstance(flags, int) and bool(flags & flag_mask)
        if mode_writes or flag_writes:
            write_open_counter["count"] += 1

    sys.addaudithook(write_audit_hook)
    write_opens_baseline = write_open_counter["count"]

    checks["initial_snapshot_nonempty"] = len(snapshot.entries) > 0
    checks["initial_lookup_exact"] = lookup_operation() is expected_entry

    mapping_immutable = False
    try:
        snapshot.entries[target_key] = expected_entry
    except TypeError:
        mapping_immutable = True
    checks["mapping_immutable"] = mapping_immutable

    entry_immutable = False
    try:
        expected_entry.length = expected_entry.length
    except (FrozenInstanceError, AttributeError):
        entry_immutable = True
    checks["entry_immutable"] = entry_immutable

    gc.collect()
    build_live_before = live_snapshot_count()
    build_fd_before = fd_count()
    build_rss_before = rss_bytes()
    build_runtime_before = runtime_stats(RUNTIME)
    tracemalloc.start()
    build_mem_before, _ = tracemalloc.get_traced_memory()

    rebuild_exact = True
    for _ in range(REBUILD_REPEATS):
        rebuilt = build_from_prepared(prepared)
        if projection_digest(rebuilt) != initial_digest:
            rebuild_exact = False
            break
    checks["rebuild_projection_stable"] = rebuild_exact
    try:
        del rebuilt
    except UnboundLocalError:
        pass

    gc.collect()
    build_mem_after, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    build_live_after = live_snapshot_count()
    build_fd_after = fd_count()
    build_rss_after = rss_bytes()
    build_runtime_after = runtime_stats(RUNTIME)
    build_retained_growth = build_mem_after - build_mem_before

    checks["build_retained_growth_within_limit"] = (
        build_retained_growth <= BUILD_RETAINED_LIMIT_BYTES
    )
    checks["build_live_snapshot_growth_within_limit"] = (
        build_live_after - build_live_before
        <= BUILD_LIVE_SNAPSHOT_GROWTH_LIMIT
    )
    checks["build_fd_growth_within_limit"] = (
        build_fd_after - build_fd_before <= BUILD_FD_GROWTH_LIMIT
    )
    checks["build_rss_growth_within_limit"] = (
        build_rss_after - build_rss_before
        <= BUILD_RSS_GROWTH_LIMIT_BYTES
    )
    checks["build_runtime_file_count_stable"] = (
        build_runtime_after["file_count"]
        == build_runtime_before["file_count"]
    )
    checks["build_runtime_byte_count_stable"] = (
        build_runtime_after["byte_count"]
        == build_runtime_before["byte_count"]
    )

    manager = resident.ResidentPKDirectory()
    first_refresh = refresh_from_prepared(manager, prepared)
    checks["successful_refresh_published_returned_snapshot"] = (
        manager_snapshot(manager) is first_refresh
    )

    gc.collect()
    failed_live_before = live_snapshot_count()
    failed_fd_before = fd_count()
    failed_rss_before = rss_bytes()
    failed_runtime_before = runtime_stats(RUNTIME)
    tracemalloc.start()
    failed_mem_before, _ = tracemalloc.get_traced_memory()

    failed_refresh_count = 0
    failed_refresh_preserved = True

    for _ in range(FAILED_REFRESH_REPEATS):
        before = manager_snapshot(manager)
        try:
            refresh_from_prepared(manager, prepared, segment_paths={})
        except Exception:
            failed_refresh_count += 1
        else:
            failed_refresh_preserved = False
            break
        if manager_snapshot(manager) is not before:
            failed_refresh_preserved = False
            break

    gc.collect()
    failed_mem_after, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    failed_live_after = live_snapshot_count()
    failed_fd_after = fd_count()
    failed_rss_after = rss_bytes()
    failed_runtime_after = runtime_stats(RUNTIME)
    failed_refresh_retained_growth = (
        failed_mem_after - failed_mem_before
    )

    checks["failed_refresh_retained_growth_within_limit"] = (
        failed_refresh_retained_growth
        <= FAILED_REFRESH_RETAINED_LIMIT_BYTES
    )
    checks["failed_refresh_live_snapshot_growth_within_limit"] = (
        failed_live_after - failed_live_before
        <= FAILED_REFRESH_LIVE_SNAPSHOT_GROWTH_LIMIT
    )
    checks["failed_refresh_fd_growth_within_limit"] = (
        failed_fd_after - failed_fd_before
        <= FAILED_REFRESH_FD_GROWTH_LIMIT
    )
    checks["failed_refresh_rss_growth_within_limit"] = (
        failed_rss_after - failed_rss_before
        <= FAILED_REFRESH_RSS_GROWTH_LIMIT_BYTES
    )
    checks["failed_refresh_runtime_file_count_stable"] = (
        failed_runtime_after["file_count"]
        == failed_runtime_before["file_count"]
    )
    checks["failed_refresh_runtime_byte_count_stable"] = (
        failed_runtime_after["byte_count"]
        == failed_runtime_before["byte_count"]
    )

    checks["all_invalid_refreshes_failed"] = (
        failed_refresh_count == FAILED_REFRESH_REPEATS
    )
    checks["invalid_refresh_preserved_prior_snapshot"] = failed_refresh_preserved

    gc.collect()
    stale_live_before = live_snapshot_count()
    stale_fd_before = fd_count()
    stale_rss_before = rss_bytes()
    stale_runtime_before = runtime_stats(RUNTIME)
    tracemalloc.start()
    stale_mem_before, _ = tracemalloc.get_traced_memory()

    stale_rejection_count = 0
    stale_exception_types = set()

    for _ in range(STALE_STATE_REPEATS):
        try:
            stale_lookup_operation()
        except Exception as exc:
            stale_rejection_count += 1
            stale_exception_types.add(type(exc).__name__)
        else:
            break

    gc.collect()
    stale_mem_after, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    stale_live_after = live_snapshot_count()
    stale_fd_after = fd_count()
    stale_rss_after = rss_bytes()
    stale_runtime_after = runtime_stats(RUNTIME)
    stale_retained_growth = stale_mem_after - stale_mem_before

    checks["stale_generation_rejected_repeatedly"] = (
        stale_rejection_count == STALE_STATE_REPEATS
    )
    checks["stale_rejection_exception_type_stable"] = (
        len(stale_exception_types) == 1
    )
    checks["stale_projection_preserved"] = (
        projection_digest(snapshot) == initial_digest
    )
    checks["stale_retained_growth_within_limit"] = (
        stale_retained_growth <= STALE_RETAINED_LIMIT_BYTES
    )
    checks["stale_live_snapshot_growth_within_limit"] = (
        stale_live_after - stale_live_before
        <= STALE_LIVE_SNAPSHOT_GROWTH_LIMIT
    )
    checks["stale_fd_growth_within_limit"] = (
        stale_fd_after - stale_fd_before <= STALE_FD_GROWTH_LIMIT
    )
    checks["stale_rss_growth_within_limit"] = (
        stale_rss_after - stale_rss_before
        <= STALE_RSS_GROWTH_LIMIT_BYTES
    )
    checks["stale_runtime_file_count_stable"] = (
        stale_runtime_after["file_count"]
        == stale_runtime_before["file_count"]
    )
    checks["stale_runtime_byte_count_stable"] = (
        stale_runtime_after["byte_count"]
        == stale_runtime_before["byte_count"]
    )

    hot_open_counter = {"count": 0}

    def audit_hook(event, args):
        if event == "open":
            hot_open_counter["count"] += 1

    sys.addaudithook(audit_hook)
    opens_before = hot_open_counter["count"]

    hot_lookup_exact = True
    for _ in range(HOT_LOOKUP_REPEATS):
        if lookup_operation() is not expected_entry:
            hot_lookup_exact = False
            break

    opens_after = hot_open_counter["count"]

    checks["hot_lookup_exact_repeated"] = hot_lookup_exact
    checks["hot_lookup_zero_open_events"] = opens_after == opens_before

    for _ in range(5000):
        lookup_operation()
    for _ in range(25):
        refresh_from_prepared(manager, prepared)

    tracemalloc.start()
    gc.collect()

    runtime_before = runtime_stats(RUNTIME)
    fd_before = fd_count()
    rss_before = rss_bytes()
    live_before = live_snapshot_count()

    lookup_before, _ = tracemalloc.get_traced_memory()

    for _ in range(LEAK_LOOKUP_REPEATS):
        lookup_operation()

    gc.collect()
    lookup_after, _ = tracemalloc.get_traced_memory()
    lookup_retained_growth = lookup_after - lookup_before

    refresh_before, _ = tracemalloc.get_traced_memory()

    for _ in range(LEAK_REFRESH_REPEATS):
        latest = refresh_from_prepared(manager, prepared)

    del latest
    gc.collect()
    refresh_after, _ = tracemalloc.get_traced_memory()
    refresh_retained_growth = refresh_after - refresh_before

    live_after = live_snapshot_count()
    fd_after = fd_count()
    rss_after = rss_bytes()
    runtime_after = runtime_stats(RUNTIME)

    tracemalloc.stop()

    checks["lookup_retained_growth_within_limit"] = (
        lookup_retained_growth <= LOOKUP_RETAINED_LIMIT_BYTES
    )
    checks["refresh_retained_growth_within_limit"] = (
        refresh_retained_growth <= REFRESH_RETAINED_LIMIT_BYTES
    )
    checks["live_snapshot_growth_within_limit"] = (
        live_after - live_before <= LIVE_SNAPSHOT_GROWTH_LIMIT
    )
    checks["fd_growth_within_limit"] = (
        fd_after - fd_before <= FD_GROWTH_LIMIT
    )
    checks["rss_growth_within_limit"] = (
        rss_after - rss_before <= RSS_GROWTH_LIMIT_BYTES
    )
    checks["runtime_file_count_stable"] = (
        runtime_after["file_count"] == runtime_before["file_count"]
    )
    checks["runtime_byte_count_stable"] = (
        runtime_after["byte_count"] == runtime_before["byte_count"]
    )

    for _ in range(LOOKUP_BATCH_WARMUPS):
        batch_ns_per_op(lookup_operation, LOOKUPS_PER_BATCH)

    lookup_batches = [
        batch_ns_per_op(lookup_operation, LOOKUPS_PER_BATCH)
        for _ in range(LOOKUP_BATCHES)
    ]

    lookup_ratio = degradation_ratio(lookup_batches)
    checks["lookup_degradation_within_limit"] = (
        lookup_ratio <= LOOKUP_DEGRADATION_LIMIT
    )

    refresh_operation = lambda: refresh_from_prepared(manager, prepared)

    for _ in range(REFRESH_BATCH_WARMUPS):
        batch_ns_per_op(refresh_operation, REFRESHES_PER_BATCH)

    refresh_batches = [
        batch_ns_per_op(refresh_operation, REFRESHES_PER_BATCH)
        for _ in range(REFRESH_BATCHES)
    ]

    refresh_ratio = degradation_ratio(refresh_batches)

    build_operation = lambda: build_from_prepared(prepared)

    for _ in range(BUILD_BATCH_WARMUPS):
        batch_ns_per_op(build_operation, BUILDS_PER_BATCH)

    build_batches = [
        batch_ns_per_op(build_operation, BUILDS_PER_BATCH)
        for _ in range(BUILD_BATCHES)
    ]

    build_ratio = degradation_ratio(build_batches)

    checks["build_degradation_within_limit"] = (
        build_ratio <= BUILD_DEGRADATION_LIMIT
    )
    checks["hash_file_validation_degradation_within_limit"] = (
        build_ratio <= BUILD_DEGRADATION_LIMIT
    )
    checks["refresh_degradation_within_limit"] = (
        refresh_ratio <= REFRESH_DEGRADATION_LIMIT
    )

    final_snapshot = manager_snapshot(manager)
    checks["post_setup_zero_write_open_events"] = (
        write_open_counter["count"] == write_opens_baseline
    )

    checks["final_projection_stable"] = (
        projection_digest(final_snapshot) == initial_digest
    )

    return {
        "schema": SCHEMA,
        "version": VERSION,
        "diagnostic_protocol_sha256": PROTOCOL_SHA256,
        "diagnostic_correction_protocol_sha256": CORRECTION_PROTOCOL_SHA256,
        "diagnostic_v1_2_correction_protocol_sha256": V1_2_CORRECTION_PROTOCOL_SHA256,
        "diagnostic_v1_3_correction_protocol_sha256": V1_3_CORRECTION_PROTOCOL_SHA256,
        "diagnostic_runner_sha256": file_sha256(Path(__file__)),
        "resident_directory_engine_sha256": ENGINE_SHA256,
        "functional_validation_result_sha256": FUNCTIONAL_RESULT_SHA256,
        "benchmark_v1_1_result_sha256": BENCHMARK_RESULT_SHA256,
        "source_candidate_sha256": SOURCE_CANDIDATE_SHA256,
        "source_active_record_sha256": SOURCE_ACTIVE_SHA256,
        "lookup_signature": lookup_signature,
        "entry_count": len(snapshot.entries),
        "target_key": list(target_key),
        "initial_projection_digest": initial_digest,
        "failed_refresh_count": failed_refresh_count,
        "hot_lookup_open_events": opens_after - opens_before,
        "stale_state_stress": {
            "repeats": STALE_STATE_REPEATS,
            "stale_generation_pk": stale_generation_pk,
            "rejection_count": stale_rejection_count,
            "exception_types": sorted(stale_exception_types),
            "retained_growth_bytes": stale_retained_growth,
            "retained_limit_bytes": STALE_RETAINED_LIMIT_BYTES,
            "live_before": stale_live_before,
            "live_after": stale_live_after,
            "rss_before_bytes": stale_rss_before,
            "rss_after_bytes": stale_rss_after,
            "fd_before": stale_fd_before,
            "fd_after": stale_fd_after,
            "runtime_before": stale_runtime_before,
            "runtime_after": stale_runtime_after,
        },
        "build_stress": {
            "retained_growth_bytes": build_retained_growth,
            "retained_limit_bytes": BUILD_RETAINED_LIMIT_BYTES,
            "live_before": build_live_before,
            "live_after": build_live_after,
            "rss_before_bytes": build_rss_before,
            "rss_after_bytes": build_rss_after,
            "fd_before": build_fd_before,
            "fd_after": build_fd_after,
            "runtime_before": build_runtime_before,
            "runtime_after": build_runtime_after,
        },
        "failed_refresh_stress": {
            "retained_growth_bytes": failed_refresh_retained_growth,
            "retained_limit_bytes": FAILED_REFRESH_RETAINED_LIMIT_BYTES,
            "live_before": failed_live_before,
            "live_after": failed_live_after,
            "rss_before_bytes": failed_rss_before,
            "rss_after_bytes": failed_rss_after,
            "fd_before": failed_fd_before,
            "fd_after": failed_fd_after,
            "runtime_before": failed_runtime_before,
            "runtime_after": failed_runtime_after,
        },
        "post_setup_write_open_events": (
            write_open_counter["count"] - write_opens_baseline
        ),
        "memory": {
            "lookup_retained_growth_bytes": lookup_retained_growth,
            "lookup_retained_limit_bytes": LOOKUP_RETAINED_LIMIT_BYTES,
            "refresh_retained_growth_bytes": refresh_retained_growth,
            "refresh_retained_limit_bytes": REFRESH_RETAINED_LIMIT_BYTES,
            "live_snapshot_count_before": live_before,
            "live_snapshot_count_after": live_after,
            "live_snapshot_growth_limit": LIVE_SNAPSHOT_GROWTH_LIMIT,
        },
        "resources": {
            "rss_before_bytes": rss_before,
            "rss_after_bytes": rss_after,
            "rss_growth_bytes": rss_after - rss_before,
            "rss_growth_limit_bytes": RSS_GROWTH_LIMIT_BYTES,
            "fd_before": fd_before,
            "fd_after": fd_after,
            "fd_growth": fd_after - fd_before,
            "fd_growth_limit": FD_GROWTH_LIMIT,
            "runtime_before": runtime_before,
            "runtime_after": runtime_after,
        },
        "degradation": {
            "lookup_batches_ns_per_op": lookup_batches,
            "lookup_ratio": lookup_ratio,
            "lookup_ratio_limit": LOOKUP_DEGRADATION_LIMIT,
            "refresh_batches_ns_per_op": refresh_batches,
            "refresh_ratio": refresh_ratio,
            "refresh_ratio_limit": REFRESH_DEGRADATION_LIMIT,
            "build_batches_ns_per_op": build_batches,
            "build_ratio": build_ratio,
            "build_ratio_limit": BUILD_DEGRADATION_LIMIT,
            "hash_file_validation_ratio": build_ratio,
            "hash_file_validation_ratio_limit": BUILD_DEGRADATION_LIMIT,
        },
        "checks": checks,
        "all_pass": all(checks.values()),
        "fatal_error": None,
        "source_gguf_required": False,
        "inference_performed": False,
        "segment_reader_implemented": False,
        "storage_engine_selected": False,
        "maf_native_compute_enabled": False,
        "phase_6c_started": False,
        "production_guarantee_claimed": False,
    }


def fatal_result(exc):
    return {
        "schema": SCHEMA,
        "version": VERSION,
        "diagnostic_protocol_sha256": PROTOCOL_SHA256,
        "diagnostic_correction_protocol_sha256": CORRECTION_PROTOCOL_SHA256,
        "diagnostic_v1_2_correction_protocol_sha256": V1_2_CORRECTION_PROTOCOL_SHA256,
        "diagnostic_v1_3_correction_protocol_sha256": V1_3_CORRECTION_PROTOCOL_SHA256,
        "diagnostic_runner_sha256": file_sha256(Path(__file__)),
        "resident_directory_engine_sha256": ENGINE_SHA256,
        "functional_validation_result_sha256": FUNCTIONAL_RESULT_SHA256,
        "benchmark_v1_1_result_sha256": BENCHMARK_RESULT_SHA256,
        "source_candidate_sha256": SOURCE_CANDIDATE_SHA256,
        "source_active_record_sha256": SOURCE_ACTIVE_SHA256,
        "checks": {},
        "all_pass": False,
        "fatal_error": {
            "type": type(exc).__name__,
            "message": str(exc),
        },
        "source_gguf_required": False,
        "inference_performed": False,
        "segment_reader_implemented": False,
        "storage_engine_selected": False,
        "maf_native_compute_enabled": False,
        "phase_6c_started": False,
        "production_guarantee_claimed": False,
    }


def main():
    if RESULT.exists():
        raise SystemExit("diagnostic result already exists; exact-once execution refused")
    if RUNTIME.exists():
        raise SystemExit("diagnostic runtime already exists; exact-once execution refused")

    try:
        result = run_diagnostics()
    except Exception as exc:
        result = fatal_result(exc)

    write_json_exclusive(RESULT, result)

    print("=" * 72)
    print(" OPENMIND / RESIDENT PK DIRECTORY DIAGNOSTICS V1.3")
    print("=" * 72)
    print("all_pass:", result["all_pass"])
    print("fatal_error:", result["fatal_error"])

    if result["all_pass"]:
        raise SystemExit(0)
    raise SystemExit(1)


if __name__ == "__main__":
    main()
