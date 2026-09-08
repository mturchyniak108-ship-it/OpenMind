# MAF Query-to-PK Selection V1 Protocol

## 1. Status

**PREREGISTERED RESEARCH PROTOCOL**

Phase:

**6D-Q2 — Query-to-PK Selection Prototype**

Protocol version:

**V1**

Phase 6D-Q1 is accepted and closed.

Phase 6D-Q2 is therefore authorized to begin.

This protocol does not authorize Phase 6D-Q3, Phase 6D-Q4, or Phase 6E.

---

## 2. Scientific question

The Phase 6D-Q2 V1 question is:

> Can deterministic signals derived only from the input query and immutable
> model-object metadata select a bounded set of MAF object PK candidates
> without using expected-answer knowledge or reference-execution knowledge?

This is a non-oracle candidate-selection question.

It is not an inference-sufficiency question.

---

## 3. Scope of V1

V1 tests **metadata-intent routing**.

Examples of supported input intent include:

- `layer 7 attention query`
- `block 3 attention key`
- `value attention in layer 12`
- `layer 8 ffn down`
- `layer 4 feed forward gate`
- `layer 10 normalization`
- `token embedding`
- `output normalization`

V1 intentionally does not claim that an arbitrary natural-language user
question can yet be mapped to the model weights that are semantically
necessary to answer that question.

General semantic prompt routing remains unvalidated.

---

## 4. Frozen upstream authorities

The future implementation and validation must bind the following frozen
authorities.

Phase 6D-Q1 scientific acceptance verdict SHA256:

`c396346adfc3d7aed08373a52d02e88ce14b2195269c9d090c2572828db77615`

Query Capsule Data Model V1 implementation SHA256:

`f897b97011714f3c84b7350c6bb53e800232be8a5d34e5148a3e50a81952976e`

Roadmap SHA256:

`50ecfa32aa64e5b0b8b0a1e8f0fbc9802de537284ca36aa9f1594bcc6ea4c94c`

Query-Scoped Working Set Architecture SHA256:

`7df826096e506d13502e442fb11f7e1f18fb2c5a342f4214b91a3c3df043559c`

---

## 5. Non-oracle rule

The selector may consume only:

1. input query text;
2. deterministic query normalization/signature;
3. a generation-bound immutable candidate catalog;
4. a frozen selector configuration.

The selector MUST NOT consume:

- expected answer text;
- expected output token;
- reference logits;
- reference hidden states;
- full-reference execution traces;
- objects touched by a reference execution;
- later selective-execution telemetry;
- route-cache entries;
- prior answer text;
- human-selected target PKs;
- benchmark target labels;
- validation pass/fail information.

Evaluation code may possess target labels.

The selector itself may not receive them.

---

## 6. Candidate catalog

The selector consumes one immutable catalog.

Catalog schema identifier:

`openmind.maf_query_pk_catalog.v1`

The exact catalog top-level fields are:

1. `schema`
2. `source_generation_pk`
3. `source_manifest_sha256`
4. `entries`

No additional fields are permitted.

---

## 7. Catalog entry schema

Each catalog entry contains exactly:

1. `object_pk`
2. `tensor_name`
3. `tensor_type`
4. `dims`
5. `element_count`

The catalog therefore exposes model-object identity and static tensor
metadata only.

Storage-layout information is not a selection feature.

In particular the selector must not score candidates using:

- segment ID;
- segment pathname;
- byte offset;
- serialized byte length;
- payload SHA256;
- segment SHA256;
- object-file SHA256;
- locality telemetry;
- cache statistics;
- residency state.

Those values may exist elsewhere in OpenMind but are outside the Q2 V1
selection surface.

---

## 8. Catalog invariants

Every `object_pk` must satisfy the existing canonical MAF object-PK grammar.

Every `tensor_name` must be a non-empty UTF-8 string.

Every `tensor_type` must be an integer and must not be a boolean.

`dims` must be a non-empty ordered sequence of positive integers.

`element_count` must be a positive integer and must not be a boolean.

