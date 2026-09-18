from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from typing import Any, Sequence


DATA_MODEL_PROTOCOL_SHA256 = (
    "712caa2e7dfc948f607a4c8d68064fc838eb1f58701fc5206c52aaf8e6492bc4"
)

PARENT_PHASE6D_PROTOCOL_SHA256 = (
    "a4c1a1d4fe22f7e714efa331cec9cf4dbd3a9e178f2b28b3ddb9034387e210ae"
)

PHASE6C_ENGINE_SHA256 = (
    "4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9"
)

SNAPSHOT_SCHEMA = (
    "openmind.maf_segment_locality.telemetry_snapshot.v1"
)

AGGREGATION_VERSION = (
    "maf_segment_locality_aggregation_v1"
)

REPACK_PLAN_SCHEMA = (
    "openmind.maf_segment_locality.repack_plan.v1"
)

RESIDENCY_STATES = (
    "COLD_DISK",
    "MAPPED",
    "HOT_MAF",
    "HOT_DENSE",
)

_HEX = frozenset(
    "0123456789abcdef"
)


class MAFSegmentLocalityDataModelError(Exception):
    pass


class MAFSegmentLocalityValidationError(
    MAFSegmentLocalityDataModelError
):
    pass


class MAFSegmentLocalitySequenceError(
    MAFSegmentLocalityValidationError
):
    pass


class MAFSegmentLocalityPrefetchError(
    MAFSegmentLocalityValidationError
):
    pass


class MAFSegmentLocalityMetricError(
    MAFSegmentLocalityValidationError
):
    pass


class MAFSegmentLocalityPlanError(
    MAFSegmentLocalityValidationError
):
    pass


def canonical_json_bytes(
    value: Any,
) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode(
        "utf-8"
    )


def _require_plain_nonnegative_int(
    value: Any,
    name: str,
) -> int:
    if (
        type(value) is not int
        or value < 0
    ):
        raise MAFSegmentLocalityValidationError(
            f"{name} must be a plain non-negative integer"
        )

    return value


def _require_nonempty_str(
    value: Any,
    name: str,
) -> str:
    if (
        not isinstance(
            value,
            str,
        )
        or not value
    ):
        raise MAFSegmentLocalityValidationError(
            f"{name} must be a non-empty string"
        )

    return value


def _require_sha256(
    value: Any,
    name: str,
) -> str:
    value = _require_nonempty_str(
        value,
        name,
    )

    if (
        len(value) != 64
        or any(
            ch not in _HEX
            for ch in value
        )
    ):
        raise MAFSegmentLocalityValidationError(
            f"{name} must be 64 lowercase hexadecimal characters"
        )

    return value


def _require_pk(
    value: Any,
    prefix: str,
    name: str,
) -> str:
    value = _require_nonempty_str(
        value,
        name,
    )

    if not value.startswith(
        prefix
    ):
        raise MAFSegmentLocalityValidationError(
            f"{name} must begin with {prefix!r}"
        )

    suffix = value[
        len(prefix):
    ]

    if (
        len(suffix) != 64
        or any(
            ch not in _HEX
            for ch in suffix
        )
    ):
        raise MAFSegmentLocalityValidationError(
            f"{name} must end in a 64-character lowercase SHA256"
        )

    return value


def _require_model_pk(
    value: Any,
) -> str:
    return _require_pk(
        value,
        "mafmodel:v1:",
        "model_pk",
    )


def _require_generation_pk(
    value: Any,
) -> str:
    return _require_pk(
        value,
        "mafgen:v1:",
        "source_generation_pk",
    )


def _require_object_pk(
    value: Any,
) -> str:
    return _require_pk(
        value,
        "mafobj:v1:",
        "object_pk",
    )


def _require_optional_none(
    values: Sequence[
        tuple[
            str,
            Any,
        ]
    ],
) -> None:
    for name, value in values:
        if value is not None:
            raise MAFSegmentLocalityValidationError(
                f"{name} must be null for this event kind"
            )


class TelemetryEventKind(
    str,
    Enum,
):
    ACCESS = "ACCESS"
    MATERIALIZATION = "MATERIALIZATION"
    BYTES_READ = "BYTES_READ"
    CACHE_HIT = "CACHE_HIT"
    CACHE_MISS = "CACHE_MISS"
    PROMOTION = "PROMOTION"
    DEMOTION = "DEMOTION"
    PREFETCH_ISSUED = "PREFETCH_ISSUED"
    PREFETCH_CONSUMED = "PREFETCH_CONSUMED"
    PREFETCH_UNUSED = "PREFETCH_UNUSED"


class LocalityMetricId(
    str,
    Enum,
):
    WEIGHTED_TRANSITION_RANK_DISTANCE = (
        "WEIGHTED_TRANSITION_RANK_DISTANCE"
    )
    CROSS_SEGMENT_FRACTION = (
        "CROSS_SEGMENT_FRACTION"
    )
    CO_SEGMENT_FRACTION = (
        "CO_SEGMENT_FRACTION"
    )


