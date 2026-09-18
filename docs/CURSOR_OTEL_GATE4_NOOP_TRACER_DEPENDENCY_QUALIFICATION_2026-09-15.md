# Cursor OTEL Gate-4 NoopTracer dependency qualification

Date: 2026-09-15

## Status

- Qualification status: PASS
- Parent module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/ProxyTracer.js`
- Parent binding: `r`
- Parent item span: 34:159
- Parent frontier remains: 159
- Dependency module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/NoopTracer.js`
- Qualification mode: `AUTHORITY_ABSENCE_BOUNDED_CHILD_SOURCE_READ_AUTHORIZED`
- Child source body extracted: NO
- Child source executed: NO
- ProxyTracer frontier advanced: NO
- ProxyTracerProvider frontier remains: 153
- trace-api frontier remains: 285
- OTEL frontier remains: 467

## Qualification contract

- Contract SHA256: `d6086688636e5df8afbd1cff66f979a18f9f16abd923cfd25339a7cc438182b8`

```json
{"child_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/NoopTracer.js","child_source_read_authorized_after_this_gate":true,"completed_state_sha256":null,"dependency_source_sha256":"c91ce49f655226cce76f0d124c824a6368eff86b7952c5b43b0cd18dd955d870","direct_authority_state_count":0,"embedded_authority_string_reference_count":0,"exact_authority_string_reference_count":0,"incomplete_authority_state_count":0,"module_header_end":25367,"module_header_sha256":"64c88229400e2cd171290d4b07fda2dda37ef62e343c33083302ff671659c72d","module_header_start":25246,"otel_frontier_end":467,"otel_frontier_resume_authorized":false,"provider_frontier_end":153,"provider_frontier_resume_authorized":false,"proxy_tracer_binding":"r","proxy_tracer_frontier_end":159,"proxy_tracer_frontier_resume_authorized_after_this_gate":false,"proxy_tracer_item_evidence_sha256":"967d85ef5e3942e3e6340c51dbef99d608789bc9619c7f7d5ecbc806b6bb2319","proxy_tracer_item_row_sha256":"ba63990a91042e934d6b8b6595933146a714114ecd51388f2cb28c96fc297931","qualification_mode":"AUTHORITY_ABSENCE_BOUNDED_CHILD_SOURCE_READ_AUTHORIZED","source_execution_authorized":false,"trace_api_frontier_end":285,"trace_api_frontier_resume_authorized":false,"version":"GATE4_NOOP_TRACER_DEPENDENCY_QUALIFICATION_V1"}
```

## Qualification evidence

Evidence SHA256: `c9b16fbf2e26896543313831985618b616169119c23ad346c3a9e446049a9513`

```json
{"authority_state_summary":[],"completed_authority_state_count":0,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","dependency_source_opened":false,"embedded_authority_string_paths":[],"exact_authority_string_paths":[],"module_header_occurrence_count":1,"noop_tracer_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/NoopTracer.js","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","provider_frontier_end":153,"proxy_tracer_frontier_end":159,"proxy_tracer_item_evidence_sha256":"967d85ef5e3942e3e6340c51dbef99d608789bc9619c7f7d5ecbc806b6bb2319","proxy_tracer_item_row_sha256":"ba63990a91042e934d6b8b6595933146a714114ecd51388f2cb28c96fc297931","qualification_contract":{"child_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/trace/NoopTracer.js","child_source_read_authorized_after_this_gate":true,"completed_state_sha256":null,"dependency_source_sha256":"c91ce49f655226cce76f0d124c824a6368eff86b7952c5b43b0cd18dd955d870","direct_authority_state_count":0,"embedded_authority_string_reference_count":0,"exact_authority_string_reference_count":0,"incomplete_authority_state_count":0,"module_header_end":25367,"module_header_sha256":"64c88229400e2cd171290d4b07fda2dda37ef62e343c33083302ff671659c72d","module_header_start":25246,"otel_frontier_end":467,"otel_frontier_resume_authorized":false,"provider_frontier_end":153,"provider_frontier_resume_authorized":false,"proxy_tracer_binding":"r","proxy_tracer_frontier_end":159,"proxy_tracer_frontier_resume_authorized_after_this_gate":false,"proxy_tracer_item_evidence_sha256":"967d85ef5e3942e3e6340c51dbef99d608789bc9619c7f7d5ecbc806b6bb2319","proxy_tracer_item_row_sha256":"ba63990a91042e934d6b8b6595933146a714114ecd51388f2cb28c96fc297931","qualification_mode":"AUTHORITY_ABSENCE_BOUNDED_CHILD_SOURCE_READ_AUTHORIZED","source_execution_authorized":false,"trace_api_frontier_end":285,"trace_api_frontier_resume_authorized":false,"version":"GATE4_NOOP_TRACER_DEPENDENCY_QUALIFICATION_V1"},"qualification_contract_sha256":"d6086688636e5df8afbd1cff66f979a18f9f16abd923cfd25339a7cc438182b8","source_executed":false,"trace_api_frontier_end":285,"version":"GATE4_NOOP_TRACER_DEPENDENCY_QUALIFICATION_EVIDENCE_V1"}
```

## Next authorized action

Statically read only the uniquely authorized NoopTracer.js webpack module record, determine its exact body boundary, and classify exactly its first eligible item.

## Strict boundary

This gate qualifies only the NoopTracer.js dependency introduced by the ProxyTracer.js r declarator. No NoopTracer.js module body is extracted or classified in this gate. No later ProxyTracer.js item is classified. ProxyTracer.js completion is not claimed. No return to ProxyTracerProvider.js is attempted. ProxyTracerProvider.js remains frozen at offset 153. trace-api.js remains frozen at offset 285. OTEL remains frozen at offset 467. No source is executed, the frozen authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