Object PKs must be unique.

Catalog entries must be stored in ascending lexical `object_pk` order.

The catalog is bound simultaneously to:

- `source_generation_pk`;
- `source_manifest_sha256`.

A generation or manifest mismatch must reject selection.

---

## 9. Catalog canonical serialization

Canonical catalog serialization is UTF-8 JSON using:

- `sort_keys=True`
- `separators=(",", ":")`
- `ensure_ascii=False`

There is no insignificant whitespace and no trailing newline.

The catalog SHA256 is the SHA256 of those exact canonical bytes.

---

## 10. Query normalization

Input query normalization is deterministic.

The normalization algorithm is exactly:

1. require a non-empty UTF-8 Python string;
2. Unicode normalize using NFKC;
3. apply Unicode `casefold()`;
4. replace `.`, `_`, `/`, and `-` with ASCII space;
5. replace all remaining non-alphanumeric characters with ASCII space;
6. collapse runs of whitespace to one ASCII space;
7. remove leading and trailing whitespace.

An empty normalized query is invalid.

---

## 11. Query signature

The Q2 V1 query signature is:

`sha256(normalized_query.encode("utf-8")).hexdigest()`

It is exactly 64 lowercase hexadecimal characters.

This signature is suitable for use as the Q1 Query Capsule
`query_signature`.

---

## 12. Query layer extraction

The selector recognizes one optional layer intent.

Accepted layer forms after normalization are:

- `layer N`
- `block N`
- `blk N`

where `N` is one or more decimal digits.

If more than one distinct layer number is present, the query is ambiguous and
must be rejected.

The layer number is interpreted as a non-negative integer.

---

## 13. Semantic intent vocabulary

The recognized canonical intent tags are exactly:

- `attn`
- `q`
- `k`
- `v`
- `ffn`
- `down`
- `up`
- `gate`
- `norm`
- `embedding`
- `output`

No additional semantic tags may be introduced after protocol freeze.

---

## 14. Frozen query alias table

The following query aliases map to canonical tags.

### Attention family

`attention` -> `attn`

`attn` -> `attn`

### Attention roles

`query` -> `q`

whole token `q` -> `q`

`key` -> `k`

whole token `k` -> `k`

`value` -> `v`

whole token `v` -> `v`

### Feed-forward family

`feed forward` -> `ffn`

`feedforward` -> `ffn`

`ffn` -> `ffn`

`mlp` -> `ffn`

### Feed-forward roles

`down projection` -> `down`

`down` -> `down`

`up projection` -> `up`

`up` -> `up`

`gate` -> `gate`

### Normalization

`normalization` -> `norm`

`norm` -> `norm`

### Embedding

`token embedding` -> `embedding`

`token embeddings` -> `embedding`

`embedding` -> `embedding`

`embeddings` -> `embedding`

`embd` -> `embedding`

### Output

`lm head` -> `output`

`output` -> `output`

---

## 15. Tensor-name descriptor extraction

Candidate descriptor extraction uses only `tensor_name`.

The tensor name is casefolded.

The characters `.`, `_`, `/`, and `-` are treated as separators.

A tensor-name layer is recognized only from the canonical form:

`blk.N`

where `N` is a non-negative decimal integer.

The following tensor-name tokens map to canonical tags:

- `attn` -> `attn`
- `q` -> `q`
- `k` -> `k`
- `v` -> `v`
- `ffn` -> `ffn`
- `down` -> `down`
- `up` -> `up`
- `gate` -> `gate`
- `norm` -> `norm`
- `embd` -> `embedding`
- `embedding` -> `embedding`
- `output` -> `output`

Unknown tensor-name tokens are ignored for Q2 V1 scoring.

---

## 16. Candidate eligibility

Let:

- `Q_layer` be the optional query layer;
- `Q_tags` be the query canonical-tag set;
- `C_layer` be the optional candidate layer;
- `C_tags` be the candidate canonical-tag set.

A candidate is metadata-eligible when:

