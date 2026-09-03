#!/usr/bin/env python3

import ast
import ctypes
import errno
import hashlib
import json
import os
import re
import sys
import time
import unicodedata
from pathlib import Path


HERE = Path(__file__).resolve().parent

VALIDATION_PROTOCOL = (
    HERE
    / "MAF_QUERY_TO_PK_SELECTION_VALIDATION_V1_PROTOCOL.md"
)

SELECTION_PROTOCOL = (
    HERE
    / "MAF_QUERY_TO_PK_SELECTION_V1_PROTOCOL.md"
)

SELECTOR_PATH = (
    HERE
    / "maf_query_to_pk_selection_v1.py"
)

Q1_VERDICT = (
    HERE
    / "MAF_QUERY_CAPSULE_DATA_MODEL_VALIDATION_V1_1_VERDICT.md"
)

CATALOG_PATH = (
    HERE
    / "maf_query_to_pk_selection_validation_v1_catalog.json"
)

QUERY_FIXTURE_PATH = (
    HERE
    / "maf_query_to_pk_selection_validation_v1_queries.json"
)

GENERATION_MANIFEST_PATH = (
    HERE
    / "maf_query_to_pk_selection_validation_v1_generation_manifest.json"
)

RESULT_PATH = (
    HERE
    / "maf_query_to_pk_selection_validation_v1.json"
)

PARTIAL_PATH = (
    HERE
    / "maf_query_to_pk_selection_validation_v1.json.partial"
)


EXPECTED_VALIDATION_PROTOCOL_SHA256 = (
    "9bea52de94d8784f6862eee9108afdd1"
    "f52f9ff4d4f95eb03fb78d5477e00c11"
)

EXPECTED_SELECTION_PROTOCOL_SHA256 = (
    "b42a0643976c2393871e3b826ba5573"
    "b4de981b49603de63230d69cf57be0811"
)

EXPECTED_IMPLEMENTATION_SHA256 = (
    "e21c05e352fe921b791e8c936425727a"
    "98911ce7566989672a96bfd2b9613fa2"
)

EXPECTED_Q1_VERDICT_SHA256 = (
    "c396346adfc3d7aed08373a52d02e88c"
    "e14b2195269c9d090c2572828db77615"
)

EXPECTED_CATALOG_SHA256 = (
    "c51ef0fabeb10e7c8a091a093aa19346"
    "20a69b2026b5a87cb02477b9dd7ca900"
)

EXPECTED_QUERY_FIXTURE_SHA256 = (
    "32f4636bd5e8ceee0dca8342335279a6"
    "f8e6acafe866a5469f2c23aa2655202a"
)

EXPECTED_SOURCE_MANIFEST_SHA256 = (
    "28e4baaf07fae450d3c8462ed86fe59c"
    "31f0eacdd9e16a8b408994f2a54924c3"
)

EXPECTED_SOURCE_GENERATION_PK = (
    "mafgen:v1:"
    "45a80a2aa271ce04853003185b6a1227c"
    "b309bd1e3e2dc538eea849fac9f5db0"
)

EXPECTED_SELECTION_CONFIG_SHA256 = (
    "0caeaeaafdd870e6b02ccc8b44505768"
    "83d4ef5234ba689c472e3b14d9dbe120"
)

RANDOM_BASELINE_SEED = (
    "OPENMIND_6D_Q2_V1_RANDOM_BASELINE"
)


RESULT_SCHEMA = (
    "openmind."
    "maf_query_to_pk_selection_validation.v1"
)

CATALOG_SCHEMA = (
    "openmind.maf_query_pk_catalog.v1"
)

QUERY_FIXTURE_SCHEMA = (
    "openmind."
    "maf_query_to_pk_selection_validation_queries.v1"
)

CONFIG_SCHEMA = (
    "openmind.maf_query_to_pk_selection_config.v1"
)


ARM_ENV = (
    "OPENMIND_Q2_SELECTION_VALIDATION_V1_ARM"
)

ARM_VALUE = (
    "I_ACCEPT_EXACT_ONCE_Q2_V1"
)

ARM_FLAG = (
    "--run-exact-once"
)

QUALIFY_BACKEND_FLAG = (
    "--qualify-backend"
)

QUALIFY_FIXTURES_FLAG = (
    "--qualify-fixtures"
)

READINESS_FLAG = (
    "--readiness"
)


RENAME_NOREPLACE = 1
EXPECTED_CHECK_COUNT = 48


CHECK_IDS = (
    "V01_q2_protocol_binding",
    "V02_selector_implementation_binding",
    "V03_q1_acceptance_verdict_binding",
    "V04_catalog_schema",
    "V05_catalog_canonical_json",
    "V06_catalog_generation_manifest_binding",
    "V07_catalog_unique_sorted_object_pks",
    "V08_catalog_static_metadata_surface_only",
    "V09_selection_config_exact",
    "V10_query_fixture_schema",
    "V11_query_fixture_canonical_json",
    "V12_evaluation_query_minimum",
    "V13_specific_query_minimum",
    "V14_distinct_specific_target_minimum",
    "V15_fallback_control_minimum",
    "V16_query_id_uniqueness_and_order",
    "V17_query_class_semantics",
    "V18_selector_api_non_oracle",
    "V19_no_route_cache_input",
    "V20_no_bounded_expansion",
    "V21_no_inference_network_or_subprocess",
    "V22_independent_target_predicate",
    "V23_target_predicate_does_not_call_selector",
    "V24_random_baseline_exact_seed_and_formula",
    "V25_random_baseline_no_oracle_input",
    "V26_renameat2_backend_required",
    "V27_rename_noreplace_exact_value",
    "V28_no_os_link_publication",
    "V29_no_link_or_linkat_fallback",
    "V30_no_replace_or_plain_rename_fallback",
    "V31_dual_arm_required",
    "V32_guard_false_non_spending",
    "V33_fixture_qualification_before_reservation",
    "V34_backend_qualification_before_reservation",
    "V35_o_excl_partial_reservation",
    "V36_matrix_after_reservation",
    "V37_no_replace_result_publication",
    "V38_partial_file_fsync_before_publication",
    "V39_parent_directory_fsync_after_publication",
    "V40_result_schema_and_canonical_json",
    "V41_result_authority_bindings",
    "V42_supported_intent_target_hit_threshold",
    "V43_supported_intent_precision_threshold",
    "V44_specific_top1_threshold",
    "V45_random_baseline_advantage_threshold",
    "V46_budget_duplicate_and_binding_thresholds",
    "V47_boundary_exclusions",
    "V48_exact_once_no_retry_contract",
)


METRIC_FIELDS = (
    "evaluation_query_count",
    "specific_intent_query_count",
    "unique_expected_object_pk_count",
    "metadata_eligible_query_count",
    "fallback_query_count",
    "mean_selected_candidate_count",
    "maximum_selected_candidate_count",
    "supported_intent_target_hit_rate",
    "supported_intent_precision",
    "specific_intent_top1_accuracy",
    "random_baseline_top1_accuracy",
    "selector_minus_baseline_top1_difference",
    "budget_violation_count",
    "duplicate_selection_count",
    "generation_binding_violation_count",
    "manifest_binding_violation_count",
    "oracle_input_violation_count",
)


RESULT_FIELDS = (
    "schema",
    "exact_once",
    "validation_protocol_sha256",
    "selection_protocol_sha256",
    "implementation_sha256",
    "q1_verdict_sha256",
    "catalog_sha256",
    "query_fixture_sha256",
    "source_generation_pk",
    "source_manifest_sha256",
    "selection_config_sha256",
    "random_baseline_seed",
    "expected_check_count",
    "check_count",
    "checks",
    "failed_checks",
    "auditor_error",
    "all_pass",
    "metrics",
    "acceptance_thresholds",
    "boundary_exclusions",
    "publication_backend",
)


BOUNDARY_EXCLUSIONS = (
    "inference",
    "real-model answer generation",
    "route-cache reuse",
    "bounded expansion",
    "Query Capsule attach/detach lifecycle",
    "selective-working-set sufficiency",
    "object/tensor avoidance",
    "output parity",
    "answer quality",
    "MAF-native compute",
    "performance improvement",
    "network access",
)


ACCEPTANCE_THRESHOLDS = {
    "evaluation_query_count_min": 32,
    "specific_intent_query_count_min": 16,
    "unique_expected_object_pk_count_min": 8,
    "supported_intent_target_hit_rate": 1.0,
    "supported_intent_precision": 1.0,
    "specific_intent_top1_accuracy_min": 0.95,
    "selector_minus_baseline_top1_difference_min": 0.50,
    "budget_violation_count": 0,
    "duplicate_selection_count": 0,
    "generation_binding_violation_count": 0,
    "manifest_binding_violation_count": 0,
    "oracle_input_violation_count": 0,
}


EXPECTED_CONFIG = {
    "schema":
        CONFIG_SCHEMA,

    "max_candidates":
        4,

    "normalization_version":
        "nfkc_casefold_v1",

    "alias_version":
        "metadata_intent_alias_v1",

    "descriptor_version":
        "tensor_name_descriptor_v1",

    "ranking_version":
        "metadata_subset_rank_v1",

    "fallback_version":
        "sha256_rendezvous_v1",
}


CATALOG_FIELDS = {
    "schema",
    "source_generation_pk",
    "source_manifest_sha256",
    "entries",
}


CATALOG_ENTRY_FIELDS = {
    "object_pk",
    "tensor_name",
    "tensor_type",
    "dims",
    "element_count",
}


QUERY_FIXTURE_FIELDS = {
    "schema",
    "source_generation_pk",
    "source_manifest_sha256",
    "catalog_sha256",
    "selection_config",
    "random_baseline_seed",
    "queries",
}


QUERY_FIELDS = {
    "query_id",
    "query_text",
    "query_class",
}


QUERY_CLASSES = {
    "specific_intent",
    "multi_target_intent",
    "fallback_control",
}


# OPENMIND_Q2_RUNNER_CHUNK_1_COMPLETE


