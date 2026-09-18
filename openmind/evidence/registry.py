"""Canonical in-memory and serialized evidence registry."""

from __future__ import annotations

import json
from pathlib import Path

from .models import EvidenceRecord


class EvidenceRegistry:
    """Deterministic registry of immutable evidence records."""

    def __init__(
        self,
        records: list[EvidenceRecord] | None = None,
    ) -> None:
        self._records: dict[str, EvidenceRecord] = {}

        for record in records or []:
            self.add(record)

    def add(self, record: EvidenceRecord) -> None:
        """Register evidence without allowing conflicting duplicates."""

        existing = self._records.get(record.id)

        if existing is not None and existing != record:
            raise ValueError(
                f"conflicting evidence id: {record.id}"
            )

        self._records[record.id] = record

    def get(self, evidence_id: str) -> EvidenceRecord | None:
        return self._records.get(evidence_id)

    def all(self) -> tuple[EvidenceRecord, ...]:
        return tuple(
            self._records[key]
            for key in sorted(self._records)
        )

    def __len__(self) -> int:
        return len(self._records)

    def to_dict(self) -> list[dict[str, object]]:
        """Return canonical evidence records in deterministic order."""

        return [
            {
                "id": record.id,
                "source": record.source,
                "claim": record.claim,
                "confidence": record.confidence,
            }
            for record in self.all()
        ]

    def to_json(self) -> str:
        """Serialize the registry using canonical JSON formatting."""

        return json.dumps(
            self.to_dict(),
            indent=2,
            sort_keys=True,
        ) + "\n"

    @classmethod
    def from_dict(
        cls,
        data: list[dict[str, object]],
    ) -> "EvidenceRegistry":
        """Construct a registry from canonical record dictionaries."""

        if not isinstance(data, list):
            raise ValueError(
                "evidence registry data must contain a list"
            )

        records = [
            EvidenceRecord(
                id=str(item["id"]),
                source=str(item["source"]),
                claim=str(item["claim"]),
                confidence=float(item["confidence"]),
            )
            for item in data
        ]

        return cls(records)

    @classmethod
    def from_json(cls, text: str) -> "EvidenceRegistry":
        """Construct a registry from canonical JSON."""

        data = json.loads(text)

        if not isinstance(data, list):
            raise ValueError("evidence registry JSON must contain a list")

        return cls.from_dict(data)

    def save(self, path: str | Path) -> None:
        """Persist the registry using canonical JSON."""

        Path(path).write_text(
            self.to_json(),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, path: str | Path) -> "EvidenceRegistry":
        """Load a registry from canonical JSON on disk."""

        return cls.from_json(
            Path(path).read_text(encoding="utf-8")
        )