@dataclass(
    frozen=True,
    slots=True,
)
class TelemetryEvent:
    sequence: int
    kind: TelemetryEventKind
    object_pk: str
    byte_count: int | None = None
    cache_name: str | None = None
    from_state: str | None = None
    to_state: str | None = None
    prefetch_id: str | None = None

    def __post_init__(
        self,
    ) -> None:
        _require_plain_nonnegative_int(
            self.sequence,
            "sequence",
        )

        if not isinstance(
            self.kind,
            TelemetryEventKind,
        ):
            raise MAFSegmentLocalityValidationError(
                "kind must be a TelemetryEventKind"
            )

        _require_object_pk(
            self.object_pk
        )

        if self.kind in (
            TelemetryEventKind.ACCESS,
            TelemetryEventKind.MATERIALIZATION,
        ):
            _require_optional_none(
                (
                    (
                        "byte_count",
                        self.byte_count,
                    ),
                    (
                        "cache_name",
                        self.cache_name,
                    ),
                    (
                        "from_state",
                        self.from_state,
                    ),
                    (
                        "to_state",
                        self.to_state,
                    ),
                    (
                        "prefetch_id",
                        self.prefetch_id,
                    ),
                )
            )
            return

        if (
            self.kind
            is TelemetryEventKind.BYTES_READ
        ):
            _require_plain_nonnegative_int(
                self.byte_count,
                "byte_count",
            )

            _require_optional_none(
                (
                    (
                        "cache_name",
                        self.cache_name,
                    ),
                    (
                        "from_state",
                        self.from_state,
                    ),
                    (
                        "to_state",
                        self.to_state,
                    ),
                    (
                        "prefetch_id",
                        self.prefetch_id,
                    ),
                )
            )
            return

        if self.kind in (
            TelemetryEventKind.CACHE_HIT,
            TelemetryEventKind.CACHE_MISS,
        ):
            _require_nonempty_str(
                self.cache_name,
                "cache_name",
            )

            _require_optional_none(
                (
                    (
                        "byte_count",
                        self.byte_count,
                    ),
                    (
                        "from_state",
                        self.from_state,
                    ),
                    (
                        "to_state",
                        self.to_state,
                    ),
                    (
                        "prefetch_id",
                        self.prefetch_id,
                    ),
                )
            )
            return

        if self.kind in (
            TelemetryEventKind.PROMOTION,
            TelemetryEventKind.DEMOTION,
        ):
            if (
                self.from_state
                not in RESIDENCY_STATES
            ):
                raise MAFSegmentLocalityValidationError(
                    "from_state must use the frozen residency-state vocabulary"
                )

            if (
                self.to_state
                not in RESIDENCY_STATES
            ):
                raise MAFSegmentLocalityValidationError(
                    "to_state must use the frozen residency-state vocabulary"
                )

            _require_optional_none(
                (
                    (
                        "byte_count",
                        self.byte_count,
                    ),
                    (
                        "cache_name",
                        self.cache_name,
                    ),
                    (
                        "prefetch_id",
                        self.prefetch_id,
                    ),
                )
            )
            return

        if self.kind in (
            TelemetryEventKind.PREFETCH_ISSUED,
            TelemetryEventKind.PREFETCH_CONSUMED,
            TelemetryEventKind.PREFETCH_UNUSED,
        ):
            _require_nonempty_str(
                self.prefetch_id,
                "prefetch_id",
            )

            _require_optional_none(
                (
                    (
                        "byte_count",
                        self.byte_count,
                    ),
                    (
                        "cache_name",
                        self.cache_name,
                    ),
                    (
                        "from_state",
                        self.from_state,
                    ),
                    (
                        "to_state",
                        self.to_state,
                    ),
                )
            )
            return

        raise MAFSegmentLocalityValidationError(
            "unsupported telemetry event kind"
        )


@dataclass(
    frozen=True,
    slots=True,
)
class ObjectTelemetryAggregate:
    object_pk: str
    access_count: int
    reuse_interval_count: int
    reuse_interval_sum: int
    reuse_interval_min: int | None
    reuse_interval_max: int | None
    materialization_count: int
    bytes_read: int

    def __post_init__(
        self,
    ) -> None:
        _require_object_pk(
            self.object_pk
        )

        _require_plain_nonnegative_int(
            self.access_count,
            "access_count",
        )

        _require_plain_nonnegative_int(
            self.reuse_interval_count,
            "reuse_interval_count",
        )

        _require_plain_nonnegative_int(
            self.reuse_interval_sum,
            "reuse_interval_sum",
        )

        _require_plain_nonnegative_int(
            self.materialization_count,
            "materialization_count",
        )

        _require_plain_nonnegative_int(
            self.bytes_read,
            "bytes_read",
        )

        if (
            self.reuse_interval_count
            == 0
        ):
            if (
                self.reuse_interval_sum
                != 0
            ):
                raise MAFSegmentLocalityValidationError(
                    "zero reuse count requires zero reuse sum"
                )

            if (
                self.reuse_interval_min
                is not None
                or self.reuse_interval_max
                is not None
            ):
                raise MAFSegmentLocalityValidationError(
                    "zero reuse count requires null min/max"
                )

        else:
            _require_plain_nonnegative_int(
                self.reuse_interval_min,
                "reuse_interval_min",
            )

            _require_plain_nonnegative_int(
                self.reuse_interval_max,
                "reuse_interval_max",
            )

            if (
                self.reuse_interval_min
                > self.reuse_interval_max
            ):
                raise MAFSegmentLocalityValidationError(
                    "reuse interval min exceeds max"
                )


@dataclass(
    frozen=True,
    slots=True,
)
class TransitionTelemetryAggregate:
    source_object_pk: str
    target_object_pk: str
    count: int

    def __post_init__(
        self,
    ) -> None:
        _require_object_pk(
            self.source_object_pk
        )

        _require_object_pk(
            self.target_object_pk
        )

        _require_plain_nonnegative_int(
            self.count,
            "count",
        )


@dataclass(
    frozen=True,
    slots=True,
)
class CacheTelemetryAggregate:
    cache_name: str
    object_pk: str
    hit_count: int
    miss_count: int

    def __post_init__(
        self,
    ) -> None:
        _require_nonempty_str(
            self.cache_name,
            "cache_name",
        )

        _require_object_pk(
            self.object_pk
        )

        _require_plain_nonnegative_int(
            self.hit_count,
            "hit_count",
        )

        _require_plain_nonnegative_int(
            self.miss_count,
            "miss_count",
        )


