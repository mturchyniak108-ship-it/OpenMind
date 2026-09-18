#!/usr/bin/env python3

# Phase 6D Telemetry Snapshot Persistence Validation V1.1
# FROZEN VALIDATION RUNNER.
# Scientific execution is forbidden while CANDIDATE_COMPLETE is False.

from pathlib import Path
import ast
import copy
import ctypes
import errno
import hashlib
import importlib
import json
import os
import stat
import sys
import tempfile
import traceback


sys.dont_write_bytecode = True


CANDIDATE_COMPLETE = True

RESULT_SCHEMA = (
    "openmind.maf_segment_locality."
    "telemetry_snapshot_persistence_validation.v1_1"
)

EXPECTED_CHECK_COUNT = 57

CHECK_NAMES = ['V01_frozen_predecessor_binding', 'V02_platform_successor_identity', 'V03_file_schema_unchanged', 'V04_envelope_key_set_unchanged', 'V05_snapshot_payload_unchanged', 'V06_snapshot_sha_unchanged', 'V07_canonical_file_bytes', 'V08_no_trailing_newline', 'V09_file_sha256', 'V10_strict_reader_semantics_unchanged', 'V11_symlink_read_rejection', 'V12_nonregular_read_rejection', 'V13_no_reader_repair_or_fallback', 'V14_parent_directory_required', 'V15_existing_final_preflight_refusal', 'V16_existing_partial_preflight_refusal', 'V17_exact_partial_path', 'V18_partial_exclusive_creation', 'V19_complete_partial_write', 'V20_partial_file_fsync_before_publication', 'V21_ctypes_standard_library_backend', 'V22_libc_load_use_errno', 'V23_renameat2_symbol_required', 'V24_exact_renameat2_abi_binding', 'V25_rename_noreplace_exact_value', 'V26_parent_directory_fd', 'V27_same_directory_relative_names', 'V28_exact_renameat2_publication', 'V29_publication_success_return', 'V30_success_consumes_partial_name', 'V31_success_final_regular_file', 'V32_success_inode_identity_preserved', 'V33_atomic_no_replace_collision', 'V34_collision_final_preserved', 'V35_collision_partial_preserved', 'V36_parent_directory_fsync_after_success', 'V37_failure_residue_preservation', 'V38_no_success_partial_unlink', 'V39_no_os_link', 'V40_no_posix_link', 'V41_no_symlink_publication', 'V42_no_replace_or_plain_rename_fallback', 'V43_no_shell_or_subprocess_publication', 'V44_no_libc_hardlink_fallback', 'V45_backend_unavailable_explicit_failure', 'V46_error_surface_distinction', 'V47_write_result_contract', 'V48_read_result_contract', 'V49_serialization_determinism', 'V50_source_authority_immutability', 'V51_phase6c_immutability_and_no_integration', 'V52_no_repack_or_generation_activation', 'V53_no_phase6e_performance_or_network', 'V54_v1_lineage_preserved', 'V55_successor_validation_exact_once', 'V56_dynamic_android_backend_validation', 'V57_no_replace_validation_without_timing_race']

PERSISTENCE_PROTOCOL_PATH = Path(
    "experiments/model_fractal/"
    "MAF_SEGMENT_LOCALITY_TELEMETRY_SNAPSHOT_PERSISTENCE_V1_1_PROTOCOL.md"
)

PERSISTENCE_PROTOCOL_SHA256 = (
    "511c995fd86998da33e47691db98794ddcda9e51ec3fd71794a2324ef2a53bba"
)

PERSISTENCE_PATH = Path(
    "experiments/model_fractal/"
    "maf_segment_locality_telemetry_snapshot_persistence_v1_1.py"
)

PERSISTENCE_SHA256 = (
    "cb1e2e3dc11006c75e38e33c941b39959aa4d99f971de9e08250d8b995fe09b0"
)

PERSISTENCE_V1_PROTOCOL_PATH = Path(
    "experiments/model_fractal/"
    "MAF_SEGMENT_LOCALITY_TELEMETRY_SNAPSHOT_PERSISTENCE_V1_PROTOCOL.md"
)

PERSISTENCE_V1_PROTOCOL_SHA256 = (
    "0e08a8a18a45a16eddc05927b8191d73ca9fc7453cb97fc1140e5e243e03db51"
)

PERSISTENCE_V1_PATH = Path(
    "experiments/model_fractal/"
    "maf_segment_locality_telemetry_snapshot_persistence_v1.py"
)

PERSISTENCE_V1_SHA256 = (
    "4a7c8ba1e1d7e9e4004a16d54464f17fd07ba75cc84ddea25403697d53d0581c"
)

VALIDATION_PROTOCOL_PATH = Path(
    "experiments/model_fractal/"
    "MAF_SEGMENT_LOCALITY_TELEMETRY_SNAPSHOT_PERSISTENCE_VALIDATION_V1_1_PROTOCOL.md"
)

VALIDATION_PROTOCOL_SHA256 = (
    "13cf1798492853be098b6e8ea31d9b0fbaf0a047f425bd2fdda91bae34ad2841"
)

PERSISTENCE_V1_VALIDATION_PROTOCOL_PATH = Path(
    "experiments/model_fractal/"
    "MAF_SEGMENT_LOCALITY_TELEMETRY_SNAPSHOT_PERSISTENCE_VALIDATION_V1_PROTOCOL.md"
)

PERSISTENCE_V1_VALIDATION_PROTOCOL_SHA256 = (
    "7c79cf2eb97e98c14fb0acbd947ca30a8e46746eba1bd2b0127375ac01b8b9a5"
)

PERSISTENCE_V1_VALIDATION_RUNNER_PATH = Path(
    "experiments/model_fractal/"
    "maf_segment_locality_telemetry_snapshot_persistence_validation_v1.py"
)

PERSISTENCE_V1_VALIDATION_RUNNER_SHA256 = (
    "27939c9524fa351af9b1b99910902c951abb1a36d00dbabc07171624515541c7"
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
    "maf_segment_locality_telemetry_snapshot_persistence_validation_v1_1.json"
)

RESULT_TEMP_PATH = Path(
    str(RESULT_PATH)
    + ".tmp"
)

PERSISTENCE_V1_RESULT_PATH = Path(
    "experiments/model_fractal/"
    "maf_segment_locality_telemetry_snapshot_persistence_validation_v1.json"
)

PERSISTENCE_V1_RESULT_TEMP_PATH = Path(
    str(PERSISTENCE_V1_RESULT_PATH)
    + ".tmp"
)

FILE_SCHEMA = (
    "openmind.maf_segment_locality."
    "telemetry_snapshot_file.v1"
)

BENCHMARK_EXECUTED = False
PERFORMANCE_VERDICT = None

RESULT_RENAME_NOREPLACE = 1

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


class AuditorError(
    Exception
):
    """Validation-harness/auditor defect; never a scientific FAIL."""


