#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
from typing import Any, Callable


RESULT_SCHEMA = (
    "openmind.maf_query_capsule_data_model_validation.v1"
)

EXPECTED_CHECK_COUNT = 36

VALIDATION_PROTOCOL_SHA256 = (
    "6e77946c0e25a72052f4b4e6f9762b46fe1e141d9e5b03eecde1184d53ff78f9"
)

DATA_MODEL_PROTOCOL_SHA256 = (
    "5255a58c8c6340c251e24ae8543760fcd66a8deb8be1a8356ad5b78ad898edda"
)

IMPLEMENTATION_SHA256 = (
    "f897b97011714f3c84b7350c6bb53e800232be8a5d34e5148a3e50a81952976e"
)

CHECKPOINT_SHA256 = (
    "7fc64010695365b73058ca450c2c161e4f3aa3758347796c8bcca826f9bc886b"
)

ARM_ENV = (
    "OPENMIND_ARM_QUERY_CAPSULE_DATA_MODEL_VALIDATION_V1"
)

ARM_VALUE = "YES"

BASE = Path(__file__).resolve().parent

VALIDATION_PROTOCOL_PATH = (
    BASE
    / "MAF_QUERY_CAPSULE_DATA_MODEL_VALIDATION_V1_PROTOCOL.md"
)

DATA_PROTOCOL_PATH = (
    BASE
    / "MAF_QUERY_CAPSULE_DATA_MODEL_V1_PROTOCOL.md"
)

IMPLEMENTATION_PATH = (
    BASE
    / "maf_query_capsule_data_model_v1.py"
)

CHECKPOINT_PATH = (
    BASE
    / "MAF_PHASE_6E_ENTRY_CHECKPOINT.md"
)

RESULT_PATH = (
    BASE
    / "maf_query_capsule_data_model_validation_v1.json"
)

PARTIAL_PATH = Path(
    str(RESULT_PATH) + ".partial"
)


CHECK_MATRIX = (
    ("V01", "schema_constants"),
    ("V02", "field_inventory"),
    ("V03", "generation_pk_grammar"),
    ("V04", "object_pk_grammar"),
    ("V05", "query_pk_grammar"),
    ("V06", "query_pk_exact_derivation"),
    ("V07", "query_pk_generation_binding"),
    ("V08", "query_pk_manifest_binding"),
    ("V09", "query_pk_configuration_binding"),
    ("V10", "capsule_canonical_json"),
    ("V11", "capsule_round_trip"),
    ("V12", "ordered_sequence_preservation"),
    ("V13", "duplicate_initial_object_rejection"),
    ("V14", "duplicate_relationship_rejection"),
    ("V15", "route_order_permutation"),
    ("V16", "object_budget"),
    ("V17", "disabled_expansion_policy"),
    ("V18", "bounded_expansion_policy"),
    ("V19", "capsule_generation_mismatch"),
    ("V20", "capsule_manifest_mismatch"),
    ("V21", "sha256_validation"),
    ("V22", "capsule_unknown_field_rejection"),
    ("V23", "route_exact_cache_key"),
    ("V24", "duplicate_route_pk_rejection"),
    ("V25", "initial_additional_disjointness"),
    ("V26", "touched_subset"),
    ("V27", "selected_unused_derivation"),
    ("V28", "route_generation_mismatch"),
    ("V29", "validation_metadata_boundary"),
    ("V30", "route_unknown_field_rejection"),
    ("V31", "immutable_value_objects"),
    ("V32", "mutable_input_alias_isolation"),
    ("V33", "construction_failure_atomicity"),
    ("V34", "canonical_authority_untouched"),
    ("V35", "canonical_serialization_field_set"),
    ("V36", "scientific_boundary_exclusions"),
)


BOUNDARY_FLAGS = {
    "benchmark_executed": False,
    "inference_executed": False,
    "real_model_accessed": False,
    "route_cache_persistence_executed": False,
    "phase_6d_q2_executed": False,
    "phase_6e_executed": False,
    "network_accessed": False,
    "subprocess_launched": False,
}


