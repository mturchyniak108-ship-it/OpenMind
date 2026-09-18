import json
import math
import random
from pathlib import Path

INPUT = Path(
    "experiments/model_fractal/normalized_geometry_v10.json"
)

OUTPUT = Path(
    "experiments/model_fractal/closed_curve_spectrum_v18.json"
)

EPS = 1e-12

d = json.loads(INPUT.read_text())

raw_points = d["layer_coordinates"]

points = [
    (
        float(p["x"]),
        float(p["y"]),
        float(p["z"]),
    )
    for p in raw_points
]

print("=" * 72)
print(" OPENMIND / CLOSED CURVE SPECTRUM V18")
print("=" * 72)

print()
print(f"Layers: {len(points)}")


# ----------------------------------------------------------------------
# Geometry helpers
# ----------------------------------------------------------------------

def sub(a, b):
    return tuple(
        x - y
        for x, y in zip(a, b)
    )


def add(a, b):
    return tuple(
        x + y
        for x, y in zip(a, b)
    )


def scale(v, s):
    return tuple(
        x * s
        for x in v
    )


def dot(a, b):
    return sum(
        x * y
        for x, y in zip(a, b)
    )


def norm(v):
    return math.sqrt(dot(v, v))


def distance(a, b):
    return norm(sub(a, b))


def centroid(values):
    return tuple(
        sum(p[k] for p in values) / len(values)
        for k in range(3)
    )


# ----------------------------------------------------------------------
# Close the curve explicitly
# ----------------------------------------------------------------------

closed = points + [points[0]]

segment_lengths = [
    distance(
        closed[i],
        closed[i + 1]
    )
    for i in range(len(closed) - 1)
]

total_length = sum(segment_lengths)

print()
print("=== CLOSED CURVE ===")
print(
    f"total arc length = {total_length:.10f}"
)

print(
    f"closure distance  = "
    f"{distance(points[0], points[-1]):.12e}"
)


# ----------------------------------------------------------------------
# Uniform arc-length resampling
# ----------------------------------------------------------------------

def resample_curve(values, count):

    closed_values = values + [values[0]]

    lengths = [
        distance(
            closed_values[i],
            closed_values[i + 1]
        )
        for i in range(len(values))
    ]

    cumulative = [0.0]

    for length in lengths:
        cumulative.append(
            cumulative[-1] + length
        )

    total = cumulative[-1]

    if total <= EPS:
        return [
            values[0]
            for _ in range(count)
        ]

    result = []

    for j in range(count):

        target = (
            total * j / count
        )

        index = 0

        while (
            index < len(lengths) - 1
            and cumulative[index + 1] < target
        ):
            index += 1

        left = cumulative[index]
        right = cumulative[index + 1]

        if right - left <= EPS:
            result.append(
                closed_values[index]
            )
            continue

        fraction = (
            (target - left)
            / (right - left)
        )

        a = closed_values[index]
        b = closed_values[index + 1]

        result.append(
            tuple(
                a[k]
                + fraction * (b[k] - a[k])
                for k in range(3)
            )
        )

    return result


SAMPLE_COUNT = 256

uniform_points = resample_curve(
    points,
    SAMPLE_COUNT
)


# ----------------------------------------------------------------------
# Center the curve
# ----------------------------------------------------------------------

center = centroid(uniform_points)

uniform_points = [
    sub(p, center)
    for p in uniform_points
]


# ----------------------------------------------------------------------
# Discrete Fourier transform
#
# We implement this directly so the experiment has no dependency on
# numpy/scipy being installed in Termux.
# ----------------------------------------------------------------------

def dft(values):

    n = len(values)

    result = []

    for k in range(n):

        real = 0.0
        imag = 0.0

        for j, value in enumerate(values):

            angle = (
                -2.0
                * math.pi
                * k
                * j
                / n
            )

            real += (
                value
                * math.cos(angle)
            )

            imag += (
                value
                * math.sin(angle)
            )

        result.append(
            complex(real, imag)
        )

    return result


xs = [
    p[0]
    for p in uniform_points
]

ys = [
    p[1]
    for p in uniform_points
]

zs = [
    p[2]
    for p in uniform_points
]

radial = [
    norm(p)
    for p in uniform_points
]


fx = dft(xs)
fy = dft(ys)
fz = dft(zs)
fr = dft(radial)


