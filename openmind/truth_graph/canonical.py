"""Canonical Truth State boundary."""

from __future__ import annotations

from dataclasses import dataclass

from openmind.evidence.bindings import EdgeEvidenceBindings
from openmind.evidence.registry import EvidenceRegistry

from .graph import TruthGraph


@dataclass(frozen=True)
class CanonicalTruthState:
    """Immutable composition of canonical graph and provenance state."""

    graph: TruthGraph
    evidence: EvidenceRegistry
    bindings: EdgeEvidenceBindings

    def validate(self) -> tuple[()]:
        """Validate the complete canonical state."""

        self.bindings.validate(self.evidence)
        self.bindings.validate_graph(self.graph)

        return ()
