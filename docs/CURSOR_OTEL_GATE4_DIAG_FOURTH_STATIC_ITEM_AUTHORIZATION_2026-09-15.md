# Cursor OTEL Gate-4 diag.js fourth static item authorization

Date: 2026-09-15

## Status

- Audit status: PASS
- Authorization status: `AUTHORIZED_FOURTH_STATIC_ITEM_ONLY`
- Authorized item count: 1
- Fifth item authorized: NO
- Global-utils source reread authorized: NO
- Source execution authorized: NO
- OTEL authority mutation authorized: NO

## Completed dependency prerequisite

- Global-utils reuse document SHA256: `abcb2a53154dce25b8e8821fef0a950a4214a67ec0f5eb8c746565a305907763`
- Global-utils reuse contract SHA256: `a493f7db7dab5b287e11d750663a0d126e51e3de7fa7fce42cb784a4911ed617`
- Global-utils reuse evidence SHA256: `a950f49835eefb7f0b106a836b23d314b514e0aebb1c1cdb98a2bc759d1626b8`
- Completed dependency state SHA256: `f4b8f19271c054b83809afc2908a394a4d33457988d2cef6c54e4013a3b3a929`
- Resume offset: 158

## Authorization contract

- Contract SHA256: `fc9d64d7818f61515aff374c331f843522834fe51db7a894e36645e720c818c8`

```json
{"authority_mutation_authorized":false,"authorized_item_count":1,"body_chars":3461,"body_sha256":"7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195","bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_mode":"NEXT_DECLARATOR_ONLY","completed_dependency_reuse_evidence_sha256":"a950f49835eefb7f0b106a836b23d314b514e0aebb1c1cdb98a2bc759d1626b8","completed_dependency_state_sha256":"f4b8f19271c054b83809afc2908a394a4d33457988d2cef6c54e4013a3b3a929","execution_authorized":false,"fifth_item_authorized":false,"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","module_record_sha256":"b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8","next_item_ordinal":4,"resume_offset":158,"source_reread_of_completed_dependency_authorized":false,"version":"GATE4_DIAG_FOURTH_STATIC_ITEM_AUTHORIZATION_CONTRACT_V1"}
```

## Authorization evidence

Evidence SHA256: `8ebc4e5186bc525fe70ebbe8f6ad45883629b1809bef823af53391f80901b5a7`

```json
{"authorization_status":"AUTHORIZED_FOURTH_STATIC_ITEM_ONLY","authorized_item_count":1,"completed_dependency_reuse_evidence_sha256":"a950f49835eefb7f0b106a836b23d314b514e0aebb1c1cdb98a2bc759d1626b8","contract":{"authority_mutation_authorized":false,"authorized_item_count":1,"body_chars":3461,"body_sha256":"7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195","bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_mode":"NEXT_DECLARATOR_ONLY","completed_dependency_reuse_evidence_sha256":"a950f49835eefb7f0b106a836b23d314b514e0aebb1c1cdb98a2bc759d1626b8","completed_dependency_state_sha256":"f4b8f19271c054b83809afc2908a394a4d33457988d2cef6c54e4013a3b3a929","execution_authorized":false,"fifth_item_authorized":false,"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","module_record_sha256":"b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8","next_item_ordinal":4,"resume_offset":158,"source_reread_of_completed_dependency_authorized":false,"version":"GATE4_DIAG_FOURTH_STATIC_ITEM_AUTHORIZATION_CONTRACT_V1"},"contract_sha256":"fc9d64d7818f61515aff374c331f843522834fe51db7a894e36645e720c818c8","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","diag_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","resume_offset":158,"source_execution_authorized":false,"version":"GATE4_DIAG_FOURTH_STATIC_ITEM_AUTHORIZATION_V1"}
```

## Strict boundary

Only one declarator beginning after the completed global-utils dependency boundary may be classified. No fifth item is authorized. The completed global-utils source may not be reread.
