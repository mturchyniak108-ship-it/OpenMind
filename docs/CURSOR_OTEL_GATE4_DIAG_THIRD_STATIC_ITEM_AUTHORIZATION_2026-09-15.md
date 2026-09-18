# Cursor OTEL Gate-4 diag.js third static item authorization

Date: 2026-09-15

## Status

- Audit status: PASS
- Authorization status: `AUTHORIZED_THIRD_STATIC_ITEM_ONLY`
- Authorized item count: 1
- Fourth item authorized: NO
- Source execution authorized: NO
- OTEL authority mutation authorized: NO

## Frozen second-row boundary

- Second-item document SHA256: `9acdab3bd62c5b5c3474ccb701c0ca03e8b0103baf1905157800be7ce650542d`
- Second-item evidence SHA256: `8fbc488a4fe9ce6688215997ea2ca013ce38c6c205effb36f4ac2557ac32003b`
- Second-row SHA256: `0f5b078bd89f25b456890011fbcac23a7502f9560d7db606dea916b2b45525da`
- Second-row terminator: 29

## Authorization contract

- Contract SHA256: `ec455b776334bbd44588455bbda9c1f0e496beb0fd7003435a176aacb80180ea`

```json
{"authority_mutation_authorized":false,"authorized_item_count":1,"body_chars":3461,"body_sha256":"7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195","bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_mode":"NEXT_STATIC_ITEM_WITH_DECLARATOR_SPLIT","execution_authorized":false,"fourth_item_authorized":false,"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","module_record_sha256":"b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8","next_item_ordinal":3,"resume_after_terminator":29,"second_item_document_sha256":"9acdab3bd62c5b5c3474ccb701c0ca03e8b0103baf1905157800be7ce650542d","second_item_evidence_sha256":"8fbc488a4fe9ce6688215997ea2ca013ce38c6c205effb36f4ac2557ac32003b","second_row_sha256":"0f5b078bd89f25b456890011fbcac23a7502f9560d7db606dea916b2b45525da","version":"GATE4_DIAG_THIRD_STATIC_ITEM_AUTHORIZATION_CONTRACT_V1"}
```

## Authorization evidence

Evidence SHA256: `b4f01215f6794e09d2a2e79a9b9a45b6347615188140ef6fbfb0ac9242abc0d6`

```json
{"authorization_status":"AUTHORIZED_THIRD_STATIC_ITEM_ONLY","authorized_item_count":1,"contract":{"authority_mutation_authorized":false,"authorized_item_count":1,"body_chars":3461,"body_sha256":"7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195","bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_mode":"NEXT_STATIC_ITEM_WITH_DECLARATOR_SPLIT","execution_authorized":false,"fourth_item_authorized":false,"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","module_record_sha256":"b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8","next_item_ordinal":3,"resume_after_terminator":29,"second_item_document_sha256":"9acdab3bd62c5b5c3474ccb701c0ca03e8b0103baf1905157800be7ce650542d","second_item_evidence_sha256":"8fbc488a4fe9ce6688215997ea2ca013ce38c6c205effb36f4ac2557ac32003b","second_row_sha256":"0f5b078bd89f25b456890011fbcac23a7502f9560d7db606dea916b2b45525da","version":"GATE4_DIAG_THIRD_STATIC_ITEM_AUTHORIZATION_CONTRACT_V1"},"contract_sha256":"ec455b776334bbd44588455bbda9c1f0e496beb0fd7003435a176aacb80180ea","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","diag_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","second_item_evidence_sha256":"8fbc488a4fe9ce6688215997ea2ca013ce38c6c205effb36f4ac2557ac32003b","second_row_sha256":"0f5b078bd89f25b456890011fbcac23a7502f9560d7db606dea916b2b45525da","source_execution_authorized":false,"version":"GATE4_DIAG_THIRD_STATIC_ITEM_AUTHORIZATION_V1"}
```

## Strict boundary

Only the next diag.js static item after the frozen second-row terminator may be classified. If the next statement is a var, let, or const declaration, only its first declarator is authorized. No fourth item is authorized.
