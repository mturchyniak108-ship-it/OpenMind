# MAF Query Route Cache Persistence Portability Recovery V1

Status: preregistration candidate. No production-module correction is authorized until this exact document is independently reviewed and frozen. Q4 V1.2 science is NOT ENTERED.

## 1. Frozen provenance and failure classification

- Frozen production module: `experiments/model_fractal/maf_query_route_cache_v1.py` SHA256 `a168528b47b2575fb18dc68d36a1c31ab6390534a779d5c769299a3dc891d507`.
- Frozen production implementation contract: SHA256 `9f253138399383d703fabd6dc6945af2e94c4af29d5b0f2995c0775984e1cf11`.
- Frozen Q4 validation protocol: SHA256 `af587bfe685deb86ac4574b3d41d1a80b5df2cec84bce757eac8c7e307d82ad9`.
- Frozen Q4 runner implementation contract: SHA256 `1d57f67e5944c6a04e50c3f18c458872b56cf45937ba04b72d529b0b78aec20c`.
- Frozen Q4 V1.1 runner: SHA256 `d323cd19fa224d4d33339d5ba9b0f22b8c903a4717b35bad9eec8a9bd455332c`.
- Frozen Q4 V1.1 failed result: SHA256 `14f7932db07ea3d8358a6dfacda9dd5ffcf2b728208bb6830ff7a5363c6369ba`.
- Frozen Q4 V1.1 permanent slot: SHA256 `5ff247ebf2c341b86979758031d947f6c2bf71282c7d2a0670a5c718cdf84902`.
- Q4 V1.1 is permanently spent and MUST NOT be rerun.
- V1.1 completed zero Q4 checks and zero frozen query cases before the post-reservation persistence failure.
- The V1.1 failure is classified as a production persistence implementation / Termux platform-portability defect, not a scientific rejection of the route-cache design.

## 2. Frozen persistence semantics that MUST NOT be weakened

The existing production implementation contract requires this ordered persistence behavior:

1. Canonicalize the record bytes.
2. If the final path already exists, accept only byte-identical canonical content as idempotent success.
3. Otherwise create a sibling partial file with exclusive creation.
4. Write the complete canonical bytes to the partial.
5. Flush and fsync the complete partial.
6. Atomically publish the complete record without overwriting an existing final path.
7. Fsync the containing directory after publication.

A pre-existing different final record MUST continue to fail closed. A reader MUST never be intentionally exposed to a partially written final record. No fallback may use ordinary `os.replace`, ordinary `os.rename`, or direct incremental writes to the final path because those mechanisms do not preserve the complete frozen semantic set.

## 3. Proven Termux primitive

On the validated Android/Termux platform, Python `os.link` is absent. A non-scientific temporary-filesystem probe established that libc exports `renameat2` and that `renameat2(AT_FDCWD, src, AT_FDCWD, dst, RENAME_NOREPLACE)`:

- atomically publishes the already-complete source file;
- does not overwrite an existing destination;
- returns `EEXIST` when the destination already exists;
- leaves the source partial intact on `EEXIST`;
- removes the source partial from its old name on successful publication;
- preserves the frozen atomic full-content visibility and no-overwrite requirements;
- requires no contract weakening.

The libc hard-link symbol is not an accepted fallback for this recovery because the same Termux probe returned `EACCES` for the first hard-link publication attempt.

## 4. Preregistered production-module correction

The production-module correction MUST be limited to the persistence publication mechanism and its required standard-library support.

The corrected module shall add only the standard-library support required to call libc `renameat2` through `ctypes` and interpret errno values. No third-party dependency is permitted.

The corrected module shall introduce one small internal helper with the semantic role `_atomic_publish_noreplace_v1(partial: Path, path: Path) -> None`.

That helper MUST:

1. Load the current process libc with `ctypes.CDLL(None, use_errno=True)`.
2. Require a `renameat2` symbol and fail closed if it is unavailable.
3. Bind arguments equivalent to `(int, char *, int, char *, unsigned int)` and integer return type.
4. Use `AT_FDCWD = -100` and `RENAME_NOREPLACE = 1`.
5. Encode filesystem paths with `os.fsencode`.
6. Invoke `renameat2(AT_FDCWD, partial, AT_FDCWD, path, RENAME_NOREPLACE)` exactly once for one publication attempt.
7. Return normally only when the libc call returns zero.
8. On return `-1` with errno `EEXIST`, raise `FileExistsError` so the existing frozen collision/idempotence branch remains authoritative.
9. On any other libc failure, raise `OSError` carrying the observed errno so the existing persistence fail-closed handling remains authoritative.
10. Never fall back to overwrite-capable `os.replace`, ordinary `os.rename`, direct final-path writes, or another weaker publication mechanism.

