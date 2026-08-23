import time
from decimal import Decimal, getcontext

# Known prefix of pi (for accuracy checking)
PI_REF = (
    "3."
    "14159265358979323846264338327950288419716939937510"
    "58209749445923078164062862089986280348253421170679"
    "82148086513282306647093844609550582231725359408128"
)


def compute_pi_chudnovsky(digits: int) -> str:
    # Set precision slightly above requested digits
    getcontext().prec = digits + 5

    C = 426880 * Decimal(10005).sqrt()
    K = 6
    M = 1
    L = 13591409
    X = 1
    S = L

    for i in range(1, digits // 14 + 2):
        M = (M * (K**3 - 16*K)) // (i**3)
        K += 12
        L += 545140134
        X *= -262537412640768000
        S += (Decimal(M * L) / X)

    pi = C / S
    s = format(pi, f".{digits}f")
    return s


def benchmark(digits_list):
    for n in digits_list:
        t0 = time.time()
        s = compute_pi_chudnovsky(n)
        dt = time.time() - t0

        # accuracy check: compare against known prefix
        ref = PI_REF[:len(s)]
        ok = (s == ref)

        print(f"\n=== π Benchmark: {n} digits ===")
        print(f"time: {dt:.3f}s")
        print(f"len: {len(s)} chars")
        print(f"matches known prefix: {ok}")
        if not ok:
            print("first mismatch:")
            for i, (a, b) in enumerate(zip(s, ref)):
                if a != b:
                    print(f"  index {i}: got {a}, expected {b}")
                    break


if __name__ == "__main__":
    benchmark([50, 100, 200])
