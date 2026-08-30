from pathlib import Path

from openmind.experimental.fuzzy_graph import FuzzyVectorGraph
from openmind.truth_graph import TruthGraph


ROOT = Path(__file__).resolve().parents[2]


def graph() -> TruthGraph:
    return TruthGraph.from_json(
        ROOT / "demo/truth_graph/nodes.json",
        ROOT / "demo/truth_graph/edges.json",
    )


def test_vector_derives_from_canonical_graph():
    fuzzy = FuzzyVectorGraph(graph())

    vector = fuzzy.node_vector("ENGINE")

    assert vector.node_id == "ENGINE"
    assert len(vector.values) == 3
    assert 0.0 <= vector.predictive_weight <= 1.0
    assert vector.magnitude >= 0.0


def test_relationship_weight_is_bounded():
    fuzzy = FuzzyVectorGraph(graph())

    relationship = fuzzy.relationship("ENGINE", "TEST")

    assert relationship.source == "ENGINE"
    assert relationship.target == "TEST"
    assert 0.0 <= relationship.membership <= 1.0
    assert 0.0 <= relationship.predictive_weight <= 1.0


def test_canonical_graph_is_unchanged():
    truth = graph()
    fuzzy = FuzzyVectorGraph(truth)

    before = len(truth.edges)
    fuzzy.node_vector("ENGINE")
    fuzzy.relationship("ENGINE", "TEST")

    assert len(truth.edges) == before


def test_fuzzy_derivation_does_not_modify_canonical_node_confidence():
    truth = graph()

    before = {
        node_id: node.truth_confidence
        for node_id, node in truth.nodes.items()
    }

    fuzzy = FuzzyVectorGraph(truth)

    for node_id in truth.nodes:
        fuzzy.node_vector(node_id)

    after = {
        node_id: node.truth_confidence
        for node_id, node in truth.nodes.items()
    }

    assert after == before


def test_fuzzy_derivation_does_not_modify_canonical_edge_weights():
    truth = graph()

    before = [
        (edge.source, edge.target, edge.weight)
        for edge in truth.edges
    ]

    fuzzy = FuzzyVectorGraph(truth)

    for edge in truth.edges:
        fuzzy.relationship(edge.source, edge.target)

    after = [
        (edge.source, edge.target, edge.weight)
        for edge in truth.edges
    ]

    assert after == before


def test_fuzzy_derivation_does_not_modify_provenance():
    truth = graph()

    before = [
        (edge.source, edge.target, edge.provenance)
        for edge in truth.edges
    ]

    fuzzy = FuzzyVectorGraph(truth)

    for edge in truth.edges:
        fuzzy.relationship(edge.source, edge.target)

    after = [
        (edge.source, edge.target, edge.provenance)
        for edge in truth.edges
    ]

    assert after == before


def test_fuzzy_derivation_does_not_change_canonical_path_score():
    truth = graph()

    canonical_before = truth.best_path("PROJECT", "EVIDENCE")

    assert canonical_before is not None
    assert canonical_before.score == 0.8758

    fuzzy = FuzzyVectorGraph(truth)

    for node_id in truth.nodes:
        fuzzy.node_vector(node_id)

    for edge in truth.edges:
        fuzzy.relationship(edge.source, edge.target)

    canonical_after = truth.best_path("PROJECT", "EVIDENCE")

    assert canonical_after is not None
    assert canonical_after.score == canonical_before.score
    assert canonical_after == canonical_before


def test_node_vector_is_deterministic():
    truth = graph()
    fuzzy = FuzzyVectorGraph(truth)

    first = fuzzy.node_vector("ENGINE")
    second = fuzzy.node_vector("ENGINE")

    assert first == second


def test_relationship_membership_is_deterministic():
    truth = graph()
    fuzzy = FuzzyVectorGraph(truth)

    first = fuzzy.relationship("ENGINE", "TEST")
    second = fuzzy.relationship("ENGINE", "TEST")

    assert first == second


def test_all_node_vectors_have_bounded_predictive_weight():
    truth = graph()
    fuzzy = FuzzyVectorGraph(truth)

    for node_id in truth.nodes:
        vector = fuzzy.node_vector(node_id)

        assert 0.0 <= vector.predictive_weight <= 1.0
        assert vector.magnitude >= 0.0
        assert all(
            value == value
            for value in vector.values
        )


def test_all_relationship_memberships_are_bounded():
    truth = graph()
    fuzzy = FuzzyVectorGraph(truth)

    for edge in truth.edges:
        relationship = fuzzy.relationship(
            edge.source,
            edge.target,
        )

        assert 0.0 <= relationship.membership <= 1.0
        assert 0.0 <= relationship.predictive_weight <= 1.0


def test_unknown_node_vector_is_rejected():
    truth = graph()
    fuzzy = FuzzyVectorGraph(truth)

    try:
        fuzzy.node_vector("DOES_NOT_EXIST")
    except KeyError:
        pass
    else:
        raise AssertionError("unknown node was accepted")


def test_unknown_relationship_is_rejected():
    truth = graph()
    fuzzy = FuzzyVectorGraph(truth)

    try:
        fuzzy.relationship("ENGINE", "DOES_NOT_EXIST")
    except KeyError as exc:
        assert "No relationship" in str(exc)
    else:
        raise AssertionError("unknown relationship was accepted")
