#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent

sys.path.insert(
    0,
    str(HERE),
)

from maf_encoder_v1 import encode_object


SCHEMA = "openmind.maf_encoder_validation.v1"

INVENTORY_PATH = (
    HERE / "gguf_tensor_inventory_v1.json"
)

RECIPE_RESULT_PATH = (
    HERE / "maf_compile_recipe_validation_v1.json"
)

RESULT_PATH = (
    HERE / "maf_encoder_validation_v1.json"
)

RUNTIME_DIR = (
    ROOT
    / "results"
    / "runtime"
    / "maf_encoder_validation_v1"
)

EXPECTED_SOURCE_SHA256 = (
    "507de59046601282ba768a9789900e6cc"
    "f60ed93ddf346730b7c68eb0715bc47"
)

EXPECTED_MODEL_PK = (
    "mafmodel:v1:"
    "d670768d29daf84be95501480a777fd1"
    "ee5fddda18f4d0a4c8c3953e1b8cc258"
)

TARGETS = (
    {
        "name": "blk.0.attn_norm.weight",
        "type": "F32",
        "span_bytes": 6144,
        "object_pk": (
            "mafobj:v1:"
            "8489061c6271db7d1e726cc1795e0840"
            "23c261ce448e31d50af22de77681c696"
        ),
    },
    {
        "name": "blk.0.attn_q.weight",
        "type": "Q8_0",
        "span_bytes": 2506752,
        "object_pk": (
            "mafobj:v1:"
            "1927b0228f913339bf9f6bd31daef6d1"
            "a2b6c3ad0aeb3c15fb158108288d44ba"
        ),
    },
    {
        "name": "blk.0.ffn_down.weight",
        "type": "Q8_0",
        "span_bytes": 14622720,
        "object_pk": (
            "mafobj:v1:"
            "787817cc07b05c7520261bbccd9c3a290"
            "9a4a088e907093c3f43053879a4cd35"
        ),
    },
)

EXPECTED_TOTAL_PAYLOAD_BYTES = 17135616

ALLOWED_CLAIMS = (
    "frozen_recipe_enforced",
    "model_pk_preserved",
    "object_pk_preserved",
    "recipe_physical_agreement_validated",
    "exact_payload_digest",
    "persistent_object_created",
    "independent_object_reopen",
    "single_source_payload_pass_by_delegated_compiler_contract",
    "bounded_streaming_by_delegated_compiler_contract",
    "no_transform",
    "no_compression",
    "no_deduplication",
    "no_operational_fragmentation",
    "no_fragment_pk_generation",
    "no_segment_placement",
    "no_runtime_residency",
    "no_maf_native_compute",
)

