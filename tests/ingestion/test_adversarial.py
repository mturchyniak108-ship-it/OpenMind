import pytest

from openmind.evidence import evidence_from_artifact
from openmind.ingestion import collect_artifact, ingest_as_evidence


def test_collect_directory_is_rejected(tmp_path):
    directory = tmp_path / "artifact"
    directory.mkdir()

    with pytest.raises(FileNotFoundError):
        collect_artifact(directory)


def test_collect_missing_path_is_rejected(tmp_path):
    with pytest.raises(FileNotFoundError):
        collect_artifact(tmp_path / "missing.bin")


def test_empty_artifact_has_stable_identity(tmp_path):
    artifact_path = tmp_path / "empty.bin"
    artifact_path.write_bytes(b"")

    first = collect_artifact(artifact_path)
    second = collect_artifact(artifact_path)

    assert first == second
    assert first.size == 0
    assert len(first.sha256) == 64
    assert first.id == f"artifact:{first.sha256}"


def test_source_is_preserved(tmp_path):
    artifact_path = tmp_path / "source.txt"
    artifact_path.write_text("canonical")

    artifact = collect_artifact(
        artifact_path,
        source="test-source",
    )

    assert artifact.source == "test-source"


def test_evidence_identity_depends_on_artifact_not_claim(tmp_path):
    artifact_path = tmp_path / "evidence.txt"
    artifact_path.write_text("same artifact")

    artifact = collect_artifact(artifact_path)

    first = evidence_from_artifact(
        artifact,
        claim="claim A",
        confidence=0.5,
    )
    second = evidence_from_artifact(
        artifact,
        claim="claim B",
        confidence=1.0,
    )

    assert first.id == second.id
    assert first.source == second.source
    assert first.claim != second.claim
    assert first.confidence != second.confidence


def test_evidence_confidence_boundaries_are_valid(tmp_path):
    artifact_path = tmp_path / "evidence.txt"
    artifact_path.write_text("evidence")

    artifact = collect_artifact(artifact_path)

    low = evidence_from_artifact(
        artifact,
        claim="low confidence",
        confidence=0.0,
    )
    high = evidence_from_artifact(
        artifact,
        claim="high confidence",
        confidence=1.0,
    )

    assert low.confidence == 0.0
    assert high.confidence == 1.0


@pytest.mark.parametrize(
    "confidence",
    [-0.001, 1.001],
)
def test_evidence_confidence_out_of_range_is_rejected(
    tmp_path,
    confidence,
):
    artifact_path = tmp_path / "evidence.txt"
    artifact_path.write_text("evidence")

    artifact = collect_artifact(artifact_path)

    with pytest.raises(ValueError):
        evidence_from_artifact(
            artifact,
            claim="invalid confidence",
            confidence=confidence,
        )


def test_ingest_as_evidence_preserves_source(tmp_path):
    artifact_path = tmp_path / "source.txt"
    artifact_path.write_text("canonical")

    evidence = ingest_as_evidence(
        artifact_path,
        claim="canonical claim",
        confidence=0.8,
        source="external-source",
    )

    assert evidence.source.startswith("artifact:")


def test_ingestion_does_not_modify_artifact(tmp_path):
    artifact_path = tmp_path / "immutable.txt"
    original = b"OPENMIND ARTIFACT"
    artifact_path.write_bytes(original)

    collect_artifact(artifact_path)

    assert artifact_path.read_bytes() == original


def test_ingestion_rejects_empty_claim(tmp_path):
    artifact_path = tmp_path / "evidence.txt"
    artifact_path.write_text("evidence")

    with pytest.raises(ValueError):
        ingest_as_evidence(
            artifact_path,
            claim="",
            confidence=0.9,
        )
