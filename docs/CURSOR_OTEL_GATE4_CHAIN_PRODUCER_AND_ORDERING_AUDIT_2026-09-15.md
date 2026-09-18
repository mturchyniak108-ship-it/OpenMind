# Cursor OTEL Gate-4 chain producer and ordering audit

Date: 2026-09-15

## Status

- Audit status: PASS
- Contraction ready: YES
- Authority mode: `ORDERED_METADATA`
- Current contraction candidate ready: YES
- OTEL authority JSON mutated: NO
- Module source read: NO
- Gate 5 evaluated: NO
- Cursor executed: NO

## Current chain

- Final module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js`
- Previous module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js`

## Ordering audit

- One-step pairs: 3
- Ordered qualified pairs: 1
- Ordered contradictory pairs: 0
- Ordering support: YES

## Producer-source audit

- Text candidates scanned: 1640
- leaf_frontier candidates: 1
- Strong producer candidates: 0
- Unique producer contract ready: NO

## Adjudication

- Model: `ORDERED_SNAPSHOT_COMPLETION_CONTRACTION`
- Rule: ordered producer-local snapshots show a completed final leaf removed by one chain element with no ordered contradictory transition
- Contraction ready: YES

## Evidence

Evidence SHA256: `1df4a52ea9e4f72b75377a586fe5dc591526a44d8d9f9295ffba09400d0ecc18`

```json
{"authority_mode":"ORDERED_METADATA","chain_relation_evidence_sha256":"de453644f654721a7038c5f7ab0505286ef010aeb12d35bbc45b42c65af05794","contraction_evidence_sha256":"38a72e06b6e8ef631039960809568814f4906ae38ad6b9b7e50129cee5501561","contraction_model":"ORDERED_SNAPSHOT_COMPLETION_CONTRACTION","contraction_ready":true,"contraction_rule":"ordered producer-local snapshots show a completed final leaf removed by one chain element with no ordered contradictory transition","current_candidate_ready":true,"current_module_sequence":["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js"],"historical_provenance":[{"file":"otel-context-manager-factory-gsv2/20260914T071124/cursor_otel_context_manager_factory_gsv2.json","leaf_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js","metadata_scalars":[{"key":"next_step","path":"classification.next_step","value":"qualify the exact frozen class-factory-aware OTEL frontier `OTEL_CONTEXT_FACTORY_RECURSIVE_COMPLEX_INITIALIZER` in module `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js`. Preserve the completed root context and the qualified NoopContextManager factory. Once OTEL closes, continue directly through file-url and local-worker. Do not rerun Cursor yet."}],"module_sequence":["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js"],"mtime_ns":1789395086829990431,"path_timestamp":"2026-09-14T07:11:24","path_timestamp_tokens":["20260914T071124"]},{"file":"otel-enum-tail-recursive-gsv2/20260914T065234/cursor_otel_enum_tail_recursive_gsv2.json","leaf_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","metadata_scalars":[{"key":"next_step","path":"classification.next_step","value":"qualify the exact frozen recursive OTEL frontier `OTEL_RECURSIVE_COMPLEX_INITIALIZER` in module `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js`. Preserve the now-complete SpanKind module and every other recursively completed OpenTelemetry dependency. Once OTEL closes, continue directly through file-url and local-worker. Do not rerun Cursor yet."}],"module_sequence":["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js"],"mtime_ns":1789393956725990862,"path_timestamp":"2026-09-14T06:52:34","path_timestamp_tokens":["20260914T065234"]},{"file":"otel-recursive-local-worker-macro-gsv2/20260914T064807/cursor_otel_recursive_local_worker_macro_gsv2.json","leaf_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/span_kind.js","metadata_scalars":[{"key":"next_step","path":"classification.next_step","value":"qualify the exact frozen recursive OTEL frontier `OTEL_RECURSIVE_DEPENDENCY_UNTERMINATED_TOP_LEVEL_OPERATION` in module `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/span_kind.js`. Preserve every recursively completed OpenTelemetry module and OTEL prefix binding from this report. Once OTEL closes, continue directly through file-url and the enclosing local-worker declaration. Do not rerun Cursor yet."}],"module_sequence":["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/span_kind.js"],"mtime_ns":1789393689653990964,"path_timestamp":"2026-09-14T06:48:07","path_timestamp_tokens":["20260914T064807"]},{"file":"otel-root-context-recursive-gsv2/20260914T070457/cursor_otel_root_context_recursive_gsv2.json","leaf_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","metadata_scalars":[{"key":"next_step","path":"classification.next_step","value":"qualify the exact frozen OTEL frontier `OTEL_ROOT_CONTEXT_RECURSIVE_COMPLEX_INITIALIZER` in module `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js`. Preserve the now-qualified root context and every completed recursive module. Once OTEL closes, continue directly through file-url and local-worker. Do not rerun Cursor yet."}],"module_sequence":["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js"],"mtime_ns":1789394700537990579,"path_timestamp":"2026-09-14T07:04:57","path_timestamp_tokens":["20260914T070457"]},{"file":"otel-singleton-recursive-gsv2/20260914T065937/cursor_otel_singleton_recursive_gsv2.json","leaf_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context/context.js","metadata_scalars":[{"key":"next_step","path":"classification.next_step","value":"qualify the exact frozen singleton-aware OTEL frontier `OTEL_SINGLETON_RECURSIVE_COMPLEX_INITIALIZER` in module `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context/context.js`. Preserve every completed singleton/module authority from this report. Once OTEL closes, continue directly through file-url and local-worker. Do not rerun Cursor yet."}],"module_sequence":["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context/context.js"],"mtime_ns":1789394379485990701,"path_timestamp":"2026-09-14T06:59:37","path_timestamp_tokens":["20260914T065937"]}],"json_failures":8,"json_parsed":958,"json_seen":966,"one_step_pair_count":3,"ordered_contradictory_pair_count":0,"ordered_qualified_pair_count":1,"ordering_support":true,"producer_candidate_count":1,"producer_candidates":[{"hit_count":1,"name":"docs/CURSOR_OTEL_GATE4_GLOBAL_UTILS_PERSISTENCE_AUTHORIZATION_2026-09-15.md","origin":"REPO","sha256":"f99f5e23b5a86b7b7a5b3a91bd7eb782ed512b76fbecf9a1db61814a9b5a1952","strong_windows":[]}],"producer_contract_ambiguous":false,"producer_contract_ready":false,"strong_producer_candidate_count":0,"version":"GATE4_OTEL_CHAIN_PRODUCER_AND_ORDERING_AUDIT_V1"}
```

## Strict boundary

This audit reads only existing qualification metadata and helper or documentation source. It does not read module source, mutate the OTEL authority JSON, execute Cursor, or evaluate Gate 5.
