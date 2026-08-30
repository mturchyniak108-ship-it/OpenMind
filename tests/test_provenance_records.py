import json
from pathlib import Path

from openmind.evidence import EvidenceRecord


ROOT = Path(__file__).resolve().parents[1]


def test_canonical_evidence_records_load():
    data = json.loads(
        (ROOT / "demo/truth_graph/evidence.json").read_text()
    )

    records = [
        EvidenceRecord(
            id=item["id"],
            source=item["source"],
            claim=item["claim"],
            confidence=float(item["confidence"]),
        )
        for item in data
    ]

    assert len(records) == 3
    assert records[0].id == "E_TEST_EVIDENCE"
    assert records[0].claim == "TEST produces EVIDENCE"
    assert records[0].confidence == 0.96


def test_evidence_ids_are_unique():
    data = json.loads(
        (ROOT / "demo/truth_graph/evidence.json").read_text()
    )

    ids = [item["id"] for item in data]

    assert len(ids) == len(set(ids))
