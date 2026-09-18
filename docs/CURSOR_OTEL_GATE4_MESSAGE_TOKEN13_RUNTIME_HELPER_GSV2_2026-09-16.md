# Cursor OTEL Gate-4 message token 13 runtime helper GSV2

Date: 2026-09-16

## Status

- module: ../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/message.js
- token 13 classification: WEBPACK_RUNTIME_HELPER_PROPERTY_ACCESS
- exact statement: n.d(t,{Q:()=>r});
- next frontier token: 190
- next frontier qualified: NO
- template literal hazard count: 1
- template literal hazard crossed: NO
- message.js complete: NO
- proto3 complete: NO
- Gate-4 closed: NO
- Gate 5 evaluated: NO
- JavaScript executed: NO

## Authority

Authority SHA256: `e008e942eed9c652f0ccc37fed6bbacd35f00e261c334afbfdaa09ad9a5a5922`

```json
{"state":{"current_entry_authority":{"block_sha256":"ab726cc93c7aa995052af732a3ceefa59d484c36f71b0dc5de8e4240922bfac9","document":"docs/CURSOR_OTEL_GATE4_MESSAGE_DEPENDENCY_ENTRY_REUSE_FIRST_GSV2_2026-09-16.md","document_sha256":"c97a7850c444b46ac2252424d39f415a6fc4bb6002cdc5f97ed14415d7a4d06c"},"module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/message.js","next_frontier":{"frontier_kind":"UNRESOLVED_NONCALL_TOKEN","source_window":{"end":390,"sha256":"d3b9e9b73edc97eda6ac0946565db805f5fae5fcc1a0f8025a497a9fc6350196","start":110,"text":"e)}clone(){return this.getType().runtime.util.clone(this)}fromBinary(e,t){const n=this.getType().runtime.bin,r=n.makeReadOptions(t);return n.readMessage(this,r.readerFactory(e),e.byteLength,r),this}fromJson(e,t){const n=this.getType(),r=n.runtime.json,s=r.makeReadOptions(t);retur"},"token_start":190},"qualified_token":{"classification":"WEBPACK_RUNTIME_HELPER_PROPERTY_ACCESS","helper_property":"d","source_window":{"end":213,"sha256":"182d736c8e8b677b85b58c133d5f1086dbf1a0492b2628d5b639fc23e9454cce","start":0,"text":"\"use strict\";n.d(t,{Q:()=>r});class r{equals(e){return this.getType().runtime.util.equals(this.getType(),this,e)}clone(){return this.getType().runtime.util.clone(this)}fromBinary(e,t){const n=this.getType().runtim"},"statement_end":30,"statement_sha256":"237c9df35ba1135388d89f24e14d0da930f3e4d96809131e1097712777666fa0","statement_start":13,"token_start":13},"record":{"body_bytes":1093,"body_chars":1093,"body_sha256":"2ebcc3eb97d4981d4162bde34f8410350b801dda22e5a0211d33834a32ffccb9","header_end":3352739,"header_start":3352627,"module":"../../node_modules/.pnpm/@bufbuild+protobuf@1.10.1/node_modules/@bufbuild/protobuf/dist/esm/message.js","next_character":",","record_end":3353833,"record_sha256":"a9f324429ad4e207e8b9cf06af05273d5304d4e5fca2e4bb381b89d3f5e68600","record_start":3352627,"require_identifier":"n"},"template_hazard":{"first_template_index":494,"template_count":1},"version":"MESSAGE_TOKEN13_RUNTIME_HELPER_GSV2_V1"},"state_sha256":"4bd7bc952dcc85d3adf20380e90656379ef37a5c24151bffcaada9fc900bc7f6","version":"GATE4_MESSAGE_TOKEN13_RUNTIME_HELPER_GSV2_V1"}
```

## Evidence

Evidence SHA256: `5dd8cebf8aeb4f61a6d9ece667f0d30fc442a7ec8740849b6d40a227aeecb091`

```json
{"authority_sha256":"e008e942eed9c652f0ccc37fed6bbacd35f00e261c334afbfdaa09ad9a5a5922","cursor_sha256":"890a77344da6c1a0be78de34e92ae292369219c7700ca46f2df540f20c45c054","gate4_closed":false,"gate5_evaluated":false,"javascript_executed":false,"message_complete":false,"next_token_190_qualified":false,"otel_authority_sha256":"145c74d23924fde9a0337dd5c291a97e27eff2b6f872b84100ec716f63fa387c","proto3_complete":false,"template_hazard_crossed":false,"token_13_qualified":true,"version":"GATE4_MESSAGE_TOKEN13_RUNTIME_HELPER_GSV2_V1_EVIDENCE"}
```

## Boundary

Token 13 is proven as webpack runtime helper property access n.d. Frozen token 190 is preserved as the next unresolved ownership frontier. The known message.js template literal hazard remains frozen and is not crossed by this qualification step.