class HarnessInvalid(
    AuditorError
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

def _exception_trace_paths(
    exc,
):
    result = []

    tb = exc.__traceback__

    while tb is not None:
        try:
            filename = str(
                Path(
                    tb.tb_frame.f_code.co_filename
                ).resolve()
            )

        except Exception:
            filename = (
                tb.tb_frame.f_code.co_filename
            )

        result.append(
            filename
        )

        tb = tb.tb_next

    return result


def exception_touches_scientific_target(
    exc,
):
    target_paths = {
        str(
            (
                REPO_ROOT
                / PERSISTENCE_PATH
            ).resolve()
        ),
        str(
            (
                REPO_ROOT
                / DATA_MODEL_PATH
            ).resolve()
        ),
    }

    return any(
        frame_path
        in target_paths
        for frame_path
        in _exception_trace_paths(
            exc
        )
    )


def run_check(
    checks,
    name,
    fn,
):
    try:
        outcome = fn()

    except AuditorError:
        raise

    except Exception as exc:
        if not exception_touches_scientific_target(
            exc
        ):
            raise AuditorError(
                "unexpected validation-harness exception in "
                + name
                + ": "
                + type(
                    exc
                ).__name__
                + ": "
                + str(
                    exc
                )
            ) from exc

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

                "origin":
                    "scientific_target",
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


def _write_all_fd(
    fd,
    data,
):
    view = memoryview(
        data
    )

    offset = 0

    while offset < len(
        view
    ):
        written = os.write(
            fd,
            view[offset:],
        )

        if written <= 0:
            raise HarnessInvalid(
                "short harness write"
            )

        offset += written


def _fsync_directory_harness(
    directory,
):
    flags = os.O_RDONLY

    if hasattr(
        os,
        "O_DIRECTORY",
    ):
        flags |= os.O_DIRECTORY

    fd = os.open(
        directory,
        flags,
    )

    try:
        os.fsync(
            fd
        )

    finally:
        os.close(
            fd
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
            PERSISTENCE_V1_PROTOCOL_PATH,
            PERSISTENCE_V1_PROTOCOL_SHA256,
        ),
        (
            PERSISTENCE_V1_PATH,
            PERSISTENCE_V1_SHA256,
        ),
        (
            VALIDATION_PROTOCOL_PATH,
            VALIDATION_PROTOCOL_SHA256,
        ),
        (
            PERSISTENCE_V1_VALIDATION_PROTOCOL_PATH,
            PERSISTENCE_V1_VALIDATION_PROTOCOL_SHA256,
        ),
        (
            PERSISTENCE_V1_VALIDATION_RUNNER_PATH,
            PERSISTENCE_V1_VALIDATION_RUNNER_SHA256,
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

    for path, expected_sha in expected:
        if not path.is_file():
            raise HarnessInvalid(
                "frozen authority missing: "
                + str(path)
            )

        actual = sha256_file(
            path
        )

        if actual != expected_sha:
            raise HarnessInvalid(
                "frozen authority SHA mismatch: "
                + str(path)
            )

    for path in (
        RESULT_PATH,
        RESULT_TEMP_PATH,
        PERSISTENCE_V1_RESULT_PATH,
        PERSISTENCE_V1_RESULT_TEMP_PATH,
    ):
        if (
            path.exists()
            or path.is_symlink()
        ):
            raise HarnessInvalid(
                "validation slot residue already exists: "
                + str(path)
            )


def reserve_result_slot():
    marker = (
        RESULT_SCHEMA
        + "|slot-reserved-v1\n"
    ).encode(
        "utf-8"
    )

    flags = (
        os.O_WRONLY
        | os.O_CREAT
        | os.O_EXCL
    )

    if hasattr(
        os,
        "O_NOFOLLOW",
    ):
        flags |= os.O_NOFOLLOW

    fd = os.open(
        RESULT_TEMP_PATH,
        flags,
        0o600,
    )

    opened = False

    try:
        opened = True

        st = os.fstat(
            fd
        )

        if not stat.S_ISREG(
            st.st_mode
        ):
            raise HarnessInvalid(
                "reserved result temp is not regular"
            )

        _write_all_fd(
            fd,
            marker,
        )

        os.fsync(
            fd
        )

    finally:
        if opened:
            os.close(
                fd
            )

    _fsync_directory_harness(
        RESULT_TEMP_PATH.parent
    )


def _load_result_renameat2():
    try:
        libc = ctypes.CDLL(
            None,
            use_errno=True,
        )

    except Exception as exc:
        raise HarnessInvalid(
            "result publisher libc load failed: "
            + type(exc).__name__
            + ": "
            + str(exc)
        ) from exc

    try:
        renameat2 = libc.renameat2

    except AttributeError as exc:
        raise HarnessInvalid(
            "result publisher requires libc renameat2"
        ) from exc

    renameat2.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    ]

    renameat2.restype = ctypes.c_int

    return renameat2


def _publish_result_noreplace():
    parent = RESULT_PATH.parent

    flags = os.O_RDONLY

    if hasattr(
        os,
        "O_DIRECTORY",
    ):
        flags |= os.O_DIRECTORY

    parent_fd = os.open(
        parent,
        flags,
    )

    error = None

    try:
        renameat2 = (
            _load_result_renameat2()
        )

        ctypes.set_errno(
            0
        )

        rc = renameat2(
            parent_fd,
            os.fsencode(
                RESULT_TEMP_PATH.name
            ),
            parent_fd,
            os.fsencode(
                RESULT_PATH.name
            ),
            RESULT_RENAME_NOREPLACE,
        )

        if rc != 0:
            err = ctypes.get_errno()

            if err == errno.EEXIST:
                raise HarnessInvalid(
                    "authoritative result appeared before "
                    "no-replace result publication"
                )

            raise HarnessInvalid(
                "result renameat2 publication failed: errno "
                + str(err)
            )

        os.fsync(
            parent_fd
        )

    except Exception as exc:
        error = exc

    try:
        os.close(
            parent_fd
        )

    except Exception as exc:
        if error is None:
            error = exc

    if error is not None:
        raise error


def independent_result_bytes(
    result,
):
    return json.dumps(
        result,
        sort_keys=True,
        separators=(
            ",",
            ":",
        ),
        ensure_ascii=False,
        allow_nan=False,
    ).encode(
        "utf-8"
    )


def write_reserved_result(
    result,
):
    if not RESULT_TEMP_PATH.exists():
        raise HarnessInvalid(
            "reserved result temp is absent"
        )

    data = independent_result_bytes(
        result
    )

    flags = os.O_WRONLY

    if hasattr(
        os,
        "O_NOFOLLOW",
    ):
        flags |= os.O_NOFOLLOW

    fd = os.open(
        RESULT_TEMP_PATH,
        flags,
    )

    try:
        st = os.fstat(
            fd
        )

        if not stat.S_ISREG(
            st.st_mode
        ):
            raise HarnessInvalid(
                "reserved result temp ceased to be regular"
            )

        os.ftruncate(
            fd,
            0,
        )

        os.lseek(
            fd,
            0,
            os.SEEK_SET,
        )

        _write_all_fd(
            fd,
            data,
        )

        os.fsync(
            fd
        )

    finally:
        os.close(
            fd
        )

    _publish_result_noreplace()


def import_exact(
    module_name,
):
    if not module_name.startswith(
        "experiments.model_fractal."
    ):
        raise HarnessInvalid(
            "unexpected scientific module namespace"
        )

    return importlib.import_module(
        module_name
    )


def runner_static_evidence():
    path = Path(
        __file__
    )

    source = path.read_text(
        encoding="utf-8"
    )

    tree = ast.parse(
        source,
        filename=str(path),
    )

    return {
        "source":
            source,

        "tree":
            tree,

        "sha256":
            hashlib.sha256(
                source.encode(
                    "utf-8"
                )
            ).hexdigest(),
    }


def target_static_evidence():
    source = PERSISTENCE_PATH.read_text(
        encoding="utf-8"
    )

    tree = ast.parse(
        source,
        filename=str(
            PERSISTENCE_PATH
        ),
    )

    return {
        "source":
            source,

        "tree":
            tree,

        "sha256":
            hashlib.sha256(
                source.encode(
                    "utf-8"
                )
            ).hexdigest(),
    }


def base_result():
    return {
        "schema":
            RESULT_SCHEMA,

        "validation_valid":
            False,

        "all_pass":
            False,

        "check_count":
            EXPECTED_CHECK_COUNT,

        "checks":
            [],

        "failed_checks":
            [],

        "fatal_error":
            None,

        "auditor_error":
            None,

        "benchmark_executed":
            BENCHMARK_EXECUTED,

        "performance_verdict":
            PERFORMANCE_VERDICT,

        "target_protocol_sha256":
            PERSISTENCE_PROTOCOL_SHA256,

        "target_implementation_sha256":
            PERSISTENCE_SHA256,

        "validation_protocol_sha256":
            VALIDATION_PROTOCOL_SHA256,

        "platform":
            sys.platform,
    }


def run_scientific_checks(
    *,
    persistence,
    model,
    runner_evidence,
    target_evidence,
):
    checks = []
    shared = {}

    runner_source = runner_evidence[
        "source"
    ]
    runner_tree = runner_evidence[
        "tree"
    ]

    target_source = target_evidence[
        "source"
    ]
    target_tree = target_evidence[
        "tree"
    ]

    phase6c_before = sha256_file(
        PHASE6C_PATH
    )

    source_snapshot = make_nonempty_snapshot(
        model
    )

    source_payload_before = copy.deepcopy(
        model.snapshot_payload(
            source_snapshot
        )
    )

    source_sha_before = model.snapshot_sha256(
        source_snapshot
    )

    empty_snapshot = make_empty_snapshot(
        model
    )

    envelope = persistence.snapshot_file_payload(
        source_snapshot
    )

    expected_snapshot_payload = model.snapshot_payload(
        source_snapshot
    )

    expected_snapshot_sha = model.snapshot_sha256(
        source_snapshot
    )

    target_file_bytes = persistence.snapshot_file_bytes(
        source_snapshot
    )

    independent_file_bytes = independent_canonical_json_bytes(
        envelope
    )

    independent_file_sha = hashlib.sha256(
        independent_file_bytes
    ).hexdigest()

    def dotted(
        node,
    ):
        if isinstance(
            node,
            ast.Name,
        ):
            return node.id

        if isinstance(
            node,
            ast.Attribute,
        ):
            prefix = dotted(
                node.value
            )

            if prefix:
                return (
                    prefix
                    + "."
                    + node.attr
                )

            return node.attr

        return ""

    def function_node(
        tree,
        name,
    ):
        matches = [
            node
            for node in tree.body
            if (
                isinstance(
                    node,
                    (
                        ast.FunctionDef,
                        ast.AsyncFunctionDef,
                    ),
                )
                and node.name == name
            )
        ]

        if len(
            matches
        ) != 1:
            raise HarnessInvalid(
                "function surface mismatch: "
                + name
            )

        return matches[
            0
        ]

    def function_source(
        tree,
        source_text,
        name,
    ):
        node = function_node(
            tree,
            name,
        )

        segment = ast.get_source_segment(
            source_text,
            node,
        )

        if segment is None:
            raise HarnessInvalid(
                "source extraction failed: "
                + name
            )

        return segment

    def calls_named(
        node,
        path,
    ):
        return [
            item
            for item in ast.walk(
                node
            )
            if (
                isinstance(
                    item,
                    ast.Call,
                )
                and dotted(
                    item.func
                )
                == path
            )
        ]

    def call_lines(
        node,
        path,
    ):
        return sorted(
            item.lineno
            for item in calls_named(
                node,
                path,
            )
        )

    def imported_roots(
        tree,
    ):
        roots = set()

        for node in tree.body:
            if isinstance(
                node,
                ast.Import,
            ):
                for alias in node.names:
                    roots.add(
                        alias.name.split(
                            ".",
                            1,
                        )[0]
                    )

            elif isinstance(
                node,
                ast.ImportFrom,
            ):
                if node.module:
                    roots.add(
                        node.module.split(
                            ".",
                            1,
                        )[0]
                    )

        return roots

    def stat_key(
        path,
    ):
        st = os.lstat(
            path
        )

        return (
            st.st_dev,
            st.st_ino,
            st.st_mode,
            st.st_size,
        )

    def regular_not_symlink(
        path,
    ):
        st = os.lstat(
            path
        )

        return (
            stat.S_ISREG(
                st.st_mode
            )
            and not stat.S_ISLNK(
                st.st_mode
            )
        )

    target_writer = function_node(
        target_tree,
        "write_snapshot_file",
    )

    target_publisher = function_node(
        target_tree,
        "_publish_snapshot_noreplace",
    )

    target_loader = function_node(
        target_tree,
        "_load_renameat2_backend",
    )

    target_writer_source = function_source(
        target_tree,
        target_source,
        "write_snapshot_file",
    )

    target_publisher_source = function_source(
        target_tree,
        target_source,
        "_publish_snapshot_noreplace",
    )

    target_loader_source = function_source(
        target_tree,
        target_source,
        "_load_renameat2_backend",
    )

    runner_main = function_node(
        runner_tree,
        "main",
    )

    runner_binding = function_node(
        runner_tree,
        "binding_gate",
    )

    runner_reserve = function_node(
        runner_tree,
        "reserve_result_slot",
    )

    runner_result_publisher = function_node(
        runner_tree,
        "_publish_result_noreplace",
    )

    runner_binding_source = function_source(
        runner_tree,
        runner_source,
        "binding_gate",
    )

    runner_reserve_source = function_source(
        runner_tree,
        runner_source,
        "reserve_result_slot",
    )

    runner_result_publisher_source = function_source(
        runner_tree,
        runner_source,
        "_publish_result_noreplace",
    )

    with tempfile.TemporaryDirectory(
        prefix=(
            "openmind_persistence_validation_v1_1_"
        )
    ) as temp_root_s:
        root = Path(
            temp_root_s
        )

        def v01():
            expected = {
                str(
                    PERSISTENCE_PROTOCOL_PATH
                ):
                    PERSISTENCE_PROTOCOL_SHA256,

                str(
                    PERSISTENCE_PATH
                ):
                    PERSISTENCE_SHA256,

                str(
                    PERSISTENCE_V1_PROTOCOL_PATH
                ):
                    PERSISTENCE_V1_PROTOCOL_SHA256,

                str(
                    PERSISTENCE_V1_PATH
                ):
                    PERSISTENCE_V1_SHA256,

                str(
                    VALIDATION_PROTOCOL_PATH
                ):
                    VALIDATION_PROTOCOL_SHA256,

                str(
                    PERSISTENCE_V1_VALIDATION_PROTOCOL_PATH
                ):
                    PERSISTENCE_V1_VALIDATION_PROTOCOL_SHA256,

                str(
                    PERSISTENCE_V1_VALIDATION_RUNNER_PATH
                ):
                    PERSISTENCE_V1_VALIDATION_RUNNER_SHA256,

                str(
                    DATA_MODEL_PATH
                ):
                    DATA_MODEL_SHA256,

                str(
                    DATA_MODEL_RESULT_PATH
                ):
                    DATA_MODEL_RESULT_SHA256,

                str(
                    DATA_MODEL_VERDICT_PATH
                ):
                    DATA_MODEL_VERDICT_SHA256,

                str(
                    PHASE6C_PATH
                ):
                    PHASE6C_SHA256,
            }

            actual = {
                path:
                    sha256_file(
                        Path(
                            path
                        )
                    )
                for path in expected
            }

            return (
                actual
                == expected,
                actual,
            )

        run_check(
            checks,
            CHECK_NAMES[0],
            v01,
        )

        def v02():
            top_level_calls = []

            for node in target_tree.body:
                if isinstance(
                    node,
                    (
                        ast.FunctionDef,
                        ast.AsyncFunctionDef,
                        ast.ClassDef,
                    ),
                ):
                    continue

                for item in ast.walk(
                    node
                ):
                    if isinstance(
                        item,
                        ast.Call,
                    ):
                        top_level_calls.append(
                            (
                                item.lineno,
                                dotted(
                                    item.func
                                ),
                            )
                        )

            return (
                (
                    persistence.PERSISTENCE_PROTOCOL_SHA256
                    == PERSISTENCE_PROTOCOL_SHA256
                    and persistence.PERSISTENCE_V1_PROTOCOL_SHA256
                    == PERSISTENCE_V1_PROTOCOL_SHA256
                    and persistence.PERSISTENCE_V1_IMPLEMENTATION_SHA256
                    == PERSISTENCE_V1_SHA256
                    and persistence.PERSISTENCE_V1_VALIDATION_PROTOCOL_SHA256
                    == PERSISTENCE_V1_VALIDATION_PROTOCOL_SHA256
                    and persistence.PERSISTENCE_V1_VALIDATION_RUNNER_SHA256
                    == PERSISTENCE_V1_VALIDATION_RUNNER_SHA256
                    and not PERSISTENCE_V1_RESULT_PATH.exists()
                    and not PERSISTENCE_V1_RESULT_TEMP_PATH.exists()
                    and [
                        name
                        for _, name
                        in top_level_calls
                    ]
                    == [
                        "frozenset"
                    ]
                ),
                {
                    "target_protocol":
                        persistence.PERSISTENCE_PROTOCOL_SHA256,

                    "v1_result_absent":
                        not PERSISTENCE_V1_RESULT_PATH.exists(),

                    "v1_result_temp_absent":
                        not PERSISTENCE_V1_RESULT_TEMP_PATH.exists(),

                    "target_top_level_calls":
                        top_level_calls,
                },
            )

        run_check(
            checks,
            CHECK_NAMES[1],
            v02,
        )

        def v03():
            return (
                persistence.SNAPSHOT_FILE_SCHEMA
                == FILE_SCHEMA
            )

        run_check(
            checks,
            CHECK_NAMES[2],
            v03,
        )

        def v04():
            return (
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
            )

        run_check(
            checks,
            CHECK_NAMES[3],
            v04,
        )

        def v05():
            return (
                envelope[
                    "snapshot"
                ]
                == expected_snapshot_payload
            )

        run_check(
            checks,
            CHECK_NAMES[4],
            v05,
        )

        def v06():
            return (
                envelope[
                    "snapshot_sha256"
                ]
                == expected_snapshot_sha
            )

        run_check(
            checks,
            CHECK_NAMES[5],
            v06,
        )

        def v07():
            return (
                target_file_bytes
                == independent_file_bytes
            )

        run_check(
            checks,
            CHECK_NAMES[6],
            v07,
        )

        def v08():
            return (
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
            )

        run_check(
            checks,
            CHECK_NAMES[7],
            v08,
        )

        def v09():
            final = root / (
                "v09_file_sha.json"
            )

            write_result = persistence.write_snapshot_file(
                source_snapshot,
                final,
            )

            read_result = persistence.read_snapshot_file(
                final
            )

            return (
                (
                    persistence.snapshot_file_sha256(
                        source_snapshot
                    )
                    == independent_file_sha
                    and write_result.file_sha256
                    == independent_file_sha
                    and read_result.file_sha256
                    == independent_file_sha
                    and write_result.snapshot_sha256
                    == expected_snapshot_sha
                    and read_result.snapshot_sha256
                    == expected_snapshot_sha
                    and independent_file_sha
                    != expected_snapshot_sha
                ),
                {
                    "snapshot_sha256":
                        expected_snapshot_sha,

                    "file_sha256":
                        independent_file_sha,
                },
            )

        run_check(
            checks,
            CHECK_NAMES[8],
            v09,
        )

        def v10():
            outcomes = []

            for label, snapshot in (
                (
                    "empty",
                    empty_snapshot,
                ),
                (
                    "nonempty",
                    source_snapshot,
                ),
            ):
                final = root / (
                    "v10_valid_"
                    + label
                    + ".json"
                )

                persistence.write_snapshot_file(
                    snapshot,
                    final,
                )

                read_result = persistence.read_snapshot_file(
                    final
                )

                outcomes.append(
                    model.snapshot_payload(
                        read_result.snapshot
                    )
                    == model.snapshot_payload(
                        snapshot
                    )
                )

            raw_cases = [
                (
                    "invalid_utf8",
                    b"\xff\xfe\x80",
                ),
                (
                    "invalid_json",
                    b'{"schema":',
                ),
                (
                    "duplicate_key",
                    b'{"schema":"a","schema":"b"}',
                ),
            ]

            noncanonical = json.dumps(
                envelope,
                sort_keys=True,
                ensure_ascii=False,
                indent=2,
            ).encode(
                "utf-8"
            )

            raw_cases.append(
                (
                    "noncanonical",
                    noncanonical,
                )
            )

            for label, raw in raw_cases:
                path = root / (
                    "v10_"
                    + label
                    + ".json"
                )

                write_candidate(
                    path,
                    raw,
                )

                outcomes.append(
                    expect_read_rejection(
                        persistence,
                        path,
                    )
                )

            mutations = []

            extra = copy.deepcopy(
                envelope
            )
            extra[
                "unexpected"
            ] = 1
            mutations.append(
                (
                    "unknown_envelope",
                    extra,
                )
            )

            for key in (
                "schema",
                "snapshot_sha256",
                "snapshot",
            ):
                item = copy.deepcopy(
                    envelope
                )
                del item[
                    key
                ]
                mutations.append(
                    (
                        "missing_"
                        + key,
                        item,
                    )
                )

            wrong_schema = copy.deepcopy(
                envelope
            )
            wrong_schema[
                "schema"
            ] = (
                FILE_SCHEMA
                + ".wrong"
            )
            mutations.append(
                (
                    "wrong_schema",
                    wrong_schema,
                )
            )

            for index, value in enumerate(
                (
                    "A" * 64,
                    "a" * 63,
                    "a" * 65,
                    "g" * 64,
                ),
                start=1,
            ):
                item = copy.deepcopy(
                    envelope
                )
                item[
                    "snapshot_sha256"
                ] = value
                mutations.append(
                    (
                        "bad_sha_"
                        + str(
                            index
                        ),
                        item,
                    )
                )

            mismatch = copy.deepcopy(
                envelope
            )
            mismatch[
                "snapshot_sha256"
            ] = (
                "0" * 64
                if expected_snapshot_sha
                != "0" * 64
                else "1" * 64
            )
            mutations.append(
                (
                    "sha_mismatch",
                    mismatch,
                )
            )

            payload_mutation = copy.deepcopy(
                envelope
            )
            payload_mutation[
                "snapshot"
            ][
                "event_count"
            ] += 1
            mutations.append(
                (
                    "payload_mutation",
                    payload_mutation,
                )
            )

            malformed = copy.deepcopy(
                envelope
            )
            malformed[
                "snapshot"
            ][
                "object_aggregates"
            ] = {}
            mutations.append(
                (
                    "malformed_nested",
                    malformed,
                )
            )

            unknown_nested = copy.deepcopy(
                envelope
            )
            unknown_nested[
                "snapshot"
            ][
                "unknown_nested_field"
            ] = 1
            mutations.append(
                (
                    "unknown_nested",
                    unknown_nested,
                )
            )

            bool_integer = copy.deepcopy(
                envelope
            )
            bool_integer[
                "snapshot"
            ][
                "event_count"
            ] = True
            mutations.append(
                (
                    "bool_integer",
                    bool_integer,
                )
            )

            negative_integer = copy.deepcopy(
                envelope
            )
            negative_integer[
                "snapshot"
            ][
                "object_aggregates"
            ][
                0
            ][
                "bytes_read"
            ] = -1
            mutations.append(
                (
                    "negative_integer",
                    negative_integer,
                )
            )

            bad_pk = copy.deepcopy(
                envelope
            )
            bad_pk[
                "snapshot"
            ][
                "model_pk"
            ] = "bad-model-pk"
            mutations.append(
                (
                    "bad_pk",
                    bad_pk,
                )
            )

            invariant = copy.deepcopy(
                envelope
            )
            pref = invariant[
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
            mutations.append(
                (
                    "bad_invariant",
                    invariant,
                )
            )

            for label, candidate in mutations:
                path = root / (
                    "v10_"
                    + label
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

            return (
                all(
                    outcomes
                ),
                {
                    "cases":
                        len(
                            outcomes
                        ),

                    "all_rejected_or_valid":
                        all(
                            outcomes
                        ),
                },
            )

        run_check(
            checks,
            CHECK_NAMES[9],
            v10,
        )

        def v11():
            target = root / (
                "v11_target.json"
            )

            write_candidate(
                target,
                independent_file_bytes,
            )

            link = root / (
                "v11_link.json"
            )

            try:
                os.symlink(
                    target,
                    link,
                )

            except Exception as exc:
                raise HarnessInvalid(
                    "symlink capability unavailable: "
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
            CHECK_NAMES[10],
            v11,
        )

        def v12():
            path = root / (
                "v12_directory"
            )

            path.mkdir()

            return expect_read_rejection(
                persistence,
                path,
            )

        run_check(
            checks,
            CHECK_NAMES[11],
            v12,
        )

        def v13():
            reader = function_node(
                target_tree,
                "read_snapshot_file",
            )

            regular_read_calls = calls_named(
                reader,
                "_read_regular_file_bytes",
            )

            parse_calls = calls_named(
                reader,
                "_parse_canonical_envelope",
            )

            reader_forbidden_calls = []

            for name in (
                "partial_path_for",
                "write_snapshot_file",
                "_publish_snapshot_noreplace",
                "os.rename",
                "os.replace",
                "os.link",
            ):
                reader_forbidden_calls.extend(
                    calls_named(
                        reader,
                        name,
                    )
                )

            static_ok = (
                len(
                    regular_read_calls
                ) == 1
                and len(
                    regular_read_calls[
                        0
                    ].args
                ) == 1
                and ast.unparse(
                    regular_read_calls[
                        0
                    ].args[
                        0
                    ]
                )
                == "final_path"
                and len(
                    parse_calls
                ) == 1
                and reader_forbidden_calls
                == []
            )

            final = root / (
                "v13_final.json"
            )

            partial = persistence.partial_path_for(
                final
            )

            write_candidate(
                final,
                b"{bad-json",
            )

            write_candidate(
                partial,
                independent_file_bytes,
            )

            partial_sha_before = sha256_file(
                partial
            )

            malformed_rejected = expect_read_rejection(
                persistence,
                final,
            )

            partial_sha_after = sha256_file(
                partial
            )

            missing_final = root / (
                "v13_missing.json"
            )

            missing_partial = persistence.partial_path_for(
                missing_final
            )

            write_candidate(
                missing_partial,
                independent_file_bytes,
            )

            missing_rejected = expect_read_rejection(
                persistence,
                missing_final,
            )

            dynamic_ok = (
                malformed_rejected
                and missing_rejected
                and partial_sha_before
                == partial_sha_after
                and missing_partial.read_bytes()
                == independent_file_bytes
            )

            return (
                static_ok
                and dynamic_ok,
                {
                    "regular_read_calls":
                        [
                            item.lineno
                            for item
                            in regular_read_calls
                        ],

                    "parse_calls":
                        [
                            item.lineno
                            for item
                            in parse_calls
                        ],

                    "forbidden_reader_calls":
                        len(
                            reader_forbidden_calls
                        ),

                    "dynamic_rejection":
                        dynamic_ok,
                },
            )

        run_check(
            checks,
            CHECK_NAMES[12],
            v13,
        )

        def v14():
            parent = root / (
                "v14_missing_parent"
            )

            final = parent / (
                "snapshot.json"
            )

            rejected = expect_write_rejection(
                persistence,
                source_snapshot,
                final,
            )

            return (
                rejected
                and not parent.exists()
                and not final.exists()
                and not persistence.partial_path_for(
                    final
                ).exists()
            )

        run_check(
            checks,
            CHECK_NAMES[13],
            v14,
        )

        def v15():
            final = root / (
                "v15_existing_final.json"
            )

            partial = persistence.partial_path_for(
                final
            )

            sentinel = (
                b"OPENMIND_V15_FINAL_SENTINEL"
            )

            write_candidate(
                final,
                sentinel,
            )

            before_sha = sha256_file(
                final
            )
            before_stat = stat_key(
                final
            )

            rejected = expect_write_rejection(
                persistence,
                source_snapshot,
                final,
            )

            after_sha = sha256_file(
                final
            )
            after_stat = stat_key(
                final
            )

            return (
                rejected
                and before_sha
                == after_sha
                and before_stat
                == after_stat
                and final.read_bytes()
                == sentinel
                and not partial.exists()
            )

        run_check(
            checks,
            CHECK_NAMES[14],
            v15,
        )

        def v16():
            final = root / (
                "v16_final.json"
            )

            partial = persistence.partial_path_for(
                final
            )

            sentinel = (
                b"OPENMIND_V16_PARTIAL_SENTINEL"
            )

            write_candidate(
                partial,
                sentinel,
            )

            before_sha = sha256_file(
                partial
            )
            before_stat = stat_key(
                partial
            )

            rejected = expect_write_rejection(
                persistence,
                source_snapshot,
                final,
            )

            after_sha = sha256_file(
                partial
            )
            after_stat = stat_key(
                partial
            )

            ok = (
                rejected
                and before_sha
                == after_sha
                and before_stat
                == after_stat
                and partial.read_bytes()
                == sentinel
                and not final.exists()
            )

            shared[
                "v16_ok"
            ] = ok

            return ok

        run_check(
            checks,
            CHECK_NAMES[15],
            v16,
        )

        def v17():
            final = (
                root
                / "nested"
                / "snapshot.json"
            )

            expected = final.with_name(
                final.name
                + ".partial"
            )

            actual = persistence.partial_path_for(
                final
            )

            return (
                actual
                == expected
                and actual.parent
                == final.parent
            )

        run_check(
            checks,
            CHECK_NAMES[16],
            v17,
        )

        def v18():
            open_calls = calls_named(
                target_writer,
                "os.open",
            )

            partial_opens = [
                call
                for call in open_calls
                if (
                    len(
                        call.args
                    ) >= 2
                    and ast.unparse(
                        call.args[
                            0
                        ]
                    )
                    == "partial"
                )
            ]

            if len(
                partial_opens
            ) != 1:
                return (
                    False,
                    {
                        "partial_open_count":
                            len(
                                partial_opens
                            ),
                    },
                )

            flag_names = {
                dotted(
                    node
                )
                for node in ast.walk(
                    partial_opens[
                        0
                    ].args[
                        1
                    ]
                )
                if isinstance(
                    node,
                    ast.Attribute,
                )
            }

            return (
                (
                    "os.O_CREAT"
                    in flag_names
                    and "os.O_EXCL"
                    in flag_names
                    and shared.get(
                        "v16_ok"
                    )
                    is True
                ),
                {
                    "partial_open_flags":
                        sorted(
                            flag_names
                        ),

                    "dynamic_existing_partial_refusal":
                        shared.get(
                            "v16_ok"
                        ),
                },
            )

        run_check(
            checks,
            CHECK_NAMES[17],
            v18,
        )

        def v19():
            write_all_calls = calls_named(
                target_writer,
                "_write_all",
            )

            publish_calls = calls_named(
                target_writer,
                "_publish_snapshot_noreplace",
            )

            static_ok = False

            if (
                len(
                    write_all_calls
                ) == 1
                and len(
                    publish_calls
                ) == 1
                and len(
                    write_all_calls[
                        0
                    ].args
                ) == 2
            ):
                static_ok = (
                    ast.unparse(
                        write_all_calls[
                            0
                        ].args[
                            0
                        ]
                    )
                    == "fd"
                    and ast.unparse(
                        write_all_calls[
                            0
                        ].args[
                            1
                        ]
                    )
                    == "data"
                    and write_all_calls[
                        0
                    ].lineno
                    < publish_calls[
                        0
                    ].lineno
                )

            final = root / (
                "v19_complete_write.json"
            )

            result = persistence.write_snapshot_file(
                source_snapshot,
                final,
            )

            raw = final.read_bytes()

            dynamic_ok = (
                raw
                == independent_file_bytes
                and sha256_file(
                    final
                )
                == independent_file_sha
                and result.byte_length
                == len(
                    independent_file_bytes
                )
            )

            ok = (
                static_ok
                and dynamic_ok
            )

            shared[
                "v19_success"
            ] = ok

            return (
                ok,
                {
                    "write_all_lines":
                        [
                            item.lineno
                            for item
                            in write_all_calls
                        ],

                    "publish_lines":
                        [
                            item.lineno
                            for item
                            in publish_calls
                        ],

                    "canonical_bytes":
                        dynamic_ok,
                },
            )

        run_check(
            checks,
            CHECK_NAMES[18],
            v19,
        )

        def v20():
            write_calls = calls_named(
                target_writer,
                "_write_all",
            )

            fsync_calls = [
                call
                for call in calls_named(
                    target_writer,
                    "os.fsync",
                )
                if (
                    len(
                        call.args
                    ) == 1
                    and ast.unparse(
                        call.args[
                            0
                        ]
                    )
                    == "fd"
                )
            ]

            close_calls = [
                call
                for call in calls_named(
                    target_writer,
                    "os.close",
                )
                if (
                    len(
                        call.args
                    ) == 1
                    and ast.unparse(
                        call.args[
                            0
                        ]
                    )
                    == "fd"
                )
            ]

            publish_calls = calls_named(
                target_writer,
                "_publish_snapshot_noreplace",
            )

            order_ok = (
                len(
                    write_calls
                ) == 1
                and len(
                    fsync_calls
                ) == 1
                and len(
                    close_calls
                ) == 1
                and len(
                    publish_calls
                ) == 1
                and write_calls[
                    0
                ].lineno
                < fsync_calls[
                    0
                ].lineno
                < close_calls[
                    0
                ].lineno
                < publish_calls[
                    0
                ].lineno
            )

            android_dynamic_ok = (
                sys.platform
                == "android"
                and shared.get(
                    "v19_success"
                )
                is True
            )

            ok = (
                order_ok
                and android_dynamic_ok
            )

            shared[
                "v20_order"
            ] = ok

            shared[
                "v20_android_success"
            ] = android_dynamic_ok

            return (
                ok,
                {
                    "write_lines":
                        [
                            item.lineno
                            for item in write_calls
                        ],

                    "file_fsync_lines":
                        [
                            item.lineno
                            for item in fsync_calls
                        ],

                    "file_close_lines":
                        [
                            item.lineno
                            for item in close_calls
                        ],

                    "publish_lines":
                        [
                            item.lineno
                            for item in publish_calls
                        ],

                    "sys_platform":
                        sys.platform,

                    "android_dynamic_success":
                        android_dynamic_ok,
                },
            )

        run_check(
            checks,
            CHECK_NAMES[19],
            v20,
        )

        def v21():
            roots = imported_roots(
                target_tree
            )

            allowed = {
                "dataclasses",
                "pathlib",
                "typing",
                "ctypes",
                "errno",
                "hashlib",
                "json",
                "os",
                "re",
                "stat",
                "experiments",
            }

            return (
                (
                    "ctypes"
                    in roots
                    and roots.issubset(
                        allowed
                    )
                ),
                {
                    "import_roots":
                        sorted(
                            roots
                        ),
                },
            )

        run_check(
            checks,
            CHECK_NAMES[20],
            v21,
        )

        def v22():
            cdll_calls = calls_named(
                target_loader,
                "ctypes.CDLL",
            )

            top_level_cdll = []

            for node in target_tree.body:
                if isinstance(
                    node,
                    (
                        ast.FunctionDef,
                        ast.AsyncFunctionDef,
                        ast.ClassDef,
                    ),
                ):
                    continue

                for item in ast.walk(
                    node
                ):
                    if (
                        isinstance(
                            item,
                            ast.Call,
                        )
                        and dotted(
                            item.func
                        )
                        == "ctypes.CDLL"
                    ):
                        top_level_cdll.append(
                            item
                        )

            exact = False

            if len(
                cdll_calls
            ) == 1:
                call = cdll_calls[
                    0
                ]

                exact = (
                    len(
                        call.args
                    ) == 1
                    and isinstance(
                        call.args[
                            0
                        ],
                        ast.Constant,
                    )
                    and call.args[
                        0
                    ].value
                    is None
                    and len(
                        call.keywords
                    ) == 1
                    and call.keywords[
                        0
                    ].arg
                    == "use_errno"
                    and isinstance(
                        call.keywords[
                            0
                        ].value,
                        ast.Constant,
                    )
                    and call.keywords[
                        0
                    ].value.value
                    is True
                )

            return (
                exact
                and len(
                    top_level_cdll
                ) == 0
            )

        run_check(
            checks,
            CHECK_NAMES[21],
            v22,
        )

        def v23():
            renameat2_attributes = [
                node
                for node in ast.walk(
                    target_loader
                )
                if (
                    isinstance(
                        node,
                        ast.Attribute,
                    )
                    and dotted(
                        node
                    )
                    == "libc.renameat2"
                )
            ]

            attribute_handlers = []

            for node in ast.walk(
                target_loader
            ):
                if not isinstance(
                    node,
                    ast.ExceptHandler,
                ):
                    continue

                if (
                    node.type is not None
                    and ast.unparse(
                        node.type
                    )
                    == "AttributeError"
                ):
                    segment = ast.get_source_segment(
                        target_source,
                        node,
                    )

                    attribute_handlers.append(
                        segment
                        or ""
                    )

            fallback_calls = []

            for name in (
                "os.link",
                "posix.link",
                "os.rename",
                "os.replace",
                "os.symlink",
            ):
                fallback_calls.extend(
                    calls_named(
                        target_loader,
                        name,
                    )
                )

            return (
                len(
                    renameat2_attributes
                )
                == 1
                and len(
                    attribute_handlers
                )
                == 1
                and "TelemetrySnapshotPersistenceBackendError"
                in attribute_handlers[
                    0
                ]
                and "required libc renameat2 symbol is unavailable"
                in attribute_handlers[
                    0
                ]
                and fallback_calls
                == []
            )

        run_check(
            checks,
            CHECK_NAMES[22],
            v23,
        )

        def v24():
            argtype_assignments = []
            restype_assignments = []

            for node in ast.walk(
                target_loader
            ):
                if not isinstance(
                    node,
                    ast.Assign,
                ):
                    continue

                for target in node.targets:
                    target_name = dotted(
                        target
                    )

                    if (
                        target_name
                        == "renameat2.argtypes"
                    ):
                        argtype_assignments.append(
                            node
                        )

                    elif (
                        target_name
                        == "renameat2.restype"
                    ):
                        restype_assignments.append(
                            node
                        )

            if (
                len(
                    argtype_assignments
                )
                != 1
                or len(
                    restype_assignments
                )
                != 1
            ):
                return (
                    False,
                    {
                        "argtype_assignments":
                            len(
                                argtype_assignments
                            ),

                        "restype_assignments":
                            len(
                                restype_assignments
                            ),
                    },
                )

            arg_value = argtype_assignments[
                0
            ].value

            if not isinstance(
                arg_value,
                (
                    ast.List,
                    ast.Tuple,
                ),
            ):
                return False

            argtype_names = [
                dotted(
                    item
                )
                for item in arg_value.elts
            ]

            restype_name = dotted(
                restype_assignments[
                    0
                ].value
            )

            return (
                (
                    argtype_names
                    == [
                        "ctypes.c_int",
                        "ctypes.c_char_p",
                        "ctypes.c_int",
                        "ctypes.c_char_p",
                        "ctypes.c_uint",
                    ]
                    and restype_name
                    == "ctypes.c_int"
                ),
                {
                    "argtypes":
                        argtype_names,

                    "restype":
                        restype_name,
                },
            )

        run_check(
            checks,
            CHECK_NAMES[23],
            v24,
        )

        def v25():
            return (
                type(
                    persistence.RENAME_NOREPLACE
                )
                is int
                and persistence.RENAME_NOREPLACE
                == 1
            )

        run_check(
            checks,
            CHECK_NAMES[24],
            v25,
        )

        def v26():
            parent_fd_assignments = []

            for node in ast.walk(
                target_publisher
            ):
                if not isinstance(
                    node,
                    ast.Assign,
                ):
                    continue

                if not (
                    len(
                        node.targets
                    ) == 1
                    and isinstance(
                        node.targets[
                            0
                        ],
                        ast.Name,
                    )
                    and node.targets[
                        0
                    ].id
                    == "parent_fd"
                    and isinstance(
                        node.value,
                        ast.Call,
                    )
                    and dotted(
                        node.value.func
                    )
                    == "os.open"
                    and len(
                        node.value.args
                    ) >= 1
                    and ast.unparse(
                        node.value.args[
                            0
                        ]
                    )
                    == "parent"
                ):
                    continue

                parent_fd_assignments.append(
                    node
                )

            rename_calls = calls_named(
                target_publisher,
                "renameat2",
            )

            supplied_twice = False

            if (
                len(
                    rename_calls
                ) == 1
                and len(
                    rename_calls[
                        0
                    ].args
                ) == 5
            ):
                supplied_twice = (
                    ast.unparse(
                        rename_calls[
                            0
                        ].args[
                            0
                        ]
                    )
                    == "parent_fd"
                    and ast.unparse(
                        rename_calls[
                            0
                        ].args[
                            2
                        ]
                    )
                    == "parent_fd"
                )

            return (
                len(
                    parent_fd_assignments
                )
                == 1
                and supplied_twice
            )

        run_check(
            checks,
            CHECK_NAMES[25],
            v26,
        )

        def v27():
            rename_calls = calls_named(
                target_publisher,
                "renameat2",
            )

            if len(
                rename_calls
            ) != 1:
                return False

            args = [
                ast.unparse(
                    item
                )
                for item in rename_calls[
                    0
                ].args
            ]

            return (
                args
                == [
                    "parent_fd",
                    "partial_name",
                    "parent_fd",
                    "final_name",
                    "RENAME_NOREPLACE",
                ]
                and "partial_name = os.fsencode"
                in target_publisher_source
                and "partial.name"
                in target_publisher_source
                and "final_name = os.fsencode"
                in target_publisher_source
                and "final.name"
                in target_publisher_source
            )

        run_check(
            checks,
            CHECK_NAMES[26],
            v27,
        )

        def v28():
            rename_calls = calls_named(
                target_publisher,
                "renameat2",
            )

            return (
                len(
                    rename_calls
                ) == 1
                and len(
                    rename_calls[
                        0
                    ].args
                ) == 5
                and ast.unparse(
                    rename_calls[
                        0
                    ].args[
                        4
                    ]
                )
                == "RENAME_NOREPLACE"
            )

        run_check(
            checks,
            CHECK_NAMES[27],
            v28,
        )

        def v29():
            final = root / (
                "v29_android_success.json"
            )

            result = persistence.write_snapshot_file(
                source_snapshot,
                final,
            )

            read_result = persistence.read_snapshot_file(
                final
            )

            ok = (
                sys.platform
                == "android"
                and final.is_file()
                and result.final_path
                == str(
                    final
                )
                and result.snapshot_sha256
                == expected_snapshot_sha
                and result.file_sha256
                == independent_file_sha
                and read_result.file_sha256
                == independent_file_sha
                and model.snapshot_payload(
                    read_result.snapshot
                )
                == expected_snapshot_payload
            )

            shared[
                "positive_final"
            ] = final

            shared[
                "positive_write"
            ] = result

            shared[
                "positive_read"
            ] = read_result

            shared[
                "v29_ok"
            ] = ok

            return (
                ok,
                {
                    "sys_platform":
                        sys.platform,

                    "final":
                        str(
                            final
                        ),

                    "file_sha256":
                        read_result.file_sha256,
                },
            )

        run_check(
            checks,
            CHECK_NAMES[28],
            v29,
        )

        def v30():
            final = shared.get(
                "positive_final"
            )

            if final is None:
                return False

            partial = persistence.partial_path_for(
                final
            )

            return (
                final.exists()
                and not partial.exists()
            )

        run_check(
            checks,
            CHECK_NAMES[29],
            v30,
        )

        def v31():
            final = shared.get(
                "positive_final"
            )

            return (
                final is not None
                and regular_not_symlink(
                    final
                )
            )

        run_check(
            checks,
            CHECK_NAMES[30],
            v31,
        )

        def v32():
            partial = root / (
                "v32_inode.partial"
            )

            final = root / (
                "v32_inode.json"
            )

            write_candidate(
                partial,
                independent_file_bytes,
            )

            before = os.lstat(
                partial
            )

            persistence._publish_snapshot_noreplace(
                partial=partial,
                final=final,
                parent=root,
            )

            after = os.lstat(
                final
            )

            ok = (
                not partial.exists()
                and regular_not_symlink(
                    final
                )
                and before.st_dev
                == after.st_dev
                and before.st_ino
                == after.st_ino
            )

            shared[
                "v32_ok"
            ] = ok

            return ok

        run_check(
            checks,
            CHECK_NAMES[31],
            v32,
        )

        def v33():
            partial = root / (
                "v33_collision.partial"
            )

            final = root / (
                "v33_collision.json"
            )

            write_candidate(
                partial,
                independent_file_bytes,
            )

            sentinel = (
                b"OPENMIND_V33_FINAL_SENTINEL"
            )

            write_candidate(
                final,
                sentinel,
            )

            before = {
                "final_sha":
                    sha256_file(
                        final
                    ),

                "final_stat":
                    stat_key(
                        final
                    ),

                "partial_sha":
                    sha256_file(
                        partial
                    ),

                "partial_stat":
                    stat_key(
                        partial
                    ),
            }

            rejected = False
            error_type = None
            error_message = None

            try:
                persistence._publish_snapshot_noreplace(
                    partial=partial,
                    final=final,
                    parent=root,
                )

            except persistence.TelemetrySnapshotPersistenceWriteError as exc:
                rejected = True

                error_type = type(
                    exc
                ).__name__

                error_message = str(
                    exc
                )

            after = {
                "final_sha":
                    sha256_file(
                        final
                    ),

                "final_stat":
                    stat_key(
                        final
                    ),

                "partial_sha":
                    sha256_file(
                        partial
                    ),

                "partial_stat":
                    stat_key(
                        partial
                    ),
            }

            eexist_branches = [
                node
                for node in ast.walk(
                    target_publisher
                )
                if (
                    isinstance(
                        node,
                        ast.Compare,
                    )
                    and ast.unparse(
                        node
                    )
                    == "error_number == errno.EEXIST"
                )
            ]

            collision = {
                "rejected":
                    rejected,

                "error_type":
                    error_type,

                "error_message":
                    error_message,

                "before":
                    before,

                "after":
                    after,

                "final_bytes":
                    final.read_bytes(),

                "partial_bytes":
                    partial.read_bytes(),
            }

            shared[
                "collision"
            ] = collision

            eexist_dynamic = (
                rejected
                and error_message
                is not None
                and "appeared before atomic rename-no-replace publication"
                in error_message
            )

            return (
                (
                    len(
                        eexist_branches
                    ) == 1
                    and eexist_dynamic
                ),
                {
                    "error_type":
                        error_type,

                    "error_message":
                        error_message,

                    "eexist_branch_count":
                        len(
                            eexist_branches
                        ),
                },
            )

        run_check(
            checks,
            CHECK_NAMES[32],
            v33,
        )

        def v34():
            collision = shared.get(
                "collision"
            )

            if collision is None:
                return False

            return (
                collision[
                    "before"
                ][
                    "final_sha"
                ]
                == collision[
                    "after"
                ][
                    "final_sha"
                ]
                and collision[
                    "before"
                ][
                    "final_stat"
                ]
                == collision[
                    "after"
                ][
                    "final_stat"
                ]
                and collision[
                    "final_bytes"
                ]
                == b"OPENMIND_V33_FINAL_SENTINEL"
            )

        run_check(
            checks,
            CHECK_NAMES[33],
            v34,
        )

        def v35():
            collision = shared.get(
                "collision"
            )

            if collision is None:
                return False

            return (
                collision[
                    "before"
                ][
                    "partial_sha"
                ]
                == collision[
                    "after"
                ][
                    "partial_sha"
                ]
                and collision[
                    "before"
                ][
                    "partial_stat"
                ]
                == collision[
                    "after"
                ][
                    "partial_stat"
                ]
                and collision[
                    "partial_bytes"
                ]
                == independent_file_bytes
            )

        run_check(
            checks,
            CHECK_NAMES[34],
            v35,
        )

        def v36():
            rename_calls = calls_named(
                target_publisher,
                "renameat2",
            )

            parent_fsync_calls = [
                call
                for call in calls_named(
                    target_publisher,
                    "os.fsync",
                )
                if (
                    len(
                        call.args
                    ) == 1
                    and ast.unparse(
                        call.args[
                            0
                        ]
                    )
                    == "parent_fd"
                )
            ]

            static_ok = (
                len(
                    rename_calls
                ) == 1
                and len(
                    parent_fsync_calls
                ) == 1
                and rename_calls[
                    0
                ].lineno
                < parent_fsync_calls[
                    0
                ].lineno
            )

            android_dynamic_ok = (
                sys.platform
                == "android"
                and shared.get(
                    "v32_ok"
                )
                is True
            )

            return (
                static_ok
                and android_dynamic_ok,
                {
                    "rename_lines":
                        [
                            item.lineno
                            for item in rename_calls
                        ],

                    "parent_fsync_lines":
                        [
                            item.lineno
                            for item
                            in parent_fsync_calls
                        ],

                    "sys_platform":
                        sys.platform,

                    "android_dynamic_success":
                        android_dynamic_ok,
                },
            )

        run_check(
            checks,
            CHECK_NAMES[35],
            v36,
        )

        def v37():
            collision = shared.get(
                "collision"
            )

            if collision is None:
                return False

            return (
                collision[
                    "rejected"
                ]
                and collision[
                    "partial_bytes"
                ]
                == independent_file_bytes
                and collision[
                    "before"
                ][
                    "partial_sha"
                ]
                == collision[
                    "after"
                ][
                    "partial_sha"
                ]
            )

        run_check(
            checks,
            CHECK_NAMES[36],
            v37,
        )

        def v38():
            unlink_calls = calls_named(
                target_tree,
                "os.unlink",
            )

            final = shared.get(
                "positive_final"
            )

            return (
                len(
                    unlink_calls
                ) == 0
                and final is not None
                and final.exists()
                and not persistence.partial_path_for(
                    final
                ).exists()
            )

        run_check(
            checks,
            CHECK_NAMES[37],
            v38,
        )

        def v39():
            return (
                len(
                    calls_named(
                        target_tree,
                        "os.link",
                    )
                )
                == 0
            )

        run_check(
            checks,
            CHECK_NAMES[38],
            v39,
        )

        def v40():
            return (
                len(
                    calls_named(
                        target_tree,
                        "posix.link",
                    )
                )
                == 0
            )

        run_check(
            checks,
            CHECK_NAMES[39],
            v40,
        )

        def v41():
            final = shared.get(
                "positive_final"
            )

            return (
                len(
                    calls_named(
                        target_tree,
                        "os.symlink",
                    )
                )
                == 0
                and final is not None
                and regular_not_symlink(
                    final
                )
            )

        run_check(
            checks,
            CHECK_NAMES[40],
            v41,
        )

        def v42():
            return (
                len(
                    calls_named(
                        target_tree,
                        "os.replace",
                    )
                )
                == 0
                and len(
                    calls_named(
                        target_tree,
                        "os.rename",
                    )
                )
                == 0
            )

        run_check(
            checks,
            CHECK_NAMES[41],
            v42,
        )

        def v43():
            roots = imported_roots(
                target_tree
            )

            return (
                "subprocess"
                not in roots
                and len(
                    calls_named(
                        target_tree,
                        "os.system",
                    )
                )
                == 0
                and "subprocess."
                not in target_source
            )

        run_check(
            checks,
            CHECK_NAMES[42],
            v43,
        )

        def v44():
            forbidden_attrs = [
                node
                for node in ast.walk(
                    target_tree
                )
                if (
                    isinstance(
                        node,
                        ast.Attribute,
                    )
                    and node.attr
                    in {
                        "link",
                        "linkat",
                    }
                )
            ]

            return (
                len(
                    forbidden_attrs
                )
                == 0
            )

        run_check(
            checks,
            CHECK_NAMES[43],
            v44,
        )

        def v45():
            required_loader_messages = (
                "failed to load process C library for renameat2 backend",
                "required libc renameat2 symbol is unavailable",
                "failed to bind exact renameat2 ABI",
            )

            required_publisher_messages = (
                "renameat2 invocation failed before publication",
                "renameat2 backend is unsupported by the running kernel",
            )

            enosys_branches = [
                node
                for node in ast.walk(
                    target_publisher
                )
                if (
                    isinstance(
                        node,
                        ast.Compare,
                    )
                    and ast.unparse(
                        node
                    )
                    == "error_number == errno.ENOSYS"
                )
            ]

            fallback_calls = []

            for name in (
                "os.link",
                "posix.link",
                "os.rename",
                "os.replace",
                "os.symlink",
            ):
                fallback_calls.extend(
                    calls_named(
                        target_tree,
                        name,
                    )
                )

            return (
                all(
                    message
                    in target_loader_source
                    for message
                    in required_loader_messages
                )
                and all(
                    message
                    in target_publisher_source
                    for message
                    in required_publisher_messages
                )
                and target_loader_source.count(
                    "TelemetrySnapshotPersistenceBackendError"
                )
                >= 3
                and target_publisher_source.count(
                    "TelemetrySnapshotPersistenceBackendError"
                )
                >= 2
                and len(
                    enosys_branches
                ) == 1
                and fallback_calls
                == []
            )

        run_check(
            checks,
            CHECK_NAMES[44],
            v45,
        )

        def v46():
            base = persistence.TelemetrySnapshotPersistenceError

            classes = (
                persistence.TelemetrySnapshotPersistenceValidationError,
                persistence.TelemetrySnapshotPersistenceReadError,
                persistence.TelemetrySnapshotPersistenceBackendError,
                persistence.TelemetrySnapshotPersistenceWriteError,
            )

            return (
                len(
                    set(
                        classes
                    )
                )
                == 4
                and all(
                    issubclass(
                        cls,
                        base,
                    )
                    for cls in classes
                )
            )

        run_check(
            checks,
            CHECK_NAMES[45],
            v46,
        )

        def v47():
            result = shared.get(
                "positive_write"
            )

            final = shared.get(
                "positive_final"
            )

            if (
                result is None
                or final is None
            ):
                return False

            cls = persistence.TelemetrySnapshotWriteResult

            params = getattr(
                cls,
                "__dataclass_params__",
                None,
            )

            return (
                isinstance(
                    result,
                    cls,
                )
                and params is not None
                and params.frozen
                is True
                and hasattr(
                    cls,
                    "__slots__",
                )
                and result.final_path
                == str(
                    final
                )
                and result.snapshot_sha256
                == expected_snapshot_sha
                and result.file_sha256
                == independent_file_sha
                and result.byte_length
                == len(
                    independent_file_bytes
                )
            )

        run_check(
            checks,
            CHECK_NAMES[46],
            v47,
        )

        def v48():
            result = shared.get(
                "positive_read"
            )

            if result is None:
                return False

            cls = persistence.TelemetrySnapshotReadResult

            params = getattr(
                cls,
                "__dataclass_params__",
                None,
            )

            return (
                isinstance(
                    result,
                    cls,
                )
                and params is not None
                and params.frozen
                is True
                and hasattr(
                    cls,
                    "__slots__",
                )
                and model.snapshot_payload(
                    result.snapshot
                )
                == expected_snapshot_payload
                and result.snapshot_sha256
                == expected_snapshot_sha
                and result.file_sha256
                == independent_file_sha
                and result.byte_length
                == len(
                    independent_file_bytes
                )
            )

        run_check(
            checks,
            CHECK_NAMES[47],
            v48,
        )

        def v49():
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

            final = root / (
                "v49_determinism.json"
            )

            persistence.write_snapshot_file(
                first,
                final,
            )

            read_back = persistence.read_snapshot_file(
                final
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
                and model.snapshot_payload(
                    read_back.snapshot
                )
                == first_payload
            )

        run_check(
            checks,
            CHECK_NAMES[48],
            v49,
        )

        def v50():
            return (
                model.snapshot_payload(
                    source_snapshot
                )
                == source_payload_before
                and model.snapshot_sha256(
                    source_snapshot
                )
                == source_sha_before
            )

        run_check(
            checks,
            CHECK_NAMES[49],
            v50,
        )

        def v51():
            phase6c_after = sha256_file(
                PHASE6C_PATH
            )

            imports = [
                (
                    node.module
                    if isinstance(
                        node,
                        ast.ImportFrom,
                    )
                    else ",".join(
                        alias.name
                        for alias in node.names
                    )
                )
                for node in target_tree.body
                if isinstance(
                    node,
                    (
                        ast.Import,
                        ast.ImportFrom,
                    ),
                )
            ]

            return (
                phase6c_before
                == PHASE6C_SHA256
                and phase6c_after
                == PHASE6C_SHA256
                and all(
                    (
                        "maf_object_runtime_residency"
                        not in (
                            item
                            or ""
                        )
                    )
                    for item in imports
                )
            )

        run_check(
            checks,
            CHECK_NAMES[50],
            v51,
        )

        def v52():
            forbidden = {
                "plan_repack",
                "build_segment",
                "build_generation",
                "activate_generation",
                "rollback_generation",
            }

            def forbidden_calls(
                tree,
            ):
                found = []

                for node in ast.walk(
                    tree
                ):
                    if not isinstance(
                        node,
                        ast.Call,
                    ):
                        continue

                    name = dotted(
                        node.func
                    ).split(
                        "."
                    )[
                        -1
                    ]

                    if name in forbidden:
                        found.append(
                            name
                        )

                return found

            return (
                forbidden_calls(
                    target_tree
                )
                == []
                and forbidden_calls(
                    runner_tree
                )
                == []
            )

        run_check(
            checks,
            CHECK_NAMES[51],
            v52,
        )

        def v53():
            forbidden_network_roots = {
                "socket",
                "urllib",
                "http",
                "httpx",
                "requests",
                "aiohttp",
            }

            forbidden_timing_roots = {
                "time",
            }

            forbidden_process_roots = {
                "subprocess",
            }

            target_roots = imported_roots(
                target_tree
            )

            runner_roots = imported_roots(
                runner_tree
            )

            inference_terminals = {
                "infer",
                "inference",
                "run_inference",
                "generate",
                "generate_batch",
                "llama_decode",
                "llama_eval",
            }

            phase6e_terminals = {
                "phase6e",
                "phase_6e",
                "selective_access",
                "selective_tensor_access",
                "run_selective_access",
            }

            forbidden_calls = []

            for tree_item in (
                target_tree,
                runner_tree,
            ):
                for node in ast.walk(
                    tree_item
                ):
                    if not isinstance(
                        node,
                        ast.Call,
                    ):
                        continue

                    call_name = dotted(
                        node.func
                    )

                    terminal = call_name.split(
                        "."
                    )[
                        -1
                    ].lower()

                    root_name = call_name.split(
                        "."
                    )[
                        0
                    ].lower()

                    if (
                        root_name
                        in forbidden_network_roots
                        or root_name
                        in forbidden_timing_roots
                        or root_name
                        in forbidden_process_roots
                        or terminal
                        in inference_terminals
                        or terminal
                        in phase6e_terminals
                    ):
                        forbidden_calls.append(
                            (
                                node.lineno,
                                call_name,
                            )
                        )

            forbidden_imports = sorted(
                (
                    target_roots
                    | runner_roots
                )
                & (
                    forbidden_network_roots
                    | forbidden_timing_roots
                    | forbidden_process_roots
                )
            )

            inference_forbidden = all(
                (
                    terminal
                    not in inference_terminals
                )
                for _, call_name
                in forbidden_calls
                for terminal in (
                    call_name.split(
                        "."
                    )[
                        -1
                    ].lower(),
                )
            )

            phase6e_forbidden = all(
                (
                    terminal
                    not in phase6e_terminals
                )
                for _, call_name
                in forbidden_calls
                for terminal in (
                    call_name.split(
                        "."
                    )[
                        -1
                    ].lower(),
                )
            )

            return (
                (
                    forbidden_imports
                    == []
                    and forbidden_calls
                    == []
                    and inference_forbidden
                    and phase6e_forbidden
                    and BENCHMARK_EXECUTED
                    is False
                    and PERFORMANCE_VERDICT
                    is None
                ),
                {
                    "forbidden_imports":
                        forbidden_imports,

                    "forbidden_calls":
                        forbidden_calls,

                    "inference_forbidden":
                        inference_forbidden,

                    "phase6e_forbidden":
                        phase6e_forbidden,

                    "benchmark_executed":
                        BENCHMARK_EXECUTED,

                    "performance_verdict":
                        PERFORMANCE_VERDICT,
                },
            )

        run_check(
            checks,
            CHECK_NAMES[52],
            v53,
        )

        def v54():
            expected = (
                (
                    PERSISTENCE_V1_PROTOCOL_PATH,
                    PERSISTENCE_V1_PROTOCOL_SHA256,
                ),
                (
                    PERSISTENCE_V1_PATH,
                    PERSISTENCE_V1_SHA256,
                ),
                (
                    PERSISTENCE_V1_VALIDATION_PROTOCOL_PATH,
                    PERSISTENCE_V1_VALIDATION_PROTOCOL_SHA256,
                ),
                (
                    PERSISTENCE_V1_VALIDATION_RUNNER_PATH,
                    PERSISTENCE_V1_VALIDATION_RUNNER_SHA256,
                ),
            )

            exact = all(
                sha256_file(
                    path
                )
                == expected_sha
                for path, expected_sha
                in expected
            )

            import_calls = calls_named(
                runner_main,
                "import_exact",
            )

            imported_modules = []

            for call in import_calls:
                if (
                    len(
                        call.args
                    ) != 1
                    or not isinstance(
                        call.args[
                            0
                        ],
                        ast.Constant,
                    )
                    or not isinstance(
                        call.args[
                            0
                        ].value,
                        str,
                    )
                ):
                    imported_modules.append(
                        "<nonliteral>"
                    )

                else:
                    imported_modules.append(
                        call.args[
                            0
                        ].value
                    )

            expected_modules = [
                (
                    "experiments.model_fractal."
                    "maf_segment_locality_data_model_v1"
                ),
                (
                    "experiments.model_fractal."
                    "maf_segment_locality_telemetry_snapshot_persistence_v1_1"
                ),
            ]

            return (
                (
                    exact
                    and not PERSISTENCE_V1_RESULT_PATH.exists()
                    and not PERSISTENCE_V1_RESULT_TEMP_PATH.exists()
                    and imported_modules
                    == expected_modules
                ),
                {
                    "imported_scientific_modules":
                        imported_modules,

                    "v1_result_absent":
                        not PERSISTENCE_V1_RESULT_PATH.exists(),

                    "v1_result_temp_absent":
                        not PERSISTENCE_V1_RESULT_TEMP_PATH.exists(),
                },
            )

        run_check(
            checks,
            CHECK_NAMES[53],
            v54,
        )

        def v55():
            binding_calls = call_lines(
                runner_main,
                "binding_gate",
            )

            reserve_calls = call_lines(
                runner_main,
                "reserve_result_slot",
            )

            import_calls = call_lines(
                runner_main,
                "import_exact",
            )

            result_calls = call_lines(
                runner_main,
                "write_reserved_result",
            )

            return (
                len(
                    binding_calls
                ) == 1
                and len(
                    reserve_calls
                ) == 1
                and len(
                    import_calls
                ) == 2
                and len(
                    result_calls
                ) == 1
                and binding_calls[
                    0
                ]
                < reserve_calls[
                    0
                ]
                < import_calls[
                    0
                ]
                and "RESULT_PATH"
                in runner_binding_source
                and "RESULT_TEMP_PATH"
                in runner_binding_source
                and "PERSISTENCE_V1_RESULT_PATH"
                in runner_binding_source
                and "PERSISTENCE_V1_RESULT_TEMP_PATH"
                in runner_binding_source
                and "os.O_EXCL"
                in runner_reserve_source
                and "os.fstat"
                in runner_reserve_source
                and "stat.S_ISREG"
                in runner_reserve_source
                and "os.fsync"
                in runner_reserve_source
                and "_fsync_directory_harness"
                in runner_reserve_source
                and "renameat2("
                in runner_result_publisher_source
                and "RESULT_RENAME_NOREPLACE"
                in runner_result_publisher_source
                and "os.replace"
                not in runner_result_publisher_source
                and "os.rename("
                not in runner_result_publisher_source
            )

        run_check(
            checks,
            CHECK_NAMES[54],
            v55,
        )

        def v56():
            backend = persistence._load_renameat2_backend()

            return (
                sys.platform
                == "android"
                and callable(
                    backend
                )
                and shared.get(
                    "v29_ok"
                )
                is True
                and shared.get(
                    "v32_ok"
                )
                is True
            )

        run_check(
            checks,
            CHECK_NAMES[55],
            v56,
        )

        def v57():
            collision = shared.get(
                "collision"
            )

            runner_roots = imported_roots(
                runner_tree
            )

            forbidden_race_names = {
                "run_race_fixture",
                "make_race_snapshot",
            }

            executable_refs = []

            for node in ast.walk(
                runner_tree
            ):
                if isinstance(
                    node,
                    (
                        ast.FunctionDef,
                        ast.AsyncFunctionDef,
                    ),
                ):
                    if node.name in forbidden_race_names:
                        executable_refs.append(
                            (
                                node.lineno,
                                "definition",
                                node.name,
                            )
                        )

                elif isinstance(
                    node,
                    ast.Call,
                ):
                    call_name = dotted(
                        node.func
                    )

                    if (
                        call_name.split(
                            "."
                        )[
                            -1
                        ]
                        in forbidden_race_names
                    ):
                        executable_refs.append(
                            (
                                node.lineno,
                                "call",
                                call_name,
                            )
                        )

                elif (
                    isinstance(
                        node,
                        ast.Name,
                    )
                    and isinstance(
                        node.ctx,
                        ast.Load,
                    )
                    and node.id
                    in forbidden_race_names
                ):
                    executable_refs.append(
                        (
                            node.lineno,
                            "name",
                            node.id,
                        )
                    )

                elif (
                    isinstance(
                        node,
                        ast.Attribute,
                    )
                    and node.attr
                    in forbidden_race_names
                ):
                    executable_refs.append(
                        (
                            node.lineno,
                            "attribute",
                            dotted(
                                node
                            ),
                        )
                    )

            return (
                (
                    shared.get(
                        "v20_order"
                    )
                    is True
                    and collision
                    is not None
                    and collision[
                        "rejected"
                    ]
                    is True
                    and collision[
                        "before"
                    ][
                        "final_sha"
                    ]
                    == collision[
                        "after"
                    ][
                        "final_sha"
                    ]
                    and collision[
                        "before"
                    ][
                        "partial_sha"
                    ]
                    == collision[
                        "after"
                    ][
                        "partial_sha"
                    ]
                    and executable_refs
                    == []
                    and "signal"
                    not in runner_roots
                    and "time"
                    not in runner_roots
                    and "subprocess"
                    not in runner_roots
                ),
                {
                    "executable_race_refs":
                        executable_refs,

                    "collision_error":
                        collision.get(
                            "error_message"
                        )
                        if collision
                        is not None
                        else None,
                },
            )

        run_check(
            checks,
            CHECK_NAMES[56],
            v57,
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
            "validation check identity/order mismatch"
        )

    return checks


def main():
    if not CANDIDATE_COMPLETE:
        raise SystemExit(
            "UNFROZEN CANDIDATE: scientific invocation forbidden"
        )

    # Pre-scientific authority gate.
    binding_gate()

    # Construct the raw-result envelope while the slot is still
    # unspent. Failure here is pre-scientific and leaves the slot
    # unspent.
    result = base_result()

    # Exact-once spend transition.
    reserve_result_slot()

    try:
        # Static evidence is read/parsed exactly once per artifact.
        runner_evidence = (
            runner_static_evidence()
        )

        target_evidence = (
            target_static_evidence()
        )

        # No scientific target import occurs before slot reservation.
        import_inventory_before = directory_inventory(
            REPO_ROOT
        )

        model = import_exact(
            "experiments.model_fractal."
            "maf_segment_locality_data_model_v1"
        )

        persistence = import_exact(
            "experiments.model_fractal."
            "maf_segment_locality_telemetry_snapshot_persistence_v1_1"
        )

        import_inventory_after = directory_inventory(
            REPO_ROOT
        )

        if (
            import_inventory_after
            != import_inventory_before
        ):
            raise HarnessInvalid(
                "scientific import changed repository path inventory"
            )

        checks = run_scientific_checks(
            persistence=persistence,
            model=model,
            runner_evidence=runner_evidence,
            target_evidence=target_evidence,
        )

        failed = [
            item["name"]
            for item in checks
            if item["pass"] is not True
        ]

        result["checks"] = checks
        result["check_count"] = len(
            checks
        )
        result["failed_checks"] = failed
        result["validation_valid"] = True
        result["all_pass"] = (
            len(checks)
            == EXPECTED_CHECK_COUNT
            and not failed
        )

    except AuditorError as exc:
        result["auditor_error"] = {
            "type":
                type(
                    exc
                ).__name__,

            "message":
                str(
                    exc
                ),

            "origin":
                "validation_harness",

            "traceback":
                traceback.format_exc(),
        }

    except (
        KeyboardInterrupt,
        SystemExit,
    ) as exc:
        result["fatal_error"] = {
            "type":
                type(
                    exc
                ).__name__,

            "message":
                str(
                    exc
                ),

            "origin":
                "interruption",

            "traceback":
                traceback.format_exc(),
        }

    except Exception as exc:
        if exception_touches_scientific_target(
            exc
        ):
            result["fatal_error"] = {
                "type":
                    type(
                        exc
                    ).__name__,

                "message":
                    str(
                        exc
                    ),

                "origin":
                    "scientific_target",

                "traceback":
                    traceback.format_exc(),
            }

        else:
            result["auditor_error"] = {
                "type":
                    type(
                        exc
                    ).__name__,

                "message":
                    str(
                        exc
                    ),

                "origin":
                    "validation_harness",

                "traceback":
                    traceback.format_exc(),
            }

    finally:
        # Once reserved, every scientific outcome attempts one durable
        # authoritative raw-result freeze. Failure residue is preserved.
        write_reserved_result(
            result
        )

    if (
        result["auditor_error"]
        is not None
        or result["fatal_error"]
        is not None
        or result["validation_valid"]
        is not True
    ):
        return 2

    if result["all_pass"] is not True:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
