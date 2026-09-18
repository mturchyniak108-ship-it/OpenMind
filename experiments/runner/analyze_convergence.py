from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
data = json.loads((ROOT / "results/experiment_dag.json").read_text())

edges = data["edges"]
nodes = set(data["experiments"])

excluded = {
    n for n in nodes
    if any(x in n.lower() for x in (
        "reference",
        "snapshot",
        "backup",
        "_work.py",
    ))
}

nodes -= excluded

parents = {
    n: {p for p in edges.get(n, []) if p in nodes}
    for n in nodes
}

children = {n: set() for n in nodes}

for child, ps in parents.items():
    for parent in ps:
        children[parent].add(child)

roots = sorted(n for n in nodes if not parents[n])
sinks = sorted(n for n in nodes if not children[n])

# Determine all roots that can reach each node.
root_sets = {n: set() for n in nodes}

for root in roots:
    stack = [root]
    seen = set()

    while stack:
        cur = stack.pop()

        if cur in seen:
            continue

        seen.add(cur)
        root_sets[cur].add(root)

        stack.extend(children[cur])

# Descendant count.
descendants = {}

for node in nodes:
    stack = list(children[node])
    seen = set()

    while stack:
        cur = stack.pop()

        if cur in seen:
            continue

        seen.add(cur)
        stack.extend(children[cur])

    descendants[node] = len(seen)

print("=" * 86)
print(" OPENMIND DAG CONVERGENCE ANALYSIS")
print("=" * 86)
print()
print(f"ACTIVE NODES : {len(nodes)}")
print(f"ROOTS        : {len(roots)}")
print(f"SINKS        : {len(sinks)}")
print()

print("MOST CONVERGENT NODES")
print("-" * 86)
print(
    f"{'EXPERIMENT':55} "
    f"{'ROOTS':>5} "
    f"{'PARENTS':>7} "
    f"{'DESC':>7}"
)

rows = sorted(
    nodes,
    key=lambda n: (
        -len(root_sets[n]),
        -descendants[n],
        n,
    )
)

for n in rows[:25]:
    print(
        f"{n:55} "
        f"{len(root_sets[n]):5d} "
        f"{len(parents[n]):7d} "
        f"{descendants[n]:7d}"
    )

print()
print("FOUNDATION NODES")
print("-" * 86)

for n in sorted(
    nodes,
    key=lambda n: (-descendants[n], n)
)[:15]:
    print(
        f"{n:55} "
        f"roots={len(root_sets[n]):2d} "
        f"descendants={descendants[n]:2d}"
    )

print()
print("ROOTS")
print("-" * 86)

for r in roots:
    print(f"  {r}")

print()
print("=" * 86)
