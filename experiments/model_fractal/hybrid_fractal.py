import numpy as np

from gguf_to_fractal import load_gguf_tensor, build_truth_graph, build_linear_truth_path
from openmind.experimental.path_meta import from_truth_path
from openmind.experimental.fractal import encode_fractal
from pi_waveform_fractal import pi_fractal


def load_maf():
    acts = load_gguf_tensor("model.gguf")
    graph = build_truth_graph(acts)
    path = build_linear_truth_path(graph)
    meta = from_truth_path(path, graph, predictive_weight=0.75)
    return encode_fractal(meta)


def hybrid_fractal():
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

        # clone original points
        ha = ma.__class__(
            x=(ma.x + pa.x) / 2.0,
            y=(ma.y + pa.y) / 2.0,
            z=ma.z,
            strand=ma.strand,
            edge_index=ma.edge_index,
            convergence_weight=ma.convergence_weight
        )

        hb = mb.__class__(
            x=(mb.x + pb.x) / 2.0,
            y=(mb.y + pb.y) / 2.0,
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
        "path_id": f"HYBRID({maf.path_id} | {pf.path_id})"
    }


if __name__ == "__main__":
    h = hybrid_fractal()
    print("=== π–MAF Hybrid Fractal ===")
    print("Strand A:", len(h["strand_a"]))
    print("Strand B:", len(h["strand_b"]))
    print("Convergence:", len(h["convergence"]))
    print("Path ID:", h["path_id"][:120] + "...")