def sha_file(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
            h.update(chunk)

    return h.hexdigest()


def h(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def verify_authorities() -> None:
    expected = (
        (
            VALIDATION_PROTOCOL_PATH,
            VALIDATION_PROTOCOL_SHA256,
            "validation protocol",
        ),
        (
            DATA_PROTOCOL_PATH,
            DATA_MODEL_PROTOCOL_SHA256,
            "data-model protocol",
        ),
        (
            IMPLEMENTATION_PATH,
            IMPLEMENTATION_SHA256,
            "implementation",
        ),
        (
            CHECKPOINT_PATH,
            CHECKPOINT_SHA256,
            "Phase 6E checkpoint",
        ),
    )

    for path, digest, label in expected:
        if not path.is_file():
            raise RuntimeError(
                f"{label} missing: {path}"
            )

        actual = sha_file(path)

        if actual != digest:
            raise RuntimeError(
                f"{label} SHA256 mismatch: "
                f"{actual} != {digest}"
            )


def authority_snapshot() -> dict[str, str]:
    return {
        str(VALIDATION_PROTOCOL_PATH):
            sha_file(VALIDATION_PROTOCOL_PATH),

        str(DATA_PROTOCOL_PATH):
            sha_file(DATA_PROTOCOL_PATH),

        str(IMPLEMENTATION_PATH):
            sha_file(IMPLEMENTATION_PATH),

        str(CHECKPOINT_PATH):
            sha_file(CHECKPOINT_PATH),
    }


def load_implementation():
    name = "_openmind_query_capsule_v1"

    spec = importlib.util.spec_from_file_location(
        name,
        IMPLEMENTATION_PATH,
    )

    if spec is None or spec.loader is None:
        raise RuntimeError(
            "cannot load frozen implementation"
        )

    module = importlib.util.module_from_spec(
        spec
    )

    sys.modules[name] = module

    spec.loader.exec_module(
        module
    )

    return module


def make_fixture(mod):
    generation = (
        "mafgen:v1:"
        + h(b"q1-validation-generation")
    )

    other_generation = (
        "mafgen:v1:"
        + h(b"q1-validation-other-generation")
    )

    manifest = h(
        b"q1-validation-manifest"
    )

    other_manifest = h(
        b"q1-validation-other-manifest"
    )

    config = h(
        b"q1-validation-selection-config"
    )

    other_config = h(
        b"q1-validation-other-config"
    )

    route_config = h(
        b"q1-validation-route-config"
    )

    exact_query = h(
        b"q1-validation-exact-query"
    )

    object_pks = tuple(
        "mafobj:v1:"
        + h(
            f"q1-validation-object-{i}".encode()
        )
        for i in range(1, 5)
    )

    signature = "validation-λ-signature-v1"

    query_pk = mod.derive_query_pk(
        query_signature=signature,
        selection_config_sha256=config,
        source_generation_pk=generation,
        source_manifest_sha256=manifest,
    )

    capsule = mod.MAFQueryCapsuleV1(
        schema=mod.QUERY_CAPSULE_SCHEMA,
        query_pk=query_pk,
        query_signature=signature,
        source_generation_pk=generation,
        source_manifest_sha256=manifest,
        initial_object_pks=(
            object_pks[0],
            object_pks[1],
        ),
        selected_relationship_pks=(
            "relationship:q1:a",
            "relationship:q1:b",
        ),
        route_order=(
            object_pks[1],
            object_pks[0],
        ),
        expansion_policy="disabled",
        max_object_budget=2,
        max_expansion_rounds=0,
        selection_config_sha256=config,
    )

    route = mod.MAFQueryRouteCacheEntryV1(
        schema=mod.QUERY_ROUTE_CACHE_ENTRY_SCHEMA,
        exact_query_sha256=exact_query,
        query_signature=signature,
        source_generation_pk=generation,
        initial_pk_route=(
            object_pks[0],
            object_pks[1],
        ),
        additional_pks=(
            object_pks[2],
        ),
        touched_pks=(
            object_pks[1],
            object_pks[2],
        ),
        selected_unused_pks=(
            object_pks[0],
        ),
        route_config_sha256=route_config,
        validation_metadata_sha256=None,
    )

    return {
        "mod": mod,
        "Error":
            mod.MAFQueryCapsuleDataModelError,

        "Capsule":
            mod.MAFQueryCapsuleV1,

        "Route":
            mod.MAFQueryRouteCacheEntryV1,

        "generation":
            generation,

        "other_generation":
            other_generation,

        "manifest":
            manifest,

        "other_manifest":
            other_manifest,

        "config":
            config,

        "other_config":
            other_config,

        "route_config":
            route_config,

        "exact_query":
            exact_query,

        "objects":
            object_pks,

        "signature":
            signature,

        "query_pk":
            query_pk,

        "capsule":
            capsule,

        "route":
            route,
    }


def qualify_fixture(mod) -> dict[str, Any]:
    ctx = make_fixture(mod)

    if not ctx["generation"].startswith(
        "mafgen:v1:"
    ):
        raise AssertionError(
            "fixture generation PK invalid"
        )

    if any(
        not pk.startswith("mafobj:v1:")
        for pk in ctx["objects"]
    ):
        raise AssertionError(
            "fixture object PK invalid"
        )

    if len(ctx["manifest"]) != 64:
        raise AssertionError(
            "fixture manifest SHA invalid"
        )

    if (
        ctx["capsule"].schema
        != mod.QUERY_CAPSULE_SCHEMA
    ):
        raise AssertionError(
            "fixture capsule invalid"
        )

    if (
        ctx["route"].schema
        != mod.QUERY_ROUTE_CACHE_ENTRY_SCHEMA
    ):
        raise AssertionError(
            "fixture route invalid"
        )

    return ctx


def expect_error(
    ctx,
    fn: Callable[[], Any],
    contains: str | None = None,
) -> None:
    Error = ctx["Error"]

    try:
        fn()
    except Error as exc:
        if (
            contains is not None
            and contains not in str(exc)
        ):
            raise AssertionError(
                f"wrong error message: {exc}"
            )
        return

    raise AssertionError(
        "expected data-model error"
    )


def capsule_kwargs(ctx) -> dict[str, Any]:
    c = ctx["capsule"]

    return {
        "schema": c.schema,
        "query_pk": c.query_pk,
        "query_signature": c.query_signature,
        "source_generation_pk":
            c.source_generation_pk,
        "source_manifest_sha256":
            c.source_manifest_sha256,
        "initial_object_pks":
            c.initial_object_pks,
        "selected_relationship_pks":
            c.selected_relationship_pks,
        "route_order":
            c.route_order,
        "expansion_policy":
            c.expansion_policy,
        "max_object_budget":
            c.max_object_budget,
        "max_expansion_rounds":
            c.max_expansion_rounds,
        "selection_config_sha256":
            c.selection_config_sha256,
    }


def route_kwargs(ctx) -> dict[str, Any]:
    r = ctx["route"]

    return {
        "schema": r.schema,
        "exact_query_sha256":
            r.exact_query_sha256,
        "query_signature":
            r.query_signature,
        "source_generation_pk":
            r.source_generation_pk,
        "initial_pk_route":
            r.initial_pk_route,
        "additional_pks":
            r.additional_pks,
        "touched_pks":
            r.touched_pks,
        "selected_unused_pks":
            r.selected_unused_pks,
        "route_config_sha256":
            r.route_config_sha256,
        "validation_metadata_sha256":
            r.validation_metadata_sha256,
    }


def execute_check(
    check_id: str,
    ctx,
) -> str:
    mod = ctx["mod"]
    Capsule = ctx["Capsule"]
    Route = ctx["Route"]

    o1, o2, o3, o4 = ctx["objects"]

    if check_id == "V01":
        assert (
            mod.QUERY_CAPSULE_SCHEMA
            == "openmind.maf_query_capsule.v1"
        )
        assert (
            mod.QUERY_ROUTE_CACHE_ENTRY_SCHEMA
            == "openmind.maf_query_route_cache_entry.v1"
        )

    elif check_id == "V02":
        assert tuple(
            Capsule.__dataclass_fields__
        ) == mod.CAPSULE_FIELDS

        assert tuple(
            Route.__dataclass_fields__
        ) == mod.ROUTE_CACHE_FIELDS

    elif check_id == "V03":
        mod.derive_query_pk(
            query_signature=ctx["signature"],
            selection_config_sha256=ctx["config"],
            source_generation_pk=ctx["generation"],
            source_manifest_sha256=ctx["manifest"],
        )

        for bad in (
            "mafgen:v1:" + "A" * 64,
            "mafgen:v2:" + "0" * 64,
            "mafgen:v1:" + "0" * 63,
        ):
            expect_error(
                ctx,
                lambda bad=bad:
                    mod.derive_query_pk(
                        query_signature=ctx["signature"],
                        selection_config_sha256=ctx["config"],
                        source_generation_pk=bad,
                        source_manifest_sha256=ctx["manifest"],
                    ),
            )

    elif check_id == "V04":
        for bad in (
            "mafobj:v1:" + "A" * 64,
            "mafobj:v2:" + "0" * 64,
            "mafobj:v1:" + "0" * 63,
        ):
            kw = capsule_kwargs(ctx)
            kw["initial_object_pks"] = (bad,)
            kw["route_order"] = (bad,)
            kw["max_object_budget"] = 1

            expect_error(
                ctx,
                lambda kw=kw: Capsule(**kw),
            )

    elif check_id == "V05":
        kw = capsule_kwargs(ctx)
        kw["query_pk"] = (
            "mafquery:v1:"
            + "A" * 64
        )

        expect_error(
            ctx,
            lambda: Capsule(**kw),
            "invalid mafquery:v1 grammar",
        )

    elif check_id == "V06":
        identity = {
            "query_signature":
                ctx["signature"],

            "selection_config_sha256":
                ctx["config"],

            "source_generation_pk":
                ctx["generation"],

            "source_manifest_sha256":
                ctx["manifest"],
        }

        expected = (
            "mafquery:v1:"
            + hashlib.sha256(
                canonical_bytes(identity)
            ).hexdigest()
        )

        assert ctx["query_pk"] == expected

    elif check_id == "V07":
        changed = mod.derive_query_pk(
            query_signature=ctx["signature"],
            selection_config_sha256=ctx["config"],
            source_generation_pk=ctx["other_generation"],
            source_manifest_sha256=ctx["manifest"],
        )

        assert changed != ctx["query_pk"]

    elif check_id == "V08":
        changed = mod.derive_query_pk(
            query_signature=ctx["signature"],
            selection_config_sha256=ctx["config"],
            source_generation_pk=ctx["generation"],
            source_manifest_sha256=ctx["other_manifest"],
        )

        assert changed != ctx["query_pk"]

    elif check_id == "V09":
        changed = mod.derive_query_pk(
            query_signature=ctx["signature"],
            selection_config_sha256=ctx["other_config"],
            source_generation_pk=ctx["generation"],
            source_manifest_sha256=ctx["manifest"],
        )

        assert changed != ctx["query_pk"]

    elif check_id == "V10":
        c = ctx["capsule"]

        manual = {
            "schema": c.schema,
            "query_pk": c.query_pk,
            "query_signature": c.query_signature,
            "source_generation_pk":
                c.source_generation_pk,
            "source_manifest_sha256":
                c.source_manifest_sha256,
            "initial_object_pks":
                list(c.initial_object_pks),
            "selected_relationship_pks":
                list(c.selected_relationship_pks),
            "route_order":
                list(c.route_order),
            "expansion_policy":
                c.expansion_policy,
            "max_object_budget":
                c.max_object_budget,
            "max_expansion_rounds":
                c.max_expansion_rounds,
            "selection_config_sha256":
                c.selection_config_sha256,
        }

        assert (
            c.canonical_bytes()
            == canonical_bytes(manual)
        )

    elif check_id == "V11":
        c = ctx["capsule"]

        assert (
            Capsule.from_json_bytes(
                c.canonical_bytes()
            )
            == c
        )

    elif check_id == "V12":
        c = ctx["capsule"]

        assert c.initial_object_pks == (
            o1,
            o2,
        )

        assert (
            c.selected_relationship_pks
            == (
                "relationship:q1:a",
                "relationship:q1:b",
            )
        )

        assert c.route_order == (
            o2,
            o1,
        )

    elif check_id == "V13":
        kw = capsule_kwargs(ctx)
        kw["initial_object_pks"] = (
            o1,
            o1,
        )
        kw["route_order"] = (
            o1,
            o1,
        )

        expect_error(
            ctx,
            lambda: Capsule(**kw),
        )

    elif check_id == "V14":
        kw = capsule_kwargs(ctx)
        kw["selected_relationship_pks"] = (
            "relationship:q1:a",
            "relationship:q1:a",
        )

        expect_error(
            ctx,
            lambda: Capsule(**kw),
        )

    elif check_id == "V15":
        kw = capsule_kwargs(ctx)
        kw["route_order"] = (
            o1,
            o3,
        )

        expect_error(
            ctx,
            lambda: Capsule(**kw),
            "exact permutation",
        )

    elif check_id == "V16":
        kw = capsule_kwargs(ctx)
        kw["max_object_budget"] = 1

        expect_error(
            ctx,
            lambda: Capsule(**kw),
            "max_object_budget",
        )

    elif check_id == "V17":
        kw = capsule_kwargs(ctx)
        kw["max_expansion_rounds"] = 1

        expect_error(
            ctx,
            lambda: Capsule(**kw),
        )

    elif check_id == "V18":
        kw = capsule_kwargs(ctx)
        kw["expansion_policy"] = "bounded_v1"
        kw["max_expansion_rounds"] = 1

        valid = Capsule(**kw)

        assert valid.max_expansion_rounds == 1

        kw["max_expansion_rounds"] = 0

        expect_error(
            ctx,
            lambda: Capsule(**kw),
        )

    elif check_id == "V19":
        expect_error(
            ctx,
            lambda:
                ctx["capsule"].require_source_binding(
                    source_generation_pk=
                        ctx["other_generation"],
                    source_manifest_sha256=
                        ctx["manifest"],
                ),
            "generation mismatch",
        )

    elif check_id == "V20":
        expect_error(
            ctx,
            lambda:
                ctx["capsule"].require_source_binding(
                    source_generation_pk=
                        ctx["generation"],
                    source_manifest_sha256=
                        ctx["other_manifest"],
                ),
            "manifest mismatch",
        )

    elif check_id == "V21":
        bad_values = (
            "",
            "A" * 64,
            "sha256:" + "0" * 64,
            "0" * 63,
            "g" * 64,
        )

        for bad in bad_values:
            expect_error(
                ctx,
                lambda bad=bad:
                    mod.derive_query_pk(
                        query_signature=ctx["signature"],
                        selection_config_sha256=bad,
                        source_generation_pk=ctx["generation"],
                        source_manifest_sha256=ctx["manifest"],
                    ),
            )

            expect_error(
                ctx,
                lambda bad=bad:
                    mod.derive_query_pk(
                        query_signature=ctx["signature"],
                        selection_config_sha256=ctx["config"],
                        source_generation_pk=ctx["generation"],
                        source_manifest_sha256=bad,
                    ),
            )

            kw = route_kwargs(ctx)
            kw["exact_query_sha256"] = bad

            expect_error(
                ctx,
                lambda kw=kw: Route(**kw),
            )

            kw = route_kwargs(ctx)
            kw["route_config_sha256"] = bad

            expect_error(
                ctx,
                lambda kw=kw: Route(**kw),
            )

            kw = route_kwargs(ctx)
            kw["validation_metadata_sha256"] = bad

            expect_error(
                ctx,
                lambda kw=kw: Route(**kw),
            )

    elif check_id == "V22":
        value = ctx["capsule"].to_dict()
        value["unknown_v1_field"] = True

        expect_error(
            ctx,
            lambda:
                Capsule.from_mapping(value),
        )

    elif check_id == "V23":
        assert ctx["route"].exact_cache_key == (
            ctx["generation"],
            ctx["exact_query"],
            ctx["route_config"],
        )

    elif check_id == "V24":
        cases = []

        kw = route_kwargs(ctx)
        kw["initial_pk_route"] = (
            o1,
            o1,
        )
        cases.append(kw)

        kw = route_kwargs(ctx)
        kw["additional_pks"] = (
            o3,
            o3,
        )
        cases.append(kw)

        kw = route_kwargs(ctx)
        kw["touched_pks"] = (
            o2,
            o2,
        )
        cases.append(kw)

        kw = route_kwargs(ctx)
        kw["selected_unused_pks"] = (
            o1,
            o1,
        )
        cases.append(kw)

        for kw in cases:
            expect_error(
                ctx,
                lambda kw=kw: Route(**kw),
            )

    elif check_id == "V25":
        kw = route_kwargs(ctx)
        kw["additional_pks"] = (
            o1,
        )

        expect_error(
            ctx,
            lambda: Route(**kw),
            "disjoint",
        )

    elif check_id == "V26":
        kw = route_kwargs(ctx)
        kw["touched_pks"] = (
            o4,
        )

        expect_error(
            ctx,
            lambda: Route(**kw),
            "subset",
        )

    elif check_id == "V27":
        kw = route_kwargs(ctx)
        kw["touched_pks"] = (
            o2,
        )
        kw["selected_unused_pks"] = (
            o3,
            o1,
        )

        expect_error(
            ctx,
            lambda: Route(**kw),
            "selected-minus-touched",
        )

    elif check_id == "V28":
        expect_error(
            ctx,
            lambda:
                ctx["route"].require_source_generation(
                    ctx["other_generation"]
                ),
            "generation mismatch",
        )

    elif check_id == "V29":
        assert (
            ctx["route"].validation_metadata_sha256
            is None
        )

    elif check_id == "V30":
        value = ctx["route"].to_dict()
        value["unknown_v1_field"] = True

        expect_error(
            ctx,
            lambda:
                Route.from_mapping(value),
        )

    elif check_id == "V31":
        frozen_count = 0

        try:
            ctx["capsule"].query_signature = "mutated"
        except (
            AttributeError,
            TypeError,
        ):
            frozen_count += 1

        try:
            ctx["route"].query_signature = "mutated"
        except (
            AttributeError,
            TypeError,
        ):
            frozen_count += 1

        assert frozen_count == 2

    elif check_id == "V32":
        initial = [
            o1,
            o2,
        ]
        relationships = [
            "relationship:q1:a",
        ]
        order = [
            o2,
            o1,
        ]

        c = Capsule(
            schema=mod.QUERY_CAPSULE_SCHEMA,
            query_pk=ctx["query_pk"],
            query_signature=ctx["signature"],
            source_generation_pk=ctx["generation"],
            source_manifest_sha256=ctx["manifest"],
            initial_object_pks=initial,
            selected_relationship_pks=relationships,
            route_order=order,
            expansion_policy="disabled",
            max_object_budget=2,
            max_expansion_rounds=0,
            selection_config_sha256=ctx["config"],
        )

        initial.append(o3)
        relationships.append(
            "relationship:q1:b"
        )
        order.append(o3)

        assert c.initial_object_pks == (
            o1,
            o2,
        )

        ri = [o1, o2]
        ra = [o3]
        rt = [o2]
        ru = [o1, o3]

        r = Route(
            schema=mod.QUERY_ROUTE_CACHE_ENTRY_SCHEMA,
            exact_query_sha256=ctx["exact_query"],
            query_signature=ctx["signature"],
            source_generation_pk=ctx["generation"],
            initial_pk_route=ri,
            additional_pks=ra,
            touched_pks=rt,
            selected_unused_pks=ru,
            route_config_sha256=ctx["route_config"],
            validation_metadata_sha256=None,
        )

        ri.clear()
        ra.clear()
        rt.clear()
        ru.clear()

        assert r.initial_pk_route == (
            o1,
            o2,
        )

        assert r.additional_pks == (
            o3,
        )

    elif check_id == "V33":
        c_before = (
            ctx["capsule"].canonical_bytes()
        )

        r_before = (
            ctx["route"].canonical_bytes()
        )

        kw = capsule_kwargs(ctx)
        kw["initial_object_pks"] = (
            o1,
            o1,
        )
        kw["route_order"] = (
            o1,
            o1,
        )

        expect_error(
            ctx,
            lambda: Capsule(**kw),
        )

        kw = route_kwargs(ctx)
        kw["touched_pks"] = (
            o4,
        )

        expect_error(
            ctx,
            lambda: Route(**kw),
        )

        assert (
            ctx["capsule"].canonical_bytes()
            == c_before
        )

        assert (
            ctx["route"].canonical_bytes()
            == r_before
        )

    elif check_id == "V34":
        assert (
            authority_snapshot()
            == ctx["authority_before"]
        )

    elif check_id == "V35":
        c = json.loads(
            ctx["capsule"].canonical_bytes().decode(
                "utf-8"
            )
        )

        r = json.loads(
            ctx["route"].canonical_bytes().decode(
                "utf-8"
            )
        )

        assert set(c) == set(
            mod.CAPSULE_FIELDS
        )

        assert set(r) == set(
            mod.ROUTE_CACHE_FIELDS
        )

        assert isinstance(
            c["initial_object_pks"],
            list,
        )

        assert isinstance(
            r["initial_pk_route"],
            list,
        )

    elif check_id == "V36":
        assert all(
            value is False
            for value in BOUNDARY_FLAGS.values()
        )

    else:
        raise AssertionError(
            f"unknown check ID: {check_id}"
        )

    return "PASS"


def run_matrix(ctx) -> list[dict[str, Any]]:
    rows = []

    for check_id, name in CHECK_MATRIX:
        try:
            details = execute_check(
                check_id,
                ctx,
            )

            rows.append(
                {
                    "id": check_id,
                    "name": name,
                    "passed": True,
                    "details": details,
                }
            )

        except Exception as exc:
            rows.append(
                {
                    "id": check_id,
                    "name": name,
                    "passed": False,
                    "details": (
                        f"{type(exc).__name__}: {exc}"
                    ),
                }
            )

    return rows


def reserve_slot() -> int:
    if RESULT_PATH.exists():
        raise RuntimeError(
            "authoritative result already exists"
        )

    if PARTIAL_PATH.exists():
        raise RuntimeError(
            "exact-once reservation already exists"
        )

    return os.open(
        PARTIAL_PATH,
        os.O_WRONLY
        | os.O_CREAT
        | os.O_EXCL,
        0o600,
    )


def make_result(
    *,
    checks: list[dict[str, Any]],
    auditor_error: dict[str, str] | None,
) -> dict[str, Any]:
    failed = [
        row["id"]
        for row in checks
        if not row["passed"]
    ]

    result = {
        "schema":
            RESULT_SCHEMA,

        "exact_once":
            True,

        "runner_sha256":
            sha_file(
                Path(__file__).resolve()
            ),

        "validation_protocol_sha256":
            VALIDATION_PROTOCOL_SHA256,

        "data_model_protocol_sha256":
            DATA_MODEL_PROTOCOL_SHA256,

        "implementation_sha256":
            IMPLEMENTATION_SHA256,

        "expected_check_count":
            EXPECTED_CHECK_COUNT,

        "check_count":
            len(checks),

        "all_pass":
            (
                auditor_error is None
                and len(checks)
                    == EXPECTED_CHECK_COUNT
                and not failed
            ),

        "failed_checks":
            failed,

        "checks":
            checks,

        "auditor_error":
            auditor_error,
    }

    result.update(
        BOUNDARY_FLAGS
    )

    return result


def publish_result(
    fd: int,
    result: dict[str, Any],
) -> None:
    raw = (
        json.dumps(
            result,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
        + "\n"
    ).encode("utf-8")

    with os.fdopen(
        fd,
        "wb",
        closefd=True,
    ) as f:
        f.write(raw)
        f.flush()
        os.fsync(
            f.fileno()
        )

    os.link(
        PARTIAL_PATH,
        RESULT_PATH,
    )

    os.unlink(
        PARTIAL_PATH
    )

    directory_fd = os.open(
        BASE,
        os.O_RDONLY,
    )

    try:
        os.fsync(
            directory_fd
        )
    finally:
        os.close(
            directory_fd
        )


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()

    p.add_argument(
        "--guard-false",
        action="store_true",
    )

    p.add_argument(
        "--qualify-fixture",
        action="store_true",
    )

    p.add_argument(
        "--arm-exact-once",
        action="store_true",
    )

    return p


def main() -> int:
    args = parser().parse_args()

    # Highest-precedence inert mode.
    if args.guard_false:
        print(
            "STATUS=VALIDATION_V1_GUARD_FALSE_PASS"
        )
        print(
            "SCIENTIFIC_VALIDATION_EXECUTED=False"
        )
        print(
            "RESULT_SLOT=UNSPENT"
        )
        return 0

    # Non-spending fixture qualification.
    if args.qualify_fixture:
        verify_authorities()

        mod = load_implementation()

        ctx = qualify_fixture(
            mod
        )

        if RESULT_PATH.exists():
            raise RuntimeError(
                "result exists during qualification"
            )

        if PARTIAL_PATH.exists():
            raise RuntimeError(
                "partial exists during qualification"
            )

        print(
            "STATUS=VALIDATION_V1_FIXTURE_QUALIFICATION_PASS"
        )
        print(
            "CAPSULE_SCHEMA="
            + ctx["capsule"].schema
        )
        print(
            "ROUTE_SCHEMA="
            + ctx["route"].schema
        )
        print(
            "SCIENTIFIC_VALIDATION_EXECUTED=False"
        )
        print(
            "RESULT_SLOT=UNSPENT"
        )
        return 0

    armed = (
        args.arm_exact_once
        and os.environ.get(
            ARM_ENV
        ) == ARM_VALUE
    )

    if not armed:
        print(
            "STATUS=VALIDATION_V1_NOT_ARMED"
        )
        print(
            "SCIENTIFIC_VALIDATION_EXECUTED=False"
        )
        print(
            "RESULT_SLOT=UNSPENT"
        )
        return 2

    # Exact-once order:
    # dual arm -> clean namespace -> frozen authorities
    # -> fixture qualification -> O_EXCL reservation
    # -> V01-V36 -> authoritative publication.

    if RESULT_PATH.exists():
        raise RuntimeError(
            "authoritative result already exists"
        )

    if PARTIAL_PATH.exists():
        raise RuntimeError(
            "exact-once slot already reserved/spent"
        )

    verify_authorities()

    mod = load_implementation()

    qualify_fixture(
        mod
    )

    fd = reserve_slot()

    checks: list[dict[str, Any]] = []
    auditor_error = None

    try:
        ctx = make_fixture(
            mod
        )

        ctx["authority_before"] = (
            authority_snapshot()
        )

        checks = run_matrix(
            ctx
        )

    except BaseException as exc:
        auditor_error = {
            "type":
                type(exc).__name__,

            "message":
                str(exc),
        }

    result = make_result(
        checks=checks,
        auditor_error=auditor_error,
    )

    publish_result(
        fd,
        result,
    )

    print(
        "OPENMIND / QUERY CAPSULE DATA MODEL VALIDATION V1"
    )

    print(
        f"all_pass:    {result['all_pass']}"
    )

    print(
        f"check_count: {result['check_count']}"
    )

    print(
        "failed:      "
        + (
            ",".join(
                result["failed_checks"]
            )
            if result["failed_checks"]
            else "NONE"
        )
    )

    print(
        f"auditor_error: {result['auditor_error']}"
    )

    print(
        f"result:      {RESULT_PATH}"
    )

    return (
        0
        if result["all_pass"]
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
