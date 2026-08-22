"""Experimental Fractal Memory layer.

Derived signal only. Truth Graph remains canonical.
"""

from .color import ConvergenceColor, encode as encode_color
from .encoder import FractalPath, HelixPoint, encode as encode_fractal
from .probe import central_convergence, probe_by_weight_threshold

# Backward compatibility: old tests import 'encode'
encode = encode_fractal

__all__ = [
    "encode",
    "encode_fractal",
    "encode_color",
    "central_convergence",
    "probe_by_weight_threshold",
    "FractalPath",
    "HelixPoint",
    "ConvergenceColor",
]