# ----------------------------------------------------------------------
# Spectral power
# ----------------------------------------------------------------------

def power(z):
    return z.real * z.real + z.imag * z.imag


spectra = {
    "x": [power(z) for z in fx],
    "y": [power(z) for z in fy],
    "z": [power(z) for z in fz],
    "radial": [power(z) for z in fr],
}


combined = []

for k in range(SAMPLE_COUNT):

    combined.append(
        (
            spectra["x"][k]
            + spectra["y"][k]
            + spectra["z"][k]
        )
    )


# ----------------------------------------------------------------------
# Normalize spectral power
# ----------------------------------------------------------------------

total_power = sum(
    combined[1:]
)

normalized_power = [
    0.0
    if total_power <= EPS
    else value / total_power
    for value in combined
]


# ----------------------------------------------------------------------
# Dominant frequencies
# ----------------------------------------------------------------------

frequency_power = [
    {
        "frequency": k,
        "power": normalized_power[k],
    }
    for k in range(
        1,
        SAMPLE_COUNT // 2
    )
]

ranked = sorted(
    frequency_power,
    key=lambda x: x["power"],
    reverse=True,
)


print()
print("=== DOMINANT FREQUENCIES ===")

for item in ranked[:15]:

    print(
        f"k={item['frequency']:3d} "
        f"power={item['power']:.8f}"
    )


# ----------------------------------------------------------------------
# Period-8 and harmonics
#
# Since 256 / 8 = 32, a period-8 motif corresponds to k=32.
# Its harmonics occur at 64, 96, ...
# ----------------------------------------------------------------------

fundamental = SAMPLE_COUNT // 8

harmonics = []

for multiplier in range(1, 5):

    k = fundamental * multiplier

    if k >= SAMPLE_COUNT // 2:
        break

    harmonics.append(
        {
            "harmonic": multiplier,
            "frequency": k,
            "power": normalized_power[k],
        }
    )


print()
print("=== PERIOD-8 SPECTRUM ===")

for h in harmonics:

    print(
        f"harmonic={h['harmonic']} "
        f"k={h['frequency']:3d} "
        f"power={h['power']:.8f}"
    )


period8_power = (
    harmonics[0]["power"]
    if harmonics
    else 0.0
)


# ----------------------------------------------------------------------
# Spectral concentration
# ----------------------------------------------------------------------

top10_power = sum(
    item["power"]
    for item in ranked[:10]
)

spectral_entropy = 0.0

for value in normalized_power[1:]:

    if value > EPS:

        spectral_entropy -= (
            value
            * math.log(value)
        )


max_entropy = math.log(
    max(1, len(normalized_power) - 1)
)

entropy_ratio = (
    spectral_entropy / max_entropy
    if max_entropy > EPS
    else 0.0
)


print()
print("=== SPECTRAL STRUCTURE ===")

print(
    f"period-8 power      = "
    f"{period8_power:.8f}"
)

print(
    f"top-10 concentration = "
    f"{top10_power:.8f}"
)

print(
    f"spectral entropy     = "
    f"{spectral_entropy:.8f}"
)

print(
    f"entropy ratio        = "
    f"{entropy_ratio:.8f}"
)


# ----------------------------------------------------------------------
# Axis agreement
# ----------------------------------------------------------------------

axis_period8 = {}

for axis in ("x", "y", "z"):

    axis_total = sum(
        spectra[axis][1:]
    )

    if axis_total <= EPS:

        value = 0.0

    else:

        value = (
            spectra[axis][fundamental]
            / axis_total
        )

    axis_period8[axis] = value


print()
print("=== AXIS PERIOD-8 POWER ===")

for axis, value in axis_period8.items():

    print(
        f"{axis}: {value:.8f}"
    )


# ----------------------------------------------------------------------
# Phase coherence at period 8
# ----------------------------------------------------------------------

phase_x = math.atan2(
    fx[fundamental].imag,
    fx[fundamental].real,
)

phase_y = math.atan2(
    fy[fundamental].imag,
    fy[fundamental].real,
)

phase_z = math.atan2(
    fz[fundamental].imag,
    fz[fundamental].real,
)


def phase_difference(a, b):

    d = abs(a - b)

    while d > math.pi:
        d = abs(d - 2.0 * math.pi)

    return d


