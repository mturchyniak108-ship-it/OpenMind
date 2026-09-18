# Cursor OTEL Gate-4 proto3 token 5767 reference GSV2

Date: 2026-09-16

## Status

- module: ../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js
- token: 5767
- classification: FUNCTION_PARAMETER_REFERENCE
- exact expression: "map"==n.kind
- member access: n.kind
- owner function: R
- owner origin: 5099
- active function R scope: YES
- proto3 source reread: NO
- next frontier start: 5768
- next frontier kind: POST_TOKEN_LEXICAL_DISCOVERY_REQUIRED
- next frontier qualified: NO
- proto3 complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO

## Authority

Authority SHA256: `35b7c212b3eb39eadb515f7c5de697d65cec79fd2e8dfdc539a9a3b16481afde`

```json
{"state":{"current_authority":{"authority_sha256":"ce18e160540e8180356fca947fa8dd9503b15ead5c8fdbef4b5be8ac0c65ba70","document":"docs/CURSOR_OTEL_GATE4_PROTO3_POST5718_LEXICAL_DISCOVERY_GSV2_2026-09-16.md","document_sha256":"99fb76e61212f2542ee2d8199f0ff9cf81e0c3c4a51ec2435aa9a5a863632349"},"module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js","next_frontier":{"frontier_kind":"POST_TOKEN_LEXICAL_DISCOVERY_REQUIRED","owner_origin":5099,"preceding_qualified_token":5767,"source_reread":false,"source_window":{"end":5863,"sha256":"daf183a320c378a896ff692b615dab4f5f1b35dc724e63fe35a68cb438365ca1","start":5734,"text":"),new Error(r)}}}}else if(\"map\"==n.kind){if(null===t)return;if(\"object\"!=typeof t||Array.isArray(t))throw new Error(`cannot decod"},"start":5768,"token_start":5768},"owner":{"binding_kind":"FUNCTION_PARAMETER","function_name":"R","hard_scope_proof_end":5219,"origin":5099,"parameter_index":2,"parameters":[{"end":5096,"start":5095,"text":"e"},{"end":5098,"start":5097,"text":"t"},{"end":5100,"start":5099,"text":"n"},{"end":5102,"start":5101,"text":"s"},{"end":5104,"start":5103,"text":"i"}],"scope_end_beyond_hard_boundary":true,"signature_end":5106,"signature_sha256":"a5d2119b4e4c6efab84b34c797ff9a1cccf06daad1aa6dcbe346c40a20b59037","signature_start":5084},"qualified_row":{"classification":"FUNCTION_PARAMETER_REFERENCE","exact_expression":"\"map\"==n.kind","member_access":"n.kind","owner":{"binding_kind":"FUNCTION_PARAMETER","function_name":"R","hard_scope_proof_end":5219,"origin":5099,"parameter_index":2,"parameters":[{"end":5096,"start":5095,"text":"e"},{"end":5098,"start":5097,"text":"t"},{"end":5100,"start":5099,"text":"n"},{"end":5102,"start":5101,"text":"s"},{"end":5104,"start":5103,"text":"i"}],"scope_end_beyond_hard_boundary":true,"signature_end":5106,"signature_sha256":"a5d2119b4e4c6efab84b34c797ff9a1cccf06daad1aa6dcbe346c40a20b59037","signature_start":5084},"scope_proof":{"brace_rows":[{"absolute_start":5748,"depth_after":4,"kind":"CLOSE"},{"absolute_start":5749,"depth_after":3,"kind":"CLOSE"},{"absolute_start":5750,"depth_after":2,"kind":"CLOSE"},{"absolute_start":5751,"depth_after":1,"kind":"CLOSE"}],"depth_at_target":1,"minimum_depth":1},"source_window":{"end":5863,"sha256":"daf183a320c378a896ff692b615dab4f5f1b35dc724e63fe35a68cb438365ca1","start":5734,"text":"),new Error(r)}}}}else if(\"map\"==n.kind){if(null===t)return;if(\"object\"!=typeof t||Array.isArray(t))throw new Error(`cannot decod"},"token_start":5767},"qualified_token":5767,"qualified_under_origin":5099,"source_reread":false,"version":"PROTO3_N5767_REFERENCE_GSV2_V1"},"state_sha256":"29fde2aeb2d1b2a71b10b3707ca30a3d03a72a5dcb469cc917436041f7bf8d4e","version":"GATE4_PROTO3_N5767_REFERENCE_GSV2_V1"}
```

## Evidence

Evidence SHA256: `03c4bae0fb2112fb200b123ca29386896dcd64402c429baf2fca605c7e339d2c`

```json
{"authority_sha256":"35b7c212b3eb39eadb515f7c5de697d65cec79fd2e8dfdc539a9a3b16481afde","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"next_frontier_qualified":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","proto3_complete":false,"proto3_source_reread":false,"token_5767_qualified":true,"version":"GATE4_PROTO3_N5767_REFERENCE_GSV2_V1_EVIDENCE"}
```

## Boundary

The committed post5718 discovery freezes token 5767 without ownership. The committed template5718 authority supplies function R parameter n at origin 5099 and its active lexical depth. The frozen span from template end 5734 to token 5767 is scanned without source reread, proving that function R remains open despite the intervening closing braces. No intervening n binding is present. Token 5767 is therefore qualified only as the n.kind reference in the expression "map"==n.kind. No token or template after token end 5768 is discovered or qualified by this authority.
