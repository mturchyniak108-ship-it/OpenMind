import numpy as np
from pi_waveform_fractal import pi_fractal


# ---------------------------------------------------------
# Convert a text seed into deterministic 2D stimulus
# ---------------------------------------------------------
def stimulus_vector(seed: str):
    h = abs(hash(seed))
    x = (h % 1000) / 1000.0
    y = ((h // 1000) % 1000) / 1000.0
    return np.array([x, y])


# ---------------------------------------------------------
# Project stimulus into π fractal attractor
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
# Full π Tokenless Inference Experiment (TIE-π)
# ---------------------------------------------------------
def tokenless_inference_pi(seed: str):
    fractal = pi_fractal()
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
        print(tokenless_inference_pi(s))
