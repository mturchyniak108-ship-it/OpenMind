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

## Exact Next Task

The next gate is:

    Phase 6B.10f3 — corrected final read-only Segment Reader V1 validation preflight

IT HAS NOT BEEN RUN YET.

Because this handoff updates and commits only `resume.md`, the current Git HEAD after the handoff commit will be newer than `e0b1443`.

Therefore DO NOT paste an older 6B.10f3 block unchanged if it hardcodes:

    EXPECTED_HEAD="e0b1443"

Regenerate the same corrected read-only preflight using the new current HEAD.

The corrected preflight must use semantic predicates for:

- dynamic prohibited-write-flag coverage;
- reader `O_RDONLY` + optional `O_CLOEXEC`;
- module-scope execution;
- GGUF self-check detection.

It must also re-confirm:

- frozen protocol/runner/engine SHA identities;
- validation result absent;
- validation runtime absent;
- exact-once guard order;
- runtime/result exclusive creation;
- fixture selection;
- at least two selected objects with distinct offsets;
- exact object-file hashes;
- payload-hash distinction;
- negative-test write isolation;
- both monkeypatches restored in `finally`;
- FD measurement support;
- no validation execution during preflight.

Required authorization outcome:

    CLASSIFICATION: SEGMENT_READER_V1_VALIDATION_FINAL_PREFLIGHT_PASS
    SAFE TO EXEC : True

Until BOTH are true:

    DO NOT EXECUTE VALIDATION

---

## After Final Preflight Pass

Next sequence only:

1. execute the frozen Segment Reader V1 validation runner exactly once;
2. freeze the first raw result immediately, PASS or FAIL;
3. interpret the result without rerunning;
4. preregister/freeze Segment Reader benchmark;
5. execute/freeze benchmark according to its protocol;
6. preregister/run mandatory post-validation diagnostics;
7. complete/freeze Phase 6B.10;
8. only then consider Phase 6C.

Do not jump directly to 6C.

---

## Historical Evidence — Do Not Rerun

Phase 6B.9 Resident PK Directory is complete.

Especially do not rerun:

- Resident PK functional validation V1;
- failed Resident PK benchmark V1;
- successful Resident PK benchmark V1.1;
- Resident PK diagnostics V1.4.

Resident diagnostics V1/V1.1/V1.2/V1.3 were never validly executed and remain forbidden.

Preserve all existing runtime evidence.

No cleanup.

---

## Phase 6B.9 Reference

Completion commit:

    9ea0294 research: complete MAF resident PK directory phase 6B.9

Resident lookup validated:

- stable generation-bound resident PK entries;
- O(1)-style lookup over the tested range/device only;
- 100K indexed median approximately 260 ns;
- 100K linear median approximately 3.74 ms;
- approximately 14,393x observed speedup;
- no universal production-performance claim.

Diagnostics V1.4 exact-once result:

    45/45 PASS

No fatal error, no write opens, stale-generation rejection passed, FD/resource/degradation/failure-path checks passed.

---

## Scope Guard

Current work proves infrastructure for MAF object access.

It does NOT yet prove:

- MAF-native LLM replacement;
- production storage-engine choice;
- production performance guarantees;
- raw payload/tensor decoding by Segment Reader V1;
- descriptor residency;
- mmap residency;
- FD caching;
- Phase 6C runtime residency;
- selective inference/tensor avoidance;
- end-to-end replacement of a standard LLM runtime.

Keep validated, implemented-but-not-validated, and future claims clearly separated.