1. if `Q_layer` exists, `C_layer` must exist and equal `Q_layer`; and
2. every member of `Q_tags` is present in `C_tags`.

If `Q_tags` is empty but `Q_layer` exists, all objects with the matching
candidate layer are metadata-eligible.

If neither a layer nor any recognized tag exists, there are no
metadata-eligible candidates and the uninformed fallback is used.

---

## 17. Candidate score

For every metadata-eligible candidate:

`matched_tag_count = len(Q_tags)`

`extra_tag_count = len(C_tags - Q_tags)`

`layer_bonus = 1000 if Q_layer exists else 0`

The exact score is:

`layer_bonus + 100 * matched_tag_count - extra_tag_count`

Candidates are ranked by:

1. descending score;
2. ascending lexical `object_pk`.

The rank order must therefore be deterministic.

---

## 18. Maximum candidate budget

The selector receives `max_candidates`.

It must be an integer and must not be a boolean.

Permitted range:

`1 <= max_candidates <= 32`

The returned candidate sequence length may never exceed this value.

No returned PK may be duplicated.

---

## 19. Metadata-selection behavior

If one or more metadata-eligible candidates exist, return the first
`max_candidates` objects from the deterministic ranking.

The selector MUST NOT fill unused budget positions with unrelated objects.

Therefore a query may legitimately return fewer than `max_candidates`
candidates.

---

## 20. Uninformed fallback

If there are zero metadata-eligible candidates, Q2 V1 uses a deterministic
uninformed fallback.

For each object PK compute:

`sha256(query_signature + "\0" + object_pk).hexdigest()`

Rank fallback candidates by:

1. ascending digest;
2. ascending object PK.

Return at most `max_candidates`.

The result must explicitly record:

`fallback_used = true`

Fallback selection is only a total-function behavior.

It is not evidence of semantic query-to-PK routing quality.

---

## 21. Selection result schema

Selection result schema identifier:

`openmind.maf_query_to_pk_selection.v1`

The exact result fields are:

1. `schema`
2. `query_signature`
3. `source_generation_pk`
4. `source_manifest_sha256`
5. `catalog_sha256`
6. `selection_config_sha256`
7. `recognized_layer`
8. `recognized_tags`
9. `fallback_used`
10. `selected_object_pks`

No additional fields are permitted.

---

## 22. Result invariants

`recognized_tags` is an ordered tuple in the canonical protocol vocabulary
order:

`attn, q, k, v, ffn, down, up, gate, norm, embedding, output`

Tags not recognized in the query are absent.

`selected_object_pks`:

- contains only PKs from the bound catalog;
- contains no duplicates;
- preserves authoritative selection rank order;
- never exceeds `max_candidates`.

The result must preserve generation and manifest binding.

---

## 23. Selector configuration

Configuration schema identifier:

`openmind.maf_query_to_pk_selection_config.v1`

The exact configuration fields are:

1. `schema`
2. `max_candidates`
3. `normalization_version`
4. `alias_version`
5. `descriptor_version`
6. `ranking_version`
7. `fallback_version`

For V1 the exact version strings are:

- `normalization_version = "nfkc_casefold_v1"`
- `alias_version = "metadata_intent_alias_v1"`
- `descriptor_version = "tensor_name_descriptor_v1"`
- `ranking_version = "metadata_subset_rank_v1"`
- `fallback_version = "sha256_rendezvous_v1"`

The configuration SHA256 is computed from its canonical JSON bytes.

---

## 24. Determinism requirement

For identical:

- query text;
- catalog bytes;
- source generation;
- source manifest;
- selector configuration;

the selector must return byte-identical canonical result bytes.

---

## 25. Input alias isolation

Mutable caller-owned input sequences must not remain aliased into selector
authority.

The future implementation must normalize catalog/result sequence values to
immutable internal representation.

---

## 26. Failure atomicity

Invalid query, catalog, configuration, generation binding, manifest binding,
or budget must fail before returning any authoritative selection result.

Construction failure must not mutate:

