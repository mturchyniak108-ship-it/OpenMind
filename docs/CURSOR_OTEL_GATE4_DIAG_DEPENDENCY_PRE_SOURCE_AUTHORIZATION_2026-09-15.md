# Cursor OTEL Gate-4 diag.js dependency pre-source authorization

Date: 2026-09-15

## Status

- Audit status: PASS
- Current parent leaf: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js`
- Classified dependency: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js`
- Authorization status: `NOT_AUTHORIZED_DIAG_METADATA_INSUFFICIENT`
- Completed state reuse ready: NO
- Source read authorized: NO
- Source read performed: NO
- Source executed: NO
- OTEL authority mutated: NO

## Frozen parent frontier

- Frontier kind: `WEBPACK_REQUIRE_BINDING`
- Binding: `o`
- Source SHA256: `6cd448ef0f65cdde11d39816a657b76ed14ddffcf5e3aecc9b034d08127571db`
- Source: `o=n("../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js")`

## Current authority topology

- diag.js references: 0
- Substantive diag.js states: 0
- Completed substantive states: 0
- Incomplete substantive states: 0

## Historical metadata

- JSON files seen: 966
- JSON files parsed: 958
- JSON parse failures: 8
- Substantive diag.js state occurrences: 0
- Unique body SHA identities: `[]`
- Unique body_chars identities: `[]`

## Adjudication

- Next authority: `NONE`
- Body identity unique: NO
- Completed reuse contract SHA256: `64f7ca16a1bd5b722753bd55040b0841f514577f8d84ff1781507866860ad762`
- Bounded source-read contract SHA256: `235d3775bf63dde81d56469f97e12072a32dde7d35c537ecd063165a95430fe6`

## Evidence

Evidence SHA256: `a9517a6e689cb5697327072d570137c51eb94576ef4f22772ba21100aee1033d`

```json
{"api_context_frontier_evidence_sha256":"ad64be1a74ea6b364f114d1b98918c4ef3d9983f7e8734b2e3fb79066ac5b973","api_context_leaf_sha256":"47856b82a05b810ab52f95549b74a720305e3a86f5bdeb5ab2a6c58ba6cedebf","authorization_status":"NOT_AUTHORIZED_DIAG_METADATA_INSUFFICIENT","body_identity_unique":false,"completed_reuse_ready":false,"completed_reuse_state_sha256":null,"corpus_body_chars_counts":{},"corpus_body_sha_counts":{},"corpus_completed_state_sha_counts":{},"corpus_examples":[],"corpus_incomplete_state_sha_counts":{},"corpus_state_sha_counts":{},"current_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","current_completed_state_count":0,"current_completed_state_shas":[],"current_diag_reference_count":0,"current_diag_states":[],"current_incomplete_state_count":0,"current_incomplete_state_shas":[],"current_substantive_state_count":0,"diag_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","frontier_binding":"o","frontier_kind":"WEBPACK_REQUIRE_BINDING","frontier_source":"o=n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js\")","frontier_source_sha256":"6cd448ef0f65cdde11d39816a657b76ed14ddffcf5e3aecc9b034d08127571db","json_failures":8,"json_parsed":958,"json_seen":966,"next_authority":"NONE","reuse_contract":{"completed_state_body_chars":null,"completed_state_body_sha256":null,"completed_state_paths":[],"completed_state_sha256":null,"execution_authorized":false,"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","mutation_authorized":false,"required_next_audit":"EXACT_API_CONTEXT_DEPENDENCY_PROPAGATION_AND_REFERENCE_MAP","version":"GATE4_DIAG_COMPLETED_STATE_REUSE_CONTRACT_V1"},"reuse_contract_sha256":"64f7ca16a1bd5b722753bd55040b0841f514577f8d84ff1781507866860ad762","source_read_authorized":false,"source_read_contract":{"body_chars":null,"body_sha256":null,"bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","execution_authorized":false,"method_definition_token":"\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js\"(e,t,n){","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","read_mode":"EXACT_METHOD_STYLE_WEBPACK_RECORD_BODY_ONLY","requirements":["current Cursor bundle SHA must remain frozen","exact quoted diag.js method-style webpack definition must be unique","only that one module wrapper body may be extracted","extracted body_chars must equal qualified metadata","extracted body SHA256 must equal qualified metadata","source must never be executed","qualification stops after the first currently unqualified static item"],"version":"GATE4_DIAG_BOUNDED_SOURCE_READ_CONTRACT_V1"},"source_read_contract_sha256":"235d3775bf63dde81d56469f97e12072a32dde7d35c537ecd063165a95430fe6","substantive_corpus_state_count":0,"unique_body_chars":[],"unique_body_shas":[],"version":"GATE4_DIAG_DEPENDENCY_PRE_SOURCE_AUTHORIZATION_V1"}
```

## Strict boundary

This gate used existing qualification JSON metadata only for diag.js state adjudication. No diag.js module body was extracted, no source was executed, and the OTEL authority was not mutated.
