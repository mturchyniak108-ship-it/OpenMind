# Cursor OTEL Gate-4 api context next static item after diag authorization

Date: 2026-09-15

## Status

- Audit status: PASS
- Authorization status: `AUTHORIZED_ONE_POST_DIAG_CONTEXT_ITEM_ONLY`
- Authorized item count: 1
- Additional item authorized: NO
- Inherited declaration prefix: `var`
- Completed diag source reread authorized: NO
- Source execution authorized: NO
- OTEL authority mutation authorized: NO

## Frozen parent-return frontier

- Parent-return document SHA256: `831182f351eddcb4249fd25bfdd0ac8659a38502def5bbf1a51a4131370d79e6`
- Parent-return evidence SHA256: `2350f8a8a66dee809417cb2feea00d848cf62628be1984d995dc3a6ccecbe900`
- Boundary adjudication SHA256: `80bb77606d2724b2e59fcfebdd920c89705e3cec29281fda66da8394d73bf9c2`
- Completed diag state SHA256: `d1c86b38caf273d343e95d5198da380ec66fbdbee2add54d4cac8305c91df0e9`
- Frozen resume offset: 1196

## Authorization contract

- Contract SHA256: `25233691ac0dc83158535be8f4595d5562440e04a302e300a4d64577f9deede5`

```json
{"authority_mutation_authorized":false,"authorized_item_count":1,"body_chars":2365,"body_sha256":"d8a3982b67173a9152b5b610028a5dad7eb9f459a3f31432e0624f89592da17e","bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_mode":"NEXT_INHERITED_VAR_DECLARATOR_ONLY","completed_diag_source_reread_authorized":false,"completed_diag_state_sha256":"d1c86b38caf273d343e95d5198da380ec66fbdbee2add54d4cac8305c91df0e9","inherited_declaration_prefix":"var","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","module_record_sha256":"e5ab0daa3dc7bed29eda2ce170e726bc6875586094dbe16a8eccf7b4a85834f7","next_additional_item_authorized":false,"parent_return_document_sha256":"831182f351eddcb4249fd25bfdd0ac8659a38502def5bbf1a51a4131370d79e6","parent_return_evidence_sha256":"2350f8a8a66dee809417cb2feea00d848cf62628be1984d995dc3a6ccecbe900","resume_offset":1196,"source_execution_authorized":false,"version":"GATE4_API_CONTEXT_POST_DIAG_NEXT_STATIC_ITEM_AUTHORIZATION_CONTRACT_V1"}
```

## Authorization evidence

Evidence SHA256: `c75b3ff4941dd1313dd78f67a5b4b19a59c1227368d605414dbef457e0a70eb7`

```json
{"authorization_status":"AUTHORIZED_ONE_POST_DIAG_CONTEXT_ITEM_ONLY","authorized_item_count":1,"contract":{"authority_mutation_authorized":false,"authorized_item_count":1,"body_chars":2365,"body_sha256":"d8a3982b67173a9152b5b610028a5dad7eb9f459a3f31432e0624f89592da17e","bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_mode":"NEXT_INHERITED_VAR_DECLARATOR_ONLY","completed_diag_source_reread_authorized":false,"completed_diag_state_sha256":"d1c86b38caf273d343e95d5198da380ec66fbdbee2add54d4cac8305c91df0e9","inherited_declaration_prefix":"var","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","module_record_sha256":"e5ab0daa3dc7bed29eda2ce170e726bc6875586094dbe16a8eccf7b4a85834f7","next_additional_item_authorized":false,"parent_return_document_sha256":"831182f351eddcb4249fd25bfdd0ac8659a38502def5bbf1a51a4131370d79e6","parent_return_evidence_sha256":"2350f8a8a66dee809417cb2feea00d848cf62628be1984d995dc3a6ccecbe900","resume_offset":1196,"source_execution_authorized":false,"version":"GATE4_API_CONTEXT_POST_DIAG_NEXT_STATIC_ITEM_AUTHORIZATION_CONTRACT_V1"},"contract_sha256":"25233691ac0dc83158535be8f4595d5562440e04a302e300a4d64577f9deede5","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","source_execution_authorized":false,"version":"GATE4_API_CONTEXT_POST_DIAG_NEXT_STATIC_ITEM_AUTHORIZATION_V1"}
```

## Strict boundary

Only one inherited var declarator beginning at frozen api/context resume offset 1196 may be classified. No additional parent item is authorized. Completed diag source must not be reread. No JavaScript execution, OTEL authority mutation, Gate 5 evaluation, Cursor execution, or Git push is authorized.
