"""Experimental predictive path scoring.

Canonical TruthGraph remains authoritative.
This scorer evaluates canonical paths using experimental
fuzzy/vector-derived weights.
"""

from __future__ import annotations

from dataclasses import dataclass

from openmind.truth_graph import TruthGraph, TruthPath

from .graph import FuzzyVectorGraph


@dataclass(frozen=True)
class PredictivePath:
    path: TruthPath
    relationship_score: float
    fuzzy_score: float
    predictive_score: float


class PredictivePathScorer:
    """Experimental scorer layered on top of canonical paths."""

    def __init__(self, truth_graph: TruthGraph) -> None:
        self.truth_graph = truth_graph
        self.fuzzy_graph = FuzzyVectorGraph(truth_graph)

    def score(self, path: TruthPath) -> PredictivePath:
        if not path.edges:
            return PredictivePath(
                path=path,
                relationship_score=0.0,
                fuzzy_score=0.0,
                predictive_score=0.0,
            )

        relationship_score = (
            sum(edge.weight for edge in path.edges)
            / len(path.edges)
        )

        fuzzy_values = []

        for edge in path.edges:
            relationship = self.fuzzy_graph.relationship(
                edge.source,
                edge.target,
            )
            fuzzy_values.append(relationship.membership)

        fuzzy_score = sum(fuzzy_values) / len(fuzzy_values)

        predictive_score = (
            0.65 * relationship_score
            + 0.35 * fuzzy_score
            - 0.02 * path.cost
        )

        return PredictivePath(
            path=path,
            relationship_score=round(relationship_score, 12),
            fuzzy_score=round(fuzzy_score, 12),
            predictive_score=round(predictive_score, 12),
        )

    def best_path(
        self,
        start_node: str,
        end_node: str,
        max_depth: int = 8,
    ) -> PredictivePath | None:
        paths = self.truth_graph.find_paths(
            start_node,
            end_node,
            max_depth=max_depth,
        )

        if not paths:
            return None

        scored = [self.score(path) for path in paths]

        scored.sort(
            key=lambda item: (
                -item.predictive_score,
                item.path.cost,
                item.path.nodes,
            )
        )

        return scored[0]
