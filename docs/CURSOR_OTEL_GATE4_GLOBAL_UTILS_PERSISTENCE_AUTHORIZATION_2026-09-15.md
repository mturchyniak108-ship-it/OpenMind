# Cursor OTEL Gate-4 global-utils persistence authorization

Date: 2026-09-15

## Status

- Audit status: PASS
- Persistence authorization: `NOT_AUTHORIZED_REFERENCE_PROPAGATION_UNRESOLVED`
- Completion persisted: NO
- OTEL authority JSON mutated: NO
- Next module read: NO
- Gate 5 evaluated: NO
- Cursor executed: NO

## Frozen completion authorities

- Initialized mapping SHA256: `978d80437883468abcae3e2db253d73bf2f5ecec792c0f16ba0ff65d66f9bd0b`
- Dual-representation contract SHA256: `7e961379694c133a42d64c4af4bd4f2232f43e616301d7acb3f6ce1124749c91`
- Proposed summary state SHA256: `31de44f1ad75d37e58713527f7aed71d15fa7ac2af4bf2ce641c093019d1a945`
- Proposed recursive state SHA256: `f4b8f19271c054b83809afc2908a394a4d33457988d2cef6c54e4013a3b3a929`
- Completion-state evidence SHA256: `ae914b7644b9ab937bbc8e58609d53a034af5e06d04a3e1cdfd43fb75d955634`
- Twelve-row sequence SHA256: `79294f5863f7bb3c4617e77e8bb87bbc395064071c856be3f5a97c423d1aff73`

## Current persistence topology

- Summary targets: 1
- Incomplete recursive references: 6
- Wrapper references: 4
- Leaf-frontier references: 1
- Dependency-result references: 4

## Historical persistence precedent

- Qualification JSON files seen: 966
- Qualification JSON files parsed: 958
- JSON parse failures: 8
- Completed summary plus recursive snapshots: 2
- Completed recursive_modules snapshots: 2
- Completed dependency-result snapshots: 0
- Completed leaf-frontier snapshots: 0

## Adjudication

- Exact reference replacement supported: NO
- Completed leaf persistence supported: NO
- Persistence authorization ready: NO

Unresolved reason:

historical completed dependency-result reference propagation was not recovered

## Authorization evidence

Evidence SHA256: `c67d8ea8746e2c5ec12eea1d5dff5b919990e108bffac9c4a56efc1f1d5082c4`

```json
{"authorization_ready":false,"authorization_status":"NOT_AUTHORIZED_REFERENCE_PROPAGATION_UNRESOLVED","completion_state_evidence_sha256":"ae914b7644b9ab937bbc8e58609d53a034af5e06d04a3e1cdfd43fb75d955634","current_global_utils":{"body_sha256":"4da695f610511146f91f5bd69f7137d3671407375cbbdfcf9d65400ac5820a16","incomplete_recursive_sha256":"03bfd5102bfa0096391e4d3b9cccb3f0cc3b403e44db6c6adfb59f91bc080519","incomplete_summary_sha256":"fb5886defad7ac69a728a9f405a4933ec048b5b5bba07649c112066aec4bcb7b","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js","wrapper_sha256":"6d475c1613300ae02befeb2e53e951db807aed8bc1503846734c983c0e17eec9"},"historical_precedent":{"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context/context.js":{"completed_dependency_result_snapshots":0,"completed_leaf_frontier_snapshots":0,"completed_recursive_module_snapshots":1,"completed_summary_and_recursive_snapshots":1,"files":[{"dependency_result":false,"leaf_frontier":false,"path":"otel-context-manager-factory-gsv2/20260914T071124/cursor_otel_context_manager_factory_gsv2.json","recursive_modules":true,"recursive_ref_count":1,"summary_ref_count":1}]},"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/span_kind.js":{"completed_dependency_result_snapshots":0,"completed_leaf_frontier_snapshots":0,"completed_recursive_module_snapshots":1,"completed_summary_and_recursive_snapshots":1,"files":[{"dependency_result":false,"leaf_frontier":false,"path":"otel-context-manager-factory-gsv2/20260914T071124/cursor_otel_context_manager_factory_gsv2.json","recursive_modules":true,"recursive_ref_count":1,"summary_ref_count":1}]}},"historical_snapshot_counts":{"completed_dependency_result_snapshots":0,"completed_leaf_frontier_snapshots":0,"completed_recursive_module_snapshots":2,"completed_summary_and_recursive_snapshots":2,"json_failures":8,"json_files_parsed":958,"json_files_seen":966},"mutation_targets":{"incomplete_recursive_reference_count":6,"incomplete_recursive_reference_paths":["otel.leaf_frontier.leaf","otel.result.dependency.result.dependency.result.dependency.result","recursive_modules.../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js.dependency.result","recursive_modules.../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js.dependency.result.dependency.result","recursive_modules.../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js","recursive_modules.../context/dist/otel.js.dependency.result.dependency.result.dependency.result"],"leaf_frontier_reference_count":1,"leaf_frontier_reference_paths":["otel.leaf_frontier.leaf"],"summary_reference_count":1,"summary_reference_paths":["module_summary.[2]"],"wrapper_reference_count":4,"wrapper_reference_paths":["otel.result.dependency.result.dependency.result.dependency","recursive_modules.../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js.dependency","recursive_modules.../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js.dependency.result.dependency","recursive_modules.../context/dist/otel.js.dependency.result.dependency.result.dependency"]},"proposed_recursive_state_sha256":"f4b8f19271c054b83809afc2908a394a4d33457988d2cef6c54e4013a3b3a929","proposed_summary_state_sha256":"31de44f1ad75d37e58713527f7aed71d15fa7ac2af4bf2ce641c093019d1a945","twelve_row_sequence_sha256":"79294f5863f7bb3c4617e77e8bb87bbc395064071c856be3f5a97c423d1aff73","unresolved_reason":"historical completed dependency-result reference propagation was not recovered","version":"GATE4_GLOBAL_UTILS_PERSISTENCE_AUTHORIZATION_AUDIT_V1"}
```

## Strict boundary

This audit authorizes no OTEL authority mutation by itself. Any persistence mutation remains a separate fail-closed Gold Standard gate.
