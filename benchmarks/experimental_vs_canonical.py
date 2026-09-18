"""Benchmark: Canonical Truth Graph vs Experimental layers.

Measures latency and storage for canonical operations against
waveform, fractal, and fuzzy graph experimental encodings.

Addresses TODO.md:
- Compare WAV storage with graph/vector storage
- Benchmark waveform generation latency
- Benchmark fractal memory generation latency
"""

from __future__ import annotations

import json
import statistics
import time
from typing import Callable

from openmind.experimental.fractal import encode_color, encode_fractal
from openmind.experimental.fuzzy_graph.scorer import PredictivePathScorer
from openmind.experimental.path_meta import from_truth_path
from openmind.experimental.waveform import decode, encode
from openmind.truth_graph import TruthEdge, TruthGraph, TruthNode


def _sample_graph() -> TruthGraph:
    nodes = {
        "A": TruthNode(id="A", tag="a", type="concept", truth_confidence=0.9),
        "B": TruthNode(id="B", tag="b", type="concept", truth_confidence=0.8),
        "C": TruthNode(id="C", tag="c", type="concept", truth_confidence=1.0),
        "D": TruthNode(id="D", tag="d", type="concept", truth_confidence=0.95),
    }
    edges = [
        TruthEdge(source="A", target="B", tag="rel", relation="supports", weight=0.7),
        TruthEdge(source="B", target="C", tag="rel", relation="supports", weight=0.6),
        TruthEdge(source="C", target="D", tag="rel", relation="supports", weight=0.85),
    ]
    return TruthGraph(nodes, edges)


def _bench(fn: Callable[[], object], iterations: int = 1000) -> tuple[float, object]:
    times: list[float] = []
    result = None
    for _ in range(iterations):
        t0 = time.perf_counter()
        result = fn()
        times.append((time.perf_counter() - t0) * 1000.0)
    return statistics.median(times), result


def main() -> None:
    graph = _sample_graph()
    path = graph.best_path("A", "D")
    assert path is not None
    meta = from_truth_path(path, graph, predictive_weight=0.75)

    wav_bytes = encode(meta)
    fractal = encode_fractal(meta)
    scorer = PredictivePathScorer(graph)

    # Canonical
    canonical_json = json.dumps(graph.to_dict(), indent=2, sort_keys=True)
    canonical_bytes = canonical_json.encode("utf-8")
    t_path, _ = _bench(lambda: graph.best_path("A", "D"))
    t_ser, _ = _bench(lambda: json.dumps(graph.to_dict(), indent=2, sort_keys=True))

    # Waveform
    t_wav_enc, _ = _bench(lambda: encode(meta))
    t_wav_dec, _ = _bench(lambda: decode(wav_bytes))

    # Fractal
    t_frac_enc, _ = _bench(lambda: encode_fractal(meta))
    t_frac_col, _ = _bench(lambda: encode_color(fractal))

    # Fuzzy
    t_fuzzy, _ = _bench(lambda: scorer.score(path))

    # Storage
    fractal_str = json.dumps({
        "path_id": fractal.path_id,
        "strand_a": [(p.x, p.y, p.z, p.strand, p.edge_index, p.convergence_weight) for p in fractal.strand_a],
        "strand_b": [(p.x, p.y, p.z, p.strand, p.edge_index, p.convergence_weight) for p in fractal.strand_b],
        "convergence": [(p.x, p.y, p.z, p.strand, p.edge_index, p.convergence_weight) for p in fractal.convergence_points],
    }, indent=2)
    fractal_bytes = fractal_str.encode("utf-8")

    colors = encode_color(fractal)
    color_str = json.dumps([{"r": c.r, "g": c.g, "b": c.b, "w": c.convergence_weight} for c in colors])
    color_bytes = color_str.encode("utf-8")

    # Integrity
    channels = decode(wav_bytes)
    roundtrip_ok = (
        len(channels) == 8
        and all(len(ch) == 3 for ch in channels)
        and abs(channels[0][0] - 0.9) < 0.01
    )

    # Report
    print("=" * 65)
    print("  CANONICAL vs EXPERIMENTAL BENCHMARK")
    print("=" * 65)
    print(f"\n  Graph: 4 nodes, 3 edges, path A -> D")
    print(f"  Iterations per benchmark: 1000 (median reported)")
    print()
    print(f"  {'Operation':<30} {'Latency (ms)':>14} {'Storage (B)':>14}")
    print(f"  {'-'*30} {'-'*14} {'-'*14}")
    print(f"  {'Canonical pathfinding':<30} {t_path:>14.6f} {'-':>14}")
    print(f"  {'Canonical JSON serialize':<30} {t_ser:>14.6f} {len(canonical_bytes):>14}")
    print(f"  {'Waveform encode':<30} {t_wav_enc:>14.6f} {len(wav_bytes):>14}")
    print(f"  {'Waveform decode':<30} {t_wav_dec:>14.6f} {'-':>14}")
    print(f"  {'Fractal encode':<30} {t_frac_enc:>14.6f} {len(fractal_bytes):>14}")
    print(f"  {'Fractal color encode':<30} {t_frac_col:>14.6f} {len(color_bytes):>14}")
    print(f"  {'Fuzzy graph score':<30} {t_fuzzy:>14.6f} {'-':>14}")
    print()
    print("  --- Storage ratios (vs Canonical JSON) ---")
    print(f"    WAV:       {len(wav_bytes)/max(len(canonical_bytes),1):.4f}x")
    print(f"    Fractal:   {len(fractal_bytes)/max(len(canonical_bytes),1):.4f}x")
    print(f"    Color:     {len(color_bytes)/max(len(canonical_bytes),1):.4f}x")
    print()
    print(f"  --- Integrity ---")
    print(f"    Waveform round-trip: {'PASS' if roundtrip_ok else 'FAIL'}")
    print()
    print("=" * 65)


if __name__ == "__main__":
    main()
