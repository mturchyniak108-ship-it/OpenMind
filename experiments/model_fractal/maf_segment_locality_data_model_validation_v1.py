#!/usr/bin/env python3

from dataclasses import fields
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import traceback


VALIDATION_SCHEMA = (
    "openmind.maf_segment_locality_data_model_validation.v1"
)

VALIDATION_PROTOCOL_SHA256 = (
    "954e71a523694b2913c35d328efdc59f7c95413c1746e7c50c087045da4291d8"
)

DATA_MODEL_PROTOCOL_SHA256 = (
    "712caa2e7dfc948f607a4c8d68064fc838eb1f58701fc5206c52aaf8e6492bc4"
)

PARENT_PHASE6D_PROTOCOL_SHA256 = (
    "a4c1a1d4fe22f7e714efa331cec9cf4dbd3a9e178f2b28b3ddb9034387e210ae"
)

IMPLEMENTATION_SHA256 = (
    "5432f2d74a610f2d0f9181e9af146013bb198a4e837af634993909358fff8ad0"
)

PHASE6C_ENGINE_SHA256 = (
    "4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9"
)

ROOT = Path(__file__).resolve().parents[2]

IMPLEMENTATION_PATH = ROOT / (
    "experiments/model_fractal/"
    "maf_segment_locality_data_model_v1.py"
)

DATA_MODEL_PROTOCOL_PATH = ROOT / (
    "experiments/model_fractal/"
    "MAF_SEGMENT_LOCALITY_DATA_MODEL_V1_PROTOCOL.md"
)

PARENT_PHASE6D_PROTOCOL_PATH = ROOT / (
    "experiments/model_fractal/"
    "MAF_SEGMENT_LOCALITY_REPACKING_V1_PROTOCOL.md"
)

VALIDATION_PROTOCOL_PATH = ROOT / (
    "experiments/model_fractal/"
    "MAF_SEGMENT_LOCALITY_DATA_MODEL_VALIDATION_V1_PROTOCOL.md"
)

PHASE6C_ENGINE_PATH = ROOT / (
    "experiments/model_fractal/"
    "maf_object_runtime_residency_v1.py"
)

RESULT_PATH = ROOT / (
    "experiments/model_fractal/"
    "maf_segment_locality_data_model_validation_v1.json"
)

EXPECTED_CHECK_COUNT = 50

CHECK_NAMES = (
    "V01_module_binding",
    "V02_canonical_json_determinism",
    "V03_plain_integer_validation",
    "V04_exact_event_kind_surface",
    "V05_event_field_combinations",
    "V06_strict_sequence_enforcement",
    "V07_duplicate_sequence_rejection",
    "V08_access_counting",
    "V09_self_transition_counting",
    "V10_directed_transition_counting",
    "V11_non_access_preserves_access_adjacency",
    "V12_first_access_reuse_behavior",
    "V13_reuse_interval_count",
    "V14_reuse_interval_sum",
    "V15_reuse_interval_min",
    "V16_reuse_interval_max",
    "V17_materialization_independence",
    "V18_bytes_read_accounting",
    "V19_named_cache_hit_accounting",
    "V20_named_cache_miss_accounting",
    "V21_residency_transition_aggregation",
    "V22_prefetch_issue_accounting",
    "V23_prefetch_consumed_accounting",
    "V24_prefetch_unused_accounting",
    "V25_duplicate_prefetch_terminal_rejection",
    "V26_invalid_event_failure_atomicity",
    "V27_empty_snapshot_semantics",
    "V28_nonempty_sequence_bounds",
    "V29_deterministic_snapshot_ordering",
    "V30_snapshot_payload_reproducibility",
    "V31_snapshot_sha_reproducibility",
    "V32_zero_denominator_metric_rejection",
    "V33_weighted_rank_distance_exactness",
    "V34_cross_segment_fraction_exactness",
    "V35_co_segment_fraction_exactness",
    "V36_cross_co_complement",
    "V37_placement_uniqueness",
    "V38_contiguous_segment_ordinals",
    "V39_contiguous_object_ordinals",
    "V40_exact_source_object_set_preservation",
    "V41_deterministic_planner_config_ordering",
    "V42_duplicate_planner_config_key_rejection",
    "V43_source_generation_binding",
    "V44_telemetry_snapshot_binding",
    "V45_deterministic_plan_ordering",
    "V46_plan_payload_reproducibility",
    "V47_plan_sha_reproducibility",
    "V48_no_payload_mutation_surface",
    "V49_phase6c_source_immutability",
    "V50_import_time_side_effect_absence",
)

MODEL_PK = (
    "mafmodel:v1:"
    + "1" * 64
)

GENERATION_PK = (
    "mafgen:v1:"
    + "2" * 64
)

OBJECT_A = (
    "mafobj:v1:"
    + "a" * 64
)

OBJECT_B = (
    "mafobj:v1:"
    + "b" * 64
)

OBJECT_C = (
    "mafobj:v1:"
    + "c" * 64
)

OBJECT_D = (
    "mafobj:v1:"
    + "d" * 64
)

MANIFEST_SHA = (
    "e" * 64
)

TELEMETRY_SHA = (
    "f" * 64
)


class ValidationHarnessError(
    Exception
):
    pass


def sha256_file(
    path,
):
    h = hashlib.sha256()

    with Path(path).open(
        "rb"
    ) as f:
        for chunk in iter(
            lambda: f.read(
                8 * 1024 * 1024
            ),
            b"",
        ):
            h.update(
                chunk
            )

    return h.hexdigest()


def canonical_json_bytes(
    value,
):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode(
        "utf-8"
    )


def require(
    condition,
    message,
):
    if not condition:
        raise AssertionError(
            message
        )


def expect_raises(
    exc_type,
    func,
):
    try:
        func()

    except exc_type:
        return

    except Exception as exc:
        raise AssertionError(
            "unexpected exception type: "
            + type(exc).__name__
            + ": "
            + str(exc)
        ) from exc

    raise AssertionError(
        "expected exception was not raised"
    )


