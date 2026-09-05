from __future__ import annotations

import hashlib
import json
import logging
import math
import ctypes
import errno
import os
import re
import uuid
from collections.abc import Mapping, Set as AbstractSet
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

from maf_query_capsule_data_model_v1 import MAFQueryCapsuleV1
from maf_resident_pk_directory_v1 import (
    MAFResidentPKDirectoryError,
    ResidentPKSnapshot,
)

LOGGER = logging.getLogger(__name__)

SCHEMA_V1 = "openmind.maf_query_route_cache.v1"
CACHE_PK_PREFIX_V1 = "mafroutecache:v1:"
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class MAFQueryRouteCacheError(Exception):
    """Base class for Q4 route-cache failures."""


class MAFQueryRouteCacheDataError(MAFQueryRouteCacheError):
    """Malformed or structurally invalid cache metadata."""


class MAFQueryRouteCacheIdentityError(MAFQueryRouteCacheError):
    """Exact cache identity does not match the requested context."""


class MAFQueryRouteCacheIntegrityError(MAFQueryRouteCacheError):
    """Deterministic cache or route-payload integrity check failed."""


class MAFQueryRouteCacheObjectPKError(MAFQueryRouteCacheError):
    """A referenced object PK cannot be resolved safely."""


class MAFQueryRouteCacheRelationshipPKError(MAFQueryRouteCacheError):
    """A referenced relationship PK is not in the supplied authority."""


class MAFQueryRouteCachePersistenceError(MAFQueryRouteCacheError):
    """Canonical route-cache persistence or readback failed."""


def _fail(error_type: type[MAFQueryRouteCacheError], message: str) -> None:
    LOGGER.error("%s", message)
    raise error_type(message)


def _log_unexpected(context: str, exc: BaseException) -> None:
    LOGGER.exception("%s: unexpected %s: %s", context, type(exc).__name__, exc)


def _require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        _fail(MAFQueryRouteCacheDataError, f"{label} must be a non-empty string")
    return value


def _require_sha256(value: Any, label: str) -> str:
    text = _require_text(value, label)
    if _SHA256_RE.fullmatch(text) is None:
        _fail(MAFQueryRouteCacheDataError, f"{label} must be a lowercase SHA256 hex digest")
    return text


def _require_positive_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        _fail(MAFQueryRouteCacheDataError, f"{label} must be a positive integer")
    return value


def _require_nonnegative_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        _fail(MAFQueryRouteCacheDataError, f"{label} must be a non-negative integer")
    return value


def _require_text_tuple(value: Any, label: str, *, allow_empty: bool = True) -> tuple[str, ...]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, (list, tuple)):
        _fail(MAFQueryRouteCacheDataError, f"{label} must be a sequence of strings")
    result = tuple(_require_text(item, f"{label}[{index}]") for index, item in enumerate(value))
    if not allow_empty and not result:
        _fail(MAFQueryRouteCacheDataError, f"{label} must not be empty")
    if len(set(result)) != len(result):
        _fail(MAFQueryRouteCacheDataError, f"{label} must contain unique values")
    return result


