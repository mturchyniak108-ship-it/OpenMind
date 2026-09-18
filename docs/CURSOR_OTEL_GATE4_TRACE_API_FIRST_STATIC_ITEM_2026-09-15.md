# Cursor OTEL Gate-4 trace-api first static item

Date: 2026-09-15

## Status

- Classification status: PASS
- Child module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace-api.js`
- Exactly one child item classified: YES
- Additional child item classified: NO
- OTEL frontier remains: 467
- Source executed: NO

## Authorized module record

- Record start: 22802
- Record end: 24355
- Record SHA256: `f0e1a4dbd5a7fcf1566c5fb0eec17a03aa4fd443ea98053ec6bbc23265492223`
- Body bytes: 1438
- Body chars: 1438
- Body SHA256: `982a41f22fcda8f4c1d9d7dac0e3cde663429cd6b5a0ac43fd9be3a3fd3a628b`

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

Evidence SHA256: `68fbe7b55fdb8307dccd37852f5a3693a396857ccd28cef379ac8b4f0a4e313b`

```json
{"authorization_contract_sha256":"8a88007399072f20d22737c92883f0ac406c984aab5b437b8dd480c00a8e609a","authorization_evidence_sha256":"4285725708d641cbbdbb498dc18bb8bf4a25a0843d14f3b8b05771417f2278c5","body_bytes":1438,"body_chars":1438,"body_sha256":"982a41f22fcda8f4c1d9d7dac0e3cde663429cd6b5a0ac43fd9be3a3fd3a628b","classification_count_this_gate":1,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","first_item":{"binding":null,"body_end_reached":false,"boundary_kind":"STATEMENT_SEMICOLON","dependencies":[],"dependency_count":0,"end":12,"kind":"DIRECTIVE","source":"\"use strict\"","source_sha256":"4ee188e1744c19816e95a540b2650ed9f033ea0371e74eac8e717355cfca8741","start":0,"structural_prefix_end":0,"structural_prefix_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","structural_prefix_start":0},"first_item_sha256":"43b8310632d9e5dddff2af160c67a6ceb883b25f18a36abb3ddcbe91e9ecbc45","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace-api.js","next_additional_item_classified":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","otel_frontier_end":467,"otel_frontier_resume_authorized":false,"record_end":24355,"record_sha256":"f0e1a4dbd5a7fcf1566c5fb0eec17a03aa4fd443ea98053ec6bbc23265492223","record_start":22802,"source_executed":false,"version":"GATE4_TRACE_API_FIRST_STATIC_ITEM_V1"}
```

## Strict boundary

This gate performs the previously authorized static read of the uniquely identified trace-api.js webpack module record and classifies exactly its first eligible item. No second child item is classified. Any dependency named by the first item is identified only from the already-read item text; no dependency source is opened. trace-api.js module completion is not claimed unless a later completion gate proves full coverage. The OTEL parent remains frozen at offset 467. No JavaScript is executed, the frozen authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