@dataclass(
    frozen=True,
    slots=True,
)
class ResidencyTransitionAggregate:
    object_pk: str
    from_state: str
    to_state: str
    count: int

    def __post_init__(
        self,
    ) -> None:
        _require_object_pk(
            self.object_pk
        )

        if (
            self.from_state
            not in RESIDENCY_STATES
        ):
            raise MAFSegmentLocalityValidationError(
                "from_state must use the frozen residency-state vocabulary"
            )

        if (
            self.to_state
            not in RESIDENCY_STATES
        ):
            raise MAFSegmentLocalityValidationError(
                "to_state must use the frozen residency-state vocabulary"
            )

        _require_plain_nonnegative_int(
            self.count,
            "count",
        )


@dataclass(
    frozen=True,
    slots=True,
)
class PrefetchTelemetryAggregate:
    object_pk: str
    issued_count: int
    consumed_count: int
    unused_count: int

    def __post_init__(
        self,
    ) -> None:
        _require_object_pk(
            self.object_pk
        )

        _require_plain_nonnegative_int(
            self.issued_count,
            "issued_count",
        )

        _require_plain_nonnegative_int(
            self.consumed_count,
            "consumed_count",
        )

        _require_plain_nonnegative_int(
            self.unused_count,
            "unused_count",
        )

        if (
            self.consumed_count
            + self.unused_count
            > self.issued_count
        ):
            raise MAFSegmentLocalityValidationError(
                "prefetch terminal count exceeds issued count"
            )


def _require_tuple_of(
    value: Any,
    cls: type,
    name: str,
) -> tuple[Any, ...]:
    if not isinstance(
        value,
        tuple,
    ):
        raise MAFSegmentLocalityValidationError(
            f"{name} must be a tuple"
        )

    if any(
        not isinstance(
            item,
            cls,
        )
        for item in value
    ):
        raise MAFSegmentLocalityValidationError(
            f"{name} contains an invalid value"
        )

    return value


def _require_sorted_unique(
    items: tuple[Any, ...],
    key,
    name: str,
) -> None:
    keys = tuple(
        key(item)
        for item in items
    )

    if keys != tuple(
        sorted(keys)
    ):
        raise MAFSegmentLocalityValidationError(
            f"{name} is not in canonical order"
        )

    if (
        len(set(keys))
        != len(keys)
    ):
        raise MAFSegmentLocalityValidationError(
            f"{name} contains duplicate keys"
        )


@dataclass(
    frozen=True,
    slots=True,
)
class TelemetrySnapshot:
    schema: str
    aggregation_version: str
    model_pk: str
    source_generation_pk: str
    source_manifest_sha256: str
    first_sequence: int | None
    last_sequence: int | None
    event_count: int
    access_event_count: int
    object_aggregates: tuple[
        ObjectTelemetryAggregate,
        ...,
    ]
    transition_aggregates: tuple[
        TransitionTelemetryAggregate,
        ...,
    ]
    cache_aggregates: tuple[
        CacheTelemetryAggregate,
        ...,
    ]
    residency_transition_aggregates: tuple[
        ResidencyTransitionAggregate,
        ...,
    ]
    prefetch_aggregates: tuple[
        PrefetchTelemetryAggregate,
        ...,
    ]

    def __post_init__(
        self,
    ) -> None:
        if (
            self.schema
            != SNAPSHOT_SCHEMA
        ):
            raise MAFSegmentLocalityValidationError(
                "invalid telemetry snapshot schema"
            )

        if (
            self.aggregation_version
            != AGGREGATION_VERSION
        ):
            raise MAFSegmentLocalityValidationError(
                "invalid aggregation version"
            )

        _require_model_pk(
            self.model_pk
        )

        _require_generation_pk(
            self.source_generation_pk
        )

        _require_sha256(
            self.source_manifest_sha256,
            "source_manifest_sha256",
        )

        _require_plain_nonnegative_int(
            self.event_count,
            "event_count",
        )

        _require_plain_nonnegative_int(
            self.access_event_count,
            "access_event_count",
        )

        if (
            self.access_event_count
            > self.event_count
        ):
            raise MAFSegmentLocalityValidationError(
                "access_event_count exceeds event_count"
            )

        objects = _require_tuple_of(
            self.object_aggregates,
            ObjectTelemetryAggregate,
            "object_aggregates",
        )

        transitions = _require_tuple_of(
            self.transition_aggregates,
            TransitionTelemetryAggregate,
            "transition_aggregates",
        )

        caches = _require_tuple_of(
            self.cache_aggregates,
            CacheTelemetryAggregate,
            "cache_aggregates",
        )

        residency = _require_tuple_of(
            self.residency_transition_aggregates,
            ResidencyTransitionAggregate,
            "residency_transition_aggregates",
        )

        prefetch = _require_tuple_of(
            self.prefetch_aggregates,
            PrefetchTelemetryAggregate,
            "prefetch_aggregates",
        )

        _require_sorted_unique(
            objects,
            lambda item:
                item.object_pk,
            "object_aggregates",
        )

        _require_sorted_unique(
            transitions,
            lambda item: (
                item.source_object_pk,
                item.target_object_pk,
            ),
            "transition_aggregates",
        )

        _require_sorted_unique(
            caches,
            lambda item: (
                item.cache_name,
                item.object_pk,
            ),
            "cache_aggregates",
        )

        _require_sorted_unique(
            residency,
            lambda item: (
                item.object_pk,
                item.from_state,
                item.to_state,
            ),
            "residency_transition_aggregates",
        )

        _require_sorted_unique(
            prefetch,
            lambda item:
                item.object_pk,
            "prefetch_aggregates",
        )

        if self.event_count == 0:
            if (
                self.first_sequence
                is not None
                or self.last_sequence
                is not None
            ):
                raise MAFSegmentLocalityValidationError(
                    "empty snapshot requires null sequence bounds"
                )

            if any(
                (
                    objects,
                    transitions,
                    caches,
                    residency,
                    prefetch,
                )
            ):
                raise MAFSegmentLocalityValidationError(
                    "empty snapshot requires empty aggregate tuples"
                )

        else:
            _require_plain_nonnegative_int(
                self.first_sequence,
                "first_sequence",
            )

            _require_plain_nonnegative_int(
                self.last_sequence,
                "last_sequence",
            )

            if (
                self.first_sequence
                > self.last_sequence
            ):
                raise MAFSegmentLocalityValidationError(
                    "first_sequence exceeds last_sequence"
                )


