#!/usr/bin/env python3

import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT_DIR = Path(__file__).resolve().parent

if str(EXPERIMENT_DIR) not in sys.path:
    sys.path.insert(0, str(EXPERIMENT_DIR))

PREREG_PATH = EXPERIMENT_DIR / "MAF_PHASE_6E_B_S1_BOUNDED_EXPANSION_RECOVERY_PREREGISTRATION_V1.md"
PREREG_SHA256 = "823853c71e378d2a559c95d80177990bea59e546965ce579cae9e589aa3991bf"

RUNNER_CONTRACT_PATH = EXPERIMENT_DIR / "MAF_PHASE_6E_B_S1_BOUNDED_EXPANSION_RECOVERY_RUNNER_IMPLEMENTATION_CONTRACT_V1.md"
RUNNER_CONTRACT_SHA256 = "3bd876254e4ab549d099ef3b473e0b775c4d8dac43111a3f660937bcc83ca292"

INCIDENT_PATH = EXPERIMENT_DIR / "MAF_PHASE_6E_B_EXECUTION_FAILURE_INCIDENT_AND_CORRECTIVE_SUCCESSOR_DESIGN_V1.md"
INCIDENT_SHA256 = "1ecf171bee1e6470d5ac48c1482a2166eca05c895313eeb4acbc8e90b64a64ad"

ORIGINAL_PREREG_PATH = EXPERIMENT_DIR / "MAF_PHASE_6E_B_BOUNDED_EXPANSION_RECOVERY_PREREGISTRATION_V1.md"
ORIGINAL_PREREG_SHA256 = "85b44a1e78193f020c54b12f9b0698b8c20cc3a69365647b9520132d4b01dacd"

ORIGINAL_RUNNER_CONTRACT_PATH = EXPERIMENT_DIR / "MAF_PHASE_6E_B_BOUNDED_EXPANSION_RECOVERY_RUNNER_IMPLEMENTATION_CONTRACT_V1.md"
ORIGINAL_RUNNER_CONTRACT_SHA256 = "747261cce78f770401155e4823bc3558bc6e41770f107d35a965e014e5cc6fb5"

ORIGINAL_RUNNER_PATH = EXPERIMENT_DIR / "maf_phase_6e_b_bounded_expansion_recovery_v1.py"
ORIGINAL_RUNNER_SHA256 = "c7e1efc2a5fddb85c49962f993be34709405979a5e9e60183a6975c7d18ee891"

PHASE_6E_ENTRY_PATH = EXPERIMENT_DIR / "MAF_PHASE_6E_ENTRY_CHECKPOINT.md"
PHASE_6E_ENTRY_SHA256 = "1807437ea97e46a6cc687adbbe8c384dabae45a562f1d2aef6bd37e43b4bbe35"

ARCHITECTURE_PATH = EXPERIMENT_DIR / "MAF_QUERY_SCOPED_WORKING_SET_ARCHITECTURE.md"
ARCHITECTURE_SHA256 = "7df826096e506d13502e442fb11f7e1f18fb2c5a342f4214b91a3c3df043559c"

CAPSULE_PROTOCOL_PATH = EXPERIMENT_DIR / "MAF_QUERY_CAPSULE_DATA_MODEL_V1_PROTOCOL.md"
CAPSULE_PROTOCOL_SHA256 = "5255a58c8c6340c251e24ae8543760fcd66a8deb8be1a8356ad5b78ad898edda"

CAPSULE_IMPL_PATH = EXPERIMENT_DIR / "maf_query_capsule_data_model_v1.py"
CAPSULE_IMPL_SHA256 = "f897b97011714f3c84b7350c6bb53e800232be8a5d34e5148a3e50a81952976e"

SELECTOR_PROTOCOL_PATH = EXPERIMENT_DIR / "MAF_QUERY_TO_PK_SELECTION_V1_PROTOCOL.md"
SELECTOR_PROTOCOL_SHA256 = "b42a0643976c2393871e3b826ba5573b4de981b49603de63230d69cf57be0811"

SELECTOR_IMPL_PATH = EXPERIMENT_DIR / "maf_query_to_pk_selection_v1.py"
SELECTOR_IMPL_SHA256 = "e21c05e352fe921b791e8c936425727a98911ce7566989672a96bfd2b9613fa2"

QUERY_FIXTURE_PATH = EXPERIMENT_DIR / "maf_query_to_pk_selection_validation_v1_queries.json"
QUERY_FIXTURE_SHA256 = "32f4636bd5e8ceee0dca8342335279a6f8e6acafe866a5469f2c23aa2655202a"

CATALOG_PATH = EXPERIMENT_DIR / "maf_query_to_pk_selection_validation_v1_catalog.json"
CATALOG_SHA256 = "c51ef0fabeb10e7c8a091a093aa1934620a69b2026b5a87cb02477b9dd7ca900"

GENERATION_AUTHORITY_PATH = EXPERIMENT_DIR / "maf_query_to_pk_selection_validation_v1_generation_construction_authority.json"
GENERATION_AUTHORITY_SHA256 = "a5e953ae2ab2dd11a9f6dc564ae5ee57cb064d6eea0a8a5517191b4a6efc1a6d"

