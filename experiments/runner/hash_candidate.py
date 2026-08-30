from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[2]

spec = json.loads(
    (ROOT / "results/production_candidate_v1.json").read_text()
)

files = spec["spine"]

manifest = {}

for name in files:
    path = ROOT / "experiments" / "model_fractal" / name

    if not path.exists():
        raise FileNotFoundError(path)

    manifest[name] = {
        "sha256": hashlib.sha256(
            path.read_bytes()
        ).hexdigest(),
        "bytes": path.stat().st_size
    }

out = ROOT / "results/production_candidate_v1_hash.json"

out.write_text(
    json.dumps(manifest, indent=2)
)

print("=" * 78)
print(" OPENMIND CANDIDATE V1 FROZEN")
print("=" * 78)
print()
print(f"COMPONENTS : {len(files)}")
print(f"MANIFEST   : {out}")
