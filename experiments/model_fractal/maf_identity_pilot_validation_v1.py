#!/usr/bin/env python3

"""Validate deterministic logical MAF identities for the frozen pilot."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import maf_identity_v1 as identity


SCHEMA = "openmind.maf_identity_pilot_validation.v1"

ROOT = Path(__file__).resolve().parents[2]

PROTOCOL_PATH = (
    ROOT
    / "experiments/model_fractal/MAF_IDENTITY_V1_PROTOCOL.md"
)

ENGINE_PATH = (
    ROOT
    / "experiments/model_fractal/maf_identity_v1.py"
)

SPEC_PATH = (
    ROOT
    / "experiments/model_fractal/"
    "maf_qwen25_coder_identity_pilot_v1.json"
)

PILOT_PATH = (
    ROOT
    / "experiments/model_fractal/maf_pilot_manifest_v1.json"
)

DEFAULT_RESULT_PATH = (
    ROOT
    / "experiments/model_fractal/"
    "maf_identity_pilot_validation_v1.json"
)

EXPECTED_PROTOCOL_SHA256 = (
    "5d1d5d44f2607d01f81a95dd5ddd870"
    "0301de82d389612c13195cc95e9aac76b"
)

EXPECTED_ENGINE_SHA256 = (
    "dd4d70c2829ceb9c0a35e0e278e3a2c"
    "37b1ffaf1654165e17641f250bec8269c"
)

EXPECTED_SPEC_SHA256 = (
    "0f391eb3d0b0374a60489a1b78926320"
    "b776f79cbdf5fadb7b5b5d59ba8f833f"
)

EXPECTED_PILOT_SHA256 = (
    "690ec47152646907eed1ca873ff9cf863"
    "52777e79b116a6c2d63186e33f859d0"
)

EXPECTED_SOURCE_SHA256 = (
    "507de59046601282ba768a9789900e6cc"
    "f60ed93ddf346730b7c68eb0715bc47"
)

EXPECTED_TARGET_NAMES = [
    "output_norm.weight",
    "blk.0.attn_norm.weight",
    "blk.0.attn_q.weight",
    "blk.0.ffn_down.weight",
    "token_embd.weight",
]


class ValidationError(RuntimeError):
    """Raised when a frozen prerequisite or validation gate fails."""


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())

    if not isinstance(value, dict):
        raise ValidationError(
            f"{path} must contain a JSON object"
        )

    return value


def require_file_sha(
    path: Path,
    expected_sha256: str,
) -> str:
    actual = sha256_file(path)

    if actual != expected_sha256:
        raise ValidationError(
            f"{path} SHA256 drift: "
            f"expected {expected_sha256}, got {actual}"
        )

    return actual


def canonical_descriptor(
    descriptor: dict[str, Any],
) -> str:
    return identity.canonical_json_bytes(
        descriptor
    ).decode("utf-8")


def descriptor_record(
    namespace: str,
    descriptor: dict[str, Any],
) -> dict[str, Any]:
    canonical_bytes = identity.canonical_json_bytes(
        descriptor
    )

    return {
        "namespace": namespace,
        "descriptor": descriptor,
        "canonical_descriptor":
            canonical_bytes.decode("utf-8"),
        "descriptor_sha256":
            hashlib.sha256(canonical_bytes).hexdigest(),
        "pk":
            identity.make_pk(
                namespace,
                descriptor,
            ),
    }


def validate_prerequisites() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, str],
]:
    hashes = {
        "identity_protocol_sha256":
            require_file_sha(
                PROTOCOL_PATH,
                EXPECTED_PROTOCOL_SHA256,
            ),
        "identity_engine_sha256":
            require_file_sha(
                ENGINE_PATH,
                EXPECTED_ENGINE_SHA256,
            ),
        "identity_spec_sha256":
            require_file_sha(
                SPEC_PATH,
                EXPECTED_SPEC_SHA256,
            ),
        "pilot_manifest_sha256":
            require_file_sha(
                PILOT_PATH,
                EXPECTED_PILOT_SHA256,
            ),
    }

    spec = load_json(SPEC_PATH)
    pilot = load_json(PILOT_PATH)

    if (
        spec.get("schema")
        != "openmind.maf_identity_pilot_spec.v1"
    ):
        raise ValidationError(
            "unexpected identity pilot specification schema"
        )

    descriptor = spec.get("model_descriptor")

    if not isinstance(descriptor, dict):
        raise ValidationError(
            "model_descriptor missing or invalid"
        )

    rebuilt_descriptor = identity.build_model_descriptor(
        architecture="qwen2",
        model_family="Qwen2.5-Coder",
        model_variant="1.5B-Instruct",
        tensor_count=339,
    )

    if descriptor != rebuilt_descriptor:
        raise ValidationError(
            "frozen model descriptor differs from engine output"
        )

    provenance = spec.get(
        "provenance_not_identity",
        {},
    )

    if (
        provenance.get("source_sha256")
        != EXPECTED_SOURCE_SHA256
    ):
        raise ValidationError(
            "source provenance SHA256 mismatch"
        )

    if (
        pilot.get("schema")
        != "openmind.maf_pilot_manifest.v1"
    ):
        raise ValidationError(
            "unexpected pilot manifest schema"
        )

    rows = pilot.get("pilot")

    if not isinstance(rows, list):
        raise ValidationError(
            "pilot manifest does not contain pilot list"
        )

    if len(rows) != 5:
        raise ValidationError(
            f"expected 5 pilot tensors, got {len(rows)}"
        )

    names = [
        row.get("name")
        for row in rows
    ]

    if names != EXPECTED_TARGET_NAMES:
        raise ValidationError(
            "pilot tensor order/name set drift"
        )

    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValidationError(
                f"pilot row {index} must be an object"
            )

        required = {
            "dims",
            "name",
            "ordinal",
            "payload_sha256",
            "span_bytes",
            "type",
        }

        missing = required - set(row)

        if missing:
            raise ValidationError(
                f"pilot row {index} missing fields: "
                f"{sorted(missing)}"
            )

        payload_sha = row["payload_sha256"]

        identity.validate_sha256_text(payload_sha)

    return spec, pilot, hashes


def model_identity(
    spec: dict[str, Any],
) -> dict[str, Any]:
    descriptor = spec["model_descriptor"]

    first = descriptor_record(
        identity.MODEL_NAMESPACE,
        descriptor,
    )

    second_pk = identity.make_pk(
        identity.MODEL_NAMESPACE,
        descriptor,
    )

    repeat_equal = (
        first["pk"] == second_pk
    )

    if not repeat_equal:
        raise ValidationError(
            "model PK repeat determinism failed"
        )

    identity.validate_pk(
        first["pk"],
        namespace=identity.MODEL_NAMESPACE,
    )

    first["repeat_pk"] = second_pk
    first["repeat_equal"] = repeat_equal

    return first


def object_identity(
    *,
    model_pk: str,
    row: dict[str, Any],
    ordinal: int,
) -> dict[str, Any]:
    descriptor = identity.build_object_descriptor(
        model_pk_value=model_pk,
        tensor_name=row["name"],
        tensor_type=row["type"],
        dims=row["dims"],
        encoding=identity.GGUF_PAYLOAD_EXACT,
    )

    first = descriptor_record(
        identity.OBJECT_NAMESPACE,
        descriptor,
    )

    second_pk = identity.object_pk(
        model_pk_value=model_pk,
        tensor_name=row["name"],
        tensor_type=row["type"],
        dims=row["dims"],
        encoding=identity.GGUF_PAYLOAD_EXACT,
    )

    repeat_equal = (
        first["pk"] == second_pk
    )

    if not repeat_equal:
        raise ValidationError(
            f"repeat determinism failed for {row['name']}"
        )

    identity.validate_pk(
        first["pk"],
        namespace=identity.OBJECT_NAMESPACE,
    )

    if "payload_sha256" in descriptor:
        raise ValidationError(
            "payload SHA256 leaked into object descriptor"
        )

    placement_a = {
        "object_path":
            f"generation-a/{ordinal:02d}.mafobj",
        "object_offset":
            1000 + ordinal * 4096,
        "segment":
            "segment-a.maf",
        "segment_offset":
            8192 + ordinal * 16384,
        "cache_residency":
            "cold",
        "device_residency":
            "disk",
        "physical_generation":
            1,
    }

    placement_b = {
        "object_path":
            f"generation-b/relocated-{ordinal:02d}.mafobj",
        "object_offset":
            900000 + ordinal * 777,
        "segment":
            "segment-z.maf",
        "segment_offset":
            7000000 + ordinal * 65536,
        "cache_residency":
            "hot",
        "device_residency":
            "ram",
        "physical_generation":
            99,
    }

    if placement_a == placement_b:
        raise ValidationError(
            "synthetic placement controls must differ"
        )

    relocated_pk_a = identity.make_pk(
        identity.OBJECT_NAMESPACE,
        descriptor,
    )

    relocated_pk_b = identity.make_pk(
        identity.OBJECT_NAMESPACE,
        descriptor,
    )

    placement_independent = (
        relocated_pk_a
        == relocated_pk_b
        == first["pk"]
    )

    if not placement_independent:
        raise ValidationError(
            f"placement independence failed for {row['name']}"
        )

    payload_sha = row["payload_sha256"]

    payload_sha_separate = (
        payload_sha not in canonical_descriptor(descriptor)
        and payload_sha != first["pk"]
        and not first["pk"].endswith(payload_sha)
    )

    if not payload_sha_separate:
        raise ValidationError(
            f"payload SHA not separate for {row['name']}"
        )

    first.update({
        "ordinal": ordinal,
        "tensor_name": row["name"],
        "tensor_type": row["type"],
        "dims": row["dims"],
        "span_bytes": row["span_bytes"],
        "payload_sha256": payload_sha,
        "repeat_pk": second_pk,
        "repeat_equal": repeat_equal,
        "placement_a": placement_a,
        "placement_b": placement_b,
        "placement_independent":
            placement_independent,
        "payload_sha_separate":
            payload_sha_separate,
    })

    return first


def validate() -> dict[str, Any]:
    spec, pilot, hashes = validate_prerequisites()

    model = model_identity(spec)
    model_pk = model["pk"]

    rows = pilot["pilot"]

    objects = [
        object_identity(
            model_pk=model_pk,
            row=row,
            ordinal=index + 1,
        )
        for index, row in enumerate(rows)
    ]

    object_pks = [
        row["pk"]
        for row in objects
    ]

    unique_object_pks = (
        len(object_pks)
        == len(set(object_pks))
        == 5
    )

    if not unique_object_pks:
        raise ValidationError(
            "object PK uniqueness gate failed"
        )

    model_repeat_equal = bool(
        model["repeat_equal"]
    )

    object_repeat_equal = all(
        row["repeat_equal"]
        for row in objects
    )

    placement_independent = all(
        row["placement_independent"]
        for row in objects
    )

    payload_sha_separate = all(
        row["payload_sha_separate"]
        for row in objects
    )

    model_pk_distinct_from_objects = (
        model_pk not in object_pks
    )

    all_pass = all([
        model_repeat_equal,
        object_repeat_equal,
        unique_object_pks,
        placement_independent,
        payload_sha_separate,
        model_pk_distinct_from_objects,
    ])

    if not all_pass:
        raise ValidationError(
            "one or more identity validation gates failed"
        )

    return {
        "schema": SCHEMA,
        "prerequisites": hashes,
        "model": model,
        "objects": objects,
        "summary": {
            "model_pk_count": 1,
            "object_pk_count": len(objects),
            "model_repeat_equal":
                model_repeat_equal,
            "object_repeat_equal":
                object_repeat_equal,
            "unique_object_pks":
                unique_object_pks,
            "placement_independent":
                placement_independent,
            "payload_sha_separate":
                payload_sha_separate,
            "model_pk_distinct_from_objects":
                model_pk_distinct_from_objects,
            "fragment_pk_generated": False,
            "all_pass": all_pass,
        },
    }


def write_atomic(
    path: Path,
    value: dict[str, Any],
) -> None:
    if path.exists():
        raise ValidationError(
            f"refusing to overwrite existing result: {path}"
        )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
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

            import os
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
    print(" OPENMIND / MAF IDENTITY PILOT VALIDATION V1")
    print("=" * 72)
    print("model PK:")
    print(result["model"]["pk"])

    print()
    print("object PKs:")

    for row in result["objects"]:
        print(
            f"{row['ordinal']:02d} "
            f"{row['tensor_name']}: "
            f"{row['pk']}"
        )

    print()
    print("model repeat equality      :", summary["model_repeat_equal"])
    print("object repeat equality     :", summary["object_repeat_equal"])
    print("unique object PKs          :", summary["unique_object_pks"])
    print("placement independence     :", summary["placement_independent"])
    print("payload SHA separate       :", summary["payload_sha_separate"])
    print(
        "model/object namespace split:",
        summary["model_pk_distinct_from_objects"],
    )
    print("fragment PK generated      :", summary["fragment_pk_generated"])
    print("all_pass                   :", summary["all_pass"])
    print("result                     :", args.output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
