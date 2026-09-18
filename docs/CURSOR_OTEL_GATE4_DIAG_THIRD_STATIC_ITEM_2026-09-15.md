# Cursor OTEL Gate-4 diag.js third static item

Date: 2026-09-15

## Status

- Audit status: PASS
- Static items classified this gate: 1
- Cumulative frozen rows: 3
- Fourth item classified: NO
- Source executed: NO
- OTEL authority mutated: NO

## Frozen authorization

- Authorization commit: `832e6a923284dc0c2def1afd781e4af0332ff235`
- Authorization document SHA256: `b0af32240e530c53773009b1a73068d53f0eb76e12aaa418373700c8328d408f`
- Authorization contract SHA256: `ec455b776334bbd44588455bbda9c1f0e496beb0fd7003435a176aacb80180ea`
- Authorization evidence SHA256: `b4f01215f6794e09d2a2e79a9b9a45b6347615188140ef6fbfb0ac9242abc0d6`

## Third static item

- Kind: `WEBPACK_REQUIRE_BINDING`
- Boundary kind: `DECLARATOR_COMMA`
- Binding: `r`
- Dependency module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js`
- Body offsets: 34:157
- Terminator offset: 157
- Source SHA256: `34199cab9401f5023274f51372433f3101e365698bd55552834b76e0cd47d186`
- Canonical row SHA256: `41c1745b022074c1e7539b8a51e9d28f9926a073f3e729d1aa70a9594773e8b0`
- Source: `r=n("../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js")`

## Evidence

Evidence SHA256: `6b7e6699a9660dae01c625b778e57df5b421f5167b68148c54bbc7d189cb7c8a`

```json
{"authorization_commit":"832e6a923284dc0c2def1afd781e4af0332ff235","authorization_contract_sha256":"ec455b776334bbd44588455bbda9c1f0e496beb0fd7003435a176aacb80180ea","authorization_document_sha256":"b0af32240e530c53773009b1a73068d53f0eb76e12aaa418373700c8328d408f","authorization_evidence_sha256":"b4f01215f6794e09d2a2e79a9b9a45b6347615188140ef6fbfb0ac9242abc0d6","body_chars":3461,"body_sha256":"7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195","classification_count_this_gate":1,"cumulative_classified_rows":3,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","fourth_item_classified":false,"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","module_record_sha256":"b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","second_row_sha256":"0f5b078bd89f25b456890011fbcac23a7502f9560d7db606dea916b2b45525da","source_executed":false,"third_item":{"binding":"r","boundary_kind":"DECLARATOR_COMMA","dependency_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js","end":157,"kind":"WEBPACK_REQUIRE_BINDING","ordinal":3,"source":"r=n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js\")","source_sha256":"34199cab9401f5023274f51372433f3101e365698bd55552834b76e0cd47d186","start":34,"terminator":157},"third_item_sha256":"41c1745b022074c1e7539b8a51e9d28f9926a073f3e729d1aa70a9594773e8b0","version":"GATE4_DIAG_THIRD_STATIC_ITEM_V1"}
```

## Strict boundary

Only the third diag.js static item was classified by this gate. For a multi-declarator declaration only its first declarator was classified. No fourth item was recovered or classified. No JavaScript was executed and no OTEL authority state was mutated.
