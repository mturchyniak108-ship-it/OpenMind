import numpy as np

# Known prefix of pi (1000 digits)
PI_REF = (
    "3."
    "14159265358979323846264338327950288419716939937510"
    "58209749445923078164062862089986280348253421170679"
    "82148086513282306647093844609550582231725359408128"
    "48111745028410270193852110555964462294895493038196"
    "44288109756659334461284756482337867831652712019091"
    "45648566923460348610454326648213393607260249141273"
    "72458700660631558817488152092096282925409171536436"
    "78925903600113305305488204665213841469519415116094"
    "33057270365759591953092186117381932611793105118548"
    "07446237996274956735188575272489122793818301194912"
)

# Strip "3."
digits = [int(c) for c in PI_REF if c.isdigit()]


def build_transition_matrix(digits):
    M = np.zeros((10, 10), dtype=float)

    for a, b in zip(digits[:-1], digits[1:]):
        M[a, b] += 1

    # Normalize rows
    row_sums = M.sum(axis=1)
    for i in range(10):
        if row_sums[i] > 0:
            M[i] /= row_sums[i]

    return M


def predict_next_digit(M, last_digit):
    probs = M[last_digit]
    return int(np.argmax(probs)), probs


if __name__ == "__main__":
    M = build_transition_matrix(digits)

    # Step 1 — Verification against known digits
    correct = 0
    total = len(digits) - 1

    for i in range(total):
        pred, _ = predict_next_digit(M, digits[i])
        if pred == digits[i + 1]:
            correct += 1

    accuracy = correct / total

    print(f"\n=== Verification Against Known π Digits ===")
    print(f"Total transitions tested: {total}")
    print(f"Correct predictions: {correct}")
    print(f"Accuracy: {accuracy:.4f}")

    # Step 2 — Generate candidate next digit beyond known prefix
    last = digits[-1]
    candidate, probs = predict_next_digit(M, last)

    print(f"\n=== π + 1 Candidate Digit ===")
    print(f"Last known digit: {last}")
    print(f"Candidate next digit: {candidate}")
    print(f"Probability distribution: {probs}")
