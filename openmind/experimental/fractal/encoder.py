"""Experimental Fractal Memory encoder.

Deterministic double-helix geometric representation of TruthPath metadata.
Truth Graph remains canonical. Fractal is derived signal only.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Tuple

from openmind.experimental.path_meta import ExperimentalPathMeta


@dataclass(frozen=True)
class HelixPoint:
    """A single point in 3D fractal space."""
    x: float
    y: float
    z: float
    strand: str
    edge_index: int
    convergence_weight: float


@dataclass(frozen=True)
class FractalPath:
    """Deterministic fractal representation of a TruthPath."""
    path_id: str
    strand_a: Tuple[HelixPoint, ...]
    strand_b: Tuple[HelixPoint, ...]
    convergence_points: Tuple[HelixPoint, ...]


def encode(path_meta: ExperimentalPathMeta) -> FractalPath:
    """Encode ExperimentalPathMeta as a deterministic double-helix fractal.

    Double-helix geometry (Milestone 11):
        - Axis z progresses from 0 to 1 along the path
        - Two strands offset by π (opposite sides of helix)
        - Radius at each step = relationship weight
        - Pitch scales with path_cost
    """
    n_edges = len(path_meta.weights)
    if n_edges == 0:
        return FractalPath(
            path_id=path_meta.path_id,
            strand_a=(),
            strand_b=(),
            convergence_points=(),
        )

    turns = n_edges
    pitch = 1.0 / max(turns, 1)

    strand_a: List[HelixPoint] = []
    strand_b: List[HelixPoint] = []
    convergence: List[HelixPoint] = []

    for i in range(n_edges):
        t = 2.0 * math.pi * i / max(n_edges, 1)
        z = i * pitch
        radius = path_meta.weights[i]

        x_a = radius * math.cos(t)
        y_a = radius * math.sin(t)
        strand_a.append(HelixPoint(
            x=round(x_a, 12),
            y=round(y_a, 12),
            z=round(z, 12),
            strand="A",
            edge_index=i,
            convergence_weight=path_meta.weights[i],
        ))

        x_b = radius * math.cos(t + math.pi)
        y_b = radius * math.sin(t + math.pi)
        strand_b.append(HelixPoint(
            x=round(x_b, 12),
            y=round(y_b, 12),
            z=round(z, 12),
            strand="B",
            edge_index=i,
            convergence_weight=path_meta.weights[i],
        ))

        convergence.append(HelixPoint(
            x=round((x_a + x_b) / 2.0, 12),
            y=round((y_a + y_b) / 2.0, 12),
            z=round(z, 12),
            strand="convergence",
            edge_index=i,
            convergence_weight=path_meta.weights[i],
        ))

    sorted_convergence = tuple(sorted(
        convergence,
        key=lambda p: (-p.convergence_weight, p.edge_index),
    ))

    return FractalPath(
        path_id=path_meta.path_id,
        strand_a=tuple(strand_a),
        strand_b=tuple(strand_b),
        convergence_points=sorted_convergence,
    )
