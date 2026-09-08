#!/usr/bin/env python3
"""OpenMind Phase 6D-Q3 exact-once attach/detach/cleanup validation."""

import ctypes
import errno
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent

PROTOCOL = HERE / "MAF_QUERY_CAPSULE_ATTACH_DETACH_CLEANUP_VALIDATION_V1_PROTOCOL.md"
RUNNER_SHA_AUTHORITY = HERE / "maf_query_capsule_attach_detach_cleanup_validation_v1.py.sha256"
SLOT_PATH = HERE / "maf_query_capsule_attach_detach_cleanup_validation_v1.slot"
PARTIAL_PATH = HERE / "maf_query_capsule_attach_detach_cleanup_validation_v1.json.partial"
RESULT_PATH = HERE / "maf_query_capsule_attach_detach_cleanup_validation_v1.json"

Q1_IMPL = HERE / "maf_query_capsule_data_model_v1.py"
RUNTIME_IMPL = HERE / "maf_object_runtime_residency_v1.py"
ACTIVATION_IMPL = HERE / "maf_activation_v1_1.py"
RESIDENT_IMPL = HERE / "maf_resident_pk_directory_v1.py"
SELECTOR_IMPL = HERE / "maf_query_to_pk_selection_v1.py"

CATALOG_PATH = HERE / "maf_query_to_pk_selection_validation_v1_catalog.json"
QUERY_FIXTURE_PATH = HERE / "maf_query_to_pk_selection_validation_v1_queries.json"
TRACKED_MANIFEST_PATH = HERE / "maf_query_to_pk_selection_validation_v1_generation_manifest.json"
PHYSICAL_MANIFEST_PATH = ROOT / "results/runtime/maf_query_to_pk_selection_validation_v1_generation/validation_generation.manifest.json"
PHYSICAL_SEGMENT_PATH = ROOT / "results/runtime/maf_query_to_pk_selection_validation_v1_generation/validation_segment.mafseg"
ACTIVE_RECORD_PATH = ROOT / "results/runtime/maf_query_capsule_attach_detach_cleanup_validation_v1_fixture/active_generation.json"
FIXTURE_AUTHORITY_PATH = HERE / "maf_query_capsule_attach_detach_cleanup_validation_v1_fixture_authority.json"

Q1_PROTOCOL_SHA256 = "5255a58c8c6340c251e24ae8543760fcd66a8deb8be1a8356ad5b78ad898edda"
Q1_IMPLEMENTATION_SHA256 = "f897b97011714f3c84b7350c6bb53e800232be8a5d34e5148a3e50a81952976e"
Q1_VALIDATION_PROTOCOL_SHA256 = "63b40e4ec91410ebea43b85b032a57ed42ba181942390c41fd603a7e5c5cfd3d"
Q1_RESULT_SHA256 = "24d1605d1ad95f1b7e7bee190fd0cc978d7b2597d095ac06f68c350208ef1774"
Q1_VERDICT_SHA256 = "c396346adfc3d7aed08373a52d02e88ce14b2195269c9d090c2572828db77615"

RUNTIME_PROTOCOL_SHA256 = "81987d00ef4cb51556dcebf08bff9c9fa8979f033df05304d347b759e545eb13"
RUNTIME_IMPLEMENTATION_SHA256 = "4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9"
RUNTIME_VALIDATION_PROTOCOL_SHA256 = "e12c5dc67d2e147d2c0305c0782cc76ce90a390e7bd276ba0030b3e461fabf17"
RUNTIME_RESULT_SHA256 = "1b7fcbe8ca8674928a11b58be950adaaa6a85e1f991636d21a557d160d0c719f"
RUNTIME_VERDICT_SHA256 = "800fd8e6e58d2af7ea46133e2e6a26d3b380fa4abd371f055324f722ad92784f"

ACTIVATION_SHA256 = "9435ae8dd32656c7350887689d453f3cb8460887068bfaf06e6f68b5b5b927a1"
RESIDENT_SHA256 = "4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6"
SELECTOR_SHA256 = "e21c05e352fe921b791e8c936425727a98911ce7566989672a96bfd2b9613fa2"
SELECTION_PROTOCOL_SHA256 = "b42a0643976c2393871e3b826ba5573b4de981b49603de63230d69cf57be0811"

Q2_PROTOCOL_SHA256 = "a814bca93a6b014ee53aad234b8396c841d0efc2a9363598e8a2192f23745699"
Q2_RUNNER_SHA256 = "7bda960c125786fdf3cfca65c4b7b5851ca8bd91257282facfee2fec1ae7a030"
Q2_SLOT_SHA256 = "0545bba0abcf73e5235d639b0d4390a1e3c01011b1ff0cc9d0372eaf5eb8716a"
Q2_RESULT_SHA256 = "b2ad49d7a9a3e1ef565e07e595efc4a4e00b283f422723553c6437ef3a42def6"
Q2_VERDICT_SHA256 = "c17198e0013fd9c0a8c59b8f09c05d4f22693dc7d56afdc0f761f55a008c2663"

Q3_PROTOCOL_SHA256 = "323c0d4e0cbd5327382e3762e4d9529fba48f3748699861d96b31920db5b0363"
FIXTURE_AUTHORITY_SHA256 = "c6ae99b0bdb2a360aba929233ed16d0dab2d8397147b4d23ac3e2cc5df83a5cd"
ACTIVE_RECORD_SHA256 = "ffcf8ada4e2959432e18650a9503bb52175b4366f85ca663d206dea94da3f4e0"
CATALOG_SHA256 = "c51ef0fabeb10e7c8a091a093aa1934620a69b2026b5a87cb02477b9dd7ca900"
QUERY_FIXTURE_SHA256 = "32f4636bd5e8ceee0dca8342335279a6f8e6acafe866a5469f2c23aa2655202a"
SOURCE_MANIFEST_SHA256 = "28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3"
PHYSICAL_SEGMENT_SHA256 = "aa6ccf99df2b65c19634bbeceb91cfe8db2aeced429e55f8fa6318f1d28ff67d"
PHYSICAL_SEGMENT_BYTES = 312326668
SELECTION_CONFIG_SHA256 = "0caeaeaafdd870e6b02ccc8b4450576883d4ef5234ba689c472e3b14d9dbe120"

MODEL_PK = "mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258"
GENERATION_PK = "mafgen:v1:45a80a2aa271ce04853003185b6a1227cb309bd1e3e2dc538eea849fac9f5db0"

SERIALIZED_BYTE_BUDGET = 33554432
DENSE_BYTE_BUDGET = 4096
MAX_OBJECT_BUDGET = 4
MAX_EXPANSION_ROUNDS = 0
EXPANSION_POLICY = "disabled"

RESULT_SCHEMA = "openmind.maf_query_capsule_attach_detach_cleanup_validation.v1"
PREPARED_SCHEMA = "openmind.maf_query_capsule_attach_detach_cleanup_validation.slot.prepared.v1"
RESERVED_SCHEMA = "openmind.maf_query_capsule_attach_detach_cleanup_validation.slot.reserved_durable.v1"
PUBLISHED_SCHEMA = "openmind.maf_query_capsule_attach_detach_cleanup_validation.slot.published_durable.v1"

READINESS_FLAG = "--readiness"
ARM_FLAG = "--run-exact-once"
RENAME_NOREPLACE = 1

