"""Canonical artifact-to-evidence binding."""

from __future__ import annotations

from dataclasses import dataclass

from openmind.ingestion import ArtifactRecord
from openmind.evidence import EvidenceRecord


@dataclass(frozen=True)
class ArtifactEvidenceBinding:
    """Immutable binding between an artifact and canonical evidence."""

    artifact_id: str
    evidence_id: str
    claim: str


def bind_artifact_to_evidence(
    artifact: ArtifactRecord,
    evidence: EvidenceRecord,
) -> ArtifactEvidenceBinding:
    """Bind an ingested artifact to an evidence record.

    Binding establishes provenance identity only.
    It does not increase or alter evidence confidence.
    """

    return ArtifactEvidenceBinding(
        artifact_id=artifact.id,
        evidence_id=evidence.id,
        claim=evidence.claim,
    )
