# Cursor OTEL Gate-4 diag types second static item semantic correction

Date: 2026-09-15

## Status

- Audit status: PASS
- Correction scope: row 2 semantic classification only
- Source reread: NO
- Third item authorized: NO
- Third item classified: NO
- Parent diag.js advanced: NO
- Source executed: NO
- OTEL authority mutated: NO

## Frozen original row

- Second-item document SHA256: `eb81a1526271e2adb160a3f845cdaae31162f58aafbb4e39078702b36921858c`
- Second-item evidence SHA256: `2e7c64280e0f67b55646d7f7efaf4846ff3902aff887d0ea8179022a0d78cb24`
- Old canonical row SHA256: `061094429421f79b8cff6e29c2a99b73a120bd352d5afaa8ceed93996fe0cfd3`
- Declaration prefix: `var`
- Source: `r`
- Source SHA256: `454349e422f05297191ead13e21d3db520e5abef52055e4964b82fb213f593a1`
- Body offsets: 17:18
- Terminator offset: 18
- Old kind: `STATIC_EXPRESSION`
- Old binding: `None`

## Corrected semantics

- Corrected kind: `STATIC_BINDING`
- Corrected binding: `r`
- Initializer present: NO
- Corrected canonical row SHA256: `785be8e5ff07510fdbe85eeaa0d3b6d36aa7bfe02643cc23eb14f0c6cbc3593c`
- Reason: `VAR_DECLARATOR_WITHOUT_INITIALIZER_CREATES_STATIC_BINDING`

## Semantic contract

- Contract SHA256: `9586a240233e625ea8a1ba0047dda38e659718ed9dd3ef04f3e0f0249667f89b`

```json
{"corrected_binding":"r","corrected_kind":"STATIC_BINDING","initializer_present":false,"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","old_binding":null,"old_kind":"STATIC_EXPRESSION","old_row_sha256":"061094429421f79b8cff6e29c2a99b73a120bd352d5afaa8ceed93996fe0cfd3","parent_advancement_authorized":false,"row_ordinal":2,"source_execution_authorized":false,"source_reread_authorized":false,"third_item_authorized":false,"version":"GATE4_DIAG_TYPES_SECOND_STATIC_ITEM_SEMANTIC_CORRECTION_CONTRACT_V1"}
```

## Correction evidence

Evidence SHA256: `7baee73c2220626d62ab35537e7d1a16ab24a36cd92847c95e280eb50c809941`

```json
{"body_sha256":"659fc768c54e343ad1e4c74982b0774bdc59272f00b32be2617ef1428d03048f","corrected_row":{"binding":"r","body_end_reached":false,"boundary_kind":"DECLARATION_STATEMENT_END","declaration_prefix":"var","dependency_module":null,"end":18,"initializer_present":false,"kind":"STATIC_BINDING","ordinal":2,"source":"r","source_sha256":"454349e422f05297191ead13e21d3db520e5abef52055e4964b82fb213f593a1","start":17,"terminator":18},"corrected_row_sha256":"785be8e5ff07510fdbe85eeaa0d3b6d36aa7bfe02643cc23eb14f0c6cbc3593c","correction_reason":"VAR_DECLARATOR_WITHOUT_INITIALIZER_CREATES_STATIC_BINDING","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","module_record_sha256":"08b2da2b398b0c8a6d09c6852ee8c49b9416fa7322f256c288ff07a795580059","old_row_sha256":"061094429421f79b8cff6e29c2a99b73a120bd352d5afaa8ceed93996fe0cfd3","second_item_document_sha256":"eb81a1526271e2adb160a3f845cdaae31162f58aafbb4e39078702b36921858c","second_item_evidence_sha256":"2e7c64280e0f67b55646d7f7efaf4846ff3902aff887d0ea8179022a0d78cb24","semantic_contract":{"corrected_binding":"r","corrected_kind":"STATIC_BINDING","initializer_present":false,"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","old_binding":null,"old_kind":"STATIC_EXPRESSION","old_row_sha256":"061094429421f79b8cff6e29c2a99b73a120bd352d5afaa8ceed93996fe0cfd3","parent_advancement_authorized":false,"row_ordinal":2,"source_execution_authorized":false,"source_reread_authorized":false,"third_item_authorized":false,"version":"GATE4_DIAG_TYPES_SECOND_STATIC_ITEM_SEMANTIC_CORRECTION_CONTRACT_V1"},"semantic_contract_sha256":"9586a240233e625ea8a1ba0047dda38e659718ed9dd3ef04f3e0f0249667f89b","source_execution_performed":false,"source_read_performed":false,"third_item_classified":false,"version":"GATE4_DIAG_TYPES_SECOND_STATIC_ITEM_SEMANTIC_CORRECTION_V1"}
```

## Strict boundary

This correction supersedes only the semantic kind and binding fields of frozen types.js row 2. The source bytes, source SHA256, body offsets, declaration prefix, statement boundary, terminator, module identity, and parent frontier remain unchanged. No third item is authorized or classified.
