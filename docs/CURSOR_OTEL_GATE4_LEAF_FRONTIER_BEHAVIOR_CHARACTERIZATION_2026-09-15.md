# Cursor OTEL Gate-4 leaf-frontier behavior characterization

Date: 2026-09-15

## Status

- Characterization: PASS
- Successor transition authorized: NO
- Completion persisted: NO
- OTEL authority JSON mutated: NO
- Next module source read: NO
- Gate 5 evaluated: NO
- Cursor executed: NO

## Current frontier

- Current leaf: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js`
- Direct parent: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js`
- Current leaf SHA256: `03bfd5102bfa0096391e4d3b9cccb3f0cc3b403e44db6c6adfb59f91bc080519`

## Historical corpus

- JSON files seen: 966
- JSON files parsed: 958
- JSON parse failures: 8
- Leaf-frontier objects: 5
- Leaf objects: 5
- Leaf absent snapshots: 953
- Leaf completed true: 0
- Leaf completed false: 5
- Leaf with direct dependency: 0
- Leaf with completed direct dependency: 0
- Historical direct-parent resume count: 0

## Adjudication

- Transition model: `COMPLETION_COEXISTS_WITH_NON_PARENT_LEAF_STATE`
- Historical direct-parent resume supported: NO
- Historical leaf carrying completed direct dependency supported: NO
- Successor transition authorized: NO

## Behavior evidence

Evidence SHA256: `f88c11bf2461578b938f9dc7325df5da2b7429b6da8d070c59e315c068b8d469`

```json
{"completed_module_leaf_relations":{"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context/context.js":{"LEAF_OTHER":2},"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/span_kind.js":{"LEAF_OTHER":4}},"completed_module_relation_examples":{"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context/context.js":[{"file":"otel-context-manager-factory-gsv2/20260914T071124/cursor_otel_context_manager_factory_gsv2.json","leaf_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js","relation":"LEAF_OTHER"},{"file":"otel-root-context-recursive-gsv2/20260914T070457/cursor_otel_root_context_recursive_gsv2.json","leaf_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","relation":"LEAF_OTHER"}],"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/span_kind.js":[{"file":"otel-context-manager-factory-gsv2/20260914T071124/cursor_otel_context_manager_factory_gsv2.json","leaf_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js","relation":"LEAF_OTHER"},{"file":"otel-enum-tail-recursive-gsv2/20260914T065234/cursor_otel_enum_tail_recursive_gsv2.json","leaf_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","relation":"LEAF_OTHER"},{"file":"otel-root-context-recursive-gsv2/20260914T070457/cursor_otel_root_context_recursive_gsv2.json","leaf_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","relation":"LEAF_OTHER"},{"file":"otel-singleton-recursive-gsv2/20260914T065937/cursor_otel_singleton_recursive_gsv2.json","leaf_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context/context.js","relation":"LEAF_OTHER"}]},"current_direct_parent_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","current_direct_parent_records":[{"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","path":"$.otel.result.dependency.result.dependency.result","sha256":"039056ba8c4ee26db17648d16874bd55604c87ab099c76dd9feb1b48a6247489"},{"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","path":"$.recursive_modules.../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","sha256":"039056ba8c4ee26db17648d16874bd55604c87ab099c76dd9feb1b48a6247489"},{"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","path":"$.recursive_modules.../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js.dependency.result","sha256":"039056ba8c4ee26db17648d16874bd55604c87ab099c76dd9feb1b48a6247489"},{"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","path":"$.recursive_modules.../context/dist/otel.js.dependency.result.dependency.result","sha256":"039056ba8c4ee26db17648d16874bd55604c87ab099c76dd9feb1b48a6247489"}],"current_leaf_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js","current_leaf_sha256":"03bfd5102bfa0096391e4d3b9cccb3f0cc3b403e44db6c6adfb59f91bc080519","frontier_object_count":5,"frontier_schema_counts":{"chain|leaf":5},"historical_completed_child_leaf_supported":false,"historical_resume_parent_supported":false,"json_failures":8,"json_parsed":958,"json_seen":966,"leaf_absent_count":953,"leaf_completed_dependency_pair_counts":{},"leaf_completed_false_count":5,"leaf_completed_other_count":0,"leaf_completed_true_count":0,"leaf_dependency_pair_counts":{},"leaf_module_counts":{"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js":1,"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js":1,"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context/context.js":1,"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js":1,"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/span_kind.js":1},"leaf_object_count":5,"leaf_with_completed_dependency_count":0,"leaf_with_dependency_count":0,"leaf_with_incomplete_dependency_count":0,"persistence_authorization_evidence_sha256":"c67d8ea8746e2c5ec12eea1d5dff5b919990e108bffac9c4a56efc1f1d5082c4","resume_parent_count":0,"successor_transition_authorized":false,"transition_model":"COMPLETION_COEXISTS_WITH_NON_PARENT_LEAF_STATE","version":"GATE4_OTEL_LEAF_FRONTIER_BEHAVIOR_CHARACTERIZATION_V1"}
```

## Strict boundary

This characterization deliberately does not invent a successor transition. The next gate must use the recovered frontier behavior to identify the actual producer rule before any OTEL authority mutation.