GENERATION_MANIFEST_PATH = ROOT / "results/runtime/maf_query_to_pk_selection_validation_v1_generation/validation_generation.manifest.json"
GENERATION_MANIFEST_SHA256 = "28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3"

REFERENCE_FIXTURE_PATH = EXPERIMENT_DIR / "maf_phase_6e_a_reference_state_fixture_v1.json"
REFERENCE_FIXTURE_SHA256 = "870b656e0c3181ec8f7be1537bdeafde10fffd1b947f5372d21cdee4c00a83a0"

PHASE_6E_A_RESULT_PATH = EXPERIMENT_DIR / "maf_phase_6e_a_selective_working_set_sufficiency_v1.json"
PHASE_6E_A_RESULT_SHA256 = "f86433603e68fc9f1e5c65f7d3ecbd8d9ce9313d252c605dd6e2cada18a91c86"

PHASE_6E_A_VERDICT_PATH = EXPERIMENT_DIR / "MAF_PHASE_6E_A_SELECTIVE_WORKING_SET_SUFFICIENCY_V1_VERDICT.md"
PHASE_6E_A_VERDICT_SHA256 = "a6c9ce2f2207beb252b2c02b47e27878b27e72736dad4275ab9905d40812e334"

OBJECT_IMPL_PATH = EXPERIMENT_DIR / "maf_object_v1.py"
OBJECT_IMPL_SHA256 = "eed6cbd96995412a632883f3c534f9023e7711ea8eb437afe35a48312502f63b"

ORIGINAL_OUTPUT_PATH = EXPERIMENT_DIR / "maf_phase_6e_b_bounded_expansion_recovery_v1.json"
OUTPUT_PATH = EXPERIMENT_DIR / "maf_phase_6e_b_s1_bounded_expansion_recovery_v1.json"

EXPECTED_BRANCH = "labs/multidimensional-maf"
EXPECTED_RUNNER_HEAD_ENV = "OPENMIND_EXPECTED_S1_HEAD"

SOURCE_MODEL_PK = "mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258"
SOURCE_GENERATION_PK = "mafgen:v1:45a80a2aa271ce04853003185b6a1227cb309bd1e3e2dc538eea849fac9f5db0"
SOURCE_MANIFEST_SHA256 = "28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3"
SOURCE_GGUF_PATH = Path("/data/data/com.termux/files/home/qwen2.5-coder-q8_0.gguf")
SOURCE_GGUF_SHA256 = "507de59046601282ba768a9789900e6ccf60ed93ddf346730b7c68eb0715bc47"

EXPANSION_POLICY = "bounded_v1"
MAX_OBJECT_BUDGET = 4
MAX_EXPANSION_ROUNDS = 3
ROUND_BUDGETS = (1, 2, 3, 4)
ROUND_CONFIG_SHA256 = (
    "2dd2925a3d9f63197deff6dc98f951c5177dc63dc08818b6492228dbac7d5576",
    "57f751a3a019bccd58c5c32b4f5ecaf78283f49cc146896d61492ce31dfdd1c6",
    "67dd6e5589cb16374e949b3ed633c3364f0ccb1d8c2b0a9ca1c6eaa2d2ceed56",
    "0caeaeaafdd870e6b02ccc8b4450576883d4ef5234ba689c472e3b14d9dbe120",
)

TRACE_SCHEMA = "openmind.maf_phase_6e_b_s1_expansion_trace_snapshot.v1"
RESULT_SCHEMA = "openmind.maf_phase_6e_b_s1_bounded_expansion_recovery.v1"

BASELINE_COUNT = 440
BASELINE_SHA256 = "f206c0eed32daef9ed0cfaae195aa56a343a85437ebd3135aeafdb4c1ffacddd"

FROZEN_AUTHORITIES = (
    (PREREG_PATH, PREREG_SHA256),
    (RUNNER_CONTRACT_PATH, RUNNER_CONTRACT_SHA256),
    (INCIDENT_PATH, INCIDENT_SHA256),
    (ORIGINAL_PREREG_PATH, ORIGINAL_PREREG_SHA256),
    (ORIGINAL_RUNNER_CONTRACT_PATH, ORIGINAL_RUNNER_CONTRACT_SHA256),
    (ORIGINAL_RUNNER_PATH, ORIGINAL_RUNNER_SHA256),
    (PHASE_6E_ENTRY_PATH, PHASE_6E_ENTRY_SHA256),
    (ARCHITECTURE_PATH, ARCHITECTURE_SHA256),
    (CAPSULE_PROTOCOL_PATH, CAPSULE_PROTOCOL_SHA256),
    (CAPSULE_IMPL_PATH, CAPSULE_IMPL_SHA256),
    (SELECTOR_PROTOCOL_PATH, SELECTOR_PROTOCOL_SHA256),
    (SELECTOR_IMPL_PATH, SELECTOR_IMPL_SHA256),
    (QUERY_FIXTURE_PATH, QUERY_FIXTURE_SHA256),
    (CATALOG_PATH, CATALOG_SHA256),
    (GENERATION_AUTHORITY_PATH, GENERATION_AUTHORITY_SHA256),
    (GENERATION_MANIFEST_PATH, GENERATION_MANIFEST_SHA256),
    (REFERENCE_FIXTURE_PATH, REFERENCE_FIXTURE_SHA256),
    (PHASE_6E_A_RESULT_PATH, PHASE_6E_A_RESULT_SHA256),
    (PHASE_6E_A_VERDICT_PATH, PHASE_6E_A_VERDICT_SHA256),
    (OBJECT_IMPL_PATH, OBJECT_IMPL_SHA256),
)


