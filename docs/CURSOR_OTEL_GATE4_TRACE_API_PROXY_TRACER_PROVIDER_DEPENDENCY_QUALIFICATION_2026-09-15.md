# Cursor OTEL Gate-4 ProxyTracerProvider dependency qualification

Date: 2026-09-15

## Status

- Qualification status: PASS
- Parent module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace-api.js`
- Parent binding: `s`
- Parent item span: 158:285
- Parent frontier remains: 285
- Dependency module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracerProvider.js`
- Qualification mode: `AUTHORITY_ABSENCE_BOUNDED_CHILD_SOURCE_READ_AUTHORIZED`
- Dependency source body extracted: NO
- Dependency source executed: NO
- trace-api frontier advanced: NO
- OTEL frontier remains: 467

## Qualification contract

- Contract SHA256: `f6ecf9bf83ca3813914d89dfd0d2a21a0052d236c5245ce406629983216122c1`

```json
{"child_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracerProvider.js","child_source_read_authorized_after_this_gate":true,"completed_state_sha256":null,"dependency_source_sha256":"5bc87e6f38ec7113d674186f752d7760093a788261dd58ec6cd49c2155897784","direct_authority_state_count":0,"exact_authority_string_reference_count":0,"incomplete_authority_state_count":0,"module_header_end":27398,"module_header_sha256":"957524f80432d9ba845eeb9a0c6b0a837e0275445a8febb2de7fe8fea3b8aa79","module_header_start":27268,"otel_frontier_end":467,"otel_frontier_resume_authorized":false,"qualification_mode":"AUTHORITY_ABSENCE_BOUNDED_CHILD_SOURCE_READ_AUTHORIZED","source_execution_authorized":false,"trace_api_binding":"s","trace_api_frontier_end":285,"trace_api_frontier_resume_authorized_after_this_gate":false,"trace_api_item_evidence_sha256":"055c0b34ab678f8ddabb94651c6ecd05cb2fc93877712f31ee9b298cd59abc1c","trace_api_item_row_sha256":"11875e5b0710b761165a15d6f1e364e2398d351da447c60e598c81674c9816ab","version":"GATE4_PROXY_TRACER_PROVIDER_DEPENDENCY_QUALIFICATION_V1"}
```

## Qualification evidence

Evidence SHA256: `16d01b36acc073c224af8e9f2bfaad9040cc27773757ba0dca0c0e5cc47a96a7`

```json
{"authority_state_summary":[],"completed_authority_state_count":0,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","dependency_source_opened":false,"embedded_authority_string_paths":[],"exact_authority_string_paths":[],"module_header_occurrence_count":1,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","qualification_contract":{"child_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracerProvider.js","child_source_read_authorized_after_this_gate":true,"completed_state_sha256":null,"dependency_source_sha256":"5bc87e6f38ec7113d674186f752d7760093a788261dd58ec6cd49c2155897784","direct_authority_state_count":0,"exact_authority_string_reference_count":0,"incomplete_authority_state_count":0,"module_header_end":27398,"module_header_sha256":"957524f80432d9ba845eeb9a0c6b0a837e0275445a8febb2de7fe8fea3b8aa79","module_header_start":27268,"otel_frontier_end":467,"otel_frontier_resume_authorized":false,"qualification_mode":"AUTHORITY_ABSENCE_BOUNDED_CHILD_SOURCE_READ_AUTHORIZED","source_execution_authorized":false,"trace_api_binding":"s","trace_api_frontier_end":285,"trace_api_frontier_resume_authorized_after_this_gate":false,"trace_api_item_evidence_sha256":"055c0b34ab678f8ddabb94651c6ecd05cb2fc93877712f31ee9b298cd59abc1c","trace_api_item_row_sha256":"11875e5b0710b761165a15d6f1e364e2398d351da447c60e598c81674c9816ab","version":"GATE4_PROXY_TRACER_PROVIDER_DEPENDENCY_QUALIFICATION_V1"},"qualification_contract_sha256":"f6ecf9bf83ca3813914d89dfd0d2a21a0052d236c5245ce406629983216122c1","source_executed":false,"trace_api_frontier_end":285,"trace_api_item_evidence_sha256":"055c0b34ab678f8ddabb94651c6ecd05cb2fc93877712f31ee9b298cd59abc1c","trace_api_item_row_sha256":"11875e5b0710b761165a15d6f1e364e2398d351da447c60e598c81674c9816ab","version":"GATE4_PROXY_TRACER_PROVIDER_DEPENDENCY_QUALIFICATION_EVIDENCE_V1"}
```

## Next authorized action

Statically read only the uniquely authorized ProxyTracerProvider.js webpack module record, determine its exact body boundary, and classify exactly its first eligible item.

## Strict boundary

This gate qualifies only the ProxyTracerProvider.js dependency introduced by the trace-api.js s declarator. No ProxyTracerProvider.js module body is extracted or classified in this gate. No further trace-api.js item is classified. trace-api.js completion is not claimed. No trace-api.js parent return is attempted. OTEL remains frozen at offset 467. No source is executed, the frozen authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
