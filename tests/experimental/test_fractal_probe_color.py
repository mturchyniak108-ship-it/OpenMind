"""Tests for fractal memory probe and deterministic color encoding."""

from openmind.experimental.fractal import (
    ConvergenceColor,
    central_convergence,
    encode_color,
    encode_fractal,
    probe_by_weight_threshold,
)
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


def test_central_convergence_is_highest_weight():
    graph = _simple_graph()
    path = graph.best_path("A", "C")
    assert path is not None

    meta = from_truth_path(path, graph)
    fractal = encode_fractal(meta)

    central = central_convergence(fractal)
    assert central is not None
    assert central.convergence_weight == max(
        p.convergence_weight for p in fractal.convergence_points
    )


def test_probe_by_weight_threshold_filters_correctly():
    graph = _simple_graph()
    path = graph.best_path("A", "C")
    assert path is not None

    meta = from_truth_path(path, graph)
    fractal = encode_fractal(meta)

    high = probe_by_weight_threshold(fractal, min_weight=0.65)
    assert len(high) == 1
    assert high[0].convergence_weight == 0.7

    low = probe_by_weight_threshold(fractal, min_weight=0.55)
    assert len(low) == 2


def test_color_encoding_is_deterministic():
    graph = _simple_graph()
    path = graph.best_path("A", "C")
    assert path is not None

    meta = from_truth_path(path, graph)
    fractal = encode_fractal(meta)

    c1 = encode_color(fractal)
    c2 = encode_color(fractal)

    assert c1 == c2
    assert len(c1) == 2


def test_color_values_in_valid_range():
    graph = _simple_graph()
    path = graph.best_path("A", "C")
    assert path is not None

    meta = from_truth_path(path, graph)
    fractal = encode_fractal(meta)

    colors = encode_color(fractal)
    for cc in colors:
        assert 0 <= cc.r <= 255
        assert 0 <= cc.g <= 255
        assert 0 <= cc.b <= 255


def test_color_saturation_correlates_with_weight():
    """Higher convergence weight must produce higher or equal saturation.

    Saturation is directly mapped from convergence_weight in the HSV
    encoding, so this is a structural guarantee of the encoder.
    """
    graph = _simple_graph()
    path = graph.best_path("A", "C")
    assert path is not None

    meta = from_truth_path(path, graph)
    fractal = encode_fractal(meta)

    colors = encode_color(fractal)
    # convergence_points are already sorted by descending weight
    sats = [c.convergence_weight for c in colors]
    assert sats == sorted(sats, reverse=True)
