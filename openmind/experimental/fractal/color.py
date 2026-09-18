"""Deterministic color encoding for fractal convergence points.

Maps each convergence point to an RGB value derived from its
geometric position and relational weight.
Truth Graph remains canonical. Color is derived signal only.
"""

from __future__ import annotations

import colorsys
from dataclasses import dataclass
from typing import Tuple

from .encoder import FractalPath


@dataclass(frozen=True)
class ConvergenceColor:
    """Deterministic RGB + metadata for a convergence point."""
    r: int   # 0-255
    g: int   # 0-255
    b: int   # 0-255
    convergence_weight: float
    edge_index: int


def encode(fractal: FractalPath) -> Tuple[ConvergenceColor, ...]:
    """Map convergence points to deterministic RGB colors.

    HSV mapping (Milestone 11):
        H = z position along path [0.0, 1.0] -> hue rotation
        S = convergence_weight [0.0, 1.0] -> saturation
        V = 0.7 + 0.3 * convergence_weight -> brightness bias
    """
    if not fractal.convergence_points:
        return ()

    max_z = max(p.z for p in fractal.convergence_points)

    colors: list[ConvergenceColor] = []
    for point in fractal.convergence_points:
        hue = point.z / max_z if max_z > 0 else 0.0
        saturation = point.convergence_weight
        value = 0.7 + 0.3 * point.convergence_weight

        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)

        colors.append(ConvergenceColor(
            r=int(r * 255),
            g=int(g * 255),
            b=int(b * 255),
            convergence_weight=point.convergence_weight,
            edge_index=point.edge_index,
        ))

    return tuple(colors)
