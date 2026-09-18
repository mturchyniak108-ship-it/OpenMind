#!/usr/bin/env python3

"""Exact-once scientific validation for Phase 6D snapshot persistence V1."""

from pathlib import Path
import ast
import copy
import hashlib
import importlib
import json
import os
import signal
import subprocess
import sys
import tempfile
import traceback


RESULT_SCHEMA = (
    "openmind.maf_segment_locality."
    "telemetry_snapshot_persistence_validation.v1"
)

EXPECTED_CHECK_COUNT = 48

CHECK_NAMES = (
    "P01_frozen_provenance_binding",
    "P02_import_time_side_effect_absence",
    "P03_exact_file_schema",
    "P04_exact_envelope_key_set",
    "P05_snapshot_member_exact_payload",
    "P06_snapshot_sha_exact",
    "P07_canonical_file_bytes",
    "P08_no_trailing_newline",
    "P09_deterministic_file_sha",
    "P10_empty_snapshot_round_trip",
    "P11_nonempty_snapshot_round_trip",
    "P12_source_identity_preservation",
    "P13_sequence_identity_preservation",
    "P14_aggregate_order_preservation",
    "P15_strict_utf8_decode",
    "P16_invalid_json_rejection",
    "P17_noncanonical_json_rejection",
    "P18_unknown_envelope_key_rejection",
    "P19_missing_envelope_key_rejection",
    "P20_wrong_schema_rejection",
    "P21_snapshot_sha_syntax_rejection",
    "P22_snapshot_sha_mismatch_rejection",
    "P23_payload_mutation_detection",
    "P24_malformed_nested_payload_rejection",
    "P25_unknown_nested_field_rejection",
    "P26_invalid_integer_semantics_rejection",
    "P27_invalid_pk_rejection",
    "P28_invalid_aggregate_invariant_rejection",
    "P29_missing_file_rejection",
    "P30_nonregular_file_rejection",
    "P31_symlink_rejection",
    "P32_parent_directory_required",
    "P33_existing_final_refusal",
    "P34_existing_partial_refusal",
    "P35_partial_exclusive_creation",
    "P36_complete_partial_write",
    "P37_atomic_no_replace_publication",
    "P38_final_no_replace_race_safety",
    "P39_parent_directory_fsync",
    "P40_success_partial_removal",
    "P41_failure_residue_preservation",
    "P42_no_read_modify_write",
    "P43_serialization_determinism",
    "P44_validated_read_result",
    "P45_write_result",
    "P46_phase6c_immutability",
    "P47_no_runtime_integration",
    "P48_no_repack_planner_or_performance_claim",
)

PERSISTENCE_PROTOCOL_PATH = Path(
    "experiments/model_fractal/"
    "MAF_SEGMENT_LOCALITY_TELEMETRY_SNAPSHOT_PERSISTENCE_V1_PROTOCOL.md"
)

PERSISTENCE_PROTOCOL_SHA256 = (
    "0e08a8a18a45a16eddc05927b8191d73ca9fc7453cb97fc1140e5e243e03db51"
)

PERSISTENCE_PATH = Path(
    "experiments/model_fractal/"
    "maf_segment_locality_telemetry_snapshot_persistence_v1.py"
)

PERSISTENCE_SHA256 = (
    "4a7c8ba1e1d7e9e4004a16d54464f17fd07ba75cc84ddea25403697d53d0581c"
)

VALIDATION_PROTOCOL_PATH = Path(
    "experiments/model_fractal/"
    "MAF_SEGMENT_LOCALITY_TELEMETRY_SNAPSHOT_PERSISTENCE_VALIDATION_V1_PROTOCOL.md"
)

VALIDATION_PROTOCOL_SHA256 = (
    "7c79cf2eb97e98c14fb0acbd947ca30a8e46746eba1bd2b0127375ac01b8b9a5"
)

DATA_MODEL_PATH = Path(
    "experiments/model_fractal/"
    "maf_segment_locality_data_model_v1.py"
)

DATA_MODEL_SHA256 = (
    "5432f2d74a610f2d0f9181e9af146013bb198a4e837af634993909358fff8ad0"
)

DATA_MODEL_RESULT_PATH = Path(
    "experiments/model_fractal/"
    "maf_segment_locality_data_model_validation_v1.json"
)

DATA_MODEL_RESULT_SHA256 = (
    "9aa2e467dc451b2d2122802e1e8b8fabf616db756a36b53a3600cca793923b4d"
)

DATA_MODEL_VERDICT_PATH = Path(
    "experiments/model_fractal/"
    "MAF_SEGMENT_LOCALITY_DATA_MODEL_VALIDATION_V1_VERDICT.md"
)

DATA_MODEL_VERDICT_SHA256 = (
    "7754c9d5dada8dc214a21236827c64cafea880e4b0c679cd84c9c4833fd3e9db"
)

PHASE6C_PATH = Path(
    "experiments/model_fractal/"
    "maf_object_runtime_residency_v1.py"
)

PHASE6C_SHA256 = (
    "4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9"
)

RESULT_PATH = Path(
    "experiments/model_fractal/"
    "maf_segment_locality_telemetry_snapshot_persistence_validation_v1.json"
)

RESULT_TEMP_PATH = Path(
    str(RESULT_PATH)
    + ".tmp"
)

FILE_SCHEMA = (
    "openmind.maf_segment_locality."
    "telemetry_snapshot_file.v1"
)

BENCHMARK_EXECUTED = False
PERFORMANCE_VERDICT = None

MODEL_PK = (
    "mafmodel:v1:"
    + "1" * 64
)

GENERATION_PK = (
    "mafgen:v1:"
    + "2" * 64
)

MANIFEST_SHA = (
    "e" * 64
)

OBJECT_A = (
    "mafobj:v1:"
    + "a" * 64
)

OBJECT_B = (
    "mafobj:v1:"
    + "b" * 64
)

REPO_ROOT = Path(
    __file__
).resolve().parents[2]


class HarnessInvalid(
    Exception
):
    pass


def sha256_file(
    path,
):
    h = hashlib.sha256()

    with Path(
        path
    ).open(
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


def independent_canonical_json_bytes(
    value,
):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(
            ",",
            ":",
        ),
        ensure_ascii=False,
    ).encode(
        "utf-8"
    )


def write_result_atomic(
    payload,
):
    if RESULT_PATH.exists():
        raise HarnessInvalid(
            "raw validation result already exists"
        )

    if RESULT_TEMP_PATH.exists():
        raise HarnessInvalid(
            "raw validation temporary residue already exists"
        )

    data = independent_canonical_json_bytes(
        payload
    )

    fd = os.open(
        RESULT_TEMP_PATH,
        (
            os.O_WRONLY
            | os.O_CREAT
            | os.O_EXCL
        ),
        0o600,
    )

    try:
        offset = 0

        while offset < len(
            data
        ):
            written = os.write(
                fd,
                data[
                    offset:
                ],
            )

            if written <= 0:
                raise HarnessInvalid(
                    "short raw-result write"
                )

            offset += written

        os.fsync(
            fd
        )

    finally:
        os.close(
            fd
        )

    os.replace(
        RESULT_TEMP_PATH,
        RESULT_PATH,
    )