def write_result_atomic(
    result,
):
    if RESULT_PATH.exists():
        raise ValidationHarnessError(
            "raw validation result already exists"
        )

    temp_path = RESULT_PATH.with_name(
        RESULT_PATH.name
        + ".tmp"
    )

    if temp_path.exists():
        raise ValidationHarnessError(
            "raw validation temporary residue already exists"
        )

    payload = (
        json.dumps(
            result,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )

    with temp_path.open(
        "x",
        encoding="utf-8",
        newline="\n",
    ) as f:
        f.write(
            payload
        )
        f.flush()
        os.fsync(
            f.fileno()
        )

    os.replace(
        temp_path,
        RESULT_PATH,
    )


def binding_gate():
    observed = {
        "implementation":
            sha256_file(
                IMPLEMENTATION_PATH
            ),

        "data_protocol":
            sha256_file(
                DATA_MODEL_PROTOCOL_PATH
            ),

        "parent_phase6d_protocol":
            sha256_file(
                PARENT_PHASE6D_PROTOCOL_PATH
            ),

        "validation_protocol":
            sha256_file(
                VALIDATION_PROTOCOL_PATH
            ),

        "phase6c_engine":
            sha256_file(
                PHASE6C_ENGINE_PATH
            ),
    }

    expected = {
        "implementation":
            IMPLEMENTATION_SHA256,

        "data_protocol":
            DATA_MODEL_PROTOCOL_SHA256,

        "parent_phase6d_protocol":
            PARENT_PHASE6D_PROTOCOL_SHA256,

        "validation_protocol":
            VALIDATION_PROTOCOL_SHA256,

        "phase6c_engine":
            PHASE6C_ENGINE_SHA256,
    }

    require(
        observed == expected,
        (
            "frozen source/protocol "
            "binding mismatch: "
            + repr(
                observed
            )
        ),
    )

    return observed


def load_target():
    spec = (
        importlib.util
        .spec_from_file_location(
            "openmind_maf_segment_locality_data_model_validation_target_v1",
            IMPLEMENTATION_PATH,
        )
    )

    if (
        spec is None
        or spec.loader
        is None
    ):
        raise ValidationHarnessError(
            "could not create target module spec"
        )

    module = (
        importlib.util
        .module_from_spec(
            spec
        )
    )

    sys.modules[
        spec.name
    ] = module

    spec.loader.exec_module(
        module
    )

    return module


def new_accumulator(
    mod,
):
    return mod.TelemetryAccumulator(
        model_pk=MODEL_PK,
        source_generation_pk=(
            GENERATION_PK
        ),
        source_manifest_sha256=(
            MANIFEST_SHA
        ),
    )


def access_event(
    mod,
    sequence,
    object_pk,
):
    return mod.TelemetryEvent(
        sequence=sequence,
        kind=(
            mod.TelemetryEventKind
            .ACCESS
        ),
        object_pk=object_pk,
    )


def object_map(
    snapshot,
):
    return {
        item.object_pk:
            item
        for item
        in snapshot.object_aggregates
    }


def transition_map(
    snapshot,
):
    return {
        (
            item.source_object_pk,
            item.target_object_pk,
        ):
            item.count
        for item
        in snapshot.transition_aggregates
    }


def cache_map(
    snapshot,
):
    return {
        (
            item.cache_name,
            item.object_pk,
        ): (
            item.hit_count,
            item.miss_count,
        )
        for item
        in snapshot.cache_aggregates
    }


def residency_map(
    snapshot,
):
    return {
        (
            item.object_pk,
            item.from_state,
            item.to_state,
        ):
            item.count
        for item
        in snapshot.residency_transition_aggregates
    }


def prefetch_map(
    snapshot,
):
    return {
        item.object_pk: (
            item.issued_count,
            item.consumed_count,
            item.unused_count,
        )
        for item
        in snapshot.prefetch_aggregates
    }


def metric_fixture(
    mod,
):
    placements = (
        mod.RepackPlacement(
            object_pk=OBJECT_A,
            target_segment_ordinal=0,
            target_object_ordinal=0,
        ),
        mod.RepackPlacement(
            object_pk=OBJECT_B,
            target_segment_ordinal=0,
            target_object_ordinal=1,
        ),
        mod.RepackPlacement(
            object_pk=OBJECT_C,
            target_segment_ordinal=1,
            target_object_ordinal=0,
        ),
    )

    transitions = (
        mod.TransitionTelemetryAggregate(
            source_object_pk=OBJECT_A,
            target_object_pk=OBJECT_B,
            count=3,
        ),
        mod.TransitionTelemetryAggregate(
            source_object_pk=OBJECT_A,
            target_object_pk=OBJECT_C,
            count=5,
        ),
        mod.TransitionTelemetryAggregate(
            source_object_pk=OBJECT_B,
            target_object_pk=OBJECT_C,
            count=2,
        ),
        mod.TransitionTelemetryAggregate(
            source_object_pk=OBJECT_C,
            target_object_pk=OBJECT_C,
            count=4,
        ),
    )

    return (
        transitions,
        placements,
    )


def make_plan(
    mod,
    *,
    placements=None,
    planner_config=None,
    model_pk=MODEL_PK,
    source_generation_pk=GENERATION_PK,
    source_manifest_sha256=MANIFEST_SHA,
    telemetry_snapshot_sha256=TELEMETRY_SHA,
):
    if placements is None:
        placements = (
            mod.RepackPlacement(
                object_pk=OBJECT_A,
                target_segment_ordinal=0,
                target_object_ordinal=0,
            ),
            mod.RepackPlacement(
                object_pk=OBJECT_B,
                target_segment_ordinal=0,
                target_object_ordinal=1,
            ),
        )

    if planner_config is None:
        planner_config = ()

    return mod.RepackPlan(
        schema=(
            mod.REPACK_PLAN_SCHEMA
        ),
        planner_version=(
            "validation_planner_v1"
        ),
        model_pk=model_pk,
        source_generation_pk=(
            source_generation_pk
        ),
        source_manifest_sha256=(
            source_manifest_sha256
        ),
        telemetry_snapshot_sha256=(
            telemetry_snapshot_sha256
        ),
        objective_metric_id=(
            mod.LocalityMetricId
            .WEIGHTED_TRANSITION_RANK_DISTANCE
        ),
        planner_config=tuple(
            planner_config
        ),
        placements=tuple(
            placements
        ),
    )


def append_check(
    checks,
    name,
    func,
):
    try:
        func()

    except Exception as exc:
        checks.append(
            {
                "name": name,
                "pass": False,
                "error": (
                    type(exc).__name__
                    + ": "
                    + str(exc)
                ),
            }
        )

    else:
        checks.append(
            {
                "name": name,
                "pass": True,
                "error": None,
            }
        )


def precompute_v50():
    try:
        with tempfile.TemporaryDirectory(
            prefix=(
                "openmind_phase6d_"
                "validation_v1_"
            )
        ) as temp_dir:
            observation = Path(
                temp_dir
            )

            before = tuple(
                sorted(
                    str(
                        path.relative_to(
                            observation
                        )
                    )
                    for path
                    in observation.rglob("*")
                )
            )

            require(
                before == (),
                "V50 observation directory was not empty",
            )

            child_code = (
                "import importlib.util, pathlib, sys\n"
                "p = pathlib.Path(sys.argv[1]).resolve()\n"
                "s = importlib.util.spec_from_file_location("
                "'openmind_v50_target', p)\n"
                "assert s is not None and s.loader is not None\n"
                "m = importlib.util.module_from_spec(s)\n"
                "sys.modules[s.name] = m\n"
                "s.loader.exec_module(m)\n"
            )

            env = dict(
                os.environ
            )

            env[
                "PYTHONDONTWRITEBYTECODE"
            ] = "1"

            proc = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    child_code,
                    str(
                        IMPLEMENTATION_PATH
                    ),
                ],
                cwd=observation,
                env=env,
                capture_output=True,
                text=True,
            )

            require(
                proc.returncode == 0,
                (
                    "isolated child import failed: "
                    + proc.stderr
                ),
            )

            after = tuple(
                sorted(
                    str(
                        path.relative_to(
                            observation
                        )
                    )
                    for path
                    in observation.rglob("*")
                )
            )

            require(
                after == before,
                (
                    "isolated import modified "
                    "observation directory: "
                    + repr(
                        after
                    )
                ),
            )

    except Exception as exc:
        return {
            "name":
                "V50_import_time_side_effect_absence",
            "pass":
                False,
            "error":
                (
                    type(exc).__name__
                    + ": "
                    + str(exc)
                ),
        }

    return {
        "name":
            "V50_import_time_side_effect_absence",
        "pass":
            True,
        "error":
            None,
    }


