#!/usr/bin/env python3
"""MAF Segment Reader Benchmark V1.1 exact-once runner.

Implements the frozen V1.1 preregistration. The frozen V1 benchmark module is
loaded only for resolve_entries() and the three measurement-mode functions.
CPU/thermal helper behavior is reused from the exact frozen CPU Thermal
Characterization V1.2 runner bound by its completion record.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
import statistics
import time
from pathlib import Path
from typing import Any


SCHEMA = "openmind.maf_segment_reader_benchmark.v1_1"

PROTOCOL = Path("experiments/model_fractal/MAF_SEGMENT_READER_BENCHMARK_V1_1_PROTOCOL.md")
V1_CORE = Path("experiments/model_fractal/benchmark_maf_segment_reader_v1.py")
THERMAL_COMPLETION = Path("experiments/model_fractal/CPU_THERMAL_CHARACTERIZATION_V1_2_COMPLETION.md")
THERMAL_RAW = Path("experiments/model_fractal/cpu_thermal_characterization_v1_2.json")
THERMAL_PROTOCOL = Path("experiments/model_fractal/CPU_THERMAL_CHARACTERIZATION_V1_2_PROTOCOL.md")
THERMAL_RUNNER = Path("experiments/model_fractal/cpu_thermal_characterization_v1_2.py")
READER = Path("experiments/model_fractal/maf_segment_reader_v1.py")
RESIDENT = Path("experiments/model_fractal/maf_resident_pk_directory_v1.py")
VALIDATION_RESULT = Path("experiments/model_fractal/maf_segment_reader_validation_v1.json")
RESULT = Path("experiments/model_fractal/maf_segment_reader_benchmark_v1_1.json")
SOURCE_RUNTIME = Path("results/runtime/maf_resident_pk_directory_benchmark_v1_1")
SOURCE_MANIFEST = SOURCE_RUNTIME / "candidate_a.manifest.json"

EXPECTED = {
    "protocol": "8a6af3a65c78c0ed9f47244ebd40613c5e84f13fc2e4e2d1543089e5481e3770",
    "v1_core": "2972beda0d1a798cf5da9bf6371f5c0c96ee493ce6903da68021cec64e7947d4",
    "thermal_completion": "3b89868f324b774c9107faa6b038c8a8573d509c0d93527d960922cda6ae62dd",
    "thermal_raw": "b2e587547ed2b7388f141210fb3de5873de7a9d61b1ca3273ec4e4a964eaa8b2",
    "thermal_protocol": "b98e4c4d7309948b0fbf71f4a961e038a7e55470f03153e85ec724ffd32f3cbb",
    "thermal_runner": "19218eaf8fe98a6bcbf6f465f9f0d5320d8fb42f6b3937bbfcc5b4a29a78c2f2",
    "reader": "3499cb8e528fe8e9315e3e5656d6aa888c95ca175310b6371e722de409827369",
    "resident": "4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6",
    "validation_result": "1ceef1ed2b814da3951811ea97e9f4475b3fa79557b341e7c8e089ec8a409328",
}

EXPECTED_CLUSTERS = {"0": [0, 1, 2, 3, 4, 5], "1": [6, 7]}
NORMAL_CPUS = (0, 3)
MICRO_CPUS = (6, 7)
NORMAL_MODES = ("reader_v1", "direct_nohash_reference", "whole_segment_hash_reference")
MICRO_MODES = ("reader_v1", "direct_nohash_reference")

# Frozen V1 measurement counts retained by V1.1 while its scheduler/governance changes.
WARMUP = 100
REPEATS = 1000

NORMAL_ACTIVE_LIMIT_NS = 250_000_000
OBSERVATION_GAP_NS = 100_000_000
INITIAL_MAX_TEMP_MC = 75_000
OPTIMAL_RISE_MC = 5_000
OPTIMAL_ABSOLUTE_MC = 75_000
HARD_RISE_MC = 8_000
HARD_ABSOLUTE_MC = 80_000
RESUME_RISE_MC = 3_000
RESUME_ABSOLUTE_MC = 70_000


def exc_record(exc: BaseException | None) -> dict[str, str] | None:
    if exc is None:
        return None
    return {"type": type(exc).__name__, "message": str(exc)}


class BenchmarkExecutionError(RuntimeError):
    def __init__(self, execution_error, affinity_restore_error, partial_evidence):
        self.execution_error = exc_record(execution_error)
        self.affinity_restore_error = exc_record(affinity_restore_error)
        self.partial_evidence = partial_evidence
        parts = []
        if execution_error is not None:
            parts.append(f"execution: {type(execution_error).__name__}: {execution_error}")
        if affinity_restore_error is not None:
            parts.append(
                f"affinity restore: {type(affinity_restore_error).__name__}: "
                f"{affinity_restore_error}"
            )
        super().__init__(" | ".join(parts) or "benchmark execution failed")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json_exclusive(path: Path, data: dict[str, Any]) -> None:
    with path.open("x", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module spec: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_frozen_identities() -> dict[str, Any]:
    bound = {
        "protocol": PROTOCOL,
        "v1_core": V1_CORE,
        "thermal_completion": THERMAL_COMPLETION,
        "thermal_raw": THERMAL_RAW,
        "thermal_protocol": THERMAL_PROTOCOL,
        "thermal_runner": THERMAL_RUNNER,
        "reader": READER,
        "resident": RESIDENT,
        "validation_result": VALIDATION_RESULT,
    }
    observed = {}
    checks = {}

    for name, path in bound.items():
        actual = sha256_file(path)
        observed[name] = {
            "path": str(path),
            "expected_sha256": EXPECTED[name],
            "observed_sha256": actual,
        }
        checks[f"{name}_identity"] = actual == EXPECTED[name]

    completion = THERMAL_COMPLETION.read_text(encoding="utf-8")
    checks.update(
        {
            "completion_status_exact":
                "Status: COMPLETE / RAW RESULT FROZEN / DO NOT RERUN" in completion,
            "completion_binds_protocol": EXPECTED["thermal_protocol"] in completion,
            "completion_binds_runner": EXPECTED["thermal_runner"] in completion,
            "completion_binds_raw": EXPECTED["thermal_raw"] in completion,
        }
    )

    thermal_raw = json.loads(THERMAL_RAW.read_text(encoding="utf-8"))
    checks.update(
        {
            "thermal_schema_exact":
                thermal_raw.get("schema") == "openmind.cpu_thermal_characterization.v1_2",
            "thermal_protocol_exact":
                thermal_raw.get("protocol_sha256") == EXPECTED["thermal_protocol"],
            "thermal_result_valid": thermal_raw.get("characterization_valid") is True,
            "thermal_fatal_error_absent": thermal_raw.get("fatal_error") is None,
        }
    )

    failed = [name for name, value in checks.items() if value is not True]
    if failed:
        raise RuntimeError("frozen identity preflight failed: " + ",".join(sorted(failed)))

    return {"identities": observed, "checks": checks}


def load_frozen_dependencies() -> tuple[Any, Any]:
    """Load only after exact identity checks and result-absence gate."""
    v1 = load_module(V1_CORE, "_openmind_frozen_segment_reader_benchmark_v1")
    thermal = load_module(THERMAL_RUNNER, "_openmind_frozen_cpu_thermal_v1_2")

    allowed_v1 = (
        "resolve_entries",
        "reader_v1",
        "direct_nohash_reference",
        "whole_segment_hash_reference",
    )
    for name in allowed_v1:
        if not callable(getattr(v1, name, None)):
            raise RuntimeError(f"frozen V1 core missing callable: {name}")

    return v1, thermal


def fixture_id(fixture: dict[str, Any]) -> str:
    return fixture["entry"].object_pk


def fixture_json(fixture: dict[str, Any]) -> dict[str, Any]:
    entry = fixture["entry"]
    runtime_state["current_workload_unit"] = None
    return {
        "fixture_id": fixture_id(fixture),
        "object_pk": entry.object_pk,
        "segment_id": entry.segment_id,
        "offset": entry.offset,
        "object_serialized_length": entry.length,
        "segment_length": entry.segment_length,
        "object_file_sha256": entry.object_file_sha256,
        "payload_sha256": entry.payload_sha256,
        "segment_sha256": entry.segment_sha256,
        "segment_path": entry.segment_path,
    }


def select_micro_fixtures(fixtures: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(fixtures, key=lambda item: (item["entry"].length, fixture_id(item)))
    if not ordered:
        return []
    return ordered[: min(8, math.ceil(len(ordered) / 2))]


def call_mode(v1: Any, mode: str, fixture: dict[str, Any], generation_pk: str) -> Any:
    entry = fixture["entry"]
    if mode == "reader_v1":
        return v1.reader_v1(entry, generation_pk)
    if mode == "direct_nohash_reference":
        return v1.direct_nohash_reference(entry)
    if mode == "whole_segment_hash_reference":
        return v1.whole_segment_hash_reference(entry)
    raise RuntimeError(f"unknown mode: {mode}")


def returned_bytes(value: Any) -> int:
    if isinstance(value, str):
        return len(value.encode("utf-8"))
    if isinstance(value, (bytes, bytearray, memoryview)):
        return len(value)
    return 0


def processed_bytes(mode: str, fixture: dict[str, Any]) -> int:
    if mode == "whole_segment_hash_reference":
        return fixture["entry"].segment_length
    return fixture["entry"].length


def limits_for_cpu(
    cpu: int,
    snapshot: dict[str, Any],
    baselines: dict[str, Any],
) -> dict[str, int]:
    key = str(cpu)
    if key not in baselines:
        baseline = snapshot["max_temp_mc"]
        baselines[key] = {
            "cpu": cpu,
            "thermal": snapshot,
            "baseline_mc": baseline,
            "optimal_limit_mc": min(baseline + OPTIMAL_RISE_MC, OPTIMAL_ABSOLUTE_MC),
            "hard_limit_mc": min(baseline + HARD_RISE_MC, HARD_ABSOLUTE_MC),
        }
    row = baselines[key]
    return {
        "baseline_mc": row["baseline_mc"],
        "optimal_limit_mc": row["optimal_limit_mc"],
        "hard_limit_mc": row["hard_limit_mc"],
    }


def record_pin(
    thermal: Any,
    target_cpu: int,
    current_cpu: int | None,
    topology: dict[int, dict[str, Any]],
    transitions: list[dict[str, Any]],
    kind: str,
) -> int:
    before = sorted(os.sched_getaffinity(0))
    thermal.pin_cpu(target_cpu)
    after = sorted(os.sched_getaffinity(0))
    transitions.append(
        {
            "sequence": len(transitions),
            "kind": kind,
            "from_cpu": current_cpu,
            "to_cpu": target_cpu,
            "from_cluster":
                topology[current_cpu]["cluster_id"] if current_cpu is not None else None,
            "to_cluster": topology[target_cpu]["cluster_id"],
            "cross_cluster":
                None
                if current_cpu is None
                else topology[current_cpu]["cluster_id"]
                != topology[target_cpu]["cluster_id"],
            "affinity_before": before,
            "affinity_after": after,
            "monotonic_ns": time.monotonic_ns(),
        }
    )
    return target_cpu


def cooldown(
    thermal: Any,
    zones: list[dict[str, str]],
    resume_limit_mc: int,
    context: dict[str, Any],
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    start = time.monotonic()
    observations = []
    before = thermal.thermal_snapshot(zones)
    observations.append({"elapsed_seconds": 0.0, "thermal": before})

    while before["max_temp_mc"] > resume_limit_mc:
        elapsed = time.monotonic() - start
        if elapsed >= thermal.MAX_COOLDOWN_SECONDS:
            record = {
                "context": context,
                "resume_limit_mc": resume_limit_mc,
                "wait_seconds": elapsed,
                "before": observations[0]["thermal"],
                "after": before,
                "observations": observations,
                "completed": False,
            }
            records.append(record)
            raise RuntimeError("thermal cooldown timeout")

        time.sleep(thermal.COOLDOWN_POLL_SECONDS)
        before = thermal.thermal_snapshot(zones)
        observations.append(
            {"elapsed_seconds": time.monotonic() - start, "thermal": before}
        )

    elapsed = time.monotonic() - start
    record = {
        "context": context,
        "resume_limit_mc": resume_limit_mc,
        "wait_seconds": elapsed,
        "before": observations[0]["thermal"],
        "after": before,
        "observations": observations,
        "completed": True,
    }
    records.append(record)
    return record


def source_fingerprint() -> str:
    digest = hashlib.sha256()
    paths = [SOURCE_MANIFEST, *sorted(SOURCE_RUNTIME.rglob("*.mafseg"))]
    for path in paths:
        raw = path.read_bytes()
        rel = str(path).encode("utf-8")
        digest.update(len(rel).to_bytes(8, "big"))
        digest.update(rel)
        digest.update(len(raw).to_bytes(8, "big"))
        digest.update(hashlib.sha256(raw).digest())
    return digest.hexdigest()


def fd_count() -> int | None:
    root = Path("/proc/self/fd")
    if not root.is_dir():
        return None
    try:
        return len(list(root.iterdir()))
    except OSError:
        return None


def measured_operation(
    v1: Any,
    thermal: Any,
    *,
    lane: str,
    cpu: int,
    cluster: str,
    fixture: dict[str, Any],
    mode: str,
    generation_pk: str,
    zones: list[dict[str, str]],
    baselines: dict[str, Any],
    observations: list[dict[str, Any]],
    runtime_state: dict[str, Any],
    sequence: int,
) -> dict[str, Any]:
    before = thermal.thermal_snapshot(zones)
    freq_before = thermal.frequency_snapshot(cpu)
    limits = limits_for_cpu(cpu, before, baselines)

    observations.append(
        {
            "sequence": len(observations),
            "context": "operation_before",
            "lane": lane,
            "cpu": cpu,
            "fixture_id": fixture_id(fixture),
            "mode": mode,
            "thermal": before,
            "frequency": freq_before,
        }
    )

    runtime_state["current_workload_unit"] = {
        "kind": "measured",
        "lane": lane,
        "cpu": cpu,
        "cluster": cluster,
        "fixture_id": fixture_id(fixture),
        "mode": mode,
        "sample_sequence": sequence,
    }
    start = time.perf_counter_ns()
    value = call_mode(v1, mode, fixture, generation_pk)
    end = time.perf_counter_ns()

    if value != fixture["expected"]:
        raise RuntimeError("measured operation returned incorrect bytes")

    latency = end - start
    if latency <= 0:
        raise RuntimeError("nonpositive measured latency")

    after = thermal.thermal_snapshot(zones)
    freq_after = thermal.frequency_snapshot(cpu)
    observations.append(
        {
            "sequence": len(observations),
            "context": "operation_after",
            "lane": lane,
            "cpu": cpu,
            "fixture_id": fixture_id(fixture),
            "mode": mode,
            "thermal": after,
            "frequency": freq_after,
        }
    )

    returned = returned_bytes(value)
    processed = processed_bytes(mode, fixture)
    hard_stop = after["max_temp_mc"] >= limits["hard_limit_mc"]
    gap_violation = latency > OBSERVATION_GAP_NS
    eligible = (
        before["max_temp_mc"] <= limits["optimal_limit_mc"]
        and after["max_temp_mc"] <= limits["optimal_limit_mc"]
        and not hard_stop
    )

    ops = 1_000_000_000.0 / latency
    ret_bps = returned * 1_000_000_000.0 / latency
    proc_bps = processed * 1_000_000_000.0 / latency

    entry = fixture["entry"]
    return {
        "sequence": sequence,
        "lane": lane,
        "cpu": cpu,
        "cluster": cluster,
        "fixture_id": fixture_id(fixture),
        "object_pk": entry.object_pk,
        "object_serialized_length": entry.length,
        "segment_length": entry.segment_length,
        "mode": mode,
        "latency_ns": latency,
        "returned_bytes": returned,
        "processed_bytes": processed,
        "operations_per_second": ops,
        "returned_bytes_per_second": ret_bps,
        "returned_mib_per_second": ret_bps / 1_048_576.0,
        "processed_bytes_per_second": proc_bps,
        "processed_mib_per_second": proc_bps / 1_048_576.0,
        "thermal_before": before,
        "thermal_after": after,
        "governing_temperature_before_mc": before["max_temp_mc"],
        "governing_temperature_after_mc": after["max_temp_mc"],
        "cpu_frequency_before": freq_before,
        "cpu_frequency_after": freq_after,
        "cpu_baseline_mc": limits["baseline_mc"],
        "optimal_limit_mc": limits["optimal_limit_mc"],
        "hard_limit_mc": limits["hard_limit_mc"],
        "thermal_eligibility": eligible,
        "hard_stop": hard_stop,
        "observation_gap_violation": gap_violation,
    }


def warmup_operation(
    v1: Any,
    thermal: Any,
    *,
    cpu: int,
    fixture: dict[str, Any],
    mode: str,
    generation_pk: str,
    zones: list[dict[str, str]],
    baselines: dict[str, Any],
    runtime_state: dict[str, Any],
) -> None:
    runtime_state["current_workload_unit"] = {
        "kind": "warmup",
        "cpu": cpu,
        "fixture_id": fixture_id(fixture),
        "mode": mode,
    }
    before = thermal.thermal_snapshot(zones)
    limits = limits_for_cpu(cpu, before, baselines)
    value = call_mode(v1, mode, fixture, generation_pk)
    if value != fixture["expected"]:
        raise RuntimeError("warmup operation returned incorrect bytes")
    after = thermal.thermal_snapshot(zones)
    if after["max_temp_mc"] >= limits["hard_limit_mc"]:
        raise RuntimeError("warmup reached CPU hard-stop limit")
    runtime_state["current_workload_unit"] = None


def normal_schedule(fixtures: list[dict[str, Any]]) -> list[tuple[dict[str, Any], str, int]]:
    work = []
    for fixture in fixtures:
        for iteration in range(REPEATS):
            shift = iteration % len(NORMAL_MODES)
            order = NORMAL_MODES[shift:] + NORMAL_MODES[:shift]
            work.extend((fixture, mode, iteration) for mode in order)
    return work


def prepare_normal_cpu(
    thermal: Any,
    target: int,
    current: int | None,
    topology: dict[int, dict[str, Any]],
    transitions: list[dict[str, Any]],
    bridge_state: dict[str, int],
    zones: list[dict[str, str]],
    resume_limit_mc: int,
    cooldowns: list[dict[str, Any]],
) -> int:
    if current is None:
        return record_pin(
            thermal, target, None, topology, transitions, "initial_normal_pin"
        )
    if current == target:
        return current

    # Same-cluster normal CPU movement must bridge through the opposite cluster.
    if topology[current]["cluster_id"] == "0" and topology[target]["cluster_id"] == "0":
        bridge = MICRO_CPUS[bridge_state["normal_bridge"] % len(MICRO_CPUS)]
        bridge_state["normal_bridge"] += 1
        current = record_pin(
            thermal, bridge, current, topology, transitions, "normal_bridge"
        )
        cooldown(
            thermal,
            zones,
            resume_limit_mc,
            {
                "lane": "normal",
                "phase": "bridge_cooldown",
                "bridge_cpu": bridge,
                "target_cpu": target,
            },
            cooldowns,
        )
        return record_pin(
            thermal, target, current, topology, transitions, "normal_bridge_to_target"
        )

    return record_pin(thermal, target, current, topology, transitions, "normal_direct")


def run_normal_lane(
    v1: Any,
    thermal: Any,
    *,
    generation_pk: str,
    fixtures: list[dict[str, Any]],
    topology: dict[int, dict[str, Any]],
    zones: list[dict[str, str]],
    resume_limit_mc: int,
    current_cpu: int | None,
    raw_samples: list[dict[str, Any]],
    batches: list[dict[str, Any]],
    observations: list[dict[str, Any]],
    transitions: list[dict[str, Any]],
    cooldowns: list[dict[str, Any]],
    baselines: dict[str, Any],
    bridge_state: dict[str, int],
    runtime_state: dict[str, Any],
) -> int | None:
    schedule = normal_schedule(fixtures)

    for cpu in NORMAL_CPUS:
        current_cpu = prepare_normal_cpu(
            thermal,
            cpu,
            current_cpu,
            topology,
            transitions,
            bridge_state,
            zones,
            resume_limit_mc,
            cooldowns,
        )
        cooldown(
            thermal,
            zones,
            resume_limit_mc,
            {"lane": "normal", "phase": "pre_warmup", "cpu": cpu},
            cooldowns,
        )
        limits_for_cpu(cpu, thermal.thermal_snapshot(zones), baselines)

        for fixture in fixtures:
            for mode in NORMAL_MODES:
                for _ in range(WARMUP):
                    warmup_operation(
                        v1,
                        thermal,
                        cpu=cpu,
                        fixture=fixture,
                        mode=mode,
                        generation_pk=generation_pk,
                        zones=zones,
                        baselines=baselines,
                        runtime_state=runtime_state,
                    )

        index = 0
        while index < len(schedule):
            cooldown(
                thermal,
                zones,
                resume_limit_mc,
                {
                    "lane": "normal",
                    "phase": "pre_batch",
                    "cpu": cpu,
                    "batch_index": len(batches),
                },
                cooldowns,
            )

            batch_start = index
            active_ns = 0
            sample_ids = []
            hard_stop = False
            gap = False

            while index < len(schedule) and active_ns < NORMAL_ACTIVE_LIMIT_NS:
                fixture, mode, iteration = schedule[index]
                sample = measured_operation(
                    v1,
                    thermal,
                    lane="normal",
                    cpu=cpu,
                    cluster="0",
                    fixture=fixture,
                    mode=mode,
                    generation_pk=generation_pk,
                    zones=zones,
                    baselines=baselines,
                    observations=observations,
                    runtime_state=runtime_state,
                    sequence=len(raw_samples),
                )
                sample["iteration"] = iteration
                raw_samples.append(sample)
                sample_ids.append(sample["sequence"])
                active_ns += sample["latency_ns"]
                index += 1

                gap = sample["observation_gap_violation"]
                hard_stop = sample["hard_stop"]
                if gap or hard_stop:
                    break

            overshoot = max(0, active_ns - NORMAL_ACTIVE_LIMIT_NS)
            batches.append(
                {
                    "batch_index": len(batches),
                    "cpu": cpu,
                    "cluster": "0",
                    "schedule_start_index": batch_start,
                    "schedule_end_index_exclusive": index,
                    "sample_sequences": sample_ids,
                    "requested_active_limit_ns": NORMAL_ACTIVE_LIMIT_NS,
                    "active_ns": active_ns,
                    "overshoot_ns": overshoot,
                    "overshoot_recorded": overshoot > 0,
                    "hard_stop": hard_stop,
                    "observation_gap_violation": gap,
                }
            )

            if gap or hard_stop:
                cooldown(
                    thermal,
                    zones,
                    resume_limit_mc,
                    {
                        "lane": "normal",
                        "phase": "batch_stop_recovery",
                        "cpu": cpu,
                        "batch_index": len(batches) - 1,
                    },
                    cooldowns,
                )

    return current_cpu


def run_micro_dispatch(
    v1: Any,
    thermal: Any,
    *,
    dispatch_index: int,
    measured: bool,
    target_cpu: int,
    relief_cpu: int,
    current_cpu: int | None,
    fixture: dict[str, Any],
    mode: str,
    generation_pk: str,
    topology: dict[int, dict[str, Any]],
    zones: list[dict[str, str]],
    resume_limit_mc: int,
    raw_samples: list[dict[str, Any]],
    dispatches: list[dict[str, Any]],
    observations: list[dict[str, Any]],
    transitions: list[dict[str, Any]],
    cooldowns: list[dict[str, Any]],
    baselines: dict[str, Any],
    runtime_state: dict[str, Any],
) -> tuple[int | None, dict[str, Any] | None]:
    if current_cpu != relief_cpu:
        current_cpu = record_pin(
            thermal,
            relief_cpu,
            current_cpu,
            topology,
            transitions,
            "micro_relief_pin",
        )

    pre_cool = cooldown(
        thermal,
        zones,
        resume_limit_mc,
        {
            "lane": "micro",
            "phase": "pre_dispatch",
            "dispatch_index": dispatch_index,
            "relief_cpu": relief_cpu,
            "target_cpu": target_cpu,
        },
        cooldowns,
    )
    relief_thermal = thermal.thermal_snapshot(zones)

    current_cpu = record_pin(
        thermal,
        target_cpu,
        current_cpu,
        topology,
        transitions,
        "micro_dispatch_to_cluster1",
    )
    target_before = thermal.thermal_snapshot(zones)
    target_freq_before = thermal.frequency_snapshot(target_cpu)
    limits_for_cpu(target_cpu, target_before, baselines)

    operation_error = None
    post_error = None
    return_error = None
    cooldown_error = None
    sample = None
    target_after = None
    target_freq_after = None
    post_cool = None

    try:
        if measured:
            sample = measured_operation(
                v1,
                thermal,
                lane="micro",
                cpu=target_cpu,
                cluster="1",
                fixture=fixture,
                mode=mode,
                generation_pk=generation_pk,
                zones=zones,
                baselines=baselines,
                observations=observations,
                runtime_state=runtime_state,
                sequence=len(raw_samples),
            )
            raw_samples.append(sample)
        else:
            warmup_operation(
                v1,
                thermal,
                cpu=target_cpu,
                fixture=fixture,
                mode=mode,
                generation_pk=generation_pk,
                zones=zones,
                baselines=baselines,
                runtime_state=runtime_state,
            )
    except BaseException as exc:
        operation_error = exc

    try:
        target_after = thermal.thermal_snapshot(zones)
        target_freq_after = thermal.frequency_snapshot(target_cpu)
    except BaseException as exc:
        post_error = exc

    # Immediate return to cluster 0 is attempted even when operation/observation fails.
    try:
        current_cpu = record_pin(
            thermal,
            relief_cpu,
            current_cpu,
            topology,
            transitions,
            "micro_immediate_return_cluster0",
        )
    except BaseException as exc:
        return_error = exc

    if return_error is None:
        try:
            post_cool = cooldown(
                thermal,
                zones,
                resume_limit_mc,
                {
                    "lane": "micro",
                    "phase": "post_dispatch",
                    "dispatch_index": dispatch_index,
                    "relief_cpu": relief_cpu,
                    "target_cpu": target_cpu,
                },
                cooldowns,
            )
        except BaseException as exc:
            cooldown_error = exc

    dispatches.append(
        {
            "dispatch_index": dispatch_index,
            "kind": "measured" if measured else "warmup",
            "fixture_id": fixture_id(fixture),
            "object_serialized_length": fixture["entry"].length,
            "mode": mode,
            "relief_cpu": relief_cpu,
            "target_cpu": target_cpu,
            "target_cluster": "1",
            "pre_cooldown": pre_cool,
            "relief_thermal_before_pin": relief_thermal,
            "target_thermal_before_operation": target_before,
            "target_frequency_before_operation": target_freq_before,
            "sample_sequence": sample["sequence"] if sample is not None else None,
            "immediate_post_operation_thermal": target_after,
            "immediate_post_operation_frequency": target_freq_after,
            "post_cooldown": post_cool,
            "operation_error": exc_record(operation_error),
            "post_observation_error": exc_record(post_error),
            "return_to_cluster0_error": exc_record(return_error),
            "cooldown_error": exc_record(cooldown_error),
        }
    )

    for error in (operation_error, post_error, return_error, cooldown_error):
        if error is not None:
            raise error

    return current_cpu, sample


def run_micro_lane(
    v1: Any,
    thermal: Any,
    *,
    generation_pk: str,
    fixtures: list[dict[str, Any]],
    topology: dict[int, dict[str, Any]],
    zones: list[dict[str, str]],
    resume_limit_mc: int,
    current_cpu: int | None,
    raw_samples: list[dict[str, Any]],
    dispatches: list[dict[str, Any]],
    observations: list[dict[str, Any]],
    transitions: list[dict[str, Any]],
    cooldowns: list[dict[str, Any]],
    baselines: dict[str, Any],
    runtime_state: dict[str, Any],
) -> int | None:
    dispatch_index = 0

    def dispatch(fixture, mode, measured):
        nonlocal current_cpu, dispatch_index
        target = MICRO_CPUS[dispatch_index % len(MICRO_CPUS)]
        relief = NORMAL_CPUS[-1]
        current_cpu, sample = run_micro_dispatch(
            v1,
            thermal,
            dispatch_index=dispatch_index,
            measured=measured,
            target_cpu=target,
            relief_cpu=relief,
            current_cpu=current_cpu,
            fixture=fixture,
            mode=mode,
            generation_pk=generation_pk,
            topology=topology,
            zones=zones,
            resume_limit_mc=resume_limit_mc,
            raw_samples=raw_samples,
            dispatches=dispatches,
            observations=observations,
            transitions=transitions,
            cooldowns=cooldowns,
            baselines=baselines,
            runtime_state=runtime_state,
        )
        dispatch_index += 1
        return sample

    for fixture in fixtures:
        for mode in MICRO_MODES:
            for _ in range(WARMUP):
                dispatch(fixture, mode, False)

    for fixture in fixtures:
        for iteration in range(REPEATS):
            shift = iteration % len(MICRO_MODES)
            order = MICRO_MODES[shift:] + MICRO_MODES[:shift]
            for mode in order:
                sample = dispatch(fixture, mode, True)
                if sample is not None:
                    sample["iteration"] = iteration

    return current_cpu


def nearest_rank_p95(values):
    ordered = sorted(values)
    rank = (95 * len(ordered) + 99) // 100
    return ordered[max(0, rank - 1)]


def distribution(values):
    if not values:
        return None
    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "mean": statistics.fmean(values),
        "median": statistics.median(values),
        "p95": nearest_rank_p95(values),
    }


def summarize_samples(samples):
    return {
        "sample_count": len(samples),
        "thermally_eligible_count":
            sum(item["thermal_eligibility"] is True for item in samples),
        "hard_stop_count": sum(item["hard_stop"] is True for item in samples),
        "observation_gap_violation_count":
            sum(item["observation_gap_violation"] is True for item in samples),
        "latency_ns": distribution([item["latency_ns"] for item in samples]),
        "operations_per_second":
            distribution([item["operations_per_second"] for item in samples]),
        "returned_bytes_per_second":
            distribution([item["returned_bytes_per_second"] for item in samples]),
        "returned_mib_per_second":
            distribution([item["returned_mib_per_second"] for item in samples]),
        "processed_bytes_per_second":
            distribution([item["processed_bytes_per_second"] for item in samples]),
        "processed_mib_per_second":
            distribution([item["processed_mib_per_second"] for item in samples]),
    }


def grouped_summary(samples, fields):
    groups = {}
    for sample in samples:
        key = "|".join(str(sample[field]) for field in fields)
        groups.setdefault(key, []).append(sample)
    return {
        key: {
            "dimensions": {field: group[0][field] for field in fields},
            "statistics": summarize_samples(group),
        }
        for key, group in sorted(groups.items())
    }


def crossover_evidence(samples):
    rows = []
    fixture_ids = sorted(
        {
            item["fixture_id"]
            for item in samples
            if item["mode"] in MICRO_MODES
        }
    )
    for fid in fixture_ids:
        for mode in MICRO_MODES:
            normal = [
                item
                for item in samples
                if item["fixture_id"] == fid
                and item["mode"] == mode
                and item["lane"] == "normal"
                and item["cluster"] == "0"
            ]
            micro = [
                item
                for item in samples
                if item["fixture_id"] == fid
                and item["mode"] == mode
                and item["lane"] == "micro"
                and item["cluster"] == "1"
            ]
            if not normal or not micro:
                continue

            n_lat = statistics.median([item["latency_ns"] for item in normal])
            m_lat = statistics.median([item["latency_ns"] for item in micro])
            n_ops = statistics.median(
                [item["operations_per_second"] for item in normal]
            )
            m_ops = statistics.median(
                [item["operations_per_second"] for item in micro]
            )
            n_mib = statistics.median(
                [item["returned_mib_per_second"] for item in normal]
            )
            m_mib = statistics.median(
                [item["returned_mib_per_second"] for item in micro]
            )

            rows.append(
                {
                    "fixture_id": fid,
                    "object_serialized_length": normal[0]["object_serialized_length"],
                    "mode": mode,
                    "normal_cluster0_sample_count": len(normal),
                    "micro_cluster1_sample_count": len(micro),
                    "normal_cluster0_median_latency_ns": n_lat,
                    "micro_cluster1_median_latency_ns": m_lat,
                    "micro_over_normal_latency_ratio": m_lat / n_lat,
                    "normal_cluster0_median_operations_per_second": n_ops,
                    "micro_cluster1_median_operations_per_second": m_ops,
                    "micro_over_normal_operations_ratio": m_ops / n_ops,
                    "normal_cluster0_median_returned_mib_per_second": n_mib,
                    "micro_cluster1_median_returned_mib_per_second": m_mib,
                    "micro_over_normal_returned_mib_ratio":
                        m_mib / n_mib if n_mib > 0 else None,
                    "micro_all_thermally_eligible":
                        all(item["thermal_eligibility"] is True for item in micro),
                }
            )
    return rows


def build_statistics(samples):
    return {
        "per_cpu": grouped_summary(samples, ("cpu",)),
        "per_cluster": grouped_summary(samples, ("cluster",)),
        "per_lane": grouped_summary(samples, ("lane",)),
        "per_mode": grouped_summary(samples, ("mode",)),
        "per_fixture_object_size":
            grouped_summary(samples, ("fixture_id", "object_serialized_length")),
        "per_lane_cpu_mode": grouped_summary(samples, ("lane", "cpu", "mode")),
        "per_lane_fixture_mode":
            grouped_summary(samples, ("lane", "fixture_id", "mode")),
        "pooled": summarize_samples(samples),
        "cluster1_vs_cluster0_size_specific_crossover": crossover_evidence(samples),
    }


def run_v1_1_benchmark(v1: Any, thermal: Any, identity_evidence: dict[str, Any]):
    original_affinity = sorted(os.sched_getaffinity(0))

    raw_samples = []
    normal_batches = []
    micro_dispatches = []
    observations = []
    transitions = []
    cooldowns = []
    baselines = {}
    runtime_state = {"current_workload_unit": None}

    evidence = {
        "raw_samples": raw_samples,
        "normal_batch_records": normal_batches,
        "micro_dispatch_records": micro_dispatches,
        "thermal_and_cpufreq_observations": observations,
        "affinity_transitions": transitions,
        "cooldown_records": cooldowns,
        "cpu_baselines": baselines,
        "runtime_state": runtime_state,
    }

    execution_error = None
    restore_error = None
    affinity_restored = False
    current_cpu = None

    allowed = None
    topology = None
    groups = None
    zones = None
    zone_mode = None
    excluded_zones = None
    initial_thermal = None
    resume_limit_mc = None
    generation_pk = None
    fixtures = []
    micro_fixtures = []
    source_before = None
    source_after = None
    fd_before = None
    fd_after = None

    try:
        fd_before = fd_count()
        allowed, topology, groups = thermal.discover_topology()
        normalized = {str(k): list(v) for k, v in groups.items()}
        if normalized != EXPECTED_CLUSTERS:
            raise RuntimeError("CPU topology differs from V1.1 preregistration")

        zones, zone_mode, excluded_zones = thermal.discover_thermal_zones()
        initial_thermal = thermal.thermal_snapshot(zones)
        initial_mc = initial_thermal["max_temp_mc"]
        if initial_mc >= INITIAL_MAX_TEMP_MC:
            raise RuntimeError("initial thermal baseline >= 75 C")

        resume_limit_mc = min(initial_mc + RESUME_RISE_MC, RESUME_ABSOLUTE_MC)
        source_before = source_fingerprint()

        generation_pk, fixtures = v1.resolve_entries()
        micro_fixtures = select_micro_fixtures(fixtures)
        if fixtures and not micro_fixtures:
            raise RuntimeError("micro fixture selection unexpectedly empty")

        current_cpu = run_normal_lane(
            v1,
            thermal,
            generation_pk=generation_pk,
            fixtures=fixtures,
            topology=topology,
            zones=zones,
            resume_limit_mc=resume_limit_mc,
            current_cpu=current_cpu,
            raw_samples=raw_samples,
            batches=normal_batches,
            observations=observations,
            transitions=transitions,
            cooldowns=cooldowns,
            baselines=baselines,
            bridge_state={"normal_bridge": 0},
            runtime_state=runtime_state,
        )

        current_cpu = run_micro_lane(
            v1,
            thermal,
            generation_pk=generation_pk,
            fixtures=micro_fixtures,
            topology=topology,
            zones=zones,
            resume_limit_mc=resume_limit_mc,
            current_cpu=current_cpu,
            raw_samples=raw_samples,
            dispatches=micro_dispatches,
            observations=observations,
            transitions=transitions,
            cooldowns=cooldowns,
            baselines=baselines,
            runtime_state=runtime_state,
        )

        fd_after = fd_count()
        source_after = source_fingerprint()

    except BaseException as exc:
        execution_error = exc

    finally:
        restore_before = None
        restore_after = None
        try:
            restore_before = sorted(os.sched_getaffinity(0))
            os.sched_setaffinity(0, set(original_affinity))
            restore_after = sorted(os.sched_getaffinity(0))
            affinity_restored = restore_after == original_affinity
            if not affinity_restored:
                raise RuntimeError("original CPU affinity was not restored")
        except BaseException as exc:
            restore_error = exc
            affinity_restored = False
        finally:
            transitions.append(
                {
                    "sequence": len(transitions),
                    "kind": "restore_original_affinity",
                    "from_cpu": current_cpu,
                    "to_cpu": None,
                    "from_cluster":
                        topology[current_cpu]["cluster_id"]
                        if topology is not None and current_cpu is not None
                        else None,
                    "to_cluster": None,
                    "cross_cluster": None,
                    "affinity_before": restore_before,
                    "affinity_after": restore_after,
                    "restore_target_affinity": original_affinity,
                    "restore_error": exc_record(restore_error),
                    "monotonic_ns": time.monotonic_ns(),
                }
            )

    common = {
        "identity_evidence": identity_evidence,
        "original_affinity": original_affinity,
        "affinity_restored": affinity_restored,
        "current_cpu": current_cpu,
        "allowed_cpus": allowed,
        "topology":
            {str(cpu): meta for cpu, meta in sorted(topology.items())}
            if topology is not None
            else None,
        "cluster_groups": groups,
        "thermal_zone_selection_mode": zone_mode,
        "governing_thermal_zones": zones,
        "excluded_thermal_zones": excluded_zones,
        "initial_thermal_baseline": initial_thermal,
        "global_resume_limit_mc": resume_limit_mc,
        "generation_pk": generation_pk,
        "source_fingerprint_before": source_before,
        "source_fingerprint_after": source_after,
        "fd_before": fd_before,
        "fd_after": fd_after,
        "fixtures": [fixture_json(item) for item in fixtures],
        "micro_fixtures": [fixture_json(item) for item in micro_fixtures],
        **evidence,
    }

    if execution_error is not None or restore_error is not None:
        raise BenchmarkExecutionError(execution_error, restore_error, common)

    statistics_report = build_statistics(raw_samples)
    checks = {
        "protocol_identity": sha256_file(PROTOCOL) == EXPECTED["protocol"],
        "v1_core_identity": sha256_file(V1_CORE) == EXPECTED["v1_core"],
        "thermal_completion_identity":
            sha256_file(THERMAL_COMPLETION) == EXPECTED["thermal_completion"],
        "thermal_raw_identity": sha256_file(THERMAL_RAW) == EXPECTED["thermal_raw"],
        "topology_exact":
            {str(k): list(v) for k, v in groups.items()} == EXPECTED_CLUSTERS,
        "affinity_restored": affinity_restored,
        "normal_cluster_not_silently_pooled":
            "per_cluster" in statistics_report
            and "0" in statistics_report["per_cluster"],
        "micro_cluster_not_silently_pooled":
            "per_cluster" in statistics_report
            and "1" in statistics_report["per_cluster"],
        "source_unchanged": source_before == source_after,
        "fd_balanced":
            True if fd_before is None or fd_after is None else fd_before == fd_after,
    }
    benchmark_valid = all(value is True for value in checks.values())

    return {
        "schema": SCHEMA,
        "frozen_identities": identity_evidence,
        "configuration": {
            "clock": "time.perf_counter_ns",
            "warmup_per_fixture_mode": WARMUP,
            "measured_per_fixture_mode": REPEATS,
            "normal_lane": {
                "cpus": list(NORMAL_CPUS),
                "cluster": "0",
                "modes": list(NORMAL_MODES),
                "requested_active_work_limit_ns": NORMAL_ACTIVE_LIMIT_NS,
                "thermal_observation_gap_limit_ns": OBSERVATION_GAP_NS,
            },
            "micro_lane": {
                "cpus": list(MICRO_CPUS),
                "cluster": "1",
                "modes": list(MICRO_MODES),
                "one_operation_per_dispatch": True,
                "cpu_alternation": "deterministic CPU6/CPU7",
                "fixture_selection":
                    "ceil(N/2) smallest by serialized length then object_pk; cap 8",
            },
            "thermal_policy": {
                "initial_max_temp_mc": INITIAL_MAX_TEMP_MC,
                "optimal_rise_mc": OPTIMAL_RISE_MC,
                "optimal_absolute_mc": OPTIMAL_ABSOLUTE_MC,
                "hard_rise_mc": HARD_RISE_MC,
                "hard_absolute_mc": HARD_ABSOLUTE_MC,
                "resume_rise_mc": RESUME_RISE_MC,
                "resume_absolute_mc": RESUME_ABSOLUTE_MC,
                "cooldown_poll_seconds": thermal.COOLDOWN_POLL_SECONDS,
                "max_cooldown_seconds": thermal.MAX_COOLDOWN_SECONDS,
            },
        },
        **common,
        "statistics": statistics_report,
        "checks": checks,
        "benchmark_valid": benchmark_valid,
        "fatal_error": None,
        "execution_error": None,
        "affinity_restore_error": None,
    }


def fatal_result(exc: BaseException, identity_evidence):
    return {
        "schema": SCHEMA,
        "protocol_sha256": EXPECTED["protocol"],
        "v1_core_sha256": EXPECTED["v1_core"],
        "thermal_completion_sha256": EXPECTED["thermal_completion"],
        "thermal_raw_sha256": EXPECTED["thermal_raw"],
        "frozen_identities": identity_evidence,
        "benchmark_valid": False,
        "fatal_error": exc_record(exc),
        "execution_error": getattr(exc, "execution_error", None),
        "affinity_restore_error": getattr(exc, "affinity_restore_error", None),
        "partial_evidence": getattr(exc, "partial_evidence", None),
    }


def main() -> None:
    # Exact-once gate occurs before dependency modules or benchmark fixtures load.
    if RESULT.exists():
        raise RuntimeError(
            "benchmark result already exists; exact-once execution forbidden"
        )

    identity_evidence = verify_frozen_identities()
    v1, thermal = load_frozen_dependencies()

    try:
        result = run_v1_1_benchmark(v1, thermal, identity_evidence)
    except BaseException as exc:
        result = fatal_result(exc, identity_evidence)

    write_json_exclusive(RESULT, result)

    if not result.get("benchmark_valid", False):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
