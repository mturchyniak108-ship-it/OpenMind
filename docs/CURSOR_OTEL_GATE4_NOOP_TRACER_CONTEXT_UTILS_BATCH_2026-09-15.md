# Cursor OTEL Gate-4 NoopTracer context-utils larger batch

Date: 2026-09-15

## Status

- Batch status: PASS
- Caller module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/NoopTracer.js`
- Caller item span: 148:269
- Caller binding: `s`
- Caller frontier remains: 269
- Child module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/context-utils.js`
- Qualification mode: `AUTHORITY_ABSENCE_BOUNDED_CHILD_SOURCE_READ_AUTHORIZED`
- Batch item count: 3
- Stop reason: `FIRST_UNRESOLVED_DEPENDENCY`
- Child completed in this batch: NO
- api context source reread: NO
- ProxyTracer frontier remains: 159
- ProxyTracerProvider frontier remains: 153
- trace-api frontier remains: 285
- OTEL frontier remains: 467

## Batch items

- Item 1 span: 0:12
- Item 1 kind: `DIRECTIVE`
- Item 1 binding: `NONE`
- Item 1 boundary: `STATEMENT_SEMICOLON`
- Item 1 unresolved dependencies: 0
- Item 1 row SHA256: `0de86c716388200531f2f3ae9052466016400ed3ad9ac2292b48bacec577616b`
- Item 2 span: 13:75
- Item 2 kind: `WEBPACK_EXPORT_GETTER_INSTALLATION`
- Item 2 binding: `NONE`
- Item 2 boundary: `STATEMENT_SEMICOLON`
- Item 2 unresolved dependencies: 0
- Item 2 row SHA256: `f26f6d241a63b703ddec8b39582eaf95a26f9cf05fe367e5e84d4432de3af457`
- Item 3 span: 80:197
- Item 3 kind: `STATIC_BINDING`
- Item 3 binding: `r`
- Item 3 boundary: `DECLARATOR_COMMA`
- Item 3 unresolved dependencies: 1
- Item 3 row SHA256: `c633264bfad0ff0320b1eaae05b2b126dfe72d3091046286d9d5c239e9d060cd`

## Batch contract

Contract SHA256: `463bc4820345ed0c56554d9df06950ca82cbeb42099a0d17a1d75993e0c63e71`

```json
{"api_context_source_reread_performed":false,"batch_item_count":3,"body_full_coverage":false,"context_utils_completed":false,"context_utils_completed_state_sha256":null,"context_utils_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/context-utils.js","declaration_group_complete":false,"dependency_source_sha256":"8cf33f91e81df5f9edaa7a100589268e6c5d462b0ddd27d6e5e5a0013b295c11","direct_authority_state_count":0,"embedded_authority_reference_count":0,"exact_authority_reference_count":0,"header_end":28616,"header_occurrence_count":1,"header_sha256":"c787aed511f75872f377a457f8dee073c86e786c2a484d50431a899caa766924","header_start":28492,"incomplete_authority_state_count":0,"items":[{"binding":null,"boundary_kind":"STATEMENT_SEMICOLON","declaration_prefix":null,"dependency_count":0,"dependency_results":[],"end":12,"kind":"DIRECTIVE","row_sha256":"0de86c716388200531f2f3ae9052466016400ed3ad9ac2292b48bacec577616b","source":"\"use strict\"","source_sha256":"4ee188e1744c19816e95a540b2650ed9f033ea0371e74eac8e717355cfca8741","start":0,"structural_prefix_end":0,"structural_prefix_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","structural_prefix_start":0,"unresolved_dependency_count":0},{"binding":null,"boundary_kind":"STATEMENT_SEMICOLON","declaration_prefix":null,"dependency_count":0,"dependency_results":[],"end":75,"kind":"WEBPACK_EXPORT_GETTER_INSTALLATION","row_sha256":"f26f6d241a63b703ddec8b39582eaf95a26f9cf05fe367e5e84d4432de3af457","source":"n.d(t,{Bk:()=>l,Bx:()=>u,EW:()=>c,fU:()=>a,g_:()=>d,w8:()=>m})","source_sha256":"1bca009087884eeb2c999ca4cb12bd2c9d128bec0d5d4b4e221e490751b870a0","start":13,"structural_prefix_end":13,"structural_prefix_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","structural_prefix_start":13,"unresolved_dependency_count":0},{"binding":"r","boundary_kind":"DECLARATOR_COMMA","declaration_prefix":"var","dependency_count":1,"dependency_results":[{"closure_mode":"UNRESOLVED","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context/context.js","status":"OPEN"}],"end":197,"kind":"STATIC_BINDING","row_sha256":"c633264bfad0ff0320b1eaae05b2b126dfe72d3091046286d9d5c239e9d060cd","source":"r=n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context/context.js\")","source_sha256":"4ce03a3763d36ad0f384fdc7c44df60924e2e2b8d801af9cb4be902490381ab5","start":80,"structural_prefix_end":80,"structural_prefix_sha256":"092090833731ec177e11c0f921ac9e0592e13aa6b6fcb5ad751246ee46fe8014","structural_prefix_start":76,"unresolved_dependency_count":1}],"noop_tracer_frontier_end":269,"noop_tracer_frontier_resume_authorized_after_this_gate":false,"otel_frontier_end":467,"provider_frontier_end":153,"proxy_tracer_frontier_end":159,"qualification_mode":"AUTHORITY_ABSENCE_BOUNDED_CHILD_SOURCE_READ_AUTHORIZED","record_end":29385,"record_sha256":"55bf7a1fff4c3e26a63b31061e59f3d4d28d1f7ceda3c240d901e7d63d4bbc50","record_start":28492,"reused_dependency_modules":[],"source_execution_authorized":false,"stop_reason":"FIRST_UNRESOLVED_DEPENDENCY","trace_api_frontier_end":285,"unresolved_dependency_modules":["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context/context.js"],"version":"GATE4_NOOP_TRACER_CONTEXT_UTILS_BATCH_V1"}
```

