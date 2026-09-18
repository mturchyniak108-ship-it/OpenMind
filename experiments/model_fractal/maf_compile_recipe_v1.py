#!/usr/bin/env python3

"""Deterministic pre-payload MAF compile recipe planner v1.

This module implements the frozen
MAF_COMPILE_RECIPE_V1_PROTOCOL.md contract.

It performs no filesystem I/O, GGUF access, payload hashing,
encoding, fragmentation, segment placement, or residency work.
"""

from __future__ import annotations

from typing import Any, Iterable


SCHEMA = "openmind.maf_compile_recipe.v1"
PLANNER_VERSION = "maf_planner_v1"

CLASSIFIER_SCHEMA = (
    "openmind.maf_metadata_classification.v1"
)

SOURCE_ENCODING = "gguf_payload_exact"
TARGET_REPRESENTATION = "persistent_maf_object_exact"
FIDELITY_REQUIREMENT = "exact"
PAYLOAD_ACCESS = "deferred_to_encoder"
PAYLOAD_PASSES = 1
HASH_POLICY = "sha256_stream_required"
TRANSFORM_POLICY = "none"
COMPRESSION_POLICY = "none"
DEDUPLICATION_POLICY = "unresolved"
FRAGMENTATION_POLICY = "none"
DENSE_MATERIALIZATION_POLICY = "optional_compute_view"
SEGMENT_PLACEMENT_POLICY = "unresolved"
RUNTIME_RESIDENCY_POLICY = "unresolved"
MAF_NATIVE_COMPUTE_POLICY = "disabled_unvalidated"

UNRESOLVED = (
    "deduplication",
    "structural_optimization",
    "segment_placement",
    "runtime_residency",
    "maf_native_compute",
)

_REQUIRED_CLASSIFICATION_FIELDS = frozenset(
    {
        "schema",
        "name",
        "layer_index",
        "component",
        "parameter_kind",
        "semantic_class",
        "structural_class",
        "runtime_class",
        "tensor_type",
        "rank",
        "dims",
        "elements",
        "classification_basis",
    }
)


class MAFCompileRecipeError(ValueError):
    """Raised when planner input violates the v1 contract."""


def _require_text(
    value: Any,
    field: str,
) -> str:
    if not isinstance(value, str):
        raise MAFCompileRecipeError(
            f"{field} must be text"
        )

    if value == "":
        raise MAFCompileRecipeError(
            f"{field} must not be empty"
        )

    return value


def _require_pk(
    value: Any,
    field: str,
    prefix: str,
) -> str:
    value = _require_text(
        value,
        field,
    )

    if not value.startswith(prefix):
        raise MAFCompileRecipeError(
            f"{field} must use {prefix} namespace"
        )

    suffix = value[len(prefix):]

    if len(suffix) != 64:
        raise MAFCompileRecipeError(
            f"{field} digest must contain 64 hex characters"
        )

    if any(
        char not in "0123456789abcdef"
        for char in suffix
    ):
        raise MAFCompileRecipeError(
            f"{field} digest must be lowercase hexadecimal"
        )

    return value


def _require_dims(
    value: Any,
) -> list[int]:
    if not isinstance(value, (list, tuple)):
        raise MAFCompileRecipeError(
            "dims must be a list or tuple"
        )

    if not value:
        raise MAFCompileRecipeError(
            "dims must not be empty"
        )

    dims: list[int] = []

    for item in value:
        if (
            not isinstance(item, int)
            or isinstance(item, bool)
            or item <= 0
        ):
            raise MAFCompileRecipeError(
                "dims must contain positive integers"
            )

        dims.append(item)

    return dims


def _require_elements(
    value: Any,
    dims: list[int],
) -> int:
    if (
        not isinstance(value, int)
        or isinstance(value, bool)
        or value <= 0
    ):
        raise MAFCompileRecipeError(
            "elements must be a positive integer"
        )

    product = 1

    for dim in dims:
        product *= dim

    if product != value:
        raise MAFCompileRecipeError(
            "elements must equal product(dims)"
        )

    return value


def _validate_classification(
    classification: Any,
) -> dict[str, Any]:
    if not isinstance(classification, dict):
        raise MAFCompileRecipeError(
            "classification must be a dict"
        )

    missing = (
        _REQUIRED_CLASSIFICATION_FIELDS
        - classification.keys()
    )

    if missing:
        raise MAFCompileRecipeError(
            "classification missing required fields: "
            + ", ".join(sorted(missing))
        )

    if classification["schema"] != CLASSIFIER_SCHEMA:
        raise MAFCompileRecipeError(
            "unexpected classifier schema"
        )

    name = _require_text(
        classification["name"],
        "name",
    )

    tensor_type = _require_text(
        classification["tensor_type"],
        "tensor_type",
    )

    semantic_class = _require_text(
        classification["semantic_class"],
        "semantic_class",
    )

    structural_class = _require_text(
        classification["structural_class"],
        "structural_class",
    )

    runtime_class = _require_text(
        classification["runtime_class"],
        "runtime_class",
    )

    dims = _require_dims(
        classification["dims"]
    )

    elements = _require_elements(
        classification["elements"],
        dims,
    )

    rank = classification["rank"]

    if (
        not isinstance(rank, int)
        or isinstance(rank, bool)
        or rank != len(dims)
    ):
        raise MAFCompileRecipeError(
            "rank must equal len(dims)"
        )

    return {
        "name": name,
        "tensor_type": tensor_type,
        "semantic_class": semantic_class,
        "structural_class": structural_class,
        "runtime_class": runtime_class,
        "dims": dims,
        "elements": elements,
    }


