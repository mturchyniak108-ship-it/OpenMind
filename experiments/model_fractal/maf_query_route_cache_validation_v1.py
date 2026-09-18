#!/usr/bin/env python3
from __future__ import annotations

import copy
import ctypes
import errno
import hashlib
import json
import logging
import math
import os
import tempfile
from dataclasses import replace
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable

from maf_query_capsule_data_model_v1 import MAFQueryCapsuleV1, derive_query_pk
from maf_query_to_pk_selection_v1 import (
    MAFQueryPKCatalogV1,
    MAFQueryToPKSelectionConfigV1,
    select_query_to_pks_v1,
)
from maf_resident_pk_directory_v1 import (
    OBJECT_PK_KIND,
    ResidentPKEntry,
    ResidentPKSnapshot,
)
from maf_query_route_cache_v1 import (
    SCHEMA_V1,
    MAFQueryRouteCacheError,
    MAFQueryRouteCacheDataError,
    MAFQueryRouteCacheIdentityError,
    MAFQueryRouteCacheIntegrityError,
    MAFQueryRouteCacheObjectPKError,
    MAFQueryRouteCacheRelationshipPKError,
    MAFQueryRouteCacheRecordV1,
    build_route_cache_record_v1,
    derive_cache_pk_v1,
    derive_route_payload_sha256_v1,
    read_route_cache_record_v1,
    validate_route_cache_for_reuse_v1,
    validated_route_payload_v1,
    write_route_cache_record_v1,
)

LOGGER = logging.getLogger("openmind.maf_query_route_cache_validation_v1")

HERE = Path(__file__).resolve().parent
RUNNER_PATH = Path(__file__).resolve()

ARCHITECTURE_PATH = HERE / "MAF_QUERY_SCOPED_WORKING_SET_ARCHITECTURE.md"
Q4_PROTOCOL_PATH = HERE / "MAF_QUERY_ROUTE_CACHE_VALIDATION_V1_PROTOCOL.md"
RUNNER_CONTRACT_PATH = HERE / "MAF_QUERY_ROUTE_CACHE_VALIDATION_RUNNER_IMPLEMENTATION_CONTRACT_V1.md"
PRODUCTION_MODULE_PATH = HERE / "maf_query_route_cache_v1.py"
Q2_SELECTOR_PATH = HERE / "maf_query_to_pk_selection_v1.py"
Q2_RUNNER_EVIDENCE_PATH = HERE / "maf_query_to_pk_selection_validation_v1_4.py"
Q2_RESULT_PATH = HERE / "maf_query_to_pk_selection_validation_v1_4.json"
Q2_CATALOG_PATH = HERE / "maf_query_to_pk_selection_validation_v1_catalog.json"
Q2_QUERY_FIXTURE_PATH = HERE / "maf_query_to_pk_selection_validation_v1_queries.json"
Q3_RUNNER_EVIDENCE_PATH = HERE / "maf_query_capsule_attach_detach_cleanup_validation_v1_1.py"
Q3_RESULT_PATH = HERE / "maf_query_capsule_attach_detach_cleanup_validation_v1_1.json"
Q3_SLOT_PATH = HERE / "maf_query_capsule_attach_detach_cleanup_validation_v1_1.slot"
Q3_VERDICT_PATH = HERE / "MAF_QUERY_CAPSULE_ATTACH_DETACH_CLEANUP_VALIDATION_V1_1_VERDICT.md"

RESULT_PATH = HERE / "maf_query_route_cache_validation_v1.json"
SLOT_PATH = HERE / "maf_query_route_cache_validation_v1.slot"
PARTIAL_PATH = HERE / "maf_query_route_cache_validation_v1.json.partial"

RESULT_SCHEMA = "openmind.maf_query_route_cache_validation.v1"
PREPARED_SCHEMA = "openmind.maf_query_route_cache_validation.slot.prepared.v1"
RESERVED_SCHEMA = "openmind.maf_query_route_cache_validation.slot.reserved_durable.v1"
PUBLISHED_SCHEMA = "openmind.maf_query_route_cache_validation.slot.published_durable.v1"

EXPECTED_ARCHITECTURE_SHA256 = "7df826096e506d13502e442fb11f7e1f18fb2c5a342f4214b91a3c3df043559c"
EXPECTED_Q4_PROTOCOL_SHA256 = "af587bfe685deb86ac4574b3d41d1a80b5df2cec84bce757eac8c7e307d82ad9"
EXPECTED_RUNNER_CONTRACT_SHA256 = "1d57f67e5944c6a04e50c3f18c458872b56cf45937ba04b72d529b0b78aec20c"
EXPECTED_PRODUCTION_MODULE_SHA256 = "a168528b47b2575fb18dc68d36a1c31ab6390534a779d5c769299a3dc891d507"
EXPECTED_CHECK_MATRIX_SHA256 = "8dc81ec92bace5678a983332cdb6aa342ba7341273a18ee51346f96e1a6414da"
EXPECTED_Q2_SELECTOR_SHA256 = "e21c05e352fe921b791e8c936425727a98911ce7566989672a96bfd2b9613fa2"
EXPECTED_Q2_RUNNER_SHA256 = "7bda960c125786fdf3cfca65c4b7b5851ca8bd91257282facfee2fec1ae7a030"
EXPECTED_Q2_RESULT_SHA256 = "b2ad49d7a9a3e1ef565e07e595efc4a4e00b283f422723553c6437ef3a42def6"
EXPECTED_Q2_CATALOG_SHA256 = "c51ef0fabeb10e7c8a091a093aa1934620a69b2026b5a87cb02477b9dd7ca900"
EXPECTED_Q2_QUERY_FIXTURE_SHA256 = "32f4636bd5e8ceee0dca8342335279a6f8e6acafe866a5469f2c23aa2655202a"
EXPECTED_Q2_SELECTION_CONFIG_SHA256 = "0caeaeaafdd870e6b02ccc8b4450576883d4ef5234ba689c472e3b14d9dbe120"
EXPECTED_Q2_SELECTION_PROTOCOL_SHA256 = "b42a0643976c2393871e3b826ba5573b4de981b49603de63230d69cf57be0811"
EXPECTED_Q3_RUNNER_SHA256 = "26b4bef94fa5f063f7340190879d37b124bba305da60ac0abc12e83433159f99"
EXPECTED_Q3_RESULT_SHA256 = "2db54aca02c913ff9c54728aeb63bca6f280296a8564ef6a388be2e994290690"
EXPECTED_Q3_SLOT_SHA256 = "d20826af7c080b8660233ae9790fc761cbcd81d4bb45e9e033177f981455fa95"
EXPECTED_Q3_VERDICT_SHA256 = "57233349f5d79f7dd00ac1a436cd3b109153d551b416ccdd32e85ef9e3ff0d0a"