@dataclass(
    frozen=True,
    slots=True,
)
class ExactRatio:
    numerator: int
    denominator: int

    def __post_init__(
        self,
    ) -> None:
        _require_plain_nonnegative_int(
            self.numerator,
            "numerator",
        )

        _require_plain_nonnegative_int(
            self.denominator,
            "denominator",
        )


@dataclass(
    frozen=True,
    slots=True,
)
class LocalityMetricValue:
    metric_id: LocalityMetricId
    numerator: int
    denominator: int

    def __post_init__(
        self,
    ) -> None:
        if not isinstance(
            self.metric_id,
            LocalityMetricId,
        ):
            raise MAFSegmentLocalityMetricError(
                "metric_id must be a LocalityMetricId"
            )

        _require_plain_nonnegative_int(
            self.numerator,
            "numerator",
        )

        _require_plain_nonnegative_int(
            self.denominator,
            "denominator",
        )

        if self.denominator == 0:
            raise MAFSegmentLocalityMetricError(
                "metric denominator must be non-zero"
            )

    def as_ratio(
        self,
    ) -> ExactRatio:
        return ExactRatio(
            numerator=self.numerator,
            denominator=self.denominator,
        )


@dataclass(
    frozen=True,
    slots=True,
)
class RepackPlacement:
    object_pk: str
    target_segment_ordinal: int
    target_object_ordinal: int

    def __post_init__(
        self,
    ) -> None:
        _require_object_pk(
            self.object_pk
        )

        _require_plain_nonnegative_int(
            self.target_segment_ordinal,
            "target_segment_ordinal",
        )

        _require_plain_nonnegative_int(
            self.target_object_ordinal,
            "target_object_ordinal",
        )


@dataclass(
    frozen=True,
    slots=True,
)
class PlannerConfigEntry:
    key: str
    canonical_value_json: str

    def __post_init__(
        self,
    ) -> None:
        _require_nonempty_str(
            self.key,
            "key",
        )

        raw = _require_nonempty_str(
            self.canonical_value_json,
            "canonical_value_json",
        )

        try:
            value = json.loads(
                raw
            )

        except Exception as exc:
            raise MAFSegmentLocalityPlanError(
                "canonical_value_json is not valid JSON"
            ) from exc

        canonical = canonical_json_bytes(
            value
        ).decode(
            "utf-8"
        )

        if canonical != raw:
            raise MAFSegmentLocalityPlanError(
                "canonical_value_json is not canonical JSON"
            )


def _validate_placements(
    placements: Sequence[
        RepackPlacement
    ],
    *,
    require_canonical: bool,
) -> tuple[
    RepackPlacement,
    ...,
]:
    values = tuple(
        placements
    )

    if any(
        not isinstance(
            item,
            RepackPlacement,
        )
        for item in values
    ):
        raise MAFSegmentLocalityPlanError(
            "placements contain an invalid value"
        )

    object_pks = tuple(
        item.object_pk
        for item in values
    )

    if (
        len(set(object_pks))
        != len(object_pks)
    ):
        raise MAFSegmentLocalityPlanError(
            "placements contain duplicate object PKs"
        )

    coordinates = tuple(
        (
            item.target_segment_ordinal,
            item.target_object_ordinal,
        )
        for item in values
    )

    if (
        len(set(coordinates))
        != len(coordinates)
    ):
        raise MAFSegmentLocalityPlanError(
            "placements contain duplicate coordinates"
        )

    canonical = tuple(
        sorted(
            values,
            key=lambda item: (
                item.target_segment_ordinal,
                item.target_object_ordinal,
                item.object_pk,
            ),
        )
    )

    if (
        require_canonical
        and values != canonical
    ):
        raise MAFSegmentLocalityPlanError(
            "placements are not in canonical order"
        )

    if values:
        segment_ordinals = sorted(
            {
                item.target_segment_ordinal
                for item in values
            }
        )

        if (
            segment_ordinals
            != list(
                range(
                    len(
                        segment_ordinals
                    )
                )
            )
        ):
            raise MAFSegmentLocalityPlanError(
                "target segment ordinals are not contiguous from zero"
            )

        for segment_ordinal in segment_ordinals:
            object_ordinals = sorted(
                item.target_object_ordinal
                for item in values
                if (
                    item.target_segment_ordinal
                    == segment_ordinal
                )
            )

            if (
                object_ordinals
                != list(
                    range(
                        len(
                            object_ordinals
                        )
                    )
                )
            ):
                raise MAFSegmentLocalityPlanError(
                    "target object ordinals are not contiguous from zero"
                )

    return canonical


@dataclass(
    frozen=True,
    slots=True,
)
class RepackPlan:
    schema: str
    planner_version: str
    model_pk: str
    source_generation_pk: str
    source_manifest_sha256: str
    telemetry_snapshot_sha256: str
    objective_metric_id: LocalityMetricId
    planner_config: tuple[
        PlannerConfigEntry,
        ...,
    ]
    placements: tuple[
        RepackPlacement,
        ...,
    ]

    def __post_init__(
        self,
    ) -> None:
        if (
            self.schema
            != REPACK_PLAN_SCHEMA
        ):
            raise MAFSegmentLocalityPlanError(
                "invalid repack-plan schema"
            )

        _require_nonempty_str(
            self.planner_version,
            "planner_version",
        )

        _require_model_pk(
            self.model_pk
        )

        _require_generation_pk(
            self.source_generation_pk
        )

        _require_sha256(
            self.source_manifest_sha256,
            "source_manifest_sha256",
        )

        _require_sha256(
            self.telemetry_snapshot_sha256,
            "telemetry_snapshot_sha256",
        )

        if not isinstance(
            self.objective_metric_id,
            LocalityMetricId,
        ):
            raise MAFSegmentLocalityPlanError(
                "objective_metric_id must be a LocalityMetricId"
            )

        config = _require_tuple_of(
            self.planner_config,
            PlannerConfigEntry,
            "planner_config",
        )

        _require_sorted_unique(
            config,
            lambda item:
                item.key,
            "planner_config",
        )

        placements = _require_tuple_of(
            self.placements,
            RepackPlacement,
            "placements",
        )

        _validate_placements(
            placements,
            require_canonical=True,
        )


