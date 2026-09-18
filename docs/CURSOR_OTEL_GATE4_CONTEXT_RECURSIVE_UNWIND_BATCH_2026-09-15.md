# Cursor OTEL Gate-4 repaired context recursive unwind batch

Date: 2026-09-15

## Status

- Batch status: PASS
- context/context.js authority discovery mode: CONTENT BASED
- context/context.js supporting documents: 2
- context/context.js source reread: NO
- context-utils.js new items: 1
- context-utils.js completed: NO
- NoopTracer.js recursive unwind reached: NO
- NoopTracer.js new items: 0
- NoopTracer.js completed: NO
- ProxyTracer.js frontier remains: 159
- ProxyTracerProvider.js frontier remains: 153
- trace-api.js frontier remains: 285
- OTEL frontier remains: 467

## Recursive contract

Contract SHA256: `67672603d84516fb9062bb7a8900596dba80bb822f671aaa25e30fd11d6e6f52`

```json
{"context_context_authority":{"commit":"920be865c552795412fd69d9eae93385b7f4c1ce","document":"docs/CURSOR_OTEL_GATE4_API_CONTEXT_MODULE_COMPLETION_2026-09-15.md","document_sha256":"bc13e338a2e889001e92df87014718bbdac32e8b45e813fe51b12f5f7c446e4f","json_path":"$.completed_dependencies[1]","score":200,"state_sha256":"e303bd5f3daa7721b8855ee2440b254971fba3717c9f96067e9d19d819e53435","supporting_candidate_count":2,"supporting_documents":["docs/CURSOR_OTEL_GATE4_API_CONTEXT_MODULE_COMPLETION_2026-09-15.md","docs/CURSOR_OTEL_GATE4_API_CONTEXT_PREDIAG_DEPENDENCY_CLOSURE_2026-09-15.md"]},"context_context_source_reread":false,"context_utils_completed":false,"context_utils_completed_state_sha256":null,"context_utils_resume":{"completed":false,"cursor":198,"in_declaration_group":true,"reused_dependencies":[],"rows":[{"binding":"s","boundary_kind":"DECLARATOR_COMMA","declaration_prefix":null,"dependency_count":1,"dependency_results":[{"closure_mode":"UNRESOLVED","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/NonRecordingSpan.js","source_read_performed":false,"status":"OPEN"}],"end":322,"kind":"STATIC_BINDING","row_sha256":"5332ec3daa904f00113f259e3355b890d91c7c54ff9e0817db167b073f50cbb8","source":"s=n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/NonRecordingSpan.js\")","source_sha256":"e0dd4ab99f4ff4a74d43b7c5a5aad0e47bf94277f95f20c3e068d604e6ef5174","start":198,"structural_prefix_end":198,"structural_prefix_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","structural_prefix_start":198,"unresolved_dependency_count":1}],"stop_reason":"FIRST_UNRESOLVED_DEPENDENCY","unresolved_dependencies":["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/NonRecordingSpan.js"]},"noop_tracer_completed":false,"noop_tracer_completed_state_sha256":null,"noop_tracer_resume":null,"otel_frontier_end":467,"provider_frontier_end":153,"proxy_tracer_frontier_end":159,"source_execution_authorized":false,"trace_api_frontier_end":285,"version":"GATE4_CONTEXT_RECURSIVE_UNWIND_REPAIRED_V1"}
```

## Recursive evidence

Evidence SHA256: `99ad696f6cf6988bfab5f60d6cf5cbf3d74dc84cb270d804adce0c2c8640ac81`

```json
{"context_batch_contract_sha256":"463bc4820345ed0c56554d9df06950ca82cbeb42099a0d17a1d75993e0c63e71","context_batch_evidence_sha256":"1171a4ed0eb50ed202994b781fef3a8590715ee51f6a8001fde735da0f85b925","context_context_source_read_performed":false,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","recursive_contract":{"context_context_authority":{"commit":"920be865c552795412fd69d9eae93385b7f4c1ce","document":"docs/CURSOR_OTEL_GATE4_API_CONTEXT_MODULE_COMPLETION_2026-09-15.md","document_sha256":"bc13e338a2e889001e92df87014718bbdac32e8b45e813fe51b12f5f7c446e4f","json_path":"$.completed_dependencies[1]","score":200,"state_sha256":"e303bd5f3daa7721b8855ee2440b254971fba3717c9f96067e9d19d819e53435","supporting_candidate_count":2,"supporting_documents":["docs/CURSOR_OTEL_GATE4_API_CONTEXT_MODULE_COMPLETION_2026-09-15.md","docs/CURSOR_OTEL_GATE4_API_CONTEXT_PREDIAG_DEPENDENCY_CLOSURE_2026-09-15.md"]},"context_context_source_reread":false,"context_utils_completed":false,"context_utils_completed_state_sha256":null,"context_utils_resume":{"completed":false,"cursor":198,"in_declaration_group":true,"reused_dependencies":[],"rows":[{"binding":"s","boundary_kind":"DECLARATOR_COMMA","declaration_prefix":null,"dependency_count":1,"dependency_results":[{"closure_mode":"UNRESOLVED","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/NonRecordingSpan.js","source_read_performed":false,"status":"OPEN"}],"end":322,"kind":"STATIC_BINDING","row_sha256":"5332ec3daa904f00113f259e3355b890d91c7c54ff9e0817db167b073f50cbb8","source":"s=n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/NonRecordingSpan.js\")","source_sha256":"e0dd4ab99f4ff4a74d43b7c5a5aad0e47bf94277f95f20c3e068d604e6ef5174","start":198,"structural_prefix_end":198,"structural_prefix_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","structural_prefix_start":198,"unresolved_dependency_count":1}],"stop_reason":"FIRST_UNRESOLVED_DEPENDENCY","unresolved_dependencies":["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/NonRecordingSpan.js"]},"noop_tracer_completed":false,"noop_tracer_completed_state_sha256":null,"noop_tracer_resume":null,"otel_frontier_end":467,"provider_frontier_end":153,"proxy_tracer_frontier_end":159,"source_execution_authorized":false,"trace_api_frontier_end":285,"version":"GATE4_CONTEXT_RECURSIVE_UNWIND_REPAIRED_V1"},"recursive_contract_sha256":"67672603d84516fb9062bb7a8900596dba80bb822f671aaa25e30fd11d6e6f52","source_executed":false,"version":"GATE4_CONTEXT_RECURSIVE_UNWIND_REPAIRED_EVIDENCE_V1"}
```

## Strict boundary

This corrected block repairs only the failed context/context.js completion-authority discovery by using committed document content rather than filename assumptions. Multiple supporting documents are accepted only when every discovered completion record converges on one completed-state identity. After that dependency is closed without source reread, the original larger recursive unwind proceeds and stops at the first new unresolved dependency or hard batch boundary. No unresolved dependency source is opened. No return to ProxyTracer.js is attempted. ProxyTracer.js remains frozen at offset 159. ProxyTracerProvider.js remains frozen at offset 153. trace-api.js remains frozen at offset 285. OTEL remains frozen at offset 467. No source is executed, the frozen authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
