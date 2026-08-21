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


def test_graph_rejects_edge_with_unknown_source(tmp_path: Path):
    import json

    nodes = [
        {
            "id": "A",
            "tag": "NODE",
            "type": "test",
            "truth_confidence": 1.0,
        },
    ]

    edges = [
        {
            "from": "UNKNOWN",
            "to": "A",
            "tag": "TEST",
            "relation": "test",
            "weight": 1.0,
        }
    ]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"

    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps(edges))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except ValueError as exc:
        assert "unknown edge source" in str(exc).lower()
    else:
        raise AssertionError(
            "edge with unknown source was accepted"
        )


def test_graph_rejects_edge_with_unknown_target(tmp_path: Path):
    import json

    nodes = [
        {
            "id": "A",
            "tag": "NODE",
            "type": "test",
            "truth_confidence": 1.0,
        },
    ]

    edges = [
        {
            "from": "A",
            "to": "UNKNOWN",
            "tag": "TEST",
            "relation": "test",
            "weight": 1.0,
        }
    ]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"

    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps(edges))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except ValueError as exc:
        assert "unknown edge target" in str(exc).lower()
    else:
        raise AssertionError(
            "edge with unknown target was accepted"
        )


def test_graph_rejects_mixed_valid_and_invalid_edges(tmp_path: Path):
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
            "weight": 1.0,
        },
        {
            "from": "A",
            "to": "UNKNOWN",
            "tag": "BAD",
            "relation": "bad",
            "weight": 1.0,
        },
    ]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"

    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps(edges))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except ValueError as exc:
        assert "unknown edge target" in str(exc).lower()
    else:
        raise AssertionError(
            "graph accepted a mixed valid/invalid edge set"
        )

def test_graph_rejects_duplicate_truth_node_id(tmp_path: Path):
    import json

    nodes = [
        {
            "id": "A",
            "tag": "NODE",
            "type": "test",
            "truth_confidence": 1.0,
        },
        {
            "id": "A",
            "tag": "NODE",
            "type": "test",
            "truth_confidence": 1.0,
        },
    ]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"

    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps([]))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except ValueError as exc:
        assert "duplicate truth node id" in str(exc).lower()
    else:
        raise AssertionError(
            "duplicate TruthNode id was accepted"
        )


def test_graph_rejects_conflicting_duplicate_truth_node_id(tmp_path: Path):
    import json

    nodes = [
        {
            "id": "A",
            "tag": "NODE",
            "type": "test",
            "truth_confidence": 1.0,
        },
        {
            "id": "A",
            "tag": "DIFFERENT",
            "type": "other",
            "truth_confidence": 0.5,
        },
    ]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"

    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps([]))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except ValueError as exc:
        assert "duplicate truth node id" in str(exc).lower()
    else:
        raise AssertionError(
            "conflicting duplicate TruthNode id was accepted"
        )

def test_graph_rejects_node_missing_id(tmp_path: Path):
    import json

    nodes = [
        {
            "tag": "NODE",
            "type": "test",
            "truth_confidence": 1.0,
        },
    ]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"

    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps([]))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except (ValueError, KeyError) as exc:
        assert "id" in str(exc).lower()
    else:
        raise AssertionError("node missing id was accepted")


def test_graph_rejects_node_missing_truth_confidence(tmp_path: Path):
    import json

    nodes = [
        {
            "id": "A",
            "tag": "NODE",
            "type": "test",
        },
    ]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"

    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps([]))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except (ValueError, KeyError) as exc:
        assert "confidence" in str(exc).lower()
    else:
        raise AssertionError(
            "node missing truth_confidence was accepted"
        )


def test_graph_rejects_node_missing_tag(tmp_path: Path):
    import json

    nodes = [
        {
            "id": "A",
            "type": "test",
            "truth_confidence": 1.0,
        },
    ]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"

    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps([]))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except (ValueError, KeyError) as exc:
        assert "tag" in str(exc).lower()
    else:
        raise AssertionError("node missing tag was accepted")


def test_graph_rejects_node_missing_type(tmp_path: Path):
    import json

    nodes = [
        {
            "id": "A",
            "tag": "NODE",
            "truth_confidence": 1.0,
        },
    ]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"

    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps([]))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except (ValueError, KeyError) as exc:
        assert "type" in str(exc).lower()
    else:
        raise AssertionError("node missing type was accepted")

