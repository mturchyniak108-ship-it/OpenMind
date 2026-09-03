# OpenMind Current Work

## Scientific authority
- branch: `labs/multidimensional-maf`
- frozen runner commit: `15d8046ab4fd83373273e28d4a82ed581f8fd9bf`
- runner SHA256: `e2e32f85b1dc7015802ec51a6f214188becc5d35f45c76f4b320617ccd6cd873`

## Phase state
- 6B: closed
- 6C: closed
- 6D: active
- 6D-Q: active preregistered query-to-PK validation
- 6E: not entered

## Q2
Runner source is complete, frozen, and statically audited: `25 PASS / 0 FAIL`.

Modes: `--qualify-fixtures`, `--qualify-backend`, `--readiness`, `--run-exact-once`.

Authoritative order:
`GUARD -> PREQUAL -> RESERVE -> SCIENCE -> V01-V48 -> RESULT -> WRITE/FSYNC -> ATOMIC NO-REPLACE PUBLISH`.

Post-reservation failure preserves partial evidence, does not silently retry, and does not synthesize a replacement result.

## Scientific boundary
- authoritative run: NOT EXECUTED
- result reservation: NONE
- V01-V48: NOT EXECUTED
- result: ABSENT
- partial: ABSENT
- exact-once slot: UNSPENT

Q2 does not yet establish inference, answer generation, selective-working-set sufficiency, tensor avoidance, output parity, answer quality, MAF-native compute, performance improvement, or LLM replacement.

## Authority order
1. exact source/Git commit
2. tests/frozen runner
3. immutable validated results
4. manifests/provenance
5. freeze records
6. current-status docs
7. README/roadmap

Termux click-paste operations are atomic and no-heredoc; see `docs/development/TERMUX_WORKFLOW.md`.

## Next gate
Synchronize this documentation to the remote before exact-once Q2 execution.