CHECK_IDS = (
    "V01_protocol_authority_binding",
    "V02_q1_capsule_implementation_binding",
    "V03_q1_acceptance_verdict_binding",
    "V04_phase6c_runtime_implementation_binding",
    "V05_phase6c_acceptance_verdict_binding",
    "V06_activation_implementation_binding",
    "V07_resident_directory_binding",
    "V08_selector_authority_binding",
    "V09_catalog_and_query_fixture_binding",
    "V10_q2_authoritative_closure_binding",
    "V11_physical_generation_hash_binding",
    "V12_fixture_authority_binding",
    "V13_fixture_active_record_source_binding",
    "V14_fixture_directory_exact_12_pk_resolution",
    "V15_exact_preregistered_query_case_set",
    "V16_selector_output_source_binding",
    "V17_capsule_deterministic_construction",
    "V18_expansion_disabled_and_budget_exact",
    "V19_only_capsule_selected_objects_registered",
    "V20_unknown_object_rejected_pre_attach",
    "V21_stale_generation_and_manifest_rejected_pre_attach",
    "V22_q001_success_lifecycle",
    "V23_q025_success_lifecycle",
    "V24_q026_success_lifecycle",
    "V25_q033_success_lifecycle",
    "V26_attach_transitions_observed",
    "V27_exact_one_ownership_lease_per_object",
    "V28_duplicate_ownership_rejected",
    "V29_pinned_demotion_rejected",
    "V30_reverse_route_cleanup_order",
    "V31_success_cleanup_active_leases_zero",
    "V32_success_cleanup_serialized_bytes_zero",
    "V33_success_cleanup_dense_bytes_zero",
    "V34_success_cleanup_all_objects_cold",
    "V35_active_record_unchanged",
    "V36_generation_manifest_unchanged",
    "V37_physical_segment_unchanged",
    "V38_q1_q2_frozen_evidence_unchanged",
    "V39_failure_before_first_attach_cleanup",
    "V40_failure_after_partial_attach_cleanup",
    "V41_failure_after_pin_cleanup",
    "V42_failure_after_hot_maf_cleanup",
    "V43_failure_after_hot_dense_cleanup",
    "V44_failure_mid_multi_object_cleanup",
    "V45_repeated_lifecycle_clean_baseline",
    "V46_close_terminal_semantics",
    "V47_route_cache_expansion_inference_and_sufficiency_excluded",
    "V48_phase_boundary_and_no_performance_claim",
)

QUERY_CASES = (
    ("q001", "specific_intent", "layer 0 attention query", 1, False),
    ("q025", "multi_target_intent", "layer 0 normalization", 2, False),
    ("q026", "multi_target_intent", "layer 0 attention", 4, False),
    ("q033", "fallback_control", "weather tomorrow", 4, True),
)

class Q3ValidationError(RuntimeError):
    pass

class Q3InjectedFailure(RuntimeError):
    pass

class Q3OwnershipError(RuntimeError):
    pass

def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")

def canonical_record_bytes(value: Any) -> bytes:
    return canonical_bytes(value) + b"\n"

def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def require(condition: bool, message: str) -> None:
    if not condition:
        raise Q3ValidationError(message)

def _present(path: Path) -> bool:
    try:
        os.lstat(path)
        return True
    except FileNotFoundError:
        return False

def _namespace_state() -> dict[str, bool]:
    return {"slot": _present(SLOT_PATH), "partial": _present(PARTIAL_PATH), "result": _present(RESULT_PATH)}

def _namespace_guard() -> dict[str, bool]:
    state = _namespace_state()
    if any(state.values()):
        raise Q3ValidationError("Q3 namespace presence refuses execution: " + json.dumps(state, sort_keys=True, separators=(",", ":")))
    return state

def _load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

def _runner_sha_authority() -> str:
    require(RUNNER_SHA_AUTHORITY.is_file(), "runner SHA authority missing")
    raw = RUNNER_SHA_AUTHORITY.read_text(encoding="ascii")
    require(raw.endswith("\n"), "runner SHA authority newline missing")
    value = raw[:-1]
    require(len(value) == 64 and all(c in "0123456789abcdef" for c in value), "runner SHA authority malformed")
    require(value == file_sha256(Path(__file__).resolve()), "runner self SHA mismatch")
    return value

def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def _canonical_json(path: Path) -> Any:
    raw = path.read_bytes()
    value = json.loads(raw.decode("utf-8"))
    require(raw == canonical_bytes(value), f"non-canonical JSON: {path}")
    return value

def _find_unique_by_sha(expected_sha: str, terms: tuple[str, ...]) -> Path:
    matches = []
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        name = path.name.lower()
        if not all(term in name for term in terms):
            continue
        try:
            if file_sha256(path) == expected_sha:
                matches.append(path)
        except OSError:
            pass
    require(len(matches) == 1, f"authority resolution failed for {expected_sha}: {matches}")
    return matches[0]

