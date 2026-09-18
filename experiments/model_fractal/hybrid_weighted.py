import numpy as np
from hybrid_fractal import load_maf
from pi_waveform_fractal import pi_fractal


def weighted_hybrid(w=0.8):
    maf = load_maf()
    pf = pi_fractal()

    n = min(len(maf.strand_a), len(pf.strand_a))

    hybrid_a = []
    hybrid_b = []

    for i in range(n):
        ma = maf.strand_a[i]
        pa = pf.strand_a[i]
        mb = maf.strand_b[i]
        pb = pf.strand_b[i]

        ha = ma.__class__(
            x=(ma.x * w + pa.x * (1 - w)),
            y=(ma.y * w + pa.y * (1 - w)),
            z=ma.z,
            strand=ma.strand,
            edge_index=ma.edge_index,
            convergence_weight=ma.convergence_weight
        )

        hb = mb.__class__(
            x=(mb.x * w + pb.x * (1 - w)),
            y=(mb.y * w + pb.y * (1 - w)),
            z=mb.z,
            strand=mb.strand,
            edge_index=mb.edge_index,
            convergence_weight=mb.convergence_weight
        )

        hybrid_a.append(ha)
        hybrid_b.append(hb)

    return {
        "strand_a": hybrid_a,
        "strand_b": hybrid_b,
        "convergence": maf.convergence_points,
        "path_id": f"WHF(w={w})"
    }


if __name__ == "__main__":
    for w in [0.2, 0.5, 0.8]:
        h = weighted_hybrid(w)
        print(f"\n=== Weighted Hybrid w={w} ===")
        print("Strand A:", len(h["strand_a"]))
        print("Strand B:", len(h["strand_b"]))
        print("Path ID:", h["path_id"])
