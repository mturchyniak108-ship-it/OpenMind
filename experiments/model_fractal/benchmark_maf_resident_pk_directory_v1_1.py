#!/usr/bin/env python3

import gc
import hashlib
import json
import platform
import shutil
import statistics
import sys
import time
import tracemalloc
from pathlib import Path
from types import MappingProxyType

import maf_activation_v1_1 as activation
import maf_resident_pk_directory_v1 as directory

BENCHMARK_SCHEMA = "openmind.maf_resident_pk_directory_benchmark.v1_1"
BENCHMARK_VERSION = "maf_resident_pk_directory_benchmark_v1_1"

BENCHMARK_PROTOCOL = Path("experiments/model_fractal/MAF_RESIDENT_PK_DIRECTORY_BENCHMARK_V1_PROTOCOL.md")
BENCHMARK_PROTOCOL_SHA256 = "496a19e5f2f2a9cebbb74aaf204b96e28916c0aa0276fb85dfb8401e55e2266f"

CORRECTION_PROTOCOL = Path("experiments/model_fractal/MAF_RESIDENT_PK_DIRECTORY_BENCHMARK_V1_1_CORRECTION_PROTOCOL.md")
CORRECTION_PROTOCOL_SHA256 = "d35aca6c8c98d891761f6fbfb176e3b7fc385d466d03e07ae3125892015b61ef"

ENGINE = Path("experiments/model_fractal/maf_resident_pk_directory_v1.py")
ENGINE_SHA256 = "4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6"

FUNCTIONAL_RESULT = Path("experiments/model_fractal/maf_resident_pk_directory_validation_v1.json")
FUNCTIONAL_RESULT_SHA256 = "24540c16eac53e9a179781c7007d61d98b34f7bc74e1f3dfc462b5786dd186b1"

SOURCE_RUNTIME = Path("results/runtime/maf_activation_validation_v1_1_1")
SOURCE_CANDIDATE = SOURCE_RUNTIME / "candidate_a.manifest.json"
SOURCE_CANDIDATE_SHA256 = "941301aa362d3f949389e5364b1be4d7f26b96f0d45efa81346c82fce3260f93"

RESULT = Path("experiments/model_fractal/benchmark_maf_resident_pk_directory_v1_1.json")
RUNTIME = Path("results/runtime/maf_resident_pk_directory_benchmark_v1_1")

SIZES = (100, 1000, 10000, 100000)
REPEATS = {
    100: 2000,
    1000: 1000,
    10000: 250,
    100000: 50,
}

BUILD_WARMUPS = 2
BUILD_REPEATS = 10
LOOKUP_WARMUPS = 20

SYNTH_MODEL = "mafmodel:benchmark:v1"
SYNTH_GENERATION = "mafgen:benchmark:v1"
SYNTH_MANIFEST_SHA = "1" * 64
SYNTH_ACTIVE_SHA = "2" * 64