def build_recipe(
    *,
    model_pk: str,
    object_pk: str,
    classification: dict[str, Any],
) -> dict[str, Any]:
    model_pk = _require_pk(
        model_pk,
        "model_pk",
        "mafmodel:v1:",
    )

    object_pk = _require_pk(
        object_pk,
        "object_pk",
        "mafobj:v1:",
    )

    normalized = _validate_classification(
        classification
    )

    planning_basis = {
        "classifier_schema": CLASSIFIER_SCHEMA,
        "planner_schema": SCHEMA,
        "planner_version": PLANNER_VERSION,
        "model_pk": model_pk,
        "object_pk": object_pk,
        "tensor_metadata": {
            "name": normalized["name"],
            "tensor_type": normalized["tensor_type"],
            "dims": list(normalized["dims"]),
            "elements": normalized["elements"],
        },
        "semantic_class": normalized["semantic_class"],
        "structural_class": normalized["structural_class"],
        "runtime_class": normalized["runtime_class"],
    }

    return {
        "schema": SCHEMA,
        "planner_version": PLANNER_VERSION,
        "model_pk": model_pk,
        "object_pk": object_pk,
        "name": normalized["name"],
        "tensor_type": normalized["tensor_type"],
        "dims": list(normalized["dims"]),
        "elements": normalized["elements"],
        "semantic_class": normalized["semantic_class"],
        "structural_class": normalized["structural_class"],
        "runtime_class": normalized["runtime_class"],
        "source_encoding": SOURCE_ENCODING,
        "target_representation": TARGET_REPRESENTATION,
        "fidelity_requirement": FIDELITY_REQUIREMENT,
        "payload_access": PAYLOAD_ACCESS,
        "payload_passes": PAYLOAD_PASSES,
        "hash_policy": HASH_POLICY,
        "transform_policy": TRANSFORM_POLICY,
        "compression_policy": COMPRESSION_POLICY,
        "deduplication_policy": DEDUPLICATION_POLICY,
        "fragmentation_policy": FRAGMENTATION_POLICY,
        "dense_materialization_policy":
            DENSE_MATERIALIZATION_POLICY,
        "segment_placement_policy":
            SEGMENT_PLACEMENT_POLICY,
        "runtime_residency_policy":
            RUNTIME_RESIDENCY_POLICY,
        "maf_native_compute_policy":
            MAF_NATIVE_COMPUTE_POLICY,
        "unresolved": list(UNRESOLVED),
        "planning_basis": planning_basis,
    }


def build_many(
    records: Iterable[
        tuple[
            str,
            str,
            dict[str, Any],
        ]
    ],
) -> list[dict[str, Any]]:
    recipes: list[dict[str, Any]] = []
    object_pks: set[str] = set()

    for (
        model_pk,
        object_pk,
        classification,
    ) in records:
        recipe = build_recipe(
            model_pk=model_pk,
            object_pk=object_pk,
            classification=classification,
        )

        if recipe["object_pk"] in object_pks:
            raise MAFCompileRecipeError(
                "duplicate object_pk"
            )

        object_pks.add(
            recipe["object_pk"]
        )

        recipes.append(
            recipe
        )

    return recipes


__all__ = [
    "CLASSIFIER_SCHEMA",
    "COMPRESSION_POLICY",
    "DEDUPLICATION_POLICY",
    "DENSE_MATERIALIZATION_POLICY",
    "FIDELITY_REQUIREMENT",
    "FRAGMENTATION_POLICY",
    "HASH_POLICY",
    "MAFCompileRecipeError",
    "MAF_NATIVE_COMPUTE_POLICY",
    "PAYLOAD_ACCESS",
    "PAYLOAD_PASSES",
    "PLANNER_VERSION",
    "RUNTIME_RESIDENCY_POLICY",
    "SCHEMA",
    "SEGMENT_PLACEMENT_POLICY",
    "SOURCE_ENCODING",
    "TARGET_REPRESENTATION",
    "TRANSFORM_POLICY",
    "UNRESOLVED",
    "build_many",
    "build_recipe",
]
