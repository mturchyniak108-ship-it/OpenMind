"""Tests for experimental Fractal Memory encoder."""

import math

from openmind.experimental.fractal import encode
from openmind.experimental.path_meta import from_truth_path
from openmind.truth_graph import TruthEdge, TruthGraph, TruthNode


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


def test_fractal_is_deterministic():
    """Same path meta must produce identical fractal encoding."""
    graph = _simple_graph()
    path = graph.best_path("A", "C")
    assert path is not None

    meta = from_truth_path(path, graph, predictive_weight=0.3)
    f1 = encode(meta)
    f2 = encode(meta)

    assert f1 == f2
    assert f1.path_id == meta.path_id


def test_fractal_double_helix_structure():
    """Strands A and B must be opposite phases, same z progression."""
    graph = _simple_graph()
    path = graph.best_path("A", "C")
    assert path is not None

    meta = from_truth_path(path, graph)
    fractal = encode(meta)

    assert len(fractal.strand_a) == 2
    assert len(fractal.strand_b) == 2

    for a, b in zip(fractal.strand_a, fractal.strand_b):
        assert a.z == b.z
        assert abs(a.x + b.x) < 0.0001
        assert abs(a.y + b.y) < 0.0001
        assert a.convergence_weight == b.convergence_weight


def test_fractal_convergence_sorted_by_weight():
    """Convergence points ordered by descending relational weight."""
    graph = _simple_graph()
    path = graph.best_path("A", "C")
    assert path is not None

    meta = from_truth_path(path, graph)
    fractal = encode(meta)

    weights = [p.convergence_weight for p in fractal.convergence_points]
    assert weights == sorted(weights, reverse=True)


def test_fractal_strand_radius_matches_edge_weight():
    """Helix radius at each step must equal the corresponding edge weight."""
    graph = _simple_graph()
    path = graph.best_path("A", "C")
    assert path is not None

    meta = from_truth_path(path, graph)
    fractal = encode(meta)

    for i, a in enumerate(fractal.strand_a):
        expected_radius = meta.weights[i]
        actual_radius = math.sqrt(a.x ** 2 + a.y ** 2)
        assert abs(actual_radius - expected_radius) < 0.0001