def _prequal() -> dict[str, Any]:
    runner_sha = _runner_sha_authority()
    require(file_sha256(PROTOCOL) == Q3_PROTOCOL_SHA256, "Q3 protocol SHA mismatch")
    require(file_sha256(Q1_IMPL) == Q1_IMPLEMENTATION_SHA256, "Q1 implementation SHA mismatch")
    require(file_sha256(RUNTIME_IMPL) == RUNTIME_IMPLEMENTATION_SHA256, "runtime implementation SHA mismatch")
    require(file_sha256(ACTIVATION_IMPL) == ACTIVATION_SHA256, "activation SHA mismatch")
    require(file_sha256(RESIDENT_IMPL) == RESIDENT_SHA256, "resident SHA mismatch")
    require(file_sha256(SELECTOR_IMPL) == SELECTOR_SHA256, "selector SHA mismatch")
    require(file_sha256(CATALOG_PATH) == CATALOG_SHA256, "catalog SHA mismatch")
    require(file_sha256(QUERY_FIXTURE_PATH) == QUERY_FIXTURE_SHA256, "query fixture SHA mismatch")
    require(file_sha256(TRACKED_MANIFEST_PATH) == SOURCE_MANIFEST_SHA256, "tracked manifest SHA mismatch")
    require(file_sha256(PHYSICAL_MANIFEST_PATH) == SOURCE_MANIFEST_SHA256, "physical manifest SHA mismatch")
    require(TRACKED_MANIFEST_PATH.read_bytes() == PHYSICAL_MANIFEST_PATH.read_bytes(), "manifest byte identity mismatch")
    require(PHYSICAL_SEGMENT_PATH.stat().st_size == PHYSICAL_SEGMENT_BYTES, "segment byte length mismatch")
    require(file_sha256(PHYSICAL_SEGMENT_PATH) == PHYSICAL_SEGMENT_SHA256, "segment SHA mismatch")
    require(file_sha256(ACTIVE_RECORD_PATH) == ACTIVE_RECORD_SHA256, "active record SHA mismatch")
    require(file_sha256(FIXTURE_AUTHORITY_PATH) == FIXTURE_AUTHORITY_SHA256, "fixture authority SHA mismatch")

    authority_paths = {
        "q1_protocol": _find_unique_by_sha(Q1_PROTOCOL_SHA256, ("query", "capsule", "protocol")),
        "q1_implementation": Q1_IMPL,
        "q1_validation_protocol": _find_unique_by_sha(Q1_VALIDATION_PROTOCOL_SHA256, ("query", "capsule", "validation", "protocol")),
        "q1_result": _find_unique_by_sha(Q1_RESULT_SHA256, ("query", "capsule", "validation")),
        "q1_verdict": _find_unique_by_sha(Q1_VERDICT_SHA256, ("query", "capsule", "verdict")),
        "runtime_protocol": _find_unique_by_sha(RUNTIME_PROTOCOL_SHA256, ("runtime", "protocol")),
        "runtime_implementation": RUNTIME_IMPL,
        "runtime_validation_protocol": _find_unique_by_sha(RUNTIME_VALIDATION_PROTOCOL_SHA256, ("runtime", "validation", "protocol")),
        "runtime_result": _find_unique_by_sha(RUNTIME_RESULT_SHA256, ("runtime", "validation")),
        "runtime_verdict": _find_unique_by_sha(RUNTIME_VERDICT_SHA256, ("runtime", "verdict")),
        "selection_protocol": _find_unique_by_sha(SELECTION_PROTOCOL_SHA256, ("selection", "protocol")),
        "q2_protocol": _find_unique_by_sha(Q2_PROTOCOL_SHA256, ("query", "selection", "validation", "protocol")),
        "q2_runner": HERE / "maf_query_to_pk_selection_validation_v1_4.py",
        "q2_slot": HERE / "maf_query_to_pk_selection_validation_v1_4.slot",
        "q2_result": HERE / "maf_query_to_pk_selection_validation_v1_4.json",
        "q2_verdict": HERE / "MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_4_VERDICT.md",
        "catalog": CATALOG_PATH,
        "query_fixture": QUERY_FIXTURE_PATH,
        "tracked_manifest": TRACKED_MANIFEST_PATH,
        "physical_manifest": PHYSICAL_MANIFEST_PATH,
        "physical_segment": PHYSICAL_SEGMENT_PATH,
        "active_record": ACTIVE_RECORD_PATH,
        "fixture_authority": FIXTURE_AUTHORITY_PATH,
    }
    expected = {
        "q1_protocol": Q1_PROTOCOL_SHA256,
        "q1_implementation": Q1_IMPLEMENTATION_SHA256,
        "q1_validation_protocol": Q1_VALIDATION_PROTOCOL_SHA256,
        "q1_result": Q1_RESULT_SHA256,
        "q1_verdict": Q1_VERDICT_SHA256,
        "runtime_protocol": RUNTIME_PROTOCOL_SHA256,
        "runtime_implementation": RUNTIME_IMPLEMENTATION_SHA256,
        "runtime_validation_protocol": RUNTIME_VALIDATION_PROTOCOL_SHA256,
        "runtime_result": RUNTIME_RESULT_SHA256,
        "runtime_verdict": RUNTIME_VERDICT_SHA256,
        "selection_protocol": SELECTION_PROTOCOL_SHA256,
        "q2_protocol": Q2_PROTOCOL_SHA256,
        "q2_runner": Q2_RUNNER_SHA256,
        "q2_slot": Q2_SLOT_SHA256,
        "q2_result": Q2_RESULT_SHA256,
        "q2_verdict": Q2_VERDICT_SHA256,
        "catalog": CATALOG_SHA256,
        "query_fixture": QUERY_FIXTURE_SHA256,
        "tracked_manifest": SOURCE_MANIFEST_SHA256,
        "physical_manifest": SOURCE_MANIFEST_SHA256,
        "physical_segment": PHYSICAL_SEGMENT_SHA256,
        "active_record": ACTIVE_RECORD_SHA256,
        "fixture_authority": FIXTURE_AUTHORITY_SHA256,
    }
    preservation_before = {}
    for label, path in authority_paths.items():
        require(path.is_file(), f"authority missing: {label}")
        observed = file_sha256(path)
        require(observed == expected[label], f"authority SHA mismatch: {label}")
        preservation_before[label] = observed

    fixture = _canonical_json(FIXTURE_AUTHORITY_PATH)
    active = _canonical_json(ACTIVE_RECORD_PATH)
    require(fixture["scientific"] is False, "fixture scientific flag mismatch")
    require(fixture["protocol_sha256"] == Q3_PROTOCOL_SHA256, "fixture protocol mismatch")
    require(fixture["active_record_sha256"] == ACTIVE_RECORD_SHA256, "fixture active SHA mismatch")
    require(fixture["recovery_active_record_sha256"] == ACTIVE_RECORD_SHA256, "fixture recovery active mismatch")
    require(fixture["active_record"] == active, "fixture active record embedding mismatch")
    require(fixture["model_pk"] == MODEL_PK, "fixture model mismatch")
    require(fixture["generation_pk"] == GENERATION_PK, "fixture generation mismatch")
    require(fixture["generation_manifest_sha256"] == SOURCE_MANIFEST_SHA256, "fixture manifest mismatch")
    require(fixture["catalog_sha256"] == CATALOG_SHA256, "fixture catalog mismatch")
    require(fixture["query_fixture_sha256"] == QUERY_FIXTURE_SHA256, "fixture query mismatch")
    require(fixture["selection_config_sha256"] == SELECTION_CONFIG_SHA256, "fixture config mismatch")
    require(fixture["physical_segment_sha256"] == PHYSICAL_SEGMENT_SHA256, "fixture segment SHA mismatch")
    require(fixture["physical_segment_bytes"] == PHYSICAL_SEGMENT_BYTES, "fixture segment bytes mismatch")
    upstream = fixture["upstream_authority_sha256"]
    require(upstream["q1_implementation"] == Q1_IMPLEMENTATION_SHA256, "fixture Q1 implementation mismatch")
    require(upstream["q1_verdict"] == Q1_VERDICT_SHA256, "fixture Q1 verdict mismatch")
    require(upstream["runtime_implementation"] == RUNTIME_IMPLEMENTATION_SHA256, "fixture runtime implementation mismatch")
    require(upstream["runtime_verdict"] == RUNTIME_VERDICT_SHA256, "fixture runtime verdict mismatch")
    require(upstream["activation"] == ACTIVATION_SHA256, "fixture activation mismatch")
    require(upstream["resident_directory"] == RESIDENT_SHA256, "fixture resident mismatch")
    require(upstream["selector"] == SELECTOR_SHA256, "fixture selector mismatch")
    require(upstream["selection_protocol"] == SELECTION_PROTOCOL_SHA256, "fixture selection protocol mismatch")
    require(upstream["q2_validation_protocol"] == Q2_PROTOCOL_SHA256, "fixture Q2 protocol mismatch")
    require(upstream["q2_validation_runner"] == Q2_RUNNER_SHA256, "fixture Q2 runner mismatch")
    require(upstream["q2_slot"] == Q2_SLOT_SHA256, "fixture Q2 slot mismatch")
    require(upstream["q2_result"] == Q2_RESULT_SHA256, "fixture Q2 result mismatch")
    require(upstream["q2_verdict"] == Q2_VERDICT_SHA256, "fixture Q2 verdict mismatch")

    q1 = _load_module("openmind_q3_q1", Q1_IMPL)
    runtime = _load_module("openmind_q3_runtime", RUNTIME_IMPL)
    _load_module("openmind_q3_activation", ACTIVATION_IMPL)
    resident = _load_module("openmind_q3_resident", RESIDENT_IMPL)
    selector = _load_module("openmind_q3_selector", SELECTOR_IMPL)

    catalog_data = _json(CATALOG_PATH)
    query_data = _json(QUERY_FIXTURE_PATH)
    catalog = selector.MAFQueryPKCatalogV1.from_mapping(catalog_data)
    config = selector.MAFQueryToPKSelectionConfigV1.from_mapping(query_data["selection_config"])
    require(catalog.catalog_sha256 == CATALOG_SHA256, "catalog canonical SHA mismatch")
    require(config.selection_config_sha256 == SELECTION_CONFIG_SHA256, "selection config SHA mismatch")
    require(catalog.source_generation_pk == GENERATION_PK, "catalog generation mismatch")
    require(catalog.source_manifest_sha256 == SOURCE_MANIFEST_SHA256, "catalog manifest mismatch")
    require(query_data["source_generation_pk"] == GENERATION_PK, "query generation mismatch")
    require(query_data["source_manifest_sha256"] == SOURCE_MANIFEST_SHA256, "query manifest mismatch")

    snapshot = resident.build_snapshot(
        model_pk=MODEL_PK,
        active_record_path=ACTIVE_RECORD_PATH,
        active_candidate_manifest_path=PHYSICAL_MANIFEST_PATH,
        active_segment_paths={"segment:00000000": PHYSICAL_SEGMENT_PATH},
    )
    require(snapshot.entry_count == 12, "resident entry count mismatch")
    catalog_pks = tuple(entry.object_pk for entry in catalog.entries)
    require(catalog_pks == tuple(fixture["resolved_object_pks"]), "fixture PK resolution mismatch")
    for object_pk in catalog_pks:
        entry = snapshot.lookup(
            model_pk=MODEL_PK,
            pk_kind=resident.OBJECT_PK_KIND,
            logical_pk=object_pk,
            expected_generation_pk=GENERATION_PK,
        )
        require(entry.object_pk == object_pk, "resident lookup mismatch")

    expected_cases = tuple((qid, qclass, text) for qid, qclass, text, _, _ in QUERY_CASES)
    wanted = {case[0] for case in QUERY_CASES}
    actual_cases = tuple(
        (row["query_id"], row["query_class"], row["query_text"])
        for row in query_data["queries"]
        if row["query_id"] in wanted
    )
    require(actual_cases == expected_cases, "query case set mismatch")

    return {
        "runner_sha256": runner_sha,
        "q1": q1,
        "runtime": runtime,
        "resident": resident,
        "selector": selector,
        "catalog": catalog,
        "config": config,
        "query_data": query_data,
        "snapshot": snapshot,
        "fixture": fixture,
        "catalog_pks": catalog_pks,
        "authority_paths": authority_paths,
        "preservation_before": preservation_before,
    }

