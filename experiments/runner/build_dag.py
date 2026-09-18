from pathlib import Path
import ast
import json
import re

ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / "experiments" / "model_fractal"

files = {
    p.name: p
    for p in EXP.glob("*.py")
}

known_artifacts = {
    p.name
    for p in EXP.iterdir()
    if p.is_file()
}

# Also recognize root-level experiment inputs.
for p in ROOT.iterdir():
    if p.is_file():
        known_artifacts.add(p.name)

deps = {}

def resolve_ref(ref, current):
    ref = str(ref)

    candidates = [
        EXP / ref,
        EXP / Path(ref).name,
        ROOT / ref,
        ROOT / Path(ref).name,
    ]

    for c in candidates:
        if c.exists():
            return c.name

    return None


for name, path in sorted(files.items()):
    text = path.read_text(errors="ignore")
    found = set()

    # Literal strings in Python AST.
    try:
        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                s = node.value

                # Explicit known artifact references.
                for artifact in known_artifacts:
                    if artifact in s:
                        found.add(artifact)

                # Filename-like literals.
                if re.search(
                    r'\.(json|txt|csv|gguf)$',
                    s,
                    re.IGNORECASE
                ):
                    resolved = resolve_ref(s, path)
                    if resolved:
                        found.add(resolved)

    except SyntaxError:
        pass

    # Conservative fallback for explicit filenames in source.
    for m in re.finditer(
        r'["\']([^"\']+\.(?:json|txt|csv|gguf))["\']',
        text,
        re.IGNORECASE
    ):
        resolved = resolve_ref(m.group(1), path)
        if resolved:
            found.add(resolved)

    deps[name] = sorted(found)


# Map artifact -> producer experiment.
producers = {}

for exp, refs in deps.items():
    for ref in refs:
        stem = Path(ref).stem
        if stem + ".py" in files:
            producers[ref] = stem + ".py"


# Convert artifact dependencies into experiment dependencies.
edges = {}

for exp, refs in deps.items():
    parents = set()

    for ref in refs:
        producer = producers.get(ref)
        if producer and producer != exp:
            parents.add(producer)

    edges[exp] = sorted(parents)


out = {
    "experiments": sorted(files),
    "dependencies": deps,
    "edges": edges,
}

(ROOT / "results" / "experiment_dag.json").write_text(
    json.dumps(out, indent=2)
)

print("=" * 70)
print(" OPENMIND EXPERIMENT DEPENDENCY GRAPH")
print("=" * 70)

edge_count = 0

for exp in sorted(edges):
    if edges[exp]:
        print(f"\n{exp}")
        for parent in edges[exp]:
            print(f"  <- {parent}")
            edge_count += 1

print()
print("=" * 70)
print(f"EXPERIMENTS: {len(files)}")
print(f"DEPENDENCY EDGES: {edge_count}")
print("=" * 70)
print()
print("Saved: results/experiment_dag.json")
