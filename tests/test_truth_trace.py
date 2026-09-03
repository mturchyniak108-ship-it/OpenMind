import json
from pathlib import Path

from openmind.evidence import (
    EvidenceRecord,
    TruthTraceResolver,
)
from openmind.truth_graph import TruthGraph


ROOT = Path(__file__).resolve().parents[1]


def test_canonical_truth_trace():
    graph = TruthGraph.from_json(
        ROOT / "demo/truth_graph/nodes.json",
        ROOT / "demo/truth_graph/edges.json",
    )

    evidence_data = json.loads(
        (ROOT / "demo/truth_graph/evidence.json").read_text()
    )

    evidence = [
        EvidenceRecord(
            id=item["id"],
            source=item["source"],
            claim=item["claim"],
            confidence=float(item["confidence"]),
        )
        for item in evidence_data
    ]

    resolver = TruthTraceResolver(graph, evidence)

    bindings = {
        ("PROJECT", "AGENT"): "E_PROJECT_AGENT",
        ("ENGINE", "TEST"): "E_ENGINE_TEST",
        ("TEST", "EVIDENCE"): "E_TEST_EVIDENCE",
    }

    trace = resolver.resolve(
        "PROJECT",
        "EVIDENCE",
        bindings,
    )

    assert trace is not None
    assert trace.start == "PROJECT"
    assert trace.end == "EVIDENCE"

    assert [
        (step.source, step.target)
        for step in trace.steps
    ] == [
        ("PROJECT", "AGENT"),
        ("AGENT", "DOCS"),
        ("DOCS", "ENGINE"),
        ("ENGINE", "TEST"),
        ("TEST", "EVIDENCE"),
    ]

    assert trace.steps[0].evidence_id == "E_PROJECT_AGENT"
    assert trace.steps[3].evidence_id == "E_ENGINE_TEST"
    assert trace.steps[4].evidence_id == "E_TEST_EVIDENCE"

    # Canonical scoring must remain untouched.
    assert trace.score == 0.8758


def test_trace_does_not_change_graph():
    graph = TruthGraph.from_json(
        ROOT / "demo/truth_graph/nodes.json",
        ROOT / "demo/truth_graph/edges.json",
    )

    before = graph.best_path("PROJECT", "EVIDENCE")
    assert before is not None

    resolver = TruthTraceResolver(graph, [])

    trace = resolver.resolve(
        "PROJECT",
        "EVIDENCE",
        {},
    )

    assert trace is not None

    after = graph.best_path("PROJECT", "EVIDENCE")
    assert after == before
