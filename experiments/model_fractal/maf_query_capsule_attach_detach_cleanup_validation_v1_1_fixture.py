#!/usr/bin/env python3

"""Non-scientific Phase 6D-Q3 fixture qualification V1.1 recovery.

This utility preserves the already-qualified Q3 active-generation authority and
publishes only the missing fixture-authority evidence under the frozen V1.1 correction protocol.

It does not execute the Q3 scientific runner, Q2 V1.4 validation runner,
Query Route Cache, bounded expansion, inference, or answer generation.
"""

from __future__ import annotations

import ctypes
import errno
import hashlib
import json
import os
from pathlib import Path
from typing import Any

import maf_activation_v1_1 as activation
import maf_resident_pk_directory_v1 as resident


ROOT = Path(__file__).resolve().parents[2]

PROTOCOL = ROOT / "experiments/model_fractal/MAF_QUERY_CAPSULE_ATTACH_DETACH_CLEANUP_VALIDATION_V1_PROTOCOL.md"
CORRECTION_PROTOCOL = ROOT / "experiments/model_fractal/MAF_QUERY_CAPSULE_ATTACH_DETACH_CLEANUP_FIXTURE_QUALIFIER_V1_1_CORRECTION_PROTOCOL.md"
FAILED_V1_QUALIFIER = ROOT / "experiments/model_fractal/maf_query_capsule_attach_detach_cleanup_validation_v1_fixture.py"
CATALOG = ROOT / "experiments/model_fractal/maf_query_to_pk_selection_validation_v1_catalog.json"
QUERIES = ROOT / "experiments/model_fractal/maf_query_to_pk_selection_validation_v1_queries.json"
TRACKED_MANIFEST = ROOT / "experiments/model_fractal/maf_query_to_pk_selection_validation_v1_generation_manifest.json"
PHYSICAL_ROOT = ROOT / "results/runtime/maf_query_to_pk_selection_validation_v1_generation"
PHYSICAL_MANIFEST = PHYSICAL_ROOT / "validation_generation.manifest.json"
PHYSICAL_SEGMENT = PHYSICAL_ROOT / "validation_segment.mafseg"

FIXTURE_ROOT = ROOT / "results/runtime/maf_query_capsule_attach_detach_cleanup_validation_v1_fixture"
ACTIVE_RECORD = FIXTURE_ROOT / "active_generation.json"
AUTHORITY = ROOT / "experiments/model_fractal/maf_query_capsule_attach_detach_cleanup_validation_v1_fixture_authority.json"
AUTHORITY_PARTIAL = AUTHORITY.with_name(AUTHORITY.name + ".partial")

MODEL_PK = "mafmodel:v1:d670768d29daf84be95501480a777fd1ee5fddda18f4d0a4c8c3953e1b8cc258"
GENERATION_PK = "mafgen:v1:45a80a2aa271ce04853003185b6a1227cb309bd1e3e2dc538eea849fac9f5db0"
MANIFEST_SHA256 = "28e4baaf07fae450d3c8462ed86fe59c31f0eacdd9e16a8b408994f2a54924c3"
SEGMENT_SHA256 = "aa6ccf99df2b65c19634bbeceb91cfe8db2aeced429e55f8fa6318f1d28ff67d"
SEGMENT_BYTES = 312326668
CATALOG_SHA256 = "c51ef0fabeb10e7c8a091a093aa1934620a69b2026b5a87cb02477b9dd7ca900"
QUERY_FIXTURE_SHA256 = "32f4636bd5e8ceee0dca8342335279a6f8e6acafe866a5469f2c23aa2655202a"
SELECTION_CONFIG_SHA256 = "0caeaeaafdd870e6b02ccc8b4450576883d4ef5234ba689c472e3b14d9dbe120"
PROTOCOL_SHA256 = "323c0d4e0cbd5327382e3762e4d9529fba48f3748699861d96b31920db5b0363"
CORRECTION_PROTOCOL_SHA256 = "f70f20c75f7a1435692537e0a2a6333b7d57ac775be95fc12cf761bd2ff1f15d"
FAILED_V1_QUALIFIER_SHA256 = "d62beb00c44deea17420d191a512050460c5c6460202d96f7d9cd5a048c516c6"
RECOVERY_ACTIVE_RECORD_SHA256 = "ffcf8ada4e2959432e18650a9503bb52175b4366f85ca663d206dea94da3f4e0"
AT_FDCWD = -100
RENAME_NOREPLACE = 1

