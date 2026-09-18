# Cursor OTEL Gate-4 diag parent return to api context authorization

Date: 2026-09-15

## Status

- Audit status: PASS
- Authorization status: `AUTHORIZED_RETURN_TO_API_CONTEXT_PARENT_FRONTIER_ONLY`
- Parent resume eligibility authorized: YES
- Next parent item classification authorized: NO
- Next parent item read: NO
- Completed diag source reread authorized: NO
- Source execution authorized: NO
- OTEL authority mutation authorized: NO

## Boundary-schema repair

- Failed old assumption: parent dependency must embed one exact modern boundary label
- Embedded boundary kind: `None`
- Embedded terminator: `None`
- Frozen delimiter byte: `,`
- Resolved boundary kind: `DECLARATOR_COMMA`
- Resolved terminator: 1195
- Boundary resolution mode: `DERIVED_FROM_FROZEN_ROW_DELIMITER_BYTE`
- Terminator resolution mode: `DERIVED_FROM_FROZEN_ROW_DELIMITER_OFFSET`
- Boundary adjudication SHA256: `80bb77606d2724b2e59fcfebdd920c89705e3cec29281fda66da8394d73bf9c2`

```json
{"boundary_resolution_mode":"DERIVED_FROM_FROZEN_ROW_DELIMITER_BYTE","delimiter":",","embedded_boundary_kind":null,"embedded_terminator":null,"parent_end":1195,"parent_resume_offset":1196,"resolved_boundary_kind":"DECLARATOR_COMMA","resolved_terminator":1195,"terminator_resolution_mode":"DERIVED_FROM_FROZEN_ROW_DELIMITER_OFFSET","version":"GATE4_API_CONTEXT_DIAG_DEPENDENCY_BOUNDARY_ADJUDICATION_V1"}
```

## Frozen api context dependency

- Parent module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js`
- Frozen parent body SHA256: `d8a3982b67173a9152b5b610028a5dad7eb9f459a3f31432e0624f89592da17e`
- Dependency document: `docs/CURSOR_OTEL_GATE4_API_CONTEXT_FIRST_STATIC_FRONTIER_2026-09-15.md`
- Dependency document SHA256: `91bd52e6759297d6cc31c5c58e4e05bb950d6752397bebb4a3ce329d86050c61`
- Dependency evidence SHA256: `ad64be1a74ea6b364f114d1b98918c4ef3d9983f7e8734b2e3fb79066ac5b973`
- Dependency row SHA256: `106c8dc17352b36202a52ff9668ac491f740819f008dcc372a6a633095e176fc`
- Binding: `o`
- Dependency module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js`
- Source SHA256: `6cd448ef0f65cdde11d39816a657b76ed14ddffcf5e3aecc9b034d08127571db`
- Body offsets: 1085:1195
- Resolved boundary: `DECLARATOR_COMMA`
- Resolved terminator: 1195
- Parent resume offset: 1196

## Completed diag child

- Completion document SHA256: `d810047b9aaca8ac555cddd0d83937d8fa3288fe2ed8107538bf593c790cdc54`
- Completion evidence SHA256: `2782e4ac04d9c5b71e1615fa86124366664cac01139655b1bea0040046c933c1`
- Completed state SHA256: `d1c86b38caf273d343e95d5198da380ec66fbdbee2add54d4cac8305c91df0e9`
- Unresolved dependency count: 0

## Parent-return contract

- Contract SHA256: `2e4c222ac096743c259ee7b2954e27b5a6c9dfd068b010d6e97bdbb1d27f8ae1`

```json
{"authority_mutation_authorized":false,"boundary_adjudication_sha256":"80bb77606d2724b2e59fcfebdd920c89705e3cec29281fda66da8394d73bf9c2","child_completed_state_sha256":"d1c86b38caf273d343e95d5198da380ec66fbdbee2add54d4cac8305c91df0e9","child_completion_document_sha256":"d810047b9aaca8ac555cddd0d83937d8fa3288fe2ed8107538bf593c790cdc54","child_completion_evidence_sha256":"2782e4ac04d9c5b71e1615fa86124366664cac01139655b1bea0040046c933c1","child_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","child_source_reread_authorized":false,"next_parent_item_classification_authorized":false,"parent_body_sha256":"d8a3982b67173a9152b5b610028a5dad7eb9f459a3f31432e0624f89592da17e","parent_dependency_binding":"o","parent_dependency_document_path":"docs/CURSOR_OTEL_GATE4_API_CONTEXT_FIRST_STATIC_FRONTIER_2026-09-15.md","parent_dependency_document_sha256":"91bd52e6759297d6cc31c5c58e4e05bb950d6752397bebb4a3ce329d86050c61","parent_dependency_evidence_sha256":"ad64be1a74ea6b364f114d1b98918c4ef3d9983f7e8734b2e3fb79066ac5b973","parent_dependency_row_sha256":"106c8dc17352b36202a52ff9668ac491f740819f008dcc372a6a633095e176fc","parent_dependency_source_sha256":"6cd448ef0f65cdde11d39816a657b76ed14ddffcf5e3aecc9b034d08127571db","parent_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","parent_module_record_sha256":"e5ab0daa3dc7bed29eda2ce170e726bc6875586094dbe16a8eccf7b4a85834f7","parent_resume_eligibility_authorized":true,"parent_resume_offset":1196,"resolved_parent_boundary_kind":"DECLARATOR_COMMA","resolved_parent_terminator":1195,"source_execution_authorized":false,"version":"GATE4_DIAG_PARENT_RETURN_TO_API_CONTEXT_AUTHORIZATION_CONTRACT_V2"}
```

