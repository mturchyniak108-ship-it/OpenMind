# OpenMind Roadmap

## Vision

OpenMind is a local-first AI inference and knowledge platform built around native `llama.cpp` execution, hardware acceleration, language-neutral knowledge representation, and optimized semantic reasoning paths.

> **Core principle:** Known truths are language-independent. Language is an interface to knowledge, not the representation of knowledge.

## Milestone 0 — Native Inference Foundation

### Completed

- Device/resource discovery
- Vulkan capability verification
- `llama.cpp` Vulkan build
- Native C++ inference
- Reproducible performance benchmarks
- Persistent native session API
- Multi-session sequence isolation
- RAII session lifecycle
- Session reset and capacity management
- CMake/CTest integration
- Native inference concurrency protection
- Concurrent session regression testing

## Milestone 1 — Language-Neutral Truth Graph

Create a knowledge representation in which semantic truth is independent of natural language.

- [ ] Define `TruthNode`
- [ ] Define canonical semantic identity
- [ ] Define truth status and confidence
- [ ] Define provenance and evidence
- [ ] Define multilingual `TruthExpression`
- [ ] Allow multiple languages to reference one `TruthNode`
- [ ] Define contradiction status
- [ ] Create initial truth-graph schema

## Milestone 2 — Truth Relationship Graph

Represent relationships between known truths as a directed, weighted graph.

- [ ] Define `TruthEdge`
- [ ] Define relationship types
- [ ] Define relationship confidence
- [ ] Define provenance model
- [ ] Implement graph storage
- [ ] Implement node lookup and edge traversal
- [ ] Implement relationship validation
- [ ] Implement contradiction representation

## Milestone 3 — Start/End Truth Paths

Discover paths between semantic start and end nodes while minimizing unnecessary cycles and favoring high-confidence routes.

- [ ] Define `TruthPath`
- [ ] Define start-node semantics
- [ ] Define end-node semantics
- [ ] Implement path discovery
- [ ] Detect cycles
- [ ] Penalize unnecessary cycles
- [ ] Detect contradictory paths
- [ ] Rank candidate paths
- [ ] Select highest-confidence useful paths

## Milestone 4 — Specialized Vector Index

Build a local vector/index system around the Truth Graph rather than a conventional document-only vector database.

- [ ] Design vector storage
- [ ] Select embedding representation
- [ ] Define vector-to-`TruthNode` mapping
- [ ] Define `TruthNode`-to-vector mapping
- [ ] Define index persistence and updates
- [ ] Define index rebuild behavior
- [ ] Benchmark candidate index structures
- [ ] Compare SQLite-backed and specialized binary/index approaches

## Milestone 5 — Compiled Heuristic Mapping

Compile frequently useful truth paths into optimized mappings that favor high-confidence, low-cost routes between semantic start and end nodes.

### Path Weighting Inputs

- Truth confidence
- Evidence strength
- Provenance quality
- Relationship confidence
- Semantic similarity
- Path length
- Cycle penalty
- Contradiction penalty
- Historical retrieval success
- Historical answer success
- Context relevance

### Heuristic Model

- [ ] Define `PathWeight`
- [ ] Define heuristic scoring
- [ ] Define path cost
- [ ] Define cycle penalty
- [ ] Define contradiction penalty
- [ ] Define confidence aggregation
- [ ] Define semantic relevance weighting
- [ ] Define evidence weighting

### Path Compilation

- [ ] Implement candidate path ranking
- [ ] Identify frequently useful paths
- [ ] Compile high-value paths into optimized mappings
- [ ] Cache compiled mappings
- [ ] Define mapping versioning
- [ ] Define mapping invalidation
- [ ] Define incremental recompilation
- [ ] Benchmark compiled vs dynamic traversal

### Optimization Principle

Prefer the path with the highest combined truth confidence and semantic relevance while minimizing path length, unnecessary cycles, contradictions, and weak relationships.

The compiled mapping should allow frequently requested semantic routes to bypass expensive graph exploration and directly reach the most probable valid knowledge path.

## Milestone 6 — Language-Independent Retrieval

Resolve queries expressed in different languages to the same underlying semantic truths when they represent the same meaning.

- [ ] Define language-independent query representation
- [ ] Test multilingual semantic retrieval
- [ ] Test cross-language `TruthNode` matching
- [ ] Test multilingual path retrieval
- [ ] Test multilingual response generation
- [ ] Verify identical truth identity across languages
- [ ] Prevent language-specific duplication of truths

## Milestone 8 — Core Truth Data Model

Define the language-independent structures that form the foundation of the OpenMind knowledge graph.

### TruthNode

`TruthNode` represents a canonical semantic truth independent of the language used to express it.

