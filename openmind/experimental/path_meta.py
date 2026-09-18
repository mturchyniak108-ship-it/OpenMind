"""Shared experimental path metadata.

Used by both Knowledge Waveform and Fractal Memory.
This is NOT canonical truth — it is a derived view of a TruthPath.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from openmind.truth_graph import TruthGraph, TruthPath


@dataclass(frozen=True)
class ExperimentalPathMeta:
    """Deterministic metadata extracted from a canonical TruthPath.

    All fields are derived. Nothing here is authoritative.
    """
    start_node: str
    end_node: str
    path_id: str
    nodes: Tuple[str, ...]
    relationship_tags: Tuple[str, ...]
    directions: Tuple[str, ...]
    weights: Tuple[float, ...]
    truth_confidences: Tuple[float, ...]
    path_cost: float
    predictive_weight: float = 0.0

    def __post_init__(self) -> None:
        if len(self.nodes) < 2:
            raise ValueError("path must contain at least start and end")
        if not (0.0 <= self.predictive_weight <= 1.0):
            raise ValueError("predictive_weight must be in [0.0, 1.0]")


def from_truth_path(
    path: TruthPath,
    truth_graph: TruthGraph,
    predictive_weight: float = 0.0,
) -> ExperimentalPathMeta:
    """Build experimental metadata from a canonical TruthPath.

    Pure derivation — never mutates the TruthGraph or the path.
    """
    if len(path.nodes) < 2:
        raise ValueError("path must contain at least start and end")

    tags = tuple(edge.tag for edge in path.edges)
    directions = tuple("forward" for _ in path.edges)  # canonical edges are directed
    weights = tuple(float(edge.weight) for edge in path.edges)
    confidences = tuple(
        float(truth_graph.nodes[nid].truth_confidence) for nid in path.nodes
    )

    path_id = "→".join(path.nodes)

    return ExperimentalPathMeta(
        start_node=path.nodes[0],
        end_node=path.nodes[-1],
        path_id=path_id,
        nodes=path.nodes,
        relationship_tags=tags,
        directions=directions,
        weights=weights,
        truth_confidences=confidences,
        path_cost=float(path.cost),
        predictive_weight=float(predictive_weight),
    )
