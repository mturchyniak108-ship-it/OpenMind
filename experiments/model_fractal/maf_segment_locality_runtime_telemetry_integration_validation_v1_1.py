#!/usr/bin/env python3
"""Phase 6D Runtime Telemetry Integration Validation V1.1.

This runner is inert unless BOTH:

    --arm-exact-once

and:

    OPENMIND_ARM_RUNTIME_TELEMETRY_INTEGRATION_VALIDATION_V1_1=YES

are supplied.

An ordinary execution or --guard-false performs no OpenMind
imports, creates no validation fixture, and does not reserve the
scientific result slot.
"""

from __future__ import annotations

import argparse
import ast
import ctypes
import dataclasses
import enum
import errno
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent

RESULT = (
    ROOT
    / "maf_segment_locality_runtime_telemetry_integration_validation_v1_1.json"
)

RESULT_TEMP = Path(
    str(RESULT) + ".partial"
)

ARM_ENV = (
    "OPENMIND_ARM_RUNTIME_TELEMETRY_INTEGRATION_VALIDATION_V1_1"
)

ARM_VALUE = "YES"

EXPECTED_CHECK_COUNT = 42


AUTH = {
    "validation_protocol": (
        "MAF_SEGMENT_LOCALITY_RUNTIME_TELEMETRY_INTEGRATION_VALIDATION_V1_1_PROTOCOL.md",
        "105d448397a03f2ced7e66871f46e85f83f3e8fef673fda369d8f41601b6779e",
    ),
    "integration_protocol": (
        "MAF_SEGMENT_LOCALITY_RUNTIME_TELEMETRY_INTEGRATION_V1_PROTOCOL.md",
        "078ab7c95bd98b94cc24a5af19bd876d69fec860a77e781aa12b6ec57262434c",
    ),
    "integration": (
        "maf_segment_locality_runtime_telemetry_integration_v1.py",
        "0c805296ca1eca8926dbd8ce28badc6b87b56bd482280624548e1ea7d53ae7bb",
    ),
    "runtime_protocol": (
        "MAF_OBJECT_RUNTIME_RESIDENCY_V1_PROTOCOL.md",
        "81987d00ef4cb51556dcebf08bff9c9fa8979f033df05304d347b759e545eb13",
    ),
    "runtime": (
        "maf_object_runtime_residency_v1.py",
        "4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9",
    ),
    "runtime_verdict": (
        "MAF_OBJECT_RUNTIME_RESIDENCY_PHASE_6C_VERDICT.md",
        "800fd8e6e58d2af7ea46133e2e6a26d3b380fa4abd371f055324f722ad92784f",
    ),
    "data_model_protocol": (
        "MAF_SEGMENT_LOCALITY_DATA_MODEL_V1_PROTOCOL.md",
        "712caa2e7dfc948f607a4c8d68064fc838eb1f58701fc5206c52aaf8e6492bc4",
    ),
    "data_model": (
        "maf_segment_locality_data_model_v1.py",
        "5432f2d74a610f2d0f9181e9af146013bb198a4e837af634993909358fff8ad0",
    ),
    "data_model_result": (
        "maf_segment_locality_data_model_validation_v1.json",
        "9aa2e467dc451b2d2122802e1e8b8fabf616db756a36b53a3600cca793923b4d",
    ),
    "data_model_verdict": (
        "MAF_SEGMENT_LOCALITY_DATA_MODEL_VALIDATION_V1_VERDICT.md",
        "7754c9d5dada8dc214a21236827c64cafea880e4b0c679cd84c9c4833fd3e9db",
    ),
    "persistence": (
        "maf_segment_locality_telemetry_snapshot_persistence_v1_1.py",
        "cb1e2e3dc11006c75e38e33c941b39959aa4d99f971de9e08250d8b995fe09b0",
    ),
    "persistence_result": (
        "maf_segment_locality_telemetry_snapshot_persistence_validation_v1_3.json",
        "042a0474e3ec9926d69cee1bda088427c23b121088a424c5c94b68f2510b2bff",
    ),
    "persistence_verdict": (
        "MAF_SEGMENT_LOCALITY_TELEMETRY_SNAPSHOT_PERSISTENCE_VALIDATION_V1_3_VERDICT.md",
        "a623507248a32c8384b5c00b509d1fe45c176eee4719527fbfb7b0e60db89322",
    ),
}


RESIDENT_DIRECTORY = (
    ROOT
    / "maf_resident_pk_directory_v1.py"
)

