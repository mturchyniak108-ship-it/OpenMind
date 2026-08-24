#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys
import time
import json
import os
import re

ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / "experiments" / "model_fractal"
RESULTS = ROOT / "results" / "experiment_runs"
RESULTS.mkdir(parents=True, exist_ok=True)

TIMEOUT = int(os.environ.get("OPENMIND_EXPERIMENT_TIMEOUT", "300"))

files = sorted(
    p for p in EXP.iterdir()
    if p.is_file()
    and p.suffix in {".py", ".cpp"}
    and p.name != "__init__.py"
)

def classify(name):
    n = name.lower()

    if "reference" in n or "backup" in n or "snapshot" in n or "_work" in n:
        return "ARCHIVE_VARIANT"
    if n.startswith("geometry_scaling"):
        return "GEOMETRY_SCALING"
    if n.startswith(("geometry_", "canonical_lattice", "closed_curve",
                     "crystal_", "fractal_renormalization",
                     "lattice_", "material_", "motif_", "normalized_geometry",
                     "null_model", "periodicity_", "spatial_null",
                     "structural_", "symmetry_", "topology_", "unit_cell")):
        return "GEOMETRY"
    if n.startswith(("q8_",)):
        return "Q8"
    if n.startswith(("transition_",)):
        return "TRANSITION"
    if n.startswith(("recurrence", "activation_recurrence")):
        return "RECURRENCE"
    if n.startswith(("pi",)):
        return "PI"
    if "maf" in n:
        return "MAF"
    if n.startswith(("gguf_", "inspect_gguf")):
        return "GGUF"
    if n.startswith(("tie_",)):
        return "TIE"
    if n in {"visualize_hybrid_basin.py"}:
        return "UTILITY"
    return "OTHER"

archive = {"ARCHIVE_VARIANT", "UTILITY"}

print("=" * 60)
print(" OPENMIND EXPERIMENT EXECUTION")
print("=" * 60)
print(f"ROOT: {ROOT}")
print(f"TIMEOUT: {TIMEOUT}s")
print(f"TOTAL FILES: {len(files)}")
print()

summary = []
counts = {}

for p in files:
    cat = classify(p.name)
    counts[cat] = counts.get(cat, 0) + 1

    if cat in archive:
        status = "SKIPPED"
        rc = None
        elapsed = 0.0
        output = "archive/utility"
        print(f"[SKIP] {p.name}")
    elif p.suffix == ".cpp":
        status = "SKIPPED"
        rc = None
        elapsed = 0.0
        output = "C++ source requires separate compilation harness"
        print(f"[SKIP] {p.name} (C++)")
    else:
        print(f"[RUN ] {p.name}", flush=True)

        start = time.monotonic()

        try:
            proc = subprocess.run(
                [sys.executable, str(p)],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=TIMEOUT,
                env=os.environ.copy(),
            )

            rc = proc.returncode
            elapsed = time.monotonic() - start
            output = proc.stdout

            status = "PASS" if rc == 0 else "FAIL"

        except subprocess.TimeoutExpired as e:
            rc = None
            elapsed = time.monotonic() - start
            status = "TIMEOUT"
            output = (e.stdout or "") if isinstance(e.stdout, str) else ""

        except Exception as e:
            rc = None
            elapsed = time.monotonic() - start
            status = "ERROR"
            output = repr(e)

        logfile = RESULTS / f"{p.stem}.log"
        logfile.write_text(output or "", errors="replace")

        print(
            f"      {status:<8} "
            f"{elapsed:8.2f}s "
            f"rc={rc}",
            flush=True,
        )

    summary.append({
        "experiment": p.name,
        "category": cat,
        "status": status,
        "returncode": rc,
        "seconds": round(elapsed, 3),
        "log": str((RESULTS / f"{p.stem}.log").relative_to(ROOT))
        if cat not in archive and p.suffix == ".py"
        else None,
    })

report = {
    "total_files": len(files),
    "categories": counts,
    "results": summary,
    "timeout_seconds": TIMEOUT,
}

(ROOT / "results" / "experiment_summary.json").write_text(
    json.dumps(report, indent=2)
)

print()
print("=" * 60)
print(" EXECUTION SUMMARY")
print("=" * 60)

for status in ["PASS", "FAIL", "TIMEOUT", "ERROR", "SKIPPED"]:
    items = [x for x in summary if x["status"] == status]
    print(f"{status:<10} {len(items)}")

print()
print("RESULTS:")
print("  results/experiment_summary.json")
print("  results/experiment_runs/*.log")
print("=" * 60)
