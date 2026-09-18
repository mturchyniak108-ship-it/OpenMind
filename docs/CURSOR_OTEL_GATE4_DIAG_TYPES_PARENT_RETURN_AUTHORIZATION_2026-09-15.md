# Cursor OTEL Gate-4 diag types parent-return authorization

Date: 2026-09-15

## Status

- Audit status: PASS
- Authorization status: `AUTHORIZED_RETURN_TO_DIAG_PARENT_FRONTIER_ONLY`
- Parent resume eligibility authorized: YES
- Next parent item classification authorized: NO
- Child source reread authorized: NO
- Source execution authorized: NO
- OTEL authority mutation authorized: NO

## Frozen parent dependency

- Parent module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js`
- Parent row-6 document SHA256: `b7367aef767b58ab8d9fcf639bbd37e9717751643b0555578961c497a2f6c582`
- Parent row-6 evidence SHA256: `655802c6fa57fd6944ccbd1afbf7ae1d87d796121faad8dc1c5f8e639bf63492`
- Parent row-6 SHA256: `94a35d9d4773eb333ec435b0ea231cb2f9372ec9675f75e555da7a41c33ddf04`
- Parent dependency binding: `o`
- Dependency module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js`
- Parent row-6 boundary: `DECLARATOR_COMMA`
- Parent row-6 terminator: 1546
- Parent resume offset: 1547

## Completed child dependency

- Completion document SHA256: `b8092cc5d766d2709a735ead8e86b773f36ed2632e3182c09a2c990ef4c1cc82`
- Completion evidence SHA256: `08ba802129f786630a30228fd6411703d3758e20acd230e1d8a3a5c3ce60e299`
- Completed state SHA256: `33bf91f35c636521e2cf73072c2970094b86adf7d784b5ef67a6d51b9ea61a23`
- Frozen rows: 3
- Dependency frontier count: 0
- Coverage: 0:208
- Body SHA256: `659fc768c54e343ad1e4c74982b0774bdc59272f00b32be2617ef1428d03048f`

## Parent-return contract

- Contract SHA256: `8bdbc7ca8c954d8f660721cc9773a50b1c74de71026e3bb6ccb543e3efad4621`

```json
{"authority_mutation_authorized":false,"child_completed_state_sha256":"33bf91f35c636521e2cf73072c2970094b86adf7d784b5ef67a6d51b9ea61a23","child_completion_document_sha256":"b8092cc5d766d2709a735ead8e86b773f36ed2632e3182c09a2c990ef4c1cc82","child_completion_evidence_sha256":"08ba802129f786630a30228fd6411703d3758e20acd230e1d8a3a5c3ce60e299","child_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","child_source_reread_authorized":false,"next_parent_item_classification_authorized":false,"parent_dependency_binding":"o","parent_dependency_row_sha256":"94a35d9d4773eb333ec435b0ea231cb2f9372ec9675f75e555da7a41c33ddf04","parent_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","parent_resume_eligibility_authorized":true,"parent_resume_offset":1547,"source_execution_authorized":false,"version":"GATE4_DIAG_TYPES_PARENT_RETURN_AUTHORIZATION_CONTRACT_V1"}
```

## Authorization evidence

Evidence SHA256: `8bafae01711d8a12c5ecf0c276dbef6a31c48ecf739e2f4e4493ac196e05a373`

```json
{"authorization_status":"AUTHORIZED_RETURN_TO_DIAG_PARENT_FRONTIER_ONLY","child_completed_state_sha256":"33bf91f35c636521e2cf73072c2970094b86adf7d784b5ef67a6d51b9ea61a23","child_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","diag_row6_document_sha256":"b7367aef767b58ab8d9fcf639bbd37e9717751643b0555578961c497a2f6c582","diag_row6_evidence_sha256":"655802c6fa57fd6944ccbd1afbf7ae1d87d796121faad8dc1c5f8e639bf63492","next_parent_item_classification_authorized":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","parent_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","parent_resume_offset":1547,"parent_return_contract":{"authority_mutation_authorized":false,"child_completed_state_sha256":"33bf91f35c636521e2cf73072c2970094b86adf7d784b5ef67a6d51b9ea61a23","child_completion_document_sha256":"b8092cc5d766d2709a735ead8e86b773f36ed2632e3182c09a2c990ef4c1cc82","child_completion_evidence_sha256":"08ba802129f786630a30228fd6411703d3758e20acd230e1d8a3a5c3ce60e299","child_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","child_source_reread_authorized":false,"next_parent_item_classification_authorized":false,"parent_dependency_binding":"o","parent_dependency_row_sha256":"94a35d9d4773eb333ec435b0ea231cb2f9372ec9675f75e555da7a41c33ddf04","parent_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","parent_resume_eligibility_authorized":true,"parent_resume_offset":1547,"source_execution_authorized":false,"version":"GATE4_DIAG_TYPES_PARENT_RETURN_AUTHORIZATION_CONTRACT_V1"},"parent_return_contract_sha256":"8bdbc7ca8c954d8f660721cc9773a50b1c74de71026e3bb6ccb543e3efad4621","source_read_this_gate":false,"version":"GATE4_DIAG_TYPES_PARENT_RETURN_AUTHORIZATION_V1"}
```

## Strict boundary

This gate binds the fully completed diag/types.js child state to the frozen diag.js row-6 dependency and authorizes return eligibility to parent body offset 1547 only. It does not authorize reading or classifying the next parent declarator. It does not authorize rereading completed types.js source, executing JavaScript, mutating the OTEL authority, evaluating Gate 5, running Cursor, or pushing Git state.