class Phase6EBS1IntegrityError(RuntimeError):
    pass


def need(condition, message):
    if not condition:
        raise Phase6EBS1IntegrityError(message)


def git(*args):
    result = subprocess.run(
        ("git",) + tuple(args),
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise Phase6EBS1IntegrityError("git failed: " + " ".join(args))
    return result.stdout


def zparts(raw):
    return tuple(item for item in raw.split(b"\0") if item)


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path, chunk_bytes=1024 * 1024):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(chunk_bytes)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")


def canonical_reference_fixture_bytes(value):
    return canonical_bytes(value) + b"\n"


def verify_pre_execution_state():
    need(git("branch", "--show-current").decode().strip() == EXPECTED_BRANCH, "scientific branch mismatch")
    expected_head = os.environ.get(EXPECTED_RUNNER_HEAD_ENV, "").strip()
    need(bool(expected_head), "frozen S1 runner HEAD binding was not supplied")
    need(git("rev-parse", "HEAD").decode().strip() == expected_head, "frozen S1 runner HEAD mismatch")
    need(not os.path.lexists(ORIGINAL_OUTPUT_PATH), "original spent Phase 6E-B result path must remain absent")
    need(not os.path.lexists(OUTPUT_PATH), "S1 result path already exists")
    need(git("diff", "--name-only", "-z") == b"", "tracked worktree is dirty")
    need(git("diff", "--cached", "--name-only", "-z") == b"", "index is not empty")
    untracked = git("ls-files", "-z", "--others", "--exclude-standard")
    need(len(zparts(untracked)) == BASELINE_COUNT, "untracked baseline count mismatch")
    need(sha256_bytes(untracked) == BASELINE_SHA256, "untracked baseline SHA256 mismatch")
    for path, expected_sha in FROZEN_AUTHORITIES:
        need(path.is_file(), "frozen authority missing: " + str(path))
        need(sha256_file(path) == expected_sha, "frozen authority SHA256 mismatch: " + str(path))
    need(SOURCE_GGUF_PATH.is_file(), "source GGUF missing")
    need(sha256_file(SOURCE_GGUF_PATH) == SOURCE_GGUF_SHA256, "source GGUF SHA256 mismatch")


def import_frozen_modules():
    selector = importlib.import_module("maf_query_to_pk_selection_v1")
    capsule = importlib.import_module("maf_query_capsule_data_model_v1")
    object_module = importlib.import_module("maf_object_v1")
    return selector, capsule, object_module


def load_non_oracle_inputs(selector_module):
    query_raw = QUERY_FIXTURE_PATH.read_bytes()
    need(sha256_bytes(query_raw) == QUERY_FIXTURE_SHA256, "query fixture changed")
    queries_doc = json.loads(query_raw.decode("utf-8"))
    need(canonical_bytes(queries_doc) == query_raw, "query fixture is not canonical JSON")
    queries = queries_doc["queries"]
    need(len(queries) == 40, "query fixture count mismatch")
    query_ids = tuple(row["query_id"] for row in queries)
    need(len(set(query_ids)) == 40, "duplicate query IDs")
    need(sum(row["query_class"] == "specific_intent" for row in queries) == 24, "specific query count mismatch")
    need(sum(row["query_class"] == "multi_target_intent" for row in queries) == 8, "multi query count mismatch")
    need(sum(row["query_class"] == "fallback_control" for row in queries) == 8, "fallback query count mismatch")
    need(queries_doc["source_generation_pk"] == SOURCE_GENERATION_PK, "query fixture generation mismatch")
    need(queries_doc["source_manifest_sha256"] == SOURCE_MANIFEST_SHA256, "query fixture manifest mismatch")

    catalog_raw = CATALOG_PATH.read_bytes()
    need(sha256_bytes(catalog_raw) == CATALOG_SHA256, "catalog changed")
    catalog_doc = json.loads(catalog_raw.decode("utf-8"))
    need(canonical_bytes(catalog_doc) == catalog_raw, "catalog is not canonical JSON")
    catalog = selector_module.MAFQueryPKCatalogV1.from_mapping(catalog_doc)
    need(catalog.canonical_bytes() == catalog_raw, "catalog canonical round trip mismatch")
    need(catalog.catalog_sha256 == CATALOG_SHA256, "catalog API SHA256 mismatch")
    catalog.require_source_binding(
        source_generation_pk=SOURCE_GENERATION_PK,
        source_manifest_sha256=SOURCE_MANIFEST_SHA256,
    )
    catalog_pks = tuple(entry.object_pk for entry in catalog.entries)
    need(len(catalog_pks) == 12, "catalog object count mismatch")
    return queries, query_ids, catalog, frozenset(catalog_pks)



