"""Tests for experimental Knowledge Waveform encoder/decoder."""

from openmind.experimental.path_meta import ExperimentalPathMeta, from_truth_path
from openmind.experimental.waveform import decode, encode
from openmind.truth_graph import TruthEdge, TruthGraph, TruthNode


def _simple_graph() -> TruthGraph:
    nodes = {
        "A": TruthNode(id="A", tag="a", type="concept", truth_confidence=0.9),
        "B": TruthNode(id="B", tag="b", type="concept", truth_confidence=0.8),
        "C": TruthNode(id="C", tag="c", type="concept", truth_confidence=1.0),
    }
    edges = [
        TruthEdge(source="A", target="B", tag="rel", relation="supports", weight=0.7),
        TruthEdge(source="B", target="C", tag="rel", relation="supports", weight=0.6),
    ]
    return TruthGraph(nodes, edges)


def test_waveform_roundtrip_is_lossless():
    """Verify encode → decode preserves derived channel values."""
    graph = _simple_graph()
    path = graph.best_path("A", "C")
    assert path is not None

    meta = from_truth_path(path, graph, predictive_weight=0.3)
    wav_bytes = encode(meta)
    channels = decode(wav_bytes)

    assert len(channels) == 8
    assert all(len(ch) == 2 for ch in channels)

    assert abs(channels[0][0] - 0.9) < 0.01
    assert abs(channels[0][1] - 0.8) < 0.01
    assert abs(channels[1][0] - 0.7) < 0.01
    assert abs(channels[1][1] - 0.6) < 0.01
    assert abs(channels[2][0] - 0.7) < 0.01
    assert abs(channels[2][1] - 0.6) < 0.01
    assert abs(channels[3][0] - 0.3) < 0.01
    assert abs(channels[3][1] - 0.3) < 0.01
    assert abs(channels[4][0] - 0.1) < 0.01
    assert abs(channels[4][1] - 0.2) < 0.01
    assert abs(channels[5][0] - 0.5) < 0.01   # 1/2 traversed
    assert abs(channels[5][1] - 1.0) < 0.01   # 2/2 traversed
    assert abs(channels[6][0] - 0.7) < 0.01
    assert abs(channels[6][1] - 0.65) < 0.01
    assert channels[7][0] == 0.0
    assert channels[7][1] == 0.0


def test_waveform_file_roundtrip(tmp_path):
    """Verify encode_to_file → decode_from_file round-trip."""
    graph = _simple_graph()
    path = graph.best_path("A", "C")
    assert path is not None

    meta = from_truth_path(path, graph)
    wav_path = tmp_path / "test.wav"

    from openmind.experimental.waveform import decode_from_file, encode_to_file
    encode_to_file(meta, wav_path)
    channels = decode_from_file(wav_path)

    assert len(channels) == 8
    assert all(len(ch) == 2 for ch in channels)
