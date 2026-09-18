# Cursor OTEL Gate-4 diag types second static item authorization

Date: 2026-09-15

## Status

- Audit status: PASS
- Authorization status: `AUTHORIZED_SECOND_STATIC_ITEM_ONLY`
- Authorized item count: 1
- Third item authorized: NO
- Source execution authorized: NO
- OTEL authority mutation authorized: NO

## Frozen first-row boundary

- First-item document SHA256: `50a221d8603add75d103ea08b0e3c312d38d9a53f9af68513719731d50be67d9`
- First-item evidence SHA256: `56a0781ba77df3d2969c926cdb237398fb3e1119ad52c5f0ba4a242891114dee`
- First-row SHA256: `a6241f0094281c7e5b2289f418f8076a04d8163949c113c901cbda59968f8621`
- First-row terminator: 12
- Resume offset: 13

## Frozen module identity

- Module record SHA256: `08b2da2b398b0c8a6d09c6852ee8c49b9416fa7322f256c288ff07a795580059`
- Body chars: 208
- Body SHA256: `659fc768c54e343ad1e4c74982b0774bdc59272f00b32be2617ef1428d03048f`

## Authorization contract

- Contract SHA256: `76c8158017560d99f0ee3a62f67c06c96f09baf0a9b06c0619768304e5e7e4c4`

```json
{"authority_mutation_authorized":false,"authorized_item_count":1,"body_chars":208,"body_sha256":"659fc768c54e343ad1e4c74982b0774bdc59272f00b32be2617ef1428d03048f","bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_mode":"SECOND_TOP_LEVEL_STATIC_ITEM_ONLY","first_item_document_sha256":"50a221d8603add75d103ea08b0e3c312d38d9a53f9af68513719731d50be67d9","first_item_evidence_sha256":"56a0781ba77df3d2969c926cdb237398fb3e1119ad52c5f0ba4a242891114dee","first_row_sha256":"a6241f0094281c7e5b2289f418f8076a04d8163949c113c901cbda59968f8621","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","module_record_sha256":"08b2da2b398b0c8a6d09c6852ee8c49b9416fa7322f256c288ff07a795580059","next_item_ordinal":2,"resume_offset":13,"source_execution_authorized":false,"third_item_authorized":false,"version":"GATE4_DIAG_TYPES_SECOND_STATIC_ITEM_AUTHORIZATION_CONTRACT_V1"}
```

## Authorization evidence

Evidence SHA256: `59a4ebe64225604466c2ad8322db075c0d08c4b0c7286d03e6de1f9d7457f6c1`

```json
{"authorization_status":"AUTHORIZED_SECOND_STATIC_ITEM_ONLY","authorized_item_count":1,"contract":{"authority_mutation_authorized":false,"authorized_item_count":1,"body_chars":208,"body_sha256":"659fc768c54e343ad1e4c74982b0774bdc59272f00b32be2617ef1428d03048f","bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_mode":"SECOND_TOP_LEVEL_STATIC_ITEM_ONLY","first_item_document_sha256":"50a221d8603add75d103ea08b0e3c312d38d9a53f9af68513719731d50be67d9","first_item_evidence_sha256":"56a0781ba77df3d2969c926cdb237398fb3e1119ad52c5f0ba4a242891114dee","first_row_sha256":"a6241f0094281c7e5b2289f418f8076a04d8163949c113c901cbda59968f8621","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","module_record_sha256":"08b2da2b398b0c8a6d09c6852ee8c49b9416fa7322f256c288ff07a795580059","next_item_ordinal":2,"resume_offset":13,"source_execution_authorized":false,"third_item_authorized":false,"version":"GATE4_DIAG_TYPES_SECOND_STATIC_ITEM_AUTHORIZATION_CONTRACT_V1"},"contract_sha256":"76c8158017560d99f0ee3a62f67c06c96f09baf0a9b06c0619768304e5e7e4c4","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","source_execution_authorized":false,"version":"GATE4_DIAG_TYPES_SECOND_STATIC_ITEM_AUTHORIZATION_V1"}
```

## Strict boundary

Only the second top-level static item after the frozen first-row terminator may be classified. A variable declaration may expose only its first declarator. No third item is authorized. No JavaScript execution, parent diag.js advancement, OTEL authority mutation, Gate 5 evaluation, Cursor execution, or Git push is authorized.
