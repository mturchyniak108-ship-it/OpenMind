from pathlib import Path

from openmind.evidence import evidence_from_artifact
from openmind.ingestion import collect_artifact


def test_artifact_evidence_binding_is_deterministic(tmp_path: Path):
    artifact_path = tmp_path / "evidence.txt"
    artifact_path.write_text("ENGINE produces TEST\n")

    artifact = collect_artifact(artifact_path)

    first = evidence_from_artifact(
        artifact,
        "ENGINE produces TEST",
        0.96,
    )
    second = evidence_from_artifact(
        artifact,
        "ENGINE produces TEST",
        0.96,
    )

    assert first == second
    assert first.id == f"evidence:{artifact.sha256}"
    assert first.source == artifact.id
    assert first.claim == "ENGINE produces TEST"
    assert first.confidence == 0.96


def test_artifact_content_changes_evidence_identity(tmp_path: Path):
    artifact_path = tmp_path / "evidence.txt"

    artifact_path.write_text("A")
    first_artifact = collect_artifact(artifact_path)
    first = evidence_from_artifact(first_artifact, "claim", 0.9)

    artifact_path.write_text("B")
    second_artifact = collect_artifact(artifact_path)
    second = evidence_from_artifact(second_artifact, "claim", 0.9)

    assert first.id != second.id
    assert first.source != second.source


def test_invalid_evidence_is_rejected(tmp_path: Path):
    artifact_path = tmp_path / "evidence.txt"
    artifact_path.write_text("A")

    artifact = collect_artifact(artifact_path)

    try:
        evidence_from_artifact(artifact, "", 0.9)
    except ValueError:
        pass
    else:
        raise AssertionError("empty claim was accepted")

    try:
        evidence_from_artifact(artifact, "claim", 1.1)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid confidence was accepted")
