# Cursor OTEL Gate-4 api context pre-diag persisted frontier recovery

Date: 2026-09-15

## Status

- Audit status: PASS
- Historical schema repaired: YES
- Historical authority mode: `AFTER_COMPLETED_PERSISTED_DEPENDENCY_FRONTIER`
- Persisted frontier body span: 30:1084
- Resume delimiter offset: 1084
- First unqualified item start: 1085
- New static item classification: NO
- Parent advancement: NO

## Frozen historical authority

- Frontier document SHA256: `91bd52e6759297d6cc31c5c58e4e05bb950d6752397bebb4a3ce329d86050c61`
- Frontier evidence SHA256: `ad64be1a74ea6b364f114d1b98918c4ef3d9983f7e8734b2e3fb79066ac5b973`
- Persisted next kind: `DEPENDENCY_INTERNAL_REQUIRE`
- Persisted next source SHA256: `b0e7c214b2e8b99a4dd37997fc4aa497658b8e4d83f09136a25d56d1a64ee8c3`
- Persisted next source: `i=n("../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js")`
- Persisted next source offsets: 961:1084
- global-utils completed state SHA256: `f4b8f19271c054b83809afc2908a394a4d33457988d2cef6c54e4013a3b3a929`

## Recovered persisted frontier

- Frontier source span: 30:1084
- Frontier source SHA256: `448c20b39be4025f774a224e7135c982ee08362c6a2b2a663fba2bf493a45bbe`
- Pre-diag coverage span: 0:1085
- Pre-diag body SHA256: `cb274f698ba42f6828f9ba0e67fe064f536a23419128206a9b372d5488b9c479`
- Coverage SHA256: `fb0d507ff248b81470a2d5f5c9b719a2e6f73865a0d7094a840d38fdb7690c54`
- Exact pre-diag reconstruction: YES

## Recovery contract

- Contract SHA256: `54adaac2a5aa04fd3384fbebc63270bb01457389ba066cb87c1a914e0ebe2d4f`

```json
{"completed_global_utils_state_sha256":"f4b8f19271c054b83809afc2908a394a4d33457988d2cef6c54e4013a3b3a929","context_body_sha256":"d8a3982b67173a9152b5b610028a5dad7eb9f459a3f31432e0624f89592da17e","frontier_document_sha256":"91bd52e6759297d6cc31c5c58e4e05bb950d6752397bebb4a3ce329d86050c61","frontier_evidence_sha256":"ad64be1a74ea6b364f114d1b98918c4ef3d9983f7e8734b2e3fb79066ac5b973","historical_resume_mode":"AFTER_COMPLETED_PERSISTED_DEPENDENCY_FRONTIER","historical_resume_offset":1084,"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","persisted_frontier_end":1084,"persisted_frontier_sha256":"448c20b39be4025f774a224e7135c982ee08362c6a2b2a663fba2bf493a45bbe","persisted_frontier_start":30,"persisted_next_sha256":"b0e7c214b2e8b99a4dd37997fc4aa497658b8e4d83f09136a25d56d1a64ee8c3","persisted_next_source_end":1084,"persisted_next_source_start":961,"prediag_coverage_end":1085,"prediag_coverage_sha256":"fb0d507ff248b81470a2d5f5c9b719a2e6f73865a0d7094a840d38fdb7690c54","prediag_coverage_start":0,"source_execution_authorized":false,"version":"GATE4_API_CONTEXT_PREDIAG_PERSISTED_FRONTIER_RECOVERY_CONTRACT_V1"}
```

## Recovery evidence

Evidence SHA256: `3b4d02e973bec124bc4c3b7ddc8fcf953e6557152ad2aa55106f90a71a3dd16a`

