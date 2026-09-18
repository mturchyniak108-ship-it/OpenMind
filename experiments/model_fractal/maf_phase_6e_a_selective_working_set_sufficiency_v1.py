#!/usr/bin/env python3

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

BRANCH = "labs/multidimensional-maf"

PROTOCOL_PATH = Path("experiments/model_fractal/MAF_PHASE_6E_A_SELECTIVE_WORKING_SET_SUFFICIENCY_PROTOCOL_V1.md")
PROTOCOL_SHA256 = "0ecf4936969f890b3d9f9c398541246642ac46f2edf975c32c121e8f4189ee1d"

REFERENCE_FIXTURE_PATH = Path("experiments/model_fractal/maf_phase_6e_a_reference_state_fixture_v1.json")
REFERENCE_FIXTURE_SHA256 = "870b656e0c3181ec8f7be1537bdeafde10fffd1b947f5372d21cdee4c00a83a0"

QUERY_FIXTURE_PATH = Path("experiments/model_fractal/maf_query_to_pk_selection_validation_v1_queries.json")
QUERY_FIXTURE_SHA256 = "32f4636bd5e8ceee0dca8342335279a6f8e6acafe866a5469f2c23aa2655202a"

CATALOG_PATH = Path("experiments/model_fractal/maf_query_to_pk_selection_validation_v1_catalog.json")
CATALOG_SHA256 = "c51ef0fabeb10e7c8a091a093aa1934620a69b2026b5a87cb02477b9dd7ca900"

GENERATION_AUTHORITY_PATH = Path("experiments/model_fractal/maf_query_to_pk_selection_validation_v1_generation_construction_authority.json")
GENERATION_AUTHORITY_SHA256 = "a5e953ae2ab2dd11a9f6dc564ae5ee57cb064d6eea0a8a5517191b4a6efc1a6d"

SELECTOR_PATH = Path("experiments/model_fractal/maf_query_to_pk_selection_v1.py")
SELECTOR_SHA256 = "e21c05e352fe921b791e8c936425727a98911ce7566989672a96bfd2b9613fa2"

OBJECT_MODULE_PATH = Path("experiments/model_fractal/maf_object_v1.py")
OBJECT_MODULE_SHA256 = "eed6cbd96995412a632883f3c534f9023e7711ea8eb437afe35a48312502f63b"

GENERATION_MANIFEST_PATH = Path("results/runtime/maf_query_to_pk_selection_validation_v1_generation/validation_generation.manifest.json")
GENERATION_MANIFEST_SHA256 = "28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3"

OUTPUT_PATH = Path("experiments/model_fractal/maf_phase_6e_a_selective_working_set_sufficiency_v1.json")

SOURCE_MODEL_PK = "mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258"
SOURCE_GENERATION_PK = "mafgen:v1:45a80a2aa271ce04853003185b6a1227cb309bd1e3e2dc538eea849fac9f5db0"
SOURCE_MANIFEST_SHA256 = GENERATION_MANIFEST_SHA256
SOURCE_GGUF_SHA256 = "507de59046601282ba768a9789900e6ccf60ed93ddf346730b7c68eb0715bc47"
SELECTION_CONFIG_SHA256 = "0caeaeaafdd870e6b02ccc8b4450576883d4ef5234ba689c472e3b14d9dbe120"
MAX_CANDIDATES = 4

BASELINE_COUNT = 440
BASELINE_SHA256 = "f206c0eed32daef9ed0cfaae195aa56a343a85437ebd3135aeafdb4c1ffacddd"

RESULT_SCHEMA = "openmind.maf_phase_6e_a_selective_working_set_sufficiency.v1"
SELECTION_SNAPSHOT_SCHEMA = "openmind.maf_phase_6e_a_selection_snapshot.v1"

EXPECTED_QUERY_IDS = tuple("q{:03d}".format(index) for index in range(1, 41))
EXPECTED_CLASS_COUNTS = {
    "specific_intent": 24,
    "multi_target_intent": 8,
    "fallback_control": 8,
}