- [ ] Define immutable TruthNode identity
- [ ] Define canonical semantic representation
- [ ] Define truth status
- [ ] Define confidence score
- [ ] Define evidence references
- [ ] Define provenance references
- [ ] Define creation and update metadata
- [ ] Define contradiction relationships
- [ ] Define semantic versioning

### TruthExpression

`TruthExpression` represents a language-specific expression that resolves to a language-independent TruthNode.

- [ ] Define language identifier
- [ ] Define normalized semantic representation
- [ ] Define original expression
- [ ] Map multiple languages to one TruthNode
- [ ] Prevent language-specific duplication of TruthNodes
- [ ] Support equivalent expressions across languages

### TruthEdge

`TruthEdge` represents a validated relationship between two TruthNodes.

- [ ] Define source TruthNode
- [ ] Define destination TruthNode
- [ ] Define relationship type
- [ ] Define relationship confidence
- [ ] Define evidence references
- [ ] Define provenance references
- [ ] Define directionality
- [ ] Define contradiction semantics
- [ ] Define edge versioning

### TruthPath

`TruthPath` represents a candidate route through the Truth Graph from a semantic start node to a semantic end node.

- [ ] Define start node
- [ ] Define end node
- [ ] Define ordered TruthEdge sequence
- [ ] Define path length
- [ ] Define aggregate confidence
- [ ] Define semantic relevance
- [ ] Define cycle count
- [ ] Define contradiction count
- [ ] Define path cost
- [ ] Define final PathWeight

### PathWeight

`PathWeight` determines how strongly OpenMind should prefer one valid path over another.

- [ ] Define deterministic weighting function
- [ ] Combine truth confidence
- [ ] Combine evidence strength
- [ ] Combine provenance quality
- [ ] Combine relationship confidence
- [ ] Combine semantic relevance
- [ ] Penalize path length
- [ ] Penalize unnecessary cycles
- [ ] Penalize contradictions
- [ ] Define stable tie-breaking rules

### Provenance

Every known truth and relationship should retain enough provenance to explain why it is considered valid.

- [ ] Define provenance identifier
- [ ] Define source reference
- [ ] Define evidence type
- [ ] Define evidence confidence
- [ ] Define verification state
- [ ] Define provenance timestamps
- [ ] Preserve provenance through compilation

### Invariants

- [ ] TruthNode identity must not depend on language
- [ ] TruthExpressions must resolve to canonical TruthNodes
- [ ] Invalid relationships must not enter the trusted graph
- [ ] Contradictory truths must remain distinguishable
- [ ] Provenance must survive graph traversal
- [ ] Compiled mappings must reference versioned graph objects
- [ ] Path ranking must be deterministic for identical inputs
- [ ] Language changes must not change TruthNode identity

## Milestone 9 — Specialized Vector Index Architecture

Build a specialized local vector index that accelerates semantic discovery without becoming the source of truth. The Truth Graph remains authoritative; vectors provide approximate semantic navigation into that graph.

### Core Principle

Vectors locate likely semantic neighbors. TruthNodes, TruthEdges, provenance, and validated relationships determine what OpenMind considers knowledge.

```text
Natural Language Query
        |
        v
Language-Independent Semantic Representation
        |
        v
Vector Search
        |
        v
Candidate TruthNodes
        |
        v
Truth Graph Validation
        |
        v
Validated Start / End Nodes
        |
        v
Path Discovery + Heuristic Ranking
        |
        v
Compiled Truth Path
```

### Vector Record

Each vector entry should map directly to a canonical TruthNode rather than storing an independent copy of knowledge.

- [ ] Define vector record format
- [ ] Define TruthNode identifier
- [ ] Define embedding identifier
- [ ] Define embedding dimensions
- [ ] Define embedding model/version
- [ ] Define normalization requirements
- [ ] Define vector metadata
- [ ] Define vector-to-TruthNode mapping
- [ ] Define TruthNode-to-vector reverse mapping

### Specialized Index

Design the index specifically for OpenMind retrieval rather than adopting a document-oriented vector database as the architectural authority.

- [ ] Evaluate flat vector search
- [ ] Evaluate approximate nearest-neighbor indexing
- [ ] Evaluate graph-assisted vector search
- [ ] Evaluate memory-mapped indexes
- [ ] Evaluate quantized vectors
- [ ] Evaluate compact mobile-readable indexes
- [ ] Benchmark index construction on Vivobook
- [ ] Benchmark index lookup on S26 Ultra
- [ ] Measure index memory footprint
- [ ] Measure index persistence size

### Storage Separation

Keep semantic truth, graph structure, and vector acceleration logically separate.

- [ ] TruthNode storage
- [ ] TruthEdge storage
- [ ] Provenance storage
- [ ] Vector storage
- [ ] Compiled mapping storage
- [ ] Query/cache storage

### Candidate Retrieval

Vector search should produce a candidate set rather than an unconditional answer.

