"""Canonical OpenMind Truth Pipeline CLI."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from openmind.evidence import (
    EvidenceRegistry,
    EdgeEvidenceBindings,
    TruthTraceResolver,
    audit_truth_trace,
)
from openmind.truth_graph import TruthGraph


ROOT = Path(__file__).resolve().parents[2]
GRAPH_ROOT = ROOT / "demo" / "truth_graph"


def load_evidence() -> EvidenceRegistry:
    """Load canonical evidence through the registry persistence layer."""

    return EvidenceRegistry.load(
        GRAPH_ROOT / "evidence.json"
    )


def report_json(start: str, end: str) -> tuple[int, str]:
    """Return the canonical truth trace as a deterministic JSON report."""

    graph = TruthGraph.from_json(
        GRAPH_ROOT / "nodes.json",
        GRAPH_ROOT / "edges.json",
    )

    registry = load_evidence()
    evidence = list(registry.all())

    binding_registry = EdgeEvidenceBindings.load(
        GRAPH_ROOT / "bindings.json"
    )

    bindings = binding_registry.as_dict()

    resolver = TruthTraceResolver(graph, evidence)

    if start not in graph.nodes or end not in graph.nodes:
        return 1, "NO CANONICAL PATH"

    trace = resolver.resolve(
        start,
        end,
        bindings,
    )

    if trace is None:
        return 1, "NO CANONICAL PATH"

    audited = audit_truth_trace(trace, registry)

    report = {
        "start": audited.start,
        "end": audited.end,
        "path": [
            audited.start,
            *[step.target for step in audited.steps],
        ],
        "score": audited.score,
        "evidence": [
            {
                "source": resolved.source,
                "target": resolved.target,
                "evidence_id": resolved.evidence_id,
                "status": resolved.status,
            }
            for resolved in audited.evidence
        ],
        "coverage": {
            "total_edges": audited.coverage.total_edges,
            "registered_edges": audited.coverage.registered_edges,
            "unbound_edges": audited.coverage.unbound_edges,
            "missing_edges": audited.coverage.missing_edges,
            "coverage": audited.coverage.coverage,
        },
        "provenance_gaps": {
            "unbound": [
                list(edge)
                for edge in audited.coverage.unbound
            ],
            "missing": [
                list(edge)
                for edge in audited.coverage.missing
            ],
        },
    }

    return 0, json.dumps(
        report,
        separators=(",", ": "),
    )


def main(start: str, end: str) -> int:
    graph = TruthGraph.from_json(
        GRAPH_ROOT / "nodes.json",
        GRAPH_ROOT / "edges.json",
    )

    registry = load_evidence()
    evidence = list(registry.all())

    binding_registry = EdgeEvidenceBindings.load(
        GRAPH_ROOT / "bindings.json"
    )

    bindings = binding_registry.as_dict()

    resolver = TruthTraceResolver(graph, evidence)

    if start not in graph.nodes or end not in graph.nodes:
        print("NO CANONICAL PATH")
        return 1

    trace = resolver.resolve(
        start,
        end,
        bindings,
    )

    if trace is None:
        print("NO CANONICAL PATH")
        return 1

    audited = audit_truth_trace(trace, registry)

    print("===== OPENMIND CANONICAL TRUTH TRACE =====")
    print()
    print(f"start: {audited.start}")
    print(f"end:   {audited.end}")
    print()

    print("PATH")
    print(" -> ".join(
        [audited.start]
        + [step.target for step in audited.steps]
    ))
    print()

    print("EVIDENCE")

    for step, resolved in zip(
        audited.steps,
        audited.evidence,
    ):
        print(
            f"{step.source} -> {step.target}"
            f" | relation={step.relation}"
            f" | weight={step.weight:.6f}"
            f" | evidence={resolved.evidence_id or 'UNBOUND'}"
            f" | status={resolved.status}"
        )

    print()
    print("CANONICAL SCORE")
    print(f"{audited.score:.12f}")

    print()
    print("PROVENANCE")
    print(f"registered: {audited.coverage.registered_edges}")
    print(f"unbound:    {audited.coverage.unbound_edges}")
    print(f"missing:    {audited.coverage.missing_edges}")
    print(f"coverage:   {audited.coverage.coverage:.6f}")

    if audited.coverage.unbound or audited.coverage.missing:
        print()
        print("PROVENANCE GAPS")

        for source, target in audited.coverage.unbound:
            print(f"UNBOUND: {source} -> {target}")

        for source, target in audited.coverage.missing:
            print(f"MISSING: {source} -> {target}")

    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "usage: python -m openmind.cli.truth "
            "<start_node> <end_node>"
        )
        raise SystemExit(2)

    raise SystemExit(
        main(sys.argv[1], sys.argv[2])
    )