def _empty_object_state() -> dict[
    str,
    Any,
]:
    return {
        "access_count": 0,
        "reuse_interval_count": 0,
        "reuse_interval_sum": 0,
        "reuse_interval_min": None,
        "reuse_interval_max": None,
        "materialization_count": 0,
        "bytes_read": 0,
    }


def _copy_nested_int_dict(
    source: dict[
        Any,
        dict[
            str,
            int,
        ],
    ],
) -> dict[
    Any,
    dict[
        str,
        int,
    ],
]:
    return {
        key: dict(value)
        for key, value
        in source.items()
    }


class TelemetryAccumulator:
    __slots__ = (
        "_model_pk",
        "_source_generation_pk",
        "_source_manifest_sha256",
        "_first_sequence",
        "_last_sequence",
        "_event_count",
        "_access_event_count",
        "_objects",
        "_transitions",
        "_caches",
        "_residency",
        "_prefetch_counts",
        "_prefetch_state",
        "_last_access_object",
        "_last_access_sequence_by_object",
    )

    def __init__(
        self,
        *,
        model_pk: str,
        source_generation_pk: str,
        source_manifest_sha256: str,
    ) -> None:
        self._model_pk = (
            _require_model_pk(
                model_pk
            )
        )

        self._source_generation_pk = (
            _require_generation_pk(
                source_generation_pk
            )
        )

        self._source_manifest_sha256 = (
            _require_sha256(
                source_manifest_sha256,
                "source_manifest_sha256",
            )
        )

        self._first_sequence = None
        self._last_sequence = None
        self._event_count = 0
        self._access_event_count = 0

        self._objects: dict[
            str,
            dict[
                str,
                Any,
            ],
        ] = {}

        self._transitions: dict[
            tuple[
                str,
                str,
            ],
            int,
        ] = {}

        self._caches: dict[
            tuple[
                str,
                str,
            ],
            dict[
                str,
                int,
            ],
        ] = {}

        self._residency: dict[
            tuple[
                str,
                str,
                str,
            ],
            int,
        ] = {}

        self._prefetch_counts: dict[
            str,
            dict[
                str,
                int,
            ],
        ] = {}

        self._prefetch_state: dict[
            str,
            tuple[
                str,
                str,
            ],
        ] = {}

        self._last_access_object: (
            str
            | None
        ) = None

        self._last_access_sequence_by_object: dict[
            str,
            int,
        ] = {}

    def _validate_commit_preconditions(
        self,
        event: TelemetryEvent,
    ) -> None:
        if not isinstance(
            event,
            TelemetryEvent,
        ):
            raise MAFSegmentLocalityValidationError(
                "event must be a TelemetryEvent"
            )

        if (
            self._last_sequence
            is not None
            and event.sequence
            <= self._last_sequence
        ):
            raise MAFSegmentLocalitySequenceError(
                "event sequence must strictly increase"
            )

        if (
            event.kind
            is TelemetryEventKind.PREFETCH_ISSUED
        ):
            if (
                event.prefetch_id
                in self._prefetch_state
            ):
                raise MAFSegmentLocalityPrefetchError(
                    "prefetch_id was already issued"
                )

        if event.kind in (
            TelemetryEventKind.PREFETCH_CONSUMED,
            TelemetryEventKind.PREFETCH_UNUSED,
        ):
            state = self._prefetch_state.get(
                event.prefetch_id
            )

            if state is None:
                raise MAFSegmentLocalityPrefetchError(
                    "prefetch terminal event references an unknown ID"
                )

            (
                issued_object_pk,
                resolution,
            ) = state

            if (
                issued_object_pk
                != event.object_pk
            ):
                raise MAFSegmentLocalityPrefetchError(
                    "prefetch terminal event object does not match issue"
                )

            if (
                resolution
                != "ISSUED"
            ):
                raise MAFSegmentLocalityPrefetchError(
                    "prefetch ID already has a terminal resolution"
                )

    def add_event(
        self,
        event: TelemetryEvent,
    ) -> None:
        self._validate_commit_preconditions(
            event
        )

        objects = {
            key: dict(value)
            for key, value
            in self._objects.items()
        }

        transitions = dict(
            self._transitions
        )

        caches = _copy_nested_int_dict(
            self._caches
        )

        residency = dict(
            self._residency
        )

        prefetch_counts = (
            _copy_nested_int_dict(
                self._prefetch_counts
            )
        )

        prefetch_state = dict(
            self._prefetch_state
        )

        last_access_by_object = dict(
            self._last_access_sequence_by_object
        )

        first_sequence = (
            event.sequence
            if (
                self._first_sequence
                is None
            )
            else self._first_sequence
        )

        last_sequence = (
            event.sequence
        )

        event_count = (
            self._event_count
            + 1
        )

        access_event_count = (
            self._access_event_count
        )

        last_access_object = (
            self._last_access_object
        )

        object_state = objects.setdefault(
            event.object_pk,
            _empty_object_state(),
        )

        if (
            event.kind
            is TelemetryEventKind.ACCESS
        ):
            object_state[
                "access_count"
            ] += 1

            access_event_count += 1

            if (
                last_access_object
                is not None
            ):
                key = (
                    last_access_object,
                    event.object_pk,
                )

                transitions[
                    key
                ] = (
                    transitions.get(
                        key,
                        0,
                    )
                    + 1
                )

            previous_sequence = (
                last_access_by_object.get(
                    event.object_pk
                )
            )

            if (
                previous_sequence
                is not None
            ):
                interval = (
                    event.sequence
                    - previous_sequence
                )

                object_state[
                    "reuse_interval_count"
                ] += 1

                object_state[
                    "reuse_interval_sum"
                ] += interval

                current_min = (
                    object_state[
                        "reuse_interval_min"
                    ]
                )

                current_max = (
                    object_state[
                        "reuse_interval_max"
                    ]
                )

                object_state[
                    "reuse_interval_min"
                ] = (
                    interval
                    if current_min is None
                    else min(
                        current_min,
                        interval,
                    )
                )

                object_state[
                    "reuse_interval_max"
                ] = (
                    interval
                    if current_max is None
                    else max(
                        current_max,
                        interval,
                    )
                )

            last_access_by_object[
                event.object_pk
            ] = event.sequence

            last_access_object = (
                event.object_pk
            )

        elif (
            event.kind
            is TelemetryEventKind.MATERIALIZATION
        ):
            object_state[
                "materialization_count"
            ] += 1

        elif (
            event.kind
            is TelemetryEventKind.BYTES_READ
        ):
            object_state[
                "bytes_read"
            ] += event.byte_count

        elif event.kind in (
            TelemetryEventKind.CACHE_HIT,
            TelemetryEventKind.CACHE_MISS,
        ):
            key = (
                event.cache_name,
                event.object_pk,
            )

            cache_state = caches.setdefault(
                key,
                {
                    "hit_count": 0,
                    "miss_count": 0,
                },
            )

            if (
                event.kind
                is TelemetryEventKind.CACHE_HIT
            ):
                cache_state[
                    "hit_count"
                ] += 1

            else:
                cache_state[
                    "miss_count"
                ] += 1

        elif event.kind in (
            TelemetryEventKind.PROMOTION,
            TelemetryEventKind.DEMOTION,
        ):
            key = (
                event.object_pk,
                event.from_state,
                event.to_state,
            )

            residency[
                key
            ] = (
                residency.get(
                    key,
                    0,
                )
                + 1
            )

        elif (
            event.kind
            is TelemetryEventKind.PREFETCH_ISSUED
        ):
            state = prefetch_counts.setdefault(
                event.object_pk,
                {
                    "issued_count": 0,
                    "consumed_count": 0,
                    "unused_count": 0,
                },
            )

            state[
                "issued_count"
            ] += 1

            prefetch_state[
                event.prefetch_id
            ] = (
                event.object_pk,
                "ISSUED",
            )

        elif event.kind in (
            TelemetryEventKind.PREFETCH_CONSUMED,
            TelemetryEventKind.PREFETCH_UNUSED,
        ):
            state = prefetch_counts.setdefault(
                event.object_pk,
                {
                    "issued_count": 0,
                    "consumed_count": 0,
                    "unused_count": 0,
                },
            )

            if (
                event.kind
                is TelemetryEventKind.PREFETCH_CONSUMED
            ):
                state[
                    "consumed_count"
                ] += 1

                resolution = (
                    "CONSUMED"
                )

            else:
                state[
                    "unused_count"
                ] += 1

                resolution = (
                    "UNUSED"
                )

            prefetch_state[
                event.prefetch_id
            ] = (
                event.object_pk,
                resolution,
            )

        else:
            raise MAFSegmentLocalityValidationError(
                "unsupported event kind"
            )

        self._objects = objects
        self._transitions = transitions
        self._caches = caches
        self._residency = residency
        self._prefetch_counts = prefetch_counts
        self._prefetch_state = prefetch_state

        self._last_access_sequence_by_object = (
            last_access_by_object
        )

        self._first_sequence = (
            first_sequence
        )

        self._last_sequence = (
            last_sequence
        )

        self._event_count = (
            event_count
        )

        self._access_event_count = (
            access_event_count
        )

        self._last_access_object = (
            last_access_object
        )

    def snapshot(
        self,
    ) -> TelemetrySnapshot:
        objects = tuple(
            ObjectTelemetryAggregate(
                object_pk=object_pk,
                access_count=state[
                    "access_count"
                ],
                reuse_interval_count=state[
                    "reuse_interval_count"
                ],
                reuse_interval_sum=state[
                    "reuse_interval_sum"
                ],
                reuse_interval_min=state[
                    "reuse_interval_min"
                ],
                reuse_interval_max=state[
                    "reuse_interval_max"
                ],
                materialization_count=state[
                    "materialization_count"
                ],
                bytes_read=state[
                    "bytes_read"
                ],
            )
            for object_pk, state
            in sorted(
                self._objects.items()
            )
        )

        transitions = tuple(
            TransitionTelemetryAggregate(
                source_object_pk=source_pk,
                target_object_pk=target_pk,
                count=count,
            )
            for (
                source_pk,
                target_pk,
            ), count
            in sorted(
                self._transitions.items()
            )
        )

        caches = tuple(
            CacheTelemetryAggregate(
                cache_name=cache_name,
                object_pk=object_pk,
                hit_count=state[
                    "hit_count"
                ],
                miss_count=state[
                    "miss_count"
                ],
            )
            for (
                cache_name,
                object_pk,
            ), state
            in sorted(
                self._caches.items()
            )
        )

        residency = tuple(
            ResidencyTransitionAggregate(
                object_pk=object_pk,
                from_state=from_state,
                to_state=to_state,
                count=count,
            )
            for (
                object_pk,
                from_state,
                to_state,
            ), count
            in sorted(
                self._residency.items()
            )
        )

        prefetch = tuple(
            PrefetchTelemetryAggregate(
                object_pk=object_pk,
                issued_count=state[
                    "issued_count"
                ],
                consumed_count=state[
                    "consumed_count"
                ],
                unused_count=state[
                    "unused_count"
                ],
            )
            for object_pk, state
            in sorted(
                self._prefetch_counts.items()
            )
        )

        return TelemetrySnapshot(
            schema=SNAPSHOT_SCHEMA,
            aggregation_version=(
                AGGREGATION_VERSION
            ),
            model_pk=self._model_pk,
            source_generation_pk=(
                self._source_generation_pk
            ),
            source_manifest_sha256=(
                self._source_manifest_sha256
            ),
            first_sequence=(
                self._first_sequence
            ),
            last_sequence=(
                self._last_sequence
            ),
            event_count=(
                self._event_count
            ),
            access_event_count=(
                self._access_event_count
            ),
            object_aggregates=objects,
            transition_aggregates=(
                transitions
            ),
            cache_aggregates=caches,
            residency_transition_aggregates=(
                residency
            ),
            prefetch_aggregates=prefetch,
        )


