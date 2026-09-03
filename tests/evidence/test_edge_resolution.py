from openmind.evidence import (
    EvidenceRecord,
    EvidenceRegistry,
    resolve_edge_evidence,
)


def registry():
    return EvidenceRegistry([
        EvidenceRecord(
            id="E1",
            source="artifact:test",
            claim="TEST produces EVIDENCE",
            confidence=0.96,
        )
    ])


def test_registered_evidence():
    result = resolve_edge_evidence(
        "TEST",
        "EVIDENCE",
        "E1",
        registry(),
    )

    assert result.status == "REGISTERED"
    assert result.evidence_id == "E1"


def test_unbound_evidence():
    result = resolve_edge_evidence(
        "AGENT",
        "DOCS",
        None,
        registry(),
    )

    assert result.status == "UNBOUND"
    assert result.evidence_id is None


def test_missing_evidence():
    result = resolve_edge_evidence(
        "ENGINE",
        "TEST",
        "DOES_NOT_EXIST",
        registry(),
    )

    assert result.status == "MISSING"
    assert result.evidence_id == "DOES_NOT_EXIST"