def _dense_materializer(entry: Any, serialized: bytes) -> tuple[bytes, int]:
    return hashlib.sha256(serialized).digest(), 32

def _new_runtime(preq: dict[str, Any]):
    return preq["runtime"].MAFObjectRuntime(
        model_pk=MODEL_PK,
        generation_pk=GENERATION_PK,
        serialized_byte_budget=SERIALIZED_BYTE_BUDGET,
        dense_byte_budget=DENSE_BYTE_BUDGET,
        dense_materializer=_dense_materializer,
    )

def _resident_entry(preq: dict[str, Any], object_pk: str):
    resident = preq["resident"]
    return preq["snapshot"].lookup(
        model_pk=MODEL_PK,
        pk_kind=resident.OBJECT_PK_KIND,
        logical_pk=object_pk,
        expected_generation_pk=GENERATION_PK,
    )

def _build_capsule(preq: dict[str, Any], selection: Any):
    q1 = preq["q1"]
    query_pk = q1.derive_query_pk(
        query_signature=selection.query_signature,
        selection_config_sha256=selection.selection_config_sha256,
        source_generation_pk=selection.source_generation_pk,
        source_manifest_sha256=selection.source_manifest_sha256,
    )
    capsule = q1.MAFQueryCapsuleV1(
        schema=q1.QUERY_CAPSULE_SCHEMA,
        query_pk=query_pk,
        query_signature=selection.query_signature,
        source_generation_pk=selection.source_generation_pk,
        source_manifest_sha256=selection.source_manifest_sha256,
        initial_object_pks=selection.selected_object_pks,
        selected_relationship_pks=(),
        route_order=selection.selected_object_pks,
        expansion_policy=EXPANSION_POLICY,
        max_object_budget=MAX_OBJECT_BUDGET,
        max_expansion_rounds=MAX_EXPANSION_ROUNDS,
        selection_config_sha256=selection.selection_config_sha256,
    )
    require(q1.MAFQueryCapsuleV1.from_json_bytes(capsule.canonical_bytes()) == capsule, "capsule round-trip mismatch")
    return capsule

def _acquire(runtime: Any, runtime_mod: ModuleType, ownership: dict[str, Any], object_pk: str):
    if object_pk in ownership:
        raise Q3OwnershipError("duplicate ownership")
    lease = runtime.pin(object_pk, runtime_mod.ResidencyState.MAPPED)
    ownership[object_pk] = lease
    return lease

def _cleanup(runtime: Any, runtime_mod: ModuleType, route: tuple[str, ...], registered: list[str], ownership: dict[str, Any]):
    cleanup_order = []
    registered_set = set(registered)
    for object_pk in reversed(route):
        if object_pk not in registered_set:
            continue
        cleanup_order.append(object_pk)
        state = runtime.state(object_pk)
        if state is runtime_mod.ResidencyState.HOT_DENSE:
            runtime.transition(object_pk, runtime_mod.ResidencyState.HOT_MAF)
            state = runtime.state(object_pk)
        if state is runtime_mod.ResidencyState.HOT_MAF:
            runtime.transition(object_pk, runtime_mod.ResidencyState.MAPPED)
            state = runtime.state(object_pk)
        if object_pk in ownership:
            runtime.unpin(ownership[object_pk].token)
            del ownership[object_pk]
        if state is runtime_mod.ResidencyState.MAPPED:
            runtime.transition(object_pk, runtime_mod.ResidencyState.COLD_DISK)

    snapshot = runtime.snapshot()
    require(not ownership, "ownership not empty after cleanup")
    require(snapshot.active_pin_leases == 0, "leases nonzero after cleanup")
    require(snapshot.serialized_resident_bytes == 0, "serialized bytes nonzero after cleanup")
    require(snapshot.dense_resident_bytes == 0, "dense bytes nonzero after cleanup")
    require(snapshot.cold_disk_count == snapshot.object_count, "registered objects not all COLD_DISK")
    return cleanup_order, snapshot

