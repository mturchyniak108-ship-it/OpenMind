from openmind.evidence import (
    ArtifactEvidenceBinding,
    bind_evidence_to_edge,
)
from openmind.truth_graph import TruthEdge


def test_edge_provenance_binding_is_immutable():
    edge = TruthEdge(
        source="TEST",
        target="EVIDENCE",
        tag="PRODUCES",
        relation="produces",
        weight=0.96,
    )

    binding = ArtifactEvidenceBinding(
        artifact_id="artifact:abc",
        evidence_id="E_TEST_EVIDENCE",
        claim="TEST produces EVIDENCE",
    )

    bound = bind_evidence_to_edge(edge, binding)

    assert edge.provenance == ()
    assert bound.provenance == ("E_TEST_EVIDENCE",)


def test_edge_provenance_binding_preserves_canonical_fields():
    edge = TruthEdge(
        source="ENGINE",
        target="TEST",
        tag="VALIDATED_BY",
        relation="validated_by",
        weight=0.97,
    )

    binding = ArtifactEvidenceBinding(
        artifact_id="artifact:def",
        evidence_id="E_ENGINE_TEST",
        claim="ENGINE validated by TEST",
    )

    bound = bind_evidence_to_edge(edge, binding)

    assert bound.source == edge.source
    assert bound.target == edge.target
    assert bound.tag == edge.tag
    assert bound.relation == edge.relation
    assert bound.weight == edge.weight
    assert bound.provenance == ("E_ENGINE_TEST",)


def test_multiple_bindings_preserve_order():
    edge = TruthEdge(
        source="PROJECT",
        target="AGENT",
        tag="DOCUMENTED_FOR",
        relation="documented_for",
        weight=0.95,
    )

    first = ArtifactEvidenceBinding(
        artifact_id="artifact:a",
        evidence_id="E1",
        claim="claim one",
    )

    second = ArtifactEvidenceBinding(
        artifact_id="artifact:b",
        evidence_id="E2",
        claim="claim two",
    )

    edge = bind_evidence_to_edge(edge, first)
    edge = bind_evidence_to_edge(edge, second)

    assert edge.provenance == ("E1", "E2")
