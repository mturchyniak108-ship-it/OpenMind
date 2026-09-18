#!/usr/bin/env python3

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import hashlib
import json
import re
import unicodedata
from typing import Any


PROTOCOL_SHA256 = (
    "b42a0643976c2393871e3b826ba5573b4de981b49603de63230d69cf57be0811"
)

CATALOG_SCHEMA = "openmind.maf_query_pk_catalog.v1"
CONFIG_SCHEMA = "openmind.maf_query_to_pk_selection_config.v1"
RESULT_SCHEMA = "openmind.maf_query_to_pk_selection.v1"

GENERATION_PK_PREFIX = "mafgen:v1:"
OBJECT_PK_PREFIX = "mafobj:v1:"

NORMALIZATION_VERSION = "nfkc_casefold_v1"
ALIAS_VERSION = "metadata_intent_alias_v1"
DESCRIPTOR_VERSION = "tensor_name_descriptor_v1"
RANKING_VERSION = "metadata_subset_rank_v1"
FALLBACK_VERSION = "sha256_rendezvous_v1"

MAX_CANDIDATE_LIMIT = 32

TAG_ORDER = (
    "attn",
    "q",
    "k",
    "v",
    "ffn",
    "down",
    "up",
    "gate",
    "norm",
    "embedding",
    "output",
)

CATALOG_FIELDS = (
    "schema",
    "source_generation_pk",
    "source_manifest_sha256",
    "entries",
)

CATALOG_ENTRY_FIELDS = (
    "object_pk",
    "tensor_name",
    "tensor_type",
    "dims",
    "element_count",
)

CONFIG_FIELDS = (
    "schema",
    "max_candidates",
    "normalization_version",
    "alias_version",
    "descriptor_version",
    "ranking_version",
    "fallback_version",
)

RESULT_FIELDS = (
    "schema",
    "query_signature",
    "source_generation_pk",
    "source_manifest_sha256",
    "catalog_sha256",
    "selection_config_sha256",
    "recognized_layer",
    "recognized_tags",
    "fallback_used",
    "selected_object_pks",
)

_SHA_RE = re.compile(r"^[0-9a-f]{64}$")
_GEN_RE = re.compile(r"^mafgen:v1:[0-9a-f]{64}$")
_OBJ_RE = re.compile(r"^mafobj:v1:[0-9a-f]{64}$")
_ASCII_DECIMAL_RE = re.compile(r"^[0-9]+$")

_TENSOR_LAYER_RE = re.compile(
    r"(?:^|[._/-])blk\.([0-9]+)(?=$|[._/-])"
)

_TENSOR_SPLIT_RE = re.compile(r"[._/-]+")

_TENSOR_TAGS = {
    "attn": "attn",
    "q": "q",
    "k": "k",
    "v": "v",
    "ffn": "ffn",
    "down": "down",
    "up": "up",
    "gate": "gate",
    "norm": "norm",
    "embd": "embedding",
    "embedding": "embedding",
    "output": "output",
}

_QUERY_PHRASES = (
    (("feed", "forward"), "ffn"),
    (("down", "projection"), "down"),
    (("up", "projection"), "up"),
    (("token", "embedding"), "embedding"),
    (("token", "embeddings"), "embedding"),
    (("lm", "head"), "output"),
)

_QUERY_SINGLE = {
    "attention": "attn",
    "attn": "attn",
    "query": "q",
    "q": "q",
    "key": "k",
    "k": "k",
    "value": "v",
    "v": "v",
    "feedforward": "ffn",
    "ffn": "ffn",
    "mlp": "ffn",
    "down": "down",
    "up": "up",
    "gate": "gate",
    "normalization": "norm",
    "norm": "norm",
    "embedding": "embedding",
    "embeddings": "embedding",
    "embd": "embedding",
    "output": "output",
}


class MAFQueryToPKSelectionError(ValueError):
    pass


