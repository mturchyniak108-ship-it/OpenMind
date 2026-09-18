# Cursor OTEL Gate-4 diag.js identity-bootstrap measurement

Date: 2026-09-15

## Status

- Audit status: PASS
- Measurement mode: `IDENTITY_BOOTSTRAP_MEASUREMENT_ONLY`
- Statement classification performed: NO
- Source executed: NO
- OTEL authority mutated: NO

## Frozen authorization

- Authorization audit SHA256: `e9056e1acfb2d875eed7d09c7339e6889bfbadb1603026fe489d1e1fcf86dfee`
- Bootstrap contract SHA256: `9498b478621f78720e4e1432960b03cc292aaad1484655f0fb811a0f4c4c4cd9`
- Authorization evidence SHA256: `d6550d2d8ffc6deee67f0fbfe3ed140be425e9f1c6ebb5c6638cd5b4fb5e4d3d`

## Measured module identity

- Module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js`
- Unique method-style definitions: 1
- Module record range: 4083:7658
- Module record SHA256: `b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8`
- Body range: 4196:7657
- Body chars: 3461
- Body SHA256: `7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195`

## Measurement evidence

Evidence SHA256: `815b1c3b9da1e5ef4ad9483f429042ba63456761bbcab99b7b79906c6c53299c`

```json
{"authorization_audit_sha256":"e9056e1acfb2d875eed7d09c7339e6889bfbadb1603026fe489d1e1fcf86dfee","authorization_evidence_sha256":"d6550d2d8ffc6deee67f0fbfe3ed140be425e9f1c6ebb5c6638cd5b4fb5e4d3d","body_chars":3461,"body_end":7657,"body_sha256":"7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195","body_start":4196,"bootstrap_contract_sha256":"9498b478621f78720e4e1432960b03cc292aaad1484655f0fb811a0f4c4c4cd9","bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","classification_performed":false,"definition_count":1,"method_definition_token":"\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js\"(e,t,n){","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","module_record_end":7658,"module_record_sha256":"b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8","module_record_start":4083,"source_executed":false,"statement_count_classified":0,"version":"GATE4_DIAG_IDENTITY_BOOTSTRAP_MEASUREMENT_V1"}
```

## Strict boundary

The diag.js wrapper body was read only to measure its exact range, character count, and SHA256. No statement splitting or classification was performed. No JavaScript was evaluated or executed. No OTEL authority state was mutated.
