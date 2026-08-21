"""Canonical persistent edge-evidence bindings."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .registry import EvidenceRegistry


@dataclass(frozen=True)
class EdgeEvidenceBinding:
    """Immutable binding between a canonical graph edge and evidence."""

    source: str
    target: str
    evidence_id: str


class EdgeEvidenceBindings:
    """Deterministic collection of canonical edge-evidence bindings."""

    def __init__(
        self,
        bindings: list[EdgeEvidenceBinding] | None = None,
    ) -> None:
        self._bindings: dict[tuple[str, str], str] = {}

        for binding in bindings or []:
            key = (binding.source, binding.target)
            existing = self._bindings.get(key)

            if existing is not None and existing != binding.evidence_id:
                raise ValueError(
                    "conflicting edge evidence binding: "
                    f"{binding.source} -> {binding.target}"
                )

            self._bindings[key] = binding.evidence_id

    def get(
        self,
        source: str,
        target: str,
    ) -> str | None:
        return self._bindings.get((source, target))

    def as_dict(self) -> dict[tuple[str, str], str]:
        return dict(self._bindings)

    def validate(
        self,
        registry: EvidenceRegistry,
    ) -> tuple[()]:
        """Validate that every declared binding resolves to registered evidence."""

        missing = tuple(
            evidence_id
            for evidence_id in self._bindings.values()
            if registry.get(evidence_id) is None
        )

        if missing:
            raise ValueError(
                "missing evidence binding: "
                + ", ".join(sorted(set(missing)))
            )

        return ()

    @classmethod
    def from_dict(
        cls,
        data: list[dict[str, object]],
    ) -> "EdgeEvidenceBindings":
        if not isinstance(data, list):
            raise ValueError(
                "edge evidence bindings data must contain a list"
            )

        return cls([
            EdgeEvidenceBinding(
                source=str(item["source"]),
                target=str(item["target"]),
                evidence_id=str(item["evidence_id"]),
            )
            for item in data
        ])

    @classmethod
    def load(cls, path: str | Path) -> "EdgeEvidenceBindings":
        data = json.loads(
            Path(path).read_text(encoding="utf-8")
        )

        if not isinstance(data, list):
            raise ValueError(
                "edge evidence bindings JSON must contain a list"
            )

        return cls.from_dict(data)
