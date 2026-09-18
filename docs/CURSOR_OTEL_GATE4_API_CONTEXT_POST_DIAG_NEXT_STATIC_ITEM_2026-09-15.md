# Cursor OTEL Gate-4 api context next static item after diag

Date: 2026-09-15

## Status

- Audit status: PASS
- Static items classified this gate: 1
- Additional item classified: NO
- Completed diag source reread: NO
- Source executed: NO
- OTEL authority mutated: NO

## Classified item

- Sequence role: `NEXT_AFTER_COMPLETED_DIAG_DEPENDENCY`
- Kind: `STATIC_BINDING`
- Boundary kind: `DECLARATOR_COMMA`
- Declaration prefix: `var`
- Binding: `a`
- Dependency module: `None`
- Initializer present: `True`
- Body offsets: 1196:1207
- Terminator offset: 1207
- Source SHA256: `e816bf11336bc27780afb432552294337b06fa8df9f5d1e434179a149ce3fde2`
- Canonical row SHA256: `3dfb28d511a1b398124d5e5f1eecc6ae8ce2f63050481255cbe7d1e566c164a4`
- Source: `a="context"`

## Completed diag prerequisite

- Completed diag state SHA256: `d1c86b38caf273d343e95d5198da380ec66fbdbee2add54d4cac8305c91df0e9`
- Completed diag source reread: NO

## Classification evidence

Evidence SHA256: `3c92ea6b811fa1d916e06520399d1667c5e9bf41214e4e45887bd23817eaac2d`

```json
{"authorization_commit":"86c99948d6ae999e7914741e468e58d3a879237f","authorization_contract_sha256":"25233691ac0dc83158535be8f4595d5562440e04a302e300a4d64577f9deede5","authorization_document_sha256":"8973b4acd29dbef1f51ea5b049d57ac83b7cfbe24b746c5e2af736eb2915733d","authorization_evidence_sha256":"c75b3ff4941dd1313dd78f67a5b4b19a59c1227368d605414dbef457e0a70eb7","body_chars":2365,"body_end_reached":false,"body_sha256":"d8a3982b67173a9152b5b610028a5dad7eb9f459a3f31432e0624f89592da17e","classification_count_this_gate":1,"completed_diag_source_reread":false,"completed_diag_state_sha256":"d1c86b38caf273d343e95d5198da380ec66fbdbee2add54d4cac8305c91df0e9","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","module_record_sha256":"e5ab0daa3dc7bed29eda2ce170e726bc6875586094dbe16a8eccf7b4a85834f7","next_additional_item_classified":false,"next_item":{"binding":"a","body_end_reached":false,"boundary_kind":"DECLARATOR_COMMA","declaration_prefix":"var","dependency_module":null,"end":1207,"initializer_present":true,"kind":"STATIC_BINDING","sequence_role":"NEXT_AFTER_COMPLETED_DIAG_DEPENDENCY","source":"a=\"context\"","source_sha256":"e816bf11336bc27780afb432552294337b06fa8df9f5d1e434179a149ce3fde2","start":1196,"terminator":1207},"next_item_sha256":"3dfb28d511a1b398124d5e5f1eecc6ae8ce2f63050481255cbe7d1e566c164a4","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","source_executed":false,"version":"GATE4_API_CONTEXT_POST_DIAG_NEXT_STATIC_ITEM_V1"}
```

## Strict boundary

Exactly one inherited var declarator after the completed diag dependency was classified. No additional api/context item was recovered or classified. Completed diag source was not reread. No JavaScript was executed and the OTEL authority was not mutated.