- the catalog;
- Q1 Query Capsule authority;
- canonical MAF objects;
- generation manifests;
- resident PK directories.

---

## 27. Prospective validation catalog

Scientific validation must bind a frozen candidate catalog before
authoritative execution.

The validation protocol must freeze:

- exact catalog bytes;
- catalog SHA256;
- source generation PK;
- source manifest SHA256;
- catalog entry count.

The selector implementation may not be changed after seeing authoritative
validation results.

---

## 28. Prospective benchmark query generation

Validation queries must be generated prospectively from the frozen catalog
using the protocol-defined metadata-intent grammar.

The harness may know the expected metadata target set.

The selector may receive only:

- query text;
- bound candidate catalog;
- frozen selector configuration.

Expected target PKs must never be passed to the selector.

---

## 29. Specific-intent evaluation

A `specific-intent` query is one whose independent protocol predicate matches
exactly one catalog entry.

Prospective validation must include at least:

- 32 total evaluation queries;
- 16 specific-intent queries;
- 8 distinct expected object PKs.

If the frozen real catalog cannot satisfy those minimums, authoritative
validation must stop before its exact-once scientific slot is reserved.

The thresholds must not be weakened post hoc.

---

## 30. Required selection metrics

Prospective scientific validation must report at minimum:

- evaluation query count;
- specific-intent query count;
- unique expected object PK count;
- metadata-eligible query count;
- fallback query count;
- mean selected-candidate count;
- maximum selected-candidate count;
- supported-intent target-hit rate;
- supported-intent precision;
- specific-intent top-1 accuracy;
- deterministic-random-baseline top-1 accuracy;
- selector-minus-baseline top-1 difference.

---

## 31. Independent target predicate

The validation harness must independently compute expected metadata targets
from the frozen catalog and the exact protocol rules.

It must not call the selector implementation's candidate-ranking helper to
construct target labels.

This prevents implementation logic from defining its own correctness oracle.

---

## 32. Random baseline

The deterministic random baseline seed is exactly:

`OPENMIND_6D_Q2_V1_RANDOM_BASELINE`

For each query/object pair, baseline rank is derived from:

`sha256(seed + "\0" + query_signature + "\0" + object_pk).hexdigest()`

The baseline selects the same `max_candidates` budget as the tested selector.

The baseline must have no access to expected targets.

---

## 33. Scientific acceptance thresholds

Future Q2 V1 acceptance requires all structural validation checks to pass and
all of the following benchmark conditions:

1. at least 32 evaluation queries;
2. at least 16 specific-intent queries;
3. at least 8 distinct expected object PKs;
4. supported-intent target-hit rate = `1.0`;
5. supported-intent precision = `1.0`;
6. specific-intent top-1 accuracy >= `0.95`;
7. selector-minus-random-baseline specific-intent top-1 difference >= `0.50`;
8. no selector result exceeds its candidate budget;
9. no duplicate selected PK exists;
10. no generation or manifest binding violation occurs;
11. no oracle-input violation occurs.

These thresholds are frozen before implementation validation.

---

## 34. Negative result policy

If the selector fails any preregistered threshold, Q2 V1 is a scientific
negative result.

The thresholds must not be weakened after execution.

A failed result must not be rescued by:

- adding expected targets to selector inputs;
- consulting full-reference execution;
- increasing the candidate budget beyond 32;
- introducing route-cache information;
- automatically expanding the working set;
- redefining the benchmark after seeing results.

A successor protocol would be required.

---

## 35. No route cache

Query Route Cache use is explicitly disabled in Q2 V1.

Route-cache reuse belongs to Phase 6D-Q4.

No exact, normalized, or similar-query route may influence Q2 V1 selection.

---

## 36. No bounded expansion

Q2 V1 produces one initial bounded candidate set.

It does not expand the set after selection.

Bounded expansion remains Phase 6E-B.

---

## 37. No execution-feedback selector

Q2 V1 selection occurs before any selective execution.

It may not consume:

