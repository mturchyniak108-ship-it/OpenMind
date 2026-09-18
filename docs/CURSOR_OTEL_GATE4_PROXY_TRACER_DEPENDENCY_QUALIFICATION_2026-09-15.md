# Cursor OTEL Gate-4 ProxyTracer dependency qualification

Date: 2026-09-15

## Status

- Qualification status: PASS
- Parent module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracerProvider.js`
- Parent binding: `r`
- Parent item span: 34:153
- Parent frontier remains: 153
- Dependency module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracer.js`
- Qualification mode: `AUTHORITY_ABSENCE_BOUNDED_CHILD_SOURCE_READ_AUTHORIZED`
- Child source body extracted: NO
- Child source executed: NO
- ProxyTracerProvider frontier advanced: NO
- trace-api frontier remains: 285
- OTEL frontier remains: 467

## Qualification contract

- Contract SHA256: `d0f8a7abba092cdaf8236a922db3bd5f2d9eb310f804476e9dc82a0aea6a4dc2`

```json
{"child_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracer.js","child_source_read_authorized_after_this_gate":true,"completed_state_sha256":null,"dependency_source_sha256":"7e05893b091b8128d2b9f8ac668056119981fdf372a425461ed3339ae11a7943","direct_authority_state_count":0,"embedded_authority_string_reference_count":0,"exact_authority_string_reference_count":0,"incomplete_authority_state_count":0,"module_header_end":26603,"module_header_sha256":"8a2f3b0334f32474b32a36efa1f96b385ec5c76a62f631dd45aa8b289832fa5f","module_header_start":26481,"otel_frontier_end":467,"otel_frontier_resume_authorized":false,"provider_binding":"r","provider_frontier_end":153,"provider_frontier_resume_authorized_after_this_gate":false,"provider_item_evidence_sha256":"5eddbab60d8be1ef9a47633f011883cb6661e7c3f85b6d907563622ce5dfa330","provider_item_row_sha256":"7a9e30d3c8b71fc24cb24929111757d1f9274797b87713bcdfec4c013566fcf8","qualification_mode":"AUTHORITY_ABSENCE_BOUNDED_CHILD_SOURCE_READ_AUTHORIZED","source_execution_authorized":false,"trace_api_frontier_end":285,"trace_api_frontier_resume_authorized":false,"version":"GATE4_PROXY_TRACER_DEPENDENCY_QUALIFICATION_V1"}
```

## Qualification evidence

Evidence SHA256: `bd73ee49a82889dc8ed202345b556081c9064c4f02fe2a4c0798cf64f57e8471`

```json
{"authority_state_summary":[],"completed_authority_state_count":0,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","dependency_source_opened":false,"embedded_authority_string_paths":[],"exact_authority_string_paths":[],"module_header_occurrence_count":1,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","provider_frontier_end":153,"provider_item_evidence_sha256":"5eddbab60d8be1ef9a47633f011883cb6661e7c3f85b6d907563622ce5dfa330","provider_item_row_sha256":"7a9e30d3c8b71fc24cb24929111757d1f9274797b87713bcdfec4c013566fcf8","qualification_contract":{"child_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracer.js","child_source_read_authorized_after_this_gate":true,"completed_state_sha256":null,"dependency_source_sha256":"7e05893b091b8128d2b9f8ac668056119981fdf372a425461ed3339ae11a7943","direct_authority_state_count":0,"embedded_authority_string_reference_count":0,"exact_authority_string_reference_count":0,"incomplete_authority_state_count":0,"module_header_end":26603,"module_header_sha256":"8a2f3b0334f32474b32a36efa1f96b385ec5c76a62f631dd45aa8b289832fa5f","module_header_start":26481,"otel_frontier_end":467,"otel_frontier_resume_authorized":false,"provider_binding":"r","provider_frontier_end":153,"provider_frontier_resume_authorized_after_this_gate":false,"provider_item_evidence_sha256":"5eddbab60d8be1ef9a47633f011883cb6661e7c3f85b6d907563622ce5dfa330","provider_item_row_sha256":"7a9e30d3c8b71fc24cb24929111757d1f9274797b87713bcdfec4c013566fcf8","qualification_mode":"AUTHORITY_ABSENCE_BOUNDED_CHILD_SOURCE_READ_AUTHORIZED","source_execution_authorized":false,"trace_api_frontier_end":285,"trace_api_frontier_resume_authorized":false,"version":"GATE4_PROXY_TRACER_DEPENDENCY_QUALIFICATION_V1"},"qualification_contract_sha256":"d0f8a7abba092cdaf8236a922db3bd5f2d9eb310f804476e9dc82a0aea6a4dc2","source_executed":false,"trace_api_frontier_end":285,"version":"GATE4_PROXY_TRACER_DEPENDENCY_QUALIFICATION_EVIDENCE_V1"}
```

## Next authorized action

Statically read only the uniquely authorized ProxyTracer.js webpack module record, determine its exact body boundary, and classify exactly its first eligible item.

## Strict boundary

This gate qualifies only the ProxyTracer.js dependency introduced by the ProxyTracerProvider.js r declarator. No ProxyTracer.js module body is extracted or classified in this gate. No later ProxyTracerProvider.js item is classified. ProxyTracerProvider.js completion is not claimed. No return to trace-api.js is attempted. trace-api.js remains frozen at offset 285. OTEL remains frozen at offset 467. No source is executed, the frozen authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
