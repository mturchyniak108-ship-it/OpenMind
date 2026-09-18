"""Experimental Knowledge Waveform encoder/decoder.

Deterministic PCM/WAV encoding of TruthPath-derived metadata.
Truth Graph remains canonical. Waveform is derived signal only.
"""

from __future__ import annotations

import struct
import wave
from io import BytesIO
from pathlib import Path
from typing import Tuple

from openmind.experimental.path_meta import ExperimentalPathMeta

SAMPLE_RATE = 8000
BITS_PER_SAMPLE = 16
MAX_AMPLITUDE = 32767
N_CHANNELS = 8


def _float_to_pcm(value: float) -> int:
    """Map [0.0, 1.0] float to signed 16-bit PCM."""
    clamped = max(0.0, min(1.0, float(value)))
    return int(clamped * MAX_AMPLITUDE)


def _pcm_to_float(sample: int) -> float:
    """Map signed 16-bit PCM back to [0.0, 1.0]."""
    return max(0.0, min(1.0, sample / MAX_AMPLITUDE))


def encode(path_meta: ExperimentalPathMeta) -> bytes:
    """Encode ExperimentalPathMeta into an 8-channel WAV byte stream.

    Each edge in the path generates one sample frame with 8 channels.
    Channel mapping (ROADMAP Milestone 10):
        0: truth confidence (source node per edge)
        1: evidence strength (edge weight)
        2: relationship weight (edge weight)
        3: semantic relevance (predictive_weight)
        4: contradiction signal (1.0 - min confidence so far)
        5: fraction of path traversed ((i + 1) / n_edges)
        6: running mean provenance (mean weight so far)
        7: retrieval history (0.0 placeholder)
    """
    n_edges = len(path_meta.weights)
    if n_edges == 0:
        buf = BytesIO()
        with wave.open(buf, "wb") as w:
            w.setnchannels(N_CHANNELS)
            w.setsampwidth(BITS_PER_SAMPLE // 8)
            w.setframerate(SAMPLE_RATE)
            w.setnframes(0)
        return buf.getvalue()

    buf = BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(N_CHANNELS)
        w.setsampwidth(BITS_PER_SAMPLE // 8)
        w.setframerate(SAMPLE_RATE)
        w.setnframes(n_edges)

        frames: list[int] = []
        min_conf_so_far = 1.0
        cum_weight = 0.0

        for i in range(n_edges):
            ch0 = path_meta.truth_confidences[i]
            ch1 = path_meta.weights[i]
            ch2 = path_meta.weights[i]
            ch3 = path_meta.predictive_weight
            min_conf_so_far = min(min_conf_so_far, path_meta.truth_confidences[i])
            ch4 = 1.0 - min_conf_so_far
            ch5 = (i + 1) / n_edges
            cum_weight += path_meta.weights[i]
            ch6 = cum_weight / (i + 1)
            ch7 = 0.0

            for ch in (ch0, ch1, ch2, ch3, ch4, ch5, ch6, ch7):
                frames.append(_float_to_pcm(ch))

        w.writeframes(struct.pack(f"<{len(frames)}h", *frames))

    return buf.getvalue()


def decode(wav_bytes: bytes) -> Tuple[Tuple[float, ...], ...]:
    """Decode 8-channel WAV bytes into a tuple of 8 channel tuples.

    Returns one tuple per channel, each containing float samples [0.0, 1.0].
    """
    buf = BytesIO(wav_bytes)
    with wave.open(buf, "rb") as w:
        nchannels = w.getnchannels()
        nframes = w.getnframes()

        if nchannels != N_CHANNELS:
            raise ValueError(f"Expected {N_CHANNELS} channels, got {nchannels}")

        raw = w.readframes(nframes)
        fmt = f"<{nframes * nchannels}h"
        samples = struct.unpack(fmt, raw)

    channels: list[list[float]] = [[] for _ in range(N_CHANNELS)]
    for i, sample in enumerate(samples):
        ch_idx = i % N_CHANNELS
        channels[ch_idx].append(_pcm_to_float(sample))

    return tuple(tuple(ch) for ch in channels)


def encode_to_file(path_meta: ExperimentalPathMeta, filepath: str | Path) -> None:
    """Write encoded waveform to a WAV file."""
    Path(filepath).write_bytes(encode(path_meta))


def decode_from_file(filepath: str | Path) -> Tuple[Tuple[float, ...], ...]:
    """Read WAV file and decode to channel tuples."""
    return decode(Path(filepath).read_bytes())