def binding_gate():
    expected = (
        (
            PERSISTENCE_PROTOCOL_PATH,
            PERSISTENCE_PROTOCOL_SHA256,
        ),
        (
            PERSISTENCE_PATH,
            PERSISTENCE_SHA256,
        ),
        (
            VALIDATION_PROTOCOL_PATH,
            VALIDATION_PROTOCOL_SHA256,
        ),
        (
            DATA_MODEL_PATH,
            DATA_MODEL_SHA256,
        ),
        (
            DATA_MODEL_RESULT_PATH,
            DATA_MODEL_RESULT_SHA256,
        ),
        (
            DATA_MODEL_VERDICT_PATH,
            DATA_MODEL_VERDICT_SHA256,
        ),
        (
            PHASE6C_PATH,
            PHASE6C_SHA256,
        ),
    )

    actual = {}

    for path, expected_sha in expected:
        if not path.is_file():
            raise HarnessInvalid(
                "required frozen input missing: "
                + str(
                    path
                )
            )

        digest = sha256_file(
            path
        )

        if digest != expected_sha:
            raise HarnessInvalid(
                "frozen input SHA mismatch: "
                + str(
                    path
                )
            )

        actual[
            str(
                path
            )
        ] = digest

    if RESULT_PATH.exists():
        raise HarnessInvalid(
            "raw validation result already exists"
        )

    if RESULT_TEMP_PATH.exists():
        raise HarnessInvalid(
            "raw validation temporary residue already exists"
        )

    return actual


def directory_inventory(
    root,
):
    root = Path(
        root
    )

    return sorted(
        (
            path.relative_to(
                root
            ).as_posix(),
            (
                "dir"
                if path.is_dir()
                else "file"
            ),
        )
        for path in root.rglob(
            "*"
        )
    )


def precompute_import_side_effect_check():
    with tempfile.TemporaryDirectory(
        prefix=(
            "openmind_persist_import_v1_"
        )
    ) as temp:
        root = Path(
            temp
        )

        before = directory_inventory(
            root
        )

        code = (
            "import importlib;"
            "importlib.import_module("
            "'experiments.model_fractal."
            "maf_segment_locality_telemetry_snapshot_persistence_v1'"
            ")"
        )

        env = os.environ.copy()
        env[
            "PYTHONDONTWRITEBYTECODE"
        ] = "1"

        existing = env.get(
            "PYTHONPATH"
        )

        env[
            "PYTHONPATH"
        ] = (
            str(
                REPO_ROOT
            )
            if not existing
            else (
                str(
                    REPO_ROOT
                )
                + os.pathsep
                + existing
            )
        )

        proc = subprocess.run(
            [
                sys.executable,
                "-c",
                code,
            ],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
        )

        after = directory_inventory(
            root
        )

        return (
            proc.returncode == 0
            and before == []
            and after == [],
            {
                "returncode":
                    proc.returncode,

                "before":
                    before,

                "after":
                    after,

                "stderr":
                    proc.stderr[-2000:],
            },
        )


def load_targets():
    model = importlib.import_module(
        "experiments.model_fractal."
        "maf_segment_locality_data_model_v1"
    )

    persistence = importlib.import_module(
        "experiments.model_fractal."
        "maf_segment_locality_telemetry_snapshot_persistence_v1"
    )

    return (
        model,
        persistence,
    )


def new_accumulator(
    model,
):
    return model.TelemetryAccumulator(
        model_pk=MODEL_PK,
        source_generation_pk=(
            GENERATION_PK
        ),
        source_manifest_sha256=(
            MANIFEST_SHA
        ),
    )


def telemetry_event(
    model,
    sequence,
    kind_name,
    object_pk,
    **kwargs,
):
    kind = getattr(
        model.TelemetryEventKind,
        kind_name,
    )

    return model.TelemetryEvent(
        sequence=sequence,
        kind=kind,
        object_pk=object_pk,
        **kwargs,
    )


def make_empty_snapshot(
    model,
):
    return new_accumulator(
        model
    ).snapshot()


def make_nonempty_snapshot(
    model,
):
    acc = new_accumulator(
        model
    )

    events = (
        telemetry_event(
            model,
            1,
            "ACCESS",
            OBJECT_B,
        ),
        telemetry_event(
            model,
            2,
            "CACHE_HIT",
            OBJECT_B,
            cache_name="cache_z",
        ),
        telemetry_event(
            model,
            3,
            "PROMOTION",
            OBJECT_B,
            from_state="COLD_DISK",
            to_state="MAPPED",
        ),
        telemetry_event(
            model,
            4,
            "PREFETCH_ISSUED",
            OBJECT_A,
            prefetch_id="prefetch_consumed_v1",
        ),
        telemetry_event(
            model,
            5,
            "ACCESS",
            OBJECT_A,
        ),
        telemetry_event(
            model,
            6,
            "PREFETCH_CONSUMED",
            OBJECT_A,
            prefetch_id="prefetch_consumed_v1",
        ),
        telemetry_event(
            model,
            7,
            "MATERIALIZATION",
            OBJECT_B,
        ),
        telemetry_event(
            model,
            8,
            "BYTES_READ",
            OBJECT_B,
            byte_count=128,
        ),
        telemetry_event(
            model,
            9,
            "CACHE_MISS",
            OBJECT_A,
            cache_name="cache_a",
        ),
        telemetry_event(
            model,
            10,
            "PREFETCH_ISSUED",
            OBJECT_B,
            prefetch_id="prefetch_unused_v1",
        ),
        telemetry_event(
            model,
            11,
            "DEMOTION",
            OBJECT_B,
            from_state="MAPPED",
            to_state="COLD_DISK",
        ),
        telemetry_event(
            model,
            12,
            "PREFETCH_UNUSED",
            OBJECT_B,
            prefetch_id="prefetch_unused_v1",
        ),
        telemetry_event(
            model,
            13,
            "ACCESS",
            OBJECT_B,
        ),
    )

    for event in events:
        acc.add_event(
            event
        )

    return acc.snapshot()


def make_race_snapshot(
    model,
):
    acc = new_accumulator(
        model
    )

    for index in range(
        1,
        20001,
    ):
        object_pk = (
            "mafobj:v1:"
            + format(
                index,
                "064x",
            )
        )

        acc.add_event(
            telemetry_event(
                model,
                index,
                "BYTES_READ",
                object_pk,
                byte_count=1,
            )
        )

    return acc.snapshot()


def append_check(
    checks,
    name,
    passed,
    detail=None,
):
    expected_index = len(
        checks
    )

    if (
        expected_index
        >= len(
            CHECK_NAMES
        )
        or CHECK_NAMES[
            expected_index
        ]
        != name
    ):
        raise HarnessInvalid(
            "validation check order mismatch at "
            + name
        )

    checks.append(
        {
            "name":
                name,

            "pass":
                bool(
                    passed
                ),

            "detail":
                detail,
        }
    )


def run_check(
    checks,
    name,
    fn,
):
    try:
        outcome = fn()

    except HarnessInvalid:
        raise

    except Exception as exc:
        append_check(
            checks,
            name,
            False,
            {
                "exception":
                    type(
                        exc
                    ).__name__,

                "message":
                    str(
                        exc
                    ),
            },
        )

        return False

    if (
        isinstance(
            outcome,
            tuple,
        )
        and len(
            outcome
        ) == 2
        and isinstance(
            outcome[
                0
            ],
            bool,
        )
    ):
        passed = outcome[
            0
        ]

        detail = outcome[
            1
        ]

    else:
        passed = bool(
            outcome
        )

        detail = None

    append_check(
        checks,
        name,
        passed,
        detail,
    )

    return passed


def expect_read_rejection(
    persistence,
    path,
):
    try:
        persistence.read_snapshot_file(
            path
        )

    except persistence.TelemetrySnapshotPersistenceReadError:
        return True

    except Exception:
        return False

    return False