def load_generation_authorities_non_oracle():
    authority_raw = GENERATION_AUTHORITY_PATH.read_bytes()
    need(sha256_bytes(authority_raw) == GENERATION_AUTHORITY_SHA256, "generation authority changed")
    authority = json.loads(authority_raw.decode("utf-8"))
    bindings = authority["bindings"]
    need(bindings["model_pk"] == SOURCE_MODEL_PK, "generation authority model PK mismatch")
    need(bindings["source_gguf"]["path"] == str(SOURCE_GGUF_PATH), "generation authority source GGUF path mismatch")
    need(bindings["source_gguf"]["sha256"] == SOURCE_GGUF_SHA256, "generation authority source GGUF SHA256 mismatch")
    need(authority["output_layout"]["generation_manifest_path"] == str(GENERATION_MANIFEST_PATH.relative_to(ROOT)), "generation manifest path mismatch")

    manifest_raw = GENERATION_MANIFEST_PATH.read_bytes()
    need(sha256_bytes(manifest_raw) == GENERATION_MANIFEST_SHA256, "generation manifest changed")
    manifest = json.loads(manifest_raw.decode("utf-8"))
    need(manifest["generation_pk"] == SOURCE_GENERATION_PK, "generation manifest PK mismatch")
    descriptor = manifest["descriptor"]
    need(descriptor["model_pk"] == SOURCE_MODEL_PK, "generation descriptor model PK mismatch")
    objects = descriptor["objects"]
    need(len(objects) == 12, "generation descriptor object count mismatch")
    placement_by_pk = {row["object_pk"]: row for row in objects}
    need(len(placement_by_pk) == 12, "duplicate generation descriptor object PK")
    targets = authority["targets"]
    need(len(targets) == 12, "generation authority target count mismatch")
    target_by_pk = {row["object_pk"]: row for row in targets}
    need(len(target_by_pk) == 12, "duplicate generation authority object PK")
    objects_dir = ROOT / authority["output_layout"]["objects_dir"]
    return placement_by_pk, target_by_pk, objects_dir

def build_round_configs(selector_module):
    configs = tuple(
        selector_module.default_selection_config_v1(max_candidates=budget)
        for budget in ROUND_BUDGETS
    )
    actual = tuple(config.selection_config_sha256 for config in configs)
    need(actual == ROUND_CONFIG_SHA256, "round selection configuration SHA256 mismatch")
    return configs


def validate_selection_result(result, budget, config_sha, catalog_pks):
    need(result.source_generation_pk == SOURCE_GENERATION_PK, "selection generation mismatch")
    need(result.source_manifest_sha256 == SOURCE_MANIFEST_SHA256, "selection manifest mismatch")
    need(result.catalog_sha256 == CATALOG_SHA256, "selection catalog SHA256 mismatch")
    need(result.selection_config_sha256 == config_sha, "selection config SHA256 mismatch")
    selected = tuple(result.selected_object_pks)
    need(len(selected) <= budget, "selection exceeds round candidate budget")
    need(len(selected) == len(set(selected)), "selection contains duplicate object PK")
    need(all(object_pk in catalog_pks for object_pk in selected), "selection contains object outside frozen catalog")
    return selected


def select_round(selector_module, queries, catalog, catalog_pks, config, round_index, previous):
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
        selected = validate_selection_result(result, budget, config_sha, catalog_pks)
        if round_index == 0:
            additional = selected
            cumulative = selected
        else:
            prior = previous[query_id]
            previous_selected = tuple(prior["selected_object_pks"])
            previous_set = set(previous_selected)
            current_set = set(selected)
            need(previous_set <= current_set, "non-monotonic selector result: " + query_id)
            need(result.query_signature == prior["query_signature"], "query signature changed across rounds: " + query_id)
            need(bool(result.fallback_used) == prior["fallback_used"], "fallback classification changed across rounds: " + query_id)
            additional = tuple(object_pk for object_pk in selected if object_pk not in previous_set)
            cumulative = tuple(prior["cumulative_route_order"]) + additional
            need(len(cumulative) == len(set(cumulative)), "cumulative route contains duplicate PK: " + query_id)
            need(set(cumulative) == current_set, "cumulative route differs from current selection: " + query_id)
        rows[query_id] = {
            "query_signature": result.query_signature,
            "fallback_used": bool(result.fallback_used),
            "selected_object_pks": selected,
            "additional_pks": additional,
            "cumulative_route_order": cumulative,
        }
    need(tuple(rows) == tuple(row["query_id"] for row in queries), "round query order mismatch")
    return rows


