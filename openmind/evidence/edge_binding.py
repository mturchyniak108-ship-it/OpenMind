"""Canonical evidence-to-TruthEdge binding."""

from __future__ import annotations

from dataclasses import replace

from openmind.truth_graph import TruthEdge

from .binding import ArtifactEvidenceBinding


def bind_evidence_to_edge(
    edge: TruthEdge,
    binding: ArtifactEvidenceBinding,
) -> TruthEdge:
    """Return an immutable TruthEdge annotated with evidence provenance."""

    return replace(
        edge,
        provenance=edge.provenance + (binding.evidence_id,),
    )
