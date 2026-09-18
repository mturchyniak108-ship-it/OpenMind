import pytest

from openmind.evidence import EvidenceRecord, EvidenceRegistry


def record(
    evidence_id: str,
    claim: str = "TEST produces EVIDENCE",
) -> EvidenceRecord:
    return EvidenceRecord(
        id=evidence_id,
        source="artifact:test",
        claim=claim,
        confidence=0.96,
    )


def test_registry_add_and_get():
    registry = EvidenceRegistry()
    evidence = record("E1")

    registry.add(evidence)

    assert registry.get("E1") == evidence
    assert len(registry) == 1


def test_registry_is_deterministically_ordered():
    registry = EvidenceRegistry(
        [
            record("E3"),
            record("E1"),
            record("E2"),
        ]
    )

    assert [item.id for item in registry.all()] == [
        "E1",
        "E2",
        "E3",
    ]


def test_identical_duplicate_is_allowed():
    evidence = record("E1")
    registry = EvidenceRegistry([evidence])

    registry.add(evidence)

    assert len(registry) == 1


def test_conflicting_duplicate_is_rejected():
    registry = EvidenceRegistry([record("E1")])

    with pytest.raises(ValueError):
        registry.add(
            record(
                "E1",
                claim="DIFFERENT CLAIM",
            )
        )


def test_missing_evidence_returns_none():
    registry = EvidenceRegistry()

    assert registry.get("DOES_NOT_EXIST") is None


def test_registry_to_dict_is_canonical():
    registry = EvidenceRegistry(
        [
            record("E3"),
            record("E1"),
            record("E2"),
        ]
    )

    assert registry.to_dict() == [
        {
            "id": "E1",
            "source": "artifact:test",
            "claim": "TEST produces EVIDENCE",
            "confidence": 0.96,
        },
        {
            "id": "E2",
            "source": "artifact:test",
            "claim": "TEST produces EVIDENCE",
            "confidence": 0.96,
        },
        {
            "id": "E3",
            "source": "artifact:test",
            "claim": "TEST produces EVIDENCE",
            "confidence": 0.96,
        },
    ]


def test_registry_json_is_deterministic():
    first = EvidenceRegistry(
        [record("E2"), record("E1")]
    )

    second = EvidenceRegistry(
        [record("E1"), record("E2")]
    )

    assert first.to_json() == second.to_json()


def test_registry_json_round_trip():
    original = EvidenceRegistry(
        [
            record("E3"),
            record("E1"),
            record("E2"),
        ]
    )

    restored = EvidenceRegistry.from_json(
        original.to_json()
    )

    assert restored.all() == original.all()
    assert restored.to_json() == original.to_json()


def test_registry_from_dict_rejects_conflicting_duplicates():
    with pytest.raises(ValueError):
        EvidenceRegistry.from_dict(
            [
                {
                    "id": "E1",
                    "source": "artifact:test",
                    "claim": "CLAIM ONE",
                    "confidence": 0.96,
                },
                {
                    "id": "E1",
                    "source": "artifact:test",
                    "claim": "CLAIM TWO",
                    "confidence": 0.96,
                },
            ]
        )


def test_registry_json_requires_list():
    with pytest.raises(ValueError):
        EvidenceRegistry.from_json(
            '{"id": "E1"}'
        )


def test_registry_save_and_load(tmp_path):
    original = EvidenceRegistry(
        [
            record("E2"),
            record("E1"),
        ]
    )

    path = tmp_path / "evidence.json"
    original.save(path)

    restored = EvidenceRegistry.load(path)

    assert restored.all() == original.all()
    assert restored.to_json() == original.to_json()


def test_registry_save_is_canonical(tmp_path):
    registry = EvidenceRegistry(
        [
            record("E3"),
            record("E1"),
            record("E2"),
        ]
    )

    path = tmp_path / "evidence.json"
    registry.save(path)

    assert path.read_text(encoding="utf-8") == registry.to_json()
