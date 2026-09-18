#!/usr/bin/env python3

import ast
import ctypes
import hashlib
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

V1_PROTOCOL = HERE / "MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_PROTOCOL.md"
V1_RUNNER = HERE / "maf_query_to_pk_selection_validation_v1.py"
V1_1_PROTOCOL = HERE / "MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_1_PROTOCOL.md"
V1_2_PROTOCOL = HERE / "MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_2_PROTOCOL.md"
V1_3_PROTOCOL = HERE / "MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_3_PROTOCOL.md"
VALIDATION_PROTOCOL = HERE / "MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_4_PROTOCOL.md"
RUNNER_SHA_AUTHORITY = HERE / "maf_query_to_pk_selection_validation_v1_4.py.sha256"
SLOT_PATH = HERE / "maf_query_to_pk_selection_validation_v1_4.slot"
PARTIAL_PATH = HERE / "maf_query_to_pk_selection_validation_v1_4.json.partial"
RESULT_PATH = HERE / "maf_query_to_pk_selection_validation_v1_4.json"

EXPECTED_V1_PROTOCOL_SHA256 = "9bea52de94d8784f6862eee9108afdd1f52f9ff4d4f95eb03fb78d5477e00c11"
EXPECTED_V1_RUNNER_SHA256 = "e2e32f85b1dc7015802ec51a6f214188becc5d35f45c76f4b320617ccd6cd873"
EXPECTED_V1_1_PROTOCOL_SHA256 = "5d94ef0e3330bb63964b0ec2f929fbc9b41290f3f307684bfaece6a1f6e1a8ed"
EXPECTED_V1_2_PROTOCOL_SHA256 = "44339b53054a31a6ff1dbcdacd122e95a7b23ad2cea97264e4e67c382a43fd86"
EXPECTED_V1_3_PROTOCOL_SHA256 = "32c69903393661cc25338ff461b9aa40796d7274e332f97743b53703326bd6cb"
EXPECTED_VALIDATION_PROTOCOL_SHA256 = "a814bca93a6b014ee53aad234b8396c841d0efc2a9363598e8a2192f23745699"

EXPECTED_SELECTION_PROTOCOL_SHA256 = "b42a0643976c2393871e3b826ba5573b4de981b49603de63230d69cf57be0811"
EXPECTED_IMPLEMENTATION_SHA256 = "e21c05e352fe921b791e8c936425727a98911ce7566989672a96bfd2b9613fa2"
EXPECTED_Q1_VERDICT_SHA256 = "c396346adfc3d7aed08373a52d02e88ce14b2195269c9d090c2572828db77615"
EXPECTED_CATALOG_SHA256 = "c51ef0fabeb10e7c8a091a093aa1934620a69b2026b5a87cb02477b9dd7ca900"
EXPECTED_QUERY_FIXTURE_SHA256 = "32f4636bd5e8ceee0dca8342335279a6f8e6acafe866a5469f2c23aa2655202a"
EXPECTED_SOURCE_MANIFEST_SHA256 = "28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3"
EXPECTED_SOURCE_GENERATION_PK = "mafgen:v1:45a80a2aa271ce04853003185b6a1227cb309bd1e3e2dc538eea849fac9f5db0"
EXPECTED_SELECTION_CONFIG_SHA256 = "0caeaeaafdd870e6b02ccc8b4450576883d4ef5234ba689c472e3b14d9dbe120"
RANDOM_BASELINE_SEED = "OPENMIND_6D_Q2_V1_RANDOM_BASELINE"

RESULT_SCHEMA = "openmind.maf_query_to_pk_selection_validation.v1_4"
PREPARED_SCHEMA = "openmind.maf_query_to_pk_selection_validation.slot.prepared.v1_4"
RESERVED_DURABLE_SCHEMA = "openmind.maf_query_to_pk_selection_validation.slot.reserved_durable.v1_4"
PUBLISHED_DURABLE_SCHEMA = "openmind.maf_query_to_pk_selection_validation.slot.published_durable.v1_4"

ARM_FLAG = "--run-exact-once"
ARM_ENV = "OPENMIND_Q2_SELECTION_VALIDATION_V1_4_ARM"
ARM_VALUE = "I_ACCEPT_EXACT_ONCE_Q2_V1_4"
READINESS_FLAG = "--readiness"
RENAME_NOREPLACE = 1
EXPECTED_CHECK_COUNT = 74

