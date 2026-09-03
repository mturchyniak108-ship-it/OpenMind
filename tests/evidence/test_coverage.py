from openmind.evidence import (
    ResolvedEdgeEvidence,
    calculate_provenance_coverage,
)


def test_provenance_coverage():
    edges = (
        ResolvedEdgeEvidence("A", "B", "E1", "REGISTERED"),
        ResolvedEdgeEvidence("B", "C", None, "UNBOUND"),
        ResolvedEdgeEvidence("C", "D", "E2", "REGISTERED"),
        ResolvedEdgeEvidence("D", "E", None, "UNBOUND"),
        ResolvedEdgeEvidence("E", "F", "E3", "REGISTERED"),
    )

    result = calculate_provenance_coverage(edges)

    assert result.total_edges == 5
    assert result.registered_edges == 3
    assert result.unbound_edges == 2
    assert result.missing_edges == 0
    assert result.coverage == 0.6


def test_missing_evidence_is_tracked():
    edges = (
        ResolvedEdgeEvidence("A", "B", "E1", "REGISTERED"),
        ResolvedEdgeEvidence("B", "C", "MISSING_ID", "MISSING"),
    )

    result = calculate_provenance_coverage(edges)

    assert result.total_edges == 2
    assert result.registered_edges == 1
    assert result.missing_edges == 1
    assert result.coverage == 0.5


def test_empty_trace_has_zero_coverage():
    result = calculate_provenance_coverage(())

    assert result.total_edges == 0
    assert result.coverage == 0.0


def test_provenance_coverage_reports_unbound_edges():
    edges = (
        ResolvedEdgeEvidence("PROJECT", "AGENT", "E1", "REGISTERED"),
        ResolvedEdgeEvidence("AGENT", "DOCS", None, "UNBOUND"),
        ResolvedEdgeEvidence("DOCS", "ENGINE", None, "UNBOUND"),
        ResolvedEdgeEvidence("ENGINE", "TEST", "E2", "REGISTERED"),
    )

    result = calculate_provenance_coverage(edges)

    assert result.unbound_edges == 2
    assert result.unbound == (
        ("AGENT", "DOCS"),
        ("DOCS", "ENGINE"),
    )


def test_provenance_coverage_reports_missing_edges():
    edges = (
        ResolvedEdgeEvidence("A", "B", "E1", "REGISTERED"),
        ResolvedEdgeEvidence("B", "C", "E_MISSING", "MISSING"),
    )

    result = calculate_provenance_coverage(edges)

    assert result.missing == (
        ("B", "C"),
    )
