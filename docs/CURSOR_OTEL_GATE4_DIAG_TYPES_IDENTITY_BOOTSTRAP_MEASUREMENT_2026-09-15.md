# Cursor OTEL Gate-4 diag types identity-bootstrap measurement

Date: 2026-09-15

## Status

- Audit status: PASS
- Read mode: `IDENTITY_BOOTSTRAP_MEASUREMENT_ONLY`
- Module body read: YES, identity measurement only
- Statement splitting performed: NO
- Static statements classified: 0
- Source executed: NO
- Parent diag.js advanced: NO
- OTEL authority mutated: NO

## Frozen authorization

- Authorization document SHA256: `1678f5ac1aa64d4af916e83307852f25964255f3f471ca6a59088ac259b9688a`
- Bootstrap contract SHA256: `739f9c2aee9b97ad3da5d715c72c0c9cd83da7c0a00717ae8509081c9097327f`
- Authorization evidence SHA256: `f09b3c54bc009b7fd616237597f2e6b078e38b54504a45e3d8eb90e4c26fbcb1`

## Measured identity

- Module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js`
- Method definition count: 1
- Module record start: 10704
- Module record end: 11028
- Module record SHA256: `08b2da2b398b0c8a6d09c6852ee8c49b9416fa7322f256c288ff07a795580059`
- Body start: 10819
- Body end: 11027
- Body chars: 208
- Body SHA256: `659fc768c54e343ad1e4c74982b0774bdc59272f00b32be2617ef1428d03048f`

## Measurement evidence

Evidence SHA256: `cc4ddad6295ebbf87f482643650ad2b7462889e2f0f88ca14ef971b29379b346`

```json
{"authorization_document_sha256":"1678f5ac1aa64d4af916e83307852f25964255f3f471ca6a59088ac259b9688a","authorization_evidence_sha256":"f09b3c54bc009b7fd616237597f2e6b078e38b54504a45e3d8eb90e4c26fbcb1","body_chars":208,"body_end":11027,"body_sha256":"659fc768c54e343ad1e4c74982b0774bdc59272f00b32be2617ef1428d03048f","body_start":10819,"bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","method_definition_count":1,"method_definition_token":"\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js\"(e,t,n){","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","module_record_end":11028,"module_record_sha256":"08b2da2b398b0c8a6d09c6852ee8c49b9416fa7322f256c288ff07a795580059","module_record_start":10704,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","source_execution_performed":false,"statement_classification_count":0,"version":"GATE4_DIAG_TYPES_IDENTITY_BOOTSTRAP_MEASUREMENT_V1"}
```

## Strict boundary

This gate used the frozen identity-bootstrap authority only to locate one exact method-style types.js module definition and calculate wrapper and body identities. No statement splitting or statement classification was performed. No JavaScript was executed. The parent diag.js frontier and OTEL authority were not advanced or mutated.