FORBIDDEN_CLAIMS = (
    "selective_access",
    "partial_reconstruction",
    "ram_reduction",
    "payload_traffic_reduction",
    "inference_speedup",
    "maf_native_inference",
    "vulkan_execution",
    "model_replacement",
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def find_recipe_collection(doc: dict) -> list[dict]:
    candidates = [
        value
        for value in doc.values()
        if isinstance(value, list)
        and value
        and isinstance(value[0], dict)
        and "object_pk" in value[0]
        and "name" in value[0]
    ]

    if len(candidates) != 1:
        raise RuntimeError(
            "expected exactly one recipe collection"
        )

    return candidates[0]


def validate_preregistered_inputs(
    inventory_doc: dict,
    recipe_doc: dict,
) -> tuple[
    Path,
    dict[str, dict],
    dict[str, dict],
]:
    source = inventory_doc["source"]

    if source["sha256"] != EXPECTED_SOURCE_SHA256:
        raise RuntimeError(
            "source SHA256 mismatch"
        )

    source_path = Path(source["path"])

    tensors = {
        item["name"]: item
        for item in inventory_doc["tensors"]
    }

    recipes = {
        item["name"]: item
        for item in find_recipe_collection(
            recipe_doc
        )
    }

    total = 0

    for target in TARGETS:
        name = target["name"]

        physical = tensors.get(name)
        recipe = recipes.get(name)

        if physical is None:
            raise RuntimeError(
                f"missing physical record: {name}"
            )

        if recipe is None:
            raise RuntimeError(
                f"missing recipe: {name}"
            )

        if physical["type"] != target["type"]:
            raise RuntimeError(
                f"type mismatch: {name}"
            )

        if (
            physical["span_bytes"]
            != target["span_bytes"]
        ):
            raise RuntimeError(
                f"span mismatch: {name}"
            )

        if recipe["model_pk"] != EXPECTED_MODEL_PK:
            raise RuntimeError(
                f"model PK mismatch: {name}"
            )

        if (
            recipe["object_pk"]
            != target["object_pk"]
        ):
            raise RuntimeError(
                f"object PK mismatch: {name}"
            )

        total += physical["span_bytes"]

    if total != EXPECTED_TOTAL_PAYLOAD_BYTES:
        raise RuntimeError(
            "target payload total mismatch"
        )

    return source_path, tensors, recipes


def main() -> None:
    inventory_doc = load_json(
        INVENTORY_PATH
    )

    recipe_doc = load_json(
        RECIPE_RESULT_PATH
    )

    (
        source_path,
        tensors,
        recipes,
    ) = validate_preregistered_inputs(
        inventory_doc,
        recipe_doc,
    )

    if RESULT_PATH.exists():
        raise RuntimeError(
            f"result already exists: {RESULT_PATH}"
        )

    RUNTIME_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    records = []

    for index, target in enumerate(
        TARGETS,
        start=1,
    ):
        name = target["name"]

        output_path = (
            RUNTIME_DIR
            / f"{index:02d}.maf"
        )

        if output_path.exists():
            raise RuntimeError(
                f"output already exists: {output_path}"
            )

        partial = output_path.with_name(
            output_path.name + ".partial"
        )

        if partial.exists():
            raise RuntimeError(
                f"partial already exists: {partial}"
            )

        print(
            f"[{index}/{len(TARGETS)}]"
            f" encoding {name}"
            f" ({target['span_bytes']} bytes)",
            flush=True,
        )

        result = encode_object(
            recipe=recipes[name],
            physical_record=tensors[name],
            source_path=source_path,
            output_path=output_path,
        )

        view = result.object_view

        passed = (
            result.model_pk
            == EXPECTED_MODEL_PK
            and result.object_pk
            == target["object_pk"]
            and view.tensor_name
            == name
            and view.tensor_type
            == target["type"]
            and view.payload_length
            == target["span_bytes"]
            and view.payload_sha256
            == tensors[name]["payload_sha256"]
        )

        records.append(
            {
                "name": name,
                "type": target["type"],
                "span_bytes": target[
                    "span_bytes"
                ],
                "model_pk": result.model_pk,
                "object_pk": result.object_pk,
                "payload_sha256": (
                    view.payload_sha256
                ),
                "output_path": str(
                    output_path
                ),
                "pass": passed,
            }
        )

    all_pass = all(
        record["pass"]
        for record in records
    )

    result_doc = {
        "schema": SCHEMA,
        "source_sha256":
            EXPECTED_SOURCE_SHA256,
        "model_pk":
            EXPECTED_MODEL_PK,
        "target_count":
            len(TARGETS),
        "total_payload_bytes":
            EXPECTED_TOTAL_PAYLOAD_BYTES,
        "targets":
            records,
        "allowed_claims":
            list(ALLOWED_CLAIMS),
        "forbidden_claims":
            list(FORBIDDEN_CLAIMS),
        "all_pass":
            all_pass,
    }

    RESULT_PATH.write_text(
        json.dumps(
            result_doc,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    print()
    print("target_count        :", len(TARGETS))
    print(
        "total_payload_bytes :",
        EXPECTED_TOTAL_PAYLOAD_BYTES,
    )
    print("all_pass            :", all_pass)
    print("result               :", RESULT_PATH)


if __name__ == "__main__":
    main()
