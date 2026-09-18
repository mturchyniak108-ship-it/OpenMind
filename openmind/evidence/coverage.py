"""Canonical provenance coverage metrics."""

from __future__ import annotations

from dataclasses import dataclass

from .edge_resolution import ResolvedEdgeEvidence


@dataclass(frozen=True)
class ProvenanceCoverage:
    """Deterministic coverage statistics for a truth trace."""

    total_edges: int
    registered_edges: int
    unbound_edges: int
    missing_edges: int
    coverage: float
    unbound: tuple[tuple[str, str], ...] = ()
    missing: tuple[tuple[str, str], ...] = ()


def calculate_provenance_coverage(
    edges: list[ResolvedEdgeEvidence]
    | tuple[ResolvedEdgeEvidence, ...],
) -> ProvenanceCoverage:
    """Calculate evidence coverage without altering canonical truth."""

    total = len(edges)
    registered = sum(
        edge.status == "REGISTERED"
        for edge in edges
    )
    unbound = sum(
        edge.status == "UNBOUND"
        for edge in edges
    )
    missing = sum(
        edge.status == "MISSING"
        for edge in edges
    )

    unbound_edges = tuple(
        (edge.source, edge.target)
        for edge in edges
        if edge.status == "UNBOUND"
    )

    missing_edges = tuple(
        (edge.source, edge.target)
        for edge in edges
        if edge.status == "MISSING"
    )

    coverage = (
        registered / total
        if total
        else 0.0
    )

    return ProvenanceCoverage(
        total_edges=total,
        registered_edges=registered,
        unbound_edges=unbound,
        missing_edges=missing,
        coverage=coverage,
        unbound=unbound_edges,
        missing=missing_edges,
    )
