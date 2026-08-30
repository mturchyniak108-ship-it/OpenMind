import numpy as np
import os
import json

from openmind.experimental.fractal import encode_fractal, encode_color
from openmind.experimental.path_meta import from_truth_path
from openmind.truth_graph import TruthGraph, TruthNode, TruthEdge, TruthPath

from gguf_to_fractal import (
    load_gguf_tensor,
    build_truth_graph,
    build_linear_truth_path,
)


def benchmark_fractal_vs_model(model_path="model.gguf"):
    # Load raw model tensor
    acts = load_gguf_tensor(model_path)
    raw_bytes = os.path.getsize(model_path)

    # Build truth graph + path
    graph = build_truth_graph(acts)
    keys = list(graph.nodes.keys())
    path = graph.best_path(keys[0], keys[-1]) or build_linear_truth_path(graph)

    # Build meta + fractal
    meta = from_truth_path(path, graph, predictive_weight=0.75)
    fractal = encode_fractal(meta)
    colors = encode_color(fractal)

    # Compute metrics
    fractal_size = len(fractal.strand_a) + len(fractal.strand_b)
    convergence = len(fractal.convergence_points)
    color_count = len(colors)

    # Entropy estimate (simple variance)
    entropy_model = float(np.var(acts))
    entropy_fractal = float(np.var([p.x for p in fractal.strand_a] +
                                   [p.y for p in fractal.strand_a]))

    # Compression ratio
    ratio = fractal_size / (acts.size)

    # Package results
    results = {
        "model_bytes": raw_bytes,
        "model_tensor_elements": int(acts.size),
        "fractal_points": fractal_size,
        "convergence_points": convergence,
        "color_samples": color_count,
        "compression_ratio": ratio,
        "entropy_model": entropy_model,
        "entropy_fractal": entropy_fractal,
        "path_length": len(path.nodes),
    }

    print(json.dumps(results, indent=4))
    return results


if __name__ == "__main__":
    benchmark_fractal_vs_model()