phase_xy = phase_difference(
    phase_x,
    phase_y
)

phase_xz = phase_difference(
    phase_x,
    phase_z
)

phase_yz = phase_difference(
    phase_y,
    phase_z
)

phase_coherence = 1.0 - (
    (
        phase_xy
        + phase_xz
        + phase_yz
    )
    / (3.0 * math.pi)
)


print()
print("=== PERIOD-8 PHASE ===")

print(
    f"X phase = {phase_x:.8f}"
)

print(
    f"Y phase = {phase_y:.8f}"
)

print(
    f"Z phase = {phase_z:.8f}"
)

print(
    f"phase coherence = "
    f"{phase_coherence:.8f}"
)


# ----------------------------------------------------------------------
# Null model
#
# Randomly permute the arc-length-resampled points.
# Recalculate period-8 spectral concentration.
# ----------------------------------------------------------------------

random.seed(8)

NULL_TRIALS = 200

null_values = []

for trial in range(NULL_TRIALS):

    shuffled = uniform_points[:]

    random.shuffle(shuffled)

    sx = dft([
        p[0]
        for p in shuffled
    ])

    sy = dft([
        p[1]
        for p in shuffled
    ])

    sz = dft([
        p[2]
        for p in shuffled
    ])

    value = (
        power(sx[fundamental])
        + power(sy[fundamental])
        + power(sz[fundamental])
    )

    total = sum(
        power(sx[k])
        + power(sy[k])
        + power(sz[k])
        for k in range(1, SAMPLE_COUNT // 2)
    )

    if total > EPS:

        null_values.append(
            value / total
        )


null_mean = (
    sum(null_values)
    / len(null_values)
    if null_values
    else 0.0
)

null_std = math.sqrt(
    sum(
        (x - null_mean) ** 2
        for x in null_values
    )
    / len(null_values)
) if null_values else 0.0

if null_std > EPS:

    z_score = (
        period8_power
        - null_mean
    ) / null_std

else:

    z_score = 0.0


print()
print("=== NULL MODEL / PERIOD-8 SPECTRUM ===")

print(
    f"observed = {period8_power:.8f}"
)

print(
    f"null mean = {null_mean:.8f}"
)

print(
    f"null std  = {null_std:.8f}"
)

print(
    f"z-score   = {z_score:.8f}"
)


# ----------------------------------------------------------------------
# Classification
# ----------------------------------------------------------------------

if z_score >= 5.0 and phase_coherence >= 0.50:

    classification = (
        "STRONG_PERIODIC_SPECTRAL_STRUCTURE"
    )

elif z_score >= 3.0:

    classification = (
        "SIGNIFICANT_PERIODIC_SPECTRAL_STRUCTURE"
    )

elif z_score >= 2.0:

    classification = (
        "WEAK_PERIODIC_SPECTRAL_STRUCTURE"
    )

else:

    classification = (
        "NO_SIGNIFICANT_PERIODIC_SPECTRAL_STRUCTURE"
    )


print()
print("=== CLASSIFICATION ===")
print(classification)


# ----------------------------------------------------------------------
# Output
# ----------------------------------------------------------------------

result = {

    "schema":
        "openmind.closed_curve_spectrum.v18",

    "source":
        str(INPUT),

    "layer_count":
        len(points),

    "sample_count":
        SAMPLE_COUNT,

    "arc_length":
        total_length,

    "period8_frequency":
        fundamental,

    "dominant_frequencies":
        ranked[:20],

    "period8_harmonics":
        harmonics,

    "period8_power":
        period8_power,

    "top10_spectral_concentration":
        top10_power,

    "spectral_entropy":
        spectral_entropy,

    "spectral_entropy_ratio":
        entropy_ratio,

    "axis_period8_power":
        axis_period8,

    "phase":
        {
            "x": phase_x,
            "y": phase_y,
            "z": phase_z,
            "coherence": phase_coherence,
        },

    "null_model":
        {
            "trials": NULL_TRIALS,
            "mean": null_mean,
            "std": null_std,
            "z_score": z_score,
        },

    "classification":
        classification,
}


OUTPUT.write_text(
    json.dumps(
        result,
        indent=2
    )
)

print()
print(f"Output: {OUTPUT}")
print()
print("CLOSED CURVE SPECTRUM COMPLETE")
