#!/usr/bin/env python3

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from maf_object_v1 import (
    DEFAULT_CHUNK_BYTES,
    ObjectView,
    compile_object,
)


SCHEMA = "openmind.maf_encoder.v1"
ENCODER_VERSION = "maf_encoder_v1"

RECIPE_SCHEMA = "openmind.maf_compile_recipe.v1"

MODEL_PK_RE = re.compile(
    r"^mafmodel:v1:[0-9a-f]{64}$"
)

OBJECT_PK_RE = re.compile(
    r"^mafobj:v1:[0-9a-f]{64}$"
)

SHA256_RE = re.compile(
    r"^[0-9a-f]{64}$"
)

EXPECTED_UNRESOLVED = (
    "deduplication",
    "structural_optimization",
    "segment_placement",
    "runtime_residency",
    "maf_native_compute",
)

EXPECTED_POLICY = {
    "source_encoding":
        "gguf_payload_exact",
    "target_representation":
        "persistent_maf_object_exact",
    "fidelity_requirement":
        "exact",
    "payload_access":
        "deferred_to_encoder",
    "payload_passes":
        1,
    "hash_policy":
        "sha256_stream_required",
    "transform_policy":
        "none",
    "compression_policy":
        "none",
    "deduplication_policy":
        "unresolved",
    "fragmentation_policy":
        "none",
    "dense_materialization_policy":
        "optional_compute_view",
    "segment_placement_policy":
        "unresolved",
    "runtime_residency_policy":
        "unresolved",
    "maf_native_compute_policy":
        "disabled_unvalidated",
}


class MAFEncoderError(RuntimeError):
    pass


@dataclass(frozen=True)
class EncoderResult:
    schema: str
    encoder_version: str
    model_pk: str
    object_pk: str
    object_view: ObjectView


def _require_dict(
    value: Any,
    label: str,
) -> dict:
    if not isinstance(value, dict):
        raise MAFEncoderError(
            f"{label} must be a dict"
        )

    return value


def _require_nonempty_text(
    value: Any,
    label: str,
) -> str:
    if (
        not isinstance(value, str)
        or not value
    ):
        raise MAFEncoderError(
            f"{label} must be non-empty text"
        )

    return value


def _require_int(
    value: Any,
    label: str,
    *,
    minimum: int | None = None,
) -> int:
    if (
        not isinstance(value, int)
        or isinstance(value, bool)
    ):
        raise MAFEncoderError(
            f"{label} must be an integer"
        )

    if (
        minimum is not None
        and value < minimum
    ):
        raise MAFEncoderError(
            f"{label} must be >= {minimum}"
        )

    return value


def _normalize_dims(
    value: Any,
    label: str,
) -> tuple[int, ...]:
    if not isinstance(
        value,
        (list, tuple),
    ):
        raise MAFEncoderError(
            f"{label} must be a list or tuple"
        )

    if not value:
        raise MAFEncoderError(
            f"{label} must not be empty"
        )

    dims = tuple(
        _require_int(
            item,
            f"{label}[{index}]",
            minimum=1,
        )
        for index, item in enumerate(value)
    )

    return dims


def _element_count(
    dims: tuple[int, ...],
) -> int:
    count = 1

    for dim in dims:
        count *= dim

    return count


def _validate_model_pk(
    value: Any,
) -> str:
    value = _require_nonempty_text(
        value,
        "model_pk",
    )

    if MODEL_PK_RE.fullmatch(value) is None:
        raise MAFEncoderError(
            "invalid model PK"
        )

    return value


def _validate_object_pk(
    value: Any,
) -> str:
    value = _require_nonempty_text(
        value,
        "object_pk",
    )

    if OBJECT_PK_RE.fullmatch(value) is None:
        raise MAFEncoderError(
            "invalid object PK"
        )

    return value


def _validate_sha256(
    value: Any,
    label: str,
) -> str:
    value = _require_nonempty_text(
        value,
        label,
    )

    if SHA256_RE.fullmatch(value) is None:
        raise MAFEncoderError(
            f"invalid {label}"
        )

    return value


def validate_recipe(
    recipe: dict,
) -> dict:
    recipe = _require_dict(
        recipe,
        "recipe",
    )

    if recipe.get("schema") != RECIPE_SCHEMA:
        raise MAFEncoderError(
            "unsupported recipe schema"
        )

    model_pk = _validate_model_pk(
        recipe.get("model_pk")
    )

    object_pk = _validate_object_pk(
        recipe.get("object_pk")
    )

    name = _require_nonempty_text(
        recipe.get("name"),
        "recipe name",
    )

    tensor_type = _require_nonempty_text(
        recipe.get("tensor_type"),
        "recipe tensor_type",
    )

    dims = _normalize_dims(
        recipe.get("dims"),
        "recipe dims",
    )

    elements = _require_int(
        recipe.get("elements"),
        "recipe elements",
        minimum=1,
    )

    if elements != _element_count(dims):
        raise MAFEncoderError(
            "recipe element count mismatch"
        )

    for field, expected in (
        EXPECTED_POLICY.items()
    ):
        actual = recipe.get(field)

        if actual != expected:
            raise MAFEncoderError(
                "unsupported recipe policy: "
                f"{field}={actual!r}"
            )

    unresolved = recipe.get(
        "unresolved"
    )

    if not isinstance(
        unresolved,
        (list, tuple),
    ):
        raise MAFEncoderError(
            "recipe unresolved must be a list"
        )

    if tuple(unresolved) != EXPECTED_UNRESOLVED:
        raise MAFEncoderError(
            "recipe unresolved list mismatch"
        )

    return {
        "model_pk": model_pk,
        "object_pk": object_pk,
        "name": name,
        "tensor_type": tensor_type,
        "dims": dims,
        "elements": elements,
    }


