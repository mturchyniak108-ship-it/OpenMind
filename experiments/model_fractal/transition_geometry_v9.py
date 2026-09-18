import json
import math
from pathlib import Path

INPUT = Path(
    "experiments/model_fractal/transition_field_v5.json"
)

OUTPUT = Path(
    "experiments/model_fractal/transition_geometry_v9.json"
)

EPS = 1e-12

d = json.loads(INPUT.read_text())
transitions = d["transitions"]

print("=" * 72)
print(" OPENMIND / TRANSITION GEOMETRY V9")
print("=" * 72)
print()
print(f"Transitions: {len(transitions)}")


# ----------------------------------------------------------------------
# Extract transition vectors
# ----------------------------------------------------------------------

vectors = [
    [float(x) for x in t["delta"]]
    for t in transitions
]

dimension = len(vectors[0])


# ----------------------------------------------------------------------
# Basic vector operations
# ----------------------------------------------------------------------

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def norm(a):
    return math.sqrt(dot(a, a))


def normalize(a):
    n = norm(a)

    if n <= EPS:
        return [0.0] * len(a)

    return [x / n for x in a]


def mat_vec(matrix, vector):
    return [
        sum(x * y for x, y in zip(row, vector))
        for row in matrix
    ]


# ----------------------------------------------------------------------
# Covariance matrix
# ----------------------------------------------------------------------

means = [
    sum(v[j] for v in vectors) / len(vectors)
    for j in range(dimension)
]

centered = [
    [v[j] - means[j] for j in range(dimension)]
    for v in vectors
]

covariance = [
    [
        sum(
            row[i] * row[j]
            for row in centered
        ) / len(centered)
        for j in range(dimension)
    ]
    for i in range(dimension)
]


# ----------------------------------------------------------------------
# Power iteration
# ----------------------------------------------------------------------

def principal_component(matrix, iterations=500):

    vector = [
        1.0 if i == 0 else 0.5
        for i in range(len(matrix))
    ]

    vector = normalize(vector)

    for _ in range(iterations):

        new_vector = mat_vec(
            matrix,
            vector
        )

        new_vector = normalize(new_vector)

        if norm([
            new_vector[i] - vector[i]
            for i in range(len(vector))
        ]) < 1e-10:
            break

        vector = new_vector

    eigenvalue = dot(
        vector,
        mat_vec(matrix, vector)
    )

    return eigenvalue, vector


# ----------------------------------------------------------------------
# Extract first three PCA directions with deflation
# ----------------------------------------------------------------------

working = [
    row[:]
    for row in covariance
]

components = []
eigenvalues = []

for _ in range(min(3, dimension)):

    eigenvalue, component = principal_component(
        working
    )

    eigenvalues.append(eigenvalue)
    components.append(component)

    for i in range(dimension):
        for j in range(dimension):
            working[i][j] -= (
                eigenvalue
                * component[i]
                * component[j]
            )


# ----------------------------------------------------------------------
# Project transition vectors into 3-D
# ----------------------------------------------------------------------

transition_coordinates = []

for index, vector in enumerate(centered):

    coordinates = [
        dot(vector, component)
        for component in components
    ]

    transition_coordinates.append(
        {
            "transition": index,
            "from_layer": transitions[index]["from_layer"],
            "to_layer": transitions[index]["to_layer"],
            "x": coordinates[0],
            "y": coordinates[1],
            "z": coordinates[2],
        }
    )


# ----------------------------------------------------------------------
# Reconstruct layer coordinates by cumulative transition motion
# ----------------------------------------------------------------------

layers = [
    {
        "layer": 0,
        "x": 0.0,
        "y": 0.0,
        "z": 0.0,
    }
]

x = y = z = 0.0

for coordinate in transition_coordinates:

    x += coordinate["x"]
    y += coordinate["y"]
    z += coordinate["z"]

    layers.append(
        {
            "layer": coordinate["to_layer"],
            "x": x,
            "y": y,
            "z": z,
        }
    )


# ----------------------------------------------------------------------
# Pairwise distances
# ----------------------------------------------------------------------

distances = []

for i in range(len(layers)):

    for j in range(i + 1, len(layers)):

        dx = layers[i]["x"] - layers[j]["x"]
        dy = layers[i]["y"] - layers[j]["y"]
        dz = layers[i]["z"] - layers[j]["z"]

        distance = math.sqrt(
            dx * dx +
            dy * dy +
            dz * dz
        )

        distances.append(
            {
                "layer_a": layers[i]["layer"],
                "layer_b": layers[j]["layer"],
                "separation": j - i,
                "distance": distance,
            }
        )