def _freeze_json(value: Any, label: str = "value") -> Any:
    if value is None or isinstance(value, (bool, str, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            _fail(MAFQueryRouteCacheDataError, f"{label} contains a non-finite number")
        return value
    if isinstance(value, Mapping):
        frozen: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                _fail(MAFQueryRouteCacheDataError, f"{label} contains a non-string mapping key")
            frozen[key] = _freeze_json(item, f"{label}.{key}")
        return MappingProxyType(frozen)
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(item, f"{label}[{index}]") for index, item in enumerate(value))
    _fail(
        MAFQueryRouteCacheDataError,
        f"{label} contains unsupported JSON type {type(value).__name__}",
    )


def _json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    return value


def _canonical_json_bytes(value: Mapping[str, Any], *, trailing_newline: bool) -> bytes:
    try:
        text = json.dumps(
            _json_ready(value),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
        raw = text.encode("utf-8")
        return raw + (b"\n" if trailing_newline else b"")
    except MAFQueryRouteCacheError:
        raise
    except (TypeError, ValueError, UnicodeError) as exc:
        LOGGER.error("canonical JSON rejected: %s", exc)
        raise MAFQueryRouteCacheDataError(f"canonical JSON rejected: {exc}") from exc
    except Exception as exc:
        _log_unexpected("canonical JSON", exc)
        raise MAFQueryRouteCacheDataError("canonical JSON failed unexpectedly") from exc


def _json_equivalent(left: Any, right: Any) -> bool:
    try:
        return _canonical_json_bytes(
            {"value": _freeze_json(left)},
            trailing_newline=False,
        ) == _canonical_json_bytes(
            {"value": _freeze_json(right)},
            trailing_newline=False,
        )
    except MAFQueryRouteCacheError:
        raise
    except Exception as exc:
        _log_unexpected("JSON equivalence", exc)
        raise MAFQueryRouteCacheDataError("JSON equivalence failed unexpectedly") from exc


def _sha256_hex(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _identity_mapping(
    *,
    query_signature: str,
    source_generation_pk: str,
    source_manifest_sha256: str,
    selection_config_sha256: str,
    expansion_policy: Any,
    max_object_budget: int,
    max_expansion_rounds: int,
) -> dict[str, Any]:
    return {
        "query_signature": query_signature,
        "source_generation_pk": source_generation_pk,
        "source_manifest_sha256": source_manifest_sha256,
        "selection_config_sha256": selection_config_sha256,
        "expansion_policy": _json_ready(expansion_policy),
        "max_object_budget": max_object_budget,
        "max_expansion_rounds": max_expansion_rounds,
    }


def _route_payload_mapping(
    *,
    initial_object_pks: tuple[str, ...],
    selected_relationship_pks: tuple[str, ...],
    route_order: tuple[str, ...],
) -> dict[str, Any]:
    return {
        "initial_object_pks": list(initial_object_pks),
        "selected_relationship_pks": list(selected_relationship_pks),
        "route_order": list(route_order),
    }


def derive_cache_pk_v1(
    *,
    query_signature: str,
    source_generation_pk: str,
    source_manifest_sha256: str,
    selection_config_sha256: str,
    expansion_policy: Any,
    max_object_budget: int,
    max_expansion_rounds: int,
) -> str:
    try:
        frozen_policy = _freeze_json(expansion_policy, "expansion_policy")
        identity = _identity_mapping(
            query_signature=_require_text(query_signature, "query_signature"),
            source_generation_pk=_require_text(source_generation_pk, "source_generation_pk"),
            source_manifest_sha256=_require_sha256(
                source_manifest_sha256,
                "source_manifest_sha256",
            ),
            selection_config_sha256=_require_sha256(
                selection_config_sha256,
                "selection_config_sha256",
            ),
            expansion_policy=frozen_policy,
            max_object_budget=_require_positive_int(max_object_budget, "max_object_budget"),
            max_expansion_rounds=_require_nonnegative_int(
                max_expansion_rounds,
                "max_expansion_rounds",
            ),
        )
        return CACHE_PK_PREFIX_V1 + _sha256_hex(
            _canonical_json_bytes(identity, trailing_newline=False)
        )
    except MAFQueryRouteCacheError:
        raise
    except Exception as exc:
        _log_unexpected("derive_cache_pk_v1", exc)
        raise MAFQueryRouteCacheIntegrityError(
            "cache PK derivation failed unexpectedly"
        ) from exc


def derive_route_payload_sha256_v1(
    *,
    initial_object_pks: tuple[str, ...],
    selected_relationship_pks: tuple[str, ...],
    route_order: tuple[str, ...],
) -> str:
    try:
        initial = _require_text_tuple(
            initial_object_pks,
            "initial_object_pks",
            allow_empty=False,
        )
        relationships = _require_text_tuple(
            selected_relationship_pks,
            "selected_relationship_pks",
        )
        route = _require_text_tuple(route_order, "route_order", allow_empty=False)
        payload = _route_payload_mapping(
            initial_object_pks=initial,
            selected_relationship_pks=relationships,
            route_order=route,
        )
        return _sha256_hex(_canonical_json_bytes(payload, trailing_newline=False))
    except MAFQueryRouteCacheError:
        raise
    except Exception as exc:
        _log_unexpected("derive_route_payload_sha256_v1", exc)
        raise MAFQueryRouteCacheIntegrityError(
            "route payload digest derivation failed unexpectedly"
        ) from exc


@dataclass(frozen=True)
class MAFQueryRouteCacheRecordV1:
    schema: str
    cache_pk: str
    query_signature: str
    source_generation_pk: str
    source_manifest_sha256: str
    selection_config_sha256: str
    expansion_policy: Any
    max_object_budget: int
    max_expansion_rounds: int
    initial_object_pks: tuple[str, ...]
    selected_relationship_pks: tuple[str, ...]
    route_order: tuple[str, ...]
    route_payload_sha256: str

    def __post_init__(self) -> None:
        try:
            if self.schema != SCHEMA_V1:
                _fail(
                    MAFQueryRouteCacheDataError,
                    f"schema must equal {SCHEMA_V1!r}",
                )

            _require_text(self.query_signature, "query_signature")
            _require_text(self.source_generation_pk, "source_generation_pk")
            _require_sha256(self.source_manifest_sha256, "source_manifest_sha256")
            _require_sha256(self.selection_config_sha256, "selection_config_sha256")
            _require_positive_int(self.max_object_budget, "max_object_budget")
            _require_nonnegative_int(self.max_expansion_rounds, "max_expansion_rounds")

            frozen_policy = _freeze_json(self.expansion_policy, "expansion_policy")
            initial = _require_text_tuple(
                self.initial_object_pks,
                "initial_object_pks",
                allow_empty=False,
            )
            relationships = _require_text_tuple(
                self.selected_relationship_pks,
                "selected_relationship_pks",
            )
            route = _require_text_tuple(
                self.route_order,
                "route_order",
                allow_empty=False,
            )

            object.__setattr__(self, "expansion_policy", frozen_policy)
            object.__setattr__(self, "initial_object_pks", initial)
            object.__setattr__(self, "selected_relationship_pks", relationships)
            object.__setattr__(self, "route_order", route)

            if len(route) > self.max_object_budget:
                _fail(
                    MAFQueryRouteCacheDataError,
                    "route_order exceeds max_object_budget",
                )

            route_set = set(route)
            missing_initial = tuple(pk for pk in initial if pk not in route_set)
            if missing_initial:
                _fail(
                    MAFQueryRouteCacheDataError,
                    "route_order does not contain every initial_object_pk",
                )

            expected_cache_pk = derive_cache_pk_v1(
                query_signature=self.query_signature,
                source_generation_pk=self.source_generation_pk,
                source_manifest_sha256=self.source_manifest_sha256,
                selection_config_sha256=self.selection_config_sha256,
                expansion_policy=self.expansion_policy,
                max_object_budget=self.max_object_budget,
                max_expansion_rounds=self.max_expansion_rounds,
            )
            if self.cache_pk != expected_cache_pk:
                _fail(
                    MAFQueryRouteCacheIntegrityError,
                    "cache_pk does not match deterministic identity",
                )

            expected_payload_sha = derive_route_payload_sha256_v1(
                initial_object_pks=initial,
                selected_relationship_pks=relationships,
                route_order=route,
            )
            if self.route_payload_sha256 != expected_payload_sha:
                _fail(
                    MAFQueryRouteCacheIntegrityError,
                    "route_payload_sha256 does not match deterministic route payload",
                )
        except MAFQueryRouteCacheError:
            raise
        except Exception as exc:
            _log_unexpected("MAFQueryRouteCacheRecordV1.__post_init__", exc)
            raise MAFQueryRouteCacheDataError(
                "route-cache record validation failed unexpectedly"
            ) from exc

    def identity_mapping(self) -> dict[str, Any]:
        try:
            return _identity_mapping(
                query_signature=self.query_signature,
                source_generation_pk=self.source_generation_pk,
                source_manifest_sha256=self.source_manifest_sha256,
                selection_config_sha256=self.selection_config_sha256,
                expansion_policy=self.expansion_policy,
                max_object_budget=self.max_object_budget,
                max_expansion_rounds=self.max_expansion_rounds,
            )
        except MAFQueryRouteCacheError:
            raise
        except Exception as exc:
            _log_unexpected("identity_mapping", exc)
            raise MAFQueryRouteCacheError("identity mapping failed unexpectedly") from exc

    def route_payload_mapping(self) -> dict[str, Any]:
        try:
            return _route_payload_mapping(
                initial_object_pks=self.initial_object_pks,
                selected_relationship_pks=self.selected_relationship_pks,
                route_order=self.route_order,
            )
        except MAFQueryRouteCacheError:
            raise
        except Exception as exc:
            _log_unexpected("route_payload_mapping", exc)
            raise MAFQueryRouteCacheError("route payload mapping failed unexpectedly") from exc

    def to_dict(self) -> dict[str, Any]:
        try:
            return {
                "schema": self.schema,
                "cache_pk": self.cache_pk,
                "query_signature": self.query_signature,
                "source_generation_pk": self.source_generation_pk,
                "source_manifest_sha256": self.source_manifest_sha256,
                "selection_config_sha256": self.selection_config_sha256,
                "expansion_policy": _json_ready(self.expansion_policy),
                "max_object_budget": self.max_object_budget,
                "max_expansion_rounds": self.max_expansion_rounds,
                "initial_object_pks": list(self.initial_object_pks),
                "selected_relationship_pks": list(self.selected_relationship_pks),
                "route_order": list(self.route_order),
                "route_payload_sha256": self.route_payload_sha256,
            }
        except Exception as exc:
            _log_unexpected("to_dict", exc)
            raise MAFQueryRouteCacheError("record serialization mapping failed unexpectedly") from exc

    def canonical_bytes(self) -> bytes:
        try:
            return _canonical_json_bytes(self.to_dict(), trailing_newline=True)
        except MAFQueryRouteCacheError:
            raise
        except Exception as exc:
            _log_unexpected("canonical_bytes", exc)
            raise MAFQueryRouteCacheError("canonical record serialization failed unexpectedly") from exc

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "MAFQueryRouteCacheRecordV1":
        try:
            if not isinstance(value, Mapping):
                _fail(MAFQueryRouteCacheDataError, "cache record must be a mapping")

            expected_fields = (
                "schema",
                "cache_pk",
                "query_signature",
                "source_generation_pk",
                "source_manifest_sha256",
                "selection_config_sha256",
                "expansion_policy",
                "max_object_budget",
                "max_expansion_rounds",
                "initial_object_pks",
                "selected_relationship_pks",
                "route_order",
                "route_payload_sha256",
            )
            actual = tuple(value.keys())
            if set(actual) != set(expected_fields) or len(actual) != len(expected_fields):
                _fail(
                    MAFQueryRouteCacheDataError,
                    "cache record fields must match the Q4 V1 schema exactly",
                )

            return cls(
                schema=value["schema"],
                cache_pk=value["cache_pk"],
                query_signature=value["query_signature"],
                source_generation_pk=value["source_generation_pk"],
                source_manifest_sha256=value["source_manifest_sha256"],
                selection_config_sha256=value["selection_config_sha256"],
                expansion_policy=value["expansion_policy"],
                max_object_budget=value["max_object_budget"],
                max_expansion_rounds=value["max_expansion_rounds"],
                initial_object_pks=value["initial_object_pks"],
                selected_relationship_pks=value["selected_relationship_pks"],
                route_order=value["route_order"],
                route_payload_sha256=value["route_payload_sha256"],
            )
        except MAFQueryRouteCacheError:
            raise
        except (KeyError, TypeError, ValueError) as exc:
            LOGGER.error("cache mapping rejected: %s", exc)
            raise MAFQueryRouteCacheDataError(f"cache mapping rejected: {exc}") from exc
        except Exception as exc:
            _log_unexpected("MAFQueryRouteCacheRecordV1.from_mapping", exc)
            raise MAFQueryRouteCacheDataError(
                "cache mapping failed unexpectedly"
            ) from exc

    @classmethod
    def from_json_bytes(cls, raw: bytes) -> "MAFQueryRouteCacheRecordV1":
        try:
            if not isinstance(raw, bytes):
                _fail(MAFQueryRouteCacheDataError, "raw cache record must be bytes")
            value = json.loads(raw.decode("utf-8"))
            record = cls.from_mapping(value)
            if raw != record.canonical_bytes():
                _fail(
                    MAFQueryRouteCachePersistenceError,
                    "persisted cache record is not canonical",
                )
            return record
        except MAFQueryRouteCacheError:
            raise
        except (UnicodeError, json.JSONDecodeError) as exc:
            LOGGER.error("cache JSON rejected: %s", exc)
            raise MAFQueryRouteCacheDataError(f"cache JSON rejected: {exc}") from exc
        except Exception as exc:
            _log_unexpected("MAFQueryRouteCacheRecordV1.from_json_bytes", exc)
            raise MAFQueryRouteCacheDataError(
                "cache JSON parsing failed unexpectedly"
            ) from exc


def build_route_cache_record_v1(
    capsule: MAFQueryCapsuleV1,
) -> MAFQueryRouteCacheRecordV1:
    try:
        if not isinstance(capsule, MAFQueryCapsuleV1):
            _fail(
                MAFQueryRouteCacheDataError,
                "capsule must be MAFQueryCapsuleV1",
            )

        cache_pk = derive_cache_pk_v1(
            query_signature=capsule.query_signature,
            source_generation_pk=capsule.source_generation_pk,
            source_manifest_sha256=capsule.source_manifest_sha256,
            selection_config_sha256=capsule.selection_config_sha256,
            expansion_policy=capsule.expansion_policy,
            max_object_budget=capsule.max_object_budget,
            max_expansion_rounds=capsule.max_expansion_rounds,
        )
        payload_sha = derive_route_payload_sha256_v1(
            initial_object_pks=tuple(capsule.initial_object_pks),
            selected_relationship_pks=tuple(capsule.selected_relationship_pks),
            route_order=tuple(capsule.route_order),
        )

        return MAFQueryRouteCacheRecordV1(
            schema=SCHEMA_V1,
            cache_pk=cache_pk,
            query_signature=capsule.query_signature,
            source_generation_pk=capsule.source_generation_pk,
            source_manifest_sha256=capsule.source_manifest_sha256,
            selection_config_sha256=capsule.selection_config_sha256,
            expansion_policy=capsule.expansion_policy,
            max_object_budget=capsule.max_object_budget,
            max_expansion_rounds=capsule.max_expansion_rounds,
            initial_object_pks=tuple(capsule.initial_object_pks),
            selected_relationship_pks=tuple(capsule.selected_relationship_pks),
            route_order=tuple(capsule.route_order),
            route_payload_sha256=payload_sha,
        )
    except MAFQueryRouteCacheError:
        raise
    except Exception as exc:
        _log_unexpected("build_route_cache_record_v1", exc)
        raise MAFQueryRouteCacheDataError(
            "failed to build route-cache record"
        ) from exc


def _resolve_object_pk_v1(
    *,
    snapshot: ResidentPKSnapshot,
    model_pk: str,
    logical_pk: str,
    expected_generation_pk: str,
) -> None:
    try:
        matches = []

        for key in snapshot.entries.keys():
            if not isinstance(key, tuple) or len(key) != 3:
                continue

            key_model_pk, pk_kind, key_logical_pk = key

            if key_model_pk == model_pk and key_logical_pk == logical_pk:
                matches.append((pk_kind, key_logical_pk))

        if len(matches) != 1:
            _fail(
                MAFQueryRouteCacheObjectPKError,
                f"object PK {logical_pk!r} is not uniquely present in resident snapshot",
            )

        pk_kind, resolved_logical_pk = matches[0]

        if not isinstance(pk_kind, str) or not pk_kind:
            _fail(
                MAFQueryRouteCacheObjectPKError,
                f"object PK {logical_pk!r} has no usable resident pk_kind",
            )

        if resolved_logical_pk != logical_pk:
            _fail(
                MAFQueryRouteCacheObjectPKError,
                f"resident logical PK mismatch for {logical_pk!r}",
            )

        snapshot.lookup(
            model_pk=model_pk,
            pk_kind=pk_kind,
            logical_pk=logical_pk,
            expected_generation_pk=expected_generation_pk,
        )
    except MAFQueryRouteCacheError:
        raise
    except MAFResidentPKDirectoryError as exc:
        LOGGER.error("resident lookup rejected %s: %s", logical_pk, exc)
        raise MAFQueryRouteCacheObjectPKError(
            f"resident lookup rejected object PK {logical_pk!r}: {exc}"
        ) from exc
    except Exception as exc:
        _log_unexpected(f"resident lookup for {logical_pk!r}", exc)
        raise MAFQueryRouteCacheObjectPKError(
            f"resident lookup failed unexpectedly for object PK {logical_pk!r}"
        ) from exc


def validate_route_cache_for_reuse_v1(
    *,
    record: MAFQueryRouteCacheRecordV1,
    expected_query_signature: str,
    expected_source_generation_pk: str,
    expected_source_manifest_sha256: str,
    expected_selection_config_sha256: str,
    expected_expansion_policy: Any,
    expected_max_object_budget: int,
    expected_max_expansion_rounds: int,
    model_pk: str,
    resident_snapshot: ResidentPKSnapshot,
    relationship_authority_pks: AbstractSet[str],
) -> None:
    try:
        if not isinstance(record, MAFQueryRouteCacheRecordV1):
            _fail(MAFQueryRouteCacheDataError, "record must be MAFQueryRouteCacheRecordV1")
        if not isinstance(resident_snapshot, ResidentPKSnapshot):
            _fail(MAFQueryRouteCacheDataError, "resident_snapshot must be ResidentPKSnapshot")
        if not isinstance(relationship_authority_pks, AbstractSet):
            _fail(
                MAFQueryRouteCacheDataError,
                "relationship_authority_pks must be a set-like authority",
            )

        try:
            relationship_authority = frozenset(
                _require_text(value, "relationship_authority_pks item")
                for value in relationship_authority_pks
            )
        except MAFQueryRouteCacheError:
            raise
        except Exception as exc:
            _log_unexpected("relationship authority normalization", exc)
            raise MAFQueryRouteCacheDataError(
                "relationship authority normalization failed unexpectedly"
            ) from exc

        expected_pairs = (
            ("query_signature", record.query_signature, expected_query_signature),
            ("source_generation_pk", record.source_generation_pk, expected_source_generation_pk),
            ("source_manifest_sha256", record.source_manifest_sha256, expected_source_manifest_sha256),
            ("selection_config_sha256", record.selection_config_sha256, expected_selection_config_sha256),
            ("max_object_budget", record.max_object_budget, expected_max_object_budget),
            ("max_expansion_rounds", record.max_expansion_rounds, expected_max_expansion_rounds),
        )
        for label, actual, expected in expected_pairs:
            if actual != expected:
                _fail(
                    MAFQueryRouteCacheIdentityError,
                    f"{label} does not match requested cache context",
                )

        if not _json_equivalent(record.expansion_policy, expected_expansion_policy):
            _fail(
                MAFQueryRouteCacheIdentityError,
                "expansion_policy does not match requested cache context",
            )

        expected_cache_pk = derive_cache_pk_v1(
            query_signature=record.query_signature,
            source_generation_pk=record.source_generation_pk,
            source_manifest_sha256=record.source_manifest_sha256,
            selection_config_sha256=record.selection_config_sha256,
            expansion_policy=record.expansion_policy,
            max_object_budget=record.max_object_budget,
            max_expansion_rounds=record.max_expansion_rounds,
        )
        if record.cache_pk != expected_cache_pk:
            _fail(MAFQueryRouteCacheIntegrityError, "cache_pk integrity check failed")

        expected_payload_sha = derive_route_payload_sha256_v1(
            initial_object_pks=record.initial_object_pks,
            selected_relationship_pks=record.selected_relationship_pks,
            route_order=record.route_order,
        )
        if record.route_payload_sha256 != expected_payload_sha:
            _fail(
                MAFQueryRouteCacheIntegrityError,
                "route_payload_sha256 integrity check failed",
            )

        object_pks = tuple(dict.fromkeys(record.initial_object_pks + record.route_order))
        for logical_pk in object_pks:
            _resolve_object_pk_v1(
                snapshot=resident_snapshot,
                model_pk=model_pk,
                logical_pk=logical_pk,
                expected_generation_pk=record.source_generation_pk,
            )

        for relationship_pk in record.selected_relationship_pks:
            if relationship_pk not in relationship_authority:
                _fail(
                    MAFQueryRouteCacheRelationshipPKError,
                    f"relationship PK {relationship_pk!r} is not authoritative",
                )
    except MAFQueryRouteCacheError:
        raise
    except Exception as exc:
        _log_unexpected("validate_route_cache_for_reuse_v1", exc)
        raise MAFQueryRouteCacheError(
            "route-cache reuse validation failed unexpectedly"
        ) from exc


def validated_route_payload_v1(
    record: MAFQueryRouteCacheRecordV1,
) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    try:
        if not isinstance(record, MAFQueryRouteCacheRecordV1):
            _fail(MAFQueryRouteCacheDataError, "record must be MAFQueryRouteCacheRecordV1")
        return (
            record.initial_object_pks,
            record.selected_relationship_pks,
            record.route_order,
        )
    except MAFQueryRouteCacheError:
        raise
    except Exception as exc:
        _log_unexpected("validated_route_payload_v1", exc)
        raise MAFQueryRouteCacheError(
            "validated route payload extraction failed unexpectedly"
        ) from exc


def read_route_cache_record_v1(path: Path) -> MAFQueryRouteCacheRecordV1:
    try:
        path = Path(path)
        raw = path.read_bytes()
        return MAFQueryRouteCacheRecordV1.from_json_bytes(raw)
    except MAFQueryRouteCacheError:
        raise
    except OSError as exc:
        LOGGER.error("route-cache read failed for %s: %s", path, exc)
        raise MAFQueryRouteCachePersistenceError(
            f"route-cache read failed for {path}: {exc}"
        ) from exc
    except Exception as exc:
        _log_unexpected(f"route-cache read for {path}", exc)
        raise MAFQueryRouteCachePersistenceError(
            f"route-cache read failed unexpectedly for {path}"
        ) from exc


def _fsync_directory(path: Path) -> None:
    fd: int | None = None
    try:
        fd = os.open(path, os.O_RDONLY)
        os.fsync(fd)
    except OSError as exc:
        LOGGER.error("directory fsync failed for %s: %s", path, exc)
        raise MAFQueryRouteCachePersistenceError(
            f"directory fsync failed for {path}: {exc}"
        ) from exc
    except Exception as exc:
        _log_unexpected(f"directory fsync for {path}", exc)
        raise MAFQueryRouteCachePersistenceError(
            f"directory fsync failed unexpectedly for {path}"
        ) from exc
    finally:
        if fd is not None:
            try:
                os.close(fd)
            except OSError as exc:
                LOGGER.warning("directory fd close failed for %s: %s", path, exc)


def _atomic_publish_noreplace_v1(partial: Path, path: Path) -> None:
    libc = ctypes.CDLL(None, use_errno=True)

    if not hasattr(libc, "renameat2"):
        raise OSError(errno.ENOSYS, "libc renameat2 is unavailable", path)

    renameat2 = libc.renameat2
    renameat2.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    ]
    renameat2.restype = ctypes.c_int

    at_fdcwd = -100
    rename_noreplace = 1

    ctypes.set_errno(0)
    rc = renameat2(
        at_fdcwd,
        os.fsencode(partial),
        at_fdcwd,
        os.fsencode(path),
        rename_noreplace,
    )

    if rc == 0:
        return

    error_number = ctypes.get_errno()

    if error_number == errno.EEXIST:
        raise FileExistsError(
            error_number,
            os.strerror(error_number),
            path,
        )

    raise OSError(
        error_number,
        os.strerror(error_number),
        path,
    )


def write_route_cache_record_v1(
    path: Path,
    record: MAFQueryRouteCacheRecordV1,
) -> None:
    partial: Path | None = None
    fd: int | None = None
    try:
        path = Path(path)
        if not isinstance(record, MAFQueryRouteCacheRecordV1):
            _fail(MAFQueryRouteCacheDataError, "record must be MAFQueryRouteCacheRecordV1")

        raw = record.canonical_bytes()
        path.parent.mkdir(parents=True, exist_ok=True)

        try:
            existing = path.read_bytes()
        except FileNotFoundError:
            existing = None
        except OSError as exc:
            LOGGER.error("pre-existing cache read failed for %s: %s", path, exc)
            raise MAFQueryRouteCachePersistenceError(
                f"pre-existing cache read failed for {path}: {exc}"
            ) from exc

        if existing is not None:
            if existing == raw:
                MAFQueryRouteCacheRecordV1.from_json_bytes(existing)
                return
            _fail(
                MAFQueryRouteCachePersistenceError,
                f"refusing to overwrite non-identical cache record at {path}",
            )

        partial = path.with_name(
            f".{path.name}.{os.getpid()}.{uuid.uuid4().hex}.partial"
        )
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        fd = os.open(partial, flags, 0o600)

        view = memoryview(raw)
        written = 0
        while written < len(view):
            count = os.write(fd, view[written:])
            if count <= 0:
                _fail(
                    MAFQueryRouteCachePersistenceError,
                    f"short write while persisting {partial}",
                )
            written += count

        os.fsync(fd)
        os.close(fd)
        fd = None

        try:
            _atomic_publish_noreplace_v1(partial, path)
        except FileExistsError:
            try:
                existing = path.read_bytes()
            except OSError as exc:
                LOGGER.error("race readback failed for %s: %s", path, exc)
                raise MAFQueryRouteCachePersistenceError(
                    f"race readback failed for {path}: {exc}"
                ) from exc
            if existing != raw:
                _fail(
                    MAFQueryRouteCachePersistenceError,
                    f"concurrent non-identical cache record exists at {path}",
                )
            MAFQueryRouteCacheRecordV1.from_json_bytes(existing)
        except OSError as exc:
            LOGGER.error("atomic no-replace publication failed for %s: %s", path, exc)
            raise MAFQueryRouteCachePersistenceError(
                f"atomic no-replace publication failed for {path}: {exc}"
            ) from exc

        _fsync_directory(path.parent)

        try:
            partial.unlink()
            partial = None
        except FileNotFoundError:
            partial = None
        except OSError as exc:
            LOGGER.warning("published cache partial cleanup failed for %s: %s", partial, exc)

        _fsync_directory(path.parent)
    except MAFQueryRouteCacheError:
        raise
    except OSError as exc:
        LOGGER.error("route-cache persistence failed for %s: %s", path, exc)
        raise MAFQueryRouteCachePersistenceError(
            f"route-cache persistence failed for {path}: {exc}"
        ) from exc
    except Exception as exc:
        _log_unexpected(f"route-cache persistence for {path}", exc)
        raise MAFQueryRouteCachePersistenceError(
            f"route-cache persistence failed unexpectedly for {path}"
        ) from exc
    finally:
        if fd is not None:
            try:
                os.close(fd)
            except OSError as exc:
                LOGGER.warning("partial fd close failed: %s", exc)
        if partial is not None:
            try:
                partial.unlink()
            except FileNotFoundError:
                LOGGER.debug("route cache cleanup partial already absent; known FileNotFoundError cleanup escape")
            except OSError as exc:
                LOGGER.warning("partial cleanup failed for %s: %s", partial, exc)


__all__ = [
    "SCHEMA_V1",
    "MAFQueryRouteCacheError",
    "MAFQueryRouteCacheDataError",
    "MAFQueryRouteCacheIdentityError",
    "MAFQueryRouteCacheIntegrityError",
    "MAFQueryRouteCacheObjectPKError",
    "MAFQueryRouteCacheRelationshipPKError",
    "MAFQueryRouteCachePersistenceError",
    "MAFQueryRouteCacheRecordV1",
    "derive_cache_pk_v1",
    "derive_route_payload_sha256_v1",
    "build_route_cache_record_v1",
    "validate_route_cache_for_reuse_v1",
    "validated_route_payload_v1",
    "read_route_cache_record_v1",
    "write_route_cache_record_v1",
]
