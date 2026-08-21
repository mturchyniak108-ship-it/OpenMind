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
            if edge.source not in self.nodes:
                raise ValueError(
                    f"unknown edge source: {edge.source}"
                )

            if edge.target not in self.nodes:
                raise ValueError(
                    f"unknown edge target: {edge.target}"
                )

            self._outgoing[edge.source].append(edge)

        for node_id in self._outgoing:
            self._outgoing[node_id].sort(
                key=lambda edge: (
                    -edge.weight,
                    edge.target,
                    edge.relation,
                )
            )

    def to_dict(self) -> dict[str, list[dict[str, object]]]:
        """Return the canonical Truth Graph representation."""

        nodes = [
            {
                "id": node.id,
                "tag": node.tag,
                "type": node.type,
                "truth_confidence": node.truth_confidence,
            }
            for node in sorted(
                self.nodes.values(),
                key=lambda node: node.id,
            )
        ]

        edges = [
            {
                "from": edge.source,
                "to": edge.target,
                "tag": edge.tag,
                "relation": edge.relation,
                "weight": edge.weight,
                "provenance": list(edge.provenance),
            }
            for edge in sorted(
                self.edges,
                key=lambda edge: (
                    edge.source,
                    edge.target,
                    edge.tag,
                    edge.relation,
                ),
            )
        ]

        return {
            "nodes": nodes,
            "edges": edges,
        }

    def to_json(self) -> str:
        """Serialize the Truth Graph using canonical JSON formatting."""

        return json.dumps(
            self.to_dict(),
            indent=2,
            sort_keys=True,
        ) + "\n"

    def save(self, path: str | Path) -> None:
        """Persist the Truth Graph using canonical JSON."""

        Path(path).write_text(
            self.to_json(),
            encoding="utf-8",
        )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, object],
    ) -> "TruthGraph":
        """Construct a Truth Graph from canonical dictionaries."""

        if not isinstance(data, dict):
            raise ValueError(
                "truth graph data must contain an object"
            )

        nodes_data = data.get("nodes")
        edges_data = data.get("edges")

        if not isinstance(nodes_data, list):
            raise ValueError("truth graph nodes payload must be a list")

        if not isinstance(edges_data, list):
            raise ValueError("truth graph edges payload must be a list")

        nodes: dict[str, TruthNode] = {}

        for item in nodes_data:
            node_id = str(item["id"])

            if not node_id.strip():
                raise ValueError(
                    "truth node id must not be empty or whitespace"
                )

            if node_id in nodes:
                raise ValueError(
                    f"duplicate truth node id: {node_id}"
                )

            nodes[node_id] = TruthNode(
                id=node_id,
                tag=item["tag"],
                type=item["type"],
                truth_confidence=float(item["truth_confidence"]),
            )

        edges: list[TruthEdge] = []
        edge_keys: set[tuple[str, str, str, str]] = set()
        endpoint_keys: set[tuple[str, str]] = set()

        for item in edges_data:
            source = str(item["from"])
            target = str(item["to"])
            tag = str(item["tag"])
            relation = str(item["relation"])

            if not tag.strip():
                raise ValueError(
                    "truth edge tag must not be empty or whitespace"
                )

            if not relation.strip():
                raise ValueError(
                    "truth edge relation must not be empty or whitespace"
                )

            if source not in nodes:
                raise ValueError(
                    f"unknown edge source: {source}"
                )

            if target not in nodes:
                raise ValueError(
                    f"unknown edge target: {target}"
                )

            edge_key = (source, target, tag, relation)
            endpoint_key = (source, target)

            if endpoint_key in endpoint_keys:
                raise ValueError(
                    f"conflicting duplicate TruthEdge: "
                    f"{source} -> {target}"
                )

            if edge_key in edge_keys:
                raise ValueError(
                    f"duplicate TruthEdge: {source} -> {target} "
                    f"({tag}, {relation})"
                )

            endpoint_keys.add(endpoint_key)
            edge_keys.add(edge_key)

            edges.append(
                TruthEdge(
                    source=source,
                    target=target,
                    tag=tag,
                    relation=relation,
                    weight=float(item["weight"]),
                    provenance=tuple(
                        str(value)
                        for value in item.get("provenance", [])
                    ),
                )
            )

        return cls(nodes, edges)

    @classmethod
    def from_json(
        cls,
        nodes_path: str | Path,
        edges_path: str | Path,
    ) -> "TruthGraph":
        """Construct a Truth Graph from the legacy split JSON files."""

        nodes_data = json.loads(
            Path(nodes_path).read_text(encoding="utf-8")
        )
        edges_data = json.loads(
            Path(edges_path).read_text(encoding="utf-8")
        )

        return cls.from_dict(
            {
                "nodes": nodes_data,
                "edges": edges_data,
            }
        )

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
