# Cursor OTEL Gate-4 diag.js completed global-utils reuse authorization

Date: 2026-09-15

## Status

- Audit status: PASS
- Dependency reuse authorized: YES
- Dependency source read required: NO
- Dependency source execution authorized: NO
- OTEL authority mutation authorized: NO

## Frozen diag dependency frontier

- Third-item document SHA256: `593eb5384c3796c92c56840673c7927c0fd9f56ff127016375c616ddf54190af`
- Third-item evidence SHA256: `6b7e6699a9660dae01c625b778e57df5b421f5167b68148c54bbc7d189cb7c8a`
- Third-row SHA256: `41c1745b022074c1e7539b8a51e9d28f9926a073f3e729d1aa70a9594773e8b0`
- Binding: `r`
- Dependency module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js`
- Resume boundary: `DECLARATOR_COMMA`
- Resume offset: 158

## Existing completed dependency authority

- Current global-utils state references: 12
- Completed global-utils references: 7
- Authoritative completed-state matches: 6
- Completed state SHA256: `f4b8f19271c054b83809afc2908a394a4d33457988d2cef6c54e4013a3b3a929`
- Body SHA256: `4da695f610511146f91f5bd69f7137d3671407375cbbdfcf9d65400ac5820a16`

## Reuse contract

- Contract SHA256: `a493f7db7dab5b287e11d750663a0d126e51e3de7fa7fce42cb784a4911ed617`

```json
{"api_context_items_advanced":0,"authority_mutation_authorized":false,"completed_dependency_state_sha256":"f4b8f19271c054b83809afc2908a394a4d33457988d2cef6c54e4013a3b3a929","dependency_body_sha256":"4da695f610511146f91f5bd69f7137d3671407375cbbdfcf9d65400ac5820a16","dependency_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js","dependency_source_read_authorized":false,"diag_dependency_binding":"r","diag_dependency_row_sha256":"41c1745b022074c1e7539b8a51e9d28f9926a073f3e729d1aa70a9594773e8b0","diag_dependency_source_sha256":"34199cab9401f5023274f51372433f3101e365698bd55552834b76e0cd47d186","diag_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","diag_resume_boundary_kind":"DECLARATOR_COMMA","diag_resume_offset":158,"execution_authorized":false,"next_gate":"DIAG_NEXT_DECLARATOR_STATIC_QUALIFICATION","reuse_authorized":true,"version":"GATE4_DIAG_GLOBAL_UTILS_COMPLETED_REUSE_CONTRACT_V1"}
```

## Evidence

Evidence SHA256: `a950f49835eefb7f0b106a836b23d314b514e0aebb1c1cdb98a2bc759d1626b8`

```json
{"authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","completed_global_utils_match_count":6,"completed_global_utils_paths":["$.otel.leaf_frontier.leaf.dependency.result","$.otel.result.dependency.result.dependency.result.dependency.result","$.recursive_modules.../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js.dependency.result","$.recursive_modules.../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js.dependency.result.dependency.result","$.recursive_modules.../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js","$.recursive_modules.../context/dist/otel.js.dependency.result.dependency.result.dependency.result"],"completed_global_utils_state_sha256":"f4b8f19271c054b83809afc2908a394a4d33457988d2cef6c54e4013a3b3a929","completed_state_shas":["31de44f1ad75d37e58713527f7aed71d15fa7ac2af4bf2ce641c093019d1a945","f4b8f19271c054b83809afc2908a394a4d33457988d2cef6c54e4013a3b3a929"],"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","diag_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","global_utils_body_sha256":"4da695f610511146f91f5bd69f7137d3671407375cbbdfcf9d65400ac5820a16","global_utils_incomplete_state_count":0,"global_utils_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js","global_utils_record_sha256":"ac0b3280fe5d4e8debe9f330dcc16138422565b618e96bf08a505cace837cc72","global_utils_record_sha_mentions":[],"global_utils_state_count":12,"reuse_authorized":true,"reuse_contract":{"api_context_items_advanced":0,"authority_mutation_authorized":false,"completed_dependency_state_sha256":"f4b8f19271c054b83809afc2908a394a4d33457988d2cef6c54e4013a3b3a929","dependency_body_sha256":"4da695f610511146f91f5bd69f7137d3671407375cbbdfcf9d65400ac5820a16","dependency_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js","dependency_source_read_authorized":false,"diag_dependency_binding":"r","diag_dependency_row_sha256":"41c1745b022074c1e7539b8a51e9d28f9926a073f3e729d1aa70a9594773e8b0","diag_dependency_source_sha256":"34199cab9401f5023274f51372433f3101e365698bd55552834b76e0cd47d186","diag_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","diag_resume_boundary_kind":"DECLARATOR_COMMA","diag_resume_offset":158,"execution_authorized":false,"next_gate":"DIAG_NEXT_DECLARATOR_STATIC_QUALIFICATION","reuse_authorized":true,"version":"GATE4_DIAG_GLOBAL_UTILS_COMPLETED_REUSE_CONTRACT_V1"},"reuse_contract_sha256":"a493f7db7dab5b287e11d750663a0d126e51e3de7fa7fce42cb784a4911ed617","source_read_performed":false,"third_item_document_sha256":"593eb5384c3796c92c56840673c7927c0fd9f56ff127016375c616ddf54190af","third_item_evidence_sha256":"6b7e6699a9660dae01c625b778e57df5b421f5167b68148c54bbc7d189cb7c8a","third_row_sha256":"41c1745b022074c1e7539b8a51e9d28f9926a073f3e729d1aa70a9594773e8b0","version":"GATE4_DIAG_GLOBAL_UTILS_COMPLETED_REUSE_AUTHORIZATION_V1"}
```

## Strict boundary

The already-completed global-utils state is reused as dependency qualification evidence. No global-utils source is reread. No diag.js declarator after the dependency boundary is classified by this gate. No JavaScript is executed and the OTEL authority is not mutated.
