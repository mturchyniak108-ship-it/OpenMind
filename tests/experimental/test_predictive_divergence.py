from openmind.experimental.fuzzy_graph import PredictivePathScorer
from openmind.truth_graph import TruthEdge, TruthGraph, TruthNode


def competing_graph() -> TruthGraph:
    nodes = {
        "START": TruthNode(
            id="START",
            tag="start",
            type="concept",
            truth_confidence=1.0,
        ),
        "CANONICAL_A": TruthNode(
            id="CANONICAL_A",
            tag="canonical",
            type="concept",
            truth_confidence=0.95,
        ),
        "CANONICAL_B": TruthNode(
            id="CANONICAL_B",
            tag="canonical",
            type="concept",
            truth_confidence=0.95,
        ),
        "PREDICTIVE_A": TruthNode(
            id="PREDICTIVE_A",
            tag="predictive",
            type="concept",
            truth_confidence=0.20,
        ),
        "PREDICTIVE_B": TruthNode(
            id="PREDICTIVE_B",
            tag="predictive",
            type="concept",
            truth_confidence=0.20,
        ),
        "END": TruthNode(
            id="END",
            tag="end",
            type="concept",
            truth_confidence=1.0,
        ),
    }

    edges = [
        # Canonical path:
        # high edge weights + high node confidence
        TruthEdge(
            source="START",
            target="CANONICAL_A",
            tag="canonical",
            relation="supports",
            weight=0.80,
        ),
        TruthEdge(
            source="CANONICAL_A",
            target="CANONICAL_B",
            tag="canonical",
            relation="supports",
            weight=0.80,
        ),
        TruthEdge(
            source="CANONICAL_B",
            target="END",
            tag="canonical",
            relation="supports",
            weight=0.80,
        ),

        # Experimental path:
        # slightly stronger relationships but poor intermediate
        # confidence, allowing fuzzy scoring to penalize it.
        TruthEdge(
            source="START",
            target="PREDICTIVE_A",
            tag="predictive",
            relation="supports",
            weight=0.84,
        ),
        TruthEdge(
            source="PREDICTIVE_A",
            target="PREDICTIVE_B",
            tag="predictive",
            relation="supports",
            weight=0.84,
        ),
        TruthEdge(
            source="PREDICTIVE_B",
            target="END",
            tag="predictive",
            relation="supports",
            weight=0.84,
        ),
    ]

    return TruthGraph(nodes, edges)


def test_predictive_divergence_does_not_replace_canonical_truth():
    truth = competing_graph()

    canonical = truth.best_path("START", "END")
    predictive = PredictivePathScorer(truth).best_path(
        "START",
        "END",
    )

    assert canonical is not None
    assert predictive is not None

    assert canonical.nodes == (
        "START",
        "CANONICAL_A",
        "CANONICAL_B",
        "END",
    )

    assert truth.best_path("START", "END") == canonical

    # Experimental scoring must never mutate or replace
    # the canonical TruthPath.
    assert truth.best_path("START", "END") == canonical


def test_predictive_result_preserves_canonical_path_identity():
    truth = competing_graph()

    canonical = truth.best_path("START", "END")
    predictive = PredictivePathScorer(truth).best_path(
        "START",
        "END",
    )

    assert canonical is not None
    assert predictive is not None

    assert predictive.path == canonical


def test_predictive_divergence_is_deterministic():
    truth = competing_graph()
    scorer = PredictivePathScorer(truth)

    first = scorer.best_path("START", "END")
    second = scorer.best_path("START", "END")

    assert first is not None
    assert second is not None
    assert first == second
