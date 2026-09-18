import json

from openmind.cli.truth import main
from openmind.evidence import EvidenceRegistry, audit_truth_trace
from openmind.cli import truth


def test_truth_report_json_contract():
    status, payload = truth.report_json("PROJECT", "EVIDENCE")

    assert status == 0

    report = json.loads(payload)

    assert report["start"] == "PROJECT"
    assert report["end"] == "EVIDENCE"
    assert report["path"] == [
        "PROJECT",
        "AGENT",
        "DOCS",
        "ENGINE",
        "TEST",
        "EVIDENCE",
    ]

    assert report["score"] == 0.8758

    assert report["coverage"]["total_edges"] == 5
    assert report["coverage"]["registered_edges"] == 3
    assert report["coverage"]["unbound_edges"] == 2
    assert report["coverage"]["missing_edges"] == 0
    assert report["coverage"]["coverage"] == 0.6

    assert report["provenance_gaps"]["unbound"] == [
        ["AGENT", "DOCS"],
        ["DOCS", "ENGINE"],
    ]

    assert report["provenance_gaps"]["missing"] == []


def test_truth_report_json_preserves_evidence_resolution():
    status, payload = truth.report_json("PROJECT", "EVIDENCE")

    assert status == 0

    report = json.loads(payload)

    evidence = report["evidence"]

    assert len(evidence) == 5

    assert evidence[0]["source"] == "PROJECT"
    assert evidence[0]["target"] == "AGENT"
    assert evidence[0]["evidence_id"] == "E_PROJECT_AGENT"
    assert evidence[0]["status"] == "REGISTERED"

    assert evidence[1]["source"] == "AGENT"
    assert evidence[1]["target"] == "DOCS"
    assert evidence[1]["evidence_id"] is None
    assert evidence[1]["status"] == "UNBOUND"

    assert evidence[2]["source"] == "DOCS"
    assert evidence[2]["target"] == "ENGINE"
    assert evidence[2]["evidence_id"] is None
    assert evidence[2]["status"] == "UNBOUND"


def test_truth_report_json_rejects_missing_path():
    status, payload = truth.report_json("PROJECT", "NONEXISTENT")

    assert status == 1
    assert payload == "NO CANONICAL PATH"


def test_truth_report_json_does_not_change_canonical_cli():
    status, payload = truth.report_json("PROJECT", "EVIDENCE")

    assert status == 0
    assert '"score": 0.8758' in payload

    cli_status = main("PROJECT", "EVIDENCE")

    assert cli_status == 0
