from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json

from openmind.experimental.fuzzy_graph import PredictivePathScorer
from openmind.truth_graph import TruthGraph, TruthNode, TruthEdge


@dataclass(frozen=True)
class AdversarialCase:
    name: str
    start: str
    end: str


def load_graph() -> TruthGraph:
    root = Path(__file__).resolve().parents[2]

    return TruthGraph.from_json(
        root / "demo/truth_graph/nodes.json",
        root / "demo/truth_graph/edges.json",
    )


def build_adversarial_graph() -> TruthGraph:
    base = load_graph()

    nodes = dict(base.nodes)
    edges = list(base.edges)

    nodes["ALT_A"] = TruthNode(
        id="ALT_A",
        tag="ALTERNATIVE_A",
        type="experimental_fixture",
        truth_confidence=0.97,
    )

    nodes["ALT_B"] = TruthNode(
        id="ALT_B",
        tag="ALTERNATIVE_B",
        type="experimental_fixture",
        truth_confidence=0.65,
    )

    nodes["ALT_C"] = TruthNode(
        id="ALT_C",
        tag="ALTERNATIVE_C",
        type="experimental_fixture",
        truth_confidence=0.92,
    )

    edges.extend(
        [
            TruthEdge(
                source="PROJECT",
                target="ALT_A",
                tag="ALTERNATIVE",
                relation="alternative",
                weight=0.91,
            ),
            TruthEdge(
                source="ALT_A",
                target="EVIDENCE",
                tag="ALTERNATIVE",
                relation="alternative",
                weight=0.91,
            ),
            TruthEdge(
                source="PROJECT",
                target="ALT_B",
                tag="ALTERNATIVE",
                relation="alternative",
                weight=0.98,
            ),
            TruthEdge(
                source="ALT_B",
                target="EVIDENCE",
                tag="ALTERNATIVE",
                relation="alternative",
                weight=0.98,
            ),
            TruthEdge(
                source="PROJECT",
                target="ALT_C",
                tag="ALTERNATIVE",
                relation="alternative",
                weight=0.94,
            ),
            TruthEdge(
                source="ALT_C",
                target="EVIDENCE",
                tag="ALTERNATIVE",
                relation="alternative",
                weight=0.94,
            ),
        ]
    )

    return TruthGraph(nodes, edges)


CASES = [
    AdversarialCase(
        name="multiple_competing_paths",
        start="PROJECT",
        end="EVIDENCE",
    ),
    AdversarialCase(
        name="multiple_competing_paths_reverse",
        start="EVIDENCE",
        end="PROJECT",
    ),
]


def main() -> None:
    graph = build_adversarial_graph()
    scorer = PredictivePathScorer(graph)

    print("===== OPENMIND ADVERSARIAL PATH BENCHMARK =====")

    results = []

    for case in CASES:
        canonical_paths = graph.find_paths(case.start, case.end)

        if not canonical_paths:
            print(f"{case.name}: NO PATH")
            continue

        canonical = canonical_paths[0]
        predictive = scorer.best_path(case.start, case.end)

        if predictive is None:
            print(f"{case.name}: NO PREDICTIVE PATH")
            continue

        agreement = canonical.nodes == predictive.path.nodes

        print()
        print(case.name)
        print(f"start: {case.start}")
        print(f"end:   {case.end}")
        print(f"candidate_paths: {len(canonical_paths)}")
        print(f"canonical:  {' -> '.join(canonical.nodes)}")
        print(f"predictive: {' -> '.join(predictive.path.nodes)}")
        print(f"agreement: {agreement}")
        print(f"canonical_score:  {canonical.score:.12f}")
        print(f"predictive_score: {predictive.predictive_score:.12f}")
        print(f"fuzzy_score:      {predictive.fuzzy_score:.12f}")

        print("ranked_candidates:")

        for index, path in enumerate(canonical_paths, start=1):
            experimental = scorer.score(path)

            print(
                f"  {index}. "
                f"{' -> '.join(path.nodes)} | "
                f"canonical={path.score:.12f} | "
                f"predictive={experimental.predictive_score:.12f}"
            )

        results.append(
            {
                "name": case.name,
                "candidate_paths": len(canonical_paths),
                "agreement": agreement,
                "canonical_path": list(canonical.nodes),
                "predictive_path": list(predictive.path.nodes),
            }
        )

    print()
    print("===== SUMMARY =====")

    if results:
        agreements = sum(item["agreement"] for item in results)

        print(f"cases: {len(results)}")
        print(f"agreement: {agreements}/{len(results)}")
        print(
            f"agreement_rate: "
            f"{agreements / len(results):.6f}"
        )

    output = (
        Path(__file__).resolve().parent
        / "results"
        / "adversarial.json"
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(
            {
                "name": "openmind_truth_graph_adversarial",
                "experimental": True,
                "results": results,
            },
            indent=2,
        )
        + "\n"
    )

    print(f"results: {output}")


if __name__ == "__main__":
    main()
