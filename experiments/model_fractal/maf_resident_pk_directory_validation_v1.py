#!/usr/bin/env python3

"""Resident PK Directory V1 validation.

This runner is intended to execute exactly once after it has been frozen.

It validates the frozen Resident PK Directory V1 engine against retained,
already-frozen Activation V1.1.1 generation evidence.

The runner creates isolated runtime evidence only when executed.
It does not use a source GGUF.
It does not benchmark.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable

import maf_activation_v1_1 as activation
import maf_generation_engine_v1 as generation
import maf_resident_pk_directory_v1 as directory
import maf_rollback_v1 as rollback


SCHEMA = (
    "openmind.maf_resident_pk_directory_validation.v1"
)

VERSION = (
    "maf_resident_pk_directory_validation_v1"
)

RESULT = Path(
    "experiments/model_fractal/"
    "maf_resident_pk_directory_validation_v1.json"
)

RUNTIME = Path(
    "results/runtime/"
    "maf_resident_pk_directory_validation_v1"
)

SOURCE_ACTIVATION_RESULT = Path(
    "experiments/model_fractal/"
    "maf_activation_validation_v1_1_1.json"
)

SOURCE_ACTIVATION_RUNTIME = Path(
    "results/runtime/"
    "maf_activation_validation_v1_1_1"
)

SOURCE_CANDIDATE_A = (
    SOURCE_ACTIVATION_RUNTIME
    / "candidate_a.manifest.json"
)

SOURCE_CANDIDATE_B = (
    SOURCE_ACTIVATION_RUNTIME
    / "candidate_b.manifest.json"
)

FROZEN_FILES = {
    Path(
        "experiments/model_fractal/"
        "MAF_RESIDENT_PK_DIRECTORY_V1_PROTOCOL.md"
    ):
        (
            "5d053b52963a10285f21a600aa0bb257"
            "b0ad645f12a9a36417cfa6f77a017939"
        ),

    Path(
        "experiments/model_fractal/"
        "maf_resident_pk_directory_v1.py"
    ):
        (
            "4dadac5a1ffe448437718432edeee14a"
            "219a20da5a54956d2884d0b0b1d426b6"
        ),

    Path(
        "experiments/model_fractal/"
        "maf_activation_v1.py"
    ):
        (
            "76d79f90d9bc30118a6dfe0297beacd"
            "9b323aed9f56876881f653a2c01c1f210"
        ),

    Path(
        "experiments/model_fractal/"
        "maf_activation_v1_1.py"
    ):
        (
            "9435ae8dd32656c7350887689d453f3c"
            "b8460887068bfaf06e6f68b5b5b927a1"
        ),

    Path(
        "experiments/model_fractal/"
        "maf_generation_engine_v1.py"
    ):
        (
            "8868c58e98084226dd957391e1a2f4d"
            "1122e886607640ae0be59279f025f1a51"
        ),

    Path(
        "experiments/model_fractal/"
        "maf_rollback_v1.py"
    ):
        (
            "73b02c26f840d59499dd7be86985db6"
            "a3a14720769de1d040f2cad9c78703b79"
        ),

    SOURCE_ACTIVATION_RESULT:
        (
            "586f4a4958aab67972dc06845171ee79"
            "bfe937dfcd731f1f5b3fc594df841ac8"
        ),

    Path(
        "experiments/model_fractal/"
        "maf_rollback_validation_v1.json"
    ):
        (
            "36698287b411b30d1616bc24455435022"
            "a0e13a9e9b35b16e68cdf32300c4a82"
        ),
}

OTHER_MODEL_PK = (
    "mafmodel:v1:"
    + (
        "f"
        * 64
    )
)

OTHER_GENERATION_PK = (
    "mafgen:v1:"
    + (
        "e"
        * 64
    )
)

MISSING_OBJECT_PK = (
    "mafobj:v1:"
    + (
        "0"
        * 64
    )
)

SYNTHETIC_FRAGMENT_PK = (
    "maffrag:v1:"
    + (
        "d"
        * 64
    )
)


def file_sha256(
    path: Path,
) -> str:
    h = hashlib.sha256()

    with path.open(
        "rb"
    ) as f:
        while True:
            chunk = f.read(
                1024
                * 1024
            )

            if not chunk:
                break

            h.update(
                chunk
            )

    return h.hexdigest()


def snapshot_tree(
    root: Path,
) -> dict[
    str,
    tuple[
        int,
        str,
    ],
]:
    rows = {}

    for path in sorted(
        root.rglob("*")
    ):
        if not path.is_file():
            continue

        relative = str(
            path.relative_to(
                root
            )
        )

        rows[
            relative
        ] = (
            path.stat().st_size,
            file_sha256(
                path
            ),
        )

    return rows


def canonical_json_bytes(
    value: Any,
) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(
                ",",
                ":",
            ),
            ensure_ascii=False,
        )
        + "\n"
    ).encode(
        "utf-8"
    )


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


def write_json_exclusive(
    path: Path,
    value: Any,
) -> None:
    write_bytes_exclusive(
        path,
        canonical_json_bytes(
            value
        ),
    )


def assert_frozen_files() -> None:
    for path, expected in (
        FROZEN_FILES.items()
    ):
        if not path.is_file():
            raise RuntimeError(
                "frozen dependency missing: "
                + str(
                    path
                )
            )

        actual = file_sha256(
            path
        )

        if actual != expected:
            raise RuntimeError(
                "frozen dependency SHA256 mismatch: "
                + str(
                    path
                )
            )


def locate_source_segment(
    record: dict[str, Any],
) -> Path:
    matches = []

    for path in sorted(
        SOURCE_ACTIVATION_RUNTIME.rglob(
            "*.mafseg"
        )
    ):
        if not path.is_file():
            continue

        if (
            path.stat().st_size
            != record[
                "segment_length"
            ]
        ):
            continue

        if (
            file_sha256(
                path
            )
            != record[
                "segment_sha256"
            ]
        ):
            continue

        matches.append(
            path
        )

    if not matches:
        raise RuntimeError(
            "source segment not found: "
            + record[
                "segment_id"
            ]
        )

    non_relocated = [
        path
        for path in matches
        if "relocated"
        not in str(
            path
        ).lower()
    ]

    if non_relocated:
        return non_relocated[
            0
        ]

    return matches[
        0
    ]


def copy_candidate(
    *,
    label: str,
    source_manifest_path: Path,
    expected_manifest_sha256: str,
) -> dict[str, Any]:
    source_bytes = (
        source_manifest_path.read_bytes()
    )

    source_sha256 = hashlib.sha256(
        source_bytes
    ).hexdigest()

    if (
        source_sha256
        != expected_manifest_sha256
    ):
        raise RuntimeError(
            "source candidate manifest SHA256 mismatch: "
            + label
        )

    manifest = json.loads(
        source_bytes.decode(
            "utf-8"
        )
    )

    candidate_dir = (
        RUNTIME
        / "candidates"
        / label
    )

    manifest_path = (
        candidate_dir
        / "candidate.manifest.json"
    )

    write_bytes_exclusive(
        manifest_path,
        source_bytes,
    )

    segment_paths = {}

    for index, row in enumerate(
        manifest[
            "descriptor"
        ][
            "segments"
        ]
    ):
        source_segment = (
            locate_source_segment(
                row
            )
        )

        destination = (
            candidate_dir
            / (
                f"segment_{index:08d}.mafseg"
            )
        )

        write_bytes_exclusive(
            destination,
            source_segment.read_bytes(),
        )

        segment_paths[
            row[
                "segment_id"
            ]
        ] = destination

    return {
        "label":
            label,
        "manifest":
            manifest,
        "manifest_path":
            manifest_path,
        "manifest_sha256":
            source_sha256,
        "generation_pk":
            manifest[
                "generation_pk"
            ],
        "segment_paths":
            segment_paths,
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

    manifest_path = (
        target_dir
        / "candidate.manifest.json"
    )

    source_manifest_bytes = (
        candidate[
            "manifest_path"
        ].read_bytes()
    )

    write_bytes_exclusive(
        manifest_path,
        source_manifest_bytes,
    )

    segment_paths = {}

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
        destination = (
            target_dir
            / (
                f"relocated_{index:08d}.mafseg"
            )
        )

        write_bytes_exclusive(
            destination,
            source_path.read_bytes(),
        )

        segment_paths[
            segment_id
        ] = destination

    return {
        "label":
            label,
        "manifest":
            copy.deepcopy(
                candidate[
                    "manifest"
                ]
            ),
        "manifest_path":
            manifest_path,
        "manifest_sha256":
            candidate[
                "manifest_sha256"
            ],
        "generation_pk":
            candidate[
                "generation_pk"
            ],
        "segment_paths":
            segment_paths,
    }


def copy_mapping(
    mapping: dict[
        str,
        Path,
    ],
) -> dict[
    str,
    Path,
]:
    return dict(
        mapping
    )


def entry_projection(
    value: directory.ResidentPKEntry,
) -> tuple[Any, ...]:
    return (
        value.model_pk,
        value.generation_pk,
        value.generation_manifest_sha256,
        value.object_pk,
        value.segment_id,
        value.offset,
        value.length,
        value.object_file_sha256,
        value.payload_sha256,
        value.segment_length,
        value.segment_sha256,
    )


def snapshot_projection(
    snapshot: directory.ResidentPKSnapshot,
) -> dict[
    tuple[
        str,
        str,
        str,
    ],
    tuple[Any, ...],
]:
    return {
        key:
            entry_projection(
                value
            )
        for key, value
        in snapshot.entries.items()
    }


def candidate_snapshot_checks(
    *,
    snapshot: directory.ResidentPKSnapshot,
    candidate: dict[str, Any],
    model_pk: str,
) -> dict[str, bool]:
    descriptor = candidate[
        "manifest"
    ][
        "descriptor"
    ]

    segments = {
        row[
            "segment_id"
        ]:
            row
        for row in descriptor[
            "segments"
        ]
    }

    expected_keys = {
        (
            model_pk,
            directory.OBJECT_PK_KIND,
            row[
                "object_pk"
            ],
        )
        for row in descriptor[
            "objects"
        ]
    }

    mapping_exact = True
    lookup_exact = True

    for row in descriptor[
        "objects"
    ]:
        key = (
            model_pk,
            directory.OBJECT_PK_KIND,
            row[
                "object_pk"
            ],
        )

        entry = snapshot.entries.get(
            key
        )

        if entry is None:
            mapping_exact = False
            lookup_exact = False
            continue

        segment = segments[
            row[
                "segment_id"
            ]
        ]

        expected = {
            "model_pk":
                model_pk,

            "generation_pk":
                candidate[
                    "generation_pk"
                ],

            "generation_manifest_sha256":
                candidate[
                    "manifest_sha256"
                ],

            "object_pk":
                row[
                    "object_pk"
                ],

            "segment_id":
                row[
                    "segment_id"
                ],

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

            "segment_length":
                segment[
                    "segment_length"
                ],

            "segment_sha256":
                segment[
                    "segment_sha256"
                ],

            "segment_path":
                str(
                    candidate[
                        "segment_paths"
                    ][
                        row[
                            "segment_id"
                        ]
                    ]
                ),
        }

        actual = {
            "model_pk":
                entry.model_pk,

            "generation_pk":
                entry.generation_pk,

            "generation_manifest_sha256":
                entry.generation_manifest_sha256,

            "object_pk":
                entry.object_pk,

            "segment_id":
                entry.segment_id,

            "offset":
                entry.offset,

            "length":
                entry.length,

            "object_file_sha256":
                entry.object_file_sha256,

            "payload_sha256":
                entry.payload_sha256,

            "segment_length":
                entry.segment_length,

            "segment_sha256":
                entry.segment_sha256,

            "segment_path":
                entry.segment_path,
        }

        if actual != expected:
            mapping_exact = False

        looked_up = snapshot.lookup(
            model_pk=model_pk,
            pk_kind=(
                directory.OBJECT_PK_KIND
            ),
            logical_pk=(
                row[
                    "object_pk"
                ]
            ),
            expected_generation_pk=(
                candidate[
                    "generation_pk"
                ]
            ),
        )

        if looked_up != entry:
            lookup_exact = False

    return {
        "snapshot_model_exact":
            snapshot.model_pk
            == model_pk,

        "snapshot_generation_exact":
            snapshot.generation_pk
            == candidate[
                "generation_pk"
            ],

        "snapshot_manifest_binding_exact":
            (
                snapshot.generation_manifest_sha256
                == candidate[
                    "manifest_sha256"
                ]
            ),

        "entry_count_exact":
            snapshot.entry_count
            == len(
                descriptor[
                    "objects"
                ]
            ),

        "key_set_exact":
            set(
                snapshot.entries
            )
            == expected_keys,

        "object_mapping_exact":
            mapping_exact,

        "direct_lookup_exact":
            lookup_exact,
    }


def expect_failure(
    *,
    label: str,
    operation: Callable[[], Any],
    expected_types: tuple[
        type[BaseException],
        ...,
    ] = (
        directory.MAFResidentPKDirectoryError,
    ),
    active_path: Path | None = None,
    expected_active_bytes: bytes | None = None,
    owner: directory.ResidentPKDirectory | None = None,
    expected_snapshot: (
        directory.ResidentPKSnapshot
        | None
    ) = None,
) -> dict[str, Any]:
    raised = False
    error_type = None
    error_text = None
    type_match = False

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
        type_match = isinstance(
            exc,
            expected_types,
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

    snapshot_preserved = True

    if (
        owner
        is not None
        and expected_snapshot
        is not None
    ):
        snapshot_preserved = (
            owner.snapshot
            is expected_snapshot
        )

    passed = (
        raised
        and type_match
        and active_preserved
        and snapshot_preserved
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

        "active_preserved":
            active_preserved,

        "snapshot_preserved":
            snapshot_preserved,

        "failed_closed":
            (
                active_preserved
                and snapshot_preserved
            ),
    }


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
    record = copy.deepcopy(
        base_record
    )

    if mutation is not None:
        mutation(
            record
        )

    path = (
        RUNTIME
        / "variants"
        / (
            name
            + ".active.json"
        )
    )

    if canonical:
        raw = (
            activation.activation_v1
            .canonical_json_bytes(
                record
            )
        )

    else:
        raw = (
            json.dumps(
                record,
                indent=2,
                ensure_ascii=False,
            )
            + "\n"
        ).encode(
            "utf-8"
        )

    write_bytes_exclusive(
        path,
        raw,
    )

    return path


def write_manifest_variant(
    *,
    name: str,
    base_candidate: dict[str, Any],
    descriptor_mutation: Callable[
        [dict[str, Any]],
        None,
    ],
    base_active_record: dict[str, Any],
) -> tuple[
    Path,
    Path,
]:
    manifest = copy.deepcopy(
        base_candidate[
            "manifest"
        ]
    )

    descriptor = manifest[
        "descriptor"
    ]

    descriptor_mutation(
        descriptor
    )

    descriptor_bytes = (
        generation.canonical_json_bytes(
            descriptor
        )
    )

    generation_pk = (
        "mafgen:v1:"
        + hashlib.sha256(
            descriptor_bytes
        ).hexdigest()
    )

    manifest[
        "generation_pk"
    ] = generation_pk

    manifest_bytes = (
        generation.canonical_json_bytes(
            manifest
        )
    )

    manifest_path = (
        RUNTIME
        / "variants"
        / (
            name
            + ".manifest.json"
        )
    )

    write_bytes_exclusive(
        manifest_path,
        manifest_bytes,
    )

    active_record = copy.deepcopy(
        base_active_record
    )

    active_record[
        "generation_pk"
    ] = generation_pk

    active_record[
        "generation_manifest_sha256"
    ] = hashlib.sha256(
        manifest_bytes
    ).hexdigest()

    active_path = (
        RUNTIME
        / "variants"
        / (
            name
            + ".active.json"
        )
    )

    write_bytes_exclusive(
        active_path,
        (
            activation.activation_v1
            .canonical_json_bytes(
                active_record
            )
        ),
    )

    return (
        active_path,
        manifest_path,
    )


def static_policy_checks() -> dict[str, bool]:
    engine_path = Path(
        "experiments/model_fractal/"
        "maf_resident_pk_directory_v1.py"
    )

    text = engine_path.read_text()
    tree = ast.parse(
        text
    )

    imports = []

    for node in ast.walk(
        tree
    ):
        if isinstance(
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
                node.module
                or ""
            )

    storage_imports_absent = (
        not any(
            name in {
                "sqlite3",
                "mmap",
                "lmdb",
                "rocksdb",
            }
            for name in imports
        )
    )

    forbidden_calls = {
        "activate_generation",
        "rollback_generation",
        "os.replace",
        "unlink",
        "remove",
        "rmtree",
    }

    operational_calls_absent = True

    for node in ast.walk(
        tree
    ):
        if not isinstance(
            node,
            ast.Call,
        ):
            continue

        name = ast.unparse(
            node.func
        )

        if any(
            item
            in name
            for item in forbidden_calls
        ):
            operational_calls_absent = False

    lookup_methods = []

    for class_node in tree.body:
        if (
            not isinstance(
                class_node,
                ast.ClassDef,
            )
            or class_node.name
            not in {
                "ResidentPKSnapshot",
                "ResidentPKDirectory",
            }
        ):
            continue

        for node in class_node.body:
            if (
                isinstance(
                    node,
                    ast.FunctionDef,
                )
                and node.name
                == "lookup"
            ):
                lookup_methods.append(
                    node
                )

    lookup_count_exact = (
        len(
            lookup_methods
        )
        == 2
    )

    lookup_no_iteration = True
    lookup_no_file_io = True
    lookup_no_validation = True

    for fn in lookup_methods:
        for node in ast.walk(
            fn
        ):
            if isinstance(
                node,
                (
                    ast.For,
                    ast.AsyncFor,
                    ast.While,
                    ast.ListComp,
                    ast.SetComp,
                    ast.DictComp,
                    ast.GeneratorExp,
                ),
            ):
                lookup_no_iteration = False

            if not isinstance(
                node,
                ast.Call,
            ):
                continue

            call_name = ast.unparse(
                node.func
            )

            if any(
                value
                in call_name
                for value in (
                    "read_bytes",
                    "read_text",
                    "open",
                    "rglob",
                    "glob",
                    "iterdir",
                )
            ):
                lookup_no_file_io = False

            if any(
                value
                in call_name
                for value in (
                    "build_snapshot",
                    "_validate_current_candidate",
                    "reopen_active_generation",
                )
            ):
                lookup_no_validation = False

    class_names = {
        node.name
        for node in tree.body
        if isinstance(
            node,
            ast.ClassDef,
        )
    }

    function_names = {
        node.name
        for node in tree.body
        if isinstance(
            node,
            ast.FunctionDef,
        )
    }

    no_segment_reader_surface = (
        not any(
            "segmentreader"
            in name.lower().replace(
                "_",
                ""
            )
            for name in (
                class_names
                | function_names
            )
        )
    )

    return {
        "engine_sha256_exact":
            (
                file_sha256(
                    engine_path
                )
                == FROZEN_FILES[
                    engine_path
                ]
            ),

        "storage_imports_absent":
            storage_imports_absent,

        "authority_or_rollback_writer_absent":
            operational_calls_absent,

        "lookup_method_count_exact":
            lookup_count_exact,

        "lookup_iteration_absent":
            lookup_no_iteration,

        "lookup_file_io_absent":
            lookup_no_file_io,

        "lookup_validation_absent":
            lookup_no_validation,

        "mapping_proxy_present":
            (
                "MappingProxyType"
                in text
            ),

        "object_pk_minimum_scope_present":
            (
                'OBJECT_PK_KIND = "object_pk"'
                in text
            ),

        "source_gguf_dependency_absent":
            (
                ".gguf"
                not in text.lower()
            ),

        "segment_reader_surface_absent":
            no_segment_reader_surface,
    }


def run_validation() -> dict[str, Any]:
    assert_frozen_files()

    activation_result = json.loads(
        SOURCE_ACTIVATION_RESULT.read_text(
            encoding="utf-8"
        )
    )

    if activation_result.get(
        "all_pass"
    ) is not True:
        raise RuntimeError(
            "source Activation V1.1.1 result is not all_pass=true"
        )

    if not SOURCE_ACTIVATION_RUNTIME.is_dir():
        raise RuntimeError(
            "source Activation V1.1.1 runtime missing"
        )

    source_snapshot_before = (
        snapshot_tree(
            SOURCE_ACTIVATION_RUNTIME
        )
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
        source_manifest_path=(
            SOURCE_CANDIDATE_A
        ),
        expected_manifest_sha256=(
            activation_result[
                "candidate_a_manifest_sha256"
            ]
        ),
    )

    candidate_b = copy_candidate(
        label="candidate_b",
        source_manifest_path=(
            SOURCE_CANDIDATE_B
        ),
        expected_manifest_sha256=(
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
            "candidate A generation identity mismatch"
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
            "candidate B generation identity mismatch"
        )

    relocated_a = relocate_candidate(
        label="candidate_a",
        candidate=candidate_a,
    )

    active_path = (
        RUNTIME
        / "active_generation.json"
    )

    activation.activate_generation(
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

    active_a_record = (
        activation.reopen_active_generation(
            active_path
        )
    )

    resident = (
        directory.ResidentPKDirectory()
    )

    snapshot_a = resident.refresh(
        model_pk=model_pk,
        active_record_path=(
            active_path
        ),
        active_candidate_manifest_path=(
            candidate_a[
                "manifest_path"
            ]
        ),
        active_segment_paths=(
            candidate_a[
                "segment_paths"
            ]
        ),
    )

    positive_checks = {}

    for key, value in (
        candidate_snapshot_checks(
            snapshot=snapshot_a,
            candidate=candidate_a,
            model_pk=model_pk,
        ).items()
    ):
        positive_checks[
            "initial_a_"
            + key
        ] = value

    initial_a_projection = (
        snapshot_projection(
            snapshot_a
        )
    )

    relocated_snapshot_a = resident.refresh(
        model_pk=model_pk,
        active_record_path=(
            active_path
        ),
        active_candidate_manifest_path=(
            relocated_a[
                "manifest_path"
            ]
        ),
        active_segment_paths=(
            relocated_a[
                "segment_paths"
            ]
        ),
    )

    for key, value in (
        candidate_snapshot_checks(
            snapshot=(
                relocated_snapshot_a
            ),
            candidate=(
                relocated_a
            ),
            model_pk=model_pk,
        ).items()
    ):
        positive_checks[
            "relocated_a_"
            + key
        ] = value

    positive_checks[
        "relocation_logical_projection_unchanged"
    ] = (
        snapshot_projection(
            relocated_snapshot_a
        )
        == initial_a_projection
    )

    positive_checks[
        "relocation_runtime_paths_changed"
    ] = all(
        relocated_snapshot_a.entries[
            key
        ].segment_path
        != snapshot_a.entries[
            key
        ].segment_path
        for key in snapshot_a.entries
    )

    activation.activate_generation(
        model_pk=model_pk,
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

    active_b_bytes = (
        active_path.read_bytes()
    )

    stale_after_activation = (
        expect_failure(
            label=(
                "stale_snapshot_after_activation"
            ),
            operation=lambda:
                resident.lookup(
                    model_pk=model_pk,
                    pk_kind=(
                        directory.OBJECT_PK_KIND
                    ),
                    logical_pk=next(
                        iter(
                            relocated_snapshot_a
                            .entries
                        )
                    )[
                        2
                    ],
                    expected_generation_pk=(
                        candidate_b[
                            "generation_pk"
                        ]
                    ),
                ),
            expected_types=(
                directory.MAFResidentPKDirectoryStaleSnapshotError,
            ),
            owner=resident,
            expected_snapshot=(
                relocated_snapshot_a
            ),
        )
    )

    snapshot_b = resident.refresh(
        model_pk=model_pk,
        active_record_path=(
            active_path
        ),
        active_candidate_manifest_path=(
            candidate_b[
                "manifest_path"
            ]
        ),
        active_segment_paths=(
            candidate_b[
                "segment_paths"
            ]
        ),
    )

    for key, value in (
        candidate_snapshot_checks(
            snapshot=snapshot_b,
            candidate=candidate_b,
            model_pk=model_pk,
        ).items()
    ):
        positive_checks[
            "active_b_"
            + key
        ] = value

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
        active_record_path=(
            active_path
        ),
        target_segment_paths=(
            candidate_a[
                "segment_paths"
            ]
        ),
    )

    stale_after_rollback = (
        expect_failure(
            label=(
                "stale_snapshot_after_rollback"
            ),
            operation=lambda:
                resident.lookup(
                    model_pk=model_pk,
                    pk_kind=(
                        directory.OBJECT_PK_KIND
                    ),
                    logical_pk=next(
                        iter(
                            snapshot_b.entries
                        )
                    )[
                        2
                    ],
                    expected_generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                ),
            expected_types=(
                directory.MAFResidentPKDirectoryStaleSnapshotError,
            ),
            owner=resident,
            expected_snapshot=(
                snapshot_b
            ),
        )
    )

    restored_snapshot_a = (
        resident.refresh(
            model_pk=model_pk,
            active_record_path=(
                active_path
            ),
            active_candidate_manifest_path=(
                candidate_a[
                    "manifest_path"
                ]
            ),
            active_segment_paths=(
                candidate_a[
                    "segment_paths"
                ]
            ),
        )
    )

    for key, value in (
        candidate_snapshot_checks(
            snapshot=(
                restored_snapshot_a
            ),
            candidate=candidate_a,
            model_pk=model_pk,
        ).items()
    ):
        positive_checks[
            "rollback_a_"
            + key
        ] = value

    positive_checks[
        "rollback_restores_a_logical_projection"
    ] = (
        snapshot_projection(
            restored_snapshot_a
        )
        == initial_a_projection
    )

    negative_controls = []

    negative_controls.append(
        stale_after_activation
    )

    negative_controls.append(
        stale_after_rollback
    )

    missing_active = (
        RUNTIME
        / "negative"
        / "missing_active.json"
    )

    negative_controls.append(
        expect_failure(
            label=(
                "missing_active_authority"
            ),
            operation=lambda:
                directory.build_snapshot(
                    model_pk=model_pk,
                    active_record_path=(
                        missing_active
                    ),
                    active_candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_segment_paths=(
                        candidate_a[
                            "segment_paths"
                        ]
                    ),
                ),
            expected_types=(
                directory.MAFResidentPKDirectoryAuthorityError,
            ),
        )
    )

    malformed_active = (
        RUNTIME
        / "negative"
        / "malformed_active.json"
    )

    write_bytes_exclusive(
        malformed_active,
        b"{",
    )

    negative_controls.append(
        expect_failure(
            label=(
                "malformed_active_authority"
            ),
            operation=lambda:
                directory.build_snapshot(
                    model_pk=model_pk,
                    active_record_path=(
                        malformed_active
                    ),
                    active_candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_segment_paths=(
                        candidate_a[
                            "segment_paths"
                        ]
                    ),
                ),
            expected_types=(
                directory.MAFResidentPKDirectoryAuthorityError,
            ),
            active_path=(
                malformed_active
            ),
            expected_active_bytes=b"{",
        )
    )

    noncanonical_active = (
        write_active_variant(
            name="noncanonical_active",
            base_record=(
                active_a_record
            ),
            canonical=False,
        )
    )

    noncanonical_bytes = (
        noncanonical_active
        .read_bytes()
    )

    negative_controls.append(
        expect_failure(
            label=(
                "noncanonical_active_authority"
            ),
            operation=lambda:
                directory.build_snapshot(
                    model_pk=model_pk,
                    active_record_path=(
                        noncanonical_active
                    ),
                    active_candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_segment_paths=(
                        candidate_a[
                            "segment_paths"
                        ]
                    ),
                ),
            expected_types=(
                directory.MAFResidentPKDirectoryAuthorityError,
            ),
            active_path=(
                noncanonical_active
            ),
            expected_active_bytes=(
                noncanonical_bytes
            ),
        )
    )

    cross_model_active = (
        write_active_variant(
            name="cross_model_active",
            base_record=(
                active_a_record
            ),
            mutation=lambda record:
                record.__setitem__(
                    "model_pk",
                    OTHER_MODEL_PK,
                ),
        )
    )

    cross_model_active_bytes = (
        cross_model_active
        .read_bytes()
    )

    negative_controls.append(
        expect_failure(
            label=(
                "cross_model_active_authority"
            ),
            operation=lambda:
                directory.build_snapshot(
                    model_pk=model_pk,
                    active_record_path=(
                        cross_model_active
                    ),
                    active_candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_segment_paths=(
                        candidate_a[
                            "segment_paths"
                        ]
                    ),
                ),
            expected_types=(
                directory.MAFResidentPKDirectoryCrossModelError,
            ),
            active_path=(
                cross_model_active
            ),
            expected_active_bytes=(
                cross_model_active_bytes
            ),
        )
    )

    hash_mismatch_active = (
        write_active_variant(
            name="manifest_hash_mismatch",
            base_record=(
                active_a_record
            ),
        )
    )

    hash_mismatch_active_bytes = (
        hash_mismatch_active
        .read_bytes()
    )

    negative_controls.append(
        expect_failure(
            label=(
                "manifest_hash_mismatch"
            ),
            operation=lambda:
                directory.build_snapshot(
                    model_pk=model_pk,
                    active_record_path=(
                        hash_mismatch_active
                    ),
                    active_candidate_manifest_path=(
                        candidate_b[
                            "manifest_path"
                        ]
                    ),
                    active_segment_paths=(
                        candidate_b[
                            "segment_paths"
                        ]
                    ),
                ),
            expected_types=(
                directory.MAFResidentPKDirectoryActiveGenerationMismatch,
            ),
            active_path=(
                hash_mismatch_active
            ),
            expected_active_bytes=(
                hash_mismatch_active_bytes
            ),
        )
    )

    generation_mismatch_active = (
        write_active_variant(
            name="active_generation_mismatch",
            base_record=(
                active_a_record
            ),
            mutation=lambda record:
                record.__setitem__(
                    "generation_pk",
                    OTHER_GENERATION_PK,
                ),
        )
    )

    generation_mismatch_bytes = (
        generation_mismatch_active
        .read_bytes()
    )

    negative_controls.append(
        expect_failure(
            label=(
                "active_generation_mismatch"
            ),
            operation=lambda:
                directory.build_snapshot(
                    model_pk=model_pk,
                    active_record_path=(
                        generation_mismatch_active
                    ),
                    active_candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_segment_paths=(
                        candidate_a[
                            "segment_paths"
                        ]
                    ),
                ),
            expected_types=(
                directory.MAFResidentPKDirectoryPhysicalEvidenceError,
            ),
            active_path=(
                generation_mismatch_active
            ),
            expected_active_bytes=(
                generation_mismatch_bytes
            ),
        )
    )

    malformed_manifest = (
        RUNTIME
        / "negative"
        / "malformed_candidate.manifest.json"
    )

    malformed_manifest_bytes = b"{"

    write_bytes_exclusive(
        malformed_manifest,
        malformed_manifest_bytes,
    )

    malformed_manifest_active = (
        write_active_variant(
            name="malformed_candidate_manifest",
            base_record=(
                active_a_record
            ),
            mutation=lambda record:
                record.__setitem__(
                    "generation_manifest_sha256",
                    hashlib.sha256(
                        malformed_manifest_bytes
                    ).hexdigest(),
                ),
        )
    )

    malformed_manifest_active_bytes = (
        malformed_manifest_active
        .read_bytes()
    )

    negative_controls.append(
        expect_failure(
            label=(
                "malformed_active_candidate_manifest"
            ),
            operation=lambda:
                directory.build_snapshot(
                    model_pk=model_pk,
                    active_record_path=(
                        malformed_manifest_active
                    ),
                    active_candidate_manifest_path=(
                        malformed_manifest
                    ),
                    active_segment_paths=(
                        candidate_a[
                            "segment_paths"
                        ]
                    ),
                ),
            expected_types=(
                directory.MAFResidentPKDirectoryPhysicalEvidenceError,
            ),
            active_path=(
                malformed_manifest_active
            ),
            expected_active_bytes=(
                malformed_manifest_active_bytes
            ),
        )
    )

    segment_ids = sorted(
        candidate_a[
            "segment_paths"
        ]
    )

    first_segment_id = (
        segment_ids[
            0
        ]
    )

    missing_mapping = copy_mapping(
        candidate_a[
            "segment_paths"
        ]
    )

    missing_mapping.pop(
        first_segment_id
    )

    missing_mapping_active = (
        write_active_variant(
            name="missing_segment_mapping",
            base_record=(
                active_a_record
            ),
        )
    )

    missing_mapping_active_bytes = (
        missing_mapping_active
        .read_bytes()
    )

    negative_controls.append(
        expect_failure(
            label=(
                "missing_segment_mapping"
            ),
            operation=lambda:
                directory.build_snapshot(
                    model_pk=model_pk,
                    active_record_path=(
                        missing_mapping_active
                    ),
                    active_candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_segment_paths=(
                        missing_mapping
                    ),
                ),
            expected_types=(
                directory.MAFResidentPKDirectoryPhysicalEvidenceError,
            ),
            active_path=(
                missing_mapping_active
            ),
            expected_active_bytes=(
                missing_mapping_active_bytes
            ),
        )
    )

    extra_mapping = copy_mapping(
        candidate_a[
            "segment_paths"
        ]
    )

    extra_mapping[
        "segment:resident-extra"
    ] = candidate_a[
        "segment_paths"
    ][
        first_segment_id
    ]

    extra_mapping_active = (
        write_active_variant(
            name="extra_segment_mapping",
            base_record=(
                active_a_record
            ),
        )
    )

    extra_mapping_active_bytes = (
        extra_mapping_active
        .read_bytes()
    )

    negative_controls.append(
        expect_failure(
            label=(
                "extra_segment_mapping"
            ),
            operation=lambda:
                directory.build_snapshot(
                    model_pk=model_pk,
                    active_record_path=(
                        extra_mapping_active
                    ),
                    active_candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_segment_paths=(
                        extra_mapping
                    ),
                ),
            expected_types=(
                directory.MAFResidentPKDirectoryPhysicalEvidenceError,
            ),
            active_path=(
                extra_mapping_active
            ),
            expected_active_bytes=(
                extra_mapping_active_bytes
            ),
        )
    )

    missing_physical_mapping = (
        copy_mapping(
            candidate_a[
                "segment_paths"
            ]
        )
    )

    missing_physical_mapping[
        first_segment_id
    ] = (
        RUNTIME
        / "negative"
        / "missing_segment.mafseg"
    )

    missing_physical_active = (
        write_active_variant(
            name="missing_physical_segment",
            base_record=(
                active_a_record
            ),
        )
    )

    missing_physical_active_bytes = (
        missing_physical_active
        .read_bytes()
    )

    negative_controls.append(
        expect_failure(
            label=(
                "missing_physical_segment"
            ),
            operation=lambda:
                directory.build_snapshot(
                    model_pk=model_pk,
                    active_record_path=(
                        missing_physical_active
                    ),
                    active_candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_segment_paths=(
                        missing_physical_mapping
                    ),
                ),
            expected_types=(
                directory.MAFResidentPKDirectoryPhysicalEvidenceError,
            ),
            active_path=(
                missing_physical_active
            ),
            expected_active_bytes=(
                missing_physical_active_bytes
            ),
        )
    )

    nonregular_path = (
        RUNTIME
        / "negative"
        / "nonregular_segment"
    )

    nonregular_path.mkdir(
        parents=True,
        exist_ok=False,
    )

    nonregular_mapping = copy_mapping(
        candidate_a[
            "segment_paths"
        ]
    )

    nonregular_mapping[
        first_segment_id
    ] = nonregular_path

    nonregular_active = (
        write_active_variant(
            name="nonregular_physical_segment",
            base_record=(
                active_a_record
            ),
        )
    )

    nonregular_active_bytes = (
        nonregular_active
        .read_bytes()
    )

    negative_controls.append(
        expect_failure(
            label=(
                "nonregular_physical_segment"
            ),
            operation=lambda:
                directory.build_snapshot(
                    model_pk=model_pk,
                    active_record_path=(
                        nonregular_active
                    ),
                    active_candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_segment_paths=(
                        nonregular_mapping
                    ),
                ),
            expected_types=(
                directory.MAFResidentPKDirectoryPhysicalEvidenceError,
            ),
            active_path=(
                nonregular_active
            ),
            expected_active_bytes=(
                nonregular_active_bytes
            ),
        )
    )

    original_segment = (
        candidate_a[
            "segment_paths"
        ][
            first_segment_id
        ]
    )

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
        candidate_a[
            "segment_paths"
        ]
    )

    short_mapping[
        first_segment_id
    ] = short_segment

    short_active = (
        write_active_variant(
            name="segment_length_mismatch",
            base_record=(
                active_a_record
            ),
        )
    )

    short_active_bytes = (
        short_active.read_bytes()
    )

    negative_controls.append(
        expect_failure(
            label=(
                "segment_length_mismatch"
            ),
            operation=lambda:
                directory.build_snapshot(
                    model_pk=model_pk,
                    active_record_path=(
                        short_active
                    ),
                    active_candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_segment_paths=(
                        short_mapping
                    ),
                ),
            expected_types=(
                directory.MAFResidentPKDirectoryPhysicalEvidenceError,
            ),
            active_path=(
                short_active
            ),
            expected_active_bytes=(
                short_active_bytes
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
        candidate_a[
            "segment_paths"
        ]
    )

    bad_sha_mapping[
        first_segment_id
    ] = bad_sha_segment

    bad_sha_active = (
        write_active_variant(
            name="segment_sha256_mismatch",
            base_record=(
                active_a_record
            ),
        )
    )

    bad_sha_active_bytes = (
        bad_sha_active.read_bytes()
    )

    negative_controls.append(
        expect_failure(
            label=(
                "segment_sha256_mismatch"
            ),
            operation=lambda:
                directory.build_snapshot(
                    model_pk=model_pk,
                    active_record_path=(
                        bad_sha_active
                    ),
                    active_candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_segment_paths=(
                        bad_sha_mapping
                    ),
                ),
            expected_types=(
                directory.MAFResidentPKDirectoryPhysicalEvidenceError,
            ),
            active_path=(
                bad_sha_active
            ),
            expected_active_bytes=(
                bad_sha_active_bytes
            ),
        )
    )

    (
        object_range_active,
        object_range_manifest,
    ) = write_manifest_variant(
        name=(
            "object_byte_range_sha256_mismatch"
        ),
        base_candidate=(
            candidate_a
        ),
        base_active_record=(
            active_a_record
        ),
        descriptor_mutation=lambda descriptor:
            descriptor[
                "objects"
            ][
                0
            ].__setitem__(
                "object_file_sha256",
                "0"
                * 64,
            ),
    )

    object_range_active_bytes = (
        object_range_active
        .read_bytes()
    )

    negative_controls.append(
        expect_failure(
            label=(
                "object_byte_range_sha256_mismatch"
            ),
            operation=lambda:
                directory.build_snapshot(
                    model_pk=model_pk,
                    active_record_path=(
                        object_range_active
                    ),
                    active_candidate_manifest_path=(
                        object_range_manifest
                    ),
                    active_segment_paths=(
                        candidate_a[
                            "segment_paths"
                        ]
                    ),
                ),
            expected_types=(
                directory.MAFResidentPKDirectoryPhysicalEvidenceError,
            ),
            active_path=(
                object_range_active
            ),
            expected_active_bytes=(
                object_range_active_bytes
            ),
        )
    )

    (
        duplicate_active,
        duplicate_manifest,
    ) = write_manifest_variant(
        name=(
            "duplicate_object_pk_conflict"
        ),
        base_candidate=(
            candidate_a
        ),
        base_active_record=(
            active_a_record
        ),
        descriptor_mutation=lambda descriptor:
            descriptor[
                "objects"
            ].append(
                copy.deepcopy(
                    descriptor[
                        "objects"
                    ][
                        0
                    ]
                )
            ),
    )

    duplicate_active_bytes = (
        duplicate_active.read_bytes()
    )

    negative_controls.append(
        expect_failure(
            label=(
                "duplicate_object_pk_conflict"
            ),
            operation=lambda:
                directory.build_snapshot(
                    model_pk=model_pk,
                    active_record_path=(
                        duplicate_active
                    ),
                    active_candidate_manifest_path=(
                        duplicate_manifest
                    ),
                    active_segment_paths=(
                        candidate_a[
                            "segment_paths"
                        ]
                    ),
                ),
            expected_types=(
                directory.MAFResidentPKDirectoryPhysicalEvidenceError,
                directory.MAFResidentPKDirectoryDuplicatePKError,
            ),
            active_path=(
                duplicate_active
            ),
            expected_active_bytes=(
                duplicate_active_bytes
            ),
        )
    )

    negative_controls.append(
        expect_failure(
            label=(
                "missing_object_pk_lookup"
            ),
            operation=lambda:
                resident.lookup(
                    model_pk=model_pk,
                    pk_kind=(
                        directory.OBJECT_PK_KIND
                    ),
                    logical_pk=(
                        MISSING_OBJECT_PK
                    ),
                    expected_generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                ),
            expected_types=(
                directory.MAFResidentPKDirectoryNotFoundError,
            ),
            owner=resident,
            expected_snapshot=(
                restored_snapshot_a
            ),
        )
    )

    first_object_pk = next(
        iter(
            restored_snapshot_a
            .entries
        )
    )[
        2
    ]

    negative_controls.append(
        expect_failure(
            label=(
                "unsupported_pk_class"
            ),
            operation=lambda:
                resident.lookup(
                    model_pk=model_pk,
                    pk_kind="fragment_pk",
                    logical_pk=(
                        first_object_pk
                    ),
                    expected_generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                ),
            expected_types=(
                directory.MAFResidentPKDirectoryUnsupportedPKError,
            ),
            owner=resident,
            expected_snapshot=(
                restored_snapshot_a
            ),
        )
    )

    negative_controls.append(
        expect_failure(
            label=(
                "cross_model_lookup"
            ),
            operation=lambda:
                resident.lookup(
                    model_pk=(
                        OTHER_MODEL_PK
                    ),
                    pk_kind=(
                        directory.OBJECT_PK_KIND
                    ),
                    logical_pk=(
                        first_object_pk
                    ),
                    expected_generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                ),
            expected_types=(
                directory.MAFResidentPKDirectoryCrossModelError,
            ),
            owner=resident,
            expected_snapshot=(
                restored_snapshot_a
            ),
        )
    )

    negative_controls.append(
        expect_failure(
            label=(
                "attempted_synthetic_pk_creation_rejected"
            ),
            operation=lambda:
                resident.lookup(
                    model_pk=model_pk,
                    pk_kind="fragment_pk",
                    logical_pk=(
                        SYNTHETIC_FRAGMENT_PK
                    ),
                    expected_generation_pk=(
                        candidate_a[
                            "generation_pk"
                        ]
                    ),
                ),
            expected_types=(
                directory.MAFResidentPKDirectoryUnsupportedPKError,
            ),
            owner=resident,
            expected_snapshot=(
                restored_snapshot_a
            ),
        )
    )

    prior_snapshot = (
        resident.snapshot
    )

    negative_controls.append(
        expect_failure(
            label=(
                "failed_refresh_preserving_prior_snapshot"
            ),
            operation=lambda:
                resident.refresh(
                    model_pk=model_pk,
                    active_record_path=(
                        active_path
                    ),
                    active_candidate_manifest_path=(
                        candidate_a[
                            "manifest_path"
                        ]
                    ),
                    active_segment_paths=(
                        bad_sha_mapping
                    ),
                ),
            expected_types=(
                directory.MAFResidentPKDirectoryPhysicalEvidenceError,
            ),
            active_path=(
                active_path
            ),
            expected_active_bytes=(
                active_a_bytes
            ),
            owner=resident,
            expected_snapshot=(
                prior_snapshot
            ),
        )
    )

    positive_checks[
        "same_generation_invalid_physical_rejected"
    ] = (
        negative_controls[
            -1
        ][
            "pass"
        ]
        is True
    )

    same_generation_refresh = (
        resident.refresh(
            model_pk=model_pk,
            active_record_path=(
                active_path
            ),
            active_candidate_manifest_path=(
                candidate_a[
                    "manifest_path"
                ]
            ),
            active_segment_paths=(
                candidate_a[
                    "segment_paths"
                ]
            ),
        )
    )

    positive_checks[
        "same_generation_good_refresh_succeeds"
    ] = (
        snapshot_projection(
            same_generation_refresh
        )
        == initial_a_projection
    )

    positive_checks[
        "active_a_authority_restored_exactly"
    ] = (
        active_path.read_bytes()
        == active_a_bytes
    )

    positive_checks[
        "activation_b_changed_authority_bytes"
    ] = (
        active_b_bytes
        != active_a_bytes
    )

    static_checks = (
        static_policy_checks()
    )

    source_snapshot_after = (
        snapshot_tree(
            SOURCE_ACTIVATION_RUNTIME
        )
    )

    source_runtime_unchanged = (
        source_snapshot_after
        == source_snapshot_before
    )

    positive_checks[
        "source_activation_runtime_unchanged"
    ] = (
        source_runtime_unchanged
    )

    positive_pass = all(
        value is True
        for value in positive_checks.values()
    )

    negative_pass = (
        len(
            negative_controls
        )
        == 22
        and all(
            row.get(
                "pass"
            )
            is True
            for row in negative_controls
        )
    )

    static_pass = (
        bool(
            static_checks
        )
        and all(
            value is True
            for value in static_checks.values()
        )
    )

    all_pass = (
        positive_pass
        and negative_pass
        and static_pass
        and source_runtime_unchanged
    )

    return {
        "schema":
            SCHEMA,

        "validation_version":
            VERSION,

        "all_pass":
            all_pass,

        "resident_pk_directory_validation_executed":
            True,

        "controlled_activation_performed":
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
            },

        "negative_controls":
            negative_controls,

        "static_policy_checks":
            static_checks,

        "source_activation_runtime_unchanged":
            source_runtime_unchanged,

        "source_activation_result_sha256":
            file_sha256(
                SOURCE_ACTIVATION_RESULT
            ),

        "resident_directory_engine_sha256":
            file_sha256(
                Path(
                    "experiments/model_fractal/"
                    "maf_resident_pk_directory_v1.py"
                )
            ),

        "source_gguf_required":
            False,

        "generation_deleted":
            False,

        "storage_engine_selected":
            False,

        "segment_reader_implemented":
            False,

        "inference_performed":
            False,

        "maf_native_compute_enabled":
            False,

        "benchmark_performed":
            False,

        "production_performance_claimed":
            False,

        "phase_6c_started":
            False,
    }


def main() -> None:
    if RESULT.exists():
        raise RuntimeError(
            "refusing rerun: validation result already exists"
        )

    if RUNTIME.exists():
        raise RuntimeError(
            "refusing rerun: validation runtime already exists"
        )

    result = run_validation()

    write_json_exclusive(
        RESULT,
        result,
    )

    print(
        "="
        * 72
    )
    print(
        " OPENMIND / RESIDENT PK DIRECTORY VALIDATION V1"
    )
    print(
        "="
        * 72
    )
    print(
        "all_pass:",
        result[
            "all_pass"
        ],
    )
    print(
        "negative_controls:",
        sum(
            1
            for row in result[
                "negative_controls"
            ]
            if row.get(
                "pass"
            )
            is True
        ),
        "/",
        len(
            result[
                "negative_controls"
            ]
        ),
    )
    print(
        "benchmark_performed:",
        result[
            "benchmark_performed"
        ],
    )
    print(
        "result:",
        RESULT,
    )
    print(
        "runtime:",
        RUNTIME,
    )


if __name__ == "__main__":
    main()
