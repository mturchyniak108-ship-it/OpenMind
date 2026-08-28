#!/usr/bin/env python3

"""Preregistered MAF compile recipe v1 validation.

Validates the frozen planner across the frozen 339-object
Qwen2.5-Coder identity and classification results.

The validation reads JSON research artifacts only.

It does not open the source GGUF, read model payload bytes,
regenerate logical identity, create fragments, encode MAF
objects, build segments, or perform runtime residency work.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
from collections import Counter
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent

PROTOCOL = (
    HERE / "MAF_COMPILE_RECIPE_V1_PROTOCOL.md"
)
ENGINE = (
    HERE / "maf_compile_recipe_v1.py"
)
IDENTITY_RESULT = (
    HERE / "maf_full_model_identity_validation_v1.json"
)
CLASSIFICATION_RESULT = (
    HERE / "maf_metadata_classification_validation_v1.json"
)
OUTPUT = (
    HERE / "maf_compile_recipe_validation_v1.json"
)

EXPECTED_PROTOCOL_SHA256 = (
    "435ac1fe7088bf9953fc9217dafe1c8e"
    "0591a306b5b8394bc2131697a62f43ae"
)
EXPECTED_ENGINE_SHA256 = (
    "388110497205591135bd191016987391"
    "fb2c9664513f9133bc7a4abd5df5ff51"
)
EXPECTED_IDENTITY_RESULT_SHA256 = (
    "ef954f38e16ccbc73211c503d7d9c9"
    "b8462028d6222fb32fb9b15eb59615d25d"
)
EXPECTED_CLASSIFICATION_RESULT_SHA256 = (
    "70a82d3f62014578175cfabe630339b6"
    "5ceebcafbd16f181d872a9d832a6da86"
)

RESULT_SCHEMA = (
    "openmind.maf_compile_recipe_validation.v1"
)

EXPECTED_COUNT = 339

EXPECTED_RECIPE_POLICY = {
    "schema":
        "openmind.maf_compile_recipe.v1",
    "planner_version":
        "maf_planner_v1",
    "source_encoding":
        "gguf_payload_exact",
    "target_representation":
        "persistent_maf_object_exact",
    "fidelity_requirement":
        "exact",
    "payload_access":
        "deferred_to_encoder",
    "payload_passes":
        1,
    "hash_policy":
        "sha256_stream_required",
    "transform_policy":
        "none",
    "compression_policy":
        "none",
    "deduplication_policy":
        "unresolved",
    "fragmentation_policy":
        "none",
    "dense_materialization_policy":
        "optional_compute_view",
    "segment_placement_policy":
        "unresolved",
    "runtime_residency_policy":
        "unresolved",
    "maf_native_compute_policy":
        "disabled_unvalidated",
}

EXPECTED_UNRESOLVED = [
    "deduplication",
    "structural_optimization",
    "segment_placement",
    "runtime_residency",
    "maf_native_compute",
]


class ValidationError(RuntimeError):
    """Raised when preregistered validation cannot proceed."""


def sha256_file(
    path: Path,
) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        while True:
            chunk = stream.read(
                1024 * 1024
            )

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


def require_sha(
    path: Path,
    expected: str,
    label: str,
) -> None:
    actual = sha256_file(
        path
    )

    if actual != expected:
        raise ValidationError(
            f"{label} SHA256 mismatch: "
            f"{actual}"
        )


def load_json(
    path: Path,
) -> dict[str, Any]:
    value = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    if not isinstance(value, dict):
        raise ValidationError(
            f"{path.name} must contain a JSON object"
        )

    return value


def load_planner():
    sys.path.insert(
        0,
        str(HERE),
    )

    try:
        import maf_compile_recipe_v1 as planner
    finally:
        sys.path.pop(0)

    return planner


def index_identity_objects(
    identity: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    objects = identity.get(
        "objects"
    )

    if not isinstance(objects, list):
        raise ValidationError(
            "identity objects must be a list"
        )

    indexed: dict[
        str,
        dict[str, Any],
    ] = {}

    for record in objects:
        if not isinstance(record, dict):
            raise ValidationError(
                "identity object record must be a dict"
            )

        name = record.get(
            "tensor_name"
        )
        pk = record.get(
            "pk"
        )

        if not isinstance(name, str) or not name:
            raise ValidationError(
                "invalid identity tensor_name"
            )

        if not isinstance(pk, str) or not pk:
            raise ValidationError(
                f"invalid identity PK for {name}"
            )

        if name in indexed:
            raise ValidationError(
                f"duplicate identity tensor name: {name}"
            )

        indexed[name] = record

    return indexed


def classification_rows(
    result: dict[str, Any],
) -> list[dict[str, Any]]:
    rows = result.get(
        "classifications"
    )

    if not isinstance(rows, list):
        raise ValidationError(
            "classifications must be a list"
        )

    names: set[str] = set()

    for record in rows:
        if not isinstance(record, dict):
            raise ValidationError(
                "classification record must be a dict"
            )

        name = record.get(
            "name"
        )

        if not isinstance(name, str) or not name:
            raise ValidationError(
                "invalid classification name"
            )

        if name in names:
            raise ValidationError(
                f"duplicate classification name: {name}"
            )

        names.add(name)

    return rows


def recipe_map(
    recipes: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    output: dict[
        str,
        dict[str, Any],
    ] = {}

    for recipe in recipes:
        object_pk = recipe[
            "object_pk"
        ]

        if object_pk in output:
            raise ValidationError(
                f"duplicate recipe object PK: {object_pk}"
            )

        output[object_pk] = recipe

    return output


def build_inputs(
    *,
    model_pk: str,
    identity_by_name: dict[
        str,
        dict[str, Any],
    ],
    classifications: list[
        dict[str, Any]
    ],
) -> list[
    tuple[
        str,
        str,
        dict[str, Any],
    ]
]:
    inputs = []

    for classification in classifications:
        name = classification[
            "name"
        ]

        identity_record = (
            identity_by_name.get(
                name
            )
        )

        if identity_record is None:
            raise ValidationError(
                f"classification has no identity object: {name}"
            )

        if (
            identity_record.get("tensor_type")
            != classification.get("tensor_type")
        ):
            raise ValidationError(
                f"tensor type mismatch: {name}"
            )

        if (
            identity_record.get("dims")
            != classification.get("dims")
        ):
            raise ValidationError(
                f"dims mismatch: {name}"
            )

        inputs.append(
            (
                model_pk,
                identity_record["pk"],
                classification,
            )
        )

    return inputs


def physical_variants(
    inputs: list[
        tuple[
            str,
            str,
            dict[str, Any],
        ]
    ],
) -> list[
    tuple[
        str,
        str,
        dict[str, Any],
    ]
]:
    output = []

    for index, (
        model_pk,
        object_pk,
        classification,
    ) in enumerate(inputs):
        variant = copy.deepcopy(
            classification
        )

        variant.update(
            {
                "file_start":
                    10_000_000 + index,
                "offset":
                    20_000_000 + index,
                "span_bytes":
                    30_000_000 + index,
                "payload_sha256":
                    hashlib.sha256(
                        (
                            "payload-control:"
                            + str(index)
                        ).encode("utf-8")
                    ).hexdigest(),
                "validation":
                    {
                        "synthetic_physical_control":
                            True,
                    },
                "physical_segment":
                    f"control-{index % 7}.maf",
                "physical_generation":
                    99 + (index % 3),
                "device":
                    f"synthetic-device-{index % 2}",
                "cache_residency":
                    "synthetic",
            }
        )

        output.append(
            (
                model_pk,
                object_pk,
                variant,
            )
        )

    return output


def payload_hash_variants(
    inputs: list[
        tuple[
            str,
            str,
            dict[str, Any],
        ]
    ],
) -> list[
    tuple[
        str,
        str,
        dict[str, Any],
    ]
]:
    output = []

    for index, (
        model_pk,
        object_pk,
        classification,
    ) in enumerate(inputs):
        variant = copy.deepcopy(
            classification
        )

        variant[
            "payload_sha256"
        ] = hashlib.sha256(
            (
                "alternate-payload-control:"
                + str(index)
            ).encode("utf-8")
        ).hexdigest()

        output.append(
            (
                model_pk,
                object_pk,
                variant,
            )
        )

    return output


def assert_policy(
    recipes: list[
        dict[str, Any]
    ],
) -> None:
    for recipe in recipes:
        for key, expected in (
            EXPECTED_RECIPE_POLICY.items()
        ):
            if recipe.get(key) != expected:
                raise ValidationError(
                    "unexpected policy "
                    f"{key} for "
                    f"{recipe.get('name')}"
                )

        if (
            recipe.get("unresolved")
            != EXPECTED_UNRESOLVED
        ):
            raise ValidationError(
                "unexpected unresolved policy for "
                f"{recipe.get('name')}"
            )


def malformed_input_checks(
    planner,
    sample: tuple[
        str,
        str,
        dict[str, Any],
    ],
) -> bool:
    model_pk, object_pk, classification = sample

    cases: list[
        tuple[
            str,
            str,
            dict[str, Any],
        ]
    ] = []

    bad_schema = copy.deepcopy(
        classification
    )
    bad_schema["schema"] = "invalid"

    cases.append(
        (
            model_pk,
            object_pk,
            bad_schema,
        )
    )

    bad_dims = copy.deepcopy(
        classification
    )
    bad_dims["dims"] = [0]
    bad_dims["rank"] = 1
    bad_dims["elements"] = 1

    cases.append(
        (
            model_pk,
            object_pk,
            bad_dims,
        )
    )

    bad_rank = copy.deepcopy(
        classification
    )
    bad_rank["rank"] = (
        bad_rank["rank"] + 1
    )

    cases.append(
        (
            model_pk,
            object_pk,
            bad_rank,
        )
    )

    cases.append(
        (
            "mafmodel:v1:not-a-valid-digest",
            object_pk,
            classification,
        )
    )

    cases.append(
        (
            model_pk,
            "mafobj:v1:not-a-valid-digest",
            classification,
        )
    )

    for (
        test_model_pk,
        test_object_pk,
        test_classification,
    ) in cases:
        try:
            planner.build_recipe(
                model_pk=test_model_pk,
                object_pk=test_object_pk,
                classification=test_classification,
            )
        except planner.MAFCompileRecipeError:
            continue

        return False

    return True


def canonical_json_bytes(
    value: dict[str, Any],
) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
        + "\n"
    ).encode("utf-8")


def write_result_atomic(
    result: dict[str, Any],
) -> None:
    partial = OUTPUT.with_name(
        OUTPUT.name + ".partial"
    )

    if OUTPUT.exists():
        raise ValidationError(
            f"result already exists: {OUTPUT}"
        )

    if partial.exists():
        raise ValidationError(
            f"partial already exists: {partial}"
        )

    raw = canonical_json_bytes(
        result
    )

    try:
        with partial.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(
                stream.fileno()
            )

        os.replace(
            partial,
            OUTPUT,
        )
    except Exception:
        if partial.exists():
            partial.unlink()

        raise


def main() -> None:
    if OUTPUT.exists():
        raise ValidationError(
            f"result already exists: {OUTPUT}"
        )

    partial = OUTPUT.with_name(
        OUTPUT.name + ".partial"
    )

    if partial.exists():
        raise ValidationError(
            f"partial already exists: {partial}"
        )

    require_sha(
        PROTOCOL,
        EXPECTED_PROTOCOL_SHA256,
        "compile recipe protocol",
    )
    require_sha(
        ENGINE,
        EXPECTED_ENGINE_SHA256,
        "compile recipe engine",
    )
    require_sha(
        IDENTITY_RESULT,
        EXPECTED_IDENTITY_RESULT_SHA256,
        "full-model identity result",
    )
    require_sha(
        CLASSIFICATION_RESULT,
        EXPECTED_CLASSIFICATION_RESULT_SHA256,
        "metadata classification result",
    )

    planner = load_planner()

    identity = load_json(
        IDENTITY_RESULT
    )
    classification_result = load_json(
        CLASSIFICATION_RESULT
    )

    if (
        identity.get("summary", {}).get("all_pass")
        is not True
    ):
        raise ValidationError(
            "frozen identity result is not passing"
        )

    if (
        classification_result
        .get("summary", {})
        .get("all_pass")
        is not True
    ):
        raise ValidationError(
            "frozen classification result is not passing"
        )

    model = identity.get(
        "model"
    )

    if not isinstance(model, dict):
        raise ValidationError(
            "identity model must be a dict"
        )

    model_pk = model.get(
        "pk"
    )

    if not isinstance(model_pk, str):
        raise ValidationError(
            "identity model PK missing"
        )

    identity_by_name = (
        index_identity_objects(
            identity
        )
    )

    classifications = (
        classification_rows(
            classification_result
        )
    )

    if (
        len(identity_by_name)
        != EXPECTED_COUNT
    ):
        raise ValidationError(
            "unexpected identity object count"
        )

    if (
        len(classifications)
        != EXPECTED_COUNT
    ):
        raise ValidationError(
            "unexpected classification count"
        )

    if (
        set(identity_by_name)
        != {
            row["name"]
            for row in classifications
        }
    ):
        raise ValidationError(
            "identity/classification name sets differ"
        )

    inputs = build_inputs(
        model_pk=model_pk,
        identity_by_name=identity_by_name,
        classifications=classifications,
    )

    baseline = planner.build_many(
        inputs
    )

    repeated = planner.build_many(
        copy.deepcopy(inputs)
    )

    reversed_recipes = planner.build_many(
        list(
            reversed(
                copy.deepcopy(inputs)
            )
        )
    )

    physical = planner.build_many(
        physical_variants(
            inputs
        )
    )

    payload_control = planner.build_many(
        payload_hash_variants(
            inputs
        )
    )

    baseline_map = recipe_map(
        baseline
    )
    repeated_map = recipe_map(
        repeated
    )
    reversed_map = recipe_map(
        reversed_recipes
    )
    physical_map = recipe_map(
        physical
    )
    payload_control_map = recipe_map(
        payload_control
    )

    assert_policy(
        baseline
    )

    expected_object_pks = {
        record["pk"]
        for record in identity_by_name.values()
    }

    actual_object_pks = set(
        baseline_map
    )

    all_model_pk_preserved = all(
        recipe["model_pk"] == model_pk
        for recipe in baseline
    )

    all_object_pk_preserved = (
        actual_object_pks
        == expected_object_pks
    )

    unique_recipe_object_pks = (
        len(actual_object_pks)
        == len(baseline)
    )

    repeated_generation_equal = (
        baseline == repeated
    )

    repeated_mapping_equal = (
        baseline_map == repeated_map
    )

    input_order_independent = (
        baseline_map == reversed_map
    )

    physical_metadata_independent = (
        baseline_map == physical_map
    )

    payload_hash_independent = (
        baseline_map
        == payload_control_map
    )

    structural_unknown_count = sum(
        recipe["structural_class"]
        == "unknown"
        for recipe in baseline
    )

    runtime_unknown_count = sum(
        recipe["runtime_class"]
        == "unknown"
        for recipe in baseline
    )

    fragment_fields = {
        "fragment_pk",
        "fragment_pks",
        "fragment_scheme",
        "logical_fragment_index",
        "logical_range",
    }

    physical_assignment_fields = {
        "segment",
        "segment_path",
        "segment_offset",
        "segment_generation",
        "device",
        "cache_tier",
        "residency",
    }

    fragment_fields_present = any(
        fragment_fields
        & recipe.keys()
        for recipe in baseline
    )

    physical_assignment_fields_present = any(
        physical_assignment_fields
        & recipe.keys()
        for recipe in baseline
    )

    policies_exact = all(
        all(
            recipe.get(key) == value
            for key, value
            in EXPECTED_RECIPE_POLICY.items()
        )
        for recipe in baseline
    )

    unresolved_exact = all(
        recipe.get("unresolved")
        == EXPECTED_UNRESOLVED
        for recipe in baseline
    )

    malformed_inputs_rejected = (
        malformed_input_checks(
            planner,
            inputs[0],
        )
    )

    schema_counts = Counter(
        recipe["schema"]
        for recipe in baseline
    )

    semantic_counts = Counter(
        recipe["semantic_class"]
        for recipe in baseline
    )

    structural_counts = Counter(
        recipe["structural_class"]
        for recipe in baseline
    )

    runtime_counts = Counter(
        recipe["runtime_class"]
        for recipe in baseline
    )

    tensor_type_counts = Counter(
        recipe["tensor_type"]
        for recipe in baseline
    )

    source_encoding_counts = Counter(
        recipe["source_encoding"]
        for recipe in baseline
    )

    target_representation_counts = Counter(
        recipe["target_representation"]
        for recipe in baseline
    )

    summary = {
        "input_record_count":
            len(inputs),
        "output_recipe_count":
            len(baseline),
        "unique_recipe_object_pks":
            unique_recipe_object_pks,
        "all_model_pk_preserved":
            all_model_pk_preserved,
        "all_object_pks_preserved":
            all_object_pk_preserved,
        "repeated_generation_equal":
            repeated_generation_equal,
        "repeated_mapping_equal":
            repeated_mapping_equal,
        "input_order_independent":
            input_order_independent,
        "physical_metadata_independent":
            physical_metadata_independent,
        "payload_hash_independent":
            payload_hash_independent,
        "policies_exact":
            policies_exact,
        "unresolved_exact":
            unresolved_exact,
        "structural_all_unknown":
            (
                structural_unknown_count
                == EXPECTED_COUNT
            ),
        "runtime_all_unknown":
            (
                runtime_unknown_count
                == EXPECTED_COUNT
            ),
        "fragment_fields_present":
            fragment_fields_present,
        "physical_assignment_fields_present":
            physical_assignment_fields_present,
        "malformed_inputs_rejected":
            malformed_inputs_rejected,
        "gguf_model_opened":
            False,
        "payload_bytes_read":
            False,
        "identity_generation_performed":
            False,
        "fragment_identity_generated":
            False,
        "encoding_performed":
            False,
        "segment_construction_performed":
            False,
        "runtime_residency_assigned":
            False,
        "maf_native_compute_enabled":
            False,
    }

    summary["all_pass"] = all(
        (
            summary["input_record_count"]
                == EXPECTED_COUNT,
            summary["output_recipe_count"]
                == EXPECTED_COUNT,
            summary["unique_recipe_object_pks"],
            summary["all_model_pk_preserved"],
            summary["all_object_pks_preserved"],
            summary["repeated_generation_equal"],
            summary["repeated_mapping_equal"],
            summary["input_order_independent"],
            summary["physical_metadata_independent"],
            summary["payload_hash_independent"],
            summary["policies_exact"],
            summary["unresolved_exact"],
            summary["structural_all_unknown"],
            summary["runtime_all_unknown"],
            not summary["fragment_fields_present"],
            not summary[
                "physical_assignment_fields_present"
            ],
            summary["malformed_inputs_rejected"],
            not summary["gguf_model_opened"],
            not summary["payload_bytes_read"],
            not summary[
                "identity_generation_performed"
            ],
            not summary[
                "fragment_identity_generated"
            ],
            not summary["encoding_performed"],
            not summary[
                "segment_construction_performed"
            ],
            not summary[
                "runtime_residency_assigned"
            ],
            not summary[
                "maf_native_compute_enabled"
            ],
        )
    )

    result = {
        "schema":
            RESULT_SCHEMA,
        "frozen_inputs":
            {
                "compile_recipe_protocol": {
                    "path":
                        PROTOCOL.name,
                    "sha256":
                        EXPECTED_PROTOCOL_SHA256,
                },
                "compile_recipe_engine": {
                    "path":
                        ENGINE.name,
                    "sha256":
                        EXPECTED_ENGINE_SHA256,
                },
                "identity_result": {
                    "path":
                        IDENTITY_RESULT.name,
                    "sha256":
                        EXPECTED_IDENTITY_RESULT_SHA256,
                },
                "classification_result": {
                    "path":
                        CLASSIFICATION_RESULT.name,
                    "sha256":
                        EXPECTED_CLASSIFICATION_RESULT_SHA256,
                },
            },
        "validation_scope":
            {
                "expected_object_count":
                    EXPECTED_COUNT,
                "join":
                    (
                        "classification.name -> "
                        "identity.objects[].tensor_name"
                    ),
                "model_pk_source":
                    "identity.model.pk",
                "object_pk_source":
                    "identity.objects[].pk",
                "gguf_model_opened":
                    False,
                "payload_bytes_read":
                    False,
                "identity_generation_performed":
                    False,
            },
        "counts":
            {
                "schema":
                    dict(
                        sorted(
                            schema_counts.items()
                        )
                    ),
                "semantic_class":
                    dict(
                        sorted(
                            semantic_counts.items()
                        )
                    ),
                "structural_class":
                    dict(
                        sorted(
                            structural_counts.items()
                        )
                    ),
                "runtime_class":
                    dict(
                        sorted(
                            runtime_counts.items()
                        )
                    ),
                "tensor_type":
                    dict(
                        sorted(
                            tensor_type_counts.items()
                        )
                    ),
                "source_encoding":
                    dict(
                        sorted(
                            source_encoding_counts.items()
                        )
                    ),
                "target_representation":
                    dict(
                        sorted(
                            target_representation_counts.items()
                        )
                    ),
            },
        "summary":
            summary,
        "recipes":
            baseline,
    }

    write_result_atomic(
        result
    )

    print(
        "=" * 72
    )
    print(
        " OPENMIND / MAF COMPILE RECIPE VALIDATION V1"
    )
    print(
        "=" * 72
    )

    for key, value in summary.items():
        print(
            f"{key}: {value}"
        )

    print()
    print(
        f"result: {OUTPUT}"
    )
    print(
        f"result sha256: {sha256_file(OUTPUT)}"
    )


if __name__ == "__main__":
    main()
