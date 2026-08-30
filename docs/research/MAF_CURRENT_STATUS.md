# MAF Current Research Status

This document is the stable documentation index for OpenMind's current MAF
research state.

Scientific authority remains the canonical local research lineage:

- branch: `labs/multidimensional-maf`
- canonical HEAD: `620d13747e34c637afbda029fd0857541e1d5536`

The GitHub-safe research publication is:

- branch: `research/multidimensional-maf-public`
- publication HEAD: `e8e5e0e517fc99966190f1ee773e2bbc89feb905`

This document summarizes research state. It does not promote experimental
implementations into production capability.

## Phase 6B

**CLOSED.**

The catalog, immutable-generation, activation/rollback, Resident PK Directory,
and Segment Reader progression completed the defined Phase 6B research line.

## Phase 6C

**CLOSED — VALIDATED PASS.**

MAF Object Runtime and Residency completed V1.3 validation and was formally
closed before Phase 6D began.

## Phase 6D

**ACTIVE RESEARCH.**

Current work concerns segment locality, telemetry persistence, and later
path-aware physical organization while preserving logical PK identity.

### Locality Data Model V1

**VALIDATED PASS / FORMALLY FROZEN.**

### Telemetry Snapshot Persistence V1

**FROZEN PREDECESSOR / VALIDATION SLOT UNSPENT.**

Its frozen validation runner remains unexecuted.

### Telemetry Snapshot Persistence V1.1

**IMPLEMENTATION FROZEN / VALIDATION PREREGISTERED / NOT YET EXECUTED.**

At canonical HEAD `620d13747e34c637afbda029fd0857541e1d5536`:

- the V1.1 persistence protocol is frozen;
- the Android-compatible V1.1 implementation is frozen;
- the V1.1 validation protocol is frozen;
- the V1.1 validation runner is not yet frozen;
- the V1.1 exact-once validation slot is unspent.

No V1.1 scientific validation result exists yet.

## Phase 6D-Q

**PROPOSED / ROADMAP ONLY / NOT ACTIVE.**

Query-scoped MAF working sets and reusable PK route caching remain prospective
research. Current evidence does not establish prompt-to-PK sufficiency,
tensor/object avoidance, output parity, or a performance advantage.

## Phase 6E

**NOT ENTERED.**

Selective working-set sufficiency, bounded expansion, actual tensor/object
avoidance, and output-parity experiments remain future gates.

## Heavyweight benchmark evidence

The frozen Segment Reader V1.2 benchmark raw result is intentionally excluded
from normal Git history because it is 323,334,664 bytes.

Frozen raw evidence:

- SHA256: `44b15ba5a02492f9a7c79cda3120c0cb4b6b398201eacb5f5249f38a281e5a54`

Published compressed evidence:

- release tag: `openmind-maf-segment-reader-benchmark-v1.2-artifact`
- compressed bytes: `4546962`
- compressed SHA256: `9bf27fcefbed59d8f372dd18e0b31b547f3ba8fd94556ea9f4b6fbc729f12fc2`

The public research branch contains the protocol, runner, completion record,
manifest, reproduction instructions, and release provenance.

## Branch responsibilities

`main` contains stable project documentation and promoted implementation.

`research/multidimensional-maf-public` contains the GitHub-safe research
snapshot and reproducibility evidence.

`labs/multidimensional-maf` remains the canonical local scientific lineage.

Future experimental branches should be created prospectively from the exact
authorized scientific parent rather than by rewriting frozen research history.
