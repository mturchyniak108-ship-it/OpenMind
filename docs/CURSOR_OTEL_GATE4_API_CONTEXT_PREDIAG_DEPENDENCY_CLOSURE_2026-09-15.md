# Cursor OTEL Gate-4 api context pre-diag dependency closure

Date: 2026-09-15

## Status

- Audit status: PASS
- Frozen persisted frontier: 30:1084
- Embedded dependency count: 2
- Unresolved dependency count: 0
- New static item classified: NO
- Parent resumed: NO

## Embedded dependencies

- `r` -> `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context/context.js`
- `i` -> `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js`

## Completed child states

- context/context.js completed state SHA256: `e303bd5f3daa7721b8855ee2440b254971fba3717c9f96067e9d19d819e53435`
- global-utils.js completed state SHA256: `f4b8f19271c054b83809afc2908a394a4d33457988d2cef6c54e4013a3b3a929`
- Dependency set SHA256: `e41dd29d3261fd0b0c25383a1876bf359fcb987694964b82905970ec8480956d`

## Closure contract

- Contract SHA256: `73f932d8b5cbb37b4f15215c93abc323a1ae5bf3ff1f538ae64d90f247147afa`

```json
{"dependency_count":2,"dependency_set_sha256":"e41dd29d3261fd0b0c25383a1876bf359fcb987694964b82905970ec8480956d","frontier_end":1084,"frontier_sha256":"448c20b39be4025f774a224e7135c982ee08362c6a2b2a663fba2bf493a45bbe","frontier_start":30,"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","new_static_item_classification_authorized":false,"parent_resume_authorized":false,"recovery_document_sha256":"8637d52372cb891f283aa7299baf9e39c2b9d0da8853c3098eb2d000e37cc925","recovery_evidence_sha256":"3b4d02e973bec124bc4c3b7ddc8fcf953e6557152ad2aa55106f90a71a3dd16a","unresolved_dependency_count":0,"version":"GATE4_API_CONTEXT_PREDIAG_DEPENDENCY_CLOSURE_CONTRACT_V1"}
```

## Closure evidence

Evidence SHA256: `7611e80edd8b4f273078491a26e5571eb38c60edbbedd8c2c7fbf85f738373a7`

```json
{"context_core_completion_provenance":[{"document_path":"docs/CURSOR_OTEL_GATE4_CHAIN_CONTRACTION_RULE_2026-09-15.md","document_sha256":"ef0d500e10cdcac2af79dc4915855cc2a62f9b2eb8e21a7a18f257c0fbc45e37","state_sha_present":false},{"document_path":"docs/CURSOR_OTEL_GATE4_CHAIN_PRODUCER_AND_ORDERING_AUDIT_2026-09-15.md","document_sha256":"6f0f447fb7b3d8120a38264b3497356f5fcd332c583569a5865153fe41d7ef5f","state_sha_present":false},{"document_path":"docs/CURSOR_OTEL_GATE4_GLOBAL_UTILS_PERSISTENCE_AUTHORIZATION_2026-09-15.md","document_sha256":"f99f5e23b5a86b7b7a5b3a91bd7eb782ed512b76fbecf9a1db61814a9b5a1952","state_sha_present":false},{"document_path":"docs/CURSOR_OTEL_GATE4_LEAF_CHAIN_RELATION_CHARACTERIZATION_2026-09-15.md","document_sha256":"91a917670cf52c066d4328e8f24d92a73eaad914b918d31480b22ebc4c3c8592","state_sha_present":false},{"document_path":"docs/CURSOR_OTEL_GATE4_LEAF_FRONTIER_BEHAVIOR_CHARACTERIZATION_2026-09-15.md","document_sha256":"bbc42f4af750add8912e3c8e9867500afc876b5a769ca389276e6b7beccb91e0","state_sha_present":false}],"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","dependency_bindings":[{"authority_json_paths":["$.recursive_modules.../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context/context.js"],"binding":"r","completed_state_sha256":"e303bd5f3daa7721b8855ee2440b254971fba3717c9f96067e9d19d819e53435","dependency_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context/context.js","source_sha256":"4ce03a3763d36ad0f384fdc7c44df60924e2e2b8d801af9cb4be902490381ab5","source_span":[34,151]},{"binding":"i","completed_state_sha256":"f4b8f19271c054b83809afc2908a394a4d33457988d2cef6c54e4013a3b3a929","dependency_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js","source_sha256":"b0e7c214b2e8b99a4dd37997fc4aa497658b8e4d83f09136a25d56d1a64ee8c3","source_span":[961,1084]}],"dependency_set_sha256":"e41dd29d3261fd0b0c25383a1876bf359fcb987694964b82905970ec8480956d","embedded_require_rows":[{"binding":"r","dependency_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context/context.js","end":151,"source":"r=n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context/context.js\")","source_sha256":"4ce03a3763d36ad0f384fdc7c44df60924e2e2b8d801af9cb4be902490381ab5","start":34},{"binding":"i","dependency_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js","end":1084,"source":"i=n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js\")","source_sha256":"b0e7c214b2e8b99a4dd37997fc4aa497658b8e4d83f09136a25d56d1a64ee8c3","start":961}],"frontier_sha256":"448c20b39be4025f774a224e7135c982ee08362c6a2b2a663fba2bf493a45bbe","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","source_executed":false,"unresolved_dependency_count":0,"version":"GATE4_API_CONTEXT_PREDIAG_DEPENDENCY_CLOSURE_V1"}
```

## Strict boundary

This audit inventories dependencies only inside the already-frozen persisted api/context.js frontier. It does not classify any new api/context.js static item. Both embedded module dependencies are bound to completed child-state authorities. No completed child source is reread, no parent is resumed, no JavaScript is executed, the OTEL authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
