#!/usr/bin/env python3

"""
OpenMind / MAF Object v1 persistent pilot fidelity experiment.

Preregistered experiment.

Exactly the five tensors in maf_pilot_manifest_v1.json are compiled
into persistent MAF Object v1 files.

Required gates:

1. frozen source GGUF hash
2. frozen inventory integrity
3. frozen pilot-manifest integrity
4. exact five-name pilot set
5. MAF Object v1 independent reopen
6. payload SHA256 equality
7. literal streamed source/object byte equality
8. no unexpected partial files
9. exactly five passing final objects

No compression, transformation, fragmentation, or selective access
is evaluated here.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

EXPERIMENTS = ROOT / "experiments" / "model_fractal"

SOURCE = Path.home() / "qwen2.5-coder-q8_0.gguf"

INVENTORY = (
    EXPERIMENTS
    / "gguf_tensor_inventory_v1.json"
)

PILOT = (
    EXPERIMENTS
    / "maf_pilot_manifest_v1.json"
)

ENGINE_PATH = (
    EXPERIMENTS
    / "maf_object_v1.py"
)

RESULT_ROOT = (
    ROOT
    / "results"
    / "runtime"
    / "maf_object_v1_pilot"
)

RESULT_JSON = (
    RESULT_ROOT
    / "maf_object_v1_pilot_fidelity.json"
)

OBJECT_DIR = (
    RESULT_ROOT
    / "objects"
)

EXPECTED_SOURCE_SHA256 = (
    "507de59046601282"
    "ba768a9789900e6c"
    "cf60ed93ddf34673"
    "0b7c68eb0715bc47"
)

EXPECTED_PROTOCOL_SHA256 = (
    "d7e081e2030ee6cf"
    "2dde99026be7ef99"
    "d4a821a9b3a8b6e0"
    "6fb780899ab3059b"
)

EXPECTED_ENGINE_SHA256 = (
    "eed6cbd96995412a"
    "632883f3c534f902"
    "3e7711ea8eb437af"
    "e35a48312502f63b"
)

EXPECTED_NAMES = (
    "output_norm.weight",
    "blk.0.attn_norm.weight",
    "blk.0.attn_q.weight",
    "blk.0.ffn_down.weight",
    "token_embd.weight",
)

CHUNK_BYTES = 4 * 1024 * 1024


def sha256_file(
    path: Path,
    *,
    chunk_bytes: int = CHUNK_BYTES,
) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        while True:
            chunk = stream.read(chunk_bytes)

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


def load_json(path: Path) -> dict:
    with path.open(
        "r",
        encoding="utf-8",
    ) as stream:
        return json.load(stream)


def load_engine():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "openmind_maf_object_v1",
        ENGINE_PATH,
    )

    if spec is None or spec.loader is None:
        raise RuntimeError(
            "HOLD: cannot load MAF object engine"
        )

    module = importlib.util.module_from_spec(
        spec
    )

    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    return module


def tensor_map(
    inventory: dict,
) -> dict[str, dict]:
    tensors = inventory.get("tensors")

    if not isinstance(tensors, list):
        raise RuntimeError(
            "HOLD: inventory tensors missing"
        )

    by_name: dict[str, dict] = {}

    for tensor in tensors:
        name = tensor.get("name")

        if not isinstance(name, str):
            raise RuntimeError(
                "HOLD: inventory tensor name invalid"
            )

        if name in by_name:
            raise RuntimeError(
                f"HOLD: duplicate tensor: {name}"
            )

        by_name[name] = tensor

    return by_name


def resolve_file_start(
    tensor: dict,
    inventory: dict,
) -> int:
    if "file_start" in tensor:
        return int(
            tensor["file_start"]
        )

    source = inventory.get(
        "source",
        {},
    )

    data_offset = source.get(
        "data_offset"
    )

    if data_offset is None:
        data_offset = inventory.get(
            "data_offset"
        )

    if data_offset is None:
        raise RuntimeError(
            "HOLD: cannot resolve GGUF data offset"
        )

    return (
        int(data_offset)
        + int(tensor["offset"])
    )


def clean_output_preflight() -> None:
    if RESULT_JSON.exists():
        raise RuntimeError(
            "HOLD: result JSON already exists"
        )

    if OBJECT_DIR.exists():
        existing = list(
            OBJECT_DIR.iterdir()
        )

        if existing:
            raise RuntimeError(
                "HOLD: object directory is not empty"
            )

    partials = list(
        RESULT_ROOT.glob(
            "**/*.partial"
        )
    )

    if partials:
        raise RuntimeError(
            "HOLD: partial object files already exist"
        )


def main() -> int:
    protocol_path = (
        EXPERIMENTS
        / "MAF_OBJECT_V1_PROTOCOL.md"
    )

    protocol_sha = sha256_file(
        protocol_path
    )

    engine_sha = sha256_file(
        ENGINE_PATH
    )

    if (
        protocol_sha
        != EXPECTED_PROTOCOL_SHA256
    ):
        raise RuntimeError(
            "HOLD: protocol SHA256 drift"
        )

    if (
        engine_sha
        != EXPECTED_ENGINE_SHA256
    ):
        raise RuntimeError(
            "HOLD: engine SHA256 drift"
        )

    inventory = load_json(
        INVENTORY
    )

    pilot = load_json(
        PILOT
    )

    source_expected = (
        inventory
        .get("source", {})
        .get("sha256")
    )

    if (
        source_expected
        != EXPECTED_SOURCE_SHA256
    ):
        raise RuntimeError(
            "HOLD: inventory source SHA256 drift"
        )

    source_actual = sha256_file(
        SOURCE
    )

    if (
        source_actual
        != EXPECTED_SOURCE_SHA256
    ):
        raise RuntimeError(
            "HOLD: source GGUF SHA256 drift"
        )

    pilot_rows = pilot.get(
        "pilot"
    )

    if not isinstance(
        pilot_rows,
        list,
    ):
        raise RuntimeError(
            "HOLD: pilot list missing"
        )

    names = tuple(
        row.get("name")
        for row in pilot_rows
    )

    if names != EXPECTED_NAMES:
        raise RuntimeError(
            "HOLD: pilot target set/order drift"
        )

    if len(pilot_rows) != 5:
        raise RuntimeError(
            "HOLD: expected exactly five pilot tensors"
        )

    tensors = tensor_map(
        inventory
    )

    clean_output_preflight()

    RESULT_ROOT.mkdir(
        parents=True,
        exist_ok=True,
    )

    OBJECT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    engine = load_engine()

    results: list[dict] = []

    print(
        "=" * 72
    )
    print(
        " OPENMIND / MAF OBJECT V1 PILOT FIDELITY"
    )
    print(
        "=" * 72
    )
    print(
        "source:",
        SOURCE,
    )
    print(
        "targets:",
        len(pilot_rows),
    )
    print(
        "chunk MiB:",
        CHUNK_BYTES // 1024 // 1024,
    )

    for index, pilot_row in enumerate(
        pilot_rows,
        start=1,
    ):
        name = pilot_row["name"]

        if name not in tensors:
            raise RuntimeError(
                f"HOLD: tensor absent from inventory: {name}"
            )

        tensor = tensors[name]

        tensor_type = tensor["type"]
        dims = tensor["dims"]
        span_bytes = int(
            tensor["span_bytes"]
        )
        payload_sha256 = tensor[
            "payload_sha256"
        ]

        if tensor_type != pilot_row["type"]:
            raise RuntimeError(
                f"HOLD: type mismatch: {name}"
            )

        if dims != pilot_row["dims"]:
            raise RuntimeError(
                f"HOLD: dims mismatch: {name}"
            )

        if (
            span_bytes
            != int(
                pilot_row["span_bytes"]
            )
        ):
            raise RuntimeError(
                f"HOLD: span mismatch: {name}"
            )

        if (
            payload_sha256
            != pilot_row["payload_sha256"]
        ):
            raise RuntimeError(
                f"HOLD: payload hash mismatch: {name}"
            )

        file_start = resolve_file_start(
            tensor,
            inventory,
        )

        output_path = (
            OBJECT_DIR
            / f"{index:02d}.mafobj"
        )

        provenance = {
            "source_model_sha256":
                EXPECTED_SOURCE_SHA256,
            "source_tensor_name":
                name,
            "source_tensor_offset":
                int(tensor["offset"]),
            "source_file_start":
                file_start,
            "pilot_ordinal":
                int(
                    pilot_row["ordinal"]
                ),
        }

        print()
        print(
            f"[{index}/5] {name}"
        )
        print(
            "  type       :",
            tensor_type,
        )
        print(
            "  span bytes :",
            f"{span_bytes:,}",
        )

        view = engine.compile_object(
            source_path=SOURCE,
            source_file_start=file_start,
            tensor_name=name,
            tensor_type=tensor_type,
            dims=dims,
            payload_length=span_bytes,
            expected_payload_sha256=payload_sha256,
            output_path=output_path,
            provenance=provenance,
            chunk_bytes=CHUNK_BYTES,
        )

        reopened = engine.inspect_object(
            output_path,
            chunk_bytes=CHUNK_BYTES,
        )

        byte_equal = (
            engine.compare_payload_to_source(
                object_path=output_path,
                source_path=SOURCE,
                source_file_start=file_start,
                chunk_bytes=CHUNK_BYTES,
            )
        )

        final_size = (
            output_path.stat().st_size
        )

        passed = (
            reopened.tensor_name
            == name
            and reopened.tensor_type
            == tensor_type
            and list(
                reopened.dims
            )
            == dims
            and reopened.payload_length
            == span_bytes
            and reopened.payload_sha256
            == payload_sha256
            and view.payload_sha256
            == payload_sha256
            and byte_equal
            and final_size
            > span_bytes
        )

        print(
            "  reopen     :",
            "PASS"
            if reopened.payload_sha256
            == payload_sha256
            else "FAIL",
        )
        print(
            "  byte equal :",
            byte_equal,
        )
        print(
            "  result     :",
            "PASS"
            if passed
            else "FAIL",
        )

        results.append(
            {
                "ordinal":
                    index,
                "name":
                    name,
                "type":
                    tensor_type,
                "dims":
                    dims,
                "span_bytes":
                    span_bytes,
                "source_file_start":
                    file_start,
                "source_payload_sha256":
                    payload_sha256,
                "object_file":
                    str(
                        output_path.relative_to(
                            ROOT
                        )
                    ),
                "object_file_bytes":
                    final_size,
                "payload_offset":
                    reopened.payload_offset,
                "object_payload_sha256":
                    reopened.payload_sha256,
                "metadata_sha256":
                    reopened.metadata_sha256,
                "literal_byte_equal":
                    byte_equal,
                "pass":
                    passed,
            }
        )

        if not passed:
            raise RuntimeError(
                f"HOLD: fidelity failure: {name}"
            )

    partials = list(
        RESULT_ROOT.glob(
            "**/*.partial"
        )
    )

    if partials:
        raise RuntimeError(
            "HOLD: partial files remain after compilation"
        )

    final_objects = sorted(
        OBJECT_DIR.glob(
            "*.mafobj"
        )
    )

    if len(final_objects) != 5:
        raise RuntimeError(
            "HOLD: expected exactly five final objects"
        )

    all_pass = (
        len(results) == 5
        and all(
            row["pass"]
            for row in results
        )
    )

    report = {
        "schema":
            "openmind.maf_object_v1_pilot_fidelity.v1",
        "source":
            str(SOURCE),
        "source_sha256":
            source_actual,
        "inventory_file_sha256":
            sha256_file(INVENTORY),
        "pilot_manifest_file_sha256":
            sha256_file(PILOT),
        "protocol_file_sha256":
            protocol_sha,
        "engine_file_sha256":
            engine_sha,
        "chunk_bytes":
            CHUNK_BYTES,
        "target_count":
            len(results),
        "total_payload_bytes":
            sum(
                row["span_bytes"]
                for row in results
            ),
        "persistent_objects":
            True,
        "independent_reopen":
            True,
        "literal_byte_comparison":
            True,
        "results":
            results,
        "all_pass":
            all_pass,
    }

    if not all_pass:
        raise RuntimeError(
            "HOLD: pilot did not fully pass"
        )

    with RESULT_JSON.open(
        "x",
        encoding="utf-8",
    ) as stream:
        json.dump(
            report,
            stream,
            indent=2,
            sort_keys=True,
        )
        stream.write("\n")

    print()
    print(
        "=" * 72
    )
    print(
        "PERSISTENT OBJECT FIDELITY: PASS"
    )
    print(
        "objects:",
        len(final_objects),
    )
    print(
        "payload bytes:",
        f"{report['total_payload_bytes']:,}",
    )
    print(
        "result:",
        RESULT_JSON,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
