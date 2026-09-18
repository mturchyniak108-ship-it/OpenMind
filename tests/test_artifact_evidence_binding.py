from pathlib import Path

from openmind.ingestion import collect_artifact
from openmind.evidence import (
    EvidenceRecord,
    ArtifactEvidenceBinding,
    bind_artifact_to_evidence,
)


def test_artifact_evidence_binding_is_deterministic(tmp_path: Path):
    artifact_path = tmp_path / "claim.txt"
    artifact_path.write_text("ENGINE produces TEST")

    artifact = collect_artifact(artifact_path)

    evidence = EvidenceRecord(
        id="E_ENGINE_TEST",
        source=artifact.id,
        claim="ENGINE produces TEST",
        confidence=0.96,
    )

    first = bind_artifact_to_evidence(artifact, evidence)
    second = bind_artifact_to_evidence(artifact, evidence)

    assert isinstance(first, ArtifactEvidenceBinding)
    assert first == second
    assert first.artifact_id == artifact.id
    assert first.evidence_id == evidence.id
    assert first.claim == evidence.claim


def test_binding_does_not_modify_evidence_confidence(tmp_path: Path):
    artifact_path = tmp_path / "claim.txt"
    artifact_path.write_text("TEST produces EVIDENCE")

    artifact = collect_artifact(artifact_path)

    evidence = EvidenceRecord(
        id="E_TEST_EVIDENCE",
        source=artifact.id,
        claim="TEST produces EVIDENCE",
        confidence=0.96,
    )

    binding = bind_artifact_to_evidence(artifact, evidence)

    assert binding.evidence_id == evidence.id
    assert evidence.confidence == 0.96
