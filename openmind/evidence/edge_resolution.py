"""Canonical resolution of edge evidence against the evidence registry."""

from __future__ import annotations

from dataclasses import dataclass

from .registry import EvidenceRegistry


@dataclass(frozen=True)
class ResolvedEdgeEvidence:
    """Resolved evidence state for one graph edge."""

    source: str
    target: str
    evidence_id: str | None
    status: str


def resolve_edge_evidence(
    source: str,
    target: str,
    evidence_id: str | None,
    registry: EvidenceRegistry,
) -> ResolvedEdgeEvidence:
    """Resolve an edge's evidence binding without changing graph semantics."""

    if evidence_id is None:
        return ResolvedEdgeEvidence(
            source=source,
            target=target,
            evidence_id=None,
            status="UNBOUND",
        )

    evidence = registry.get(evidence_id)

    if evidence is None:
        return ResolvedEdgeEvidence(
            source=source,
            target=target,
            evidence_id=evidence_id,
            status="MISSING",
        )

    return ResolvedEdgeEvidence(
        source=source,
        target=target,
        evidence_id=evidence_id,
        status="REGISTERED",
    )
