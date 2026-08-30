from openmind.evidence import (
    EvidenceRecord,
    EvidenceRegistry,
    AuditedTruthTrace,
    ProvenanceCoverage,
    ResolvedEdgeEvidence,
    TruthTrace,
    TraceStep,
    audit_truth_trace,
)


def test_audited_trace_preserves_canonical_score():
    trace = TruthTrace(
        start="PROJECT",
        end="EVIDENCE",
        steps=(
            TraceStep(
                source="PROJECT",
                target="EVIDENCE",
                relation="supports",
                weight=0.96,
                evidence_id="E1",
            ),
        ),
        score=0.8758,
    )

    evidence = (
        ResolvedEdgeEvidence(
            source="PROJECT",
            target="EVIDENCE",
            evidence_id="E1",
            status="REGISTERED",
        ),
    )

    coverage = ProvenanceCoverage(
        total_edges=1,
        registered_edges=1,
        unbound_edges=0,
        missing_edges=0,
        coverage=1.0,
    )

    audited = AuditedTruthTrace(
        trace=trace,
        evidence=evidence,
        coverage=coverage,
    )

    assert audited.start == "PROJECT"
    assert audited.end == "EVIDENCE"
    assert audited.score == 0.8758
    assert audited.coverage.coverage == 1.0


def test_audited_trace_is_immutable():
    trace = TruthTrace(
        start="A",
        end="B",
        steps=(),
        score=0.5,
    )

    audited = AuditedTruthTrace(
        trace=trace,
        evidence=(),
        coverage=ProvenanceCoverage(
            total_edges=0,
            registered_edges=0,
            unbound_edges=0,
            missing_edges=0,
            coverage=0.0,
        ),
    )

    try:
        audited.trace = trace
    except Exception:
        pass
    else:
        raise AssertionError("AuditedTruthTrace must be immutable")


def test_audited_trace_exposes_provenance_gaps():
    trace = TruthTrace(
        start="A",
        end="D",
        steps=(
            TraceStep(
                source="A",
                target="B",
                relation="supports",
                weight=0.95,
                evidence_id="E1",
            ),
            TraceStep(
                source="B",
                target="C",
                relation="uses",
                weight=0.96,
                evidence_id=None,
            ),
            TraceStep(
                source="C",
                target="D",
                relation="produces",
                weight=0.97,
                evidence_id="E_MISSING",
            ),
        ),
        score=0.8758,
    )

    from openmind.evidence import EvidenceRegistry, audit_truth_trace

    registry = EvidenceRegistry([
        EvidenceRecord(
            id="E1",
            source="artifact:test",
            claim="A supports B",
            confidence=0.95,
        ),
    ])

    audited = audit_truth_trace(trace, registry)

    assert audited.coverage.unbound == (
        ("B", "C"),
    )

    assert audited.coverage.missing == (
        ("C", "D"),
    )

    assert audited.score == 0.8758


def test_audited_trace_gap_lists_match_resolved_evidence():
    trace = TruthTrace(
        start="PROJECT",
        end="TEST",
        steps=(
            TraceStep(
                source="PROJECT",
                target="AGENT",
                relation="supports",
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
                source="DOCS",
                target="ENGINE",
                relation="uses",
                weight=0.97,
                evidence_id="E_MISSING",
            ),
        ),
        score=0.8758,
    )

    registry = EvidenceRegistry([
        EvidenceRecord(
            id="E1",
            source="artifact:test",
            claim="PROJECT supports AGENT",
            confidence=0.95,
        ),
    ])

    audited = audit_truth_trace(trace, registry)

    assert audited.coverage.unbound == (
        ("AGENT", "DOCS"),
    )

    assert audited.coverage.missing == (
        ("DOCS", "ENGINE"),
    )

    assert audited.coverage.registered_edges == 1
    assert audited.coverage.unbound_edges == 1
    assert audited.coverage.missing_edges == 1
    assert audited.coverage.total_edges == 3
    assert audited.coverage.coverage == 1 / 3

    assert audited.score == 0.8758
