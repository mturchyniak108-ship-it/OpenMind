# Cursor OTEL Gate-4 OTEL parent first bounded resume item

Date: 2026-09-15

## Status

- Classification status: PASS
- Parent module: `../context/dist/otel.js`
- Completed child: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js`
- Exactly one resumed item classified: YES
- Additional item classified: NO
- Source executed: NO

## Frozen OTEL parent body

- Body chars: 2607
- Body SHA256: `0475d054c3ecdefffcc7f90efe9e757e3078514760baffcd0ed872e6b8452a45`
- Bundle record SHA256: `08c141e7da13cc4b8240145885e7dd196ebf82065cdfbc70fcf5a130a28aac66`

## Resumed item

- Classification mode: `DIRECT_FROZEN_NEXT_SOURCE`
- Span: 242:355
- Source SHA256: `86cb265e85145d363fa39e97ef8f5d24e17d945881cdb4dafb740fe701a5708d`
- Boundary: `DECLARATOR_COMMA`
- Body end reached: NO
- Completed child state SHA256: `818323b07b3af43330ca263580e0842ae7e82c7771c7b05441442c637ddb743a`
- Row SHA256: `3b78888df470ad30fa9c7d9584153cf09d376b41d1969459d2313069d6c06e83`

## Classification evidence

Evidence SHA256: `5c3b89a6088b350e03bedf0cbb1c5f7903d7cb0485978d995ba685f93670f2f9`

```json
{"body_chars":2607,"body_sha256":"0475d054c3ecdefffcc7f90efe9e757e3078514760baffcd0ed872e6b8452a45","bundle_record_end":4054094,"bundle_record_sha256":"08c141e7da13cc4b8240145885e7dd196ebf82065cdfbc70fcf5a130a28aac66","bundle_record_start":4051453,"child_completed_state_sha256":"818323b07b3af43330ca263580e0842ae7e82c7771c7b05441442c637ddb743a","classification_count_this_gate":1,"completed_child_source_reread":false,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","frozen_metadata_source_candidates":[{"field":"next_source","json_path":"$","source":"s=n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js\")","source_sha256":"86cb265e85145d363fa39e97ef8f5d24e17d945881cdb4dafb740fe701a5708d"}],"module":"../context/dist/otel.js","next_additional_item_classified":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","parent_return_evidence_sha256":"9cd9eac9d27c49c8bf31092fbd2179ad7572b1cb2cadac9cafacbac95e3152ed","parent_state_sha256":"138d9a73153af3f7d606022cc7e1b537a4e87c0d0656303854f24627f0c05c6a","resumed_item":{"binding":"s","body_end_reached":false,"boundary_kind":"DECLARATOR_COMMA","classification_mode":"DIRECT_FROZEN_NEXT_SOURCE","completed_dependency_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","completed_dependency_state_sha256":"818323b07b3af43330ca263580e0842ae7e82c7771c7b05441442c637ddb743a","declaration_prefix":null,"dependency_end":355,"dependency_start":244,"end":355,"initializer_present":true,"kind":"STATIC_OTEL_PARENT_ITEM_WITH_COMPLETED_DEPENDENCY","source":"s=n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js\")","source_sha256":"86cb265e85145d363fa39e97ef8f5d24e17d945881cdb4dafb740fe701a5708d","start":242},"resumed_item_sha256":"3b78888df470ad30fa9c7d9584153cf09d376b41d1969459d2313069d6c06e83","source_executed":false,"version":"GATE4_OTEL_PARENT_FIRST_RESUME_ITEM_V1"}
```

## Strict boundary

This gate classifies exactly one OTEL parent item after the authorized return from completed context-api.js. No second OTEL item is classified. The completed child source is not reread. No JavaScript is executed, the frozen OTEL authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
