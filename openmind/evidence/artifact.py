"""Canonical artifact-to-evidence binding."""

from __future__ import annotations

from openmind.ingestion import ArtifactRecord
from .models import EvidenceRecord


def evidence_from_artifact(
    artifact: ArtifactRecord,
    claim: str,
    confidence: float,
) -> EvidenceRecord:
    """Create immutable evidence anchored to an artifact identity."""

    if not claim:
        raise ValueError("claim must not be empty")

    if not 0.0 <= confidence <= 1.0:
        raise ValueError("confidence must be between 0.0 and 1.0")

    return EvidenceRecord(
        id=f"evidence:{artifact.sha256}",
        source=artifact.id,
        claim=claim,
        confidence=float(confidence),
    )
