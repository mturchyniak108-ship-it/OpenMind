#!/usr/bin/env python3

import gc
import hashlib
import json
import os
import stat
import statistics
import time
from pathlib import Path

import maf_segment_reader_v1 as reader
from maf_resident_pk_directory_v1 import ResidentPKEntry


SCHEMA = "openmind.maf_segment_reader_benchmark.v1"

PROTOCOL = Path(
    "experiments/model_fractal/"
    "MAF_SEGMENT_READER_BENCHMARK_V1_PROTOCOL.md"
)

ENGINE = Path(
    "experiments/model_fractal/"
    "maf_segment_reader_v1.py"
)

RESIDENT = Path(
    "experiments/model_fractal/"
    "maf_resident_pk_directory_v1.py"
)

VALIDATION_RESULT = Path(
    "experiments/model_fractal/"
    "maf_segment_reader_validation_v1.json"
)

RESULT = Path(
    "experiments/model_fractal/"
    "maf_segment_reader_benchmark_v1.json"
)

SOURCE_RUNTIME = Path(
    "results/runtime/"
    "maf_resident_pk_directory_benchmark_v1_1"
)

SOURCE_MANIFEST = (
    SOURCE_RUNTIME /
    "candidate_a.manifest.json"
)

EXPECTED_PROTOCOL_SHA256 = "48263a8c6e57c4e3739f0c1c2eeef1a85c4ab04bc53b7b24762aaacff889d55b"

EXPECTED_ENGINE_SHA256 = "3499cb8e528fe8e9315e3e5656d6aa888c95ca175310b6371e722de409827369"

EXPECTED_RESIDENT_SHA256 = "4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6"

EXPECTED_VALIDATION_RESULT_SHA256 = "1ceef1ed2b814da3951811ea97e9f4475b3fa79557b341e7c8e089ec8a409328"

WARMUP = 100
REPEATS = 1000


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    return sha256_bytes(path.read_bytes())


def write_json_exclusive(path, data):
    with path.open("x", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            sort_keys=True,
        )
        f.write("\n")


def fd_count():
    root = Path("/proc/self/fd")

    if not root.is_dir():
        return None

    try:
        return len(list(root.iterdir()))
    except OSError:
        return None


def source_fingerprint():
    h = hashlib.sha256()

    paths = [
        SOURCE_MANIFEST,
        *sorted(SOURCE_RUNTIME.rglob("*.mafseg")),
    ]

    for path in paths:
        raw = path.read_bytes()
        rel = str(path).encode("utf-8")

        h.update(
            len(rel).to_bytes(8, "big")
        )
        h.update(rel)

        h.update(
            len(raw).to_bytes(8, "big")
        )
        h.update(
            hashlib.sha256(raw).digest()
        )

    return h.hexdigest()


def open_flags():
    flags = os.O_RDONLY

    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC

    return flags


def resolve_entries():
    manifest_raw = SOURCE_MANIFEST.read_bytes()

    manifest = json.loads(
        manifest_raw.decode("utf-8")
    )

    descriptor = manifest["descriptor"]
    generation_pk = manifest["generation_pk"]
    model_pk = descriptor["model_pk"]

    manifest_sha = sha256_bytes(
        manifest_raw
    )

    segments = {
        item["segment_id"]: item
        for item in descriptor["segments"]
    }

    candidates = sorted(
        SOURCE_RUNTIME.rglob("*.mafseg")
    )

    segment_paths = {}
    segment_raw = {}

    for segment_id, segment in segments.items():
        matches = []

        for path in candidates:
            if (
                path.stat().st_size
                != segment["segment_length"]
            ):
                continue

            raw = path.read_bytes()

            if (
                sha256_bytes(raw)
                == segment["segment_sha256"]
            ):
                matches.append(
                    (path, raw)
                )

        if matches:
            path, raw = matches[0]
            segment_paths[segment_id] = path
            segment_raw[segment_id] = raw

    resolved = []

    for obj in descriptor["objects"]:
        segment_id = obj["segment_id"]

        if segment_id not in segment_paths:
            continue

        segment = segments[segment_id]
        raw = segment_raw[segment_id]

        offset = obj["offset"]
        length = obj["length"]

        expected = raw[
            offset:
            offset + length
        ]

        if (
            len(expected) != length
            or sha256_bytes(expected)
            != obj["object_file_sha256"]
        ):
            continue

        entry = ResidentPKEntry(
            model_pk=model_pk,
            generation_pk=generation_pk,
            generation_manifest_sha256=manifest_sha,
            object_pk=obj["object_pk"],
            segment_id=segment_id,
            offset=offset,
            length=length,
            object_file_sha256=
                obj["object_file_sha256"],
            payload_sha256=
                obj["payload_sha256"],
            segment_length=
                segment["segment_length"],
            segment_sha256=
                segment["segment_sha256"],
            segment_path=
                str(segment_paths[segment_id]),
        )

        resolved.append(
            {
                "entry": entry,
                "expected": expected,
            }
        )

    selected = resolved[:3]

    if len(selected) < 2:
        raise RuntimeError(
            "fewer than two benchmark objects"
        )

    if len({
        item["entry"].offset
        for item in selected
    }) < 2:
        raise RuntimeError(
            "benchmark objects lack distinct offsets"
        )

    for item in selected:
        entry = item["entry"]

        if (
            entry.object_file_sha256
            == entry.payload_sha256
        ):
            raise RuntimeError(
                "payload/object hash distinction missing"
            )

    return generation_pk, selected