AUTHORITIES = {
    "architecture": (
        "experiments/model_fractal/MAF_QUERY_SCOPED_WORKING_SET_ARCHITECTURE.md",
        "7df826096e506d13502e442fb11f7e1f18fb2c5a342f4214b91a3c3df043559c",
    ),
    "q1_protocol": (
        "experiments/model_fractal/MAF_QUERY_CAPSULE_DATA_MODEL_V1_PROTOCOL.md",
        "5255a58c8c6340c251e24ae8543760fcd66a8deb8be1a8356ad5b78ad898edda",
    ),
    "q1_implementation": (
        "experiments/model_fractal/maf_query_capsule_data_model_v1.py",
        "f897b97011714f3c84b7350c6bb53e800232be8a5d34e5148a3e50a81952976e",
    ),
    "q1_validation_protocol": (
        "experiments/model_fractal/MAF_QUERY_CAPSULE_DATA_MODEL_VALIDATION_V1_1_PROTOCOL.md",
        "63b40e4ec91410ebea43b85b032a57ed42ba181942390c41fd603a7e5c5cfd3d",
    ),
    "q1_result": (
        "experiments/model_fractal/maf_query_capsule_data_model_validation_v1_1.json",
        "24d1605d1ad95f1b7e7bee190fd0cc978d7b2597d095ac06f68c350208ef1774",
    ),
    "q1_verdict": (
        "experiments/model_fractal/MAF_QUERY_CAPSULE_DATA_MODEL_VALIDATION_V1_1_VERDICT.md",
        "c396346adfc3d7aed08373a52d02e88ce14b2195269c9d090c2572828db77615",
    ),
    "runtime_protocol": (
        "experiments/model_fractal/MAF_OBJECT_RUNTIME_RESIDENCY_V1_PROTOCOL.md",
        "81987d00ef4cb51556dcebf08bff9c9fa8979f033df05304d347b759e545eb13",
    ),
    "runtime_implementation": (
        "experiments/model_fractal/maf_object_runtime_residency_v1.py",
        "4b8c0b8f5db9a67b4bcc368b18f159de6a3f2501f0badf0286de1459125d5cf9",
    ),
    "runtime_validation_protocol": (
        "experiments/model_fractal/MAF_OBJECT_RUNTIME_RESIDENCY_VALIDATION_V1_3_PROTOCOL.md",
        "e12c5dc67d2e147d2c0305c0782cc76ce90a390e7bd276ba0030b3e461fabf17",
    ),
    "runtime_result": (
        "experiments/model_fractal/maf_object_runtime_residency_validation_v1_3.json",
        "1b7fcbe8ca8674928a11b58be950adaaa6a85e1f991636d21a557d160d0c719f",
    ),
    "runtime_verdict": (
        "experiments/model_fractal/MAF_OBJECT_RUNTIME_RESIDENCY_PHASE_6C_VERDICT.md",
        "800fd8e6e58d2af7ea46133e2e6a26d3b380fa4abd371f055324f722ad92784f",
    ),
    "activation": (
        "experiments/model_fractal/maf_activation_v1_1.py",
        "9435ae8dd32656c7350887689d453f3cb8460887068bfaf06e6f68b5b5b927a1",
    ),
    "resident_directory": (
        "experiments/model_fractal/maf_resident_pk_directory_v1.py",
        "4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6",
    ),
    "selection_protocol": (
        "experiments/model_fractal/MAF_QUERY_TO_PK_SELECTION_V1_PROTOCOL.md",
        "b42a0643976c2393871e3b826ba5573b4de981b49603de63230d69cf57be0811",
    ),
    "selector": (
        "experiments/model_fractal/maf_query_to_pk_selection_v1.py",
        "e21c05e352fe921b791e8c936425727a98911ce7566989672a96bfd2b9613fa2",
    ),
    "catalog": (
        "experiments/model_fractal/maf_query_to_pk_selection_validation_v1_catalog.json",
        CATALOG_SHA256,
    ),
    "query_fixture": (
        "experiments/model_fractal/maf_query_to_pk_selection_validation_v1_queries.json",
        QUERY_FIXTURE_SHA256,
    ),
    "q2_validation_protocol": (
        "experiments/model_fractal/MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_4_PROTOCOL.md",
        "a814bca93a6b014ee53aad234b8396c841d0efc2a9363598e8a2192f23745699",
    ),
    "q2_validation_runner": (
        "experiments/model_fractal/maf_query_to_pk_selection_validation_v1_4.py",
        "7bda960c125786fdf3cfca65c4b7b5851ca8bd91257282facfee2fec1ae7a030",
    ),
    "q2_slot": (
        "experiments/model_fractal/maf_query_to_pk_selection_validation_v1_4.slot",
        "0545bba0abcf73e5235d639b0d4390a1e3c01011b1ff0cc9d0372eaf5eb8716a",
    ),
    "q2_result": (
        "experiments/model_fractal/maf_query_to_pk_selection_validation_v1_4.json",
        "b2ad49d7a9a3e1ef565e07e595efc4a4e00b283f422723553c6437ef3a42def6",
    ),
    "q2_verdict": (
        "experiments/model_fractal/MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_4_VERDICT.md",
        "c17198e0013fd9c0a8c59b8f09c05d4f22693dc7d56afdc0f761f55a008c2663",
    ),
}


