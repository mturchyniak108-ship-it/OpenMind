# Cursor OTEL Gate-4 proto3 token 5417 reference GSV2

Date: 2026-09-16

## Status

- module: ../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js
- owner origin: 5099
- owner function: R
- token 5417: FUNCTION_PARAMETER_REFERENCE
- exact expression: switch(n.kind)
- proto3 source reread: NO
- preceding template: 5344-5408
- scope continuity after template: );switch(
- next token: 5446
- token 5446 context: n.T.fromJson
- token 5446 qualified: NO
- proto3 complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO

## Authority

Authority SHA256: `415d9e7c9c0907227095c788f2c59195ba8f2ff3d16fdefb4b633bd12dc47cbe`

```json
{"state":{"current_authority":{"authority_sha256":"98cdbc677495369fddd147228e5a0dde03575c86ef3070376afe36c108e1f5f3","document":"docs/CURSOR_OTEL_GATE4_PROTO3_TEMPLATE5344_INTERPOLATION_GSV2_2026-09-16.md","document_sha256":"2866246e13a769987ecf2f3d7aa61eceba7432444edf8f61f8417229bc77f81e"},"module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/proto3.js","next_frontier":{"frontier_kind":"FUNCTION_PARAMETER_REFERENCE_UNQUALIFIED","owner_origin":5099,"preceding_qualified_token":5417,"source_reread":false,"source_window":{"end":5637,"sha256":"fe0b5b365634b6f00bf30a155aa0fd2af093143c33d35cc7b1e339e38c310405","start":5267,"text":"m JSON: ${B(t)}`);const a=e[o];for(const e of t){if(null===e)throw new Error(`cannot decode field ${i.typeName}.${n.name} from JSON: ${B(e)}`);switch(n.kind){case\"message\":a.push(n.T.fromJson(e,s));break;case\"enum\":const t=P(n.T,e,s.ignoreUnknownFields,!0);t!==b&&a.push(t);break;case\"scalar\":try{a.push(N(n.T,e,n.L,!0))}catch(t){let r=`cannot decode field ${i.typeName}"},"token_start":5446},"owner":{"binding_kind":"FUNCTION_PARAMETER","function_name":"R","hard_scope_proof_end":5219,"origin":5099,"parameter_index":2,"parameters":[{"end":5096,"start":5095,"text":"e"},{"end":5098,"start":5097,"text":"t"},{"end":5100,"start":5099,"text":"n"},{"end":5102,"start":5101,"text":"s"},{"end":5104,"start":5103,"text":"i"}],"scope_end_beyond_hard_boundary":true,"signature_end":5106,"signature_sha256":"a5d2119b4e4c6efab84b34c797ff9a1cccf06daad1aa6dcbe346c40a20b59037","signature_start":5084},"preceding_template":{"end":5408,"sha256":"91ebd91704211eeeaea48af6c0ab13ae8d77fb6bdb87a583c157cd908f6ae9c4","start":5344},"qualified_row":{"classification":"FUNCTION_PARAMETER_REFERENCE","exact_expression":"switch(n.kind)","owner":{"binding_kind":"FUNCTION_PARAMETER","function_name":"R","hard_scope_proof_end":5219,"origin":5099,"parameter_index":2,"parameters":[{"end":5096,"start":5095,"text":"e"},{"end":5098,"start":5097,"text":"t"},{"end":5100,"start":5099,"text":"n"},{"end":5102,"start":5101,"text":"s"},{"end":5104,"start":5103,"text":"i"}],"scope_end_beyond_hard_boundary":true,"signature_end":5106,"signature_sha256":"a5d2119b4e4c6efab84b34c797ff9a1cccf06daad1aa6dcbe346c40a20b59037","signature_start":5084},"source_window":{"end":5637,"sha256":"fe0b5b365634b6f00bf30a155aa0fd2af093143c33d35cc7b1e339e38c310405","start":5267,"text":"m JSON: ${B(t)}`);const a=e[o];for(const e of t){if(null===e)throw new Error(`cannot decode field ${i.typeName}.${n.name} from JSON: ${B(e)}`);switch(n.kind){case\"message\":a.push(n.T.fromJson(e,s));break;case\"enum\":const t=P(n.T,e,s.ignoreUnknownFields,!0);t!==b&&a.push(t);break;case\"scalar\":try{a.push(N(n.T,e,n.L,!0))}catch(t){let r=`cannot decode field ${i.typeName}"},"token_start":5417},"qualified_token":5417,"qualified_under_origin":5099,"scope_continuity":{"end":5417,"sha256":"d99f95a80ffd323d525ea684f3494e311d14f7ed4b8cf9225f99975110e4947e","start":5408,"text":");switch("},"source_reread":false,"version":"PROTO3_N5417_REFERENCE_GSV2_V1"},"state_sha256":"9208f0f8b5900ee22e68684c7ea95e8e91645ed3491d40715856e343e0da1042","version":"GATE4_PROTO3_N5417_REFERENCE_GSV2_V1"}
```

## Evidence

Evidence SHA256: `a4903a341d3e5b299455e5e9d45012f5c75f4a4e207b7528d2b8dc27e06e9716`

```json
{"authority_sha256":"415d9e7c9c0907227095c788f2c59195ba8f2ff3d16fdefb4b633bd12dc47cbe","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"next_token_5446_qualified":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","proto3_complete":false,"proto3_source_reread":false,"token_5417_qualified":true,"token_5446_advanced":false,"version":"GATE4_PROTO3_N5417_REFERENCE_GSV2_V1_EVIDENCE"}
```

## Boundary

The committed template-5344 authority already proves function R remains open at that template. The frozen frontier window proves exact continuity from template end 5408 to token 5417 as );switch( with no closing brace. Token 5417 is therefore qualified as the n reference in switch(n.kind), owned by function R parameter n at origin 5099. Token 5446 is frozen as n.T.fromJson and remains unqualified. No proto3 source reread or later-template advancement occurs.
