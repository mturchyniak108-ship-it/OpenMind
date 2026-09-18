# Cursor OTEL Gate-4 proto3 token 5573 reference GSV2

Date: 2026-09-16

## Status

- module: ../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js
- owner origin: 5099
- owner function: R
- token 5573: FUNCTION_PARAMETER_REFERENCE
- exact expression: N(n.T,e,n.L,!0)
- proto3 source reread: NO
- next token: 5579
- next context: n.L,!0
- token 5579 qualified: NO
- hard template boundary: 5603
- template 5603 crossed: NO
- proto3 complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO

## Authority

Authority SHA256: `197ea95ce1e5729c2144eeb9b0eabecc00af26d5c17a1ea5c93e15c36497208d`

```json
{"state":{"current_authority":{"authority_sha256":"566820ace8b617d5a4b27845e1222acda7d98a9f4bc1085139def950d9d3ee1b","document":"docs/CURSOR_OTEL_GATE4_PROTO3_N5492_REFERENCE_GSV2_2026-09-16.md","document_sha256":"1c61728b362df6642ee6c52c5f9e144f4146c1f7465307c731745025e056bfa1"},"hard_template_boundary":5603,"module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js","next_frontier":{"frontier_kind":"FUNCTION_PARAMETER_REFERENCE_UNQUALIFIED","hard_template_boundary":5603,"owner_origin":5099,"preceding_qualified_token":5573,"source_reread":false,"source_window":{"end":5637,"sha256":"fe0b5b365634b6f00bf30a155aa0fd2af093143c33d35cc7b1e339e38c310405","start":5267,"text":"m JSON: ${B(t)}`);const a=e[o];for(const e of t){if(null===e)throw new Error(`cannot decode field ${i.typeName}.${n.name} from JSON: ${B(e)}`);switch(n.kind){case\"message\":a.push(n.T.fromJson(e,s));break;case\"enum\":const t=P(n.T,e,s.ignoreUnknownFields,!0);t!==b&&a.push(t);break;case\"scalar\":try{a.push(N(n.T,e,n.L,!0))}catch(t){let r=`cannot decode field ${i.typeName}"},"token_start":5579},"owner":{"binding_kind":"FUNCTION_PARAMETER","function_name":"R","hard_scope_proof_end":5219,"origin":5099,"parameter_index":2,"parameters":[{"end":5096,"start":5095,"text":"e"},{"end":5098,"start":5097,"text":"t"},{"end":5100,"start":5099,"text":"n"},{"end":5102,"start":5101,"text":"s"},{"end":5104,"start":5103,"text":"i"}],"scope_end_beyond_hard_boundary":true,"signature_end":5106,"signature_sha256":"a5d2119b4e4c6efab84b34c797ff9a1cccf06daad1aa6dcbe346c40a20b59037","signature_start":5084},"qualified_row":{"classification":"FUNCTION_PARAMETER_REFERENCE","exact_expression":"N(n.T,e,n.L,!0)","owner":{"binding_kind":"FUNCTION_PARAMETER","function_name":"R","hard_scope_proof_end":5219,"origin":5099,"parameter_index":2,"parameters":[{"end":5096,"start":5095,"text":"e"},{"end":5098,"start":5097,"text":"t"},{"end":5100,"start":5099,"text":"n"},{"end":5102,"start":5101,"text":"s"},{"end":5104,"start":5103,"text":"i"}],"scope_end_beyond_hard_boundary":true,"signature_end":5106,"signature_sha256":"a5d2119b4e4c6efab84b34c797ff9a1cccf06daad1aa6dcbe346c40a20b59037","signature_start":5084},"source_window":{"end":5637,"sha256":"fe0b5b365634b6f00bf30a155aa0fd2af093143c33d35cc7b1e339e38c310405","start":5267,"text":"m JSON: ${B(t)}`);const a=e[o];for(const e of t){if(null===e)throw new Error(`cannot decode field ${i.typeName}.${n.name} from JSON: ${B(e)}`);switch(n.kind){case\"message\":a.push(n.T.fromJson(e,s));break;case\"enum\":const t=P(n.T,e,s.ignoreUnknownFields,!0);t!==b&&a.push(t);break;case\"scalar\":try{a.push(N(n.T,e,n.L,!0))}catch(t){let r=`cannot decode field ${i.typeName}"},"token_start":5573},"qualified_token":5573,"qualified_under_origin":5099,"source_continuity":{"end":5579,"sha256":"1d742cde4e7a2906ef6bbf3393e3f610366b2487f1ac4c565c97a7676e61f626","start":5573,"text":"n.T,e,"},"source_reread":false,"version":"PROTO3_N5573_REFERENCE_GSV2_V1"},"state_sha256":"bcfe5abe78b9cef76c13576ae28343fbe3a303bf49731f34fe7ad7265a635f71","version":"GATE4_PROTO3_N5573_REFERENCE_GSV2_V1"}
```

## Evidence

Evidence SHA256: `a6334c326d30d15641c8ce6ff9cf5b06fdf969cf28c022842e1b6dedd45dd9bf`

```json
{"authority_sha256":"197ea95ce1e5729c2144eeb9b0eabecc00af26d5c17a1ea5c93e15c36497208d","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"next_token_5579_qualified":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","proto3_complete":false,"proto3_source_reread":false,"template_5603_crossed":false,"token_5573_qualified":true,"token_5579_advanced":false,"version":"GATE4_PROTO3_N5573_REFERENCE_GSV2_V1_EVIDENCE"}
```

## Boundary

The committed token-5492 authority freezes token 5573 inside the scalar case under function R parameter n at origin 5099. Token 5573 is qualified as the n.T reference in N(n.T,e,n.L,!0). Token 5579 is the following n.L reference in the same scalar expression and remains unqualified. Template hazard 5603 remains frozen and uncrossed. No proto3 source reread occurs.
