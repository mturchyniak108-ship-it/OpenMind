# Cursor OTEL Gate-4 diag.js sixth static item authorization

Date: 2026-09-15

## Status

- Audit status: PASS
- Authorization status: `AUTHORIZED_SIXTH_STATIC_ITEM_ONLY`
- Authorized item count: 1
- Seventh item authorized: NO
- Function declaration boundary recognition: YES
- Class declaration boundary recognition: YES
- Multi-declarator split: FIRST DECLARATOR ONLY
- Source execution authorized: NO
- OTEL authority mutation authorized: NO

## Frozen fifth-row boundary

- Fifth-item document SHA256: `10945fcabbaf7c5842cd94e4186e50cfea863d3035a7e344541d1dfcc0136cf6`
- Fifth-item evidence SHA256: `abb46e2b28d72d98ba950f144c54ca2a5c581106d09b1a1adc72133b51fd5f9b`
- Fifth-row SHA256: `fd068697d93b453865dfbd2d1baf118774804a93c8e46640bac8798ac7f63283`
- Fifth-row end: 1430
- Fifth-row closing-brace offset: 1429

## Authorization contract

- Contract SHA256: `5603508f2941afeb3dad601c6e2f1527be494e0b5788140d4430dadd0cc72b07`

```json
{"authority_mutation_authorized":false,"authorized_item_count":1,"body_chars":3461,"body_sha256":"7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195","bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_mode":"NEXT_TOP_LEVEL_STATIC_ITEM_DECLARATION_AWARE","completed_dependency_reuse_evidence_sha256":"a950f49835eefb7f0b106a836b23d314b514e0aebb1c1cdb98a2bc759d1626b8","execution_authorized":false,"fifth_item_document_sha256":"10945fcabbaf7c5842cd94e4186e50cfea863d3035a7e344541d1dfcc0136cf6","fifth_item_evidence_sha256":"abb46e2b28d72d98ba950f144c54ca2a5c581106d09b1a1adc72133b51fd5f9b","fifth_row_sha256":"fd068697d93b453865dfbd2d1baf118774804a93c8e46640bac8798ac7f63283","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","module_record_sha256":"b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8","next_item_ordinal":6,"resume_offset":1430,"seventh_item_authorized":false,"version":"GATE4_DIAG_SIXTH_STATIC_ITEM_AUTHORIZATION_CONTRACT_V1"}
```

## Authorization evidence

Evidence SHA256: `1e8e4c00de15d8c52852e1d5b39b7ba9dfa3099e7d0620625b97db29f2b7f38f`

```json
{"authorization_status":"AUTHORIZED_SIXTH_STATIC_ITEM_ONLY","authorized_item_count":1,"contract":{"authority_mutation_authorized":false,"authorized_item_count":1,"body_chars":3461,"body_sha256":"7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195","bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_mode":"NEXT_TOP_LEVEL_STATIC_ITEM_DECLARATION_AWARE","completed_dependency_reuse_evidence_sha256":"a950f49835eefb7f0b106a836b23d314b514e0aebb1c1cdb98a2bc759d1626b8","execution_authorized":false,"fifth_item_document_sha256":"10945fcabbaf7c5842cd94e4186e50cfea863d3035a7e344541d1dfcc0136cf6","fifth_item_evidence_sha256":"abb46e2b28d72d98ba950f144c54ca2a5c581106d09b1a1adc72133b51fd5f9b","fifth_row_sha256":"fd068697d93b453865dfbd2d1baf118774804a93c8e46640bac8798ac7f63283","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","module_record_sha256":"b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8","next_item_ordinal":6,"resume_offset":1430,"seventh_item_authorized":false,"version":"GATE4_DIAG_SIXTH_STATIC_ITEM_AUTHORIZATION_CONTRACT_V1"},"contract_sha256":"5603508f2941afeb3dad601c6e2f1527be494e0b5788140d4430dadd0cc72b07","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","diag_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","fifth_item_evidence_sha256":"abb46e2b28d72d98ba950f144c54ca2a5c581106d09b1a1adc72133b51fd5f9b","fifth_row_sha256":"fd068697d93b453865dfbd2d1baf118774804a93c8e46640bac8798ac7f63283","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","source_execution_authorized":false,"version":"GATE4_DIAG_SIXTH_STATIC_ITEM_AUTHORIZATION_V1"}
```

## Strict boundary

Only the next diag.js top-level static item beginning at or after body offset 1430 may be classified. Function and class declarations are bounded structurally. For a var, let, or const declaration only its first declarator is authorized. No seventh item is authorized.
