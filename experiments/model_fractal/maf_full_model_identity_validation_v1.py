#!/usr/bin/env python3

"""Validate deterministic logical MAF identities for all frozen tensors."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

import maf_identity_v1 as identity


SCHEMA = "openmind.maf_full_model_identity_validation.v1"

ROOT = Path(__file__).resolve().parents[2]

ENGINE_PATH = (
    ROOT / "experiments/model_fractal/maf_identity_v1.py"
)

SPEC_PATH = (
    ROOT
    / "experiments/model_fractal/"
    "maf_qwen25_coder_identity_pilot_v1.json"
)

INVENTORY_PATH = (
    ROOT
    / "experiments/model_fractal/"
    "gguf_tensor_inventory_v1.json"
)

PILOT_RESULT_PATH = (
    ROOT
    / "experiments/model_fractal/"
    "maf_identity_pilot_validation_v2.json"
)

DEFAULT_RESULT_PATH = (
    ROOT
    / "experiments/model_fractal/"
    "maf_full_model_identity_validation_v1.json"
)

EXPECTED_ENGINE_SHA256 = (
    "dd4d70c2829ceb9c0a35e0e278e3a2c"
    "37b1ffaf1654165e17641f250bec8269c"
)

EXPECTED_SPEC_SHA256 = (
    "0f391eb3d0b0374a60489a1b78926320"
    "b776f79cbdf5fadb7b5b5d59ba8f833f"
)

EXPECTED_INVENTORY_SHA256 = (
    "7acf6d5dc672182aee0244b1bb85a474"
    "66f33dbdcdf10bde863e24f3659240ee"
)

EXPECTED_PILOT_RESULT_SHA256 = (
    "3d26b8eb39406f323dc571937ac2cc68"
    "4d58946613be5bdbd9c71f8872728d3e"
)

EXPECTED_MODEL_PK = (
    "mafmodel:v1:"
    "d670768d29daf84be95501480a777fd1"
    "ee5fddda18f4d0a4c8c3953e1b8cc258"
)

EXPECTED_TENSOR_COUNT = 339

PHYSICAL_OR_INTEGRITY_FIELDS = {
    "decoded_elements",
    "elements",
    "file_start",
    "index",
    "offset",
    "payload_sha256",
    "span_bytes",
    "validation",
}


class ValidationError(RuntimeError):
    """Raised when a frozen prerequisite or identity gate fails."""


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()


def require_sha(path: Path, expected: str) -> str:
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


def descriptor_record(
    namespace: str,
    descriptor: dict[str, Any],
) -> dict[str, Any]:
    canonical = identity.canonical_json_bytes(
        descriptor
    )

    return {
        "namespace": namespace,
        "descriptor": descriptor,
        "canonical_descriptor":
            canonical.decode("utf-8"),
        "descriptor_sha256":
            hashlib.sha256(canonical).hexdigest(),
        "pk":
            identity.make_pk(
                namespace,
                descriptor,
            ),
    }


def validate_prerequisites() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, str],
]:
    hashes = {
        "identity_engine_sha256":
            require_sha(
                ENGINE_PATH,
                EXPECTED_ENGINE_SHA256,
            ),
        "identity_spec_sha256":
            require_sha(
                SPEC_PATH,
                EXPECTED_SPEC_SHA256,
            ),
        "tensor_inventory_sha256":
            require_sha(
                INVENTORY_PATH,
                EXPECTED_INVENTORY_SHA256,
            ),
        "pilot_result_sha256":
            require_sha(
                PILOT_RESULT_PATH,
                EXPECTED_PILOT_RESULT_SHA256,
            ),
    }

    spec = load_json(SPEC_PATH)
    inventory = load_json(INVENTORY_PATH)
    pilot_result = load_json(PILOT_RESULT_PATH)

    tensors = inventory.get("tensors")

    if not isinstance(tensors, list):
        raise ValidationError(
            "inventory tensors must be a list"
        )

    if len(tensors) != EXPECTED_TENSOR_COUNT:
        raise ValidationError(
            "inventory tensor count drift"
        )

    names = []

    for index, row in enumerate(tensors):
        if not isinstance(row, dict):
            raise ValidationError(
                f"tensor row {index} is not an object"
            )

        required = {
            "name",
            "type",
            "dims",
        }

        missing = required - set(row)

        if missing:
            raise ValidationError(
                f"tensor row {index} missing "
                f"{sorted(missing)}"
            )

        names.append(row["name"])

    if len(set(names)) != EXPECTED_TENSOR_COUNT:
        raise ValidationError(
            "tensor names are not globally unique"
        )

    if pilot_result["summary"]["all_pass"] is not True:
        raise ValidationError(
            "frozen pilot identity gate did not pass"
        )

    if (
        pilot_result["model"]["pk"]
        != EXPECTED_MODEL_PK
    ):
        raise ValidationError(
            "pilot model PK drift"
        )

    return spec, inventory, pilot_result, hashes


def build_model(
    spec: dict[str, Any],
) -> dict[str, Any]:
    descriptor = spec["model_descriptor"]

    record = descriptor_record(
        identity.MODEL_NAMESPACE,
        descriptor,
    )

    repeated = identity.model_pk(
        architecture=descriptor["architecture"],
        model_family=descriptor["model_family"],
        model_variant=descriptor["model_variant"],
        tensor_count=descriptor["tensor_count"],
    )

    record["repeat_pk"] = repeated
    record["repeat_equal"] = (
        record["pk"] == repeated
    )

    if record["pk"] != EXPECTED_MODEL_PK:
        raise ValidationError(
            "full-model model PK differs from pilot"
        )

    if not record["repeat_equal"]:
        raise ValidationError(
            "model repeat determinism failed"
        )

    return record


def build_object(
    *,
    model_pk: str,
    row: dict[str, Any],
) -> dict[str, Any]:
    descriptor = identity.build_object_descriptor(
        model_pk_value=model_pk,
        tensor_name=row["name"],
        tensor_type=row["type"],
        dims=row["dims"],
        encoding=identity.GGUF_PAYLOAD_EXACT,
    )

    leaked = (
        PHYSICAL_OR_INTEGRITY_FIELDS
        & set(descriptor)
    )

    if leaked:
        raise ValidationError(
            f"{row['name']} descriptor leaked "
            f"non-identity fields: {sorted(leaked)}"
        )

    first = descriptor_record(
        identity.OBJECT_NAMESPACE,
        descriptor,
    )

    repeat_pk = identity.object_pk(
        model_pk_value=model_pk,
        tensor_name=row["name"],
        tensor_type=row["type"],
        dims=row["dims"],
        encoding=identity.GGUF_PAYLOAD_EXACT,
    )

    if first["pk"] != repeat_pk:
        raise ValidationError(
            f"{row['name']} repeat determinism failed"
        )

    return {
        "inventory_index": row["index"],
        "tensor_name": row["name"],
        "tensor_type": row["type"],
        "dims": row["dims"],
        "payload_sha256": row["payload_sha256"],
        "pk": first["pk"],
        "descriptor_sha256":
            first["descriptor_sha256"],
        "descriptor":
            first["descriptor"],
        "repeat_equal": True,
    }


def validate() -> dict[str, Any]:
    spec, inventory, pilot_result, hashes = (
        validate_prerequisites()
    )

    model = build_model(spec)
    model_pk = model["pk"]

    objects = [
        build_object(
            model_pk=model_pk,
            row=row,
        )
        for row in inventory["tensors"]
    ]

    object_pks = [
        row["pk"]
        for row in objects
    ]

    unique_object_pks = (
        len(object_pks)
        == len(set(object_pks))
        == EXPECTED_TENSOR_COUNT
    )

    if not unique_object_pks:
        raise ValidationError(
            "339-object PK uniqueness gate failed"
        )

    repeat_equal = all(
        row["repeat_equal"]
        for row in objects
    )

    by_name = {
        row["tensor_name"]: row
        for row in objects
    }

    output_weight = by_name["output.weight"]
    token_embedding = by_name["token_embd.weight"]

    shared_payload_control = (
        output_weight["payload_sha256"]
        == token_embedding["payload_sha256"]
    )

    shared_shape_control = (
        output_weight["dims"]
        == token_embedding["dims"]
        and output_weight["tensor_type"]
        == token_embedding["tensor_type"]
    )

    distinct_logical_identity = (
        output_weight["pk"]
        != token_embedding["pk"]
    )

    if not shared_payload_control:
        raise ValidationError(
            "expected shared-payload control disappeared"
        )

    if not shared_shape_control:
        raise ValidationError(
            "expected shared-shape control disappeared"
        )

    if not distinct_logical_identity:
        raise ValidationError(
            "same-payload tensors collapsed to one object PK"
        )

    pilot_by_name = {
        row["tensor_name"]: row["pk"]
        for row in pilot_result["objects"]
    }

    full_by_name = {
        row["tensor_name"]: row["pk"]
        for row in objects
    }

    pilot_pk_consistency = all(
        full_by_name[name] == pk
        for name, pk in pilot_by_name.items()
    )

    if not pilot_pk_consistency:
        raise ValidationError(
            "full-model PK differs from frozen pilot PK"
        )

    all_pass = all([
        model["repeat_equal"],
        repeat_equal,
        unique_object_pks,
        shared_payload_control,
        shared_shape_control,
        distinct_logical_identity,
        pilot_pk_consistency,
    ])

    return {
        "schema": SCHEMA,
        "prerequisites": hashes,
        "model": model,
        "objects": objects,
        "controls": {
            "shared_payload_pair": [
                "output.weight",
                "token_embd.weight",
            ],
            "shared_payload_sha256":
                output_weight["payload_sha256"],
            "shared_payload_equal":
                shared_payload_control,
            "shared_shape_and_type_equal":
                shared_shape_control,
            "logical_object_pks_distinct":
                distinct_logical_identity,
        },
        "summary": {
            "model_pk_count": 1,
            "object_pk_count": len(objects),
            "unique_object_pks":
                unique_object_pks,
            "model_repeat_equal":
                model["repeat_equal"],
            "object_repeat_equal":
                repeat_equal,
            "pilot_pk_consistency":
                pilot_pk_consistency,
            "shared_payload_control":
                shared_payload_control,
            "shared_payload_distinct_identity":
                distinct_logical_identity,
            "fragment_pk_generated": False,
            "gguf_payload_accessed": False,
            "all_pass": all_pass,
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

    write_atomic(
        args.output,
        result,
    )

    summary = result["summary"]

    print("=" * 72)
    print(" OPENMIND / FULL-MODEL MAF IDENTITY VALIDATION V1")
    print("=" * 72)
    print("model PK                  :", result["model"]["pk"])
    print("object PK count           :", summary["object_pk_count"])
    print("unique object PKs         :", summary["unique_object_pks"])
    print("object repeat equality    :", summary["object_repeat_equal"])
    print("pilot PK consistency      :", summary["pilot_pk_consistency"])
    print("shared payload control    :", summary["shared_payload_control"])
    print(
        "shared payload distinct ID:",
        summary["shared_payload_distinct_identity"],
    )
    print("fragment PK generated     :", summary["fragment_pk_generated"])
    print("GGUF payload accessed     :", summary["gguf_payload_accessed"])
    print("all_pass                  :", summary["all_pass"])
    print("result                    :", args.output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
