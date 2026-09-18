# Cursor OTEL Gate-4 trace-api resume after global-utils

Date: 2026-09-15

## Status

- Classification status: PASS
- Module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace-api.js`
- Closed dependency state SHA256: `f4b8f19271c054b83809afc2908a394a4d33457988d2cef6c54e4013a3b3a929`
- Previous item span: 34:157
- Resume comma span: 157:158
- Exactly one resumed item classified: YES
- Further child item classified: NO
- OTEL frontier remains: 467

## Resumed trace-api item

- Span: 158:285
- Kind: `STATIC_BINDING`
- Binding: `s`
- Source SHA256: `5079d29ed90b3e574ca041417d7e747dd119d58e5a343f912fe5a2cfb4ac2cd3`
- Row SHA256: `11875e5b0710b761165a15d6f1e364e2398d351da447c60e598c81674c9816ab`
- Boundary: `DECLARATOR_COMMA`
- Body end reached: NO
- Dependency count: 1
- Dependency modules: `["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracerProvider.js"]`

## Resume evidence

Evidence SHA256: `055c0b34ab678f8ddabb94651c6ecd05cb2fc93877712f31ee9b298cd59abc1c`

```json
{"body_chars":1438,"body_sha256":"982a41f22fcda8f4c1d9d7dac0e3cde663429cd6b5a0ac43fd9be3a3fd3a628b","classification_count_this_gate":1,"closed_dependency_state_sha256":"f4b8f19271c054b83809afc2908a394a4d33457988d2cef6c54e4013a3b3a929","closure_contract_sha256":"e684e1e62ac7570b20d42b8b30049f60ea54a32c10faac72cc0983eb990030f7","closure_evidence_sha256":"7a6edb901f39bca0128b2f76aaf714b55de4e04f73d135834a8d103480c58219","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace-api.js","next_additional_item_classified":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","otel_frontier_end":467,"otel_frontier_resume_authorized":false,"previous_item_end":157,"previous_item_evidence_sha256":"4c877e5b220c359876fba5df0ef577d52f69039d7a4457dccfc5ebc028420a49","previous_item_row_sha256":"3559e28d982c391c3104ca8bfe0f12341f43be78aa25bb9b9962cb836b4879bf","record_sha256":"f0e1a4dbd5a7fcf1566c5fb0eec17a03aa4fd443ea98053ec6bbc23265492223","resume_delimiter":",","resume_delimiter_end":158,"resume_delimiter_start":157,"resumed_item":{"binding":"s","body_end_reached":false,"boundary_kind":"DECLARATOR_COMMA","dependencies":[{"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracerProvider.js","relative_end":127,"relative_start":2,"source":"n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracerProvider.js\")","source_sha256":"5bc87e6f38ec7113d674186f752d7760093a788261dd58ec6cd49c2155897784"}],"dependency_count":1,"end":285,"kind":"STATIC_BINDING","source":"s=n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracerProvider.js\")","source_sha256":"5079d29ed90b3e574ca041417d7e747dd119d58e5a343f912fe5a2cfb4ac2cd3","start":158,"whitespace_prefix_end":158,"whitespace_prefix_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","whitespace_prefix_start":158},"resumed_item_sha256":"11875e5b0710b761165a15d6f1e364e2398d351da447c60e598c81674c9816ab","source_executed":false,"version":"GATE4_TRACE_API_RESUME_AFTER_GLOBAL_UTILS_V1"}
```

## Strict boundary

This gate resumes trace-api.js only after the previously closed global-utils.js dependency and the exact declarator comma at 157:158. Exactly one next child item is classified. No later child item is classified. Any newly reported dependency is identified only from the already frozen item text and its source is not opened. trace-api.js completion is not claimed. No parent return is attempted. OTEL remains frozen at offset 467. No source is executed, the frozen authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
