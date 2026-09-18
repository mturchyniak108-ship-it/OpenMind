# Cursor OTEL Gate-4 diag types third static item authorization

Date: 2026-09-15

## Status

- Audit status: PASS
- Authorization status: `AUTHORIZED_THIRD_STATIC_ITEM_ONLY`
- Authorized item count: 1
- Fourth item authorized: NO
- Source execution authorized: NO
- OTEL authority mutation authorized: NO

## Frozen corrected row-2 boundary

- Correction document SHA256: `aa7c384442416816a5f6a2a72900d159e216bf24874db87757285ba27dc23276`
- Correction evidence SHA256: `7baee73c2220626d62ab35537e7d1a16ab24a36cd92847c95e280eb50c809941`
- Corrected row-2 SHA256: `785be8e5ff07510fdbe85eeaa0d3b6d36aa7bfe02643cc23eb14f0c6cbc3593c`
- Corrected row kind: `STATIC_BINDING`
- Corrected row binding: `r`
- Corrected row terminator: 18
- Resume offset: 19

## Authorization contract

- Contract SHA256: `bca89a05031664ed58aaee78b72cf500483aa12154e673097f846d091b0e1573`

```json
{"authority_mutation_authorized":false,"authorized_item_count":1,"body_chars":208,"body_sha256":"659fc768c54e343ad1e4c74982b0774bdc59272f00b32be2617ef1428d03048f","bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_mode":"THIRD_TOP_LEVEL_STATIC_ITEM_ONLY","corrected_row2_sha256":"785be8e5ff07510fdbe85eeaa0d3b6d36aa7bfe02643cc23eb14f0c6cbc3593c","correction_document_sha256":"aa7c384442416816a5f6a2a72900d159e216bf24874db87757285ba27dc23276","correction_evidence_sha256":"7baee73c2220626d62ab35537e7d1a16ab24a36cd92847c95e280eb50c809941","fourth_item_authorized":false,"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","module_record_sha256":"08b2da2b398b0c8a6d09c6852ee8c49b9416fa7322f256c288ff07a795580059","next_item_ordinal":3,"resume_offset":19,"source_execution_authorized":false,"version":"GATE4_DIAG_TYPES_THIRD_STATIC_ITEM_AUTHORIZATION_CONTRACT_V1"}
```

## Authorization evidence

Evidence SHA256: `2cc4f113081f3aed7c354521b88d119eb535c1261ecec0dc92b4ff51208ccb13`

```json
{"authorization_status":"AUTHORIZED_THIRD_STATIC_ITEM_ONLY","authorized_item_count":1,"contract":{"authority_mutation_authorized":false,"authorized_item_count":1,"body_chars":208,"body_sha256":"659fc768c54e343ad1e4c74982b0774bdc59272f00b32be2617ef1428d03048f","bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_mode":"THIRD_TOP_LEVEL_STATIC_ITEM_ONLY","corrected_row2_sha256":"785be8e5ff07510fdbe85eeaa0d3b6d36aa7bfe02643cc23eb14f0c6cbc3593c","correction_document_sha256":"aa7c384442416816a5f6a2a72900d159e216bf24874db87757285ba27dc23276","correction_evidence_sha256":"7baee73c2220626d62ab35537e7d1a16ab24a36cd92847c95e280eb50c809941","fourth_item_authorized":false,"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","module_record_sha256":"08b2da2b398b0c8a6d09c6852ee8c49b9416fa7322f256c288ff07a795580059","next_item_ordinal":3,"resume_offset":19,"source_execution_authorized":false,"version":"GATE4_DIAG_TYPES_THIRD_STATIC_ITEM_AUTHORIZATION_CONTRACT_V1"},"contract_sha256":"bca89a05031664ed58aaee78b72cf500483aa12154e673097f846d091b0e1573","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","source_execution_authorized":false,"version":"GATE4_DIAG_TYPES_THIRD_STATIC_ITEM_AUTHORIZATION_V1"}
```

## Strict boundary

Only the third static item after corrected row 2 may be classified. No fourth item is authorized. No parent diag.js advancement, JavaScript execution, OTEL authority mutation, Gate 5 evaluation, Cursor execution, or Git push is authorized.