## Parent-return evidence

Evidence SHA256: `2350f8a8a66dee809417cb2feea00d848cf62628be1984d995dc3a6ccecbe900`

```json
{"authorization_status":"AUTHORIZED_RETURN_TO_API_CONTEXT_PARENT_FRONTIER_ONLY","boundary_adjudication":{"boundary_resolution_mode":"DERIVED_FROM_FROZEN_ROW_DELIMITER_BYTE","delimiter":",","embedded_boundary_kind":null,"embedded_terminator":null,"parent_end":1195,"parent_resume_offset":1196,"resolved_boundary_kind":"DECLARATOR_COMMA","resolved_terminator":1195,"terminator_resolution_mode":"DERIVED_FROM_FROZEN_ROW_DELIMITER_OFFSET","version":"GATE4_API_CONTEXT_DIAG_DEPENDENCY_BOUNDARY_ADJUDICATION_V1"},"boundary_adjudication_sha256":"80bb77606d2724b2e59fcfebdd920c89705e3cec29281fda66da8394d73bf9c2","child_completed_state_sha256":"d1c86b38caf273d343e95d5198da380ec66fbdbee2add54d4cac8305c91df0e9","child_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","next_parent_item_classification_authorized":false,"next_parent_item_read":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","parent_dependency_row_sha256":"106c8dc17352b36202a52ff9668ac491f740819f008dcc372a6a633095e176fc","parent_dependency_source_sha256":"6cd448ef0f65cdde11d39816a657b76ed14ddffcf5e3aecc9b034d08127571db","parent_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","parent_resume_offset":1196,"return_contract":{"authority_mutation_authorized":false,"boundary_adjudication_sha256":"80bb77606d2724b2e59fcfebdd920c89705e3cec29281fda66da8394d73bf9c2","child_completed_state_sha256":"d1c86b38caf273d343e95d5198da380ec66fbdbee2add54d4cac8305c91df0e9","child_completion_document_sha256":"d810047b9aaca8ac555cddd0d83937d8fa3288fe2ed8107538bf593c790cdc54","child_completion_evidence_sha256":"2782e4ac04d9c5b71e1615fa86124366664cac01139655b1bea0040046c933c1","child_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","child_source_reread_authorized":false,"next_parent_item_classification_authorized":false,"parent_body_sha256":"d8a3982b67173a9152b5b610028a5dad7eb9f459a3f31432e0624f89592da17e","parent_dependency_binding":"o","parent_dependency_document_path":"docs/CURSOR_OTEL_GATE4_API_CONTEXT_FIRST_STATIC_FRONTIER_2026-09-15.md","parent_dependency_document_sha256":"91bd52e6759297d6cc31c5c58e4e05bb950d6752397bebb4a3ce329d86050c61","parent_dependency_evidence_sha256":"ad64be1a74ea6b364f114d1b98918c4ef3d9983f7e8734b2e3fb79066ac5b973","parent_dependency_row_sha256":"106c8dc17352b36202a52ff9668ac491f740819f008dcc372a6a633095e176fc","parent_dependency_source_sha256":"6cd448ef0f65cdde11d39816a657b76ed14ddffcf5e3aecc9b034d08127571db","parent_module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/context.js","parent_module_record_sha256":"e5ab0daa3dc7bed29eda2ce170e726bc6875586094dbe16a8eccf7b4a85834f7","parent_resume_eligibility_authorized":true,"parent_resume_offset":1196,"resolved_parent_boundary_kind":"DECLARATOR_COMMA","resolved_parent_terminator":1195,"source_execution_authorized":false,"version":"GATE4_DIAG_PARENT_RETURN_TO_API_CONTEXT_AUTHORIZATION_CONTRACT_V2"},"return_contract_sha256":"2e4c222ac096743c259ee7b2954e27b5a6c9dfd068b010d6e97bdbb1d27f8ae1","source_execution_performed":false,"version":"GATE4_DIAG_PARENT_RETURN_TO_API_CONTEXT_AUTHORIZATION_V2"}
```

## Strict boundary

This repair changes only the historical parent-boundary schema assumption. The frozen api/context dependency source SHA, offsets, binding, dependency module, Cursor authority, and completed diag state remain unchanged. Only the already-qualified dependency source bytes and its single delimiter byte were verified. No byte from the next api/context item was read or classified. Completed diag source was not reread. No JavaScript was executed, the OTEL authority was not mutated, Gate 5 was not evaluated, Cursor was not run, and no Git push was performed.