EXPECTED_SOURCE_GENERATION_PK = "mafgen:v1:45a80a2aa271ce04853003185b6a1227cb309bd1e3e2dc538eea849fac9f5db0"
EXPECTED_SOURCE_MANIFEST_SHA256 = "28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3"

FROZEN_CASE_IDS = ("q001", "q025", "q026", "q033")
FROZEN_CASE_TEXT = {
    "q001": ("specific_intent", "layer 0 attention query"),
    "q025": ("multi_target_intent", "layer 0 normalization"),
    "q026": ("multi_target_intent", "layer 0 attention"),
    "q033": ("fallback_control", "weather tomorrow"),
}

CHECK_IDS = tuple(f"Q4-V{i:02d}" for i in range(1, 45))

CLAIM_BOUNDARY = {
    "claim_scope": "safe_generation_bound_route_metadata_persistence_reuse_invalidation_only",
    "inference_executed": False,
    "answer_generation_executed": False,
    "working_set_sufficiency_tested": False,
    "route_expansion_optimality_claimed": False,
    "performance_metrics_emitted": False,
    "performance_superiority_claimed": False,
    "output_parity_claimed": False,
    "llm_replacement_claimed": False,
    "maf_native_compute_claimed": False,
    "phase_6e_entered": False,
}

_AT_FDCWD = -100
_RENAME_NOREPLACE = 1


class Q4ValidationHarnessError(RuntimeError):
    pass


class Q4ValidationAuthorityError(Q4ValidationHarnessError):
    pass


