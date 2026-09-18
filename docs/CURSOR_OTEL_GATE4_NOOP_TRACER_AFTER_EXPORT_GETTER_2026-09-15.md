# Cursor OTEL Gate-4 NoopTracer item after export getter

Date: 2026-09-15

## Status

- Classification status: PASS
- Module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/NoopTracer.js`
- Previous item span: 13:29
- Resume semicolon span: 29:30
- Exactly one additional child item classified: YES
- Further child item classified: NO
- ProxyTracer frontier remains: 159
- ProxyTracerProvider frontier remains: 153
- trace-api frontier remains: 285
- OTEL frontier remains: 467

## Newly classified NoopTracer item

- Declaration prefix: `var`
- Item span: 34:147
- Kind: `STATIC_BINDING`
- Binding: `r`
- Source SHA256: `8d42d0619f877fdbe1e3cca3cbc3d4b42a784bee99554b444413c0f96567c0ce`
- Row SHA256: `c1a1db7d637311d517a6305f70041e382ce85e8173a900f2e6252640a54abf4e`
- Boundary: `DECLARATOR_COMMA`
- Body end reached: NO
- Dependency count: 1
- Dependency modules: `["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js"]`

## Classification evidence

Evidence SHA256: `4333e3b7d1c4eba5247b630235b1dde3f91f4ead8dfc9d4ecb766e441835711e`

```json
{"body_chars":1112,"body_sha256":"cca1354fa44e399622bfafd82c46fe6ecb153660a6a151c7159fa94bd4638b3f","classification_count_this_gate":1,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/NoopTracer.js","next_additional_item_classified":false,"next_item":{"binding":"r","body_end_reached":false,"boundary_kind":"DECLARATOR_COMMA","declaration_prefix":"var","declaration_prefix_end":34,"declaration_prefix_sha256":"092090833731ec177e11c0f921ac9e0592e13aa6b6fcb5ad751246ee46fe8014","declaration_prefix_start":30,"dependencies":[{"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","relative_end":113,"relative_start":2,"source":"n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js\")","source_sha256":"b7b76c13dd6c6e0937eba3548b8a9a6c03431365c8022422f25b547b5c41db4a"}],"dependency_count":1,"end":147,"kind":"STATIC_BINDING","source":"r=n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js\")","source_sha256":"8d42d0619f877fdbe1e3cca3cbc3d4b42a784bee99554b444413c0f96567c0ce","start":34,"whitespace_prefix_end":30,"whitespace_prefix_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","whitespace_prefix_start":30},"next_item_sha256":"c1a1db7d637311d517a6305f70041e382ce85e8173a900f2e6252640a54abf4e","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","otel_frontier_end":467,"previous_item_end":29,"previous_item_evidence_sha256":"3ed2ece604bb2a867cf5db41956c7b63d087f0d5786499c5b802ce466a0b034d","previous_item_row_sha256":"b30e3a725779f3948f935abb0984cc4e42a641676d90a88d85e6593186aed2c5","provider_frontier_end":153,"proxy_tracer_frontier_end":159,"proxy_tracer_frontier_resume_authorized":false,"record_sha256":"21e7c05873488b19e50b3069dfc3540fe4cbf007549b238b8ea5c98d87b0c445","resume_delimiter":";","resume_delimiter_end":30,"resume_delimiter_start":29,"source_executed":false,"trace_api_frontier_end":285,"trace_api_frontier_resume_authorized":false,"version":"GATE4_NOOP_TRACER_AFTER_EXPORT_GETTER_V1"}
```

## Strict boundary

This gate advances exactly one NoopTracer.js item after the export-getter semicolon at 29:30. A leading var declaration prefix is treated only as structural syntax and at most one declarator is classified. Any dependency is identified only from the frozen item text and no dependency source is opened. No later NoopTracer.js item is classified. NoopTracer.js completion is not claimed. No return to ProxyTracer.js is attempted. ProxyTracer.js remains frozen at offset 159. ProxyTracerProvider.js remains frozen at offset 153. trace-api.js remains frozen at offset 285. OTEL remains frozen at offset 467. No source is executed, the frozen authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
