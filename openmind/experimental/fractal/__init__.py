"""Experimental Fractal Memory layer.

Derived signal only. Truth Graph remains canonical.
"""

from .encoder import FractalPath, HelixPoint, encode

__all__ = [
    "encode",
    "FractalPath",
    "HelixPoint",
]
