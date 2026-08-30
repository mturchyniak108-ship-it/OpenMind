"""Experimental fuzzy/vector graph models.

This module must never redefine canonical truth.
It derives experimental representations from the canonical Truth Graph.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WeightedVector:
    node_id: str
    values: tuple[float, ...]
    magnitude: float
    predictive_weight: float


@dataclass(frozen=True)
class FuzzyRelationship:
    source: str
    target: str
    membership: float
    predictive_weight: float