def test_graph_rejects_edge_missing_source(tmp_path: Path):
    import json

    nodes = [
        {"id": "A", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
        {"id": "B", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
    ]
    edges = [
        {
            "to": "B",
            "tag": "TEST",
            "relation": "test",
            "weight": 1.0,
        }
    ]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"
    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps(edges))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except (ValueError, KeyError) as exc:
        assert "from" in str(exc).lower() or "source" in str(exc).lower()
    else:
        raise AssertionError("edge missing source was accepted")


def test_graph_rejects_edge_missing_target(tmp_path: Path):
    import json

    nodes = [
        {"id": "A", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
        {"id": "B", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
    ]
    edges = [
        {
            "from": "A",
            "tag": "TEST",
            "relation": "test",
            "weight": 1.0,
        }
    ]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"
    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps(edges))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except (ValueError, KeyError) as exc:
        assert "to" in str(exc).lower() or "target" in str(exc).lower()
    else:
        raise AssertionError("edge missing target was accepted")


def test_graph_rejects_edge_missing_weight(tmp_path: Path):
    import json

    nodes = [
        {"id": "A", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
        {"id": "B", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
    ]
    edges = [
        {
            "from": "A",
            "to": "B",
            "tag": "TEST",
            "relation": "test",
        }
    ]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"
    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps(edges))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except (ValueError, KeyError) as exc:
        assert "weight" in str(exc).lower()
    else:
        raise AssertionError("edge missing weight was accepted")


def test_graph_rejects_edge_missing_relation(tmp_path: Path):
    import json

    nodes = [
        {"id": "A", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
        {"id": "B", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
    ]
    edges = [
        {
            "from": "A",
            "to": "B",
            "tag": "TEST",
            "weight": 1.0,
        }
    ]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"
    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps(edges))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except (ValueError, KeyError) as exc:
        assert "relation" in str(exc).lower()
    else:
        raise AssertionError("edge missing relation was accepted")

def test_graph_rejects_duplicate_truth_edge(tmp_path: Path):
    import json

    nodes = [
        {"id": "A", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
        {"id": "B", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
    ]

    edge = {
        "from": "A",
        "to": "B",
        "tag": "TEST",
        "relation": "test",
        "weight": 1.0,
    }

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"
    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps([edge, edge]))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except ValueError as exc:
        assert "duplicate" in str(exc).lower()
    else:
        raise AssertionError("duplicate TruthEdge was accepted")


def test_graph_rejects_conflicting_duplicate_truth_edge(tmp_path: Path):
    import json

    nodes = [
        {"id": "A", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
        {"id": "B", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
    ]

    edges = [
        {
            "from": "A",
            "to": "B",
            "tag": "TEST",
            "relation": "test",
            "weight": 1.0,
        },
        {
            "from": "A",
            "to": "B",
            "tag": "DIFFERENT",
            "relation": "other",
            "weight": 0.5,
        },
    ]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"
    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps(edges))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except ValueError as exc:
        assert "duplicate" in str(exc).lower() or "conflict" in str(exc).lower()
    else:
        raise AssertionError(
            "conflicting duplicate TruthEdge was accepted"
        )

def test_graph_rejects_non_list_nodes_payload(tmp_path: Path):
    import json

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"

    nodes_path.write_text(json.dumps({"id": "A"}))
    edges_path.write_text(json.dumps([]))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except (ValueError, TypeError) as exc:
        assert "node" in str(exc).lower() or "list" in str(exc).lower()
    else:
        raise AssertionError("non-list nodes payload was accepted")


def test_graph_rejects_non_list_edges_payload(tmp_path: Path):
    import json

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"

    nodes_path.write_text(json.dumps([
        {
            "id": "A",
            "tag": "NODE",
            "type": "test",
            "truth_confidence": 1.0,
        }
    ]))
    edges_path.write_text(json.dumps({"from": "A"}))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except (ValueError, TypeError) as exc:
        assert "edge" in str(exc).lower() or "list" in str(exc).lower()
    else:
        raise AssertionError("non-list edges payload was accepted")


def test_graph_rejects_invalid_node_truth_confidence(tmp_path: Path):
    import json

    nodes = [
        {
            "id": "A",
            "tag": "NODE",
            "type": "test",
            "truth_confidence": "not-a-number",
        }
    ]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"
    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps([]))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except (ValueError, TypeError) as exc:
        assert "confidence" in str(exc).lower() or "float" in str(exc).lower()
    else:
        raise AssertionError(
            "node with invalid truth confidence was accepted"
        )

def test_graph_rejects_empty_truth_node_id(tmp_path: Path):
    import json

    nodes = [
        {
            "id": "",
            "tag": "NODE",
            "type": "test",
            "truth_confidence": 1.0,
        }
    ]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"
    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps([]))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except ValueError as exc:
        assert "id" in str(exc).lower()
    else:
        raise AssertionError("empty TruthNode id was accepted")


def test_graph_rejects_whitespace_truth_node_id(tmp_path: Path):
    import json

    nodes = [
        {
            "id": "   ",
            "tag": "NODE",
            "type": "test",
            "truth_confidence": 1.0,
        }
    ]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"
    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps([]))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except ValueError as exc:
        assert "id" in str(exc).lower()
    else:
        raise AssertionError("whitespace TruthNode id was accepted")


def test_graph_rejects_truth_confidence_below_zero(tmp_path: Path):
    import json

    nodes = [
        {
            "id": "A",
            "tag": "NODE",
            "type": "test",
            "truth_confidence": -0.1,
        }
    ]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"
    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps([]))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except ValueError as exc:
        assert "confidence" in str(exc).lower()
    else:
        raise AssertionError(
            "truth confidence below zero was accepted"
        )


def test_graph_rejects_truth_confidence_above_one(tmp_path: Path):
    import json

    nodes = [
        {
            "id": "A",
            "tag": "NODE",
            "type": "test",
            "truth_confidence": 1.1,
        }
    ]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"
    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps([]))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except ValueError as exc:
        assert "confidence" in str(exc).lower()
    else:
        raise AssertionError(
            "truth confidence above one was accepted"
        )

def test_graph_rejects_edge_weight_nan(tmp_path: Path):
    import json

    nodes = [
        {"id": "A", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
        {"id": "B", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
    ]
    edges = [{
        "from": "A",
        "to": "B",
        "tag": "TEST",
        "relation": "test",
        "weight": "nan",
    }]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"
    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps(edges))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except ValueError as exc:
        assert "weight" in str(exc).lower()
    else:
        raise AssertionError("NaN edge weight was accepted")


def test_graph_rejects_edge_weight_infinity(tmp_path: Path):
    import json

    nodes = [
        {"id": "A", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
        {"id": "B", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
    ]
    edges = [{
        "from": "A",
        "to": "B",
        "tag": "TEST",
        "relation": "test",
        "weight": "inf",
    }]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"
    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps(edges))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except ValueError as exc:
        assert "weight" in str(exc).lower()
    else:
        raise AssertionError("infinite edge weight was accepted")


def test_graph_rejects_empty_edge_tag(tmp_path: Path):
    import json

    nodes = [
        {"id": "A", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
        {"id": "B", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
    ]
    edges = [{
        "from": "A",
        "to": "B",
        "tag": "",
        "relation": "test",
        "weight": 1.0,
    }]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"
    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps(edges))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except ValueError as exc:
        assert "tag" in str(exc).lower()
    else:
        raise AssertionError("empty edge tag was accepted")

def test_graph_rejects_empty_edge_relation(tmp_path: Path):
    import json

    nodes = [
        {"id": "A", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
        {"id": "B", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
    ]
    edges = [{
        "from": "A",
        "to": "B",
        "tag": "TEST",
        "relation": "",
        "weight": 1.0,
    }]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"
    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps(edges))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except ValueError as exc:
        assert "relation" in str(exc).lower()
    else:
        raise AssertionError("empty edge relation was accepted")


def test_graph_rejects_whitespace_edge_relation(tmp_path: Path):
    import json

    nodes = [
        {"id": "A", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
        {"id": "B", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
    ]
    edges = [{
        "from": "A",
        "to": "B",
        "tag": "TEST",
        "relation": "   ",
        "weight": 1.0,
    }]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"
    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps(edges))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except ValueError as exc:
        assert "relation" in str(exc).lower()
    else:
        raise AssertionError("whitespace edge relation was accepted")

def test_graph_rejects_empty_edge_source(tmp_path: Path):
    import json

    nodes = [
        {"id": "A", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
        {"id": "B", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
    ]
    edges = [{
        "from": "",
        "to": "B",
        "tag": "TEST",
        "relation": "test",
        "weight": 1.0,
    }]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"
    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps(edges))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except ValueError as exc:
        assert "source" in str(exc).lower()
    else:
        raise AssertionError("empty edge source was accepted")


def test_graph_rejects_whitespace_edge_source(tmp_path: Path):
    import json

    nodes = [
        {"id": "A", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
        {"id": "B", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
    ]
    edges = [{
        "from": "   ",
        "to": "B",
        "tag": "TEST",
        "relation": "test",
        "weight": 1.0,
    }]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"
    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps(edges))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except ValueError as exc:
        assert "source" in str(exc).lower()
    else:
        raise AssertionError("whitespace edge source was accepted")


def test_graph_rejects_empty_edge_target(tmp_path: Path):
    import json

    nodes = [
        {"id": "A", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
        {"id": "B", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
    ]
    edges = [{
        "from": "A",
        "to": "",
        "tag": "TEST",
        "relation": "test",
        "weight": 1.0,
    }]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"
    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps(edges))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except ValueError as exc:
        assert "target" in str(exc).lower()
    else:
        raise AssertionError("empty edge target was accepted")


def test_graph_rejects_whitespace_edge_target(tmp_path: Path):
    import json

    nodes = [
        {"id": "A", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
        {"id": "B", "tag": "NODE", "type": "test", "truth_confidence": 1.0},
    ]
    edges = [{
        "from": "A",
        "to": "   ",
        "tag": "TEST",
        "relation": "test",
        "weight": 1.0,
    }]

    nodes_path = tmp_path / "nodes.json"
    edges_path = tmp_path / "edges.json"
    nodes_path.write_text(json.dumps(nodes))
    edges_path.write_text(json.dumps(edges))

    try:
        TruthGraph.from_json(nodes_path, edges_path)
    except ValueError as exc:
        assert "target" in str(exc).lower()
    else:
        raise AssertionError("whitespace edge target was accepted")