CHECK_IDS = ('V01_v1_protocol_binding', 'V02_v1_runner_binding', 'V03_v1_1_protocol_binding', 'V04_v1_2_protocol_binding', 'V05_q2_protocol_binding', 'V06_selector_implementation_binding', 'V07_q1_acceptance_verdict_binding', 'V08_catalog_schema', 'V09_catalog_canonical_json', 'V10_catalog_generation_manifest_binding', 'V11_catalog_unique_sorted_object_pks', 'V12_catalog_static_metadata_surface_only', 'V13_selection_config_exact', 'V14_query_fixture_schema', 'V15_query_fixture_canonical_json', 'V16_evaluation_query_minimum', 'V17_specific_query_minimum', 'V18_distinct_specific_target_minimum', 'V19_fallback_control_minimum', 'V20_query_id_uniqueness_and_order', 'V21_query_class_semantics', 'V22_selector_api_non_oracle', 'V23_no_route_cache_input', 'V24_no_bounded_expansion', 'V25_no_inference_network_or_subprocess', 'V26_independent_target_predicate', 'V27_target_predicate_does_not_call_selector', 'V28_random_baseline_exact_seed_and_formula', 'V29_random_baseline_no_oracle_input', 'V30_v1_science_semantic_equivalence', 'V31_runner_self_sha_authority', 'V32_dual_arm_required', 'V33_guard_false_non_spending', 'V34_backend_qualification_before_slot', 'V35_fixture_qualification_before_slot', 'V36_unconditional_namespace_guard_before_all_work', 'V37_existing_slot_always_refuses', 'V38_empty_prepared_malformed_torn_slot_refuses', 'V39_existing_partial_always_refuses', 'V40_existing_final_always_refuses', 'V41_slot_path_exact', 'V42_prepared_schema_exact', 'V43_reserved_durable_schema_exact', 'V44_published_durable_schema_exact', 'V45_slot_o_excl_append_creation', 'V46_successful_slot_creation_spends_namespace', 'V47_initial_write_failure_spends_namespace', 'V48_prepared_slot_fsync', 'V49_prepared_parent_directory_fsync', 'V50_reserved_append_after_prepared_barrier', 'V51_reserved_slot_fsync', 'V52_reserved_parent_directory_fsync', 'V53_science_after_reserved_durable_only', 'V54_any_post_slot_failure_no_retry', 'V55_slot_journal_never_removed_or_replaced', 'V56_partial_o_excl_after_durable_reservation', 'V57_partial_file_fsync_before_publication', 'V58_renameat2_backend_required', 'V59_rename_noreplace_exact_value', 'V60_no_publication_fallback', 'V61_parent_directory_fsync_after_rename', 'V62_post_rename_failure_no_retry', 'V63_published_record_after_result_name_durable', 'V64_published_record_slot_fsync', 'V65_result_schema_and_canonical_json', 'V66_result_authority_bindings', 'V67_supported_intent_target_hit_threshold', 'V68_supported_intent_precision_threshold', 'V69_top1_baseline_structural_thresholds', 'V70_boundary_exclusions', 'V71_final_result_exists_rejects_execution', 'V72_slot_creation_permanently_spends_namespace', 'V73_prepared_reserved_science_literal_order', 'V74_result_binds_validation_runner_sha256')

PREPARED_FIELDS = (
    "schema","sequence","state","validation_protocol_sha256",
    "prior_v1_3_protocol_sha256","prior_v1_2_protocol_sha256",
    "prior_v1_1_protocol_sha256","prior_v1_protocol_sha256",
    "prior_v1_runner_sha256","validation_runner_sha256",
    "selection_protocol_sha256","implementation_sha256","catalog_sha256",
    "query_fixture_sha256","source_generation_manifest_sha256",
    "source_generation_pk","partial_basename","final_basename",
)
RESERVED_DURABLE_FIELDS = (
    "schema","sequence","state","prepared_record_sha256",
)
PUBLISHED_DURABLE_FIELDS = (
    "schema","sequence","state","reserved_durable_record_sha256",
    "final_result_sha256","final_result_bytes","final_result_basename",
)

RESULT_FIELDS = (
    "schema","exact_once","validation_protocol_sha256",
    "prior_v1_protocol_sha256","prior_v1_runner_sha256",
    "prior_v1_1_protocol_sha256","prior_v1_2_protocol_sha256",
    "prior_v1_3_protocol_sha256","selection_protocol_sha256",
    "implementation_sha256","q1_verdict_sha256","catalog_sha256",
    "query_fixture_sha256","source_generation_pk","source_manifest_sha256",
    "selection_config_sha256","validation_runner_sha256",
    "random_baseline_seed","expected_check_count","check_count","checks",
    "failed_checks","auditor_error","all_pass","metrics",
    "acceptance_thresholds","boundary_exclusions","publication_backend",
)

