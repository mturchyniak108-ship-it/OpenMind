from pathlib import Path
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
DAG_FILE = ROOT / "results" / "experiment_dag.json"
RESULTS = ROOT / "results" / "dag_runs"
RESULTS.mkdir(parents=True, exist_ok=True)

data = json.loads(DAG_FILE.read_text())

nodes = set(data["experiments"])
edges = data["edges"]

EXCLUDED = {
    n for n in nodes
    if any(x in n.lower() for x in (
        "reference",
        "snapshot",
        "backup",
        "_work.py",
    ))
}

ACTIVE = nodes - EXCLUDED

parents = {
    n: {p for p in edges.get(n, []) if p in ACTIVE}
    for n in ACTIVE
}

remaining = {n: set(p) for n, p in parents.items()}

levels = []

while remaining:
    ready = sorted(
        n for n, ps in remaining.items()
        if not ps
    )

    if not ready:
        raise RuntimeError("Cycle detected")

    levels.append(ready)

    for n in ready:
        del remaining[n]

    for ps in remaining.values():
        ps.difference_update(ready)

run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

run_dir = RESULTS / run_id
run_dir.mkdir()

results = {}

print("=" * 78)
print(" OPENMIND DAG EXECUTION")
print("=" * 78)
print()
print(f"RUN ID             : {run_id}")
print(f"ACTIVE EXPERIMENTS : {len(ACTIVE)}")
print(f"LEVELS             : {len(levels)}")
print()

for level_no, level in enumerate(levels):

    print("=" * 78)
    print(f"LEVEL {level_no:02d}")
    print("=" * 78)

    for name in level:

        failed_parent = next(
            (
                p for p in parents[name]
                if results.get(p, {}).get("status") != "PASS"
            ),
            None,
        )

        if failed_parent:
            results[name] = {
                "status": "BLOCKED",
                "blocked_by": failed_parent,
            }

            print(f"BLOCKED  {name}")
            print(f"         dependency: {failed_parent}")
            continue

        path = EXP = ROOT / "experiments" / "model_fractal" / name

        started = time.time()

        print(f"RUN      {name}")

        try:
            proc = subprocess.run(
                [sys.executable, str(path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                timeout=600,
            )

            elapsed = time.time() - started

            status = "PASS" if proc.returncode == 0 else "FAIL"

            results[name] = {
                "status": status,
                "returncode": proc.returncode,
                "seconds": round(elapsed, 3),
                "stdout": proc.stdout[-10000:],
                "stderr": proc.stderr[-10000:],
            }

            print(
                f"{status:<8} {name:<55} "
                f"{elapsed:8.2f}s"
            )

        except subprocess.TimeoutExpired as e:

            elapsed = time.time() - started

            results[name] = {
                "status": "TIMEOUT",
                "seconds": round(elapsed, 3),
                "stdout": str(e.stdout)[-10000:],
                "stderr": str(e.stderr)[-10000:],
            }

            print(
                f"TIMEOUT  {name:<55} "
                f"{elapsed:8.2f}s"
            )

    print()

summary = defaultdict(int)

for result in results.values():
    summary[result["status"]] += 1

report = {
    "run_id": run_id,
    "levels": len(levels),
    "active": len(ACTIVE),
    "excluded": len(EXCLUDED),
    "summary": dict(summary),
    "results": results,
}

out = run_dir / "run.json"
out.write_text(json.dumps(report, indent=2))

print("=" * 78)
print(" DAG EXECUTION SUMMARY")
print("=" * 78)

for k in sorted(summary):
    print(f"{k:<12} {summary[k]}")

print()
print(f"Saved: {out.relative_to(ROOT)}")
