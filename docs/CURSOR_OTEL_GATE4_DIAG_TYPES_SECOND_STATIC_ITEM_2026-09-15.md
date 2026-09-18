# Cursor OTEL Gate-4 diag types second static item

Date: 2026-09-15

## Status

- Audit status: PASS
- Static items classified this gate: 1
- Cumulative frozen rows: 2
- Body end reached: NO
- Third item classified: NO
- Source executed: NO
- Parent diag.js advanced: NO
- OTEL authority mutated: NO

## Second static item

- Kind: `STATIC_EXPRESSION`
- Boundary kind: `DECLARATION_STATEMENT_END`
- Declaration prefix: `var`
- Binding: `None`
- Dependency module: `None`
- Body offsets: 17:18
- Terminator offset: 18
- Source SHA256: `454349e422f05297191ead13e21d3db520e5abef52055e4964b82fb213f593a1`
- Canonical row SHA256: `061094429421f79b8cff6e29c2a99b73a120bd352d5afaa8ceed93996fe0cfd3`
- Source: `r`

## Evidence

Evidence SHA256: `2e7c64280e0f67b55646d7f7efaf4846ff3902aff887d0ea8179022a0d78cb24`

```json
{"authorization_commit":"21395ead3910735f48fa417fc37e9f5d44f539a6","authorization_contract_sha256":"76c8158017560d99f0ee3a62f67c06c96f09baf0a9b06c0619768304e5e7e4c4","authorization_document_sha256":"626407c8a516668572b2290f65de0ccb3d04be0f6876de70f5d3122b39585556","authorization_evidence_sha256":"59a4ebe64225604466c2ad8322db075c0d08c4b0c7286d03e6de1f9d7457f6c1","body_chars":208,"body_end_reached":false,"body_sha256":"659fc768c54e343ad1e4c74982b0774bdc59272f00b32be2617ef1428d03048f","classification_count_this_gate":1,"cumulative_classified_rows":2,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","first_row_sha256":"a6241f0094281c7e5b2289f418f8076a04d8163949c113c901cbda59968f8621","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","module_record_sha256":"08b2da2b398b0c8a6d09c6852ee8c49b9416fa7322f256c288ff07a795580059","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","second_item":{"binding":null,"body_end_reached":false,"boundary_kind":"DECLARATION_STATEMENT_END","declaration_prefix":"var","dependency_module":null,"end":18,"kind":"STATIC_EXPRESSION","ordinal":2,"source":"r","source_sha256":"454349e422f05297191ead13e21d3db520e5abef52055e4964b82fb213f593a1","start":17,"terminator":18},"second_item_sha256":"061094429421f79b8cff6e29c2a99b73a120bd352d5afaa8ceed93996fe0cfd3","source_executed":false,"third_item_classified":false,"version":"GATE4_DIAG_TYPES_SECOND_STATIC_ITEM_V1"}
```

## Strict boundary

Exactly one second static item from the frozen types.js body was classified. A multi-declarator declaration was limited to its first declarator. No third item was recovered or classified. No JavaScript was executed. The parent diag.js frontier and OTEL authority were not advanced or mutated.
