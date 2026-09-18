# Cursor OTEL Gate-4 NoopTracer next static item

Date: 2026-09-15

## Status

- Classification status: PASS
- Module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/NoopTracer.js`
- Previous item span: 0:12
- Resume semicolon span: 12:13
- Exactly one additional child item classified: YES
- Further child item classified: NO
- ProxyTracer frontier remains: 159
- ProxyTracerProvider frontier remains: 153
- trace-api frontier remains: 285
- OTEL frontier remains: 467

## Next NoopTracer item

- Span: 13:29
- Kind: `WEBPACK_EXPORT_GETTER_INSTALLATION`
- Binding: `NONE`
- Source SHA256: `76c7f9b90682c42fb1eec565c6ff127ba9cfbb2790dc13a6bf7f80f0202153de`
- Row SHA256: `b30e3a725779f3948f935abb0984cc4e42a641676d90a88d85e6593186aed2c5`
- Boundary: `STATEMENT_SEMICOLON`
- Body end reached: NO
- Dependency count: 0
- Dependency modules: `[]`

## Classification evidence

Evidence SHA256: `3ed2ece604bb2a867cf5db41956c7b63d087f0d5786499c5b802ce466a0b034d`

```json
{"body_chars":1112,"body_sha256":"cca1354fa44e399622bfafd82c46fe6ecb153660a6a151c7159fa94bd4638b3f","classification_count_this_gate":1,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/NoopTracer.js","next_additional_item_classified":false,"next_item":{"binding":null,"body_end_reached":false,"boundary_kind":"STATEMENT_SEMICOLON","dependencies":[],"dependency_count":0,"end":29,"kind":"WEBPACK_EXPORT_GETTER_INSTALLATION","source":"n.d(t,{o:()=>l})","source_sha256":"76c7f9b90682c42fb1eec565c6ff127ba9cfbb2790dc13a6bf7f80f0202153de","start":13,"structural_prefix_end":13,"structural_prefix_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","structural_prefix_start":13},"next_item_sha256":"b30e3a725779f3948f935abb0984cc4e42a641676d90a88d85e6593186aed2c5","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","otel_frontier_end":467,"previous_item_end":12,"previous_item_evidence_sha256":"2b91b968be73a34aca5690cc269142e5204210cbd1fb1823644b9304db7ac2a0","previous_item_row_sha256":"43b8310632d9e5dddff2af160c67a6ceb883b25f18a36abb3ddcbe91e9ecbc45","provider_frontier_end":153,"proxy_tracer_frontier_end":159,"proxy_tracer_frontier_resume_authorized":false,"record_sha256":"21e7c05873488b19e50b3069dfc3540fe4cbf007549b238b8ea5c98d87b0c445","resume_delimiter":";","resume_delimiter_end":13,"resume_delimiter_start":12,"source_executed":false,"trace_api_frontier_end":285,"trace_api_frontier_resume_authorized":false,"version":"GATE4_NOOP_TRACER_NEXT_STATIC_ITEM_V1"}
```

## Strict boundary

This gate advances exactly one NoopTracer.js item after the first-item semicolon at 12:13. No third NoopTracer.js item is classified. Any dependency is identified only from the frozen item text and no dependency source is opened. NoopTracer.js completion is not claimed. No return to ProxyTracer.js is attempted. ProxyTracer.js remains frozen at offset 159. ProxyTracerProvider.js remains frozen at offset 153. trace-api.js remains frozen at offset 285. OTEL remains frozen at offset 467. No source is executed, the frozen authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