def _lifecycle(preq: dict[str, Any], capsule: Any, *, injection: str | None = None, dense_q001: bool = False) -> dict[str, Any]:
    runtime_mod = preq["runtime"]
    runtime = _new_runtime(preq)
    ownership: dict[str, Any] = {}
    registered: list[str] = []
    attach_order: list[str] = []
    ownership_order: list[str] = []
    duplicate_rejected = False
    pinned_demotion_rejected = False
    injection_seen = False
    injection_name = None
    lease_shape_exact = False
    pre_cleanup_snapshot = None

    try:
        if injection == "F01":
            raise Q3InjectedFailure("F01")

        for index, object_pk in enumerate(capsule.route_order):
            runtime.register_entry(_resident_entry(preq, object_pk))
            registered.append(object_pk)
            runtime.transition(object_pk, runtime_mod.ResidencyState.MAPPED)
            attach_order.append(object_pk)

            if injection == "F02" and index == 0:
                raise Q3InjectedFailure("F02")

            _acquire(runtime, runtime_mod, ownership, object_pk)
            ownership_order.append(object_pk)

            if injection == "F03" and index == 0:
                raise Q3InjectedFailure("F03")

            if injection == "F06" and len(ownership_order) == 2:
                raise Q3InjectedFailure("F06")

        pre_cleanup_snapshot = runtime.snapshot()
        by_pk = {item.object_pk: item for item in pre_cleanup_snapshot.objects}
        lease_shape_exact = (
            pre_cleanup_snapshot.active_pin_leases == len(capsule.route_order)
            and len(ownership) == len(capsule.route_order)
            and all(by_pk[pk].pin_count == 1 for pk in capsule.route_order)
            and all(by_pk[pk].effective_pin_floor is runtime_mod.ResidencyState.MAPPED for pk in capsule.route_order)
        )

        if injection is None and capsule.route_order:
            first = capsule.route_order[0]
            try:
                _acquire(runtime, runtime_mod, ownership, first)
            except Q3OwnershipError:
                duplicate_rejected = True
            try:
                runtime.transition(first, runtime_mod.ResidencyState.COLD_DISK)
            except runtime_mod.MAFObjectRuntimePinnedDemotionError:
                pinned_demotion_rejected = True

        if dense_q001:
            target = capsule.route_order[0]
            runtime.transition(target, runtime_mod.ResidencyState.HOT_MAF)
            if injection == "F04":
                raise Q3InjectedFailure("F04")
            runtime.transition(target, runtime_mod.ResidencyState.HOT_DENSE)
            dense = runtime.dense_view(target)
            require(isinstance(dense, bytes) and len(dense) == 32, "synthetic dense view mismatch")
            if injection == "F05":
                raise Q3InjectedFailure("F05")

    except Q3InjectedFailure as exc:
        injection_seen = True
        injection_name = str(exc)
    finally:
        cleanup_order, cleanup_snapshot = _cleanup(
            runtime,
            runtime_mod,
            tuple(capsule.route_order),
            registered,
            ownership,
        )
        runtime.close()
        runtime.close()
        closed_snapshot = runtime.snapshot()

    return {
        "injection": injection,
        "injection_seen": injection_seen,
        "injection_name": injection_name,
        "registered_order": registered,
        "attach_order": attach_order,
        "ownership_order": ownership_order,
        "lease_shape_exact": lease_shape_exact,
        "duplicate_ownership_rejected": duplicate_rejected,
        "pinned_demotion_rejected": pinned_demotion_rejected,
        "cleanup_order": cleanup_order,
        "cleanup": {
            "object_count": cleanup_snapshot.object_count,
            "active_pin_leases": cleanup_snapshot.active_pin_leases,
            "serialized_resident_bytes": cleanup_snapshot.serialized_resident_bytes,
            "dense_resident_bytes": cleanup_snapshot.dense_resident_bytes,
            "all_cold": cleanup_snapshot.cold_disk_count == cleanup_snapshot.object_count,
        },
        "closed": closed_snapshot.closed,
    }

def _negative_source_tests(preq: dict[str, Any], base_capsule: Any) -> dict[str, bool]:
    runtime_mod = preq["runtime"]
    q1 = preq["q1"]

    runtime = _new_runtime(preq)
    unknown_pk = "mafobj:v1:" + ("0" * 64)
    if unknown_pk in preq["catalog_pks"]:
        unknown_pk = "mafobj:v1:" + ("f" * 64)
    unknown_rejected = False
    try:
        runtime.transition(unknown_pk, runtime_mod.ResidencyState.MAPPED)
    except runtime_mod.MAFObjectRuntimeUnknownObjectError:
        unknown_rejected = True
    runtime.close()

    stale_generation = "mafgen:v1:" + ("0" * 64)
    stale_generation_capsule = q1.MAFQueryCapsuleV1(
        schema=q1.QUERY_CAPSULE_SCHEMA,
        query_pk=q1.derive_query_pk(
            query_signature=base_capsule.query_signature,
            selection_config_sha256=base_capsule.selection_config_sha256,
            source_generation_pk=stale_generation,
            source_manifest_sha256=SOURCE_MANIFEST_SHA256,
        ),
        query_signature=base_capsule.query_signature,
        source_generation_pk=stale_generation,
        source_manifest_sha256=SOURCE_MANIFEST_SHA256,
        initial_object_pks=base_capsule.initial_object_pks,
        selected_relationship_pks=(),
        route_order=base_capsule.route_order,
        expansion_policy=EXPANSION_POLICY,
        max_object_budget=MAX_OBJECT_BUDGET,
        max_expansion_rounds=MAX_EXPANSION_ROUNDS,
        selection_config_sha256=base_capsule.selection_config_sha256,
    )
    stale_generation_rejected = False
    try:
        stale_generation_capsule.require_source_binding(
            source_generation_pk=GENERATION_PK,
            source_manifest_sha256=SOURCE_MANIFEST_SHA256,
        )
    except q1.MAFQueryCapsuleDataModelError:
        stale_generation_rejected = True

    stale_manifest = "0" * 64
    stale_manifest_capsule = q1.MAFQueryCapsuleV1(
        schema=q1.QUERY_CAPSULE_SCHEMA,
        query_pk=q1.derive_query_pk(
            query_signature=base_capsule.query_signature,
            selection_config_sha256=base_capsule.selection_config_sha256,
            source_generation_pk=GENERATION_PK,
            source_manifest_sha256=stale_manifest,
        ),
        query_signature=base_capsule.query_signature,
        source_generation_pk=GENERATION_PK,
        source_manifest_sha256=stale_manifest,
        initial_object_pks=base_capsule.initial_object_pks,
        selected_relationship_pks=(),
        route_order=base_capsule.route_order,
        expansion_policy=EXPANSION_POLICY,
        max_object_budget=MAX_OBJECT_BUDGET,
        max_expansion_rounds=MAX_EXPANSION_ROUNDS,
        selection_config_sha256=base_capsule.selection_config_sha256,
    )
    stale_manifest_rejected = False
    try:
        stale_manifest_capsule.require_source_binding(
            source_generation_pk=GENERATION_PK,
            source_manifest_sha256=SOURCE_MANIFEST_SHA256,
        )
    except q1.MAFQueryCapsuleDataModelError:
        stale_manifest_rejected = True

    return {
        "unknown_object_rejected": unknown_rejected,
        "stale_generation_rejected": stale_generation_rejected,
        "stale_manifest_rejected": stale_manifest_rejected,
    }

def _close_semantics(preq: dict[str, Any], object_pk: str) -> dict[str, bool]:
    runtime_mod = preq["runtime"]
    runtime = _new_runtime(preq)
    runtime.register_entry(_resident_entry(preq, object_pk))
    runtime.transition(object_pk, runtime_mod.ResidencyState.MAPPED)
    runtime.close()
    first_closed = runtime.snapshot().closed
    runtime.close()
    second_closed = runtime.snapshot().closed

    mutation_rejected = False
    try:
        runtime.transition(object_pk, runtime_mod.ResidencyState.COLD_DISK)
    except runtime_mod.MAFObjectRuntimeClosedError:
        mutation_rejected = True

    resource_rejected = False
    try:
        runtime.serialized_bytes(object_pk)
    except runtime_mod.MAFObjectRuntimeClosedError:
        resource_rejected = True

    return {
        "first_close_closed": first_closed,
        "second_close_harmless": second_closed,
        "post_close_mutation_rejected": mutation_rejected,
        "post_close_resource_rejected": resource_rejected,
    }

