"""Deterministic canonical Truth Graph implementation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import math


@dataclass(frozen=True)
class TruthNode:
    id: str
    tag: str
    type: str
    truth_confidence: float

    def __post_init__(self) -> None:
        confidence = float(self.truth_confidence)

        if not math.isfinite(confidence):
            raise ValueError(
                "truth_confidence must be finite"
            )

        if not 0.0 <= confidence <= 1.0:
            raise ValueError(
                "truth_confidence must be between 0.0 and 1.0"
            )


@dataclass(frozen=True)
class TruthEdge:
    source: str
    target: str
    tag: str
    relation: str
    weight: float
    provenance: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        weight = float(self.weight)

        if not math.isfinite(weight):
            raise ValueError(
                "edge weight must be finite"
            )

        if not 0.0 <= weight <= 1.0:
            raise ValueError(
                "edge weight must be between 0.0 and 1.0"
            )


@dataclass(frozen=True)
class TruthPath:
    nodes: tuple[str, ...]
    edges: tuple[TruthEdge, ...]
    score: float
    cost: float


class TruthGraph:
    """Canonical knowledge graph.

    This class contains canonical structured knowledge only.
    Experimental vector, ML, fuzzy, waveform, and fractal layers
    must consume this graph rather than replace it.
    """

    def __init__(
        self,
        nodes: dict[str, TruthNode],
        edges: list[TruthEdge],
    ) -> None:
        self.nodes = dict(nodes)
        self.edges = list(edges)

        self._outgoing: dict[str, list[TruthEdge]] = {
            node_id: [] for node_id in self.nodes
        }

        for edge in self.edges:
            if edge.source in self.nodes and edge.target in self.nodes:
                self._outgoing[edge.source].append(edge)

        for node_id in self._outgoing:
            self._outgoing[node_id].sort(
                key=lambda edge: (
                    -edge.weight,
                    edge.target,
                    edge.relation,
                )
            )

    @classmethod
    def from_json(
        cls,
        nodes_path: str | Path,
        edges_path: str | Path,
    ) -> "TruthGraph":
        nodes_data = json.loads(Path(nodes_path).read_text())
        edges_data = json.loads(Path(edges_path).read_text())

        nodes = {
            item["id"]: TruthNode(
                id=item["id"],
                tag=item["tag"],
                type=item["type"],
                truth_confidence=float(item["truth_confidence"]),
            )
            for item in nodes_data
        }

        edges = [
            TruthEdge(
                source=item["from"],
                target=item["to"],
                tag=item["tag"],
                relation=item["relation"],
                weight=float(item["weight"]),
                provenance=tuple(
                    str(value)
                    for value in item.get("provenance", [])
                ),
            )
            for item in edges_data
        ]

        return cls(nodes, edges)

    def neighbors(self, node_id: str) -> tuple[TruthEdge, ...]:
        return tuple(self._outgoing.get(node_id, ()))

    def path_score(self, edges: list[TruthEdge]) -> float:
        """Deterministic path score.

        Strong relationships and high-confidence nodes increase score.
        Longer paths incur cost.
        """

        if not edges:
            return 0.0

        relationship_score = sum(edge.weight for edge in edges) / len(edges)

        node_confidence = sum(
            self.nodes[node_id].truth_confidence
            for node_id in {
                edge.source for edge in edges
            } | {
                edge.target for edge in edges
            }
        )

        node_count = len(
            {
                edge.source for edge in edges
            } | {
                edge.target for edge in edges
            }
        )

        confidence_score = node_confidence / max(node_count, 1)

        path_cost = len(edges)

        score = (
            0.55 * relationship_score
            + 0.45 * confidence_score
            - 0.02 * path_cost
        )

        return round(score, 12)

    def find_paths(
        self,
        start_node: str,
        end_node: str,
        max_depth: int = 8,
    ) -> list[TruthPath]:
        """Enumerate deterministic simple paths."""

        if start_node not in self.nodes:
            raise KeyError(f"Unknown start_node: {start_node}")

        if end_node not in self.nodes:
            raise KeyError(f"Unknown end_node: {end_node}")

        results: list[TruthPath] = []

        def visit(
            current: str,
            node_path: list[str],
            edge_path: list[TruthEdge],
        ) -> None:
            if len(edge_path) > max_depth:
                return

            if current == end_node:
                score = self.path_score(edge_path)
                cost = float(len(edge_path))

                results.append(
                    TruthPath(
                        nodes=tuple(node_path),
                        edges=tuple(edge_path),
                        score=score,
                        cost=cost,
                    )
                )
                return

            for edge in self._outgoing.get(current, []):
                if edge.target in node_path:
                    continue

                visit(
                    edge.target,
                    node_path + [edge.target],
                    edge_path + [edge],
                )

        visit(start_node, [start_node], [])

        results.sort(
            key=lambda path: (
                -path.score,
                path.cost,
                path.nodes,
            )
        )

        return results

    def best_path(
        self,
        start_node: str,
        end_node: str,
        max_depth: int = 8,
    ) -> TruthPath | None:
        paths = self.find_paths(
            start_node,
            end_node,
            max_depth=max_depth,
        )

        return paths[0] if paths else None
