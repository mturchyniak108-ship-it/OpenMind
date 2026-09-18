# Cursor OTEL Gate-4 context-api first bounded resume item

Date: 2026-09-15

## Status

- Classification status: PASS
- Parent module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js`
- Completed child: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js`
- Exactly one resumed item classified: YES
- Additional item classified: NO
- Source executed: NO

## Frozen parent body

- Body chars: 163
- Body SHA256: `8f021ccd0e4e6de42936447534e5812dd24285ade731280775a395c495caed62`
- Bundle record SHA256: `0d49f06e85641e3559a1c41cb9bdbe4c8df86a622f96392f37738fbcd388a376`

## Resumed item

- Binding: `r`
- Span: 34:163
- Source SHA256: `8ccb12417cbe3e59c4ad43a893f83c13c0d5edb912d4c493d1af3526cf6cd469`
- Boundary: `DECLARATION_BODY_END`
- Body end reached: YES
- Completed child state SHA256: `fada3ecb5ce3e16fb2da60c54a312af1bc98dc3ad1339e50e8788c336739d215`
- Row SHA256: `bfc3f4428f9e3f9430c580852df5e864995e9451fb3cbd84a9a1f75ddf898464`

## Classification evidence

Evidence SHA256: `134be84ec4441916fc7a6e1efd6b801a7aa20484f40d42fcc7bacbe33b31a88b`

```json
{"body_chars":163,"body_sha256":"8f021ccd0e4e6de42936447534e5812dd24285ade731280775a395c495caed62","bundle_record_end":9918,"bundle_record_sha256":"0d49f06e85641e3559a1c41cb9bdbe4c8df86a622f96392f37738fbcd388a376","bundle_record_start":9638,"child_completed_state_sha256":"fada3ecb5ce3e16fb2da60c54a312af1bc98dc3ad1339e50e8788c336739d215","classification_count_this_gate":1,"completed_child_source_reread":false,"cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","historical_dependency_object":{"json_path":"$.dependency","object_sha256":"1ddcc9726d14957a21656173cf9fce0c8ae530789f0f0bf25262112aa3657b82"},"historical_source_matches":[{"field":"next_source","json_path":"$","object_sha256":"3d759e6436d9fd61555b422c8d570136021e08f699a09a990f15096f176ea112"}],"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","next_additional_item_classified":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","parent_return_evidence_sha256":"e21a6dcbb88cf746d84228ec2c03ff34deb7fbdb86fb46d1dc91a49f6aafb8a0","parent_state_sha256":"3d759e6436d9fd61555b422c8d570136021e08f699a09a990f15096f176ea112","resumed_item":{"binding":"r","body_end_reached":true,"boundary_kind":"DECLARATION_BODY_END","completed_dependency_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","completed_dependency_state_sha256":"fada3ecb5ce3e16fb2da60c54a312af1bc98dc3ad1339e50e8788c336739d215","declaration_prefix":"var","dependency_end":147,"dependency_start":36,"end":163,"initializer_present":true,"kind":"STATIC_BINDING_WITH_COMPLETED_DEPENDENCY","source":"r=n(\"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js\")._.getInstance()","source_sha256":"8ccb12417cbe3e59c4ad43a893f83c13c0d5edb912d4c493d1af3526cf6cd469","start":34},"resumed_item_sha256":"bfc3f4428f9e3f9430c580852df5e864995e9451fb3cbd84a9a1f75ddf898464","source_executed":false,"version":"GATE4_CONTEXT_API_FIRST_RESUME_ITEM_V1"}
```

## Strict boundary

This gate classifies exactly one context-api.js parent item after the authorized return from completed api/context.js. No second parent item is classified. The completed child source is not reread. No JavaScript is executed, the OTEL authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
