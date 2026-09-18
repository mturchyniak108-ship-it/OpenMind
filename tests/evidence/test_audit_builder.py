from openmind.evidence import (
    EvidenceRecord,
    EvidenceRegistry,
    TruthTrace,
    TraceStep,
    audit_truth_trace,
)


def test_audit_truth_trace_resolves_provenance():
    trace = TruthTrace(
        start="PROJECT",
        end="EVIDENCE",
        steps=(
            TraceStep(
                source="PROJECT",
                target="AGENT",
                relation="documented_for",
                weight=0.95,
                evidence_id="E1",
            ),
            TraceStep(
                source="AGENT",
                target="DOCS",
                relation="uses",
                weight=0.96,
                evidence_id=None,
            ),
            TraceStep(
                source="ENGINE",
                target="TEST",
                relation="validated_by",
                weight=0.97,
                evidence_id="E2",
            ),
        ),
        score=0.8758,
    )

    registry = EvidenceRegistry([
        EvidenceRecord(
            id="E1",
            source="artifact:one",
            claim="PROJECT documents AGENT",
            confidence=0.95,
        ),
        EvidenceRecord(
            id="E2",
            source="artifact:two",
            claim="ENGINE validated by TEST",
            confidence=0.97,
        ),
    ])

    audited = audit_truth_trace(trace, registry)

    assert audited.score == 0.8758
    assert audited.start == "PROJECT"
    assert audited.end == "EVIDENCE"

    assert [
        item.status
        for item in audited.evidence
    ] == [
        "REGISTERED",
        "UNBOUND",
        "REGISTERED",
    ]

    assert audited.coverage.total_edges == 3
    assert audited.coverage.registered_edges == 2
    assert audited.coverage.unbound_edges == 1
    assert audited.coverage.missing_edges == 0
    assert audited.coverage.coverage == 2 / 3
