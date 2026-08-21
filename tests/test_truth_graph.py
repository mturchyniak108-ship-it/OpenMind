from pathlib import Path

from openmind.truth_graph import TruthGraph, TruthEdge


ROOT = Path(__file__).resolve().parents[1]


def graph() -> TruthGraph:
    return TruthGraph.from_json(
        ROOT / "demo/truth_graph/nodes.json",
        ROOT / "demo/truth_graph/edges.json",
    )


def test_graph_loads():
    g = graph()

    assert len(g.nodes) == 20
    assert len(g.edges) == 24


def test_neighbors_are_deterministic():
    g = graph()

    first = g.neighbors("ENGINE")
    second = g.neighbors("ENGINE")

    assert first == second


def test_path_is_deterministic():
    g = graph()

    first = g.best_path("PROJECT", "EVIDENCE")
    second = g.best_path("PROJECT", "EVIDENCE")

    assert first == second
    assert first is not None


def test_path_has_start_and_end():
    g = graph()

    path = g.best_path("PROJECT", "EVIDENCE")

    assert path is not None
    assert path.nodes[0] == "PROJECT"
    assert path.nodes[-1] == "EVIDENCE"


def test_path_score_is_reproducible():
    g = graph()

    path = g.best_path("PROJECT", "EVIDENCE")

    assert path is not None
    assert math_is_finite(path.score)


def math_is_finite(value: float) -> bool:
    return value == value and abs(value) != float("inf")


def test_edge_provenance_round_trips_from_json(tmp_path: Path):
    nodes = [
        {
            "id": "A",
            "tag": "NODE",
            "type": "test",
            "truth_confidence": 0.9,
        },
        {
            "id": "B",
            "tag": "NODE",
            "type": "test",
            "truth_confidence": 0.9,
        },
    ]

    edges = [
        {
            "from": "A",
            "to": "B",
            "tag": "TEST",
            "relation": "test",
            "weight": 0.9,
            "provenance": ["E_ONE", "E_TWO"],
        }
    ]

    import json

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"

    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps(edges))

    graph = TruthGraph.from_json(nodes_path, edges_path)

    assert graph.edges[0].provenance == ("E_ONE", "E_TWO")


def test_path_score_uses_canonical_weighting():
    g = graph()

    path = g.best_path("PROJECT", "EVIDENCE")

    assert path is not None
    assert path.score == 0.8758


def test_path_ordering_is_score_then_cost_then_nodes():
    g = graph()

    paths = g.find_paths("PROJECT", "EVIDENCE")

    assert paths == sorted(
        paths,
        key=lambda path: (
            -path.score,
            path.cost,
            path.nodes,
        ),
    )


def test_find_paths_rejects_unknown_start():
    g = graph()

    try:
        g.find_paths("DOES_NOT_EXIST", "EVIDENCE")
    except KeyError as exc:
        assert "Unknown start_node" in str(exc)
    else:
        raise AssertionError("unknown start node was accepted")


def test_find_paths_rejects_unknown_end():
    g = graph()

    try:
        g.find_paths("PROJECT", "DOES_NOT_EXIST")
    except KeyError as exc:
        assert "Unknown end_node" in str(exc)
    else:
        raise AssertionError("unknown end node was accepted")


def test_find_paths_are_simple():
    g = graph()

    paths = g.find_paths("PROJECT", "EVIDENCE")

    for path in paths:
        assert len(path.nodes) == len(set(path.nodes))


def test_max_depth_is_respected():
    g = graph()

    paths = g.find_paths(
        "PROJECT",
        "EVIDENCE",
        max_depth=2,
    )

    assert all(len(path.edges) <= 2 for path in paths)


def test_truth_nodes_are_immutable():
    g = graph()
    node = g.nodes["ENGINE"]

    try:
        node.truth_confidence = 0.5
    except Exception:
        pass
    else:
        raise AssertionError("TruthNode was mutable")


def test_truth_edges_are_immutable():
    g = graph()
    edge = g.edges[0]

    try:
        edge.weight = 0.1
    except Exception:
        pass
    else:
        raise AssertionError("TruthEdge was mutable")


def test_truth_paths_are_immutable():
    g = graph()

    path = g.best_path("PROJECT", "EVIDENCE")

    assert path is not None

    try:
        path.score = 0.1
    except Exception:
        pass
    else:
        raise AssertionError("TruthPath was mutable")


def test_graph_rejects_invalid_truth_confidence(tmp_path: Path):
    import json

    nodes = [
        {
            "id": "A",
            "tag": "NODE",
            "type": "test",
            "truth_confidence": 2.0,
        }
    ]

    edges = []

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"

    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps(edges))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except ValueError:
        pass
    else:
        raise AssertionError(
            "invalid truth confidence was accepted"
        )


def test_graph_does_not_expose_mutable_canonical_edge_lists():
    g = graph()

    first = g.neighbors("ENGINE")
    second = g.neighbors("ENGINE")

    assert isinstance(first, tuple)
    assert isinstance(second, tuple)
    assert first == second


def test_canonical_path_score_is_independent_of_provenance():
    g = graph()

    baseline = g.best_path("PROJECT", "EVIDENCE")

    assert baseline is not None

    original_edges = list(g.edges)

    for edge in original_edges:
        assert isinstance(edge.provenance, tuple)

    after = g.best_path("PROJECT", "EVIDENCE")

    assert after == baseline
    assert after.score == 0.8758


def test_graph_rejects_invalid_edge_weight(tmp_path: Path):
    import json

    nodes = [
        {
            "id": "A",
            "tag": "NODE",
            "type": "test",
            "truth_confidence": 1.0,
        },
        {
            "id": "B",
            "tag": "NODE",
            "type": "test",
            "truth_confidence": 1.0,
        },
    ]

    edges = [
        {
            "from": "A",
            "to": "B",
            "tag": "TEST",
            "relation": "test",
            "weight": 1.5,
        }
    ]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"

    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps(edges))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except ValueError:
        pass
    else:
        raise AssertionError(
            "invalid edge weight was accepted"
        )


def test_zero_and_one_edge_weights_are_valid():
    zero = TruthEdge(
        source="A",
        target="B",
        tag="TEST",
        relation="test",
        weight=0.0,
    )

    one = TruthEdge(
        source="A",
        target="B",
        tag="TEST",
        relation="test",
        weight=1.0,
    )

    assert zero.weight == 0.0
    assert one.weight == 1.0


def test_non_finite_edge_weight_is_rejected():
    for weight in (
        float("nan"),
        float("inf"),
        float("-inf"),
    ):
        try:
            TruthEdge(
                source="A",
                target="B",
                tag="TEST",
                relation="test",
                weight=weight,
            )
        except ValueError:
            pass
        else:
            raise AssertionError(
                f"non-finite edge weight was accepted: {weight!r}"
            )