RESIDENT_DIRECTORY_KNOWN_SHA256 = (
    "4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6"
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()


def authority_inventory() -> dict[str, str]:
    return {
        label: sha256_file(ROOT / relative)
        for label, (relative, _expected)
        in AUTH.items()
    }


def authority_exact() -> bool:
    for relative, expected in AUTH.values():
        path = ROOT / relative

        if not path.is_file():
            return False

        if sha256_file(path) != expected:
            return False

    return True
def canonical(value):
    if dataclasses.is_dataclass(value):
        return {
            field.name: canonical(
                getattr(value, field.name)
            )
            for field in dataclasses.fields(value)
        }

    if isinstance(value, enum.Enum):
        return value.value

    if isinstance(value, bytes):
        return {
            "sha256": hashlib.sha256(value).hexdigest(),
            "length": len(value),
        }

    if isinstance(value, Path):
        return str(value)

    if isinstance(value, (tuple, list)):
        return [
            canonical(item)
            for item in value
        ]

    if isinstance(value, dict):
        return {
            str(key): canonical(value[key])
            for key in sorted(
                value,
                key=lambda item: str(item),
            )
        }

    if isinstance(
        value,
        (
            str,
            int,
            float,
            bool,
            type(None),
        ),
    ):
        return value

    return repr(value)


def canonical_json(value) -> str:
    return json.dumps(
        canonical(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def event_kind(event) -> str:
    kind = getattr(
        event,
        "kind",
        None,
    )

    if isinstance(kind, enum.Enum):
        return str(kind.value)

    return str(kind)


def event_kinds(events) -> list[str]:
    return [
        event_kind(event)
        for event in events
    ]


def capture_exception(fn):
    try:
        fn()
    except Exception as exc:
        return (
            type(exc).__name__,
            str(exc),
        )

    return None


class CheckRecorder:
    def __init__(self) -> None:
        self.rows = []

    def add(
        self,
        name: str,
        passed: bool,
        detail=None,
    ) -> None:
        self.rows.append(
            {
                "name": name,
                "pass": bool(passed),
                "detail": canonical(detail),
            }
        )

    def run(
        self,
        name: str,
        fn,
    ) -> None:
        try:
            passed, detail = fn()

            self.add(
                name,
                passed,
                detail,
            )

        except Exception as exc:
            self.add(
                name,
                False,
                {
                    "unexpected_exception_type":
                        type(exc).__name__,
                    "unexpected_exception_message":
                        str(exc),
                },
            )


class AuditProbe:
    NETWORK_EVENTS = {
        "socket.connect",
        "socket.connect_ex",
        "socket.getaddrinfo",
        "socket.sendto",
        "socket.sendmsg",
    }

    SUBPROCESS_EVENTS = {
        "subprocess.Popen",
        "os.system",
        "os.posix_spawn",
        "os.posix_spawnp",
    }

    def __init__(self) -> None:
        self.capture_writes = False
        self.write_events = []
        self.network_events = []
        self.subprocess_events = []

    def hook(
        self,
        event,
        args,
    ) -> None:
        if event in self.NETWORK_EVENTS:
            self.network_events.append(
                (
                    event,
                    repr(args),
                )
            )

        if event in self.SUBPROCESS_EVENTS:
            self.subprocess_events.append(
                (
                    event,
                    repr(args),
                )
            )

        if (
            not self.capture_writes
            or event != "open"
        ):
            return

        path = (
            args[0]
            if len(args) > 0
            else None
        )

        mode = (
            args[1]
            if len(args) > 1
            else None
        )

        flags = (
            args[2]
            if len(args) > 2
            else 0
        )

        write_mode = (
            isinstance(mode, str)
            and any(
                marker in mode
                for marker in (
                    "w",
                    "a",
                    "x",
                    "+",
                )
            )
        )

        write_flags = (
            isinstance(flags, int)
            and bool(
                flags
                & (
                    os.O_WRONLY
                    | os.O_RDWR
                    | os.O_CREAT
                    | os.O_TRUNC
                    | os.O_APPEND
                )
            )
        )

        if write_mode or write_flags:
            self.write_events.append(
                (
                    repr(path),
                    repr(mode),
                    flags,
                )
            )


class RecordingAccumulator:
    def __init__(
        self,
        delegate,
        *,
        fail: bool=False,
    ) -> None:
        self.delegate = delegate
        self.fail = fail
        self.events = []

    def add_event(
        self,
        event,
    ) -> None:
        if self.fail:
            raise RuntimeError(
                "validation injected telemetry fault"
            )

        self.events.append(event)

        self.delegate.add_event(
            event
        )

    def snapshot(self):
        return self.delegate.snapshot()


def prefetch_zero(
    snapshot,
    events,
):
    raw_prefetch_events = [
        canonical(event)
        for event in events
        if event_kind(event).startswith(
            "PREFETCH_"
        )
    ]

    aggregates = canonical(
        snapshot.prefetch_aggregates
    )

    nonzero = []

    def walk(
        value,
        key="",
    ):
        if isinstance(value, dict):
            for child_key, child in value.items():
                walk(
                    child,
                    str(child_key),
                )

        elif isinstance(value, list):
            for child in value:
                walk(
                    child,
                    key,
                )

        elif (
            isinstance(
                value,
                (
                    int,
                    float,
                ),
            )
            and not isinstance(value, bool)
            and value != 0
            and any(
                marker in key.lower()
                for marker in (
                    "count",
                    "bytes",
                    "issued",
                    "consumed",
                    "unused",
                )
            )
        ):
            nonzero.append(
                (
                    key,
                    value,
                )
            )

    walk(aggregates)

    return (
        not raw_prefetch_events
        and not nonzero,
        {
            "events":
                raw_prefetch_events,
            "aggregates":
                aggregates,
            "nonzero":
                nonzero,
        },
    )
def static_boundaries():
    integration_path = (
        ROOT
        / AUTH["integration"][0]
    )

    tree = ast.parse(
        integration_path.read_text(
            encoding="utf-8"
        ),
        filename=str(
            integration_path
        ),
    )

    imports = []
    calls = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(
                alias.name
                for alias in node.names
            )

        elif (
            isinstance(
                node,
                ast.ImportFrom,
            )
            and node.module
        ):
            imports.append(
                node.module
            )

        elif isinstance(
            node,
            ast.Call,
        ):
            try:
                calls.append(
                    (
                        node.lineno,
                        ast.unparse(
                            node.func
                        ),
                        ast.unparse(
                            node
                        ),
                    )
                )
            except Exception:
                pass

    network_modules = (
        "socket",
        "urllib",
        "http.client",
        "requests",
        "httpx",
        "aiohttp",
    )

    bad_imports = [
        name
        for name in imports
        if (
            any(
                name == module
                or name.startswith(
                    module + "."
                )
                for module
                in network_modules
            )
            or name.startswith(
                "subprocess"
            )
        )
    ]

    bad_calls = [
        (
            line,
            name,
        )
        for line, name, _text
        in calls
        if (
            any(
                name == module
                or name.startswith(
                    module + "."
                )
                for module
                in network_modules
            )
            or name.startswith(
                "subprocess."
            )
            or name
            in {
                "os.system",
                "os.posix_spawn",
                "os.posix_spawnp",
            }
        )
    ]

    persistence_imports = [
        name
        for name in imports
        if "persistence"
        in name.lower()
    ]

    persistence_calls = [
        (
            line,
            name,
        )
        for line, name, _text
        in calls
        if "persist"
        in name.lower()
    ]

    adapter_classes = [
        node
        for node in tree.body
        if (
            isinstance(
                node,
                ast.ClassDef,
            )
            and node.name
            == (
                "MAFSegmentLocality"
                "RuntimeTelemetryAdapter"
            )
        )
    ]

    composition = {
        "class_count":
            len(adapter_classes),
        "bases": [],
        "runtime_assignments": [],
        "runtime_setattr": [],
        "runtime_callbacks": [],
    }

    if len(adapter_classes) == 1:
        adapter_class = (
            adapter_classes[0]
        )

        composition["bases"] = [
            ast.unparse(base)
            for base
            in adapter_class.bases
        ]

        for node in ast.walk(
            adapter_class
        ):
            if isinstance(
                node,
                (
                    ast.Assign,
                    ast.AnnAssign,
                ),
            ):
                targets = (
                    node.targets
                    if isinstance(
                        node,
                        ast.Assign,
                    )
                    else [
                        node.target
                    ]
                )

                for target in targets:
                    try:
                        rendered = (
                            ast.unparse(
                                target
                            )
                        )
                    except Exception:
                        continue

                    if rendered.startswith(
                        "self._runtime."
                    ):
                        composition[
                            "runtime_assignments"
                        ].append(
                            (
                                node.lineno,
                                rendered,
                            )
                        )

            if isinstance(
                node,
                ast.Call,
            ):
                try:
                    function = (
                        ast.unparse(
                            node.func
                        )
                    )

                    text = (
                        ast.unparse(
                            node
                        )
                    )
                except Exception:
                    continue

                if (
                    function
                    in {
                        "setattr",
                        "object.__setattr__",
                    }
                    and "_runtime"
                    in text
                ):
                    composition[
                        "runtime_setattr"
                    ].append(
                        (
                            node.lineno,
                            text,
                        )
                    )

                if (
                    function.startswith(
                        "self._runtime."
                    )
                    and any(
                        marker
                        in function.lower()
                        for marker
                        in (
                            "callback",
                            "hook",
                            "listener",
                            "observer",
                        )
                    )
                ):
                    composition[
                        "runtime_callbacks"
                    ].append(
                        (
                            node.lineno,
                            function,
                        )
                    )

    return {
        "bad_imports":
            bad_imports,
        "bad_calls":
            bad_calls,
        "persistence_imports":
            persistence_imports,
        "persistence_calls":
            persistence_calls,
        "composition":
            composition,
    }


def fsync_directory(
    path: Path,
) -> None:
    fd = os.open(
        path,
        os.O_RDONLY,
    )

    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def reserve_result_slot() -> int:
    if RESULT.exists():
        raise RuntimeError(
            "final validation result "
            "already exists"
        )

    if RESULT_TEMP.exists():
        raise RuntimeError(
            "temporary validation result "
            "already exists"
        )

    return os.open(
        RESULT_TEMP,
        (
            os.O_WRONLY
            | os.O_CREAT
            | os.O_EXCL
        ),
        0o600,
    )


def rename_noreplace(
    source: Path,
    destination: Path,
) -> None:
    libc = ctypes.CDLL(
        None,
        use_errno=True,
    )

    try:
        renameat2 = (
            libc.renameat2
        )
    except AttributeError as exc:
        raise RuntimeError(
            "result publisher requires "
            "libc renameat2"
        ) from exc

    renameat2.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    ]

    renameat2.restype = (
        ctypes.c_int
    )

    AT_FDCWD = -100
    RENAME_NOREPLACE = 1

    rc = renameat2(
        AT_FDCWD,
        os.fsencode(source),
        AT_FDCWD,
        os.fsencode(destination),
        RENAME_NOREPLACE,
    )

    if rc == 0:
        return

    code = ctypes.get_errno()

    if code == errno.EEXIST:
        raise FileExistsError(
            code,
            "final validation result "
            "already exists",
            str(destination),
        )

    raise OSError(
        code,
        os.strerror(code),
        str(destination),
    )


def publish_result(
    reservation_fd: int,
    result: dict,
) -> None:
    payload = (
        json.dumps(
            result,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
        + "\n"
    ).encode(
        "utf-8"
    )

    try:
        os.write(
            reservation_fd,
            payload,
        )

        os.fsync(
            reservation_fd
        )

    finally:
        os.close(
            reservation_fd
        )

    fsync_directory(
        RESULT_TEMP.parent
    )

    rename_noreplace(
        RESULT_TEMP,
        RESULT,
    )

    fsync_directory(
        RESULT.parent
    )


def guard_false_packet() -> None:
    print(
        "🟨📦 ===== GOLD STANDARD "
        "RETURN PACKET ===== 📦🟨"
    )

    print(
        "STATUS             : "
        "VALIDATION V1.1 RUNNER "
        "GUARD-FALSE / UNARMED"
    )

    print(
        "PROJECT IMPORTS    : NONE"
    )

    print(
        "FIXTURE CREATION   : NONE"
    )

    print(
        "VALIDATION RUN     : NONE"
    )

    print(
        "SCIENTIFIC RUN     : NONE"
    )

    print(
        "RESULT             : "
        + (
            "PRESENT"
            if RESULT.exists()
            else "ABSENT"
        )
    )

    print(
        "RESULT TEMP        : "
        + (
            "PRESENT"
            if RESULT_TEMP.exists()
            else "ABSENT"
        )
    )

    print(
        "RESULT SLOT        : UNSPENT"
    )

    print(
        "🟨📦 ===== END GOLD STANDARD "
        "RETURN PACKET ===== 📦🟨"
    )

def _canonical_fixture_pk(
    prefix: str,
    seed: bytes,
) -> str:
    return (
        prefix
        + hashlib.sha256(
            seed
        ).hexdigest()
    )


def _require_fixture_sha256(
    value: str,
    name: str,
) -> str:
    if (
        type(value) is not str
        or len(value) != 64
        or any(
            ch not in "0123456789abcdef"
            for ch in value
        )
    ):
        raise RuntimeError(
            name
            + " is not canonical lowercase SHA256"
        )

    return value


def _require_fixture_pk(
    value: str,
    prefix: str,
    name: str,
) -> str:
    if (
        type(value) is not str
        or not value.startswith(
            prefix
        )
    ):
        raise RuntimeError(
            name
            + " does not use canonical prefix "
            + prefix
        )

    _require_fixture_sha256(
        value[
            len(prefix):
        ],
        name + " suffix",
    )

    return value


def build_validation_fixture_v1_1(
    temp_root: Path,
    resident_directory,
):
    payloads = (
        b"A" * 64,
        b"B" * 96,
        b"C" * 128,
        b"D" * 160,
    )

    segment_bytes = b"".join(
        payloads
    )

    segment_path = (
        temp_root
        / "segment_00000000.mafseg"
    )

    segment_path.write_bytes(
        segment_bytes
    )

    model_pk = (
        _canonical_fixture_pk(
            "mafmodel:v1:",
            b"validation-model-v1.1",
        )
    )

    generation_pk = (
        _canonical_fixture_pk(
            "mafgen:v1:",
            b"validation-generation-v1.1",
        )
    )

    manifest_sha256 = (
        hashlib.sha256(
            b"validation-manifest-v1.1"
        ).hexdigest()
    )

    segment_sha256 = (
        hashlib.sha256(
            segment_bytes
        ).hexdigest()
    )

    _require_fixture_pk(
        model_pk,
        "mafmodel:v1:",
        "model_pk",
    )

    _require_fixture_pk(
        generation_pk,
        "mafgen:v1:",
        "generation_pk",
    )

    _require_fixture_sha256(
        manifest_sha256,
        "generation_manifest_sha256",
    )

    _require_fixture_sha256(
        segment_sha256,
        "segment_sha256",
    )

    entries_list = []

    offset = 0

    for index, payload in enumerate(
        payloads
    ):
        object_pk = (
            _canonical_fixture_pk(
                "mafobj:v1:",
                (
                    "validation-object-v1.1-"
                    + str(index)
                ).encode(
                    "utf-8"
                ),
            )
        )

        payload_sha256 = (
            hashlib.sha256(
                payload
            ).hexdigest()
        )

        _require_fixture_pk(
            object_pk,
            "mafobj:v1:",
            "object_pk",
        )

        _require_fixture_sha256(
            payload_sha256,
            "payload_sha256",
        )

        entry = (
            resident_directory
            .ResidentPKEntry(
                model_pk=
                    model_pk,
                generation_pk=
                    generation_pk,
                generation_manifest_sha256=
                    manifest_sha256,
                object_pk=
                    object_pk,
                segment_id=
                    "segment:00000000",
                offset=
                    offset,
                length=
                    len(payload),
                object_file_sha256=
                    payload_sha256,
                payload_sha256=
                    payload_sha256,
                segment_length=
                    len(
                        segment_bytes
                    ),
                segment_sha256=
                    segment_sha256,
                segment_path=
                    str(
                        segment_path
                    ),
            )
        )

        if (
            type(entry.offset) is not int
            or entry.offset < 0
        ):
            raise RuntimeError(
                "fixture offset is invalid"
            )

        if (
            type(entry.length) is not int
            or entry.length <= 0
        ):
            raise RuntimeError(
                "fixture length is invalid"
            )

        if (
            type(entry.segment_length)
            is not int
            or entry.segment_length <= 0
        ):
            raise RuntimeError(
                "fixture segment_length is invalid"
            )

        if (
            entry.offset
            + entry.length
            > entry.segment_length
        ):
            raise RuntimeError(
                "fixture object range exceeds segment"
            )

        entries_list.append(
            entry
        )

        offset += len(
            payload
        )

    entries = tuple(
        entries_list
    )

    if len(entries) != 4:
        raise RuntimeError(
            "fixture must contain exactly four entries"
        )

    if (
        len(
            {
                entry.object_pk
                for entry in entries
            }
        )
        != len(entries)
    ):
        raise RuntimeError(
            "fixture object_pk values are not unique"
        )

    if (
        segment_path.stat().st_size
        != len(segment_bytes)
    ):
        raise RuntimeError(
            "fixture segment length mismatch"
        )

    if (
        sha256_file(
            segment_path
        )
        != segment_sha256
    ):
        raise RuntimeError(
            "fixture segment SHA mismatch"
        )

    return (
        payloads,
        segment_bytes,
        segment_path,
        model_pk,
        generation_pk,
        manifest_sha256,
        segment_sha256,
        entries,
    )


def qualify_validation_fixture_v1_1():
    # This is harness qualification, not scientific
    # execution. Project imports occur only when the
    # qualification mode or armed pre-spend path calls it.

    sys.path.insert(
        0,
        str(ROOT),
    )

    import maf_object_runtime_residency_v1 as runtime_module
    import maf_resident_pk_directory_v1 as resident_directory
    import maf_segment_locality_runtime_telemetry_integration_v1 as integration

    with tempfile.TemporaryDirectory(
        prefix=(
            "openmind-maf-integration-"
            "v1-1-qualification-"
        )
    ) as temp_raw:
        temp_root = Path(
            temp_raw
        )

        (
            _payloads,
            segment_bytes,
            _segment_path,
            model_pk,
            generation_pk,
            manifest_sha256,
            _segment_sha256,
            entries,
        ) = build_validation_fixture_v1_1(
            temp_root,
            resident_directory,
        )

        runtime = (
            runtime_module
            .MAFObjectRuntime(
                model_pk=
                    model_pk,
                generation_pk=
                    generation_pk,
                serialized_byte_budget=
                    max(
                        1,
                        len(segment_bytes)
                        * 2,
                    ),
                dense_byte_budget=
                    max(
                        1,
                        len(segment_bytes)
                        * 2,
                    ),
            )
        )

        adapter = None

        try:
            adapter = (
                integration
                .MAFSegmentLocalityRuntimeTelemetryAdapter(
                    runtime,
                    source_manifest_sha256=
                        manifest_sha256,
                )
            )

            expected = tuple(
                (
                    entry.object_pk,
                    entry.length,
                )
                for entry in entries
            )

            for entry in entries:
                adapter.register_entry(
                    entry
                )

            observed = tuple(
                (
                    record.entry.object_pk,
                    record.entry.length,
                )
                for record
                in runtime._records.values()
            )

            if observed != expected:
                raise RuntimeError(
                    "qualification registration "
                    "did not preserve object order/length"
                )

            if len(observed) != 4:
                raise RuntimeError(
                    "qualification runtime does not "
                    "contain exactly four objects"
                )

            if any(
                not object_pk.startswith(
                    "mafobj:v1:"
                )
                for object_pk, _length
                in observed
            ):
                raise RuntimeError(
                    "qualification object_pk prefix mismatch"
                )

            return {
                "entry_count":
                    len(observed),
                "model_pk":
                    model_pk,
                "generation_pk":
                    generation_pk,
                "manifest_sha256":
                    manifest_sha256,
                "registration":
                    observed,
            }

        finally:
            if adapter is not None:
                adapter.close()
            else:
                runtime.close()


def fixture_qualification_packet_v1_1() -> int:
    if RESULT.exists():
        raise SystemExit(
            "REFUSED: Validation V1.1 final result "
            "already exists."
        )

    if RESULT_TEMP.exists():
        raise SystemExit(
            "REFUSED: Validation V1.1 temporary "
            "result already exists."
        )

    if not authority_exact():
        raise SystemExit(
            "REFUSED: frozen authority SHA gate "
            "failed before fixture qualification."
        )

    if not RESIDENT_DIRECTORY.is_file():
        raise SystemExit(
            "REFUSED: resident PK directory "
            "implementation is missing."
        )

    resident_sha = (
        sha256_file(
            RESIDENT_DIRECTORY
        )
    )

    if (
        resident_sha
        != RESIDENT_DIRECTORY_KNOWN_SHA256
    ):
        raise SystemExit(
            "REFUSED: resident PK directory "
            "execution dependency does not match "
            "accepted Phase 6C authority."
        )

    qualification = (
        qualify_validation_fixture_v1_1()
    )

    if RESULT.exists() or RESULT_TEMP.exists():
        raise RuntimeError(
            "fixture qualification touched "
            "the exact-once result namespace"
        )

    print(
        "🟨📦 ===== GOLD STANDARD "
        "RETURN PACKET ===== 📦🟨"
    )

    print(
        "STATUS             : "
        "VALIDATION V1.1 FIXTURE QUALIFICATION PASS"
    )

    print(
        "ENTRY COUNT        : "
        + str(
            qualification[
                "entry_count"
            ]
        )
    )

    print(
        "MODEL PK PREFIX    : "
        + (
            "PASS"
            if qualification[
                "model_pk"
            ].startswith(
                "mafmodel:v1:"
            )
            else "FAIL"
        )
    )

    print(
        "GENERATION PREFIX  : "
        + (
            "PASS"
            if qualification[
                "generation_pk"
            ].startswith(
                "mafgen:v1:"
            )
            else "FAIL"
        )
    )

    print(
        "OBJECT PK PREFIXES : PASS"
    )

    print(
        "RUNTIME REGISTER   : PASS"
    )

    print(
        "ADAPTER ATTACHMENT : PASS"
    )

    print(
        "V01..V42 EXECUTED  : NONE"
    )

    print(
        "RESULT             : ABSENT"
    )

    print(
        "RESULT TEMP        : ABSENT"
    )

    print(
        "RESULT SLOT        : UNSPENT"
    )

    print(
        "SCIENTIFIC RUN     : NONE"
    )

    print(
        "🟨📦 ===== END GOLD STANDARD "
        "RETURN PACKET ===== 📦🟨"
    )

    return 0



def run_scientific_validation():
    # These project imports occur only after
    # the explicit exact-once arming gate.
    sys.path.insert(
        0,
        str(ROOT),
    )

    import maf_object_runtime_residency_v1 as runtime_module
    import maf_resident_pk_directory_v1 as resident_directory
    import maf_segment_locality_runtime_telemetry_integration_v1 as integration

    recorder = CheckRecorder()

    frozen_before = (
        authority_inventory()
    )

    probe = AuditProbe()

    sys.addaudithook(
        probe.hook
    )

    def dense_materializer(
        entry,
        serialized: bytes,
    ):
        digest = hashlib.sha256(
            serialized
        ).hexdigest()

        view = (
            "validation-dense-view",
            entry.model_pk,
            entry.generation_pk,
            entry.object_pk,
            digest,
            len(serialized),
        )

        return (
            view,
            len(serialized),
        )

    def failing_materializer(
        entry,
        serialized: bytes,
    ):
        del entry
        del serialized

        raise RuntimeError(
            "validation dense "
            "materializer failure"
        )

    with tempfile.TemporaryDirectory(
        prefix=(
            "openmind-maf-"
            "integration-v1-"
        )
    ) as temp_raw:
        temp_root = Path(
            temp_raw
        )

        (
            payloads,
            segment_bytes,
            segment_path,
            model_pk,
            generation_pk,
            manifest_sha256,
            segment_sha256,
            entries,
        ) = build_validation_fixture_v1_1(
            temp_root,
            resident_directory,
        )

        source_before = {
            "segment_sha256":
                sha256_file(
                    segment_path
                ),
            "segment_length":
                segment_path
                .stat()
                .st_size,
            "entries":
                canonical(
                    entries
                ),
        }

        def new_runtime(
            *,
            materializer=
                dense_materializer,
            selected_entries=(),
            model_identity=
                model_pk,
            generation_identity=
                generation_pk,
        ):
            runtime = (
                runtime_module
                .MAFObjectRuntime(
                    model_pk=
                        model_identity,
                    generation_pk=
                        generation_identity,
                    serialized_byte_budget=
                        1024 * 1024,
                    dense_byte_budget=
                        1024 * 1024,
                    dense_materializer=
                        materializer,
                )
            )

            for entry in (
                selected_entries
            ):
                runtime.register_entry(
                    entry
                )

            return runtime

        def new_adapter(
            *,
            selected_entries=
                entries,
            materializer=
                dense_materializer,
            source_manifest_sha256=
                manifest_sha256,
            fail_telemetry=False,
        ):
            runtime = (
                new_runtime(
                    materializer=
                        materializer
                )
            )

            adapter = (
                integration
                .MAFSegmentLocalityRuntimeTelemetryAdapter(
                    runtime,
                    source_manifest_sha256=
                        source_manifest_sha256,
                )
            )

            recording = (
                RecordingAccumulator(
                    adapter._accumulator,
                    fail=
                        fail_telemetry,
                )
            )

            adapter._accumulator = (
                recording
            )

            for entry in (
                selected_entries
            ):
                adapter.register_entry(
                    entry
                )

            return (
                runtime,
                adapter,
                recording,
            )

        def new_pair(
            *,
            selected_entries=
                entries,
            materializer=
                dense_materializer,
        ):
            control = (
                new_runtime(
                    materializer=
                        materializer,
                    selected_entries=
                        selected_entries,
                )
            )

            (
                integrated_runtime,
                adapter,
                recording,
            ) = new_adapter(
                selected_entries=
                    selected_entries,
                materializer=
                    materializer,
            )

            return (
                control,
                integrated_runtime,
                adapter,
                recording,
            )

        def clear_events(
            recording,
        ) -> None:
            recording.events.clear()

        def exact_events(
            recording,
            expected,
        ):
            observed = (
                event_kinds(
                    recording.events
                )
            )

            return (
                observed
                == expected,
                {
                    "expected":
                        expected,
                    "observed":
                        observed,
                    "events":
                        canonical(
                            recording.events
                        ),
                },
            )

        def compare_failures(
            control_fn,
            integrated_fn,
        ):
            control_error = (
                capture_exception(
                    control_fn
                )
            )

            integrated_error = (
                capture_exception(
                    integrated_fn
                )
            )

            return (
                control_error
                is not None
                and integrated_error
                == control_error,
                {
                    "control":
                        control_error,
                    "integrated":
                        integrated_error,
                },
            )

        # --------------------------------------------------
        # V01 — exact predecessor identity
        # --------------------------------------------------

        recorder.run(
            "V01",
            lambda: (
                authority_exact(),
                authority_inventory(),
            ),
        )

        # --------------------------------------------------
        # V02 — runtime bytes unchanged
        # --------------------------------------------------

        recorder.run(
            "V02",
            lambda: (
                sha256_file(
                    ROOT
                    / AUTH[
                        "runtime"
                    ][0]
                )
                == AUTH[
                    "runtime"
                ][1],
                sha256_file(
                    ROOT
                    / AUTH[
                        "runtime"
                    ][0]
                ),
            ),
        )

        # --------------------------------------------------
        # V03 — data-model bytes unchanged
        # --------------------------------------------------

        recorder.run(
            "V03",
            lambda: (
                sha256_file(
                    ROOT
                    / AUTH[
                        "data_model"
                    ][0]
                )
                == AUTH[
                    "data_model"
                ][1],
                sha256_file(
                    ROOT
                    / AUTH[
                        "data_model"
                    ][0]
                ),
            ),
        )

        # --------------------------------------------------
        # V04 — persistence bytes unchanged
        # --------------------------------------------------

        recorder.run(
            "V04",
            lambda: (
                sha256_file(
                    ROOT
                    / AUTH[
                        "persistence"
                    ][0]
                )
                == AUTH[
                    "persistence"
                ][1],
                sha256_file(
                    ROOT
                    / AUTH[
                        "persistence"
                    ][0]
                ),
            ),
        )

        # --------------------------------------------------
        # V05 — clean empty attachment
        # --------------------------------------------------

        def v05():
            runtime = (
                new_runtime()
            )

            adapter = (
                integration
                .MAFSegmentLocalityRuntimeTelemetryAdapter(
                    runtime,
                    source_manifest_sha256=
                        manifest_sha256,
                )
            )

            runtime_snapshot = (
                runtime.snapshot()
            )

            telemetry_snapshot = (
                adapter
                .telemetry_snapshot()
            )

            passed = (
                runtime_snapshot
                .object_count
                == 0
                and telemetry_snapshot
                .event_count
                == 0
                and telemetry_snapshot
                .first_sequence
                is None
                and telemetry_snapshot
                .last_sequence
                is None
            )

            return (
                passed,
                {
                    "runtime":
                        canonical(
                            runtime_snapshot
                        ),
                    "telemetry":
                        canonical(
                            telemetry_snapshot
                        ),
                },
            )

        recorder.run(
            "V05",
            v05,
        )

        # --------------------------------------------------
        # V06 — exact binding and valid-but-wrong authority
        # --------------------------------------------------

        def v06():
            runtime = (
                new_runtime()
            )

            adapter = (
                integration
                .MAFSegmentLocalityRuntimeTelemetryAdapter(
                    runtime,
                    source_manifest_sha256=
                        manifest_sha256,
                )
            )

            adapter.register_entry(
                entries[0]
            )

            telemetry = (
                adapter
                .telemetry_snapshot()
            )

            exact_binding = (
                telemetry.model_pk
                == model_pk
                and telemetry
                .source_generation_pk
                == generation_pk
                and telemetry
                .source_manifest_sha256
                == manifest_sha256
            )

            wrong_manifest_runtime = (
                new_runtime()
            )

            wrong_manifest_adapter = (
                integration
                .MAFSegmentLocalityRuntimeTelemetryAdapter(
                    wrong_manifest_runtime,
                    source_manifest_sha256=
                        "e" * 64,
                )
            )

            manifest_error = (
                capture_exception(
                    lambda:
                        wrong_manifest_adapter
                        .register_entry(
                            entries[0]
                        )
                )
            )

            wrong_model_runtime = (
                new_runtime()
            )

            wrong_model_adapter = (
                integration
                .MAFSegmentLocalityRuntimeTelemetryAdapter(
                    wrong_model_runtime,
                    source_manifest_sha256=
                        manifest_sha256,
                )
            )

            wrong_model_entry = (
                dataclasses.replace(
                    entries[0],
                    model_pk=
                        "d" * 64,
                )
            )

            model_error = (
                capture_exception(
                    lambda:
                        wrong_model_adapter
                        .register_entry(
                            wrong_model_entry
                        )
                )
            )

            wrong_generation_runtime = (
                new_runtime()
            )

            wrong_generation_adapter = (
                integration
                .MAFSegmentLocalityRuntimeTelemetryAdapter(
                    wrong_generation_runtime,
                    source_manifest_sha256=
                        manifest_sha256,
                )
            )

            wrong_generation_entry = (
                dataclasses.replace(
                    entries[0],
                    generation_pk=
                        "c" * 64,
                )
            )

            generation_error = (
                capture_exception(
                    lambda:
                        wrong_generation_adapter
                        .register_entry(
                            wrong_generation_entry
                        )
                )
            )

            passed = (
                exact_binding
                and manifest_error
                is not None
                and model_error
                is not None
                and generation_error
                is not None
            )

            return (
                passed,
                {
                    "binding": {
                        "model_pk":
                            telemetry.model_pk,
                        "generation_pk":
                            telemetry
                            .source_generation_pk,
                        "manifest_sha256":
                            telemetry
                            .source_manifest_sha256,
                    },
                    "wrong_manifest":
                        manifest_error,
                    "wrong_model":
                        model_error,
                    "wrong_generation":
                        generation_error,
                },
            )

        recorder.run(
            "V06",
            v06,
        )
        # --------------------------------------------------
        # V07 — first committed sequence equals 1
        # V08 — every committed sequence increments by 1
        # --------------------------------------------------

        (
            _sequence_runtime,
            sequence_adapter,
            sequence_recording,
        ) = new_adapter(
            selected_entries=(
                entries[0],
            )
        )

        sequence_adapter.ensure_state(
            entries[0].object_pk,
            runtime_module
            .ResidencyState
            .HOT_MAF,
        )

        sequences = [
            event.sequence
            for event
            in sequence_recording.events
        ]

        recorder.add(
            "V07",
            bool(sequences)
            and sequences[0] == 1,
            {
                "sequences":
                    sequences,
            },
        )

        recorder.add(
            "V08",
            sequences
            == list(
                range(
                    1,
                    len(sequences) + 1,
                )
            ),
            {
                "sequences":
                    sequences,
            },
        )

        # --------------------------------------------------
        # V09–V12 — serialized/dense ACCESS + cache result
        # --------------------------------------------------

        def access_case(
            *,
            dense: bool,
            ready: bool,
        ):
            (
                _runtime,
                adapter,
                recording,
            ) = new_adapter(
                selected_entries=(
                    entries[0],
                )
            )

            if ready:
                adapter.ensure_state(
                    entries[0].object_pk,
                    (
                        runtime_module
                        .ResidencyState
                        .HOT_DENSE
                        if dense
                        else runtime_module
                        .ResidencyState
                        .HOT_MAF
                    ),
                )

            clear_events(
                recording
            )

            function = (
                adapter.dense_view
                if dense
                else adapter.serialized_bytes
            )

            observed_value = None
            observed_error = None

            try:
                observed_value = function(
                    entries[0].object_pk
                )
            except Exception as exc:
                observed_error = (
                    type(exc).__name__,
                    str(exc),
                )

            expected_events = (
                [
                    "ACCESS",
                    "CACHE_HIT",
                ]
                if ready
                else [
                    "ACCESS",
                    "CACHE_MISS",
                ]
            )

            event_ok, event_detail = (
                exact_events(
                    recording,
                    expected_events,
                )
            )

            if ready:
                outcome_ok = (
                    observed_error is None
                    and observed_value
                    is not None
                )

            else:
                outcome_ok = (
                    observed_error
                    is not None
                    and observed_error[0]
                    == (
                        "MAFObjectRuntime"
                        "ResidencyUnavailableError"
                    )
                )

            return (
                event_ok
                and outcome_ok,
                {
                    "dense":
                        dense,
                    "ready":
                        ready,
                    "value":
                        canonical(
                            observed_value
                        ),
                    "exception":
                        observed_error,
                    "events":
                        event_detail,
                },
            )

        # V09 — serialized success ACCESS/HIT

        recorder.run(
            "V09",
            lambda:
                access_case(
                    dense=False,
                    ready=True,
                ),
        )

        # V10 — serialized unavailable ACCESS/MISS

        recorder.run(
            "V10",
            lambda:
                access_case(
                    dense=False,
                    ready=False,
                ),
        )

        # V11 — dense success ACCESS/HIT

        recorder.run(
            "V11",
            lambda:
                access_case(
                    dense=True,
                    ready=True,
                ),
        )

        # V12 — dense unavailable ACCESS/MISS

        recorder.run(
            "V12",
            lambda:
                access_case(
                    dense=True,
                    ready=False,
                ),
        )

        # --------------------------------------------------
        # V13 — unknown object produces no ACCESS/cache event
        # V14 — closed runtime produces no ACCESS/cache event
        # --------------------------------------------------

        def pre_access_failure_case(
            *,
            closed: bool,
        ):
            (
                _runtime,
                adapter,
                recording,
            ) = new_adapter(
                selected_entries=(
                    entries[0],
                )
            )

            if closed:
                adapter.close()

            clear_events(
                recording
            )

            object_pk = (
                entries[0].object_pk
                if closed
                else "f" * 64
            )

            observed_error = (
                capture_exception(
                    lambda:
                        adapter
                        .serialized_bytes(
                            object_pk
                        )
                )
            )

            access_cache_events = [
                canonical(event)
                for event
                in recording.events
                if event_kind(event)
                in {
                    "ACCESS",
                    "CACHE_HIT",
                    "CACHE_MISS",
                }
            ]

            return (
                observed_error
                is not None
                and not access_cache_events,
                {
                    "closed":
                        closed,
                    "exception":
                        observed_error,
                    "access_cache_events":
                        access_cache_events,
                    "all_events":
                        canonical(
                            recording.events
                        ),
                },
            )

        recorder.run(
            "V13",
            lambda:
                pre_access_failure_case(
                    closed=False
                ),
        )

        recorder.run(
            "V14",
            lambda:
                pre_access_failure_case(
                    closed=True
                ),
        )
        # --------------------------------------------------
        # V15–V20 — exact residency primitive telemetry
        # --------------------------------------------------

        def transition_case(
            *,
            start_state,
            target_state,
            expected_events,
            entry=entries[0],
        ):
            (
                _runtime,
                adapter,
                recording,
            ) = new_adapter(
                selected_entries=(
                    entry,
                )
            )

            if start_state is not None:
                adapter.ensure_state(
                    entry.object_pk,
                    start_state,
                )

            clear_events(
                recording
            )

            result = adapter.transition(
                entry.object_pk,
                target_state,
            )

            event_ok, detail = (
                exact_events(
                    recording,
                    expected_events,
                )
            )

            return (
                event_ok,
                {
                    "result":
                        canonical(
                            result
                        ),
                    "events":
                        detail,
                },
            )

        # V15 — cold -> mapped promotion

        recorder.run(
            "V15",
            lambda:
                transition_case(
                    start_state=None,
                    target_state=(
                        runtime_module
                        .ResidencyState
                        .MAPPED
                    ),
                    expected_events=[
                        "PROMOTION",
                    ],
                ),
        )

        # V16 — mapped -> hot-maf:
        # BYTES_READ then PROMOTION

        recorder.run(
            "V16",
            lambda:
                transition_case(
                    start_state=(
                        runtime_module
                        .ResidencyState
                        .MAPPED
                    ),
                    target_state=(
                        runtime_module
                        .ResidencyState
                        .HOT_MAF
                    ),
                    expected_events=[
                        "BYTES_READ",
                        "PROMOTION",
                    ],
                ),
        )

        # V17 — BYTES_READ equals exact ResidentPKEntry.length

        def v17():
            (
                _runtime,
                adapter,
                recording,
            ) = new_adapter(
                selected_entries=(
                    entries[1],
                )
            )

            adapter.transition(
                entries[1].object_pk,
                runtime_module
                .ResidencyState
                .MAPPED,
            )

            clear_events(
                recording
            )

            adapter.transition(
                entries[1].object_pk,
                runtime_module
                .ResidencyState
                .HOT_MAF,
            )

            byte_counts = [
                event.byte_count
                for event
                in recording.events
                if event_kind(event)
                == "BYTES_READ"
            ]

            return (
                byte_counts
                == [
                    entries[1].length
                ],
                {
                    "expected":
                        entries[1].length,
                    "observed":
                        byte_counts,
                    "events":
                        canonical(
                            recording.events
                        ),
                },
            )

        recorder.run(
            "V17",
            v17,
        )

        # V18 — hot-maf -> hot-dense:
        # MATERIALIZATION then PROMOTION

        recorder.run(
            "V18",
            lambda:
                transition_case(
                    start_state=(
                        runtime_module
                        .ResidencyState
                        .HOT_MAF
                    ),
                    target_state=(
                        runtime_module
                        .ResidencyState
                        .HOT_DENSE
                    ),
                    expected_events=[
                        "MATERIALIZATION",
                        "PROMOTION",
                    ],
                ),
        )

        # V19 — every downward primitive emits DEMOTION

        def v19():
            (
                _runtime,
                adapter,
                recording,
            ) = new_adapter(
                selected_entries=(
                    entries[0],
                )
            )

            adapter.ensure_state(
                entries[0].object_pk,
                runtime_module
                .ResidencyState
                .HOT_DENSE,
            )

            clear_events(
                recording
            )

            targets = (
                runtime_module
                .ResidencyState
                .HOT_MAF,
                runtime_module
                .ResidencyState
                .MAPPED,
                runtime_module
                .ResidencyState
                .COLD_DISK,
            )

            snapshots = []

            for target in targets:
                snapshots.append(
                    adapter.transition(
                        entries[0].object_pk,
                        target,
                    )
                )

            observed = [
                (
                    event_kind(event),
                    event.from_state,
                    event.to_state,
                )
                for event
                in recording.events
            ]

            expected = [
                (
                    "DEMOTION",
                    runtime_module
                    .ResidencyState
                    .HOT_DENSE
                    .value,
                    runtime_module
                    .ResidencyState
                    .HOT_MAF
                    .value,
                ),
                (
                    "DEMOTION",
                    runtime_module
                    .ResidencyState
                    .HOT_MAF
                    .value,
                    runtime_module
                    .ResidencyState
                    .MAPPED
                    .value,
                ),
                (
                    "DEMOTION",
                    runtime_module
                    .ResidencyState
                    .MAPPED
                    .value,
                    runtime_module
                    .ResidencyState
                    .COLD_DISK
                    .value,
                ),
            ]

            return (
                observed
                == expected,
                {
                    "expected":
                        expected,
                    "observed":
                        observed,
                    "snapshots":
                        canonical(
                            snapshots
                        ),
                },
            )

        recorder.run(
            "V19",
            v19,
        )

        # V20 — no skipped synthetic residency transition

        def v20():
            (
                _runtime,
                adapter,
                recording,
            ) = new_adapter(
                selected_entries=(
                    entries[0],
                )
            )

            adapter.ensure_state(
                entries[0].object_pk,
                runtime_module
                .ResidencyState
                .HOT_DENSE,
            )

            state_order = [
                state.value
                for state
                in (
                    runtime_module
                    .ResidencyState
                    .COLD_DISK,
                    runtime_module
                    .ResidencyState
                    .MAPPED,
                    runtime_module
                    .ResidencyState
                    .HOT_MAF,
                    runtime_module
                    .ResidencyState
                    .HOT_DENSE,
                )
            ]

            state_rank = {
                state:
                    index
                for index, state
                in enumerate(
                    state_order
                )
            }

            transitions = [
                (
                    event.from_state,
                    event.to_state,
                )
                for event
                in recording.events
                if event_kind(event)
                in {
                    "PROMOTION",
                    "DEMOTION",
                }
            ]

            valid = (
                bool(transitions)
                and all(
                    start
                    in state_rank
                    and end
                    in state_rank
                    and abs(
                        state_rank[start]
                        - state_rank[end]
                    )
                    == 1
                    for start, end
                    in transitions
                )
            )

            return (
                valid,
                {
                    "transitions":
                        transitions,
                },
            )

        recorder.run(
            "V20",
            v20,
        )

        # --------------------------------------------------
        # V21 — ensure_state exact control equivalence
        # --------------------------------------------------

        def v21():
            (
                control,
                _integrated_runtime,
                adapter,
                recording,
            ) = new_pair(
                selected_entries=(
                    entries[0],
                )
            )

            control_result = (
                control.ensure_state(
                    entries[0].object_pk,
                    runtime_module
                    .ResidencyState
                    .HOT_MAF,
                )
            )

            integrated_result = (
                adapter.ensure_state(
                    entries[0].object_pk,
                    runtime_module
                    .ResidencyState
                    .HOT_MAF,
                )
            )

            observed_events = (
                event_kinds(
                    recording.events
                )
            )

            expected_events = [
                "PROMOTION",
                "BYTES_READ",
                "PROMOTION",
            ]

            return (
                canonical(
                    control_result
                )
                == canonical(
                    integrated_result
                )
                and observed_events
                == expected_events,
                {
                    "control":
                        canonical(
                            control_result
                        ),
                    "integrated":
                        canonical(
                            integrated_result
                        ),
                    "expected_events":
                        expected_events,
                    "observed_events":
                        observed_events,
                },
            )

        recorder.run(
            "V21",
            v21,
        )

        # --------------------------------------------------
        # V22 — pin exact control equivalence
        # --------------------------------------------------

        def v22():
            (
                control,
                _integrated_runtime,
                adapter,
                recording,
            ) = new_pair(
                selected_entries=(
                    entries[0],
                )
            )

            control_lease = (
                control.pin(
                    entries[0].object_pk,
                    runtime_module
                    .ResidencyState
                    .HOT_MAF,
                )
            )

            integrated_lease = (
                adapter.pin(
                    entries[0].object_pk,
                    runtime_module
                    .ResidencyState
                    .HOT_MAF,
                )
            )

            observed_events = (
                event_kinds(
                    recording.events
                )
            )

            expected_events = [
                "PROMOTION",
                "BYTES_READ",
                "PROMOTION",
            ]

            return (
                canonical(
                    control_lease
                )
                == canonical(
                    integrated_lease
                )
                and observed_events
                == expected_events,
                {
                    "control_lease":
                        canonical(
                            control_lease
                        ),
                    "integrated_lease":
                        canonical(
                            integrated_lease
                        ),
                    "expected_events":
                        expected_events,
                    "observed_events":
                        observed_events,
                },
            )

        recorder.run(
            "V22",
            v22,
        )
        # --------------------------------------------------
        # V23 — partial failure records committed
        # primitives only
        # --------------------------------------------------

        def v23():
            (
                control,
                _integrated_runtime,
                adapter,
                recording,
            ) = new_pair(
                selected_entries=(
                    entries[0],
                ),
                materializer=
                    failing_materializer,
            )

            control.transition(
                entries[0].object_pk,
                runtime_module
                .ResidencyState
                .MAPPED,
            )

            adapter.transition(
                entries[0].object_pk,
                runtime_module
                .ResidencyState
                .MAPPED,
            )

            clear_events(
                recording
            )

            control_error = (
                capture_exception(
                    lambda:
                        control.ensure_state(
                            entries[0]
                            .object_pk,
                            runtime_module
                            .ResidencyState
                            .HOT_DENSE,
                        )
                )
            )

            integrated_error = (
                capture_exception(
                    lambda:
                        adapter.ensure_state(
                            entries[0]
                            .object_pk,
                            runtime_module
                            .ResidencyState
                            .HOT_DENSE,
                        )
                )
            )

            observed_events = (
                event_kinds(
                    recording.events
                )
            )

            final_state = (
                adapter.state(
                    entries[0].object_pk
                )
            )

            passed = (
                control_error
                is not None
                and integrated_error
                == control_error
                and final_state
                == runtime_module
                .ResidencyState
                .HOT_MAF
                and observed_events
                == [
                    "BYTES_READ",
                    "PROMOTION",
                ]
            )

            return (
                passed,
                {
                    "control_exception":
                        control_error,
                    "integrated_exception":
                        integrated_error,
                    "final_state":
                        final_state.value,
                    "events":
                        observed_events,
                },
            )

        recorder.run(
            "V23",
            v23,
        )

        # --------------------------------------------------
        # V24 — failure before relevant primitive commit
        # emits no residency/read/materialization event
        # --------------------------------------------------

        def v24():
            (
                _runtime,
                adapter,
                recording,
            ) = new_adapter(
                selected_entries=(
                    entries[0],
                ),
                materializer=
                    failing_materializer,
            )

            adapter.ensure_state(
                entries[0].object_pk,
                runtime_module
                .ResidencyState
                .HOT_MAF,
            )

            clear_events(
                recording
            )

            observed_error = (
                capture_exception(
                    lambda:
                        adapter.transition(
                            entries[0]
                            .object_pk,
                            runtime_module
                            .ResidencyState
                            .HOT_DENSE,
                        )
                )
            )

            forbidden_kinds = {
                "PROMOTION",
                "DEMOTION",
                "BYTES_READ",
                "MATERIALIZATION",
            }

            forbidden_events = [
                canonical(event)
                for event
                in recording.events
                if event_kind(event)
                in forbidden_kinds
            ]

            final_state = (
                adapter.state(
                    entries[0].object_pk
                )
            )

            return (
                observed_error
                is not None
                and not forbidden_events
                and final_state
                == runtime_module
                .ResidencyState
                .HOT_MAF,
                {
                    "exception":
                        observed_error,
                    "forbidden_events":
                        forbidden_events,
                    "all_events":
                        canonical(
                            recording.events
                        ),
                    "final_state":
                        final_state.value,
                },
            )

        recorder.run(
            "V24",
            v24,
        )

        # --------------------------------------------------
        # V25 — registration preserves order/length
        # and registration itself emits no telemetry
        # --------------------------------------------------

        def v25():
            runtime = (
                new_runtime()
            )

            adapter = (
                integration
                .MAFSegmentLocalityRuntimeTelemetryAdapter(
                    runtime,
                    source_manifest_sha256=
                        manifest_sha256,
                )
            )

            recording = (
                RecordingAccumulator(
                    adapter._accumulator
                )
            )

            adapter._accumulator = (
                recording
            )

            registration_order = (
                entries[2],
                entries[0],
                entries[3],
            )

            registration_results = []

            for entry in (
                registration_order
            ):
                registration_results.append(
                    adapter.register_entry(
                        entry
                    )
                )

            expected_order = tuple(
                entry.object_pk
                for entry
                in registration_order
            )

            expected_lengths = {
                entry.object_pk:
                    entry.length
                for entry
                in registration_order
            }

            observed_order = tuple(
                adapter
                ._registration_order
            )

            observed_lengths = dict(
                adapter
                ._registered_lengths
            )

            return (
                observed_order
                == expected_order
                and observed_lengths
                == expected_lengths
                and not recording.events,
                {
                    "expected_order":
                        expected_order,
                    "observed_order":
                        observed_order,
                    "expected_lengths":
                        expected_lengths,
                    "observed_lengths":
                        observed_lengths,
                    "registration_results":
                        canonical(
                            registration_results
                        ),
                    "event_count":
                        len(
                            recording.events
                        ),
                },
            )

        recorder.run(
            "V25",
            v25,
        )

        # --------------------------------------------------
        # V26 — close emits deterministic demotions
        # in registration order
        # --------------------------------------------------

        def v26():
            selected_entries = (
                entries[0],
                entries[1],
                entries[2],
            )

            (
                _runtime,
                adapter,
                recording,
            ) = new_adapter(
                selected_entries=
                    selected_entries
            )

            adapter.ensure_state(
                entries[0].object_pk,
                runtime_module
                .ResidencyState
                .HOT_DENSE,
            )

            adapter.ensure_state(
                entries[1].object_pk,
                runtime_module
                .ResidencyState
                .HOT_MAF,
            )

            adapter.ensure_state(
                entries[2].object_pk,
                runtime_module
                .ResidencyState
                .MAPPED,
            )

            clear_events(
                recording
            )

            close_result = (
                adapter.close()
            )

            observed_kinds = (
                event_kinds(
                    recording.events
                )
            )

            observed_objects = [
                event.object_pk
                for event
                in recording.events
            ]

            expected_objects = (
                [
                    entries[0].object_pk
                ] * 3
                + [
                    entries[1].object_pk
                ] * 2
                + [
                    entries[2].object_pk
                ]
            )

            return (
                close_result is None
                and observed_kinds
                == [
                    "DEMOTION",
                ] * 6
                and observed_objects
                == expected_objects,
                {
                    "kinds":
                        observed_kinds,
                    "objects":
                        observed_objects,
                    "expected_objects":
                        expected_objects,
                },
            )

        recorder.run(
            "V26",
            v26,
        )

        # --------------------------------------------------
        # V27 — exact cache names
        # --------------------------------------------------

        def v27():
            (
                _runtime,
                adapter,
                recording,
            ) = new_adapter(
                selected_entries=(
                    entries[0],
                )
            )

            # Serialized MISS.
            capture_exception(
                lambda:
                    adapter
                    .serialized_bytes(
                        entries[0]
                        .object_pk
                    )
            )

            # Serialized HIT.
            adapter.ensure_state(
                entries[0].object_pk,
                runtime_module
                .ResidencyState
                .HOT_MAF,
            )

            adapter.serialized_bytes(
                entries[0].object_pk
            )

            # Dense MISS.
            capture_exception(
                lambda:
                    adapter.dense_view(
                        entries[0]
                        .object_pk
                    )
            )

            # Dense HIT.
            adapter.transition(
                entries[0].object_pk,
                runtime_module
                .ResidencyState
                .HOT_DENSE,
            )

            adapter.dense_view(
                entries[0].object_pk
            )

            cache_events = [
                event
                for event
                in recording.events
                if event_kind(event)
                in {
                    "CACHE_HIT",
                    "CACHE_MISS",
                }
            ]

            observed_names = [
                event.cache_name
                for event
                in cache_events
            ]

            allowed_names = {
                integration
                .SERIALIZED_RESIDENCY_CACHE,
                integration
                .DENSE_RESIDENCY_CACHE,
            }

            passed = (
                bool(
                    observed_names
                )
                and set(
                    observed_names
                )
                == allowed_names
                and all(
                    name
                    in allowed_names
                    for name
                    in observed_names
                )
            )

            return (
                passed,
                {
                    "observed_names":
                        observed_names,
                    "allowed_names":
                        sorted(
                            allowed_names
                        ),
                    "cache_events":
                        canonical(
                            cache_events
                        ),
                },
            )

        recorder.run(
            "V27",
            v27,
        )

        # --------------------------------------------------
        # V28 — state/snapshot/unpin do not manufacture
        # ACCESS or cache telemetry
        # --------------------------------------------------

        def v28():
            (
                _runtime,
                adapter,
                recording,
            ) = new_adapter(
                selected_entries=(
                    entries[0],
                )
            )

            lease = adapter.pin(
                entries[0].object_pk,
                runtime_module
                .ResidencyState
                .MAPPED,
            )

            clear_events(
                recording
            )

            state_result = (
                adapter.state(
                    entries[0].object_pk
                )
            )

            snapshot_result = (
                adapter.snapshot()
            )

            unpin_result = (
                adapter.unpin(
                    lease.token
                )
            )

            access_cache_events = [
                canonical(event)
                for event
                in recording.events
                if event_kind(event)
                in {
                    "ACCESS",
                    "CACHE_HIT",
                    "CACHE_MISS",
                }
            ]

            return (
                unpin_result is None
                and not access_cache_events,
                {
                    "state":
                        canonical(
                            state_result
                        ),
                    "snapshot":
                        canonical(
                            snapshot_result
                        ),
                    "unpin_result":
                        canonical(
                            unpin_result
                        ),
                    "access_cache_events":
                        access_cache_events,
                    "all_events":
                        canonical(
                            recording.events
                        ),
                },
            )

        recorder.run(
            "V28",
            v28,
        )

        # --------------------------------------------------
        # V29 — prefetch remains unsupported / zero
        # --------------------------------------------------

        def v29():
            (
                _runtime,
                adapter,
                recording,
            ) = new_adapter(
                selected_entries=(
                    entries[0],
                )
            )

            adapter.ensure_state(
                entries[0].object_pk,
                runtime_module
                .ResidencyState
                .HOT_DENSE,
            )

            telemetry_snapshot = (
                adapter
                .telemetry_snapshot()
            )

            return prefetch_zero(
                telemetry_snapshot,
                recording.events,
            )

        recorder.run(
            "V29",
            v29,
        )
        # --------------------------------------------------
        # V30 — successful runtime outcomes preserved across
        # the complete shared public API surface
        # --------------------------------------------------

        def v30():
            control = new_runtime()

            integrated_runtime = (
                new_runtime()
            )

            adapter = (
                integration
                .MAFSegmentLocalityRuntimeTelemetryAdapter(
                    integrated_runtime,
                    source_manifest_sha256=
                        manifest_sha256,
                )
            )

            rows = []
            all_equal = True

            def compare(
                operation,
                control_fn,
                integrated_fn,
            ):
                nonlocal all_equal

                control_value = (
                    control_fn()
                )

                integrated_value = (
                    integrated_fn()
                )

                equal = (
                    canonical(
                        control_value
                    )
                    == canonical(
                        integrated_value
                    )
                )

                all_equal = (
                    all_equal
                    and equal
                )

                rows.append(
                    {
                        "operation":
                            operation,
                        "equal":
                            equal,
                        "control":
                            canonical(
                                control_value
                            ),
                        "integrated":
                            canonical(
                                integrated_value
                            ),
                    }
                )

                return (
                    control_value,
                    integrated_value,
                )

            compare(
                "register_entry",
                lambda:
                    control.register_entry(
                        entries[0]
                    ),
                lambda:
                    adapter.register_entry(
                        entries[0]
                    ),
            )

            compare(
                "state",
                lambda:
                    control.state(
                        entries[0]
                        .object_pk
                    ),
                lambda:
                    adapter.state(
                        entries[0]
                        .object_pk
                    ),
            )

            compare(
                "transition",
                lambda:
                    control.transition(
                        entries[0]
                        .object_pk,
                        runtime_module
                        .ResidencyState
                        .MAPPED,
                    ),
                lambda:
                    adapter.transition(
                        entries[0]
                        .object_pk,
                        runtime_module
                        .ResidencyState
                        .MAPPED,
                    ),
            )

            compare(
                "ensure_state",
                lambda:
                    control.ensure_state(
                        entries[0]
                        .object_pk,
                        runtime_module
                        .ResidencyState
                        .HOT_MAF,
                    ),
                lambda:
                    adapter.ensure_state(
                        entries[0]
                        .object_pk,
                        runtime_module
                        .ResidencyState
                        .HOT_MAF,
                    ),
            )

            (
                control_lease,
                integrated_lease,
            ) = compare(
                "pin",
                lambda:
                    control.pin(
                        entries[0]
                        .object_pk,
                        runtime_module
                        .ResidencyState
                        .HOT_MAF,
                    ),
                lambda:
                    adapter.pin(
                        entries[0]
                        .object_pk,
                        runtime_module
                        .ResidencyState
                        .HOT_MAF,
                    ),
            )

            compare(
                "serialized_bytes",
                lambda:
                    control
                    .serialized_bytes(
                        entries[0]
                        .object_pk
                    ),
                lambda:
                    adapter
                    .serialized_bytes(
                        entries[0]
                        .object_pk
                    ),
            )

            compare(
                "unpin",
                lambda:
                    control.unpin(
                        control_lease.token
                    ),
                lambda:
                    adapter.unpin(
                        integrated_lease.token
                    ),
            )

            compare(
                "ensure_hot_dense",
                lambda:
                    control.ensure_state(
                        entries[0]
                        .object_pk,
                        runtime_module
                        .ResidencyState
                        .HOT_DENSE,
                    ),
                lambda:
                    adapter.ensure_state(
                        entries[0]
                        .object_pk,
                        runtime_module
                        .ResidencyState
                        .HOT_DENSE,
                    ),
            )

            compare(
                "dense_view",
                lambda:
                    control.dense_view(
                        entries[0]
                        .object_pk
                    ),
                lambda:
                    adapter.dense_view(
                        entries[0]
                        .object_pk
                    ),
            )

            (
                control_snapshot,
                integrated_snapshot,
            ) = compare(
                "snapshot",
                control.snapshot,
                adapter.snapshot,
            )

            snapshot_equal = (
                canonical(
                    control_snapshot
                )
                == canonical(
                    integrated_snapshot
                )
            )

            compare(
                "close",
                control.close,
                adapter.close,
            )

            return (
                bool(all_equal),
                {
                    "rows":
                        rows,
                    "snapshot_equal":
                        snapshot_equal,
                },
            )

        (
            v30_passed,
            v30_detail,
        ) = v30()

        recorder.add(
            "V30",
            v30_passed,
            v30_detail,
        )

        # --------------------------------------------------
        # V31 — authoritative failure type/message preserved
        # --------------------------------------------------

        def v31():
            rows = []
            all_equal = True

            # Unknown object.
            (
                control,
                _integrated_runtime,
                adapter,
                _recording,
            ) = new_pair(
                selected_entries=(
                    entries[0],
                )
            )

            passed, detail = (
                compare_failures(
                    lambda:
                        control.state(
                            "f" * 64
                        ),
                    lambda:
                        adapter.state(
                            "f" * 64
                        ),
                )
            )

            all_equal &= passed

            rows.append(
                {
                    "case":
                        "unknown_object",
                    "detail":
                        detail,
                }
            )

            # Serialized residency unavailable.
            (
                control,
                _integrated_runtime,
                adapter,
                _recording,
            ) = new_pair(
                selected_entries=(
                    entries[0],
                )
            )

            passed, detail = (
                compare_failures(
                    lambda:
                        control
                        .serialized_bytes(
                            entries[0]
                            .object_pk
                        ),
                    lambda:
                        adapter
                        .serialized_bytes(
                            entries[0]
                            .object_pk
                        ),
                )
            )

            all_equal &= passed

            rows.append(
                {
                    "case":
                        "serialized_unavailable",
                    "detail":
                        detail,
                }
            )

            # Dense residency unavailable.
            (
                control,
                _integrated_runtime,
                adapter,
                _recording,
            ) = new_pair(
                selected_entries=(
                    entries[0],
                )
            )

            control.ensure_state(
                entries[0].object_pk,
                runtime_module
                .ResidencyState
                .HOT_MAF,
            )

            adapter.ensure_state(
                entries[0].object_pk,
                runtime_module
                .ResidencyState
                .HOT_MAF,
            )

            passed, detail = (
                compare_failures(
                    lambda:
                        control.dense_view(
                            entries[0]
                            .object_pk
                        ),
                    lambda:
                        adapter.dense_view(
                            entries[0]
                            .object_pk
                        ),
                )
            )

            all_equal &= passed

            rows.append(
                {
                    "case":
                        "dense_unavailable",
                    "detail":
                        detail,
                }
            )

            # Closed runtime.
            (
                control,
                _integrated_runtime,
                adapter,
                _recording,
            ) = new_pair(
                selected_entries=(
                    entries[0],
                )
            )

            control.close()
            adapter.close()

            passed, detail = (
                compare_failures(
                    lambda:
                        control.state(
                            entries[0]
                            .object_pk
                        ),
                    lambda:
                        adapter.state(
                            entries[0]
                            .object_pk
                        ),
                )
            )

            all_equal &= passed

            rows.append(
                {
                    "case":
                        "closed_runtime",
                    "detail":
                        detail,
                }
            )

            return (
                bool(all_equal),
                rows,
            )

        recorder.run(
            "V31",
            v31,
        )

        # --------------------------------------------------
        # V32 — telemetry failure cannot replace runtime result
        # --------------------------------------------------

        fault_control = new_runtime(
            selected_entries=(
                entries[0],
            )
        )

        fault_runtime = (
            new_runtime()
        )

        fault_adapter = (
            integration
            .MAFSegmentLocalityRuntimeTelemetryAdapter(
                fault_runtime,
                source_manifest_sha256=
                    manifest_sha256,
            )
        )

        fault_adapter.register_entry(
            entries[0]
        )

        fault_recording = (
            RecordingAccumulator(
                fault_adapter
                ._accumulator,
                fail=True,
            )
        )

        fault_adapter._accumulator = (
            fault_recording
        )

        fault_control_result = (
            fault_control.transition(
                entries[0].object_pk,
                runtime_module
                .ResidencyState
                .MAPPED,
            )
        )

        fault_integrated_result = (
            fault_adapter.transition(
                entries[0].object_pk,
                runtime_module
                .ResidencyState
                .MAPPED,
            )
        )

        fault_diagnostics = (
            fault_adapter
            .telemetry_fault_diagnostics()
        )

        recorder.add(
            "V32",
            canonical(
                fault_control_result
            )
            == canonical(
                fault_integrated_result
            )
            and fault_diagnostics.faulted,
            {
                "control":
                    canonical(
                        fault_control_result
                    ),
                "integrated":
                    canonical(
                        fault_integrated_result
                    ),
                "diagnostics":
                    canonical(
                        fault_diagnostics
                    ),
            },
        )

        # --------------------------------------------------
        # V33 — persistent fault permanently blocks export
        # --------------------------------------------------

        subsequent_result = (
            fault_adapter.transition(
                entries[0].object_pk,
                runtime_module
                .ResidencyState
                .HOT_MAF,
            )
        )

        export_error = (
            capture_exception(
                fault_adapter
                .telemetry_snapshot
            )
        )

        later_diagnostics = (
            fault_adapter
            .telemetry_fault_diagnostics()
        )

        recorder.add(
            "V33",
            subsequent_result
            is not None
            and later_diagnostics
            .faulted
            and export_error
            is not None
            and export_error[0]
            == (
                "MAFSegmentLocalityRuntime"
                "TelemetryFaultedError"
            ),
            {
                "subsequent_result":
                    canonical(
                        subsequent_result
                    ),
                "export_exception":
                    export_error,
                "diagnostics":
                    canonical(
                        later_diagnostics
                    ),
            },
        )
        # --------------------------------------------------
        # V34 — deterministic canonical telemetry trace
        # --------------------------------------------------

        def deterministic_trace():
            (
                _runtime,
                adapter,
                recording,
            ) = new_adapter(
                selected_entries=(
                    entries[0],
                )
            )

            adapter.ensure_state(
                entries[0].object_pk,
                runtime_module
                .ResidencyState
                .HOT_MAF,
            )

            adapter.serialized_bytes(
                entries[0].object_pk
            )

            adapter.ensure_state(
                entries[0].object_pk,
                runtime_module
                .ResidencyState
                .HOT_DENSE,
            )

            adapter.dense_view(
                entries[0].object_pk
            )

            return {
                "events":
                    canonical(
                        recording.events
                    ),
                "snapshot":
                    canonical(
                        adapter
                        .telemetry_snapshot()
                    ),
            }

        trace_a = (
            deterministic_trace()
        )

        trace_b = (
            deterministic_trace()
        )

        recorder.add(
            "V34",
            canonical_json(
                trace_a
            )
            == canonical_json(
                trace_b
            ),
            {
                "trace_a":
                    trace_a,
                "trace_b":
                    trace_b,
            },
        )

        # --------------------------------------------------
        # V35 — telemetry/control equal Phase 6C
        # RuntimeSnapshot after matched operations
        # --------------------------------------------------

        recorder.add(
            "V35",
            bool(
                v30_detail.get(
                    "snapshot_equal",
                    False,
                )
            ),
            {
                "snapshot_equal":
                    v30_detail.get(
                        "snapshot_equal",
                        False,
                    ),
            },
        )

        # --------------------------------------------------
        # V36 — logical identities unchanged
        # --------------------------------------------------

        def v36():
            (
                _runtime,
                adapter,
                _recording,
            ) = new_adapter()

            runtime_snapshot = (
                adapter.snapshot()
            )

            observed = {
                "model_pk":
                    runtime_snapshot
                    .model_pk,
                "generation_pk":
                    runtime_snapshot
                    .generation_pk,
                "object_pks": [
                    object_snapshot
                    .object_pk
                    for object_snapshot
                    in runtime_snapshot
                    .objects
                ],
            }

            expected = {
                "model_pk":
                    model_pk,
                "generation_pk":
                    generation_pk,
                "object_pks": [
                    entry.object_pk
                    for entry
                    in entries
                ],
            }

            return (
                observed
                == expected,
                {
                    "observed":
                        observed,
                    "expected":
                        expected,
                },
            )

        recorder.run(
            "V36",
            v36,
        )

        # --------------------------------------------------
        # V37 — source segment/model authority unchanged
        # --------------------------------------------------

        def v37():
            (
                _runtime,
                adapter,
                _recording,
            ) = new_adapter()

            adapter.ensure_state(
                entries[0].object_pk,
                runtime_module
                .ResidencyState
                .HOT_DENSE,
            )

            adapter.serialized_bytes(
                entries[0].object_pk
            )

            telemetry_snapshot = (
                adapter
                .telemetry_snapshot()
            )

            source_after = {
                "segment_sha256":
                    sha256_file(
                        segment_path
                    ),
                "segment_length":
                    segment_path
                    .stat()
                    .st_size,
                "entries":
                    canonical(
                        entries
                    ),
            }

            binding_after = {
                "model_pk":
                    telemetry_snapshot
                    .model_pk,
                "generation_pk":
                    telemetry_snapshot
                    .source_generation_pk,
                "manifest_sha256":
                    telemetry_snapshot
                    .source_manifest_sha256,
            }

            binding_expected = {
                "model_pk":
                    model_pk,
                "generation_pk":
                    generation_pk,
                "manifest_sha256":
                    manifest_sha256,
            }

            return (
                source_after
                == source_before
                and binding_after
                == binding_expected,
                {
                    "source_before":
                        source_before,
                    "source_after":
                        source_after,
                    "binding_expected":
                        binding_expected,
                    "binding_after":
                        binding_after,
                },
            )

        recorder.run(
            "V37",
            v37,
        )
        # --------------------------------------------------
        # V38–V41 — side-effect and composition boundaries
        # --------------------------------------------------

        static_evidence = (
            static_boundaries()
        )

        probe.write_events.clear()
        probe.network_events.clear()
        probe.subprocess_events.clear()

        probe.capture_writes = True

        try:
            (
                _probe_runtime,
                probe_adapter,
                probe_recording,
            ) = new_adapter(
                selected_entries=(
                    entries[0],
                )
            )

            probe_adapter.ensure_state(
                entries[0].object_pk,
                runtime_module
                .ResidencyState
                .HOT_DENSE,
            )

            probe_adapter.serialized_bytes(
                entries[0].object_pk
            )

            probe_adapter.dense_view(
                entries[0].object_pk
            )

            probe_adapter.snapshot()

            probe_adapter.telemetry_snapshot()

            probe_adapter.close()

        finally:
            probe.capture_writes = False

        # --------------------------------------------------
        # V38 — no integration filesystem writes
        # --------------------------------------------------

        recorder.add(
            "V38",
            not probe.write_events,
            {
                "write_events":
                    probe.write_events,
            },
        )

        # --------------------------------------------------
        # V39 — no network or subprocess activity
        #
        # Dynamic audit evidence is combined with static
        # source inspection so a dormant network/process
        # dependency cannot silently escape the check.
        # --------------------------------------------------

        recorder.add(
            "V39",
            not static_evidence[
                "bad_imports"
            ]
            and not static_evidence[
                "bad_calls"
            ]
            and not probe.network_events
            and not probe.subprocess_events,
            {
                "static_bad_imports":
                    static_evidence[
                        "bad_imports"
                    ],
                "static_bad_calls":
                    static_evidence[
                        "bad_calls"
                    ],
                "dynamic_network":
                    probe.network_events,
                "dynamic_subprocess":
                    probe.subprocess_events,
            },
        )

        # --------------------------------------------------
        # V40 — no automatic telemetry persistence
        #
        # This is intentionally distinct from V38:
        # source must contain no persistence dependency/call,
        # and wrapped runtime operations must create no write.
        # --------------------------------------------------

        recorder.add(
            "V40",
            not static_evidence[
                "persistence_imports"
            ]
            and not static_evidence[
                "persistence_calls"
            ]
            and not probe.write_events,
            {
                "persistence_imports":
                    static_evidence[
                        "persistence_imports"
                    ],
                "persistence_calls":
                    static_evidence[
                        "persistence_calls"
                    ],
                "dynamic_write_events":
                    probe.write_events,
            },
        )

        # --------------------------------------------------
        # V41 — composition only:
        # no subclass semantic replacement,
        # monkey patch, runtime-method assignment,
        # setattr mutation, or callback/hook injection.
        # --------------------------------------------------

        composition = (
            static_evidence[
                "composition"
            ]
        )

        composition_passed = (
            composition[
                "class_count"
            ]
            == 1
            and not composition[
                "bases"
            ]
            and not composition[
                "runtime_assignments"
            ]
            and not composition[
                "runtime_setattr"
            ]
            and not composition[
                "runtime_callbacks"
            ]
        )

        recorder.add(
            "V41",
            composition_passed,
            composition,
        )

        # --------------------------------------------------
        # V42 — final frozen predecessor SHA revalidation
        # --------------------------------------------------

        frozen_after = (
            authority_inventory()
        )

        recorder.add(
            "V42",
            authority_exact()
            and frozen_after
            == frozen_before,
            {
                "before":
                    frozen_before,
                "after":
                    frozen_after,
            },
        )

        # Capture the final synthetic source identity before
        # the TemporaryDirectory context removes the fixture.
        final_fixture_state = {
            "segment_sha256":
                sha256_file(
                    segment_path
                ),
            "segment_length":
                segment_path
                .stat()
                .st_size,
        }

    # ------------------------------------------------------
    # Scientific result assembly
    # ------------------------------------------------------

    failed_checks = [
        row["name"]
        for row in recorder.rows
        if not row["pass"]
    ]

    resident_directory_sha256 = (
        sha256_file(
            RESIDENT_DIRECTORY
        )
        if RESIDENT_DIRECTORY.is_file()
        else "MISSING"
    )

    result = {
        "schema": (
            "openmind."
            "maf_segment_locality_runtime_telemetry_"
            "integration_validation.v1_1"
        ),
        "exact_once":
            True,
        "validation_protocol_sha256":
            AUTH[
                "validation_protocol"
            ][1],
        "integration_protocol_sha256":
            AUTH[
                "integration_protocol"
            ][1],
        "integration_sha256":
            AUTH[
                "integration"
            ][1],
        "runner_sha256":
            sha256_file(
                Path(__file__)
            ),
        "check_count":
            len(
                recorder.rows
            ),
        "expected_check_count":
            EXPECTED_CHECK_COUNT,
        "all_pass":
            (
                len(
                    recorder.rows
                )
                == EXPECTED_CHECK_COUNT
                and not failed_checks
            ),
        "failed_checks":
            failed_checks,
        "checks":
            recorder.rows,
        "frozen_authorities_before":
            frozen_before,
        "frozen_authorities_after":
            authority_inventory(),
        "resident_directory_sha256_diagnostic":
            resident_directory_sha256,
        "resident_directory_matches_known_authority":
            (
                resident_directory_sha256
                == RESIDENT_DIRECTORY_KNOWN_SHA256
            ),
        "source_fixture_after":
            final_fixture_state,
        "benchmark_executed":
            False,
        "inference_executed":
            False,
        "real_model_accessed":
            False,
        "phase_6e_executed":
            False,
        "network_accessed":
            bool(
                probe.network_events
            ),
        "subprocess_launched":
            bool(
                probe.subprocess_events
            ),
        "auditor_error":
            None,
    }

    return result
def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Exact-once Phase 6D "
            "Runtime Telemetry Integration "
            "Validation V1.1"
        )
    )

    parser.add_argument(
        "--guard-false",
        action="store_true",
        help=(
            "prove the runner remains inert "
            "without spending the result slot"
        ),
    )

    parser.add_argument(
        "--qualify-fixture",
        action="store_true",
        help=(
            "run the non-spending V1.1 "
            "fixture qualification only"
        ),
    )

    parser.add_argument(
        "--arm-exact-once",
        action="store_true",
        help=(
            "arm the scientific validation; "
            "also requires the explicit "
            "environment token"
        ),
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    # Explicit guard-false always wins, even if somebody
    # accidentally supplied an arming token at the same time.
    if args.guard_false:
        guard_false_packet()
        return 0

    if args.qualify_fixture:
        return fixture_qualification_packet_v1_1()

    armed = (
        args.arm_exact_once
        and os.environ.get(
            ARM_ENV
        )
        == ARM_VALUE
    )

    # Ordinary execution is deliberately inert.
    if not armed:
        guard_false_packet()
        return 0

    # ------------------------------------------------------
    # Exact-once pre-spend gates
    # ------------------------------------------------------

    if RESULT.exists():
        raise SystemExit(
            "REFUSED: Validation V1.1 final result "
            "already exists; exact-once slot is "
            "spent or occupied."
        )

    if RESULT_TEMP.exists():
        raise SystemExit(
            "REFUSED: Validation V1.1 temporary "
            "result already exists; exact-once "
            "slot is not clean."
        )

    if not authority_exact():
        raise SystemExit(
            "REFUSED: frozen predecessor SHA "
            "gate failed before exact-once spend."
        )

    # ResidentPKDirectory is a transitive Phase 6C
    # implementation dependency. Its identity is checked
    # diagnostically, not promoted into a new preregistered
    # V01/V42 scientific criterion.
    if not RESIDENT_DIRECTORY.is_file():
        raise SystemExit(
            "REFUSED: required resident PK directory "
            "implementation is missing."
        )

    resident_sha = (
        sha256_file(
            RESIDENT_DIRECTORY
        )
    )

    if (
        resident_sha
        != RESIDENT_DIRECTORY_KNOWN_SHA256
    ):
        raise SystemExit(
            "REFUSED: resident PK directory "
            "execution dependency does not match "
            "the accepted Phase 6C authority."
        )

    # V1.1 preregistration requires the canonical
    # fixture to cross the frozen runtime/integration
    # boundary before the exact-once slot is reserved.
    try:
        qualify_validation_fixture_v1_1()

    except Exception as error:
        raise SystemExit(
            "REFUSED: Validation V1.1 fixture "
            "qualification failed before exact-once "
            "spend: "
            + type(error).__name__
            + ": "
            + str(error)
        )

    if RESULT.exists() or RESULT_TEMP.exists():
        raise SystemExit(
            "REFUSED: fixture qualification touched "
            "the V1.1 result namespace."
        )

    # This is the exact-once spend transition.
    reservation_fd = (
        reserve_result_slot()
    )

    try:
        result = (
            run_scientific_validation()
        )

    except Exception as error:
        # An armed runner/harness failure is itself frozen as
        # the single raw result. It must not silently free the
        # slot for an in-place rerun.
        result = {
            "schema": (
                "openmind."
                "maf_segment_locality_runtime_telemetry_"
                "integration_validation.v1_1"
            ),
            "exact_once":
                True,
            "validation_protocol_sha256":
                AUTH[
                    "validation_protocol"
                ][1],
            "integration_protocol_sha256":
                AUTH[
                    "integration_protocol"
                ][1],
            "integration_sha256":
                AUTH[
                    "integration"
                ][1],
            "runner_sha256":
                sha256_file(
                    Path(__file__)
                ),
            "check_count":
                0,
            "expected_check_count":
                EXPECTED_CHECK_COUNT,
            "all_pass":
                False,
            "failed_checks":
                [],
            "checks":
                [],
            "benchmark_executed":
                False,
            "inference_executed":
                False,
            "real_model_accessed":
                False,
            "phase_6e_executed":
                False,
            "network_accessed":
                None,
            "subprocess_launched":
                None,
            "auditor_error": {
                "type":
                    type(error).__name__,
                "message":
                    str(error),
            },
        }

    publish_result(
        reservation_fd,
        result,
    )

    print(
        "=" * 72
    )

    print(
        " OPENMIND / RUNTIME TELEMETRY "
        "INTEGRATION VALIDATION V1.1"
    )

    print(
        "=" * 72
    )

    print(
        f"all_pass:    "
        f"{result['all_pass']}"
    )

    print(
        f"check_count: "
        f"{result['check_count']}"
    )

    print(
        "failed:      "
        + (
            ", ".join(
                result[
                    "failed_checks"
                ]
            )
            if result[
                "failed_checks"
            ]
            else "NONE"
        )
    )

    print(
        f"auditor_error: "
        f"{result['auditor_error']}"
    )

    print(
        f"result:      {RESULT}"
    )

    return (
        0
        if result[
            "all_pass"
        ]
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
