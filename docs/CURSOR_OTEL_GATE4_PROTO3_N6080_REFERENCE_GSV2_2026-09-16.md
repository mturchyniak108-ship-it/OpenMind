# Cursor OTEL Gate-4 proto3 token 6080 reference GSV2

Date: 2026-09-16

## Status

- module: ../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js
- token: 6080
- classification: FUNCTION_PARAMETER_REFERENCE
- exact expression: Q(n.K,e)
- member access: n.K
- owner function: R
- owner origin: 5099
- function R active at token: YES
- proto3 source reread: NO
- next frontier start: 6081
- next frontier kind: POST_TOKEN_LEXICAL_DISCOVERY_REQUIRED
- next frontier qualified: NO
- proto3 complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO

## Authority

Authority SHA256: `414084e1e54312dc3762bac1942519a9b0f0b99e7e2ed68a80ee956f31c338b4`

```json
{"state":{"current_authority":{"authority_sha256":"793e857ad3845b547af4d0b09153c25bfa91884e9e1a158b937cba8a4e3af7de","document":"docs/CURSOR_OTEL_GATE4_PROTO3_POST5993_LEXICAL_DISCOVERY_GSV2_2026-09-16.md","document_sha256":"204c2e67fc1ae63ae3712bbd8015532652b55100b0e9a02c1ff8cb6fbf843a47"},"module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js","next_frontier":{"frontier_kind":"POST_TOKEN_LEXICAL_DISCOVERY_REQUIRED","owner_origin":5099,"preceding_qualified_token":6080,"source_reread":false,"source_window":{"end":6176,"sha256":"98c87cf2890f6469db2e9d1141e3f9abbe1bd916139ec13578c1e8764c7dadb3","start":6064,"text":");let a;try{a=Q(n.K,e)}catch(e){let r=`cannot decode map key for field ${i.typeName}.${n.name} from JSON: ${B(t)"},"start":6081,"token_start":6081},"owner":{"binding_kind":"FUNCTION_PARAMETER","function_name":"R","hard_scope_proof_end":5219,"origin":5099,"parameter_index":2,"parameters":[{"end":5096,"start":5095,"text":"e"},{"end":5098,"start":5097,"text":"t"},{"end":5100,"start":5099,"text":"n"},{"end":5102,"start":5101,"text":"s"},{"end":5104,"start":5103,"text":"i"}],"scope_end_beyond_hard_boundary":true,"signature_end":5106,"signature_sha256":"a5d2119b4e4c6efab84b34c797ff9a1cccf06daad1aa6dcbe346c40a20b59037","signature_start":5084},"qualified_row":{"classification":"FUNCTION_PARAMETER_REFERENCE","exact_expression":"Q(n.K,e)","member_access":"n.K","owner":{"binding_kind":"FUNCTION_PARAMETER","function_name":"R","hard_scope_proof_end":5219,"origin":5099,"parameter_index":2,"parameters":[{"end":5096,"start":5095,"text":"e"},{"end":5098,"start":5097,"text":"t"},{"end":5100,"start":5099,"text":"n"},{"end":5102,"start":5101,"text":"s"},{"end":5104,"start":5103,"text":"i"}],"scope_end_beyond_hard_boundary":true,"signature_end":5106,"signature_sha256":"a5d2119b4e4c6efab84b34c797ff9a1cccf06daad1aa6dcbe346c40a20b59037","signature_start":5084},"scope_proof":{"brace_rows":[{"absolute_start":6075,"depth_after":4,"kind":"OPEN"}],"depth_at_target":4,"minimum_depth":3},"source_window":{"end":6176,"sha256":"98c87cf2890f6469db2e9d1141e3f9abbe1bd916139ec13578c1e8764c7dadb3","start":6064,"text":");let a;try{a=Q(n.K,e)}catch(e){let r=`cannot decode map key for field ${i.typeName}.${n.name} from JSON: ${B(t)"},"token_start":6080},"qualified_token":6080,"qualified_under_origin":5099,"source_reread":false,"version":"PROTO3_N6080_REFERENCE_GSV2_V1"},"state_sha256":"1d22f6345528ecb1e4dc84384e5dc179d5f36b2a132310db0252e6d17c19cb3e","version":"GATE4_PROTO3_N6080_REFERENCE_GSV2_V1"}
```

## Evidence

Evidence SHA256: `f9a4bc9f64bef96d14f32a17beba4f14c2e38cad6a0ea40226aada443f615393`

```json
{"authority_sha256":"414084e1e54312dc3762bac1942519a9b0f0b99e7e2ed68a80ee956f31c338b4","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"next_frontier_qualified":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","proto3_complete":false,"proto3_source_reread":false,"token_6080_qualified":true,"version":"GATE4_PROTO3_N6080_REFERENCE_GSV2_V1_EVIDENCE"}
```

## Boundary

The committed post5993 discovery freezes token 6080 without ownership. The committed template5993 authority supplies function R parameter n at origin 5099 and active scope depth 3. The committed frozen span from 6064 to 6080 contains the try block opening brace at 6075, raising active scope depth to 4 at token 6080. No intervening n binding is present. Token 6080 is qualified only as n.K in Q(n.K,e). No frontier after token end 6081 is discovered or qualified.