def _clean(outcome: dict[str, Any]) -> bool:
    c = outcome["cleanup"]
    return (
        c["active_pin_leases"] == 0
        and c["serialized_resident_bytes"] == 0
        and c["dense_resident_bytes"] == 0
        and c["all_cold"]
        and outcome["closed"]
    )

def _science(preq: dict[str, Any]) -> dict[str, Any]:
    selector = preq["selector"]
    rows = {row["query_id"]: row for row in preq["query_data"]["queries"]}
    selections = {}
    capsules = {}
    successes = {}
    case_evidence = {}

    for qid, qclass, text, expected_count, expected_fallback in QUERY_CASES:
        row = rows[qid]
        require(row["query_class"] == qclass and row["query_text"] == text, f"{qid} fixture mismatch")
        selection = selector.select_query_to_pks_v1(
            query=text,
            catalog=preq["catalog"],
            config=preq["config"],
            source_generation_pk=GENERATION_PK,
            source_manifest_sha256=SOURCE_MANIFEST_SHA256,
        )
        require(len(selection.selected_object_pks) == expected_count, f"{qid} cardinality mismatch")
        require(selection.fallback_used is expected_fallback, f"{qid} fallback mismatch")
        capsule = _build_capsule(preq, selection)
        lifecycle = _lifecycle(preq, capsule, dense_q001=(qid == "q001"))
        selections[qid] = selection
        capsules[qid] = capsule
        successes[qid] = lifecycle
        case_evidence[qid] = {
            "query_class": qclass,
            "query_text": text,
            "selection": selection.to_dict(),
            "capsule": capsule.to_dict(),
            "lifecycle": lifecycle,
        }

    negative = _negative_source_tests(preq, capsules["q001"])

    failure_plan = (
        ("F01", "q001"),
        ("F02", "q001"),
        ("F03", "q001"),
        ("F04", "q001"),
        ("F05", "q001"),
        ("F06", "q026"),
    )
    failures = {
        fid: _lifecycle(
            preq,
            capsules[qid],
            injection=fid,
            dense_q001=(qid == "q001"),
        )
        for fid, qid in failure_plan
    }

    repeated = {
        qid: _lifecycle(preq, capsules[qid], dense_q001=(qid == "q001"))
        for qid in ("q001", "q025", "q026", "q033")
    }

    close_semantics = _close_semantics(preq, capsules["q001"].route_order[0])
    preservation_after = {
        label: file_sha256(path)
        for label, path in preq["authority_paths"].items()
    }

    selector_binding = all(
        s.source_generation_pk == GENERATION_PK
        and s.source_manifest_sha256 == SOURCE_MANIFEST_SHA256
        and s.catalog_sha256 == CATALOG_SHA256
        and s.selection_config_sha256 == SELECTION_CONFIG_SHA256
        for s in selections.values()
    )
    capsule_determinism = all(
        c.query_pk
        == preq["q1"].derive_query_pk(
            query_signature=c.query_signature,
            selection_config_sha256=c.selection_config_sha256,
            source_generation_pk=c.source_generation_pk,
            source_manifest_sha256=c.source_manifest_sha256,
        )
        and c.route_order == c.initial_object_pks
        and c.route_order == selections[qid].selected_object_pks
        and preq["q1"].MAFQueryCapsuleV1.from_json_bytes(c.canonical_bytes()) == c
        for qid, c in capsules.items()
    )
    expansion_exact = all(
        c.expansion_policy == "disabled"
        and c.max_object_budget == 4
        and c.max_expansion_rounds == 0
        and c.selected_relationship_pks == ()
        for c in capsules.values()
    )
    registered_exact = all(tuple(successes[qid]["registered_order"]) == capsules[qid].route_order for qid in successes)
    attach_exact = all(tuple(successes[qid]["attach_order"]) == capsules[qid].route_order for qid in successes)
    lease_exact = all(successes[qid]["lease_shape_exact"] for qid in successes)
    reverse_cleanup = all(
        tuple(successes[qid]["cleanup_order"]) == tuple(reversed(capsules[qid].route_order))
        for qid in successes
    )
    failure_clean = {
        fid: outcome["injection_seen"] and outcome["injection_name"] == fid and _clean(outcome)
        for fid, outcome in failures.items()
    }
    repeated_clean = all(_clean(outcome) for outcome in repeated.values())
    preservation_ok = preservation_after == preq["preservation_before"]

    boundary = {
        "claim_scope": "lifecycle_ownership_source_binding_failure_atomicity_only",
        "route_cache_used": False,
        "bounded_expansion_used": False,
        "inference_executed": False,
        "answer_generation_executed": False,
        "working_set_sufficiency_tested": False,
        "tensor_object_avoidance_claimed": False,
        "output_parity_claimed": False,
        "answer_quality_claimed": False,
        "maf_native_compute_claimed": False,
        "performance_superiority_claimed": False,
        "llm_replacement_claimed": False,
        "q4_entered": False,
        "phase_6e_entered": False,
        "performance_metrics_emitted": False,
    }

    wanted = {case[0] for case in QUERY_CASES}
    actual_case_set = tuple(
        (row["query_id"], row["query_class"], row["query_text"])
        for row in preq["query_data"]["queries"]
        if row["query_id"] in wanted
    )
    expected_case_set = tuple((qid, qclass, text) for qid, qclass, text, _, _ in QUERY_CASES)

    checks_map = {
        "V01_protocol_authority_binding": file_sha256(PROTOCOL) == Q3_PROTOCOL_SHA256,
        "V02_q1_capsule_implementation_binding": file_sha256(Q1_IMPL) == Q1_IMPLEMENTATION_SHA256,
        "V03_q1_acceptance_verdict_binding": preq["preservation_before"]["q1_verdict"] == Q1_VERDICT_SHA256,
        "V04_phase6c_runtime_implementation_binding": file_sha256(RUNTIME_IMPL) == RUNTIME_IMPLEMENTATION_SHA256,
        "V05_phase6c_acceptance_verdict_binding": preq["preservation_before"]["runtime_verdict"] == RUNTIME_VERDICT_SHA256,
        "V06_activation_implementation_binding": file_sha256(ACTIVATION_IMPL) == ACTIVATION_SHA256,
        "V07_resident_directory_binding": file_sha256(RESIDENT_IMPL) == RESIDENT_SHA256,
        "V08_selector_authority_binding": file_sha256(SELECTOR_IMPL) == SELECTOR_SHA256 and preq["preservation_before"]["selection_protocol"] == SELECTION_PROTOCOL_SHA256,
        "V09_catalog_and_query_fixture_binding": file_sha256(CATALOG_PATH) == CATALOG_SHA256 and file_sha256(QUERY_FIXTURE_PATH) == QUERY_FIXTURE_SHA256,
        "V10_q2_authoritative_closure_binding": (
            preq["preservation_before"]["q2_protocol"] == Q2_PROTOCOL_SHA256
            and preq["preservation_before"]["q2_runner"] == Q2_RUNNER_SHA256
            and preq["preservation_before"]["q2_slot"] == Q2_SLOT_SHA256
            and preq["preservation_before"]["q2_result"] == Q2_RESULT_SHA256
            and preq["preservation_before"]["q2_verdict"] == Q2_VERDICT_SHA256
        ),
        "V11_physical_generation_hash_binding": (
            file_sha256(TRACKED_MANIFEST_PATH) == SOURCE_MANIFEST_SHA256
            and file_sha256(PHYSICAL_MANIFEST_PATH) == SOURCE_MANIFEST_SHA256
            and TRACKED_MANIFEST_PATH.read_bytes() == PHYSICAL_MANIFEST_PATH.read_bytes()
            and PHYSICAL_SEGMENT_PATH.stat().st_size == PHYSICAL_SEGMENT_BYTES
            and file_sha256(PHYSICAL_SEGMENT_PATH) == PHYSICAL_SEGMENT_SHA256
        ),
        "V12_fixture_authority_binding": file_sha256(FIXTURE_AUTHORITY_PATH) == FIXTURE_AUTHORITY_SHA256,
        "V13_fixture_active_record_source_binding": (
            file_sha256(ACTIVE_RECORD_PATH) == ACTIVE_RECORD_SHA256
            and preq["fixture"]["generation_pk"] == GENERATION_PK
            and preq["fixture"]["generation_manifest_sha256"] == SOURCE_MANIFEST_SHA256
            and preq["fixture"]["active_record_sha256"] == ACTIVE_RECORD_SHA256
        ),
        "V14_fixture_directory_exact_12_pk_resolution": preq["snapshot"].entry_count == 12 and len(preq["catalog_pks"]) == 12 and preq["catalog_pks"] == tuple(preq["fixture"]["resolved_object_pks"]),
        "V15_exact_preregistered_query_case_set": actual_case_set == expected_case_set,
        "V16_selector_output_source_binding": selector_binding,
        "V17_capsule_deterministic_construction": capsule_determinism,
        "V18_expansion_disabled_and_budget_exact": expansion_exact,
        "V19_only_capsule_selected_objects_registered": registered_exact,
        "V20_unknown_object_rejected_pre_attach": negative["unknown_object_rejected"],
        "V21_stale_generation_and_manifest_rejected_pre_attach": negative["stale_generation_rejected"] and negative["stale_manifest_rejected"],
        "V22_q001_success_lifecycle": _clean(successes["q001"]),
        "V23_q025_success_lifecycle": _clean(successes["q025"]),
        "V24_q026_success_lifecycle": _clean(successes["q026"]),
        "V25_q033_success_lifecycle": _clean(successes["q033"]),
        "V26_attach_transitions_observed": attach_exact,
        "V27_exact_one_ownership_lease_per_object": lease_exact,
        "V28_duplicate_ownership_rejected": all(successes[qid]["duplicate_ownership_rejected"] for qid in successes),
        "V29_pinned_demotion_rejected": all(successes[qid]["pinned_demotion_rejected"] for qid in successes),
        "V30_reverse_route_cleanup_order": reverse_cleanup,
        "V31_success_cleanup_active_leases_zero": all(outcome["cleanup"]["active_pin_leases"] == 0 for outcome in successes.values()),
        "V32_success_cleanup_serialized_bytes_zero": all(outcome["cleanup"]["serialized_resident_bytes"] == 0 for outcome in successes.values()),
        "V33_success_cleanup_dense_bytes_zero": all(outcome["cleanup"]["dense_resident_bytes"] == 0 for outcome in successes.values()),
        "V34_success_cleanup_all_objects_cold": all(outcome["cleanup"]["all_cold"] for outcome in successes.values()),
        "V35_active_record_unchanged": preservation_after["active_record"] == ACTIVE_RECORD_SHA256,
        "V36_generation_manifest_unchanged": preservation_after["tracked_manifest"] == SOURCE_MANIFEST_SHA256 and preservation_after["physical_manifest"] == SOURCE_MANIFEST_SHA256,
        "V37_physical_segment_unchanged": preservation_after["physical_segment"] == PHYSICAL_SEGMENT_SHA256,
        "V38_q1_q2_frozen_evidence_unchanged": preservation_ok,
        "V39_failure_before_first_attach_cleanup": failure_clean["F01"],
        "V40_failure_after_partial_attach_cleanup": failure_clean["F02"],
        "V41_failure_after_pin_cleanup": failure_clean["F03"],
        "V42_failure_after_hot_maf_cleanup": failure_clean["F04"],
        "V43_failure_after_hot_dense_cleanup": failure_clean["F05"],
        "V44_failure_mid_multi_object_cleanup": failure_clean["F06"],
        "V45_repeated_lifecycle_clean_baseline": repeated_clean,
        "V46_close_terminal_semantics": all(close_semantics.values()),
        "V47_route_cache_expansion_inference_and_sufficiency_excluded": (
            boundary["route_cache_used"] is False
            and boundary["bounded_expansion_used"] is False
            and boundary["inference_executed"] is False
            and boundary["working_set_sufficiency_tested"] is False
        ),
        "V48_phase_boundary_and_no_performance_claim": (
            boundary["q4_entered"] is False
            and boundary["phase_6e_entered"] is False
            and boundary["performance_metrics_emitted"] is False
            and boundary["performance_superiority_claimed"] is False
            and boundary["llm_replacement_claimed"] is False
        ),
    }
    require(tuple(checks_map.keys()) == CHECK_IDS, "check order mismatch")
    checks = [{"id": cid, "passed": bool(checks_map[cid])} for cid in CHECK_IDS]
    failed = [row["id"] for row in checks if not row["passed"]]

    return {
        "checks": checks,
        "failed_checks": failed,
        "all_pass": not failed,
        "query_cases": case_evidence,
        "failure_cases": failures,
        "negative_tests": negative,
        "repeated_lifecycle": repeated,
        "close_semantics": close_semantics,
        "preservation_before": dict(preq["preservation_before"]),
        "preservation_after": preservation_after,
        "boundary": boundary,
    }