def direct_nohash_reference(entry):
    fd = None

    try:
        fd = os.open(
            entry.segment_path,
            open_flags(),
        )

        st = os.fstat(fd)

        if not stat.S_ISREG(st.st_mode):
            raise RuntimeError(
                "direct reference nonregular segment"
            )

        if st.st_size != entry.segment_length:
            raise RuntimeError(
                "direct reference segment length mismatch"
            )

        data = os.pread(
            fd,
            entry.length,
            entry.offset,
        )

        if len(data) != entry.length:
            raise RuntimeError(
                "direct reference short read"
            )

        return data

    finally:
        if fd is not None:
            os.close(fd)


def whole_segment_hash_reference(entry):
    fd = None

    try:
        fd = os.open(
            entry.segment_path,
            open_flags(),
        )

        st = os.fstat(fd)

        if not stat.S_ISREG(st.st_mode):
            raise RuntimeError(
                "whole-hash reference nonregular segment"
            )

        if st.st_size != entry.segment_length:
            raise RuntimeError(
                "whole-hash reference segment length mismatch"
            )

        raw = os.pread(
            fd,
            entry.segment_length,
            0,
        )

        if len(raw) != entry.segment_length:
            raise RuntimeError(
                "whole-hash reference short read"
            )

        if (
            sha256_bytes(raw)
            != entry.segment_sha256
        ):
            raise RuntimeError(
                "whole-hash reference hash mismatch"
            )

        return raw[
            entry.offset:
            entry.offset + entry.length
        ]

    finally:
        if fd is not None:
            os.close(fd)


def reader_v1(entry, generation_pk):
    return reader.read_serialized_object(
        entry,
        generation_pk,
    )


def nearest_rank_p95(values):
    ordered = sorted(values)

    rank = (
        95 * len(ordered) + 99
    ) // 100

    return ordered[
        max(0, rank - 1)
    ]


def stats(values):
    return {
        "count": len(values),
        "min_ns": min(values),
        "max_ns": max(values),
        "mean_ns": statistics.fmean(values),
        "median_ns": statistics.median(values),
        "p95_ns": nearest_rank_p95(values),
    }


def rate_stats(values):
    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "mean": statistics.fmean(values),
        "median": statistics.median(values),
        "p95": nearest_rank_p95(values),
    }


def throughput_stats(latencies_ns, bytes_per_operation):
    if isinstance(bytes_per_operation, int):
        byte_counts = [
            bytes_per_operation
            for _ in latencies_ns
        ]
    else:
        byte_counts = list(
            bytes_per_operation
        )

    if len(byte_counts) != len(latencies_ns):
        raise RuntimeError(
            "throughput byte-count/sample mismatch"
        )

    if any(
        latency <= 0
        for latency in latencies_ns
    ):
        raise RuntimeError(
            "nonpositive benchmark latency"
        )

    operations_per_second = [
        1_000_000_000.0 / latency
        for latency in latencies_ns
    ]

    bytes_per_second = [
        byte_count
        * 1_000_000_000.0
        / latency
        for latency, byte_count
        in zip(
            latencies_ns,
            byte_counts,
        )
    ]

    mib_per_second = [
        value / (1024.0 * 1024.0)
        for value in bytes_per_second
    ]

    return {
        "operations_per_second":
            rate_stats(
                operations_per_second
            ),

        "bytes_per_second":
            rate_stats(
                bytes_per_second
            ),

        "mib_per_second":
            rate_stats(
                mib_per_second
            ),
    }


