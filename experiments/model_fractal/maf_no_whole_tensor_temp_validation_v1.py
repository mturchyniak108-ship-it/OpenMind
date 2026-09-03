#!/usr/bin/env python3

from __future__ import annotations

import ast
import hashlib
import json
import sys
import tracemalloc
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent

sys.path.insert(
    0,
    str(HERE),
)

import maf_encoder_v1
import maf_object_v1


SCHEMA = (
    "openmind."
    "maf_no_whole_tensor_temp_validation.v1"
)

ENCODER_PATH = (
    HERE / "maf_encoder_v1.py"
)

OBJECT_PATH = (
    HERE / "maf_object_v1.py"
)

RESULT_PATH = (
    HERE
    / "maf_no_whole_tensor_temp_validation_v1.json"
)

RUNTIME_DIR = (
    ROOT
    / "results"
    / "runtime"
    / "maf_no_whole_tensor_temp_validation_v1"
)

SOURCE_PATH = (
    RUNTIME_DIR
    / "synthetic_source.bin"
)

OBJECT_OUTPUT_PATH = (
    RUNTIME_DIR
    / "synthetic_object.maf"
)

PAYLOAD_BYTES = 16 * 1024 * 1024
CHUNK_BYTES = 1 * 1024 * 1024

# A tensor-sized 16 MiB Python bytes temporary would itself
# exceed this bound. This is intentionally conservative
# relative to the 1 MiB streaming chunk.
MAX_TRACED_PEAK_BYTES = 8 * 1024 * 1024

SOURCE_BUILD_BLOCK_BYTES = 64 * 1024

EXPECTED_ENCODER_SHA256 = (
    "0232fc49c2ef568291453b48b62bf6a3"
    "7fa64f123051224b4228a214454995c0"
)

EXPECTED_OBJECT_SHA256 = (
    "eed6cbd96995412a632883f3c534f902"
    "3e7711ea8eb437afe35a48312502f63b"
)

FORBIDDEN_MECHANISMS = (
    "read_bytes",
    "write_bytes",
    "bytearray(",
    "memoryview(",
    "BytesIO",
    "mmap",
    "numpy",
)

ALLOWED_CLAIMS = (
    "encoder_delegates_payload_compilation_once",
    "compiler_payload_loop_uses_iter_exact",
    "iter_exact_bounds_each_requested_read",
    "dynamic_payload_exceeds_stream_chunk",
    "dynamic_multiple_payload_chunks_required",
    "dynamic_traced_peak_below_half_payload",
    "exact_persisted_payload_sha256",
    "independent_persisted_object_reopen",
    "no_python_tensor_sized_temporary_observed",
)

FORBIDDEN_CLAIMS = (
    "total_process_rss_bound",
    "kernel_page_cache_bound",
    "filesystem_cache_bound",
    "zero_copy",
    "no_native_allocator_temporary",
    "compression",
    "selective_access",
    "runtime_residency_reduction",
    "inference_speedup",
    "maf_native_compute",
    "vulkan_execution",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        while True:
            chunk = stream.read(
                SOURCE_BUILD_BLOCK_BYTES
            )

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


def function_node(
    tree: ast.Module,
    name: str,
) -> ast.FunctionDef:
    matches = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == name
    ]

    if len(matches) != 1:
        raise RuntimeError(
            f"expected one function {name}, "
            f"found {len(matches)}"
        )

    return matches[0]


