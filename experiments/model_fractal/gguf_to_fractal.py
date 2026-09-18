import numpy as np

from openmind.truth_graph import TruthGraph, TruthNode, TruthEdge, TruthPath
from openmind.experimental.path_meta import from_truth_path
from openmind.experimental.fractal import encode_fractal, encode_color


def load_gguf_tensor(path: str) -> np.ndarray:
    raw = np.fromfile(path, dtype=np.float32)

    raw = np.nan_to_num(raw, nan=0.0, posinf=1e6, neginf=-1e6)
    raw = np.clip(raw, -1e6, 1e6)

    if raw.size < 4096:
        raise ValueError("GGUF file too small for fractal extraction.")

    hidden = 768
    seq = raw.size // hidden
    acts = raw[: seq * hidden].reshape(seq, hidden)

    norms = np.linalg.norm(acts, axis=-1, keepdims=True)
    norms = np.where(norms == 0, 1.0, norms)
    acts = acts / norms

    return acts


def build_truth_graph(acts: np.ndarray) -> TruthGraph:
    mags = np.linalg.norm(acts, axis=-1)
    max_mag = mags.max() if mags.size else 1.0

    nodes = {}
    edges = []

    for i, mag in enumerate(mags):
        conf = float(mag / max_mag)
        if not np.isfinite(conf):
            conf = 0.0

        nid = f"N{i}"
        nodes[nid] = TruthNode(
            id=nid,
            tag=f"pos_{i}",
            type="activation",
            truth_confidence=conf,
        )

        if i > 0:
            prev = f"N{i-1}"
            edges.append(
                TruthEdge(
                    source=prev,
                    target=nid,
                    tag="flow",
                    relation="flows_to",
                    weight=conf,
                )
            )

    return TruthGraph(nodes, edges)


def build_linear_truth_path(graph: TruthGraph) -> TruthPath:
    keys = list(graph.nodes.keys())
    if len(keys) < 2:
        raise ValueError("Graph too small for path generation.")

    keys = keys[:128]  # limit length

    node_ids = keys[:]  # TruthPath expects IDs, not objects
    edges = []

    weights = []

    for i in range(len(node_ids) - 1):
        src = node_ids[i]
        dst = node_ids[i + 1]

        edge = next(
            (e for e in graph.edges if e.source == src and e.target == dst),
            TruthEdge(
                source=src,
                target=dst,
                tag="flow",
                relation="flows_to",
                weight=graph.nodes[dst].truth_confidence,
            )
        )

        edges.append(edge)
        weights.append(edge.weight)

    score = float(sum(weights))
    cost = float(sum(1.0 - w for w in weights))

    return TruthPath(
        score=score,
        cost=cost,
        nodes=node_ids,   # MUST be IDs
        edges=edges,      # edges referencing IDs
    )


def main():
    acts = load_gguf_tensor("model.gguf")
    graph = build_truth_graph(acts)

    keys = list(graph.nodes.keys())
    path = graph.best_path(keys[0], keys[-1])

    if path is None:
        path = build_linear_truth_path(graph)

    meta = from_truth_path(path, graph, predictive_weight=0.75)
    fractal = encode_fractal(meta)
    colors = encode_color(fractal)

    print("=== Mitchell Activation Fractal (MAF) from GGUF ===")
    print("Path ID:", fractal.path_id)
    print("Strand A:", len(fractal.strand_a))
    print("Strand B:", len(fractal.strand_b))
    print("Convergence:", len(fractal.convergence_points))
    print("Color samples:", len(colors))
    print("Fractal successfully generated from GGUF model data.")


if __name__ == "__main__":
    main()
