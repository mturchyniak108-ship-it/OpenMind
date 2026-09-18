# Cursor OTEL Gate-4 diag types pre-source metadata audit

Date: 2026-09-15

## Status

- Audit status: PASS
- Dependency module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js`
- Dependency source read this gate: NO
- Source execution this gate: NO
- OTEL authority mutation this gate: NO

## Frozen parent frontier

- Sixth-item document SHA256: `b7367aef767b58ab8d9fcf639bbd37e9717751643b0555578961c497a2f6c582`
- Sixth-item evidence SHA256: `655802c6fa57fd6944ccbd1afbf7ae1d87d796121faad8dc1c5f8e639bf63492`
- Sixth-row SHA256: `94a35d9d4773eb333ec435b0ea231cb2f9372ec9675f75e555da7a41c33ddf04`
- Parent binding: `o`
- Parent boundary: `DECLARATOR_COMMA`
- Parent terminator offset: 1546

## Current authority metadata

- Exact types.js states: 0
- Completed states: 0
- Incomplete states: 0
- Current body identity pairs: 0

## Surviving qualification metadata

- JSON files seen: 954
- JSON files parsed: 946
- JSON parse failures: 8
- Historical exact types.js records: 0
- Historical body identity pairs: 0

## Adjudication

- Completed state reuse ready: NO
- Body identity ready: NO
- Metadata conflict: NO
- Metadata absence proven: YES
- Identity bootstrap required: YES
- Authorized body chars: None
- Authorized body SHA256: `None`
- Adjudication: `NO_SURVIVING_DIAG_TYPES_BODY_IDENTITY`
- Next authority: `DIAG_TYPES_IDENTITY_BOOTSTRAP_READ_AUTHORIZATION_AUDIT`

## Evidence

Evidence SHA256: `352a8a31365b4c45d14c4a5218c8f5ded5ed2b9730a0c150447e1072fd67cb4a`

```json
{"adjudication":"NO_SURVIVING_DIAG_TYPES_BODY_IDENTITY","authorized_body_chars":null,"authorized_body_sha256":null,"body_identity_ready":false,"combined_body_identity_pairs":[],"completed_reuse_ready":false,"completed_state_sha256_values":[],"current_body_identity_pairs":[],"current_completed_state_count":0,"current_incomplete_state_count":0,"current_state_count":0,"current_state_paths":[],"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","dependency_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","dependency_source_read_performed":false,"diag_parent_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","historical_body_identity_pairs":[],"historical_record_count":0,"historical_record_origins":[],"identity_bootstrap_required":true,"json_files_parsed":946,"json_files_seen":954,"json_parse_failures":8,"metadata_absence_proven":true,"metadata_conflict":false,"next_authority":"DIAG_TYPES_IDENTITY_BOOTSTRAP_READ_AUTHORIZATION_AUDIT","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","sixth_item_document_sha256":"b7367aef767b58ab8d9fcf639bbd37e9717751643b0555578961c497a2f6c582","sixth_item_evidence_sha256":"655802c6fa57fd6944ccbd1afbf7ae1d87d796121faad8dc1c5f8e639bf63492","sixth_row_sha256":"94a35d9d4773eb333ec435b0ea231cb2f9372ec9675f75e555da7a41c33ddf04","source_execution_performed":false,"version":"GATE4_DIAG_TYPES_PRE_SOURCE_METADATA_AUDIT_V1"}
```

## Strict boundary

This gate inspected only existing OTEL and qualification metadata for diag/types.js. It did not locate, extract, split, or classify the types.js module body. It did not execute JavaScript, advance the parent diag.js frontier, mutate the OTEL authority, evaluate Gate 5, or run Cursor.