# ----------------------------------------------------------------------
# Distance statistics by layer separation
# ----------------------------------------------------------------------

distance_scales = {}

for item in distances:

    separation = str(item["separation"])

    distance_scales.setdefault(
        separation,
        []
    ).append(
        item["distance"]
    )


distance_summary = []

for separation, values in distance_scales.items():

    mean = sum(values) / len(values)

    rms = math.sqrt(
        sum(x * x for x in values)
        / len(values)
    )

    variance = sum(
        (x - mean) ** 2
        for x in values
    ) / len(values)

    distance_summary.append(
        {
            "separation": int(separation),
            "count": len(values),
            "mean_distance": mean,
            "rms_distance": rms,
            "std_distance": math.sqrt(variance),
            "min_distance": min(values),
            "max_distance": max(values),
        }
    )


distance_summary.sort(
    key=lambda x: x["separation"]
)


# ----------------------------------------------------------------------
# Nearest-neighbor structure
# ----------------------------------------------------------------------

nearest_neighbors = []

for i in range(len(layers)):

    candidates = []

    for j in range(len(layers)):

        if i == j:
            continue

        dx = layers[i]["x"] - layers[j]["x"]
        dy = layers[i]["y"] - layers[j]["y"]
        dz = layers[i]["z"] - layers[j]["z"]

        distance = math.sqrt(
            dx * dx +
            dy * dy +
            dz * dz
        )

        candidates.append(
            (
                distance,
                layers[j]["layer"]
            )
        )

    candidates.sort()

    nearest_neighbors.append(
        {
            "layer": layers[i]["layer"],
            "nearest": [
                {
                    "layer": layer,
                    "distance": distance,
                }
                for distance, layer in candidates[:3]
            ],
        }
    )


# ----------------------------------------------------------------------
# Repeated-scale test
#
# Compare distances at separations 2,4,6,8,10.
# ----------------------------------------------------------------------

candidate_scales = [2, 4, 6, 8, 10]

scale_ratios = []

for a, b in zip(
    candidate_scales,
    candidate_scales[1:]
):

    da = next(
        (
            x["mean_distance"]
            for x in distance_summary
            if x["separation"] == a
        ),
        None
    )

    db = next(
        (
            x["mean_distance"]
            for x in distance_summary
            if x["separation"] == b
        ),
        None
    )

    if da is not None and db is not None:

        scale_ratios.append(
            {
                "separation_a": a,
                "separation_b": b,
                "ratio": (
                    db / max(da, EPS)
                ),
            }
        )


# ----------------------------------------------------------------------
# PCA explained variance
# ----------------------------------------------------------------------

total_variance = sum(
    max(x, 0.0)
    for x in eigenvalues
)

explained_variance = []

for value in eigenvalues:

    explained_variance.append(
        value / max(total_variance, EPS)
    )


# ----------------------------------------------------------------------
# Output
# ----------------------------------------------------------------------

result = {
    "schema":
        "openmind.transition_geometry.v9",

    "source":
        str(INPUT),

    "transition_count":
        len(transitions),

    "transition_dimension":
        dimension,

    "pca_eigenvalues":
        eigenvalues,

    "pca_explained_variance":
        explained_variance,

    "transition_coordinates":
        transition_coordinates,

    "layer_coordinates":
        layers,

    "distance_summary":
        distance_summary,

    "nearest_neighbors":
        nearest_neighbors,

    "candidate_scale_ratios":
        scale_ratios,
}


OUTPUT.write_text(
    json.dumps(
        result,
        indent=2
    )
)


print()
print("=== PCA EXPLAINED VARIANCE ===")

for i, value in enumerate(
    explained_variance,
    start=1
):

    print(
        f"PC{i}: {value:.8f}"
    )


print()
print("=== LAYER COORDINATES ===")

for layer in layers:

    print(
        f"L{layer['layer']:02d} "
        f"x={layer['x']:.6f} "
        f"y={layer['y']:.6f} "
        f"z={layer['z']:.6f}"
    )


print()
print("=== DISTANCE SCALES ===")

for item in distance_summary:

    if item["separation"] in candidate_scales:

        print(
            f"ΔL={item['separation']:2d} "
            f"mean={item['mean_distance']:.6f} "
            f"std={item['std_distance']:.6f} "
            f"min={item['min_distance']:.6f} "
            f"max={item['max_distance']:.6f}"
        )


print()
print("=== SCALE RATIOS ===")

for item in scale_ratios:

    print(
        f"{item['separation_a']} -> "
        f"{item['separation_b']} "
        f"ratio={item['ratio']:.8f}"
    )


print()
print(f"Output: {OUTPUT}")

print()
print("TRANSITION GEOMETRY V9 COMPLETE")
