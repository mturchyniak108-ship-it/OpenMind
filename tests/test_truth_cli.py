from contextlib import redirect_stdout
from io import StringIO

from openmind.cli.truth import main


def run_cli(start: str, end: str):
    output = StringIO()

    with redirect_stdout(output):
        status = main(start, end)

    return status, output.getvalue()


def test_truth_cli_project_to_evidence():
    status, output = run_cli("PROJECT", "EVIDENCE")

    assert status == 0
    assert "===== OPENMIND CANONICAL TRUTH TRACE =====" in output
    assert "start: PROJECT" in output
    assert "end:   EVIDENCE" in output
    assert (
        "PROJECT -> AGENT -> DOCS -> ENGINE -> TEST -> EVIDENCE"
        in output
    )


def test_truth_cli_preserves_canonical_score():
    status, output = run_cli("PROJECT", "EVIDENCE")

    assert status == 0
    assert "CANONICAL SCORE" in output
    assert "0.875800000000" in output


def test_truth_cli_reports_provenance_coverage():
    status, output = run_cli("PROJECT", "EVIDENCE")

    assert status == 0
    assert "registered: 3" in output
    assert "unbound:    2" in output
    assert "missing:    0" in output
    assert "coverage:   0.600000" in output


def test_truth_cli_reports_registered_evidence():
    status, output = run_cli("PROJECT", "EVIDENCE")

    assert status == 0
    assert (
        "PROJECT -> AGENT"
        " | relation=documented_for"
        " | weight=0.950000"
        " | evidence=E_PROJECT_AGENT"
        " | status=REGISTERED"
    ) in output

    assert (
        "ENGINE -> TEST"
        " | relation=validated_by"
        " | weight=0.970000"
        " | evidence=E_ENGINE_TEST"
        " | status=REGISTERED"
    ) in output

    assert (
        "TEST -> EVIDENCE"
        " | relation=produces"
        " | weight=0.960000"
        " | evidence=E_TEST_EVIDENCE"
        " | status=REGISTERED"
    ) in output


def test_truth_cli_reports_unbound_edges():
    status, output = run_cli("PROJECT", "EVIDENCE")

    assert status == 0
    assert (
        "AGENT -> DOCS"
        " | relation=uses"
        " | weight=0.960000"
        " | evidence=UNBOUND"
        " | status=UNBOUND"
    ) in output

    assert (
        "DOCS -> ENGINE"
        " | relation=documents"
        " | weight=0.940000"
        " | evidence=UNBOUND"
        " | status=UNBOUND"
    ) in output


def test_truth_cli_rejects_missing_canonical_path():
    status, output = run_cli("PROJECT", "NONEXISTENT")

    assert status == 1
    assert output.strip() == "NO CANONICAL PATH"


def test_truth_cli_uses_persistent_binding_manifest(tmp_path, monkeypatch):
    from openmind.cli import truth

    bindings_path = truth.GRAPH_ROOT / "bindings.json"
    original = bindings_path.read_text()

    try:
        bindings_path.write_text("""[
  {
    "source": "ENGINE",
    "target": "TEST",
    "evidence_id": "E_ENGINE_TEST"
  }
]
""")

        status, output = run_cli("PROJECT", "EVIDENCE")

        assert status == 0
        assert "PROJECT -> AGENT" in output
        assert (
            "PROJECT -> AGENT"
            " | relation=documented_for"
            " | weight=0.950000"
            " | evidence=UNBOUND"
            " | status=UNBOUND"
        ) in output

        assert (
            "ENGINE -> TEST"
            " | relation=validated_by"
            " | weight=0.970000"
            " | evidence=E_ENGINE_TEST"
            " | status=REGISTERED"
        ) in output

    finally:
        bindings_path.write_text(original)


def test_truth_cli_reports_unbound_gap_edges():
    status, output = run_cli("PROJECT", "EVIDENCE")

    assert status == 0
    assert "PROVENANCE GAPS" in output
    assert "UNBOUND: AGENT -> DOCS" in output
    assert "UNBOUND: DOCS -> ENGINE" in output


def test_truth_cli_reports_missing_gap_edges():
    from openmind.cli import truth

    bindings_path = truth.GRAPH_ROOT / "bindings.json"
    original = bindings_path.read_text()

    try:
        bindings_path.write_text("""[
  {
    "source": "PROJECT",
    "target": "AGENT",
    "evidence_id": "E_PROJECT_AGENT"
  },
  {
    "source": "ENGINE",
    "target": "TEST",
    "evidence_id": "E_MISSING"
  },
  {
    "source": "TEST",
    "target": "EVIDENCE",
    "evidence_id": "E_TEST_EVIDENCE"
  }
]
""")

        status, output = run_cli("PROJECT", "EVIDENCE")

        assert status == 0
        assert "PROVENANCE GAPS" in output
        assert "MISSING: ENGINE -> TEST" in output

    finally:
        bindings_path.write_text(original)
