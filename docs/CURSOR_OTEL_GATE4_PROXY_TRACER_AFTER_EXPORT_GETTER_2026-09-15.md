# Cursor OTEL Gate-4 ProxyTracer item after export getter

Date: 2026-09-15

## Status

- Classification status: PASS
- Module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracer.js`
- Previous item span: 13:29
- Resume semicolon span: 29:30
- Exactly one additional child item classified: YES
- Further child item classified: NO
- ProxyTracerProvider frontier remains: 153
- trace-api frontier remains: 285
- OTEL frontier remains: 467

## Newly classified ProxyTracer item

- Declaration prefix: `var`
- Item span: 34:159
- Kind: `STATIC_BINDING`
- Binding: `r`
- Source SHA256: `7e4ce37da119bc68ace2108541aaeb8ddc833165b742273872a7e2d678a5e1fb`
- Row SHA256: `ba63990a91042e934d6b8b6595933146a714114ecd51388f2cb28c96fc297931`
- Boundary: `DECLARATOR_COMMA`
- Body end reached: NO
- Dependency count: 1
- Dependency modules: `["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/NoopTracer.js"]`

## Classification evidence

Evidence SHA256: `967d85ef5e3942e3e6340c51dbef99d608789bc9619c7f7d5ecbc806b6bb2319`

```json
{"body_chars":663,"body_sha256":"b1bc0b206c1e21d7e82abc0105f567af585a8f293eccd870fe696ef9d3c2816d","classification_count_this_gate":1,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracer.js","next_additional_item_classified":false,"next_item":{"binding":"r","body_end_reached":false,"boundary_kind":"DECLARATOR_COMMA","declaration_prefix":"var","declaration_prefix_end":34,"declaration_prefix_sha256":"092090833731ec177e11c0f921ac9e0592e13aa6b6fcb5ad751246ee46fe8014","declaration_prefix_start":30,"dependencies":[{"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/NoopTracer.js","relative_end":122,"relative_start":6,"source":"n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/NoopTracer.js\")","source_sha256":"c91ce49f655226cce76f0d124c824a6368eff86b7952c5b43b0cd18dd955d870"}],"dependency_count":1,"end":159,"kind":"STATIC_BINDING","source":"r=new(n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/NoopTracer.js\").o)","source_sha256":"7e4ce37da119bc68ace2108541aaeb8ddc833165b742273872a7e2d678a5e1fb","start":34,"whitespace_prefix_end":30,"whitespace_prefix_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","whitespace_prefix_start":30},"next_item_sha256":"ba63990a91042e934d6b8b6595933146a714114ecd51388f2cb28c96fc297931","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","otel_frontier_end":467,"previous_item_end":29,"previous_item_evidence_sha256":"b0825783e41e8a43b8ab03f5a0e88c5daa151e88f9d27a1c3b8e9edf25326329","previous_item_row_sha256":"b27329f7768ee8d72a54e245a605491f250b61be63ba0036dedf2b2903b2d67d","provider_frontier_end":153,"provider_frontier_resume_authorized":false,"record_sha256":"86a8030c988d2831b36a487fc8109317b62143566ae08cc669e957fe24c477ca","resume_delimiter":";","resume_delimiter_end":30,"resume_delimiter_start":29,"source_executed":false,"trace_api_frontier_end":285,"trace_api_frontier_resume_authorized":false,"version":"GATE4_PROXY_TRACER_AFTER_EXPORT_GETTER_V1"}
```

## Strict boundary

This gate advances exactly one ProxyTracer.js item after the export-getter semicolon at 29:30. A leading var declaration prefix is treated only as structural syntax and at most one declarator is classified. Any dependency is identified only from the frozen item text and no dependency source is opened. No later ProxyTracer.js item is classified. ProxyTracer.js completion is not claimed. No return to ProxyTracerProvider.js is attempted. ProxyTracerProvider.js remains frozen at offset 153. trace-api.js remains frozen at offset 285. OTEL remains frozen at offset 467. No source is executed, the frozen authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
