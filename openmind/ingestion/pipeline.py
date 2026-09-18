"""Canonical artifact-to-evidence ingestion pipeline."""

from __future__ import annotations

from .collector import collect_artifact


def ingest_as_evidence(
    path: str,
    claim: str,
    confidence: float,
    source: str = "local",
):
    """Collect an artifact and create evidence anchored to its identity.

    Imports the evidence layer lazily so the canonical ingestion and
    evidence packages remain acyclic at module import time.
    """

    from openmind.evidence import evidence_from_artifact

    artifact = collect_artifact(path, source=source)

    return evidence_from_artifact(
        artifact,
        claim=claim,
        confidence=confidence,
    )
