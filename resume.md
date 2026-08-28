# OpenMind — Compact Handoff Resume

## Where We Are

Repository:

    ~/OpenMind

Branch:

    labs/multidimensional-maf

Authoritative research HEAD before this docs-only handoff commit:

    e0b1443

Current major phase:

    Phase 6B — Model Catalog and Segment Store

Current active component:

    Phase 6B.10 — Segment Reader V1

Phase 6B.9 Resident PK Directory is complete.

Phase 6C has NOT started.

No upstream push is requested. Upstream pushes should wait for Wi-Fi.

---

## Working Protocol

Use one safety-gated step at a time.

For Termux blocks:

- start from `~/OpenMind`;
- disable Git pagers;
- avoid `exit` / `logout`;
- never use broad `git add .`, `git add -A`, `git clean`, or broad stash;
- stage only named files;
- preserve negative evidence;
- freeze protocols/runners before execution;
- exact-once executions are never automatically rerun;
- never alter a frozen implementation merely to satisfy a defective external auditor;
- fix the auditor semantics instead.

Only paste compact GOLD STANDARD RETURN PACKETS back to ChatGPT.

---

## Frozen Segment Reader V1

Protocol:

    experiments/model_fractal/MAF_SEGMENT_READER_V1_PROTOCOL.md

SHA256:

    192402f1e4f2d41540d225cce7629757152b9996a9adffaafeab6674e13f0f5d

Engine commit:

    d9eb8ad research: implement MAF segment reader v1

Engine:

    experiments/model_fractal/maf_segment_reader_v1.py

SHA256:

    3499cb8e528fe8e9315e3e5656d6aa888c95ca175310b6371e722de409827369

Resident PK engine dependency SHA256:

    4dadac5a1ffe448437718432edeee14a219a20da5a54956d2884d0b0b1d426b6

### Reader Contract

API:

    read_serialized_object(entry, expected_generation_pk)

Input is a frozen `ResidentPKEntry` plus the expected generation PK.

Generation mismatch must fail before physical storage access.

`offset:length` addresses serialized object-file bytes inside the immutable `.mafseg`, NOT raw payload bytes.

Returned bytes must hash to:

    object_file_sha256

They must NOT be verified against:

    payload_sha256

Physical read contract:

- validate offset/length/segment_length;
- open `segment_path` read-only;
- flags are exactly `O_RDONLY` plus optional `O_CLOEXEC`;
- same FD is used for `fstat` and `pread`;
- target must be a regular file;
- actual size must equal `segment_length`;
- positional read must return exactly `length` bytes;
- returned range SHA256 must equal `object_file_sha256`;
- descriptor closes in `finally`.

No JSON/manifest discovery, source GGUF access, whole-segment hashing per read, payload decoding, FD cache, mmap residency, or Phase 6C functionality belongs in V1.

---

## Frozen Functional Validation

Preregistration commit:

    e0b1443 research: preregister MAF segment reader validation v1

Validation protocol:

    experiments/model_fractal/MAF_SEGMENT_READER_VALIDATION_V1_PROTOCOL.md

SHA256:

    c896e6b68be67352e4b09ed8f6486cdea2e20435fa03c7c44fd4871051e202be

Validation runner:

    experiments/model_fractal/maf_segment_reader_validation_v1.py

SHA256:

    1f5cfdba3d3bd681eb78b07d98b9ee49497a3608bc51408c7e503b0dbc80bf88

Validation has NEVER executed.

The following must currently remain absent:

    experiments/model_fractal/maf_segment_reader_validation_v1.json
    results/runtime/maf_segment_reader_validation_v1

When authorized, the runner may execute exactly once.

Its first raw result is preserved whether PASS or FAIL.

The frozen matrix covers:

- exact serialized-object reconstruction;
- multiple physical offsets;
- object-file SHA verification;
- payload-hash distinction;
- generation rejection before I/O;
- invalid entry/range rejection;
- missing segment;
- non-regular target;
- segment-length mismatch;
- forced short read;
- same-size object corruption;
- wrong object hash;
- frozen-entry behavior;
- repeated FD balance on success and failures;
- read-only open flags;
- static hot-path prohibitions;
- preserved-source immutability.

---

## Final-Preflight History

The validation protocol/runner are not known defective.

Several external preregistration/preflight auditors produced false positives and were investigated read-only.

### Resolved auditor false positive 1

The auditor recursively walked top-level function definitions and counted 18 legitimate `reader.read_serialized_object()` calls inside `run_validation()` as module-level execution.

Resolved facts:

    module-scope reader calls = 0
    run_validation reader calls = 18

### Resolved auditor false positive 2

A blanket `.gguf` text search found the runner's own prohibition detector:

    ".gguf" not in source.lower()

Structural audit proved:

    GGUF detector assignments = 1
    GGUF path assignments = 0
    GGUF access calls = 0
    module GGUF values = 0

### Resolved auditor false positive 3

The first final preflight searched for AST attributes such as `os.O_WRONLY`.