def static_audit() -> dict:
    encoder_text = ENCODER_PATH.read_text()
    object_text = OBJECT_PATH.read_text()

    encoder_sha = hashlib.sha256(
        encoder_text.encode("utf-8")
    ).hexdigest()

    object_sha = hashlib.sha256(
        object_text.encode("utf-8")
    ).hexdigest()

    if encoder_sha != EXPECTED_ENCODER_SHA256:
        raise RuntimeError(
            "frozen Encoder SHA mismatch"
        )

    if object_sha != EXPECTED_OBJECT_SHA256:
        raise RuntimeError(
            "frozen Object V1 SHA mismatch"
        )

    encoder_tree = ast.parse(
        encoder_text
    )

    object_tree = ast.parse(
        object_text
    )

    encode_node = function_node(
        encoder_tree,
        "encode_object",
    )

    compile_node = function_node(
        object_tree,
        "compile_object",
    )

    iter_node = function_node(
        object_tree,
        "iter_exact",
    )

    encoder_calls = [
        node
        for node in ast.walk(encode_node)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "compile_object"
    ]

    compile_iter_calls = [
        node
        for node in ast.walk(compile_node)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "iter_exact"
    ]

    iter_reads = [
        node
        for node in ast.walk(iter_node)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "read"
    ]

    if len(encoder_calls) != 1:
        raise RuntimeError(
            "Encoder must call compile_object "
            "exactly once"
        )

    if len(compile_iter_calls) != 1:
        raise RuntimeError(
            "compile_object must use iter_exact "
            "exactly once for source payload"
        )

    if len(iter_reads) != 1:
        raise RuntimeError(
            "iter_exact must contain exactly "
            "one stream.read call"
        )

    encode_source = ast.get_source_segment(
        encoder_text,
        encode_node,
    ) or ""

    compile_source = ast.get_source_segment(
        object_text,
        compile_node,
    ) or ""

    iter_source = ast.get_source_segment(
        object_text,
        iter_node,
    ) or ""

    relevant_source = (
        encode_source
        + "\n"
        + compile_source
        + "\n"
        + iter_source
    )

    forbidden_found = [
        item
        for item in FORBIDDEN_MECHANISMS
        if item in relevant_source
    ]

    if forbidden_found:
        raise RuntimeError(
            "forbidden whole-buffer mechanism: "
            + ", ".join(forbidden_found)
        )

    required_iter_fragments = (
        "want = min(remaining, chunk_bytes)",
        "chunk = stream.read(want)",
        "remaining -= len(chunk)",
    )

    for fragment in required_iter_fragments:
        if fragment not in iter_source:
            raise RuntimeError(
                "missing bounded-read invariant: "
                + fragment
            )

    if "chunk_bytes=chunk_bytes" not in encode_source:
        raise RuntimeError(
            "Encoder does not forward chunk_bytes"
        )

    if "chunk_bytes," not in compile_source:
        raise RuntimeError(
            "compiler streaming chunk not visible"
        )

    return {
        "encoder_sha256": encoder_sha,
        "object_sha256": object_sha,
        "encoder_compile_object_calls": (
            len(encoder_calls)
        ),
        "compiler_iter_exact_calls": (
            len(compile_iter_calls)
        ),
        "iter_exact_stream_read_calls": (
            len(iter_reads)
        ),
        "bounded_read_expression_present": True,
        "chunk_forwarding_present": True,
        "forbidden_mechanisms_found": (
            forbidden_found
        ),
        "pass": True,
    }


def build_synthetic_source() -> str:
    if RUNTIME_DIR.exists():
        raise RuntimeError(
            f"runtime directory already exists: "
            f"{RUNTIME_DIR}"
        )

    RUNTIME_DIR.mkdir(
        parents=True,
        exist_ok=False,
    )

    block = bytes(
        (
            index % 251
            for index in range(
                SOURCE_BUILD_BLOCK_BYTES
            )
        )
    )

    if len(block) != SOURCE_BUILD_BLOCK_BYTES:
        raise RuntimeError(
            "synthetic block size mismatch"
        )

    digest = hashlib.sha256()
    written = 0

    with SOURCE_PATH.open("xb") as stream:
        while written < PAYLOAD_BYTES:
            remaining = (
                PAYLOAD_BYTES - written
            )

            part = block[
                :min(
                    remaining,
                    len(block),
                )
            ]

            stream.write(part)
            digest.update(part)
            written += len(part)

        stream.flush()

    if written != PAYLOAD_BYTES:
        raise RuntimeError(
            "synthetic payload byte-count mismatch"
        )

    return digest.hexdigest()