- [ ] Retrieve top-K candidate TruthNodes
- [ ] Apply semantic similarity threshold
- [ ] Remove duplicate semantic identities
- [ ] Validate candidate TruthNodes
- [ ] Reject invalidated truths
- [ ] Preserve confidence and provenance
- [ ] Pass candidates to graph traversal

### Index Updates

- [ ] Support insertion of new TruthNodes
- [ ] Support vector updates
- [ ] Support TruthNode invalidation
- [ ] Support deletion/tombstoning
- [ ] Support incremental index updates
- [ ] Support background rebuilds
- [ ] Support index versioning
- [ ] Detect embedding-model changes
- [ ] Rebuild affected vectors when required

### Vivobook Compilation

The Vivobook should perform expensive index construction and optimization while the S26 Ultra consumes compact runtime artifacts.

- [ ] Generate embeddings on Vivobook
- [ ] Construct vector index on Vivobook
- [ ] Optimize index layout
- [ ] Validate TruthNode mappings
- [ ] Produce versioned index artifact
- [ ] Transfer runtime index to S26 Ultra
- [ ] Validate artifact integrity on S26 Ultra

### Runtime Requirements

- [ ] Fast candidate retrieval
- [ ] Low memory overhead
- [ ] Deterministic TruthNode mapping
- [ ] Offline operation
- [ ] No mandatory network dependency
- [ ] Efficient mobile storage
- [ ] Compatible with compiled heuristic mappings

### Benchmark Comparison

- [ ] SQLite-backed vector prototype
- [ ] Specialized binary index prototype
- [ ] ANN prototype
- [ ] Memory-mapped prototype
- [ ] Compare latency
- [ ] Compare RAM usage
- [ ] Compare storage size
- [ ] Compare retrieval recall
- [ ] Compare S26 Ultra runtime performance
- [ ] Compare Vivobook build performance

### Architectural Constraint

The vector index must never silently become the authority for truth. A high-similarity vector match is a candidate semantic location, not proof that the associated knowledge is true.

## Milestone 10 — Knowledge Waveform Encoding

Experiment with lossless PCM/WAV representations of Truth Graph relationships and paths.

The Truth Graph remains the canonical knowledge representation. Waveforms are derived experimental representations.

### Core Model

- start_node
- end_node
- relationship tag
- relationship direction
- relationship weight
- truth confidence
- evidence strength
- provenance strength
- semantic relevance
- contradiction signal
- path cost

### Waveform Concept

- Amplitude may represent relationship strength.
- Frequency may represent relationship class.
- Phase may represent relationship direction.
- Duration may represent path significance or cost.
- Positive signal regions may represent supporting evidence.
- Negative signal regions may represent contradiction or known-untruth evidence.
- Silence may represent absence of evidence.

These mappings are experimental and must be benchmarked rather than assumed to improve reasoning.

### Multi-Channel Experiment

- Channel 1: truth confidence
- Channel 2: evidence strength
- Channel 3: relationship weight
- Channel 4: semantic relevance
- Channel 5: contradiction
- Channel 6: path cost
- Channel 7: provenance strength
- Channel 8: retrieval history

### Path Encoding

Encode a start_node to end_node route as a deterministic waveform.

The waveform must be reproducible from the same Truth Graph state and path metadata.

### Validation

- [ ] Define deterministic waveform encoding
- [ ] Define reversible metadata representation
- [ ] Define relationship-tag encoding
- [ ] Define truth-confidence encoding
- [ ] Define contradiction encoding
- [ ] Define multi-channel representation
- [ ] Generate test WAV files
- [ ] Verify lossless round-trip
- [ ] Compare waveform storage against structured graph storage
- [ ] Benchmark waveform generation
- [ ] Benchmark waveform retrieval
- [ ] Benchmark waveform path comparison
- [ ] Test candidate-path ranking
- [ ] Test unnecessary graph traversal reduction

### Benchmark Comparison

Traditional LLM retrieval
vs
Traditional vector retrieval
vs
OpenMind Truth Graph
vs
OpenMind Truth Graph + Knowledge Waveform

Success requires measurable improvement in retrieval, path selection, latency, memory efficiency, or answer accuracy.

## Milestone 11 — Experimental Fractal Memory

Investigate whether a deterministic multimodal fractal representation of the Truth Graph can function as associative/predictive memory.

The fractal may use double-helix paths from `start_node` to `end_node`, with candidate answers represented by points of greatest validated relational convergence.

### Experimental Status

This milestone is EXPERIMENTAL and NON-CANONICAL.

Truth Graph remains the canonical knowledge representation.

Fractal geometry, color, sound, video, predictive weighting, and RUNE2 are derived experimental mechanisms.

No experimental representation may become authoritative unless a reproducible scientific hypothesis demonstrates measurable benefit.

### Scientific Method

