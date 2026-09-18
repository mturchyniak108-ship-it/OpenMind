# Cursor OTEL Gate-4 ProxyTracer next static item

Date: 2026-09-15

## Status

- Classification status: PASS
- Module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracer.js`
- Previous item span: 0:12
- Resume semicolon span: 12:13
- Exactly one additional child item classified: YES
- Further child item classified: NO
- ProxyTracerProvider frontier remains: 153
- trace-api frontier remains: 285
- OTEL frontier remains: 467

## Next ProxyTracer item

- Span: 13:29
- Kind: `WEBPACK_EXPORT_GETTER_INSTALLATION`
- Binding: `NONE`
- Source SHA256: `d3e4df89ddcf041e25ca3a3933ca2aca5a48f56e90caf008d9c9023718aa988b`
- Row SHA256: `b27329f7768ee8d72a54e245a605491f250b61be63ba0036dedf2b2903b2d67d`
- Boundary: `STATEMENT_SEMICOLON`
- Body end reached: NO
- Dependency count: 0
- Dependency modules: `[]`

## Classification evidence

Evidence SHA256: `b0825783e41e8a43b8ab03f5a0e88c5daa151e88f9d27a1c3b8e9edf25326329`

```json
{"body_chars":663,"body_sha256":"b1bc0b206c1e21d7e82abc0105f567af585a8f293eccd870fe696ef9d3c2816d","classification_count_this_gate":1,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracer.js","next_additional_item_classified":false,"next_item":{"binding":null,"body_end_reached":false,"boundary_kind":"STATEMENT_SEMICOLON","dependencies":[],"dependency_count":0,"end":29,"kind":"WEBPACK_EXPORT_GETTER_INSTALLATION","source":"n.d(t,{y:()=>s})","source_sha256":"d3e4df89ddcf041e25ca3a3933ca2aca5a48f56e90caf008d9c9023718aa988b","start":13,"structural_prefix_end":13,"structural_prefix_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","structural_prefix_start":13},"next_item_sha256":"b27329f7768ee8d72a54e245a605491f250b61be63ba0036dedf2b2903b2d67d","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","otel_frontier_end":467,"previous_item_end":12,"previous_item_evidence_sha256":"857461d8b24cdba64471bc9e13b655efc4914114b20740b2166ddf798c334fd1","previous_item_row_sha256":"43b8310632d9e5dddff2af160c67a6ceb883b25f18a36abb3ddcbe91e9ecbc45","provider_frontier_end":153,"provider_frontier_resume_authorized":false,"record_sha256":"86a8030c988d2831b36a487fc8109317b62143566ae08cc669e957fe24c477ca","resume_delimiter":";","resume_delimiter_end":13,"resume_delimiter_start":12,"source_executed":false,"trace_api_frontier_end":285,"trace_api_frontier_resume_authorized":false,"version":"GATE4_PROXY_TRACER_NEXT_STATIC_ITEM_V1"}
```

## Strict boundary

This gate advances exactly one ProxyTracer.js item after the first-item semicolon at 12:13. No third ProxyTracer.js item is classified. Any dependency is identified only from the frozen item text and no dependency source is opened. ProxyTracer.js completion is not claimed. No return to ProxyTracerProvider.js is attempted. ProxyTracerProvider.js remains frozen at offset 153. trace-api.js remains frozen at offset 285. OTEL remains frozen at offset 467. No source is executed, the frozen authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