def _canonical_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _require_mapping(
    value: Any,
    fields: tuple[str, ...],
    label: str,
) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise MAFQueryToPKSelectionError(
            f"{label} must be a mapping"
        )

    actual = set(value.keys())
    expected = set(fields)

    if actual != expected:
        raise MAFQueryToPKSelectionError(
            f"{label} fields differ from frozen schema"
        )

    return value


def _require_text(
    value: Any,
    label: str,
) -> str:
    if type(value) is not str or not value:
        raise MAFQueryToPKSelectionError(
            f"{label} must be a non-empty string"
        )

    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise MAFQueryToPKSelectionError(
            f"{label} must be valid UTF-8 text"
        ) from exc

    return value


def _require_sha(
    value: Any,
    label: str,
) -> str:
    value = _require_text(value, label)

    if _SHA_RE.fullmatch(value) is None:
        raise MAFQueryToPKSelectionError(
            f"{label} must be 64 lowercase hexadecimal characters"
        )

    return value


def _require_generation_pk(value: Any) -> str:
    value = _require_text(
        value,
        "source_generation_pk",
    )

    if _GEN_RE.fullmatch(value) is None:
        raise MAFQueryToPKSelectionError(
            "source_generation_pk is not canonical"
        )

    return value


def _require_object_pk(
    value: Any,
    label: str = "object_pk",
) -> str:
    value = _require_text(value, label)

    if _OBJ_RE.fullmatch(value) is None:
        raise MAFQueryToPKSelectionError(
            f"{label} is not canonical"
        )

    return value


def _require_int(
    value: Any,
    label: str,
    *,
    minimum: int | None = None,
    maximum: int | None = None,
) -> int:
    if type(value) is not int:
        raise MAFQueryToPKSelectionError(
            f"{label} must be an integer and not a boolean"
        )

    if minimum is not None and value < minimum:
        raise MAFQueryToPKSelectionError(
            f"{label} is below its minimum"
        )

    if maximum is not None and value > maximum:
        raise MAFQueryToPKSelectionError(
            f"{label} exceeds its maximum"
        )

    return value


def _sequence_tuple(
    value: Any,
    label: str,
) -> tuple[Any, ...]:
    if isinstance(
        value,
        (str, bytes, bytearray),
    ) or not isinstance(value, Sequence):
        raise MAFQueryToPKSelectionError(
            f"{label} must be a sequence"
        )

    return tuple(value)


def _require_unique(
    values: tuple[Any, ...],
    label: str,
) -> None:
    if len(values) != len(set(values)):
        raise MAFQueryToPKSelectionError(
            f"{label} must not contain duplicates"
        )


@dataclass(frozen=True, slots=True)
class MAFQueryPKCatalogEntryV1:
    object_pk: str
    tensor_name: str
    tensor_type: int
    dims: tuple[int, ...]
    element_count: int

    def __post_init__(self) -> None:
        object_pk = _require_object_pk(self.object_pk)

        tensor_name = _require_text(
            self.tensor_name,
            "tensor_name",
        )

        tensor_type = _require_int(
            self.tensor_type,
            "tensor_type",
        )

        raw_dims = _sequence_tuple(
            self.dims,
            "dims",
        )

        if not raw_dims:
            raise MAFQueryToPKSelectionError(
                "dims must not be empty"
            )

        dims = tuple(
            _require_int(
                value,
                "dimension",
                minimum=1,
            )
            for value in raw_dims
        )

        element_count = _require_int(
            self.element_count,
            "element_count",
            minimum=1,
        )

        object.__setattr__(
            self,
            "object_pk",
            object_pk,
        )
        object.__setattr__(
            self,
            "tensor_name",
            tensor_name,
        )
        object.__setattr__(
            self,
            "tensor_type",
            tensor_type,
        )
        object.__setattr__(
            self,
            "dims",
            dims,
        )
        object.__setattr__(
            self,
            "element_count",
            element_count,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "object_pk": self.object_pk,
            "tensor_name": self.tensor_name,
            "tensor_type": self.tensor_type,
            "dims": list(self.dims),
            "element_count": self.element_count,
        }

    @classmethod
    def from_mapping(
        cls,
        value: Mapping[str, Any],
    ) -> "MAFQueryPKCatalogEntryV1":
        value = _require_mapping(
            value,
            CATALOG_ENTRY_FIELDS,
            "catalog entry",
        )

        return cls(
            object_pk=value["object_pk"],
            tensor_name=value["tensor_name"],
            tensor_type=value["tensor_type"],
            dims=value["dims"],
            element_count=value["element_count"],
        )


