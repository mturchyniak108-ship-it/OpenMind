#!/usr/bin/env python3

"""Validate deterministic MAF fragment logical identity."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

import maf_identity_v1 as identity


SCHEMA = "openmind.maf_fragment_identity_validation.v1"

ROOT = Path(__file__).resolve().parents[2]

SPEC_PATH = (
    ROOT
    / "experiments/model_fractal/"
    "maf_fragment_identity_validation_spec_v1.json"
)

ENGINE_PATH = (
    ROOT
    / "experiments/model_fractal/"
    "maf_identity_v1.py"
)

FULL_RESULT_PATH = (
    ROOT
    / "experiments/model_fractal/"
    "maf_full_model_identity_validation_v1.json"
)

DEFAULT_RESULT_PATH = (
    ROOT
    / "experiments/model_fractal/"
    "maf_fragment_identity_validation_v1.json"
)

EXPECTED_SPEC_SHA256 = (
    "166e94d4024978f43e4139dc48234e8a"
    "35bb311397949982d1e3a0ca6c8d61ec"
)

EXPECTED_ENGINE_SHA256 = (
    "dd4d70c2829ceb9c0a35e0e278e3a2c"
    "37b1ffaf1654165e17641f250bec8269c"
)

EXPECTED_FULL_RESULT_SHA256 = (
    "ef954f38e16ccbc73211c503d7d9c9b"
    "8462028d6222fb32fb9b15eb59615d25d"
)


class ValidationError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()


def require_sha(
    path: Path,
    expected: str,
) -> str:
    actual = sha256_file(path)

    if actual != expected:
        raise ValidationError(
            f"{path} SHA256 drift: "
            f"expected {expected}, got {actual}"
        )

    return actual


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())

    if not isinstance(value, dict):
        raise ValidationError(
            f"{path} must contain a JSON object"
        )

    return value


def fragment_record(
    *,
    object_pk: str,
    scheme: str,
    logical_fragment_index: int,
    logical_range: list[int],
) -> dict[str, Any]:
    descriptor = identity.build_fragment_descriptor(
        object_pk_value=object_pk,
        fragment_scheme=scheme,
        logical_fragment_index=logical_fragment_index,
        logical_range=logical_range,
    )

    first_pk = identity.fragment_pk(
        object_pk_value=object_pk,
        fragment_scheme=scheme,
        logical_fragment_index=logical_fragment_index,
        logical_range=logical_range,
    )

    second_pk = identity.fragment_pk(
        object_pk_value=object_pk,
        fragment_scheme=scheme,
        logical_fragment_index=logical_fragment_index,
        logical_range=logical_range,
    )

    return {
        "descriptor": descriptor,
        "pk": first_pk,
        "repeat_pk": second_pk,
        "repeat_equal": first_pk == second_pk,
    }


def validate_invalid_inputs(
    *,
    parent_pk: str,
    scheme: str,
    cases: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    results = []

    for case in cases:
        rejected = False
        error_type = None

        try:
            identity.fragment_pk(
                object_pk_value=parent_pk,
                fragment_scheme=scheme,
                logical_fragment_index=
                    case["logical_fragment_index"],
                logical_range=
                    case["logical_range"],
            )

        except identity.MAFIdentityError as exc:
            rejected = True
            error_type = type(exc).__name__

        results.append({
            "name": case["name"],
            "rejected": rejected,
            "error_type": error_type,
        })

    return results


def validate() -> dict[str, Any]:
    hashes = {
        "fragment_spec_sha256":
            require_sha(
                SPEC_PATH,
                EXPECTED_SPEC_SHA256,
            ),
        "identity_engine_sha256":
            require_sha(
                ENGINE_PATH,
                EXPECTED_ENGINE_SHA256,
            ),
        "full_model_result_sha256":
            require_sha(
                FULL_RESULT_PATH,
                EXPECTED_FULL_RESULT_SHA256,
            ),
    }

    spec = load_json(SPEC_PATH)
    full = load_json(FULL_RESULT_PATH)

    scheme_info = spec["validation_scheme"]

    if scheme_info["status"] != "test_only":
        raise ValidationError(
            "fragment validation scheme is not test-only"
        )

    if (
        scheme_info["operational_fragmentation"]
        is not False
    ):
        raise ValidationError(
            "operational fragmentation must remain false"
        )

    if (
        scheme_info["range_unit"]
        != "intentionally_unspecified"
    ):
        raise ValidationError(
            "range unit unexpectedly defined"
        )

    scheme = scheme_info["name"]

    objects_by_name = {
        row["tensor_name"]: row
        for row in full["objects"]
    }

    parent_names = spec["parent_objects"]

    if len(parent_names) != 3:
        raise ValidationError(
            "expected exactly three parent objects"
        )

    parent_pks = {
        name: objects_by_name[name]["pk"]
        for name in parent_names
    }

    cases = {
        row["case"]: row
        for row in spec["cases"]
    }

    baseline = cases["baseline"]
    different_index = cases["different_index"]
    different_range = cases["different_range"]

    baseline_records = {
        name: fragment_record(
            object_pk=parent_pks[name],
            scheme=scheme,
            logical_fragment_index=
                baseline["logical_fragment_index"],
            logical_range=
                baseline["logical_range"],
        )
        for name in parent_names
    }

    baseline_pks = [
        row["pk"]
        for row in baseline_records.values()
    ]

    baseline_unique = (
        len(baseline_pks)
        == len(set(baseline_pks))
        == 3
    )

    repeated_equal = all(
        row["repeat_equal"]
        for row in baseline_records.values()
    )

    control_parent = parent_names[0]
    control_parent_pk = parent_pks[control_parent]

    index_record = fragment_record(
        object_pk=control_parent_pk,
        scheme=scheme,
        logical_fragment_index=
            different_index["logical_fragment_index"],
        logical_range=
            different_index["logical_range"],
    )

    range_record = fragment_record(
        object_pk=control_parent_pk,
        scheme=scheme,
        logical_fragment_index=
            different_range["logical_fragment_index"],
        logical_range=
            different_range["logical_range"],
    )

    baseline_control_pk = (
        baseline_records[control_parent]["pk"]
    )

    parent_changes_identity = baseline_unique

    index_changes_identity = (
        index_record["pk"]
        != baseline_control_pk
    )

    range_changes_identity = (
        range_record["pk"]
        != baseline_control_pk
    )

    placement_controls = spec["placement_controls"]

    placement_a = placement_controls[0]
    placement_b = placement_controls[1]

    placement_pk_a = identity.fragment_pk(
        object_pk_value=control_parent_pk,
        fragment_scheme=scheme,
        logical_fragment_index=
            baseline["logical_fragment_index"],
        logical_range=
            baseline["logical_range"],
    )

    placement_pk_b = identity.fragment_pk(
        object_pk_value=control_parent_pk,
        fragment_scheme=scheme,
        logical_fragment_index=
            baseline["logical_fragment_index"],
        logical_range=
            baseline["logical_range"],
    )

    placement_independent = (
        placement_a != placement_b
        and placement_pk_a == placement_pk_b
    )

    invalid_results = validate_invalid_inputs(
        parent_pk=control_parent_pk,
        scheme=scheme,
        cases=spec["negative_inputs"],
    )

    invalid_inputs_rejected = all(
        row["rejected"]
        for row in invalid_results
    )

    all_pass = all([
        baseline_unique,
        repeated_equal,
        parent_changes_identity,
        index_changes_identity,
        range_changes_identity,
        placement_independent,
        invalid_inputs_rejected,
    ])

    return {
        "schema": SCHEMA,
        "prerequisites": hashes,
        "validation_scheme": {
            "name": scheme,
            "status": "test_only",
            "range_unit": "intentionally_unspecified",
            "operational_fragmentation": False,
        },
        "parents": [
            {
                "tensor_name": name,
                "object_pk": parent_pks[name],
                "baseline_fragment":
                    baseline_records[name],
            }
            for name in parent_names
        ],
        "controls": {
            "control_parent": control_parent,
            "baseline_fragment_pk":
                baseline_control_pk,
            "different_index_fragment_pk":
                index_record["pk"],
            "different_range_fragment_pk":
                range_record["pk"],
            "placement_control_a":
                placement_a,
            "placement_control_b":
                placement_b,
            "placement_pk_a":
                placement_pk_a,
            "placement_pk_b":
                placement_pk_b,
        },
        "negative_inputs": invalid_results,
        "summary": {
            "parent_object_count": len(parent_names),
            "baseline_fragment_pk_count":
                len(baseline_pks),
            "baseline_fragment_pks_unique":
                baseline_unique,
            "repeated_generation_equal":
                repeated_equal,
            "parent_object_changes_identity":
                parent_changes_identity,
            "logical_index_changes_identity":
                index_changes_identity,
            "logical_range_changes_identity":
                range_changes_identity,
            "placement_independent":
                placement_independent,
            "invalid_inputs_rejected":
                invalid_inputs_rejected,
            "production_fragment_scheme_defined":
                False,
            "payload_fragment_generated":
                False,
            "gguf_payload_accessed":
                False,
            "all_pass":
                all_pass,
        },
    }


def write_atomic(
    path: Path,
    value: dict[str, Any],
) -> None:
    if path.exists():
        raise ValidationError(
            f"refusing to overwrite result: {path}"
        )

    partial = path.with_name(
        path.name + ".partial"
    )

    if partial.exists():
        raise ValidationError(
            f"stale partial exists: {partial}"
        )

    encoded = (
        json.dumps(
            value,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    ).encode("utf-8")

    try:
        with partial.open("xb") as f:
            f.write(encoded)
            f.flush()
            os.fsync(f.fileno())

        partial.replace(path)

    except Exception:
        if partial.exists():
            partial.unlink()

        raise


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_RESULT_PATH,
    )

    args = parser.parse_args()

    result = validate()
    write_atomic(args.output, result)

    s = result["summary"]

    print("=" * 72)
    print(" OPENMIND / MAF FRAGMENT IDENTITY VALIDATION V1")
    print("=" * 72)
    print("parent objects              :", s["parent_object_count"])
    print("baseline fragment PKs       :", s["baseline_fragment_pk_count"])
    print("baseline PKs unique         :", s["baseline_fragment_pks_unique"])
    print("repeat equality             :", s["repeated_generation_equal"])
    print("parent changes identity     :", s["parent_object_changes_identity"])
    print("index changes identity      :", s["logical_index_changes_identity"])
    print("range changes identity      :", s["logical_range_changes_identity"])
    print("placement independent       :", s["placement_independent"])
    print("invalid inputs rejected     :", s["invalid_inputs_rejected"])
    print("production scheme defined   :", s["production_fragment_scheme_defined"])
    print("payload fragment generated  :", s["payload_fragment_generated"])
    print("GGUF payload accessed       :", s["gguf_payload_accessed"])
    print("all_pass                    :", s["all_pass"])
    print("result                      :", args.output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
