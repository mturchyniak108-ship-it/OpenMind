import json
import math
from pathlib import Path

INPUT = Path(
    "experiments/model_fractal/transition_recurrence_v7.json"
)

OUTPUT = Path(
    "experiments/model_fractal/transition_periodicity_v8.json"
)

EPS = 1e-12

d = json.loads(INPUT.read_text())

transitions = d["similarity_matrix"]
n = len(transitions)

# ----------------------------------------------------------------------
# Convert transition-pair similarity matrix into separation profiles
# ----------------------------------------------------------------------

separation_profiles = {}

for separation in range(1, n):

    values = []

    for i in range(n - separation):

        values.append(
            float(
                transitions[i][i + separation]
            )
        )

    separation_profiles[str(separation)] = values


# ----------------------------------------------------------------------
# Summary statistics by separation
# ----------------------------------------------------------------------

separation_summary = []

for separation in range(1, n):

    values = separation_profiles[str(separation)]

    if not values:
        continue

    mean = sum(values) / len(values)

    rms = math.sqrt(
        sum(x * x for x in values)
        / len(values)
    )

    max_value = max(values)

    min_value = min(values)

    separation_summary.append(
        {
            "separation": separation,
            "count": len(values),
            "mean": mean,
            "rms": rms,
            "max": max_value,
            "min": min_value,
        }
    )


# ----------------------------------------------------------------------
# Autocorrelation-style signal
#
# Use RMS of similarity at each separation.
# This avoids allowing positive and negative recurrence
# to cancel completely.
# ----------------------------------------------------------------------

signal = [
    item["rms"]
    for item in separation_summary
]


def correlation(a, b):

    if len(a) != len(b) or not a:
        return 0.0

    ma = sum(a) / len(a)
    mb = sum(b) / len(b)

    numerator = sum(
        (x - ma) * (y - mb)
        for x, y in zip(a, b)
    )

    da = math.sqrt(
        sum((x - ma) ** 2 for x in a)
    )

    db = math.sqrt(
        sum((y - mb) ** 2 for y in b)
    )

    if da <= EPS or db <= EPS:
        return 0.0

    return numerator / (da * db)


# ----------------------------------------------------------------------
# Test candidate periods
# ----------------------------------------------------------------------

period_candidates = []

for period in range(1, len(signal)):

    a = signal[:-period]
    b = signal[period:]

    period_candidates.append(
        {
            "period": period,
            "correlation": correlation(a, b),
        }
    )


period_candidates.sort(
    key=lambda x: x["correlation"],
    reverse=True,
)


# ----------------------------------------------------------------------
# Direct recurrence peaks
# ----------------------------------------------------------------------

recurrence_peaks = sorted(
    separation_summary,
    key=lambda x: x["max"],
    reverse=True,
)


# ----------------------------------------------------------------------
# RMS peaks
# ----------------------------------------------------------------------

rms_peaks = sorted(
    separation_summary,
    key=lambda x: x["rms"],
    reverse=True,
)


result = {
    "schema":
        "openmind.transition_periodicity.v8",

    "source":
        str(INPUT),

    "transition_count":
        n,

    "separation_summary":
        separation_summary,

    "period_candidates":
        period_candidates,

    "recurrence_peaks":
        recurrence_peaks,

    "rms_peaks":
        rms_peaks,
}


OUTPUT.write_text(
    json.dumps(
        result,
        indent=2
    )
)


print("=" * 72)
print(" OPENMIND / TRANSITION PERIODICITY V8")
print("=" * 72)

print()
print(f"Transitions: {n}")

print()
print("=== STRONGEST SEPARATION RECURRENCES ===")

for item in recurrence_peaks[:10]:

    print(
        f"ΔL={item['separation']:2d} "
        f"mean={item['mean']:.8f} "
        f"rms={item['rms']:.8f} "
        f"max={item['max']:.8f}"
    )


print()
print("=== STRONGEST RMS SCALES ===")

for item in rms_peaks[:10]:

    print(
        f"ΔL={item['separation']:2d} "
        f"rms={item['rms']:.8f} "
        f"mean={item['mean']:.8f}"
    )


print()
print("=== CANDIDATE PERIODS ===")

for item in period_candidates[:10]:

    print(
        f"period={item['period']:2d} "
        f"correlation={item['correlation']:.8f}"
    )


print()
print(f"Output: {OUTPUT}")

print()
print("TRANSITION PERIODICITY COMPLETE")
