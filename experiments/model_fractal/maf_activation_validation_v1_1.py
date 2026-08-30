#!/usr/bin/env python3

"""MAF Activation V1.1 frozen validation runner.

This runner validates the corrective current-physical-validity boundary,
atomic authority transition, integrity preservation, and scope controls.

The runner is designed to be frozen before its first execution.

It uses controlled local MAF segment fixtures and does not require source
model files, inference, rollback, residency, or a catalog database.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Callable

import maf_activation_v1 as activation_v1
import maf_activation_v1_1 as activation
import maf_generation_engine_v1 as generation


SCHEMA = "openmind.maf_activation_validation.v1_1"
VERSION = "maf_activation_validation_v1_1"

ROOT = Path(__file__).resolve().parents[2]
MODULE_DIR = Path(__file__).resolve().parent

RUNTIME = (
    ROOT
    / "results/runtime"
    / "maf_activation_validation_v1_1"
)

RESULT = (
    MODULE_DIR
    / "maf_activation_validation_v1_1.json"
)

RESULT_PARTIAL = RESULT.with_name(
    RESULT.name + ".partial"
)

ACTIVATION_V11_PROTOCOL = (
    MODULE_DIR
    / "MAF_ACTIVATION_V1_1_PROTOCOL.md"
)

ACTIVATION_V1_ENGINE = (
    MODULE_DIR
    / "maf_activation_v1.py"
)

ACTIVATION_V11_ENGINE = (
    MODULE_DIR
    / "maf_activation_v1_1.py"
)

GENERATION_ENGINE = (
    MODULE_DIR
    / "maf_generation_engine_v1.py"
)

GENERATION_V11_RESULT = (
    MODULE_DIR
    / "maf_generation_engine_validation_v1_1.json"
)

EXPECTED_ACTIVATION_V11_PROTOCOL_SHA256 = (
    "94aebe64ab466f9ae94db91ce8a82f2c"
    "56f87376cd962f687d133712a491bcfb"
)

EXPECTED_ACTIVATION_V1_ENGINE_SHA256 = (
    "76d79f90d9bc30118a6dfe0297beacd9"
    "b323aed9f56876881f653a2c01c1f210"
)

EXPECTED_ACTIVATION_V11_ENGINE_SHA256 = (
    "9435ae8dd32656c7350887689d453f3c"
    "b8460887068bfaf06e6f68b5b5b927a1"
)

EXPECTED_GENERATION_ENGINE_SHA256 = (
    "8868c58e98084226dd957391e1a2f4d1"
    "122e886607640ae0be59279f025f1a51"
)

EXPECTED_GENERATION_V11_RESULT_SHA256 = (
    "a37ee07ab548b1dea398bb42de42cd893"
    "df437b06b91a8a767464a4559e52727"
)

MODEL_PK = (
    "mafmodel:v1:"
    + hashlib.sha256(
        b"openmind-activation-v1.1-model"
    ).hexdigest()
)

OTHER_MODEL_PK = (
    "mafmodel:v1:"
    + hashlib.sha256(
        b"openmind-activation-v1.1-other-model"
    ).hexdigest()
)

OBJECT_PK_A = (
    "mafobj:v1:"
    + hashlib.sha256(
        b"openmind-activation-v1.1-object-a"
    ).hexdigest()
)

OBJECT_PK_B = (
    "mafobj:v1:"
    + hashlib.sha256(
        b"openmind-activation-v1.1-object-b"
    ).hexdigest()
)

MULTI_OBJECT_PK_A = (
    "mafobj:v1:"
    + hashlib.sha256(
        b"openmind-activation-v1.1-multi-object-a"
    ).hexdigest()
)

MULTI_OBJECT_PK_B = (
    "mafobj:v1:"
    + hashlib.sha256(
        b"openmind-activation-v1.1-multi-object-b"
    ).hexdigest()
)


def sha256_bytes(
    payload: bytes,
) -> str:
    return hashlib.sha256(
        payload
    ).hexdigest()


def file_sha256(
    path: Path,
) -> str:
    digest = hashlib.sha256()

    with Path(path).open("rb") as handle:
        while True:
            block = handle.read(
                1024 * 1024
            )

            if not block:
                break

            digest.update(
                block
            )

    return digest.hexdigest()


def write_bytes_exclusive(
    path: Path,
    payload: bytes,
) -> None:
    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open("xb") as handle:
        handle.write(
            payload
        )
        handle.flush()
        os.fsync(
            handle.fileno()
        )


def write_canonical_json(
    path: Path,
    value: Any,
) -> None:
    write_bytes_exclusive(
        path,
        generation.canonical_json_bytes(
            value
        ),
    )


def deterministic_pk(
    prefix: str,
    label: str,
) -> str:
    return (
        prefix
        + hashlib.sha256(
            label.encode("utf-8")
        ).hexdigest()
    )


def base_segment_bytes() -> bytes:
    return bytes(
        (
            (
                i * 73
                + 19
            )
            % 256
        )
        for i in range(4096)
    )


def variant_segment_bytes() -> bytes:
    payload = bytearray(
        base_segment_bytes()
    )

    # Deliberately outside all controlled object ranges.
    payload[3500] ^= 0x5A

    return bytes(
        payload
    )


def payload_hash_for(
    object_pk: str,
) -> str:
    return hashlib.sha256(
        (
            "payload:"
            + object_pk
        ).encode("utf-8")
    ).hexdigest()


def object_specs() -> list[
    tuple[str, int, int]
]:
    return [
        (
            OBJECT_PK_A,
            64,
            512,
        ),
        (
            OBJECT_PK_B,
            1024,
            640,
        ),
    ]


def create_single_segment_candidate(
    *,
    label: str,
    segment_bytes: bytes,
) -> dict[str, Any]:
    segment_path = (
        RUNTIME
        / f"{label}.mafseg"
    )

    manifest_path = (
        RUNTIME
        / f"{label}.manifest.json"
    )

    write_bytes_exclusive(
        segment_path,
        segment_bytes,
    )

    segment_sha256 = sha256_bytes(
        segment_bytes
    )

    objects = []

    for (
        object_pk,
        offset,
        length,
    ) in object_specs():
        object_payload = (
            segment_bytes[
                offset:
                offset + length
            ]
        )

        objects.append(
            {
                "model_pk":
                    MODEL_PK,
                "object_pk":
                    object_pk,
                "segment_path":
                    str(segment_path),
                "offset":
                    offset,
                "length":
                    length,
                "object_file_sha256":
                    sha256_bytes(
                        object_payload
                    ),
                "payload_sha256":
                    payload_hash_for(
                        object_pk
                    ),
            }
        )

    build = generation.build_generation(
        model_pk=MODEL_PK,
        segments=[
            {
                "segment_path":
                    str(segment_path),
                "segment_length":
                    len(segment_bytes),
                "segment_sha256":
                    segment_sha256,
            }
        ],
        objects=objects,
        manifest_path=manifest_path,
    )

    descriptor = build.manifest[
        "descriptor"
    ]

    segment_id = descriptor[
        "segments"
    ][0][
        "segment_id"
    ]

    return {
        "label":
            label,
        "model_pk":
            MODEL_PK,
        "generation_pk":
            build.generation_pk,
        "manifest_path":
            manifest_path,
        "manifest":
            build.manifest,
        "descriptor":
            descriptor,
        "segment_paths":
            {
                segment_id:
                    segment_path,
            },
        "segment_files":
            [
                segment_path,
            ],
    }


def create_multi_segment_candidate() -> dict[
    str,
    Any,
]:
    segment_a_bytes = bytes(
        (
            (
                i * 17
                + 3
            )
            % 256
        )
        for i in range(2048)
    )

    segment_b_bytes = bytes(
        (
            (
                i * 29
                + 7
            )
            % 256
        )
        for i in range(3072)
    )

    segment_a = (
        RUNTIME
        / "multi_a.mafseg"
    )

    segment_b = (
        RUNTIME
        / "multi_b.mafseg"
    )

    manifest_path = (
        RUNTIME
        / "multi.manifest.json"
    )

    write_bytes_exclusive(
        segment_a,
        segment_a_bytes,
    )

    write_bytes_exclusive(
        segment_b,
        segment_b_bytes,
    )

    segment_rows = [
        {
            "segment_path":
                str(segment_a),
            "segment_length":
                len(segment_a_bytes),
            "segment_sha256":
                sha256_bytes(
                    segment_a_bytes
                ),
        },
        {
            "segment_path":
                str(segment_b),
            "segment_length":
                len(segment_b_bytes),
            "segment_sha256":
                sha256_bytes(
                    segment_b_bytes
                ),
        },
    ]

    objects = [
        {
            "model_pk":
                MODEL_PK,
            "object_pk":
                MULTI_OBJECT_PK_A,
            "segment_path":
                str(segment_a),
            "offset":
                128,
            "length":
                384,
            "object_file_sha256":
                sha256_bytes(
                    segment_a_bytes[
                        128:
                        128 + 384
                    ]
                ),
            "payload_sha256":
                payload_hash_for(
                    MULTI_OBJECT_PK_A
                ),
        },
        {
            "model_pk":
                MODEL_PK,
            "object_pk":
                MULTI_OBJECT_PK_B,
            "segment_path":
                str(segment_b),
            "offset":
                512,
            "length":
                448,
            "object_file_sha256":
                sha256_bytes(
                    segment_b_bytes[
                        512:
                        512 + 448
                    ]
                ),
            "payload_sha256":
                payload_hash_for(
                    MULTI_OBJECT_PK_B
                ),
        },
    ]

    build = generation.build_generation(
        model_pk=MODEL_PK,
        segments=segment_rows,
        objects=objects,
        manifest_path=manifest_path,
    )

    descriptor = build.manifest[
        "descriptor"
    ]

    content_to_path = {
        (
            sha256_bytes(
                segment_a_bytes
            ),
            len(segment_a_bytes),
        ):
            segment_a,
        (
            sha256_bytes(
                segment_b_bytes
            ),
            len(segment_b_bytes),
        ):
            segment_b,
    }

    mapping = {}

    for row in descriptor[
        "segments"
    ]:
        mapping[
            row["segment_id"]
        ] = content_to_path[
            (
                row[
                    "segment_sha256"
                ],
                row[
                    "segment_length"
                ],
            )
        ]

    return {
        "label":
            "multi",
        "model_pk":
            MODEL_PK,
        "generation_pk":
            build.generation_pk,
        "manifest_path":
            manifest_path,
        "manifest":
            build.manifest,
        "descriptor":
            descriptor,
        "segment_paths":
            mapping,
        "segment_files":
            [
                segment_a,
                segment_b,
            ],
    }


def reconstruct_candidate(
    fixture: dict[str, Any],
    segment_paths: dict[
        str,
        Path,
    ],
) -> dict[str, Any]:
    descriptor = fixture[
        "descriptor"
    ]

    segment_inputs = [
        {
            "segment_path":
                str(
                    segment_paths[
                        row[
                            "segment_id"
                        ]
                    ]
                ),
            "segment_length":
                row[
                    "segment_length"
                ],
            "segment_sha256":
                row[
                    "segment_sha256"
                ],
        }
        for row in descriptor[
            "segments"
        ]
    ]

    object_inputs = [
        {
            "model_pk":
                descriptor[
                    "model_pk"
                ],
            "object_pk":
                row[
                    "object_pk"
                ],
            "segment_path":
                str(
                    segment_paths[
                        row[
                            "segment_id"
                        ]
                    ]
                ),
            "offset":
                row[
                    "offset"
                ],
            "length":
                row[
                    "length"
                ],
            "object_file_sha256":
                row[
                    "object_file_sha256"
                ],
            "payload_sha256":
                row[
                    "payload_sha256"
                ],
        }
        for row in descriptor[
            "objects"
        ]
    ]

    (
        rebuilt,
        descriptor_sha256,
        generation_pk,
    ) = generation.build_descriptor(
        model_pk=descriptor[
            "model_pk"
        ],
        segments=segment_inputs,
        objects=object_inputs,
    )

    candidate_bytes = (
        generation.canonical_json_bytes(
            descriptor
        )
    )

    rebuilt_bytes = (
        generation.canonical_json_bytes(
            rebuilt
        )
    )

    return {
        "descriptor_exact":
            rebuilt == descriptor,
        "canonical_bytes_exact":
            rebuilt_bytes
            == candidate_bytes,
        "descriptor_sha256_exact":
            descriptor_sha256
            == sha256_bytes(
                candidate_bytes
            ),
        "generation_pk_exact":
            generation_pk
            == fixture[
                "generation_pk"
            ],
        "rebuilt_generation_pk":
            generation_pk,
    }


def snapshot_fixture(
    fixture: dict[str, Any],
) -> dict[str, str]:
    paths = [
        fixture[
            "manifest_path"
        ],
        *fixture[
            "segment_files"
        ],
    ]

    return {
        str(path):
            file_sha256(
                path
            )
        for path in paths
    }


def snapshot_exact(
    snapshot: dict[str, str],
) -> bool:
    for (
        path_text,
        expected_sha,
    ) in snapshot.items():
        path = Path(
            path_text
        )

        if not path.is_file():
            return False

        if (
            file_sha256(
                path
            )
            != expected_sha
        ):
            return False

    return True


def write_manifest_variant(
    *,
    label: str,
    manifest: dict[str, Any],
    canonical: bool = True,
) -> Path:
    path = (
        RUNTIME
        / f"{label}.manifest.json"
    )

    if canonical:
        payload = (
            generation.canonical_json_bytes(
                manifest
            )
        )
    else:
        payload = json.dumps(
            manifest,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
        ).encode("utf-8")

    write_bytes_exclusive(
        path,
        payload,
    )

    return path


def expect_failure(
    *,
    label: str,
    operation: Callable[[], Any],
    expected_text: str | None = None,
    active_path: Path | None = None,
    expected_active_bytes: bytes | None = None,
    require_active_absent: bool = False,
    partial_path: Path | None = None,
    expected_partial_bytes: bytes | None = None,
) -> dict[str, Any]:
    error_type = None
    error_text = None
    raised = False

    try:
        operation()

    except Exception as exc:
        raised = True
        error_type = type(
            exc
        ).__name__
        error_text = str(
            exc
        )

    active_preserved = True

    if (
        active_path is not None
        and expected_active_bytes
        is not None
    ):
        active_preserved = (
            active_path.is_file()
            and active_path.read_bytes()
            == expected_active_bytes
        )

    if (
        active_path is not None
        and require_active_absent
    ):
        active_preserved = (
            active_preserved
            and not active_path.exists()
        )

    partial_preserved = True

    if (
        partial_path is not None
        and expected_partial_bytes
        is not None
    ):
        partial_preserved = (
            partial_path.is_file()
            and partial_path.read_bytes()
            == expected_partial_bytes
        )

    expected_error = (
        raised
        and (
            expected_text is None
            or (
                error_text is not None
                and expected_text
                in error_text
            )
        )
    )

    passed = (
        expected_error
        and active_preserved
        and partial_preserved
    )

    return {
        "label":
            label,
        "error_type":
            error_type,
        "error_text":
            error_text,
        "raised":
            raised,
        "failed_closed":
            (
                active_preserved
                and partial_preserved
            ),
        "pass":
            passed,
    }


def manual_manifest(
    descriptor: dict[str, Any],
) -> dict[str, Any]:
    descriptor_bytes = (
        generation.canonical_json_bytes(
            descriptor
        )
    )

    generation_pk = (
        generation.GENERATION_PREFIX
        + hashlib.sha256(
            descriptor_bytes
        ).hexdigest()
    )

    return {
        "schema":
            generation.MANIFEST_SCHEMA,
        "manifest_version":
            generation.MANIFEST_VERSION,
        "generation_pk":
            generation_pk,
        "descriptor":
            descriptor,
    }


def operational_extension_literals(
    path: Path,
) -> list[
    tuple[int, str]
]:
    tree = ast.parse(
        Path(path).read_text()
    )

    needle = "." + "gguf"
    rows = []

    for node in tree.body:
        if not isinstance(
            node,
            (
                ast.FunctionDef,
                ast.ClassDef,
            ),
        ):
            continue

        for child in ast.walk(
            node
        ):
            if (
                isinstance(
                    child,
                    ast.Constant,
                )
                and isinstance(
                    child.value,
                    str,
                )
                and needle
                in child.value.lower()
            ):
                rows.append(
                    (
                        child.lineno,
                        child.value,
                    )
                )

    return rows


def public_function_names(
    path: Path,
) -> set[str]:
    tree = ast.parse(
        Path(path).read_text()
    )

    return {
        node.name.lower()
        for node in tree.body
        if (
            isinstance(
                node,
                ast.FunctionDef,
            )
            and not node.name.startswith(
                "_"
            )
        )
    }


def imported_modules(
    path: Path,
) -> set[str]:
    tree = ast.parse(
        Path(path).read_text()
    )

    result = set()

    for node in tree.body:
        if isinstance(
            node,
            ast.Import,
        ):
            result.update(
                alias.name
                for alias in node.names
            )

        elif isinstance(
            node,
            ast.ImportFrom,
        ):
            if node.module:
                result.add(
                    node.module
                )

    return result


def activation_v11_direct_calls() -> set[str]:
    tree = ast.parse(
        ACTIVATION_V11_ENGINE.read_text()
    )

    calls = set()

    for node in ast.walk(
        tree
    ):
        if not isinstance(
            node,
            ast.Call,
        ):
            continue

        func = node.func

        if (
            isinstance(
                func,
                ast.Attribute,
            )
            and isinstance(
                func.value,
                ast.Name,
            )
        ):
            calls.add(
                func.value.id
                + "."
                + func.attr
            )

    return calls


def static_policy_checks() -> dict[
    str,
    bool,
]:
    v11_functions = (
        public_function_names(
            ACTIVATION_V11_ENGINE
        )
    )

    imports = imported_modules(
        ACTIVATION_V11_ENGINE
    )

    calls = (
        activation_v11_direct_calls()
    )

    forbidden_names = {
        "rollback",
        "restore_generation",
        "retire_generation",
        "delete_generation",
    }

    no_forbidden_api = not any(
        any(
            term in name
            for term in forbidden_names
        )
        for name in v11_functions
    )

    v11_tree = ast.parse(
        ACTIVATION_V11_ENGINE.read_text()
    )

    replace_calls = [
        node.lineno
        for node in ast.walk(
            v11_tree
        )
        if (
            isinstance(
                node,
                ast.Call,
            )
            and isinstance(
                node.func,
                ast.Attribute,
            )
            and node.func.attr
            == "replace"
        )
    ]

    unlink_calls = [
        node.lineno
        for node in ast.walk(
            v11_tree
        )
        if (
            isinstance(
                node,
                ast.Call,
            )
            and isinstance(
                node.func,
                ast.Attribute,
            )
            and node.func.attr
            == "unlink"
        )
    ]

    return {
        "activation_v11_protocol_exact":
            file_sha256(
                ACTIVATION_V11_PROTOCOL
            )
            == EXPECTED_ACTIVATION_V11_PROTOCOL_SHA256,

        "activation_v1_engine_exact":
            file_sha256(
                ACTIVATION_V1_ENGINE
            )
            == EXPECTED_ACTIVATION_V1_ENGINE_SHA256,

        "activation_v11_engine_exact":
            file_sha256(
                ACTIVATION_V11_ENGINE
            )
            == EXPECTED_ACTIVATION_V11_ENGINE_SHA256,

        "generation_engine_exact":
            file_sha256(
                GENERATION_ENGINE
            )
            == EXPECTED_GENERATION_ENGINE_SHA256,

        "generation_v11_result_exact":
            file_sha256(
                GENERATION_V11_RESULT
            )
            == EXPECTED_GENERATION_V11_RESULT_SHA256,

        "v11_reuses_build_descriptor":
            "generation.build_descriptor"
            in calls,

        "v11_delegates_activation_v1":
            "activation_v1.activate_generation"
            in calls,

        "v11_no_direct_replace":
            not replace_calls,

        "v11_no_generation_deletion":
            not unlink_calls,

        "v11_no_rollback_api":
            no_forbidden_api,

        "v11_no_sqlite":
            "sqlite3"
            not in imports,

        "v11_no_mmap":
            "mmap"
            not in imports,

        "v11_no_operational_source_model_extension":
            not operational_extension_literals(
                ACTIVATION_V11_ENGINE
            ),

        "runner_no_operational_source_model_extension":
            not operational_extension_literals(
                Path(__file__)
            ),
    }


def persist_result(
    result: dict[str, Any],
) -> None:
    if RESULT.exists():
        raise RuntimeError(
            "validation result already exists"
        )

    if RESULT_PARTIAL.exists():
        raise RuntimeError(
            "validation result partial already exists"
        )

    payload = (
        generation.canonical_json_bytes(
            result
        )
    )

    created_partial = False

    try:
        with RESULT_PARTIAL.open(
            "xb"
        ) as handle:
            created_partial = True
            handle.write(
                payload
            )
            handle.flush()
            os.fsync(
                handle.fileno()
            )

        reopened = json.loads(
            RESULT_PARTIAL.read_text(
                encoding="utf-8"
            )
        )

        if (
            generation.canonical_json_bytes(
                reopened
            )
            != payload
        ):
            raise RuntimeError(
                "validation result canonical reopen mismatch"
            )

        os.replace(
            RESULT_PARTIAL,
            RESULT,
        )

        created_partial = False

    except Exception:
        if (
            created_partial
            and RESULT_PARTIAL.exists()
        ):
            RESULT_PARTIAL.unlink()

        raise


def run_validation() -> dict[str, Any]:
    candidate_a = (
        create_single_segment_candidate(
            label="candidate_a",
            segment_bytes=(
                base_segment_bytes()
            ),
        )
    )

    candidate_b = (
        create_single_segment_candidate(
            label="candidate_b",
            segment_bytes=(
                variant_segment_bytes()
            ),
        )
    )

    multi = (
        create_multi_segment_candidate()
    )

    snapshot_a = snapshot_fixture(
        candidate_a
    )

    snapshot_b = snapshot_fixture(
        candidate_b
    )

    reconstruction_a = (
        reconstruct_candidate(
            candidate_a,
            candidate_a[
                "segment_paths"
            ],
        )
    )

    reconstruction_b = (
        reconstruct_candidate(
            candidate_b,
            candidate_b[
                "segment_paths"
            ],
        )
    )

    expected_manifest_sha_a = (
        file_sha256(
            candidate_a[
                "manifest_path"
            ]
        )
    )

    expected_manifest_sha_b = (
        file_sha256(
            candidate_b[
                "manifest_path"
            ]
        )
    )

    record_a = (
        activation.build_active_record(
            model_pk=MODEL_PK,
            generation_pk=(
                candidate_a[
                    "generation_pk"
                ]
            ),
            candidate_manifest_path=(
                candidate_a[
                    "manifest_path"
                ]
            ),
            segment_paths=(
                candidate_a[
                    "segment_paths"
                ]
            ),
        )
    )

    canonical_record_a = (
        activation.canonical_json_bytes(
            record_a
        )
    )

    relocated_manifest = (
        RUNTIME
        / "candidate_a_relocated.manifest.json"
    )

    write_bytes_exclusive(
        relocated_manifest,
        candidate_a[
            "manifest_path"
        ].read_bytes(),
    )

    relocated_manifest_record = (
        activation.build_active_record(
            model_pk=MODEL_PK,
            generation_pk=(
                candidate_a[
                    "generation_pk"
                ]
            ),
            candidate_manifest_path=(
                relocated_manifest
            ),
            segment_paths=(
                candidate_a[
                    "segment_paths"
                ]
            ),
        )
    )

    original_segment_a = next(
        iter(
            candidate_a[
                "segment_paths"
            ].values()
        )
    )

    relocated_segment = (
        RUNTIME
        / "candidate_a_relocated.mafseg"
    )

    write_bytes_exclusive(
        relocated_segment,
        Path(
            original_segment_a
        ).read_bytes(),
    )

    relocated_segment_mapping = {
        key:
            relocated_segment
        for key
        in candidate_a[
            "segment_paths"
        ]
    }

    relocated_segment_record = (
        activation.build_active_record(
            model_pk=MODEL_PK,
            generation_pk=(
                candidate_a[
                    "generation_pk"
                ]
            ),
            candidate_manifest_path=(
                candidate_a[
                    "manifest_path"
                ]
            ),
            segment_paths=(
                relocated_segment_mapping
            ),
        )
    )

    active_path = (
        RUNTIME
        / "active_generation.json"
    )

    first = activation.activate_generation(
        model_pk=MODEL_PK,
        generation_pk=(
            candidate_a[
                "generation_pk"
            ]
        ),
        candidate_manifest_path=(
            candidate_a[
                "manifest_path"
            ]
        ),
        active_record_path=(
            active_path
        ),
        segment_paths=(
            candidate_a[
                "segment_paths"
            ]
        ),
    )

    active_a_bytes = (
        active_path.read_bytes()
    )

    active_a_stat = active_path.stat()

    reopened_a = (
        activation.reopen_active_generation(
            active_path
        )
    )

    idempotent = (
        activation.activate_generation(
            model_pk=MODEL_PK,
            generation_pk=(
                candidate_a[
                    "generation_pk"
                ]
            ),
            candidate_manifest_path=(
                candidate_a[
                    "manifest_path"
                ]
            ),
            active_record_path=(
                active_path
            ),
            segment_paths=(
                candidate_a[
                    "segment_paths"
                ]
            ),
        )
    )

    active_a_after_idempotent = (
        active_path.read_bytes()
    )

    active_a_stat_after = (
        active_path.stat()
    )

    replacement = (
        activation.activate_generation(
            model_pk=MODEL_PK,
            generation_pk=(
                candidate_b[
                    "generation_pk"
                ]
            ),
            candidate_manifest_path=(
                candidate_b[
                    "manifest_path"
                ]
            ),
            active_record_path=(
                active_path
            ),
            segment_paths=(
                candidate_b[
                    "segment_paths"
                ]
            ),
        )
    )

    active_b_bytes = (
        active_path.read_bytes()
    )

    reopened_b = (
        activation.reopen_active_generation(
            active_path
        )
    )

    object_pks_a = [
        row[
            "object_pk"
        ]
        for row
        in candidate_a[
            "descriptor"
        ][
            "objects"
        ]
    ]

    object_pks_b = [
        row[
            "object_pk"
        ]
        for row
        in candidate_b[
            "descriptor"
        ][
            "objects"
        ]
    ]

    authority_text = (
        active_b_bytes.decode(
            "utf-8"
        )
    )

    path_strings = [
        str(
            candidate_a[
                "manifest_path"
            ]
        ),
        str(
            candidate_b[
                "manifest_path"
            ]
        ),
        *[
            str(path)
            for path
            in candidate_a[
                "segment_paths"
            ].values()
        ],
        *[
            str(path)
            for path
            in candidate_b[
                "segment_paths"
            ].values()
        ],
    ]

    forward_mapping = dict(
        multi[
            "segment_paths"
        ]
    )

    reverse_mapping = dict(
        reversed(
            list(
                multi[
                    "segment_paths"
                ].items()
            )
        )
    )

    multi_record_forward = (
        activation.build_active_record(
            model_pk=MODEL_PK,
            generation_pk=(
                multi[
                    "generation_pk"
                ]
            ),
            candidate_manifest_path=(
                multi[
                    "manifest_path"
                ]
            ),
            segment_paths=(
                forward_mapping
            ),
        )
    )

    multi_record_reverse = (
        activation.build_active_record(
            model_pk=MODEL_PK,
            generation_pk=(
                multi[
                    "generation_pk"
                ]
            ),
            candidate_manifest_path=(
                multi[
                    "manifest_path"
                ]
            ),
            segment_paths=(
                reverse_mapping
            ),
        )
    )

    negative_controls = []

    missing_candidate_active = (
        RUNTIME
        / "neg_missing_candidate_active.json"
    )

    negative_controls.append(
        expect_failure(
            label="missing_candidate_manifest",
            expected_text=(
                "candidate manifest missing"
            ),
            active_path=(
                missing_candidate_active
            ),
            require_active_absent=True,
            operation=lambda:
                activation.activate_generation(
                    model_pk=MODEL_PK,
                    generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                    candidate_manifest_path=(
                        RUNTIME
                        / "does_not_exist.manifest.json"
                    ),
                    active_record_path=(
                        missing_candidate_active
                    ),
                    segment_paths=(
                        candidate_a[
                            "segment_paths"
                        ]
                    ),
                ),
        )
    )

    malformed_json = (
        RUNTIME
        / "malformed_candidate.manifest.json"
    )

    write_bytes_exclusive(
        malformed_json,
        b"{malformed",
    )

    malformed_json_active = (
        RUNTIME
        / "neg_malformed_json_active.json"
    )

    negative_controls.append(
        expect_failure(
            label="malformed_candidate_json",
            expected_text=(
                "invalid candidate manifest JSON"
            ),
            active_path=(
                malformed_json_active
            ),
            require_active_absent=True,
            operation=lambda:
                activation.activate_generation(
                    model_pk=MODEL_PK,
                    generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                    candidate_manifest_path=(
                        malformed_json
                    ),
                    active_record_path=(
                        malformed_json_active
                    ),
                    segment_paths=(
                        candidate_a[
                            "segment_paths"
                        ]
                    ),
                ),
        )
    )

    invalid_schema_manifest = copy.deepcopy(
        candidate_a[
            "manifest"
        ]
    )

    invalid_schema_manifest[
        "schema"
    ] = "invalid.activation.test.schema"

    invalid_schema_path = (
        write_manifest_variant(
            label="invalid_schema",
            manifest=(
                invalid_schema_manifest
            ),
        )
    )

    invalid_schema_active = (
        RUNTIME
        / "neg_invalid_schema_active.json"
    )

    negative_controls.append(
        expect_failure(
            label="invalid_manifest_schema",
            expected_text=(
                "invalid manifest schema"
            ),
            active_path=(
                invalid_schema_active
            ),
            require_active_absent=True,
            operation=lambda:
                activation.activate_generation(
                    model_pk=MODEL_PK,
                    generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                    candidate_manifest_path=(
                        invalid_schema_path
                    ),
                    active_record_path=(
                        invalid_schema_active
                    ),
                    segment_paths=(
                        candidate_a[
                            "segment_paths"
                        ]
                    ),
                ),
        )
    )

    invalid_version_manifest = copy.deepcopy(
        candidate_a[
            "manifest"
        ]
    )

    invalid_version_manifest[
        "manifest_version"
    ] = "invalid_manifest_version"

    invalid_version_path = (
        write_manifest_variant(
            label="invalid_version",
            manifest=(
                invalid_version_manifest
            ),
        )
    )

    invalid_version_active = (
        RUNTIME
        / "neg_invalid_version_active.json"
    )

    negative_controls.append(
        expect_failure(
            label="invalid_manifest_version",
            expected_text=(
                "invalid manifest version"
            ),
            active_path=(
                invalid_version_active
            ),
            require_active_absent=True,
            operation=lambda:
                activation.activate_generation(
                    model_pk=MODEL_PK,
                    generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                    candidate_manifest_path=(
                        invalid_version_path
                    ),
                    active_record_path=(
                        invalid_version_active
                    ),
                    segment_paths=(
                        candidate_a[
                            "segment_paths"
                        ]
                    ),
                ),
        )
    )

    bad_derivation_manifest = copy.deepcopy(
        candidate_a[
            "manifest"
        ]
    )

    bad_derivation_manifest[
        "generation_pk"
    ] = (
        generation.GENERATION_PREFIX
        + ("0" * 64)
    )

    bad_derivation_path = (
        write_manifest_variant(
            label="generation_pk_derivation_mismatch",
            manifest=(
                bad_derivation_manifest
            ),
        )
    )

    bad_derivation_active = (
        RUNTIME
        / "neg_generation_derivation_active.json"
    )

    negative_controls.append(
        expect_failure(
            label="generation_pk_derivation_mismatch",
            expected_text=(
                "generation_pk mismatch"
            ),
            active_path=(
                bad_derivation_active
            ),
            require_active_absent=True,
            operation=lambda:
                activation.activate_generation(
                    model_pk=MODEL_PK,
                    generation_pk=(
                        bad_derivation_manifest[
                            "generation_pk"
                        ]
                    ),
                    candidate_manifest_path=(
                        bad_derivation_path
                    ),
                    active_record_path=(
                        bad_derivation_active
                    ),
                    segment_paths=(
                        candidate_a[
                            "segment_paths"
                        ]
                    ),
                ),
        )
    )

    requested_generation_active = (
        RUNTIME
        / "neg_requested_generation_active.json"
    )

    requested_wrong_generation = (
        generation.GENERATION_PREFIX
        + hashlib.sha256(
            b"wrong-requested-generation"
        ).hexdigest()
    )

    negative_controls.append(
        expect_failure(
            label="requested_generation_pk_mismatch",
            expected_text=(
                "requested generation_pk mismatch"
            ),
            active_path=(
                requested_generation_active
            ),
            require_active_absent=True,
            operation=lambda:
                activation.activate_generation(
                    model_pk=MODEL_PK,
                    generation_pk=(
                        requested_wrong_generation
                    ),
                    candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        requested_generation_active
                    ),
                    segment_paths=(
                        candidate_a[
                            "segment_paths"
                        ]
                    ),
                ),
        )
    )

    requested_model_active = (
        RUNTIME
        / "neg_requested_model_active.json"
    )

    negative_controls.append(
        expect_failure(
            label="requested_model_pk_mismatch",
            expected_text=(
                "requested model_pk mismatch"
            ),
            active_path=(
                requested_model_active
            ),
            require_active_absent=True,
            operation=lambda:
                activation.activate_generation(
                    model_pk=OTHER_MODEL_PK,
                    generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                    candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        requested_model_active
                    ),
                    segment_paths=(
                        candidate_a[
                            "segment_paths"
                        ]
                    ),
                ),
        )
    )

    malformed_model_active = (
        RUNTIME
        / "neg_malformed_model_active.json"
    )

    negative_controls.append(
        expect_failure(
            label="malformed_requested_model_pk",
            expected_text=(
                "invalid model_pk"
            ),
            active_path=(
                malformed_model_active
            ),
            require_active_absent=True,
            operation=lambda:
                activation.activate_generation(
                    model_pk="malformed-model",
                    generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                    candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        malformed_model_active
                    ),
                    segment_paths=(
                        candidate_a[
                            "segment_paths"
                        ]
                    ),
                ),
        )
    )

    malformed_generation_active = (
        RUNTIME
        / "neg_malformed_generation_active.json"
    )

    negative_controls.append(
        expect_failure(
            label="malformed_requested_generation_pk",
            expected_text=(
                "invalid generation_pk"
            ),
            active_path=(
                malformed_generation_active
            ),
            require_active_absent=True,
            operation=lambda:
                activation.activate_generation(
                    model_pk=MODEL_PK,
                    generation_pk=(
                        "malformed-generation"
                    ),
                    candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        malformed_generation_active
                    ),
                    segment_paths=(
                        candidate_a[
                            "segment_paths"
                        ]
                    ),
                ),
        )
    )

    noncanonical_path = (
        write_manifest_variant(
            label="noncanonical_candidate",
            manifest=(
                candidate_a[
                    "manifest"
                ]
            ),
            canonical=False,
        )
    )

    noncanonical_active = (
        RUNTIME
        / "neg_noncanonical_active.json"
    )

    negative_controls.append(
        expect_failure(
            label="noncanonical_candidate_manifest",
            expected_text=(
                "candidate manifest is not canonical JSON"
            ),
            active_path=(
                noncanonical_active
            ),
            require_active_absent=True,
            operation=lambda:
                activation.activate_generation(
                    model_pk=MODEL_PK,
                    generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                    candidate_manifest_path=(
                        noncanonical_path
                    ),
                    active_record_path=(
                        noncanonical_active
                    ),
                    segment_paths=(
                        candidate_a[
                            "segment_paths"
                        ]
                    ),
                ),
        )
    )

    missing_mapping_active = (
        RUNTIME
        / "neg_missing_mapping_active.json"
    )

    negative_controls.append(
        expect_failure(
            label="missing_segment_paths_mapping",
            expected_text=(
                "segment_paths mapping required"
            ),
            active_path=(
                missing_mapping_active
            ),
            require_active_absent=True,
            operation=lambda:
                activation.activate_generation(
                    model_pk=MODEL_PK,
                    generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                    candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        missing_mapping_active
                    ),
                    segment_paths=None,
                ),
        )
    )

    missing_descriptor_mapping_active = (
        RUNTIME
        / "neg_missing_descriptor_mapping_active.json"
    )

    negative_controls.append(
        expect_failure(
            label="missing_descriptor_segment_mapping",
            expected_text=(
                "missing descriptor segment mapping"
            ),
            active_path=(
                missing_descriptor_mapping_active
            ),
            require_active_absent=True,
            operation=lambda:
                activation.activate_generation(
                    model_pk=MODEL_PK,
                    generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                    candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        missing_descriptor_mapping_active
                    ),
                    segment_paths={},
                ),
        )
    )

    extra_mapping = dict(
        candidate_a[
            "segment_paths"
        ]
    )

    extra_mapping[
        "segment:99999999"
    ] = original_segment_a

    extra_mapping_active = (
        RUNTIME
        / "neg_extra_mapping_active.json"
    )

    negative_controls.append(
        expect_failure(
            label="extra_descriptor_segment_mapping",
            expected_text=(
                "extra descriptor segment mapping"
            ),
            active_path=(
                extra_mapping_active
            ),
            require_active_absent=True,
            operation=lambda:
                activation.activate_generation(
                    model_pk=MODEL_PK,
                    generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                    candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        extra_mapping_active
                    ),
                    segment_paths=(
                        extra_mapping
                    ),
                ),
        )
    )

    segment_id_a = next(
        iter(
            candidate_a[
                "segment_paths"
            ]
        )
    )

    mapped_missing = {
        segment_id_a:
            (
                RUNTIME
                / "missing_physical_segment.mafseg"
            )
    }

    mapped_missing_active = (
        RUNTIME
        / "neg_mapped_missing_active.json"
    )

    negative_controls.append(
        expect_failure(
            label="mapped_segment_path_missing",
            expected_text=(
                "segment is not a regular file"
            ),
            active_path=(
                mapped_missing_active
            ),
            require_active_absent=True,
            operation=lambda:
                activation.activate_generation(
                    model_pk=MODEL_PK,
                    generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                    candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        mapped_missing_active
                    ),
                    segment_paths=(
                        mapped_missing
                    ),
                ),
        )
    )

    directory_segment = (
        RUNTIME
        / "directory_segment"
    )

    directory_segment.mkdir()

    mapped_directory = {
        segment_id_a:
            directory_segment,
    }

    mapped_directory_active = (
        RUNTIME
        / "neg_mapped_directory_active.json"
    )

    negative_controls.append(
        expect_failure(
            label="mapped_segment_not_regular_file",
            expected_text=(
                "segment is not a regular file"
            ),
            active_path=(
                mapped_directory_active
            ),
            require_active_absent=True,
            operation=lambda:
                activation.activate_generation(
                    model_pk=MODEL_PK,
                    generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                    candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        mapped_directory_active
                    ),
                    segment_paths=(
                        mapped_directory
                    ),
                ),
        )
    )

    length_bad_segment = (
        RUNTIME
        / "length_bad_segment.mafseg"
    )

    write_bytes_exclusive(
        length_bad_segment,
        Path(
            original_segment_a
        ).read_bytes()
        + b"\x00",
    )

    length_bad_mapping = {
        segment_id_a:
            length_bad_segment,
    }

    length_bad_active = (
        RUNTIME
        / "neg_length_bad_active.json"
    )

    negative_controls.append(
        expect_failure(
            label="mapped_segment_length_mismatch",
            expected_text=(
                "segment length mismatch"
            ),
            active_path=(
                length_bad_active
            ),
            require_active_absent=True,
            operation=lambda:
                activation.activate_generation(
                    model_pk=MODEL_PK,
                    generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                    candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        length_bad_active
                    ),
                    segment_paths=(
                        length_bad_mapping
                    ),
                ),
        )
    )

    sha_bad_payload = bytearray(
        Path(
            original_segment_a
        ).read_bytes()
    )

    sha_bad_payload[3500] ^= 0x33

    sha_bad_segment = (
        RUNTIME
        / "sha_bad_segment.mafseg"
    )

    write_bytes_exclusive(
        sha_bad_segment,
        bytes(
            sha_bad_payload
        ),
    )

    sha_bad_mapping = {
        segment_id_a:
            sha_bad_segment,
    }

    sha_bad_active = (
        RUNTIME
        / "neg_sha_bad_active.json"
    )

    negative_controls.append(
        expect_failure(
            label="mapped_segment_sha256_mismatch",
            expected_text=(
                "segment SHA256 mismatch"
            ),
            active_path=(
                sha_bad_active
            ),
            require_active_absent=True,
            operation=lambda:
                activation.activate_generation(
                    model_pk=MODEL_PK,
                    generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                    candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        sha_bad_active
                    ),
                    segment_paths=(
                        sha_bad_mapping
                    ),
                ),
        )
    )

    object_bad_descriptor = copy.deepcopy(
        candidate_a[
            "descriptor"
        ]
    )

    object_bad_descriptor[
        "objects"
    ][0][
        "object_file_sha256"
    ] = "0" * 64

    object_bad_manifest = manual_manifest(
        object_bad_descriptor
    )

    object_bad_path = (
        write_manifest_variant(
            label="object_range_hash_mismatch",
            manifest=(
                object_bad_manifest
            ),
        )
    )

    object_bad_active = (
        RUNTIME
        / "neg_object_hash_active.json"
    )

    negative_controls.append(
        expect_failure(
            label="object_byte_range_sha256_mismatch",
            expected_text=(
                "object byte-range SHA256 mismatch"
            ),
            active_path=(
                object_bad_active
            ),
            require_active_absent=True,
            operation=lambda:
                activation.activate_generation(
                    model_pk=MODEL_PK,
                    generation_pk=(
                        object_bad_manifest[
                            "generation_pk"
                        ]
                    ),
                    candidate_manifest_path=(
                        object_bad_path
                    ),
                    active_record_path=(
                        object_bad_active
                    ),
                    segment_paths=(
                        candidate_a[
                            "segment_paths"
                        ]
                    ),
                ),
        )
    )

    synthetic_descriptor = {
        "schema":
            generation.DESCRIPTOR_SCHEMA,
        "descriptor_version":
            generation.DESCRIPTOR_VERSION,
        "model_pk":
            MODEL_PK,
        "segments": [
            {
                "segment_id":
                    "segment:00000000",
                "segment_length":
                    2048,
                "segment_sha256":
                    "1" * 64,
            }
        ],
        "objects": [
            {
                "object_pk":
                    deterministic_pk(
                        "mafobj:v1:",
                        "synthetic-object",
                    ),
                "segment_id":
                    "segment:00000000",
                "offset":
                    0,
                "length":
                    128,
                "object_file_sha256":
                    "2" * 64,
                "payload_sha256":
                    "3" * 64,
            }
        ],
    }

    synthetic_manifest = manual_manifest(
        synthetic_descriptor
    )

    synthetic_manifest_verified = (
        generation.verify_manifest(
            synthetic_manifest
        )
        == synthetic_manifest[
            "generation_pk"
        ]
    )

    synthetic_path = (
        write_manifest_variant(
            label="synthetic_canonical",
            manifest=(
                synthetic_manifest
            ),
        )
    )

    synthetic_active = (
        RUNTIME
        / "neg_synthetic_active.json"
    )

    synthetic_segment_missing = (
        RUNTIME
        / "synthetic_missing.mafseg"
    )

    negative_controls.append(
        expect_failure(
            label="synthetic_canonical_without_physical_evidence",
            expected_text=(
                "segment is not a regular file"
            ),
            active_path=(
                synthetic_active
            ),
            require_active_absent=True,
            operation=lambda:
                activation.activate_generation(
                    model_pk=MODEL_PK,
                    generation_pk=(
                        synthetic_manifest[
                            "generation_pk"
                        ]
                    ),
                    candidate_manifest_path=(
                        synthetic_path
                    ),
                    active_record_path=(
                        synthetic_active
                    ),
                    segment_paths={
                        "segment:00000000":
                            synthetic_segment_missing,
                    },
                ),
        )
    )

    physical_revalidation_active = (
        RUNTIME
        / "physical_revalidation_active.json"
    )

    activation.activate_generation(
        model_pk=MODEL_PK,
        generation_pk=(
            candidate_a[
                "generation_pk"
            ]
        ),
        candidate_manifest_path=(
            candidate_a[
                "manifest_path"
            ]
        ),
        active_record_path=(
            physical_revalidation_active
        ),
        segment_paths=(
            candidate_a[
                "segment_paths"
            ]
        ),
    )

    physical_revalidation_before = (
        physical_revalidation_active.read_bytes()
    )

    negative_controls.append(
        expect_failure(
            label="same_generation_physical_revalidation",
            expected_text=(
                "segment SHA256 mismatch"
            ),
            active_path=(
                physical_revalidation_active
            ),
            expected_active_bytes=(
                physical_revalidation_before
            ),
            operation=lambda:
                activation.activate_generation(
                    model_pk=MODEL_PK,
                    generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                    candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        physical_revalidation_active
                    ),
                    segment_paths=(
                        sha_bad_mapping
                    ),
                ),
        )
    )

    malformed_existing_active = (
        RUNTIME
        / "malformed_existing_active.json"
    )

    malformed_existing_bytes = (
        b"{malformed-active"
    )

    write_bytes_exclusive(
        malformed_existing_active,
        malformed_existing_bytes,
    )

    negative_controls.append(
        expect_failure(
            label="malformed_existing_active_record",
            expected_text=(
                "invalid active record JSON"
            ),
            active_path=(
                malformed_existing_active
            ),
            expected_active_bytes=(
                malformed_existing_bytes
            ),
            operation=lambda:
                activation.activate_generation(
                    model_pk=MODEL_PK,
                    generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                    candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        malformed_existing_active
                    ),
                    segment_paths=(
                        candidate_a[
                            "segment_paths"
                        ]
                    ),
                ),
        )
    )

    cross_model_active = (
        RUNTIME
        / "cross_model_existing_active.json"
    )

    cross_model_record = {
        "schema":
            activation.ACTIVE_SCHEMA,
        "active_generation_version":
            activation.ACTIVE_VERSION,
        "model_pk":
            OTHER_MODEL_PK,
        "generation_pk":
            deterministic_pk(
                generation.GENERATION_PREFIX,
                "other-active-generation",
            ),
        "generation_manifest_sha256":
            hashlib.sha256(
                b"other-active-manifest"
            ).hexdigest(),
    }

    cross_model_bytes = (
        activation.canonical_json_bytes(
            cross_model_record
        )
    )

    write_bytes_exclusive(
        cross_model_active,
        cross_model_bytes,
    )

    negative_controls.append(
        expect_failure(
            label="cross_model_existing_active_record",
            expected_text=(
                "existing active record model mismatch"
            ),
            active_path=(
                cross_model_active
            ),
            expected_active_bytes=(
                cross_model_bytes
            ),
            operation=lambda:
                activation.activate_generation(
                    model_pk=MODEL_PK,
                    generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                    candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        cross_model_active
                    ),
                    segment_paths=(
                        candidate_a[
                            "segment_paths"
                        ]
                    ),
                ),
        )
    )

    partial_active = (
        RUNTIME
        / "preexisting_partial_active.json"
    )

    partial_path = (
        partial_active.with_name(
            partial_active.name
            + ".partial"
        )
    )

    partial_bytes = (
        b"preexisting-partial-evidence"
    )

    write_bytes_exclusive(
        partial_path,
        partial_bytes,
    )

    negative_controls.append(
        expect_failure(
            label="preexisting_partial_active_target",
            expected_text=(
                "partial active record already exists"
            ),
            active_path=(
                partial_active
            ),
            require_active_absent=True,
            partial_path=(
                partial_path
            ),
            expected_partial_bytes=(
                partial_bytes
            ),
            operation=lambda:
                activation.activate_generation(
                    model_pk=MODEL_PK,
                    generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                    candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        partial_active
                    ),
                    segment_paths=(
                        candidate_a[
                            "segment_paths"
                        ]
                    ),
                ),
        )
    )

    multi_keys = list(
        multi[
            "segment_paths"
        ]
    )

    wrong_multi_mapping = {
        multi_keys[0]:
            multi[
                "segment_paths"
            ][
                multi_keys[1]
            ],
        multi_keys[1]:
            multi[
                "segment_paths"
            ][
                multi_keys[0]
            ],
    }

    negative_controls.append(
        expect_failure(
            label="multi_segment_wrong_content_association",
            expected_text=(
                "segment SHA256 mismatch"
            ),
            operation=lambda:
                activation.build_active_record(
                    model_pk=MODEL_PK,
                    generation_pk=(
                        multi[
                            "generation_pk"
                        ]
                    ),
                    candidate_manifest_path=(
                        multi[
                            "manifest_path"
                        ]
                    ),
                    segment_paths=(
                        wrong_multi_mapping
                    ),
                ),
        )
    )

    fault_active = (
        RUNTIME
        / "fault_injection_active.json"
    )

    activation.activate_generation(
        model_pk=MODEL_PK,
        generation_pk=(
            candidate_a[
                "generation_pk"
            ]
        ),
        candidate_manifest_path=(
            candidate_a[
                "manifest_path"
            ]
        ),
        active_record_path=(
            fault_active
        ),
        segment_paths=(
            candidate_a[
                "segment_paths"
            ]
        ),
    )

    fault_before = (
        fault_active.read_bytes()
    )

    original_replace = (
        activation_v1.os.replace
    )

    injected_replace_calls = 0

    def injected_replace(
        source: Any,
        target: Any,
    ) -> None:
        nonlocal injected_replace_calls

        injected_replace_calls += 1

        raise OSError(
            "injected precommit replace failure"
        )

    activation_v1.os.replace = (
        injected_replace
    )

    try:
        fault_control = (
            expect_failure(
                label="injected_failure_before_os_replace",
                expected_text=(
                    "injected precommit replace failure"
                ),
                active_path=(
                    fault_active
                ),
                expected_active_bytes=(
                    fault_before
                ),
                operation=lambda:
                    activation.activate_generation(
                        model_pk=MODEL_PK,
                        generation_pk=(
                            candidate_b[
                                "generation_pk"
                            ]
                        ),
                        candidate_manifest_path=(
                            candidate_b[
                                "manifest_path"
                            ]
                        ),
                        active_record_path=(
                            fault_active
                        ),
                        segment_paths=(
                            candidate_b[
                                "segment_paths"
                            ]
                        ),
                    ),
            )
        )

    finally:
        activation_v1.os.replace = (
            original_replace
        )

    fault_partial = (
        fault_active.with_name(
            fault_active.name
            + ".partial"
        )
    )

    fault_control[
        "replace_calls"
    ] = injected_replace_calls

    fault_control[
        "partial_cleaned"
    ] = not fault_partial.exists()

    fault_control[
        "active_reopens"
    ] = (
        activation.reopen_active_generation(
            fault_active
        )[
            "generation_pk"
        ]
        == candidate_a[
            "generation_pk"
        ]
    )

    fault_control[
        "pass"
    ] = (
        fault_control[
            "pass"
        ]
        and injected_replace_calls
        == 1
        and fault_control[
            "partial_cleaned"
        ]
        and fault_control[
            "active_reopens"
        ]
    )

    negative_controls.append(
        fault_control
    )

    static_checks = (
        static_policy_checks()
    )

    active_expected_fields = {
        "schema",
        "active_generation_version",
        "model_pk",
        "generation_pk",
        "generation_manifest_sha256",
    }

    positive_checks = {
        "candidate_a_reconstruction_exact":
            all(
                reconstruction_a.values()
            ),

        "candidate_b_reconstruction_exact":
            all(
                reconstruction_b.values()
            ),

        "first_activation_changed":
            first.changed is True,

        "first_active_record_exact_fields":
            set(
                first.record
            )
            == active_expected_fields,

        "first_active_record_canonical":
            active_a_bytes
            == activation.canonical_json_bytes(
                first.record
            ),

        "first_active_model_pk_exact":
            first.record[
                "model_pk"
            ]
            == MODEL_PK,

        "first_active_generation_pk_exact":
            first.record[
                "generation_pk"
            ]
            == candidate_a[
                "generation_pk"
            ],

        "first_active_manifest_sha256_exact":
            first.record[
                "generation_manifest_sha256"
            ]
            == expected_manifest_sha_a,

        "first_active_independent_reopen":
            reopened_a
            == first.record,

        "manifest_path_independent":
            relocated_manifest_record
            == record_a,

        "segment_path_independent":
            relocated_segment_record
            == record_a,

        "idempotent_changed_false":
            idempotent.changed
            is False,

        "idempotent_bytes_unchanged":
            active_a_after_idempotent
            == active_a_bytes,

        "idempotent_stat_unchanged":
            (
                active_a_stat_after.st_ino
                == active_a_stat.st_ino
                and active_a_stat_after.st_size
                == active_a_stat.st_size
                and active_a_stat_after.st_mtime_ns
                == active_a_stat.st_mtime_ns
            ),

        "replacement_changed":
            replacement.changed
            is True,

        "replacement_generation_exact":
            replacement.record[
                "generation_pk"
            ]
            == candidate_b[
                "generation_pk"
            ],

        "replacement_manifest_sha_exact":
            replacement.record[
                "generation_manifest_sha256"
            ]
            == expected_manifest_sha_b,

        "replacement_independent_reopen":
            reopened_b
            == replacement.record,

        "replacement_record_changed":
            active_b_bytes
            != active_a_bytes,

        "logical_model_pk_preserved":
            candidate_a[
                "descriptor"
            ][
                "model_pk"
            ]
            == candidate_b[
                "descriptor"
            ][
                "model_pk"
            ]
            == MODEL_PK,

        "logical_object_pks_preserved":
            object_pks_a
            == object_pks_b,

        "active_authority_has_no_execution_paths":
            not any(
                path_text
                in authority_text
                for path_text
                in path_strings
            ),

        "multi_segment_mapping_order_independent":
            multi_record_forward
            == multi_record_reverse,

        "candidate_a_unchanged":
            snapshot_exact(
                snapshot_a
            ),

        "candidate_b_unchanged":
            snapshot_exact(
                snapshot_b
            ),

        "synthetic_manifest_passes_structure_verifier":
            synthetic_manifest_verified,

        "source_model_required":
            False,
    }

    negative_pass = all(
        row[
            "pass"
        ]
        for row
        in negative_controls
    )

    positive_pass = all(
        (
            value is True
            for key, value
            in positive_checks.items()
            if key
            != "source_model_required"
        )
    ) and (
        positive_checks[
            "source_model_required"
        ]
        is False
    )

    static_pass = all(
        static_checks.values()
    )

    all_pass = (
        positive_pass
        and negative_pass
        and static_pass
    )

    return {
        "schema":
            SCHEMA,

        "validation_version":
            VERSION,

        "all_pass":
            all_pass,

        "model_pk":
            MODEL_PK,

        "candidate_a_generation_pk":
            candidate_a[
                "generation_pk"
            ],

        "candidate_b_generation_pk":
            candidate_b[
                "generation_pk"
            ],

        "candidate_a_manifest_sha256":
            expected_manifest_sha_a,

        "candidate_b_manifest_sha256":
            expected_manifest_sha_b,

        "positive": {
            "checks":
                positive_checks,

            "active_a_record":
                first.record,

            "active_b_record":
                replacement.record,

            "reconstruction_a":
                reconstruction_a,

            "reconstruction_b":
                reconstruction_b,
        },

        "multi_segment_mapping": {
            "generation_pk":
                multi[
                    "generation_pk"
                ],

            "forward_reverse_equal":
                multi_record_forward
                == multi_record_reverse,

            "pass":
                multi_record_forward
                == multi_record_reverse,
        },

        "negative_controls":
            negative_controls,

        "atomicity": {
            "failed_replacement_prior_bytes_preserved":
                fault_control[
                    "failed_closed"
                ],

            "injected_replace_calls":
                injected_replace_calls,

            "partial_cleaned":
                fault_control[
                    "partial_cleaned"
                ],

            "prior_active_reopens":
                fault_control[
                    "active_reopens"
                ],

            "pass":
                fault_control[
                    "pass"
                ],
        },

        "static_policy_checks":
            static_checks,

        "source_gguf_required":
            False,

        "activation_validation_executed":
            True,

        "controlled_generation_activated":
            True,

        "rollback_implemented":
            False,

        "catalog_engine_selected":
            False,

        "maf_native_compute_enabled":
            False,

        "inference_performed":
            False,
    }


def main() -> None:
    if RESULT.exists():
        raise RuntimeError(
            "raw validation result already exists"
        )

    if RESULT_PARTIAL.exists():
        raise RuntimeError(
            "raw validation result partial already exists"
        )

    if RUNTIME.exists():
        raise RuntimeError(
            "validation runtime already exists"
        )

    RUNTIME.mkdir(
        parents=True,
        exist_ok=False,
    )

    try:
        result = run_validation()

    except Exception as exc:
        result = {
            "schema":
                SCHEMA,

            "validation_version":
                VERSION,

            "all_pass":
                False,

            "harness_error": {
                "error_type":
                    type(exc).__name__,

                "error_text":
                    str(exc),
            },

            "source_gguf_required":
                False,

            "rollback_implemented":
                False,

            "catalog_engine_selected":
                False,

            "maf_native_compute_enabled":
                False,

            "inference_performed":
                False,
        }

    persist_result(
        result
    )

    reopened = json.loads(
        RESULT.read_text(
            encoding="utf-8"
        )
    )

    if (
        generation.canonical_json_bytes(
            reopened
        )
        != RESULT.read_bytes()
    ):
        raise RuntimeError(
            "raw validation result is not canonical"
        )

    print("=" * 72)
    print(
        " OPENMIND / MAF ACTIVATION V1.1 VALIDATION"
    )
    print("=" * 72)

    print(
        "schema:",
        result[
            "schema"
        ],
    )

    print(
        "all_pass:",
        result[
            "all_pass"
        ],
    )

    if "positive" in result:
        print(
            "positive:",
            all(
                (
                    value is True
                    for key, value
                    in result[
                        "positive"
                    ][
                        "checks"
                    ].items()
                    if key
                    != "source_model_required"
                )
            )
            and (
                result[
                    "positive"
                ][
                    "checks"
                ][
                    "source_model_required"
                ]
                is False
            ),
        )

    if "negative_controls" in result:
        print(
            "negative controls:",
            all(
                row[
                    "pass"
                ]
                for row
                in result[
                    "negative_controls"
                ]
            ),
        )

    if "atomicity" in result:
        print(
            "atomicity:",
            result[
                "atomicity"
            ][
                "pass"
            ],
        )

    if "static_policy_checks" in result:
        print(
            "static policy:",
            all(
                result[
                    "static_policy_checks"
                ].values()
            ),
        )

    print(
        "source_gguf_required:",
        result.get(
            "source_gguf_required"
        ),
    )

    print(
        "rollback_implemented:",
        result.get(
            "rollback_implemented"
        ),
    )

    print(
        "result:",
        RESULT,
    )

    if result[
        "all_pass"
    ] is not True:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
