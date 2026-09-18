import pytest

from openmind.evidence import (
    EdgeEvidenceBindings,
    EvidenceRegistry,
)


def test_evidence_missing_id_is_rejected():
    with pytest.raises((KeyError, ValueError, TypeError)):
        EvidenceRegistry.from_dict([
            {
                "source": "source",
                "claim": "claim",
                "confidence": 0.9,
            }
        ])


def test_evidence_missing_source_is_rejected():
    with pytest.raises((KeyError, ValueError, TypeError)):
        EvidenceRegistry.from_dict([
            {
                "id": "E_ONE",
                "claim": "claim",
                "confidence": 0.9,
            }
        ])


def test_evidence_missing_claim_is_rejected():
    with pytest.raises((KeyError, ValueError, TypeError)):
        EvidenceRegistry.from_dict([
            {
                "id": "E_ONE",
                "source": "source",
                "confidence": 0.9,
            }
        ])


def test_evidence_missing_confidence_is_rejected():
    with pytest.raises((KeyError, ValueError, TypeError)):
        EvidenceRegistry.from_dict([
            {
                "id": "E_ONE",
                "source": "source",
                "claim": "claim",
            }
        ])


def test_evidence_invalid_confidence_is_rejected():
    with pytest.raises((ValueError, TypeError)):
        EvidenceRegistry.from_dict([
            {
                "id": "E_ONE",
                "source": "source",
                "claim": "claim",
                "confidence": "not-a-number",
            }
        ])


def test_bindings_missing_source_is_rejected():
    with pytest.raises((KeyError, ValueError, TypeError)):
        EdgeEvidenceBindings.from_dict([
            {
                "target": "B",
                "evidence_id": "E_ONE",
            }
        ])


def test_bindings_missing_target_is_rejected():
    with pytest.raises((KeyError, ValueError, TypeError)):
        EdgeEvidenceBindings.from_dict([
            {
                "source": "A",
                "evidence_id": "E_ONE",
            }
        ])


def test_bindings_missing_evidence_id_is_rejected():
    with pytest.raises((KeyError, ValueError, TypeError)):
        EdgeEvidenceBindings.from_dict([
            {
                "source": "A",
                "target": "B",
            }
        ])


def test_binding_non_list_is_rejected():
    with pytest.raises(ValueError):
        EdgeEvidenceBindings.from_dict({
            "source": "A",
            "target": "B",
            "evidence_id": "E_ONE",
        })


def test_evidence_non_list_is_rejected():
    with pytest.raises(ValueError):
        EvidenceRegistry.from_dict({
            "id": "E_ONE",
            "source": "source",
            "claim": "claim",
            "confidence": 1.0,
        })
