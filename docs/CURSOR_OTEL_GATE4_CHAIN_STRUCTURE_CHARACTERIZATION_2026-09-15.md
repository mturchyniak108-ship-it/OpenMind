# Cursor OTEL Gate-4 exact chain structure characterization

Date: 2026-09-15

## Status

- Audit status: PASS
- OTEL authority JSON mutated: NO
- Module source read: NO
- Gate 5 evaluated: NO
- Cursor executed: NO

## Failed transaction assumption

The prior atomic transaction incorrectly required the raw chain to equal a three-string list.
The qualified invariant is the module traversal sequence, not raw object equality.

## Exact chain

- Chain type: `list`
- Top-level length: 4
- Chain SHA256: `d72811f8e9e4586c2c09b38809693a67a696e66b3191178aba08f33963f1f23d`
- Module traversal: `["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js"]`
- Top-level module sequences: `[[],["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js"],["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js"],["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js"]]`

## Structural contraction

- Mode: `REMOVE_FINAL_TOP_LEVEL_CHAIN_ITEM`
- Structurally ready: YES
- Final top-level item contains only global-utils: YES
- Previous top-level item contains api/context.js: YES

## Evidence

Evidence SHA256: `aa8344a360bd05d14a671bf0a78bb44ac306d30457cf497a53346c8ac59631dd`

```json
{"authority_sha256":"9e0db7a5b036a96571530cec0a573f64daa24c6cad038dcf1d789222730ac2d4","chain_canonical_json":["../context/dist/otel.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js"],"chain_sha256":"d72811f8e9e4586c2c09b38809693a67a696e66b3191178aba08f33963f1f23d","chain_top_level_length":4,"chain_type":"list","final_top_level_index":3,"final_top_level_is_global_only":true,"global_utils_occurrences":[{"kind":"STRING","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js","path":"$[3]"}],"module_occurrences":[{"kind":"STRING","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","path":"$[1]"},{"kind":"STRING","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","path":"$[2]"},{"kind":"STRING","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js","path":"$[3]"}],"module_sequence":["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js"],"previous_top_level_contains_api_context":true,"structural_contraction_mode":"REMOVE_FINAL_TOP_LEVEL_CHAIN_ITEM","structural_contraction_ready":true,"top_level_items":[{"canonical_sha256":"81d3a62862674e02e6c1fb7a4f16d712ea1ad977e9a02095a92665a47ea0e0a0","index":0,"module_occurrence_count":0,"module_sequence":[],"type":"str","value":"../context/dist/otel.js"},{"canonical_sha256":"ef318f8e2acf972aa4a20a18e78dc84c5e9291320714e59de0856f3a3f50053f","index":1,"module_occurrence_count":1,"module_sequence":["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js"],"type":"str","value":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js"},{"canonical_sha256":"12352a3bfe22aea00fc8b25f9d959c48d1c7709c1de7d5cc2c42c37d2fa346ab","index":2,"module_occurrence_count":1,"module_sequence":["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js"],"type":"str","value":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js"},{"canonical_sha256":"66292d8bf54e6c23194fd7665ccfb15d706942fbc4ea2259bc6210f5bf8ef684","index":3,"module_occurrence_count":1,"module_sequence":["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js"],"type":"str","value":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js"}],"top_level_module_sequences":[[],["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/context-api.js"],["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js"],["../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js"]],"version":"GATE4_OTEL_CHAIN_STRUCTURE_CHARACTERIZATION_V1"}
```

## Strict boundary

This audit characterizes only the chain data structure. It does not mutate the OTEL authority JSON, contract the chain, persist completion, read module source, evaluate Gate 5, or execute Cursor.
