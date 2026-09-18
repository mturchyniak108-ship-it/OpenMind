import numpy as np
from hybrid_fractal import hybrid_fractal


def stimulus_vector(seed: str):
    h = abs(hash(seed))
    x = (h % 1000) / 1000.0
    y = ((h // 1000) % 1000) / 1000.0
    return np.array([x, y])


def project(fractal, stim):
    proj_a = [
        np.linalg.norm(np.array([p.x, p.y]) - stim)
        for p in fractal["strand_a"]
    ]
    proj_b = [
        np.linalg.norm(np.array([p.x, p.y]) - stim)
        for p in fractal["strand_b"]
    ]

    idx_a = int(np.argmin(proj_a))
    idx_b = int(np.argmin(proj_b))

    return idx_a, idx_b


def semantic_signature(idx_a, idx_b):
    delta = abs(idx_a - idx_b)
    coherence = 1.0 / (1.0 + delta)

    return {
        "anchor_a": idx_a,
        "anchor_b": idx_b,
        "delta": delta,
        "coherence": coherence
    }


def tokenless_inference_hybrid(seed: str):
    fractal = hybrid_fractal()
    stim = stimulus_vector(seed)
    idx_a, idx_b = project(fractal, stim)
    return semantic_signature(idx_a, idx_b)


if __name__ == "__main__":
    seeds = ["creativity", "math", "danger", "language", "emotion"]

    for s in seeds:
        print(f"\nSeed: {s}")
        print(tokenless_inference_hybrid(s))
