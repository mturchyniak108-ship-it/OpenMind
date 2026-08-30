import numpy as np

from openmind.truth_graph import TruthGraph, TruthNode, TruthEdge, TruthPath
from openmind.experimental.path_meta import from_truth_path
from openmind.experimental.fractal import encode_fractal


# ---------------------------------------------------------
# Generate digits of pi (simple spigot-like approximation)
# ---------------------------------------------------------
def pi_digits(n=2000):
    # This is a safe, Termux-friendly approximation
    # Not a full spigot algorithm, but stable enough for fractalization
    pi_str = (
        "3."
        "14159265358979323846264338327950288419716939937510"
        "58209749445923078164062862089986280348253421170679"
        "82148086513282306647093844609550582231725359408128"
        "48111745028410270193852110555964462294895493038196"
        "44288109756659334461284756482337867831652712019091"
        "45648566923460348610454326648213393607260249141273"
        "72458700660631558817488152092096282925409171536436"
        "78925903600113305305488204665213841469519415116094"
        "33057270365759591953092186117381932611793105118548"
    )
    digits = [int(c) for c in pi_str if c.isdigit()]
    return digits[:n]


# ---------------------------------------------------------
# Convert pi digits into a 3-channel waveform
# ---------------------------------------------------------
def pi_waveform(pi):
    amps = np.array(pi) / 9.0
    freqs = np.abs(np.diff(pi)) / 9.0
    phases = (np.array(pi[1:]) / (np.array(pi[:-1]) + 1e-6)) % 1.0

    wf = np.stack([amps[:-1], freqs, phases], axis=1)
    return wf


# ---------------------------------------------------------
# Build TruthGraph from waveform
# ---------------------------------------------------------
def waveform_truth_graph(wf):
    mags = np.linalg.norm(wf, axis=1)
    max_mag = mags.max()

    nodes = {}
    edges = []

    for i, mag in enumerate(mags):
        conf = float(mag / max_mag)
        nid = f"P{i}"

        nodes[nid] = TruthNode(
            id=nid,
            tag=f"pi_{i}",
            type="waveform",
            truth_confidence=conf
        )

        if i > 0:
            edges.append(
                TruthEdge(
                    source=f"P{i-1}",
                    target=nid,
                    tag="flow",
                    relation="flows_to",
                    weight=conf
                )
            )

    return TruthGraph(nodes, edges)


# ---------------------------------------------------------
# Build a linear TruthPath
# ---------------------------------------------------------
def build_linear_truth_path(graph):
    keys = list(graph.nodes.keys())[:128]
    edges = []
    weights = []

    for i in range(len(keys) - 1):
        src = keys[i]
        dst = keys[i + 1]

        edge = next(
            (e for e in graph.edges if e.source == src and e.target == dst),
            TruthEdge(
                source=src,
                target=dst,
                tag="flow",
                relation="flows_to",
                weight=graph.nodes[dst].truth_confidence
            )
        )

        edges.append(edge)
        weights.append(edge.weight)

    score = float(sum(weights))
    cost = float(sum(1.0 - w for w in weights))

    return TruthPath(
        score=score,
        cost=cost,
        nodes=keys,
        edges=edges
    )


# ---------------------------------------------------------
# Generate the π Waveform Fractal (PWF)
# ---------------------------------------------------------
def pi_fractal():
    pi = pi_digits(2000)
    wf = pi_waveform(pi)
    graph = waveform_truth_graph(wf)
    path = build_linear_truth_path(graph)
    meta = from_truth_path(path, graph, predictive_weight=0.75)
    return encode_fractal(meta)


# ---------------------------------------------------------
# Demo run
# ---------------------------------------------------------
if __name__ == "__main__":
    fractal = pi_fractal()
    print("=== π Waveform Fractal (PWF) ===")
    print("Strand A:", len(fractal.strand_a))
    print("Strand B:", len(fractal.strand_b))
    print("Convergence:", len(fractal.convergence_points))
    print("Color samples:", len(fractal.strand_a))
    print("Fractal Hash:", fractal.path_id)
