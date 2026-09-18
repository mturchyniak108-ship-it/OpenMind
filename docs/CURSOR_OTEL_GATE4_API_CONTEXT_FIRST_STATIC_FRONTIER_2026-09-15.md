# Cursor OTEL Gate-4 api/context.js first static frontier

Date: 2026-09-15

## Status

- Bounded source read: PASS
- Source executed: NO
- OTEL authority mutated: NO
- Gate 5 evaluated: NO
- Cursor executed: NO

## Frozen module extraction

- Module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js`
- Unique webpack module records: 1
- Body chars: 2365
- Body SHA256: `d8a3982b67173a9152b5b610028a5dad7eb9f459a3f31432e0624f89592da17e`
- Module record SHA256: `e5ab0daa3dc7bed29eda2ce170e726bc6875586094dbe16a8eccf7b4a85834f7`
- Body bundle range: 1716:4081

## Persisted qualification reconciliation

- Persisted rows: 2
- Persisted next kind: `DEPENDENCY_INTERNAL_REQUIRE`
- Persisted next source: `i=n("../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js")`
- Resume mode: `AFTER_COMPLETED_PERSISTED_DEPENDENCY_FRONTIER`
- Resume offset: 1084

## First unqualified item

- Kind: `WEBPACK_REQUIRE_BINDING`
- Binding: `o`
- Dependency module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js`
- Body offsets: 1085:1195
- Source SHA256: `6cd448ef0f65cdde11d39816a657b76ed14ddffcf5e3aecc9b034d08127571db`
- Source: `o=n("../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js")`

## Evidence

Evidence SHA256: `ad64be1a74ea6b364f114d1b98918c4ef3d9983f7e8734b2e3fb79066ac5b973`

```json
{"authorization_evidence_sha256":"1aafe18e7887b251aba7b3a0f88cf6cd80deb277f12c3b9359ad07a902f11c30","body_chars":2365,"body_sha256":"d8a3982b67173a9152b5b610028a5dad7eb9f459a3f31432e0624f89592da17e","bundle_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","first_unqualified":{"binding":"o","dependency_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","end":1195,"kind":"WEBPACK_REQUIRE_BINDING","source":"o=n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js\")","source_sha256":"6cd448ef0f65cdde11d39816a657b76ed14ddffcf5e3aecc9b034d08127571db","start":1085},"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","module_body_bundle_end":4081,"module_body_bundle_start":1716,"module_key_count":1,"module_record_bundle_end":4082,"module_record_bundle_start":1600,"module_record_sha256":"e5ab0daa3dc7bed29eda2ce170e726bc6875586094dbe16a8eccf7b4a85834f7","persisted_next_kind":"DEPENDENCY_INTERNAL_REQUIRE","persisted_next_sha256":"b0e7c214b2e8b99a4dd37997fc4aa497658b8e4d83f09136a25d56d1a64ee8c3","persisted_next_source":"i=n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js\")","persisted_row_count":2,"persisted_row_positions":[{"end":12,"index":0,"kind":"DIRECTIVE","source":"\"use strict\"","source_sha256":"4ee188e1744c19816e95a540b2650ed9f033ea0371e74eac8e717355cfca8741","start":0},{"end":29,"index":1,"kind":"WEBPACK_EXPORT_GETTER_INSTALLATION","source":"n.d(t,{_:()=>u})","source_sha256":"6a35bbd573628400d124a3d1c79e8ea45de35828f68ad8fc2c9086693afb5ea5","start":13}],"read_contract_sha256":"acf394e8d3456227b474c3fc5820d2fa999868c54f8605c2f2a670b6dcad3bfb","resume_mode":"AFTER_COMPLETED_PERSISTED_DEPENDENCY_FRONTIER","resume_offset":1084,"source_executed":false,"static_item_count":9,"version":"GATE4_API_CONTEXT_FIRST_STATIC_FRONTIER_V1"}
```

## Strict boundary

Exactly one previously unqualified static item was classified. No source was executed and no OTEL authority state was advanced.
