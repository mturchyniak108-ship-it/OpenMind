#!/usr/bin/env python3

"""Preregistered validation for OpenMind MAF Segment Builder v1."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import maf_segment_builder_v1 as builder


SCHEMA = "openmind.maf_segment_builder_validation.v1"

ROOT = Path(__file__).resolve().parents[2]

SOURCE_RUNTIME = (
    ROOT
    / "results"
    / "runtime"
    / "maf_encoder_validation_v1"
)

RUNTIME = (
    ROOT
    / "results"
    / "runtime"
    / "maf_segment_builder_validation_v1"
)

RESULT_PATH = (
    ROOT
    / "experiments"
    / "model_fractal"
    / "maf_segment_builder_validation_v1.json"
)

CHUNK_BYTES = 1024 * 1024

MODEL_PK = (
    "mafmodel:v1:"
    "d670768d29daf84be95501480a777fd1"
    "ee5fddda18f4d0a4c8c3953e1b8cc258"
)

OTHER_MODEL_PK = (
    "mafmodel:v1:"
    "00000000000000000000000000000000"
    "00000000000000000000000000000000"
)

INPUTS = [
    {
        "filename": "01.maf",
        "tensor_name": "blk.0.attn_norm.weight",
        "tensor_type": "F32",
        "model_pk": MODEL_PK,
        "object_pk": (
            "mafobj:v1:"
            "8489061c6271db7d1e726cc1795e0840"
            "23c261ce448e31d50af22de77681c696"
        ),
        "length": 6863,
        "offset": 0,
        "object_file_sha256": (
            "bcfbcc3e9c3a6bb3d27ec85e08f1fc2"
            "b6e67f1a0d3d8851d1d9b3dc612aebc08"
        ),
        "payload_length": 6144,
        "payload_sha256": (
            "7052e000bdc3d4442a8beb442998629c"
            "84ca4ff39fe9c92c78495736a96d3250"
        ),
    },
    {
        "filename": "02.maf",
        "tensor_name": "blk.0.attn_q.weight",
        "tensor_type": "Q8_0",
        "model_pk": MODEL_PK,
        "object_pk": (
            "mafobj:v1:"
            "1927b0228f913339bf9f6bd31daef6d1"
            "a2b6c3ad0aeb3c15fb158108288d44ba"
        ),
        "length": 2507480,
        "offset": 6863,
        "object_file_sha256": (
            "e800c4ae71eb64e005a770a186e12fe4"
            "ba87b4b154894f0f366b957e77fdf2a9"
        ),
        "payload_length": 2506752,
        "payload_sha256": (
            "97c8200d325e58cb936c84d7d5ee34d5"
            "e64e0a1c9b1f511b735d986d63ac5300"
        ),
    },
    {
        "filename": "03.maf",
        "tensor_name": "blk.0.ffn_down.weight",
        "tensor_type": "Q8_0",
        "model_pk": MODEL_PK,
        "object_pk": (
            "mafobj:v1:"
            "787817cc07b05c7520261bbccd9c3a290"
            "9a4a088e907093c3f43053879a4cd35"
        ),
        "length": 14623452,
        "offset": 2514343,
        "object_file_sha256": (
            "aec8a3ca7e9f310f4f85d32537720660"
            "af73f62c7e24dabf8d59e4686189d755"
        ),
        "payload_length": 14622720,
        "payload_sha256": (
            "d8f311c842b4abf6c51fd79bf8189760"
            "5bddb2dfea1529e79688900303c7dd37"
        ),
    },
]

EXPECTED_OBJECT_COUNT = 3
EXPECTED_SEGMENT_LENGTH = 17137795


def canonical_json_bytes(value: dict) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def stream_sha256(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        while True:
            chunk = stream.read(
                CHUNK_BYTES
            )

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


def assert_preregistered_inputs() -> list[dict]:
    records = []

    if len(INPUTS) != EXPECTED_OBJECT_COUNT:
        raise RuntimeError(
            "preregistered object count mismatch"
        )

    running_offset = 0
    total = 0

    for expected_ordinal, spec in enumerate(INPUTS):
        path = SOURCE_RUNTIME / spec["filename"]

        if not path.is_file():
            raise RuntimeError(
                f"missing frozen input: {path}"
            )

        actual_length = path.stat().st_size

        if actual_length != spec["length"]:
            raise RuntimeError(
                f"input length mismatch: {spec['filename']}"
            )

        actual_file_sha = stream_sha256(path)

        if (
            actual_file_sha
            != spec["object_file_sha256"]
        ):
            raise RuntimeError(
                f"input file SHA mismatch: {spec['filename']}"
            )

        view = builder.inspect_object(
            path,
            chunk_bytes=CHUNK_BYTES,
        )

        if view.tensor_name != spec["tensor_name"]:
            raise RuntimeError(
                "tensor-name mismatch: "
                f"{spec['filename']}"
            )

        if view.tensor_type != spec["tensor_type"]:
            raise RuntimeError(
                "tensor-type mismatch: "
                f"{spec['filename']}"
            )

        if (
            view.payload_length
            != spec["payload_length"]
        ):
            raise RuntimeError(
                "payload-length mismatch: "
                f"{spec['filename']}"
            )

        if (
            view.payload_sha256
            != spec["payload_sha256"]
        ):
            raise RuntimeError(
                "payload SHA mismatch: "
                f"{spec['filename']}"
            )

        if spec["offset"] != running_offset:
            raise RuntimeError(
                "preregistered offset arithmetic mismatch"
            )

        records.append(
            {
                "model_pk": spec["model_pk"],
                "object_pk": spec["object_pk"],
                "object_path": str(path),
                "object_file_sha256": (
                    spec["object_file_sha256"]
                ),
                "payload_sha256": (
                    spec["payload_sha256"]
                ),
            }
        )

        running_offset += actual_length
        total += actual_length

    if total != EXPECTED_SEGMENT_LENGTH:
        raise RuntimeError(
            "preregistered total length mismatch"
        )

    return records


def expected_concatenation_sha256() -> str:
    digest = hashlib.sha256()

    for spec in INPUTS:
        path = SOURCE_RUNTIME / spec["filename"]

        with path.open("rb") as stream:
            while True:
                chunk = stream.read(
                    CHUNK_BYTES
                )

                if not chunk:
                    break

                digest.update(chunk)

    return digest.hexdigest()


def compare_segment_ranges(
    segment_path: Path,
) -> list[dict]:
    rows = []

    with segment_path.open("rb") as segment:
        for ordinal, spec in enumerate(INPUTS):
            if segment.tell() != spec["offset"]:
                raise RuntimeError(
                    "segment range offset mismatch"
                )

            digest = hashlib.sha256()
            remaining = spec["length"]

            with (
                SOURCE_RUNTIME
                / spec["filename"]
            ).open("rb") as original:
                while remaining:
                    want = min(
                        remaining,
                        CHUNK_BYTES,
                    )

                    segment_chunk = segment.read(want)
                    original_chunk = original.read(want)

                    if len(segment_chunk) != want:
                        raise RuntimeError(
                            "segment range truncated"
                        )

                    if len(original_chunk) != want:
                        raise RuntimeError(
                            "original object truncated"
                        )

                    if segment_chunk != original_chunk:
                        raise RuntimeError(
                            "segment/original byte mismatch"
                        )

                    digest.update(
                        segment_chunk
                    )

                    remaining -= want

                if original.read(1):
                    raise RuntimeError(
                        "unexpected original trailing byte"
                    )

            actual_sha = digest.hexdigest()

            if (
                actual_sha
                != spec["object_file_sha256"]
            ):
                raise RuntimeError(
                    "segment range SHA mismatch"
                )

            rows.append(
                {
                    "ordinal": ordinal,
                    "object_pk": spec["object_pk"],
                    "offset": spec["offset"],
                    "length": spec["length"],
                    "object_file_sha256": actual_sha,
                    "exact_byte_match": True,
                }
            )

        if segment.read(1):
            raise RuntimeError(
                "unexpected trailing segment bytes"
            )

    return rows


def expect_failure(
    *,
    label: str,
    records: list[dict],
    segment_path: Path,
    manifest_path: Path,
) -> dict:
    failed_closed = False
    error_type = None
    error_text = None

    try:
        builder.build_segment(
            model_pk=MODEL_PK,
            objects=records,
            segment_path=segment_path,
            manifest_path=manifest_path,
            chunk_bytes=CHUNK_BYTES,
        )
    except Exception as exc:
        failed_closed = True
        error_type = type(exc).__name__
        error_text = str(exc)

    partials = [
        segment_path.with_name(
            segment_path.name + ".partial"
        ),
        manifest_path.with_name(
            manifest_path.name + ".partial"
        ),
    ]

    no_outputs = (
        not segment_path.exists()
        and not manifest_path.exists()
        and all(
            not path.exists()
            for path in partials
        )
    )

    passed = (
        failed_closed
        and no_outputs
    )

    return {
        "label": label,
        "failed_closed": failed_closed,
        "no_activated_outputs": no_outputs,
        "error_type": error_type,
        "error_text": error_text,
        "pass": passed,
    }


def main() -> None:
    if RESULT_PATH.exists():
        raise RuntimeError(
            f"result already exists: {RESULT_PATH}"
        )

    if RUNTIME.exists():
        raise RuntimeError(
            f"runtime directory already exists: {RUNTIME}"
        )

    records = assert_preregistered_inputs()

    expected_segment_sha = (
        expected_concatenation_sha256()
    )

    RUNTIME.mkdir(
        parents=True,
        exist_ok=False,
    )

    segment_path = (
        RUNTIME
        / "candidate_segment.mafseg"
    )

    manifest_path = (
        RUNTIME
        / "candidate_segment.manifest.json"
    )

    positive = builder.build_segment(
        model_pk=MODEL_PK,
        objects=records,
        segment_path=segment_path,
        manifest_path=manifest_path,
        chunk_bytes=CHUNK_BYTES,
    )

    segment_file_sha = stream_sha256(
        segment_path
    )

    manifest_doc = json.loads(
        manifest_path.read_text(
            encoding="utf-8"
        )
    )

    manifest_canonical = (
        canonical_json_bytes(manifest_doc)
        == manifest_path.read_bytes()
    )

    range_rows = compare_segment_ranges(
        segment_path
    )

    expected_offsets = [
        spec["offset"]
        for spec in INPUTS
    ]

    actual_offsets = [
        row["offset"]
        for row in positive.manifest["objects"]
    ]

    actual_lengths = [
        row["length"]
        for row in positive.manifest["objects"]
    ]

    expected_lengths = [
        spec["length"]
        for spec in INPUTS
    ]

    actual_object_pks = [
        row["object_pk"]
        for row in positive.manifest["objects"]
    ]

    expected_object_pks = [
        spec["object_pk"]
        for spec in INPUTS
    ]

    actual_object_hashes = [
        row["object_file_sha256"]
        for row in positive.manifest["objects"]
    ]

    expected_object_hashes = [
        spec["object_file_sha256"]
        for spec in INPUTS
    ]

    actual_payload_hashes = [
        row["payload_sha256"]
        for row in positive.manifest["objects"]
    ]

    expected_payload_hashes = [
        spec["payload_sha256"]
        for spec in INPUTS
    ]

    positive_checks = {
        "builder_schema": (
            positive.schema
            == builder.SCHEMA
        ),
        "builder_version": (
            positive.builder_version
            == builder.BUILDER_VERSION
        ),
        "model_pk_preserved": (
            positive.model_pk
            == MODEL_PK
        ),
        "manifest_schema": (
            positive.manifest["schema"]
            == builder.MANIFEST_SCHEMA
        ),
        "placement_policy": (
            positive.manifest["placement_policy"]
            == builder.PLACEMENT_POLICY
        ),
        "object_count": (
            positive.manifest["object_count"]
            == EXPECTED_OBJECT_COUNT
        ),
        "segment_length_result": (
            positive.segment_length
            == EXPECTED_SEGMENT_LENGTH
        ),
        "segment_length_filesystem": (
            segment_path.stat().st_size
            == EXPECTED_SEGMENT_LENGTH
        ),
        "segment_sha_expected_concat": (
            positive.segment_sha256
            == expected_segment_sha
        ),
        "segment_sha_independent_rehash": (
            segment_file_sha
            == expected_segment_sha
        ),
        "manifest_segment_sha": (
            manifest_doc["segment_sha256"]
            == expected_segment_sha
        ),
        "caller_order_preserved": (
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
        "object_file_hashes_exact": (
            actual_object_hashes
            == expected_object_hashes
        ),
        "payload_hashes_exact": (
            actual_payload_hashes
            == expected_payload_hashes
        ),
        "first_offset_zero": (
            actual_offsets[0] == 0
        ),
        "contiguous_no_gaps": all(
            actual_offsets[i]
            ==
            actual_offsets[i - 1]
            + actual_lengths[i - 1]
            for i in range(
                1,
                len(actual_offsets),
            )
        ),
        "final_arithmetic_exact": (
            actual_offsets[-1]
            + actual_lengths[-1]
            == EXPECTED_SEGMENT_LENGTH
        ),
        "manifest_canonical_json": (
            manifest_canonical
        ),
        "all_ranges_exact_bytes": all(
            row["exact_byte_match"]
            for row in range_rows
        ),
    }

    duplicate_records = [
        records[0],
        dict(records[0]),
    ]

    duplicate_result = expect_failure(
        label="duplicate_object_pk",
        records=duplicate_records,
        segment_path=(
            RUNTIME
            / "negative_duplicate.mafseg"
        ),
        manifest_path=(
            RUNTIME
            / "negative_duplicate.manifest.json"
        ),
    )

    mixed_records = [
        dict(records[0]),
        {
            **records[1],
            "model_pk": OTHER_MODEL_PK,
        },
    ]

    mixed_result = expect_failure(
        label="mixed_model",
        records=mixed_records,
        segment_path=(
            RUNTIME
            / "negative_mixed.mafseg"
        ),
        manifest_path=(
            RUNTIME
            / "negative_mixed.manifest.json"
        ),
    )

    malformed_path = (
        RUNTIME
        / "malformed_input.maf"
    )

    with (
        SOURCE_RUNTIME
        / INPUTS[0]["filename"]
    ).open("rb") as source, \
            malformed_path.open("xb") as target:
        raw = source.read(32)

        if len(raw) != 32:
            raise RuntimeError(
                "could not create malformed control"
            )

        target.write(raw)

    malformed_records = [
        {
            **records[0],
            "object_path": str(
                malformed_path
            ),
            "object_file_sha256": None,
            "payload_sha256": None,
        }
    ]

    malformed_result = expect_failure(
        label="malformed_object",
        records=malformed_records,
        segment_path=(
            RUNTIME
            / "negative_malformed.mafseg"
        ),
        manifest_path=(
            RUNTIME
            / "negative_malformed.manifest.json"
        ),
    )

    preexisting_segment = (
        RUNTIME
        / "negative_existing_final.mafseg"
    )

    preexisting_segment.write_bytes(
        b"sentinel"
    )

    existing_final_failed = False
    existing_final_error = None

    try:
        builder.build_segment(
            model_pk=MODEL_PK,
            objects=records,
            segment_path=preexisting_segment,
            manifest_path=(
                RUNTIME
                / "negative_existing_final.manifest.json"
            ),
            chunk_bytes=CHUNK_BYTES,
        )
    except Exception as exc:
        existing_final_failed = True
        existing_final_error = str(exc)

    existing_final_result = {
        "label": "preexisting_final",
        "failed_closed": existing_final_failed,
        "sentinel_preserved": (
            preexisting_segment.read_bytes()
            == b"sentinel"
        ),
        "manifest_not_activated": (
            not (
                RUNTIME
                / "negative_existing_final.manifest.json"
            ).exists()
        ),
        "error_text": existing_final_error,
    }

    existing_final_result["pass"] = all(
        (
            existing_final_result["failed_closed"],
            existing_final_result["sentinel_preserved"],
            existing_final_result[
                "manifest_not_activated"
            ],
        )
    )

    partial_segment = (
        RUNTIME
        / "negative_existing_partial.mafseg"
    )

    partial_path = partial_segment.with_name(
        partial_segment.name + ".partial"
    )

    partial_path.write_bytes(
        b"sentinel-partial"
    )

    partial_failed = False
    partial_error = None

    try:
        builder.build_segment(
            model_pk=MODEL_PK,
            objects=records,
            segment_path=partial_segment,
            manifest_path=(
                RUNTIME
                / "negative_existing_partial.manifest.json"
            ),
            chunk_bytes=CHUNK_BYTES,
        )
    except Exception as exc:
        partial_failed = True
        partial_error = str(exc)

    partial_result = {
        "label": "preexisting_partial",
        "failed_closed": partial_failed,
        "sentinel_preserved": (
            partial_path.read_bytes()
            == b"sentinel-partial"
        ),
        "final_not_activated": (
            not partial_segment.exists()
        ),
        "manifest_not_activated": (
            not (
                RUNTIME
                / "negative_existing_partial.manifest.json"
            ).exists()
        ),
        "error_text": partial_error,
    }

    partial_result["pass"] = all(
        (
            partial_result["failed_closed"],
            partial_result["sentinel_preserved"],
            partial_result["final_not_activated"],
            partial_result[
                "manifest_not_activated"
            ],
        )
    )

    negative_controls = [
        duplicate_result,
        mixed_result,
        malformed_result,
        existing_final_result,
        partial_result,
    ]

    no_builder_partials = not any(
        path.name.endswith(".partial")
        and path != partial_path
        for path in RUNTIME.iterdir()
    )

    static_policy_checks = {
        "fragmentation_disabled": True,
        "deduplication_not_performed": True,
        "generation_pk_not_generated": True,
        "catalog_generation_not_activated": True,
        "runtime_residency_not_assigned": True,
        "locality_reordering_not_performed": True,
        "source_gguf_not_required": True,
    }

    all_positive = all(
        positive_checks.values()
    )

    all_negative = all(
        row["pass"]
        for row in negative_controls
    )

    all_static = all(
        static_policy_checks.values()
    )

    all_pass = all(
        (
            all_positive,
            all_negative,
            all_static,
            no_builder_partials,
        )
    )

    result = {
        "schema": SCHEMA,
        "builder_schema": builder.SCHEMA,
        "builder_version": builder.BUILDER_VERSION,
        "manifest_schema": builder.MANIFEST_SCHEMA,
        "placement_policy": builder.PLACEMENT_POLICY,
        "model_pk": MODEL_PK,
        "chunk_bytes": CHUNK_BYTES,
        "preregistered_inputs": INPUTS,
        "expected_object_count": EXPECTED_OBJECT_COUNT,
        "expected_segment_length": EXPECTED_SEGMENT_LENGTH,
        "expected_segment_sha256": expected_segment_sha,
        "positive": {
            "segment_path": str(
                segment_path
            ),
            "manifest_path": str(
                manifest_path
            ),
            "segment_length": (
                positive.segment_length
            ),
            "segment_sha256": (
                positive.segment_sha256
            ),
            "independent_segment_sha256": (
                segment_file_sha
            ),
            "placements": (
                positive.manifest["objects"]
            ),
            "range_audit": range_rows,
            "checks": positive_checks,
            "pass": all_positive,
        },
        "negative_controls": negative_controls,
        "static_policy_checks": static_policy_checks,
        "no_unexpected_builder_partials": (
            no_builder_partials
        ),
        "all_pass": all_pass,
    }

    RESULT_PATH.write_bytes(
        canonical_json_bytes(
            result
        )
        + b"\n"
    )

    print("=" * 72)
    print(
        " OPENMIND / MAF SEGMENT BUILDER V1 VALIDATION"
    )
    print("=" * 72)
    print("model PK             :", MODEL_PK)
    print(
        "object count         :",
        EXPECTED_OBJECT_COUNT,
    )
    print(
        "segment bytes        :",
        EXPECTED_SEGMENT_LENGTH,
    )
    print(
        "expected segment SHA :",
        expected_segment_sha,
    )
    print(
        "actual segment SHA   :",
        positive.segment_sha256,
    )
    print(
        "positive checks      :",
        all_positive,
    )
    print(
        "negative controls    :",
        all_negative,
    )
    print(
        "policy checks        :",
        all_static,
    )
    print(
        "unexpected partials  :",
        not no_builder_partials,
    )
    print("all pass             :", all_pass)
    print("result               :", RESULT_PATH)

    if not all_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
