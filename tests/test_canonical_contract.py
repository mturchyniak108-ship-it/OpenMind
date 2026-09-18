import json
from pathlib import Path

from openmind.evidence import EvidenceRecord, TruthTraceResolver
from openmind.truth_graph import TruthGraph


ROOT = Path(__file__).resolve().parents[1]


def load_graph():
    return TruthGraph.from_json(
        ROOT / "demo/truth_graph/nodes.json",
        ROOT / "demo/truth_graph/edges.json",
    )


def load_evidence():
    data = json.loads(
        (ROOT / "demo/truth_graph/evidence.json").read_text()
    )
    return [
        EvidenceRecord(
            id=item["id"],
            source=item["source"],
            claim=item["claim"],
            confidence=float(item["confidence"]),
        )
        for item in data
    ]


def test_canonical_contract_is_stable():
    contract = json.loads(
        (
            ROOT
            / "benchmarks/truth_graph/results/canonical_contract.json"
        ).read_text()
    )

    assert contract["status"] == "canonical"
    assert contract["experimental"] is False

    assert contract["invariants"]["truth_graph_is_authoritative"] is True
    assert contract["invariants"]["predictive_layers_are_experimental"] is True
    assert contract["invariants"]["evidence_does_not_modify_graph"] is True
    assert contract["invariants"]["provenance_does_not_modify_score"] is True


def test_project_to_evidence_contract():
    graph = load_graph()
    evidence = load_evidence()

    resolver = TruthTraceResolver(graph, evidence)

    trace = resolver.resolve(
        "PROJECT",
        "EVIDENCE",
        {
            ("PROJECT", "AGENT"): "E_PROJECT_AGENT",
            ("ENGINE", "TEST"): "E_ENGINE_TEST",
            ("TEST", "EVIDENCE"): "E_TEST_EVIDENCE",
        },
    )

    assert trace is not None

    assert trace.start == "PROJECT"
    assert trace.end == "EVIDENCE"

    assert trace.steps[0].evidence_id == "E_PROJECT_AGENT"
    assert trace.steps[3].evidence_id == "E_ENGINE_TEST"
    assert trace.steps[4].evidence_id == "E_TEST_EVIDENCE"

    assert trace.score == 0.8758


def test_engine_to_evidence_contract():
    graph = load_graph()
    evidence = load_evidence()

    resolver = TruthTraceResolver(graph, evidence)

    trace = resolver.resolve(
        "ENGINE",
        "EVIDENCE",
        {
            ("ENGINE", "TEST"): "E_ENGINE_TEST",
            ("TEST", "EVIDENCE"): "E_TEST_EVIDENCE",
        },
    )

    assert trace is not None
    assert trace.score == 0.94075

    assert [
        (step.source, step.target)
        for step in trace.steps
    ] == [
        ("ENGINE", "TEST"),
        ("TEST", "EVIDENCE"),
    ]


def test_evidence_cannot_change_canonical_graph():
    graph = load_graph()

    before = graph.best_path("PROJECT", "EVIDENCE")
    assert before is not None

    resolver = TruthTraceResolver(
        graph,
        load_evidence(),
    )

    trace = resolver.resolve(
        "PROJECT",
        "EVIDENCE",
        {},
    )

    assert trace is not None

    after = graph.best_path("PROJECT", "EVIDENCE")

    assert after == before
    assert after.score == 0.8758
