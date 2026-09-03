from pathlib import Path

from openmind.evidence import EvidenceRecord
from openmind.ingestion import ingest_as_evidence


def test_ingest_as_evidence_is_deterministic(tmp_path: Path):
    artifact = tmp_path / "evidence.txt"
    artifact.write_text("OPENMIND CANONICAL EVIDENCE\n")

    first = ingest_as_evidence(
        artifact,
        claim="artifact supports canonical evidence",
        confidence=0.96,
    )

    second = ingest_as_evidence(
        artifact,
        claim="artifact supports canonical evidence",
        confidence=0.96,
    )

    assert isinstance(first, EvidenceRecord)
    assert first == second


def test_ingest_as_evidence_is_artifact_anchored(tmp_path: Path):
    artifact = tmp_path / "evidence.txt"
    artifact.write_text("OPENMIND CANONICAL EVIDENCE\n")

    evidence = ingest_as_evidence(
        artifact,
        claim="artifact supports canonical evidence",
        confidence=0.96,
    )

    assert evidence.id.startswith("evidence:")
    assert evidence.source.startswith("artifact:")
    assert evidence.claim == "artifact supports canonical evidence"
    assert evidence.confidence == 0.96


def test_content_change_changes_evidence_identity(tmp_path: Path):
    artifact = tmp_path / "evidence.txt"

    artifact.write_text("VERSION A")
    first = ingest_as_evidence(
        artifact,
        claim="artifact claim",
        confidence=0.9,
    )

    artifact.write_text("VERSION B")
    second = ingest_as_evidence(
        artifact,
        claim="artifact claim",
        confidence=0.9,
    )

    assert first.id != second.id
    assert first.source != second.source


def test_ingest_as_evidence_round_trips_through_registry(
    tmp_path: Path,
):
    from openmind.evidence import EvidenceRegistry

    artifact = tmp_path / "canonical.txt"
    artifact.write_text("OPENMIND CANONICAL ARTIFACT\n")

    evidence = ingest_as_evidence(
        artifact,
        claim="artifact supports canonical evidence",
        confidence=0.96,
    )

    registry = EvidenceRegistry([evidence])

    registry_path = tmp_path / "evidence.json"
    registry.save(registry_path)

    restored = EvidenceRegistry.load(registry_path)

    assert restored.get(evidence.id) == evidence
    assert restored.all() == registry.all()
    assert restored.to_json() == registry.to_json()
