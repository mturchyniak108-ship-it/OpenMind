# Cursor OTEL Gate-4 ProxyTracerProvider first static item

Date: 2026-09-15

## Status

- Classification status: PASS
- Child module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracerProvider.js`
- Exactly one child item classified: YES
- Additional child item classified: NO
- trace-api frontier remains: 285
- OTEL frontier remains: 467
- Source executed: NO

## Authorized module record

- Record start: 27268
- Record end: 28204
- Record SHA256: `841a1e1f7f049a2c4cb3b1444765dbde3c6b95843e2bbd1d2502504d5cbd5077`
- Body bytes: 805
- Body chars: 805
- Body SHA256: `8730d97b0735d9b50fcf9957d3fe0116543c0c48df8a4433544ac5e0a714557c`

## First child item

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

Evidence SHA256: `828c0b57f3198755a3e021939f69107a0ffecdd03f7bce7ab1acd1bbd3c01b4a`

```json
{"body_bytes":805,"body_chars":805,"body_sha256":"8730d97b0735d9b50fcf9957d3fe0116543c0c48df8a4433544ac5e0a714557c","classification_count_this_gate":1,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","first_item":{"binding":null,"body_end_reached":false,"boundary_kind":"STATEMENT_SEMICOLON","dependencies":[],"dependency_count":0,"end":12,"kind":"DIRECTIVE","source":"\"use strict\"","source_sha256":"4ee188e1744c19816e95a540b2650ed9f033ea0371e74eac8e717355cfca8741","start":0,"structural_prefix_end":0,"structural_prefix_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","structural_prefix_start":0},"first_item_sha256":"43b8310632d9e5dddff2af160c67a6ceb883b25f18a36abb3ddcbe91e9ecbc45","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracerProvider.js","next_additional_item_classified":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","otel_frontier_end":467,"otel_frontier_resume_authorized":false,"qualification_contract_sha256":"f6ecf9bf83ca3813914d89dfd0d2a21a0052d236c5245ce406629983216122c1","qualification_evidence_sha256":"16d01b36acc073c224af8e9f2bfaad9040cc27773757ba0dca0c0e5cc47a96a7","record_end":28204,"record_sha256":"841a1e1f7f049a2c4cb3b1444765dbde3c6b95843e2bbd1d2502504d5cbd5077","record_start":27268,"source_executed":false,"trace_api_frontier_end":285,"trace_api_frontier_resume_authorized":false,"version":"GATE4_PROXY_TRACER_PROVIDER_FIRST_STATIC_ITEM_V1"}
```

## Strict boundary

This gate performs only the previously authorized static read of the uniquely identified ProxyTracerProvider.js webpack module record and classifies exactly its first eligible item. No second ProxyTracerProvider.js item is classified. Any dependency is identified only from the already read first-item text and no dependency source is opened. ProxyTracerProvider.js completion is not claimed. No return to trace-api.js is attempted. trace-api.js remains frozen at offset 285. OTEL remains frozen at offset 467. No source is executed, the frozen authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
