# Cursor OTEL Gate-4 diag types identity-bootstrap read authorization

Date: 2026-09-15

## Status

- Audit status: PASS
- Authorization status: `AUTHORIZED_IDENTITY_BOOTSTRAP_MEASUREMENT_ONLY`
- Identity bootstrap required: YES
- Source read this gate: NO
- Statement classification authorized: NO
- Authorized statement count: 0
- Source execution authorized: NO
- OTEL authority mutation authorized: NO

## Frozen prerequisite

- Pre-source audit SHA256: `5d728a47849f55e6e991c4779a9e9723bc28844deaf2f4e731dfca5cfdaa8bc6`
- Pre-source evidence SHA256: `352a8a31365b4c45d14c4a5218c8f5ded5ed2b9730a0c150447e1072fd67cb4a`
- Metadata absence proven: YES
- Current types.js states: 0
- Historical exact types.js records: 0
- Unique body identities: 0
- Parent dependency row SHA256: `94a35d9d4773eb333ec435b0ea231cb2f9372ec9675f75e555da7a41c33ddf04`

## Bootstrap authorization

- Module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js`
- Read mode: `IDENTITY_BOOTSTRAP_MEASUREMENT_ONLY`
- Required definition count: 1
- Method definition token: `"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js"(e,t,n){`
- Body length measurement authorized: YES
- Body SHA256 measurement authorized: YES
- Module record SHA256 measurement authorized: YES
- Statement classification authorized: NO
- Source execution authorized: NO

## Bootstrap contract

- Contract SHA256: `739f9c2aee9b97ad3da5d715c72c0c9cd83da7c0a00717ae8509081c9097327f`

```json
{"authority_mutation_authorized":false,"body_length_measurement_authorized":true,"body_sha256_measurement_authorized":true,"bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_authorized":false,"identity_bootstrap_required":true,"measurement_mode":"IDENTITY_BOOTSTRAP_MEASUREMENT_ONLY","method_definition_token":"\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js\"(e,t,n){","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","module_record_sha256_measurement_authorized":true,"parent_dependency_row_sha256":"94a35d9d4773eb333ec435b0ea231cb2f9372ec9675f75e555da7a41c33ddf04","pre_source_evidence_sha256":"352a8a31365b4c45d14c4a5218c8f5ded5ed2b9730a0c150447e1072fd67cb4a","required_definition_count":1,"source_execution_authorized":false,"statement_count_authorized":0,"version":"GATE4_DIAG_TYPES_IDENTITY_BOOTSTRAP_READ_CONTRACT_V1"}
```

## Authorization evidence

Evidence SHA256: `f09b3c54bc009b7fd616237597f2e6b078e38b54504a45e3d8eb90e4c26fbcb1`

```json
{"authorization_status":"AUTHORIZED_IDENTITY_BOOTSTRAP_MEASUREMENT_ONLY","bootstrap_contract":{"authority_mutation_authorized":false,"body_length_measurement_authorized":true,"body_sha256_measurement_authorized":true,"bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_authorized":false,"identity_bootstrap_required":true,"measurement_mode":"IDENTITY_BOOTSTRAP_MEASUREMENT_ONLY","method_definition_token":"\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js\"(e,t,n){","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","module_record_sha256_measurement_authorized":true,"parent_dependency_row_sha256":"94a35d9d4773eb333ec435b0ea231cb2f9372ec9675f75e555da7a41c33ddf04","pre_source_evidence_sha256":"352a8a31365b4c45d14c4a5218c8f5ded5ed2b9730a0c150447e1072fd67cb4a","required_definition_count":1,"source_execution_authorized":false,"statement_count_authorized":0,"version":"GATE4_DIAG_TYPES_IDENTITY_BOOTSTRAP_READ_CONTRACT_V1"},"bootstrap_contract_sha256":"739f9c2aee9b97ad3da5d715c72c0c9cd83da7c0a00717ae8509081c9097327f","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","metadata_absence_proven":true,"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","pre_source_document_sha256":"5d728a47849f55e6e991c4779a9e9723bc28844deaf2f4e731dfca5cfdaa8bc6","pre_source_evidence_sha256":"352a8a31365b4c45d14c4a5218c8f5ded5ed2b9730a0c150447e1072fd67cb4a","source_read_this_gate":false,"version":"GATE4_DIAG_TYPES_IDENTITY_BOOTSTRAP_READ_AUTHORIZATION_V1"}
```

## Strict boundary

This gate authorizes the next gate to locate exactly one method-style types.js module definition and measure only module-record range, module-record SHA256, body range, body length, and body SHA256. It does not authorize statement splitting or classification. It does not authorize JavaScript execution, parent diag.js advancement, OTEL authority mutation, Gate 5 evaluation, Cursor execution, or Git push.
