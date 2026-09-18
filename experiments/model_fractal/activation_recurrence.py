import json
import math
import struct
from pathlib import Path

import numpy as np

MODEL = Path.home() / "qwen2.5-coder-q8_0.gguf"

# Candidate recurrences discovered by recurrence_stability_v2.py
PAIRS = [
    (6, 14),
    (8, 14),
    (12, 18),
    (5, 15),
    (7, 11),
    (7, 18),
]

# Control pairs with comparable depth gaps
CONTROLS = [
    (3, 11),
    (10, 18),
    (12, 20),
    (4, 12),
    (9, 17),
    (13, 21),
]

# Deterministic probe set.
PROBES = [
    "The quick brown fox jumps over the lazy dog.",
    "Explain how a compiler transforms source code into machine instructions.",
    "A system should distinguish evidence from inference and uncertainty.",
    "Write a Python function that calculates Fibonacci numbers efficiently.",
    "Artificial intelligence combines statistical inference with computation.",
    "The purpose of this experiment is to measure internal representation similarity.",
    "Security requires authentication, confidentiality, integrity, and auditability.",
    "A graph consists of nodes connected by weighted relationships.",
]


def cosine(a, b):
    denom = np.linalg.norm(a) * np.linalg.norm(b)

    if denom == 0:
        return 0.0

    return float(np.dot(a, b) / denom)


def relative_distance(a, b):
    denom = max(
        float(np.linalg.norm(a)),
        float(np.linalg.norm(b)),
        1e-12,
    )

    return float(np.linalg.norm(a - b) / denom)


def stats(a, b):
    return {
        "relative": relative_distance(a, b),
        "cosine": cosine(a, b),
        "rms_a": float(np.sqrt(np.mean(a * a))),
        "rms_b": float(np.sqrt(np.mean(b * b))),
    }


# ------------------------------------------------------------
# LOCATE LLAMA CPP
# ------------------------------------------------------------

ROOT = Path.home() / "OpenMind"
LLAMA = ROOT / "llama.cpp"

CANDIDATES = [
    LLAMA / "build-vulkan" / "bin" / "llama-cli",
    LLAMA / "build-vulkan" / "bin" / "llama-run",
    LLAMA / "build" / "bin" / "llama-cli",
    LLAMA / "build" / "bin" / "llama-run",
]

EXECUTABLE = None

for candidate in CANDIDATES:
    if candidate.exists():
        EXECUTABLE = candidate
        break

if EXECUTABLE is None:
    raise SystemExit(
        "Could not locate llama.cpp executable.\n"
        "Checked:\n"
        + "\n".join(str(x) for x in CANDIDATES)
    )


print("=" * 72)
print(" OPENMIND / ACTIVATION RECURRENCE")
print("=" * 72)
print()
print(f"Model:     {MODEL}")
print(f"Executable:{EXECUTABLE}")
print(f"Probes:    {len(PROBES)}")
print()
print("Candidate recurrence pairs:")
for a, b in PAIRS:
    print(f"  L{a:02d} <-> L{b:02d}")

print()
print("Control pairs:")
for a, b in CONTROLS:
    print(f"  L{a:02d} <-> L{b:02d}")

print()
print("=" * 72)
print(" IMPORTANT")
print("=" * 72)
print()
print(
    "This stage requires hidden-state extraction from llama.cpp."
)
print(
    "If the installed executable does not expose hidden states,"
)
print(
    "the script will stop rather than fabricate activation data."
)
print()


# ------------------------------------------------------------
# CHECK CLI CAPABILITIES
# ------------------------------------------------------------

import subprocess

try:
    help_output = subprocess.run(
        [str(EXECUTABLE), "--help"],
        capture_output=True,
        text=True,
        timeout=10,
    )

    help_text = (
        help_output.stdout
        + "\n"
        + help_output.stderr
    )

except Exception as exc:
    raise SystemExit(
        f"Unable to inspect llama.cpp executable: {exc}"
    )


hidden_keywords = [
    "embeddings",
    "embedding",
    "injection",
]

available = [
    x for x in hidden_keywords
    if x.lower() in help_text.lower()
]

print(
    "Detected relevant CLI capabilities:",
    ", ".join(available) if available else "none",
)

print()


# ------------------------------------------------------------
# CURRENT LIMITATION
# ------------------------------------------------------------

print("=" * 72)
print(" ACTIVATION EXTRACTION STATUS")
print("=" * 72)
print()

print(
    "The current llama.cpp CLI generally exposes final embeddings,"
)
print(
    "but arbitrary intermediate transformer hidden states require"
)
print(
    "the llama.cpp C/C++ API or a custom instrumentation layer."
)

print()
print("Therefore this experiment will NOT substitute final embeddings")
print("for intermediate layer activations.")
print()

print("NEXT REQUIRED COMPONENT:")
print()
print("  OpenMind native activation probe")
print()
print("Target:")
print()
print("  prompt")
print("    -> tokenizer")
print("    -> llama_decode()")
print("    -> transformer evaluation")
print("    -> capture hidden state at selected layer")
print("    -> L2 normalize")
print("    -> compare recurrence pairs")
print()

print("=" * 72)
print(" ACTIVATION RECURRENCE TEST DEFERRED")
print("=" * 72)
print()
print(
    "Reason: intermediate activations cannot be inferred reliably "
    "from the GGUF weight file alone."
)
print()
print(
    "The weight-level recurrence results remain valid as structural "
    "candidates, but behavioral validation requires native instrumentation."
)