def snapshot_payload(
    snapshot: TelemetrySnapshot,
) -> dict[
    str,
    Any,
]:
    if not isinstance(
        snapshot,
        TelemetrySnapshot,
    ):
        raise MAFSegmentLocalityValidationError(
            "snapshot must be a TelemetrySnapshot"
        )

    return {
        "schema":
            snapshot.schema,

        "aggregation_version":
            snapshot.aggregation_version,

        "model_pk":
            snapshot.model_pk,

        "source_generation_pk":
            snapshot.source_generation_pk,

        "source_manifest_sha256":
            snapshot.source_manifest_sha256,

        "first_sequence":
            snapshot.first_sequence,

        "last_sequence":
            snapshot.last_sequence,

        "event_count":
            snapshot.event_count,

        "access_event_count":
            snapshot.access_event_count,

        "object_aggregates": [
            {
                "object_pk":
                    item.object_pk,

                "access_count":
                    item.access_count,

                "reuse_interval_count":
                    item.reuse_interval_count,

                "reuse_interval_sum":
                    item.reuse_interval_sum,

                "reuse_interval_min":
                    item.reuse_interval_min,

                "reuse_interval_max":
                    item.reuse_interval_max,

                "materialization_count":
                    item.materialization_count,

                "bytes_read":
                    item.bytes_read,
            }
            for item
            in snapshot.object_aggregates
        ],

        "transition_aggregates": [
            {
                "source_object_pk":
                    item.source_object_pk,

                "target_object_pk":
                    item.target_object_pk,

                "count":
                    item.count,
            }
            for item
            in snapshot.transition_aggregates
        ],

        "cache_aggregates": [
            {
                "cache_name":
                    item.cache_name,

                "object_pk":
                    item.object_pk,

                "hit_count":
                    item.hit_count,

                "miss_count":
                    item.miss_count,
            }
            for item
            in snapshot.cache_aggregates
        ],

        "residency_transition_aggregates": [
            {
                "object_pk":
                    item.object_pk,

                "from_state":
                    item.from_state,

                "to_state":
                    item.to_state,

                "count":
                    item.count,
            }
            for item
            in snapshot.residency_transition_aggregates
        ],

        "prefetch_aggregates": [
            {
                "object_pk":
                    item.object_pk,

                "issued_count":
                    item.issued_count,

                "consumed_count":
                    item.consumed_count,

                "unused_count":
                    item.unused_count,
            }
            for item
            in snapshot.prefetch_aggregates
        ],
    }


