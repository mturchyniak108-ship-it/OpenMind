import json
import math
from pathlib import Path

INPUT = Path(
    "experiments/model_fractal/transition_field_v5.json"
)

OUTPUT = Path(
    "experiments/model_fractal/normalized_geometry_v10.json"
)

EPS = 1e-12

d = json.loads(INPUT.read_text())
transitions = d["transitions"]

print("=" * 72)
print(" OPENMIND / NORMALIZED FRACTAL GEOMETRY V10")
print("=" * 72)
print()
print(f"Transitions: {len(transitions)}")


vectors = [
    [float(x) for x in t["relative_delta"]]
    for t in transitions
]

dimension = len(vectors[0])


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


def principal_component(matrix, iterations=1000):

    vector = [
        math.sin(i + 1) + 1.0
        for i in range(len(matrix))
    ]

    vector = normalize(vector)

    for _ in range(iterations):

        new_vector = normalize(
            mat_vec(matrix, vector)
        )

        difference = math.sqrt(
            sum(
                (
                    new_vector[i] -
                    vector[i]
                ) ** 2
                for i in range(len(vector))
            )
        )

        vector = new_vector

        if difference < 1e-10:
            break

    eigenvalue = dot(
        vector,
        mat_vec(matrix, vector)
    )

    return eigenvalue, vector


working = [
    row[:]
    for row in covariance
]

eigenvalues = []
components = []

for _ in range(min(6, dimension)):

    eigenvalue, component = (
        principal_component(working)
    )

    eigenvalues.append(eigenvalue)
    components.append(component)

    for i in range(dimension):
        for j in range(dimension):

            working[i][j] -= (
                eigenvalue *
                component[i] *
                component[j]
            )


total = sum(
    max(x, 0.0)
    for x in eigenvalues
)

explained = [
    max(x, 0.0) / max(total, EPS)
    for x in eigenvalues
]


# ------------------------------------------------------------
# Project transitions
# ------------------------------------------------------------

coordinates = []

for i, vector in enumerate(centered):

    projected = [
        dot(vector, component)
        for component in components[:3]
    ]

    coordinates.append(
        {
            "transition": i,
            "from_layer": transitions[i]["from_layer"],
            "to_layer": transitions[i]["to_layer"],
            "x": projected[0],
            "y": projected[1],
            "z": projected[2],
        }
    )


# ------------------------------------------------------------
# Cumulative layer trajectory
# ------------------------------------------------------------

layers = [
    {
        "layer": 0,
        "x": 0.0,
        "y": 0.0,
        "z": 0.0,
    }
]

x = y = z = 0.0

for p in coordinates:

    x += p["x"]
    y += p["y"]
    z += p["z"]

    layers.append(
        {
            "layer": p["to_layer"],
            "x": x,
            "y": y,
            "z": z,
        }
    )


# ------------------------------------------------------------
# Segment lengths
# ------------------------------------------------------------

segment_lengths = []

for i in range(1, len(layers)):

    a = layers[i - 1]
    b = layers[i]

    dx = b["x"] - a["x"]
    dy = b["y"] - a["y"]
    dz = b["z"] - a["z"]

    segment_lengths.append(
        math.sqrt(
            dx * dx +
            dy * dy +
            dz * dz
        )
    )


# ------------------------------------------------------------
# Total path and endpoint closure
# ------------------------------------------------------------

path_length = sum(segment_lengths)

endpoint = layers[-1]

closure_distance = math.sqrt(
    endpoint["x"] ** 2 +
    endpoint["y"] ** 2 +
    endpoint["z"] ** 2
)

closure_ratio = (
    closure_distance /
    max(path_length, EPS)
)


# ------------------------------------------------------------
# Output
# ------------------------------------------------------------

result = {
    "schema":
        "openmind.normalized_fractal_geometry.v10",

    "source":
        str(INPUT),

    "transition_count":
        len(transitions),

    "component_dimension":
        dimension,

    "pca_eigenvalues":
        eigenvalues,

    "pca_explained_variance":
        explained,

    "transition_coordinates":
        coordinates,

    "layer_coordinates":
        layers,

    "segment_lengths":
        segment_lengths,

    "path_length":
        path_length,

    "closure_distance":
        closure_distance,

    "closure_ratio":
        closure_ratio,
}


OUTPUT.write_text(
    json.dumps(
        result,
        indent=2
    )
)


print()
print("=== NORMALIZED PCA ===")

for i, value in enumerate(
    explained,
    start=1
):

    print(
        f"PC{i}: {value:.8f}"
    )


print()
print("=== PATH GEOMETRY ===")

print(
    f"Path length: "
    f"{path_length:.8f}"
)

print(
    f"Endpoint distance: "
    f"{closure_distance:.8f}"
)

print(
    f"Closure ratio: "
    f"{closure_ratio:.8f}"
)


print()
print("=== NORMALIZED LAYER TRAJECTORY ===")

for layer in layers:

    print(
        f"L{layer['layer']:02d} "
        f"x={layer['x']:.6f} "
        f"y={layer['y']:.6f} "
        f"z={layer['z']:.6f}"
    )


print()
print(f"Output: {OUTPUT}")

print()
print("NORMALIZED FRACTAL GEOMETRY COMPLETE")
