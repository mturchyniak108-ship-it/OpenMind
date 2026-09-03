from pathlib import Path

from openmind.experimental.fuzzy_graph import PredictivePathScorer
from openmind.truth_graph import TruthGraph


ROOT = Path(__file__).resolve().parents[2]


def graph() -> TruthGraph:
    return TruthGraph.from_json(
        ROOT / "demo/truth_graph/nodes.json",
        ROOT / "demo/truth_graph/edges.json",
    )


def test_predictive_scorer_returns_path():
    scorer = PredictivePathScorer(graph())

    result = scorer.best_path("PROJECT", "EVIDENCE")

    assert result is not None
    assert result.path.nodes == (
        "PROJECT",
        "AGENT",
        "DOCS",
        "ENGINE",
        "TEST",
        "EVIDENCE",
    )


def test_predictive_score_is_bounded():
    scorer = PredictivePathScorer(graph())

    result = scorer.best_path("PROJECT", "EVIDENCE")

    assert result is not None
    assert 0.0 <= result.relationship_score <= 1.0
    assert 0.0 <= result.fuzzy_score <= 1.0
    assert result.predictive_score > 0.0


def test_canonical_path_score_remains_available():
    truth = graph()
    scorer = PredictivePathScorer(truth)

    canonical = truth.best_path("PROJECT", "EVIDENCE")
    predictive = scorer.best_path("PROJECT", "EVIDENCE")

    assert canonical is not None
    assert predictive is not None
    assert predictive.path == canonical
    assert canonical.score == 0.8758


def test_predictive_scoring_does_not_change_canonical_best_path():
    truth = graph()

    canonical_before = truth.best_path("PROJECT", "EVIDENCE")

    assert canonical_before is not None
    assert canonical_before.score == 0.8758

    scorer = PredictivePathScorer(truth)
    predictive = scorer.best_path("PROJECT", "EVIDENCE")

    assert predictive is not None

    canonical_after = truth.best_path("PROJECT", "EVIDENCE")

    assert canonical_after is not None
    assert canonical_after == canonical_before


def test_predictive_score_is_distinct_from_canonical_score():
    truth = graph()

    canonical = truth.best_path("PROJECT", "EVIDENCE")
    predictive = PredictivePathScorer(truth).best_path(
        "PROJECT",
        "EVIDENCE",
    )

    assert canonical is not None
    assert predictive is not None

    assert predictive.path.score == canonical.score
    assert predictive.predictive_score != canonical.score


def test_predictive_scoring_does_not_modify_canonical_edges():
    truth = graph()

    before = [
        (
            edge.source,
            edge.target,
            edge.weight,
            edge.provenance,
        )
        for edge in truth.edges
    ]

    PredictivePathScorer(truth).best_path(
        "PROJECT",
        "EVIDENCE",
    )

    after = [
        (
            edge.source,
            edge.target,
            edge.weight,
            edge.provenance,
        )
        for edge in truth.edges
    ]

    assert after == before


def test_predictive_best_path_uses_experimental_ordering_only():
    truth = graph()

    canonical = truth.best_path("PROJECT", "EVIDENCE")
    predictive = PredictivePathScorer(truth).best_path(
        "PROJECT",
        "EVIDENCE",
    )

    assert canonical is not None
    assert predictive is not None

    # Predictive selection is experimental and must not rewrite
    # or replace the canonical TruthPath.
    assert predictive.path == canonical
    assert truth.best_path("PROJECT", "EVIDENCE") == canonical


def test_predictive_scoring_is_deterministic():
    truth = graph()
    scorer = PredictivePathScorer(truth)

    first = scorer.best_path("PROJECT", "EVIDENCE")
    second = scorer.best_path("PROJECT", "EVIDENCE")

    assert first == second


def test_predictive_score_is_finite():
    truth = graph()
    scorer = PredictivePathScorer(truth)

    result = scorer.best_path("PROJECT", "EVIDENCE")

    assert result is not None
    assert result.predictive_score == result.predictive_score
    assert abs(result.predictive_score) != float("inf")


def test_predictive_score_preserves_canonical_path_metadata():
    truth = graph()
    scorer = PredictivePathScorer(truth)

    canonical = truth.best_path("PROJECT", "EVIDENCE")
    predictive = scorer.best_path("PROJECT", "EVIDENCE")

    assert canonical is not None
    assert predictive is not None

    assert predictive.path.nodes == canonical.nodes
    assert predictive.path.edges == canonical.edges
    assert predictive.path.cost == canonical.cost
    assert predictive.path.score == canonical.score
