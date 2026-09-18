"""Canonical evidence and provenance layer."""

from .models import EvidenceRecord, ProvenanceRecord
from .trace import TruthTraceResolver
from .artifact import evidence_from_artifact

__all__ = [
    "EvidenceRecord",
    "ProvenanceRecord",
    "TruthTraceResolver",
    "evidence_from_artifact",
]

from .edge_binding import bind_evidence_to_edge

__all__.append("bind_evidence_to_edge")

from .binding import ArtifactEvidenceBinding, bind_artifact_to_evidence

__all__.extend([
    "ArtifactEvidenceBinding",
    "bind_artifact_to_evidence",
])

from .registry import EvidenceRegistry

__all__.append("EvidenceRegistry")

from .edge_resolution import ResolvedEdgeEvidence, resolve_edge_evidence

__all__.extend([
    "ResolvedEdgeEvidence",
    "resolve_edge_evidence",
])

from .coverage import ProvenanceCoverage, calculate_provenance_coverage

__all__.extend([
    "ProvenanceCoverage",
    "calculate_provenance_coverage",
])

from .audit import AuditedTruthTrace

__all__.append("AuditedTruthTrace")

from .trace import TraceStep, TruthTrace

__all__.extend([
    "TraceStep",
    "TruthTrace",
])

from .audit import audit_truth_trace

__all__.append("audit_truth_trace")

from .bindings import EdgeEvidenceBinding, EdgeEvidenceBindings

__all__.extend([
    "EdgeEvidenceBinding",
    "EdgeEvidenceBindings",
])