def dynamic_audit(
    expected_sha256: str,
) -> dict:
    if PAYLOAD_BYTES <= CHUNK_BYTES:
        raise RuntimeError(
            "payload must exceed chunk size"
        )

    if (
        PAYLOAD_BYTES
        % CHUNK_BYTES
        != 0
    ):
        raise RuntimeError(
            "frozen test requires exact chunk multiple"
        )

    expected_chunks = (
        PAYLOAD_BYTES // CHUNK_BYTES
    )

    tracemalloc.start()

    try:
        view = maf_object_v1.compile_object(
            source_path=SOURCE_PATH,
            source_file_start=0,
            tensor_name=(
                "synthetic."
                "no_whole_tensor_temp.weight"
            ),
            tensor_type="F32",
            dims=(
                PAYLOAD_BYTES // 4,
            ),
            payload_length=PAYLOAD_BYTES,
            expected_payload_sha256=(
                expected_sha256
            ),
            output_path=OBJECT_OUTPUT_PATH,
            provenance={
                "validation_schema": SCHEMA,
                "purpose": (
                    "dynamic bounded-memory "
                    "compiler validation"
                ),
            },
            chunk_bytes=CHUNK_BYTES,
        )

        current_bytes, peak_bytes = (
            tracemalloc.get_traced_memory()
        )
    finally:
        tracemalloc.stop()

    reopened = (
        maf_object_v1.inspect_object(
            OBJECT_OUTPUT_PATH,
            chunk_bytes=CHUNK_BYTES,
        )
    )

    output_sha_pass = (
        view.payload_sha256
        == expected_sha256
        == reopened.payload_sha256
    )

    source_sha_pass = (
        sha256_file(SOURCE_PATH)
        == expected_sha256
    )

    peak_pass = (
        peak_bytes
        < MAX_TRACED_PEAK_BYTES
    )

    half_payload_pass = (
        peak_bytes
        < PAYLOAD_BYTES // 2
    )

    all_pass = (
        output_sha_pass
        and source_sha_pass
        and peak_pass
        and half_payload_pass
        and expected_chunks > 1
        and view.payload_length
            == PAYLOAD_BYTES
        and reopened.payload_length
            == PAYLOAD_BYTES
    )

    return {
        "payload_bytes": PAYLOAD_BYTES,
        "chunk_bytes": CHUNK_BYTES,
        "expected_payload_chunks": (
            expected_chunks
        ),
        "max_traced_peak_bytes": (
            MAX_TRACED_PEAK_BYTES
        ),
        "tracemalloc_current_bytes": (
            current_bytes
        ),
        "tracemalloc_peak_bytes": (
            peak_bytes
        ),
        "peak_less_than_half_payload": (
            half_payload_pass
        ),
        "peak_under_frozen_bound": (
            peak_pass
        ),
        "source_payload_sha256": (
            expected_sha256
        ),
        "persisted_payload_sha256": (
            reopened.payload_sha256
        ),
        "exact_payload_sha_pass": (
            output_sha_pass
        ),
        "source_rehash_pass": (
            source_sha_pass
        ),
        "output_path": str(
            OBJECT_OUTPUT_PATH
        ),
        "pass": all_pass,
    }


def main() -> None:
    if RESULT_PATH.exists():
        raise RuntimeError(
            f"result already exists: {RESULT_PATH}"
        )

    static = static_audit()

    expected_sha256 = (
        build_synthetic_source()
    )

    dynamic = dynamic_audit(
        expected_sha256
    )

    all_pass = (
        static["pass"]
        and dynamic["pass"]
    )

    result = {
        "schema": SCHEMA,
        "test_scope": (
            "python_level_tensor_temporary_"
            "allocation_in_frozen_encoder_"
            "compiler_path"
        ),
        "static_audit": static,
        "dynamic_audit": dynamic,
        "allowed_claims": list(
            ALLOWED_CLAIMS
        ),
        "forbidden_claims": list(
            FORBIDDEN_CLAIMS
        ),
        "all_pass": all_pass,
    }

    RESULT_PATH.write_text(
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    print(
        "schema                   :",
        SCHEMA,
    )
    print(
        "payload bytes            :",
        PAYLOAD_BYTES,
    )
    print(
        "chunk bytes              :",
        CHUNK_BYTES,
    )
    print(
        "expected payload chunks  :",
        dynamic[
            "expected_payload_chunks"
        ],
    )
    print(
        "tracemalloc peak bytes   :",
        dynamic[
            "tracemalloc_peak_bytes"
        ],
    )
    print(
        "frozen max peak bytes    :",
        MAX_TRACED_PEAK_BYTES,
    )
    print(
        "peak < half payload      :",
        dynamic[
            "peak_less_than_half_payload"
        ],
    )
    print(
        "exact payload SHA        :",
        dynamic[
            "exact_payload_sha_pass"
        ],
    )
    print(
        "all_pass                 :",
        all_pass,
    )

    if not all_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
