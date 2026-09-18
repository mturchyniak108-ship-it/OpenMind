# Cursor OTEL Gate-4 proto3 token 6267 reference GSV2

Date: 2026-09-16

## Status

- module: ../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js
- token: 6267
- classification: FUNCTION_PARAMETER_REFERENCE
- exact expression: switch(n.V.kind)
- member access: n.V.kind
- owner function: R
- owner origin: 5099
- function R active at token: YES
- proto3 source reread: NO
- next frontier start: 6268
- next frontier kind: POST_TOKEN_LEXICAL_DISCOVERY_REQUIRED
- next frontier qualified: NO
- proto3 complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO

## Authority

Authority SHA256: `45c82ea43a5962aa6f54c0ff38ad505fa1600f1cdbe9b0af2dff28f18bd68cf6`

```json
{"state":{"current_authority":{"authority_sha256":"5f06b9d5cabb3b10753f01ff1c33661094d3056b6f8717f0155dec579705ac74","document":"docs/CURSOR_OTEL_GATE4_PROTO3_POST6229_LEXICAL_DISCOVERY_GSV2_2026-09-16.md","document_sha256":"69ff92c728f7f8222a909bf2c70ea76d6b0597bed5594ecf285fcfb11c605b8a"},"module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js","next_frontier":{"frontier_kind":"POST_TOKEN_LEXICAL_DISCOVERY_REQUIRED","owner_origin":5099,"preceding_qualified_token":6267,"source_reread":false,"source_window":{"end":6363,"sha256":"3cf0fac65bf2471473b9fd67015485bb4dea3ed46d31718ed4d77e1e7a0f9980","start":6245,"text":"),new Error(r)}switch(n.V.kind){case\"message\":r[a]=n.V.T.fromJson(o,s);break;case\"enum\":const e=P(n.V.T,o,s.ignoreUnkn"},"start":6268,"token_start":6268},"owner":{"binding_kind":"FUNCTION_PARAMETER","function_name":"R","hard_scope_proof_end":5219,"origin":5099,"parameter_index":2,"parameters":[{"end":5096,"start":5095,"text":"e"},{"end":5098,"start":5097,"text":"t"},{"end":5100,"start":5099,"text":"n"},{"end":5102,"start":5101,"text":"s"},{"end":5104,"start":5103,"text":"i"}],"scope_end_beyond_hard_boundary":true,"signature_end":5106,"signature_sha256":"a5d2119b4e4c6efab84b34c797ff9a1cccf06daad1aa6dcbe346c40a20b59037","signature_start":5084},"qualified_row":{"classification":"FUNCTION_PARAMETER_REFERENCE","exact_expression":"switch(n.V.kind)","member_access":"n.V.kind","owner":{"binding_kind":"FUNCTION_PARAMETER","function_name":"R","hard_scope_proof_end":5219,"origin":5099,"parameter_index":2,"parameters":[{"end":5096,"start":5095,"text":"e"},{"end":5098,"start":5097,"text":"t"},{"end":5100,"start":5099,"text":"n"},{"end":5102,"start":5101,"text":"s"},{"end":5104,"start":5103,"text":"i"}],"scope_end_beyond_hard_boundary":true,"signature_end":5106,"signature_sha256":"a5d2119b4e4c6efab84b34c797ff9a1cccf06daad1aa6dcbe346c40a20b59037","signature_start":5084},"scope_proof":{"brace_rows":[{"absolute_start":6259,"depth_after":3,"kind":"CLOSE"}],"depth_at_target":3,"minimum_depth":3},"source_window":{"end":6363,"sha256":"3cf0fac65bf2471473b9fd67015485bb4dea3ed46d31718ed4d77e1e7a0f9980","start":6245,"text":"),new Error(r)}switch(n.V.kind){case\"message\":r[a]=n.V.T.fromJson(o,s);break;case\"enum\":const e=P(n.V.T,o,s.ignoreUnkn"},"token_start":6267},"qualified_token":6267,"qualified_under_origin":5099,"source_reread":false,"version":"PROTO3_N6267_REFERENCE_GSV2_V1"},"state_sha256":"8100d350b600747372e5ffdf3805764a5438ec5f431e03803a69bb831b1ac979","version":"GATE4_PROTO3_N6267_REFERENCE_GSV2_V1"}
```

## Evidence

Evidence SHA256: `6ad6555b7c7f58f76c31badae1b483055713c8a40025ed63872f265f038222db`

```json
{"authority_sha256":"45c82ea43a5962aa6f54c0ff38ad505fa1600f1cdbe9b0af2dff28f18bd68cf6","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"next_frontier_qualified":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","proto3_complete":false,"proto3_source_reread":false,"token_6267_qualified":true,"version":"GATE4_PROTO3_N6267_REFERENCE_GSV2_V1_EVIDENCE"}
```

## Boundary

The committed post6229 discovery freezes token 6267 without ownership. The committed template6229 authority supplies function R parameter n at origin 5099 and active scope depth 4. The exact committed span from 6245 to 6267 is reverified from the frozen source window. The closing brace at 6259 reduces lexical depth from 4 to 3 while keeping function R active. No intervening n binding hazard is present. Token 6267 is qualified only as n.V.kind in switch(n.V.kind). No frontier after token end 6268 is discovered or qualified.
