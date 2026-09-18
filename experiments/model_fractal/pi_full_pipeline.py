import numpy as np
from hybrid_weighted import weighted_hybrid

# ============================================================
# 1. LOAD LARGE π PREFIX (10,000 DIGITS)
# ============================================================

# You can replace this with a larger file later if you want.
with open("pi_10000.txt", "r") as f:
    PI_REF = f.read().strip()

digits = [int(c) for c in PI_REF if c.isdigit()]


# ============================================================
# 2. BUILD TRANSITION MODEL
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


# ============================================================
# 3. HYBRID ATTRACTOR WEIGHTING
# ============================================================

def hybrid_digit_weights():
    # Use semantic‑dominant hybrid (w=0.8)
    h = weighted_hybrid(0.8)

    # Basin stats for weighting
    xs = np.array([p.x for p in h["strand_a"]])
    ys = np.array([p.y for p in h["strand_a"]])

    # Map digits 0–9 to weights using normalized attractor geometry
    weights = np.zeros(10)

    for d in range(10):
        # simple stable mapping: digit → attractor energy
        idx = d * (len(xs) // 10)
        energy = abs(xs[idx]) + abs(ys[idx])
        weights[d] = 1.0 / (1.0 + energy)

    # normalize
    weights /= weights.sum()
    return weights


def stabilize_probs(probs, weights):
    p = probs * weights
    p /= p.sum()
    return p


# ============================================================
# 4. RUN FULL PIPELINE
# ============================================================

if __name__ == "__main__":
    print("\n=== Building Transition Model ===")
    M = build_transition_matrix(digits)

    print("\n=== Verifying Against Known π Digits ===")
    correct = 0
    total = len(digits) - 1

    for i in range(total):
        pred, _ = predict_next_digit(M, digits[i])
        if pred == digits[i + 1]:
            correct += 1

    accuracy = correct / total
    print(f"Total transitions tested: {total}")
    print(f"Correct predictions: {correct}")
    print(f"Accuracy: {accuracy:.4f}")

    print("\n=== Hybrid Stabilization ===")
    weights = hybrid_digit_weights()
    print(f"Hybrid weights: {weights}")

    print("\n=== π + 1 Candidate Digit (Stabilized) ===")
    last = digits[-1]
    raw_candidate, raw_probs = predict_next_digit(M, last)
    stable_probs = stabilize_probs(raw_probs, weights)
    stable_candidate = int(np.argmax(stable_probs))

    print(f"Last known digit: {last}")
    print(f"Raw candidate: {raw_candidate}")
    print(f"Stabilized candidate: {stable_candidate}")
    print(f"Raw probabilities: {raw_probs}")
    print(f"Stabilized probabilities: {stable_probs}")
