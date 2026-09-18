#!/usr/bin/env python3

"""Deterministic logical identity primitives for OpenMind MAF v1."""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any


IDENTITY_SCHEMA = "openmind.maf_identity.v1"

MODEL_SCHEMA = "openmind.maf_model_identity.v1"
OBJECT_SCHEMA = "openmind.maf_object_identity.v1"
FRAGMENT_SCHEMA = "openmind.maf_fragment_identity.v1"

MODEL_NAMESPACE = "mafmodel:v1"
OBJECT_NAMESPACE = "mafobj:v1"
FRAGMENT_NAMESPACE = "maffrag:v1"

GGUF_PAYLOAD_EXACT = "gguf_payload_exact"

_HEX64 = re.compile(r"^[0-9a-f]{64}$")


class MAFIdentityError(ValueError):
    """Raised when an identity descriptor or PK is invalid."""


def canonical_json_bytes(value: dict[str, Any]) -> bytes:
    """Return the protocol canonical UTF-8 JSON representation."""
    if not isinstance(value, dict):
        raise MAFIdentityError(
            "identity descriptor must be a dictionary"
        )

    try:
        text = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise MAFIdentityError(
            "identity descriptor is not canonical-JSON serializable"
        ) from exc

    return text.encode("utf-8")


def descriptor_sha256(
    descriptor: dict[str, Any],
) -> str:
    """Hash only the canonical descriptor bytes."""
    return hashlib.sha256(
        canonical_json_bytes(descriptor)
    ).hexdigest()


def make_pk(
    namespace: str,
    descriptor: dict[str, Any],
) -> str:
    """Construct a printable namespaced logical primary key."""
    if namespace not in {
        MODEL_NAMESPACE,
        OBJECT_NAMESPACE,
        FRAGMENT_NAMESPACE,
    }:
        raise MAFIdentityError(
            f"unsupported identity namespace: {namespace!r}"
        )

    return (
        namespace
        + ":"
        + descriptor_sha256(descriptor)
    )


def _require_text(
    field: str,
    value: Any,
) -> str:
    if not isinstance(value, str) or not value:
        raise MAFIdentityError(
            f"{field} must be a non-empty string"
        )

    return value


def _require_positive_int(
    field: str,
    value: Any,
) -> int:
    if (
        isinstance(value, bool)
        or not isinstance(value, int)
        or value <= 0
    ):
        raise MAFIdentityError(
            f"{field} must be a positive integer"
        )

    return value


def normalize_dims(
    dims: Any,
) -> list[int]:
    if not isinstance(
        dims,
        (list, tuple),
    ):
        raise MAFIdentityError(
            "dims must be a list or tuple"
        )

    if not dims:
        raise MAFIdentityError(
            "dims must not be empty"
        )

    normalized: list[int] = []

    for index, dim in enumerate(dims):
        normalized.append(
            _require_positive_int(
                f"dims[{index}]",
                dim,
            )
        )

    return normalized


def build_model_descriptor(
    *,
    architecture: str,
    model_family: str,
    model_variant: str,
    tensor_count: int,
) -> dict[str, Any]:
    """
    Build exactly the required MAF model identity v1 descriptor.

    Provenance, file paths, file hashes, offsets, and physical
    placement are intentionally absent.
    """
    return {
        "architecture":
            _require_text(
                "architecture",
                architecture,
            ),
        "model_family":
            _require_text(
                "model_family",
                model_family,
            ),
        "model_variant":
            _require_text(
                "model_variant",
                model_variant,
            ),
        "schema":
            MODEL_SCHEMA,
        "tensor_count":
            _require_positive_int(
                "tensor_count",
                tensor_count,
            ),
    }


def model_pk(
    *,
    architecture: str,
    model_family: str,
    model_variant: str,
    tensor_count: int,
) -> str:
    descriptor = build_model_descriptor(
        architecture=architecture,
        model_family=model_family,
        model_variant=model_variant,
        tensor_count=tensor_count,
    )

    return make_pk(
        MODEL_NAMESPACE,
        descriptor,
    )