def measure_all(generation_pk, fixtures):
    mode_names = [
        "reader_v1",
        "direct_nohash_reference",
        "whole_segment_hash_reference",
    ]

    raw_samples = {}
    all_returns_exact = True

    gc_was_enabled = gc.isenabled()

    try:
        gc.disable()

        for fixture_index, fixture in enumerate(fixtures):
            entry = fixture["entry"]
            expected = fixture["expected"]

            functions = {
                "reader_v1":
                    lambda: reader_v1(
                        entry,
                        generation_pk,
                    ),

                "direct_nohash_reference":
                    lambda: direct_nohash_reference(
                        entry
                    ),

                "whole_segment_hash_reference":
                    lambda: whole_segment_hash_reference(
                        entry
                    ),
            }

            for name in mode_names:
                for _ in range(WARMUP):
                    data = functions[name]()

                    if data != expected:
                        raise RuntimeError(
                            "warmup returned incorrect bytes: "
                            + name
                        )

            object_key = str(
                fixture_index
            )

            raw_samples[object_key] = {
                name: []
                for name in mode_names
            }

            for iteration in range(REPEATS):
                shift = iteration % 3

                order = (
                    mode_names[shift:]
                    + mode_names[:shift]
                )

                for name in order:
                    t0 = time.perf_counter_ns()

                    data = functions[name]()

                    t1 = time.perf_counter_ns()

                    if data != expected:
                        all_returns_exact = False
                        raise RuntimeError(
                            "measured call returned "
                            "incorrect bytes: "
                            + name
                        )

                    raw_samples[
                        object_key
                    ][name].append(
                        t1 - t0
                    )

    finally:
        if gc_was_enabled:
            gc.enable()

    return (
        raw_samples,
        all_returns_exact,
    )


