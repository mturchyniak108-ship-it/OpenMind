from pathlib import Path
import json
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
data = json.loads((ROOT / "results/experiment_dag.json").read_text())

edges = data["edges"]
nodes = set(data["experiments"])

# Remove archive/reference/snapshot/backup/work nodes from production analysis.
excluded = {
    n for n in nodes
    if any(x in n.lower() for x in (
        "reference",
        "snapshot",
        "backup",
        "_work.py",
    ))
}

active = nodes - excluded

parents = {
    n: {p for p in edges.get(n, []) if p in active}
    for n in active
}

children = defaultdict(set)

for child, ps in parents.items():
    for parent in ps:
        children[parent].add(child)

remaining = {n: set(ps) for n, ps in parents.items()}

levels = []
done = set()

while remaining:
    ready = sorted(
        n for n, ps in remaining.items()
        if not ps
    )

    if not ready:
        raise RuntimeError("Cycle detected in active DAG")

    levels.append(ready)

    for n in ready:
        done.add(n)
        del remaining[n]

    for ps in remaining.values():
        ps.difference_update(ready)

print("=" * 78)
print(" OPENMIND TOPOLOGICAL EXECUTION LEVELS")
print("=" * 78)
print()
print(f"ACTIVE EXPERIMENTS : {len(active)}")
print(f"EXCLUDED           : {len(excluded)}")
print(f"LEVELS             : {len(levels)}")
print()

for i, level in enumerate(levels):
    print(f"LEVEL {i:02d}  ({len(level)} experiments)")
    print("-" * 78)

    for n in level:
        print(f"  {n}")

    print()

print("=" * 78)
print("EXCLUDED FROM PRODUCTION DAG")
print("=" * 78)

for n in sorted(excluded):
    print(f"  {n}")