def build_round_zero_capsules(capsule_module, queries, round_zero):
    capsules = {}
    for source_row in queries:
        query_id = source_row["query_id"]
        state = round_zero[query_id]
        query_pk = capsule_module.derive_query_pk(
            query_signature=state["query_signature"],
            selection_config_sha256=ROUND_CONFIG_SHA256[0],
            source_generation_pk=SOURCE_GENERATION_PK,
            source_manifest_sha256=SOURCE_MANIFEST_SHA256,
        )
        capsule = capsule_module.MAFQueryCapsuleV1(
            schema=capsule_module.QUERY_CAPSULE_SCHEMA,
            query_pk=query_pk,
            query_signature=state["query_signature"],
            source_generation_pk=SOURCE_GENERATION_PK,
            source_manifest_sha256=SOURCE_MANIFEST_SHA256,
            initial_object_pks=state["selected_object_pks"],
            selected_relationship_pks=(),
            route_order=state["selected_object_pks"],
            expansion_policy=EXPANSION_POLICY,
            max_object_budget=MAX_OBJECT_BUDGET,
            max_expansion_rounds=MAX_EXPANSION_ROUNDS,
            selection_config_sha256=ROUND_CONFIG_SHA256[0],
        )
        capsule.require_source_binding(
            source_generation_pk=SOURCE_GENERATION_PK,
            source_manifest_sha256=SOURCE_MANIFEST_SHA256,
        )
        capsule_raw = capsule.canonical_bytes()
        need(capsule_module.MAFQueryCapsuleV1.from_json_bytes(capsule_raw).canonical_bytes() == capsule_raw, "capsule canonical round trip mismatch: " + query_id)
        capsules[query_id] = {
            "query_pk": query_pk,
            "capsule_sha256": sha256_bytes(capsule_raw),
        }
    need(tuple(capsules) == tuple(row["query_id"] for row in queries), "capsule query order mismatch")
    return capsules


