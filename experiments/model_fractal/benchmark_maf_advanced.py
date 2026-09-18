import numpy as np
import hashlib
from gguf_to_fractal import (
    load_gguf_tensor,
    build_truth_graph,
    build_linear_truth_path,
)
from openmind.experimental.path_meta import from_truth_path
from openmind.experimental.fractal import encode_fractal, encode_color


def fractal_hash(fractal):
    h = hashlib.sha256()
    for p in fractal.strand_a:
        h.update(str(p.x).encode())
        h.update(str(p.y).encode())
    for p in fractal.strand_b:
        h.update(str(p.x).encode())
        h.update(str(p.y).encode())
    return h.hexdigest()


def benchmark(model_path="model.gguf"):
    acts = load_gguf_tensor(model_path)
    graph = build_truth_graph(acts)
    keys = list(graph.nodes.keys())
    path = graph.best_path(keys[0], keys[-1]) or build_linear_truth_path(graph)

    meta = from_truth_path(path, graph, predictive_weight=0.75)
    fractal = encode_fractal(meta)
    colors = encode_color(fractal)

    # Strand divergence
    div = float(np.mean([
        abs(a.x - b.x) + abs(a.y - b.y)
        for a, b in zip(fractal.strand_a, fractal.strand_b)
    ]))

    # Convergence stability
    conv = float(np.var([p.x + p.y for p in fractal.convergence_points]))

    # Semantic drift (model vs fractal)
    drift = float(abs(np.var(acts) - np.var([p.x for p in fractal.strand_a])))

    # Identity hash
    fid = fractal_hash(fractal)

    print({
        "strand_divergence": div,
        "convergence_stability": conv,
        "semantic_drift": drift,
        "fractal_hash": fid,
    })


if __name__ == "__main__":
    benchmark()
