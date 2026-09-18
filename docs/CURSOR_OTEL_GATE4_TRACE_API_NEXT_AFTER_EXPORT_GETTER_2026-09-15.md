# Cursor OTEL Gate-4 trace-api item after export getter

Date: 2026-09-15

## Status

- Classification status: PASS
- Module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace-api.js`
- Exactly one additional child item classified: YES
- Further child item classified: NO
- OTEL frontier remains: 467

## Previous qualified frontier

- Previous item span: 13:29
- Previous row SHA256: `8f121e40a9b4106fbded1dd432f4df1b4a9b82e3cc8a5932713ed61b11c0ae15`
- Previous evidence SHA256: `0a88d496e9fbf6f4f36616485de63d3d3a65e8ad2a1397847c17d060bc7b2549`
- Resume semicolon span: 29:30

## Newly classified item

- Declaration prefix: `var`
- Item span: 34:157
- Kind: `STATIC_BINDING`
- Binding: `r`
- Source SHA256: `34199cab9401f5023274f51372433f3101e365698bd55552834b76e0cd47d186`
- Row SHA256: `3559e28d982c391c3104ca8bfe0f12341f43be78aa25bb9b9962cb836b4879bf`
- Boundary: `DECLARATOR_COMMA`
- Body end reached: NO
- Dependency count: 1
- Dependency modules: `["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js"]`

## Classification evidence

Evidence SHA256: `4c877e5b220c359876fba5df0ef577d52f69039d7a4457dccfc5ebc028420a49`

```json
{"body_chars":1438,"body_sha256":"982a41f22fcda8f4c1d9d7dac0e3cde663429cd6b5a0ac43fd9be3a3fd3a628b","classification_count_this_gate":1,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace-api.js","next_additional_item_classified":false,"next_item":{"binding":"r","body_end_reached":false,"boundary_kind":"DECLARATOR_COMMA","declaration_prefix":"var","declaration_prefix_end":34,"declaration_prefix_sha256":"092090833731ec177e11c0f921ac9e0592e13aa6b6fcb5ad751246ee46fe8014","declaration_prefix_start":30,"dependencies":[{"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js","relative_end":123,"relative_start":2,"source":"n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js\")","source_sha256":"3d93510314abe17bdaa031d4fc4c07e192f84be5b93e8b6779e30f6520778925"}],"dependency_count":1,"end":157,"kind":"STATIC_BINDING","source":"r=n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js\")","source_sha256":"34199cab9401f5023274f51372433f3101e365698bd55552834b76e0cd47d186","start":34,"whitespace_prefix_end":30,"whitespace_prefix_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","whitespace_prefix_start":30},"next_item_sha256":"3559e28d982c391c3104ca8bfe0f12341f43be78aa25bb9b9962cb836b4879bf","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","otel_frontier_end":467,"otel_frontier_resume_authorized":false,"previous_item_end":29,"previous_item_evidence_sha256":"0a88d496e9fbf6f4f36616485de63d3d3a65e8ad2a1397847c17d060bc7b2549","previous_item_row_sha256":"8f121e40a9b4106fbded1dd432f4df1b4a9b82e3cc8a5932713ed61b11c0ae15","record_sha256":"f0e1a4dbd5a7fcf1566c5fb0eec17a03aa4fd443ea98053ec6bbc23265492223","resume_delimiter":";","resume_delimiter_end":30,"resume_delimiter_start":29,"source_executed":false,"version":"GATE4_TRACE_API_NEXT_AFTER_EXPORT_GETTER_V1"}
```

## Strict boundary

This gate advances exactly one trace-api.js item after the qualified export-getter semicolon. A leading var declaration prefix is treated only as structural syntax and at most one declarator is classified. Any dependency is identified only from the frozen item text and no dependency source is opened. No later child item is classified. trace-api.js completion is not claimed. No return to OTEL is attempted. OTEL remains frozen at offset 467. No source is executed, the frozen authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
