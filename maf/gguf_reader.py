import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "llama.cpp" / "gguf-py"))

import gguf


def load_model(path):
    return gguf.GGUFReader(str(path))


def tensor_summary(reader):
    result = []

    for t in reader.tensors:
        result.append({
            "name": t.name,
            "shape": tuple(int(x) for x in t.shape),
            "type": int(t.tensor_type),
            "bytes": int(t.data.nbytes),
        })

    return result
