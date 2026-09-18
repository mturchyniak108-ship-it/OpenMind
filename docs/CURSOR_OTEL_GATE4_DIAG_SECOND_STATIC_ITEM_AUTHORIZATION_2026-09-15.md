# Cursor OTEL Gate-4 diag.js second static item authorization

Date: 2026-09-15

## Status

- Audit status: PASS
- Authorization status: `AUTHORIZED_SECOND_STATIC_ITEM_ONLY`
- Authorized item count: 1
- Third item authorized: NO
- Source execution authorized: NO
- OTEL authority mutation authorized: NO

## Frozen first-row boundary

- First-item document SHA256: `d830bbe3648569c6da249a141acf703ef8ad74223d7f73556d700673065f3561`
- First-item evidence SHA256: `83ad31f6d99024d3c0efcd7677d52db6ef0bf65c172c6b0babdc4ea4c28ef56f`
- First-row SHA256: `9b88aea1a1e6c5bf6e311b75c23ae1b3e9abe23eaffbe23ead0171ab1d14fe7a`
- First-row terminator: 12

## Authorization contract

- Contract SHA256: `91157757c99be8ad7f5dce7da2c044e3ea1cd8d80a468b1c0726279a1a54ece3`

```json
{"authority_mutation_authorized":false,"authorized_item_count":1,"body_chars":3461,"body_sha256":"7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195","bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_mode":"NEXT_TOP_LEVEL_STATIC_ITEM_ONLY","execution_authorized":false,"first_item_document_sha256":"d830bbe3648569c6da249a141acf703ef8ad74223d7f73556d700673065f3561","first_item_evidence_sha256":"83ad31f6d99024d3c0efcd7677d52db6ef0bf65c172c6b0babdc4ea4c28ef56f","first_row_sha256":"9b88aea1a1e6c5bf6e311b75c23ae1b3e9abe23eaffbe23ead0171ab1d14fe7a","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","module_record_sha256":"b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8","next_item_ordinal":2,"resume_after_terminator":12,"third_item_authorized":false,"version":"GATE4_DIAG_SECOND_STATIC_ITEM_AUTHORIZATION_CONTRACT_V1"}
```

## Authorization evidence

Evidence SHA256: `f4f53e13b1d5ae4743f5c0c0648e4e136c3867828109a0eec9f96b800c59e664`

```json
{"authorization_status":"AUTHORIZED_SECOND_STATIC_ITEM_ONLY","authorized_item_count":1,"contract":{"authority_mutation_authorized":false,"authorized_item_count":1,"body_chars":3461,"body_sha256":"7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195","bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_mode":"NEXT_TOP_LEVEL_STATIC_ITEM_ONLY","execution_authorized":false,"first_item_document_sha256":"d830bbe3648569c6da249a141acf703ef8ad74223d7f73556d700673065f3561","first_item_evidence_sha256":"83ad31f6d99024d3c0efcd7677d52db6ef0bf65c172c6b0babdc4ea4c28ef56f","first_row_sha256":"9b88aea1a1e6c5bf6e311b75c23ae1b3e9abe23eaffbe23ead0171ab1d14fe7a","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","module_record_sha256":"b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8","next_item_ordinal":2,"resume_after_terminator":12,"third_item_authorized":false,"version":"GATE4_DIAG_SECOND_STATIC_ITEM_AUTHORIZATION_CONTRACT_V1"},"contract_sha256":"91157757c99be8ad7f5dce7da2c044e3ea1cd8d80a468b1c0726279a1a54ece3","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","diag_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","first_item_evidence_sha256":"83ad31f6d99024d3c0efcd7677d52db6ef0bf65c172c6b0babdc4ea4c28ef56f","first_row_sha256":"9b88aea1a1e6c5bf6e311b75c23ae1b3e9abe23eaffbe23ead0171ab1d14fe7a","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","source_execution_authorized":false,"version":"GATE4_DIAG_SECOND_STATIC_ITEM_AUTHORIZATION_V1"}
```

## Strict boundary

Only the next top-level diag.js item after the frozen first-row terminator may be classified. No third item is authorized.
