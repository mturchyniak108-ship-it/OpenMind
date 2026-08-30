from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / "experiments" / "model_fractal"
RESULTS = ROOT / "results"

files = sorted(
    p for p in EXP.iterdir()
    if p.is_file() and p.suffix in {".py", ".json"}
)

manifest = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "experiment_count": len([p for p in files if p.suffix == ".py"]),
    "artifacts": {}
}

for p in files:
    h = hashlib.sha256(p.read_bytes()).hexdigest()

    manifest["artifacts"][str(p.relative_to(ROOT))] = {
        "sha256": h,
        "bytes": p.stat().st_size,
    }

out = RESULTS / "experimental_state_manifest.json"
out.write_text(json.dumps(manifest, indent=2))

print("=" * 78)
print(" OPENMIND EXPERIMENTAL STATE FREEZE")
print("=" * 78)
print()
print(f"PYTHON EXPERIMENTS : {manifest['experiment_count']}")
print(f"FILES HASHED       : {len(manifest['artifacts'])}")
print()
print(f"Saved: {out.relative_to(ROOT)}")
