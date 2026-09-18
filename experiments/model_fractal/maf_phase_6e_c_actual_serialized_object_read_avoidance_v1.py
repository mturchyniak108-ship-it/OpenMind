#!/usr/bin/env python3
"""
OpenMind / Phase 6E-C V1
Actual generation-bound serialized MAF object read avoidance.

This runner is intentionally fail-closed.

Scientific boundary:
- application-level serialized MAF object reads only;
- no inference;
- no source-GGUF payload access;
- no inspect_object;
- no dense materialization;
- no Route Cache;
- no relationship expansion;
- no performance claim.

Authoritative execution requires an external one-shot wrapper to provide:
    OPENMIND_PHASE_6E_C_FROZEN_HEAD
    OPENMIND_PHASE_6E_C_RUNNER_SHA256

The wrapper is also responsible for creating the external spent-slot sentinel
before invoking this runner.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True


# ---------------------------------------------------------------------------
# FROZEN REPOSITORY / PHASE IDENTITY
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT_DIR = ROOT / "experiments" / "model_fractal"

EXPECTED_BRANCH = "labs/multidimensional-maf"

PREREG_PATH = EXPERIMENT_DIR / (
    "MAF_PHASE_6E_C_ACTUAL_SERIALIZED_OBJECT_READ_AVOIDANCE_"
    "PREREGISTRATION_V1.md"
)
PREREG_SHA256 = (
    "8a143ec7a978d157e2dd700b541cfef6"
    "dc4b4781cc2bf582546443534e9c41e6"
)

CONTRACT_PATH = EXPERIMENT_DIR / (
    "MAF_PHASE_6E_C_ACTUAL_SERIALIZED_OBJECT_READ_AVOIDANCE_"
    "RUNNER_IMPLEMENTATION_CONTRACT_V1.md"
)
CONTRACT_SHA256 = (
    "e9449191c68aa045335042ee29f7e16e"
    "ff5e7db419cb93e9b5b2f9eb6fda4ac7"
)

ENTRY_CHECKPOINT_PATH = EXPERIMENT_DIR / "MAF_PHASE_6E_ENTRY_CHECKPOINT.md"
ENTRY_CHECKPOINT_SHA256 = (
    "1807437ea97e46a6cc687adbbe8c384d"
    "abae45a562f1d2aef6bd37e43b4bbe35"
)

PHASE_6E_A_RESULT_PATH = (
    EXPERIMENT_DIR
    / "maf_phase_6e_a_selective_working_set_sufficiency_v1.json"
)
PHASE_6E_A_RESULT_SHA256 = (
    "f86433603e68fc9f1e5c65f7d3ecbd8"
    "d9ce9313d252c605dd6e2cada18a91c86"
)

PHASE_6E_A_VERDICT_PATH = (
    EXPERIMENT_DIR
    / "MAF_PHASE_6E_A_SELECTIVE_WORKING_SET_SUFFICIENCY_V1_VERDICT.md"
)
PHASE_6E_A_VERDICT_SHA256 = (
    "a6c9ce2f2207beb252b2c02b47e27878"
    "b27e72736dad4275ab9905d40812e334"
)

PHASE_6E_B_S1_RESULT_PATH = (
    EXPERIMENT_DIR
    / "maf_phase_6e_b_s1_bounded_expansion_recovery_v1.json"
)
PHASE_6E_B_S1_RESULT_SHA256 = (
    "194857dd4df6baabbee3138f1e6cb3d7"
    "5988ddd092a4fd877892ab4528cf81a4"
)

PHASE_6E_B_S1_VERDICT_PATH = (
    EXPERIMENT_DIR
    / "MAF_PHASE_6E_B_S1_BOUNDED_EXPANSION_RECOVERY_V1_VERDICT.md"
)
PHASE_6E_B_S1_VERDICT_SHA256 = (
    "6ba5427a18d4bbbb24354562508743720"
    "16438367d8c591913432c084c627abf"
)

PHASE_6E_B_S1_TRACE_SHA256 = (
    "5fab94f632b8e653b2debe3f5e98f9a"
    "19b9688bd9bacb4a578c75537c1b0ca53"
)

PHASE_6E_B_INCIDENT_PATH = (
    EXPERIMENT_DIR
    / (
        "MAF_PHASE_6E_B_EXECUTION_FAILURE_INCIDENT_AND_"
        "CORRECTIVE_SUCCESSOR_DESIGN_V1.md"
    )
)
PHASE_6E_B_INCIDENT_SHA256 = (
    "1ecf171bee1e6470d5ac48c1482a2166"
    "eca05c895313eeb4acbc8e90b64a64ad"
)

ORIGINAL_PHASE_6E_B_RESULT_PATH = (
    EXPERIMENT_DIR
    / "maf_phase_6e_b_bounded_expansion_recovery_v1.json"
)

QUERIES_PATH = (
    EXPERIMENT_DIR
    / "maf_query_to_pk_selection_validation_v1_queries.json"
)
QUERIES_SHA256 = (
    "32f4636bd5e8ceee0dca8342335279a6"
    "f8e6acafe866a5469f2c23aa2655202a"
)

CATALOG_PATH = (
    EXPERIMENT_DIR
    / "maf_query_to_pk_selection_validation_v1_catalog.json"
)
CATALOG_SHA256 = (
    "c51ef0fabeb10e7c8a091a093aa19346"
    "20a69b2026b5a87cb02477b9dd7ca900"
)

SELECTOR_PROTOCOL_PATH = (
    EXPERIMENT_DIR
    / "MAF_QUERY_TO_PK_SELECTION_V1_PROTOCOL.md"
)
SELECTOR_PROTOCOL_SHA256 = (
    "b42a0643976c2393871e3b826ba5573b"
    "4de981b49603de63230d69cf57be0811"
)

SELECTOR_PATH = (
    EXPERIMENT_DIR
    / "maf_query_to_pk_selection_v1.py"
)
SELECTOR_SHA256 = (
    "e21c05e352fe921b791e8c936425727a"
    "98911ce7566989672a96bfd2b9613fa2"
)

CAPSULE_PROTOCOL_PATH = (
    EXPERIMENT_DIR
    / "MAF_QUERY_CAPSULE_DATA_MODEL_V1_PROTOCOL.md"
)
CAPSULE_PROTOCOL_SHA256 = (
    "5255a58c8c6340c251e24ae8543760fc"
    "d66a8deb8be1a8356ad5b78ad898edda"
)

CAPSULE_PATH = (
    EXPERIMENT_DIR
    / "maf_query_capsule_data_model_v1.py"
)
CAPSULE_SHA256 = (
    "f897b97011714f3c84b7350c6bb53e80"
    "0232be8a5d34e5148a3e50a81952976e"
)

GENERATION_AUTHORITY_PATH = (
    EXPERIMENT_DIR
    / "maf_query_to_pk_selection_validation_v1_generation_construction_authority.json"
)
GENERATION_AUTHORITY_SHA256 = (
    "a5e953ae2ab2dd11a9f6dc564ae5ee57"
    "cb064d6eea0a8a5517191b4a6efc1a6d"
)

GENERATION_ROOT = (
    ROOT
    / "results"
    / "runtime"
    / "maf_query_to_pk_selection_validation_v1_generation"
)

GENERATION_MANIFEST_PATH = GENERATION_ROOT / "validation_generation.manifest.json"
GENERATION_MANIFEST_SHA256 = (
    "28e4baaf07fae450d3c8462ed86fe59c"
    "31f0eacdd9e16a8b408994f2a54924c3"
)

REFERENCE_FIXTURE_PATH = (
    EXPERIMENT_DIR
    / "maf_phase_6e_a_reference_state_fixture_v1.json"
)
REFERENCE_FIXTURE_SHA256 = (
    "870b656e0c3181ec8f7be1537bdeafde"
    "10fffd1b947f5372d21cdee4c00a83a0"
)

MAF_OBJECT_PATH = EXPERIMENT_DIR / "maf_object_v1.py"
MAF_OBJECT_SHA256 = (
    "eed6cbd96995412a632883f3c534f902"
    "3e7711ea8eb437afe35a48312502f63b"
)

RESIDENT_DIRECTORY_PATH = (
    EXPERIMENT_DIR
    / "maf_resident_pk_directory_v1.py"
)
RESIDENT_DIRECTORY_SHA256 = (
    "4dadac5a1ffe448437718432edeee14a2"
    "19a20da5a54956d2884d0b0b1d426b6"
)

SEGMENT_READER_PATH = (
    EXPERIMENT_DIR
    / "maf_segment_reader_v1.py"
)
SEGMENT_READER_SHA256 = (
    "3499cb8e528fe8e9315e3e5656d6aa8"
    "88c95ca175310b6371e722de409827369"
)

TELEMETRY_MODEL_PATH = (
    EXPERIMENT_DIR
    / "maf_segment_locality_data_model_v1.py"
)
TELEMETRY_MODEL_SHA256 = (
    "5432f2d74a610f2d0f9181e9af146013"
    "bb198a4e837af634993909358fff8ad0"
)

TELEMETRY_INTEGRATION_PATH = (
    EXPERIMENT_DIR
    / "maf_segment_locality_runtime_telemetry_integration_v1_1.py"
)
TELEMETRY_INTEGRATION_SHA256 = (
    "850c4bae5f6c361c34f504b5af76b9ac"
    "6530980d777f8bd1a9003f3b9bb55ae6"
)

RUNTIME_RESIDENCY_PATH = (
    EXPERIMENT_DIR
    / "maf_object_runtime_residency_v1.py"
)
RUNTIME_RESIDENCY_SHA256 = (
    "4b8c0b8f5db9a67b4bcc368b18f159de"
    "6a3f2501f0badf0286de1459125d5cf9"
)

RESULT_PATH = (
    EXPERIMENT_DIR
    / "maf_phase_6e_c_actual_serialized_object_read_avoidance_v1.json"
)

SOURCE_MODEL_PK = (
    "mafmodel:v1:"
    "d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258"
)

SOURCE_GENERATION_PK = (
    "mafgen:v1:"
    "45a80a2aa271ce04853003185b6a1227cb309bd1e3e2dc538eea849fac9f5db0"
)

SOURCE_GGUF_SHA256 = (
    "507de59046601282ba768a9789900e6c"
    "cf60ed93ddf346730b7c68eb0715bc47"
)

SOURCE_MANIFEST_SHA256 = GENERATION_MANIFEST_SHA256

CATALOG_SERIALIZED_BYTES = 312_326_668
CATALOG_OBJECT_COUNT = 12
QUERY_COUNT = 40
SCIENTIFIC_QUERY_COUNT = 32
FALLBACK_CONTROL_COUNT = 8

ROUND_BUDGETS = (1, 2, 3, 4)

ROUND_CONFIG_SHA256 = (
    "2dd2925a3d9f63197deff6dc98f951c5177dc63dc08818b6492228dbac7d5576",
    "57f751a3a019bccd58c5c32b4f5ecaf78283f49cc146896d61492ce31dfdd1c6",
    "67dd6e5589cb16374e949b3ed633c3364f0ccb1d8c2b0a9ca1c6eaa2d2ceed56",
    "0caeaeaafdd870e6b02ccc8b4450576883d4ef5234ba689c472e3b14d9dbe120",
)

READ_PLAN_SCHEMA = (
    "openmind.maf_phase_6e_c_serialized_object_read_plan_snapshot.v1"
)
ACCESS_LEDGER_SCHEMA = (
    "openmind.maf_phase_6e_c_serialized_object_access_ledger.v1"
)
RESULT_SCHEMA = (
    "openmind.maf_phase_6e_c_actual_serialized_object_read_avoidance.v1"
)

UNTRACKED_BASELINE_COUNT = 440
UNTRACKED_BASELINE_SHA256 = (
    "f206c0eed32daef9ed0cfaae195aa56a343a85437ebd3135aeafdb4c1ffacddd"
)

FROZEN_HEAD_ENV = "OPENMIND_PHASE_6E_C_FROZEN_HEAD"
RUNNER_SHA_ENV = "OPENMIND_PHASE_6E_C_RUNNER_SHA256"


# ---------------------------------------------------------------------------
# FAIL-CLOSED HELPERS
# ---------------------------------------------------------------------------


class Phase6ECIntegrityError(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise Phase6ECIntegrityError(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with Path(path).open("rb") as handle:
        while True:
            block = handle.read(1024 * 1024)

            if not block:
                break

            digest.update(block)

    return digest.hexdigest()


def run_git(*args: str) -> bytes:
    result = subprocess.run(
        ("git",) + tuple(args),
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    if result.returncode != 0:
        raise Phase6ECIntegrityError(
            "git command failed: "
            + " ".join(args)
            + " :: "
            + result.stderr.decode(errors="replace")
        )

    return result.stdout


def zparts(raw: bytes) -> tuple[bytes, ...]:
    return tuple(
        part
        for part in raw.split(b"\0")
        if part
    )


def exact_file_bytes(path: Path, expected_sha256: str) -> bytes:
    raw = Path(path).read_bytes()
    need(
        sha256_bytes(raw) == expected_sha256,
        "frozen authority changed: " + str(path),
    )
    return raw


def import_frozen_module(module_name: str, path: Path, expected_sha256: str):
    need(
        sha256_file(path) == expected_sha256,
        "module SHA256 changed: " + str(path),
    )

    if str(EXPERIMENT_DIR) not in sys.path:
        sys.path.insert(0, str(EXPERIMENT_DIR))

    module = importlib.import_module(module_name)

    observed_file = Path(module.__file__).resolve()
    need(
        observed_file == path.resolve(),
        "module resolved to unexpected path: " + module_name,
    )

    return module


# ---------------------------------------------------------------------------
# EXECUTION-WRAPPER / REPOSITORY PRECHECK
# ---------------------------------------------------------------------------


def verify_pre_execution_state() -> tuple[str, str]:
    frozen_head = os.environ.get(FROZEN_HEAD_ENV, "")
    expected_runner_sha = os.environ.get(RUNNER_SHA_ENV, "")

    need(
        len(frozen_head) == 40
        and all(ch in "0123456789abcdef" for ch in frozen_head),
        FROZEN_HEAD_ENV + " must be a full lowercase Git commit",
    )

    need(
        len(expected_runner_sha) == 64
        and all(ch in "0123456789abcdef" for ch in expected_runner_sha),
        RUNNER_SHA_ENV + " must be a lowercase SHA256",
    )

    branch = run_git("branch", "--show-current").decode().strip()
    head = run_git("rev-parse", "HEAD").decode().strip()

    need(branch == EXPECTED_BRANCH, "wrong scientific branch")
    need(head == frozen_head, "HEAD differs from wrapper-supplied frozen runner commit")

    need(
        run_git("diff", "--name-only", "-z") == b"",
        "tracked worktree is dirty",
    )

    need(
        run_git("diff", "--cached", "--name-only", "-z") == b"",
        "Git index is non-empty",
    )

    untracked = run_git(
        "ls-files",
        "-z",
        "--others",
        "--exclude-standard",
    )

    need(
        len(zparts(untracked)) == UNTRACKED_BASELINE_COUNT,
        "untracked path count changed",
    )

    need(
        sha256_bytes(untracked) == UNTRACKED_BASELINE_SHA256,
        "canonical NUL-delimited untracked baseline changed",
    )

    need(
        not RESULT_PATH.exists(),
        "Phase 6E-C result path already exists",
    )

    need(
        not ORIGINAL_PHASE_6E_B_RESULT_PATH.exists(),
        "original Phase 6E-B result path must remain absent",
    )

    observed_runner_sha = sha256_file(Path(__file__))

    need(
        observed_runner_sha == expected_runner_sha,
        "runner source SHA256 differs from wrapper-supplied frozen identity",
    )

    return frozen_head, observed_runner_sha


# ---------------------------------------------------------------------------
# FROZEN AUTHORITY QUALIFICATION
# ---------------------------------------------------------------------------


AUTHORITY_SHA256 = {
    PREREG_PATH: PREREG_SHA256,
    CONTRACT_PATH: CONTRACT_SHA256,
    ENTRY_CHECKPOINT_PATH: ENTRY_CHECKPOINT_SHA256,
    PHASE_6E_A_RESULT_PATH: PHASE_6E_A_RESULT_SHA256,
    PHASE_6E_A_VERDICT_PATH: PHASE_6E_A_VERDICT_SHA256,
    PHASE_6E_B_S1_RESULT_PATH: PHASE_6E_B_S1_RESULT_SHA256,
    PHASE_6E_B_S1_VERDICT_PATH: PHASE_6E_B_S1_VERDICT_SHA256,
    PHASE_6E_B_INCIDENT_PATH: PHASE_6E_B_INCIDENT_SHA256,
    QUERIES_PATH: QUERIES_SHA256,
    CATALOG_PATH: CATALOG_SHA256,
    SELECTOR_PROTOCOL_PATH: SELECTOR_PROTOCOL_SHA256,
    SELECTOR_PATH: SELECTOR_SHA256,
    CAPSULE_PROTOCOL_PATH: CAPSULE_PROTOCOL_SHA256,
    CAPSULE_PATH: CAPSULE_SHA256,
    GENERATION_AUTHORITY_PATH: GENERATION_AUTHORITY_SHA256,
    GENERATION_MANIFEST_PATH: GENERATION_MANIFEST_SHA256,
    REFERENCE_FIXTURE_PATH: REFERENCE_FIXTURE_SHA256,
    MAF_OBJECT_PATH: MAF_OBJECT_SHA256,
    RESIDENT_DIRECTORY_PATH: RESIDENT_DIRECTORY_SHA256,
    SEGMENT_READER_PATH: SEGMENT_READER_SHA256,
    TELEMETRY_MODEL_PATH: TELEMETRY_MODEL_SHA256,
    TELEMETRY_INTEGRATION_PATH: TELEMETRY_INTEGRATION_SHA256,
    RUNTIME_RESIDENCY_PATH: RUNTIME_RESIDENCY_SHA256,
}


def load_and_verify_authority_bytes() -> dict[Path, bytes]:
    raw_by_path = {}

    for path, expected_sha in AUTHORITY_SHA256.items():
        raw_by_path[path] = exact_file_bytes(path, expected_sha)

    return raw_by_path


# ---------------------------------------------------------------------------
# NON-ORACLE INPUTS
# ---------------------------------------------------------------------------


def load_catalog_from_frozen_module(selector_module, raw: bytes):
    catalog_cls = getattr(
        selector_module,
        "MAFQueryPKCatalogV1",
        None,
    )

    need(
        catalog_cls is not None,
        "selector module lacks MAFQueryPKCatalogV1",
    )

    from_json_bytes = getattr(
        catalog_cls,
        "from_json_bytes",
        None,
    )

    if callable(from_json_bytes):
        return from_json_bytes(raw)

    from_mapping = getattr(
        catalog_cls,
        "from_mapping",
        None,
    )

    if callable(from_mapping):
        return from_mapping(
            json.loads(raw.decode("utf-8"))
        )

    raise Phase6ECIntegrityError(
        "frozen selector catalog class exposes no supported deterministic loader"
    )


def load_non_oracle_inputs(selector_module, raw_by_path: dict[Path, bytes]):
    query_doc = json.loads(
        raw_by_path[QUERIES_PATH].decode("utf-8")
    )

    queries = query_doc.get("queries")

    need(
        isinstance(queries, list),
        "query fixture queries must be list",
    )

    need(
        len(queries) == QUERY_COUNT,
        "query count mismatch",
    )

    expected_classes = {
        "specific_intent": 24,
        "multi_target_intent": 8,
        "fallback_control": 8,
    }

    class_counts = {}
    query_ids = []

    for row in queries:
        need(isinstance(row, dict), "query row must be object")

        query_id = row.get("query_id")
        query_text = row.get("query_text")
        query_class = row.get("query_class")

        need(
            isinstance(query_id, str) and query_id,
            "query_id must be non-empty str",
        )

        need(
            isinstance(query_text, str),
            "query_text must be str",
        )

        need(
            query_class in expected_classes,
            "unexpected query_class: " + str(query_class),
        )

        query_ids.append(query_id)

        class_counts[query_class] = (
            class_counts.get(query_class, 0) + 1
        )

    need(
        len(query_ids) == len(set(query_ids)),
        "duplicate query_id",
    )

    need(
        class_counts == expected_classes,
        "frozen query class counts changed",
    )

    catalog_raw = raw_by_path[CATALOG_PATH]

    catalog_doc = json.loads(
        catalog_raw.decode("utf-8")
    )

    entries = catalog_doc.get("entries")

    need(
        isinstance(entries, list),
        "catalog entries must be list",
    )

    need(
        len(entries) == CATALOG_OBJECT_COUNT,
        "catalog object count mismatch",
    )

    catalog_pks = tuple(
        row["object_pk"]
        for row in entries
    )

    need(
        len(catalog_pks) == len(set(catalog_pks)),
        "duplicate catalog object PK",
    )

    catalog = load_catalog_from_frozen_module(
        selector_module,
        catalog_raw,
    )

    return (
        tuple(queries),
        catalog,
        catalog_pks,
    )


# ---------------------------------------------------------------------------
# GENERATION-BOUND PHYSICAL PLACEMENT
# ---------------------------------------------------------------------------


def load_generation_metadata(raw_by_path: dict[Path, bytes]):
    authority = json.loads(
        raw_by_path[GENERATION_AUTHORITY_PATH].decode("utf-8")
    )

    manifest = json.loads(
        raw_by_path[GENERATION_MANIFEST_PATH].decode("utf-8")
    )

    bindings = authority["bindings"]

    need(
        bindings["model_pk"] == SOURCE_MODEL_PK,
        "generation authority model PK mismatch",
    )

    need(
        bindings["source_gguf"]["sha256"] == SOURCE_GGUF_SHA256,
        "source GGUF provenance SHA mismatch",
    )

    output_layout = authority["output_layout"]

    expected_manifest_rel = str(
        GENERATION_MANIFEST_PATH.relative_to(ROOT)
    )

    need(
        output_layout["generation_manifest_path"] == expected_manifest_rel,
        "generation manifest path binding mismatch",
    )

    segment_path = ROOT / output_layout["segment_path"]

    need(
        segment_path.is_file(),
        "generation segment path missing",
    )

    segment_stat = segment_path.stat()

    need(
        stat.S_ISREG(segment_stat.st_mode),
        "generation segment is not a regular file",
    )

    need(
        manifest["generation_pk"] == SOURCE_GENERATION_PK,
        "generation manifest PK mismatch",
    )

    descriptor = manifest["descriptor"]

    need(
        descriptor["model_pk"] == SOURCE_MODEL_PK,
        "generation descriptor model PK mismatch",
    )

    objects = descriptor["objects"]
    segments = descriptor["segments"]

    need(
        len(objects) == CATALOG_OBJECT_COUNT,
        "generation object count mismatch",
    )

    need(
        len(segments) == 1,
        "Phase 6E-C V1 requires exactly one frozen validation segment",
    )

    segment_record = segments[0]

    need(
        segment_record["segment_length"] == CATALOG_SERIALIZED_BYTES,
        "catalog serialized byte denominator mismatch",
    )

    need(
        segment_stat.st_size == segment_record["segment_length"],
        "physical segment length differs from frozen descriptor",
    )

    placement_by_pk = {
        row["object_pk"]: row
        for row in objects
    }

    need(
        len(placement_by_pk) == CATALOG_OBJECT_COUNT,
        "duplicate generation object PK",
    )

    return (
        authority,
        manifest,
        placement_by_pk,
        segment_record,
        segment_path,
    )


def build_resident_entries(
    resident_module,
    catalog_pks: tuple[str, ...],
    placement_by_pk: dict[str, dict[str, Any]],
    segment_record: dict[str, Any],
    segment_path: Path,
):
    entry_by_pk = {}

    for object_pk in catalog_pks:
        placement = placement_by_pk.get(object_pk)

        need(
            placement is not None,
            "catalog PK absent from generation manifest: " + object_pk,
        )

        need(
            placement["segment_id"] == segment_record["segment_id"],
            "object segment ID mismatch",
        )

        entry = resident_module.ResidentPKEntry(
            model_pk=SOURCE_MODEL_PK,
            generation_pk=SOURCE_GENERATION_PK,
            generation_manifest_sha256=GENERATION_MANIFEST_SHA256,
            object_pk=object_pk,
            segment_id=placement["segment_id"],
            offset=placement["offset"],
            length=placement["length"],
            object_file_sha256=placement["object_file_sha256"],
            payload_sha256=placement["payload_sha256"],
            segment_length=segment_record["segment_length"],
            segment_sha256=segment_record["segment_sha256"],
            segment_path=str(segment_path),
        )

        entry_by_pk[object_pk] = entry

    need(
        tuple(entry_by_pk) == catalog_pks,
        "resident-entry catalog order changed",
    )

    return entry_by_pk


# ---------------------------------------------------------------------------
# FROZEN SELECTOR SCHEDULE
# ---------------------------------------------------------------------------


def build_round_configs(selector_module):
    configs = tuple(
        selector_module.default_selection_config_v1(
            max_candidates=budget
        )
        for budget in ROUND_BUDGETS
    )

    actual = tuple(
        config.selection_config_sha256
        for config in configs
    )

    need(
        actual == ROUND_CONFIG_SHA256,
        "round selection configuration SHA256 mismatch",
    )

    return configs


def validate_selection_result(
    result,
    budget: int,
    config_sha: str,
    catalog_pks: tuple[str, ...],
):
    need(
        result.source_generation_pk == SOURCE_GENERATION_PK,
        "selector source generation mismatch",
    )

    need(
        result.source_manifest_sha256 == SOURCE_MANIFEST_SHA256,
        "selector source manifest mismatch",
    )

    need(
        result.catalog_sha256 == CATALOG_SHA256,
        "selector catalog SHA256 mismatch",
    )

    need(
        result.selection_config_sha256 == config_sha,
        "selector selection-config SHA mismatch",
    )

    selected = tuple(
        result.selected_object_pks
    )

    need(
        len(selected) <= budget,
        "selector exceeded candidate budget",
    )

    need(
        len(selected) == len(set(selected)),
        "selector returned duplicate object PK",
    )

    catalog_set = set(catalog_pks)

    need(
        all(pk in catalog_set for pk in selected),
        "selector returned PK outside frozen catalog",
    )

    return selected


def select_round(
    selector_module,
    queries: tuple[dict[str, Any], ...],
    catalog,
    catalog_pks: tuple[str, ...],
    config,
    round_index: int,
    previous: dict[str, dict[str, Any]] | None,
):
    budget = ROUND_BUDGETS[round_index]
    config_sha = ROUND_CONFIG_SHA256[round_index]

    rows = {}

    for source_row in queries:
        query_id = source_row["query_id"]

        result = selector_module.select_query_to_pks_v1(
            query=source_row["query_text"],
            catalog=catalog,
            config=config,
            source_generation_pk=SOURCE_GENERATION_PK,
            source_manifest_sha256=SOURCE_MANIFEST_SHA256,
        )

        selected = validate_selection_result(
            result,
            budget,
            config_sha,
            catalog_pks,
        )

        expected_fallback = (
            source_row["query_class"] == "fallback_control"
        )

        need(
            bool(result.fallback_used) == expected_fallback,
            "selector fallback classification differs from frozen query class: "
            + query_id,
        )

        if round_index == 0:
            additional = selected
            cumulative = selected

        else:
            need(previous is not None, "previous round missing")

            prior = previous[query_id]
            previous_selected = tuple(
                prior["selected_object_pks"]
            )
            previous_set = set(previous_selected)
            current_set = set(selected)

            need(
                previous_set <= current_set,
                "non-monotonic selector result: " + query_id,
            )

            need(
                result.query_signature == prior["query_signature"],
                "query signature changed across rounds: " + query_id,
            )

            need(
                bool(result.fallback_used) == prior["fallback_used"],
                "fallback state changed across rounds: " + query_id,
            )

            additional = tuple(
                object_pk
                for object_pk in selected
                if object_pk not in previous_set
            )

            cumulative = (
                tuple(prior["cumulative_route_order"])
                + additional
            )

            need(
                len(cumulative) == len(set(cumulative)),
                "cumulative route contains duplicate PK: " + query_id,
            )

            need(
                set(cumulative) == current_set,
                "cumulative route differs from current selector set: " + query_id,
            )

        rows[query_id] = {
            "query_signature": result.query_signature,
            "fallback_used": bool(result.fallback_used),
            "selected_object_pks": selected,
            "additional_pks": additional,
            "cumulative_route_order": cumulative,
        }

    need(
        tuple(rows) == tuple(row["query_id"] for row in queries),
        "round query order mismatch",
    )

    return rows


def build_complete_read_plan(
    selector_module,
    capsule_module,
    queries: tuple[dict[str, Any], ...],
    catalog,
    catalog_pks: tuple[str, ...],
):
    configs = build_round_configs(selector_module)

    round_states = []
    previous = None

    for round_index, config in enumerate(configs):
        current = select_round(
            selector_module,
            queries,
            catalog,
            catalog_pks,
            config,
            round_index,
            previous,
        )

        round_states.append(current)
        previous = current

    records = []

    for source_row in queries:
        query_id = source_row["query_id"]

        round_zero = round_states[0][query_id]

        query_pk = capsule_module.derive_query_pk(
            query_signature=round_zero["query_signature"],
            selection_config_sha256=ROUND_CONFIG_SHA256[0],
            source_generation_pk=SOURCE_GENERATION_PK,
            source_manifest_sha256=SOURCE_MANIFEST_SHA256,
        )

        rounds = []

        for round_index in range(len(ROUND_BUDGETS)):
            state = round_states[round_index][query_id]

            rounds.append(
                {
                    "round_index": round_index,
                    "candidate_budget": ROUND_BUDGETS[round_index],
                    "selection_config_sha256": ROUND_CONFIG_SHA256[round_index],
                    "selected_object_pks": list(state["selected_object_pks"]),
                    "selected_count": len(state["selected_object_pks"]),
                    "additional_pks": list(state["additional_pks"]),
                    "cumulative_route_order": list(state["cumulative_route_order"]),
                }
            )

        final_route = tuple(
            round_states[-1][query_id]["cumulative_route_order"]
        )

        need(
            len(final_route) == len(set(final_route)),
            "final route contains duplicate PK: " + query_id,
        )

        records.append(
            {
                "query_id": query_id,
                "query_pk": query_pk,
                "query_class": source_row["query_class"],
                "query_text_sha256": sha256_bytes(
                    source_row["query_text"].encode("utf-8")
                ),
                "query_signature": round_zero["query_signature"],
                "fallback_used": round_zero["fallback_used"],
                "rounds": rounds,
                "final_planned_treatment_pks": list(final_route),
            }
        )

    snapshot = {
        "schema": READ_PLAN_SCHEMA,
        "phase": "6E-C",
        "source_model_pk": SOURCE_MODEL_PK,
        "source_generation_pk": SOURCE_GENERATION_PK,
        "source_manifest_sha256": SOURCE_MANIFEST_SHA256,
        "query_count": QUERY_COUNT,
        "round_budgets": list(ROUND_BUDGETS),
        "round_config_sha256": list(ROUND_CONFIG_SHA256),
        "records": records,
    }

    snapshot_raw = canonical_bytes(snapshot)
    snapshot_sha = sha256_bytes(snapshot_raw)

    forbidden_tokens = (
        b"required_object_pks",
        b"reference_payload_sha256",
        b"observed_payload_sha256",
        b"scientific_verdict",
        b"avoidance_verdict",
    )

    need(
        all(token not in snapshot_raw for token in forbidden_tokens),
        "read-plan snapshot contains reference-derived scientific state",
    )

    return snapshot, snapshot_raw, snapshot_sha


# ---------------------------------------------------------------------------
# IN-MEMORY SERIALIZED MAF OBJECT VALIDATION
# ---------------------------------------------------------------------------


def parse_serialized_object_bytes(
    object_module,
    serialized: bytes,
    entry,
):
    need(
        isinstance(serialized, bytes),
        "segment reader must return bytes",
    )

    need(
        len(serialized) == entry.length,
        "serialized object length mismatch",
    )

    need(
        sha256_bytes(serialized) == entry.object_file_sha256,
        "serialized object SHA256 mismatch",
    )

    header_size = object_module.HEADER_SIZE

    need(
        len(serialized) >= header_size,
        "serialized object shorter than MAF Object V1 header",
    )

    header_raw = serialized[:header_size]
    header = object_module.unpack_header(header_raw)

    metadata_length = header["metadata_length"]
    payload_length = header["payload_length"]

    metadata_start = header_size
    metadata_end = metadata_start + metadata_length
    payload_start = metadata_end
    payload_end = payload_start + payload_length

    need(
        metadata_end >= metadata_start,
        "metadata span arithmetic overflow",
    )

    need(
        payload_end >= payload_start,
        "payload span arithmetic overflow",
    )

    need(
        payload_end == len(serialized),
        "serialized object contains truncated or trailing bytes",
    )

    metadata_raw = serialized[metadata_start:metadata_end]

    need(
        len(metadata_raw) == metadata_length,
        "metadata byte count mismatch",
    )

    metadata_sha = sha256_bytes(metadata_raw)

    need(
        metadata_sha == header["metadata_sha256"],
        "metadata SHA256 mismatch",
    )

    try:
        metadata = json.loads(
            metadata_raw.decode("utf-8")
        )
    except (
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as exc:
        raise Phase6ECIntegrityError(
            "invalid in-memory metadata JSON"
        ) from exc

    need(
        object_module.canonical_json_bytes(metadata) == metadata_raw,
        "metadata is not frozen canonical JSON",
    )

    object_module.validate_metadata(
        metadata,
        header,
    )

    payload = serialized[payload_start:payload_end]

    need(
        len(payload) == payload_length,
        "payload byte count mismatch",
    )

    payload_sha = sha256_bytes(payload)

    need(
        payload_sha == header["payload_sha256"],
        "payload SHA256 differs from header",
    )

    need(
        payload_sha == entry.payload_sha256,
        "payload SHA256 differs from generation placement",
    )

    return {
        "metadata_sha256": metadata_sha,
        "payload_offset": payload_start,
        "payload_length": payload_length,
        "payload_sha256": payload_sha,
        "tensor_name": metadata["tensor_name"],
        "tensor_type": metadata["tensor_type"],
        "dims": list(metadata["dims"]),
        "element_count": metadata["element_count"],
    }


# ---------------------------------------------------------------------------
# SCIENTIFIC ACCESS LEDGER + TELEMETRY
# ---------------------------------------------------------------------------


def execute_frozen_read_plan(
    segment_reader_module,
    object_module,
    telemetry_module,
    read_plan: dict[str, Any],
    catalog_pks: tuple[str, ...],
    entry_by_pk: dict[str, Any],
):
    accumulator = telemetry_module.TelemetryAccumulator(
        model_pk=SOURCE_MODEL_PK,
        source_generation_pk=SOURCE_GENERATION_PK,
        source_manifest_sha256=SOURCE_MANIFEST_SHA256,
    )

    sequence = 1
    global_event_ordinal = 1
    records = []
    scientific_records = 0
    fallback_controls = 0

    for plan_record in read_plan["records"]:
        query_id = plan_record["query_id"]
        query_class = plan_record["query_class"]
        planned_pks = tuple(
            plan_record["final_planned_treatment_pks"]
        )

        if query_class == "fallback_control":
            fallback_controls += 1

            records.append(
                {
                    "query_id": query_id,
                    "query_pk": plan_record["query_pk"],
                    "query_class": query_class,
                    "status": "CONTROL",
                    "planned_pks": list(planned_pks),
                    "successful_touch_events": [],
                    "failed_read_events": [],
                    "touched_pks": [],
                    "untouched_pks": list(catalog_pks),
                    "touched_serialized_bytes": 0,
                    "avoided_serialized_bytes": CATALOG_SERIALIZED_BYTES,
                    "avoided_object_count": CATALOG_OBJECT_COUNT,
                }
            )

            continue

        scientific_records += 1

        need(
            query_class in (
                "specific_intent",
                "multi_target_intent",
            ),
            "unexpected scientific query class",
        )

        need(
            len(planned_pks) == len(set(planned_pks)),
            "planned treatment contains duplicate PK",
        )

        need(
            all(pk in entry_by_pk for pk in planned_pks),
            "planned treatment contains PK outside generation entries",
        )

        successful_events = []
        failed_events = []
        touched = []
        touched_bytes = 0

        for object_pk in planned_pks:
            entry = entry_by_pk[object_pk]

            attempt = {
                "event_ordinal": global_event_ordinal,
                "query_id": query_id,
                "object_pk": object_pk,
                "generation_pk": entry.generation_pk,
                "segment_id": entry.segment_id,
                "segment_path": entry.segment_path,
                "offset": entry.offset,
                "serialized_span_length": entry.length,
                "expected_serialized_object_sha256": entry.object_file_sha256,
                "status": "ATTEMPTED",
            }

            global_event_ordinal += 1

            try:
                serialized = segment_reader_module.read_serialized_object(
                    entry,
                    SOURCE_GENERATION_PK,
                )

                parsed = parse_serialized_object_bytes(
                    object_module,
                    serialized,
                    entry,
                )

            except Exception as exc:
                failed = dict(attempt)
                failed["status"] = "FAILED"
                failed["error_type"] = (
                    type(exc).__module__
                    + "."
                    + type(exc).__qualname__
                )
                failed["error_message"] = str(exc)
                failed_events.append(failed)

                raise Phase6ECIntegrityError(
                    "authorized serialized-object read failed for "
                    + query_id
                    + " / "
                    + object_pk
                ) from exc

            event = dict(attempt)
            event.update(
                {
                    "status": "SUCCEEDED",
                    "observed_serialized_byte_length": len(serialized),
                    "observed_serialized_object_sha256": sha256_bytes(serialized),
                    "observed_payload_sha256": parsed["payload_sha256"],
                    "observed_payload_offset": parsed["payload_offset"],
                    "observed_payload_length": parsed["payload_length"],
                    "metadata_sha256": parsed["metadata_sha256"],
                    "tensor_name": parsed["tensor_name"],
                    "tensor_type": parsed["tensor_type"],
                    "dims": parsed["dims"],
                    "element_count": parsed["element_count"],
                }
            )

            successful_events.append(event)
            touched.append(object_pk)
            touched_bytes += entry.length

            telemetry_event = telemetry_module.TelemetryEvent(
                sequence=sequence,
                kind=telemetry_module.TelemetryEventKind.BYTES_READ,
                object_pk=object_pk,
                byte_count=entry.length,
            )

            accumulator.add_event(
                telemetry_event
            )

            sequence += 1

        touched_tuple = tuple(touched)

        need(
            touched_tuple == planned_pks,
            "event-sourced touched PKs differ from frozen planned PKs",
        )

        untouched = tuple(
            object_pk
            for object_pk in catalog_pks
            if object_pk not in set(touched_tuple)
        )

        avoided_bytes = (
            CATALOG_SERIALIZED_BYTES
            - touched_bytes
        )

        need(
            touched_bytes >= 0,
            "negative touched-byte arithmetic",
        )

        need(
            avoided_bytes >= 0,
            "negative avoided-byte arithmetic",
        )

        need(
            touched_bytes + avoided_bytes == CATALOG_SERIALIZED_BYTES,
            "catalog byte arithmetic does not close",
        )

        records.append(
            {
                "query_id": query_id,
                "query_pk": plan_record["query_pk"],
                "query_class": query_class,
                "status": "SCIENTIFIC_TRACE_FROZEN",
                "planned_pks": list(planned_pks),
                "successful_touch_events": successful_events,
                "failed_read_events": failed_events,
                "touched_pks": list(touched_tuple),
                "untouched_pks": list(untouched),
                "touched_serialized_bytes": touched_bytes,
                "avoided_serialized_bytes": avoided_bytes,
                "avoided_object_count": len(untouched),
            }
        )

    need(
        scientific_records == SCIENTIFIC_QUERY_COUNT,
        "scientific query denominator changed",
    )

    need(
        fallback_controls == FALLBACK_CONTROL_COUNT,
        "fallback control count changed",
    )

    snapshot = accumulator.snapshot()

    ledger_bytes_by_object = {}

    for record in records:
        if record["status"] == "CONTROL":
            continue

        for event in record["successful_touch_events"]:
            object_pk = event["object_pk"]

            ledger_bytes_by_object[object_pk] = (
                ledger_bytes_by_object.get(object_pk, 0)
                + event["serialized_span_length"]
            )

    telemetry_bytes_by_object = {
        row.object_pk: row.bytes_read
        for row in snapshot.object_aggregates
    }

    need(
        telemetry_bytes_by_object == ledger_bytes_by_object,
        "telemetry BYTES_READ accounting differs from independent event ledger",
    )

    total_successful_events = sum(
        len(record["successful_touch_events"])
        for record in records
    )

    need(
        snapshot.event_count == total_successful_events,
        "telemetry event count differs from successful read event count",
    )

    ledger = {
        "schema": ACCESS_LEDGER_SCHEMA,
        "phase": "6E-C",
        "source_model_pk": SOURCE_MODEL_PK,
        "source_generation_pk": SOURCE_GENERATION_PK,
        "source_manifest_sha256": SOURCE_MANIFEST_SHA256,
        "catalog_object_count": CATALOG_OBJECT_COUNT,
        "catalog_serialized_bytes": CATALOG_SERIALIZED_BYTES,
        "scientific_query_count": SCIENTIFIC_QUERY_COUNT,
        "fallback_control_count": FALLBACK_CONTROL_COUNT,
        "records": records,
        "telemetry": {
            "schema": snapshot.schema,
            "aggregation_version": snapshot.aggregation_version,
            "event_count": snapshot.event_count,
            "access_event_count": snapshot.access_event_count,
            "bytes_read_by_object": telemetry_bytes_by_object,
            "reconciled_with_event_ledger": True,
        },
        "prohibited_access_counters": {
            "source_gguf_payload_reads": 0,
            "direct_object_file_payload_reads": 0,
            "inspect_object_calls": 0,
            "dense_materializations": 0,
            "route_cache_uses": 0,
            "relationship_expansion_uses": 0,
            "network_accesses": 0,
            "duplicate_per_query_object_reads": 0,
            "unplanned_serialized_object_reads": 0,
        },
    }

    ledger_raw = canonical_bytes(ledger)
    ledger_sha = sha256_bytes(ledger_raw)

    forbidden_tokens = (
        b"required_object_pks",
        b"reference_payload_sha256",
        b"scientific_verdict",
        b"READ_COMPLETE_AND_AVOIDED",
    )

    need(
        all(token not in ledger_raw for token in forbidden_tokens),
        "access ledger contains reference-derived scientific classification",
    )

    return ledger, ledger_raw, ledger_sha


# ---------------------------------------------------------------------------
# REFERENCE SEMANTICS — ONLY AFTER ACCESS LEDGER FREEZE
# ---------------------------------------------------------------------------


def load_reference_after_access_freeze(reference_raw: bytes):
    need(
        reference_raw.endswith(b"\n"),
        "reference fixture must contain exactly one historical terminal LF",
    )

    need(
        not reference_raw.endswith(b"\n\n"),
        "reference fixture has more than one terminal LF",
    )

    semantic_raw = reference_raw[:-1]

    fixture = json.loads(
        semantic_raw.decode("utf-8")
    )

    need(
        canonical_bytes(fixture) == semantic_raw,
        "reference fixture is not canonical JSON plus one terminal LF",
    )

    required_top = {
        "source_model_pk",
        "source_generation_pk",
        "source_manifest_sha256",
        "source_gguf_sha256",
        "queries",
        "objects",
    }

    need(
        required_top <= set(fixture),
        "reference fixture missing required top-level fields",
    )

    need(
        fixture["source_model_pk"] == SOURCE_MODEL_PK,
        "reference model PK mismatch",
    )

    need(
        fixture["source_generation_pk"] == SOURCE_GENERATION_PK,
        "reference generation PK mismatch",
    )

    need(
        fixture["source_manifest_sha256"] == SOURCE_MANIFEST_SHA256,
        "reference manifest SHA mismatch",
    )

    need(
        fixture["source_gguf_sha256"] == SOURCE_GGUF_SHA256,
        "reference GGUF provenance SHA mismatch",
    )

    reference_queries = fixture["queries"]
    reference_objects = fixture["objects"]

    need(
        len(reference_queries) == QUERY_COUNT,
        "reference query count mismatch",
    )

    need(
        len(reference_objects) == CATALOG_OBJECT_COUNT,
        "reference object count mismatch",
    )

    query_by_id = {
        row["query_id"]: row
        for row in reference_queries
    }

    object_by_pk = {
        row["object_pk"]: row
        for row in reference_objects
    }

    need(
        len(query_by_id) == QUERY_COUNT,
        "duplicate reference query ID",
    )

    need(
        len(object_by_pk) == CATALOG_OBJECT_COUNT,
        "duplicate reference object PK",
    )

    return fixture, query_by_id, object_by_pk


# ---------------------------------------------------------------------------
# SCIENTIFIC EVALUATION AFTER PLAN + ACCESS TRACE ARE FROZEN
# ---------------------------------------------------------------------------


def evaluate_after_access_freeze(
    read_plan: dict[str, Any],
    access_ledger: dict[str, Any],
    reference_query_by_id: dict[str, dict[str, Any]],
    reference_object_by_pk: dict[str, dict[str, Any]],
    placement_by_pk: dict[str, dict[str, Any]],
):
    plan_by_id = {
        row["query_id"]: row
        for row in read_plan["records"]
    }

    ledger_by_id = {
        row["query_id"]: row
        for row in access_ledger["records"]
    }

    scientific_rows = []
    control_rows = []

    pass_count = 0
    read_complete_no_avoidance = 0
    read_incomplete = 0
    read_payload_mismatch = 0

    aggregate_treatment_bytes = 0
    aggregate_avoided_bytes = 0
    aggregate_full_reference_bytes = (
        SCIENTIFIC_QUERY_COUNT
        * CATALOG_SERIALIZED_BYTES
    )

    for query_id in tuple(plan_by_id):
        plan = plan_by_id[query_id]
        ledger = ledger_by_id[query_id]
        reference_query = reference_query_by_id[query_id]

        need(
            reference_query["query_text_sha256"]
            == plan["query_text_sha256"],
            "reference query text SHA mismatch: " + query_id,
        )

        if plan["query_class"] == "fallback_control":
            need(
                ledger["status"] == "CONTROL",
                "fallback ledger status mismatch",
            )

            control_rows.append(
                {
                    "query_id": query_id,
                    "query_pk": plan["query_pk"],
                    "query_class": plan["query_class"],
                    "classification": "CONTROL",
                    "planned_pks": plan["final_planned_treatment_pks"],
                    "touched_pks": [],
                }
            )

            continue

        required = tuple(
            reference_query["required_object_pks"]
        )

        need(
            required == tuple(sorted(required)),
            "reference required PKs are not in frozen sorted order: " + query_id,
        )

        planned = tuple(
            plan["final_planned_treatment_pks"]
        )

        touched = tuple(
            ledger["touched_pks"]
        )

        successful_event_by_pk = {
            event["object_pk"]: event
            for event in ledger["successful_touch_events"]
        }

        required_coverage = all(
            object_pk in touched
            for object_pk in required
        )

        payload_matches = True
        required_payload_evidence = []

        for object_pk in required:
            placement = placement_by_pk[object_pk]
            reference_object = reference_object_by_pk[object_pk]

            need(
                placement["payload_sha256"]
                == reference_object["payload_sha256"],
                "generation/reference payload SHA mismatch: " + object_pk,
            )

            event = successful_event_by_pk.get(object_pk)

            if event is None:
                payload_matches = False

                required_payload_evidence.append(
                    {
                        "object_pk": object_pk,
                        "descriptor_payload_sha256": placement["payload_sha256"],
                        "reference_payload_sha256": reference_object["payload_sha256"],
                        "observed_payload_sha256": None,
                        "payload_match": False,
                    }
                )

                continue

            observed = event["observed_payload_sha256"]
            reference_payload = reference_object["payload_sha256"]

            match = (
                observed == reference_payload
            )

            if not match:
                payload_matches = False

            required_payload_evidence.append(
                {
                    "object_pk": object_pk,
                    "descriptor_payload_sha256": placement["payload_sha256"],
                    "reference_payload_sha256": reference_payload,
                    "observed_payload_sha256": observed,
                    "payload_match": match,
                }
            )

        treatment_bytes = ledger["touched_serialized_bytes"]
        avoided_bytes = ledger["avoided_serialized_bytes"]
        avoided_count = ledger["avoided_object_count"]

        aggregate_treatment_bytes += treatment_bytes
        aggregate_avoided_bytes += avoided_bytes

        strict_subset = (
            len(touched) < CATALOG_OBJECT_COUNT
        )

        avoidance = all(
            (
                strict_subset,
                avoided_count > 0,
                avoided_bytes > 0,
                treatment_bytes < CATALOG_SERIALIZED_BYTES,
            )
        )

        if not required_coverage:
            classification = "READ_INCOMPLETE"
            read_incomplete += 1

        elif not payload_matches:
            classification = "READ_PAYLOAD_MISMATCH"
            read_payload_mismatch += 1

        elif not avoidance:
            classification = "READ_COMPLETE_NO_AVOIDANCE"
            read_complete_no_avoidance += 1

        else:
            classification = "READ_COMPLETE_AND_AVOIDED"
            pass_count += 1

        scientific_rows.append(
            {
                "query_id": query_id,
                "query_pk": plan["query_pk"],
                "query_class": plan["query_class"],
                "classification": classification,
                "planned_treatment_pks": list(planned),
                "touched_pks": list(touched),
                "untouched_catalog_pks": ledger["untouched_pks"],
                "required_object_pks": list(required),
                "required_object_coverage": required_coverage,
                "required_payload_evidence": required_payload_evidence,
                "catalog_object_count": CATALOG_OBJECT_COUNT,
                "treatment_object_count": len(touched),
                "untouched_object_count": avoided_count,
                "catalog_serialized_bytes": CATALOG_SERIALIZED_BYTES,
                "treatment_serialized_bytes": treatment_bytes,
                "avoided_serialized_bytes": avoided_bytes,
                "avoided_serialized_fraction": (
                    avoided_bytes
                    / CATALOG_SERIALIZED_BYTES
                ),
                "serialized_object_identity_verification": all(
                    event["observed_serialized_object_sha256"]
                    == event["expected_serialized_object_sha256"]
                    for event in ledger["successful_touch_events"]
                ),
                "prohibited_read_state": "PASS",
                "query_pass": (
                    classification == "READ_COMPLETE_AND_AVOIDED"
                ),
            }
        )

    need(
        len(scientific_rows) == SCIENTIFIC_QUERY_COUNT,
        "scientific result denominator mismatch",
    )

    need(
        len(control_rows) == FALLBACK_CONTROL_COUNT,
        "fallback result count mismatch",
    )

    need(
        aggregate_treatment_bytes
        + aggregate_avoided_bytes
        == aggregate_full_reference_bytes,
        "aggregate byte arithmetic does not close",
    )

    phase_pass = all(
        (
            pass_count == SCIENTIFIC_QUERY_COUNT,
            read_complete_no_avoidance == 0,
            read_incomplete == 0,
            read_payload_mismatch == 0,
        )
    )

    phase_verdict = (
        "PASS"
        if phase_pass
        else "FAIL"
    )

    return {
        "scientific_rows": scientific_rows,
        "control_rows": control_rows,
        "counts": {
            "scientific_query_count": SCIENTIFIC_QUERY_COUNT,
            "fallback_control_count": FALLBACK_CONTROL_COUNT,
            "read_complete_and_avoided": pass_count,
            "read_complete_no_avoidance": read_complete_no_avoidance,
            "read_incomplete": read_incomplete,
            "read_payload_mismatch": read_payload_mismatch,
        },
        "aggregate": {
            "full_reference_serialized_bytes": aggregate_full_reference_bytes,
            "treatment_serialized_bytes": aggregate_treatment_bytes,
            "avoided_serialized_bytes": aggregate_avoided_bytes,
            "avoided_serialized_fraction": (
                aggregate_avoided_bytes
                / aggregate_full_reference_bytes
            ),
        },
        "phase_verdict": phase_verdict,
    }


# ---------------------------------------------------------------------------
# RESULT
# ---------------------------------------------------------------------------


def build_result(
    frozen_runner_commit: str,
    runner_sha256: str,
    read_plan_sha256: str,
    access_ledger_sha256: str,
    access_ledger: dict[str, Any],
    evaluation: dict[str, Any],
):
    successful_events = sum(
        len(row["successful_touch_events"])
        for row in access_ledger["records"]
    )

    failed_events = sum(
        len(row["failed_read_events"])
        for row in access_ledger["records"]
    )

    result = {
        "schema": RESULT_SCHEMA,
        "phase": "6E-C",
        "status": "COMPLETE_SCIENTIFIC_RESULT",
        "bindings": {
            "preregistration_sha256": PREREG_SHA256,
            "runner_implementation_contract_sha256": CONTRACT_SHA256,
            "runner_source_sha256": runner_sha256,
            "runner_commit": frozen_runner_commit,
            "phase_6e_entry_checkpoint_sha256": ENTRY_CHECKPOINT_SHA256,
            "phase_6e_a_result_sha256": PHASE_6E_A_RESULT_SHA256,
            "phase_6e_a_verdict_sha256": PHASE_6E_A_VERDICT_SHA256,
            "phase_6e_b_s1_result_sha256": PHASE_6E_B_S1_RESULT_SHA256,
            "phase_6e_b_s1_verdict_sha256": PHASE_6E_B_S1_VERDICT_SHA256,
            "phase_6e_b_s1_trace_sha256": PHASE_6E_B_S1_TRACE_SHA256,
            "phase_6e_b_failure_incident_sha256": PHASE_6E_B_INCIDENT_SHA256,
            "query_fixture_sha256": QUERIES_SHA256,
            "catalog_sha256": CATALOG_SHA256,
            "selector_protocol_sha256": SELECTOR_PROTOCOL_SHA256,
            "selector_implementation_sha256": SELECTOR_SHA256,
            "capsule_protocol_sha256": CAPSULE_PROTOCOL_SHA256,
            "capsule_implementation_sha256": CAPSULE_SHA256,
            "generation_authority_sha256": GENERATION_AUTHORITY_SHA256,
            "generation_manifest_sha256": GENERATION_MANIFEST_SHA256,
            "reference_fixture_sha256": REFERENCE_FIXTURE_SHA256,
            "maf_object_implementation_sha256": MAF_OBJECT_SHA256,
            "resident_directory_sha256": RESIDENT_DIRECTORY_SHA256,
            "segment_reader_sha256": SEGMENT_READER_SHA256,
            "telemetry_data_model_sha256": TELEMETRY_MODEL_SHA256,
            "telemetry_runtime_integration_sha256": TELEMETRY_INTEGRATION_SHA256,
            "runtime_residency_sha256": RUNTIME_RESIDENCY_SHA256,
            "source_model_pk": SOURCE_MODEL_PK,
            "source_generation_pk": SOURCE_GENERATION_PK,
            "source_gguf_sha256_provenance_only": SOURCE_GGUF_SHA256,
            "read_plan_snapshot_sha256": read_plan_sha256,
            "access_ledger_sha256": access_ledger_sha256,
            "round_config_sha256": list(ROUND_CONFIG_SHA256),
        },
        "population": {
            "query_count": QUERY_COUNT,
            "scientific_query_count": SCIENTIFIC_QUERY_COUNT,
            "fallback_control_count": FALLBACK_CONTROL_COUNT,
            "catalog_object_count": CATALOG_OBJECT_COUNT,
            "catalog_serialized_bytes": CATALOG_SERIALIZED_BYTES,
        },
        "event_accounting": {
            "successful_serialized_object_read_events": successful_events,
            "failed_serialized_object_read_events": failed_events,
            "telemetry_event_count": access_ledger["telemetry"]["event_count"],
            "telemetry_access_event_count": access_ledger["telemetry"][
                "access_event_count"
            ],
            "telemetry_event_ledger_reconciled": access_ledger["telemetry"][
                "reconciled_with_event_ledger"
            ],
            "prohibited_access_counters": access_ledger[
                "prohibited_access_counters"
            ],
        },
        "scientific_boundary": {
            "object_state_payload_identity_only": True,
            "application_level_serialized_reads_observed": True,
            "application_level_serialized_object_read_claimed": True,
            "storage_device_physical_io_claimed": False,
            "hardware_physical_io_avoidance_claimed": False,
            "source_gguf_payload_accessed": False,
            "source_gguf_tensor_avoidance_claimed": False,
            "full_model_avoidance_claimed": False,
            "dense_materialization_executed": False,
            "dense_materialization_avoidance_claimed": False,
            "inference_executed": False,
            "output_fidelity_claimed": False,
            "answer_quality_claimed": False,
            "performance_claimed": False,
            "maf_native_compute": "disabled_unvalidated",
            "route_cache_used": False,
            "relationship_expansion_used": False,
            "reference_informed_route": False,
            "reference_informed_read_plan": False,
            "reference_informed_access_trace": False,
            "inspect_object_used_in_observation_window": False,
            "touched_pks_event_sourced": True,
            "metadata_reads_excluded_from_treatment_bytes": True,
            "counterfactual_full_reference_physically_read": False,
        },
        "counts": evaluation["counts"],
        "aggregate": evaluation["aggregate"],
        "scientific_queries": evaluation["scientific_rows"],
        "fallback_controls": evaluation["control_rows"],
        "phase_verdict": evaluation["phase_verdict"],
    }

    return result


def write_result_immutably(result: dict[str, Any]) -> tuple[bytes, str]:
    raw = canonical_bytes(result)
    digest = sha256_bytes(raw)

    fd = os.open(
        RESULT_PATH,
        os.O_WRONLY
        | os.O_CREAT
        | os.O_EXCL,
        0o644,
    )

    try:
        view = memoryview(raw)
        written = 0

        while written < len(view):
            count = os.write(
                fd,
                view[written:],
            )

            if count <= 0:
                raise Phase6ECIntegrityError(
                    "result write returned non-positive byte count"
                )

            written += count

        os.fsync(fd)

    finally:
        os.close(fd)

    reread = RESULT_PATH.read_bytes()

    need(
        reread == raw,
        "published result bytes differ from constructed canonical bytes",
    )

    need(
        sha256_bytes(reread) == digest,
        "published result SHA256 mismatch",
    )

    return raw, digest


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------


def main() -> int:
    frozen_runner_commit, runner_sha256 = verify_pre_execution_state()

    raw_by_path = load_and_verify_authority_bytes()

    selector_module = import_frozen_module(
        "maf_query_to_pk_selection_v1",
        SELECTOR_PATH,
        SELECTOR_SHA256,
    )

    capsule_module = import_frozen_module(
        "maf_query_capsule_data_model_v1",
        CAPSULE_PATH,
        CAPSULE_SHA256,
    )

    resident_module = import_frozen_module(
        "maf_resident_pk_directory_v1",
        RESIDENT_DIRECTORY_PATH,
        RESIDENT_DIRECTORY_SHA256,
    )

    segment_reader_module = import_frozen_module(
        "maf_segment_reader_v1",
        SEGMENT_READER_PATH,
        SEGMENT_READER_SHA256,
    )

    object_module = import_frozen_module(
        "maf_object_v1",
        MAF_OBJECT_PATH,
        MAF_OBJECT_SHA256,
    )

    telemetry_module = import_frozen_module(
        "maf_segment_locality_data_model_v1",
        TELEMETRY_MODEL_PATH,
        TELEMETRY_MODEL_SHA256,
    )

    (
        queries,
        catalog,
        catalog_pks,
    ) = load_non_oracle_inputs(
        selector_module,
        raw_by_path,
    )

    (
        _authority,
        _manifest,
        placement_by_pk,
        segment_record,
        segment_path,
    ) = load_generation_metadata(
        raw_by_path
    )

    need(
        set(catalog_pks) == set(placement_by_pk),
        "catalog and generation placement PK sets differ",
    )

    entry_by_pk = build_resident_entries(
        resident_module,
        catalog_pks,
        placement_by_pk,
        segment_record,
        segment_path,
    )

    # ---------------------------------------------------------------
    # NON-ORACLE BARRIER 1:
    # Freeze the full 40-query selector/read plan before reference parse.
    # ---------------------------------------------------------------

    (
        read_plan,
        _read_plan_raw,
        read_plan_sha256,
    ) = build_complete_read_plan(
        selector_module,
        capsule_module,
        queries,
        catalog,
        catalog_pks,
    )

    # ---------------------------------------------------------------
    # NON-ORACLE BARRIER 2:
    # Execute exactly the already-frozen plan for the 32 scientific
    # queries. No reference JSON semantics have been parsed yet.
    # ---------------------------------------------------------------

    (
        access_ledger,
        _access_ledger_raw,
        access_ledger_sha256,
    ) = execute_frozen_read_plan(
        segment_reader_module,
        object_module,
        telemetry_module,
        read_plan,
        catalog_pks,
        entry_by_pk,
    )

    # ---------------------------------------------------------------
    # REFERENCE BARRIER OPENS ONLY NOW:
    # The read plan and complete access trace are already immutable
    # canonical structures with SHA256 identities.
    # ---------------------------------------------------------------

    (
        _reference_fixture,
        reference_query_by_id,
        reference_object_by_pk,
    ) = load_reference_after_access_freeze(
        raw_by_path[REFERENCE_FIXTURE_PATH]
    )

    need(
        tuple(reference_query_by_id)
        == tuple(row["query_id"] for row in read_plan["records"]),
        "reference query order differs from frozen read-plan order",
    )

    need(
        set(reference_object_by_pk)
        == set(catalog_pks),
        "reference object PK set differs from frozen catalog",
    )

    evaluation = evaluate_after_access_freeze(
        read_plan,
        access_ledger,
        reference_query_by_id,
        reference_object_by_pk,
        placement_by_pk,
    )

    result = build_result(
        frozen_runner_commit,
        runner_sha256,
        read_plan_sha256,
        access_ledger_sha256,
        access_ledger,
        evaluation,
    )

    result_raw, result_sha = write_result_immutably(
        result
    )

    print("=" * 88)
    print(" OPENMIND / PHASE 6E-C ACTUAL SERIALIZED OBJECT READ AVOIDANCE V1")
    print("=" * 88)
    print("result path:      " + str(RESULT_PATH))
    print("result bytes:     " + str(len(result_raw)))
    print("result sha256:    " + result_sha)
    print("read-plan sha256: " + read_plan_sha256)
    print("access-ledger sha:" + access_ledger_sha256)
    print("scientific count: " + str(SCIENTIFIC_QUERY_COUNT))
    print("control count:    " + str(FALLBACK_CONTROL_COUNT))
    print(
        "pass count:       "
        + str(
            evaluation["counts"]["read_complete_and_avoided"]
        )
    )
    print(
        "no avoidance:     "
        + str(
            evaluation["counts"]["read_complete_no_avoidance"]
        )
    )
    print(
        "read incomplete:  "
        + str(
            evaluation["counts"]["read_incomplete"]
        )
    )
    print(
        "payload mismatch: "
        + str(
            evaluation["counts"]["read_payload_mismatch"]
        )
    )
    print(
        "treatment bytes:  "
        + str(
            evaluation["aggregate"]["treatment_serialized_bytes"]
        )
    )
    print(
        "avoided bytes:    "
        + str(
            evaluation["aggregate"]["avoided_serialized_bytes"]
        )
    )
    print("phase verdict:     " + evaluation["phase_verdict"])
    print("=" * 88)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())

    except FileExistsError:
        print(
            "PHASE 6E-C INFRASTRUCTURE/INTEGRITY FAILURE: "
            "result path already exists",
            file=sys.stderr,
        )
        raise SystemExit(2)

    except Phase6ECIntegrityError as exc:
        print(
            "PHASE 6E-C INFRASTRUCTURE/INTEGRITY FAILURE: "
            + str(exc),
            file=sys.stderr,
        )
        raise SystemExit(2)

    except Exception as exc:
        print(
            "PHASE 6E-C INFRASTRUCTURE/INTEGRITY FAILURE: "
            + type(exc).__module__
            + "."
            + type(exc).__qualname__
            + ": "
            + str(exc),
            file=sys.stderr,
        )
        raise SystemExit(2)
