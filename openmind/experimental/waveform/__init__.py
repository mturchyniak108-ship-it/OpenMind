"""Experimental Knowledge Waveform layer.

Derived signal only. Truth Graph remains canonical.
"""

from .encoder import decode, decode_from_file, encode, encode_to_file

__all__ = [
    "encode",
    "decode",
    "encode_to_file",
    "decode_from_file",
]
