from __future__ import annotations

import json
import time
from pathlib import Path

from openmind.experimental.fuzzy_graph import PredictivePathScorer
from openmind.truth_graph import TruthGraph


ROOT = Path(__file__).resolve().parents[2]
BASELINE = ROOT / "benchmarks/truth_graph/results/baseline.json"

CASES = json.loads(BASELINE.read_text())["cases"]


def main() -> None:
    graph = TruthGraph.from_json(
        ROOT / "demo/truth_graph/nodes.json",
        ROOT / "demo/truth_graph/edges.json",
    )

    scorer = PredictivePathScorer(graph)

    print("===== OPENMIND CANONICAL vs PREDICTIVE =====")

    results = []

    for case in CASES:
        start = case["start"]
        end = case["end"]

        begin = time.perf_counter()
        canonical = graph.best_path(start, end)
        canonical_ms = (time.perf_counter() - begin) * 1000

        begin = time.perf_counter()
        predictive = scorer.best_path(start, end)
        predictive_ms = (time.perf_counter() - begin) * 1000

        if canonical is None or predictive is None:
            raise RuntimeError(f"No path for {start} -> {end}")

        agreement = canonical.nodes == predictive.path.nodes

        print()
        print(f"{start} -> {end}")
        print(f"canonical:  {' -> '.join(canonical.nodes)}")
        print(f"predictive: {' -> '.join(predictive.path.nodes)}")
        print(f"agreement: {agreement}")
        print(f"canonical_score:  {canonical.score:.12f}")
        print(f"predictive_score: {predictive.predictive_score:.12f}")
        print(f"fuzzy_score:      {predictive.fuzzy_score:.12f}")
        print(f"canonical_ms: {canonical_ms:.6f}")
        print(f"predictive_ms: {predictive_ms:.6f}")

        results.append({
            "start": start,
            "end": end,
            "agreement": agreement,
            "canonical_path": list(canonical.nodes),
            "predictive_path": list(predictive.path.nodes),
            "canonical_score": canonical.score,
            "predictive_score": predictive.predictive_score,
            "fuzzy_score": predictive.fuzzy_score,
            "canonical_latency_ms": canonical_ms,
            "predictive_latency_ms": predictive_ms,
        })

    agreement_count = sum(r["agreement"] for r in results)

    print()
    print("===== SUMMARY =====")
    print(f"cases: {len(results)}")
    print(f"path_agreement: {agreement_count}/{len(results)}")
    print(
        f"agreement_rate: "
        f"{agreement_count / len(results):.6f}"
    )


if __name__ == "__main__":
    main()