def _prepared_record(runner_sha: str) -> dict[str, Any]:
    return {
        "schema": PREPARED_SCHEMA,
        "sequence": 1,
        "state": "RESERVATION_PREPARED",
        "validation_protocol_sha256": Q3_PROTOCOL_SHA256,
        "validation_runner_sha256": runner_sha,
        "fixture_authority_sha256": FIXTURE_AUTHORITY_SHA256,
        "active_record_sha256": ACTIVE_RECORD_SHA256,
        "source_generation_pk": GENERATION_PK,
        "source_manifest_sha256": SOURCE_MANIFEST_SHA256,
        "partial_basename": PARTIAL_PATH.name,
        "final_basename": RESULT_PATH.name,
    }

def _reserved_record(prepared_sha: str) -> dict[str, Any]:
    return {
        "schema": RESERVED_SCHEMA,
        "sequence": 2,
        "state": "RESERVED_DURABLE",
        "prepared_record_sha256": prepared_sha,
    }

def _published_record(reserved_sha: str, result_sha: str, result_bytes: int) -> dict[str, Any]:
    return {
        "schema": PUBLISHED_SCHEMA,
        "sequence": 3,
        "state": "PUBLISHED_DURABLE",
        "reserved_durable_record_sha256": reserved_sha,
        "final_result_sha256": result_sha,
        "final_result_bytes": result_bytes,
        "final_result_basename": RESULT_PATH.name,
    }

def _append_record(fd: int, value: dict[str, Any]) -> str:
    raw = canonical_record_bytes(value)
    total = 0
    while total < len(raw):
        written = os.write(fd, raw[total:])
        if written <= 0:
            raise Q3ValidationError("short slot journal write")
        total += written
    return hashlib.sha256(raw).hexdigest()

