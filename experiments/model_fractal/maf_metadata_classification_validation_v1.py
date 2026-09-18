#!/usr/bin/env python3

"""Validate MAF metadata-only classification over the frozen Qwen inventory."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

import maf_metadata_classification_v1 as classifier


BASE = Path(__file__).resolve().parent

PROTOCOL = BASE / "MAF_METADATA_CLASSIFICATION_V1_PROTOCOL.md"
ENGINE = BASE / "maf_metadata_classification_v1.py"
INVENTORY = BASE / "gguf_tensor_inventory_v1.json"

RESULT = BASE / "maf_metadata_classification_validation_v1.json"
PARTIAL = Path(str(RESULT) + ".partial")

SCHEMA = "openmind.maf_metadata_classification_validation.v1"

EXPECTED_PROTOCOL_SHA256 = (
    "4630cad87dd852c6597ed695b18b90eb747c7fb9ed043c4cd55ceef8337f1c96"
)

EXPECTED_ENGINE_SHA256 = (
    "7ed816edd955b3df4d7b029a879f95c5318dfea3724e32fc847d3b663299f78a"
)

EXPECTED_INVENTORY_SHA256 = (
    "7acf6d5dc672182aee0244b1bb85a47466f33dbdcdf10bde863e24f3659240ee"
)

PHYSICAL_FIELDS = (
    "file_start",
    "offset",
    "payload_sha256",
    "span_bytes",
    "validation",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        while True:
            block = handle.read(1024 * 1024)

            if not block:
                break

            digest.update(block)

    return digest.hexdigest()


def require_frozen_inputs() -> None:
    expected = {
        PROTOCOL: EXPECTED_PROTOCOL_SHA256,
        ENGINE: EXPECTED_ENGINE_SHA256,
        INVENTORY: EXPECTED_INVENTORY_SHA256,
    }

    for path, expected_sha in expected.items():
        actual = sha256_file(path)

        if actual != expected_sha:
            raise RuntimeError(
                f"frozen prerequisite SHA mismatch: {path.name}: "
                f"{actual} != {expected_sha}"
            )


def logical_metadata(
    tensor: dict[str, Any],
) -> dict[str, Any]:
    return {
        "name": tensor["name"],
        "type": tensor["type"],
        "dims": tensor["dims"],
        "elements": tensor["elements"],
    }


def classification_map(
    rows: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    return {
        row["name"]: row
        for row in rows
    }


def validate_inventory_shape(
    tensors: list[dict[str, Any]],
) -> None:
    if len(tensors) != 339:
        raise RuntimeError(
            f"expected 339 tensors, got {len(tensors)}"
        )

    names = [
        tensor["name"]
        for tensor in tensors
    ]

    if len(set(names)) != 339:
        raise RuntimeError(
            "expected 339 unique tensor names"
        )


def build_physical_variants(
    tensors: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    variants: list[dict[str, Any]] = []

    for index, tensor in enumerate(tensors):
        row = dict(tensor)

        row["file_start"] = 10_000_000 + index
        row["offset"] = 20_000_000 + index
        row["payload_sha256"] = (
            f"{index:064x}"[-64:]
        )
        row["span_bytes"] = 30_000_000 + index
        row["validation"] = {
            "synthetic": True,
            "index": index,
        }

        variants.append(row)

    return variants


def classify_inventory(
    tensors: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return classifier.classify_many(
        logical_metadata(tensor)
        for tensor in tensors
    )


def main() -> int:
    require_frozen_inputs()

    if RESULT.exists():
        raise RuntimeError(
            f"refusing to overwrite existing result: {RESULT}"
        )

    if PARTIAL.exists():
        raise RuntimeError(
            f"partial result already exists: {PARTIAL}"
        )

    inventory_data = json.loads(
        INVENTORY.read_text()
    )

    tensors = inventory_data["tensors"]

    validate_inventory_shape(
        tensors
    )

    baseline = classify_inventory(
        tensors
    )

    repeated = classify_inventory(
        tensors
    )

    reversed_rows = classify_inventory(
        list(reversed(tensors))
    )

    physical_variants = build_physical_variants(
        tensors
    )

    physical_classified = classifier.classify_many(
        physical_variants
    )

    baseline_map = classification_map(
        baseline
    )

    repeated_map = classification_map(
        repeated
    )

    reversed_map = classification_map(
        reversed_rows
    )

    physical_map = classification_map(
        physical_classified
    )

    semantic_counts = Counter(
        row["semantic_class"]
        for row in baseline
    )

    structural_counts = Counter(
        row["structural_class"]
        for row in baseline
    )

    runtime_counts = Counter(
        row["runtime_class"]
        for row in baseline
    )

    parameter_kind_counts = Counter(
        row["parameter_kind"]
        for row in baseline
    )

    tensor_type_counts = Counter(
        row["tensor_type"]
        for row in baseline
    )

    rank_counts = Counter(
        str(row["rank"])
        for row in baseline
    )

    baseline_output_count = len(
        baseline
    )

    unique_output_names = (
        len(baseline_map)
    )

    repeated_equal = (
        baseline == repeated
    )

    order_independent = (
        baseline_map == reversed_map
    )

    physical_independent = (
        baseline_map == physical_map
    )

    all_semantically_classified = (
        semantic_counts.get(
            classifier.UNKNOWN,
            0,
        )
        == 0
    )

    structural_all_unknown = (
        structural_counts
        == Counter(
            {
                classifier.UNKNOWN: 339,
            }
        )
    )

    runtime_all_unknown = (
        runtime_counts
        == Counter(
            {
                classifier.UNKNOWN: 339,
            }
        )
    )

    repeated_map_equal = (
        baseline_map == repeated_map
    )

    schema_all_valid = all(
        row["schema"] == classifier.SCHEMA
        for row in baseline
    )

    identity_fields_present = any(
        any(
            field in row
            for field in (
                "model_pk",
                "object_pk",
                "fragment_pk",
            )
        )
        for row in baseline
    )

    result = {
        "schema": SCHEMA,
        "frozen_inputs": {
            "protocol": {
                "path": PROTOCOL.name,
                "sha256": EXPECTED_PROTOCOL_SHA256,
            },
            "engine": {
                "path": ENGINE.name,
                "sha256": EXPECTED_ENGINE_SHA256,
            },
            "inventory": {
                "path": INVENTORY.name,
                "sha256": EXPECTED_INVENTORY_SHA256,
            },
        },
        "validation_scope": {
            "inventory_tensor_count": len(tensors),
            "logical_input_fields": [
                "name",
                "type",
                "dims",
                "elements",
            ],
            "physical_control_fields": list(
                PHYSICAL_FIELDS
            ),
            "gguf_model_opened": False,
            "payload_bytes_read": False,
            "identity_generation_performed": False,
        },
        "summary": {
            "input_record_count": len(tensors),
            "output_record_count": baseline_output_count,
            "unique_output_names": unique_output_names,
            "schema_all_valid": schema_all_valid,
            "repeated_generation_equal": repeated_equal,
            "repeated_mapping_equal": repeated_map_equal,
            "input_order_independent": order_independent,
            "physical_metadata_independent": physical_independent,
            "all_semantically_classified": all_semantically_classified,
            "semantic_unknown_count": semantic_counts.get(
                classifier.UNKNOWN,
                0,
            ),
            "structural_all_unknown": structural_all_unknown,
            "runtime_all_unknown": runtime_all_unknown,
            "identity_fields_present": identity_fields_present,
            "gguf_payload_accessed": False,
            "all_pass": all(
                (
                    len(tensors) == 339,
                    baseline_output_count == 339,
                    unique_output_names == 339,
                    schema_all_valid,
                    repeated_equal,
                    repeated_map_equal,
                    order_independent,
                    physical_independent,
                    all_semantically_classified,
                    structural_all_unknown,
                    runtime_all_unknown,
                    not identity_fields_present,
                )
            ),
        },
        "counts": {
            "semantic_class": dict(
                sorted(
                    semantic_counts.items()
                )
            ),
            "structural_class": dict(
                sorted(
                    structural_counts.items()
                )
            ),
            "runtime_class": dict(
                sorted(
                    runtime_counts.items()
                )
            ),
            "parameter_kind": dict(
                sorted(
                    parameter_kind_counts.items()
                )
            ),
            "tensor_type": dict(
                sorted(
                    tensor_type_counts.items()
                )
            ),
            "rank": dict(
                sorted(
                    rank_counts.items()
                )
            ),
        },
        "classifications": baseline,
    }

    if not result["summary"]["all_pass"]:
        raise RuntimeError(
            "metadata classification validation failed"
        )

    encoded = (
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    PARTIAL.write_text(
        encoded
    )

    PARTIAL.replace(
        RESULT
    )

    summary = result["summary"]

    print(
        "input records                  :",
        summary["input_record_count"],
    )
    print(
        "output records                 :",
        summary["output_record_count"],
    )
    print(
        "unique names                   :",
        summary["unique_output_names"],
    )
    print(
        "repeat determinism             :",
        summary["repeated_generation_equal"],
    )
    print(
        "order independence             :",
        summary["input_order_independent"],
    )
    print(
        "physical metadata independence :",
        summary["physical_metadata_independent"],
    )
    print(
        "semantic unknown count         :",
        summary["semantic_unknown_count"],
    )
    print(
        "structural all unknown         :",
        summary["structural_all_unknown"],
    )
    print(
        "runtime all unknown            :",
        summary["runtime_all_unknown"],
    )
    print(
        "identity fields present        :",
        summary["identity_fields_present"],
    )
    print(
        "GGUF payload accessed          :",
        summary["gguf_payload_accessed"],
    )
    print(
        "all_pass                       :",
        summary["all_pass"],
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
