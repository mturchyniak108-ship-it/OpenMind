from openmind.experimental.fuzzy_graph import PredictivePathScorer
from openmind.truth_graph import TruthEdge, TruthGraph, TruthNode


def competing_graph() -> TruthGraph:
    """Build a graph with two competing paths.

    Canonical path has higher node confidence.
    Experimental path has stronger edge weights so that the
    predictive scorer can legitimately rank it higher.
    """
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
            truth_confidence=0.85,
        ),
        "PREDICTIVE_B": TruthNode(
            id="PREDICTIVE_B",
            tag="predictive",
            type="concept",
            truth_confidence=0.85,
        ),
        "END": TruthNode(
            id="END",
            tag="end",
            type="concept",
            truth_confidence=1.0,
        ),
    }

    edges = [
        # Canonical path — high node confidence, solid edge weights
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
        # Experimental path — stronger edge weights so predictive
        # ranking can diverge while remaining a valid canonical path.
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
    """Predictive ranking may diverge; canonical TruthGraph stays authoritative.

    Architectural invariants (ROADMAP / TODO / docs/ai):
    - Truth Graph = canonical knowledge.
    - Predictive scoring is a derived experimental signal only.
    - Experimental ranking must never mutate or replace canonical best_path.
    """
    truth = competing_graph()

    canonical = truth.best_path("START", "END")
    predictive = PredictivePathScorer(truth).best_path("START", "END")

    assert canonical is not None
    assert predictive is not None

    # Canonical ranking remains the high-confidence structured path.
    assert canonical.nodes == (
        "START",
        "CANONICAL_A",
        "CANONICAL_B",
        "END",
    )

    # Predictive ranking selects the stronger-edge experimental path.
    assert predictive.path.nodes == (
        "START",
        "PREDICTIVE_A",
        "PREDICTIVE_B",
        "END",
    )

    # Genuine divergence: predictive ranking differs from canonical.
    assert predictive.path != canonical

    # The predictive path is still a valid path that exists in the
    # canonical graph (no new nodes/edges were invented).
    assert predictive.path in truth.find_paths("START", "END")

    # Predictive score of the experimental path is higher than the
    # score the same scorer would give the canonical path.
    canonical_scored = PredictivePathScorer(truth).score(canonical)
    assert predictive.predictive_score > canonical_scored.predictive_score

    # Canonical TruthGraph is completely unchanged.
    assert truth.best_path("START", "END") == canonical


def test_predictive_result_preserves_canonical_path_identity():
    """Divergence changes ranking only; path objects remain canonical."""
    truth = competing_graph()

    canonical = truth.best_path("START", "END")
    predictive = PredictivePathScorer(truth).best_path("START", "END")

    assert canonical is not None
    assert predictive is not None

    # Predictive result is still a TruthPath that belongs to the
    # canonical graph. Ranking may differ; identity does not.
    assert predictive.path in truth.find_paths("START", "END")
    assert predictive.path != canonical


def test_predictive_divergence_is_deterministic():
    """Predictive ranking must be deterministic for identical inputs."""
    truth = competing_graph()
    scorer = PredictivePathScorer(truth)

    first = scorer.best_path("START", "END")
    second = scorer.best_path("START", "END")

    assert first is not None
    assert second is not None
    assert first == second
