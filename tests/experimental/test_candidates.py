from pathlib import Path

from openmind.experimental.fuzzy_graph import PredictivePathScorer
from openmind.experimental.candidates import ExperimentalCandidate
from openmind.truth_graph import TruthGraph


ROOT = Path(__file__).resolve().parents[2]


def graph() -> TruthGraph:
    return TruthGraph.from_json(
        ROOT / "demo/truth_graph/nodes.json",
        ROOT / "demo/truth_graph/edges.json",
    )


def test_candidate_wraps_canonical_predictive_result():
    truth = graph()
    predictive = PredictivePathScorer(truth).best_path(
        "PROJECT",
        "EVIDENCE",
    )

    assert predictive is not None

    candidate = ExperimentalCandidate.from_predictive_path(
        predictive
    )

    assert candidate.path == predictive.path
    assert candidate.predictive_score == predictive.predictive_score
    assert candidate.fuzzy_score == predictive.fuzzy_score
    assert candidate.relationship_score == predictive.relationship_score


def test_candidate_is_explicitly_non_canonical():
    truth = graph()
    predictive = PredictivePathScorer(truth).best_path(
        "PROJECT",
        "EVIDENCE",
    )

    assert predictive is not None

    candidate = ExperimentalCandidate.from_predictive_path(
        predictive
    )

    assert candidate.status == "CANDIDATE"
    assert candidate.canonical_score == predictive.path.score


def test_candidate_preserves_canonical_path_identity():
    truth = graph()

    canonical = truth.best_path("PROJECT", "EVIDENCE")
    predictive = PredictivePathScorer(truth).best_path(
        "PROJECT",
        "EVIDENCE",
    )

    assert canonical is not None
    assert predictive is not None

    candidate = ExperimentalCandidate.from_predictive_path(
        predictive
    )

    assert candidate.path == canonical
    assert candidate.path.score == 0.8758


def test_candidate_does_not_modify_truth_graph():
    truth = graph()

    before_nodes = dict(truth.nodes)
    before_edges = tuple(truth.edges)

    predictive = PredictivePathScorer(truth).best_path(
        "PROJECT",
        "EVIDENCE",
    )

    assert predictive is not None

    ExperimentalCandidate.from_predictive_path(predictive)

    assert truth.nodes == before_nodes
    assert tuple(truth.edges) == before_edges


def test_candidate_is_deterministic():
    truth = graph()
    scorer = PredictivePathScorer(truth)

    first = scorer.best_path("PROJECT", "EVIDENCE")
    second = scorer.best_path("PROJECT", "EVIDENCE")

    assert first is not None
    assert second is not None

    candidate_one = ExperimentalCandidate.from_predictive_path(first)
    candidate_two = ExperimentalCandidate.from_predictive_path(second)

    assert candidate_one == candidate_two
