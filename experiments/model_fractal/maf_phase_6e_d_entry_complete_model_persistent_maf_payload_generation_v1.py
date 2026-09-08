#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import inspect
import json
from pathlib import Path
from typing import Any

import maf_generation_engine_v1 as generation_engine
import maf_object_v1 as object_engine
import maf_segment_builder_v1 as segment_builder


ROOT = Path(__file__).resolve().parents[2]

SOURCE = Path.home() / "qwen2.5-coder-q8_0.gguf"

INVENTORY = (
    ROOT
    / "experiments/model_fractal/"
    "gguf_tensor_inventory_v1.json"
)

FULL_IDENTITY = (
    ROOT
    / "experiments/model_fractal/"
    "maf_full_model_identity_validation_v1.json"
)

PROTOCOL = (
    ROOT
    / "experiments/model_fractal/"
    "MAF_PHASE_6E_D_ENTRY_COMPLETE_MODEL_PERSISTENT_"
    "MAF_PAYLOAD_GENERATION_CONSTRUCTION_PROTOCOL_V1.md"
)

OBJECT_API = (
    ROOT
    / "experiments/model_fractal/"
    "maf_object_v1.py"
)

SEGMENT_BUILDER = (
    ROOT
    / "experiments/model_fractal/"
    "maf_segment_builder_v1.py"
)

GENERATION_ENGINE = (
    ROOT
    / "experiments/model_fractal/"
    "maf_generation_engine_v1.py"
)

COMPILE_RECIPE_VALIDATION = Path(
    "experiments/model_fractal/"
    "maf_compile_recipe_validation_v1.json"
)

EXPECTED_COMPILE_RECIPE_SHA256 = (
    "ceed863754a119fc59b6fdeb80b9a6d1766bfa47e33992315536669f58331ccd"
)

FULL_REPRESENTATION = Path(
    "experiments/model_fractal/"
    "maf_representation_v1.json"
)

EXPECTED_FULL_REPRESENTATION_SHA256 = (
    "0e70bc32fb76945d7c684b3d73d5598f587fd17c6bda77b32db3e601af3f8dbe"
)

RUNTIME_PARENT = (
    ROOT
    / "results/runtime"
)

FINAL_RUNTIME = (
    RUNTIME_PARENT
    / "maf_full_model_persistent_generation_v1"
)

BUILDING_RUNTIME = (
    RUNTIME_PARENT
    / "maf_full_model_persistent_generation_v1.building"
)

OBJECTS_DIR = (
    BUILDING_RUNTIME
    / "objects"
)

SEGMENT_PATH = (
    BUILDING_RUNTIME
    / "segment_00000000.mafseg"
)

SEGMENT_MANIFEST_PATH = (
    BUILDING_RUNTIME
    / "segment_00000000.manifest.json"
)

GENERATION_MANIFEST_PATH = (
    BUILDING_RUNTIME
    / "generation.manifest.json"
)

