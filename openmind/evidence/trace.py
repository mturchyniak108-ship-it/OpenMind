"""Canonical truth trace resolution."""

from __future__ import annotations

from dataclasses import dataclass

from .models import EvidenceRecord
from openmind.truth_graph import TruthGraph


@dataclass(frozen=True)
class TraceStep:
    source: str
    target: str
    relation: str
    weight: float
    evidence_id: str | None


@dataclass(frozen=True)
class TruthTrace:
    start: str
    end: str
    steps: tuple[TraceStep, ...]
    score: float


class TruthTraceResolver:
    """Resolve an auditable canonical path with evidence references."""

    def __init__(
        self,
        graph: TruthGraph,
        evidence: list[EvidenceRecord],
    ) -> None:
        self.graph = graph
        self.evidence = {record.id: record for record in evidence}

    def resolve(
        self,
        start: str,
        end: str,
        evidence_bindings: dict[tuple[str, str], str],
    ) -> TruthTrace | None:
        path = self.graph.best_path(start, end)

        if path is None:
            return None

        steps = tuple(
            TraceStep(
                source=edge.source,
                target=edge.target,
                relation=edge.relation,
                weight=edge.weight,
                evidence_id=evidence_bindings.get(
                    (edge.source, edge.target)
                ),
            )
            for edge in path.edges
        )

        return TruthTrace(
            start=start,
            end=end,
            steps=steps,
            score=path.score,
        )
