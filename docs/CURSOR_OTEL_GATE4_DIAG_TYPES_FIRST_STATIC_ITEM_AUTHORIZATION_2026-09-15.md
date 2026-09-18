# Cursor OTEL Gate-4 diag types first static item authorization

Date: 2026-09-15

## Status

- Audit status: PASS
- Authorization status: `AUTHORIZED_FIRST_STATIC_ITEM_ONLY`
- Authorized item count: 1
- Second item authorized: NO
- Source execution authorized: NO
- OTEL authority mutation authorized: NO

## Frozen measured identity

- Measurement document SHA256: `bb715323c93a8ee6929f94cb1930e3d690adcafe62ea7318d82964d358eee5f5`
- Measurement evidence SHA256: `cc4ddad6295ebbf87f482643650ad2b7462889e2f0f88ca14ef971b29379b346`
- Module record SHA256: `08b2da2b398b0c8a6d09c6852ee8c49b9416fa7322f256c288ff07a795580059`
- Body chars: 208
- Body SHA256: `659fc768c54e343ad1e4c74982b0774bdc59272f00b32be2617ef1428d03048f`
- Body range: 10819:11027

## Authorization contract

- Contract SHA256: `a1c4acc5ed1b3859cf7d3fc856b09fb88e602a7ad77e4307b35a3c180ec730fd`

```json
{"authority_mutation_authorized":false,"authorized_item_count":1,"body_chars":208,"body_end":11027,"body_sha256":"659fc768c54e343ad1e4c74982b0774bdc59272f00b32be2617ef1428d03048f","body_start":10819,"bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_mode":"FIRST_TOP_LEVEL_STATIC_ITEM_ONLY","measurement_document_sha256":"bb715323c93a8ee6929f94cb1930e3d690adcafe62ea7318d82964d358eee5f5","measurement_evidence_sha256":"cc4ddad6295ebbf87f482643650ad2b7462889e2f0f88ca14ef971b29379b346","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","module_record_end":11028,"module_record_sha256":"08b2da2b398b0c8a6d09c6852ee8c49b9416fa7322f256c288ff07a795580059","module_record_start":10704,"next_item_ordinal":1,"second_item_authorized":false,"source_execution_authorized":false,"version":"GATE4_DIAG_TYPES_FIRST_STATIC_ITEM_AUTHORIZATION_CONTRACT_V1"}
```

## Authorization evidence

Evidence SHA256: `0bdbd38db0a0edde2018f3c2ba16fb0c243ae792b33e3a5d3941dcf0124d2e2f`

```json
{"authorization_status":"AUTHORIZED_FIRST_STATIC_ITEM_ONLY","authorized_item_count":1,"contract":{"authority_mutation_authorized":false,"authorized_item_count":1,"body_chars":208,"body_end":11027,"body_sha256":"659fc768c54e343ad1e4c74982b0774bdc59272f00b32be2617ef1428d03048f","body_start":10819,"bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_mode":"FIRST_TOP_LEVEL_STATIC_ITEM_ONLY","measurement_document_sha256":"bb715323c93a8ee6929f94cb1930e3d690adcafe62ea7318d82964d358eee5f5","measurement_evidence_sha256":"cc4ddad6295ebbf87f482643650ad2b7462889e2f0f88ca14ef971b29379b346","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","module_record_end":11028,"module_record_sha256":"08b2da2b398b0c8a6d09c6852ee8c49b9416fa7322f256c288ff07a795580059","module_record_start":10704,"next_item_ordinal":1,"second_item_authorized":false,"source_execution_authorized":false,"version":"GATE4_DIAG_TYPES_FIRST_STATIC_ITEM_AUTHORIZATION_CONTRACT_V1"},"contract_sha256":"a1c4acc5ed1b3859cf7d3fc856b09fb88e602a7ad77e4307b35a3c180ec730fd","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","source_execution_authorized":false,"version":"GATE4_DIAG_TYPES_FIRST_STATIC_ITEM_AUTHORIZATION_V1"}
```

## Strict boundary

Only the first top-level static item in the frozen types.js body may be classified after this authorization commits. No second item is authorized. No JavaScript execution, parent diag.js advancement, OTEL authority mutation, Gate 5 evaluation, Cursor execution, or Git push is authorized.
