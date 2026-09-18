# Cursor OTEL Gate-4 api context module completion

Date: 2026-09-15

## Status

- Audit status: PASS
- Module completion qualified: YES
- Exact body coverage: 0:2365
- Exact body reconstruction: YES
- Dependency count: 3
- Unresolved dependency count: 0
- Parent context-api.js advanced: NO

## Frozen pre-diag authority

- Persisted-frontier recovery evidence SHA256: `3b4d02e973bec124bc4c3b7ddc8fcf953e6557152ad2aa55106f90a71a3dd16a`
- Persisted-frontier dependency-closure evidence SHA256: `7611e80edd8b4f273078491a26e5571eb38c60edbbedd8c2c7fbf85f738373a7`
- Pre-diag body SHA256: `cb274f698ba42f6828f9ba0e67fe064f536a23419128206a9b372d5488b9c479`

## Frozen post-frontier authority

- diag require source SHA256: `6cd448ef0f65cdde11d39816a657b76ed14ddffcf5e3aecc9b034d08127571db`
- binding a row SHA256: `3dfb28d511a1b398124d5e5f1eecc6ae8ce2f63050481255cbe7d1e566c164a4`
- binding l row SHA256: `0b96fb7f6596f33758dc5b6d2b4c20d5e4e9c77e727428ebe51efd97566888c0`
- body-end binding u row SHA256: `bebedf0bb38b789d0a6e78a841cd741ff945a1070f43f7c6cbaa432a72eab1c9`

## Exact coverage

- Coverage SHA256: `4309f03808fbd9a42a432cc631838eadfdbed4e82c191730c41e3d949b5e44e2`
- Body reconstruction SHA256: `d8a3982b67173a9152b5b610028a5dad7eb9f459a3f31432e0624f89592da17e`

## Completed dependencies

- context/context.js completed state SHA256: `e303bd5f3daa7721b8855ee2440b254971fba3717c9f96067e9d19d819e53435`
- global-utils.js completed state SHA256: `f4b8f19271c054b83809afc2908a394a4d33457988d2cef6c54e4013a3b3a929`
- diag.js completed state SHA256: `d1c86b38caf273d343e95d5198da380ec66fbdbee2add54d4cac8305c91df0e9`
- Completed dependency set SHA256: `6cfc4852c64ca550f8c4f6b2e5a1835851a672f3e05b81edf835ee2c30aa1f0f`
- Unresolved dependency count: 0

## Completed api context state

- Completed state SHA256: `fada3ecb5ce3e16fb2da60c54a312af1bc98dc3ad1339e50e8788c336739d215`

```json
{"body_chars":2365,"body_sha256":"d8a3982b67173a9152b5b610028a5dad7eb9f459a3f31432e0624f89592da17e","completed":true,"completed_dependency_set_sha256":"6cfc4852c64ca550f8c4f6b2e5a1835851a672f3e05b81edf835ee2c30aa1f0f","coverage_end":2365,"coverage_sha256":"4309f03808fbd9a42a432cc631838eadfdbed4e82c191730c41e3d949b5e44e2","coverage_start":0,"dependency_count":3,"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","module_record_sha256":"e5ab0daa3dc7bed29eda2ce170e726bc6875586094dbe16a8eccf7b4a85834f7","prediag_dependency_closure_evidence_sha256":"7611e80edd8b4f273078491a26e5571eb38c60edbbedd8c2c7fbf85f738373a7","prediag_frontier_recovery_evidence_sha256":"3b4d02e973bec124bc4c3b7ddc8fcf953e6557152ad2aa55106f90a71a3dd16a","unresolved_dependency_count":0,"version":"GATE4_API_CONTEXT_COMPLETED_STATE_V2"}
```

## Completion evidence

Evidence SHA256: `765ddd2b4de1f77d1a6c3b070f7fe945ded98ff111f7cd0c10dc2d144530bd63`

