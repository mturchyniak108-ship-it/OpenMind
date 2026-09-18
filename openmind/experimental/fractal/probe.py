"""Fractal memory probe.

Retrieves candidate convergence points from a FractalPath.
Truth Graph remains canonical. Probe is derived signal only.
"""

from __future__ import annotations

from .encoder import FractalPath, HelixPoint


def central_convergence(fractal: FractalPath) -> HelixPoint | None:
    """Return the highest-weight convergence point.

    This is the 'central candidate' per Milestone 11 —
    the point of greatest validated relational convergence.
    """
    if not fractal.convergence_points:
        return None
    return fractal.convergence_points[0]


def probe_by_weight_threshold(
    fractal: FractalPath,
    min_weight: float = 0.5,
) -> tuple[HelixPoint, ...]:
    """Return convergence points above a weight threshold."""
    return tuple(
        p for p in fractal.convergence_points
        if p.convergence_weight >= min_weight
    )
