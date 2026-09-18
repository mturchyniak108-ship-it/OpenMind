import json
from pathlib import Path

from openmind.ingestion import collect_artifact
from openmind.evidence import (
    EvidenceRecord,
    ProvenanceRecord,
    bind_artifact_to_evidence,
    TruthTraceResolver,
)
from openmind.truth_graph import TruthGraph


ROOT = Path(__file__).resolve().parents[1]


def test_end_to_end_artifact_to_truth(tmp_path: Path):
    artifact_path = tmp_path / "engine_test.txt"
    artifact_path.write_text("ENGINE validated_by TEST")

    artifact = collect_artifact(
        artifact_path,
        source="canonical-test",
    )

    evidence = EvidenceRecord(
        id="E_ENGINE_TEST",
        source=artifact.id,
        claim="ENGINE validated_by TEST",
        confidence=0.97,
    )

    binding = bind_artifact_to_evidence(
        artifact,
        evidence,
    )

    provenance = ProvenanceRecord(
        evidence_id=evidence.id,
        relation="validated_by",
        source_node="ENGINE",
        target_node="TEST",
    )

    graph = TruthGraph.from_json(
        ROOT / "demo/truth_graph/nodes.json",
        ROOT / "demo/truth_graph/edges.json",
    )

    resolver = TruthTraceResolver(
        graph,
        [evidence],
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

    assert binding.artifact_id == artifact.id
    assert binding.evidence_id == evidence.id

    assert provenance.evidence_id == evidence.id
    assert provenance.source_node == "ENGINE"
    assert provenance.target_node == "TEST"

    assert [
        (step.source, step.target)
        for step in trace.steps
    ] == [
        ("ENGINE", "TEST"),
        ("TEST", "EVIDENCE"),
    ]

    assert trace.steps[0].evidence_id == "E_ENGINE_TEST"
    assert trace.score == 0.94075
