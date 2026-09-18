#!/usr/bin/env python3

"""Frozen MAF Rollback V1 validation runner.

This runner validates operational reactivation of retained immutable
generation evidence.

It does not create historical-authority provenance.
It does not require a source GGUF.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Callable

import maf_activation_v1_1 as activation
import maf_rollback_v1 as rollback


SCHEMA = "openmind.maf_rollback_validation.v1"
VERSION = "maf_rollback_validation_v1"

ROOT = Path(__file__).resolve().parents[2]
MODULE_DIR = Path(__file__).resolve().parent

SOURCE_ACTIVATION_RESULT = (
    MODULE_DIR
    / "maf_activation_validation_v1_1_1.json"
)

SOURCE_ACTIVATION_RUNTIME = (
    ROOT
    / "results/runtime"
    / "maf_activation_validation_v1_1_1"
)

RUNTIME = (
    ROOT
    / "results/runtime"
    / "maf_rollback_validation_v1"
)

RESULT = (
    MODULE_DIR
    / "maf_rollback_validation_v1.json"
)

RESULT_PARTIAL = RESULT.with_name(
    RESULT.name
    + ".partial"
)

ROLLBACK_PROTOCOL = (
    MODULE_DIR
    / "MAF_ROLLBACK_V1_PROTOCOL.md"
)

ROLLBACK_ENGINE = (
    MODULE_DIR
    / "maf_rollback_v1.py"
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

ACTIVATION_FINAL_RUNNER = (
    MODULE_DIR
    / "maf_activation_validation_v1_1_1.py"
)

EXPECTED_ROLLBACK_PROTOCOL_SHA256 = (
    "0d71f4eb28ea35658d9c24a55d085e54"
    "b6cc6a5c92cda9dc2a17dfe57df07a42"
)

EXPECTED_ROLLBACK_ENGINE_SHA256 = (
    "73b02c26f840d59499dd7be86985db6a"
    "3a14720769de1d040f2cad9c78703b79"
)

EXPECTED_ACTIVATION_V1_SHA256 = (
    "76d79f90d9bc30118a6dfe0297beacd9"
    "b323aed9f56876881f653a2c01c1f210"
)

EXPECTED_ACTIVATION_V11_SHA256 = (
    "9435ae8dd32656c7350887689d453f3c"
    "b8460887068bfaf06e6f68b5b5b927a1"
)

EXPECTED_GENERATION_ENGINE_SHA256 = (
    "8868c58e98084226dd957391e1a2f4d1"
    "122e886607640ae0be59279f025f1a51"
)

EXPECTED_ACTIVATION_FINAL_RUNNER_SHA256 = (
    "7d6d5c106cd8b438938a1d6d33bb55e"
    "9c107795f8da05207c210bd94ebdb42d2"
)

EXPECTED_ACTIVATION_RESULT_SHA256 = (
    "586f4a4958aab67972dc06845171ee79"
    "bfe937dfcd731f1f5b3fc594df841ac8"
)

OTHER_MODEL_PK = (
    "mafmodel:v1:"
    + hashlib.sha256(
        b"openmind-rollback-v1-other-model"
    ).hexdigest()
)

OTHER_GENERATION_PK = (
    "mafgen:v1:"
    + hashlib.sha256(
        b"openmind-rollback-v1-other-generation"
    ).hexdigest()
)


def canonical_json_bytes(
    value: Any,
) -> bytes:
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


def sha256_bytes(
    value: bytes,
) -> str:
    return hashlib.sha256(
        value
    ).hexdigest()


def file_sha256(
    path: Path,
) -> str:
    h = hashlib.sha256()

    with path.open(
        "rb"
    ) as f:
        while True:
            block = f.read(
                1024
                * 1024
            )

            if not block:
                break

            h.update(
                block
            )

    return h.hexdigest()


def write_bytes_exclusive(
    path: Path,
    value: bytes,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "xb"
    ) as f:
        f.write(
            value
        )
        f.flush()
        os.fsync(
            f.fileno()
        )


def write_canonical_json(
    path: Path,
    value: Any,
) -> None:
    write_bytes_exclusive(
        path,
        canonical_json_bytes(
            value
        ),
    )


def snapshot_tree(
    root: Path,
) -> dict[str, tuple[int, str]]:
    result = {}

    for path in sorted(
        root.rglob(
            "*"
        )
    ):
        if not path.is_file():
            continue

        relative = str(
            path.relative_to(
                root
            )
        )

        result[
            relative
        ] = (
            path.stat().st_size,
            file_sha256(
                path
            ),
        )

    return result


def find_files_by_sha(
    root: Path,
    expected_sha256: str,
    *,
    expected_length: int | None = None,
) -> list[Path]:
    matches = []

    for path in sorted(
        root.rglob(
            "*"
        )
    ):
        if not path.is_file():
            continue

        if (
            expected_length
            is not None
            and path.stat().st_size
            != expected_length
        ):
            continue

        if file_sha256(
            path
        ) == expected_sha256:
            matches.append(
                path
            )

    return matches


def locate_manifest(
    expected_sha256: str,
) -> Path:
    matches = find_files_by_sha(
        SOURCE_ACTIVATION_RUNTIME,
        expected_sha256,
    )

    json_matches = [
        path
        for path in matches
        if path.suffix
        == ".json"
    ]

    if not json_matches:
        raise RuntimeError(
            "retained activation manifest not found"
        )

    return json_matches[0]


def load_canonical_manifest(
    path: Path,
) -> tuple[
    dict[str, Any],
    bytes,
]:
    raw = path.read_bytes()

    value = json.loads(
        raw.decode(
            "utf-8"
        )
    )

    if not isinstance(
        value,
        dict,
    ):
        raise RuntimeError(
            "retained manifest is not an object"
        )

    if raw != canonical_json_bytes(
        value
    ):
        raise RuntimeError(
            "retained manifest is not canonical"
        )

    return (
        value,
        raw,
    )


def descriptor_segments(
    manifest: dict[str, Any],
) -> list[dict[str, Any]]:
    descriptor = manifest.get(
        "descriptor"
    )

    if not isinstance(
        descriptor,
        dict,
    ):
        raise RuntimeError(
            "manifest descriptor missing"
        )

    segments = descriptor.get(
        "segments"
    )

    if not isinstance(
        segments,
        list,
    ) or not segments:
        raise RuntimeError(
            "descriptor segments missing"
        )

    for row in segments:
        if not isinstance(
            row,
            dict,
        ):
            raise RuntimeError(
                "invalid descriptor segment"
            )

        for key in (
            "segment_id",
            "segment_length",
            "segment_sha256",
        ):
            if key not in row:
                raise RuntimeError(
                    "descriptor segment field missing: "
                    + key
                )

    return segments


def retained_segment_mapping(
    manifest: dict[str, Any],
) -> dict[str, Path]:
    mapping = {}

    for row in descriptor_segments(
        manifest
    ):
        segment_id = row[
            "segment_id"
        ]

        expected_length = row[
            "segment_length"
        ]

        expected_sha256 = row[
            "segment_sha256"
        ]

        matches = find_files_by_sha(
            SOURCE_ACTIVATION_RUNTIME,
            expected_sha256,
            expected_length=(
                expected_length
            ),
        )

        if not matches:
            raise RuntimeError(
                "retained segment evidence not found: "
                + segment_id
            )

        mapping[
            segment_id
        ] = matches[0]

    return mapping


def copy_candidate(
    *,
    label: str,
    manifest_sha256: str,
) -> dict[str, Any]:
    source_manifest_path = locate_manifest(
        manifest_sha256
    )

    manifest, manifest_bytes = (
        load_canonical_manifest(
            source_manifest_path
        )
    )

    source_mapping = (
        retained_segment_mapping(
            manifest
        )
    )

    target_dir = (
        RUNTIME
        / "candidates"
        / label
    )

    target_manifest_path = (
        target_dir
        / "candidate.manifest.json"
    )

    write_bytes_exclusive(
        target_manifest_path,
        manifest_bytes,
    )

    target_mapping = {}

    for index, row in enumerate(
        descriptor_segments(
            manifest
        )
    ):
        segment_id = row[
            "segment_id"
        ]

        source_path = (
            source_mapping[
                segment_id
            ]
        )

        target_path = (
            target_dir
            / (
                f"segment_{index:04d}.mafseg"
            )
        )

        write_bytes_exclusive(
            target_path,
            source_path.read_bytes(),
        )

        target_mapping[
            segment_id
        ] = target_path

    return {
        "generation_pk":
            manifest[
                "generation_pk"
            ],
        "manifest":
            manifest,
        "manifest_bytes":
            manifest_bytes,
        "manifest_path":
            target_manifest_path,
        "manifest_sha256":
            sha256_bytes(
                manifest_bytes
            ),
        "segment_paths":
            target_mapping,
    }


def relocate_candidate(
    *,
    label: str,
    candidate: dict[str, Any],
) -> dict[str, Any]:
    target_dir = (
        RUNTIME
        / "relocated"
        / label
    )

    target_manifest_path = (
        target_dir
        / "candidate.manifest.json"
    )

    write_bytes_exclusive(
        target_manifest_path,
        candidate[
            "manifest_bytes"
        ],
    )

    target_mapping = {}

    for index, (
        segment_id,
        source_path,
    ) in enumerate(
        sorted(
            candidate[
                "segment_paths"
            ].items()
        )
    ):
        target_path = (
            target_dir
            / (
                f"copy_{index:04d}.mafseg"
            )
        )

        write_bytes_exclusive(
            target_path,
            source_path.read_bytes(),
        )

        target_mapping[
            segment_id
        ] = target_path

    return {
        "generation_pk":
            candidate[
                "generation_pk"
            ],
        "manifest":
            candidate[
                "manifest"
            ],
        "manifest_bytes":
            candidate[
                "manifest_bytes"
            ],
        "manifest_path":
            target_manifest_path,
        "manifest_sha256":
            candidate[
                "manifest_sha256"
            ],
        "segment_paths":
            target_mapping,
    }


def copy_mapping(
    value: dict[str, Path],
) -> dict[str, Path]:
    return {
        key:
            Path(
                path
            )
        for key, path
        in value.items()
    }


def expect_failure(
    *,
    label: str,
    operation: Callable[[], Any],
    expected_error_types: tuple[str, ...] = (
        "MAFActivationError",
    ),
    expected_texts: tuple[str, ...] | None = None,
    active_path: Path | None = None,
    expected_active_bytes: bytes | None = None,
    require_partial_absent: bool = False,
) -> dict[str, Any]:
    raised = False
    error_type = None
    error_text = None

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

    type_match = (
        raised
        and error_type
        in expected_error_types
    )

    if expected_texts is None:
        text_match = True
    else:
        text_match = (
            error_text is not None
            and any(
                item
                in error_text
                for item
                in expected_texts
            )
        )

    active_preserved = True

    if (
        active_path
        is not None
        and expected_active_bytes
        is not None
    ):
        active_preserved = (
            active_path.is_file()
            and active_path.read_bytes()
            == expected_active_bytes
        )

    partial_absent = True

    if (
        active_path
        is not None
        and require_partial_absent
    ):
        partial = active_path.with_name(
            active_path.name
            + ".partial"
        )

        partial_absent = (
            not partial.exists()
        )

    passed = (
        type_match
        and text_match
        and active_preserved
        and partial_absent
    )

    return {
        "label":
            label,
        "pass":
            passed,
        "raised":
            raised,
        "error_type":
            error_type,
        "error_text":
            error_text,
        "failed_closed":
            (
                active_preserved
                and partial_absent
            ),
    }


def version_field(
    manifest: dict[str, Any],
) -> str:
    candidates = [
        key
        for key in manifest
        if (
            key != "schema"
            and "version"
            in key.lower()
        )
    ]

    if len(
        candidates
    ) != 1:
        raise RuntimeError(
            "manifest version field not uniquely identifiable"
        )

    return candidates[0]


def write_manifest_variant(
    *,
    name: str,
    base_manifest: dict[str, Any],
    mutation: Callable[
        [dict[str, Any]],
        None,
    ],
    canonical: bool = True,
) -> Path:
    value = json.loads(
        json.dumps(
            base_manifest
        )
    )

    mutation(
        value
    )

    path = (
        RUNTIME
        / "variants"
        / (
            name
            + ".manifest.json"
        )
    )

    if canonical:
        raw = canonical_json_bytes(
            value
        )
    else:
        raw = json.dumps(
            value,
            indent=2,
            sort_keys=False,
        ).encode(
            "utf-8"
        )

    write_bytes_exclusive(
        path,
        raw,
    )

    return path


def write_active_variant(
    *,
    name: str,
    base_record: dict[str, Any],
    mutation: Callable[
        [dict[str, Any]],
        None,
    ] | None = None,
    canonical: bool = True,
) -> Path:
    value = json.loads(
        json.dumps(
            base_record
        )
    )

    if mutation is not None:
        mutation(
            value
        )

    path = (
        RUNTIME
        / "authority_variants"
        / (
            name
            + ".json"
        )
    )

    if canonical:
        raw = canonical_json_bytes(
            value
        )
    else:
        raw = json.dumps(
            value,
            indent=2,
        ).encode(
            "utf-8"
        )

    write_bytes_exclusive(
        path,
        raw,
    )

    return path


def active_copy(
    *,
    name: str,
    active_bytes: bytes,
) -> Path:
    path = (
        RUNTIME
        / "authority_cases"
        / (
            name
            + ".json"
        )
    )

    write_bytes_exclusive(
        path,
        active_bytes,
    )

    return path


def inherited_activation_control(
    *,
    activation_result: dict[str, Any],
    label: str,
) -> dict[str, Any]:
    rows = [
        row
        for row
        in activation_result[
            "negative_controls"
        ]
        if row.get(
            "label"
        ) == label
    ]

    if len(
        rows
    ) != 1:
        return {
            "label":
                label,
            "pass":
                False,
            "mode":
                "inherited_frozen_activation_v1_1_1",
            "error":
                "control not uniquely present",
        }

    source = rows[0]

    return {
        "label":
            label,
        "pass":
            source.get(
                "pass"
            ) is True,
        "mode":
            "inherited_frozen_activation_v1_1_1",
        "source_error_type":
            source.get(
                "error_type"
            ),
        "source_error_text":
            source.get(
                "error_text"
            ),
        "source_failed_closed":
            source.get(
                "failed_closed"
            ),
    }


def static_policy_checks() -> dict[str, bool]:
    rollback_text = (
        ROLLBACK_ENGINE.read_text()
    )

    rollback_tree = ast.parse(
        rollback_text
    )

    imports = []

    for node in rollback_tree.body:
        if isinstance(
            node,
            ast.Import,
        ):
            imports.extend(
                alias.name
                for alias
                in node.names
            )

        elif isinstance(
            node,
            ast.ImportFrom,
        ):
            imports.append(
                node.module
            )

    function_names = {
        node.name
        for node in rollback_tree.body
        if isinstance(
            node,
            ast.FunctionDef,
        )
    }

    direct_replace = False
    direct_delete = False

    for node in ast.walk(
        rollback_tree
    ):
        if isinstance(
            node,
            ast.Attribute,
        ):
            if node.attr == "replace":
                direct_replace = True

            if node.attr in {
                "unlink",
                "remove",
                "delete_generation",
                "retire_generation",
                "purge_generation",
            }:
                direct_delete = True

    return {
        "rollback_protocol_exact":
            file_sha256(
                ROLLBACK_PROTOCOL
            )
            == EXPECTED_ROLLBACK_PROTOCOL_SHA256,

        "rollback_engine_exact":
            file_sha256(
                ROLLBACK_ENGINE
            )
            == EXPECTED_ROLLBACK_ENGINE_SHA256,

        "activation_v1_exact":
            file_sha256(
                ACTIVATION_V1_ENGINE
            )
            == EXPECTED_ACTIVATION_V1_SHA256,

        "activation_v11_exact":
            file_sha256(
                ACTIVATION_V11_ENGINE
            )
            == EXPECTED_ACTIVATION_V11_SHA256,

        "generation_engine_exact":
            file_sha256(
                GENERATION_ENGINE
            )
            == EXPECTED_GENERATION_ENGINE_SHA256,

        "activation_final_runner_exact":
            file_sha256(
                ACTIVATION_FINAL_RUNNER
            )
            == EXPECTED_ACTIVATION_FINAL_RUNNER_SHA256,

        "activation_final_result_exact":
            file_sha256(
                SOURCE_ACTIVATION_RESULT
            )
            == EXPECTED_ACTIVATION_RESULT_SHA256,

        "rollback_imports_activation_v11_only":
            imports
            == [
                "maf_activation_v1_1",
            ],

        "rollback_public_surface_exact":
            function_names
            == {
                "rollback_generation",
            },

        "rollback_no_direct_replace":
            not direct_replace,

        "rollback_no_generation_deletion":
            not direct_delete,

        "rollback_no_sqlite":
            "sqlite3"
            not in rollback_text,

        "rollback_no_mmap":
            "mmap"
            not in rollback_text,

        "rollback_no_source_gguf_literal":
            ".gguf"
            not in rollback_text.lower(),

        "rollback_no_historical_authority_claim":
            (
                "does not create or infer "
                "historical-authority provenance"
            )
            in rollback_text,

        "rollback_no_phase_6b9_surface":
            (
                "resident_lookup"
                not in function_names
                and "resident_directory"
                not in function_names
            ),
    }


def persist_result(
    value: dict[str, Any],
) -> None:
    if RESULT.exists():
        raise RuntimeError(
            "rollback validation result already exists"
        )

    if RESULT_PARTIAL.exists():
        raise RuntimeError(
            "rollback validation result partial already exists"
        )

    raw = canonical_json_bytes(
        value
    )

    with RESULT_PARTIAL.open(
        "xb"
    ) as f:
        f.write(
            raw
        )
        f.flush()
        os.fsync(
            f.fileno()
        )

    reopened = (
        RESULT_PARTIAL.read_bytes()
    )

    if reopened != raw:
        raise RuntimeError(
            "rollback result partial reopen mismatch"
        )

    decoded = json.loads(
        reopened.decode(
            "utf-8"
        )
    )

    if canonical_json_bytes(
        decoded
    ) != reopened:
        raise RuntimeError(
            "rollback result partial not canonical"
        )

    os.replace(
        RESULT_PARTIAL,
        RESULT,
    )


def run_validation() -> dict[str, Any]:
    activation_result = json.loads(
        SOURCE_ACTIVATION_RESULT.read_text(
            encoding="utf-8"
        )
    )

    if activation_result.get(
        "all_pass"
    ) is not True:
        raise RuntimeError(
            "frozen activation validation is not all_pass=true"
        )

    if not SOURCE_ACTIVATION_RUNTIME.is_dir():
        raise RuntimeError(
            "retained activation runtime missing"
        )

    source_snapshot_before = snapshot_tree(
        SOURCE_ACTIVATION_RUNTIME
    )

    RUNTIME.mkdir(
        parents=True,
        exist_ok=False,
    )

    model_pk = activation_result[
        "model_pk"
    ]

    candidate_a = copy_candidate(
        label="candidate_a",
        manifest_sha256=(
            activation_result[
                "candidate_a_manifest_sha256"
            ]
        ),
    )

    candidate_b = copy_candidate(
        label="candidate_b",
        manifest_sha256=(
            activation_result[
                "candidate_b_manifest_sha256"
            ]
        ),
    )

    if (
        candidate_a[
            "generation_pk"
        ]
        != activation_result[
            "candidate_a_generation_pk"
        ]
    ):
        raise RuntimeError(
            "candidate A retained identity mismatch"
        )

    if (
        candidate_b[
            "generation_pk"
        ]
        != activation_result[
            "candidate_b_generation_pk"
        ]
    ):
        raise RuntimeError(
            "candidate B retained identity mismatch"
        )

    relocated_b = relocate_candidate(
        label="candidate_b",
        candidate=candidate_b,
    )

    retained_copy_before = snapshot_tree(
        RUNTIME
        / "candidates"
    )

    active_path = (
        RUNTIME
        / "active_generation.json"
    )

    initial = activation.activate_generation(
        model_pk=model_pk,
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
        active_record_path=active_path,
        segment_paths=(
            candidate_a[
                "segment_paths"
            ]
        ),
    )

    active_a_bytes = (
        active_path.read_bytes()
    )

    active_a_record = (
        activation.reopen_active_generation(
            active_path
        )
    )

    rollback_to_b = rollback.rollback_generation(
        model_pk=model_pk,
        target_generation_pk=(
            candidate_b[
                "generation_pk"
            ]
        ),
        target_candidate_manifest_path=(
            candidate_b[
                "manifest_path"
            ]
        ),
        active_record_path=active_path,
        target_segment_paths=(
            candidate_b[
                "segment_paths"
            ]
        ),
    )

    active_b_bytes = (
        active_path.read_bytes()
    )

    active_b_record = (
        activation.reopen_active_generation(
            active_path
        )
    )

    rollback_to_a = rollback.rollback_generation(
        model_pk=model_pk,
        target_generation_pk=(
            candidate_a[
                "generation_pk"
            ]
        ),
        target_candidate_manifest_path=(
            candidate_a[
                "manifest_path"
            ]
        ),
        active_record_path=active_path,
        target_segment_paths=(
            candidate_a[
                "segment_paths"
            ]
        ),
    )

    active_a2_bytes = (
        active_path.read_bytes()
    )

    same_generation = rollback.rollback_generation(
        model_pk=model_pk,
        target_generation_pk=(
            candidate_a[
                "generation_pk"
            ]
        ),
        target_candidate_manifest_path=(
            candidate_a[
                "manifest_path"
            ]
        ),
        active_record_path=active_path,
        target_segment_paths=(
            candidate_a[
                "segment_paths"
            ]
        ),
    )

    same_generation_bytes = (
        active_path.read_bytes()
    )

    relocated_to_b = rollback.rollback_generation(
        model_pk=model_pk,
        target_generation_pk=(
            relocated_b[
                "generation_pk"
            ]
        ),
        target_candidate_manifest_path=(
            relocated_b[
                "manifest_path"
            ]
        ),
        active_record_path=active_path,
        target_segment_paths=(
            relocated_b[
                "segment_paths"
            ]
        ),
    )

    relocated_b_bytes = (
        active_path.read_bytes()
    )

    rollback.rollback_generation(
        model_pk=model_pk,
        target_generation_pk=(
            candidate_a[
                "generation_pk"
            ]
        ),
        target_candidate_manifest_path=(
            candidate_a[
                "manifest_path"
            ]
        ),
        active_record_path=active_path,
        target_segment_paths=(
            candidate_a[
                "segment_paths"
            ]
        ),
    )

    positive_checks = {
        "initial_a_activation_changed":
            getattr(
                initial,
                "changed",
                None,
            )
            is True,

        "rollback_a_to_b_changed":
            getattr(
                rollback_to_b,
                "changed",
                None,
            )
            is True,

        "rollback_b_to_a_changed":
            getattr(
                rollback_to_a,
                "changed",
                None,
            )
            is True,

        "same_generation_changed_false":
            getattr(
                same_generation,
                "changed",
                None,
            )
            is False,

        "same_generation_bytes_unchanged":
            same_generation_bytes
            == active_a2_bytes,

        "relocated_b_changed":
            getattr(
                relocated_to_b,
                "changed",
                None,
            )
            is True,

        "path_independent_active_b_bytes":
            relocated_b_bytes
            == active_b_bytes,

        "active_a_generation_exact":
            active_a_record[
                "generation_pk"
            ]
            == candidate_a[
                "generation_pk"
            ],

        "active_b_generation_exact":
            active_b_record[
                "generation_pk"
            ]
            == candidate_b[
                "generation_pk"
            ],

        "active_a_model_exact":
            active_a_record[
                "model_pk"
            ]
            == model_pk,

        "active_b_model_exact":
            active_b_record[
                "model_pk"
            ]
            == model_pk,

        "active_a_manifest_binding_exact":
            active_a_record[
                "generation_manifest_sha256"
            ]
            == candidate_a[
                "manifest_sha256"
            ],

        "active_b_manifest_binding_exact":
            active_b_record[
                "generation_manifest_sha256"
            ]
            == candidate_b[
                "manifest_sha256"
            ],

        "active_record_exact_five_fields":
            set(
                active_b_record
            )
            == {
                "schema",
                "active_generation_version",
                "model_pk",
                "generation_pk",
                "generation_manifest_sha256",
            },

        "rollback_b_to_a_restores_exact_a_authority":
            active_a2_bytes
            == active_a_bytes,

        "candidate_a_retained":
            candidate_a[
                "manifest_path"
            ].is_file(),

        "candidate_b_retained":
            candidate_b[
                "manifest_path"
            ].is_file(),

        "source_model_required":
            False,

        "source_gguf_required":
            False,
    }

    negative_controls = []

    missing_current = (
        RUNTIME
        / "negative"
        / "missing_current.json"
    )

    negative_controls.append(
        expect_failure(
            label="missing_current_authority",
            operation=lambda:
                rollback.rollback_generation(
                    model_pk=model_pk,
                    target_generation_pk=(
                        candidate_b[
                            "generation_pk"
                        ]
                    ),
                    target_candidate_manifest_path=(
                        candidate_b[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        missing_current
                    ),
                    target_segment_paths=(
                        candidate_b[
                            "segment_paths"
                        ]
                    ),
                ),
        )
    )

    malformed_current = (
        RUNTIME
        / "negative"
        / "malformed_current.json"
    )

    write_bytes_exclusive(
        malformed_current,
        b"{",
    )

    negative_controls.append(
        expect_failure(
            label="malformed_current_authority",
            operation=lambda:
                rollback.rollback_generation(
                    model_pk=model_pk,
                    target_generation_pk=(
                        candidate_b[
                            "generation_pk"
                        ]
                    ),
                    target_candidate_manifest_path=(
                        candidate_b[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        malformed_current
                    ),
                    target_segment_paths=(
                        candidate_b[
                            "segment_paths"
                        ]
                    ),
                ),
            active_path=malformed_current,
            expected_active_bytes=b"{",
        )
    )

    noncanonical_current = write_active_variant(
        name="noncanonical_current",
        base_record=active_a_record,
        canonical=False,
    )

    noncanonical_current_bytes = (
        noncanonical_current.read_bytes()
    )

    negative_controls.append(
        expect_failure(
            label="noncanonical_current_authority",
            operation=lambda:
                rollback.rollback_generation(
                    model_pk=model_pk,
                    target_generation_pk=(
                        candidate_b[
                            "generation_pk"
                        ]
                    ),
                    target_candidate_manifest_path=(
                        candidate_b[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        noncanonical_current
                    ),
                    target_segment_paths=(
                        candidate_b[
                            "segment_paths"
                        ]
                    ),
                ),
            active_path=noncanonical_current,
            expected_active_bytes=(
                noncanonical_current_bytes
            ),
        )
    )

    cross_model_current = write_active_variant(
        name="cross_model_current",
        base_record=active_a_record,
        mutation=lambda value:
            value.__setitem__(
                "model_pk",
                OTHER_MODEL_PK,
            ),
    )

    cross_model_bytes = (
        cross_model_current.read_bytes()
    )

    negative_controls.append(
        expect_failure(
            label="cross_model_current_authority",
            operation=lambda:
                rollback.rollback_generation(
                    model_pk=model_pk,
                    target_generation_pk=(
                        candidate_b[
                            "generation_pk"
                        ]
                    ),
                    target_candidate_manifest_path=(
                        candidate_b[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        cross_model_current
                    ),
                    target_segment_paths=(
                        candidate_b[
                            "segment_paths"
                        ]
                    ),
                ),
            expected_texts=(
                "active model_pk mismatch",
            ),
            active_path=cross_model_current,
            expected_active_bytes=(
                cross_model_bytes
            ),
        )
    )

    malformed_model_active = active_copy(
        name="malformed_requested_model_pk",
        active_bytes=active_a_bytes,
    )

    negative_controls.append(
        expect_failure(
            label="malformed_requested_model_pk",
            operation=lambda:
                rollback.rollback_generation(
                    model_pk="not-a-model-pk",
                    target_generation_pk=(
                        candidate_b[
                            "generation_pk"
                        ]
                    ),
                    target_candidate_manifest_path=(
                        candidate_b[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        malformed_model_active
                    ),
                    target_segment_paths=(
                        candidate_b[
                            "segment_paths"
                        ]
                    ),
                ),
            active_path=malformed_model_active,
            expected_active_bytes=(
                active_a_bytes
            ),
        )
    )

    malformed_generation_active = active_copy(
        name="malformed_target_generation_pk",
        active_bytes=active_a_bytes,
    )

    negative_controls.append(
        expect_failure(
            label="malformed_target_generation_pk",
            operation=lambda:
                rollback.rollback_generation(
                    model_pk=model_pk,
                    target_generation_pk=(
                        "not-a-generation-pk"
                    ),
                    target_candidate_manifest_path=(
                        candidate_b[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        malformed_generation_active
                    ),
                    target_segment_paths=(
                        candidate_b[
                            "segment_paths"
                        ]
                    ),
                ),
            active_path=malformed_generation_active,
            expected_active_bytes=(
                active_a_bytes
            ),
        )
    )

    missing_manifest_active = active_copy(
        name="missing_target_manifest",
        active_bytes=active_a_bytes,
    )

    missing_manifest = (
        RUNTIME
        / "negative"
        / "missing_target.manifest.json"
    )

    negative_controls.append(
        expect_failure(
            label="missing_target_manifest",
            operation=lambda:
                rollback.rollback_generation(
                    model_pk=model_pk,
                    target_generation_pk=(
                        candidate_b[
                            "generation_pk"
                        ]
                    ),
                    target_candidate_manifest_path=(
                        missing_manifest
                    ),
                    active_record_path=(
                        missing_manifest_active
                    ),
                    target_segment_paths=(
                        candidate_b[
                            "segment_paths"
                        ]
                    ),
                ),
            active_path=missing_manifest_active,
            expected_active_bytes=(
                active_a_bytes
            ),
        )
    )

    malformed_target = (
        RUNTIME
        / "variants"
        / "malformed_target.manifest.json"
    )

    write_bytes_exclusive(
        malformed_target,
        b"{",
    )

    malformed_target_active = active_copy(
        name="malformed_target_json",
        active_bytes=active_a_bytes,
    )

    negative_controls.append(
        expect_failure(
            label="malformed_target_json",
            operation=lambda:
                rollback.rollback_generation(
                    model_pk=model_pk,
                    target_generation_pk=(
                        candidate_b[
                            "generation_pk"
                        ]
                    ),
                    target_candidate_manifest_path=(
                        malformed_target
                    ),
                    active_record_path=(
                        malformed_target_active
                    ),
                    target_segment_paths=(
                        candidate_b[
                            "segment_paths"
                        ]
                    ),
                ),
            active_path=malformed_target_active,
            expected_active_bytes=(
                active_a_bytes
            ),
        )
    )

    invalid_schema = write_manifest_variant(
        name="invalid_schema",
        base_manifest=(
            candidate_b[
                "manifest"
            ]
        ),
        mutation=lambda value:
            value.__setitem__(
                "schema",
                "invalid.rollback.schema",
            ),
    )

    invalid_schema_active = active_copy(
        name="invalid_target_schema",
        active_bytes=active_a_bytes,
    )

    negative_controls.append(
        expect_failure(
            label="invalid_target_schema",
            operation=lambda:
                rollback.rollback_generation(
                    model_pk=model_pk,
                    target_generation_pk=(
                        candidate_b[
                            "generation_pk"
                        ]
                    ),
                    target_candidate_manifest_path=(
                        invalid_schema
                    ),
                    active_record_path=(
                        invalid_schema_active
                    ),
                    target_segment_paths=(
                        candidate_b[
                            "segment_paths"
                        ]
                    ),
                ),
            active_path=invalid_schema_active,
            expected_active_bytes=(
                active_a_bytes
            ),
        )
    )

    vkey = version_field(
        candidate_b[
            "manifest"
        ]
    )

    invalid_version = write_manifest_variant(
        name="invalid_version",
        base_manifest=(
            candidate_b[
                "manifest"
            ]
        ),
        mutation=lambda value:
            value.__setitem__(
                vkey,
                "invalid-version",
            ),
    )

    invalid_version_active = active_copy(
        name="invalid_target_version",
        active_bytes=active_a_bytes,
    )

    negative_controls.append(
        expect_failure(
            label="invalid_target_version",
            operation=lambda:
                rollback.rollback_generation(
                    model_pk=model_pk,
                    target_generation_pk=(
                        candidate_b[
                            "generation_pk"
                        ]
                    ),
                    target_candidate_manifest_path=(
                        invalid_version
                    ),
                    active_record_path=(
                        invalid_version_active
                    ),
                    target_segment_paths=(
                        candidate_b[
                            "segment_paths"
                        ]
                    ),
                ),
            active_path=invalid_version_active,
            expected_active_bytes=(
                active_a_bytes
            ),
        )
    )

    derivation_mismatch = write_manifest_variant(
        name="generation_derivation_mismatch",
        base_manifest=(
            candidate_b[
                "manifest"
            ]
        ),
        mutation=lambda value:
            value.__setitem__(
                "generation_pk",
                OTHER_GENERATION_PK,
            ),
    )

    derivation_active = active_copy(
        name="target_generation_derivation_mismatch",
        active_bytes=active_a_bytes,
    )

    negative_controls.append(
        expect_failure(
            label="target_generation_derivation_mismatch",
            operation=lambda:
                rollback.rollback_generation(
                    model_pk=model_pk,
                    target_generation_pk=(
                        OTHER_GENERATION_PK
                    ),
                    target_candidate_manifest_path=(
                        derivation_mismatch
                    ),
                    active_record_path=(
                        derivation_active
                    ),
                    target_segment_paths=(
                        candidate_b[
                            "segment_paths"
                        ]
                    ),
                ),
            active_path=derivation_active,
            expected_active_bytes=(
                active_a_bytes
            ),
        )
    )

    requested_generation_active = active_copy(
        name="requested_generation_mismatch",
        active_bytes=active_a_bytes,
    )

    negative_controls.append(
        expect_failure(
            label="requested_generation_mismatch",
            operation=lambda:
                rollback.rollback_generation(
                    model_pk=model_pk,
                    target_generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                    target_candidate_manifest_path=(
                        candidate_b[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        requested_generation_active
                    ),
                    target_segment_paths=(
                        candidate_b[
                            "segment_paths"
                        ]
                    ),
                ),
            active_path=requested_generation_active,
            expected_active_bytes=(
                active_a_bytes
            ),
        )
    )

    requested_model_active = active_copy(
        name="requested_model_mismatch",
        active_bytes=active_a_bytes,
    )

    negative_controls.append(
        expect_failure(
            label="requested_model_mismatch",
            operation=lambda:
                rollback.rollback_generation(
                    model_pk=OTHER_MODEL_PK,
                    target_generation_pk=(
                        candidate_b[
                            "generation_pk"
                        ]
                    ),
                    target_candidate_manifest_path=(
                        candidate_b[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        requested_model_active
                    ),
                    target_segment_paths=(
                        candidate_b[
                            "segment_paths"
                        ]
                    ),
                ),
            expected_texts=(
                "active model_pk mismatch",
            ),
            active_path=requested_model_active,
            expected_active_bytes=(
                active_a_bytes
            ),
        )
    )

    noncanonical_target = write_manifest_variant(
        name="noncanonical_target",
        base_manifest=(
            candidate_b[
                "manifest"
            ]
        ),
        mutation=lambda value:
            None,
        canonical=False,
    )

    noncanonical_target_active = active_copy(
        name="noncanonical_target_manifest",
        active_bytes=active_a_bytes,
    )

    negative_controls.append(
        expect_failure(
            label="noncanonical_target_manifest",
            operation=lambda:
                rollback.rollback_generation(
                    model_pk=model_pk,
                    target_generation_pk=(
                        candidate_b[
                            "generation_pk"
                        ]
                    ),
                    target_candidate_manifest_path=(
                        noncanonical_target
                    ),
                    active_record_path=(
                        noncanonical_target_active
                    ),
                    target_segment_paths=(
                        candidate_b[
                            "segment_paths"
                        ]
                    ),
                ),
            active_path=noncanonical_target_active,
            expected_active_bytes=(
                active_a_bytes
            ),
        )
    )

    segment_keys = sorted(
        candidate_b[
            "segment_paths"
        ]
    )

    first_segment_id = (
        segment_keys[0]
    )

    missing_mapping = copy_mapping(
        candidate_b[
            "segment_paths"
        ]
    )

    missing_mapping.pop(
        first_segment_id
    )

    missing_mapping_active = active_copy(
        name="missing_target_segment_mapping",
        active_bytes=active_a_bytes,
    )

    negative_controls.append(
        expect_failure(
            label="missing_target_segment_mapping",
            operation=lambda:
                rollback.rollback_generation(
                    model_pk=model_pk,
                    target_generation_pk=(
                        candidate_b[
                            "generation_pk"
                        ]
                    ),
                    target_candidate_manifest_path=(
                        candidate_b[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        missing_mapping_active
                    ),
                    target_segment_paths=(
                        missing_mapping
                    ),
                ),
            active_path=missing_mapping_active,
            expected_active_bytes=(
                active_a_bytes
            ),
        )
    )

    extra_mapping = copy_mapping(
        candidate_b[
            "segment_paths"
        ]
    )

    extra_mapping[
        "segment:rollback-extra"
    ] = candidate_b[
        "segment_paths"
    ][
        first_segment_id
    ]

    extra_mapping_active = active_copy(
        name="extra_target_segment_mapping",
        active_bytes=active_a_bytes,
    )

    negative_controls.append(
        expect_failure(
            label="extra_target_segment_mapping",
            operation=lambda:
                rollback.rollback_generation(
                    model_pk=model_pk,
                    target_generation_pk=(
                        candidate_b[
                            "generation_pk"
                        ]
                    ),
                    target_candidate_manifest_path=(
                        candidate_b[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        extra_mapping_active
                    ),
                    target_segment_paths=(
                        extra_mapping
                    ),
                ),
            active_path=extra_mapping_active,
            expected_active_bytes=(
                active_a_bytes
            ),
        )
    )

    missing_segment_mapping = copy_mapping(
        candidate_b[
            "segment_paths"
        ]
    )

    missing_segment_mapping[
        first_segment_id
    ] = (
        RUNTIME
        / "negative"
        / "missing_segment.mafseg"
    )

    missing_segment_active = active_copy(
        name="missing_mapped_segment",
        active_bytes=active_a_bytes,
    )

    negative_controls.append(
        expect_failure(
            label="missing_mapped_segment",
            operation=lambda:
                rollback.rollback_generation(
                    model_pk=model_pk,
                    target_generation_pk=(
                        candidate_b[
                            "generation_pk"
                        ]
                    ),
                    target_candidate_manifest_path=(
                        candidate_b[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        missing_segment_active
                    ),
                    target_segment_paths=(
                        missing_segment_mapping
                    ),
                ),
            active_path=missing_segment_active,
            expected_active_bytes=(
                active_a_bytes
            ),
        )
    )

    nonregular_dir = (
        RUNTIME
        / "negative"
        / "nonregular_segment"
    )

    nonregular_dir.mkdir(
        parents=True,
        exist_ok=False,
    )

    nonregular_mapping = copy_mapping(
        candidate_b[
            "segment_paths"
        ]
    )

    nonregular_mapping[
        first_segment_id
    ] = nonregular_dir

    nonregular_active = active_copy(
        name="nonregular_mapped_segment",
        active_bytes=active_a_bytes,
    )

    negative_controls.append(
        expect_failure(
            label="nonregular_mapped_segment",
            operation=lambda:
                rollback.rollback_generation(
                    model_pk=model_pk,
                    target_generation_pk=(
                        candidate_b[
                            "generation_pk"
                        ]
                    ),
                    target_candidate_manifest_path=(
                        candidate_b[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        nonregular_active
                    ),
                    target_segment_paths=(
                        nonregular_mapping
                    ),
                ),
            active_path=nonregular_active,
            expected_active_bytes=(
                active_a_bytes
            ),
        )
    )

    original_segment = candidate_b[
        "segment_paths"
    ][
        first_segment_id
    ]

    original_segment_bytes = (
        original_segment.read_bytes()
    )

    short_segment = (
        RUNTIME
        / "negative"
        / "short_segment.mafseg"
    )

    write_bytes_exclusive(
        short_segment,
        original_segment_bytes[
            :-1
        ],
    )

    short_mapping = copy_mapping(
        candidate_b[
            "segment_paths"
        ]
    )

    short_mapping[
        first_segment_id
    ] = short_segment

    short_active = active_copy(
        name="segment_length_mismatch",
        active_bytes=active_a_bytes,
    )

    negative_controls.append(
        expect_failure(
            label="segment_length_mismatch",
            operation=lambda:
                rollback.rollback_generation(
                    model_pk=model_pk,
                    target_generation_pk=(
                        candidate_b[
                            "generation_pk"
                        ]
                    ),
                    target_candidate_manifest_path=(
                        candidate_b[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        short_active
                    ),
                    target_segment_paths=(
                        short_mapping
                    ),
                ),
            expected_texts=(
                "segment length mismatch",
            ),
            active_path=short_active,
            expected_active_bytes=(
                active_a_bytes
            ),
        )
    )

    bad_sha_bytes = bytearray(
        original_segment_bytes
    )

    bad_sha_bytes[
        -1
    ] ^= 1

    bad_sha_segment = (
        RUNTIME
        / "negative"
        / "bad_sha_segment.mafseg"
    )

    write_bytes_exclusive(
        bad_sha_segment,
        bytes(
            bad_sha_bytes
        ),
    )

    bad_sha_mapping = copy_mapping(
        candidate_b[
            "segment_paths"
        ]
    )

    bad_sha_mapping[
        first_segment_id
    ] = bad_sha_segment

    bad_sha_active = active_copy(
        name="segment_sha256_mismatch",
        active_bytes=active_a_bytes,
    )

    negative_controls.append(
        expect_failure(
            label="segment_sha256_mismatch",
            operation=lambda:
                rollback.rollback_generation(
                    model_pk=model_pk,
                    target_generation_pk=(
                        candidate_b[
                            "generation_pk"
                        ]
                    ),
                    target_candidate_manifest_path=(
                        candidate_b[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        bad_sha_active
                    ),
                    target_segment_paths=(
                        bad_sha_mapping
                    ),
                ),
            expected_texts=(
                "segment SHA256 mismatch",
            ),
            active_path=bad_sha_active,
            expected_active_bytes=(
                active_a_bytes
            ),
        )
    )

    negative_controls.append(
        inherited_activation_control(
            activation_result=(
                activation_result
            ),
            label=(
                "object_byte_range_sha256_mismatch"
            ),
        )
    )

    negative_controls.append(
        inherited_activation_control(
            activation_result=(
                activation_result
            ),
            label=(
                "multi_segment_wrong_content_association"
            ),
        )
    )

    negative_controls.append(
        inherited_activation_control(
            activation_result=(
                activation_result
            ),
            label=(
                "synthetic_canonical_without_physical_evidence"
            ),
        )
    )

    same_bad_active = active_copy(
        name="same_generation_invalid_physical",
        active_bytes=active_b_bytes,
    )

    same_bad_before = (
        same_bad_active.read_bytes()
    )

    negative_controls.append(
        expect_failure(
            label="same_generation_invalid_physical_evidence",
            operation=lambda:
                rollback.rollback_generation(
                    model_pk=model_pk,
                    target_generation_pk=(
                        candidate_b[
                            "generation_pk"
                        ]
                    ),
                    target_candidate_manifest_path=(
                        candidate_b[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        same_bad_active
                    ),
                    target_segment_paths=(
                        bad_sha_mapping
                    ),
                ),
            expected_texts=(
                "segment SHA256 mismatch",
            ),
            active_path=same_bad_active,
            expected_active_bytes=(
                same_bad_before
            ),
        )
    )

    fault_active = active_copy(
        name="injected_failure_before_authority_replacement",
        active_bytes=active_a_bytes,
    )

    fault_before = (
        fault_active.read_bytes()
    )

    original_replace = (
        activation.activation_v1.os.replace
    )

    replace_calls = 0

    def injected_replace(
        source,
        destination,
    ):
        nonlocal replace_calls

        replace_calls += 1

        raise RuntimeError(
            "injected rollback pre-authority replacement failure"
        )

    try:
        activation.activation_v1.os.replace = (
            injected_replace
        )

        fault_control = expect_failure(
            label="injected_failure_before_authority_replacement",
            operation=lambda:
                rollback.rollback_generation(
                    model_pk=model_pk,
                    target_generation_pk=(
                        candidate_b[
                            "generation_pk"
                        ]
                    ),
                    target_candidate_manifest_path=(
                        candidate_b[
                            "manifest_path"
                        ]
                    ),
                    active_record_path=(
                        fault_active
                    ),
                    target_segment_paths=(
                        candidate_b[
                            "segment_paths"
                        ]
                    ),
                ),
            expected_error_types=(
                "RuntimeError",
            ),
            expected_texts=(
                "injected rollback pre-authority replacement failure",
            ),
            active_path=fault_active,
            expected_active_bytes=(
                fault_before
            ),
            require_partial_absent=True,
        )

    finally:
        activation.activation_v1.os.replace = (
            original_replace
        )

    negative_controls.append(
        fault_control
    )

    atomicity = {
        "replace_calls":
            replace_calls,

        "prior_active_bytes_preserved":
            fault_active.read_bytes()
            == fault_before,

        "partial_absent":
            not fault_active.with_name(
                fault_active.name
                + ".partial"
            ).exists(),

        "prior_active_reopens":
            activation.reopen_active_generation(
                fault_active
            )
            == active_a_record,
    }

    atomicity[
        "pass"
    ] = (
        atomicity[
            "replace_calls"
        ] == 1
        and atomicity[
            "prior_active_bytes_preserved"
        ]
        and atomicity[
            "partial_absent"
        ]
        and atomicity[
            "prior_active_reopens"
        ]
    )

    source_snapshot_after = snapshot_tree(
        SOURCE_ACTIVATION_RUNTIME
    )

    retained_copy_after = snapshot_tree(
        RUNTIME
        / "candidates"
    )

    retention = {
        "source_activation_runtime_unchanged":
            source_snapshot_after
            == source_snapshot_before,

        "rollback_candidate_copies_unchanged":
            retained_copy_after
            == retained_copy_before,

        "candidate_a_manifest_retained":
            candidate_a[
                "manifest_path"
            ].is_file(),

        "candidate_b_manifest_retained":
            candidate_b[
                "manifest_path"
            ].is_file(),

        "pass":
            (
                source_snapshot_after
                == source_snapshot_before
                and retained_copy_after
                == retained_copy_before
                and candidate_a[
                    "manifest_path"
                ].is_file()
                and candidate_b[
                    "manifest_path"
                ].is_file()
            ),
    }

    static_checks = (
        static_policy_checks()
    )

    positive_pass = all(
        value is True
        or (
            key
            in {
                "source_model_required",
                "source_gguf_required",
            }
            and value is False
        )
        for key, value
        in positive_checks.items()
    )

    negative_pass = all(
        row.get(
            "pass"
        ) is True
        for row
        in negative_controls
    )

    static_pass = all(
        value is True
        for value
        in static_checks.values()
    )

    all_pass = (
        positive_pass
        and negative_pass
        and atomicity[
            "pass"
        ]
        and retention[
            "pass"
        ]
        and static_pass
    )

    return {
        "schema":
            SCHEMA,

        "validation_version":
            VERSION,

        "all_pass":
            all_pass,

        "rollback_validation_executed":
            True,

        "controlled_rollback_performed":
            True,

        "model_pk":
            model_pk,

        "candidate_a_generation_pk":
            candidate_a[
                "generation_pk"
            ],

        "candidate_a_manifest_sha256":
            candidate_a[
                "manifest_sha256"
            ],

        "candidate_b_generation_pk":
            candidate_b[
                "generation_pk"
            ],

        "candidate_b_manifest_sha256":
            candidate_b[
                "manifest_sha256"
            ],

        "positive":
            {
                "pass":
                    positive_pass,
                "checks":
                    positive_checks,
                "active_a_record":
                    active_a_record,
                "active_b_record":
                    active_b_record,
            },

        "negative_controls":
            negative_controls,

        "atomicity":
            atomicity,

        "generation_retention":
            retention,

        "static_policy_checks":
            static_checks,

        "source_activation_result_sha256":
            file_sha256(
                SOURCE_ACTIVATION_RESULT
            ),

        "historical_authority_provenance_created":
            False,

        "source_gguf_required":
            False,

        "generation_deleted":
            False,

        "catalog_engine_selected":
            False,

        "inference_performed":
            False,

        "maf_native_compute_enabled":
            False,

        "resident_pk_directory_implemented":
            False,
    }


def main() -> int:
    if RESULT.exists():
        raise RuntimeError(
            "rollback validation result already exists; "
            "do not reexecute"
        )

    if RESULT_PARTIAL.exists():
        raise RuntimeError(
            "rollback validation result partial already exists; "
            "do not reexecute"
        )

    if RUNTIME.exists():
        raise RuntimeError(
            "rollback validation runtime already exists; "
            "do not reexecute"
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
            "rollback_validation_executed":
                True,
            "controlled_rollback_performed":
                False,
            "harness_error":
                {
                    "error_type":
                        type(
                            exc
                        ).__name__,
                    "error_text":
                        str(
                            exc
                        ),
                },
            "historical_authority_provenance_created":
                False,
            "source_gguf_required":
                False,
            "generation_deleted":
                False,
            "catalog_engine_selected":
                False,
            "inference_performed":
                False,
            "maf_native_compute_enabled":
                False,
            "resident_pk_directory_implemented":
                False,
        }

    persist_result(
        result
    )

    print(
        "="
        * 72
    )
    print(
        " OPENMIND / MAF ROLLBACK V1 VALIDATION"
    )
    print(
        "="
        * 72
    )

    print(
        "schema:",
        result.get(
            "schema"
        ),
    )

    print(
        "all_pass:",
        result.get(
            "all_pass"
        ),
    )

    if "positive" in result:
        print(
            "positive:",
            result[
                "positive"
            ].get(
                "pass"
            ),
        )

    if "negative_controls" in result:
        print(
            "negative controls:",
            all(
                row.get(
                    "pass"
                ) is True
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
            ].get(
                "pass"
            ),
        )

    if "generation_retention" in result:
        print(
            "generation retention:",
            result[
                "generation_retention"
            ].get(
                "pass"
            ),
        )

    if "static_policy_checks" in result:
        print(
            "static policy:",
            all(
                value is True
                for value
                in result[
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
        "historical_authority_provenance_created:",
        result.get(
            "historical_authority_provenance_created"
        ),
    )

    print(
        "result:",
        RESULT,
    )

    return (
        0
        if result.get(
            "all_pass"
        ) is True
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
