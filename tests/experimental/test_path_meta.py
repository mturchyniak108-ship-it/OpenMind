"""Tests for shared experimental path metadata."""

from openmind.experimental.path_meta import ExperimentalPathMeta, from_truth_path
from openmind.truth_graph import TruthEdge, TruthGraph, TruthNode, TruthPath


def _simple_graph() -> TruthGraph:
    nodes = {
        "A": TruthNode(id="A", tag="a", type="concept", truth_confidence=0.9),
        "B": TruthNode(id="B", tag="b", type="concept", truth_confidence=0.8),
        "C": TruthNode(id="C", tag="c", type="concept", truth_confidence=1.0),
    }
    edges = [
        TruthEdge(source="A", target="B", tag="rel", relation="supports", weight=0.7),
        TruthEdge(source="B", target="C", tag="rel", relation="supports", weight=0.6),
    ]
    return TruthGraph(nodes, edges)


def test_from_truth_path_is_pure_and_deterministic():
    graph = _simple_graph()
    path = graph.best_path("A", "C")
    assert path is not None

    meta1 = from_truth_path(path, graph, predictive_weight=0.3)
    meta2 = from_truth_path(path, graph, predictive_weight=0.3)

    assert meta1 == meta2
    assert meta1.start_node == "A"
    assert meta1.end_node == "C"
    assert meta1.nodes == ("A", "B", "C")
    assert meta1.weights == (0.7, 0.6)
    assert meta1.truth_confidences == (0.9, 0.8, 1.0)
    assert meta1.predictive_weight == 0.3
    assert meta1.path_cost == path.cost


def test_experimental_path_meta_rejects_short_path():
    try:
        ExperimentalPathMeta(
            start_node="A",
            end_node="A",
            path_id="A",
            nodes=("A",),
            relationship_tags=(),
            directions=(),
            weights=(),
            truth_confidences=(1.0,),
            path_cost=0.0,
        )
        assert False, "should have raised"
    except ValueError as exc:
        assert "at least start and end" in str(exc)
