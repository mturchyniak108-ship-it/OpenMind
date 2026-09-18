# Cursor OTEL Gate-4 diag.js identity-bootstrap read authorization

Date: 2026-09-15

## Status

- Audit status: PASS
- Authorization status: `AUTHORIZED_IDENTITY_BOOTSTRAP_MEASUREMENT_ONLY`
- Identity-bootstrap measurement authorized: YES
- Statement classification authorized: NO
- Source execution authorized: NO
- OTEL authority mutation authorized: NO

## Frozen prerequisite

- Previous metadata audit SHA256: `62ffa2880cfed5d37a1e00d9a9e7263f3201d56b5efe84cdecb6554d397a1ab1`
- Previous metadata evidence SHA256: `0b38a7ada35d2f0bf1010d0e277a063231c4fa814423d1f02f0d5b97d80dde62`
- Metadata absence proven: YES
- Strong body identity candidates: 0
- Unique body identity pairs: 0
- Identity bootstrap required: YES

## Authorized measurement

- Module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js`
- Frozen Cursor SHA256: `890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054`
- Read mode: `IDENTITY_BOOTSTRAP_MEASUREMENT_ONLY`
- Expected method-style locator token: `"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js"(e,t,n){`
- Required definition count: 1
- Authorized static statement count: 0

## Contract

- Bootstrap contract SHA256: `9498b478621f78720e4e1432960b03cc292aaad1484655f0fb811a0f4c4c4cd9`

```json
{"allowed_operations":["read frozen Cursor bundle bytes or text","search exact diag.js method-style module definition token","require exactly one matching module definition","structurally match only the wrapper closing brace","measure exact wrapper body character count","compute exact wrapper body SHA256","compute exact module record SHA256"],"allowed_outputs":["unique_method_definition_count","module_record_start","module_record_end","module_record_sha256","body_start","body_end","body_chars","body_sha256"],"authority_mutation_authorized":false,"bundle_path":"package/dist-package/index.js","bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_authorized":false,"dependency_parent_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","execution_authorized":false,"identity_bootstrap_reason":"NO_SURVIVING_DIAG_BODY_IDENTITY","method_definition_token":"\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js\"(e,t,n){","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","next_gate_after_success":"DIAG_BODY_IDENTITY_FREEZE","prohibited_operations":["split diag.js body into statements","classify any diag.js statement or initializer","evaluate or execute JavaScript","persist any diag.js recursive state","advance api/context.js rows","mutate OTEL authority JSON","evaluate Gate 5","execute Cursor","push Git"],"read_mode":"IDENTITY_BOOTSTRAP_MEASUREMENT_ONLY","statement_count_authorized":0,"version":"GATE4_DIAG_IDENTITY_BOOTSTRAP_READ_CONTRACT_V1"}
```

## Evidence

Evidence SHA256: `d6550d2d8ffc6deee67f0fbfe3ed140be425e9f1c6ebb5c6638cd5b4fb5e4d3d`

```json
{"api_context_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","authorization_status":"AUTHORIZED_IDENTITY_BOOTSTRAP_MEASUREMENT_ONLY","bootstrap_authorized":true,"bootstrap_contract":{"allowed_operations":["read frozen Cursor bundle bytes or text","search exact diag.js method-style module definition token","require exactly one matching module definition","structurally match only the wrapper closing brace","measure exact wrapper body character count","compute exact wrapper body SHA256","compute exact module record SHA256"],"allowed_outputs":["unique_method_definition_count","module_record_start","module_record_end","module_record_sha256","body_start","body_end","body_chars","body_sha256"],"authority_mutation_authorized":false,"bundle_path":"package/dist-package/index.js","bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_authorized":false,"dependency_parent_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","execution_authorized":false,"identity_bootstrap_reason":"NO_SURVIVING_DIAG_BODY_IDENTITY","method_definition_token":"\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js\"(e,t,n){","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","next_gate_after_success":"DIAG_BODY_IDENTITY_FREEZE","prohibited_operations":["split diag.js body into statements","classify any diag.js statement or initializer","evaluate or execute JavaScript","persist any diag.js recursive state","advance api/context.js rows","mutate OTEL authority JSON","evaluate Gate 5","execute Cursor","push Git"],"read_mode":"IDENTITY_BOOTSTRAP_MEASUREMENT_ONLY","statement_count_authorized":0,"version":"GATE4_DIAG_IDENTITY_BOOTSTRAP_READ_CONTRACT_V1"},"bootstrap_contract_sha256":"9498b478621f78720e4e1432960b03cc292aaad1484655f0fb811a0f4c4c4cd9","classification_authorized":false,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","diag_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","expected_locator_precedent_evidence_sha256":"52eac2bc539d8f3e5c338a27edbfedd76e065deec1f025ce89199e32e4ce915e","metadata_absence_proven":true,"metadata_identity_pair_count":0,"metadata_strong_candidate_count":0,"previous_metadata_audit_sha256":"62ffa2880cfed5d37a1e00d9a9e7263f3201d56b5efe84cdecb6554d397a1ab1","previous_metadata_evidence_sha256":"0b38a7ada35d2f0bf1010d0e277a063231c4fa814423d1f02f0d5b97d80dde62","source_execution_authorized":false,"statement_count_authorized":0,"version":"GATE4_DIAG_IDENTITY_BOOTSTRAP_READ_AUTHORIZATION_V1"}
```

## Strict boundary

This gate authorizes one later identity-bootstrap measurement only. The later measurement may locate exactly one diag.js webpack definition and measure its body length and SHA256. It may not split, classify, evaluate, execute, or persist any diag.js statement.