class Phase6EAError(RuntimeError):
    pass


def need(condition, message):
    if not condition:
        raise Phase6EAError(message)


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path, chunk_bytes=1024 * 1024):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        while True:
            chunk = handle.read(chunk_bytes)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def canonical_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8") + b"\n"


def git(*args):
    result = subprocess.run(
        ("git",) + tuple(args),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise Phase6EAError("git command failed: " + " ".join(args))
    return result.stdout


def zparts(raw):
    return [item for item in raw.split(b"\0") if item]


def verify_repository_preflight():
    branch = git("branch", "--show-current").decode("utf-8").strip()
    need(branch == BRANCH, "unexpected branch")
    need(git("diff", "--name-only", "-z") == b"", "tracked worktree is dirty")
    need(git("diff", "--cached", "--name-only", "-z") == b"", "index is not empty")
    untracked = git("ls-files", "-z", "--others", "--exclude-standard")
    need(len(zparts(untracked)) == BASELINE_COUNT, "untracked baseline count mismatch")
    need(sha256_bytes(untracked) == BASELINE_SHA256, "untracked baseline SHA256 mismatch")
    need(not os.path.lexists(OUTPUT_PATH), "result artifact already exists")


def verify_static_authorities():
    checks = (
        (PROTOCOL_PATH, PROTOCOL_SHA256),
        (QUERY_FIXTURE_PATH, QUERY_FIXTURE_SHA256),
        (CATALOG_PATH, CATALOG_SHA256),
        (GENERATION_AUTHORITY_PATH, GENERATION_AUTHORITY_SHA256),
        (SELECTOR_PATH, SELECTOR_SHA256),
        (OBJECT_MODULE_PATH, OBJECT_MODULE_SHA256),
    )
    for path, expected in checks:
        need(path.is_file(), "missing frozen authority: " + str(path))
        need(sha256_file(path) == expected, "frozen authority SHA256 mismatch: " + str(path))
    need(REFERENCE_FIXTURE_PATH.is_file(), "missing frozen reference fixture")
    need(
        sha256_file(REFERENCE_FIXTURE_PATH) == REFERENCE_FIXTURE_SHA256,
        "reference fixture SHA256 mismatch",
    )
    need(GENERATION_MANIFEST_PATH.is_file(), "missing frozen generation manifest")
    need(
        sha256_file(GENERATION_MANIFEST_PATH) == GENERATION_MANIFEST_SHA256,
        "generation manifest SHA256 mismatch",
    )


def load_module_exact(module_name, path, expected_sha256):
    need(sha256_file(path) == expected_sha256, "module identity changed: " + str(path))
    spec = importlib.util.spec_from_file_location(module_name, path)
    need(spec is not None and spec.loader is not None, "module spec failure: " + module_name)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def load_q2_inputs():
    queries_raw = QUERY_FIXTURE_PATH.read_bytes()
    catalog_raw = CATALOG_PATH.read_bytes()
    need(sha256_bytes(queries_raw) == QUERY_FIXTURE_SHA256, "query fixture changed")
    need(sha256_bytes(catalog_raw) == CATALOG_SHA256, "catalog changed")
    queries_doc = json.loads(queries_raw.decode("utf-8"))
    catalog_doc = json.loads(catalog_raw.decode("utf-8"))
    need(queries_doc.get("source_generation_pk") == SOURCE_GENERATION_PK, "query fixture generation mismatch")
    need(queries_doc.get("source_manifest_sha256") == SOURCE_MANIFEST_SHA256, "query fixture manifest mismatch")
    need(queries_doc.get("catalog_sha256") == CATALOG_SHA256, "query fixture catalog mismatch")
    need(catalog_doc.get("source_generation_pk") == SOURCE_GENERATION_PK, "catalog generation mismatch")
    need(catalog_doc.get("source_manifest_sha256") == SOURCE_MANIFEST_SHA256, "catalog manifest mismatch")
    queries = queries_doc["queries"]
    need(len(queries) == 40, "query count mismatch")
    need(tuple(row["query_id"] for row in queries) == EXPECTED_QUERY_IDS, "query order mismatch")
    counts = {
        key: sum(row["query_class"] == key for row in queries)
        for key in EXPECTED_CLASS_COUNTS
    }
    need(counts == EXPECTED_CLASS_COUNTS, "query class count mismatch")
    return queries, catalog_doc


def execute_all_q2_selections(selector_module, queries, catalog_doc):
    catalog = selector_module.MAFQueryPKCatalogV1.from_mapping(catalog_doc)
    catalog.require_source_binding(
        source_generation_pk=SOURCE_GENERATION_PK,
        source_manifest_sha256=SOURCE_MANIFEST_SHA256,
    )
    config = selector_module.default_selection_config_v1(max_candidates=MAX_CANDIDATES)
    need(
        config.selection_config_sha256 == SELECTION_CONFIG_SHA256,
        "selection configuration SHA256 mismatch",
    )
    snapshot_queries = []
    selection_results = {}
    for row in queries:
        result = selector_module.select_query_to_pks_v1(
            query=row["query_text"],
            catalog=catalog,
            config=config,
            source_generation_pk=SOURCE_GENERATION_PK,
            source_manifest_sha256=SOURCE_MANIFEST_SHA256,
        )
        need(
            result.selection_config_sha256 == SELECTION_CONFIG_SHA256,
            "selection result configuration mismatch",
        )
        need(
            result.source_generation_pk == SOURCE_GENERATION_PK,
            "selection result generation mismatch",
        )
        need(
            result.source_manifest_sha256 == SOURCE_MANIFEST_SHA256,
            "selection result manifest mismatch",
        )
        raw_selected = tuple(result.selected_object_pks)
        need(len(raw_selected) == len(set(raw_selected)), "duplicate selected object PK")
        selected = tuple(sorted(raw_selected))
        need(len(selected) <= MAX_CANDIDATES, "selected object PK budget exceeded")
        snapshot_queries.append(
            {
                "query_id": row["query_id"],
                "selected_object_pks": list(selected),
            }
        )
        selection_results[row["query_id"]] = {
            "query_signature": result.query_signature,
            "fallback_used": bool(result.fallback_used),
            "selected_object_pks": selected,
        }
    need(tuple(row["query_id"] for row in snapshot_queries) == EXPECTED_QUERY_IDS, "selection snapshot order mismatch")
    snapshot = {
        "schema": SELECTION_SNAPSHOT_SCHEMA,
        "source_generation_pk": SOURCE_GENERATION_PK,
        "source_manifest_sha256": SOURCE_MANIFEST_SHA256,
        "selection_config_sha256": SELECTION_CONFIG_SHA256,
        "queries": snapshot_queries,
    }
    snapshot_raw = canonical_bytes(snapshot)
    return snapshot, snapshot_raw, sha256_bytes(snapshot_raw), selection_results


def load_reference_fixture_after_snapshot():
    raw = REFERENCE_FIXTURE_PATH.read_bytes()
    need(sha256_bytes(raw) == REFERENCE_FIXTURE_SHA256, "reference fixture changed after selection")
    fixture = json.loads(raw.decode("utf-8"))
    need(canonical_bytes(fixture) == raw, "reference fixture is not canonical JSON")
    need(fixture["source_model_pk"] == SOURCE_MODEL_PK, "reference model PK mismatch")
    need(fixture["source_generation_pk"] == SOURCE_GENERATION_PK, "reference generation PK mismatch")
    need(fixture["source_manifest_sha256"] == SOURCE_MANIFEST_SHA256, "reference manifest mismatch")
    need(fixture["source_gguf_sha256"] == SOURCE_GGUF_SHA256, "reference GGUF mismatch")
    need(len(fixture["queries"]) == 40, "reference query count mismatch")
    need(tuple(row["query_id"] for row in fixture["queries"]) == EXPECTED_QUERY_IDS, "reference query order mismatch")
    return fixture


def load_generation_binding_after_snapshot():
    authority_raw = GENERATION_AUTHORITY_PATH.read_bytes()
    need(sha256_bytes(authority_raw) == GENERATION_AUTHORITY_SHA256, "generation authority changed")
    authority = json.loads(authority_raw.decode("utf-8"))
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
    objects_dir = Path(authority["output_layout"]["objects_dir"])
    return placement_by_pk, target_by_pk, objects_dir


def inspect_generation_bound_object(object_module, object_pk, reference_object, placement_by_pk, target_by_pk, objects_dir):
    need(object_pk in placement_by_pk, "selected required PK missing from generation descriptor: " + object_pk)
    need(object_pk in target_by_pk, "selected required PK missing from generation authority: " + object_pk)
    placement = placement_by_pk[object_pk]
    target = target_by_pk[object_pk]
    object_path = objects_dir / target["object_filename"]
    need(object_path.is_file(), "dedicated MAF object file missing: " + str(object_path))
    disk_object_sha256 = sha256_file(object_path)
    need(
        disk_object_sha256 == placement["object_file_sha256"],
        "generation-bound serialized object SHA256 mismatch: " + object_pk,
    )
    need(
        placement["payload_sha256"] == reference_object["payload_sha256"],
        "generation manifest payload identity differs from frozen reference: " + object_pk,
    )
    view = object_module.inspect_object(object_path)
    need(view.tensor_name == reference_object["tensor_name"], "object tensor name mismatch: " + object_pk)
    need(view.tensor_type == reference_object["tensor_type"], "object tensor type mismatch: " + object_pk)
    need(list(view.dims) == reference_object["dims"], "object dims mismatch: " + object_pk)
    need(view.element_count == reference_object["element_count"], "object element count mismatch: " + object_pk)
    observed = view.payload_sha256
    reference = reference_object["payload_sha256"]
    return {
        "object_pk": object_pk,
        "reference_payload_sha256": reference,
        "observed_payload_sha256": observed,
        "payload_match": observed == reference,
    }


def evaluate_after_snapshot(object_module, queries, selection_results, fixture, placement_by_pk, target_by_pk, objects_dir):
    reference_queries = {row["query_id"]: row for row in fixture["queries"]}
    reference_objects = {row["object_pk"]: row for row in fixture["objects"]}
    need(len(reference_queries) == 40, "duplicate reference query IDs")
    need(len(reference_objects) == 12, "duplicate reference object PKs")
    results = []
    payload_cache = {}
    evaluable_pass = 0
    evaluable_fail = 0
    control_count = 0
    for source_row in queries:
        query_id = source_row["query_id"]
        query_class = source_row["query_class"]
        reference_query = reference_queries[query_id]
        query_text_sha256 = sha256_bytes(source_row["query_text"].encode("utf-8"))
        need(
            query_text_sha256 == reference_query["query_text_sha256"],
            "query text identity mismatch: " + query_id,
        )
        selected = tuple(selection_results[query_id]["selected_object_pks"])
        required = tuple(reference_query["required_object_pks"])
        need(required == tuple(sorted(required)), "reference required PK ordering mismatch")
        selected_set = set(selected)
        required_set = set(required)
        covered = tuple(sorted(required_set.intersection(selected_set)))
        missing = tuple(sorted(required_set.difference(selected_set)))
        extra = tuple(sorted(selected_set.difference(required_set)))
        payload_evidence = []
        payload_mismatch = []
        for object_pk in covered:
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
            need(len(required) == 0, "fallback control required set is not empty")
            verdict = "CONTROL"
            control_count += 1
        else:
            need(query_class in {"specific_intent", "multi_target_intent"}, "unexpected query class")
            complete = (
                not missing
                and not payload_mismatch
                and len(payload_evidence) == len(required)
                and tuple(item["object_pk"] for item in payload_evidence) == required
            )
            verdict = "PASS" if complete else "FAIL"
            if verdict == "PASS":
                evaluable_pass += 1
            else:
                evaluable_fail += 1
        results.append(
            {
                "query_id": query_id,
                "query_class": query_class,
                "query_text_sha256": query_text_sha256,
                "source_generation_pk": SOURCE_GENERATION_PK,
                "selection_config_sha256": SELECTION_CONFIG_SHA256,
                "query_signature": selection_results[query_id]["query_signature"],
                "fallback_used": selection_results[query_id]["fallback_used"],
                "selected_object_pks": list(selected),
                "selected_count": len(selected),
                "required_object_pks": list(required),
                "required_count": len(required),
                "covered_required_pks": list(covered),
                "missing_required_pks": list(missing),
                "payload_mismatch_pks": sorted(payload_mismatch),
                "extra_selected_pks": list(extra),
                "payload_evidence": payload_evidence,
                "expansion_rounds": 0,
                "verdict": verdict,
            }
        )
    need(len(results) == 40, "result query count mismatch")
    need(tuple(row["query_id"] for row in results) == EXPECTED_QUERY_IDS, "result query order mismatch")
    need(evaluable_pass + evaluable_fail == 32, "evaluable denominator mismatch")
    need(control_count == 8, "fallback CONTROL count mismatch")
    phase_verdict = "PASS" if evaluable_pass == 32 and evaluable_fail == 0 else "FAIL"
    return results, evaluable_pass, evaluable_fail, control_count, phase_verdict


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
    need(OUTPUT_PATH.is_file(), "result artifact missing after write")
    need(OUTPUT_PATH.read_bytes() == expected_raw, "result artifact reread mismatch")
    need(git("diff", "--name-only", "-z") == b"", "tracked mutation after science run")
    need(git("diff", "--cached", "--name-only", "-z") == b"", "index mutation after science run")
    untracked = git("ls-files", "-z", "--others", "--exclude-standard")
    output_b = str(OUTPUT_PATH).encode("utf-8")
    items = zparts(untracked)
    need(sum(item == output_b for item in items) == 1, "result untracked identity mismatch")
    baseline = [item for item in items if item != output_b]
    baseline_raw = b"".join(item + b"\0" for item in baseline)
    need(len(baseline) == BASELINE_COUNT, "post-run baseline count mismatch")
    need(sha256_bytes(baseline_raw) == BASELINE_SHA256, "post-run baseline SHA256 mismatch")


def rollback_result_verified():
    if os.path.lexists(OUTPUT_PATH):
        os.unlink(OUTPUT_PATH)
    dirty = git("diff", "--name-only", "-z")
    staged = git("diff", "--cached", "--name-only", "-z")
    untracked = git("ls-files", "-z", "--others", "--exclude-standard")
    return all(
        (
            not os.path.lexists(OUTPUT_PATH),
            dirty == b"",
            staged == b"",
            len(zparts(untracked)) == BASELINE_COUNT,
            sha256_bytes(untracked) == BASELINE_SHA256,
        )
    )


def main():
    created = False
    try:
        verify_repository_preflight()
        verify_static_authorities()

        selector_module = load_module_exact(
            "openmind_phase6ea_selector",
            SELECTOR_PATH,
            SELECTOR_SHA256,
        )
        object_module = load_module_exact(
            "openmind_phase6ea_object",
            OBJECT_MODULE_PATH,
            OBJECT_MODULE_SHA256,
        )

        queries, catalog_doc = load_q2_inputs()

        (
            selection_snapshot,
            selection_snapshot_raw,
            selection_snapshot_sha256,
            selection_results,
        ) = execute_all_q2_selections(
            selector_module,
            queries,
            catalog_doc,
        )

        reference_fixture = load_reference_fixture_after_snapshot()

        (
            placement_by_pk,
            target_by_pk,
            objects_dir,
        ) = load_generation_binding_after_snapshot()

        (
            query_results,
            evaluable_pass,
            evaluable_fail,
            control_count,
            phase_verdict,
        ) = evaluate_after_snapshot(
            object_module,
            queries,
            selection_results,
            reference_fixture,
            placement_by_pk,
            target_by_pk,
            objects_dir,
        )

        result = {
            "schema": RESULT_SCHEMA,
            "protocol_sha256": PROTOCOL_SHA256,
            "reference_fixture_sha256": REFERENCE_FIXTURE_SHA256,
            "query_fixture_sha256": QUERY_FIXTURE_SHA256,
            "catalog_sha256": CATALOG_SHA256,
            "generation_authority_sha256": GENERATION_AUTHORITY_SHA256,
            "generation_manifest_sha256": GENERATION_MANIFEST_SHA256,
            "source_model_pk": SOURCE_MODEL_PK,
            "source_generation_pk": SOURCE_GENERATION_PK,
            "source_manifest_sha256": SOURCE_MANIFEST_SHA256,
            "source_gguf_sha256": SOURCE_GGUF_SHA256,
            "q2_selector_sha256": SELECTOR_SHA256,
            "q2_selection_config_sha256": SELECTION_CONFIG_SHA256,
            "selection_snapshot_sha256": selection_snapshot_sha256,
            "selection_snapshot": selection_snapshot,
            "class_counts": dict(EXPECTED_CLASS_COUNTS),
            "evaluable_query_count": 32,
            "fallback_control_count": 8,
            "evaluable_pass_count": evaluable_pass,
            "evaluable_fail_count": evaluable_fail,
            "fallback_control_verdict_count": control_count,
            "phase_verdict": phase_verdict,
            "queries": query_results,
            "scientific_boundary": {
                "bounded_expansion": False,
                "inference": False,
                "maf_native_compute": False,
                "avoidance_claim": False,
                "fidelity_claim": False,
                "performance_claim": False,
            },
        }

        result_raw = write_result(result)
        created = True
        verify_post_write(result_raw)

        print("🟨🟨🟨 OPENMIND / GOLD STANDARD V2 🟨🟨🟨")
        print("PHASE 6E-A — AUTHORITATIVE SELECTIVE WORKING-SET SUFFICIENCY")
        print()
        print("[ SELECTION SNAPSHOT ]")
        print("  query count                     : 40")
        print("  selection config SHA256         : " + SELECTION_CONFIG_SHA256)
        print("  selection snapshot SHA256       : " + selection_snapshot_sha256)
        print()
        print("[ RESULT ]")
        print("  evaluable queries               : 32")
        print("  evaluable PASS                  : " + str(evaluable_pass))
        print("  evaluable FAIL                  : " + str(evaluable_fail))
        print("  fallback CONTROL                : " + str(control_count))
        print("  Phase 6E-A verdict              : " + phase_verdict)
        print("  result bytes                    : " + str(len(result_raw)))
        print("  result SHA256                   : " + sha256_bytes(result_raw))
        print()
        print("[ SCIENTIFIC BOUNDARY ]")
        print("  bounded expansion               : NO")
        print("  inference                       : NO")
        print("  MAF-native compute              : NO")
        print("  avoidance claim                 : NO")
        print("  fidelity claim                  : NO")
        print("  performance claim               : NO")
        print("  network access                  : NO")
        print("  Git staging                     : NO")
        print()
        print("🟨🟨🟨 PASTE BACK TO CHAT FROM HERE 🟨🟨🟨")
        return 0

    except Exception as exc:
        rollback_ok = True
        if created or os.path.lexists(OUTPUT_PATH):
            try:
                rollback_ok = rollback_result_verified()
            except Exception:
                rollback_ok = False
        print("🟨🟨🟨 OPENMIND / GOLD STANDARD V2 🟨🟨🟨")
        print("PHASE 6E-A — AUTHORITATIVE SELECTIVE WORKING-SET SUFFICIENCY")
        print()
        print("[ FAILURE ]")
        print("  error                           : " + type(exc).__name__ + ": " + str(exc))
        print("  rollback verified               : " + ("PASS" if rollback_ok else "FAIL"))
        print("  Phase 6E-A result               : NOT VALID")
        print()
        print("🟨🟨🟨 PASTE BACK TO CHAT FROM HERE 🟨🟨🟨")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
