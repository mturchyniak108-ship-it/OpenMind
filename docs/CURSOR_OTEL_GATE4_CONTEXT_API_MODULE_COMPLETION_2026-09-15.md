# Cursor OTEL Gate-4 context-api module completion

Date: 2026-09-15

## Status

- Audit status: PASS
- Module completion qualified: YES
- Exact body coverage: 0:163
- Exact body reconstruction: YES
- Dependency count: 1
- Unresolved dependency count: 0
- Parent return attempted: NO

## Frozen historical prefix

- Prefix span: 0:34
- Prefix SHA256: `34551a32aaa2e4aceb621b39acf327b5038f603fc62ae7f589d019d101fcab36`
- Directive SHA256: `4ee188e1744c19816e95a540b2650ed9f033ea0371e74eac8e717355cfca8741`
- Export getter SHA256: `38e69e08f3d923913fbe7f0c482e07788467071f39fe390b4e2acf30aafb3e2a`
- Parent state SHA256: `3d759e6436d9fd61555b422c8d570136021e08f699a09a990f15096f176ea112`

## Qualified body-end item

- Item span: 34:163
- Item source SHA256: `8ccb12417cbe3e59c4ad43a893f83c13c0d5edb912d4c493d1af3526cf6cd469`
- Item row SHA256: `bfc3f4428f9e3f9430c580852df5e864995e9451fb3cbd84a9a1f75ddf898464`
- Resume evidence SHA256: `134be84ec4441916fc7a6e1efd6b801a7aa20484f40d42fcc7bacbe33b31a88b`

## Completed dependency

- api/context.js completed state SHA256: `fada3ecb5ce3e16fb2da60c54a312af1bc98dc3ad1339e50e8788c336739d215`
- Completed dependency set SHA256: `6770d7d869bb68420d8f3194d6c11cbcafd4f082a6a9d636ec3ab37e37f9eaf1`

## Completed context-api state

- Coverage SHA256: `ed99022bb727ee076a01e88e75ae705ed8a764f8212677e23abfda4843fdde35`
- Completed state SHA256: `818323b07b3af43330ca263580e0842ae7e82c7771c7b05441442c637ddb743a`

```json
{"body_chars":163,"body_sha256":"8f021ccd0e4e6de42936447534e5812dd24285ade731280775a395c495caed62","completed":true,"completed_dependency_set_sha256":"6770d7d869bb68420d8f3194d6c11cbcafd4f082a6a9d636ec3ab37e37f9eaf1","coverage_end":163,"coverage_sha256":"ed99022bb727ee076a01e88e75ae705ed8a764f8212677e23abfda4843fdde35","coverage_start":0,"dependency_count":1,"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","module_record_sha256":"0d49f06e85641e3559a1c41cb9bdbe4c8df86a622f96392f37738fbcd388a376","resume_item_evidence_sha256":"134be84ec4441916fc7a6e1efd6b801a7aa20484f40d42fcc7bacbe33b31a88b","unresolved_dependency_count":0,"version":"GATE4_CONTEXT_API_COMPLETED_STATE_V1"}
```

## Completion evidence

Evidence SHA256: `279929899b0f862fbc92a27a51bbb3140031a877df02928e6ae3871e4df3fda5`

```json
{"body_reconstruction_equal":true,"body_reconstruction_sha256":"8f021ccd0e4e6de42936447534e5812dd24285ade731280775a395c495caed62","completed_dependencies":[{"binding":"r","completed_state_sha256":"fada3ecb5ce3e16fb2da60c54a312af1bc98dc3ad1339e50e8788c336739d215","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","source_sha256":"8ccb12417cbe3e59c4ad43a893f83c13c0d5edb912d4c493d1af3526cf6cd469"}],"completed_dependency_set_sha256":"6770d7d869bb68420d8f3194d6c11cbcafd4f082a6a9d636ec3ab37e37f9eaf1","completed_state":{"body_chars":163,"body_sha256":"8f021ccd0e4e6de42936447534e5812dd24285ade731280775a395c495caed62","completed":true,"completed_dependency_set_sha256":"6770d7d869bb68420d8f3194d6c11cbcafd4f082a6a9d636ec3ab37e37f9eaf1","coverage_end":163,"coverage_sha256":"ed99022bb727ee076a01e88e75ae705ed8a764f8212677e23abfda4843fdde35","coverage_start":0,"dependency_count":1,"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","module_record_sha256":"0d49f06e85641e3559a1c41cb9bdbe4c8df86a622f96392f37738fbcd388a376","resume_item_evidence_sha256":"134be84ec4441916fc7a6e1efd6b801a7aa20484f40d42fcc7bacbe33b31a88b","unresolved_dependency_count":0,"version":"GATE4_CONTEXT_API_COMPLETED_STATE_V1"},"completed_state_sha256":"818323b07b3af43330ca263580e0842ae7e82c7771c7b05441442c637ddb743a","coverage_segments":[{"end":12,"kind":"FROZEN_HISTORICAL_DIRECTIVE","sha256":"4ee188e1744c19816e95a540b2650ed9f033ea0371e74eac8e717355cfca8741","start":0},{"end":13,"kind":"STRUCTURAL_SEMICOLON","sha256":"41b805ea7ac014e23556e98bb374702a08344268f92489a02f0880849394a1e4","start":12},{"end":29,"kind":"FROZEN_HISTORICAL_EXPORT_GETTER","sha256":"38e69e08f3d923913fbe7f0c482e07788467071f39fe390b4e2acf30aafb3e2a","start":13},{"end":30,"kind":"STRUCTURAL_SEMICOLON","sha256":"41b805ea7ac014e23556e98bb374702a08344268f92489a02f0880849394a1e4","start":29},{"end":34,"kind":"STRUCTURAL_VAR_PREFIX","sha256":"092090833731ec177e11c0f921ac9e0592e13aa6b6fcb5ad751246ee46fe8014","start":30},{"end":163,"kind":"QUALIFIED_BODY_END_BINDING","row_sha256":"bfc3f4428f9e3f9430c580852df5e864995e9451fb3cbd84a9a1f75ddf898464","sha256":"8ccb12417cbe3e59c4ad43a893f83c13c0d5edb912d4c493d1af3526cf6cd469","start":34}],"coverage_sha256":"ed99022bb727ee076a01e88e75ae705ed8a764f8212677e23abfda4843fdde35","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","historical_prefix_authority":{"directive_paths":["$.dependency.result.dependency.result.rows[0].source","$.dependency.result.rows[0].source","$.rows[0].source"],"export_getter_paths":["$.rows[1].source"],"parent_state_sha256":"3d759e6436d9fd61555b422c8d570136021e08f699a09a990f15096f176ea112","prefix_sha256":"34551a32aaa2e4aceb621b39acf327b5038f603fc62ae7f589d019d101fcab36"},"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","next_parent_advanced":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","resume_item_evidence_sha256":"134be84ec4441916fc7a6e1efd6b801a7aa20484f40d42fcc7bacbe33b31a88b","source_executed":false,"unresolved_dependency_count":0,"version":"GATE4_CONTEXT_API_MODULE_COMPLETION_V1"}
```

## Strict boundary

This audit completes only context-api.js. The frozen historical directive and export-getter prefix are bound through the frozen parent metadata state, and the already-qualified resumed binding reaches the exact module body end. The completed api/context.js child source is not reread. No return to the next parent is performed. No JavaScript is executed, the OTEL authority is not mutated, Gate 5 is not evaluated, Cursor is not run, and no Git push is performed.
