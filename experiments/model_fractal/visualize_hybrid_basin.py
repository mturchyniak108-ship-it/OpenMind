import numpy as np
from hybrid_weighted import weighted_hybrid


def basin_stats(points):
    xs = np.array([p.x for p in points])
    ys = np.array([p.y for p in points])

    return {
        "min_x": float(xs.min()),
        "max_x": float(xs.max()),
        "min_y": float(ys.min()),
        "max_y": float(ys.max()),
        "spread_x": float(xs.max() - xs.min()),
        "spread_y": float(ys.max() - ys.min()),
        "centroid_x": float(xs.mean()),
        "centroid_y": float(ys.mean()),
        "std_x": float(xs.std()),
        "std_y": float(ys.std()),
    }


def visualize(w):
    h = weighted_hybrid(w)

    a_stats = basin_stats(h["strand_a"])
    b_stats = basin_stats(h["strand_b"])

    print(f"\n=== Hybrid Attractor Basin (w={w}) ===")
    print("\nStrand A Basin:")
    for k, v in a_stats.items():
        print(f"  {k}: {v}")

    print("\nStrand B Basin:")
    for k, v in b_stats.items():
        print(f"  {k}: {v}")

    # Convergence centroid
    cx = np.mean([p.x for p in h["convergence"]])
    cy = np.mean([p.y for p in h["convergence"]])

    print("\nConvergence Centroid:")
    print(f"  x: {cx}")
    print(f"  y: {cy}")

    # Divergence band
    div = abs(a_stats["centroid_x"] - b_stats["centroid_x"]) + \
          abs(a_stats["centroid_y"] - b_stats["centroid_y"])

    print("\nHybrid Divergence Band:")
    print(f"  divergence: {div}")


if __name__ == "__main__":
    for w in [0.2, 0.5, 0.8]:
        visualize(w)
