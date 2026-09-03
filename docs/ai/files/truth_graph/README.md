# OpenMind Canonical Truth Graph — AI Documentation

## Status

**Current priority subsystem.**

The Truth Graph is the canonical structured knowledge layer currently used by OpenMind truth-trace resolution.

The verified implementation provides deterministic graph loading, weighted path resolution, evidence binding, provenance auditing, and deterministic CLI/JSON reporting.

## Verified Regression

The canonical truth/provenance subsystem has verified coverage across:

- Truth Graph contracts
- Truth trace resolution
- CLI and JSON reporting
- Evidence registry
- Persistent edge/evidence bindings
- Provenance auditing and coverage
- Artifact ingestion
- Cross-layer provenance
- Adversarial provenance validation
- Persistence input validation
- Experimental fuzzy/vector isolation

Recent focused regression checkpoints include:

- 36 truth/provenance contract tests passed
- 22 ingestion tests passed
- 32 evidence tests passed
- 12 cross-layer provenance tests passed

Exact totals may change as the test suite evolves; individual subsystem
results are the authoritative regression evidence.

## Verified Canonical Pipeline

TruthGraph
  ↓
Weighted directed graph traversal
  ↓
best_path(start, end)
  ↓
TruthTraceResolver
  ↓
EdgeEvidenceBindings
  ↓
EvidenceRegistry
  ↓
audit_truth_trace()
  ↓
Deterministic CLI / JSON report

## Canonical Path Scoring Contract

For a non-empty path: `0.55 * mean(edge.weight) + 0.45 * mean(unique node.truth_confidence) - 0.02 * path_cost`. The result is rounded to 12 decimal places.

`path_cost` is the number of edges. Empty paths score `0.0`.

### Canonical Path Discovery

- Start and end nodes must exist.
- Paths are simple; nodes cannot be revisited.
- Default maximum depth is 8 edges.
- `max_depth` can be explicitly configured.

### Canonical Ordering

Paths are ordered deterministically by descending score, ascending cost, then lexicographically ascending node tuple. `best_path()` returns the first path.

These rules are protected by regression tests.

## Verified Contracts

### Graph

- Graph state is loaded from persistent node and edge JSON.
- Neighbor traversal is deterministic.
- Best-path resolution is deterministic.
- A resolved path preserves its start and end nodes.
- Path scoring is deterministic and finite.

### Truth Trace

- TruthTrace contains start, end, ordered steps, and canonical score.
- TraceStep records source, target, relation, weight, and optional evidence ID.
- Resolution does not mutate the underlying TruthGraph.
- Existing canonical graph scoring is preserved by trace resolution.

### Evidence Binding

- Edge/evidence bindings are persisted separately from the graph.
- A binding maps a directed source/target edge to an evidence record ID.
- A path edge may be REGISTERED, UNBOUND, or MISSING during audit.
- Resolver attachment and evidence validation are separate responsibilities.

### Provenance Audit

- Audit reports total path edges.
- Audit reports registered edges.
- Audit reports unbound edges.
- Audit reports missing evidence references.
- Audit calculates provenance coverage.
- Provenance gaps are explicitly exposed rather than silently ignored.

### Reporting

- CLI output exposes the canonical path, relations, weights, evidence state, score, and provenance coverage.
- JSON reporting exposes the same canonical information in deterministic structure.
- Invalid start/end nodes return NO CANONICAL PATH.
- No resolvable path returns NO CANONICAL PATH.

## Canonical Authority Rule

Only validated structured Truth Graph state may establish canonical knowledge.

Vector similarity, fuzzy membership, ML prediction, predictive weighting, waveform encoding, fractal representation, and multimodal representations are derived signals only.

Derived systems may rank or propose candidates, but they must never silently promote candidates into canonical knowledge.

## Current Limitations

The following are not yet established as canonical implementation contracts:

- semantic TruthNode abstraction beyond the current graph node representation
- formal TruthEdge domain object contract
- contradiction-resolution model
- provenance weighting model
- fuzzy truth membership
- vector-to-TruthNode mapping
- vector-to-TruthEdge mapping
- learned predictive weighting
- multimodal truth representation
- waveform representation
- fractal-memory representation

These remain roadmap or experimental concerns until source code and regression tests establish them.

## Current Engineering Priority

The core Truth Graph, evidence, provenance, ingestion, persistence, and
experimental fuzzy/vector boundaries are now implemented and regression-tested.

The next priority is documentation and contract consolidation:

1. reconcile TruthNode/TruthEdge/TruthPath contracts with source code
2. document canonical persistence formats
3. document deterministic path scoring and ordering
4. document provenance persistence and validation semantics
5. distinguish completed architecture from future research
6. establish benchmark baselines for experimental retrieval layers

Specialized vector, ML, waveform, and fractal retrieval remain derived
experimental systems and must continue to validate candidates against the
canonical Truth Graph.

## AI Output Discipline

Every conclusion must distinguish:

- CANONICAL FACT
- VERIFIED IMPLEMENTATION BEHAVIOR
- EXPERIMENTAL SIGNAL
- MODEL PREDICTION
- FUZZY INFERENCE
- UNRESOLVED HYPOTHESIS

Never merge these categories.

## Canonical Persistence and Provenance Contract

### Truth Graph Persistence

Canonical graph state is loaded from two JSON collections:

- `nodes.json` — canonical `TruthNode` records
- `edges.json` — canonical `TruthEdge` records

`TruthEdge.provenance` is an optional immutable tuple of evidence IDs.
Missing provenance is valid and represents an edge without directly attached
provenance IDs.

### Evidence Records

`EvidenceRecord` is immutable and contains:

- `id`
- `source`
- `claim`
- `confidence`

`EvidenceRegistry`:

- stores evidence by immutable ID
- rejects conflicting duplicate IDs
- permits identical duplicate records idempotently
- returns records in deterministic ID order
- serializes using canonical JSON
- supports deterministic save/load round trips
- rejects non-list persistence input

### Edge Evidence Bindings

`EdgeEvidenceBinding` associates:

`source + target -> evidence_id`

Bindings are immutable and deterministic.

Conflicting bindings for the same directed source/target pair are rejected.

Binding validation verifies that every referenced evidence ID exists in the
`EvidenceRegistry`.

### Evidence Resolution

An edge's evidence state is explicitly one of:

- `REGISTERED` — evidence ID resolves in the registry
- `UNBOUND` — no evidence ID is attached
- `MISSING` — an evidence ID is present but cannot be resolved

Missing provenance is reported explicitly and is never silently treated as
verified evidence.

### Provenance Coverage

`ProvenanceCoverage` reports:

- total edges
- registered edges
- unbound edges
- missing edges
- coverage ratio
- unbound edge pairs
- missing edge pairs

Coverage is a diagnostic property of a trace. It does not change canonical
truth or canonical path score.

### Provenance Invariant

Evidence and provenance must remain separate from canonical path scoring.

The canonical path score is determined by the Truth Graph scoring contract.
Auditing, evidence resolution, and provenance coverage may explain or qualify
a trace, but must never rewrite its canonical score.

### Current Persistence Boundary

The current implementation establishes deterministic JSON persistence for:

- Truth Graph input
- Evidence Registry
- Edge Evidence Bindings

The canonical graph/evidence model should be treated as the authoritative
structured representation.

Vector indexes, fuzzy scores, ML predictions, waveform encodings, fractal
representations, and other derived signals remain non-canonical.
