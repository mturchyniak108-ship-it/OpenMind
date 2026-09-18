from pathlib import Path
import ast
import json
import hashlib
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / "experiments" / "model_fractal"
DAG = ROOT / "results" / "experiment_dag.json"

data = json.loads(DAG.read_text())
deps = data["dependencies"]

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

print("=" * 78)
print(" OPENMIND ARTIFACT PROVENANCE AUDIT")
print("=" * 78)
print()

artifact_users = defaultdict(list)

for exp, refs in deps.items():
    for ref in refs:
        artifact_users[ref].append(exp)

print("HIGH-FANOUT ARTIFACTS")
print("-" * 78)

for artifact, users in sorted(
    artifact_users.items(),
    key=lambda x: (-len(x[1]), x[0])
):
    if len(users) >= 5:
        print(f"{artifact:<55} users={len(users)}")

print()
print("ARTIFACT HASHES")
print("-" * 78)

for artifact in sorted(artifact_users):
    candidates = [
        EXP / artifact,
        ROOT / artifact,
    ]

    path = next((p for p in candidates if p.exists()), None)

    if path:
        print(
            f"{artifact:<55} "
            f"{sha256(path)[:16]}"
        )

print()
print("=" * 78)
print("DEPENDENCY ROOTS")
print("=" * 78)

for exp in sorted(data["experiments"]):
    if not data["edges"].get(exp):
        print(f"ROOT  {exp}")

print()
print("Audit complete.")
