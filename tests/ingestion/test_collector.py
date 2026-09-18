from pathlib import Path

from openmind.ingestion import ArtifactRecord, collect_artifact


def test_collect_artifact_is_deterministic(tmp_path: Path):
    artifact = tmp_path / "sample.txt"
    artifact.write_text("OPENMIND CANONICAL ARTIFACT\n")

    first = collect_artifact(artifact)
    second = collect_artifact(artifact)

    assert isinstance(first, ArtifactRecord)
    assert first == second
    assert first.source == "local"
    assert first.path == str(artifact)
    assert first.size == len(artifact.read_bytes())
    assert len(first.sha256) == 64
    assert first.id == f"artifact:{first.sha256}"


def test_collect_artifact_changes_when_content_changes(tmp_path: Path):
    artifact = tmp_path / "sample.txt"

    artifact.write_text("A")
    first = collect_artifact(artifact)

    artifact.write_text("B")
    second = collect_artifact(artifact)

    assert first.sha256 != second.sha256
    assert first.id != second.id


def test_collect_artifact_rejects_missing_file(tmp_path: Path):
    missing = tmp_path / "missing.txt"

    try:
        collect_artifact(missing)
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("missing artifact was accepted")
