from pathlib import Path

from openmind.evidence import (
    EdgeEvidenceBinding,
    EdgeEvidenceBindings,
)


ROOT = Path(__file__).resolve().parents[2]


def test_bindings_load_from_canonical_manifest():
    bindings = EdgeEvidenceBindings.load(
        ROOT / "demo/truth_graph/bindings.json"
    )

    assert bindings.get(
        "PROJECT",
        "AGENT",
    ) == "E_PROJECT_AGENT"

    assert bindings.get(
        "ENGINE",
        "TEST",
    ) == "E_ENGINE_TEST"

    assert bindings.get(
        "TEST",
        "EVIDENCE",
    ) == "E_TEST_EVIDENCE"


def test_unbound_edge_returns_none():
    bindings = EdgeEvidenceBindings.load(
        ROOT / "demo/truth_graph/bindings.json"
    )

    assert bindings.get(
        "AGENT",
        "DOCS",
    ) is None


def test_binding_is_immutable():
    binding = EdgeEvidenceBinding(
        source="ENGINE",
        target="TEST",
        evidence_id="E_ENGINE_TEST",
    )

    assert binding.source == "ENGINE"
    assert binding.target == "TEST"
    assert binding.evidence_id == "E_ENGINE_TEST"


def test_conflicting_duplicate_binding_is_rejected():
    try:
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
    except ValueError as exc:
        assert "conflicting edge evidence binding" in str(exc)
    else:
        raise AssertionError(
            "conflicting duplicate binding was silently accepted"
        )


def test_identical_duplicate_binding_is_deterministic():
    bindings = EdgeEvidenceBindings([
        EdgeEvidenceBinding(
            source="ENGINE",
            target="TEST",
            evidence_id="E_ENGINE_TEST",
        ),
        EdgeEvidenceBinding(
            source="ENGINE",
            target="TEST",
            evidence_id="E_ENGINE_TEST",
        ),
    ])

    assert bindings.get("ENGINE", "TEST") == "E_ENGINE_TEST"


def test_validate_bindings_accepts_registered_evidence():
    from openmind.evidence import EvidenceRecord, EvidenceRegistry

    bindings = EdgeEvidenceBindings([
        EdgeEvidenceBinding(
            source="ENGINE",
            target="TEST",
            evidence_id="E_ENGINE_TEST",
        ),
    ])

    registry = EvidenceRegistry([
        EvidenceRecord(
            id="E_ENGINE_TEST",
            source="artifact:test",
            claim="ENGINE validated by TEST",
            confidence=0.97,
        ),
    ])

    assert bindings.validate(registry) == ()


def test_validate_bindings_rejects_missing_evidence():
    from openmind.evidence import EvidenceRegistry

    bindings = EdgeEvidenceBindings([
        EdgeEvidenceBinding(
            source="ENGINE",
            target="TEST",
            evidence_id="E_DOES_NOT_EXIST",
        ),
    ])

    try:
        bindings.validate(EvidenceRegistry())
    except ValueError as exc:
        assert "missing evidence binding" in str(exc)
        assert "E_DOES_NOT_EXIST" in str(exc)
    else:
        raise AssertionError(
            "missing evidence binding was silently accepted"
        )


def test_validate_graph_accepts_existing_edges():
    from openmind.truth_graph import TruthEdge, TruthGraph, TruthNode

    graph = TruthGraph(
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

    bindings = EdgeEvidenceBindings([
        EdgeEvidenceBinding(
            source="A",
            target="B",
            evidence_id="E1",
        ),
    ])

    assert bindings.validate_graph(graph) == ()


def test_validate_graph_rejects_unknown_edges():
    from openmind.truth_graph import TruthEdge, TruthGraph, TruthNode

    graph = TruthGraph(
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

    bindings = EdgeEvidenceBindings([
        EdgeEvidenceBinding(
            source="FAKE",
            target="EDGE",
            evidence_id="E1",
        ),
    ])

    try:
        bindings.validate_graph(graph)
    except ValueError as exc:
        assert "binding references unknown graph edge" in str(exc)
        assert "FAKE -> EDGE" in str(exc)
    else:
        raise AssertionError(
            "unknown graph edge binding was silently accepted"
        )
