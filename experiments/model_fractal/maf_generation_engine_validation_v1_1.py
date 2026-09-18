#!/usr/bin/env python3

"""Preregistered MAF Generation Engine V1.1 corrective validation.

This runner is frozen before execution.

It validates candidate-generation construction only. It does not
activate generations, select a catalog database, open the source GGUF,
assign runtime residency, or perform inference.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import shutil
from pathlib import Path
from typing import Any, Callable

import maf_generation_engine_v1 as engine


ROOT = Path(__file__).resolve().parents[2]

FROZEN_RESULT = (
    ROOT
    / "experiments/model_fractal/"
    "maf_segment_builder_validation_v1.json"
)

SOURCE_RUNTIME = (
    ROOT
    / "results/runtime/"
    "maf_segment_builder_validation_v1"
)

SOURCE_SEGMENT = (
    SOURCE_RUNTIME
    / "candidate_segment.mafseg"
)

SOURCE_MANIFEST = (
    SOURCE_RUNTIME
    / "candidate_segment.manifest.json"
)

RUNTIME = (
    ROOT
    / "results/runtime/"
    "maf_generation_engine_validation_v1_1"
)

RESULT_PATH = (
    ROOT
    / "experiments/model_fractal/"
    "maf_generation_engine_validation_v1_1.json"
)

EXPECTED_FROZEN_RESULT_SHA256 = (
    "732291986d1b1ee3feeeadec1af34b5222d887f8b01acecc"
    "492de3cb0f0f242f"
)

EXPECTED_SEGMENT_SHA256 = (
    "c9f9ef93b96c60569d130fb1c27aa3357aa35e82f0b2b2c3"
    "aec497342df3e7b6"
)

EXPECTED_SEGMENT_LENGTH = 17_137_795
EXPECTED_OBJECT_COUNT = 3

EXPECTED_MODEL_PK = (
    "mafmodel:v1:"
    "d670768d29daf84be95501480a777fd1"
    "ee5fddda18f4d0a4c8c3953e1b8cc258"
)

CHUNK_BYTES = 1024 * 1024

RESULT_SCHEMA = (
    "openmind.maf_generation_engine_validation.v1_1"
)

MIXED_MODEL_PK = (
    "mafmodel:v1:"
    + ("0" * 64)
)

BAD_SHA256 = "0" * 64

MALFORMED_OBJECT_PK = "mafobj:v1:not-a-valid-digest"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        while True:
            block = handle.read(
                CHUNK_BYTES
            )

            if not block:
                break

            digest.update(block)

    return digest.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def frozen_input() -> tuple[
    dict[str, Any],
    dict[str, Any],
]:
    if not FROZEN_RESULT.is_file():
        raise RuntimeError(
            "frozen Segment Builder result missing"
        )

    if (
        file_sha256(FROZEN_RESULT)
        != EXPECTED_FROZEN_RESULT_SHA256
    ):
        raise RuntimeError(
            "frozen Segment Builder result SHA mismatch"
        )

    result = json.loads(
        FROZEN_RESULT.read_text(
            encoding="utf-8"
        )
    )

    if result.get("all_pass") is not True:
        raise RuntimeError(
            "Segment Builder result not all-pass"
        )

    if (
        result.get("model_pk")
        != EXPECTED_MODEL_PK
    ):
        raise RuntimeError(
            "frozen model_pk mismatch"
        )

    positive = result.get("positive")

    if not isinstance(positive, dict):
        raise RuntimeError(
            "positive Segment Builder record missing"
        )

    if (
        positive.get("segment_length")
        != EXPECTED_SEGMENT_LENGTH
    ):
        raise RuntimeError(
            "frozen segment length mismatch"
        )

    if (
        positive.get("segment_sha256")
        != EXPECTED_SEGMENT_SHA256
    ):
        raise RuntimeError(
            "frozen segment SHA field mismatch"
        )

    placements = positive.get(
        "placements"
    )

    if (
        not isinstance(placements, list)
        or len(placements)
        != EXPECTED_OBJECT_COUNT
    ):
        raise RuntimeError(
            "frozen placement count mismatch"
        )

    return result, positive


def validate_source_evidence(
    result: dict[str, Any],
    positive: dict[str, Any],
) -> None:
    if not SOURCE_SEGMENT.is_file():
        raise RuntimeError(
            "frozen candidate segment missing"
        )

    if not SOURCE_MANIFEST.is_file():
        raise RuntimeError(
            "frozen Segment Builder manifest missing"
        )

    if (
        SOURCE_SEGMENT.stat().st_size
        != EXPECTED_SEGMENT_LENGTH
    ):
        raise RuntimeError(
            "source segment length changed"
        )

    if (
        file_sha256(SOURCE_SEGMENT)
        != EXPECTED_SEGMENT_SHA256
    ):
        raise RuntimeError(
            "source segment SHA changed"
        )

    manifest = json.loads(
        SOURCE_MANIFEST.read_text(
            encoding="utf-8"
        )
    )

    if (
        manifest.get("schema")
        != "openmind.maf_segment_manifest.v1"
    ):
        raise RuntimeError(
            "Segment Builder manifest schema mismatch"
        )

    if (
        manifest.get("model_pk")
        != EXPECTED_MODEL_PK
    ):
        raise RuntimeError(
            "Segment Builder manifest model mismatch"
        )

    if (
        manifest.get("segment_length")
        != EXPECTED_SEGMENT_LENGTH
    ):
        raise RuntimeError(
            "Segment Builder manifest length mismatch"
        )

    if (
        manifest.get("segment_sha256")
        != EXPECTED_SEGMENT_SHA256
    ):
        raise RuntimeError(
            "Segment Builder manifest SHA mismatch"
        )

    if (
        manifest.get("objects")
        != positive.get("placements")
    ):
        raise RuntimeError(
            "Segment Builder placement evidence mismatch"
        )

    if (
        result.get("manifest_schema")
        != manifest.get("schema")
    ):
        raise RuntimeError(
            "frozen result/manifest schema mismatch"
        )


def segment_records(
    path: Path = SOURCE_SEGMENT,
) -> list[dict[str, Any]]:
    return [
        {
            "segment_path": str(path),
            "segment_length": (
                path.stat().st_size
            ),
            "segment_sha256": (
                file_sha256(path)
            ),
        }
    ]


def object_records(
    positive: dict[str, Any],
    path: Path = SOURCE_SEGMENT,
) -> list[dict[str, Any]]:
    rows = []

    for placement in positive["placements"]:
        rows.append(
            {
                "model_pk": EXPECTED_MODEL_PK,
                "object_pk": (
                    placement["object_pk"]
                ),
                "segment_path": str(path),
                "offset": placement["offset"],
                "length": placement["length"],
                "object_file_sha256": (
                    placement[
                        "object_file_sha256"
                    ]
                ),
                "payload_sha256": (
                    placement["payload_sha256"]
                ),
            }
        )

    return rows


def expect_failure(
    label: str,
    operation: Callable[[], Any],
) -> dict[str, Any]:
    failed_closed = False
    error_type = None
    error_text = None

    try:
        operation()
    except Exception as exc:
        failed_closed = True
        error_type = type(exc).__name__
        error_text = str(exc)

    return {
        "label": label,
        "failed_closed": failed_closed,
        "error_type": error_type,
        "error_text": error_text,
        "pass": failed_closed,
    }


def extract_range(
    *,
    source: Path,
    target: Path,
    offset: int,
    length: int,
) -> None:
    remaining = length

    with (
        source.open("rb") as src,
        target.open("xb") as dst,
    ):
        src.seek(offset)

        while remaining:
            want = min(
                remaining,
                CHUNK_BYTES,
            )
            block = src.read(want)

            if len(block) != want:
                raise RuntimeError(
                    "short source range read"
                )

            dst.write(block)
            remaining -= len(block)


def positive_case(
    positive: dict[str, Any],
) -> dict[str, Any]:
    segments = segment_records()
    objects = object_records(
        positive
    )

    in_memory_a = engine.build_manifest(
        model_pk=EXPECTED_MODEL_PK,
        segments=segments,
        objects=objects,
        chunk_bytes=CHUNK_BYTES,
    )

    in_memory_b = engine.build_manifest(
        model_pk=EXPECTED_MODEL_PK,
        segments=copy.deepcopy(segments),
        objects=copy.deepcopy(objects),
        chunk_bytes=CHUNK_BYTES,
    )

    permuted_objects = list(
        reversed(
            copy.deepcopy(objects)
        )
    )

    permuted_manifest = (
        engine.build_manifest(
            model_pk=EXPECTED_MODEL_PK,
            segments=copy.deepcopy(segments),
            objects=permuted_objects,
            chunk_bytes=CHUNK_BYTES,
        )
    )

    candidate_path = (
        RUNTIME
        / "candidate_generation.manifest.json"
    )

    build_result = engine.build_generation(
        model_pk=EXPECTED_MODEL_PK,
        segments=segments,
        objects=objects,
        manifest_path=candidate_path,
        chunk_bytes=CHUNK_BYTES,
    )

    reopened = (
        engine.reopen_candidate_manifest(
            candidate_path
        )
    )

    generation_pk = (
        engine.verify_manifest(
            reopened
        )
    )

    descriptor = reopened["descriptor"]

    actual_object_pks = [
        row["object_pk"]
        for row in descriptor["objects"]
    ]

    expected_object_pks = sorted(
        placement["object_pk"]
        for placement
        in positive["placements"]
    )

    actual_offsets = {
        row["object_pk"]: row["offset"]
        for row in descriptor["objects"]
    }

    expected_offsets = {
        row["object_pk"]: row["offset"]
        for row in positive["placements"]
    }

    actual_lengths = {
        row["object_pk"]: row["length"]
        for row in descriptor["objects"]
    }

    expected_lengths = {
        row["object_pk"]: row["length"]
        for row in positive["placements"]
    }

    actual_file_hashes = {
        row["object_pk"]:
            row["object_file_sha256"]
        for row in descriptor["objects"]
    }

    expected_file_hashes = {
        row["object_pk"]:
            row["object_file_sha256"]
        for row in positive["placements"]
    }

    actual_payload_hashes = {
        row["object_pk"]:
            row["payload_sha256"]
        for row in descriptor["objects"]
    }

    expected_payload_hashes = {
        row["object_pk"]:
            row["payload_sha256"]
        for row in positive["placements"]
    }

    checks = {
        "model_pk_preserved": (
            descriptor["model_pk"]
            == EXPECTED_MODEL_PK
        ),
        "one_segment": (
            len(descriptor["segments"]) == 1
        ),
        "segment_length_preserved": (
            descriptor["segments"][0][
                "segment_length"
            ]
            == EXPECTED_SEGMENT_LENGTH
        ),
        "segment_sha_preserved": (
            descriptor["segments"][0][
                "segment_sha256"
            ]
            == EXPECTED_SEGMENT_SHA256
        ),
        "object_count_exact": (
            len(descriptor["objects"])
            == EXPECTED_OBJECT_COUNT
        ),
        "object_pks_exact": (
            actual_object_pks
            == expected_object_pks
        ),
        "offsets_exact": (
            actual_offsets
            == expected_offsets
        ),
        "lengths_exact": (
            actual_lengths
            == expected_lengths
        ),
        "object_hashes_exact": (
            actual_file_hashes
            == expected_file_hashes
        ),
        "payload_hashes_exact": (
            actual_payload_hashes
            == expected_payload_hashes
        ),
        "repeated_construction_equal": (
            in_memory_a == in_memory_b
        ),
        "object_input_permutation_equal": (
            in_memory_a
            == permuted_manifest
        ),
        "persisted_equals_memory": (
            reopened == in_memory_a
        ),
        "canonical_manifest_bytes": (
            candidate_path.read_bytes()
            == canonical_bytes(reopened)
        ),
        "generation_pk_reopens": (
            generation_pk
            == build_result.generation_pk
        ),
        "descriptor_sha_matches_pk": (
            generation_pk
            == (
                "mafgen:v1:"
                + build_result.descriptor_sha256
            )
        ),
    }

    return {
        "pass": all(checks.values()),
        "checks": checks,
        "generation_pk": generation_pk,
        "descriptor_sha256": (
            build_result.descriptor_sha256
        ),
        "manifest_path": str(
            candidate_path
        ),
        "manifest_sha256": file_sha256(
            candidate_path
        ),
        "descriptor": descriptor,
    }


def path_independence_case(
    positive: dict[str, Any],
    baseline_generation_pk: str,
) -> dict[str, Any]:
    alias_path = (
        RUNTIME
        / "path_alias_segment.mafseg"
    )

    shutil.copyfile(
        SOURCE_SEGMENT,
        alias_path,
    )

    if (
        file_sha256(alias_path)
        != EXPECTED_SEGMENT_SHA256
    ):
        raise RuntimeError(
            "path-alias segment SHA mismatch"
        )

    manifest = engine.build_manifest(
        model_pk=EXPECTED_MODEL_PK,
        segments=segment_records(
            alias_path
        ),
        objects=object_records(
            positive,
            alias_path,
        ),
        chunk_bytes=CHUNK_BYTES,
    )

    alias_generation_pk = (
        engine.verify_manifest(
            manifest
        )
    )

    passed = (
        alias_generation_pk
        == baseline_generation_pk
    )

    return {
        "pass": passed,
        "baseline_generation_pk": (
            baseline_generation_pk
        ),
        "alias_generation_pk": (
            alias_generation_pk
        ),
        "segment_sha_equal": (
            file_sha256(alias_path)
            == EXPECTED_SEGMENT_SHA256
        ),
        "physical_path_changed": (
            alias_path.resolve()
            != SOURCE_SEGMENT.resolve()
        ),
    }


def multi_segment_order_case(
    positive: dict[str, Any],
) -> dict[str, Any]:
    first = positive["placements"][0]
    second = positive["placements"][1]

    segment_a = (
        RUNTIME
        / "synthetic_two_segment_a.mafseg"
    )
    segment_b = (
        RUNTIME
        / "synthetic_two_segment_b.mafseg"
    )

    extract_range(
        source=SOURCE_SEGMENT,
        target=segment_a,
        offset=first["offset"],
        length=first["length"],
    )

    extract_range(
        source=SOURCE_SEGMENT,
        target=segment_b,
        offset=second["offset"],
        length=second["length"],
    )

    if (
        file_sha256(segment_a)
        != first["object_file_sha256"]
    ):
        raise RuntimeError(
            "synthetic segment A hash mismatch"
        )

    if (
        file_sha256(segment_b)
        != second["object_file_sha256"]
    ):
        raise RuntimeError(
            "synthetic segment B hash mismatch"
        )

    segments = [
        {
            "segment_path": str(segment_a),
            "segment_length": (
                segment_a.stat().st_size
            ),
            "segment_sha256": (
                file_sha256(segment_a)
            ),
        },
        {
            "segment_path": str(segment_b),
            "segment_length": (
                segment_b.stat().st_size
            ),
            "segment_sha256": (
                file_sha256(segment_b)
            ),
        },
    ]

    objects = [
        {
            "model_pk": EXPECTED_MODEL_PK,
            "object_pk": first["object_pk"],
            "segment_path": str(segment_a),
            "offset": 0,
            "length": first["length"],
            "object_file_sha256": (
                first["object_file_sha256"]
            ),
            "payload_sha256": (
                first["payload_sha256"]
            ),
        },
        {
            "model_pk": EXPECTED_MODEL_PK,
            "object_pk": second["object_pk"],
            "segment_path": str(segment_b),
            "offset": 0,
            "length": second["length"],
            "object_file_sha256": (
                second["object_file_sha256"]
            ),
            "payload_sha256": (
                second["payload_sha256"]
            ),
        },
    ]

    forward = engine.build_manifest(
        model_pk=EXPECTED_MODEL_PK,
        segments=segments,
        objects=objects,
        chunk_bytes=CHUNK_BYTES,
    )

    reverse = engine.build_manifest(
        model_pk=EXPECTED_MODEL_PK,
        segments=list(
            reversed(
                copy.deepcopy(segments)
            )
        ),
        objects=copy.deepcopy(objects),
        chunk_bytes=CHUNK_BYTES,
    )

    forward_pk = engine.verify_manifest(
        forward
    )
    reverse_pk = engine.verify_manifest(
        reverse
    )

    return {
        "pass": (
            forward == reverse
            and forward_pk == reverse_pk
        ),
        "generation_pk_forward": (
            forward_pk
        ),
        "generation_pk_reverse": (
            reverse_pk
        ),
        "distinct_segment_hashes": (
            file_sha256(segment_a)
            != file_sha256(segment_b)
        ),
        "segment_count": 2,
    }


def placement_sensitivity_case(
    positive: dict[str, Any],
) -> dict[str, Any]:
    first = positive["placements"][0]

    repeated_segment = (
        RUNTIME
        / "synthetic_repeated_object.mafseg"
    )

    object_bytes_path = (
        RUNTIME
        / "synthetic_object_bytes.bin"
    )

    extract_range(
        source=SOURCE_SEGMENT,
        target=object_bytes_path,
        offset=first["offset"],
        length=first["length"],
    )

    object_bytes = (
        object_bytes_path.read_bytes()
    )

    with repeated_segment.open("xb") as dst:
        dst.write(object_bytes)
        dst.write(object_bytes)

    object_bytes_path.unlink()

    expected_object_sha = (
        first["object_file_sha256"]
    )

    if (
        hashlib.sha256(
            object_bytes
        ).hexdigest()
        != expected_object_sha
    ):
        raise RuntimeError(
            "placement sensitivity object hash mismatch"
        )

    repeated_sha = file_sha256(
        repeated_segment
    )

    segments = [
        {
            "segment_path": str(
                repeated_segment
            ),
            "segment_length": (
                repeated_segment.stat().st_size
            ),
            "segment_sha256": repeated_sha,
        }
    ]

    base_object = {
        "model_pk": EXPECTED_MODEL_PK,
        "object_pk": first["object_pk"],
        "segment_path": str(
            repeated_segment
        ),
        "offset": 0,
        "length": first["length"],
        "object_file_sha256": (
            expected_object_sha
        ),
        "payload_sha256": (
            first["payload_sha256"]
        ),
    }

    moved_object = copy.deepcopy(
        base_object
    )
    moved_object["offset"] = (
        first["length"]
    )

    base_manifest = engine.build_manifest(
        model_pk=EXPECTED_MODEL_PK,
        segments=segments,
        objects=[base_object],
        chunk_bytes=CHUNK_BYTES,
    )

    moved_manifest = engine.build_manifest(
        model_pk=EXPECTED_MODEL_PK,
        segments=segments,
        objects=[moved_object],
        chunk_bytes=CHUNK_BYTES,
    )

    base_pk = engine.verify_manifest(
        base_manifest
    )
    moved_pk = engine.verify_manifest(
        moved_manifest
    )

    base_object_pk = (
        base_manifest["descriptor"][
            "objects"
        ][0]["object_pk"]
    )
    moved_object_pk = (
        moved_manifest["descriptor"][
            "objects"
        ][0]["object_pk"]
    )

    return {
        "pass": (
            base_pk != moved_pk
            and base_object_pk
            == moved_object_pk
            == first["object_pk"]
        ),
        "generation_pk_changed": (
            base_pk != moved_pk
        ),
        "object_pk_changed": (
            base_object_pk
            != moved_object_pk
        ),
        "base_generation_pk": base_pk,
        "moved_generation_pk": moved_pk,
        "object_pk": base_object_pk,
        "base_offset": 0,
        "moved_offset": first["length"],
        "exact_bytes_repeated": True,
    }


def negative_controls(
    positive: dict[str, Any],
) -> list[dict[str, Any]]:
    base_segments = segment_records()
    base_objects = object_records(
        positive
    )

    rows = []

    duplicate_objects = copy.deepcopy(
        base_objects
    )
    duplicate_objects.append(
        copy.deepcopy(
            base_objects[0]
        )
    )

    rows.append(
        expect_failure(
            "duplicate_object_pk",
            lambda: engine.build_manifest(
                model_pk=EXPECTED_MODEL_PK,
                segments=base_segments,
                objects=duplicate_objects,
                chunk_bytes=CHUNK_BYTES,
            ),
        )
    )

    mixed_objects = copy.deepcopy(
        base_objects
    )
    mixed_objects[0][
        "model_pk"
    ] = MIXED_MODEL_PK

    rows.append(
        expect_failure(
            "mixed_model",
            lambda: engine.build_manifest(
                model_pk=EXPECTED_MODEL_PK,
                segments=base_segments,
                objects=mixed_objects,
                chunk_bytes=CHUNK_BYTES,
            ),
        )
    )

    missing_segment = (
        RUNTIME
        / "does_not_exist.mafseg"
    )

    rows.append(
        expect_failure(
            "missing_segment",
            lambda: engine.build_manifest(
                model_pk=EXPECTED_MODEL_PK,
                segments=[
                    {
                        "segment_path": str(
                            missing_segment
                        ),
                        "segment_length": (
                            EXPECTED_SEGMENT_LENGTH
                        ),
                        "segment_sha256": (
                            EXPECTED_SEGMENT_SHA256
                        ),
                    }
                ],
                objects=base_objects,
                chunk_bytes=CHUNK_BYTES,
            ),
        )
    )

    bad_segment_sha = copy.deepcopy(
        base_segments
    )
    bad_segment_sha[0][
        "segment_sha256"
    ] = BAD_SHA256

    rows.append(
        expect_failure(
            "altered_segment_sha",
            lambda: engine.build_manifest(
                model_pk=EXPECTED_MODEL_PK,
                segments=bad_segment_sha,
                objects=base_objects,
                chunk_bytes=CHUNK_BYTES,
            ),
        )
    )

    out_of_bounds = copy.deepcopy(
        base_objects
    )
    out_of_bounds[0]["offset"] = (
        EXPECTED_SEGMENT_LENGTH
    )

    rows.append(
        expect_failure(
            "out_of_bounds_offset",
            lambda: engine.build_manifest(
                model_pk=EXPECTED_MODEL_PK,
                segments=base_segments,
                objects=out_of_bounds,
                chunk_bytes=CHUNK_BYTES,
            ),
        )
    )

    zero_length = copy.deepcopy(
        base_objects
    )
    zero_length[0]["length"] = 0

    rows.append(
        expect_failure(
            "zero_length",
            lambda: engine.build_manifest(
                model_pk=EXPECTED_MODEL_PK,
                segments=base_segments,
                objects=zero_length,
                chunk_bytes=CHUNK_BYTES,
            ),
        )
    )

    bad_object_hash = copy.deepcopy(
        base_objects
    )
    bad_object_hash[0][
        "object_file_sha256"
    ] = BAD_SHA256

    rows.append(
        expect_failure(
            "incorrect_object_file_sha256",
            lambda: engine.build_manifest(
                model_pk=EXPECTED_MODEL_PK,
                segments=base_segments,
                objects=bad_object_hash,
                chunk_bytes=CHUNK_BYTES,
            ),
        )
    )

    bad_object_pk = copy.deepcopy(
        base_objects
    )
    bad_object_pk[0][
        "object_pk"
    ] = MALFORMED_OBJECT_PK

    rows.append(
        expect_failure(
            "malformed_object_pk",
            lambda: engine.build_manifest(
                model_pk=EXPECTED_MODEL_PK,
                segments=base_segments,
                objects=bad_object_pk,
                chunk_bytes=CHUNK_BYTES,
            ),
        )
    )

    malformed_sha = copy.deepcopy(
        base_objects
    )
    malformed_sha[0][
        "payload_sha256"
    ] = "not-a-sha256"

    rows.append(
        expect_failure(
            "malformed_sha256",
            lambda: engine.build_manifest(
                model_pk=EXPECTED_MODEL_PK,
                segments=base_segments,
                objects=malformed_sha,
                chunk_bytes=CHUNK_BYTES,
            ),
        )
    )

    final_path = (
        RUNTIME
        / "negative_existing_final.json"
    )
    final_path.write_bytes(
        b"sentinel"
    )

    rows.append(
        expect_failure(
            "preexisting_final_manifest",
            lambda: engine.build_generation(
                model_pk=EXPECTED_MODEL_PK,
                segments=base_segments,
                objects=base_objects,
                manifest_path=final_path,
                chunk_bytes=CHUNK_BYTES,
            ),
        )
    )

    if (
        final_path.read_bytes()
        != b"sentinel"
    ):
        raise RuntimeError(
            "preexisting final sentinel changed"
        )

    partial_final = (
        RUNTIME
        / "negative_existing_partial.json"
    )
    partial_path = (
        partial_final.with_name(
            partial_final.name + ".partial"
        )
    )
    partial_path.write_bytes(
        b"partial-sentinel"
    )

    rows.append(
        expect_failure(
            "preexisting_partial_manifest",
            lambda: engine.build_generation(
                model_pk=EXPECTED_MODEL_PK,
                segments=base_segments,
                objects=base_objects,
                manifest_path=partial_final,
                chunk_bytes=CHUNK_BYTES,
            ),
        )
    )

    if (
        partial_path.read_bytes()
        != b"partial-sentinel"
    ):
        raise RuntimeError(
            "preexisting partial sentinel changed"
        )

    good_manifest = engine.build_manifest(
        model_pk=EXPECTED_MODEL_PK,
        segments=base_segments,
        objects=base_objects,
        chunk_bytes=CHUNK_BYTES,
    )

    tampered_manifest = copy.deepcopy(
        good_manifest
    )
    tampered_manifest[
        "generation_pk"
    ] = (
        "mafgen:v1:"
        + ("f" * 64)
    )

    tampered_path = (
        RUNTIME
        / "negative_generation_pk_mismatch.json"
    )

    tampered_path.write_bytes(
        canonical_bytes(
            tampered_manifest
        )
    )

    rows.append(
        expect_failure(
            "generation_pk_mismatch_on_reopen",
            lambda: (
                engine.reopen_candidate_manifest(
                    tampered_path
                )
            ),
        )
    )

    return rows


def static_policy_checks() -> dict[str, bool]:
    engine_source = (
        ROOT
        / "experiments/model_fractal/"
        "maf_generation_engine_v1.py"
    ).read_text(
        encoding="utf-8"
    ).lower()

    runner_source = Path(
        __file__
    ).read_text(
        encoding="utf-8"
    )

    runner_tree = ast.parse(
        runner_source
    )

    class OperationalGGUFLiteralAudit(
        ast.NodeVisitor
    ):
        """Find executable GGUF path literals.

        Module/function/class docstrings are descriptive
        policy text, not operational file dependencies.

        The static_policy_checks function is also excluded
        because it necessarily describes and searches for
        the prohibited condition itself.
        """

        def __init__(self) -> None:
            self.found = False

        @staticmethod
        def body_without_docstring(
            node: ast.AST,
        ) -> list[ast.stmt]:
            body = getattr(
                node,
                "body",
                [],
            )

            if (
                body
                and isinstance(
                    body[0],
                    ast.Expr,
                )
                and isinstance(
                    body[0].value,
                    ast.Constant,
                )
                and isinstance(
                    body[0].value.value,
                    str,
                )
            ):
                return body[1:]

            return body

        def visit_Module(
            self,
            node: ast.Module,
        ) -> None:
            for child in (
                self.body_without_docstring(
                    node
                )
            ):
                self.visit(child)

        def visit_FunctionDef(
            self,
            node: ast.FunctionDef,
        ) -> None:
            if (
                node.name
                == "static_policy_checks"
            ):
                return

            self.visit(node.args)

            for decorator in (
                node.decorator_list
            ):
                self.visit(decorator)

            if node.returns is not None:
                self.visit(node.returns)

            for child in (
                self.body_without_docstring(
                    node
                )
            ):
                self.visit(child)

        def visit_AsyncFunctionDef(
            self,
            node: ast.AsyncFunctionDef,
        ) -> None:
            self.visit_FunctionDef(node)

        def visit_ClassDef(
            self,
            node: ast.ClassDef,
        ) -> None:
            for base in node.bases:
                self.visit(base)

            for keyword in node.keywords:
                self.visit(keyword)

            for decorator in (
                node.decorator_list
            ):
                self.visit(decorator)

            for child in (
                self.body_without_docstring(
                    node
                )
            ):
                self.visit(child)

        def visit_Constant(
            self,
            node: ast.Constant,
        ) -> None:
            if (
                isinstance(node.value, str)
                and ".gguf"
                in node.value.lower()
            ):
                self.found = True

    audit = OperationalGGUFLiteralAudit()
    audit.visit(runner_tree)

    return {
        "engine_no_sqlite": (
            "sqlite3" not in engine_source
        ),
        "engine_no_mmap": (
            "import mmap" not in engine_source
        ),
        "engine_no_activation_api": (
            "activate_generation"
            not in engine_source
        ),
        "runner_no_source_gguf_path": (
            not audit.found
        ),
        "maf_native_not_enabled": (
            "enable_maf_native"
            not in engine_source
        ),
    }


def main() -> None:
    if RESULT_PATH.exists():
        raise RuntimeError(
            "frozen-result target already exists"
        )

    if RUNTIME.exists():
        raise RuntimeError(
            "generation validation runtime "
            "directory already exists"
        )

    result, positive = frozen_input()

    validate_source_evidence(
        result,
        positive,
    )

    source_sha_before = file_sha256(
        SOURCE_SEGMENT
    )

    RUNTIME.mkdir(
        parents=True,
        exist_ok=False,
    )

    positive_result = positive_case(
        positive
    )

    path_result = path_independence_case(
        positive,
        positive_result[
            "generation_pk"
        ],
    )

    segment_order_result = (
        multi_segment_order_case(
            positive
        )
    )

    placement_result = (
        placement_sensitivity_case(
            positive
        )
    )

    negative_result = negative_controls(
        positive
    )

    policy = static_policy_checks()

    source_sha_after = file_sha256(
        SOURCE_SEGMENT
    )

    source_segment_unchanged = (
        source_sha_before
        == source_sha_after
        == EXPECTED_SEGMENT_SHA256
    )

    negative_all_pass = all(
        row["pass"]
        for row in negative_result
    )

    all_pass = all(
        (
            positive_result["pass"],
            path_result["pass"],
            segment_order_result["pass"],
            placement_result["pass"],
            negative_all_pass,
            all(policy.values()),
            source_segment_unchanged,
        )
    )

    output = {
        "schema": RESULT_SCHEMA,
        "engine_schema": (
            engine.ENGINE_SCHEMA
        ),
        "engine_version": (
            engine.ENGINE_VERSION
        ),
        "descriptor_schema": (
            engine.DESCRIPTOR_SCHEMA
        ),
        "manifest_schema": (
            engine.MANIFEST_SCHEMA
        ),
        "chunk_bytes": CHUNK_BYTES,
        "frozen_segment_builder_result_sha256": (
            EXPECTED_FROZEN_RESULT_SHA256
        ),
        "source_segment_sha256": (
            EXPECTED_SEGMENT_SHA256
        ),
        "source_segment_length": (
            EXPECTED_SEGMENT_LENGTH
        ),
        "model_pk": EXPECTED_MODEL_PK,
        "positive": positive_result,
        "path_independence": path_result,
        "multi_segment_order_independence": (
            segment_order_result
        ),
        "placement_sensitivity": (
            placement_result
        ),
        "negative_controls": (
            negative_result
        ),
        "static_policy_checks": policy,
        "source_segment_unchanged": (
            source_segment_unchanged
        ),
        "generation_activated": False,
        "catalog_engine_selected": False,
        "source_gguf_required": False,
        "maf_native_compute_enabled": False,
        "all_pass": all_pass,
    }

    RESULT_PATH.write_bytes(
        canonical_bytes(output)
    )

    print("=" * 72)
    print(
        " OPENMIND / MAF GENERATION ENGINE V1.1 VALIDATION"
    )
    print("=" * 72)
    print(
        "generation_pk:",
        positive_result["generation_pk"],
    )
    print(
        "positive:",
        positive_result["pass"],
    )
    print(
        "path independence:",
        path_result["pass"],
    )
    print(
        "multi-segment order:",
        segment_order_result["pass"],
    )
    print(
        "placement sensitivity:",
        placement_result["pass"],
    )
    print(
        "negative controls:",
        negative_all_pass,
    )
    print(
        "source segment unchanged:",
        source_segment_unchanged,
    )
    print(
        "all_pass:",
        all_pass,
    )
    print(
        "result:",
        RESULT_PATH,
    )

    if not all_pass:
        raise RuntimeError(
            "Generation Engine V1.1 validation failed"
        )


if __name__ == "__main__":
    main()
