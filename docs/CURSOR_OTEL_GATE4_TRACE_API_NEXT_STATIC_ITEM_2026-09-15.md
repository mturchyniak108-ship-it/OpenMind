# Cursor OTEL Gate-4 trace-api next static item

Date: 2026-09-15

## Status

- Classification status: PASS
- Module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace-api.js`
- Exactly one additional child item classified: YES
- Further child item classified: NO
- OTEL frontier remains: 467

## Previous child frontier

- Previous item span: 0:12
- Previous row SHA256: `43b8310632d9e5dddff2af160c67a6ceb883b25f18a36abb3ddcbe91e9ecbc45`
- Previous evidence SHA256: `68fbe7b55fdb8307dccd37852f5a3693a396857ccd28cef379ac8b4f0a4e313b`
- Semicolon boundary span: 12:13

## Next child item

- Span: 13:29
- Kind: `WEBPACK_EXPORT_GETTER_INSTALLATION`
- Binding: `NONE`
- Source SHA256: `82961e30493fad8213f6b50e5fb82c3cccffba645b46dcb195b457c897d668df`
- Row SHA256: `8f121e40a9b4106fbded1dd432f4df1b4a9b82e3cc8a5932713ed61b11c0ae15`
- Boundary: `STATEMENT_SEMICOLON`
- Body end reached: NO
- Dependency count: 0
- Dependency modules: `[]`

## Classification evidence

Evidence SHA256: `0a88d496e9fbf6f4f36616485de63d3d3a65e8ad2a1397847c17d060bc7b2549`

```json
{"body_chars":1438,"body_sha256":"982a41f22fcda8f4c1d9d7dac0e3cde663429cd6b5a0ac43fd9be3a3fd3a628b","classification_count_this_gate":1,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace-api.js","next_additional_item_classified":false,"next_item":{"binding":null,"body_end_reached":false,"boundary_kind":"STATEMENT_SEMICOLON","dependencies":[],"dependency_count":0,"end":29,"kind":"WEBPACK_EXPORT_GETTER_INSTALLATION","source":"n.d(t,{u:()=>u})","source_sha256":"82961e30493fad8213f6b50e5fb82c3cccffba645b46dcb195b457c897d668df","start":13,"structural_prefix_end":13,"structural_prefix_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","structural_prefix_start":13},"next_item_sha256":"8f121e40a9b4106fbded1dd432f4df1b4a9b82e3cc8a5932713ed61b11c0ae15","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","otel_frontier_end":467,"otel_frontier_resume_authorized":false,"previous_item_end":12,"previous_item_evidence_sha256":"68fbe7b55fdb8307dccd37852f5a3693a396857ccd28cef379ac8b4f0a4e313b","previous_item_row_sha256":"43b8310632d9e5dddff2af160c67a6ceb883b25f18a36abb3ddcbe91e9ecbc45","record_sha256":"f0e1a4dbd5a7fcf1566c5fb0eec17a03aa4fd443ea98053ec6bbc23265492223","source_executed":false,"version":"GATE4_TRACE_API_NEXT_STATIC_ITEM_V1"}
```

## Strict boundary

This gate advances exactly one trace-api.js item after the qualified first-item semicolon. No third child item is classified. Any dependency is identified only from the frozen item text and no dependency source is opened. trace-api.js completion is not claimed. No return to OTEL is attempted. OTEL remains frozen at offset 467. No source is executed, the frozen authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