def canonical_json_bytes(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def file_sha256(path):
    digest = hashlib.sha256()

    with Path(path).open("rb") as stream:
        while True:
            chunk = stream.read(
                1024 * 1024
            )

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


def _load_canonical_json(
    path,
    *,
    terminal_newline=False,
):
    path = Path(path)
    raw = path.read_bytes()

    if terminal_newline:
        if not raw.endswith(b"\n"):
            raise RuntimeError(
                f"missing terminal newline: {path}"
            )

        body = raw[:-1]

        if body.endswith(b"\n"):
            raise RuntimeError(
                f"multiple terminal newlines: {path}"
            )

    else:
        if raw.endswith(b"\n"):
            raise RuntimeError(
                f"unexpected terminal newline: {path}"
            )

        body = raw

    value = json.loads(
        body.decode("utf-8")
    )

    if canonical_json_bytes(value) != body:
        raise RuntimeError(
            f"noncanonical JSON: {path}"
        )

    return value, raw


def _normalize_query(text):
    if not isinstance(text, str):
        raise RuntimeError(
            "query must be str"
        )

    text = unicodedata.normalize(
        "NFKC",
        text,
    ).casefold()

    text = re.sub(
        r"[._/\-]",
        " ",
        text,
    )

    text = "".join(
        char
        if (
            char.isalnum()
            or char.isspace()
        )
        else " "
        for char in text
    )

    text = " ".join(
        text.split()
    )

    if not text:
        raise RuntimeError(
            "empty normalized query"
        )

    return text


def _independent_query_intent(text):
    normalized = _normalize_query(
        text
    )

    layers = set(
        int(match.group(1))
        for match in re.finditer(
            (
                r"(?:^|\s)"
                r"(?:layer|block|blk)"
                r"\s+([0-9]+)"
                r"(?:\s|$)"
            ),
            normalized,
        )
    )

    if len(layers) > 1:
        raise RuntimeError(
            "multiple distinct query layers"
        )

    layer = (
        next(iter(layers))
        if layers
        else None
    )

    words = set(
        normalized.split()
    )

    tags = set()

    if (
        "attention" in words
        or "attn" in words
    ):
        tags.add("attn")

    if (
        "query" in words
        or "q" in words
    ):
        tags.add("q")

    if (
        "key" in words
        or "k" in words
    ):
        tags.add("k")

    if (
        "value" in words
        or "v" in words
    ):
        tags.add("v")

    if (
        "feed forward" in normalized
        or "feedforward" in words
        or "ffn" in words
        or "mlp" in words
    ):
        tags.add("ffn")

    if (
        "down projection" in normalized
        or "down" in words
    ):
        tags.add("down")

    if (
        "up projection" in normalized
        or "up" in words
    ):
        tags.add("up")

    if "gate" in words:
        tags.add("gate")

    if (
        "normalization" in words
        or "norm" in words
    ):
        tags.add("norm")

    if (
        "token embedding" in normalized
        or "token embeddings" in normalized
        or "embedding" in words
        or "embeddings" in words
        or "embd" in words
    ):
        tags.add("embedding")

    if (
        "lm head" in normalized
        or "output" in words
    ):
        tags.add("output")

    return (
        layer,
        frozenset(tags),
    )


def _independent_tensor_descriptor(
    tensor_name,
):
    if not isinstance(
        tensor_name,
        str,
    ):
        raise RuntimeError(
            "tensor name must be str"
        )

    normalized = unicodedata.normalize(
        "NFKC",
        tensor_name,
    ).casefold()

    normalized = re.sub(
        r"[._/\-]",
        " ",
        normalized,
    )

    words = normalized.split()

    match = re.search(
        (
            r"(?:^|\s)"
            r"blk\s+([0-9]+)"
            r"(?:\s|$)"
        ),
        normalized,
    )

    layer = (
        int(match.group(1))
        if match
        else None
    )

    mapping = {
        "attn": "attn",
        "q": "q",
        "k": "k",
        "v": "v",
        "ffn": "ffn",
        "down": "down",
        "up": "up",
        "gate": "gate",
        "norm": "norm",
        "embd": "embedding",
        "embedding": "embedding",
        "embeddings": "embedding",
        "output": "output",
    }

    tags = frozenset(
        mapping[word]
        for word in words
        if word in mapping
    )

    return (
        layer,
        tags,
    )


def _independent_targets(
    query_text,
    catalog_entries,
):
    (
        query_layer,
        query_tags,
    ) = _independent_query_intent(
        query_text
    )

    if (
        query_layer is None
        and not query_tags
    ):
        return tuple()

    output = []

    for entry in catalog_entries:
        (
            candidate_layer,
            candidate_tags,
        ) = _independent_tensor_descriptor(
            entry["tensor_name"]
        )

        if (
            query_layer is not None
            and candidate_layer
            != query_layer
        ):
            continue

        if not query_tags.issubset(
            candidate_tags
        ):
            continue

        output.append(
            entry["object_pk"]
        )

    return tuple(output)


def _independent_query_signature(
    query_text,
):
    normalized = _normalize_query(
        query_text
    )

    return hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()


def _random_baseline_selection(
    seed,
    query_signature,
    object_pks,
    budget,
):
    ranked = []

    for object_pk in object_pks:
        digest = hashlib.sha256(
            (
                seed
                + "\0"
                + query_signature
                + "\0"
                + object_pk
            ).encode("utf-8")
        ).hexdigest()

        ranked.append(
            (
                digest,
                object_pk,
            )
        )

    ranked.sort(
        key=lambda item: (
            item[0],
            item[1],
        )
    )

    return tuple(
        object_pk
        for _digest, object_pk
        in ranked[:budget]
    )


def _selector_static_contract():
    source = SELECTOR_PATH.read_text(
        encoding="utf-8"
    )

    tree = ast.parse(
        source,
        filename=str(
            SELECTOR_PATH
        ),
    )

    selector_node = None

    for node in tree.body:
        if (
            isinstance(
                node,
                ast.FunctionDef,
            )
            and node.name
            == "select_query_to_pks_v1"
        ):
            selector_node = node
            break

    if selector_node is None:
        raise RuntimeError(
            "selector API missing"
        )

    positional = [
        arg.arg
        for arg in (
            list(
                selector_node.args.posonlyargs
            )
            + list(
                selector_node.args.args
            )
        )
    ]

    keyword_only = [
        arg.arg
        for arg
        in selector_node.args.kwonlyargs
    ]

    expected_keyword_only = [
        "query",
        "catalog",
        "config",
        "source_generation_pk",
        "source_manifest_sha256",
    ]

    api_non_oracle = (
        positional == []
        and keyword_only
        == expected_keyword_only
        and selector_node.args.vararg
        is None
        and selector_node.args.kwarg
        is None
    )

    forbidden_api_tokens = {
        "expected",
        "answer",
        "reference",
        "logit",
        "hidden",
        "trace",
        "telemetry",
        "route_cache",
        "expansion",
    }

    api_tokens = set(
        positional
        + keyword_only
    )

    no_oracle_api_tokens = not (
        api_tokens
        & forbidden_api_tokens
    )

    imported_roots = set()

    for node in ast.walk(tree):
        if isinstance(
            node,
            ast.Import,
        ):
            for alias in node.names:
                imported_roots.add(
                    alias.name.split(
                        "."
                    )[0]
                )

        elif isinstance(
            node,
            ast.ImportFrom,
        ):
            if node.module:
                imported_roots.add(
                    node.module.split(
                        "."
                    )[0]
                )

    forbidden_runtime_modules = {
        "subprocess",
        "socket",
        "requests",
        "urllib",
        "http",
        "llama_cpp",
        "torch",
        "transformers",
    }

    no_inference_network_subprocess = (
        not (
            imported_roots
            & forbidden_runtime_modules
        )
    )

    return {
        "api_non_oracle":
            (
                api_non_oracle
                and no_oracle_api_tokens
            ),

        "no_route_cache_input":
            "route_cache"
            not in api_tokens,

        "no_bounded_expansion":
            "expansion"
            not in api_tokens,

        "no_inference_network_subprocess":
            no_inference_network_subprocess,
    }


def _runner_static_contract():
    source = Path(
        __file__
    ).read_text(
        encoding="utf-8"
    )

    tree = ast.parse(
        source,
        filename=str(__file__),
    )

    forbidden_os_calls = set()
    forbidden_native_calls = set()
    imported_subprocess = False

    independent_target_calls_selector = (
        False
    )

    target_function = None
    baseline_function = None

    for node in tree.body:
        if not isinstance(
            node,
            ast.FunctionDef,
        ):
            continue

        if (
            node.name
            == "_independent_targets"
        ):
            target_function = node

        elif (
            node.name
            == "_random_baseline_selection"
        ):
            baseline_function = node

    if target_function is None:
        raise RuntimeError(
            "independent target predicate missing"
        )

    if baseline_function is None:
        raise RuntimeError(
            "baseline helper missing"
        )

    for node in ast.walk(tree):
        if isinstance(
            node,
            ast.Import,
        ):
            for alias in node.names:
                if (
                    alias.name.split(".")[0]
                    == "subprocess"
                ):
                    imported_subprocess = True

        elif isinstance(
            node,
            ast.ImportFrom,
        ):
            if (
                node.module
                and node.module.split(".")[0]
                == "subprocess"
            ):
                imported_subprocess = True

        if not isinstance(
            node,
            ast.Call,
        ):
            continue

        function = node.func

        if (
            isinstance(
                function,
                ast.Attribute,
            )
            and isinstance(
                function.value,
                ast.Name,
            )
            and function.value.id == "os"
            and function.attr
            in {
                "link",
                "rename",
                "replace",
            }
        ):
            forbidden_os_calls.add(
                function.attr
            )

        if (
            isinstance(
                function,
                ast.Attribute,
            )
            and function.attr
            in {
                "link",
                "linkat",
            }
        ):
            forbidden_native_calls.add(
                function.attr
            )

        if (
            isinstance(
                function,
                ast.Name,
            )
            and function.id == "getattr"
            and len(node.args) >= 2
            and isinstance(
                node.args[1],
                ast.Constant,
            )
            and node.args[1].value
            in {
                "link",
                "linkat",
            }
        ):
            forbidden_native_calls.add(
                str(
                    node.args[1].value
                )
            )

    for node in ast.walk(
        target_function
    ):
        if (
            isinstance(
                node,
                ast.Name,
            )
            and node.id
            == "select_query_to_pks_v1"
        ):
            independent_target_calls_selector = (
                True
            )

        if (
            isinstance(
                node,
                ast.Attribute,
            )
            and node.attr
            == "select_query_to_pks_v1"
        ):
            independent_target_calls_selector = (
                True
            )

    baseline_args = [
        arg.arg
        for arg
        in baseline_function.args.args
    ]

    baseline_no_oracle = (
        baseline_args
        == [
            "seed",
            "query_signature",
            "object_pks",
            "budget",
        ]
    )

    return {
        "independent_target_predicate":
            True,

        "target_predicate_no_selector":
            (
                not
                independent_target_calls_selector
            ),

        "baseline_exact_contract":
            baseline_no_oracle,

        "baseline_no_oracle":
            baseline_no_oracle,

        "no_os_link":
            "link"
            not in forbidden_os_calls,

        "no_libc_link":
            "link"
            not in forbidden_native_calls,

        "no_libc_linkat":
            "linkat"
            not in forbidden_native_calls,

        "no_plain_os_rename":
            "rename"
            not in forbidden_os_calls,

        "no_os_replace":
            "replace"
            not in forbidden_os_calls,

        "no_subprocess":
            not imported_subprocess,

        "guard_false_contract":
            (
                ARM_ENV in source
                and ARM_FLAG in source
                and "_guard_refusal"
                in source
            ),

        "o_excl_contract":
            "os.O_EXCL"
            in source,

        "partial_fsync_contract":
            "os.fsync(partial_fd)"
            in source,

        "parent_fsync_contract":
            "os.fsync(parent_fd)"
            in source,

        "renameat2_contract":
            (
                '"renameat2"'
                in source
                or "'renameat2'"
                in source
            ),
    }


# OPENMIND_Q2_RUNNER_CHUNK_2_COMPLETE


_SHA256_TEXT_RE = re.compile(
    r"^[0-9a-f]{64}$"
)

_OBJECT_PK_TEXT_RE = re.compile(
    r"^mafobj:v1:[0-9a-f]{64}$"
)

_GENERATION_PK_TEXT_RE = re.compile(
    r"^mafgen:v1:[0-9a-f]{64}$"
)


def _require_exact_fields(
    value,
    expected,
    label,
):
    if not isinstance(value, dict):
        raise RuntimeError(
            f"{label} must be object"
        )

    actual = set(value)
    expected = set(expected)

    if actual != expected:
        missing = sorted(
            expected - actual
        )
        extra = sorted(
            actual - expected
        )

        raise RuntimeError(
            f"{label} field mismatch; "
            f"missing={missing}; "
            f"extra={extra}"
        )

    return value


def _require_sha256_text(
    value,
    label,
):
    if (
        not isinstance(value, str)
        or _SHA256_TEXT_RE.fullmatch(
            value
        )
        is None
    ):
        raise RuntimeError(
            f"invalid {label}"
        )

    return value


def _require_object_pk(
    value,
    label,
):
    if (
        not isinstance(value, str)
        or _OBJECT_PK_TEXT_RE.fullmatch(
            value
        )
        is None
    ):
        raise RuntimeError(
            f"invalid {label}"
        )

    return value


def _require_generation_pk(
    value,
    label,
):
    if (
        not isinstance(value, str)
        or _GENERATION_PK_TEXT_RE.fullmatch(
            value
        )
        is None
    ):
        raise RuntimeError(
            f"invalid {label}"
        )

    return value


def _dims_element_count(
    dims,
):
    if (
        not isinstance(dims, list)
        or not dims
    ):
        raise RuntimeError(
            "dims must be nonempty list"
        )

    total = 1

    for dim in dims:
        if (
            type(dim) is not int
            or dim <= 0
        ):
            raise RuntimeError(
                "dims must contain "
                "positive plain integers"
            )

        total *= dim

    return total


def _qualify_frozen_authorities():
    bindings = {
        "validation_protocol_sha256":
            (
                VALIDATION_PROTOCOL,
                EXPECTED_VALIDATION_PROTOCOL_SHA256,
            ),

        "selection_protocol_sha256":
            (
                SELECTION_PROTOCOL,
                EXPECTED_SELECTION_PROTOCOL_SHA256,
            ),

        "implementation_sha256":
            (
                SELECTOR_PATH,
                EXPECTED_IMPLEMENTATION_SHA256,
            ),

        "q1_verdict_sha256":
            (
                Q1_VERDICT,
                EXPECTED_Q1_VERDICT_SHA256,
            ),

        "catalog_sha256":
            (
                CATALOG_PATH,
                EXPECTED_CATALOG_SHA256,
            ),

        "query_fixture_sha256":
            (
                QUERY_FIXTURE_PATH,
                EXPECTED_QUERY_FIXTURE_SHA256,
            ),

        "source_manifest_sha256":
            (
                GENERATION_MANIFEST_PATH,
                EXPECTED_SOURCE_MANIFEST_SHA256,
            ),
    }

    actual = {}

    for name, (
        path,
        expected_sha,
    ) in bindings.items():
        if not path.is_file():
            raise RuntimeError(
                f"authority missing: {path}"
            )

        observed = file_sha256(
            path
        )

        if observed != expected_sha:
            raise RuntimeError(
                f"authority SHA mismatch: "
                f"{path}"
            )

        actual[name] = observed

    return actual


def _qualify_catalog():
    if (
        file_sha256(
            CATALOG_PATH
        )
        != EXPECTED_CATALOG_SHA256
    ):
        raise RuntimeError(
            "catalog frozen SHA mismatch"
        )

    catalog, _raw = (
        _load_canonical_json(
            CATALOG_PATH,
            terminal_newline=False,
        )
    )

    _require_exact_fields(
        catalog,
        CATALOG_FIELDS,
        "catalog",
    )

    if (
        catalog["schema"]
        != CATALOG_SCHEMA
    ):
        raise RuntimeError(
            "catalog schema mismatch"
        )

    source_generation_pk = (
        _require_generation_pk(
            catalog[
                "source_generation_pk"
            ],
            "catalog source_generation_pk",
        )
    )

    source_manifest_sha256 = (
        _require_sha256_text(
            catalog[
                "source_manifest_sha256"
            ],
            "catalog source_manifest_sha256",
        )
    )

    if (
        source_generation_pk
        != EXPECTED_SOURCE_GENERATION_PK
    ):
        raise RuntimeError(
            "catalog generation binding mismatch"
        )

    if (
        source_manifest_sha256
        != EXPECTED_SOURCE_MANIFEST_SHA256
    ):
        raise RuntimeError(
            "catalog manifest binding mismatch"
        )

    if (
        file_sha256(
            GENERATION_MANIFEST_PATH
        )
        != source_manifest_sha256
    ):
        raise RuntimeError(
            "frozen generation manifest "
            "SHA binding mismatch"
        )

    generation_manifest = json.loads(
        GENERATION_MANIFEST_PATH.read_text(
            encoding="utf-8"
        )
    )

    if (
        not isinstance(
            generation_manifest,
            dict,
        )
        or generation_manifest.get(
            "generation_pk"
        )
        != source_generation_pk
    ):
        raise RuntimeError(
            "generation manifest PK "
            "binding mismatch"
        )

    entries = catalog["entries"]

    if (
        not isinstance(entries, list)
        or not entries
    ):
        raise RuntimeError(
            "catalog entries must be "
            "nonempty list"
        )

    normalized_entries = []
    object_pks = []
    tensor_names = []

    for ordinal, entry in enumerate(
        entries
    ):
        _require_exact_fields(
            entry,
            CATALOG_ENTRY_FIELDS,
            (
                "catalog entry "
                f"{ordinal}"
            ),
        )

        object_pk = _require_object_pk(
            entry["object_pk"],
            (
                "catalog object_pk "
                f"{ordinal}"
            ),
        )

        tensor_name = entry[
            "tensor_name"
        ]

        if (
            not isinstance(
                tensor_name,
                str,
            )
            or not tensor_name
        ):
            raise RuntimeError(
                "catalog tensor_name "
                "must be nonempty str"
            )

        tensor_type = entry[
            "tensor_type"
        ]

        if type(tensor_type) is not int:
            raise RuntimeError(
                "catalog tensor_type "
                "must be plain integer"
            )

        element_count = entry[
            "element_count"
        ]

        if (
            type(element_count)
            is not int
            or element_count <= 0
        ):
            raise RuntimeError(
                "catalog element_count "
                "must be positive integer"
            )

        calculated = (
            _dims_element_count(
                entry["dims"]
            )
        )

        if calculated != element_count:
            raise RuntimeError(
                "catalog element_count "
                "does not equal dims product"
            )

        object_pks.append(
            object_pk
        )

        tensor_names.append(
            tensor_name
        )

        normalized_entries.append(
            {
                "object_pk":
                    object_pk,

                "tensor_name":
                    tensor_name,

                "tensor_type":
                    tensor_type,

                "dims":
                    list(
                        entry["dims"]
                    ),

                "element_count":
                    element_count,
            }
        )

    if (
        len(object_pks)
        != len(set(object_pks))
    ):
        raise RuntimeError(
            "duplicate catalog object PK"
        )

    if object_pks != sorted(
        object_pks
    ):
        raise RuntimeError(
            "catalog PK order "
            "is not lexical"
        )

    if (
        len(tensor_names)
        != len(set(tensor_names))
    ):
        raise RuntimeError(
            "duplicate catalog tensor name"
        )

    return {
        "catalog":
            catalog,

        "entries":
            tuple(
                normalized_entries
            ),

        "object_pks":
            tuple(object_pks),

        "source_generation_pk":
            source_generation_pk,

        "source_manifest_sha256":
            source_manifest_sha256,

        "catalog_sha256":
            EXPECTED_CATALOG_SHA256,

        "entry_count":
            len(entries),
    }


def _qualify_query_fixture(
    catalog_info,
):
    if (
        file_sha256(
            QUERY_FIXTURE_PATH
        )
        != EXPECTED_QUERY_FIXTURE_SHA256
    ):
        raise RuntimeError(
            "query fixture frozen "
            "SHA mismatch"
        )

    fixture, _raw = (
        _load_canonical_json(
            QUERY_FIXTURE_PATH,
            terminal_newline=False,
        )
    )

    _require_exact_fields(
        fixture,
        QUERY_FIXTURE_FIELDS,
        "query fixture",
    )

    if (
        fixture["schema"]
        != QUERY_FIXTURE_SCHEMA
    ):
        raise RuntimeError(
            "query fixture schema mismatch"
        )

    if (
        fixture[
            "source_generation_pk"
        ]
        != catalog_info[
            "source_generation_pk"
        ]
    ):
        raise RuntimeError(
            "fixture generation "
            "binding mismatch"
        )

    if (
        fixture[
            "source_manifest_sha256"
        ]
        != catalog_info[
            "source_manifest_sha256"
        ]
    ):
        raise RuntimeError(
            "fixture manifest "
            "binding mismatch"
        )

    if (
        fixture["catalog_sha256"]
        != catalog_info[
            "catalog_sha256"
        ]
    ):
        raise RuntimeError(
            "fixture catalog "
            "binding mismatch"
        )

    config = fixture[
        "selection_config"
    ]

    _require_exact_fields(
        config,
        EXPECTED_CONFIG.keys(),
        "selection config",
    )

    if config != EXPECTED_CONFIG:
        raise RuntimeError(
            "selection config mismatch"
        )

    config_sha = hashlib.sha256(
        canonical_json_bytes(
            config
        )
    ).hexdigest()

    if (
        config_sha
        != EXPECTED_SELECTION_CONFIG_SHA256
    ):
        raise RuntimeError(
            "selection config SHA mismatch"
        )

    if (
        fixture[
            "random_baseline_seed"
        ]
        != RANDOM_BASELINE_SEED
    ):
        raise RuntimeError(
            "random baseline seed mismatch"
        )

    queries = fixture[
        "queries"
    ]

    if not isinstance(
        queries,
        list,
    ):
        raise RuntimeError(
            "queries must be list"
        )

    query_ids = []
    specific_count = 0
    multi_count = 0
    fallback_count = 0
    metadata_eligible_count = 0

    specific_expected_pks = set()
    expected_targets_by_id = {}
    query_signatures = {}

    for ordinal, query in enumerate(
        queries
    ):
        _require_exact_fields(
            query,
            QUERY_FIELDS,
            (
                "query entry "
                f"{ordinal}"
            ),
        )

        query_id = query[
            "query_id"
        ]

        query_text = query[
            "query_text"
        ]

        query_class = query[
            "query_class"
        ]

        if (
            not isinstance(
                query_id,
                str,
            )
            or not query_id
        ):
            raise RuntimeError(
                "query_id must be "
                "nonempty str"
            )

        try:
            query_id.encode(
                "ascii"
            )
        except UnicodeEncodeError as exc:
            raise RuntimeError(
                "query_id must be ASCII"
            ) from exc

        if (
            not isinstance(
                query_text,
                str,
            )
            or not query_text
        ):
            raise RuntimeError(
                "query_text must be "
                "nonempty str"
            )

        if query_class not in (
            QUERY_CLASSES
        ):
            raise RuntimeError(
                "invalid query_class"
            )

        targets = (
            _independent_targets(
                query_text,
                catalog_info[
                    "entries"
                ],
            )
        )

        signature = (
            _independent_query_signature(
                query_text
            )
        )

        query_ids.append(
            query_id
        )

        expected_targets_by_id[
            query_id
        ] = tuple(
            targets
        )

        query_signatures[
            query_id
        ] = signature

        if targets:
            metadata_eligible_count += 1

        if (
            query_class
            == "specific_intent"
        ):
            specific_count += 1

            if len(targets) != 1:
                raise RuntimeError(
                    "specific_intent must "
                    "resolve to exactly one "
                    "independent target"
                )

            specific_expected_pks.add(
                targets[0]
            )

        elif (
            query_class
            == "multi_target_intent"
        ):
            multi_count += 1

            if len(targets) < 2:
                raise RuntimeError(
                    "multi_target_intent "
                    "must resolve to at "
                    "least two targets"
                )

        elif (
            query_class
            == "fallback_control"
        ):
            fallback_count += 1

            if len(targets) != 0:
                raise RuntimeError(
                    "fallback_control must "
                    "resolve to zero targets"
                )

    if (
        len(query_ids)
        != len(set(query_ids))
    ):
        raise RuntimeError(
            "duplicate query_id"
        )

    if query_ids != sorted(
        query_ids
    ):
        raise RuntimeError(
            "query IDs not in "
            "lexical order"
        )

    if len(queries) < 32:
        raise RuntimeError(
            "evaluation query minimum "
            "not satisfied"
        )

    if specific_count < 16:
        raise RuntimeError(
            "specific query minimum "
            "not satisfied"
        )

    if fallback_count < 4:
        raise RuntimeError(
            "fallback-control minimum "
            "not satisfied"
        )

    if (
        len(
            specific_expected_pks
        )
        < 8
    ):
        raise RuntimeError(
            "distinct specific target "
            "minimum not satisfied"
        )

    return {
        "fixture":
            fixture,

        "queries":
            tuple(
                dict(query)
                for query in queries
            ),

        "query_ids":
            tuple(query_ids),

        "expected_targets_by_id":
            expected_targets_by_id,

        "query_signatures":
            query_signatures,

        "selection_config":
            dict(config),

        "selection_config_sha256":
            config_sha,

        "random_baseline_seed":
            fixture[
                "random_baseline_seed"
            ],

        "evaluation_query_count":
            len(queries),

        "specific_intent_query_count":
            specific_count,

        "multi_target_query_count":
            multi_count,

        "fallback_query_count":
            fallback_count,

        "metadata_eligible_query_count":
            metadata_eligible_count,

        "unique_expected_object_pk_count":
            len(
                specific_expected_pks
            ),
    }


def _qualify_fixtures():
    authorities = (
        _qualify_frozen_authorities()
    )

    catalog_info = (
        _qualify_catalog()
    )

    fixture_info = (
        _qualify_query_fixture(
            catalog_info
        )
    )

    return {
        "authorities":
            authorities,

        "catalog":
            catalog_info,

        "fixture":
            fixture_info,
    }


# OPENMIND_Q2_RUNNER_CHUNK_3_COMPLETE


def _load_renameat2():
    libc = ctypes.CDLL(
        None,
        use_errno=True,
    )

    renameat2 = getattr(
        libc,
        "renameat2",
        None,
    )

    if renameat2 is None:
        raise RuntimeError(
            "renameat2 unavailable"
        )

    renameat2.argtypes = [
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    ]

    renameat2.restype = (
        ctypes.c_int
    )

    return renameat2


def _exclusive_write(
    path,
    data,
):
    path = Path(path)

    fd = os.open(
        path,
        (
            os.O_WRONLY
            | os.O_CREAT
            | os.O_EXCL
        ),
        0o600,
    )

    try:
        view = memoryview(
            data
        )

        while view:
            written = os.write(
                fd,
                view,
            )

            if written <= 0:
                raise RuntimeError(
                    "short exclusive write"
                )

            view = view[
                written:
            ]

        os.fsync(fd)

    finally:
        os.close(fd)


def _assert_result_slot_unspent():
    if RESULT_PATH.exists():
        raise RuntimeError(
            "authoritative result "
            "already exists"
        )

    if PARTIAL_PATH.exists():
        raise RuntimeError(
            "authoritative partial "
            "already exists"
        )


def _qualify_backend():
    _assert_result_slot_unspent()

    renameat2 = (
        _load_renameat2()
    )

    token = hashlib.sha256(
        (
            str(os.getpid())
            + ":"
            + str(time.time_ns())
        ).encode("ascii")
    ).hexdigest()[:24]

    source = (
        HERE
        / (
            ".q2v1_backend_"
            + token
            + ".source"
        )
    )

    target = (
        HERE
        / (
            ".q2v1_backend_"
            + token
            + ".target"
        )
    )

    collision_source = (
        HERE
        / (
            ".q2v1_backend_"
            + token
            + ".collision_source"
        )
    )

    incumbent = (
        HERE
        / (
            ".q2v1_backend_"
            + token
            + ".incumbent"
        )
    )

    paths = (
        source,
        target,
        collision_source,
        incumbent,
    )

    for path in paths:
        if path.exists():
            raise RuntimeError(
                "backend qualification "
                "temporary collision"
            )

    parent_fd = None

    success_publication = False
    byte_preserved = False
    inode_preserved = False
    directory_fsync = False
    collision_rejected = False
    incumbent_preserved = False
    collision_source_preserved = False

    try:
        _exclusive_write(
            source,
            b"OPENMIND_Q2_V1_BACKEND_SOURCE",
        )

        source_stat = (
            source.stat()
        )

        parent_fd = os.open(
            HERE,
            (
                os.O_RDONLY
                | os.O_DIRECTORY
            ),
        )

        ctypes.set_errno(0)

        rc = renameat2(
            parent_fd,
            source.name.encode(
                "utf-8"
            ),
            parent_fd,
            target.name.encode(
                "utf-8"
            ),
            RENAME_NOREPLACE,
        )

        if rc != 0:
            value = ctypes.get_errno()

            raise OSError(
                value,
                os.strerror(value),
            )

        success_publication = True

        os.fsync(
            parent_fd
        )

        directory_fsync = True

        if source.exists():
            raise RuntimeError(
                "successful source remained"
            )

        if not target.is_file():
            raise RuntimeError(
                "successful target missing"
            )

        target_stat = (
            target.stat()
        )

        byte_preserved = (
            target.read_bytes()
            == b"OPENMIND_Q2_V1_BACKEND_SOURCE"
        )

        inode_preserved = (
            source_stat.st_dev
            == target_stat.st_dev
            and source_stat.st_ino
            == target_stat.st_ino
        )

        if not (
            byte_preserved
            and inode_preserved
        ):
            raise RuntimeError(
                "successful publication "
                "did not preserve bytes/inode"
            )

        _exclusive_write(
            collision_source,
            b"OPENMIND_Q2_V1_COLLISION_SOURCE",
        )

        _exclusive_write(
            incumbent,
            b"OPENMIND_Q2_V1_INCUMBENT",
        )

        collision_stat = (
            collision_source.stat()
        )

        incumbent_stat = (
            incumbent.stat()
        )

        ctypes.set_errno(0)

        rc = renameat2(
            parent_fd,
            collision_source.name.encode(
                "utf-8"
            ),
            parent_fd,
            incumbent.name.encode(
                "utf-8"
            ),
            RENAME_NOREPLACE,
        )

        collision_errno = (
            ctypes.get_errno()
        )

        collision_rejected = (
            rc != 0
            and collision_errno
            == errno.EEXIST
        )

        collision_source_preserved = (
            collision_source.is_file()
            and collision_source.read_bytes()
            == (
                b"OPENMIND_Q2_V1_"
                b"COLLISION_SOURCE"
            )
            and collision_source.stat().st_dev
            == collision_stat.st_dev
            and collision_source.stat().st_ino
            == collision_stat.st_ino
        )

        incumbent_preserved = (
            incumbent.is_file()
            and incumbent.read_bytes()
            == b"OPENMIND_Q2_V1_INCUMBENT"
            and incumbent.stat().st_dev
            == incumbent_stat.st_dev
            and incumbent.stat().st_ino
            == incumbent_stat.st_ino
        )

        if not collision_rejected:
            raise RuntimeError(
                "RENAME_NOREPLACE "
                "collision not rejected"
            )

        if not collision_source_preserved:
            raise RuntimeError(
                "collision source changed"
            )

        if not incumbent_preserved:
            raise RuntimeError(
                "incumbent changed"
            )

        os.fsync(
            parent_fd
        )

        _assert_result_slot_unspent()

        return {
            "renameat2_available":
                True,

            "rename_noreplace_exact_value":
                RENAME_NOREPLACE == 1,

            "successful_publication":
                success_publication,

            "byte_preservation":
                byte_preserved,

            "inode_preservation":
                inode_preserved,

            "directory_fsync":
                directory_fsync,

            "collision_rejection":
                collision_rejected,

            "incumbent_preservation":
                incumbent_preserved,

            "unpublished_partial_preservation":
                collision_source_preserved,

            "result_slot_unspent":
                (
                    not RESULT_PATH.exists()
                    and not PARTIAL_PATH.exists()
                ),
        }

    finally:
        cleanup_parent_fd = (
            parent_fd
        )

        if cleanup_parent_fd is None:
            try:
                cleanup_parent_fd = os.open(
                    HERE,
                    (
                        os.O_RDONLY
                        | os.O_DIRECTORY
                    ),
                )
            except Exception:
                cleanup_parent_fd = None

        for path in paths:
            try:
                path.unlink(
                    missing_ok=True
                )
            except Exception:
                pass

        if cleanup_parent_fd is not None:
            try:
                os.fsync(
                    cleanup_parent_fd
                )
            except Exception:
                pass

        if (
            cleanup_parent_fd is not None
            and cleanup_parent_fd
            != parent_fd
        ):
            try:
                os.close(
                    cleanup_parent_fd
                )
            except Exception:
                pass

        if parent_fd is not None:
            try:
                os.close(
                    parent_fd
                )
            except Exception:
                pass


def _full_prequalification():
    _assert_result_slot_unspent()

    fixture_info = (
        _qualify_fixtures()
    )

    selector_static = (
        _selector_static_contract()
    )

    runner_static = (
        _runner_static_contract()
    )

    backend = (
        _qualify_backend()
    )

    if not all(
        selector_static.values()
    ):
        failed = [
            name
            for name, passed
            in selector_static.items()
            if not passed
        ]

        raise RuntimeError(
            "selector static "
            "qualification failed: "
            + ",".join(failed)
        )

    if not all(
        runner_static.values()
    ):
        failed = [
            name
            for name, passed
            in runner_static.items()
            if not passed
        ]

        raise RuntimeError(
            "runner static "
            "qualification failed: "
            + ",".join(failed)
        )

    if not all(
        backend.values()
    ):
        failed = [
            name
            for name, passed
            in backend.items()
            if not passed
        ]

        raise RuntimeError(
            "backend qualification failed: "
            + ",".join(failed)
        )

    _assert_result_slot_unspent()

    return {
        "fixture":
            fixture_info,

        "selector_static":
            selector_static,

        "runner_static":
            runner_static,

        "backend":
            backend,

        "fixture_qualified_before_reservation":
            True,

        "backend_qualified_before_reservation":
            True,

        "result_slot_unspent":
            True,
    }


# OPENMIND_Q2_RUNNER_CHUNK_4_COMPLETE


def _arm_decision(
    env_value,
    cli_armed,
):
    env_armed = (
        env_value == ARM_VALUE
    )

    if (
        env_armed
        and cli_armed
    ):
        return "FULLY_ARMED"

    if (
        env_armed
        and not cli_armed
    ):
        return "REFUSE_ENV_ONLY"

    if (
        not env_armed
        and cli_armed
    ):
        return "REFUSE_CLI_ONLY"

    return "REFUSE_GUARD_FALSE"


def _runtime_arm_decision(
    args,
):
    if not isinstance(
        args,
        (list, tuple),
    ):
        raise RuntimeError(
            "args must be sequence"
        )

    cli_armed = (
        len(args) == 1
        and args[0] == ARM_FLAG
    )

    return _arm_decision(
        os.environ.get(
            ARM_ENV
        ),
        cli_armed,
    )


def _guard_refusal(
    reason,
):
    _assert_result_slot_unspent()

    if not isinstance(
        reason,
        str,
    ) or not reason:
        raise RuntimeError(
            "guard refusal reason "
            "must be nonempty str"
        )

    print(
        "SCIENTIFIC_GUARD=REFUSED"
    )

    print(
        "REASON="
        + reason
    )

    print(
        "RESULT_PATH_PRESENT="
        + str(
            RESULT_PATH.exists()
        )
    )

    print(
        "PARTIAL_PATH_PRESENT="
        + str(
            PARTIAL_PATH.exists()
        )
    )

    _assert_result_slot_unspent()

    print(
        "RESULT_SLOT=UNSPENT"
    )

    return 3


def _qualify_guard_logic():
    _assert_result_slot_unspent()

    checks = {
        "guard_false":
            (
                _arm_decision(
                    None,
                    False,
                )
                == "REFUSE_GUARD_FALSE"
            ),

        "wrong_environment_value":
            (
                _arm_decision(
                    "WRONG_VALUE",
                    False,
                )
                == "REFUSE_GUARD_FALSE"
            ),

        "environment_only":
            (
                _arm_decision(
                    ARM_VALUE,
                    False,
                )
                == "REFUSE_ENV_ONLY"
            ),

        "cli_only":
            (
                _arm_decision(
                    None,
                    True,
                )
                == "REFUSE_CLI_ONLY"
            ),

        "fully_armed":
            (
                _arm_decision(
                    ARM_VALUE,
                    True,
                )
                == "FULLY_ARMED"
            ),

        "result_slot_unspent":
            (
                not RESULT_PATH.exists()
                and not PARTIAL_PATH.exists()
            ),
    }

    if not all(
        checks.values()
    ):
        failed = [
            name
            for name, passed
            in checks.items()
            if not passed
        ]

        raise RuntimeError(
            "guard logic qualification "
            "failed: "
            + ",".join(failed)
        )

    _assert_result_slot_unspent()

    return checks


def _fixture_qualification_summary():
    _assert_result_slot_unspent()

    value = (
        _qualify_fixtures()
    )

    fixture = value[
        "fixture"
    ]

    catalog = value[
        "catalog"
    ]

    summary = {
        "catalog_entry_count":
            catalog[
                "entry_count"
            ],

        "evaluation_query_count":
            fixture[
                "evaluation_query_count"
            ],

        "specific_intent_query_count":
            fixture[
                "specific_intent_query_count"
            ],

        "multi_target_query_count":
            fixture[
                "multi_target_query_count"
            ],

        "fallback_query_count":
            fixture[
                "fallback_query_count"
            ],

        "metadata_eligible_query_count":
            fixture[
                "metadata_eligible_query_count"
            ],

        "unique_expected_object_pk_count":
            fixture[
                "unique_expected_object_pk_count"
            ],

        "selection_config_sha256":
            fixture[
                "selection_config_sha256"
            ],

        "result_slot_unspent":
            (
                not RESULT_PATH.exists()
                and not PARTIAL_PATH.exists()
            ),
    }

    _assert_result_slot_unspent()

    return summary


def _backend_qualification_summary():
    _assert_result_slot_unspent()

    summary = (
        _qualify_backend()
    )

    _assert_result_slot_unspent()

    return summary


def _readiness_summary():
    _assert_result_slot_unspent()

    value = (
        _full_prequalification()
    )

    summary = {
        "fixture_qualified":
            value[
                "fixture_qualified_before_reservation"
            ],

        "backend_qualified":
            value[
                "backend_qualified_before_reservation"
            ],

        "selector_static_qualified":
            all(
                value[
                    "selector_static"
                ].values()
            ),

        "runner_static_qualified":
            all(
                value[
                    "runner_static"
                ].values()
            ),

        "result_slot_unspent":
            (
                not RESULT_PATH.exists()
                and not PARTIAL_PATH.exists()
            ),
    }

    if not all(
        summary.values()
    ):
        failed = [
            name
            for name, passed
            in summary.items()
            if not passed
        ]

        raise RuntimeError(
            "readiness qualification "
            "failed: "
            + ",".join(failed)
        )

    _assert_result_slot_unspent()

    return summary


def _print_qualification(
    mode,
    value,
):
    if (
        not isinstance(mode, str)
        or not mode
    ):
        raise RuntimeError(
            "qualification mode "
            "must be nonempty str"
        )

    print(
        "MODE="
        + mode
    )

    print(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
    )

    print(
        "RESULT_PATH_PRESENT="
        + str(
            RESULT_PATH.exists()
        )
    )

    print(
        "PARTIAL_PATH_PRESENT="
        + str(
            PARTIAL_PATH.exists()
        )
    )

    _assert_result_slot_unspent()

    print(
        "RESULT_SLOT=UNSPENT"
    )


# OPENMIND_Q2_RUNNER_CHUNK_5_COMPLETE


def _run_scientific_evaluation(
    prequalification,
):
    from maf_query_to_pk_selection_v1 import (
        MAFQueryPKCatalogV1,
        MAFQueryToPKSelectionConfigV1,
        MAFQueryToPKSelectionResultV1,
        select_query_to_pks_v1,
    )

    if not isinstance(
        prequalification,
        dict,
    ):
        raise RuntimeError(
            "prequalification must be dict"
        )

    if (
        prequalification.get(
            "fixture_qualified_before_reservation"
        )
        is not True
    ):
        raise RuntimeError(
            "fixture was not qualified "
            "before reservation"
        )

    if (
        prequalification.get(
            "backend_qualified_before_reservation"
        )
        is not True
    ):
        raise RuntimeError(
            "backend was not qualified "
            "before reservation"
        )

    fixture_bundle = (
        prequalification[
            "fixture"
        ]
    )

    catalog_info = (
        fixture_bundle[
            "catalog"
        ]
    )

    fixture_info = (
        fixture_bundle[
            "fixture"
        ]
    )

    catalog_document = (
        catalog_info[
            "catalog"
        ]
    )

    fixture_document = (
        fixture_info[
            "fixture"
        ]
    )

    catalog = (
        MAFQueryPKCatalogV1.from_mapping(
            catalog_document
        )
    )

    config = (
        MAFQueryToPKSelectionConfigV1.from_mapping(
            fixture_document[
                "selection_config"
            ]
        )
    )

    if (
        catalog.catalog_sha256
        != EXPECTED_CATALOG_SHA256
    ):
        raise RuntimeError(
            "selector catalog object "
            "SHA mismatch"
        )

    if (
        config.selection_config_sha256
        != EXPECTED_SELECTION_CONFIG_SHA256
    ):
        raise RuntimeError(
            "selector config object "
            "SHA mismatch"
        )

    catalog.require_source_binding(
        source_generation_pk=(
            EXPECTED_SOURCE_GENERATION_PK
        ),
        source_manifest_sha256=(
            EXPECTED_SOURCE_MANIFEST_SHA256
        ),
    )

    catalog_object_pks = tuple(
        catalog_info[
            "object_pks"
        ]
    )

    queries = tuple(
        fixture_info[
            "queries"
        ]
    )

    expected_targets_by_id = (
        fixture_info[
            "expected_targets_by_id"
        ]
    )

    query_signatures = (
        fixture_info[
            "query_signatures"
        ]
    )

    selected_candidate_counts = []

    supported_query_count = 0
    supported_hit_count = 0

    total_selected_supported = 0
    total_selected_expected = 0

    specific_top1_correct = 0
    random_baseline_top1_correct = 0

    budget_violation_count = 0
    duplicate_selection_count = 0
    generation_binding_violation_count = 0
    manifest_binding_violation_count = 0

    # The frozen selector invocation below receives only:
    # query, catalog, config, source_generation_pk,
    # source_manifest_sha256.
    #
    # No expected target, answer, reference execution,
    # route cache, expansion result, inference output or
    # telemetry is supplied.
    oracle_input_violation_count = 0

    fallback_contract_pass = True
    supported_fallback_contract_pass = True
    selector_result_contract_pass = True

    selector_call_count = 0

    for query_record in queries:
        query_id = query_record[
            "query_id"
        ]

        query_text = query_record[
            "query_text"
        ]

        query_class = query_record[
            "query_class"
        ]

        expected_targets = tuple(
            expected_targets_by_id[
                query_id
            ]
        )

        expected_set = set(
            expected_targets
        )

        expected_signature = (
            query_signatures[
                query_id
            ]
        )

        result = (
            select_query_to_pks_v1(
                query=query_text,
                catalog=catalog,
                config=config,
                source_generation_pk=(
                    EXPECTED_SOURCE_GENERATION_PK
                ),
                source_manifest_sha256=(
                    EXPECTED_SOURCE_MANIFEST_SHA256
                ),
            )
        )

        selector_call_count += 1

        if not isinstance(
            result,
            MAFQueryToPKSelectionResultV1,
        ):
            raise RuntimeError(
                "selector returned "
                "unexpected result type"
            )

        selected = tuple(
            result.selected_object_pks
        )

        selected_candidate_counts.append(
            len(selected)
        )

        if (
            len(selected)
            > config.max_candidates
        ):
            budget_violation_count += 1

        if (
            len(selected)
            != len(set(selected))
        ):
            duplicate_selection_count += 1

        if (
            result.source_generation_pk
            != EXPECTED_SOURCE_GENERATION_PK
        ):
            generation_binding_violation_count += 1

        if (
            result.source_manifest_sha256
            != EXPECTED_SOURCE_MANIFEST_SHA256
        ):
            manifest_binding_violation_count += 1

        if (
            result.catalog_sha256
            != EXPECTED_CATALOG_SHA256
        ):
            selector_result_contract_pass = False

        if (
            result.selection_config_sha256
            != EXPECTED_SELECTION_CONFIG_SHA256
        ):
            selector_result_contract_pass = False

        if (
            result.query_signature
            != expected_signature
        ):
            selector_result_contract_pass = False

        if any(
            object_pk
            not in catalog_object_pks
            for object_pk in selected
        ):
            selector_result_contract_pass = False

        if (
            query_class
            == "fallback_control"
        ):
            if result.fallback_used is not True:
                fallback_contract_pass = False

            continue

        supported_query_count += 1

        if result.fallback_used is not False:
            supported_fallback_contract_pass = False

        selected_set = set(
            selected
        )

        if (
            selected_set
            & expected_set
        ):
            supported_hit_count += 1

        total_selected_supported += (
            len(selected)
        )

        total_selected_expected += (
            len(
                selected_set
                & expected_set
            )
        )

        if (
            query_class
            != "specific_intent"
        ):
            continue

        if len(expected_targets) != 1:
            raise RuntimeError(
                "specific query lost "
                "its independently qualified "
                "single target"
            )

        expected_pk = (
            expected_targets[0]
        )

        if (
            selected
            and selected[0]
            == expected_pk
        ):
            specific_top1_correct += 1

        baseline_selection = (
            _random_baseline_selection(
                RANDOM_BASELINE_SEED,
                expected_signature,
                catalog_object_pks,
                config.max_candidates,
            )
        )

        if (
            baseline_selection
            and baseline_selection[0]
            == expected_pk
        ):
            random_baseline_top1_correct += 1

    evaluation_query_count = (
        len(queries)
    )

    specific_intent_query_count = (
        fixture_info[
            "specific_intent_query_count"
        ]
    )

    if (
        selector_call_count
        != evaluation_query_count
    ):
        raise RuntimeError(
            "selector call count "
            "does not equal evaluation count"
        )

    if supported_query_count <= 0:
        raise RuntimeError(
            "supported query set empty"
        )

    if (
        specific_intent_query_count
        <= 0
    ):
        raise RuntimeError(
            "specific query set empty"
        )

    supported_intent_target_hit_rate = (
        supported_hit_count
        / supported_query_count
    )

    if total_selected_supported:
        supported_intent_precision = (
            total_selected_expected
            / total_selected_supported
        )
    else:
        supported_intent_precision = 0.0

    specific_intent_top1_accuracy = (
        specific_top1_correct
        / specific_intent_query_count
    )

    random_baseline_top1_accuracy = (
        random_baseline_top1_correct
        / specific_intent_query_count
    )

    selector_minus_baseline = (
        specific_intent_top1_accuracy
        - random_baseline_top1_accuracy
    )

    if selected_candidate_counts:
        mean_selected_candidate_count = (
            sum(
                selected_candidate_counts
            )
            / len(
                selected_candidate_counts
            )
        )

        maximum_selected_candidate_count = (
            max(
                selected_candidate_counts
            )
        )

    else:
        mean_selected_candidate_count = 0.0
        maximum_selected_candidate_count = 0

    metrics = {
        "evaluation_query_count":
            evaluation_query_count,

        "specific_intent_query_count":
            specific_intent_query_count,

        "unique_expected_object_pk_count":
            fixture_info[
                "unique_expected_object_pk_count"
            ],

        "metadata_eligible_query_count":
            fixture_info[
                "metadata_eligible_query_count"
            ],

        "fallback_query_count":
            fixture_info[
                "fallback_query_count"
            ],

        "mean_selected_candidate_count":
            mean_selected_candidate_count,

        "maximum_selected_candidate_count":
            maximum_selected_candidate_count,

        "supported_intent_target_hit_rate":
            supported_intent_target_hit_rate,

        "supported_intent_precision":
            supported_intent_precision,

        "specific_intent_top1_accuracy":
            specific_intent_top1_accuracy,

        "random_baseline_top1_accuracy":
            random_baseline_top1_accuracy,

        "selector_minus_baseline_top1_difference":
            selector_minus_baseline,

        "budget_violation_count":
            budget_violation_count,

        "duplicate_selection_count":
            duplicate_selection_count,

        "generation_binding_violation_count":
            generation_binding_violation_count,

        "manifest_binding_violation_count":
            manifest_binding_violation_count,

        "oracle_input_violation_count":
            oracle_input_violation_count,
    }

    if tuple(
        metrics.keys()
    ) != METRIC_FIELDS:
        raise RuntimeError(
            "scientific metric schema mismatch"
        )

    return {
        "metrics":
            metrics,

        "selector_call_count":
            selector_call_count,

        "fallback_contract_pass":
            fallback_contract_pass,

        "supported_fallback_contract_pass":
            supported_fallback_contract_pass,

        "selector_result_contract_pass":
            selector_result_contract_pass,
    }


# OPENMIND_Q2_RUNNER_CHUNK_6_COMPLETE


def _baseline_exact_contract_check(
    fixture_info,
    catalog_info,
):
    if (
        fixture_info[
            "random_baseline_seed"
        ]
        != RANDOM_BASELINE_SEED
    ):
        return False

    object_pks = tuple(
        catalog_info[
            "object_pks"
        ]
    )

    if len(object_pks) < 2:
        return False

    query_signature = (
        "0123456789abcdef"
        * 4
    )

    budget = min(
        4,
        len(object_pks),
    )

    expected_rank = []

    for object_pk in object_pks:
        digest = hashlib.sha256(
            (
                RANDOM_BASELINE_SEED
                + "\0"
                + query_signature
                + "\0"
                + object_pk
            ).encode("utf-8")
        ).hexdigest()

        expected_rank.append(
            (
                digest,
                object_pk,
            )
        )

    expected_rank.sort(
        key=lambda item: (
            item[0],
            item[1],
        )
    )

    expected = tuple(
        object_pk
        for _digest, object_pk
        in expected_rank[:budget]
    )

    observed = (
        _random_baseline_selection(
            RANDOM_BASELINE_SEED,
            query_signature,
            object_pks,
            budget,
        )
    )

    return observed == expected


def _exact_once_static_contract():
    source = Path(
        __file__
    ).read_text(
        encoding="utf-8"
    )

    tree = ast.parse(
        source,
        filename=str(__file__),
    )

    functions = {
        node.name: node
        for node in tree.body
        if isinstance(
            node,
            ast.FunctionDef,
        )
    }

    authoritative = functions.get(
        "_authoritative_run"
    )

    reserve = functions.get(
        "_reserve_partial"
    )

    publish = functions.get(
        "_publish_result"
    )

    write_partial = functions.get(
        "_write_result_partial"
    )

    if (
        authoritative is None
        or reserve is None
        or publish is None
        or write_partial is None
    ):
        return False

    authoritative_text = (
        ast.unparse(
            authoritative
        )
    )

    reserve_text = (
        ast.unparse(
            reserve
        )
    )

    publish_text = (
        ast.unparse(
            publish
        )
    )

    write_text = (
        ast.unparse(
            write_partial
        )
    )

    retry_loop = any(
        isinstance(
            node,
            (
                ast.While,
                ast.For,
                ast.AsyncFor,
            ),
        )
        for node in ast.walk(
            authoritative
        )
    )

    recursive_call = False

    for node in ast.walk(
        authoritative
    ):
        if (
            isinstance(
                node,
                ast.Call,
            )
            and isinstance(
                node.func,
                ast.Name,
            )
            and node.func.id
            == "_authoritative_run"
        ):
            recursive_call = True

    prequal_index = (
        authoritative_text.find(
            "_full_prequalification()"
        )
    )

    reserve_index = (
        authoritative_text.find(
            "_reserve_partial()"
        )
    )

    science_index = (
        authoritative_text.find(
            "_run_scientific_evaluation"
        )
    )

    publish_index = (
        authoritative_text.find(
            "_publish_result()"
        )
    )

    ordering = (
        prequal_index >= 0
        and reserve_index
        > prequal_index
        and science_index
        > reserve_index
        and publish_index
        > science_index
    )

    exact_names = (
        RESULT_PATH.name
        == (
            "maf_query_to_pk_selection_"
            "validation_v1.json"
        )
        and PARTIAL_PATH.name
        == (
            "maf_query_to_pk_selection_"
            "validation_v1.json.partial"
        )
    )

    exclusive_reservation = (
        "os.O_EXCL"
        in reserve_text
        and "os.O_CREAT"
        in reserve_text
    )

    no_replace_publication = (
        "renameat2"
        in publish_text
        and "RENAME_NOREPLACE"
        in publish_text
        and "os.rename"
        not in publish_text
        and "os.replace"
        not in publish_text
    )

    durability = (
        "os.fsync"
        in write_text
        and "os.fsync"
        in publish_text
    )

    return (
        exact_names
        and exclusive_reservation
        and no_replace_publication
        and durability
        and ordering
        and not retry_loop
        and not recursive_call
    )


def _check_record(
    check_id,
    passed,
    detail,
):
    if check_id not in CHECK_IDS:
        raise RuntimeError(
            "unknown scientific check ID"
        )

    if type(passed) is not bool:
        raise RuntimeError(
            "check passed field "
            "must be bool"
        )

    if (
        not isinstance(
            detail,
            str,
        )
        or not detail
    ):
        raise RuntimeError(
            "check detail must be "
            "nonempty str"
        )

    return {
        "id":
            check_id,

        "passed":
            passed,

        "detail":
            detail,
    }


def _make_checks(
    prequalification,
    science,
    guard_qualification,
    *,
    dual_arm_satisfied,
    reservation_succeeded,
    matrix_after_reservation,
):
    fixture_bundle = (
        prequalification[
            "fixture"
        ]
    )

    authorities = (
        fixture_bundle[
            "authorities"
        ]
    )

    catalog_info = (
        fixture_bundle[
            "catalog"
        ]
    )

    fixture_info = (
        fixture_bundle[
            "fixture"
        ]
    )

    selector_static = (
        prequalification[
            "selector_static"
        ]
    )

    runner_static = (
        prequalification[
            "runner_static"
        ]
    )

    backend = (
        prequalification[
            "backend"
        ]
    )

    metrics = science[
        "metrics"
    ]

    catalog_document = (
        catalog_info[
            "catalog"
        ]
    )

    catalog_entries = (
        catalog_document[
            "entries"
        ]
    )

    object_pks = tuple(
        catalog_info[
            "object_pks"
        ]
    )

    query_ids = tuple(
        fixture_info[
            "query_ids"
        ]
    )

    all_authorities_bound = (
        authorities[
            "validation_protocol_sha256"
        ]
        == EXPECTED_VALIDATION_PROTOCOL_SHA256
        and authorities[
            "selection_protocol_sha256"
        ]
        == EXPECTED_SELECTION_PROTOCOL_SHA256
        and authorities[
            "implementation_sha256"
        ]
        == EXPECTED_IMPLEMENTATION_SHA256
        and authorities[
            "q1_verdict_sha256"
        ]
        == EXPECTED_Q1_VERDICT_SHA256
        and authorities[
            "catalog_sha256"
        ]
        == EXPECTED_CATALOG_SHA256
        and authorities[
            "query_fixture_sha256"
        ]
        == EXPECTED_QUERY_FIXTURE_SHA256
        and authorities[
            "source_manifest_sha256"
        ]
        == EXPECTED_SOURCE_MANIFEST_SHA256
    )

    guard_contract_pass = (
        guard_qualification[
            "guard_false"
        ]
        and guard_qualification[
            "environment_only"
        ]
        and guard_qualification[
            "cli_only"
        ]
        and guard_qualification[
            "fully_armed"
        ]
        and guard_qualification[
            "result_slot_unspent"
        ]
    )

    exact_boundary = (
        BOUNDARY_EXCLUSIONS
        == (
            "inference",
            "real-model answer generation",
            "route-cache reuse",
            "bounded expansion",
            "Query Capsule attach/detach lifecycle",
            "selective-working-set sufficiency",
            "object/tensor avoidance",
            "output parity",
            "answer quality",
            "MAF-native compute",
            "performance improvement",
            "network access",
        )
    )

    values = {
        "V01_q2_protocol_binding":
            (
                authorities[
                    "selection_protocol_sha256"
                ]
                == EXPECTED_SELECTION_PROTOCOL_SHA256
            ),

        "V02_selector_implementation_binding":
            (
                authorities[
                    "implementation_sha256"
                ]
                == EXPECTED_IMPLEMENTATION_SHA256
            ),

        "V03_q1_acceptance_verdict_binding":
            (
                authorities[
                    "q1_verdict_sha256"
                ]
                == EXPECTED_Q1_VERDICT_SHA256
            ),

        "V04_catalog_schema":
            (
                catalog_document[
                    "schema"
                ]
                == CATALOG_SCHEMA
            ),

        "V05_catalog_canonical_json":
            (
                catalog_info[
                    "catalog_sha256"
                ]
                == EXPECTED_CATALOG_SHA256
            ),

        "V06_catalog_generation_manifest_binding":
            (
                catalog_info[
                    "source_generation_pk"
                ]
                == EXPECTED_SOURCE_GENERATION_PK
                and catalog_info[
                    "source_manifest_sha256"
                ]
                == EXPECTED_SOURCE_MANIFEST_SHA256
            ),

        "V07_catalog_unique_sorted_object_pks":
            (
                object_pks
                == tuple(
                    sorted(
                        object_pks
                    )
                )
                and len(object_pks)
                == len(
                    set(object_pks)
                )
            ),

        "V08_catalog_static_metadata_surface_only":
            all(
                set(entry)
                == CATALOG_ENTRY_FIELDS
                for entry
                in catalog_entries
            ),

        "V09_selection_config_exact":
            (
                fixture_info[
                    "selection_config"
                ]
                == EXPECTED_CONFIG
                and fixture_info[
                    "selection_config_sha256"
                ]
                == EXPECTED_SELECTION_CONFIG_SHA256
            ),

        "V10_query_fixture_schema":
            (
                fixture_info[
                    "fixture"
                ][
                    "schema"
                ]
                == QUERY_FIXTURE_SCHEMA
            ),

        "V11_query_fixture_canonical_json":
            (
                authorities[
                    "query_fixture_sha256"
                ]
                == EXPECTED_QUERY_FIXTURE_SHA256
            ),

        "V12_evaluation_query_minimum":
            (
                metrics[
                    "evaluation_query_count"
                ]
                >= 32
            ),

        "V13_specific_query_minimum":
            (
                metrics[
                    "specific_intent_query_count"
                ]
                >= 16
            ),

        "V14_distinct_specific_target_minimum":
            (
                metrics[
                    "unique_expected_object_pk_count"
                ]
                >= 8
            ),

        "V15_fallback_control_minimum":
            (
                metrics[
                    "fallback_query_count"
                ]
                >= 4
            ),

        "V16_query_id_uniqueness_and_order":
            (
                len(query_ids)
                == len(
                    set(query_ids)
                )
                and query_ids
                == tuple(
                    sorted(
                        query_ids
                    )
                )
            ),

        "V17_query_class_semantics":
            (
                science[
                    "fallback_contract_pass"
                ]
                and science[
                    "supported_fallback_contract_pass"
                ]
            ),

        "V18_selector_api_non_oracle":
            selector_static[
                "api_non_oracle"
            ],

        "V19_no_route_cache_input":
            selector_static[
                "no_route_cache_input"
            ],

        "V20_no_bounded_expansion":
            selector_static[
                "no_bounded_expansion"
            ],

        "V21_no_inference_network_or_subprocess":
            (
                selector_static[
                    "no_inference_network_subprocess"
                ]
                and runner_static[
                    "no_subprocess"
                ]
            ),

        "V22_independent_target_predicate":
            runner_static[
                "independent_target_predicate"
            ],

        "V23_target_predicate_does_not_call_selector":
            runner_static[
                "target_predicate_no_selector"
            ],

        "V24_random_baseline_exact_seed_and_formula":
            _baseline_exact_contract_check(
                fixture_info,
                catalog_info,
            ),

        "V25_random_baseline_no_oracle_input":
            runner_static[
                "baseline_no_oracle"
            ],

        "V26_renameat2_backend_required":
            backend[
                "renameat2_available"
            ],

        "V27_rename_noreplace_exact_value":
            (
                RENAME_NOREPLACE == 1
                and backend[
                    "rename_noreplace_exact_value"
                ]
            ),

        "V28_no_os_link_publication":
            runner_static[
                "no_os_link"
            ],

        "V29_no_link_or_linkat_fallback":
            (
                runner_static[
                    "no_os_link"
                ]
                and runner_static[
                    "no_libc_link"
                ]
                and runner_static[
                    "no_libc_linkat"
                ]
            ),

        "V30_no_replace_or_plain_rename_fallback":
            (
                runner_static[
                    "no_plain_os_rename"
                ]
                and runner_static[
                    "no_os_replace"
                ]
            ),

        "V31_dual_arm_required":
            (
                dual_arm_satisfied
                is True
            ),

        "V32_guard_false_non_spending":
            guard_contract_pass,

        "V33_fixture_qualification_before_reservation":
            (
                prequalification[
                    "fixture_qualified_before_reservation"
                ]
                is True
            ),

        "V34_backend_qualification_before_reservation":
            (
                prequalification[
                    "backend_qualified_before_reservation"
                ]
                is True
            ),

        "V35_o_excl_partial_reservation":
            (
                reservation_succeeded
                is True
                and runner_static[
                    "o_excl_contract"
                ]
            ),

        "V36_matrix_after_reservation":
            (
                matrix_after_reservation
                is True
            ),

        "V37_no_replace_result_publication":
            (
                runner_static[
                    "renameat2_contract"
                ]
                and runner_static[
                    "no_plain_os_rename"
                ]
                and runner_static[
                    "no_os_replace"
                ]
                and runner_static[
                    "no_os_link"
                ]
                and runner_static[
                    "no_libc_link"
                ]
                and runner_static[
                    "no_libc_linkat"
                ]
            ),

        "V38_partial_file_fsync_before_publication":
            runner_static[
                "partial_fsync_contract"
            ],

        "V39_parent_directory_fsync_after_publication":
            (
                runner_static[
                    "parent_fsync_contract"
                ]
                and backend[
                    "directory_fsync"
                ]
            ),

        "V40_result_schema_and_canonical_json":
            (
                RESULT_SCHEMA
                == (
                    "openmind."
                    "maf_query_to_pk_selection_validation.v1"
                )
                and len(
                    RESULT_FIELDS
                )
                == 22
            ),

        "V41_result_authority_bindings":
            (
                all_authorities_bound
                and fixture_info[
                    "selection_config_sha256"
                ]
                == EXPECTED_SELECTION_CONFIG_SHA256
                and catalog_info[
                    "source_generation_pk"
                ]
                == EXPECTED_SOURCE_GENERATION_PK
                and science[
                    "selector_result_contract_pass"
                ]
            ),

        "V42_supported_intent_target_hit_threshold":
            (
                metrics[
                    "supported_intent_target_hit_rate"
                ]
                == 1.0
            ),

        "V43_supported_intent_precision_threshold":
            (
                metrics[
                    "supported_intent_precision"
                ]
                == 1.0
            ),

        "V44_specific_top1_threshold":
            (
                metrics[
                    "specific_intent_top1_accuracy"
                ]
                >= 0.95
            ),

        "V45_random_baseline_advantage_threshold":
            (
                metrics[
                    "selector_minus_baseline_top1_difference"
                ]
                >= 0.50
            ),

        "V46_budget_duplicate_and_binding_thresholds":
            (
                metrics[
                    "budget_violation_count"
                ]
                == 0
                and metrics[
                    "duplicate_selection_count"
                ]
                == 0
                and metrics[
                    "generation_binding_violation_count"
                ]
                == 0
                and metrics[
                    "manifest_binding_violation_count"
                ]
                == 0
                and metrics[
                    "oracle_input_violation_count"
                ]
                == 0
            ),

        "V47_boundary_exclusions":
            (
                exact_boundary
                and selector_static[
                    "no_route_cache_input"
                ]
                and selector_static[
                    "no_bounded_expansion"
                ]
                and selector_static[
                    "no_inference_network_subprocess"
                ]
                and runner_static[
                    "no_subprocess"
                ]
            ),

        "V48_exact_once_no_retry_contract":
            _exact_once_static_contract(),
    }

    if tuple(
        values.keys()
    ) != CHECK_IDS:
        raise RuntimeError(
            "V01-V48 value order mismatch"
        )

    records = tuple(
        _check_record(
            check_id,
            bool(
                values[
                    check_id
                ]
            ),
            (
                "PASS"
                if values[
                    check_id
                ]
                else "FAIL"
            ),
        )
        for check_id in CHECK_IDS
    )

    if (
        len(records)
        != EXPECTED_CHECK_COUNT
    ):
        raise RuntimeError(
            "scientific check count mismatch"
        )

    if tuple(
        record[
            "id"
        ]
        for record in records
    ) != CHECK_IDS:
        raise RuntimeError(
            "scientific check order mismatch"
        )

    return records


# OPENMIND_Q2_RUNNER_CHUNK_7_COMPLETE


def _empty_metrics():
    metrics = {
        "evaluation_query_count":
            0,

        "specific_intent_query_count":
            0,

        "unique_expected_object_pk_count":
            0,

        "metadata_eligible_query_count":
            0,

        "fallback_query_count":
            0,

        "mean_selected_candidate_count":
            0.0,

        "maximum_selected_candidate_count":
            0,

        "supported_intent_target_hit_rate":
            0.0,

        "supported_intent_precision":
            0.0,

        "specific_intent_top1_accuracy":
            0.0,

        "random_baseline_top1_accuracy":
            0.0,

        "selector_minus_baseline_top1_difference":
            0.0,

        "budget_violation_count":
            0,

        "duplicate_selection_count":
            0,

        "generation_binding_violation_count":
            0,

        "manifest_binding_violation_count":
            0,

        "oracle_input_violation_count":
            0,
    }

    if tuple(
        metrics.keys()
    ) != METRIC_FIELDS:
        raise RuntimeError(
            "empty metric schema mismatch"
        )

    return metrics


def _error_checks(
    error_text,
):
    if (
        not isinstance(
            error_text,
            str,
        )
        or not error_text
    ):
        raise RuntimeError(
            "error_text must be "
            "nonempty str"
        )

    records = tuple(
        _check_record(
            check_id,
            False,
            (
                "AUDITOR_ERROR: "
                + error_text
            ),
        )
        for check_id
        in CHECK_IDS
    )

    if (
        len(records)
        != EXPECTED_CHECK_COUNT
    ):
        raise RuntimeError(
            "error check count mismatch"
        )

    if tuple(
        record["id"]
        for record in records
    ) != CHECK_IDS:
        raise RuntimeError(
            "error check order mismatch"
        )

    return records


def _exact_once_result_record():
    return {
        "arm_environment_variable":
            ARM_ENV,

        "arm_environment_value":
            ARM_VALUE,

        "cli_arm_flag":
            ARM_FLAG,

        "dual_arm_required":
            True,

        "dual_arm_satisfied":
            True,

        "final_result_name":
            RESULT_PATH.name,

        "partial_result_name":
            PARTIAL_PATH.name,

        "partial_is_reservation_authority":
            True,

        "reservation_primitive":
            "os.open(O_WRONLY|O_CREAT|O_EXCL)",

        "automatic_retry":
            False,
    }


def _publication_backend_result_record(
    prequalification,
):
    if not isinstance(
        prequalification,
        dict,
    ):
        raise RuntimeError(
            "prequalification must be dict"
        )

    backend = prequalification[
        "backend"
    ]

    if (
        not isinstance(
            backend,
            dict,
        )
        or not all(
            backend.values()
        )
    ):
        raise RuntimeError(
            "publication backend "
            "was not qualified"
        )

    return {
        "primitive":
            "libc.renameat2",

        "flag":
            "RENAME_NOREPLACE",

        "flag_value":
            RENAME_NOREPLACE,

        "same_parent_directory_fd":
            True,

        "partial_fsync_before_publication":
            True,

        "parent_directory_fsync_after_publication":
            True,

        "fallback":
            None,

        "qualification":
            dict(
                backend
            ),
    }


def _build_result(
    checks,
    metrics,
    auditor_error,
    prequalification,
):
    if not isinstance(
        checks,
        (list, tuple),
    ):
        raise RuntimeError(
            "checks must be sequence"
        )

    checks = tuple(
        checks
    )

    if (
        len(checks)
        != EXPECTED_CHECK_COUNT
    ):
        raise RuntimeError(
            "result check count mismatch"
        )

    if tuple(
        record.get(
            "id"
        )
        for record in checks
    ) != CHECK_IDS:
        raise RuntimeError(
            "result check order mismatch"
        )

    for record in checks:
        if (
            not isinstance(
                record,
                dict,
            )
            or set(
                record.keys()
            )
            != {
                "id",
                "passed",
                "detail",
            }
        ):
            raise RuntimeError(
                "invalid result check record"
            )

        if (
            type(
                record[
                    "passed"
                ]
            )
            is not bool
        ):
            raise RuntimeError(
                "result check passed "
                "must be bool"
            )

        if (
            not isinstance(
                record[
                    "detail"
                ],
                str,
            )
            or not record[
                "detail"
            ]
        ):
            raise RuntimeError(
                "result check detail invalid"
            )

    if not isinstance(
        metrics,
        dict,
    ):
        raise RuntimeError(
            "metrics must be dict"
        )

    if tuple(
        metrics.keys()
    ) != METRIC_FIELDS:
        raise RuntimeError(
            "result metric schema mismatch"
        )

    if (
        auditor_error is not None
        and (
            not isinstance(
                auditor_error,
                str,
            )
            or not auditor_error
        )
    ):
        raise RuntimeError(
            "auditor_error must be "
            "null or nonempty str"
        )

    failed_checks = [
        record[
            "id"
        ]
        for record in checks
        if (
            record[
                "passed"
            ]
            is not True
        )
    ]

    all_pass = (
        auditor_error is None
        and not failed_checks
    )

    result = {
        "schema":
            RESULT_SCHEMA,

        "exact_once":
            _exact_once_result_record(),

        "validation_protocol_sha256":
            EXPECTED_VALIDATION_PROTOCOL_SHA256,

        "selection_protocol_sha256":
            EXPECTED_SELECTION_PROTOCOL_SHA256,

        "implementation_sha256":
            EXPECTED_IMPLEMENTATION_SHA256,

        "q1_verdict_sha256":
            EXPECTED_Q1_VERDICT_SHA256,

        "catalog_sha256":
            EXPECTED_CATALOG_SHA256,

        "query_fixture_sha256":
            EXPECTED_QUERY_FIXTURE_SHA256,

        "source_generation_pk":
            EXPECTED_SOURCE_GENERATION_PK,

        "source_manifest_sha256":
            EXPECTED_SOURCE_MANIFEST_SHA256,

        "selection_config_sha256":
            EXPECTED_SELECTION_CONFIG_SHA256,

        "random_baseline_seed":
            RANDOM_BASELINE_SEED,

        "expected_check_count":
            EXPECTED_CHECK_COUNT,

        "check_count":
            len(
                checks
            ),

        "checks":
            [
                dict(
                    record
                )
                for record
                in checks
            ],

        "failed_checks":
            failed_checks,

        "auditor_error":
            auditor_error,

        "all_pass":
            all_pass,

        "metrics":
            dict(
                metrics
            ),

        "acceptance_thresholds":
            dict(
                ACCEPTANCE_THRESHOLDS
            ),

        "boundary_exclusions":
            list(
                BOUNDARY_EXCLUSIONS
            ),

        "publication_backend":
            _publication_backend_result_record(
                prequalification
            ),
    }

    if tuple(
        result.keys()
    ) != RESULT_FIELDS:
        raise RuntimeError(
            "result top-level "
            "field schema mismatch"
        )

    if (
        len(result)
        != 22
    ):
        raise RuntimeError(
            "result top-level "
            "field count mismatch"
        )

    if (
        result[
            "schema"
        ]
        != RESULT_SCHEMA
    ):
        raise RuntimeError(
            "result schema mismatch"
        )

    if (
        result[
            "expected_check_count"
        ]
        != EXPECTED_CHECK_COUNT
        or result[
            "check_count"
        ]
        != EXPECTED_CHECK_COUNT
    ):
        raise RuntimeError(
            "result expected/check "
            "count mismatch"
        )

    if tuple(
        result[
            "metrics"
        ].keys()
    ) != METRIC_FIELDS:
        raise RuntimeError(
            "result metric keys changed"
        )

    if (
        result[
            "acceptance_thresholds"
        ]
        != ACCEPTANCE_THRESHOLDS
    ):
        raise RuntimeError(
            "result acceptance "
            "thresholds changed"
        )

    if tuple(
        result[
            "boundary_exclusions"
        ]
    ) != BOUNDARY_EXCLUSIONS:
        raise RuntimeError(
            "result boundary "
            "exclusions changed"
        )

    if (
        result[
            "all_pass"
        ]
        != (
            result[
                "auditor_error"
            ]
            is None
            and not result[
                "failed_checks"
            ]
        )
    ):
        raise RuntimeError(
            "result all_pass mismatch"
        )

    return result


def _canonical_result_bytes(
    result,
):
    if not isinstance(
        result,
        dict,
    ):
        raise RuntimeError(
            "result must be dict"
        )

    if tuple(
        result.keys()
    ) != RESULT_FIELDS:
        raise RuntimeError(
            "canonical result "
            "field schema mismatch"
        )

    body = canonical_json_bytes(
        result
    )

    raw = (
        body
        + b"\n"
    )

    if not raw.endswith(
        b"\n"
    ):
        raise RuntimeError(
            "result terminal newline missing"
        )

    if raw.endswith(
        b"\n\n"
    ):
        raise RuntimeError(
            "result has multiple "
            "terminal newlines"
        )

    parsed = json.loads(
        body.decode(
            "utf-8"
        )
    )

    if canonical_json_bytes(
        parsed
    ) != body:
        raise RuntimeError(
            "result canonicalization "
            "round-trip failed"
        )

    return raw


# OPENMIND_Q2_RUNNER_CHUNK_8_COMPLETE


def _reserve_partial():
    _assert_result_slot_unspent()

    partial_fd = os.open(
        PARTIAL_PATH,
        (
            os.O_WRONLY
            | os.O_CREAT
            | os.O_EXCL
        ),
        0o600,
    )

    return partial_fd


def _write_result_partial(
    partial_fd,
    result,
):
    if (
        type(partial_fd) is not int
        or partial_fd < 0
    ):
        raise RuntimeError(
            "partial_fd must be "
            "nonnegative plain integer"
        )

    raw = _canonical_result_bytes(
        result
    )

    view = memoryview(
        raw
    )

    while view:
        written = os.write(
            partial_fd,
            view,
        )

        if written <= 0:
            raise RuntimeError(
                "short authoritative "
                "result write"
            )

        view = view[
            written:
        ]

    # os.write is unbuffered at Python level.
    # fsync below establishes the required
    # pre-publication durability boundary.
    os.fsync(partial_fd)

    return raw


def _publish_result():
    if (
        PARTIAL_PATH.parent
        != RESULT_PATH.parent
    ):
        raise RuntimeError(
            "partial and final result "
            "must be same-directory siblings"
        )

    if (
        PARTIAL_PATH.name
        != (
            "maf_query_to_pk_selection_"
            "validation_v1.json.partial"
        )
    ):
        raise RuntimeError(
            "unexpected partial result name"
        )

    if (
        RESULT_PATH.name
        != (
            "maf_query_to_pk_selection_"
            "validation_v1.json"
        )
    ):
        raise RuntimeError(
            "unexpected final result name"
        )

    if not PARTIAL_PATH.is_file():
        raise RuntimeError(
            "reserved partial result missing"
        )

    renameat2 = (
        _load_renameat2()
    )

    parent_fd = os.open(
        RESULT_PATH.parent,
        (
            os.O_RDONLY
            | os.O_DIRECTORY
        ),
    )

    try:
        ctypes.set_errno(0)

        rc = renameat2(
            parent_fd,
            PARTIAL_PATH.name.encode(
                "utf-8"
            ),
            parent_fd,
            RESULT_PATH.name.encode(
                "utf-8"
            ),
            RENAME_NOREPLACE,
        )

        if rc != 0:
            value = ctypes.get_errno()

            raise OSError(
                value,
                os.strerror(value),
            )

        os.fsync(parent_fd)

    finally:
        os.close(
            parent_fd
        )

    if PARTIAL_PATH.exists():
        raise RuntimeError(
            "partial remained after "
            "successful publication"
        )

    if not RESULT_PATH.is_file():
        raise RuntimeError(
            "final result missing after "
            "successful publication"
        )


# OPENMIND_Q2_RUNNER_CHUNK_9_COMPLETE


def _classify_post_reservation_failure(
    exc,
):
    partial_present = (
        PARTIAL_PATH.is_file()
    )

    final_present = (
        RESULT_PATH.is_file()
    )

    partial_size = None
    partial_sha256 = None

    if partial_present:
        partial_size = (
            PARTIAL_PATH.stat().st_size
        )

        partial_sha256 = (
            file_sha256(
                PARTIAL_PATH
            )
        )

    classification = {
        "phase":
            "POST_RESERVATION_FAILURE",

        "slot_state":
            "SPENT",

        "automatic_retry":
            False,

        "partial_preserved":
            partial_present,

        "partial_path":
            str(
                PARTIAL_PATH
            ),

        "partial_size":
            partial_size,

        "partial_sha256":
            partial_sha256,

        "final_present":
            final_present,

        "exception_type":
            type(
                exc
            ).__name__,

        "exception":
            str(
                exc
            ),
    }

    print(
        "OPENMIND_Q2_EXACT_ONCE_FAILURE="
        + json.dumps(
            classification,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ),
        file=sys.stderr,
    )

    return classification


def _authoritative_run(
    *,
    dual_arm_satisfied,
):
    if (
        dual_arm_satisfied
        is not True
    ):
        raise RuntimeError(
            "authoritative run requires "
            "both exact-once arms"
        )

    _assert_result_slot_unspent()

    guard_qualification = (
        _qualify_guard_logic()
    )

    prequalification = (
        _full_prequalification()
    )

    _assert_result_slot_unspent()

    partial_fd = None
    reservation_succeeded = False

    try:
        partial_fd = (
            _reserve_partial()
        )

        reservation_succeeded = True

        science = (
            _run_scientific_evaluation(
                prequalification
            )
        )

        checks = (
            _make_checks(
                prequalification,
                science,
                guard_qualification,
                dual_arm_satisfied=(
                    dual_arm_satisfied
                ),
                reservation_succeeded=(
                    reservation_succeeded
                ),
                matrix_after_reservation=True,
            )
        )

        result = (
            _build_result(
                checks,
                science[
                    "metrics"
                ],
                None,
                prequalification,
            )
        )

        raw = (
            _write_result_partial(
                partial_fd,
                result,
            )
        )

        os.close(
            partial_fd
        )

        partial_fd = None

        _publish_result()

        return {
            "result":
                result,

            "result_bytes":
                raw,

            "result_sha256":
                hashlib.sha256(
                    raw
                ).hexdigest(),

            "result_path":
                str(
                    RESULT_PATH
                ),

            "all_pass":
                result[
                    "all_pass"
                ],
        }

    except BaseException as exc:
        if partial_fd is not None:
            try:
                os.close(
                    partial_fd
                )
            except OSError:
                pass

            partial_fd = None

        if reservation_succeeded:
            try:
                _classify_post_reservation_failure(
                    exc
                )
            except BaseException as classify_exc:
                print(
                    "OPENMIND_Q2_FAILURE_"
                    "CLASSIFICATION_ERROR="
                    + repr(
                        classify_exc
                    ),
                    file=sys.stderr,
                )

        raise


# OPENMIND_Q2_RUNNER_CHUNK_10_COMPLETE


def main():
    argv = tuple(
        sys.argv[1:]
    )

    valid_modes = (
        QUALIFY_BACKEND_FLAG,
        QUALIFY_FIXTURES_FLAG,
        READINESS_FLAG,
        ARM_FLAG,
    )

    if (
        len(argv) != 1
        or argv[0] not in valid_modes
    ):
        print(
            "usage: "
            "maf_query_to_pk_selection_validation_v1.py "
            "{"
            + QUALIFY_FIXTURES_FLAG
            + "|"
            + QUALIFY_BACKEND_FLAG
            + "|"
            + READINESS_FLAG
            + "|"
            + ARM_FLAG
            + "}",
            file=sys.stderr,
        )

        return 2

    mode = argv[0]

    if (
        mode
        == QUALIFY_FIXTURES_FLAG
    ):
        _print_qualification(
            "qualify-fixtures",
            _fixture_qualification_summary(),
        )

        return 0

    if (
        mode
        == QUALIFY_BACKEND_FLAG
    ):
        _print_qualification(
            "qualify-backend",
            _backend_qualification_summary(),
        )

        return 0

    if (
        mode
        == READINESS_FLAG
    ):
        _print_qualification(
            "readiness",
            _readiness_summary(),
        )

        return 0

    dual_arm_satisfied = (
        mode == ARM_FLAG
        and os.environ.get(
            ARM_ENV
        )
        == ARM_VALUE
    )

    if (
        dual_arm_satisfied
        is not True
    ):
        raise RuntimeError(
            "exact-once authoritative run requires "
            + ARM_FLAG
            + " and "
            + ARM_ENV
            + "="
            + ARM_VALUE
        )

    outcome = (
        _authoritative_run(
            dual_arm_satisfied=(
                dual_arm_satisfied
            )
        )
    )

    print(
        "MODE=run-exact-once"
    )

    print(
        "RESULT_PATH="
        + outcome[
            "result_path"
        ]
    )

    print(
        "RESULT_SHA256="
        + outcome[
            "result_sha256"
        ]
    )

    print(
        "ALL_PASS="
        + str(
            outcome[
                "all_pass"
            ]
        )
    )

    print(
        "FAILED_CHECKS="
        + json.dumps(
            outcome[
                "result"
            ][
                "failed_checks"
            ],
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
    )

    return (
        0
        if outcome[
            "all_pass"
        ]
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )


# OPENMIND_Q2_RUNNER_CHUNK_11_COMPLETE
