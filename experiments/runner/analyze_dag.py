from pathlib import Path
import json
from collections import defaultdict, deque

ROOT = Path(__file__).resolve().parents[2]
d = json.loads((ROOT / "results" / "experiment_dag.json").read_text())

nodes = d["experiments"]
edges = d["edges"]

children = defaultdict(set)
parents = {n: set(edges.get(n, [])) for n in nodes}

for child, ps in parents.items():
    for parent in ps:
        children[parent].add(child)

def descendants(start):
    seen = set()
    q = deque([start])

    while q:
        n = q.popleft()
        for c in children[n]:
            if c not in seen:
                seen.add(c)
                q.append(c)

    return seen

def ancestors(start):
    seen = set()
    q = deque([start])

    while q:
        n = q.popleft()
        for p in parents[n]:
            if p not in seen:
                seen.add(p)
                q.append(p)

    return seen

roots = sorted(n for n in nodes if not parents[n])
sinks = sorted(n for n in nodes if not children[n])

print("=" * 78)
print(" OPENMIND DAG ARCHITECTURE ANALYSIS")
print("=" * 78)

print("\nROOT EXPERIMENTS")
print("-" * 78)
for n in roots:
    print(f"{n:55} downstream={len(descendants(n)):3}")

print("\nSINK EXPERIMENTS")
print("-" * 78)
for n in sinks:
    print(f"{n:55} upstream={len(ancestors(n)):3}")

print("\nMOST CENTRAL EXPERIMENTS")
print("-" * 78)

ranking = []

for n in nodes:
    ranking.append((
        len(descendants(n)),
        len(children[n]),
        len(parents[n]),
        n,
    ))

for downstream, direct_children, direct_parents, n in sorted(
    ranking, reverse=True
)[:20]:
    print(
        f"{n:55} "
        f"downstream={downstream:3} "
        f"direct_children={direct_children:2} "
        f"parents={direct_parents:2}"
    )

print("\nROOT COUNT :", len(roots))
print("SINK COUNT :", len(sinks))
print("=" * 78)
