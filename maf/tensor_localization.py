from pathlib import Path
import re
import numpy as np

from maf.divergence import load_model, decode_tensor


MODEL = (
    Path.home()
    / "qwen2.5-coder-q8_0.gguf"
)

TARGETS = [
    (14, 15, "attn_k.bias"),
    (21, 22, "attn_k.bias"),
    (23, 24, "attn_q.bias"),
    (12, 13, "attn_v.bias"),
    (22, 23, "attn_v.bias"),
]


def flatten(x):
    return np.asarray(x, dtype=np.float64).reshape(-1)


def analyze(previous, current, top_n=10):
    a = flatten(previous)
    b = flatten(current)

    if a.shape != b.shape:
        raise ValueError(
            f"Shape mismatch: {a.shape} vs {b.shape}"
        )

    delta = b - a
    abs_delta = np.abs(delta)

    # Relative element change.
    denom = np.maximum(np.abs(a), 1e-12)
    relative_delta = abs_delta / denom

    changed = abs_delta > 0
    changed_count = int(np.count_nonzero(changed))

    l2 = float(np.linalg.norm(delta))

    return {
        "size": len(a),
        "mean_previous": float(np.mean(a)),
        "mean_current": float(np.mean(b)),
        "std_previous": float(np.std(a)),
        "std_current": float(np.std(b)),
        "min_previous": float(np.min(a)),
        "max_previous": float(np.max(a)),
        "min_current": float(np.min(b)),
        "max_current": float(np.max(b)),
        "l2_delta": l2,
        "changed_count": changed_count,
        "changed_percent": (
            100.0 * changed_count / len(a)
        ),
        "top_abs": np.argsort(abs_delta)[-top_n:][::-1],
        "top_relative": np.argsort(relative_delta)[-top_n:][::-1],
        "delta": delta,
        "abs_delta": abs_delta,
        "relative_delta": relative_delta,
        "previous": a,
        "current": b,
    }


def main():
    reader = load_model(MODEL)

    tensors = {
        t.name: t
        for t in reader.tensors
    }

    decoded = {}

    pattern = re.compile(r"blk\.(\d+)\.(.+)")

    for name, tensor in tensors.items():
        match = pattern.match(name)

        if not match:
            continue

        layer = int(match.group(1))
        component = match.group(2)

        decoded.setdefault(layer, {})[
            component
        ] = decode_tensor(tensor)

    print("=" * 78)
    print(" MAF / TENSOR ELEMENT LOCALIZATION")
    print("=" * 78)
    print("Model:", MODEL)
    print()

    for left, right, component in TARGETS:
        print("-" * 78)
        print(
            f"TRANSITION {left:02d} -> {right:02d} | "
            f"{component}"
        )
        print("-" * 78)

        a = decoded[left][component]
        b = decoded[right][component]

        result = analyze(a, b)

        print(f"Elements          : {result['size']}")
        print(
            f"Mean              : "
            f"{result['mean_previous']:.8e} -> "
            f"{result['mean_current']:.8e}"
        )
        print(
            f"STD               : "
            f"{result['std_previous']:.8e} -> "
            f"{result['std_current']:.8e}"
        )
        print(
            f"Range             : "
            f"[{result['min_previous']:.8e}, "
            f"{result['max_previous']:.8e}] -> "
            f"[{result['min_current']:.8e}, "
            f"{result['max_current']:.8e}]"
        )
        print(
            f"Raw delta L2      : "
            f"{result['l2_delta']:.8e}"
        )
        print(
            f"Changed elements  : "
            f"{result['changed_count']} / "
            f"{result['size']} "
            f"({result['changed_percent']:.4f}%)"
        )

        print()
        print("TOP ABSOLUTE ELEMENT DELTAS")
        print("index        previous          current           delta")

        for idx in result["top_abs"]:
            print(
                f"{idx:6d}  "
                f"{result['previous'][idx]: .8e}  "
                f"{result['current'][idx]: .8e}  "
                f"{result['delta'][idx]: .8e}"
            )

        print()
        print("TOP RELATIVE ELEMENT DELTAS")
        print("index        previous          current           relative")

        for idx in result["top_relative"]:
            print(
                f"{idx:6d}  "
                f"{result['previous'][idx]: .8e}  "
                f"{result['current'][idx]: .8e}  "
                f"{result['relative_delta'][idx]: .8e}"
            )

        print()

    print("=" * 78)
    print(" MAF / TENSOR ELEMENT LOCALIZATION COMPLETE")
    print("=" * 78)


if __name__ == "__main__":
    main()
