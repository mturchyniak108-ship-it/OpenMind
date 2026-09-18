# Cursor OTEL Gate-4 ProxyTracerProvider item after export getter

Date: 2026-09-15

## Status

- Classification status: PASS
- Module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracerProvider.js`
- Previous item span: 13:29
- Resume semicolon span: 29:30
- Exactly one additional child item classified: YES
- Further child item classified: NO
- trace-api frontier remains: 285
- OTEL frontier remains: 467

## Newly classified item

- Declaration prefix: `var`
- Item span: 34:153
- Kind: `STATIC_BINDING`
- Binding: `r`
- Source SHA256: `4a9fbe9e03c013c7ebced0fc18ace86220d2226b59f0d083755953365de59f45`
- Row SHA256: `7a9e30d3c8b71fc24cb24929111757d1f9274797b87713bcdfec4c013566fcf8`
- Boundary: `DECLARATOR_COMMA`
- Body end reached: NO
- Dependency count: 1
- Dependency modules: `["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracer.js"]`

## Classification evidence

Evidence SHA256: `5eddbab60d8be1ef9a47633f011883cb6661e7c3f85b6d907563622ce5dfa330`

```json
{"body_chars":805,"body_sha256":"8730d97b0735d9b50fcf9957d3fe0116543c0c48df8a4433544ac5e0a714557c","classification_count_this_gate":1,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracerProvider.js","next_additional_item_classified":false,"next_item":{"binding":"r","body_end_reached":false,"boundary_kind":"DECLARATOR_COMMA","declaration_prefix":"var","declaration_prefix_end":34,"declaration_prefix_sha256":"092090833731ec177e11c0f921ac9e0592e13aa6b6fcb5ad751246ee46fe8014","declaration_prefix_start":30,"dependencies":[{"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracer.js","relative_end":119,"relative_start":2,"source":"n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracer.js\")","source_sha256":"7e05893b091b8128d2b9f8ac668056119981fdf372a425461ed3339ae11a7943"}],"dependency_count":1,"end":153,"kind":"STATIC_BINDING","source":"r=n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracer.js\")","source_sha256":"4a9fbe9e03c013c7ebced0fc18ace86220d2226b59f0d083755953365de59f45","start":34,"whitespace_prefix_end":30,"whitespace_prefix_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","whitespace_prefix_start":30},"next_item_sha256":"7a9e30d3c8b71fc24cb24929111757d1f9274797b87713bcdfec4c013566fcf8","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","otel_frontier_end":467,"previous_item_end":29,"previous_item_evidence_sha256":"b277783077498ed79b6bd755c8e5fa06da1bf694e0ea35a1ba1f158e357bdf6a","previous_item_row_sha256":"1bb70ff9c47d64b218c9c80c384a4b637e86190ad8476fd0c2372b23e8a60d56","record_sha256":"841a1e1f7f049a2c4cb3b1444765dbde3c6b95843e2bbd1d2502504d5cbd5077","resume_delimiter":";","resume_delimiter_end":30,"resume_delimiter_start":29,"source_executed":false,"trace_api_frontier_end":285,"trace_api_frontier_resume_authorized":false,"version":"GATE4_PROXY_TRACER_PROVIDER_AFTER_EXPORT_GETTER_V1"}
```

## Strict boundary

This gate advances exactly one ProxyTracerProvider.js item after the export-getter semicolon at 29:30. A leading var declaration prefix is treated only as structural syntax and at most one declarator is classified. Any dependency is identified only from the frozen item text and no dependency source is opened. No later ProxyTracerProvider.js item is classified. ProxyTracerProvider.js completion is not claimed. No return to trace-api.js is attempted. trace-api.js remains frozen at offset 285. OTEL remains frozen at offset 467. No source is executed, the frozen authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