def file_sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def read_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json_exclusive(path, value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n"
    with path.open("x", encoding="utf-8") as f:
        f.write(data)


def percentile(values, fraction):
    ordered = sorted(values)
    if not ordered:
        raise RuntimeError("empty timing distribution")
    index = int(round((len(ordered) - 1) * fraction))
    return ordered[index]


def assert_frozen_inputs():
    checks = {
        "benchmark_protocol_sha256_exact": file_sha256(BENCHMARK_PROTOCOL) == BENCHMARK_PROTOCOL_SHA256,
        "correction_protocol_sha256_exact": file_sha256(CORRECTION_PROTOCOL) == CORRECTION_PROTOCOL_SHA256,
        "engine_sha256_exact": file_sha256(ENGINE) == ENGINE_SHA256,
        "functional_result_sha256_exact": file_sha256(FUNCTIONAL_RESULT) == FUNCTIONAL_RESULT_SHA256,
        "source_candidate_sha256_exact": file_sha256(SOURCE_CANDIDATE) == SOURCE_CANDIDATE_SHA256,
    }
    functional = read_json(FUNCTIONAL_RESULT)
    checks["functional_result_all_pass"] = functional.get("all_pass") is True
    checks["functional_result_benchmark_absent"] = functional.get("benchmark_performed") is False
    failed = [key for key, value in checks.items() if value is not True]
    if failed:
        raise RuntimeError("frozen input check failed: " + repr(failed))
    return checks


def locate_source_segment(expected_sha, expected_length):
    candidates = []
    for path in sorted(SOURCE_RUNTIME.rglob("*")):
        if not path.is_file():
            continue
        try:
            if path.stat().st_size != expected_length:
                continue
        except OSError:
            continue
        if file_sha256(path) == expected_sha:
            candidates.append(path)
    if not candidates:
        raise RuntimeError("retained source segment not found")
    return candidates[0]


def prepare_actual_runtime():
    RUNTIME.mkdir(parents=True, exist_ok=False)
    candidate_copy = RUNTIME / "candidate_a.manifest.json"
    shutil.copyfile(SOURCE_CANDIDATE, candidate_copy)
    if file_sha256(candidate_copy) != SOURCE_CANDIDATE_SHA256:
        raise RuntimeError("candidate copy identity mismatch")
    manifest = read_json(candidate_copy)
    descriptor = manifest["descriptor"]
    segment_paths = {}
    for segment in descriptor["segments"]:
        source = locate_source_segment(
            segment["segment_sha256"],
            int(segment["segment_length"]),
        )
        safe = segment["segment_id"].replace(":", "_").replace("/", "_")
        target = RUNTIME / (safe + ".mafseg")
        shutil.copyfile(source, target)
        if file_sha256(target) != segment["segment_sha256"]:
            raise RuntimeError("copied segment identity mismatch")
        segment_paths[segment["segment_id"]] = target
    active_record = RUNTIME / "active_generation.json"
    activation.activate_generation(
        model_pk=descriptor["model_pk"],
        generation_pk=manifest["generation_pk"],
        candidate_manifest_path=candidate_copy,
        active_record_path=active_record,
        segment_paths=segment_paths,
    )
    return descriptor, manifest, candidate_copy, active_record, segment_paths


def synthetic_snapshot(size):
    entries = {}
    target_pk = None
    for index in range(size):
        object_pk = "mafobj:benchmark:" + str(index).zfill(12)
        target_pk = object_pk
        key = (SYNTH_MODEL, directory.OBJECT_PK_KIND, object_pk)
        entries[key] = directory.ResidentPKEntry(
            model_pk=SYNTH_MODEL,
            generation_pk=SYNTH_GENERATION,
            generation_manifest_sha256=SYNTH_MANIFEST_SHA,
            object_pk=object_pk,
            segment_id="segment:" + str(index // 1000).zfill(8),
            offset=index * 64,
            length=64,
            object_file_sha256="3" * 64,
            payload_sha256="4" * 64,
            segment_length=65536,
            segment_sha256="5" * 64,
            segment_path="/benchmark/segment",
        )
    snapshot = directory.ResidentPKSnapshot(
        model_pk=SYNTH_MODEL,
        generation_pk=SYNTH_GENERATION,
        generation_manifest_sha256=SYNTH_MANIFEST_SHA,
        active_record_sha256=SYNTH_ACTIVE_SHA,
        entries=MappingProxyType(entries),
    )
    return snapshot, target_pk


def linear_lookup(snapshot, model_pk, pk_kind, logical_pk, expected_generation_pk):
    if model_pk != snapshot.model_pk:
        raise directory.MAFResidentPKDirectoryCrossModelError("benchmark cross-model")
    if expected_generation_pk != snapshot.generation_pk:
        raise directory.MAFResidentPKDirectoryStaleSnapshotError("benchmark stale generation")
    if pk_kind != directory.OBJECT_PK_KIND:
        raise directory.MAFResidentPKDirectoryUnsupportedPKError("benchmark unsupported pk")
    wanted = (model_pk, pk_kind, logical_pk)
    for key, entry in snapshot.entries.items():
        if key == wanted:
            return entry
    raise directory.MAFResidentPKDirectoryNotFoundError("benchmark key absent")


def measure_lookup_scaling():
    rows = []
    for size in SIZES:
        repeats = REPEATS[size]
        snapshot, target_pk = synthetic_snapshot(size)
        for _ in range(min(LOOKUP_WARMUPS, repeats)):
            snapshot.lookup(
                model_pk=SYNTH_MODEL,
                pk_kind=directory.OBJECT_PK_KIND,
                logical_pk=target_pk,
                expected_generation_pk=SYNTH_GENERATION,
            )
            linear_lookup(
                snapshot,
                SYNTH_MODEL,
                directory.OBJECT_PK_KIND,
                target_pk,
                SYNTH_GENERATION,
            )
        direct_ns = []
        linear_ns = []
        direct_exact = True
        for _ in range(repeats):
            start = time.perf_counter_ns()
            entry = snapshot.lookup(
                model_pk=SYNTH_MODEL,
                pk_kind=directory.OBJECT_PK_KIND,
                logical_pk=target_pk,
                expected_generation_pk=SYNTH_GENERATION,
            )
            direct_ns.append(time.perf_counter_ns() - start)
            direct_exact = direct_exact and entry.object_pk == target_pk
        for _ in range(repeats):
            start = time.perf_counter_ns()
            entry = linear_lookup(
                snapshot,
                SYNTH_MODEL,
                directory.OBJECT_PK_KIND,
                target_pk,
                SYNTH_GENERATION,
            )
            linear_ns.append(time.perf_counter_ns() - start)
            direct_exact = direct_exact and entry.object_pk == target_pk
        rows.append({
            "size": size,
            "repeats": repeats,
            "direct_exact": direct_exact,
            "direct_median_ns": int(statistics.median(direct_ns)),
            "direct_p95_ns": int(percentile(direct_ns, 0.95)),
            "linear_median_ns": int(statistics.median(linear_ns)),
            "linear_p95_ns": int(percentile(linear_ns, 0.95)),
        })
        del snapshot
        gc.collect()
    return rows


def measure_memory_scaling():
    rows = []
    for size in SIZES:
        gc.collect()
        tracemalloc.start()
        before, _ = tracemalloc.get_traced_memory()
        snapshot, target_pk = synthetic_snapshot(size)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        current_delta = max(0, current - before)
        peak_delta = max(0, peak - before)
        rows.append({
            "size": size,
            "current_allocated_bytes": current_delta,
            "peak_allocated_bytes": peak_delta,
            "peak_bytes_per_entry": peak_delta / size,
            "target_pk": target_pk,
        })
        del snapshot
        gc.collect()
    return rows


def measure_actual_build_refresh():
    descriptor, manifest, candidate, active_record, segment_paths = prepare_actual_runtime()
    model_pk = descriptor["model_pk"]
    generation_pk = manifest["generation_pk"]
    for _ in range(BUILD_WARMUPS):
        directory.build_snapshot(
            model_pk=model_pk,
            active_record_path=active_record,
            active_candidate_manifest_path=candidate,
            active_segment_paths=segment_paths,
        )
    build_ns = []
    build_counts = []
    for _ in range(BUILD_REPEATS):
        start = time.perf_counter_ns()
        snapshot = directory.build_snapshot(
            model_pk=model_pk,
            active_record_path=active_record,
            active_candidate_manifest_path=candidate,
            active_segment_paths=segment_paths,
        )
        build_ns.append(time.perf_counter_ns() - start)
        build_counts.append(snapshot.entry_count)
    manager = directory.ResidentPKDirectory()
    for _ in range(BUILD_WARMUPS):
        manager.refresh(
            model_pk=model_pk,
            active_record_path=active_record,
            active_candidate_manifest_path=candidate,
            active_segment_paths=segment_paths,
        )
    refresh_ns = []
    refresh_counts = []
    for _ in range(BUILD_REPEATS):
        start = time.perf_counter_ns()
        snapshot = manager.refresh(
            model_pk=model_pk,
            active_record_path=active_record,
            active_candidate_manifest_path=candidate,
            active_segment_paths=segment_paths,
        )
        refresh_ns.append(time.perf_counter_ns() - start)
        refresh_counts.append(snapshot.entry_count)
    return {
        "warmups": BUILD_WARMUPS,
        "repeats": BUILD_REPEATS,
        "entry_count": build_counts[0],
        "build_counts": build_counts,
        "refresh_counts": refresh_counts,
        "build_median_ns": int(statistics.median(build_ns)),
        "build_p95_ns": int(percentile(build_ns, 0.95)),
        "refresh_median_ns": int(statistics.median(refresh_ns)),
        "refresh_p95_ns": int(percentile(refresh_ns, 0.95)),
    }


def evaluate(lookup_rows, memory_rows, actual):
    scaling_rows = [row for row in lookup_rows if row["size"] >= 1000]
    direct_medians = [row["direct_median_ns"] for row in scaling_rows]
    direct_p95 = [row["direct_p95_ns"] for row in scaling_rows]
    by_size = {row["size"]: row for row in lookup_rows}
    median_ratio = max(direct_medians) / min(direct_medians)
    p95_ratio = max(direct_p95) / min(direct_p95)
    linear_growth = by_size[100000]["linear_median_ns"] / by_size[1000]["linear_median_ns"]
    checks = {
        "all_direct_results_exact": all(row["direct_exact"] for row in lookup_rows),
        "all_lookup_sizes_complete": all(row["repeats"] == REPEATS[row["size"]] for row in lookup_rows),
        "direct_median_scaling_ratio_le_4": median_ratio <= 4.0,
        "direct_p95_scaling_ratio_le_6": p95_ratio <= 6.0,
        "linear_median_growth_ge_20": linear_growth >= 20.0,
        "direct_faster_than_linear_at_100000": by_size[100000]["direct_median_ns"] < by_size[100000]["linear_median_ns"],
        "actual_build_repeats_complete": len(actual["build_counts"]) == BUILD_REPEATS,
        "actual_refresh_repeats_complete": len(actual["refresh_counts"]) == BUILD_REPEATS,
        "actual_build_counts_consistent": len(set(actual["build_counts"])) == 1,
        "actual_refresh_counts_consistent": len(set(actual["refresh_counts"])) == 1,
        "memory_measurements_complete": len(memory_rows) == len(SIZES),
        "memory_peaks_positive": all(row["peak_allocated_bytes"] > 0 for row in memory_rows),
    }
    return {
        "checks": checks,
        "direct_median_scaling_ratio": median_ratio,
        "direct_p95_scaling_ratio": p95_ratio,
        "linear_median_growth_ratio_100000_vs_1000": linear_growth,
        "pass": all(checks.values()),
    }


def run_benchmark():
    frozen = assert_frozen_inputs()
    lookup_rows = measure_lookup_scaling()
    memory_rows = measure_memory_scaling()
    actual = measure_actual_build_refresh()
    acceptance = evaluate(lookup_rows, memory_rows, actual)
    return {
        "schema": BENCHMARK_SCHEMA,
        "benchmark_version": BENCHMARK_VERSION,
        "benchmark_protocol_sha256": BENCHMARK_PROTOCOL_SHA256,
        "benchmark_runner_sha256": file_sha256(Path(__file__)),
        "resident_directory_engine_sha256": ENGINE_SHA256,
        "functional_validation_result_sha256": FUNCTIONAL_RESULT_SHA256,
        "frozen_input_checks": frozen,
        "python_version": sys.version,
        "platform": platform.platform(),
        "sizes": list(SIZES),
        "repeats": {str(key): value for key, value in REPEATS.items()},
        "lookup": lookup_rows,
        "memory": memory_rows,
        "actual_build_refresh": actual,
        "acceptance": acceptance,
        "all_pass": acceptance["pass"],
        "benchmark_performed": True,
        "production_performance_claimed": False,
        "source_gguf_required": False,
        "generation_deleted": False,
        "storage_engine_selected": False,
        "segment_reader_implemented": False,
        "inference_performed": False,
        "maf_native_compute_enabled": False,
        "phase_6c_started": False,
    }


def main():
    if RESULT.exists():
        raise RuntimeError("refusing rerun: benchmark result already exists")
    if RUNTIME.exists():
        raise RuntimeError("refusing rerun: benchmark runtime already exists")
    result = run_benchmark()
    write_json_exclusive(RESULT, result)
    print("=" * 72)
    print(" OPENMIND / RESIDENT PK DIRECTORY BENCHMARK V1.1")
    print("=" * 72)
    print("all_pass:", result["all_pass"])
    print("direct_median_scaling_ratio:", result["acceptance"]["direct_median_scaling_ratio"])
    print("direct_p95_scaling_ratio:", result["acceptance"]["direct_p95_scaling_ratio"])
    print("linear_growth:", result["acceptance"]["linear_median_growth_ratio_100000_vs_1000"])
    print("result:", RESULT)
    print("runtime:", RUNTIME)


if __name__ == "__main__":
    main()