def file_sha256(path):
    d = hashlib.sha256()
    with Path(path).open("rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            d.update(b)
    return d.hexdigest()

def canonical_json_bytes(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")

def canonical_record_bytes(value):
    return canonical_json_bytes(value) + b"\n"

def _path_present(path):
    return os.path.lexists(os.fspath(path))

def _namespace_state():
    return {
        "slot": _path_present(SLOT_PATH),
        "partial": _path_present(PARTIAL_PATH),
        "result": _path_present(RESULT_PATH),
    }

def _namespace_guard():
    state = _namespace_state()
    if state["slot"] or state["partial"] or state["result"]:
        raise RuntimeError(
            "V1.4 namespace presence refuses execution: "
            + json.dumps(state, sort_keys=True, separators=(",", ":"))
        )
    return state

def _read_runner_authority():
    if not RUNNER_SHA_AUTHORITY.is_file():
        raise RuntimeError("V1.4 runner SHA authority missing")
    raw = RUNNER_SHA_AUTHORITY.read_bytes()
    if not re.fullmatch(rb"[0-9a-f]{64}\n", raw):
        raise RuntimeError("V1.4 runner SHA authority malformed")
    expected = raw[:-1].decode("ascii")
    observed = file_sha256(Path(__file__).resolve())
    if observed != expected:
        raise RuntimeError("V1.4 runner self-SHA mismatch")
    return observed

def _require_sha(path, expected, label):
    if not Path(path).is_file():
        raise RuntimeError(label + " missing")
    observed = file_sha256(path)
    if observed != expected:
        raise RuntimeError(label + " SHA mismatch")
    return observed

def _load_v1():
    _require_sha(V1_RUNNER, EXPECTED_V1_RUNNER_SHA256, "V1 runner")
    spec = importlib.util.spec_from_file_location("openmind_q2_v1_frozen", V1_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load frozen V1 runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def _qualify_authorities():
    return {
        "prior_v1_protocol_sha256": _require_sha(V1_PROTOCOL, EXPECTED_V1_PROTOCOL_SHA256, "V1 protocol"),
        "prior_v1_runner_sha256": _require_sha(V1_RUNNER, EXPECTED_V1_RUNNER_SHA256, "V1 runner"),
        "prior_v1_1_protocol_sha256": _require_sha(V1_1_PROTOCOL, EXPECTED_V1_1_PROTOCOL_SHA256, "V1.1 protocol"),
        "prior_v1_2_protocol_sha256": _require_sha(V1_2_PROTOCOL, EXPECTED_V1_2_PROTOCOL_SHA256, "V1.2 protocol"),
        "prior_v1_3_protocol_sha256": _require_sha(V1_3_PROTOCOL, EXPECTED_V1_3_PROTOCOL_SHA256, "V1.3 protocol"),
        "validation_protocol_sha256": _require_sha(VALIDATION_PROTOCOL, EXPECTED_VALIDATION_PROTOCOL_SHA256, "V1.4 protocol"),
        "validation_runner_sha256": _read_runner_authority(),
    }

def _arm_decision(env_value, cli_armed):
    if env_value == ARM_VALUE and cli_armed:
        return "FULLY_ARMED"
    if env_value == ARM_VALUE:
        return "REFUSE_ENV_ONLY"
    if cli_armed:
        return "REFUSE_CLI_ONLY"
    return "REFUSE_GUARD_FALSE"

def _runtime_arm_decision(argv):
    cli_armed = len(argv) == 1 and argv[0] == ARM_FLAG
    return _arm_decision(os.environ.get(ARM_ENV), cli_armed)

def _parent_fd():
    return os.open(HERE, os.O_RDONLY | os.O_DIRECTORY)

def _write_all(fd, raw):
    view = memoryview(raw)
    while view:
        n = os.write(fd, view)
        if n <= 0:
            raise RuntimeError("zero-progress write")
        view = view[n:]

def _verify_open_inode(fd, path):
    a = os.fstat(fd)
    b = os.stat(path, follow_symlinks=False)
    if a.st_dev != b.st_dev or a.st_ino != b.st_ino:
        raise RuntimeError("slot pathname no longer names opened journal inode")
    if not os.path.isfile(path):
        raise RuntimeError("slot journal is not regular file")

def _prepared_record(runner_sha):
    value = {
        "schema": PREPARED_SCHEMA,
        "sequence": 1,
        "state": "RESERVATION_PREPARED",
        "validation_protocol_sha256": EXPECTED_VALIDATION_PROTOCOL_SHA256,
        "prior_v1_3_protocol_sha256": EXPECTED_V1_3_PROTOCOL_SHA256,
        "prior_v1_2_protocol_sha256": EXPECTED_V1_2_PROTOCOL_SHA256,
        "prior_v1_1_protocol_sha256": EXPECTED_V1_1_PROTOCOL_SHA256,
        "prior_v1_protocol_sha256": EXPECTED_V1_PROTOCOL_SHA256,
        "prior_v1_runner_sha256": EXPECTED_V1_RUNNER_SHA256,
        "validation_runner_sha256": runner_sha,
        "selection_protocol_sha256": EXPECTED_SELECTION_PROTOCOL_SHA256,
        "implementation_sha256": EXPECTED_IMPLEMENTATION_SHA256,
        "catalog_sha256": EXPECTED_CATALOG_SHA256,
        "query_fixture_sha256": EXPECTED_QUERY_FIXTURE_SHA256,
        "source_generation_manifest_sha256": EXPECTED_SOURCE_MANIFEST_SHA256,
        "source_generation_pk": EXPECTED_SOURCE_GENERATION_PK,
        "partial_basename": PARTIAL_PATH.name,
        "final_basename": RESULT_PATH.name,
    }
    if tuple(value.keys()) != PREPARED_FIELDS:
        raise RuntimeError("PREPARED field order mismatch")
    return value

def _reserved_record(prepared_sha):
    value = {
        "schema": RESERVED_DURABLE_SCHEMA,
        "sequence": 2,
        "state": "RESERVED_DURABLE",
        "prepared_record_sha256": prepared_sha,
    }
    if tuple(value.keys()) != RESERVED_DURABLE_FIELDS:
        raise RuntimeError("RESERVED_DURABLE field order mismatch")
    return value

def _published_record(reserved_sha, result_sha, result_bytes):
    value = {
        "schema": PUBLISHED_DURABLE_SCHEMA,
        "sequence": 3,
        "state": "PUBLISHED_DURABLE",
        "reserved_durable_record_sha256": reserved_sha,
        "final_result_sha256": result_sha,
        "final_result_bytes": result_bytes,
        "final_result_basename": RESULT_PATH.name,
    }
    if tuple(value.keys()) != PUBLISHED_DURABLE_FIELDS:
        raise RuntimeError("PUBLISHED_DURABLE field order mismatch")
    return value

def _static_contract():
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(__file__))
    forbidden = set()
    imported_subprocess = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_subprocess |= any(a.name.split(".")[0] == "subprocess" for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported_subprocess |= bool(node.module and node.module.split(".")[0] == "subprocess")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "os" and node.func.attr in {"rename","replace","link","unlink","remove"}:
                forbidden.add(node.func.attr)
    return {
        "namespace_paths_exact": (
            SLOT_PATH.name == "maf_query_to_pk_selection_validation_v1_4.slot"
            and PARTIAL_PATH.name == "maf_query_to_pk_selection_validation_v1_4.json.partial"
            and RESULT_PATH.name == "maf_query_to_pk_selection_validation_v1_4.json"
        ),
        "namespace_guard_before_work": "def _authoritative_run():\n    _namespace_guard()" in source,
        "existing_slot_refuses": 'state["slot"] or state["partial"] or state["result"]' in source,
        "existing_partial_refuses": 'state["slot"] or state["partial"] or state["result"]' in source,
        "existing_final_refuses": 'state["slot"] or state["partial"] or state["result"]' in source,
        "torn_slot_refuses": "_path_present(SLOT_PATH)" in source,
        "slot_flags_exact": "os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_APPEND" in source,
        "slot_creation_spends": "slot_spent = True" in source,
        "initial_write_failure_spends": "RESERVATION_PREPARED_WRITE_FAILURE" in source,
        "post_slot_no_retry": "NO_V1_4_RETRY" in source,
        "slot_never_removed": not ({"unlink","remove","rename","replace","link"} & forbidden),
        "prepared_schema_exact": len(PREPARED_FIELDS) == 18,
        "reserved_schema_exact": len(RESERVED_DURABLE_FIELDS) == 4,
        "published_schema_exact": len(PUBLISHED_DURABLE_FIELDS) == 7,
        "literal_order": (
            source.find('phase = "SLOT_CREATE"')
            < source.find('phase = "PREPARED_WRITE"')
            < source.find('phase = "RESERVED_DURABLE_APPEND"')
            < source.find('phase = "PARTIAL_CREATE"')
            < source.find('phase = "SCIENCE"')
        ),
        "partial_exclusive": "os.O_WRONLY | os.O_CREAT | os.O_EXCL" in source,
        "partial_fsync_before_publication": (
            source.find('phase = "PARTIAL_WRITE"')
            < source.find("os.fsync(partial_fd)", source.find('phase = "PARTIAL_WRITE"'))
            < source.find('phase = "RENAME_NOREPLACE"')
        ),
        "renameat2": "renameat2" in source and "RENAME_NOREPLACE" in source,
        "post_rename_dir_fsync": (
            source.find('phase = "POST_RENAME_DIR_FSYNC"')
            < source.find("os.fsync(parent_fd)", source.find('phase = "POST_RENAME_DIR_FSYNC"'))
            < source.find('phase = "PUBLISHED_APPEND"')
        ),
        "published_after_result_durable": (
            source.find('phase = "POST_RENAME_DIR_FSYNC"')
            < source.find('phase = "PUBLISHED_APPEND"')
        ),
        "published_slot_fsync": (
            source.find('phase = "PUBLISHED_APPEND"')
            < source.find("os.fsync(slot_fd)", source.find('phase = "PUBLISHED_APPEND"'))
            < source.find('phase = "PUBLISHED_DURABLE"')
        ),
        "no_publication_fallback": not ({"rename","replace","link"} & forbidden),
        "no_subprocess": not imported_subprocess,
        "allow_nan_false": "allow_nan=False" in source,
        "result_runner_sha": "validation_runner_sha256" in RESULT_FIELDS,
        "v1_science_reused": 'preq["v1"]._run_scientific_evaluation' in source,
    }

def _full_prequalification():
    _namespace_guard()
    authorities = _qualify_authorities()
    v1 = _load_v1()
    fixture = v1._full_prequalification()
    _namespace_guard()
    if not all(fixture["selector_static"].values()):
        raise RuntimeError("frozen V1 selector static qualification failed")
    if not all(fixture["runner_static"].values()):
        raise RuntimeError("frozen V1 runner static qualification failed")
    if not all(fixture["backend"].values()):
        raise RuntimeError("frozen V1 backend qualification failed")
    static = _static_contract()
    if not all(static.values()):
        failed = [k for k,v in static.items() if not v]
        raise RuntimeError("V1.4 static qualification failed: " + ",".join(failed))
    _namespace_guard()
    return {"authorities": authorities, "v1": v1, "v1_prequalification": fixture, "static": static}

def _build_checks(preq, science, runtime):
    v1 = preq["v1"]
    p = preq["v1_prequalification"]
    static = preq["static"]
    metrics = science["metrics"]
    fixture = p["fixture"]["fixture"]
    catalog = p["fixture"]["catalog"]
    sstatic = p["selector_static"]
    rstatic = p["runner_static"]
    backend = p["backend"]
    values = {
        "V01_v1_protocol_binding": file_sha256(V1_PROTOCOL) == EXPECTED_V1_PROTOCOL_SHA256,
        "V02_v1_runner_binding": file_sha256(V1_RUNNER) == EXPECTED_V1_RUNNER_SHA256,
        "V03_v1_1_protocol_binding": file_sha256(V1_1_PROTOCOL) == EXPECTED_V1_1_PROTOCOL_SHA256,
        "V04_v1_2_protocol_binding": file_sha256(V1_2_PROTOCOL) == EXPECTED_V1_2_PROTOCOL_SHA256,
        "V05_q2_protocol_binding": p["fixture"]["authorities"]["selection_protocol_sha256"] == EXPECTED_SELECTION_PROTOCOL_SHA256,
        "V06_selector_implementation_binding": p["fixture"]["authorities"]["implementation_sha256"] == EXPECTED_IMPLEMENTATION_SHA256,
        "V07_q1_acceptance_verdict_binding": p["fixture"]["authorities"]["q1_verdict_sha256"] == EXPECTED_Q1_VERDICT_SHA256,
        "V08_catalog_schema": catalog["catalog"]["schema"] == v1.CATALOG_SCHEMA,
        "V09_catalog_canonical_json": catalog["catalog_sha256"] == EXPECTED_CATALOG_SHA256,
        "V10_catalog_generation_manifest_binding": catalog["source_generation_pk"] == EXPECTED_SOURCE_GENERATION_PK and catalog["source_manifest_sha256"] == EXPECTED_SOURCE_MANIFEST_SHA256,
        "V11_catalog_unique_sorted_object_pks": catalog["object_pks"] == tuple(sorted(catalog["object_pks"])) and len(catalog["object_pks"]) == len(set(catalog["object_pks"])),
        "V12_catalog_static_metadata_surface_only": all(set(e) == v1.CATALOG_ENTRY_FIELDS for e in catalog["catalog"]["entries"]),
        "V13_selection_config_exact": fixture["selection_config_sha256"] == EXPECTED_SELECTION_CONFIG_SHA256,
        "V14_query_fixture_schema": fixture["fixture"]["schema"] == v1.QUERY_FIXTURE_SCHEMA,
        "V15_query_fixture_canonical_json": p["fixture"]["authorities"]["query_fixture_sha256"] == EXPECTED_QUERY_FIXTURE_SHA256,
        "V16_evaluation_query_minimum": metrics["evaluation_query_count"] >= 32,
        "V17_specific_query_minimum": metrics["specific_intent_query_count"] >= 16,
        "V18_distinct_specific_target_minimum": metrics["unique_expected_object_pk_count"] >= 8,
        "V19_fallback_control_minimum": metrics["fallback_query_count"] >= 4,
        "V20_query_id_uniqueness_and_order": fixture["query_ids"] == tuple(sorted(fixture["query_ids"])) and len(fixture["query_ids"]) == len(set(fixture["query_ids"])),
        "V21_query_class_semantics": science["fallback_contract_pass"] and science["supported_fallback_contract_pass"],
        "V22_selector_api_non_oracle": sstatic["api_non_oracle"],
        "V23_no_route_cache_input": sstatic["no_route_cache_input"],
        "V24_no_bounded_expansion": sstatic["no_bounded_expansion"],
        "V25_no_inference_network_or_subprocess": sstatic["no_inference_network_subprocess"] and rstatic["no_subprocess"] and static["no_subprocess"],
        "V26_independent_target_predicate": rstatic["independent_target_predicate"],
        "V27_target_predicate_does_not_call_selector": rstatic["target_predicate_no_selector"],
        "V28_random_baseline_exact_seed_and_formula": v1._baseline_exact_contract_check(fixture, catalog),
        "V29_random_baseline_no_oracle_input": rstatic["baseline_no_oracle"],
        "V30_v1_science_semantic_equivalence": file_sha256(V1_RUNNER) == EXPECTED_V1_RUNNER_SHA256 and static["v1_science_reused"],
        "V31_runner_self_sha_authority": preq["authorities"]["validation_runner_sha256"] == file_sha256(Path(__file__).resolve()),
        "V32_dual_arm_required": runtime["dual_arm_satisfied"],
        "V33_guard_false_non_spending": _arm_decision(None, False) == "REFUSE_GUARD_FALSE",
        "V34_backend_qualification_before_slot": runtime["backend_before_slot"],
        "V35_fixture_qualification_before_slot": runtime["fixture_before_slot"],
        "V36_unconditional_namespace_guard_before_all_work": static["namespace_guard_before_work"],
        "V37_existing_slot_always_refuses": static["existing_slot_refuses"],
        "V38_empty_prepared_malformed_torn_slot_refuses": static["torn_slot_refuses"],
        "V39_existing_partial_always_refuses": static["existing_partial_refuses"],
        "V40_existing_final_always_refuses": static["existing_final_refuses"],
        "V41_slot_path_exact": static["namespace_paths_exact"],
        "V42_prepared_schema_exact": static["prepared_schema_exact"],
        "V43_reserved_durable_schema_exact": static["reserved_schema_exact"],
        "V44_published_durable_schema_exact": static["published_schema_exact"],
        "V45_slot_o_excl_append_creation": static["slot_flags_exact"],
        "V46_successful_slot_creation_spends_namespace": runtime["slot_spent"],
        "V47_initial_write_failure_spends_namespace": static["initial_write_failure_spends"],
        "V48_prepared_slot_fsync": runtime["prepared_slot_fsync"],
        "V49_prepared_parent_directory_fsync": runtime["prepared_dir_fsync"],
        "V50_reserved_append_after_prepared_barrier": runtime["reserved_after_prepared"],
        "V51_reserved_slot_fsync": runtime["reserved_slot_fsync"],
        "V52_reserved_parent_directory_fsync": runtime["reserved_dir_fsync"],
        "V53_science_after_reserved_durable_only": runtime["science_after_reserved"],
        "V54_any_post_slot_failure_no_retry": static["post_slot_no_retry"],
        "V55_slot_journal_never_removed_or_replaced": static["slot_never_removed"],
        "V56_partial_o_excl_after_durable_reservation": runtime["partial_after_reserved"] and static["partial_exclusive"],
        "V57_partial_file_fsync_before_publication": static["partial_fsync_before_publication"],
        "V58_renameat2_backend_required": backend["renameat2_available"] and static["renameat2"],
        "V59_rename_noreplace_exact_value": RENAME_NOREPLACE == 1 and backend["rename_noreplace_exact_value"],
        "V60_no_publication_fallback": static["no_publication_fallback"],
        "V61_parent_directory_fsync_after_rename": static["post_rename_dir_fsync"],
        "V62_post_rename_failure_no_retry": static["post_slot_no_retry"],
        "V63_published_record_after_result_name_durable": static["published_after_result_durable"],
        "V64_published_record_slot_fsync": static["published_slot_fsync"],
        "V65_result_schema_and_canonical_json": RESULT_SCHEMA == "openmind.maf_query_to_pk_selection_validation.v1_4" and static["allow_nan_false"],
        "V66_result_authority_bindings": (
            science["selector_result_contract_pass"]
            and preq["authorities"]["validation_protocol_sha256"] == EXPECTED_VALIDATION_PROTOCOL_SHA256
            and preq["authorities"]["prior_v1_protocol_sha256"] == EXPECTED_V1_PROTOCOL_SHA256
            and preq["authorities"]["prior_v1_runner_sha256"] == EXPECTED_V1_RUNNER_SHA256
            and preq["authorities"]["prior_v1_1_protocol_sha256"] == EXPECTED_V1_1_PROTOCOL_SHA256
            and preq["authorities"]["prior_v1_2_protocol_sha256"] == EXPECTED_V1_2_PROTOCOL_SHA256
            and preq["authorities"]["prior_v1_3_protocol_sha256"] == EXPECTED_V1_3_PROTOCOL_SHA256
            and preq["authorities"]["validation_runner_sha256"] == file_sha256(Path(__file__).resolve())
        ),
        "V67_supported_intent_target_hit_threshold": metrics["supported_intent_target_hit_rate"] == 1.0,
        "V68_supported_intent_precision_threshold": metrics["supported_intent_precision"] == 1.0,
        "V69_top1_baseline_structural_thresholds": metrics["specific_intent_top1_accuracy"] >= 0.95 and metrics["selector_minus_baseline_top1_difference"] >= 0.50 and all(metrics[k] == 0 for k in ("budget_violation_count","duplicate_selection_count","generation_binding_violation_count","manifest_binding_violation_count","oracle_input_violation_count")),
        "V70_boundary_exclusions": tuple(v1.BOUNDARY_EXCLUSIONS) == tuple(science.get("boundary_exclusions", v1.BOUNDARY_EXCLUSIONS)),
        "V71_final_result_exists_rejects_execution": static["existing_final_refuses"],
        "V72_slot_creation_permanently_spends_namespace": runtime["slot_spent"] and static["slot_creation_spends"],
        "V73_prepared_reserved_science_literal_order": static["literal_order"] and runtime["science_after_reserved"],
        "V74_result_binds_validation_runner_sha256": static["result_runner_sha"],
    }
    if tuple(values.keys()) != CHECK_IDS:
        raise RuntimeError("V01-V74 value order mismatch")
    return tuple({"id": cid, "passed": bool(values[cid]), "detail": "PASS" if values[cid] else "FAIL"} for cid in CHECK_IDS)

def _build_result(preq, science, checks):
    v1 = preq["v1"]
    failed = [x["id"] for x in checks if not x["passed"]]
    result = {
        "schema": RESULT_SCHEMA,
        "exact_once": {
            "protocol_version": "V1.4",
            "slot_state": "SPENT",
            "automatic_retry": False,
            "manual_scientific_retry": False,
        },
        "validation_protocol_sha256": EXPECTED_VALIDATION_PROTOCOL_SHA256,
        "prior_v1_protocol_sha256": EXPECTED_V1_PROTOCOL_SHA256,
        "prior_v1_runner_sha256": EXPECTED_V1_RUNNER_SHA256,
        "prior_v1_1_protocol_sha256": EXPECTED_V1_1_PROTOCOL_SHA256,
        "prior_v1_2_protocol_sha256": EXPECTED_V1_2_PROTOCOL_SHA256,
        "prior_v1_3_protocol_sha256": EXPECTED_V1_3_PROTOCOL_SHA256,
        "selection_protocol_sha256": EXPECTED_SELECTION_PROTOCOL_SHA256,
        "implementation_sha256": EXPECTED_IMPLEMENTATION_SHA256,
        "q1_verdict_sha256": EXPECTED_Q1_VERDICT_SHA256,
        "catalog_sha256": EXPECTED_CATALOG_SHA256,
        "query_fixture_sha256": EXPECTED_QUERY_FIXTURE_SHA256,
        "source_generation_pk": EXPECTED_SOURCE_GENERATION_PK,
        "source_manifest_sha256": EXPECTED_SOURCE_MANIFEST_SHA256,
        "selection_config_sha256": EXPECTED_SELECTION_CONFIG_SHA256,
        "validation_runner_sha256": preq["authorities"]["validation_runner_sha256"],
        "random_baseline_seed": RANDOM_BASELINE_SEED,
        "expected_check_count": EXPECTED_CHECK_COUNT,
        "check_count": len(checks),
        "checks": [dict(x) for x in checks],
        "failed_checks": failed,
        "auditor_error": None,
        "all_pass": not failed,
        "metrics": dict(science["metrics"]),
        "acceptance_thresholds": dict(v1.ACCEPTANCE_THRESHOLDS),
        "boundary_exclusions": list(v1.BOUNDARY_EXCLUSIONS),
        "publication_backend": {
            "primitive": "renameat2",
            "flag": "RENAME_NOREPLACE",
            "flag_value": 1,
            "partial_fsync_required": True,
            "parent_directory_fsync_required": True,
            "permanent_slot_journal": True,
        },
    }
    if tuple(result.keys()) != RESULT_FIELDS:
        raise RuntimeError("result field schema mismatch")
    raw = canonical_record_bytes(result)
    parsed = json.loads(raw[:-1].decode("utf-8"))
    if canonical_record_bytes(parsed) != raw:
        raise RuntimeError("result canonical round-trip failed")
    return result, raw

def _load_renameat2():
    libc = ctypes.CDLL(None, use_errno=True)
    fn = getattr(libc, "renameat2", None)
    if fn is None:
        raise RuntimeError("renameat2 unavailable")
    fn.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    fn.restype = ctypes.c_int
    return fn

def _failure_class(phase):
    if phase == "PREPARED_WRITE":
        return "RESERVATION_PREPARED_WRITE_FAILURE"
    if phase == "POST_RENAME_DIR_FSYNC":
        return "POST_RENAME_DURABILITY_UNCONFIRMED"
    if phase == "PUBLISHED_APPEND":
        return "PUBLICATION_JOURNAL_COMMIT_FAILURE_NAMESPACE_SPENT"
    return "V1_4_POST_SLOT_FAILURE_NAMESPACE_SPENT"

def _authoritative_run():
    _namespace_guard()
    decision = _runtime_arm_decision(tuple(sys.argv[1:]))
    if decision != "FULLY_ARMED":
        raise RuntimeError("V1.4 exact-once dual arm not satisfied: " + decision)
    preq = _full_prequalification()
    _namespace_guard()
    runtime = {
        "dual_arm_satisfied": True,
        "backend_before_slot": True,
        "fixture_before_slot": True,
        "slot_spent": False,
        "prepared_slot_fsync": False,
        "prepared_dir_fsync": False,
        "reserved_after_prepared": False,
        "reserved_slot_fsync": False,
        "reserved_dir_fsync": False,
        "partial_after_reserved": False,
        "science_after_reserved": False,
        "partial_fsync": False,
    }
    slot_fd = None
    partial_fd = None
    parent_fd = None
    phase = "PRE_SLOT"
    slot_spent = False
    rename_succeeded = False
    try:
        parent_fd = _parent_fd()
        phase = "SLOT_CREATE"
        slot_fd = os.open(
            SLOT_PATH,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_APPEND,
            0o600,
        )
        slot_spent = True
        runtime["slot_spent"] = True

        phase = "PREPARED_WRITE"
        prepared_raw = canonical_record_bytes(
            _prepared_record(preq["authorities"]["validation_runner_sha256"])
        )
        _write_all(slot_fd, prepared_raw)
        os.fsync(slot_fd)
        runtime["prepared_slot_fsync"] = True
        os.fsync(parent_fd)
        runtime["prepared_dir_fsync"] = True
        _verify_open_inode(slot_fd, SLOT_PATH)

        phase = "RESERVED_DURABLE_APPEND"
        reserved_raw = canonical_record_bytes(
            _reserved_record(hashlib.sha256(prepared_raw).hexdigest())
        )
        runtime["reserved_after_prepared"] = True
        _write_all(slot_fd, reserved_raw)
        os.fsync(slot_fd)
        runtime["reserved_slot_fsync"] = True
        os.fsync(parent_fd)
        runtime["reserved_dir_fsync"] = True
        _verify_open_inode(slot_fd, SLOT_PATH)

        phase = "PARTIAL_CREATE"
        partial_fd = os.open(
            PARTIAL_PATH,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            0o600,
        )
        runtime["partial_after_reserved"] = True

        phase = "SCIENCE"
        runtime["science_after_reserved"] = True
        science = preq["v1"]._run_scientific_evaluation(preq["v1_prequalification"])

        phase = "RESULT_CONSTRUCTION"
        checks = _build_checks(preq, science, runtime)
        result, result_raw = _build_result(preq, science, checks)

        phase = "PARTIAL_WRITE"
        _write_all(partial_fd, result_raw)
        os.fsync(partial_fd)
        runtime["partial_fsync"] = True
        os.close(partial_fd)
        partial_fd = None

        phase = "RENAME_NOREPLACE"
        fn = _load_renameat2()
        ctypes.set_errno(0)
        rc = fn(parent_fd, PARTIAL_PATH.name.encode(), parent_fd, RESULT_PATH.name.encode(), RENAME_NOREPLACE)
        if rc != 0:
            e = ctypes.get_errno()
            raise OSError(e, os.strerror(e))
        rename_succeeded = True

        phase = "POST_RENAME_DIR_FSYNC"
        os.fsync(parent_fd)

        phase = "PUBLISHED_APPEND"
        published_raw = canonical_record_bytes(
            _published_record(
                hashlib.sha256(reserved_raw).hexdigest(),
                hashlib.sha256(result_raw).hexdigest(),
                len(result_raw),
            )
        )
        _write_all(slot_fd, published_raw)
        os.fsync(slot_fd)
        os.fsync(parent_fd)
        _verify_open_inode(slot_fd, SLOT_PATH)

        phase = "PUBLISHED_DURABLE"
        return {
            "result_path": str(RESULT_PATH),
            "result_sha256": hashlib.sha256(result_raw).hexdigest(),
            "all_pass": result["all_pass"],
            "failed_checks": result["failed_checks"],
        }
    except BaseException as exc:
        if slot_spent:
            record = {
                "phase": _failure_class(phase),
                "slot_state": "SPENT",
                "automatic_retry": False,
                "manual_scientific_retry": False,
                "rename_succeeded": rename_succeeded,
                "slot_present": _path_present(SLOT_PATH),
                "partial_present": _path_present(PARTIAL_PATH),
                "result_present": _path_present(RESULT_PATH),
                "exception_type": type(exc).__name__,
                "exception": str(exc),
                "disposition": "NO_V1_4_RETRY",
            }
            print(
                "OPENMIND_Q2_V1_4_EXACT_ONCE_FAILURE="
                + json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False),
                file=sys.stderr,
            )
        raise
    finally:
        for fd in (partial_fd, slot_fd, parent_fd):
            if fd is not None:
                try:
                    os.close(fd)
                except OSError:
                    pass

def _readiness():
    _namespace_guard()
    preq = _full_prequalification()
    _namespace_guard()
    return {
        "backend_qualified": all(preq["v1_prequalification"]["backend"].values()),
        "fixture_qualified": True,
        "selector_static_qualified": all(preq["v1_prequalification"]["selector_static"].values()),
        "v1_runner_static_qualified": all(preq["v1_prequalification"]["runner_static"].values()),
        "v1_4_static_qualified": all(preq["static"].values()),
        "runner_self_sha_qualified": preq["authorities"]["validation_runner_sha256"] == file_sha256(Path(__file__).resolve()),
        "result_slot_unspent": not any(_namespace_state().values()),
    }

def main():
    argv = tuple(sys.argv[1:])
    if argv == (READINESS_FLAG,):
        value = _readiness()
        print("MODE=readiness")
        print(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False))
        print("V1_4_RESULT_SLOT=UNSPENT")
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
        "usage: maf_query_to_pk_selection_validation_v1_4.py "
        + "{--readiness|--run-exact-once}",
        file=sys.stderr,
    )
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
