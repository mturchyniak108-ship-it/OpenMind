# Cursor OTEL Gate-4 proto3 token 5446 reference GSV2

Date: 2026-09-16

## Status

- module: ../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js
- owner origin: 5099
- owner function: R
- token 5446: FUNCTION_PARAMETER_REFERENCE
- exact expression: n.T.fromJson(e,s)
- proto3 source reread: NO
- next token: 5492
- next context: n.T,e
- token 5492 qualified: NO
- proto3 complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO

## Authority

Authority SHA256: `c97c9457c5fb8c908bf15b2f7da21470edc3e3312355fc34ee1fdfeb9fcca3ba`

```json
{"state":{"current_authority":{"authority_sha256":"415d9e7c9c0907227095c788f2c59195ba8f2ff3d16fdefb4b633bd12dc47cbe","document":"docs/CURSOR_OTEL_GATE4_PROTO3_N5417_REFERENCE_GSV2_2026-09-16.md","document_sha256":"b264f7df5f1a0e1d17fecfe3211059a1ffe077a7e06a4f48c3d26812c368757e"},"module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js","next_frontier":{"frontier_kind":"FUNCTION_PARAMETER_REFERENCE_UNQUALIFIED","owner_origin":5099,"preceding_qualified_token":5446,"source_reread":false,"source_window":{"end":5637,"sha256":"fe0b5b365634b6f00bf30a155aa0fd2af093143c33d35cc7b1e339e38c310405","start":5267,"text":"m JSON: ${B(t)}`);const a=e[o];for(const e of t){if(null===e)throw new Error(`cannot decode field ${i.typeName}.${n.name} from JSON: ${B(e)}`);switch(n.kind){case\"message\":a.push(n.T.fromJson(e,s));break;case\"enum\":const t=P(n.T,e,s.ignoreUnknownFields,!0);t!==b&&a.push(t);break;case\"scalar\":try{a.push(N(n.T,e,n.L,!0))}catch(t){let r=`cannot decode field ${i.typeName}"},"token_start":5492},"owner":{"binding_kind":"FUNCTION_PARAMETER","function_name":"R","hard_scope_proof_end":5219,"origin":5099,"parameter_index":2,"parameters":[{"end":5096,"start":5095,"text":"e"},{"end":5098,"start":5097,"text":"t"},{"end":5100,"start":5099,"text":"n"},{"end":5102,"start":5101,"text":"s"},{"end":5104,"start":5103,"text":"i"}],"scope_end_beyond_hard_boundary":true,"signature_end":5106,"signature_sha256":"a5d2119b4e4c6efab84b34c797ff9a1cccf06daad1aa6dcbe346c40a20b59037","signature_start":5084},"qualified_row":{"classification":"FUNCTION_PARAMETER_REFERENCE","exact_expression":"n.T.fromJson(e,s)","owner":{"binding_kind":"FUNCTION_PARAMETER","function_name":"R","hard_scope_proof_end":5219,"origin":5099,"parameter_index":2,"parameters":[{"end":5096,"start":5095,"text":"e"},{"end":5098,"start":5097,"text":"t"},{"end":5100,"start":5099,"text":"n"},{"end":5102,"start":5101,"text":"s"},{"end":5104,"start":5103,"text":"i"}],"scope_end_beyond_hard_boundary":true,"signature_end":5106,"signature_sha256":"a5d2119b4e4c6efab84b34c797ff9a1cccf06daad1aa6dcbe346c40a20b59037","signature_start":5084},"source_window":{"end":5637,"sha256":"fe0b5b365634b6f00bf30a155aa0fd2af093143c33d35cc7b1e339e38c310405","start":5267,"text":"m JSON: ${B(t)}`);const a=e[o];for(const e of t){if(null===e)throw new Error(`cannot decode field ${i.typeName}.${n.name} from JSON: ${B(e)}`);switch(n.kind){case\"message\":a.push(n.T.fromJson(e,s));break;case\"enum\":const t=P(n.T,e,s.ignoreUnknownFields,!0);t!==b&&a.push(t);break;case\"scalar\":try{a.push(N(n.T,e,n.L,!0))}catch(t){let r=`cannot decode field ${i.typeName}"},"token_start":5446},"qualified_token":5446,"qualified_under_origin":5099,"source_continuity":{"end":5492,"sha256":"c6523af74c78ffb74766b9a180e1a75a04487f8aa0b623dd08b570f11aaeef93","start":5446,"text":"n.T.fromJson(e,s));break;case\"enum\":const t=P("},"source_reread":false,"version":"PROTO3_N5446_REFERENCE_GSV2_V1"},"state_sha256":"a713f5cc532e54c8c34986d7d9b08f27d0aad4f13fc594551febc8e8a639cb3f","version":"GATE4_PROTO3_N5446_REFERENCE_GSV2_V1"}
```

## Evidence

Evidence SHA256: `6554653d9cba9348b65a18f3cda348238d247718be33babace520896192ce647`

```json
{"authority_sha256":"c97c9457c5fb8c908bf15b2f7da21470edc3e3312355fc34ee1fdfeb9fcca3ba","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"next_token_5492_qualified":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","proto3_complete":false,"proto3_source_reread":false,"token_5446_qualified":true,"token_5492_advanced":false,"version":"GATE4_PROTO3_N5446_REFERENCE_GSV2_V1_EVIDENCE"}
```

## Boundary

The committed token-5417 authority freezes token 5446 in the same function R scope and source window. Token 5446 is qualified as the n reference in n.T.fromJson(e,s), owned by function R parameter n at origin 5099. Exact continuity from token 5446 to token 5492 contains no closing brace and no template delimiter. Token 5492 is frozen as the next n reference in n.T,e and remains unqualified. No proto3 source reread occurs.