def validate_physical_record(
    physical: dict,
) -> dict:
    physical = _require_dict(
        physical,
        "physical record",
    )

    name = _require_nonempty_text(
        physical.get("name"),
        "physical name",
    )

    tensor_type = _require_nonempty_text(
        physical.get("type"),
        "physical type",
    )

    dims = _normalize_dims(
        physical.get("dims"),
        "physical dims",
    )

    elements = _require_int(
        physical.get("elements"),
        "physical elements",
        minimum=1,
    )

    if elements != _element_count(dims):
        raise MAFEncoderError(
            "physical element count mismatch"
        )

    file_start = _require_int(
        physical.get("file_start"),
        "physical file_start",
        minimum=0,
    )

    span_bytes = _require_int(
        physical.get("span_bytes"),
        "physical span_bytes",
        minimum=0,
    )

    payload_sha256 = _validate_sha256(
        physical.get("payload_sha256"),
        "physical payload_sha256",
    )

    return {
        "name": name,
        "tensor_type": tensor_type,
        "dims": dims,
        "elements": elements,
        "file_start": file_start,
        "span_bytes": span_bytes,
        "payload_sha256": payload_sha256,
    }


def validate_agreement(
    recipe: dict,
    physical: dict,
) -> None:
    comparisons = (
        (
            "name",
            recipe["name"],
            physical["name"],
        ),
        (
            "tensor_type",
            recipe["tensor_type"],
            physical["tensor_type"],
        ),
        (
            "dims",
            recipe["dims"],
            physical["dims"],
        ),
        (
            "elements",
            recipe["elements"],
            physical["elements"],
        ),
    )

    for (
        field,
        recipe_value,
        physical_value,
    ) in comparisons:
        if recipe_value != physical_value:
            raise MAFEncoderError(
                "recipe/physical metadata "
                f"disagreement: {field}"
            )


def build_provenance(
    *,
    model_pk: str,
    object_pk: str,
    recipe: dict,
) -> dict:
    planner_version = (
        recipe.get("planner_version")
    )

    if not isinstance(
        planner_version,
        str,
    ) or not planner_version:
        raise MAFEncoderError(
            "missing planner version"
        )

    return {
        "model_pk": model_pk,
        "object_pk": object_pk,
        "recipe_schema": RECIPE_SCHEMA,
        "planner_version": planner_version,
        "encoder_schema": SCHEMA,
        "encoder_version": ENCODER_VERSION,
    }


def encode_object(
    *,
    recipe: dict,
    physical_record: dict,
    source_path: Path,
    output_path: Path,
    chunk_bytes: int = DEFAULT_CHUNK_BYTES,
) -> EncoderResult:
    """
    Execute one frozen MAF compile recipe.

    All recipe and physical metadata validation occurs before
    compile_object() is invoked. compile_object() owns the
    source-payload stream, SHA256 update, bounded copy, partial
    persistence, independent object reopen, and atomic activation.
    """

    if (
        not isinstance(chunk_bytes, int)
        or isinstance(chunk_bytes, bool)
        or chunk_bytes <= 0
    ):
        raise MAFEncoderError(
            "chunk_bytes must be a positive integer"
        )

    recipe_valid = validate_recipe(
        recipe
    )

    physical_valid = (
        validate_physical_record(
            physical_record
        )
    )

    validate_agreement(
        recipe_valid,
        physical_valid,
    )

    provenance = build_provenance(
        model_pk=recipe_valid["model_pk"],
        object_pk=recipe_valid["object_pk"],
        recipe=recipe,
    )

    view = compile_object(
        source_path=Path(source_path),
        source_file_start=(
            physical_valid["file_start"]
        ),
        tensor_name=recipe_valid["name"],
        tensor_type=(
            recipe_valid["tensor_type"]
        ),
        dims=recipe_valid["dims"],
        payload_length=(
            physical_valid["span_bytes"]
        ),
        expected_payload_sha256=(
            physical_valid[
                "payload_sha256"
            ]
        ),
        output_path=Path(output_path),
        provenance=provenance,
        chunk_bytes=chunk_bytes,
    )

    return EncoderResult(
        schema=SCHEMA,
        encoder_version=ENCODER_VERSION,
        model_pk=recipe_valid["model_pk"],
        object_pk=recipe_valid["object_pk"],
        object_view=view,
    )
