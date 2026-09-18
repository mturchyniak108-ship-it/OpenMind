# Cursor OTEL Gate-4 diag seventh static item authorization

Date: 2026-09-15

## Status

- Audit status: PASS
- Authorization status: `AUTHORIZED_SEVENTH_STATIC_ITEM_ONLY`
- Authorized item count: 1
- Eighth item authorized: NO
- Inherited declaration prefix: `var`
- Child source reread authorized: NO
- Source execution authorized: NO
- OTEL authority mutation authorized: NO

## Frozen parent-return frontier

- Parent-return document SHA256: `20f136fc9f2759630db550f6ea7c4a522c55ebf27b3c3fa39d794114ee81368b`
- Parent-return evidence SHA256: `8bafae01711d8a12c5ecf0c276dbef6a31c48ecf739e2f4e4493ac196e05a373`
- Parent row-6 SHA256: `94a35d9d4773eb333ec435b0ea231cb2f9372ec9675f75e555da7a41c33ddf04`
- Completed child state SHA256: `33bf91f35c636521e2cf73072c2970094b86adf7d784b5ef67a6d51b9ea61a23`
- Resume offset: 1547

## Authorization contract

- Contract SHA256: `9bdbd82780febd834c630343dc8cbefde7e5999fef4b0cfdd36dfe57c67798d6`

```json
{"authority_mutation_authorized":false,"authorized_item_count":1,"body_chars":3461,"body_sha256":"7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195","bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","child_completed_state_sha256":"33bf91f35c636521e2cf73072c2970094b86adf7d784b5ef67a6d51b9ea61a23","child_source_reread_authorized":false,"classification_mode":"NEXT_INHERITED_VAR_DECLARATOR_ONLY","eighth_item_authorized":false,"inherited_declaration_prefix":"var","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","module_record_sha256":"b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8","next_item_ordinal":7,"parent_return_document_sha256":"20f136fc9f2759630db550f6ea7c4a522c55ebf27b3c3fa39d794114ee81368b","parent_return_evidence_sha256":"8bafae01711d8a12c5ecf0c276dbef6a31c48ecf739e2f4e4493ac196e05a373","resume_offset":1547,"row6_sha256":"94a35d9d4773eb333ec435b0ea231cb2f9372ec9675f75e555da7a41c33ddf04","source_execution_authorized":false,"version":"GATE4_DIAG_SEVENTH_STATIC_ITEM_AUTHORIZATION_CONTRACT_V1"}
```

## Authorization evidence

Evidence SHA256: `a0877f3c0aaf9e7b1523f6f436e960984f832bde37ac0962c5959e1bac0bee2f`

```json
{"authorization_status":"AUTHORIZED_SEVENTH_STATIC_ITEM_ONLY","authorized_item_count":1,"contract":{"authority_mutation_authorized":false,"authorized_item_count":1,"body_chars":3461,"body_sha256":"7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195","bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","child_completed_state_sha256":"33bf91f35c636521e2cf73072c2970094b86adf7d784b5ef67a6d51b9ea61a23","child_source_reread_authorized":false,"classification_mode":"NEXT_INHERITED_VAR_DECLARATOR_ONLY","eighth_item_authorized":false,"inherited_declaration_prefix":"var","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","module_record_sha256":"b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8","next_item_ordinal":7,"parent_return_document_sha256":"20f136fc9f2759630db550f6ea7c4a522c55ebf27b3c3fa39d794114ee81368b","parent_return_evidence_sha256":"8bafae01711d8a12c5ecf0c276dbef6a31c48ecf739e2f4e4493ac196e05a373","resume_offset":1547,"row6_sha256":"94a35d9d4773eb333ec435b0ea231cb2f9372ec9675f75e555da7a41c33ddf04","source_execution_authorized":false,"version":"GATE4_DIAG_SEVENTH_STATIC_ITEM_AUTHORIZATION_CONTRACT_V1"},"contract_sha256":"9bdbd82780febd834c630343dc8cbefde7e5999fef4b0cfdd36dfe57c67798d6","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","source_execution_authorized":false,"version":"GATE4_DIAG_SEVENTH_STATIC_ITEM_AUTHORIZATION_V1"}
```

## Strict boundary

Only one inherited var declarator beginning at or after parent resume offset 1547 may be classified. The completed diag/types.js child source must not be reread. No eighth parent item is authorized. No source execution, OTEL authority mutation, Gate 5 evaluation, Cursor execution, or Git push is authorized.