The frozen runner instead enumerates prohibited flags as strings and resolves them dynamically.

Structural audit proved coverage for all five:

    O_APPEND
    O_CREAT
    O_RDWR
    O_TRUNC
    O_WRONLY

It records actual `os.open()` flags and verifies:

    flags & prohibited_flags == 0

### Resolved auditor false positive 4

A textual check incorrectly reported optional `O_CLOEXEC` handling absent.

Structural audit proved the engine constructs the open mode as:

    flags = os.O_RDONLY

then, when available:

    flags |= os.O_CLOEXEC

Actual reader flag attributes:

    O_CLOEXEC,O_RDONLY

Write-capable reader flags:

    NONE

Termux reports `O_CLOEXEC` available with value `524288`.

Classification:

    CLOEXEC_TEXT_AUDITOR_FALSE_POSITIVE_ONLY

---

## Last Completed Gate

Phase:

    6B.10f2 — O_CLOEXEC semantic root-cause audit

Result:

    PASS

Important values:

    RDONLY assignments = 1
    CLOEXEC guards = 1
    os.open using flags = 1
    allowed flags only = True
    write flags = NONE
    semantic pass = True

Validation execution remained:

    NONE

Validation result:

    ABSENT

Validation runtime:

    ABSENT

Staging:

    EMPTY

---


## Phase 6B.10 Segment Reader V1 — Exact-Once Validation Evidence

The frozen Segment Reader V1 functional-validation runner has executed exactly once.

Execution parent HEAD:

    66be27b

Validation runner SHA256:

    1f5cfdba3d3bd681eb78b07d98b9ee49497a3608bc51408c7e503b0dbc80bf88

Runner exit code:

    0

Raw result:

    experiments/model_fractal/maf_segment_reader_validation_v1.json

Raw result SHA256:

    1ceef1ed2b814da3951811ea97e9f4475b3fa79557b341e7c8e089ec8a409328

Result schema:

    openmind.maf_segment_reader_validation.v1

Result all_pass:

    True

Checks:

    total = 39
    passed = 39
    failed = 0
    first failure = NONE

Fatal error type:

    NONE

Fatal error message:

    NONE

Preserved source evidence unchanged:

    True

Validation runtime:

    results/runtime/maf_segment_reader_validation_v1

Runtime files:

    2

Runtime bytes:

    8193

This execution is historical exact-once evidence.

DO NOT execute maf_segment_reader_validation_v1.py again.

DO NOT clean or overwrite the validation runtime.

DO NOT alter the first raw result.


## Phase 6B.10 Segment Reader V1 — Benchmark V1 Preregistered

Functional validation is accepted and its exact-once runner is permanently forbidden from rerun.

Benchmark V1 protocol:

    experiments/model_fractal/MAF_SEGMENT_READER_BENCHMARK_V1_PROTOCOL.md

SHA256:

    48263a8c6e57c4e3739f0c1c2eeef1a85c4ab04bc53b7b24762aaacff889d55b

Benchmark V1 runner:

    experiments/model_fractal/benchmark_maf_segment_reader_v1.py

SHA256:

    2972beda0d1a798cf5da9bf6371f5c0c96ee493ce6903da68021cec64e7947d4

Benchmark execution:

    NONE

Benchmark result:

    ABSENT

Frozen configuration:

    warmup = 100 per object/mode
    measured repeats = 1000 per object/mode
    clock = time.perf_counter_ns
    mode order = deterministic rotating
    raw timing samples = preserved
    performance threshold = NONE / observational

Modes:

    reader_v1
    direct_nohash_reference
    whole_segment_hash_reference

Throughput is mandatory alongside latency.

Every applicable per-object and aggregate report includes:

    operations/second
    returned bytes/second
    returned MiB/second

Whole-segment-hash mode additionally includes:

    full segment processing bytes/second
    full segment processing MiB/second

Throughput is derived deterministically from the raw timing samples and actual byte counts.

Latency and throughput ratios are descriptive only.

The original prereg static failure was an auditor false positive caused by treating the canonical __main__ guard as module-scope benchmark execution. The corrected structural audit permits only the canonical guard and rejects real unsafe module-level calls.

## Exact Next Task

Perform the final read-only Benchmark V1 preflight.

Do not execute Benchmark V1 yet.

The preflight must confirm the frozen hashes above and revalidate:

- benchmark result absent;
- source fixture identity;
- fixture count and distinct offsets;
- exact object bytes and payload-hash distinction;
- all three benchmark modes;
- read-only flags;
- timer boundaries;
- deterministic rotation;
- raw timing preservation;
- latency statistics;
- operations/s throughput;
- returned bytes/s and MiB/s throughput;
- full-segment processing throughput for whole-hash mode;
- sample-specific aggregate byte accounting;
- latency and throughput ratios;
- no manifest/JSON work in the timed orchestrator;
- exact-once publication;
- no cleanup;
- no validation rerun.

Only after that read-only preflight passes may Benchmark V1 execute exactly once.

Do not start Phase 6C.

Do not push upstream.