def snapshot_sha256(
    snapshot: TelemetrySnapshot,
) -> str:
    return hashlib.sha256(
        canonical_json_bytes(
            snapshot_payload(
                snapshot
            )
        )
    ).hexdigest()


def _transition_tuple(
    transitions: Sequence[
        TransitionTelemetryAggregate
    ],
) -> tuple[
    TransitionTelemetryAggregate,
    ...,
]:
    values = tuple(
        transitions
    )

    if any(
        not isinstance(
            item,
            TransitionTelemetryAggregate,
        )
        for item in values
    ):
        raise MAFSegmentLocalityMetricError(
            "transitions contain an invalid value"
        )

    return values


def _placement_maps(
    placements: Sequence[
        RepackPlacement
    ],
) -> tuple[
    dict[
        str,
        int,
    ],
    dict[
        str,
        int,
    ],
]:
    canonical = _validate_placements(
        placements,
        require_canonical=False,
    )

    rank_map = {
        item.object_pk: rank
        for rank, item
        in enumerate(
            canonical
        )
    }

    segment_map = {
        item.object_pk:
            item.target_segment_ordinal
        for item
        in canonical
    }

    return (
        rank_map,
        segment_map,
    )


def weighted_transition_rank_distance(
    transitions: Sequence[
        TransitionTelemetryAggregate
    ],
    placements: Sequence[
        RepackPlacement
    ],
) -> LocalityMetricValue:
    values = _transition_tuple(
        transitions
    )

    rank_map, _ = (
        _placement_maps(
            placements
        )
    )

    numerator = 0
    denominator = 0

    for item in values:
        try:
            source_rank = (
                rank_map[
                    item.source_object_pk
                ]
            )

            target_rank = (
                rank_map[
                    item.target_object_pk
                ]
            )

        except KeyError as exc:
            raise MAFSegmentLocalityMetricError(
                "transition references an object absent from placements"
            ) from exc

        numerator += (
            item.count
            * abs(
                source_rank
                - target_rank
            )
        )

        denominator += (
            item.count
        )

    if denominator == 0:
        raise MAFSegmentLocalityMetricError(
            "weighted transition rank distance has zero denominator"
        )

    return LocalityMetricValue(
        metric_id=(
            LocalityMetricId
            .WEIGHTED_TRANSITION_RANK_DISTANCE
        ),
        numerator=numerator,
        denominator=denominator,
    )


