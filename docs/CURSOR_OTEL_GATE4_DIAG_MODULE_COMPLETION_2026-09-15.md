# Cursor OTEL Gate-4 diag module completion

Date: 2026-09-15

## Status

- Audit status: PASS
- Module completion qualified: YES
- Frozen row count: 7
- Ordinal authority mode: `FROZEN_SEQUENCE_WITH_OPTIONAL_EMBEDDED_ORDINAL`
- Rows carrying embedded ordinal: 6
- Rows without embedded ordinal: 1
- Exact body coverage: 0:3461
- Coverage contiguous: YES
- Body reconstruction equal: YES
- Dependency count: 2
- Unresolved dependency count: 0
- Parent api/context advanced: NO
- Source executed: NO
- OTEL authority mutated: NO

## Schema repair

Historical row objects are not required to duplicate the row ordinal when their frozen document, evidence SHA, canonical row SHA, sequence position, source SHA, and body boundaries already uniquely identify the row. When an embedded ordinal is present it must agree with the frozen sequence.

## Frozen module identity

- Module: `../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js`
- Module record SHA256: `b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8`
- Body chars: 3461
- Body SHA256: `7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195`

## Frozen row sequence

- Row count: 7
- Row sequence SHA256: `fab6529e8f5d5177400bba2e6b58f53c893c02fcfdb50c07a3042c84f956176a`

## Exact body coverage

- Coverage SHA256: `c991799c3944dbe106b2888d2489a5022cb806fd39298bf2cc1264e32cb6e8fe`
- Coverage start: 0
- Coverage end: 3461
- Coverage gaps: 0
- Coverage overlaps: 0
- Exact body reconstruction: YES

## Completed dependencies

- global-utils completed state SHA256: `f4b8f19271c054b83809afc2908a394a4d33457988d2cef6c54e4013a3b3a929`
- diag/types.js completed state SHA256: `33bf91f35c636521e2cf73072c2970094b86adf7d784b5ef67a6d51b9ea61a23`
- Completed dependency set SHA256: `500b94d51f6c4ed1d95b226149595cd9fea882633f11318bbec247738980ca55`
- Unresolved dependency count: 0

## Completed diag state

- Completed state SHA256: `d1c86b38caf273d343e95d5198da380ec66fbdbee2add54d4cac8305c91df0e9`

```json
{"body_chars":3461,"body_sha256":"7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195","completed":true,"completed_dependencies_sha256":"500b94d51f6c4ed1d95b226149595cd9fea882633f11318bbec247738980ca55","coverage_end":3461,"coverage_sha256":"c991799c3944dbe106b2888d2489a5022cb806fd39298bf2cc1264e32cb6e8fe","coverage_start":0,"dependency_count":2,"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","module_record_sha256":"b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8","row_count":7,"row_sequence_sha256":"fab6529e8f5d5177400bba2e6b58f53c893c02fcfdb50c07a3042c84f956176a","unresolved_dependency_count":0,"version":"GATE4_DIAG_COMPLETED_STATE_V1"}
```

## Completion evidence

Evidence SHA256: `2782e4ac04d9c5b71e1615fa86124366664cac01139655b1bea0040046c933c1`