class FixtureQualificationError(RuntimeError):
    """Fail-closed non-scientific fixture qualification error."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FixtureQualificationError(message)


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def verify_frozen_authorities() -> dict[str, str]:
    observed: dict[str, str] = {}
    require(sha256_file(PROTOCOL) == PROTOCOL_SHA256, "Q3 protocol SHA mismatch")
    require(
        sha256_file(CORRECTION_PROTOCOL) == CORRECTION_PROTOCOL_SHA256,
        "V1.1 correction protocol SHA mismatch",
    )
    require(
        sha256_file(FAILED_V1_QUALIFIER) == FAILED_V1_QUALIFIER_SHA256,
        "failed V1 qualifier SHA mismatch",
    )
    for label, (name, expected) in AUTHORITIES.items():
        path = ROOT / name
        require(path.is_file(), f"missing authority: {label}")
        actual = sha256_file(path)
        require(actual == expected, f"authority SHA mismatch: {label}")
        observed[label] = actual
    return observed


def verify_selection_config() -> None:
    fixture = json.loads(QUERIES.read_text(encoding="utf-8"))
    raw = canonical_json_bytes(fixture["selection_config"])
    require(
        hashlib.sha256(raw).hexdigest() == SELECTION_CONFIG_SHA256,
        "selection config SHA mismatch",
    )


def verify_physical_generation() -> dict[str, Any]:
    require(TRACKED_MANIFEST.is_file(), "tracked generation manifest missing")
    require(PHYSICAL_MANIFEST.is_file(), "physical generation manifest missing")
    require(PHYSICAL_SEGMENT.is_file(), "physical generation segment missing")
    tracked = TRACKED_MANIFEST.read_bytes()
    physical = PHYSICAL_MANIFEST.read_bytes()
    require(tracked == physical, "tracked/physical manifest byte mismatch")
    require(hashlib.sha256(tracked).hexdigest() == MANIFEST_SHA256, "manifest SHA mismatch")
    require(PHYSICAL_SEGMENT.stat().st_size == SEGMENT_BYTES, "segment byte length mismatch")
    require(sha256_file(PHYSICAL_SEGMENT) == SEGMENT_SHA256, "segment SHA mismatch")
    manifest = json.loads(physical.decode("utf-8"))
    require(manifest["generation_pk"] == GENERATION_PK, "generation PK mismatch")
    require(manifest["descriptor"]["model_pk"] == MODEL_PK, "model PK mismatch")
    segments = manifest["descriptor"]["segments"]
    require(len(segments) == 1, "Q3 V1 requires exactly one frozen source segment")
    require(segments[0]["segment_id"] == "segment:00000000", "unexpected segment id")
    require(segments[0]["segment_length"] == SEGMENT_BYTES, "manifest segment length mismatch")
    require(segments[0]["segment_sha256"] == SEGMENT_SHA256, "manifest segment SHA mismatch")
    return manifest


def load_catalog_pks() -> tuple[str, ...]:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    require(catalog["source_generation_pk"] == GENERATION_PK, "catalog generation mismatch")
    require(catalog["source_manifest_sha256"] == MANIFEST_SHA256, "catalog manifest mismatch")
    entries = catalog["entries"]
    pks = tuple(row["object_pk"] for row in entries)
    require(len(pks) == 12, "catalog must contain exactly 12 object PKs")
    require(len(set(pks)) == 12, "catalog object PKs are not unique")
    require(tuple(sorted(pks)) == pks, "catalog object PK order is not canonical")
    return pks


def qualify_preserved_active_authority() -> tuple[dict[str, Any], str]:
    require(ACTIVE_RECORD.is_file(), "preserved recovery active record missing")
    active_sha = sha256_file(ACTIVE_RECORD)
    require(
        active_sha == RECOVERY_ACTIVE_RECORD_SHA256,
        "preserved recovery active record SHA mismatch",
    )
    reopened = activation.reopen_active_generation(ACTIVE_RECORD)
    require(set(reopened) == set(activation.ACTIVE_FIELDS), "active record field set mismatch")
    require(reopened["model_pk"] == MODEL_PK, "active record model mismatch")
    require(reopened["generation_pk"] == GENERATION_PK, "active record generation mismatch")
    require(
        reopened["generation_manifest_sha256"] == MANIFEST_SHA256,
        "active record manifest mismatch",
    )
    return reopened, active_sha


def qualify_resident_directory(expected_pks: tuple[str, ...]) -> tuple[Any, tuple[str, ...]]:
    snapshot = resident.build_snapshot(
        model_pk=MODEL_PK,
        active_record_path=ACTIVE_RECORD,
        active_candidate_manifest_path=PHYSICAL_MANIFEST,
        active_segment_paths={"segment:00000000": PHYSICAL_SEGMENT},
    )
    require(snapshot.model_pk == MODEL_PK, "snapshot model mismatch")
    require(snapshot.generation_pk == GENERATION_PK, "snapshot generation mismatch")
    require(snapshot.generation_manifest_sha256 == MANIFEST_SHA256, "snapshot manifest mismatch")
    require(snapshot.entry_count == 12, "resident snapshot entry count mismatch")
    resolved: list[str] = []
    for object_pk in expected_pks:
        entry = snapshot.lookup(
            model_pk=MODEL_PK,
            pk_kind=resident.OBJECT_PK_KIND,
            logical_pk=object_pk,
            expected_generation_pk=GENERATION_PK,
        )
        require(entry.object_pk == object_pk, "resident lookup object mismatch")
        require(entry.generation_pk == GENERATION_PK, "resident entry generation mismatch")
        require(entry.generation_manifest_sha256 == MANIFEST_SHA256, "resident entry manifest mismatch")
        require(Path(entry.segment_path).resolve() == PHYSICAL_SEGMENT.resolve(), "resident segment path mismatch")
        resolved.append(object_pk)
    require(tuple(resolved) == expected_pks, "resident PK resolution order mismatch")
    return snapshot, tuple(resolved)


def build_fixture_authority(
    upstream: dict[str, str],
    active_record: dict[str, Any],
    active_record_sha256: str,
    snapshot: Any,
    resolved_pks: tuple[str, ...],
) -> dict[str, Any]:
    return {
        "schema": "openmind.maf_query_capsule_attach_detach_cleanup_validation_v1_fixture_authority.v1",
        "authority_version": "maf_query_capsule_attach_detach_cleanup_validation_v1_fixture_authority_v1",
        "phase": "6D-Q3",
        "scientific": False,
        "protocol_sha256": PROTOCOL_SHA256,
        "fixture_qualifier_correction_protocol_sha256": CORRECTION_PROTOCOL_SHA256,
        "fixture_qualifier_sha256": sha256_file(Path(__file__).resolve()),
        "failed_fixture_qualifier_sha256": FAILED_V1_QUALIFIER_SHA256,
        "recovery_active_record_sha256": RECOVERY_ACTIVE_RECORD_SHA256,
        "model_pk": MODEL_PK,
        "generation_pk": GENERATION_PK,
        "generation_manifest_sha256": MANIFEST_SHA256,
        "physical_segment_sha256": SEGMENT_SHA256,
        "physical_segment_bytes": SEGMENT_BYTES,
        "catalog_sha256": CATALOG_SHA256,
        "query_fixture_sha256": QUERY_FIXTURE_SHA256,
        "selection_config_sha256": SELECTION_CONFIG_SHA256,
        "active_record_path": relative(ACTIVE_RECORD),
        "active_record_sha256": active_record_sha256,
        "active_record": active_record,
        "resident_snapshot_active_record_sha256": snapshot.active_record_sha256,
        "resident_entry_count": snapshot.entry_count,
        "resolved_object_pks": list(resolved_pks),
        "upstream_authority_sha256": upstream,
        "boundary": {
            "fixture_qualification_only": True,
            "q3_science_executed": False,
            "q2_validation_runner_invoked": False,
            "route_cache_used": False,
            "bounded_expansion_used": False,
            "inference_executed": False,
            "answer_generation_executed": False,
            "phase_6e_entered": False,
        },
    }


def rename_noreplace(source: Path, target: Path) -> None:
    libc = ctypes.CDLL(None, use_errno=True)
    renameat2 = libc.renameat2
    renameat2.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    ]
    renameat2.restype = ctypes.c_int
    ctypes.set_errno(0)
    rc = renameat2(
        AT_FDCWD,
        os.fsencode(source),
        AT_FDCWD,
        os.fsencode(target),
        RENAME_NOREPLACE,
    )
    if rc == 0:
        return
    error_number = ctypes.get_errno()
    if error_number == errno.EEXIST:
        raise FixtureQualificationError("fixture authority final path already exists")
    raise OSError(error_number, os.strerror(error_number), str(target))


def publish_authority(value: dict[str, Any]) -> tuple[str, bool]:
    raw = canonical_json_bytes(value)
    require(not AUTHORITY.exists(), "fixture authority final path already exists")
    require(not AUTHORITY_PARTIAL.exists(), "fixture authority partial already exists")
    AUTHORITY.parent.mkdir(parents=True, exist_ok=True)
    with AUTHORITY_PARTIAL.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    try:
        rename_noreplace(AUTHORITY_PARTIAL, AUTHORITY)
        directory_fd = os.open(str(AUTHORITY.parent), os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except Exception:
        if AUTHORITY_PARTIAL.exists():
            AUTHORITY_PARTIAL.unlink()
        raise
    require(not AUTHORITY_PARTIAL.exists(), "fixture authority partial remains after publication")
    require(AUTHORITY.read_bytes() == raw, "published fixture authority byte mismatch")
    return hashlib.sha256(raw).hexdigest(), True


def main() -> int:
    upstream = verify_frozen_authorities()
    verify_selection_config()
    verify_physical_generation()
    expected_pks = load_catalog_pks()
    require(not AUTHORITY.exists(), "fixture authority final path already exists")
    require(not AUTHORITY_PARTIAL.exists(), "fixture authority partial already exists")
    active_record, active_sha = qualify_preserved_active_authority()
    snapshot, resolved = qualify_resident_directory(expected_pks)
    authority = build_fixture_authority(
        upstream,
        active_record,
        active_sha,
        snapshot,
        resolved,
    )
    authority_sha, authority_created = publish_authority(authority)
    print("MODE=qualify-q3-fixture")
    print(f"ACTIVE_RECORD_PATH={relative(ACTIVE_RECORD)}")
    print(f"ACTIVE_RECORD_SHA256={active_sha}")
    print("ACTIVE_RECORD_PRESERVED=True")
    print(f"RECOVERY_ACTIVE_RECORD_SHA256={active_sha}")
    print(f"FIXTURE_AUTHORITY_PATH={relative(AUTHORITY)}")
    print(f"FIXTURE_AUTHORITY_SHA256={authority_sha}")
    print(f"FIXTURE_AUTHORITY_CREATED={authority_created}")
    print(f"RESIDENT_ENTRY_COUNT={snapshot.entry_count}")
    print(f"RESOLVED_OBJECT_PK_COUNT={len(resolved)}")
    print("Q3_SCIENCE_EXECUTED=False")
    print("Q2_VALIDATION_RUNNER_INVOKED=False")
    print("ROUTE_CACHE_USED=False")
    print("PHASE_6E_ENTERED=False")
    print("ALL_PASS=True")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