def expect_write_rejection(
    persistence,
    snapshot,
    path,
):
    try:
        persistence.write_snapshot_file(
            snapshot,
            path,
        )

    except persistence.TelemetrySnapshotPersistenceWriteError:
        return True

    except Exception:
        return False

    return False


def canonical_candidate_bytes(
    model,
    envelope,
):
    return model.canonical_json_bytes(
        envelope
    )


def write_candidate(
    path,
    data,
):
    path = Path(
        path
    )

    with path.open(
        "xb"
    ) as f:
        f.write(
            data
        )

        f.flush()
        os.fsync(
            f.fileno()
        )


def persistence_static_evidence():
    source = PERSISTENCE_PATH.read_text(
        encoding="utf-8"
    )

    tree = ast.parse(
        source,
        filename=str(
            PERSISTENCE_PATH
        ),
    )

    functions = {}
    imports = []

    for node in tree.body:
        if isinstance(
            node,
            ast.FunctionDef,
        ):
            functions[
                node.name
            ] = node

        elif isinstance(
            node,
            ast.Import,
        ):
            imports.extend(
                alias.name
                for alias in node.names
            )

        elif isinstance(
            node,
            ast.ImportFrom,
        ):
            imports.append(
                node.module or ""
            )

    writer = functions.get(
        "write_snapshot_file"
    )

    write_all = functions.get(
        "_write_all"
    )

    if writer is None:
        raise HarnessInvalid(
            "write_snapshot_file missing during static audit"
        )

    if write_all is None:
        raise HarnessInvalid(
            "_write_all missing during static audit"
        )

    writer_calls = []
    writer_call_lines = {}

    for node in ast.walk(
        writer
    ):
        if not isinstance(
            node,
            ast.Call,
        ):
            continue

        try:
            rendered = ast.unparse(
                node.func
            )
        except Exception:
            rendered = ""

        writer_calls.append(
            rendered
        )

        writer_call_lines.setdefault(
            rendered,
            []
        ).append(
            node.lineno
        )

    write_all_calls = []

    for node in ast.walk(
        write_all
    ):
        if isinstance(
            node,
            ast.Call,
        ):
            try:
                rendered = ast.unparse(
                    node.func
                )
            except Exception:
                rendered = ""

            write_all_calls.append(
                rendered
            )

    link_nodes = []

    for node in ast.walk(
        writer
    ):
        if not isinstance(
            node,
            ast.Call,
        ):
            continue

        try:
            rendered = ast.unparse(
                node.func
            )
        except Exception:
            rendered = ""

        if rendered == "os.link":
            link_nodes.append(
                node
            )

    link_no_follow = False

    if len(
        link_nodes
    ) == 1:
        for keyword in link_nodes[
            0
        ].keywords:
            if (
                keyword.arg
                == "follow_symlinks"
                and isinstance(
                    keyword.value,
                    ast.Constant,
                )
                and keyword.value.value
                is False
            ):
                link_no_follow = True

    link_lines = writer_call_lines.get(
        "os.link",
        [],
    )

    fsync_lines = writer_call_lines.get(
        "_fsync_directory",
        [],
    )

    unlink_lines = writer_call_lines.get(
        "os.unlink",
        [],
    )

    public_functions = {
        name
        for name in functions
        if not name.startswith(
            "_"
        )
    }

    timing_imports = [
        name
        for name in imports
        if name in {
            "time",
            "timeit",
        }
    ]

    timing_calls = []

    for node in ast.walk(
        tree
    ):
        if not isinstance(
            node,
            ast.Call,
        ):
            continue

        try:
            rendered = ast.unparse(
                node.func
            ).lower()
        except Exception:
            rendered = ""

        if any(
            token in rendered
            for token in (
                "perf_counter",
                "timeit",
                "monotonic",
                "process_time",
                "thread_time",
                "clock_gettime",
            )
        ):
            timing_calls.append(
                rendered
            )

    return {
        "exclusive_create":
            (
                "os.O_EXCL"
                in source
                and "os.O_CREAT"
                in source
            ),

        "write_loop":
            (
                any(
                    isinstance(
                        node,
                        ast.While,
                    )
                    for node in ast.walk(
                        write_all
                    )
                )
                and "os.write"
                in write_all_calls
                and "os.fsync"
                in writer_calls
            ),

        "hardlink_exact_once":
            len(
                link_lines
            ) == 1,

        "hardlink_no_follow":
            link_no_follow,

        "no_replace_or_rename":
            (
                "os.replace"
                not in writer_calls
                and "os.rename"
                not in writer_calls
            ),

        "directory_fsync_order":
            (
                len(
                    link_lines
                ) == 1
                and len(
                    fsync_lines
                ) == 2
                and len(
                    unlink_lines
                ) == 1
                and link_lines[
                    0
                ]
                < fsync_lines[
                    0
                ]
                < unlink_lines[
                    0
                ]
                < fsync_lines[
                    1
                ]
            ),

        "phase6c_not_imported":
            all(
                "maf_object_runtime_residency"
                not in name
                for name in imports
            ),

        "no_runtime_surface":
            all(
                token
                not in source
                for token in (
                    "RuntimeResidency",
                    "promote(",
                    "demote(",
                    "pin(",
                    "unpin(",
                )
            ),

        "no_update_api":
            public_functions.isdisjoint(
                {
                    "overwrite_snapshot",
                    "update_snapshot",
                    "append_snapshot",
                    "repair_snapshot",
                }
            ),

        "no_repack_realization":
            all(
                token
                not in source
                for token in (
                    "build_segment(",
                    "build_generation(",
                    "activate_generation(",
                    "rollback_generation(",
                )
            ),

        "no_timing_api":
            (
                timing_imports == []
                and timing_calls == []
            ),

        "link_lines":
            link_lines,

        "directory_fsync_lines":
            fsync_lines,

        "unlink_lines":
            unlink_lines,
    }