@dataclass(frozen=True, slots=True)
class MAFQueryPKCatalogV1:
    schema: str
    source_generation_pk: str
    source_manifest_sha256: str
    entries: tuple[MAFQueryPKCatalogEntryV1, ...]

    def __post_init__(self) -> None:
        if self.schema != CATALOG_SCHEMA:
            raise MAFQueryToPKSelectionError(
                "catalog schema mismatch"
            )

        generation_pk = _require_generation_pk(
            self.source_generation_pk
        )

        manifest_sha = _require_sha(
            self.source_manifest_sha256,
            "source_manifest_sha256",
        )

        raw_entries = _sequence_tuple(
            self.entries,
            "entries",
        )

        entries = tuple(
            item
            if isinstance(
                item,
                MAFQueryPKCatalogEntryV1,
            )
            else MAFQueryPKCatalogEntryV1.from_mapping(item)
            for item in raw_entries
        )

        pks = tuple(
            entry.object_pk
            for entry in entries
        )

        _require_unique(
            pks,
            "catalog object PKs",
        )

        if pks != tuple(sorted(pks)):
            raise MAFQueryToPKSelectionError(
                "catalog entries must be sorted by object_pk"
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
            "entries",
            entries,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "source_generation_pk": self.source_generation_pk,
            "source_manifest_sha256": self.source_manifest_sha256,
            "entries": [
                entry.to_dict()
                for entry in self.entries
            ],
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_bytes(
            self.to_dict()
        )

    @property
    def catalog_sha256(self) -> str:
        return hashlib.sha256(
            self.canonical_bytes()
        ).hexdigest()

    def require_source_binding(
        self,
        *,
        source_generation_pk: str,
        source_manifest_sha256: str,
    ) -> None:
        source_generation_pk = _require_generation_pk(
            source_generation_pk
        )
        source_manifest_sha256 = _require_sha(
            source_manifest_sha256,
            "source_manifest_sha256",
        )

        if (
            source_generation_pk
            != self.source_generation_pk
        ):
            raise MAFQueryToPKSelectionError(
                "catalog generation binding mismatch"
            )

        if (
            source_manifest_sha256
            != self.source_manifest_sha256
        ):
            raise MAFQueryToPKSelectionError(
                "catalog manifest binding mismatch"
            )

    @classmethod
    def from_mapping(
        cls,
        value: Mapping[str, Any],
    ) -> "MAFQueryPKCatalogV1":
        value = _require_mapping(
            value,
            CATALOG_FIELDS,
            "catalog",
        )

        return cls(
            schema=value["schema"],
            source_generation_pk=value["source_generation_pk"],
            source_manifest_sha256=value[
                "source_manifest_sha256"
            ],
            entries=value["entries"],
        )


@dataclass(frozen=True, slots=True)
class MAFQueryToPKSelectionConfigV1:
    schema: str
    max_candidates: int
    normalization_version: str
    alias_version: str
    descriptor_version: str
    ranking_version: str
    fallback_version: str

    def __post_init__(self) -> None:
        if self.schema != CONFIG_SCHEMA:
            raise MAFQueryToPKSelectionError(
                "selection configuration schema mismatch"
            )

        max_candidates = _require_int(
            self.max_candidates,
            "max_candidates",
            minimum=1,
            maximum=MAX_CANDIDATE_LIMIT,
        )

        expected = {
            "normalization_version": NORMALIZATION_VERSION,
            "alias_version": ALIAS_VERSION,
            "descriptor_version": DESCRIPTOR_VERSION,
            "ranking_version": RANKING_VERSION,
            "fallback_version": FALLBACK_VERSION,
        }

        for field, required in expected.items():
            if getattr(self, field) != required:
                raise MAFQueryToPKSelectionError(
                    f"{field} mismatch"
                )

        object.__setattr__(
            self,
            "max_candidates",
            max_candidates,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "max_candidates": self.max_candidates,
            "normalization_version": self.normalization_version,
            "alias_version": self.alias_version,
            "descriptor_version": self.descriptor_version,
            "ranking_version": self.ranking_version,
            "fallback_version": self.fallback_version,
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_bytes(
            self.to_dict()
        )

    @property
    def selection_config_sha256(self) -> str:
        return hashlib.sha256(
            self.canonical_bytes()
        ).hexdigest()

    @classmethod
    def from_mapping(
        cls,
        value: Mapping[str, Any],
    ) -> "MAFQueryToPKSelectionConfigV1":
        value = _require_mapping(
            value,
            CONFIG_FIELDS,
            "selection configuration",
        )

        return cls(
            schema=value["schema"],
            max_candidates=value["max_candidates"],
            normalization_version=value[
                "normalization_version"
            ],
            alias_version=value["alias_version"],
            descriptor_version=value[
                "descriptor_version"
            ],
            ranking_version=value["ranking_version"],
            fallback_version=value["fallback_version"],
        )


@dataclass(frozen=True, slots=True)
class MAFQueryToPKSelectionResultV1:
    schema: str
    query_signature: str
    source_generation_pk: str
    source_manifest_sha256: str
    catalog_sha256: str
    selection_config_sha256: str
    recognized_layer: int | None
    recognized_tags: tuple[str, ...]
    fallback_used: bool
    selected_object_pks: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.schema != RESULT_SCHEMA:
            raise MAFQueryToPKSelectionError(
                "selection result schema mismatch"
            )

        query_signature = _require_sha(
            self.query_signature,
            "query_signature",
        )

        generation_pk = _require_generation_pk(
            self.source_generation_pk
        )

        manifest_sha = _require_sha(
            self.source_manifest_sha256,
            "source_manifest_sha256",
        )

        catalog_sha = _require_sha(
            self.catalog_sha256,
            "catalog_sha256",
        )

        config_sha = _require_sha(
            self.selection_config_sha256,
            "selection_config_sha256",
        )

        if self.recognized_layer is None:
            recognized_layer = None
        else:
            recognized_layer = _require_int(
                self.recognized_layer,
                "recognized_layer",
                minimum=0,
            )

        raw_tags = _sequence_tuple(
            self.recognized_tags,
            "recognized_tags",
        )

        tags = tuple(
            _require_text(
                value,
                "recognized tag",
            )
            for value in raw_tags
        )

        _require_unique(
            tags,
            "recognized_tags",
        )

        if any(
            tag not in TAG_ORDER
            for tag in tags
        ):
            raise MAFQueryToPKSelectionError(
                "recognized_tags contains unknown tag"
            )

        canonical_tags = tuple(
            tag
            for tag in TAG_ORDER
            if tag in set(tags)
        )

        if tags != canonical_tags:
            raise MAFQueryToPKSelectionError(
                "recognized_tags order is not canonical"
            )

        if type(self.fallback_used) is not bool:
            raise MAFQueryToPKSelectionError(
                "fallback_used must be boolean"
            )

        raw_pks = _sequence_tuple(
            self.selected_object_pks,
            "selected_object_pks",
        )

        selected_pks = tuple(
            _require_object_pk(
                value,
                "selected_object_pk",
            )
            for value in raw_pks
        )

        _require_unique(
            selected_pks,
            "selected_object_pks",
        )

        object.__setattr__(
            self,
            "query_signature",
            query_signature,
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
            "catalog_sha256",
            catalog_sha,
        )
        object.__setattr__(
            self,
            "selection_config_sha256",
            config_sha,
        )
        object.__setattr__(
            self,
            "recognized_layer",
            recognized_layer,
        )
        object.__setattr__(
            self,
            "recognized_tags",
            tags,
        )
        object.__setattr__(
            self,
            "selected_object_pks",
            selected_pks,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "query_signature": self.query_signature,
            "source_generation_pk": self.source_generation_pk,
            "source_manifest_sha256": self.source_manifest_sha256,
            "catalog_sha256": self.catalog_sha256,
            "selection_config_sha256": self.selection_config_sha256,
            "recognized_layer": self.recognized_layer,
            "recognized_tags": list(self.recognized_tags),
            "fallback_used": self.fallback_used,
            "selected_object_pks": list(
                self.selected_object_pks
            ),
        }

    def canonical_bytes(self) -> bytes:
        return _canonical_bytes(
            self.to_dict()
        )

    @classmethod
    def from_mapping(
        cls,
        value: Mapping[str, Any],
    ) -> "MAFQueryToPKSelectionResultV1":
        value = _require_mapping(
            value,
            RESULT_FIELDS,
            "selection result",
        )

        return cls(
            schema=value["schema"],
            query_signature=value["query_signature"],
            source_generation_pk=value["source_generation_pk"],
            source_manifest_sha256=value[
                "source_manifest_sha256"
            ],
            catalog_sha256=value["catalog_sha256"],
            selection_config_sha256=value[
                "selection_config_sha256"
            ],
            recognized_layer=value["recognized_layer"],
            recognized_tags=value["recognized_tags"],
            fallback_used=value["fallback_used"],
            selected_object_pks=value[
                "selected_object_pks"
            ],
        )


def default_selection_config_v1(
    *,
    max_candidates: int,
) -> MAFQueryToPKSelectionConfigV1:
    return MAFQueryToPKSelectionConfigV1(
        schema=CONFIG_SCHEMA,
        max_candidates=max_candidates,
        normalization_version=NORMALIZATION_VERSION,
        alias_version=ALIAS_VERSION,
        descriptor_version=DESCRIPTOR_VERSION,
        ranking_version=RANKING_VERSION,
        fallback_version=FALLBACK_VERSION,
    )


def normalize_query_v1(query: str) -> str:
    query = _require_text(
        query,
        "query",
    )

    value = unicodedata.normalize(
        "NFKC",
        query,
    ).casefold()

    value = "".join(
        " "
        if char in "._/-"
        else char
        for char in value
    )

    value = "".join(
        char
        if char.isalnum()
        else " "
        for char in value
    )

    value = " ".join(
        value.split()
    )

    if not value:
        raise MAFQueryToPKSelectionError(
            "normalized query is empty"
        )

    return value


def derive_query_signature_v1(
    query: str,
) -> str:
    normalized = normalize_query_v1(
        query
    )

    return hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()


def parse_query_intent_v1(
    query: str,
) -> tuple[str, int | None, tuple[str, ...]]:
    normalized = normalize_query_v1(
        query
    )

    tokens = tuple(
        normalized.split(" ")
    )

    layer_values: set[int] = set()

    for index in range(
        len(tokens) - 1
    ):
        if tokens[index] not in {
            "layer",
            "block",
            "blk",
        }:
            continue

        number = tokens[index + 1]

        if _ASCII_DECIMAL_RE.fullmatch(number):
            layer_values.add(
                int(number)
            )

    if len(layer_values) > 1:
        raise MAFQueryToPKSelectionError(
            "query contains multiple distinct layer intents"
        )

    recognized_layer = (
        next(iter(layer_values))
        if layer_values
        else None
    )

    tags: set[str] = set()

    for phrase, tag in _QUERY_PHRASES:
        width = len(phrase)

        for index in range(
            0,
            len(tokens) - width + 1,
        ):
            if (
                tokens[index:index + width]
                == phrase
            ):
                tags.add(tag)

    for token in tokens:
        tag = _QUERY_SINGLE.get(
            token
        )

        if tag is not None:
            tags.add(tag)

    ordered_tags = tuple(
        tag
        for tag in TAG_ORDER
        if tag in tags
    )

    return (
        normalized,
        recognized_layer,
        ordered_tags,
    )


def parse_tensor_descriptor_v1(
    tensor_name: str,
) -> tuple[int | None, frozenset[str]]:
    tensor_name = _require_text(
        tensor_name,
        "tensor_name",
    )

    folded = tensor_name.casefold()

    layers = {
        int(value)
        for value in _TENSOR_LAYER_RE.findall(
            folded
        )
    }

    recognized_layer = (
        next(iter(layers))
        if len(layers) == 1
        else None
    )

    tokens = tuple(
        token
        for token in _TENSOR_SPLIT_RE.split(
            folded
        )
        if token
    )

    tags = frozenset(
        _TENSOR_TAGS[token]
        for token in tokens
        if token in _TENSOR_TAGS
    )

    return (
        recognized_layer,
        tags,
    )


def select_query_to_pks_v1(
    *,
    query: str,
    catalog: MAFQueryPKCatalogV1,
    config: MAFQueryToPKSelectionConfigV1,
    source_generation_pk: str,
    source_manifest_sha256: str,
) -> MAFQueryToPKSelectionResultV1:
    if not isinstance(
        catalog,
        MAFQueryPKCatalogV1,
    ):
        raise MAFQueryToPKSelectionError(
            "catalog must be MAFQueryPKCatalogV1"
        )

    if not isinstance(
        config,
        MAFQueryToPKSelectionConfigV1,
    ):
        raise MAFQueryToPKSelectionError(
            "config must be MAFQueryToPKSelectionConfigV1"
        )

    catalog.require_source_binding(
        source_generation_pk=source_generation_pk,
        source_manifest_sha256=source_manifest_sha256,
    )

    (
        normalized,
        query_layer,
        query_tags,
    ) = parse_query_intent_v1(
        query
    )

    query_signature = hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()

    query_tag_set = frozenset(
        query_tags
    )

    eligible: list[
        tuple[int, str]
    ] = []

    if (
        query_layer is not None
        or query_tags
    ):
        for entry in catalog.entries:
            (
                candidate_layer,
                candidate_tags,
            ) = parse_tensor_descriptor_v1(
                entry.tensor_name
            )

            if (
                query_layer is not None
                and candidate_layer
                != query_layer
            ):
                continue

            if not query_tag_set.issubset(
                candidate_tags
            ):
                continue

            matched_tag_count = len(
                query_tags
            )

            extra_tag_count = len(
                candidate_tags
                - query_tag_set
            )

            layer_bonus = (
                1000
                if query_layer is not None
                else 0
            )

            score = (
                layer_bonus
                + 100 * matched_tag_count
                - extra_tag_count
            )

            eligible.append(
                (
                    -score,
                    entry.object_pk,
                )
            )

    if eligible:
        eligible.sort()

        selected = tuple(
            object_pk
            for _, object_pk in eligible[
                :config.max_candidates
            ]
        )

        fallback_used = False

    else:
        fallback_rank = []

        for entry in catalog.entries:
            digest = hashlib.sha256(
                (
                    query_signature
                    + "\0"
                    + entry.object_pk
                ).encode("utf-8")
            ).hexdigest()

            fallback_rank.append(
                (
                    digest,
                    entry.object_pk,
                )
            )

        fallback_rank.sort()

        selected = tuple(
            object_pk
            for _, object_pk in fallback_rank[
                :config.max_candidates
            ]
        )

        fallback_used = True

    return MAFQueryToPKSelectionResultV1(
        schema=RESULT_SCHEMA,
        query_signature=query_signature,
        source_generation_pk=catalog.source_generation_pk,
        source_manifest_sha256=(
            catalog.source_manifest_sha256
        ),
        catalog_sha256=catalog.catalog_sha256,
        selection_config_sha256=(
            config.selection_config_sha256
        ),
        recognized_layer=query_layer,
        recognized_tags=query_tags,
        fallback_used=fallback_used,
        selected_object_pks=selected,
    )
