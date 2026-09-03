from pathlib import Path

from openmind.evidence import (
    EvidenceRegistry,
    TruthTraceResolver,
)
from openmind.ingestion import ingest_as_evidence
from openmind.truth_graph import TruthGraph


ROOT = Path(__file__).resolve().parents[2]


def test_ingested_artifact_becomes_truth_trace_evidence(tmp_path: Path):
    artifact = tmp_path / "engine_test.txt"
    artifact.write_text("ENGINE validated_by TEST\n")

    evidence = ingest_as_evidence(
        artifact,
        claim="ENGINE validated_by TEST",
        confidence=0.97,
        source="canonical-test",
    )

    registry = EvidenceRegistry([evidence])

    graph = TruthGraph.from_json(
        ROOT / "demo/truth_graph/nodes.json",
        ROOT / "demo/truth_graph/edges.json",
    )

    resolver = TruthTraceResolver(
        graph,
        registry.all(),
    )

    trace = resolver.resolve(
        "ENGINE",
        "EVIDENCE",
        {
            ("ENGINE", "TEST"): evidence.id,
            ("TEST", "EVIDENCE"): "E_TEST_EVIDENCE",
        },
    )

    assert trace is not None
    assert trace.start == "ENGINE"
    assert trace.end == "EVIDENCE"

    assert trace.steps[0].evidence_id == evidence.id
    assert trace.steps[1].evidence_id == "E_TEST_EVIDENCE"

    assert trace.score == 0.94075

    registered = registry.get(evidence.id)

    assert registered is not None
    assert registered.source == evidence.source
    assert registered.claim == "ENGINE validated_by TEST"
    assert registered.confidence == 0.97