```json
{"body_reconstruction_equal":true,"body_reconstruction_sha256":"7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195","completed_dependencies":[{"binding":"r","completed_state_sha256":"f4b8f19271c054b83809afc2908a394a4d33457988d2cef6c54e4013a3b3a929","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/internal/global-utils.js","parent_row_ordinal":3,"parent_row_sha256":"41c1745b022074c1e7539b8a51e9d28f9926a073f3e729d1aa70a9594773e8b0"},{"binding":"o","completed_state_sha256":"33bf91f35c636521e2cf73072c2970094b86adf7d784b5ef67a6d51b9ea61a23","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/diag/types.js","parent_row_ordinal":6,"parent_row_sha256":"94a35d9d4773eb333ec435b0ea231cb2f9372ec9675f75e555da7a41c33ddf04"}],"completed_dependencies_sha256":"500b94d51f6c4ed1d95b226149595cd9fea882633f11318bbec247738980ca55","completed_state":{"body_chars":3461,"body_sha256":"7d8633d3dbb5363eb479e34938c5cff93b5cf3f20eb1bcc3576c06ebea5d9195","completed":true,"completed_dependencies_sha256":"500b94d51f6c4ed1d95b226149595cd9fea882633f11318bbec247738980ca55","coverage_end":3461,"coverage_sha256":"c991799c3944dbe106b2888d2489a5022cb806fd39298bf2cc1264e32cb6e8fe","coverage_start":0,"dependency_count":2,"module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","module_record_sha256":"b1497737d23f6fd14563a3204377ac10e41a6b9b8d25c8c6f25f47646b5f6cb8","row_count":7,"row_sequence_sha256":"fab6529e8f5d5177400bba2e6b58f53c893c02fcfdb50c07a3042c84f956176a","unresolved_dependency_count":0,"version":"GATE4_DIAG_COMPLETED_STATE_V1"},"completed_state_sha256":"d1c86b38caf273d343e95d5198da380ec66fbdbee2add54d4cac8305c91df0e9","coverage_contiguous":true,"coverage_segments":[{"end":12,"kind":"ROW_1_SOURCE","start":0},{"end":13,"kind":"ROW_1_TERMINATOR","start":12},{"end":29,"kind":"ROW_2_SOURCE","start":13},{"end":30,"kind":"ROW_2_TERMINATOR","start":29},{"end":34,"kind":"ROW_3_DECLARATION_PREFIX","start":30},{"end":157,"kind":"ROW_3_SOURCE","start":34},{"end":158,"kind":"ROW_3_COMMA","start":157},{"end":867,"kind":"ROW_4_SOURCE","start":158},{"end":868,"kind":"ROW_4_TERMINATOR","start":867},{"end":1430,"kind":"ROW_5_FUNCTION_DECLARATION","start":868},{"end":1434,"kind":"ROW_6_DECLARATION_PREFIX","start":1430},{"end":1546,"kind":"ROW_6_SOURCE","start":1434},{"end":1547,"kind":"ROW_6_COMMA","start":1546},{"end":3461,"kind":"ROW_7_SOURCE_TO_BODY_END","start":1547}],"coverage_sha256":"c991799c3944dbe106b2888d2489a5022cb806fd39298bf2cc1264e32cb6e8fe","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","global_utils_reuse_document_sha256":"abcb2a53154dce25b8e8821fef0a950a4214a67ec0f5eb8c746565a305907763","global_utils_reuse_evidence_sha256":"a950f49835eefb7f0b106a836b23d314b514e0aebb1c1cdb98a2bc759d1626b8","module":"../../node_modules/.pnpm/@opentelemetry+api@1.9.0/node_modules/@opentelemetry/api/build/esm/api/diag.js","otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","parent_api_context_advanced":false,"row_documents":[{"document_sha256":"d830bbe3648569c6da249a141acf703ef8ad74223d7f73556d700673065f3561","embedded_ordinal":null,"evidence_sha256":"83ad31f6d99024d3c0efcd7677d52db6ef0bf65c172c6b0babdc4ea4c28ef56f","expected_ordinal":1,"row_sha256":"9b88aea1a1e6c5bf6e311b75c23ae1b3e9abe23eaffbe23ead0171ab1d14fe7a"},{"document_sha256":"9acdab3bd62c5b5c3474ccb701c0ca03e8b0103baf1905157800be7ce650542d","embedded_ordinal":2,"evidence_sha256":"8fbc488a4fe9ce6688215997ea2ca013ce38c6c205effb36f4ac2557ac32003b","expected_ordinal":2,"row_sha256":"0f5b078bd89f25b456890011fbcac23a7502f9560d7db606dea916b2b45525da"},{"document_sha256":"593eb5384c3796c92c56840673c7927c0fd9f56ff127016375c616ddf54190af","embedded_ordinal":3,"evidence_sha256":"6b7e6699a9660dae01c625b778e57df5b421f5167b68148c54bbc7d189cb7c8a","expected_ordinal":3,"row_sha256":"41c1745b022074c1e7539b8a51e9d28f9926a073f3e729d1aa70a9594773e8b0"},{"document_sha256":"0e458abdf5cd152d08aa1bc89570c8988c0ca9663caf71769ea5e29a948fef7e","embedded_ordinal":4,"evidence_sha256":"8d3d098732846e07bebb33a28a703e5dde3298c09094e95c2ced82200463bc81","expected_ordinal":4,"row_sha256":"0949c21d737be5745db462ee8c322405eb516b078daa6277afdca5e7b7d72a8d"},{"document_sha256":"10945fcabbaf7c5842cd94e4186e50cfea863d3035a7e344541d1dfcc0136cf6","embedded_ordinal":5,"evidence_sha256":"abb46e2b28d72d98ba950f144c54ca2a5c581106d09b1a1adc72133b51fd5f9b","expected_ordinal":5,"row_sha256":"fd068697d93b453865dfbd2d1baf118774804a93c8e46640bac8798ac7f63283"},{"document_sha256":"b7367aef767b58ab8d9fcf639bbd37e9717751643b0555578961c497a2f6c582","embedded_ordinal":6,"evidence_sha256":"655802c6fa57fd6944ccbd1afbf7ae1d87d796121faad8dc1c5f8e639bf63492","expected_ordinal":6,"row_sha256":"94a35d9d4773eb333ec435b0ea231cb2f9372ec9675f75e555da7a41c33ddf04"},{"document_sha256":"753d7f479696a5a3ff4b5a90439a2c8304dd7b2376434cbb09c0d70e0a51619e","embedded_ordinal":7,"evidence_sha256":"adcbc46f37b63564273f99cc09528c8aa7166565e1f060432c1a2d4698905066","expected_ordinal":7,"row_sha256":"11404136848cfc6ee252624f4b29124011756e126ce389cc4e979ab328cf32ba"}],"row_sequence":[{"ordinal":1,"row_sha256":"9b88aea1a1e6c5bf6e311b75c23ae1b3e9abe23eaffbe23ead0171ab1d14fe7a"},{"ordinal":2,"row_sha256":"0f5b078bd89f25b456890011fbcac23a7502f9560d7db606dea916b2b45525da"},{"ordinal":3,"row_sha256":"41c1745b022074c1e7539b8a51e9d28f9926a073f3e729d1aa70a9594773e8b0"},{"ordinal":4,"row_sha256":"0949c21d737be5745db462ee8c322405eb516b078daa6277afdca5e7b7d72a8d"},{"ordinal":5,"row_sha256":"fd068697d93b453865dfbd2d1baf118774804a93c8e46640bac8798ac7f63283"},{"ordinal":6,"row_sha256":"94a35d9d4773eb333ec435b0ea231cb2f9372ec9675f75e555da7a41c33ddf04"},{"ordinal":7,"row_sha256":"11404136848cfc6ee252624f4b29124011756e126ce389cc4e979ab328cf32ba"}],"row_sequence_sha256":"fab6529e8f5d5177400bba2e6b58f53c893c02fcfdb50c07a3042c84f956176a","rows_with_embedded_ordinal":6,"rows_without_embedded_ordinal":1,"source_execution_performed":false,"types_return_document_sha256":"20f136fc9f2759630db550f6ea7c4a522c55ebf27b3c3fa39d794114ee81368b","types_return_evidence_sha256":"8bafae01711d8a12c5ecf0c276dbef6a31c48ecf739e2f4e4493ac196e05a373","unresolved_dependency_count":0,"version":"GATE4_DIAG_MODULE_COMPLETION_V2"}
```

## Strict boundary

This repaired completion gate changes only the historical embedded-ordinal assumption. All previously frozen row documents, evidence hashes, canonical row hashes, source hashes, boundaries, module identity, and completed dependency identities remain mandatory. Completed dependency source was not reread. The api/context parent was not resumed. No JavaScript was executed, the OTEL authority was not mutated, Gate 5 was not evaluated, Cursor was not run, and no Git push was performed.
