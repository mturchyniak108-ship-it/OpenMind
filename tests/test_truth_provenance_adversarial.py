import pytest

from openmind.evidence import (
    EdgeEvidenceBinding,
    EdgeEvidenceBindings,
    EvidenceRecord,
    EvidenceRegistry,
    TruthTraceResolver,
    audit_truth_trace,
)
from openmind.truth_graph import TruthGraph


def test_unknown_evidence_id_is_missing_not_registered():
    registry = EvidenceRegistry([
        EvidenceRecord(
            id="E_REAL",
            source="test",
            claim="real evidence",
            confidence=1.0,
        )
    ])

    # Use the canonical demo graph for an actual trace.
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    graph = TruthGraph.from_json(
        root / "demo/truth_graph/nodes.json",
        root / "demo/truth_graph/edges.json",
    )

    resolver = TruthTraceResolver(
        graph,
        list(registry.all()),
    )

    trace = resolver.resolve(
        "PROJECT",
        "EVIDENCE",
        {
            ("PROJECT", "AGENT"): "E_UNKNOWN",
        },
    )

    assert trace is not None

    audited = audit_truth_trace(trace, registry)

    first = audited.evidence[0]

    assert first.evidence_id == "E_UNKNOWN"
    assert first.status == "MISSING"
    assert audited.coverage.missing_edges == 1
    assert audited.coverage.registered_edges == 0


def test_unbound_edge_remains_unbound():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    graph = TruthGraph.from_json(
        root / "demo/truth_graph/nodes.json",
        root / "demo/truth_graph/edges.json",
    )

    resolver = TruthTraceResolver(graph, [])

    trace = resolver.resolve(
        "PROJECT",
        "EVIDENCE",
        {},
    )

    assert trace is not None

    audited = audit_truth_trace(
        trace,
        EvidenceRegistry(),
    )

    assert audited.evidence[0].status == "UNBOUND"
    assert audited.coverage.unbound_edges == 5
    assert audited.coverage.coverage == 0.0


def test_conflicting_edge_binding_is_rejected():
    with pytest.raises(
        ValueError,
        match="conflicting edge evidence binding",
    ):
        EdgeEvidenceBindings([
            EdgeEvidenceBinding(
                source="ENGINE",
                target="TEST",
                evidence_id="E_ONE",
            ),
            EdgeEvidenceBinding(
                source="ENGINE",
                target="TEST",
                evidence_id="E_TWO",
            ),
        ])


def test_conflicting_evidence_id_is_rejected():
    with pytest.raises(
        ValueError,
        match="conflicting evidence id",
    ):
        EvidenceRegistry([
            EvidenceRecord(
                id="E_DUP",
                source="source-a",
                claim="claim-a",
                confidence=0.9,
            ),
            EvidenceRecord(
                id="E_DUP",
                source="source-b",
                claim="claim-b",
                confidence=0.8,
            ),
        ])


def test_missing_binding_validation_is_explicit():
    registry = EvidenceRegistry([
        EvidenceRecord(
            id="E_REAL",
            source="source",
            claim="claim",
            confidence=1.0,
        )
    ])

    bindings = EdgeEvidenceBindings([
        EdgeEvidenceBinding(
            source="ENGINE",
            target="TEST",
            evidence_id="E_MISSING",
        )
    ])

    with pytest.raises(
        ValueError,
        match="missing evidence binding",
    ):
        bindings.validate(registry)


def test_provenance_cannot_change_canonical_score():
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    graph = TruthGraph.from_json(
        root / "demo/truth_graph/nodes.json",
        root / "demo/truth_graph/edges.json",
    )

    baseline = graph.best_path("PROJECT", "EVIDENCE")

    assert baseline is not None
    assert baseline.score == 0.8758

    evidence = [
        EvidenceRecord(
            id="E_ONE",
            source="x",
            claim="claim",
            confidence=0.0,
        ),
        EvidenceRecord(
            id="E_TWO",
            source="y",
            claim="different claim",
            confidence=1.0,
        ),
    ]

    resolver = TruthTraceResolver(graph, evidence)

    trace = resolver.resolve(
        "PROJECT",
        "EVIDENCE",
        {
            ("PROJECT", "AGENT"): "E_ONE",
            ("AGENT", "DOCS"): "E_TWO",
            ("DOCS", "ENGINE"): "E_ONE",
            ("ENGINE", "TEST"): "E_TWO",
            ("TEST", "EVIDENCE"): "E_ONE",
        },
    )

    assert trace is not None
    assert trace.score == 0.8758

    audited = audit_truth_trace(
        trace,
        EvidenceRegistry(evidence),
    )

    assert audited.score == 0.8758
    assert graph.best_path(
        "PROJECT",
        "EVIDENCE",
    ) == baseline
