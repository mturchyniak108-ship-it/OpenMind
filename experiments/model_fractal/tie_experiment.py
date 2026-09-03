import numpy as np

from gguf_to_fractal import (
    load_gguf_tensor,
    build_truth_graph,
    build_linear_truth_path
)

from openmind.experimental.path_meta import from_truth_path
from openmind.experimental.fractal import encode_fractal


# ---------------------------------------------------------
# Load the Mitchell Activation Fractal (MAF)
# ---------------------------------------------------------
def load_maf():
    acts = load_gguf_tensor("model.gguf")
    graph = build_truth_graph(acts)
    path = build_linear_truth_path(graph)
    meta = from_truth_path(path, graph, predictive_weight=0.75)
    return encode_fractal(meta)


# ---------------------------------------------------------
# Convert a text seed into a deterministic 2D stimulus
# ---------------------------------------------------------
def stimulus_vector(seed: str):
    h = abs(hash(seed))
    x = (h % 1000) / 1000.0
    y = ((h // 1000) % 1000) / 1000.0
    return np.array([x, y])


# ---------------------------------------------------------
# Project stimulus into fractal attractor
# ---------------------------------------------------------
def project(fractal, stim):
    proj_a = [
        np.linalg.norm(np.array([p.x, p.y]) - stim)
        for p in fractal.strand_a
    ]
    proj_b = [
        np.linalg.norm(np.array([p.x, p.y]) - stim)
        for p in fractal.strand_b
    ]

    idx_a = int(np.argmin(proj_a))
    idx_b = int(np.argmin(proj_b))

    return idx_a, idx_b


# ---------------------------------------------------------
# Convert anchor indices into semantic signature
# ---------------------------------------------------------
def semantic_signature(idx_a, idx_b):
    delta = abs(idx_a - idx_b)
    coherence = 1.0 / (1.0 + delta)

    return {
        "anchor_a": idx_a,
        "anchor_b": idx_b,
        "delta": delta,
        "coherence": coherence
    }


# ---------------------------------------------------------
# Full Tokenless Inference Experiment (TIE-1)
# ---------------------------------------------------------
def tokenless_inference(seed: str):
    fractal = load_maf()
    stim = stimulus_vector(seed)
    idx_a, idx_b = project(fractal, stim)
    return semantic_signature(idx_a, idx_b)


# ---------------------------------------------------------
# Demo run
# ---------------------------------------------------------
if __name__ == "__main__":
    seeds = ["creativity", "math", "danger", "language", "emotion"]

    for s in seeds:
        print(f"\nSeed: {s}")
        print(tokenless_inference(s))
