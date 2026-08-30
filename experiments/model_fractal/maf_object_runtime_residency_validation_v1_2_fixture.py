#!/usr/bin/env python3
"""Exact-once Phase 6C V1.2 four-object authority fixture constructor.

This file is inert until explicitly invoked as a script.

Its construction protocol must be frozen before this builder is frozen.
After this builder is frozen, a separate no-write preflight is required
before the first and only authorized construction invocation.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import os
from pathlib import Path
from typing import Any


SCHEMA = (
    "openmind.maf_object_runtime_residency_validation.v1.2.fixture"
)

FIXTURE_VERSION = "v1.2"

PROTOCOL_PATH = Path(
    "experiments/model_fractal/"
    "MAF_OBJECT_RUNTIME_RESIDENCY_VALIDATION_V1_2_FIXTURE_PROTOCOL.md"
)

PROTOCOL_SHA256 = (
    "da86e2c86967c64865010bea45846237baa6a9b877f560bdb9201e52d1723a31"
)

BUILDER_PATH = Path(
    "experiments/model_fractal/"
    "maf_object_runtime_residency_validation_v1_2_fixture.py"
)

RESULT_PATH = Path(
    "experiments/model_fractal/"
    "maf_object_runtime_residency_validation_v1_2_fixture.json"
)

FIXTURE_ROOT = Path(
    "results/runtime/"
    "maf_object_runtime_residency_validation_v1_2_fixture"
)

SEGMENT_PATH = (
    FIXTURE_ROOT
    / "segment_00000000.mafseg"
)

MANIFEST_PATH = (
    FIXTURE_ROOT
    / "candidate_a.manifest.json"
)

ACTIVE_PATH = (
    FIXTURE_ROOT
    / "active_generation.json"
)

ACTIVE_PARTIAL_PATH = (
    FIXTURE_ROOT
    / "active_generation.json.partial"
)

V12_PROTOCOL = Path(
    "experiments/model_fractal/"
    "MAF_OBJECT_RUNTIME_RESIDENCY_VALIDATION_V1_2_PROTOCOL.md"
)

V12_RUNNER = Path(
    "experiments/model_fractal/"
    "maf_object_runtime_residency_validation_v1_2.py"
)

V12_RESULT = Path(
    "experiments/model_fractal/"
    "maf_object_runtime_residency_validation_v1_2.json"
)

V12_RUNTIME = Path(
    "results/runtime/"
    "maf_object_runtime_residency_validation_v1_2"
)

MODEL_PK = (
    "mafmodel:v1:"
    "b3d13be495d56e4fa7bafe145bf4efdc3b5dc13596446252d45f8adadd340a1b"
)

SEGMENT_LENGTH = 4096

SEGMENT_SHA256 = (
    "f965b526538d757ca2d6114af6517c57"
    "cbcb3650b71d8cfb92046a04ef2f566b"
)

EXPECTED_SEGMENT_ID = "segment:00000000"

PROTECTED_BYTE_INDEX = 3500

ACTIVE_SCHEMA = "openmind.maf_active_generation.v1"
ACTIVE_VERSION = "maf_active_generation_v1"

FROZEN_DEPENDENCIES = {
    "generation": {
        "path":
            "experiments/model_fractal/maf_generation_engine_v1.py",
        "sha256":
            "8868c58e98084226dd957391e1a2f4d1122e886607640ae0be59279f025f1a51",
    },
    "activation_wrapper": {
        "path":
            "experiments/model_fractal/maf_activation_v1_1.py",
        "sha256":
            "9435ae8dd32656c7350887689d453f3cb8460887068bfaf06e6f68b5b5b927a1",
    },
    "activation_base": {
        "path":
            "experiments/model_fractal/maf_activation_v1.py",
        "sha256":
            "76d79f90d9bc30118a6dfe0297beacd9b323aed9f56876881f653a2c01c1f210",
    },
    "activation_validation": {
        "path":
            "experiments/model_fractal/maf_activation_validation_v1_1.py",
        "sha256":
            "b6457a3f9e9cdf971b6d92f4531c4484790146b1fcc4f4f10f20280f60c9f664",
    },
    "runtime_engine": {
        "path":
            "experiments/model_fractal/maf_object_runtime_residency_v1.py",
        "sha256":
            "4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9",
    },
    "resident_directory": {
        "path":
            "experiments/model_fractal/maf_resident_pk_directory_v1.py",
        "sha256":
            "4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6",
    },
    "segment_reader": {
        "path":
            "experiments/model_fractal/maf_segment_reader_v1.py",
        "sha256":
            "3499cb8e528fe8e9315e3e5656d6aa888c95ca175310b6371e722de409827369",
    },
    "v1_1_protocol": {
        "path":
            "experiments/model_fractal/"
            "MAF_OBJECT_RUNTIME_RESIDENCY_VALIDATION_V1_1_PROTOCOL.md",
        "sha256":
            "e93ea0f418fc25a01573aad6d23b8d3f999be73b932828596b47ed6548128681",
    },
    "v1_1_runner": {
        "path":
            "experiments/model_fractal/"
            "maf_object_runtime_residency_validation_v1_1.py",
        "sha256":
            "87fc8a01cde4f90afd4b45cb799c2a9c52573db410e365ac620f30092803c029",
    },
    "v1_1_result": {
        "path":
            "experiments/model_fractal/"
            "maf_object_runtime_residency_validation_v1_1.json",
        "sha256":
            "18204da5e5c50af29a1a5f67a26288a6aec48bf35c2d09b5415c82f0113ad778",
    },
}

OBJECT_SPECS = (
    {
        "label": "A",
        "object_pk":
            "mafobj:v1:"
            "ea258c628d783a1e140430a6bbde438f97f0be7d85e5f218ee149ad3b1fb2815",
        "offset": 64,
        "length": 512,
        "object_file_sha256":
            "f9849113558b125c1cfa52b62e5625d362300ff2d9897ca8bb7143dd4473f611",
        "payload_sha256":
            "f9849113558b125c1cfa52b62e5625d362300ff2d9897ca8bb7143dd4473f611",
    },
    {
        "label": "B",
        "object_pk":
            "mafobj:v1:"
            "ecec2d8fcca3888752e67802867631919dbfeb2bafbd137b45441a068f346deb",
        "offset": 1024,
        "length": 640,
        "object_file_sha256":
            "4e492d3bdc486105115cb3c1ffa07b688385f88fe23dc7881acd3f0bd00585e4",
        "payload_sha256":
            "4e492d3bdc486105115cb3c1ffa07b688385f88fe23dc7881acd3f0bd00585e4",
    },
    {
        "label": "C",
        "object_pk":
            "mafobj:v1:"
            "cc2c9d0c6eab228cadf17888746a3d432ed6e361c4a59678a5015f80d65c24ba",
        "offset": 1792,
        "length": 768,
        "object_file_sha256":
            "d1031a4a74d6d775c24a8cc0a29760ed01e97254eaab4c845323dc2ed15eac1f",
        "payload_sha256":
            "d1031a4a74d6d775c24a8cc0a29760ed01e97254eaab4c845323dc2ed15eac1f",
    },
    {
        "label": "D",
        "object_pk":
            "mafobj:v1:"
            "b68292655c246c99a9c1796dcaa4f12dbaa1e6fc668d44d9e6890bce38084b93",
        "offset": 2688,
        "length": 800,
        "object_file_sha256":
            "5b300021bebaa7ccdaed30c058cae6511533fad0101892fda2017bef69931a79",
        "payload_sha256":
            "5b300021bebaa7ccdaed30c058cae6511533fad0101892fda2017bef69931a79",
    },
)


class FixtureConstructionError(RuntimeError):
    pass


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(8 * 1024 * 1024),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()


def bytes_sha256(payload: bytes) -> str:
    return hashlib.sha256(
        payload
    ).hexdigest()


def canonical_json_bytes(
    value: Any,
) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def write_bytes_exclusive(
    path: Path,
    payload: bytes,
) -> None:
    path = Path(path)

    with path.open("xb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())


def write_result_exclusive(
    result: dict[str, Any],
) -> None:
    payload = canonical_json_bytes(
        result
    )

    write_bytes_exclusive(
        RESULT_PATH,
        payload,
    )


def deterministic_segment_bytes() -> bytes:
    return bytes(
        (
            (
                index * 73
                + 19
            )
            % 256
        )
        for index in range(
            SEGMENT_LENGTH
        )
    )


def require(
    checks: dict[str, bool],
    name: str,
    condition: bool,
    message: str,
) -> None:
    passed = bool(condition)
    checks[name] = passed

    if not passed:
        raise FixtureConstructionError(
            message
        )


def object_result_rows() -> list[dict[str, Any]]:
    return [
        {
            "label": row["label"],
            "object_pk": row["object_pk"],
            "offset": row["offset"],
            "length": row["length"],
            "object_file_sha256":
                row["object_file_sha256"],
            "payload_sha256":
                row["payload_sha256"],
        }
        for row in OBJECT_SPECS
    ]


def base_result(
    *,
    builder_sha256: str,
) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "fixture_version":
            FIXTURE_VERSION,
        "protocol_path":
            str(PROTOCOL_PATH),
        "protocol_sha256":
            PROTOCOL_SHA256,
        "builder_path":
            str(BUILDER_PATH),
        "builder_sha256":
            builder_sha256,
        "frozen_dependencies":
            FROZEN_DEPENDENCIES,
        "fixture_root":
            str(FIXTURE_ROOT),
        "model_pk":
            MODEL_PK,
        "generation_pk":
            None,
        "generation_manifest_sha256":
            None,
        "segment_sha256":
            None,
        "fixture_entry_count":
            0,
        "positive_length_entry_count":
            0,
        "objects":
            object_result_rows(),
        "checks":
            {},
        "failed_checks":
            [],
        "construction_valid":
            False,
        "all_pass":
            False,
        "fatal":
            None,
    }


def run_construction() -> int:
    builder_sha256 = file_sha256(
        Path(__file__)
    )

    result = base_result(
        builder_sha256=builder_sha256,
    )

    checks: dict[str, bool] = {}
    fatal: dict[str, str] | None = None

    generation_pk: str | None = None
    manifest_sha256: str | None = None
    actual_segment_sha256: str | None = None
    fixture_entry_count = 0
    positive_length_entry_count = 0

    try:
        require(
            checks,
            "result_path_absent",
            not RESULT_PATH.exists(),
            "fixture construction result already exists",
        )

        require(
            checks,
            "fixture_root_absent",
            not FIXTURE_ROOT.exists(),
            "dedicated fixture root already exists",
        )

        for label, path in (
            ("v1_2_protocol", V12_PROTOCOL),
            ("v1_2_runner", V12_RUNNER),
            ("v1_2_result", V12_RESULT),
            ("v1_2_runtime", V12_RUNTIME),
        ):
            require(
                checks,
                label + "_absent",
                not path.exists(),
                label + " already exists",
            )

        require(
            checks,
            "protocol_present",
            PROTOCOL_PATH.is_file(),
            "fixture construction protocol missing",
        )

        require(
            checks,
            "protocol_sha256_exact",
            file_sha256(
                PROTOCOL_PATH
            )
            == PROTOCOL_SHA256,
            "fixture construction protocol SHA256 mismatch",
        )

        for name, spec in (
            FROZEN_DEPENDENCIES.items()
        ):
            path = Path(
                spec["path"]
            )

            require(
                checks,
                "dependency_"
                + name
                + "_present",
                path.is_file(),
                "frozen dependency missing: "
                + name,
            )

            require(
                checks,
                "dependency_"
                + name
                + "_sha256_exact",
                file_sha256(path)
                == spec["sha256"],
                "frozen dependency SHA256 mismatch: "
                + name,
            )

        generation = importlib.import_module(
            "maf_generation_engine_v1"
        )

        activation = importlib.import_module(
            "maf_activation_v1_1"
        )

        segment_bytes = (
            deterministic_segment_bytes()
        )

        require(
            checks,
            "segment_length_exact",
            len(segment_bytes)
            == SEGMENT_LENGTH,
            "deterministic segment length mismatch",
        )

        actual_segment_sha256 = (
            bytes_sha256(
                segment_bytes
            )
        )

        require(
            checks,
            "segment_sha256_exact",
            actual_segment_sha256
            == SEGMENT_SHA256,
            "deterministic segment SHA256 mismatch",
        )

        require(
            checks,
            "object_count_exact",
            len(OBJECT_SPECS) == 4,
            "fixture requires exactly four objects",
        )

        object_pks = [
            row["object_pk"]
            for row in OBJECT_SPECS
        ]

        require(
            checks,
            "object_pks_distinct",
            len(set(object_pks))
            == 4,
            "fixture object PKs are not distinct",
        )

        for row in OBJECT_SPECS:
            offset = int(
                row["offset"]
            )

            length = int(
                row["length"]
            )

            end = (
                offset
                + length
            )

            require(
                checks,
                "object_"
                + row["label"]
                + "_offset_nonnegative",
                offset >= 0,
                "negative object offset",
            )

            require(
                checks,
                "object_"
                + row["label"]
                + "_length_positive",
                length > 0,
                "nonpositive object length",
            )

            require(
                checks,
                "object_"
                + row["label"]
                + "_range_in_segment",
                end
                <= SEGMENT_LENGTH,
                "object range outside segment",
            )

            payload = (
                segment_bytes[
                    offset:end
                ]
            )

            actual_hash = (
                bytes_sha256(
                    payload
                )
            )

            require(
                checks,
                "object_"
                + row["label"]
                + "_range_sha256_exact",
                actual_hash
                == row[
                    "object_file_sha256"
                ],
                "object byte-range SHA256 mismatch",
            )

            require(
                checks,
                "object_"
                + row["label"]
                + "_payload_sha256_exact",
                row[
                    "payload_sha256"
                ]
                == row[
                    "object_file_sha256"
                ],
                "fixture payload SHA256 rule mismatch",
            )

            require(
                checks,
                "object_"
                + row["label"]
                + "_protected_byte_outside",
                not (
                    offset
                    <= PROTECTED_BYTE_INDEX
                    < end
                ),
                "protected byte lies inside object range",
            )

        for left_index in range(
            len(OBJECT_SPECS)
        ):
            for right_index in range(
                left_index + 1,
                len(OBJECT_SPECS),
            ):
                left = (
                    OBJECT_SPECS[
                        left_index
                    ]
                )
                right = (
                    OBJECT_SPECS[
                        right_index
                    ]
                )

                left_start = int(
                    left["offset"]
                )
                left_end = (
                    left_start
                    + int(
                        left["length"]
                    )
                )

                right_start = int(
                    right["offset"]
                )
                right_end = (
                    right_start
                    + int(
                        right["length"]
                    )
                )

                require(
                    checks,
                    "range_"
                    + left["label"]
                    + "_"
                    + right["label"]
                    + "_nonoverlap",
                    (
                        left_end
                        <= right_start
                        or right_end
                        <= left_start
                    ),
                    "controlled object ranges overlap",
                )

        sorted_labels = [
            row["label"]
            for row in sorted(
                OBJECT_SPECS,
                key=lambda row: (
                    int(
                        row["length"]
                    ),
                    str(
                        row["object_pk"]
                    ),
                ),
            )
        ]

        require(
            checks,
            "v1_1_sort_order_exact",
            sorted_labels
            == [
                "A",
                "B",
                "C",
                "D",
            ],
            "frozen V1.1 sort order mismatch",
        )

        FIXTURE_ROOT.mkdir(
            parents=True,
            exist_ok=False,
        )

        write_bytes_exclusive(
            SEGMENT_PATH,
            segment_bytes,
        )

        require(
            checks,
            "segment_file_sha256_exact",
            file_sha256(
                SEGMENT_PATH
            )
            == SEGMENT_SHA256,
            "persisted segment SHA256 mismatch",
        )

        object_inputs = [
            {
                "model_pk":
                    MODEL_PK,
                "object_pk":
                    row[
                        "object_pk"
                    ],
                "segment_path":
                    str(
                        SEGMENT_PATH
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
            for row in OBJECT_SPECS
        ]

        build = generation.build_generation(
            model_pk=MODEL_PK,
            segments=[
                {
                    "segment_path":
                        str(
                            SEGMENT_PATH
                        ),
                    "segment_length":
                        SEGMENT_LENGTH,
                    "segment_sha256":
                        SEGMENT_SHA256,
                }
            ],
            objects=object_inputs,
            manifest_path=(
                MANIFEST_PATH
            ),
        )

        require(
            checks,
            "manifest_file_present",
            MANIFEST_PATH.is_file(),
            "candidate manifest missing after build",
        )

        manifest_bytes = (
            MANIFEST_PATH.read_bytes()
        )

        manifest_sha256 = (
            bytes_sha256(
                manifest_bytes
            )
        )

        manifest = json.loads(
            manifest_bytes.decode(
                "utf-8"
            )
        )

        require(
            checks,
            "manifest_canonical",
            generation.canonical_json_bytes(
                manifest
            )
            == manifest_bytes,
            "candidate manifest is not canonical JSON",
        )

        verified_generation_pk = (
            generation.verify_manifest(
                manifest
            )
        )

        generation_pk = str(
            verified_generation_pk
        )

        require(
            checks,
            "build_generation_pk_matches_verified",
            str(
                build.generation_pk
            )
            == generation_pk,
            "build generation PK differs from verified manifest",
        )

        require(
            checks,
            "manifest_generation_pk_exact",
            manifest[
                "generation_pk"
            ]
            == generation_pk,
            "manifest generation PK mismatch",
        )

        descriptor = manifest[
            "descriptor"
        ]

        require(
            checks,
            "descriptor_model_pk_exact",
            descriptor[
                "model_pk"
            ]
            == MODEL_PK,
            "descriptor model PK mismatch",
        )

        require(
            checks,
            "descriptor_segment_count_exact",
            len(
                descriptor[
                    "segments"
                ]
            )
            == 1,
            "descriptor segment count mismatch",
        )

        require(
            checks,
            "descriptor_object_count_exact",
            len(
                descriptor[
                    "objects"
                ]
            )
            == 4,
            "descriptor object count mismatch",
        )

        segment_row = (
            descriptor[
                "segments"
            ][0]
        )

        segment_id = str(
            segment_row[
                "segment_id"
            ]
        )

        require(
            checks,
            "segment_id_exact",
            segment_id
            == EXPECTED_SEGMENT_ID,
            "generated segment ID mismatch",
        )

        require(
            checks,
            "descriptor_segment_length_exact",
            segment_row[
                "segment_length"
            ]
            == SEGMENT_LENGTH,
            "descriptor segment length mismatch",
        )

        require(
            checks,
            "descriptor_segment_sha256_exact",
            segment_row[
                "segment_sha256"
            ]
            == SEGMENT_SHA256,
            "descriptor segment SHA256 mismatch",
        )

        expected_by_pk = {
            row["object_pk"]:
                row
            for row in OBJECT_SPECS
        }

        actual_by_pk = {
            row["object_pk"]:
                row
            for row in descriptor[
                "objects"
            ]
        }

        require(
            checks,
            "descriptor_object_pk_set_exact",
            set(
                actual_by_pk
            )
            == set(
                expected_by_pk
            ),
            "descriptor object PK set mismatch",
        )

        for object_pk, expected in (
            expected_by_pk.items()
        ):
            actual = (
                actual_by_pk[
                    object_pk
                ]
            )

            for field in (
                "offset",
                "length",
                "object_file_sha256",
                "payload_sha256",
            ):
                require(
                    checks,
                    "descriptor_"
                    + expected["label"]
                    + "_"
                    + field
                    + "_exact",
                    actual[field]
                    == expected[field],
                    "descriptor object field mismatch",
                )

            require(
                checks,
                "descriptor_"
                + expected["label"]
                + "_segment_id_exact",
                actual[
                    "segment_id"
                ]
                == EXPECTED_SEGMENT_ID,
                "descriptor object segment ID mismatch",
            )

        activation.activate_generation(
            model_pk=MODEL_PK,
            generation_pk=(
                generation_pk
            ),
            candidate_manifest_path=(
                MANIFEST_PATH
            ),
            active_record_path=(
                ACTIVE_PATH
            ),
            segment_paths={
                EXPECTED_SEGMENT_ID:
                    SEGMENT_PATH,
            },
        )

        require(
            checks,
            "active_record_present",
            ACTIVE_PATH.is_file(),
            "active generation record missing",
        )

        active_bytes = (
            ACTIVE_PATH.read_bytes()
        )

        active = json.loads(
            active_bytes.decode(
                "utf-8"
            )
        )

        require(
            checks,
            "active_record_canonical",
            activation.canonical_json_bytes(
                active
            )
            == active_bytes,
            "active generation record is not canonical JSON",
        )

        require(
            checks,
            "active_schema_exact",
            active["schema"]
            == ACTIVE_SCHEMA,
            "active record schema mismatch",
        )

        require(
            checks,
            "active_version_exact",
            active[
                "active_generation_version"
            ]
            == ACTIVE_VERSION,
            "active record version mismatch",
        )

        require(
            checks,
            "active_model_pk_exact",
            active[
                "model_pk"
            ]
            == MODEL_PK,
            "active record model PK mismatch",
        )

        require(
            checks,
            "active_generation_pk_exact",
            active[
                "generation_pk"
            ]
            == generation_pk,
            "active record generation PK mismatch",
        )

        require(
            checks,
            "active_manifest_sha256_exact",
            active[
                "generation_manifest_sha256"
            ]
            == manifest_sha256,
            "active record manifest SHA256 mismatch",
        )

        require(
            checks,
            "active_partial_absent",
            not ACTIVE_PARTIAL_PATH.exists(),
            "active record partial file remains",
        )

        expected_files = {
            SEGMENT_PATH.name,
            MANIFEST_PATH.name,
            ACTIVE_PATH.name,
        }

        actual_files = {
            path.name
            for path in FIXTURE_ROOT.iterdir()
            if path.is_file()
        }

        actual_directories = {
            path.name
            for path in FIXTURE_ROOT.iterdir()
            if path.is_dir()
        }

        require(
            checks,
            "fixture_files_exact",
            actual_files
            == expected_files,
            "fixture root file set mismatch",
        )

        require(
            checks,
            "fixture_no_subdirectories",
            actual_directories
            == set(),
            "unexpected fixture subdirectory",
        )

        fixture_entry_count = len(
            descriptor[
                "objects"
            ]
        )

        positive_length_entry_count = sum(
            1
            for row in descriptor[
                "objects"
            ]
            if row[
                "length"
            ] > 0
        )

        require(
            checks,
            "fixture_entry_count_exact",
            fixture_entry_count
            == 4,
            "fixture entry count mismatch",
        )

        require(
            checks,
            "positive_length_entry_count_exact",
            positive_length_entry_count
            == 4,
            "positive-length entry count mismatch",
        )

        require(
            checks,
            "runtime_engine_final_sha256_exact",
            file_sha256(
                Path(
                    FROZEN_DEPENDENCIES[
                        "runtime_engine"
                    ][
                        "path"
                    ]
                )
            )
            == FROZEN_DEPENDENCIES[
                "runtime_engine"
            ][
                "sha256"
            ],
            "runtime-residency engine changed during construction",
        )

        require(
            checks,
            "v1_2_validation_still_absent",
            (
                not V12_PROTOCOL.exists()
                and not V12_RUNNER.exists()
                and not V12_RESULT.exists()
                and not V12_RUNTIME.exists()
            ),
            "V1.2 scientific validation artifact appeared",
        )

    except Exception as exc:
        fatal = {
            "type":
                type(exc).__name__,
            "message":
                str(exc),
        }

    result[
        "generation_pk"
    ] = generation_pk

    result[
        "generation_manifest_sha256"
    ] = manifest_sha256

    result[
        "segment_sha256"
    ] = actual_segment_sha256

    result[
        "fixture_entry_count"
    ] = fixture_entry_count

    result[
        "positive_length_entry_count"
    ] = positive_length_entry_count

    result[
        "checks"
    ] = checks

    failed_checks = [
        name
        for name, passed
        in checks.items()
        if not passed
    ]

    result[
        "failed_checks"
    ] = failed_checks

    construction_valid = (
        fatal is None
        and not failed_checks
    )

    result[
        "construction_valid"
    ] = construction_valid

    result[
        "all_pass"
    ] = construction_valid

    result[
        "fatal"
    ] = fatal

    try:
        write_result_exclusive(
            result
        )
    except Exception as result_exc:
        print(
            "FATAL RESULT WRITE:",
            type(result_exc).__name__,
            str(result_exc),
        )

        return 3

    print("=" * 72)
    print(
        " OPENMIND / PHASE 6C V1.2 FOUR-OBJECT FIXTURE CONSTRUCTION"
    )
    print("=" * 72)

    print(
        "construction_valid:",
        construction_valid,
    )

    print(
        "all_pass:",
        construction_valid,
    )

    print(
        "generation_pk:",
        generation_pk,
    )

    print(
        "manifest_sha256:",
        manifest_sha256,
    )

    print(
        "segment_sha256:",
        actual_segment_sha256,
    )

    print(
        "entry_count:",
        fixture_entry_count,
    )

    print(
        "positive_length_entry_count:",
        positive_length_entry_count,
    )

    print(
        "failed_checks:",
        failed_checks,
    )

    print(
        "fatal:",
        fatal,
    )

    return (
        0
        if construction_valid
        else 2
    )


def main() -> int:
    return run_construction()


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
