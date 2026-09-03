"""Demonstration and benchmark for Knowledge Waveform encoding.

Generates a sample TruthPath, encodes it to WAV, and compares storage
against canonical JSON representation.

Addresses TODO.md:
- Generate demonstration knowledge waveforms
- Compare WAV storage with graph/vector storage
- Benchmark waveform generation latency
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from openmind.experimental.path_meta import from_truth_path
from openmind.experimental.waveform import encode, decode, encode_to_file
from openmind.truth_graph import TruthEdge, TruthGraph, TruthNode


def _sample_graph() -> TruthGraph:
    """Build a sample truth graph for demonstration."""
    nodes = {
        "sun": TruthNode(id="sun", tag="star", type="astro", truth_confidence=0.95),
        "earth": TruthNode(id="earth", tag="planet", type="astro", truth_confidence=0.99),
        "moon": TruthNode(id="moon", tag="satellite", type="astro", truth_confidence=0.97),
        "tide": TruthNode(id="tide", tag="phenomenon", type="geo", truth_confidence=0.88),
    }
    edges = [
        TruthEdge(source="sun", target="earth", tag="gravity", relation="binds", weight=0.9),
        TruthEdge(source="earth", target="moon", tag="gravity", relation="binds", weight=0.85),
        TruthEdge(source="moon", target="tide", tag="causes", relation="induces", weight=0.8),
    ]
    return TruthGraph(nodes, edges)


def main() -> None:
    graph = _sample_graph()
    path = graph.best_path("sun", "tide")
    if path is None:
        raise RuntimeError("No path found")

    meta = from_truth_path(path, graph, predictive_weight=0.75)

    # Canonical JSON size
    canonical_json = json.dumps(graph.to_dict(), indent=2, sort_keys=True)
    json_bytes = canonical_json.encode("utf-8")

    # Waveform generation benchmark
    t0 = time.perf_counter()
    wav_bytes = encode(meta)
    gen_ms = (time.perf_counter() - t0) * 1000.0

    # Decode benchmark
    t0 = time.perf_counter()
    channels = decode(wav_bytes)
    decode_ms = (time.perf_counter() - t0) * 1000.0

    # Write demo file
    out_path = Path("demo/output_waveform.wav")
    out_path.parent.mkdir(exist_ok=True)
    encode_to_file(meta, out_path)

    # Report
    print("=" * 50)
    print(" KNOWLEDGE WAVEFORM DEMONSTRATION")
    print("=" * 50)
    print(f"Path: {' -> '.join(meta.nodes)}")
    print(f"Edges: {len(meta.weights)}")
    print(f"Predictive weight: {meta.predictive_weight}")
    print()
    print("--- Storage Comparison ---")
    print(f"Canonical JSON:     {len(json_bytes):>6} bytes")
    print(f"WAV (8ch, 16bit):   {len(wav_bytes):>6} bytes")
    print(f"Ratio WAV/JSON:     {len(wav_bytes)/max(len(json_bytes),1):.3f}")
    print()
    print("--- Latency ---")
    print(f"Encode: {gen_ms:.3f} ms")
    print(f"Decode: {decode_ms:.3f} ms")
    print()
    print("--- Channel Summary ---")
    labels = [
        "truth_confidence", "evidence_strength", "relationship_weight",
        "semantic_relevance", "contradiction", "path_progress",
        "provenance_mean", "retrieval_history",
    ]
    for i, label in enumerate(labels):
        vals = channels[i]
        print(f"  Ch{i} {label:20s}: {vals}")
    print()
    print(f"Demo file written: {out_path.resolve()}")
    print("=" * 50)


if __name__ == "__main__":
    main()
