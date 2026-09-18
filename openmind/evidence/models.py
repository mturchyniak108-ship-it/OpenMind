"""Canonical evidence and provenance models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceRecord:
    """Immutable evidence supporting a canonical claim or relationship."""

    id: str
    source: str
    claim: str
    confidence: float


@dataclass(frozen=True)
class ProvenanceRecord:
    """Immutable record describing where a canonical result came from."""

    evidence_id: str
    relation: str
    source_node: str
    target_node: str
