# Cursor OTEL Gate-4 global-utils atomic persistence evidence

Date: 2026-09-15

## Status

- Persistence transaction: PASS
- global-utils completion persisted: YES
- Chain contracted: YES
- Successor leaf: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js`
- Module source read: NO
- Gate 5 evaluated: NO
- Cursor executed: NO

## Authority transition

- Before SHA256: `9e0db7a5b036a96571530cec0a573f64daa24c6cad038dcf1d789222730ac2d4`
- After SHA256: `145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c`

## Frozen inputs

- Reference-map evidence SHA256: `7b9e39150ae7776c37059721374dd0589ccd100c9d171d721a9fe01053190437`
- Contraction authority SHA256: `1df4a52ea9e4f72b75377a586fe5dc591526a44d8d9f9295ffba09400d0ecc18`
- Completion-state evidence SHA256: `ae914b7644b9ab937bbc8e58609d53a034af5e06d04a3e1cdfd43fb75d955634`
- Completed summary-state SHA256: `31de44f1ad75d37e58713527f7aed71d15fa7ac2af4bf2ce641c093019d1a945`
- Completed recursive-state SHA256: `f4b8f19271c054b83809afc2908a394a4d33457988d2cef6c54e4013a3b3a929`

## Mutation

- Summary replacements: 1
- Non-leaf recursive replacements: 5
- Completed recursive references after successor projection: 6
- Completed wrappers after successor projection: 5
- global-utils references before: 11
- global-utils references after: 12
- Chain before: `["../context/dist/otel.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js"]`
- Chain after: `["../context/dist/otel.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js"]`
- Leaf before: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js`
- Leaf after: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js`
- Successor leaf SHA256: `47856b82a05b810ab52f95549b74a720305e3a86f5bdeb5ab2a6c58ba6cedebf`

## Evidence

Evidence SHA256: `0a04dda30d4ae33e2e99a2cfdc7c443218568f0473dd44a67b84345407a85696`

```json
{"authority_sha256_after":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","authority_sha256_before":"9e0db7a5b036a96571530cec0a573f64daa24c6cad038dcf1d789222730ac2d4","chain_after":["../context/dist/otel.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js"],"chain_after_sha256":"2e6517267f4bf3b6807fc7c47cfdc1f76b7359368a98b5a70d5fb267f4b3bcc9","chain_before":["../context/dist/otel.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js"],"chain_before_sha256":"d72811f8e9e4586c2c09b38809693a67a696e66b3191178aba08f33963f1f23d","completed_recursive_reference_count_after":6,"completed_summary_reference_count_after":1,"completed_wrapper_count_after":5,"completion_state_evidence_sha256":"ae914b7644b9ab937bbc8e58609d53a034af5e06d04a3e1cdfd43fb75d955634","global_utils_reference_count_after":12,"global_utils_reference_count_before":11,"leaf_after_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","leaf_after_sha256":"47856b82a05b810ab52f95549b74a720305e3a86f5bdeb5ab2a6c58ba6cedebf","leaf_before_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js","leaf_before_sha256":"03bfd5102bfa0096391e4d3b9cccb3f0cc3b403e44db6c6adfb59f91bc080519","leaf_source_path":"$.otel.result.dependency.result.dependency.result","nonleaf_recursive_replacement_paths":["$.otel.result.dependency.result.dependency.result.dependency.result","$.recursive_modules.../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js.dependency.result","$.recursive_modules.../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js.dependency.result.dependency.result","$.recursive_modules.../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js","$.recursive_modules.../context/dist/otel.js.dependency.result.dependency.result.dependency.result"],"reference_map_evidence_sha256":"7b9e39150ae7776c37059721374dd0589ccd100c9d171d721a9fe01053190437","successor_existing_parent_count_before_leaf_projection":4,"successor_parent_sha256_after_child_completion":"47856b82a05b810ab52f95549b74a720305e3a86f5bdeb5ab2a6c58ba6cedebf","successor_state_reference_count_after":5,"summary_replacement_path":"$.module_summary[2]","transaction":"ATOMIC_AUTHORITY_REPLACEMENT","version":"GATE4_GLOBAL_UTILS_ATOMIC_PERSISTENCE_EVIDENCE_V1"}
```

## Strict boundary

The global-utils completion persistence transaction is complete. This checkpoint does not authorize reading api/context.js source, evaluating Gate 5, executing Cursor, or pushing Git.
