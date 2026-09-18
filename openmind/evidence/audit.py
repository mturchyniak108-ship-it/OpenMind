"""Canonical audited truth trace."""

from __future__ import annotations

from dataclasses import dataclass

from .coverage import (
    ProvenanceCoverage,
    calculate_provenance_coverage,
)
from .edge_resolution import (
    ResolvedEdgeEvidence,
    resolve_edge_evidence,
)
from .registry import EvidenceRegistry
from .trace import TruthTrace


@dataclass(frozen=True)
class AuditedTruthTrace:
    """Immutable truth trace with resolved provenance metadata."""

    trace: TruthTrace
    evidence: tuple[ResolvedEdgeEvidence, ...]
    coverage: ProvenanceCoverage

    @property
    def start(self) -> str:
        return self.trace.start

    @property
    def end(self) -> str:
        return self.trace.end

    @property
    def steps(self):
        return self.trace.steps

    @property
    def score(self) -> float:
        """Canonical score; never modified by provenance."""
        return self.trace.score


def audit_truth_trace(
    trace: TruthTrace,
    registry: EvidenceRegistry,
) -> AuditedTruthTrace:
    """Resolve provenance for every edge in a canonical truth trace."""

    resolved = tuple(
        resolve_edge_evidence(
            step.source,
            step.target,
            step.evidence_id,
            registry,
        )
        for step in trace.steps
    )

    coverage = calculate_provenance_coverage(resolved)

    return AuditedTruthTrace(
        trace=trace,
        evidence=resolved,
        coverage=coverage,
    )
