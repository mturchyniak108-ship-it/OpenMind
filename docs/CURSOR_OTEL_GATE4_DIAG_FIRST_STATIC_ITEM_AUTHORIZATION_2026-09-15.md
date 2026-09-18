# Cursor OTEL Gate-4 diag.js first static item authorization

Date: 2026-09-15

## Status

- Audit status: PASS
- Authorization status: `AUTHORIZED_FIRST_STATIC_ITEM_ONLY`
- Authorized item count: 1
- Source execution authorized: NO
- OTEL authority mutation authorized: NO

## Frozen body authority

- Measurement audit SHA256: `45271319770b0071c5aa3dd8089789e95409f042a9620cd8eded245560c29f3d`
- Measurement evidence SHA256: `815b1c3b9da1e5ef4ad9483f429042ba63456761bbcab99b7b79906c6c53299c`
- Module record SHA256: `b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8`
- Body chars: 3461
- Body SHA256: `7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195`

## Authorization contract

- Contract SHA256: `d3556ae3dc7b31940d2decbba0c516a981132a0ac264e19a09c4b4f11950f75e`

```json
{"authority_mutation_authorized":false,"authorized_item_count":1,"body_chars":3461,"body_end":7657,"body_sha256":"7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195","body_start":4196,"bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_mode":"FIRST_TOP_LEVEL_STATIC_ITEM_ONLY","execution_authorized":false,"measurement_audit_sha256":"45271319770b0071c5aa3dd8089789e95409f042a9620cd8eded245560c29f3d","measurement_evidence_sha256":"815b1c3b9da1e5ef4ad9483f429042ba63456761bbcab99b7b79906c6c53299c","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","module_record_end":7658,"module_record_sha256":"b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8","module_record_start":4083,"next_item_authorized":false,"requirements":["frozen Cursor SHA must remain exact","frozen OTEL authority SHA must remain exact","method-style diag.js definition must remain unique","module record range and SHA must match frozen measurement","body range, body_chars, and body SHA must match frozen measurement","scanner may stop only after recovering the first top-level static item","exactly one item may be classified","JavaScript execution is prohibited","OTEL authority mutation is prohibited"],"version":"GATE4_DIAG_FIRST_STATIC_ITEM_AUTHORIZATION_CONTRACT_V1"}
```

## Authorization evidence

Evidence SHA256: `7bb218b478c37f0d3326fa84839b0d0f057a46429d7fa9e63e59220ca7050204`

```json
{"authorization_status":"AUTHORIZED_FIRST_STATIC_ITEM_ONLY","authorized_item_count":1,"contract":{"authority_mutation_authorized":false,"authorized_item_count":1,"body_chars":3461,"body_end":7657,"body_sha256":"7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195","body_start":4196,"bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_mode":"FIRST_TOP_LEVEL_STATIC_ITEM_ONLY","execution_authorized":false,"measurement_audit_sha256":"45271319770b0071c5aa3dd8089789e95409f042a9620cd8eded245560c29f3d","measurement_evidence_sha256":"815b1c3b9da1e5ef4ad9483f429042ba63456761bbcab99b7b79906c6c53299c","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","module_record_end":7658,"module_record_sha256":"b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8","module_record_start":4083,"next_item_authorized":false,"requirements":["frozen Cursor SHA must remain exact","frozen OTEL authority SHA must remain exact","method-style diag.js definition must remain unique","module record range and SHA must match frozen measurement","body range, body_chars, and body SHA must match frozen measurement","scanner may stop only after recovering the first top-level static item","exactly one item may be classified","JavaScript execution is prohibited","OTEL authority mutation is prohibited"],"version":"GATE4_DIAG_FIRST_STATIC_ITEM_AUTHORIZATION_CONTRACT_V1"},"contract_sha256":"d3556ae3dc7b31940d2decbba0c516a981132a0ac264e19a09c4b4f11950f75e","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","diag_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","measurement_audit_sha256":"45271319770b0071c5aa3dd8089789e95409f042a9620cd8eded245560c29f3d","measurement_evidence_sha256":"815b1c3b9da1e5ef4ad9483f429042ba63456761bbcab99b7b79906c6c53299c","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","source_execution_authorized":false,"version":"GATE4_DIAG_FIRST_STATIC_ITEM_AUTHORIZATION_V1"}
```

## Strict boundary

Exactly one top-level static item may be recovered and classified after all frozen module and body identities are reverified. No later item may be classified by this authorization.
