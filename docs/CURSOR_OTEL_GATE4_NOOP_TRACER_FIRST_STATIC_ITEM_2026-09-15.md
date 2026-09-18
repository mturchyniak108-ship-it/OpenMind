# Cursor OTEL Gate-4 NoopTracer first static item

Date: 2026-09-15

## Status

- Classification status: PASS
- Child module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/NoopTracer.js`
- Exactly one child item classified: YES
- Additional child item classified: NO
- ProxyTracer frontier remains: 159
- ProxyTracerProvider frontier remains: 153
- trace-api frontier remains: 285
- OTEL frontier remains: 467
- Source executed: NO

## Authorized module record

- Record start: 25246
- Record end: 26480
- Record SHA256: `21e7c05873488b19e50b3069dfc3540fe4cbf007549b238b8ea5c98d87b0c445`
- Body bytes: 1112
- Body chars: 1112
- Body SHA256: `cca1354fa44e399622bfafd82c46fe6ecb153660a6a151c7159fa94bd4638b3f`

## First NoopTracer item

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

Evidence SHA256: `2b91b968be73a34aca5690cc269142e5204210cbd1fb1823644b9304db7ac2a0`

```json
{"body_bytes":1112,"body_chars":1112,"body_sha256":"cca1354fa44e399622bfafd82c46fe6ecb153660a6a151c7159fa94bd4638b3f","classification_count_this_gate":1,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","first_item":{"binding":null,"body_end_reached":false,"boundary_kind":"STATEMENT_SEMICOLON","dependencies":[],"dependency_count":0,"end":12,"kind":"DIRECTIVE","source":"\"use strict\"","source_sha256":"4ee188e1744c19816e95a540b2650ed9f033ea0371e74eac8e717355cfca8741","start":0,"structural_prefix_end":0,"structural_prefix_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","structural_prefix_start":0},"first_item_sha256":"43b8310632d9e5dddff2af160c67a6ceb883b25f18a36abb3ddcbe91e9ecbc45","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/NoopTracer.js","next_additional_item_classified":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","otel_frontier_end":467,"provider_frontier_end":153,"proxy_tracer_frontier_end":159,"proxy_tracer_frontier_resume_authorized":false,"qualification_contract_sha256":"d6086688636e5df8afbd1cff66f979a18f9f16abd923cfd25339a7cc438182b8","qualification_evidence_sha256":"c9b16fbf2e26896543313831985618b616169119c23ad346c3a9e446049a9513","record_end":26480,"record_sha256":"21e7c05873488b19e50b3069dfc3540fe4cbf007549b238b8ea5c98d87b0c445","record_start":25246,"source_executed":false,"trace_api_frontier_end":285,"trace_api_frontier_resume_authorized":false,"version":"GATE4_NOOP_TRACER_FIRST_STATIC_ITEM_V1"}
```

## Strict boundary

This gate performs only the authorized static read of the uniquely identified NoopTracer.js webpack module record and classifies exactly its first eligible item. No second NoopTracer.js item is classified. Any dependency is identified only from the frozen first-item text and no dependency source is opened. NoopTracer.js completion is not claimed. No return to ProxyTracer.js is attempted. ProxyTracer.js remains frozen at offset 159. ProxyTracerProvider.js remains frozen at offset 153. trace-api.js remains frozen at offset 285. OTEL remains frozen at offset 467. No source is executed, the frozen authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
