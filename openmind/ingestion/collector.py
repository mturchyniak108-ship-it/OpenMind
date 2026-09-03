"""Deterministic canonical artifact ingestion."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import hashlib


@dataclass(frozen=True)
class ArtifactRecord:
    """Immutable representation of an ingested artifact."""

    id: str
    source: str
    path: str
    sha256: str
    size: int


def collect_artifact(path: str | Path, source: str = "local") -> ArtifactRecord:
    """Collect deterministic identity metadata for an artifact.

    Ingestion records what exists.
    It does not decide whether the artifact is true.
    """

    artifact_path = Path(path)

    if not artifact_path.is_file():
        raise FileNotFoundError(artifact_path)

    data = artifact_path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()

    return ArtifactRecord(
        id=f"artifact:{digest}",
        source=source,
        path=str(artifact_path),
        sha256=digest,
        size=len(data),
    )
