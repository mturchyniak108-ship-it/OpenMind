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

SCHEMA = "openmind.maf_resident_pk_directory_diagnostics.v1"
VERSION = "maf_resident_pk_directory_diagnostics_v1"

PROTOCOL = Path("experiments/model_fractal/MAF_RESIDENT_PK_DIRECTORY_DIAGNOSTICS_V1_PROTOCOL.md")
PROTOCOL_SHA256 = "5101e4a4dd78b869eb91ce226a1a304181bc2c3636d2ff86a056db15caf0560a"

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

RESULT = Path("experiments/model_fractal/maf_resident_pk_directory_diagnostics_v1.json")
RUNTIME = Path("results/runtime/maf_resident_pk_directory_diagnostics_v1")

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
LIVE_SNAPSHOT_GROWTH_LIMIT = 2
RSS_GROWTH_LIMIT_BYTES = 16 * 1024 * 1024
FD_GROWTH_LIMIT = 2
LOOKUP_DEGRADATION_LIMIT = 2.0
REFRESH_DEGRADATION_LIMIT = 2.5


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


def call_lookup(snapshot, key):
    values = {
        "model_pk": snapshot.model_pk,
        "pk_kind": key[1],
        "pk_class": key[1],
        "logical_pk": key[2],
        "object_pk": key[2],
        "expected_generation_pk": snapshot.generation_pk,
    }
    sig = inspect.signature(snapshot.lookup)
    kwargs = {}
    for name, param in sig.parameters.items():
        if name in values:
            kwargs[name] = values[name]
            continue
        if param.default is inspect.Parameter.empty:
            raise RuntimeError("unsupported required lookup parameter: " + name)
    return snapshot.lookup(**kwargs)


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
    initial_digest = projection_digest(snapshot)

    lookup_signature = str(inspect.signature(snapshot.lookup))

    checks = {}

    checks["initial_snapshot_nonempty"] = len(snapshot.entries) > 0
    checks["initial_lookup_exact"] = call_lookup(snapshot, target_key) is expected_entry

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

    manager = resident.ResidentPKDirectory()
    first_refresh = refresh_from_prepared(manager, prepared)
    checks["successful_refresh_published_returned_snapshot"] = (
        manager_snapshot(manager) is first_refresh
    )

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

    checks["all_invalid_refreshes_failed"] = (
        failed_refresh_count == FAILED_REFRESH_REPEATS
    )
    checks["invalid_refresh_preserved_prior_snapshot"] = failed_refresh_preserved

    hot_open_counter = {"count": 0}

    def audit_hook(event, args):
        if event == "open":
            hot_open_counter["count"] += 1

    sys.addaudithook(audit_hook)
    opens_before = hot_open_counter["count"]

    hot_lookup_exact = True
    for _ in range(HOT_LOOKUP_REPEATS):
        if call_lookup(snapshot, target_key) is not expected_entry:
            hot_lookup_exact = False
            break

    opens_after = hot_open_counter["count"]

    checks["hot_lookup_exact_repeated"] = hot_lookup_exact
    checks["hot_lookup_zero_open_events"] = opens_after == opens_before

    for _ in range(5000):
        call_lookup(snapshot, target_key)
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
        call_lookup(snapshot, target_key)

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

    lookup_operation = lambda: call_lookup(snapshot, target_key)

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
    checks["refresh_degradation_within_limit"] = (
        refresh_ratio <= REFRESH_DEGRADATION_LIMIT
    )

    final_snapshot = manager_snapshot(manager)
    checks["final_projection_stable"] = (
        projection_digest(final_snapshot) == initial_digest
    )

    return {
        "schema": SCHEMA,
        "version": VERSION,
        "diagnostic_protocol_sha256": PROTOCOL_SHA256,
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
    print(" OPENMIND / RESIDENT PK DIRECTORY DIAGNOSTICS V1")
    print("=" * 72)
    print("all_pass:", result["all_pass"])
    print("fatal_error:", result["fatal_error"])

    if result["all_pass"]:
        raise SystemExit(0)
    raise SystemExit(1)


if __name__ == "__main__":
    main()