def validate_pk(
    value: str,
    *,
    namespace: str | None = None,
) -> str:
    if not isinstance(value, str):
        raise MAFIdentityError(
            "PK must be a string"
        )

    if namespace is None:
        candidates = (
            MODEL_NAMESPACE,
            OBJECT_NAMESPACE,
            FRAGMENT_NAMESPACE,
        )
    else:
        if namespace not in {
            MODEL_NAMESPACE,
            OBJECT_NAMESPACE,
            FRAGMENT_NAMESPACE,
        }:
            raise MAFIdentityError(
                f"unsupported namespace: {namespace!r}"
            )

        candidates = (namespace,)

    for candidate in candidates:
        prefix = candidate + ":"

        if not value.startswith(prefix):
            continue

        digest = value[len(prefix):]

        if not _HEX64.fullmatch(digest):
            raise MAFIdentityError(
                "PK digest must be 64 lowercase hexadecimal characters"
            )

        return value

    raise MAFIdentityError(
        "PK namespace mismatch"
    )


def build_object_descriptor(
    *,
    model_pk_value: str,
    tensor_name: str,
    tensor_type: str,
    dims: Any,
    encoding: str = GGUF_PAYLOAD_EXACT,
) -> dict[str, Any]:
    """
    Build the logical MAF object identity descriptor.

    No payload hash or physical placement field participates.
    """
    validate_pk(
        model_pk_value,
        namespace=MODEL_NAMESPACE,
    )

    return {
        "dims":
            normalize_dims(dims),
        "encoding":
            _require_text(
                "encoding",
                encoding,
            ),
        "model_pk":
            model_pk_value,
        "schema":
            OBJECT_SCHEMA,
        "tensor_name":
            _require_text(
                "tensor_name",
                tensor_name,
            ),
        "tensor_type":
            _require_text(
                "tensor_type",
                tensor_type,
            ),
    }


def object_pk(
    *,
    model_pk_value: str,
    tensor_name: str,
    tensor_type: str,
    dims: Any,
    encoding: str = GGUF_PAYLOAD_EXACT,
) -> str:
    descriptor = build_object_descriptor(
        model_pk_value=model_pk_value,
        tensor_name=tensor_name,
        tensor_type=tensor_type,
        dims=dims,
        encoding=encoding,
    )

    return make_pk(
        OBJECT_NAMESPACE,
        descriptor,
    )


def build_fragment_descriptor(
    *,
    object_pk_value: str,
    fragment_scheme: str,
    logical_fragment_index: int,
    logical_range: Any,
) -> dict[str, Any]:
    """
    Build the future fragment identity descriptor.

    This function defines identity only. It does not create or
    activate fragments.
    """
    validate_pk(
        object_pk_value,
        namespace=OBJECT_NAMESPACE,
    )

    if (
        isinstance(logical_fragment_index, bool)
        or not isinstance(logical_fragment_index, int)
        or logical_fragment_index < 0
    ):
        raise MAFIdentityError(
            "logical_fragment_index must be a non-negative integer"
        )

    if (
        not isinstance(logical_range, (list, tuple))
        or len(logical_range) != 2
    ):
        raise MAFIdentityError(
            "logical_range must contain [start, end]"
        )

    start, end = logical_range

    if (
        isinstance(start, bool)
        or not isinstance(start, int)
        or start < 0
    ):
        raise MAFIdentityError(
            "logical_range start must be a non-negative integer"
        )

    if (
        isinstance(end, bool)
        or not isinstance(end, int)
        or end <= start
    ):
        raise MAFIdentityError(
            "logical_range end must be greater than start"
        )

    return {
        "fragment_scheme":
            _require_text(
                "fragment_scheme",
                fragment_scheme,
            ),
        "logical_fragment_index":
            logical_fragment_index,
        "logical_range":
            [start, end],
        "object_pk":
            object_pk_value,
        "schema":
            FRAGMENT_SCHEMA,
    }


def fragment_pk(
    *,
    object_pk_value: str,
    fragment_scheme: str,
    logical_fragment_index: int,
    logical_range: Any,
) -> str:
    descriptor = build_fragment_descriptor(
        object_pk_value=object_pk_value,
        fragment_scheme=fragment_scheme,
        logical_fragment_index=logical_fragment_index,
        logical_range=logical_range,
    )

    return make_pk(
        FRAGMENT_NAMESPACE,
        descriptor,
    )
