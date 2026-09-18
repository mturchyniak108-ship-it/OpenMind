# Cursor OTEL Gate-4 diag.js fifth static item authorization

Date: 2026-09-15

## Status

- Audit status: PASS
- Authorization status: `AUTHORIZED_FIFTH_STATIC_ITEM_ONLY`
- Authorized item count: 1
- Sixth item authorized: NO
- Function declaration boundary recognition: YES
- Class declaration boundary recognition: YES
- Multi-declarator split: FIRST DECLARATOR ONLY
- Source execution authorized: NO
- OTEL authority mutation authorized: NO

## Frozen fourth-row boundary

- Fourth-item document SHA256: `0e458abdf5cd152d08aa1bc89570c8988c0ca9663caf71769ea5e29a948fef7e`
- Fourth-item evidence SHA256: `8d3d098732846e07bebb33a28a703e5dde3298c09094e95c2ced82200463bc81`
- Fourth-row SHA256: `0949c21d737be5745db462ee8c322405eb516b078daa6277afdca5e7b7d72a8d`
- Fourth-row terminator: 867

## Authorization contract

- Contract SHA256: `e9ee8cbddd413427e6b8cd53b60b0fa50ac2cb2b0eeecaee5a6d4f79e02a4fec`

```json
{"authority_mutation_authorized":false,"authorized_item_count":1,"body_chars":3461,"body_sha256":"7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195","bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_mode":"NEXT_TOP_LEVEL_STATIC_ITEM_DECLARATION_AWARE","completed_dependency_reuse_evidence_sha256":"a950f49835eefb7f0b106a836b23d314b514e0aebb1c1cdb98a2bc759d1626b8","execution_authorized":false,"fourth_item_document_sha256":"0e458abdf5cd152d08aa1bc89570c8988c0ca9663caf71769ea5e29a948fef7e","fourth_item_evidence_sha256":"8d3d098732846e07bebb33a28a703e5dde3298c09094e95c2ced82200463bc81","fourth_row_sha256":"0949c21d737be5745db462ee8c322405eb516b078daa6277afdca5e7b7d72a8d","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","module_record_sha256":"b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8","next_item_ordinal":5,"resume_after_terminator":867,"sixth_item_authorized":false,"version":"GATE4_DIAG_FIFTH_STATIC_ITEM_AUTHORIZATION_CONTRACT_V1"}
```

## Authorization evidence

Evidence SHA256: `cc195cac85bcd690d358b01462898e7c13408a2715b1438ef816a8c9a9dcd5d4`

```json
{"authorization_status":"AUTHORIZED_FIFTH_STATIC_ITEM_ONLY","authorized_item_count":1,"contract":{"authority_mutation_authorized":false,"authorized_item_count":1,"body_chars":3461,"body_sha256":"7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195","bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_mode":"NEXT_TOP_LEVEL_STATIC_ITEM_DECLARATION_AWARE","completed_dependency_reuse_evidence_sha256":"a950f49835eefb7f0b106a836b23d314b514e0aebb1c1cdb98a2bc759d1626b8","execution_authorized":false,"fourth_item_document_sha256":"0e458abdf5cd152d08aa1bc89570c8988c0ca9663caf71769ea5e29a948fef7e","fourth_item_evidence_sha256":"8d3d098732846e07bebb33a28a703e5dde3298c09094e95c2ced82200463bc81","fourth_row_sha256":"0949c21d737be5745db462ee8c322405eb516b078daa6277afdca5e7b7d72a8d","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","module_record_sha256":"b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8","next_item_ordinal":5,"resume_after_terminator":867,"sixth_item_authorized":false,"version":"GATE4_DIAG_FIFTH_STATIC_ITEM_AUTHORIZATION_CONTRACT_V1"},"contract_sha256":"e9ee8cbddd413427e6b8cd53b60b0fa50ac2cb2b0eeecaee5a6d4f79e02a4fec","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","diag_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","fourth_item_evidence_sha256":"8d3d098732846e07bebb33a28a703e5dde3298c09094e95c2ced82200463bc81","fourth_row_sha256":"0949c21d737be5745db462ee8c322405eb516b078daa6277afdca5e7b7d72a8d","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","source_execution_authorized":false,"version":"GATE4_DIAG_FIFTH_STATIC_ITEM_AUTHORIZATION_V1"}
```

## Strict boundary

Only the next diag.js top-level static item after the frozen fourth-row boundary may be classified. A function or class declaration ends at its structural closing brace even when no semicolon follows. For a var, let, or const declaration only its first declarator is authorized. No sixth item is authorized.