def summarize(fixtures, raw_samples):
    mode_names = [
        "reader_v1",
        "direct_nohash_reference",
        "whole_segment_hash_reference",
    ]

    per_object = {}

    aggregate_latencies = {
        mode: []
        for mode in mode_names
    }

    aggregate_returned_bytes = {
        mode: []
        for mode in mode_names
    }

    aggregate_segment_bytes = []

    for index, fixture in enumerate(fixtures):
        key = str(index)
        entry = fixture["entry"]

        mode_stats = {}

        for mode, values in raw_samples[key].items():
            record = {
                "latency":
                    stats(values),

                "throughput":
                    throughput_stats(
                        values,
                        entry.length,
                    ),
            }

            if (
                mode
                == "whole_segment_hash_reference"
            ):
                record[
                    "segment_processing_throughput"
                ] = throughput_stats(
                    values,
                    entry.segment_length,
                )

            mode_stats[mode] = record

            aggregate_latencies[
                mode
            ].extend(values)

            aggregate_returned_bytes[
                mode
            ].extend(
                [
                    entry.length
                    for _ in values
                ]
            )

            if (
                mode
                == "whole_segment_hash_reference"
            ):
                aggregate_segment_bytes.extend(
                    [
                        entry.segment_length
                        for _ in values
                    ]
                )

        reader_latency_median = (
            mode_stats[
                "reader_v1"
            ]["latency"]["median_ns"]
        )

        direct_latency_median = (
            mode_stats[
                "direct_nohash_reference"
            ]["latency"]["median_ns"]
        )

        whole_latency_median = (
            mode_stats[
                "whole_segment_hash_reference"
            ]["latency"]["median_ns"]
        )

        reader_ops_median = (
            mode_stats[
                "reader_v1"
            ]["throughput"][
                "operations_per_second"
            ]["median"]
        )

        direct_ops_median = (
            mode_stats[
                "direct_nohash_reference"
            ]["throughput"][
                "operations_per_second"
            ]["median"]
        )

        whole_ops_median = (
            mode_stats[
                "whole_segment_hash_reference"
            ]["throughput"][
                "operations_per_second"
            ]["median"]
        )

        reader_mib_median = (
            mode_stats[
                "reader_v1"
            ]["throughput"][
                "mib_per_second"
            ]["median"]
        )

        direct_mib_median = (
            mode_stats[
                "direct_nohash_reference"
            ]["throughput"][
                "mib_per_second"
            ]["median"]
        )

        whole_mib_median = (
            mode_stats[
                "whole_segment_hash_reference"
            ]["throughput"][
                "mib_per_second"
            ]["median"]
        )

        per_object[key] = {
            "object_pk":
                entry.object_pk,

            "segment_id":
                entry.segment_id,

            "offset":
                entry.offset,

            "length":
                entry.length,

            "segment_length":
                entry.segment_length,

            "modes":
                mode_stats,

            "ratios": {
                "latency": {
                    "reader_over_direct_median":
                        reader_latency_median
                        / direct_latency_median,

                    "whole_over_reader_median":
                        whole_latency_median
                        / reader_latency_median,
                },

                "throughput": {
                    "reader_over_direct_ops_median":
                        reader_ops_median
                        / direct_ops_median,

                    "whole_over_reader_ops_median":
                        whole_ops_median
                        / reader_ops_median,

                    "reader_over_direct_mib_median":
                        reader_mib_median
                        / direct_mib_median,

                    "whole_over_reader_mib_median":
                        whole_mib_median
                        / reader_mib_median,
                },
            },
        }

    aggregate = {}

    for mode in mode_names:
        values = aggregate_latencies[mode]

        aggregate[mode] = {
            "latency":
                stats(values),

            "throughput":
                throughput_stats(
                    values,
                    aggregate_returned_bytes[
                        mode
                    ],
                ),
        }

    whole_values = aggregate_latencies[
        "whole_segment_hash_reference"
    ]

    aggregate[
        "whole_segment_hash_reference"
    ][
        "segment_processing_throughput"
    ] = throughput_stats(
        whole_values,
        aggregate_segment_bytes,
    )

    reader_latency_median = (
        aggregate[
            "reader_v1"
        ]["latency"]["median_ns"]
    )

    direct_latency_median = (
        aggregate[
            "direct_nohash_reference"
        ]["latency"]["median_ns"]
    )

    whole_latency_median = (
        aggregate[
            "whole_segment_hash_reference"
        ]["latency"]["median_ns"]
    )

    reader_ops_median = (
        aggregate[
            "reader_v1"
        ]["throughput"][
            "operations_per_second"
        ]["median"]
    )

    direct_ops_median = (
        aggregate[
            "direct_nohash_reference"
        ]["throughput"][
            "operations_per_second"
        ]["median"]
    )

    whole_ops_median = (
        aggregate[
            "whole_segment_hash_reference"
        ]["throughput"][
            "operations_per_second"
        ]["median"]
    )

    reader_mib_median = (
        aggregate[
            "reader_v1"
        ]["throughput"][
            "mib_per_second"
        ]["median"]
    )

    direct_mib_median = (
        aggregate[
            "direct_nohash_reference"
        ]["throughput"][
            "mib_per_second"
        ]["median"]
    )

    whole_mib_median = (
        aggregate[
            "whole_segment_hash_reference"
        ]["throughput"][
            "mib_per_second"
        ]["median"]
    )

    aggregate["ratios"] = {
        "latency": {
            "reader_over_direct_median":
                reader_latency_median
                / direct_latency_median,

            "whole_over_reader_median":
                whole_latency_median
                / reader_latency_median,
        },

        "throughput": {
            "reader_over_direct_ops_median":
                reader_ops_median
                / direct_ops_median,

            "whole_over_reader_ops_median":
                whole_ops_median
                / reader_ops_median,

            "reader_over_direct_mib_median":
                reader_mib_median
                / direct_mib_median,

            "whole_over_reader_mib_median":
                whole_mib_median
                / reader_mib_median,
        },
    }

    return per_object, aggregate

