import time
import numpy as np
from mpmath import mp
from hybrid_weighted import weighted_hybrid

# ============================================================
# Load known π prefix (1000 digits)
# ============================================================

with open("pi_100000.txt", "r") as f:
    PI_REF = f.read().strip()

digits = [int(c) for c in PI_REF if c.isdigit()]


# ============================================================
# Science-grade π using mpmath (proven math library)
# ============================================================

def compute_pi_mpmath(n):
    mp.dps = n + 5  # FIXED: correct mpmath precision setting
    return str(mp.pi)


def verify_prefix(computed, reference):
    L = min(len(computed), len(reference))
    return computed[:L] == reference[:L]


def benchmark_mpmath(digit_list):
    results = []
    for n in digit_list:
        t0 = time.time()
        pi_val = compute_pi_mpmath(n)
        dt = time.time() - t0

        ok = verify_prefix(pi_val, PI_REF)
        results.append((n, dt, ok))
    return results


# ============================================================
# Fractal-based π predictor (MAF/PWF hybrid)
# ============================================================

def build_transition_matrix(digits):
    M = np.zeros((10, 10), dtype=float)
    for a, b in zip(digits[:-1], digits[1:]):
        M[a, b] += 1
    row_sums = M.sum(axis=1)
    for i in range(10):
        if row_sums[i] > 0:
            M[i] /= row_sums[i]
    return M


def predict_next_digit(M, last_digit):
    probs = M[last_digit]
    return int(np.argmax(probs)), probs


def hybrid_digit_weights():
    h = weighted_hybrid(0.8)
    xs = np.array([p.x for p in h["strand_a"]])
    ys = np.array([p.y for p in h["strand_a"]])
    weights = np.zeros(10)
    for d in range(10):
        idx = d * (len(xs) // 10)
        energy = abs(xs[idx]) + abs(ys[idx])
        weights[d] = 1.0 / (1.0 + energy)
    weights /= weights.sum()
    return weights


def stabilize_probs(probs, weights):
    p = probs * weights
    p /= p.sum()
    return p


def benchmark_fractal_predictor():
    M = build_transition_matrix(digits)
    correct = 0
    total = len(digits) - 1

    for i in range(total):
        pred, _ = predict_next_digit(M, digits[i])
        if pred == digits[i + 1]:
            correct += 1

    accuracy = correct / total

    last = digits[-1]
    raw_candidate, raw_probs = predict_next_digit(M, last)
    weights = hybrid_digit_weights()
    stable_probs = stabilize_probs(raw_probs, weights)
    stable_candidate = int(np.argmax(stable_probs))

    return accuracy, raw_candidate, stable_candidate


# ============================================================
# Run full benchmark
# ============================================================

if __name__ == "__main__":
    print("\n=== Science-grade π Benchmark (mpmath) ===")
    sci_results = benchmark_mpmath([100, 500, 1000])

    for n, dt, ok in sci_results:
        print(f"Digits={n}, time={dt:.6f}s, verified={ok}")

    print("\n=== Fractal-based Predictor Benchmark ===")
    accuracy, raw_cand, stable_cand = benchmark_fractal_predictor()

    print(f"Transition accuracy: {accuracy:.4f}")
    print(f"Raw π+1 candidate: {raw_cand}")
    print(f"Stabilized π+1 candidate: {stable_cand}")

    print("\n=== Comparison Summary ===")
    print("mpmath: exact, proven, deterministic")
    print(f"Fractal predictor accuracy: {accuracy:.4f}")
    print(f"Fractal stabilized π+1: {stable_cand}")
