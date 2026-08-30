#!/usr/bin/env python3

"""Deterministic metadata-only MAF object classification.

This module implements the frozen
MAF_METADATA_CLASSIFICATION_V1_PROTOCOL.md contract.

It performs no GGUF payload access and no filesystem I/O.
"""

from __future__ import annotations

import re
from typing import Any, Iterable


SCHEMA = "openmind.maf_metadata_classification.v1"

UNKNOWN = "unknown"

_BLOCK_RE = re.compile(
    r"^blk\.(0|[1-9][0-9]*)\.(.+)$"
)

_MODEL_COMPONENTS = {
    "token_embd.weight": "token_embd",
    "output.weight": "output",
    "output_norm.weight": "output_norm",
}

_MODEL_SEMANTIC = {
    "token_embd.weight": "embedding",
    "output.weight": "output_projection",
    "output_norm.weight": "normalization",
}

_BLOCK_SEMANTIC = {
    "attn_norm.weight": "normalization",
    "ffn_norm.weight": "normalization",
    "attn_q.weight": "attention_query_weight",
    "attn_k.weight": "attention_key_weight",
    "attn_v.weight": "attention_value_weight",
    "attn_output.weight": "attention_output_weight",
    "attn_q.bias": "attention_query_bias",
    "attn_k.bias": "attention_key_bias",
    "attn_v.bias": "attention_value_bias",
    "ffn_gate.weight": "ffn_gate_weight",
    "ffn_up.weight": "ffn_up_weight",
    "ffn_down.weight": "ffn_down_weight",
}

_ALLOWED_INPUT_FIELDS = frozenset(
    {
        "name",
        "type",
        "dims",
        "elements",
    }
)


class MAFMetadataClassificationError(ValueError):
    """Raised when logical metadata violates the v1 contract."""


def _require_nonempty_text(
    value: Any,
    field: str,
) -> str:
    if not isinstance(value, str):
        raise MAFMetadataClassificationError(
            f"{field} must be text"
        )

    if value == "":
        raise MAFMetadataClassificationError(
            f"{field} must not be empty"
        )

    return value


def _require_dims(value: Any) -> list[int]:
    if not isinstance(value, (list, tuple)):
        raise MAFMetadataClassificationError(
            "dims must be a list or tuple"
        )

    if len(value) == 0:
        raise MAFMetadataClassificationError(
            "dims must not be empty"
        )

    dims: list[int] = []

    for item in value:
        if (
            not isinstance(item, int)
            or isinstance(item, bool)
            or item <= 0
        ):
            raise MAFMetadataClassificationError(
                "dims must contain positive integers"
            )

        dims.append(item)

    return dims


def _require_elements(value: Any) -> int:
    if (
        not isinstance(value, int)
        or isinstance(value, bool)
        or value <= 0
    ):
        raise MAFMetadataClassificationError(
            "elements must be a positive integer"
        )

    return value


def _validate_elements(
    dims: list[int],
    elements: int,
) -> None:
    product = 1

    for dim in dims:
        product *= dim

    if product != elements:
        raise MAFMetadataClassificationError(
            "elements must equal product(dims)"
        )


def parse_name(
    name: str,
) -> tuple[int | None, str]:
    name = _require_nonempty_text(
        name,
        "name",
    )

    match = _BLOCK_RE.fullmatch(name)

    if match is not None:
        layer_index = int(match.group(1))
        component = match.group(2)

        if component == "":
            raise MAFMetadataClassificationError(
                "block component must not be empty"
            )

        return layer_index, component

    if name.startswith("blk."):
        raise MAFMetadataClassificationError(
            "malformed block tensor name"
        )

    component = _MODEL_COMPONENTS.get(
        name,
        name,
    )

    return None, component


def parameter_kind(name: str) -> str:
    name = _require_nonempty_text(
        name,
        "name",
    )

    if name.endswith(".weight"):
        return "weight"

    if name.endswith(".bias"):
        return "bias"

    return UNKNOWN


def semantic_class(
    name: str,
    layer_index: int | None,
    component: str,
) -> str:
    if layer_index is None:
        return _MODEL_SEMANTIC.get(
            name,
            UNKNOWN,
        )

    return _BLOCK_SEMANTIC.get(
        component,
        UNKNOWN,
    )


def classify_metadata(
    metadata: dict[str, Any],
) -> dict[str, Any]:
    if not isinstance(metadata, dict):
        raise MAFMetadataClassificationError(
            "metadata must be a dict"
        )

    missing = (
        _ALLOWED_INPUT_FIELDS
        - metadata.keys()
    )

    if missing:
        raise MAFMetadataClassificationError(
            "missing required fields: "
            + ", ".join(sorted(missing))
        )

    name = _require_nonempty_text(
        metadata["name"],
        "name",
    )

    tensor_type = _require_nonempty_text(
        metadata["type"],
        "type",
    )

    dims = _require_dims(
        metadata["dims"]
    )

    elements = _require_elements(
        metadata["elements"]
    )

    _validate_elements(
        dims,
        elements,
    )

    layer_index, component = parse_name(
        name
    )

    kind = parameter_kind(
        name
    )

    semantic = semantic_class(
        name,
        layer_index,
        component,
    )

    return {
        "schema": SCHEMA,
        "name": name,
        "layer_index": layer_index,
        "component": component,
        "parameter_kind": kind,
        "semantic_class": semantic,
        "structural_class": UNKNOWN,
        "runtime_class": UNKNOWN,
        "tensor_type": tensor_type,
        "rank": len(dims),
        "dims": dims,
        "elements": elements,
        "classification_basis": [
            "name",
            "type",
            "dims",
            "elements",
        ],
    }


def classify_many(
    records: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    names: set[str] = set()

    for metadata in records:
        record = classify_metadata(
            metadata
        )

        name = record["name"]

        if name in names:
            raise MAFMetadataClassificationError(
                f"duplicate tensor name: {name}"
            )

        names.add(name)
        output.append(record)

    return output


__all__ = [
    "MAFMetadataClassificationError",
    "SCHEMA",
    "UNKNOWN",
    "classify_many",
    "classify_metadata",
    "parameter_kind",
    "parse_name",
    "semantic_class",
]
