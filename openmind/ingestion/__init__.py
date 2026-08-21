"""Canonical artifact ingestion layer."""

from .collector import ArtifactRecord, collect_artifact
from .filesystem import ingest_file

__all__ = [
    "ArtifactRecord",
    "collect_artifact",
    "ingest_file",
]

from .pipeline import ingest_as_evidence

__all__.append("ingest_as_evidence")
