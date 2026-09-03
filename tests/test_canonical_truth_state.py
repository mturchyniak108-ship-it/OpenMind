from openmind.evidence import (
    EdgeEvidenceBinding,
    EdgeEvidenceBindings,
    EvidenceRecord,
    EvidenceRegistry,
)
from openmind.truth_graph import (
    CanonicalTruthState,
    TruthEdge,
    TruthGraph,
    TruthNode,
)


def make_graph() -> TruthGraph:
    return TruthGraph(
        nodes={
            "A": TruthNode(
                id="A",
                tag="A",
                type="concept",
                truth_confidence=1.0,
            ),
            "B": TruthNode(
                id="B",
                tag="B",
                type="concept",
                truth_confidence=1.0,
            ),
        },
        edges=[
            TruthEdge(
                source="A",
                target="B",
                tag="SUPPORTS",
                relation="supports",
                weight=1.0,
            ),
        ],
    )


def make_evidence() -> EvidenceRegistry:
    return EvidenceRegistry([
        EvidenceRecord(
            id="E1",
            source="test",
            claim="A supports B",
            confidence=1.0,
        ),
    ])


def make_bindings() -> EdgeEvidenceBindings:
    return EdgeEvidenceBindings([
        EdgeEvidenceBinding(
            source="A",
            target="B",
            evidence_id="E1",
        ),
    ])


def test_canonical_truth_state_is_composable():
    state = CanonicalTruthState(
        graph=make_graph(),
        evidence=make_evidence(),
        bindings=make_bindings(),
    )

    assert state.graph is not None
    assert state.evidence is not None
    assert state.bindings is not None


def test_canonical_truth_state_validates():
    state = CanonicalTruthState(
        graph=make_graph(),
        evidence=make_evidence(),
        bindings=make_bindings(),
    )

    assert state.validate() == ()


def test_canonical_truth_state_rejects_missing_evidence():
    bindings = EdgeEvidenceBindings([
        EdgeEvidenceBinding(
            source="A",
            target="B",
            evidence_id="MISSING",
        ),
    ])

    state = CanonicalTruthState(
        graph=make_graph(),
        evidence=EvidenceRegistry(),
        bindings=bindings,
    )

    try:
        state.validate()
    except ValueError as exc:
        assert "missing evidence binding" in str(exc)
    else:
        raise AssertionError(
            "missing evidence was silently accepted"
        )


def test_canonical_truth_state_rejects_unknown_edge():
    bindings = EdgeEvidenceBindings([
        EdgeEvidenceBinding(
            source="FAKE",
            target="EDGE",
            evidence_id="E1",
        ),
    ])

    state = CanonicalTruthState(
        graph=make_graph(),
        evidence=make_evidence(),
        bindings=bindings,
    )

    try:
        state.validate()
    except ValueError as exc:
        assert "binding references unknown graph edge" in str(exc)
    else:
        raise AssertionError(
            "unknown graph edge was silently accepted"
        )
