# Cursor OTEL Gate-4 leaf-to-chain relation characterization

Date: 2026-09-15

## Status

- Characterization: PASS
- Exact-object selector model: REJECTED
- Module relation ready: YES
- OTEL authority JSON mutated: NO
- Module source read: NO
- Gate 5 evaluated: NO
- Cursor executed: NO

## Current failure characterization

- Leaf module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js`
- Exact leaf object matches inside chain: 0
- Leaf module events inside chain: 1
- Leaf module positions: `[2]`

## Historical relation

- Historical snapshots: 5
- Exact-object counts: `[0,0,0,0,0]`
- Leaf-module event counts: `[1,1,1,1,1]`
- Relation model: `LEAF_IS_UNIQUE_LAST_CHAIN_MODULE_IDENTITY`
- Relation rule: leaf is materialized separately from chain and its module identity matches the unique final module event in chain traversal order

## Evidence

Evidence SHA256: `de453644f654721a7038c5f7ab0505286ef010aeb12d35bbc45b42c65af05794`

```json
{"behavior_evidence_sha256":"f88c11bf2461578b938f9dc7325df5da2b7429b6da8d070c59e315c068b8d469","current_record":{"chain_event_count":3,"chain_sha256":"d72811f8e9e4586c2c09b38809693a67a696e66b3191178aba08f33963f1f23d","chain_type":"list","exact_object_match_count":0,"first_event_is_leaf":false,"last_event_is_leaf":true,"leaf_completed":false,"leaf_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js","leaf_module_event_count":1,"leaf_module_positions":[2],"leaf_sha256":"03bfd5102bfa0096391e4d3b9cccb3f0cc3b403e44db6c6adfb59f91bc080519","module_sequence":["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js"],"source":"CURRENT_AUTHORITY","state_match_comparisons":[],"state_match_count":0,"string_match_count":1,"unique_module_identity":true},"exact_object_model_rejected":true,"historical_exact_object_match_counts":[0,0,0,0,0],"historical_leaf_module_event_counts":[1,1,1,1,1],"historical_records":[{"chain_event_count":3,"chain_sha256":"d72811f8e9e4586c2c09b38809693a67a696e66b3191178aba08f33963f1f23d","chain_type":"list","exact_object_match_count":0,"first_event_is_leaf":false,"last_event_is_leaf":true,"leaf_completed":false,"leaf_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js","leaf_module_event_count":1,"leaf_module_positions":[2],"leaf_sha256":"03bfd5102bfa0096391e4d3b9cccb3f0cc3b403e44db6c6adfb59f91bc080519","module_sequence":["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js"],"source":"otel-context-manager-factory-gsv2/20260914T071124/cursor_otel_context_manager_factory_gsv2.json","state_match_comparisons":[],"state_match_count":0,"string_match_count":1,"unique_module_identity":true},{"chain_event_count":1,"chain_sha256":"75e09f193d6a5f4fe9f714cf9a6532268553faa9b6f75c66537592baf14bba8a","chain_type":"list","exact_object_match_count":0,"first_event_is_leaf":true,"last_event_is_leaf":true,"leaf_completed":false,"leaf_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","leaf_module_event_count":1,"leaf_module_positions":[0],"leaf_sha256":"20a489bb1274c3dfe8b361a0d7335528d7cd3ba993017328fa665403791c8245","module_sequence":["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js"],"source":"otel-enum-tail-recursive-gsv2/20260914T065234/cursor_otel_enum_tail_recursive_gsv2.json","state_match_comparisons":[],"state_match_count":0,"string_match_count":1,"unique_module_identity":true},{"chain_event_count":1,"chain_sha256":"e9e8bcbd7ab6fb4cd80e2aefb46ec78790cbcb3799d1e8772f553bf47848b571","chain_type":"list","exact_object_match_count":0,"first_event_is_leaf":true,"last_event_is_leaf":true,"leaf_completed":false,"leaf_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/span_kind.js","leaf_module_event_count":1,"leaf_module_positions":[0],"leaf_sha256":"793c3a52fd755d55232ee664cba756bcb794366440b80d33644c6fc31eb57906","module_sequence":["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/span_kind.js"],"source":"otel-recursive-local-worker-macro-gsv2/20260914T064807/cursor_otel_recursive_local_worker_macro_gsv2.json","state_match_comparisons":[],"state_match_count":0,"string_match_count":1,"unique_module_identity":true},{"chain_event_count":2,"chain_sha256":"2e6517267f4bf3b6807fc7c47cfdc1f76b7359368a98b5a70d5fb267f4b3bcc9","chain_type":"list","exact_object_match_count":0,"first_event_is_leaf":false,"last_event_is_leaf":true,"leaf_completed":false,"leaf_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","leaf_module_event_count":1,"leaf_module_positions":[1],"leaf_sha256":"785d8ac0c2e8c31fdc7fed5c7e9776e75a5e0609b4472b659728352a922eac90","module_sequence":["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js"],"source":"otel-root-context-recursive-gsv2/20260914T070457/cursor_otel_root_context_recursive_gsv2.json","state_match_comparisons":[],"state_match_count":0,"string_match_count":1,"unique_module_identity":true},{"chain_event_count":3,"chain_sha256":"e3be8db014ccc19cc1face5891e649230885b43ca83ccf1a329b40e2c3378e74","chain_type":"list","exact_object_match_count":0,"first_event_is_leaf":false,"last_event_is_leaf":true,"leaf_completed":false,"leaf_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context/context.js","leaf_module_event_count":1,"leaf_module_positions":[2],"leaf_sha256":"b0c3613b27be623be920137b6b7d5a38698f334bc7c0d4dad5a19a104379fef3","module_sequence":["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context/context.js"],"source":"otel-singleton-recursive-gsv2/20260914T065937/cursor_otel_singleton_recursive_gsv2.json","state_match_comparisons":[],"state_match_count":0,"string_match_count":1,"unique_module_identity":true}],"json_failures":8,"json_parsed":958,"json_seen":966,"module_relation_ready":true,"projection_present":false,"relation_model":"LEAF_IS_UNIQUE_LAST_CHAIN_MODULE_IDENTITY","relation_rule":"leaf is materialized separately from chain and its module identity matches the unique final module event in chain traversal order","state_projection_records":[],"version":"GATE4_OTEL_LEAF_CHAIN_RELATION_CHARACTERIZATION_V1"}
```

## Strict boundary

This audit only replaces the disproved exact-object assumption with observed chain-to-leaf relations. It does not authorize chain contraction, successor selection, completion persistence, or OTEL authority mutation.
