# Cursor OTEL Gate-4 proto3 token 5492 reference GSV2

Date: 2026-09-16

## Status

- module: ../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js
- owner origin: 5099
- owner function: R
- token 5492: FUNCTION_PARAMETER_REFERENCE
- exact expression: P(n.T,e,s.ignoreUnknownFields,!0)
- proto3 source reread: NO
- next token: 5573
- next context: n.T,e,n.L
- token 5573 qualified: NO
- hard template boundary: 5603
- template 5603 crossed: NO
- proto3 complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO

## Authority

Authority SHA256: `566820ace8b617d5a4b27845e1222acda7d98a9f4bc1085139def950d9d3ee1b`

```json
{"state":{"current_authority":{"authority_sha256":"c97c9457c5fb8c908bf15b2f7da21470edc3e3312355fc34ee1fdfeb9fcca3ba","document":"docs/CURSOR_OTEL_GATE4_PROTO3_N5446_REFERENCE_GSV2_2026-09-16.md","document_sha256":"225375bb83517bf1c362516b80e437f670b89d7f07d89b19d98d2068b1470a33"},"hard_template_boundary":5603,"module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js","next_frontier":{"frontier_kind":"FUNCTION_PARAMETER_REFERENCE_UNQUALIFIED","hard_template_boundary":5603,"owner_origin":5099,"preceding_qualified_token":5492,"source_reread":false,"source_window":{"end":5637,"sha256":"fe0b5b365634b6f00bf30a155aa0fd2af093143c33d35cc7b1e339e38c310405","start":5267,"text":"m JSON: ${B(t)}`);const a=e[o];for(const e of t){if(null===e)throw new Error(`cannot decode field ${i.typeName}.${n.name} from JSON: ${B(e)}`);switch(n.kind){case\"message\":a.push(n.T.fromJson(e,s));break;case\"enum\":const t=P(n.T,e,s.ignoreUnknownFields,!0);t!==b&&a.push(t);break;case\"scalar\":try{a.push(N(n.T,e,n.L,!0))}catch(t){let r=`cannot decode field ${i.typeName}"},"token_start":5573},"owner":{"binding_kind":"FUNCTION_PARAMETER","function_name":"R","hard_scope_proof_end":5219,"origin":5099,"parameter_index":2,"parameters":[{"end":5096,"start":5095,"text":"e"},{"end":5098,"start":5097,"text":"t"},{"end":5100,"start":5099,"text":"n"},{"end":5102,"start":5101,"text":"s"},{"end":5104,"start":5103,"text":"i"}],"scope_end_beyond_hard_boundary":true,"signature_end":5106,"signature_sha256":"a5d2119b4e4c6efab84b34c797ff9a1cccf06daad1aa6dcbe346c40a20b59037","signature_start":5084},"qualified_row":{"classification":"FUNCTION_PARAMETER_REFERENCE","exact_expression":"P(n.T,e,s.ignoreUnknownFields,!0)","owner":{"binding_kind":"FUNCTION_PARAMETER","function_name":"R","hard_scope_proof_end":5219,"origin":5099,"parameter_index":2,"parameters":[{"end":5096,"start":5095,"text":"e"},{"end":5098,"start":5097,"text":"t"},{"end":5100,"start":5099,"text":"n"},{"end":5102,"start":5101,"text":"s"},{"end":5104,"start":5103,"text":"i"}],"scope_end_beyond_hard_boundary":true,"signature_end":5106,"signature_sha256":"a5d2119b4e4c6efab84b34c797ff9a1cccf06daad1aa6dcbe346c40a20b59037","signature_start":5084},"source_window":{"end":5637,"sha256":"fe0b5b365634b6f00bf30a155aa0fd2af093143c33d35cc7b1e339e38c310405","start":5267,"text":"m JSON: ${B(t)}`);const a=e[o];for(const e of t){if(null===e)throw new Error(`cannot decode field ${i.typeName}.${n.name} from JSON: ${B(e)}`);switch(n.kind){case\"message\":a.push(n.T.fromJson(e,s));break;case\"enum\":const t=P(n.T,e,s.ignoreUnknownFields,!0);t!==b&&a.push(t);break;case\"scalar\":try{a.push(N(n.T,e,n.L,!0))}catch(t){let r=`cannot decode field ${i.typeName}"},"token_start":5492},"qualified_token":5492,"qualified_under_origin":5099,"source_continuity":{"end":5573,"sha256":"c4a73956d9a0e318c9760cc253055baead6ae5546311f8bdae37413e8d97ed84","start":5492,"text":"n.T,e,s.ignoreUnknownFields,!0);t!==b&&a.push(t);break;case\"scalar\":try{a.push(N("},"source_reread":false,"version":"PROTO3_N5492_REFERENCE_GSV2_V1"},"state_sha256":"364c191124cdf7b71ec9fd0860e56b19aaf720b8bc85d2e29145faa667c9a6a5","version":"GATE4_PROTO3_N5492_REFERENCE_GSV2_V1"}
```

## Evidence

Evidence SHA256: `03af21b12582372091443f00937ce8008ae36530f1274418626c12e9ab882c44`

```json
{"authority_sha256":"566820ace8b617d5a4b27845e1222acda7d98a9f4bc1085139def950d9d3ee1b","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"next_token_5573_qualified":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","proto3_complete":false,"proto3_source_reread":false,"template_5603_crossed":false,"token_5492_qualified":true,"token_5573_advanced":false,"version":"GATE4_PROTO3_N5492_REFERENCE_GSV2_V1_EVIDENCE"}
```

## Boundary

The committed token-5446 authority freezes token 5492 in the enum case under function R parameter n at origin 5099. Token 5492 is qualified as the n.T reference inside P(n.T,e,s.ignoreUnknownFields,!0). Exact continuity through the enum break and into the scalar case contains no closing brace and no template delimiter. Token 5573 is frozen as the next n.T reference and remains unqualified. The template hazard at 5603 remains uncrossed.
