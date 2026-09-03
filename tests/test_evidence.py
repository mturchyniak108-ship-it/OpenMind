from openmind.evidence import EvidenceRecord, ProvenanceRecord


def test_evidence_record_is_deterministic():
    evidence = EvidenceRecord(
        id="E1",
        source="test",
        claim="ENGINE produces TEST",
        confidence=0.96,
    )

    assert evidence.id == "E1"
    assert evidence.source == "test"
    assert evidence.claim == "ENGINE produces TEST"
    assert evidence.confidence == 0.96


def test_provenance_record_is_deterministic():
    provenance = ProvenanceRecord(
        evidence_id="E1",
        relation="produces",
        source_node="TEST",
        target_node="EVIDENCE",
    )

    assert provenance.evidence_id == "E1"
    assert provenance.relation == "produces"
    assert provenance.source_node == "TEST"
    assert provenance.target_node == "EVIDENCE"


def test_evidence_confidence_is_independent_of_path_scoring():
    evidence = EvidenceRecord(
        id="E2",
        source="benchmark",
        claim="TEST produces EVIDENCE",
        confidence=0.99,
    )

    assert evidence.confidence == 0.99
