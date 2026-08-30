from pathlib import Path

from openmind.evidence import (
    ArtifactEvidenceBinding,
    bind_evidence_to_edge,
)
from openmind.truth_graph import TruthEdge, TruthGraph


ROOT = Path(__file__).resolve().parents[1]


def test_canonical_provenance_contract():
    graph = TruthGraph.from_json(
        ROOT / "demo/truth_graph/nodes.json",
        ROOT / "demo/truth_graph/edges.json",
    )

    assert len(graph.nodes) == 20
    assert len(graph.edges) == 24

    path = graph.best_path("PROJECT", "EVIDENCE")

    assert path is not None
    assert path.nodes == (
        "PROJECT",
        "AGENT",
        "DOCS",
        "ENGINE",
        "TEST",
        "EVIDENCE",
    )
    assert path.score == 0.8758

    edge = TruthEdge(
        source="TEST",
        target="EVIDENCE",
        tag="PRODUCES",
        relation="produces",
        weight=0.96,
    )

    binding = ArtifactEvidenceBinding(
        artifact_id="artifact:test",
        evidence_id="E_TEST_EVIDENCE",
        claim="TEST produces EVIDENCE",
    )

    bound = bind_evidence_to_edge(edge, binding)

    assert edge.provenance == ()
    assert bound.provenance == ("E_TEST_EVIDENCE",)
    assert bound.weight == edge.weight
    assert bound.source == edge.source
    assert bound.target == edge.target

    # Provenance is annotation, never scoring input.
    assert graph.best_path("PROJECT", "EVIDENCE").score == 0.8758
