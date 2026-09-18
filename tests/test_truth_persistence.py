import json

import pytest

from openmind.evidence import (
    EdgeEvidenceBinding,
    EdgeEvidenceBindings,
    EvidenceRecord,
    EvidenceRegistry,
)


def test_evidence_registry_json_round_trip_is_deterministic():
    registry = EvidenceRegistry([
        EvidenceRecord(
            id="E_TWO",
            source="source-b",
            claim="claim b",
            confidence=0.8,
        ),
        EvidenceRecord(
            id="E_ONE",
            source="source-a",
            claim="claim a",
            confidence=0.9,
        ),
    ])

    first = registry.to_json()
    restored = EvidenceRegistry.from_json(first)
    second = restored.to_json()

    assert first == second
    assert restored.all() == registry.all()


def test_evidence_registry_serialization_is_sorted_by_id():
    registry = EvidenceRegistry([
        EvidenceRecord(
            id="Z",
            source="z",
            claim="z",
            confidence=1.0,
        ),
        EvidenceRecord(
            id="A",
            source="a",
            claim="a",
            confidence=1.0,
        ),
    ])

    data = json.loads(registry.to_json())

    assert [item["id"] for item in data] == ["A", "Z"]


def test_evidence_registry_rejects_non_list_json():
    with pytest.raises(
        ValueError,
        match="evidence registry JSON must contain a list",
    ):
        EvidenceRegistry.from_json('{"id": "E_ONE"}')


def test_evidence_registry_save_load_round_trip(tmp_path):
    registry = EvidenceRegistry([
        EvidenceRecord(
            id="E_ONE",
            source="source",
            claim="claim",
            confidence=0.75,
        )
    ])

    path = tmp_path / "evidence.json"

    registry.save(path)
    restored = EvidenceRegistry.load(path)

    assert restored.all() == registry.all()
    assert path.read_text() == registry.to_json()


def test_identical_duplicate_evidence_is_idempotent():
    record = EvidenceRecord(
        id="E_ONE",
        source="source",
        claim="claim",
        confidence=0.75,
    )

    registry = EvidenceRegistry([record, record])

    assert len(registry) == 1
    assert registry.get("E_ONE") == record


def test_bindings_reject_non_list_json(tmp_path):
    path = tmp_path / "bindings.json"
    path.write_text('{"source": "A"}')

    with pytest.raises(
        ValueError,
        match="edge evidence bindings JSON must contain a list",
    ):
        EdgeEvidenceBindings.load(path)


def test_bindings_round_trip_from_json():
    data = [
        {
            "source": "ENGINE",
            "target": "TEST",
            "evidence_id": "E_ENGINE_TEST",
        },
        {
            "source": "PROJECT",
            "target": "AGENT",
            "evidence_id": "E_PROJECT_AGENT",
        },
    ]

    bindings = EdgeEvidenceBindings.from_dict(data)

    assert bindings.get("ENGINE", "TEST") == "E_ENGINE_TEST"
    assert bindings.get("PROJECT", "AGENT") == "E_PROJECT_AGENT"


def test_bindings_duplicate_identical_entries_are_idempotent():
    binding = EdgeEvidenceBinding(
        source="ENGINE",
        target="TEST",
        evidence_id="E_ENGINE_TEST",
    )

    bindings = EdgeEvidenceBindings([binding, binding])

    assert bindings.get("ENGINE", "TEST") == "E_ENGINE_TEST"
    assert len(bindings.as_dict()) == 1


def test_bindings_validate_all_registered_evidence():
    registry = EvidenceRegistry([
        EvidenceRecord(
            id="E_ENGINE_TEST",
            source="source",
            claim="claim",
            confidence=1.0,
        )
    ])

    bindings = EdgeEvidenceBindings([
        EdgeEvidenceBinding(
            source="ENGINE",
            target="TEST",
            evidence_id="E_ENGINE_TEST",
        )
    ])

    assert bindings.validate(registry) == ()


def test_bindings_validation_reports_all_missing_ids():
    registry = EvidenceRegistry()

    bindings = EdgeEvidenceBindings([
        EdgeEvidenceBinding(
            source="A",
            target="B",
            evidence_id="E_TWO",
        ),
        EdgeEvidenceBinding(
            source="C",
            target="D",
            evidence_id="E_ONE",
        ),
    ])

    with pytest.raises(
        ValueError,
        match="missing evidence binding: E_ONE, E_TWO",
    ):
        bindings.validate(registry)
