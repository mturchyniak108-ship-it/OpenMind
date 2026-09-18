# Cursor OTEL Gate-4 OTEL parent next static item

Date: 2026-09-15

## Status

- Classification status: PASS
- Module: `../context/dist/otel.js`
- Exactly one additional item classified: YES
- Further item classified: NO
- Source executed: NO

## Previous qualified frontier

- Previous item span: 242:355
- Previous row SHA256: `3b78888df470ad30fa9c7d9584153cf09d376b41d1969459d2313069d6c06e83`
- Previous resume evidence SHA256: `5c3b89a6088b350e03bedf0cbb1c5f7903d7cb0485978d995ba685f93670f2f9`
- Resume delimiter span: 355:356

## Next classified item

- Span: 356:467
- Kind: `STATIC_BINDING_WITH_DEPENDENCY`
- Source SHA256: `277bcc0dcea4ee3b78cb4b71a45d61813cc68d3b2d3b56a97ac665fecc2e37cc`
- Row SHA256: `fd9eabde66e18c81d70d2dd21881d89079111e9087c00291d8f8d27b931173ca`
- Boundary: `DECLARATOR_COMMA`
- Body end reached: NO
- Dependency count: 1
- Dependency modules: `["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace-api.js"]`

## Classification evidence

Evidence SHA256: `50ac22df28a39411db6de7069b0ebb5b76c6cb55ae4c1be2187a5ccea6c6f34f`

```json
{"body_chars":2607,"body_sha256":"0475d054c3ecdefffcc7f90efe9e757e3078514760baffcd0ed872e6b8452a45","classification_count_this_gate":1,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","module":"../context/dist/otel.js","next_additional_item_classified":false,"next_item":{"binding":"i","body_end_reached":false,"boundary_kind":"DECLARATOR_COMMA","dependencies":[{"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace-api.js","relative_end":111,"relative_start":2,"source":"n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace-api.js\")","source_sha256":"fe33f0b54d04d5c178bb72aafa347e53010aad25237c2ed24d7d6c182cb89331"}],"dependency_count":1,"end":467,"initializer_present":true,"kind":"STATIC_BINDING_WITH_DEPENDENCY","source":"i=n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace-api.js\")","source_sha256":"277bcc0dcea4ee3b78cb4b71a45d61813cc68d3b2d3b56a97ac665fecc2e37cc","start":356,"structural_prefix_end":356,"structural_prefix_sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","structural_prefix_start":356},"next_item_sha256":"fd9eabde66e18c81d70d2dd21881d89079111e9087c00291d8f8d27b931173ca","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","parent_state_sha256":"138d9a73153af3f7d606022cc7e1b537a4e87c0d0656303854f24627f0c05c6a","previous_item_end":355,"previous_item_row_sha256":"3b78888df470ad30fa9c7d9584153cf09d376b41d1969459d2313069d6c06e83","previous_resume_evidence_sha256":"5c3b89a6088b350e03bedf0cbb1c5f7903d7cb0485978d995ba685f93670f2f9","resume_delimiter":",","resume_delimiter_end":356,"resume_delimiter_start":355,"source_executed":false,"version":"GATE4_OTEL_PARENT_NEXT_STATIC_ITEM_V1"}
```

## Strict boundary

This gate advances exactly one OTEL item after the previously qualified declarator comma. Any dependency discovered in this item is classified only by module identity and source span; no dependency source is opened or executed in this gate. No later OTEL item is classified. OTEL module completion is not claimed. No parent return is attempted. The frozen authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
