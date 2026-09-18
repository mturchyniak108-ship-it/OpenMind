# Cursor OTEL Gate-4 ProxyTracerProvider next static item

Date: 2026-09-15

## Status

- Classification status: PASS
- Module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracerProvider.js`
- Previous item span: 0:12
- Resume semicolon span: 12:13
- Exactly one additional child item classified: YES
- Further child item classified: NO
- trace-api frontier remains: 285
- OTEL frontier remains: 467

## Next child item

- Span: 13:29
- Kind: `WEBPACK_EXPORT_GETTER_INSTALLATION`
- Binding: `NONE`
- Source SHA256: `3a4ebee7f887018504ad488ce48414615bf69f5bc0dd07e119cedea8e33e893f`
- Row SHA256: `1bb70ff9c47d64b218c9c80c384a4b637e86190ad8476fd0c2372b23e8a60d56`
- Boundary: `STATEMENT_SEMICOLON`
- Body end reached: NO
- Dependency count: 0
- Dependency modules: `[]`

## Classification evidence

Evidence SHA256: `b277783077498ed79b6bd755c8e5fa06da1bf694e0ea35a1ba1f158e357bdf6a`

```json
{"body_chars":805,"body_sha256":"8730d97b0735d9b50fcf9957d3fe0116543c0c48df8a4433544ac5e0a714557c","classification_count_this_gate":1,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracerProvider.js","next_additional_item_classified":false,"next_item":{"binding":null,"body_end_reached":false,"boundary_kind":"STATEMENT_SEMICOLON","dependencies":[],"dependency_count":0,"end":29,"kind":"WEBPACK_EXPORT_GETTER_INSTALLATION","source":"n.d(t,{n:()=>o})","source_sha256":"3a4ebee7f887018504ad488ce48414615bf69f5bc0dd07e119cedea8e33e893f","start":13,"structural_prefix_end":13,"structural_prefix_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","structural_prefix_start":13},"next_item_sha256":"1bb70ff9c47d64b218c9c80c384a4b637e86190ad8476fd0c2372b23e8a60d56","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","otel_frontier_end":467,"previous_item_end":12,"previous_item_evidence_sha256":"828c0b57f3198755a3e021939f69107a0ffecdd03f7bce7ab1acd1bbd3c01b4a","previous_item_row_sha256":"43b8310632d9e5dddff2af160c67a6ceb883b25f18a36abb3ddcbe91e9ecbc45","record_sha256":"841a1e1f7f049a2c4cb3b1444765dbde3c6b95843e2bbd1d2502504d5cbd5077","resume_delimiter":";","resume_delimiter_end":13,"resume_delimiter_start":12,"source_executed":false,"trace_api_frontier_end":285,"trace_api_frontier_resume_authorized":false,"version":"GATE4_PROXY_TRACER_PROVIDER_NEXT_STATIC_ITEM_V1"}
```

## Strict boundary

This gate advances exactly one ProxyTracerProvider.js item after the qualified first-item semicolon at 12:13. No third child item is classified. Any dependency is identified only from the frozen item text and no dependency source is opened. ProxyTracerProvider.js completion is not claimed. No return to trace-api.js is attempted. trace-api.js remains frozen at offset 285. OTEL remains frozen at offset 467. No source is executed, the frozen authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