## Batch evidence

Evidence SHA256: `1171a4ed0eb50ed202994b781fef3a8590715ee51f6a8001fde735da0f85b925`

```json
{"batch_contract":{"api_context_source_reread_performed":false,"batch_item_count":3,"body_full_coverage":false,"context_utils_completed":false,"context_utils_completed_state_sha256":null,"context_utils_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/context-utils.js","declaration_group_complete":false,"dependency_source_sha256":"8cf33f91e81df5f9edaa7a100589268e6c5d462b0ddd27d6e5e5a0013b295c11","direct_authority_state_count":0,"embedded_authority_reference_count":0,"exact_authority_reference_count":0,"header_end":28616,"header_occurrence_count":1,"header_sha256":"c787aed511f75872f377a457f8dee073c86e786c2a484d50431a899caa766924","header_start":28492,"incomplete_authority_state_count":0,"items":[{"binding":null,"boundary_kind":"STATEMENT_SEMICOLON","declaration_prefix":null,"dependency_count":0,"dependency_results":[],"end":12,"kind":"DIRECTIVE","row_sha256":"0de86c716388200531f2f3ae9052466016400ed3ad9ac2292b48bacec577616b","source":"\"use strict\"","source_sha256":"4ee188e1744c19816e95a540b2650ed9f033ea0371e74eac8e717355cfca8741","start":0,"structural_prefix_end":0,"structural_prefix_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","structural_prefix_start":0,"unresolved_dependency_count":0},{"binding":null,"boundary_kind":"STATEMENT_SEMICOLON","declaration_prefix":null,"dependency_count":0,"dependency_results":[],"end":75,"kind":"WEBPACK_EXPORT_GETTER_INSTALLATION","row_sha256":"f26f6d241a63b703ddec8b39582eaf95a26f9cf05fe367e5e84d4432de3af457","source":"n.d(t,{Bk:()=>l,Bx:()=>u,EW:()=>c,fU:()=>a,g_:()=>d,w8:()=>m})","source_sha256":"1bca009087884eeb2c999ca4cb12bd2c9d128bec0d5d4b4e221e490751b870a0","start":13,"structural_prefix_end":13,"structural_prefix_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","structural_prefix_start":13,"unresolved_dependency_count":0},{"binding":"r","boundary_kind":"DECLARATOR_COMMA","declaration_prefix":"var","dependency_count":1,"dependency_results":[{"closure_mode":"UNRESOLVED","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context/context.js","status":"OPEN"}],"end":197,"kind":"STATIC_BINDING","row_sha256":"c633264bfad0ff0320b1eaae05b2b126dfe72d3091046286d9d5c239e9d060cd","source":"r=n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context/context.js\")","source_sha256":"4ce03a3763d36ad0f384fdc7c44df60924e2e2b8d801af9cb4be902490381ab5","start":80,"structural_prefix_end":80,"structural_prefix_sha256":"092090833731ec177e11c0f921ac9e0592e13aa6b6fcb5ad751246ee46fe8014","structural_prefix_start":76,"unresolved_dependency_count":1}],"noop_tracer_frontier_end":269,"noop_tracer_frontier_resume_authorized_after_this_gate":false,"otel_frontier_end":467,"provider_frontier_end":153,"proxy_tracer_frontier_end":159,"qualification_mode":"AUTHORITY_ABSENCE_BOUNDED_CHILD_SOURCE_READ_AUTHORIZED","record_end":29385,"record_sha256":"55bf7a1fff4c3e26a63b31061e59f3d4d28d1f7ceda3c240d901e7d63d4bbc50","record_start":28492,"reused_dependency_modules":[],"source_execution_authorized":false,"stop_reason":"FIRST_UNRESOLVED_DEPENDENCY","trace_api_frontier_end":285,"unresolved_dependency_modules":["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context/context.js"],"version":"GATE4_NOOP_TRACER_CONTEXT_UTILS_BATCH_V1"},"batch_contract_sha256":"463bc4820345ed0c56554d9df06950ca82cbeb42099a0d17a1d75993e0c63e71","body_bytes":768,"body_chars":768,"body_sha256":"2e7d5ad1df916dcbc766c9ad3a19deb0c66648b762afd381c8d7146ff4ca2551","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","dependency_source_opened_before_authorization":false,"noop_tracer_item_evidence_sha256":"d62b84468347e5edb6744c1b2a95a78c38dfcab0377d54f08b3219c4ca4a5253","noop_tracer_item_row_sha256":"ef43c5932960bc8ef1b3e06f7a1d9c8b4173699e85ab22eea0a31209c04680f7","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","source_executed":false,"version":"GATE4_NOOP_TRACER_CONTEXT_UTILS_BATCH_EVIDENCE_V1"}
```

## Strict boundary

This larger block qualifies the context-utils.js dependency and, when bounded source reading is authorized, classifies multiple adjacent safe preamble or declaration items in one pass. Already completed api/context.js authority may be reused without source reread. The batch stops at the first unresolved dependency, authority ambiguity, completed declaration group, module end, or hard item limit. No unresolved dependency source is opened. NoopTracer.js remains frozen at offset 269 unless context-utils.js becomes fully complete, and even then no NoopTracer.js parent item is classified in this block. ProxyTracer.js remains frozen at offset 159. ProxyTracerProvider.js remains frozen at offset 153. trace-api.js remains frozen at offset 285. OTEL remains frozen at offset 467. No source is executed, the frozen authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
