#!/usr/bin/env python3

import hashlib
import json
import math
import os
import statistics
import time
from pathlib import Path


SCHEMA = "openmind.cpu_thermal_characterization.v1"

PROTOCOL = Path(
    "experiments/model_fractal/"
    "CPU_THERMAL_CHARACTERIZATION_V1_PROTOCOL.md"
)

RESULT = Path(
    "experiments/model_fractal/"
    "cpu_thermal_characterization_v1.json"
)

EXPECTED_PROTOCOL_SHA256 = "16ac28f006c14aba612d93f774a6e52bfb44520a7f28a0b0980213928fbf70bb"

EXPECTED_CLUSTERS = {
    "0": [0, 1, 2, 3, 4, 5],
    "1": [6, 7],
}

BUFFER_SIZE = 1024 * 1024

STAGE_MS = (
    100,
    250,
    500,
    1000,
    2000,
    4000,
    8000,
)

EPOCH_MAX_MS = 100

PASSIVE_REST_SECONDS = 0.5

INITIAL_MAX_TEMP_MC = 75000

OPTIMAL_RISE_MC = 5000
OPTIMAL_ABSOLUTE_MC = 75000

HARD_RISE_MC = 8000
HARD_ABSOLUTE_MC = 80000

RESUME_RISE_MC = 3000
RESUME_ABSOLUTE_MC = 70000

COOLDOWN_POLL_SECONDS = 2.0
MAX_COOLDOWN_SECONDS = 120.0

THERMAL_KEYWORDS = (
    "cpu",
    "soc",
    "cpuss",
    "cluster",
    "apss",
    "little",
    "big",
    "silver",
    "gold",
    "prime",
)