```json
{"contract":{"completed_global_utils_state_sha256":"f4b8f19271c054b83809afc2908a394a4d33457988d2cef6c54e4013a3b3a929","context_body_sha256":"d8a3982b67173a9152b5b610028a5dad7eb9f459a3f31432e0624f89592da17e","frontier_document_sha256":"91bd52e6759297d6cc31c5c58e4e05bb950d6752397bebb4a3ce329d86050c61","frontier_evidence_sha256":"ad64be1a74ea6b364f114d1b98918c4ef3d9983f7e8734b2e3fb79066ac5b973","historical_resume_mode":"AFTER_COMPLETED_PERSISTED_DEPENDENCY_FRONTIER","historical_resume_offset":1084,"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","persisted_frontier_end":1084,"persisted_frontier_sha256":"448c20b39be4025f774a224e7135c982ee08362c6a2b2a663fba2bf493a45bbe","persisted_frontier_start":30,"persisted_next_sha256":"b0e7c214b2e8b99a4dd37997fc4aa497658b8e4d83f09136a25d56d1a64ee8c3","persisted_next_source_end":1084,"persisted_next_source_start":961,"prediag_coverage_end":1085,"prediag_coverage_sha256":"fb0d507ff248b81470a2d5f5c9b719a2e6f73865a0d7094a840d38fdb7690c54","prediag_coverage_start":0,"source_execution_authorized":false,"version":"GATE4_API_CONTEXT_PREDIAG_PERSISTED_FRONTIER_RECOVERY_CONTRACT_V1"},"contract_sha256":"54adaac2a5aa04fd3384fbebc63270bb01457389ba066cb87c1a914e0ebe2d4f","coverage_segments":[{"end":12,"kind":"FROZEN_PERSISTED_ROW","source_sha256":"4ee188e1744c19816e95a540b2650ed9f033ea0371e74eac8e717355cfca8741","start":0},{"end":13,"kind":"STRUCTURAL_SEMICOLON","sha256":"41b805ea7ac014e23556e98bb374702a08344268f92489a02f0880849394a1e4","start":12},{"end":29,"kind":"FROZEN_PERSISTED_ROW","source_sha256":"6a35bbd573628400d124a3d1c79e8ea45de35828f68ad8fc2c9086693afb5ea5","start":13},{"end":30,"kind":"STRUCTURAL_SEMICOLON","sha256":"41b805ea7ac014e23556e98bb374702a08344268f92489a02f0880849394a1e4","start":29},{"end":1084,"frontier_tail_source_sha256":"b0e7c214b2e8b99a4dd37997fc4aa497658b8e4d83f09136a25d56d1a64ee8c3","frontier_tail_start":961,"kind":"FROZEN_COMPLETED_PERSISTED_DEPENDENCY_FRONTIER","sha256":"448c20b39be4025f774a224e7135c982ee08362c6a2b2a663fba2bf493a45bbe","start":30},{"end":1085,"kind":"STRUCTURAL_DECLARATOR_COMMA","sha256":"d03502c43d74a30b936740a9517dc4ea2b2ad7168caa0a774cefe793ce0b33e7","start":1084}],"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","first_unqualified_diag_source_sha256":"6cd448ef0f65cdde11d39816a657b76ed14ddffcf5e3aecc9b034d08127571db","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","prediag_body_sha256":"cb274f698ba42f6828f9ba0e67fe064f536a23419128206a9b372d5488b9c479","source_auth_document_sha256":"8a1c6125c757d4db142e0f5821abf29ba6adf7e2ea2c8d288f89b0bf4494fbb5","source_auth_evidence_sha256":"1aafe18e7887b251aba7b3a0f88cf6cd80deb277f12c3b9359ad07a902f11c30","source_executed":false,"version":"GATE4_API_CONTEXT_PREDIAG_PERSISTED_FRONTIER_RECOVERY_V1"}
```

## Strict boundary

This audit repairs only the historical authority representation for api/context.js bytes before the already-frozen diag frontier. The region 30:1084 is treated as one previously completed persisted dependency frontier because the committed historical frontier explicitly resumes after that completed frontier at offset 1084. The final persisted dependency source is verified to terminate exactly at the frozen resume delimiter. No new static item is classified. No completed child source is reread, no parent is resumed, no JavaScript is executed, the OTEL authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
