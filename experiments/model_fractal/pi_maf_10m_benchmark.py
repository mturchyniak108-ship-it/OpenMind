import time
import os
import random
import numpy as np
from mpmath import mp

PI_FILE = "pi_10M.txt"
N_DIGITS = 10_000_000
N_LOOKUPS = 100_000


def generate_pi_file():
    print(f"Generating {N_DIGITS} digits of π with mpmath (this may take a while)...")
    mp.dps = N_DIGITS + 10
    pi_val = str(mp.pi)
    with open(PI_FILE, "w") as f:
        f.write(pi_val)
    print(f"Saved π to {PI_FILE}")


def load_pi_digits():
    print(f"Loading π digits from {PI_FILE}...")
    with open(PI_FILE, "r") as f:
        s = f.read().strip()
    digits = [int(c) for c in s if c.isdigit()]
    if len(digits) < N_DIGITS:
        print(f"Warning: only {len(digits)} digits loaded, expected {N_DIGITS}")
    return np.array(digits, dtype=np.uint8)


def build_transition_matrix(digits):
    print("Building transition matrix (MAF core)...")
    M = np.zeros((10, 10), dtype=float)
    for a, b in zip(digits[:-1], digits[1:]):
        M[a, b] += 1
    row_sums = M.sum(axis=1)
    for i in range(10):
        if row_sums[i] > 0:
            M[i] /= row_sums[i]
    return M


def benchmark_naive_lookup():
    print("\nBenchmark: naive lookup (file read per query)")
    t0 = time.time()
    for _ in range(N_LOOKUPS):
        idx = random.randint(0, N_DIGITS - 1)
        with open(PI_FILE, "r") as f:
            s = f.read().strip()
        # crude: scan to digit index
        count = 0
        for c in s:
            if c.isdigit():
                if count == idx:
                    _ = c
                    break
                count += 1
    dt = time.time() - t0
    print(f"Naive lookup time for {N_LOOKUPS} queries: {dt:.3f}s")
    return dt


def benchmark_maf_lookup(digits):
    print("\nBenchmark: MAF lookup (in-memory array)")
    t0 = time.time()
    for _ in range(N_LOOKUPS):
        idx = random.randint(0, len(digits) - 1)
        _ = digits[idx]
    dt = time.time() - t0
    print(f"MAF lookup time for {N_LOOKUPS} queries: {dt:.3f}s")
    return dt


if __name__ == "__main__":
    if not os.path.exists(PI_FILE):
        generate_pi_file()

    digits = load_pi_digits()
    M = build_transition_matrix(digits)

    t_naive = benchmark_naive_lookup()
    t_maf = benchmark_maf_lookup(digits)

    speedup = (t_naive / t_maf) if t_maf > 0 else 0.0

    print("\n=== 10M-digit MAF Benchmark Summary ===")
    print(f"Naive lookup total time: {t_naive:.3f}s")
    print(f"MAF lookup total time:   {t_maf:.3f}s")
    print(f"Speedup (naive / MAF):   {speedup:.2f}x")
