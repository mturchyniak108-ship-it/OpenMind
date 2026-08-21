"""Experimental fuzzy/vector representation of the canonical Truth Graph."""

from __future__ import annotations

import math

from openmind.truth_graph import TruthGraph

from .models import FuzzyRelationship, WeightedVector


class FuzzyVectorGraph:
    """Non-canonical experimental graph layer.

    The canonical TruthGraph remains authoritative.
    This layer only derives vectors and fuzzy relationship weights.
    """

    def __init__(self, truth_graph: TruthGraph) -> None:
        self.truth_graph = truth_graph

    @staticmethod
    def _clamp(value: float) -> float:
        return max(0.0, min(1.0, value))

    def node_vector(self, node_id: str) -> WeightedVector:
        node = self.truth_graph.nodes[node_id]
        outgoing = self.truth_graph.neighbors(node_id)

        if outgoing:
            relation_mean = sum(e.weight for e in outgoing) / len(outgoing)
        else:
            relation_mean = 0.0

        values = (
            node.truth_confidence,
            relation_mean,
            float(len(outgoing)),
        )

        magnitude = math.sqrt(sum(value * value for value in values))

        predictive_weight = self._clamp(
            0.6 * node.truth_confidence
            + 0.4 * relation_mean
        )

        return WeightedVector(
            node_id=node_id,
            values=values,
            magnitude=magnitude,
            predictive_weight=predictive_weight,
        )

    def relationship(self, source: str, target: str) -> FuzzyRelationship:
        for edge in self.truth_graph.neighbors(source):
            if edge.target == target:
                membership = self._clamp(
                    edge.weight
                    * self.truth_graph.nodes[source].truth_confidence
                    * self.truth_graph.nodes[target].truth_confidence
                )

                return FuzzyRelationship(
                    source=source,
                    target=target,
                    membership=membership,
                    predictive_weight=edge.weight,
                )

        raise KeyError(f"No relationship: {source} -> {target}")
