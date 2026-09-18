"""Filesystem ingestion compatibility API."""

from __future__ import annotations

from pathlib import Path

from .collector import ArtifactRecord, collect_artifact


def ingest_file(path: str | Path) -> ArtifactRecord:
    """Ingest one local artifact using the canonical collector."""

    return collect_artifact(path)


__all__ = [
    "ArtifactRecord",
    "ingest_file",
]
