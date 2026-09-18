# Cursor OTEL Gate-4 proto3 token 5112 reference GSV2

Date: 2026-09-16

## Status

- module: ../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js
- owner origin: 5099
- owner binding: FUNCTION_PARAMETER
- owner function: R
- token 5112: FUNCTION_PARAMETER_REFERENCE
- exact context: n.localName
- source reread: NO
- next frontier token: 5127
- token 5127 qualified: NO
- hard template boundary: 5219
- template boundary crossed: NO
- proto3 complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO
- JavaScript executed: NO

## Authority

Authority SHA256: `7c071c12bef1bcb71989d2936c69dd169eb2053150075a76d7c434701fc44864`

```json
{"state":{"bounded_local_n_tokens":[5099,5112,5127,5158],"current_authority":{"authority_sha256":"938eaf368a416e6af8cbc1fef2ffff831192433693aec110374ccfc54b2f9920","document":"docs/CURSOR_OTEL_GATE4_PROTO3_N5099_BOUNDED_GSV2_2026-09-16.md","document_sha256":"2d9edf0293143bbc55376b0b4c339273be673733572985b4a545b258e11b2dd1"},"first_future_template":5219,"module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js","next_frontier":{"frontier_kind":"FUNCTION_PARAMETER_REFERENCE_UNQUALIFIED","hard_template_boundary":5219,"owner_origin":5099,"preceding_qualified_token":5112,"source_window":{"end":5219,"sha256":"094a908b0677abe25f164bfc4a2e87617e84ef76fee8e0ec3dcdb87034741914","start":4932,"text":"se\"object\":return Array.isArray(e)?\"array\":\"object\";case\"string\":return e.length>100?\"string\":`\"${e.split('\"').join('\\\\\"')}\"`;default:return String(e)}}function R(e,t,n,s,i){let o=n.localName;if(n.repeated){if((0,r.vA)(\"map\"!=n.kind),null===t)return;if(!Array.isArray(t))throw new Error("},"token_start":5127},"owner":{"binding_kind":"FUNCTION_PARAMETER","function_name":"R","hard_scope_proof_end":5219,"origin":5099,"parameter_index":2,"parameters":[{"end":5096,"start":5095,"text":"e"},{"end":5098,"start":5097,"text":"t"},{"end":5100,"start":5099,"text":"n"},{"end":5102,"start":5101,"text":"s"},{"end":5104,"start":5103,"text":"i"}],"scope_end_beyond_hard_boundary":true,"signature_end":5106,"signature_sha256":"a5d2119b4e4c6efab84b34c797ff9a1cccf06daad1aa6dcbe346c40a20b59037","signature_start":5084},"qualified_row":{"classification":"FUNCTION_PARAMETER_REFERENCE","owner":{"binding_kind":"FUNCTION_PARAMETER","function_name":"R","hard_scope_proof_end":5219,"origin":5099,"parameter_index":2,"parameters":[{"end":5096,"start":5095,"text":"e"},{"end":5098,"start":5097,"text":"t"},{"end":5100,"start":5099,"text":"n"},{"end":5102,"start":5101,"text":"s"},{"end":5104,"start":5103,"text":"i"}],"scope_end_beyond_hard_boundary":true,"signature_end":5106,"signature_sha256":"a5d2119b4e4c6efab84b34c797ff9a1cccf06daad1aa6dcbe346c40a20b59037","signature_start":5084},"source_window":{"end":5219,"sha256":"094a908b0677abe25f164bfc4a2e87617e84ef76fee8e0ec3dcdb87034741914","start":4932,"text":"se\"object\":return Array.isArray(e)?\"array\":\"object\";case\"string\":return e.length>100?\"string\":`\"${e.split('\"').join('\\\\\"')}\"`;default:return String(e)}}function R(e,t,n,s,i){let o=n.localName;if(n.repeated){if((0,r.vA)(\"map\"!=n.kind),null===t)return;if(!Array.isArray(t))throw new Error("},"token_start":5112},"qualified_token":5112,"qualified_under_origin":5099,"source_reread":false,"version":"PROTO3_N5112_REFERENCE_GSV2_V1"},"state_sha256":"e0391964e3365c272e430d78a7820f8221967cf29dcb87fda140c6e8f4de6baa","version":"GATE4_PROTO3_N5112_REFERENCE_GSV2_V1"}
```

## Evidence

Evidence SHA256: `5772cbdc6c6bb9b4a8368471740414478766572a3dc91b5eec21d21d8e8ea6e4`

```json
{"authority_sha256":"7c071c12bef1bcb71989d2936c69dd169eb2053150075a76d7c434701fc44864","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"next_token_5127_qualified":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","proto3_complete":false,"proto3_source_reread":false,"template_5219_crossed":false,"token_5112_qualified":true,"version":"GATE4_PROTO3_N5112_REFERENCE_GSV2_V1_EVIDENCE"}
```

## Boundary

The committed token-5099 authority already proves function R parameter n and freezes the bounded n population 5099, 5112, 5127, and 5158. Token 5112 is therefore qualified without rereading proto3 source as a reference to parameter n at 5099. Its frozen source context is n.localName. Token 5127 remains unqualified and the hard template boundary at 5219 remains uncrossed.
