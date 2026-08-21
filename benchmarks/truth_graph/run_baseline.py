from __future__ import annotations

import time
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from openmind.truth_graph import TruthGraph


ROOT = Path(__file__).resolve().parents[2]

CASES = [
    ("PROJECT", "EVIDENCE"),
    ("PROJECT", "TRUTH"),
    ("ENGINE", "EVIDENCE"),
    ("PATH", "TRUTH"),
    ("TRUTH", "VECTOR"),
]


def main() -> None:
    graph = TruthGraph.from_json(
        ROOT / "demo/truth_graph/nodes.json",
        ROOT / "demo/truth_graph/edges.json",
    )

    print("===== OPENMIND TRUTH GRAPH BASELINE =====")

    for start, end in CASES:
        begin = time.perf_counter()
        paths = graph.find_paths(start, end)
        elapsed = time.perf_counter() - begin

        best = paths[0] if paths else None

        print()
        print(f"{start} -> {end}")
        print(f"candidates: {len(paths)}")
        print(f"latency_ms: {elapsed * 1000:.6f}")

        if best is None:
            print("path: NONE")
            continue

        print(f"path: {' -> '.join(best.nodes)}")
        print(f"path_length: {len(best.edges)}")
        print(f"score: {best.score:.12f}")


if __name__ == "__main__":
    main()
