from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class RepresentationState:
    parameter_field: dict
    phase: dict | None
    transition: dict | None
    geometry: dict | None
    lattice: dict | None
    topology: dict | None


class OpenMindCandidate:
    """
    Frozen-artifact representation pipeline.

    This class intentionally does not modify experimental artifacts.
    """

    def __init__(self, artifact_root):
        self.root = Path(artifact_root)

    def load(self, name):
        path = self.root / name

        if not path.exists():
            raise FileNotFoundError(path)

        return json.loads(path.read_text())

    def build(self):
        parameter_field = self.load(
            "q8_parameter_field_v4_1.json"
        )

        transition = self.load(
            "transition_field_v5.json"
        )

        geometry = self.load(
            "normalized_geometry_v10.json"
        )

        phase = self.load(
            "q8_phase_detection_v6.json"
        )

        lattice = self.load(
            "canonical_lattice_v21.json"
        )

        topology = self.load(
            "topology_lattice_v22.json"
        )

        return RepresentationState(
            parameter_field=parameter_field,
            phase=phase,
            transition=transition,
            geometry=geometry,
            lattice=lattice,
            topology=topology,
        )