def main():
    checks = []
    fatal_error = None

    phase6c_before = (
        sha256_file(
            PHASE6C_ENGINE_PATH
        )
    )

    try:
        binding_observed = (
            binding_gate()
        )

    except Exception as exc:
        fatal_error = (
            type(exc).__name__
            + ": "
            + str(exc)
        )

        result = {
            "schema":
                VALIDATION_SCHEMA,
            "validation_valid":
                False,
            "all_pass":
                False,
            "checks":
                checks,
            "failed_checks":
                [],
            "fatal_error":
                fatal_error,
            "benchmark_executed":
                False,
            "performance_verdict":
                None,
            "implementation_path":
                str(
                    IMPLEMENTATION_PATH.relative_to(
                        ROOT
                    )
                ),
            "implementation_sha256":
                sha256_file(
                    IMPLEMENTATION_PATH
                ),
            "protocol_path":
                str(
                    VALIDATION_PROTOCOL_PATH.relative_to(
                        ROOT
                    )
                ),
            "protocol_sha256":
                sha256_file(
                    VALIDATION_PROTOCOL_PATH
                ),
            "phase6c_engine_sha256":
                sha256_file(
                    PHASE6C_ENGINE_PATH
                ),
            "check_count":
                0,
        }

        write_result_atomic(
            result
        )

        return 2

    try:
        mod = load_target()

        append_check(
            checks,
            CHECK_NAMES[0],
            lambda: require(
                (
                    binding_observed[
                        "implementation"
                    ]
                    == IMPLEMENTATION_SHA256
                    and binding_observed[
                        "data_protocol"
                    ]
                    == DATA_MODEL_PROTOCOL_SHA256
                    and binding_observed[
                        "validation_protocol"
                    ]
                    == VALIDATION_PROTOCOL_SHA256
                    and binding_observed[
                        "phase6c_engine"
                    ]
                    == PHASE6C_ENGINE_SHA256
                ),
                "V01 frozen binding mismatch",
            ),
        )

        def v02():
            left = {
                "b": 2,
                "a": 1,
            }

            right = {
                "a": 1,
                "b": 2,
            }

            a = (
                mod.canonical_json_bytes(
                    left
                )
            )

            b = (
                mod.canonical_json_bytes(
                    right
                )
            )

            require(
                a == b,
                "canonical JSON depends on insertion order",
            )

            require(
                a == b'{"a":1,"b":2}',
                "unexpected canonical JSON bytes",
            )

            require(
                not a.endswith(
                    b"\n"
                ),
                "canonical JSON contains trailing newline",
            )

        append_check(
            checks,
            CHECK_NAMES[1],
            v02,
        )

        def v03():
            expect_raises(
                mod.MAFSegmentLocalityValidationError,
                lambda:
                    mod.TelemetryEvent(
                        sequence=True,
                        kind=(
                            mod.TelemetryEventKind
                            .ACCESS
                        ),
                        object_pk=OBJECT_A,
                    ),
            )

            expect_raises(
                mod.MAFSegmentLocalityValidationError,
                lambda:
                    mod.TelemetryEvent(
                        sequence=-1,
                        kind=(
                            mod.TelemetryEventKind
                            .ACCESS
                        ),
                        object_pk=OBJECT_A,
                    ),
            )

            expect_raises(
                mod.MAFSegmentLocalityValidationError,
                lambda:
                    mod.RepackPlacement(
                        object_pk=OBJECT_A,
                        target_segment_ordinal=True,
                        target_object_ordinal=0,
                    ),
            )

            expect_raises(
                mod.MAFSegmentLocalityValidationError,
                lambda:
                    mod.LocalityMetricValue(
                        metric_id=(
                            mod.LocalityMetricId
                            .CO_SEGMENT_FRACTION
                        ),
                        numerator=0,
                        denominator=True,
                    ),
            )

        append_check(
            checks,
            CHECK_NAMES[2],
            v03,
        )

        def v04():
            require(
                [
                    item.name
                    for item
                    in mod.TelemetryEventKind
                ] == [
                    "ACCESS",
                    "MATERIALIZATION",
                    "BYTES_READ",
                    "CACHE_HIT",
                    "CACHE_MISS",
                    "PROMOTION",
                    "DEMOTION",
                    "PREFETCH_ISSUED",
                    "PREFETCH_CONSUMED",
                    "PREFETCH_UNUSED",
                ],
                "event kind surface mismatch",
            )

        append_check(
            checks,
            CHECK_NAMES[3],
            v04,
        )

        def v05():
            mod.TelemetryEvent(
                sequence=1,
                kind=(
                    mod.TelemetryEventKind
                    .ACCESS
                ),
                object_pk=OBJECT_A,
            )

            mod.TelemetryEvent(
                sequence=2,
                kind=(
                    mod.TelemetryEventKind
                    .BYTES_READ
                ),
                object_pk=OBJECT_A,
                byte_count=7,
            )

            mod.TelemetryEvent(
                sequence=3,
                kind=(
                    mod.TelemetryEventKind
                    .CACHE_HIT
                ),
                object_pk=OBJECT_A,
                cache_name="maf_cache",
            )

            mod.TelemetryEvent(
                sequence=4,
                kind=(
                    mod.TelemetryEventKind
                    .PROMOTION
                ),
                object_pk=OBJECT_A,
                from_state="MAPPED",
                to_state="HOT_MAF",
            )

            mod.TelemetryEvent(
                sequence=5,
                kind=(
                    mod.TelemetryEventKind
                    .PREFETCH_ISSUED
                ),
                object_pk=OBJECT_A,
                prefetch_id="p1",
            )

            expect_raises(
                mod.MAFSegmentLocalityValidationError,
                lambda:
                    mod.TelemetryEvent(
                        sequence=6,
                        kind=(
                            mod.TelemetryEventKind
                            .ACCESS
                        ),
                        object_pk=OBJECT_A,
                        byte_count=1,
                    ),
            )

            expect_raises(
                mod.MAFSegmentLocalityValidationError,
                lambda:
                    mod.TelemetryEvent(
                        sequence=7,
                        kind=(
                            mod.TelemetryEventKind
                            .BYTES_READ
                        ),
                        object_pk=OBJECT_A,
                    ),
            )

            expect_raises(
                mod.MAFSegmentLocalityValidationError,
                lambda:
                    mod.TelemetryEvent(
                        sequence=8,
                        kind="ACCESS",
                        object_pk=OBJECT_A,
                    ),
            )

        append_check(
            checks,
            CHECK_NAMES[4],
            v05,
        )

        def v06():
            acc = new_accumulator(
                mod
            )

            acc.add_event(
                access_event(
                    mod,
                    10,
                    OBJECT_A,
                )
            )

            before = (
                mod.snapshot_sha256(
                    acc.snapshot()
                )
            )

            expect_raises(
                mod.MAFSegmentLocalitySequenceError,
                lambda:
                    acc.add_event(
                        access_event(
                            mod,
                            9,
                            OBJECT_B,
                        )
                    ),
            )

            require(
                mod.snapshot_sha256(
                    acc.snapshot()
                ) == before,
                "decreasing sequence changed committed state",
            )

        append_check(
            checks,
            CHECK_NAMES[5],
            v06,
        )

        def v07():
            acc = new_accumulator(
                mod
            )

            acc.add_event(
                access_event(
                    mod,
                    10,
                    OBJECT_A,
                )
            )

            before = (
                mod.snapshot_sha256(
                    acc.snapshot()
                )
            )

            expect_raises(
                mod.MAFSegmentLocalitySequenceError,
                lambda:
                    acc.add_event(
                        access_event(
                            mod,
                            10,
                            OBJECT_B,
                        )
                    ),
            )

            require(
                mod.snapshot_sha256(
                    acc.snapshot()
                ) == before,
                "duplicate sequence changed committed state",
            )

        append_check(
            checks,
            CHECK_NAMES[6],
            v07,
        )

        def v08():
            acc = new_accumulator(
                mod
            )

            acc.add_event(
                access_event(
                    mod,
                    1,
                    OBJECT_A,
                )
            )

            snap = acc.snapshot()
            objects = object_map(
                snap
            )

            require(
                objects[
                    OBJECT_A
                ].access_count
                == 1,
                "object access count mismatch",
            )

            require(
                snap.access_event_count
                == 1,
                "global access event count mismatch",
            )

        append_check(
            checks,
            CHECK_NAMES[7],
            v08,
        )

        def v09():
            acc = new_accumulator(
                mod
            )

            acc.add_event(
                access_event(
                    mod,
                    1,
                    OBJECT_A,
                )
            )

            acc.add_event(
                access_event(
                    mod,
                    2,
                    OBJECT_A,
                )
            )

            transitions = transition_map(
                acc.snapshot()
            )

            require(
                transitions
                == {
                    (
                        OBJECT_A,
                        OBJECT_A,
                    ): 1
                },
                "self transition mismatch",
            )

        append_check(
            checks,
            CHECK_NAMES[8],
            v09,
        )

        def v10():
            acc = new_accumulator(
                mod
            )

            acc.add_event(
                access_event(
                    mod,
                    1,
                    OBJECT_A,
                )
            )

            acc.add_event(
                access_event(
                    mod,
                    2,
                    OBJECT_B,
                )
            )

            transitions = transition_map(
                acc.snapshot()
            )

            require(
                transitions.get(
                    (
                        OBJECT_A,
                        OBJECT_B,
                    )
                ) == 1,
                "A->B transition missing",
            )

            require(
                (
                    OBJECT_B,
                    OBJECT_A,
                )
                not in transitions,
                "reverse transition was invented",
            )

        append_check(
            checks,
            CHECK_NAMES[9],
            v10,
        )

        def v11():
            acc = new_accumulator(
                mod
            )

            acc.add_event(
                access_event(
                    mod,
                    1,
                    OBJECT_A,
                )
            )

            acc.add_event(
                mod.TelemetryEvent(
                    sequence=2,
                    kind=(
                        mod.TelemetryEventKind
                        .BYTES_READ
                    ),
                    object_pk=OBJECT_A,
                    byte_count=17,
                )
            )

            acc.add_event(
                access_event(
                    mod,
                    3,
                    OBJECT_B,
                )
            )

            transitions = transition_map(
                acc.snapshot()
            )

            require(
                transitions
                == {
                    (
                        OBJECT_A,
                        OBJECT_B,
                    ): 1
                },
                "non-access event broke access adjacency",
            )

        append_check(
            checks,
            CHECK_NAMES[10],
            v11,
        )

        def v12():
            acc = new_accumulator(
                mod
            )

            acc.add_event(
                access_event(
                    mod,
                    4,
                    OBJECT_A,
                )
            )

            item = object_map(
                acc.snapshot()
            )[OBJECT_A]

            require(
                item.reuse_interval_count
                == 0,
                "first access produced reuse count",
            )

            require(
                item.reuse_interval_sum
                == 0,
                "first access produced reuse sum",
            )

            require(
                item.reuse_interval_min
                is None,
                "first access produced reuse min",
            )

            require(
                item.reuse_interval_max
                is None,
                "first access produced reuse max",
            )

        append_check(
            checks,
            CHECK_NAMES[11],
            v12,
        )

        def reuse_fixture():
            acc = new_accumulator(
                mod
            )

            for sequence in (
                1,
                5,
                8,
            ):
                acc.add_event(
                    access_event(
                        mod,
                        sequence,
                        OBJECT_A,
                    )
                )

            return object_map(
                acc.snapshot()
            )[OBJECT_A]

        append_check(
            checks,
            CHECK_NAMES[12],
            lambda: require(
                reuse_fixture()
                .reuse_interval_count
                == 2,
                "reuse count mismatch",
            ),
        )

        append_check(
            checks,
            CHECK_NAMES[13],
            lambda: require(
                reuse_fixture()
                .reuse_interval_sum
                == 7,
                "reuse sum mismatch",
            ),
        )

        append_check(
            checks,
            CHECK_NAMES[14],
            lambda: require(
                reuse_fixture()
                .reuse_interval_min
                == 3,
                "reuse min mismatch",
            ),
        )

        append_check(
            checks,
            CHECK_NAMES[15],
            lambda: require(
                reuse_fixture()
                .reuse_interval_max
                == 4,
                "reuse max mismatch",
            ),
        )

        def v17():
            acc = new_accumulator(
                mod
            )

            acc.add_event(
                mod.TelemetryEvent(
                    sequence=1,
                    kind=(
                        mod.TelemetryEventKind
                        .MATERIALIZATION
                    ),
                    object_pk=OBJECT_A,
                )
            )

            snap = acc.snapshot()
            item = object_map(
                snap
            )[OBJECT_A]

            require(
                item.materialization_count
                == 1,
                "materialization count mismatch",
            )

            require(
                item.access_count == 0,
                "materialization changed access count",
            )

            require(
                item.bytes_read == 0,
                "materialization changed bytes read",
            )

            require(
                snap.access_event_count
                == 0,
                "materialization changed access-event count",
            )

            require(
                snap.cache_aggregates
                == (),
                "materialization changed cache state",
            )

            require(
                snap.residency_transition_aggregates
                == (),
                "materialization changed residency state",
            )

        append_check(
            checks,
            CHECK_NAMES[16],
            v17,
        )

        def v18():
            acc = new_accumulator(
                mod
            )

            for sequence, count in (
                (
                    1,
                    123,
                ),
                (
                    2,
                    7,
                ),
            ):
                acc.add_event(
                    mod.TelemetryEvent(
                        sequence=sequence,
                        kind=(
                            mod.TelemetryEventKind
                            .BYTES_READ
                        ),
                        object_pk=OBJECT_A,
                        byte_count=count,
                    )
                )

            require(
                object_map(
                    acc.snapshot()
                )[
                    OBJECT_A
                ].bytes_read
                == 130,
                "bytes-read accounting mismatch",
            )

        append_check(
            checks,
            CHECK_NAMES[17],
            v18,
        )

        def v19():
            acc = new_accumulator(
                mod
            )

            acc.add_event(
                mod.TelemetryEvent(
                    sequence=1,
                    kind=(
                        mod.TelemetryEventKind
                        .CACHE_HIT
                    ),
                    object_pk=OBJECT_A,
                    cache_name="cache_a",
                )
            )

            require(
                cache_map(
                    acc.snapshot()
                )
                == {
                    (
                        "cache_a",
                        OBJECT_A,
                    ): (
                        1,
                        0,
                    )
                },
                "cache-hit accounting mismatch",
            )

        append_check(
            checks,
            CHECK_NAMES[18],
            v19,
        )

        def v20():
            acc = new_accumulator(
                mod
            )

            acc.add_event(
                mod.TelemetryEvent(
                    sequence=1,
                    kind=(
                        mod.TelemetryEventKind
                        .CACHE_MISS
                    ),
                    object_pk=OBJECT_A,
                    cache_name="cache_a",
                )
            )

            require(
                cache_map(
                    acc.snapshot()
                )
                == {
                    (
                        "cache_a",
                        OBJECT_A,
                    ): (
                        0,
                        1,
                    )
                },
                "cache-miss accounting mismatch",
            )

        append_check(
            checks,
            CHECK_NAMES[19],
            v20,
        )

        def v21():
            acc = new_accumulator(
                mod
            )

            acc.add_event(
                mod.TelemetryEvent(
                    sequence=1,
                    kind=(
                        mod.TelemetryEventKind
                        .PROMOTION
                    ),
                    object_pk=OBJECT_A,
                    from_state="MAPPED",
                    to_state="HOT_MAF",
                )
            )

            acc.add_event(
                mod.TelemetryEvent(
                    sequence=2,
                    kind=(
                        mod.TelemetryEventKind
                        .DEMOTION
                    ),
                    object_pk=OBJECT_A,
                    from_state="HOT_MAF",
                    to_state="MAPPED",
                )
            )

            require(
                residency_map(
                    acc.snapshot()
                )
                == {
                    (
                        OBJECT_A,
                        "HOT_MAF",
                        "MAPPED",
                    ): 1,
                    (
                        OBJECT_A,
                        "MAPPED",
                        "HOT_MAF",
                    ): 1,
                },
                "residency aggregation mismatch",
            )

        append_check(
            checks,
            CHECK_NAMES[20],
            v21,
        )

        def v22():
            acc = new_accumulator(
                mod
            )

            acc.add_event(
                mod.TelemetryEvent(
                    sequence=1,
                    kind=(
                        mod.TelemetryEventKind
                        .PREFETCH_ISSUED
                    ),
                    object_pk=OBJECT_A,
                    prefetch_id="p1",
                )
            )

            require(
                prefetch_map(
                    acc.snapshot()
                )[
                    OBJECT_A
                ] == (
                    1,
                    0,
                    0,
                ),
                "prefetch issue accounting mismatch",
            )

        append_check(
            checks,
            CHECK_NAMES[21],
            v22,
        )

        def v23():
            acc = new_accumulator(
                mod
            )

            acc.add_event(
                mod.TelemetryEvent(
                    sequence=1,
                    kind=(
                        mod.TelemetryEventKind
                        .PREFETCH_ISSUED
                    ),
                    object_pk=OBJECT_A,
                    prefetch_id="p1",
                )
            )

            acc.add_event(
                mod.TelemetryEvent(
                    sequence=2,
                    kind=(
                        mod.TelemetryEventKind
                        .PREFETCH_CONSUMED
                    ),
                    object_pk=OBJECT_A,
                    prefetch_id="p1",
                )
            )

            require(
                prefetch_map(
                    acc.snapshot()
                )[
                    OBJECT_A
                ] == (
                    1,
                    1,
                    0,
                ),
                "prefetch consumed accounting mismatch",
            )

        append_check(
            checks,
            CHECK_NAMES[22],
            v23,
        )

        def v24():
            acc = new_accumulator(
                mod
            )

            acc.add_event(
                mod.TelemetryEvent(
                    sequence=1,
                    kind=(
                        mod.TelemetryEventKind
                        .PREFETCH_ISSUED
                    ),
                    object_pk=OBJECT_A,
                    prefetch_id="p1",
                )
            )

            acc.add_event(
                mod.TelemetryEvent(
                    sequence=2,
                    kind=(
                        mod.TelemetryEventKind
                        .PREFETCH_UNUSED
                    ),
                    object_pk=OBJECT_A,
                    prefetch_id="p1",
                )
            )

            require(
                prefetch_map(
                    acc.snapshot()
                )[
                    OBJECT_A
                ] == (
                    1,
                    0,
                    1,
                ),
                "prefetch unused accounting mismatch",
            )

        append_check(
            checks,
            CHECK_NAMES[23],
            v24,
        )

        def v25():
            acc = new_accumulator(
                mod
            )

            acc.add_event(
                mod.TelemetryEvent(
                    sequence=1,
                    kind=(
                        mod.TelemetryEventKind
                        .PREFETCH_ISSUED
                    ),
                    object_pk=OBJECT_A,
                    prefetch_id="p1",
                )
            )

            acc.add_event(
                mod.TelemetryEvent(
                    sequence=2,
                    kind=(
                        mod.TelemetryEventKind
                        .PREFETCH_CONSUMED
                    ),
                    object_pk=OBJECT_A,
                    prefetch_id="p1",
                )
            )

            before = (
                mod.snapshot_sha256(
                    acc.snapshot()
                )
            )

            expect_raises(
                mod.MAFSegmentLocalityPrefetchError,
                lambda:
                    acc.add_event(
                        mod.TelemetryEvent(
                            sequence=3,
                            kind=(
                                mod.TelemetryEventKind
                                .PREFETCH_UNUSED
                            ),
                            object_pk=OBJECT_A,
                            prefetch_id="p1",
                        )
                    ),
            )

            require(
                mod.snapshot_sha256(
                    acc.snapshot()
                ) == before,
                "duplicate terminal resolution changed state",
            )

        append_check(
            checks,
            CHECK_NAMES[24],
            v25,
        )

        def v26():
            acc = new_accumulator(
                mod
            )

            acc.add_event(
                access_event(
                    mod,
                    1,
                    OBJECT_A,
                )
            )

            before = (
                mod.snapshot_sha256(
                    acc.snapshot()
                )
            )

            invalid = (
                mod.TelemetryEvent(
                    sequence=2,
                    kind=(
                        mod.TelemetryEventKind
                        .PREFETCH_CONSUMED
                    ),
                    object_pk=OBJECT_A,
                    prefetch_id="unknown",
                )
            )

            expect_raises(
                mod.MAFSegmentLocalityPrefetchError,
                lambda:
                    acc.add_event(
                        invalid
                    ),
            )

            after = (
                mod.snapshot_sha256(
                    acc.snapshot()
                )
            )

            require(
                after == before,
                "invalid event changed snapshot identity",
            )

        append_check(
            checks,
            CHECK_NAMES[25],
            v26,
        )

        def v27():
            snap = (
                new_accumulator(
                    mod
                ).snapshot()
            )

            require(
                snap.event_count == 0,
                "empty event count mismatch",
            )

            require(
                snap.access_event_count
                == 0,
                "empty access count mismatch",
            )

            require(
                snap.first_sequence
                is None,
                "empty first sequence not null",
            )

            require(
                snap.last_sequence
                is None,
                "empty last sequence not null",
            )

            require(
                snap.object_aggregates
                == (),
                "empty object aggregates not empty",
            )

            require(
                snap.transition_aggregates
                == (),
                "empty transitions not empty",
            )

            require(
                snap.cache_aggregates
                == (),
                "empty cache aggregates not empty",
            )

            require(
                snap.residency_transition_aggregates
                == (),
                "empty residency aggregates not empty",
            )

            require(
                snap.prefetch_aggregates
                == (),
                "empty prefetch aggregates not empty",
            )

        append_check(
            checks,
            CHECK_NAMES[26],
            v27,
        )

        def v28():
            acc = new_accumulator(
                mod
            )

            acc.add_event(
                access_event(
                    mod,
                    5,
                    OBJECT_A,
                )
            )

            acc.add_event(
                mod.TelemetryEvent(
                    sequence=9,
                    kind=(
                        mod.TelemetryEventKind
                        .MATERIALIZATION
                    ),
                    object_pk=OBJECT_A,
                )
            )

            snap = acc.snapshot()

            require(
                snap.first_sequence
                == 5,
                "first sequence mismatch",
            )

            require(
                snap.last_sequence
                == 9,
                "last sequence mismatch",
            )

            require(
                snap.event_count
                == 2,
                "event count mismatch",
            )

        append_check(
            checks,
            CHECK_NAMES[27],
            v28,
        )

        def v29():
            acc = new_accumulator(
                mod
            )

            events = (
                access_event(
                    mod,
                    1,
                    OBJECT_B,
                ),
                access_event(
                    mod,
                    2,
                    OBJECT_A,
                ),
                access_event(
                    mod,
                    3,
                    OBJECT_B,
                ),
                mod.TelemetryEvent(
                    sequence=4,
                    kind=(
                        mod.TelemetryEventKind
                        .CACHE_HIT
                    ),
                    object_pk=OBJECT_B,
                    cache_name="z_cache",
                ),
                mod.TelemetryEvent(
                    sequence=5,
                    kind=(
                        mod.TelemetryEventKind
                        .CACHE_MISS
                    ),
                    object_pk=OBJECT_A,
                    cache_name="a_cache",
                ),
                mod.TelemetryEvent(
                    sequence=6,
                    kind=(
                        mod.TelemetryEventKind
                        .PROMOTION
                    ),
                    object_pk=OBJECT_B,
                    from_state="MAPPED",
                    to_state="HOT_MAF",
                ),
                mod.TelemetryEvent(
                    sequence=7,
                    kind=(
                        mod.TelemetryEventKind
                        .DEMOTION
                    ),
                    object_pk=OBJECT_A,
                    from_state="HOT_MAF",
                    to_state="MAPPED",
                ),
                mod.TelemetryEvent(
                    sequence=8,
                    kind=(
                        mod.TelemetryEventKind
                        .PREFETCH_ISSUED
                    ),
                    object_pk=OBJECT_B,
                    prefetch_id="p2",
                ),
                mod.TelemetryEvent(
                    sequence=9,
                    kind=(
                        mod.TelemetryEventKind
                        .PREFETCH_UNUSED
                    ),
                    object_pk=OBJECT_B,
                    prefetch_id="p2",
                ),
                mod.TelemetryEvent(
                    sequence=10,
                    kind=(
                        mod.TelemetryEventKind
                        .PREFETCH_ISSUED
                    ),
                    object_pk=OBJECT_A,
                    prefetch_id="p1",
                ),
                mod.TelemetryEvent(
                    sequence=11,
                    kind=(
                        mod.TelemetryEventKind
                        .PREFETCH_CONSUMED
                    ),
                    object_pk=OBJECT_A,
                    prefetch_id="p1",
                ),
            )

            for event in events:
                acc.add_event(
                    event
                )

            snap = acc.snapshot()

            require(
                [
                    x.object_pk
                    for x
                    in snap.object_aggregates
                ] == sorted(
                    [
                        OBJECT_A,
                        OBJECT_B,
                    ]
                ),
                "object ordering mismatch",
            )

            require(
                [
                    (
                        x.source_object_pk,
                        x.target_object_pk,
                    )
                    for x
                    in snap.transition_aggregates
                ] == sorted(
                    [
                        (
                            OBJECT_B,
                            OBJECT_A,
                        ),
                        (
                            OBJECT_A,
                            OBJECT_B,
                        ),
                    ]
                ),
                "transition ordering mismatch",
            )

            require(
                [
                    (
                        x.cache_name,
                        x.object_pk,
                    )
                    for x
                    in snap.cache_aggregates
                ] == sorted(
                    [
                        (
                            "z_cache",
                            OBJECT_B,
                        ),
                        (
                            "a_cache",
                            OBJECT_A,
                        ),
                    ]
                ),
                "cache ordering mismatch",
            )

            require(
                [
                    (
                        x.object_pk,
                        x.from_state,
                        x.to_state,
                    )
                    for x
                    in snap.residency_transition_aggregates
                ] == sorted(
                    [
                        (
                            OBJECT_B,
                            "MAPPED",
                            "HOT_MAF",
                        ),
                        (
                            OBJECT_A,
                            "HOT_MAF",
                            "MAPPED",
                        ),
                    ]
                ),
                "residency ordering mismatch",
            )

            require(
                [
                    x.object_pk
                    for x
                    in snap.prefetch_aggregates
                ] == sorted(
                    [
                        OBJECT_A,
                        OBJECT_B,
                    ]
                ),
                "prefetch ordering mismatch",
            )

        append_check(
            checks,
            CHECK_NAMES[28],
            v29,
        )

        def reproducible_snapshots():
            def build():
                acc = new_accumulator(
                    mod
                )

                fresh_events = (
                    access_event(
                        mod,
                        1,
                        OBJECT_A,
                    ),
                    mod.TelemetryEvent(
                        sequence=2,
                        kind=(
                            mod.TelemetryEventKind
                            .BYTES_READ
                        ),
                        object_pk=OBJECT_A,
                        byte_count=32,
                    ),
                    access_event(
                        mod,
                        3,
                        OBJECT_B,
                    ),
                )

                for event in fresh_events:
                    acc.add_event(
                        event
                    )

                return (
                    acc.snapshot()
                )

            return (
                build(),
                build(),
            )

        def v30():
            left, right = (
                reproducible_snapshots()
            )

            require(
                mod.snapshot_payload(
                    left
                )
                == mod.snapshot_payload(
                    right
                ),
                "independent snapshot payloads differ",
            )

        append_check(
            checks,
            CHECK_NAMES[29],
            v30,
        )

        def v31():
            left, right = (
                reproducible_snapshots()
            )

            left_sha = (
                mod.snapshot_sha256(
                    left
                )
            )

            right_sha = (
                mod.snapshot_sha256(
                    right
                )
            )

            reference = (
                hashlib.sha256(
                    mod.canonical_json_bytes(
                        mod.snapshot_payload(
                            left
                        )
                    )
                ).hexdigest()
            )

            require(
                left_sha
                == right_sha
                == reference,
                "snapshot SHA reproducibility mismatch",
            )

        append_check(
            checks,
            CHECK_NAMES[30],
            v31,
        )

        def v32():
            placements = (
                mod.RepackPlacement(
                    object_pk=OBJECT_A,
                    target_segment_ordinal=0,
                    target_object_ordinal=0,
                ),
            )

            empty = ()

            for func in (
                mod.weighted_transition_rank_distance,
                mod.cross_segment_fraction,
                mod.co_segment_fraction,
            ):
                expect_raises(
                    mod.MAFSegmentLocalityMetricError,
                    lambda func=func:
                        func(
                            empty,
                            placements,
                        ),
                )

        append_check(
            checks,
            CHECK_NAMES[31],
            v32,
        )

        def metric_values():
            transitions, placements = (
                metric_fixture(
                    mod
                )
            )

            return (
                mod.weighted_transition_rank_distance(
                    transitions,
                    placements,
                ),
                mod.cross_segment_fraction(
                    transitions,
                    placements,
                ),
                mod.co_segment_fraction(
                    transitions,
                    placements,
                ),
            )

        append_check(
            checks,
            CHECK_NAMES[32],
            lambda: require(
                (
                    metric_values()[0]
                    .numerator,
                    metric_values()[0]
                    .denominator,
                ) == (
                    15,
                    14,
                ),
                "weighted rank distance mismatch",
            ),
        )

        append_check(
            checks,
            CHECK_NAMES[33],
            lambda: require(
                (
                    metric_values()[1]
                    .numerator,
                    metric_values()[1]
                    .denominator,
                ) == (
                    7,
                    14,
                ),
                "cross-segment metric mismatch",
            ),
        )

        append_check(
            checks,
            CHECK_NAMES[34],
            lambda: require(
                (
                    metric_values()[2]
                    .numerator,
                    metric_values()[2]
                    .denominator,
                ) == (
                    7,
                    14,
                ),
                "co-segment metric mismatch",
            ),
        )

        def v36():
            _, cross, co = (
                metric_values()
            )

            require(
                cross.denominator
                == co.denominator,
                "cross/co denominator mismatch",
            )

            require(
                (
                    cross.numerator
                    + co.numerator
                )
                == cross.denominator,
                "cross/co complement invariant failed",
            )

        append_check(
            checks,
            CHECK_NAMES[35],
            v36,
        )

        def v37():
            duplicate_object = (
                mod.RepackPlacement(
                    object_pk=OBJECT_A,
                    target_segment_ordinal=0,
                    target_object_ordinal=0,
                ),
                mod.RepackPlacement(
                    object_pk=OBJECT_A,
                    target_segment_ordinal=0,
                    target_object_ordinal=1,
                ),
            )

            expect_raises(
                mod.MAFSegmentLocalityPlanError,
                lambda:
                    make_plan(
                        mod,
                        placements=(
                            duplicate_object
                        ),
                    ),
            )

            duplicate_coordinate = (
                mod.RepackPlacement(
                    object_pk=OBJECT_A,
                    target_segment_ordinal=0,
                    target_object_ordinal=0,
                ),
                mod.RepackPlacement(
                    object_pk=OBJECT_B,
                    target_segment_ordinal=0,
                    target_object_ordinal=0,
                ),
            )

            expect_raises(
                mod.MAFSegmentLocalityPlanError,
                lambda:
                    make_plan(
                        mod,
                        placements=(
                            duplicate_coordinate
                        ),
                    ),
            )

        append_check(
            checks,
            CHECK_NAMES[36],
            v37,
        )

        def v38():
            placements = (
                mod.RepackPlacement(
                    object_pk=OBJECT_A,
                    target_segment_ordinal=0,
                    target_object_ordinal=0,
                ),
                mod.RepackPlacement(
                    object_pk=OBJECT_B,
                    target_segment_ordinal=2,
                    target_object_ordinal=0,
                ),
            )

            expect_raises(
                mod.MAFSegmentLocalityPlanError,
                lambda:
                    make_plan(
                        mod,
                        placements=placements,
                    ),
            )

        append_check(
            checks,
            CHECK_NAMES[37],
            v38,
        )

        def v39():
            placements = (
                mod.RepackPlacement(
                    object_pk=OBJECT_A,
                    target_segment_ordinal=0,
                    target_object_ordinal=0,
                ),
                mod.RepackPlacement(
                    object_pk=OBJECT_B,
                    target_segment_ordinal=0,
                    target_object_ordinal=2,
                ),
            )

            expect_raises(
                mod.MAFSegmentLocalityPlanError,
                lambda:
                    make_plan(
                        mod,
                        placements=placements,
                    ),
            )

        append_check(
            checks,
            CHECK_NAMES[38],
            v39,
        )

        def v40():
            plan = make_plan(
                mod
            )

            require(
                mod.validate_complete_source_object_set(
                    plan,
                    (
                        OBJECT_B,
                        OBJECT_A,
                    ),
                )
                is True,
                "exact source set was rejected",
            )

            for invalid in (
                (
                    OBJECT_A,
                ),
                (
                    OBJECT_A,
                    OBJECT_B,
                    OBJECT_C,
                ),
                (
                    OBJECT_A,
                    OBJECT_A,
                ),
            ):
                expect_raises(
                    mod.MAFSegmentLocalityPlanError,
                    lambda invalid=invalid:
                        mod.validate_complete_source_object_set(
                            plan,
                            invalid,
                        ),
                )

        append_check(
            checks,
            CHECK_NAMES[39],
            v40,
        )

        def config_entries():
            return (
                mod.PlannerConfigEntry(
                    key="alpha",
                    canonical_value_json="1",
                ),
                mod.PlannerConfigEntry(
                    key="beta",
                    canonical_value_json="true",
                ),
            )

        def v41():
            config = (
                config_entries()
            )

            plan = make_plan(
                mod,
                planner_config=config,
            )

            payload = (
                mod.repack_plan_payload(
                    plan
                )
            )

            require(
                [
                    item["key"]
                    for item
                    in payload[
                        "planner_config"
                    ]
                ] == [
                    "alpha",
                    "beta",
                ],
                "planner config payload order mismatch",
            )

            expect_raises(
                mod.MAFSegmentLocalityValidationError,
                lambda:
                    make_plan(
                        mod,
                        planner_config=(
                            tuple(
                                reversed(
                                    config
                                )
                            )
                        ),
                    ),
            )

        append_check(
            checks,
            CHECK_NAMES[40],
            v41,
        )

        def v42():
            duplicate = (
                mod.PlannerConfigEntry(
                    key="alpha",
                    canonical_value_json="1",
                ),
                mod.PlannerConfigEntry(
                    key="alpha",
                    canonical_value_json="2",
                ),
            )

            expect_raises(
                mod.MAFSegmentLocalityValidationError,
                lambda:
                    make_plan(
                        mod,
                        planner_config=duplicate,
                    ),
            )

        append_check(
            checks,
            CHECK_NAMES[41],
            v42,
        )

        def bound_plan():
            return make_plan(
                mod,
                model_pk=MODEL_PK,
                source_generation_pk=(
                    GENERATION_PK
                ),
                source_manifest_sha256=(
                    MANIFEST_SHA
                ),
                telemetry_snapshot_sha256=(
                    TELEMETRY_SHA
                ),
            )

        def v43():
            payload = (
                mod.repack_plan_payload(
                    bound_plan()
                )
            )

            require(
                payload["model_pk"]
                == MODEL_PK,
                "model PK binding mismatch",
            )

            require(
                payload[
                    "source_generation_pk"
                ] == GENERATION_PK,
                "generation PK binding mismatch",
            )

            require(
                payload[
                    "source_manifest_sha256"
                ] == MANIFEST_SHA,
                "manifest SHA binding mismatch",
            )

        append_check(
            checks,
            CHECK_NAMES[42],
            v43,
        )

        append_check(
            checks,
            CHECK_NAMES[43],
            lambda: require(
                mod.repack_plan_payload(
                    bound_plan()
                )[
                    "telemetry_snapshot_sha256"
                ] == TELEMETRY_SHA,
                "telemetry snapshot binding mismatch",
            ),
        )

        def v45():
            valid = make_plan(
                mod
            )

            payload = (
                mod.repack_plan_payload(
                    valid
                )
            )

            require(
                [
                    (
                        item[
                            "target_segment_ordinal"
                        ],
                        item[
                            "target_object_ordinal"
                        ],
                    )
                    for item
                    in payload[
                        "placements"
                    ]
                ] == [
                    (
                        0,
                        0,
                    ),
                    (
                        0,
                        1,
                    ),
                ],
                "canonical plan order mismatch",
            )

            noncanonical = (
                mod.RepackPlacement(
                    object_pk=OBJECT_B,
                    target_segment_ordinal=0,
                    target_object_ordinal=1,
                ),
                mod.RepackPlacement(
                    object_pk=OBJECT_A,
                    target_segment_ordinal=0,
                    target_object_ordinal=0,
                ),
            )

            expect_raises(
                mod.MAFSegmentLocalityPlanError,
                lambda:
                    make_plan(
                        mod,
                        placements=noncanonical,
                    ),
            )

        append_check(
            checks,
            CHECK_NAMES[44],
            v45,
        )

        def independent_plans():
            left = make_plan(
                mod,
                planner_config=(
                    config_entries()
                ),
            )

            right = make_plan(
                mod,
                planner_config=(
                    config_entries()
                ),
            )

            return (
                left,
                right,
            )

        def v46():
            left, right = (
                independent_plans()
            )

            require(
                mod.repack_plan_payload(
                    left
                )
                == mod.repack_plan_payload(
                    right
                ),
                "independent plan payloads differ",
            )

        append_check(
            checks,
            CHECK_NAMES[45],
            v46,
        )

        def v47():
            left, right = (
                independent_plans()
            )

            left_sha = (
                mod.repack_plan_sha256(
                    left
                )
            )

            right_sha = (
                mod.repack_plan_sha256(
                    right
                )
            )

            reference = (
                hashlib.sha256(
                    mod.canonical_json_bytes(
                        mod.repack_plan_payload(
                            left
                        )
                    )
                ).hexdigest()
            )

            require(
                left_sha
                == right_sha
                == reference,
                "plan SHA reproducibility mismatch",
            )

        append_check(
            checks,
            CHECK_NAMES[46],
            v47,
        )

        def v48():
            forbidden_exports = {
                "payload_bytes",
                "replacement_payload",
                "activate_generation",
                "build_generation",
                "build_segment",
            }

            exported = set(
                getattr(
                    mod,
                    "__all__",
                    (),
                )
            )

            require(
                not (
                    exported
                    & forbidden_exports
                ),
                "forbidden mutation API exported",
            )

            plan_fields = {
                item.name
                for item
                in fields(
                    mod.RepackPlan
                )
            }

            require(
                plan_fields
                == {
                    "schema",
                    "planner_version",
                    "model_pk",
                    "source_generation_pk",
                    "source_manifest_sha256",
                    "telemetry_snapshot_sha256",
                    "objective_metric_id",
                    "planner_config",
                    "placements",
                },
                "RepackPlan field surface mismatch",
            )

            placement_fields = {
                item.name
                for item
                in fields(
                    mod.RepackPlacement
                )
            }

            require(
                placement_fields
                == {
                    "object_pk",
                    "target_segment_ordinal",
                    "target_object_ordinal",
                },
                "RepackPlacement field surface mismatch",
            )

            source = (
                IMPLEMENTATION_PATH
                .read_text(
                    encoding="utf-8"
                )
            )

            for token in (
                "replacement_payload",
                "activate_generation",
                "build_generation",
                "build_segment",
            ):
                require(
                    token
                    not in source,
                    (
                        "forbidden implementation "
                        "surface token present: "
                        + token
                    ),
                )

        append_check(
            checks,
            CHECK_NAMES[47],
            v48,
        )

        v50_outcome = (
            precompute_v50()
        )

        def v49():
            phase6c_after = (
                sha256_file(
                    PHASE6C_ENGINE_PATH
                )
            )

            require(
                phase6c_before
                == PHASE6C_ENGINE_SHA256,
                "Phase 6C pre-validation SHA mismatch",
            )

            require(
                phase6c_after
                == PHASE6C_ENGINE_SHA256,
                "Phase 6C post-validation SHA mismatch",
            )

        append_check(
            checks,
            CHECK_NAMES[48],
            v49,
        )

        require(
            v50_outcome[
                "name"
            ] == CHECK_NAMES[49],
            "V50 precomputed name mismatch",
        )

        checks.append(
            v50_outcome
        )

        require(
            len(checks)
            == EXPECTED_CHECK_COUNT,
            "runner did not produce exactly 50 checks",
        )

        require(
            [
                item["name"]
                for item
                in checks
            ] == list(
                CHECK_NAMES
            ),
            "runner check order differs from protocol",
        )

    except Exception as exc:
        fatal_error = (
            type(exc).__name__
            + ": "
            + str(exc)
            + "\n"
            + traceback.format_exc()
        )

    failed_checks = [
        item["name"]
        for item
        in checks
        if not item[
            "pass"
        ]
    ]

    validation_valid = (
        fatal_error is None
        and len(checks)
        == EXPECTED_CHECK_COUNT
        and [
            item["name"]
            for item
            in checks
        ] == list(
            CHECK_NAMES
        )
    )

    all_pass = (
        validation_valid
        and not failed_checks
    )

    result = {
        "schema":
            VALIDATION_SCHEMA,

        "validation_valid":
            validation_valid,

        "all_pass":
            all_pass,

        "checks":
            checks,

        "failed_checks":
            failed_checks,

        "fatal_error":
            fatal_error,

        "benchmark_executed":
            False,

        "performance_verdict":
            None,

        "implementation_path":
            str(
                IMPLEMENTATION_PATH.relative_to(
                    ROOT
                )
            ),

        "implementation_sha256":
            sha256_file(
                IMPLEMENTATION_PATH
            ),

        "protocol_path":
            str(
                VALIDATION_PROTOCOL_PATH.relative_to(
                    ROOT
                )
            ),

        "protocol_sha256":
            sha256_file(
                VALIDATION_PROTOCOL_PATH
            ),

        "data_model_protocol_sha256":
            sha256_file(
                DATA_MODEL_PROTOCOL_PATH
            ),

        "parent_phase6d_protocol_sha256":
            sha256_file(
                PARENT_PHASE6D_PROTOCOL_PATH
            ),

        "phase6c_engine_sha256":
            sha256_file(
                PHASE6C_ENGINE_PATH
            ),

        "check_count":
            len(checks),
    }

    write_result_atomic(
        result
    )

    return (
        0
        if all_pass
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
