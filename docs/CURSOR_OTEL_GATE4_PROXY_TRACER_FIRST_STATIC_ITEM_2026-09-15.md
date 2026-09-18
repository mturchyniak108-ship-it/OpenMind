# Cursor OTEL Gate-4 ProxyTracer first static item

Date: 2026-09-15

## Status

- Classification status: PASS
- Child module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracer.js`
- Exactly one child item classified: YES
- Additional child item classified: NO
- ProxyTracerProvider frontier remains: 153
- trace-api frontier remains: 285
- OTEL frontier remains: 467
- Source executed: NO

## Authorized module record

- Record start: 26481
- Record end: 27267
- Record SHA256: `86a8030c988d2831b36a487fc8109317b62143566ae08cc669e957fe24c477ca`
- Body bytes: 663
- Body chars: 663
- Body SHA256: `b1bc0b206c1e21d7e82abc0105f567af585a8f293eccd870fe696ef9d3c2816d`

## First ProxyTracer item

- Span: 0:12
- Kind: `DIRECTIVE`
- Binding: `NONE`
- Source SHA256: `4ee188e1744c19816e95a540b2650ed9f033ea0371e74eac8e717355cfca8741`
- Row SHA256: `43b8310632d9e5dddff2af160c67a6ceb883b25f18a36abb3ddcbe91e9ecbc45`
- Boundary: `STATEMENT_SEMICOLON`
- Body end reached: NO
- Dependency count: 0
- Dependency modules: `[]`

## Classification evidence

Evidence SHA256: `857461d8b24cdba64471bc9e13b655efc4914114b20740b2166ddf798c334fd1`

```json
{"body_bytes":663,"body_chars":663,"body_sha256":"b1bc0b206c1e21d7e82abc0105f567af585a8f293eccd870fe696ef9d3c2816d","classification_count_this_gate":1,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","first_item":{"binding":null,"body_end_reached":false,"boundary_kind":"STATEMENT_SEMICOLON","dependencies":[],"dependency_count":0,"end":12,"kind":"DIRECTIVE","source":"\"use strict\"","source_sha256":"4ee188e1744c19816e95a540b2650ed9f033ea0371e74eac8e717355cfca8741","start":0,"structural_prefix_end":0,"structural_prefix_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","structural_prefix_start":0},"first_item_sha256":"43b8310632d9e5dddff2af160c67a6ceb883b25f18a36abb3ddcbe91e9ecbc45","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracer.js","next_additional_item_classified":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","otel_frontier_end":467,"provider_frontier_end":153,"provider_frontier_resume_authorized":false,"qualification_contract_sha256":"d0f8a7abba092cdaf8236a922db3bd5f2d9eb310f804476e9dc82a0aea6a4dc2","qualification_evidence_sha256":"bd73ee49a82889dc8ed202345b556081c9064c4f02fe2a4c0798cf64f57e8471","record_end":27267,"record_sha256":"86a8030c988d2831b36a487fc8109317b62143566ae08cc669e957fe24c477ca","record_start":26481,"source_executed":false,"trace_api_frontier_end":285,"trace_api_frontier_resume_authorized":false,"version":"GATE4_PROXY_TRACER_FIRST_STATIC_ITEM_V1"}
```

## Strict boundary

This gate performs only the authorized static read of the uniquely identified ProxyTracer.js webpack module record and classifies exactly its first eligible item. No second ProxyTracer.js item is classified. Any dependency is identified only from the frozen first-item text and no dependency source is opened. ProxyTracer.js completion is not claimed. No return to ProxyTracerProvider.js is attempted. ProxyTracerProvider.js remains frozen at offset 153. trace-api.js remains frozen at offset 285. OTEL remains frozen at offset 467. No source is executed, the frozen authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
