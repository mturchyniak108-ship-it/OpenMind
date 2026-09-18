# Cursor OTEL Gate-4 proto3 token 5127 reference GSV2

Date: 2026-09-16

## Status

- module: ../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js
- owner origin: 5099
- owner binding: FUNCTION_PARAMETER
- owner function: R
- token 5127: FUNCTION_PARAMETER_REFERENCE
- exact context: n.repeated
- source reread: NO
- next frontier token: 5158
- token 5158 qualified: NO
- next frozen context: n.kind
- hard template boundary: 5219
- template boundary crossed: NO
- proto3 complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO
- JavaScript executed: NO

## Authority

Authority SHA256: `d8922fd4abbf6446a86745a342b66dc19daa2e2a9d01e41f8b4f55b22747f9a3`

```json
{"state":{"bounded_local_n_tokens":[5099,5112,5127,5158],"current_authority":{"authority_sha256":"7c071c12bef1bcb71989d2936c69dd169eb2053150075a76d7c434701fc44864","document":"docs/CURSOR_OTEL_GATE4_PROTO3_N5112_REFERENCE_GSV2_2026-09-16.md","document_sha256":"f202ffe54317ddb435566efd86b7e8223c928401cc64907c16af3579d109c5c3"},"first_future_template":5219,"module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js","next_frontier":{"frontier_kind":"FUNCTION_PARAMETER_REFERENCE_UNQUALIFIED","hard_template_boundary":5219,"owner_origin":5099,"preceding_qualified_token":5127,"source_window":{"end":5219,"sha256":"094a908b0677abe25f164bfc4a2e87617e84ef76fee8e0ec3dcdb87034741914","start":4932,"text":"se\"object\":return Array.isArray(e)?\"array\":\"object\";case\"string\":return e.length>100?\"string\":`\"${e.split('\"').join('\\\\\"')}\"`;default:return String(e)}}function R(e,t,n,s,i){let o=n.localName;if(n.repeated){if((0,r.vA)(\"map\"!=n.kind),null===t)return;if(!Array.isArray(t))throw new Error("},"token_start":5158},"owner":{"binding_kind":"FUNCTION_PARAMETER","function_name":"R","hard_scope_proof_end":5219,"origin":5099,"parameter_index":2,"parameters":[{"end":5096,"start":5095,"text":"e"},{"end":5098,"start":5097,"text":"t"},{"end":5100,"start":5099,"text":"n"},{"end":5102,"start":5101,"text":"s"},{"end":5104,"start":5103,"text":"i"}],"scope_end_beyond_hard_boundary":true,"signature_end":5106,"signature_sha256":"a5d2119b4e4c6efab84b34c797ff9a1cccf06daad1aa6dcbe346c40a20b59037","signature_start":5084},"qualified_row":{"classification":"FUNCTION_PARAMETER_REFERENCE","owner":{"binding_kind":"FUNCTION_PARAMETER","function_name":"R","hard_scope_proof_end":5219,"origin":5099,"parameter_index":2,"parameters":[{"end":5096,"start":5095,"text":"e"},{"end":5098,"start":5097,"text":"t"},{"end":5100,"start":5099,"text":"n"},{"end":5102,"start":5101,"text":"s"},{"end":5104,"start":5103,"text":"i"}],"scope_end_beyond_hard_boundary":true,"signature_end":5106,"signature_sha256":"a5d2119b4e4c6efab84b34c797ff9a1cccf06daad1aa6dcbe346c40a20b59037","signature_start":5084},"source_window":{"end":5219,"sha256":"094a908b0677abe25f164bfc4a2e87617e84ef76fee8e0ec3dcdb87034741914","start":4932,"text":"se\"object\":return Array.isArray(e)?\"array\":\"object\";case\"string\":return e.length>100?\"string\":`\"${e.split('\"').join('\\\\\"')}\"`;default:return String(e)}}function R(e,t,n,s,i){let o=n.localName;if(n.repeated){if((0,r.vA)(\"map\"!=n.kind),null===t)return;if(!Array.isArray(t))throw new Error("},"token_start":5127},"qualified_token":5127,"qualified_under_origin":5099,"source_reread":false,"version":"PROTO3_N5127_REFERENCE_GSV2_V1"},"state_sha256":"6da51b5f393a4bba7490c1cc13a31d8fde4aabf944eadb30e82853fe08a65ff0","version":"GATE4_PROTO3_N5127_REFERENCE_GSV2_V1"}
```

## Evidence

Evidence SHA256: `10de999bdbd27919ef4f28956e8324194a67b6c5628663557b518bec57b6f010`

```json
{"authority_sha256":"d8922fd4abbf6446a86745a342b66dc19daa2e2a9d01e41f8b4f55b22747f9a3","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"next_token_5158_qualified":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","proto3_complete":false,"proto3_source_reread":false,"template_5219_crossed":false,"token_5127_qualified":true,"version":"GATE4_PROTO3_N5127_REFERENCE_GSV2_V1_EVIDENCE"}
```

## Boundary

The committed token-5112 authority preserves function R parameter n at origin 5099 and freezes the bounded n population 5099, 5112, 5127, and 5158. Token 5127 is qualified without rereading proto3 source as the n.repeated reference. Token 5158 remains unqualified in the frozen n.kind context. The hard template boundary at 5219 remains uncrossed.
