# Cursor OTEL Gate-4 api context parent return to context-api authorization

Date: 2026-09-15

## Status

- Authorization status: PASS
- Completed child: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js`
- Parent: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js`
- Child completed state SHA256: `fada3ecb5ce3e16fb2da60c54a312af1bc98dc3ad1339e50e8788c336739d215`
- Parent classified in this gate: NO
- Parent source executed: NO

## Frozen parent edge

- Parent state path: `$.recursive_modules.../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js`
- Parent state SHA256: `3d759e6436d9fd61555b422c8d570136021e08f699a09a990f15096f176ea112`
- Historical child result path: `$.recursive_modules.../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js.dependency.result`
- Historical child state SHA256: `47856b82a05b810ab52f95549b74a720305e3a86f5bdeb5ab2a6c58ba6cedebf`

## Return contract

- Contract SHA256: `df11b4939e092044bb41096587fb85562074fbbb294fa834b56fb7600ac8d9e3`

```json
{"authority_mutation_authorized":false,"child_completed_state_sha256":"fada3ecb5ce3e16fb2da60c54a312af1bc98dc3ad1339e50e8788c336739d215","child_completion_evidence_sha256":"765ddd2b4de1f77d1a6c3b070f7fe945ded98ff111f7cd0c10dc2d144530bd63","child_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","historical_child_result_path":"$.recursive_modules.../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js.dependency.result","historical_child_state_sha256":"47856b82a05b810ab52f95549b74a720305e3a86f5bdeb5ab2a6c58ba6cedebf","next_parent_action":"BOUNDED_CONTEXT_API_STATIC_RESUME_AUTHORIZATION_ONLY","parent_classification_performed":false,"parent_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","parent_resume_authorized_after_this_gate":true,"parent_source_execution_authorized":false,"parent_state_path":"$.recursive_modules.../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","parent_state_sha256":"3d759e6436d9fd61555b422c8d570136021e08f699a09a990f15096f176ea112","source_auth_evidence_sha256":"1aafe18e7887b251aba7b3a0f88cf6cd80deb277f12c3b9359ad07a902f11c30","version":"GATE4_API_CONTEXT_PARENT_RETURN_TO_CONTEXT_API_CONTRACT_V1"}
```

## Authorization evidence

Evidence SHA256: `e21a6dcbb88cf746d84228ec2c03ff34deb7fbdb86fb46d1dc91a49f6aafb8a0`

```json
{"authorization_status":"AUTHORIZED_RETURN_FROM_COMPLETED_API_CONTEXT_TO_CONTEXT_API","child_completed_state_sha256":"fada3ecb5ce3e16fb2da60c54a312af1bc98dc3ad1339e50e8788c336739d215","child_completion_document_sha256":"bc13e338a2e889001e92df87014718bbdac32e8b45e813fe51b12f5f7c446e4f","child_completion_evidence_sha256":"765ddd2b4de1f77d1a6c3b070f7fe945ded98ff111f7cd0c10dc2d144530bd63","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","historical_chain_modules":["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js"],"historical_child_result_path":"$.recursive_modules.../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js.dependency.result","historical_child_state_sha256":"47856b82a05b810ab52f95549b74a720305e3a86f5bdeb5ab2a6c58ba6cedebf","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","parent_candidate_count":5,"parent_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","parent_state_path":"$.recursive_modules.../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","parent_state_sha256":"3d759e6436d9fd61555b422c8d570136021e08f699a09a990f15096f176ea112","return_contract":{"authority_mutation_authorized":false,"child_completed_state_sha256":"fada3ecb5ce3e16fb2da60c54a312af1bc98dc3ad1339e50e8788c336739d215","child_completion_evidence_sha256":"765ddd2b4de1f77d1a6c3b070f7fe945ded98ff111f7cd0c10dc2d144530bd63","child_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","historical_child_result_path":"$.recursive_modules.../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js.dependency.result","historical_child_state_sha256":"47856b82a05b810ab52f95549b74a720305e3a86f5bdeb5ab2a6c58ba6cedebf","next_parent_action":"BOUNDED_CONTEXT_API_STATIC_RESUME_AUTHORIZATION_ONLY","parent_classification_performed":false,"parent_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","parent_resume_authorized_after_this_gate":true,"parent_source_execution_authorized":false,"parent_state_path":"$.recursive_modules.../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","parent_state_sha256":"3d759e6436d9fd61555b422c8d570136021e08f699a09a990f15096f176ea112","source_auth_evidence_sha256":"1aafe18e7887b251aba7b3a0f88cf6cd80deb277f12c3b9359ad07a902f11c30","version":"GATE4_API_CONTEXT_PARENT_RETURN_TO_CONTEXT_API_CONTRACT_V1"},"return_contract_sha256":"df11b4939e092044bb41096587fb85562074fbbb294fa834b56fb7600ac8d9e3","source_auth_document_sha256":"8a1c6125c757d4db142e0f5821abf29ba6adf7e2ea2c8d288f89b0bf4494fbb5","source_auth_evidence_sha256":"1aafe18e7887b251aba7b3a0f88cf6cd80deb277f12c3b9359ad07a902f11c30","source_executed":false,"version":"GATE4_API_CONTEXT_PARENT_RETURN_TO_CONTEXT_API_AUTHORIZATION_V1"}
```

## Strict boundary

This gate authorizes only the return from the fully completed api/context.js child to its frozen context-api.js parent edge. No context-api.js item is classified in this gate. No JavaScript is executed, no completed child source is reread, the OTEL authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
