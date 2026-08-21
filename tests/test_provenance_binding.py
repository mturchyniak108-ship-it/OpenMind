from pathlib import Path

from openmind.truth_graph import TruthGraph


ROOT = Path(__file__).resolve().parents[1]


def graph() -> TruthGraph:
    return TruthGraph.from_json(
        ROOT / "demo/truth_graph/nodes.json",
        ROOT / "demo/truth_graph/edges.json",
    )


def test_truth_edge_supports_provenance():
    g = graph()

    edge = next(
        edge
        for edge in g.edges
        if edge.source == "TEST"
        and edge.target == "EVIDENCE"
    )

    assert edge.weight == 0.96
    assert edge.provenance == ()


def test_provenance_does_not_change_canonical_score():
    g = graph()

    path = g.best_path("PROJECT", "EVIDENCE")

    assert path is not None
    assert path.score == 0.8758


def test_provenance_is_immutable():
    g = graph()

    edge = next(iter(g.edges))

    assert edge.provenance == ()

    try:
        edge.provenance = ("E1",)
    except Exception:
        pass
    else:
        raise AssertionError("TruthEdge provenance must be immutable")