- cache misses;
- tensor requests;
- object faults;
- hidden-state divergence;
- logits;
- answer quality;
- later runtime telemetry.

---

## 38. No selective inference claim

A successful Q2 V1 result means only:

> bounded non-oracle metadata-intent query-to-PK selection is feasible under
> the frozen benchmark contract.

It does not mean the selected objects are sufficient to run the model or
produce a correct answer.

Selective working-set sufficiency remains Phase 6E-A.

---

## 39. General-prompt nonclaim

Q2 V1 does not establish that unrestricted natural-language prompts can be
routed to sufficient model objects.

A later selector successor may broaden the validated query domain under a
new prospective protocol.

No such broader claim may be inferred from Q2 V1.

---

## 40. No object-avoidance claim

Even if Q2 V1 returns a small candidate set, this protocol does not establish
that unselected objects are actually avoided during execution.

Actual object/tensor avoidance remains Phase 6E-C.

---

## 41. No output-quality claim

Q2 V1 performs no answer-quality evaluation.

Output parity and quality remain Phase 6E-D.

---

## 42. No performance claim

Candidate count, catalog size, or small result size is not evidence of
runtime performance improvement.

Performance evaluation remains Phase 6F.

---

## 43. No MAF-native compute claim

MAF-native compute remains:

`DISABLED_UNVALIDATED`

Q2 V1 does not alter the dense-compute compatibility boundary.

---

## 44. No persistence claim

Q2 V1 selection results are ordinary in-memory derived data.

This protocol does not authorize persistent Query Route Cache storage.

It does not define a persistent selector-result authority.

Any new persistent mechanism requires its own correctness protocol.

---

## 45. Implementation boundary

The future Q2 implementation must be a deterministic pure data-model /
selection component.

It must not:

- perform inference;
- launch subprocesses;
- access the network;
- mutate MAFDB;
- mutate generation manifests;
- mutate resident PK directories;
- attach/detach Query Capsules;
- read or write Query Route Cache state;
- trigger bounded expansion.

---

## 46. Implementation construction authorization

After this protocol is frozen, construction of:

`experiments/model_fractal/maf_query_to_pk_selection_v1.py`

is authorized.

Construction and static/non-scientific testing are permitted.

Scientific validation is not yet authorized.

---

## 47. Validation authorization sequence

Before scientific Q2 execution:

1. freeze this protocol;
2. build implementation candidate;
3. independently audit candidate;
4. freeze exact implementation bytes;
5. preregister validation protocol;
6. freeze exact validation catalog and benchmark authorities;
7. build validation runner;
8. independently audit validation runner;
9. freeze runner;
10. run all required non-spending qualification/readiness gates;
11. perform one authoritative exact-once scientific validation.

No scientific execution may occur earlier.

---

## 48. Q2 closure requirement

Phase 6D-Q2 closes only after:

- the implementation is frozen;
- prospective validation is frozen;
- authoritative result is frozen;
- all acceptance thresholds pass;
- a formal scientific acceptance verdict is frozen.

Implementation construction alone does not close Q2.

---

## 49. Downstream progression

If Q2 closes successfully:

**Phase 6D-Q3 becomes the next gate.**

Q3 remains responsible for:

- Query Capsule attach;
- ownership;
- detach;
- cleanup;
- failure atomicity.

Phase 6D-Q4 remains responsible for Query Route Cache reuse.

Phase 6E-A remains blocked until Q1, Q2, Q3, and Q4 are all closed.

---

## 50. Final nonclaims

This protocol does not establish:

- arbitrary prompt semantic routing;
- selective inference sufficiency;
- bounded expansion correctness;
- output parity;
- answer quality;
- reduced object reads;
- reduced tensor reads;
- lower RAM;
- lower latency;
- higher throughput;
- MAF-native computation.

---

## 51. Next gate

After protocol freeze:

**BUILD PHASE 6D-Q2 QUERY-TO-PK SELECTION V1 IMPLEMENTATION CANDIDATE**

Scientific execution remains unauthorized.