def _write_all(fd: int, raw: bytes) -> None:
    total = 0
    while total < len(raw):
        written = os.write(fd, raw[total:])
        if written <= 0:
            raise Q3ValidationError("short result write")
        total += written

def _load_renameat2():
    libc = ctypes.CDLL(None, use_errno=True)
    fn = getattr(libc, "renameat2", None)
    if fn is None:
        raise Q3ValidationError("renameat2 unavailable")
    fn.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    ]
    fn.restype = ctypes.c_int
    return fn

def _build_result(preq: dict[str, Any], science: dict[str, Any]) -> tuple[dict[str, Any], bytes]:
    result = {
        "schema": RESULT_SCHEMA,
        "exact_once": {
            "slot_state": "SPENT",
            "automatic_retry": False,
            "manual_scientific_retry": False,
        },
        "validation_protocol_sha256": Q3_PROTOCOL_SHA256,
        "validation_runner_sha256": preq["runner_sha256"],
        "fixture_authority_sha256": FIXTURE_AUTHORITY_SHA256,
        "active_record_sha256": ACTIVE_RECORD_SHA256,
        "model_pk": MODEL_PK,
        "source_generation_pk": GENERATION_PK,
        "source_manifest_sha256": SOURCE_MANIFEST_SHA256,
        "catalog_sha256": CATALOG_SHA256,
        "query_fixture_sha256": QUERY_FIXTURE_SHA256,
        "selection_config_sha256": SELECTION_CONFIG_SHA256,
        "expected_check_count": len(CHECK_IDS),
        "check_count": len(science["checks"]),
        "checks": science["checks"],
        "failed_checks": science["failed_checks"],
        "all_pass": science["all_pass"],
        "query_cases": science["query_cases"],
        "failure_cases": science["failure_cases"],
        "negative_tests": science["negative_tests"],
        "repeated_lifecycle": science["repeated_lifecycle"],
        "close_semantics": science["close_semantics"],
        "preservation_before": science["preservation_before"],
        "preservation_after": science["preservation_after"],
        "boundary": science["boundary"],
        "publication_backend": {
            "primitive": "renameat2",
            "flag": "RENAME_NOREPLACE",
            "flag_value": RENAME_NOREPLACE,
            "partial_fsync_required": True,
            "result_parent_directory_fsync_required": True,
            "permanent_slot_journal": True,
        },
    }
    raw = canonical_record_bytes(result)
    require(canonical_record_bytes(json.loads(raw[:-1].decode("utf-8"))) == raw, "result canonical round-trip failed")
    return result, raw

def _authoritative_run() -> dict[str, Any]:
    _namespace_guard()
    preq = _prequal()

    parent_fd = os.open(str(HERE), os.O_RDONLY)
    slot_fd = -1
    partial_fd = -1
    phase = "PREQUAL"
    rename_succeeded = False

    try:
        phase = "SLOT_CREATE"
        slot_fd = os.open(
            SLOT_PATH,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_APPEND,
            0o644,
        )

        phase = "PREPARED_DURABLE"
        prepared_sha = _append_record(slot_fd, _prepared_record(preq["runner_sha256"]))
        os.fsync(slot_fd)
        os.fsync(parent_fd)

        phase = "RESERVED_DURABLE"
        reserved_sha = _append_record(slot_fd, _reserved_record(prepared_sha))
        os.fsync(slot_fd)
        os.fsync(parent_fd)

        phase = "PARTIAL_CREATE"
        partial_fd = os.open(
            PARTIAL_PATH,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            0o644,
        )

        phase = "SCIENCE"
        science = _science(preq)
        result, result_raw = _build_result(preq, science)

        phase = "PARTIAL_FSYNC"
        _write_all(partial_fd, result_raw)
        os.fsync(partial_fd)
        os.close(partial_fd)
        partial_fd = -1

        phase = "RENAME_NOREPLACE"
        renameat2 = _load_renameat2()
        ctypes.set_errno(0)
        rc = renameat2(
            parent_fd,
            PARTIAL_PATH.name.encode(),
            parent_fd,
            RESULT_PATH.name.encode(),
            RENAME_NOREPLACE,
        )
        if rc != 0:
            error_number = ctypes.get_errno()
            if error_number == errno.EEXIST:
                raise Q3ValidationError("final result path already exists")
            raise OSError(error_number, os.strerror(error_number), str(RESULT_PATH))
        rename_succeeded = True

        phase = "RESULT_DIR_FSYNC"
        os.fsync(parent_fd)

        result_sha = hashlib.sha256(result_raw).hexdigest()
        require(file_sha256(RESULT_PATH) == result_sha, "published result SHA mismatch")

        phase = "PUBLISHED_DURABLE"
        _append_record(slot_fd, _published_record(reserved_sha, result_sha, len(result_raw)))
        os.fsync(slot_fd)
        os.fsync(parent_fd)

        return {
            "result_path": str(RESULT_PATH),
            "result_sha256": result_sha,
            "all_pass": result["all_pass"],
            "failed_checks": result["failed_checks"],
        }
    except Exception as exc:
        raise Q3ValidationError(
            "Q3 post-slot failure; namespace permanently spent: "
            + json.dumps(
                {
                    "phase": phase,
                    "rename_succeeded": rename_succeeded,
                    "slot_present": _present(SLOT_PATH),
                    "partial_present": _present(PARTIAL_PATH),
                    "result_present": _present(RESULT_PATH),
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                },
                sort_keys=True,
                separators=(",", ":"),
            )
        ) from exc
    finally:
        if partial_fd >= 0:
            os.close(partial_fd)
        if slot_fd >= 0:
            os.close(slot_fd)
        os.close(parent_fd)

def _readiness() -> dict[str, bool]:
    _namespace_guard()
    preq = _prequal()
    return {
        "namespace_empty": not any(_namespace_state().values()),
        "runner_self_hash": preq["runner_sha256"] == file_sha256(Path(__file__).resolve()),
        "protocol_bound": file_sha256(PROTOCOL) == Q3_PROTOCOL_SHA256,
        "fixture_bound": file_sha256(FIXTURE_AUTHORITY_PATH) == FIXTURE_AUTHORITY_SHA256,
        "active_bound": file_sha256(ACTIVE_RECORD_PATH) == ACTIVE_RECORD_SHA256,
        "resident_exact_12": preq["snapshot"].entry_count == 12,
        "query_cases_exact": len(QUERY_CASES) == 4,
        "check_ids_exact": len(CHECK_IDS) == 48,
        "renameat2_available": _load_renameat2() is not None,
    }

def main() -> int:
    argv = tuple(sys.argv[1:])
    if argv == (READINESS_FLAG,):
        value = _readiness()
        print("MODE=readiness")
        print(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False))
        print("Q3_RESULT_SLOT=UNSPENT")
        return 0 if all(value.values()) else 1

    if argv == (ARM_FLAG,):
        outcome = _authoritative_run()
        print("MODE=run-exact-once")
        print("RESULT_PATH=" + outcome["result_path"])
        print("RESULT_SHA256=" + outcome["result_sha256"])
        print("ALL_PASS=" + str(outcome["all_pass"]))
        print("FAILED_CHECKS=" + json.dumps(outcome["failed_checks"], separators=(",", ":")))
        return 0 if outcome["all_pass"] else 1

    print(
        "usage: maf_query_capsule_attach_detach_cleanup_validation_v1.py "
        + "{--readiness|--run-exact-once}",
        file=sys.stderr,
    )
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