def cross_segment_fraction(
    transitions: Sequence[
        TransitionTelemetryAggregate
    ],
    placements: Sequence[
        RepackPlacement
    ],
) -> LocalityMetricValue:
    values = _transition_tuple(
        transitions
    )

    _, segment_map = (
        _placement_maps(
            placements
        )
    )

    numerator = 0
    denominator = 0

    for item in values:
        try:
            source_segment = (
                segment_map[
                    item.source_object_pk
                ]
            )

            target_segment = (
                segment_map[
                    item.target_object_pk
                ]
            )

        except KeyError as exc:
            raise MAFSegmentLocalityMetricError(
                "transition references an object absent from placements"
            ) from exc

        denominator += (
            item.count
        )

        if (
            source_segment
            != target_segment
        ):
            numerator += (
                item.count
            )

    if denominator == 0:
        raise MAFSegmentLocalityMetricError(
            "cross-segment fraction has zero denominator"
        )

    return LocalityMetricValue(
        metric_id=(
            LocalityMetricId
            .CROSS_SEGMENT_FRACTION
        ),
        numerator=numerator,
        denominator=denominator,
    )


def co_segment_fraction(
    transitions: Sequence[
        TransitionTelemetryAggregate
    ],
    placements: Sequence[
        RepackPlacement
    ],
) -> LocalityMetricValue:
    values = _transition_tuple(
        transitions
    )

    _, segment_map = (
        _placement_maps(
            placements
        )
    )

    numerator = 0
    denominator = 0

    for item in values:
        try:
            source_segment = (
                segment_map[
                    item.source_object_pk
                ]
            )

            target_segment = (
                segment_map[
                    item.target_object_pk
                ]
            )

        except KeyError as exc:
            raise MAFSegmentLocalityMetricError(
                "transition references an object absent from placements"
            ) from exc

        denominator += (
            item.count
        )

        if (
            source_segment
            == target_segment
        ):
            numerator += (
                item.count
            )

    if denominator == 0:
        raise MAFSegmentLocalityMetricError(
            "co-segment fraction has zero denominator"
        )

    return LocalityMetricValue(
        metric_id=(
            LocalityMetricId
            .CO_SEGMENT_FRACTION
        ),
        numerator=numerator,
        denominator=denominator,
    )


def validate_complete_source_object_set(
    plan: RepackPlan,
    source_object_pks: Sequence[
        str
    ],
) -> bool:
    if not isinstance(
        plan,
        RepackPlan,
    ):
        raise MAFSegmentLocalityPlanError(
            "plan must be a RepackPlan"
        )

    source = tuple(
        source_object_pks
    )

    for object_pk in source:
        _require_object_pk(
            object_pk
        )

    if (
        len(set(source))
        != len(source)
    ):
        raise MAFSegmentLocalityPlanError(
            "source object set contains duplicates"
        )

    planned = tuple(
        item.object_pk
        for item
        in plan.placements
    )

    if (
        set(planned)
        != set(source)
    ):
        raise MAFSegmentLocalityPlanError(
            "plan does not preserve the exact source object set"
        )

    return True


def repack_plan_payload(
    plan: RepackPlan,
) -> dict[
    str,
    Any,
]:
    if not isinstance(
        plan,
        RepackPlan,
    ):
        raise MAFSegmentLocalityPlanError(
            "plan must be a RepackPlan"
        )

    return {
        "schema":
            plan.schema,

        "planner_version":
            plan.planner_version,

        "model_pk":
            plan.model_pk,

        "source_generation_pk":
            plan.source_generation_pk,

        "source_manifest_sha256":
            plan.source_manifest_sha256,

        "telemetry_snapshot_sha256":
            plan.telemetry_snapshot_sha256,

        "objective_metric_id":
            plan.objective_metric_id.value,

        "planner_config": [
            {
                "key":
                    item.key,

                "canonical_value_json":
                    item.canonical_value_json,
            }
            for item
            in plan.planner_config
        ],

        "placements": [
            {
                "object_pk":
                    item.object_pk,

                "target_segment_ordinal":
                    item.target_segment_ordinal,

                "target_object_ordinal":
                    item.target_object_ordinal,
            }
            for item
            in plan.placements
        ],
    }


def repack_plan_sha256(
    plan: RepackPlan,
) -> str:
    return hashlib.sha256(
        canonical_json_bytes(
            repack_plan_payload(
                plan
            )
        )
    ).hexdigest()


__all__ = [
    "AGGREGATION_VERSION",
    "CacheTelemetryAggregate",
    "DATA_MODEL_PROTOCOL_SHA256",
    "ExactRatio",
    "LocalityMetricId",
    "LocalityMetricValue",
    "MAFSegmentLocalityDataModelError",
    "MAFSegmentLocalityMetricError",
    "MAFSegmentLocalityPlanError",
    "MAFSegmentLocalityPrefetchError",
    "MAFSegmentLocalitySequenceError",
    "MAFSegmentLocalityValidationError",
    "ObjectTelemetryAggregate",
    "PARENT_PHASE6D_PROTOCOL_SHA256",
    "PHASE6C_ENGINE_SHA256",
    "PlannerConfigEntry",
    "PrefetchTelemetryAggregate",
    "REPACK_PLAN_SCHEMA",
    "RESIDENCY_STATES",
    "RepackPlacement",
    "RepackPlan",
    "ResidencyTransitionAggregate",
    "SNAPSHOT_SCHEMA",
    "TelemetryAccumulator",
    "TelemetryEvent",
    "TelemetryEventKind",
    "TelemetrySnapshot",
    "TransitionTelemetryAggregate",
    "canonical_json_bytes",
    "co_segment_fraction",
    "cross_segment_fraction",
    "repack_plan_payload",
    "repack_plan_sha256",
    "snapshot_payload",
    "snapshot_sha256",
    "validate_complete_source_object_set",
    "weighted_transition_rank_distance",
]
