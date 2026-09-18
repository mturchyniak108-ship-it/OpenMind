"""Experimental fuzzy/vector representation of the canonical Truth Graph."""

from __future__ import annotations

import math

from openmind.truth_graph import TruthGraph

from .models import FuzzyRelationship, WeightedVector


class FuzzyVectorGraph:
    """Non-canonical experimental graph layer.

    The canonical TruthGraph remains authoritative.
    This layer only derives vectors and fuzzy relationship weights.
    It never mutates the TruthGraph.
    """

    def __init__(self, truth_graph: TruthGraph) -> None:
        self.truth_graph = truth_graph

    @staticmethod
    def _clamp(value: float) -> float:
        """Force value into the closed interval [0.0, 1.0]."""
        return max(0.0, min(1.0, float(value)))

    def node_vector(self, node_id: str) -> WeightedVector:
        """Derive a 3-dimensional experimental vector for a node.

        Components
        ----------
        [0] truth_confidence of the node
        [1] mean weight of outgoing edges
        [2] out-degree (raw count)
        """
        if node_id not in self.truth_graph.nodes:
            raise KeyError(f"Unknown node: {node_id}")

        node = self.truth_graph.nodes[node_id]
        outgoing = self.truth_graph.neighbors(node_id)

        relation_mean = (
            sum(edge.weight for edge in outgoing) / len(outgoing)
            if outgoing
            else 0.0
        )

        values = (
            float(node.truth_confidence),
            float(relation_mean),
            float(len(outgoing)),
        )

        magnitude = math.sqrt(sum(v * v for v in values))

        # Predictive weight is a simple linear blend biased toward
        # intrinsic truth confidence.  This is an experimental signal only.
        predictive_weight = self._clamp(
            0.6 * node.truth_confidence + 0.4 * relation_mean
        )

        return WeightedVector(
            node_id=node_id,
            values=values,
            magnitude=magnitude,
            predictive_weight=predictive_weight,
        )

    def relationship(self, source: str, target: str) -> FuzzyRelationship:
        """Derive a fuzzy membership for an existing canonical edge.

        membership = clamp(edge.weight × source.conf × target.conf)

        This is a multiplicative fuzzy-AND.  The result is purely
        derived and never written back into the TruthGraph.
        """
        if source not in self.truth_graph.nodes:
            raise KeyError(f"Unknown source node: {source}")

        # Keep original message style so existing tests continue to pass.
        # Unknown target or missing edge both surface as "No relationship".
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
                    predictive_weight=float(edge.weight),
                )

        raise KeyError(f"No relationship: {source} -> {target}")