def build_complete_trace(selector_module, capsule_module, queries, catalog, catalog_pks, configs):
    round_states = []
    round_zero = select_round(
        selector_module,
        queries,
        catalog,
        catalog_pks,
        configs[0],
        0,
        None,
    )
    round_states.append(round_zero)
    capsules = build_round_zero_capsules(capsule_module, queries, round_zero)
    previous = round_zero
    for round_index in (1, 2, 3):
        current = select_round(
            selector_module,
            queries,
            catalog,
            catalog_pks,
            configs[round_index],
            round_index,
            previous,
        )
        round_states.append(current)
        previous = current

    trace_queries = []
    for source_row in queries:
        query_id = source_row["query_id"]
        round_records = []
        for round_index in range(4):
            state = round_states[round_index][query_id]
            round_records.append(
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
        trace_queries.append(
            {
                "query_id": query_id,
                "query_signature": round_zero[query_id]["query_signature"],
                "query_pk": capsules[query_id]["query_pk"],
                "round_zero_capsule_sha256": capsules[query_id]["capsule_sha256"],
                "rounds": round_records,
            }
        )

    trace = {
        "schema": TRACE_SCHEMA,
        "source_generation_pk": SOURCE_GENERATION_PK,
        "source_manifest_sha256": SOURCE_MANIFEST_SHA256,
        "query_fixture_sha256": QUERY_FIXTURE_SHA256,
        "catalog_sha256": CATALOG_SHA256,
        "selector_sha256": SELECTOR_IMPL_SHA256,
        "capsule_implementation_sha256": CAPSULE_IMPL_SHA256,
        "expansion_policy": EXPANSION_POLICY,
        "max_object_budget": MAX_OBJECT_BUDGET,
        "max_expansion_rounds": MAX_EXPANSION_ROUNDS,
        "round_config_sha256": list(ROUND_CONFIG_SHA256),
        "queries": trace_queries,
    }
    trace_raw = canonical_bytes(trace)
    need(len(trace_queries) == 40, "trace query count mismatch")
    need(tuple(row["query_id"] for row in trace_queries) == tuple(row["query_id"] for row in queries), "trace query order mismatch")
    forbidden_keys = {
        "required_object_pks",
        "required_object_pk",
        "required_pks",
        "reference_payload_sha256",
        "reference_object",
        "expected_payload_sha256",
    }
    for row in trace_queries:
        need(not forbidden_keys.intersection(row), "trace contains forbidden reference field")
        for round_row in row["rounds"]:
            need(not forbidden_keys.intersection(round_row), "trace round contains forbidden reference field")
    return trace, trace_raw, sha256_bytes(trace_raw)


def load_reference_fixture_after_snapshot(expected_query_ids):
    raw = REFERENCE_FIXTURE_PATH.read_bytes()
    need(sha256_bytes(raw) == REFERENCE_FIXTURE_SHA256, "reference fixture changed after trace snapshot")
    fixture = json.loads(raw.decode("utf-8"))
    need(canonical_reference_fixture_bytes(fixture) == raw, "reference fixture is not canonical JSON with terminal LF")
    need(fixture["source_model_pk"] == SOURCE_MODEL_PK, "reference model PK mismatch")
    need(fixture["source_generation_pk"] == SOURCE_GENERATION_PK, "reference generation PK mismatch")
    need(fixture["source_manifest_sha256"] == SOURCE_MANIFEST_SHA256, "reference manifest mismatch")
    need(fixture["source_gguf_sha256"] == SOURCE_GGUF_SHA256, "reference GGUF mismatch")
    need(len(fixture["queries"]) == 40, "reference query count mismatch")
    need(tuple(row["query_id"] for row in fixture["queries"]) == expected_query_ids, "reference query order mismatch")
    return fixture


def inspect_generation_bound_object(object_module, object_pk, reference_object, placement_by_pk, target_by_pk, objects_dir):
    need(object_pk in placement_by_pk, "required PK missing from generation descriptor: " + object_pk)
    need(object_pk in target_by_pk, "required PK missing from generation authority: " + object_pk)
    placement = placement_by_pk[object_pk]
    target = target_by_pk[object_pk]
    object_path = objects_dir / target["object_filename"]
    need(object_path.is_file(), "dedicated MAF object file missing: " + str(object_path))
    disk_object_sha256 = sha256_file(object_path)
    need(disk_object_sha256 == placement["object_file_sha256"], "serialized object SHA256 mismatch: " + object_pk)
    need(placement["payload_sha256"] == reference_object["payload_sha256"], "generation/reference payload authority mismatch: " + object_pk)
    view = object_module.inspect_object(object_path)
    need(view.tensor_name == reference_object["tensor_name"], "object tensor name mismatch: " + object_pk)
    need(view.tensor_type == reference_object["tensor_type"], "object tensor type mismatch: " + object_pk)
    need(list(view.dims) == reference_object["dims"], "object dims mismatch: " + object_pk)
    need(view.element_count == reference_object["element_count"], "object element count mismatch: " + object_pk)
    observed = view.payload_sha256
    descriptor_payload = placement["payload_sha256"]
    reference_payload = reference_object["payload_sha256"]
    need(observed == descriptor_payload, "observed payload differs from generation descriptor: " + object_pk)
    return {
        "object_pk": object_pk,
        "serialized_object_sha256": disk_object_sha256,
        "descriptor_payload_sha256": descriptor_payload,
        "reference_payload_sha256": reference_payload,
        "observed_payload_sha256": observed,
        "descriptor_payload_match": observed == descriptor_payload,
        "reference_payload_match": observed == reference_payload,
        "payload_match": observed == reference_payload,
    }


def evaluate_after_snapshot(object_module, queries, trace, fixture, placement_by_pk, target_by_pk, objects_dir):
    reference_queries = {row["query_id"]: row for row in fixture["queries"]}
    reference_objects = {row["object_pk"]: row for row in fixture["objects"]}
    trace_queries = {row["query_id"]: row for row in trace["queries"]}
    need(len(reference_queries) == 40, "duplicate reference query IDs")
    need(len(reference_objects) == 12, "duplicate reference object PKs")
    need(len(trace_queries) == 40, "duplicate trace query IDs")

    payload_cache = {}
    results = []
    challenge_count = 0
    initial_sufficient_count = 0
    recovered_count = 0
    not_recovered_count = 0
    control_count = 0

    for source_row in queries:
        query_id = source_row["query_id"]
        query_class = source_row["query_class"]
        trace_row = trace_queries[query_id]
        reference_query = reference_queries[query_id]
        query_text_sha256 = sha256_bytes(source_row["query_text"].encode("utf-8"))
        need(query_text_sha256 == reference_query["query_text_sha256"], "query text identity mismatch: " + query_id)
        required = tuple(reference_query["required_object_pks"])
        need(required == tuple(sorted(required)), "reference required PK ordering mismatch: " + query_id)
        round_records = trace_row["rounds"]
        need(len(round_records) == 4, "trace round count mismatch: " + query_id)

        round_zero_selected = tuple(round_records[0]["selected_object_pks"])
        initial_missing = tuple(sorted(set(required).difference(round_zero_selected)))
        final_selected = tuple(round_records[3]["selected_object_pks"])
        final_covered = tuple(sorted(set(required).intersection(final_selected)))
        final_missing = tuple(sorted(set(required).difference(final_selected)))

        payload_evidence = []
        payload_mismatch = []
        for object_pk in final_covered:
            need(object_pk in reference_objects, "required reference object missing: " + object_pk)
            if object_pk not in payload_cache:
                payload_cache[object_pk] = inspect_generation_bound_object(
                    object_module,
                    object_pk,
                    reference_objects[object_pk],
                    placement_by_pk,
                    target_by_pk,
                    objects_dir,
                )
            evidence = dict(payload_cache[object_pk])
            payload_evidence.append(evidence)
            if not evidence["payload_match"]:
                payload_mismatch.append(object_pk)

        if query_class == "fallback_control":
            need(len(required) == 0, "fallback control required set is not empty: " + query_id)
            initial_classification = "CONTROL"
            earliest_recovery_round = None
            verdict = "CONTROL"
            control_count += 1
        else:
            need(query_class in {"specific_intent", "multi_target_intent"}, "unexpected query class: " + query_id)
            if not initial_missing:
                initial_classification = "INITIAL_SUFFICIENT"
                earliest_recovery_round = None
                verdict = "INITIAL_SUFFICIENT"
                initial_sufficient_count += 1
            else:
                initial_classification = "INITIAL_INSUFFICIENT"
                challenge_count += 1
                earliest_recovery_round = None
                for round_index in (1, 2, 3):
                    selected = tuple(round_records[round_index]["selected_object_pks"])
                    missing = tuple(sorted(set(required).difference(selected)))
                    if missing:
                        continue
                    mismatch = []
                    evidence_count = 0
                    for object_pk in required:
                        need(object_pk in reference_objects, "required reference object missing: " + object_pk)
                        if object_pk not in payload_cache:
                            payload_cache[object_pk] = inspect_generation_bound_object(
                                object_module,
                                object_pk,
                                reference_objects[object_pk],
                                placement_by_pk,
                                target_by_pk,
                                objects_dir,
                            )
                        evidence = payload_cache[object_pk]
                        evidence_count += 1
                        if not evidence["payload_match"]:
                            mismatch.append(object_pk)
                    if not mismatch and evidence_count == len(required):
                        earliest_recovery_round = round_index
                        break
                if earliest_recovery_round is None:
                    verdict = "NOT_RECOVERED"
                    not_recovered_count += 1
                else:
                    verdict = "RECOVERED"
                    recovered_count += 1

        results.append(
            {
                "query_id": query_id,
                "query_class": query_class,
                "query_text_sha256": query_text_sha256,
                "query_signature": trace_row["query_signature"],
                "query_pk": trace_row["query_pk"],
                "source_generation_pk": SOURCE_GENERATION_PK,
                "round_zero_capsule_sha256": trace_row["round_zero_capsule_sha256"],
                "rounds": round_records,
                "round_zero_selected_pks": list(round_zero_selected),
                "round_zero_missing_required_pks": list(initial_missing),
                "required_object_pks": list(required),
                "initial_sufficiency_classification": initial_classification,
                "earliest_recovery_round": earliest_recovery_round,
                "final_selected_pks": list(final_selected),
                "final_covered_required_pks": list(final_covered),
                "final_missing_required_pks": list(final_missing),
                "payload_mismatch_pks": sorted(payload_mismatch),
                "required_object_payload_evidence": payload_evidence,
                "additional_pks_by_round": [list(row["additional_pks"]) for row in round_records],
                "final_cumulative_route_order": list(round_records[3]["cumulative_route_order"]),
                "verdict": verdict,
            }
        )

    need(len(results) == 40, "result query count mismatch")
    need(tuple(row["query_id"] for row in results) == tuple(row["query_id"] for row in queries), "result query order mismatch")
    need(challenge_count + initial_sufficient_count == 32, "non-fallback denominator mismatch")
    need(control_count == 8, "fallback CONTROL count mismatch")
    need(recovered_count + not_recovered_count == challenge_count, "challenge verdict count mismatch")

    if challenge_count == 0:
        phase_verdict = "NOT_TESTABLE"
    elif not_recovered_count > 0:
        phase_verdict = "FAIL"
    else:
        need(recovered_count == challenge_count, "PASS recovery numerator mismatch")
        phase_verdict = "PASS"

    return (
        results,
        challenge_count,
        initial_sufficient_count,
        recovered_count,
        not_recovered_count,
        control_count,
        phase_verdict,
    )


def build_result(trace_sha256, query_results, challenge_count, initial_sufficient_count, recovered_count, not_recovered_count, control_count, phase_verdict):
    class_counts = {
        "specific_intent": sum(row["query_class"] == "specific_intent" for row in query_results),
        "multi_target_intent": sum(row["query_class"] == "multi_target_intent" for row in query_results),
        "fallback_control": sum(row["query_class"] == "fallback_control" for row in query_results),
    }
    need(class_counts == {"specific_intent": 24, "multi_target_intent": 8, "fallback_control": 8}, "result class counts mismatch")
    return {
        "schema": RESULT_SCHEMA,
        "phase": "6E-B-S1",
        "preregistration_sha256": PREREG_SHA256,
        "runner_implementation_contract_sha256": RUNNER_CONTRACT_SHA256,
        "frozen_failure_incident_sha256": INCIDENT_SHA256,
        "original_phase_6e_b_runner_sha256": ORIGINAL_RUNNER_SHA256,
        "original_phase_6e_b_spent_execution_status": "SPENT_INFRASTRUCTURE_INTEGRITY_FAILURE",
        "original_phase_6e_b_result_state": "ABSENT_PERMANENTLY",
        "phase_6e_a_verdict_sha256": PHASE_6E_A_VERDICT_SHA256,
        "phase_6e_a_result_sha256": PHASE_6E_A_RESULT_SHA256,
        "reference_fixture_sha256": REFERENCE_FIXTURE_SHA256,
        "phase_6e_entry_checkpoint_sha256": PHASE_6E_ENTRY_SHA256,
        "query_scoped_architecture_sha256": ARCHITECTURE_SHA256,
        "capsule_protocol_sha256": CAPSULE_PROTOCOL_SHA256,
        "capsule_implementation_sha256": CAPSULE_IMPL_SHA256,
        "selector_protocol_sha256": SELECTOR_PROTOCOL_SHA256,
        "selector_implementation_sha256": SELECTOR_IMPL_SHA256,
        "query_fixture_sha256": QUERY_FIXTURE_SHA256,
        "catalog_sha256": CATALOG_SHA256,
        "generation_authority_sha256": GENERATION_AUTHORITY_SHA256,
        "maf_object_implementation_sha256": OBJECT_IMPL_SHA256,
        "source_model_pk": SOURCE_MODEL_PK,
        "source_generation_pk": SOURCE_GENERATION_PK,
        "source_manifest_sha256": SOURCE_MANIFEST_SHA256,
        "source_gguf_sha256": SOURCE_GGUF_SHA256,
        "expansion_policy": EXPANSION_POLICY,
        "max_object_budget": MAX_OBJECT_BUDGET,
        "max_expansion_rounds": MAX_EXPANSION_ROUNDS,
        "round_config_sha256": list(ROUND_CONFIG_SHA256),
        "expansion_trace_snapshot_sha256": trace_sha256,
        "class_counts": class_counts,
        "query_count": 40,
        "challenge_count": challenge_count,
        "initial_sufficient_count": initial_sufficient_count,
        "recovered_count": recovered_count,
        "not_recovered_count": not_recovered_count,
        "fallback_control_count": control_count,
        "queries": query_results,
        "phase_verdict": phase_verdict,
        "scientific_boundary": {
            "object_state_payload_identity_only": True,
            "selector_fresh_invocations": True,
            "fixed_round_schedule_completed_before_reference_parse": True,
            "reference_informed_expansion": False,
            "reference_specific_terminal_lf_validation": True,
            "global_canonical_bytes_terminal_lf": False,
            "runner_commit_binding_enforced": True,
            "route_cache_used": False,
            "relationship_expansion_used": False,
            "inference_executed": False,
            "actual_object_avoidance_claimed": False,
            "actual_tensor_avoidance_claimed": False,
            "output_fidelity_claimed": False,
            "answer_quality_claimed": False,
            "performance_claimed": False,
            "maf_native_compute": "disabled_unvalidated",
        },
    }


def write_result(result):
    raw = canonical_bytes(result)
    fd = os.open(OUTPUT_PATH, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    created = True
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        if created and os.path.lexists(OUTPUT_PATH):
            os.unlink(OUTPUT_PATH)
        raise
    return raw


def verify_post_write(expected_raw):
    need(not os.path.lexists(ORIGINAL_OUTPUT_PATH), "original spent Phase 6E-B result path appeared")
    need(OUTPUT_PATH.is_file(), "result artifact missing after write")
    need(OUTPUT_PATH.read_bytes() == expected_raw, "result artifact reread mismatch")
    need(git("diff", "--name-only", "-z") == b"", "tracked mutation after science run")
    need(git("diff", "--cached", "--name-only", "-z") == b"", "index mutation after science run")
    untracked = git("ls-files", "-z", "--others", "--exclude-standard")
    output_b = str(OUTPUT_PATH.relative_to(ROOT)).encode("utf-8")
    items = zparts(untracked)
    need(sum(item == output_b for item in items) == 1, "result untracked identity mismatch")
    baseline = [item for item in items if item != output_b]
    baseline_raw = b"".join(item + b"\0" for item in baseline)
    need(len(baseline) == BASELINE_COUNT, "post-run baseline count mismatch")
    need(sha256_bytes(baseline_raw) == BASELINE_SHA256, "post-run baseline SHA256 mismatch")


def main():
    verify_pre_execution_state()
    selector_module, capsule_module, object_module = import_frozen_modules()
    queries, expected_query_ids, catalog, catalog_pks = load_non_oracle_inputs(selector_module)
    placement_by_pk, target_by_pk, objects_dir = load_generation_authorities_non_oracle()
    configs = build_round_configs(selector_module)

    trace, trace_raw, trace_sha256 = build_complete_trace(
        selector_module,
        capsule_module,
        queries,
        catalog,
        catalog_pks,
        configs,
    )
    need(sha256_bytes(trace_raw) == trace_sha256, "trace snapshot SHA256 instability")

    fixture = load_reference_fixture_after_snapshot(expected_query_ids)

    (
        query_results,
        challenge_count,
        initial_sufficient_count,
        recovered_count,
        not_recovered_count,
        control_count,
        phase_verdict,
    ) = evaluate_after_snapshot(
        object_module,
        queries,
        trace,
        fixture,
        placement_by_pk,
        target_by_pk,
        objects_dir,
    )

    result = build_result(
        trace_sha256,
        query_results,
        challenge_count,
        initial_sufficient_count,
        recovered_count,
        not_recovered_count,
        control_count,
        phase_verdict,
    )

    result_raw = write_result(result)
    verify_post_write(result_raw)

    print("=" * 72)
    print(" OPENMIND / PHASE 6E-B-S1 BOUNDED EXPANSION RECOVERY V1")
    print("=" * 72)
    print("trace_sha256           :", trace_sha256)
    print("challenge_count        :", challenge_count)
    print("initial_sufficient     :", initial_sufficient_count)
    print("recovered_count        :", recovered_count)
    print("not_recovered_count    :", not_recovered_count)
    print("fallback_control_count :", control_count)
    print("phase_verdict          :", phase_verdict)
    print("result_sha256          :", sha256_bytes(result_raw))
    print("result_path            :", OUTPUT_PATH.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Phase6EBS1IntegrityError as exc:
        print("PHASE 6E-B-S1 INFRASTRUCTURE/INTEGRITY FAILURE:", str(exc), file=sys.stderr)
        raise SystemExit(2)