class Q4ValidationPersistenceError(Q4ValidationHarnessError):
    pass


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _sha256_file(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8") + b"\n"


def _json_load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise Q4ValidationAuthorityError(message)


def _require_sha(path: Path, expected: str, label: str) -> None:
    actual = _sha256_file(path)
    if actual != expected:
        raise Q4ValidationAuthorityError(
            f"{label} SHA256 mismatch: expected {expected}, got {actual}"
        )


def _fsync_directory(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _rename_noreplace(src: Path, dst: Path) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    func = getattr(libc, "renameat2", None)
    if func is None:
        raise Q4ValidationPersistenceError("renameat2 unavailable")
    func.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    ]
    func.restype = ctypes.c_int
    rc = func(
        _AT_FDCWD,
        os.fsencode(src),
        _AT_FDCWD,
        os.fsencode(dst),
        _RENAME_NOREPLACE,
    )
    if rc != 0:
        err = ctypes.get_errno()
        if err == errno.EEXIST:
            raise FileExistsError(dst)
        raise Q4ValidationPersistenceError(
            f"renameat2(RENAME_NOREPLACE) failed with errno {err}"
        )


def _append_journal_record(path: Path, record: dict[str, Any], *, create: bool) -> str:
    raw = _json_bytes(record)
    flags = os.O_WRONLY
    if create:
        flags |= os.O_CREAT | os.O_EXCL
    else:
        flags |= os.O_APPEND
    fd = os.open(path, flags, 0o600)
    try:
        with os.fdopen(fd, "ab" if not create else "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        LOGGER.exception("slot journal write failed")
        raise
    _fsync_directory(path.parent)
    return _sha256_bytes(raw.rstrip(b"\n"))


def _reserve_slot(runner_sha256: str) -> dict[str, str]:
    prepared = {
        "schema": PREPARED_SCHEMA,
        "sequence": 1,
        "state": "RESERVATION_PREPARED",
        "protocol_sha256": EXPECTED_Q4_PROTOCOL_SHA256,
        "runner_contract_sha256": EXPECTED_RUNNER_CONTRACT_SHA256,
        "runner_sha256": runner_sha256,
        "production_module_sha256": EXPECTED_PRODUCTION_MODULE_SHA256,
        "check_matrix_sha256": EXPECTED_CHECK_MATRIX_SHA256,
        "final_basename": RESULT_PATH.name,
        "partial_basename": PARTIAL_PATH.name,
    }
    prepared_sha = _append_journal_record(SLOT_PATH, prepared, create=True)
    reserved = {
        "schema": RESERVED_SCHEMA,
        "sequence": 2,
        "state": "RESERVED_DURABLE",
        "prepared_record_sha256": prepared_sha,
    }
    reserved_sha = _append_journal_record(SLOT_PATH, reserved, create=False)
    return {
        "prepared_record_sha256": prepared_sha,
        "reserved_durable_record_sha256": reserved_sha,
    }


def _publish_result(result: dict[str, Any], reservation: dict[str, str]) -> str:
    raw = _json_bytes(result)
    if PARTIAL_PATH.exists() or RESULT_PATH.exists():
        raise FileExistsError("Q4 result namespace is not unused")
    fd = os.open(PARTIAL_PATH, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        LOGGER.exception("Q4 partial-result write failed")
        raise
    _rename_noreplace(PARTIAL_PATH, RESULT_PATH)
    _fsync_directory(RESULT_PATH.parent)
    result_sha = _sha256_file(RESULT_PATH)
    published = {
        "schema": PUBLISHED_SCHEMA,
        "sequence": 3,
        "state": "PUBLISHED_DURABLE",
        "reserved_durable_record_sha256": reservation["reserved_durable_record_sha256"],
        "final_result_basename": RESULT_PATH.name,
        "final_result_bytes": len(raw),
        "final_result_sha256": result_sha,
    }
    _append_journal_record(SLOT_PATH, published, create=False)
    return result_sha


def _preflight_authorities() -> dict[str, Any]:
    authorities = (
        (ARCHITECTURE_PATH, EXPECTED_ARCHITECTURE_SHA256, "primary architecture"),
        (Q4_PROTOCOL_PATH, EXPECTED_Q4_PROTOCOL_SHA256, "Q4 protocol"),
        (RUNNER_CONTRACT_PATH, EXPECTED_RUNNER_CONTRACT_SHA256, "runner contract"),
        (PRODUCTION_MODULE_PATH, EXPECTED_PRODUCTION_MODULE_SHA256, "production module"),
        (Q2_SELECTOR_PATH, EXPECTED_Q2_SELECTOR_SHA256, "Q2 selector"),
        (Q2_RUNNER_EVIDENCE_PATH, EXPECTED_Q2_RUNNER_SHA256, "Q2 runner evidence"),
        (Q2_RESULT_PATH, EXPECTED_Q2_RESULT_SHA256, "Q2 result"),
        (Q2_CATALOG_PATH, EXPECTED_Q2_CATALOG_SHA256, "Q2 catalog"),
        (Q2_QUERY_FIXTURE_PATH, EXPECTED_Q2_QUERY_FIXTURE_SHA256, "Q2 query fixture"),
        (Q3_RUNNER_EVIDENCE_PATH, EXPECTED_Q3_RUNNER_SHA256, "Q3 runner evidence"),
        (Q3_RESULT_PATH, EXPECTED_Q3_RESULT_SHA256, "Q3 result"),
        (Q3_SLOT_PATH, EXPECTED_Q3_SLOT_SHA256, "Q3 slot"),
        (Q3_VERDICT_PATH, EXPECTED_Q3_VERDICT_SHA256, "Q3 verdict"),
    )
    for path, expected, label in authorities:
        _require_sha(path, expected, label)
    _require(not RESULT_PATH.exists(), "Q4 result already exists")
    _require(not SLOT_PATH.exists(), "Q4 slot already exists")
    _require(not PARTIAL_PATH.exists(), "Q4 partial already exists")

    q2_result = _json_load(Q2_RESULT_PATH)
    q2_fixture = _json_load(Q2_QUERY_FIXTURE_PATH)
    q2_catalog = _json_load(Q2_CATALOG_PATH)
    q3_result = _json_load(Q3_RESULT_PATH)
    q3_verdict_text = Q3_VERDICT_PATH.read_text(encoding="utf-8")

    _require(q2_result.get("all_pass") is True, "Q2 result is not PASS")
    _require(q2_result.get("implementation_sha256") == EXPECTED_Q2_SELECTOR_SHA256, "Q2 selector binding mismatch")
    _require(q2_result.get("selection_protocol_sha256") == EXPECTED_Q2_SELECTION_PROTOCOL_SHA256, "Q2 selection protocol binding mismatch")
    _require(q2_result.get("selection_config_sha256") == EXPECTED_Q2_SELECTION_CONFIG_SHA256, "Q2 selection config binding mismatch")
    _require(q2_result.get("source_generation_pk") == EXPECTED_SOURCE_GENERATION_PK, "Q2 generation binding mismatch")
    _require(q2_result.get("source_manifest_sha256") == EXPECTED_SOURCE_MANIFEST_SHA256, "Q2 manifest binding mismatch")
    _require(q2_result.get("validation_runner_sha256") == EXPECTED_Q2_RUNNER_SHA256, "Q2 runner evidence binding mismatch")

    _require(q3_result.get("all_pass") is True, "Q3 result is not PASS")
    _require(q3_result.get("check_count") == 48, "Q3 check count mismatch")
    _require(q3_result.get("source_generation_pk") == EXPECTED_SOURCE_GENERATION_PK, "Q3 generation binding mismatch")
    _require(q3_result.get("source_manifest_sha256") == EXPECTED_SOURCE_MANIFEST_SHA256, "Q3 manifest binding mismatch")
    _require(q3_result.get("validation_runner_sha256") == EXPECTED_Q3_RUNNER_SHA256, "Q3 runner binding mismatch")
    _require(q3_result.get("exact_once", {}).get("slot_state") == "SPENT", "Q3 slot state is not SPENT")
    _require("must never be rerun" in q3_verdict_text.lower(), "Q3 non-rerunnable verdict text missing")

    _require(q2_fixture.get("source_generation_pk") == EXPECTED_SOURCE_GENERATION_PK, "fixture generation mismatch")
    _require(q2_fixture.get("source_manifest_sha256") == EXPECTED_SOURCE_MANIFEST_SHA256, "fixture manifest mismatch")
    _require(q2_fixture.get("catalog_sha256") == EXPECTED_Q2_CATALOG_SHA256, "fixture catalog binding mismatch")
    _require(len(q2_fixture.get("queries", [])) == 40, "Q2 query count mismatch")
    _require(q2_catalog.get("source_generation_pk") == EXPECTED_SOURCE_GENERATION_PK, "catalog generation mismatch")
    _require(q2_catalog.get("source_manifest_sha256") == EXPECTED_SOURCE_MANIFEST_SHA256, "catalog manifest mismatch")

    q3_cases = q3_result.get("query_cases", {})
    _require(tuple(q3_cases) == FROZEN_CASE_IDS, "Q3 frozen-case ordering mismatch")
    for query_id in FROZEN_CASE_IDS:
        expected_class, expected_text = FROZEN_CASE_TEXT[query_id]
        case = q3_cases[query_id]
        _require(case.get("query_class") == expected_class, f"{query_id} class mismatch")
        _require(case.get("query_text") == expected_text, f"{query_id} text mismatch")

    return {
        "q2_result": q2_result,
        "q2_fixture": q2_fixture,
        "q2_catalog": q2_catalog,
        "q3_result": q3_result,
    }


def _synthetic_hash(label: str, object_pk: str) -> str:
    return hashlib.sha256(f"{label}:{object_pk}".encode("utf-8")).hexdigest()


def _build_resident_snapshot(q2_catalog: dict[str, Any], q3_result: dict[str, Any]) -> ResidentPKSnapshot:
    model_pk = q3_result["model_pk"]
    active_record_sha256 = q3_result["active_record_sha256"]
    entries: dict[tuple[str, str, str], ResidentPKEntry] = {}
    for item in q2_catalog["entries"]:
        object_pk = item["object_pk"]
        length = max(1, int(item["element_count"]))
        digest = _synthetic_hash("segment", object_pk)
        entry = ResidentPKEntry(
            model_pk=model_pk,
            generation_pk=EXPECTED_SOURCE_GENERATION_PK,
            generation_manifest_sha256=EXPECTED_SOURCE_MANIFEST_SHA256,
            object_pk=object_pk,
            segment_id="mafsegment:v1:" + digest,
            offset=0,
            length=length,
            object_file_sha256=_synthetic_hash("object-file", object_pk),
            payload_sha256=_synthetic_hash("payload", object_pk),
            segment_length=length,
            segment_sha256=digest,
            segment_path=str(HERE / ("q4-validation-" + digest + ".mafseg")),
        )
        entries[(model_pk, OBJECT_PK_KIND, object_pk)] = entry
    return ResidentPKSnapshot(
        model_pk=model_pk,
        generation_pk=EXPECTED_SOURCE_GENERATION_PK,
        generation_manifest_sha256=EXPECTED_SOURCE_MANIFEST_SHA256,
        active_record_sha256=active_record_sha256,
        entries=MappingProxyType(entries),
    )


def _primitive_metadata_only(value: Any) -> bool:
    if value is None or isinstance(value, (str, bool, int)):
        return True
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, list):
        return all(_primitive_metadata_only(item) for item in value)
    if isinstance(value, dict):
        return all(
            isinstance(key, str) and _primitive_metadata_only(item)
            for key, item in value.items()
        )
    return False


def _forbidden_metadata_keys(value: Any) -> list[str]:
    forbidden_tokens = (
        "tensor_bytes",
        "dense",
        "serialized_maf",
        "mmap",
        "file_descriptor",
        "runtime_ref",
        "pin",
        "lease",
        "capsule_ref",
        "engine_handle",
    )
    hits: list[str] = []

    def walk(item: Any, prefix: str) -> None:
        if isinstance(item, dict):
            for key, child in item.items():
                lowered = key.lower()
                if any(token == lowered or lowered.endswith("_" + token) for token in forbidden_tokens):
                    hits.append(prefix + key)
                walk(child, prefix + key + ".")
        elif isinstance(item, list):
            for index, child in enumerate(item):
                walk(child, prefix + str(index) + ".")

    walk(value, "")
    return hits


def _expect_q4_rejection(
    expected_error: type[MAFQueryRouteCacheError],
    action: Callable[[], Any],
) -> bool:
    try:
        action()
    except MAFQueryRouteCacheError as exc:
        return type(exc) is expected_error
    return False


def _validate_reuse(
    record: MAFQueryRouteCacheRecordV1,
    capsule: MAFQueryCapsuleV1,
    snapshot: ResidentPKSnapshot,
    relationship_authority: frozenset[str],
    model_pk: str,
) -> None:
    validate_route_cache_for_reuse_v1(
        record=record,
        expected_query_signature=capsule.query_signature,
        expected_source_generation_pk=capsule.source_generation_pk,
        expected_source_manifest_sha256=capsule.source_manifest_sha256,
        expected_selection_config_sha256=capsule.selection_config_sha256,
        expected_expansion_policy=capsule.expansion_policy,
        expected_max_object_budget=capsule.max_object_budget,
        expected_max_expansion_rounds=capsule.max_expansion_rounds,
        model_pk=model_pk,
        resident_snapshot=snapshot,
        relationship_authority_pks=relationship_authority,
    )


def _replace_first(values: tuple[str, ...], old: str, new: str) -> tuple[str, ...]:
    out = list(values)
    try:
        index = out.index(old)
    except ValueError as exc:
        raise Q4ValidationHarnessError("object PK not present in route payload") from exc
    out[index] = new
    return tuple(out)


def _run_science(authority: dict[str, Any], runner_sha256: str) -> dict[str, Any]:
    q2_result = authority["q2_result"]
    q2_fixture = authority["q2_fixture"]
    q2_catalog_mapping = authority["q2_catalog"]
    q3_result = authority["q3_result"]

    catalog = MAFQueryPKCatalogV1.from_mapping(q2_catalog_mapping)
    config = MAFQueryToPKSelectionConfigV1.from_mapping(q2_fixture["selection_config"])

    _require(catalog.catalog_sha256() == EXPECTED_Q2_CATALOG_SHA256, "catalog canonical SHA mismatch")
    _require(config.selection_config_sha256() == EXPECTED_Q2_SELECTION_CONFIG_SHA256, "selection-config canonical SHA mismatch")

    query_records = {record["query_id"]: record for record in q2_fixture["queries"]}
    _require(all(query_id in query_records for query_id in FROZEN_CASE_IDS), "frozen query missing from Q2 fixture")

    q3_cases = q3_result["query_cases"]
    snapshot = _build_resident_snapshot(q2_catalog_mapping, q3_result)
    model_pk = q3_result["model_pk"]
    relationship_authority = frozenset(
        relationship_pk
        for query_id in FROZEN_CASE_IDS
        for relationship_pk in q3_cases[query_id]["capsule"]["selected_relationship_pks"]
    )

    checks: dict[str, bool] = {check_id: False for check_id in CHECK_IDS}
    details: dict[str, str] = {}
    case_results: dict[str, Any] = {}
    records: dict[str, MAFQueryRouteCacheRecordV1] = {}
    capsules: dict[str, MAFQueryCapsuleV1] = {}

    def mark(check_id: str, passed: bool, detail: str = "PASS") -> None:
        if check_id not in checks:
            raise Q4ValidationHarnessError(f"unknown check id {check_id}")
        checks[check_id] = bool(passed)
        details[check_id] = detail if passed else "FAIL: " + detail

    mark("Q4-V01", _sha256_file(ARCHITECTURE_PATH) == EXPECTED_ARCHITECTURE_SHA256)
    mark("Q4-V02", _sha256_file(Q3_VERDICT_PATH) == EXPECTED_Q3_VERDICT_SHA256)
    mark("Q4-V03", _sha256_file(Q3_RESULT_PATH) == EXPECTED_Q3_RESULT_SHA256)
    mark("Q4-V04", _sha256_file(Q3_SLOT_PATH) == EXPECTED_Q3_SLOT_SHA256)
    mark("Q4-V05", q3_result["all_pass"] is True and q3_result["exact_once"]["slot_state"] == "SPENT" and q3_result["boundary"]["q4_entered"] is False)
    mark("Q4-V06", _sha256_file(Q2_SELECTOR_PATH) == EXPECTED_Q2_SELECTOR_SHA256 and q2_result["selection_protocol_sha256"] == EXPECTED_Q2_SELECTION_PROTOCOL_SHA256 and q2_result["validation_runner_sha256"] == EXPECTED_Q2_RUNNER_SHA256)
    mark("Q4-V07", q2_fixture["source_generation_pk"] == EXPECTED_SOURCE_GENERATION_PK and q2_fixture["source_manifest_sha256"] == EXPECTED_SOURCE_MANIFEST_SHA256 and q3_result["source_generation_pk"] == EXPECTED_SOURCE_GENERATION_PK and q3_result["source_manifest_sha256"] == EXPECTED_SOURCE_MANIFEST_SHA256)
    mark("Q4-V08", tuple(q3_cases) == FROZEN_CASE_IDS)

    for query_id in FROZEN_CASE_IDS:
        fixture_record = query_records[query_id]
        query_class, query_text = FROZEN_CASE_TEXT[query_id]
        _require(fixture_record["query_class"] == query_class, f"{query_id} fixture class mismatch")
        _require(fixture_record["query_text"] == query_text, f"{query_id} fixture text mismatch")

        selection = select_query_to_pks_v1(
            query=query_text,
            catalog=catalog,
            config=config,
            source_generation_pk=EXPECTED_SOURCE_GENERATION_PK,
            source_manifest_sha256=EXPECTED_SOURCE_MANIFEST_SHA256,
        )
        frozen_selection = q3_cases[query_id]["selection"]
        _require(selection.to_dict() == frozen_selection, f"{query_id} production selector diverged from frozen Q3 evidence")

        capsule = MAFQueryCapsuleV1.from_mapping(q3_cases[query_id]["capsule"])
        _require(
            capsule.query_pk == derive_query_pk(
                query_signature=selection.query_signature,
                selection_config_sha256=selection.selection_config_sha256,
                source_generation_pk=selection.source_generation_pk,
                source_manifest_sha256=selection.source_manifest_sha256,
            ),
            f"{query_id} query PK mismatch",
        )
        _require(tuple(selection.selected_object_pks) == capsule.initial_object_pks, f"{query_id} initial object PK mismatch")

        record = build_route_cache_record_v1(capsule)
        records[query_id] = record
        capsules[query_id] = capsule

        expected_cache_pk = derive_cache_pk_v1(
            query_signature=capsule.query_signature,
            source_generation_pk=capsule.source_generation_pk,
            source_manifest_sha256=capsule.source_manifest_sha256,
            selection_config_sha256=capsule.selection_config_sha256,
            expansion_policy=capsule.expansion_policy,
            max_object_budget=capsule.max_object_budget,
            max_expansion_rounds=capsule.max_expansion_rounds,
        )
        expected_payload_sha = derive_route_payload_sha256_v1(
            initial_object_pks=capsule.initial_object_pks,
            selected_relationship_pks=capsule.selected_relationship_pks,
            route_order=capsule.route_order,
        )

        _validate_reuse(record, capsule, snapshot, relationship_authority, model_pk)
        payload = validated_route_payload_v1(record)

        case_results[query_id] = {
            "query_class": query_class,
            "query_text": query_text,
            "query_signature": capsule.query_signature,
            "cache_pk": record.cache_pk,
            "route_payload_sha256": record.route_payload_sha256,
            "initial_object_pks": list(record.initial_object_pks),
            "selected_relationship_pks": list(record.selected_relationship_pks),
            "route_order": list(record.route_order),
            "reuse_accepted": True,
            "validated_route_payload": copy.deepcopy(payload),
        }

        _require(record.schema == SCHEMA_V1, f"{query_id} cache schema mismatch")
        _require(record.cache_pk == expected_cache_pk, f"{query_id} cache PK mismatch")
        _require(record.canonical_bytes() == MAFQueryRouteCacheRecordV1.from_json_bytes(record.canonical_bytes()).canonical_bytes(), f"{query_id} canonical serialization mismatch")
        _require(record.query_signature == capsule.query_signature, f"{query_id} query signature mismatch")
        _require(record.source_generation_pk == capsule.source_generation_pk, f"{query_id} generation mismatch")
        _require(record.source_manifest_sha256 == capsule.source_manifest_sha256, f"{query_id} manifest mismatch")
        _require(record.selection_config_sha256 == capsule.selection_config_sha256, f"{query_id} selection config mismatch")
        _require(record.expansion_policy == capsule.expansion_policy, f"{query_id} expansion policy mismatch")
        _require(record.max_object_budget == capsule.max_object_budget, f"{query_id} object budget mismatch")
        _require(record.max_expansion_rounds == capsule.max_expansion_rounds, f"{query_id} expansion-round mismatch")
        _require(record.initial_object_pks == capsule.initial_object_pks, f"{query_id} initial payload mismatch")
        _require(record.selected_relationship_pks == capsule.selected_relationship_pks, f"{query_id} relationship payload mismatch")
        _require(record.route_order == capsule.route_order, f"{query_id} route order mismatch")
        _require(record.route_payload_sha256 == expected_payload_sha, f"{query_id} route payload digest mismatch")

    all_records = tuple(records[query_id] for query_id in FROZEN_CASE_IDS)
    all_capsules = tuple(capsules[query_id] for query_id in FROZEN_CASE_IDS)

    mark("Q4-V09", all(record.schema == SCHEMA_V1 for record in all_records))
    mark("Q4-V10", all(record.cache_pk == derive_cache_pk_v1(query_signature=capsule.query_signature, source_generation_pk=capsule.source_generation_pk, source_manifest_sha256=capsule.source_manifest_sha256, selection_config_sha256=capsule.selection_config_sha256, expansion_policy=capsule.expansion_policy, max_object_budget=capsule.max_object_budget, max_expansion_rounds=capsule.max_expansion_rounds) for record, capsule in zip(all_records, all_capsules)))
    mark("Q4-V11", all(record.canonical_bytes() == MAFQueryRouteCacheRecordV1.from_json_bytes(record.canonical_bytes()).canonical_bytes() for record in all_records))
    mark("Q4-V12", all(r.query_signature == c.query_signature for r, c in zip(all_records, all_capsules)))
    mark("Q4-V13", all(r.source_generation_pk == c.source_generation_pk for r, c in zip(all_records, all_capsules)))
    mark("Q4-V14", all(r.source_manifest_sha256 == c.source_manifest_sha256 for r, c in zip(all_records, all_capsules)))
    mark("Q4-V15", all(r.selection_config_sha256 == c.selection_config_sha256 for r, c in zip(all_records, all_capsules)))
    mark("Q4-V16", all(r.expansion_policy == c.expansion_policy and r.max_object_budget == c.max_object_budget and r.max_expansion_rounds == c.max_expansion_rounds for r, c in zip(all_records, all_capsules)))
    mark("Q4-V17", all(r.initial_object_pks == c.initial_object_pks for r, c in zip(all_records, all_capsules)))
    mark("Q4-V18", all(r.selected_relationship_pks == c.selected_relationship_pks for r, c in zip(all_records, all_capsules)))
    mark("Q4-V19", all(r.route_order == c.route_order for r, c in zip(all_records, all_capsules)))
    mark("Q4-V20", all(r.route_payload_sha256 == derive_route_payload_sha256_v1(initial_object_pks=r.initial_object_pks, selected_relationship_pks=r.selected_relationship_pks, route_order=r.route_order) for r in all_records))

    record_dicts = tuple(record.to_dict() for record in all_records)
    metadata_only = all(_primitive_metadata_only(value) for value in record_dicts)
    forbidden_hits = [hit for value in record_dicts for hit in _forbidden_metadata_keys(value)]
    serialized = b"".join(record.canonical_bytes() for record in all_records)
    mark("Q4-V21", metadata_only and not forbidden_hits)
    mark("Q4-V22", b"tensor_bytes" not in serialized and b"dense_resident" not in serialized)
    mark("Q4-V23", b"serialized_maf" not in serialized and b"maf_payload" not in serialized)
    mark("Q4-V24", not forbidden_hits)

    with tempfile.TemporaryDirectory(prefix="openmind-q4-route-cache-") as tmp_name:
        tmp_dir = Path(tmp_name)
        first_path = tmp_dir / "q001.route-cache.json"
        first_record = records["q001"]
        first_capsule = capsules["q001"]

        write_route_cache_record_v1(first_path, first_record)
        first_readback = read_route_cache_record_v1(first_path)
        mark("Q4-V25", first_readback.to_dict() == first_record.to_dict())

        write_route_cache_record_v1(first_path, first_record)
        second_readback = read_route_cache_record_v1(first_path)
        mark("Q4-V26", second_readback.to_dict() == first_record.to_dict())

        _validate_reuse(second_readback, first_capsule, snapshot, relationship_authority, model_pk)
        mark("Q4-V27", validated_route_payload_v1(second_readback) == validated_route_payload_v1(first_record))

        mismatch_sha = hashlib.sha256(b"q4-mismatch").hexdigest()
        mismatch_generation = "mafgen:v1:" + mismatch_sha

        mark("Q4-V28", _expect_q4_rejection(MAFQueryRouteCacheIdentityError, lambda: validate_route_cache_for_reuse_v1(record=first_record, expected_query_signature="q4-mismatched-query-signature", expected_source_generation_pk=first_capsule.source_generation_pk, expected_source_manifest_sha256=first_capsule.source_manifest_sha256, expected_selection_config_sha256=first_capsule.selection_config_sha256, expected_expansion_policy=first_capsule.expansion_policy, expected_max_object_budget=first_capsule.max_object_budget, expected_max_expansion_rounds=first_capsule.max_expansion_rounds, model_pk=model_pk, resident_snapshot=snapshot, relationship_authority_pks=relationship_authority)))
        mark("Q4-V29", _expect_q4_rejection(MAFQueryRouteCacheIdentityError, lambda: validate_route_cache_for_reuse_v1(record=first_record, expected_query_signature=first_capsule.query_signature, expected_source_generation_pk=mismatch_generation, expected_source_manifest_sha256=first_capsule.source_manifest_sha256, expected_selection_config_sha256=first_capsule.selection_config_sha256, expected_expansion_policy=first_capsule.expansion_policy, expected_max_object_budget=first_capsule.max_object_budget, expected_max_expansion_rounds=first_capsule.max_expansion_rounds, model_pk=model_pk, resident_snapshot=snapshot, relationship_authority_pks=relationship_authority)))
        mark("Q4-V30", _expect_q4_rejection(MAFQueryRouteCacheIdentityError, lambda: validate_route_cache_for_reuse_v1(record=first_record, expected_query_signature=first_capsule.query_signature, expected_source_generation_pk=first_capsule.source_generation_pk, expected_source_manifest_sha256=mismatch_sha, expected_selection_config_sha256=first_capsule.selection_config_sha256, expected_expansion_policy=first_capsule.expansion_policy, expected_max_object_budget=first_capsule.max_object_budget, expected_max_expansion_rounds=first_capsule.max_expansion_rounds, model_pk=model_pk, resident_snapshot=snapshot, relationship_authority_pks=relationship_authority)))
        mark("Q4-V31", _expect_q4_rejection(MAFQueryRouteCacheIdentityError, lambda: validate_route_cache_for_reuse_v1(record=first_record, expected_query_signature=first_capsule.query_signature, expected_source_generation_pk=first_capsule.source_generation_pk, expected_source_manifest_sha256=first_capsule.source_manifest_sha256, expected_selection_config_sha256=mismatch_sha, expected_expansion_policy=first_capsule.expansion_policy, expected_max_object_budget=first_capsule.max_object_budget, expected_max_expansion_rounds=first_capsule.max_expansion_rounds, model_pk=model_pk, resident_snapshot=snapshot, relationship_authority_pks=relationship_authority)))
        mark("Q4-V32", _expect_q4_rejection(MAFQueryRouteCacheIdentityError, lambda: validate_route_cache_for_reuse_v1(record=first_record, expected_query_signature=first_capsule.query_signature, expected_source_generation_pk=first_capsule.source_generation_pk, expected_source_manifest_sha256=first_capsule.source_manifest_sha256, expected_selection_config_sha256=first_capsule.selection_config_sha256, expected_expansion_policy="q4-mismatched-policy", expected_max_object_budget=first_capsule.max_object_budget + 1, expected_max_expansion_rounds=first_capsule.max_expansion_rounds + 1, model_pk=model_pk, resident_snapshot=snapshot, relationship_authority_pks=relationship_authority)))

        target = records["q026"]
        target_capsule = capsules["q026"]

        mark("Q4-V33", _expect_q4_rejection(MAFQueryRouteCacheIntegrityError, lambda: _validate_reuse(replace(target, route_payload_sha256="0" * 64), target_capsule, snapshot, relationship_authority, model_pk)))

        tampered_order = tuple(reversed(target.route_order))
        if tampered_order == target.route_order and len(target.route_order) > 1:
            tampered_order = target.route_order[1:] + target.route_order[:1]
        mark("Q4-V34", _expect_q4_rejection(MAFQueryRouteCacheIntegrityError, lambda: _validate_reuse(replace(target, route_order=tampered_order), target_capsule, snapshot, relationship_authority, model_pk)))

        unknown_object = "mafobj:v1:" + hashlib.sha256(b"q4-unknown-object").hexdigest()
        old_object = target.initial_object_pks[0]
        unknown_initial = _replace_first(target.initial_object_pks, old_object, unknown_object)
        unknown_route = _replace_first(target.route_order, old_object, unknown_object)
        unknown_object_digest = derive_route_payload_sha256_v1(initial_object_pks=unknown_initial, selected_relationship_pks=target.selected_relationship_pks, route_order=unknown_route)
        mark("Q4-V35", _expect_q4_rejection(MAFQueryRouteCacheObjectPKError, lambda: _validate_reuse(replace(target, initial_object_pks=unknown_initial, route_order=unknown_route, route_payload_sha256=unknown_object_digest), target_capsule, snapshot, relationship_authority, model_pk)))

        unknown_relationship = "relationship:q4:unknown"
        unknown_relationships = target.selected_relationship_pks + (unknown_relationship,)
        unknown_relationship_digest = derive_route_payload_sha256_v1(initial_object_pks=target.initial_object_pks, selected_relationship_pks=unknown_relationships, route_order=target.route_order)
        mark("Q4-V36", _expect_q4_rejection(MAFQueryRouteCacheRelationshipPKError, lambda: _validate_reuse(replace(target, selected_relationship_pks=unknown_relationships, route_payload_sha256=unknown_relationship_digest), target_capsule, snapshot, relationship_authority, model_pk)))

        mark("Q4-V37", _expect_q4_rejection(MAFQueryRouteCacheDataError, lambda: _validate_reuse(replace(target, schema="openmind.maf_query_route_cache.invalid"), target_capsule, snapshot, relationship_authority, model_pk)))

        q3_cleanup_clean = all(
            q3_result["repeated_lifecycle"][query_id]["cleanup"]["all_cold"] is True
            and q3_result["repeated_lifecycle"][query_id]["cleanup"]["active_pin_leases"] == 0
            and q3_result["repeated_lifecycle"][query_id]["closed"] is True
            for query_id in FROZEN_CASE_IDS
        )
        metadata_survives_cleanup = first_path.exists() and read_route_cache_record_v1(first_path).to_dict() == first_record.to_dict()
        mark("Q4-V38", q3_cleanup_clean and metadata_survives_cleanup)
        mark("Q4-V39", q3_cleanup_clean)

        before_generation_binding = (snapshot.generation_pk, snapshot.generation_manifest_sha256, snapshot.active_record_sha256)
        _expect_q4_rejection(lambda: validate_route_cache_for_reuse_v1(record=first_record, expected_query_signature=first_capsule.query_signature, expected_source_generation_pk=mismatch_generation, expected_source_manifest_sha256=first_capsule.source_manifest_sha256, expected_selection_config_sha256=first_capsule.selection_config_sha256, expected_expansion_policy=first_capsule.expansion_policy, expected_max_object_budget=first_capsule.max_object_budget, expected_max_expansion_rounds=first_capsule.max_expansion_rounds, model_pk=model_pk, resident_snapshot=snapshot, relationship_authority_pks=relationship_authority))
        after_generation_binding = (snapshot.generation_pk, snapshot.generation_manifest_sha256, snapshot.active_record_sha256)
        mark("Q4-V40", before_generation_binding == after_generation_binding)

        first_payload = validated_route_payload_v1(first_record)
        _validate_reuse(first_record, first_capsule, snapshot, relationship_authority, model_pk)
        second_payload = validated_route_payload_v1(first_record)
        _validate_reuse(first_record, first_capsule, snapshot, relationship_authority, model_pk)
        third_payload = validated_route_payload_v1(first_record)
        mark("Q4-V41", first_payload == second_payload == third_payload)
        mark("Q4-V42", q3_result["boundary"]["q4_entered"] is False and q3_result["boundary"]["route_cache_used"] is False)

    mark("Q4-V43", CLAIM_BOUNDARY["working_set_sufficiency_tested"] is False and CLAIM_BOUNDARY["inference_executed"] is False and CLAIM_BOUNDARY["performance_metrics_emitted"] is False)
    mark("Q4-V44", CLAIM_BOUNDARY["phase_6e_entered"] is False and CLAIM_BOUNDARY["llm_replacement_claimed"] is False and CLAIM_BOUNDARY["maf_native_compute_claimed"] is False)

    failed_checks = [check_id for check_id in CHECK_IDS if not checks[check_id]]
    check_records = [
        {
            "id": check_id,
            "passed": checks[check_id],
            "detail": details.get(check_id, "PASS" if checks[check_id] else "FAIL"),
        }
        for check_id in CHECK_IDS
    ]

    return {
        "schema": RESULT_SCHEMA,
        "status": "PASS" if not failed_checks else "FAIL",
        "all_pass": not failed_checks,
        "protocol_sha256": EXPECTED_Q4_PROTOCOL_SHA256,
        "runner_contract_sha256": EXPECTED_RUNNER_CONTRACT_SHA256,
        "runner_sha256": runner_sha256,
        "production_module_sha256": EXPECTED_PRODUCTION_MODULE_SHA256,
        "check_matrix_sha256": EXPECTED_CHECK_MATRIX_SHA256,
        "q2_selector_sha256": EXPECTED_Q2_SELECTOR_SHA256,
        "q2_runner_evidence_sha256": EXPECTED_Q2_RUNNER_SHA256,
        "q3_runner_evidence_sha256": EXPECTED_Q3_RUNNER_SHA256,
        "query_fixture_sha256": EXPECTED_Q2_QUERY_FIXTURE_SHA256,
        "catalog_sha256": EXPECTED_Q2_CATALOG_SHA256,
        "source_generation_pk": EXPECTED_SOURCE_GENERATION_PK,
        "source_manifest_sha256": EXPECTED_SOURCE_MANIFEST_SHA256,
        "selection_config_sha256": EXPECTED_Q2_SELECTION_CONFIG_SHA256,
        "expected_check_count": 44,
        "check_count": len(check_records),
        "failed_checks": failed_checks,
        "frozen_cases": list(FROZEN_CASE_IDS),
        "checks": check_records,
        "case_results": case_results,
        "claim_boundary": copy.deepcopy(CLAIM_BOUNDARY),
        "failure": None,
    }


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    reservation: dict[str, str] | None = None
    runner_sha256 = _sha256_file(RUNNER_PATH)
    try:
        authority = _preflight_authorities()
        reservation = _reserve_slot(runner_sha256)
        result = _run_science(authority, runner_sha256)
        _publish_result(result, reservation)
        return 0 if result["all_pass"] else 1
    except (
        Q4ValidationHarnessError,
        MAFQueryRouteCacheError,
        FileExistsError,
        OSError,
        ValueError,
        KeyError,
        TypeError,
    ) as exc:
        LOGGER.error("Q4 validation failed closed: %s", exc)
        if reservation is not None and not RESULT_PATH.exists() and not PARTIAL_PATH.exists():
            failure_result = {
                "schema": RESULT_SCHEMA,
                "status": "FAIL",
                "all_pass": False,
                "protocol_sha256": EXPECTED_Q4_PROTOCOL_SHA256,
                "runner_contract_sha256": EXPECTED_RUNNER_CONTRACT_SHA256,
                "runner_sha256": runner_sha256,
                "production_module_sha256": EXPECTED_PRODUCTION_MODULE_SHA256,
                "check_matrix_sha256": EXPECTED_CHECK_MATRIX_SHA256,
                "q2_selector_sha256": EXPECTED_Q2_SELECTOR_SHA256,
                "q2_runner_evidence_sha256": EXPECTED_Q2_RUNNER_SHA256,
                "q3_runner_evidence_sha256": EXPECTED_Q3_RUNNER_SHA256,
                "query_fixture_sha256": EXPECTED_Q2_QUERY_FIXTURE_SHA256,
                "catalog_sha256": EXPECTED_Q2_CATALOG_SHA256,
                "frozen_cases": list(FROZEN_CASE_IDS),
                "checks": [],
                "case_results": {},
                "claim_boundary": copy.deepcopy(CLAIM_BOUNDARY),
                "failure": {
                    "type": type(exc).__name__,
                    "message": str(exc),
                    "stage": "post_reservation",
                },
            }
            try:
                _publish_result(failure_result, reservation)
            except Exception:
                LOGGER.exception("failed to publish Q4 failure result")
        return 1
    except Exception:
        LOGGER.exception("unexpected Q4 validation failure")
        if reservation is not None:
            LOGGER.error("Q4 slot is permanently spent; automatic retry is forbidden")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