def sha256_file(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def write_json_exclusive(path, data):
    with path.open(
        "x",
        encoding="utf-8",
    ) as f:
        json.dump(
            data,
            f,
            indent=2,
            sort_keys=True,
        )
        f.write("\n")


def read_text(path):
    try:
        return Path(path).read_text(
            encoding="utf-8"
        ).strip()
    except (OSError, UnicodeError):
        return None


def read_int(path):
    value = read_text(path)

    if value is None:
        return None

    try:
        return int(value)
    except ValueError:
        return None


def nearest_rank_p95(values):
    ordered = sorted(values)

    rank = (
        95 * len(ordered) + 99
    ) // 100

    return ordered[
        max(0, rank - 1)
    ]


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


def discover_topology():
    if not hasattr(
        os,
        "sched_getaffinity",
    ):
        raise RuntimeError(
            "sched_getaffinity unavailable"
        )

    if not hasattr(
        os,
        "sched_setaffinity",
    ):
        raise RuntimeError(
            "sched_setaffinity unavailable"
        )

    allowed = sorted(
        os.sched_getaffinity(0)
    )

    topology = {}
    groups = {}

    for cpu in allowed:
        root = (
            Path(
                "/sys/devices/system/cpu"
            )
            / f"cpu{cpu}"
        )

        cluster = read_text(
            root /
            "topology/cluster_id"
        )

        if cluster is None:
            raise RuntimeError(
                f"cluster unavailable for cpu{cpu}"
            )

        topology[cpu] = {
            "cpu":
                cpu,

            "cluster_id":
                cluster,

            "core_id":
                read_text(
                    root /
                    "topology/core_id"
                ),

            "physical_package_id":
                read_text(
                    root /
                    "topology/"
                    "physical_package_id"
                ),

            "cpu_capacity":
                read_int(
                    root /
                    "cpu_capacity"
                ),
        }

        groups.setdefault(
            cluster,
            [],
        ).append(cpu)

    for cpus in groups.values():
        cpus.sort()

    normalized = {
        str(cluster):
            list(cpus)
        for cluster, cpus
        in groups.items()
    }

    if normalized != EXPECTED_CLUSTERS:
        raise RuntimeError(
            "CPU topology differs from preregistration"
        )

    return allowed, topology, groups


def discover_thermal_zones():
    plausible = []

    for root in sorted(
        Path(
            "/sys/class/thermal"
        ).glob("thermal_zone*")
    ):
        zone_type = (
            read_text(
                root / "type"
            )
            or "UNKNOWN"
        )

        temp = read_int(
            root / "temp"
        )

        if (
            temp is None
            or temp < 0
            or temp > 120000
        ):
            continue

        plausible.append({
            "path": str(root),
            "type": zone_type,
        })

    preferred = [
        zone
        for zone in plausible
        if any(
            word in zone[
                "type"
            ].lower()
            for word in THERMAL_KEYWORDS
        )
    ]

    if preferred:
        return (
            preferred,
            "keyword_preferred",
        )

    if plausible:
        return (
            plausible,
            "all_plausible_fallback",
        )

    raise RuntimeError(
        "no plausible thermal sensors"
    )


def thermal_snapshot(zones):
    readings = []

    for zone in zones:
        temp = read_int(
            Path(
                zone["path"]
            ) / "temp"
        )

        if (
            temp is None
            or temp < 0
            or temp > 120000
        ):
            continue

        readings.append({
            "path":
                zone["path"],

            "type":
                zone["type"],

            "temp_mc":
                temp,
        })

    if not readings:
        raise RuntimeError(
            "thermal sensors became unreadable"
        )

    hottest = max(
        readings,
        key=lambda item:
            item["temp_mc"],
    )

    return {
        "max_temp_mc":
            hottest["temp_mc"],

        "max_zone_type":
            hottest["type"],

        "max_zone_path":
            hottest["path"],

        "readings":
            readings,
    }


def frequency_snapshot(cpu):
    root = (
        Path(
            "/sys/devices/system/cpu"
        )
        / f"cpu{cpu}"
        / "cpufreq"
    )

    return {
        "scaling_cur_freq":
            read_int(
                root /
                "scaling_cur_freq"
            ),

        "scaling_min_freq":
            read_int(
                root /
                "scaling_min_freq"
            ),

        "scaling_max_freq":
            read_int(
                root /
                "scaling_max_freq"
            ),

        "cpuinfo_min_freq":
            read_int(
                root /
                "cpuinfo_min_freq"
            ),

        "cpuinfo_max_freq":
            read_int(
                root /
                "cpuinfo_max_freq"
            ),

        "scaling_governor":
            read_text(
                root /
                "scaling_governor"
            ),
    }


def pin_cpu(cpu):
    os.sched_setaffinity(
        0,
        {cpu},
    )

    actual = set(
        os.sched_getaffinity(0)
    )

    if actual != {cpu}:
        raise RuntimeError(
            f"affinity pin failed for cpu{cpu}"
        )


def wait_until_cool(
    zones,
    resume_limit_mc,
    context,
):
    start = time.monotonic()

    before = thermal_snapshot(
        zones
    )

    if (
        before["max_temp_mc"]
        <= resume_limit_mc
    ):
        return {
            "context":
                context,

            "wait_seconds":
                0.0,

            "before":
                before,

            "after":
                before,

            "completed":
                True,
        }

    while True:
        time.sleep(
            COOLDOWN_POLL_SECONDS
        )

        current = thermal_snapshot(
            zones
        )

        elapsed = (
            time.monotonic()
            - start
        )

        if (
            current["max_temp_mc"]
            <= resume_limit_mc
        ):
            return {
                "context":
                    context,

                "wait_seconds":
                    elapsed,

                "before":
                    before,

                "after":
                    current,

                "completed":
                    True,
            }

        if (
            elapsed
            >= MAX_COOLDOWN_SECONDS
        ):
            raise RuntimeError(
                "thermal cooldown timeout"
            )


def bridge_cpu(
    groups,
    from_cluster,
    bridge_positions,
):
    other = next(
        cluster
        for cluster in sorted(groups)
        if cluster != from_cluster
    )

    cpus = groups[other]

    index = (
        bridge_positions[other]
        % len(cpus)
    )

    bridge_positions[other] += 1

    return cpus[index]


def move_cross_cluster(
    current_cpu,
    target_cpu,
    topology,
    groups,
    bridge_positions,
    transitions,
    zones,
    resume_limit_mc,
    bridge_cooldowns,
):
    if current_cpu is None:
        pin_cpu(target_cpu)

        transitions.append({
            "from_cpu":
                None,

            "to_cpu":
                target_cpu,

            "from_cluster":
                None,

            "to_cluster":
                topology[
                    target_cpu
                ]["cluster_id"],

            "kind":
                "initial_pin",

            "cross_cluster":
                None,
        })

        return target_cpu

    current_cluster = topology[
        current_cpu
    ]["cluster_id"]

    target_cluster = topology[
        target_cpu
    ]["cluster_id"]

    if current_cluster != target_cluster:
        pin_cpu(target_cpu)

        transitions.append({
            "from_cpu":
                current_cpu,

            "to_cpu":
                target_cpu,

            "from_cluster":
                current_cluster,

            "to_cluster":
                target_cluster,

            "kind":
                "direct",

            "cross_cluster":
                True,
        })

        return target_cpu

    bridge = bridge_cpu(
        groups,
        current_cluster,
        bridge_positions,
    )

    bridge_cluster = topology[
        bridge
    ]["cluster_id"]

    pin_cpu(bridge)

    transitions.append({
        "from_cpu":
            current_cpu,

        "to_cpu":
            bridge,

        "from_cluster":
            current_cluster,

        "to_cluster":
            bridge_cluster,

        "kind":
            "bridge",

        "cross_cluster":
            True,
    })

    bridge_cooldown = wait_until_cool(
        zones,
        resume_limit_mc,
        {
            "phase":
                "bridge_cooldown",

            "from_cpu":
                current_cpu,

            "bridge_cpu":
                bridge,

            "bridge_cluster":
                bridge_cluster,

            "target_cpu":
                target_cpu,

            "target_cluster":
                target_cluster,
        },
    )

    bridge_cooldowns.append({
        "from_cpu":
            current_cpu,

        "bridge_cpu":
            bridge,

        "bridge_cluster":
            bridge_cluster,

        "target_cpu":
            target_cpu,

        "target_cluster":
            target_cluster,

        "cooldown":
            bridge_cooldown,
    })

    pin_cpu(target_cpu)

    transitions.append({
        "from_cpu":
            bridge,

        "to_cpu":
            target_cpu,

        "from_cluster":
            bridge_cluster,

        "to_cluster":
            target_cluster,

        "kind":
            "bridge_to_target",

        "cross_cluster":
            True,
    })

    return target_cpu


def run_epoch(
    buffer,
    requested_ns,
):
    start = time.perf_counter_ns()
    deadline = start + requested_ns

    operations = 0

    while (
        time.perf_counter_ns()
        < deadline
    ):
        hashlib.sha256(
            buffer
        ).digest()

        operations += 1

    end = time.perf_counter_ns()

    active_ns = end - start

    if operations <= 0:
        raise RuntimeError(
            "zero operations in active epoch"
        )

    bytes_processed = (
        operations
        * len(buffer)
    )

    ns_per_operation = (
        active_ns
        / operations
    )

    operations_per_second = (
        operations
        * 1_000_000_000.0
        / active_ns
    )

    bytes_per_second = (
        bytes_processed
        * 1_000_000_000.0
        / active_ns
    )

    mib_per_second = (
        bytes_per_second
        / (1024.0 * 1024.0)
    )

    return {
        "active_ns":
            active_ns,

        "operations":
            operations,

        "bytes_processed":
            bytes_processed,

        "ns_per_operation":
            ns_per_operation,

        "operations_per_second":
            operations_per_second,

        "bytes_per_second":
            bytes_per_second,

        "mib_per_second":
            mib_per_second,
    }


def summarize_epochs(epochs):
    return {
        "ns_per_operation":
            distribution([
                item[
                    "ns_per_operation"
                ]
                for item in epochs
            ]),

        "operations_per_second":
            distribution([
                item[
                    "operations_per_second"
                ]
                for item in epochs
            ]),

        "bytes_per_second":
            distribution([
                item[
                    "bytes_per_second"
                ]
                for item in epochs
            ]),

        "mib_per_second":
            distribution([
                item[
                    "mib_per_second"
                ]
                for item in epochs
            ]),
    }


def run_stage(
    cpu,
    cluster_id,
    target_ms,
    buffer,
    zones,
    cpu_baseline_mc,
    optimal_limit_mc,
    hard_limit_mc,
    stage_kind,
):
    stage_start_wall = (
        time.monotonic()
    )

    thermal_start = (
        thermal_snapshot(
            zones
        )
    )

    frequency_start = (
        frequency_snapshot(
            cpu
        )
    )

    requested_active_ns = (
        target_ms
        * 1_000_000
    )

    epoch_max_ns = (
        EPOCH_MAX_MS
        * 1_000_000
    )

    active_ns = 0
    epochs = []
    hard_stop = False

    peak_temp_mc = (
        thermal_start[
            "max_temp_mc"
        ]
    )

    while (
        active_ns
        < requested_active_ns
    ):
        remaining = (
            requested_active_ns
            - active_ns
        )

        requested_epoch_ns = min(
            epoch_max_ns,
            remaining,
        )

        epoch = run_epoch(
            buffer,
            requested_epoch_ns,
        )

        active_ns += (
            epoch["active_ns"]
        )

        thermal_after = (
            thermal_snapshot(
                zones
            )
        )

        frequency_after = (
            frequency_snapshot(
                cpu
            )
        )

        peak_temp_mc = max(
            peak_temp_mc,
            thermal_after[
                "max_temp_mc"
            ],
        )

        epochs.append({
            **epoch,

            "cpu":
                cpu,

            "cluster_id":
                cluster_id,

            "stage_kind":
                stage_kind,

            "stage_target_ms":
                target_ms,

            "epoch_index":
                len(epochs),

            "thermal_after":
                thermal_after,

            "frequency_after":
                frequency_after,
        })

        if (
            thermal_after[
                "max_temp_mc"
            ]
            >= hard_limit_mc
        ):
            hard_stop = True
            break

    thermal_end = thermal_snapshot(
        zones
    )

    frequency_end = frequency_snapshot(
        cpu
    )

    wall_seconds = (
        time.monotonic()
        - stage_start_wall
    )

    total_ops = sum(
        item["operations"]
        for item in epochs
    )

    total_bytes = sum(
        item["bytes_processed"]
        for item in epochs
    )

    total_active_ns = sum(
        item["active_ns"]
        for item in epochs
    )

    completed = (
        not hard_stop
        and total_active_ns
        >= requested_active_ns
    )

    rise_mc = (
        peak_temp_mc
        - cpu_baseline_mc
    )

    rise_c = rise_mc / 1000.0

    active_seconds = (
        total_active_ns
        / 1_000_000_000.0
    )

    overall_ops_per_second = (
        total_ops
        / active_seconds
        if active_seconds > 0
        else None
    )

    overall_bytes_per_second = (
        total_bytes
        / active_seconds
        if active_seconds > 0
        else None
    )

    overall_mib_per_second = (
        overall_bytes_per_second
        / (1024.0 * 1024.0)
        if overall_bytes_per_second
        is not None
        else None
    )

    thermal_rise_c_per_second = (
        rise_c
        / active_seconds
        if active_seconds > 0
        else None
    )

    mib_processed = (
        total_bytes
        / (1024.0 * 1024.0)
    )

    mib_per_degree = (
        mib_processed / rise_c
        if rise_c > 0
        else None
    )

    thermally_eligible = (
        completed
        and peak_temp_mc
        <= optimal_limit_mc
    )

    return {
        "stage_kind":
            stage_kind,

        "target_ms":
            target_ms,

        "completed":
            completed,

        "hard_stop":
            hard_stop,

        "thermally_eligible":
            thermally_eligible,

        "cpu_baseline_mc":
            cpu_baseline_mc,

        "optimal_limit_mc":
            optimal_limit_mc,

        "hard_limit_mc":
            hard_limit_mc,

        "thermal_start":
            thermal_start,

        "thermal_end":
            thermal_end,

        "peak_temp_mc":
            peak_temp_mc,

        "temperature_rise_mc":
            rise_mc,

        "active_ns":
            total_active_ns,

        "active_seconds":
            active_seconds,

        "wall_seconds":
            wall_seconds,

        "operations":
            total_ops,

        "bytes_processed":
            total_bytes,

        "overall_operations_per_second":
            overall_ops_per_second,

        "overall_bytes_per_second":
            overall_bytes_per_second,

        "overall_mib_per_second":
            overall_mib_per_second,

        "thermal_rise_c_per_active_second":
            thermal_rise_c_per_second,

        "mib_processed_per_degree_c":
            mib_per_degree,

        "frequency_start":
            frequency_start,

        "frequency_end":
            frequency_end,

        "epoch_statistics":
            summarize_epochs(
                epochs
            ),

        "epochs":
            epochs,
    }


def characterize_cpu(
    cpu,
    topology,
    buffer,
    zones,
    global_resume_limit_mc,
):
    cluster = topology[
        cpu
    ]["cluster_id"]

    cooldown_before = (
        wait_until_cool(
            zones,
            global_resume_limit_mc,
            {
                "cpu":
                    cpu,
                "phase":
                    "pre_test",
            },
        )
    )

    cpu_baseline = (
        thermal_snapshot(
            zones
        )
    )

    baseline_mc = (
        cpu_baseline[
            "max_temp_mc"
        ]
    )

    optimal_limit_mc = min(
        baseline_mc
        + OPTIMAL_RISE_MC,
        OPTIMAL_ABSOLUTE_MC,
    )

    hard_limit_mc = min(
        baseline_mc
        + HARD_RISE_MC,
        HARD_ABSOLUTE_MC,
    )

    stages = []

    for target_ms in STAGE_MS:
        stage = run_stage(
            cpu,
            cluster,
            target_ms,
            buffer,
            zones,
            baseline_mc,
            optimal_limit_mc,
            hard_limit_mc,
            "staircase",
        )

        stages.append(stage)

        if stage["hard_stop"]:
            break

        time.sleep(
            PASSIVE_REST_SECONDS
        )

    eligible = [
        stage
        for stage in stages
        if stage[
            "thermally_eligible"
        ]
    ]

    preliminary = (
        max(
            eligible,
            key=lambda item:
                item["target_ms"],
        )
        if eligible
        else None
    )

    confirmation = None
    recovery = None
    confirmed = False
    duty_cycle = None

    if preliminary is not None:
        cooldown_pre_confirm = (
            wait_until_cool(
                zones,
                global_resume_limit_mc,
                {
                    "cpu":
                        cpu,
                    "phase":
                        "pre_confirmation",
                },
            )
        )

        confirm_baseline = (
            thermal_snapshot(
                zones
            )
        )

        confirm_baseline_mc = (
            confirm_baseline[
                "max_temp_mc"
            ]
        )

        confirm_optimal = min(
            confirm_baseline_mc
            + OPTIMAL_RISE_MC,
            OPTIMAL_ABSOLUTE_MC,
        )

        confirm_hard = min(
            confirm_baseline_mc
            + HARD_RISE_MC,
            HARD_ABSOLUTE_MC,
        )

        confirmation = run_stage(
            cpu,
            cluster,
            preliminary[
                "target_ms"
            ],
            buffer,
            zones,
            confirm_baseline_mc,
            confirm_optimal,
            confirm_hard,
            "confirmation",
        )

        confirmation[
            "cooldown_before"
        ] = cooldown_pre_confirm

        confirmed = (
            confirmation[
                "thermally_eligible"
            ]
        )

        recovery = wait_until_cool(
            zones,
            global_resume_limit_mc,
            {
                "cpu":
                    cpu,
                "phase":
                    "post_confirmation",
            },
        )

        if confirmed:
            active = confirmation[
                "active_seconds"
            ]

            cool = recovery[
                "wait_seconds"
            ]

            denominator = (
                active + cool
            )

            duty_cycle = (
                active / denominator
                if denominator > 0
                else 1.0
            )

    return {
        "cpu":
            cpu,

        "cluster_id":
            cluster,

        "cooldown_before":
            cooldown_before,

        "cpu_baseline":
            cpu_baseline,

        "cpu_baseline_mc":
            baseline_mc,

        "optimal_limit_mc":
            optimal_limit_mc,

        "hard_limit_mc":
            hard_limit_mc,

        "stages":
            stages,

        "preliminary_optimal_target_ms":
            (
                preliminary[
                    "target_ms"
                ]
                if preliminary
                else None
            ),

        "confirmation":
            confirmation,

        "confirmation_status":
            (
                "CONFIRMED"
                if confirmed
                else
                "NOT_CONFIRMED"
            ),

        "confirmed_active_window_ms":
            (
                confirmation[
                    "target_ms"
                ]
                if confirmed
                else None
            ),

        "recovery":
            recovery,

        "sustainable_duty_cycle":
            duty_cycle,

        "hard_stop_observed":
            any(
                stage[
                    "hard_stop"
                ]
                for stage in stages
            ),
    }


def run_characterization():
    original_affinity = sorted(
        os.sched_getaffinity(0)
    )

    allowed, topology, groups = (
        discover_topology()
    )

    zones, zone_mode = (
        discover_thermal_zones()
    )

    initial_thermal = thermal_snapshot(
        zones
    )

    initial_baseline_mc = (
        initial_thermal[
            "max_temp_mc"
        ]
    )

    if (
        initial_baseline_mc
        >= INITIAL_MAX_TEMP_MC
    ):
        raise RuntimeError(
            "initial thermal baseline >= 75 C"
        )

    global_resume_limit_mc = min(
        initial_baseline_mc
        + RESUME_RISE_MC,
        RESUME_ABSOLUTE_MC,
    )

    buffer = bytes(
        (
            index % 251
            for index in range(
                BUFFER_SIZE
            )
        )
    )

    test_order = [
        0,
        6,
        1,
        7,
        2,
        3,
        4,
        5,
    ]

    profiles = []
    transitions = []
    bridge_cooldowns = []

    bridge_positions = {
        cluster: 0
        for cluster in groups
    }

    current_cpu = None
    affinity_restored = False

    try:
        for cpu in test_order:
            current_cpu = (
                move_cross_cluster(
                    current_cpu,
                    cpu,
                    topology,
                    groups,
                    bridge_positions,
                    transitions,
                    zones,
                    global_resume_limit_mc,
                    bridge_cooldowns,
                )
            )

            profile = characterize_cpu(
                cpu,
                topology,
                buffer,
                zones,
                global_resume_limit_mc,
            )

            profiles.append(
                profile
            )

    finally:
        os.sched_setaffinity(
            0,
            set(
                original_affinity
            ),
        )

        affinity_restored = (
            sorted(
                os.sched_getaffinity(
                    0
                )
            )
            == original_affinity
        )

    cross_cluster_transitions = [
        item
        for item in transitions
        if item[
            "kind"
        ] != "initial_pin"
    ]

    checks = {
        "topology_exact":
            {
                str(cluster):
                    cpus
                for cluster, cpus
                in groups.items()
            }
            == EXPECTED_CLUSTERS,

        "all_eight_cpus_profiled":
            sorted(
                profile["cpu"]
                for profile
                in profiles
            )
            == list(range(8)),

        "thermal_sensors_available":
            bool(zones),

        "initial_baseline_safe":
            initial_baseline_mc
            < INITIAL_MAX_TEMP_MC,

        "all_single_cpu_transitions_cross_cluster":
            all(
                item[
                    "cross_cluster"
                ] is True
                for item
                in cross_cluster_transitions
            ),

        "affinity_restored":
            affinity_restored,

        "profiles_complete":
            len(profiles) == 8,
    }

    characterization_valid = all(
        checks.values()
    )

    confirmed = [
        profile
        for profile in profiles
        if profile[
            "confirmation_status"
        ] == "CONFIRMED"
    ]

    return {
        "schema":
            SCHEMA,

        "protocol_sha256":
            EXPECTED_PROTOCOL_SHA256,

        "configuration": {
            "buffer_size_bytes":
                BUFFER_SIZE,

            "stage_ms":
                list(STAGE_MS),

            "epoch_max_ms":
                EPOCH_MAX_MS,

            "passive_rest_seconds":
                PASSIVE_REST_SECONDS,

            "optimal_rise_mc":
                OPTIMAL_RISE_MC,

            "optimal_absolute_mc":
                OPTIMAL_ABSOLUTE_MC,

            "hard_rise_mc":
                HARD_RISE_MC,

            "hard_absolute_mc":
                HARD_ABSOLUTE_MC,

            "resume_rise_mc":
                RESUME_RISE_MC,

            "resume_absolute_mc":
                RESUME_ABSOLUTE_MC,

            "cooldown_poll_seconds":
                COOLDOWN_POLL_SECONDS,

            "max_cooldown_seconds":
                MAX_COOLDOWN_SECONDS,

            "selection_rule":
                "longest confirmed thermally eligible stage",
        },

        "original_affinity":
            original_affinity,

        "allowed_cpus":
            allowed,

        "topology": {
            str(cpu): meta
            for cpu, meta
            in sorted(
                topology.items()
            )
        },

        "cluster_groups":
            groups,

        "thermal_zone_selection_mode":
            zone_mode,

        "thermal_zones":
            zones,

        "initial_thermal_baseline":
            initial_thermal,

        "global_resume_limit_mc":
            global_resume_limit_mc,

        "test_order":
            test_order,

        "affinity_transitions":
            transitions,

        "bridge_cooldowns":
            bridge_cooldowns,

        "profiles":
            profiles,

        "confirmed_cpu_count":
            len(confirmed),

        "checks":
            checks,

        "characterization_valid":
            characterization_valid,

        "fatal_error":
            None,
    }


def fatal_result(exc):
    return {
        "schema":
            SCHEMA,

        "protocol_sha256":
            EXPECTED_PROTOCOL_SHA256,

        "characterization_valid":
            False,

        "fatal_error": {
            "type":
                type(exc).__name__,

            "message":
                str(exc),
        },
    }


def main():
    if RESULT.exists():
        raise RuntimeError(
            "CPU characterization result already exists; "
            "exact-once execution forbidden"
        )

    if (
        sha256_file(PROTOCOL)
        != EXPECTED_PROTOCOL_SHA256
    ):
        raise RuntimeError(
            "CPU characterization protocol identity mismatch"
        )

    try:
        result = run_characterization()

    except Exception as exc:
        result = fatal_result(
            exc
        )

    write_json_exclusive(
        RESULT,
        result,
    )

    if not result.get(
        "characterization_valid",
        False,
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