Inside `write_route_cache_record_v1`, the sole publication-site semantic replacement shall be the current `os.link(partial, path)` call with the preregistered no-replace helper call.

The pre-publication exclusive partial creation, complete write loop, partial fsync, existing-final byte comparison, canonical validation, different-content rejection, final readback, directory fsync, and cleanup behavior MUST remain scientifically and semantically unchanged.

Successful `renameat2(..., RENAME_NOREPLACE)` publication consumes the partial pathname. The already-existing cleanup branch that treats an absent partial as a known `FileNotFoundError` cleanup escape shall remain valid and MUST NOT reinterpret successful publication as failure.

On an `EEXIST` collision, the partial remains present until the existing collision branch reads and validates the final path; ordinary cleanup then removes the partial. Identical existing content remains idempotent success and different existing content remains fail-closed.

## 5. Explicitly forbidden production changes

This recovery MUST NOT change:

- `MAFQueryRouteCacheRecordV1` fields or schema;
- canonical serialization;
- cache identity or `cache_pk` construction;
- route payload digest semantics;
- query/source/config identity semantics;
- object-PK or relationship-PK validation;
- metadata-only persistence requirements;
- cache reuse or invalidation rules;
- Q3 cleanup interaction;
- public API names or signatures;
- scientific check definitions, frozen query cases, thresholds, or claim boundaries.

No new persistence fallback is authorized beyond the preregistered `renameat2(..., RENAME_NOREPLACE)` mechanism.

## 6. Required correction workflow

The sequence is frozen as follows:

1. Independently review this exact preregistration candidate.
2. Freeze this preregistration as a sole-path commit.
3. Create the corrected production-module candidate only after that freeze.
4. Audit the corrected module against the frozen module and this preregistration; only the preregistered portability delta is permitted.
5. Compile and perform focused non-scientific persistence tests, including first publication, identical idempotent write, different-content no-overwrite rejection, canonical readback, partial cleanup, and directory durability behavior.
6. Independently review and freeze the corrected production module as a sole-path commit.
7. Supersede the Q4 runner implementation contract only as necessary to bind the corrected frozen production-module SHA. No scientific check or claim meaning may change.
8. Independently review and freeze that runner-contract supersession.
9. Create a Q4 V1.2 runner candidate derived from the frozen V1.1 runner only after the corrected module and superseded runner contract have frozen hashes.
10. The V1.2 runner delta may update only the fresh V1.2 execution namespace plus the corrected production-module and superseded runner-contract bindings required by those frozen artifacts. No Q4 science change is permitted.
11. Independently review, compile without execution, and freeze the V1.2 runner.
12. Reverify the unused V1.2 namespace and perform a final read-only pre-arm gate before any V1.2 execution.

## 7. Fresh Q4 V1.2 exact-once namespace

- Runner: `experiments/model_fractal/maf_query_route_cache_validation_v1_2.py`
- Result: `experiments/model_fractal/maf_query_route_cache_validation_v1_2.json`
- Permanent slot: `experiments/model_fractal/maf_query_route_cache_validation_v1_2.slot`
- Transient publication partial: `experiments/model_fractal/maf_query_route_cache_validation_v1_2.json.partial`

All four V1.2 execution paths MUST be absent before execution. Creation or review of source candidates does not enter Q4 V1.2 science.

Once the V1.2 durable slot reaches its durable reservation state, Q4 V1.2 is permanently spent whether execution passes, fails, or aborts. No retry is permitted in the V1.2 namespace.

## 8. Scientific boundary

This portability recovery does not establish a Q4 scientific PASS. Q4 has not yet obtained a successful 44/44 validation result.

All original Q4-V01 through Q4-V44 checks, their order and meanings, and frozen cases `q001`, `q025`, `q026`, and `q033` remain unchanged.

No inference, answer generation, working-set sufficiency, performance superiority, output parity, route-expansion optimality, LLM replacement, or MAF-native-compute claim is authorized.

Phase 6E remains NOT ENTERED.