```json
{"body_reconstruction_equal":true,"body_reconstruction_sha256":"d8a3982b67173a9152b5b610028a5dad7eb9f459a3f31432e0624f89592da17e","completed_dependencies":[{"binding":"o","completed_state_sha256":"d1c86b38caf273d343e95d5198da380ec66fbdbee2add54d4cac8305c91df0e9","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","source_sha256":"6cd448ef0f65cdde11d39816a657b76ed14ddffcf5e3aecc9b034d08127571db"},{"binding":"r","completed_state_sha256":"e303bd5f3daa7721b8855ee2440b254971fba3717c9f96067e9d19d819e53435","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context/context.js","source_sha256":"4ce03a3763d36ad0f384fdc7c44df60924e2e2b8d801af9cb4be902490381ab5"},{"binding":"i","completed_state_sha256":"f4b8f19271c054b83809afc2908a394a4d33457988d2cef6c54e4013a3b3a929","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js","source_sha256":"b0e7c214b2e8b99a4dd37997fc4aa497658b8e4d83f09136a25d56d1a64ee8c3"}],"completed_dependency_set_sha256":"6cfc4852c64ca550f8c4f6b2e5a1835851a672f3e05b81edf835ee2c30aa1f0f","completed_state":{"body_chars":2365,"body_sha256":"d8a3982b67173a9152b5b610028a5dad7eb9f459a3f31432e0624f89592da17e","completed":true,"completed_dependency_set_sha256":"6cfc4852c64ca550f8c4f6b2e5a1835851a672f3e05b81edf835ee2c30aa1f0f","coverage_end":2365,"coverage_sha256":"4309f03808fbd9a42a432cc631838eadfdbed4e82c191730c41e3d949b5e44e2","coverage_start":0,"dependency_count":3,"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","module_record_sha256":"e5ab0daa3dc7bed29eda2ce170e726bc6875586094dbe16a8eccf7b4a85834f7","prediag_dependency_closure_evidence_sha256":"7611e80edd8b4f273078491a26e5571eb38c60edbbedd8c2c7fbf85f738373a7","prediag_frontier_recovery_evidence_sha256":"3b4d02e973bec124bc4c3b7ddc8fcf953e6557152ad2aa55106f90a71a3dd16a","unresolved_dependency_count":0,"version":"GATE4_API_CONTEXT_COMPLETED_STATE_V2"},"completed_state_sha256":"fada3ecb5ce3e16fb2da60c54a312af1bc98dc3ad1339e50e8788c336739d215","coverage_segments":[{"end":1085,"kind":"FROZEN_PREDIAG_COVERAGE","sha256":"cb274f698ba42f6828f9ba0e67fe064f536a23419128206a9b372d5488b9c479","start":0},{"end":1195,"kind":"FROZEN_DIAG_REQUIRE_ROW","sha256":"6cd448ef0f65cdde11d39816a657b76ed14ddffcf5e3aecc9b034d08127571db","start":1085},{"end":1196,"kind":"STRUCTURAL_DECLARATOR_COMMA","sha256":"d03502c43d74a30b936740a9517dc4ea2b2ad7168caa0a774cefe793ce0b33e7","start":1195},{"end":1207,"kind":"FROZEN_STATIC_ROW_A","row_sha256":"3dfb28d511a1b398124d5e5f1eecc6ae8ce2f63050481255cbe7d1e566c164a4","sha256":"e816bf11336bc27780afb432552294337b06fa8df9f5d1e434179a149ce3fde2","start":1196},{"end":1208,"kind":"STRUCTURAL_DECLARATOR_COMMA","sha256":"d03502c43d74a30b936740a9517dc4ea2b2ad7168caa0a774cefe793ce0b33e7","start":1207},{"end":1215,"kind":"FROZEN_STATIC_ROW_L","row_sha256":"0b96fb7f6596f33758dc5b6d2b4c20d5e4e9c77e727428ebe51efd97566888c0","sha256":"70c9a99297f6a03f7d6c6fc218f25378cd6ebb682d48b3434f4ac9096bc6c0da","start":1208},{"end":1216,"kind":"STRUCTURAL_DECLARATOR_COMMA","sha256":"d03502c43d74a30b936740a9517dc4ea2b2ad7168caa0a774cefe793ce0b33e7","start":1215},{"end":2365,"kind":"FROZEN_BODY_END_ROW_U","row_sha256":"bebedf0bb38b789d0a6e78a841cd741ff945a1070f43f7c6cbaa432a72eab1c9","sha256":"d4d365601fc083152d6263c5455c21ca92fcc7afcb4242a440f833fa82a966ef","start":1216}],"coverage_sha256":"4309f03808fbd9a42a432cc631838eadfdbed4e82c191730c41e3d949b5e44e2","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","diag_completion_evidence_sha256":"2782e4ac04d9c5b71e1615fa86124366664cac01139655b1bea0040046c933c1","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","next_parent_advanced":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","prediag_dependency_closure_evidence_sha256":"7611e80edd8b4f273078491a26e5571eb38c60edbbedd8c2c7fbf85f738373a7","prediag_frontier_recovery_evidence_sha256":"3b4d02e973bec124bc4c3b7ddc8fcf953e6557152ad2aa55106f90a71a3dd16a","source_executed":false,"unresolved_dependency_count":0,"version":"GATE4_API_CONTEXT_MODULE_COMPLETION_V2"}
```

## Strict boundary

This audit completes only api/context.js. It binds the already-qualified persisted pre-diag frontier, its closed child dependencies, the completed diag child, and the already-frozen post-diag rows through the exact body end. No completed child source is reread. context-api.js is not resumed. No JavaScript is executed, the OTEL authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