- [ ] Define hypothesis
- [ ] Define prediction
- [ ] Define controlled experiment
- [ ] Define measurements
- [ ] Define statistical evaluation
- [ ] Define replication protocol
- [ ] Define acceptance/rejection criteria

### Fractal Memory

- [ ] Define deterministic fractal representation
- [ ] Encode complete Truth Graph state
- [ ] Encode start_node/end_node paths
- [ ] Implement double-helix relationship representation
- [ ] Define candidate answer convergence
- [ ] Define predictive weighting
- [ ] Implement fractal memory probe
- [ ] Validate every candidate against Truth Graph

### Multimodal Representation

- [ ] Define geometry encoding
- [ ] Define color encoding
- [ ] Define sound encoding
- [ ] Synchronize geometry/color/sound
- [ ] Generate deterministic fractal video
- [ ] Test real-time updates

### Scientific Benchmark

Compare increasing sensory representations:

Traditional retrieval
vs
Truth Graph
vs
Truth Graph + fractal geometry
vs
Truth Graph + fractal + color
vs
Truth Graph + fractal + sound
vs
Truth Graph + fractal + color + sound

Measure answer accuracy, retrieval recall, path selection, convergence accuracy, contradiction detection, provenance preservation, latency, memory, storage, prediction calibration, and replication stability.

### Experimental Gate

A visually compelling or complex fractal does not constitute evidence.

The center is a candidate hypothesis, not truth.

Predictive weight measures historical prediction performance, not truth confidence.

The feature remains experimental until controlled, reproducible, statistically meaningful results demonstrate a benefit.

## Milestone 12 — Experimental ML Fuzzy Logic Weighted Graph

Investigate whether fuzzy logic and machine-learned weighted vectors can improve Truth Graph retrieval and path selection.

The Truth Graph remains canonical. This subsystem produces candidate hypotheses and rankings only.

### Core Model

- TruthNode
- TruthEdge
- relationship tags
- relationship direction
- relationship weight
- truth confidence
- evidence strength
- provenance strength
- semantic relevance
- contradiction state
- path cost
- vector representation
- fuzzy membership
- learned weighting
- predictive performance

### Weighted Vector Layer

- [ ] Define vector-to-TruthNode mapping
- [ ] Define vector-to-TruthEdge mapping
- [ ] Define vector metadata
- [ ] Define embedding model/version
- [ ] Define graph-version binding
- [ ] Define deterministic vector generation
- [ ] Preserve provenance
- [ ] Preserve contradiction state

### Fuzzy Graph

- [ ] Define fuzzy node membership
- [ ] Define fuzzy relationship membership
- [ ] Define semantic similarity membership
- [ ] Define evidence membership
- [ ] Define provenance membership
- [ ] Define contradiction penalty
- [ ] Define path-cost penalty
- [ ] Define fuzzy path score
- [ ] Define explainable score components

### ML Weighting

- [ ] Define training data
- [ ] Define target outcomes
- [ ] Define baseline weights
- [ ] Train experimental weighting model
- [ ] Version learned weights
- [ ] Record model provenance
- [ ] Calibrate predictions
- [ ] Test overfitting
- [ ] Test cross-language consistency
- [ ] Test model drift
- [ ] Define deterministic fallback

### Candidate Path Ranking

- [ ] Retrieve candidate TruthNodes
- [ ] Construct candidate paths
- [ ] Apply fuzzy relationship scoring
- [ ] Apply learned weighting
- [ ] Penalize contradictions
- [ ] Penalize weak provenance
- [ ] Penalize unnecessary cycles
- [ ] Penalize excessive path cost
- [ ] Rank candidate paths
- [ ] Validate winning candidates against canonical Truth Graph

### Scientific Validation

- [ ] Define explicit hypothesis
- [ ] Define baseline
- [ ] Define independent variables
- [ ] Define dependent variables
- [ ] Define evaluation dataset
- [ ] Define accuracy metrics
- [ ] Define recall metrics
- [ ] Define path-efficiency metrics
- [ ] Define latency metrics
- [ ] Define memory metrics
- [ ] Define contradiction-detection metrics
- [ ] Run reproducible experiments
- [ ] Replicate results
- [ ] Document limitations
- [ ] Define falsification criteria

### Benchmark Comparison

Compare:

Traditional vector retrieval
vs
Truth Graph traversal
vs
Fuzzy graph without ML
vs
ML-weighted fuzzy graph
vs
OpenMind Truth Graph + ML Fuzzy Graph
vs
future multimodal/fractal-assisted retrieval

Success requires measurable and reproducible improvement.

### Architectural Constraint

A vector score, fuzzy score, ML prediction, waveform feature, fractal pattern, or predictive behavior is never canonical truth.

Truth Graph + Provenance + Validation remain authoritative.

Experimental systems may rank hypotheses but may not silently promote hypotheses into TruthNodes or TruthEdges.
