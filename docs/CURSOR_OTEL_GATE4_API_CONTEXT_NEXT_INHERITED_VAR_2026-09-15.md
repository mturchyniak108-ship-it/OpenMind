# Cursor OTEL Gate-4 api context next inherited var

Date: 2026-09-15

## Status

- Audit status: PASS
- Static items classified this gate: 1
- Additional item classified: NO
- Completed diag source reread: NO
- Source executed: NO
- OTEL authority mutated: NO

## Classified item

- Sequence role: `NEXT_AFTER_POST_DIAG_CONTEXT_BINDING_A`
- Kind: `STATIC_BINDING`
- Boundary kind: `DECLARATOR_COMMA`
- Declaration prefix: `var`
- Binding: `l`
- Dependency module: `None`
- Initializer present: `True`
- Body offsets: 1208:1215
- Terminator offset: 1215
- Source SHA256: `70c9a99297f6a03f7d6c6fc218f25378cd6ebb682d48b3434f4ac9096bc6c0da`
- Canonical row SHA256: `0b96fb7f6596f33758dc5b6d2b4c20d5e4e9c77e727428ebe51efd97566888c0`
- Source: `l=new s`

## Classification evidence

Evidence SHA256: `e3c3980bb9c07bc648d9ed58cffdf574e4200efca028ad72a084de19eb7b9263`

```json
{"authorization_commit":"da0763e45cbf307eb1de9ffcf1b851be026ac7f5","authorization_contract_sha256":"0d76d7101c3872870cf755dfc32b765734529f53cf9088d16496a259fe7e0e28","authorization_document_sha256":"de28a09be285ace96d5ca544d5c33179724ee01e995ff16f250a9573bbf54ed6","authorization_evidence_sha256":"bdeae72f78f5dcea7212ff6c92f231fd40a5114278a88f310a76d2992ef60f1e","body_chars":2365,"body_end_reached":false,"body_sha256":"d8a3982b67173a9152b5b610028a5dad7eb9f459a3f31432e0624f89592da17e","classification_count_this_gate":1,"completed_diag_source_reread":false,"completed_diag_state_sha256":"d1c86b38caf273d343e95d5198da380ec66fbdbee2add54d4cac8305c91df0e9","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","module_record_sha256":"e5ab0daa3dc7bed29eda2ce170e726bc6875586094dbe16a8eccf7b4a85834f7","next_additional_item_classified":false,"next_item":{"binding":"l","body_end_reached":false,"boundary_kind":"DECLARATOR_COMMA","declaration_prefix":"var","dependency_module":null,"end":1215,"initializer_present":true,"kind":"STATIC_BINDING","sequence_role":"NEXT_AFTER_POST_DIAG_CONTEXT_BINDING_A","source":"l=new s","source_sha256":"70c9a99297f6a03f7d6c6fc218f25378cd6ebb682d48b3434f4ac9096bc6c0da","start":1208,"terminator":1215},"next_item_sha256":"0b96fb7f6596f33758dc5b6d2b4c20d5e4e9c77e727428ebe51efd97566888c0","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","previous_row_sha256":"3dfb28d511a1b398124d5e5f1eecc6ae8ce2f63050481255cbe7d1e566c164a4","source_executed":false,"version":"GATE4_API_CONTEXT_NEXT_INHERITED_VAR_V1"}
```

## Strict boundary

Exactly one inherited var declarator after frozen comma offset 1207 was classified. No additional api/context item was recovered or classified. Completed diag source was not reread. No JavaScript was executed and the OTEL authority was not mutated.