def run_benchmark():
    source_before = source_fingerprint()
    fd_before = fd_count()

    generation_pk, fixtures = resolve_entries()

    fixture_checks = {
        "fixture_count_at_least_two":
            len(fixtures) >= 2,

        "fixture_offsets_distinct":
            len({
                item["entry"].offset
                for item in fixtures
            }) >= 2,

        "fixture_object_hashes_exact":
            all(
                sha256_bytes(
                    item["expected"]
                )
                == item[
                    "entry"
                ].object_file_sha256
                for item in fixtures
            ),

        "fixture_payload_hashes_distinct":
            all(
                item[
                    "entry"
                ].object_file_sha256
                != item[
                    "entry"
                ].payload_sha256
                for item in fixtures
            ),
    }

    raw_samples, returns_exact = (
        measure_all(
            generation_pk,
            fixtures,
        )
    )

    per_object, aggregate = summarize(
        fixtures,
        raw_samples,
    )

    fd_after = fd_count()
    source_after = source_fingerprint()

    checks = {
        "protocol_identity":
            sha256_file(PROTOCOL)
            == EXPECTED_PROTOCOL_SHA256,

        "engine_identity":
            sha256_file(ENGINE)
            == EXPECTED_ENGINE_SHA256,

        "resident_identity":
            sha256_file(RESIDENT)
            == EXPECTED_RESIDENT_SHA256,

        "functional_validation_identity":
            sha256_file(
                VALIDATION_RESULT
            )
            == EXPECTED_VALIDATION_RESULT_SHA256,

        **fixture_checks,

        "all_returns_exact":
            returns_exact,

        "source_unchanged":
            source_before
            == source_after,

        "fd_balanced":
            (
                True
                if fd_before is None
                or fd_after is None
                else fd_before == fd_after
            ),
    }

    benchmark_valid = all(
        value is True
        for value in checks.values()
    )

    fixtures_json = []

    for fixture in fixtures:
        entry = fixture["entry"]

        fixtures_json.append({
            "object_pk":
                entry.object_pk,

            "segment_id":
                entry.segment_id,

            "offset":
                entry.offset,

            "length":
                entry.length,

            "object_file_sha256":
                entry.object_file_sha256,

            "payload_sha256":
                entry.payload_sha256,

            "segment_length":
                entry.segment_length,

            "segment_sha256":
                entry.segment_sha256,

            "segment_path":
                entry.segment_path,
        })

    return {
        "schema": SCHEMA,

        "protocol_sha256":
            EXPECTED_PROTOCOL_SHA256,

        "engine_sha256":
            EXPECTED_ENGINE_SHA256,

        "resident_sha256":
            EXPECTED_RESIDENT_SHA256,

        "functional_validation_result_sha256":
            EXPECTED_VALIDATION_RESULT_SHA256,

        "source_manifest":
            str(SOURCE_MANIFEST),

        "source_manifest_sha256":
            sha256_file(
                SOURCE_MANIFEST
            ),

        "source_fingerprint_before":
            source_before,

        "source_fingerprint_after":
            source_after,

        "configuration": {
            "clock":
                "time.perf_counter_ns",

            "warmup_per_object_per_mode":
                WARMUP,

            "repeats_per_object_per_mode":
                REPEATS,

            "mode_order":
                "deterministic rotating order",

            "gc_disabled_during_measurement":
                True,

            "performance_threshold":
                None,

            "throughput_metrics": {
                "operations_per_second":
                    "1e9 / latency_ns",

                "returned_bytes_per_second":
                    "object_length * 1e9 / latency_ns",

                "returned_mib_per_second":
                    "returned_bytes_per_second / 1048576",

                "whole_segment_bytes_per_second":
                    "segment_length * 1e9 / latency_ns",

                "whole_segment_mib_per_second":
                    "whole_segment_bytes_per_second / 1048576",
            },
        },

        "fixtures":
            fixtures_json,

        "raw_samples_ns":
            raw_samples,

        "per_object":
            per_object,

        "aggregate":
            aggregate,

        "fd_before":
            fd_before,

        "fd_after":
            fd_after,

        "checks":
            checks,

        "benchmark_valid":
            benchmark_valid,

        "fatal_error":
            None,
    }


def fatal_result(exc):
    return {
        "schema": SCHEMA,

        "protocol_sha256":
            EXPECTED_PROTOCOL_SHA256,

        "engine_sha256":
            EXPECTED_ENGINE_SHA256,

        "resident_sha256":
            EXPECTED_RESIDENT_SHA256,

        "functional_validation_result_sha256":
            EXPECTED_VALIDATION_RESULT_SHA256,

        "benchmark_valid":
            False,

        "fatal_error": {
            "type":
                type(exc).__name__,

            "message":
                str(exc),
        },
    }


def main():
    if RESULT.exists():
        raise RuntimeError(
            "benchmark result already exists; "
            "exact-once execution forbidden"
        )

    if (
        sha256_file(PROTOCOL)
        != EXPECTED_PROTOCOL_SHA256
    ):
        raise RuntimeError(
            "benchmark protocol identity mismatch"
        )

    if (
        sha256_file(ENGINE)
        != EXPECTED_ENGINE_SHA256
    ):
        raise RuntimeError(
            "Segment Reader identity mismatch"
        )

    if (
        sha256_file(RESIDENT)
        != EXPECTED_RESIDENT_SHA256
    ):
        raise RuntimeError(
            "Resident PK dependency identity mismatch"
        )

    if (
        sha256_file(VALIDATION_RESULT)
        != EXPECTED_VALIDATION_RESULT_SHA256
    ):
        raise RuntimeError(
            "functional validation identity mismatch"
        )

    try:
        result = run_benchmark()
    except Exception as exc:
        result = fatal_result(exc)

    write_json_exclusive(
        RESULT,
        result,
    )

    if not result.get(
        "benchmark_valid",
        False,
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