RESULT_PATH = (
    BUILDING_RUNTIME
    / "construction_result.json"
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

EXPECTED_TENSOR_COUNT = 339

EXPECTED_INVENTORY_SHA256 = (
    "7acf6d5dc672182aee0244b1bb85a4746"
    "6f33dbdcdf10bde863e24f3659240ee"
)

EXPECTED_FULL_IDENTITY_SHA256 = (
    "ef954f38e16ccbc73211c503d7d9c9b8"
    "462028d6222fb32fb9b15eb59615d25d"
)

EXPECTED_PROTOCOL_SHA256 = (
    "f599a652ae88bcf7ae193bdc26e42fdde"
    "89b6bef21a98012a061e55bb48919bb"
)

EXPECTED_OBJECT_API_SHA256 = (
    "eed6cbd96995412a632883f3c534f9023"
    "e7711ea8eb437afe35a48312502f63b"
)

EXPECTED_SEGMENT_BUILDER_SHA256 = (
    "f063c87989f9a646497743034e85d3f46"
    "74a7b45cf88df754b669d6621cc28f0"
)

EXPECTED_GENERATION_ENGINE_SHA256 = (
    "8868c58e98084226dd957391e1a2f4d1"
    "122e886607640ae0be59279f025f1a51"
)

OBJECT_WRITER_NAME = "compile_object"
SEGMENT_WRITER_NAME = "build_segment"
GENERATION_WRITER_NAME = "build_generation"

CHUNK_BYTES = 4 * 1024 * 1024


class ConstructionError(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ConstructionError(message)


def sha256_file(
    path: Path,
    chunk_bytes: int = CHUNK_BYTES,
) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        while True:
            block = handle.read(chunk_bytes)

            if not block:
                break

            digest.update(block)

    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    need(
        isinstance(value, dict),
        "JSON root must be object: " + str(path),
    )

    return value


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


def safe_tensor_filename(
    ordinal: int,
    name: str,
) -> str:
    normalized = "".join(
        character
        if (
            character.isalnum()
            or character in "._-"
        )
        else "_"
        for character in name
    )

    return (
        str(ordinal).zfill(3)
        + "_"
        + normalized
        + ".maf"
    )


def identity_object_pk(
    row: dict[str, Any],
) -> str:
    value = row.get("pk")

    if value is None:
        value = row.get("object_pk")

    need(
        isinstance(value, str)
        and value.startswith("mafobj:v1:"),
        "invalid frozen object PK",
    )

    return value


def resolve_file_start(
    tensor: dict[str, Any],
    inventory: dict[str, Any],
) -> int:
    direct = tensor.get("file_start")

    if direct is not None:
        return int(direct)

    source = inventory.get(
        "source",
        {},
    )

    need(
        isinstance(source, dict),
        "inventory source record invalid",
    )

    data_offset = source.get(
        "data_offset"
    )

    if data_offset is None:
        data_offset = inventory.get(
            "data_offset"
        )

    need(
        data_offset is not None,
        "cannot resolve GGUF data offset",
    )

    need(
        "offset" in tensor,
        "tensor offset missing",
    )

    return (
        int(data_offset)
        + int(tensor["offset"])
    )


def invoke_bound(
    function: Any,
    semantics: dict[str, Any],
    label: str,
) -> Any:
    signature = inspect.signature(
        function
    )

    kwargs: dict[str, Any] = {}

    for name, parameter in (
        signature.parameters.items()
    ):
        if (
            parameter.kind
            == inspect.Parameter.POSITIONAL_ONLY
        ):
            raise ConstructionError(
                label
                + " exposes unsupported positional-only parameter: "
                + name
            )

        if name in semantics:
            kwargs[name] = semantics[name]
            continue

        if parameter.default is not inspect.Parameter.empty:
            continue

        if parameter.kind in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        ):
            continue

        raise ConstructionError(
            label
            + " has unmapped required parameter: "
            + name
        )

    return function(
        **kwargs
    )


def extract_object_pks(
    value: Any,
) -> set[str]:
    output: set[str] = set()

    if isinstance(value, dict):
        for key, child in value.items():
            if (
                key in (
                    "object_pk",
                    "pk",
                )
                and isinstance(child, str)
                and child.startswith(
                    "mafobj:v1:"
                )
            ):
                output.add(child)

            output.update(
                extract_object_pks(
                    child
                )
            )

    elif isinstance(value, list):
        for child in value:
            output.update(
                extract_object_pks(
                    child
                )
            )

    return output


def strong_locator_pks(
    value: Any,
) -> set[str]:
    output: set[str] = set()

    if isinstance(value, dict):
        pk = value.get(
            "object_pk"
        )

        segment_id = value.get(
            "segment_id"
        )

        offset = value.get(
            "offset"
        )

        length = value.get(
            "length"
        )

        if length is None:
            length = value.get(
                "segment_length"
            )

        if (
            isinstance(pk, str)
            and pk.startswith("mafobj:v1:")
            and isinstance(segment_id, str)
            and segment_id
            and type(offset) is int
            and offset >= 0
            and type(length) is int
            and length > 0
        ):
            output.add(pk)

        for child in value.values():
            output.update(
                strong_locator_pks(
                    child
                )
            )

    elif isinstance(value, list):
        for child in value:
            output.update(
                strong_locator_pks(
                    child
                )
            )

    return output


def inspect_serialized_object_bytes(
    object_module: Any,
    serialized: bytes,
) -> dict[str, Any]:
    need(
        type(
            serialized
        ) is bytes,
        "serialized readback must be bytes",
    )

    header_size = int(
        object_module.HEADER_SIZE
    )

    need(
        len(
            serialized
        ) >= header_size,
        "serialized readback shorter than object header",
    )

    header = object_module.unpack_header(
        serialized[
            :header_size
        ]
    )

    metadata_start = header_size
    metadata_end = (
        metadata_start
        + int(
            header[
                "metadata_length"
            ]
        )
    )

    payload_end = (
        metadata_end
        + int(
            header[
                "payload_length"
            ]
        )
    )

    need(
        metadata_end >= metadata_start
        and payload_end >= metadata_end
        and payload_end
        == len(
            serialized
        ),
        "serialized object range / trailing-byte mismatch",
    )

    metadata_raw = serialized[
        metadata_start:
        metadata_end
    ]

    need(
        hashlib.sha256(
            metadata_raw
        ).hexdigest()
        == header[
            "metadata_sha256"
        ],
        "serialized metadata SHA mismatch",
    )

    try:
        metadata = json.loads(
            metadata_raw.decode(
                "utf-8"
            )
        )
    except Exception as exc:
        raise ConstructionError(
            "serialized metadata JSON invalid"
        ) from exc

    need(
        isinstance(
            metadata,
            dict,
        ),
        "serialized metadata root invalid",
    )

    need(
        object_module.canonical_json_bytes(
            metadata
        ) == metadata_raw,
        "serialized metadata is not canonical",
    )

    object_module.validate_metadata(
        metadata,
        header,
    )

    payload_view = memoryview(
        serialized
    )[
        metadata_end:
        payload_end
    ]

    payload_sha256 = hashlib.sha256(
        payload_view
    ).hexdigest()

    need(
        payload_sha256
        == header[
            "payload_sha256"
        ],
        "serialized payload SHA mismatch",
    )

    return {
        "tensor_name": metadata[
            "tensor_name"
        ],
        "tensor_type": metadata[
            "tensor_type"
        ],
        "dims": tuple(
            metadata[
                "dims"
            ]
        ),
        "payload_length": int(
            header[
                "payload_length"
            ]
        ),
        "payload_sha256": payload_sha256,
        "metadata_sha256": header[
            "metadata_sha256"
        ],
        "structurally_valid": True,
    }


def main() -> int:
    need(
        not FINAL_RUNTIME.exists(),
        "final runtime already exists",
    )

    need(
        not BUILDING_RUNTIME.exists(),
        "building runtime already exists",
    )

    frozen_files = (
        (
            COMPILE_RECIPE_VALIDATION,
            EXPECTED_COMPILE_RECIPE_SHA256,
        ),
        (
            FULL_REPRESENTATION,
            EXPECTED_FULL_REPRESENTATION_SHA256,
        ),
        (
            Path(
                "experiments/model_fractal/"
                "maf_segment_reader_v1.py"
            ),
            "3499cb8e528fe8e9315e3e5656d6aa888c95ca175310b6371e722de409827369",
        ),
        (
            Path(
                "experiments/model_fractal/"
                "maf_resident_pk_directory_v1.py"
            ),
            "4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6",
        ),
        (
            INVENTORY,
            EXPECTED_INVENTORY_SHA256,
        ),
        (
            FULL_IDENTITY,
            EXPECTED_FULL_IDENTITY_SHA256,
        ),
        (
            PROTOCOL,
            EXPECTED_PROTOCOL_SHA256,
        ),
        (
            OBJECT_API,
            EXPECTED_OBJECT_API_SHA256,
        ),
        (
            SEGMENT_BUILDER,
            EXPECTED_SEGMENT_BUILDER_SHA256,
        ),
        (
            GENERATION_ENGINE,
            EXPECTED_GENERATION_ENGINE_SHA256,
        ),
    )

    for path, expected_sha256 in frozen_files:
        need(
            path.is_file(),
            "missing frozen input: " + str(path),
        )

        need(
            sha256_file(path)
            == expected_sha256,
            "frozen input SHA mismatch: " + str(path),
        )

    need(
        SOURCE.is_file(),
        "source GGUF missing",
    )

    need(
        sha256_file(SOURCE)
        == EXPECTED_SOURCE_SHA256,
        "source GGUF SHA mismatch",
    )

    inventory = load_json(
        INVENTORY
    )

    identity = load_json(
        FULL_IDENTITY
    )

    tensors = inventory.get(
        "tensors"
    )

    objects = identity.get(
        "objects"
    )

    need(
        isinstance(tensors, list)
        and len(tensors)
        == EXPECTED_TENSOR_COUNT,
        "inventory tensor count mismatch",
    )

    need(
        isinstance(objects, list)
        and len(objects)
        == EXPECTED_TENSOR_COUNT,
        "identity object count mismatch",
    )

    model = identity.get(
        "model"
    )

    need(
        isinstance(model, dict),
        "identity model record missing",
    )

    model_pk = model.get(
        "pk"
    )

    need(
        model_pk
        == EXPECTED_MODEL_PK,
        "model PK mismatch",
    )

    tensor_by_name = {}

    for row in tensors:
        need(
            isinstance(row, dict),
            "invalid inventory tensor record",
        )

        name = row.get(
            "name"
        )

        need(
            isinstance(name, str)
            and name,
            "inventory tensor name invalid",
        )

        need(
            name not in tensor_by_name,
            "duplicate inventory tensor name: " + name,
        )

        tensor_by_name[name] = row

    identity_by_name = {}

    for row in objects:
        need(
            isinstance(row, dict),
            "invalid identity object record",
        )

        name = row.get(
            "tensor_name"
        )

        need(
            isinstance(name, str)
            and name,
            "identity tensor name invalid",
        )

        need(
            name not in identity_by_name,
            "duplicate identity tensor name: " + name,
        )

        identity_by_name[name] = row

    need(
        set(tensor_by_name)
        == set(identity_by_name),
        "inventory and identity tensor-name sets differ",
    )

    expected_pks = {
        identity_object_pk(row)
        for row in objects
    }

    need(
        len(expected_pks)
        == EXPECTED_TENSOR_COUNT,
        "frozen object PK uniqueness failure",
    )

    object_writer = getattr(
        object_engine,
        OBJECT_WRITER_NAME,
        None,
    )

    segment_writer = getattr(
        segment_builder,
        SEGMENT_WRITER_NAME,
        None,
    )

    generation_writer = getattr(
        generation_engine,
        GENERATION_WRITER_NAME,
        None,
    )

    need(
        callable(object_writer),
        "frozen object writer unavailable",
    )

    need(
        callable(segment_writer),
        "frozen segment writer unavailable",
    )

    need(
        callable(generation_writer),
        "frozen generation writer unavailable",
    )

    compile_recipe_validation = load_json(
        COMPILE_RECIPE_VALIDATION
    )

    recipes = compile_recipe_validation.get(
        "recipes"
    )

    need(
        isinstance(
            recipes,
            list,
        )
        and len(
            recipes
        ) == EXPECTED_TENSOR_COUNT,
        "compile-recipe cardinality mismatch",
    )

    compile_recipe_by_name = {}

    for recipe in recipes:
        need(
            isinstance(
                recipe,
                dict,
            ),
            "compile-recipe row invalid",
        )

        recipe_name = recipe.get(
            "name"
        )

        recipe_pk = recipe.get(
            "object_pk"
        )

        need(
            isinstance(
                recipe_name,
                str,
            )
            and bool(
                recipe_name
            ),
            "compile-recipe tensor name invalid",
        )

        need(
            isinstance(
                recipe_pk,
                str,
            )
            and recipe_pk.startswith(
                "mafobj:v1:"
            ),
            "compile-recipe object PK invalid",
        )

        need(
            recipe_name
            not in compile_recipe_by_name,
            "duplicate compile-recipe tensor name",
        )

        compile_recipe_by_name[
            recipe_name
        ] = recipe

    need(
        set(
            compile_recipe_by_name
        )
        == set(
            identity_by_name
        ),
        "compile-recipe tensor-name set mismatch",
    )

    compile_recipe_pk_map_count = 0

    for recipe_name in sorted(
        identity_by_name
    ):
        identity_row = identity_by_name[
            recipe_name
        ]

        recipe = compile_recipe_by_name[
            recipe_name
        ]

        qualified_pk = identity_object_pk(
            identity_row
        )

        need(
            recipe[
                "object_pk"
            ] == qualified_pk,
            "identity / compile-recipe PK mismatch: "
            + recipe_name,
        )

        need(
            recipe.get(
                "tensor_type"
            )
            == identity_row.get(
                "tensor_type"
            ),
            "identity / compile-recipe type mismatch: "
            + recipe_name,
        )

        need(
            tuple(
                recipe.get(
                    "dims",
                    []
                )
            )
            == tuple(
                identity_row.get(
                    "dims",
                    []
                )
            ),
            "identity / compile-recipe dims mismatch: "
            + recipe_name,
        )

        compile_recipe_pk_map_count += 1

    need(
        compile_recipe_pk_map_count
        == EXPECTED_TENSOR_COUNT,
        "identity / compile-recipe 339-map count mismatch",
    )

    full_representation = load_json(
        FULL_REPRESENTATION
    )

    need(
        isinstance(
            full_representation,
            dict,
        ),
        "full representation root invalid",
    )

    need(
        all(
            key in full_representation
            for key in (
                "format",
                "gguf",
                "representation",
                "source",
            )
        ),
        "full representation authority shape mismatch",
    )

    RUNTIME_PARENT.mkdir(
        parents=True,
        exist_ok=True,
    )

    BUILDING_RUNTIME.mkdir()
    OBJECTS_DIR.mkdir()

    object_records = []

    for ordinal, tensor in enumerate(
        tensors,
        start=1,
    ):
        name = tensor["name"]
        identity_row = identity_by_name[name]

        object_pk = identity_object_pk(
            identity_row
        )

        tensor_type = tensor.get(
            "type"
        )

        dims = tensor.get(
            "dims"
        )

        span_bytes = int(
            tensor.get(
                "span_bytes",
                0,
            )
        )

        payload_sha256 = tensor.get(
            "payload_sha256"
        )

        need(
            tensor_type
            == identity_row.get(
                "tensor_type"
            ),
            "tensor type authority mismatch: " + name,
        )

        need(
            dims
            == identity_row.get(
                "dims"
            ),
            "tensor dims authority mismatch: " + name,
        )

        need(
            payload_sha256
            == identity_row.get(
                "payload_sha256"
            ),
            "payload SHA authority mismatch: " + name,
        )

        need(
            span_bytes > 0,
            "invalid tensor span: " + name,
        )

        need(
            isinstance(payload_sha256, str)
            and len(payload_sha256) == 64,
            "invalid payload SHA: " + name,
        )

        file_start = resolve_file_start(
            tensor,
            inventory,
        )

        output_path = (
            OBJECTS_DIR
            / safe_tensor_filename(
                ordinal,
                name,
            )
        )

        provenance = {
            "construction_protocol_sha256":
                EXPECTED_PROTOCOL_SHA256,
            "source_model_sha256":
                EXPECTED_SOURCE_SHA256,
            "source_tensor_name":
                name,
            "source_tensor_offset":
                int(
                    tensor.get(
                        "offset",
                        0,
                    )
                ),
            "source_file_start":
                file_start,
            "source_payload_sha256":
                payload_sha256,
            "frozen_object_pk":
                object_pk,
            "inventory_sha256":
                EXPECTED_INVENTORY_SHA256,
            "full_identity_sha256":
                EXPECTED_FULL_IDENTITY_SHA256,
        }

        object_semantics = {
            "source": SOURCE,
            "source_path": SOURCE,
            "source_file": SOURCE,
            "source_model_path": SOURCE,
            "gguf_path": SOURCE,

            "file_start": file_start,
            "source_file_start": file_start,
            "start": file_start,
            "offset": file_start,

            "tensor_name": name,
            "name": name,

            "tensor_type": tensor_type,
            "type": tensor_type,

            "dims": dims,
            "dimensions": dims,

            "payload_length": span_bytes,
            "span_bytes": span_bytes,
            "length": span_bytes,

            "expected_payload_sha256":
                payload_sha256,
            "payload_sha256":
                payload_sha256,

            "output_path": output_path,
            "object_path": output_path,
            "path": output_path,

            "provenance": provenance,
            "chunk_bytes": CHUNK_BYTES,
        }

        invoke_bound(
            object_writer,
            object_semantics,
            "object writer",
        )

        need(
            output_path.is_file(),
            "object writer did not create file: "
            + str(output_path),
        )

        view = object_engine.inspect_object(
            output_path
        )

        need(
            view.tensor_name == name,
            "object tensor name mismatch: " + name,
        )

        need(
            view.tensor_type == tensor_type,
            "object tensor type mismatch: " + name,
        )

        need(
            list(view.dims) == dims,
            "object dims mismatch: " + name,
        )

        need(
            view.payload_sha256
            == payload_sha256,
            "object payload SHA mismatch: " + name,
        )

        if hasattr(
            view,
            "object_pk",
        ):
            need(
                view.object_pk == object_pk,
                "object PK mismatch: " + name,
            )

        object_records.append(
            {
                "ordinal": ordinal,
                "model_pk": model_pk,
                "object_pk": object_pk,
                "tensor_name": name,
                "tensor_type": tensor_type,
                "dims": dims,
                "object_path": str(
                    output_path
                ),
                "object_file_sha256":
                    sha256_file(
                        output_path
                    ),
                "payload_sha256":
                    payload_sha256,
                "payload_length":
                    span_bytes,
            }
        )

    need(
        len(object_records)
        == EXPECTED_TENSOR_COUNT,
        "materialized object count mismatch",
    )

    need(
        {
            row["object_pk"]
            for row in object_records
        }
        == expected_pks,
        "materialized PK set mismatch",
    )

    segment_id = "segment:00000000"

    segment_semantics = {
        "objects": object_records,
        "object_records": object_records,
        "records": object_records,
        "inputs": object_records,

        "object_paths": [
            Path(
                row["object_path"]
            )
            for row in object_records
        ],
        "paths": [
            Path(
                row["object_path"]
            )
            for row in object_records
        ],

        "model_pk": model_pk,

        "segment_id": segment_id,

        "output_path": SEGMENT_PATH,
        "segment_path": SEGMENT_PATH,
        "path": SEGMENT_PATH,

        "manifest_path":
            SEGMENT_MANIFEST_PATH,
        "segment_manifest_path":
            SEGMENT_MANIFEST_PATH,

        "chunk_bytes": CHUNK_BYTES,
    }

    invoke_bound(
        segment_writer,
        segment_semantics,
        "segment writer",
    )

    need(
        SEGMENT_PATH.is_file(),
        "segment writer did not create segment",
    )

    need(
        SEGMENT_MANIFEST_PATH.is_file(),
        "segment writer did not create manifest",
    )

    segment_sha256 = sha256_file(
        SEGMENT_PATH
    )

    segment_length = (
        SEGMENT_PATH.stat().st_size
    )

    segment_manifest = load_json(
        SEGMENT_MANIFEST_PATH
    )

    segment_pks = extract_object_pks(
        segment_manifest
    )

    need(
        segment_pks == expected_pks,
        "segment manifest PK set mismatch",
    )

    segment_record = {
        "segment_id": segment_id,
        "segment_path": str(
            SEGMENT_PATH
        ),
        "segment_manifest_path": str(
            SEGMENT_MANIFEST_PATH
        ),
        "segment_length":
            segment_length,
        "segment_sha256":
            segment_sha256,
        "objects":
            object_records,
    }

    generation_semantics = {
        "model_pk": model_pk,
        "objects": object_records,

        "segments": [
            segment_record
        ],
        "segment_records": [
            segment_record
        ],
        "records": [
            segment_record
        ],
        "inputs": [
            segment_record
        ],

        "segment_paths": [
            SEGMENT_PATH
        ],
        "segment_manifests": [
            SEGMENT_MANIFEST_PATH
        ],
        "segment_manifest_paths": [
            SEGMENT_MANIFEST_PATH
        ],

        "output_path":
            GENERATION_MANIFEST_PATH,
        "manifest_path":
            GENERATION_MANIFEST_PATH,
        "generation_manifest_path":
            GENERATION_MANIFEST_PATH,
        "candidate_path":
            GENERATION_MANIFEST_PATH,

        "output_dir":
            BUILDING_RUNTIME,
        "generation_root":
            BUILDING_RUNTIME,
        "directory":
            BUILDING_RUNTIME,

        "chunk_bytes": CHUNK_BYTES,
    }

    invoke_bound(
        generation_writer,
        generation_semantics,
        "generation writer",
    )

    need(
        GENERATION_MANIFEST_PATH.is_file(),
        "generation writer did not create manifest",
    )

    generation = load_json(
        GENERATION_MANIFEST_PATH
    )

    generation_pks = extract_object_pks(
        generation
    )

    need(
        generation_pks == expected_pks,
        "generation manifest PK set mismatch",
    )

    locator_pks = strong_locator_pks(
        generation
    )

    need(
        locator_pks == expected_pks,
        "generation strong-locator coverage mismatch",
    )

    resident_module = __import__(
        "maf_resident_pk_directory_v1"
    )

    segment_reader_module = __import__(
        "maf_segment_reader_v1"
    )

    object_module = __import__(
        "maf_object_v1"
    )

    object_module_path = Path(
        object_module.__file__
    ).resolve()

    need(
        object_module_path
        == (
            ROOT
            / "experiments/model_fractal/"
            "maf_object_v1.py"
        ).resolve(),
        "object API import path mismatch",
    )

    resident_module_path = Path(
        resident_module.__file__
    ).resolve()

    segment_reader_module_path = Path(
        segment_reader_module.__file__
    ).resolve()

    need(
        resident_module_path
        == (
            ROOT
            / "experiments/model_fractal/"
            "maf_resident_pk_directory_v1.py"
        ).resolve(),
        "resident PK directory import path mismatch",
    )

    need(
        segment_reader_module_path
        == (
            ROOT
            / "experiments/model_fractal/"
            "maf_segment_reader_v1.py"
        ).resolve(),
        "segment reader import path mismatch",
    )

    generation_descriptor = generation.get(
        "descriptor"
    )

    need(
        isinstance(
            generation_descriptor,
            dict,
        ),
        "generation descriptor missing",
    )

    need(
        generation_descriptor.get(
            "model_pk"
        ) == model_pk,
        "generation model PK mismatch",
    )

    generation_pk = generation.get(
        "generation_pk"
    )

    need(
        isinstance(
            generation_pk,
            str,
        )
        and bool(
            generation_pk
        ),
        "generation PK missing",
    )

    generation_manifest_sha256 = sha256_file(
        GENERATION_MANIFEST_PATH
    )

    generation_segments = generation_descriptor.get(
        "segments"
    )

    generation_objects = generation_descriptor.get(
        "objects"
    )

    need(
        isinstance(
            generation_segments,
            list,
        )
        and len(
            generation_segments
        ) == 1,
        "generation segment cardinality mismatch",
    )

    need(
        isinstance(
            generation_objects,
            list,
        )
        and len(
            generation_objects
        ) == EXPECTED_TENSOR_COUNT,
        "generation readback object cardinality mismatch",
    )

    segment_by_id = {}

    for row in generation_segments:
        need(
            isinstance(
                row,
                dict,
            ),
            "generation segment record invalid",
        )

        current_segment_id = row.get(
            "segment_id"
        )

        need(
            isinstance(
                current_segment_id,
                str,
            )
            and bool(
                current_segment_id
            ),
            "generation segment ID invalid",
        )

        need(
            current_segment_id
            not in segment_by_id,
            "duplicate generation segment ID",
        )

        segment_by_id[
            current_segment_id
        ] = row

    need(
        set(
            segment_by_id
        ) == {
            segment_id
        },
        "generation segment ID set mismatch",
    )

    object_record_by_pk = {}

    for row in object_records:
        current_object_pk = row[
            "object_pk"
        ]

        need(
            current_object_pk
            not in object_record_by_pk,
            "duplicate materialized object PK",
        )

        object_record_by_pk[
            current_object_pk
        ] = row

    need(
        set(
            object_record_by_pk
        ) == expected_pks,
        "materialized object authority map mismatch",
    )

    readback_seen = set()
    readback_count = 0
    readback_serialized_sha256_count = 0
    readback_payload_authority_count = 0
    readback_pk_binding_count = 0
    readback_tensor_name_count = 0
    readback_tensor_type_count = 0
    readback_dims_count = 0
    readback_payload_length_count = 0
    readback_payload_sha256_direct_count = 0
    readback_structural_validity_count = 0
    readback_generation_confinement_count = 0

    for locator in generation_objects:
        need(
            isinstance(
                locator,
                dict,
            ),
            "generation object locator invalid",
        )

        current_object_pk = locator.get(
            "object_pk"
        )

        need(
            current_object_pk
            in expected_pks,
            "unexpected generation object PK",
        )

        need(
            current_object_pk
            not in readback_seen,
            "duplicate generation object locator",
        )

        authority = object_record_by_pk[
            current_object_pk
        ]

        current_segment_id = locator.get(
            "segment_id"
        )

        need(
            current_segment_id
            in segment_by_id,
            "generation object references unknown segment",
        )

        segment_authority = segment_by_id[
            current_segment_id
        ]

        need(
            locator.get(
                "object_file_sha256"
            )
            == authority[
                "object_file_sha256"
            ],
            "generation object-file SHA authority mismatch",
        )

        need(
            locator.get(
                "payload_sha256"
            )
            == authority[
                "payload_sha256"
            ],
            "generation payload SHA authority mismatch",
        )

        entry = resident_module.ResidentPKEntry(
            model_pk=model_pk,
            generation_pk=generation_pk,
            generation_manifest_sha256=(
                generation_manifest_sha256
            ),
            object_pk=current_object_pk,
            segment_id=current_segment_id,
            offset=locator[
                "offset"
            ],
            length=locator[
                "length"
            ],
            object_file_sha256=locator[
                "object_file_sha256"
            ],
            payload_sha256=locator[
                "payload_sha256"
            ],
            segment_length=segment_authority[
                "segment_length"
            ],
            segment_sha256=segment_authority[
                "segment_sha256"
            ],
            segment_path=str(
                SEGMENT_PATH
            ),
        )

        serialized_readback = (
            segment_reader_module.read_serialized_object(
                entry,
                generation_pk,
            )
        )

        need(
            type(
                serialized_readback
            ) is bytes,
            "segment reader returned non-bytes object",
        )

        need(
            len(
                serialized_readback
            ) == entry.length,
            "segment reader returned wrong serialized length",
        )

        need(
            hashlib.sha256(
                serialized_readback
            ).hexdigest()
            == entry.object_file_sha256,
            "segment reader serialized SHA mismatch",
        )

        need(
            entry.payload_sha256
            == authority[
                "payload_sha256"
            ],
            "segment readback payload authority mismatch",
        )

        decoded_readback = inspect_serialized_object_bytes(
            object_module,
            serialized_readback,
        )

        need(
            entry.object_pk
            == current_object_pk,
            "requested / resident-entry PK mismatch",
        )

        readback_name = decoded_readback[
            "tensor_name"
        ]

        need(
            readback_name
            == authority[
                "tensor_name"
            ],
            "readback tensor-name mismatch",
        )

        need(
            readback_name
            in identity_by_name,
            "readback tensor absent from frozen identity map",
        )

        returned_identity = identity_by_name[
            readback_name
        ]

        need(
            identity_object_pk(
                returned_identity
            ) == current_object_pk,
            "requested / decoded-object PK binding mismatch",
        )

        need(
            compile_recipe_by_name[
                readback_name
            ][
                "object_pk"
            ] == current_object_pk,
            "requested / compile-recipe PK binding mismatch",
        )

        need(
            decoded_readback[
                "tensor_type"
            ]
            == authority[
                "tensor_type"
            ],
            "readback tensor-type mismatch",
        )

        need(
            decoded_readback[
                "tensor_type"
            ]
            == returned_identity.get(
                "tensor_type"
            ),
            "readback type / frozen identity mismatch",
        )

        need(
            decoded_readback[
                "dims"
            ]
            == tuple(
                authority[
                    "dims"
                ]
            ),
            "readback dimensions mismatch",
        )

        need(
            decoded_readback[
                "dims"
            ]
            == tuple(
                returned_identity.get(
                    "dims",
                    []
                )
            ),
            "readback dimensions / frozen identity mismatch",
        )

        need(
            decoded_readback[
                "payload_length"
            ]
            == authority[
                "payload_length"
            ],
            "readback payload-length mismatch",
        )

        need(
            decoded_readback[
                "payload_sha256"
            ]
            == authority[
                "payload_sha256"
            ],
            "readback direct payload-SHA mismatch",
        )

        need(
            decoded_readback[
                "structurally_valid"
            ] is True,
            "readback structural object validation failed",
        )

        segment_path_resolved = Path(
            entry.segment_path
        ).resolve()

        building_runtime_resolved = BUILDING_RUNTIME.resolve()

        need(
            segment_path_resolved.parent
            == building_runtime_resolved,
            "readback locator resolves outside generation root",
        )

        need(
            current_segment_id
            in segment_by_id,
            "readback locator escaped generation segment set",
        )

        readback_pk_binding_count += 1
        readback_tensor_name_count += 1
        readback_tensor_type_count += 1
        readback_dims_count += 1
        readback_payload_length_count += 1
        readback_payload_sha256_direct_count += 1
        readback_structural_validity_count += 1
        readback_generation_confinement_count += 1

        readback_seen.add(
            current_object_pk
        )

        readback_count += 1
        readback_serialized_sha256_count += 1
        readback_payload_authority_count += 1

        del serialized_readback

    need(
        readback_seen == expected_pks,
        "segment-reader readback PK set mismatch",
    )

    need(
        readback_count
        == EXPECTED_TENSOR_COUNT,
        "segment-reader readback count mismatch",
    )

    need(
        readback_serialized_sha256_count
        == EXPECTED_TENSOR_COUNT,
        "serialized SHA readback count mismatch",
    )

    need(
        readback_payload_authority_count
        == EXPECTED_TENSOR_COUNT,
        "payload authority readback count mismatch",
    )

    for label, observed_count in (
        (
            "PK binding",
            readback_pk_binding_count,
        ),
        (
            "tensor name",
            readback_tensor_name_count,
        ),
        (
            "tensor type",
            readback_tensor_type_count,
        ),
        (
            "dimensions",
            readback_dims_count,
        ),
        (
            "payload length",
            readback_payload_length_count,
        ),
        (
            "direct payload SHA256",
            readback_payload_sha256_direct_count,
        ),
        (
            "structural validity",
            readback_structural_validity_count,
        ),
        (
            "generation confinement",
            readback_generation_confinement_count,
        ),
    ):
        need(
            observed_count
            == EXPECTED_TENSOR_COUNT,
            "339/339 readback qualification count mismatch: "
            + label,
        )

    result = {
        "schema":
            "openmind.maf_phase_6e_d_entry_"
            "complete_model_persistent_"
            "maf_payload_generation.v1",

        "model_pk":
            model_pk,

        "source_model_sha256":
            EXPECTED_SOURCE_SHA256,

        "tensor_count":
            EXPECTED_TENSOR_COUNT,

        "object_count":
            len(
                object_records
            ),

        "object_pk_count":
            len(
                expected_pks
            ),

        "strong_locator_count":
            len(
                locator_pks
            ),

        "segment_reader_readback_count":
            readback_count,

        "segment_reader_serialized_sha256_count":
            readback_serialized_sha256_count,

        "segment_reader_payload_authority_count":
            readback_payload_authority_count,

        "pg11_segment_reader_readback": True,
        "pg12_payload_sha256_authority": True,

        "compile_recipe_validation_sha256":
            EXPECTED_COMPILE_RECIPE_SHA256,

        "full_representation_sha256":
            EXPECTED_FULL_REPRESENTATION_SHA256,

        "compile_recipe_pk_map_count":
            compile_recipe_pk_map_count,

        "readback_pk_binding_count":
            readback_pk_binding_count,

        "readback_tensor_name_count":
            readback_tensor_name_count,

        "readback_tensor_type_count":
            readback_tensor_type_count,

        "readback_dims_count":
            readback_dims_count,

        "readback_payload_length_count":
            readback_payload_length_count,

        "readback_payload_sha256_direct_count":
            readback_payload_sha256_direct_count,

        "readback_structural_validity_count":
            readback_structural_validity_count,

        "readback_generation_confinement_count":
            readback_generation_confinement_count,

        "readback_direct_object_validation": True,
        "runtime_root_protocol_conformant": True,

        "payload_readback_verification_basis": (
            "segment_reader_exact_serialized_object_sha256"
            " -> materialized_object_record"
            " -> frozen_payload_sha256_authority"
        ),

        "segment_count":
            1,

        "segment_sha256":
            segment_sha256,

        "segment_length":
            segment_length,

        "generation_manifest_sha256":
            sha256_file(
                GENERATION_MANIFEST_PATH
            ),

        "frozen_inputs": {
            "construction_protocol_sha256":
                EXPECTED_PROTOCOL_SHA256,
            "inventory_sha256":
                EXPECTED_INVENTORY_SHA256,
            "full_identity_sha256":
                EXPECTED_FULL_IDENTITY_SHA256,
            "object_api_sha256":
                EXPECTED_OBJECT_API_SHA256,
            "segment_builder_sha256":
                EXPECTED_SEGMENT_BUILDER_SHA256,
            "generation_engine_sha256":
                EXPECTED_GENERATION_ENGINE_SHA256,
        },

        "claims": {
            "complete_persistent_generation":
                True,
            "maf_native_compute":
                False,
            "selective_inference":
                False,
            "output_parity":
                False,
            "phase_6e_d_science_authorized":
                False,
        },
    }

    RESULT_PATH.write_bytes(
        canonical_json_bytes(
            result
        )
    )

    BUILDING_RUNTIME.rename(
        FINAL_RUNTIME
    )

    print(
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
