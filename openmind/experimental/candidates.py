"""Experimental candidate boundary.

This module represents derived experimental signals without redefining
or modifying canonical Truth Graph semantics.
"""

from __future__ import annotations

from dataclasses import dataclass

from openmind.truth_graph import TruthPath

from .fuzzy_graph import PredictivePath


@dataclass(frozen=True)
class ExperimentalCandidate:
    """Immutable experimental interpretation of a canonical TruthPath."""

    path: TruthPath
    relationship_score: float
    fuzzy_score: float
    predictive_score: float
    canonical_score: float
    status: str = "CANDIDATE"

    @classmethod
    def from_predictive_path(
        cls,
        predictive: PredictivePath,
    ) -> "ExperimentalCandidate":
        """Create a non-canonical candidate from an experimental result."""

        return cls(
            path=predictive.path,
            relationship_score=predictive.relationship_score,
            fuzzy_score=predictive.fuzzy_score,
            predictive_score=predictive.predictive_score,
            canonical_score=predictive.path.score,
        )