def run_race_fixture(
    model,
    persistence,
    root,
):
    race_snapshot = make_race_snapshot(
        model
    )

    expected_bytes = persistence.snapshot_file_bytes(
        race_snapshot
    )

    payload_path = root / (
        "race_snapshot_payload.json"
    )

    payload_bytes = independent_canonical_json_bytes(
        model.snapshot_payload(
            race_snapshot
        )
    )

    write_candidate(
        payload_path,
        payload_bytes,
    )

    final_path = root / (
        "race_final.json"
    )

    partial_path = Path(
        str(
            final_path
        )
        + ".partial"
    )

    status_path = root / (
        "race_child_status.json"
    )

    child_code = r'''
import json
from pathlib import Path
import sys

from experiments.model_fractal import (
    maf_segment_locality_telemetry_snapshot_persistence_v1 as p,
)

payload_path = Path(sys.argv[1])
final_path = Path(sys.argv[2])
status_path = Path(sys.argv[3])

payload = json.loads(
    payload_path.read_text(
        encoding="utf-8"
    )
)

snapshot = p.reconstruct_snapshot_payload(
    payload
)

try:
    p.write_snapshot_file(
        snapshot,
        final_path,
    )

except Exception as exc:
    status = {
        "ok":
            False,

        "type":
            type(exc).__name__,

        "message":
            str(exc),
    }

else:
    status = {
        "ok":
            True,

        "type":
            None,

        "message":
            None,
    }

status_path.write_text(
    json.dumps(
        status,
        sort_keys=True,
        separators=(",", ":"),
    ),
    encoding="utf-8",
)
'''

    env = os.environ.copy()
    env[
        "PYTHONDONTWRITEBYTECODE"
    ] = "1"

    existing = env.get(
        "PYTHONPATH"
    )

    env[
        "PYTHONPATH"
    ] = (
        str(
            REPO_ROOT
        )
        if not existing
        else (
            str(
                REPO_ROOT
            )
            + os.pathsep
            + existing
        )
    )

    proc = subprocess.Popen(
        [
            sys.executable,
            "-c",
            child_code,
            str(
                payload_path
            ),
            str(
                final_path
            ),
            str(
                status_path
            ),
        ],
        cwd=REPO_ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    observed_partial = False

    for _ in range(
        5000000
    ):
        if partial_path.exists():
            observed_partial = True
            break

        if proc.poll() is not None:
            break

    if not observed_partial:
        stdout, stderr = proc.communicate()

        raise HarnessInvalid(
            "P38 race fixture could not observe partial before child exit; "
            "stdout="
            + repr(
                stdout[-1000:]
            )
            + "; stderr="
            + repr(
                stderr[-1000:]
            )
        )

    try:
        os.kill(
            proc.pid,
            signal.SIGSTOP,
        )

        waited_pid, wait_status = os.waitpid(
            proc.pid,
            os.WUNTRACED,
        )

        if (
            waited_pid
            != proc.pid
            or not os.WIFSTOPPED(
                wait_status
            )
        ):
            raise HarnessInvalid(
                "P38 child could not be proven stopped"
            )

        if not partial_path.exists():
            raise HarnessInvalid(
                "P38 partial disappeared before race injection"
            )

        if final_path.exists():
            raise HarnessInvalid(
                "P38 target publication completed before race injection"
            )

        sentinel = (
            b"OPENMIND_P38_COMPETING_FINAL_V1"
        )

        write_candidate(
            final_path,
            sentinel,
        )

        sentinel_sha_before = hashlib.sha256(
            sentinel
        ).hexdigest()

        os.kill(
            proc.pid,
            signal.SIGCONT,
        )

        try:
            stdout, stderr = proc.communicate(
                timeout=60,
            )

        except subprocess.TimeoutExpired as exc:
            proc.kill()
            proc.communicate()

            raise HarnessInvalid(
                "P38 child did not terminate after race injection"
            ) from exc

    finally:
        if proc.poll() is None:
            try:
                os.kill(
                    proc.pid,
                    signal.SIGCONT,
                )
            except ProcessLookupError:
                pass

    if not status_path.is_file():
        raise HarnessInvalid(
            "P38 child status artifact missing"
        )

    status_data = json.loads(
        status_path.read_text(
            encoding="utf-8"
        )
    )

    final_bytes = final_path.read_bytes()

    partial_bytes = (
        partial_path.read_bytes()
        if partial_path.is_file()
        else None
    )

    return {
        "observed_partial_before_final":
            observed_partial,

        "child_returncode":
            proc.returncode,

        "child_status":
            status_data,

        "stdout":
            stdout[-1000:],

        "stderr":
            stderr[-1000:],

        "final_bytes":
            final_bytes,

        "final_sha_before":
            sentinel_sha_before,

        "final_sha_after":
            hashlib.sha256(
                final_bytes
            ).hexdigest(),

        "partial_exists":
            partial_path.is_file(),

        "partial_bytes":
            partial_bytes,

        "expected_partial_bytes":
            expected_bytes,

        "partial_path":
            str(
                partial_path
            ),

        "final_path":
            str(
                final_path
            ),
    }


def make_result_base(
    bindings,
):
    return {
        "schema":
            RESULT_SCHEMA,

        "validation_valid":
            False,

        "all_pass":
            False,

        "checks":
            [],

        "failed_checks":
            [],

        "fatal_error":
            None,

        "benchmark_executed":
            BENCHMARK_EXECUTED,

        "performance_verdict":
            PERFORMANCE_VERDICT,

        "implementation_path":
            str(
                PERSISTENCE_PATH
            ),

        "implementation_sha256":
            bindings.get(
                str(
                    PERSISTENCE_PATH
                )
            ),

        "protocol_path":
            str(
                VALIDATION_PROTOCOL_PATH
            ),

        "protocol_sha256":
            bindings.get(
                str(
                    VALIDATION_PROTOCOL_PATH
                )
            ),

        "persistence_protocol_sha256":
            bindings.get(
                str(
                    PERSISTENCE_PROTOCOL_PATH
                )
            ),

        "data_model_sha256":
            bindings.get(
                str(
                    DATA_MODEL_PATH
                )
            ),

        "data_model_validation_result_sha256":
            bindings.get(
                str(
                    DATA_MODEL_RESULT_PATH
                )
            ),

        "data_model_verdict_sha256":
            bindings.get(
                str(
                    DATA_MODEL_VERDICT_PATH
                )
            ),

        "phase6c_engine_sha256":
            bindings.get(
                str(
                    PHASE6C_PATH
                )
            ),

        "check_count":
            EXPECTED_CHECK_COUNT,
    }


def main():
    bindings = {}

    try:
        bindings = binding_gate()

    except Exception as exc:
        result = make_result_base(
            bindings
        )

        result[
            "fatal_error"
        ] = (
            type(
                exc
            ).__name__
            + ": "
            + str(
                exc
            )
        )

        try:
            write_result_atomic(
                result
            )
        except Exception:
            traceback.print_exc()

        print(
            "VALIDATION_VALID: false"
        )

        print(
            "FATAL:",
            result[
                "fatal_error"
            ],
        )

        return 2

    result = make_result_base(
        bindings
    )

    checks = []

    phase6c_before = sha256_file(
        PHASE6C_PATH
    )

    try:
        import_ok, import_detail = (
            precompute_import_side_effect_check()
        )

        model, persistence = load_targets()

        static = persistence_static_evidence()

        run_check(
            checks,
            CHECK_NAMES[0],
            lambda: (
                all(
                    (
                        bindings[
                            str(
                                path
                            )
                        ]
                        == expected_sha
                    )
                    for path, expected_sha
                    in (
                        (
                            PERSISTENCE_PROTOCOL_PATH,
                            PERSISTENCE_PROTOCOL_SHA256,
                        ),
                        (
                            PERSISTENCE_PATH,
                            PERSISTENCE_SHA256,
                        ),
                        (
                            VALIDATION_PROTOCOL_PATH,
                            VALIDATION_PROTOCOL_SHA256,
                        ),
                        (
                            DATA_MODEL_PATH,
                            DATA_MODEL_SHA256,
                        ),
                        (
                            DATA_MODEL_RESULT_PATH,
                            DATA_MODEL_RESULT_SHA256,
                        ),
                        (
                            DATA_MODEL_VERDICT_PATH,
                            DATA_MODEL_VERDICT_SHA256,
                        ),
                        (
                            PHASE6C_PATH,
                            PHASE6C_SHA256,
                        ),
                    )
                ),
                bindings,
            ),
        )

        run_check(
            checks,
            CHECK_NAMES[1],
            lambda: (
                import_ok,
                import_detail,
            ),
        )

        empty_snapshot = make_empty_snapshot(
            model
        )

        nonempty_snapshot = make_nonempty_snapshot(
            model
        )

        envelope = persistence.snapshot_file_payload(
            nonempty_snapshot
        )

        expected_snapshot_payload = model.snapshot_payload(
            nonempty_snapshot
        )

        expected_snapshot_sha = model.snapshot_sha256(
            nonempty_snapshot
        )

        target_file_bytes = persistence.snapshot_file_bytes(
            nonempty_snapshot
        )

        independent_file_bytes = independent_canonical_json_bytes(
            envelope
        )

        independent_file_sha = hashlib.sha256(
            independent_file_bytes
        ).hexdigest()

        run_check(
            checks,
            CHECK_NAMES[2],
            lambda: (
                persistence.SNAPSHOT_FILE_SCHEMA
                == FILE_SCHEMA
            ),
        )

        run_check(
            checks,
            CHECK_NAMES[3],
            lambda: (
                set(
                    envelope.keys()
                )
                == {
                    "schema",
                    "snapshot_sha256",
                    "snapshot",
                }
                and len(
                    envelope
                )
                == 3
            ),
        )

        run_check(
            checks,
            CHECK_NAMES[4],
            lambda: (
                envelope[
                    "snapshot"
                ]
                == expected_snapshot_payload
            ),
        )

        run_check(
            checks,
            CHECK_NAMES[5],
            lambda: (
                envelope[
                    "snapshot_sha256"
                ]
                == expected_snapshot_sha
            ),
        )

        run_check(
            checks,
            CHECK_NAMES[6],
            lambda: (
                target_file_bytes
                == independent_file_bytes
            ),
        )

        run_check(
            checks,
            CHECK_NAMES[7],
            lambda: (
                len(
                    target_file_bytes
                ) > 0
                and target_file_bytes
                == independent_file_bytes
                and not target_file_bytes.endswith(
                    (
                        b"\n",
                        b"\r",
                        b" ",
                        b"\t",
                    )
                )
            ),
        )

        run_check(
            checks,
            CHECK_NAMES[8],
            lambda: (
                persistence.snapshot_file_sha256(
                    nonempty_snapshot
                )
                == independent_file_sha
            ),
        )

        shared = {}

        with tempfile.TemporaryDirectory(
            prefix=(
                "openmind_persistence_validation_v1_"
            )
        ) as temp_root_s:
            root = Path(
                temp_root_s
            )

            def p10():
                final = root / (
                    "p10_empty.json"
                )

                write_result = persistence.write_snapshot_file(
                    empty_snapshot,
                    final,
                )

                read_result = persistence.read_snapshot_file(
                    final
                )

                return (
                    (
                        model.snapshot_payload(
                            read_result.snapshot
                        )
                        == model.snapshot_payload(
                            empty_snapshot
                        )
                        and read_result.snapshot_sha256
                        == model.snapshot_sha256(
                            empty_snapshot
                        )
                        and write_result.snapshot_sha256
                        == read_result.snapshot_sha256
                    ),
                    {
                        "file_sha256":
                            read_result.file_sha256,

                        "byte_length":
                            read_result.byte_length,
                    },
                )

            run_check(
                checks,
                CHECK_NAMES[9],
                p10,
            )

            def p11():
                final = root / (
                    "p11_nonempty.json"
                )

                write_result = persistence.write_snapshot_file(
                    nonempty_snapshot,
                    final,
                )

                read_result = persistence.read_snapshot_file(
                    final
                )

                shared[
                    "positive_final"
                ] = final

                shared[
                    "positive_write"
                ] = write_result

                shared[
                    "positive_read"
                ] = read_result

                shared[
                    "positive_bytes"
                ] = final.read_bytes()

                return (
                    (
                        model.snapshot_payload(
                            read_result.snapshot
                        )
                        == expected_snapshot_payload
                        and read_result.snapshot_sha256
                        == expected_snapshot_sha
                        and read_result.file_sha256
                        == independent_file_sha
                        and read_result.byte_length
                        == len(
                            independent_file_bytes
                        )
                    ),
                    {
                        "snapshot_sha256":
                            read_result.snapshot_sha256,

                        "file_sha256":
                            read_result.file_sha256,

                        "byte_length":
                            read_result.byte_length,
                    },
                )

            run_check(
                checks,
                CHECK_NAMES[10],
                p11,
            )

            def p12():
                read_result = shared.get(
                    "positive_read"
                )

                if read_result is None:
                    return False

                reconstructed = read_result.snapshot

                return (
                    reconstructed.model_pk
                    == nonempty_snapshot.model_pk
                    and reconstructed.source_generation_pk
                    == nonempty_snapshot.source_generation_pk
                    and reconstructed.source_manifest_sha256
                    == nonempty_snapshot.source_manifest_sha256
                )

            run_check(
                checks,
                CHECK_NAMES[11],
                p12,
            )

            def p13():
                read_result = shared.get(
                    "positive_read"
                )

                if read_result is None:
                    return False

                reconstructed = read_result.snapshot

                return (
                    reconstructed.first_sequence
                    == nonempty_snapshot.first_sequence
                    and reconstructed.last_sequence
                    == nonempty_snapshot.last_sequence
                    and reconstructed.event_count
                    == nonempty_snapshot.event_count
                    and reconstructed.access_event_count
                    == nonempty_snapshot.access_event_count
                )

            run_check(
                checks,
                CHECK_NAMES[12],
                p13,
            )

            def p14():
                read_result = shared.get(
                    "positive_read"
                )

                if read_result is None:
                    return False

                reconstructed = read_result.snapshot

                return (
                    reconstructed.object_aggregates
                    == nonempty_snapshot.object_aggregates
                    and reconstructed.transition_aggregates
                    == nonempty_snapshot.transition_aggregates
                    and reconstructed.cache_aggregates
                    == nonempty_snapshot.cache_aggregates
                    and reconstructed.residency_transition_aggregates
                    == nonempty_snapshot.residency_transition_aggregates
                    and reconstructed.prefetch_aggregates
                    == nonempty_snapshot.prefetch_aggregates
                )

            run_check(
                checks,
                CHECK_NAMES[13],
                p14,
            )

            def p15():
                path = root / (
                    "p15_invalid_utf8.json"
                )

                write_candidate(
                    path,
                    b"\xff\xfe\x80",
                )

                return expect_read_rejection(
                    persistence,
                    path,
                )

            run_check(
                checks,
                CHECK_NAMES[14],
                p15,
            )

            def p16():
                path = root / (
                    "p16_invalid_json.json"
                )

                write_candidate(
                    path,
                    b'{"schema":',
                )

                return expect_read_rejection(
                    persistence,
                    path,
                )

            run_check(
                checks,
                CHECK_NAMES[15],
                p16,
            )

            def p17():
                path = root / (
                    "p17_noncanonical.json"
                )

                noncanonical = json.dumps(
                    envelope,
                    sort_keys=True,
                    ensure_ascii=False,
                    indent=2,
                ).encode(
                    "utf-8"
                )

                if (
                    noncanonical
                    == independent_file_bytes
                ):
                    raise HarnessInvalid(
                        "P17 fixture unexpectedly canonical"
                    )

                write_candidate(
                    path,
                    noncanonical,
                )

                return expect_read_rejection(
                    persistence,
                    path,
                )

            run_check(
                checks,
                CHECK_NAMES[16],
                p17,
            )

            def p18():
                path = root / (
                    "p18_extra_key.json"
                )

                candidate = copy.deepcopy(
                    envelope
                )

                candidate[
                    "unexpected"
                ] = 1

                write_candidate(
                    path,
                    canonical_candidate_bytes(
                        model,
                        candidate,
                    ),
                )

                return expect_read_rejection(
                    persistence,
                    path,
                )

            run_check(
                checks,
                CHECK_NAMES[17],
                p18,
            )

            def p19():
                outcomes = []

                for key in (
                    "schema",
                    "snapshot_sha256",
                    "snapshot",
                ):
                    candidate = copy.deepcopy(
                        envelope
                    )

                    del candidate[
                        key
                    ]

                    path = root / (
                        "p19_missing_"
                        + key
                        + ".json"
                    )

                    write_candidate(
                        path,
                        canonical_candidate_bytes(
                            model,
                            candidate,
                        ),
                    )

                    outcomes.append(
                        expect_read_rejection(
                            persistence,
                            path,
                        )
                    )

                return all(
                    outcomes
                )

            run_check(
                checks,
                CHECK_NAMES[18],
                p19,
            )

            def p20():
                candidate = copy.deepcopy(
                    envelope
                )

                candidate[
                    "schema"
                ] = (
                    FILE_SCHEMA
                    + ".wrong"
                )

                path = root / (
                    "p20_wrong_schema.json"
                )

                write_candidate(
                    path,
                    canonical_candidate_bytes(
                        model,
                        candidate,
                    ),
                )

                return expect_read_rejection(
                    persistence,
                    path,
                )

            run_check(
                checks,
                CHECK_NAMES[19],
                p20,
            )

            def p21():
                values = (
                    "A" * 64,
                    "a" * 63,
                    "a" * 65,
                    "g" * 64,
                )

                outcomes = []

                for index, value in enumerate(
                    values,
                    start=1,
                ):
                    candidate = copy.deepcopy(
                        envelope
                    )

                    candidate[
                        "snapshot_sha256"
                    ] = value

                    path = root / (
                        "p21_bad_sha_"
                        + str(
                            index
                        )
                        + ".json"
                    )

                    write_candidate(
                        path,
                        canonical_candidate_bytes(
                            model,
                            candidate,
                        ),
                    )

                    outcomes.append(
                        expect_read_rejection(
                            persistence,
                            path,
                        )
                    )

                return all(
                    outcomes
                )

            run_check(
                checks,
                CHECK_NAMES[20],
                p21,
            )

            def p22():
                candidate = copy.deepcopy(
                    envelope
                )

                candidate[
                    "snapshot_sha256"
                ] = (
                    "0" * 64
                    if expected_snapshot_sha
                    != "0" * 64
                    else "1" * 64
                )

                path = root / (
                    "p22_sha_mismatch.json"
                )

                write_candidate(
                    path,
                    canonical_candidate_bytes(
                        model,
                        candidate,
                    ),
                )

                return expect_read_rejection(
                    persistence,
                    path,
                )

            run_check(
                checks,
                CHECK_NAMES[21],
                p22,
            )

            def p23():
                candidate = copy.deepcopy(
                    envelope
                )

                candidate[
                    "snapshot"
                ][
                    "event_count"
                ] += 1

                path = root / (
                    "p23_payload_mutation.json"
                )

                write_candidate(
                    path,
                    canonical_candidate_bytes(
                        model,
                        candidate,
                    ),
                )

                return expect_read_rejection(
                    persistence,
                    path,
                )

            run_check(
                checks,
                CHECK_NAMES[22],
                p23,
            )

            def p24():
                mutations = []

                c1 = copy.deepcopy(
                    envelope
                )
                c1[
                    "snapshot"
                ][
                    "object_aggregates"
                ] = {}
                mutations.append(
                    c1
                )

                c2 = copy.deepcopy(
                    envelope
                )
                c2[
                    "snapshot"
                ][
                    "transition_aggregates"
                ] = [
                    {
                        "source_object_pk":
                            OBJECT_A,
                    }
                ]
                mutations.append(
                    c2
                )

                c3 = copy.deepcopy(
                    envelope
                )
                c3[
                    "snapshot"
                ][
                    "cache_aggregates"
                ] = "bad"
                mutations.append(
                    c3
                )

                c4 = copy.deepcopy(
                    envelope
                )
                c4[
                    "snapshot"
                ][
                    "residency_transition_aggregates"
                ] = [
                    7
                ]
                mutations.append(
                    c4
                )

                c5 = copy.deepcopy(
                    envelope
                )
                c5[
                    "snapshot"
                ][
                    "prefetch_aggregates"
                ][
                    0
                ][
                    "consumed_count"
                ] = "bad"
                mutations.append(
                    c5
                )

                outcomes = []

                for index, candidate in enumerate(
                    mutations,
                    start=1,
                ):
                    path = root / (
                        "p24_malformed_"
                        + str(
                            index
                        )
                        + ".json"
                    )

                    write_candidate(
                        path,
                        canonical_candidate_bytes(
                            model,
                            candidate,
                        ),
                    )

                    outcomes.append(
                        expect_read_rejection(
                            persistence,
                            path,
                        )
                    )

                return all(
                    outcomes
                )

            run_check(
                checks,
                CHECK_NAMES[23],
                p24,
            )

            def p25():
                targets = (
                    None,
                    "object_aggregates",
                    "transition_aggregates",
                    "cache_aggregates",
                    "residency_transition_aggregates",
                    "prefetch_aggregates",
                )

                outcomes = []

                for index, target in enumerate(
                    targets,
                    start=1,
                ):
                    candidate = copy.deepcopy(
                        envelope
                    )

                    if target is None:
                        candidate[
                            "snapshot"
                        ][
                            "unknown_nested_field"
                        ] = 1
                    else:
                        if not candidate[
                            "snapshot"
                        ][
                            target
                        ]:
                            raise HarnessInvalid(
                                "P25 representative fixture lacks "
                                + target
                            )

                        candidate[
                            "snapshot"
                        ][
                            target
                        ][
                            0
                        ][
                            "unknown_nested_field"
                        ] = 1

                    path = root / (
                        "p25_unknown_"
                        + str(
                            index
                        )
                        + ".json"
                    )

                    write_candidate(
                        path,
                        canonical_candidate_bytes(
                            model,
                            candidate,
                        ),
                    )

                    outcomes.append(
                        expect_read_rejection(
                            persistence,
                            path,
                        )
                    )

                return all(
                    outcomes
                )

            run_check(
                checks,
                CHECK_NAMES[24],
                p25,
            )

            def p26():
                candidates = []

                first = copy.deepcopy(
                    envelope
                )

                first[
                    "snapshot"
                ][
                    "event_count"
                ] = True

                candidates.append(
                    first
                )

                second = copy.deepcopy(
                    envelope
                )

                second[
                    "snapshot"
                ][
                    "object_aggregates"
                ][
                    0
                ][
                    "bytes_read"
                ] = -1

                candidates.append(
                    second
                )

                outcomes = []

                for index, candidate in enumerate(
                    candidates,
                    start=1,
                ):
                    path = root / (
                        "p26_invalid_integer_"
                        + str(
                            index
                        )
                        + ".json"
                    )

                    write_candidate(
                        path,
                        canonical_candidate_bytes(
                            model,
                            candidate,
                        ),
                    )

                    outcomes.append(
                        expect_read_rejection(
                            persistence,
                            path,
                        )
                    )

                return all(
                    outcomes
                )

            run_check(
                checks,
                CHECK_NAMES[25],
                p26,
            )

            def p27():
                candidates = []

                c1 = copy.deepcopy(
                    envelope
                )
                c1[
                    "snapshot"
                ][
                    "model_pk"
                ] = "bad-model-pk"
                candidates.append(
                    c1
                )

                c2 = copy.deepcopy(
                    envelope
                )
                c2[
                    "snapshot"
                ][
                    "source_generation_pk"
                ] = "bad-generation-pk"
                candidates.append(
                    c2
                )

                c3 = copy.deepcopy(
                    envelope
                )
                c3[
                    "snapshot"
                ][
                    "object_aggregates"
                ][
                    0
                ][
                    "object_pk"
                ] = "bad-object-pk"
                candidates.append(
                    c3
                )

                outcomes = []

                for index, candidate in enumerate(
                    candidates,
                    start=1,
                ):
                    path = root / (
                        "p27_bad_pk_"
                        + str(
                            index
                        )
                        + ".json"
                    )

                    write_candidate(
                        path,
                        canonical_candidate_bytes(
                            model,
                            candidate,
                        ),
                    )

                    outcomes.append(
                        expect_read_rejection(
                            persistence,
                            path,
                        )
                    )

                return all(
                    outcomes
                )

            run_check(
                checks,
                CHECK_NAMES[26],
                p27,
            )

            def p28():
                candidates = []

                prefetch_bad = copy.deepcopy(
                    envelope
                )

                pref = prefetch_bad[
                    "snapshot"
                ][
                    "prefetch_aggregates"
                ][
                    0
                ]

                pref[
                    "issued_count"
                ] = 1
                pref[
                    "consumed_count"
                ] = 1
                pref[
                    "unused_count"
                ] = 1

                candidates.append(
                    prefetch_bad
                )

                reuse_bad = copy.deepcopy(
                    envelope
                )

                reuse_candidates = [
                    item
                    for item in reuse_bad[
                        "snapshot"
                    ][
                        "object_aggregates"
                    ]
                    if item[
                        "reuse_interval_count"
                    ] > 0
                ]

                if not reuse_candidates:
                    raise HarnessInvalid(
                        "P28 fixture lacks reuse aggregate"
                    )

                target = reuse_candidates[
                    0
                ]

                target[
                    "reuse_interval_min"
                ] = 9

                target[
                    "reuse_interval_max"
                ] = 4

                candidates.append(
                    reuse_bad
                )

                outcomes = []

                for index, candidate in enumerate(
                    candidates,
                    start=1,
                ):
                    path = root / (
                        "p28_invariant_"
                        + str(
                            index
                        )
                        + ".json"
                    )

                    write_candidate(
                        path,
                        canonical_candidate_bytes(
                            model,
                            candidate,
                        ),
                    )

                    outcomes.append(
                        expect_read_rejection(
                            persistence,
                            path,
                        )
                    )

                return all(
                    outcomes
                )

            run_check(
                checks,
                CHECK_NAMES[27],
                p28,
            )

            def p29():
                path = root / (
                    "p29_missing.json"
                )

                return (
                    not path.exists()
                    and expect_read_rejection(
                        persistence,
                        path,
                    )
                )

            run_check(
                checks,
                CHECK_NAMES[28],
                p29,
            )

            def p30():
                path = root / (
                    "p30_directory"
                )

                path.mkdir()

                before = list(
                    path.iterdir()
                )

                rejected = expect_read_rejection(
                    persistence,
                    path,
                )

                after = list(
                    path.iterdir()
                )

                return (
                    rejected
                    and before == after == []
                )

            run_check(
                checks,
                CHECK_NAMES[29],
                p30,
            )

            def p31():
                target = shared.get(
                    "positive_final"
                )

                if target is None:
                    raise HarnessInvalid(
                        "P31 requires successful positive fixture"
                    )

                link = root / (
                    "p31_symlink.json"
                )

                try:
                    os.symlink(
                        target,
                        link,
                    )

                except Exception as exc:
                    raise HarnessInvalid(
                        "P31 symlink capability unavailable: "
                        + type(
                            exc
                        ).__name__
                        + ": "
                        + str(
                            exc
                        )
                    ) from exc

                return (
                    link.is_symlink()
                    and expect_read_rejection(
                        persistence,
                        link,
                    )
                )

            run_check(
                checks,
                CHECK_NAMES[30],
                p31,
            )

            def p32():
                missing_parent = root / (
                    "p32_missing_parent"
                )

                final = missing_parent / (
                    "snapshot.json"
                )

                partial = Path(
                    str(
                        final
                    )
                    + ".partial"
                )

                rejected = expect_write_rejection(
                    persistence,
                    nonempty_snapshot,
                    final,
                )

                return (
                    rejected
                    and not missing_parent.exists()
                    and not final.exists()
                    and not partial.exists()
                )

            run_check(
                checks,
                CHECK_NAMES[31],
                p32,
            )

            def p33():
                final = root / (
                    "p33_existing_final.json"
                )

                sentinel = (
                    b"OPENMIND_P33_FINAL_SENTINEL"
                )

                write_candidate(
                    final,
                    sentinel,
                )

                before = sha256_file(
                    final
                )

                rejected = expect_write_rejection(
                    persistence,
                    nonempty_snapshot,
                    final,
                )

                after = sha256_file(
                    final
                )

                return (
                    rejected
                    and before == after
                    and final.read_bytes()
                    == sentinel
                )

            run_check(
                checks,
                CHECK_NAMES[32],
                p33,
            )

            def p34():
                final = root / (
                    "p34_final.json"
                )

                partial = Path(
                    str(
                        final
                    )
                    + ".partial"
                )

                sentinel = (
                    b"OPENMIND_P34_PARTIAL_SENTINEL"
                )

                write_candidate(
                    partial,
                    sentinel,
                )

                before = sha256_file(
                    partial
                )

                rejected = expect_write_rejection(
                    persistence,
                    nonempty_snapshot,
                    final,
                )

                after = sha256_file(
                    partial
                )

                shared[
                    "p34_ok"
                ] = (
                    rejected
                    and before == after
                    and partial.read_bytes()
                    == sentinel
                    and not final.exists()
                )

                return shared[
                    "p34_ok"
                ]

            run_check(
                checks,
                CHECK_NAMES[33],
                p34,
            )

            run_check(
                checks,
                CHECK_NAMES[34],
                lambda: (
                    static[
                        "exclusive_create"
                    ]
                    and shared.get(
                        "p34_ok"
                    )
                    is True
                ),
            )

            def p36():
                final = shared.get(
                    "positive_final"
                )

                if final is None:
                    return False

                raw = final.read_bytes()

                return (
                    static[
                        "write_loop"
                    ]
                    and raw
                    == independent_file_bytes
                    and len(
                        raw
                    )
                    == len(
                        independent_file_bytes
                    )
                )

            run_check(
                checks,
                CHECK_NAMES[35],
                p36,
            )

            def p37():
                final = shared.get(
                    "positive_final"
                )

                return (
                    final is not None
                    and final.is_file()
                    and static[
                        "hardlink_exact_once"
                    ]
                    and static[
                        "hardlink_no_follow"
                    ]
                    and static[
                        "no_replace_or_rename"
                    ]
                )

            run_check(
                checks,
                CHECK_NAMES[36],
                p37,
            )

            def p38():
                race = run_race_fixture(
                    model,
                    persistence,
                    root,
                )

                shared[
                    "race"
                ] = race

                status = race[
                    "child_status"
                ]

                return (
                    race[
                        "observed_partial_before_final"
                    ]
                    and status.get(
                        "ok"
                    )
                    is False
                    and status.get(
                        "type"
                    )
                    == "TelemetrySnapshotPersistenceWriteError"
                    and race[
                        "final_sha_before"
                    ]
                    == race[
                        "final_sha_after"
                    ]
                    and race[
                        "partial_exists"
                    ]
                )

            run_check(
                checks,
                CHECK_NAMES[37],
                p38,
            )

            run_check(
                checks,
                CHECK_NAMES[38],
                lambda: (
                    static[
                        "directory_fsync_order"
                    ]
                    and len(
                        static[
                            "directory_fsync_lines"
                        ]
                    )
                    == 2
                    and static[
                        "link_lines"
                    ][
                        0
                    ]
                    < static[
                        "directory_fsync_lines"
                    ][
                        0
                    ]
                ),
            )

            def p40():
                final = shared.get(
                    "positive_final"
                )

                if final is None:
                    return False

                partial = Path(
                    str(
                        final
                    )
                    + ".partial"
                )

                return (
                    final.is_file()
                    and not partial.exists()
                    and static[
                        "directory_fsync_order"
                    ]
                )

            run_check(
                checks,
                CHECK_NAMES[39],
                p40,
            )

            def p41():
                race = shared.get(
                    "race"
                )

                if race is None:
                    return False

                return (
                    race[
                        "partial_exists"
                    ]
                    and race[
                        "partial_bytes"
                    ]
                    == race[
                        "expected_partial_bytes"
                    ]
                )

            run_check(
                checks,
                CHECK_NAMES[40],
                p41,
            )

            def p42():
                final = shared.get(
                    "positive_final"
                )

                if final is None:
                    return False

                before = sha256_file(
                    final
                )

                rejected = expect_write_rejection(
                    persistence,
                    nonempty_snapshot,
                    final,
                )

                after = sha256_file(
                    final
                )

                return (
                    static[
                        "no_update_api"
                    ]
                    and rejected
                    and before == after
                )

            run_check(
                checks,
                CHECK_NAMES[41],
                p42,
            )

            def p43():
                first = make_nonempty_snapshot(
                    model
                )

                second = make_nonempty_snapshot(
                    model
                )

                first_payload = model.snapshot_payload(
                    first
                )

                second_payload = model.snapshot_payload(
                    second
                )

                first_sha = model.snapshot_sha256(
                    first
                )

                second_sha = model.snapshot_sha256(
                    second
                )

                first_envelope = persistence.snapshot_file_payload(
                    first
                )

                second_envelope = persistence.snapshot_file_payload(
                    second
                )

                first_bytes = persistence.snapshot_file_bytes(
                    first
                )

                second_bytes = persistence.snapshot_file_bytes(
                    second
                )

                first_file_sha = persistence.snapshot_file_sha256(
                    first
                )

                second_file_sha = persistence.snapshot_file_sha256(
                    second
                )

                return (
                    first_payload
                    == second_payload
                    and first_sha
                    == second_sha
                    and first_envelope
                    == second_envelope
                    and first_bytes
                    == second_bytes
                    and first_file_sha
                    == second_file_sha
                )

            run_check(
                checks,
                CHECK_NAMES[42],
                p43,
            )

            def p44():
                read_result = shared.get(
                    "positive_read"
                )

                if read_result is None:
                    return False

                cls = persistence.TelemetrySnapshotReadResult

                dataclass_params = getattr(
                    cls,
                    "__dataclass_params__",
                    None,
                )

                return (
                    isinstance(
                        read_result,
                        cls,
                    )
                    and dataclass_params
                    is not None
                    and dataclass_params.frozen
                    is True
                    and hasattr(
                        cls,
                        "__slots__",
                    )
                    and model.snapshot_payload(
                        read_result.snapshot
                    )
                    == expected_snapshot_payload
                    and read_result.snapshot_sha256
                    == expected_snapshot_sha
                    and read_result.file_sha256
                    == independent_file_sha
                    and read_result.byte_length
                    == len(
                        independent_file_bytes
                    )
                )

            run_check(
                checks,
                CHECK_NAMES[43],
                p44,
            )

            def p45():
                write_result = shared.get(
                    "positive_write"
                )

                final = shared.get(
                    "positive_final"
                )

                if (
                    write_result is None
                    or final is None
                ):
                    return False

                cls = persistence.TelemetrySnapshotWriteResult

                dataclass_params = getattr(
                    cls,
                    "__dataclass_params__",
                    None,
                )

                return (
                    isinstance(
                        write_result,
                        cls,
                    )
                    and dataclass_params
                    is not None
                    and dataclass_params.frozen
                    is True
                    and hasattr(
                        cls,
                        "__slots__",
                    )
                    and write_result.final_path
                    == str(
                        final
                    )
                    and write_result.snapshot_sha256
                    == expected_snapshot_sha
                    and write_result.file_sha256
                    == independent_file_sha
                    and write_result.byte_length
                    == len(
                        independent_file_bytes
                    )
                )

            run_check(
                checks,
                CHECK_NAMES[44],
                p45,
            )

        phase6c_after = sha256_file(
            PHASE6C_PATH
        )

        run_check(
            checks,
            CHECK_NAMES[45],
            lambda: (
                phase6c_before
                == PHASE6C_SHA256
                and phase6c_after
                == PHASE6C_SHA256
            ),
        )

        run_check(
            checks,
            CHECK_NAMES[46],
            lambda: (
                static[
                    "phase6c_not_imported"
                ]
                and static[
                    "no_runtime_surface"
                ]
            ),
        )

        run_check(
            checks,
            CHECK_NAMES[47],
            lambda: (
                static[
                    "no_repack_realization"
                ]
                and static[
                    "no_timing_api"
                ]
                and BENCHMARK_EXECUTED
                is False
                and PERFORMANCE_VERDICT
                is None
            ),
        )

        if len(
            checks
        ) != EXPECTED_CHECK_COUNT:
            raise HarnessInvalid(
                "validation check count mismatch"
            )

        if [
            item[
                "name"
            ]
            for item in checks
        ] != list(
            CHECK_NAMES
        ):
            raise HarnessInvalid(
                "validation check identity mismatch"
            )

        failed_checks = [
            item[
                "name"
            ]
            for item in checks
            if item[
                "pass"
            ]
            is not True
        ]

        result[
            "checks"
        ] = checks

        result[
            "failed_checks"
        ] = failed_checks

        result[
            "validation_valid"
        ] = True

        result[
            "all_pass"
        ] = (
            failed_checks
            == []
        )

        result[
            "fatal_error"
        ] = None

    except HarnessInvalid as exc:
        result[
            "checks"
        ] = checks

        result[
            "failed_checks"
        ] = [
            item[
                "name"
            ]
            for item in checks
            if item[
                "pass"
            ]
            is not True
        ]

        result[
            "validation_valid"
        ] = False

        result[
            "all_pass"
        ] = False

        result[
            "fatal_error"
        ] = (
            type(
                exc
            ).__name__
            + ": "
            + str(
                exc
            )
        )

    except Exception as exc:
        result[
            "checks"
        ] = checks

        result[
            "failed_checks"
        ] = [
            item[
                "name"
            ]
            for item in checks
            if item[
                "pass"
            ]
            is not True
        ]

        result[
            "validation_valid"
        ] = False

        result[
            "all_pass"
        ] = False

        result[
            "fatal_error"
        ] = (
            type(
                exc
            ).__name__
            + ": "
            + str(
                exc
            )
            + "\n"
            + traceback.format_exc()
        )

    write_result_atomic(
        result
    )

    print(
        "schema:",
        result[
            "schema"
        ],
    )

    print(
        "validation_valid:",
        result[
            "validation_valid"
        ],
    )

    print(
        "all_pass:",
        result[
            "all_pass"
        ],
    )

    print(
        "checks:",
        len(
            result[
                "checks"
            ]
        ),
    )

    print(
        "failed_checks:",
        result[
            "failed_checks"
        ],
    )

    print(
        "fatal_error:",
        result[
            "fatal_error"
        ],
    )

    print(
        "benchmark_executed:",
        result[
            "benchmark_executed"
        ],
    )

    print(
        "performance_verdict:",
        result[
            "performance_verdict"
        ],
    )

    if result[
        "validation_valid"
    ] is not True:
        return 2

    if result[
        "all_pass"
    ] is not True:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
