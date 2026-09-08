#!/usr/bin/env python3

"""Phase 6D-Q1 deterministic Query Capsule data model V1."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import hashlib
import json
import re
from typing import Any


DATA_MODEL_VERSION = "v1"

PROTOCOL_SHA256 = (
    "5255a58c8c6340c251e24ae8543760fcd66a8deb8be1a8356ad5b78ad898edda"
)

QUERY_CAPSULE_SCHEMA = "openmind.maf_query_capsule.v1"

QUERY_ROUTE_CACHE_ENTRY_SCHEMA = (
    "openmind.maf_query_route_cache_entry.v1"
)

QUERY_PK_PREFIX = "mafquery:v1:"
GENERATION_PK_PREFIX = "mafgen:v1:"
OBJECT_PK_PREFIX = "mafobj:v1:"

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_QUERY_PK_RE = re.compile(r"^mafquery:v1:[0-9a-f]{64}$")
_GENERATION_PK_RE = re.compile(r"^mafgen:v1:[0-9a-f]{64}$")
_OBJECT_PK_RE = re.compile(r"^mafobj:v1:[0-9a-f]{64}$")

CAPSULE_FIELDS = (
    "schema",
    "query_pk",
    "query_signature",
    "source_generation_pk",
    "source_manifest_sha256",
    "initial_object_pks",
    "selected_relationship_pks",
    "route_order",
    "expansion_policy",
    "max_object_budget",
    "max_expansion_rounds",
    "selection_config_sha256",
)

ROUTE_CACHE_FIELDS = (
    "schema",
    "exact_query_sha256",
    "query_signature",
    "source_generation_pk",
    "initial_pk_route",
    "additional_pks",
    "touched_pks",
    "selected_unused_pks",
    "route_config_sha256",
    "validation_metadata_sha256",
)

EXPANSION_POLICIES = frozenset(
    {
        "disabled",
        "bounded_v1",
    }
)


class MAFQueryCapsuleDataModelError(ValueError):
    """Raised when a frozen Phase 6D-Q1 invariant is violated."""


def _canonical_json_bytes(
    value: Mapping[str, Any],
) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _require_exact_keys(
    value: Mapping[str, Any],
    expected: tuple[str, ...],
    label: str,
) -> None:
    actual = set(value)
    required = set(expected)

    if actual != required:
        missing = sorted(
            required - actual
        )
        unknown = sorted(
            actual - required
        )

        raise MAFQueryCapsuleDataModelError(
            f"{label} fields differ from V1 schema; "
            f"missing={missing!r}; unknown={unknown!r}"
        )


def _require_string(
    value: Any,
    label: str,
) -> str:
    if not isinstance(value, str):
        raise MAFQueryCapsuleDataModelError(
            f"{label} must be a string"
        )

    return value


def _require_nonempty_utf8(
    value: Any,
    label: str,
) -> str:
    text = _require_string(
        value,
        label,
    )

    if not text:
        raise MAFQueryCapsuleDataModelError(
            f"{label} must be non-empty"
        )

    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise MAFQueryCapsuleDataModelError(
            f"{label} must be valid UTF-8"
        ) from exc

    return text


def _require_sha256(
    value: Any,
    label: str,
) -> str:
    text = _require_string(
        value,
        label,
    )

    if _SHA256_RE.fullmatch(text) is None:
        raise MAFQueryCapsuleDataModelError(
            f"{label} must be exactly 64 lowercase "
            "hexadecimal characters"
        )

    return text


def _require_query_pk(
    value: Any,
) -> str:
    text = _require_string(
        value,
        "query_pk",
    )

    if _QUERY_PK_RE.fullmatch(text) is None:
        raise MAFQueryCapsuleDataModelError(
            "query_pk has invalid mafquery:v1 grammar"
        )

    return text


def _require_generation_pk(
    value: Any,
    label: str = "source_generation_pk",
) -> str:
    text = _require_string(
        value,
        label,
    )

    if _GENERATION_PK_RE.fullmatch(text) is None:
        raise MAFQueryCapsuleDataModelError(
            f"{label} has invalid mafgen:v1 grammar"
        )

    return text


def _require_object_pk(
    value: Any,
    label: str,
) -> str:
    text = _require_string(
        value,
        label,
    )

    if _OBJECT_PK_RE.fullmatch(text) is None:
        raise MAFQueryCapsuleDataModelError(
            f"{label} has invalid mafobj:v1 grammar"
        )

    return text


def _require_plain_int(
    value: Any,
    label: str,
) -> int:
    if type(value) is not int:
        raise MAFQueryCapsuleDataModelError(
            f"{label} must be an integer"
        )

    return value


def _tuple_input(
    value: Any,
    label: str,
) -> tuple[Any, ...]:
    if isinstance(
        value,
        (
            str,
            bytes,
            bytearray,
        ),
    ):
        raise MAFQueryCapsuleDataModelError(
            f"{label} must be an ordered sequence"
        )

    try:
        return tuple(value)
    except TypeError as exc:
        raise MAFQueryCapsuleDataModelError(
            f"{label} must be an ordered iterable"
        ) from exc


def _object_pk_tuple(
    value: Any,
    label: str,
) -> tuple[str, ...]:
    raw = _tuple_input(
        value,
        label,
    )

    checked = tuple(
        _require_object_pk(
            item,
            f"{label}[{index}]",
        )
        for index, item in enumerate(raw)
    )

    if len(set(checked)) != len(checked):
        raise MAFQueryCapsuleDataModelError(
            f"{label} contains duplicate object PKs"
        )

    return checked


def _logical_pk_tuple(
    value: Any,
    label: str,
) -> tuple[str, ...]:
    raw = _tuple_input(
        value,
        label,
    )

    checked = tuple(
        _require_nonempty_utf8(
            item,
            f"{label}[{index}]",
        )
        for index, item in enumerate(raw)
    )

    if len(set(checked)) != len(checked):
        raise MAFQueryCapsuleDataModelError(
            f"{label} contains duplicate PKs"
        )

    return checked


def derive_query_pk(
    *,
    query_signature: str,
    selection_config_sha256: str,
    source_generation_pk: str,
    source_manifest_sha256: str,
) -> str:
    signature = _require_nonempty_utf8(
        query_signature,
        "query_signature",
    )

    config_sha = _require_sha256(
        selection_config_sha256,
        "selection_config_sha256",
    )

    generation_pk = _require_generation_pk(
        source_generation_pk
    )

    manifest_sha = _require_sha256(
        source_manifest_sha256,
        "source_manifest_sha256",
    )

    identity = {
        "query_signature": signature,
        "selection_config_sha256": config_sha,
        "source_generation_pk": generation_pk,
        "source_manifest_sha256": manifest_sha,
    }

    digest = hashlib.sha256(
        _canonical_json_bytes(
            identity
        )
    ).hexdigest()

    return QUERY_PK_PREFIX + digest


@dataclass(
    frozen=True,
    slots=True,
)
class MAFQueryCapsuleV1:
    schema: str
    query_pk: str
    query_signature: str
    source_generation_pk: str
    source_manifest_sha256: str
    initial_object_pks: tuple[str, ...]
    selected_relationship_pks: tuple[str, ...]
    route_order: tuple[str, ...]
    expansion_policy: str
    max_object_budget: int
    max_expansion_rounds: int
    selection_config_sha256: str

    def __post_init__(
        self,
    ) -> None:
        if self.schema != QUERY_CAPSULE_SCHEMA:
            raise MAFQueryCapsuleDataModelError(
                "query capsule schema mismatch"
            )

        query_pk = _require_query_pk(
            self.query_pk
        )

        signature = _require_nonempty_utf8(
            self.query_signature,
            "query_signature",
        )

        generation_pk = _require_generation_pk(
            self.source_generation_pk
        )

        manifest_sha = _require_sha256(
            self.source_manifest_sha256,
            "source_manifest_sha256",
        )

        config_sha = _require_sha256(
            self.selection_config_sha256,
            "selection_config_sha256",
        )

        initial = _object_pk_tuple(
            self.initial_object_pks,
            "initial_object_pks",
        )

        relationships = _logical_pk_tuple(
            self.selected_relationship_pks,
            "selected_relationship_pks",
        )

        route = _object_pk_tuple(
            self.route_order,
            "route_order",
        )

        budget = _require_plain_int(
            self.max_object_budget,
            "max_object_budget",
        )

        rounds = _require_plain_int(
            self.max_expansion_rounds,
            "max_expansion_rounds",
        )

        policy = _require_string(
            self.expansion_policy,
            "expansion_policy",
        )

        if budget <= 0:
            raise MAFQueryCapsuleDataModelError(
                "max_object_budget must be greater than zero"
            )

        if rounds < 0:
            raise MAFQueryCapsuleDataModelError(
                "max_expansion_rounds must be "
                "greater than or equal to zero"
            )

        if len(initial) > budget:
            raise MAFQueryCapsuleDataModelError(
                "initial_object_pks exceeds max_object_budget"
            )

        if policy not in EXPANSION_POLICIES:
            raise MAFQueryCapsuleDataModelError(
                "expansion_policy must be "
                "'disabled' or 'bounded_v1'"
            )

        if (
            policy == "disabled"
            and rounds != 0
        ):
            raise MAFQueryCapsuleDataModelError(
                "disabled expansion_policy requires "
                "max_expansion_rounds == 0"
            )

        if (
            policy == "bounded_v1"
            and rounds <= 0
        ):
            raise MAFQueryCapsuleDataModelError(
                "bounded_v1 expansion_policy requires "
                "max_expansion_rounds > 0"
            )

        if (
            len(route) != len(initial)
            or set(route) != set(initial)
        ):
            raise MAFQueryCapsuleDataModelError(
                "route_order must be an exact permutation "
                "of initial_object_pks"
            )

        expected_query_pk = derive_query_pk(
            query_signature=signature,
            selection_config_sha256=config_sha,
            source_generation_pk=generation_pk,
            source_manifest_sha256=manifest_sha,
        )

        if query_pk != expected_query_pk:
            raise MAFQueryCapsuleDataModelError(
                "query_pk differs from deterministic "
                "V1 derivation"
            )

        object.__setattr__(
            self,
            "query_signature",
            signature,
        )

        object.__setattr__(
            self,
            "source_generation_pk",
            generation_pk,
        )

        object.__setattr__(
            self,
            "source_manifest_sha256",
            manifest_sha,
        )

        object.__setattr__(
            self,
            "initial_object_pks",
            initial,
        )

        object.__setattr__(
            self,
            "selected_relationship_pks",
            relationships,
        )

        object.__setattr__(
            self,
            "route_order",
            route,
        )

        object.__setattr__(
            self,
            "expansion_policy",
            policy,
        )

        object.__setattr__(
            self,
            "max_object_budget",
            budget,
        )

        object.__setattr__(
            self,
            "max_expansion_rounds",
            rounds,
        )

        object.__setattr__(
            self,
            "selection_config_sha256",
            config_sha,
        )

    def to_dict(
        self,
    ) -> dict[str, Any]:
        return {
            "schema":
                self.schema,

            "query_pk":
                self.query_pk,

            "query_signature":
                self.query_signature,

            "source_generation_pk":
                self.source_generation_pk,

            "source_manifest_sha256":
                self.source_manifest_sha256,

            "initial_object_pks":
                list(
                    self.initial_object_pks
                ),

            "selected_relationship_pks":
                list(
                    self.selected_relationship_pks
                ),

            "route_order":
                list(
                    self.route_order
                ),

            "expansion_policy":
                self.expansion_policy,

            "max_object_budget":
                self.max_object_budget,

            "max_expansion_rounds":
                self.max_expansion_rounds,

            "selection_config_sha256":
                self.selection_config_sha256,
        }

    def canonical_bytes(
        self,
    ) -> bytes:
        return _canonical_json_bytes(
            self.to_dict()
        )

    @classmethod
    def from_mapping(
        cls,
        value: Mapping[str, Any],
    ) -> "MAFQueryCapsuleV1":
        if not isinstance(
            value,
            Mapping,
        ):
            raise MAFQueryCapsuleDataModelError(
                "query capsule input must be a mapping"
            )

        _require_exact_keys(
            value,
            CAPSULE_FIELDS,
            "query capsule",
        )

        return cls(
            **{
                field: value[field]
                for field in CAPSULE_FIELDS
            }
        )

    @classmethod
    def from_json_bytes(
        cls,
        raw: bytes,
    ) -> "MAFQueryCapsuleV1":
        if not isinstance(
            raw,
            bytes,
        ):
            raise MAFQueryCapsuleDataModelError(
                "query capsule JSON input must be bytes"
            )

        try:
            value = json.loads(
                raw.decode("utf-8")
            )
        except (
            UnicodeDecodeError,
            json.JSONDecodeError,
        ) as exc:
            raise MAFQueryCapsuleDataModelError(
                "query capsule JSON is invalid"
            ) from exc

        return cls.from_mapping(
            value
        )

    def require_source_binding(
        self,
        *,
        source_generation_pk: str,
        source_manifest_sha256: str,
    ) -> None:
        generation_pk = _require_generation_pk(
            source_generation_pk
        )

        manifest_sha = _require_sha256(
            source_manifest_sha256,
            "source_manifest_sha256",
        )

        if (
            generation_pk
            != self.source_generation_pk
        ):
            raise MAFQueryCapsuleDataModelError(
                "query capsule source generation mismatch"
            )

        if (
            manifest_sha
            != self.source_manifest_sha256
        ):
            raise MAFQueryCapsuleDataModelError(
                "query capsule source manifest mismatch"
            )


@dataclass(
    frozen=True,
    slots=True,
)
class MAFQueryRouteCacheEntryV1:
    schema: str
    exact_query_sha256: str
    query_signature: str
    source_generation_pk: str
    initial_pk_route: tuple[str, ...]
    additional_pks: tuple[str, ...]
    touched_pks: tuple[str, ...]
    selected_unused_pks: tuple[str, ...]
    route_config_sha256: str
    validation_metadata_sha256: str | None

    def __post_init__(
        self,
    ) -> None:
        if (
            self.schema
            != QUERY_ROUTE_CACHE_ENTRY_SCHEMA
        ):
            raise MAFQueryCapsuleDataModelError(
                "route cache schema mismatch"
            )

        exact_query_sha = _require_sha256(
            self.exact_query_sha256,
            "exact_query_sha256",
        )

        signature = _require_nonempty_utf8(
            self.query_signature,
            "query_signature",
        )

        generation_pk = _require_generation_pk(
            self.source_generation_pk
        )

        route_config_sha = _require_sha256(
            self.route_config_sha256,
            "route_config_sha256",
        )

        if (
            self.validation_metadata_sha256
            is None
        ):
            validation_sha = None
        else:
            validation_sha = _require_sha256(
                self.validation_metadata_sha256,
                "validation_metadata_sha256",
            )

        initial = _object_pk_tuple(
            self.initial_pk_route,
            "initial_pk_route",
        )

        additional = _object_pk_tuple(
            self.additional_pks,
            "additional_pks",
        )

        touched = _object_pk_tuple(
            self.touched_pks,
            "touched_pks",
        )

        unused = _object_pk_tuple(
            self.selected_unused_pks,
            "selected_unused_pks",
        )

        initial_set = set(initial)
        additional_set = set(additional)

        if (
            initial_set
            & additional_set
        ):
            raise MAFQueryCapsuleDataModelError(
                "initial_pk_route and additional_pks "
                "must be disjoint"
            )

        selected = (
            initial
            + additional
        )

        selected_set = set(
            selected
        )

        if not set(
            touched
        ).issubset(
            selected_set
        ):
            raise MAFQueryCapsuleDataModelError(
                "touched_pks must be a subset "
                "of selected PKs"
            )

        touched_set = set(
            touched
        )

        expected_unused = tuple(
            pk
            for pk in selected
            if pk not in touched_set
        )

        if unused != expected_unused:
            raise MAFQueryCapsuleDataModelError(
                "selected_unused_pks differs from "
                "deterministic selected-minus-touched order"
            )

        object.__setattr__(
            self,
            "exact_query_sha256",
            exact_query_sha,
        )

        object.__setattr__(
            self,
            "query_signature",
            signature,
        )

        object.__setattr__(
            self,
            "source_generation_pk",
            generation_pk,
        )

        object.__setattr__(
            self,
            "initial_pk_route",
            initial,
        )

        object.__setattr__(
            self,
            "additional_pks",
            additional,
        )

        object.__setattr__(
            self,
            "touched_pks",
            touched,
        )

        object.__setattr__(
            self,
            "selected_unused_pks",
            unused,
        )

        object.__setattr__(
            self,
            "route_config_sha256",
            route_config_sha,
        )

        object.__setattr__(
            self,
            "validation_metadata_sha256",
            validation_sha,
        )

    @property
    def exact_cache_key(
        self,
    ) -> tuple[str, str, str]:
        return (
            self.source_generation_pk,
            self.exact_query_sha256,
            self.route_config_sha256,
        )

    def to_dict(
        self,
    ) -> dict[str, Any]:
        return {
            "schema":
                self.schema,

            "exact_query_sha256":
                self.exact_query_sha256,

            "query_signature":
                self.query_signature,

            "source_generation_pk":
                self.source_generation_pk,

            "initial_pk_route":
                list(
                    self.initial_pk_route
                ),

            "additional_pks":
                list(
                    self.additional_pks
                ),

            "touched_pks":
                list(
                    self.touched_pks
                ),

            "selected_unused_pks":
                list(
                    self.selected_unused_pks
                ),

            "route_config_sha256":
                self.route_config_sha256,

            "validation_metadata_sha256":
                self.validation_metadata_sha256,
        }

    def canonical_bytes(
        self,
    ) -> bytes:
        return _canonical_json_bytes(
            self.to_dict()
        )

    @classmethod
    def from_mapping(
        cls,
        value: Mapping[str, Any],
    ) -> "MAFQueryRouteCacheEntryV1":
        if not isinstance(
            value,
            Mapping,
        ):
            raise MAFQueryCapsuleDataModelError(
                "route cache input must be a mapping"
            )

        _require_exact_keys(
            value,
            ROUTE_CACHE_FIELDS,
            "route cache entry",
        )

        return cls(
            **{
                field: value[field]
                for field in ROUTE_CACHE_FIELDS
            }
        )

    @classmethod
    def from_json_bytes(
        cls,
        raw: bytes,
    ) -> "MAFQueryRouteCacheEntryV1":
        if not isinstance(
            raw,
            bytes,
        ):
            raise MAFQueryCapsuleDataModelError(
                "route cache JSON input must be bytes"
            )

        try:
            value = json.loads(
                raw.decode("utf-8")
            )
        except (
            UnicodeDecodeError,
            json.JSONDecodeError,
        ) as exc:
            raise MAFQueryCapsuleDataModelError(
                "route cache JSON is invalid"
            ) from exc

        return cls.from_mapping(
            value
        )

    def require_source_generation(
        self,
        source_generation_pk: str,
    ) -> None:
        generation_pk = _require_generation_pk(
            source_generation_pk
        )

        if (
            generation_pk
            != self.source_generation_pk
        ):
            raise MAFQueryCapsuleDataModelError(
                "query route cache source generation mismatch"
            )
